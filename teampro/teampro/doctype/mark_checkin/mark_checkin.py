# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MarkCheckin(Document):
	pass


@frappe.whitelist()
def create_checkin(user_id, checkin_time):
    employee = frappe.db.get_value('Employee', {'user_id': user_id}, 'name')
    if employee:
        if frappe.db.exists('Employee', {'name': employee}):
            if not frappe.db.exists('Employee Checkin', {'employee': employee, 'time': checkin_time}):
                ec = frappe.new_doc('Employee Checkin')
                ec.employee = employee
                ec.time = checkin_time
                ec.log_type = "IN"
                ec.save(ignore_permissions=True)
                frappe.db.commit()  
                return "True" 
            else:
                return "False"  
        else:
            return "False" 
   

