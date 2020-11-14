// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["IT Services Task Status Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Open\nWorking\nPending Review\nCompleted\nAll",
			"default": "All",
			"reqd": 1
		},
	]
};
