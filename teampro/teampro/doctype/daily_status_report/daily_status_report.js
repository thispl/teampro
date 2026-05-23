// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Status Report", {
	view(frm) {
        frappe.call({
            method:"teampro.teampro.doctype.daily_status_report.daily_status_report.view_proj_details",
            args:{
                'project':frm.doc.project
            },
            callback(r){
                if (r.message) {
                    let d = new frappe.ui.Dialog({
                        title: "Project Task Details",
                        size: "large",  
                        primary_action_label: "Close",
                        primary_action() {
                            d.hide();
                        }
                    });

                    d.$body.html(r.message);

                    d.show();
                }
            }
        })
	},
    get_dsr(frm) {
        if(frm.doc.allocated_to){
        frappe.call({
            method:"teampro.teampro.doctype.daily_status_report.daily_status_report.get_data",
            args:{
                'user':frm.doc.allocated_to || frappe.session.User
            },
            callback(r){
                if (r.message) {
                    let d = new frappe.ui.Dialog({
                        title: "Task Details",
                        size: "large",  
                        primary_action_label: "Close",
                        primary_action() {
                            d.hide();
                        }
                    });

                    d.$body.html(r.message);

                    d.show();
                }
            }
        })
    }
	},
});
