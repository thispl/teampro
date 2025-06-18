import frappe
from datetime import datetime
from frappe import _
from frappe.utils import getdate, get_timespan_date_range,flt,today,nowdate,add_months,fmt_money
import json
from datetime import date, timedelta
import pandas as pd

@frappe.whitelist()
def ptis_live_report():
    projects = frappe.db.get_all(
        "Project",
        filters={"service": "IT-SW", "status": ["not in", ["Completed", "Cancelled", "Hold"]]},
        fields=["name", "project_name", "project_type"]
    )

    data = []
    s_no=1
    for project in projects:
        cr_count = frappe.db.count("Task", {"project": project.name, "status": "Client Review"})
        pr_count = frappe.db.count("Task", {"project": project.name, "status": "Pending Review"})
        hold_count = frappe.db.count("Task", {"project": project.name, "status": "Hold"})
        open_count = frappe.db.count("Task", {"project": project.name, "status": "Open"})
        overdue_count = frappe.db.count("Task", {"project": project.name, "status": "Overdue"})
        working_count = frappe.db.count("Task", {"project": project.name, "status": "Working"})
        total_count = cr_count + pr_count + hold_count + open_count + overdue_count + working_count
        s_no+=1
        data.append({
            "s_no":s_no,
            "project_name": project.project_name,
            "type": project.project_type,
            "client_review": cr_count,
            "pending_review": pr_count,
            "hold": hold_count,
            "open": open_count,
            "overdue": overdue_count,
            "working": working_count,
            "total": total_count
        })

    return data
