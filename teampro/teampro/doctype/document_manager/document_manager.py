# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, date_diff
from frappe.model.document import Document


class DocumentManager(Document):
	pass




def update_statuses():
    doc_obj = frappe.get_doc("Document Manager")  
    updated = False

    for row in doc_obj.document_manager:
        if row.category == "Renewable" and row.expiry_date:
            age = date_diff(today(), row.expiry_date)
            if age > 0 and row.status != "Inactive":
                row.status = "Inactive"
                updated = True
            elif age <= 0 and row.status != "Active":
                row.status = "Active"
                updated = True
        else:
            if row.status != "Active":
                row.status = "Active"
                updated = True

    if updated:
        doc_obj.save(ignore_permissions=True)



@frappe.whitelist()
def create_schedule_job_doc_manager():
    job = frappe.db.exists('Scheduled Job Type', 'update_statuses')
    if not job:
        exp = frappe.new_doc("Scheduled Job Type")
        exp.update({
            "method": 'teampro.teampro.doctype.document_manager.document_manager.update_statuses',
            "frequency": 'Daily'
            
        })
        exp.save(ignore_permissions=True)