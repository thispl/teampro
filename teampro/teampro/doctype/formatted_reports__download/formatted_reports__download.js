// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Formatted Reports  Download", {
	refresh(frm){
		// frm.add_custom_button(("Test Download"),function(){
				// only acc manger and fiscal year filter
					// frappe.call({
					// 	method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_manager_individual",
					// 	args: {
					// 		"quarter":frm.doc.quarter,
					// 		"fiscal_year":frm.doc.fiscal_year,
							
					// 	},
					// 	callback: function (r) {
					// 		if (r.message) {
					// 			let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
					// 			let link = document.createElement("a");
					// 			link.href = window.URL.createObjectURL(blob);
					// 			link.download = r.message.filename;
					// 			document.body.appendChild(link);
					// 			link.click();
					// 			document.body.removeChild(link);
					// 		}
					// 	}
					// });
				// only fiscal year filter
					// frappe.call({
					// 	method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_manager",
					// 	args: {
					// 		"fiscal_year":frm.doc.fiscal_year
					// 	},
					// 	callback: function (r) {
					// 		if (r.message) {
					// 			let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
					// 			let link = document.createElement("a");
					// 			link.href = window.URL.createObjectURL(blob);
					// 			link.download = r.message.filename;
					// 			document.body.appendChild(link);
					// 			link.click();
					// 			document.body.removeChild(link);
					// 		}
					// 	}
					// });
				// without account manager and with quarter and fiscal year filter
					// frappe.call({
					// 	method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_manager_quarter",
					// 	args: {
					// 		"quarter":frm.doc.quarter,
					// 		"fiscal_year":frm.doc.fiscal_year,
							
					// 	},
					// 	callback: function (r) {
					// 		if (r.message) {
					// 			let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
					// 			let link = document.createElement("a");
					// 			link.href = window.URL.createObjectURL(blob);
					// 			link.download = r.message.filename;
					// 			document.body.appendChild(link);
					// 			link.click();
					// 			document.body.removeChild(link);
					// 		}
					// 	}
					// });
					// acc,fiscalyear,quarter filter
						// frappe.call({
						// 	method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc",
						// 	args: {
						// 		"quarter":frm.doc.quarter,
						// 		"fiscal_year":frm.doc.fiscal_year,
						// 		"acc_manager":frm.doc.acc_manager
						// 	},
						// 	callback: function (r) {
						// 		if (r.message) {
						// 			let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
						// 			let link = document.createElement("a");
						// 			link.href = window.URL.createObjectURL(blob);
						// 			link.download = r.message.filename;
						// 			document.body.appendChild(link);
						// 			link.click();
						// 			document.body.removeChild(link);
						// 		}
						// 	}
						// });
					// acc,fiscalyear,quarter,month
						// frappe.call({
						// 	method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_acc_month",
						// 	args: {
						// 		"quarter":frm.doc.quarter,
						// 		"fiscal_year":frm.doc.fiscal_year,
						// 		"acc_manager":frm.doc.acc_manager,
						// 		"month":frm.doc.month
						// 	},
						// 	callback: function (r) {
						// 		if (r.message) {
						// 			let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
						// 			let link = document.createElement("a");
						// 			link.href = window.URL.createObjectURL(blob);
						// 			link.download = r.message.filename;
						// 			document.body.appendChild(link);
						// 			link.click();
						// 			document.body.removeChild(link);
						// 		}
						// 	}
						// });
					// fiscalyear,month,quarter
						// frappe.call({
						// 	method: "teampro.teampro.doctype.formatted_reports__download.updated_target_report.download_quarter_month_report",
						// 	args: {
						// 		"quarter":frm.doc.quarter,
						// 		"fiscal_year":frm.doc.fiscal_year,
						// 		"acc_manager":frm.doc.acc_manager,
						// 		"month":frm.doc.month
						// 	},
						// 	callback: function (r) {
						// 		if (r.message) {
						// 			let blob = new Blob([new Uint8Array(r.message.content)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
						// 			let link = document.createElement("a");
						// 			link.href = window.URL.createObjectURL(blob);
						// 			link.download = r.message.filename;
						// 			document.body.appendChild(link);
						// 			link.click();
						// 			document.body.removeChild(link);
						// 		}
						// 	}
						// });
		// })
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
				console.log("inside of if")
	
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
				console.log("inside of path")
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s&%(args)s', {
					cmd: path_for_todo,
					args: args,
					allocated_to : frm.doc.allocated_to,
	
				});
			}
			if (path_for_bsr) {
				console.log("inside of path")
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_bsr,
					// args: args_for_bsr,
					// batch_customer : frm.doc.batch_customer,
					// batch:frm.doc.batch
	
				});
			}
			if (path_for_bsr_cust) {
				console.log("inside of path")
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
					cmd: path_for_bsr_cust,
	
				});
			}
			if (path_for_bsr_batch) {
				console.log("inside of path")
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
				console.log("inside of path")
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
					console.log("hi1")
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
					console.log("hi2")
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
					console.log("hi3")
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
					console.log("hi4")
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
						console.log("hi5")
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
						console.log("hi6")
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
						console.log("hi7")
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
						console.log("hi8")
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
						console.log("hi9")
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
		},("Action")); 
		frm.add_custom_button(("View"), function () {
			frappe.msgprint("Developer working on it.Kindly select PDF or Excel")
		},("Action")); 
	},
	// date(frm){
	// 	frm.set_value("fiscal_year","")
	// },
	fiscal_year(frm){
		frm.set_value("date","")
	},
	onload(frm) {
		frappe.breadcrumbs.add("Formatted Reports  Download","Teampro");

	},
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
			var path = "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.download_PSR";
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
			console.log("inside of if")

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
			console.log("inside of path")
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path_for_todo,
				args: args,
				allocated_to : frm.doc.allocated_to,

			});
		}
		if (path_for_bsr) {
			console.log("inside of path")
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s', {
				cmd: path_for_bsr,
				// args: args_for_bsr,
				// batch_customer : frm.doc.batch_customer,
				// batch:frm.doc.batch

			});
		}
		if (path_for_bsr_cust) {
			console.log("inside of path")
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s', {
				cmd: path_for_bsr_cust,

			});
		}
		if (path_for_bsr_batch) {
			console.log("inside of path")
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
			console.log("inside of path")
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
				console.log("hello")
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
