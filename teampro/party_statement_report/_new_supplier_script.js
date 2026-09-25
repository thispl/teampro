frappe.ui.form.on('Supplier', {
	refresh(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Statement"), function() {
				var party = frm.doc.name;
				var company = frappe.defaults.get_user_default("Company");
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype: "Fiscal Year",
						filters: { disabled: 0, year_start_date: ["<=", frappe.datetime.get_today()], year_end_date: [">=", frappe.datetime.get_today()] },
						fieldname: "year_start_date, year_end_date",
					},
					callback: function(r) {
						var fy_start = r && r.message && r.message.year_start_date ? r.message.year_start_date : frappe.datetime.add_months(frappe.datetime.get_today(), -12);
						var fy_end = r && r.message && r.message.year_end_date ? r.message.year_end_date : frappe.datetime.get_today();
						var d = new frappe.ui.Dialog({
							title: __("Statement of Account"),
							fields: [
								{ label: __("Company"), fieldname: "company", fieldtype: "Link", options: "Company", default: company, reqd: 1 },
								{ label: __("From Date"), fieldname: "from_date", fieldtype: "Date", default: fy_start, reqd: 1 },
								{ label: __("To Date"), fieldname: "to_date", fieldtype: "Date", default: fy_end, reqd: 1 },
							],
							primary_action_label: __("Download PDF"),
							primary_action: function() {
								var values = d.get_values();
								if (!values) return;
								d.hide();
								var url = "/api/method/teampro.utility.download_party_statement_pdf"
									+ "?party_type=Supplier"
									+ "&party=" + encodeURIComponent(party)
									+ "&from_date=" + encodeURIComponent(values.from_date)
									+ "&to_date=" + encodeURIComponent(values.to_date)
									+ "&company=" + encodeURIComponent(values.company);
								window.open(url, "_blank");
							},
							secondary_action_label: __("View Statement"),
							secondary_action: function() {
								var values = d.get_values();
								if (!values) return;
								d.hide();
								frappe.call({
									method: "teampro.utility.get_party_statement",
									args: {
										party_type: "Supplier",
										party: party,
										from_date: values.from_date,
										to_date: values.to_date,
										company: values.company,
									},
									freeze: true,
									freeze_message: __("Generating Statement..."),
									callback: function(r) {
										if (r && r.message && r.message.html) {
											var w = window.open("", "_blank");
											w.document.write(r.message.html);
											w.document.close();
										}
									}
								});
							}
						});
						d.show();
						// Add Excel download button
						$(d.footer).find('.btn-secondary').before(
							'<button class="btn btn-default btn-sm btn-excel" style="margin-right: 5px;">Download Excel</button>'
						);
						$(d.footer).find('.btn-excel').on('click', function() {
							var values = d.get_values();
							if (!values) return;
							d.hide();
							var url = "/api/method/teampro.utility.download_party_statement_excel"
								+ "?party_type=Supplier"
								+ "&party=" + encodeURIComponent(party)
								+ "&from_date=" + encodeURIComponent(values.from_date)
								+ "&to_date=" + encodeURIComponent(values.to_date)
								+ "&company=" + encodeURIComponent(values.company);
							window.open(url, "_blank");
						});
					}
				});
			}, __("View"));
		}
	}
});
