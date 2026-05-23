# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DailyStatusReport(Document):
    pass

from datetime import datetime
from frappe.utils.data import nowdate
import frappe
from frappe.utils import getdate, date_diff

@frappe.whitelist()
def view_proj_details(project):
    today = nowdate()
    date_obj = datetime.strptime(today, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')

    data = ''
    data += f'<p>Dear Sir,<br>Greetings of the day!!!<br>'
    data += f'Please find the Daily Development status as on {formatted_date}.</p>'

    comp = frappe.db.get_all("Task", {"project": project,"completed_on":today}, ["name", "subject", "creation", "status"])
    data += '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '<tr style="background-color: #0f1568 ;text-align:center;color: white;"><th>S.No</th><th>TASK ID</th><th>Subject</th><th>Created On</th><th>Status</th></tr>'
    if not comp:
        data += f'<tr><td>1</td><td>Nil</td><td>Nil</td><td>Nil</td><td>Nil</td></tr>'
    for idx, i in enumerate(comp, start=1):
        data += f'<tr><td>{idx}</td><td>{i.name}</td><td>{i.subject}</td><td>{i.creation.strftime("%d-%m-%Y")}</td><td>{i.status}</td></tr>'
    
    data += '</table>'
    data+=f'<br><p>And please find the TASK details which kept pending for your review and request your convenient time to explain the same to you.<br>'
    data += '<table border="1" width="100%" style="border-collapse: collapse;">'
    data+='<tr style="background-color: #0f1568 ;text-align:center;color: white;"><td colspan=7 >POINTS PENDING FOR</td></tr>'
    data += '<tr style="background-color: #0f1568 ;text-align:center;color: white;"><th>S.No</th><th>TASK ID</th><th>ISSUE ID</th><th>CREATION DATE</th><th>SUBJECT</th><th>Age</th><th>STATUS</th></tr>'
    pending=frappe.db.get_all("Task", {"project": project,"status":("in",["Pending Review","Client Review"])}, ["name","issue", "subject", "creation", "status","custom_new_pr_date"],order_by='status asc')
    if not pending:
        data += f'<tr><td>1</td>' \
            f'<td>Nil</td>' \
            f'<td>Nil</td>' \
            f'<td>Nil</td>' \
            f'<td>Nil</td>' \
            f'<td>Nil</td>' \
            f'<td>Nil</td></tr>'
    for idx, i in enumerate(pending, start=1):
        custom_date = getdate(i.custom_new_pr_date) if i.custom_new_pr_date else None
        age = date_diff(getdate(nowdate()), custom_date) if custom_date else 0
        age_html = f'<span style="color:red;">{age}</span>' if age > 3 else age
        data += f'<tr><td>{idx}</td>' \
            f'<td>{i.name}</td>' \
            f'<td>{i.issue or ""}</td>' \
            f'<td>{i.creation.strftime("%d-%m-%Y")}</td>' \
            f'<td>{i.subject}</td>' \
            f'<td>{age_html}</td>' \
            f'<td>{i.status}</td></tr>'
    data+='</table>'
    holidays = get_holidays()
    today = getdate(nowdate())
    data += f'<br><p>And the following are the pending with us.<br>'
    data += '<table border="1" width="100%" style="border-collapse: collapse;">'
    data+='<tr style="background-color: #0f1568 ;text-align:center;color: white;"><td colspan=8>POINTS PENDING FOR TEAMPRO</td></tr>'
    data += '<tr style="background-color: #0f1568 ;text-align:center;color: white;">' \
            '<th>S.No</th><th>TASK ID</th><th>ISSUE ID</th><th>CREATION DATE</th>' \
            '<th>SUBJECT</th><th>STATUS</th><th>EDC</th><th>Age</th></tr>'
    pending_task = frappe.db.get_all(
        "Task",
        {"project": project, "status": ("in", ["Open", "Working", "Overdue", "Code Review"])},
        ["name", "issue", "subject", "creation", "status"],order_by='status asc'
    )
    if not pending_task:
        data += f'<tr>' \
                f'<td>1</td>' \
                f'<td>Nil</td>' \
                f'<td>Nil</td>' \
                f'<td>Nil</td>' \
                f'<td>Nil</td>' \
                f'<td>Nil</td>' \
                f'<td>Nil</td>' \
                f'<td>Nil</td>' \
                f'</tr>'

    for idx, i in enumerate(pending_task, start=1):
        creation_date = getdate(i.creation)
        edc = get_next_working_day(today, holidays)
        age = calculate_age(creation_date, today, holidays)
        pending_age_html = f'<span style="color:red;">{age}</span>' if age > 3 else age

        data += f'<tr>' \
                f'<td>{idx}</td>' \
                f'<td>{i.name}</td>' \
                f'<td>{i.issue or ""}</td>' \
                f'<td>{creation_date.strftime("%d-%m-%Y")}</td>' \
                f'<td>{i.subject}</td>' \
                f'<td>{i.status}</td>' \
                f'<td>{edc.strftime("%d-%m-%Y")}</td>' \
                f'<td>{pending_age_html}</td>' \
                f'</tr>'

    data += '</table>'
    data+='</table>'

    return data

import frappe
from frappe.utils import getdate, add_days, nowdate, formatdate
def get_holidays():
    """Return a set of holiday dates for the company"""
    holiday_list = frappe.db.get_value("Company", "TEAMPRO HR & IT Services Pvt. Ltd.", "default_holiday_list")
    if not holiday_list:
        return set()

    holidays = frappe.get_all(
        "Holiday",
        filters={"parent": holiday_list},
        fields=["holiday_date"]
    )
    return {getdate(h.holiday_date) for h in holidays}

def get_next_working_day(date, holidays):
    """Get the next working day skipping weekends and company holidays"""
    next_day = add_days(date, 1)
    while next_day.weekday() >= 5 or next_day in holidays: 
        next_day = add_days(next_day, 1)
    return next_day

def calculate_age(start_date, today, holidays):
    """Age = working days difference (excluding weekends & holidays)"""
    age = 0
    temp_date = start_date
    while temp_date < today:
        if temp_date.weekday() < 5:
            age += 1
        temp_date = add_days(temp_date, 1)
    return age


import frappe
from frappe.utils import today


@frappe.whitelist()
def get_data(user):
    production_date = today()

    # ---------------------------------
    # 1️⃣ HTML Header
    # ---------------------------------
    html = """
    <style>
        table { width: 100%; border-collapse: collapse !important; }
        table, th, td { border: 1px solid black !important; }
        thead th {
            background-color: #0F1568; color: #fff;
            text-align: center; font-size: 14px; padding: 8px;
            position: sticky; top: 0; z-index: 2;
        }
        td { padding: 6px; text-align: center; font-size: 13px; }
        .left-align { text-align: left !important; }
        .scrollable-table-container { max-height: 600px; overflow-y: auto; }
    </style>

    <div class="scrollable-table-container">
        <table>
            <thead>
                <tr>
                    <th>Sl No</th>
                    <th>Sprint</th>
                    <th>Team</th>
                    <th>CB</th>
                    <th>Project</th>
                    <th>Task</th>
                    <th>Subject</th>
                    <th>Priority</th>
                    <th>KT</th>
                    <th>ET</th>
                    <th>AT</th>
                    <th>TRT</th>
                    <th>TAT</th>
                    <th>Status</th>
                    <th>Allocated To</th>
                    <th>Remarks</th>
                    <th>API Remarks</th>
                    <th>ET VS AT Remarks</th>
                </tr>
            </thead>
            <tbody>
    """

    emp = frappe.get_value(
        "Employee",
        {"user_id": user},
        ["short_code", "name", "custom_dev_team"],
        as_dict=True,
    ) or frappe._dict(short_code="", name="", custom_dev_team="")

    short_code, emp_name, dev_team = emp.short_code, emp.name, emp.custom_dev_team

    allocated_tasks = frappe.db.sql("""
        SELECT
            name, project, subject, custom_allocated_to, status,
            expected_time, rt, actual_time, priority,
            custom_spot_task, custom_remarks, custom_dev_team,
            custom_sprint, custom_et_vs_at_remark
        FROM `tabTask`
        WHERE custom_allocated_to = %s AND custom_production_date = %s
        ORDER BY project, priority
    """, (user, production_date), as_dict=True)

    allocated_names = tuple([t.name for t in allocated_tasks]) or ("",)

    timesheet_tasks = frappe.db.sql("""
        SELECT DISTINCT d.task AS name, d.project, d.subject, d.task_status AS status
        FROM `tabTimesheet Detail` d
        JOIN `tabTimesheet` t ON d.parent = t.name
        WHERE t.docstatus != 2
          AND t.start_date = %s
          AND t.employee = %s
          AND d.task IS NOT NULL
          AND d.task NOT IN %s
    """, (production_date, emp_name, allocated_names), as_dict=True)

    all_tasks = allocated_tasks + timesheet_tasks

    for i, task in enumerate(all_tasks, start=1):
        task_name = task.name
        expected_time = getattr(task, "expected_time", 0) or 0
        rt = getattr(task, "rt", 0) or 0
        remarks = getattr(task, "custom_remarks", "") or ""
        et_vs_at_remark = getattr(task, "custom_et_vs_at_remark", "") or ""
        priority = getattr(task, "priority", "") or frappe.get_value("Task", task_name, "priority") or ""
        dev_team_val = getattr(task, "custom_dev_team", dev_team)
        sprint_val = getattr(task, "custom_sprint", "")

        # Get timing info
        actual_time = frappe.db.sql("""
            SELECT SUM(d.hours) AS h FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus = 1 AND t.employee = %s AND d.task = %s
        """, (emp_name, task_name), as_dict=True)[0].h or 0

        today_at = frappe.db.sql("""
            SELECT SUM(d.hours) AS h FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
        """, (production_date, emp_name, task_name), as_dict=True)[0].h or 0

        today_rt = frappe.db.sql("""
            SELECT SUM(a.today_rt) AS h FROM `tabAllocated Tasks` a
            JOIN `tabDaily Monitor` m ON a.parent = m.name
            WHERE m.docstatus != 2 AND m.date = %s AND m.dev_team = %s AND a.id = %s AND m.sprint = %s
        """, (production_date, dev_team_val, task_name, sprint_val), as_dict=True)[0].h or 0

        # Spot task
        spot_task = frappe.db.get_value(
            "Sprint Task",
            {"production_date": production_date, "task": task_name, "cb": short_code},
            "spot_task"
        ) or 1
        if getattr(task,'custom_allocated_to') ==user:
            html += f"""
            <tr>
                <td>{i}</td>
                <td>{task.custom_sprint or ''}</td>
                <td>{dev_team_val}</td>
                <td>{short_code}</td>
                <td>{getattr(task, 'project', '') or ''}</td>
                <td>{task_name}</td>
                <td class='left-align'>{getattr(task, 'subject', '') or ''}</td>
                <td>{priority}</td>
                <td>1</td>
                <td>{round(expected_time, 2)}</td>
                <td>{round(actual_time, 2)}</td>
                <td>{round(today_rt, 2)}</td>
                <td>{round(today_at, 2)}</td>
                <td>{getattr(task, 'status', '') or ''}</td>
                <td class='left-align'>{remarks}</td>
                <td></td>
                <td class='left-align'>{et_vs_at_remark}</td>
            </tr>
            """
    html += """
            </tbody>
        </table>
    </div>
    """

    return html
