// Copyright (c) 2022, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Miss Punch Application', {
	date:function(frm) {
		if (frm.doc.__islocal){
			frappe.call({
				'method':'frappe.client.get_value',
				'args':{
					'doctype':'Attendance',
					'filters':{
						'employee':frm.doc.employee,
						'attendance_date':frm.doc.date
					},
					'fieldname':['in_time','out_time','shift']
				},
				callback(r){
					if(r.message){
						// console.log(r.message)
						frm.set_value('in_time',r.message.in_time)
						frm.set_value('out_time',r.message.out_time)
						frm.set_value('shift',r.message.shift)
					
						
					}
				}
			})
		}
	},
});
