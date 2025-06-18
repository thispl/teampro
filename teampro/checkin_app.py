import frappe
import requests

@frappe.whitelist()
def get_employee_data(user):
    if frappe.db.exists("Employee", {"user_id": user, "status": "Active"}):
        employee = frappe.get_doc("Employee", {"user_id": user, "status": "Active"})
        return employee
    else:
        return "Employee Not Found"
    
# @frappe.whitelist()
# def get_last_punch(employee):