// Copyright (c) 2022, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Balance Report', {
	// refresh: function(frm) {

	// }
	onload(frm){
		
		frm.call('get_data').then(r=>{
			if (r.message ) {
				frm.fields_dict.html.$wrapper.empty().append(r.message)
				// frm.set_value("overtime_hours","16")
			}

		})	
		
	}
	
});
