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
		_("CB") +":Data/:150",
				("Allocated To") +":Data/:150",

		_("Project") + ":Data/:150",
		_("Task ID") + ":Data/:150",
		_("Subject") + ":Data/:200",
		_("Priority") + ":Data/:200",
		_("Status") + ":Data/:150",
		_("Revisions") + ":Data/:150",
		_("ET") + ":Data/:150",
		_("AT(Total)") + ":Data/:150",
		_("AT(Period)") + ":Data/:150",
		_("ET Vs AT") + ":Data/:150",
		_("ET Vs AT %" )+":Data/:150",
		_("CDR Comment" )+":Data/:250",
	]
	return columns

def get_data(filters):
	data = []
	if filters.completed_by:
		emp = frappe.get_value(
			"Employee",
			{'user_id': filters['completed_by'], 'status': 'Active'},
			['name', 'user_id'],
			as_dict=True
		)

		if emp:
			emp_short_code = frappe.db.get_value("Employee", {"name": emp.name}, ["short_code"])

			tasks = frappe.get_all(
				"Task",
				filters={
					"custom_allocated_to": emp.user_id,
					"custom_allocated_on": ["between", [filters.from_date, filters.to_date]]
				},
				fields=[
					"name",
					"project",
					"subject",
					"priority",
					"status",
					"revisions",
					"expected_time",
					"custom_code_reviewer_comment",
					"custom_allocated_to"
				]
			)

			for t in tasks:

				# actual time (optional - if still needed from timesheet)
				actual_time = frappe.db.sql("""
					SELECT SUM(td.hours) as hours
					FROM `tabTimesheet` ts
					LEFT JOIN `tabTimesheet Detail` td ON ts.name = td.parent
					WHERE ts.docstatus = 1
					AND td.task = %s
					AND td.activity_type != "Manual Testing"
				""", (t.name,), as_dict=1)

				atime = actual_time[0].hours if actual_time and actual_time[0].hours else 0

				etime = atime - (t.expected_time or 0)

				if t.expected_time and t.expected_time > 0:
					etper = (atime / t.expected_time) * 100
				else:
					etper = 0

				row = [
					emp.name,
					emp_short_code,
					t.custom_allocated_to,
					t.project,
					t.name,
					t.subject,
					t.priority,
					t.status,
					t.revisions,
					t.expected_time,
					round(atime, 2),
					0,  # timesheet hours remove panna, so 0
					round(etime, 2),
					round(etper, 2),
					t.custom_code_reviewer_comment
				]

				data.append(row)
				
	else:
		employees = frappe.get_all(
			"Employee",
			filters={'department': "IT. Development - THIS", 'status': "Active"},
			fields=['name', 'employee_name', 'short_code', 'user_id']
		)

		for e in employees:

			tasks = frappe.get_all(
				"Task",
				filters={
					"custom_allocated_to": e.user_id,
					"custom_allocated_on": ["between", [filters.from_date, filters.to_date]]
				},
				fields=[
					"name",
					"project",
					"subject",
					"priority",
					"status",
					"revisions",
					"expected_time",
					"custom_code_reviewer_comment",
					"custom_allocated_to"
				]
			)

			for t in tasks:

				actual_time = frappe.db.sql("""
					SELECT SUM(td.hours) as hours
					FROM `tabTimesheet` ts
					LEFT JOIN `tabTimesheet Detail` td ON ts.name = td.parent
					WHERE 
						ts.docstatus = 1
						AND td.task = %s
						AND td.activity_type != "Manual Testing"
				""", (t.name,), as_dict=1)

				atime = actual_time[0].hours if actual_time and actual_time[0].hours else 0

				etime = atime - (t.expected_time or 0)

				if t.expected_time and t.expected_time > 0:
					etper = (atime / t.expected_time) * 100
				else:
					etper = 0

				row = [
					e.name,
					e.short_code,
					t.custom_allocated_to,
					t.project,
					t.name,
					t.subject,
					t.priority,
					t.status,
					t.revisions,
					t.expected_time,
					round(atime, 2),
					0,
					round(etime, 2),
					round(etper, 2),
					t.custom_code_reviewer_comment
				]

				data.append(row)

		return data