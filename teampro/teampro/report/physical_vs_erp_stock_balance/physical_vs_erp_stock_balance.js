// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["Physical VS ERP Stock Balance"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        }
	],
    formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "status") {
			if (value === "Variance") {
				value = `<span style="color:red; font-weight:bold;">${value}</span>`;
			} else if (value === "Match") {
				value = `<span style="color:green; font-weight:bold;">${value}</span>`;
			}
		}

		return value;
	}
    
};
