// Copyright (c) 2022, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Target Manager', {
	refresh: function (frm) {
		frappe.breadcrumbs.add("HR", "Target Manager");
		if (frm.doc.__islocal) {
			// var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
			var months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec","Jan", "Feb", "Mar"]
			var month_no = {'Apr':'12','May':'11','Jun':'10','Jul':'9','Aug':'8','Sep':'7','Oct':'6','Nov':'5','Dec':'4','Jan':'3','Feb':'2','Mar':'1'}
			if (frm.doc.target_child.length == 0) {
				$.each(months, function (i, v) {
					frm.add_child("target_child", {
						'month': v,
						'month_nos': month_no[v]  
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
		frm.add_custom_button(("Submit"), function () {
		$.each(frm.fields_dict, function(fieldname, field) {
			frm.set_df_property(fieldname, 'read_only', 1);
			});
		});

	},
	annual_ct(frm){
		var months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'];
		var month_no = {'Apr':'12','May':'11','Jun':'10','Jul':'9','Aug':'8','Sep':'7','Oct':'6','Nov':'5','Dec':'4','Jan':'3','Feb':'2','Mar':'1'}
		var value = frm.doc.annual_ct / 12;
		frm.clear_table('target_child');  
		$.each(months, function(i, month) {
			frm.add_child("target_child", {
				'month': month, 
				'month_nos': month_no[month], 
				'ct': value
			});
		});

		frm.refresh_field('target_child');
	},
	annual_ft(frm){
		var values = frm.doc.annual_ft / 12;
		$.each(frm.doc.target_child, function(i, row) {
			row.ft = values;
		});

    frm.refresh_field('target_child');
	},
	update_target(frm) {
		frappe.call({
			// method: "teampro.teampro.doctype.target_manager.target_manager.calculate_target",
			method: "teampro.teampro.doctype.target_manager.target_manager.calculate_target_for_manager",
			callback(r) {
				if (r.message == 'OK') {
					frappe.msgprint("Target Updated Successfully")
					frm.reload_doc();
				}
			}
		})
	},
	// onload: function(frm) {
    //     const today = new Date();
    //     const year = today.getFullYear();
    //     let fiscalYear;
    //     if (today.getMonth() + 1 >= 4) {  
    //         fiscalYear = year;
    //     } else {  
    //         fiscalYear = year + 1;
    //     }
    //     frm.set_value('year', fiscalYear);
    // }
});
