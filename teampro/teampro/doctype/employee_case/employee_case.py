# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeCase(Document):
    pass
	# def on_submit(self):
	# 	self.status='Submitted'
	# def validate(self):

	# 	# ---------- AADHAR ----------
	# 	if self.aadhar_no:
	# 		found = False
	# 		for i in self.employee_case_details:
	# 			if i.title_of_attachment == "Aadhar":
	# 				i.attachment_id = self.aadhar_no
	# 				i.attach = self.aadhar_link   # weblink
	# 				found = True
	# 				break

	# 		if not found:
	# 			self.append("employee_case_details", {
	# 				"title_of_attachment": "Aadhar",
	# 				"attachment_id": self.aadhar_no,
	# 				"attach": self.aadhar_link
	# 			})

	# 	# ---------- PAN ----------
	# 	if self.pan_no:
	# 		found = False
	# 		for i in self.employee_case_details:
	# 			if i.title_of_attachment == "PAN":
	# 				i.attachment_id = self.pan_no
	# 				if self.pan_link:
	# 					i.attach = self.pan_link      # weblink
	# 				found = True
	# 				break

	# 		if not found:
	# 			self.append("employee_case_details", {
	# 				"title_of_attachment": "PAN",
	# 				"attachment_id": self.pan_no,
	# 				"attach": self.pan_link if self.pan_link else None
	# 			})


		
