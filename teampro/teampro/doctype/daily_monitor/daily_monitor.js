// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Monitor",{
    onload(frm){
        if(frm.doc.service ==='CMN'){
            frappe.meta.get_docfield('Allocated Tasks', 'revisions', frm.doc.name).hidden = 1;
            frappe.meta.get_docfield('Allocated Tasks', 'tl_remark', frm.doc.name).hidden = 1;
        }

    },
     refresh(frm){
        // frm.add_custom_button(__('Send DSR Test'), function() {
        //         frappe.call({
        //             freeze: true,
        //             freeze_message: 'Loading',
        //             method: 'teampro.teampro.doctype.daily_monitor.dm_it_dev.dsr_task_mail_it_dev_hod',
        //             args: {
        //                 name: frm.doc.name,
        //                 date: frm.doc.date,
        //                 service: frm.doc.service,
        //                 dev_team: frm.doc.dev_team,
        //                 sprint: frm.doc.sprint,
        //             }
        //         });
        
        //     })
      user = frappe.session.user
      tl = frappe.get_doc("Employee",{"user_id":user},["name"])
      if(frm.doc.dm_status=="DPR Completed"){
        frm.add_custom_button(__('Update DM'), function() {
            frappe.call({
                method: "teampro.teampro.doctype.daily_monitor.dm_it_dev.run_daily_monitor_update_team",
                args: {
                    date: frm.doc.custom_dm_production_date,
                    name: frm.doc.name,
                    dev_team: frm.doc.dev_team,
                    sprint: frm.doc.sprint,
                    service:frm.doc.service,
                    task_type: frm.doc.task_type
                },
                callback: function (r) {
                }
            })
        })
        if(frm.doc.workflow_state == "Pending for HOD (DPR)" && frm.doc.dm_status=="DPR Pending"){
            frm.add_custom_button(__('Send DPR'), function() {
                frappe.call({
                    freeze: true,
                    freeze_message: 'Loading',
                    method: 'teampro.teampro.doctype.daily_monitor.dm_it_dev.dpr_task_mail_it_dev_md',
                    args: {
                        name: frm.doc.name,
                        date: frm.doc.date,
                        service: frm.doc.service,
                        dev_team: frm.doc.dev_team,
                        sprint: frm.doc.sprint,
                    }
                });
        
            })
        }
      }
    //   frm.add_custom_button(__('Send DSR'), function() {

    //         frappe.call({
    //             method: "teampro.teampro.doctype.daily_monitor.dm_it_dev.dpr_task_mail_it_dev",
    //             args: {
    //                 date:frm.doc.date,
    //                 name: frm.doc.name,
    //                 service: frm.doc.service,
    //                 dev_team: frm.doc.dev_team,
    //                 sprint: frm.doc.sprint
    //             },
    //             freeze: true,
    //             freeze_message: __("Sending mail..."),
    //             callback: function(r) {
    //                 frappe.msgprint(__('Mail triggered successfully'));
    //             }
    //         });

    // });
    },
    
    custom_dm_production_date(frm) {
    if(frm.doc.service ==='CMN' && frm.doc.custom_dm_production_date){
        frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Project",
                    filters: {
                        service: frm.doc.service,
                        status: "Open"
                    },
                    fields: ["name"]
                },
                callback: function(projectsRes) {
                    frm.clear_table('task_details');
                    if (projectsRes.message && projectsRes.message.length > 0) {
                        projectsRes.message.forEach(function(project) {
                            frappe.call({
                                method: "frappe.client.get_list",
                                args: {
                                    doctype: "Task",
                                    filters: {
                                        service: frm.doc.service,
                                        status: ["not in", ["Cancelled","Hold"]],
                                        project: project.name,
                                        // allocated:1,
                                        custom_production_date:frm.doc.custom_dm_production_date
                                    },
                                    fields: [
                                        "name",
                                        "subject",
                                        "expected_time",
                                        "actual_time",
                                        "custom_allocated_to",
                                        "cb",
                                        "status",
                                        "project_name",
                                        "rt"
                                    ],
                                },
                                callback: function(task_response) {
                                    
                                    if (task_response.message && task_response.message.length > 0) {
                                        task_response.message.forEach(function(d) {
                

                    let row = frm.add_child("task_details");
                    row.id =d.name; 
                    row.project_name = d.project_name;
                    row.subject = d.subject;
                    row.cb = d.cb;
                    row.status = d.status;
                    row.project_name =d.project_name;
                    row.rt =d.rt;
                    row.today_rt= d.rt;
                });

                frm.refresh_field('task_details');
            } else {
                console.warn("No task data received or response is invalid.");
            }
                                    
                                }
                            });
                        });
                    } else {
                        frappe.msgprint("No open projects found for service: CMN");
                    }
                }
            });
        }
        
    else{
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
}
},




});

frappe.ui.form.on("Allocated Tasks", {
    raise_nc(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        raise_nc(frm, child);
    }
});

function raise_nc(frm, child) {
    frappe.db.get_value('Employee', {'short_code': child.cb}, ['name'])
        .then(r => {
            if (r.message) {
                let emp_name = r.message.name;
                frappe.db.get_value('Energy Point And Non Conformity', {
                    task: child.id,
                    emp: emp_name,
                    docstatus: ['!=',2]
                }, 'name').then(existing => {
                    if (existing.message.name) {
                        // console.log(existing.message)
                        frappe.set_route('Form', 'Energy Point And Non Conformity', existing.message.name);
                    } else {
                        // console.log("TEST2")
                        frappe.model.with_doctype('Energy Point And Non Conformity', function() {
                            let nc = frappe.model.get_new_doc('Energy Point And Non Conformity');
                            nc.action = 'Non Conformity(NC)';
                            nc.task = child.id;
                            nc.emp = r.message.name; 
                            nc.class_proposed='Minor';
                            frappe.set_route('Form', 'Energy Point And Non Conformity', nc.name);
                        });
                    }
                });
            }
        });
}

