// Copyright (c) 2024, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Monthly Energy Point  Non Conformity", {
	to_date(frm) {
        frappe.call({
            method: "teampro.teampro.doctype.monthly_energy_point__non_conformity.monthly_energy_point__non_conformity.mo_epnc",
            args: {
                emp: frm.doc.employee_id,
                from_date: frm.doc.from_date,
                to_date: frm.doc.to_date,
                emp_name: frm.doc.employee_name
            },
            callback: function (r) {
                frm.fields_dict.html.$wrapper.empty().append(r.message)
            }
        })
    
	},

});
