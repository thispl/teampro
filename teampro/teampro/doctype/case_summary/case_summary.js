// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Case Summary", {
	refresh(frm){
		frappe.db.get_value("User Permission", {'user': frappe.session.user,'allow':'Customer'}, ['for_value'], (r) => {
			if (r){
				frm.set_value('company', r.for_value);
			}
		});
		// frm.trigger('get_data');
		frm.disable_save();
	},
	onload: function(frm) {
        frm.disable_save(); 
        frappe.call({
            method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options', 
            callback: function(response) {
                if (response.message) {
                    var options = response.message;
                    var field = frm.fields_dict.report_status;
                    field.df.options = options.join("\n");
                    field.refresh();
                }
            }
        });
    },
	employee_name(frm){
		frm.trigger('get_data');
			// frappe.call({
			// 	method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
			// 	args: {
			// 		batch: frm.doc.batch,
			// 		from_date: frm.doc.from_date,
			// 		to_date: frm.doc.to_date,
			// 		company: frm.doc.company,
			// 		case: frm.doc.case_status 
			// 	},
			// 	callback: function(r) {
			// 		if (r.message) {
			// 			var options = r.message.report_options;
			// 			var field = frm.fields_dict.report_status;
			// 			field.df.options = options.join("\n");
			// 			field.refresh();			
			// 			var caseOptions = r.message.status_options;
			// 			var caseField = frm.fields_dict.case_status;
			// 			caseField.df.options = caseOptions.join("\n");
			// 			caseField.refresh();
			// 		}
			// 	}
			// });
		// }
		
	},
	employee_id(frm){
		// if (frm.doc.employee_id) {
			frm.trigger('get_data');
			// frappe.call({
			// 	method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
			// 	args: {
			// 		batch: frm.doc.batch,
			// 		from_date: frm.doc.from_date,
			// 		to_date: frm.doc.to_date,
			// 		company: frm.doc.company,
			// 		case: frm.doc.case_status 
			// 	},
			// 	callback: function(r) {
			// 		if (r.message) {
			// 			var options = r.message.report_options;
			// 			var field = frm.fields_dict.report_status;
			// 			field.df.options = options.join("\n");
			// 			field.refresh();			
			// 			var caseOptions = r.message.status_options;
			// 			var caseField = frm.fields_dict.case_status;
			// 			caseField.df.options = caseOptions.join("\n");
			// 			caseField.refresh();
			// 		}
			// 	}
			// });
		// }
		
	},
	report_status(frm){
		if (frm.doc.report_status) {
			frm.trigger('get_data');
			// frappe.call({
			// 	method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
			// 	args: {
			// 		batch: frm.doc.batch,
			// 		from_date: frm.doc.from_date,
			// 		to_date: frm.doc.to_date,
			// 		company: frm.doc.company,
			// 		case: frm.doc.case_status 
			// 	},
			// 	callback: function(r) {
			// 		if (r.message) {
			// 			var options = r.message.report_options;
			// 			var field = frm.fields_dict.report_status;
			// 			field.df.options = options.join("\n");
			// 			field.refresh();			
			// 			var caseOptions = r.message.status_options;
			// 			var caseField = frm.fields_dict.case_status;
			// 			caseField.df.options = caseOptions.join("\n");
			// 			caseField.refresh();
			// 		}
			// 	}
			// });
		}
		
	},
	case_status(frm){
		// if (frm.doc.case_status) {
			frm.trigger('get_data');
			// frappe.call({
			// 	method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
			// 	args: {
			// 		batch: frm.doc.batch,
			// 		from_date: frm.doc.from_date,
			// 		to_date: frm.doc.to_date,
			// 		company: frm.doc.company,
			// 		case: frm.doc.case_status 
			// 	},
			// 	callback: function(r) {
			// 		if (r.message) {
			// 			var options = r.message.report_options;
			// 			var field = frm.fields_dict.report_status;
			// 			field.df.options = options.join("\n");
			// 			field.refresh();			
			// 			var caseOptions = r.message.status_options;
			// 			var caseField = frm.fields_dict.case_status;
			// 			caseField.df.options = caseOptions.join("\n");
			// 			caseField.refresh();
			// 		}
			// 	}
			// });
			
		// }
		
	},
	// company(frm) {
	// 	if (frm.doc.company) {
	// 		frm.trigger('get_data');
	// 		frappe.call({
	// 			method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
	// 			args: {
	// 				batch: frm.doc.batch,
	// 				from_date: frm.doc.from_date,
	// 				to_date: frm.doc.to_date,
	// 				company: frm.doc.company,
	// 				case: frm.doc.case_status 
	// 			},
	// 			callback: function(r) {
	// 				if (r.message) {
	// 					console.log(r.message)
	// 					var options = r.message.report_options;
	// 					var field = frm.fields_dict.report_status;
	// 					field.df.options = options.join("\n");
	// 					field.refresh();			
	// 					var caseOptions = r.message.status_options;
	// 					var caseField = frm.fields_dict.case_status;
	// 					caseField.df.options = caseOptions.join("\n");
	// 					caseField.refresh();
	// 				}
	// 			}
	// 		});
	// 	}
		
	// },
	batch(frm) {
		if (frm.doc.batch) {
			frm.trigger('get_data');
			frappe.call({
				method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
				args: {
					batch: frm.doc.batch,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date,
					company: frm.doc.company,
					case: frm.doc.case_status 
				},
				callback: function(r) {
					if (r.message) {
						var options = r.message.report_options;
						var field = frm.fields_dict.report_status;
						field.df.options = options.join("\n");
						field.refresh();			
						var caseOptions = r.message.status_options;
						var caseField = frm.fields_dict.case_status;
						caseField.df.options = caseOptions.join("\n");
						caseField.refresh();
					}
				}
			});
		}
		
	},
	
	to_date(frm) {
		if (frm.doc.from_date && frm.doc.to_date ){
			frm.trigger('get_data');
			frappe.call({
				method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
				args: {
					batch: frm.doc.batch,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date,
					company: frm.doc.company,
					case: frm.doc.case_status 
				},
				callback: function(r) {
					if (r.message) {
						var options = r.message.report_options;
						var field = frm.fields_dict.report_status;
						field.df.options = options.join("\n");
						field.refresh();			
						var caseOptions = r.message.status_options;
						var caseField = frm.fields_dict.case_status;
						caseField.df.options = caseOptions.join("\n");
						caseField.refresh();
					}
				}
			});
		}
	},
	from_date(frm) {
		if (frm.doc.from_date && frm.doc.to_date ){
			frm.trigger('get_data');
			frappe.call({
				method: 'teampro.teampro.doctype.case_summary.case_summary.return_report_options',
				args: {
					batch: frm.doc.batch,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date,
					company: frm.doc.company,
					case: frm.doc.case_status 
				},
				callback: function(r) {
					if (r.message) {
						var options = r.message.report_options;
						var field = frm.fields_dict.report_status;
						field.df.options = options.join("\n");
						field.refresh();			
						var caseOptions = r.message.status_options;
						var caseField = frm.fields_dict.case_status;
						caseField.df.options = caseOptions.join("\n");
						caseField.refresh();
					}
				}
			});
		}
	},
	download(frm) {
		var path = "teampro.case_details.download";
		var args = {
			cmd: path,
			from_date: frm.doc.from_date,
			to_date: frm.doc.to_date,
			batch: frm.doc.batch,
			company:frm.doc.company,
			case:frm.doc.case_status,
			report:frm.doc.report_status,
			empname:frm.doc.employee_name,
			empid:frm.doc.employee_id
		};
	
		var url = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
		url += '&' + $.param(args); 
		window.location.href = url;
	},
	get_data(frm) {
		frappe.call({
			method: "teampro.teampro.doctype.case_summary.case_summary.get_batch_data",
			args: {
				batch: frm.doc.batch,
				from_date: frm.doc.from_date,
				to_date: frm.doc.to_date,
				company: frm.doc.company,
				case: frm.doc.case_status,
				report: frm.doc.report_status,
				empname: frm.doc.employee_name,
				empid: frm.doc.employee_id,
			},
			callback: function (r) {
				if (r.message) {
					frappe.require("assets/teampro/js/dataTables.min.js", () => {
					frm.fields_dict.html.$wrapper.empty().append(frappe.render_template('case_summary',{
						data:r.message
					}));
				});
				} else {
					frm.fields_dict.html.$wrapper.empty().append("<center><h2>Data Not Found</h2></center>");
				}
			}
		});
	}
	
	
});
window.downloadReport = function(f_name) {
	
				var print_format = "Verify Check Report-New3";
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Case")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
};
window.viewCaseStatus = function(f_name) {
    let d = new frappe.ui.Dialog({
        title: 'Check Status',
        fields: [
            {
                label: 'Checks',
                fieldname: 'checks',
                fieldtype: 'HTML',
            },
        ],
    });
    d.show();
    frappe.call({
        method: "teampro.teampro.doctype.case_summary.case_summary.check_status_table",
        args: {
            'name': f_name,
        },
        callback: function(response) {
            if(response.message) {
                d.fields_dict.checks.$wrapper.html(response.message);
            }
        }
    });
};


