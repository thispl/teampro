# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "id", "label": "Task", "fieldtype": "Link","options":"Task", "width": 120},
        {"fieldname": "date", "label": "Date", "fieldtype": "Date","width": 150},
        {"fieldname": "project", "label": "Project", "fieldtype": "Link","options":"Project","width": 150},
        {"fieldname": "project_name", "label": "Project Name", "fieldtype": "Data", "width": 120},
        {"fieldname": "subject", "label": "Subject", "fieldtype": "Data", "width": 200},
        {"fieldname": "allocated_to", "label": "Allocated To", "fieldtype": "Link" ,"options":"User","width": 150},
        {"fieldname": "vac", "label": "VAC", "fieldtype": "Int" ,"width": 120},
        {"fieldname": "rc", "label": "RC", "fieldtype": "Int" ,"width": 120},
        {"fieldname": "actual_count", "label": "Actual Count", "fieldtype": "Int" ,"width": 120},
    ]


def get_data(filters):
    conditions = "WHERE dm.service = 'REC-I'"
    values = {}

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND dm.date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters["from_date"]
        values["to_date"] = filters["to_date"]

    if filters.get("allocated_to"):
        conditions += " AND dmt.allocated_to = %(allocated_to)s"
        values["allocated_to"] = filters["allocated_to"]

    data = frappe.db.sql(f"""
        SELECT 
            dm.name, dm.date, dm.service, 
            dmt.id, dmt.project, dmt.project_name, 
            dmt.subject, dmt.allocated_to, dmt.vac, 
            dmt.rc, dmt.actual_count
        FROM `tabDaily Monitor` dm
        JOIN `tabREC DM` dmt ON dm.name = dmt.parent
        {conditions}
    """, values, as_dict=True)

    return data
