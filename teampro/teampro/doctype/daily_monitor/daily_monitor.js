// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Monitor", {
    refresh:function(frm){
        if(frm.doc.dm_status == "Draft"){
            frm.add_custom_button(__("Get DPR"), function () {
                frm.clear_table('task_details');
                if (frm.doc.service=="IT-SW"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        // method : 'teampro.custom.get_allocated_tasks',
                        method:'teampro.teampro.doctype.daily_monitor.daily_monitor.get_allocated_tasks_for_it_cs',
                        args: {
                            date: frm.doc.date,
                            name:frm.doc.name,
                            service:frm.doc.service,
                            type:frm.doc.task_type
                        },
                        // freeze: true,
                        // freeze_message: 'Loading',
                        callback: function (r) {
                            // frm.set_value("status","DPR Pending")
                        }
                        
                    });
                    // frm.refresh_field('task_details');
                    // frm.save()
                }
            frm.clear_table("dm_rec_task_details")
            if (frm.doc.service=="REC-I"){
                frappe.call({
                    freeze: true,
                    freeze_message: 'Loading',
                    method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rec_allocated_tasks',
                    args: {
                        name:frm.doc.name,
                        service:frm.doc.service,
                        date:frm.doc.date
                    },
                    callback: function (r) {
                    }
                    
                });
                // frm.refresh_field('dm_rec_task_details');
            }
                // frm.clear_table("dm_sales_details")
                if (frm.doc.department =="R&S - THIS"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.sales_allocated_tasks',
                        args: {
                            name:frm.doc.name,
                            // service:frm.doc.service,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }
            
        },('Action'));
        }
        if(frm.doc.dm_status == "DPR Pending"){
            frm.add_custom_button(__("Send DPR"), function () {
                // frm.clear_table('task_details');
                if (frm.doc.service=="IT-SW"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        // method : 'teampro.custom.dpr_task_mail',
                        method:'teampro.teampro.doctype.daily_monitor.daily_monitor.dpr_task_mail_cs_it',
                        args: {
                                date: frm.doc.date,
                                name:frm.doc.name,
                                service:frm.doc.service,
                                task_type:frm.doc.task_type
                            },
                        callback: function (r) {
                            // frm.set_value("status","DPR Completed")
                        }
                                        
                    });
                }
                if (frm.doc.service=="REC-I"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.update_rec_dpr',
                        args: {
                            name:frm.doc.name,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }
                if (frm.doc.department =="R&S - THIS"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.update_sales_dpr',
                        args: {
                            name:frm.doc.name,
                            // service:frm.doc.service,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }
            },('Action'));
            frm.add_custom_button(__("Get DPR"), function () {
                // frm.clear_table('task_details');
                if (frm.doc.service=="IT-SW"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        // method : 'teampro.custom.get_allocated_tasks',
                        method:'teampro.teampro.doctype.daily_monitor.daily_monitor.get_allocated_tasks_for_it_cs',
                        args: {
                            date: frm.doc.date,
                            name:frm.doc.name,
                            service:frm.doc.service,
                            type:frm.doc.task_type
                        },
                        // freeze: true,
                        // freeze_message: 'Loading',
                        callback: function (r) {
                            // frm.set_value("status","DPR Pending")
                        }
                        
                    });
                    frm.refresh_field('task_details');
                    // frm.save()
                }
            // frm.clear_table("dm_rec_task_details")
            if (frm.doc.service=="REC-I"){
                frappe.call({
                    freeze: true,
                    freeze_message: 'Loading',
                    method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rec_allocated_tasks',
                    args: {
                        name:frm.doc.name,
                        service:frm.doc.service,
                        date:frm.doc.date
                    },
                    callback: function (r) {
                    }
                    
                });
                // frm.refresh_field('dm_rec_task_details');
            }
            // frm.clear_table("dm_sales_details")
                if (frm.doc.department =="R&S - THIS"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.sales_allocated_tasks',
                        args: {
                            name:frm.doc.name,
                            // service:frm.doc.service,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }
            },('Action'));
        }
        if(frm.doc.dm_status == "DPR Completed"){
            frm.add_custom_button(__("Get DSR"), function () {
                frm.clear_table('task_details');
                if (frm.doc.service=="IT-SW"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        // method : 'teampro.custom.update_dsr',
                        method:"teampro.teampro.doctype.daily_monitor.daily_monitor.update_dsr_cs_it",
                        args: {
                                date: frm.doc.date,
                                name:frm.doc.name,
                                service:frm.doc.service,
                                type:frm.doc.task_type
                                
                            },
                        callback: function (r) {
                        }
                    });
                }
                if (frm.doc.service=="REC-I"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rec_update_dsr',
                        args: {
                            name:frm.doc.name,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                    // frm.refresh_field('dm_rec_task_details');
                }
                if (frm.doc.department =="R&S - THIS"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rs_update_dsr',
                        args: {
                            name:frm.doc.name,
                            // service:frm.doc.service,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }
            },('Action'));
        }
        if(frm.doc.dm_status == "DSR Pending"){
            frm.add_custom_button(__("Send DSR"), function () {
                // frm.clear_table('task_details');
                if (frm.doc.service=="IT-SW"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        // method : 'teampro.custom.dpr_task_mail',
                        method:'teampro.teampro.doctype.daily_monitor.daily_monitor.dpr_task_mail_cs_it',
                        args: {
                                date: frm.doc.date,
                                name:frm.doc.name,
                                service:frm.doc.service,
                                task_type:frm.doc.task_type
                            },
                        callback: function (r) {
                        }
                                        
                    });
                }
                
                if (frm.doc.service=="REC-I"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.update_rec_dpr',
                        args: {
                            name:frm.doc.name,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }
                if (frm.doc.department =="R&S - THIS"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.update_sales_dpr',
                        args: {
                            name:frm.doc.name,
                            // service:frm.doc.service,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }

            },('Action'));
            frm.add_custom_button(__("Get DSR"), function () {
                frm.clear_table('task_details');
                if (frm.doc.service=="IT-SW"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        // method : 'teampro.custom.update_dsr',
                        method:"teampro.teampro.doctype.daily_monitor.daily_monitor.update_dsr_cs_it",
                        args: {
                                date: frm.doc.date,
                                name:frm.doc.name,
                                service:frm.doc.service,
                                type:frm.doc.task_type
                                
                            },
                        callback: function (r) {
                        }
                    });
                }
                if (frm.doc.service=="REC-I"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rec_update_dsr',
                        args: {
                            name:frm.doc.name,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                    // frm.refresh_field('dm_rec_task_details');
                }
                if (frm.doc.department =="R&S - THIS"){
                    frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rs_update_dsr',
                        args: {
                            name:frm.doc.name,
                            // service:frm.doc.service,
                            date:frm.doc.date
                        },
                        callback: function (r) {
                        }
                        
                    });
                }
            },('Action'));
       
        }
    }
    // before_workflow_action: async (frm) => {
    //     if (frm.doc.workflow_state == "Draft") {
	// 		let promise = new Promise((resolve, reject) => {
	// 			if (frm.selected_workflow_action == "Get DPR") {
    //                 // frm.clear_table('task_details');
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                         method : 'teampro.custom.get_allocated_tasks',
    //                         args: {
    //                             date: frm.doc.date,
    //                             name:frm.doc.name,
    //                             service:frm.doc.service,
    //                             type:frm.doc.task_type
    //                         },
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                         callback: function (r) {
                               
    //                         }
                            
    //                     });
    //                     // frm.refresh_field('task_details');
    //                 }
                    
	// 			}
	// 			resolve();
	// 		});
	// 		await promise.catch((error) => frappe.throw(error));
	// 	}
	// 	if (frm.doc.workflow_state == "DPR Pending") {
	// 		let promise = new Promise((resolve, reject) => {
	// 			if (frm.selected_workflow_action == "Send DPR") {
	// 				if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                         method : 'teampro.custom.dpr_task_mail',
    //                         args: {
    //                                 date: frm.doc.date,
    //                                 name:frm.doc.name,
    //                                 service:frm.doc.service
    //                             },
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                     });
    //                 }
	// 			}
	// 			resolve();
	// 		});
	// 		await promise.catch((error) => frappe.throw(error));
	// 	}
    //     if (frm.doc.workflow_state == "DPR Completed") {
	// 		let promise = new Promise((resolve, reject) => {
	// 			if (frm.selected_workflow_action == "Get DSR") {
	// 				if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                         method : 'teampro.custom.update_dsr',
    //                         args: {
    //                                 date: frm.doc.date,
    //                                 name:frm.doc.name,
    //                                 service:frm.doc.service,
    //                                 type:frm.doc.task_type
                                    
    //                             },
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                         callback: function (r) {
    //                             // if (r.message) {
    //                             //     frm.fields_dict.html.$wrapper.empty().append(r.message);
    //                             // }
    //                         }
    //                     });
    //                     }
	// 			}
	// 			resolve();
	// 		});
	// 		await promise.catch((error) => frappe.throw(error));
	// 	}
    //     if (frm.doc.workflow_state == "DSR Pending") {
	// 		let promise = new Promise((resolve, reject) => {
	// 			if (frm.selected_workflow_action == "Send DSR") {
	// 				if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                         method : 'teampro.custom.dpr_task_mail',
    //                         args: {
    //                                 date: frm.doc.date,
    //                                 name:frm.doc.name,
    //                                 service:frm.doc.service
    //                             },
    //                         // freeze: true,
    //                         // freeze_message: 'Loading',
    //                     });
    //                 }
	// 			}
	// 			resolve();
	// 		});
	// 		await promise.catch((error) => frappe.throw(error));
	// 	}
	// }
        // get_task(frm){
        //     frm.clear_table('task_details');
        //     if (frm.doc.service=="IT-SW"){
        //         frappe.call({
        //             freeze: true,
        //             freeze_message: 'Loading',
        //             method : 'teampro.custom.get_allocated_tasks',
        //             args: {
        //                 date: frm.doc.date,
        //                 name:frm.doc.name,
        //                 service:frm.doc.service,
        //                 type:frm.doc.task_type
        //             },
        //             // freeze: true,
        //             // freeze_message: 'Loading',
        //             callback: function (r) {
        //                 if (r.message) {
        //                     frm.fields_dict.html.$wrapper.empty().append(r.message);
        //                 }
        //             }
                    
        //         });
        //         frm.refresh_field('task_details');
        //     }
        //     if (frm.doc.service=="REC-I"){
        //         frappe.call({
        //             freeze: true,
        //             freeze_message: 'Loading',
        //             method : 'teampro.custom.rec_allocated_tasks',
        //             args: {
        //                 name:frm.doc.name,
        //                 service:frm.doc.service,
        //                 date:frm.doc.date
        //             },
        //             callback: function (r) {
        //             }
                    
        //         });
        //         frm.refresh_field('dm_rec_task_details');
        //     }
        //     // frm.save();
        // },
        // date(frm){
        //     frm.save()
        // },
        // send_alert(frm){
        //     if (frm.doc.service=="IT-SW"){
        //     frappe.call({
        //         freeze: true,
		// 		freeze_message: 'Loading',
        //         method : 'teampro.custom.dpr_task_mail',
        //         args: {
        //              date: frm.doc.date,
        //              name:frm.doc.name,
        //              service:frm.doc.service
        //          },
        //         // freeze: true,
		// 		// freeze_message: 'Loading',
        //     });
        // }
        // if (frm.doc.service=="REC-I"){
        //     frappe.call({
        //         freeze: true,
        //         freeze_message: 'Loading',
        //         method : 'teampro.custom.update_rec_dpr',
        //         args: {
        //             name:frm.doc.name,
        //             date:frm.doc.date
        //         },
        //         callback: function (r) {
        //         }
                
        //     });
        // }
        // },
        // update_dsr(frm){
        //     frm.clear_table('task_details');
        //     if (frm.doc.service=="IT-SW"){
        //     frappe.call({
        //         freeze: true,
		// 		freeze_message: 'Loading',
        //         method : 'teampro.custom.update_dsr',
        //         args: {
        //              date: frm.doc.date,
        //              name:frm.doc.name,
        //              service:frm.doc.service,
        //              type:frm.doc.task_type
                     
        //          },
        //         // freeze: true,
        //         // freeze_message: 'Loading',
        //         callback: function (r) {
        //             if (r.message) {
        //                 frm.fields_dict.html.$wrapper.empty().append(r.message);
        //             }
        //         }
        //     });
        // }
        // if (frm.doc.service=="REC-I"){
        //     frappe.call({
        //         freeze: true,
        //         freeze_message: 'Loading',
        //         method : 'teampro.custom.rec_update_dsr',
        //         args: {
        //             name:frm.doc.name,
        //             service:frm.doc.service,
        //             date:frm.doc.date
        //         },
        //         callback: function (r) {
        //         }
                
        //     });
        //     // frm.refresh_field('dm_rec_task_details');
        // }
        // },
        // refresh: function(frm) {
        //     if (frm.doc.workflow_state === "Submitted") {
        //         $.each(frm.fields_dict, function(fieldname, field) {
        //             frm.set_df_property(fieldname, 'read_only', 1);
        //         });
        //     }
        // },
});
