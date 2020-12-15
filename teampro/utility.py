import frappe

def change_ends_on_date():
    leads = frappe.get_all("Lead")
    for l in leads:
        print(l.name)
        frappe.db.set_value("Lead",l.name,"ends_on","2021-03-31 00:00:00")