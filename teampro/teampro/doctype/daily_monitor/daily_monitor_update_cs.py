import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days

@frappe.whitelist()
def get_allocated_tasks_for_it_cs_update(date,name,service,type):
    total=0
    percent=0
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details=[]
    parent_doc.dm_summary=[]
    issue_id=''
    issue_id_cs=''
    spoc_set=set()
    # task_det=''
    pending_total=0
    working_total=0
    client_review=0
    issue_count=0
    if type == "CS":
        task_det=frappe.db.get_all("Task",{"custom_production_date_cs":date,"service":service,"type":type,"status":("in",["Working","Pending Review","Client Review"])},['*'],order_by='spoc asc',group_by='spoc asc')
        task_id_cs=frappe.db.get_all("Task",{"custom_production_date_cs":date,"service":service,"type":type,"status":("in",["Working","Pending Review","Client Review"])},['*'],order_by='spoc asc, project asc, priority asc')
        joint_task=frappe.db.get_all("Task",{"custom_production_date_cs":date,"service":service,"type":"Joint","status":("in",["Working","Pending Review","Client Review"])},['*'],order_by='spoc asc, project asc, priority asc')
        issue=frappe.db.get_all("Issue",{"custom_production_date":date},["*"])
        for i in task_id_cs:
            emp_short=frappe.db.get_value("Employee",{"user_id":i.spoc},["short_code"])
            parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":emp_short})
            spoc_set.add(i.spoc)
        for joint in joint_task:
            parent_doc.append("task_details", {"id": joint.name,"a_task_type":joint.type,"cb":joint.emp_short})
            spoc_data = {}
        for j in issue:
            emp_short=frappe.db.get_value("Employee",{"user_id":j.custom_spoc},["short_code"])
            parent_doc.append("task_details", {"id": j.name,"cb":emp_short,"project_name":j.project,"subject":j.subject,"status":j.custom_issue_status})

        for k in task_det:
            emp_shortcode=frappe.db.get_value("Employee",{"user_id":k.spoc},["short_code"])
            actual_aph=frappe.db.get_value('Employee',{'short_code':emp_shortcode},['custom_aph'])
            # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date_cs=%s and type='OPS' group by cb""",(k.custom_allocated_to,date), as_dict=True)
            issue_data = frappe.db.get_all(
                "Issue",
                filters={"custom_production_date": date},
                fields=["assigned_to", "custom_spoc"]
            )

            for issues in issue_data:
                emp_short_1 = frappe.db.get_value("Employee", {"user_id": issues["custom_spoc"]}, "user_id")
            issue_count = frappe.db.count("Issue", {"custom_production_date": date, "custom_spoc": emp_short_1},['name'])
            print(issue_count)
            issue_1 = frappe.db.sql("""select sum(custom_excepted_time_cs) as issue_1 from `tabIssue` where custom_spoc=%s and custom_production_date=%s """,(emp_short_1,date), as_dict=True)
            print(issue_1)
            sum_et=frappe.db.sql("""select sum(pr_expected_time) as et from `tabTask` where spoc=%s and custom_production_date_cs=%s and type='CS' and status!="Cancelled" group by spoc""",(k.spoc,date), as_dict=True)
            pr_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS pr_rt FROM `tabTask`
                             WHERE spoc=%s AND custom_production_date_cs=%s 
                             AND type='CS' AND status='Pending Review' 
                             GROUP BY spoc""", (k.spoc, date), as_dict=True)

            working_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS working_rt FROM `tabTask`
                                        WHERE spoc=%s AND custom_production_date_cs=%s 
                                        AND type='CS' AND status='Working' 
                                        GROUP BY spoc""", (k.spoc, date), as_dict=True)

            client_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS client_rt FROM `tabTask`
                                        WHERE spoc=%s AND custom_production_date_cs=%s 
                                        AND type='CS' AND status='Client Review' 
                                        GROUP BY spoc""", (k.spoc, date), as_dict=True)
            
            pr_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":"CS","service":service,"spoc":k.spoc,"status":"Pending Review"})
            working_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":"CS","service":service,"spoc":k.spoc,"status":"Working"})
            client_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":"CS","service":service,"spoc":k.spoc,"status":"Client Review"})
            # # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date_cs=%s and service="IT-SW" group by custom_allocated_to""",(k.custom_allocated_to,date), as_dict=True)
            pr_rt_value = f"{pr_rt[0].pr_rt:.3f}" if pr_rt else "0.000"
            working_rt_value = f"{working_rt[0].working_rt:.3f}" if working_rt else "0.000"
            client_rt_value = f"{client_rt[0].client_rt:.3f}" if client_rt else "0.000"
            issue_value = f"{issue_1[0].issue_1:.3f}" if issue_1 else "0.000"
            pending_total+=float(pr_count)
            working_total+=float(working_count)
            client_review+=float(client_count)
            issue_count+=issue_count
            if sum_et is not None:
                if actual_aph is not None:
                    percent=(float(sum_et[0].et)/float(actual_aph))*100
                    parent_doc.append("dm_summary",{'d_cb':emp_shortcode,'d_aph':actual_aph or '8','d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or'0',"pr":pending_total,"working":working_total,"client_review":client_review,"issue":issue_count})
                else:
                    # percent=(float(sum_et[0].et)/8)*100
                    parent_doc.append("dm_summary",{'d_cb':emp_shortcode,'d_aph':'8','d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0',"pr":pending_total,"working":working_total,"client_review":client_review,"issue":issue_count})
    # parent_doc.dm_status="DPR Pending"
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")



@frappe.whitelist()
def dpr_task_mail_cs_it_update(name,date,service,task_type):
    total=0
    total_count=0
    percent=0
    or_count=0
    pr_count=0
    client_count=0
    issue_et=0
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]

    if task_type == "CS":
        emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00023'},['*'])
        recievers.append('anil.p@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    # task = frappe.db.get_all("Task", {"custom_production_date_cs":date,"type":task_type,"service":service}, ['*'], order_by='cb asc',group_by='spoc asc')
    cs_task = frappe.db.get_all("Task", {"custom_production_date_cs":date,"type":task_type,"service":service,"status":("in",["Working","Pending Review"])}, ['*'], order_by='spoc asc',group_by='spoc asc')
    # cs_task = frappe.db.get_all("Task", {"custom_production_date_cs":date,"type":task_type,"service":service}, ['*'], order_by='spoc asc',group_by='spoc asc')    
    total_at=0
    or_total=0
    pr_total=0
    pr_count=0
    or_count=0
    client_count=0
    issue_count=0
    issue_et=0
    if task_data.dsr_check==1:
        if task_type =="CS":
            sum_et=0
            table=''
            spot_table=''
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
                <td style='width:1%'><b>PR[#/hr]</b></td>
                <td style='width:1%'><b>Working[#/hr]</b></td>
                <td style='width:1%'><b>CR[#/hr]</b></td>
                <td style='width:1%'><b>Issue[#/hr]</b></td>
                <td style='width:1%'><b>OR %</b></td>
                <td style='width:1%'><b>PR %</b></td>
            </tr>
            '''
            spot_table = '<table border="1" width="70%" style="border-collapse: collapse;text-align:center;">'
            spot_table += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:1%'><b>SPOC</b></td>
                <td style='width:1%'><b>APH</b></td>
                <td style='width:1%'><b>RT</b></td>
                <td style='width:1%'><b>Actual Time Taken</b></td>
                <td style='width:1%'><b>RT Vs APH %</b></td>
                <td style='width:1%'><b>PR[#/hr]</b></td>
                <td style='width:1%'><b>Working[#/hr]</b></td>
                <td style='width:1%'><b>CR[#/hr]</b></td>
                <td style='width:1%'><b>Issue[#/hr]</b></td>
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
            client_review=0
            spot_pending_count_total=0
            spot_working_total=0
            spot_client_review=0
            issue_dsr=0
            issue_et=0
            issue_data = frappe.db.get_all(
                
                    "Issue",

                    filters={"custom_production_date": date},

                    fields=["assigned_to", "custom_spoc"]
                )

            issue_count=0
            issue_et=0
            for issues in issue_data:

                issue_1 = frappe.db.sql(
                    """SELECT SUM(custom_excepted_time_cs) AS issue_1 FROM `tabIssue`
                        WHERE custom_spoc=%s AND custom_production_date=%s""",
                    (issues.spoc, date), as_dict=True,
                )
                issue_et=f"{issue_1[0].issue_1:.1f}" if issue_1 and issue_1[0].issue_1 else "0.000"
                issue_dsr += frappe.db.count("Issue", {"custom_production_date": date, "custom_spoc": issues.spoc})
            for j in cs_task:
                employee_id=frappe.db.get_value('Employee',{'user_id':j.spoc},['name'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':j.spoc},['short_code'])
                timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])  
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date_cs=%s and service="IT-SW" group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
                # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date_cs=%s and type='OPS' group by cb""",(j.custom_allocated_to,date), as_dict=True)                
                pr_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS pr_rt FROM `tabTask`
                                    WHERE spoc=%s AND custom_production_date_cs=%s 
                                    AND type='CS' AND status='Pending Review' 
                                    GROUP BY spoc""", (j.spoc, date), as_dict=True)

                working_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS working_rt FROM `tabTask`
                                            WHERE spoc=%s AND custom_production_date_cs=%s 
                                            AND type='CS' AND status='Working' 
                                            GROUP BY spoc""", (j.spoc, date), as_dict=True)

                client_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS client_rt FROM `tabTask`
                                            WHERE spoc=%s AND custom_production_date_cs=%s 
                                            AND type='CS' AND status='Client Review' 
                                            GROUP BY spoc""", (j.spoc, date), as_dict=True)

                pending_review_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Pending Review"})
                working_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Working"})
                client_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Client Review"})
                pr_rt_value = f"{pr_rt[0].pr_rt:.3f}" if pr_rt else "0.000"
                working_rt_value = f"{working_rt[0].working_rt:.3f}" if working_rt else "0.000"
                client_rt_value = f"{client_rt[0].client_rt:.3f}" if client_rt else "0.000"
                pending_count_total+=float(pending_review_count)
                working_total+=float(working_count)
                client_review+=float(client_count)
            

            
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
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et if sum_et else '0',round(timesheet,2) if timesheet is not None else '0',round(percent) if timesheet is not None else '0',f"{pending_review_count or '0'} / {pr_rt_value}",f"{working_count or '0'} / {working_rt_value}",f"{client_count or '0'} / {client_rt_value}",issue_dsr,round(or_count) if timesheet is not None else '0',round(pr_count) if timesheet is not None else '0')
                else:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et if sum_et else '0',round(timesheet,2) if timesheet is not None else'0','0',f"{pending_review_count or '0'} / {pr_rt_value}",f"{working_count or '0'} / {working_rt_value}",f"{client_count or '0'} / {client_rt_value}",f"{issue_dsr or '0'} / {issue_et}",round(or_count,2) or '0',round(pr_count,2) or '0')
            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_totals,total,round(total_at,2),round(total_count),pending_count_total,working_total,client_review,issue_dsr,round(or_total),round(pr_total))
            table += "</table>"

            spot_pr_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS pr_rt FROM `tabTask`
                                    WHERE spoc=%s AND custom_production_date_cs=%s 
                                    AND type='CS' AND status='Pending Review' AND 'custom_spot_task_cs'=1 
                                    GROUP BY spoc""", (j.spoc, date), as_dict=True)

            spot_working_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS working_rt FROM `tabTask`
                                        WHERE spoc=%s AND custom_production_date_cs=%s 
                                        AND type='CS' AND status='Working' AND custom_spot_task_cs=1
                                        GROUP BY spoc""", (j.spoc, date), as_dict=True)

            spot_client_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS client_rt FROM `tabTask`
                                        WHERE spoc=%s AND custom_production_date_cs=%s 
                                        AND type='CS' AND status='Client Review' AND custom_spot_task_cs=1
                                        GROUP BY spoc""", (j.spoc, date), as_dict=True)

            spot_pending_review_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Pending Review","custom_spot_task_cs":1})
            spot_working_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Working","custom_spot_task_cs":1})
            spot_client_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":j.spoc,"status":"Client Review","custom_spot_task_cs":1})
            issue_data = frappe.db.get_all(
            
                "Issue",

                filters={"custom_production_date": date},

                fields=["assigned_to", "custom_spoc"]
            )

            issue_count=0
            issue_et=0
            for issues in issue_data:

                issue_1 = frappe.db.sql(
                    """SELECT SUM(custom_excepted_time_cs) AS issue_1 FROM `tabIssue`
                        WHERE custom_spoc=%s AND custom_production_date=%s""",
                    (issues.spoc, date), as_dict=True,
                )
            issue_et=f"{issue_1[0].issue_1:.1f}" if issue_1 and issue_1[0].issue_1 else "0.000"
            issue_dsr += frappe.db.count("Issue", {"custom_production_date": date, "custom_spoc": issues.spoc})
            spot_pr_rt_value = f"{spot_pr_rt[0].spot_pr_rt:.3f}" if spot_pr_rt else "0.000"
            spot_working_rt_value = f"{spot_working_rt[0].spot_working_rt:.3f}" if spot_working_rt else "0.000"
            spot_client_rt_value = f"{spot_client_rt[0].spot_client_rt:.3f}" if spot_client_rt else "0.000"
            spot_pending_count_total+=float(spot_pending_review_count)
            spot_working_total+=float(spot_working_count)
            spot_client_review+=float(spot_client_count)
            spot_table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et if sum_et else '0',round(timesheet,2) if timesheet is not None else '0',round(percent) if timesheet is not None else '0',f"{spot_pending_review_count or '0'} / {spot_pr_rt_value}",f"{spot_working_count or '0'} / {spot_working_rt_value}",f"{spot_client_count or '0'} / {spot_client_rt_value}",issue_dsr,round(or_count) if timesheet is not None else '0',round(pr_count) if timesheet is not None else '0')
            spot_table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_totals,total,round(total_at,2),round(total_count),spot_pending_count_total,spot_working_total,spot_client_review,issue_dsr,round(or_total),round(pr_total))
            spot_table+="</table>"
            frappe.sendmail(
                    sender='sarath.v@groupteampro.com',
                    recipients=["siva.m@groupteampro.com","jenisha.p@groupteampro.com"],
                    # recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
                    # cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
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

        if task_type=="CS":
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
                <td style='width:3%'><b>PR[#/hr]</b></td>
                <td style='width:3%'><b>Working [#/hr]</b></td>
                <td style='width:3%'><b>CR[#/hr]</b></td>
                <td style='width:3%'><b>Issue[#/hr]</b></td>
                <td style='width:3%'><b>RT</b></td>
                <td style='width:8%'><b>RT Vs APH %</b></td>
                
            </tr>
            '''

            task_det=frappe.db.get_all("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"status":("in",["Working","Pending Review","Client Review"])},['*'],order_by='spoc asc',group_by='spoc asc')

            value=0
            pending_total=0
            working_total=0
            client_review=0
            issue_count=0
            for k in task_det:
                employee_id=frappe.db.get_value('Employee',{'user_id':k.spoc},['user_id'])
                emp_cb=frappe.db.get_value('Employee',{'user_id':k.spoc},['short_code'])
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                sum_rt=frappe.db.sql("""select sum(pr_expected_time) as rt from `tabTask` where spoc=%s and custom_production_date_cs=%s and type='CS' and status!="Client Review" group by spoc""",(k.spoc,date), as_dict=True)
                pr_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS pr_rt FROM `tabTask`
                                    WHERE spoc=%s AND custom_production_date_cs=%s 
                                    AND type='CS' AND status='Pending Review' 
                                    GROUP BY spoc""", (k.spoc, date), as_dict=True)

                working_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS working_rt FROM `tabTask`
                                            WHERE spoc=%s AND custom_production_date_cs=%s 
                                            AND type='CS' AND status='Working' 
                                            GROUP BY spoc""", (k.spoc, date), as_dict=True)

                client_rt = frappe.db.sql("""SELECT SUM(pr_expected_time) AS client_rt FROM `tabTask`
                                            WHERE spoc=%s AND custom_production_date_cs=%s 
                                            AND type='CS' AND status='Client Review' 
                                            GROUP BY spoc""", (k.spoc, date), as_dict=True)
                
                pr_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":k.spoc,"status":"Pending Review"})
                working_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":k.spoc,"status":"Working"})
                client_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":task_type,"service":service,"spoc":k.spoc,"status":"Client Review"})
            
                # # sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date_cs=%s and service="IT-SW" group by custom_allocated_to""",(k.custom_allocated_to,date), as_dict=True)
            
                issue_data = frappe.db.get_all(
                
                    "Issue",

                    filters={"custom_production_date": date},

                    fields=["assigned_to", "custom_spoc"]
                )

                issue_count=0
                for issues in issue_data:

                    issue_1 = frappe.db.sql(
                        """SELECT SUM(custom_excepted_time_cs) AS issue_1 FROM `tabIssue`
                            WHERE custom_spoc=%s AND custom_production_date=%s""",
                        (issues.spoc, date), as_dict=True,
                    )
                    issue_value = f"{issue_1[0].issue_1:.1f}" if issue_1 and issue_1[0].issue_1 else "0.000"

                    pr_rt_value = f"{pr_rt[0].pr_rt:.3f}" if pr_rt else "0.000"
                    working_rt_value = f"{working_rt[0].working_rt:.3f}" if working_rt else "0.000"
                    client_rt_value = f"{client_rt[0].client_rt:.3f}" if client_rt else "0.000"

                    pending_total += pr_count
                    working_total += working_count
                    client_review += client_count
                    issue_count += frappe.db.count("Issue", {"custom_production_date": date, "custom_spoc": issues.spoc})
                    
                    if sum_rt:
                        total+=sum_rt[0].rt
                    if actual_aph is not None:
                        value=actual_aph
                        aph_total+=float(value)
                    if sum_rt and actual_aph is not None:
                        total_count=float(total)/float(aph_total)*100
                        percent=(float(sum_rt[0].rt)/float(actual_aph))*100
                        
                        # percent=(float(issue_value))
                    # # print(employee_id)
                if percent:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb ,value or '8',f"{pr_count or '0'} / {pr_rt_value}",f"{working_count or '0'}/{working_rt_value}",f"{client_count or '0'}/{client_rt_value}",f"{issue_count or '0'}/{issue_value}",sum_rt[0].rt if sum_rt else '0',round(percent,2) or '-')
                else:
                    table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb ,actual_aph or '',f"{pr_count or '0'} / {pr_rt_value}",f"{working_count or '0'}/{working_rt_value}",f"{client_count or '0'}/{client_rt_value}",f"{issue_count or '0'}/{issue_value}",sum_rt[0].rt if sum_rt else '0',round(percent,2) or '-')
            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_total,round(pending_total,2),round(working_total,2),round(client_review,2),issue_count if issue_count else '0',round(total,2) if total else '0',round(total_count,2) if total_count else '0')
            table+='</table>'
            frappe.sendmail(
                    sender='sarath.v@groupteampro.com',
                    # recipients='divya.p@groupteampro.com',
                    recipients=["siva.m@groupteampro.com","jenisha.p@groupteampro.com"],
                    # recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
                    # cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
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
def update_dsr_cs_it(date, name, service, type):
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details = []
    
    issues, meetings, tasks_by_spoc = [], [], {}
    appended_issues, appended_meetings, appended_tasks = set(), set(), set()

    if type == "CS":
        employee_list = frappe.get_all(
            "Employee",
            filters={'department': 'IT. Customer Sucess (CS) - THIS', 'custom_dept_type': 'CS'},
            fields=['short_code', 'name', 'user_id']
        )

        issue_id_lists = frappe.get_all(
            "Issue",
            filters={"custom_production_date": date},  
            fields=['name', 'priority', 'custom_issue_status', 'customer', 'subject', 'custom_spoc']
        )

        for issue in issue_id_lists:
            spoc_user = issue.custom_spoc
            emp_short = frappe.db.get_value("Employee", {"user_id": spoc_user}, "short_code") or "Unknown"

            if issue.name not in appended_issues:
                sum_issue = frappe.db.sql(
                    """
                    SELECT COALESCE(SUM(cs.hours), 0) as total_hours
                    FROM `tabTimesheet` c 
                    INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                    WHERE cs.custom_issue=%s AND c.start_date=%s
                    """,
                    (issue.name, date),
                    as_dict=True
                )

                issues.append({
                    "id": issue.name,
                    "at_taken": sum_issue[0]['total_hours'] if sum_issue else 0,
                    "project_name": issue.customer,
                    "subject": issue.subject,
                    "status": issue.custom_issue_status,
                    "cb": emp_short,
                    "priority": issue.priority
                })
                appended_issues.add(issue.name)

        for emp in employee_list:
            timesheet = frappe.db.get_value(
                "Timesheet",
                {'start_date': date, 'employee': emp.name, "department": "IT. Customer Sucess (CS) - THIS"},
                ['name']
            )

            if timesheet:
                meeting_logs = frappe.get_all(
                    "Timesheet Detail",
                    filters={'parent': timesheet, 'custom_meeting': ['!=', '']},
                    fields=['custom_meeting']
                )

                for meeting in meeting_logs:
                    if meeting.custom_meeting not in appended_meetings:
                        sum_meeting = frappe.db.sql(
                            """
                            SELECT COALESCE(SUM(cs.hours), 0) as total_hours
                            FROM `tabTimesheet` c 
                            INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                            WHERE cs.custom_meeting=%s AND c.start_date=%s
                            """,
                            (meeting.custom_meeting, date),
                            as_dict=True
                        )

                        meetings.append({
                            "id": meeting.custom_meeting,
                            "at_taken": sum_meeting[0]['total_hours'] if sum_meeting else 0,
                            "subject": frappe.db.get_value("Meeting", meeting.custom_meeting, "name"),
                            "cb": emp.short_code
                        })
                        appended_meetings.add(meeting.custom_meeting)

        # Fetch tasks grouped by SPOC and sorted
        task_id_lists = frappe.get_all(
            "Task",
            filters={
                "custom_production_date_cs": date,
                "service": service,
                "type": type,
                "status": ["not in", ["Open", "Working"]]
            },
            fields=['name', 'spoc', 'status'],
            order_by='spoc asc, status asc'
        )

        for task in task_id_lists:
            emp_short = frappe.db.get_value("Employee", {"user_id": task.spoc}, "short_code") or "Unknown"

            if emp_short not in tasks_by_spoc:
                tasks_by_spoc[emp_short] = []

            tasks_by_spoc[emp_short].append({
                "id": task.name,
                "cb": emp_short,
                "current_status": task.status
            })
            appended_tasks.add(task.name)

        # Sorting for better readability
        issues.sort(key=lambda x: (x['cb'] or '', x['priority'] or '', x['project_name'] or ''))
        meetings.sort(key=lambda x: (x['cb'] or '', x['subject'] or ''))

        # Appending data to `task_details`
        for d in issues:
            parent_doc.append("task_details", d)
        for meeting in meetings:
            parent_doc.append("task_details", meeting)

        # Appending SPOC-wise tasks
        for spoc, spoc_tasks in sorted(tasks_by_spoc.items()):
            for task in spoc_tasks:
                parent_doc.append("task_details", task)

        parent_doc.dsr_check = 1

    parent_doc.dm_status = 'DSR Pending'
    parent_doc.save()
    frappe.db.commit()
