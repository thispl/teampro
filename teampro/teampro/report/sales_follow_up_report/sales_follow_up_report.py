import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": _("ID"), "fieldtype": "Link", "fieldname": "id", "options": "Sales Follow Up", "width": 180},
        {"label": _("Service"), "fieldtype": "Data", "fieldname": "service", "width": 150},
        {"label": _("CRM ID"), "fieldtype": "Dynamic Link", "fieldname": "crm_id", "options": "crm_doctype", "width": 250},
        {"label": _("Organization Name"), "fieldtype": "Data", "fieldname": "organization_name", "width": 250},
        {"label": _("Status"), "fieldtype": "Data", "fieldname": "status", "width": 120},
        {"label": _("Person Name"), "fieldtype": "Data", "fieldname": "person_name", "width": 200},
        {"label": _("Mobile"), "fieldtype": "Data", "fieldname": "mobile", "width": 150},
        {"label": _("Has WhatsApp"), "fieldtype": "Data", "fieldname": "has_whatsapp", "width": 120},
        {"label": _("Next Contact Date"), "fieldtype": "Date", "fieldname": "next_contact_date", "width": 130},
        {"label": _("Next Contact By"), "fieldtype": "Data", "fieldname": "next_contact_by", "width": 180},
        {"label": _("Last Contact On"), "fieldtype": "Date", "fieldname": "last_contact_on", "width": 130},
        {"label": _("Call status"), "fieldtype": "Data", "fieldname": "call_status", "width": 120},
        {"label": _("Territory"), "fieldtype": "Data", "fieldname": "territory", "width": 150},
        {"label": _("Remarks"), "fieldtype": "Data", "fieldname": "remarks", "width": 200},
    ]


def get_data(filters=None):
    filters = filters or {}
    data = []

   
    conditions = ["sfp.status != 'Do Not Contact'"]
    params = {}

    if filters.get("sfp_id"):
        conditions.append("sfp.name = %(sfp_id)s")
        params["sfp_id"] = filters["sfp_id"]

    if filters.get("organization_name"):
        conditions.append("sfp.organization_name = %(organization_name)s")
        params["organization_name"] = filters["organization_name"]
        
    if filters.get("next_contact_by"):
        conditions.append("sfp.next_contact_by = %(next_contact_by)s")
        params["next_contact_by"] = filters["next_contact_by"]
        
    if filters.get("territory"):
        conditions.append("sfp.sfp_territory = %(territory)s")
        params["territory"] = filters["territory"]

    
    sales_followups = frappe.db.sql(f"""
        SELECT
            sfp.name,
            sfp.service,
            sfp.organization_name,
            sfp.next_contact_date,
            sfp.next_contact_by,
            sfp.last_contacted_on,
            sfp.sfp_territory,
            sfp.remarks,
            sfp.party_name,
            sfp.party_from,
            sfp.status,
            sfp.call_status
        FROM `tabSales Follow Up` sfp
        WHERE {" AND ".join(conditions)}
    """, params, as_dict=True)

    
    for sfp in sales_followups:
        
        # lead_contacts = frappe.db.sql("""
        #     SELECT DISTINCT person_name, mobile, has_whatsapp
        #     FROM `tabLead Contacts`
        #     WHERE parent = %s
        # """, (sfp.name,), as_dict=True)
        
        lead_contacts = frappe.db.sql("""
			SELECT DISTINCT person_name, mobile, has_whatsapp
			FROM `tabLead Contacts`
			WHERE parent = %s AND person_name IS NOT NULL AND person_name != ''
		""", (sfp.name,), as_dict=True)

        
        whatsapp_contacts = [c for c in lead_contacts if c.has_whatsapp]
        non_whatsapp_contacts = [c for c in lead_contacts if not c.has_whatsapp]

        
        if filters.get("has_whatsapp"):
            
            for contact in whatsapp_contacts:
                data.append(make_row(sfp, contact.person_name, contact.mobile, "Yes"))

        else:
           
            # for contact in whatsapp_contacts:
            #     data.append(make_row(sfp, contact.person_name, contact.mobile, "Yes"))

            if non_whatsapp_contacts:
                
                data.append(make_row(sfp, None, None, "No"))

    return data







def make_row(sfp, person_name, mobile, has_whatsapp_value):
    """Helper to create a clean report row"""
    return {
        "id": sfp.name,
        "service": sfp.service,
        "crm_id":sfp.party_name,
        "crm_doctype": "Customer" if sfp.party_from == "Customer" else "Lead",
        "status": sfp.status,
        "organization_name": sfp.organization_name,
        "person_name": person_name or "",
        "mobile": mobile or "",
        "has_whatsapp": has_whatsapp_value,
        "next_contact_date": sfp.next_contact_date,
        "next_contact_by": sfp.next_contact_by,
        "last_contact_on": sfp.last_contacted_on,
        "call_status":sfp.call_status,
        "territory": sfp.sfp_territory,
        "remarks": sfp.remarks,
    }
