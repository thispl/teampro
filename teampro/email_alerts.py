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
	
# @frappe.whitelist()    
# def so_in_draft():
#     so_draft= frappe.db.sql("""select name,customer,service,account_manager,delivery_manager,company,transaction_date,grand_total,per_billed,advance_paid from `tabSales Order` where status ='Draft'""",as_dict=1)
#     draft = ''
#     draft += '<table class = table table - bordered style="border-width:2px"><tr><td colspan = 10><b>SO in Draft</b></td></tr>'
#     draft += '<tr><td>ID</td><td>Customer Name</td><td>Service</td><td>Account Manager</td><td>Delivery manager</td><td>Company</td><td>Date</td><td>Grand Total</td><td>% Amount</td><td>Advance Paid</td></tr>'
#     for s in so_draft:
#         draft += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(s.name,s.customer,s.service,s.account_manager or'',s.delivery_manager or '',s.company,s.transaction_date,s.grand_total,s.per_billed,s.advance_paid or '')
#     draft += '</table>' 
#     frappe.sendmail(
#         recipients=[''],
#         cc = [''],
#         subject=('SO in Draft'),
#         message="""
#                 Dear Sir/Mam,<br>
#                 <p>Kindly check the below attached SO documents in draft</p>
#                 %s <br>
#                 Thanks & Regards<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
#                 """ % (draft)
#     ) 
#     return True

# @frappe.whitelist()    
# def so_in_to_bill():
#     so_to_bill= frappe.db.sql("""select name,customer,service,account_manager,delivery_manager,company,transaction_date,grand_total,per_billed,advance_paid from `tabSales Order` where status ='To Bill'""",as_dict=1)
#     draft = ''
#     draft += '<table class = table table - bordered style="border-width:2px"><tr><td colspan = 10><b>SO To Bill</b></td></tr>'
#     draft += '<tr><td>ID</td><td>Customer Name</td><td>Service</td><td>Account Manager</td><td>Delivery manager</td><td>Company</td><td>Date</td><td>Grand Total</td><td>% Amount</td><td>Advance Paid</td></tr>'
#     for s in so_to_bill:
#         draft += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(s.name,s.customer,s.service,s.account_manager or'',s.delivery_manager or '',s.company,s.transaction_date,s.grand_total,s.per_billed,s.advance_paid or '')
#     draft += '</table>' 
#     frappe.sendmail(
#         recipients=[''],
#         cc = [''],
#         subject=('SO in To Bill'),
#         message="""
#                 Dear Sir/Mam,<br>
#                 <p>Kindly check the below attached SO documents in To Bill</p>
#                 %s <br>
#                 Thanks & Regards<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
#                 """ % (draft)
#     ) 
#     return True

# @frappe.whitelist()    
# def so_in_to_deliver_and_bill():
#     so_draft= frappe.db.sql("""select name,customer,service,account_manager,delivery_manager,company,transaction_date,grand_total,per_billed,advance_paid from `tabSales Order` where status ='To Deliver and Bill'""",as_dict=1)
#     draft = ''
#     draft += '<table class = table table - bordered style="border-width:2px"><tr><td colspan = 10><b>SO in To Deliver and Bill</b></td></tr>'
#     draft += '<tr><td>ID</td><td>Customer Name</td><td>Service</td><td>Account Manager</td><td>Delivery manager</td><td>Company</td><td>Date</td><td>Grand Total</td><td>% Amount</td><td>Advance Paid</td></tr>'
#     for s in so_draft:
#         draft += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(s.name,s.customer,s.service,s.account_manager or'',s.delivery_manager or '',s.company,s.transaction_date,s.grand_total,s.per_billed,s.advance_paid or '')
#     draft += '</table>' 
#     frappe.sendmail(
#         recipients=[''],
#         cc = [''],
#         subject=('SO in To Deliver and Bill'),
#         message="""
#                 Dear Sir/Mam,<br>
#                 <p>Kindly check the below attached SO documents in To Deliver and Bill</p>
#                 %s <br>
#                 Thanks & Regards<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
#                 """ % (draft)
#     ) 
#     return True


from datetime import datetime
@frappe.whitelist()    
def validate_for_easytimepro():
	fromdate=today()
	todate= add_days(today(),30)
	doc_name = frappe.get_doc("Monitoring System for EasytimePRO and EasyWDMS")
	children = doc_name.table_vcma
	for c in children:
		fromdate1 = datetime.strptime(fromdate, '%Y-%m-%d').date()
		todate1 = datetime.strptime(todate, '%Y-%m-%d').date()
		if c.license_validate_upto is not None and  fromdate1 < c.license_validate_upto < todate1:
			print(c.software)
			expiry_date =c.license_validate_upto
			days_diff = (expiry_date - fromdate1).days
			if c.software=="Trial/Demo Login":
				frappe.sendmail(
			recipients=['divya.p@groupteampro.com'],
			# recipients=[c.spoc,c.account_manager,c.project_manager,'gifty.p@groupteampro.com','jenisha.p@groupteampro.com','divya.p@groupteampro.com'],
			subject=('Trial/ Demo Login Expiry Alert - '+ c.project),
			message=f"""
					Dear Sir/Mam,<br>
					<p>This is a reminder that the {c.project} - {c.software} license will expire in next {days_diff} days ({c.license_validate_upto}). Kindly take the necessary action.
					</p>
					<br>
					Thanks & Regards<br>TEAMPRO<br>
					""" % ()
				) 
			else:
				frappe.sendmail(
			# recipients=['divya.p@groupteampro.com'],
			recipients=[c.spoc,c.account_manager,c.project_manager,'gifty.p@groupteampro.com','jenisha.p@groupteampro.com'],
			subject=('EasytimePRO License Renewal - '+ c.project),
			message=f"""
					Dear Sir/Mam,<br>
					<p>This is a reminder that the {c.project} - {c.software} license will expire in next {days_diff} days ({c.license_validate_upto}). Kindly take the necessary action.
					</p>
					<br>
					Thanks & Regards<br>TEAMPRO<br>
					""" % ()
				) 
			print("mail shared")
			print(days_diff)



		######################   Sales Invoice   #####################


# # # # # Sales Invoice New Correction # # # # # #  

from datetime import datetime,date
from frappe.utils import date_diff

@frappe.whitelist()
def sales_invoice_overdue_docs():
	sales_invoice = frappe.get_list("Sales Invoice", filters={"status":["not in",[ "Return","Credit Note Issued","Paid","Cancelled"]]}, fields=["name","company","customer","services","posting_date","due_date","grand_total","outstanding_amount","account_manager","delivery_manager"])
	from datetime import datetime

	def format_currency(amount):
		return "{:,.2f}".format(amount)

	additional = '<br><br><table border=1><tr><td style="background-color:#063970;color:white">S.No</td><td style="background-color:#063970;color:white">Service</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding</td></tr>'
	tfp = '<table border=1><tr style="text-align: center"><td style="background-color:#063970;color:white">ID</td><td style="background-color:#063970;color:white">Services</td><td style="background-color:#063970;color:white">AM</td><td style="background-color:#063970;color:white">DM</td><td style="background-color:#063970;color:white">Customer Name</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding Amount</td><td style="background-color:#063970;color:white">Date</td><td style="background-color:#063970;color:white">Age</td></tr>'

	amount = 0
	grand_total = 0

	for j in sales_invoice:
		postingdate = j.posting_date
		todate = today()
		postingdate1 = datetime.strptime(str(postingdate), '%Y-%m-%d').date()
		todate1 = datetime.strptime(str(todate), '%Y-%m-%d').date()
		j['age'] = (todate1 - postingdate1).days

	sales_invoice_sorted = sorted(sales_invoice, key=lambda x: x['age'], reverse=True)

	for j in sales_invoice_sorted:
		formatted_date = j.get("posting_date").strftime('%d-%m-%Y')
		
		if j.services == 'TFP':
			amount += j.outstanding_amount
			grand_total += j.get('grand_total')
			tfp += '<tr style="font-size:14px"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'.format(
				j['name'], j['services'], j['account_manager'], j['delivery_manager'], j['customer'], format_currency(j['grand_total']), format_currency(j['outstanding_amount']), formatted_date, j['age']
			)

	additional += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format("1.", "TFP", format_currency(grand_total), format_currency(amount))

	tfp += '<tr><td></td><td></td><td style="text-align:center;" colspan=3>Total</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td></td><td></td></tr>'.format(format_currency(grand_total), format_currency(amount))
	tfp += '</table>'

	additional += '</table>'


	
	frappe.sendmail(
		recipients='amirtham.g@groupteampro.com',
		# recipients='divya.p@groupteampro.com',
		cc=['sangeetha.s@groupteampro.com','dineshbabu.k@groupteampro.com','accounts@groupteampro.com'],
		subject='Collection Follow Up-Sales Invoice Report',
		message="""
		<p>Collection Outstanding Report For Further Action.</p>
		TFP : SBMK/AM
		<br>
		{}
		<br>
		{}
		Thanks & Regards,<br>TEAMPRO<br>"This email has been automatically generated. Please do not reply"<br><br>"Initiate further action and intimate a direct manager through email."
		""".format(additional,tfp)
	)

	from datetime import datetime

	def format_currency(amount):
		return "{:,.2f}".format(amount)

	additional = '<br><br><table border=1><tr><td style="background-color:#063970;color:white">S.No</td><td style="background-color:#063970;color:white">Service</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding</td></tr>'
	bcs = '<table border=1><tr style="text-align: center"><td style="background-color:#063970;color:white">ID</td><td style="background-color:#063970;color:white">Services</td><td style="background-color:#063970;color:white">AM</td><td style="background-color:#063970;color:white">DM</td><td style="background-color:#063970;color:white">Customer Name</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding Amount</td><td style="background-color:#063970;color:white">Date</td><td style="background-color:#063970;color:white">Age</td></tr>'

	amount = 0
	grand_total = 0

	
	for j in sales_invoice:
		postingdate = j.posting_date
		todate = today()
		postingdate1 = datetime.strptime(str(postingdate), '%Y-%m-%d').date()
		todate1 = datetime.strptime(str(todate), '%Y-%m-%d').date()
		j['age'] = (todate1 - postingdate1).days

	
	sales_invoice_sorted = sorted(sales_invoice, key=lambda x: x['age'], reverse=True)

	
	for j in sales_invoice_sorted:
		formatted_date = j.get("posting_date").strftime('%d-%m-%Y')
		
		if j.services == 'BCS':
			amount += j.outstanding_amount
			grand_total += j.get('grand_total')
			bcs += '<tr style="font-size:14px"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'.format(
				j['name'], j['services'], j['account_manager'], j['delivery_manager'], j['customer'],format_currency(j['grand_total']),format_currency(j['outstanding_amount']), formatted_date, j['age']
			)

	additional += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format("1.", "BCS", format_currency(grand_total),format_currency(amount))

	bcs += '<tr><td></td><td></td><td style="text-align:center;" colspan=3>Total</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td></td><td></td></tr>'.format(format_currency(grand_total),format_currency(amount))
	bcs += '</table>'

	additional += '</table>'

	
	frappe.sendmail(
		# recipients='siva.m@groupteampro.com',
		# recipients='accounts@groupteampro.com',
		recipients=['chitra.g@groupteampro.com','sangeetha.a@groupteampro.com'],
		cc=['dineshbabu.k@groupteampro.com','accounts@groupteampro.com','sangeetha.s@groupteampro.com'],
		subject='Collection Follow Up-Sales Invoice Report',
		message="""
		<p>Collection Outstanding Report For Further Action.</p>
		BCS : SBMK
		<br>
		{}
		<br>
		{}
		Thanks & Regards,<br>TEAMPRO<br>"This email has been automatically generated. Please do not reply"<br><br>"Initiate further action and intimate a direct manager through email."
		""".format(additional,bcs)
	)

	from datetime import datetime

	def format_currency(amount):
		return "{:,.2f}".format(amount) 

	additional = '<br><br><table border=1><tr><td style="background-color:#063970;color:white">S.No</td><td style="background-color:#063970;color:white">Service</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding</td></tr>'
	rec = '<table border=1><tr style="text-align: center"><td style="background-color:#063970;color:white">ID</td><td style="background-color:#063970;color:white">Services</td><td style="background-color:#063970;color:white">AM</td><td style="background-color:#063970;color:white">DM</td><td style="background-color:#063970;color:white">Customer Name</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding Amount</td><td style="background-color:#063970;color:white">Date</td><td style="background-color:#063970;color:white">Age</td></tr>'

	amount = 0
	grand_total = 0

	
	for j in sales_invoice:
		postingdate = j.posting_date
		todate = today()
		postingdate1 = datetime.strptime(str(postingdate), '%Y-%m-%d').date()
		todate1 = datetime.strptime(str(todate), '%Y-%m-%d').date()
		j['age'] = (todate1 - postingdate1).days

	
	sales_invoice_sorted = sorted(sales_invoice, key=lambda x: x['age'], reverse=True)

	
	for j in sales_invoice_sorted:
		formatted_date = j.get("posting_date").strftime('%d-%m-%Y')
		
		if j['services'] in ['REC-I', 'REC-D']:
			amount += j.outstanding_amount
			grand_total += j.get('grand_total')
			rec += '<tr style="font-size:14px"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'.format(
				j['name'], j['services'], j['account_manager'], j['delivery_manager'], j['customer'],format_currency(j['grand_total']),format_currency(j['outstanding_amount']), formatted_date, j['age']
			)

	additional += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format("1.", "REC-I/REC-D",format_currency(grand_total),format_currency(amount))

	rec += '<tr><td></td><td></td><td style="text-align:center;" colspan=3>Total</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td></td><td></td></tr>'.format(format_currency(grand_total),format_currency(amount))
	rec += '</table>'

	additional += '</table>'
	
	frappe.sendmail(
		# recipients='siva.m@groupteampro.com',
		# # recipients='accounts@groupteampro.com',
		recipients=['sangeetha.a@groupteampro.com'],
		cc=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','accounts@groupteampro.com','annie.m@groupteampro.com'],
		subject='Collection Follow Up-Sales Invoice Report',
		message="""
		<p>Collection Outstanding Report For Further Action.</p>
		REC-I / REC-D : AS/AM
		<br>
		{}
		<br>
		{}
		Thanks & Regards,<br>TEAMPRO<br>"This email has been automatically generated. Please do not reply"<br><br>"Initiate further action and intimate a direct manager through email."
		""".format(additional,rec)
	)

	from datetime import datetime

	def format_currency(amount):
		return "{:,.2f}".format(amount)

	additional = '<br><br><table border=1><tr><td style="background-color:#063970;color:white">S.No</td><td style="background-color:#063970;color:white">Service</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding</td></tr>'
	itsw = '<table border=1><tr style="text-align: center"><td style="background-color:#063970;color:white">ID</td><td style="background-color:#063970;color:white">Services</td><td style="background-color:#063970;color:white">AM</td><td style="background-color:#063970;color:white">DM</td><td style="background-color:#063970;color:white">Customer Name</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding Amount</td><td style="background-color:#063970;color:white">Date</td><td style="background-color:#063970;color:white">Age</td></tr>'

	amount = 0
	grand_total = 0

	
	for j in sales_invoice:
		postingdate = j.posting_date
		todate = today()
		postingdate1 = datetime.strptime(str(postingdate), '%Y-%m-%d').date()
		todate1 = datetime.strptime(str(todate), '%Y-%m-%d').date()
		j['age'] = (todate1 - postingdate1).days

	
	sales_invoice_sorted = sorted(sales_invoice, key=lambda x: x['age'], reverse=True)

	
	for j in sales_invoice_sorted:
		formatted_date = j.get("posting_date").strftime('%d-%m-%Y')
		
		if j['services'] in ['IT-SW', 'IT-IS']:
			amount += j.outstanding_amount
			grand_total += j.get('grand_total')
			itsw += '<tr style="font-size:14px"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'.format(
				j['name'], j['services'], j['account_manager'], j['delivery_manager'], j['customer'],format_currency(j['grand_total']),format_currency(j['outstanding_amount']), formatted_date, j['age']
			)

	additional += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format("1.", "IT-SW/IT-IS",format_currency(grand_total),format_currency(amount))

	itsw += '<tr><td></td><td></td><td style="text-align:center;" colspan=3>Total</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td></td><td></td></tr>'.format(format_currency(grand_total),format_currency(amount))
	itsw += '</table>'

	additional += '</table>'

	
	frappe.sendmail(
		# recipients='siva.m@groupteampro.com',
		# recipients='accounts@groupteampro.com',
		recipients=['dineshbabu.k@groupteampro.com'],
		cc=['anil.p@groupteampro.com','sangeetha.s@groupteampro.com','accounts@groupteampro.com'],
		subject='Collection Follow Up-Sales Invoice Report',
		message="""
		<p>Collection Outstanding Report For Further Action.</p>
		IT-SW / IT-IS : DKB/APP
		<br>
		{}
		<br>
		{}
		Thanks & Regards,<br>TEAMPRO<br>"This email has been automatically generated. Please do not reply"<br><br>"Initiate further action and intimate a direct manager through email."
		""".format(additional,itsw)
	)

	from datetime import datetime

	def format_currency(amount):
		return "{:,.2f}".format(amount)

	additional = '<br><br><table border=1><tr><td style="background-color:#063970;color:white">S.No</td><td style="background-color:#063970;color:white">Service</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding</td></tr>'
	tgt = '<table border=1><tr style="text-align: center"><td style="background-color:#063970;color:white">ID</td><td style="background-color:#063970;color:white">Services</td><td style="background-color:#063970;color:white">AM</td><td style="background-color:#063970;color:white">DM</td><td style="background-color:#063970;color:white">Customer Name</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding Amount</td><td style="background-color:#063970;color:white">Date</td><td style="background-color:#063970;color:white">Age</td></tr>'

	amount = 0
	grand_total = 0

	
	for j in sales_invoice:
		postingdate = j.posting_date
		todate = today()
		postingdate1 = datetime.strptime(str(postingdate), '%Y-%m-%d').date()
		todate1 = datetime.strptime(str(todate), '%Y-%m-%d').date()
		j['age'] = (todate1 - postingdate1).days

	
	sales_invoice_sorted = sorted(sales_invoice, key=lambda x: x['age'], reverse=True)

	
	for j in sales_invoice_sorted:
		formatted_date = j.get("posting_date").strftime('%d-%m-%Y')
		
		if j.services == 'TGT':
			amount += j.outstanding_amount
			grand_total += j.get('grand_total')
			tgt += '<tr style="font-size:14px"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'.format(
				j['name'], j['services'], j['account_manager'], j['delivery_manager'], j['customer'],format_currency(j['grand_total']),format_currency(j['outstanding_amount']), formatted_date, j['age']
			)

	additional += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format("1.", "TGT",format_currency(grand_total),format_currency(amount))

	tgt += '<tr><td></td><td></td><td style="text-align:center;" colspan=3>Total</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td></td><td></td></tr>'.format(format_currency(grand_total),format_currency(amount))
	tgt += '</table>'

	additional += '</table>'
	
	frappe.sendmail(
		# recipients='siva.m@groupteampro.com',
		# recipients='accounts@groupteampro.com',
		recipients='sangeetha.s@groupteampro.com',
		cc=['dineshbabu.k@groupteampro.com','accounts@groupteampro.com'],
		subject='Collection Follow Up-Sales Invoice Report',
		message="""
		<p>Collection Outstanding Report For Further Action.</p>
		TGT : SBMK
		<br>
		{}
		<br>
		{}
		Thanks & Regards,<br>TEAMPRO<br>"This email has been automatically generated. Please do not reply"<br><br>"Initiate further action and intimate a direct manager through email."
		""".format(additional,tgt)
	)


				
	
			
		   