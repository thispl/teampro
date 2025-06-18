// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase Invoice Booked(TGT)"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1,
            "width": "100",
			"default": frappe.datetime.get_today().slice(0, 7) + "-01" // First day of current month
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1,
            "width": "100",
			"default": frappe.datetime.get_today()
        },
        // {
        //     "fieldname": "company",
        //     "label": __("Company"),
        //     "fieldtype": "Link",
        //     "options": "Company",
        //     "width": "100",
		// 	"default": frappe.defaults.get_user_default("Company")
        // }

	],
    "onload": function (report) {
        // Hide filters by default
        report.page.sidebar.hide();

        // Listen for number card click event
        frappe.query_reports["Purchase Invoice Booked(TGT)"].toggle_filters_on_card_selection(report);
    },

    "toggle_filters_on_card_selection": function (report) {
        // Custom function to toggle filters
        $(document).on("click", ".number-card-container", function () {
            // Show filters when number card is clicked
            report.page.sidebar.show();
        });
    }
};
