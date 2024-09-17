# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EnergyPointsAllocation(Document):
	def validate(self):
		self.ep_reported_by = frappe.get_value('Employee',{'user_id':frappe.session.user},'name')
		self.name3 = frappe.get_value('Employee',{'user_id':frappe.session.user},'employee_name')
		self.nc_dep = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
		self.nc_des = frappe.get_value('Employee',{'user_id':frappe.session.user},'designation')
		self.ep_class_confirmed=self.ep_class_proposed
		if self.ep_class_confirmed=='Good':
			self.energy_score='+1'
		elif self.ep_class_confirmed=='Very Good':
			self.energy_score='+2'
		elif self.ep_class_confirmed=='Excellent':
			self.energy_score='+3'
