// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt


frappe.ui.form.on('Daily Status Meeting - DSM', {
    refresh(frm){
        if (!frappe.user.has_role("System Manager")) {
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Employee",
                    filters: { name: frm.doc.employee },
                    fieldname: "user_id"
                },
                callback: function(r) {
                    if (r.message) {
                        let emp_code = r.message.user_id;

                        frm.set_query(
                            "id",      
                            "todo_details",
                            function(doc, cdt, cdn) {
                                return {
                                    filters: {
                                        allocated_to: emp_code 
                                    }
                                };
                            }
                        );

                    }
                }
            });

        }
    }, 
    employee(frm){
        if (!frappe.user.has_role("System Manager")) {
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Employee",
                    filters: { name: frm.doc.employee },
                    fieldname: "user_id"
                },
                callback: function(r) {
                    if (r.message) {
                        let emp_code = r.message.user_id;

                        frm.set_query(
                            "id",      
                            "todo_details",
                            function(doc, cdt, cdn) {
                                return {
                                    filters: {
                                        allocated_to: emp_code 
                                    }
                                };
                            }
                        );

                    }
                }
            });

        }

    },
    onload: function(frm) {
        if (!frm.doc.employee) {
            frappe.db.get_list('Employee', {
                filters: { user_id: frappe.session.user },
                fields: ['name'],
                limit_page_length: 1
            }).then(r => {
                if (r.length) {
                    frm.set_value('employee', r[0].name);
                }
            });
        }
        if (!frm.is_new()) {
            frm.doc.__unsaved = 0;
        }

        if (!frm.doc.opportunity_with_sf || frm.doc.opportunity_with_sf.length === 0) {
            opportunity_with_sf_details(frm, 0);
        }

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Sales Follow Up",
                fields: ["status"],
                filters: {
                    next_contact_date: frm.doc.dsm_date
                },
                limit_page_length: 1000
            },
            callback: function(r) {

                let counts = {
                    "Lead": 0,
                    "Open": 0,
                    "Replied": 0,
                    "Opportunity": 0,
                    "Quotation": 0,
                    "Lost Quotation": 0,
                    "Interested": 0,
                    "Converted": 0,
                    "Customer": 0,
                    "Do Not Contact": 0
                };

                (r.message || []).forEach(row => {
                    if (counts[row.status] != undefined) {
                        counts[row.status]++;
                    }
                });

                frm.set_value("lead", counts["Lead"]);
                frm.set_value("open", counts["Open"]);
                frm.set_value("replied", counts["Replied"]);
                frm.set_value("opportunity", counts["Opportunity"]);
                frm.set_value("quotation", counts["Quotation"]);
                frm.set_value("lost_quotation", counts["Lost Quotation"]);
                frm.set_value("interested", counts["Interested"]);
                frm.set_value("converted", counts["Converted"]);
                frm.set_value("customer", counts["Customer"]);
                frm.set_value("do_not_contact", counts["Do Not Contact"]);
            }
        });


        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Project",
                filters: {
                    custom_spoc__next_contact_on: frm.doc.dsm_date,
                    service: "IT-SW",
                    "status":"Open"
                }
            },
            callback: function(r) {
                frm.set_value("it", r.message || 0);
            }
        });


        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Project",
                filters: {
                    custom_spoc__next_contact_on: frm.doc.dsm_date,
                    service: ["in",["REC-I","REC-D"]],
                    "status":"Open"
                }
            },
            callback: function(r) {
                frm.set_value("rec", r.message || 0);
            }
        });


        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Project",
                fields: ["name"],
                filters: {
                    custom_spoc__next_contact_on: frm.doc.dsm_date,
                    service: "IT-SW",
                    status:"Open"
              },
                limit_page_length: 1000
            },
            callback: function(r) {

                let project_list = (r.message || []).map(p => p.name);

                if (project_list.length > 0) {

                    frappe.call({
                        method: "frappe.client.get_count",
                        args: {
                            doctype: "Task",
                            filters: {
                                project: ["in", project_list],
                                status:["in",["Open", "Working", "Pending Review", "Client Review", "Overdue"]]
                            }
                        },
                        callback: function(res) {
                            frm.set_value("it_task", res.message || 0);
                        }
                    });

                } else {
                    frm.set_value("it_task", 0);
                }
            }
        });


        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Project",
                fields: ["name"],
                filters: {
                    custom_spoc__next_contact_on: frm.doc.dsm_date,
                    service: ["in",["REC-I","REC-D"]],
                    status:"Open"
                },
                limit_page_length: 1000
            },
            callback: function(r) {

                let project_list = (r.message || []).map(p => p.name);

                if (project_list.length > 0) {

                    frappe.call({
                        method: "frappe.client.get_count",
                        args: {
                            doctype: "Task",
                            filters: {
                                project: ["in", project_list],
                                status:["in",["Open", "Working", "Overdue"]]
                            }
                        },
                        callback: function(res) {
                            frm.set_value("rec_task", res.message || 0);
                        }
                    });

                } else {
                    frm.set_value("rec_task", 0);
                }
            }
        });


        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Candidate",
                filters: {
                    custom_next_contact_on: frm.doc.dsm_date,
                    pending_for: ["in",["Sourced", "Pending QC", "Submitted (SPOC)", "Submitted (Client)"]],
                }
            },
            callback: function(r) {
                frm.set_value("ip", r.message || 0);
            }
        });
        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Candidate",
                filters: {
                    custom_next_contact_on: frm.doc.dsm_date,
                    pending_for: ["in",["Interviewed", "Reported", "Result Pending"]],
                }
            },
            callback: function(r) {
                frm.set_value("fp", r.message || 0);
            }
        });



        //Closure
        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Closure",
                filters: {
                    custom_next_follow_up_on: frm.doc.dsm_date,
                    pp_original_at: "Candidate",
                }
            },
            callback: function(r) {
                frm.set_value("candidate_count", r.message || 0);
            }
        });
        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Closure",
                filters: {
                    custom_next_follow_up_on: frm.doc.dsm_date,
                    pp_original_at: "Agent",
                }
            },
            callback: function(r) {
                frm.set_value("agent", r.message || 0);
            }
        });
        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Closure",
                filters: {
                    custom_next_follow_up_on: frm.doc.dsm_date,
                    pp_original_at: "Supplier",
                }
            },
            callback: function(r) {
                frm.set_value("supplier", r.message || 0);
            }
        });
        frappe.call({
            method: "frappe.client.get_count",
            args: {
                doctype: "Closure",
                filters: {
                    custom_next_follow_up_on: frm.doc.dsm_date,
                    pp_original_at: "TEAMPRO",
                }
            },
            callback: function(r) {
                frm.set_value("internal", r.message || 0);
            }
        });
        
    }
}); 


// function fetch_all_todos(frm, start) {

//     let page_length = 200;

//     frappe.call({
//         method: "frappe.client.get_list",
//         args: {
//             doctype: "ToDo",
//             fields: ["name", "custom_subject", "status", "created_on"],
//             filters: {
//                 status: "Open"
//             },
//             order_by: "created_on desc",
//             limit_start: start,
//             limit_page_length: page_length
//         },
//         callback: function(r) {

//             if (r.message && r.message.length > 0) {

//                 r.message.forEach((row) => {

//                     let age = Math.floor(
//                         (new Date() - new Date(row.created_on)) / (1000 * 60 * 60 * 24)
//                     );

//                     let child = frm.add_child("todo_details");

//                     child.id = row.name;
//                     child.subject = row.custom_subject || "";
//                     child.current_status = row.status;
//                     child.age = age;
//                 });

//                 // frm.refresh_field("todo_details");
                

//                 // recursive call
//                 fetch_all_todos(frm, start + page_length);
//             }else {
//                 frm.dirty(false); 
//             }
//         }
//     });
    
// }

function opportunity_with_sf_details(frm, start) {

    let page_length = 200;

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Opportunity",
            fields: ["name", "status","opportunity_from","party_name"],
            filters: {
                transaction_date: frm.doc.dsm_date,
                "custom_sales_follow_up":["is","set"]
            },
            limit_start: start,
            limit_page_length: page_length
        },
        callback: function(r) {

            console.log("Opportunity Data:", r.message);

            if (r.message && r.message.length > 0) {

                r.message.forEach((row) => {

                    let child = frm.add_child("opportunity_with_sf");

                    child.id = row.name;
                    child.status = row.status || "";
                    child.opportunity_from = row.opportunity_from || "";
                    child.lead = row.party_name || "";
                });

                frm.refresh_field("opportunity_with_sf");
                

                opportunity_with_sf_details(frm, start + page_length);
            }else {
                frm.dirty(false); 
            }
        }
    });
}


frappe.ui.form.on('TODO Status', {
    id: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if(row.id){  
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "ToDo",
                    name: row.id
                },
                callback: function(r) {
                    if(r.message){
                        let created_date = new Date(r.message.created_on);
                        let today = new Date();

                        let diffTime = Math.abs(today - created_date);
                        let diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

                        row.age = diffDays; 
                    }
                }
            });
        }
    }
});


// frappe.ui.form.on('Daily Status Meeting - DSM', {

//     onload: function(frm) {

//         // Auto set employee
//         if (!frm.doc.employee) {
//             frappe.db.get_list('Employee', {
//                 filters: { user_id: frappe.session.user },
//                 fields: ['name'],
//                 limit_page_length: 1
//             }).then(r => {
//                 if (r.length) {
//                     frm.set_value('employee', r[0].name);
//                 }
//             });
//         }

//         // Call single backend method
//         if (frm.doc.dsm_date) {
//             frappe.call({
//                 method: "teampro.teampro.doctype.daily_status_meeting___dsm.daily_status_meeting___dsm.get_dsm_data",
//                 args: {
//                     dsm_date: frm.doc.dsm_date
//                 },
//                 callback: function(r) {
//                     if (r.message) {

//                         let data = r.message;

//                         // Sales Follow Up Counts
//                         frm.set_value("lead", data.lead);
//                         frm.set_value("open", data.open);
//                         frm.set_value("replied", data.replied);
//                         frm.set_value("opportunity", data.opportunity);
//                         frm.set_value("quotation", data.quotation);
//                         frm.set_value("lost_quotation", data.lost_quotation);
//                         frm.set_value("interested", data.interested);
//                         frm.set_value("converted", data.converted);
//                         frm.set_value("customer", data.customer);
//                         frm.set_value("do_not_contact", data.do_not_contact);

//                         // Project Counts
//                         frm.set_value("it", data.it);
//                         frm.set_value("rec", data.rec);
//                         frm.set_value("it_task", data.it_task);
//                         frm.set_value("rec_task", data.rec_task);

//                         // Candidate Counts
//                         frm.set_value("ip", data.ip);
//                         frm.set_value("fp", data.fp);

//                         // Closure
//                         frm.set_value("candidate_count", data.candidate);
//                         frm.set_value("agent", data.agent);
//                         frm.set_value("supplier", data.supplier);
//                         frm.set_value("internal", data.internal);

//                         // Opportunity child table
//                         frm.clear_table("opportunity_with_sf");

//                         data.opportunity_list.forEach(row => {
//                             let child = frm.add_child("opportunity_with_sf");
//                             child.id = row.name;
//                             child.status = row.status;
//                             child.opportunity_from = row.opportunity_from;
//                             child.lead = row.party_name;
//                         });

//                         frm.refresh_field("opportunity_with_sf");

//                         frm.dirty(false);
//                     }
//                 }
//             });
//         }
//     }
// });