# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RECWeekPlan(Document):
	# pass
    def validate(self):
        processed_projects = set()
        indexes_to_remove = []

        for alloc_row in self.allocation:
            project = alloc_row.project
            if project and project not in processed_projects:
                for i, detail_row in enumerate(self.project_details):
                    if detail_row.project == project:
                        # Add to details only once
                        self.append("details", {
                            "project": project
                        })
                        indexes_to_remove.append(i)
                        processed_projects.add(project)
                        break

        # Remove matched project_details rows
        for i in sorted(indexes_to_remove, reverse=True):
            self.project_details.pop(i)

        # Reset row numbers (idx) for details and project_details
        for i, row in enumerate(self.details, start=1):
            row.idx = i
        for i, row in enumerate(self.project_details, start=1):
            row.idx = i
    #     self.update_task_allocation_totals()
    # def update_task_allocation_totals(self):
    #     task_exe_totals = {}
    #     for row in self.allocation:
    #         key = (row.task, row.exe)
    #         task_exe_totals[key] = task_exe_totals.get(key, 0) + (row.ac or 0)
    #     for row in self.task_allocation:
    #         key = (row.task, row.exe)
    #         if key in task_exe_totals:
    #             row.ac = task_exe_totals[key]


@frappe.whitelist()
def get_teampro_holidays(start_date, end_date):
    return frappe.get_all("Holiday", 
        filters={
            "parent": "TEAMPRO 2023",
            "holiday_date": ["between", [start_date, end_date]]
        },
        fields=["holiday_date"]
    )

@frappe.whitelist()
def update_week_plan_ac_by_today(candidate):
    from frappe.utils import today, getdate

    today_date = getdate(today())

    # Find REC Week Plan with today's date in range
    week_plan = frappe.db.get_value("REC Week Plan", {
        "start_date": ["<=", today_date],
        "end_date": [">=", today_date]
    }, "name")

    if week_plan:
        return update_allocation_actual_count(week_plan)


@frappe.whitelist()
def update_allocation_actual_count(docname):
    doc = frappe.get_doc("REC Week Plan", docname)

    for row in doc.allocation:  # Replace 'allocation' with your actual child table fieldname
        task = row.task
        exe = row.exe
        date = row.date

        if task and exe and date:
            count = frappe.db.sql("""
                SELECT COUNT(DISTINCT c.name) AS status_count
                FROM `tabCandidate` c
                INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                WHERE DATE(cs.sourced_date) = %s
                AND cs.sourced_by = %s
                AND c.candidate_created_by = %s
                AND cs.task = %s
                AND cs.status IN (%s, %s)
            """, (date, exe, exe, task, "Submitted(Client)", "Submit(SPOC)"))

            row.ac = count[0][0] if count else 0

    doc.save()
    frappe.db.commit()
    return "AC updated successfully"

from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days
import frappe

@frappe.whitelist()
def update_rec_dpr(name):
    today = nowdate()
    date_obj = datetime.strptime(today, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')

    emp = frappe.db.get_all("Employee", {
        'status': 'Active',
        'reports_to': 'TI00003',
        'user_id': ('not in', ['keerthana.k@groupteampro.com'])
    }, ['user_id'])

    recievers = [i.user_id for i in emp]
    recievers.append('sangeetha.a@groupteampro.com')

    parent_doc = frappe.get_doc("REC Week Plan", name)
    count = 1
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '''
    <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
        <td style='width:5%'><b>SI NO</b></td>
        <td style='width:10%'><b>ID</b></td>
        <td style='width:15%'><b>Project</b></td>
        <td style='width:20%'><b>Subject</b></td>
        <td style='width:13%'><b>Allocated To</b></td>
        <td style='width:13%'><b>RC</b></td>
    </b></tr>
    '''

    task_group = {}

    for i in parent_doc.allocation:
        if str(i.date) == today:  # Only today's records
            data += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right">{}</td></tr>'.format(
                count, i.task, i.project or '-', i.subject, i.exe, i.rc or '-'
            )
            count += 1

            if i.exe not in task_group:
                task_group[i.exe] = []
            task_group[i.exe].append(i)

    data += '</table>'

    # Send summary mail to team
    frappe.sendmail(
        sender='sangeetha.a@groupteampro.com',
        # recipients=recievers,
        recipients='divya.p@groupteampro.com',
        subject=f'REC-DPR {formatted_date} - Reg',
        message=f"""
            <b>Dear Team,</b><br><br>
            Please find the below DPR for {formatted_date} for your kind reference and action.<br><br>
            {data}<br><br>
            Thanks & Regards,<br>TEAM ERP<br>
            <i>This email has been automatically generated. Please do not reply</i>
        """
    )

    # Send individual mail to each employee with their tasks
    for allocated_to, tasks in task_group.items():
        task_data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        task_data += '''
        <tr style="background-color: #0f1568; text-align:center; color:white;">
            <td style='width:5%'><b>SI NO</b></td>
            <td style='width:10%'><b>ID</b></td>
            <td style='width:15%'><b>Project</b></td>
            <td style='width:20%'><b>Subject</b></td>
            <td style='width:13%'><b>RC</b></td>
        </tr>
        '''
        individual_count = 1
        for j in tasks:
            task_data += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                individual_count, j.task, j.project or '-', j.subject, j.rc or '-'
            )
            individual_count += 1
        task_data += '</table>'

        # if allocated_to:
        #     frappe.sendmail(
        #         sender='sangeetha.a@groupteampro.com',
        #         recipients=allocated_to,
        #         subject=f'Task DPR {formatted_date} - Reg',
        #         message=f"""
        #             <b>Dear Team</b>,<br><br>
        #             Please find your assigned task for {formatted_date}.<br><br>
        #             {task_data}<br><br>
        #             Thanks & Regards,<br>TEAM ERP<br>
        #             <i>This email has been automatically generated. Please do not reply</i>
        #         """
        #     )

    frappe.msgprint("DPR mail has been successfully sent")


# @frappe.whitelist()
# def update_rec_dpr_html(name):
#     today = nowdate()
#     parent_doc = frappe.get_doc("REC Week Plan", name)

#     data = '<table border="1" width="100%" style="border-collapse: collapse;">'
#     data += '''
#     <tr style="background-color: #0f1568 ;text-align:center;color: white;">
#         <td style='width:5%'><b>SI NO</b></td>
#         <td style='width:10%'><b>ID</b></td>
#         <td style='width:15%'><b>Project</b></td>
#         <td style='width:20%'><b>Subject</b></td>
#         <td style='width:13%'><b>Allocated To</b></td>
#         <td style='width:13%'><b>RC</b></td>
#     </tr>
#     '''
#     count = 1
#     for i in parent_doc.allocation:
#         if str(i.date) == today:
#             data += f'''
#             <tr>
#                 <td>{count}</td>
#                 <td>{i.task}</td>
#                 <td>{i.project or "-"}</td>
#                 <td>{i.subject}</td>
#                 <td>{i.exe}</td>
#                 <td>{i.rc or "-"}</td>
#             </tr>
#             '''
#             count += 1
#     data += '</table>'
#     return data

@frappe.whitelist()
def get_dpr_collapsible_html(name, start_date=None, end_date=None):
    import frappe
    from frappe.utils import getdate
    parent_doc = frappe.get_doc("REC Week Plan", name)

    # Parse the dates
    start_date = getdate(start_date)
    end_date = getdate(end_date)

    exe_tasks = {}
    for row in parent_doc.allocation:
        row_date = getdate(row.date)
        if start_date <= row_date <= end_date:
            exe_tasks.setdefault(row.exe, []).append({
                "task": row.task,
                "subject":row.subject,
                "rc": row.rc or 0
            })

    return exe_tasks

@frappe.whitelist()
def get_dsr_collapsible_html(name, start_date=None, end_date=None):
    import frappe
    from frappe.utils import getdate

    parent_doc = frappe.get_doc("REC Week Plan", name)

    # Parse the dates
    start_date = getdate(start_date)
    end_date = getdate(end_date)

    exe_tasks = {}

    # Step 1: Add Allocation data
    for row in parent_doc.allocation:
        row_date = getdate(row.date)
        if start_date <= row_date <= end_date:
            exe_tasks.setdefault(row.exe, []).append({
                "task": row.task,
                "subject": row.subject,
                "rc": row.rc or 0,
                "from": "Allocation"
            })

    # Step 2: Add DSR data
    for row in parent_doc.dsr:
        row_date = getdate(row.date)
        if start_date <= row_date <= end_date:
            exe_tasks.setdefault(row.exe, []).append({
                "task": row.task,
                "subject": "",  # You can fetch subject if needed
                "rc": row.ac or 0,
                "from": "DSR"
            })

    return exe_tasks


# @frappe.whitelist()
# def update_dsr_data(name, date):
#     doc = frappe.get_doc("REC Week Plan", name)
#     task_ids = set()

#     # Update AC for existing allocation rows
#     for row in doc.allocation:
#         candidate_count = frappe.db.sql("""
#             SELECT COUNT(DISTINCT c.name)
#             FROM `tabCandidate` c
#             INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
#             WHERE DATE(cs.sourced_date) = %s
#               AND cs.sourced_by = %s
#               AND c.candidate_created_by = %s
#               AND cs.task = %s
#               AND cs.status IN (%s, %s)
#         """, (date, row.exe, row.exe, row.task, "Submitted(Client)", "Submit(SPOC)"))

#         row.ac = candidate_count[0][0] if candidate_count else 0
#         task_ids.add((row.task, row.exe))

#     # Check for additional task submissions not in allocation
#     candidate_tasks = frappe.db.sql("""
#         SELECT cs.task, c.candidate_created_by
#         FROM `tabCandidate` c
#         INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
#         WHERE DATE(cs.sourced_date) = %s
#           AND cs.status IN (%s, %s)
#     """, (date, "Submitted(Client)", "Submit(SPOC)"))

#     for task_id, owner in candidate_tasks:
#         if (task_id, owner) not in task_ids:
#             add_count = frappe.db.sql("""
#                 SELECT COUNT(DISTINCT c.name)
#                 FROM `tabCandidate` c
#                 INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
#                 WHERE DATE(cs.sourced_date) = %s
#                   AND cs.sourced_by = %s
#                   AND c.candidate_created_by = %s
#                   AND cs.task = %s
#                   AND cs.status IN (%s, %s)
#             """, (date, owner, owner, task_id, "Submitted(Client)", "Submit(SPOC)"))

#             count = add_count[0][0] if add_count else 0
#             if count > 0:
#                 doc.append("dsr", {
#                     "task": task_id,
#                     "exe": owner,
#                     "ac": count,
#                     "date":today()
#                 })
#                 task_ids.add((task_id, owner))

#     doc.save()

@frappe.whitelist()
def update_dsr_data(name, date):
    from frappe.utils import today

    doc = frappe.get_doc("REC Week Plan", name)
    task_ids = set()

    # Step 1: Update AC for existing allocation rows
    for row in doc.allocation:
        candidate_count = frappe.db.sql("""
            SELECT COUNT(DISTINCT c.name)
            FROM `tabCandidate` c
            INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
            WHERE DATE(cs.sourced_date) = %s
              AND cs.sourced_by = %s
              AND c.candidate_created_by = %s
              AND cs.task = %s
              AND cs.status IN (%s, %s)
        """, (date, row.exe, row.exe, row.task, "Submitted(Client)", "Submit(SPOC)"))

        row.ac = candidate_count[0][0] if candidate_count else 0
        task_ids.add((row.task, row.exe))

    # Step 2: Check for additional task submissions not in allocation
    candidate_tasks = frappe.db.sql("""
        SELECT cs.task, c.candidate_created_by
        FROM `tabCandidate` c
        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE DATE(cs.sourced_date) = %s
          AND cs.status IN (%s, %s)
    """, (date, "Submitted(Client)", "Submit(SPOC)"))

    for task_id, owner in candidate_tasks:
        if (task_id, owner) not in task_ids:
            add_count = frappe.db.sql("""
                SELECT COUNT(DISTINCT c.name)
                FROM `tabCandidate` c
                INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                WHERE DATE(cs.sourced_date) = %s
                  AND cs.sourced_by = %s
                  AND c.candidate_created_by = %s
                  AND cs.task = %s
                  AND cs.status IN (%s, %s)
            """, (date, owner, owner, task_id, "Submitted(Client)", "Submit(SPOC)"))

            count = add_count[0][0] if add_count else 0
            if count > 0:
                # Check if entry already exists in DSR
                existing_row = next(
                    (d for d in doc.dsr if d.task == task_id and d.exe == owner),
                    None
                )
                if existing_row:
                    existing_row.ac = count  # Update count if exists
                else:
                    doc.append("dsr", {
                        "task": task_id,
                        "exe": owner,
                        "ac": count,
                        "date": today()
                    })
                task_ids.add((task_id, owner))

    doc.save()
