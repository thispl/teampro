// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["AT Period Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "100",
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "100",
			"reqd": 1,
		},
		{
			"fieldname": "completed_by",
			"label": __("CB"),
			"fieldtype": "Link",
			"width": "180",
			"options": "User",
			// "reqd": 1,
		},


	]
};
