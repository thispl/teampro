// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Formatted Reports  Download", {
	refresh(frm){
		
		frm.add_custom_button(("PDF"), function () {
			if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:04 – Batch Status Report (BSR)"){
				var print_format ="BCS - Batch Status Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:06 – Collection Pending Report – SI Outstanding (CPR)"){
				var print_format ="Sales Invoice Outstanding Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:01 – Opportunity Status Report (OSR)"){
				var print_format ="Opportunity Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:05 – To Be Billed - SO Outstanding (TBB)"){
				var print_format ="Sales Invoice Outstanding Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:02 – Project Status Report –(PSR - R)" && frm.doc.services_psr=="REC-I"){
				var print_format ="Project Status Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:03 – Project Task Status Report – REC (PTSR - R)"){
				var print_format ="Project Task Status Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type=="PR: Primary Reports" && frm.doc.primary_reports=="PR:03 – Closure Status Report (CSR)"){
				var print_format ="Closure Count - Status Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type=="MR: Monitoring Report" && frm.doc.primary_reports=="MR:05 – Closure Detailed Status Report (CDSR)"){
				var print_format ="Closure Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:07 – TODO Status Report"){
				var print_format ="ToDO Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.primary_reports=="Appointment Schedule Report"){
				var print_format ="Appointment Schedule Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.primary_reports=="Appointment Taken Report"){
				var print_format ="Appointment Taken Report";
				var f_name = frm.doc.name
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			}
			if (frm.doc.report_type == 'PR: Primary Reports' &&
				frm.doc.primary_reports == "PR:02 – Project Status Report –(PSR - R)" &&
				frm.doc.services_psr == "IT-SW") {
	   
				var path = "teampro.teampro.doctype.formatted_reports__download.formatted_report_download_pdf.download_pdf";
			
				// If both fields are empty, prevent download and show a message
				// if (!frm.doc.customer && !frm.doc.project) {
				// 	frappe.msgprint(__('Please select either a Customer or a Project to generate the report.'));
				// 	return;
				// }
			
				var args = [];
	
				if (frm.doc.customer) {
					
					args.push("customer=" + encodeURIComponent(frm.doc.customer));
				}
				if (frm.doc.project) {
					args.push("project=" + encodeURIComponent(frm.doc.project));
				}
			
				if (path) {
					window.location.href = frappe.request.url + '?cmd=' + encodeURIComponent(path) + '&' + args.join("&");
				}
			}	
		},("Action")); 
		frm.add_custom_button(("Excel"), function () {

			



			if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:04 – Batch Status Report (BSR)") {
				if(!frm.doc.batch_customer && !frm.doc.batch){
				var path_for_bsr = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_bcs_report";
				}
				else if(frm.doc.batch_customer && !frm.doc.batch){
					var path_for_bsr_cust = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_bcs_report_cust";
				}
				else if(frm.doc.batch && !frm.doc.batch_customer){
					var path_for_bsr_batch = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_bcs_report_batch";
				}
				// var path_for_bsr = "teampro.custom.download_bcs_report";	
				// var args_for_bsr="batch_customer=%(batch_customer)s&batch=%(batch)s"
	
			}
			else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:06 – Collection Pending Report – SI Outstanding (CPR)") {
				var si_path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_sales_invoice_outstanding_report";
				var args = "account_manager=%(account_manager)s&delivery_manager=%(delivery_manager)s&service=%(service)s&sompany=%(company)s"
			}
			if (si_path) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: si_path,
					args: args,
					account_manager : frm.doc.account_manager,
					delivery_manager: frm.doc.delivery_manager,
					service: frm.doc.service,
					company: frm.doc.company
				});
			}
			
			else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:01 – Opportunity Status Report (OSR)") {

				var opp_path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.opportunity_excel_report"
				var args = "opportunity_owner=%(opportunity_owner)s&opp_am=%(opp_am)s&opp_service=%(opp_service)s"
			}
			if (opp_path){
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
						cmd: opp_path,
						args: args,
						opportunity_owner: frm.doc.opportunity_owner,
						opp_am: frm.doc.opp_am,
						opp_service: frm.doc.opp_service
					}
				)
			}
			else if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:03 – Project Task Status Report – REC (PTSR - R)") {
				// var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PTSR"
				var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports_download.download_PTSR_new"
			}
			else if( frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:04 – Batch Check Status Report (BCSR)"){
				var path = "teampro.teampro.doctype.formatted_reports__download.bcsr_report.download_bcsr"
			}
			else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:02 – Project Status Report –(PSR - R)" && frm.doc.services_psr=="REC-I") {
				if(!frm.doc.customer && !frm.doc.project){
				// var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR";
				var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports_download.download_PSR_new";
				}
				else if(frm.doc.customer && !frm.doc.project){
				// var path_for_psr_cust = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR_customer";	
				var path_for_psr_cust = "teampro.teampro.doctype.formatted_reports__download.formatted_reports_download.download_PSR_customer";
				var args_for_psr_cust="customer=%(customer)s"
				}	
				else if(frm.doc.project && !frm.doc.customer){
					// var path_for_psr_proj = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR_proj";
					var path_for_psr_proj = "teampro.teampro.doctype.formatted_reports__download.formatted_reports_download.download_PSR_proj";	
					var args_for_psr_proj="project=%(project)s"
					}	
				else if(frm.doc.project && frm.doc.customer){
					// var path_for_psr_both = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR_both";
					var path_for_psr_both = "teampro.teampro.doctype.formatted_reports__download.formatted_reports_download.download_PSR_both";	
					var args_for_psr_both="project=%(project)s&customer=%(customer)s"
					}		
	
			}
			else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:05 – To Be Billed - SO Outstanding (TBB)") {
				var so_path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_sales_order_outstanding_report";
				var args = "account_manager=%(account_manager)s&delivery_manager=%(delivery_manager)s&service=%(service)s&sompany=%(company)s"
			}
			if (so_path) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: so_path,
					args: args,
					account_manager : frm.doc.account_manager,
					delivery_manager: frm.doc.delivery_manager,
					service: frm.doc.service,
					company: frm.doc.company
				});
			}
			else if (frm.doc.report_type=="PR: Primary Reports" && frm.doc.primary_reports=="PR:03 – Closure Status Report (CSR)") {
				if (frm.doc.so_validate==1){
					var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_status_report_test";
				}
				else if(frm.doc.so_status==0 && frm.doc.so_validate==0){
					var path= "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_status_report_so_false";
				}
				else if(frm.doc.so_status==1){
					var path= "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_status_report_so_true";
				}
			}
			else if (frm.doc.report_type=="MR: Monitoring Report" && frm.doc.mr_title=="MR:05 – Closure Detailed Status Report (CDSR)") {
				var path_for_clr = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_report";
				var args_for_clr="so_status=%(so_status)s&so_validate=%(so_validate)s"
			}
			else if (frm.doc.primary_reports == "Appointment Schedule Report") {
				var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.app_schedule_excel_report"
			}
			else if (frm.doc.primary_reports == "Appointment Taken Report") {
				var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.app_taken_excel_report"
			}
			else if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:07 – TODO Status Report") {
	
				var path_for_todo = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_todo_report"
				var args = 'allocated_to=%(allocated_to)s'
			}
			if (path) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
						cmd: path
				});
			}
			if (path_for_todo) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: path_for_todo,
					args: args,
					allocated_to : frm.doc.allocated_to,
	
				});
			}
			if (path_for_bsr) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_bsr,
					// args: args_for_bsr,
					// batch_customer : frm.doc.batch_customer,
					// batch:frm.doc.batch
	
				});
			}
			if (path_for_bsr_cust) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_bsr_cust,
	
				});
			}
			if (path_for_bsr_batch) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_bsr_batch,
	
				});
			}
			if (path_for_psr_cust) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: path_for_psr_cust,
					args: args_for_psr_cust,
					customer : frm.doc.customer,
					// project:frm.doc.project
	
				});
			}
			if (path_for_psr_proj) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: path_for_psr_proj,
					args: args_for_psr_proj,
					project : frm.doc.project,
	
				});
			}
			if (path_for_psr_both) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: path_for_psr_both,
					args: args_for_psr_both,
					project : frm.doc.project,
					customer : frm.doc.customer,
	
				});
			}
			if (path_for_clr) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: path_for_clr,
					args: args_for_clr,
					so_status:frm.doc.so_status,
					so_validate:frm.doc.so_validate
	
				});
			}
			else if (frm.doc.report_type == 'PR: Primary Reports' &&
				frm.doc.primary_reports == "PR:02 – Project Status Report –(PSR - R)" &&
				frm.doc.services_psr == "IT-SW") {
	   
				var path = "teampro.teampro.doctype.formatted_reports__download.formatted_report_it_sw.download";
			
				var args = [];
	
				if (frm.doc.customer) {
					
					args.push("customer=" + encodeURIComponent(frm.doc.customer));
				}
				if (frm.doc.project) {
					args.push("project=" + encodeURIComponent(frm.doc.project));
				}
			
				if (path) {
					window.location.href = frappe.request.url + '?cmd=' + encodeURIComponent(path) + '&' + args.join("&");
				}
			}
			else if(frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR.07 – Target Status Report"){
				if(frm.doc.acc_manager && frm.doc.fiscal_year && !frm.doc.quarter && !frm.doc.month&& !frm.doc.date){
					frappe.call({
						method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_manager_individual",
						args: {
							"acc_manager":frm.doc.acc_manager,
							"fiscal_year":frm.doc.fiscal_year,
							
						},
						callback: function (r) {
							if (r.message) {
								let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
								let link = document.createElement("a");
								link.href = window.URL.createObjectURL(blob);
								link.download = r.message.filename;
								document.body.appendChild(link);
								link.click();
								document.body.removeChild(link);
							}
						}
					});
				}
				if(frm.doc.fiscal_year && !frm.doc.acc_manager && !frm.doc.quarter && !frm.doc.month&& !frm.doc.date && !frm.doc.target_service){
				
					frappe.call({
						method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_manager",
						args: {
							"fiscal_year":frm.doc.fiscal_year
						},
						callback: function (r) {
							if (r.message) {
								let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
								let link = document.createElement("a");
								link.href = window.URL.createObjectURL(blob);
								link.download = r.message.filename;
								document.body.appendChild(link);
								link.click();
								document.body.removeChild(link);
							}
						}
					});
				}
				if(!frm.doc.acc_manager &&  frm.doc.fiscal_year && frm.doc.quarter){
				frappe.call({
						method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_manager_quarter",
						args: {
							"quarter":frm.doc.quarter,
							"fiscal_year":frm.doc.fiscal_year,
							
						},
						callback: function (r) {
							if (r.message) {
								let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
								let link = document.createElement("a");
								link.href = window.URL.createObjectURL(blob);
								link.download = r.message.filename;
								document.body.appendChild(link);
								link.click();
								document.body.removeChild(link);
							}
						}
					});
				}
				if(frm.doc.acc_manager &&  frm.doc.fiscal_year && frm.doc.quarter && !frm.doc.month){
					frappe.call({
							method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc",
							args: {
								"quarter":frm.doc.quarter,
								"fiscal_year":frm.doc.fiscal_year,
								"acc_manager":frm.doc.acc_manager
							},
							callback: function (r) {
								if (r.message) {
									let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
									let link = document.createElement("a");
									link.href = window.URL.createObjectURL(blob);
									link.download = r.message.filename;
									document.body.appendChild(link);
									link.click();
									document.body.removeChild(link);
								}
							}
						});
					}
					if(frm.doc.acc_manager &&  frm.doc.fiscal_year && frm.doc.quarter && frm.doc.month){
					frappe.call({
							method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_month",
							args: {
								"quarter":frm.doc.quarter,
								"fiscal_year":frm.doc.fiscal_year,
								"acc_manager":frm.doc.acc_manager,
								"month":frm.doc.month
							},
							callback: function (r) {
								if (r.message) {
									let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
									let link = document.createElement("a");
									link.href = window.URL.createObjectURL(blob);
									link.download = r.message.filename;
									document.body.appendChild(link);
									link.click();
									document.body.removeChild(link);
								}
							}
						});
					}
					if(!frm.doc.acc_manager &&  frm.doc.fiscal_year && frm.doc.quarter && frm.doc.month){
					frappe.call({
							method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_quarter_month_report",
							args: {
								"quarter":frm.doc.quarter,
								"fiscal_year":frm.doc.fiscal_year,
								"acc_manager":frm.doc.acc_manager,
								"month":frm.doc.month
							},
							callback: function (r) {
								if (r.message) {
									let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
									let link = document.createElement("a");
									link.href = window.URL.createObjectURL(blob);
									link.download = r.message.filename;
									document.body.appendChild(link);
									link.click();
									document.body.removeChild(link);
								}
							}
						});
					}
					if(!frm.doc.acc_manager && frm.doc.fiscal_year&& frm.doc.date &&!frm.doc.quarter && !frm.doc.month && !frm.doc.target_service){
						
						frappe.call({
							method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_employee_targets_report",
							args: {
								"date":frm.doc.date,
								"acc_manager":frm.doc.acc_manager,
								"fiscal_year":frm.doc.fiscal_year
							},
							callback: function (r) {
								if (r.message) {
									let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
									let link = document.createElement("a");
									link.href = window.URL.createObjectURL(blob);
									link.download = r.message.filename;
									document.body.appendChild(link);
									link.click();
									document.body.removeChild(link);
								}
							}
						});
					}
					if(frm.doc.acc_manager && !frm.doc.month && !frm.doc.target_service && frm.doc.date &&!frm.doc.quarter && frm.doc.fiscal_year){
						
							frappe.call({
								method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_employee_targets_report_acc",
								args: {
									"acc_manager":frm.doc.acc_manager,
									"fiscal_year":frm.doc.fiscal_year,
									"date":frm.doc.date
								},
								callback: function (r) {
									if (r.message) {
										let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
										let link = document.createElement("a");
										link.href = window.URL.createObjectURL(blob);
										link.download = r.message.filename;
										document.body.appendChild(link);
										link.click();
										document.body.removeChild(link);
									}
								}
							});
						}
					if(!frm.doc.acc_manager && !frm.doc.month && frm.doc.target_service){
					frappe.call({
						method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_service",
						args: {
							"acc_manager":frm.doc.acc_manager,
							"month":frm.doc.month,
							"target_service":frm.doc.target_service
						},
						callback: function (r) {
							if (r.message) {
								let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
								let link = document.createElement("a");
								link.href = window.URL.createObjectURL(blob);
								link.download = r.message.filename;
								document.body.appendChild(link);
								link.click();
								document.body.removeChild(link);
							}
						}
					});
				}
				// if(!frm.doc.acc_manager && !frm.doc.month && !frm.doc.target_service){
				// 	frappe.call({
				// 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_excel",
				// 		args: {
				// 			"acc_manager":frm.doc.acc_manager,
				// 			"month":frm.doc.month,
				// 			"target_service":frm.doc.target_service
				// 		},
				// 		callback: function (r) {
				// 			if (r.message) {
				// 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
				// 				let link = document.createElement("a");
				// 				link.href = window.URL.createObjectURL(blob);
				// 				link.download = r.message.filename;
				// 				document.body.appendChild(link);
				// 				link.click();
				// 				document.body.removeChild(link);
				// 			}
				// 		}
				// 	});
				// }
				// if(frm.doc.acc_manager && !frm.doc.month && !frm.doc.target_service){
				// 	frappe.call({
				// 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_acc_manager",
				// 		args: {
				// 			"acc_manager":frm.doc.acc_manager,
				// 			"month":frm.doc.month,
				// 			"target_service":frm.doc.target_service
				// 		},
				// 		callback: function (r) {
				// 			if (r.message) {
				// 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
				// 				let link = document.createElement("a");
				// 				link.href = window.URL.createObjectURL(blob);
				// 				link.download = r.message.filename;
				// 				document.body.appendChild(link);
				// 				link.click();
				// 				document.body.removeChild(link);
				// 			}
				// 		}
				// 	});
				// }
				// if(!frm.doc.acc_manager && !frm.doc.month && frm.doc.target_service){
				// 	frappe.call({
				// 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_service",
				// 		args: {
				// 			"acc_manager":frm.doc.acc_manager,
				// 			"month":frm.doc.month,
				// 			"target_service":frm.doc.target_service
				// 		},
				// 		callback: function (r) {
				// 			if (r.message) {
				// 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
				// 				let link = document.createElement("a");
				// 				link.href = window.URL.createObjectURL(blob);
				// 				link.download = r.message.filename;
				// 				document.body.appendChild(link);
				// 				link.click();
				// 				document.body.removeChild(link);
				// 			}
				// 		}
				// 	});
				// }
				// if(!frm.doc.acc_manager && frm.doc.month && !frm.doc.target_service){
				// 	frappe.call({
				// 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_month",
				// 		args: {
				// 			"acc_manager":frm.doc.acc_manager,
				// 			"month":frm.doc.month,
				// 			"target_service":frm.doc.target_service
				// 		},
				// 		callback: function (r) {
				// 			if (r.message) {
				// 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
				// 				let link = document.createElement("a");
				// 				link.href = window.URL.createObjectURL(blob);
				// 				link.download = r.message.filename;
				// 				document.body.appendChild(link);
				// 				link.click();
				// 				document.body.removeChild(link);
				// 			}
				// 		}
				// 	});
				// }
				// // if(frm.doc.acc_manager && frm.doc.month && frm.doc.target_service){
				// // 	frappe.call({
				// // 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_excel",
				// // 		args: {
				// // 			"acc_manager":frm.doc.acc_manager,
				// // 			"month":frm.doc.month,
				// // 			"target_service":frm.doc.target_service
				// // 		},
				// // 		callback: function (r) {
				// // 			if (r.message) {
				// // 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
				// // 				let link = document.createElement("a");
				// // 				link.href = window.URL.createObjectURL(blob);
				// // 				link.download = r.message.filename;
				// // 				document.body.appendChild(link);
				// // 				link.click();
				// // 				document.body.removeChild(link);
				// // 			}
				// // 		}
				// // 	});
				// // }
				// if(frm.doc.fiscal_year && frm.doc.quarter&& !frm.doc.date){
				// 	frappe.call({
				// 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_excel_filter",
				// 		args: {
				// 			"fiscal_year":frm.doc.fiscal_year,
				// 			"quarter": frm.doc.quarter,
				// 		},
				// 		callback: function (r) {
				// 			if (r.message) {
				// 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
				// 				let link = document.createElement("a");
				// 				link.href = window.URL.createObjectURL(blob);
				// 				link.download = r.message.filename;
				// 				document.body.appendChild(link);
				// 				link.click();
				// 				document.body.removeChild(link);
				// 			}
				// 		}
				// 	});
				// }
				// if(!frm.doc.fiscal_year&& frm.doc.date){
				// 	frappe.call({
				// 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_date_filter",
				// 		args: {
				// 			"date":frm.doc.date
				// 		},
				// 		callback: function (r) {
				// 			if (r.message) {
				// 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
				// 				let link = document.createElement("a");
				// 				link.href = window.URL.createObjectURL(blob);
				// 				link.download = r.message.filename;
				// 				document.body.appendChild(link);
				// 				link.click();
				// 				document.body.removeChild(link);
				// 			}
				// 		}
				// 	});
				// }
			}

			else if(frm.doc.report_type == "CR: Closure Report"){

				var path_for_cr = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_cr_report";
				
			}
			if (path_for_cr) {
				
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_cr,
					
				});
			}
			else if(frm.doc.report_type == "MR: Monitoring Report" && frm.doc.mr_title=="MR:08 - Closure Follow-Up Report (CLFR)"){

				var path_for_clfr = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_all_closures_excel";
				
			}
			if (path_for_clfr) {
				
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_clfr,
					
				});
			}
			else if(frm.doc.report_type == "MR: Monitoring Report" && frm.doc.mr_title=="MR:09 - REC Project Task Planner (RPTP)"){

				var path_for_rptp = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_rptp_report";
				
			}
			if (path_for_rptp) {
				
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_rptp,
					
				});
			}
			else if(frm.doc.report_type == "MR: Monitoring Report" && frm.doc.mr_title=="MR:10 - Closure Weekly Status Report (CWSR)"){

				var path_for_cwsr = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_cwsr_report";
				var args_for_cwsr = "customer=%(customer)s"
				
			}
			if (path_for_cwsr) {
				
				window.location.href = repl(frappe.request.url +
 
					'?cmd=%(cmd)s&%(args)s',{
					cmd: path_for_cwsr,
					args:args_for_cwsr,
					customer:frm.doc.customer
					
				});
			}
			
			


		},("Action")); 

		frm.add_custom_button(("View"), function () {
			frappe.msgprint("Developer working on it.Kindly select PDF or Excel")
		},("Action")); 




frm.add_custom_button("Project Status Summary View", function() {
    frappe.call({
        method: "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.project_status_summ",
        args: {},
        callback: function(r) {
            if (r.message && r.message.grouped_data) {

                let dialog = new frappe.ui.Dialog({
                    title: "Project Status Summary",
                    size: "extra-large",
                    fields: [
                        {
                            fieldtype: "HTML",
                            fieldname: "project_status_summary",
                            label: __("Project Status Summary")
                        }
                    ]
                });

                let groupedData = r.message.grouped_data;
                let grand_v = 0, grand_fp = 0, grand_sp = 0, grand_psl = 0;
                let summaryCounts = {};

                let htmlContent = `
                    <div style="max-height: 600px; overflow-y: auto;">
                    <table border="1" style="width: 100%; border-collapse: collapse; font-size:13px;">
                        <thead>
                            <tr>
                                <th style="text-align:center; background-color:#0f1568; color:white;">Criteria</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">ID</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">Project Name</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">Sourcing Status</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">V#</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">FP#</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">SP#</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">PSL</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                // Object.keys(groupedData).forEach(function(priority) {
				const priorityOrder = ["High", "Medium", "Low"];
				Object.keys(groupedData)
					.sort((a, b) => priorityOrder.indexOf(a) - priorityOrder.indexOf(b))
					.forEach(function(priority) {
                    let projects = groupedData[priority];
                    let rowspan = projects.length;

                    summaryCounts[priority] = { SP: 0, 'SP/FP': 0, FP: 0, total: 0 };

                    projects.forEach(function(project, index) {
                        
                        let rowStyle = (index % 2 === 1) ? "background-color:#d9d9d9;" : "";

                        htmlContent += `<tr style="${rowStyle}">`;

                        if (index === 0) {
                            htmlContent += `<td rowspan="${rowspan}" style="font-weight:bold; text-align:center; background:#fafafa;">${priority}</td>`;
                        }

                        let tvac = parseFloat(project.tvac) || 0;
                        let tfp = parseFloat(project.tfp) || 0;
                        let tsp = parseFloat(project.tsp) || 0;
                        let tpsl = parseFloat(project.tpsl) || 0;

                        grand_v += tvac;
                        grand_fp += tfp;
                        grand_sp += tsp;
                        grand_psl += tpsl;

                        let source = (project.sourcing_statu || "").trim();
                        if (["SP", "SP/FP", "FP"].includes(source)) {
                            summaryCounts[priority][source] += 1;
                            summaryCounts[priority].total += 1;
                        }

                        htmlContent += `
                            <td>${project.ID}</td>
                            <td>${project.project_name}</td>
                            <td>${project.sourcing_statu || '-'}</td>
                            <td style="text-align:center;">${tvac}</td>
                            <td style="text-align:center;">${tfp}</td>
                            <td style="text-align:center;">${tsp}</td>
                            <td style="text-align:center;">${tpsl}</td>
                        </tr>`;
                    });
                });

                htmlContent += `
                    <tr style="background:#d9edf7; font-weight:bold;">
                        <td colspan="4" style="text-align:center;">Grand Total</td>
                        <td style="text-align:center;">${grand_v.toFixed(0)}</td>
                        <td style="text-align:center;">${grand_fp.toFixed(0)}</td>
                        <td style="text-align:center;">${grand_sp.toFixed(0)}</td>
                        <td style="text-align:center;">${grand_psl.toFixed(0)}</td>
                    </tr>
                `;

                htmlContent += `</tbody></table><br><br>`;

                
                let totalSP = 0, totalSPFP = 0, totalFP = 0, totalAll = 0;

                htmlContent += `
                    <table border="1" style="width:40%; border-collapse: collapse; font-size:13px;">
                        <thead>
                            <tr>
                                <th colspan="1" style="text-align:center; background-color:#0f1568; color:white;">Count of CUSTOMER/PROJECT NAME</th>
                                <th colspan="4" style="text-align:center; background-color:#0f1568; color:white;">Sourcing Status</th>
                            </tr>
                            <tr>
                                <th style="text-align:center; background-color:#0f1568; color:white;">Row Labels</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">SP</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">SP/FP</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">FP</th>
                                <th style="text-align:center; background-color:#0f1568; color:white;">Grand Total</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                Object.keys(summaryCounts).forEach(function(priority, idx) {
                    
                    let rowStyle = (idx % 2 === 1) ? "background-color:#d9d9d9;" : "";
                    let counts = summaryCounts[priority];
                    totalSP += counts.SP;
                    totalSPFP += counts['SP/FP'];
                    totalFP += counts.FP;
                    totalAll += counts.total;

                    htmlContent += `
                        <tr style="${rowStyle}">
                            <td style="text-align:left;">${priority}</td>
                            <td style="text-align:center;">${counts.SP}</td>
                            <td style="text-align:center;">${counts['SP/FP']}</td>
                            <td style="text-align:center;">${counts.FP}</td>
                            <td style="text-align:center; font-weight:bold;">${counts.total}</td>
                        </tr>
                    `;
                });

                htmlContent += `
                    <tr style="background:#d9edf7; font-weight:bold;">
                        <td style="text-align:center;">Grand Total</td>
                        <td style="text-align:center;">${totalSP}</td>
                        <td style="text-align:center;">${totalSPFP}</td>
                        <td style="text-align:center;">${totalFP}</td>
                        <td style="text-align:center;">${totalAll}</td>
                    </tr>
                `;

                htmlContent += `</tbody></table></div>`;

                dialog.fields_dict['project_status_summary'].html(htmlContent);
                dialog.show();
            }
        }
    });
}, "Action");

frm.add_custom_button("Update Task", function() {

frappe.call({
	"method":"teampro.custom.update_task_psotions_count_hourly"
})

}, "Action")

frm.add_custom_button("Update Project", function() {

frappe.call({
	"method":"teampro.custom.update_proj_positions_count_hourly"
})

}, "Action")



	},
	// date(frm){
	// 	frm.set_value("fiscal_year","")
	// },
	fiscal_year(frm){
		frm.set_value("date","")
	},
	// onload(frm) {
	// 	frappe.breadcrumbs.add("Formatted Reports  Download","Teampro");

	// },
	mr_title(frm){
		if(frm.doc.mr_title=="MR:01 – Sales Follow-Up Report"||frm.doc.mr_title=="MR:02 – Customer Follow-Up Report (CFR)"||frm.doc.mr_title=="MR:06 – Project Task Issue Status Report (PTISR)"){
			frappe.msgprint("Currently this report in working")
		}
	},
	dm_title(frm){
		if(frm.doc.dm_title=="DM:01 – DPR Vs. DSR : REC"||frm.doc.dm_title=="DM:02 – DPR Vs. DSR : DND"||frm.doc.dm_title=="DM:03 – DPR Vs. DSR : BCS"||frm.doc.dm_title=="DM:04 – DPR Vs. DSR : IT. DV"||frm.doc.dm_title=="DM:05 – DPR Vs. DSR : IT. CS"||frm.doc.dm_title=="DM:06 – DPR Vs. DSR : TFP"||frm.doc.dm_title=="DM:07 – DPR Vs. DSR : R&S (T)"||frm.doc.dm_title=="DM:08 – DPR Vs. DSR : R&S (D)"||frm.doc.dm_title=="DM:09 – DPR Vs. DSR : H&A"||frm.doc.dm_title=="DM:10 – DPR Vs. DSR : F&A"){
			frappe.msgprint("Currently this report in working")
		}
	},
	print(frm){
		
		if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:04 – Batch Status Report (BSR)"){
			var print_format ="BCS - Batch Status Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:06 – Collection Pending Report – SI Outstanding (CPR)"){
			var print_format ="Sales Invoice Outstanding Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:01 – Opportunity Status Report (OSR)"){
			var print_format ="Opportunity Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:05 – To Be Billed - SO Outstanding (TBB)"){
			var print_format ="Sales Invoice Outstanding Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:02 – Project Status Report –(PSR - R)" && frm.doc.services_psr=="REC-I"){
			var print_format ="Project Status Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:03 – Project Task Status Report – REC (PTSR - R)"){
			var print_format ="Project Task Status Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type=="PR: Primary Reports" && frm.doc.primary_reports=="PR:03 – Closure Status Report (CSR)"){
			var print_format ="Closure Count - Status Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type=="MR: Monitoring Report" && frm.doc.primary_reports=="MR:05 – Closure Detailed Status Report (CDSR)"){
			var print_format ="Closure Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:07 – TODO Status Report"){
			var print_format ="ToDO Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.primary_reports=="Appointment Schedule Report"){
			var print_format ="Appointment Schedule Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.primary_reports=="Appointment Taken Report"){
			var print_format ="Appointment Taken Report";
			var f_name = frm.doc.name
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Formatted Reports  Download")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		}
		if (frm.doc.report_type == 'PR: Primary Reports' &&
			frm.doc.primary_reports == "PR:02 – Project Status Report –(PSR - R)" &&
			frm.doc.services_psr == "IT-SW") {
   
			var path = "teampro.teampro.doctype.formatted_reports__download.formatted_report_download_pdf.download_pdf";
		
			// If both fields are empty, prevent download and show a message
			// if (!frm.doc.customer && !frm.doc.project) {
			// 	frappe.msgprint(__('Please select either a Customer or a Project to generate the report.'));
			// 	return;
			// }
		
			var args = [];

			if (frm.doc.customer) {
				
				args.push("customer=" + encodeURIComponent(frm.doc.customer));
			}
			if (frm.doc.project) {
				args.push("project=" + encodeURIComponent(frm.doc.project));
			}
		
			if (path) {
				window.location.href = frappe.request.url + '?cmd=' + encodeURIComponent(path) + '&' + args.join("&");
			}
		}	
	},
	download: function (frm) {
		if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:04 – Batch Status Report (BSR)") {
			if(!frm.doc.batch_customer && !frm.doc.batch){
			var path_for_bsr = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_bcs_report";
			}
			else if(frm.doc.batch_customer && !frm.doc.batch){
				var path_for_bsr_cust = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_bcs_report_cust";
			}
			else if(frm.doc.batch && !frm.doc.batch_customer){
				var path_for_bsr_batch = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_bcs_report_batch";
			}
		
		}
		else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:06 – Collection Pending Report – SI Outstanding (CPR)") {
			var si_path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_sales_invoice_outstanding_report";
			var args = "account_manager=%(account_manager)s&delivery_manager=%(delivery_manager)s&service=%(service)s&sompany=%(company)s"
		}
		if (si_path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: si_path,
				args: args,
				account_manager : frm.doc.account_manager,
				delivery_manager: frm.doc.delivery_manager,
				service: frm.doc.service,
				company: frm.doc.company
			});
		}
		
		else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:01 – Opportunity Status Report (OSR)") {
			var opp_path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.opportunity_excel_report"
			var args = "opportunity_owner=%(opportunity_owner)s&opp_am=%(opp_am)s&opp_service=%(opp_service)s"
		}
		if (opp_path){
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
					cmd: opp_path,
					args: args,
					opportunity_owner: frm.doc.opportunity_owner,
					opp_am: frm.doc.opp_am,
					opp_service: frm.doc.opp_service
				}
			)
		}
		else if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:03 – Project Task Status Report – REC (PTSR - R)") {
			// var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PTSR"
			var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports_download.download_PTSR_new"
		}
		else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports=="PR:02 – Project Status Report –(PSR - R)" && frm.doc.services_psr=="REC-I") {
			if(!frm.doc.customer && !frm.doc.project){
			// var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR";
			var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports_download.download_PSR_new";
			}
			else if(frm.doc.customer && !frm.doc.project){
			var path_for_psr_cust = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR_customer";	
			var args_for_psr_cust="customer=%(customer)s"
			}	
			else if(frm.doc.project && !frm.doc.customer){
				var path_for_psr_proj = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR_proj";	
				var args_for_psr_proj="project=%(project)s"
				}	
			else if(frm.doc.project && frm.doc.customer){
				var path_for_psr_both = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR_both";	
				var args_for_psr_both="project=%(project)s&customer=%(customer)s"
				}		

		}
		else if (frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR:05 – To Be Billed - SO Outstanding (TBB)") {
			var so_path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_sales_order_outstanding_report";
			var args = "account_manager=%(account_manager)s&delivery_manager=%(delivery_manager)s&service=%(service)s&sompany=%(company)s"
		}
		if (so_path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: so_path,
				args: args,
				account_manager : frm.doc.account_manager,
				delivery_manager: frm.doc.delivery_manager,
				service: frm.doc.service,
				company: frm.doc.company
			});
		}
		else if (frm.doc.report_type=="PR: Primary Reports" && frm.doc.primary_reports=="PR:03 – Closure Status Report (CSR)") {
			if (frm.doc.so_validate==1){
				var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_status_report";
			}
			else if(frm.doc.so_status==0 && frm.doc.so_validate==0){
				var path= "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_status_report_so_false";
			}
			else if(frm.doc.so_status==1){
				var path= "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_status_report_so_true";
			}
		}
		else if (frm.doc.report_type=="MR: Monitoring Report" && frm.doc.mr_title=="MR:05 – Closure Detailed Status Report (CDSR)") {
			var path_for_clr = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_closure_report";
			var args_for_clr="so_status=%(so_status)s&so_validate=%(so_validate)s"
		}
		else if (frm.doc.primary_reports == "Appointment Schedule Report") {
			var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.app_schedule_excel_report"
		}
		else if (frm.doc.primary_reports == "Appointment Taken Report") {
			var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.app_taken_excel_report"
		}
		else if (frm.doc.report_type == 'MR: Monitoring Report' && frm.doc.mr_title=="MR:07 – TODO Status Report") {

			var path_for_todo = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_todo_report"
			var args = 'allocated_to=%(allocated_to)s'
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s', {
					cmd: path
			});
		}
		if (path_for_todo) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path_for_todo,
				args: args,
				allocated_to : frm.doc.allocated_to,

			});
		}
		if (path_for_bsr) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s', {
				cmd: path_for_bsr,
				// args: args_for_bsr,
				// batch_customer : frm.doc.batch_customer,
				// batch:frm.doc.batch

			});
		}
		if (path_for_bsr_cust) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s', {
				cmd: path_for_bsr_cust,

			});
		}
		if (path_for_bsr_batch) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s', {
				cmd: path_for_bsr_batch,

			});
		}
		if (path_for_psr_cust) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path_for_psr_cust,
				args: args_for_psr_cust,
				customer : frm.doc.customer,
				// project:frm.doc.project

			});
		}
		if (path_for_psr_proj) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path_for_psr_proj,
				args: args_for_psr_proj,
				project : frm.doc.project,

			});
		}
		if (path_for_psr_both) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path_for_psr_both,
				args: args_for_psr_both,
				project : frm.doc.project,
				customer : frm.doc.customer,

			});
		}
		if (path_for_clr) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path_for_clr,
				args: args_for_clr,
				so_status:frm.doc.so_status,
				so_validate:frm.doc.so_validate

			});
		}
		else if (frm.doc.report_type == 'PR: Primary Reports' &&
			frm.doc.primary_reports == "PR:02 – Project Status Report –(PSR - R)" &&
			frm.doc.services_psr == "IT-SW") {
   
			// var path = "teampro.teampro.doctype.formatted_reports__download.formatted_report_it_sw.download";
			var path = "teampro.teampro.doctype.formatted_reports__download.formatted_report_it_sw.download_new";
		
			var args = [];

			if (frm.doc.customer) {
				
				args.push("customer=" + encodeURIComponent(frm.doc.customer));
			}
			if (frm.doc.project) {
				args.push("project=" + encodeURIComponent(frm.doc.project));
			}
		
			if (path) {
				window.location.href = frappe.request.url + '?cmd=' + encodeURIComponent(path) + '&' + args.join("&");
			}
		}
		else if(frm.doc.report_type == 'PR: Primary Reports' && frm.doc.primary_reports == "PR.07 – Target Status Report"){
			if(!frm.doc.acc_manager && !frm.doc.month && !frm.doc.target_service){
				frappe.call({
					method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_excel",
					args: {
						"acc_manager":frm.doc.acc_manager,
						"month":frm.doc.month,
						"target_service":frm.doc.target_service
					},
					callback: function (r) {
						if (r.message) {
							let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
							let link = document.createElement("a");
							link.href = window.URL.createObjectURL(blob);
							link.download = r.message.filename;
							document.body.appendChild(link);
							link.click();
							document.body.removeChild(link);
						}
					}
				});
			}
			if(frm.doc.acc_manager && !frm.doc.month && !frm.doc.target_service){
				frappe.call({
					method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_acc_manager",
					args: {
						"acc_manager":frm.doc.acc_manager,
						"month":frm.doc.month,
						"target_service":frm.doc.target_service
					},
					callback: function (r) {
						if (r.message) {
							let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
							let link = document.createElement("a");
							link.href = window.URL.createObjectURL(blob);
							link.download = r.message.filename;
							document.body.appendChild(link);
							link.click();
							document.body.removeChild(link);
						}
					}
				});
			}
			if(!frm.doc.acc_manager && !frm.doc.month && frm.doc.target_service){
				frappe.call({
					method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_service",
					args: {
						"acc_manager":frm.doc.acc_manager,
						"month":frm.doc.month,
						"target_service":frm.doc.target_service
					},
					callback: function (r) {
						if (r.message) {
							let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
							let link = document.createElement("a");
							link.href = window.URL.createObjectURL(blob);
							link.download = r.message.filename;
							document.body.appendChild(link);
							link.click();
							document.body.removeChild(link);
						}
					}
				});
			}
			if(!frm.doc.acc_manager && frm.doc.month && !frm.doc.target_service){
				frappe.call({
					method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_month",
					args: {
						"acc_manager":frm.doc.acc_manager,
						"month":frm.doc.month,
						"target_service":frm.doc.target_service
					},
					callback: function (r) {
						if (r.message) {
							let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
							let link = document.createElement("a");
							link.href = window.URL.createObjectURL(blob);
							link.download = r.message.filename;
							document.body.appendChild(link);
							link.click();
							document.body.removeChild(link);
						}
					}
				});
			}
			// if(frm.doc.acc_manager && frm.doc.month && frm.doc.target_service){
			// 	frappe.call({
			// 		method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_excel",
			// 		args: {
			// 			"acc_manager":frm.doc.acc_manager,
			// 			"month":frm.doc.month,
			// 			"target_service":frm.doc.target_service
			// 		},
			// 		callback: function (r) {
			// 			if (r.message) {
			// 				let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
			// 				let link = document.createElement("a");
			// 				link.href = window.URL.createObjectURL(blob);
			// 				link.download = r.message.filename;
			// 				document.body.appendChild(link);
			// 				link.click();
			// 				document.body.removeChild(link);
			// 			}
			// 		}
			// 	});
			// }
			if(frm.doc.fiscal_year && frm.doc.quarter&& !frm.doc.date){
				frappe.call({
					method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_excel_filter",
					args: {
						"fiscal_year":frm.doc.fiscal_year,
						"quarter": frm.doc.quarter,
					},
					callback: function (r) {
						if (r.message) {
							let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
							let link = document.createElement("a");
							link.href = window.URL.createObjectURL(blob);
							link.download = r.message.filename;
							document.body.appendChild(link);
							link.click();
							document.body.removeChild(link);
						}
					}
				});
			}
			if(!frm.doc.fiscal_year&& frm.doc.date){
				frappe.call({
					method: "teampro.teampro.doctype.formatted_reports__download.target_report.download_date_filter",
					args: {
						"date":frm.doc.date
					},
					callback: function (r) {
						if (r.message) {
							let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
							let link = document.createElement("a");
							link.href = window.URL.createObjectURL(blob);
							link.download = r.message.filename;
							document.body.appendChild(link);
							link.click();
							document.body.removeChild(link);
						}
					}
				});
			}
			
		}	
	}
});
