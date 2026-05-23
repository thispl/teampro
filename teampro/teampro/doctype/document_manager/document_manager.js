// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Document Manager", {
	refresh(frm) {

	},
});

frappe.ui.form.on('Document Proof', {
    
    category:function(frm,cdt,cdn){
       let row = frappe.get_doc(cdt, cdn);
       if (row.category=="Non Renewable") { 
           frappe.model.set_value(cdt, cdn, 'status', 'Active');

       }
    },

    expiry_date: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.expiry_date) {
            const today = frappe.datetime.get_today();
            const age = frappe.datetime.get_day_diff(row.expiry_date, today);
            frappe.model.set_value(cdt, cdn, 'expiry_age', Math.abs(age));

            if (frappe.datetime.get_diff(today, row.expiry_date) > 0) {
                
                frappe.model.set_value(cdt, cdn, 'status', 'Inactive');
            } else {
                frappe.model.set_value(cdt, cdn, 'status', 'Active');
            }
        } else {
            frappe.model.set_value(cdt, cdn, 'expiry_age', null);
            frappe.model.set_value(cdt, cdn, 'status', 'Active');
        }
        frm.refresh_field('document_manager');
    },

    validate: function(frm) {
        frm.doc.document_manager.forEach(row => {
            if (row.category === 'Renewable') {
                if (!row.expiry_date) {
                    frappe.msgprint(`Expiry Date is mandatory for renewable category in row ${row.idx}`);
                    frappe.validated = false;
                }
            } else {
                frappe.model.set_value(row.doctype, row.name, 'status', 'Active');
            }
        });
    }
});
