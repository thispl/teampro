// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Follow Up', {
	refresh: function(frm) {
		if (frm.doc.app_status == 'Yet to Meet') {
			frm.add_custom_button("Fix meeting", function () {
				frappe.confirm(
					'Are you sure you want to fix the meeting?',
					function () {
						let d = new frappe.ui.Dialog({
							title: 'Fix Meeting',
							fields: [
								{
									label: 'Appointment On',
									fieldname: 'appointment_on',
									fieldtype: 'Date',
									// reqd: 1
								},
								{
									label: 'Appointment For',
									fieldname: 'appointment_for',
									fieldtype: 'Link',
									options: 'User',
									// reqd: 1
								}
							],
							primary_action_label: 'Submit',
							primary_action(values) {
								frm.set_value('app_status', 'Fix Meeting');
								frm.set_value('appointment_created_on', frappe.datetime.now_date());
								frm.set_value('custom_appointment_fixed_for', values.appointment_for);
								frm.set_value('appointment_fixed_on', values.appointment_on);
								d.hide();
								frm.save(); 
							}
						});
		
						d.show();
					},
					function () {
						
					}
				);
			});
			
		}
		
		if (frm.doc.app_status=='Fix Meeting'){
			frm.add_custom_button(("Schedule Meeting"), function () {
				frappe.confirm(
					'Are you sure, you want to schedule the meeting?',
					function () {
						frm.set_value('app_status', 'Scheduled');
						frm.save()
						// frm.reload_doc()
					},
					function () {					
					}
				);
			}); 
		}
		if (frm.doc.app_status === "Scheduled") {
            frm.add_custom_button("Visited", function () {

                frappe.confirm(
                    'Are you sure you want to mark as Visited?',
                    function() {
                        // Show dialog after confirmation
                        const d = new frappe.ui.Dialog({
                            title: 'Visit Details',
                            fields: [
                                {
                                    label: 'Appointment Remarks',
                                    fieldname: 'appointment_remarks',
                                    fieldtype: 'Small Text',
                                    reqd: 1
                                },
                                {
                                    label: 'Person Met',
                                    fieldname: 'person_met',
                                    fieldtype: 'Data',
                                    reqd: 0
                                },
                                {
                                    label: 'Email',
                                    fieldname: 'email',
                                    fieldtype: 'Data',
                                    reqd: 0
                                },
								{
                                    label: 'Accompanied by',
                                    fieldname: 'accompanied_by',
                                    fieldtype: 'Table MultiSelect',
                                    reqd: 0,
									options:'DPR Mail Users'
                                }
                            ],
                            primary_action_label: 'Submit',
                            primary_action(values) {
                                d.hide();
								if (frm.doc.party_from=='Lead'){
									frappe.call({
										method:"teampro.custom.update_app_visit_status",
										args:{
											'lead':frm.doc.party_name,
											'visit':'Visited'
											
										},
									})
								}
                                frm.set_value('app_status', 'Visited');
								frm.set_value('visit_status', 'Visited');
                                frm.set_value('appointment_remarks', values.appointment_remarks);
                                frm.set_value('custom_person_met', values.person_met);
                                frm.set_value('custom_contact_email', values.email);
                                frm.set_value('appointment_fixed_on', '');
                                frm.set_value('custom_appointment_fixed_for', '');
                                frm.set_value('visted_by', frappe.session.user);
                                frm.set_value('visted_date', frappe.datetime.now_date());
								if (values.accompanied_by){
									frm.set_value('accompanied_by', values.accompanied_by);
								}
								else{
									frm.set_value('accompanied_by','')
								}
                                if (values.person_met || values.email) {
                                    const child = frm.add_child('contacts', {
                                        person_name: values.person_met,
                                        email_id: values.email
                                    });
                                    frm.refresh_field('contacts');
                                }
								if (values.appointment_remarks) {
                                    const child = frm.add_child('custom_appointment_details', {
                                        visted_date: frappe.datetime.now_date(),
                                        visted_by: frappe.session.user,
										appointment_remarks:values.appointment_remarks
                                    });
                                    frm.refresh_field('custom_appointment_details');
                                }
                                frm.save();
                            }
                        });
                        d.show();
                    }
                );
            });
        }
		if (frm.doc.app_status=='Visited'){
			frm.add_custom_button("Yet to Meet", function () {
				if (frm.doc.party_from=='Lead'){
					frappe.call({
						method:"teampro.custom.update_app_visit_status",
						args:{
							'lead':frm.doc.party_name,
							'visit':''
							
						},
					})
				}
				frm.set_value('app_status', 'Yet to Meet');
				frm.set_value('appointment_remarks', '');
				frm.set_value('visit_status', '');
				frm.set_value('visted_by', '');
				frm.set_value('visted_date', '');
				frm.save()
			});
			
		}
		// if(frm.doc.app_status=="Visited" || frm.doc.app_status=="Yet to visit(YTV)"){
		// 	frm.add_custom_button(("Planned"), function () {
		// 		if(frm.doc.visted_date && frm.doc.visted_by){
		// 			frm.add_child('custom_appointment_details', {
		// 				'visted_date':frm.doc.visted_date,
		// 				'visted_by':frm.doc.visted_by,
		// 				'appointment_remarks':frm.doc.appointment_remarks,
		// 			});
		// 		}
		// 		frm.refresh_field('custom_appointment_details');  // Corrected field name
		// 		frm.set_value("appointment_created_on",frappe.datetime.now_date())
		// 		frm.set_value('app_status', 'Planned');
		// 		if(frm.doc.party_from=="Lead" && frm.doc.visted_date && frm.doc.visted_by && frm.doc.appointment_remarks){
		// 			frappe.call({
		// 				method:"teampro.custom.add_custom_appointment_details_in_lead",
		// 				args:{
		// 					'lead':frm.doc.party_name,
		// 					'visted_date':frm.doc.visted_date,
		// 					'visted_by':frm.doc.visted_by,
		// 					'appointment_remarks':frm.doc.appointment_remarks,
		// 					'name':frm.doc.name
		// 				},
		// 				callback(){

		// 				}
		// 			})
		// 		}
		// 		frm.set_value('appointment_remarks', '');
		// 		frm.set_df_property("appointment_remarks","reqd",0)
		// 		frm.set_value('visted_by', '');
		// 		frm.set_value('visted_date', '');
		// 	}); 
		// }
		// if(frm.doc.app_status=="Scheduled"){
		// 	frm.add_custom_button(("Visited"), function () {
		// 		frm.set_value('app_status','Visited')
		// 		frm.set_df_property('appointment_remarks','reqd',1)
		// 		// frm.set_df_property('accompanied_by','reqd',1)
		// 		frm.set_value('appointment_fixed_on', '');
		// 		frm.set_value('custom_appointment_fixed_for', '');
		// 		frm.set_value("visted_by",frappe.session.user)
		// 		frm.set_value("visted_date",frappe.datetime.now_date())
		// 	});
			// frm.add_custom_button(("Cancel"), function () {
			// 	frm.set_value('app_status','Yet to Meet')
			// 	frm.set_value('appointment_fixed_on', '');
			// 	frm.set_value('appointment_created_on','')
			// 	frm.set_value('custom_appointment_fixed_for', '');
			// });
		// }
		$(frm.fields_dict.custom_html_2.wrapper).html(`
			<p>If you want to add a new contact person, add it in Lead Contacts. If you want to remove a contact person, select and remove the row.</p>`);
	
		frm.trigger("set_dynamic_field_label");
		// render_status_button(frm);
		if (frm.doc.active==1) {
			frm.set_intro(__("<h5 style ='color:blue'><b>Alert:</b>Next Action and Remarks are freezed.Please update in respective <b>Project</b></h5>"))
			frm.add_custom_button(__('Active'), function() {
			})
			.css({
				'background-color': 'green',
				'color': 'white',
				'font-weight': 'bold'
			});
		}
		if (!frm.doc.__islocal){
		if(frm.doc.status == "Lead"){
			frm.add_custom_button(("Open"), function () {
				frm.set_value("status","Open")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("DNC"), function () {
				frm.set_value("status","Do Not Contact")
				frm.save()
			},("Action")); 
		}
		if(frm.doc.status == "Open"){
			frm.add_custom_button(("Replied"), function () {
				frm.set_value("status","Replied")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("DNC"), function () {
				frm.set_value("status","Do Not Contact")
				frm.save()
			},("Action")); 
		}
		
		// Extra
		if(frm.doc.status=="Interested"){
			frm.add_custom_button(("Opportunity"), function () {
				frappe.msgprint({
					title: __('Please Wait'),
					message: __('Creating Opportunity...'),
					indicator: 'blue',
					freeze: true
				});
				var bg = frappe.model.make_new_doc_and_get_name('Opportunity');
				bg = locals['Opportunity'][bg];
				bg.opportunity_from=frm.doc.party_from
				bg.party_name=frm.doc.party_name
				bg.organization_name=frm.doc.organization_name
				bg.custom_sales_follow_up=frm.doc.name
				frappe.set_route("Form", "Opportunity",bg.name)
				frm.set_value("status","Opportunity")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("DNC"), function () {
				frm.set_value("status","Do Not Contact")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("Replied"), function () {
				frm.set_value("status","Replied")
				frm.save()
			},("Action")); 
		}
		if(frm.doc.status == "Replied"){
			frm.add_custom_button(("Interested"), function () {
				frm.set_value("status","Interested")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("DNC"), function () {
				frm.set_value("status","Do Not Contact")
				frm.save()
			},("Action")); 
		}
		if(frm.doc.status == "Opportunity"){
			frm.add_custom_button(("Interested"), function () {
				frm.set_value("status","Interested")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("Replied"), function () {
				frm.set_value("status","Replied")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("DNC"), function () {
				frm.set_value("status","Do Not Contact")
				frm.save()
			},("Action")); 
		}
		if(frm.doc.status == "Converted"){
			frm.add_custom_button(("Opportunity"), function () {
				frappe.msgprint({
					title: __('Please Wait'),
					message: __('Creating Opportunity...'),
					indicator: 'blue',
					freeze: true
				});
				var bg = frappe.model.make_new_doc_and_get_name('Opportunity');
				bg = locals['Opportunity'][bg];
				bg.opportunity_from=frm.doc.party_from
				bg.party_name=frm.doc.party_name
				bg.custom_sales_follow_up=frm.doc.name
				bg.organization_name=frm.doc.organization_name
				frappe.set_route("Form", "Opportunity",bg.name)
				frm.set_value("status","Opportunity")
				frm.save()
			},("Action")); 
			frm.add_custom_button(("DNC"), function () {
				frm.set_value("status","Do Not Contact")
				frm.save()
			},("Action")); 
		}
		if(frm.doc.status == "Do Not Contact"){
			frm.add_custom_button(("Reopen"), function () {
				if(frm.doc.party_from=="Lead"){
					frm.set_value("status","Replied")
				}
				else if(frm.doc.party_from=="Customer"){
					frm.set_value("status","Converted")
				}
				frm.save()
			},("Action")); 
		}
	}
	},
	validate(frm){
		if ((frm.doc.contacts || []).length === 0) {
			if(frm.doc.party_from == "Lead" && frm.doc.party_name){
				frappe.call({
					method: "teampro.teampro.doctype.sales_follow_up.sales_follow_up.lead_contacts",
					args: {
						lead: frm.doc.lead
					},
					
					callback: function (r) {
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
			}
		}
		if(frm.is_new()){
        	if(frm.doc.party_from == "Lead"){
        	    
			frm.set_value("follow_up_to","Lead")
			frappe.call({
					method: "teampro.teampro.doctype.sales_follow_up.sales_follow_up.lead_contacts",
					args: {
						lead: frm.doc.lead
					},
					
					callback: function (r) {
						console.log(r.message);
						frm.clear_table('custom_contact_details')
						$.each(r.message, function (i, d) {
							frm.add_child('custom_contact_details', {
								'person_name': d.person_name,
								'mobile': d.mobile,
								'is_primary': d.is_primary,
								'has_whatsapp': d.has_whatsapp,
								'email_id': d.email_id,
								'is_primaryemail': d.is_primaryemail,
								'service':d.service
							});
						});
						frm.refresh_field('custom_contact_details');
					}
				});
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
			}
		}
		
	},
	planned(frm){
		// frappe.confirm(__("Are you sure you want to change the appointment status to Planned?"), function () {
		if(frm.doc.visted_date && frm.doc.visted_by && frm.doc.appointment_remarks){
			frm.add_child('custom_appointment_details', {
				'visted_date':frm.doc.visted_date,
				'visted_by':frm.doc.visted_by,
				'appointment_remarks':frm.doc.appointment_remarks,
			});
		}
		frm.refresh_field('custom_appointment_details');  // Corrected field name
		frm.set_value("appointment_created_on",frappe.datetime.now_date())
		frm.set_value('app_status', 'Planned');
		frm.set_value('appointment_remarks', '');
		frm.set_df_property("appointment_remarks","reqd",0)
		frm.set_value('visted_by', '');
		frm.set_value('visted_date', '');
	// })
	},
	cancel(frm){
		frm.set_value('app_status','Yet to visit(YTV)')
		frm.set_value('appointment_fixed_on', '');
		frm.set_value('appointment_created_on','')
		frm.set_value('custom_appointment_fixed_for', '');
	},
	visited(frm){
		frm.set_value('app_status','Visited')
		frm.set_value('appointment_fixed_on', '');
		frm.set_value('custom_appointment_fixed_for', '');
		frm.set_value("visted_by",frappe.session.user)
		frm.set_value("visted_date",frappe.datetime.now_date())
	},
	party_type(frm){
		frm.trigger("set_dynamic_field_label");
		if (frm.doc.party_type){
			frm.set_value('follow_up_to',frm.doc.party_type)
		}
	},
	// onload(frm){
	// 	if (frm.doc.contacts) {
    //         let rows = "";
    //         frm.doc.contacts.forEach(contact => {
    //             rows += `
    //             <tr>
    //                 <td><b>${contact.person_name || ''}</b></td>
    //                 <td><b>${contact.mobile || ''}</b></td>
    //                 <td><b>${contact.email_id || ''}</b></td>
    //             </tr>`;
    //         });

    //         $(frm.fields_dict.custom_html.wrapper).html(`
    //             <table border="1" width="100%">
    //                 <tbody>
    //                     <tr>
    //                         <td style='background-color:blue;color:white;text-align:center'><b>Person Name</b></td>
    //                         <td style='background-color:blue;color:white;text-align:center'><b>Mobile</b></td>
    //                         <td style='background-color:blue;color:white;text-align:center'><b>Email</b></td>
    //                     </tr>
    //                     ${rows}
    //                 </tbody>
    //             </table>
    //         `);
    //     }
	// },
	after_insert(frm){
		frm.set_value('app_status','Yet to visit(YTV)')
		// frm.set_value('appointment_fixed_on', '');
		// frm.set_value('custom_appointment_fixed_for', '');
	},
	party_name(frm){
		if(frm.doc.party_from=="Customer" && frm.doc.party_name){
			frappe.call({
				method:"teampro.custom.organization_update_sp",
				args:{
					"customer":frm.doc.party_name
				},
				callback(r){
					if(r.message){
						frm.set_value("organization_name",r.message)
					}
				}
			})
		}
		if(frm.doc.party_from=="Lead" && frm.doc.party_name){
			frappe.call({
				method:"teampro.custom.organization_update_sp_lead",
				args:{
					"lead":frm.doc.party_name
				},
				callback(r){
					if(r.message){
						frm.set_value("organization_name",r.message)
					}
				}
			})
		}
		if (frm.doc.party_name){
			frappe.call({
				method: "teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_lead_manager",
				args: {
					'party_name': frm.doc.party_name,
					'party_type':	frm.doc.party_from,
					'name': frm.doc.name
				},
				callback: function (r) {
					if(r.message){
						frm.set_value("account_manager_lead_owner",r.message)
					}
				}
			});
			if (frm.doc.party_type){
				if (frm.doc.party_type=="Lead"){
					frm.set_value("follow_up_from","Lead")
					frm.set_value("lead",frm.doc.party_name)
				}
				else{
					frm.set_value("follow_up_from","Customer")
					frm.set_value("customer",frm.doc.party_name)
				}
			}
		}
		if(frm.doc.party_from == "Lead"){
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
			}
		
	},
	setup: function(frm)  {
		frm.set_query("party_from", function() {
			return {
				"filters": {
					"name": ["in", ["Customer", "Lead"]]
				}
			};
		});
	},
	
	set_dynamic_field_label: function(frm){
		if (frm.doc.party_from) {
			frm.set_df_property("party_name", "label", frm.doc.party_from);
		}
	},
	// status(frm){
	// 	render_status_button(frm);
	// },
	// lead(frm){
	// 	frm.set_value("follow_up_to","Lead")
	// 	frappe.call({
	// 			method: "teampro.teampro.doctype.sales_follow_up.sales_follow_up.lead_contacts",
	// 			args: {
	// 				lead: frm.doc.lead
	// 			},
				
	// 			callback: function (r) {
	// 				console.log(r.message);
	// 				frm.clear_table('contacts')
	// 				$.each(r.message, function (i, d) {
	// 					frm.add_child('contacts', {
	// 						'person_name': d.person_name,
	// 						'mobile': d.mobile,
	// 						'is_primary': d.is_primary,
	// 						'has_whatsapp': d.has_whatsapp,
	// 						'email_id': d.email_id,
	// 						'is_primaryemail': d.is_primaryemail,
	// 						'service':d.service
	// 					});
	// 				});
	// 				frm.refresh_field('contacts');
	// 			}
	// 		});
	// 	},
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
		next_contact_date(frm){
			if (frm.doc.follow_up_to =="Customer"){
				frappe.call({
					method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_customer_next_contact_date",
					args:{
						customer_name:frm.doc.customer,
						s_next_contact_date:frm.doc.next_contact_date,
						service:frm.doc.service
					},
					callback:function(r){

					}
				});
			}
			// if(frm.doc.status=="Opportunity" && frm.doc.follow_up_to=="Lead"){
			// 	frappe.call({
			// 		method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_opportunity_next_contact_date",
			// 		args:{
			// 			lead_name:frm.doc.lead,
			// 			s_next_contact_date:frm.doc.next_contact_date,
			// 			service:frm.doc.service,
			// 		},
			// 		callback:function(r){

			// 		}
			// 	});
			// }
			// if(frm.doc.status=="Opportunity" && frm.doc.follow_up_to=="Customer"){
			// 	frappe.call({
			// 		method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_opportunity_next_contact_date_from_customer",
			// 		args:{
			// 			customer:frm.doc.customer,
			// 			s_next_contact_date:frm.doc.next_contact_date,
			// 			service:frm.doc.service,
			// 		},
			// 		callback:function(r){

			// 		}
			// 	});
			// }
		},
		remarks(frm){
			frm.set_value("custom_details2",frm.doc.remarks)
			// if (frm.doc.follow_up_to =="Customer"){
			// 	frappe.call({
			// 		method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_customer_s_remarks",
			// 		args:{
			// 			customer_name:frm.doc.customer,
			// 			s_remarks:frm.doc.remarks,
			// 			service:frm.doc.service
			// 		},
			// 		callback:function(r){

			// 		}
			// 	});
			// }
			if(frm.doc.status=="Opportunity" && frm.doc.party_from=="Lead" && frm.doc.party_name){
				frappe.call({
					method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_opportunity_s_remarks",
					args:{
						lead_name:frm.doc.party_name,
						s_remarks:frm.doc.remarks,
						service:frm.doc.service,
						name:frm.doc.name
					},
					callback:function(r){

					}
				});
			}
			// if(frm.doc.status=="Opportunity"){
			// 	frappe.call({
			// 		method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_opportunity_sfp",
			// 		args:{
			// 			name:frm.doc.name,
			// 			remarks:frm.doc.remarks
			// 		},
			// 		callback:function(r){

			// 		}
			// 	});
			// }
			if(frm.doc.status=="Opportunity" && frm.doc.party_from=="Customer"){
				frappe.call({
					method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_opportunity_s_remarks_from_customer",
					args:{
						customer:frm.doc.party_name,
						name:frm.doc.name,
						s_remarks:frm.doc.remarks,
						service:frm.doc.service,
					},
					callback:function(r){

					}
				});
			}
		}
})
function render_status_button(frm) {
    if (!frm.doc.status) return; // Ensure status exists

    // Define colors for different statuses
    let status_colors = {
        "Open": "danger",          // Red
        "Converted": "success",     // Green
        "Lead": "primary",          // Blue
        "Replied": "info",          // Light Blue
        "Do Not Contact": "secondary", // Grey
        "Opportunity": "warning",   // Yellow
        "Interested": "purple"      // Custom Color (Bootstrap doesn't have purple by default)
    };

    let status_label = frm.doc.status || "Unknown"; // Get current status
    let color_class = status_colors[status_label] || "dark"; // Default to dark if not found

    // Custom color for "Interested" (since Bootstrap doesn't have 'purple' by default)
    let custom_style = (status_label === "Interested") ? "background-color: #6f42c1; color: white;" : "";

    // HTML button element
    let html_content = `
        <button class="btn btn-${color_class}" disabled style="font-weight: bold; ${custom_style}">
            ${status_label}
        </button>
    `;

    // Set the HTML field value
    frm.set_df_property('custom_status_html', 'options', html_content);
}