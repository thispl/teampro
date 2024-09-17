# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff,format_datetime
from datetime import date, timedelta, datetime, time
from frappe.utils import (
	add_days,
	cstr,
	flt,
	format_datetime,
	formatdate,
	get_datetime,
	get_first_day,
	get_last_day,
	get_link_to_form,
	get_number_format_info,
	getdate,
	nowdate,
)

class MonthlyEnergyPointNonConformity(Document):
	pass
@frappe.whitelist()
def mo_epnc(emp,from_date,to_date,emp_name):
	data = """<table class='table table-bordered' style='border-collapse: collapse; width: 100%;'><tr style='border: 1px solid black; background-color: #0f1568; color: white;'><th>S No</th><th>Employee ID</th><th>Employee Name</th><th>Energy Score</th><th>NC Score</th></tr>"""
	# e= frappe.get_all("Energy Point  Non Conformity",{"emp":emp,"docstatus":0},["emp","name3","energy_score","total"])
	ep = frappe.db.sql(
	"""
	SELECT sum(total) as total,sum(total_nc) as total_nc, emp_name as emp_name,emp as emp from `tabEnergy Point And Non Conformity` where date(creation) BETWEEN %s AND %s AND docstatus=1 group by emp""", (from_date,to_date), as_dict=True)
	s_no=0
	for i in ep:
		s_no+=1
		data += """<tr style='border: 1px solid black;'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"""%(s_no,i.emp,i.emp_name,i['total'],i['total_nc'])
	data += "</table>"
	return data
	



