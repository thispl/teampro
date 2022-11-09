# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TargetPlanner(Document):
	def validate(self):
		if frappe.db.exists("Target Allocation",{'year':self.year,'employee':self.employee}):
			frappe.throw("Target for %s is already Allocated for %s "%(self.employee_name,self.year))

def calculate_target_on_update(self,method):
	calculate_target()

@frappe.whitelist()
def calculate_target():
	tps = frappe.get_all('Target Planner',['*'])
	map_months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
	for tp in tps:
		doc = frappe.get_doc('Target Planner',tp.name)
		if tp.target_based_unit == 'Service Based':
			servs = frappe.get_all('Employee services',{'parent':tp.name},['services'])
			service_list = []
			for serv in servs:
				service_list.append(serv.services)
			service_list = (str(service_list).replace('[','')).replace(']','')
			pending_ct = 0
			pending_ft = 0
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				year = tp.year
				achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status != 'Cancelled' """%(service_list,month,year),as_dict=True)[0].total or 0
				tc.revised_ct = tc.ct + pending_ct
				tc.revised_ft = tc.ft + pending_ft
				tc.achieved = achieved
				tc.ct_yta = tc.revised_ct - achieved
				tc.ft_yta = tc.revised_ft - achieved
				pending_ct = tc.revised_ct - achieved
				pending_ft = tc.revised_ft - achieved
				doc.save(ignore_permissions=True)
				frappe.db.commit()
		elif tp.target_based_unit == 'Account Based':
			ac = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
			if ac:
				pending_ct = 0
				pending_ft = 0
				for tc in doc.target_child:
					month = map_months.get(tc.month)
					year = tp.year
					am_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where account_manager = '%s' and delivery_manager != '%s' and month(creation) = %s and year(creation) = %s and status != 'Cancelled' """%(ac,ac,month,year),as_dict=True)[0].total or 0
					dm_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where delivery_manager = '%s' and account_manager != '%s' and month(creation) = %s and year(creation) = %s and status != 'Cancelled' """%(ac,ac,month,year),as_dict=True)[0].total or 0
					am_dm_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where delivery_manager = '%s' and account_manager = '%s' and month(creation) = %s and year(creation) = %s and status != 'Cancelled' """%(ac,ac,month,year),as_dict=True)[0].total or 0
					tc.revised_ct = tc.ct + pending_ct
					tc.revised_ft = tc.ft + pending_ft
					achieved = am_achieved + dm_achieved + am_dm_achieved
					tc.achieved = achieved
					tc.ct_yta = tc.revised_ct - achieved
					tc.ft_yta = tc.revised_ft - achieved
					pending_ct = tc.revised_ct - achieved
					pending_ft = tc.revised_ft - achieved
					doc.save(ignore_permissions=True)
					frappe.db.commit()

	return 'OK'

def test_method():
	d = frappe.db.sql("select creation from `tabSales Invoice` where delivery_manager = account_manager and month(creation) = 2 ",as_dict=True)
	print(d)