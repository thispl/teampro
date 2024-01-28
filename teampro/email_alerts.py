import frappe
from frappe.utils.data import add_days, today
from frappe.utils import  formatdate
from frappe.utils import format_datetime


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
        print(ec)
        if len(ec) < 2:
            frappe.sendmail(
            recipients=[emp.user_id],
            subject='Miss Punch Alert - '+ formatdate(yesterday),
            message="""
            <p>Dear %s,</p>
            <P> Please be informed that, the Bio Metric Punch of yours is missing for  - %s
            Please initiate action for Leave / OD in ERP immediately. In any other case contact your reporting head
            """ % (emp.employee_name,yesterday))

@frappe.whitelist()    
def daily_att_report():
    daily_att= frappe.db.sql("""
	select
		att.employee,
		att.employee_name,
		att.attendance_date,
		att.in_time,
		att.out_time,
        att.status
	from
		`tabAttendance` att
        join `tabEmployee` emp on emp.name = att.employee
		where
        att.attendance_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        and emp.status = 'Active'
	""", as_dict=1)
    staff = ''
    staff += '<table class = table table - bordered style=border-width:2px><tr><td colspan = 6><b>Attendance Report</b></td></tr>'
    staff += '<tr><td>Employee</td><td>Employee Name</td><td>Attendance date</td><td>In Time</td><td>Out Time</td><td>Status</td>'
    for att in daily_att:
        staff += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(att.employee,att.employee_name,formatdate(att.attendance_date),format_datetime(att.in_time) or '',format_datetime(att.out_time) or '',att.status) 
    staff += '</table>' 
    frappe.sendmail(
    		   recipients=['veeramayandi.p@groupteampro.com','sangeetha.a@groupteampro.com','accounts@groupteampro.com'],
#		   recipients=['veeramayandi.p@groupteampro.com'],
             cc = [''],
             subject=('Daily Attendance Report'),
             message="""
                    Dear Sir/Mam,<br>
                    <p>Kindly find the attached Attendance List for Previous day</p>
                    %s
                    """ % (staff)
        ) 
    return True

@frappe.whitelist()    
def daily_emc_report():
    daily_emc= frappe.db.sql("""
	select
		att.employee,
		att.employee_name,
		att.in_time
	from
		`tabAttendance` att
        join `tabEmployee` emp on emp.name = att.employee
		where
        att.attendance_date = DATE_SUB(CURDATE(), INTERVAL 0 DAY)
        and emp.status = 'Active'
	""", as_dict=1)
    staff = ''
    staff += '<table class = table table - bordered style=border-width:2px><tr><td colspan = 3><b>Checkin Report</b></td></tr>'
    staff += '<tr><td>Employee</td><td>Employee Name</td><td>Time</td>'
    for att in daily_emc:
        staff += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(att.employee,att.employee_name,format_datetime(att.in_time) or '') 
    staff += '</table>' 
    frappe.sendmail(
            recipients=['veeramayandi.p@groupteampro.com','sangeetha.a@groupteampro.com','accounts@groupteampro.com'],
#            recipients=['veeramayandi.p@groupteampro.com'],
            cc = [''],
            subject=('Daily Checkin Report'),
            message="""
                    Dear Sir/Mam,<br>
                    <p>Kindly find the attached Employee Checkin List for Today</p>
                    %s
                    """ % (staff)
        ) 
    return True
    

            
    


