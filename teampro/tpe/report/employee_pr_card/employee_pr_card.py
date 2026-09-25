# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"label": _("Employee"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 140},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 160},
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 120},
        {"label": _("Designation"), "fieldname": "designation", "fieldtype": "Data", "width": 120},
        {"label": _("Period"), "fieldname": "period_label", "fieldtype": "Data", "width": 90},
        {"label": _("Overall PR"), "fieldname": "overall_pr", "fieldtype": "Float", "width": 90},
        {"label": _("Rank"), "fieldname": "department_rank", "fieldtype": "Int", "width": 60},
        {"label": _("EP"), "fieldname": "energy_points", "fieldtype": "Float", "width": 70},
        {"label": _("NC"), "fieldname": "non_conformities", "fieldtype": "Int", "width": 60},
        {"label": _("Strength"), "fieldname": "strength", "fieldtype": "Data", "width": 140},
        {"label": _("Improvement Area"), "fieldname": "improvement_area", "fieldtype": "Data", "width": 140},
    ]
    filters = filters or {}
    cond = []
    if filters.get("employee"):
        cond.append(["employee", "=", filters["employee"]])
    if filters.get("department"):
        cond.append(["department", "=", filters["department"]])
    if filters.get("period_label"):
        cond.append(["period_label", "=", filters["period_label"]])
    rows = frappe.db.get_all(
        "Performance Rating",
        filters=cond,
        fields=["employee", "employee_name", "department", "designation",
                "period_label", "overall_pr", "department_rank",
                "energy_points", "non_conformities", "strength", "improvement_area"],
        order_by="overall_pr desc",
    )
    return columns, rows
