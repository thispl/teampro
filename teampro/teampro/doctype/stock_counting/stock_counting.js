// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Stock Counting", {
    
    // scan_item(frm){
    //      load_barcode_scanner_lib(() => {
    //             open_barcode_scanner(frm);
    //         });
    // }
// });
// // Load qr-scanner.min.js dynamically
// function load_barcode_scanner_lib(callback) {
//     if (window.Quagga) {
//         callback();
//     } else {
//         const script = document.createElement("script");
//         script.src = "https://unpkg.com/@ericblade/quagga2@1.2.6/dist/quagga.min.js";
//         script.onload = callback;
//         document.head.appendChild(script);
//     }
// }


// function open_barcode_scanner(frm) {
//     const dialog = new frappe.ui.Dialog({
//         title: "Scan Barcode",
//         fields: [
//             {
//                 fieldtype: "HTML",
//                 fieldname: "scanner_html",
//                 options: `<div id="barcode-scanner" ></div>`
//             },
//             {
//             fieldtype: "HTML",
//             fieldname: "scan_message",
//             options: `<div style="text-align:center; font-weight:bold; color: #333;">
//                         Kindly scan the item for further processing
//                       </div>`
//         },
//         ],
        
//         size: "small",

//         primary_action_label: "Cancel",
//         primary_action() {
//             stop_barcode_scanner();
//             dialog.hide();
//         }
//     });

//     dialog.show();

//     const scannerElem = dialog.fields_dict.scanner_html.$wrapper[0];

//     window.Quagga.init({
//         inputStream: {
//     name: "Live",
//     type: "LiveStream",
//     target: scannerElem,
//     constraints: {
//         facingMode: "environment",
//         width: { ideal: 320 },
//         height: { ideal: 180 }
//     }
// },
//         decoder: {
//            readers: ["code_128_reader", "code_39_reader"]
//         }
//     }, err => {
//         if (err) {
//             console.error(err);
//             frappe.msgprint("Failed to start barcode scanner.");
//             return;
//         }

//         window.Quagga.start();
//     });
//    window.Quagga.onDetected(result => {
//     const scanned_value = result.codeResult.code;
//     stop_barcode_scanner();
//     dialog.hide();

//     frappe.call({
//         method: "teampro.custom.get_previous_count",
//         args: {
//             "name": scanned_value,
//             "date": frm.doc.date
//         },
//         callback(r) {
//             let previous_count = r.message || 0;

//             frappe.db.get_value('Item', { custom_item_barcode: scanned_value }, 'item_name')
//                 .then(res => {
//                     if (res.message) {
//                         const item_name = res.message.item_name;

//                         frappe.prompt([
//                             {
//                                 label: 'Item',
//                                 fieldname: 'item_code',
//                                 fieldtype: 'Data',
//                                 default: scanned_value,
//                                 read_only: 1
//                             },
//                             {
//                                 label: 'Item Name',
//                                 fieldname: 'item_name',
//                                 fieldtype: 'Data',
//                                 default: item_name,
//                                 read_only: 1
//                             },
//                             {
//                                 label: 'Previous Day Count',
//                                 fieldname: 'previous_count',
//                                 fieldtype: 'Int',
//                                 default: previous_count,
//                                 read_only: 1
//                             },
//                             {
//                                 label: 'Current Count',
//                                 fieldname: 'current_count',
//                                 fieldtype: 'Int',
//                                 reqd: 1
//                             }
//                         ], function(values) {
//                             frm.add_child('details', {
//                                 'item': values.item_code,
//                                 'count': values.current_count,
//                                 'date_and_time': frappe.datetime.now_datetime()
//                             });
//                             frm.refresh_field('details');
//                             frm.save();
//                         }, `Stock Entry for ${item_name}`);
//                     }
//                 });
//         }
//     });
// });


// }

// function stop_barcode_scanner() {
//     if (window.Quagga) {
//         window.Quagga.stop();
//         window.Quagga.offDetected();
//     }
// }



// frappe.ui.form.on("Stock Counting", {
//     scan_barcode: function(frm) {
//         if (frm.doc.scan_barcode) {
//             frappe.call({
//                 method: "frappe.client.get_list",
//                 args: {
//                     doctype: "Item",
//                     filters: {
//                         barcode: frm.doc.scan_barcode
//                     },
//                     fields: ["item_code", "item_name","stock_uom"]
//                 },
//                 callback: function(r) {
//                     if (r.message && r.message.length) {
//                         const item = r.message[0];

//                         // Now call your custom method to get the previous count
//                         frappe.call({
//                             method: "teampro.custom.get_previous_count",
//                             args: {
//                                 name: item.item_code,
//                                 date: frm.doc.date // assuming `date` is a field on the Stock Counting doctype
//                             },
//                             callback: function(res) {
//                                 const previous_count = res.message || 0;

//                                 frappe.prompt([
//                                     {
//                                         label: 'Item',
//                                         fieldname: 'item_code',
//                                         fieldtype: 'Data',
//                                         default: item.item_code,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Item Name',
//                                         fieldname: 'item_name',
//                                         fieldtype: 'Data',
//                                         default: item.item_name,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Stock UOM',
//                                         fieldname: 'stock_uom',
//                                         fieldtype: 'Data',
//                                         default: item.stock_uom,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Previous Day Count',
//                                         fieldname: 'previous_count',
//                                         fieldtype: 'Int',
//                                         default: previous_count,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Current Count',
//                                         fieldname: 'current_count',
//                                         fieldtype: 'Int',
//                                         reqd: 1
//                                     }
//                                 ], function(values) {
//                                     frm.add_child('details', {
//                                         'item': values.item_code,
//                                         'item_name':item.item_name,
//                                         'previous_count':previous_count,
//                                         'count': values.current_count,
//                                         'date_and_time': frappe.datetime.now_datetime()
//                                     });
//                                     frm.refresh_field('details');
//                                     frm.set_value("scan_barcode", ""); // Clear barcode field after scan
//                                     frm.save();
//                                 }, `Stock Entry for ${item.item_name}`);
//                             }
//                         });
//                     } else {
//                         frappe.msgprint("No item found with this barcode.");
//                     }
//                 }
//             });
//         }
//     }
// });

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
