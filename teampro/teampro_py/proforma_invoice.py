import frappe
@frappe.whitelist()
def get_so_details(so):
    sales_order = frappe.get_doc("Sales Order",so)
    return sales_order.items