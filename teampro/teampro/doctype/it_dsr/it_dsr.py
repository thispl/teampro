# # Copyright (c) 2024, TeamPRO and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ITDSR(Document):
    pass

@frappe.whitelist()
def get_task(name,date):
# def get_task():
#     name= "TI00150"
#     date= "2024-06-20"
    data_list = []
    total_task_list ={}
    user_id= frappe.get_value("Employee",{"name":name},"user_id")
    task_list=frappe.get_all("Task",{"status":["in",["Open","Working","Overdue"]],'custom_allocated_on': ['<=',date],"custom_allocated_to":user_id},["name","project","subject","custom_allocated_to","custom_allocated_on","completed_by","cb","actual_time"])
    # frappe.errprint(task_list)
    for t in task_list:
        total_task_list.update({
            'task_id':t.name,
            'project':t.project,
            'subject':t.subject,
            'custom_allocated_to':t.custom_allocated_to,
            'custom_allocated_on':t.custom_allocated_on,
            'cb':t.cb,
            'actual_time':t.actual_time,
            'over_all_actual_time':0
        })
        data_list.append(total_task_list.copy())
        # frappe.errprint(data_list)
    return data_list

@frappe.whitelist()
def get_timesheet(name, date):
# def get_timesheet():
#     name= "TC00042"
#     date= "2024-06-19"
    datalist = []
    data = {}
    timesheet_names = frappe.db.sql("""SELECT name FROM `tabTimesheet` WHERE employee = %s AND start_date = %s AND docstatus = 1 """, (name, date), as_dict=1)
    ts = []
    for t in timesheet_names:
        ts.append(t.name)
    ts_tuple=tuple(ts)
    if len(ts_tuple) != 0:
        query = """SELECT 
                `tabTimesheet Detail`.task, SUM(`tabTimesheet Detail`.hours) AS hours 
            FROM `tabTimesheet` 
            LEFT JOIN `tabTimesheet Detail` 
            ON `tabTimesheet`.name = `tabTimesheet Detail`.parent
            WHERE `tabTimesheet`.docstatus = 1 AND `tabTimesheet Detail`.parent IN %s 
            GROUP BY `tabTimesheet Detail`.task """
        task_hours = frappe.db.sql(query, (ts_tuple,), as_dict=True)
        for t in task_hours:
            data.update({
                'task_id':t.task,
                'project':frappe.get_value("Task",{'name':t.task},['project']),
                'subject':frappe.get_value("Task",{'name':t.task},['subject']),
                'custom_allocated_to':frappe.get_value("Task",{'name':t.task},['custom_allocated_to']),
                'custom_allocated_on':frappe.get_value("Task",{'name':t.task},['custom_allocated_on']),
                'cb':frappe.get_value("Task",{'name':t.task},['cb']),
                # 'expected_time':frappe.get_value("Task",{'name':t.task},['expected_time']),
                'actual_time':frappe.get_value("Task",{'name':t.task},['actual_time']),
                'over_all_actual_time':t.hours
            })
            datalist.append(data.copy())
            # frappe.errprint(datalist)
        return datalist
 




