import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days
from teampro.teampro.doctype.sprint.sprint import get_retro_summary_html_test

@frappe.whitelist()
def get_allocated_tasks_for_it_dev(date,name,service,type,dev_team,sprint):
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details=[]
    parent_doc.dm_summary=[]
    if service == "IT-SW":
        task_id=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"custom_dev_team":dev_team,"custom_sprint":sprint},['*'],order_by='cb asc, project asc, priority asc')
        task_det=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"custom_dev_team":dev_team,"custom_sprint":sprint},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
        for i in task_id:
            parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":i.cb})
            frappe.db.set_value("Task",i.name,"allocated",1)
        for k in task_det:
            actual_aph=frappe.db.get_value('Employee',{'short_code':k.cb},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and service='IT-SW' and custom_dev_team=%s and custom_sprint=%s group by custom_allocated_to""",(k.custom_allocated_to,date,dev_team,sprint), as_dict=True)
            allocated_count=frappe.db.count("Task",{"custom_allocated_to":k.custom_allocated_to,"custom_production_date":date,"service":"IT-SW","status":"Working","allocated":1})
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
def dpr_task_mail_it_dev(date,name,service,dev_team,sprint):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]
    if service =="IT-SW":
        emp=frappe.db.get_all("Employee",{'status':'Active','custom_dev_team':dev_team,'department':'IT. Development - THIS'},['*'])
        recievers.append('abdulla.pi@groupteampro.com')
        recievers.append('gifty.p@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
        if dev_team == "BRAVO":
            recievers.append('kmoorthy.paulraj@gmail.com')
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    # tl_email=frappe.db.get_value("Employee",{"custom_is_tl":1,"custom_is_sub_tl":0,"custom_dev_team":dev_team,'department':'IT. Development - THIS'},["user_id"])
    tl_email=frappe.session.user
    task = frappe.db.get_all("Task", {"custom_production_date":date,"service":service,"custom_dev_team":dev_team,"custom_sprint":sprint}, ['*'], order_by='cb asc',group_by='custom_allocated_to asc')
    if task_data.dsr_check==1:
        if service =="IT-SW":
            count=1
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>SI NO</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>Task ID</b></td>
                <td style='width:15%;text-align:center; vertical-align:middle;'><b>Project Name</b></td>
                <td style='width:20%;text-align:center; vertical-align:middle;'><b>Subject</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>CB</b></td>
                <td style='width:10%;text-align:center; vertical-align:middle;'><b>Status</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>ET</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>RT</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>AT Total</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>AT Period</b></td>
                <td style='width:7%;text-align:center; vertical-align:middle;'><b>Priority</b></td>
                <td style='width:20%;text-align:center; vertical-align:middle;'><b>Working Remarks</b></td>
                <td style='width:15%;text-align:center; vertical-align:middle;'><b>ET Vs AT Remarks</b></td>
                <td style='width:15%;text-align:center; vertical-align:middle;'><b>TL Remarks</b></td>
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
                bg_color = "#b8cce4" if count % 2 == 0 else "#ffffff"
                cell_style = f'style="background-color: {bg_color}; border: 1px solid #333; padding: 4px; vertical-align: middle;"'

                data += f'<tr {cell_style}>' \
                        f'<td style="text-align:center">{count}</td>' \
                        f'<td style="text-align:center">{i.id or ""}</td>' \
                        f'<td style="text-align:center">{i.project_name or ""}</td>' \
                        f'<td style="text-align:center">{i.subject}</td>' \
                        f'<td style="text-align:center">{i.cb}</td>' \
                        f'<td style="text-align:center">{i.current_status}</td>' \
                        f'<td style="text-align:center">{i.et}</td>' \
                        f'<td style="text-align:center">{i.rt}</td>' \
                        f'<td style="text-align:center">{at}</td>' \
                        f'<td style="text-align:center">{at_taken}</td>' \
                        f'<td style="text-align:center">{i.priority}</td>' \
                        f'<td style="text-align:center">{i.remark or ""}</td>' \
                        f'<td style="text-align:center">{i.et_vs_at_remark or ""}</td>' \
                        f'<td style="text-align:center">{i.remarks or "-"}</td>' \
                        f'</tr>'
                count += 1

            data += '</table>'

            cb_summary = defaultdict(lambda: {'rt': 0,'at_taken':0})
            grand_total_rt = 0
            grand_total_aph = 0
            grand_total_at=0
            for i in task_data.task_details:
                cb = i.cb or "Not Set"
                cb_summary[cb]['rt'] += i.today_rt or 0
                cb_summary[cb]['at_taken'] += float(i.at_taken or 0)
            summary = '''
            <table border="1" width="40%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td style="text-align:center; vertical-align:middle;"><b>CB</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>APH</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>RT</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>AT</b></td>
                    <td style="text-align:center; vertical-align:middle;"   ><b>RT Vs AT%</b></td>
                </tr>
            '''
            for cb, data_cb in cb_summary.items():
                aph = 6 if frappe.db.get_value(
                    "Employee",
                    {
                        "short_code": cb,
                        "department": "IT. Development - THIS",
                        "custom_is_tl": 1,
                        "custom_is_sub_tl": 0
                    },
                    "custom_is_tl"
                ) else 8
                # aph = 6  if(frappe.db.get_value("Employee",{'short_code':cb,'custom_is_tl':1,'custom_is_sub_tl':0},['custom_is_tl'])) else 8
                rt = data_cb['rt']
                if float(rt) > float(aph):
                    rt=aph
                at=data_cb['at_taken']
                grand_total_aph += aph
                grand_total_rt += rt
                grand_total_at+=data_cb['at_taken']
                rt_vs_aph = round((at / rt) * 100, 2) if rt else 0
                summary += f'''
                <tr style="text-align:center;font-size: 12px;">
                    <td style="text-align:center; vertical-align:middle;">{cb}</td>
                    <td style="text-align:center; vertical-align:middle;">{aph}</td>
                    <td style="text-align:center; vertical-align:middle;">{round(rt,2)}</td>
                    <td style="text-align:center; vertical-align:middle;">{round(at,2)}</td>
                    <td style="text-align:center; vertical-align:middle;">{rt_vs_aph}</td>
                </tr>
                '''
            # grand_rt_vs_aph = round((grand_total_rt / grand_total_aph) * 100, 2) if grand_total_aph else 0
            grand_rt_vs_aph = round((grand_total_at / grand_total_rt) * 100, 2) if grand_total_rt else 0
            grand_total_at_rounded = round(grand_total_at, 2)
           
            summary += f'''
            <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
                <td style="text-align:center; vertical-align:middle;">Grand Total</td>
                <td style="text-align:center; vertical-align:middle;">{grand_total_aph}</td>
                <td style="text-align:center; vertical-align:middle;">{round(grand_total_rt,2)}</td>
                <td style="text-align:center; vertical-align:middle;">{grand_total_at_rounded}</td>
                <td style="text-align:center; vertical-align:middle;">{grand_rt_vs_aph}</td>
            </tr>
            '''
            summary += '</table>'
            team_type=frappe.db.get_value("Dev Team",{"name":dev_team},['team_type'])
            frappe.sendmail(
                    sender=tl_email,
                    recipients=recievers,
                    # recipients='pavithra.s@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    # subject = f'{service} - {dev_team} DSR {formatted_date} -Reg',
                    subject = f'DSR - {dev_team} ({team_type} )-{formatted_date} -Reg',
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
        if service =="IT-SW":
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>SI NO</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>Task ID</b></td>
                <td style='width:15%;text-align:center; vertical-align:middle;'><b>Project Name</b></td>
                <td style='width:20%;text-align:center; vertical-align:middle;'><b>Subject</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>CB</b></td>
                <td style='width:10%;text-align:center; vertical-align:middle;'><b>Status</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>ET</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>RT</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>Today RT</b></td>
                <td style='width:7%;text-align:center; vertical-align:middle;'><b>Priority</b></td>
            </b></tr>
            '''
            
            sorted_tasks = sorted(
                task_data.task_details,
                key=lambda x: (x.cb or '', x.project_name or '', x.priority or '')
            )

            count = 1
            for i in sorted_tasks:
                id='-'
                sub=''
                proj=''
                status=''
                priority=''
                exp_time='0.00'
                req_time='0.00'
                cb=''
                if i.id is not None:
                    id=i.id
                    sub=i.subject
                    proj=i.project_name
                    status=i.status
                    priority=i.priority
                    exp_time=i.et
                    req_time=i.rt
                    cb=i.cb
                elif i.issue is not None:
                    id=i.issue
                    sub=i.issue_subject
                    proj_name=frappe.db.get_value("Project",i.issue_project,"project_name")
                    proj=proj_name
                    status=i.issue_status
                    priority=i.issue_priority
                    exp_time=i.issue_et
                    req_time=i.issue_rt
                    cb=i.issue_cb
                else:
                    id='-'
                    sub='-'
                    proj=''
                    status=''
                    priority=''
                    exp_time='0.00'
                    req_time='0.00'
                    cb=''
                # data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td>' % (
                #     count, i.id, i.project_name or '', i.subject, i.cb, i.status, i.et, i.rt, i.priority
                # )
                row_bg = "#b8cce4" if count % 2 == 0 else "#ffffff"

                base_style = f"border: 1px solid #333; padding: 8px; background-color: {row_bg}; vertical-align: middle;"

                data += f'''
                <tr style="background-color: {row_bg};">
                    <td style="{base_style} text-align: center;">{count}</td>
                    <td style="{base_style} text-align: center;">{i.id}</td>
                    <td style="{base_style} text-align: center;">{i.project_name or ''}</td>
                    <td style="{base_style} text-align: center;">{i.subject}</td>
                    <td style="{base_style} text-align: center;">{i.cb}</td>
                    <td style="{base_style} text-align: center;">{i.status}</td>
                    <td style="{base_style} text-align: center;">{i.et}</td>
                    <td style="{base_style} text-align: center;">{i.rt}</td>
                    <td style="{base_style} text-align: center;">{i.today_rt}</td>
                    <td style="{base_style} text-align: center;">{i.priority}</td>
                </tr>
                '''
                count += 1

            data += '</table>'

           
            cb_summary = defaultdict(lambda: {'rt': 0})
            grand_total_rt = 0
            grand_total_aph = 0
            # Group RT by CB
            for i in task_data.task_details:
                cb = i.cb or "Not Set"
                cb_summary[cb]['rt'] += i.today_rt or 0


            # Generate summary HTML table
            summary = '''
            <table border="1" width="40%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;vertical-align:middle;font-size: 12px;">
                    <td style="text-align:center; vertical-align:middle;"><b>CB</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>APH</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>RT</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>RT Vs APH%</b></td>
                </tr>
            '''
            for cb, data_cb in cb_summary.items():
                aph = 6 if frappe.db.get_value(
                    "Employee",
                    {
                        "short_code": cb,
                        "department": "IT. Development - THIS",
                        "custom_is_tl": 1,
                        "custom_is_sub_tl": 0
                    },
                    "custom_is_tl"
                ) else 8
                # aph = 6  if(frappe.db.get_value("Employee",{'short_code':cb, 'department':"IT. Development - THIS",'custom_is_tl':1,'custom_is_sub_tl':0},['custom_is_tl'])) else 8
                rt = data_cb['rt']
                if float(rt) > float(aph):
                    rt=aph
                grand_total_aph += aph
                grand_total_rt += rt
                rt_vs_aph = round((rt / aph) * 100, 2) if aph else 0
                summary += f'''
                <tr style="text-align:center;font-size: 12px;">
                    <td style="text-align:center; vertical-align:middle;">{cb}</td>
                    <td style="text-align:center; vertical-align:middle;">{aph}</td>
                    <td style="text-align:center; vertical-align:middle;">{rt}</td>
                    <td style="text-align:center; vertical-align:middle;">{rt_vs_aph}</td>
                </tr>
                '''
            grand_rt_vs_aph = round((grand_total_rt / grand_total_aph) * 100, 2) if grand_total_aph else 0
            summary += f'''
            <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
                <td style="text-align:center; vertical-align:middle;">Grand Total</td>
                <td style="text-align:center; vertical-align:middle;">{grand_total_aph}</td>
                <td style="text-align:center; vertical-align:middle;">{round(grand_total_rt,2)}</td>
                <td style="text-align:center; vertical-align:middle;">{grand_rt_vs_aph}%</td>
            </tr>
            '''
            summary += '</table>'
            team_type=frappe.db.get_value("Dev Team",{"name":dev_team},['team_type'])
            frappe.sendmail(
                    sender=tl_email,
                    recipients=recievers,
                    # recipients='divya.p@groupteampro.com',
                    subject = f'DPR - {dev_team} ({team_type} )-{formatted_date} -Reg',
                    # subject = f'{service} - {dev_team} DPR {formatted_date} -Reg',
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
# def send_sprint_panned_mail():
#     name = 'SPM00049'
#     sprint_id = 'SPRINT 22'
#     team= 'DELTA'
    sprint_doc = frappe.get_doc("Sprint", name)
    sprint_retro = frappe.db.get_all("Sprint",{"team":team, "from_date":sprint_doc.from_date},["service","team","from_date","to_date","sprint_id","sprint_hours","allocated_hours","status"])[0]
    current_sprint_start = sprint_doc.from_date
    current_sprint_to = sprint_doc.to_date
    previous_sprint_name = frappe.db.get_value("Sprint",{"team": team,"from_date": ["<", current_sprint_start]},"name")
    recievers=[]
    if sprint_doc and previous_sprint_name:
        emp=frappe.db.get_all("Employee",{'status':'Active',"custom_dev_team":sprint_doc.team,'department':'IT. Development - THIS'},['*'])
        for n in emp:
            recievers.append(n.user_id)
        recievers.append('dineshbabu.k@groupteampro.com')
        recievers.append('abdulla.pi@groupteampro.com')
        recievers.append('gifty.p@groupteampro.com')
        if team == "BRAVO":
            recievers.append('kmoorthy.paulraj@gmail.com')
        # tl_email=frappe.db.get_value("Employee",{"custom_is_tl":1,"custom_is_sub_tl":0,"custom_dev_team":sprint_doc.team,'department':'IT. Development - THIS'},["user_id"])
        tl_email = frappe.session.user
        retro_sprint=frappe.get_doc("Sprint", previous_sprint_name)
        retro_sprint = frappe.get_doc("Sprint", previous_sprint_name)
        formatted_date = retro_sprint.from_date.strftime('%d/%m/%Y')
        formatted_date_to = retro_sprint.to_date.strftime('%d/%m/%Y')
        formatted_date_1 = current_sprint_start.strftime('%d/%m/%Y')
        formatted_date_2 = current_sprint_to.strftime('%d/%m/%Y')

        s_no=1
        index_no=1
        data = '''
            <table border="1"  width="20%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td style='width:5%'><b>S.No</b></td>
                    <td style='width:5%'><b>CB</b></td>
                    <td style='width:5%'><b>APH</b></td>
                    <td style='width:5%'><b>RT</b></td>
                    <td style='width:5%'><b>Occupany%</b></td>
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
        table_details = ''' 
                <table border="1" width="50%" style="border-collapse: collapse; margin-bottom: 10px;">
                    <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                        <td><b>Service</b></td>
                        <td><b>Team</b></td>
                        <td><b>From Date</b></td>
                        <td><b>To Date</b></td>
                        <td><b>Sprint ID</b></td>
                        <td><b>Sprint Hours</b></td>
                        <td><b>Allocated Hours</b></td>
                        <td><b>Status</b></td>
                    </tr>
            '''

        table_details += f'''
                <tr style="font-size: 12px;">
                    <td style="text-align:center;">{sprint_retro.service}</td>
                    <td style="text-align:left;">{sprint_retro.team}</td>
                    <td style="text-align:left;">{sprint_retro.from_date.strftime('%d/%m/%Y')}</td>
                    <td style="text-align:left;">{sprint_retro.to_date.strftime('%d/%m/%Y')}</td>
                    <td style="text-align:left;">{sprint_retro.sprint_id}</td>
                    <td style="text-align:right;">{sprint_retro.sprint_hours}</td>
                    <td style="text-align:right;">{sprint_retro.allocated_hours}</td>
                    <td style="text-align:left;">{sprint_retro.status}</td>
                </tr>
            '''

        table_details += '</table>'

                    
        table = '''
            <table border="1" width="100%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td><b>Sr</b></td>
                    <td><b>Project Name</b></td>
                    <td><b>Task</b></td>
                    <td><b>Subject</b></td>
                    <td><b>CB</b></td>
                    <td><b>Status</b></td>
                    <td><b>AT</b></td>
                    <td><b>RT</b></td>
                    <td><b>Current Status</b></td>
                </tr>
            '''
        if sprint_doc.sprint_task:
            for s in sprint_doc.sprint_task:
                table += f'''
                    <tr style="font-size: 12px;">
                        <td style="text-align:left;">{s_no}</td>
                        <td style="text-align:left;">{s.project}</td>
                        <td style="text-align:left;">{s.task}</td>
                        <td style="text-align:left;">{s.subject}</td>
                        <td style="text-align:left;">{s.cb}</td>
                        <td style="text-align:left;">{s.status}</td>
                        <td style="text-align:right;">{s.at:.2f}</td>
                        <td style="text-align:right;">{s.rt}</td>
                        <td style="text-align:left;">{s.cr_status}</td>
                    </tr>
                    '''
                s_no+=1
            table += '</table>'
        if sprint_doc:
            if sprint_doc.sprint_avl_time:
                for i in sprint_doc.sprint_avl_time:
                    emp_id=frappe.db.get_value("Employee",{"short_code":i.short_code,"status":"Active"},["name"])
                    timesheet_hrs = frappe.db.sql("""
                    SELECT SUM(total_hours) AS total_hours 
                    FROM `tabTimesheet`
                    WHERE employee=%s AND start_date BETWEEN %s AND %s
                """, (emp_id, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)
                    

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
                    """, (sprint_doc.from_date, sprint_doc.to_date, emp_id), as_dict=True)
                    present_days = present[0].count if present and present[0].count else 0

                    # Calculate average
                    avg_th_per_day = total_hours / present_days if present_days else 0
                    wastage=(i.bh-total_hours)/present_days if present_days else 0
                    frappe.errprint(wastage)
                    data += f"""
                    <tr style="font-size: 12px;">
                        <td style="text-align:center;">{index_no}</td>
                        <td style="text-align:left;">{i.short_code}</td>
                        <td style="text-align:right;">{i.available_hours:.2f}</td>
                        <td style="text-align:right;">{i.allocated_hours:.2f}</td>
                        <td style="text-align:right;">{i.occupancy:.2f}</td>
                        
                    </tr>
                    """
                    index_no+=1
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
        retro_summary = get_retro_summary_html_test(previous_sprint_name)
        # frappe.errprint(recievers)      
        frappe.sendmail(
                    sender=tl_email,
                    recipients=recievers,
                    # recipients=['jeniba.a@groupteampro.com','sivarenisha.m@groupteampro.com','abdulla.pi@groupteampro.com'],
                    subject = f'SPM - {team} - {formatted_date_1}-{formatted_date_2} -{sprint_doc.sprint_id}',
                    message = """
                    <b>Dear Team,</b><br><br>
                    <b>Sprint Details </b>
                    {}<br>
                    
                    <b>Sprint Avl Time</b><br><br>
                    {}<br>
                
                    <b>{}</b> <b>Planned Task</b><br><br>

                    {}<br>
                    <b>Retro Summary Table</b><br><br>
                    {}<br>
                    <b>RETRO</b><br><br>
                    {}<br><br>


                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(table_details,data,sprint_id,table,retro_summary,retro)
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
    cdr_list = []
    if service == "IT-SW":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list = frappe.get_all("Employee", {
            'department': "IT. Development - THIS",
            "custom_dev_team": dev_team
        }, ['short_code', 'name'])
        

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
                        "at_taken": round(sum_issue,2),
                        'project_name': issue.project_name,
                        'subject': issue.custom_subject_issue,
                        'current_status': status,
                        "status": status,
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
                        "at_taken": round(sum_meeting,2),
                        'subject': meeting.custom_subject_meeting,
                        'cb': short_code,
                        'current_status': status,
                        "status": status,
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
                            "at_taken": round(sum_task,2),
                            "cb": short_code,
                            "current_status": status,
                            "status": status,
                            "rt":0.5,
                            'today_rt':0.5
                        }
                        
                    else:
                        
                        data = {
                            "id": log.task,
                            "at_taken": round(sum_task,2),
                            "cb": short_code,
                            "current_status": status,
                            "status": status,
                            "rt": frappe.db.get_value("Task",{'name':log.task},['rt']),
                            'today_rt':frappe.db.get_value("Task",{'name':log.task},['rt'])
                        }

                    if key in existing_task_ids:
                        row = existing_task_ids[key]
                        for k, v in data.items():
                            if k == "today_rt":
                                continue
                            row.set(k, v)
                    else:
                        tasks.append(data)

                    appended_tasks.add(key)
    
                cdr_task_logs = frappe.get_all("Timesheet Summary", filters={'parent': timesheet, 'id': ['!=', '']}, fields=['*'])
                for log in cdr_task_logs:
                    key = (log.id, short_code)
                    if key in appended_tasks:
                        continue
                    status = frappe.db.get_value("Task", log.task, "status")
                    sum_task_result = frappe.db.sql("""
                        SELECT cs.tu as total 
                        FROM `tabTimesheet` c
                        INNER JOIN `tabTimesheet Summary` cs ON c.name = cs.parent
                        WHERE cs.document = 'Task' AND cs.task = %s AND c.employee = %s AND c.start_date = %s
                    """, (log.id, emp.name, date), as_dict=True)

                    sum_task = sum_task_result[0].total if sum_task_result else 0.0
                    # print(log.id)
                    if frappe.db.exists('Task',{'name':log.id}): 
                        alloc=frappe.db.get_value('Employee',{'short_code':short_code},['user_id']) 
                        allocated_person=frappe.db.get_value('Task',{'name':log.id},['custom_allocated_to']) 
                        if alloc != allocated_person:
                            data = {
                            "id": log.id,
                            "at_taken": round(sum_task,2),
                            "cb": short_code,
                            "current_status": status,
                            "status": status,
                            "rt": frappe.db.get_value("Task", log.task, "rt"),
                            "today_rt": 0.5,
                            }
                        else:
                            data = {
                            "id": log.id,
                            "at_taken": round(sum_task,2),
                            "cb": short_code,
                            "current_status": status,
                            "status": status,
                            "rt": frappe.db.get_value("Task", log.task, "rt"),
                            "today_rt": frappe.db.get_value("Task", log.task, "rt"),
                            }
                    else:
                        data = {
                            "id": log.id,
                            "at_taken": round(sum_task,2),
                            "cb": short_code,
                            "current_status": status,
                            "status": status,
                            "rt": frappe.db.get_value("Task", log.task, "rt"),
                            "today_rt": frappe.db.get_value("Task", log.task, "rt"),
                        }
                    if key in existing_task_ids:
                        row = existing_task_ids[key]
                        for k, v in data.items():
                            if k == "today_rt":
                                continue
                            row.set(k, v)
                    else:
                        cdr_list.append(data)

                    appended_tasks.add(key)

        for d in issues:
            parent_doc.append("task_details", d)
        for m in meetings:
            parent_doc.append("task_details", m)
        # print(tasks)
        # print(cdr_list)
        for t in tasks:
            parent_doc.append("task_details", t)
        for c in cdr_list:
            parent_doc.append("task_details", c)
        parent_doc.dsr_check = 1
        for row in parent_doc.task_details:
            if frappe.db.exists('Issue',{'name':row.id}):
                status =frappe.db.get_value('Issue',{'name':row.id},['status'])
            elif frappe.db.exists('Task',{'name':row.id}):
                status =frappe.db.get_value('Task',{'name':row.id},['status'])
            if status:
                row.current_status = status
    parent_doc.save()
    frappe.db.commit()
    if sprint:
        sprint_doc = frappe.get_doc("Sprint", {"sprint_id": sprint, "team": dev_team})
        existing_sprint_entries = {(d.task, d.cb): d for d in sprint_doc.sprint_task}

        for d in parent_doc.task_details:
            task_id = d.id
            allocated_to=frappe.db.get_value('Employee',{'short_code':d.cb},['user_id'])
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
                if frappe.db.exists('Issue',{'name':task_id}):
                    cr_status=frappe.db.get_value('Issue',{'name':task_id},['custom_issue_status'])
                    alloc=frappe.db.get_value('Issue',{'name':task_id},['assigned_to'])
                    project=frappe.db.get_value('Issue',{'name':task_id},['project'])
                    subject=frappe.db.get_value('Issue',{'name':task_id},['subject'])
                    total_period = frappe.db.sql("""
                    SELECT SUM(cs.hours) AS hours 
                    FROM `tabTimesheet` c  
                    INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                    WHERE cs.custom_issue = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
                """, (task_id, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)[0].hours or 0
                    existing_entry = existing_sprint_entries[key]
                    existing_entry.at_period = total_period
                    existing_entry.at = 0.5
                    existing_entry.cr_status = cr_status
                    existing_entry.project= project
                    existing_entry.subject= subject
                    if alloc!=allocated_to:
                        existing_entry.rt=0.5
                else:
                    alloc=frappe.db.get_value('Task',{'name':task_id},['custom_allocated_to'])
                    existing_entry = existing_sprint_entries[key]
                    existing_entry.at_period = total_period
                    existing_entry.at = round(total_hours,2)
                    existing_entry.cr_status = task_status
                    if alloc!=allocated_to:
                        existing_entry.rt=0.5
            else:
                # Add new entry and mark it as spot task
                if frappe.db.exists('Task',{'name':task_id}):
                    alloc=frappe.db.get_value('Task',{'name':task_id},['custom_allocated_to'])
                    sub=frappe.db.get_value('Task',{'name':task_id},['subject'])
                    if alloc!=allocated_to:
                        sprint_doc.append("sprint_task", {
                            "task": task_id,
                            "project": project,
                            "cb": cb,
                            'subject':sub,
                            "at": round(total_hours,2),
                            "at_period": total_period,
                            "cr_status": task_status,
                            'status':task_status,
                            'spot_task':1,
                            'rt':0.5
                        })
                    else:
                        sprint_doc.append("sprint_task", {
                            "task": task_id,
                            "project": project,
                            "cb": cb,
                            'subject':sub,
                            "at": round(total_hours,2),
                            "at_period": total_period,
                            "cr_status": task_status,
                            'status':task_status,
                            'spot_task':1,
                        })
                elif frappe.db.exists('Issue',{'name':task_id}):
                    issue_doc=frappe.get_doc('Issue',{'name':task_id})
                    sprint_doc.append("sprint_task", {
                        "task": task_id,
                        "project": issue_doc.project,
                        "cb": cb,
                        "at": round(total_hours,2),
                        "at_period": total_period,
                        "cr_status": issue_doc.custom_issue_status,
                        'status':issue_doc.custom_issue_status,
                        'spot_task':1,
                    })
                else:
                    sprint_doc.append("sprint_task", {
                        "task": task_id,
                        "project": project,
                        "cb": cb,
                        "at": round(total_hours,2),
                        "at_period": total_period,
                        "cr_status": task_status,
                        'status':task_status,
                        'spot_task':1,
                    })
        sprint_doc.save()
        sprint_doc.reload()


@frappe.whitelist()
def run_daily_monitor_updates():
    # today="2026-02-19"
    today = nowdate()
    daily_monitors = frappe.get_all("Daily Monitor", filters={"date": today}, fields=["name", "service", "task_type", "dev_team", "sprint"])
    # daily_monitors = frappe.get_all("Daily Monitor", filters={"date": "2025-06-03","name":"DM-00666"}, fields=["name", "service", "task_type", "dev_team", "sprint"])
    
    for dm in daily_monitors:
        # print(dm.name)
        try:
            # print(dm.name)
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
    # today="2026-02-19"
    today = nowdate()

    daily_monitors = frappe.get_all("Daily Monitor", filters={"date": today,"workflow_state":"Pending for HOD"}, fields=["name", "service", "task_type", "dev_team", "sprint"])
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
                # type=dm.task_type
            )
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Daily Monitor Auto Update Failed for {dm.name}")


@frappe.whitelist()
def update_the_current_status_in_sprint_document():
    sprint_docs = frappe.db.get_all('Sprint',{'workflow_state':'In Progress'},pluck='name')
    for sprint_name in sprint_docs:
        sprint_doc = frappe.get_doc('Sprint',sprint_name)
        for row in sprint_doc.sprint_task:
            if row.task and 'ISS-' in row.task:
               emp_name=frappe.db.get_value('Employee',{'short_code':row.cb},['name'])
            #    status =frappe.db.get_value('Issue',{'name':row.task},['status'])
               total_period = frappe.db.sql("""
                SELECT SUM(cs.hours) AS hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.custom_issue = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
                """, (row.task, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)[0].hours or 0
               total_hours = frappe.db.sql("""
                    SELECT SUM(cs.hours) AS total_hours 
                    FROM `tabTimesheet` c  
                    INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                    WHERE cs.custom_issue = %s AND c.employee = %s
                """, (row.task, emp_name), as_dict=True)[0].total_hours or 0
            else:
                emp_name=frappe.db.get_value('Employee',{'short_code':row.cb},['name'])
                # status =frappe.db.get_value('Task',{'name':row.task},['status'])
                total_period = frappe.db.sql("""
                SELECT SUM(cs.hours) AS hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
                """, (row.task, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)[0].hours or 0
                total_hours = frappe.db.sql("""
                    SELECT SUM(cs.hours) AS total_hours 
                    FROM `tabTimesheet` c  
                    INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                    WHERE cs.task = %s AND c.employee = %s
                """, (row.task, emp_name), as_dict=True)[0].total_hours or 0
            
            # if status:
            #     row.cr_status = status
            row.at_period=round(total_period,2)
            row.at= round(total_hours,2)
           
            frappe.log_error(message= round(float(total_hours),2), title="AT")
            frappe.log_error(title="ROW AT", message=str(row.at))

        sprint_doc.save(ignore_permissions=True)
        frappe.db.commit()
   
@frappe.whitelist()
def create_schedule_job_type():
    job = frappe.db.exists('Scheduled Job Type', 'update_the_current_status_in_sprint_document')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'teampro.teampro.doctype.daily_monitor.dm_it_dev.update_the_current_status_in_sprint_document',
            "frequency": 'Cron',
            "cron_format": "30 23 * * *"
        })
        sjt.save(ignore_permissions=True)



@frappe.whitelist()
def dpr_task_mail_for_cmn_service(date,name,service):

    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=['annie.m@groupteampro.com','dm@groupteampro.com']
    task_data=frappe.get_doc("Daily Monitor",name)
    if task_data.dsr_check==1:
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
        cb_summary = defaultdict(lambda: {'rt': 0,'at_taken':0})
        grand_total_rt = 0
        grand_total_aph = 0
        grand_total_at=0
        for i in task_data.task_details:
            cb = i.cb or "Not Set"
            cb_summary[cb]['rt'] += i.today_rt or 0
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
            aph = 8
            rt = data_cb['rt']
            if float(rt) > float(aph):
                rt=aph
            at=data_cb['at_taken']
            grand_total_aph += aph
            grand_total_rt += rt
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
        sender =frappe.db.get_value('Employee',{'department': 'Support Team - THIS','designation':'Graphic Designer','status':'Active'},['user_id'])
        if sender:
            frappe.sendmail(
                # sender=sender,
                recipients=recievers,
                # recipients=['jothi.m@groupteampro.com'],
                subject = f'{service} - DSR {formatted_date}',
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
            data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td>' % (
                count,id, i.project_name or '', i.subject, i.cb, i.status, i.et, i.rt, i.priority
            )
            count += 1

        data += '</table>'

        cb_summary = defaultdict(lambda: {'rt': 0})
        grand_total_rt = 0
        grand_total_aph = 0
        # Group RT by CB
        for i in task_data.task_details:
            cb = i.cb or "Not Set"
            cb_summary[cb]['rt'] += i.today_rt or 0


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
            if float(rt) > float(aph):
                rt=aph
            grand_total_aph += aph
            grand_total_rt += rt
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
        sender =frappe.db.get_value('Employee',{'department': 'Support Team - THIS','designation':'Graphic Designer','status':'Active'},['user_id'])
        if sender:
            frappe.sendmail(
                sender=sender,
                recipients=recievers,
                cc ='dineshbabu.k@groupteampro.com',
                subject = f'{service} - DPR {formatted_date}',
                message = """
                <b>Dear Team,</b><br><br>
                Please find the below DPR for {} for your kind reference. <br><br>
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
def dsr_task_mail_for_cmn_service():
    service ="CMN"
    date =today()
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=['annie.m@groupteampro.com','dm@groupteampro.com']
    if frappe.db.exists("Daily Monitor",{'service':service,'date':date,'dm_status':'DPR Completed'}):
        task_data=frappe.get_doc("Daily Monitor",{'service':service,'date':date,'dm_status':'DPR Completed'})
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
        </b></tr>
        '''
        sorted_tasks = sorted(
                task_data.task_details,
                key=lambda x: (x.cb or '', x.project_name or '', x.priority or '')
            )

        count = 1
        existing_task_ids = {i.id for i in sorted_tasks}
        emp_name =frappe.db.get_value('Employee', {"status":"Active","department": "Support Team - THIS","designation":'Graphic Designer'}, ['name'])
        for i in sorted_tasks:        
            # at = round(float(i.at or 0), 2)
            today_at=  frappe.db.sql("""
            SELECT SUM(d.hours) AS hours
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
        """, (date, emp_name, i.id), as_dict=1)[0].hours or 0
            print(emp_name)
            at_taken = round(float(today_at or 0), 2)
            i.at_taken =at_taken
            # at_taken = round(float(i.at_taken or 0), 2)
            at = round(float(frappe.get_value("Task", i.id, "actual_time") or 0),2)
            task_status = frappe.get_value("Task", i.id, "status")
            data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td>' % (
                count, i.id or '', i.project_name or '', i.subject, i.cb, task_status, i.et, i.rt, at, at_taken
            )
            count += 1
        timesheet_tasks = frappe.db.sql("""
            SELECT DISTINCT d.task, d.activity_type, d.project, d.subject, d.task_status
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task NOT IN %s
        """, (date, emp_name, existing_task_ids), as_dict=True)

        for row in timesheet_tasks:
            today_at = frappe.db.sql("""
                SELECT SUM(d.hours) AS hours
                FROM `tabTimesheet Detail` d
                JOIN `tabTimesheet` t ON d.parent = t.name
                WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
            """, (date, emp_name, row.task), as_dict=1)[0].hours or 0
            today_at=  frappe.db.sql("""
            SELECT SUM(d.hours) AS hours
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
        """, (date, emp_name, row.task), as_dict=1)[0].hours or 0
            print(emp_name)
            at_taken = round(float(today_at or 0), 2)
            et = round(float(frappe.get_value("Task", row.task, "expected_time") or 0),2)
            at = round(float(frappe.get_value("Task", row.task, "actual_time") or 0),2)
            rt = round(float(frappe.get_value("Task", row.task, "rt") or 0),2)
            task_cb = frappe.get_value("Task", row.task, "cb")
            task_status = frappe.get_value("Task", row.task, "status")
            # at_taken = round(float(i.at_taken or 0), 2)
            data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td>' % (
                count, row.task or '', row.project or '', row.subject, task_cb, task_status, et, rt, at_taken, at
            )

            count += 1
            
            task_data.append("task_details", {
                "id": row.task,
                "project_name": row.project,
                "subject": row.subject,
                "cb": task_cb,
                "current_status": task_status,
                "et": et,
                "rt": rt,
                "at": at,
                "at_taken": at_taken
            })



        data += '</table>'
        cb_summary = defaultdict(lambda: {'rt': 0,'at_taken':0})
        grand_total_rt = 0
        grand_total_aph = 0
        grand_total_at=0
        for i in task_data.task_details:
            cb = i.cb or "Not Set"
            cb_summary[cb]['rt'] += i.today_rt or 0
            cb_summary[cb]['at_taken'] += float(at_taken or 0)
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
            aph = 8
            rt = data_cb['rt']
            if float(rt) > float(aph):
                rt=aph
            at=data_cb['at_taken']
            grand_total_aph += aph
            grand_total_rt += rt
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
            # recipients='jothi.m@groupteampro.com',
            recipients=recievers,
            cc ='dineshbabu.k@groupteampro.com',
            subject = f'{service} - DSR {formatted_date}',
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
        if frappe.db.exists('Sprint', {'status': 'In Progress','service': service,'from_date': ['<=', date],'to_date': ['>=', date]}):
            sprint_doc = frappe.get_doc('Sprint', {'status': 'In Progress','service': service,'from_date': ['<=', date],'to_date': ['>=', date]})

            sprint_task_ids = {i.task for i in sprint_doc.sprint_task}

            timesheet_tasks = frappe.db.sql("""
                SELECT DISTINCT d.task, d.activity_type, d.project, d.subject, d.task_status
                FROM `tabTimesheet Detail` d
                JOIN `tabTimesheet` t ON d.parent = t.name
                WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task NOT IN %s
            """, (date, emp_name, tuple(sprint_task_ids) or ('',)), as_dict=True)

            for row in timesheet_tasks:
                today_at = frappe.db.sql("""
                    SELECT SUM(d.hours) AS hours
                    FROM `tabTimesheet Detail` d
                    JOIN `tabTimesheet` t ON d.parent = t.name
                    WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
                """, (date, emp_name, row.task), as_dict=1)[0].hours or 0

                at_taken = round(float(today_at or 0), 2)
                total_period = frappe.db.sql("""
                SELECT SUM(cs.hours) AS hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
                """, (row.task, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)[0].hours or 0

                # Fetch from Task if available
                et = round(float(frappe.get_value("Task", row.task, "expected_time") or 0), 2)
                at = round(float(frappe.get_value("Task", row.task, "actual_time") or 0), 2)
                rt = round(float(frappe.get_value("Task", row.task, "rt") or 0), 2)
                task_cb = frappe.get_value("Task", row.task, "cb") or "Not Set"
                priority = frappe.get_value("Task", row.task, "priority") or "Medium"
                task_status = row.task_status or "Working"
                production_date = frappe.get_value("Task", row.task, "custom_production_date")

                # Append to Sprint Task child table
                sprint_doc.append("sprint_task", {
                    "task": row.task,
                    "project": row.project,
                    "subject": row.subject,
                    "cb": task_cb,
                    "cr_status": task_status,
                    "et": et,
                    "rt": rt,
                    "at": at,
                    "at_period": total_period,
                    "production_date": production_date,
                    "status": "Working",
                    "priority": priority,
                    "spot_task":1
                })
                frappe.db.set_value('Task',{'name':row.task},'custom_spot_task',1)
            for i in sprint_doc.sprint_task:
                production_date = frappe.get_value("Task", i.task, "custom_production_date")
                today_at = frappe.db.sql("""
                    SELECT SUM(d.hours) AS hours
                    FROM `tabTimesheet Detail` d
                    JOIN `tabTimesheet` t ON d.parent = t.name
                    WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
                """, (production_date, emp_name, i.task), as_dict=1)[0].hours or 0

                at_taken = round(float(today_at or 0), 2)
                total_period = frappe.db.sql("""
                SELECT SUM(cs.hours) AS hours 
                FROM `tabTimesheet` c  
                INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                WHERE cs.task = %s AND c.employee = %s AND c.start_date BETWEEN %s AND %s
                """, (i.task, emp_name, sprint_doc.from_date, sprint_doc.to_date), as_dict=True)[0].hours or 0

                # Fetch data from Task doctype
                et = round(float(frappe.get_value("Task", i.task, "expected_time") or 0), 2)
                at = round(float(frappe.get_value("Task", i.task, "actual_time") or 0), 2)
                rt = round(float(frappe.get_value("Task", i.task, "rt") or 0), 2)
                task_cb = frappe.get_value("Task", i.task, "cb") or "Not Set"
                priority = frappe.get_value("Task", i.task, "priority") or "Medium"
                task_status = frappe.get_value("Task", i.task, "status") or "Working"
                

                # Update values
                i.cb = task_cb
                i.cr_status = task_status
                i.et = et
                i.rt = rt
                i.at = at,2
                i.at_period = total_period
                i.production_date = production_date or None
                i.status = "Working"
                i.priority = priority

            sprint_doc.save()
            frappe.db.commit()

@frappe.whitelist()
def run_daily_monitor_update_team(date,name,dev_team,sprint,service,task_type):
    today = nowdate()
    
    try:
        update_allocated_task_at_dev(
            date=date,
            name=name,
            service=service,
            type=task_type,
            dev_team=dev_team,
            sprint=sprint
        )
        task_details = frappe.get_all("Allocated Tasks", 
            filters={"parent":name, "current_status": "Working"},
            fields=["id"])

        if task_details and sprint and dev_team:
            sprint_doc = frappe.get_doc("Sprint",{"team":dev_team,"sprint_id":sprint})
            existing_task_ids = {row.task for row in sprint_doc.table_cusg}

            for task in task_details:
                sprint_doc.append("table_cusg", {
                    "task": task.id,
                    "date":today
                })

            sprint_doc.save()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Daily Monitor Auto Update Failed for {name}")


from frappe.utils import getdate
@frappe.whitelist()
def update_daily_monitor(task_id,production_date):
    
    task = frappe.get_doc("Task", task_id)
    dev_team = task.custom_dev_team
    sprint = task.custom_sprint
    dm = frappe.get_all("Daily Monitor",filters={"date": production_date, "dev_team": dev_team,"sprint": sprint},fields=["name"],limit=1)
    if dm:
        dm_doc = frappe.get_doc("Daily Monitor", dm[0].name)
        exists = False
        for d in dm_doc.task_details:
            if d.id == task_id:
                exists = True
                break
        if not exists:
            dm_doc.append("task_details", {
                "id": task_id,
                "today_rt":task.rt
            })
            dm_doc.save(ignore_permissions=True)
    return "Done"





def update_daily_monitor_task(doc, method):

    if doc.custom_production_date:

        production_date = doc.custom_production_date

        dev_team = doc.custom_dev_team
        sprint = doc.custom_sprint

        dm = frappe.get_all(
            "Daily Monitor",
            filters={
                "date": production_date,
                "dev_team": dev_team,
                "sprint": sprint
            },
            fields=["name"],
            limit=1
        )

        if dm:
            dm_doc = frappe.get_doc("Daily Monitor", dm[0].name)

            exists = False
            for d in dm_doc.task_details:
                if d.id == doc.name:
                    exists = True
                    break

            if not exists:
                dm_doc.append("task_details", {
                    "id": doc.name,
                    "today_rt": doc.rt
                })
                dm_doc.save(ignore_permissions=True)


from collections import defaultdict   
@frappe.whitelist()
def dpr_task_mail_it_dev_hod(date,name,service,dev_team,sprint):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]
    if service =="IT-SW":
        emp=frappe.db.get_all("Employee",{'status':'Active','custom_dev_team':dev_team,'department':'IT. Development - THIS'},['*'])
        recievers.append('abdulla.pi@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
        if dev_team == "BRAVO":
            recievers.append('kmoorthy.paulraj@gmail.com')
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    # tl_email=frappe.db.get_value("Employee",{"custom_is_tl":1,"custom_is_sub_tl":0,"custom_dev_team":dev_team,'department':'IT. Development - THIS'},["user_id"])
    tl_email = frappe.session.user
    task = frappe.db.get_all("Task", {"custom_production_date":date,"service":service,"custom_dev_team":dev_team,"custom_sprint":sprint}, ['*'], order_by='cb asc',group_by='custom_allocated_to asc')
    count=1
    if service =="IT-SW":
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>SI NO</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>Task ID</b></td>
            <td style='width:15%;text-align:center; vertical-align:middle;'><b>Project Name</b></td>
            <td style='width:20%;text-align:center; vertical-align:middle;'><b>Subject</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>CB</b></td>
            <td style='width:10%;text-align:center; vertical-align:middle;'><b>Status</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>ET</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>RT</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>Today RT</b></td>
            <td style='width:7%;text-align:center; vertical-align:middle;'><b>Priority</b></td>
        </b></tr>
        '''
        
        sorted_tasks = sorted(
            task_data.task_details,
            key=lambda x: (x.cb or '', x.project_name or '', x.priority or '')
        )

        count = 1
        for i in sorted_tasks:
            id='-'
            sub=''
            proj=''
            status=''
            priority=''
            exp_time='0.00'
            req_time='0.00'
            cb=''
            if i.id is not None:
                id=i.id
                sub=i.subject
                proj=i.project_name
                status=i.status
                priority=i.priority
                exp_time=i.et
                req_time=i.rt
                cb=i.cb
            elif i.issue is not None:
                id=i.issue
                sub=i.issue_subject
                proj_name=frappe.db.get_value("Project",i.issue_project,"project_name")
                proj=proj_name
                status=i.issue_status
                priority=i.issue_priority
                exp_time=i.issue_et
                req_time=i.issue_rt
                cb=i.issue_cb
            else:
                id='-'
                sub='-'
                proj=''
                status=''
                priority=''
                exp_time='0.00'
                req_time='0.00'
                cb=''
          
            row_bg = "#b8cce4" if count % 2 == 0 else "#ffffff"

            base_style = f"border: 1px solid #333; padding: 8px; background-color: {row_bg}; vertical-align: middle;"

            data += f'''
            <tr style="background-color: {row_bg};">
                <td style="{base_style} text-align: center;">{count}</td>
                <td style="{base_style} text-align: center;">{i.id}</td>
                <td style="{base_style} text-align: center;">{i.project_name or ''}</td>
                <td style="{base_style} text-align: center;">{i.subject}</td>
                <td style="{base_style} text-align: center;">{i.cb}</td>
                <td style="{base_style} text-align: center;">{i.status}</td>
                <td style="{base_style} text-align: center;">{i.et}</td>
                <td style="{base_style} text-align: center;">{i.rt}</td>
                <td style="{base_style} text-align: center;">{i.today_rt}</td>
                <td style="{base_style} text-align: center;">{i.priority}</td>
            </tr>
            '''
            count += 1

        data += '</table>'

        
        cb_summary = defaultdict(lambda: {'rt': 0})
        grand_total_rt = 0
        grand_total_aph = 0
        # Group RT by CB
        for i in task_data.task_details:
            cb = i.cb or "Not Set"
            cb_summary[cb]['rt'] += i.today_rt or 0


        # Generate summary HTML table
        summary = '''
        <table border="1" width="40%" style="border-collapse: collapse; margin-bottom: 10px;">
            <tr style="background-color: #0f1568 ;color: white;text-align:center;vertical-align:middle;font-size: 12px;">
                <td style="text-align:center; vertical-align:middle;"><b>CB</b></td>
                <td style="text-align:center; vertical-align:middle;"><b>APH</b></td>
                <td style="text-align:center; vertical-align:middle;"><b>RT</b></td>
                <td style="text-align:center; vertical-align:middle;"><b>RT Vs APH%</b></td>
            </tr>
        '''
        for cb, data_cb in cb_summary.items():
            aph = 6 if frappe.db.get_value(
                "Employee",
                {
                    "short_code": cb,
                    "department": "IT. Development - THIS",
                    "custom_is_tl": 1,
                    "custom_is_sub_tl": 0
                },
                "custom_is_tl"
            ) else 8
            # aph = 6  if(frappe.db.get_value("Employee",{'short_code':cb, 'department':"IT. Development - THIS",'custom_is_tl':1,'custom_is_sub_tl':0},['custom_is_tl'])) else 8
            rt = data_cb['rt']
            if float(rt) > float(aph):
                rt=aph
            grand_total_aph += aph
            grand_total_rt += rt
            rt_vs_aph = round((rt / aph) * 100, 2) if aph else 0
            summary += f'''
            <tr style="text-align:center;font-size: 12px;">
                <td style="text-align:center; vertical-align:middle;">{cb}</td>
                <td style="text-align:center; vertical-align:middle;">{aph}</td>
                <td style="text-align:center; vertical-align:middle;">{rt}</td>
                <td style="text-align:center; vertical-align:middle;">{rt_vs_aph}</td>
            </tr>
            '''
        grand_rt_vs_aph = round((grand_total_rt / grand_total_aph) * 100, 2) if grand_total_aph else 0
        summary += f'''
        <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
            <td style="text-align:center; vertical-align:middle;">Grand Total</td>
            <td style="text-align:center; vertical-align:middle;">{grand_total_aph}</td>
            <td style="text-align:center; vertical-align:middle;">{round(grand_total_rt,2)}</td>
            <td style="text-align:center; vertical-align:middle;">{grand_rt_vs_aph}%</td>
        </tr>
        '''
        summary += '</table>'
        team_type=frappe.db.get_value("Dev Team",{"name":dev_team},['team_type'])
        frappe.sendmail(
                sender=tl_email,
                recipients='abdulla.pi@groupteampro.com',
                cc=tl_email,
                # recipients="divya.p@groupteampro.com",
                subject = f'DPR - {dev_team} ({team_type} )-{formatted_date} -Reg',
                # subject = f'{service} - {dev_team} DPR {formatted_date} -Reg',
                message = """
                <b>Dear Sir,</b><br>
                 <p>
                Daily Monitor
                <a href='https://erp.teamproit.com/app/daily-monitor/{}' target="_blank">
                {}
                </a> - DPR was pending for your approval.
                </p>
                <p>Kindly review the DPR and approve the same.</p>
            {}<br>
            {}<br><br>
                Thanks & Regards,<br>TEAM ERP<br>
                
                <i>This email has been automatically generated. Please do not reply</i>
                """.format(name,name,summary,data)
            )
        frappe.msgprint("DPR mail has been successfully sent")
        task_data.save()
        frappe.db.commit()

from collections import defaultdict   
@frappe.whitelist()
def dpr_task_mail_it_dev_md(date,name,service,dev_team,sprint):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]
    if service =="IT-SW":
        emp=frappe.db.get_all("Employee",{'status':'Active','custom_dev_team':dev_team,'department':'IT. Development - THIS'},['*'])
        recievers.append('abdulla.pi@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
        if dev_team == "BRAVO":
            recievers.append('kmoorthy.paulraj@gmail.com')
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    # tl_email=frappe.db.get_value("Employee",{"custom_is_tl":1,"custom_is_sub_tl":0,"custom_dev_team":dev_team,'department':'IT. Development - THIS'},["user_id"])
    tl_email = frappe.session.user
    task = frappe.db.get_all("Task", {"custom_production_date":date,"service":service,"custom_dev_team":dev_team,"custom_sprint":sprint}, ['*'], order_by='cb asc',group_by='custom_allocated_to asc')
    count=1
    if service =="IT-SW":
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>SI NO</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>Task ID</b></td>
            <td style='width:15%;text-align:center; vertical-align:middle;'><b>Project Name</b></td>
            <td style='width:20%;text-align:center; vertical-align:middle;'><b>Subject</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>CB</b></td>
            <td style='width:10%;text-align:center; vertical-align:middle;'><b>Status</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>ET</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>RT</b></td>
            <td style='width:5%;text-align:center; vertical-align:middle;'><b>Today RT</b></td>
            <td style='width:7%;text-align:center; vertical-align:middle;'><b>Priority</b></td>
        </b></tr>
        '''
        
        sorted_tasks = sorted(
            task_data.task_details,
            key=lambda x: (x.cb or '', x.project_name or '', x.priority or '')
        )

        count = 1
        for i in sorted_tasks:
            id='-'
            sub=''
            proj=''
            status=''
            priority=''
            exp_time='0.00'
            req_time='0.00'
            cb=''
            if i.id is not None:
                id=i.id
                sub=i.subject
                proj=i.project_name
                status=i.status
                priority=i.priority
                exp_time=i.et
                req_time=i.rt
                cb=i.cb
            elif i.issue is not None:
                id=i.issue
                sub=i.issue_subject
                proj_name=frappe.db.get_value("Project",i.issue_project,"project_name")
                proj=proj_name
                status=i.issue_status
                priority=i.issue_priority
                exp_time=i.issue_et
                req_time=i.issue_rt
                cb=i.issue_cb
            else:
                id='-'
                sub='-'
                proj=''
                status=''
                priority=''
                exp_time='0.00'
                req_time='0.00'
                cb=''
            # data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td>' % (
            #     count, i.id, i.project_name or '', i.subject, i.cb, i.status, i.et, i.rt, i.priority
            # )
            row_bg = "#b8cce4" if count % 2 == 0 else "#ffffff"

            base_style = f"border: 1px solid #333; padding: 8px; background-color: {row_bg}; vertical-align: middle;"

            data += f'''
            <tr style="background-color: {row_bg};">
                <td style="{base_style} text-align: center;">{count}</td>
                <td style="{base_style} text-align: center;">{i.id}</td>
                <td style="{base_style} text-align: center;">{i.project_name or ''}</td>
                <td style="{base_style} text-align: center;">{i.subject}</td>
                <td style="{base_style} text-align: center;">{i.cb}</td>
                <td style="{base_style} text-align: center;">{i.status}</td>
                <td style="{base_style} text-align: center;">{i.et}</td>
                <td style="{base_style} text-align: center;">{i.rt}</td>
                <td style="{base_style} text-align: center;">{i.today_rt}</td>
                <td style="{base_style} text-align: center;">{i.priority}</td>
            </tr>
            '''
            count += 1

        data += '</table>'

        
        cb_summary = defaultdict(lambda: {'rt': 0})
        grand_total_rt = 0
        grand_total_aph = 0
        # Group RT by CB
        for i in task_data.task_details:
            cb = i.cb or "Not Set"
            cb_summary[cb]['rt'] += i.today_rt or 0


        # Generate summary HTML table
        summary = '''
        <table border="1" width="40%" style="border-collapse: collapse; margin-bottom: 10px;">
            <tr style="background-color: #0f1568 ;color: white;text-align:center;vertical-align:middle;font-size: 12px;">
                <td style="text-align:center; vertical-align:middle;"><b>CB</b></td>
                <td style="text-align:center; vertical-align:middle;"><b>APH</b></td>
                <td style="text-align:center; vertical-align:middle;"><b>RT</b></td>
                <td style="text-align:center; vertical-align:middle;"><b>RT Vs APH%</b></td>
            </tr>
        '''
        for cb, data_cb in cb_summary.items():
            aph = 6 if frappe.db.get_value(
                "Employee",
                {
                    "short_code": cb,
                    "department": "IT. Development - THIS",
                    "custom_is_tl": 1,
                    "custom_is_sub_tl": 0
                },
                "custom_is_tl"
            ) else 8
            # aph = 6  if(frappe.db.get_value("Employee",{'short_code':cb, 'department':"IT. Development - THIS",'custom_is_tl':1,'custom_is_sub_tl':0},['custom_is_tl'])) else 8
            rt = data_cb['rt']
            if float(rt) > float(aph):
                rt=aph
            grand_total_aph += aph
            grand_total_rt += rt
            rt_vs_aph = round((rt / aph) * 100, 2) if aph else 0
            summary += f'''
            <tr style="text-align:center;font-size: 12px;">
                <td style="text-align:center; vertical-align:middle;">{cb}</td>
                <td style="text-align:center; vertical-align:middle;">{aph}</td>
                <td style="text-align:center; vertical-align:middle;">{rt}</td>
                <td style="text-align:center; vertical-align:middle;">{rt_vs_aph}</td>
            </tr>
            '''
        grand_rt_vs_aph = round((grand_total_rt / grand_total_aph) * 100, 2) if grand_total_aph else 0
        summary += f'''
        <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
            <td style="text-align:center; vertical-align:middle;">Grand Total</td>
            <td style="text-align:center; vertical-align:middle;">{grand_total_aph}</td>
            <td style="text-align:center; vertical-align:middle;">{round(grand_total_rt,2)}</td>
            <td style="text-align:center; vertical-align:middle;">{grand_rt_vs_aph}%</td>
        </tr>
        '''
        summary += '</table>'
        team_type=frappe.db.get_value("Dev Team",{"name":dev_team},['team_type'])
        frappe.sendmail(
                sender=tl_email,
                recipients='dineshbabu.k@groupteampro.com',
                # recipients="divya.p@groupteampro.com",
                subject = f'DPR - {dev_team} ({team_type} )-{formatted_date} -Reg',
                # subject = f'{service} - {dev_team} DPR {formatted_date} -Reg',
                message = """
                <b>Dear Sir,</b><br>
                 <p>
                Daily Monitor
                <a href='https://erp.teamproit.com/app/daily-monitor/{}' target="_blank">
                {}
                </a> - DPR was pending for your approval.
                </p>
                <p>Kindly review the DPR and approve the same.</p>
            {}<br>
            {}<br><br>
                Thanks & Regards,<br>TEAM ERP<br>
                
                <i>This email has been automatically generated. Please do not reply</i>
                """.format(name,name,summary,data)
            )
        frappe.msgprint("DPR mail has been successfully sent")
        task_data.save()
        frappe.db.commit()


from collections import defaultdict   
@frappe.whitelist()
def dsr_task_mail_it_dev_hod(date,name,service,dev_team,sprint):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]
    if service =="IT-SW":
        emp=frappe.db.get_all("Employee",{'status':'Active','custom_dev_team':dev_team,'department':'IT. Development - THIS'},['*'])
        recievers.append('abdulla.pi@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
        if dev_team == "BRAVO":
            recievers.append('kmoorthy.paulraj@gmail.com')
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    # tl_email=frappe.db.get_value("Employee",{"custom_is_tl":1,"custom_is_sub_tl":0,"custom_dev_team":dev_team,'department':'IT. Development - THIS'},["user_id"])
    tl_email = frappe.session.user
    task = frappe.db.get_all("Task", {"custom_production_date":date,"service":service,"custom_dev_team":dev_team,"custom_sprint":sprint}, ['*'], order_by='cb asc',group_by='custom_allocated_to asc')
    if task_data.dsr_check==1:
        if service =="IT-SW":
            count=1
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>SI NO</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>Task ID</b></td>
                <td style='width:15%;text-align:center; vertical-align:middle;'><b>Project Name</b></td>
                <td style='width:20%;text-align:center; vertical-align:middle;'><b>Subject</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>CB</b></td>
                <td style='width:10%;text-align:center; vertical-align:middle;'><b>Status</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>ET</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>RT</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>AT Total</b></td>
                <td style='width:5%;text-align:center; vertical-align:middle;'><b>AT Period</b></td>
                <td style='width:7%;text-align:center; vertical-align:middle;'><b>Priority</b></td>
                <td style='width:20%;text-align:center; vertical-align:middle;'><b>Working Remarks</b></td>
                <td style='width:15%;text-align:center; vertical-align:middle;'><b>ET Vs AT Remarks</b></td>
                <td style='width:15%;text-align:center; vertical-align:middle;'><b>TL Remarks</b></td>
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
                bg_color = "#b8cce4" if count % 2 == 0 else "#ffffff"
                cell_style = f'style="background-color: {bg_color}; border: 1px solid #333; padding: 4px; vertical-align: middle;"'

                data += f'<tr {cell_style}>' \
                        f'<td style="text-align:center">{count}</td>' \
                        f'<td style="text-align:center">{i.id or ""}</td>' \
                        f'<td style="text-align:center">{i.project_name or ""}</td>' \
                        f'<td style="text-align:center">{i.subject}</td>' \
                        f'<td style="text-align:center">{i.cb}</td>' \
                        f'<td style="text-align:center">{i.current_status}</td>' \
                        f'<td style="text-align:center">{i.et}</td>' \
                        f'<td style="text-align:center">{i.rt}</td>' \
                        f'<td style="text-align:center">{at}</td>' \
                        f'<td style="text-align:center">{at_taken}</td>' \
                        f'<td style="text-align:center">{i.priority}</td>' \
                        f'<td style="text-align:center">{i.remark or ""}</td>' \
                        f'<td style="text-align:center">{i.et_vs_at_remark or ""}</td>' \
                        f'<td style="text-align:center">{i.remarks or "-"}</td>' \
                        f'</tr>'
                count += 1

            data += '</table>'

            cb_summary = defaultdict(lambda: {'rt': 0,'at_taken':0})
            grand_total_rt = 0
            grand_total_aph = 0
            grand_total_at=0
            for i in task_data.task_details:
                cb = i.cb or "Not Set"
                cb_summary[cb]['rt'] += i.today_rt or 0
                cb_summary[cb]['at_taken'] += float(i.at_taken or 0)
            summary = '''
            <table border="1" width="40%" style="border-collapse: collapse; margin-bottom: 10px;">
                <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                    <td style="text-align:center; vertical-align:middle;"><b>CB</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>APH</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>RT</b></td>
                    <td style="text-align:center; vertical-align:middle;"><b>AT</b></td>
                    <td style="text-align:center; vertical-align:middle;"   ><b>RT Vs AT%</b></td>
                </tr>
            '''
            for cb, data_cb in cb_summary.items():
                aph = 6 if frappe.db.get_value(
                    "Employee",
                    {
                        "short_code": cb,
                        "department": "IT. Development - THIS",
                        "custom_is_tl": 1,
                        "custom_is_sub_tl": 0
                    },
                    "custom_is_tl"
                ) else 8
                # aph = 6  if(frappe.db.get_value("Employee",{'short_code':cb,'custom_is_tl':1,'custom_is_sub_tl':0},['custom_is_tl'])) else 8
                rt = data_cb['rt']
                if float(rt) > float(aph):
                    rt=aph
                at=data_cb['at_taken']
                grand_total_aph += aph
                grand_total_rt += rt
                grand_total_at+=data_cb['at_taken']
                rt_vs_aph = round((at / rt) * 100, 2) if rt else 0
                summary += f'''
                <tr style="text-align:center;font-size: 12px;">
                    <td style="text-align:center; vertical-align:middle;">{cb}</td>
                    <td style="text-align:center; vertical-align:middle;">{aph}</td>
                    <td style="text-align:center; vertical-align:middle;">{round(rt,2)}</td>
                    <td style="text-align:center; vertical-align:middle;">{round(at,2)}</td>
                    <td style="text-align:center; vertical-align:middle;">{rt_vs_aph}</td>
                </tr>
                '''
            # grand_rt_vs_aph = round((grand_total_rt / grand_total_aph) * 100, 2) if grand_total_aph else 0
            grand_rt_vs_aph = round((grand_total_at / grand_total_rt) * 100, 2) if grand_total_rt else 0
            grand_total_at_rounded = round(grand_total_at, 2)
           
            summary += f'''
            <tr style="font-weight:bold; background-color:#eaeaea; text-align:center;">
                <td style="text-align:center; vertical-align:middle;">Grand Total</td>
                <td style="text-align:center; vertical-align:middle;">{grand_total_aph}</td>
                <td style="text-align:center; vertical-align:middle;">{round(grand_total_rt,2)}</td>
                <td style="text-align:center; vertical-align:middle;">{grand_total_at_rounded}</td>
                <td style="text-align:center; vertical-align:middle;">{grand_rt_vs_aph}</td>
            </tr>
            '''
            summary += '</table>'
            team_type=frappe.db.get_value("Dev Team",{"name":dev_team},['team_type'])
            frappe.sendmail(
                    sender=tl_email,
                    # recipients=recievers,
                    cc=tl_email,
                    recipients='abdulla.pi@groupteampro.com',
                    subject = f'DSR - {dev_team} ({team_type} )-{formatted_date} -Reg',
                    message = """
                        <b>Dear Sir,</b><br>
                        <p>
                        Daily Monitor
                        <a href='https://erp.teamproit.com/app/daily-monitor/{}' target="_blank">
                        {}
                        </a> - DSR was pending for your approval.
                        </p>
                        <p>Kindly review the DSR and approve the same.</p>
                    {}<br>
                    {}<br><br>
                        Thanks & Regards,<br>TEAM ERP<br>
                        
                        <i>This email has been automatically generated. Please do not reply</i>
                        """.format(name,name,summary,data)
                    )
            frappe.msgprint("DSR mail has been successfully sent.")
            task_data.save()
            frappe.db.commit()




import frappe
from frappe.utils import formatdate


@frappe.whitelist()
def send_daily_pr_report():

    tasks = frappe.get_all(
        "Task",
        fields=[
            "name",
            "subject",
            "project",
            "status",
            "creation",
            "custom_new_pr_date",
            "custom_age"
        ],
        filters={
            "status": "Pending Review",
            "service": "IT-SW"
        }
    )

    print(tasks)

    if not tasks:
        return


    project_wise_tasks = {}

    for task in tasks:

        if not task.project:
            continue

        if task.project not in project_wise_tasks:
            project_wise_tasks[task.project] = []

        project_wise_tasks[task.project].append(task)


    spoc_wise_tasks = {}

    for project_name, project_tasks in project_wise_tasks.items():

        spoc_mail = frappe.db.get_value(
            "Project",
            project_name,
            "spoc"
        )

        if not spoc_mail:
            continue

        if spoc_mail not in spoc_wise_tasks:
            spoc_wise_tasks[spoc_mail] = []

        spoc_wise_tasks[spoc_mail].extend(project_tasks)

    for spoc_mail, tasks_list in spoc_wise_tasks.items():

        table_rows = ""

        for i, task in enumerate(tasks_list, start=1):

            age = task.custom_age or 0

            pr_date = formatdate(
                task.custom_new_pr_date,
                "dd-MM-yyyy"
            ) if task.custom_new_pr_date else ""

            table_rows += f"""
            <tr style="background-color:{'#b8cce4' if i % 2 == 0 else '#ffffff'};">
                <td>{i}</td>
                <td>{task.name}</td>
                <td>{task.subject or ''}</td>
                <td>{task.project or ''}</td>
                <td>{age}</td>
                <td>{pr_date}</td>
            </tr>
            """

        html = f"""
        <p>Dear Team,</p>

        <p>Please find below the Pending Review Tasks Report.</p>

        <table border="1" cellpadding="8" cellspacing="0"
            style="border-collapse:collapse; width:100%;">

            <tr style="background:#0f1568;color:white;">
                <th>S.No</th>
                <th>Task</th>
                <th>Subject</th>
                <th>Project</th>
                <th>Age</th>
                <th>PR Date</th>
            </tr>

            {table_rows}

        </table>

        <br><br>

        <p>Regards,<br>
        TeamPro</p>
        """

        frappe.sendmail(
            recipients=[spoc_mail],
            subject="Pending Review Tasks Report",
            message=html
        )


    all_rows = ""

    grouped_projects = {}

    for task in tasks:

        if task.project not in grouped_projects:
            grouped_projects[task.project] = []

        grouped_projects[task.project].append(task)

    serial_no = 1

    for project_name, project_tasks in grouped_projects.items():


        for task in project_tasks:

            age = task.custom_age or 0

            pr_date = formatdate(
                task.custom_new_pr_date,
                "dd-MM-yyyy"
            ) if task.custom_new_pr_date else ""

            all_rows += f"""
            <tr style="background-color:{'#b8cce4' if serial_no % 2 == 0 else '#ffffff'};">
                <td>{task.name}</td>
                <td>{task.subject or ''}</td>
                <td>{task.project or ''}</td>
                <td>{age}</td>
                <td>{pr_date}</td>
            </tr>
            """

            serial_no += 1

    full_html = f"""
    <p>Dear Team,</p>

    <p>Please find below the Overall Pending Review Tasks Report.</p>

    <table border="1" cellpadding="8" cellspacing="0"
        style="border-collapse:collapse; width:100%;">

        <tr style="background:#0f1568;color:white;">
            <th>S.No</th>
            <th>Task</th>
            <th>Subject</th>
            <th>Project</th>
            <th>Age</th>
            <th>PR Date</th>
        </tr>

        {all_rows}

    </table>
    """


    frappe.sendmail(
        recipients=["gifty.p@groupteampro.com"],
        subject="Pending Review Tasks - Reg",
        message=full_html
    )




import frappe
from frappe.utils import formatdate


@frappe.whitelist()
def kt_not_confirmed_task():

    tasks = frappe.get_all(
        "Task",
        fields=[
            "name",
            "subject",
            "project",
            "status",
            "creation",
            "custom_new_pr_date",
            "custom_age"
        ],
        filters={
            "kt_confirmed": 0,
            "service": "IT-SW"
        }
    )


    if not tasks:
        return


    project_wise_tasks = {}

    for task in tasks:

        if not task.project:
            continue

        if task.project not in project_wise_tasks:
            project_wise_tasks[task.project] = []

        project_wise_tasks[task.project].append(task)


    spoc_wise_tasks = {}

    for project_name, project_tasks in project_wise_tasks.items():

        spoc_mail = frappe.db.get_value(
            "Project",
            project_name,
            "spoc"
        )

        if not spoc_mail:
            continue

        if spoc_mail not in spoc_wise_tasks:
            spoc_wise_tasks[spoc_mail] = []

        spoc_wise_tasks[spoc_mail].extend(project_tasks)

    for spoc_mail, tasks_list in spoc_wise_tasks.items():

        table_rows = ""

        for i, task in enumerate(tasks_list, start=1):

            age = task.custom_age or 0

            pr_date = formatdate(
                task.custom_new_pr_date,
                "dd-MM-yyyy"
            ) if task.custom_new_pr_date else ""

            table_rows += f"""
            <tr style="background-color:{'#b8cce4' if i % 2 == 0 else '#ffffff'};">
                <td>{i}</td>
                <td>{task.name}</td>
                <td>{task.subject or ''}</td>
                <td>{task.project or ''}</td>
                <td>{age}</td>
            </tr>
            """

        html = f"""
        <p>Dear Team,</p>

        <p>Please find below the KT not confirmed Tasks.</p>

        <table border="1" cellpadding="8" cellspacing="0"
            style="border-collapse:collapse; width:100%;">

            <tr style="background:#0f1568;color:white;">
                <th>S.No</th>
                <th>Task</th>
                <th>Subject</th>
                <th>Project</th>
                <th>Age</th>
            </tr>

            {table_rows}

        </table>

        <br><br>

        <p>Regards,<br>
        TeamPro</p>
        """

        frappe.sendmail(
            recipients=[spoc_mail],
            subject="KT Not Confirmed Tasks Report",
            message=html
        )


    all_rows = ""

    grouped_projects = {}

    for task in tasks:

        if task.project not in grouped_projects:
            grouped_projects[task.project] = []

        grouped_projects[task.project].append(task)

    serial_no = 1

    for project_name, project_tasks in grouped_projects.items():


        for task in project_tasks:

            age = task.custom_age or 0

            pr_date = formatdate(
                task.custom_new_pr_date,
                "dd-MM-yyyy"
            ) if task.custom_new_pr_date else ""

            all_rows += f"""
            <tr style="background-color:{'#b8cce4' if serial_no % 2 == 0 else '#ffffff'};">
                <td>{task.name}</td>
                <td>{task.subject or ''}</td>
                <td>{task.project or ''}</td>
                <td>{age}</td>
            </tr>
            """

            serial_no += 1

    full_html = f"""
    <p>Dear Team,</p>

    <p>Please find below the KT not confirmed Tasks.</p>

    <table border="1" cellpadding="8" cellspacing="0"
        style="border-collapse:collapse; width:100%;">

        <tr style="background:#0f1568;color:white;">
            <th>S.No</th>
            <th>Task</th>
            <th>Subject</th>
            <th>Project</th>
            <th>Age</th>
        </tr>

        {all_rows}

    </table>
    """


    frappe.sendmail(
        recipients=["gifty.p@groupteampro.com"],
        subject="KT Not Confirmed Tasks - Reg",
        message=full_html
    )




import frappe
from frappe.utils import nowdate, formatdate


@frappe.whitelist()
def send_next_contact_by_report():

    tasks = frappe.get_all(
        "Task",
        fields=[
            "name",
            "subject",
            "project",
            "custom_cr_next_contact_by",
            "custom_age"
        ],
        filters={
            "custom_cr_next_contact_by": nowdate(),
            "service": "IT-SW"
        }
    )

    if not tasks:
        return


    project_wise_tasks = {}

    for task in tasks:

        if not task.project:
            continue

        if task.project not in project_wise_tasks:
            project_wise_tasks[task.project] = []

        project_wise_tasks[task.project].append(task)
    spoc_wise_tasks = {}

    for project_name, project_tasks in project_wise_tasks.items():

        spoc_mail = frappe.db.get_value(
            "Project",
            project_name,
            "spoc"
        )

        if not spoc_mail:
            continue

        if spoc_mail not in spoc_wise_tasks:
            spoc_wise_tasks[spoc_mail] = []

        spoc_wise_tasks[spoc_mail].extend(project_tasks)


    for spoc_mail, tasks_list in spoc_wise_tasks.items():

        table_rows = ""

        for i, task in enumerate(tasks_list, start=1):

            next_contact_date = formatdate(
                task.custom_cr_next_contact_by,
                "dd-MM-yyyy"
            ) if task.custom_cr_next_contact_by else ""

            age = task.custom_age or 0

            table_rows += f"""
            <tr style="background-color:{'#b8cce4' if i % 2 == 0 else '#ffffff'};">
                <td>{i}</td>
                <td>{task.name}</td>
                <td>{task.subject or ''}</td>
                <td>{task.project or ''}</td>
                <td>{age}</td>
                <td>{next_contact_date}</td>
            </tr>
            """

        html = f"""
        <p>Dear Team,</p>

        <p>Please find below the Tasks with Next Contact By Date as Today.</p>

        <table border="1" cellpadding="8" cellspacing="0"
            style="border-collapse:collapse; width:100%;">

            <tr style="background:#0f1568;color:white;">
                <th>S.No</th>
                <th>Task</th>
                <th>Subject</th>
                <th>Project</th>
                <th>Age</th>
                <th>Next Contact By Date</th>
            </tr>

            {table_rows}

        </table>

        <br><br>

        <p>Regards,<br>
        TeamPro</p>
        """

        frappe.sendmail(
            recipients=[spoc_mail],
            subject="CR Reminder Mail - Reg",
            message=html
        )

    all_rows = ""

    serial_no = 1

    for project_name, project_tasks in project_wise_tasks.items():

        for task in project_tasks:

            next_contact_date = formatdate(
                task.custom_cr_next_contact_by,
                "dd-MM-yyyy"
            ) if task.custom_cr_next_contact_by else ""

            age = task.custom_age or 0

            all_rows += f"""
            <tr style="background-color:{'#b8cce4' if serial_no % 2 == 0 else '#ffffff'};">
                <td>{serial_no}</td>
                <td>{task.name}</td>
                <td>{task.subject or ''}</td>
                <td>{task.project or ''}</td>
                <td>{age}</td>
                <td>{next_contact_date}</td>
            </tr>
            """

            serial_no += 1

    full_html = f"""
    <p>Dear Team,</p>

    <p>Please find below the Overall Tasks with Next Contact By Date as Today.</p>

    <table border="1" cellpadding="8" cellspacing="0"
        style="border-collapse:collapse; width:100%;">

        <tr style="background:#0f1568;color:white;">
            <th>S.No</th>
            <th>Task</th>
            <th>Subject</th>
            <th>Project</th>
            <th>Age</th>
            <th>Next Contact By Date</th>
        </tr>

        {all_rows}

    </table>

    <br><br>

    <p>Regards,<br>
    TeamPro</p>
    """

    frappe.sendmail(
        recipients=["gifty.p@groupteampro.com"],
        subject="CR Reminder Mail - Reg",
        message=full_html
    )

