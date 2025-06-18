# Copyright (c) 2023, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesFollowUp(Document):
	pass
@frappe.whitelist()
def lead_contacts(lead):
	lead_contacts=[]

	lead_contact = frappe.get_doc("Lead", lead)
	for i in lead_contact.lead_contacts:
		contact_data = {
			"person_name": i.person_name or '',
			"mobile": i.mobile or '',
			"is_primary": i.is_primary or False,
			"has_whatsapp": i.has_whatsapp or False,
			"email_id": i.email_id or '',
			"is_primaryemail": i.is_primaryemail or False,
			"service":i.service or ''
		}
		lead_contacts.append(frappe._dict(contact_data))
	return lead_contacts

@frappe.whitelist()
def update_child_contacts(name):
	lead_contacts=[]

	lead_contact = frappe.get_doc("Sales Follow Up", name)
	for i in lead_contact.contacts:
		contact_data = {
			"person_name": i.person_name or '',
			"mobile": i.mobile or '',
			"is_primary": i.is_primary or False,
			"has_whatsapp": i.has_whatsapp or False,
			"email_id": i.email_id or '',
			"is_primaryemail": i.is_primaryemail or False,
			"service":i.service or ''
		}
		lead_contacts.append(frappe._dict(contact_data))
	return lead_contacts

@frappe.whitelist()
def update_child_customer_contacts(name):
	lead_contacts=[]

	lead_contact = frappe.get_doc("Sales Follow Up", name)
	for i in lead_contact.customer_contacts:
		contact_data = {
			"person_name": i.person_name or '',
			"mobile": i.mobile or '',
			"is_primary": i.is_primary or False,
			"has_whatsapp": i.has_whatsapp or False,
			"email_id": i.email_id or '',
			"is_primaryemail": i.is_primaryemail or False,
			"has_whatsapp":i.has_whatsapp or False,
			"service":i.service or ''
		}
		lead_contacts.append(frappe._dict(contact_data))
	return lead_contacts

@frappe.whitelist()
def customer_contacts(customer):
	customer_contacts=[]

	customer_contact = frappe.get_doc("Customer", customer)
	for i in customer_contact.customer_contact:
		contact_data = {
			"person_name": i.person_name or '',
			"mobile": i.mobile or '',
			"is_primary": i.is_primary or False,
			"has_whatsapp": i.has_whatsapp or False,
			"email_id": i.email_id or '',
			"is_primaryemail": i.is_primaryemail or False,
			"service":i.service or ''
		}
		customer_contacts.append(frappe._dict(contact_data))
	return customer_contacts

# @frappe.whitelist()
# def address():
# 	customer_address = []
# 	customer = frappe.get_doc("Customer", "Foodexochennai")
# 	# if customer.address_html and customer.contact_html:
# 	# 	customer_address.append(frappe._dict({"adress_html":customer.address_html or '',"customer":customer.contact_html or '' }))
# 	# elif customer.contact_html:
# 	# 	customer_address.append(frappe._dict({"adress_html":'',"customer":customer.contact_html or '' }))
# 	# elif customer.address_html:
# 	# 	customer_address.append(frappe._dict({"adress_html":customer.address_html or '',"customer":'' }))
# 	# else:
# 	# 	customer_address.append(frappe._dict({"adress_html":'',"customer":'' }))
# 	print(customer.contact_html or '')
@frappe.whitelist()
def update_customer_next_contact_date(customer_name,s_next_contact_date,service):
	frappe.db.set_value("Customer",{"customer_name":customer_name,"service":service},"next_contact_date",s_next_contact_date)
	contact_by=frappe.db.get_value("Sales Follow Up",{"customer":customer_name},["next_contact_by"])
	frappe.db.set_value("Customer",{"customer_name":customer_name,"service":service},"next_contact_by",contact_by)

@frappe.whitelist()
def update_customer_s_remarks(customer_name,s_remarks,service):
	frappe.db.set_value("Customer",{"customer_name":customer_name,"service":service},"remarks",s_remarks)

@frappe.whitelist()
def update_opportunity_next_contact_date(lead_name,s_next_contact_date,service):
	frappe.db.set_value("Opportunity",{"party_name":lead_name,"service":service,"status":("not in",["Closed","Lost","Quotation"])},"next_contact_date",s_next_contact_date)
	contact_by=frappe.db.get_value("Sales Follow Up",{"follow_up_to":"Lead","lead":lead_name},["next_contact_by"])
	frappe.db.set_value("Opportunity",{"opportunity_from":"Lead","party_name":lead_name,"service":service,"status":("not in",["Closed","Lost"])},"next_contact_by",contact_by)

@frappe.whitelist()
def update_opportunity_s_remarks(lead_name,s_remarks,service,name):
	frappe.db.set_value("Opportunity",{"opportunity_from":"Lead","party_name":lead_name,"custom_sales_follow_up":name,"service":service,"status":("not in",["Closed","Lost"])},"remark",s_remarks)

@frappe.whitelist()
def update_opportunity_next_contact_date_from_customer(customer,s_next_contact_date,service):
	frappe.db.set_value("Opportunity",{"party_name":customer,"service":service,"status":("not in",["Closed","Lost","Quotation"])},"next_contact_date",s_next_contact_date)
	contact_by=frappe.db.get_value("Sales Follow Up",{"follow_up_to":"Customer","customer":customer},["next_contact_by"])
	frappe.db.set_value("Opportunity",{"opportunity_from":"Customer","party_name":customer,"service":service,"status":("not in",["Closed","Lost"])},"next_contact_by",contact_by)

@frappe.whitelist()
def update_opportunity_s_remarks_from_customer(customer,s_remarks,service,name):
	frappe.db.set_value("Opportunity",{"opportunity_from":"Customer","party_name":customer,"custom_sales_follow_up":name,"service":service,"status":("not in",["Closed","Lost","Converted"])},"remark",s_remarks)

@frappe.whitelist()
def update_opportunity_sfp(name,remarks):
	oppr=frappe.db.get_value("Opportunity",{"opportunity_from":"Sales Follow Up","party_name":name},["name"])
	frappe.db.set_value("Opportunity",oppr,"remark",remarks)


@frappe.whitelist()
def update_lead_manager(party_name,party_type,name):
	if party_type:
		if party_type=="Lead":
			owner=frappe.db.get_value("Lead",{'name':party_name},['lead_owner'])
		else:
			owner=frappe.db.get_value("Customer",{'name':party_name},['account_manager'])
	return owner

@frappe.whitelist()
def get_contact_details(party_name,party_type,name):
	if party_type=='Sales Follow Up':
		sfp=frappe.get_doc('Sales Follow Up',party_name)
		for contact in sfp.contacts:
			if contact.is_primary == 1:
				cont=contact.mobile
				email=contact.is_primaryemail
				person=contact.person_name
	return {
        'cont': cont,
        'email': email,
        'person': person
    }