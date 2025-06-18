// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Daily Monitor", {
    // sprint(frm){
    //     frappe.call({
    //         method:"teampro.teampro.doctype.daily_monitor.daily_monitor.load_sprint_data",
    //         args: {
    //             sprint:frm.doc.sprint,
    //             dev_team:frm.doc.dev_team,
    //             name:frm.doc.name
    //         },
    //         callback: function (r) {
    //             frm.reload_doc();
    //         }

    //     })
    // },
    // refresh:function(frm){
    //     if(frm.doc.dm_status == "Draft"){
    //         frm.add_custom_button(__("Get DPR"), function () {
    //             frm.clear_table('task_details');
    //             if (frm.doc.service=="IT-SW"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method:'teampro.teampro.doctype.daily_monitor.daily_monitor_update_cs.get_allocated_tasks_for_it_cs_update',
    //                     args: {
    //                         date: frm.doc.date,
    //                         name:frm.doc.name,
    //                         service:frm.doc.service,
    //                         type:frm.doc.task_type
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //             }
    //         frm.clear_table("dm_rec_task_details")
    //         if (frm.doc.service=="REC-I"){
    //             frappe.call({
    //                 freeze: true,
    //                 freeze_message: 'Loading',
    //                 method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rec_allocated_tasks',
    //                 args: {
    //                     name:frm.doc.name,
    //                     service:frm.doc.service,
    //                     date:frm.doc.date
    //                 },
    //                 callback: function (r) {
    //                 }
                    
    //             });
    //         }
    //         frm.clear_table("dnd_summary")
    //         if (frm.doc.type=="DND"){
    //             frappe.call({
    //                 freeze: true,
    //                 freeze_message: 'Loading',
    //                 method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.dnd_allocated_tasks',
    //                 args: {
    //                     name:frm.doc.name,
    //                     date:frm.doc.date
    //                 },
    //                 callback: function (r) {
    //                 }
                    
    //             });
    //         }
            
    //     },('Action'));
    //     }
    //     if(frm.doc.dm_status == "DPR Pending"){
    //         frm.add_custom_button(__("Send DPR"), function () {
    //             if (frm.doc.service=="IT-SW"){
    //                 frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_dev.dpr_task_mail_it_dev',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             dev_team:frm.doc.dev_team,
    //                             sprint:frm.doc.sprint,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
                    
    //             }
    //             if (frm.doc.service=="REC-I"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.update_rec_dpr',
    //                     args: {
    //                         name:frm.doc.name,
    //                         date:frm.doc.date,
    //                         service:frm.doc.service
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //             }
    //             if (frm.doc.type=="DND"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.dnd_send_dpr_dsr',
    //                     args: {
    //                         name:frm.doc.name,
    //                         date:frm.doc.date
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //             }
    //         },("Action"));
    //         frm.add_custom_button(__("Get DPR"), function () {
    //             if (frm.doc.service=="IT-SW"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method:'teampro.teampro.doctype.daily_monitor.daily_monitor_update_cs.get_allocated_tasks_for_it_cs_update',
    //                     args: {
    //                         date: frm.doc.date,
    //                         name:frm.doc.name,
    //                         service:frm.doc.service,
    //                         type:frm.doc.task_type
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //                 frm.refresh_field('task_details');
    //             }
    //         if (frm.doc.service=="REC-I"){
    //             frappe.call({
    //                 freeze: true,
    //                 freeze_message: 'Loading',
    //                 method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rec_allocated_tasks',
    //                 args: {
    //                     name:frm.doc.name,
    //                     service:frm.doc.service,
    //                     date:frm.doc.date
    //                 },
    //                 callback: function (r) {
    //                 }
                    
    //             });
    //         }
    //         if (frm.doc.type=="DND"){
    //             frappe.call({
    //                 freeze: true,
    //                 freeze_message: 'Loading',
    //                 method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.dnd_allocated_tasks',
    //                 args: {
    //                     name:frm.doc.name,
    //                     date:frm.doc.date
    //                 },
    //                 callback: function (r) {
    //                 }
                    
    //             });
    //         }
    //         },('Action'));
    //     }
       
    //     if(frm.doc.dm_status == "DSR Pending"){
    //         frm.add_custom_button(__("Send DSR"), function () {
    //             if (frm.doc.service=="IT-SW"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     // method:'teampro.teampro.doctype.daily_monitor.daily_monitor_update_cs.dpr_task_mail_cs_it_update',
    //                     method:'jobpro.custom.dsr_mail',
    //                     args: {
    //                             date: frm.doc.date,
    //                             name:frm.doc.name,
    //                             service:frm.doc.service,
    //                             task_type:frm.doc.task_type
    //                         },
    //                     callback: function (r) {
    //                     }
                                        
    //                 });
    //             }
                
    //             if (frm.doc.service=="REC-I"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.update_rec_dpr',
    //                     args: {
    //                         name:frm.doc.name,
    //                         date:frm.doc.date,
    //                         service:frm.doc.service
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //             }
    //             if (frm.doc.type=="DND"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.dnd_send_dpr_dsr',
    //                     args: {
    //                         name:frm.doc.name,
    //                         date:frm.doc.date
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //             }

    //         },('Action'));
    //         frm.add_custom_button(__("Get DSR"), function () {
    //             frm.clear_table('task_details');
    //             if (frm.doc.service=="IT-SW"){
    //                 frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_dev.update_allocated_task_at_dev',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             type:frm.doc.task_type,
    //                             dev_team:frm.doc.dev_team,
    //                             sprint:frm.doc.sprint,
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
                    
    //             }
    //             if (frm.doc.service=="REC-I"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.rec_update_dsr',
    //                     args: {
    //                         name:frm.doc.name,
    //                         date:frm.doc.date
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //             }
    //             if (frm.doc.type=="DND"){
    //                 frappe.call({
    //                     freeze: true,
    //                     freeze_message: 'Loading',
    //                     method : 'teampro.teampro.doctype.daily_monitor.daily_monitor.dnd_update_dsr',
    //                     args: {
    //                         name:frm.doc.name,
    //                         date:frm.doc.date
    //                     },
    //                     callback: function (r) {
    //                     }
                        
    //                 });
    //             }

    //         },('Action'));
       
    //     }   
              
    //             frm.add_custom_button(__("Send DPR For IT"),function(){
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_dev.dpr_task_mail_it_dev',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             dev_team:frm.doc.dev_team,
    //                             sprint:frm.doc.sprint,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
    //                 }
    //             },('DEV Action'));
    //             frm.add_custom_button(__("Get DSR For IT"),function(){
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_dev.update_allocated_task_at_dev',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             type:frm.doc.task_type,
    //                             dev_team:frm.doc.dev_team,
    //                             sprint:frm.doc.sprint,
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
                      
    //                 }
    //             },('DEV Action'));
    //             frm.add_custom_button(__("Send DSR For IT"),function(){
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_dev.dpr_task_mail_it_dev',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             dev_team:frm.doc.dev_team,
    //                             sprint:frm.doc.sprint,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
    //                 }
    //             },('DEV Action'));
    //             frm.add_custom_button(__("Get DPR For CS"),function(){
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_cs.get_allocated_tasks_for_it_cs',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
    //                 }
    //             },('CS Action'));
    //             frm.add_custom_button(__("Send DPR For CS"),function(){
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_cs.dpr_mail_it_cs',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
    //                 }
    //             },('CS Action'));
    //             frm.add_custom_button(__("Get DSR For CS"),function(){
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_cs.update_it_cs',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
    //                 }
    //             },('CS Action'));
    //             frm.add_custom_button(__("Send DSR For CS"),function(){
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_cs.dpr_mail_it_cs',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
    //                 }
    //             },('CS Action'));
       
    // }
    // before_workflow_action: async (frm) => {
    //        if (frm.doc.workflow_state == "Draft") {
	// 		let promise = new Promise((resolve, reject) => {
	// 			if (frm.selected_workflow_action == "Send DPR") {
    //                 if (frm.doc.service=="IT-SW"){
    //                     frappe.call({
    //                         freeze: true,
    //                         freeze_message: 'Loading',
    //                         method : 'teampro.teampro.doctype.daily_monitor.dm_it_dev.dpr_task_mail_it_dev',
    //                         args: {
    //                             name:frm.doc.name,
    //                             date:frm.doc.date,
    //                             service:frm.doc.service,
    //                             dev_team:frm.doc.dev_team,
    //                             sprint:frm.doc.sprint,
    //                             type:frm.doc.task_type
    //                         },
    //                         callback: function (r) {
    //                         }
                            
    //                     });
    //                 }
                    
	// 			}
	// 			resolve();
	// 		});
	// 		await promise.catch((error) => frappe.throw(error));
	// 	}
    // }
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
// });

frappe.ui.form.on("Daily Monitor",{
     refresh(frm){
      console.log("Working")  
      user = frappe.session.user
      console.log(user)
      tl = frappe.get_doc("Employee",{"user_id":user},["name"])
      console.log(tl.name)
      
    },
    // refresh: function(frm){
    //     frm.add_custom_button(__("Demo"),function(){
    //         frappe.call({
    //             method:"teampro.teampro.doctype.daily_monitor.dm_it_dev.dpr_task_mail_it_dev",
    //             args:{
    //                 date:frm.doc.date,
    //                 name:frm.doc.name,
    //                 service:frm.doc.service,
    //                 type:frm.doc.task_type,
    //                 dev_team:frm.doc.dev_team,
    //                 sprint:frm.doc.sprint
    //             },
    //             callback(r){
    //                 console.log(r.message)
                    
                    
    //             }

    //         })

    //     });

    // },

    custom_dm_production_date(frm) {
    console.log("OMG it is Working..........");

    frappe.call({
        method: "teampro.teampro.doctype.daily_monitor.dm_it_dev_update.get_tl",
        args: {
            date: frm.doc.custom_dm_production_date,
            name: frm.doc.name,
            service: frm.doc.service,
            type: frm.doc.task_type,
            dev_team: frm.doc.dev_team,
            sprint: frm.doc.sprint
        },
        callback: function (r) {
            if (r.message && Array.isArray(r.message)) {
                frm.clear_table('task_details');
                console.log( r.message);

                r.message.forEach(function (d) {
                    let row = frm.add_child("task_details");
                    row.id =d.name; 
                    row.project_name = d.project_name;
                    row.subject = d.subject;
                    row.cb = d.cb;
                    row.status = d.status;
                    row.revisions = d.revisions;
                });

                frm.refresh_field('task_details');
            } else {
                console.warn("No task data received or response is invalid.");
            }
        },
        error: function (err) {
            console.error("Frappe call failed:", err);
        }
    });
},

// validate:function(frm){

//     if(doc.task_details && doc.dm_status!="Submitted" ){

//     }
// }



});