# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MassWhatsAppBroadcast(Document):
    # pass
    def on_submit(self):
        if not self.template:
            frappe.throw("Please select a WhatsApp Template")

        template_doc = frappe.get_doc("WhatsApp Templates",self.template)

        url = "https://graph.facebook.com/v22.0/118654914550336/messages"
        headers = {
            "Authorization": f"Bearer EAAIsCk6qqtMBQzaynopwQryrkwNRqmUsVSwWbtNnXdvNLJvOkw75GtSuqHLcVaqLej4ZAZChZBTZCTCMQP6iFbr41cWDZAEx7JCRGHPKA6ODWsyuvwB1M2FNI1uIe9qSVboVKhNMGUmjJG1ztBNFvG8LYyv4pA9ZBndu5vO9iKREmnVSLAC0ZAmD6OwO4bsDVWHrt3hpjMyJfLLz17vFVoryi5OZCaZBmUZAZCjJaZA3eYk6ZCmZAQIQwiaCCXTfnVQMdZATRJTBQYMRMGpmfzddZCBe7C08jAZDZD",

            "Content-Type": "application/json"
        }

        sent_count = 0
        fail_count = 0
        mobile_numbers = []
        if self.recipient_type == "Recipient List":
            recipient_list_doc = frappe.get_doc("WhatsApp Recipient List", self.recipient_list)
            mobile_numbers = [r.mobile_number for r in recipient_list_doc.recipients if r.mobile_number]
        else:
            for row in self.recipients:
                if row.mobile_number:
                    mobile_numbers.append(row.mobile_number)
        for num in mobile_numbers:
            payload = {
                "messaging_product": "whatsapp",
                "to": num,
                "type": "template",
                "template": {
                    "name": template_doc.template_name,
                    "language": {
                        "code": template_doc.language or "en_US"
                    }
                }
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code in [200, 201]:
                sent_count += 1
            else:
                fail_count += 1
                frappe.log_error(response.text, f"WhatsApp Sending Failed for {num}")

        return {
            "message": f"WhatsApp Send Complete. Sent: {sent_count}, Failed: {fail_count}"
        }

import frappe
import requests
import json

@frappe.whitelist()
def send_whatsapp_messages(docname):
    doc = frappe.get_doc("Mass WhatsApp Broadcast", docname)

    if not doc.template:
        frappe.throw("Please select a WhatsApp Template")

    template_doc = frappe.get_doc("WhatsApp Templates",doc.template)

    url = "https://graph.facebook.com/v22.0/118654914550336/messages"
    headers = {
        "Authorization": f"Bearer EAAIsCk6qqtMBQzaynopwQryrkwNRqmUsVSwWbtNnXdvNLJvOkw75GtSuqHLcVaqLej4ZAZChZBTZCTCMQP6iFbr41cWDZAEx7JCRGHPKA6ODWsyuvwB1M2FNI1uIe9qSVboVKhNMGUmjJG1ztBNFvG8LYyv4pA9ZBndu5vO9iKREmnVSLAC0ZAmD6OwO4bsDVWHrt3hpjMyJfLLz17vFVoryi5OZCaZBmUZAZCjJaZA3eYk6ZCmZAQIQwiaCCXTfnVQMdZATRJTBQYMRMGpmfzddZCBe7C08jAZDZD",

        "Content-Type": "application/json"
    }

    sent_count = 0
    fail_count = 0
    mobile_numbers = []
    if doc.recipient_type == "Recipient List":
        recipient_list_doc = frappe.get_doc("WhatsApp Recipient List", doc.recipient_list)
        mobile_numbers = [r.mobile_number for r in recipient_list_doc.recipients if r.mobile_number]
    else:
        for row in doc.recipients:
            if row.mobile_number:
                mobile_numbers.append(row.mobile_number)
    for num in mobile_numbers:
        payload = {
            "messaging_product": "whatsapp",
            "to": num,
            "type": "template",
            "template": {
                "name": template_doc.template_name,
                "language": {
                    "code": template_doc.language or "en_US"
                }
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code in [200, 201]:
            sent_count += 1
        else:
            fail_count += 1
            frappe.log_error(response.text, f"WhatsApp Sending Failed for {num}")

    return {
        "message": f"WhatsApp Send Complete. Sent: {sent_count}, Failed: {fail_count}"
    }

# @frappe.whitelist()
# def send_whatsapp_messages(docname):
#     doc = frappe.get_doc("Mass WhatsApp Broadcast", docname)

#     if not doc.template:
#         frappe.throw("Please select a WhatsApp Template")
#     template_doc = frappe.get_doc("WhatsApp Templates", doc.template)
#     url = "https://graph.facebook.com/v22.0/118654914550336/messages"
#     headers = {
#         "Authorization": f"Bearer EAAIsCk6qqtMBPvN2EPkRSJhCUYZAh6vIlkuZCUjBOGuPFiaErPWpWTOZADfI50DjnOPba7XzZCCUh9VMNXq1NrIHh4dS1SkhOXFT0DhWr5nZCJUO7eZCbL0JIxZAkcWGebLBNw4z4Q2U7QZAK5UtPNhr2uFoRqIFZCxjQZCiXtnNGaM3vvpUdiGOTGcxYZAwcb84FPz2h16oJoNBsv6j2sYkqjlCxXHuZCelRfr1evV4dTiV",
#         "Content-Type": "application/json"
#     }

#     sent_count = 0
#     fail_count = 0
    
#     for row in doc.recipients:
#         mobile = row.mobile_number

#         payload = {
#             "messaging_product": "whatsapp",
#             "to": mobile,
#             "type": "template",
#             "template": {
#                 "name": template_doc.template_name,
#                 "language": {
#                     "code": template_doc.language or "en_US"
#                 }
#             }
#         }

#         response = requests.post(url, headers=headers, data=json.dumps(payload))

#         if response.status_code in [200, 201]:
#             sent_count += 1
#         else:
#             fail_count += 1
#             frappe.log_error(response.text, "WhatsApp Sending Failed")

#     return {
#         "message": f"WhatsApp Send Complete. Sent: {sent_count}, Failed: {fail_count}"
#     }

import frappe
import requests
import json

@frappe.whitelist()
def send_project_broadcast(project_name, template_name, recipient_list):
    project = frappe.get_doc("Project", project_name)
    template = frappe.get_doc("WhatsApp Templates", template_name)
    rlist = frappe.get_doc("WhatsApp Recipient List", recipient_list)
    field_list = [f.strip() for f in str(template.field_names).split("\n") if f.strip()]
    parameters = []
    for field in field_list:
        val = project.get(field) or "-"
        if not isinstance(val, str):
            val = str(val)
        val = val.strip()
        parameters.append({"type": "text", "text": val})
    mobile_numbers = [row.mobile_number for row in rlist.recipients if row.mobile_number]
    if not mobile_numbers:
        frappe.throw("No mobile numbers found in selected Recipient List")
    broadcast = frappe.new_doc("Mass WhatsApp Broadcast")
    broadcast.title = f"Broadcast - {project.name}"
    broadcast.template = template.name    
    broadcast.recipient_list = recipient_list
    broadcast.recipient_type="Recipient List"
    for num in mobile_numbers:
        broadcast.append("recipients", {
            "mobile_number": num,
            "reference_doctype": "Project",
            "reference_docname": project.name,
            "template_parameters": json.dumps(parameters)
        })

    broadcast.insert(ignore_permissions=True)
    url = "https://graph.facebook.com/v22.0/118654914550336/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer EAAIsCk6qqtMBQJr9bXvcGzUCWlWsl4uFGEmjcIEgSh0IHWP4lseuuix3Bxq9ZCcbh3QTSIlKIEKApKGzmh5sTNPyfcqbZBspJtScZA1khyOEOESWDtEy57wxSvIcqZCZCDyTQ3qDdCAbIs9xKBQYsnSaL0PA4AT49qwSZCIEfPBg4ZCaIXJMHDiSV2JBn8WxTFBcCdA9cMXPMHDE7ZBWpxmz6ctdYFGMKHE3HVkJXdZCmmM0pS7YTGAYanZAy0AJs13ROHVlHgy2ZAOrcdweZATf5nJ3",
    }
    failed = []
    success = []
    for num in mobile_numbers:
        payload = {
            "messaging_product": "whatsapp",
            "to": num,
            "type": "template",
            "template": {
                "name": template.template_name,
                "language": {"code": template.language or "en_US"},
                "components": [
                    {
                        "type": "body",
                        "parameters": parameters
                    }
                ]
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code in (200, 201):
            success.append(num)
        else:
            failed.append({"mobile": num, "error": response.text})

    return {
        "broadcast": broadcast.name,
        "sent": success,
        "failed": failed
    }

