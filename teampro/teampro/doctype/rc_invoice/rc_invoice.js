// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("RC Invoice", {
	refresh(frm) {
       
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
                window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
                    + "doctype=" + encodeURIComponent("RC Invoice")
                    + "&name=" + encodeURIComponent(f_name)
                    + "&trigger_print=1"
                    + "&format=" + print_format
                    + "&no_letterhead=0" 
                    + "&letterhead=" + encodeURIComponent(letter_head)
                  ));
            });
            frm.add_custom_button("Back", function() {
                frappe.set_route("List", "RC Invoice");
            });
        }
        if (frm.is_new()) return;

        frappe.call({
            method: "teampro.teampro.doctype.rc_invoice.rc_invoice.check_sales_invoice",
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
                        method: "teampro.teampro.doctype.rc_invoice.rc_invoice.create_sales_invoice_from_button",
                        args: { rc_invoice: frm.doc.name },
                        callback: function(r) {
                            if (r.message) {
                                // Show popup with invoice name
                                frappe.msgprint(r.message.message);

                                // Update outstanding details AFTER SI creation
                                frappe.call({
                                    method: "teampro.teampro.doctype.rc_invoice.rc_invoice.get_customer_pending_invoices",
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
                        method: "teampro.teampro.doctype.rc_invoice.rc_invoice.cancel_sales_invoice",
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
    customer(frm){
        if(frm.doc.customer){
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
            frappe.call({
                method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_transferred_items_with_qty",
                args: {
                    customer: frm.doc.customer,
                    customer_warehouse: frm.doc.customer_warehouse
                },
                callback: function(r) {
                    if(r.message && r.message.length > 0){
                        frm.clear_table("invoice_items"); 
                        r.message.forEach(item => {
                            let row = frm.add_child("invoice_items");
                            row.item_code = item.item_code;
                            row.item_name = item.item_name;
                            let default_uom = "";

                                if (item.item_code == "LL-SV-00002") {
                                    default_uom = "100gm";
                                }
                                else if (item.item_code == "LL-CH-00002") {
                                    default_uom = "80gm";
                                }
                                else if (item.item_code == "LL-CH-00033") {
                                    default_uom = "80gm";
                                }
                                else if (item.item_code == "LL-SV-00080") {
                                    default_uom = "100gm";
                                }
                                else if (item.item_code == "LL-SV-00114") {
                                    default_uom = "100gm";
                                }

                                row.uom = default_uom;
                                let pack_size = 0;

                                // set pack size
                                if (item.item_code == "LL-SV-00002") {
                                    pack_size = 100;
                                }
                                else if (item.item_code == "LL-CH-00002") {
                                    pack_size = 80;
                                }
                                else if (item.item_code == "LL-CH-00033") {
                                    pack_size = 80;
                                }
                                else if (item.item_code == "LL-SV-00080") {
                                    pack_size = 100;
                                }
                                else if (item.item_code == "LL-SV-00114") {
                                    pack_size = 100;
                                }

                                // convert kg → grams → packets
                                let total_grams = (item.qty || 0) * 1000;

                                let packets = 0;
                                if (pack_size > 0) {
                                    packets = total_grams / pack_size;
                                }
                                row.customer_qty = packets;
                                                            
                        });
                        frm.refresh_field("invoice_items");
                    }else {
                        frappe.msgprint("No items found for this customer and warehouse.");
                    }
                }
            });
        }
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
    customer_warehouse(frm){
            if(frm.doc.customer && frm.doc.customer_warehouse) {
                frappe.call({
                    method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_transferred_items_with_qty",
                    args: {
                        customer: frm.doc.customer,
                        customer_warehouse: frm.doc.customer_warehouse
                    },
                    callback: function(r) {
                        if(r.message) {
                            frm.clear_table("invoice_items"); 
                            r.message.forEach(item => {
                                let row = frm.add_child("invoice_items");
                                row.item_code = item.item_code;
                                row.item_name = item.item_name;
                                row.customer_qty = item.qty;
                                row.uom = item.uom;
                            });
                            frm.refresh_field("invoice_items");
                        }
                    }
                });
            }
    },
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
						method: "teampro.teampro.doctype.rc_invoice.rc_invoice.process_invoice",
						args: {
							docname: frm.doc.name
						},
						callback: function () {
							frappe.validated = true;
							frm.submit();
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
    // balance_available_qty(frm, cdt, cdn) {

    //     let row = locals[cdt][cdn];

    //     let customer_qty = flt(row.customer_qty);
    //     let balance_qty = flt(row.balance_available_qty);

    //     if (balance_qty > customer_qty) {
    //         frappe.throw("Balance Quantity must be less than Customer Quantity");
    //     }

    //     let billable = customer_qty - balance_qty;
    //     frappe.model.set_value(cdt, cdn, "billable_qty", billable);

    //     frappe.call({
    //         method: "teampro.teampro.doctype.rc_invoice.rc_invoice.get_latest_selling_price",
    //         args: {
    //             item_code: row.item_code,
    //             posting_date: frm.doc.delivered_date
    //         },
    //         callback: function(r) {
    //             if (r.message) {

    //                 let mrp = r.message;
    //                 frappe.model.set_value(cdt, cdn, "mrp_without_gst", mrp);

    //                 frappe.db.get_value("Shop RC", 
    //                     {customer_name: frm.doc.customer}, 
    //                     ["margin_percentage", "has_gst"]
    //                 ).then(res => {

    //                     let margin = res.message.margin_percentage || 0;
    //                     let gst_flag = res.message.has_gst;

    //                     frappe.model.set_value(cdt, cdn, "margin_percentage", margin);

    //                     let rate = mrp * (margin / 100);
    //                     frappe.model.set_value(cdt, cdn, "rate_without_gst", rate);

    //                     let amount = billable * rate;
    //                     frappe.model.set_value(cdt, cdn, "amount_without_gst", amount);

    //                     let total_billable = 0;
    //                     frm.doc.invoice_items.forEach(function(item) {
    //                         total_billable += item.amount_without_gst || 0;
    //                     });

    //                     frm.set_value("billable_amount", total_billable);

    //                     // ✅ CONDITION HERE
    //                     if (gst_flag) {
    //                         frappe.db.get_value("Item", row.item_code, "custom_gst_rate")
    //                     .then(item_res => {

    //                         let gst_rate = item_res.message.custom_gst_rate || 0;
    //                         let mrp_without_gst = row.mrp_without_gst || 0;
    //                         let rate_without_gst = row.rate_without_gst || 0;
    //                         let amount_without_gst = row.amount_without_gst ||0;

    //                         // GST amount
    //                         let gst_amount = mrp_without_gst + (gst_rate / 100);

    //                         let rate_gst = rate_without_gst + (gst_rate / 100);
    //                         let amount_gst = amount_without_gst + (gst_rate / 100);
    //                         // set field (create field if not exists)
    //                         frappe.model.set_value(
    //                             cdt,
    //                             cdn,
    //                             "gst",
    //                             gst_rate
    //                         );

    //                         frappe.model.set_value(
    //                             cdt,
    //                             cdn,
    //                             "mrp",
    //                             gst_amount
    //                         );
    //                         frappe.model.set_value(
    //                             cdt,
    //                             cdn,
    //                             "rate",
    //                             rate_gst
    //                         );
    //                         frappe.model.set_value(
    //                             cdt,
    //                             cdn,
    //                             "amount",
    //                             amount_gst
    //                         );
    //                         let total_gst = 0;

    //                         frm.doc.invoice_items.forEach(function(item) {
    //                             total_gst += item.gst || 0;
    //                         });

    //                         // ✅ set to main doctype field
    //                         frm.set_value("vat_amount", total_gst);

    //                         // total amount
    //                         frm.set_value("total_amount", total_billable + total_gst);


                            
    //                     });

    //                     } else {
    //                         let rate = mrp * (margin / 100);
    //                         let amount = billable * rate;
    //                         frappe.model.set_value(cdt, cdn, "rate", rate);
    //                         frappe.model.set_value(cdt, cdn, "amount", amount);
    //                         frappe.model.set_value(cdt, cdn, "mrp", mrp);
    //                         frm.set_value("total_amount", total_billable);
    //                     }

    //                 });
    //             }
    //         }
    //     });

    balance_available_qty: function(frm, cdt, cdn) {

        let row = locals[cdt][cdn];


        if (row.balance_available_qty > row.customer_qty) {
            frappe.throw("Balance Quantity must be less than Customer Quantity");
        }

        frappe.call({
            method: "teampro.teampro.doctype.rc_invoice.rc_invoice.calculate_row_values",
            args: {
                item_code: row.item_code,
                customer_qty: row.customer_qty,
                balance_available_qty: row.balance_available_qty,
                customer: frm.doc.customer,
                delivered_date: frm.doc.delivered_date
            },
            callback: function(r) {
                if (r.message) {

                    let d = r.message;


                    frappe.model.set_value(cdt, cdn, "billable_qty", d.billable_qty);
                    frappe.model.set_value(cdt, cdn, "mrp", d.mrp);
                    frappe.model.set_value(cdt, cdn, "rate", d.rate);
                    frappe.model.set_value(cdt, cdn, "amount", d.amount);

                    if (d.gst_flag) {
                        frappe.model.set_value(cdt, cdn, "gst", d.gst);
                        frappe.model.set_value(cdt, cdn, "rate_without_gst", d.rate_without_gst);
                        frappe.model.set_value(cdt, cdn, "amount_without_gst", d.amount_without_gst);
                        frappe.model.set_value(cdt, cdn, "mrp_without_gst", d.mrp_without_gst);
                    }


                    frm.set_value("billable_amount", d.total_billable);
                    frm.set_value("vat_amount", d.vat_amount);
                    frm.set_value("total_amount", d.total_amount);
                }
            }
        });
    }
        // frappe.call({
        //     method: "teampro.teampro.doctype.rc_invoice.rc_invoice.get_latest_selling_price",
        //     args: {
        //         item_code: row.item_code,
        //         posting_date: frm.doc.delivered_date
        //     },
        //     callback: function(r) {
        //         if (r.message) {

        //             let mrp = r.message;
        //             frappe.model.set_value(cdt, cdn, "mrp_without_gstmrp", mrp);

        //             frappe.db.get_value("Shop RC", {customer_name: frm.doc.customer}, "margin_percentage")
                    
        //                 .then(res => {

        //                     let margin = res.message.margin_percentage || 0;
        //                     frappe.model.set_value(cdt, cdn,"margin_percentage",margin);

        //                     // Calculate Rate
        //                     let margin_value = margin/100;
        //                     let rate = mrp * margin_value;
        //                     frappe.model.set_value(cdt, cdn, "rate_without_gst", rate);

        //                     let amount = billable * rate;
        //                     frappe.model.set_value(cdt, cdn, "amount_without_gst", amount);

        //                     let total_billable = 0;

        //                     frm.doc.invoice_items.forEach(function(item) {
        //                         total_billable += item.amount || 0;
        //                     });

        //                     frm.set_value("billable_amount", total_billable);

        //                     let vat_amount = total_billable * 0.18;
        //                     frm.set_value("vat_amount", vat_amount);

        //                     frm.set_value("total_amount", total_billable + vat_amount);
        //                 });
        //         }
        //     }
        // });
    
});


function load_outstanding(frm){

    if (!frm.doc.customer) return;

    frappe.call({
        method: "teampro.teampro.doctype.rc_invoice.rc_invoice.get_customer_pending_invoices",
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