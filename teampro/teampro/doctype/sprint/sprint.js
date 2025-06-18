// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sprint", {
	validate(frm) {
        if(frm.doc.__islocal){
        if(frm.doc.from_date && frm.doc.to_date){
            frappe.call({
                method:"teampro.teampro.doctype.sprint.sprint.get_working_days",
                args:{
                    from_date:frm.doc.from_date,
                    to_date:frm.doc.to_date
                },
                callback(r){
                    if(r.message){
                        frm.doc.sprint_avl_time.forEach(row => {
                            if (row.tl == 1) {
                                row.available_hours = r.message * 5;
                            } else {
                                row.available_hours = r.message * 6;
                            }
                        });
                        frm.refresh_field('sprint_avl_time');
                    }
                }
            })
            
            // const fromDate = frappe.datetime.str_to_obj(frm.doc.from_date);
            // const toDate = frappe.datetime.str_to_obj(frm.doc.to_date);
            // const diffTime = toDate - fromDate; 
            // const diffDays = diffTime / (1000 * 60 * 60 * 24); 
            //     frm.doc.sprint_avl_time.forEach(row => {
            //     if (row.tl == 1) {
            //         row.available_hours = diffDays * 5;
            //     } else {
            //         row.available_hours = diffDays * 6;
            //     }
            // });
            // frm.refresh_field('sprint_avl_time');
        }
        
    }
	},
    refresh(frm){
        if (frm.doc.status=="In Progress"){
            frm.add_custom_button(__("Create DPR"), function () {
                frappe.model.with_doctype('Daily Monitor', function () {
                let sfu = frappe.model.get_new_doc('Daily Monitor');
                sfu.service = "IT-SW";
                sfu.task_type = "OPS";
                sfu.dev_team = frm.doc.team;
                sfu.sprint = frm.doc.sprint_id;
                frappe.db.insert(sfu).then(doc => {
                    frappe.set_route("Form", "Daily Monitor", doc.name);
                });
            });
            })
        }
        frm.add_custom_button(__("Send Planned Mail"),function(){
            frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method: 'teampro.teampro.doctype.daily_monitor.dm_it_dev.send_sprint_panned_mail',
                        args: {
                            name: frm.doc.name,
                            sprint_id:frm.doc.sprint_id,
                            team:frm.doc.team
                        }
                    });
        })
    },
    team(frm){
        if(frm.doc.team){
            frappe.call({
                method:"teampro.teampro.doctype.sprint.sprint.update_sprint",
                args:{
                    name:frm.doc.name,
                    team:frm.doc.team
                },
                callback(r){
                    if(r.message){
                        frm.set_value("sprint_id",r.message)
                    }
                }
            })
        }
    },
    before_workflow_action: async (frm) => {
        if (frm.doc.workflow_state == "Draft" && frm.selected_workflow_action == "Planned") {
                try {
                    await frappe.call({
                        freeze: true,
                        freeze_message: 'Loading',
                        method: 'teampro.teampro.doctype.daily_monitor.dm_it_dev.send_sprint_panned_mail',
                        args: {
                            name: frm.doc.name,
                            sprint_id:frm.doc.sprint_id,
                            team:frm.doc.team
                        },
                        callback(r){
                            frappe.msgprint("SPM has been sent successfully.")
                        }
                    });
                } catch (err) {
                    frappe.throw(`Failed to send DPR: ${err.message || err}`);
                }
            }
    }
});
