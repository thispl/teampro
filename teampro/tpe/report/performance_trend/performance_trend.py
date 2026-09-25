# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": _("Period"), "fieldname": "period_label", "fieldtype": "Data", "width": 100},
        {"label": _("Employee"), "fieldname": "employee_name", "fieldtype": "Data", "width": 160},
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Data", "width": 120},
        {"label": _("Overall PR"), "fieldname": "overall_pr", "fieldtype": "Float", "width": 90},
        {"label": _("Rank"), "fieldname": "department_rank", "fieldtype": "Int", "width": 60},
    ]
    cond = []
    if filters.get("employee"):
        cond.append(["employee", "=", filters["employee"]])
    if filters.get("department"):
        cond.append(["department", "=", filters["department"]])
    rows = frappe.db.get_all(
        "Performance Rating",
        filters=cond,
        fields=["period_label", "employee_name", "department", "overall_pr", "department_rank"],
        order_by="employee_name, period_label",
    )
    return columns, rows
