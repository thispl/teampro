// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt
frappe.ui.form.on("Stock Counting", {
    scan_barcode: function(frm) {
        if (frm.doc.scan_barcode) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Item",
                    filters: {
                        barcode: frm.doc.scan_barcode
                    },
                    fields: ["item_code", "item_name", "stock_uom"]
                },
                callback: function(r) {
                    if (r.message && r.message.length) {
                        
                        const item = r.message[0];
                        frappe.db.get_value('Item',{"name":item.item_code},'disabled')
                    .then(r => {
                        var value = r.message.disabled
                        if (value==1){
                            frm.set_value("scan_barcode", ""); 
                            frappe.throw("This item is disabled. Kindly scan another Item")
                        }else{
                            frappe.call({
                            method: "teampro.custom.get_previous_count",
                            args: {
                                name: item.item_code,
                                date: frm.doc.date
                            },
                            callback: function(res) {
                                const previous_count = res.message || 0;

                                let dialog = new frappe.ui.Dialog({
                                    title: `Stock Entry for ${item.item_name}`,
                                    fields: [
                                        {
                                            label: 'Item',
                                            fieldname: 'item_code',
                                            fieldtype: 'Data',
                                            default: item.item_code,
                                            read_only: 1
                                        },
                                        {
                                            label: 'Item Name',
                                            fieldname: 'item_name',
                                            fieldtype: 'Data',
                                            default: item.item_name,
                                            read_only: 1
                                        },
                                        {
                                            label: 'Stock UOM',
                                            fieldname: 'stock_uom',
                                            fieldtype: 'Data',
                                            default: item.stock_uom,
                                            read_only: 1
                                        },
                                        {
                                            label: 'Previous Day Count',
                                            fieldname: 'previous_count',
                                            fieldtype: 'Int',
                                            default: previous_count,
                                            read_only: 1
                                        },
                                        {
                                            label: 'Current Count',
                                            fieldname: 'current_count',
                                            fieldtype: 'Float',
                                            reqd: 1
                                        }
                                    ],
                                    primary_action_label: 'Submit',
                                    primary_action(values) {
                                        const exists = frm.doc.details.some(row => row.item === values.item_code);
                                        if (exists) {
                                            frappe.msgprint(`Item ${values.item_code} is already added.`);
                                            dialog.hide();
                                            frm.set_value("scan_barcode", ""); // Clear barcode
                                            frm.save();
                                            return;
                                        }

                                        frm.add_child('details', {
                                            'item': values.item_code,
                                            'item_name': item.item_name,
                                            'previous_count': previous_count,
                                            'count': values.current_count,
                                            'date_and_time': frappe.datetime.now_datetime()
                                        });
                                        frm.refresh_field('details');
                                        dialog.hide();
                                        frm.set_value("scan_barcode", ""); // Clear barcode after use
                                        frm.save();
                                    }
                                });

                                // Always clear scan_barcode when dialog is closed
                                dialog.onhide = function () {
                                    frm.set_value("scan_barcode", "");
                                };

                                dialog.show();
                            }
                        });
                        }
                    })
                        // frappe.call({
                        //     method: "teampro.custom.get_previous_count",
                        //     args: {
                        //         name: item.item_code,
                        //         date: frm.doc.date
                        //     },
                        //     callback: function(res) {
                        //         const previous_count = res.message || 0;

                        //         let dialog = new frappe.ui.Dialog({
                        //             title: `Stock Entry for ${item.item_name}`,
                        //             fields: [
                        //                 {
                        //                     label: 'Item',
                        //                     fieldname: 'item_code',
                        //                     fieldtype: 'Data',
                        //                     default: item.item_code,
                        //                     read_only: 1
                        //                 },
                        //                 {
                        //                     label: 'Item Name',
                        //                     fieldname: 'item_name',
                        //                     fieldtype: 'Data',
                        //                     default: item.item_name,
                        //                     read_only: 1
                        //                 },
                        //                 {
                        //                     label: 'Stock UOM',
                        //                     fieldname: 'stock_uom',
                        //                     fieldtype: 'Data',
                        //                     default: item.stock_uom,
                        //                     read_only: 1
                        //                 },
                        //                 {
                        //                     label: 'Previous Day Count',
                        //                     fieldname: 'previous_count',
                        //                     fieldtype: 'Int',
                        //                     default: previous_count,
                        //                     read_only: 1
                        //                 },
                        //                 {
                        //                     label: 'Current Count',
                        //                     fieldname: 'current_count',
                        //                     fieldtype: 'Int',
                        //                     reqd: 1
                        //                 }
                        //             ],
                        //             primary_action_label: 'Submit',
                        //             primary_action(values) {
                        //                 frm.add_child('details', {
                        //                     'item': values.item_code,
                        //                     'item_name': item.item_name,
                        //                     'previous_count': previous_count,
                        //                     'count': values.current_count,
                        //                     'date_and_time': frappe.datetime.now_datetime()
                        //                 });
                        //                 frm.refresh_field('details');
                        //                 dialog.hide();
                        //                 frm.set_value("scan_barcode", ""); // Clear barcode after use
                        //                 frm.save();
                        //             }
                        //         });

                        //         // Always clear scan_barcode when dialog is closed
                        //         dialog.onhide = function () {
                        //             frm.set_value("scan_barcode", "");
                        //         };

                        //         dialog.show();
                        //     }
                        // });
                    } else {
                        frappe.msgprint("No item found with this barcode.");
                        frm.set_value("scan_barcode", ""); // Clear on failed scan
                    }
                }
            });
        }
    }
});
