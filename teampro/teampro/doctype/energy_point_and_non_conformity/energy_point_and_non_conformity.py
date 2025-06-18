# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EnergyPointAndNonConformity(Document):
	def validate(self):
		self.ep_reported_by = frappe.get_value('Employee',{'user_id':frappe.session.user},'name')
		self.name3 = frappe.get_value('Employee',{'user_id':frappe.session.user},'employee_name')
		self.nc_dep = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
		self.nc_des = frappe.get_value('Employee',{'user_id':frappe.session.user},'designation')
		self.ep_class_confirmed=self.ep_class_proposed

		# if self.workflow_state == 'Submitted':
		if self.ep_class_confirmed=='Good':
			self.energy_score='+1'
			self.total=1
		elif self.ep_class_confirmed=='Very Good':
			self.energy_score='+2'
			self.total=2
		elif self.ep_class_confirmed=='Excellent':
			self.energy_score='+3'
			self.total=3
		
		self.class_confirmed=self.class_proposed
		if self.class_confirmed=='Minor':
			self.nc_score='-1'
			self.total_nc=1
		elif self.class_confirmed=='Major':
			self.nc_score='-2'
			self.total_nc=2
		elif self.class_confirmed=='Critical':
			self.nc_score='-3'	
			self.total_nc=3

		# elif self.workflow_state=='NC Revoked':
		# 	self.class_confirmed=self.class_proposed
		# 	if self.class_confirmed=='Minor':
		# 		self.nc_score='1'
		# 		self.total_nc=1
		# 	elif self.class_confirmed=='Major':
		# 		self.nc_score='2'
		# 		self.total_nc=2
		# 	elif self.class_confirmed=='Critical':
		# 		self.nc_score='3'	
		# 		self.total_nc=3



