// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Salary Register Dashboard", {
	// refresh(frm) {

	// },
    download(frm) {
        if (frm.doc.reports == "Salary Register Report"){
            if (frm.doc.from_date && frm.doc.to_date) {// Ensure both date and shift are present
                var path = 'teampro.teampro.doctype.salary_register_dashboard.salary_register_dashboard.download';
                var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
                    "&to_date=" + encodeURIComponent(frm.doc.to_date);  
            }
            if (path && args) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args: args,
                    from_date:frm.doc.from_date,
                    to_date:frm.doc.to_date
                });
            }
        }   
		if (frm.doc.reports == "Bank Upload"){
            if (frm.doc.reports) {// Ensure both date and shift are present
                var path = 'teampro.teampro.doctype.salary_register_dashboard.bank_report.get_template';
                var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
                    "&to_date=" + encodeURIComponent(frm.doc.to_date);  
            }
            if (path && args) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                });
            }
        }
        if (frm.doc.reports == "PF Upload Sheet"){
            if (frm.doc.reports) {// Ensure both date and shift are present
                var path = 'teampro.teampro.doctype.salary_register_dashboard.PF.text_template';
                var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
                    "&to_date=" + encodeURIComponent(frm.doc.to_date);  
            }
            if (path && args) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args: args,
                    from_date:frm.doc.from_date,
                    to_date:frm.doc.to_date,
                });
            }
        }
        
	},
});
// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Salary Register Dashboard", {
// 	download(frm) {
//         if (frm.doc.from_date && frm.doc.to_date) {// Ensure both date and shift are present
//             var path = 'teampro.teampro.doctype.salary_register_report.salary_register_report.download';
//             var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
//                 "&to_date=" + encodeURIComponent(frm.doc.to_date);  
//         }
// 		if (path && args) {
// 			window.location.href = repl(frappe.request.url +
// 				'?cmd=%(cmd)s&%(args)s', {
// 				cmd: path,
// 				args: args,
// 				from_date:frm.doc.from_date,
// 				to_date:frm.doc.to_date
// 			});
// 		}

// 	},
// });
