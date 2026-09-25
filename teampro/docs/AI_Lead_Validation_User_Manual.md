# AI Lead Validation — User Manual

## Sales Follow Up (SFP) Module | TEAMPRO ERPNext

---

## Table of Contents

1. [What Is AI Lead Validation?](#1-what-is-ai-lead-validation)
2. [Where to Find It](#2-where-to-find-it)
3. [How to Validate a Lead](#3-how-to-validate-a-lead)
4. [Understanding the AI Dashboard](#4-understanding-the-ai-dashboard)
5. [Understanding the 7 AI Fields](#5-understanding-the-7-ai-fields)
6. [LVS Scoring Framework](#6-lvs-scoring-framework)
7. [What Data the AI Uses](#7-what-data-the-ai-uses)
8. [Score Ratings and Qualification](#8-score-ratings-and-qualification)
9. [Reading the AI Reasoning](#9-reading-the-ai-reasoning)
10. [When to Re-validate](#10-when-to-re-validate)
11. [Troubleshooting](#11-troubleshooting)
12. [Frequently Asked Questions](#12-frequently-asked-questions)

---

## 1. What Is AI Lead Validation?

AI Lead Validation is a feature that automatically evaluates and scores your leads and customers using artificial intelligence. When you trigger validation on a Sales Follow Up (SFP) record, the AI:

1. **Searches the web** for the company (visits their website or uses Google Search)
2. **Reads your sales remarks** — notes from your interactions with the lead (10% weight)
3. **Compares against TEAMPRO's services** — checks how well the lead's needs match what TEAMPRO offers
4. **Runs the LVS Scoring Framework** — evaluates 11 validation checks across two groups to produce a structured score
5. **Produces a score (0–100)** with a clear explanation of which checks passed and failed

This helps you **prioritize which leads to contact first** and **know exactly what to pitch**.

---

## 2. Where to Find It

1. Open **ERPNext** and go to the **Sales Follow Up** list.
2. Open any SFP record (or create a new one linked to a Lead or Customer).
3. Scroll to the **AI Validation** tab/section on the form.
4. The **AI → Validate Lead** button appears in the toolbar at the top right.

> **Note:** The button only appears on saved SFP records that have a service selected.

---

## 3. How to Validate a Lead

### Step-by-Step

| Step | Action | What Happens |
|------|--------|--------------|
| 1 | Open a **Sales Follow Up** record | The form loads with existing data |
| 2 | Ensure the **Service** field is filled | The AI scores based on the specific service |
| 3 | Add any **Remarks** from your sales interactions | Remarks provide supporting context (10% weight) |
| 4 | Click **AI → Validate Lead** in the toolbar | A loading overlay appears: "Enriching lead from web & scoring with AI..." |
| 5 | Wait **10–30 seconds** | The AI searches the web, reads the company website, runs the 11 LVS checks, and scores the lead |
| 6 | Review the result dialog | Shows score, rating, LVS checks, data source, summary, next step, and reasoning |
| 7 | Click **OK** on the dialog | The form refreshes and the AI Dashboard renders with a visual score gauge |

### What You'll See After Validation

A popup appears with:

```
AI Lead Validation - Service: TFP (Food Products)

Data Source: Google Search
Score: 57/100 (Warm) - Not Qualified

Polkart Logistics scored 8/14 (Warm category) as a verified mid-market
logistics firm in Chennai with 51-200 employees...

Next Step: Nurture: Follow up with Ms. Nithyashree to share TEAMPRO's
food product catalog and present corporate snack/pantry packages.

Reasoning: [LVS] Company Validated: Yes (1pt) | Hiring Verified: No (0pt) |
Relevant Contact: Yes (1pt) | Industry Fit: No (0pt) | No Risk Flags: Yes (1pt) |
Industry & Sector: No (0pts) | Company Size: Yes (1pt) | Annual Revenue: Yes (2pts) |
Geographic Location: Yes (1pt) | Tech Stack: No (0pt) | Ownership Type: Yes (1pt) |
LVS Score: 8/14 | [Company] Polkart Logistics is a verified tech-enabled logistics...
```

After closing the popup, the **AI Validation Dashboard** renders on the form with a visual gauge.

---

## 4. Understanding the AI Dashboard

The AI Validation Dashboard is a visual panel that appears in the **AI Validation** section of the SFP form. It displays:

### Dashboard Components

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 AI Lead Validation              Service: Food Products  │
│                                              [Completed]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     ┌─────────┐         ┌──────────────┐                   │
│     │         │         │   ⚡ WARM     │                   │
│     │   57    │         │              │                   │
│     │  /100   │         │  ✗ NOT QUAL. │                   │
│     └─────────┘         └──────────────┘                   │
│     Lead Score                                              │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ SUMMARY                                               │ │
│  │ Polkart Logistics scored 8/14 (Warm) as a verified    │ │
│  │ mid-market logistics firm in Chennai with 51-200      │ │
│  │ employees. Staff snack requirement presents a steady  │ │
│  │ corporate food supply opportunity.                    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 🎯 RECOMMENDED NEXT STEP                              │ │
│  │ Nurture: Follow up with Ms. Nithyashree to share      │ │
│  │ TEAMPRO's food product catalog and present corporate  │ │
│  │ snack/pantry packages.                                │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 📊 REASONING & ANALYSIS                               │ │
│  │ • [LVS] Company Validated: Yes (1pt)                  │ │
│  │ • [LVS] Hiring Verified: No (0pt)                     │ │
│  │ • [LVS] Relevant Contact: Yes (1pt)                   │ │
│  │ • [LVS] Industry Fit: No (0pt)                        │ │
│  │ • [LVS] No Risk Flags: Yes (1pt)                      │ │
│  │ • [LVS] Industry & Sector: No (0pts)                  │ │
│  │ • [LVS] Company Size: Yes (1pt)                       │ │
│  │ • [LVS] Annual Revenue: Yes (2pts)                    │ │
│  │ • [LVS] Geographic Location: Yes (1pt)                │ │
│  │ • [LVS] Tech Stack: No (0pt)                          │ │
│  │ • [LVS] Ownership Type: Yes (1pt)                     │ │
│  │ • [LVS] LVS Score: 8/14                               │ │
│  │ • [Company] Polkart Logistics is a verified 3PL...     │ │
│  │ • [Hiring] No active recruitment signals detected...   │ │
│  │ • [Sector] NIC Code 630 — outside core food verticals │ │
│  │ • [Size] 51-200 employees — solid mid-market scale... │ │
│  │ • [Revenue] Est. ₹1-10 Cr — financial stability...    │ │
│  │ • [Location] Guindy, Chennai — matches TEAMPRO region │ │
│  │ • [Remarks] Ms. Nithyashree confirmed snacks (10%)... │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Dashboard Color Guide

| Element | Color | Meaning |
|---------|-------|---------|
| Score gauge | **Green** | Score ≥ 71 (Hot, LVS 10-14) |
| Score gauge | **Orange** | Score 36–70 (Warm, LVS 5-9) |
| Score gauge | **Red** | Score < 36 (Cold, LVS 0-4) |
| Rating badge | **Red** | Hot — prioritize |
| Rating badge | **Orange** | Warm — pursue with strategy |
| Rating badge | **Blue** | Cold — deprioritize |
| Qualified badge | **Green** | Qualified (LVS score ≥ 9) |
| Qualified badge | **Gray** | Not qualified (LVS score < 9) |
| Status badge | **Green** | Completed successfully |
| Status badge | **Gray** | Pending (not yet validated) |
| Status badge | **Red** | Failed (error occurred) |

### If the Dashboard Shows "Not Validated Yet"

If you see:
> 📋 AI validation has not been run yet for this SFP.
> Click **AI → Validate Lead** to generate the assessment.

This means the SFP has not been validated yet. Click the **AI → Validate Lead** button to run the assessment.

---

## 5. Understanding the 7 AI Fields

After validation, 7 fields are populated on the SFP:

| Field | What It Shows | Example |
|-------|---------------|---------|
| **AI Score** | A number from 0 to 100 mapped from the LVS score (0-14) | 57 |
| **AI Rating** | A category: Hot, Warm, or Cold (based on LVS score) | Warm |
| **AI Qualified** | Checkmark if the LVS score is 9 or above | (unchecked) |
| **AI Validation Status** | Whether validation ran: Pending, Completed, or Failed | Completed |
| **AI Reasoning** | LVS checks summary + detailed explanation of each check | [LVS] Company Validated: Yes (1pt) \| ... |
| **AI Summary** | 1–2 sentence plain-English summary including LVS score | Polkart Logistics scored 8/14 (Warm)... |
| **AI Next Step** | Specific recommended action matching LVS recommendation | Nurture: Follow up with Ms. Nithyashree... |

All 7 fields are **read-only** — they are populated by the AI and cannot be manually edited.

---

## 6. LVS Scoring Framework

The AI uses the **Lead Validation Scoring (LVS)** framework to evaluate leads. This is a structured, rule-based scoring system with **11 validation checks** across two groups, ensuring consistent and transparent lead assessment.

### Group A: Business Validation (5 checks, max 6 points)

These checks verify the lead's basic business validity and fit:

| # | Check | Weight | What the AI Evaluates |
|---|-------|--------|-----------------------|
| 1 | **Company Validated** | 1 point | Does the company exist and is it a real, verifiable business? The AI checks the website, web data, or Google Search results for evidence of a legitimate company. |
| 2 | **Hiring Verified** | **2 points** | Is the company actively hiring? The AI looks for job postings, careers pages, or hiring activity signals in web data. **High-weight check.** |
| 3 | **Relevant Contact** | 1 point | Is there a decision-maker or influencer contact available? The AI checks if the contact designation is relevant to the service line (e.g., HR Manager for recruitment, IT Head for IT services, Procurement for food products). |
| 4 | **Industry Fit** | 1 point | Does the company's industry match TEAMPRO's service offerings? (HR/Recruitment for companies hiring, IT for tech needs, Food Products for F&B companies). |
| 5 | **No Risk Flags** | 1 point | Are there any red flags? The AI checks for bankruptcy, scam reports, legal issues, negative reviews, or fraud signals. If any risk flag exists, this check fails. |

### Group B: Firmographic Validation (6 checks, max 8 points)

These checks validate the lead's firmographic profile — sector, size, revenue, location, technology, and ownership.

> **Important:** All Group B checks are sourced from **web data** (company website or Google Search results) — NOT from ERP Lead fields. The AI searches the web for the actual company profile, LinkedIn data, business directories, news articles, and financial databases. ERP fields may be incomplete or outdated, so the AI verifies everything from the web.

| # | Check | Weight | What the AI Evaluates | Data Source |
|---|-------|--------|-----------------------|-------------|
| 6 | **Industry & Sector** | **2 points** | Standard Industrial Classification (SIC) or NAICS code matching TEAMPRO's target verticals. The AI determines the sector code from web data — company description, business directories, industry classification. Does the sector align with TEAMPRO's service lines? **High-weight check.** | Web data (Google Search / website) |
| 7 | **Company Size / Headcount** | 1 point | Employee count from web sources — LinkedIn, business directories (ZoomInfo, Apollo), or company website. Classified as SMB (<50), Mid-Market (50-500), Enterprise (500+). The AI does NOT use the ERP "Employees" field. | Web data (LinkedIn, directories) |
| 8 | **Annual Revenue** | **2 points** | Financial bandwidth from web sources — financial databases, news articles, financial reports, or industry benchmarks. If explicit revenue is not found, the AI infers from web-sourced company size and sector. The AI does NOT use the ERP "Annual Revenue" field. **High-weight check.** | Web data (financial databases, news) |
| 9 | **Geographic Location** | 1 point | Headquarters and operational locations from web sources — company website, Google Maps, business directories. The AI does NOT use the ERP "City" or "Country" fields. Does the company operate in regions where TEAMPRO can deliver services? (India, Oman, UAE, Saudi Arabia, Kuwait, Qatar, Bahrain, Iraq). | Web data (website, Google Maps) |
| 10 | **Tech Stack / Technographics** | 1 point | Tools, frameworks, or cloud infrastructure the company currently uses — identified from web data. Verifies compatibility or competitor usage. (e.g., using SAP → harder to sell ERP; using spreadsheets → ERP opportunity; using Workday → recruitment integration opportunity). | Web data (website, tech profiles) |
| 11 | **Ownership Type** | 1 point | Public, private, venture-backed, bootstrap, or non-profit status — determined from web data. Assesses if the ownership type is favorable for B2B sales (e.g., venture-backed companies have budget and growth mandate; public companies have procurement processes; non-profits may have limited budget). | Web data (company registration, news) |

### LVS Score Calculation

```
LVS Score = GROUP A + GROUP B

GROUP A (max 6):
  (Company Validated = Yes ? 1 : 0)
+ (Hiring Verified    = Yes ? 2 : 0)
+ (Relevant Contact   = Yes ? 1 : 0)
+ (Industry Fit       = Yes ? 1 : 0)
+ (No Risk Flags      = Yes ? 1 : 0)

GROUP B (max 8):
  (Industry & Sector    = Yes ? 2 : 0)
+ (Company Size         = Yes ? 1 : 0)
+ (Annual Revenue       = Yes ? 2 : 0)
+ (Geographic Location  = Yes ? 1 : 0)
+ (Tech Stack           = Yes ? 1 : 0)
+ (Ownership Type       = Yes ? 1 : 0)

Maximum LVS Score = 14
```

### LVS Score → 0-100 Score Mapping

The LVS score (0-14) is mapped to a 0-100 scale for the AI Score field:

| LVS Score | 0-100 Score | Category | Recommendation |
|-----------|-------------|----------|----------------|
| 14 | 100 | Hot | Contact |
| 13 | 93 | Hot | Contact |
| 12 | 86 | Hot | Contact |
| 11 | 79 | Hot | Contact |
| 10 | 71 | Hot | Contact |
| 9 | 64 | Warm | Nurture |
| 8 | 57 | Warm | Nurture |
| 7 | 50 | Warm | Nurture |
| 6 | 43 | Warm | Nurture |
| 5 | 36 | Warm | Nurture |
| 4 | 29 | Cold | Drop |
| 3 | 21 | Cold | Drop |
| 2 | 14 | Cold | Drop |
| 1 | 7 | Cold | Drop |
| 0 | 0 | Cold | Drop |

### High-Weight Checks (2 points each)

Three checks carry double weight because they are the strongest predictors of lead quality:

| Check | Why It's 2 Points |
|-------|-------------------|
| **Hiring Verified** | Companies actively hiring have immediate needs, budget, and growth signals — especially for TEAMPRO's recruitment services. |
| **Industry & Sector** | SIC/NAICS sector alignment determines whether TEAMPRO's services are even relevant to the company's business model. |
| **Annual Revenue** | Financial bandwidth determines whether the company can actually afford TEAMPRO's services — a critical viability factor. |

### Why the LVS Framework?

| Feature | Benefit |
|---------|---------|
| **Structured** | Every lead is evaluated against the same 11 checks — no arbitrary scoring |
| **Transparent** | The reasoning shows exactly which checks passed and failed, and why |
| **Comprehensive** | Covers both business validity (Group A) and firmographic fit (Group B) |
| **Consistent** | The same company will get a similar LVS score regardless of when you validate |
| **Actionable** | The recommendation (Contact / Nurture / Drop) tells you exactly what to do next |
| **Data-driven** | Uses web data, ERP fields, and industry classifications — not just sales notes |

### Example LVS Evaluation

**Polkart Logistics (SFP-35609, Food Products):**

| # | Check | Result | Points | Reason |
|---|-------|--------|--------|--------|
| 1 | Company Validated | Yes | 1 | Verified tech-enabled logistics company incorporated in 2021 |
| 2 | Hiring Verified | No | 0 | No active recruitment or job posting signals detected |
| 3 | Relevant Contact | Yes | 1 | Ms. Nithyashree — handles staff snack requirements |
| 4 | Industry Fit | No | 0 | Primary industry is logistics, not F&B |
| 5 | No Risk Flags | Yes | 1 | No legal issues, scam reports, or financial risk flags |
| 6 | Industry & Sector | No | 0 | NIC Code 630 (Transportation auxiliary) — outside core food verticals |
| 7 | Company Size | Yes | 1 | 51-200 employees — solid mid-market scale for snack orders |
| 8 | Annual Revenue | Yes | 2 | Est. ₹1-10 Cr — financial stability to pay for food products |
| 9 | Geographic Location | Yes | 1 | Guindy, Chennai — directly matches TEAMPRO's regional presence |
| 10 | Tech Stack | No | 0 | No specific procurement or catering management tech identified |
| 11 | Ownership Type | Yes | 1 | Private Limited unlisted corporate structure |
| | **Total** | | **8/14** | **Warm → Nurture** |

---

## 7. What Data the AI Uses

The AI considers **5 types of data** when scoring a lead:

### 7.1 Lead/Customer Information
Data from the ERP system:
- Company name
- Industry
- Number of employees
- Annual revenue
- Territory and country
- Email, phone, website
- Market segment
- Qualification status

These feed **Group A** checks (Company Validated, Industry Fit, Relevant Contact). Group B checks (Company Size, Annual Revenue, Geographic Location, etc.) are sourced from web data — NOT from ERP fields.

### 7.2 SFP Remarks (10% Weight)
Your notes from sales interactions provide **supporting context** at 10% weight. They do NOT override the LVS checks but can help the AI understand nuances:

| Remark | What the AI Detects |
|--------|---------------------|
| "They provide snacks to staff's, she will discuss later" | Supporting signal for Industry Fit and Industry & Sector context |
| "Follow up for Protection Engineer details" | Supporting signal for Hiring Verified context |
| "Not interested currently" | Minor negative signal |
| "Sent quotation, awaiting response" | Minor positive engagement signal |

> **Tip:** Remarks are now a minor factor (10% weight). The primary scoring comes from the 11 LVS checks. However, detailed remarks still help the AI make better judgments on Industry Fit, Relevant Contact, and Industry & Sector checks.

### 7.3 Contact Information
Contacts from both the Lead/Customer record and the SFP:
- Person name
- Mobile number
- Email address
- Service interest

The AI uses contacts for the **Relevant Contact** LVS check — assessing if any contact is a decision-maker or influencer relevant to the service line.

### 7.4 TEAMPRO Company Profile
The AI reads TEAMPRO's own website (www.groupteampro.com) to understand:
- What services TEAMPRO offers (HR, IT, Trading)
- TEAMPRO's certifications (ISO 27001 & 9001)
- TEAMPRO's geographic coverage

This is used for the **Industry Fit** and **Geographic Location** LVS checks — matching the lead's needs and location to what TEAMPRO can actually deliver.

### 7.5 Web Data (Company Website or Google Search)
The AI tries to find out what the company actually does. This is the **primary data source for all Group B checks** (firmographic validation) and several Group A checks:

| Priority | Method | When Used | LVS Checks Fed |
|----------|--------|-----------|----------------|
| 1st | **Company Website** | Visits the lead's website and reads the homepage + about page | All 11 checks (web data is the primary source for Group B) |
| 2nd | **Google Search** | If no website or website can't be accessed, searches Google for the company name | All 11 checks (web data is the primary source for Group B) |
| 3rd | **Contacts Only** | If both fail, scores using only ERP data + remarks + contacts | Group A only — Group B checks will likely fail without web data |

> **Important:** Group B checks (Industry & Sector, Company Size, Annual Revenue, Geographic Location, Tech Stack, Ownership Type) are **always sourced from web data** — never from ERP Lead fields. If no web data is available, these checks will fail, resulting in a lower score. This ensures the AI validates the company's actual current profile, not potentially outdated ERP data.

The **Data Source** field tells you which method was used.

---

## 8. Score Ratings and Qualification

### Rating Scale (Based on LVS Score)

| LVS Score | 0-100 Score | Rating | What It Means | Action |
|-----------|-------------|--------|---------------|--------|
| 10-14 | 71-100 | **Hot** | Strong potential — company is verified, hiring, fits TEAMPRO's services, has revenue and sector alignment | **Contact immediately** |
| 5-9 | 36-64 | **Warm** | Moderate potential — some checks passed but not all (e.g., not hiring, or sector doesn't perfectly align) | **Nurture** with targeted approach |
| 0-4 | 0-29 | **Cold** | Low potential — company may not be verified, has risk flags, doesn't fit industry, or lacks financial bandwidth | **Drop** or deprioritize |

### Qualification

| LVS Score | Qualified? | Meaning |
|-----------|------------|---------|
| ≥ 9 | **Yes** | Lead meets the minimum threshold (at least 9 out of 14 LVS points) |
| < 9 | **No** | Lead does not meet the qualification threshold |

### Service-Specific Scoring

The same company can get **different LVS scores for different services** because the **Industry Fit**, **Industry & Sector**, **Relevant Contact**, and **Tech Stack** checks depend on the service:

| Company | Food Products (TFP) | Recruitment (REC-I) | IT Services (IT-SW) |
|---------|---------------------|---------------------|---------------------|
| Polkart Logistics (provides snacks to staff) | **8/14 (Warm)** | 6/14 (Warm) | 4/14 (Cold) |
| Shaher United (needs Protection Engineer) | 3/14 (Cold) | **11/14 (Hot)** | 7/14 (Warm) |
| Tech Startup (needs ERP) | 2/14 (Cold) | 5/14 (Warm) | **10/14 (Hot)** |

Always check the **Service** field on the SFP to know which service the score applies to.

---

## 9. Reading the AI Reasoning

The reasoning field now starts with the **LVS check summary** (all 11 checks), followed by detailed explanations:

### LVS Check Summary (First Line)

The first line of reasoning always shows all 11 LVS checks and the total score:

```
[LVS] Company Validated: Yes (1pt) | Hiring Verified: No (0pt) |
Relevant Contact: Yes (1pt) | Industry Fit: No (0pt) |
No Risk Flags: Yes (1pt) | Industry & Sector: No (0pts) |
Company Size: Yes (1pt) | Annual Revenue: Yes (2pts) |
Geographic Location: Yes (1pt) | Tech Stack: No (0pt) |
Ownership Type: Yes (1pt) | LVS Score: 8/14
```

### Detailed Explanation Tags

After the LVS summary, each check is explained with a category tag:

| Tag | What It Covers | Example |
|-----|----------------|---------|
| `[LVS]` | The 11 validation checks summary | "[LVS] Company Validated: Yes (1pt) \| Hiring Verified: No (0pt) \| ..." |
| `[Company]` | Details on Company Validated check | "[Company] Polkart Logistics is a verified tech-enabled logistics company..." |
| `[Hiring]` | Details on Hiring Verified check | "[Hiring] No active recruitment or job posting signals detected..." |
| `[Contact]` | Details on Relevant Contact check | "[Contact] Ms. Nithyashree — handles staff snack requirements..." |
| `[Industry]` | Details on Industry Fit check | "[Industry] Primary industry is logistics, not F&B..." |
| `[Risk]` | Details on No Risk Flags check | "[Risk] No legal issues, scam reports, or financial risk flags..." |
| `[Sector]` | Details on Industry & Sector check | "[Sector] NIC Code 630 — outside core food verticals..." |
| `[Size]` | Details on Company Size check | "[Size] 51-200 employees — solid mid-market scale..." |
| `[Revenue]` | Details on Annual Revenue check | "[Revenue] Est. ₹1-10 Cr — financial stability..." |
| `[Location]` | Details on Geographic Location check | "[Location] Guindy, Chennai — matches TEAMPRO region..." |
| `[TechStack]` | Details on Tech Stack check | "[TechStack] No specific procurement tech identified..." |
| `[Ownership]` | Details on Ownership Type check | "[Ownership] Private Limited unlisted corporate structure..." |
| `[Remarks]` | Sales notes context (10% weight) | "[Remarks] Ms. Nithyashree confirmed providing snacks (10%)..." |

### How to Use the Reasoning

- **Before calling the lead:** Read the LVS summary to quickly see which checks passed/failed, then read the details to understand why
- **For prioritization:** Compare LVS scores across leads — a 10/14 is clearly better than a 6/14
- **For coaching:** Review which checks failed — was it missing revenue data? Wrong sector? Not hiring? No tech stack info?
- **In sales meetings:** Use the summary and next step as talking points

---

## 10. When to Re-validate

Re-run AI validation when:

| Situation | Why |
|-----------|-----|
| You added new **remarks** after a customer interaction | Remarks may provide context that helps the AI on Industry Fit, Relevant Contact, or Industry & Sector checks |
| The lead's **company information** was updated | New industry, size, revenue, or website data affects multiple checks |
| The **service** on the SFP changed | Different services produce different LVS scores (Industry Fit, Industry & Sector, Relevant Contact, and Tech Stack all change) |
| You want a **fresh web search** | Company may have started hiring, changed tech stack, or updated their website |
| The previous validation **failed** | Retry after fixing any issues |

### How to Re-validate

Simply click **AI → Validate Lead** again. The AI will re-run the full pipeline and update all 7 fields with the latest data.

---

## 11. Troubleshooting

### The AI Dashboard Is Not Visible

| Possible Cause | Solution |
|----------------|----------|
| The SFP has not been validated yet | Click **AI → Validate Lead** to generate the assessment |
| The AI Validation section is collapsed | Click the **AI Validation** section header to expand it |
| The form hasn't refreshed | Close and reopen the SFP record |
| Browser cache issue | Hard-refresh the page (Ctrl+Shift+R) |

### The Validate Lead Button Is Missing

| Possible Cause | Solution |
|----------------|----------|
| The SFP is new and not saved yet | Save the SFP first, then the button will appear |
| No service is selected on the SFP | Select a service field, save, and reload |
| The SFP has no linked Lead or Customer | Link a Lead or Customer to the SFP |

### Validation Status Shows "Failed"

| Possible Cause | Solution |
|----------------|----------|
| Gemini API key is missing or invalid | Contact your system administrator |
| Network timeout | Wait a moment and try again |
| Company name is too vague for Google Search | Ensure the Lead/Customer has a proper company name |
| Website blocked the scraper | The AI will fall back to Google Search automatically |

> **Note:** When validation fails, the SFP is not blocked. You can still save and use the SFP normally. The error is logged for the IT team to review.

### Score Seems Too Low or Too High

| Check | Action |
|-------|--------|
| Check the LVS summary in reasoning | See which of the 11 checks failed — this tells you exactly what's dragging the score down |
| Is the company name correct? | A wrong company name means the AI can't validate the company, find hiring info, or determine sector |
| Is the service correct? | Industry Fit, Industry & Sector, Relevant Contact, and Tech Stack all depend on the service |
| Is the industry filled in? | Update the industry field on the Lead/Customer — affects Industry Fit and Industry & Sector checks |
| Are contacts up to date? | Add decision-maker contacts with proper designations — affects Relevant Contact check |
| Is the company actually hiring? | If Hiring Verified = No, the company may not be actively recruiting. This is a 2-point check. |
| Is revenue data available? | If Annual Revenue = No, the AI couldn't verify financial bandwidth. This is a 2-point check. Update the Lead's annual revenue field if known. |
| Is the company in TEAMPRO's region? | If Geographic Location = No, the company may be outside TEAMPRO's service area (India, Middle East). |

---

## 12. Frequently Asked Questions

### Q: Does the AI call the customer?
**A:** No. The AI only reads data from your ERP system, searches the web for company information, and produces a score. It never contacts the customer.

### Q: How long does validation take?
**A:** Typically 10–30 seconds. If the company website is slow or Google Search takes longer, it may take up to 45 seconds.

### Q: Does it cost money each time I validate?
**A:** Each validation uses a small amount of Gemini API credits. The cost is approximately 0.5–2 cents per validation depending on whether Google Search is used. The system is designed to minimize costs by caching the TEAMPRO profile and trying free website scraping before paid Google Search.

### Q: Can I edit the AI fields manually?
**A:** No. All 7 AI fields are read-only. They are populated only by the AI validation process. This ensures consistency and prevents manual score manipulation.

### Q: What is the LVS framework?
**A:** LVS stands for Lead Validation Scoring. It's a structured framework that evaluates each lead against 11 checks in two groups:
- **Group A (Business Validation, max 6 pts):** Company Validated, Hiring Verified, Relevant Contact, Industry Fit, No Risk Flags
- **Group B (Firmographic Validation, max 8 pts):** Industry & Sector, Company Size, Annual Revenue, Geographic Location, Tech Stack, Ownership Type

The total LVS score (0-14) determines the lead category (Hot/Warm/Cold) and recommendation (Contact/Nurture/Drop).

### Q: Why are there 11 checks instead of 5?
**A:** The original 5 checks (Group A) verified basic business validity. The 6 additional checks (Group B) add firmographic validation — sector classification, company size, revenue, location, technology, and ownership. Together they provide a much more comprehensive assessment of whether a lead is truly qualified, not just whether the company exists.

### Q: Why are Hiring Verified, Industry & Sector, and Annual Revenue worth 2 points?
**A:** These three factors are the strongest predictors of lead quality:
- **Hiring Verified** — Companies actively hiring have immediate needs, budget, and growth signals.
- **Industry & Sector** — SIC/NAICS sector alignment determines whether TEAMPRO's services are even relevant.
- **Annual Revenue** — Financial bandwidth determines whether the company can actually afford TEAMPRO's services.

### Q: What if the AI can't find revenue or tech stack data?
**A:** The AI will infer from available signals (company size, industry, web data). If it truly can't determine a check, it will answer No and explain why in the reasoning. You can help by filling in the Annual Revenue and Industry fields on the Lead/Customer record.

### Q: What if the AI gives a wrong score?
**A:** Check the LVS summary in the reasoning field to see which checks failed. If a check failed incorrectly (e.g., the company is actually hiring but the AI couldn't find it), you can re-validate after updating the company information. Remarks are a minor factor (10% weight) — the primary scoring comes from the 11 LVS checks based on web data and ERP fields.

### Q: Does it work for both Leads and Customers?
**A:** Yes. The AI validates SFPs linked to either Leads or Customers. For existing customers, it uses the Customer record data instead of Lead data.

### Q: Can I validate multiple SFPs at once?
**A:** Currently, validation is done one SFP at a time via the Validate Lead button. Bulk validation can be added as a future enhancement.

### Q: What if the company doesn't have a website?
**A:** The AI will use Google Search to find information about the company. If Google Search also finds nothing, it will score based on the ERP data, remarks, and contacts only. In this case, several checks (Company Validated, Hiring Verified, Industry & Sector, Tech Stack) may fail, resulting in a lower LVS score.

### Q: Why did the AI search Google instead of visiting the company website?
**A:** The AI first tries to visit the company's website. If the website URL is not available, the website is down, or the website blocks automated access, it falls back to Google Search. The "Data Source" field shows which method was used.

### Q: Are my sales remarks shared with anyone?
**A:** The remarks are sent to Google Gemini's API for analysis. They are not shared with any other third party. The API key is stored securely in the ERP system's configuration. Remarks carry only 10% weight in the scoring — the LVS framework is the primary scoring driver.

### Q: What is the difference between "Hot", "Warm", and "Cold"?
**A:**
- **Hot (LVS 10-14, Score 71-100):** The lead passed most or all LVS checks. The company is verified, hiring, has relevant contacts, fits the industry/sector, has revenue, and has no risk flags. Contact them immediately.
- **Warm (LVS 5-9, Score 36-64):** The lead passed some checks but not all. For example, the company may be verified and have revenue, but is not hiring or the sector doesn't perfectly align. Nurture with a targeted approach.
- **Cold (LVS 0-4, Score 0-29):** The lead failed most checks. The company may not be verifiable, has risk flags, doesn't fit the industry/sector, or lacks financial bandwidth. Drop or deprioritize.

### Q: What does "Qualified" mean?
**A:** A lead is Qualified if its LVS score is 9 or higher (out of 14). This means the lead passed enough validation checks — including at least some of the high-weight checks (Hiring, Sector, Revenue) — to warrant sales pursuit.

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────┐
│                 AI LEAD VALIDATION                        │
│                 Quick Reference                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  WHEN: Click "AI → Validate Lead" on any SFP             │
│  TIME: 10-30 seconds                                     │
│  COST: ~0.5-2 cents per validation                       │
│                                                          │
│  LVS SCORING FRAMEWORK (11 checks, max 14 points):       │
│                                                          │
│  GROUP A: BUSINESS VALIDATION (max 6 pts)                │
│    1. Company Validated   = 1 point                      │
│    2. Hiring Verified     = 2 points ★                   │
│    3. Relevant Contact    = 1 point                      │
│    4. Industry Fit        = 1 point                      │
│    5. No Risk Flags       = 1 point                      │
│                                                          │
│  GROUP B: FIRMGRAPHIC VALIDATION (max 8 pts)             │
│    6. Industry & Sector   = 2 points ★                   │
│    7. Company Size        = 1 point                      │
│    8. Annual Revenue      = 2 points ★                   │
│    9. Geographic Location = 1 point                      │
│   10. Tech Stack          = 1 point                      │
│   11. Ownership Type      = 1 point                      │
│                                                          │
│  ★ = High-weight checks (2 points each)                  │
│                                                          │
│  SCORE GUIDE:                                            │
│    LVS 10-14 = 71-100 = Hot  → Contact immediately       │
│    LVS 5-9   = 36-64  = Warm → Nurture                   │
│    LVS 0-4   = 0-29   = Cold → Drop                      │
│                                                          │
│  QUALIFIED: LVS score ≥ 9 = Yes                          │
│                                                          │
│  REMARKS WEIGHT: 10% (supporting context only)           │
│                                                          │
│  DATA SOURCES (in priority order):                       │
│    1. Company Website (direct scrape)                    │
│    2. Google Search (Gemini grounding)                   │
│    3. Contacts Only (ERP data + remarks)                 │
│                                                          │
│  TIP: The same company gets different LVS scores for     │
│       different services. Check the Service field.       │
│                                                          │
│  TIP: 3 checks are worth 2 points each — Hiring,         │
│       Sector, and Revenue. These are the strongest       │
│       predictors of lead quality.                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

*This manual covers the AI Lead Validation feature in the TEAMPRO ERPNext system. For technical support, contact your system administrator.*
