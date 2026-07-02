import frappe
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days
from frappe.utils import getdate, nowdate

@frappe.whitelist()
def update_sla_status():
    customers = frappe.db.get_all("Customer", {"disabled": 0}, ["*"])

    for customer_info in customers:
        customer = frappe.get_doc("Customer", customer_info.name)
        if customer.custom_sla_details:
            for sla in customer.custom_sla_details:
                if sla.sla_to_date and getdate(sla.sla_to_date) < getdate(nowdate()):
                    sla.status = "Expired"
            customer.save(ignore_permissions=True)
            frappe.db.commit()

@frappe.whitelist()
def update_sla_value():
    frappe.enqueue(
        update_expired_sla,
        queue="long",
        timeout=36000,
        is_async=True,
        now=False,
        job_name=f"Project Update",
        enqueue_after_commit=True,
    )


def update_expired_sla():
    docs = frappe.get_all("Customer", fields=["name"])
    for d in docs:
        doc = frappe.get_doc("Customer", d.name)
        updated = False
        
        if doc.custom_sla_details:
            for row in doc.custom_sla_details:
                if row.sla_to_date:
                    sla_to_date = getdate(row.sla_to_date)  
                    if sla_to_date < getdate(today()):       
                        row.status = "Expired"
                        updated = True
        
        if updated:
            doc.save()
