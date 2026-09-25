# Copyright (c) 2026, TeamPRO
# For license information, please see license.txt

"""Add a ``Custom Remarks`` field on Sales Order, Delivery Note and Sales Invoice
(both the parent doctype and their line-item child tables).

The parent ``custom_remarks`` is automatically propagated to every line item by
``teampro.teampro_hooks_method.propagate_parent_remarks_to_items`` (wired on the
``validate`` event of each doctype).

Because the same fieldname ``custom_remarks`` is used on the parent and child
tables of all three doctypes, ERPNext's standard mapper
(``frappe.model.mapper.get_mapped_doc``) automatically carries the value over
when a Delivery Note or Sales Invoice is created from a Sales Order / Delivery
Note - no extra mapping code is required.
"""

import frappe


FIELDNAME = "custom_remarks"
LABEL = "Custom Remarks"
FIELDTYPE = "Small Text"

# (DocType, insert_after)
TARGETS = [
    ("Sales Order", "customer_name"),
    ("Sales Order Item", "description"),
    ("Delivery Note", "customer_name"),
    ("Delivery Note Item", "description"),
    ("Sales Invoice", "customer_name"),
    ("Sales Invoice Item", "description"),
]


def execute():
    for dt, insert_after in TARGETS:
        if frappe.db.exists("Custom Field", {"dt": dt, "fieldname": FIELDNAME}):
            continue

        # Fall back to a safe insert_after if the preferred field is missing.
        if not frappe.db.exists(
            "DocField", {"parent": dt, "fieldname": insert_after}
        ) and not frappe.db.exists(
            "Custom Field", {"dt": dt, "fieldname": insert_after}
        ):
            insert_after = None

        doc = frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": dt,
                "fieldname": FIELDNAME,
                "label": LABEL,
                "fieldtype": FIELDTYPE,
                "insert_after": insert_after,
                "translatable": 0,
                "no_copy": 0,
            }
        )
        doc.insert(ignore_permissions=True)

    frappe.clear_cache()
