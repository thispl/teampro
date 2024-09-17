# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days

class DailyMonitor(Document):
	pass
@frappe.whitelist()
def get_allocated_tasks_for_it_cs(date,name,service,type):
    total=0
    percent=0
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details=[]
    parent_doc.dm_summary=[]
    issue_id=''
    issue_id_cs=''
    # task_det=''
    if type == "OPS":
        task_id=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type},['*'],order_by='cb asc, project asc, priority asc')
        task_det=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
        for i in task_id:
            parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":i.cb})
            employee_id=frappe.db.get_value('Employee',{'short_code':i.cb},['user_id'])
            issue_id=frappe.db.get_all("Issue",{'assigned_to':employee_id,'status':'Open'},['*'])
        for j in issue_id:
            issue_list=frappe.db.get_value("Employee",{'user_id':j.assigned_to},['short_code'])
            parent_doc.append("task_details", {"id": j.name,"project_name":j.project,"subject":j.subject,"cb":issue_list,"status":j.status})
        for k in task_det:
            actual_aph=frappe.db.get_value('Employee',{'short_code':k.cb},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(k.custom_allocated_to,date), as_dict=True)
            emp_cb=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['short_code'])
            total=sum_et[0].et
            if actual_aph is not None:
                percent=(float(sum_et[0].et)/float(actual_aph))*100
                parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph or '8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0'})
            else:
                percent=(float(sum_et[0].et)/8)*100
                parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':'8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0'})
    elif type == "CS":
        task_id_cs=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type,"status":("in",["Working","Pending Review","Client Review"])},['*'],order_by='cb asc, project asc, priority asc')
        for i in task_id_cs:
            parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":i.cb})
            employee_id=frappe.db.get_value('Employee',{'short_code':i.cb},['user_id'])
            issue_id_cs=frappe.db.get_all("Issue",{'assigned_to':employee_id,'status':'Open'},['*'])
        for j in issue_id_cs:
            issue_list=frappe.db.get_value("Employee",{'user_id':j.assigned_to},['short_code'])
            parent_doc.append("task_details", {"id": j.name,"project_name":j.project,"subject":j.subject,"cb":issue_list,"status":j.status})
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")

@frappe.whitelist()
def rec_allocated_tasks(name,service,date):
    task_id=frappe.db.get_all("Task",{"service":service,"custom_production_date":date},['*'],order_by='custom_allocated_to asc')
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.dm_rec_task_details=[]
    for i in task_id:
            parent_doc.append("dm_rec_task_details", {"id": i.name})
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")
    
@frappe.whitelist()
def sales_allocated_tasks(name, date):
    emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00023','user_id':('not in',['sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'])},['*'])
    recievers=[]
    for i in emp:
        recievers.append(i.user_id)
    recievers.append('anil.p@groupteampro.com')
    emp_list=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00007','user_id':('not in',['dm@groupteampro.com'])},['*'])
    for j in emp_list:
        recievers.append(j.user_id)
    recievers.append('annie.m@groupteampro.com')  
    # user_list = ["cheran.c@groupteampro.com", "harish.g@groupteampro.com", "aarthi.e@groupteampro.com", "vijiyalakshmi.k@groupteampro.com", "annie.m@groupteampro.com", "anil.p@groupteampro.com"]
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.dm_sales_details = []
    for user_email in recievers:
        short_code = frappe.db.get_value("Employee", {"user_id": user_email}, "short_code")
        lead_count = frappe.db.count("Sales Follow Up", {"next_contact_by": user_email,"next_contact_date": date,"follow_up_to":"Lead","status": "Lead"})
        open_count= frappe.db.count("Sales Follow Up", {"next_contact_by": user_email,"next_contact_date": date,"follow_up_to":"Lead","status": "Open"})
        replied_count= frappe.db.count("Sales Follow Up", {"next_contact_by": user_email,"next_contact_date": date,"follow_up_to":"Lead","status": "Replied"})       
        interested_count= frappe.db.count("Sales Follow Up", {"next_contact_by": user_email,"next_contact_date": date,"follow_up_to":"Lead","status": "Interested"})               
        opportunity_count= frappe.db.count("Sales Follow Up", {"next_contact_by": user_email,"next_contact_date": date,"follow_up_to":"Lead","status": "Opportunity"})   
        customer_count=frappe.db.count("Sales Follow Up", {"next_contact_by": user_email,"next_contact_date": date,"follow_up_to":"Customer"})
        appointment_count = frappe.db.count("Appointment",{"scheduled_time": ["between", [f"{date} 00:00:00", f"{date} 23:59:59"]],"owner":user_email})
        parent_doc.append("dm_sales_details", {
            "exe": short_code,
            "appointments":appointment_count,
            "lead": lead_count,
            "open":open_count,
            "interested":interested_count,
            "replied":replied_count,
            "opportunity":opportunity_count,
            "customer":customer_count
            
        })
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")
    
@frappe.whitelist()
def dpr_task_mail_cs_it(name,date,service,task_type):
    total=0
    total_count=0
    percent=0
    or_count=0
    pr_count=0
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]
    if task_type=="OPS":
        emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00005'},['*'])
        recievers.append('abdulla.pi@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
    elif task_type == "CS":
        emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00023'},['*'])
        recievers.append('anil.p@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    task = frappe.db.get_all("Task", {"custom_production_date":date,"type":task_type,"service":service}, ['*'], order_by='cb asc',group_by='custom_allocated_to asc')
    total_at=0
    if task_data.dsr_check==1:
        if task_type =="OPS":
            count=1
            aph_totals=0
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:4%'><b>SI NO</b></td>
                <td style='width:6%'><b>Task/Issue ID</b></td>
                <td style='width:12%'><b>Project </b></td>
                <td style='width:18%'><b>Subject</b></td>
                <td style='width:4%'><b>CB</b></td>
                <td style='width:7%'><b>Status</b></td>
                <td style='width:4%'><b>Revision</b></td>
                <td style='width:4%'><b>AT</b></td>
                <td style='width:4%'><b>ET</b></td>
                <td style='width:4%'><b>RT</b></td>
                <td style='width:6%'><b>Priority</b></td>
            <td style='width:8%'><b>Allocated On</b></td>
            <td style='width:4%'><b>Time Taken</b></td>
            <td style='width:10%'><b>Remarks</b></td>
            <td style='width:9%'><b>TL Remarks</b></td>
            </tr>
            '''
            table = '<table border="1" width="70%" style="border-collapse: collapse;text-align:center;">'
            table += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:1%'><b>CB</b></td>
                <td style='width:1%'><b>APH</b></td>
                <td style='width:1%'><b>RT</b></td>
                <td style='width:1%'><b>Actual Time Taken</b></td>
                <td style='width:1%'><b>RT Vs APH %</b></td>
                <td style='width:1%'><b>OR %</b></td>
                <td style='width:1%'><b>PR %</b></td>
            </tr>
            '''
            sorted_task_details = sorted(task_data.task_details, key=lambda i: i.cb)
            count = 1
            for i in sorted_task_details:
        #         # emp_cb=frappe.db.get_value('Employee',)
                vtaken = float(i.at)
                value_taken = round(vtaken, 3)
                if i.at_taken:
                    t_taken = float(i.at_taken)
                    today_taken = round(t_taken, 3)
                else:
                    t_taken='0'
                    today_taken='0'
                remark = '-' if i.remark is None else i.remark
                tl_remark = '-' if i.tl_remark is None else i.tl_remark
                if i.id is not None:
                    id=i.id
                elif i.issue is not None:
                    id=i.issue
                elif i.meeting is not None:
                    id=i.meeting
                else:
                    id='-'
                data += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'% (count,id, i.project_name, i.subject, i.cb, i.status, i.revisions, value_taken,i.et, i.rt, i.priority, i.allocated_on, today_taken, remark, tl_remark)
                count += 1
            data += '</table>'
            for j in task:
                employee_id=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['name'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['short_code'])
                timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])  
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and service="IT-SW" group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
                sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(j.custom_allocated_to,date), as_dict=True)                
                if sum_et:
                    total+=sum_et[0].et
                if actual_aph is not None:
                    aph_totals+=float(actual_aph)
                if timesheet is not None:
                    total_at+=float(timesheet)
                if actual_aph and timesheet:
                    percent=(float(timesheet)/float(actual_aph))*100
                    value=actual_aph
                    total_count=float(total_at)/float(aph_totals)*100
                    or_count=float(timesheet)/float(value)*100
                    pr_count=float(sum_et[0].et)/float(timesheet)*100
                    or_total=float(total_at)/float(aph_totals)*100
                    pr_total=float(total)/float(total_at)*100
                if percent:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et[0].et if sum_et else '0',round(timesheet,2) if timesheet is not None else '0',round(percent) if timesheet is not None else '0',round(or_count) if timesheet is not None else '0',round(pr_count) if timesheet is not None else '0')
                else:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et[0].et if sum_et else '0',round(timesheet,2) if timesheet is not None else'0','0',round(or_count,2) or '0',round(pr_count,2) or '0')
            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_totals,total,round(total_at,2),round(total_count),round(or_total),round(pr_total))
            table += "</table>"
            
            
            frappe.sendmail(
                    sender='abdulla.pi@groupteampro.com',
                    recipients='dineshbabu.k@groupteampro.com',
                    cc='abdulla.pi@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    subject='DSR %s -Reg' % formatted_date,
                    message = """
                <b>Dear Team,</b><br><br>
                    Please find the below DSR for {} for your kind reference.<br><br>
                    {}<br><br>
                    {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,table,data)
                )
            frappe.msgprint("DSR mail has been successfully sent.")
            frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
            frappe.db.set_value("Daily Monitor",name,'dsr_submitted_on',today())
        elif task_type =="CS":
            table=''
            count=1
            aph_totals=0
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:4%'><b>SI NO</b></td>
                <td style='width:6%'><b>Task/Issue ID</b></td>
                <td style='width:12%'><b>Project </b></td>
                <td style='width:18%'><b>Subject</b></td>
                <td style='width:4%'><b>CB</b></td>
                <td style='width:7%'><b>Status</b></td>
                <td style='width:4%'><b>Revision</b></td>
                <td style='width:6%'><b>Priority</b></td>
                <td style='width:8%'><b>Allocated On</b></td>
                <td style='width:4%'><b>Time Taken</b></td>
                <td style='width:10%'><b>Remarks</b></td>
                <td style='width:9%'><b>TL Remarks</b></td>
            </tr>
            '''
            sorted_task_details = sorted(task_data.task_details, key=lambda i: i.cb)
            count = 1
            for i in sorted_task_details:
        #         # emp_cb=frappe.db.get_value('Employee',)
                vtaken = float(i.at)
                value_taken = round(vtaken, 3)
                if i.at_taken:
                    t_taken = float(i.at_taken)
                    today_taken = round(t_taken, 3)
                else:
                    t_taken='0'
                    today_taken='0'
                remark = '-' if i.remark is None else i.remark
                tl_remark = '-' if i.tl_remark is None else i.tl_remark
                if i.id is not None:
                    id=i.id
                elif i.issue is not None:
                    id=i.issue
                elif i.meeting is not None:
                    id=i.meeting
                else:
                    id='-'
                data += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'% (count,id, i.project_name, i.subject, i.cb, i.status, i.revisions,i.priority, i.allocated_on, today_taken, remark, tl_remark)
                count += 1
            data += '</table>'
            frappe.sendmail(
                    # sender='abdulla.pi@groupteampro.com',
                    # recipients='dineshbabu.k@groupteampro.com',
                    # cc='abdulla.pi@groupteampro.com',
                    recipients=['divya.p@groupteampro.com','sarath.v@groupteampro.com'],
                    subject='DSR %s -Reg' % formatted_date,
                    message = """
                <b>Dear Team,</b><br><br>
                    Please find the below DSR for {} for your kind reference.<br><br>
                    {}<br><br>
                    {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,table if table else '',data)
                )
            frappe.msgprint("DSR mail has been successfully sent.")
            frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
            frappe.db.set_value("Daily Monitor",name,'dsr_submitted_on',today())
    else:
        count=1
        aph_total=0
        table=''
        if task_type=="OPS":
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
                <td style='width:5%'><b>SI NO</b></td>
                <td style='width:10%'><b>ID</b></td>
                <td style='width:15%'><b>Project </b></td>
                <td style='width:20%'><b>Subject</b></td>
                <td style='width:5%'><b>CB</b></td>
                <td style='width:10%'><b>Status</b></td>
                <td style='width:5%'><b>Revision</b></td>
                <td style='width:5%'><b>AT</b></td>
                <td style='width:5%'><b>ET</b></td>
                <td style='width:5%'><b>RT</b></td>
                <td style='width:7%'><b>Priority</b></td>
                <td style='width:13%'><b>Allocated On</b></td>
            </b></tr>
            '''
            for i in task_data.task_details:
                value_taken = round(i.at, 3)
                data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id or i.issue,i.project_name or '-',i.subject,i.cb,i.status,i.revisions,value_taken,i.et,i.rt,i.priority,i.allocated_on or '')
                count+=1
            data += '</table>'
            table = '<table border="1" width="50%" style="border-collapse: collapse;text-align:center;">'
            table += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:1%'><b>CB</b></td>
                <td style='width:1%'><b>APH</b></td>
                <td style='width:1%'><b>RT</b></td>
                <td style='width:1%'><b>RT Vs APH%</b></td>
            </tr>
            '''
            task_det=frappe.db.get_all("Task",{"custom_production_date":date,"type":task_type,"service":service},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
            for k in task_det:
                employee_id=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['user_id'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['short_code'])
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                sum_rt=frappe.db.sql("""select sum(rt) as rt from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(k.custom_allocated_to,date), as_dict=True)
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and service="IT-SW" group by custom_allocated_to""",(k.custom_allocated_to,date), as_dict=True)
                if sum_rt:
                    total+=sum_rt[0].rt
                if actual_aph is not None and sum_rt:
                    percent=(float(sum_rt[0].rt)/float(actual_aph))*100
                    value=actual_aph
                    aph_total+=float(value)
                total_count=float(total)/float(aph_total)*100
                # print(employee_id)
                if percent:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,value or '8',sum_rt[0].rt,round(percent,2) or '-')
                else:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '',sum_rt[0].rt,round(percent,2) or '-')
            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_total,total,round(total_count,2))
            table+='</table>'
            frappe.sendmail(
                    sender='abdulla.pi@groupteampro.com',
                    recipients=recievers,
                    # recipients='divya.p@groupteampro.com',
                    subject='DPR %s -Reg' % formatted_date,
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DPR for {} for your kind reference and action, ensure all the Tasks allocated on time and as per the requirement, for each Revision and AT going beyond 150% there will be NC applied and accumulated NC will be reviewed every week and directly affects your Performance.<br><br>

                {}<br><br>
                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,table,data)
                )
            frappe.msgprint("DPR mail has been successfully sent")
            frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
            frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())
        elif task_type=="CS":
            table=''
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '''
            <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
                <td style='width:5%'><b>SI NO</b></td>
                <td style='width:10%'><b>ID</b></td>
                <td style='width:15%'><b>Project </b></td>
                <td style='width:20%'><b>Subject</b></td>
                <td style='width:5%'><b>CB</b></td>
                <td style='width:10%'><b>Status</b></td>
                <td style='width:5%'><b>Revision</b></td>
                <td style='width:5%'><b>AT</b></td>
                <td style='width:5%'><b>ET</b></td>
                <td style='width:5%'><b>RT</b></td>
                <td style='width:7%'><b>Priority</b></td>
                <td style='width:13%'><b>Allocated On</b></td>
            </b></tr>
            '''
            for i in task_data.task_details:
                # value_taken = round(i.at, 3)
                data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id or i.issue,i.project_name or '-',i.subject,i.cb,i.status,'-','-','-','-',i.priority,i.allocated_on or '')
                count+=1
            data += '</table>' 
            frappe.sendmail(
                    sender='sarath.v@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
                    cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
                    subject='DPR %s -Reg' % formatted_date,
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DPR for {} for your kind reference and action, ensure all the Tasks allocated on time and as per the requirement.<br><br>

                {}<br><br>
                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,table if table else '',data)
                )
            frappe.msgprint("DPR mail has been successfully sent")
            frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
            frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())

@frappe.whitelist()
def update_rec_dpr(date, name):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00003','user_id':('not in',['chitra.g@groupteampro.com','keerthana.k@groupteampro.com','narendharan.k@groupteampro.com'])},['*'])
    recievers=[]
    for i in emp:
        recievers.append(i.user_id)
    # recievers.append('venkat.r@groupteampro.com')
    # recievers.append('ronaldo.a@groupteampro.com')
    # recievers.append('vignesh.j@groupteampro.com')
    # recievers.append('kamatchi.v@groupteampro.com')
    # recievers.append('dc@groupteampro.com')
    # recievers.append('aruna.g@groupteampro.com')
    # recievers.append('rama.a@groupteampro.com')
    # recievers.append('lokeshkumar.a@groupteampro.com')
    recievers.append('sangeetha.a@groupteampro.com')
    parent_doc = frappe.get_doc("Daily Monitor", name)
    if parent_doc.dsr_check==1:
        count=1

        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%'><b>SI NO</b></td>
            <td style='width:10%'><b>ID</b></td>
            <td style='width:15%'><b>Project </b></td>
            <td style='width:20%'><b>Subject</b></td>
            <td style='width:13%'><b>Allocated To</b></td>
            <td style='width:10%'><b>Status</b></td>
            <td style='width:7%'><b>Priority</b></td>
            <td style='width:13%'><b>RC</b></td>
            <td style='width:13%'><b>Actual Count</b></td>
            <td style='width:13%'><b>Current Status</b></td>
            <td style='width:13%'><b>TL Remarks</b></td>
        </b></tr>
        '''
        for i in parent_doc.dm_rec_task_details:
            data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id ,i.project_name or '-',i.subject,i.allocated_to,i.status,i.priority,i.rc or '-',i.actual_count or '-',i.current_status or '-',i.tl_remarks or '-')
            count+=1
        data += '</table>'
        frappe.sendmail(
                    # sender='sangeetha.a@groupteampro.com',
                    # recipients='dineshbabu.k@groupteampro.com',
                    # cc='sangeetha.a@groupteampro.com',
                    recipients='divya.p@groupteampro.com',
                    subject='DSR %s -Reg' % formatted_date,
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DSR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        frappe.msgprint("DSR mail has been successfully sent")
        frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
        frappe.db.set_value('Daily Monitor',name,'dsr_submitted_on',today())
    else:
        count=1
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%'><b>SI NO</b></td>
            <td style='width:10%'><b>ID</b></td>
            <td style='width:15%'><b>Project </b></td>
            <td style='width:20%'><b>Subject</b></td>
            <td style='width:13%'><b>Allocated To</b></td>
            <td style='width:10%'><b>Status</b></td>
            <td style='width:7%'><b>Priority</b></td>
            <td style='width:13%'><b>RC</b></td>
        </b></tr>
        '''
        for i in parent_doc.dm_rec_task_details:
            data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id ,i.project_name or '-',i.subject,i.allocated_to,i.status,i.priority,i.rc or '')
            count+=1
        data += '</table>'
        frappe.sendmail(
                    sender='sangeetha.a@groupteampro.com',
                    recipients=recievers,
                    # recipients='divya.p@groupteampro.com',
                    subject='DPR %s -Reg' % formatted_date,
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DPR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        frappe.msgprint("DPR mail has been successfully sent")
        frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
        frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())
        
        
@frappe.whitelist()
def update_sales_dpr(date, name):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00023','user_id':('not in',['sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'])},['*'])
    recievers=[]
    for i in emp:
        recievers.append(i.user_id)
    recievers.append('anil.p@groupteampro.com')
    emp_list=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00007','user_id':('not in',['dm@groupteampro.com'])},['*'])
    for j in emp_list:
        recievers.append(j.user_id)
    recievers.append('annie.m@groupteampro.com')   
    # user_list = ["cheran.c@groupteampro.com", "harish.g@groupteampro.com", "aarthi.e@groupteampro.com", "vijiyalakshmi.k@groupteampro.com", "annie.m@groupteampro.com", "anil.p@groupteampro.com"]
    parent_doc = frappe.get_doc("Daily Monitor", name)
    if parent_doc.dsr_check==1:
        count=1

        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '<tr style="text-align:center;"><td colspan="8"><b>R&S DSR, {}</b></td></tr>'.format(formatted_date)
        data += '''
            <tr style="background-color: #0f1568; color: white; text-align:center;">
                <td style="width:10%;"><b>Exe</b></td>
                <td style="width:15%;"><b>Effective</b></td>
                <td style="width:20%;"><b>Non Effective</b></td>
                <td style="width:20%;"><b>Total</b></td>
            </tr>
        '''
        for i in parent_doc.dm_sales_details:
            total_calls = i.effective_calls + i.non_effective_calls
            data += '<tr style="text-align:center;"><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                i.exe, i.effective_calls,i.non_effective_calls,total_calls
            )
        data += '</table>'
        frappe.sendmail(
                    # sender='sangeetha.a@groupteampro.com',
                    # recipients='dineshbabu.k@groupteampro.com',
                    # cc='sangeetha.a@groupteampro.com',
                    recipients='divya.p@groupteampro.com',
                    subject='DSR %s -Reg' % formatted_date,
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DSR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        frappe.msgprint("DSR mail has been successfully sent")
        frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
        frappe.db.set_value('Daily Monitor',name,'dsr_submitted_on',today())
    else:
        count=1
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '<tr style="text-align:center;"><td colspan="8"><b>R&S DPR, {}</b></td></tr>'.format(formatted_date)
        data += '''
            <tr style="background-color: #0f1568; color: white; text-align:center;">
                <td style="width:10%;"><b>Exe</b></td>
                <td style="width:15%;"><b>Appointments</b></td>
                <td style="width:20%;"><b>Lead</b></td>
                <td style="width:13%;"><b>Open</b></td>
                <td style="width:10%;"><b>Replied</b></td>
                <td style="width:7%;"><b>Interested</b></td>
                <td style="width:13%;"><b>Opportunity</b></td>
                <td style="width:13%;"><b>Customer</b></td>
            </tr>
        '''
        for i in parent_doc.dm_sales_details:
            data += '<tr style="text-align:center;"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                i.exe, i.appointments or '0', i.lead or '0', i.open or '0', i.replied or '0', i.interested or '0', i.opportunity or '0', i.customer or '0'
            )
        data += '</table>'

        frappe.sendmail(
                    # sender='sangeetha.a@groupteampro.com',
                    # recipients=recievers,
                    recipients='divya.p@groupteampro.com',
                    subject='DPR %s -Reg' % formatted_date,
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DPR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        frappe.msgprint("DPR mail has been successfully sent")
        frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
        frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())
        
@frappe.whitelist()
def update_dsr_cs_it(date, name,service,type):
    parent_doc = frappe.get_doc("Daily Monitor",name)
    parent_doc.task_details = []
    issues = []
    meetings = []
    tasks = []
    # appended_issues = set()
    # appended_meetings = set()
    # appended_tasks = set()
    parent_doc.dm_summary=[]
    if type == "OPS":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list=frappe.get_all("Employee",{'department':"ITS - THIS",'custom_dept_type':'OPS'},['short_code','name'])
        for emp in employee_list:
            timesheet = frappe.db.get_value("Timesheet", {'start_date':date, 'employee': emp.name},['name'])   
            task_hours_total = 0.0 
            if timesheet:
                issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_issue': ['!=', '']}, fields=['*'])
                i_taken=0.0
                for issue in issue_logs:
                    i_taken+=issue.hours
                    if issue.custom_issue not in appended_issues:
                        short_code=frappe.db.get_value("Employee",{'name':emp.name},['short_code'])
                        prior = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['priority'])
                        i_id = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['status'])
                        issues.append({
                            "id": issue.custom_issue,
                            "at_taken": issue.hours,
                            'project_name': issue.project_name,
                            'subject': issue.custom_subject_issue,
                            'status': i_id,
                            'cb':short_code,
                            'priority':prior
                        })
                        appended_issues.add(issue.custom_issue)            
                meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_meeting': ['!=', '']}, fields=['*'])
                for meeting in meeting_logs:
                    if meeting.custom_meeting not in appended_meetings:
                        m_id = frappe.db.get_value("Issue", {'name': meeting.custom_meeting}, ['status'])
                        short_code=frappe.db.get_value("Employee",{'name':emp.name},['short_code'])
                        meetings.append({
                            "id": meeting.custom_meeting,
                            "at_taken": meeting.hours,
                            'subject':meeting.custom_subject_meeting,
                            'cb':short_code
                        })
                        appended_meetings.add(meeting.custom_meeting)  
                # task_hours_total = 0.0
                task_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'task': ['!=','']}, fields=['*'])
                # timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':emp.name}, ['total_hours'])      
                for log in task_logs:
                    task_hours_total += log.hours
                    if log.task not in appended_tasks:
                        t_id=frappe.db.get_value("Task",{"name":log.task},['status'])
                        short_code=frappe.db.get_value("Employee",{'name':emp.name},['short_code'])
                        tasks.append({
                            "id": log.task,
                            "at_taken": log.hours,
                            "cb":short_code,
                            "current_status":t_id
                        })
                        appended_tasks.add(log.task)
        task_id_list = frappe.db.get_all("Task", {"custom_production_date":date,"service":service,"type":"OPS"}, ['*'], order_by='custom_allocated_to asc, project asc, priority asc')
        for task in task_id_list:
            emp_id = frappe.db.get_value("Employee", {'user_id': task.custom_allocated_to}, ['name'])
            emp_short_code= frappe.db.get_value("Employee", {'name': emp_id},['short_code'])
            if task.name not in appended_tasks:
                tasks.append({
                    "id": task.name,
                    "at_taken": 0,
                    "a_task_type":task.type,
                    "cb":emp_short_code,
                    "current_status":task.status
                })
        for d in issues:
            parent_doc.append("task_details", d)
        for meeting in meetings:
            parent_doc.append("task_details", meeting)
        for task in tasks:
            parent_doc.append("task_details", task)
        parent_doc.dsr_check = 1
        task_list = frappe.db.get_all("Task", {"custom_production_date":date,"type":type,"service":service}, ['*'], order_by='cb asc',group_by='custom_allocated_to asc')
        for j in task_list:
                employee_id=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['name'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['short_code'])
                timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])      
                actual_aph=frappe.db.get_value('Employee',{'name':employee_id},['custom_aph'])
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
                sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(j.custom_allocated_to,date), as_dict=True)

                if timesheet and actual_aph is not None:
                    percent=(float(timesheet)/float(actual_aph))*100
                    parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':round(timesheet,2),'rt_vs_aph_':round(percent,2)})
                else:
                    parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0' ,'d_actual_time_taken':'0','rt_vs_aph_':'0'})
    elif type == "CS":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list=frappe.get_all("Employee",{'department':"ITS - THIS",'custom_dept_type':'CS'},['short_code','name'])
        for emp in employee_list:
            timesheet = frappe.db.get_value("Timesheet", {'start_date':date, 'employee': emp.name},['name'])   
            task_hours_total = 0.0 
            if timesheet:
                # issue_logs = frappe.get_all("Timesheet Summary", filters={'parent': timesheet, 'task': ['!=', '']}, fields=['*'])
                issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_issue': ['!=', '']}, fields=['*'])
                
                i_taken=0.0
                for issue in issue_logs:
                    i_taken+=issue.hours
                    if issue.custom_issue not in appended_issues:
                        short_code=frappe.db.get_value("Employee",{'name':emp.name},['short_code'])
                        prior = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['priority'])
                        i_id = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['status'])
                        issues.append({
                            "id": issue.custom_issue,
                            "at_taken": issue.hours,
                            'project_name': issue.project_name,
                            'subject': issue.custom_subject_issue,
                            'status': i_id,
                            'cb':short_code,
                            'priority':prior
                        })
                        appended_issues.add(issue.custom_issue)            
                meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_meeting': ['!=', '']}, fields=['*'])
                for meeting in meeting_logs:
                    if meeting.custom_meeting not in appended_meetings:
                        m_id = frappe.db.get_value("Meeting", {'name': meeting.custom_meeting}, ['status'])
                        short_code=frappe.db.get_value("Employee",{'name':emp.name},['short_code'])
                        meetings.append({
                            "id": meeting.custom_meeting,
                            "at_taken": meeting.hours,
                            'subject':meeting.custom_subject_meeting,
                            'cb':short_code
                        })
                        appended_meetings.add(meeting.custom_meeting)  
                # task_hours_total = 0.0
                task_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'task': ['!=','']}, fields=['*'])
                # timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':emp.name}, ['total_hours'])      
                for log in task_logs:
                    task_hours_total += log.hours
                    if log.task not in appended_tasks:
                        t_id=frappe.db.get_value("Task",{"name":log.task},['status'])
                        short_code=frappe.db.get_value("Task",{"name":log.task},['cb'])
                        tasks.append({
                        "id": log.task,
                        "at_taken": log.hours,
                        # "a_task_type":task.type,
                        "cb":short_code,
                        "current_status":t_id
                        })
                        appended_tasks.add(log.task)        
        # task_id_list = frappe.db.get_all("Task", {"custom_production_date": date,"service":service,"type":type}, ['*'], order_by='cb asc, project asc, priority asc',group_by='cb')
        # for task in task_id_list:
        #     emp_id = frappe.db.get_value("Employee", {'short_code': task.cb}, ['name'])
        #     emp_short_code= frappe.db.get_value("Employee", {'name': emp_id},['short_code'])
            
        task_id_lists = frappe.db.get_all("Task", {"custom_production_date": date,"service":service,"type":type,"status":("in",["Working","Pending Review","Client Review"])}, ['*'], order_by='cb asc, project asc, priority asc')
        for i in task_id_lists: 
            tasks.append({
                "id": i.name,
                "a_task_type": i.type,
                "cb": i.cb,
                "current_status": i.status
            })
            appended_tasks.add(i.name)
        issues.sort(key=lambda x: (x['cb'] or '', x['priority'] or '', x['project_name'] or ''))
        meetings.sort(key=lambda x: (x['cb'] or '', x['subject'] or ''))
        tasks.sort(key=lambda x: (x['cb'] or '', x['current_status'] or ''))
        for d in issues:
            parent_doc.append("task_details", d)
        for meeting in meetings:
            parent_doc.append("task_details", meeting)
        for task in tasks:
            parent_doc.append("task_details", task)
        parent_doc.dsr_check = 1
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value('Daily Monitor',name,'dm_status','DSR Pending')

@frappe.whitelist()
def rec_update_dsr(name,date):
    parent_doc = frappe.get_doc("Daily Monitor", name)
    for j in parent_doc.dm_rec_task_details:
        candidate=frappe.db.count("Candidate",{"custom_project_modified_date":date,"candidate_created_by":j.allocated_to,"pending_for":("in",["Submitted(Internal)","Submitted(Client)","Submit(SPOC)","Linedup","QC Cleared","Shortlisted"]),"task":j.id},["name"])
        current_status=frappe.db.get_value("Task",{"name":j.id},["status"])
        j.actual_count=candidate
        j.current_status=current_status
    parent_doc.dsr_check = 1
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value('Daily Monitor',name,'dm_status','DSR Pending')
    
@frappe.whitelist()
def rs_update_dsr(name,date):
    emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00023','user_id':('not in',['sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'])},['*'])
    recievers=[]
    date_in_remarks_format = frappe.utils.formatdate(date, "dd/MM")
    for i in emp:
        recievers.append(i.user_id)
    recievers.append('anil.p@groupteampro.com')
    emp_list=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00007','user_id':('not in',['dm@groupteampro.com'])},['*'])
    for j in emp_list:
        recievers.append(j.user_id)
    recievers.append('annie.m@groupteampro.com')
    parent_doc=frappe.get_doc("Daily Monitor",name)
    for c in recievers:
        short_code=frappe.db.get_value("Employee",{"user_id":c},["short_code"])
        effective_call = frappe.db.sql("""SELECT COUNT(call_status) AS call_count FROM `tabSales Follow Up` WHERE modified_by = %s AND remarks LIKE %s AND call_status='Effective'""", (c,f"%{date_in_remarks_format}%"))
        non_effective_call= frappe.db.sql("""SELECT COUNT(call_status) AS call_count FROM `tabSales Follow Up` WHERE modified_by = %s AND remarks LIKE %s AND call_status='Non Effective'""", (c,f"%{date_in_remarks_format}%"))
        effective_call_count = effective_call[0][0] if effective_call else 0
        non_effective_call_count = non_effective_call[0][0] if non_effective_call else 0
        for doc in parent_doc.dm_sales_details:
            if doc.exe == short_code: 
                doc.effective_calls = effective_call_count
                doc.non_effective_calls = non_effective_call_count
    parent_doc.dsr_check = 1
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value('Daily Monitor',name,'dm_status','DSR Pending')

# @frappe.whitelist()
# def update_dsr_cs_it(name,date,service,type):
#     parent_doc = frappe.get_doc("Daily Monitor",name)
#     issues = []
#     meetings = []
#     e_tasks=[]
#     appended_issues = set()
#     appended_meetings = set()
#     appended_tasks = set()
#     for i in parent_doc.task_details:
#         allocated = frappe.db.get_value("Task", {"name": i.id}, ["custom_allocated_to"])
#         emp = frappe.db.get_value("Employee", {"user_id": allocated},["name"])
#         timesheets = frappe.get_value("Timesheet",{'start_date':date, 'employee': emp},['name'])
#         task_log=frappe.db.sql("""select sum(hours) as hrs from `tabTimesheet Detail` where parent=%s and task=%s """,(timesheets,i.id),as_dict=True)
#         current_status=frappe.db.get_value("Task",{"name":i.id},["status"])
#         current_type=frappe.db.get_value("Task",{"name":i.id},["type"])
#         i.current_status=current_status 
#         i.a_task_type=current_type
#         i.at_taken=task_log[0].hrs
#         task_logs = frappe.get_all("Timesheet Detail",{'parent': timesheets, 'task': ['!=', '']},['*'])
#         for k in task_logs:
#             if k.task not in i.id:
#                 allocate=frappe.db.get_value("Task",{"name":k.task},["custom_allocated_to"])
#                 emp_shortcode = frappe.db.get_value("Employee", {'user_id':allocate}, ['short_code'])
#                 t=frappe.db.sql("""select sum(hours) as hr from `tabTimesheet Detail` where parent=%s and task=%s """,(timesheets,k.task),as_dict=True)
#                 extra_status=frappe.db.get_value("Task",{"name":k.task},["status"])
#                 e_tasks.append({
#                         "id": k.task,
#                         "at_taken": t,
#                         'status': extra_status,
#                         'cb':emp_shortcode
#                     })
#                 appended_tasks.add(k.task)  
#     issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheets, 'custom_issue': ['!=', '']}, fields=['*'])
#     for issue in issue_logs:
#         if issue.custom_issue not in appended_issues:
#             short_code=frappe.db.get_value("Employee",{'name':emp},['short_code'])
#             prior = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['priority'])
#             i_id = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['status'])
#             issues.append({
#                 "id": issue.custom_issue,
#                 "at_taken": issue.hours,
#                 'project_name': issue.project_name,
#                 'subject': issue.custom_subject_issue,
#                 'status': i_id,
#                 'cb':short_code,
#                 'priority':prior
#             })
#             appended_issues.add(issue.custom_issue)            
#     meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheets, 'custom_meeting': ['!=', '']}, fields=['*'])
#     for meeting in meeting_logs:
#         if meeting.custom_meeting not in appended_meetings:
#             m_id = frappe.db.get_value("Issue", {'name': meeting.custom_meeting}, ['status'])
#             short_code=frappe.db.get_value("Employee",{'name':emp},['short_code'])
#             meetings.append({
#                 "id": meeting.custom_meeting,
#                 "at_taken": meeting.hours,
#                 'subject':meeting.custom_subject_meeting,
#                 'cb':short_code 
#             })
#             appended_meetings.add(meeting.custom_meeting)  
#     for d in issues:
#         parent_doc.append("task_details", d)
#     for meeting in meetings:
#         parent_doc.append("task_details", meeting)
#     for h in e_tasks:
#         parent_doc.append("task_details", h)
#     parent_doc.save()
#     frappe.db.commit()

