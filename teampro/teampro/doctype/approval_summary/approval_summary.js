// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Approval Summary', {
	refresh: function(frm) {
		frm.disable_save()
		frm.trigger("data_fetch")

	$('*[data-fieldname="leave_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="leave_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="leave_approval"]').find('.grid-add-row').remove()

	$('*[data-fieldname="attendance_request_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="attendance_request_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="attendance_request_approval"]').find('.grid-add-row').remove()

	$('*[data-fieldname="expense_claim_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="expense_claim_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="expense_claim_approval"]').find('.grid-add-row').remove()

	
	$('*[data-fieldname="sales_order_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="sales_order_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="sales_order_approval"]').find('.grid-add-row').remove()


	$('*[data-fieldname="sales_invoice_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="sales_invoice_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="sales_invoice_approval"]').find('.grid-add-row').remove()


	$('*[data-fieldname="purchase_order_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="purchase_order_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="purchase_order_approval"]').find('.grid-add-row').remove()
	
	$('*[data-fieldname="purchase_invoice_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="purchase_invoice_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="purchase_invoice_approval"]').find('.grid-add-row').remove()

	$('*[data-fieldname="purchase_receipt_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="purchase_receipt_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="purchase_receipt_approval"]').find('.grid-add-row').remove()
	
	$('*[data-fieldname="material_request_approval"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="material_request_approval"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="material_request_approval"]').find('.grid-add-row').remove()

	if (frappe.user.has_role(['HR Manager'])){
		frm.fields_dict["leave_approval"].grid.add_custom_button(__('Reject'),
		function () {
			if(frm.doc.leave_approval){
				$.each(frm.doc.leave_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Leave Application",
							name: d.application_no,
							workflow_state: 'Rejected'
						}).then(r => {
							frm.get_field("leave_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}			
		}).addClass('btn-danger')


		frm.fields_dict["leave_approval"].grid.add_custom_button(__('Approve'),
		function () {
			if(frm.doc.leave_approval){
				$.each(frm.doc.leave_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Leave Application",
							name: d.application_no,
							workflow_state : "Approved",
						}).then(r => {
							frm.get_field("leave_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}
		}).css({'color':'white','background-color':"#009E60","margin-left": "10px", "margin-right": "10px"});
		
		frm.fields_dict["attendance_request_approval"].grid.add_custom_button(__('Reject'),
		function () {
			if(frm.doc.attendance_request_approval){
				$.each(frm.doc.attendance_request_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Attendance Request",
							name: d.attendance_request_number,
							workflow_state: 'Rejected'
						}).then(r => {
							frm.get_field("attendance_request_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}			
		}).addClass('btn-danger')


		frm.fields_dict["attendance_request_approval"].grid.add_custom_button(__('Approve'),
		function () {
			if(frm.doc.leave_approval){
				$.each(frm.doc.attendance_request_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Attendance Request",
							name: d.attendance_request_number,
							workflow_state : "Approved",
						}).then(r => {
							frm.get_field("attendance_request_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}
		}).css({'color':'white','background-color':"#009E60","margin-left": "10px", "margin-right": "10px"});

		frm.fields_dict["expense_claim_approval"].grid.add_custom_button(__('Reject'),
		function () {
			if(frm.doc.expense_claim_approval){
				$.each(frm.doc.expense_claim_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Expense Claim",
							name: d.application_no,
							workflow_state: 'Rejected'
						}).then(r => {
							frm.get_field("expense_claim_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}			
		}).addClass('btn-danger')


		frm.fields_dict["expense_claim_approval"].grid.add_custom_button(__('Approve'),
		function () {
			if(frm.doc.expense_claim_approval){
				$.each(frm.doc.expense_claim_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Expense Claim",
							name: d.application_no,
							workflow_state : "Approved",
						}).then(r => {
							frm.get_field("expense_claim_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}
		}).css({'color':'white','background-color':"#009E60","margin-left": "10px", "margin-right": "10px"});
		

	
		
		frm.fields_dict["purchase_invoice_approval"].grid.add_custom_button(__('Reject'),
		function () {
			if(frm.doc.purchase_invoice_approval){
				$.each(frm.doc.purchase_invoice_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('get_sales_invoice', {
							doctype: "Purchase Invoice",
							name: d.purchase_invoice,
							docstatus: 'Draft'
						}).then(r => {
							frm.get_field("purchase_invoice_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}			
		}).addClass('btn-danger')


		frm.fields_dict["purchase_invoice_approval"].grid.add_custom_button(__('Approve'),
		function () {
			if(frm.doc.purchase_invoice_approval){
				$.each(frm.doc.purchase_invoice_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Purchase Invoice",
							name: d.purchase_invoice,
							workflow_state :"Approved",
						}).then(r => {
							frm.get_field("purchase_invoice_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}
		}).css({'color':'white','background-color':"#009E60","margin-left": "10px", "margin-right": "10px"});


	}
	},
		
	
	onload(frm){
		frappe.run_serially([
			() => frm.call('get_leave_app').then(r=>{
				if (frappe.session.user){
					if (frappe.user.has_role(['HR Manager'])){
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('leave_approval', {
							'application_no':d.name,
							'for_employee':d.employee,
							'employee_name':d.employee_name,
							'leave_type' :d.leave_type,
							'from_date':d.from_date,
							'to_date':d.to_date,
							'total_leave_days':d.total_leave_days,
							'workflow_state' :d.workflow_state

						})
						frm.refresh_field('leave_approval')	
					})
				}
			}
		}
			})	,
			() => frm.call('get_att_req').then(r=>{
				if (frappe.session.user){
				if (frappe.user.has_role(['HR Manager'])){
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('attendance_request_approval', {
							'attendance_request_number':d.name,
							'for_employee':d.employee,
							'employee_name':d.employee_name,
							'from_date':d.from_date,
							'to_date':d.to_date,
							'reason':d.explanation,
							'workflow_state' :d.workflow_state,
						})
						frm.refresh_field('attendance_request_approval')
					})
				}
			}
		}
			})	,
			() => frm.call('get_expence_claim').then(r=>{
				if (frappe.session.user){
				if (frappe.user.has_role(['HR Manager'])){
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('expense_claim_approval', {
							'application_no':d.name,
							'from_employee':d.employee,	
							'employee_name':d.employee_name,
							'expense_approver':d.expense_approver,
							'total_amount':d.total_claimed_amount,
							'workflow_state':d.workflow_state,
							
						})
						frm.refresh_field('expense_claim_approval')
					})
				}
			}
		}
			})	,
			() => frm.call('get_expence_claim_md').then(r=>{
				if (frappe.session.user){
				if (frappe.user.has_role(['Managing Director'])){
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('expense_claim_approval', {
							'application_no':d.name,
							'from_employee':d.employee,	
							'employee_name':d.employee_name,
							'expense_approver':d.expense_approver,
							'total_amount':d.total_claimed_amount,
							'workflow_state':d.workflow_state,
							
						})
						frm.refresh_field('expense_claim_approval')
					})
				}
			}
		}
			})	,
			
			() => frm.call('get_purchase_invoice').then(r=>{
				if (frappe.session.user){
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('purchase_invoice_approval', {
							'purchase_invoice':d.name,
							'supplier':d.supplier,
							'date':d.posting_date,
							'workflow_state':d.workflow_state,
						})
						frm.refresh_field('purchase_invoice_approval')
					})
				
			}
		}
			})	,
			() => frm.call('get_purchase_invoice_ceo').then(r=>{
				if (frappe.session.user){
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('purchase_invoice_approval', {
							'purchase_invoice':d.name,
							'supplier':d.supplier,
							'date':d.posting_date,
							'workflow_state':d.workflow_state,
						})
						frm.refresh_field('purchase_invoice_approval')
					})
				
			}
		}
			})	,
			
			
		])
	}	

});
