# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days

class DailyMonitor(Document):
    
    def validate(self):
        if self.service == "IT-SW" and self.task_type == "OPS":
            # Update TL Remaks in tasks
            for task_d in self.task_details:
                if task_d.tl_remark:
                    frappe.db.set_value('Task',task_d.id,'custom_tl__remarks',task_d.tl_remark)
            # Step 1: Group RTs by CB
            cb_rt_map = {}
            for row in self.task_details:
                if row.cb:
                    cb_rt_map.setdefault(row.cb, 0)
                    cb_rt_map[row.cb] += row.rt or 0

            # Step 2: Clear existing summary table
            self.set("dm_summary", [])

            # Step 3: Populate summary table with calculated values
            for cb, total_rt in cb_rt_map.items():
                actual_aph = 8  # You can later make this dynamic if needed
                percent = (float(total_rt) / float(actual_aph)) * 100

                self.append("dm_summary", {
                    "d_cb": cb,
                    "d_aph": actual_aph,
                    "d_rt": total_rt,
                    "d_actual_time_taken": "",  # Fill later if needed
                    "rt_vs_aph_": round(percent, 2),
                    "allocated": 0  # Fill later if needed
                })
                
        if self.dm_status == "DPR Pending" and self.task_details:
            if self.service == "IT-SW" and self.task_type == "OPS":
                
                for row in self.task_details:
                    row.rt = frappe.db.get_value("Task",{"name":row.id},['rt']) 
                

    # pass
@frappe.whitelist()
def get_allocated_tasks_for_it_cs(date,name,service,type):
    total=0
    percent=0
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details=[]
    parent_doc.dm_summary=[]
    issue_id=''
    issue_id_cs=''
    spoc_set=set()
    # task_det=''
    if type == "OPS":
        task_id=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type},['*'],order_by='cb asc, project asc, priority asc')
        task_det=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
        joint_task=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":"Joint","status":"Working"},['*'],order_by='cb asc, project asc, priority asc')
        for i in task_id:
            parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":i.cb})
            employee_id=frappe.db.get_value('Employee',{'short_code':i.cb},['user_id'])
            issue_id=frappe.db.get_all("Issue",{'assigned_to':employee_id,'status':'Open'},['*'])
            frappe.db.set_value("Task",i.name,"allocated",1)
        for joint in joint_task:
            parent_doc.append("task_details", {"id": joint.name,"a_task_type":joint.type,"cb":joint.cb})
        for j in issue_id:
            issue_list=frappe.db.get_value("Employee",{'user_id':j.assigned_to},['short_code'])
            parent_doc.append("task_details", {"id": j.name,"project_name":j.project,"subject":j.subject,"cb":issue_list,"status":j.status})
        for k in task_det:
            actual_aph=frappe.db.get_value('Employee',{'short_code':k.cb},['custom_aph'])
            # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(k.custom_allocated_to,date), as_dict=True)
            sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by custom_allocated_to""",(k.custom_allocated_to,date), as_dict=True)
            allocated_count=frappe.db.count("Task",{"custom_allocated_to":k.custom_allocated_to,"custom_production_date":date,"type":"OPS","status":"Working","allocated":1})
            emp_cb=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['short_code'])
            # total=sum_et[0].et
            if sum_et[0].et:
                if actual_aph is not None:
                    percent=(float(sum_et[0].et)/float(actual_aph))*100
                    parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph or '8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0','allocated':allocated_count})
                else:
                    percent=(float(sum_et[0].et)/8)*100
                    parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':'8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0','allocated':allocated_count})
    elif type == "CS":
        task_det=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type,"status":("in",["Working","Pending Review"])},['*'],order_by='spoc asc',group_by='spoc asc')
        task_id_cs=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type,"status":("in",["Working","Pending Review"])},['*'],order_by='spoc asc, project asc, priority asc')
        joint_task=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":"Joint","status":("in",["Working","Pending Review"])},['*'],order_by='spoc asc, project asc, priority asc')

        for i in task_id_cs:
            parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":i.cb})
            spoc_set.add(i.spoc)
        for joint in joint_task:
            parent_doc.append("task_details", {"id": joint.name,"a_task_type":joint.type,"cb":joint.cb})
        for j in spoc_set:
            cb=frappe.db.get_value("Employee",{'user_id':j},['short_code'])
            if frappe.db.exists("Issue",{"assigned_to":j,"custom_issue_status":"Working"}):
                issue_list=frappe.db.get_all("Issue",{"assigned_to":j,"custom_issue_status":"Working"},["*"])
                for issue in issue_list:
                    parent_doc.append("task_details", {"id": issue.name,"project_name":issue.project,"subject":issue.subject,"cb":cb,"status":issue.custom_issue_status})
        for k in task_det:
            emp_shortcode=frappe.db.get_value("Employee",{"user_id":k.spoc},["short_code"])
            actual_aph=frappe.db.get_value('Employee',{'short_code':emp_shortcode},['custom_aph'])
            # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(k.custom_allocated_to,date), as_dict=True)
            sum_et=frappe.db.sql("""select sum(pr_expected_time) as et from `tabTask` where spoc=%s and custom_production_date=%s and type='CS' and status!="Client Review" group by spoc""",(k.spoc,date), as_dict=True)
            if sum_et is not None:
                if actual_aph is not None:
                    percent=(float(sum_et[0].et)/float(actual_aph))*100
                    parent_doc.append("dm_summary",{'d_cb':emp_shortcode,'d_aph':actual_aph or '8','d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or'0'})
                else:
                    # percent=(float(sum_et[0].et)/8)*100
                    parent_doc.append("dm_summary",{'d_cb':emp_shortcode,'d_aph':'8','d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0'})
    # parent_doc.dm_status="DPR Pending"
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")

# @frappe.whitelist()
# def rec_allocated_tasks(name,service,date):
#     task_id=frappe.db.get_all("Task",{"service":service,"custom_production_date":date},['*'],order_by='custom_allocated_to asc')
#     parent_doc = frappe.get_doc("Daily Monitor", name)
#     parent_doc.dm_rec_task_details=[]
#     for i in task_id:
#             parent_doc.append("dm_rec_task_details", {"id": i.name})
#     # parent_doc.dm_status="DPR Pending"
#     parent_doc.save()
#     frappe.db.commit()
#     frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")
@frappe.whitelist()
def rec_allocated_tasks(name, service, date):
    tasks = frappe.db.get_all(
        "Task",
        filters={"service": service, "custom_production_date": date},
        fields=["*"],
        order_by="custom_allocated_to asc"
    )
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.dm_rec_task_details = []
    for task in tasks:
        task_doc = frappe.get_doc("Task", task["name"]) 
        if task_doc.custom_assign_task:
            for assign in task_doc.custom_assign_task:
                parent_doc.append(
                    "dm_rec_task_details",
                    {
                        "id": task_doc.name,
                        "allocated_to": assign.assigned_to
                    }
                )
        else:
            parent_doc.append(
                    "dm_rec_task_details",
                    {
                        "id": task_doc.name,
                    }
                )
    parent_doc.dm_status = "DPR Pending"
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor", name, "dm_status", "DPR Pending")

    
@frappe.whitelist()
def dnd_allocated_tasks(name,date):
    dnd_details=frappe.db.get_all("Closure",{"custom_next_follow_up_on":date,"status":("not in",["Dropped","Onboarded"])})
    parent_doc=frappe.get_doc("Daily Monitor",name)
    parent_doc.dnd_summary=[]
    for i in dnd_details:
        parent_doc.append("dnd_summary", {"id": i.name})
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
    cs_task = frappe.db.get_all("Task", {"custom_production_date":date,"type":task_type,"service":service,"status":("in",["Working","Pending Review"])}, ['*'], order_by='spoc asc',group_by='spoc asc')
    # cs_task = frappe.db.get_all("Task", {"custom_production_date":date,"type":task_type,"service":service}, ['*'], order_by='spoc asc',group_by='spoc asc')    
    total_at=0
    or_total=0
    pr_total=0
    pr_count=0
    or_count=0
    if task_data.dsr_check==1:
        if task_type =="OPS":
            count=1
            sum_et=0
            pr=0
            working=0
            allocated=0
            aph_totals=0
            total_allocated=0
            total_pr=0
            total_working=0
            un_allocated=0
            total_unallocated=0
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
                <td style='width:1%'><b>Allocated</b></td>
                <td style='width:1%'><b>Un Allocated</b></td>
                <td style='width:1%'><b>PR</b></td>
                <td style='width:1%'><b>Working</b></td>
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
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(j.custom_allocated_to,date), as_dict=True)                
                for datas in task_data.dm_summary:
                    if datas.d_cb == emp_cb:
                        sum_et=datas.d_rt
                        pr=datas.pr
                        working=datas.working
                        allocated=datas.allocated
                        un_allocated=datas.un_allocated
                # if sum_et:
                #     total+=sum_et[0].et
                total_allocated+=allocated
                total_pr+=pr
                total_working+=working
                total_unallocated+=un_allocated
                if sum_et:
                    total+=float(sum_et)
                if actual_aph is not None:
                    aph_totals+=float(actual_aph)
                if timesheet is not None:
                    total_at+=float(timesheet)
                if actual_aph and timesheet:
                    percent=(float(sum_et)/float(actual_aph))*100
                    value=actual_aph
                    total_count=float(total)/float(aph_totals)*100
                    or_count=float(timesheet)/float(value)*100
                    # pr_count=float(sum_et[0].et)/float(timesheet)*100
                    pr_count=float(sum_et)/float(timesheet)*100
                    or_total=float(total_at)/float(aph_totals)*100
                    pr_total=float(total)/float(total_at)*100
                if percent:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et if sum_et else '0',round(timesheet,2) if timesheet is not None else '0',allocated if allocated else '0',un_allocated if un_allocated else '0',pr if pr else '0',working if working else '0',round(percent) if timesheet is not None else '0',round(or_count) if timesheet is not None else '0',round(pr_count) if timesheet is not None else '0')
                else:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et if sum_et else '0',round(timesheet,2) if timesheet is not None else'0',allocated if allocated else '0',un_allocated if un_allocated else '0',pr if pr else '0',working if working else '0','0',round(or_count,2) or '0',round(pr_count,2) or '0')
            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_totals,total,round(total_at,2),total_allocated,total_unallocated,total_pr,total_working,round(total_count),round(or_total),round(pr_total))
            table += "</table>"
            
            
            frappe.sendmail(
                    sender='abdulla.pi@groupteampro.com',
                    recipients=recievers,
                    cc='abdulla.pi@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    subject = f'{service} - {task_type} DSR {formatted_date} -Reg',
                    message = """
                <b>Dear Team,</b><br><br>
                    Please find the below DSR for {} for your kind reference.<br><br>
                    {}<br><br>
                    {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,table if task_data.dm_summary else '',data)
                )
            frappe.msgprint("DSR mail has been successfully sent.")
            task_data.dm_status='Submitted'
            task_data.dsr_submitted_on=today()
            task_data.save()
            frappe.db.commit()
            # frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
            # frappe.db.set_value("Daily Monitor",name,'dsr_submitted_on',today())
        elif task_type =="CS":
            sum_et=0
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
            table = '<table border="1" width="70%" style="border-collapse: collapse;text-align:center;">'
            table += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:1%'><b>SPOC</b></td>
                <td style='width:1%'><b>APH</b></td>
                <td style='width:1%'><b>RT</b></td>
                <td style='width:1%'><b>Actual Time Taken</b></td>
                <td style='width:1%'><b>RT Vs APH %</b></td>
                <td style='width:1%'><b>PR</b></td>
                <td style='width:1%'><b>Working</b></td>
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
                data += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'% (count,id, i.project_name, i.subject, i.cb, i.status, i.revisions,i.priority, i.allocated_on, today_taken, remark, tl_remark)
                count += 1
            data += '</table>'
            pending_count_total=0
            working_total=0
            for j in cs_task:
                employee_id=frappe.db.get_value('Employee',{'user_id':j.spoc},['name'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':j.spoc},['short_code'])
                timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])  
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and service="IT-SW" group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by cb""",(j.custom_allocated_to,date), as_dict=True)                
                pending_review_count=frappe.db.count("Task",{"custom_production_date":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Pending Review"})
                working_count=frappe.db.count("Task",{"custom_production_date":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Working"})
                pending_count_total+=float(pending_review_count)
                working_total+=float(working_count)
                for datas in task_data.dm_summary:
                    if datas.d_cb == emp_cb:
                        sum_et=datas.d_rt
                # if sum_et:
                #     total+=sum_et[0].et
                if sum_et:
                    total+=float(sum_et)

                if actual_aph:
                    aph_totals+=float(actual_aph)
                if timesheet is not None:
                    total_at+=float(timesheet)
                # or_total=float(total_at)/float(aph_totals)*100
                # pr_total=float(total)/float(total_at)*100
                if actual_aph and timesheet:
                    percent=(float(sum_et)/float(actual_aph))*100
                    value=actual_aph
                    # total_count=float(total)/float(aph_totals)*100
                    or_count=float(timesheet)/float(value)*100
                    # pr_count=float(sum_et)/float(timesheet)*100

                    # or_total=float(total_at)/float(aph_totals)*100
                    # pr_total=float(total)/float(total_at)*100
                if timesheet and sum_et is not None:
                    pr_count=float(sum_et)/float(timesheet)*100

                if total_at:
                    or_total=float(total_at)/float(aph_totals)*100
                    pr_total=float(total)/float(total_at)*100
                if aph_totals!=0:
                    total_count=float(total)/float(aph_totals)*100
                if percent:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et if sum_et else '0',round(timesheet,2) if timesheet is not None else '0',round(percent) if timesheet is not None else '0',pending_review_count,working_count,round(or_count) if timesheet is not None else '0',round(pr_count) if timesheet is not None else '0')
                else:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et if sum_et else '0',round(timesheet,2) if timesheet is not None else'0','0',pending_review_count,working_count,round(or_count,2) or '0',round(pr_count,2) or '0')
            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_totals,total,round(total_at,2),round(total_count),pending_count_total,working_total,round(or_total),round(pr_total))
            table += "</table>"
            frappe.sendmail(
                    sender='sarath.v@groupteampro.com',
                    # recipients=['divya.p@groupteampro.com',"siva.m@groupteampro.com"],
                    recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
                    cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
                    subject = f'{service} - {task_type} DSR {formatted_date} -Reg',
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
            task_data.dm_status='Submitted'
            task_data.dsr_submitted_on=today()
            task_data.save()
            frappe.db.commit()
            # frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
            # frappe.db.set_value("Daily Monitor",name,'dsr_submitted_on',today())
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
            # table+='''<tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
            #     <td style='width:1%' colspan=4><b>TODO</b></td></tr>
            #     <tr><td style='width:1%'>EXE<b></b></td>
            #     <td style='width:1%'><b>ID</b></td>
            #     <td style='width:1%'><b>Subject</b></td>
            #     <td style='width:1%'><b>Status</b></td>
            # </tr>
            # '''
            # for user in recievers:
            #     todo_list=frappe.db.get_all("Todo",{"allocated_to":user,"custom_production_date":date,"status":"Open"},["*"])
            #     cb=frappe.db.get_value("Employee",{"user_id":user},["short_code"])
            #     for todo in todo_list:
            #         table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(cb,todo.name,todo.custom_subject,todo.status)


            task_det=frappe.db.get_all("Task",{"custom_production_date":date,"type":task_type,"service":service},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
            for k in task_det:
                employee_id=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['user_id'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['short_code'])
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                sum_rt=frappe.db.sql("""select sum(rt) as rt from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and type='OPS' group by custom_allocated_to""",(k.custom_allocated_to,date), as_dict=True)
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
            table+='''<tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:1%' colspan=4><b>TODO</b></td></tr>
                <tr><td style='width:1%'><b>EXE<b></b></td>
                <td style='width:1%'><b>ID</b></td>
                <td style='width:1%'><b>Subject</b></td>
                <td style='width:1%'><b>Status</b></td>
            </tr>
            '''
            for user in recievers:
                todo_list=frappe.db.get_all("ToDo",{"allocated_to":user,"custom_production_date":date,"status":"Open"},["*"])
                cb=frappe.db.get_value("Employee",{"user_id":user},["short_code"])
                for todo in todo_list:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(cb,todo.name,todo.custom_subject,todo.status)
            table+='</table>'
            
            frappe.sendmail(
                    sender='abdulla.pi@groupteampro.com',
                    recipients=recievers,
                    # recipients='jenisha.p@groupteampro.com',
                    subject = f'{service} - {task_type} DPR {formatted_date} -Reg',
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
            task_data.dm_status='DPR Completed'
            task_data.dpr_submitted_on=today()
            task_data.save()
            frappe.db.commit()
            # frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
            # frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())
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
            table = '<table border="1" width="50%" style="border-collapse: collapse;text-align:center;">'
            table += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:3%'><b>SPOC</b></td>
                <td style='width:3%'><b>APH</b></td>
                <td style='width:3%'><b>RT</b></td>
                <td style='width:8%'><b>RT Vs APH %</b></td>
                <td style='width:3%'><b>PR</b></td>
                <td style='width:3%'><b>Working</b></td>
            </tr>
            '''
            task_det=frappe.db.get_all("Task",{"custom_production_date":date,"type":task_type,"service":service,"status":("in",["Working","Pending Review"])},['*'],order_by='spoc asc',group_by='spoc asc')
            value=0
            pending_total=0
            working_total=0
            for k in task_det:
                employee_id=frappe.db.get_value('Employee',{'user_id':k.spoc},['user_id'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':k.spoc},['short_code'])
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                sum_rt=frappe.db.sql("""select sum(pr_expected_time) as rt from `tabTask` where spoc=%s and custom_production_date=%s and type='CS' and status!="Client Review" group by spoc""",(k.spoc,date), as_dict=True)
                pr_count=frappe.db.count("Task",{"custom_production_date":date,"type":task_type,"service":service,"spoc":k.spoc,"status":"Pending Review"})
                working_count=frappe.db.count("Task",{"custom_production_date":date,"type":task_type,"service":service,"spoc":k.spoc,"status":"Working"})
                # # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and service="IT-SW" group by custom_allocated_to""",(k.custom_allocated_to,date), as_dict=True)

                pending_total+=float(pr_count)
                working_total+=float(working_count)
                if sum_rt:
                    total+=sum_rt[0].rt
                if actual_aph is not None:
                    value=actual_aph
                    aph_total+=float(value)
                if sum_rt and actual_aph is not None:
                    total_count=float(total)/float(aph_total)*100
                    percent=(float(sum_rt[0].rt)/float(actual_aph))*100
                # # print(employee_id)
                if percent:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,value or '8',sum_rt[0].rt if sum_rt else '0',round(percent,2) or '-',pr_count or '0',working_count or '0')
                else:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '',sum_rt[0].rt if sum_rt else '0',round(percent,2) or '-',pr_count or '0',working_count or '0')
            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_total,round(total,2) if total else '0',round(total_count,2) if total_count else '0',round(pending_total,2) if pending_total else '0',round(working_total,2) if working_total else '0')
            table+='</table>'
            frappe.sendmail(
                    sender='sarath.v@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    # recipients=['divya.p@groupteampro.com',"siva.m@groupteampro.com"],
                    recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
                    cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
                    subject = f'{service} - {task_type} DPR {formatted_date} -Reg',
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
            task_data.dm_status='DPR Completed'
            task_data.dpr_submitted_on=today()
            task_data.save()
            frappe.db.commit()
            # frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
            # frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())

@frappe.whitelist()
def update_rec_dpr(date,name,service):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00003','user_id':('not in',['chitra.g@groupteampro.com','keerthana.k@groupteampro.com','narendharan.k@groupteampro.com'])},['*'])
    recievers=[]
    for i in emp:
        recievers.append(i.user_id)
    
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
                    sender='sangeetha.a@groupteampro.com',
                    recipients='sangeetha.a@groupteampro.com',
                    cc=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','aruna.g@groupteampro.com','lokeshkumar.a@groupteampro.com',"prabhu.m@groupteampro.com"],
                    # recipients='divya.p@groupteampro.com',
                    subject = f'{service} DSR {formatted_date} -Reg',
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DSR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        frappe.msgprint("DSR mail has been successfully sent")
        parent_doc.dm_status='Submitted'
        parent_doc.dsr_submitted_on=today()
        parent_doc.save()
        frappe.db.commit()
        # frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
        # frappe.db.set_value('Daily Monitor',name,'dsr_submitted_on',today())
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
                    # recipients=recievers,
                    recipients=['sangeetha.a@groupteampro.com'],
                    cc=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','aruna.g@groupteampro.com','lokeshkumar.a@groupteampro.com',"prabhu.m@groupteampro.com"],
                    # recipients='divya.p@groupteampro.com',
                    subject = f'{service} DPR {formatted_date} -Reg',
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DPR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        task_group = {}
        for task in parent_doc.dm_rec_task_details:
            if task.allocated_to not in task_group:
                task_group[task.allocated_to] = []
            task_group[task.allocated_to].append(task)
        for allocated_to, tasks in task_group.items():
            task_data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            task_data += '''
            <tr style="background-color: #0f1568; text-align:center; color:white;">
                <td style='width:5%'><b>SI NO</b></td>
                <td style='width:10%'><b>ID</b></td>
                <td style='width:15%'><b>Project</b></td>
                <td style='width:20%'><b>Subject</b></td>
                <td style='width:10%'><b>Status</b></td>
                <td style='width:7%'><b>Priority</b></td>
                <td style='width:13%'><b>RC</b></td>
            </tr>
            '''
            individual_count = 1
            for j in tasks:
                task_data += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                    individual_count, j.id, j.project_name or '-', j.subject, j.status, j.priority, j.rc or '-')
                individual_count += 1
            task_data += '</table>'
            if allocated_to:
                frappe.sendmail(
                    sender='sangeetha.a@groupteampro.com',
                    recipients=allocated_to,  # Send to the allocated user
                    subject=f'{service} Task DPR {formatted_date} - Reg',
                    message="""
                    <b>Dear Team</b>,<br><br>
                    Please find your assigned task for {}.<br><br>
                    {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date, task_data)
                )
        frappe.msgprint("DPR mail has been successfully sent")
        parent_doc.dm_status='DPR Completed'
        parent_doc.dpr_submitted_on=today()
        parent_doc.save()
        frappe.db.commit()
        # frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
        # frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())
        
        
        
@frappe.whitelist()
def update_dsr_cs_it(date, name,service,type):
    parent_doc = frappe.get_doc("Daily Monitor",name)
    parent_doc.task_details = []
    issues = []
    meetings = []
    tasks = []
    if type == "OPS":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list=frappe.get_all("Employee",{'department':"IT. Development - THIS",'custom_dept_type':'OPS'},['short_code','name'])
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
                        sum_issue=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_issue=%s AND employee=%s AND start_date=%s""",(issue.custom_issue,emp.name,date), as_dict=True)

                        issues.append({
                            "id": issue.custom_issue,
                            # "at_taken": issue.hours,
                            "at_taken": sum_issue[0]['sum(cs.hours)'],
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
                        sum_meeting=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_meeting=%s AND employee=%s AND start_date=%s""",(meeting.custom_meeting,emp.name,date), as_dict=True)
                        meetings.append({
                            "id": meeting.custom_meeting,
                            "at_taken": sum_meeting[0]['sum(cs.hours)'],
                            'subject':meeting.custom_subject_meeting,
                            'cb':short_code,
                            'status':m_id
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
                        sum_task=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s AND start_date=%s""",(log.task,emp.name,date), as_dict=True)                                 
                        if log.activity_type=="Code Review":
                            tasks.append({
                                "id": log.task,
                                "at_taken":sum_task[0]['sum(cs.hours)'],
                                # "at_taken": log.hours,
                                "cb":short_code,
                                "current_status":t_id,
                                'rt':0
                            })
                        else:    
                            
                            tasks.append({
                                "id": log.task,
                                "at_taken":sum_task[0]['sum(cs.hours)'],
                                # "at_taken": log.hours,
                                "cb":short_code,
                                "current_status":t_id,
                                "rt": frappe.db.get_value("Task",{'name':log.task},['rt'])
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
                    "current_status":task.status,
                    "rt": frappe.db.get_value("Task",{'name':task.name},['rt'])
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
                sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s  group by cb""",(j.custom_allocated_to,date), as_dict=True)
                pr_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_pr_date":date})
                # un_allocated_count=frappe.db.sql("""select count(name) from `tabTask` where custom_allocated_to=%s and  allocated=0 and custom_pr_date=%s or custom_allocated_on=%s""",(j.custom_allocated_to,date,date))
                un_allocated_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_allocated_on":date,"allocated":0})
                extra_unallocated_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_allocated_on":('!=',date),"allocated":0,"custom_pr_date":date})
                working_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_production_date":date,"status":"Working"})
                if timesheet and actual_aph is not None:
                    percent=(float(timesheet)/float(actual_aph))*100
                    for data in parent_doc.dm_summary:
                        if data.d_cb == emp_cb:
                            data.d_aph=actual_aph
                            data.d_actual_time_taken=round(timesheet,2)
                            data.pr=pr_count
                            data.working=working_count
                            data.un_allocated=un_allocated_count + extra_unallocated_count
                #     parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':round(timesheet,2),'rt_vs_aph_':round(percent,2)})
                else:
                    for datas in parent_doc.dm_summary:
                        if datas.d_cb == emp_cb:
                            datas.d_aph=actual_aph
                            datas.d_actual_time_taken=0
                            datas.pr=pr_count
                            datas.working=working_count
                            datas.un_allocated=un_allocated_count + extra_unallocated_count
                #     parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0' ,'d_actual_time_taken':'0','rt_vs_aph_':'0'})
    elif type == "CS":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list=frappe.get_all("Employee",{'custom_dept_type':'CS'},['short_code','name'])
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
                        prior = frappe.db.get_value("Issue", {'custom_production_date':date,'name': issue.custom_issue}, ['priority'])
                        i_id = frappe.db.get_value("Issue", {'custom_production_date':date,'name': issue.custom_issue}, ['status'])
                        sum_issue=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_issue=%s AND employee=%s AND start_date=%s""",(issue.custom_issue,emp.name,date), as_dict=True)

                        issues.append({
                            "id": issue.custom_issue,
                            # "at_taken": issue.hours,
                            "at_taken": sum_issue[0]['sum(cs.hours)'],
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
                        sum_meeting=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_meeting=%s AND employee=%s AND start_date=%s""",(meeting.custom_meeting,emp.name,date), as_dict=True)
                        meetings.append({
                            "id": meeting.custom_meeting,
                            # "at_taken": meeting.hours,
                            "at_taken": sum_meeting[0]['sum(cs.hours)'],
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
                        sum_task=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s AND start_date=%s""",(log.task,emp.name,date), as_dict=True)
                        tasks.append({
                        "id": log.task,
                        # "at_taken": log.hours,
                        "at_taken":sum_task[0]['sum(cs.hours)'],
                        # "a_task_type":task.type,
                        "cb":short_code,
                        "current_status":t_id
                        })
                        appended_tasks.add(log.task)        
        # task_id_list = frappe.db.get_all("Task", {"custom_production_date": date,"service":service,"type":type}, ['*'], order_by='cb asc, project asc, priority asc',group_by='cb')
        # for task in task_id_list:
        #     emp_id = frappe.db.get_value("Employee", {'short_code': task.cb}, ['name'])
        #     emp_short_code= frappe.db.get_value("Employee", {'name': emp_id},['short_code'])
            
        task_id_lists = frappe.db.get_all("Task", {"custom_production_date": date,"service":service,"type":type,"status":("in",["Working","Pending Review"])}, ['*'], order_by='cb asc, project asc, priority asc')
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
        task_list = frappe.db.get_all("Task", {"custom_production_date":date,"type":type,"service":service,"status":("in",["Working","Pending Review"])}, ['*'], order_by='cb asc',group_by='cb asc')
        for j in task_list:
            employee_id=frappe.db.get_value('Employee',{'user_id':j.spoc},['name'])
            emp_cb=frappe.db.get_value('Employee',{'user_id':j.spoc},['short_code'])
            timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])      
            actual_aph=frappe.db.get_value('Employee',{'name':employee_id},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(pr_expected_time) as et from `tabTask` where cb=%s and cb=%s group by cb""",(j.cb,date), as_dict=True)
            # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s  group by cb""",(j.custom_allocated_to,date), as_dict=True)
            if timesheet and actual_aph is not None:
                percent=(float(timesheet)/float(actual_aph))*100
                for data in parent_doc.dm_summary:
                    if data.d_cb == emp_cb:
                        data.d_aph=actual_aph
                        data.d_actual_time_taken=round(timesheet,2)
            #     parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':round(timesheet,2),'rt_vs_aph_':round(percent,2)})
            else:
                for n in parent_doc.dm_summary:
                    if n.d_cb == emp_cb:
                        n.d_aph=actual_aph
                        n.d_actual_time_taken=0
    parent_doc.dm_status='DSR Pending'
    parent_doc.save()
    frappe.db.commit()
    # frappe.db.set_value('Daily Monitor',name,'dm_status','DSR Pending')


@frappe.whitelist()
def rec_update_dsr(name,date):
    parent_doc = frappe.get_doc("Daily Monitor",name)
    task_ids = set()
    for j in parent_doc.dm_rec_task_details:
        candidate_count = frappe.db.sql("""
        SELECT COUNT(DISTINCT c.name) AS status_count
        FROM `tabCandidate` c
        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE DATE(cs.sourced_date) = %s
        AND cs.sourced_by = %s 
        AND c.candidate_created_by=%s 
        AND cs.task = %s
        AND cs.status IN (%s, %s)
        """, (date, j.allocated_to,j.allocated_to,j.id,"Submitted(Client)","Submit(SPOC)"))

        j.actual_count = candidate_count[0][0] if candidate_count else 0  
        j.current_status = frappe.db.get_value("Task", {"name": j.id}, "status")
        task_ids.add((j.id, j.allocated_to))  
    candidate_tasks = frappe.db.sql("""
        SELECT cs.task, c.candidate_created_by
        FROM `tabCandidate` c
        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE DATE(cs.sourced_date) = %s
        AND cs.status IN (%s, %s)
    """, (date,"Submitted(Client)","Submit(SPOC)"))

    for i in candidate_tasks:
        task_id = i[0]  
        owner = i[1]   

        if (task_id, owner) not in task_ids:
            add_count = frappe.db.sql("""
                SELECT COUNT(DISTINCT c.name) AS status_count
                FROM `tabCandidate` c
                INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                WHERE DATE(cs.sourced_date) = %s
                AND cs.sourced_by = %s
                AND c.candidate_created_by=%s
                AND cs.task = %s
                AND cs.status IN (%s, %s)
            """, (date, owner,owner, task_id, "Submitted(Client)","Submit(SPOC)"))

            add_count_value = add_count[0][0] if add_count else 0
            if add_count_value>0:
                parent_doc.append("dm_rec_task_details", {
                    "id": task_id,
                    "allocated_to": owner,
                    "actual_count": add_count_value
                })
                task_ids.add((task_id, owner))  
    parent_doc.dm_status='DSR Pending'
    parent_doc.dsr_check = 1
    parent_doc.save()
    frappe.db.commit()

# @frappe.whitelist()
# def rec_update_dsr(name, date):
#     parent_doc = frappe.get_doc("Daily Monitor", name)
#     task_ids = set()  # To track already processed tasks (task_id, allocated_to)
#     existing_task_ids = set()  # Track existing (task_id, allocated_to) pairs from the child table

#     # Add existing task ids from the child table to existing_task_ids
#     for j in parent_doc.dm_rec_task_details:
#         existing_task_ids.add((j.id, j.allocated_to))

#     # Iterate through each task detail in the child table
#     for j in parent_doc.dm_rec_task_details:
#         # Fetch all statuses for the task on the given date
#         task_statuses = frappe.db.sql("""
#             SELECT cs.status
#             FROM `tabCandidate status` cs
#             WHERE DATE(cs.sourced_date) = %s
#             AND cs.task = %s
#         """, (date, j.id))

#         # Flags to track status
#         valid_status_found = False
#         idb_found = False

#         # Iterate through the statuses and determine if we should count them
#         for i, status in enumerate(task_statuses):
#             status_value = status[0]  # Get the status value

#             if status_value == "IDB":
#                 idb_found = True  # Mark that IDB is found, but don't count it yet
#             elif status_value in ["Submitted(Internal)", "Submitted(Client)", "Submit(SPOC)", 
#                                    "Linedup", "QC Cleared", "Shortlisted"]:
#                 # If the valid status comes after IDB or if IDB is not found before, we count it
#                 if idb_found or not task_statuses[i-1][0] == "IDB":
#                     valid_status_found = True  # Mark that a valid status is found after IDB
#                     break  # Once we find a valid status, we can stop checking further statuses

#         # If we found a valid status after IDB or a valid status was found without IDB
#         if valid_status_found:
#             candidate_count = frappe.db.sql("""
#                 SELECT COUNT(DISTINCT c.name) AS status_count
#                 FROM `tabCandidate` c
#                 INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
#                 WHERE DATE(cs.sourced_date) = %s
#                 AND c.candidate_created_by = %s
#                 AND cs.task = %s
#                 AND cs.status IN (%s, %s, %s, %s, %s, %s)
#             """, (date, j.allocated_to, j.id, 
#                 "Submitted(Internal)", "Submitted(Client)", 
#                 "Submit(SPOC)", "Linedup", "QC Cleared", "Shortlisted"))

#             # Update the actual count if any valid status was found
#             j.actual_count = candidate_count[0][0] if candidate_count else 0
#         else:
#             # If the last status is IDB or no valid status after IDB, don't count it
#             j.actual_count = 0

#         task_ids.add((j.id, j.allocated_to))  # Track processed task ids

#     # Check for tasks that are not yet in the child table and append them
#     candidate_tasks = frappe.db.sql("""
#         SELECT cs.task, c.candidate_created_by
#         FROM `tabCandidate` c
#         INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
#         WHERE DATE(cs.sourced_date) = %s
#         AND cs.status IN (%s, %s, %s, %s, %s, %s)
#     """, (date, 
#             "Submitted(Internal)", "Submitted(Client)", 
#             "Submit(SPOC)", "Linedup", "QC Cleared", "Shortlisted"))

#     for i in candidate_tasks:
#         task_id = i[0]  # Task ID
#         owner = i[1]    # Candidate created_by (owner)

#         # Check if the task is already in the child table
#         if (task_id, owner) not in existing_task_ids:
#             # Get the count of candidates for this task and date, based on valid statuses
#             add_count = frappe.db.sql("""
#                 SELECT COUNT(DISTINCT c.name) AS status_count
#                 FROM `tabCandidate` c
#                 INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
#                 WHERE DATE(cs.sourced_date) = %s
#                 AND c.candidate_created_by = %s
#                 AND cs.task = %s
#                 AND cs.status IN (%s, %s, %s, %s, %s, %s)
#             """, (date, owner, task_id, 
#                 "Submitted(Internal)", "Submitted(Client)", 
#                 "Submit(SPOC)", "Linedup", "QC Cleared", "Shortlisted"))

#             # Get the count value from the query
#             add_count_value = add_count[0][0] if add_count else 0

#             # Append the new task details to the child table
#             parent_doc.append("dm_rec_task_details", {
#                 "id": task_id,
#                 "allocated_to": owner,
#                 "actual_count": add_count_value
#             })
#             existing_task_ids.add((task_id, owner))  # Add to existing_task_ids after appending

#     # Mark the DSR check as done
#     parent_doc.dsr_check = 1
#     parent_doc.save()
#     frappe.db.commit()

@frappe.whitelist()
def dnd_send_dpr_dsr(date,name):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    parent_doc = frappe.get_doc("Daily Monitor", name)
    if parent_doc.dsr_check==1:
        count=1

        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%'><b>SI NO</b></td>
            <td style='width:10%'><b>ID</b></td>
            <td style='width:15%'><b>Passport Number </b></td>
            <td style='width:20%'><b>Given Name/Surname</b></td>
            <td style='width:13%'><b>Status To</b></td>
            <td style='width:10%'><b>Customer Name</b></td>
            <td style='width:7%'><b>Position</b></td>
            <td style='width:13%'><b>Next Action</b></td>
            <td style='width:13%'><b>Next Action On</b></td>
            <td style='width:13%'><b>Remarks</b></td>
            <td style='width:13%'><b>Latest Remarks</b></td>
            <td style='width:13%'><b>Next Action</b></td>
            <td style='width:13%'><b>Next Action On</b></td>

        </b></tr>
        '''
        for i in parent_doc.dnd_summary:
            data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id ,i.passport_number or '-',i.given_namesurname,i.status,i.customer_name,i.position,i.next_action or '-',i.next_action_on or '-',i.remarks or '-',i.latest_remarks,i.latest_next_action,i.latest_next_action_on)
            count+=1
        data += '</table>'
        frappe.sendmail(
                    recipients='dc@groupteampro.com',
                    cc=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','aruna.g@groupteampro.com','lokeshkumar.a@groupteampro.com','sangeetha.a@groupteampro.com','keerthana.k@groupteampro.com'],
                    # recipients='divya.p@groupteampro.com',
                    subject = f'DND- DSR {formatted_date} -Reg',
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DSR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        frappe.msgprint("DSR mail has been successfully sent")
        parent_doc.dm_status='Submitted'
        parent_doc.dsr_submitted_on=today()
        parent_doc.save()
        frappe.db.commit()
    else:
        count=1
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%'><b>SI NO</b></td>
            <td style='width:10%'><b>ID</b></td>
            <td style='width:15%'><b>Passport Number </b></td>
            <td style='width:20%'><b>Given Name/Surname</b></td>
            <td style='width:13%'><b>Status To</b></td>
            <td style='width:10%'><b>Customer Name</b></td>
            <td style='width:7%'><b>Position</b></td>
            <td style='width:13%'><b>Next Action</b></td>
            <td style='width:15%'><b>Next Action On</b></td>
            <td style='width:20%'><b>Remarks</b></td>
        </b></tr>
        '''
        for i in parent_doc.dnd_summary:
            data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id ,i.passport_number or '-',i.given_namesurname,i.status,i.customer_name,i.position,i.next_action or '-',i.next_action_on or '-',i.remarks or '-')
            count+=1
        data += '</table>'
        frappe.sendmail(
                    recipients='dc@groupteampro.com',
                    cc=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','aruna.g@groupteampro.com','lokeshkumar.a@groupteampro.com','keerthana.k@groupteampro.com','sangeetha.a@groupteampro.com'],
                    # recipients=['divya.p@groupteampro.com'],
                    # cc='dineshbabu.k@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    subject = f'DND- DPR {formatted_date} -Reg',
                    message = """
                    <b>Dear Team,</b><br><br>
    Please find the below DPR for {} for your kind reference and action.<br><br>

                {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    
                    <i>This email has been automatically generated. Please do not reply</i>
                    """.format(formatted_date,data)
                )
        frappe.msgprint("DPR mail has been successfully sent")
        parent_doc.dm_status='DPR Completed'
        parent_doc.dpr_submitted_on=today()
        parent_doc.save()
        frappe.db.commit()

@frappe.whitelist()
def dnd_update_dsr(name, date):
    parent_doc = frappe.get_doc("Daily Monitor", name)
    existing_ids = {row.id for row in parent_doc.dnd_summary}
    for j in parent_doc.dnd_summary:
        j.latest_remarks = frappe.db.get_value("Closure", {"name": j.id}, "remark")
        j.latest_next_action = frappe.db.get_value("Closure", {"name": j.id}, "std_remarks")
        j.latest_next_action_on = frappe.db.get_value("Closure", {"name": j.id}, "custom_next_follow_up_on")
    add_taken = frappe.db.get_all(
        "Closure",
        filters={
            "next_action_modfied_date": date,
            "name": ["not in", list(existing_ids)]
        },
        fields=["name", "remark", "std_remarks", "custom_next_follow_up_on"]
    )
    for i in add_taken:
        parent_doc.append("dnd_summary", {
            "id": i["name"],
            "latest_remarks": i["remark"],
            "latest_next_action": i["std_remarks"],
            "latest_next_action_on": i["custom_next_follow_up_on"]
        })
    parent_doc.dsr_check = 1
    parent_doc.dm_status='DSR Pending'
    parent_doc.save()
    frappe.db.commit()

# @frappe.whitelist()
# def load_sprint_data(sprint, dev_team, name):
#     parent_doc = frappe.get_doc("Daily Monitor", name)
#     sprint_data = frappe.get_doc("Sprint", {"team": dev_team, "sprint_id": sprint})
#     if sprint_data and sprint_data.sprint_task:
#         for i in sprint_data.sprint_task:
#             parent_doc.append("task_details", {
#                 "id": i.task,
#                 "a_task_type": i.task_type,
#                 "cb": i.cb
#             })
#         parent_doc.dm_status="DPR Pending"
#         parent_doc.save()  
#         sprint_data.status = "Planned"
#         sprint_data.save()
#         frappe.db.commit() 

@frappe.whitelist()
def load_sprint_data(doc,method):
    if doc.service=="IT-SW" and doc.task_type=="OPS":
        sprint_data = frappe.get_doc("Sprint", {"team": doc.dev_team, "sprint_id": doc.sprint})
        if sprint_data and sprint_data.sprint_task:
            for i in sprint_data.sprint_task:
                doc.append("task_details", {
                    "id": i.task,
                    "a_task_type": i.task_type,
                    "cb": i.cb
                })
            doc.dm_status="DPR Pending"
            doc.save()  
            sprint_data.save()
            frappe.db.commit() 


def update_sprint_avl_time(doc, method):
    from collections import defaultdict

    # Group totals by cb
    grouped = defaultdict(lambda: {"allocated_hours": 0.0, "at_taken": 0.0})

    for row in doc.task_details:
        if row.cb:
            grouped[row.cb]["allocated_hours"] += float(row.today_rt or 0)
            grouped[row.cb]["at_taken"] += float(row.at_taken or 0)

    # Clear and rebuild sprint_avl_time
    
    doc.sprint_avl_time = []

    for cb, values in grouped.items():
        allocated = values["allocated_hours"]
        at = values["at_taken"]
        available = 5.0  if(frappe.db.get_value("Employee",{'short_code':cb},['custom_is_tl'])) else 6.0
        occupancy = (allocated / available * 100) if allocated else 0

        doc.append("sprint_avl_time", {
            "short_code": cb,
            "available_hours": available,
            "allocated_hours": allocated,
            "at_period": at,
            "occupancy": occupancy
        })


@frappe.whitelist()
@frappe.whitelist()
def update_dsr_cs_it_manual():
    date = '2025-06-17'
    name = 'DM-00708'
    service="IT-SW"
    type="OPS"
    parent_doc = frappe.get_doc("Daily Monitor",name)
    parent_doc.task_details = []
    issues = []
    meetings = []
    tasks = []
    if type == "OPS":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list=frappe.get_all("Employee",{'department':"IT. Development - THIS",'custom_dept_type':'OPS'},['short_code','name'])
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
                        sum_issue=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_issue=%s AND employee=%s AND start_date=%s""",(issue.custom_issue,emp.name,date), as_dict=True)

                        issues.append({
                            "id": issue.custom_issue,
                            # "at_taken": issue.hours,
                            "at_taken": sum_issue[0]['sum(cs.hours)'],
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
                        sum_meeting=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_meeting=%s AND employee=%s AND start_date=%s""",(meeting.custom_meeting,emp.name,date), as_dict=True)
                        meetings.append({
                            "id": meeting.custom_meeting,
                            "at_taken": sum_meeting[0]['sum(cs.hours)'],
                            'subject':meeting.custom_subject_meeting,
                            'cb':short_code,
                            'status':m_id
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
                        sum_task=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s AND start_date=%s""",(log.task,emp.name,date), as_dict=True)                                 
                        if log.activity_type=="Code Review":
                            tasks.append({
                                "id": log.task,
                                "at_taken":sum_task[0]['sum(cs.hours)'],
                                # "at_taken": log.hours,
                                "cb":short_code,
                                "current_status":t_id,
                                'rt':0
                            })
                        else:    
                            
                            tasks.append({
                                "id": log.task,
                                "at_taken":sum_task[0]['sum(cs.hours)'],
                                # "at_taken": log.hours,
                                "cb":short_code,
                                "current_status":t_id,
                                "rt": frappe.db.get_value("Task",{'name':log.task},['rt'])
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
                    "current_status":task.status,
                    "rt": frappe.db.get_value("Task",{'name':task.name},['rt'])
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
                sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s  group by cb""",(j.custom_allocated_to,date), as_dict=True)
                pr_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_pr_date":date})
                # un_allocated_count=frappe.db.sql("""select count(name) from `tabTask` where custom_allocated_to=%s and  allocated=0 and custom_pr_date=%s or custom_allocated_on=%s""",(j.custom_allocated_to,date,date))
                un_allocated_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_allocated_on":date,"allocated":0})
                extra_unallocated_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_allocated_on":('!=',date),"allocated":0,"custom_pr_date":date})
                working_count=frappe.db.count("Task",{"custom_allocated_to":j.custom_allocated_to,"custom_production_date":date,"status":"Working"})
                if timesheet and actual_aph is not None:
                    percent=(float(timesheet)/float(actual_aph))*100
                    for data in parent_doc.dm_summary:
                        if data.d_cb == emp_cb:
                            data.d_aph=actual_aph
                            data.d_actual_time_taken=round(timesheet,2)
                            data.pr=pr_count
                            data.working=working_count
                            data.un_allocated=un_allocated_count + extra_unallocated_count
                #     parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':round(timesheet,2),'rt_vs_aph_':round(percent,2)})
                else:
                    for datas in parent_doc.dm_summary:
                        if datas.d_cb == emp_cb:
                            datas.d_aph=actual_aph
                            datas.d_actual_time_taken=0
                            datas.pr=pr_count
                            datas.working=working_count
                            datas.un_allocated=un_allocated_count + extra_unallocated_count
                #     parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0' ,'d_actual_time_taken':'0','rt_vs_aph_':'0'})
    elif type == "CS":
        appended_issues = set()
        appended_meetings = set()
        appended_tasks = set()
        employee_list=frappe.get_all("Employee",{'custom_dept_type':'CS'},['short_code','name'])
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
                        prior = frappe.db.get_value("Issue", {'custom_production_date':date,'name': issue.custom_issue}, ['priority'])
                        i_id = frappe.db.get_value("Issue", {'custom_production_date':date,'name': issue.custom_issue}, ['status'])
                        sum_issue=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_issue=%s AND employee=%s AND start_date=%s""",(issue.custom_issue,emp.name,date), as_dict=True)

                        issues.append({
                            "id": issue.custom_issue,
                            # "at_taken": issue.hours,
                            "at_taken": sum_issue[0]['sum(cs.hours)'],
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
                        sum_meeting=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE custom_meeting=%s AND employee=%s AND start_date=%s""",(meeting.custom_meeting,emp.name,date), as_dict=True)
                        meetings.append({
                            "id": meeting.custom_meeting,
                            # "at_taken": meeting.hours,
                            "at_taken": sum_meeting[0]['sum(cs.hours)'],
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
                        sum_task=frappe.db.sql("""select sum(cs.hours) from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s AND start_date=%s""",(log.task,emp.name,date), as_dict=True)
                        tasks.append({
                        "id": log.task,
                        # "at_taken": log.hours,
                        "at_taken":sum_task[0]['sum(cs.hours)'],
                        # "a_task_type":task.type,
                        "cb":short_code,
                        "current_status":t_id
                        })
                        appended_tasks.add(log.task)        
        # task_id_list = frappe.db.get_all("Task", {"custom_production_date": date,"service":service,"type":type}, ['*'], order_by='cb asc, project asc, priority asc',group_by='cb')
        # for task in task_id_list:
        #     emp_id = frappe.db.get_value("Employee", {'short_code': task.cb}, ['name'])
        #     emp_short_code= frappe.db.get_value("Employee", {'name': emp_id},['short_code'])
            
        task_id_lists = frappe.db.get_all("Task", {"custom_production_date": date,"service":service,"type":type,"status":("in",["Working","Pending Review"])}, ['*'], order_by='cb asc, project asc, priority asc')
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
        task_list = frappe.db.get_all("Task", {"custom_production_date":date,"type":type,"service":service,"status":("in",["Working","Pending Review"])}, ['*'], order_by='cb asc',group_by='cb asc')
        for j in task_list:
            employee_id=frappe.db.get_value('Employee',{'user_id':j.spoc},['name'])
            emp_cb=frappe.db.get_value('Employee',{'user_id':j.spoc},['short_code'])
            timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])      
            actual_aph=frappe.db.get_value('Employee',{'name':employee_id},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(pr_expected_time) as et from `tabTask` where cb=%s and cb=%s group by cb""",(j.cb,date), as_dict=True)
            # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s  group by cb""",(j.custom_allocated_to,date), as_dict=True)
            if timesheet and actual_aph is not None:
                percent=(float(timesheet)/float(actual_aph))*100
                for data in parent_doc.dm_summary:
                    if data.d_cb == emp_cb:
                        data.d_aph=actual_aph
                        data.d_actual_time_taken=round(timesheet,2)
            #     parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':round(timesheet,2),'rt_vs_aph_':round(percent,2)})
            else:
                for n in parent_doc.dm_summary:
                    if n.d_cb == emp_cb:
                        n.d_aph=actual_aph
                        n.d_actual_time_taken=0
    parent_doc.dm_status='DSR Pending'
    parent_doc.save()
    frappe.db.commit()
    # frappe.db.set_value('Daily Monitor',name,'dm_status','DSR Pending')


