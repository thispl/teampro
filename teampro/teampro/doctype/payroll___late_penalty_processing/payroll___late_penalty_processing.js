// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payroll - Late Penalty Processing', {
	process_late(frm){
		frappe.call({
			"method": "teampro.utility.attendance_calc",
			"args":{
				"from_date" : frm.doc.start_date,
				"to_date" : frm.doc.end_date,
			},
			freeze: true,
			freeze_message: 'Processing late....',
			callback(r){
				console.log(r.message)
				if(r.message == "ok"){
					frappe.msgprint("Late Penalty Created Successfully")
				}
			}
		})
	},
	create_late_penalty(frm){
		frappe.call({
			"method": "teampro.utility.additional_salary",
			"args":{
				"from_date" : frm.doc.start_date,
				"to_date" : frm.doc.end_date,
			},
			freeze: true,
			freeze_message: 'Processing additional salary....',
			callback(r){
				console.log(r.message)
				if(r.message == "ok"){
					frappe.msgprint("Late Penalty - Additional Created Successfully")
				}
			}
		})
	}
});
