// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Follow Up', {
	refresh: function(frm) {
	},
	lead(frm){
		frm.set_value("follow_up_to","Lead")
		frappe.call({
				method: "teampro.teampro.doctype.sales_follow_up.sales_follow_up.lead_contacts",
				args: {
					lead: frm.doc.lead
				},
				
				callback: function (r) {
					console.log(r.message);
					frm.clear_table('contacts')
					$.each(r.message, function (i, d) {
						frm.add_child('contacts', {
							'person_name': d.person_name,
							'mobile': d.mobile,
							'is_primary': d.is_primary,
							'has_whatsapp': d.has_whatsapp,
							'email_id': d.email_id,
							'is_primaryemail': d.is_primaryemail,
							'service':d.service
						});
					});
					frm.refresh_field('contacts');
				}
			});
		},
		customer(frm){
			frm.set_value("follow_up_to","Customer")
			frappe.call({
					method: "teampro.teampro.doctype.sales_follow_up.sales_follow_up.customer_contacts",
					args: {
						customer: frm.doc.customer
					},
					
					callback: function (r) {
						console.log(r.message);
						frm.clear_table('customer_contacts')
						$.each(r.message, function (i, d) {
							frm.add_child('customer_contacts', {
								'person_name': d.person_name,
								'mobile': d.mobile,
								'is_primary': d.is_primary,
								'has_whatsapp': d.has_whatsapp,
								'email_id': d.email_id,
								'is_primaryemail': d.is_primaryemail,
								'service':d.service
							});
						});
						frm.refresh_field('customer_contacts');
					}
				});
			},
		// customer(frm){
		// 	frappe.call({
		// 			method: "teampro.teampro.doctype.sales_follow_up.sales_follow_up.address",
		// 			args: {
		// 				customer: frm.doc.customer
		// 			},
					
		// 			callback: function (r) {
		// 				console.log(r.message);
		// 				frm.set_value("adress_html",r.message['adress_html'])
		// 				frm.set_value("contact",r.message['contact'])
		// 			}
		// 		});
		// 	}
})
