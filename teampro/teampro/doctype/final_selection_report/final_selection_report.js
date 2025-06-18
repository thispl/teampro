// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Final Selection Report", {
    download: function(frm) {
        if (frm.doc.report === 'Interview Final Selection') {
            var path = "teampro.teampro.doctype.final_selection_report.final_report.download";
            var args = 'project=%(project)s'
        }
        if(path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s',{
				cmd: path,
				args: args,
                project:frm.doc.project,
			});
		}
    }
});
