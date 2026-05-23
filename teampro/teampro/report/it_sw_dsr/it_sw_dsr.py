# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {"label": "Sprint", "fieldname": "custom_sprint", "fieldtype": "Data", "width": 100},
        {"label": "Team", "fieldname": "custom_dev_team", "fieldtype": "Data", "width": 100},
        {"label": "CB", "fieldname": "cb", "fieldtype": "Data", "width": 80},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
        {"label": "Task", "fieldname": "task", "fieldtype": "Link", "options": "Task", "width": 180},
        {"label": "Subject", "fieldname": "subject", "fieldtype": "Data", "width": 200},
        {"label": "KT", "fieldname": "kt_confirmed", "fieldtype": "Check", "width": 60},
        {"label": "ET", "fieldname": "expected_time", "fieldtype": "Float", "precision": 2, "width": 90},
        {"label": "RT", "fieldname": "rt", "fieldtype": "Float", "precision": 2, "width": 80},
        {"label": "AT", "fieldname": "actual_time", "fieldtype": "Float", "precision": 2, "width": 90},
        {"label": "Today RT", "fieldname": "today_rt", "fieldtype": "Float", "precision": 2, "width": 90},
        {"label": "AT Period", "fieldname": "today_at", "fieldtype": "Float", "precision": 2, "width": 90},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 80},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]


def get_data():
    from frappe.utils import getdate, nowdate

    # --- Get date filters (from query report) ---
    date = getdate(frappe.form_dict.get("date")) if frappe.form_dict.get("date") else nowdate()

    data = []

    # --- Get active sprints ordered by team ---
    active_sprints = frappe.get_all(
        'Sprint',
        filters={'status': 'In Progress'},
        fields=['sprint_id', 'team'],
        order_by='team asc'
    )
    sprint_ids = [s.sprint_id for s in active_sprints]

    if not sprint_ids:
        return []

    # --- Get task data within date range ---
    task_data = frappe.db.sql("""
        SELECT name, project, subject, custom_allocated_to, status,
               expected_time, rt, actual_time, priority,
               status as current_status, custom_dev_team, custom_sprint, kt_confirmed
        FROM `tabTask`
        WHERE custom_production_date = %s
          AND custom_sprint IN %s
        ORDER BY custom_sprint, custom_dev_team, custom_allocated_to, priority, project
    """, (date, tuple(sprint_ids)), as_dict=True)

    allocated_task_names = [t.name for t in task_data]
    employee_list = set()

    # --- Main task data ---
    for task in task_data:
        emp = frappe.get_value("Employee", {"user_id": task.custom_allocated_to}, ["short_code", "name"], as_dict=True)
        short_code = emp.short_code if emp else ""
        emp_name = emp.name if emp else ""
        employee_list.add(emp_name)

        # Total actual time
        actual_time = frappe.db.sql("""
            SELECT SUM(d.hours) as hours
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus = 1 AND t.employee = %s AND d.task = %s
        """, (emp_name, task.name), as_dict=True)[0].hours or 0

        # Today's actual time
        today_at = frappe.db.sql("""
            SELECT SUM(d.hours) as hours
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus != 2 AND t.start_date = %s
              AND t.employee = %s AND d.task = %s
        """, (date, emp_name, task.name), as_dict=True)[0].hours or 0

        # Today's RT from Daily Monitor
        today_rt = frappe.db.sql("""
            SELECT SUM(a.today_rt) as hours
            FROM `tabAllocated Tasks` a
            JOIN `tabDaily Monitor` m ON a.parent = m.name
            WHERE m.docstatus != 2 AND m.date = %s
              AND m.dev_team = %s AND a.id = %s AND m.sprint = %s
        """, (date, task.custom_dev_team, task.name, task.custom_sprint), as_dict=True)[0].hours or 0

        data.append({
            "custom_sprint": task.custom_sprint,
            "custom_dev_team": task.custom_dev_team,
            "cb": short_code,
            "project": task.project,
            "task": task.name,
            "subject": task.subject,
            "kt_confirmed": task.kt_confirmed,
            "expected_time": round(task.expected_time or 0, 2),
            "rt": round(task.rt or 0, 2),
            "actual_time": round(actual_time, 2),
            "today_rt": round(today_rt, 2),
            "today_at": round(today_at, 2),
            "priority": task.priority,
            "status": task.current_status,
        })

    # --- Timesheet tasks & issues ---
    for emp_name in employee_list:
        if not emp_name:
            continue
        short_code = frappe.db.get_value("Employee", emp_name, 'short_code') or ""
        dev_team = frappe.db.get_value("Employee", emp_name, 'custom_dev_team') or ""
        not_in_tasks = tuple(allocated_task_names) or ("",)

        # Timesheet tasks not already in list
        timesheet_tasks = frappe.db.sql("""
            SELECT DISTINCT d.task, d.activity_type, d.project, d.subject, d.task_status
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus != 2 AND t.start_date = %s
              AND t.employee = %s AND d.task IS NOT NULL AND d.task NOT IN %s
        """, (date, emp_name, not_in_tasks), as_dict=True)

        for row in timesheet_tasks:
            task_doc = frappe.get_doc("Task", row.task)
            expected_time = task_doc.expected_time or 0
            custom_sprint = task_doc.custom_sprint or ""
            priority = task_doc.priority or ""
            kt_confirmed = task_doc.kt_confirmed or 0

            actual_time = frappe.db.sql("""
                SELECT SUM(d.hours) as hours
                FROM `tabTimesheet Detail` d
                JOIN `tabTimesheet` t ON d.parent = t.name
                WHERE t.docstatus = 1 AND t.employee = %s AND d.task = %s
            """, (emp_name, row.task), as_dict=True)[0].hours or 0

            today_at = frappe.db.sql("""
                SELECT SUM(d.hours) as hours
                FROM `tabTimesheet Detail` d
                JOIN `tabTimesheet` t ON d.parent = t.name
                WHERE t.docstatus != 2 AND t.start_date = %s
                  AND t.employee = %s AND d.task = %s
            """, (date, emp_name, row.task), as_dict=True)[0].hours or 0

            today_rt = frappe.db.sql("""
                SELECT SUM(a.today_rt) as hours
                FROM `tabAllocated Tasks` a
                JOIN `tabDaily Monitor` m ON a.parent = m.name
                WHERE m.docstatus != 2 AND m.date = %s
                  AND m.dev_team = %s AND a.id = %s AND m.sprint = %s
            """, (date, dev_team, row.task, custom_sprint), as_dict=True)[0].hours or 0

            status = "Working"
            if row.activity_type == "Manual Testing":
                status = "Pending Review"
            elif row.activity_type == "Code Review":
                status = "Code Review"
                expected_time = 0

            data.append({
                "custom_sprint": custom_sprint,
                "custom_dev_team": dev_team,
                "cb": short_code,
                "project": row.project,
                "task": row.task,
                "subject": row.subject,
                "kt_confirmed": kt_confirmed,
                "expected_time": round(expected_time, 2),
                "rt": 0,
                "actual_time": round(actual_time, 2),
                "today_rt": round(today_rt, 2),
                "today_at": round(today_at, 2),
                "priority": priority,
                "status": status,
            })

        # Timesheet issues
        timesheet_issues = frappe.db.sql("""
            SELECT DISTINCT d.custom_issue, d.activity_type, d.project, d.custom_subject_issue
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus != 2 AND t.start_date = %s
              AND t.employee = %s AND d.custom_issue IS NOT NULL
        """, (date, emp_name), as_dict=True)

        for row in timesheet_issues:
            priority = frappe.get_value("Issue", row.custom_issue, "priority") or ''
            current_status = frappe.get_value("Issue", row.custom_issue, "status") or ''
            custom_sprint = frappe.get_value("Issue", row.custom_issue, "custom_sprint") or ''

            today_at = frappe.db.sql("""
                SELECT SUM(d.hours) as hours
                FROM `tabTimesheet Detail` d
                JOIN `tabTimesheet` t ON d.parent = t.name
                WHERE t.docstatus != 2 AND t.start_date = %s
                  AND t.employee = %s AND d.custom_issue = %s
            """, (date, emp_name, row.custom_issue), as_dict=True)[0].hours or 0

            data.append({
                "custom_sprint": custom_sprint,
                "custom_dev_team": dev_team,
                "cb": short_code,
                "project": row.project,
                "task": row.custom_issue,
                "subject": row.custom_subject_issue,
                "kt_confirmed": 0,
                "expected_time": 0,
                "rt": 0,
                "actual_time": 0,
                "today_rt": 0,
                "today_at": round(today_at, 2),
                "priority": priority,
                "status": current_status,
            })

    # --- FINAL SORT ---
    data = sorted(data, key=lambda x: (
        x["custom_dev_team"] or "",
        x["cb"] or "",
        {"High": 1, "Medium": 2, "Low": 3}.get(x["priority"], 4)  # sort High > Medium > Low
    ))

    return data
