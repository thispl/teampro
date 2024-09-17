import frappe

@frappe.whitelist(allow_guest=True)
def get_biometric_logs(**args):
    frappe.log_error(title='biometric logs',message=args)



import frappe
import requests
from frappe import _

@frappe.whitelist()
def get_address(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        frappe.throw(_("Unable to fetch address from coordinates."))
