// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["Sprint Wise Report"] = {
	"filters": [
		
		{
			"fieldname": "sprint",
			"label": __("Sprint"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Task Sprint",
		},
		{
			"fieldname": "dev_team",
			"label": __("Dev Team"),
			"fieldtype": "Link",
			"width": "100",
			"options": "Dev Team",
		},

	]
};
