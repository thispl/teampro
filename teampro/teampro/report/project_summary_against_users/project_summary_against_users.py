# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days,date_diff
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
    columns = []
    columns += [
        _("Project") + ":Data/:200",
        _("User") + ":Data/:200",
        _("Task") + ":Data/:200",
        _("Total Hours") + ":Data/:200",
    ]
    return columns

def get_data(filters):
	data = []
	if filters.project:
		project = frappe.db.sql("""select * from `tabProject` where name = '%s' and service = "IT-SW" and company = '%s' """%(filters.project,filters.company),as_dict = True)
	else:
		project = frappe.db.sql("""select * from `tabProject` where company = '%s' and service = "IT-SW" """%(filters.company),as_dict = True)
	for p in project:
		project_hours = frappe.db.sql("""select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent  where `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.project = '%s' and start_date between '%s' and '%s' """%(p.name,filters.from_date,filters.to_date),as_dict = 1)
		pt_hrs = project_hours[0].hours if project_hours and project_hours[0].hours is not None else 0
		data.append([p.name, '', '',f"{pt_hrs:.2f}"])
		# user = frappe.db.sql("""select * from `tabTask` where project = '%s' and exp_start_date between '%s' and '%s' and custom_allocated_to != '' order by custom_allocated_to ASC """ % (p.name,.from_date,filters.to_date), as_dict=True)
		user = frappe.db.sql("""select * from `tabTask` where project = '%s' and custom_allocated_to != '' group by custom_allocated_to ASC """ % (p.name), as_dict=True)
		for u in user:
			employee , employee_name = frappe.db.get_value("Employee",{'user_id':u.custom_allocated_to},['name','employee_name'])
			project_hours = frappe.db.sql("""select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent  where `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.project = '%s' and `tabTimesheet`.employee = '%s' and  start_date between '%s' and '%s' """%(p.name,employee,filters.from_date,filters.to_date),as_dict = 1)
			pt_hrs = project_hours[0].hours if project_hours and project_hours[0].hours is not None else 0
			if pt_hrs > 0:
				data.append(['', employee_name, '', f"{pt_hrs:.2f}"])
				timesheet = frappe.db.sql("""select `tabTimesheet Detail`.task as task from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.project = '%s' and `tabTimesheet`.employee = '%s' and  start_date between '%s' and '%s' group by `tabTimesheet Detail`.task """%(p.name,employee,filters.from_date,filters.to_date),as_dict = 1)
				for t in timesheet:
					project_hours = frappe.db.sql("""select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent  where `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.task = '%s' and `tabTimesheet`.employee = '%s' and  start_date between '%s' and '%s' """%(t.task,employee,filters.from_date,filters.to_date),as_dict = 1)
					pt_hrs = project_hours[0].hours if project_hours and project_hours[0].hours is not None else 0
					data.append(['', '', t.task,f"{pt_hrs:.2f}"])
	return data		

@frappe.whitelist()
def get_to_date(from_date):
	return get_last_day(from_date)