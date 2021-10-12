// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["TIIP"] = {
	
	"filters": [
		{			
			"fieldname":"month_based",
			"label": __("Month Based"),
			"fieldtype": "Check",			
		},
		{
			"fieldname":"yearly",
			"label": __("Yearly"),
			"fieldtype": "Link",
			"options": "Yearly",
			"default": "2021",
			// on_change: () => {
			// 	var yearly = frappe.query_report.get_filter_value('yearly');
			// 	if (yearly) {
					
			// 		frappe.query_report.set_filter_value('from_date', "");
			// 		frappe.query_report.set_filter_value('to_date', "");
			// 	}
			// 	frappe.query_report.refresh();
			// }

		},
		{			
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			"depends_on": 'eval:doc.month_based!=1',	
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"depends_on": 'eval:doc.month_based!=1',
		},
		
		{
			"fieldname":"half_yearly",
			"label": __("Half-Yearly"),
			"fieldtype": "Link",
			"options": "Half Yearly",
			"depends_on": 'eval:doc.month_based',
			on_change: () => {
				var half_yearly = frappe.query_report.get_filter_value('half_yearly');
				if (half_yearly) {
					frappe.query_report.set_filter_value('quarterly', "");
					frappe.query_report.set_filter_value('month', "");
					frappe.query_report.set_filter_value('from_date', "");
					frappe.query_report.set_filter_value('to_date', "");
				}
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"quarterly",
			"label": __("Quarterly"),
			"fieldtype": "Link",
			"options": "Quarterly",
			"depends_on": 'eval:doc.month_based',
			on_change: () => {
				var quarterly = frappe.query_report.get_filter_value('quarterly');
				if (quarterly) {
					frappe.query_report.set_filter_value('month', "");
					frappe.query_report.set_filter_value('half_yearly', "");
					frappe.query_report.set_filter_value('from_date', "");
					frappe.query_report.set_filter_value('to_date', "");
				}
				frappe.query_report.refresh();
			}
			

		},
		
		{
			"fieldname": "month",
			"label": __("Monthly"),
			"fieldtype": "Select",
			// "default":"0",
			// "read_only_depends_on":"eval:doc.from_date",
			"options": [
				// { "value": 0, "label": __("Monthly") },
				{ "value": 1, "label": __("Jan") },
				{ "value": 2, "label": __("Feb") },
				{ "value": 3, "label": __("Mar") },
				{ "value": 4, "label": __("Apr") },
				{ "value": 5, "label": __("May") },
				{ "value": 6, "label": __("June") },
				{ "value": 7, "label": __("July") },
				{ "value": 8, "label": __("Aug") },
				{ "value": 9, "label": __("Sep") },
				{ "value": 10, "label": __("Oct") },
				{ "value": 11, "label": __("Nov") },
				{ "value": 12, "label": __("Dec") },
			],
			"depends_on": 'eval:doc.month_based',
			on_change: () => {
				frappe.query_report.refresh();
				var month = frappe.query_report.get_filter_value('month');
				if (month) {
					frappe.query_report.set_filter_value('quarterly', "");
					frappe.query_report.set_filter_value('half_yearly', "");
					frappe.query_report.set_filter_value('from_date', "");
					frappe.query_report.set_filter_value('to_date', "");
				}
			}
			// "default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		},
		
		
	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if(value > 0){
            value = "<span style='color:green!important;font-weight:bold'>" + value + "</span>";
		}
		if( value < 0){
            value = "<span style='color:Red!important;font-weight:bold'>" + value + "</span>";
		}
		if( value == 0){
            value = "<span style='color:Red!important;font-weight:bold'>" + value + "</span>";
		}
		// if( column.content == "FT-Pending"){
        //     value = "<span style='color:Blue!important;font-weight:bold'>" + value + "</span>";
        // }

        return value;
    }	
};