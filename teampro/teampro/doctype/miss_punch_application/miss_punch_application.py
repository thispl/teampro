# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MissPunchApplication(Document):

	def on_submit(self):
		att = frappe.db.exists('Attendance',{'attendance_date':self.date,'employee':self.employee})
		# frappe.errprint(att)
		if att:
			frappe.db.set_value('Attendance',att,'in_time',self.in_time)
			frappe.db.set_value('Attendance',att,'out_time',self.out_time)
			frappe.db.set_value('Attendance',att,'shift',self.shift)
			frappe.db.set_value("Attendance",att,"status","Present")
			frappe.db.set_value('Attendance',att,'miss_punch_marked',self.name)
			self.attendance = att
