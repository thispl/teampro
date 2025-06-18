import frappe
from datetime import datetime

def get_context(context):
    context.ptsr_data = get_ptsr_data()

@frappe.whitelist(allow_guest=True)
def get_ptsr_data():
    from datetime import datetime
    posting_date = datetime.now().strftime("%d-%m-%Y")
    data_list = []
    cust = frappe.db.sql("""SELECT * FROM `tabCustomer` WHERE `disabled` = 0 AND service IN ('REC-I','REC-D') ORDER BY `customer_name` ASC""", as_dict=True)

    ev_total = 0
    grand_totals = {'vac': 0, 'sp': 0, 'fp': 0, 'sl': 0, 'psl': 0, 'custom_lp': 0}

    for c in cust:
        pname = frappe.get_all("Project", {"status": ("in", ['Open', 'Enquiry']), "customer": c['name'], "service": ("in", ['REC-I', 'REC-D'])}, ['*'], order_by="priority ASC")
        task_totals = {'vac': 0, 'sp': 0, 'fp': 0, 'sl': 0, 'psl': 0, 'custom_lp': 0}
        for p in pname:
            try:
                ev_total += float(p.get('expected_value', 0) or 0)
            except ValueError:
                frappe.log_error(f"Expected value is not a number for project {p.get('project_name')}", "Data Error in PSR Report")

            taskid = frappe.get_all("Task", {"status": ("in", ('Working', 'Open', 'Overdue', 'Pending Review')), "project": p.name}, ['*'], order_by="priority ASC")
            total = frappe.db.sql("""
                                SELECT
                                    SUM(vac) AS vac,
                                    SUM(sp) AS sp,
                                    SUM(fp) AS fp,
                                    SUM(sl) AS sl,
                                    SUM(psl) AS psl,
                                    SUM(custom_lp) AS lp
                                FROM `tabTask`
                                WHERE
                                    status IN ("Working", "Open", "Overdue", "Pending Review")
                                    AND project = %s
                                """, (p.name,), as_dict=True)[0]


            task_chunks = [taskid[i:i + 15] for i in range(0, len(taskid), 15)]
            s_no = 1
            
            for chunk_index, chunk in enumerate(task_chunks):
                # Initialize data for this chunk
                data = f'''<div class="zoom-out-content"><h6 style="text-align:center; font-weight: 700;">REC : Project - Task Status Report - {posting_date}</h6>'''
                data += '<table border="1" style="border-collapse: width: 100%; collapse; font-size: 10px; scroll-behavior: smooth;">'
                data += '''<tr style="background-color: #002060; color: white;">
                        <td style="text-align:center; min-width: 2%; color:white;">S.NO</td>
                        <td style="text-align:center; min-width: 8%; color:white;">Customer / Project Name</td>
                        <td style="text-align:center; min-width: 5%; color:white;">Project Priority</td>
                        <td style="text-align:center; min-width: 13%; color:white;">AM Remark</td>
                        <td style="text-align:center; min-width: 13%; color:white;">PM Remark</td>
                        <td style="text-align:center; min-width: 13%; color:white;">Spoc Remark</td>
                        <td style="text-align:center; min-width: 5.5%; color:white;">Expected Value</td>
                        <td style="text-align:center; min-width: 4.5%; color:white;">Expected PSL</td>
                        <td style="text-align:center; min-width: 6%; color:white;">Sourcing Status</td>
                        <td style="text-align:center; min-width: 3.2%; color:white;">Territory</td>
                        <td style="text-align:center; min-width: 4.5%; color:white;">Task</td>
                        <td style="text-align:center; min-width: 4%; color:white;">Task Priority</td>
                        <td style="text-align:center; min-width: 2%; color:white;">#VAC</td>
                        <td style="text-align:center; min-width: 2%; color:white;">#SP</td>
                        <td style="text-align:center; min-width: 2%; color:white;">#FP</td>
                        <td style="text-align:center; min-width: 2%; color:white;">#SL</td>
                        <td style="text-align:center; min-width: 2%; color:white;">#PSL</td>
                        <td style="text-align:center; min-width: 2%; color:white;">#LP</td>
                        </tr>'''

                # Add customer/project row
                data += f'''<tr style="background-color: #98d7f5;">
                        <td colspan=12 style="padding-left: 20px;"><b>{c.name}</b></td>
                        <td style="text-align:center;">{int(total.vac or 0)}</td>
                        <td style="text-align:center;">{int(total.sp or 0)}</td>
                        <td style="text-align:center;">{int(total.fp or 0)}</td>
                        <td style="text-align:center;">{int(total.sl or 0)}</td>
                        <td style="text-align:center;">{int(total.psl or 0)}</td>
                        <td style="text-align:center;">{int(total.custom_lp or 0)}</td>
                        </tr>'''

                # Add task rows
                for t in chunk:
                    data += f'''<tr>
                            <td style="text-align:center;">{s_no}</td>
                            <td style="text-align:left;">{p.project_name}</td>
                            <td style="text-align:center;">{p.priority}</td>
                            <td style="text-align:left;">{p.remark or ""}</td>
                            <td style="text-align:left;">{p.account_manager_remark or ""}</td>
                            <td style="text-align:left;">{p.custom_spoc_remark or ""}</td>
                            <td style="text-align:center;">{p.expected_value}</td>
                            <td style="text-align:center;">{p.expected_psl}</td>
                            <td style="text-align:center;">{p.sourcing_statu}</td>
                            <td style="text-align:center;">{p.territory}</td>
                            <td style="text-align:left;">{t.subject}</td>
                            <td style="text-align:center;">{t.priority}</td>
                            <td style="text-align:center;">{t.vac or 0}</td>
                            <td style="text-align:center;">{t.sp or 0}</td>
                            <td style="text-align:center;">{t.fp or 0}</td>
                            <td style="text-align:center;">{t.sl or 0}</td>
                            <td style="text-align:center;">{t.pl or 0}</td>
                            <td style="text-align:center;">{t.custom_lp or 0}</td>
                            </tr>'''
                    s_no += 1
                    task_totals['vac'] += t.get('vac', 0)
                    task_totals['sp'] += t.get('sp', 0)
                    task_totals['fp'] += t.get('fp', 0)
                    task_totals['sl'] += t.get('sl', 0)
                    task_totals['psl'] += t.get('psl', 0)
                    task_totals['custom_lp'] += t.get('custom_lp', 0)

                # Add totals for the chunk
                data += f'''<tr style="background-color: #002060;">
                            <td></td>
                            <td style="text-align:center; font-weight: bold;color: #ffffff;">Total</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style="text-align:center; font-weight: bold; color: #ffffff;">{task_totals["vac"]}</td>
                            <td style="text-align:center; font-weight: bold;color: #ffffff;">{task_totals["sp"]}</td>
                            <td style="text-align:center; font-weight: bold; color: #ffffff;">{task_totals["fp"]}</td>
                            <td style="text-align:center; font-weight: bold; color: #ffffff;">{task_totals["sl"]}</td>
                            <td style="text-align:center; font-weight: bold; color: #ffffff;">{task_totals["psl"]}</td>
                            <td style="text-align:center; font-weight: bold; color: #ffffff;">{task_totals["custom_lp"]}</td>
                        </tr>'''

                # Close table and div
                data += '</table></div>'
                data_list.append(data)  # Append the chunk to the data list


    return data_list
