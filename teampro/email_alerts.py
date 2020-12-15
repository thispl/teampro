import frappe
from frappe.utils.data import today
from frappe.utils import  formatdate

@frappe.whitelist()
def next_contact_alert():
    contacts = frappe.db.sql("""select contact_by from `tabLead` where date(contact_date) = %s group by contact_by""",(today()),as_dict=1)
    for c in contacts:
        lead_info = frappe.db.sql("""select contact_by,contact_date,company_name,lead_name,status,territory,mobile_no from `tabLead` where date(contact_date) = %s and contact_by = %s""",(today(),c.contact_by),as_dict=1)
          
        content = """<table class='table table-bordered'>
                <tr>
                <th>S.No.</th>
                <th>Person Name</th>
                <th>Organization Name</th>
                <th>Status</th>
                <th>Territory</th>
                <th>Mobile</th>
                <th>Phone</th>
                <th>Email</th>
                </tr>"""
        data = ''
        for idx, l in enumerate(lead_info):
            data = """
            <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            </tr>
            """ %(idx+1,l.lead_name,l.company_name,l.status,l.territory,l.mobile_no,l.phone,l.email_id)
            content += data
        if data:
            emp_name = frappe.get_value('User',c.contact_by,'full_name')
            frappe.sendmail(
            recipients=[c.contact_by],
            subject='Lead Next Contact Alert -'+ formatdate(today()),
            message="""
            <p>Dear %s,</p>
            <P> Please find the list of Leads to be contacted today - %s %s""" % (emp_name,formatdate(today()), content)) 