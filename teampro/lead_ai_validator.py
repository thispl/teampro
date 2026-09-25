# -*- coding: utf-8 -*-
"""
AI-based Lead Validation for ERPNext / Frappe.

Hooks into the Lead DocType ``before_save`` event and asks an external
LLM (OpenAI, Google Gemini, or Anthropic Claude) to score and qualify
the lead.  Results are written into four custom fields:

    - custom_ai_score              (Int, 0-100)
    - custom_ai_qualified          (Check / Boolean)
    - custom_ai_reasoning          (Small Text)
    - custom_ai_validation_status  (Select: Pending / Completed / Failed)

Design goals
------------
* Never block the Lead save — every external call is wrapped in
  try/except; on failure the status is set to "Failed" and the error
  is logged via ``frappe.log_error``.
* Skip re-validation when ``custom_ai_validation_status`` is already
  "Completed" (avoids burning API quota on every minor save).
* API key is read from ``frappe.conf.get("ai_api_key")`` first, then
  falls back to provider-specific keys (``openai_api_key``,
  ``gemini_api_key``, ``anthropic_api_key``) and environment variables.
* Provider is selectable via ``ai_lead_provider`` site-config key
  (``"openai"``, ``"gemini"``, or ``"anthropic"``).  Defaults to
  ``"gemini"`` to preserve existing setups.
"""

from __future__ import unicode_literals

import json
import os
import re

import frappe
import requests
from frappe import _

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------

DEFAULT_PROVIDER = "gemini"
DEFAULT_TIMEOUT = 30  # seconds

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "gemini": "gemini-3.6-flash",
    "anthropic": "claude-3-5-haiku-20241022",
}

API_URLS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "gemini": (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "{model}:generateContent"
    ),
    "anthropic": "https://api.anthropic.com/v1/messages",
}

# Fields whose change should trigger a re-validation even if the
# status was already "Completed".  If *any* of these change, we reset
# the status to "Pending" so the hook re-scores.
RELEVANT_FIELDS = (
    "lead_name",
    "company_name",
    "email_id",
    "mobile_no",
    "phone",
    "industry",
    "no_of_employees",
    "annual_revenue",
    "market_segment",
    "qualification_status",
    "request_type",
    "type",
    "notes",
    "description",
    "country",
    "city",
    "job_title",
)

SYSTEM_PROMPT = (
    "You are an expert B2B Lead Qualification Specialist. "
    "Evaluate the following lead based on company profile, contact "
    "quality, industry fit, company size, revenue signals, and any "
    "context in the notes.\n\n"
    "Return a STRICTLY VALID JSON object — no markdown, no code fences, "
    "no commentary — with exactly these keys:\n"
    "  - score: integer between 0 and 100 (lead potential).\n"
    "  - qualified: boolean (true if score >= 60, false otherwise).\n"
    "  - reasoning: 2-3 sentence summary explaining the score.\n"
    "Example:\n"
    '{"score": 72, "qualified": true, '
    '"reasoning": "Mid-market manufacturer with active hiring need and '
    'verified decision-maker contact. Revenue band aligns with our ICP. '
    'Recommended for immediate outreach."}'
)


# ===========================================================================
# 1. DocType Event Hook
# ===========================================================================


def validate_lead_with_ai(doc, method=None):
    """
    Frappe ``before_save`` hook for the Lead DocType.

    Calls the configured LLM, parses the JSON response, and writes the
    result into the Lead's custom AI fields.  Any failure is logged and
    silently ignored so the Lead save is never blocked.
    """
    if doc.doctype != "Lead":
        return

    # If a relevant field changed, reset status so we re-validate.
    if not doc.is_new() and _has_relevant_change(doc):
        doc.custom_ai_validation_status = "Pending"

    # Skip if already completed — avoid unnecessary API calls.
    if doc.get("custom_ai_validation_status") == "Completed":
        return

    # Mark as Pending while we attempt validation.
    doc.custom_ai_validation_status = "Pending"

    # Gather lead data.
    payload = _extract_lead_data(doc)
    if not _has_signal(payload):
        # Nothing meaningful to evaluate — leave as Pending.
        return

    provider = _get_provider()
    api_key = _get_api_key(provider)
    if not api_key:
        frappe.log_error(
            title="AI Lead Validator: Missing API Key",
            message=(
                "Lead: {0}\nProvider: {1}\n"
                "No API key found. Set `ai_api_key` (or provider-specific "
                "key) in site_config.json or environment variables."
            ).format(doc.name, provider),
        )
        doc.custom_ai_validation_status = "Failed"
        return

    try:
        result = _call_llm(provider, api_key, payload)
        if not result:
            doc.custom_ai_validation_status = "Failed"
            return

        _apply_result(doc, result)
        doc.custom_ai_validation_status = "Completed"

    except Exception as e:  # noqa: BLE001 — broad catch is intentional
        frappe.log_error(
            title="AI Lead Validator: Unhandled Error",
            message="Lead: {0}\nError: {1}\n\n{2}".format(
                doc.name, str(e), frappe.get_traceback()
            ),
        )
        doc.custom_ai_validation_status = "Failed"
        # Do NOT re-raise — Lead save must continue.


# ===========================================================================
# Whitelisted manual re-validation
# ===========================================================================


@frappe.whitelist()
def revalidate_lead(lead_id):
    """
    Manually re-run AI validation on an existing Lead.

    Forces re-evaluation by resetting the status to "Pending", then
    calls the hook logic and persists the result via ``db_set``.
    """
    lead = frappe.get_doc("Lead", lead_id)
    lead.custom_ai_validation_status = "Pending"
    validate_lead_with_ai(lead, method="manual")

    # Persist via db_set so the caller sees the result without a full
    # form save.
    lead.db_set("custom_ai_score", lead.custom_ai_score or 0,
                update_modified=False)
    lead.db_set("custom_ai_qualified",
                1 if lead.custom_ai_qualified else 0,
                update_modified=False)
    lead.db_set("custom_ai_reasoning", lead.custom_ai_reasoning or "",
                update_modified=False)
    lead.db_set("custom_ai_validation_status",
                lead.custom_ai_validation_status or "Pending",
                update_modified=False)

    return {
        "score": lead.custom_ai_score,
        "qualified": bool(lead.custom_ai_qualified),
        "reasoning": lead.custom_ai_reasoning,
        "validation_status": lead.custom_ai_validation_status,
    }


# ===========================================================================
# 2. Data Extraction & Prompt Construction
# ===========================================================================


def _extract_lead_data(doc):
    """
    Extract key lead details from the Lead document for AI evaluation.
    Uses ``.get()`` so missing fields don't raise.
    """
    notes = doc.get("notes") or doc.get("description") or ""
    return {
        "lead_name": doc.get("lead_name") or doc.get("first_name") or "",
        "company_name": doc.get("company_name") or "",
        "email_id": doc.get("email_id") or "",
        "mobile_no": doc.get("mobile_no") or doc.get("phone") or "",
        "industry": doc.get("industry") or "",
        "no_of_employees": doc.get("no_of_employees") or "",
        "annual_revenue": doc.get("annual_revenue") or "",
        "qualification_status": doc.get("qualification_status") or "",
        "notes": notes,
    }


def _build_user_prompt(payload):
    return (
        "Evaluate the following B2B lead and return the JSON object only.\n\n"
        "Lead Details:\n"
        "- Lead Name: {lead_name}\n"
        "- Company: {company_name}\n"
        "- Email: {email_id}\n"
        "- Mobile: {mobile_no}\n"
        "- Industry: {industry}\n"
        "- No. of Employees: {no_of_employees}\n"
        "- Annual Revenue: {annual_revenue}\n"
        "- Qualification Status: {qualification_status}\n"
        "- Notes: {notes}\n"
    ).format(
        lead_name=payload.get("lead_name") or "N/A",
        company_name=payload.get("company_name") or "N/A",
        email_id=payload.get("email_id") or "N/A",
        mobile_no=payload.get("mobile_no") or "N/A",
        industry=payload.get("industry") or "N/A",
        no_of_employees=payload.get("no_of_employees") or "N/A",
        annual_revenue=payload.get("annual_revenue") or "N/A",
        qualification_status=payload.get("qualification_status") or "N/A",
        notes=payload.get("notes") or "N/A",
    )


# ===========================================================================
# 3. API Integration & Security
# ===========================================================================


def _get_provider():
    provider = (
        frappe.conf.get("ai_lead_provider")
        or os.environ.get("AI_LEAD_PROVIDER")
        or DEFAULT_PROVIDER
    )
    return provider.lower()


def _get_api_key(provider):
    """
    Retrieve the API key.

    Priority:
      1. ``frappe.conf.get("ai_api_key")``  — spec-required key
      2. Provider-specific conf key
      3. Provider-specific environment variable
    """
    # 1. Generic key (per spec).
    key = frappe.conf.get("ai_api_key")
    if key:
        return key

    # 2. Provider-specific conf keys.
    provider_keys = {
        "openai": "openai_api_key",
        "gemini": "gemini_api_key",
        "anthropic": "anthropic_api_key",
    }
    key = frappe.conf.get(provider_keys.get(provider, ""))
    if key:
        return key

    # 3. Environment variables.
    env_keys = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    return os.environ.get(env_keys.get(provider, ""))


def _get_model(provider):
    return (
        frappe.conf.get("ai_lead_model")
        or os.environ.get("AI_LEAD_MODEL")
        or DEFAULT_MODELS.get(provider, "gpt-4o-mini")
    )


def _get_timeout():
    try:
        return int(
            frappe.conf.get("ai_lead_timeout")
            or os.environ.get("AI_LEAD_TIMEOUT")
            or DEFAULT_TIMEOUT
        )
    except (TypeError, ValueError):
        return DEFAULT_TIMEOUT


# ===========================================================================
# 4. LLM Calls (provider dispatch)
# ===========================================================================


def _call_llm(provider, api_key, payload):
    """Dispatch to the configured provider and return a normalized dict."""
    if provider == "gemini":
        raw = _call_gemini(api_key, payload)
    elif provider == "anthropic":
        raw = _call_anthropic(api_key, payload)
    else:
        raw = _call_openai(api_key, payload)
    return _normalize_result(raw)


def _call_openai(api_key, payload):
    user_content = _build_user_prompt(payload)
    body = {
        "model": _get_model("openai"),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(api_key),
    }
    try:
        resp = requests.post(
            API_URLS["openai"], headers=headers, json=body,
            timeout=_get_timeout(),
        )
    except requests.exceptions.RequestException as e:
        _log_api_error("OpenAI Request Failed", str(e))
        return {}

    if resp.status_code != 200:
        _log_api_error("OpenAI HTTP Error",
                       "Status: {0}\nResponse: {1}".format(
                           resp.status_code, resp.text[:1000]))
        return {}

    try:
        data = resp.json()
        return json.loads(data["choices"][0]["message"]["content"])
    except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        _log_api_error("OpenAI Parse Error",
                       "Error: {0}\nBody: {1}".format(str(e), resp.text[:1000]))
        return {}


def _call_gemini(api_key, payload):
    user_content = _build_user_prompt(payload)
    model = _get_model("gemini")
    url = API_URLS["gemini"].format(model=model) + "?key={0}".format(api_key)
    body = {
        "contents": [
            {"role": "user",
             "parts": [{"text": SYSTEM_PROMPT + "\n\n" + user_content}]}
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "score": {"type": "INTEGER"},
                    "qualified": {"type": "BOOLEAN"},
                    "reasoning": {"type": "STRING"},
                },
                "required": ["score", "qualified", "reasoning"],
            },
        },
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, headers=headers, json=body,
                             timeout=_get_timeout())
    except requests.exceptions.RequestException as e:
        _log_api_error("Gemini Request Failed", str(e))
        return {}

    if resp.status_code != 200:
        _log_api_error("Gemini HTTP Error",
                       "Status: {0}\nResponse: {1}".format(
                           resp.status_code, resp.text[:1000]))
        return {}

    try:
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        _log_api_error("Gemini Parse Error",
                       "Error: {0}\nBody: {1}".format(str(e), resp.text[:1000]))
        return {}


def _call_anthropic(api_key, payload):
    user_content = _build_user_prompt(payload)
    body = {
        "model": _get_model("anthropic"),
        "max_tokens": 512,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": user_content},
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    try:
        resp = requests.post(
            API_URLS["anthropic"], headers=headers, json=body,
            timeout=_get_timeout(),
        )
    except requests.exceptions.RequestException as e:
        _log_api_error("Anthropic Request Failed", str(e))
        return {}

    if resp.status_code != 200:
        _log_api_error("Anthropic HTTP Error",
                       "Status: {0}\nResponse: {1}".format(
                           resp.status_code, resp.text[:1000]))
        return {}

    try:
        data = resp.json()
        text = data["content"][0]["text"]
        return json.loads(text)
    except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        _log_api_error("Anthropic Parse Error",
                       "Error: {0}\nBody: {1}".format(str(e), resp.text[:1000]))
        return {}


# ===========================================================================
# 5. Error Handling, JSON Parsing & Result Application
# ===========================================================================


def _log_api_error(title, message):
    """Centralised error logger so call sites stay compact."""
    frappe.log_error(
        title="AI Lead Validator: {0}".format(title),
        message=message,
    )


def _normalize_result(raw):
    """
    Convert whatever the LLM returned into a clean dict with the three
    expected keys.  Tolerates missing keys, wrong types, and stray
    markdown fences.
    """
    if not isinstance(raw, dict):
        raw = {}

    # If the model returned a string under a common key, parse it.
    for key in ("content", "text", "output"):
        val = raw.get(key)
        if isinstance(val, str):
            raw = _safe_json_loads(val) or raw
            break

    score = _coerce_score(raw.get("score"))
    qualified = _coerce_bool(raw.get("qualified"), threshold=score >= 60)
    reasoning = _coerce_str(raw.get("reasoning"))[:1000]

    return {"score": score, "qualified": qualified, "reasoning": reasoning}


def _coerce_score(value):
    try:
        score = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, score))


def _coerce_bool(value, threshold=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "y", "qualified")
    return bool(threshold)


def _coerce_str(value):
    if value is None:
        return ""
    return str(value).strip()


def _safe_json_loads(text):
    """Parse JSON from a possibly-fenced / prose-wrapped string."""
    if not text:
        return None
    text = text.strip()
    # Strip markdown code fences ```json ... ``` or ``` ... ```
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    # Fallback: grab the first {...} block.
    if not text.startswith("{"):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _apply_result(doc, result):
    """Write the normalized result onto the Lead document in-memory."""
    if not result:
        return
    doc.custom_ai_score = result["score"]
    doc.custom_ai_qualified = 1 if result["qualified"] else 0
    doc.custom_ai_reasoning = result["reasoning"]


# ---------------------------------------------------------------------------
# Helpers — change detection
# ---------------------------------------------------------------------------


def _has_signal(payload):
    """True if there's at least a company or contact to evaluate."""
    return bool(payload.get("company_name") or payload.get("email_id"))


def _has_relevant_change(doc):
    """True if any RELEVANT_FIELDS changed since the last DB save."""
    try:
        db_values = doc.get_doc_before_save()
        if db_values is None:
            return True
        for field in RELEVANT_FIELDS:
            if (doc.get(field) or "") != (db_values.get(field) or ""):
                return True
        return False
    except Exception:
        return False
