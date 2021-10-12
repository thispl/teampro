// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Late In"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		// {
		// 	"fieldname":"shift",
		// 	"label": __("Shift"),
		// 	"fieldtype": "Link",
		// 	"options": "Shift Type",
		// },
		// {
		// 	"fieldname":"department",
		// 	"label": __("Department"),
		// 	"fieldtype": "Link",
		// 	"options": "Department",
		// },

	]
};
