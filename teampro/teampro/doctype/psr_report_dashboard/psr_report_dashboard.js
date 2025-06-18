// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("PSR Report Dashboard", {
	download(frm) {
        if (frm.doc.report=="Daily PSR Report") {
            var path = 'teampro.teampro.doctype.psr_report_dashboard.psr_report_dashboard.download';
        }
        else if(frm.doc.report=="Daily PSR Report(Hour)"){
            var path = 'teampro.teampro.doctype.psr_report_dashboard.psr_report_hour.download';
        }
        if (path) {
            window.location.href = repl(frappe.request.url +
                '?cmd=%(cmd)s', {
                cmd: path,
            });
        }
	},
});
