import frappe
from frappe import _
from frappe.utils.file_manager import get_file
from frappe.utils import get_url
import requests
from datetime import date

@frappe.whitelist()
def update_sla_status(doc,method):

    today = date.today()
    
    for sla in doc.custom_sla_details:  
        if sla.sla_to_date and sla.sla_to_date < today:
            sla.status = "Expired"
            frappe.errprint(sla.status)