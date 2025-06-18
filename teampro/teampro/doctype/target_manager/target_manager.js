// Copyright (c) 2022, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Target Manager', {
	custom_fiscal_year: async function(frm) {
		let is_valid = await frappe.call({
			method: "teampro.teampro.doctype.target_manager.target_manager.validate_fiscal_year",
			args: {
				employee: frm.doc.employee,
				year: frm.doc.custom_fiscal_year,
				target_based_unit: frm.doc.target_based_unit,
				name: frm.doc.name

			}
		});
	
		if (is_valid.message) {
			frappe.throw(__('Validation failed: Fiscal year validation error.'));
			frappe.validated = false; // Prevent saving the document
		}
	},
	before_save: async function(frm) {
        if (!frm.is_new()) {
            return;  // If it's an existing document, skip the validation
        }
        let is_valid = await frappe.call({
            method: "teampro.teampro.doctype.target_manager.target_manager.validate_fiscal_year",
            args: {
                employee: frm.doc.employee,
                year: frm.doc.custom_fiscal_year,
				target_based_unit: frm.doc.target_based_unit,
				name: frm.doc.name
            }
        });

        if (is_valid.message) {
            frappe.throw(__('Validation failed: Fiscal year validation error.'));
            frappe.validated = false;  // Prevent the save action
        }
    },
	validate: async function(frm) {
       
        let is_valid = await frappe.call({
            method: "teampro.teampro.doctype.target_manager.target_manager.validate_fiscal_year",
            args: {
                employee: frm.doc.employee,
                year: frm.doc.custom_fiscal_year,
				target_based_unit: frm.doc.target_based_unit,
				name: frm.doc.name
            }
        });

        if (is_valid.message) {
            frappe.throw(__('Validation failed: Fiscal year validation error.'));
            frappe.validated = false;  // Prevent the save action
        }
    },
	based_on_service(frm){
		frm.set_value("based_on_account_manager",0)
	},
	custom_year_start_date(frm){
		frm.clear_table('target_child')
	let start = frm.doc.custom_year_start_date;
	let end = frm.doc.custom_year_end_date;

	if (!start || !end) return;

	// Convert to Date objects
	start = new Date(start);
	end = new Date(end);

	// Clear existing children
	frm.doc.target_child = [];
	frm.doc.monthly_ft_allocation = [];

	const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	const month_no = {
		'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7',
		'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'
	};

	// Loop through each month between start and end
	while (start <= end) {
		let month_index = start.getMonth(); // 0-11
		let month_name = month_names[month_index];

		if (month_no[month_name]) {
			frm.add_child("target_child", {
				month: month_name,
				month_nos: month_no[month_name]
			});
			frm.add_child("monthly_ft_allocation", {
				month: month_name,
				month_nos: month_no[month_name]
			});
		}

		// Move to next month
		start.setMonth(start.getMonth() + 1);
	}

	frm.refresh_field('target_child');
	frm.refresh_field('monthly_ft_allocation');
	},
	custom_year_end_date(frm){
		frm.clear_table('target_child')
	let start = frm.doc.custom_year_start_date;
	let end = frm.doc.custom_year_end_date;

	if (!start || !end) return;

	// Convert to Date objects
	start = new Date(start);
	end = new Date(end);

	// Clear existing children
	frm.doc.target_child = [];
	frm.doc.monthly_ft_allocation = [];

	const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	const month_no = {
		'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7',
		'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'
	};

	// Loop through each month between start and end
	while (start <= end) {
		let month_index = start.getMonth(); // 0-11
		let month_name = month_names[month_index];

		if (month_no[month_name]) {
			frm.add_child("target_child", {
				month: month_name,
				month_nos: month_no[month_name]
			});
			frm.add_child("monthly_ft_allocation", {
				month: month_name,
				month_nos: month_no[month_name]
			});
		}

		// Move to next month
		start.setMonth(start.getMonth() + 1);
	}

	frm.refresh_field('target_child');
	frm.refresh_field('monthly_ft_allocation');
	},
	refresh: function (frm) {
		if(!frm.doc.__islocal){
			frm.add_custom_button(__("Refresh"),function(){
				frappe.call({
					// method: "teampro.teampro.doctype.target_manager.target_manager.calculate_target_for_manager",
					method: "teampro.teampro.doctype.target_manager.updated_target_manager.calculate_target_for_manager_test",
					args:{
						"name":frm.doc.name,
						"emp":frm.doc.employee,
						"year":frm.doc.custom_fiscal_year
					},
					callback(r) {
						if (r.message) {
							frm.reload_doc();
							console.log("Response:", r.message);
						} else {
							console.log("No response message.");
						}
					},
					error: function(err) {
						console.error("Error in frappe.call:", err);
					}
				});
				},("Action"))
		}
		frappe.breadcrumbs.add("HR", "Target Manager");
		if (frm.doc.__islocal) {
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
			if (frm.doc.monthly_ft_allocation.length == 0) {
				$.each(months, function (i, v) {
					frm.add_child("monthly_ft_allocation", {
						'month': v,
						'month_nos': month_no[v]  
					})
					frm.refresh_field('monthly_ft_allocation')
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
		if(!frm.doc.__islocal){
			frm.add_custom_button(("Submit"), function () {
			$.each(frm.fields_dict, function(fieldname, field) {
				frm.set_df_property(fieldname, 'read_only', 1);
				});
			},("Action"));
		}
		$.each(months, function(i, d) {
			frm.doc.annual_ct+=d.ct	
		});
	},

	annual_ct(frm){
		
		frm.clear_table('target_child')
	let start = frm.doc.custom_year_start_date;
	let end = frm.doc.custom_year_end_date;

	if (!start || !end) return;

	// Convert to Date objects
	start = new Date(start);
	end = new Date(end);

	// Clear existing children
	frm.doc.target_child = [];

	const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	const month_no = {
		'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7',
		'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'
	};
	let temp_start = new Date(start);
    let total_months = 0;
    while (temp_start <= end) {
        total_months++;
        temp_start.setMonth(temp_start.getMonth() + 1);
    }
	let per_month_ct = (frm.doc.annual_ct || 0) / total_months;

	// Loop through each month between start and end
	while (start <= end) {
		let month_index = start.getMonth(); // 0-11
		let month_name = month_names[month_index];

		if (month_no[month_name]) {
			frm.add_child("target_child", {
				month: month_name,
				month_nos: month_no[month_name],
				ct: per_month_ct
			});
			
		}

		// Move to next month
		start.setMonth(start.getMonth() + 1);
	}

	frm.refresh_field('target_child');
		// var months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'];
		// var month_no = {'Apr':'12','May':'11','Jun':'10','Jul':'9','Aug':'8','Sep':'7','Oct':'6','Nov':'5','Dec':'4','Jan':'3','Feb':'2','Mar':'1'}
		// var value = frm.doc.annual_ct / 12;
		// frm.clear_table('target_child');  
		// $.each(months, function(i, month) {
		// 	frm.add_child("target_child", {
		// 		'month': month, 
		// 		'month_nos': month_no[month], 
		// 		'ct': value
		// 	});
		// });

		// frm.refresh_field('target_child');
	},
	
	annual_ft(frm){
		frm.clear_table('monthly_ft_allocation')
	let start = frm.doc.custom_year_start_date;
	let end = frm.doc.custom_year_end_date;

	if (!start || !end) return;

	// Convert to Date objects
	start = new Date(start);
	end = new Date(end);

	// Clear existing children
	frm.doc.monthly_ft_allocation = [];

	const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	const month_no = {
		'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7',
		'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'
	};
	 let temp_start = new Date(start);
    let total_months = 0;
    while (temp_start <= end) {
        total_months++;
        temp_start.setMonth(temp_start.getMonth() + 1);
    }
	let per_month_ft = (frm.doc.annual_ft || 0) / total_months;


	// Loop through each month between start and end
	while (start <= end) {
		let month_index = start.getMonth(); // 0-11
		let month_name = month_names[month_index];

		if (month_no[month_name]) {
		
			frm.add_child("monthly_ft_allocation", {
				month: month_name,
				month_nos: month_no[month_name],
				ft: per_month_ft
			});
		}

		// Move to next month
		start.setMonth(start.getMonth() + 1);
	}

	frm.refresh_field('monthly_ft_allocation');
		// var months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'];
		// var month_no = {'Apr':'12','May':'11','Jun':'10','Jul':'9','Aug':'8','Sep':'7','Oct':'6','Nov':'5','Dec':'4','Jan':'3','Feb':'2','Mar':'1'}
		// var value = frm.doc.annual_ft / 12;
		// frm.clear_table('monthly_ft_allocation');  
		// $.each(months, function(i, month) {
		// 	frm.add_child("monthly_ft_allocation", {
		// 		'month': month, 
		// 		'month_nos': month_no[month], 
		// 		'ft': value
		// 	});
		// });

		// frm.refresh_field('monthly_ft_allocation');
	},
	
	// onload(frm){
	// 	frappe.call({
	// 		method: "teampro.teampro.doctype.target_manager.target_manager.calculate_target_for_manager",
	// 		callback(r) {
	// 			if (r.message == 'OK') {
	// 				// frappe.msgprint("Target Updated Successfully")
	// 				// frm.reload_doc();
	// 			}
	// 		}
	// 	})
	// },
	update_target(frm) {
    frappe.call({
        method: "teampro.teampro.doctype.target_manager.target_manager.calculate_target_for_manager",
        callback(r) {
            if (r.message) {
                console.log("Response:", r.message);
            } else {
                console.log("No response message.");
            }
        },
        error: function(err) {
            console.error("Error in frappe.call:", err);
        }
    });
	},
});
