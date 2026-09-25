# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff


class LatePenalty(Document):
	def validate(self):
		# When late_days is manually changed, recalculate actual_late and deduction_days
		allowed_late = 3
		late = 0

		if self.late_days:
			actual_late = int(self.late_days) - allowed_late
			at = max(0, actual_late)
		else:
			at = 0

		if at >= 3:
			if at <= 5:
				late = 0.5
			elif at <= 8:
				late = 1
			elif at <= 11:
				late = 1.5
			elif at <= 14:
				late = 2
			elif at <= 17:
				late = 2.5
			elif at <= 20:
				late = 3
			elif at <= 23:
				late = 3.5
			elif at <= 26:
				late = 4
			elif at <= 29:
				late = 4.5
			else:
				late = 5
		else:
			late = 0

		self.actual_late = at
		self.deduction_days = late

		# Recalculate penalty amount if we have salary structure + dates
		if self.from_date and self.to_date and self.emp_name:
			ssa = frappe.db.sql("""
				SELECT base, variable
				FROM `tabSalary Structure Assignment`
				WHERE employee = %s AND docstatus = 1
				ORDER BY from_date DESC LIMIT 1
			""", [self.emp_name], as_dict=True)
			if ssa:
				days = date_diff(self.to_date, self.from_date) + 1
				base = int(ssa[0].base or 0)
				variable = int(ssa[0].variable or 0)
				if days > 0:
					self.late_penalty = late * (base + variable) / days
				else:
					self.late_penalty = 0
			else:
				self.late_penalty = 0
		else:
			self.late_penalty = 0
