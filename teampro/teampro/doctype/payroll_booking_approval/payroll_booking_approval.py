# Copyright (c) 2026, Teampro
# See license.txt

import frappe
from frappe.model.document import Document


class PayrollBookingApproval(Document):
	def validate(self):
		if not self.start_date or not self.end_date:
			frappe.throw("Start Date and End Date are required")
		if self.start_date > self.end_date:
			frappe.throw("Start Date cannot be after End Date")
