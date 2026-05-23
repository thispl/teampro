// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["IT-SW DSR"] = {
	"filters": [
        {
            fieldname: "date",
            label: __("Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today()
        }
    ]
};
