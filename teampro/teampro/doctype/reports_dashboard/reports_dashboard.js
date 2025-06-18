// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Reports Dashboard", {
	
	download(frm) {
        
        if (frm.doc.report_title == 'consolidated Check Report')

            {
   
			var path = "teampro.teampro.doctype.reports_dashboard.check_status_report.check_status_report";
			var args = [];

			if (path) {
				window.location.href = frappe.request.url + '?cmd=' + encodeURIComponent(path) + '&' + args.join("&");
			}
		}
		if (frm.doc.report_title == 'Daily Status Report')

            {
   
			var path = "teampro.teampro.doctype.reports_dashboard.daily_status_report.daily_status_report";
			var args = [];

			if (path) {
				window.location.href = frappe.request.url + '?cmd=' + encodeURIComponent(path) + '&' + args.join("&");
			}
		}
		if (frm.doc.report_title == 'Issue Report')

            {
   
			var path = "teampro.teampro.doctype.reports_dashboard.issue_report.issue_report";
			var args = [];

			if (path) {
				window.location.href = frappe.request.url + '?cmd=' + encodeURIComponent(path) + '&' + args.join("&");
			}
		}		
	}
});
