# Copyright (c) 2026, Teampro
# See license.txt

import frappe
from frappe.model.document import Document


class PayrollPeriodApproval(Document):
	def validate(self):
		if not self.start_date or not self.end_date:
			frappe.throw("Start Date and End Date are required")
		if self.start_date > self.end_date:
			frappe.throw("Start Date cannot be after End Date")

	def on_update(self):
		# Prevent duplicate approvals for the same period + company
		if self.status == "Approved":
			existing = frappe.db.sql(
				"""
				SELECT name FROM `tabPayroll Period Approval`
				WHERE company = %s
				  AND start_date = %s
				  AND end_date = %s
				  AND status = 'Approved'
				  AND name != %s
				""",
				(self.company, self.start_date, self.end_date, self.name),
			)
			if existing:
				frappe.throw(
					f"Attendance for this period is already approved ({existing[0][0]})"
				)
