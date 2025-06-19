import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days

@frappe.whitelist()
def get_allocated_tasks_for_it_dev(date,name,service,type,dev_team,sprint):
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details=[]
    parent_doc.dm_summary=[]
    if type == "OPS":
        task_id=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type,"custom_dev_team":dev_team,"custom_sprint":sprint},['*'],order_by='cb asc, project asc, priority asc')
        task_det=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type,"custom_dev_team":dev_team,"custom_sprint":sprint},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
        for i in task_id:
            parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":i.cb})
            frappe.db.set_value("Task",i.name,"allocated",1)
        for k in task_det:
            actual_aph=frappe.db.get_value('Employee',{'short_code':k.cb},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' and custom_dev_team=%s and custom_sprint=%s group by custom_allocated_to""",(k.custom_allocated_to,date,dev_team,sprint), as_dict=True)
            allocated_count=frappe.db.count("Task",{"custom_allocated_to":k.custom_allocated_to,"custom_production_date":date,"type":"OPS","status":"Working","allocated":1})
            emp_cb=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['short_code'])
            if sum_et[0].et:
                if actual_aph is not None:
                    percent=(float(sum_et[0].et)/float(actual_aph))*100
                    parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph or '8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0','allocated':allocated_count})
                else:
                    percent=(float(sum_et[0].et)/8)*100
                    parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':'8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0','allocated':allocated_count})
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")

from collections import defaultdict   
@frappe.whitelist()
def dpr_task_mail_it_dev(date,name,service,type,dev_team,sprint):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]
    if type=="OPS":
        emp=frappe.db.get_all("Employee",{'status':'Active','custom_dev_team':dev_team},['*'])
        recievers.append('abdulla.pi@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    tl_email=frappe.db.get_value("Employee",{"custom_is_tl":1,"custom_dev_team":dev_team},["user_id"])
    task = frappe.db.get_all("Task", {"custom_production_date":date,"type":type,"service":service,"custom_dev_team":dev_team,"custom_sprint":sprint}, ['*'], order_by='cb asc',group_by='custom_allocated_to asc')
    if task_data.dsr_check==1:
        if type =="OPS":
            count=1
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
                <td style='width:5%'><b>SI NO</b></td>
                <td style='width:5%'><b>Task ID</b></td>
                <td style='width:15%'><b>Project Name</b></td>
                <td style='width:20%'><b>Subject</b></td>
                <td style='width:5%'><b>CB</b></td>
                <td style='width:10%'><b>Status</b></td>
                <td style='width:5%'><b>ET</b></td>
                <td style='width:5%'><b>RT</b></td>
                <td style='width:5%'><b>AT Total</b></td>
                <td style='width:5%'><b>AT Period</b></td>
                <td style='width:7%'><b>Priority</b></td>
                <td style='width:20%'><b>Working Remarks</b></td>
                <td style='width:15%'><b>ET Vs AT Remarks</b></td>
            </b></tr>
            '''
            sorted_tasks = sorted(
                    task_data.task_details,
                    key=lambda x: (x.cb or '', x.project_name or '', x.priority or '')
                )

            count = 1
            for i in sorted_tasks:
                at = round(float(i.at or 0), 2)
                at_taken = round(float(i.at_taken or 0), 2)
                data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td><td style="text-align:left">%s</td><td style="text-align:left">%s</td>' % (
                    count, i.id or '', i.project_name or '', i.subject, i.cb, i.current_status, i.et, i.rt, at, at_taken, i.priority,i.remark or '',i.et_vs_at_remark or ''
                )
                count += 1

            data += '</table>'

            # for i in task_data.task_details:
            #     at = round(float(i.at or 0), 2)
            #     at_taken = round(float(i.at_taken or 0), 2)
            #     data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td>'%(count,i.id or '',i.project_name or '',i.subject,i.cb,i.current_status,i.et,i.rt,at,at_taken,i.priority)
            #     count+=1
            # data += '</table>'
            # aph = 8  
            cb_summary = defaultdict(lambda: {'rt': 0,'at_taken':0})
            grand_total_rt = 0
            grand_total_aph = 0
            grand_total_at=0
            for i in task_data.task_details:
                cb = i.cb or "Not Set"
                cb_summary[cb]['rt'] += i.rt or 0
                cb_summary[cb]['at_taken'] += float(i.at_taken or 0)
            summary = '''
            <table border="1" width="40%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td><b>CB</b></td>
                    <td><b>APH</b></td>
                    <td><b>RT</b></td>
                    <td><b>AT</b></td>
                    <td><b>RT Vs APH%</b></td>
                </tr>
            '''
            for cb, data_cb in cb_summary.items():
                aph = 5  if(frappe.db.get_value("Employee",{'short_code':cb},['custom_is_tl'])) else 6
                rt = data_cb['rt']
                at=data_cb['at_taken']
                grand_total_aph += aph
                grand_total_rt += data_cb['rt']
                grand_total_at+=data_cb['at_taken']
                rt_vs_aph = round((rt / aph) * 100, 2) if aph else 0
                summary += f'''
                <tr style="text-align:center;font-size: 12px;">
                    <td>{cb}</td>
                    <td>{aph}</td>
                    <td>{round(rt,2)}</td>
                    <td>{round(at,2)}</td>
                    <td>{rt_vs_aph}</td>
                </tr>
                '''
            grand_rt_vs_aph = round((grand_total_rt / grand_total_aph) * 100, 2) if grand_total_aph else 0
            grand_total_at_rounded = round(grand_total_at, 2)
            # summary += f'''
            # <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
            #     <td>Grand Total</td>
            #     <td>{grand_total_aph}</td>
            #     <td>{grand_total_rt}</td>
            #     <td>{grand_total_at}</td>
            #     <td>{grand_rt_vs_aph}</td>
            # </tr>
            # '''
            summary += f'''
            <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
                <td>Grand Total</td>
                <td>{grand_total_aph}</td>
                <td>{round(grand_total_rt,2)}</td>
                <td>{grand_total_at_rounded}</td>
                <td>{grand_rt_vs_aph}</td>
            </tr>
            '''
            summary += '</table>'
            frappe.sendmail(
                    sender=tl_email,
                    recipients=recievers,
                    cc='abdulla.pi@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    subject = f'{service} - {dev_team} DSR {formatted_date} -Reg',
                    message = """
                <b>Dear Team,</b><br><br>
                    Please find the below DSR for {} for your kind reference.<br><br>
                    {}<br>
                    {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,summary,data)
                )
            frappe.msgprint("DSR mail has been successfully sent.")
            task_data.dm_status='Submitted'
            task_data.dsr_submitted_on=today()
            task_data.workflow_state='Submitted'
            task_data.save()
            frappe.db.commit()
    else:
        count=1
        if type=="OPS":
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
                <td style='width:5%'><b>SI NO</b></td>
                <td style='width:5%'><b>Task ID</b></td>
                <td style='width:15%'><b>Project Name</b></td>
                <td style='width:20%'><b>Subject</b></td>
                <td style='width:5%'><b>CB</b></td>
                <td style='width:10%'><b>Status</b></td>
                <td style='width:5%'><b>ET</b></td>
                <td style='width:5%'><b>RT</b></td>
                <td style='width:7%'><b>Priority</b></td>
            </b></tr>
            '''
            sorted_tasks = sorted(
                task_data.task_details,
                key=lambda x: (x.cb or '', x.project_name or '', x.priority or '')
            )

            count = 1
            for i in sorted_tasks:
                data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td>' % (
                    count, i.id, i.project_name or '', i.subject, i.cb, i.status, i.et, i.rt, i.priority
                )
                count += 1

            data += '</table>'

            # for i in task_data.task_details:
            #     data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td>'%(count,i.id,i.project_name or '',i.subject,i.cb,i.status,i.et,i.rt,i.priority)
            #     count+=1
            # data += '</table>'
            # aph = 8  # fixed APH value
            cb_summary = defaultdict(lambda: {'rt': 0})
            grand_total_rt = 0
            grand_total_aph = 0
            # Group RT by CB
            for i in task_data.task_details:
                cb = i.cb or "Not Set"
                cb_summary[cb]['rt'] += i.rt or 0


            # Generate summary HTML table
            summary = '''
            <table border="1" width="40%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td><b>CB</b></td>
                    <td><b>APH</b></td>
                    <td><b>RT</b></td>
                    <td><b>RT Vs APH%</b></td>
                </tr>
            '''
            for cb, data_cb in cb_summary.items():
                aph = 5  if(frappe.db.get_value("Employee",{'short_code':cb},['custom_is_tl'])) else 6
                rt = data_cb['rt']
                grand_total_aph += aph
                grand_total_rt += data_cb['rt']
                rt_vs_aph = round((rt / aph) * 100, 2) if aph else 0
                summary += f'''
                <tr style="text-align:center;font-size: 12px;">
                    <td>{cb}</td>
                    <td>{aph}</td>
                    <td>{rt}</td>
                    <td>{rt_vs_aph}</td>
                </tr>
                '''
            grand_rt_vs_aph = round((grand_total_rt / grand_total_aph) * 100, 2) if grand_total_aph else 0
            summary += f'''
            <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
                <td>Grand Total</td>
                <td>{grand_total_aph}</td>
                <td>{round(grand_total_rt,2)}</td>
                <td>{grand_rt_vs_aph}%</td>
            </tr>
            '''
            summary += '</table>'
            frappe.sendmail(
                    sender=tl_email,
                    recipients=recievers,
                    # recipients='divya.p@groupteampro.com',
                    subject = f'{service} - {dev_team} DPR {formatted_date} -Reg',
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DPR for {} for your kind reference and action, ensure all the Tasks allocated on time and as per the requirement, for each Revision and AT going beyond 150% there will be NC applied and accumulated NC will be reviewed every week and directly affects your Performance.<br><br>
                {}<br>
                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,summary,data)
                )
            frappe.msgprint("DPR mail has been successfully sent")
            task_data.dm_status='DPR Completed'
            task_data.dpr_submitted_on=today()
            task_data.save()
            frappe.db.commit()

@frappe.whitelist()
def send_sprint_panned_mail(name,sprint_id,team):
    sprint_doc = frappe.get_doc("Sprint", name)
    current_sprint_start = sprint_doc.from_date
    previous_sprint_name = frappe.db.get_value("Sprint",{"team": team,"from_date": ["<", current_sprint_start]},"name")
    recievers=[]
    if sprint_doc and previous_sprint_name:
        emp=frappe.db.get_all("Employee",{'status':'Active',"custom_dev_team":sprint_doc.team},['*'])
        for n in emp:
            recievers.append(n.user_id)
        recievers.append('dineshbabu.k@groupteampro.com')
        recievers.append('abdulla.pi@groupteampro.com')
        tl_email=frappe.db.get_value("Employee",{"custom_is_tl":1,"custom_dev_team":sprint_doc.team},["user_id"])
        retro_sprint=frappe.get_doc("Sprint", previous_sprint_name)
        retro_sprint = frappe.get_doc("Sprint", previous_sprint_name)
        formatted_date = retro_sprint.from_date.strftime('%d/%m/%Y')
        formatted_date_to = retro_sprint.to_date.strftime('%d/%m/%Y')

        s_no=1
        data = '''
            <table border="1" width="50%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td><b>CB</b></td>
                    <td><b>Timesheet Hour (TH)</b></td>
                    <td><b>Biometric Hour (BH)</b></td>
                    <td><b>Average TH/Day</b></td>
                    <td><b>TH vs BH Wastage Hour/Day</b></td>
                </tr>
            '''
        retro = '''
            <table border="1" width="50%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td><b>What Went Well</b></td>
                    <td><b>What Went Wrong</b></td>
                    <td><b>Points to Improve</b></td>
                    <td><b>Kudos</b></td>
                </tr>
            '''
        table = '''
            <table border="1" width="100%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td><b>Sr</b></td>
                    <td><b>ID</b></td>
                    <td><b>Project Name</b></td>
                    <td><b>Subject</b></td>
                    <td><b>CB</b></td>
                    <td><b>Status</b></td>
                    <td><b>AT</b></td>
                    <td><b>ET</b></td>
                    <td><b>RT</b></td>
                    <td><b>Priority</b></td>
                    <td><b>KT Confirmed</b></td>
                </tr>
            '''
        if sprint_doc.sprint_task:
            for s in sprint_doc.sprint_task:
                table += f'''
                    <tr style="font-size: 12px;">
                        <td style="text-align:left;">{s_no}</td>
                        <td style="text-align:left;">{s.task}</td>
                        <td style="text-align:left;">{s.project}</td>
                        <td style="text-align:left;">{s.subject}</td>
                        <td style="text-align:left;">{s.cb}</td>
                        <td style="text-align:left;">{s.status}</td>
                        <tdstyle="text-align:right;">{s.at}</td>
                        <td style="text-align:right;">{s.et}</td>
                        <td style="text-align:right;">{s.rt}</td>
                        <td style="text-align:left;">{s.priority}</td>
                        <td style="text-align:right;">{s.kt_confirmed}</td>
                    </tr>
                    '''
                s_no+=1
            table += '</table>'
        if retro_sprint:
            if retro_sprint.sprint_avl_time:
                for i in retro_sprint.sprint_avl_time:
                    emp_id=frappe.db.get_value("Employee",{"short_code":i.short_code,"status":"Active"},["name"])
                    timesheet_hrs = frappe.db.sql("""
                    SELECT SUM(total_hours) AS total_hours 
                    FROM `tabTimesheet`
                    WHERE employee=%s AND start_date BETWEEN %s AND %s
                """, (emp_id, retro_sprint.from_date, retro_sprint.to_date), as_dict=True)
                    

                    total_hours = timesheet_hrs[0].total_hours if timesheet_hrs and timesheet_hrs[0].total_hours else 0
                    present = frappe.db.sql("""
                        SELECT SUM(
                            CASE 
                                WHEN status = 'Present' THEN 1
                                WHEN status = 'Half Day' THEN 0.5
                                ELSE 0
                            END
                        ) AS count
                        FROM `tabAttendance`
                        WHERE attendance_date BETWEEN %s AND %s AND employee=%s
                    """, (retro_sprint.from_date, retro_sprint.to_date, emp_id), as_dict=True)
                    present_days = present[0].count if present and present[0].count else 0

                    # Calculate average
                    avg_th_per_day = total_hours / present_days if present_days else 0
                    wastage=(i.bh-total_hours)/present_days if present_days else 0
                    frappe.errprint(wastage)
                    data += f'''
                    <tr style="font-size: 12px;">
                        <td style="text-align:left;">{i.short_code}</td>
                        <td style="text-align:right;">{total_hours:.2f}</td>
                        <td style="text-align:right;">{i.bh:.2f}</td>
                        <td style="text-align:right;">{avg_th_per_day:.2f}</td>
                        <td style="text-align:right;">{wastage:.2f}</td>
                    </tr>
                    '''
                data += '</table>'
            if retro_sprint.retro:
                for j in retro_sprint.retro:
                    retro += f'''
                    <tr style="font-size: 12px;">
                        <td style="text-align:left;">{j.what_went_well}</td>
                        <td style="text-align:left;">{j.what_went_wrong}</td>
                        <td style="text-align:left;">{j.points_to_improve}</td>
                        <td style="text-align:left;">{j.kudos}</td>
                    </tr>
                    '''
            else:
                retro += f'''
                    <tr style="text-align:center;font-size: 12px;">
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    '''

                retro += '</table>'
        frappe.sendmail(
                    sender=tl_email,
                    # recipients=recievers,
                    recipients=['divya.p@groupteampro.com','jenisha.p@groupteampro.com'],
                    subject = f'SPM - {team} - {formatted_date}-{formatted_date_to} -{sprint_doc.sprint_id}',
                    message = """
                    <b>Dear Team,</b><br><br>
                    {} Retro <br><br>
                    Timesheet vs Biometric Hour utility Summary
                {}<br>
                RETRO
                {}<br><br>
                {} Plan<br>
                Total Available Hours{}<br>
                Total Allocated Hours{}<br><br>
                {}

                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(retro_sprint.sprint_id,data,retro,sprint_id,sprint_doc.sprint_hours,sprint_doc.allocated_hours,table)
                )

        

# @frappe.whitelist()
# def update_allocated_task_at_dev(date, name, service, type, dev_team, sprint):
#     parent_doc = frappe.get_doc("Daily Monitor", name)
#     existing_task_ids = {d.id: d for d in parent_doc.task_details}
    
#     issues = []
#     meetings = []
#     tasks = []

#     if type == "OPS":
#         appended_issues = set()
#         appended_meetings = set()
#         appended_tasks = set()

#         employee_list = frappe.get_all("Employee", {
#             'department': "IT. Development - THIS",
#             'custom_dept_type': 'OPS',
#             "custom_dev_team": dev_team
#         }, ['short_code', 'name'])

#         for emp in employee_list:
#             timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee': emp.name}, ['name'])
#             task_hours_total = 0.0

#             if timesheet:
#                 # === Issues ===
#                 issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_issue': ['!=', '']}, fields=['*'])
#                 for issue in issue_logs:
#                     if issue.custom_issue in appended_issues:
#                         continue

#                     short_code = emp.short_code
#                     priority = frappe.db.get_value("Issue", issue.custom_issue, "priority")
#                     status = frappe.db.get_value("Issue", issue.custom_issue, "status")
#                     sum_issue = frappe.db.sql("""
#                         SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
#                         INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
#                         WHERE cs.custom_issue=%s AND c.employee=%s AND c.start_date=%s
#                     """, (issue.custom_issue, emp.name, date), as_dict=True)[0].total or 0.0

#                     data = {
#                         "id": issue.custom_issue,
#                         "at_taken": sum_issue,
#                         'project_name': issue.project_name,
#                         'subject': issue.custom_subject_issue,
#                         'status': status,
#                         'cb': short_code,
#                         'priority': priority
#                     }

#                     if issue.custom_issue in existing_task_ids:
#                         # Update existing row
#                         row = existing_task_ids[issue.custom_issue]
#                         for k, v in data.items():
#                             row.set(k, v)
#                     else:
#                         issues.append(data)

#                     appended_issues.add(issue.custom_issue)

#                 # === Meetings ===
#                 meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_meeting': ['!=', '']}, fields=['*'])
#                 for meeting in meeting_logs:
#                     if meeting.custom_meeting in appended_meetings:
#                         continue

#                     status = frappe.db.get_value("Meeting", meeting.custom_meeting, "status")
#                     short_code = emp.short_code
#                     sum_meeting = frappe.db.sql("""
#                         SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
#                         INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
#                         WHERE cs.custom_meeting=%s AND c.employee=%s AND c.start_date=%s
#                     """, (meeting.custom_meeting, emp.name, date), as_dict=True)[0].total or 0.0

#                     data = {
#                         "id": meeting.custom_meeting,
#                         "at_taken": sum_meeting,
#                         'subject': meeting.custom_subject_meeting,
#                         'cb': short_code,
#                         'status': status
#                     }

#                     if meeting.custom_meeting in existing_task_ids:
#                         row = existing_task_ids[meeting.custom_meeting]
#                         for k, v in data.items():
#                             row.set(k, v)
#                     else:
#                         meetings.append(data)

#                     appended_meetings.add(meeting.custom_meeting)

#                 # === Tasks ===
#                 task_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'task': ['!=', '']}, fields=['*'])
#                 for log in task_logs:
#                     if log.task in appended_tasks:
#                         continue

#                     status = frappe.db.get_value("Task", log.task, "status")
#                     short_code = emp.short_code
#                     sum_task = frappe.db.sql("""
#                         SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
#                         INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
#                         WHERE cs.task=%s AND c.employee=%s AND c.start_date=%s
#                     """, (log.task, emp.name, date), as_dict=True)[0].total or 0.0

#                     data = {
#                         "id": log.task,
#                         "at_taken": sum_task,
#                         "cb": short_code,
#                         "current_status": status
#                     }

#                     if log.task in existing_task_ids:
#                         row = existing_task_ids[log.task]
#                         for k, v in data.items():
#                             row.set(k, v)
#                     else:
#                         tasks.append(data)

#                     appended_tasks.add(log.task)

#         # Append new items only
#         for d in issues:
#             parent_doc.append("task_details", d)
#         for m in meetings:
#             parent_doc.append("task_details", m)
#         for t in tasks:
#             parent_doc.append("task_details", t)

#         parent_doc.dsr_check = 1

#     parent_doc.dm_status = 'DSR Pending'
#     parent_doc.save()
#     frappe.db.commit()
#     if sprint:
#         sprint_doc = frappe.get_doc("Sprint", {"sprint_id":sprint,"team":dev_team})
#         sprint_task_ids = {d.task for d in sprint_doc.sprint_task}
#         dm_task_ids = {d.id for d in parent_doc.task_details if d.id}
#         new_tasks_to_add = dm_task_ids - sprint_task_ids
#         for task_id in new_tasks_to_add:
#             project = frappe.db.get_value("Task", task_id, "project")
#             emp_id=frappe.db.get_value("Task", task_id, "custom_allocated_to")
#             short_code=frappe.db.get_value("Employee", {"user_id":emp_id}, "short_code")
#             sprint_doc.append("sprint_task", {
#                 "task": task_id,
#                 "project":project,
#                 "cb":short_code
#             })
#         for i in sprint_doc.sprint_task:
#             emp_id = frappe.db.get_value("Task", i.task, "custom_allocated_to")
#             task_status=frappe.db.get_value("Task",i.task,"status")
#             emp_name = frappe.db.get_value("Employee", {"user_id": emp_id}, "name") if emp_id else None

#             total_hours = 0
#             total_period = 0

#             if emp_name:
#                 sum_task = frappe.db.sql("""
#                     SELECT SUM(cs.hours) AS total_hours 
#                     FROM `tabTimesheet` c  
#                     INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
#                     WHERE cs.task = %s AND c.employee = %s
#                 """, (i.task, emp_name), as_dict=True)

#                 sum_total = frappe.db.sql("""
#                     SELECT SUM(cs.hours) AS hours 
#                     FROM `tabTimesheet` c  
#                     INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
#                     WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
#                 """, (i.task, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)

#                 total_hours = sum_task[0].total_hours or 0 if sum_task else 0
#                 total_period = sum_total[0].hours or 0 if sum_total else 0

#             i.at = total_hours
#             i.at_period = total_period
#             i.cr_status=task_status
#         sprint_doc.save()

@frappe.whitelist()
def update_allocated_task_at_dev(date, name, service, type, dev_team, sprint):
    parent_doc = frappe.get_doc("Daily Monitor",
                                 name)
    existing_task_ids = {(d.id, d.cb): d for d in parent_doc.task_details if d.id and d.cb}
    
    issues = []
    meetings = []
    tasks = []

    if type == "OPS":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list = frappe.get_all("Employee", {
            'department': "IT. Development - THIS",
            'custom_dept_type': 'OPS',
            "custom_dev_team": dev_team
        }, ['short_code', 'name'])
        # employee_list = frappe.get_all("Employee", ['short_code', 'name'])

        for emp in employee_list:
            timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee': emp.name}, ['name'])
            short_code = emp.short_code

            if timesheet:
                issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_issue': ['!=', '']}, fields=['*'])
                for issue in issue_logs:
                    key = (issue.custom_issue, short_code)
                    if key in appended_issues:
                        continue

                    priority = frappe.db.get_value("Issue", issue.custom_issue, "priority")
                    status = frappe.db.get_value("Issue", issue.custom_issue, "status")
                    sum_issue = frappe.db.sql("""
                        SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                        WHERE cs.custom_issue=%s AND c.employee=%s AND c.start_date=%s
                    """, (issue.custom_issue, emp.name, date), as_dict=True)[0].total or 0.0

                    data = {
                        "id": issue.custom_issue,
                        "at_taken": sum_issue,
                        'project_name': issue.project_name,
                        'subject': issue.custom_subject_issue,
                        'status': status,
                        'cb': short_code,
                        'priority': priority
                    }

                    if key in existing_task_ids:
                        row = existing_task_ids[key]
                        for k, v in data.items():
                            row.set(k, v)
                    else:
                        issues.append(data)

                    appended_issues.add(key)

                meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_meeting': ['!=', '']}, fields=['*'])
                for meeting in meeting_logs:
                    key = (meeting.custom_meeting, short_code)
                    if key in appended_meetings:
                        continue

                    status = frappe.db.get_value("Meeting", meeting.custom_meeting, "status")
                    sum_meeting = frappe.db.sql("""
                        SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                        WHERE cs.custom_meeting=%s AND c.employee=%s AND c.start_date=%s
                    """, (meeting.custom_meeting, emp.name, date), as_dict=True)[0].total or 0.0

                    data = {
                        "id": meeting.custom_meeting,
                        "at_taken": sum_meeting,
                        'subject': meeting.custom_subject_meeting,
                        'cb': short_code,
                        'status': status
                    }

                    if key in existing_task_ids:
                        row = existing_task_ids[key]
                        for k, v in data.items():
                            row.set(k, v)
                    else:
                        meetings.append(data)

                    appended_meetings.add(key)

                task_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'task': ['!=', '']}, fields=['*'])
                for log in task_logs:
                    key = (log.task, short_code)
                    if key in appended_tasks:
                        continue

                    status = frappe.db.get_value("Task", log.task, "status")
                    sum_task = frappe.db.sql("""
                        SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
                        WHERE cs.task=%s AND c.employee=%s AND c.start_date=%s
                    """, (log.task, emp.name, date), as_dict=True)[0].total or 0.0

                    if log.activity_type =="Code Review":
                        
                        data = {
                            "id": log.task,
                            "at_taken": sum_task,
                            "cb": short_code,
                            "current_status": status,
                            "rt":0
                        }
                        
                    else:
                        
                        data = {
                            "id": log.task,
                            "at_taken": sum_task,
                            "cb": short_code,
                            "current_status": status,
                            "rt": frappe.db.get_value("Task",{'name':log.task},['rt'])
                        }

                    if key in existing_task_ids:
                        row = existing_task_ids[key]
                        for k, v in data.items():
                            row.set(k, v)
                    else:
                        tasks.append(data)

                    appended_tasks.add(key)

        for d in issues:
            parent_doc.append("task_details", d)
        for m in meetings:
            parent_doc.append("task_details", m)
        for t in tasks:
            parent_doc.append("task_details", t)

        parent_doc.dsr_check = 1

    parent_doc.dm_status = 'DSR Pending'
    parent_doc.save()
    frappe.db.commit()

    # === Update Sprint Task Table ===
    # if sprint:
    #     sprint_doc = frappe.get_doc("Sprint", {"sprint_id": sprint, "team": dev_team})
    #     existing_sprint_entries = {(d.task, d.cb) for d in sprint_doc.sprint_task}

    #     for d in parent_doc.task_details:
    #         task_id = d.id
    #         cb = d.cb
    #         if not task_id or not cb:
    #             continue

    #         emp_name = frappe.db.get_value("Employee", {"short_code": cb}, "name")
    #         emp_id = frappe.db.get_value("Employee", {"short_code": cb}, "user_id")
    #         task_status = frappe.db.get_value("Task", task_id, "status")
    #         project = frappe.db.get_value("Task", task_id, "project")

    #         if (task_id, cb) in existing_sprint_entries:
    #             continue

    #         total_hours = frappe.db.sql("""
    #             SELECT SUM(cs.hours) AS total_hours 
    #             FROM `tabTimesheet` c  
    #             INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
    #             WHERE cs.task = %s AND c.employee = %s
    #         """, (task_id, emp_name), as_dict=True)[0].total_hours or 0

    #         total_period = frappe.db.sql("""
    #             SELECT SUM(cs.hours) AS hours 
    #             FROM `tabTimesheet` c  
    #             INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
    #             WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
    #         """, (task_id, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)[0].hours or 0

    #         sprint_doc.append("sprint_task", {
    #             "task": task_id,
    #             "project": project,
    #             "cb": cb,
    #             "at": total_hours,
    #             "at_period": total_period,
    #             "cr_status": task_status
    #         })

    #     sprint_doc.save()
    if sprint:
        sprint_doc = frappe.get_doc("Sprint", {"sprint_id": sprint, "team": dev_team})
        existing_sprint_entries = {(d.task, d.cb): d for d in sprint_doc.sprint_task}

        for d in parent_doc.task_details:
            task_id = d.id
            cb = d.cb
            if not task_id or not cb:
                continue

            emp_name = frappe.db.get_value("Employee", {"short_code": cb}, "name")
            if not emp_name:
                continue

            task_status = frappe.db.get_value("Task", task_id, "status")
            project = frappe.db.get_value("Task", task_id, "project")

            total_hours = frappe.db.sql("""
                SELECT SUM(cs.hours) AS total_hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.task = %s AND c.employee = %s
            """, (task_id, emp_name), as_dict=True)[0].total_hours or 0

            total_period = frappe.db.sql("""
                SELECT SUM(cs.hours) AS hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
            """, (task_id, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)[0].hours or 0

            # Check if (task, cb) already exists
            key = (task_id, cb)
            if key in existing_sprint_entries:
                # Update existing entry's at_period
                existing_entry = existing_sprint_entries[key]
                existing_entry.at_period = total_period
                existing_entry.at = total_hours
                existing_entry.cr_status = task_status
            else:
                # Add new entry
                sprint_doc.append("sprint_task", {
                    "task": task_id,
                    "project": project,
                    "cb": cb,
                    "at": total_hours,
                    "at_period": total_period,
                    "cr_status": task_status
                })

        sprint_doc.save()


@frappe.whitelist()
def run_daily_monitor_updates():
    today = nowdate()
    daily_monitors = frappe.get_all("Daily Monitor", filters={"date": today}, fields=["name", "service", "task_type", "dev_team", "sprint"])
    # daily_monitors = frappe.get_all("Daily Monitor", filters={"date": "2025-06-03","name":"DM-00666"}, fields=["name", "service", "task_type", "dev_team", "sprint"])
    
    for dm in daily_monitors:
        print(dm.name)
        try:
            print(dm.name)
            update_allocated_task_at_dev(
                # date="2025-06-03",
                date=today,
                name=dm.name,
                service=dm.service,
                type=dm.task_type,
                dev_team=dm.dev_team,
                sprint=dm.sprint
            )
            task_details = frappe.get_all("Allocated Tasks", 
                filters={"parent": dm.name, "current_status": "Working"},
                fields=["id"])

            if task_details and dm.sprint and dm.dev_team:
                sprint_doc = frappe.get_doc("Sprint",{"team":dm.dev_team,"sprint_id":dm.sprint})
                existing_task_ids = {row.task for row in sprint_doc.table_cusg}

                for task in task_details:
                    # if task.id not in existing_task_ids:
                    sprint_doc.append("table_cusg", {
                        "task": task.id,
                        "date":today
                    })

                sprint_doc.save()
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Daily Monitor Auto Update Failed for {dm.name}")


@frappe.whitelist()
def run_daily_monitor_dsr():
    today = nowdate()
    daily_monitors = frappe.get_all("Daily Monitor", filters={"date": today}, fields=["name", "service", "task_type", "dev_team", "sprint"])
    # daily_monitors = frappe.get_all("Daily Monitor", filters={"date": "2025-06-03","name":"DM-00666"}, fields=["name", "service", "task_type", "dev_team", "sprint"])
    for dm in daily_monitors:
        try:
            dpr_task_mail_it_dev(
                # date="2025-06-03",
                date=today,
                name=dm.name,
                service=dm.service,
                dev_team=dm.dev_team,
                sprint=dm.sprint,
                type=dm.task_type
            )
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Daily Monitor Auto Update Failed for {dm.name}")


