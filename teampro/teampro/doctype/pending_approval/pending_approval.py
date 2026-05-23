# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import throw,_
from frappe.utils import date_diff, add_months, today,nowtime,nowdate, format_date, add_days
import datetime
import asyncio
import datetime
import time
from frappe.utils import add_days
from datetime import date, datetime,timedelta
from frappe import throw, _
from frappe.exceptions import ValidationError
from frappe.utils import add_years, getdate,add_days
from dateutil.relativedelta import relativedelta
import math
from datetime import datetime, time
from datetime import datetime, timedelta
import calendar
from datetime import datetime
import json 
from frappe.utils import today

class PendingApproval(Document):
    pass

@frappe.whitelist()
def get_workflow_notifications():
    user = frappe.session.user
    # user ="abdulla.pi@groupteampro.com"
    if frappe.db.exists("Employee", {"user_id": user}):
        employee = frappe.db.get_value("Employee", {"user_id": user},'name')
        emp_ids = frappe.db.get_all("Employee", filters = {"leave_approver": user},pluck="name")
        roles = frappe.get_roles(user)
        notifications = []

        # --- Helper to fetch unseen Activity docs ---
        def unseen_docs(filters):
            activity_list = frappe.get_all(
                "Pending Approval",
                filters=filters,
                fields=["name", "workflow_state", "documnet_type", "count"]
            )
            unseen = []
            for d in activity_list:
                doc = frappe.get_doc("Pending Approval", d.name)
                seen_users = [row.user for row in (doc.seen_by or [])]
                if user not in seen_users:
                    unseen.append(d)
            return unseen

        rules = []
        workflows = frappe.get_all("Workflow", filters={"is_active": 1,"document_type":["in",["Leave Application","Attendance Request"]]}, pluck="document_type")
        if not workflows:
            return []

        for document_type in workflows:
            workflow_doc_names = frappe.get_all(
                "Workflow",
                filters={"is_active": 1, "document_type": document_type},
                pluck="name"
            )

            for workflow_name in workflow_doc_names:
                states = frappe.get_all(
                    "Workflow Document State",
                    filters={"parent": workflow_name,"doc_status":0, 'state': ["not in", ['Cancelled', 'Approved', 'Rejected', 'Draft',"Submitted"]]},
                    pluck="state"
                )

                unique_states = sorted(set(states))
                for workflow_state in unique_states:
                    workflow_roles = frappe.get_all(
                        "Workflow Document State",
                        filters={"parent": workflow_name, "state": workflow_state},
                        pluck="allow_edit"
                    )
                    if any(role in roles for role in workflow_roles):
                        if emp_ids:
                            rules.append({
                                "doctype": document_type,
                                "workflow_state": workflow_state,
                                "message": f"{document_type}s ({workflow_state})",
                                "filters": {
                                    "workflow_state": workflow_state,
                                    "employee":["in",emp_ids]
                                }
                            })
                            


        attendance_date = add_days(today(),-1)
        attendance = frappe.get_all(
            "Attendance",
            filters={
                "employee": employee,
                "docstatus": ["!=", 2],
                "attendance_date": attendance_date,
                "status": ["in", ["Absent", "Half Day"]],
            },
            or_filters=[
                ["Attendance", "in_time", "is", "set"],
                ["Attendance", "out_time", "is", "set"],
            ],
            fields=["status"],
            limit=1
        )

        attendance_status = attendance[0].status if attendance else None

        if attendance_status:
            rules.append({
                "doctype": "Attendance",
                "workflow_state":None,
                "message": f"Miss Punch: {employee}'s attendance has been marked as {attendance_status} for {attendance_date}. If you have any queries, please contact your HOD or regularize your attendance.",
                "filters": {
                    "attendance_date": attendance_date,
                    "employee":employee,
                    "status":attendance_status,
                }
            })
        else:
            last_activity = frappe.get_all(
                "Pending Approval",
                filters={
                    "documnet_type": 'Attendance',
                    "disabled": 0,
                    "expired_on": today(),
                    "user":user
                },
                fields=["name", "count", "filters_json"],
                order_by="creation desc",
                limit_page_length=1
            )
            if last_activity and last_activity[0]:
                frappe.db.set_value("Pending Approval", last_activity[0].name, "disabled", 1)
        for rule in rules:
            create_or_update_activity(
                doctype=rule["doctype"],
                workflow_state=rule["workflow_state"],
                message=rule["message"],
                filters=rule["filters"],
                user=user
            )

            unseen = unseen_docs({
                "documnet_type": rule["doctype"],
                "workflow_state": rule["workflow_state"] or '',
                "disabled": 0,
                "user": user,
                "expired_on": today()
            })
            for doc in unseen:
                notifications.append({
                    "message": rule["message"],
                    "count": doc.count,
                    "doctype": rule["doctype"],
                    "docname": doc.name,
                    "workflow_state": doc.workflow_state,
                    "user": user
                })

        return notifications


@frappe.whitelist()
def create_or_update_activity(doctype, workflow_state, message, filters,user):
    """
    Create or update an Activity record for a workflow group.
    - If the count has changed, disable old and create new one.
    """
    # ✅ Use filters as-is (may include leave_approver=user)
    current_count = len(frappe.get_all(doctype, filters=filters))
    json_str = json.dumps(filters)
    like_pattern = f'{json_str[1:-1]}' 

    last_activity = frappe.get_all(
        "Pending Approval",
        filters={
            "documnet_type": doctype,
            "disabled": 0,
            "expired_on": today(),
            "workflow_state":workflow_state or '',
            "user":user
        },
        fields=["name", "count", "filters_json"],
        order_by="creation desc",
        limit_page_length=1
    )
    
    current_count =len(frappe.db.get_all(doctype, filters=filters))
    
    # ✅ Convert filters to JSON for storage (optional)
    filters_json = frappe.as_json(filters)
    temp = True
    if last_activity:
        last_activity = last_activity[0]
        if last_activity.count == current_count and last_activity.get("filters_json") == filters_json:
            temp = False
        else:
            temp = True
            frappe.db.set_value("Pending Approval", last_activity.name, "disabled", 1)
            frappe.db.commit()

    if current_count > 0 and temp:
        act = frappe.new_doc("Pending Approval")
        act.documnet_type = doctype
        act.message = message
        act.message = message
        act.workflow_state = workflow_state
        act.user=user
        act.count = current_count
        act.disabled = 0
        act.expired_on = today()
        act.filters_json = filters_json  
        act.insert(ignore_permissions=True)
        frappe.db.commit()


@frappe.whitelist()
def mark_notification_seen(docname):
    doc = frappe.get_doc("Pending Approval", docname)

    if not doc.get("seen_by"):
        doc.seen_by = []

    if frappe.session.user not in [row.user for row in doc.seen_by]:
        doc.append("seen_by", {"user": frappe.session.user})
        doc.flags.ignore_version = True
        doc.flags.ignore_validate_update_after_submit = True
        doc.flags.ignore_mandatory = True
        doc.flags.ignore_permissions = True

        doc.db_update()
        frappe.db.commit()

    return "OK"


import frappe
from frappe.utils import today

@frappe.whitelist()
def delete_today_approval_docs():
    docs = frappe.get_all(
        "Pending Approval",
        filters={"expired_on": ["<", today()]},
        fields=["name"]
    )

    count = 0
    for d in docs:
        try:
            frappe.delete_doc("Pending Approval", d.name, force=True)
            count += 1
        except Exception as e:
            frappe.log_error(f"Delete Pending Approval Error: {e}")

    return count




@frappe.whitelist()
def delete_today_approval_docs_new():
    job = frappe.db.exists('Scheduled Job Type', 'delete_today_approval_docs')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'ten.ten.doctype.pending_approval.pending_approval.delete_today_approval_docs',
            "frequency": 'Cron',
            "cron_format": "0 0 * * *"
        })
        sjt.save(ignore_permissions=True)