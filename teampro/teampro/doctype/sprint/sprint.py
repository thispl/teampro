# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff, add_days,cint,get_link_to_form
import datetime
from datetime import date
from frappe.utils import getdate, today
today = date.today()
class Sprint(Document):
    def after_insert(self):
        if frappe.db.exists("Sprint", {'team': self.team, 'workflow_state': 'In Progress','name':['!=',self.name]}):
            doc_name = frappe.db.get_value("Sprint", {'team': self.team, 'workflow_state': 'In Progress'}, 'name')
            form_link = get_link_to_form("Sprint", doc_name)
            frappe.throw("Already another sprint present {0}, with status <b>In Progress</b>".format(form_link))

    # def validate(self):
    #     for row in self.sprint_avl_time:
    #        if row.available_hours is not None and row.allocated_hours is not None:
    #             allowed_hours = row.available_hours + (row.available_hours * 0.3)
    #             if row.allocated_hours > allowed_hours:
    #                 frappe.throw(
    #                     f"Row #{row.idx}: Allocated hours ({row.allocated_hours}) exceed 30% of available hours ({allowed_hours:.2f})."
    #                 )
    



@frappe.whitelist()
def get_working_days(from_date, to_date):
    from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
    from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
    holiday_list_name = 'TEAMPRO-2025'
    total_days=(date_diff(to_date,from_date))+ 1
    working_days = 0
    for i in range(total_days):
        current_date = add_days(from_date, i)
        if not is_holiday(holiday_list_name, current_date):
            working_days += 1

    return working_days

@frappe.whitelist()
def update_at_status(name,dev_team):
    sprint=frappe.get_doc("Sprint",{"team":dev_team,"sprint_id":name})
    if sprint:
        if sprint.sprint_task:
            for i in sprint.sprint_task:
                emp=frappe.db.get_value("Task",i.task,"custom_allocated_to")
                emp_name=frappe.db.get_value("Employee",{"user_id":emp},"name")
                total_period=0
                total_hours = 0 
                sum_task=frappe.db.sql("""select sum(cs.hours) as total_hours from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s""",(i.task,emp_name), as_dict=True) 
                sum_total=frappe.db.sql("""select sum(cs.hours) as hours from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s AND start_date BETWEEN %s AND %s""",(i.task,emp_name,sprint.from_date,sprint.to_date), as_dict=True) 
                total_hours += sum_task[0].total_hours if sum_task and sum_task[0].total_hours else 0
                total_period+=sum_total[0].hours if sum_task and sum_total[0].hours else 0
                i.at = total_hours
                i.at_period=total_period
    sprint.save()

@frappe.whitelist()
def update_sprint(name,team):
    previous_sprint=frappe.db.get_value("Sprint",{"team":team},["sprint_id"])
    new_sprint_id=""
    if previous_sprint and previous_sprint.startswith("SPRINT "):
        number_part = int(previous_sprint.replace("SPRINT ", "").strip())
        new_sprint_id = f"SPRINT {number_part + 1}"
        if not frappe.db.exists("Task Sprint", {"sprint": new_sprint_id}):
            ts = frappe.new_doc("Task Sprint")
            ts.sprint = new_sprint_id
            ts.active=1
            ts.insert()
            frappe.db.commit()
    else:
        frappe.msgprint("There is no previous sprint for this team so kindly select the sprint id manually")
    return new_sprint_id


# @frappe.whitelist()
# def update_allocated_task_dsr(dev_team, sprint,from_date,to_date,name):
#     parent_doc = frappe.get_doc("Sprint", name)
#     existing_task_ids = {d.task: d for d in parent_doc.sprint_task}
    
#     issues = []
#     meetings = []
#     tasks = []
#     appended_issues = set()
#     appended_meetings = set()
#     appended_tasks = set()

#     employee_list = frappe.get_all("Employee", {
#         'department': "IT. Development - THIS",
#         'custom_dept_type': 'OPS',
#         "custom_dev_team": dev_team
#     }, ['short_code', 'name'])

#     for emp in employee_list:
#         timesheet = frappe.db.get_value("Timesheet", {'start_date': ('between', [from_date, to_date]), 'employee': emp.name}, ['name'])
#         if timesheet:
#             frappe.log_error(title=timesheet,message="Timesheet")
#             issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_issue': ['!=', '']}, fields=['*'])
#             for issue in issue_logs:
#                 if issue.custom_issue in appended_issues:
#                     continue

#                 short_code = emp.short_code
#                 priority = frappe.db.get_value("Issue", issue.custom_issue, "priority")
#                 status = frappe.db.get_value("Issue", issue.custom_issue, "status")
#                 sum_issue = frappe.db.sql("""
#                     SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
#                     INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
#                     WHERE cs.custom_issue=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
#                 """, (issue.custom_issue, emp.name,from_date,to_date), as_dict=True)[0].total or 0.0

#                 data = {
#                     "task": issue.custom_issue,
#                     "at": sum_issue,
#                     'project': issue.project_name,
#                     'subject': issue.custom_subject_issue,
#                     'cr_status': status,
#                     'cb': short_code,
#                     'priority': priority
#                 }

#                 if issue.custom_issue in existing_task_ids:
#                     # Update existing row
#                     row = existing_task_ids[issue.custom_issue]
#                     for k, v in data.items():
#                         row.set(k, v)
#                 else:
#                     issues.append(data)

#                 appended_issues.add(issue.custom_issue)

#             # === Meetings ===
#             meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_meeting': ['!=', '']}, fields=['*'])
#             for meeting in meeting_logs:
#                 if meeting.custom_meeting in appended_meetings:
#                     continue

#                 status = frappe.db.get_value("Meeting", meeting.custom_meeting, "status")
#                 short_code = emp.short_code
#                 sum_meeting = frappe.db.sql("""
#                     SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
#                     INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
#                     WHERE cs.custom_meeting=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
#                 """, (meeting.custom_meeting, emp.name, from_date,to_date), as_dict=True)[0].total or 0.0

#                 data = {
#                     "task": meeting.custom_meeting,
#                     "at": sum_meeting,
#                     'subject': meeting.custom_subject_meeting,
#                     'cb': short_code,
#                     'cr_status': status
#                 }

#                 if meeting.custom_meeting in existing_task_ids:
#                     row = existing_task_ids[meeting.custom_meeting]
#                     for k, v in data.items():
#                         row.set(k, v)
#                 else:
#                     meetings.append(data)

#                 appended_meetings.add(meeting.custom_meeting)

#             # === Tasks ===
#             task_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'task': ['!=', '']}, fields=['*'])
#             for log in task_logs:
#                 frappe.log_error(title=log.task,message="DSR")
#                 if log.task in appended_tasks:
#                     continue

#                 status = frappe.db.get_value("Task", log.task, "status")
#                 short_code = emp.short_code
#                 sum_task = frappe.db.sql("""
#                     SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
#                     INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
#                     WHERE cs.task=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
#                 """, (log.task, emp.name, from_date,to_date), as_dict=True)[0].total or 0.0

#                 data = {
#                     "task": log.task,
#                     "at": sum_task,
#                     "cb": short_code,
#                     "cr_status": status
#                 }

#                 if log.task in existing_task_ids:
#                     row = existing_task_ids[log.task]
#                     for k, v in data.items():
#                         row.set(k, v)
#                 else:
#                     tasks.append(data)

#                 appended_tasks.add(log.task)

#     # Append new items only
#     for d in issues:
#         parent_doc.append("sprint_task", d)
#     for m in meetings:
#         parent_doc.append("sprint_task", m)
#     for t in tasks:
#         parent_doc.append("sprint_task", t)
    
#     for i in parent_doc.sprint_task:
#         emp_id = frappe.db.get_value("Task", i.task, "custom_allocated_to")
#         task_status=frappe.db.get_value("Task",i.task,"status")
#         emp_name = frappe.db.get_value("Employee", {"user_id": emp_id}, "name") if emp_id else None

#         total_hours = 0
#         total_period = 0

#         if emp_name:
#             sum_task = frappe.db.sql("""
#                 SELECT SUM(cs.hours) AS total_hours 
#                 FROM `tabTimesheet` c  
#                 INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
#                 WHERE cs.task = %s AND c.employee = %s
#             """, (i.task, emp_name), as_dict=True)

#             sum_total = frappe.db.sql("""
#                 SELECT SUM(cs.hours) AS hours 
#                 FROM `tabTimesheet` c  
#                 INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
#                 WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
#             """, (i.task, emp_name, from_date,to_date), as_dict=True)

#             total_hours = sum_task[0].total_hours or 0 if sum_task else 0
#             total_period = sum_total[0].hours or 0 if sum_total else 0

#         i.at = total_hours
#         i.at_period = total_period
#         i.cr_status=task_status
#     parent_doc.save()
#     frappe.db.commit()


@frappe.whitelist()
def update_allocated_task_dsr(dev_team, sprint,from_date,to_date,name):
    parent_doc = frappe.get_doc("Sprint", name)
    existing_task_ids = {d.task: d for d in parent_doc.sprint_task}
    
    issues = []
    meetings = []
    tasks = []
    appended_issues = set()
    appended_meetings = set()
    appended_tasks = set()

    employee_list = frappe.get_all("Employee", {
        'department': "IT. Development - THIS",
        'custom_dept_type': 'OPS',
        "custom_dev_team": dev_team
    }, ['short_code', 'name'])

    for emp in employee_list:
        timesheets = frappe.get_all("Timesheet", 
            filters={
                'start_date': ['between', [from_date, to_date]],
                'employee': emp.name
            }, 
            fields=['name']
        )
        for ts in timesheets:
            # timesheet = frappe.db.get_value("Timesheet", {'start_date': ('between', [from_date, to_date]), 'employee': emp.name}, ['name'])
            timesheet=ts.name
            if timesheet:
                frappe.log_error(title=timesheet,message="Timesheet")
                issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_issue': ['!=', '']}, fields=['*'])
                for issue in issue_logs:
                    if issue.custom_issue in appended_issues:
                        continue

                    short_code = emp.short_code
                    priority = frappe.db.get_value("Issue", issue.custom_issue, "priority")
                    status = frappe.db.get_value("Issue", issue.custom_issue, "status")
                    sum_issue = frappe.db.sql("""
                        SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                        WHERE cs.custom_issue=%s AND c.employee=%s
                    """, (issue.custom_issue, emp.name), as_dict=True)[0].total or 0.0
                    sum_total = frappe.db.sql("""
                        SELECT SUM(cs.hours) as hrs_total FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                        WHERE cs.custom_issue=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
                    """, (issue.custom_issue, emp.name, from_date,to_date), as_dict=True)[0].hrs_total or 0.0
                    
                    data = {
                        "task": issue.custom_issue,
                        "at": sum_issue,
                        "at_period":sum_total,
                        'project': issue.project_name,
                        'subject': issue.custom_subject_issue,
                        'cr_status': status,
                        'cb': short_code,
                        'priority': priority
                    }

                    if issue.custom_issue in existing_task_ids:
                        # Update existing row
                        row = existing_task_ids[issue.custom_issue]
                        for k, v in data.items():
                            row.set(k, v)
                    else:
                        issues.append(data)

                    appended_issues.add(issue.custom_issue)

                # === Meetings ===
                meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_meeting': ['!=', '']}, fields=['*'])
                for meeting in meeting_logs:
                    if meeting.custom_meeting in appended_meetings:
                        continue

                    status = frappe.db.get_value("Meeting", meeting.custom_meeting, "status")
                    short_code = emp.short_code
                    sum_meeting = frappe.db.sql("""
                        SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                        WHERE cs.custom_meeting=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
                    """, (meeting.custom_meeting, emp.name, from_date,to_date), as_dict=True)[0].total or 0.0

                    data = {
                        "task": meeting.custom_meeting,
                        "at": sum_meeting,
                        'subject': meeting.custom_subject_meeting,
                        'cb': short_code,
                        'cr_status': status
                    }

                    if meeting.custom_meeting in existing_task_ids:
                        row = existing_task_ids[meeting.custom_meeting]
                        for k, v in data.items():
                            row.set(k, v)
                    else:
                        meetings.append(data)

                    appended_meetings.add(meeting.custom_meeting)

                # === Tasks ===
                task_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'task': ['!=', '']}, fields=['*'])
                for log in task_logs:
                    frappe.log_error(title=log.task,message="DSR")
                    if log.task in appended_tasks:
                        continue

                    status = frappe.db.get_value("Task", log.task, "status")
                    short_code = emp.short_code
                    project=frappe.db.get_value("Task", log.task, "project")
                    sum_task = frappe.db.sql("""
                        SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                        WHERE cs.task=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
                    """, (log.task, emp.name, from_date,to_date), as_dict=True)[0].total or 0.0

                    data = {
                        "task": log.task,
                        "at": sum_task,
                        "project":project,
                        "cb": short_code,
                        "cr_status": status
                    }

                    if log.task in existing_task_ids:
                        row = existing_task_ids[log.task]
                        for k, v in data.items():
                            row.set(k, v)
                    else:
                        tasks.append(data)

                    appended_tasks.add(log.task)

    # Append new items only
    for d in issues:
        parent_doc.append("sprint_task", d)
    for m in meetings:
        parent_doc.append("sprint_task", m)
    for t in tasks:
        parent_doc.append("sprint_task", t)
    
    for i in parent_doc.sprint_task:
        emp_id = frappe.db.get_value("Task", i.task, "custom_allocated_to")
        task_status=frappe.db.get_value("Task",i.task,"status")
        emp_name = frappe.db.get_value("Employee", {"user_id": emp_id}, "name") if emp_id else None

        total_hours = 0
        total_period = 0

        if emp_name:
           
            sum_task = frappe.db.sql("""
                SELECT SUM(cs.hours) AS total_hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.task = %s AND c.employee = %s
            """, (i.task, emp_name), as_dict=True)

            sum_total = frappe.db.sql("""
                SELECT SUM(cs.hours) AS hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
            """, (i.task, emp_name, from_date,to_date), as_dict=True)

            total_hours = sum_task[0].total_hours or 0 if sum_task else 0

            total_period = sum_total[0].hours or 0 if sum_total else 0
        if not i.task.startswith("ISS"):
            i.at = total_hours
            i.at_period = total_period
            i.cr_status=task_status
    parent_doc.save()
    frappe.db.commit()

@frappe.whitelist()
def update_sprint_hours(doc,method):
    avl_hrs=0
    allocated_hrs=0
    if doc.sprint_avl_time:
        for i in doc.sprint_avl_time:
            avl_hrs+=float(i.available_hours or 0)
            allocated_hrs+=float(i.allocated_hours or 0)
    frappe.db.set_value("Sprint",doc.name,"sprint_hours",avl_hrs)
    frappe.db.set_value("Sprint",doc.name,"allocated_hours",allocated_hrs)
    

# @frappe.whitelist()
# def update_allocated_hrs(doc, method):
#     cb_rt_map = {}
#     for task in doc.sprint_task:
#         if task.cb and task.status in ("Open", "Working"):
#             cb_rt_map.setdefault(task.cb, 0)
#             cb_rt_map[task.cb] += task.rt or 0

#     total_allocated_hours = 0

#     for row in doc.sprint_avl_time:
#         allocated = cb_rt_map.get(row.short_code, 0)
#         row.allocated_hours = allocated
#         total_allocated_hours += allocated
#         row.occupancy = (
#             (row.allocated_hours / row.available_hours) * 100
#             if row.available_hours else 0
#         )

#     doc.allocated_hours = total_allocated_hours

@frappe.whitelist()
def update_allocated_hrs(doc, method):
    cb_rt_map = {}
    cb_at_period_map = {}

    for task in doc.sprint_task:
        if task.cb:
            cb_at_period_map.setdefault(task.cb, 0)
            cb_at_period_map[task.cb] += task.at_period or 0
            if task.status in ("Open", "Working","Code Review"):
                cb_rt_map.setdefault(task.cb, 0)
                cb_rt_map[task.cb] += task.rt or 0

    total_allocated_hours = 0

    for row in doc.sprint_avl_time:
        short_code = row.short_code
        allocated = cb_rt_map.get(short_code, 0)
        row.allocated_hours = allocated
        total_allocated_hours += allocated
        row.at_period = cb_at_period_map.get(short_code, 0)
        row.occupancy = (
            (float(allocated) /float( row.available_hours)) * 100
            if row.available_hours > 0 else 0
        )
    for i in doc.sprint_avl_time:
        if i.short_code:
            emp_name=frappe.db.get_value("Employee",{"short_code":("like", i.short_code),"status":"Active"},["name"])
            sum_bt = frappe.db.sql("""
                SELECT SUM(bt_difference) AS total_hours 
                FROM `tabAttendance` 
                WHERE employee=%s AND attendance_date BETWEEN %s AND %s AND docstatus = 0
            """, (emp_name,doc.from_date,doc.to_date), as_dict=True)
            total_hours = sum_bt[0].total_hours or 0 if sum_bt else 0
            i.bh=total_hours

    doc.allocated_hours = total_allocated_hours


@frappe.whitelist()
def update_task_rt(task, rt):
    if task:
        task_doc = frappe.get_doc("Task", task)
        task_doc.rt = rt
        task_doc.save()
        frappe.db.commit()
        return {"status": "success"}
    
@frappe.whitelist()
def update_task_status(task, status):
    if task:
        task_doc = frappe.get_doc("Task", task)
        task_doc.status = status
        task_doc.save()
        frappe.db.commit()
        return {"status": "success"}
    
@frappe.whitelist()
def update_task_kt_confirmed(task, kt):
    if task:
        task_doc = frappe.get_doc("Task", task)
        task_doc.kt_confirmed = kt
        task_doc.save()
        frappe.db.commit()
        return {"status": "success"}

@frappe.whitelist()
def update_sprint_status(doc,method):
    if doc:
        if doc.sprint_task and doc.status=="In Progress":
            for row in doc.sprint_task:
                if row.task:
                    task_status = frappe.db.get_value("Task", row.task, "status")
                    if task_status:
                        row.status = task_status
        
@frappe.whitelist()
def validate_allocate_hrs(doc,method):
    for row in doc.sprint_avl_time:
        if row.available_hours is not None and row.allocated_hours is not None:
            allowed_hours = row.available_hours + (row.available_hours * 0.3)
            if row.allocated_hours > allowed_hours:
                frappe.throw(
                    f"Row #{row.idx}: Allocated hours ({row.allocated_hours}) exceed 30% of available hours ({allowed_hours:.2f})."
                )



@frappe.whitelist()
def get_sprint(team):
    sprint = frappe.db.get_value("Sprint",{
            "team": team,
            "from_date": ("<=", today),
            "to_date": (">=", today)
        },
        "sprint_id" )
    return sprint


@frappe.whitelist()
def get_retro_summary(name):
    sprint = frappe.get_doc('Sprint', name)
    original_cb_list = [s.short_code for s in sprint.sprint_avl_time]
    if not original_cb_list:
        return []
    cb_list=[]
    tl_cb = []
    non_tl_cb = []
    for cb in original_cb_list:
        # sort tl to come first in list
        has_tl = frappe.db.exists(
            "Employee",
            {"short_code": cb, "custom_is_tl": 1}
        )
        if has_tl:
            tl_cb.append(cb)
        else:
            non_tl_cb.append(cb)

    cb_list = tl_cb + non_tl_cb
    result = []
    # loop cb and create summary for every user
    for cb in cb_list:
        user_id = frappe.db.get_value('Employee', {'short_code': cb}, ['user_id'])
        emp_id = frappe.db.get_value('Employee', {'short_code': cb}, ['name'])
        filters_base = {
            'custom_allocated_to': user_id,
            'custom_sprint': sprint.sprint_id
        }
        completed_statuses = ['Pending Review','Client Review','Completed']
        # Allocated total
        allocated = frappe.db.count('Task', {**filters_base, 'custom_spot_task': 0})
        alloc_rt = sum([d.rt for d in frappe.get_all('Task', filters={'custom_allocated_to': user_id,'custom_sprint': sprint.sprint_id,'custom_spot_task': 0}, fields=['rt']) if d.rt])
        # Spot total
        spot = frappe.db.count('Task', {**filters_base, 'custom_spot_task': 1})
        spot_rt = sum([d.rt for d in frappe.get_all('Task', filters={'custom_allocated_to': user_id,'custom_sprint': sprint.sprint_id,'custom_spot_task': 1}, fields=['rt']) if d.rt])
        # Allocated completed
        a_comp_filter = {**filters_base, 'custom_spot_task': 0, 'status': ['in', completed_statuses]}
        a_comp = frappe.db.count('Task', a_comp_filter)
        a_comp_rt = sum([d.rt for d in frappe.get_all('Task', filters=a_comp_filter, fields=['rt']) if d.rt])
        # Spot completed
        s_comp_filter = {**filters_base, 'custom_spot_task': 1, 'status': ['in', completed_statuses]}
        s_comp = frappe.db.count('Task', s_comp_filter)
        s_comp_rt = sum([d.rt for d in frappe.get_all('Task', filters=s_comp_filter, fields=['rt']) if d.rt])
        # Allocated not completed
        a_not_comp_filter = {**filters_base, 'custom_spot_task': 0, 'status': ['not in', completed_statuses]}
        a_not_comp = frappe.db.count('Task', a_not_comp_filter)
        a_not_comp_rt = sum([d.rt for d in frappe.get_all('Task', filters=a_not_comp_filter, fields=['rt']) if d.rt])
        # Spot not completed
        s_not_comp_filter = {**filters_base, 'custom_spot_task': 1, 'status': ['not in', completed_statuses]}
        s_not_comp = frappe.db.count('Task', s_not_comp_filter)
        s_not_comp_rt = sum([d.rt for d in frappe.get_all('Task', filters=s_not_comp_filter, fields=['rt']) if d.rt])
        # Get biometric of sprint period
        bt_diff_total = frappe.db.sql("""
            SELECT SUM(bt_difference) 
            FROM `tabAttendance` 
            WHERE 
                employee = %s 
                AND attendance_date BETWEEN %s AND %s 
                AND status != 'Cancelled'
        """, (emp_id, sprint.from_date, sprint.to_date))[0][0] or 0
        # Get time sheet of sprint period      
        timesheets=frappe.db.get_all('Timesheet',{'start_date':('between',(sprint.from_date,sprint.to_date)),'employee':emp_id,'status':['!=','Cancelled']},['name'])
        timesheet_tasks=[]
        allocated_not_taken_tasks = []
        spot_not_taken_tasks = []
        seen_ids = set()
        for time in timesheets:
            doc = frappe.get_doc('Timesheet', time.name)
            for d in doc.timesheet_summary:
                allocated_person=frappe.db.get_value('Task',{'name':d.id},['custom_allocated_to'])
                if d.id not in seen_ids and allocated_person==user_id:
                    timesheet_tasks.append(d.id)
                    seen_ids.add(d.id)
        #Allocated not taken count
        allocated_tasks=frappe.db.get_all('Task',filters={'custom_allocated_to': user_id,'custom_sprint': sprint.sprint_id,'custom_spot_task': 0}, fields=['name'])
        for alloc in allocated_tasks:
            if alloc.name not in timesheet_tasks:
                allocated_not_taken_tasks.append(alloc.name)
            
        #Spot not taken count
        spot_tasks=frappe.db.get_all('Task',filters={'custom_allocated_to': user_id,'custom_sprint': sprint.sprint_id,'custom_spot_task': 1}, fields=['name'])
        for spot_t in spot_tasks:
            if spot_t.name not in timesheet_tasks:
                spot_not_taken_tasks.append(spot_t.name)
            
        # for allocated_t in timesheets:
        a_not_taken_rt = sum([d.rt for d in frappe.get_all('Task', filters={'name':['in',allocated_not_taken_tasks]}, fields=['rt']) if d.rt])
        s_not_taken_rt = sum([d.rt for d in frappe.get_all('Task', filters={'name':['in',spot_not_taken_tasks]}, fields=['rt']) if d.rt])
        a_nt=len(allocated_not_taken_tasks)
        s_nt=len(spot_not_taken_tasks)
        allocated_completed=frappe.db.get_all('Task',{'custom_allocated_to':user_id,'custom_sprint':sprint.sprint_id,'custom_spot_task':0,'status':['in',('Pending Review','Client Review','Completed')]},['name'])
        allocated_completed_list=[]
        for a in allocated_completed:
            allocated_completed_list.append(a.name)
        
        alloc_completed_hrs=0
        for ac in allocated_completed_list:
            for time_s in timesheets:
                time_logs = frappe.get_all("Timesheet Detail", filters={'parent': time_s.name, 'task':ac }, fields=['hours','task'])
                for log in time_logs:
                    if log['task']==ac:
                        alloc_completed_hrs+= log['hours']
        spot_completed=frappe.db.get_all('Task',{'custom_allocated_to':user_id,'custom_sprint':sprint.sprint_id,'custom_spot_task':1,'status':['in',('Pending Review','Client Review','Completed')]},['name'])
        spot_completed_list=[]
        for a in spot_completed:
            spot_completed_list.append(a.name)
        
        
        spot_completed_hrs=0
        for sc in spot_completed_list:
            for time_s in timesheets:
                time_logs = frappe.get_all("Timesheet Detail", filters={'parent': time_s.name, 'task':sc }, fields=['hours','task'])
                for log in time_logs:
                    if log['task']==sc:
                        spot_completed_hrs+= log['hours']
        allocated_ncompleted=frappe.db.get_all('Task',{'custom_allocated_to':user_id,'custom_sprint':sprint.sprint_id,'custom_spot_task':0,'status':['not in',('Pending Review','Client Review','Completed')]},['name'])
        allocated_ncompleted_list=[]
        for a in allocated_ncompleted:
            allocated_ncompleted_list.append(a.name)
        alloc_ncompleted_hrs=0
        for ac in allocated_ncompleted_list:
            for time_s in timesheets:
                time_logs = frappe.get_all("Timesheet Detail", filters={'parent': time_s.name, 'task':ac }, fields=['hours','task'])
                for log in time_logs:
                    if log['task']==ac:
                        alloc_ncompleted_hrs+= log['hours']
        spot_ncompleted=frappe.db.get_all('Task',{'custom_allocated_to':user_id,'custom_sprint':sprint.sprint_id,'custom_spot_task':1,'status':['not in',('Pending Review','Client Review','Completed')]},['name'])
        spot_ncompleted_list=[]
        for a in spot_ncompleted:
            spot_ncompleted_list.append(a.name)
        spot_ncompleted_hrs=0
        for sc in spot_ncompleted_list:
            for time_s in timesheets:
                time_logs = frappe.get_all("Timesheet Detail", filters={'parent': time_s.name, 'task':sc }, fields=['hours','task'])
                for log in time_logs:
                    if log['task']==sc:
                        spot_ncompleted_hrs+= log['hours']
        result.append({
            'cb': cb,
            'biometric_hours':bt_diff_total,
            'allocated_count': allocated,
            'spot_count': spot,
            'total_count':allocated+spot,
            'allocated_completed': a_comp,
            'spot_completed': s_comp,
            'total_completed':a_comp+s_comp,
            'allocated_pending': a_not_comp-a_nt,
            'spot_pending': s_not_comp-s_nt,
            'total_pending':(a_not_comp-a_nt)+(s_not_comp-s_nt),
            'allocated_not_taken':a_nt,
            'spot_not_taken':s_nt,
            'total_not_taken':a_nt+s_nt,
            'allocated_hrs':alloc_rt,
            'spot_hrs':spot_rt,
            'total_hrs':alloc_rt+spot_rt,
            'allocated_completed_hrs': a_comp_rt,
            'spot_completed_hrs': s_comp_rt,
            'total_completed_hrs':a_comp_rt+s_comp_rt,
            'allocated_pending_hrs': a_not_comp_rt-a_not_taken_rt,
            'spot_pending_hrs': s_not_comp_rt-s_not_taken_rt,
            'total_pending_hrs':(a_not_comp_rt-a_not_taken_rt)+(s_not_comp_rt-s_not_taken_rt),
            'allocated_nt_hrs':a_not_taken_rt,
            'spot_nt_hrs':s_not_taken_rt,
            'total_nt_hrs':a_not_taken_rt+s_not_taken_rt,
            'ac_ts_hrs':alloc_completed_hrs,
            'sp_ts_hrs':spot_completed_hrs,
            'total_ts_hrs':alloc_completed_hrs+spot_completed_hrs,
            'ac_nc_ts':alloc_ncompleted_hrs,
            'sp_nc_ts':spot_ncompleted_hrs,
            'tot_nc_ts':alloc_ncompleted_hrs+spot_ncompleted_hrs
        })

    return result

