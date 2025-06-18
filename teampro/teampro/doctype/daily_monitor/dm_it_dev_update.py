import frappe
from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days

from collections import defaultdict   
@frappe.whitelist()
def dpr_task_mail_it_dev_update(date,name,service,type,dev_team,sprint):
    # date,name,service,type,dev_team,sprint
    # date= "2025-05-27"      
    # name="DM-00651"
    # service="IT-SW"
    # type="OPS"
    # dev_team="BRAVO"
    # sprint = "SPRINT 13"
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    frappe.errprint(formatted_date)
    u_id = frappe.db.get_value("Employee",{"custom_dev_team":dev_team,"custom_is_tl":1},["user_id"])
    frappe.errprint(u_id)
    # u_id = frappe.db.get_value("Employee",{"custom_dev_team":dev_team,"custom_is_tl":1},["user_id"])
    # frappe.errprint(u_id)
    recievers=[]
    if type=="OPS":
        emp=frappe.db.get_all("Employee",{'status':'Active','custom_dev_team':dev_team},['*'])
        # dev = frappe.db.get_doc("Daily Monitor",name)
            
        recievers.append('abdulla.pi@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
    recievers.append('dineshbabu.k@groupteampro.com')
    # recievers.append('muthuselvan.e@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
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
                data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td>' % (
                    count, i.id or '', i.project_name or '', i.subject, i.cb, i.current_status, i.et, i.rt, at, at_taken, i.priority
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
                    <td>{rt}</td>
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
                <td>{grand_total_rt}</td>
                <td>{grand_total_at_rounded}</td>
                <td>{grand_rt_vs_aph}</td>
            </tr>
            '''
            summary += '</table>'
            frappe.sendmail(
                    # sender='abdulla.pi@groupteampro.com',
                    sender= u_id,
                    # recipients=recievers,
                    # cc='abdulla.pi@groupteampro.com',
                    #   cc='divya.p@groupteampro.com',
                    recipients='muthuselvan.e@groupteampro.com',
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
            # task_data.workflow_state='Submitted'
            task_data.save()
            # frappe.db.commit()
    else:
        # u_id = frappe.db.get_value("Employee",{"custom_dev_team":dev_team,"custom_is_tl":1},["user_id"])
        # frappe.errprint(u_id)
    
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
                data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style="text-align:right">%s</td><td style="text-align:right">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
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
                <td>{grand_total_rt}</td>
                <td>{grand_rt_vs_aph}%</td>
            </tr>
            '''
            summary += '</table>'
            frappe.sendmail(
                    # sender='abdulla.pi@groupteampro.com',
                    sender= u_id,
                    recipients="muthuselvan.e@groupteampro.com",
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
    

# @frappe.whitelist()
# def get_tl(date,name=None,service=None,type=None,dev_team=None,sprint=None):
#     # data = frappe.get_all("Employee",{"custom_production_date":date,"custom_is_tl": 1},["company_email","custom_dev_team"])
#     value = []
#     u_id = frappe.db.get_value("Employee",{"custom_dev_team":dev_team,"custom_is_tl":1},["user_id"])
#     task = frappe.db.get_all("Task",{"custom_production_date":date,"custom_dev_team":dev_team,"custom_sprint":sprint},["custom_production_date","custom_sprint","custom_dev_team","subject","name","project_name","cb","status","revisions"])
#     for i in task:
#         frappe.errprint(i.subject)
#         frappe.errprint(i.name)
#         value[i.name]
#     frappe.errprint(u_id)
#     return task
@frappe.whitelist()
def get_tl(date, name=None, service=None, type=None, dev_team=None, sprint=None):
    if not (date and dev_team and sprint):
        frappe.throw("Date, Development Team, and Sprint are required fields.")
    u_id = frappe.db.get_value(
        "Employee",
        {"custom_dev_team": dev_team, "custom_is_tl": 1},
        "user_id"
    )
    tasks = frappe.db.get_all(
        "Task",
        filters={
            "custom_production_date": date,
            "custom_dev_team": dev_team,
            "custom_sprint": sprint
        },
        fields=[
            "custom_production_date", "custom_sprint", "custom_dev_team",
            "subject", "name", "project_name", "cb", "status", "revisions"
        ]
    )
    for task in tasks:
        frappe.errprint(f"Subject: {task.subject}, Name: {task.name}")

    frappe.errprint(f"Team Lead User ID: {u_id}")

    return tasks
