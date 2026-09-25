frappe.ui.form.on('Customer', {
    onload(frm){
        if (frm.doc.__islocal && frm.doc.lead_name && frm.doc.customer_name){
                frappe.call({
	            method:"teampro.project_updates.create_cust",
	            args:{
	                name:frm.doc.customer_name,
	            },
	            callback(){
	                
	            }
	        })
        }
        
    },
    territory(frm) {

        if (!frm.doc.__islocal && frm.doc.territory) {
    
            frappe.call({
                method: "teampro.project_updates.update_territory_sfp",
                args: {
                    name: frm.doc.name,
                    territory: frm.doc.territory
                },
                freeze: true,
                callback: function (r) {
                    frm.refresh_field("territory");
                }
            });
    
        }
    
    },
    account_manager(frm){
        if(frm.doc.account_manager){
            frappe.call({
                method:"teampro.teampro.doctype.sales_follow_up.sales_follow_up.update_acc_manager",
                args:{
	                name:frm.doc.name,
	                account_manager:frm.doc.account_manager
	            },
	            callback(){
	                
	            }
	            
            })
        }
    },
    validate: function(frm) {
        let today = frappe.datetime.get_today();

        if (frm.doc.custom_sla_details && frm.doc.custom_sla_details.length > 0) {
            frm.doc.custom_sla_details.forEach(row => {
                if (row.sla_to_date && row.sla_to_date < today) {
                    row.status = "Expired";
                }
            });
        }
    },
    customer_group(frm){
        if(frm.doc.customer_group=="Individual"){
            frm.set_value("market_segment","RETAIL")
        }
    },
	refresh(frm) {
	   if (frm.doc.custom_sfp_created == 1) {
            const btn = frm.add_custom_button("SFP Created", () => {});
            btn.removeClass("btn-default");
            btn.addClass("btn-success");
        }

    frm.set_query("account_manager", function() {
			return{
				"filters": {
					"enabled":1,
				}
			};
		});
		frm.set_query("location", function() {
			return{
				"filters": {
					"custom_territory":frm.doc.territory,
				}
			};
		});
	    frm.fields_dict['custom_sla_details'].grid.get_field('project').get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    customer: frm.doc.name // Filter projects by the selected customer
                }
            };
        };
    
	if (!frm.doc.__islocal){
           frm.add_custom_button(__("Follow Up"), function () {
        var sfu = frappe.model.make_new_doc_and_get_name('Sales Follow Up');
            sfu = locals['Sales Follow Up'][sfu];
            sfu.party_from = "Customer"
            sfu.status = "Converted"
            sfu.party_name = frm.doc.name
            sfu.sfp_territory=frm.doc.territory
            sfu.account_manager_lead_owner=frm.doc.account_manager
            sfu.service=frm.doc.service
            frappe.set_route("Form", "Sales Follow Up",sfu.name)
       
           },__("Create"))
           frm.add_custom_button(__("Appointment"), function () {
                var app = frappe.model.make_new_doc_and_get_name('Appointment');
                app = locals['Appointment'][app];
                app.customer_name = frm.doc.customer_name
                app.appointment_with = 'Customer'
                app.party = frm.doc.name
                app.status = "Open" 
                app.customer_phone_number = frm.doc.contact_mobile
                app.customer_email = frm.doc.contact_email
                app.custom_appointment_from = 'Customer'
                frappe.set_route("Form", "Appointment",app.name)
            },'Create');

        // --- Statement of Account button ---
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("Statement"), function() {
                var party = frm.doc.name;
                var company = frappe.defaults.get_user_default("Company");
                frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Fiscal Year",
                        filters: { disabled: 0, year_start_date: ["<=", frappe.datetime.get_today()], year_end_date: [">=", frappe.datetime.get_today()] },
                        fieldname: "year_start_date, year_end_date",
                    },
                    callback: function(r) {
                        var fy_start = r && r.message && r.message.year_start_date ? r.message.year_start_date : frappe.datetime.add_months(frappe.datetime.get_today(), -12);
                        var fy_end = r && r.message && r.message.year_end_date ? r.message.year_end_date : frappe.datetime.get_today();
                        var d = new frappe.ui.Dialog({
                            title: __("Statement of Account"),
                            fields: [
                                { label: __("Company"), fieldname: "company", fieldtype: "Link", options: "Company", default: company, reqd: 1 },
                                { label: __("From Date"), fieldname: "from_date", fieldtype: "Date", default: fy_start, reqd: 1 },
                                { label: __("To Date"), fieldname: "to_date", fieldtype: "Date", default: fy_end, reqd: 1 },
                            ],
                            primary_action_label: __("Download PDF"),
                            primary_action: function() {
                                var values = d.get_values();
                                if (!values) return;
                                d.hide();
                                var url = "/api/method/teampro.utility.download_party_statement_pdf"
                                    + "?party_type=Customer"
                                    + "&party=" + encodeURIComponent(party)
                                    + "&from_date=" + encodeURIComponent(values.from_date)
                                    + "&to_date=" + encodeURIComponent(values.to_date)
                                    + "&company=" + encodeURIComponent(values.company);
                                window.open(url, "_blank");
                            },
                            secondary_action_label: __("View Statement"),
                            secondary_action: function() {
                                var values = d.get_values();
                                if (!values) return;
                                d.hide();
                                frappe.call({
                                    method: "teampro.utility.get_party_statement",
                                    args: {
                                        party_type: "Customer",
                                        party: party,
                                        from_date: values.from_date,
                                        to_date: values.to_date,
                                        company: values.company,
                                    },
                                    freeze: true,
                                    freeze_message: __("Generating Statement..."),
                                    callback: function(r) {
                                        if (r && r.message && r.message.html) {
                                            var w = window.open("", "_blank");
                                            w.document.write(r.message.html);
                                            w.document.close();
                                        }
                                    }
                                });
                            }
                        });
                        d.show();
                        // Add Excel download button
                        $(d.footer).find('.btn-secondary').before(
                            '<button class="btn btn-default btn-sm btn-excel" style="margin-right: 5px;">Download Excel</button>'
                        );
                        $(d.footer).find('.btn-excel').on('click', function() {
                            var values = d.get_values();
                            if (!values) return;
                            d.hide();
                            var url = "/api/method/teampro.utility.download_party_statement_excel"
                                + "?party_type=Customer"
                                + "&party=" + encodeURIComponent(party)
                                + "&from_date=" + encodeURIComponent(values.from_date)
                                + "&to_date=" + encodeURIComponent(values.to_date)
                                + "&company=" + encodeURIComponent(values.company);
                            window.open(url, "_blank");
                        });
                    }
                });
            }, __("View"));
        }
        // --- End Statement button ---
        }
      
	},
	disabled(frm){
	    if(frm.doc.disabled==1){
	        frappe.call({
	            method:"teampro.project_updates.update_dnc",
	            args:{
	                name:frm.doc.name,
	            },
	            callback(){
	                
	            }
	        })
	    }
	     if(frm.doc.disabled==0){
	        frappe.call({
	            method:"teampro.project_updates.update_dnc_converted",
	            args:{
	                name:frm.doc.name,
	            },
	            callback(){
	                
	            }
	        })
	    }
	}
	
})


frappe.ui.form.on('SLA Details', {
    renew(frm, cdt, cdn) {
        let d = new frappe.ui.Dialog({
            title: 'Renew SLA Details',
            fields: [
                {
                    label: 'Service',
                    fieldname: 'service',
                    fieldtype: 'Link',
                    options: 'Services',
                    reqd:1
                },
                {
                    label: 'SLA From Date',
                    fieldname: 'from_date',
                    fieldtype: 'Date',
                    reqd:1
                },
                {
                    label: 'SLA To Date',
                    fieldname: 'to_date',
                    fieldtype: 'Date',
                    reqd:1
                },
                {
                    label: 'SLA Type',
                    fieldname: 'type',
                    fieldtype: 'Select',
                    options: 'AMC\nREC\nAgreement\nSoftware License\nSLA\nPO',
                    reqd:1
                },
                {
                    label: 'Status',
                    fieldname: 'status',
                    fieldtype: 'Select',
                    options: 'Active\nExpired',
                    reqd:1
                },
                {
                    label: 'Attach',
                    fieldname: 'attach',
                    fieldtype: 'Attach',
                    reqd:1
                },
            ],
            primary_action_label: 'Submit',
            primary_action() {
                d.hide();
                let values = d.get_values();
                
                if(values.service && values.from_date && values.to_date && values.status && values.attach){
                    frappe.call({
                        method: 'teampro.project_updates.update_sla_details',
                        args: {
                            name: frm.doc.name,
                            service: values.service,
                            sla_from_date: values.from_date,
                            sla_to_date: values.to_date,
                            sla_type: values.type,
                            status: values.status,
                            attach:values.attach,
                        },
                        callback: function (r) {
                            if (r.message && r.message.status === "success") {
                                frm.reload_doc();
                                frappe.show_alert({
                                    message: r.message.message,
                                    indicator: "green"
                                });
                            } else {
                                frappe.msgprint({
                                    title: __('Error'),
                                    indicator: 'red',
                                    message: r.message.message || __('Something went wrong')
                                });
                            }
                        }
                    });
                }
                    
                }
        });
        d.show();
    }
});
