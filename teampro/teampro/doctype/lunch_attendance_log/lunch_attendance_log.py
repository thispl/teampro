# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class LunchAttendanceLog(Document):
	def before_insert(self):
		self._enforce_uniqueness()

	def validate(self):
		if not self.employee_name:
			self.employee_name = frappe.db.get_value(
				"Employee", self.employee, "employee_name"
			)
		if self.response in ("Yes", "No") and not self.responded_at:
			self.responded_at = frappe.utils.now()

	def _enforce_uniqueness(self):
		"""Ensure only ONE Lunch Attendance Log per employee per date."""
		exists = frappe.db.exists(
			"Lunch Attendance Log",
			{"employee": self.employee, "date": self.date},
		)
		if exists:
			frappe.throw(
				_("Lunch Attendance Log {0} already exists for employee {1} on {2}").format(
					exists, self.employee, self.date
				),
				frappe.DuplicateEntryError,
			)
