// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["Project Summary against Users"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd":1,
			on_change: function () {
				var from_date = frappe.query_report.get_filter_value('from_date')
				frappe.call({
					method: "teampro.teampro.report.project_summary_against_users.project_summary_against_users.get_to_date",
					args: {
						from_date: from_date
					},
					callback(r) {
						frappe.query_report.set_filter_value('to_date', r.message);
						frappe.query_report.refresh();
					}
				})
			},
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd":1
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd":1
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname":"user",
			"label": __("User"),
			"fieldtype": "Link",
			"options": "User"
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
		if(value >= 50 && column.colIndex == 4 ){
            value = "<span style='color:green!important;font-weight:bold;text-align:center'>" + value + "</span>";
		}
		if( value < 50 && column.colIndex == 4 ){
            value = "<span style='color:Red!important;font-weight:bold;text-align:center'>" + value + "</span>";
		}
		if (column.colIndex == 1) {
			value = "<span style='color:green!important;font-weight:bold;text-align:center'>" + value + "</span>";
		}
		if (column.colIndex == 2) {
			value = "<span style='color:Red!important;font-weight:bold;text-align:center'>" + value + "</span>";
		}
        return value;
    }
};