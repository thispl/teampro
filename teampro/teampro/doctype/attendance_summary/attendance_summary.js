// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Attendance Summary", {
	refresh(frm) {
		if(frappe.session.user != 'Administrator') {
			frm.set_df_property('from_date','hidden',0)
			frm.set_df_property('to_date','hidden',0)
        }
		var currentDate = new Date();
		var currentYear = currentDate.getFullYear();
		var currentMonth = currentDate.getMonth() + 1; 
		var months = [
			"January", "February", "March", "April", "May", "June",
			"July", "August", "September", "October", "November", "December"
		];
		var monthName = months[currentMonth - 1]; 
		frm.set_value('month', monthName);
		frm.set_value('year', currentYear);
		frm.disable_save();
		if (!frappe.user.has_role('System Manager') && !frappe.user.has_role('HOD') && !frappe.user.has_role('HR Manager') && !frappe.user.has_role('HR User')) {
			frappe.db.get_value("Employee", {'user_id': frappe.session.user}, ['employee', 'employee_name'], (r) => {
				if (r){
					frm.set_value('employee_id', r.employee);
					frm.set_value('employee_name', r.employee_name);
				}
			});
			frm.set_df_property('employee_id','read_only',1)
		}
		frm.trigger('get_from_to_dates')
		frappe.call({
			method:"teampro.custom.update_last_execution",
			callback(r){
				if (r.message) {
					console.log(r.message)
					// frm.set_value(' ', r.message);
				}
			}
		})
    },
    onload(frm){
		if(frappe.session.user != 'Administrator') {
			frappe.db.get_value("Employee", {'user_id': frappe.session.user}, ['employee','employee_name'], (r) => {
				if (r){
					frm.set_value('employee_id', r.employee);
					frm.set_value('employee_name', r.employee_name);
				}
			});
			frm.set_df_property('from_date','hidden',0)
			frm.set_df_property('to_date','hidden',0)
        }
		var currentDate = new Date();
		var currentYear = currentDate.getFullYear();
		var currentMonth = currentDate.getMonth() + 1; 
		var months = [
			"January", "February", "March", "April", "May", "June",
			"July", "August", "September", "October", "November", "December"
		];
		var monthName = months[currentMonth - 1]; 
		frm.set_value('month', monthName);
		frm.set_value('year', currentYear);
		frm.disable_save();
		if (!frappe.user.has_role('System Manager') && !frappe.user.has_role('HOD') && !frappe.user.has_role('HR Manager') && !frappe.user.has_role('HR User')) {
			frappe.db.get_value("Employee", {'user_id': frappe.session.user}, ['employee', 'employee_name'], (r) => {
				if (r){
					frm.set_value('employee_id', r.employee);
					frm.set_value('employee_name', r.employee_name);
				}
			});
			frm.set_df_property('employee_id','read_only',1)
		}
		frm.trigger('get_from_to_dates')
	},
    employee_id(frm){
		frm.trigger('get_from_to_dates')
		frm.trigger('get_data')
	},
	year(frm){
		frm.trigger('get_from_to_dates')
	},
	month(frm){
		frm.trigger('get_from_to_dates')
	},
	from_date(frm){
		frm.trigger('get_data')
	},
	to_date(frm){
		frm.trigger('get_data')
	},
	get_from_to_dates(frm){
		frappe.call({
			"method": "teampro.teampro.doctype.attendance_summary.attendance_summary.get_from_to_dates",
			"args":{
				"month" : frm.doc.month,
				"year" : frm.doc.year
			},
			callback(r){
				// console.log(r.message)
				if(r.message){
					// console.log(r.message)
					frm.set_value('from_date', r.message[0]);
					frm.set_value('to_date', r.message[1]);
				}
			}
		})

	},
    get_data: function (frm) {
		if (frm.doc.from_date && frm.doc.to_date && frm.doc.employee_id) {
			if (!frappe.is_mobile()) {
				frm.trigger('get_data_system')
				frm.trigger('get_data_summary')
			}
			else {
				frm.trigger('get_data_mobile')
			}
		}
	},
    get_data_system(frm) {
		if (frm.doc.employee_id) {
			frappe.call({
				method: "teampro.teampro.doctype.attendance_summary.attendance_summary.get_data_system",
				args: {
					emp: frm.doc.employee_id,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date
				},
				callback: function (r) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			})
		}
		else {
			frm.fields_dict.html.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
		}
	},
	get_data_summary(frm) {
		if (frm.doc.employee_id) {
			frappe.call({
				method: "teampro.teampro.doctype.attendance_summary.attendance_summary.get_data_summary",
				args: {
					emp: frm.doc.employee_id,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date
				},
				callback: function (r) {
					frm.fields_dict.html1.$wrapper.empty().append(r.message)
				}
			})
		}
		else {
			frm.fields_dict.html1.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
		}
	},
    get_data_mobile(frm) {
		if (frm.doc.employee_id) {
			frappe.call({
				method: "teampro.teampro.doctype.attendance_summary.attendance_summary.get_data_system",
				args: {
					emp: frm.doc.employee_id,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date
				},
				callback: function (r) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			})
		}
		else {
			frm.fields_dict.html.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
		}
	},
});
