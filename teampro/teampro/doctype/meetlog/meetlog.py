# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from teampro.teampro.report.meetlog.meetlog import get_graphhopper_distance

class MeetLog(Document):
	import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from frappe.utils.data import get_link_to_form

from frappe.model.document import Document
from frappe.utils import getdate, get_link_to_form
import frappe

class MeetLog(Document):
    def on_submit(self):
        if not self.reached_location:
            frappe.throw('Reached Location not Captured. Use <b>Reached</b> Button.')
        if not self.submitted_area:
            frappe.throw('Completed Location not Captured. Use <b>Completed</b> Button.')
    def validate(self):
        if self.latitude and self.longitude and self.reached_latitude and self.reached_longitude:
            distance=get_graphhopper_distance(self.latitude,self.longitude,self.reached_latitude,self.reached_longitude)
            self.distance=float(distance)
    def before_insert(self):
        current_date = getdate(self.date_and_time)
        frappe.errprint(f"Current date: {current_date}")
        existing_docs = frappe.db.get_list(
            "MeetLog",
            filters=[
                ["employee", "=", self.employee],
                ["docstatus", "=", 0],
                ["name", "!=", self.name]
            ],
            fields=["name", "date_and_time"],
            order_by="creation desc",
            limit=10 
        )
        for doc in existing_docs:
            existing_date = getdate(doc.date_and_time)
            if existing_date == current_date:
                form_link = get_link_to_form("MeetLog", doc.name)
                frappe.throw(
                    f"Already another MeetLog document exists for this employee on {current_date}. "
                    f"Please check {form_link} before creating a new one."
                )
        current_date = getdate(self.date_and_time)
        doc_count = frappe.db.sql(
            """
            SELECT COUNT(*) as count 
            FROM `tabMeetLog`
            WHERE DATE(date_and_time) = %s
            AND employee = %s
            """,
            (current_date,self.employee,), 
            as_dict=True
        )

        
        self.day_sequence = doc_count[0]['count'] + 1

@frappe.whitelist()
def submit_meetlog(name):
    if frappe.db.exists("MeetLog",name):
        doc=frappe.get_doc("MeetLog",name)
        if doc.visit_type=="Appointment" and doc.sales_follow_up:
            if frappe.db.exists('Sales Follow Up',doc.sales_follow_up):
                sfu = frappe.get_doc("Sales Follow Up", doc.sales_follow_up)
                sfu.app_status = "Visited"
                sfu.visit_status = "Visited"
                sfu.appointment_remarks = doc.visit_remarks
                sfu.custom_person_met = doc.person_to_meet
                sfu.custom_contact_email = doc.mail_id
                sfu.appointment_fixed_on = ""
                sfu.custom_appointment_fixed_for = ""
                sfu.visted_by = frappe.session.user
                sfu.visted_date = today()
                if doc.visiting_card:
                    sfu.custom_attach_vc=doc.visiting_card
                if doc.person_to_meet or doc.mail_id:
                    sfu.append("contacts", {
                        "person_name": doc.person_to_meet,
                        "email_id": doc.mail_id
                    })
                if doc.visit_remarks:
                    sfu.append("custom_appointment_details", {
                        "visted_date": today(),
                        "visted_by": frappe.session.user,
                        "appointment_remarks": doc.visit_remarks
                    })
                sfu.save(ignore_permissions=True)
        doc.submit()