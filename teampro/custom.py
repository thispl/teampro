import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import cint
from frappe.utils.data import today

def bulk_update_from_csv(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    count = 0
    for pp in pps:
        ld = frappe.db.exists("Lead",{'name':pp[0]})
        if ld:
            # items = frappe.get_all("Lead",{'name':pp[0]})
            # for item in items:
            i = frappe.get_doc('Lead',pp[0])
            if not i.contact_date:
                i.contact_date = pp[1]
                # i.append("supplier_items",{
                #     'supplier' : pp[1]
                # })
                i.save(ignore_permissions=True)
                frappe.db.commit()

def update_nxd():
    leads = frappe.get_list("Lead")
    for lead in leads:
        l = frappe.get_doc("Lead",lead.name)
        if not l.contact_date:
            l.contact_date = "2020-08-31 0:00:00"
            l.save(ignore_permissions=True)
            frappe.db.commit()

def update_lead():
    leads = frappe.get_list("Lead",{"organization_lead":"0"})
    for lead in leads:
        doc = frappe.get_doc("Lead",lead.name)
        doc.organization_lead = 1
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        # frappe.errprint(lead.name)