// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Target ', {
	period: function(frm) {
		frappe.db.get_value('Salary Structure Assignment', {employee: frm.doc.employee_id}, 'base')
			.then(r => {
				// const base = r.message.base;
				console.log(r.message.base)
				const qft = r.message.base*10
				const mft = qft/3
				const aft = qft*4
				console.log(qft)
				console.log(mft)
				console.log(aft)
				cur_frm.clear_table("target");
				if(frm.doc.period=="Quarterly"){
					frm.add_child('target',{
						target:qft,
						data_1:"FT"
					});
				}
				if(frm.doc.period=="Monthly"){
					frm.add_child('target',{
						target:mft,
						data_1:"FT"
					});
					
				}
				if(frm.doc.period=="Annually"){
					frm.add_child('target',{
						target:aft,
						data_1:"FT"
					});
				}
				frm.refresh_field("target")
		})
		
	},
})
