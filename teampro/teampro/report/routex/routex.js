// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["RouteX"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"reqd":1,
			"default": frappe.datetime.month_start()
		},
		{
			"label": __("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"reqd":1,
			"default": frappe.datetime.get_today()
		},
		{
			"label": __("Department"),
			"fieldname": "department",
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"label": __("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee"
		},
	]
};