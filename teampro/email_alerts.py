import frappe
from frappe.utils.data import add_days, today
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

@frappe.whitelist()
def checkin_alert():
    yesterday = add_days(today(),-1)
    employees = frappe.get_all('Employee',{'status':'Active'},['name','user_id','employee_name'])
    for emp in employees:
        ec = frappe.db.sql("select employee from `tabEmployee Checkin` where date(time) = '%s' and employee = '%s'" %(yesterday,emp.name),as_dict=True)
        if len(ec) < 2:
            frappe.sendmail(
            recipients=[emp.user_id],
            subject='Miss Punch Alert - '+ formatdate(yesterday),
            message="""
            <p>Dear %s,</p>
            <P> Please be informed that, the Bio Metric Punch of yours is missing for  - %s
            Please initiate action for Leave / OD in ERP immediately. In any other case contact your reporting head
            """ % (emp.employee_name,yesterday))

            
    


