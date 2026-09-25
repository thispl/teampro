# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class LunchAttendanceSettings(Document):
	def validate(self):
		if self.enabled:
			if not self.whatsapp_template_name:
				frappe.throw(_("Please select a WhatsApp Template"))
			if not self.sending_time or not self.cutoff_time:
				frappe.throw(_("Sending Time and Cutoff Time are required"))
			if self.sending_time >= self.cutoff_time:
				frappe.throw(_("Sending Time must be earlier than Cutoff Time"))
			if self.create_lunch_entry_on_yes and not self.lunch_entry_doctype:
				frappe.throw(_("Please select a Lunch Entry DocType"))
