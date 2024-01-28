# Copyright (c) 2023, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
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
		_("Employee") + ":Data/:150",
		_("Project") + ":Data/:150",
		_("Task ID") + ":Data/:150",
		_("Subject") + ":Data/:200",
		_("Status") + ":Data/:150",
		_("Revisions") + ":Data/:150",
		_("ET") + ":Data/:150",
		_("AT(Total)") + ":Data/:150",
		_("AT(Period)") + ":Data/:150",
	]
	return columns

def get_data(filters):
	data = []
	if filters.completed_by:
		emp = frappe.get_value("Employee",{'user_id':filters['completed_by'],'status':'Active'},['name'])
		if emp:
			row = []
			timesheet = frappe.db.sql(""" select `tabTimesheet Detail`.task as task,sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and  employee = '%s' and start_date between '%s' and '%s' group by `tabTimesheet Detail`.task"""%(emp,filters.from_date,filters.to_date),as_dict = 1)
			for j in timesheet:
				task = frappe.get_value("Task",{'name':j.task},['project','subject','status','revisions','expected_time'])
				actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.task = '%s' """%(j.task),as_dict = 1) or ''
				for at in actual_time:
					atime = at.hours
					row = [emp,task[0],j.task,task[1],task[2],task[3],task[4],atime,j.hours]
				data.append(row)
	else:
		emp = frappe.get_all("Employee",{'department':"ITS - THIS",'status':"Active"},['name',"employee_name"])
		frappe.errprint(emp)
		for e in emp:
			frappe.errprint(e.name)
			row = []
			timesheet = frappe.db.sql(""" select `tabTimesheet Detail`.task as task,sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent  where `tabTimesheet`.docstatus = 1 and employee = '%s' and start_date between '%s' and '%s' group by `tabTimesheet Detail`.task"""%(e.name,filters.from_date,filters.to_date),as_dict = 1) or ''
			for j in timesheet:
				task = frappe.get_value("Task",{'name':j.task},['project','subject','status','revisions','expected_time'])
				actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent  where `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.task = '%s' """%(j.task),as_dict = 1)
				for at in actual_time:
					atime = at.hours
					row = [e.employee_name or '',task[0] or '',j.task or '',task[1] or '',task[2] or '',task[3] or '',task[4] or '',atime or '',j.hours or '']
				data.append(row)
	return data
	
