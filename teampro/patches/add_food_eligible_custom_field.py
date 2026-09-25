# Copyright (c) 2026, TeamPRO
# For license information, please see license.txt

"""Add a custom ``Is Food Eligible`` check field on the Employee DocType.

This flag is used by the Lunch Attendance feature when the
``Is Food Eligible Flag`` eligibility filter is selected in
``Lunch Attendance Settings``.
"""

import frappe


CUSTOM_FIELD = {
    "doctype": "Custom Field",
    "dt": "Employee",
    "fieldname": "custom_is_food_eligible",
    "label": "Is Food Eligible",
    "fieldtype": "Check",
    "default": "0",
    "insert_after": "employment_type",
}


def execute():
    if frappe.db.exists(
        "Custom Field", {"dt": "Employee", "fieldname": "custom_is_food_eligible"}
    ):
        return

    doc = frappe.get_doc(CUSTOM_FIELD)
    doc.insert(ignore_permissions=True)
