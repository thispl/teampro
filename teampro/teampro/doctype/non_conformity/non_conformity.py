# Copyright (c) 2023, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class NonConformity(Document):
	def validate(self):
		self.nc_reported_by = frappe.get_value('Employee',{'user_id':frappe.session.user},'name')
		self.name3 = frappe.get_value('Employee',{'user_id':frappe.session.user},'employee_name')
		self.nc_department = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
		self.nc_designation = frappe.get_value('Employee',{'user_id':frappe.session.user},'designation')
		self.nc_class_confirmed=self.nc_class_proposed
		if self.nc_class_confirmed=='Minor':
			self.energy_score='-1'
		elif self.nc_class_confirmed=='Major':
			self.energy_score='-2'
		elif self.nc_class_confirmed=='Critical':
			self.energy_score='-3'