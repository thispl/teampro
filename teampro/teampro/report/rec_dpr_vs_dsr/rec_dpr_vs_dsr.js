// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["REC DPR Vs DSR"] = {
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
			"fieldname": "allocated_to",
			"label": __("Allocated To"),
			"fieldtype": "Link",
			"width": "180",
			"options": "User",
		},

	]
};
