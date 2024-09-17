# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BGEntryForm(Document):
	pass
@frappe.whitelist()
def val_bg_form(email_id):
    if frappe.db.exists("BG Entry Form",{"email_id":email_id}):
        return "No"
    
@frappe.whitelist(allow_guest=True)
def mark_files_public(doc,method):
	if doc.document_required:
		if frappe.db.exists("File",{"file_url":doc.document_required}):
			filename = frappe.db.get_value("File",{"file_url":doc.document_required},"name")
			frappe.db.set_value("File",filename,'is_private',0)
	if doc.education_document_required:
		if frappe.db.exists("File",{"file_url":doc.education_document_required}):
			filename = frappe.db.get_value("File",{"file_url":doc.education_document_required},"name")
			frappe.db.set_value("File",filename,'is_private',0)
	if doc.documents_required:
		if frappe.db.exists("File",{"file_url":doc.documents_required}):
			filename = frappe.db.get_value("File",{"file_url":doc.documents_required},"name")
			frappe.db.set_value("File",filename,'is_private',0)
	if doc.document_required11:
		if frappe.db.exists("File",{"file_url":doc.document_required11}):
			filename = frappe.db.get_value("File",{"file_url":doc.document_required11},"name")
			frappe.db.set_value("File",filename,'is_private',0)
	if doc.criminal_check_document_required:
		if frappe.db.exists("File",{"file_url":doc.criminal_check_document_required}):
			filename = frappe.db.get_value("File",{"file_url":doc.criminal_check_document_required},"name")
			frappe.db.set_value("File",filename,'is_private',0)
	if doc.scanned_document_required:
		if frappe.db.exists("File",{"file_url":doc.scanned_document_required}):
			filename = frappe.db.get_value("File",{"file_url":doc.scanned_document_required},"name")
			frappe.db.set_value("File",filename,'is_private',0)
