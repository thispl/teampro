// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order Outstanding"] = {
	"filters": [
		{
			"fieldname":"sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": "100px"
		},
		
		
	]
};
