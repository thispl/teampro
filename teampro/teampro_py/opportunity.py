import frappe
@frappe.whitelist()
def update_sfp_opportunity(sfp,status):
    if sfp and status=="Lost":
        frappe.db.set_value("Sales Follow Up",sfp,"status","Replied")

@frappe.whitelist()
def get_contact_details(party_name,party_type,name):
    cont=''
    email=''
    person=''
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

from frappe.utils import getdate, nowdate, add_days, formatdate
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days

@frappe.whitelist()
def update_opportunity_age():
    opportunity = frappe.db.get_all("Opportunity",{"status":("not in", ["Lost", "Converted"])},["name","transaction_date"])
    current_date = getdate(today())
    ind = 0
    for i in opportunity:
        opportunity_date = getdate(i.transaction_date)
        age = (current_date - opportunity_date).days
        ind += 1
        frappe.db.set_value("Opportunity",i.name,"custom_opportunity_age",age)



@frappe.whitelist()
def task_mail_notification_status ():
    job = frappe.db.exists('Scheduled Job Type','update_opportunity_age')
    if not job:
        task = frappe.new_doc("Scheduled Job Type")
        task.update({
            "method": 'teampro.teampro_py.opportunity.update_opportunity_age',
            "frequency": 'Cron',
            "cron_format": '30 9 * * *'
        })
        task.save(ignore_permissions=True)
