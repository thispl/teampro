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
	tawh = wh_utilized = remaining_wh = 0
	projects = frappe.get_all('Project',{'service':'IT',},['*'])
	for project in projects:
		project_status = frappe.get_value('Project',project.project,'status')
		tewh = frappe.db.sql("""select sum(expected_time) as hours from `tabTask` where project= '{project}' """.format(project=project.name),as_dict=1)[0]
		query = """select sum(hours) as hours from `tabTimesheet Detail` where project= '{project}' """.format(project=project.name)
		timesheet_hours = frappe.db.sql(query,as_dict=1)[0]
		if timesheet_hours.hours:
			tawh = round(timesheet_hours.hours,2)
		ts_dates = frappe.db.sql("""select min(date(from_time)) as tsd,max(date(to_time)) as ted from `tabTimesheet Detail` where project= '{project}' """.format(project=project.name),as_dict=1)[0]
		
		row = [project.name,project.status,project.expected_start_date,project.expected_end_date,tewh.hours,tawh,wh_utilized,remaining_wh]
		data.append(row)
	return data

def get_columns():
	return [
		
			{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 120
		},
			{
			"label": _("Status"),
			"fieldname": "status",
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
			"label": _("TEWH"),
			"fieldname": "ewh",
			"fieldtype": "float",
			"width": 80
		},
		{
			"label": _("TAWH"),
			"fieldname": "awh",
			"fieldtype": "float",
			"width": 80
		},
		{
			"label": _("WH Utilized"),
			"fieldname": "wh_utilized",
			"fieldtype": "float",
			"width": 120
		},
		{
			"label": _("Remaining WH"),
			"fieldname": "remaining_wh",
			"fieldtype": "float",
			"width": 100
		}
	]

	return columns