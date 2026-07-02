# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EnergyPointAndNonConformity(Document):
	def autoname(self):
		if self.action == "Energy Point(EP)":
			self.naming_series = "EP"
		else:
			self.naming_series = "NC"
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

@frappe.whitelist()
def nc_for_check_reject(name=None,id=None,allocated=None,class_proposed=None,reason=None):
    if allocated:
        emp_id=frappe.db.get_value("Employee",{'user_id':allocated},['name'])
        reopen_cause='(%s) Check :(%s) Rejected .Reason(%s)' % (name,id,reason)
        nc = frappe.new_doc('Energy Point And Non Conformity')
        nc.emp = emp_id
        nc.action='Non Conformity(NC)'
        nc.class_proposed = class_proposed
        nc.reason_of_ep = reopen_cause
        nc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Energy Point And Non Conformity", nc.name, "workflow_state", "Explanation")
        frappe.db.commit()
        return {"status": "success", "message": "NC created"}

import frappe
from frappe.utils import add_days, getdate, today

def auto_submit_ep1():
    cutoff_date = add_days(getdate(today()), -2)

    print(cutoff_date)
    active_emps = frappe.get_all("Employee", filters={"status": "Active"}, pluck="name")
    for employee in active_emps:
        print(employee)
        docs = frappe.db.sql("""
            SELECT name, workflow_state
            FROM `tabEnergy Point And Non Conformity`
            WHERE workflow_state IN ('Draft', 'Explanation')
            AND action = 'Non Conformity(NC)'
            AND docstatus = 0
            AND DATE(creation) <= %s
            AND emp = %s
        """, (cutoff_date,employee), as_dict=True)
        print(docs)
        for row in docs:
            name = row.name
            doc = frappe.get_doc("Energy Point And Non Conformity", name)

            if row.workflow_state == "Draft":
                # frappe.errprint(f"Moving {name} from Draft → Explanation")
                doc.workflow_state = "Explanation"
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                doc.workflow_state = "Submitted"
                doc.docstatus = 1
                doc.save(ignore_permissions=True)
                frappe.db.commit()

            if row.workflow_state == "Explanation":
                # frappe.errprint(f"Auto-submitting {name}")
                doc.workflow_state = "Submitted"
                doc.docstatus = 1
                doc.save(ignore_permissions=True)
                frappe.db.commit()
				
from frappe.utils import get_first_day, get_last_day, format_datetime, get_url_to_form

@frappe.whitelist()
def create_new_epnc_review():
    employee=frappe.db.get_all("Employee",{"status":"Active"},["*"])
    today_date=today()
    start_date=get_first_day(today_date)
    end_date=get_last_day(today_date)
    for i in employee:
        doc=frappe.new_doc("Monthly EP NC Review")
        doc.start_date=start_date
        doc.end_date=end_date
        doc.employee=i.name
        doc.total_score='100'
        doc.save()
    frappe.db.commit()