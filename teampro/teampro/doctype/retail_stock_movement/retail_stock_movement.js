// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Retail Stock Movement", {
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

	},
    customer: function(frm) {
        if (frm.doc.customer) {
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
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Item",
                    filters: {
                        custom_is_retail_item: 1
                    },
                    fields: ["item_code", "item_name", "stock_uom"]
                },
                callback: function(r) {

                    if (r.message) {

                        r.message.forEach(item => {

                            let row = frm.add_child("items");

                            row.item_code = item.item_code;
                            row.item_name = item.item_name;
                            row.uom = item.stock_uom;
                            row.qty = 1;   

                        });

                        frm.refresh_field("items");
                    }
                }
            });

        } 

    },

});
