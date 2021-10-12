import frappe

# def change_ends_on_date():
#     leads = frappe.get_all("Lead")
#     print(len(leads))
#     for l in leads:
#         print(l.name)
#         frappe.db.set_value("Lead",l.name,"ends_on","2295-12-31 00:00:00")


# def change_validation():
#     leads = frappe.get_all("Lead")
#     print(len(leads))
#     for l in leads:
#         print(l.name)
#         frappe.db.set_value("Lead",l.name,"validation_status","Invalid")


# def transfer_website():
#     leads = frappe.get_all("Lead",['name','website'])
#     for l in leads:
#         frappe.db.set_value("Lead",l.name,"web",l.website)

# @frappe.whitelist()
# def transfer_contacts():
    # leads = frappe.get_all('Contact',['name','temp_mobile_no'])
    # for lead in leads:
#     contacts = frappe.db.sql("""select `tabContact`.name,`tabContact`.first_name,`tabContact`.middle_name,`tabContact`.last_name,`tabDynamic Link`.link_doctype, `tabDynamic Link`.link_name,`tabContact Email`.email_id
#     from `tabContact` Left Join `tabDynamic Link` on `tabContact`.name = `tabDynamic Link`.parent
#     Left Join `tabContact Email` on `tabContact`.name = `tabContact Email`.parent where `tabDynamic Link`.link_doctype = 'Lead'  """,as_dict=True)
#     for contact in contacts:
#         lead = frappe.get_doc('Lead',contact.link_name)
#         if not contact.last_name:
#             person_name = contact.first_name
#         else:
#             person_name = contact.first_name + contact.last_name
#         lead.append('lead_contacts',{
#             'person_name': person_name,
#             'mobile': lead.temp_mobile_no,
#             'email_id': contact.email_id
#         })
#         lead.save(ignore_permissions=True)
#         frappe.db.commit()
#         print(lead.name,person_name,lead.temp_mobile_no,contact.email_id)

# # @frappe.whitelist()
# def transfer_address():
#     addresses = frappe.db.sql("""select `tabAddress`.address_line1,`tabAddress`.address_line2,`tabAddress`.city,`tabAddress`.phone,`tabAddress`.state,`tabAddress`.country,`tabDynamic Link`.link_doctype, `tabDynamic Link`.link_name
#     from `tabAddress` Left Join `tabDynamic Link` on `tabAddress`.name = `tabDynamic Link`.parent where `tabDynamic Link`.link_doctype = 'Lead' """,as_dict=True)
#     for address in addresses:
#         lead = frappe.get_doc('Lead',address.link_name)
#         addr = ''
#         addr += address.address_line1 or '' + "\n"
#         addr += address.address_line2 or '' + "\n"
#         addr += address.city or '' + "\n"
#         addr += address.state or '' + "\n"
#         addr += address.country or '' + "\n"
#         addr += address.phone or '' + "\n"
#         lead.address = addr
#         lead.save(ignore_permissions=True)
#         frappe.db.commit()
        # print(addr)
    # print(lead.name,person_name,lead.temp_mobile_no,contact.email_id)


@frappe.whitelist()
def change_lead_owner():
    leads = frappe.get_all("Lead",{'contact_by':'sr@groupteampro.com','territory':'Tamil Nadu'})
    print(len(leads))
    # for l in leads:
    #     print(l.name)
    #     # frappe.db.set_value("Lead",l.name,"contact_by","sales@groupteampro.com")
    #     frappe.db.set_value("Lead",l.name,"lead_owner","anil.p@groupteampro.com")


