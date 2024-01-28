// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Food Request Report"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"width": "100",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
		},
		// {
		// 	"fieldname": "employee",
		// 	"label": __("Employee"),
		// 	"fieldtype": "Link",
		// 	"width": "180",
		// 	"options": "Employee",
		// },
	]
};
