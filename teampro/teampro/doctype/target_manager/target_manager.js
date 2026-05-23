// Copyright (c) 2022, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Target Manager', {

	



	custom_fiscal_year: async function (frm) {
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
	before_save: async function (frm) {
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
	validate: async function (frm) {

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
	based_on_service(frm) {
		frm.set_value("based_on_account_manager", 0)
		frm.set_value("based_on_candidate_owner", 0)
	},
	based_on_account_manager(frm) {
		frm.set_value("based_on_service", 0)
		frm.set_value("based_on_candidate_owner", 0)
	},
	based_on_candidate_owner(frm) {
		frm.set_value("based_on_account_manager", 0)
		frm.set_value("based_on_service", 0)
	},
	employee: function (frm) {
		if (frm.doc.employee) {
			set_incentive(frm);
		}


		// if (!frm.doc.employee) return;

		// frappe.db.get_value('Employee', frm.doc.employee,
		// 	'custom__invective_eligibility_group'
		// ).then(r => {

		// 	if (!r.message) return;

		// 	let group = r.message.custom__invective_eligibility_group?.trim();

		// 	console.log("Group:", group);

		// 	// Reset first
		// 	frm.set_value({
		// 		based_on_service: 0,
		// 		based_on_account_manager: 0,
		// 		based_on_candidate_owner: 0
		// 	});

		// 	if (group === "Service") {
		// 		frm.set_value('based_on_service', 1);
		// 	}
		// 	else if (group === "Account Manager") {
		// 		frm.set_value('based_on_account_manager', 1);
		// 	}
		// 	else if (group === "Candidate Owner") {
		// 		frm.set_value('based_on_candidate_owner', 1);
		// 	}

		// 	frm.refresh_fields();
		// });
	},
	custom_year_start_date(frm) {
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
	custom_year_end_date(frm) {
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
	custom_annual_ct_point: function (frm) {
		calculate_annual_ct(frm);
	},
	custom_annual_ft_point(frm) {
		calculate_annual_ft(frm);
	},
	refresh: function (frm) {
		console.log(frm.doc.custom_sr);
		if (frm.doc.employee) {
			set_incentive(frm);
		}
		if (!frm.doc.__islocal) {
			// frm.add_custom_button(__("Refresh"), function () {
			// 	frappe.call({
			// 		method: "teampro.teampro.doctype.target_manager.updated_target_manager.calculate_target_for_manager_point",
			// 		args: {
			// 			"name": frm.doc.name,
			// 			"emp": frm.doc.employee,
			// 			"year": frm.doc.custom_fiscal_year
			// 		},
			// 		callback(r) {
			// 			if (r.message) {
			// 				frm.reload_doc();
			// 				console.log("Response:", r.message);
			// 			} else {
			// 				console.log("No response message.");
			// 			}
			// 		},
			// 		error: function (err) {
			// 			console.error("Error in frappe.call:", err);
			// 		}
			// 	});
			// }, ("Action"))
			frm.add_custom_button(__("Refresh"), function () {
				frappe.call({
					method: "teampro.teampro.doctype.target_manager.updated_target_manager.calculate_target_for_manager_point",
					args: {
						"name": frm.doc.name,
						"emp": frm.doc.employee,
						"year": frm.doc.custom_fiscal_year
					},
					callback(r) {
						if (r.message) {
							frm.reload_doc();
							console.log("Response:", r.message);
						} else {
							console.log("No response message.");
						}
					},
					error: function (err) {
						console.error("Error in frappe.call:", err);
					}
				});
			}, ("Action"))
		}
		frappe.breadcrumbs.add("HR", "Target Manager");
		if (frm.doc.__islocal) {
			var months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
			var month_no = { 'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1' }
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
		if (!frm.doc.__islocal) {
			frm.add_custom_button(("Submit"), function () {
				$.each(frm.fields_dict, function (fieldname, field) {
					frm.set_df_property(fieldname, 'read_only', 1);
				});
			}, ("Action"));
		}
		$.each(months, function (i, d) {
			frm.doc.annual_ct += d.ct
		});
	},

	// annual_ct(frm){
	// 	calculate_ct_point(frm);
	// 	frm.clear_table('target_child')
	// let start = frm.doc.custom_year_start_date;
	// let end = frm.doc.custom_year_end_date;

	// if (!start || !end) return;

	// // Convert to Date objects
	// start = new Date(start);
	// end = new Date(end);

	// // Clear existing children
	// frm.doc.target_child = [];

	// const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	// const month_no = {
	// 	'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7',
	// 	'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'
	// };
	// let temp_start = new Date(start);
	// let total_months = 0;
	// while (temp_start <= end) {
	//     total_months++;
	//     temp_start.setMonth(temp_start.getMonth() + 1);
	// }
	// let per_month_ct = (frm.doc.annual_ct || 0) / total_months;

	// // Loop through each month between start and end
	// while (start <= end) {
	// 	let month_index = start.getMonth(); // 0-11
	// 	let month_name = month_names[month_index];

	// 	if (month_no[month_name]) {
	// 		frm.add_child("target_child", {
	// 			month: month_name,
	// 			month_nos: month_no[month_name],
	// 			ct: per_month_ct
	// 		});

	// 	}

	// 	// Move to next month
	// 	start.setMonth(start.getMonth() + 1);
	// }

	// frm.refresh_field('target_child');

	// },
	annual_ct: function (frm) {
		calculate_ct_point(frm);
		if (!frm.doc.custom_fiscal_year || !frm.doc.custom_company || !frm.doc.annual_ct)
			return;

		frappe.call({
			method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
			args: {
				company: frm.doc.custom_company,
				fiscal_year: frm.doc.custom_fiscal_year
			},
			callback: function (r) {

				if (!r.message) {
					frappe.msgprint("No Point Value defined in Company");
					return;
				}

				let point_value = r.message;
				let ct_point = frm.doc.annual_ct / point_value;
				frm.clear_table('target_child');
				let start = frm.doc.custom_year_start_date;
				let end = frm.doc.custom_year_end_date;

				if (!start || !end) return;

				start = new Date(start);
				end = new Date(end);

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
				let per_month_ct_point = ct_point / total_months;
				while (start <= end) {
					let month_index = start.getMonth(); // 0-11
					let month_name = month_names[month_index];
					if (month_no[month_name]) {
						frm.add_child("target_child", {
							month: month_name,
							month_nos: month_no[month_name],
							ct: per_month_ct,
							ct_point: per_month_ct_point
						});

					}
					start.setMonth(start.getMonth() + 1);
				}

				frm.refresh_field('target_child');
			}
		});
	},
	// annual_ft(frm){
	// 	calculate_ft_point(frm);
	// 	frm.clear_table('monthly_ft_allocation')
	// 	if (!frm.doc.custom_fiscal_year || !frm.doc.custom_company || !frm.doc.annual_ct)
	//     return;


	// let start = frm.doc.custom_year_start_date;
	// let end = frm.doc.custom_year_end_date;

	// if (!start || !end) return;

	// // Convert to Date objects
	// start = new Date(start);
	// end = new Date(end);

	// // Clear existing children
	// frm.doc.monthly_ft_allocation = [];

	// const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	// const month_no = {
	// 	'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7',
	// 	'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'
	// };
	//  let temp_start = new Date(start);
	// let total_months = 0;
	// while (temp_start <= end) {
	//     total_months++;
	//     temp_start.setMonth(temp_start.getMonth() + 1);
	// }
	// let per_month_ft = (frm.doc.annual_ft || 0) / total_months;


	// // Loop through each month between start and end
	// while (start <= end) {
	// 	let month_index = start.getMonth(); // 0-11
	// 	let month_name = month_names[month_index];

	// 	if (month_no[month_name]) {

	// 		frm.add_child("monthly_ft_allocation", {
	// 			month: month_name,
	// 			month_nos: month_no[month_name],
	// 			ft: per_month_ft
	// 		});
	// 	}

	// 	// Move to next month
	// 	start.setMonth(start.getMonth() + 1);
	// }

	// frm.refresh_field('monthly_ft_allocation');

	// },
	annual_ft: function (frm) {
		calculate_ft_point(frm);
		if (!frm.doc.custom_fiscal_year || !frm.doc.custom_company || !frm.doc.annual_ft)
			return;

		frappe.call({
			method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
			args: {
				company: frm.doc.custom_company,
				fiscal_year: frm.doc.custom_fiscal_year
			},
			callback: function (r) {

				if (!r.message) {
					frappe.msgprint("No Point Value defined in Company");
					return;
				}

				let point_value = r.message;
				let ft_point = frm.doc.annual_ft / point_value;
				frm.clear_table('monthly_ft_allocation');
				let start = frm.doc.custom_year_start_date;
				let end = frm.doc.custom_year_end_date;

				if (!start || !end) return;

				start = new Date(start);
				end = new Date(end);

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
				let per_month_ft_point = ft_point / total_months;
				while (start <= end) {
					let month_index = start.getMonth(); // 0-11
					let month_name = month_names[month_index];
					if (month_no[month_name]) {
						frm.add_child("monthly_ft_allocation", {
							month: month_name,
							month_nos: month_no[month_name],
							ft: per_month_ft,
							ft_point: per_month_ft_point
						});

					}
					start.setMonth(start.getMonth() + 1);
				}

				frm.refresh_field('monthly_ft_allocation');
			}
		});
	},
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
			error: function (err) {
				console.error("Error in frappe.call:", err);
			}
		});
	},
});
function calculate_annual_ct(frm) {
	if (frm.doc.custom_annual_ct_point == 0) {
		frm.set_value(
			"annual_ct",
			"0.00"
		);
	}

	if (!frm.doc.custom_fiscal_year || !frm.doc.custom_annual_ct_point || !frm.doc.custom_company)
		return;

	frappe.call({
		method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
		args: {
			company: frm.doc.custom_company,
			fiscal_year: frm.doc.custom_fiscal_year
		},
		callback: function (r) {

			if (r.message) {

				frm.set_value(
					"annual_ct",
					frm.doc.custom_annual_ct_point * r.message
				);

			} else {
				frappe.msgprint("No Point Value defined in Company for this Fiscal Year");
			}
		}
	});
}
function calculate_annual_ft(frm) {
	if (frm.doc.custom_annual_ft_point == 0) {
		frm.set_value(
			"annual_ft",
			"0.00"
		);
	}
	if (!frm.doc.custom_fiscal_year || !frm.doc.custom_annual_ft_point || !frm.doc.custom_company)
		return;

	frappe.call({
		method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
		args: {
			company: frm.doc.custom_company,
			fiscal_year: frm.doc.custom_fiscal_year
		},
		callback: function (r) {

			if (r.message) {

				frm.set_value(
					"annual_ft",
					frm.doc.custom_annual_ft_point * r.message
				);

			} else {
				frappe.msgprint("No Point Value defined in Company for this Fiscal Year");
			}
		}
	});
}
function calculate_ct_point(frm) {
	if (frm.doc.annual_ct == 0) {
		frm.set_value(
			"custom_annual_ct_point",
			"0.00"
		);
	}
	if (!frm.doc.custom_fiscal_year || !frm.doc.annual_ct || !frm.doc.custom_company)
		return;

	frappe.call({
		method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
		args: {
			company: frm.doc.custom_company,
			fiscal_year: frm.doc.custom_fiscal_year
		},
		callback: function (r) {

			if (r.message) {

				frm.set_value(
					"custom_annual_ct_point",
					frm.doc.annual_ct / r.message
				);

			} else {
				frappe.msgprint("No Point Value defined in Company for this Fiscal Year");
			}
		}
	});
}
function calculate_ft_point(frm) {
	if (frm.doc.annual_ft == 0) {
		frm.set_value(
			"custom_annual_ft_point",
			"0.00"
		);
	}
	if (!frm.doc.custom_fiscal_year || !frm.doc.annual_ft || !frm.doc.custom_company)
		return;

	frappe.call({
		method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
		args: {
			company: frm.doc.custom_company,
			fiscal_year: frm.doc.custom_fiscal_year
		},
		callback: function (r) {

			if (r.message) {

				frm.set_value(
					"custom_annual_ft_point",
					frm.doc.annual_ft / r.message
				);

			} else {
				frappe.msgprint("No Point Value defined in Company for this Fiscal Year");
			}
		}
	});
}
frappe.ui.form.on('DM Services', {

	ct_point: function (frm, cdt, cdn) {
		calculate_row_values(frm, cdt, cdn);
	},

	ft_point: function (frm, cdt, cdn) {
		calculate_row_values(frm, cdt, cdn);
	},
	ct: function (frm, cdt, cdn) {
		calculate_row_point(frm, cdt, cdn);
	},
	ft: function (frm, cdt, cdn) {
		calculate_row_point(frm, cdt, cdn);
	},

});
function calculate_row_values(frm, cdt, cdn) {

	let row = locals[cdt][cdn];

	if (!frm.doc.custom_company || !frm.doc.custom_fiscal_year)
		return;

	frappe.call({
		method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
		args: {
			company: frm.doc.custom_company,
			fiscal_year: frm.doc.custom_fiscal_year
		},
		callback: function (r) {

			if (!r.message) {
				frappe.msgprint("Point value not defined for this Fiscal Year");
				return;
			}

			let point_value = r.message;
			if (row.ct_point == 0) {
				row.ct = "0.00"
			}
			if (row.ft_point == 0) {
				row.ft = "0.00"
			}
			if (row.ct_point) {
				row.ct = row.ct_point * point_value;
			}

			if (row.ft_point) {
				row.ft = row.ft_point * point_value;
			}

			frm.refresh_field("service_list");
		}
	});
}
function calculate_row_point(frm, cdt, cdn) {

	let row = locals[cdt][cdn];

	if (!frm.doc.custom_company || !frm.doc.custom_fiscal_year)
		return;

	frappe.call({
		method: "teampro.teampro.doctype.target_manager.updated_target_manager.get_point_value",
		args: {
			company: frm.doc.custom_company,
			fiscal_year: frm.doc.custom_fiscal_year
		},
		callback: function (r) {

			if (!r.message) {
				frappe.msgprint("Point value not defined for this Fiscal Year");
				return;
			}

			let point_value = r.message;
			if (row.ct == 0) {
				row.ct_point = "0.00"
			}
			if (row.ft == 0) {
				row.ft_point = "0.00"
			}
			if (row.ct) {
				row.ct_point = row.ct / point_value;
			}

			if (row.ft) {
				row.ft_point = row.ft / point_value;
			}

			frm.refresh_field("service_list");
		}
	});
}

function set_incentive(frm) {

	frappe.db.get_value('Employee', frm.doc.employee,
		'custom__invective_eligibility_group'
	).then(r => {

		if (!r.message) return;

		let group = r.message.custom__invective_eligibility_group?.trim();


		frm.doc.based_on_service = 0;
		frm.doc.based_on_account_manager = 0;
		frm.doc.based_on_candidate_owner = 0;

		if (group === "Service") {
			frm.doc.based_on_service = 1;
		}
		else if (group === "Account Manager") {
			frm.doc.based_on_account_manager = 1;
		}
		else if (group === "Candidate Owner") {
			frm.doc.based_on_candidate_owner = 1;
		}

		frm.refresh_field('based_on_service');
		frm.refresh_field('based_on_account_manager');
		frm.refresh_field('based_on_candidate_owner');
	});
}