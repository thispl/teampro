# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Installer for the AI Lead Validation custom fields.

Creates the three custom fields required by `lead_ai_validation.py` on the
Lead DocType, if they don't already exist:

    - custom_ai_score      (Int)
    - custom_ai_qualified  (Check)
    - custom_ai_reasoning  (Small Text)

Run from bench console:

    bench --site <site> execute teampro.lead_validation_install.create_lead_ai_custom_fields

Or call from a migration / post-install hook.
"""

import frappe

# The button snippet injected into the existing Lead-Form Client Script.
# Grouped under an "AI" menu to keep the toolbar tidy alongside the
# existing DNC / Follow Up buttons.
AI_BUTTON_SNIPPET = """
    frm.add_custom_button(__("Re-run AI Validation"), function () {
        frappe.call({
            method: "teampro.lead_ai_validation.revalidate_lead",
            args: { lead_id: frm.doc.name },
            freeze: true,
            freeze_message: __("Re-running AI validation..."),
            callback: function (r) {
                if (r.message) {
                    frm.refresh();
                    var status = r.message.qualified ? __("Qualified") : __("Not Qualified");
                    frappe.msgprint({
                        title: __("AI Validation Complete"),
                        message: "<b>" + __("Score") + ":</b> " + r.message.score
                            + " — " + status
                            + "<br><br>" + (r.message.reasoning || ""),
                        indicator: r.message.qualified ? "green" : "orange"
                    });
                }
            }
        });
    }, __("AI"));
"""

# Anchor: end of the existing "Follow Up" button inside the
# `if (!frm.doc.__islocal)` block. We insert the AI button right after it.
_BUTTON_ANCHOR = '    }, __("Create"));\n}'


def create_lead_ai_custom_fields():
    """Create custom AI fields on the Lead doctype if they don't exist."""

    custom_fields = [
        {
            "fieldname": "custom_ai_score",
            "label": "AI Score",
            "fieldtype": "Int",
            "read_only": 1,
            "insert_after": "qualification_status",
            "description": "AI-generated lead score (0-100).",
        },
        {
            "fieldname": "custom_ai_qualified",
            "label": "AI Qualified",
            "fieldtype": "Check",
            "read_only": 1,
            "default": "0",
            "insert_after": "custom_ai_score",
            "description": "AI qualification flag (true if score >= 60).",
        },
        {
            "fieldname": "custom_ai_reasoning",
            "label": "AI Reasoning",
            "fieldtype": "Small Text",
            "read_only": 1,
            "insert_after": "custom_ai_qualified",
            "description": "AI-generated explanation of the lead assessment.",
        },
        {
            "fieldname": "custom_ai_validation_status",
            "label": "AI Validation Status",
            "fieldtype": "Select",
            "options": "\nPending\nCompleted\nFailed",
            "read_only": 1,
            "default": "Pending",
            "insert_after": "custom_ai_reasoning",
            "description": "Status of the AI validation process.",
        },
    ]

    for cf in custom_fields:
        existing = frappe.db.get_value(
            "Custom Field",
            {"dt": "Lead", "fieldname": cf["fieldname"]},
            "name",
        )
        if existing:
            continue

        doc = frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": "Lead",
                "module": "Teampro",
                **cf,
            }
        )
        doc.insert(ignore_permissions=True)

    frappe.db.commit()
    frappe.clear_cache()


def update_lead_client_script():
    """
    Patch the existing 'Lead-Form' Client Script to add a
    'Re-run AI Validation' button under an 'AI' toolbar group.

    Idempotent: if the button is already present, the script is left
    untouched so re-running this installer never duplicates the button.
    """
    cs_name = frappe.db.get_value("Client Script", {"dt": "Lead"}, "name")
    if not cs_name:
        frappe.log_error(
            title="AI Lead Validation: Lead Client Script not found",
            message=(
                "No Client Script for dt='Lead' exists. Create a Client "
                "Script named 'Lead-Form' first, then re-run "
                "teampro.lead_validation_install.update_lead_client_script."
            ),
        )
        return

    cs = frappe.get_doc("Client Script", cs_name)
    script = cs.script or ""

    if "Re-run AI Validation" in script:
        # Already patched — nothing to do.
        return

    if _BUTTON_ANCHOR not in script:
        frappe.log_error(
            title="AI Lead Validation: Client Script anchor not found",
            message=(
                "Could not find the expected insertion anchor in Client "
                "Script '{0}'. The 'Follow Up' button block may have been "
                "edited. Add the 'Re-run AI Validation' button manually."
            ).format(cs_name),
        )
        return

    new_script = script.replace(
        _BUTTON_ANCHOR,
        '    }, __("Create"));\n' + AI_BUTTON_SNIPPET + '}',
        1,
    )

    cs.script = new_script
    cs.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()


# ---------------------------------------------------------------------------
# UI layout fix — group all AI fields into a collapsible section
# ---------------------------------------------------------------------------

# Desired layout on the Lead form:
#
#   ┌─ AI Validation ────────────────────── (collapsible) ──┐
#   │  AI Score          │  AI Reasoning                    │
#   │  AI Qualified      │  AI Summary                      │
#   │  AI Rating         │  AI Next Step                    │
#   └────────────────────┴──────────────────────────────────┘
#
# Field order chain (insert_after):
#   qualification_status -> custom_ai_section (Section Break)
#   custom_ai_section    -> custom_ai_score
#   custom_ai_score      -> custom_ai_qualified
#   custom_ai_qualified  -> custom_ai_rating
#   custom_ai_rating     -> custom_ai_column_break (Column Break)
#   custom_ai_column_break -> custom_ai_reasoning
#   custom_ai_reasoning  -> custom_ai_summary
#   custom_ai_summary    -> custom_ai_next_step

_AI_SECTION_FIELD = "custom_ai_section"
_AI_COLUMN_BREAK_FIELD = "custom_ai_column_break"

_AI_FIELD_ORDER = [
    # (fieldname, insert_after, extra_props)
    ("custom_ai_score", _AI_SECTION_FIELD, {}),
    ("custom_ai_qualified", "custom_ai_score", {}),
    ("custom_ai_rating", "custom_ai_qualified", {}),
    ("custom_ai_validation_status", "custom_ai_rating", {}),
    ("custom_ai_reasoning", _AI_COLUMN_BREAK_FIELD, {}),
    ("custom_ai_summary", "custom_ai_reasoning", {}),
    ("custom_ai_next_step", "custom_ai_summary", {}),
]


def fix_lead_ai_field_layout():
    """
    Reorganize all AI custom fields on the Lead form into a single
    collapsible 'AI Validation' section with a clean 2-column layout.

    Creates the section break and column break if they don't exist,
    then re-chains every AI field's insert_after so the order is
    deterministic and there are no conflicts.

    Idempotent: safe to re-run.
    """
    # 1. Create section break if missing.
    _ensure_custom_field(
        fieldname=_AI_SECTION_FIELD,
        label="AI Validation",
        fieldtype="Section Break",
        insert_after="qualification_status",
        collapsible=1,
        is_collapsed=1,
    )

    # 2. Create column break if missing.
    _ensure_custom_field(
        fieldname=_AI_COLUMN_BREAK_FIELD,
        label="",
        fieldtype="Column Break",
        insert_after="custom_ai_rating",
    )

    # 3. Re-chain every AI field in the correct order.
    for fieldname, insert_after, extra in _AI_FIELD_ORDER:
        _update_custom_field(fieldname, insert_after=insert_after, **extra)

    frappe.db.commit()
    frappe.clear_cache()


def _ensure_custom_field(fieldname, label, fieldtype, insert_after, **extra):
    """Create a Custom Field on Lead if it doesn't already exist."""
    existing = frappe.db.get_value(
        "Custom Field", {"dt": "Lead", "fieldname": fieldname}, "name"
    )
    if existing:
        return existing

    doc = frappe.get_doc(
        {
            "doctype": "Custom Field",
            "dt": "Lead",
            "module": "Teampro",
            "fieldname": fieldname,
            "label": label,
            "fieldtype": fieldtype,
            "insert_after": insert_after,
            **extra,
        }
    )
    doc.insert(ignore_permissions=True)
    return doc.name


def _update_custom_field(fieldname, **props):
    """Update properties on an existing Custom Field."""
    name = frappe.db.get_value(
        "Custom Field", {"dt": "Lead", "fieldname": fieldname}, "name"
    )
    if not name:
        frappe.log_error(
            title="AI Lead Validation: Custom Field not found",
            message=(
                "Cannot update field '{0}' on Lead — it does not exist. "
                "Run create_lead_ai_custom_fields first."
            ).format(fieldname),
        )
        return

    doc = frappe.get_doc("Custom Field", name)
    changed = False
    for key, value in props.items():
        if doc.get(key) != value:
            doc.set(key, value)
            changed = True
    if changed:
        doc.save(ignore_permissions=True)


# ---------------------------------------------------------------------------
# SFP Client Script — upgrade "Validate Lead" button to web-enriched version
# ---------------------------------------------------------------------------

# The old button called `lead_validation.validate` (rules-based, no web data).
# The new button calls `teampro.lead_web_enrichment.enrich_and_validate_sfp`
# which scrapes the company website or uses Gemini Google Search, then scores
# with Gemini using all available data.

_OLD_SFP_BUTTON = '''                frappe.call({
                    method: "lead_validation.validate",
                    args: {
                        sfp_name: frm.doc.name,
                        write_back: true
                    },
                    freeze: true,
                    freeze_message: __("Validating lead for this service..."),
                    callback: function (r) {
                        if (r.message) {
                            frm.refresh();
                            render_ai_dashboard(frm);
                            var results = r.message.results || [];
                            var summary = r.message.summary || {};
                            var msg = "<b>Lead Validation - Service: " + (frm.doc.service || "") + "</b><br><br>"
                                + "Score: <b>" + (summary.average_score || 0) + "/100</b> | "
                                + "Hot: " + (summary.hot || 0) + " | "
                                + "Warm: " + (summary.warm || 0) + " | "
                                + "Cold: " + (summary.cold || 0) + "<br>"
                                + "Qualified: " + (summary.qualified || 0) + "/" + (summary.total || 0) + "<br><br>";
                            results.forEach(function(res) {
                                var color = res.rating === "Hot" ? "red" : (res.rating === "Warm" ? "orange" : "blue");
                                msg += "<b>Score: " + res.score + "/100</b> "
                                    + "<span style='color:" + color + ";font-weight:bold'>(" + res.rating + ")</span>"
                                    + (res.qualified ? " - <span style='color:green;font-weight:bold'>Qualified</span>" : "") + "<br>"
                                    + "<small>" + (res.summary || "") + "</small><br>"
                                    + "<small><b>Next:</b> " + (res.next_step || "") + "</small><br>"
                                    + "<small><b>Reasoning:</b> " + (res.reasoning || "") + "</small><br>";
                            });
                            frappe.msgprint({
                                title: __("Lead Validation Complete"),
                                message: msg,
                                indicator: summary.hot > 0 ? "green" : "orange"
                            });
                        }
                    }
                });'''

_NEW_SFP_BUTTON = '''                frappe.call({
                    method: "teampro.lead_web_enrichment.enrich_and_validate_sfp",
                    args: {
                        sfp_name: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: __("Enriching lead from web & scoring with AI..."),
                    callback: function (r) {
                        if (r.message && !r.message.error) {
                            frm.refresh();
                            render_ai_dashboard(frm);
                            var res = r.message;
                            var color = res.rating === "Hot" ? "red" : (res.rating === "Warm" ? "orange" : "blue");
                            var sourceLabel = {
                                "website": "Company Website",
                                "google_search": "Google Search",
                                "contacts_only": "Contacts Only"
                            }[res.data_source] || res.data_source;
                            var msg = "<b>AI Lead Validation - Service: " + (frm.doc.service || "") + "</b><br><br>"
                                + "Data Source: <b>" + sourceLabel + "</b><br>"
                                + "Score: <b>" + res.score + "/100</b> "
                                + "<span style='color:" + color + ";font-weight:bold'>(" + res.rating + ")</span>"
                                + (res.qualified ? " - <span style='color:green;font-weight:bold'>Qualified</span>" : "") + "<br><br>"
                                + "<small>" + (res.summary || "") + "</small><br><br>"
                                + "<small><b>Next Step:</b> " + (res.next_step || "") + "</small><br><br>"
                                + "<small><b>Reasoning:</b> " + (res.reasoning || "") + "</small>";
                            frappe.msgprint({
                                title: __("AI Validation Complete"),
                                message: msg,
                                indicator: res.qualified ? "green" : "orange"
                            });
                        } else if (r.message && r.message.error) {
                            frappe.msgprint({
                                title: __("AI Validation Failed"),
                                message: r.message.error,
                                indicator: "red"
                            });
                        }
                    }
                });'''


def upgrade_sfp_validate_button():
    """
    Replace the old `lead_validation.validate` call in the Sales Follow Up
    Client Script with the new web-enriched `enrich_and_validate_sfp` call.

    Idempotent: if already upgraded, does nothing.
    """
    cs_name = frappe.db.get_value("Client Script", {"dt": "Sales Follow Up"}, "name")
    if not cs_name:
        frappe.log_error(
            title="AI Lead Validation: SFP Client Script not found",
            message="No Client Script for dt='Sales Follow Up' exists.",
        )
        return

    cs = frappe.get_doc("Client Script", cs_name)
    script = cs.script or ""

    # Already upgraded?
    if "enrich_and_validate_sfp" in script:
        return

    if _OLD_SFP_BUTTON not in script:
        frappe.log_error(
            title="AI Lead Validation: SFP button anchor not found",
            message=(
                "Could not find the old `lead_validation.validate` block in "
                "Client Script '{0}'. The button may have been edited. "
                "Upgrade manually to call "
                "teampro.lead_web_enrichment.enrich_and_validate_sfp."
            ).format(cs_name),
        )
        return

    new_script = script.replace(_OLD_SFP_BUTTON, _NEW_SFP_BUTTON, 1)
    cs.script = new_script
    cs.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
