// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt

// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("RS Invoice", {
    validate(frm) {

        frappe.db.get_value("Shop RC",{ customer_name: frm.doc.customer },["contact_person_number", "postal_code"]).then(r => {
            if (r.message) {
                setTimeout(() => {
                    if (!frm.doc.custom_contact_number_) {
                        frm.set_value("custom_contact_number_",r.message.contact_person_number || "");
                    }
                    if (!frm.doc.custom_pin_code_) {
                        frm.set_value("custom_pin_code_",r.message.postal_code || "");
                    }
                }, 500);
            }
        });
    },
	refresh(frm) {
       frm.set_query("bank", function() {
            return {
                filters: {
                    company: "TEAMPRO Food Products"  
                }
            };
        });
        frm.set_query("customer", function() {
            return {
                filters: {
                    custom_is_retail_customer: 1  
                }
            };
        });
        frm.set_query("dispatch_warehouse", function() {
            return {
                filters: {
                    custom_dispatch_warehouse: 1  
                }
            };
        });
        if(frm.doc.is_return == 0 && frm.doc.docstatus !=2 && !frm.doc.__islocal){
            // frm.add_custom_button("Return", function() {
            //     frappe.call({
            //         method: "teampro.teampro.doctype.rc_invoice.rc_invoice.create_return_invoice",
            //         args: { original_invoice_name: frm.doc.name },
            //         callback: function(r) {
            //             if(r.message) {
            //                 frappe.set_route("Form", "RC Invoice", r.message);
            //             }
            //         }
            //     });
            // });
            frm.add_custom_button("Print Preview", function() {
                var f_name = frm.doc.name
                var letter_head = frm.doc.letter_head
                var print_format ="RC Invoice"
                // window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
                //     + "doctype=" + encodeURIComponent("RS Invoice")
                //     + "&name=" + encodeURIComponent(f_name)
                //     + "&trigger_print=1"
                //     + "&format=" + print_format
                //     + "&no_letterhead=0" 
                //     + "&letterhead=" + encodeURIComponent(letter_head)
                //   ));
                // let url = "/api/method/frappe.utils.print_format.download_pdf?"
                //     + "doctype=" + encodeURIComponent("RS Invoice")
                //     + "&name=" + encodeURIComponent(f_name)
                //     + "&format=" + encodeURIComponent(print_format)
                //     + "&no_letterhead=0"
                //     + "&letterhead=" + encodeURIComponent(letter_head)
                //     + "&trigger_print=1";

                window.open(`https://erp.teamproit.com/printview?doctype=RS%20Invoice&name=${frm.doc.name}&format=RS%20Invoice&no_letterhead=0&letterhead=TFP`);
                 
            });
            frm.add_custom_button("Back", function() {
                frappe.set_route("List", "RS Invoice");
            });
        }
        if (frm.is_new()) return;

        frappe.call({
            method: "teampro.teampro.doctype.rs_invoice.rs_invoice.check_sales_invoice",
            args: {
                rc_invoice: frm.doc.name
            },
            callback: function(r) {

                let html = "";

                if (frm.doc.docstatus === 1) {
                    if (r.message) {
                        html = `<button class="btn btn-danger cancel-si">Cancel Sales Invoice</button>`;
                    } else {
                        html = "";
                    }
                } else {
                    html = r.message
                        ? `<button class="btn btn-danger cancel-si">Cancel Sales Invoice</button>`
                        : `<button class="btn btn-primary create-si">Create Sales Invoice</button>`;
            }

                frm.fields_dict.invoice_action.$wrapper.html(html);

                // $(".create-si").click(function() {

                //     frappe.call({
                //         method: "teampro.teampro.doctype.rc_invoice.rc_invoice.create_sales_invoice_from_button",
                //         args: {
                //             rc_invoice: frm.doc.name
                //         },
                //         callback: function(r) {

                //             frappe.msgprint("Sales Invoice Created & Submitted");
                //             load_outstanding(frm);
                //             frm.save().then(() => {
                //                 frm.reload_doc(); // optional, ensures form is fully synced
                //             });
                                        

                //         }
                //     });

                // });

                $(".create-si").click(function() {
                    if (!frm.doc.customer_signature_) {
                        frappe.throw("Please upload Signature before creating Sales Invoice");
                    }

                    frappe.call({
                        method: "teampro.teampro.doctype.rs_invoice.rs_invoice.create_sales_invoice_from_button",
                        args: { rc_invoice: frm.doc.name },
                        callback: function(r) {
                            if (r.message) {
                                // Show popup with invoice name
                                frappe.msgprint(r.message.message);

                                // Update outstanding details AFTER SI creation
                                frappe.call({
                                    method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_customer_pending_invoices",
                                    args: { customer: frm.doc.customer },
                                    callback: function(res) {

                                        // Clear existing outstanding table
                                        frm.clear_table("outstanding");

                                        let total_outstanding = 0;

                                        if (res.message) {
                                            res.message.forEach(inv => {
                                                let row = frm.add_child("outstanding");
                                                row.invoice = inv.invoice;
                                                row.outstanding_amount = inv.outstanding_amount;
                                                total_outstanding += inv.outstanding_amount;
                                            });
                                        }

                                        // Update total outstanding field
                                        frm.set_value("outstanding_amount", total_outstanding);

                                        // Refresh the table and field
                                        frm.refresh_field("outstanding");
                                        frm.refresh_field("outstanding_amount");

                                        // Save the RC Invoice after updating outstanding
                                        frm.save(); 
                                    }
                                });
                            }
                        }
                    });
                });
                $(".cancel-si").click(function() {

                    frappe.call({
                        method: "teampro.teampro.doctype.rs_invoice.rs_invoice.cancel_sales_invoice",
                        args: {
                            rc_invoice: frm.doc.name
                        },
                        callback: function() {

                            frappe.msgprint("Sales Invoice Cancelled");
                            frm.reload_doc();
                            setTimeout(function(){
                                load_outstanding(frm);
                            },800);
                            frm.trigger("refresh");

                        }
                    });

                });

            }
        });

	}, 
    after_insert: function(frm) {

        if (frm.doc.invoice_items && frm.doc.invoice_items.length > 0) {
            return; 
        }

        if (frm.doc.customer && frm.doc.customer_warehouse) {

            setTimeout(function () {
                frappe.call({
                    // method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_transferred_items_with_qty",
                    method: "teampro.teampro.doctype.rs_invoice.rs_invoice.transferred_items_with_qty",
                    args: {
                        customer: frm.doc.customer,
                        customer_warehouse: frm.doc.customer_warehouse
                    },
                    freeze: true,
                    freeze_message: "Loading Data.....",
                    callback: function (r) {
                        if (r.message && r.message.length > 0) {

                            frm.clear_table("invoice_items");

                            r.message.forEach(item => {
                                let row = frm.add_child("invoice_items");
                                row.item_code = item.item_code;
                                row.item_name = item.item_name;
                                row.uom = item.uom;
                                row.customer_qty = item.customer_qty;
                            });

                            frm.refresh_field("invoice_items");
                        } else {
                            frappe.msgprint("No items found for this customer and warehouse.");
                        }
                    }
                });
            }, 200);
        }
    },
    customer(frm){
        if(frm.doc.customer){
            frappe.db.get_value(
                    "Shop RC",
                    { customer_name: frm.doc.customer },
                    ["contact_person_number", "postal_code"]
                ).then(r => {

                    if (r.message) {

                        if (r.message.contact_person_number) {
                            frm.set_value("custom_contact_number_", r.message.contact_person_number);
                        }

                        if (r.message.postal_code) {
                            frm.set_value("custom_pin_code_", r.message.postal_code);
                        }

                    }

                });
            frappe.db.get_value("Customer", frm.doc.customer, "custom_retail_customer")
                .then(r => {

                    if (r.message.custom_retail_customer) {

                        let retail_id = r.message.custom_retail_customer;
                        frappe.db.get_value("Warehouse",
                            { custom_retail_customer: retail_id },
                            "name"
                        ).then(res => {

                            if (res.message.name) {
                                frm.set_value("customer_warehouse", res.message.name);
                            } else {
                                frm.set_value("customer_warehouse", "");
                                frappe.msgprint("Warehouse not found for this Retail Customer");
                            }

                        });

                    } else {
                        frm.set_value("customer_warehouse", "");
                    }

                });
        }
        if(frm.doc.customer && frm.doc.customer_warehouse) {
            setTimeout(function() {
            frappe.call({
                // method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_transferred_items_with_qty",
                method: "teampro.teampro.doctype.rs_invoice.rs_invoice.transferred_items_with_qty",
                args: {
                    customer: frm.doc.customer,
                    customer_warehouse: frm.doc.customer_warehouse
                },
                freeze: true,
                freeze_message: "Loading Data.....",
                callback: function(r) {
                    if(r.message && r.message.length > 0){
                        console.log(r.message);
                        frm.clear_table("invoice_items");  

                        r.message.forEach(item => {
                            let row = frm.add_child("invoice_items");
                            row.item_code = item.item_code;
                            row.item_name = item.item_name;
                            row.uom = item.uom;
                            row.customer_qty = item.customer_qty;
                        });  

                        frm.refresh_field("invoice_items");
                    } else {
                        frappe.msgprint("No items found for this customer and warehouse.");
                    }
                }
            });
        }, 200);
    }
        // if(frm.doc.customer && frm.doc.customer_warehouse) {
        //     frappe.call({
        //         method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_transferred_items",
        //         args: {
        //             customer: frm.doc.customer,
        //             customer_warehouse: frm.doc.customer_warehouse
        //         },
        //         callback: function(r) {
        //             if(r.message && r.message.length > 0){
        //                 frm.clear_table("invoice_items"); 
        //                 r.message.forEach(item => {
        //                     let row = frm.add_child("invoice_items");
                            
        //                     let default_uom = "";

        //                         if (item.item_code == "LL-SV-00002") {
        //                             default_uom = "100gm";
        //                         }
        //                         else if (item.item_code == "LL-CH-00002") {
        //                             default_uom = "80gm";
        //                         }
        //                         else if (item.item_code == "LL-CH-00033") {
        //                             default_uom = "80gm";
        //                         }
        //                         else if (item.item_code == "LL-SV-00080") {
        //                             default_uom = "100gm";
        //                         }
        //                         else if (item.item_code == "LL-SV-00114") {
        //                             default_uom = "100gm";
        //                         }

                                
        //                         let pack_size = 0;

        //                         // set pack size
        //                         if (item.item_code == "LL-SV-00002") {
        //                             pack_size = 100;
        //                         }
        //                         else if (item.item_code == "LL-CH-00002") {
        //                             pack_size = 80;
        //                         }
        //                         else if (item.item_code == "LL-CH-00033") {
        //                             pack_size = 80;
        //                         }
        //                         else if (item.item_code == "LL-SV-00080") {
        //                             pack_size = 100;
        //                         }
        //                         else if (item.item_code == "LL-SV-00114") {
        //                             pack_size = 100;
        //                         }

        //                         // convert kg → grams → packets
        //                         let total_grams = (item.qty || 0) * 1000;

        //                         let packets = 0;
        //                         if (pack_size > 0) {
        //                             packets = total_grams / pack_size;
        //                         }
        //                         row.item_code = item.item_code;
        //                         row.item_name = item.item_name;
        //                         row.customer_qty = packets;
        //                         row.uom = default_uom;
                                                            
        //                 });
        //                 frm.refresh_field("invoice_items");
        //             }else {
        //                 frappe.msgprint("No items found for this customer and warehouse.");
        //             }
        //         }
        //     });
        // }
        if(frm.doc.customer){
            frappe.db.get_value("Shop RC",
                {customer_name: frm.doc.customer},
                "name",
                function(r){
                    if(r.name){
                        frm.set_value("rc_customer", r.name);
                    }
                }
            );
        }
        load_outstanding(frm);
    },
    // delivered_date(frm){
    //     if(frm.doc.customer && frm.doc.customer_warehouse) {
    //         frappe.call({
    //             method: "teampro.teampro.doctype.rc_invoice.rc_invoice.get_transferred_items",
    //             args: {
    //                 customer: frm.doc.customer,
    //                 customer_warehouse: frm.doc.customer_warehouse
    //             },
    //             callback: function(r) {
    //                 if(r.message) {
    //                     frm.clear_table("invoice_items"); 
    //                     r.message.forEach(item => {
    //                         let row = frm.add_child("invoice_items");
    //                         row.item_code = item.item_code;
    //                         row.item_name = item.item_name;
    //                         row.customer_qty = item.qty;
    //                         row.uom = item.uom;
    //                     });
    //                     frm.refresh_field("invoice_items");
    //                 }
    //             }
    //         });
    //     }
    // },
    // customer_warehouse(frm){
    //         if(frm.doc.customer && frm.doc.customer_warehouse) {
    //             frappe.call({
    //                 method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_transferred_items_with_qty",
    //                 args: {
    //                     customer: frm.doc.customer,
    //                     customer_warehouse: frm.doc.customer_warehouse
    //                 },
    //                 callback: function(r) {
    //                     if(r.message) {
    //                         frm.clear_table("invoice_items"); 
    //                         r.message.forEach(item => {
    //                             let row = frm.add_child("invoice_items");
    //                             row.item_code = item.item_code;
    //                             row.item_name = item.item_name;
    //                             row.customer_qty = item.qty;
    //                             row.uom = item.uom;
    //                         });
    //                         frm.refresh_field("invoice_items");
    //                     }
    //                 }
    //             });
    //         }
    // },
    // dispatch_warehouse(frm){
    //         if(frm.doc.customer && frm.doc.customer_warehouse) {
    //             frappe.call({
    //                 method: "teampro.teampro.doctype.rc_invoice.rc_invoice.get_transferred_items",
    //                 args: {
    //                     customer: frm.doc.customer,
    //                     customer_warehouse: frm.doc.customer_warehouse
    //                 },
    //                 callback: function(r) {
    //                     if(r.message) {
    //                         frm.clear_table("invoice_items"); 
    //                         r.message.forEach(item => {
    //                             let row = frm.add_child("invoice_items");
    //                             row.item_code = item.item_code;
    //                             row.item_name = item.item_name;
    //                             row.customer_qty = item.qty;
    //                             row.uom = item.uom;
    //                         });
    //                         frm.refresh_field("invoice_items");
    //                     }
    //                 }
    //             });
    //         }
    // },
    before_submit(frm) {

		let paid_amount = frm.doc.paid_amount || 0;
		let has_payable = false;

		(frm.doc.outstanding || []).forEach(row => {
			if (row.payable_amount && row.payable_amount > 0) {
				has_payable = true;
			}
		});

		if (paid_amount == 0 && !has_payable) {

			frappe.validated = false;  

			frappe.confirm(
				"No Paid Amount and No Payable Amount. Do you want to continue without payment?",
				function () {

					frappe.call({
						method: "teampro.teampro.doctype.rs_invoice.rs_invoice.process_invoice",
						args: {
							docname: frm.doc.name
						},
						callback: function () {
							frappe.validated = true;
							// frm.submit();
                            frm.save("Submit");
						}
					});
				}
			);
		}
	},
    paid_amount(frm) {

        let remaining_payment = frm.doc.paid_amount || 0;

        frm.doc.outstanding.forEach(function(row) {

            if (remaining_payment <= 0) {
                row.payable_amount = 0;
            } else {

                if (remaining_payment >= row.outstanding_amount) {
                    row.payable_amount = row.outstanding_amount;
                    remaining_payment -= row.outstanding_amount;
                } else {
                    row.payable_amount = remaining_payment;
                    remaining_payment = 0;
                }
            }
        });

        frm.refresh_field("outstanding");
        
    }
    
});


frappe.ui.form.on('RC Invoice Items', {
    balance_available_qty(frm, cdt, cdn) {

        let row = locals[cdt][cdn];

        let customer_qty = flt(row.customer_qty);
        let balance_qty = flt(row.balance_available_qty);

        if (balance_qty > customer_qty) {
            frappe.throw("Balance Quantity must be less than Customer Quantity");
        }

        let billable = customer_qty - balance_qty;
        frappe.model.set_value(cdt, cdn, "billable_qty", billable);

        frappe.call({
            method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_latest_selling_price",
            args: {
                item_code: row.item_code,
                uom:row.uom,
                posting_date: frm.doc.delivered_date
                
            },
            callback: function(r) {
                if (r.message) {

                    let mrp = r.message;
                    frappe.model.set_value(cdt, cdn, "mrp", mrp);

                    frappe.db.get_value("Shop RC", 
                        {customer_name: frm.doc.customer}, 
                        ["margin_percentage", "has_gst"]
                    ).then(res => {

                        let margin = res.message.margin_percentage || 0;
                         if (row.item_code === "LL-GI-00053") {
                            margin = 20;
                        }
                        let gst_flag = res.message.has_gst;

                        frappe.model.set_value(cdt, cdn, "margin_percentage", margin);

                        let rate = mrp * (margin / 100);
                        let total_rate = mrp - rate
                        frappe.model.set_value(cdt, cdn, "rate", total_rate);

                        let amount = billable * total_rate;
                        frappe.model.set_value(cdt, cdn, "amount", amount);

                        let total_billable = 0;
                        frm.doc.invoice_items.forEach(function(item) {
                            total_billable += item.amount || 0;
                        });

                        frm.set_value("billable_amount", total_billable);

                        if (gst_flag) {
                            frappe.db.get_value("Item", row.item_code, "custom_gst_rate")
                        .then(item_res => {

                            let gst_rate = item_res.message.custom_gst_rate || 0;
                            let mrp_without_gst = row.mrp || 0;
                            let rate_without_gst = row.rate || 0;
                            let shop_qty = row.customer_qty || 0;
                            let amount_without_gst = row.amount ||0;


                            let gst_value = gst_rate / 100;
                            let gst_rate_total = gst_value * mrp_without_gst
                            let mrp_gst = mrp_without_gst - gst_rate_total;


                            let rate = mrp_gst * (margin / 100);
                            let total_rate = mrp_gst - rate

                            let rate_gst = rate_without_gst + gst_rate_total;
                            console.log(rate_without_gst);
                            


                            let amount_gst = total_rate * billable;

                            // set values
                            frappe.model.set_value(cdt, cdn, "gst", gst_rate_total);
                            frappe.model.set_value(cdt, cdn, "rate_without_gst", total_rate);
                            frappe.model.set_value(cdt, cdn, "amount_without_gst", amount_gst);
                            frappe.model.set_value(cdt, cdn, "mrp_without_gst", mrp_gst);


                            
                            let vat_amount = 0;

                            frm.doc.invoice_items.forEach(function(item) {
                                let amt_wo_gst = flt(item.amount_without_gst || 0);
                                let amt = flt(item.amount || 0);

                                vat_amount += (amt - amt_wo_gst);  
                            });

                            // Sum of amount_without_gst
                            let total_billable = 0;
                            frm.doc.invoice_items.forEach(function(item) {
                                total_billable += flt(item.amount_without_gst || 0);
                            });

                            // Set values in main doc
                            frm.set_value("billable_amount", flt(total_billable, 2));
                            frm.set_value("vat_amount", flt(vat_amount, 2));
                            frm.set_value("total_amount", flt(total_billable + vat_amount, 2));

                            
                        });

                        } else {
                            let rate = mrp * (margin / 100);
                            let total_rate = mrp_without_gst - rate
                            let amount = billable * rate;
                            frappe.model.set_value(cdt, cdn, "rate", rate);
                            frappe.model.set_value(cdt, cdn, "amount", amount);
                            frappe.model.set_value(cdt, cdn, "mrp", mrp);
                            frm.set_value("total_amount", total_billable);
                            
                            let total_billable = 0;
                            frm.doc.invoice_items.forEach(function(item) {
                                total_billable += flt(item.amount || 0);
                            });
                            console.log(total_billable)
                            // Set values in main doc
                            frm.set_value("total_amount", total_billable);
                        }

                    });
                }
            }
        });
        
    },
    
});


function load_outstanding(frm){

    if (!frm.doc.customer) return;

    frappe.call({
        method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_customer_pending_invoices",
        args: {
            customer: frm.doc.customer
        },
        callback: function(r) {

            frm.clear_table("outstanding");

            let total_outstanding = 0;

            if (r.message) {

                r.message.forEach(inv => {

                    let row = frm.add_child("outstanding");

                    row.invoice = inv.invoice;
                    row.outstanding_amount = inv.outstanding_amount;

                    total_outstanding += inv.outstanding_amount;

                });

            }

            frm.refresh_field("outstanding");

            frm.doc.outstanding_amount = total_outstanding;
            frm.refresh_field("outstanding_amount");

        }
    });

}