# Copyright (c) 2025, TeamPRO and contributors
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
		_("Task ID") + ":Data/:100",
		_("Project") +":Data/:150",
		_("Subject") + ":Data/:250",
		_("CB") + ":Data/:50",
		_("Status") + ":Data/:100",
		_("ET") + ":Data/:50",
		_("RT") + ":Data/:50",
		_("AT") + ":Data/:50",
		_("Priority") + ":Data/:100",
		_("Spot Task") + ":Data/:100",
		_("Current Status") + ":Data/:150",
		_("Remarks") + ":Data/:300:Align/Center",
	]
	return columns

def get_data(filters):
	data = []
	if filters:
		if filters.sprint and filters.dev_team:
			task_data = frappe.db.sql("""
				SELECT name, project, subject, custom_allocated_to, status, expected_time, rt, actual_time, priority, custom_spot_task, custom_remarks
				FROM `tabTask`
				WHERE custom_dev_team = %s AND custom_sprint = %s
				ORDER BY custom_allocated_to,project
			""", (filters.dev_team, filters.sprint), as_dict=1)
		elif filters.sprint and filters.dev_team is None:
			task_data = frappe.db.sql("""
				SELECT name, project, subject, custom_allocated_to, status, expected_time, rt, actual_time, priority, custom_spot_task, custom_remarks
				FROM `tabTask`
				WHERE custom_sprint = %s
				ORDER BY custom_allocated_to,project
			""", (filters.sprint), as_dict=1)
		elif filters.sprint is None and filters.dev_team:
			task_data = frappe.db.sql("""
				SELECT name, project, subject, custom_allocated_to, status, expected_time, rt, actual_time, priority, custom_spot_task, custom_remarks
				FROM `tabTask`
				WHERE custom_dev_team = %s
				ORDER BY custom_allocated_to,project
			""", (filters.dev_team), as_dict=1)
		row = []
		for task in task_data:
			if task.custom_spot_task:
				spot_task = 1
			else:
				spot_task = 0
			emp_short_code=frappe.db.get_value("Employee",{"user_id":task.custom_allocated_to},["short_code"])
			employee=frappe.db.get_value("Employee",{"user_id":task.custom_allocated_to},["name"])
			actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join 
			`tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and 
			`tabTimesheet`.employee = '%s' and `tabTimesheet Detail`.task = '%s' """%(employee,task.name),as_dict = 1) or ''
			actual_hours = actual_time[0].get('hours', 0) or 0
			row = [task.name,task.project,task.subject,emp_short_code,"Working",task.expected_time,task.rt,
			round(actual_hours, 2),task.priority,spot_task,task.status,task.custom_remarks]
			data.append(row)
	return data
	