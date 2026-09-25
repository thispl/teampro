# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": _("Checklist"), "fieldname": "checklist", "fieldtype": "Link", "options": "Accounts Checklist", "width": 140},
        {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": _("Frequency"), "fieldname": "frequency", "fieldtype": "Data", "width": 90},
        {"label": _("Period"), "fieldname": "period_label", "fieldtype": "Data", "width": 110},
        {"label": _("Category"), "fieldname": "category", "fieldtype": "Data", "width": 120},
        {"label": _("Item"), "fieldname": "item_title", "fieldtype": "Data", "width": 240},
        {"label": _("Statutory"), "fieldname": "is_statutory", "fieldtype": "Check", "width": 70},
        {"label": _("Compliance Ref"), "fieldname": "compliance_reference", "fieldtype": "Data", "width": 110},
        {"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 80},
        {"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": _("Assigned To"), "fieldname": "assigned_to", "fieldtype": "Link", "options": "User", "width": 130},
        {"label": _("Completed By"), "fieldname": "completed_by", "fieldtype": "Link", "options": "User", "width": 130},
        {"label": _("Completed On"), "fieldname": "completed_on", "fieldtype": "Datetime", "width": 150},
        {"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Data", "width": 180},
    ]


def get_data(filters):
    filters = filters or {}
    conditions, values = build_conditions(filters)

    rows = frappe.db.sql(
        """
        select
            c.name as checklist, c.period_start as date, c.frequency,
            c.period_label, ci.category, ci.item_title, ci.is_statutory,
            ci.compliance_reference, ci.priority, ci.due_date, ci.status,
            ci.assigned_to, ci.completed_by, ci.completed_on, ci.remarks
        from `tabAccounts Checklist Item` ci
        inner join `tabAccounts Checklist` c on c.name = ci.parent
        where c.docstatus < 2 {cond}
        order by c.period_start desc, ci.idx
        """.format(cond=conditions),
        values,
        as_dict=True,
    )
    return rows


def build_conditions(filters):
    cond = ""
    values = {}
    if filters.get("from_date"):
        cond += " and c.period_start >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        cond += " and c.period_end <= %(to_date)s"
        values["to_date"] = filters["to_date"]
    if filters.get("frequency"):
        cond += " and c.frequency = %(frequency)s"
        values["frequency"] = filters["frequency"]
    if filters.get("category"):
        cond += " and ci.category = %(category)s"
        values["category"] = filters["category"]
    if filters.get("status"):
        cond += " and ci.status = %(status)s"
        values["status"] = filters["status"]
    if filters.get("is_statutory"):
        cond += " and ci.is_statutory = 1"
    if filters.get("assigned_to"):
        cond += " and ci.assigned_to = %(assigned_to)s"
        values["assigned_to"] = filters["assigned_to"]
    return cond, values
