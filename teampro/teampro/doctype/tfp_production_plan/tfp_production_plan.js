// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("TFP Production Plan", {
	download(frm) {
        // var print_format ="TFP Production Plan";
		// 		var f_name = frm.doc.name
		// 		window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
		// 			+ "doctype=" + encodeURIComponent("TFP Production Plan")
		// 			+ "&name=" + encodeURIComponent(f_name)
		// 			+ "&trigger_print=1"
		// 			+ "&format=" + print_format
		// 			+ "&no_letterhead=0"
		// 		));
		var path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_production_plan_excel"
            if (path) {
				window.location.href = repl(frappe.request.url +
					'?cmd=%(cmd)s', {
						cmd: path
				});
			}
	},
    // refresh(frm){
    //     frm.add_custom_button(__("Download Excel"), function () {
    //         var path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_production_plan_excel"
    //         if (path) {
	// 			window.location.href = repl(frappe.request.url +
	// 				'?cmd=%(cmd)s', {
	// 					cmd: path
	// 			});
	// 		}
    //     })
        
    // }
});
