# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": _("Rank"), "fieldname": "rank", "fieldtype": "Int", "width": 60},
        {"label": _("Employee"), "fieldname": "employee_name", "fieldtype": "Data", "width": 160},
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Data", "width": 120},
        {"label": _("Designation"), "fieldname": "designation", "fieldtype": "Data", "width": 120},
        {"label": _("Overall PR"), "fieldname": "overall_pr", "fieldtype": "Float", "width": 90},
    ]
    cond = []
    if filters.get("department"):
        cond.append(["department", "=", filters["department"]])
    if filters.get("period_label"):
        cond.append(["period_label", "=", filters["period_label"]])
    rows = frappe.db.get_all(
        "Performance Rating",
        filters=cond,
        fields=["department_rank", "employee_name", "department", "designation", "overall_pr"],
        order_by="overall_pr desc",
    )
    direction = (filters.get("direction") or "Top").lower()
    limit = int(filters.get("limit") or 10)
    if direction == "bottom":
        rows = list(reversed(rows))[:limit]
        rows = [{"rank": i + 1, **r} for i, r in enumerate(rows)]
    else:
        rows = rows[:limit]
        rows = [{"rank": i + 1, **r} for i, r in enumerate(rows)]
    return columns, rows
