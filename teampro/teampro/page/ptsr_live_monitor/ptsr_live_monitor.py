import frappe
from frappe import _
from frappe.utils import getdate, flt, today, nowdate

@frappe.whitelist()
def get_ptsr_data():
    data = []
    cust = frappe.db.sql("""SELECT * FROM `tabCustomer` WHERE `disabled` = 0 AND service IN ('REC-I','REC-D') ORDER BY `customer_name` ASC""", as_dict=True)
    
    for c in cust:
        project_data = []
        pname = frappe.get_all("Project", {"status": ("in", ['Open', 'Enquiry']), "customer": c['name'], "service": ("in", ['REC-I', 'REC-D'])}, ['*'], order_by="priority ASC")
        if not pname:
            continue

        for p in pname:
            task_list = frappe.get_all("Task", {"status": ("in", ('Working', 'Open', 'Overdue', 'Pending Review')), "project": p.name}, ['*'], order_by="priority ASC")
            tasks = [{
                "name":t['name'],
                "task_name": t['subject'],
                "task_priority": t['priority'],
                "vac": t['vac'],
                "sp": t['sp'],
                "fp": t['fp'],
                "sl": t['sl'],
                "psl": t['psl'],
                "custom_lp": t['custom_lp']
            } for t in task_list]

            project_data.append({
                "name":p['name'],
                "project_name": p['project_name'],
                "priority": p['priority'],
                "remark": p['remark'],
                "account_manager_remark": p['account_manager_remark'],
                "custom_spoc_remark": p['custom_spoc_remark'],
                "sourcing_statu": p['sourcing_statu'],
                "territory": p['territory'],
                "expected_value": p['expected_value'],
                "expected_psl": p['expected_psl'],
                "tasks": tasks
            })

        data.append({"customer_name": c['name'], "projects": project_data})

    return data

@frappe.whitelist()
def update_project_remark(projects):
    import json
    projects = json.loads(projects)

    for project_name, fields in projects.items():
        # frappe.log_error(title="projects updating",message=project_name)
        # frappe.log_error(title="Projects Fields updating",message=fields)
        frappe.db.set_value("Project", project_name, fields)

    frappe.db.commit()
    return "Projects updated successfully"

import frappe
import json

@frappe.whitelist()
def update_task_priority(tasks):
    try:
        tasks = json.loads(tasks)  # Convert JSON string to dictionary

        for task_name, fields in tasks.items():
            # frappe.log_error(title="Task Updating", message=task_name)
            # frappe.log_error(title="Task Fields Updating", message=fields)
            frappe.db.set_value("Task", task_name, fields)

        frappe.db.commit()
        return "Tasks updated successfully"

    except Exception as e:
        frappe.log_error(title="Task Priority Update Error", message=str(e))
        return f"Error: {str(e)}"

