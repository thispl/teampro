// Copyright (c) 2022, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Target Planner', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("HR", "Target Planner");
		if (frm.doc.__islocal) {
			var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
			if (!frm.doc.target_child) {
				$.each(months, function (i, v) {
					frm.add_child("target_child", {
						'month': v
					})
					frm.refresh_field('target_child')
				})
			}
		}
		frm.set_query("employee", function () {
			return {
				"filters": {
					"status": 'Active'
				}
			};
		});
	},
	update_target(frm) {
		frappe.call({
			method: "teampro.teampro.doctype.target_planner.target_planner.calculate_target",
			callback(r) {
				if (r.message == 'OK') {
					frappe.msgprint("Target Updated Successfully")
					frm.reload_doc();
				}
			}
		})
	}
});
