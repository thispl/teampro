// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("RS Delivery", {
    validate: async function(frm) {

            let r = await frappe.db.get_value(
                "Shop RC",
                { customer_name: frm.doc.customer },
                ["contact_person_number", "postal_code"]
            );

            if (r.message) {
                if (!frm.doc.custom_contact_number) {
                    frm.set_value("custom_contact_number", r.message.contact_person_number || "");
                }
                if (!frm.doc.custom_pin_code_) {
                    frm.set_value("custom_pin_code_", r.message.postal_code || "");
                }
            }

            for (let row of (frm.doc.items || [])) {
                await new Promise(resolve => {
                    frappe.ui.form.trigger('Stock Movement Items', 'qty', frm, row.doctype, row.name);
                    setTimeout(resolve, 300);
                });
            }
        },
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
                    "parent_warehouse": "Dispatch Warehouse - TFP" 
                }
            };
        });
        frm.add_custom_button("Back", function() {
                frappe.set_route("List", "RS Delivery");
        });
	},
    customer: function(frm) {
        if (frm.doc.customer) {
            frappe.db.get_value("Shop RC",{ customer_name: frm.doc.customer },["contact_person_number", "postal_code"]).then(r => {
                if (r.message) {
                    setTimeout(() => {
                        if (!frm.doc.custom_contact_number) {
                            frm.set_value("custom_contact_number",r.message.contact_person_number || "");
                        }
                        if (!frm.doc.custom_pin_code_) {
                            frm.set_value("custom_pin_code_",r.message.postal_code || "");
                        }
                    }, 500);
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
            
            frm.clear_table("items");
        //     frappe.call({
        //     method: "frappe.client.get_list",
        //     args: {
        //         doctype: "Item",
        //         filters: {
        //             custom_is_retail_item: 1
        //         },
        //         fields: ["item_code", "item_name", "stock_uom"]
        //     },
        //     callback: function(r) {

        //         if (r.message) {

        //             r.message.forEach(item => {

        //                 let row = frm.add_child("items");

        //                 row.item_code = item.item_code;
        //                 row.item_name = item.item_name;
        //                 row.qty = 1;

        //                 let default_uom = "";

        //                 if (item.item_code == "LL-SV-00002") {
        //                     default_uom = "100gm";
        //                 }
        //                 else if (item.item_code == "LL-CH-00002") {
        //                     default_uom = "80gm";
        //                 }
        //                 else if (item.item_code == "LL-CH-00033") {
        //                     default_uom = "80gm";
        //                 }
        //                 else if (item.item_code == "LL-SV-00080") {
        //                     default_uom = "100gm";
        //                 }
        //                 else if (item.item_code == "LL-SV-00114") {
        //                     default_uom = "100gm";
        //                 }
        //                 else if (item.item_code == "LL-GI-00053") {
        //                     default_uom = "200gm";
        //                 }
                        

        //                 row.uom = default_uom;

        //             });

        //             frm.refresh_field("items");
        //         }
        //     }
        // });
        frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Item",
                    filters: {
                        custom_is_retail_item: 1
                    },
                    fields: ["name", "item_name", "stock_uom"]
                },
                callback: function (r) {

                    if (r.message) {

                        let items = r.message;
                        let pending = items.length;

                        items.forEach(item => {

                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Item",
                                    name: item.name
                                },
                                callback: function(res) {

                                    let retail_uoms = [];

                                    if (res.message && res.message.uoms) {
                                        retail_uoms = res.message.uoms.filter(d => d.custom_is_retail_uom == 1);
                                    }


                                    if (retail_uoms.length > 0) {

                                        retail_uoms.forEach(uom_row => {

                                            let row = frm.add_child("items");

                                            row.item_code = item.name;
                                            row.item_name = item.item_name;
                                            row.qty = 1;

                                            row.uom = uom_row.uom;
                                            row.stock_uom = item.stock_uom;
                                            row.conversion_factor = uom_row.conversion_factor;
                                        });

                                    } else {

                                        // fallback
                                        let row = frm.add_child("items");

                                        row.item_code = item.name;
                                        row.item_name = item.item_name;
                                        row.qty = 1;

                                        row.uom = item.stock_uom;
                                        row.stock_uom = item.stock_uom;
                                        row.conversion_factor = 1;
                                    }

                                    pending--;

                                    if (pending === 0) {
                                        frm.refresh_field("items");
                                    }
                                }
                            });

                        });
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

    },
});


frappe.ui.form.on('Stock Movement Items', {
    qty(frm, cdt, cdn) {

        let row = locals[cdt][cdn];
        let qty = flt(row.qty);

        frappe.call({
            method: "teampro.teampro.doctype.rs_delivery.rs_delivery.get_latest_selling_price",
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

                        let amount = qty * total_rate;
                        frappe.model.set_value(cdt, cdn, "amount", amount);

                        let total_billable = 0;
                        frm.doc.items.forEach(function(item) {
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
                            


                            let amount_gst = total_rate * qty;

                            // set values
                            frappe.model.set_value(cdt, cdn, "gst", gst_rate_total);
                            frappe.model.set_value(cdt, cdn, "rate_without_gst", total_rate);
                            frappe.model.set_value(cdt, cdn, "amount_without_gst", amount_gst);
                            frappe.model.set_value(cdt, cdn, "mrp_without_gst", mrp_gst);


                            
                            let vat_amount = 0;

                            frm.doc.items.forEach(function(item) {
                                let amt_wo_gst = flt(item.amount_without_gst || 0);
                                let amt = flt(item.amount || 0);

                                vat_amount += (amt - amt_wo_gst);  
                            });

                            // Sum of amount_without_gst
                            let total_billable = 0;
                            frm.doc.items.forEach(function(item) {
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
                            let amount = qty * rate;
                            frappe.model.set_value(cdt, cdn, "rate", rate);
                            frappe.model.set_value(cdt, cdn, "amount", amount);
                            frappe.model.set_value(cdt, cdn, "mrp", mrp);
                            frm.set_value("total_amount", total_billable);
                            
                            let total_billable = 0;
                            frm.doc.items.forEach(function(item) {
                                total_billable += flt(item.amount || 0);
                            });
                            frm.set_value("total_amount", total_billable);
                        }

                    });
                }
            }
        });
        
    },
    
});



