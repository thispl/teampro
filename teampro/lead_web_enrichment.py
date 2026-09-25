# -*- coding: utf-8 -*-
"""
Web-enriched AI Lead Validation for Sales Follow Up (SFP).

Hybrid approach:
  1. Try to find the organization's website URL (from Lead fields or
     email domain in Lead Contacts / SFP Contacts).
  2. If a URL is found → scrape the website (homepage + /about) and
     send the extracted text + Lead data to Gemini for scoring.
  3. If no URL or scraping fails → use Gemini with Google Search
     grounding to search the company name and score based on search
     results.
  4. If Gemini also fails → fall back to Lead Contacts + SFP Contacts
     data and score with Gemini using only that data.
  5. If everything fails → log the error and leave the SFP untouched.

The result (score, rating, qualified, reasoning, summary, next_step,
validation_status) is written back to the SFP's 7 custom AI fields.
"""

from __future__ import unicode_literals

import json
import os
import re
import urllib.parse

import frappe
import requests
from bs4 import BeautifulSoup
from frappe import _

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)
SCRAPE_TIMEOUT = 15
GEMINI_TIMEOUT = 45
MAX_CONTENT_CHARS = 8000  # limit website text sent to Gemini
TEAMPRO_URL = "https://www.groupteampro.com"
TEAMPRO_PROFILE_CACHE_KEY = "teampro_company_profile"
TEAMPRO_PROFILE_CACHE_TTL = 86400  # 24 hours in seconds

FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "yahoo.co.in", "hotmail.com",
    "outlook.com", "rediffmail.com", "live.com", "icloud.com",
    "protonmail.com", "zoho.com",
}

SERVICE_LINE_NAMES = {
    "recruitment": "HR / Recruitment Services",
    "it_services": "IT Services",
    "food_products": "Food Products",
}

SERVICE_LINES = {
    "REC-I": "recruitment", "REC-D": "recruitment", "BCS": "recruitment",
    "R&S": "recruitment", "Payroll": "recruitment", "HRIT": "recruitment",
    "IT-SW": "it_services", "IT-IS": "it_services", "SCP": "it_services",
    "TGT": "it_services", "CMN": "it_services", "NL": "it_services",
    "TFP": "food_products", "EMS": "food_products",
}

SYSTEM_PROMPT = (
    "You are an expert B2B Lead Qualification Specialist for TEAMPRO, "
    "a company offering HR/Recruitment, IT, and Food Products (Trading) "
    "services.\n\n"
    "You will receive:\n"
    "  1. TEAMPRO's company profile (so you understand what TEAMPRO "
    "offers and can match the lead's needs to TEAMPRO's services).\n"
    "  2. Lead data from the ERP system.\n"
    "  3. SFP Remarks — notes from the sales team's interactions with "
    "the lead. These are a MINOR signal (10% weight) — use them as "
    "supporting context only, not as the primary scoring driver.\n"
    "  4. Optionally, web content scraped from the lead's company "
    "website or Google Search results.\n\n"
    "=== LVS SCORING FRAMEWORK (11 CHECKS, MAX 14 POINTS) ===\n"
    "You must evaluate the lead using the Lead Validation Scoring (LVS) "
    "framework. Answer each of the following 11 checks as Yes or No, "
    "then compute the total LVS score.\n\n"
    "--- GROUP A: BUSINESS VALIDATION (5 checks, max 6 pts) ---\n"
    "  1. Company Validated (weight: 1) — Does the company exist and is "
    "it a real, verifiable business? Check website, web data, or search "
    "results for evidence of a legitimate company.\n"
    "  2. Hiring Verified (weight: 2) — Is the company actively hiring? "
    "Look for job postings, careers pages, or hiring activity signals "
    "in web data. This is a HIGH-WEIGHT check.\n"
    "  3. Relevant Contact (weight: 1) — Is there a decision-maker or "
    "influencer contact available? Check if the contact designation is "
    "relevant (HR Manager, IT Head, CEO, Procurement, etc.).\n"
    "  4. Industry Fit (weight: 1) — Does the company's industry match "
    "TEAMPRO's service offerings? (HR/Recruitment for companies hiring, "
    "IT for tech needs, Food Products for F&B companies).\n"
    "  5. No Risk Flags (weight: 1) — Are there any red flags? "
    "Bankruptcy, scam reports, legal issues, negative reviews, or "
    "fraud signals. If any risk flag exists, answer No.\n\n"
    "--- GROUP B: FIRMGRAPHIC VALIDATION (6 checks, max 8 pts) ---\n"
    "IMPORTANT: For all Group B checks, you MUST source the data from "
    "WEB DATA (company website or Google Search results) — NOT from the "
    "ERP Lead fields. The ERP fields may be incomplete or outdated. "
    "Search the web for the actual company profile, LinkedIn data, "
    "business directories, news articles, and financial databases.\n\n"
    "  6. Industry & Sector (weight: 2) — Standard Industrial "
    "Classification (SIC) or NAICS code matching TEAMPRO's target "
    "verticals. Determine the sector code FROM WEB DATA — search for "
    "the company's industry classification, business description, and "
    "sector. Does the company's industry sector align with TEAMPRO's "
    "service lines? (e.g., manufacturing → IT/ERP; F&B → Food Products; "
    "any sector hiring → Recruitment). HIGH-WEIGHT check.\n"
    "  7. Company Size / Headcount (weight: 1) — Employee count FROM "
    "WEB DATA. Search for the company's headcount on LinkedIn, business "
    "directories (ZoomInfo, Apollo), or the company website. Classify "
    "as SMB (<50), Mid-Market (50-500), Enterprise (500+). Assess if "
    "the company size is suitable for TEAMPRO's services. Do NOT rely "
    "on the ERP 'no_of_employees' field — verify from web sources.\n"
    "  8. Annual Revenue (weight: 2) — Financial bandwidth FROM WEB "
    "DATA. Search for the company's revenue in business databases, "
    "news articles, financial reports, or industry benchmarks. If "
    "explicit revenue is not found, infer from web-sourced company "
    "size and industry sector. Assess if the company has sufficient "
    "revenue to be a viable customer. HIGH-WEIGHT check. Do NOT rely "
    "on the ERP 'annual_revenue' field.\n"
    "  9. Geographic Location (weight: 1) — Headquarters and operational "
    "locations FROM WEB DATA. Search for the company's registered "
    "address, office locations, and operational regions from their "
    "website, Google Maps, or business directories. Do NOT rely on the "
    "ERP 'city' or 'country' fields — verify from web sources. Does "
    "the company operate in regions where TEAMPRO can deliver services? "
    "(TEAMPRO operates in India, Oman, UAE, Saudi Arabia, Kuwait, "
    "Qatar, Bahrain, Iraq).\n"
    "  10. Tech Stack / Technographics (weight: 1) — Tools, frameworks, "
    "or cloud infrastructure the company currently uses. Verify "
    "compatibility or competitor usage. (e.g., using SAP → harder to "
    "sell ERP; using spreadsheets → ERP opportunity; using Workday → "
    "recruitment integration opportunity).\n"
    "  11. Ownership Type (weight: 1) — Public, private, venture-backed, "
    "bootstrap, or non-profit status. Assess if the ownership type is "
    "favorable for B2B sales (e.g., venture-backed companies have "
    "budget and growth mandate; public companies have procurement "
    "processes; non-profits may have limited budget).\n\n"
    "LVS Score = Sum of all 11 check weights for Yes answers.\n"
    "Maximum LVS Score = 14\n\n"
    "LVS Category and Recommendation:\n"
    "  LVS Score 10-14 → Hot → Contact\n"
    "  LVS Score 5-9   → Warm → Nurture\n"
    "  LVS Score 0-4   → Cold → Drop\n\n"
    "Map the LVS Score (0-14) to a 0-100 scale for the 'score' field:\n"
    "  14→100, 13→93, 12→86, 11→79, 10→71, 9→64, 8→57, 7→50, "
    "6→43, 5→36, 4→29, 3→21, 2→14, 1→7, 0→0\n\n"
    "Return a STRICTLY VALID JSON object — no markdown, no code fences — "
    "with exactly these keys:\n"
    "  - score: integer 0-100 (mapped from LVS score as above).\n"
    "  - rating: \"Hot\" (LVS 10-14), \"Warm\" (LVS 5-9), or \"Cold\" "
    "(LVS 0-4).\n"
    "  - qualified: boolean (true if LVS score >= 9).\n"
    "  - reasoning: MUST start with all 11 LVS checks in this format:\n"
    "    \"[LVS] Company Validated: Yes (1pt) | Hiring Verified: No "
    "(0pt) | Relevant Contact: Yes (1pt) | Industry Fit: Yes (1pt) | "
    "No Risk Flags: Yes (1pt) | Industry & Sector: Yes (2pts) | "
    "Company Size: Yes (1pt) | Annual Revenue: Yes (2pts) | "
    "Geographic Location: Yes (1pt) | Tech Stack: No (0pt) | "
    "Ownership Type: Yes (1pt) | LVS Score: 10/14\"\n"
    "    Then add pipe-separated (|) detail lines explaining each check, "
    "prefixed with categories: \"[Company] ...\", \"[Hiring] ...\", "
    "\"[Contact] ...\", \"[Industry] ...\", \"[Risk] ...\", "
    "\"[Sector] ...\", \"[Size] ...\", \"[Revenue] ...\", "
    "\"[Location] ...\", \"[TechStack] ...\", \"[Ownership] ...\", "
    "\"[Remarks] ...\" (remarks at 10% weight only).\n"
    "  - summary: 1-2 sentence plain-English summary including the LVS "
    "score and category.\n"
    "  - next_step: actionable recommendation matching the LVS "
    "Recommendation (Contact / Nurture / Drop) with brief context.\n"
    "  - data_source: \"website\" | \"google_search\" | \"contacts_only\" "
    "(indicates where the enrichment data came from).\n"
)


# ===========================================================================
# Main entry point
# ===========================================================================


@frappe.whitelist()
def enrich_and_validate_sfp(sfp_name):
    """
    Enrich a Sales Follow Up with web data and score it with Gemini.

    Handles both Lead-linked and Customer-linked SFPs.

    1. Find website URL from Lead/Customer fields or contact email domains.
    2. Scrape website if URL found.
    3. Call Gemini with scraped content.
    4. If no URL / scrape fails → Gemini with Google Search grounding.
    5. If Gemini fails → Gemini with contacts-only data.
    6. Write results back to the SFP's 7 AI fields.
    """
    sfp = frappe.get_doc("Sales Follow Up", sfp_name)

    # Determine whether this SFP is linked to a Lead or a Customer.
    party_from = sfp.get("party_from") or "Lead"
    party_name = sfp.get("party_name") or sfp.get("lead") or sfp.get("customer")

    if not party_name:
        frappe.throw(_("SFP {0} has no linked Lead or Customer.").format(sfp_name))

    if party_from == "Customer":
        party_doc = frappe.get_doc("Customer", party_name)
    else:
        party_doc = frappe.get_doc("Lead", party_name)

    service_code = sfp.get("service") or "REC-I"
    service_line = SERVICE_LINES.get(service_code, "recruitment")
    service_name = SERVICE_LINE_NAMES.get(service_line, "TEAMPRO Services")

    # Gather all available data.
    lead_data = _extract_party_data(party_doc, party_from)
    contacts_data = _get_contacts_data(party_doc, sfp, party_from)
    sfp_remarks = _get_sfp_remarks(sfp)

    # Fetch TEAMPRO's own company profile (cached for 24h).
    teampro_profile = _get_teampro_profile()

    # Mark as Pending while processing.
    frappe.db.set_value("Sales Follow Up", sfp_name,
                        "custom_ai_validation_status", "Pending",
                        update_modified=False)

    api_key = _get_gemini_api_key()
    if not api_key:
        _log_error("Web Enrichment: Missing API Key",
                   "SFP: {0}".format(sfp_name))
        _set_failed(sfp_name)
        return {"error": "Missing Gemini API key"}

    # Step 1: Try to find a website URL.
    website_url = _find_website_url(party_doc, contacts_data)
    frappe.log("Web Enrichment: website_url = {0}".format(website_url))

    web_content = None
    data_source = "contacts_only"

    # Step 2: Try to scrape the website.
    if website_url:
        web_content = _scrape_website(website_url)
        if web_content:
            data_source = "website"

    # Step 3: If no website content, try Gemini Google Search.
    if not web_content:
        frappe.log("Web Enrichment: no website content, trying Google Search")
        search_result = _gemini_google_search(
            api_key, lead_data, contacts_data, service_name
        )
        if search_result:
            web_content = search_result
            data_source = "google_search"

    # Step 4: Call Gemini for scoring with whatever data we have.
    try:
        result = _score_with_gemini(
            api_key, lead_data, contacts_data, web_content,
            data_source, service_name, service_code,
            sfp_remarks=sfp_remarks,
            teampro_profile=teampro_profile,
        )
    except Exception as e:
        _log_error("Web Enrichment: Gemini Scoring Error",
                   "SFP: {0}\nError: {1}\n{2}".format(
                       sfp_name, str(e), frappe.get_traceback()))
        _set_failed(sfp_name)
        return {"error": str(e)}

    if not result:
        _set_failed(sfp_name)
        return {"error": "Gemini returned empty result"}

    # Step 5: Write results back to SFP.
    _write_back_sfp(sfp_name, result)

    return result


# ===========================================================================
# Website URL discovery
# ===========================================================================


def _find_website_url(lead, contacts_data):
    """
    Find the organization's website URL from:
      1. Lead.website or Lead.web field
      2. Email domain from Lead Contacts or SFP Contacts
    """
    # 1. Check Lead website fields.
    url = (lead.get("website") or lead.get("web") or "").strip()
    if url:
        return _normalize_url(url)

    # 2. Derive from email domain in contacts.
    for contact in contacts_data:
        email = (contact.get("email_id") or "").strip()
        if email and "@" in email:
            domain = email.split("@")[-1].lower().strip()
            if domain not in FREE_EMAIL_DOMAINS:
                return _normalize_url(domain)

    return None


def _normalize_url(url):
    """Ensure URL has a scheme; bare domains get https:// prepended."""
    if not url:
        return None
    url = url.strip()
    if url.startswith("http://") or url.startswith("https://"):
        return url
    # Bare domain like "polkartlogistics.com"
    if "." in url and " " not in url:
        return "https://" + url
    return None


# ===========================================================================
# Website scraping
# ===========================================================================


def _scrape_website(url):
    """
    Fetch the homepage and /about page, extract visible text.
    Returns a string of up to MAX_CONTENT_CHARS chars, or None on failure.
    """
    texts = []

    # Fetch homepage.
    homepage_text = _fetch_and_extract(url)
    if homepage_text:
        texts.append("=== HOMEPAGE ===\n{0}".format(homepage_text))

    # Try /about, /about-us, /company pages.
    parsed = urllib.parse.urlparse(url)
    base = "{0}://{1}".format(parsed.scheme, parsed.netloc)
    for path in ["/about", "/about-us", "/company", "/who-we-are"]:
        about_url = base + path
        about_text = _fetch_and_extract(about_url)
        if about_text:
            texts.append("=== {0} ===\n{1}".format(path.upper(), about_text))
            break  # one about page is enough

    if not texts:
        return None

    content = "\n\n".join(texts)
    if len(content) > MAX_CONTENT_CHARS:
        content = content[:MAX_CONTENT_CHARS] + "\n...[truncated]"
    return content


def _fetch_and_extract(url):
    """Fetch a URL and extract visible text with BeautifulSoup."""
    try:
        resp = requests.get(
            url,
            timeout=SCRAPE_TIMEOUT,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            },
            allow_redirects=True,
        )
    except requests.exceptions.RequestException:
        return None

    if resp.status_code != 200:
        return None

    # Skip non-HTML responses.
    content_type = resp.headers.get("Content-Type", "")
    if "text/html" not in content_type and "application/xhtml" not in content_type:
        return None

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception:
        return None

    # Remove script, style, nav, footer, header tags.
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "noscript", "iframe", "form"]):
        tag.decompose()

    # Extract text.
    text = soup.get_text(separator=" ", strip=True)
    # Collapse whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    # Skip if too short (likely a JS-only page or error page).
    if len(text) < 100:
        return None

    return text[:4000]  # per-page limit


# ===========================================================================
# Gemini API calls
# ===========================================================================


def _get_gemini_api_key():
    return (
        frappe.conf.get("ai_api_key")
        or frappe.conf.get("gemini_api_key")
        or os.environ.get("GEMINI_API_KEY")
        or os.environ.get("AI_API_KEY")
    )


def _gemini_google_search(api_key, lead_data, contacts_data, service_name):
    """
    Use Gemini with Google Search grounding to find and analyze the
    company online.  Returns text content for the scoring prompt, or
    None on failure.
    """
    company = lead_data.get("company_name") or ""
    if not company:
        return None

    prompt = (
        "Search the web for information about this company and summarize "
        "what you find for B2B lead qualification purposes:\n\n"
        "Company: {company}\n"
        "Industry: {industry}\n"
        "Location: {city}, {country}\n\n"
        "Provide:\n"
        "1. Company description (what they do)\n"
        "2. Industry and sector\n"
        "3. Approximate company size if available\n"
        "4. Key services or products\n"
        "5. Any news, growth signals, or hiring activity\n"
        "6. Contact information found online (email, phone, address)\n"
    ).format(
        company=company,
        industry=lead_data.get("industry") or "N/A",
        city=lead_data.get("city") or "N/A",
        country=lead_data.get("country") or "N/A",
    )

    body = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ],
        "tools": [{"google_search": {}}],
    }

    url = GEMINI_URL.format(model=GEMINI_MODEL) + "?key={0}".format(api_key)
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(url, headers=headers, json=body,
                             timeout=GEMINI_TIMEOUT)
    except requests.exceptions.RequestException as e:
        _log_error("Web Enrichment: Google Search Request Failed", str(e))
        return None

    if resp.status_code != 200:
        _log_error("Web Enrichment: Google Search HTTP Error",
                   "Status: {0}\nResponse: {1}".format(
                       resp.status_code, resp.text[:1000]))
        return None

    try:
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Also extract grounding metadata (sources).
        metadata = data["candidates"][0].get("groundingMetadata", {})
        sources = []
        for chunk in metadata.get("groundingChunks", []):
            web = chunk.get("web", {})
            if web.get("title"):
                sources.append("{0} ({1})".format(
                    web["title"], web.get("uri", "")))
        if sources:
            text += "\n\nSources:\n" + "\n".join(sources[:5])
        return text
    except (KeyError, IndexError, ValueError) as e:
        _log_error("Web Enrichment: Google Search Parse Error",
                   "Error: {0}\nBody: {1}".format(str(e), resp.text[:1000]))
        return None


def _score_with_gemini(api_key, lead_data, contacts_data, web_content,
                       data_source, service_name, service_code,
                       sfp_remarks="", teampro_profile=""):
    """
    Call Gemini to score the lead using all available data.
    Returns a dict with score, rating, qualified, reasoning, summary,
    next_step, data_source.
    """
    # Build the user prompt.
    prompt_parts = [
        "Evaluate this B2B lead for: {0}\n".format(service_name),
        "Service Code: {0}\n".format(service_code),
    ]

    # Add TEAMPRO company profile first so the AI understands the context.
    if teampro_profile:
        prompt_parts.append("\n=== TEAMPRO COMPANY PROFILE ===")
        prompt_parts.append(teampro_profile)
        prompt_parts.append(
            "\nUse the above to understand what TEAMPRO offers and "
            "assess how well this lead's needs match TEAMPRO's services."
        )

    prompt_parts.append("\n=== LEAD DATA ===")
    prompt_parts.append("Company: {0}".format(lead_data.get("company_name") or "N/A"))
    prompt_parts.append("Lead Name: {0}".format(lead_data.get("lead_name") or "N/A"))
    prompt_parts.append("Industry: {0}".format(lead_data.get("industry") or "N/A"))
    prompt_parts.append("Employees: {0}".format(lead_data.get("no_of_employees") or "N/A"))
    prompt_parts.append("Annual Revenue: {0}".format(lead_data.get("annual_revenue") or "N/A"))
    prompt_parts.append("Territory: {0}".format(lead_data.get("territory") or "N/A"))
    prompt_parts.append("Country: {0}".format(lead_data.get("country") or "N/A"))
    prompt_parts.append("City: {0}".format(lead_data.get("city") or "N/A"))
    prompt_parts.append("Email: {0}".format(lead_data.get("email_id") or "N/A"))
    prompt_parts.append("Phone: {0}".format(lead_data.get("phone") or "N/A"))
    prompt_parts.append("Mobile: {0}".format(lead_data.get("mobile_no") or "N/A"))
    prompt_parts.append("Website: {0}".format(lead_data.get("website") or "N/A"))
    prompt_parts.append("Job Title: {0}".format(lead_data.get("job_title") or "N/A"))
    prompt_parts.append("Qualification Status: {0}".format(
        lead_data.get("qualification_status") or "N/A"))
    prompt_parts.append("Lead Status: {0}".format(lead_data.get("status") or "N/A"))
    prompt_parts.append("Market Segment: {0}".format(
        lead_data.get("market_segment") or "N/A"))

    # Add SFP remarks — minor signal (10% weight per LVS framework).
    if sfp_remarks:
        prompt_parts.append("\n=== SFP REMARKS (sales interaction notes — 10% weight) ===")
        prompt_parts.append(sfp_remarks)
        prompt_parts.append(
            "\nNOTE: These remarks are from the sales team's interactions. "
            "Use them as MINOR supporting context only (10% weight). "
            "Do NOT let remarks override the 11 LVS checks. The primary "
            "scoring must come from the LVS framework."
        )

    # Add contacts data — include designation for LVS "Relevant Contact" check.
    if contacts_data:
        prompt_parts.append("\n=== CONTACTS (from Lead Contacts + SFP) ===")
        for i, c in enumerate(contacts_data[:5], 1):
            prompt_parts.append(
                "  Contact {0}: {1} | {2} | {3} | service: {4}".format(
                    i,
                    c.get("person_name") or "N/A",
                    c.get("mobile") or "N/A",
                    c.get("email_id") or "N/A",
                    c.get("service") or "N/A",
                )
            )
        prompt_parts.append(
            "\nFor LVS Check 3 (Relevant Contact): assess if any contact "
            "is a decision-maker or influencer relevant to the service "
            "line (e.g., HR Manager for recruitment, IT Head for IT "
            "services, Procurement for food products)."
        )

    # Add web content.
    if web_content:
        prompt_parts.append("\n=== WEB DATA (source: {0}) ===".format(data_source))
        prompt_parts.append(web_content)
        prompt_parts.append(
            "\nIMPORTANT: All Group B checks (6-11) MUST be evaluated "
            "from this WEB DATA, not from the ERP Lead fields above.\n"
            "  Check 1 (Company Validated): confirm the company exists.\n"
            "  Check 2 (Hiring Verified): look for job postings, careers "
            "pages, or hiring mentions.\n"
            "  Check 5 (No Risk Flags): look for negative news, scam "
            "reports, or legal issues.\n"
            "  Check 6 (Industry & Sector): identify SIC/NAICS sector "
            "from company description, business directories, or industry "
            "classification found in web data.\n"
            "  Check 7 (Company Size): find headcount from LinkedIn, "
            "business directories, or company website in web data. Do "
            "NOT use the ERP 'Employees' field.\n"
            "  Check 8 (Annual Revenue): find revenue from financial "
            "databases, news, or industry benchmarks in web data. Do "
            "NOT use the ERP 'Annual Revenue' field. If not explicitly "
            "found, infer from web-sourced company size and sector.\n"
            "  Check 9 (Geographic Location): find HQ and operational "
            "locations from company website, Google Maps, or business "
            "directories in web data. Do NOT use the ERP 'City' or "
            "'Country' fields.\n"
            "  Check 10 (Tech Stack): identify tools, frameworks, or "
            "cloud infrastructure mentioned in web data.\n"
            "  Check 11 (Ownership Type): determine if public, private, "
            "venture-backed, bootstrap, or non-profit from web data."
        )
    else:
        prompt_parts.append("\n=== WEB DATA ===")
        prompt_parts.append("No web data available. For Group B checks "
                            "(6-11), answer No if you cannot verify from "
                            "web sources. Do NOT fall back to ERP Lead "
                            "fields for Company Size, Annual Revenue, or "
                            "Geographic Location — these must come from "
                            "web data. Use ERP fields only for Group A "
                            "checks (Company name, Industry, Contacts).")

    # LVS scoring reminder.
    prompt_parts.append(
        "\n\n=== LVS SCORING REMINDER ===\n"
        "Evaluate all 11 checks, compute LVS score (0-14), then map to "
        "0-100:\n"
        "  14→100, 13→93, 12→86, 11→79, 10→71, 9→64, 8→57, 7→50, "
        "6→43, 5→36, 4→29, 3→21, 2→14, 1→7, 0→0\n"
        "Category: 10-14=Hot, 5-9=Warm, 0-4=Cold\n"
        "Recommendation: 10-14=Contact, 5-9=Nurture, 0-4=Drop\n"
        "Qualified: LVS score >= 9\n"
        "Remarks weight: 10% only (supporting context, not primary).\n\n"
        "Return the JSON object now. Use data_source = \"{0}\".".format(
            data_source)
    )

    user_content = "\n".join(prompt_parts)

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
                    "rating": {
                        "type": "STRING",
                        "enum": ["Hot", "Warm", "Cold"],
                    },
                    "qualified": {"type": "BOOLEAN"},
                    "reasoning": {"type": "STRING"},
                    "summary": {"type": "STRING"},
                    "next_step": {"type": "STRING"},
                    "data_source": {"type": "STRING"},
                },
                "required": ["score", "rating", "qualified",
                             "reasoning", "summary", "next_step",
                             "data_source"],
            },
        },
    }

    url = GEMINI_URL.format(model=GEMINI_MODEL) + "?key={0}".format(api_key)
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(url, headers=headers, json=body,
                             timeout=GEMINI_TIMEOUT)
    except requests.exceptions.RequestException as e:
        _log_error("Web Enrichment: Gemini Scoring Request Failed", str(e))
        return None

    if resp.status_code != 200:
        _log_error("Web Enrichment: Gemini Scoring HTTP Error",
                   "Status: {0}\nResponse: {1}".format(
                       resp.status_code, resp.text[:1000]))
        return None

    try:
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(text)
    except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
        _log_error("Web Enrichment: Gemini Scoring Parse Error",
                   "Error: {0}\nBody: {1}".format(str(e), resp.text[:1000]))
        return None

    # Normalize.
    result = _normalize_result(parsed)
    result["data_source"] = data_source
    return result


# ===========================================================================
# SFP Remarks & TEAMPRO profile helpers
# ===========================================================================


def _get_sfp_remarks(sfp):
    """
    Extract all remarks-related fields from the Sales Follow Up document.
    These contain the sales team's interaction notes — critical buying signals.
    """
    parts = []
    remarks = (sfp.get("remarks") or "").strip()
    if remarks:
        parts.append("Remarks: {0}".format(remarks))

    app_remarks = (sfp.get("appointment_remarks") or "").strip()
    if app_remarks:
        parts.append("Appointment Remarks: {0}".format(app_remarks))

    custom_app_remarks = (sfp.get("custom_app_remarks") or "").strip()
    if custom_app_remarks:
        parts.append("Custom Appointment Remarks: {0}".format(custom_app_remarks))

    return "\n".join(parts) if parts else ""


def _get_teampro_profile():
    """
    Fetch TEAMPRO's company profile from www.groupteampro.com.
    Cached in Frappe cache for 24 hours to avoid repeated scraping.
    """
    # Check cache first.
    cached = frappe.cache().get_value(TEAMPRO_PROFILE_CACHE_KEY)
    if cached:
        return cached

    # Try to scrape the website.
    profile = _scrape_teampro_website()
    if not profile:
        # Fallback to a static summary if scraping fails.
        profile = (
            "TEAMPRO is a HR & IT consulting company offering:\n"
            "HR Services: Recruitment, Background Check, Manpower Staffing, "
            "Payroll (payPRO), Compliance Management, Event Management.\n"
            "IT Services: ERP Implementation, Mobile App Development, "
            "Website & E-Commerce, Web Application, Infrastructure Service, "
            "Knowledge Process Outsourcing.\n"
            "Trading: Food Products and supplies.\n"
            "ISO 27001 & 9001 Certified. Based in Tamil Nadu, India with "
            "operations in Oman, UAE, Saudi Arabia, Kuwait, Qatar, Bahrain, "
            "and Iraq."
        )

    # Cache for 24 hours.
    frappe.cache().set_value(
        TEAMPRO_PROFILE_CACHE_KEY, profile, expires_in_sec=TEAMPRO_PROFILE_CACHE_TTL
    )
    return profile


def _scrape_teampro_website():
    """Scrape www.groupteampro.com homepage and extract company profile text."""
    try:
        resp = requests.get(
            TEAMPRO_URL,
            timeout=SCRAPE_TIMEOUT,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            },
            allow_redirects=True,
        )
    except requests.exceptions.RequestException as e:
        _log_error("Web Enrichment: TEAMPRO Scrape Failed", str(e))
        return None

    if resp.status_code != 200:
        _log_error("Web Enrichment: TEAMPRO Scrape HTTP Error",
                   "Status: {0}".format(resp.status_code))
        return None

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception:
        return None

    # Remove non-content tags.
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "noscript", "iframe", "form"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) < 200:
        return None

    # Limit to 4000 chars — we just need the company overview.
    return text[:4000]


# ===========================================================================
# Data extraction helpers
# ===========================================================================


def _extract_party_data(party_doc, party_from="Lead"):
    """
    Extract relevant fields from a Lead or Customer document.
    Handles field name differences between the two doctypes.
    """
    if party_from == "Customer":
        return {
            "lead_name": party_doc.get("customer_name") or "",
            "company_name": party_doc.get("customer_name") or "",
            "email_id": party_doc.get("email_id") or "",
            "phone": party_doc.get("mobile_no") or "",
            "mobile_no": party_doc.get("mobile_no") or "",
            "website": party_doc.get("website") or "",
            "industry": party_doc.get("industry") or "",
            "no_of_employees": party_doc.get("no_of_employees") or "",
            "annual_revenue": party_doc.get("annual_revenue") or "",
            "territory": party_doc.get("territory") or "",
            "country": party_doc.get("country") or "",
            "city": party_doc.get("city") or "",
            "job_title": "",
            "market_segment": party_doc.get("market_segment") or "",
            "qualification_status": "",
            "status": "",
            "notes": "",
        }

    # Lead
    return {
        "lead_name": party_doc.get("lead_name") or party_doc.get("first_name") or "",
        "company_name": party_doc.get("company_name") or "",
        "email_id": party_doc.get("email_id") or "",
        "phone": party_doc.get("phone") or "",
        "mobile_no": party_doc.get("mobile_no") or "",
        "website": party_doc.get("website") or party_doc.get("web") or "",
        "industry": party_doc.get("industry") or "",
        "no_of_employees": party_doc.get("no_of_employees") or "",
        "annual_revenue": party_doc.get("annual_revenue") or "",
        "territory": party_doc.get("territory") or "",
        "country": party_doc.get("country") or party_doc.get("country__") or "",
        "city": party_doc.get("city") or "",
        "job_title": party_doc.get("job_title") or "",
        "market_segment": party_doc.get("market_segment") or "",
        "qualification_status": party_doc.get("qualification_status") or "",
        "status": party_doc.get("status") or "",
        "notes": party_doc.get("notes") or party_doc.get("description") or "",
    }


# Keep old name as alias for backward compatibility.
_extract_lead_data = _extract_party_data


def _get_contacts_data(party_doc, sfp, party_from="Lead"):
    """
    Extract contact info from Lead Contacts / Customer Contacts
    (child table on the party doc) and SFP Contacts (child table on SFP).
    """
    contacts = []

    # Party doc contacts — field name differs by doctype.
    if party_from == "Customer":
        child_field = "customer_contact"
        source_label = "customer_contacts"
    else:
        child_field = "lead_contacts"
        source_label = "lead_contacts"

    for c in (party_doc.get(child_field) or []):
        contacts.append({
            "person_name": c.get("person_name") or "",
            "mobile": c.get("mobile") or "",
            "email_id": c.get("email_id") or "",
            "service": c.get("service") or "",
            "source": source_label,
        })

    # SFP Contacts.
    for c in (sfp.get("contacts") or []):
        contacts.append({
            "person_name": c.get("person_name") or "",
            "mobile": c.get("mobile") or "",
            "email_id": c.get("email_id") or "",
            "service": c.get("service") or "",
            "source": "sfp_contacts",
        })

    # SFP Custom Contact Details.
    for c in (sfp.get("custom_contact_details") or []):
        contacts.append({
            "person_name": c.get("person_name") or "",
            "mobile": c.get("mobile") or "",
            "email_id": c.get("email_id") or "",
            "service": c.get("service") or "",
            "source": "sfp_custom_contacts",
        })

    # SFP Customer Contacts (for Customer-linked SFPs).
    for c in (sfp.get("customer_contacts") or []):
        contacts.append({
            "person_name": c.get("person_name") or "",
            "mobile": c.get("mobile") or "",
            "email_id": c.get("email_id") or "",
            "service": c.get("service") or "",
            "source": "sfp_customer_contacts",
        })

    # Deduplicate by email+mobile.
    seen = set()
    unique = []
    for c in contacts:
        key = (c["email_id"].lower(), c["mobile"])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique


# ===========================================================================
# Result normalization & write-back
# ===========================================================================


# LVS score (0-14) → 0-100 scale mapping.
LVS_SCORE_MAP = {
    0: 0, 1: 7, 2: 14, 3: 21, 4: 29, 5: 36, 6: 43,
    7: 50, 8: 57, 9: 64, 10: 71, 11: 79, 12: 86, 13: 93, 14: 100,
}


def _extract_lvs_score(reasoning):
    """
    Parse the LVS score (0-14) from the reasoning string.
    Looks for patterns like 'LVS Score: 10/14' or 'LVS Score: 10'.
    """
    if not reasoning:
        return None
    match = re.search(r"LVS\s*Score\s*:\s*(\d+)\s*/\s*14", reasoning, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"LVS\s*Score\s*:\s*(\d+)", reasoning, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def _normalize_result(parsed):
    """
    Clean up the Gemini response into a consistent dict.
    Enforces LVS scoring framework: if the reasoning contains an LVS
    score (0-14), remap the 0-100 score and rating to match the LVS
    framework exactly.
    """
    if not isinstance(parsed, dict):
        parsed = {}

    reasoning = _coerce_str(parsed.get("reasoning"))[:2000]

    # Try to extract the LVS score from the reasoning and enforce
    # the mapping so the AI can't deviate from the framework.
    lvs_score = _extract_lvs_score(reasoning)
    if lvs_score is not None and 0 <= lvs_score <= 14:
        score = LVS_SCORE_MAP[lvs_score]
        if lvs_score >= 10:
            rating = "Hot"
        elif lvs_score >= 5:
            rating = "Warm"
        else:
            rating = "Cold"
        qualified = lvs_score >= 9
    else:
        # Fallback: use the AI's score/rating directly.
        score = _coerce_int(parsed.get("score"), 0, 100)
        rating = parsed.get("rating")
        if rating not in ("Hot", "Warm", "Cold"):
            rating = "Hot" if score >= 70 else ("Warm" if score >= 40 else "Cold")
        qualified = _coerce_bool(parsed.get("qualified"), score >= 60)

    summary = _coerce_str(parsed.get("summary"))[:500]
    next_step = _coerce_str(parsed.get("next_step"))[:500]

    return {
        "score": score,
        "rating": rating,
        "qualified": qualified,
        "reasoning": reasoning,
        "summary": summary,
        "next_step": next_step,
    }


def _coerce_int(value, lo, hi):
    try:
        v = int(value)
    except (TypeError, ValueError):
        v = 0
    return max(lo, min(hi, v))


def _coerce_bool(value, threshold=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "qualified")
    return bool(threshold)


def _coerce_str(value):
    if value is None:
        return ""
    return str(value).strip()


def _write_back_sfp(sfp_name, result):
    """Write the 7 AI fields back to the SFP."""
    frappe.db.set_value("Sales Follow Up", sfp_name, {
        "custom_ai_score": result["score"],
        "custom_ai_rating": result["rating"],
        "custom_ai_qualified": 1 if result["qualified"] else 0,
        "custom_ai_validation_status": "Completed",
        "custom_ai_reasoning": result["reasoning"],
        "custom_ai_summary": result["summary"],
        "custom_ai_next_step": result["next_step"],
    }, update_modified=False)
    frappe.db.commit()


def _set_failed(sfp_name):
    """Mark the SFP validation as failed."""
    frappe.db.set_value("Sales Follow Up", sfp_name,
                        "custom_ai_validation_status", "Failed",
                        update_modified=False)
    frappe.db.commit()


def _log_error(title, message):
    frappe.log_error(
        title="AI Lead Validation: {0}".format(title),
        message=message,
    )
