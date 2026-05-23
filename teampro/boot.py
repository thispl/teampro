import frappe

def get_boot_data(bootinfo):

    user = frappe.session.user

    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")

    if not employee:
        bootinfo.has_target_manager = False
        return

    target_exists = frappe.db.exists("Target Manager", {"employee": employee})

    bootinfo.has_target_manager = True if target_exists else False