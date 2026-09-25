# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import frappe
import requests
from frappe import _

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

SYSTEM_PROMPT = (
	"You are an AI Lead Qualification Engine for TEAMPRO. "
	"Evaluate the lead based on HR (Recruitment, Staffing, Payroll, BGV) and "
	"IT (ERPNext, Apps, Web, KPO) service fit.\n\n"
	"VALIDATION MATRIX — evaluate each criterion as Yes or No:\n"
	"1. Company Validated: Is the company real, active, and verifiable? (weight: 1)\n"
	"2. Hiring Verified: Is there evidence of active hiring or staffing needs? (weight: 2)\n"
	"3. Relevant Contact: Is the contact a decision-maker (HR Head, CEO, CTRO, Procurement)? (weight: 1)\n"
	"4. Industry Fit: Does the company belong to an industry TEAMPRO serves (HR/IT outsourcing, manufacturing, tech, retail, healthcare, logistics)? (weight: 1)\n"
	"5. No Risk Flags: No bankruptcy, legal issues, scam signals, or out-of-scope requests? (weight: 1)\n\n"
	"SCORING (max 6 points):\n"
	"- Score = sum of weights where criterion is Yes\n"
	"- Convert to 0-100 scale: final_score = (raw_score / 6) * 100\n\n"
	"CATEGORIES:\n"
	"- Score >= 5 (raw) or >= 83 (scaled): Hot → Recommendation: Contact\n"
	"- Score >= 3 (raw) or >= 50 (scaled): Warm → Recommendation: Nurture\n"
	"- Score < 3 (raw) or < 50 (scaled): Cold → Recommendation: Drop\n\n"
	"Return JSON schema: "
	 '{"score": integer (0-100), '
	 '"rating": "Hot" | "Warm" | "Cold" | "Job Applicant", '
	 '"summary": "string (include which validation criteria passed/failed)", '
	 '"next_action": "string (Contact/Nurture/Drop + specific action)", '
	 '"validation": {"company_validated": boolean, "hiring_verified": boolean, "relevant_contact": boolean, "industry_fit": boolean, "no_risk_flags": boolean}, '
	 '"raw_score": integer (0-6)}'
	" Rule: If applying for a job or submitting a CV, mark rating as 'Job Applicant' and score as 0."
)

RATING_COLORS = {
	"Hot": "green",
	"Warm": "yellow",
	"Cold": "red",
	"Job Applicant": "gray",
}


@frappe.whitelist()
def validate_lead_ai(lead_id):
	"""
	Fetch Lead document, send data to Gemini API, save AI score/rating/summary/next_step.
	If rating == 'Job Applicant', set doc.status = 'Do Not Contact'.
	"""
	lead = frappe.get_doc("Lead", lead_id)

	lead_data = _build_lead_payload(lead)

	api_key = _get_gemini_api_key()
	if not api_key:
		frappe.log_error(
			title="AI Lead Validation: Missing Gemini API Key",
			message=f"Lead: {lead_id} — No API key found in site config or System Settings.",
		)
		frappe.throw(_("Gemini API key is not configured. Please set it in Site Config as 'gemini_api_key'."))

	try:
		result = _call_gemini_api(api_key, lead_data)
	except Exception as e:
		frappe.log_error(
			title="AI Lead Validation: Gemini API Error",
			message=f"Lead: {lead_id}\nError: {str(e)}",
		)
		frappe.throw(_("Failed to call Gemini API. Check error log for details."))

	# Save fields
	lead.db_set("custom_ai_score", result.get("score", 0))
	lead.db_set("custom_ai_rating", result.get("rating", "Cold"))
	lead.db_set("custom_ai_summary", result.get("summary", ""))
	lead.db_set("custom_ai_next_step", result.get("next_action", ""))

	if result.get("rating") == "Job Applicant":
		lead.db_set("status", "Do Not Contact")

	frappe.db.commit()

	return {
		"score": result.get("score", 0),
		"rating": result.get("rating", "Cold"),
		"summary": result.get("summary", ""),
		"next_action": result.get("next_action", ""),
		"color": RATING_COLORS.get(result.get("rating", "Cold"), "gray"),
		"validation": result.get("validation", {}),
		"raw_score": result.get("raw_score", 0),
	}


@frappe.whitelist()
def get_unvalidated_leads():
	"""Return all recent leads that have not been AI-validated yet.
	Filters to active lead statuses only for performance and relevance.
	"""
	leads = frappe.db.sql(
		"""
		SELECT name, lead_name, company_name, website, industry, no_of_employees,
			city, country, email_id, mobile_no, phone, job_title, status,
			custom_ai_score, custom_ai_rating, custom_ai_summary, custom_ai_next_step,
			creation
		FROM `tabLead`
		WHERE (custom_ai_score IS NULL OR custom_ai_score = '')
			AND status IN ('Lead', 'Open', 'Replied', 'Opportunity', 'Interested', 'Contacted')
		ORDER BY creation DESC
		""",
		as_dict=True,
	)
	return leads


@frappe.whitelist()
def get_validated_lead(lead_id):
	"""Return AI validation fields for a given lead."""
	lead = frappe.db.get_value(
		"Lead",
		lead_id,
		["name", "lead_name", "company_name", "email_id", "mobile_no", "phone",
		 "country", "status", "custom_ai_score", "custom_ai_rating",
		 "custom_ai_summary", "custom_ai_next_step"],
		as_dict=True,
	)
	if not lead:
		frappe.throw(_("Lead not found: {0}").format(lead_id))

	lead["color"] = RATING_COLORS.get(lead.get("custom_ai_rating") or "Cold", "gray")
	return lead


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_lead_payload(lead):
	"""Extract relevant fields from the Lead document for Gemini evaluation."""
	notes_text = ""
	if lead.get("notes"):
		notes_text = lead.notes

	return {
		"lead_name": lead.lead_name or lead.first_name or "",
		"company_name": lead.company_name or "",
		"job_title": lead.job_title or "",
		"email_id": lead.email_id or "",
		"mobile_no": lead.mobile_no or "",
		"phone": lead.phone or "",
		"country": lead.country or "",
		"city": lead.city or "",
		"industry": lead.industry or "",
		"request_type": lead.request_type or "",
		"type": lead.type or "",
		"notes": notes_text,
		"status": lead.status or "",
	}


def _get_gemini_api_key():
	"""Retrieve Gemini API key from site config or System Settings."""
	api_key = frappe.db.get_single_value("System Settings", "gemini_api_key")
	if not api_key:
		api_key = frappe.conf.get("gemini_api_key")
	return api_key


def _call_gemini_api(api_key, lead_data):
	"""
	Call Gemini API with structured JSON mode.
	Returns parsed dict with score, rating, summary, next_action.
	"""
	user_content = (
		f"Evaluate the following lead for TEAMPRO's HR and IT services.\n\n"
		f"Lead Details:\n"
		f"- Name: {lead_data.get('lead_name', 'N/A')}\n"
		f"- Company: {lead_data.get('company_name', 'N/A')}\n"
		f"- Job Title: {lead_data.get('job_title', 'N/A')}\n"
		f"- Email: {lead_data.get('email_id', 'N/A')}\n"
		f"- Mobile: {lead_data.get('mobile_no', 'N/A')}\n"
		f"- Phone: {lead_data.get('phone', 'N/A')}\n"
		f"- Country: {lead_data.get('country', 'N/A')}\n"
		f"- City: {lead_data.get('city', 'N/A')}\n"
		f"- Industry: {lead_data.get('industry', 'N/A')}\n"
		f"- Request Type: {lead_data.get('request_type', 'N/A')}\n"
		f"- Lead Type: {lead_data.get('type', 'N/A')}\n"
		f"- Notes: {lead_data.get('notes', 'N/A')}\n"
		f"- Current Status: {lead_data.get('status', 'N/A')}\n\n"
		f"Return the evaluation as JSON with fields: score, rating, summary, next_action."
	)

	payload = {
		"contents": [
			{
				"role": "user",
				"parts": [{"text": SYSTEM_PROMPT + "\n\n" + user_content}],
			}
		],
		"generationConfig": {
			"responseMimeType": "application/json",
			"responseSchema": {
				"type": "OBJECT",
				"properties": {
					"score": {"type": "INTEGER"},
					"rating": {
						"type": "STRING",
						"enum": ["Hot", "Warm", "Cold", "Job Applicant"],
					},
					"summary": {"type": "STRING"},
					"next_action": {"type": "STRING"},
					"validation": {
						"type": "OBJECT",
						"properties": {
							"company_validated": {"type": "BOOLEAN"},
							"hiring_verified": {"type": "BOOLEAN"},
							"relevant_contact": {"type": "BOOLEAN"},
							"industry_fit": {"type": "BOOLEAN"},
							"no_risk_flags": {"type": "BOOLEAN"},
						},
					},
					"raw_score": {"type": "INTEGER"},
				},
				"required": ["score", "rating", "summary", "next_action", "validation", "raw_score"],
			},
		},
	}

	url = f"{GEMINI_API_URL}?key={api_key}"
	headers = {"Content-Type": "application/json"}

	response = requests.post(url, headers=headers, json=payload, timeout=30)

	if response.status_code != 200:
		frappe.log_error(
			title="AI Lead Validation: Gemini API HTTP Error",
			message=f"Status: {response.status_code}\nResponse: {response.text}",
		)
		frappe.throw(_("Gemini API returned HTTP {0}: {1}").format(response.status_code, response.text[:500]))

	resp_json = response.json()

	# Extract text from the first candidate
	try:
		text_content = resp_json["candidates"][0]["content"]["parts"][0]["text"]
	except (KeyError, IndexError):
		frappe.log_error(
			title="AI Lead Validation: Unexpected Gemini Response",
			message=json.dumps(resp_json, indent=2),
		)
		frappe.throw(_("Unexpected response format from Gemini API."))

	# Parse JSON from the text content
	try:
		parsed = json.loads(text_content)
	except json.JSONDecodeError:
		frappe.log_error(
			title="AI Lead Validation: JSON Parse Error",
			message=f"Raw text: {text_content}",
		)
		frappe.throw(_("Failed to parse JSON response from Gemini API."))

	# Validate and clamp score
	score = int(parsed.get("score", 0))
	score = max(0, min(100, score))
	parsed["score"] = score

	# Validate rating
	valid_ratings = ["Hot", "Warm", "Cold", "Job Applicant"]
	if parsed.get("rating") not in valid_ratings:
		parsed["rating"] = "Cold"

	return parsed
