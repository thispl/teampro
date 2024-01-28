# Copyright (c) 2023, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ApprovalSummary(Document):
	@frappe.whitelist()
	def get_leave_app(self):
		data = frappe.get_list("Leave Application",{"workflow_state":"Pending for HOD"},["name","employee","employee_name","leave_type",	"from_date","to_date","total_leave_days","workflow_state"])
		return data

	@frappe.whitelist()
	def get_att_req(self):
		att_req = frappe.get_list("Attendance Request",{"workflow_state":"Pending for HOD"},["name","employee","employee_name","workflow_state","from_date","to_date","explanation"])
		return att_req

	@frappe.whitelist()
	def get_expence_claim(self):
		# active_employees = frappe.get_list("Employee", {"status": "Active"}, ["name"])
		# for employee in active_employees:
		employee_expenses = frappe.get_list("Expense Claim",{"workflow_state":"Pending for HOD"},["name","workflow_state","employee","employee_name","expense_approver","total_claimed_amount"])
		return employee_expenses

	@frappe.whitelist()
	def get_expence_claim_md(self):
		# active_employees = frappe.get_list("Employee", {"status": "Active"}, ["name"])
		# for employee in active_employees:
		employee_expenses = frappe.get_list("Expense Claim",{"workflow_state":"Pending for MD"},["name","workflow_state","employee","employee_name","expense_approver","total_claimed_amount"])
		return employee_expenses

	

	@frappe.whitelist()
	def get_purchase_invoice(self):
		data = frappe.get_list("Purchase Invoice",{"workflow_state":"Pending for MD"},["name","supplier","posting_date","workflow_state"])
		return data

	@frappe.whitelist()
	def get_purchase_invoice_ceo(self):
		data = frappe.get_list("Purchase Invoice",{"workflow_state":"Pending for CEO"},["name","supplier","posting_date","workflow_state"])
		return data
	

	@frappe.whitelist()
	def submit_quote(self,doctype,name,work_flow):
		frappe.db.set_value(doctype,name,"work_flow",work_flow)
		return "ok"

	@frappe.whitelist()
	def submit_doc(self,doctype,name,workflow_state):
		doc = frappe.get_doc(doctype,name)
		doc.workflow_state = workflow_state
		# doc.save(ignore_permissions=True)
		doc.submit()
		return "ok"
	

	@frappe.whitelist()
	def submit_document(self,doctype,name,docstatus):
		doc = frappe.get_doc(doctype,name)
		doc.docstatus = docstatus
		# doc.save(ignore_permissions=True)
		doc.submit()
		return "ok"

	@frappe.whitelist()
	def submit_all_doc_after_approval(self,doctype,name,workflow_state):
		frappe.db.set_value(doctype,name,"workflow_state",workflow_state)
		return "ok"