// Copyright (c) 2022, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('IAF Form', {
	passport_number(frm){
		frappe.db.get_list('Candidate', {
			filters: { passport_number: frm.doc.passport_number},
			fields: ['*']
		}).then((r) => {
			if(r){
				var a= r[0]
				frm.set_value("customer",a.customer)
				frm.set_value("given_name",a.given_name)
				frm.set_value("passport_expiry_date",a.passport_expiry_date)
				frm.set_value("position",a.position)
				frm.set_value("dob",a.dob)
				frm.set_value("territory",a.territory)
				frm.set_value("age",a.age)
				frm.set_value("mobile_number",a.mobile_number)
				frm.set_value("mobile",a.mobile)
				frm.set_value("mail_id",a.mail_id)
				frm.set_value("total_experience",a.total_experience)
				frm.set_value("overseas_experience",a.overseas_experience)
				frm.set_value("india_experience",a.india_experience)
				frm.set_value("vaccination_status",a.vaccination_status)
				frm.set_value("vaccine_name",a.vaccine_name)
				frm.set_value("notice_period_months",a.notice_period_months)
				frm.set_value("overall_rating",a.overall_rating)
				frm.set_value("location",a.location)
				frm.set_value("current_ctc",a.current_ctc)
				frm.set_value("expected_ctc",a.expected_ctc)
				frm.set_value("currency",a.currency)
				frm.set_value("confidence",a.confidence)
				frm.set_value("interest",a.interest)
				frm.set_value("relevance",a.relevance)
				frm.set_value("communication_1",a.communication_1)
				frm.set_value("remarks_1",a.remarks_1)
				frm.set_value("remarks",a.remarks)
				frm.set_value("evaluated_by",a.interest)
				frm.set_value("final_result",a.final_result)
				frm.set_value("is_married",a.is_married)
				frm.set_value("organization",a.organization)
				frm.set_value("candidate_id",a.name)
				frm.set_value("specialization",a.specialization)
				frm.set_value("year_of_passing",a.year_of_passing)
				frm.set_value("qualification",a.qualification)
			}
		})
	},
		candidate_id(frm){
		frappe.db.get_list('Education Details',{
			filters: { parent: frm.doc.candidate_id},
			fields: ['*']
		}).then(d => {
			if(d){
				var b = d[0]
				frm.set_value("year_of_passing",b.year_of_passing)
				frm.set_value("specialization",b.specialization)
				frm.set_value("qualification",b.qualification)
			}
		})
		frappe.db.get_list('Experience Details',{
			filters: { parent: frm.doc.candidate_id},
			fields: ['*']
		}).then(d => {
			if(d){
				var b = d[0]
				frm.set_value("organization",b.organization)
			}
		})
	}
});
