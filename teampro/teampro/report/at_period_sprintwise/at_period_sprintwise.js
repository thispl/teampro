// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["AT Period Sprintwise"] = {
	"filters": [
		{
			label:"From Date",
			fieldname:"from_date",
			fieldtype:"Date",
			reqd:1
		},
		{
			label:"To Date",
			fieldname:"to_date",
			fieldtype:"Date",
			reqd:1
		},
		{
			label:"Dev Team",
			fieldname:"team",
			fieldtype:"Link",
			options:"Dev Team"
		},
		{
			label:"User",
			fieldname:"user",
			fieldtype:"Link",
			options:"User"
		}
	]
};
