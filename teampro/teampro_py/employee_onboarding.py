import frappe

def after_insert_employee_onboarding(doc, method):
    frappe.msgprint(f"Employee Onboarding Created for {doc.employee}")

    if doc.employee_onboarding_template:
        activities = frappe.get_all(
            "Employee Boarding Activity",
            fields=[
                "activity_name", "role", "user", "required_for_employee_creation",
                "description", "task_weight", "begin_on", "duration"
            ],
            filters={"parent": doc.employee_onboarding_template, "parenttype": "Employee Onboarding Template"},
            order_by="idx",
        )
        chc=frappe.get_all(
            "Employee Boarding Activity",
            fields=[
                "activity_name", "role", "user", "required_for_employee_creation",
                "description", "task_weight", "begin_on", "duration"
            ],
            filters={"parent": doc.custom_employee_chc_template, "parenttype": "Employee Onboarding Template"},
            order_by="idx",
        )
        for activity in activities:
            new_activity = doc.append("activities", {})
            new_activity.update(activity)
        for i in chc:
            new_chc=doc.append("custom_employee_chc", {})
            new_chc.update(i)
        job_offer=frappe.db.get_value("Job Offer",{"job_applicant":doc.job_applicant},["name"])
        doc.job_offer=job_offer
        doc.save()
        # frappe.msgprint(f"Activities added from template {doc.employee_onboarding_template}")

def on_submit_employee_onboarding(doc, method):
    pending_activities = [i.activity_name for i in doc.activities if i.status == "Pending"]
    pending_custom_activities = [j.activity_name for j in doc.custom_employee_chc if j.status == "Pending"]
    if pending_activities or pending_custom_activities:
        pending_list = pending_activities + pending_custom_activities
        frappe.throw(f"The following activities are pending: {', '.join(pending_list)}. Kindly complete them before submission.")
    if frappe.db.exists("Employee Onboarding",{"employee": doc.employee,"docstatus": 1}):
        employee = frappe.get_doc("Employee", doc.employee)
        employee.workflow_state = "Joined"
        employee.save(ignore_permissions=True)
        frappe.msgprint(f"Employee {doc.employee} has been successfully set as active.")
