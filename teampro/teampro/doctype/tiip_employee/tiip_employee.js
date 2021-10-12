// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TIIP Employee', {
	refresh: function(frm) {
		// frm.set_value("from_date", frappe.datetime.add_months(frappe.datetime.get_today(),-1))
		// frm.set_value("to_date", frappe.datetime.get_today())
		if(!frm.doc.__islocal){
			// frappe.model.clear_table(frm.doc, "sales_invoice");
			
			frappe.model.clear_table(frm.doc, "analytical_section");
			refresh_field("sales_invoice")
			refresh_field("analytical_section")
		frm.call('get_all_employees')
// 		.then(r => {
// 			var total = 0 
// 			var out = 0 
// 		$.each(frm.doc.sales_invoice, function (i, d) {
// 			total += Number(d.total_sc)
// 			out += Number(d.outstanding_amount)
			

// 		})
// 		refresh_field("sales_invoice")
// 		refresh_field("analytical_section")
// 		frm.set_value("achieved",total)
// 		frm.set_value("outstanding",out)
// 		frm.save()
// 		})	
	}
},
onload:function(frm,cdt,cdn){
	$(".grid-add-row").hide();
	// cur_frm.fields_dict [sales_invoice].grid.wrapper.find(`.grid-add-row`).hide();
	// cur_frm.fields_dict[sales_invoice].grid.wrapper.find(`.grid-insert-row`).hide();
},
to_date:function(frm){
	
	if (frm.doc.to_date){
		frappe.model.clear_table(frm.doc, "sales_invoice");

		frm.set_value("yearly","")
		frm.set_value("quarterly","")
		frm.set_value("half_yearly","")
		frm.set_value("monthly","")
		console.log("hi")
		
		frm.call('get_data')
		.then(r => {
						var total = 0 
						var out = 0 
					$.each(frm.doc.sales_invoice, function (i, d) {
						total += Number(d.total_sc.toFixed(2))
						out += Number(d.outstanding_amount.toFixed(2))
						
			
					})
					refresh_field("sales_invoice")
					refresh_field("analytical_section")
					frm.set_value("achieved",total)
					frm.set_value("outstanding",out)
					frm.save()
					})	
		// frm.save()
	}
	else{
		frappe.model.clear_table(frm.doc, "sales_invoice");
		frm.set_value("achieved","")
		frm.set_value("outstanding","")
	}
	
	
	
},
monthly:function(frm){
	if (frm.doc.monthly){
		
		frm.set_value("from_date","")
		frm.set_value("to_date","")
		frm.set_value("yearly","")
		frm.set_value("quarterly","")
		frm.set_value("half_yearly","")
		frm.call('get_data_monthly')
		.then(r => {
						var total = 0 
						var out = 0 
					$.each(frm.doc.sales_invoice, function (i, d) {
						total += Number(d.total_sc.toFixed(2))
						out += Number(d.outstanding_amount.toFixed(2))
						
			
					})
					refresh_field("sales_invoice")
					refresh_field("analytical_section")
					frm.set_value("achieved",total)
					frm.set_value("outstanding",out)
					frm.save()
					})	
	
	// frm.save()
	}
	else{
		frappe.model.clear_table(frm.doc, "sales_invoice");
		frm.set_value("achieved","")
		frm.set_value("outstanding","")
	}
},
quarterly:function(frm){
	if (frm.doc.quarterly){
		
		frm.set_value("from_date","")
		frm.set_value("to_date","")
		frm.set_value("yearly","")
		frm.set_value("monthly","")
		frm.set_value("half_yearly","")
		frm.call('get_data_quarterly')
		.then(r => {
						var total = 0 
						var out = 0 
					$.each(frm.doc.sales_invoice, function (i, d) {
						total += Number(d.total_sc.toFixed(2))
						out += Number(d.outstanding_amount.toFixed(2))
						
			
					})
					refresh_field("sales_invoice")
					refresh_field("analytical_section")
					frm.set_value("achieved",total)
					frm.set_value("outstanding",out)
					frm.save()
					})	
	
	// frm.save()
	}
	else{
		frappe.model.clear_table(frm.doc, "sales_invoice");
		frm.set_value("achieved","")
		frm.set_value("outstanding","")
	}
},
half_yearly:function(frm){
	if (frm.doc.half_yearly){
		
		frm.set_value("from_date","")
		frm.set_value("to_date","")
		frm.set_value("yearly","")
		frm.set_value("monthly","")
		frm.set_value("quarterly","")
		frm.call('get_data_half_yearly')
		.then(r => {
						var total = 0 
						var out = 0 
					$.each(frm.doc.sales_invoice, function (i, d) {
						total += Number(d.total_sc.toFixed(2))
						out += Number(d.outstanding_amount.toFixed(2))
						
			
					})
					refresh_field("sales_invoice")
					refresh_field("analytical_section")
					frm.set_value("achieved",total)
					frm.set_value("outstanding",out)
					frm.save()
					})	
	
	// frm.save()
	}
	else{
		frappe.model.clear_table(frm.doc, "sales_invoice");
		frm.set_value("achieved","")
		frm.set_value("outstanding","")
	}
},
yearly:function(frm){
	if (frm.doc.yearly){
		
		frm.set_value("from_date","")
		frm.set_value("to_date","")
		frm.set_value("half_yearly","")
		frm.set_value("monthly","")
		frm.set_value("quarterly","")
		frm.call('get_data_yearly')
		.then(r => {
						var total = 0 
						var out = 0 
					$.each(frm.doc.sales_invoice, function (i, d) {
						total += Number(d.total_sc.toFixed(2))
						out += Number(d.outstanding_amount.toFixed(2))
						
			
					})
					refresh_field("sales_invoice")
					refresh_field("analytical_section")
					frm.set_value("achieved",total)
					frm.set_value("outstanding",out)
					frm.save()
					})	
	
	// frm.save()
	}
	else{
		frappe.model.clear_table(frm.doc, "sales_invoice");
		frm.set_value("achieved","")
		frm.set_value("outstanding","")
	}
}
});







