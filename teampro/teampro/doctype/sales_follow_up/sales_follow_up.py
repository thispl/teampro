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
