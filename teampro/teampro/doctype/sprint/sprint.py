# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, date_diff, add_days,cint,get_link_to_form
import datetime
from datetime import date
from frappe.utils import flt
from frappe.utils import getdate, today
today = date.today()
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days
class Sprint(Document):
    # def on_submit(self):
    #     for s in self.sprint_task:
    #         if s.cr_status=='Pending Review':
    #             frappe.throw('Not allowed to submit.Some rows are still in <b>Pending Review</b> status')
    def validate(self):
        
        
        # if not row.created_on and row.task:
        #     task_doc = frappe.get_doc("Task", row.task)
        #     row.created_on = task_doc.creation
        if not self.is_new():
            if float(self.sprint_hours) > 0 and float(self.allocated_hours) >0:
                occupancy=float(self.allocated_hours) / float(self.sprint_hours) *100
                self.occupancy=occupancy
            else:
                self.occupancy=0
            for i in self.sprint_task:
                if i.et and flt(i.et)>0:
                    at=round(i.at,2) if i.at else 0
                    per=(at/i.et)*100
                    i.atet=round(per,2)
                    
                if i.rt and flt(i.rt)>0:
                    at=round(i.at_period,2) if i.at_period else 0
                    per = (at / flt(i.rt)) * 100
                    i.rtet_ = round(per, 2)
            
                if frappe.db.exists('Task',{'name':i.task}):
                    # if i.subject=='':
                    sub=frappe.db.get_value('Task',{'name':i.task},['subject'])
                    i.subject=sub
                    if i.kt_confirmed==0:
                        kt_conf=frappe.db.get_value('Task',{'name':i.task},['kt_confirmed'])
                        i.kt_confirmed=kt_conf
                    status=frappe.db.get_value('Task',{'name':i.task},['status'])
                    alloc=frappe.db.get_value('Task',{'name':i.task},['custom_allocated_to'])
                    rev=frappe.db.get_value('Task',{'name':i.task},['revisions'])
                    etvsat=frappe.db.get_value('Task',{'name':i.task},["custom_et_vs_at_remark"])
                    i.et_vs_at_remarks = etvsat
                elif frappe.db.exists('Issue',{'name':i.task}):
                    # frappe.errprint('sub')
                    status=frappe.db.get_value('Issue',{'name':i.task},['custom_issue_status'])
                    alloc=frappe.db.get_value('Issue',{'name':i.task},['assigned_to'])
                    sub=frappe.db.get_value('Issue',{'name':i.task},['subject'])
                    i.subject=sub
                    if i.rt==0:
                        i.rt=0.5
                    if not i.project:
                        i.project=frappe.db.get_value('Issue',{'name':i.task},['project'])
                    if not i.status:
                        i.status='Open'
                    rev=0
                else:
                    status='Completed'
                    alloc=None
                    rev=0
                # i.cr_status=status
                i.allocated_to=alloc
                if i.cb:
                    cb_user=frappe.db.get_value('Employee',{'short_code':i.cb},['user_id']) 
                    if cb_user==alloc:
                        i.revisions=int(rev)
                    else:
                        i.revisions=0
            seen = set()
            unique_rows = []

            for row in self.sprint_task:
                key = (row.task, row.cb)
                if key not in seen:
                    seen.add(key)
                    unique_rows.append(row)
            self.sprint_task = []
            for row in unique_rows:
                self.append('sprint_task', row)
        for i in self.sprint_task:
            
            if i.cb and i.allocated_to:
                short_code=frappe.db.get_value('Employee',{'user_id':i.allocated_to},'short_code')
                if i.cb!=short_code and (i.at_period==None or i.at_period==0):
                    self.remove(i)
        for row in self.sprint_task:
            if not row.kt_confirmed:
                frappe.throw(
                    f"KT Confirmed is not enabled for Task: {row.task}"
                )     

    def on_update(self):
        if self.workflow_state == "In Progress" and self.get_doc_before_save().workflow_state != "In Progress":
            update_tasks_sprint(self.name)
            empty_sprint(self.name)
        
    
    

    def after_insert(self):
        count= frappe.db.count("Sprint", {'team': self.team, 'workflow_state': 'In Progress','name':['!=',self.name]})
        if count > 1:
            frappe.throw("More than one sprint present in status <b>In Progress</b>")
        else:
            if frappe.db.exists("Sprint", {'team': self.team, 'workflow_state': 'In Progress','name':['!=',self.name]}):
                doc_name = frappe.db.get_value("Sprint", {'team': self.team, 'workflow_state': 'In Progress'}, 'name')
                form_link = get_link_to_form("Sprint", doc_name)
                frappe.msgprint("Already another sprint present {0}, with status <b>In Progress</b>.".format(form_link))
        
        if self.from_date and self.to_date:

            working_days = get_working_days(self.from_date, self.to_date)

            if working_days:
                for row in self.sprint_avl_time:
                    if row.tl == 1:
                        row.available_hours = working_days * 6
                    else:
                        row.available_hours = working_days * 8

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
                sum_total=frappe.db.sql("""select sum(cs.hours) as hours from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s AND start_date BETWEEN %s AND %s""",(i.task,emp_name,sprint.from_date,end_date), as_dict=True) 
                total_hours += sum_task[0].total_hours if sum_task and sum_task[0].total_hours else 0
                total_period+=sum_total[0].hours if sum_task and sum_total[0].hours else 0
                i.at = round(total_hours,2)
                i.at_period=round(total_period,2)
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
                        "at": round(sum_issue,2),
                        "at_period":round(sum_total,2),
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
                        "at": round(sum_meeting,2),
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
                        "at": round(sum_task,2),
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
            i.at = round(total_hours,2)
            i.at_period = round(total_period,2)
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
    frappe.db.set_value("Sprint",doc.name,{
        "sprint_hours": avl_hrs,
        "allocated_hours": allocated_hrs,
    })
    
@frappe.whitelist()
def update_allocated_hrs(doc, method):
    cb_rt_map = {}
    cb_at_period_map = {}

    for task in doc.sprint_task:
        if task.cb:
            cb_at_period_map.setdefault(task.cb, 0)
            cb_at_period_map[task.cb] += task.at_period or 0
            if task.status != 'Cancelled':
                cb_rt_map.setdefault(task.cb, 0)
                cb_rt_map[task.cb] += flt(task.rt) or 0

    total_allocated_hours = 0

    for row in doc.sprint_avl_time:
        short_code = row.short_code
        allocated = cb_rt_map.get(short_code, 0)
        row.allocated_hours = allocated
        total_allocated_hours += allocated
        row.at_period = cb_at_period_map.get(short_code, 0)
        row.occupancy = (
            (float(allocated) / float(row.available_hours)) * 100
            if float(row.available_hours) > 0 else 0
        )

    # Batch: get all employees for this dev team in a single query,
    # then match short_codes in Python (preserves original LIKE behavior)
    short_codes = [i.short_code for i in doc.sprint_avl_time if i.short_code]
    emp_name_by_short_code = {}
    if short_codes:
        employees = frappe.db.get_all(
            "Employee",
            filters={
                "custom_dev_team": doc.team,
                "status": "Active",
                "department": "IT. Development - THIS",
            },
            fields=["name", "short_code"],
        )
        for sc in short_codes:
            for emp in employees:
                if emp.short_code and sc in emp.short_code:
                    emp_name_by_short_code[sc] = emp.name
                    break

    # Batch: get attendance sums for all matched employees in a single query
    emp_names = list(emp_name_by_short_code.values())
    bt_by_emp = {}
    if emp_names and doc.from_date and doc.to_date:
        attendance_rows = frappe.db.sql(
            """SELECT employee, SUM(bt_difference) AS total_hours
               FROM `tabAttendance`
               WHERE employee IN %s
                 AND attendance_date BETWEEN %s AND %s
                 AND docstatus != 2
               GROUP BY employee""",
            (tuple(emp_names), doc.from_date, doc.to_date),
            as_dict=True,
        )
        for ar in attendance_rows:
            bt_by_emp[ar.employee] = ar.total_hours or 0

    for i in doc.sprint_avl_time:
        if i.short_code:
            emp_name = emp_name_by_short_code.get(i.short_code)
            if emp_name:
                i.bh = bt_by_emp.get(emp_name, 0)

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
    if doc and doc.sprint_task and doc.status == "In Progress":
        task_names = [row.task for row in doc.sprint_task if row.task]
        if not task_names:
            return
        # Batch: get all task statuses in a single query
        task_statuses = frappe.db.get_all(
            "Task",
            filters={"name": ["in", task_names]},
            fields=["name", "status"],
        )
        status_map = {t.name: t.status for t in task_statuses}
        for row in doc.sprint_task:
            if row.task and status_map.get(row.task):
                row.cr_status = status_map[row.task]
        
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
    today = nowdate() 
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
            'parent': name,
            'cb': cb
        }
        completed_statuses = ['Pending Review','Client Review','Completed']
        # Allocated total
        allocated = frappe.db.count('Sprint Task', {**filters_base, 'spot_task': 0})
        alloc_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 0
        """, (name, cb))[0][0] or 0 

        # Spot total
        spot = frappe.db.count('Sprint Task', {**filters_base, 'spot_task': 1})
        spot_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 1
        """, (name, cb))[0][0] or 0 
        # Allocated completed
        a_comp = frappe.db.count('Sprint Task', {**filters_base, 'spot_task': 0,'status': ['in', completed_statuses]})
        a_comp_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 0 AND status in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 
        
        # Spot completed
        s_comp = frappe.db.count('Sprint Task', {**filters_base, 'spot_task': 1,'status': ['in', completed_statuses]})
        s_comp_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 1 AND status in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 

        # Allocated not completed
        a_not_comp = frappe.db.count('Sprint Task', {**filters_base, 'spot_task': 0,'status': ['not in', completed_statuses]})
        a_not_comp_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 0 AND status not in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 
        # Spot not completed
        s_not_comp = frappe.db.count('Sprint Task', {**filters_base, 'spot_task': 1,'status': ['not in', completed_statuses]})
        s_not_comp_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 1 AND status not in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 
        bt_diff_total = frappe.db.sql("""
            SELECT SUM(bt_difference) 
            FROM `tabAttendance` 
            WHERE 
                employee = %s 
                AND attendance_date BETWEEN %s AND %s 
                AND status != 'Cancelled'
        """, (emp_id, sprint.from_date, sprint.to_date))[0][0] or 0
        
        # Get time sheet of sprint period
        timesheets = frappe.db.get_all(
            'Sprint Task',
            {'parent': name, 'cb': cb},
            ['at_period', 'task']
        )
        timesheet_tasks = []
        allocated_not_taken_tasks = []
        spot_not_taken_tasks = []
        seen_tasks = set()
        for time in timesheets:
            if time.at_period > 0:
                if time.task and time.task not in seen_tasks:
                    timesheet_tasks.append(time.task)
                    seen_tasks.add(time.task)

        # Allocated but not taken tasks 
        not_taken_allocated = frappe.db.get_all(
            'Sprint Task',{
                'parent': name,
                'cb': cb,
                'spot_task': 0,
                'at_period': 0
            },['task']
        )
        for row in not_taken_allocated:
            if row.task:
                allocated_not_taken_tasks.append(row.task)
            
        #Spot not taken count
        not_taken_spot = frappe.db.get_all(
            'Sprint Task',{
                'parent': name,
                'cb': cb,
                'spot_task': 1,
                'at_period': 0
            },['task']
        )
        for row in not_taken_spot:
            if row.task:
                spot_not_taken_tasks.append(row.task)
        a_not_taken_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 0 AND at_period = 0
        """, (name, cb ))[0][0] or 0 
        s_not_taken_rt = frappe.db.sql("""
            SELECT SUM(rt) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 1 AND at_period = 0
        """, (name, cb ))[0][0] or 0 
        a_nt=len(allocated_not_taken_tasks)
        s_nt=len(spot_not_taken_tasks)
        alloc_completed_hrs=frappe.db.sql("""
            SELECT SUM(at_period) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 0 AND  status in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 
        spot_completed_hrs=frappe.db.sql("""
            SELECT SUM(at_period) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 1 AND  status in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 
        alloc_ncompleted_hrs=frappe.db.sql("""
            SELECT SUM(at_period) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 0 AND  status not in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 
        spot_ncompleted_hrs=frappe.db.sql("""
            SELECT SUM(at_period) FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s AND spot_task = 1 AND  status not in %s
        """, (name, cb,completed_statuses ))[0][0] or 0 
        for bm_hrs in sprint.sprint_avl_time:
            if bm_hrs.short_code==cb:
                bt_diff_total=bm_hrs.bh
            # else:
            #     bt_diff_total=0
        result.append({
            'cb': cb,
            'biometric_hours':bt_diff_total,
            'allocated_count': allocated,
            'spot_count': spot,
            'total_count':allocated+spot,
            'allocated_completed': a_comp,
            'spot_completed': s_comp,
            'total_completed':a_comp+s_comp,
            'allocated_pending': a_not_comp,
            'spot_pending': s_not_comp,
            'total_pending':(a_not_comp)+(s_not_comp),
            'allocated_not_taken':a_nt,
            'spot_not_taken':s_nt,
            'total_not_taken':a_nt+s_nt,
            'allocated_hrs':alloc_rt,
            'spot_hrs':spot_rt,
            'total_hrs':alloc_rt+spot_rt,
            'allocated_completed_hrs': a_comp_rt,
            'spot_completed_hrs': s_comp_rt,
            'total_completed_hrs':a_comp_rt+s_comp_rt,
            'allocated_pending_hrs': a_not_comp_rt,
            'spot_pending_hrs': s_not_comp_rt,
            'total_pending_hrs':(a_not_comp_rt)+(s_not_comp_rt),
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

@frappe.whitelist()
def get_tasks_for_sprint(team):
    result=[]
    # tl=frappe.db.get_value('Employee',{'status':'Active','custom_dev_team':team,'custom_is_tl':1},['short_code'])
    # user_id=frappe.db.get_value('Employee',{'status':'Active','custom_dev_team':team,'custom_is_tl':1},['user_id'])
    # team_list=[]
    # team_members=frappe.db.get_all('Employee',{'status':'Active','custom_dev_team':team,'custom_is_tl':0},['user_id'])
    # for tm in team_members:
    #     team_list.append(tm.user_id)
    # team_name=frappe.db.get_value('Dev Team', {'code_reviewer': user_id}, ['name'])
    # if team_name:
    #     team_tl=frappe.db.get_value('Employee', {'status':'Active','custom_is_tl': 1,'custom_dev_team':team_name}, ['user_id'])
    #     if team_tl:
    #         team_list.append(team_tl)
    wrk_tasks=frappe.db.get_all('Task',{'custom_dev_team':team,'status':('in',('Open','Working'))},['actual_time','subject','name','kt_confirmed','status','priority','type','cb','custom_production_date','expected_time','project','creation'])
    for tl_t in wrk_tasks:
        result.append({
            'project':tl_t.project,
            'task':tl_t.name,
            'subject':tl_t.subject,
            'cb':tl_t.cb,
            # 'task_type':tl_t.type,
            'kt_confirmed':tl_t.kt_confirmed,
            'et':tl_t.expected_time,
            'at': round(tl_t.actual_time,2),
            'rt':tl_t.rt,
            'status':tl_t.status,
            'priority':tl_t.priority,
            'production_date':tl_t.custom_production_date,
            'previous_sprint':0,
            'created_on':tl_t.creation
        })
    # cdr_tasks=frappe.db.get_all('Task',{'custom_allocated_to':('in',(team_list)),'status':'Code Review'},['actual_time','subject','name','kt_confirmed','status','priority','type','cb','custom_production_date','expected_time','project'])
    # for tl_t in cdr_tasks:
    #     result.append({
    #         'project':tl_t.project,
    #         'task':tl_t.name,
    #         'subject':tl_t.subject,
    #         'cb':tl,
    #         'task_type':tl_t.type,
    #         'kt_confirmed':tl_t.kt_confirmed,
    #         'et':tl_t.expected_time,
    #         'at':tl_t.actual_time,
    #         'rt':0.5,
    #         'status':tl_t.status,
    #         'priority':tl_t.priority,
    #         'production_date':tl_t.custom_production_date,
    #         'previous_sprint':1
    #     })
    result.sort(key=lambda x: x['cb'] or '')
    return result

@frappe.whitelist()
def get_retro_summary_html(name):
    sprint = frappe.get_doc('Sprint', name)
    if today > sprint.to_date:
        end_date=sprint.to_date
    else:
        end_date=add_days(today,-1)
    original_cb_list = [s.short_code for s in sprint.sprint_avl_time]
    if not original_cb_list:
        return []
    cb_list=[]
    tl_cb = []
    non_tl_cb = []
    for cb in original_cb_list:
        has_tl = frappe.db.exists(
            "Employee",
            {"short_code": cb, "custom_is_tl": 1}
        )
        if has_tl:
            tl_cb.append(cb)
        else:
            non_tl_cb.append(cb)

    cb_list = tl_cb + non_tl_cb
    table = f"""
    <table border="1" cellpadding="5" cellspacing="0" width=100% style="border-collapse: collapse; text-align: center;">
        <thead>
            <tr>
                <th style="color:red;">{name}</th>
                <th colspan="4" style="background:#d9edf7;">Sprint</th>
                <th colspan="4" style="background:#fcf8e3;">Others</th>
                <th colspan="7" style="background:#f0b616;">Total</th>
                <th colspan="2" style="background:#f0b616;">Observation</th>
            </tr>
            <tr>
                <th style="background:#020c59;color:white;">CB</th>
                <th style="background:#020c59;color:white;">Plan</th><th style="background:#020c59;color:white;">Comp.</th><th style="background:#020c59;color:white;">Work</th><th style="background:#020c59;color:white;">NT</th>
                <th style="background:#020c59;color:white;">Plan</th><th style="background:#020c59;color:white;">Comp.</th><th style="background:#020c59;color:white;">Work</th><th style="background:#020c59;color:white;">NT</th>
                <th style="background:#020c59;color:white;">Plan</th><th style="background:#020c59;color:white;">Attd</th><th style="background:#020c59;color:white;">AT Period</th><th style="background:#020c59;color:white;">Used(%)</th><th style="background:#020c59;color:white;">Comp(%)</th><th style="background:#020c59;color:white;">Work(%)</th><th style="background:#020c59;color:white;">NT(%)</th>
                <th style="background:#020c59;color:white;">NC</th><th style="background:#020c59;color:white;">REOPEN</th>
            </tr>
            <tr><th colspan="18" style="background:#e8edea;">(in Hours)</th></tr>
        </thead>
        <tbody>
    """
    sub_total_rt=0
    sub_tot_comp_rt=0
    sub_tot_work_rt=0
    sub_nt_rt=0
    sub_total_s_rt=0
    sub_tot_comp_srt=0
    sub_tot_work_srt=0
    sub_nt_srt=0
    sub_total=0
    sub_bt_hours=0
    sub_used_percent=0
    sub_comp_per=0
    sub_ncomp_per=0
    sub_not_taken_percent=0
    used_percent=0
    comp_percent=0
    ncomp_percent=0
    nt_percent=0
    sr_no=1
    tot_bt_hrs=0
    reopen_count=0
    tot_reopen_count=0
    tot_nc_rt=0
    for cb in cb_list:
        emp=frappe.db.get_value('Employee',{'short_code':cb},['name'])
        user_id=frappe.db.get_value('Employee',{'short_code':cb},['user_id'])
        ts_list=[]
        for taken in sprint.sprint_task:
            if taken.cb==cb and taken.at_period and taken.at_period > 0:
                ts_list.append(taken.task)
        total_rt = 0
        total_s_rt = 0
        nt_rt=0
        nt_srt=0
        tot_comp_rt=0
        tot_work_rt=0
        tot_comp_srt=0
        tot_work_srt=0
        nc_rt=0
        # comp=[]
        # not_comp=[]
        completed_hrs=0 
        ncompleted_hrs=0
        for st in sprint.sprint_task:
            if st.cb == cb:
                if st.spot_task == 0:
                    total_rt += st.rt or 0
                    if st.cr_status not in ['Open','Working','Code Review']:
                        # comp.append(st.task)
                        tot_comp_rt+= st.rt or 0
                        completed_hrs+=st.at_period
                    else:
                        # not_comp.append(st.task)
                        tot_work_rt+= st.rt or 0
                        ncompleted_hrs+=st.at_period
                    if st.task not in ts_list:
                        nt_rt+=st.rt or 0  

                else:
                    total_s_rt += st.rt or 0
                    if st.cr_status not in ['Open','Working','Code Review']:
                        # comp.append(st.task)
                        tot_comp_srt+= st.rt or 0
                        completed_hrs+=st.at_period
                    else:
                        # not_comp.append(st.task)
                        tot_work_srt+= st.rt or 0
                        ncompleted_hrs+=st.at_period
                    if st.task not in ts_list:
                        nt_srt+=st.rt or 0
                reopen=frappe.db.get_value('Task',{'name':st.rt,'custom_allocated_to':user_id},['revisions'])
                if reopen:
                    if int(reopen) > 1:
                        reopen_count+=st.rt
                if frappe.db.exists('Energy Point And Non Conformity',{'task':st.task,'docstatus':['!=',2],'emp':emp}):
                    nc_rt+=st.rt
        bt_hours = frappe.db.sql("""
            SELECT IFNULL(SUM(bt_difference), 0)
            FROM `tabAttendance`
            WHERE employee = %s
            AND docstatus != 2
            AND attendance_date BETWEEN %s AND %s
        """, (emp, sprint.from_date, end_date))[0][0]
        bt_hours=round(bt_hours,2)
        ts_hours = frappe.db.sql("""
            SELECT IFNULL(SUM(total_hours), 0)
            FROM `tabTimesheet`
            WHERE employee = %s
            AND docstatus != 2
            AND start_date BETWEEN %s AND %s
        """, (emp, sprint.from_date, end_date))[0][0]
        
        if ts_hours > 0 and bt_hours > 0:
            used_percent=(ts_hours/bt_hours)*100
        else:
            used_percent=0
        
        if completed_hrs > 0:
            comp_percent=(completed_hrs/ts_hours)*100
        else:
            comp_percent=0
        if ncompleted_hrs > 0:
            ncomp_percent=(ncompleted_hrs/ts_hours)*100
        else:
            ncomp_percent=0
        if nt_rt+nt_srt > 0:
            tot_nt=nt_rt+nt_srt
            tot_alloc=total_rt+total_s_rt
            nt_percent=(tot_nt/tot_alloc)*100
        # frappe.errprint(nt_percent)
        used_percent=round(used_percent,2)
        comp_percent=round(comp_percent,2)
        ncomp_percent=round(ncomp_percent,2)
        nt_percent=round(float(nt_percent),2)
        tot_reopen_count+=round(reopen_count,2)
        ts_hours=round(ts_hours,2)
        tot_bt_hrs+=ts_hours
        sub_total_rt+=total_rt
        sub_tot_comp_rt+=tot_comp_rt
        sub_tot_work_rt+=tot_work_rt
        sub_nt_rt+=nt_rt
        sub_total_s_rt+=total_s_rt
        sub_tot_comp_srt+=tot_comp_srt
        sub_tot_work_srt+=tot_work_srt
        sub_nt_srt+=nt_srt
        sub_total+=total_rt+total_s_rt
        sub_bt_hours+=bt_hours
        sub_used_percent+=used_percent
        sub_comp_per+=comp_percent
        sub_ncomp_per+=ncomp_percent
        sub_not_taken_percent+=nt_percent
        tot_nc_rt+=nc_rt
        if sr_no % 2 == 0:
            color = '#e8edea'
        else:
            color = '#ffffff'
        used_percent=str(used_percent) + '%'
        comp_percent=str(comp_percent) + '%'
        ncomp_percent=str(ncomp_percent) + '%'
        nt_percent_s=str(nt_percent) + '%'
        table += f"""
        <tr style="background-color: {color};">
            <td>{cb}</td>
            <td>{total_rt}</td>
            <td>{tot_comp_rt}</td>
            <td>{tot_work_rt}</td>
            <td>{nt_rt}</td>
            <td>{total_s_rt}</td>
            <td>{tot_comp_srt}</td>
            <td>{tot_work_srt}</td>
            <td>{nt_srt}</td>
            <td>{total_rt+total_s_rt}</td>
            <td>{bt_hours}</td>
            <td>{ts_hours}</td>
            <td>{used_percent}</td>
            <td>{comp_percent}</td>
            <td>{ncomp_percent}</td>
            <td>{nt_percent_s}</td>
            <td>{nc_rt}</td>
            <td>{round(reopen_count,2)}</td>
        </tr>
        """

        sr_no+=1
    table+=f"""
        <tr>
        <td style="background:#020c59;color:white;">Total(Hrs)</td>
        <td style="background:#d9edf7;">{sub_total_rt}</td>
        <td style="background:#d9edf7;">{sub_tot_comp_rt}</td>
        <td style="background:#d9edf7;">{sub_tot_work_rt}</td>
        <td style="background:#d9edf7;">{sub_nt_rt}</td>
        <td style="background:#fcf8e3;">{sub_total_s_rt}</td>
        <td style="background:#fcf8e3;">{sub_tot_comp_srt}</td>
        <td style="background:#fcf8e3;">{sub_tot_work_srt}</td>
        <td style="background:#fcf8e3;">{sub_nt_srt}</td>
        <td style="background:#f0b616;">{sub_total_rt+sub_total_s_rt}</td>
        <td style="background:#f0b616;">{round(sub_bt_hours,2)}</td>
        <td style="background:#f0b616;">{round(tot_bt_hrs,2)}</td>
        <td style="background:#f0b616;">{round(sub_used_percent,2)}</td>
        <td style="background:#f0b616;">{round(sub_comp_per,2)}</td>
        <td style="background:#f0b616;">{round(sub_ncomp_per,2)}</td>
        <td style="background:#f0b616;">{round(sub_not_taken_percent,2)}</td>
        <td style="background:#f0b616;">{tot_nc_rt}</td>
        <td style="background:#f0b616;">{tot_reopen_count}</td>
        </tr>
        """
    table += """
        <tr>
        <td colspan="18" style="background:#e8edea;"><b>(in Count)</b></td>
        </tr>
    """
    s_no = 1
    sub_total = 0
    overall_comp = 0
    overall_work = 0
    overall_nt = 0
    sub_total_count = 0
    sub_total_s_count = 0
    sub_nt_count = 0
    sub_nt_scount = 0
    sub_tot_comp_count = 0
    sub_tot_work_count = 0
    sub_tot_comp_scount = 0
    sub_tot_work_scount = 0
    sub_total_reopen_count = 0
    tot_nc_count = 0
    for cb in cb_list:
        emp = frappe.db.get_value('Employee', {'short_code': cb}, ['name'])
        user_id = frappe.db.get_value('Employee', {'short_code': cb}, ['user_id'])
        ts_list = [taken.task for taken in sprint.sprint_task if taken.cb == cb and taken.at_period and taken.at_period > 0]
        total_count = total_s_count = 0
        nt_count = nt_scount = 0
        tot_comp_count = tot_work_count = 0
        tot_comp_scount = tot_work_scount = 0
        nc_count = 0
        reopen_count = 0
        for st in sprint.sprint_task:
            if st.cb != cb:
                continue
            if st.spot_task == 0:
                total_count += 1
                if st.cr_status not in ['Open', 'Working', 'Code Review']:
                    tot_comp_count += 1
                else:
                    tot_work_count += 1
                if st.task not in ts_list:
                    nt_count += 1
            else:
                total_s_count += 1
                if st.cr_status not in ['Open', 'Working', 'Code Review']:
                    tot_comp_scount += 1
                else:
                    tot_work_scount += 1
                if st.task not in ts_list:
                    nt_scount += 1
            reopen = frappe.db.get_value('Task', {'name': st.rt, 'custom_allocated_to': user_id}, ['revisions'])
            if reopen and int(reopen) > 1:
                reopen_count += int(reopen)
            if frappe.db.exists('Energy Point And Non Conformity', {'task': st.task, 'docstatus': ['!=', 2], 'emp': emp}):
                nc_count += 1
        color = '#e8edea' if s_no % 2 == 0 else '#ffffff'
        sub_total_count += total_count
        sub_tot_comp_count += tot_comp_count
        sub_tot_work_count += tot_work_count
        sub_nt_count += nt_count
        sub_total_s_count += total_s_count
        sub_tot_comp_scount += tot_comp_scount
        sub_tot_work_scount += tot_work_scount
        sub_nt_scount += nt_scount
        sub_total += total_count + total_s_count
        overall_comp += tot_comp_count + tot_comp_scount
        overall_work += tot_work_count + tot_work_scount
        overall_nt += nt_count + nt_scount
        sub_total_reopen_count += reopen_count
        tot_nc_count += nc_count
        table += f"""
        <tr style="background-color: {color};">
            <td>{cb}</td>
            <td>{total_count}</td>
            <td>{tot_comp_count}</td>
            <td>{tot_work_count}</td>
            <td>{nt_count}</td>
            <td>{total_s_count}</td>
            <td>{tot_comp_scount}</td>
            <td>{tot_work_scount}</td>
            <td>{nt_scount}</td>
            <td>{total_count + total_s_count}</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>{tot_comp_count + tot_comp_scount}</td>
            <td>{tot_work_count + tot_work_scount}</td>
            <td>{nt_count + nt_scount}</td>
            <td>{nc_count}</td>
            <td>{reopen_count}</td>
        </tr>
        """
        s_no += 1
    table += f"""
    <tr>
        <td style="background:#020c59;color:white;">Total(Count)</td>
        <td style="background:#d9edf7;">{sub_total_count}</td>
        <td style="background:#d9edf7;">{sub_tot_comp_count}</td>
        <td style="background:#d9edf7;">{sub_tot_work_count}</td>
        <td style="background:#d9edf7;">{sub_nt_count}</td>
        <td style="background:#fcf8e3;">{sub_total_s_count}</td>
        <td style="background:#fcf8e3;">{sub_tot_comp_scount}</td>
        <td style="background:#fcf8e3;">{sub_tot_work_scount}</td>
        <td style="background:#fcf8e3;">{sub_nt_scount}</td>
        <td style="background:#f0b616;">{sub_total_count + sub_total_s_count}</td>
        <td style="background:#f0b616;">-</td>
        <td style="background:#f0b616;">-</td>
        <td style="background:#f0b616;">-</td>
        <td style="background:#f0b616;">{overall_comp}</td>
        <td style="background:#f0b616;">{overall_work}</td>
        <td style="background:#f0b616;">{overall_nt}</td>
        <td style="background:#f0b616;">{tot_nc_count}</td>
        <td style="background:#f0b616;">{sub_total_reopen_count}</td>
    </tr>
    """
    table+="""
        </body>
        </table>
    """
    return table

@frappe.whitelist()
def get_retro_summary_html_test(name):
    sprint = frappe.get_doc('Sprint', name)
    end_date = sprint.to_date
    original_cb_list = [s.short_code for s in sprint.sprint_avl_time]
    if not original_cb_list:
        return []
    tl_cb = []
    non_tl_cb = []
    for cb in original_cb_list:
        if frappe.db.exists("Employee", {"short_code": cb, "custom_is_tl": 1}):
            tl_cb.append(cb)
        else:
            non_tl_cb.append(cb)
    cb_list = tl_cb + non_tl_cb
    table = f"""
    <table border="1" cellpadding="5" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: center;">
    <colgroup>
        <!-- 17 columns: 1 + 4 + 4 + 6 + 2 = 17 -->
        <col span="17" style="width: 5.88%;">
    </colgroup>
    <thead>
        <tr>
            <th style="color:red;">{sprint.sprint_id}</th>
            <th colspan="4" style="background:#d9edf7;">Sprint</th>
            <th colspan="4" style="background:#fcf8e3;">Others</th>
            <th colspan="6" style="background:#f0b616;">Total</th>
            <th colspan="2" style="background:#f0b616;">Observation</th>
        </tr>
        <tr>
            <th style="background:#020c59;color:white;">CB</th>
            <th style="background:#020c59;color:white;">Plan</th>
            <th style="background:#020c59;color:white;">Comp.</th>
            <th style="background:#020c59;color:white;">Work</th>
            <th style="background:#020c59;color:white;">NT</th>
            <th style="background:#020c59;color:white;">Plan</th>
            <th style="background:#020c59;color:white;">Comp.</th>
            <th style="background:#020c59;color:white;">Work</th>
            <th style="background:#020c59;color:white;">NT</th>
            <th style="background:#020c59;color:white;">Plan</th>
            <th style="background:#020c59;color:white;">Attd</th>
            <th style="background:#020c59;color:white;">Used</th>
            <th style="background:#020c59;color:white;">Comp</th>
            <th style="background:#020c59;color:white;">Work</th>
            <th style="background:#020c59;color:white;">NT</th>
            <th style="background:#020c59;color:white;">NC</th>
            <th style="background:#020c59;color:white;">REOPEN</th>
        </tr>
        <tr>
            <th style="background:#e8edea;">(in Hours)</th>
            <th style="background:#e8edea;font-size:7px;">Planned RT</th>
            <th style="background:#e8edea;font-size:7px;">Comp RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Work RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Not taken RT</th>
            <th style="background:#e8edea;font-size:7px;">Spot RT</th>
            <th style="background:#e8edea;font-size:7px;">Spot Comp RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Spot Work RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Spot Not taken RT</th>
            <th style="background:#e8edea;font-size:7px;">Total RT</th>
            <th style="background:#e8edea;font-size:7px;">Biometric Hrs</th>
            <th style="background:#e8edea;font-size:7px;">Used Hrs (Used Hrs/Biometric Hrs)%</th>
            <th style="background:#e8edea;font-size:7px;">Completed RT / Completed Hrs (Timesheet against completed tasks/Used Hrs)%</th>
            <th style="background:#e8edea;font-size:7px;">Working RT / Working Hrs (Timesheet against working tasks/Used Hrs)%</th>
            <th style="background:#e8edea;font-size:7px;">Total Not Taken Hours</th>
            <th style="background:#e8edea;font-size:7px;">RT of tasks have NC</th>
            <th style="background:#e8edea;font-size:7px;">RT of tasks have Reopen</th>
        </tr>
    </thead>
    <tbody>
    """

    sub_total_rt = sub_tot_comp_rt = sub_tot_work_rt = sub_nt_rt = 0
    sub_total_s_rt = sub_tot_comp_srt = sub_tot_work_srt = sub_nt_srt = sub_bt_hours = 0
    sub_used_percent = sub_comp_per = sub_ncomp_per = tot_bt_hrs = tot_reopen_count = 0
    tot_c = tot_nc = tot_spr_chrs = tot_spr_whrs = tot_spot_chrs = tot_spot_whrs = tot_nc_rt = 0
    sr_no = 1
    for cb in cb_list:
        if sprint.service and sprint.service=='CMN':
            emp = frappe.db.get_value('Employee', {'short_code': cb,"department": "Support Team - THIS","designation":'Graphic Designer'}, ['name'])
        else:
            emp = frappe.db.get_value('Employee', {'short_code': cb,'custom_dev_team':sprint.team,'department':'IT. Development - THIS'}, ['name'])
        user_id = frappe.db.get_value('Employee', {'short_code': cb,'custom_dev_team':sprint.team,'department':'IT. Development - THIS'}, ['user_id'])
        result = frappe.db.sql("""
            SELECT
                SUM(CASE WHEN spot_task = 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND at_period = 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND at_period = 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN revisions > 0 THEN rt ELSE 0 END)
            FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s
        """, (sprint.name, cb))[0]

        (
            total_rt, tot_comp_rt, spr_comp_hrs, tot_work_rt, spr_wor_hrs, nt_rt,
            total_s_rt, tot_comp_srt, spot_comp_hrs, tot_work_srt, spot_wor_hrs, nt_srt,reopen_count
        ) = [x or 0 for x in result]

        completed_hrs = spr_comp_hrs + spot_comp_hrs
        ncompleted_hrs = spr_wor_hrs + spot_wor_hrs
        nc_rt = 0

        for st in sprint.sprint_task:
            if st.cb != cb:
                continue
            if frappe.db.exists('Energy Point And Non Conformity',
                {'task': st.task, 'docstatus': ['!=', 2], 'emp': emp}):
                nc_rt += st.rt or 0

        bt_hours = frappe.db.sql("""
            SELECT IFNULL(SUM(bt_difference), 0)
            FROM `tabAttendance`
            WHERE employee = %s AND docstatus != 2
            AND attendance_date BETWEEN %s AND %s
        """, (emp, sprint.from_date, end_date))[0][0]
        bt_hours = round(bt_hours or 0, 2)

        ts_hours = frappe.db.sql("""
            SELECT IFNULL(SUM(total_hours), 0)
            FROM `tabTimesheet`
            WHERE employee = %s AND docstatus != 2
            AND start_date BETWEEN %s AND %s
        """, (emp, sprint.from_date, end_date))[0][0]
        ts_hours = round(ts_hours or 0, 2)

        used_percent = (ts_hours / bt_hours) * 100 if ts_hours and bt_hours else 0
        comp_percent = (completed_hrs / ts_hours) * 100 if ts_hours and completed_hrs else 0
        ncomp_percent = (ncompleted_hrs / ts_hours) * 100 if ts_hours and ncompleted_hrs else 0
        tot_c += round(completed_hrs, 2)
        tot_nc += round(ncompleted_hrs, 2)
        tot_reopen_count += round(reopen_count, 2)
        tot_bt_hrs += ts_hours
        tot_spr_chrs += spr_comp_hrs
        tot_spr_whrs += spr_wor_hrs
        tot_spot_chrs += spot_comp_hrs
        tot_spot_whrs += spot_wor_hrs

        sub_total_rt += total_rt
        sub_tot_comp_rt += tot_comp_rt
        sub_tot_work_rt += tot_work_rt
        sub_nt_rt += nt_rt
        sub_total_s_rt += total_s_rt
        sub_tot_comp_srt += tot_comp_srt
        sub_tot_work_srt += tot_work_srt
        sub_nt_srt += nt_srt
        sub_bt_hours += bt_hours
        # sub_used_percent += used_percent
        sub_comp_per += comp_percent
        sub_ncomp_per += ncomp_percent
        tot_nc_rt += nc_rt

        spr_comp_s = f"{round(tot_comp_rt, 2)}/{round(spr_comp_hrs, 2)}"
        spr_ncomp_s = f"{round(tot_work_rt, 2)}/{round(spr_wor_hrs, 2)}"
        spot_comp_s = f"{round(tot_comp_srt, 2)}/{round(spot_comp_hrs, 2)}"
        spot_ncomp_s = f"{round(tot_work_srt, 2)}/{round(spot_wor_hrs, 2)}"

        completed_rt = round(tot_comp_rt + tot_comp_srt, 2)
        working_rt = round(tot_work_rt + tot_work_srt, 2)

        used_percent_str = f"{ts_hours} ({round(used_percent, 2)}%)"
        comp_percent_str = f"{completed_rt} / {round(completed_hrs, 2)} ({round(comp_percent, 2)}%)"
        ncomp_percent_str = f"{working_rt} / {round(ncompleted_hrs, 2)} ({round(ncomp_percent, 2)}%)"
        
        # if comp_percent < 70:
        font_color= "#f02e0c" if comp_percent < 70 else "#110404"
        att_color="#2059d4" if used_percent < 80 else "#110404"
        row_color = '#e8edea' if sr_no % 2 == 0 else '#ffffff'

        table += f"""
        <tr style="background-color: {row_color};color:#110404;">
            <td>{cb}</td>
            <td>{total_rt}</td>
            <td>{spr_comp_s}</td>
            <td>{spr_ncomp_s}</td>
            <td>{nt_rt}</td>
            <td>{total_s_rt}</td>
            <td>{spot_comp_s}</td>
            <td>{spot_ncomp_s}</td>
            <td>{nt_srt}</td>
            <td>{round((total_rt + total_s_rt),2)}</td>
            <td>{bt_hours}</td>
            <td  style="color: {att_color};">{used_percent_str}</td>
            <td style="color: {font_color};font-size:12px;">{comp_percent_str}</td>
            <td style="font-size:12px;">{ncomp_percent_str}</td>
            <td>{round(nt_rt + nt_srt, 2)}</td>
            <td>{nc_rt}</td>
            <td>{round(reopen_count, 2)}</td>
        </tr>
        """

        sr_no += 1
    if sub_bt_hours > 0:
        sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
    else:
        sub_used_str=0
    if  tot_bt_hrs > 0:
        sub_comp_str=(tot_c/tot_bt_hrs)*100
    else:
        sub_comp_str=0
    if  tot_bt_hrs > 0:
        sub_work_str=(tot_nc/tot_bt_hrs)*100
    else:
        sub_work_str=0
    font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
    att_color="#2059d4" if sub_used_str < 80 else "#110404"
    sub_used_str = f"{round(tot_bt_hrs, 2)} ({round(sub_used_str, 2)})"
    sub_comp_str = f"{round(tot_c, 2)} ({round(sub_comp_str, 2)})"
    sub_work_str = f"{round(tot_nc, 2)} ({round(sub_work_str, 2)})"
    
    table += f"""
    <tr>
        <td style="background:#020c59;color:white;">Total(Hrs)</td>
        <td style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
        <td style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/{round(tot_spr_chrs, 2)}</td>
        <td style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/{round(tot_spr_whrs, 2)}</td>
        <td style="background:#d9edf7;color:#110404;">{round(sub_nt_rt,1)}</td>
        <td style="background:#fcf8e3;color:#110404;">{round(sub_total_s_rt,2)}</td>
        <td style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/{round(tot_spot_chrs, 2)}</td>
        <td style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/{round(tot_spot_whrs, 2)}</td>
        <td style="background:#fcf8e3;color:#110404;">{round(sub_nt_srt,1)}</td>
        <td style="background:#f0b616;color:#110404;">{round((sub_total_rt + sub_total_s_rt),2)}</td>
        <td style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
        <td style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
        <td style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
        <td style="background:#f0b616;color:#110404;">{sub_work_str}</td>
        <td style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
        <td style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
        <td style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
    </tr>
    <tr>
        <th colspan="17" style="background:#e8edea;">
            (in Count) <span style="color:#2059d4;">Used percent should be minimum of 80% </span> <span style="color:red;">Comp percent should be minimum of 70%</span>
        </th>
    </tr>

    """
    
    sub_total_count = sub_tot_comp_count =sub_tot_work_count =sub_nt_count =sub_total_s_count =0
    sub_tot_comp_scount = sub_tot_work_scount=sub_nt_scount=sub_total=overall_comp=0
    overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=0
    s_no=1
    for cb in cb_list:
        emp = frappe.db.get_value('Employee', {'short_code': cb,'custom_dev_team':sprint.team,'department':'IT. Development - THIS'}, 'name')
        user_id = frappe.db.get_value('Employee', {'short_code': cb,'custom_dev_team':sprint.team,'department':'IT. Development - THIS'}, 'user_id')

        counts = frappe.db.sql("""
            SELECT
                SUM(CASE WHEN st.spot_task = 0 THEN 1 ELSE 0 END) AS total_count,
                SUM(CASE WHEN st.spot_task = 0 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_count,
                SUM(CASE WHEN st.spot_task = 0 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_count,
                SUM(CASE WHEN st.spot_task = 0 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_count,
                SUM(CASE WHEN st.spot_task = 1 THEN 1 ELSE 0 END) AS total_s_count,
                SUM(CASE WHEN st.spot_task = 1 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_scount,
                SUM(CASE WHEN st.spot_task = 1 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_scount,
                SUM(CASE WHEN st.spot_task = 1 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_scount,
                SUM(CASE WHEN st.revisions > 0 THEN revisions ELSE 0 END) AS reopen_count
            FROM `tabSprint Task` st
            WHERE st.parent = %s AND st.cb = %s
        """, (sprint.name, cb), as_dict=1)[0]

        total_count = counts.total_count or 0
        tot_comp_count = counts.tot_comp_count or 0
        tot_work_count = counts.tot_work_count or 0
        nt_count = counts.nt_count or 0
        total_s_count = counts.total_s_count or 0
        tot_comp_scount = counts.tot_comp_scount or 0
        tot_work_scount = counts.tot_work_scount or 0
        nt_scount = counts.nt_scount or 0
        reopen_count=counts.reopen_count or 0
        # reopen_count = frappe.db.sql("""
        #     SELECT IFNULL(SUM(CAST(t.revisions AS UNSIGNED)), 0)
        #     FROM `tabSprint Task` st
        #     JOIN `tabTask` t ON t.name = st.rt
        #     WHERE st.parent = %s 
        #     AND st.cb = %s 
        #     AND t.custom_allocated_to = %s 
        #     AND IFNULL(t.revisions, 0) > 0
        # """, (sprint.name, cb, user_id))[0][0] or 0

        nc_count = frappe.db.sql("""
            SELECT SUM(e.nc_score)
            FROM `tabSprint Task` st
            JOIN `tabEnergy Point And Non Conformity` e
            ON e.task = st.task
            WHERE st.parent = %s
            AND st.cb = %s
            AND e.emp = %s
            AND e.docstatus != 2
        """, (sprint.name, cb, emp))[0][0] or 0

        # nc_count = frappe.db.sql("""
        #     SELECT COUNT(DISTINCT st.task)
        #     FROM `tabSprint Task` st
        #     WHERE st.parent = %s AND st.cb = %s
        #     AND EXISTS (
        #         SELECT 1 FROM `tabEnergy Point And Non Conformity` e
        #         WHERE e.task = st.task AND e.emp = %s AND e.docstatus != 2
        #     )
        # """, (sprint.name, cb, emp))[0][0] or 0

        color = '#e8edea' if s_no % 2 == 0 else '#ffffff'

        sub_total_count += total_count
        sub_tot_comp_count += tot_comp_count
        sub_tot_work_count += tot_work_count
        sub_nt_count += nt_count
        sub_total_s_count += total_s_count
        sub_tot_comp_scount += tot_comp_scount
        sub_tot_work_scount += tot_work_scount
        sub_nt_scount += nt_scount
        sub_total += total_count + total_s_count
        overall_comp += tot_comp_count + tot_comp_scount
        overall_work += tot_work_count + tot_work_scount
        overall_nt += nt_count + nt_scount
        sub_total_reopen_count += reopen_count
        tot_nc_count += nc_count

        table += f"""
        <tr style="background-color: {color};color:#110404;">
            <td>{cb}</td>
            <td>{total_count}</td>
            <td>{tot_comp_count}</td>
            <td>{tot_work_count}</td>
            <td>{nt_count}</td>
            <td>{total_s_count}</td>
            <td>{tot_comp_scount}</td>
            <td>{tot_work_scount}</td>
            <td>{nt_scount}</td>
            <td>{total_count + total_s_count}</td>
            <td>-</td>
            <td>-</td>
            <td>{tot_comp_count + tot_comp_scount}</td>
            <td>{tot_work_count + tot_work_scount}</td>
            <td>{nt_count + nt_scount}</td>
            <td>{nc_count}</td>
            <td>{reopen_count}</td>
        </tr>
        """
        s_no += 1

    table += f"""
    <tr>
        <td style="background:#020c59;color:white;">Total(Count)</td>
        <td style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
        <td style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
        <td style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
        <td style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
        <td style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
        <td style="background:#f0b616;color:#110404;">-</td>
        <td style="background:#f0b616;color:#110404;">-</td>
        <td style="background:#f0b616;color:#110404;">{overall_comp}</td>
        <td style="background:#f0b616;color:#110404;">{overall_work}</td>
        <td style="background:#f0b616;color:#110404;">{overall_nt}</td>
        <td style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
        <td style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
    </tr>
    """
    table += """
        </tbody></table>
    """

    return table

from frappe.utils import flt
@frappe.whitelist()
def update_spr_table(name):
# def update_spr_table():
#     name="SPM00076"
    spr = frappe.get_doc('Sprint', name)
    tasks = []  
    # Update existing rows
    for i in spr.sprint_task:
        tasks.append(i.task)
        if i.cb:
            if spr.service =='CMN':
                emp_id =frappe.db.get_value('Employee', {'short_code': i.cb,"department": "Support Team - THIS","designation":'Graphic Designer'}, ['name'])
            else:
                emp_id = frappe.db.get_value('Employee', {'short_code': i.cb,'custom_dev_team':spr.team,'department':'IT. Development - THIS'}, ['name'])
            if frappe.db.exists('Task', {'name': i.task}):
                cr_status = frappe.db.get_value('Task', {'name': i.task}, ['status'])
                task_at = frappe.db.get_value("Task",{'name': i.task},['actual_time'])
                task_rt = frappe.db.get_value('Task', i.task, 'rt') or 0
                if flt(i.rt) != flt(task_rt):
                    i.rt = task_rt
                tot_at = frappe.db.sql("""
                    SELECT SUM(cs.hours) as total
                    FROM `tabTimesheet` c
                    INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                    WHERE cs.task=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
                """, (i.task, emp_id, spr.from_date, spr.to_date), as_dict=True)[0].total or 0.0
            elif frappe.db.exists('Issue', {'name': i.task}):
                cr_status = frappe.db.get_value('Issue', {'name': i.task}, ['custom_issue_status'])
                task_at = frappe.db.get_value("Task",{'name': i.task},['actual_time'])
                tot_at = frappe.db.sql("""
                    SELECT SUM(cs.hours) as total
                    FROM `tabTimesheet` c
                    INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                    WHERE cs.custom_issue=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
                """, (i.task, emp_id, spr.from_date, spr.to_date), as_dict=True)[0].total or 0.0
            else:
                tot_at = 0
                cr_status = 'Completed'
            i.cr_status = cr_status
            i.at_period = round(tot_at,2)
            if task_at:
                i.at = round(task_at,2)

    from frappe.utils import today 
    emp_list = frappe.db.get_all('Employee', {'custom_dev_team': spr.team,'department':'IT. Development - THIS'}, ['name', 'short_code','user_id','custom_is_tl','custom_tl'])
    for e in emp_list:
        tasks = []  
        # Update existing rows
        for i in spr.sprint_task:
            if i.cb ==e.short_code:
                tasks.append(i.task)
        today_date = today() 
        if getdate(spr.to_date) < getdate(today_date):
            today_date=getdate(spr.to_date)
        ts = frappe.db.get_value('Timesheet', {'employee': e.name, 'start_date': today_date,"docstatus":["!=",2]},'name')
        if not ts:
            continue  
        task_query = """
            SELECT
                `tabTimesheet Detail`.task AS key_id,
                SUM(`tabTimesheet Detail`.hours) AS total_hours
            FROM `tabTimesheet`
            LEFT JOIN `tabTimesheet Detail` 
                ON `tabTimesheet`.name = `tabTimesheet Detail`.parent
            WHERE `tabTimesheet Detail`.task IS NOT NULL
                AND `tabTimesheet`.name = %s
            GROUP BY `tabTimesheet Detail`.task
        """
        rows = frappe.db.sql(task_query, (ts,), as_dict=True)
        for r in rows:
            key = r.key_id
            prior=frappe.db.get_value('Task',{'name':key},['priority'])
            project=frappe.db.get_value('Task',{'name':key},['project'])
            alloc=frappe.db.get_value('Task',{'name':key},['custom_allocated_to'])
            if e.user_id!=alloc:
                rt=0.5
            else:
                rt=frappe.db.get_value('Task',{'name':key},['rt'])
            if key and key not in tasks:
                # print('key')
                # print(key)
                sub=frappe.db.get_value('Task',{'name':key},['subject'])
                spr.append('sprint_task', {
                    'task': key,
                    'subject':sub,
                    'cb': e.short_code,
                    'at_period':round( r.total_hours,2),
                    'status': get_cr_status(key),
                    'cr_status': get_cr_status(key),
                    'spot_task':1,
                    'priority':prior,
                    'project':project,
                    'rt':rt
                })
                tasks.append(key)  
        task_query = """
            SELECT
                `tabTimesheet Detail`.custom_issue AS key_id,
                SUM(`tabTimesheet Detail`.hours) AS total_hours
            FROM `tabTimesheet`
            LEFT JOIN `tabTimesheet Detail` 
                ON `tabTimesheet`.name = `tabTimesheet Detail`.parent
            WHERE `tabTimesheet Detail`.custom_issue IS NOT NULL
                AND `tabTimesheet`.name = %s
            GROUP BY `tabTimesheet Detail`.custom_issue
        """
        rows = frappe.db.sql(task_query, (ts,), as_dict=True)
        

        for r in rows:
            key = r.key_id
            prior=frappe.db.get_value('Issue',{'name':key},['priority'])
            project=frappe.db.get_value('Issue',{'name':key},['project'])
            rt=0.5

            if key and key not in tasks:
                # print('key1')
                # print(key)
                sub=frappe.db.get_value('Issue',{'name':key},['subject'])
                spr.append('sprint_task', {
                    'task': key,
                    'cb': e.short_code,
                    'at_period': round(r.total_hours,2),
                    'status': get_cr_status(key),
                    'cr_status': get_cr_status(key),
                    'spot_task':1,
                    'priority':prior,
                    'project':project,
                    'subject':sub,
                    'rt':rt
                })
                tasks.append(key) 
    
    
        query = """
            SELECT 
                name, project, subject, custom_allocated_to, status,
                expected_time, rt, actual_time, priority,
                custom_remarks, custom_dev_team, custom_sprint
            FROM `tabTask`
            WHERE custom_allocated_to = %s AND custom_production_date =%s
            ORDER BY custom_allocated_to, project, priority
        """
        task_data = frappe.db.sql(query, (e.user_id,today_date), as_dict=1)

        for task in task_data:
            task_id = task.name
            if e.custom_is_tl:
                rt=0.5
                cdr_employees = frappe.db.get_all(
                    'Employee', 
                    {'custom_is_tl': 0, 'custom_tl': e.name}, 
                    pluck="user_id"
                )
                cdr_reviewer_team =frappe.db.get_value('Dev Team',{'code_reviewer':e.user_id},'name')
                tl_short_code =frappe.db.get_value('Employee',{'custom_dev_team':cdr_reviewer_team,"custom_is_tl":1,'department':'IT. Development - THIS'},'short_code')
                cdr_reviewer =frappe.db.get_value('Employee',{'custom_dev_team':cdr_reviewer_team,"custom_is_tl":1,'department':'IT. Development - THIS'},'user_id')
                query = """
                    SELECT 
                        name, project, subject, custom_allocated_to, status,
                        expected_time, rt, actual_time, priority,
                        custom_remarks, custom_dev_team, custom_sprint
                    FROM `tabTask`
                    WHERE custom_allocated_to = %s AND custom_pr_date =%s
                    ORDER BY custom_allocated_to, project, priority
                """
                cdr_task_data = frappe.db.sql(query, (cdr_reviewer,today_date), as_dict=1)
                for cdr_task in cdr_task_data:
                    if cdr_task.name and cdr_task.name not in tasks:
                        at_period = frappe.db.sql("""
                            SELECT SUM(d.hours) AS hours
                            FROM `tabTimesheet Detail` d
                            JOIN `tabTimesheet` t ON d.parent = t.name
                            WHERE t.docstatus != 2 AND t.start_date BETWEEN %s AND %s AND t.employee = %s AND d.task = %s
                        """, (getdate(spr.from_date),getdate(spr.to_date), e.name, cdr_task.name), as_dict=1)[0].hours or 0
                        spr.append('sprint_task', {
                            'task': cdr_task.name,
                            'subject': cdr_task.subject,
                            'cb': e.short_code,
                            'at_period': at_period,
                            'status': get_cr_status(cdr_task.name),
                            'cr_status': get_cr_status(cdr_task.name),
                            'spot_task': 1,
                            'priority': cdr_task.priority,
                            'project': cdr_task.project,
                            'rt': 0.5
                        })
                        tasks.append(cdr_task.name)  
                  
                query = """
                    SELECT 
                        name, project, subject, custom_allocated_to, status,
                        expected_time, rt, actual_time, priority,
                        custom_remarks, custom_dev_team, custom_sprint
                    FROM `tabTask`
                    WHERE custom_allocated_to IN %s AND custom_pr_date =%s
                    ORDER BY custom_allocated_to, project, priority
                """
                # cdr_task_data_for_teams = frappe.db.sql(query, (cdr_employees,today_date), as_dict=1)
                # for cdr_task in cdr_task_data_for_teams:
                    # if cdr_task.name and cdr_task.name not in tasks:
                    #     at_period = frappe.db.sql("""
                    #         SELECT SUM(d.hours) AS hours
                    #         FROM `tabTimesheet Detail` d
                    #         JOIN `tabTimesheet` t ON d.parent = t.name
                    #         WHERE t.docstatus != 2 AND t.start_date BETWEEN %s AND %s AND t.employee = %s AND d.task = %s
                    #     """, (getdate(spr.from_date),getdate(spr.to_date), e.name, cdr_task.name), as_dict=1)[0].hours or 0
                    #     spr.append('sprint_task', {
                    #         'task': cdr_task.name,
                    #         'subject': cdr_task.subject,
                    #         'cb': e.short_code,
                    #         'at_period': at_period,
                    #         'status': get_cr_status(cdr_task.name),
                    #         'cr_status': get_cr_status(cdr_task.name),
                    #         'spot_task': 1,
                    #         'priority': cdr_task.priority,
                    #         'project': cdr_task.project,
                    #         'rt': 0.5
                    #     })
                    #     tasks.append(cdr_task.name)
            if e.user_id != task.custom_allocated_to:
                rt = 0.5
            else:
                rt = task.rt
            
            if task_id and task_id not in tasks:
                at_period = frappe.db.sql("""
                    SELECT SUM(d.hours) AS hours
                    FROM `tabTimesheet Detail` d
                    JOIN `tabTimesheet` t ON d.parent = t.name
                    WHERE t.docstatus != 2 AND t.start_date BETWEEN %s AND %s AND t.employee = %s AND d.task = %s
                """, (getdate(spr.from_date),getdate(spr.to_date), e.name, task_id), as_dict=1)[0].hours or 0
                spr.append('sprint_task', {
                    'task': task_id,
                    'subject': task.subject,
                    'cb': e.short_code,
                    'at_period': at_period,
                    'status': get_cr_status(task_id),
                    'cr_status': get_cr_status(task_id),
                    'spot_task': 1,
                    'priority': task.priority,
                    'project': task.project,
                    'rt': rt
                })
                
                tasks.append(task_id)  

    spr.save(ignore_permissions=True)
    frappe.db.commit()

  

def get_cr_status(key):
    if frappe.db.exists('Task', {'name': key}):
        return frappe.db.get_value('Task', {'name': key}, ['status'])
    elif frappe.db.exists('Issue', {'name': key}):
        return frappe.db.get_value('Issue', {'name': key}, ['custom_issue_status'])
    else:
        return 'Completed'

@frappe.whitelist()
def get_sprint_employees(short_codes, team):
    if not short_codes:
        return []

    employees = frappe.db.get_all(
        "Employee",
        filters={
            "short_code": ["in", short_codes],
            "custom_dev_team": team,
            "department": "IT. Development - THIS"
        },
        fields=[
            "name",
            "employee_name",
            "image",
            "short_code",
            "custom_is_tl",
            "custom_dev_team",
            "department"
        ]
    )
    return employees



@frappe.whitelist()
def get_retro_summary_html_for_cnm_service(name):
    sprint = frappe.get_doc('Sprint', name)
    end_date = sprint.to_date
    cb_list = [s.short_code for s in sprint.sprint_avl_time]
    table = f"""
    <table border="1" cellpadding="5" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: center;">
    <colgroup>
        <col span="17" style="width: 5.88%;">
    </colgroup>
    <thead>
        <tr>
            <th style="color:red;">{sprint.sprint_id}</th>
            <th colspan="4" style="background:#d9edf7;">Sprint</th>
            <th colspan="4" style="background:#fcf8e3;">Others</th>
            <th colspan="6" style="background:#f0b616;">Total</th>
            <th colspan="2" style="background:#f0b616;">Observation</th>
        </tr>
        <tr>
            <th style="background:#020c59;color:white;">CB</th>
            <th style="background:#020c59;color:white;">Plan</th>
            <th style="background:#020c59;color:white;">Comp.</th>
            <th style="background:#020c59;color:white;">Work</th>
            <th style="background:#020c59;color:white;">NT</th>
            <th style="background:#020c59;color:white;">Plan</th>
            <th style="background:#020c59;color:white;">Comp.</th>
            <th style="background:#020c59;color:white;">Work</th>
            <th style="background:#020c59;color:white;">NT</th>
            <th style="background:#020c59;color:white;">Plan</th>
            <th style="background:#020c59;color:white;">Attd</th>
            <th style="background:#020c59;color:white;">Used</th>
            <th style="background:#020c59;color:white;">Comp</th>
            <th style="background:#020c59;color:white;">Work</th>
            <th style="background:#020c59;color:white;">NT</th>
            <th style="background:#020c59;color:white;">NC</th>
            <th style="background:#020c59;color:white;">REOPEN</th>
        </tr>
        <tr>
            <th style="background:#e8edea;">(in Hours)</th>
            <th style="background:#e8edea;font-size:7px;">Planned RT</th>
            <th style="background:#e8edea;font-size:7px;">Comp RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Work RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Not taken RT</th>
            <th style="background:#e8edea;font-size:7px;">Spot RT</th>
            <th style="background:#e8edea;font-size:7px;">Spot Comp RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Spot Work RT/AT</th>
            <th style="background:#e8edea;font-size:7px;">Spot Not taken RT</th>
            <th style="background:#e8edea;font-size:7px;">Total RT</th>
            <th style="background:#e8edea;font-size:7px;">Biometric Hrs</th>
            <th style="background:#e8edea;font-size:7px;">Used Hrs (Used Hrs/Biometric Hrs)%</th>
            <th style="background:#e8edea;font-size:7px;">Completed Hrs (Timesheet against completed tasks/Used Hrs)%</th>
            <th style="background:#e8edea;font-size:7px;">Working Hrs (Timesheet against working tasks/Used Hrs)%</th>
            <th style="background:#e8edea;font-size:7px;">Total Not Taken Hours</th>
            <th style="background:#e8edea;font-size:7px;">RT of tasks have NC</th>
            <th style="background:#e8edea;font-size:7px;">RT of tasks have Reopen</th>
        </tr>
    </thead>
    <tbody>
    """

    sub_total_rt = sub_tot_comp_rt = sub_tot_work_rt = sub_nt_rt = 0
    sub_total_s_rt = sub_tot_comp_srt = sub_tot_work_srt = sub_nt_srt = sub_bt_hours = 0
    sub_used_percent = sub_comp_per = sub_ncomp_per = tot_bt_hrs = tot_reopen_count = 0
    tot_c = tot_nc = tot_spr_chrs = tot_spr_whrs = tot_spot_chrs = tot_spot_whrs = tot_nc_rt = 0
    sr_no = 1
    for cb in cb_list:
        emp = frappe.db.get_value('Employee', {'short_code': cb,"department": "Support Team - THIS","designation":'Graphic Designer'}, ['name'])
        result = frappe.db.sql("""
            SELECT
                SUM(CASE WHEN spot_task = 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 0 AND at_period = 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Pending Review') AND at_period > 0 THEN at_period ELSE 0 END),
                SUM(CASE WHEN spot_task = 1 AND at_period = 0 THEN rt ELSE 0 END),
                SUM(CASE WHEN revisions > 0 THEN rt ELSE 0 END)
            FROM `tabSprint Task`
            WHERE parent = %s AND cb = %s
        """, (sprint.name, cb))[0]

        (
            total_rt, tot_comp_rt, spr_comp_hrs, tot_work_rt, spr_wor_hrs, nt_rt,
            total_s_rt, tot_comp_srt, spot_comp_hrs, tot_work_srt, spot_wor_hrs, nt_srt,reopen_count
        ) = [x or 0 for x in result]

        completed_hrs = spr_comp_hrs + spot_comp_hrs
        ncompleted_hrs = spr_wor_hrs + spot_wor_hrs
        nc_rt = 0

        for st in sprint.sprint_task:
            if st.cb != cb:
                continue
            if frappe.db.exists('Energy Point And Non Conformity',
                {'task': st.task, 'docstatus': ['!=', 2], 'emp': emp}):
                nc_rt += st.rt or 0

        bt_hours = frappe.db.sql("""
            SELECT IFNULL(SUM(bt_difference), 0)
            FROM `tabAttendance`
            WHERE employee = %s AND docstatus != 2
            AND attendance_date BETWEEN %s AND %s
        """, (emp, sprint.from_date, end_date))[0][0]
        bt_hours = round(bt_hours or 0, 2)

        ts_hours = frappe.db.sql("""
            SELECT IFNULL(SUM(total_hours), 0)
            FROM `tabTimesheet`
            WHERE employee = %s AND docstatus != 2
            AND start_date BETWEEN %s AND %s
        """, (emp, sprint.from_date, end_date))[0][0]
        ts_hours = round(ts_hours or 0, 2)
        used_percent = (ts_hours / bt_hours) * 100 if ts_hours and bt_hours else 0
        comp_percent = (completed_hrs / ts_hours) * 100 if ts_hours and completed_hrs else 0
        ncomp_percent = (ncompleted_hrs / ts_hours) * 100 if ts_hours and ncompleted_hrs else 0
        tot_c += round(completed_hrs, 2)
        tot_nc += round(ncompleted_hrs, 2)
        tot_reopen_count += round(reopen_count, 2)
        tot_bt_hrs += ts_hours
        tot_spr_chrs += spr_comp_hrs
        tot_spr_whrs += spr_wor_hrs
        tot_spot_chrs += spot_comp_hrs
        tot_spot_whrs += spot_wor_hrs

        sub_total_rt += total_rt
        sub_tot_comp_rt += tot_comp_rt
        sub_tot_work_rt += tot_work_rt
        sub_nt_rt += nt_rt
        sub_total_s_rt += total_s_rt
        sub_tot_comp_srt += tot_comp_srt
        sub_tot_work_srt += tot_work_srt
        sub_nt_srt += nt_srt
        sub_bt_hours += bt_hours
        # sub_used_percent += used_percent
        sub_comp_per += comp_percent
        sub_ncomp_per += ncomp_percent
        tot_nc_rt += nc_rt

        spr_comp_s = f"{round(tot_comp_rt, 2)}/{round(spr_comp_hrs, 2)}"
        spr_ncomp_s = f"{round(tot_work_rt, 2)}/{round(spr_wor_hrs, 2)}"
        spot_comp_s = f"{round(tot_comp_srt, 2)}/{round(spot_comp_hrs, 2)}"
        spot_ncomp_s = f"{round(tot_work_srt, 2)}/{round(spot_wor_hrs, 2)}"

        used_percent_str = f"{ts_hours} ({round(used_percent, 2)}%)"
        comp_percent_str = f"{round(completed_hrs, 2)} ({round(comp_percent, 2)}%)"
        ncomp_percent_str = f"{round(ncompleted_hrs, 2)} ({round(ncomp_percent, 2)}%)"
        # if comp_percent < 70:
        font_color= "#f02e0c" if comp_percent < 70 else "#110404"
        att_color="#2059d4" if used_percent < 80 else "#110404"
        row_color = '#e8edea' if sr_no % 2 == 0 else '#ffffff'

        table += f"""
        <tr style="background-color: {row_color};color:#110404;">
            <td>{cb}</td>
            <td>{total_rt}</td>
            <td>{spr_comp_s}</td>
            <td>{spr_ncomp_s}</td>
            <td>{nt_rt}</td>
            <td>{total_s_rt}</td>
            <td>{spot_comp_s}</td>
            <td>{spot_ncomp_s}</td>
            <td>{nt_srt}</td>
            <td>{total_rt + total_s_rt}</td>
            <td>{bt_hours}</td>
            <td  style="color: {att_color};">{used_percent_str}</td>
            <td style="color: {font_color};">{comp_percent_str}</td>
            <td>{ncomp_percent_str}</td>
            <td>{round(nt_rt + nt_srt, 2)}</td>
            <td>{nc_rt}</td>
            <td>{round(reopen_count, 2)}</td>
        </tr>
        """

        sr_no += 1
    if sub_bt_hours > 0:
        sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
    else:
        sub_used_str=0
    if  tot_bt_hrs > 0:
        sub_comp_str=(tot_c/tot_bt_hrs)*100
    else:
        sub_comp_str=0
    if  tot_bt_hrs > 0:
        sub_work_str=(tot_nc/tot_bt_hrs)*100
    else:
        sub_work_str=0
    font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
    att_color="#2059d4" if sub_used_str < 80 else "#110404"
    sub_used_str = f"{round(tot_bt_hrs, 2)} ({round(sub_used_str, 2)})"
    sub_comp_str = f"{round(tot_c, 2)} ({round(sub_comp_str, 2)})"
    sub_work_str = f"{round(tot_nc, 2)} ({round(sub_work_str, 2)})"
    
    table += f"""
    <tr>
        <td style="background:#020c59;color:white;">Total(Hrs)</td>
        <td style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
        <td style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/{round(tot_spr_chrs, 2)}</td>
        <td style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/{round(tot_spr_whrs, 2)}</td>
        <td style="background:#d9edf7;color:#110404;">{sub_nt_rt}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_total_s_rt}</td>
        <td style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/{round(tot_spot_chrs, 2)}</td>
        <td style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/{round(tot_spot_whrs, 2)}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_nt_srt}</td>
        <td style="background:#f0b616;color:#110404;">{sub_total_rt + sub_total_s_rt}</td>
        <td style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
        <td style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
        <td style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
        <td style="background:#f0b616;color:#110404;">{sub_work_str}</td>
        <td style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
        <td style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
        <td style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
    </tr>
    <tr>
        <th colspan="17" style="background:#e8edea;">
            (in Count) <span style="color:#2059d4;">Used percent should be minimum of 80% </span> <span style="color:red;">Comp percent should be minimum of 70%</span>
        </th>
    </tr>

    """
    
    sub_total_count = sub_tot_comp_count =sub_tot_work_count =sub_nt_count =sub_total_s_count =0
    sub_tot_comp_scount = sub_tot_work_scount=sub_nt_scount=sub_total=overall_comp=0
    overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=0
    s_no=1
    for cb in cb_list:
        emp = frappe.db.get_value('Employee', {'short_code': cb}, 'name')
        user_id = frappe.db.get_value('Employee', {'short_code': cb}, 'user_id')

        counts = frappe.db.sql("""
            SELECT
                SUM(CASE WHEN st.spot_task = 0 THEN 1 ELSE 0 END) AS total_count,
                SUM(CASE WHEN st.spot_task = 0 AND st.cr_status NOT IN ('Open','Working','Pending Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_count,
                SUM(CASE WHEN st.spot_task = 0 AND st.cr_status IN ('Open','Working','Pending Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_count,
                SUM(CASE WHEN st.spot_task = 0 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_count,
                SUM(CASE WHEN st.spot_task = 1 THEN 1 ELSE 0 END) AS total_s_count,
                SUM(CASE WHEN st.spot_task = 1 AND st.cr_status NOT IN ('Open','Working','Pending Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_scount,
                SUM(CASE WHEN st.spot_task = 1 AND st.cr_status IN ('Open','Working','Pending Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_scount,
                SUM(CASE WHEN st.spot_task = 1 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_scount,
                SUM(CASE WHEN st.revisions > 0 THEN revisions ELSE 0 END) AS reopen_count
            FROM `tabSprint Task` st
            WHERE st.parent = %s AND st.cb = %s
        """, (sprint.name, cb), as_dict=1)[0]

        total_count = counts.total_count or 0
        tot_comp_count = counts.tot_comp_count or 0
        tot_work_count = counts.tot_work_count or 0
        nt_count = counts.nt_count or 0
        total_s_count = counts.total_s_count or 0
        tot_comp_scount = counts.tot_comp_scount or 0
        tot_work_scount = counts.tot_work_scount or 0
        nt_scount = counts.nt_scount or 0
        reopen_count=counts.reopen_count or 0
        # reopen_count = frappe.db.sql("""
        #     SELECT IFNULL(SUM(CAST(t.revisions AS UNSIGNED)), 0)
        #     FROM `tabSprint Task` st
        #     JOIN `tabTask` t ON t.name = st.rt
        #     WHERE st.parent = %s 
        #     AND st.cb = %s 
        #     AND t.custom_allocated_to = %s 
        #     AND IFNULL(t.revisions, 0) > 0
        # """, (sprint.name, cb, user_id))[0][0] or 0

        nc_count = frappe.db.sql("""
            SELECT SUM(e.nc_score)
            FROM `tabSprint Task` st
            JOIN `tabEnergy Point And Non Conformity` e
            ON e.task = st.task
            WHERE st.parent = %s
            AND st.cb = %s
            AND e.emp = %s
            AND e.docstatus != 2
        """, (sprint.name, cb, emp))[0][0] or 0

        # nc_count = frappe.db.sql("""
        #     SELECT COUNT(DISTINCT st.task)
        #     FROM `tabSprint Task` st
        #     WHERE st.parent = %s AND st.cb = %s
        #     AND EXISTS (
        #         SELECT 1 FROM `tabEnergy Point And Non Conformity` e
        #         WHERE e.task = st.task AND e.emp = %s AND e.docstatus != 2
        #     )
        # """, (sprint.name, cb, emp))[0][0] or 0

        color = '#e8edea' if s_no % 2 == 0 else '#ffffff'

        sub_total_count += total_count
        sub_tot_comp_count += tot_comp_count
        sub_tot_work_count += tot_work_count
        sub_nt_count += nt_count
        sub_total_s_count += total_s_count
        sub_tot_comp_scount += tot_comp_scount
        sub_tot_work_scount += tot_work_scount
        sub_nt_scount += nt_scount
        sub_total += total_count + total_s_count
        overall_comp += tot_comp_count + tot_comp_scount
        overall_work += tot_work_count + tot_work_scount
        overall_nt += nt_count + nt_scount
        sub_total_reopen_count += reopen_count
        tot_nc_count += nc_count

        table += f"""
        <tr style="background-color: {color};color:#110404;">
            <td>{cb}</td>
            <td>{total_count}</td>
            <td>{tot_comp_count}</td>
            <td>{tot_work_count}</td>
            <td>{nt_count}</td>
            <td>{total_s_count}</td>
            <td>{tot_comp_scount}</td>
            <td>{tot_work_scount}</td>
            <td>{nt_scount}</td>
            <td>{total_count + total_s_count}</td>
            <td>-</td>
            <td>-</td>
            <td>{tot_comp_count + tot_comp_scount}</td>
            <td>{tot_work_count + tot_work_scount}</td>
            <td>{nt_count + nt_scount}</td>
            <td>{nc_count}</td>
            <td>{reopen_count}</td>
        </tr>
        """
        s_no += 1

    table += f"""
    <tr>
        <td style="background:#020c59;color:white;">Total(Count)</td>
        <td style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
        <td style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
        <td style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
        <td style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
        <td style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
        <td style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
        <td style="background:#f0b616;color:#110404;">-</td>
        <td style="background:#f0b616;color:#110404;">-</td>
        <td style="background:#f0b616;color:#110404;">{overall_comp}</td>
        <td style="background:#f0b616;color:#110404;">{overall_work}</td>
        <td style="background:#f0b616;color:#110404;">{overall_nt}</td>
        <td style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
        <td style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
    </tr>
    """
    table += """
        </tbody></table>
    """

    return table



@frappe.whitelist()
def update_tasks_sprint(sprint):
    sprint_doc = frappe.get_doc("Sprint", sprint)

    if not sprint_doc.sprint_task:
        return "No tasks found"

    for row in sprint_doc.sprint_task:
        if row.task:
            frappe.db.set_value("Task", row.task, "custom_sprint", sprint_doc.sprint_id)

    return "Updated"


@frappe.whitelist()
def empty_sprint(sprint):

    sprint_doc = frappe.get_doc("Sprint", sprint)

    # Allocated tasks from sprint child table
    allocated_tasks = [row.task for row in sprint_doc.sprint_task if row.task]

    # All valid team tasks except Cancelled/Hold
    task_list = frappe.get_all(
        "Task",
        filters={
            "custom_dev_team": sprint_doc.team,
            "status": ["not in", ["Cancelled", "Hold"]]
        },
        fields=["name", "status", "custom_sprint"]
    )

    for task in task_list:

        if (
            task.name not in allocated_tasks
            and task.status in ["Open", "Working"]
        ):
            frappe.db.set_value(
                "Task",
                task.name,
                "custom_sprint",
                ""
            )

    frappe.db.commit()

    return "Updated"



from frappe.utils import getdate
@frappe.whitelist()
def update_task_sprint(task_id, production_date):

    production_date = getdate(production_date)

    sprint = frappe.get_all(
        "Sprint",
        filters={
            "from_date": ["<=", production_date],
            "to_date": [">=", production_date]
        },
        fields=["sprint_id"],
        limit=1
    )

    if sprint:
        frappe.db.set_value("Task", task_id, "custom_sprint", sprint[0].sprint_id)

    return "Sprint Updated"

