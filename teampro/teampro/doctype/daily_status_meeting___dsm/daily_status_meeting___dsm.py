# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class DailyStatusMeetingDSM(Document):
	pass



import frappe
from frappe.utils import today

@frappe.whitelist()
def get_status_counts(date):

    data = frappe.get_all(
        "Sales Follow Up",
        fields=["status", "count(name) as count"],
        filters={"next_contact_date": date},
        group_by="status"
    )

    counts = {
        "Lead": 0,
        "Open": 0,
        "Replied": 0,
        "Opportunity": 0,
        "Quotation": 0,
        "Lost Quotation": 0,
        "Interested": 0,
        "Converted": 0,
        "Customer": 0,
        "Do Not Contact": 0
    }

    for d in data:
        counts[d.status] = d.count

    return counts



# import frappe

# @frappe.whitelist()
# def get_dsm_data(dsm_date):

#     data = {}

#     counts = {
#         "Lead": 0, "Open": 0, "Replied": 0, "Opportunity": 0,
#         "Quotation": 0, "Lost Quotation": 0, "Interested": 0,
#         "Converted": 0, "Customer": 0, "Do Not Contact": 0
#     }

#     sf_list = frappe.get_all("Sales Follow Up",
#         filters={"next_contact_date": dsm_date},
#         fields=["status"]
#     )

#     for row in sf_list:
#         if row.status in counts:
#             counts[row.status] += 1

#     data.update({
#         "lead": counts["Lead"],
#         "open": counts["Open"],
#         "replied": counts["Replied"],
#         "opportunity": counts["Opportunity"],
#         "quotation": counts["Quotation"],
#         "lost_quotation": counts["Lost Quotation"],
#         "interested": counts["Interested"],
#         "converted": counts["Converted"],
#         "customer": counts["Customer"],
#         "do_not_contact": counts["Do Not Contact"],
#     })

#     data["it"] = frappe.db.count("Project", {
#         "custom_spoc__next_contact_on": dsm_date,
#         "service": "IT-SW",
#         "status": "Open"
#     })

#     data["rec"] = frappe.db.count("Project", {
#         "custom_spoc__next_contact_on": dsm_date,
#         "service": ["in", ["REC-I", "REC-D"]],
#         "status": "Open"
#     })

#     it_projects = frappe.get_all("Project",
#         filters={"custom_spoc__next_contact_on": dsm_date, "service": "IT-SW", "status": "Open"},
#         pluck="name"
#     )

#     if it_projects:
#         data["it_task"] = frappe.db.count("Task", {
#             "project": ["in", it_projects],
#             "status": ["in", ["Open", "Working", "Pending Review", "Client Review", "Overdue"]]
#         })
#     else:
#         data["it_task"] = 0

#     rec_projects = frappe.get_all("Project",
#         filters={"custom_spoc__next_contact_on": dsm_date, "service": ["in", ["REC-I", "REC-D"]], "status": "Open"},
#         pluck="name"
#     )

#     if rec_projects:
#         data["rec_task"] = frappe.db.count("Task", {
#             "project": ["in", rec_projects],
#             "status": ["in", ["Open", "Working", "Overdue"]]
#         })
#     else:
#         data["rec_task"] = 0


#     data["ip"] = frappe.db.count("Candidate", {
#         "custom_next_contact_on": dsm_date,
#         "pending_for": ["in", ["Sourced", "Pending QC", "Submitted (SPOC)", "Submitted (Client)"]]
#     })

#     data["fp"] = frappe.db.count("Candidate", {
#         "custom_next_contact_on": dsm_date,
#         "pending_for": ["in", ["Interviewed", "Reported", "Result Pending"]]
#     })


#     data["candidate"] = frappe.db.count("Closure", {
#         "custom_next_follow_up_on": dsm_date,
#         "pp_original_at": "Candidate"
#     })

#     data["agent"] = frappe.db.count("Closure", {
#         "custom_next_follow_up_on": dsm_date,
#         "pp_original_at": "Agent"
#     })

#     data["supplier"] = frappe.db.count("Closure", {
#         "custom_next_follow_up_on": dsm_date,
#         "pp_original_at": "Supplier"
#     })

#     data["internal"] = frappe.db.count("Closure", {
#         "custom_next_follow_up_on": dsm_date,
#         "pp_original_at": "TEAMPRO"
#     })

#     data["opportunity_list"] = frappe.get_all("Opportunity",
#         filters={
#             "transaction_date": dsm_date,
#             "custom_sales_follow_up": ["is", "set"]
#         },
#         fields=["name", "status", "opportunity_from", "party_name"]
#     )

#     return data