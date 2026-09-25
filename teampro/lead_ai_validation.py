# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
AI-based Lead Validation for ERPNext (Frappe framework).

This module hooks into the Lead DocType `before_save` event and asks an
external LLM (OpenAI or Google Gemini) to score and qualify the lead.
The result is written back into three custom fields on the Lead:

    - custom_ai_score      (Int, 0-100)
    - custom_ai_qualified  (Check / Boolean)
    - custom_ai_reasoning  (Small Text)

Design goals:
    * Never break the Lead save flow — every external call is wrapped in
      try/except and failures are logged via frappe.log_error.
    * API key is read from frappe.conf (site_config.json) or environment
      variables, never hard-coded.
    * Provider is selectable via `ai_lead_provider` site config key
      ("openai" or "gemini"). Defaults to "openai".
    * JSON parsing is defensive — strips code fences and falls back to a
      regex extraction if the model wraps the JSON in prose.
"""

import json
import os
import re

import frappe
import requests
from frappe import _

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------

DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL_OPENAI = "gpt-4o-mini"
DEFAULT_MODEL_GEMINI = "gemini-3.6-flash"
DEFAULT_TIMEOUT = 30  # seconds

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)

# Only re-run AI validation if the lead's substantive fields change, to
# avoid burning API quota on every minor save.
RELEVANT_FIELDS = (
    "lead_name",
    "company_name",
    "email_id",
    "phone",
    "mobile_no",
    "industry",
    "market_segment",
    "request_type",
    "type",
    "notes",
    "description",
    "country",
    "city",
    "job_title",
)

SYSTEM_PROMPT = (
    "You are an expert B2B Sales Development Representative (SDR). "
    "Evaluate the following lead and assess its sales potential based on "
    "company information, contact quality, industry fit, and any signals "
    "in the notes.\n\n"
    "Return a STRICTLY VALID JSON object — no markdown, no code fences, "
    "no commentary — with exactly these keys:\n"
    "  - score: integer between 0 and 100 (lead potential).\n"
    "  - qualified: boolean (true if score >= 60, false otherwise).\n"
    "  - reasoning: short text (max ~280 chars) explaining the assessment.\n"
    "Example:\n"
    '{"score": 72, "qualified": true, "reasoning": "Mid-market manufacturer '
    'with active hiring need and verified decision-maker contact."}'
)


# ---------------------------------------------------------------------------
# Public hook entry-point
# ---------------------------------------------------------------------------


def validate_lead_ai(doc, method=None):
    """
    Frappe `before_save` hook for the Lead DocType.

    Calls the configured LLM, parses the JSON response, and writes the
    result into the Lead's custom AI fields. Any failure is logged and
    silently ignored so the Lead save is never blocked.
    """
    # Only run on the Lead doctype (defensive — in case hooked broadly).
    if doc.doctype != "Lead":
        return

    # Skip if AI validation is explicitly disabled for this site.
    if not _is_enabled():
        return

    # Avoid re-scoring on every save unless something relevant changed
    # AND we don't already have a score. First insert always scores.
    if not doc.is_new() and not _has_relevant_change(doc):
        return

    try:
        payload = _build_lead_payload(doc)
        if not _payload_has_signal(payload):
            # Nothing meaningful to evaluate — leave fields untouched.
            return

        provider = _get_provider()
        api_key = _get_api_key(provider)
        if not api_key:
            frappe.log_error(
                title="AI Lead Validation: Missing API Key",
                message=(
                    "Lead: {0}\nProvider: {1}\n"
                    "No API key found. Set `openai_api_key` or "
                    "`gemini_api_key` in site_config.json or env."
                ).format(doc.name, provider),
            )
            return

        result = _call_llm(provider, api_key, payload)
        _apply_result(doc, result)

        frappe.msgprint(
            _("AI Lead Validation: score {0} ({1}).").format(
                result.get("score", 0),
                "Qualified" if result.get("qualified") else "Not Qualified",
            ),
            indicator="green" if result.get("qualified") else "orange",
            alert=True,
        )

    except Exception as e:  # noqa: BLE001 — broad catch is intentional
        frappe.log_error(
            title="AI Lead Validation: Unhandled Error",
            message="Lead: {0}\nError: {1}\n\n{2}".format(
                doc.name, str(e), frappe.get_traceback()
            ),
        )
        # Do NOT re-raise — Lead save must continue.


# ---------------------------------------------------------------------------
# Whitelisted manual trigger (optional — useful for re-scoring leads)
# ---------------------------------------------------------------------------


@frappe.whitelist()
def revalidate_lead(lead_id):
    """Manually re-run AI validation on an existing Lead."""
    lead = frappe.get_doc("Lead", lead_id)
    # Force re-evaluation by clearing the existing score.
    lead.custom_ai_score = None
    validate_lead_ai(lead, method="manual")
    lead.db_set(
        "custom_ai_score", lead.custom_ai_score or 0, update_modified=False
    )
    lead.db_set(
        "custom_ai_qualified",
        1 if lead.custom_ai_qualified else 0,
        update_modified=False,
    )
    lead.db_set(
        "custom_ai_reasoning",
        lead.custom_ai_reasoning or "",
        update_modified=False,
    )
    return {
        "score": lead.custom_ai_score,
        "qualified": bool(lead.custom_ai_qualified),
        "reasoning": lead.custom_ai_reasoning,
    }


# ---------------------------------------------------------------------------
# Internal helpers — configuration
# ---------------------------------------------------------------------------


def _is_enabled():
    """AI validation is on unless `ai_lead_enabled` is explicitly 0/false."""
    enabled = frappe.conf.get("ai_lead_enabled")
    if enabled is None:
        enabled = os.environ.get("AI_LEAD_ENABLED", "1")
    return str(enabled).lower() not in ("0", "false", "no", "off")


def _get_provider():
    provider = (
        frappe.conf.get("ai_lead_provider")
        or os.environ.get("AI_LEAD_PROVIDER")
        or DEFAULT_PROVIDER
    )
    return provider.lower()


def _get_api_key(provider):
    """Read the API key from site config first, then environment."""
    if provider == "gemini":
        return (
            frappe.conf.get("gemini_api_key")
            or os.environ.get("GEMINI_API_KEY")
        )
    # default: openai
    return (
        frappe.conf.get("openai_api_key")
        or os.environ.get("OPENAI_API_KEY")
    )


def _get_model(provider):
    if provider == "gemini":
        return (
            frappe.conf.get("ai_lead_model")
            or os.environ.get("AI_LEAD_MODEL_GEMINI")
            or DEFAULT_MODEL_GEMINI
        )
    return (
        frappe.conf.get("ai_lead_model")
        or os.environ.get("AI_LEAD_MODEL_OPENAI")
        or DEFAULT_MODEL_OPENAI
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


# ---------------------------------------------------------------------------
# Internal helpers — payload
# ---------------------------------------------------------------------------


def _build_lead_payload(lead):
    """
    Gather relevant fields from the Lead document.
    Uses .get() so missing custom/standard fields don't blow up.
    """
    notes = lead.get("notes") or lead.get("description") or ""
    return {
        "lead_name": lead.get("lead_name") or lead.get("first_name") or "",
        "company_name": lead.get("company_name") or "",
        "email_id": lead.get("email_id") or "",
        "phone": lead.get("phone") or lead.get("mobile_no") or "",
        "industry": lead.get("industry") or "",
        "market_segment": lead.get("market_segment") or "",
        "notes": notes,
    }


def _payload_has_signal(payload):
    """True if there's at least a company or contact to evaluate."""
    return bool(payload.get("company_name") or payload.get("email_id"))


def _has_relevant_change(doc):
    """True if any RELEVANT_FIELDS changed since last DB load."""
    try:
        db_values = doc.get_doc_before_save()
        if db_values is None:
            return True
        for field in RELEVANT_FIELDS:
            if (doc.get(field) or "") != (db_values.get(field) or ""):
                return True
        return False
    except Exception:
        # If we can't tell, err on the side of not re-scoring.
        return False


# ---------------------------------------------------------------------------
# Internal helpers — LLM calls
# ---------------------------------------------------------------------------


def _call_llm(provider, api_key, payload):
    """Dispatch to the configured provider and return a normalized dict."""
    if provider == "gemini":
        raw = _call_gemini(api_key, payload)
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
            OPENAI_URL, headers=headers, json=body, timeout=_get_timeout()
        )
    except requests.exceptions.RequestException as e:
        frappe.log_error(
            title="AI Lead Validation: OpenAI Request Failed",
            message="Error: {0}".format(str(e)),
        )
        return {}

    if resp.status_code != 200:
        frappe.log_error(
            title="AI Lead Validation: OpenAI HTTP Error",
            message="Status: {0}\nResponse: {1}".format(
                resp.status_code, resp.text[:1000]
            ),
        )
        return {}

    try:
        data = resp.json()
        return json.loads(data["choices"][0]["message"]["content"])
    except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        frappe.log_error(
            title="AI Lead Validation: OpenAI Parse Error",
            message="Error: {0}\nBody: {1}".format(str(e), resp.text[:1000]),
        )
        return {}


def _call_gemini(api_key, payload):
    user_content = _build_user_prompt(payload)
    model = _get_model("gemini")
    url = GEMINI_URL.format(model=model) + "?key={0}".format(api_key)
    body = {
        "contents": [
            {"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\n" + user_content}]}
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
        resp = requests.post(
            url, headers=headers, json=body, timeout=_get_timeout()
        )
    except requests.exceptions.RequestException as e:
        frappe.log_error(
            title="AI Lead Validation: Gemini Request Failed",
            message="Error: {0}".format(str(e)),
        )
        return {}

    if resp.status_code != 200:
        frappe.log_error(
            title="AI Lead Validation: Gemini HTTP Error",
            message="Status: {0}\nResponse: {1}".format(
                resp.status_code, resp.text[:1000]
            ),
        )
        return {}

    try:
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        frappe.log_error(
            title="AI Lead Validation: Gemini Parse Error",
            message="Error: {0}\nBody: {1}".format(str(e), resp.text[:1000]),
        )
        return {}


def _build_user_prompt(payload):
    return (
        "Evaluate the following B2B lead and return the JSON object only.\n\n"
        "Lead Details:\n"
        "- Lead Name: {lead_name}\n"
        "- Company: {company_name}\n"
        "- Email: {email_id}\n"
        "- Phone: {phone}\n"
        "- Industry: {industry}\n"
        "- Market Segment: {market_segment}\n"
        "- Notes: {notes}\n"
    ).format(
        lead_name=payload.get("lead_name") or "N/A",
        company_name=payload.get("company_name") or "N/A",
        email_id=payload.get("email_id") or "N/A",
        phone=payload.get("phone") or "N/A",
        industry=payload.get("industry") or "N/A",
        market_segment=payload.get("market_segment") or "N/A",
        notes=payload.get("notes") or "N/A",
    )


# ---------------------------------------------------------------------------
# Internal helpers — parsing & applying result
# ---------------------------------------------------------------------------


def _normalize_result(raw):
    """
    Convert whatever the LLM returned into a clean dict with the three
    expected keys. Tolerates missing keys, wrong types, and stray
    markdown fences.
    """
    if not isinstance(raw, dict):
        raw = {}

    # If the model returned a string under a "content"/"text" key, parse it.
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
