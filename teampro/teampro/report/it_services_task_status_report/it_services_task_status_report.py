# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,json
from frappe import msgprint, _

def execute(filters=None):
	columns, data = [], []
	row = []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	row = []
	data = []
	resource = ''
	if filters.status == 'All':
		tasks = frappe.get_all('Task',{'service':'IT'},['*'])
	else:
		tasks = frappe.get_all('Task',{'service':'IT','status':filters.status},['*'])
	for task in tasks:
		awh = 0
		project_status = frappe.get_value('Project',task.project,'status')
		query = """select sum(hours) as hours from `tabTimesheet Detail` where task= '{task}' """.format(task=task.name)
		ts_dates = frappe.db.sql("""select min(date(from_time)) as tsd,max(date(to_time)) as ted from `tabTimesheet Detail` where task= '{task}' """.format(task=task.name),as_dict=1)[0]
		tsd = ts_dates.tsd
		ted = ts_dates.ted
		timesheet_hours = frappe.db.sql(query,as_dict=1)[0]
		if timesheet_hours.hours:
			awh = round(timesheet_hours.hours,2)
		if task._assign:
			assigned_to = json.loads(task._assign)
			if assigned_to:
				resource = frappe.get_value('Employee',{'user_id':assigned_to[0]},['short_code'])
		row = [task.name,task.subject,task.status,task.project,project_status,task.exp_start_date,task.exp_end_date,task.expected_time,awh,resource,tsd,ted]
		data.append(row)
	return data

def get_columns():
	return [
		{
			"label": _("Task ID"),
			"fieldname": "task",
			"fieldtype": "Link",
			"options": "Task",
			"width": 120
		},
			{
			"label": _("Subject"),
			"fieldname": "subject",
			"fieldtype": "Data",
			"width": 300
		},
		{
			"label": _("Task Status"),
			"fieldname": "task_status",
			"fieldtype": "Data",
			"width": 120
		},
			{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 120
		},
			{
			"label": _("Project Status"),
			"fieldname": "project_status",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("ESD"),
			"fieldname": "esd",
			"fieldtype": "Date",
			"width": 100
		},
			{
			"label": _("EED"),
			"fieldname": "eed",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("EWH"),
			"fieldname": "ewh",
			"fieldtype": "float",
			"width": 80
		},
		{
			"label": _("AWH"),
			"fieldname": "awh",
			"fieldtype": "float",
			"width": 80
		},
		{
			"label": _("Resource"),
			"fieldname": "resource",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("TSD"),
			"fieldname": "tsd",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("TED"),
			"fieldname": "ted",
			"fieldtype": "Date",
			"width": 100
		}
	]

	return columns