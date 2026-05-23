// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("RC Return", {
    refresh(frm){
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
    },
	customer(frm) {
        if(frm.doc.customer){
            frappe.db.get_value("Customer", frm.doc.customer, "custom_retail_customer")
            .then(r => {
                if(r.message && r.message.custom_retail_customer){
                    let retail_id = r.message.custom_retail_customer;
                    frappe.db.get_value("Warehouse", { custom_retail_customer: retail_id }, "name")
                    .then(res => {
                        if(res.message && res.message.name){
                            frm.set_value("customer_warehouse", res.message.name).then(() => {
                                // Only now fetch items
                                frappe.call({
                                    // method: "teampro.teampro.doctype.rs_invoice.rs_invoice.get_transferred_items_with_qty",
                                    method: "teampro.teampro.doctype.rs_invoice.rs_invoice.transferred_items_with_qty",
                                    args: {
                                        customer: frm.doc.customer,
                                        customer_warehouse: res.message.name
                                    },
                                    callback: function(r){
                                        if(r.message){
                                            frm.clear_table("return_items");
                                            r.message.forEach(item => {
                                                let row = frm.add_child("return_items");
                                                row.item_code = item.item_code;
                                                row.item_name = item.item_name;
                                                row.uom = item.uom;
                                                row.customer_qty = item.customer_qty;
                                            });  
                                            frm.refresh_field("return_items");
                                        }
                                    }
                                });
                            });
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
    }
});
