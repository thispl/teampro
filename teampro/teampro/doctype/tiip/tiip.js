// Copyright (c) 2021, Finaxar and contributors
// For license information, please see license.txt

frappe.ui.form.on('TIIP', {
	refresh(frm) {
		frm.set_value("period","Quarterly")
		frm.set_value("quarterly","1")
		frm.set_value("year","2021")
		frm.disable_save()
		var d = new Date();
		var from_date =new Date(d.getFullYear(),d.getMonth(),1)
		// console.log(get_date)
		var end_date=frappe.datetime.nowdate()
		// frm.set_value("from_period",from_date)
		// frm.set_value("to",end_date)
		frm.trigger("get_target")
	},	
	get_target:function(frm){
		frm.call('get_all_employees')
		.then(r => {
			refresh_field("target")
			refresh_field("tiips")
			if (r.message) {
				$.each(frm.doc.target, function (i, d) {
					d.pending = d.goal - r.message
					d.achieved_percentage = (r.message / d.goal) * 100
				})
				refresh_field("target")
				
			}
		})
	},
	quarterly:function(frm){
		frm.trigger("get_target")
	},
	period:function(frm){
		frm.trigger("get_target")
	},
	// period: function (frm) {
	// 	frappe.call({
	// 		"method": "teampro.teampro.doctype.tiip.tiip.get_ft",
	// 		args: {
	// 			'employee_name': frm.doc.employee_name,
	// 			'period': frm.doc.period,
	// 			'name':frm.doc.name
	// 		},
	// 		callback: function (r) {
	// 			// console.log(r.message)
	// 			frm.clear_table("target")
	// 			if (frm.doc.period == "Quarterly") {
	// 				var row = frappe.model.add_child(frm.doc, "Target", "target")
	// 				row.goal = r.message
	// 				refresh_field("target")

	// 			}
	// 			else if (frm.doc.period == "Monthly") {
	// 				var row = frappe.model.add_child(frm.doc, "Target", "target")
	// 				// console.log(typeof(r.message))
	// 				row.goal = (r.message / 3).toFixed(0)
	// 				refresh_field("target")
	// 			}
	// 			else if (frm.doc.period == "Annually") {
	// 				var row = frappe.model.add_child(frm.doc, "Target", "target")
	// 				row.goal = r.message * 4
	// 				refresh_field("target")
	// 			}
	// 		}

	// 	})


	// },

	// to: function (frm) {
	// 	frappe.call({
	// 		"method": "teampro.teampro.doctype.tiip.tiip.get_achieved",
	// 		args: {
	// 			'employee_name': frm.doc.employee_name,
	// 			'employee_mail': frm.doc.employee_mail,
	// 			'period': frm.doc.period,
	// 			'from_period': frm.doc.from_period,
	// 			'to': frm.doc.to,
	// 		},
	// 		callback: function (r) {
	// 			console.log(r.message)

	// 			$.each(frm.doc.target, function (i, d) {
	// 				console.log(d)
	// 				d.achieved = r.message
	// 				d.pending = d.goal - r.message
	// 				d.achieved_percentage = (r.message / d.goal) * 100
	// 			})
	// 			refresh_field("target")


	// 		}
	// 	})

	// },
	employee_id: function (frm) {
		console.log(frm.doc.employee_id)
		if (frm.doc.employee_id) {
			frappe.db.get_doc("Employee", frm.doc.employee_id)
				.then(r => {
					console.log(r)
					$.each(r.tiips, function (i, d) {
						console.log(d)
						var row = frm.add_child("tiips")
						row.quarterly = d.quarterly
						row.year = d.year
						row.bt = d.bt
					})
					frm.refresh_field("tiips")
				})

		}
	}
});

