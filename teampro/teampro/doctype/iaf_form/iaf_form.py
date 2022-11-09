# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IAFForm(Document):
    pass

@frappe.whitelist()
def update_candidate(doc,method):
        iaf = frappe.db.exists("Candidate", {"passport_number": doc.passport_number})
        if iaf:
            candidate = frappe.get_doc("Candidate", iaf)
            candidate.customer =  doc.customer
            candidate.passport_number =  doc.passport_number
            candidate.given_name =  doc.given_name
            candidate.passport_expiry_date = doc.passport_expiry_date
            candidate.position = doc.position
            candidate.dob = doc.dob
            candidate.territory = doc.territory
            candidate.age = doc.age
            candidate.mobile_number = doc.mobile_number
            candidate.mobile = doc.mobile
            candidate.mail_id = doc.mail_id
            candidate.overseas_experience  =  doc.overseas_experience
            candidate.india_experience = doc.india_experience
            candidate.notice_period_months = doc.notice_period_months
            candidate.overall_rating = doc.overall_rating
            candidate.location = doc.location
            candidate.organization =  doc.organization
            candidate.current_ctc = doc.current_ctc
            candidate.expected_ctc = doc.expected_ctc
            candidate.currency = doc.currency
            candidate.confidence = doc.confidence
            candidate.interest = doc.interest
            candidate.relevance = doc.relevance
            candidate.communication_1 = doc.communication_1
            candidate.remarks_1 = doc.remarks_1
            candidate.remarks = doc.remarks
            candidate.evaluated_by = doc.evaluated_by
            candidate.final_result = doc.final_result
            candidate.is_married = doc.is_married
            candidate.vaccination_status = doc.vaccination_status
            candidate.vaccine_name  =  doc.vaccine_name
            candidate.total_experience =  doc.total_experience
            candidate.append('table_28',{
                'specialization':doc.specialization,
                'qualification': doc.qualification,
                'year_of_passing':doc.year_of_passing

            })	
            candidate.append('experience_details',{
                'organization':doc.organization,
            })
            candidate.save(ignore_permissions=True)
            frappe.db.commit()

        else:    
            candidate = frappe.new_doc("Candidate")
            candidate.customer =  doc.customer
            candidate.passport_number =  doc.passport_number
            candidate.given_name =  doc.given_name
            candidate.passport_expiry_date = doc.passport_expiry_date
            candidate.position = doc.position
            candidate.dob = doc.dob
            candidate.territory = doc.territory
            candidate.age = doc.age
            candidate.mobile_number = doc.mobile_number
            candidate.mobile = doc.mobile
            candidate.mail_id =  doc.mail_id
            candidate.overseas_experience  =  doc.overseas_experience
            candidate.india_experience = doc.india_experience
            candidate.notice_period_months = doc.notice_period_months
            candidate.overall_rating = doc.overall_rating
            candidate.location = doc.location
            candidate.organization =  doc.organization
            candidate.current_ctc = doc.current_ctc
            candidate.expected_ctc = doc.expected_ctc
            candidate.currency = doc.currency
            candidate.confidence = doc.confidence
            candidate.interest = doc.interest
            candidate.relevance = doc.relevance
            candidate.communication_1 = doc.communication_1
            candidate.remarks_1 = doc.remarks_1
            candidate.remarks = doc.remarks
            candidate.evaluated_by = doc.evaluated_by
            candidate.final_result = doc.final_result
            candidate.is_married = doc.is_married
            candidate.vaccination_status = doc.vaccination_status
            candidate.vaccine_name  =  doc.vaccine_name
            candidate.total_experience =  doc.total_experience
            candidate.append('table_28',{
                'specialization':doc.specialization,
                'qualification': doc.qualification,
                'year_of_passing':doc.year_of_passing,

            })
            candidate.append('experience_details',{
                'organization':doc.organization,
            })	
            candidate.save(ignore_permissions=True)
            frappe.db.commit()
