import frappe
@frappe.whitelist()
def get_child(parent):
    if parent:
        so = frappe.get_doc("Candidate", parent)
        if so.table_28:
            return so.table_28
