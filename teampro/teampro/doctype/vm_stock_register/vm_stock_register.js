// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("VM Stock Register", {
	machine_id(frm) {
		if (frm.doc.machine_id) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Warehouse",
					name: frm.doc.machine_id
				},
				callback: function(res) {
					let rack_data = res.message.custom_rack_wise_capacity_details || [];
					// Slot A
					(frm.doc.slot_a || []).forEach(row => {
						let match = rack_data.find(d => d.rack_id === row.slot_id);
						if (match) {
							frappe.model.set_value(
								row.doctype,
								row.name,
								'custom_capacity',
								match.capacity
							);
						}
					});
					frm.refresh_field('slot_a');
					// Slot B
					(frm.doc.slot_b || []).forEach(row => {
						let match = rack_data.find(d => d.rack_id === row.slot_id);
						if (match) {
							frappe.model.set_value(
								row.doctype,
								row.name,
								'custom_capacity',
								match.capacity
							);
						}
					});
					frm.refresh_field('slot_b');
					// Slot C
					(frm.doc.slot_c || []).forEach(row => {
						let match = rack_data.find(d => d.rack_id === row.slot_id);
						if (match) {
							frappe.model.set_value(
								row.doctype,
								row.name,
								'custom_capacity',
								match.capacity
							);
						}
					});
					frm.refresh_field('slot_c');
					// Slot D
					(frm.doc.slot_d || []).forEach(row => {
						let match = rack_data.find(d => d.rack_id === row.slot_id);
						if (match) {
							frappe.model.set_value(
								row.doctype,
								row.name,
								'custom_capacity',
								match.capacity
							);
						}
					});
					frm.refresh_field('slot_d');
					// Slot E
					(frm.doc.slot_e || []).forEach(row => {
						let match = rack_data.find(d => d.rack_id === row.slot_id);
						if (match) {
							frappe.model.set_value(
								row.doctype,
								row.name,
								'custom_capacity',
								match.capacity
							);
						}
					});
					frm.refresh_field('slot_e');
					// Slot F
					(frm.doc.slot_f || []).forEach(row => {
						let match = rack_data.find(d => d.rack_id === row.slot_id);
						if (match) {
							frappe.model.set_value(
								row.doctype,
								row.name,
								'custom_capacity',
								match.capacity
							);
						}
					});
					frm.refresh_field('slot_f');
				}
			});
		}
	},
	setup: function(frm) {
		frm.set_query("machine_id", function () {

            let filters = [
                ["Warehouse","parent_warehouse", "=","LSVM - Vending Machines - TFP"],
				["Warehouse","disabled","=",0]
            ];


            return {
                filters: filters
            };
        });
		frappe.call({
			method: 'teampro.teampro.doctype.vm_stock_register.vm_stock_register.get_parent_item_group',
			args: {
				parent_item_group: 'Food Products',
			},
			callback: function(r) {
				if (r.message) {
					frm.set_query("item_code", "slot_a", function(doc, cdt, cdn) {
						return {
							filters: [
								['Item', 'item_group', 'in', r.message]
							]
						};
					});
					frm.set_query("item_code", "slot_b", function(doc, cdt, cdn) {
						return {
							filters: [
								['Item', 'item_group', 'in', r.message]
							]
						};
					});
					frm.set_query("item_code", "slot_c", function(doc, cdt, cdn) {
						return {
							filters: [
								['Item', 'item_group', 'in', r.message]
							]
						};
					});
					frm.set_query("item_code", "slot_d", function(doc, cdt, cdn) {
						return {
							filters: [
								['Item', 'item_group', 'in', r.message]
							]
						};
					});
					frm.set_query("item_code", "slot_e", function(doc, cdt, cdn) {
						return {
							filters: [
								['Item', 'item_group', 'in', r.message]
							]
						};
					});
					frm.set_query("item_code", "slot_f", function(doc, cdt, cdn) {
						return {
							filters: [
								['Item', 'item_group', 'in', r.message]
							]
						};
					});
				}
			}
		});
	},

	onload(frm) {
		if (frm.is_new()) {
			for (let i = 1; i <= 10; i++) {
				let row = frm.add_child("slot_a");
				row.slot_id = `A x ${i}`;
					if (i % 2 === 0) {
					row.read_only_row = 1;
				}
			}
			frm.refresh_field("slot_a");
			
			for (let i = 1; i <= 10; i++) {
				let row = frm.add_child("slot_b");
				row.slot_id = `B x ${i}`;
				if (i % 2 === 0) {
					row.read_only_row = 1;
				}
			}
			frm.refresh_field("slot_b");
			for (let i = 1; i <= 10; i++) {
				let row = frm.add_child("slot_c");
				row.slot_id = `C x ${i}`;
				if (i % 2 === 0) {
					row.read_only_row = 1;
				}
			}
			frm.refresh_field("slot_c");
			for (let i = 1; i <= 10; i++) {
				let row = frm.add_child("slot_d");
				row.slot_id = `D x ${i}`;
			   
			}
			frm.refresh_field("slot_d");
			for (let i = 1; i <= 10; i++) {
				let row = frm.add_child("slot_e");
				row.slot_id = `E x ${i}`;
				
			}
			frm.refresh_field("slot_e");
			for (let i = 1; i <= 10; i++) {
				let row = frm.add_child("slot_f");
				row.slot_id = `F x ${i}`;
				
			}
			frm.refresh_field("slot_f");
		}
	},
   
	refresh(frm){
		if(!frm.doc.__islocal){
			render_capacity_chart(frm);
			frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Stock Entry",
                    filters: {
                        custom_vm_stock_register: frm.doc.name,
						docstatus:["in",[0,1]]
                    },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function(r) {
                    if (!r.message || r.message.length === 0) {

                        frm.add_custom_button(__("Confirmed"), function () {

                            frappe.call({
                                method: "teampro.teampro.doctype.vm_stock_register.vm_stock_register.create_re_filling_stock_entries",
                                args: {
                                    doc_name: frm.doc.name
                                },
                                callback: function(r) {
                                    if (r.message) {
                                        frappe.msgprint(r.message);
										frm.reload_doc();
                                    }
                                }
                            });

                            frappe.call({
                                method: "teampro.teampro.doctype.vm_stock_register.vm_stock_register.create_packing_stock_entries",
                                args: {
                                    doc_name: frm.doc.name
                                }
                            });

                        }, "Status");

                    }

                }
            });
			
			
			if(frm.doc.status=="GRN Received"){
			frm.add_custom_button(__("Return"), function () {
					open_return_dialog(frm);
				},"Status");
			frm.add_custom_button(__("Completed"), function () {
					if(!frm.doc.refill_attachment){
						frappe.throw("Please attach the Refill Attachment before marking as Completed.")
					}
					let now = frappe.datetime.now_datetime();
					let d = new frappe.ui.Dialog({
						title: 'Completed Confirmation',
						fields: [
							{
								fieldtype: 'HTML',
								fieldname: 'info',
								options: `<div>Completed at <b>${frappe.datetime.str_to_user(now)}</b></div>`
							}
						],
						primary_action_label: 'Yes',
						primary_action() {
							frm.set_value('status', 'Completed');
							let child = frm.add_child('status_transition');
							child.status = 'Completed';
							child.date = now;
							frm.refresh_field('status_transition');
							// frm.save('Update');
							frm.save()
							d.hide();
						},
						secondary_action_label: 'No',
						secondary_action() {
							d.hide();
						}
					});
					d.show();
				},"Status");
			}
			frm.add_custom_button(__("Product Layout"), function () {
			var f_name = frm.doc.name
					var print_format = "Packing Slip - VM Stock Register";
					window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
						+ "doctype=" + encodeURIComponent("VM Stock Register")
						+ "&name=" + encodeURIComponent(f_name)
						+ "&trigger_print=1"
						+ "&format=" + print_format
						+ "&no_letterhead=0"
					));
				},"Print");
		frm.add_custom_button(__("Packing Slip"), function () {
					frappe.db.get_value('Stock Entry', { 'custom_vm_stock_register': frm.doc.name }, 'name')
                .then(r => {
                    if (r.message && r.message.name) {
                        let f_name = r.message.name;
                        let print_format = "Packing Slip VM";
                        
                        window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
                            + "doctype=" + encodeURIComponent("Stock Entry")
                            + "&name=" + encodeURIComponent(f_name)
                            + "&trigger_print=1"
                            + "&format=" + encodeURIComponent(print_format)
                            + "&no_letterhead=0"
                        ));
                    } else {
                        frappe.msgprint(__('Related Stock Entry not found'));
                    }
                });
				},"Print");
		frm.add_custom_button(__("DN Print"), function () {
			var f_name = frm.doc.name
					var print_format = "VM Delivery Note";
					window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
						+ "doctype=" + encodeURIComponent("VM Stock Register")
						+ "&name=" + encodeURIComponent(f_name)
						+ "&trigger_print=1"
						+ "&format=" + print_format
						+ "&no_letterhead=0"
					));
				},"Print");

		
			}

		
			
		let grid = frm.fields_dict.slot_a.grid;
		grid.grid_rows.forEach(row => {
			let is_read_only = row.doc.read_only_row === 1;
			row.toggle_editable('slot_id', !is_read_only);
			if (is_read_only) {
				row.wrapper.css('background-color', '#f2f2f2');
			}
		});
		
		let grid1 = frm.fields_dict.slot_b.grid;
		grid1.grid_rows.forEach(row => {
			let is_read_only = row.doc.read_only_row === 1;
			row.toggle_editable('slot_id', !is_read_only);
			if (is_read_only) {
				row.wrapper.css('background-color', '#f2f2f2');
			}
		});

		let grid2 = frm.fields_dict.slot_c.grid;
		grid2.grid_rows.forEach(row => {
			let is_read_only = row.doc.read_only_row === 1;
			row.toggle_editable('slot_id', !is_read_only);
			if (is_read_only) {
				row.wrapper.css('background-color', '#f2f2f2');
			}
		});
	   
		$('*[data-fieldname="slot_a"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="slot_a"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="slot_a"]').find('.grid-add-row').remove()
	 $('*[data-fieldname="slot_b"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="slot_b"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="slot_b"]').find('.grid-add-row').remove()
	 $('*[data-fieldname="slot_c"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="slot_c"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="slot_c"]').find('.grid-add-row').remove()
	 $('*[data-fieldname="slot_d"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="slot_d"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="slot_d"]').find('.grid-add-row').remove()
	 $('*[data-fieldname="slot_e"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="slot_e"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="slot_e"]').find('.grid-add-row').remove()
	 $('*[data-fieldname="slot_f"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="slot_f"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="slot_f"]').find('.grid-add-row').remove()
	 if(frm.doc.status=="Schedule"){
		 frm.add_custom_button(__("Packed"), function () {
		   let now = frappe.datetime.now_datetime();
			let d = new frappe.ui.Dialog({
				title: 'Packing Confirmation',
				fields: [
					{
						fieldtype: 'HTML',
						fieldname: 'info',
						options: `<div>Packing completed at <b>${frappe.datetime.str_to_user(now)}</b></div>`
					}
				],
				primary_action_label: 'Yes',
				primary_action() {
					frm.set_value('status', 'Packed');
					let child = frm.add_child('status_transition');
					child.status = 'Packed';
					child.date = now;
					frm.refresh_field('status_transition');
					// frm.save('Update');
					frm.save()
					d.hide();
				},
				secondary_action_label: 'No',
				secondary_action() {
					d.hide();
				}
			});
			d.show();

		},("Status"));}
		if(frm.doc.status=="Packed"){
		 frm.add_custom_button(__("Dispatched"), function () {
		   let now = frappe.datetime.now_datetime();
			let d = new frappe.ui.Dialog({
				title: 'Dispatched Confirmation',
				fields: [
					{
						fieldtype: 'HTML',
						fieldname: 'info',
						options: `<div>Dispatched completed at <b>${frappe.datetime.str_to_user(now)}</b></div>`
					}
				],
				primary_action_label: 'Yes',
				primary_action() {
					frm.set_value('status', 'Dispatched');
					let child = frm.add_child('status_transition');
					child.status = 'Dispatched';
					child.date = now;
					frm.refresh_field('status_transition');
					// frm.save('Update');
					frm.save()
					d.hide();
				},
				secondary_action_label: 'No',
				secondary_action() {
					d.hide();
				}
			});
			d.show();

		},("Status"));}
		if(frm.doc.status=="Dispatched"){
		//  frm.add_custom_button(__("GRN Received"), function () {
		//    let now = frappe.datetime.now_datetime();
		// 	let d = new frappe.ui.Dialog({
		// 		title: 'GRN Received Confirmation',
		// 		fields: [
		// 			{
		// 				fieldtype: 'HTML',
		// 				fieldname: 'info',
		// 				options: `<div>GRN Received (DN) completed at <b>${frappe.datetime.str_to_user(now)}</b></div>`
		// 			},
		// 			{
		// 				fieldtype: 'Attach',
		// 				fieldname: 'attach_grn',
		// 				reqd:1
		// 			}
		// 		],
				
		// 		primary_action_label: 'Yes',
		// 		primary_action() {
		// 			let values = d.get_values();
		// 			frm.set_value('status', 'GRN Received');
		// 			frm.set_value('grn_received',values.attach_grn);
		// 			let child = frm.add_child('status_transition');
		// 			child.status = 'GRN Received';
		// 			child.date = now;
		// 			frm.refresh_field('status_transition');
		// 			frm.save('Update');
		// 			d.hide();
		// 		},
		// 		secondary_action_label: 'No',
		// 		secondary_action() {
		// 			d.hide();
		// 		}
		// 	});
		// 	d.show();

		// },("Status"));
		frm.add_custom_button(__("GRN Received"), function () {
			let now = frappe.datetime.now_datetime();

			let d = new frappe.ui.Dialog({
				title: 'GRN Received Confirmation',
				fields: [
					{
						fieldtype: 'HTML',
						fieldname: 'info',
						options: `<div>GRN Received (DN) completed at <b>${frappe.datetime.str_to_user(now)}</b></div>`
					},
					{
						fieldtype: 'Attach',
						fieldname: 'attach_grn',
						reqd: 1
					}
				],

				primary_action_label: 'Yes',
				primary_action() {
					let values = d.get_values();

					if (!values.attach_grn) {
						frappe.msgprint("Please attach GRN file");
						return;
					}

					let promises = [];

					// Insert file like your requirement
					promises.push(
						frappe.call({
							freeze: true,
							freeze_message: 'Saving, please wait...',
							method: "frappe.client.insert",
							args: {
								doc: {
									doctype: "File",
									file_url: values.attach_grn,
									attached_to_doctype: frm.doc.doctype,
									attached_to_name: frm.doc.name,
									is_private: 0
								}
							}
						})
					);

					Promise.all(promises).then(() => {

						frm.set_value('status', 'GRN Received');
						frm.set_value('grn_received', values.attach_grn);

						let child = frm.add_child('status_transition');
						child.status = 'GRN Received';
						child.date = now;

						frm.refresh_field('status_transition');

						// frm.save('Update');
						frm.save()
						d.hide();
					});
				},

				secondary_action_label: 'No',
				secondary_action() {
					d.hide();
				}
			});

			d.show();

		}, __("Status"));
		
		}
		
   if(frm.doc.__islocal){
			frm.set_value("posting_date",frappe.datetime.now_datetime())
			frm.save()
		}
	   
		frm.fields_dict['slot_a'].grid.get_field('custom_primary_packing_cover').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Primary Packing (Cover)"
				}
			};
		};
		frm.fields_dict['slot_a'].grid.get_field('custom_secondary_packing_bag').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Secondary Packing (Bag)"
				}
			};
		};
		frm.fields_dict['slot_a'].grid.get_field('custom_tertiary_packingbox').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Tertiary Packing (Box)"
				}
			};
		};
		// 
		frm.fields_dict['slot_b'].grid.get_field('custom_primary_packing_cover').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Primary Packing (Cover)"
				}
			};
		};
		frm.fields_dict['slot_b'].grid.get_field('custom_secondary_packing_bag').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Secondary Packing (Bag)"
				}
			};
		};
		frm.fields_dict['slot_b'].grid.get_field('custom_tertiary_packingbox').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Tertiary Packing (Box)"
				}
			};
		};
		// 
		frm.fields_dict['slot_c'].grid.get_field('custom_primary_packing_cover').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Primary Packing (Cover)"
				}
			};
		};
		frm.fields_dict['slot_c'].grid.get_field('custom_secondary_packing_bag').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Secondary Packing (Bag)"
				}
			};
		};
		frm.fields_dict['slot_c'].grid.get_field('custom_tertiary_packingbox').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Tertiary Packing (Box)"
				}
			};
		};
		// 
		frm.fields_dict['slot_d'].grid.get_field('custom_primary_packing_cover').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Primary Packing (Cover)"
				}
			};
		};
		frm.fields_dict['slot_d'].grid.get_field('custom_secondary_packing_bag').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Secondary Packing (Bag)"
				}
			};
		};
		frm.fields_dict['slot_d'].grid.get_field('custom_tertiary_packingbox').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Tertiary Packing (Box)"
				}
			};
		};
		// 
		frm.fields_dict['slot_e'].grid.get_field('custom_primary_packing_cover').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Primary Packing (Cover)"
				}
			};
		};
		frm.fields_dict['slot_e'].grid.get_field('custom_secondary_packing_bag').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Secondary Packing (Bag)"
				}
			};
		};
		frm.fields_dict['slot_e'].grid.get_field('custom_tertiary_packingbox').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Tertiary Packing (Box)"
				}
			};
		};
		// 
		frm.fields_dict['slot_f'].grid.get_field('custom_primary_packing_cover').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Primary Packing (Cover)"
				}
			};
		};
		frm.fields_dict['slot_f'].grid.get_field('custom_secondary_packing_bag').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Secondary Packing (Bag)"
				}
			};
		};
		frm.fields_dict['slot_f'].grid.get_field('custom_tertiary_packingbox').get_query = function(doc, cdt, cdn) {
			return {
				filters: {
					item_group: "Tertiary Packing (Box)"
				}
			};
		};
	},
   
	upload(frm){
	   
		if (frm.doc.upload) {
			frappe.call({
				method: "teampro.teampro.doctype.vm_stock_register.vm_stock_register.vm_stock_import_excel",
				args: { docname: frm.doc.name },
				callback: function(r) {
					if (!r.exc) {
						frappe.msgprint("Excel data imported successfully.");
						frm.reload_doc();
					}
				}
			});
		}
	   
	},
	refill_attachment(frm){
		if (frm.doc.refill_attachment) {

        frm.save().then(() => {

            frappe.call({
                method: "teampro.teampro.doctype.vm_stock_register.vm_stock_register.vm_stock_import_refill_excel",
                args: { docname: frm.doc.name },
                callback: function(r) {
                    if (!r.exc) {
                        frappe.msgprint("Excel data imported successfully.");
                        frm.reload_doc();
                    }
                }
            });

        });

    	}
		if (!frm.doc.refill_attachment) {

            let slot_tables = ["slot_a", "slot_b", "slot_c", "slot_d", "slot_e", "slot_f"];

            slot_tables.forEach(function(table) {

                let rows = frm.doc[table] || [];

                rows.forEach(function(row) {
                    row.re_filling_qty = 0;
                });

                frm.refresh_field(table);
            });

        }
	}
  
});
frappe.ui.form.on('VM Stock Details', {
	item_code: function(frm, cdt, cdn) { 
		var child = locals[cdt][cdn];
		if (child.item_code){
			frappe.call({
				method: 'teampro.teampro.doctype.vm_stock_register.vm_stock_register.get_available_balance',
				args: {
					item_code: child.item_code,
					warehouse: 'Stores - TFP'
				},
				callback: function(r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, 'stock_qty', r.message);
					} 
					else {
						frappe.model.set_value(cdt, cdn, 'stock_qty', 0);
					}
				}
			});
		}
		else {
			frappe.model.set_value(cdt, cdn, 'stock_qty', 0);
		}
		if (child.new_stockuom && child.item_code) {
			frappe.call({
				method: 'teampro.teampro.doctype.vm_stock_register.vm_stock_register.get_uom_conversion',
				args: {
					item_code: child.item_code,
					uom: child.new_stockuom
				},
				callback: function(r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, 'conversion', r.message);
						if (child.new_stock_qty) {
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', (r.message * child.new_stock_qty));
						}
						else{
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', 0);
						}
					} 
					else {
						frappe.model.set_value(cdt, cdn, 'conversion', 0);
						if (child.new_stock_qty) {
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', child.new_stock_qty);
						}
						else{
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', 0);
						}
					}
				}
			});
		} 
		else {
			frappe.model.set_value(cdt, cdn, 'conversion', 0);
			if (child.new_stock_qty) {
				frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', child.new_stock_qty);
			}
			else{
				frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', 0);
			}
		}
	},
	custom_mrp: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, 'custom_mrp_r',child.custom_mrp);
	},
	new_stockuom: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, 'custom_weight_w',child.new_stockuom);
		if (child.new_stockuom && child.item_code) {
			frappe.call({
				method: 'teampro.teampro.doctype.vm_stock_register.vm_stock_register.get_uom_conversion',
				args: {
					item_code: child.item_code,
					uom: child.new_stockuom
				},
				callback: function(r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, 'conversion', r.message);
						if (child.new_stock_qty) {
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', (r.message * child.new_stock_qty));
						}
						else{
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', 0);
						}
					} 
					else {
						frappe.model.set_value(cdt, cdn, 'conversion', 0);
						if (child.new_stock_qty) {
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', child.new_stock_qty);
						}
						else{
							frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', 0);
						}
					}
				}
			});
		} 
		else {
			frappe.model.set_value(cdt, cdn, 'conversion', 0);
			if (child.new_stock_qty) {
				frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', child.new_stock_qty);
			}
			else{
				frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', 0);
			}
		}
	},

	new_stock_qty: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
			frappe.model.set_value(cdt, cdn, 'custom_covers',child.new_stock_qty);
			if(child.new_stock_qty && child.conversion){
				frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom', (child.conversion * child.new_stock_qty));
			}
			else{
				frappe.model.set_value(cdt, cdn, 'qty_as_per_stock_uom',0)
			}
	 },
	 custom_cover_per_bag: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.custom_covers && row.custom_cover_per_bag) {
			if (row.custom_cover_per_bag != 0) {
				row.custom_bag = row.custom_covers / row.custom_cover_per_bag;
			} else {
				row.custom_bag = 0;
			}
			frm.refresh_field('slot_a');
		}
		if (row.custom_covers && row.custom_cover_per_bag) {
			if (row.custom_cover_per_bag != 0) {
				row.custom_bag = row.custom_covers / row.custom_cover_per_bag;
			} else {
				row.custom_bag = 0;
			}
			frm.refresh_field('slot_b');
		}
		if (row.custom_covers && row.custom_cover_per_bag) {
			if (row.custom_cover_per_bag != 0) {
				row.custom_bag = row.custom_covers / row.custom_cover_per_bag;
			} else {
				row.custom_bag = 0;
			}
			frm.refresh_field('slot_c');
		}
	 },
	 custom_cover_per_box: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.custom_covers && row.custom_cover_per_box) {
			if (row.custom_cover_per_box != 0) {
				row.custom_box = row.custom_covers / row.custom_cover_per_box;
			} else {
				row.custom_box = 0;
			}
			frm.refresh_field('slot_a');
		}
	 },

});

function make_even_rows_read_only(frm) {
	let grid = frm.fields_dict.slot_a.grid;

	// Wait for grid to render
	setTimeout(() => {
		grid.grid_rows.forEach((grid_row, index) => {
			const row_number = index + 1;

			if (row_number % 2 === 0) {
				// Disable each field in this row
				for (let fieldname in grid_row.fields_dict) {
					let field = grid_row.fields_dict[fieldname];
					if (field) {
						field.set_input_disabled();  // ✅ disables input
					}
				}

				// Optional: style and hide delete button
				grid_row.wrapper.css('background-color', '#f2f2f2');
				grid_row.wrapper.find('.grid-remove-rows').hide();
			}
		});
	}, 100); // wait slightly for UI to render
}

frappe.provide('frappe.utils.link_title');

frappe.utils.link_title['Item'] = function (doc) {
	return `${doc.name} - ${doc.item_name}`;
};
function open_return_dialog(frm) {
	let dialog = new frappe.ui.Dialog({
		title: "Return Items",
		fields: [
			{
				label: "Download Template",
				fieldname: "download_template",
				fieldtype: "Button"
			},
			{
				label: "Upload Return File (.xlsx or .csv)",
				fieldname: "upload_file",
				fieldtype: "Attach",
				reqd:1
			}
		],
		primary_action_label: "Submit",
		primary_action: function (data) {
			if (!data.upload_file) {
				frappe.msgprint("Please upload a return file.");
				return;
			}
			frappe.dom.freeze("Processing file and creating Stock Entry...");
			// ✅ Save file to `return_document` and call backend to create stock entry
			frappe.call({
				method: "teampro.teampro.doctype.vm_stock_register.vm_stock_register.create_return_stock_entry",
				args: {
					docname: frm.doc.name,
					attached_file: data.upload_file
				},
				callback: function (r) {
					frappe.dom.unfreeze();
					if (!r.exc) {
						frappe.msgprint("Stock Entry created successfully.");
						dialog.hide();
					}
				},
				error: function () {
					frappe.dom.unfreeze();
					frappe.msgprint("❌ An error occurred while processing the file.");
				}
			});
		}
	});

	dialog.fields_dict.download_template.$wrapper.find("button").click(() => {
		download_template();
	});

	dialog.show();
}

function download_template() {
	const headers = ["Item Code", "UOM", "Qty"];
	const rows = [headers.join(",")];
	const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8;" });
	const link = document.createElement("a");
	link.href = URL.createObjectURL(blob);
	link.download = "return_template.csv";
	link.click();
}

function render_capacity_chart(frm) {
    let slots = ["slot_a", "slot_b", "slot_c", "slot_d", "slot_e", "slot_f"];

    let labels = [];
    let capacity = [];
    let refilled = [];

    slots.forEach(slot => {
        let total_capacity = 0;
        let total_refilled = 0;

        (frm.doc[slot] || []).forEach(row => {
            total_capacity += row.custom_capacity || 0;
            total_refilled += row.re_filling_qty || 0;
        });

        let rack_label = "Rack-" + slot.split("_")[1].toUpperCase();

        labels.push(rack_label);
        capacity.push(total_capacity);
        refilled.push(total_refilled);
    });

    $(frm.fields_dict.capacity_data.wrapper).html("");

    let chart_container = $(`<div id="capacity-chart" style="height:300px;"></div>`);
    $(frm.fields_dict.capacity_data.wrapper).append(chart_container);

    new frappe.Chart("#capacity-chart", {
        data: {
            labels: labels,
            datasets: [
                { name: "Capacity", values: capacity },
                { name: "Refilled", values: refilled }
            ]
        },
        type: "bar",
        height: 300,
        colors: ["#5e64ff", "#28a745"]
    });
}