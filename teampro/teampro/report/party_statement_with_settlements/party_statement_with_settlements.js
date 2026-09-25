// Party Statement (with Settlements) - filter setup
frappe.query_reports["Party Statement (with Settlements)"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Link",
			options: "DocType",
			get_query: function () {
				return {
					filters: [
						["name", "in", ["Customer", "Supplier", "Employee", "Donor", "Member"]],
					],
				};
			},
			default: "Supplier",
			reqd: 1,
			on_change: function () {
				var pt = frappe.query_report.get_filter_value("party_type");
				var party_filter = frappe.query_report.get_filter("party");
				if (pt) {
					party_filter.df.options = pt;
				} else {
					party_filter.df.options = "";
				}
				frappe.query_report.set_filter_value("party", "");
				party_filter.refresh();
			},
		},
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "Link",
			options: "Supplier",
			reqd: 1,
			get_query: function () {
				var pt = frappe.query_report.get_filter_value("party_type");
				return { filters: pt ? {} : [["name", "=", ""]] };
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -12),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "presentation_currency",
			label: __("Currency"),
			fieldtype: "Link",
			options: "Currency",
		},
	],
};
