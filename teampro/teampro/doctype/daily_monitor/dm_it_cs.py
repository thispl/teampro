import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days

@frappe.whitelist()
def get_allocated_tasks_for_it_cs(date, name, service, type):
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details = []
    parent_doc.dm_summary = []

    if type == "CS":
        task_id = frappe.db.get_all("Task",{"custom_production_date_cs": date, "service": service, "type": type},["*"],order_by="spoc asc, project asc, priority asc")
        task_det = frappe.db.get_all("Task",{"custom_production_date_cs": date, "service": service, "type": type},["*"],order_by="spoc asc",group_by="spoc asc")
        issue_id = frappe.db.get_all("Issue",{"custom_production_date": date, "status": "Open"},["*"],order_by="custom_spoc asc",group_by="custom_spoc asc")
        for i in task_id:
            cb = frappe.db.get_value("Employee", {"user_id": i.spoc}, "short_code")
            parent_doc.append("task_details", {"id": i.name, "a_task_type": i.type, "cb": cb})

        for j in issue_id:
            cb_spoc = frappe.db.get_value("Employee", {"user_id": j.custom_spoc}, "short_code")
            parent_doc.append("task_details",{
                    "id": j.name,
                    "project_name": j.project,
                    "cb": cb_spoc,
                    "subject": j.subject,
                    "status": j.status,
                },
            )
        for k in task_det:
            actual_aph = frappe.db.get_value("Employee", {"user_id": k.spoc}, ["custom_aph"])
            emp_cb = frappe.db.get_value("Employee", {"user_id": k.spoc}, ["short_code"])
            sum_task_et = frappe.db.sql(
                """
                SELECT SUM(pr_expected_time) AS et
                FROM `tabTask`
                WHERE spoc = %s AND custom_production_date_cs = %s AND type = 'CS'
                GROUP BY spoc
                """,
                (k.spoc, date),
                as_dict=True,
            )
            sum_issue_et = frappe.db.sql(
                """
                SELECT SUM(custom_excepted_time_cs) AS et
                FROM `tabIssue`
                WHERE custom_spoc = %s AND custom_production_date = %s AND status = 'Open'
                GROUP BY custom_spoc
                """,
                (k.spoc, date),
                as_dict=True,
            )
            total_et = (sum_task_et[0].et if sum_task_et else 0) + (sum_issue_et[0].et if sum_issue_et else 0)
            if total_et:
                if actual_aph is not None:
                    percent = (float(total_et) / float(actual_aph)) * 100
                    parent_doc.append(
                        "dm_summary",
                        {
                            "d_cb": emp_cb,
                            "d_aph": actual_aph or "8",
                            "d_rt": total_et,
                            "d_actual_time_taken": "",
                            "rt_vs_aph_": round(percent, 2) or "0",
                        },
                    )
                else:
                    percent = (float(total_et) / 8) * 100
                    parent_doc.append(
                        "dm_summary",
                        {
                            "d_cb": emp_cb,
                            "d_aph": "8",
                            "d_rt": total_et,
                            "d_actual_time_taken": "",
                            "rt_vs_aph_": round(percent, 2) or "0",
                        },
                    )

    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor", name, "dm_status", "DPR Pending")

from collections import defaultdict
@frappe.whitelist()
def dpr_mail_it_cs(name,date,service,type):
    total=0
    total_count=0
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    recievers=[]
    if type == "CS":
        emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00023'},['*'])
        recievers.append('anil.p@groupteampro.com')
        for i in emp:
            recievers.append(i.user_id)
    recievers.append('dineshbabu.k@groupteampro.com')
    task_data=frappe.get_doc("Daily Monitor",name)
    cs_task = frappe.db.get_all("Task", {"custom_production_date_cs":date,"type":type,"service":service}, ['*'], order_by='spoc asc',group_by='spoc asc')
    if task_data.dsr_check==1:

        count = 1
        task_summary = defaultdict(lambda: {"at_taken":0,"pr_count": 0, "working_count": 0, "cr_count": 0, "issue_count": 0, "rt_count": 0,"pr_time":0,"cr_time":0,"working_time":0,"issue_time":0})
        spot_task_summary = defaultdict(lambda: {"spot_at_taken":0,"spot_pr_count": 0, "spot_working_count": 0, "spot_cr_count": 0, "spot_issue_count": 0, "spot_rt_count": 0,"spot_pr_time":0,"spot_cr_time":0,"spot_working_time":0,"spot_issue_time":0})
        # Initialize grand totals
        grand_total = {
            "pr_count": 0, "pr_time": 0, "working_count": 0, "working_time": 0,
            "cr_count": 0, "cr_time": 0, "issue_count": 0, "issue_time": 0,
            "rt_count": 0, "at_taken": 0,
            "spot_pr_count": 0, "spot_pr_time": 0, "spot_working_count": 0,
            "spot_working_time": 0, "spot_cr_count": 0, "spot_cr_time": 0,
            "spot_issue_count": 0, "spot_issue_time": 0,
            "spot_rt_count": 0, "spot_at_taken": 0
        }

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
            cb = i.cb or " "
            short_code = i.cb or ''
            data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id or i.issue,i.project_name or '-',i.subject,i.cb,i.status,'-',i.at_taken,'-','-',i.priority,i.allocated_on or '')
            if i.spot_task == 0:
                task_summary[cb]["at_taken"]+= float(i.at_taken) if i.at_taken else 0
                if i.status == "Pending Review":
                    task_summary[cb]["rt_count"] +=i.cs_rt or 0
                    task_summary[cb]["pr_count"] += 1
                    task_summary[cb]["pr_time"] += i.cs_rt or 0
                elif i.status == "Working":
                    task_summary[cb]["rt_count"] +=i.cs_rt or 0
                    task_summary[cb]["working_count"] += 1
                    task_summary[cb]["working_time"] += i.cs_rt or 0
                elif i.status == "Client Review":
                    task_summary[cb]["cr_count"] += 1
                    task_summary[cb]["cr_time"] += i.cs_rt or 0
                elif i.status == "Open" and i.a_task_type is None:
                    task_summary[cb]["rt_count"] +=i.cs_rt or 0
                    task_summary[cb]["issue_count"] += 1
                    task_summary[cb]["issue_time"] += i.cs_rt or 0
            if i.spot_task == 1:
                spot_task_summary[short_code]["spot_at_taken"] += float(i.at_taken) if i.at_taken else 0
                if i.status == "Pending Review":
                    spot_task_summary[short_code]["spot_rt_count"] +=i.cs_rt or 0
                    spot_task_summary[short_code]["spot_pr_count"] += 1
                    spot_task_summary[short_code]["spot_pr_time"] += i.cs_rt or 0
                elif i.status == "Working":
                    spot_task_summary[short_code]["spot_rt_count"] +=i.cs_rt or 0
                    spot_task_summary[short_code]["spot_working_count"] += 1
                    spot_task_summary[short_code]["spot_working_time"] += i.cs_rt or 0
                elif i.status == "Client Review":
                    spot_task_summary[short_code]["spot_cr_count"] += 1
                    spot_task_summary[short_code]["spot_cr_time"] += i.cs_rt or 0
                elif i.status == "Open" and i.a_task_type is None:
                    spot_task_summary[short_code]["spot_rt_count"] +=i.cs_rt or 0
                    spot_task_summary[short_code]["spot_issue_count"] += 1
                    spot_task_summary[short_code]["spot_issue_time"] += i.cs_rt or 0

            count+=1
        data += '</table>' 
       
        table = '<table border="1" width="100%" style="border-collapse: collapse; text-align:center;">'
        table += '''
        <tr style="background-color: #0f1568; color: white; text-align: center; font-size: 14px;">
            <td colspan="7"><b>DSR</b></td>
            <td colspan="5" style="background-color: yellow; color: red;"><b>SPOT</b></td>
            <td colspan="3" style="background-color: yellow; color: black;"></td>
        </tr>
        <tr style="background-color: #0f1568; color: white; text-align: center; font-size: 12px;">
            <td><b>SPOC</b></td>
            <td><b>APH</b></td>
            <td><b>PR[#/hr]</b></td>
            <td><b>Working[#/hr]</b></td>
            <td><b>CR[#/hr]</b></td>
            <td><b>Issue[#/hr]</b></td>
            <td><b>RT</b></td>
            <td><b>PR[#/hr]</b></td>
            <td><b>Working[#/hr]</b></td>
            <td><b>CR[#/hr]</b></td>
            <td><b>Issue[#/hr]</b></td>
            <td><b>RT</b></td>
            <td><b>AT Total</b></td>
            <td><b>OR %</b></td>
            <td><b>PR %</b></td>
        </tr>
        '''
        all_cb_keys = set(task_summary.keys()).union(set(spot_task_summary.keys()))

        for cb in all_cb_keys:
            # Get DSR (Normal Task) Data
            counts = task_summary.get(cb, {
                "pr_count": 0, "pr_time": 0,
                "working_count": 0, "working_time": 0,
                "cr_count": 0, "cr_time": 0,
                "issue_count": 0, "issue_time": 0,
                "rt_count": 0,"at_taken":0
            })

            pr_text = f"{counts['pr_count']} / {round(counts['pr_time'],2)}"
            working_text = f"{counts['working_count']} / {round(counts['working_time'],2)}"
            cr_text = f"{counts['cr_count']} / {round(counts['cr_time'],2)}"
            issue_text = f"{counts['issue_count']} / {round(counts['issue_time'],2)}"
            
            # Get SPOT Data
            spot_counts = spot_task_summary.get(cb, {
                "spot_pr_count": 0, "spot_pr_time": 0,
                "spot_working_count": 0, "spot_working_time": 0,
                "spot_cr_count": 0, "spot_cr_time": 0,
                "spot_issue_count": 0, "spot_issue_time": 0,
                "spot_rt_count": 0,"spot_at_taken":0
            })

            spot_pr_text = f"{spot_counts['spot_pr_count']} / {round(spot_counts['spot_pr_time'],2)}"
            spot_working_text = f"{spot_counts['spot_working_count']} / {round(spot_counts['spot_working_time'],2)}"
            spot_cr_text = f"{spot_counts['spot_cr_count']} / {round(spot_counts['spot_cr_time'],2)}"
            spot_issue_text = f"{spot_counts['spot_issue_count']} / {round(spot_counts['spot_issue_time'],2)}"
            spot_rt_text = f"{spot_counts['spot_rt_count']}"
            total_at=spot_counts['spot_at_taken'] + counts['at_taken']
            # or_percentage = round((total_at / 8) * 100, 2) if total_at else 0
            or_percentage = round((total_at / 8) * 100, 2) if total_at else 0
            pr_percentage = round(((counts['rt_count'] + spot_counts['spot_rt_count']) / total_at) * 100, 2) if total_at else 0
            table += f'''
            <tr>
                <td>{cb}</td>
                <td>8</td>
                <td>{pr_text}</td>
                <td>{working_text}</td>
                <td>{cr_text}</td>
                <td>{issue_text}</td>
                <td>{counts['rt_count']}</td>
                <td>{spot_pr_text}</td>
                <td>{spot_working_text}</td>
                <td>{spot_cr_text}</td>
                <td>{spot_issue_text}</td>
                <td>{spot_rt_text}</td>
                <td>{round(total_at,2)}</td>
                <td>{or_percentage}</td>
                <td>{pr_percentage}</td>
            </tr>
            '''
            for key in grand_total:
                if key in counts:
                    grand_total[key] += counts[key]
                if key in spot_counts:
                    grand_total[key] += spot_counts[key]
        grand_total_at = grand_total["at_taken"] + grand_total["spot_at_taken"]
        grand_total_rt = grand_total["rt_count"] + grand_total["spot_rt_count"]
        grand_or_percentage = round((grand_total_at / (8 * len(all_cb_keys))) * 100, 2) if grand_total_at else 0
        grand_pr_percentage = round((grand_total_rt / grand_total_at) * 100, 2) if grand_total_at else 0

        table += f'''
        <tr style="font-weight:bold; background-color:#f0f0f0;">
            <td>Total</td>
            <td>{8 * len(all_cb_keys)}</td>
            <td>{grand_total["pr_count"]} / {round(grand_total["pr_time"], 2)}</td>
            <td>{grand_total["working_count"]} / {round(grand_total["working_time"], 2)}</td>
            <td>{grand_total["cr_count"]} / {round(grand_total["cr_time"], 2)}</td>
            <td>{grand_total["issue_count"]} / {round(grand_total["issue_time"], 2)}</td>
            <td>{grand_total["rt_count"]}</td>
            <td>{grand_total["spot_pr_count"]} / {round(grand_total["spot_pr_time"], 2)}</td>
            <td>{grand_total["spot_working_count"]} / {round(grand_total["spot_working_time"], 2)}</td>
            <td>{grand_total["spot_cr_count"]} / {round(grand_total["spot_cr_time"], 2)}</td>
            <td>{grand_total["spot_issue_count"]} / {round(grand_total["spot_issue_time"], 2)}</td>
            <td>{grand_total["spot_rt_count"]}</td>
            <td>{round(grand_total_at, 2)}</td>
            <td>{grand_or_percentage}</td>
            <td>{grand_pr_percentage}</td>
        </tr>
        '''
        table += '</table>' 

        frappe.sendmail(
                recipients=['sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com','shylin.j@groupteampro.com'],
                # recipients=['divya.p@groupteampro.com'],
                # cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
                subject = f'{service} - {type} DSR {formatted_date} -Reg',
                message = """
                <b>Dear Team,</b><br><br>
                    Please find the below DSR for {} for your kind reference.<br><br>
                    {}<br><br>
                    {}<br><br>
                    Thanks & Regards,<br>TEAM ERP<br>
                    <i>This email has been automatically generated. Please do not reply</i>
                """.format(formatted_date,table if table else '',data)
            )
        frappe.msgprint("DSR mail has been successfully sent")
        task_data.dm_status='DSR Completed'
        task_data.dpr_submitted_on=today()
        task_data.save()
        frappe.db.commit()
    else:
        count=1
        aph_total=0
        if type=="CS":
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
                data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id or i.issue,i.project_name or '-',i.subject,i.cb,i.status,'-','-','-','-',i.priority,i.allocated_on or '')
                count+=1
            data += '</table>' 
            table = '<table border="1" width="50%" style="border-collapse: collapse;text-align:center;">'
            table += '''
            <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
                <td style='width:3%'><b>SPOC</b></td>
                <td style='width:3%'><b>APH</b></td>
                <td style='width:3%'><b>PR[#/hr]</b></td>
                <td style='width:3%'><b>Working[#/hr]</b></td>
                <td style='width:3%'><b>CR[#/hr]</b></td>
                <td style='width:3%'><b>Issue[#/hr]</b></td>
                <td style='width:3%'><b>RT</b></td>
                <td style='width:8%'><b>RT Vs APH %</b></td>
            </tr>
            '''
            task_det=frappe.db.get_all("Task",{"custom_production_date_cs":date,"type":type,"service":service},['*'],order_by='spoc asc',group_by='spoc asc')
            value=0
            pending_total=0
            working_total=0
            cr_total=0
            issue_total=0
            pr_time_total=0
            working_time_total=0
            cr_time_total=0
            issue_time_total=0
            total_pr=0
            total_working=0
            total_cr=0
            total_issue=0
            percent=0
            for k in task_det:
                emp_cb=frappe.db.get_value('Employee',{'user_id':k.spoc},['short_code'])
                actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
                sum_rt=frappe.db.sql("""select sum(pr_expected_time) as rt from `tabTask` where spoc=%s and custom_production_date_cs=%s and type='CS' group by spoc""",(k.spoc,date), as_dict=True)
                sum_pr_rt=frappe.db.sql("""select sum(pr_expected_time) as rt from `tabTask` where spoc=%s and custom_production_date_cs=%s and type='CS' and status !="Client Review" group by spoc""",(k.spoc,date), as_dict=True)                
                pr_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":type,"service":service,"spoc":k.spoc,"status":"Pending Review"})
                working_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":type,"service":service,"spoc":k.spoc,"status":"Working"})
                cr_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":type,"service":service,"spoc":k.spoc,"status":"Client Review"})
                issue_count=frappe.db.count("Issue",{"custom_production_date":date,"custom_spoc":k.spoc,"status":"Open"})                
                total_pr+=pr_count
                total_working+=working_count
                total_cr+=cr_count
                total_issue+=issue_count
                pr_time=frappe.db.sql(
                    """
                    SELECT SUM(pr_expected_time) AS et
                    FROM `tabTask`
                    WHERE spoc = %s AND custom_production_date_cs = %s AND type = 'CS' AND status='Pending Review'
                    GROUP BY spoc
                    """,
                    (k.spoc, date),
                    as_dict=True,
                    )
                cr_time=frappe.db.sql(
                    """
                    SELECT SUM(pr_expected_time) AS et
                    FROM `tabTask`
                    WHERE spoc = %s AND custom_production_date_cs = %s AND type = 'CS' AND status='Client Review'
                    GROUP BY spoc
                    """,
                    (k.spoc, date),
                    as_dict=True,
                    )
                working_time=frappe.db.sql(
                    """
                    SELECT SUM(pr_expected_time) AS et
                    FROM `tabTask`
                    WHERE spoc = %s AND custom_production_date_cs = %s AND type = 'CS' AND status='Working'
                    GROUP BY spoc
                    """,
                    (k.spoc, date),
                    as_dict=True,
                    )
                issue_time=frappe.db.sql(
                    """
                    SELECT SUM(custom_excepted_time_cs) AS et
                    FROM `tabIssue`
                    WHERE custom_spoc = %s AND custom_production_date = %s AND status = 'Open'
                    GROUP BY custom_spoc
                    """,
                    (k.spoc, date),
                    as_dict=True,
                    )
                pending_total+=float(pr_count)
                working_total+=float(working_count)
                cr_total+=float(cr_count)
                issue_total+=float(issue_count)
                if pr_time:
                    pr_time_total+=pr_time[0].et
                if cr_time:
                    cr_time_total=cr_time[0].et
                if working_time:
                    working_time_total=working_time[0].et
                if issue_time:
                    issue_time_total=issue_time[0].et
                if sum_pr_rt:
                    total+=sum_pr_rt[0].rt
                if actual_aph is not None:
                    value=actual_aph
                    aph_total+=float(value)
                if sum_pr_rt and actual_aph is not None:
                    total_count=float(total)/float(aph_total)*100
                    percent=(float(sum_rt[0].rt)/float(actual_aph))*100
                if percent:
                    table += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                        emp_cb,
                        value or '8',
                        "%s/%s" % (pr_count, pr_time[0].et if pr_time else '0.0'),
                        "%s/%s" % (working_count, working_time[0].et if working_time else '0.0'),
                        "%s/%s" % (cr_count, cr_time[0].et if cr_time else '0.0'),
                        "%s/%s" % (issue_count, issue_time[0].et if issue_time else '0.0'),
                        sum_rt[0].rt if sum_rt else '0',
                        round(percent, 2) or '-'
                    )
                else:
                    table += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                        emp_cb,
                        actual_aph or '',
                        "%s/%s" % (pr_count, pr_time[0].et if pr_time else '0.0'),
                        "%s/%s" % (working_count, working_time[0].et if working_time else '0.0'),
                        "%s/%s" % (cr_count, cr_time[0].et if cr_time else '0.0'),
                        "%s/%s" % (issue_count, issue_time[0].et if issue_time else '0.0'),
                        sum_rt[0].rt if sum_rt else '0',
                        round(percent, 2) or '-'
                    )

            table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                aph_total,
                "%s/%s" % (total_pr,pr_time_total or '0.0'),
                "%s/%s" % (total_working,working_time_total or '0.0'),
                "%s/%s" % (total_cr,cr_time_total or '0.0'),
                "%s/%s" % (total_issue,issue_time_total or '0.0'),
                round(total, 2) if total else '0',  # Removed extra comma
                round(total_count, 2) if total_count else '0'
            )

            table+='</table>'
            frappe.sendmail(
                    # sender='sarath.v@groupteampro.com',
                    recipients=['sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com','shylin.j@groupteampro.com'],
                    # recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
                    cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
                    subject = f'{service} - {type} DPR {formatted_date} -Reg',
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

@frappe.whitelist()
def update_it_cs(name,date,service,type):
    parent_doc = frappe.get_doc("Daily Monitor",name)
    timesheets = frappe.db.get_all(
        "Timesheet",
        filters={'start_date':date, 'department': "IT. Customer Sucess (CS) - THIS"},
        fields=['name', 'employee']
    )
    employee_list=frappe.get_all("Employee",{'department':"IT. Customer Sucess (CS) - THIS",'custom_dept_type':'CS'},['short_code','name'])

    if timesheets:
        existing_tasks = {(task.id, task.cb) for task in parent_doc.task_details}  # Set for quick lookup

        for timesheet in timesheets:
            cb = frappe.db.get_value("Employee", {"name": timesheet.employee}, ["short_code"])

            task_logs = frappe.get_all(
                "Timesheet Detail",
                filters={'parent': timesheet.name},
                fields=['task']
            )

            for log in task_logs:
                # Ensure the same task can be added if cb (short_code) is different
                if (log.task, cb) not in existing_tasks:
                    parent_doc.append("task_details", {"id": log.task, "cb": cb,"spot_task":1})
                    existing_tasks.add((log.task, cb))  # Add to set to prevent duplicates
    for i in parent_doc.task_details:
        total_hours = 0 
        for emp in employee_list:
            sum_task = frappe.db.sql(
                """SELECT SUM(cs.hours) AS total_hours FROM `tabTimesheet` c  
                   INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent 
                   WHERE task = %s AND employee = %s AND start_date = %s""",
                (i.id, emp.name, date),
                as_dict=True
            )

            emp_hours = sum_task[0].total_hours if sum_task and sum_task[0].total_hours else 0

            # Check if the row belongs to the current employee
            if i.cb == emp.short_code:
                i.at_taken = round(emp_hours, 2)
            # sum_task=frappe.db.sql("""select sum(cs.hours) as total_hours from `tabTimesheet` c  INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent WHERE task=%s AND employee=%s AND start_date=%s""",(i.id,emp.name,date), as_dict=True) 
            # total_hours += sum_task[0].total_hours if sum_task and sum_task[0].total_hours else 0
            # i.at_taken =round(total_hours,2)
    parent_doc.dsr_check = 1
    parent_doc.save(ignore_permissions=True)  # Save the document after updates


@frappe.whitelist()
def update_it_cs_test():
    parent_doc = frappe.get_doc("Daily Monitor", "DM-00592")
    
    timesheets = frappe.db.get_all(
        "Timesheet",
        filters={'start_date': "2025-04-01", 'department': "IT. Customer Sucess (CS) - THIS"},
        fields=['name', 'employee']
    )

    if timesheets:
        existing_tasks = {(task.id, task.cb) for task in parent_doc.task_details}  # Set for quick lookup

        for timesheet in timesheets:
            cb = frappe.db.get_value("Employee", {"name": timesheet.employee}, ["short_code"])

            task_logs = frappe.get_all(
                "Timesheet Detail",
                filters={'parent': timesheet.name},
                fields=['task']
            )

            for log in task_logs:
                # Ensure the same task can be added if cb (short_code) is different
                if (log.task, cb) not in existing_tasks:
                    parent_doc.append("task_details", {"id": log.task, "cb": cb})
                    existing_tasks.add((log.task, cb))  # Add to set to prevent duplicates

        parent_doc.save(ignore_permissions=True)  # Save the document after updates


# from collections import defaultdict
# @frappe.whitelist()
# def dpr_mail_it_cs(name,date,service,type):
#     total=0
#     total_count=0
#     date_obj = datetime.strptime(date, '%Y-%m-%d')
#     formatted_date = date_obj.strftime('%d/%m/%Y')
#     recievers=[]
#     if type == "CS":
#         emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00023'},['*'])
#         recievers.append('anil.p@groupteampro.com')
#         for i in emp:
#             recievers.append(i.user_id)
#     recievers.append('dineshbabu.k@groupteampro.com')
#     task_data=frappe.get_doc("Daily Monitor",name)
#     cs_task = frappe.db.get_all("Task", {"custom_production_date_cs":date,"type":type,"service":service}, ['*'], order_by='spoc asc',group_by='spoc asc')
#     if task_data.dsr_check==1:

#         count = 1
#         task_summary = defaultdict(lambda: {"pr_count": 0, "working_count": 0, "cr_count": 0, "issue_count": 0, "rt_count": 0,"pr_time":0,"cr_time":0,"working_time":0,"issue_time":0})
#         spot_task_summary = defaultdict(lambda: {"spot_pr_count": 0, "spot_working_count": 0, "spot_cr_count": 0, "spot_issue_count": 0, "spot_rt_count": 0,"spot_pr_time":0,"spot_cr_time":0,"spot_working_time":0,"spot_issue_time":0})
#         data = '<table border="1" width="100%" style="border-collapse: collapse;">'
#         data += '''
#         <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
#             <td style='width:5%'><b>SI NO</b></td>
#             <td style='width:10%'><b>ID</b></td>
#             <td style='width:15%'><b>Project </b></td>
#             <td style='width:20%'><b>Subject</b></td>
#             <td style='width:5%'><b>CB</b></td>
#             <td style='width:10%'><b>Status</b></td>
#             <td style='width:5%'><b>Revision</b></td>
#             <td style='width:5%'><b>AT</b></td>
#             <td style='width:5%'><b>ET</b></td>
#             <td style='width:5%'><b>RT</b></td>
#             <td style='width:7%'><b>Priority</b></td>
#             <td style='width:13%'><b>Allocated On</b></td>
#         </b></tr>
#         '''
#         for i in task_data.task_details:
#             cb = i.cb or " "
#             short_code = i.cb or ''
#             data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id or i.issue,i.project_name or '-',i.subject,i.cb,i.status,'-',i.at_taken,'-','-',i.priority,i.allocated_on or '')
#             if i.spot_task == 0:
#                 task_summary[cb]["rt_count"] +=i.cs_rt or 0
#                 if i.status == "Pending Review":
#                     task_summary[cb]["pr_count"] += 1
#                     task_summary[cb]["pr_time"] += i.cs_rt or 0
#                 elif i.status == "Working":
#                     task_summary[cb]["working_count"] += 1
#                     task_summary[cb]["working_time"] += i.cs_rt or 0
#                 elif i.status == "Client Review":
#                     task_summary[cb]["cr_count"] += 1
#                     task_summary[cb]["cr_time"] += i.cs_rt or 0
#                 elif i.status == "Open" and i.a_task_type is None:
#                     task_summary[cb]["issue_count"] += 1
#                     task_summary[cb]["issue_time"] += i.cs_rt or 0
#             if i.spot_task == 1:
#                 spot_task_summary[short_code]["spot_rt_count"] +=i.cs_rt or 0
#                 if i.status == "Pending Review":
#                     spot_task_summary[short_code]["spot_pr_count"] += 1
#                     spot_task_summary[short_code]["spot_pr_time"] += i.cs_rt or 0
#                 elif i.status == "Working":
#                     spot_task_summary[short_code]["spot_working_count"] += 1
#                     spot_task_summary[short_code]["spot_working_time"] += i.cs_rt or 0
#                 elif i.status == "Client Review":
#                     spot_task_summary[short_code]["spot_cr_count"] += 1
#                     spot_task_summary[short_code]["spot_cr_time"] += i.cs_rt or 0
#                 elif i.status == "Open" and i.a_task_type is None:
#                     spot_task_summary[short_code]["spot_issue_count"] += 1
#                     spot_task_summary[short_code]["spot_issue_time"] += i.cs_rt or 0

#             count+=1
#         data += '</table>' 
#         # table = '<table border="1" width="50%" style="border-collapse: collapse;text-align:center;">'
#         # table += '''
#         # <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
#         #     <td style='width:3%'><b>SPOC</b></td>
#         #     <td style='width:3%'><b>APH</b></td>
#         #     <td style='width:3%'><b>PR[#/hr]</b></td>
#         #     <td style='width:3%'><b>Working[#/hr]</b></td>
#         #     <td style='width:3%'><b>CR[#/hr]</b></td>
#         #     <td style='width:3%'><b>Issue[#/hr]</b></td>
#         #     <td style='width:3%'><b>RT</b></td>
#         #     <td style='width:8%'><b>RT Vs APH %</b></td>
#         # </tr>
#         # '''
#         # spot_table = '<table border="1" width="50%" style="border-collapse: collapse;text-align:center;">'
#         # spot_table += '''
#         # <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
#         #     <td style='width:3%'><b>SPOC</b></td>
#         #     <td style='width:3%'><b>APH</b></td>
#         #     <td style='width:3%'><b>PR[#/hr]</b></td>
#         #     <td style='width:3%'><b>Working[#/hr]</b></td>
#         #     <td style='width:3%'><b>CR[#/hr]</b></td>
#         #     <td style='width:3%'><b>Issue[#/hr]</b></td>
#         #     <td style='width:3%'><b>RT</b></td>
#         #     <td style='width:8%'><b>RT Vs APH %</b></td>
#         # </tr>
#         # '''
#         table = '<table border="1" width="100%" style="border-collapse: collapse; text-align:center;">'
#         table += '''
#         <tr style="background-color: #0f1568; color: white; text-align: center; font-size: 14px;">
#             <td colspan="7"><b>DSR</b></td>
#             <td colspan="7" style="background-color: yellow; color: red;"><b>SPOT</b></td>
#             <td colspan="3" style="background-color: yellow; color: black;"><b>Additional Columns</b></td>
#         </tr>
#         <tr style="background-color: #0f1568; color: white; text-align: center; font-size: 12px;">
#             <td><b>SPOC</b></td>
#             <td><b>APH</b></td>
#             <td><b>PR[#/hr]</b></td>
#             <td><b>Working[#/hr]</b></td>
#             <td><b>CR[#/hr]</b></td>
#             <td><b>Issue[#/hr]</b></td>
#             <td><b>RT</b></td>
#             <td><b>PR[#/hr]</b></td>
#             <td><b>Working[#/hr]</b></td>
#             <td><b>CR[#/hr]</b></td>
#             <td><b>Issue[#/hr]</b></td>
#             <td><b>RT</b></td>
#             <td><b>AT Total of S+N</b></td>
#             <td><b>OR %</b></td>
#             <td><b>PR %</b></td>
#         </tr>
#         '''
#         # for cb, counts in task_summary.items():
#         #     pr_text = f"{counts['pr_count']} / {counts['pr_time']}"
#         #     working_text = f"{counts['working_count']} / {counts['working_time']}"
#         #     cr_text = f"{counts['cr_count']} / {counts['cr_time']}"
#         #     issue_text = f"{counts['issue_count']} / {counts['issue_time']}"

#         #     table += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
#         #         cb, "8", pr_text, working_text, cr_text, issue_text,counts['rt_count'], ""
#         #     )

#         # table += '</table>'
#         # for short_code, c in spot_task_summary.items():
#         #     pr_text = f"{c['spot_pr_count']} / {c['spot_pr_time']}"
#         #     working_text = f"{c['spot_working_count']} / {c['spot_working_time']}"
#         #     cr_text = f"{c['spot_cr_count']} / {c['spot_cr_time']}"
#         #     issue_text = f"{c['spot_issue_count']} / {c['spot_issue_time']}"

#         #     spot_table += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
#         #         short_code, "8", pr_text, working_text, cr_text, issue_text,c['spot_rt_count'], ""
#         #     )

#         # spot_table += '</table>'
#         for cb,short_code, counts in task_summary.items():
#             pr_text = f"{counts['pr_count']} / {counts['pr_time']}"
#             working_text = f"{counts['working_count']} / {counts['working_time']}"
#             cr_text = f"{counts['cr_count']} / {counts['cr_time']}"
#             issue_text = f"{counts['issue_count']} / {counts['issue_time']}"

#             spot_counts = spot_task_summary.get(short_code, {
#                 "spot_pr_count": 0, "spot_pr_time": 0,
#                 "spot_working_count": 0, "spot_working_time": 0,
#                 "spot_cr_count": 0, "spot_cr_time": 0,
#                 "spot_issue_count": 0, "spot_issue_time": 0,
#                 "spot_rt_count": 0
#             })

#             spot_pr_text = f"{spot_counts['spot_pr_count']} / {spot_counts['spot_pr_time']}"
#             spot_working_text = f"{spot_counts['spot_working_count']} / {spot_counts['spot_working_time']}"
#             spot_cr_text = f"{spot_counts['spot_cr_count']} / {spot_counts['spot_cr_time']}"
#             spot_issue_text = f"{spot_counts['spot_issue_count']} / {spot_counts['spot_issue_time']}"
#             spot_rt_text = f"{spot_counts['spot_rt_count']}"

#             table += f'''
#             <tr>
#                 <td>{cb}</td>
#                 <td>8</td>
#                 <td>{pr_text}</td>
#                 <td>{working_text}</td>
#                 <td>{cr_text}</td>
#                 <td>{issue_text}</td>
#                 <td>{counts['rt_count']}</td>
#                 <td>{spot_pr_text}</td>
#                 <td>{spot_working_text}</td>
#                 <td>{spot_cr_text}</td>
#                 <td>{spot_issue_text}</td>
#                 <td>{spot_rt_text}</td>
#                 <td>-</td>
#                 <td>-</td>
#                 <td>-</td>
#             </tr>
#             '''

#         table += '</table>'

#         frappe.sendmail(
#                 recipients='divya.p@groupteampro.com',
#                 # recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
#                 # cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
#                 subject = f'{service} - {type} DSR {formatted_date} -Reg',
#                 message = """
#                 <b>Dear Team,</b><br><br>
# Please find the below DSR for {} for your kind reference and action, ensure all the Tasks allocated on time and as per the requirement.<br><br>
#             DPR:<br>
#             {}<br><br>
#             {}<br><br>
#                 Thanks & Regards,<br>TEAM ERP<br>
                
#                 <i>This email has been automatically generated. Please do not reply</i>
#                 """.format(formatted_date,table if table else '',data)
#             )
#         frappe.msgprint("DSR mail has been successfully sent")
#         task_data.dm_status='DSR Completed'
#         task_data.dpr_submitted_on=today()
#         task_data.save()
#         frappe.db.commit()
#     else:
#         count=1
#         aph_total=0
#         if type=="CS":
#             table=''
#             data = '<table border="1" width="100%" style="border-collapse: collapse;">'
#             data += '''
#             <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
#                 <td style='width:5%'><b>SI NO</b></td>
#                 <td style='width:10%'><b>ID</b></td>
#                 <td style='width:15%'><b>Project </b></td>
#                 <td style='width:20%'><b>Subject</b></td>
#                 <td style='width:5%'><b>CB</b></td>
#                 <td style='width:10%'><b>Status</b></td>
#                 <td style='width:5%'><b>Revision</b></td>
#                 <td style='width:5%'><b>AT</b></td>
#                 <td style='width:5%'><b>ET</b></td>
#                 <td style='width:5%'><b>RT</b></td>
#                 <td style='width:7%'><b>Priority</b></td>
#                 <td style='width:13%'><b>Allocated On</b></td>
#             </b></tr>
#             '''
#             for i in task_data.task_details:
#                 data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id or i.issue,i.project_name or '-',i.subject,i.cb,i.status,'-','-','-','-',i.priority,i.allocated_on or '')
#                 count+=1
#             data += '</table>' 
#             table = '<table border="1" width="50%" style="border-collapse: collapse;text-align:center;">'
#             table += '''
#             <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
#                 <td style='width:3%'><b>SPOC</b></td>
#                 <td style='width:3%'><b>APH</b></td>
#                 <td style='width:3%'><b>PR[#/hr]</b></td>
#                 <td style='width:3%'><b>Working[#/hr]</b></td>
#                 <td style='width:3%'><b>CR[#/hr]</b></td>
#                 <td style='width:3%'><b>Issue[#/hr]</b></td>
#                 <td style='width:3%'><b>RT</b></td>
#                 <td style='width:8%'><b>RT Vs APH %</b></td>
#             </tr>
#             '''
#             task_det=frappe.db.get_all("Task",{"custom_production_date_cs":date,"type":type,"service":service},['*'],order_by='spoc asc',group_by='spoc asc')
#             value=0
#             pending_total=0
#             working_total=0
#             cr_total=0
#             issue_total=0
#             pr_time_total=0
#             working_time_total=0
#             cr_time_total=0
#             issue_time_total=0
#             total_pr=0
#             total_working=0
#             total_cr=0
#             total_issue=0
#             for k in task_det:
#                 emp_cb=frappe.db.get_value('Employee',{'user_id':k.spoc},['short_code'])
#                 actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
#                 sum_rt=frappe.db.sql("""select sum(pr_expected_time) as rt from `tabTask` where spoc=%s and custom_production_date_cs=%s and type='CS' group by spoc""",(k.spoc,date), as_dict=True)
#                 sum_pr_rt=frappe.db.sql("""select sum(pr_expected_time) as rt from `tabTask` where spoc=%s and custom_production_date_cs=%s and type='CS' and status !="Client Review" group by spoc""",(k.spoc,date), as_dict=True)                
#                 pr_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":type,"service":service,"spoc":k.spoc,"status":"Pending Review"})
#                 working_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":type,"service":service,"spoc":k.spoc,"status":"Working"})
#                 cr_count=frappe.db.count("Task",{"custom_production_date_cs":date,"type":type,"service":service,"spoc":k.spoc,"status":"Client Review"})
#                 issue_count=frappe.db.count("Issue",{"custom_production_date":date,"custom_spoc":k.spoc,"status":"Open"})                
#                 total_pr+=pr_count
#                 total_working+=working_count
#                 total_cr+=cr_count
#                 total_issue+=issue_count
#                 pr_time=frappe.db.sql(
#                     """
#                     SELECT SUM(pr_expected_time) AS et
#                     FROM `tabTask`
#                     WHERE spoc = %s AND custom_production_date_cs = %s AND type = 'CS' AND status='Pending Review'
#                     GROUP BY spoc
#                     """,
#                     (k.spoc, date),
#                     as_dict=True,
#                     )
#                 cr_time=frappe.db.sql(
#                     """
#                     SELECT SUM(pr_expected_time) AS et
#                     FROM `tabTask`
#                     WHERE spoc = %s AND custom_production_date_cs = %s AND type = 'CS' AND status='Client Review'
#                     GROUP BY spoc
#                     """,
#                     (k.spoc, date),
#                     as_dict=True,
#                     )
#                 working_time=frappe.db.sql(
#                     """
#                     SELECT SUM(pr_expected_time) AS et
#                     FROM `tabTask`
#                     WHERE spoc = %s AND custom_production_date_cs = %s AND type = 'CS' AND status='Working'
#                     GROUP BY spoc
#                     """,
#                     (k.spoc, date),
#                     as_dict=True,
#                     )
#                 issue_time=frappe.db.sql(
#                     """
#                     SELECT SUM(custom_excepted_time_cs) AS et
#                     FROM `tabIssue`
#                     WHERE custom_spoc = %s AND custom_production_date = %s AND status = 'Open'
#                     GROUP BY custom_spoc
#                     """,
#                     (k.spoc, date),
#                     as_dict=True,
#                     )
#                 pending_total+=float(pr_count)
#                 working_total+=float(working_count)
#                 cr_total+=float(cr_count)
#                 issue_total+=float(issue_count)
#                 if pr_time:
#                     pr_time_total+=pr_time[0].et
#                 if cr_time:
#                     cr_time_total=cr_time[0].et
#                 if working_time:
#                     working_time_total=working_time[0].et
#                 if issue_time:
#                     issue_time_total=issue_time[0].et
#                 if sum_pr_rt:
#                     total+=sum_pr_rt[0].rt
#                 if actual_aph is not None:
#                     value=actual_aph
#                     aph_total+=float(value)
#                 if sum_pr_rt and actual_aph is not None:
#                     total_count=float(total)/float(aph_total)*100
#                     percent=(float(sum_rt[0].rt)/float(actual_aph))*100
#                 if percent:
#                     table += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
#                         emp_cb,
#                         value or '8',
#                         "%s/%s" % (pr_count, pr_time[0].et if pr_time else '0.0'),
#                         "%s/%s" % (working_count, working_time[0].et if working_time else '0.0'),
#                         "%s/%s" % (cr_count, cr_time[0].et if cr_time else '0.0'),
#                         "%s/%s" % (issue_count, issue_time[0].et if issue_time else '0.0'),
#                         sum_rt[0].rt if sum_rt else '0',
#                         round(percent, 2) or '-'
#                     )
#                 else:
#                     table += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
#                         emp_cb,
#                         actual_aph or '',
#                         "%s/%s" % (pr_count, pr_time[0].et if pr_time else '0.0'),
#                         "%s/%s" % (working_count, working_time[0].et if working_time else '0.0'),
#                         "%s/%s" % (cr_count, cr_time[0].et if cr_time else '0.0'),
#                         "%s/%s" % (issue_count, issue_time[0].et if issue_time else '0.0'),
#                         sum_rt[0].rt if sum_rt else '0',
#                         round(percent, 2) or '-'
#                     )

#             table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
#                 aph_total,
#                 "%s/%s" % (total_pr,pr_time_total or '0.0'),
#                 "%s/%s" % (total_working,working_time_total or '0.0'),
#                 "%s/%s" % (total_cr,cr_time_total or '0.0'),
#                 "%s/%s" % (total_issue,issue_time_total or '0.0'),
#                 round(total, 2) if total else '0',  # Removed extra comma
#                 round(total_count, 2) if total_count else '0'
#             )

#             table+='</table>'
#             frappe.sendmail(
#                     # sender='sarath.v@groupteampro.com',
#                     recipients='divya.p@groupteampro.com',
#                     # recipients=['sarath.v@groupteampro.com','sivarenisha.m@groupteampro.com','jeniba.a@groupteampro.com'],
#                     # cc=['dineshbabu.k@groupteampro.com','anil.p@groupteampro.com','abdulla.pi@groupteampro.com'],
#                     subject = f'{service} - {type} DPR {formatted_date} -Reg',
#                     message = """
#                     <b>Dear Team,</b><br><br>
#     Please find the below DPR for {} for your kind reference and action, ensure all the Tasks allocated on time and as per the requirement.<br><br>

#                 {}<br><br>
#                 {}<br><br>
#                     Thanks & Regards,<br>TEAM ERP<br>
                    
#                     <i>This email has been automatically generated. Please do not reply</i>
#                     """.format(formatted_date,table if table else '',data)
#                 )
#             frappe.msgprint("DPR mail has been successfully sent")
#             task_data.dm_status='DPR Completed'
#             task_data.dpr_submitted_on=today()
#             task_data.save()
#             frappe.db.commit()
