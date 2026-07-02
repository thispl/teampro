import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import get_first_day, get_last_day, format_datetime, get_url_to_form
from frappe.utils import cint
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days
import datetime
import frappe
from frappe.utils import today
from datetime import datetime
import frappe
from frappe.utils import flt
from frappe.utils import nowdate, add_days
from frappe import _
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate
from frappe import throw, msgprint
import frappe
from datetime import date
from frappe import throw, _
from frappe.utils import getdate, today
today = date.today()
from frappe.model.document import Document
import datetime
from frappe.utils import formatdate, get_url
import frappe,erpnext
from frappe.utils import cint
from frappe.utils import validate_email_address
import json
from frappe.utils import date_diff, add_months,today,add_days,add_years,nowdate,flt
from frappe.model.mapper import get_mapped_doc
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
import datetime
from datetime import date,datetime,timedelta
import openpyxl
from openpyxl import Workbook
import openpyxl
import xlrd
import re
from frappe.utils import today
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime
from io import BytesIO
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import GradientFill, PatternFill
import pandas as pd
from frappe.utils import formatdate
from frappe.utils import now
from erpnext.setup.utils import get_exchange_rate
from datetime import date
from six import BytesIO, string_types
from frappe.utils import time_diff
from frappe.utils.csvutils import read_csv_content
from erpnext.buying.doctype.purchase_order.purchase_order import update_status
from frappe.utils.file_manager import get_file
from urllib.parse import urlencode
from frappe.model.rename_doc import rename_doc
from datetime import datetime
from frappe.utils import today


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
			# recipients=['divya.p@groupteampro.com'],
			recipients=[c.spoc,c.account_manager,c.project_manager],
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
			recipients=[c.spoc,c.account_manager,c.project_manager],
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

from datetime import datetime,date
from frappe.utils import date_diff

@frappe.whitelist()
def sales_invoice_overdue_docs():
	sales_invoice = frappe.get_list("Sales Invoice", filters={"status":["not in",[ "Return","Credit Note Issued","Paid","Cancelled"]]}, fields=["name","company","customer","services","posting_date","due_date","grand_total","outstanding_amount","account_manager","delivery_manager","base_total","base_grand_total"])
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
		recipients=['sangeetha.a@groupteampro.com'],
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
			grand_total += j.get('base_grand_total')
			itsw += '<tr style="font-size:14px"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td>{}</td><td style="text-align:right;">{}</td></tr>'.format(
				j['name'], j['services'], j['account_manager'], j['delivery_manager'], j['customer'],format_currency(j['base_grand_total']),format_currency(j['outstanding_amount']), formatted_date, j['age']
			)

	additional += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format("1.", "IT-SW/IT-IS",format_currency(grand_total),format_currency(amount))

	itsw += '<tr><td></td><td></td><td style="text-align:center;" colspan=3>Total</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td></td><td></td></tr>'.format(format_currency(grand_total),format_currency(amount))
	itsw += '</table>'

	additional += '</table>'

	
	frappe.sendmail(
		# recipients='siva.m@groupteampro.com',
		# recipients='accounts@groupteampro.com',
		recipients=['dineshbabu.k@groupteampro.com'],
		cc=['sangeetha.s@groupteampro.com','accounts@groupteampro.com'],
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


import frappe
from frappe.utils import formatdate

@frappe.whitelist()
def send_cr_email(docname,client_mail):
    doc = frappe.get_doc("Task", docname)
    allocated =frappe.session.user
    data = f"""
		<table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>
			<tr style='background-color: #0f1568; color: white; font-size: 17px;'>
				<td colspan=2 style="font-weight:bold">Task Client Review Note</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Meeting ID</td>
				<td style="text-align:left;border: 1px solid black;">{doc.custom_meeting_id or '-'}</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Project</td>
				<td style="text-align:left;border: 1px solid black;">{doc.project or '-'}</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Task ID</td>
				<td style="text-align:left;border: 1px solid black;">{doc.name}</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Task Raised By</td>
				<td style="text-align:left;border: 1px solid black;">{doc.custom_user or '-'}</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Task Statement</td>
				<td style="text-align:left;border: 1px solid black;">{doc.subject or '-'}</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Action Taken</td>
				<td style="text-align:left;border: 1px solid black;">{doc.custom_taskissue_action_taken or '-'}</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Live At</td>
				<td style="text-align:left;border: 1px solid black;">{doc.custom_live_at or '-'}</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Domain</td>
				<td style="text-align:left;border: 1px solid black;">
					<a href='{doc.custom_domain}' target='_blank' style='color: blue; text-decoration: underline;'>{doc.custom_domain}</a>
				</td>
			</tr>

			<tr>
				<td style="font-weight:bold;text-align:left; border: 1px solid black;">Proof</td>
				<td style="text-align:left;border: 1px solid black;">
					<a href='https://erp.teamproit.com/{doc.custom_proof_of_closure_review}' target='_blank'>Link to Proof</a>
				</td>
			</tr>
		</table>
		"""

    # Send email
    frappe.sendmail(
        sender=allocated,
        recipients=client_mail,
        cc=["dineshbabu.k@groupteampro.com","abdulla.pi@groupteampro.com"],
        # recipients="divya.p@groupteampro.com",
        subject=f"Task- {doc.name} Pending for Final Review and Acknowledgement -reg",
        message=f"""
            <p>Dear Patron,</p>

            <p>Greetings from TEAMPRO !!!</p>

            <p>The following  Task has been completed and tested by the Delivery Manager and forwarded for your final review, please confirm if it satisfies all your requirement and reply back as Completed or if you feel it is still pending for some action please give your remark, will re-open the task and share you the completion status along with root cause.</p>

            {data}<br>
<br>
            
            Thanks & Regards,<br>TEAM ERP<br>
            <i>This email has been automatically generated. Please do not reply</i>
        """
    )
    return "Email Sent Successfully"
			
@frappe.whitelist()
def intimate_task_completion(task):
    taskid = frappe.get_doc('Task', task)
    message = frappe.render_template(
        "teampro/templates/intimate_task_completion.html",
        {"doc": taskid},
    )
    frappe.sendmail(
        recipients=[taskid.account_manager,
                    taskid.project_manager, taskid.custom_allocated_to],
        cc=[taskid.spoc],
        message=message,
        subject=_("Task Pending Review - Intimation"),
    )

@frappe.whitelist()
def rns_mail(project):
    data = ''
    project_doc = frappe.get_doc("Project",project)
    data += 'Project %s has been returned to R&S'%(project_doc.name)
    created_by=project_doc.owner
    frappe.sendmail(
        recipients=created_by,
        message=data,
        subject=_("Project Returned -  %s" %(project_doc.project_name)),
    )
			
@frappe.whitelist()
def confirm_mail(project):
    data = ''
    project_doc = frappe.get_doc("Project",project)
    data += 'Project %s has been confirmed to OPS'%(project_doc.name)
    frappe.sendmail(
        recipients=['dineshbabu.k@groupteampro.com',"sangeetha.s@groupteampro.com","sangeetha.a@groupteampro.com","sams@groupteampro.com","dm@groupteampro.com"],
        message=data,
        subject=_("Project Confirmed -  %s" %(project_doc.project_name)),
    )	   

from frappe import _

@frappe.whitelist()
def meeting_mail(meet):
    meet_doc = frappe.get_doc("Meeting",meet)
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '''
<tr style="background-color: #063970;">
    <td width="5%" style="text-align:center;color:white;">S.No</td>
    <td width="75%" style="text-align:center;color:white;">Description</td>
    <td width="10%" style="text-align:center;color:white;">Action</td>
    <td width="10%" style="text-align:center;color:white;">CB</td>
</tr>
'''

    ind = 1
    recipients = []
    cc = []
    for i in meet_doc.minutes:
        if i.custom_action in ["Info", "SOP-U"]:
            action_val = i.custom_action
        elif i.custom_action in ["Task", "To Do"]:
            action_val = getattr(i, 'custom_id', '')
        else:
            action_val = i.custom_action or ''
        data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(ind, i.description, action_val, i.get_formatted('complete_by'))
        ind += 1
    data += '</table>'
    for j in meet_doc.attendees:
        if j.attended == '1':
            recipients.append(j.attendee)
        else:
            cc.append(j.attendee)

    for i in meet_doc.external_attendees:
        if validate_email_address(i.attendee):
            recipients.append(i.attendee)
            
    attachments = []
    for file in frappe.get_all("File",filters={"attached_to_doctype": "Meeting", "attached_to_name": meet},fields=["file_url", "file_name"]):
        attachments.append({
            "file_url": file.file_url
        })   
    
    


    frappe.sendmail(
        recipients=recipients,
        cc=cc,
        subject=_("Minutes of Meeting -  %s on %s " % (meet_doc.title, formatdate(meet_doc.date))),
        message="""
            Dear Sir/Madam,<br>Kindly Find the below List of MOM points against the meeting happened at {} {}<br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
            """.format(formatdate(meet_doc.date), data),
        attachments=attachments        
    )
    return "Ok"

@frappe.whitelist()
def closure_mail(subject,id,owner,action_taken,live,et,at,revision,service,proof,allocated=None,project=None,issue=None,domain=None,spoc=None,reason=None,dev_spoc=None,et_remark=None):
    if service=='IT-SW':
        percentage=et_at_calculation(id, et, at, allocated,subject)
        reports=frappe.db.get_value("Employee",{'user_id':allocated},['reports_to'])
        reports_to=frappe.db.get_value("Employee",{'name':reports},['user_id'])
        tl=frappe.db.get_value("Employee",{'user_id':allocated},["custom_tl"])
        tl_mail=frappe.db.get_value("Employee",{'name':tl},['user_id'])
        et_rate= 'ET : %s and AT : %s'%(et,round(percentage,2))
        if issue:
            raised_by=frappe.db.get_value("Issue",{'name':issue},['raised_by'])
        else:
            raised_by='None'
        
        data = ''
        data += f"<table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>\
        <tr><td colspan='2' style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black;'><b>Task / Issue Pending Review Note</b></td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Task ID</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/app/task/{id}' target='_blank'>{id}</a></td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Project</b></td><td style='border: 1px solid black;'>{project}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task Raised By</b></td><td style='border: 1px solid black;'>{owner}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue ID</b></td><td style='border: 1px solid black;'>{issue}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Raised By</b></td><td style='border: 1px solid black;'>{raised_by}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Statement</b></td><td style='border: 1px solid black;'>{subject}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Action Taken</b></td><td style='border: 1px solid black;'>{action_taken}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Live At</b></td><td style='border: 1px solid black;'>{live}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Domain</b></td><td style='border: 1px solid black;'><a href='{domain}' target='_blank' style='color: blue; text-decoration: underline;'>{domain}</a></td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Proof</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/{proof}' target='_blank'>Link to Proof</a></td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>ET & AT</b></td><td style='border: 1px solid black;'>{et_rate}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Re-Open Count</b></td><td style='border: 1px solid black;'>{revision}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Cause of Re-Open</b></td><td style='border: 1px solid black;'>{reason}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>ET VS AT Remark</b></td><td style='border: 1px solid black;'>{et_remark}</td></tr></table>"

        cc = [reports_to, allocated,spoc] +([tl_mail] if tl_mail else [])
        if spoc!="dineshbabu.k@groupteampro.com":
            frappe.sendmail(
                sender=allocated,
                recipients=spoc,
                cc=cc,
                subject='Task : %s Pending Review : Forward for Review to Mark Completion or Re-Open' % id,
                message = """
                <b>Dear Patron,<br><br>Greeting !!!</b><br><br>
            The attached Task has been completed by Development and forwarded for your kind review, please confirm if it satisfies all your requirement and Mark the Task Status as Client Review / Completed or if you feel it is still pending for some action please change the status as “OPEN” and give your remark for Re-open <br><br>
            {}<br><br>
                Thanks & Regards,<br>TEAM ERP<br>

                <i>This email has been automatically generated. Please do not reply</i>
                """.format(data)
            )

@frappe.whitelist()
def et_at_calculation(id, et, at, allocated,subject):
    today_date = datetime.now().strftime('%Y-%m-%d')
    emp_id = frappe.db.get_value("Employee", {'user_id': allocated}, 'name')
    emp_name = frappe.db.get_value("Employee", {'name': emp_id}, 'employee_name')
    timesheets = frappe.get_all("Timesheet",{'employee': emp_id, 'docstatus': ['!=',2]},['name'])
    overall_at = 0.0
    if timesheets:
        for timesheet in timesheets:
            time_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet['name'], 'task': id}, fields=['hours'])
            for log in time_logs:
                overall_at += log['hours']
    else:
        overall_at = 0.0
    return overall_at

@frappe.whitelist()
def send_mail_for_profile_submission(project):
    pro=frappe.get_doc("Project",{"name":project})
    posting_date = datetime.now().strftime("%d-%m-%Y")
    spoc=pro.spoc
    table = '<table text-align="center" border="1" width="75%" style="border-collapse: collapse;">'
    table += '<tr style="background-color: #87CEFA"><td style= width="1%;font-weight: bold;"><b>Project</b></td><td style= width="1%";font-weight: bold;"><b>Task ID</b></td><td style="width:1%; font-weight: bold;">Position</td><td style="width: 1%; font-weight: bold;">#Profiles</td><td style="width:2%; font-weight: bold;">Date</td></tr>'
    for i in pro.custom_profile_submission:
        formatted_date = frappe.utils.formatdate(i.date, 'dd-mm-yyyy')
        table+="""<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"""%(i.project,i.task,i.position,i.profiles,formatted_date)
    table+='</table>'
    subject="New Project Batch Profile Submission Plan-  %s" % posting_date
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below Project Details:<p><b>Project Name:</b>{}<p><b>Project ID:</b>{}<p><b>Project Manager</b>{}<p> A new project has been opened for your further action.<br>Kindly find the 1 st batch profile submission plan<br>{}<br></p><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(pro.project_name,pro.name,pro.project_manager,table)
    frappe.sendmail(
        # recipients=["divya.p@groupteampro.com"],
        recipients=["sangeetha.a@groupteampro.com","dineshbabu.k@groupteampro.com","sangeetha.s@groupteampro.com","aruna.g@groupteampro.com",spoc],
        subject=subject,
        message=message
    )

@frappe.whitelist()
def project_send_mail_to_creation_adv(name):
# def project_send_mail_to_creation_adv():
#     name ="PROJ-2011"
    posting_date = datetime.now().strftime("%d-%m-%Y")
    pro = frappe.get_doc("Project",name)
    tasks = frappe.get_all("Task",{'project': pro.name},['*'])
    t=frappe.db.get_all("Task",{'project': pro.name},['food'],group_by='food')
    food_count=len(t)
    qualification=frappe.get_all("Task",{'project': pro.name},['qualification_type'],group_by='qualification_type')
    qual_count=len(qualification)
    experience=frappe.get_all("Task",{'project': pro.name},['total_experience'],group_by='total_experience')
    exp_count=len(experience)
    g_experience=frappe.get_all("Task",{'project': pro.name},['gulf_experience'],group_by='gulf_experience')
    g_exp=len(g_experience)
    interview=frappe.get_all("Task",{'project': pro.name},['mode_of_interview'],group_by='mode_of_interview')
    int_count=len(interview)
    acc=frappe.get_all("Task",{'project': pro.name},['accommodation'],group_by='accommodation')
    a_count=len(acc)
    transport=frappe.get_all("Task",{'project': pro.name},['transportation'],group_by='transportation')
    trans_count=len(transport)
    visa=frappe.get_all("Task",{'project': pro.name},['visa_type'],group_by='visa_type')
    v_count=len(visa)
    con=frappe.get_all("Task",{'project': pro.name},['contract_period_year'],group_by='contract_period_year')
    con_count=len(con)
    categorys=frappe.get_all("Task",{'project': pro.name},['category'],group_by='category')
    ca_count=len(categorys)
    keys=frappe.get_all("Task",{'project': pro.name},['custom_major_key_skills'],group_by='custom_major_key_skills')
    key_count=len(keys)
    rec=frappe.get_all("Task",{'project': pro.name},['custom_free_recruitment'],group_by='custom_free_recruitment')
    rec_count=len(rec)
    task_count=(frappe.db.count("Task",{'project': pro.name}))
    serial_no = 1
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: left;">'
    table += '<tr style="background-color: #87CEFA"><td style="width: 10%; font-weight: bold; text-align: center;">S.NO</td><td style="width: 30%; font-weight: bold; text-align: center;">Title</td><td style="width: 60%; font-weight: bold; text-align: center;">Details</td></tr>'
    table += """<tr><td style="text-align: center;">1</td><td>Project ID</td><td>{}</td></tr>""".format(pro.name or '')
    table += """<tr><td style="text-align: center;">2</td><td>Date</td><td>{}</td></tr>""".format(pro.custom_actionconfirmed_datetime or '')
    table += """<tr><td style="text-align: center;">3</td><td>Country</td><td>{}</td></tr>""".format(pro.territory or '')
    table += """<tr><td style="text-align: center;">4</td><td>Client</td><td>{}</td></tr>""".format(pro.customer or '')
    for i in tasks:
        if tasks.index(i)==0:
            table += """<tr><td rowspan={} style="text-align: center;">5</td><td rowspan={}>Positions</td><td>{}</td></tr>""".format(task_count,task_count,i.subject or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(i.subject or '')
    for k in keys:
        if keys.index(k)==0:
            table += """<tr><td rowspan={} style="text-align: center;">6</td><td rowspan={}>Major Key Skills</td><td>{}</td></tr>""".format(key_count,key_count,k.custom_major_key_skills or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(k.custom_major_key_skills or '')
    for d in qualification:
        if qualification.index(d)==0:
            table += """<tr><td rowspan={} style="text-align: center;">7</td><td rowspan={}>Qualification</td><td>{}</td></tr>""".format(qual_count,qual_count,d.qualification_type or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(d.qualification_type or '')
    for e in experience:
        if experience.index(e)==0:
            table += """<tr><td rowspan={} style="text-align: center;">8</td><td rowspan={}>Experience</td><td>{}</td></tr>""".format(exp_count,exp_count,e.total_experience or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(e.total_experience or '')
    for g in g_experience:
        if g_experience.index(g)==0:
            table += """<tr><td rowspan={} style="text-align: center;">9</td><td rowspan={}>GCC Experience</td><td>{}</td></tr>""".format(g_exp,g_exp,g.gulf_experience or '')
        else:
            table +="""<tr><td>{}</td></tr>""".format(g.gulf_experience or '')
    for r in rec:
        if rec.index(r)==0:
            table += """<tr><td rowspan={} style="text-align: center;">10</td><td rowspan={}>Free Recruitment</td><td>{}</td></tr>""".format(rec_count,rec_count,r.custom_free_recruitment or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(r.custom_free_recruitment or '')
    for m in interview:
        if interview.index(m)==0:
            table += """<tr><td rowspan={} style="text-align: center;">11</td><td rowspan={}>Mode Of Interview</td><td>{}</td></tr>""".format(int_count,int_count,m.mode_of_interview or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(m.mode_of_interview or '')
    
    table += """<tr><td style="text-align: center;">12</td><td>If Direct Client Interview - Location & Date</td><td></td></tr>"""
    table += """<tr><td style="text-align: center;">13</td><td>Food</td><td>{}</td></tr>""".format(pro.food or '')
    table += """<tr><td style="text-align: center;">14</td><td>Accommodation</td><td>{}</td></tr>""".format(pro.accommodation or '')
    table += """<tr><td style="text-align: center;">15</td><td>Transportation</td><td>{}</td></tr>""".format(pro.transportation or '')
    table += """<tr><td style="text-align: center;">16</td><td>Contact Number</td><td>+91 75502 24400/+9191503 93908</td></tr>"""
    table += """<tr><td style="text-align: center;">17</td><td>Mail ID</td><td>aruna.g@groupteampro.com</td></tr>"""
    for v in visa:
            if visa.index(v)==0:
                table += """<tr><td style="text-align: center;" rowspan={}>18</td><td rowspan={}>Visa Type</td><td>{}</td></tr>""".format(v_count,v_count,v.visa_type or '')
            else:
                table += """<tr><td>{}</td></tr>""".format(v.visa_type or '')
    for cons in con:
            if con.index(cons)==0:
                table += """<tr><td style="text-align: center;" rowspan={}>19</td><td rowspan={}>Contract</td><td>{}</td></tr>""".format(con_count,con_count,cons.contract_period_year or '')
            else:
                table += """<tr><td>{}</td></tr>""".format(cons.contract_period_year or '')
    for cat in categorys:
            if categorys.index(cat)==0:
                table += """<tr><td style="text-align: center;" rowspan={}>20</td><td rowspan={}>ECR/ECNR</td><td>{}</td></tr>""".format(ca_count,ca_count,cat.category or '')
            else:
                table += """<tr><td>{}</td></tr>""".format(cat.category or '')
    table += """<tr><td style="text-align: center;" >21</td><td>Special Remarks</td><td>Attractive Salary</td></tr>"""
    table += """<tr><td style="text-align: center;" >22</td><td>Common</td><td>Company Name + Logo + RA Licence + Location + Website + Common Number (7305056202)(7550224400) +  sangeetha.a@groupteampro.com</td></tr>"""
    table += '</table>'
    subject = "Advertisement Details - %s" %posting_date
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below Advertisement Confirmed Details:<br><br>{}<br><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(table)
    frappe.sendmail(
        # recipients=["jothi.m@groupteampro.com"],
        recipients=["cv@groupteampro.com","aruna.g@groupteampro.com","sangeetha.s@groupteampro.com"],
        subject=subject,
        message=message
    )
    
@frappe.whitelist()
def new_project_creation_mail(name):
    create=frappe.get_doc("Project",name)
    posting_date = datetime.now().strftime("%d-%m-%Y")
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table += '<tr style="background-color: #87CEFA"><td style="width: 10%; font-weight: bold; text-align: center;">S.NO</td><td style="width: 30%; font-weight: bold; text-align: center;">Title</td><td style="width: 60%; font-weight: bold; text-align: center;">Details</td></tr>'
    table += """<tr><td>1</td><td>Project ID</td><td>{}</td></tr>""".format(create.name or '')
    table += """<tr><td>2</td><td>Project Name</td><td>{}</td></tr>""".format(create.project_name or '')
    table += """<tr><td>3</td><td>Customer</td><td>{}</td></tr>""".format(create.customer or '')
    table += """<tr><td>4</td><td>Mode Of Interview</td><td>{}</td></tr>""".format(create.mode_of_interview or '')
    table += """<tr><td>5</td><td>#Positions</td><td>{}</td></tr>""".format(create.task or '')
    table += """<tr><td>6</td><td>#vacancies</td><td>{}</td></tr>""".format(create.tvac or '')
    table+='</table>'
    subject="Project Created-  %s" % posting_date
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below project Created Details:<p><b>Project Name:</b>{}<p><b>Project ID:</b>{}– a new project has been created for your further action.<br>{}<br></p><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(create.project_name,create.name,table)
    frappe.sendmail(
        # recipients=["divya.p@groupteampro.com"],
        recipients=["sangeetha.a@groupteampro.com","dineshbabu.k@groupteampro.com","sangeetha.s@groupteampro.com","aruna.g@groupteampro.com"],
        subject=subject,
        message=message
    )
    
@frappe.whitelist()
def send_appraisal_mail(doc,method):
    
    employee_email = frappe.db.get_value("Employee", doc.employee, "user_id")
    cc_emails = []
    hod = frappe.db.get_value("Employee", doc.employee, "reports_to")
    if hod:
        hod_email = frappe.db.get_value("Employee", hod, "user_id")
        if hod_email:
            cc_emails.append(hod_email)
    for fixed_email in ["dineshbabu.k@groupteampro.com", "sangeetha.s@groupteampro.com"]:
        if fixed_email not in cc_emails:
            cc_emails.append(fixed_email)
    kra_html = """
    <table border='1' cellspacing='0' cellpadding='5' style='border-collapse: collapse;'>
        <tr style="background-color: #00008b;color:white">
            <th>Goal</th>
            <th>Description</th>
            <th>Weightage (%)</th>
            <th>Score (0-5)</th>
            <th>Score Earned</th>
        </tr>
    """
    for kra in doc.goals:
        kra_html += f"""
        <tr>
            <td>{kra.kra or ''}</td>
            <td>{kra.description or ''}</td>
            <td style="text-align:right">{flt(kra.per_weightage, 2):.2f}</td>
            <td style="text-align:right">{flt(kra.score, 2):.2f}</td>
            <td style="text-align:right">{flt(kra.score_earned, 2):.2f}</td>
        </tr>
        """
    kra_html += "</table>"
    subject = f"Appraisal Submitted - {doc.employee_name}"
    message = f"""
    <p>Dear {doc.employee_name},</p>
    <p>Greetings from TEAMPRO,<br>
    This is to inform you that the appraisal for the month of <b>{doc.custom_appraisal_cycle_month}</b> has been concluded with the following score sheet:</p>
    <p style="font-size:18px;"><b>Total Goal Score:</b> {flt(doc.total_score, 2):.2f}</p>
    <p style="font-size:18px;"><b>Total ENS:</b> {flt(doc.custom_total_ens, 2):.2f}</p>
    <p><b>KRA Details:</b></p>
    {kra_html}
    <p><b>Reviewer Remark:</b> {doc.custom_reviewer_remark or 'No remarks provided'}</p>
    <p>Regards,<br>TEAMPRO</p>
    """
    frappe.sendmail(
        recipients=[employee_email],
        cc=cc_emails,
        # recipients='riyaz.a@groupteampro.com',
        subject=subject,
        message=message
    )

@frappe.whitelist()
def set_to_enquiry(docname):
    doc = frappe.get_doc("Project", docname)
    if doc.status == "Draft" or doc.status == "Clarification":
        doc.status = "Enquiry"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

        recipients = [email for email in [PM, SPOC, AM, DM] if email]
        # recipients = "bhuvaneswari.a@groupteampro.com"
        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"{doc.project_name} - Status Changed to {doc.status}",
                message=f"<p>Mail2</p>"
            )
            return "Mail Sent"
        else:
            frappe.msgprint("Mail ID not set for PM, SPOC, AM, DM")

@frappe.whitelist()
def send_clarification_mail(docname, emails):
    doc = frappe.get_doc("Project", docname)
    email_list = [e.strip() for e in emails.split(",") if e.strip()]

    subject = f"{doc.project_name} - Status Changed to {doc.status}"
    message = f"Mail1"

    frappe.sendmail(
        recipients=email_list,
        subject=subject,
        message=message
    )

@frappe.whitelist()
def change_to_kickoff(docname):
    doc = frappe.get_doc("Project", docname)
    if doc.status == "Enquiry":
        doc.status = "Kick OFF"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

        recipients = [email for email in [PM, SPOC, AM, DM] if email]
        # recipients = "bhuvaneswari.a@groupteampro.com"
        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"{doc.project_name} - Status Changed to {doc.status}",
                message=f"<p>Mail4</p>"
            )
        return "Mail Sent"
    
@frappe.whitelist()
def set_to_cancelled(docname):
    doc = frappe.get_doc("Project", docname)
    doc.status = "Cancelled"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

    recipients = [email for email in [PM, SPOC, AM, DM] if email]

    # recipients = ["bhuvaneswari.a@groupteampro.com"]
    subject = f"{doc.project_name} - Status Changed to {doc.status}"
    message = f"Mail3"

    frappe.sendmail(recipients=recipients, subject=subject, message=message)
    return "Mail sent"

@frappe.whitelist()
def change_to_working(docname):
    doc = frappe.get_doc("Project", docname)
    if doc.status == "Open":
        doc.status = "Working"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

        recipients = [email for email in [PM, SPOC, AM, DM] if email]
        # recipients = "bhuvaneswari.a@groupteampro.com"
        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"{doc.project_name} - Status Changed to {doc.status}",
                message=f"<p>Mail6</p>"
            )
        return "Mail Sent"

@frappe.whitelist()
def change_to_hold(docname):
    doc = frappe.get_doc("Project", docname)
    if doc.status == "Open":
        doc.status = "Hold"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

        recipients = [email for email in [PM, SPOC, AM, DM] if email]
        # recipients = "bhuvaneswari.a@groupteampro.com"
        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"{doc.project_name} - Status Changed to {doc.status}",
                message=f"<p>Mail9</p>"
            )
        return "Mail Sent"
    
@frappe.whitelist()
def change_to_complete(docname):
    doc = frappe.get_doc("Project", docname)
    doc.status = "Completed"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

    recipients = [email for email in [PM, SPOC, AM, DM] if email]

    subject = f"{doc.project_name} - Status Changed to {doc.status}"
    message = f"Mail7"

    frappe.sendmail(recipients=recipients, subject=subject, message=message)
    return "Mail sent"

@frappe.whitelist()
def change_to_cancel(docname, reason):
    doc = frappe.get_doc("Project", docname)
    doc.status = "Cancelled"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

    recipients = [email for email in [PM, SPOC, AM, DM] if email]

    # recipients = ["bhuvaneswari.a@groupteampro.com"]
    subject = f"{doc.project_name} - Status Changed to {doc.status}"
    message = f"Mail8"

    frappe.sendmail(recipients=recipients, subject=subject, message=message)
    return "Mail sent"

@frappe.whitelist()
def change_to_open(docname):
    doc = frappe.get_doc("Project", docname)
    PM, SPOC, AM, DM = frappe.db.get_value("Project", doc.name, ["project_manager","spoc","account_manager","custom_delivery_manager"] )

    recipients = [email for email in [PM, SPOC, AM, DM] if email]
    # recipients = "bhuvaneswari.a@groupteampro.com"
    if recipients:
        frappe.sendmail(
            recipients=recipients,
            subject=f"{doc.project_name} - Status Changed to {doc.status}",
            message=f"<p>Mail5</p>"
        )
    return "Mail Sent"

@frappe.whitelist()
def auto_mail_to_sams(project,territory):
    task =frappe.get_all("Task",filters = {"project":project}, fields = ["*"])
    for t in task:
        sams =frappe.db.sql("""select email_address,person_name from`tabSAMS` where NOT sa_status= "Do Not Contact" """,as_dict=True)
        for s in sams:
            vacancy =t.vac * t.prop
            frappe.sendmail(
                recipients=["sarumathy.d@groupteampro.com"],
                subject='Regarding Vacancy' ,
                message="""<p>Dear %s,</p>
                <p>Greetings From TEAMPRO !!! <br>
                    We are always happy to be associated with you, and appreciate your sincere efforts to be support us in recruitment.
                    We have a manpower requirement������������������������������������������������������������������������������������������������������������������������������������������������������������������for once of our reputed client in %s������������������������������������������������������������������������������������������������������������������������������������������������������������������; The details for project is as below:
                    <table class='table table-bordered'>
                    <tr>
                    <th>Position</th>  <th>Vacancy</th>  <th> Valid till</th>
                    </tr>
                    <tr>
                     <td> %s </td> <td> %s </td> <td> %s </td>
                    </tr>
                     </table>
                     <br>
                     <table class='table table-bordered'>
                     <tr>
                    <th> Job Requirement</th> 
                    </tr>
                    <tr>
                    <th> Qualification Type </th>   <th> Temp Qualification </th> <th>Minimum Experience</th>  <th>Total Experience</th>
                    </tr>
                    <tr>
                    <td> %s </td>   <td> %s </td> <td> %s </td> <td> %s </td>
                    </tr>
                    <tr>
                    <th> Salary Type </th>  <th>Specialization</th> <th> Maximum Experience </th> <th>Currency</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                    <tr>
                    <th> Category </th>  <th>Gulf Experience</th> <th> Amount </th> <th>Driving Licence (If any)</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                     </table>
                     <br>
                     <table class='table table-bordered'>
                     <tr>
                    <th>Job Description </th> 
                    </tr>
                    <tr>
                    <td> %s </td>
                    </tr>
                     </table>
                     <br>
                     <table class='table table-bordered'>
                    <tr>
                    <th>Allowance and Benefits  </th> 
                    </tr>
                    <tr>
                    <th> Working Days/HRS </th>  <th> Food </th> <th>Visa Type </th> <th>Transportation </th> 
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                     <tr>
                    <th> Accommodation </th>  <th> Nationality </th> <th>  Contract Period Year</th> <th> Contract Period  Month</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                    <tr>
                    <th>  Over Time </th>  <th> Joining Ticket </th> <th> Leave </th> <th> Any Other Allowance</th>
                    </tr>
                    <tr>
                    <td> %s </td>  <td>%s</td> <td> %s </td> <td> %s </td>
                    </tr>
                    </table>
                    <br>
                    Please contact us at������������������������������������������������������������������������������������������������������������������������������������������������������������������+91 73050 56202������������������������������������������������������������������������������������������������������������������������������������������������������������������/������������������������������������������������������������������������������������������������������������������������������������������������������������������+91 73050 56203������������������������������������������������������������������������������������������������������������������������������������������������������������������/������������������������������������������������������������������������������������������������������������������������������������������������������������������+91 73050 56201������������������������������������������������������������������������������������������������������������������������������������������������������������������/������������������������������������������������������������������������������������������������������������������������������������������������������������������+91 7550224400
                    or write to us at������������������������������������������������������������������������������������������������������������������������������������������������������������������cv@groupteampro.com������������������������������������������������������������������������������������������������������������������������������������������������������������������/������������������������������������������������������������������������������������������������������������������������������������������������������������������hr@groupteampro.com
                    </p> 
                    <style>
                    th {
                        background-color:989898
                    }
                    </style>
                    """ % (s.person_name,territory,t.subject,vacancy,t.exp_end_date ,t.qualification_type,t.temp_qualification,
                    t.minimum_experience,t.total_experience, t.salary_type,t.specialization,t.maximum_experience,t.currency,t.category,t.gulf_experience,
                    t.amount ,t.driving_licence ,t.description,t.working_days,t.food,t.visa_type,t.transportation,t.accommodation,t.nationality,
                    t.contract_period_year,t.contract_period__month,t.over_time,t.joining_ticket,t.leave,t.any_other_allowance,))

@frappe.whitelist()     
def on_click_create_mail(project,name,task,vac):
    create=frappe.get_doc("Project",name)
    table = '<table text-align="center" border="1" width="25%" style="border-collapse: collapse;">'
    table += '<tr style="background-color: #87CEFA"><td style= width="1%";font-weight: bold;">Task ID</td><td style="width:1%; font-weight: bold;">Subject</td><td style="width: 1%; font-weight: bold;">No of Vacancies</td><td style="width:1%; font-weight: bold;">SP</td></tr>'
    task=frappe.db.get_all("Task",{'project':name},['name','subject','vac','sp'])
    for i in task:
        tot_sp=frappe.db.sql("""SELECT sum(sp) as sp from `tabTask` where project=%s group by project""",(create.name),as_dict=True)[0]
        tot_vac=frappe.db.sql("""SELECT sum(vac) as vac from `tabTask` where project=%s group by project""",(create.name),as_dict=True)[0]
        table+="""<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"""%(i.name,i.subject,i.vac,i.sp)
    table+="""<tr><td colspan=2 style="text-align: center;">Total</td><td>%s</td><td>%s</td></tr>"""%(round(tot_vac['vac']) or '',round(tot_sp['sp']) or '')
    table+='</table>'
    subject="Action Created-  %s" % nowdate()
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below Action Created Details:<p><b>Project Name:</b>{}<p><b>Project ID:</b>{}– a new project has been created for your further action.<br>{}<br></p><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(create.project_name,create.name,table)
    frappe.sendmail(
        # recipients=["divya.p@groupteampro.com"],
        recipients=["sangeetha.a@groupteampro.com","dineshbabu.k@groupteampro.com","sangeetha.s@groupteampro.com"],
        subject=subject,
        message=message
    )

@frappe.whitelist()     
def on_click_confirm_mail(project,name):
    create=frappe.get_doc("Project",name)
    # det=frappe.db.get_all("Task",{'project_name':'project','project':'name'})
    table= '<table text-align="center" border="1" width="25%" style="border-collapse: collapse;">'
    table += '<tr style="background-color: #87CEFA"><td style="width:1%; font-weight: bold;">Task ID</td><td style="width: 1%; font-weight: bold;">Subject</td><td style="width: 1%; font-weight: bold;">No of Vacancies</td><td style="width: 1%; font-weight: bold;">#SP</td><td style="width: 1%; font-weight: bold;">Date Batch-1</td><td style="width: 1%; font-weight: bold;">Date Batch-2</td></tr>'
    task=frappe.db.get_all("Task",{'project':name},['name','subject','vac','sp'])
    manager=frappe.db.get_value("Project",{'name':name},['account_manager'])
    for i in task:
        tot_sp=frappe.db.sql("""SELECT sum(sp) as sp from `tabTask` where project=%s group by project""",(create.name),as_dict=True)[0]
        tot_vac=frappe.db.sql("""SELECT sum(vac) as vac from `tabTask` where project=%s group by project""",(create.name),as_dict=True)[0]
        table+="""<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td></td><td></td></tr>"""%(i.name,i.subject,i.vac,i.sp)
    table+="""<tr><td colspan=2 style="text-align: center;">Total</td><td>%s</td><td>%s</td><td></td><td></td></tr>"""%(round(tot_vac['vac']) or '',round(tot_sp['sp']) or '')
    table+='</table>'
    subject="Action Confirmed-  %s" % nowdate()
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below Action Created Details:<p><b>Project Name:{}</b><p><b>Project ID:</b>{}– has been confirmed for execution by OPS Team.<br>{}<br></p><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(create.project_name,create.name,table)
    frappe.sendmail(
        # recipients=["divya.p@groupteampro.com"],
        recipients=["dineshbabu.k@groupteampro.com","sangeetha.s@groupteampro.com","annie.m@groupteampro.com",manager],
        subject = subject,
        message=message
    
        ) 
    

@frappe.whitelist()
def send_mail_to_creation_adv(name):
    pro = frappe.get_doc("Project",name)
    tasks = frappe.get_all("Task",{'project': pro.name},['*'])
    t=frappe.db.get_all("Task",{'project': pro.name},['food'],group_by='food')
    food_count=len(t)
    qualification=frappe.get_all("Task",{'project': pro.name},['qualification_type'],group_by='qualification_type')
    qual_count=len(qualification)
    experience=frappe.get_all("Task",{'project': pro.name},['total_experience'],group_by='total_experience')
    exp_count=len(experience)
    g_experience=frappe.get_all("Task",{'project': pro.name},['gulf_experience'],group_by='gulf_experience')
    g_exp=len(g_experience)
    interview=frappe.get_all("Task",{'project': pro.name},['mode_of_interview'],group_by='mode_of_interview')
    int_count=len(interview)
    acc=frappe.get_all("Task",{'project': pro.name},['accommodation'],group_by='accommodation')
    a_count=len(acc)
    transport=frappe.get_all("Task",{'project': pro.name},['transportation'],group_by='transportation')
    trans_count=len(transport)
    visa=frappe.get_all("Task",{'project': pro.name},['visa_type'],group_by='visa_type')
    v_count=len(visa)
    con=frappe.get_all("Task",{'project': pro.name},['contract_period_year'],group_by='contract_period_year')
    con_count=len(con)
    categorys=frappe.get_all("Task",{'project': pro.name},['category'],group_by='category')
    ca_count=len(categorys)
    keys=frappe.get_all("Task",{'project': pro.name},['custom_major_key_skills'],group_by='custom_major_key_skills')
    key_count=len(keys)
    rec=frappe.get_all("Task",{'project': pro.name},['custom_free_recruitment'],group_by='custom_free_recruitment')
    rec_count=len(rec)
    task_count=(frappe.db.count("Task",{'project': pro.name}))
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table += '<tr style="background-color: #87CEFA"><td style="width: 10%; font-weight: bold; text-align: center;">S.NO</td><td style="width: 30%; font-weight: bold; text-align: center;">Title</td><td style="width: 60%; font-weight: bold; text-align: center;">Details</td></tr>'
    table += """<tr><td></td><td>Project ID</td><td>{}</td></tr>""".format(pro.name or '')
    table += """<tr><td></td><td>Date</td><td>{}</td></tr>""".format(pro.custom_actionconfirmed_datetime or '')
    table += """<tr><td>1</td><td>Country</td><td>{}</td></tr>""".format(pro.territory or '')
    table += """<tr><td></td><td>Client</td><td>{}</td></tr>""".format(pro.customer or '')
    s_no = 0
    for i in tasks:
        if tasks.index(i)==0:
            table += """<tr><td rowspan={}>2</td><td rowspan={}>Positions</td><td>{}</td></tr>""".format(task_count,task_count,i.subject or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(i.subject or '')
    for k in keys:
        if keys.index(k)==0:
            table += """<tr><td rowspan={}>3</td><td rowspan={}>Major Key Skills</td><td>{}</td></tr>""".format(key_count,key_count,k.custom_major_key_skills or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(k.custom_major_key_skills or '')
    for d in qualification:
        if qualification.index(d)==0:
            table += """<tr><td rowspan={}>4</td><td rowspan={}>Qualification</td><td>{}</td></tr>""".format(qual_count,qual_count,d.qualification_type or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(d.qualification_type or '')
    for e in experience:
        if experience.index(e)==0:
            table += """<tr><td rowspan={}>5</td><td rowspan={}>Experience</td><td>{}</td></tr>""".format(exp_count,exp_count,e.total_experience or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(e.total_experience or '')
    for g in g_experience:
        if g_experience.index(g)==0:
            table += """<tr><td rowspan={}>6</td><td rowspan={}>GCC Experience</td><td>{}</td></tr>""".format(g_exp,g_exp,g.gulf_experience or '')
        else:
            table +="""<tr><td>{}</td></tr>""".format(g.gulf_experience or '')
    for r in rec:
        if rec.index(r)==0:
            table += """<tr><td rowspan={}>7</td><td rowspan={}>Free Recruitment</td><td>{}</td></tr>""".format(rec_count,rec_count,r.custom_free_recruitment or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(r.custom_free_recruitment or '')
    for m in interview:
        if interview.index(m)==0:
            table += """<tr><td rowspan={}>8</td><td rowspan={}>Mode Of Interview</td><td>{}</td></tr>""".format(int_count,int_count,m.mode_of_interview or '')
        else:
            table += """<tr><td>{}</td></tr>""".format(m.mode_of_interview or '')
    table += """<tr><td>9</td><td>If Direct Client Interview - Location & Date</td><td></td></tr>"""
    for j in t:
            if t.index(j)==0:
                table += """<tr><td rowspan={}>10</td><td rowspan={}>Food</td><td>{}</td></tr>""".format(food_count,food_count,j.food or '')
            else:
                table +=  """<tr><td>{}</td></tr>""".format(j.food or '')
    for a in acc:
            if acc.index(a)==0:
                table += """<tr><td rowspan={}>11</td><td rowspan={}>Accomodation</td><td>{}</td></tr>""".format(a_count,a_count,a.accommodation or '')
            else:
                table +=  """<tr><td>{}</td></tr>""".format(a.accommodation or '')
    for tr in transport:
            if transport.index(tr)==0:
                table += """<tr><td rowspan={}>12</td><td rowspan={}>Transportation</td><td>{}</td></tr>""".format(trans_count,trans_count,tr.transportation or '')
            else:
                table += """<tr><td>{}</td></tr>""".format(tr.transportation or '')
    table += """<tr><td>13</td><td>Contact Number</td><td></td></tr>"""
    table += """<tr><td>14</td><td>Mail ID</td><td></td></tr>"""
    for v in visa:
            if visa.index(v)==0:
                table += """<tr><td rowspan={}>15</td><td rowspan={}>Visa Type</td><td>{}</td></tr>""".format(v_count,v_count,v.visa_type or '')
            else:
                table += """<tr><td>{}</td></tr>""".format(v.visa_type or '')
    for cons in con:
            if con.index(cons)==0:
                table += """<tr><td rowspan={}>16</td><td rowspan={}>Contract</td><td>{}</td></tr>""".format(con_count,con_count,cons.contract_period_year or '')
            else:
                table += """<tr><td>{}</td></tr>""".format(cons.contract_period_year or '')
    for cat in categorys:
            if categorys.index(cat)==0:
                table += """<tr><td rowspan={}>17</td><td rowspan={}>ECR/ECNR</td><td>{}</td></tr>""".format(ca_count,ca_count,cat.category or '')
            else:
                table += """<tr><td>{}</td></tr>""".format(cat.category or '')
    table += """<tr><td>18</td><td>Special Remarks</td><td>Attractive Salary</td></tr>"""
    table += """<tr><td>19</td><td>Common Version 1.0</td><td>Company Name + Logo + RA Licence + Location + Website + Common Number (7305056202) + Common Mail ID</td></tr>"""
    table += '</table>'
    subject = " Action Confirmed -  {}".format(frappe.utils.nowdate())
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below Action Confirmed Details:<br><br>{}<br><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(table)
    frappe.sendmail(
        # recipients=["divya.p@groupteampro.com"],
        recipients=["dineshbabu.k@groupteampro.com","dm@groupteampro.com","annie.m@groupteampro.com"],
        subject=subject,
        message=message
    )

@frappe.whitelist()     
def send_mail_to_drop(name):
    create=frappe.get_doc("Closure",name)
    candidate=frappe.db.get_all("Candidate",{"name":create.candidate},['task'])
    spoc=frappe.db.get_value("Task",{'name':candidate},['spoc'])
    frappe.sendmail(
        # recipients=["divya.p@groupteampro.com"],
        recipients=[spoc],
        subject = "Candidate Droped-  %s" % nowdate(),
        message="""   
        Dear Sir/Mam,<br>
        <p><b>Closure ID: </b>%s – has been Droped.Additional CV is Required</p><br>
        
            Thanks & Regards<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
    """ % (create.name)
        ) 

@frappe.whitelist() 
def send_mail_to_candidate(candidate_id):
    candidate=frappe.db.get_all("Candidate",{'name':candidate_id},['mail_id','territory','position','given_name','interview_location','interview_date','passport_number'])
    candidate_mail=frappe.db.get_value("Candidate",{'name':candidate_id},['mail_id'])
    if candidate:
        candidate = candidate[0]
    subject = " Acknowledgement of Receipt - Original Passport for ACGC, {}  {}".format(candidate['territory'],candidate['position']) 
    message = """
    Dear {},
    <br><br>
    Greetings from TEAMPRO!
    <br><br>
    Following your interview for the position of {} with ACGC, {} in {} on {}, we are delighted to inform you that you have been shortlisted for further consideration.
    <br><br>
    This email serves as confirmation of the receipt of your original passport (Passport No: {}), which we will securely hold until the next stage of the process.
    <br><br>
    Should you have any questions or require further clarification, please don't hesitate to contact us.
    <br><br>
    We appreciate the opportunity to be of service to you.
    <br><br>
    Note: This acknowledgment does not guarantee employment and is subject to confirmation from the client's side.
    <br><br>
    With Best Wishes & Regards,
    <br><br>
    TEAMPRO""".format(candidate['given_name'],candidate['position'],candidate['territory'],candidate['interview_location'],candidate['interview_date'],candidate['passport_number'])
    frappe.sendmail(
        # recipients=[candidate_mail],
        recipients=["abdulla.pi@groupteampro.com"],
        subject=subject,
        message=message,
    )

@frappe.whitelist() 
def send_mail_to_candidate_pass_return(candidate_id):
    candidate=frappe.db.get_all("Candidate",{'name':candidate_id},['mail_id','territory','position','given_name','interview_location','interview_date','passport_number'])
    candidate_mail=frappe.db.get_value("Candidate",{'name':candidate_id},['mail_id'])
    if candidate:
        candidate = candidate[0]
    subject = " Acknowledgement of Returned- Original Passport for ACGC, {}  {}".format(candidate['territory'],candidate['position']) 
    message = """
    Dear {},
    <br><br>
    Greetings from TEAMPRO!
    <br><br>
    Following your interview for the position of {} with ACGC, {} in {} on {}.
    <br><br>
    This email serves as confirmation of the return of your original passport (Passport No: {})
    <br><br>
    Should you have any questions or require further clarification, please don't hesitate to contact us.
    <br><br>
    We appreciate the opportunity to be of service to you.
    <br><br>
    Note: This acknowledgment does not guarantee employment and is subject to confirmation from the client's side.
    <br><br>
    With Best Wishes & Regards,
    <br><br>
    TEAMPRO""".format(candidate['given_name'],candidate['position'],candidate['territory'],candidate['interview_location'],candidate['interview_date'],candidate['passport_number'])
    frappe.sendmail(
        # recipients=[candidate_mail],
        recipients=["sangeetha.a@groupteampro.com"],
        subject=subject,
        message=message,
    )

@frappe.whitelist() 
def send_mail_to_draft(acc_manager,reason,name):
    subject="Project:{} is moved to draft".format(name)
    message="""
        <br>Dear Sir/Mam,<br>
        The Project:{} status is moved to Draft.The following queries need to be clarified.
        <br>Reason:{}
        <br><br>
        With Best Wishes & Regards,
        <br><br>
        TEAMPRO""".format(name,reason)
    frappe.sendmail(
        recipients=acc_manager,
        # recipients=["divya.p@groupteampro.com"],
        subject=subject,
        message=message,
    )

@frappe.whitelist() 
def send_notification_to_am_cofirmed(name):
    subject="Project:{} is conifirmed by Account Manager".format(name)
    message="""
            <br>Dear Sir/Mam,<br>
            The Project:{} is conifirmed by Account Manager for your further action.
            <br><br>
            With Best Wishes & Regards,
            <br><br>
            TEAMPRO""".format(name)
    frappe.sendmail(
        recipients=["sangeetha.a@groupteampro.com"],
        # recipients=["divya.p@groupteampro.com"],
        subject=subject,
        message=message,
    )

@frappe.whitelist() 
def candidate_idb_remarks(candidate_id,reason):
    subject="Candidate:{} is {}".format(candidate_id,reason)
    message="""
            <br>Dear Sir/Mam,<br>
            Candidate:{} is {}
            <br><br>
            With Best Wishes & Regards,
            <br><br>
            TEAMPRO""".format(candidate_id,reason)
    frappe.sendmail(
        recipients=["sangeetha.a@groupteampro.com"],
        # recipients=["divya.p@groupteampro.com"],
        subject=subject,
        message=message,
    )

@frappe.whitelist()
def send_mail_to_sams(name):
    from datetime import datetime
    
    posting_date = datetime.now().strftime("%d-%m-%Y")
    pro = frappe.get_doc("Project",name)
    tasks = frappe.get_all("Task", {'project': pro.name}, ['*'])
    
    # Generate the HTML table
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table +='<tr><td colspan="7" style="text-align: center; font-weight: bold;">Territory: {}</td></tr>'.format(pro.territory or '')
    table += '<tr style="background-color: #87CEFA"><td style="width: 5%; font-weight: bold; text-align: center;">Positions</td><td style="width: 4%; font-weight: bold; text-align: center;"># Vac </td><td style="width: 10%; font-weight: bold; text-align: center;">Salary</td><td style="width: 5%; font-weight: bold; text-align: center;">Food</td><td style="width: 5%; font-weight: bold; text-align: center;">Accommodation</td><td style="width: 5%; font-weight: bold; text-align: center;">ECR/ECNR</td><td style="width: 10%; font-weight: bold; text-align: center;">Major Key Skills</td></tr>'
    
    for i in tasks:
        vac = (i.vac * 3)
        table += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            i.subject, vac, i.amount, i.food, i.accommodation, i.category, i.custom_major_key_skills
        )
    table += '</table>'
    sams=frappe.get_all("SAMS",{"sa_status": ["!=", "Do Not Contact"]},["email_address","name"])
    ind=0
    frappe.sendmail(
        recipients=['sangeetha.a@groupteampro.com'],
        # recipients=[user.email_address],
        subject=f'Position Details {posting_date} - Reg',
        message=f"""
        <b>Dear Sir/Mam,</b><br><br>
        Please find the below positions for {pro.name} for your kind reference and action.<br><br>
        {table}<br><br>
        Thanks & Regards,<br>TEAM ERP<br>
        <i>This email has been automatically generated. Please do not reply</i>
        """
    )

import frappe
from frappe import _
from frappe.utils import today
from datetime import datetime

@frappe.whitelist()
def send_proj_creation(name, account_manager=None, customer=None):
    custom_date = today()
    date_obj = datetime.strptime(str(custom_date), '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')

    subject = f'New Project Created on {formatted_date} - Reg'

    message = f"""
    <b>Dear Team,</b><br><br>

    A new project has been created on kick of completion. Please find the project details below:<br><br>

    <table border="1" cellspacing="0" cellpadding="5">
        <tr><td><b>Project Name</b></td><td>{name}</td></tr>
        <tr><td><b>Customer</b></td><td>{customer or ''}</td></tr>
    """

    if account_manager:
        message += f"<tr><td><b>Account Manager</b></td><td>{account_manager}</td></tr>"

    message += """
    </table>
    <br><br>
    Kindly take the necessary actions.<br><br>

    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """

    recipients = ['sangeetha.s@groupteampro.com','dineshbabu.k@groupteampro.com','sangeetha.a@groupteampro.com']
    if account_manager:
        recipients.append(account_manager)

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message
    )

@frappe.whitelist()    
def batch_creation_mail(name):
    batch_doc = frappe.get_doc("Batch",name)
    for i in batch_doc:
        frappe.sendmail(
        recipients=['sangeetha.s@groupteampro.com',"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],
        cc = [''],
        subject=('New Batch Creation'),
        message="""   
            Dear Sir/Mam,<br>
            <p>New batch <b>%s</b> has been created with <b>%s</b> cases for customer : <b>%s</b> on the Date : <b>%s</b> </p><br>
         
                Thanks & Regards<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
        """ % (batch_doc.name,batch_doc.no_of_cases,batch_doc.customer,batch_doc.expected_start_date)
        ) 
    return True

@frappe.whitelist()
def closure_mail_issue(subject,id,live,created_by,priority,assigned=None,project=None,action_taken=None,proof=None,domain=None):
    project_spoc=''
    reports_to=''
    report=''
    if project:
        project_spoc=frappe.db.get_value("Project",{'name':project},['spoc'])
        reports_to_mail=frappe.db.get_value("Employee",{'user_id':project_spoc},['reports_to'])
        reports_to=frappe.db.get_value("Employee",{'name':reports_to_mail},['user_id'])
    if assigned:
        report_mail=frappe.db.get_value("Employee",{'user_id':assigned},['reports_to'])
        report=frappe.db.get_value("Employee",{'name':report_mail},['user_id'])
    data = ''
    data += f"<table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>\
    <tr><td colspan='2' style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black;'><b>Issue Closure Review</b></td></tr>\
    <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Issue ID</b></td><td style='border: 1px solid black;'>{id}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Statement</b></td><td style='border: 1px solid black;'>{subject}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Raised By</b></td><td style='border: 1px solid black;'>{created_by}</td></tr>\
    <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Project</b></td><td style='border: 1px solid black;'>{project}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Priority</b></td><td style='border: 1px solid black;'>{priority}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Action Taken</b></td><td style='border: 1px solid black;'>{action_taken}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Live At</b></td><td style='border: 1px solid black;'>{live}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Domain</b></td><td style='border: 1px solid black;'>{domain}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Proof</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/{proof}' target='_blank'>Link to Proof</a></td></tr></table>"


    frappe.sendmail(
        sender=assigned,
        # recipients='divya.p@groupteampro.com',  
        recipients=project_spoc,
        cc=[reports_to,report,assigned],
        subject='Issue : %s Closure Review Document' % id,
        message = """
        <b>Dear Patron,<br><br>Greeting !!!</b><br><br>
           The attached Issue has been completed by Development and forwarded for your kind review, please confirm if it satisfies all your requirement and Mark the Issue Status as Client Review / Completed or if you feel it is still pending for some action please change the status as “OPEN”<br><br>
        {}<br><br>
        Thanks & Regards,<br>TEAM ERP<br>
        
        <i>This email has been automatically generated. Please do not reply</i>
        """.format(data)
    )
    




def check_daily_attendance():
    today = nowdate()
    yesterday = add_days(today, -1)

    
    attendance_list = frappe.get_all(
        "Attendance",
        filters={"attendance_date": yesterday, "status": ["!=", "Present"]},
        fields=["name", "employee", "employee_name", "status","in_time","out_time"]
    )

    for att in attendance_list:
        
        if att.in_time or att.out_time:
        
            user_id = frappe.db.get_value("Employee", att.employee, "user_id")

            if user_id:
                send_absent_mail(att.employee_name, user_id, att.status, yesterday)
            
            
            

def send_absent_mail(employee_name, email, status, date):
    
    formatted_date = frappe.format(date, {"fieldtype": "Date"})
    
    subject = f"Attendance Mispunch for {formatted_date}"

    message = f"""
    Dear {employee_name},<br><br>
    Your attendance for <b>{formatted_date}</b> is marked as <b>{status}</b>.<br><br>

    Please check this immediately and discuss with your HOD if required.<br>
    <b>Note:</b> Attendance can be revised only within <b>24 hours</b>. After that, no changes will be allowed.<br><br>

    Regards,<br>
    TEAM ERP
    """

    frappe.sendmail(
        recipients=[email],
        # recipients=["riyaz.a@groupteampro.com"],
        subject=subject,
        message=message
    )
            






# @frappe.whitelist()
# def create_schedule_job_mail():
#     job = frappe.db.exists('Scheduled Job Type', 'check_daily_attendance')
#     if not job:
#         exp = frappe.new_doc("Scheduled Job Type")
#         exp.update({
#             "method": 'teampro.email_alerts.check_daily_attendance',
#             "frequency": 'Cron',
#             "cron_format": "0 0 * * *"
#         })
#         exp.save(ignore_permissions=True)   





@frappe.whitelist()
def send_fp_mail():

   
    custom_date = today()
    formatted_date = datetime.strptime(
        custom_date, '%Y-%m-%d'
    ).strftime('%d/%m/%Y')

    subject = f'FP List of Team on {formatted_date} - Reg'

    
    teams = ["ALPHA", "BRAVO", "CHARLIE", "DELTA"]

    VALID_STATUS = [
        "Linedup",
        "Shortlisted",
        "Interviewed",
        "Submit(SPOC)",
        "Submitted(Client)",
        "Pending QC",
        "Result Pending"
    ]

    for team in teams:

      
        team_users = frappe.get_all(
            "Employee",
            filters={
                "custom_dev_team": team,
                "department": "Recruitment - THIS"
            },
            pluck="user_id"
        )

        if not team_users:
            continue

      
        tl_user = frappe.get_value(
            "Employee",
            {
                "custom_dev_team": team,
                "department": "Recruitment - THIS",
                "custom_is_tl": 1
            },
            "user_id"
        )

        if not tl_user:
            continue

        
        candidates = frappe.get_all(
            "Candidate",
            filters={
                "candidate_created_by": ["in", team_users],
                "pending_for": ["in", VALID_STATUS]
            },
            fields=[
                "name",
                "given_name",
                "position",
                "pending_for",
                "candidate_created_by",
                "customer",
                "task",
                "territory",
                "age_of_cv"
            ]
        )

        if not candidates:
            continue

       
        rows = ""
        for i, c in enumerate(candidates, start=1):
            
            if c.task:
                usr = frappe.db.get_value("Task",{"name":c.task},"spoc") or ""
                if usr:
                    Spoc = frappe.db.get_value("Employee",{"user_id":usr},"short_code") or ""
                    
            if c.candidate_created_by:
                
                co_short = frappe.db.get_value("Employee",{"user_id":c.candidate_created_by},"short_code") or ""
            
            rows += f"""
                <tr>
                    <td style="text-align:center;">{i}</td>
                    <td style="text-align:center;">{c.name}</td>
                    <td>{c.given_name or ''}</td>
                    <td>{c.position or ''}</td>
                    <td>{c.pending_for}</td>
                    <td style="text-align:center;">{co_short or ''}</td>
                    <td style="width:400px;  min-width:400px;">{c.customer or ''}</td>
                    <td style="text-align:center;">{Spoc or ''}</td>
                    <td>{c.territory or ''}</td>
                    <td style="text-align:center;">{c.age_of_cv or ''}</td>
                </tr>
            """

        
        message = f"""
        Dear Sir/Madam,<br><br>
        Please find below the Feedback Pending List of <b>{team}</b> team for <b>{formatted_date}</b>.
        <br><br>
        
        

        <table border="1" cellspacing="0" cellpadding="5" style="border-collapse:collapse;">
            <tr>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">SR</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">CD ID</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">Given Name / Surname</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">Position</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">Status</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">Candidate Owner</th>
                <th style="text-align:center; width:400px;  min-width:400px; white-space: nowrap; background-color:#0f1568; color:white;">Customer</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">SPOC</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">Territory</th>
                <th style="text-align:center; white-space: nowrap; background-color:#0f1568; color:white;">Age of CV</th>
            </tr>
            {rows}
        </table>

        
        """

        
        frappe.sendmail(
            recipients=[tl_user],
            # recipients=["riyaz.a@groupteampro.com"],
            subject=subject,
            message=message
        )
       


# @frappe.whitelist()
# def create_schedule_fp_mail():
#     job = frappe.db.exists('Scheduled Job Type', 'send_fp_mail')
#     if not job:
#         exp = frappe.new_doc("Scheduled Job Type")
#         exp.update({
#             "method": 'teampro.email_alerts.send_fp_mail',
#             "frequency": 'Cron',
#             "cron_format": "0 21 * * *"
#         })
#         exp.save(ignore_permissions=True) 

@frappe.whitelist()
def closure_mail_completion(subject,id,owner,action_taken,live,et,at,revision,service,proof,allocated=None,project=None,issue=None,domain=None,spoc=None,reason=None,dev_spoc=None,et_remark=None):
    if service=='IT-SW':
        percentage=et_at_calculation(id, et, at, allocated,subject)
        reports=frappe.db.get_value("Employee",{'user_id':allocated},['reports_to'])
        reports_to=frappe.db.get_value("Employee",{'name':reports},['user_id'])
        tl=frappe.db.get_value("Employee",{'user_id':allocated},["custom_tl"])
        tl_mail=frappe.db.get_value("Employee",{'name':tl},['user_id'])
        et_rate= 'ET : %s and AT : %s'%(et,round(percentage,2))
        if issue:
            raised_by=frappe.db.get_value("Issue",{'name':issue},['raised_by'])
        else:
            raised_by='None'
        
        data = ''
        data += f"<table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>\
        <tr><td colspan='2' style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black;'><b>Task / Issue Completion</b></td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Task ID</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/app/task/{id}' target='_blank'>{id}</a></td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Project</b></td><td style='border: 1px solid black;'>{project}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task Raised By</b></td><td style='border: 1px solid black;'>{owner}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue ID</b></td><td style='border: 1px solid black;'>{issue}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Raised By</b></td><td style='border: 1px solid black;'>{raised_by}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Statement</b></td><td style='border: 1px solid black;'>{subject}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Action Taken</b></td><td style='border: 1px solid black;'>{action_taken}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Live At</b></td><td style='border: 1px solid black;'>{live}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Domain</b></td><td style='border: 1px solid black;'><a href='{domain}' target='_blank' style='color: blue; text-decoration: underline;'>{domain}</a></td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Proof</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/{proof}' target='_blank'>Link to Proof</a></td></tr></table>"

        cc = [reports_to, allocated,spoc,"dineshbabu.k@groupteampro.com"] + ([dev_spoc] if dev_spoc else []) +([tl_mail] if tl_mail else [])
        frappe.sendmail(
            sender=allocated,
            recipients=spoc,
            cc=cc,
            subject='Task : %s Completed' % id,
            message = """
            <b>Dear Patron,<br><br>Greeting !!!</b><br><br>
            <b>The below Task has been <b>successfully completed</b><br><br>
        {}<br><br>
            Thanks & Regards,<br>TEAM ERP<br>

            <i>This email has been automatically generated. Please do not reply</i>
            """.format(data)
        )

@frappe.whitelist() 
def send_odr_mail_to_candidate(candidate_id):
    candidate=frappe.db.get_all("Candidate",{'name':candidate_id},['mail_id','customer','territory','position','given_name','interview_location','interview_date','passport_number'])
    candidate_mail=frappe.db.get_value("Candidate",{'name':candidate_id},['mail_id'])
    if candidate:
        candidate = candidate[0]
    subject = " Acknowledgement of Receipt - Original Passport for {}, {}  {}".format(candidate['customer'],candidate['territory'],candidate['position']) 
    message = """
    Dear {},
    <br><br>
    Greetings from TEAMPRO!
    <br><br>
    Following your interview for the position of {} with {}, {} in {} on {}, we are delighted to inform you that you have been shortlisted for further consideration.
    <br><br>
    This email serves as confirmation of the receipt of your original passport (Passport No: {}), which we will securely hold until the next stage of the process.
    <br><br>
    Should you have any questions or require further clarification, please don't hesitate to contact us.
    <br><br>
    We appreciate the opportunity to be of service to you.
    <br><br>
    Note: This acknowledgment does not guarantee employment and is subject to confirmation from the client's side.
    <br><br>
    With Best Wishes & Regards,
    <br><br>
    TEAMPRO""".format(candidate['given_name'],candidate['position'],candidate['customer'],candidate['territory'],candidate['interview_location'],candidate['interview_date'],candidate['passport_number'])
    frappe.sendmail(
        recipients=[candidate_mail],
        cc=["keerthana.b@groupteampro.com","dc@groupteampro.com"],
        # recipients=["divya.p@groupteampro.com","keerthana.b@groupteampro.com"],
        subject=subject,
        message=message,
    )

@frappe.whitelist()
def send_mail_nc_for_check_reject(name=None,id=None,allocated=None,class_proposed=None,reason=None):
    if allocated:
        emp_id=frappe.db.get_value("Employee",{'user_id':allocated},['name'])
        subject = _("{} - {} Rejected").format(name, id)
        message = """
            <p>Dear {},</p>
            <p><b>{} - {}</b> has been rejected.</p>
            <p><b>Reason:</b> {}</p>
            <p><b>NC Class:</b>{}</p>
            <p>Kindly review and take the necessary action.</p>
            <p>Best Regards,<br>TEAMPRO</p>
            """.format(emp_id,name, id, reason,class_proposed)

        frappe.sendmail(
            recipients=allocated,
            subject=subject,
            message=message
        )


@frappe.whitelist()
def meeting_status_check():
    from frappe.utils import today
    from datetime import datetime

    completed_meetings = []

    meetings = frappe.db.get_all(
        "Meeting",
        filters={"status": ["not in", [ "Completed" , "Cancelled"]], "custom_services": "IT-SW"},
        fields=["name", "title", "project", "date"]
    )

    for meet in meetings:
        task_count = 0
        comp_count = 0

        minutes = frappe.get_all(
            "Meeting Minute",
            filters={"parent": meet.name},
            fields=["custom_id", "description"]
        )

        for minute in minutes:
            if minute.custom_id:
                task_count += 1
                status = frappe.db.get_value("Task", {"name": minute.custom_id}, "status")
                if status == "Completed":
                    comp_count += 1

        
        if task_count > 0 and task_count == comp_count:
            frappe.db.set_value("Meeting", meet.name, "status", "Completed")

            # Capture completed meeting info
            meeting_info = {
                "name": meet.name,
                "title": meet.title or "",
                "project": meet.project or "",
                "status": "Completed",
                "date": meet.date or ""
            }
            completed_meetings.append(meeting_info)

            
            completed_tasks = []
            for minute in minutes:
                if minute.custom_id:
                    completed_tasks.append({
                        "description": minute.description or "",
                        "action": "Task",
                        "task": minute.custom_id or "",
                        "cr_status": "Completed",
                        "completed_on": frappe.db.get_value("Task", {"name": minute.custom_id}, "completed_on") or ""
                    })

            
            date_obj = datetime.strptime(today(), "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")
            created_on_date = ""
            if meeting_info.get("date"):
                created_on_date = formatdate(meeting_info["date"], "dd/MM/yyyy")
            
            table_html = f"""
                <table border="1" cellpadding="5" cellspacing="0">
                    <thead>
                        <tr style="background-color:#0F1568; color:white;">
                            <th style="text-align:center; border:1px solid black;" >S.No</th>
                            <th style="text-align:center; border:1px solid black;" >Title</th>
                            <th style="text-align:center; border:1px solid black;" >Project</th>
                            <th style="text-align:center; border:1px solid black;" >Status</th>
                            <th style="text-align:center; border:1px solid black;" >Created On</th>
                            <th style="text-align:center; border:1px solid black;" >Completed On</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="text-align:center; border:1px solid black; ">1</td>
                            <td style="text-align:center; border:1px solid black; ">{meeting_info['title']}</td>
                            <td style="text-align:center; border:1px solid black; ">{meeting_info['project']}</td>
                            <td style="text-align:center; border:1px solid black; ">{meeting_info['status']}</td>
                            <td style="text-align:center; border:1px solid black; ">{created_on_date}</td>
                            <td style="text-align:center; border:1px solid black; ">{formatted_date}</td>
                        </tr>
                    </tbody>
                </table>
            """

            
            table_html_2 = ""
            if completed_tasks:
                table_html_2 = """
                    <table border="1" cellpadding="5" cellspacing="0">
                        <thead>
                            <tr style="background-color:#0F1568; color:white;">
                                <th style="text-align:center; border:1px solid black;" >S.No</th>
                                <th style="text-align:center; border:1px solid black;" >Description</th>
                                <th style="text-align:center; border:1px solid black;" >Action</th>
                                <th style="text-align:center; border:1px solid black;" >Task</th>
                                <th style="text-align:center; border:1px solid black;" >Cr.Status</th>
                                <th style="text-align:center; border:1px solid black;" >Completed On</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                for idx, task in enumerate(completed_tasks, start=1):
                    
                    # if task['completed_on']:
                    #     formated_date_2 = frappe.format(task['completed_on'],{"fieldtype":"Date"})
                        
                    formated_date_2 = ""
                    if task['completed_on']:
                        formated_date_2 = formatdate(task['completed_on'], "dd/MM/yyyy")
                            
                    table_html_2 += f"""
                        <tr>
                            <td style="text-align:center; border:1px solid black; ">{idx}</td>
                            <td style="text-align:center; border:1px solid black; ">{task['description']}</td>
                            <td style="text-align:center; border:1px solid black; ">{task['action']}</td>
                            <td style="text-align:center; border:1px solid black; ">{task['task']}</td>
                            <td style="text-align:center; border:1px solid black; ">{task['cr_status']}</td>
                            <td style="text-align:center; border:1px solid black; ">{formated_date_2}</td>
                        </tr>
                    """
                table_html_2 += "</tbody></table>"

            subject = f"Meeting ID : {meeting_info['title']} as Completed on {formatted_date} - Reg"
            message = f"""
                <p>Dear Patron,</p>
                <br>
                <p>Greetings from TEAMPRO !!!</p>
                <br>
                <p>The following meeting has been marked as <b>Completed</b>:</p>
                <br>
                <p><b>Meeting Summary:</b></p>
                <br>
                {table_html}
                <br>
                <p><b>Points noted during the meeting and their current status:</b></p>
                {table_html_2}
                <br>
                
            """

            
            frappe.sendmail(
                recipients=["abdulla.pi@groupteampro.com"],
                subject=subject,
                message=message
            )

    return completed_meetings

from collections import defaultdict
@frappe.whitelist()
def send_daily_candidate_status_alert4():

    date = getdate(today())
    formatted_date = formatdate(date, "dd-mm-yyyy")
    statuses = ["IDB", "Sourced", "Pending QC", "Submit(SPOC)"]

    executives = frappe.get_all(
        'Employee',
        filters={"department": "Recruitment - THIS", "status": "Active"},
        fields=['user_id'],
        distinct=True
    )
    executive_list = [exe.user_id for exe in executives if exe.user_id]

    if not executive_list:
        frappe.msgprint("No active executives found.")
        return

    placeholders = ", ".join(["%s"] * len(executive_list))

    candidate_statuses = frappe.db.sql(f"""
    SELECT DISTINCT c.name,
           c.candidate_created_by AS executive,
           cs.task AS task,
           c.position AS position,
           cs.status AS status
    FROM `tabCandidate status` cs
    INNER JOIN `tabCandidate` c ON c.name = cs.parent
    WHERE c.candidate_created_by IN ({placeholders})
    AND DATE(cs.sourced_date) = %s
    AND cs.status = 'Submit(SPOC)'
""", tuple(executive_list + [date]), as_dict=True)

    pending_candidates = frappe.db.sql(f"""
        SELECT DISTINCT c.name,
            c.candidate_created_by AS executive,
            cs.task AS task,
            c.position AS position,
            c.pending_for AS status
        FROM `tabCandidate` c
        LEFT JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by IN ({placeholders})
        AND c.pending_for IN (%s, %s, %s)
        AND DATE(cs.sourced_date) = %s
    """, tuple(executive_list + ["IDB", "Sourced", "Pending QC", date]), as_dict=True)

    all_rows = candidate_statuses + pending_candidates

    if not all_rows:
        frappe.msgprint("No candidate data found for today.")
        return

    table_data = defaultdict(lambda: defaultdict(lambda: {"position": "", **{s: 0 for s in statuses}}))
    for r in all_rows:
        exe = r.get('executive')
        task = r.get('task') or "N/A"
        pos = r.get('position') or "N/A"
        stat = r.get('status')
        if exe and stat in statuses:
            table_data[exe][task]["position"] = pos
            table_data[exe][task][stat] += 1

    html = f"""
    <h3>Daily Candidate Status Alert - {formatted_date}</h3>
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
        <thead>
            <tr style="background-color:#007bff;color:white;">
                <th>S.No</th>
                <th>Executive</th>
                <th>Task</th>
                <th>Position</th>
                <th>IDB</th>
                <th>Sourced</th>
                <th>Pending QC</th>
                <th>Submit(SPOC)</th>
            </tr>
        </thead>
        <tbody>
    """

    sno = 1
    for exe, tasks in table_data.items():
        task_list = list(tasks.keys())
        rowspan = len(task_list)
        first_row = True
        for task_name in task_list:
            counts = tasks[task_name]
            html += "<tr>"
            html += f"<td>{sno}</td>"
            if first_row:
                html += f"<td rowspan='{rowspan}'>{exe}</td>"
                first_row = False
            html += f"<td>{task_name}</td>"
            html += f"<td>{counts.get('position', '')}</td>"
            html += f"<td>{counts.get('IDB', 0)}</td>"
            html += f"<td>{counts.get('Sourced', 0)}</td>"
            html += f"<td>{counts.get('Pending QC', 0)}</td>"
            html += f"<td>{counts.get('Submit(SPOC)', 0)}</td>"
            html += "</tr>"
            sno += 1

    html += "</tbody></table>"

    subject = f"Daily Candidate Status Alert - {formatted_date}"
    recipients = ["sangeetha.s@groupteampro.com"]  # Replace with actual recipients

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=html
    )

    frappe.msgprint(f"Alert email sent for {sno-1} rows for today.")

@frappe.whitelist()
def send_daily_candidate_status_alert3():

    date = getdate(today())
    formatted_date = formatdate(date, "dd-mm-yyyy")
    statuses = ["IDB", "Sourced", "Pending QC", "Submit(SPOC)"]

    executives = frappe.get_all(
        'Employee',
        filters={"department": "Recruitment - THIS", "status": "Active"},
        fields=['user_id'],
        distinct=True
    )
    executive_list = [exe.user_id for exe in executives if exe.user_id]

    if not executive_list:
        frappe.msgprint("No active executives found.")
        return

    placeholders = ", ".join(["%s"] * len(executive_list))

    candidate_statuses = frappe.db.sql(f"""
    SELECT DISTINCT c.name,
           c.candidate_created_by AS executive,
           cs.task AS task,
           c.position AS position,
           cs.status AS status
    FROM `tabCandidate status` cs
    INNER JOIN `tabCandidate` c ON c.name = cs.parent
    WHERE c.candidate_created_by IN ({placeholders})
    AND DATE(cs.sourced_date) = %s
    AND cs.status = 'Submit(SPOC)'
""", tuple(executive_list + [date]), as_dict=True)

    pending_candidates = frappe.db.sql(f"""
        SELECT DISTINCT c.name,
            c.candidate_created_by AS executive,
            cs.task AS task,
            c.position AS position,
            c.pending_for AS status
        FROM `tabCandidate` c
        LEFT JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by IN ({placeholders})
        AND c.pending_for IN (%s, %s, %s)
        AND DATE(cs.sourced_date) = %s
    """, tuple(executive_list + ["IDB", "Sourced", "Pending QC", date]), as_dict=True)

    all_rows = candidate_statuses + pending_candidates

    if not all_rows:
        frappe.msgprint("No candidate data found for today.")
        return

    table_data = defaultdict(lambda: defaultdict(lambda: {"position": "", **{s: 0 for s in statuses}}))
    for r in all_rows:
        exe = r.get('executive')
        task = r.get('task') or "N/A"
        pos = r.get('position') or "N/A"
        stat = r.get('status')
        if exe and stat in statuses:
            table_data[exe][task]["position"] = pos
            table_data[exe][task][stat] += 1

    html = f"""
    <h3>Daily Candidate Status Alert - {formatted_date}</h3>
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
        <thead>
            <tr style="background-color:#007bff;color:white;">
                <th>S.No</th>
                <th>Executive</th>
                <th>Task</th>
                <th>Position</th>
                <th>IDB</th>
                <th>Sourced</th>
                <th>Pending QC</th>
                <th>Submit(SPOC)</th>
            </tr>
        </thead>
        <tbody>
    """

    sno = 1
    for exe, tasks in table_data.items():
        task_list = list(tasks.keys())
        rowspan = len(task_list)
        first_row = True
        for task_name in task_list:
            counts = tasks[task_name]
            html += "<tr>"
            html += f"<td>{sno}</td>"
            if first_row:
                html += f"<td rowspan='{rowspan}'>{exe}</td>"
                first_row = False
            html += f"<td>{task_name}</td>"
            html += f"<td>{counts.get('position', '')}</td>"
            html += f"<td>{counts.get('IDB', 0)}</td>"
            html += f"<td>{counts.get('Sourced', 0)}</td>"
            html += f"<td>{counts.get('Pending QC', 0)}</td>"
            html += f"<td>{counts.get('Submit(SPOC)', 0)}</td>"
            html += "</tr>"
            sno += 1

    html += "</tbody></table>"

    subject = f"Daily Candidate Status Alert - {formatted_date}"
    recipients = ["sangeetha.s@groupteampro.com"]  # Replace with actual recipients

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=html
    )

    frappe.msgprint(f"Alert email sent for {sno-1} rows for today.")

@frappe.whitelist()
def send_daily_candidate_status_alert2():

    date = getdate(today())
    formatted_date = formatdate(date, "dd-mm-yyyy")
    statuses = ["IDB", "Sourced", "Pending QC", "Submit(SPOC)"]

    executives = frappe.get_all(
        'Employee',
        filters={"department": "Recruitment - THIS", "status": "Active"},
        fields=['user_id'],
        distinct=True
    )
    executive_list = [exe.user_id for exe in executives if exe.user_id]

    if not executive_list:
        frappe.msgprint("No active executives found.")
        return

    placeholders = ", ".join(["%s"] * len(executive_list))

    candidate_statuses = frappe.db.sql(f"""
    SELECT DISTINCT c.name,
           c.candidate_created_by AS executive,
           cs.task AS task,
           c.position AS position,
           cs.status AS status
    FROM `tabCandidate status` cs
    INNER JOIN `tabCandidate` c ON c.name = cs.parent
    WHERE c.candidate_created_by IN ({placeholders})
    AND DATE(cs.sourced_date) = %s
    AND cs.status = 'Submit(SPOC)'
""", tuple(executive_list + [date]), as_dict=True)

    pending_candidates = frappe.db.sql(f"""
        SELECT DISTINCT c.name,
            c.candidate_created_by AS executive,
            cs.task AS task,
            c.position AS position,
            c.pending_for AS status
        FROM `tabCandidate` c
        LEFT JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by IN ({placeholders})
        AND c.pending_for IN (%s, %s, %s)
        AND DATE(cs.sourced_date) = %s
    """, tuple(executive_list + ["IDB", "Sourced", "Pending QC", date]), as_dict=True)

    all_rows = candidate_statuses + pending_candidates

    if not all_rows:
        frappe.msgprint("No candidate data found for today.")
        return

    table_data = defaultdict(lambda: defaultdict(lambda: {"position": "", **{s: 0 for s in statuses}}))
    for r in all_rows:
        exe = r.get('executive')
        task = r.get('task') or "N/A"
        pos = r.get('position') or "N/A"
        stat = r.get('status')
        if exe and stat in statuses:
            table_data[exe][task]["position"] = pos
            table_data[exe][task][stat] += 1

    html = f"""
    <h3>Daily Candidate Status Alert - {formatted_date}</h3>
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
        <thead>
            <tr style="background-color:#007bff;color:white;">
                <th>S.No</th>
                <th>Executive</th>
                <th>Task</th>
                <th>Position</th>
                <th>IDB</th>
                <th>Sourced</th>
                <th>Pending QC</th>
                <th>Submit(SPOC)</th>
            </tr>
        </thead>
        <tbody>
    """

    sno = 1
    for exe, tasks in table_data.items():
        task_list = list(tasks.keys())
        rowspan = len(task_list)
        first_row = True
        for task_name in task_list:
            counts = tasks[task_name]
            html += "<tr>"
            html += f"<td>{sno}</td>"
            if first_row:
                html += f"<td rowspan='{rowspan}'>{exe}</td>"
                first_row = False
            html += f"<td>{task_name}</td>"
            html += f"<td>{counts.get('position', '')}</td>"
            html += f"<td>{counts.get('IDB', 0)}</td>"
            html += f"<td>{counts.get('Sourced', 0)}</td>"
            html += f"<td>{counts.get('Pending QC', 0)}</td>"
            html += f"<td>{counts.get('Submit(SPOC)', 0)}</td>"
            html += "</tr>"
            sno += 1

    html += "</tbody></table>"

    subject = f"Daily Candidate Status Alert - {formatted_date}"
    recipients = ["sangeetha.s@groupteampro.com"]
    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=html
    )

    frappe.msgprint(f"Alert email sent for {sno-1} rows for today.")


@frappe.whitelist()
def send_daily_candidate_status_alert1():

    date = getdate(today())
    formatted_date = formatdate(date, "dd-mm-yyyy")
    statuses = ["IDB", "Sourced", "Pending QC", "Submit(SPOC)"]

    executives = frappe.get_all(
        'Employee',
        filters={"department": "Recruitment - THIS", "status": "Active"},
        fields=['user_id'],
        distinct=True
    )
    executive_list = [exe.user_id for exe in executives if exe.user_id]

    if not executive_list:
        frappe.msgprint("No active executives found.")
        return

    placeholders = ", ".join(["%s"] * len(executive_list))

    candidate_statuses = frappe.db.sql(f"""
    SELECT DISTINCT c.name,
           c.candidate_created_by AS executive,
           cs.task AS task,
           c.position AS position,
           cs.status AS status
    FROM `tabCandidate status` cs
    INNER JOIN `tabCandidate` c ON c.name = cs.parent
    WHERE c.candidate_created_by IN ({placeholders})
    AND DATE(cs.sourced_date) = %s
    AND cs.status = 'Submit(SPOC)'
""", tuple(executive_list + [date]), as_dict=True)

    pending_candidates = frappe.db.sql(f"""
        SELECT DISTINCT c.name,
            c.candidate_created_by AS executive,
            cs.task AS task,
            c.position AS position,
            c.pending_for AS status
        FROM `tabCandidate` c
        LEFT JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by IN ({placeholders})
        AND c.pending_for IN (%s, %s, %s)
        AND DATE(cs.sourced_date) = %s
    """, tuple(executive_list + ["IDB", "Sourced", "Pending QC", date]), as_dict=True)

    all_rows = candidate_statuses + pending_candidates

    if not all_rows:
        frappe.msgprint("No candidate data found for today.")
        return

    table_data = defaultdict(lambda: defaultdict(lambda: {"position": "", **{s: 0 for s in statuses}}))
    for r in all_rows:
        exe = r.get('executive')
        task = r.get('task') or "N/A"
        pos = r.get('position') or "N/A"
        stat = r.get('status')
        if exe and stat in statuses:
            table_data[exe][task]["position"] = pos
            table_data[exe][task][stat] += 1

    html = f"""
    <h3>Daily Candidate Status Alert - {formatted_date}</h3>
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
        <thead>
            <tr style="background-color:#007bff;color:white;">
                <th>S.No</th>
                <th>Executive</th>
                <th>Task</th>
                <th>Position</th>
                <th>IDB</th>
                <th>Sourced</th>
                <th>Pending QC</th>
                <th>Submit(SPOC)</th>
            </tr>
        </thead>
        <tbody>
    """

    sno = 1
    for exe, tasks in table_data.items():
        task_list = list(tasks.keys())
        rowspan = len(task_list)
        first_row = True
        for task_name in task_list:
            counts = tasks[task_name]
            html += "<tr>"
            html += f"<td>{sno}</td>"
            if first_row:
                html += f"<td rowspan='{rowspan}'>{exe}</td>"
                first_row = False
            html += f"<td>{task_name}</td>"
            html += f"<td>{counts.get('position', '')}</td>"
            html += f"<td>{counts.get('IDB', 0)}</td>"
            html += f"<td>{counts.get('Sourced', 0)}</td>"
            html += f"<td>{counts.get('Pending QC', 0)}</td>"
            html += f"<td>{counts.get('Submit(SPOC)', 0)}</td>"
            html += "</tr>"
            sno += 1

    html += "</tbody></table>"

    subject = f"Daily Candidate Status Alert - {formatted_date}"
    recipients =["sangeetha.s@groupteampro.com"]

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=html
    )

    frappe.msgprint(f"Alert email sent for {sno-1} rows for today.")


import frappe
from frappe.utils import today, getdate, formatdate
from collections import defaultdict

@frappe.whitelist()
def send_daily_candidate_status_alert():

    date = getdate(today())
    formatted_date = formatdate(date, "dd-mm-yyyy")
    statuses = ["IDB", "Sourced", "Pending QC", "Submit(SPOC)"]

    # Get all active executives
    executives = frappe.get_all(
        'Employee',
        filters={"department": "Recruitment - THIS", "status": "Active"},
        fields=['user_id'],
        distinct=True
    )
    executive_list = [exe.user_id for exe in executives if exe.user_id]

    if not executive_list:
        frappe.msgprint("No active executives found.")
        return

    placeholders = ", ".join(["%s"] * len(executive_list))

    # Fetch Submit(SPOC) candidates
    candidate_statuses = frappe.db.sql(f"""
    SELECT DISTINCT c.name,
           c.candidate_created_by AS executive,
           cs.task AS task,
           c.position AS position,
           cs.status AS status
    FROM `tabCandidate status` cs
    INNER JOIN `tabCandidate` c ON c.name = cs.parent
    WHERE c.candidate_created_by IN ({placeholders})
    AND DATE(cs.sourced_date) = %s
    AND cs.status = 'Submit(SPOC)'
""", tuple(executive_list + [date]), as_dict=True)

    # Fetch pending_for candidates (distinct)
    pending_candidates = frappe.db.sql(f"""
        SELECT DISTINCT c.name,
            c.candidate_created_by AS executive,
            cs.task AS task,
            c.position AS position,
            c.pending_for AS status
        FROM `tabCandidate` c
        LEFT JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by IN ({placeholders})
        AND c.pending_for IN (%s, %s, %s)
        AND DATE(cs.sourced_date) = %s
    """, tuple(executive_list + ["IDB", "Sourced", "Pending QC", date]), as_dict=True)

    # Combine both
    all_rows = candidate_statuses + pending_candidates

    if not all_rows:
        frappe.msgprint("No candidate data found for today.")
        return

    # Aggregate counts: {executive: {task: {status: count, position: value}}}
    table_data = defaultdict(lambda: defaultdict(lambda: {"position": "", **{s: 0 for s in statuses}}))
    for r in all_rows:
        exe = r.get('executive')
        task = r.get('task') or "N/A"
        pos = r.get('position') or "N/A"
        stat = r.get('status')
        if exe and stat in statuses:
            table_data[exe][task]["position"] = pos
            table_data[exe][task][stat] += 1

    # Build HTML table
    html = f"""
    <h3>Daily Candidate Status Alert - {formatted_date}</h3>
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
        <thead>
            <tr style="background-color:#007bff;color:white;">
                <th>S.No</th>
                <th>Executive</th>
                <th>Task</th>
                <th>Position</th>
                <th>IDB</th>
                <th>Sourced</th>
                <th>Pending QC</th>
                <th>Submit(SPOC)</th>
            </tr>
        </thead>
        <tbody>
    """

    sno = 1
    for exe, tasks in table_data.items():
        task_list = list(tasks.keys())
        rowspan = len(task_list)
        first_row = True
        for task_name in task_list:
            counts = tasks[task_name]
            html += "<tr>"
            html += f"<td>{sno}</td>"
            if first_row:
                html += f"<td rowspan='{rowspan}'>{exe}</td>"
                first_row = False
            html += f"<td>{task_name}</td>"
            html += f"<td>{counts.get('position', '')}</td>"
            html += f"<td>{counts.get('IDB', 0)}</td>"
            html += f"<td>{counts.get('Sourced', 0)}</td>"
            html += f"<td>{counts.get('Pending QC', 0)}</td>"
            html += f"<td>{counts.get('Submit(SPOC)', 0)}</td>"
            html += "</tr>"
            sno += 1

    html += "</tbody></table>"

    # Send email
    subject = f"Daily Candidate Status Alert - {formatted_date}"
    recipients = ["sangeetha.s@groupteampro.com"]

    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=html
    )

    frappe.msgprint(f"Alert email sent for {sno-1} rows for today.")


import frappe
from frappe.utils import getdate, nowdate, add_days, formatdate

@frappe.whitelist()
def update_sla_status_and_notify():
    customers = frappe.db.get_all("Customer", {"disabled": 0}, ["*"])
    expired_sla_data = []
    nearing_expiry_sla_data = []

    today = getdate(nowdate())

    for customer_info in customers:
        customer = frappe.get_doc("Customer", customer_info.name)

        if customer.custom_sla_details:
            for sla in customer.custom_sla_details:
                if sla.sla_to_date:
                    sla_date = getdate(sla.sla_to_date)
                    formatted_sla_date = formatdate(sla.sla_to_date, "dd-MM-yyyy")

                    # Expired SLAs (already past)
                    if sla_date < today:
                        expired_sla_data.append({
                            "customer_name": customer.customer_name,
                            "service": sla.service,
                            "sla_to_date": formatted_sla_date,
                            "description":sla.description if sla.description else None,
                            "sla_type":sla.sla_type
                        })

                    # Nearing Expiry SLAs (expiring within the next 60 days)
                    elif 0 <= (sla_date - today).days <= 60:
                        nearing_expiry_sla_data.append({
                            "customer_name": customer.customer_name,
                            "service": sla.service,
                            "sla_to_date": formatted_sla_date,
                            "days_remaining": (sla_date - today).days,
                            "description":sla.description if sla.description else None,
                            "sla_type":sla.sla_type
                        })

    # If there's any data to notify
    if expired_sla_data or nearing_expiry_sla_data:
        expired_table_rows = "".join(
            f"<tr><td>{entry['customer_name']}</td><td>{entry['service']}</td><td>{entry['sla_type']}</td><td>{entry['sla_to_date']}</td><td>{entry['description']}</td></tr>"
            for entry in expired_sla_data
        )
        nearing_expiry_table_rows = "".join(
            f"<tr><td>{entry['customer_name']}</td><td>{entry['service']}</td><td>{entry['sla_type']}</td><td>{entry['sla_to_date']}</td><td>{entry['days_remaining']} days</td><td>{entry['description']}</td></tr>"
            for entry in nearing_expiry_sla_data
        )

        # Tables with equal widths
        expired_table_html = f"""
            <div>
                <h3>Expired SLAs</h3>
                <table border="1" width="100%" style="border-collapse: collapse;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="width: 40%;">Customer Name</th>
                            <th style="width: 20%;">Service</th>
                            <th style="width: 20%;">Type</th>
                            <th style="width: 20%;">SLA To Date</th>
                            <th style="width: 40%;">Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {expired_table_rows}
                    </tbody>
                </table>
            </div>
        """ if expired_sla_data else ""

        nearing_expiry_table_html = f"""
            <div>
                <h3>SLAs Nearing Expiry (Next 60 Days)</h3>
                <table border="1" width="100%" style="border-collapse: collapse;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="width: 30%;">Customer Name</th>
                            <th style="width: 10%;">Service</th>
                            <th style="width: 10%;">Type</th>
                            <th style="width: 20%;">SLA To Date</th>
                            <th style="width: 20%;">Days Remaining</th>
                            <th style="width: 40%;">Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {nearing_expiry_table_rows}
                    </tbody>
                </table>
            </div>
        """ if nearing_expiry_sla_data else ""

        # Construct final email message
        subject = "Alert: SLA Expiry Notifications"
        message = f"""
            Dear Sir/Mam,<br><br>
            Please find the SLA expiry details below:<br><br>
            {expired_table_html}
            {nearing_expiry_table_html}
            <br><br>
            These alerts will be sent daily until the SLA expires.<br><br>
            Best Regards,<br>Teampro
        """


        recipients = ["annie.m@groupteampro.com","abdulla.pi@groupteampro.com", "sivarenisha.m@groupteampro.com", "jeniba.a@groupteampro.com"]

        frappe.sendmail(
            recipients=recipients,
            cc = "dineshbabu.k@groupteampro.com",
            subject=subject,
            message=message,
        )

import frappe
from frappe.utils import today
from datetime import datetime

@frappe.whitelist()
def send_mail_for_update_checkpro_holiday():
    holiday_list = frappe.get_doc("Holiday List", {"name": "TEAMPRO 2023 - Checkpro"})
    if holiday_list.holidays:
        current_date = today()
        current_year = datetime.now().year
        current_month = datetime.now().month

        if current_month == 12:  # Perform the check only in December
            next_year = current_year + 1  # Calculate the next year
            holiday_for_next_year = any(
                holiday.holiday_date.year == next_year for holiday in holiday_list.holidays
            )

            if not holiday_for_next_year:
                subject = f"Add Holidays for TEAMPRO 2023 - Checkpro{next_year}"
                message = (
                    f"Dear Sir/Mam, <br><br>"
                    f"The holiday list for the year {next_year} is missing in the 'TEAMPRO 2023 - Checkpro' holiday list. "
                    f"Please update the holiday list for {next_year} to avoid any disruptions. <br><br>"
                    f"Regards,<br>Team"
                )
                recipients = ["sangeetha.s@groupteampro.com"]
                frappe.sendmail(
                    recipients=recipients,
                    subject=subject,
                    message=message)

def send_project_spoc_report_weekly():
    posting_date = datetime.now().strftime("%d-%m-%Y")
    spoc_list = get_spoc_list_weekly()

    for spoc in spoc_list:
        filename = "DSR_" + spoc + "_" + posting_date
        xlsx_file = build_xlsx_response_spoc_project_even_weekly(spoc, filename)
        send_mail_with_attachment_spoc_project_even_weekly(spoc, filename, xlsx_file.getvalue())

def send_mail_with_attachment_spoc_project_even_weekly(spoc, filename, file_content):
    posting_date = datetime.now().strftime("%d-%m-%Y")
    subject = f"DSR Report for {spoc} : - {posting_date}"
    message = (
        f"Dear {spoc},<br>"
        "Please find attached the DSR Report.<br><br>"
        "<br>Thanks & Regards,<br>TEAM ERP<br>"
        "This email has been automatically generated. Please do not reply"
    )
    attachments = [{"fname": filename + '.xlsx', "fcontent": file_content}]
    week_date=today()
    day_of_week=week_date.weekday()
    week_number = (week_date.day - 1) // 7 + 1
    if day_of_week == 5 and (week_number == 2 or week_number == 4):
        # Send the email for each SPOC
        frappe.sendmail(
            recipients=[spoc],  # Assuming spoc is the email ID of the SPOC
            # recipients=['jeniba.a@groupteampro.com'],
            sender=None,
            subject=subject,
            message=message,
            attachments=attachments,
        )

def build_xlsx_response_spoc_project_even_weekly(spoc, filename):
    return make_xlsx_spoc_project_weekly(spoc, filename)

def make_xlsx_spoc_project_weekly(spoc, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "DSR Report"
    today = datetime.now().strftime('%Y-%m-%d')
    header_fill = PatternFill(start_color="A6CAF0", end_color="A6CAF0", fill_type="solid")
    head_fill = PatternFill(start_color="0f1568", end_color="0f1568", fill_type="solid")
    row_fill = PatternFill(start_color="FFC1CC", end_color="FFC1CC", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
    border = Border(left=Side(border_style='thin', color='000000'),
            right=Side(border_style='thin', color='000000'),
            top=Side(border_style='thin', color='000000'),
            bottom=Side(border_style='thin', color='000000'))
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=17):
        for cell in row:
            cell.border = thin_border
    posting_date = datetime.now().strftime("%d-%m-%Y")
    spoc_code = frappe.db.get_value("Employee", {"user_id": spoc}, ["short_code"])
    header_value = f"{spoc_code} DSR {posting_date}"

    # Manually place the header value in the first cell
    first_cell = ws.cell(row=1, column=1)
    first_cell.value = header_value

    # Apply styles to the first cell (where the value is placed)
    first_cell.fill = header_fill
    first_cell.font = Font(bold=True)
    first_cell.alignment = Alignment(horizontal="center", vertical="center")
    first_cell.border = thin_border

    # Merge cells from column 1 to 17
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=17)

    # Apply styles to the entire merged range (though value only goes into the first cell)
    for col in range(1, 18):  # Merged range is from column 1 to 17
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
    headers = ["S.NO", "Project", "Priority", "New", "", "Open", "", "Working", "", "Overdue", "", "PR", "", "CR", "", "Total", ""]
    sub_headers = ["", "", "", "Task", "Issue", "Task", "Issue", "Task", "Issue", "Task", "Issue", "Task", "Issue", "Task", "Issue", "Task", "Issue"]
    ws.append(headers)
    ws.append(sub_headers)
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=2, column=col)
        cell.fill = head_fill
        cell.font = Font(bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
    for col in range(1, len(sub_headers) + 1):
        cell = ws.cell(row=3, column=col)
        cell.fill = row_fill
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=3)
    merged_cell = ws.cell(row=3, column=1)  # This is the top-left cell of the merged area

    # Create a new fill color
    new_fill_color = PatternFill(start_color="0f1568", end_color="0f1568", fill_type="solid")

    # Apply the new fill color to the merged cell
    merged_cell.fill = new_fill_color

    for col in range(4, 17, 2):
        ws.merge_cells(start_row=2, start_column=col, end_row=2, end_column=col + 1)
    serial_number = 1
    priority_rows = [("High",), ("Medium",), ("Low",)]

    cust = frappe.db.get_all("Project", {"status":"Open","spoc": spoc, "service": "IT-SW"}, ["*"])
    total_new_tasks=0
    total_new_issues=0
    total_open_tasks=0
    total_open_issues=0
    total_working_tasks=0
    total_working_issues=0
    total_overdue_tasks=0
    total_overdue_issues=0
    total_pr_tasks=0
    total_pr_issues=0
    total_cr_tasks=0
    total_cr_issues=0
    total_all_tasks=0
    total_all_issues=0
    current_row = 4
    s_row=4
    for c in cust:
        total_task_count = 0
        total_issue_count = 0
        priority_levels = ["High", "Medium", "Low"]
        h_new_taskcount = frappe.db.count("Task", {"spoc": spoc, "project_name": c.project_name, "priority": "High","creation": ["between", [today + " 00:00:00", today + " 23:59:59"]]})
        h_new_issuecount = frappe.db.count("Issue", {"project": c.project_name, "priority": "High","creation": ["between", [today + " 00:00:00", today + " 23:59:59"]]})
        h_open_taskcount = frappe.db.count("Task", {"status": "Open", "spoc": spoc, "project_name": c.project_name, "priority": "High"})
        h_open_issuecount = frappe.db.count("Issue", {"status": "Open", "project": c.project_name, "priority": "High"})
        h_working_taskcount=frappe.db.count("Task",{"status":"Working","spoc":spoc,"project_name":c.project_name,"priority":"High"})
        h_working_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Working","project":c.project_name,"priority":"High"})
        h_overdue_taskcount=frappe.db.count("Task",{"status":"Overdue","spoc":spoc,"project_name":c.project_name,"priority":"High"})
        h_overdue_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Overdue","project":c.project_name,"priority":"High"})
        h_pr_taskcount=frappe.db.count("Task",{"status":"Pending Review","spoc":spoc,"project_name":c.project_name,"priority":"High"})
        h_pr_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Pending Review","project":c.project_name,"priority":"High"})
        h_cr_taskcount=frappe.db.count("Task",{"status":"Client Review","spoc":spoc,"project_name":c.project_name,"priority":"High"})
        h_cr_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Client Review","project":c.project_name,"priority":"High"})
        high_task_count = h_open_taskcount + h_working_taskcount + h_overdue_taskcount + h_pr_taskcount + h_cr_taskcount
        high_issue_count = h_open_issuecount + h_working_issuecount + h_overdue_issuecount + h_pr_issuecount + h_cr_issuecount
        e_high_task_count = h_open_taskcount + h_working_taskcount + h_overdue_taskcount + h_pr_taskcount + h_cr_taskcount
        e_high_issue_count = h_open_issuecount + h_working_issuecount + h_overdue_issuecount + h_pr_issuecount + h_cr_issuecount

        total_new_tasks += h_new_taskcount
        total_new_issues += h_new_issuecount
        total_open_tasks += h_open_taskcount
        total_open_issues += h_open_issuecount
        total_working_tasks += h_working_taskcount
        total_working_issues += h_working_issuecount
        total_overdue_tasks += h_overdue_taskcount
        total_overdue_issues += h_overdue_issuecount
        total_pr_tasks += h_pr_taskcount
        total_pr_issues += h_pr_issuecount
        total_cr_tasks += h_cr_taskcount
        total_cr_issues += h_cr_issuecount
        total_all_tasks += e_high_task_count
        total_all_issues += e_high_issue_count
        # Add to total task/issue counts
        total_task_count += high_task_count
        total_issue_count += high_issue_count
        # Initialize row data
        row_data = [serial_number, c['project_name'], "High"] + [""] * 14

        # Prepare the row data, excluding the project name
        row_data[3] = '' if h_new_taskcount == 0 else h_new_taskcount  # Open Task Count (High)
        row_data[4] = '' if h_new_issuecount == 0 else h_new_issuecount  # Open Issue Count (High)
        row_data[5] = '' if h_open_taskcount == 0 else h_open_taskcount  # Open Task Count (High)
        row_data[6] = '' if h_open_issuecount == 0 else h_open_issuecount  # Open Issue Count (High)
        row_data[7] = '' if h_working_taskcount == 0 else h_working_taskcount  # Working Task Count (High)
        row_data[8] = '' if h_working_issuecount == 0 else h_working_issuecount  # Working Issue Count (High)
        row_data[9] = '' if h_overdue_taskcount == 0 else h_overdue_taskcount  # Overdue Task Count (High)
        row_data[10] = '' if h_overdue_issuecount == 0 else h_overdue_issuecount  # Overdue Issue Count (High)
        row_data[11] = '' if h_pr_taskcount == 0 else h_pr_taskcount  # Pending Review Task Count (High)
        row_data[12] = '' if h_pr_issuecount == 0 else h_pr_issuecount  # Pending Review Issue Count (High)
        row_data[13] = '' if h_cr_taskcount == 0 else h_cr_taskcount  # Client Review Task Count (High)
        row_data[14] = '' if h_cr_issuecount == 0 else h_cr_issuecount  # Client Review Issue Count (High)
        row_data[15] = '' if total_task_count == 0 else total_task_count  # Total Task Count (High)
        row_data[16] = '' if total_issue_count == 0 else total_issue_count  # Total Issue Count (High)


        ws.append(row_data)

        priority_cell = ws.cell(row=ws.max_row, column=3)  # Column C for "High"
        priority_cell.font = Font(color="FF0000")
        for idx in [3,4,5, 6, 7, 8, 9, 10, 11, 12, 13,14, 15, 16,17]:
            cell = ws.cell(row=ws.max_row, column=idx)
            cell.font = Font(color="FF0000")

        # # Now check the third column for "High" and color it red
        for row in range(4, ws.max_row+1):  # Adjust based on where your actual data starts
            cell = ws.cell(row=row, column=3)  # Third column
            if cell.value and cell.value.strip() == "High":  # Check for "High"
                cell.font = Font(color="FF0000")  # Set the font color to red
 # Change font color to red
        for priority in priority_rows[1:]:
            total_mediumtask_count = 0
            total_mediumissue_count = 0
     # Start from Medium to avoid duplicating 'High'
            priority_row_data = ["", c['project_name'], priority[0]] + [""] * 14  # Priority in column 3, rest as blanks
            # priority_row_data[1] = c['project_name']
            priority_cell = ws.cell(row=ws.max_row, column=3)  # Column C for Medium/Low
            priority_cell.font = Font(color="000000")  # Set the font color to black
            # Add counts for Medium and Low priority
            if priority[0] == "Medium":
                m_new_taskcount = frappe.db.count("Task", {"spoc": spoc, "project_name": c.project_name, "priority": "Medium","creation": ["between", [today + " 00:00:00", today + " 23:59:59"]]})
                m_new_issuecount = frappe.db.count("Issue", {"project": c.project_name, "priority": "Medium","creation": ["between", [today + " 00:00:00", today + " 23:59:59"]]})
                m_open_taskcount = frappe.db.count("Task", {"status": "Open", "spoc": spoc, "project_name": c.project_name, "priority": "Medium"})
                m_open_issuecount = frappe.db.count("Issue", {"status": "Open", "project": c.project_name, "priority": "Medium"})
                m_working_taskcount=frappe.db.count("Task",{"status":"Working","spoc":spoc,"project_name":c.project_name,"priority":"Medium"})
                m_working_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Working","project":c.project_name,"priority":"Medium"})
                m_overdue_taskcount=frappe.db.count("Task",{"status":"Overdue","spoc":spoc,"project_name":c.project_name,"priority":"Medium"})
                m_overdue_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Overdue","project":c.project_name,"priority":"Medium"})
                m_pr_taskcount=frappe.db.count("Task",{"status":"Pending Review","spoc":spoc,"project_name":c.project_name,"priority":"Medium"})
                m_pr_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Pending Review","project":c.project_name,"priority":"Medium"})
                m_cr_taskcount=frappe.db.count("Task",{"status":"Client Review","spoc":spoc,"project_name":c.project_name,"priority":"Medium"})
                m_cr_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Client Review","project":c.project_name,"priority":"Medium"})
                medium_task_count = m_open_taskcount + m_working_taskcount + m_overdue_taskcount + m_pr_taskcount + m_cr_taskcount
                medium_issue_count = m_open_issuecount + m_working_issuecount + m_overdue_issuecount + m_pr_issuecount + m_cr_issuecount
                e_medium_task_count = m_open_taskcount + m_working_taskcount + m_overdue_taskcount + m_pr_taskcount + m_cr_taskcount
                e_medium_issue_count = m_open_issuecount + m_working_issuecount + m_overdue_issuecount + m_pr_issuecount + m_cr_issuecount
                total_new_tasks +=  m_new_taskcount
                total_new_issues +=m_new_issuecount
                total_open_tasks += m_open_taskcount
                total_open_issues +=  m_open_issuecount
                total_working_tasks +=  m_working_taskcount
                total_working_issues +=  m_working_issuecount
                total_overdue_tasks +=  m_overdue_taskcount
                total_overdue_issues +=  m_overdue_issuecount
                total_pr_tasks += m_pr_taskcount
                total_pr_issues +=m_pr_issuecount
                total_cr_tasks += m_cr_taskcount
                total_cr_issues += m_cr_issuecount             # Accumulate to total task/issue counts
                total_mediumtask_count += medium_task_count
                total_mediumissue_count += medium_issue_count
                total_all_tasks += e_medium_task_count
                total_all_issues += e_medium_issue_count
                priority_row_data[3] = '' if m_new_taskcount == 0 else m_new_taskcount  # Open Task Count (High)
                priority_row_data[4] = '' if m_new_issuecount == 0 else m_new_issuecount  # Open Issue Count (High)
                priority_row_data[5] = '' if m_open_taskcount == 0 else m_open_taskcount  # Open Task Count (Medium)
                priority_row_data[6] = '' if m_open_issuecount == 0 else m_open_issuecount  # Open Issue Count (Medium)
                priority_row_data[7] = '' if m_working_taskcount == 0 else m_working_taskcount  # Working Task Count (Medium)
                priority_row_data[8] = '' if m_working_issuecount == 0 else m_working_issuecount  # Working Issue Count (Medium)
                priority_row_data[9] = '' if m_overdue_taskcount == 0 else m_overdue_taskcount  # Overdue Task Count (Medium)
                priority_row_data[10] = '' if m_overdue_issuecount == 0 else m_overdue_issuecount  # Overdue Issue Count (Medium)
                priority_row_data[11] = '' if m_pr_taskcount == 0 else m_pr_taskcount  # Pending Review Task Count (Medium)
                priority_row_data[12] = '' if m_pr_issuecount == 0 else m_pr_issuecount  # Pending Review Issue Count (Medium)
                priority_row_data[13] = '' if m_cr_taskcount == 0 else m_cr_taskcount  # Client Review Task Count (Medium)
                priority_row_data[14] = '' if m_cr_issuecount == 0 else m_cr_issuecount  # Client Review Issue Count (Medium)
                priority_row_data[15] = '' if total_mediumtask_count == 0 else total_mediumtask_count  # Total Task Count
                priority_row_data[16] = '' if total_mediumissue_count == 0 else total_mediumissue_count  # Total Issue Count


            elif priority[0] == "Low":
                l_new_taskcount = frappe.db.count("Task", {"spoc": spoc, "project_name": c.project_name, "priority": "Low","creation": ["between", [today + " 00:00:00", today + " 23:59:59"]]})
                l_new_issuecount = frappe.db.count("Issue", {"project": c.project_name, "priority": "Low","creation": ["between", [today + " 00:00:00", today + " 23:59:59"]]})
                l_open_taskcount = frappe.db.count("Task", {"status": "Open", "spoc": spoc, "project_name": c.project_name, "priority": "Low"})
                l_open_issuecount = frappe.db.count("Issue", {"status": "Open", "project": c.project_name, "priority": "Low"})
                l_working_taskcount=frappe.db.count("Task",{"status":"Working","spoc":spoc,"project_name":c.project_name,"priority":"Low"})
                l_working_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Working","project":c.project_name,"priority":"Low"})
                l_overdue_taskcount=frappe.db.count("Task",{"status":"Overdue","spoc":spoc,"project_name":c.project_name,"priority":"Low"})
                l_overdue_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Overdue","project":c.project_name,"priority":"Low"})
                l_pr_taskcount=frappe.db.count("Task",{"status":"Pending Review","spoc":spoc,"project_name":c.project_name,"priority":"Low"})
                l_pr_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Pending Review","project":c.project_name,"priority":"Low"})
                l_cr_taskcount=frappe.db.count("Task",{"status":"Client Review","spoc":spoc,"project_name":c.project_name,"priority":"Low"})
                l_cr_issuecount=frappe.db.count("Issue",{"custom_issue_status":"Client Review","project":c.project_name,"priority":"Low"})
                low_task_count = l_open_taskcount + l_working_taskcount + l_overdue_taskcount + l_pr_taskcount + l_cr_taskcount
                low_issue_count = l_open_issuecount + l_working_issuecount + l_overdue_issuecount + l_pr_issuecount + l_cr_issuecount
                e_low_task_count = l_open_taskcount + l_working_taskcount + l_overdue_taskcount + l_pr_taskcount + l_cr_taskcount
                e_low_issue_count = l_open_issuecount + l_working_issuecount + l_overdue_issuecount + l_pr_issuecount + l_cr_issuecount
                total_new_tasks += l_new_taskcount
                total_new_issues += l_new_issuecount
                total_open_tasks += l_open_taskcount
                total_open_issues += l_open_issuecount
                total_working_tasks += l_working_taskcount
                total_working_issues += l_working_issuecount
                total_overdue_tasks += l_overdue_taskcount
                total_overdue_issues += l_overdue_issuecount
                total_pr_tasks += l_pr_taskcount
                total_pr_issues +=l_pr_issuecount
                total_cr_tasks += l_cr_taskcount
                total_cr_issues += l_cr_issuecount
                # Accumulate to total task/issue counts
                total_mediumtask_count += low_task_count
                total_mediumissue_count += low_issue_count
                total_all_tasks += e_low_task_count
                total_all_issues += e_low_issue_count
                priority_row_data[3] = '' if l_new_taskcount == 0 else l_new_taskcount  # Open Task Count (Low)
                priority_row_data[4] = '' if l_new_issuecount == 0 else l_new_issuecount  # Open Issue Count (Low)
                priority_row_data[5] = '' if l_open_taskcount == 0 else l_open_taskcount  # Open Task Count (Low)
                priority_row_data[6] = '' if l_open_issuecount == 0 else l_open_issuecount  # Open Issue Count (Low)
                priority_row_data[7] = '' if l_working_taskcount == 0 else l_working_taskcount  # Working Task Count (Low)
                priority_row_data[8] = '' if l_working_issuecount == 0 else l_working_issuecount  # Working Issue Count (Low)
                priority_row_data[9] = '' if l_overdue_taskcount == 0 else l_overdue_taskcount  # Overdue Task Count (Low)
                priority_row_data[10] = '' if l_overdue_issuecount == 0 else l_overdue_issuecount  # Overdue Issue Count (Low)
                priority_row_data[11] = '' if l_pr_taskcount == 0 else l_pr_taskcount  # Pending Review Task Count (Low)
                priority_row_data[12] = '' if l_pr_issuecount == 0 else l_pr_issuecount  # Pending Review Issue Count (Low)
                priority_row_data[13] = '' if l_cr_taskcount == 0 else l_cr_taskcount  # Client Review Task Count (Low)
                priority_row_data[14] = '' if l_cr_issuecount == 0 else l_cr_issuecount  # Client Review Issue Count (Low)
                priority_row_data[15] = '' if total_mediumtask_count == 0 else total_mediumtask_count  # Total Task Count
                priority_row_data[16] = '' if total_mediumissue_count == 0 else total_mediumissue_count  # Total Issue Count

            ws.append(priority_row_data)
            # ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row+2, end_column=2)

            for idx in [3,4,5, 6, 7, 8, 9, 10, 11, 12, 13,14, 15, 16,17]:
                cell = ws.cell(row=ws.max_row, column=idx)
                cell.font = Font(color="000000")
            for row in range(4, ws.max_row+1):  # Adjust based on where your actual data starts
                cell = ws.cell(row=row, column=3)  # Third column
                if cell.value and cell.value.strip() == "High":  # Check for "High"
                    cell.font = Font(color="FF0000")

        serial_number += 1
        ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row+2, end_column=2)
        ws.merge_cells(start_row=s_row, start_column=1, end_row=s_row+2, end_column=1)
        merged_cell = ws.cell(row=current_row, column=2)
        merges_cell = ws.cell(row=s_row, column=1)  # Get the first cell of the merged range
        merged_cell.alignment = Alignment(horizontal="center",vertical='center')
        merges_cell.alignment = Alignment(horizontal="center",vertical='center')


        current_row += 3
        s_row +=3
    total_row = ["", "TOTAL", "",
        total_new_tasks, total_new_issues,
        total_open_tasks, total_open_issues,
        total_working_tasks, total_working_issues,
        total_overdue_tasks, total_overdue_issues,
        total_pr_tasks, total_pr_issues,
        total_cr_tasks, total_cr_issues,
        total_all_tasks, total_all_issues
    ]
    ws.append(total_row)
    total_row_index = ws.max_row
# Merge the first three cells in the total row
    ws.merge_cells(start_row=total_row_index, start_column=1, end_row=total_row_index, end_column=3)
    merged_cell = ws.cell(row=total_row_index, column=1)
    merged_cell.value = "TOTAL"
    for col in range(1, len(total_row) + 1):
        cell = ws.cell(row=ws.max_row, column=col)
        cell.fill = row_fill
        cell.font = Font(bold=True, color="000000")  # Bold black font for the total row
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=17):
        for cell in row:
            cell.border = thin_border
    # Save the workbook to a BytesIO object
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)

    return xlsx_file

def get_spoc_list_weekly():
    projects = frappe.get_all("Project", filters={'status': 'Open', 'service': 'IT-SW',"spoc":("not in",["abdulla.pi@groupteampro.com","sarath.v@groupteampro.com"])}, fields=['spoc'])
    spoc_set = {project['spoc'] for project in projects if project.get('spoc')}
    return list(spoc_set)

@frappe.whitelist()
def send_mail_for_expenseapproval_weekly_md():
    expenses=frappe.db.get_all("Expense Claim",{"workflow_state":"Pending for MD"},["*"])
    s_no=1
    data = '<table border="1" style="border-collapse: collapse; width: 100%;">'
    data += '<tr style="background-color: #002060; color: white;">' \
            '<td style="text-align:center; font-weight:bold; color:white;">S NO</td>' \
            '<td style="text-align:center; font-weight:bold; color:white;">ID</td>' \
            '<td style="text-align:center; font-weight:bold; color:white;">Employee</td>' \
            '<td style="text-align:center; font-weight:bold; color:white;">Total Claimed Amount</td>' \
            '</tr>'
    for i in expenses:
        data += f'<tr>' \
                f'<td style="text-align:center;">{s_no}</td>' \
                f'<td style="text-align:center;">{i.name}</td>' \
                f'<td style="text-align:center;">{i.employee_name}</td>' \
                f'<td style="text-align:center;">{i.total_claimed_amount}</td>' \
                '</tr>'
        s_no+=1
    data += '</table>'
    frappe.sendmail(
            recipients=['dineshbabu.k@groupteampro.com'],
            subject='Expense Claim Waiting for Approval' ,
            message="""
            <b>Dear Sir/Madam,</b><br><br>
            Please find below the list of expense claims waiting for your approval:<br><br>
            {}<br><br>
            Thanks & Regards,<br>TEAM ERP<br><br>
            <i>This email has been automatically generated. Please do not reply.</i>
        """.format(data)
        )

@frappe.whitelist()
def send_mail_for_expenseapproval_weekly_ceo():
    expenses=frappe.db.get_all("Expense Claim",{"workflow_state":"Pending for CEO"},["*"])
    s_no=1
    data = '<table border="1" style="border-collapse: collapse; width: 100%;">'
    data += '<tr style="background-color: #002060; color: white;">' \
            '<td style="text-align:center; font-weight:bold; color:white;">S NO</td>' \
            '<td style="text-align:center; font-weight:bold; color:white;">ID</td>' \
            '<td style="text-align:center; font-weight:bold; color:white;">Employee</td>' \
            '<td style="text-align:center; font-weight:bold; color:white;">Total Claimed Amount</td>' \
            '</tr>'
    for i in expenses:
        data += f'<tr>' \
                f'<td style="text-align:center;">{s_no}</td>' \
                f'<td style="text-align:center;">{i.name}</td>' \
                f'<td style="text-align:center;">{i.employee_name}</td>' \
                f'<td style="text-align:center;">{i.total_claimed_amount}</td>' \
                '</tr>'
        s_no+=1
    data += '</table>'
    frappe.sendmail(
            recipients=['sangeetha.s@groupteampro.com'],
            subject='Expense Claim Waiting for Approval' ,
            message="""
            <b>Dear Sir/Madam,</b><br><br>
            Please find below the list of expense claims waiting for your approval:<br><br>
            {}<br><br>
            Thanks & Regards,<br>TEAM ERP<br><br>
            <i>This email has been automatically generated. Please do not reply.</i>
        """.format(data)
        )

@frappe.whitelist()
def send_mail_for_expenseapproval_weekly_hod():
    expenses=frappe.db.get_all("Expense Claim",{"workflow_state":"Pending for HOD"},["*"])
    # Group expense claims by Expense Approver
    approver_expenses = {}
    for expense in expenses:
        approver = expense.get("expense_approver")
        if approver not in approver_expenses:
            approver_expenses[approver] = []
        approver_expenses[approver].append(expense)
    for approver, approver_expense_list in approver_expenses.items():
        s_no = 1
        data = '<table border="1" style="border-collapse: collapse; width: 100%;">'
        data += '<tr style="background-color: #002060; color: white;">' \
                '<td style="text-align:center; font-weight:bold; color:white;">S NO</td>' \
                '<td style="text-align:center; font-weight:bold; color:white;">ID</td>' \
                '<td style="text-align:center; font-weight:bold; color:white;">Employee</td>' \
                '<td style="text-align:center; font-weight:bold; color:white;">Total Claimed Amount</td>' \
                '</tr>'

        # Add each expense claim to the email content
        for expense in approver_expense_list:
            data += f'<tr>' \
                    f'<td style="text-align:center;">{s_no}</td>' \
                    f'<td style="text-align:center;">{expense["name"]}</td>' \
                    f'<td style="text-align:center;">{expense["employee_name"]}</td>' \
                    f'<td style="text-align:center;">{expense["total_claimed_amount"]}</td>' \
                    '</tr>'
            s_no += 1
        data += '</table>'

        # Send the email
        frappe.sendmail(
            # recipients=["divya.p@groupteampro.com"],
            recipients=[approver],  # Send to the respective approver
            subject='Expense Claim Waiting for Approval',
            message=f"""
                <b>Dear {approver},</b><br><br>
                Please find below the list of expense claims waiting for your approval:<br><br>
                {data}<br><br>
                Thanks & Regards,<br>TEAM ERP<br><br>
                <i>This email has been automatically generated. Please do not reply.</i>
            """
        )


@frappe.whitelist()
def purchase_invoice_due_above():
    purchase_invoices = frappe.get_all("Purchase Invoice",{"status": ("in", ["Partly Paid", "Unpaid", "Overdue"]),"docstatus": ("!=",2),"due_date": (">=", nowdate())},["*"])
    # print(purchase_invoices)
    # purchase_invoices = frappe.get_all("Purchase Invoice",{"status": "Paid","docstatus": ("!=",2),"due_date": (">=", nowdate())},["*"])

    count = 1
    f_count=0
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '''
    <tr style="background-color: #0f1568; text-align:center; color: white;">
        <td style='width:5%'><b>SI NO</b></td>
        <td style='width:10%'><b>Invoice Number</b></td>
        <td style='width:15%'><b>Party Name</b></td>
        <td style='width:20%'><b>Bill Value</b></td>
        <td style='width:5%'><b>Outstanding Value</b></td>
        <td style='width:10%'><b>Age of the Bill</b></td>
        <td style='width:10%'><b>Remarks</b></td>
    </tr>
    '''
    current_date = getdate(today())
    for i in purchase_invoices:
        print(i.due_date)
        posting_date = getdate(i.posting_date)
        due=getdate(i.due_date)
        age_of_bill = (current_date - posting_date).days
        age=(due -current_date).days
        data += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>The Due date for this invoice will  approach in {} days</td></tr>'.format(count,i.name, i.supplier,i.grand_total,i.outstanding_amount,age_of_bill,age)
        count += 1
        f_count +=1
    print(count)

    data += '</table>'
    if f_count>=1:
        frappe.sendmail(
            recipients=['accounts@groupteampro.com','sangeetha.s@groupteampro.com'],
            subject='Purchase Invoice-Due Date Approaching',
            message="""
            <b>Dear Sir/Mam,</b><br><br>
            Please find the below purchase invoice list for your kind reference and action.<br><br>
            {}<br><br>
            Thanks & Regards,<br>TEAM ERP<br>
            <i>This email has been automatically generated. Please do not reply</i>
            """.format(data)
        )


@frappe.whitelist()
def purchase_invoice_beyond_duedate():
    purchase_invoices = frappe.db.get_all("Purchase Invoice",{"status": ["in", ["Partly Paid", "Unpaid", "Overdue"]],"docstatus": ["!=",2],"due_date": ["<=", nowdate()]},["*"])
    count = 1
    f_count=0
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '''
    <tr style="background-color: #0f1568; text-align:center; color: white;">
        <td style='width:5%'><b>SI NO</b></td>
        <td style='width:10%'><b>Invoice Number</b></td>
        <td style='width:15%'><b>Party Name</b></td>
        <td style='width:20%'><b>Bill Value</b></td>
        <td style='width:5%'><b>Outstanding Value</b></td>
        <td style='width:10%'><b>Age of the Bill</b></td>
    </tr>
    '''
    current_date = getdate(today())
    for i in purchase_invoices:
        posting_date = getdate(i.posting_date)
        age_of_bill = (current_date - posting_date).days
        data += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(count,i.name, i.supplier,i.grand_total,i.outstanding_amount,age_of_bill)
        count += 1
        f_count +=1
    print(count)

    data += '</table>'
    if f_count>=1:
        frappe.sendmail(
            recipients=['accounts@groupteampro.com','sangeetha.s@groupteampro.com'],
            subject='Purchase Invoice-Beyond Due Date',
            message="""
            <b>Dear Sir/Mam,</b><br><br>
            Please find the below purchase invoice list for your kind reference and action.<br><br>
            {}<br><br>
            Thanks & Regards,<br>TEAM ERP<br>
            <i>This email has been automatically generated. Please do not reply</i>
            """.format(data)
        )

@frappe.whitelist()
def dpnd_excel_format():
    filename = "DND Details_" + today() +".xlsx"
    xlsx_file = build_xlsx_response(filename)
    dnd_report(filename, xlsx_file.getvalue())

def dnd_report(filename,file_content):
    task=frappe.db.get_all("Closure",{"custom_status_transition":nowdate()},["*"],order_by='project')
    count=0
    closure_status=["PSL","Sales Order","Client Offer Letter","Signed Offer Letter","Visa","Premedical","PCC","Certificate Attestation","Final Medical","Biometric","Visa Stamping","Emigration","Ticket","Onboarding","Arrived","Dropped","Waitlisted"]
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table += '<tr style="background-color: #87CEFA"><td style="width: 45%; font-weight: bold; text-align: center;">Closure ID</td><td style="width: 30%; font-weight: bold; text-align: center;">Candidate Name</td><td style="width: 25%; font-weight: bold; text-align: center;">Project</td><td style="width: 45%; font-weight: bold; text-align: center;">Status</td><td style="width: 25%; font-weight: bold; text-align: center;">Current Status</td></tr>'
    for i in task:
        if i.status in closure_status:
            indx=closure_status.index(i.status)
            next_indx=closure_status[indx-1]
        table += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (i.name,i.given_name,i.project,next_indx,i.status)
        count+=1
    table += '</table>'
    subject = "DND Transition -  %s" % nowdate()
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below Transition :<br><br>{}<br><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(table)
    if count>=1:
        frappe.sendmail(
            recipients=["dc@groupteampro.com","sangeetha.a@groupteampro.com"],
            # recipients=["divya.p@groupteampro.com"],
            subject=subject,
            message=message,
            # attachments=attachments,
            attachments=[{
                "fname": filename,
                "fcontent": file_content,
            }
            ]
        )


def build_xlsx_response(filename):
    xlsx_file = make_xlsx_dnd(filename)
    return xlsx_file

def make_xlsx_dnd(filename, sheet_name=None, wb=None, column_widths=None):
    # args = frappe.local.form_dict
    column_widths = column_widths or []
    data_row=[]
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name, 0)
    fill = PatternFill(start_color="87CEFA", end_color="87CEFA", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    header_row = ["Closure ID", "Candidate Name", "Project", "Status","Current Status"]
    ws.append(header_row)
    for cell in ws[1]:
        cell.fill = fill
        cell.border = thin_border
    # ws.append(["Closure ID","Candidate Name","Project","Status"])
    # ws.append([args.closure_id,args.candidate_name,args.project,args.status])
    closure_data=frappe.db.get_all("Closure",{"custom_status_transition":nowdate()},["*"],order_by='project')
    closure_status=["PSL","Sales Order","Client Offer Letter","Signed Offer Letter","Visa","Premedical","PCC","Certificate Attestation","Final Medical","Biometric","Visa Stamping","Emigration","Ticket","Onboarding","Arrived","Dropped","Waitlisted"]
    for i in closure_data:
        if i.status in closure_status:
            indx=closure_status.index(i.status)
            next_indx=closure_status[indx-1]
        data_row = [i.name or '', i.given_name or '', i.project or '',next_indx, i.status or '']
        ws.append(data_row)
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file

def send_project_report():
    posting_date = datetime.now().strftime("%d-%m-%Y")
    filename = "PTSR_" + posting_date
    xlsx_file = build_xlsx_response_project(filename)
    send_mail_with_attachment_project(filename, xlsx_file.getvalue())

def send_mail_with_attachment_project(filename, file_content):
    posting_date = datetime.now().strftime("%d-%m-%Y")
    subject = "REC : Project – Task Status Report : - %s" % posting_date
    message = (
        "Dear Sir/Madam,<br>"
        "Please find attached the attached Project Report.<br><br>"
        "<br>Thanks & Regards,<br>TEAM ERP<br>"
        "This email has been automatically generated. Please do not reply"
    )
    attachments = [{"fname": filename + '.xlsx', "fcontent": file_content}]
    frappe.sendmail(
        recipients=["dineshbabu.k@groupteampro.com","sangeetha.a@groupteampro.com","sangeetha.s@groupteampro.com","annie.m@groupteampro.com",'keerthana.k@groupteampro.com','lokeshkumar.a@groupteampro.com','aruna.g@groupteampro.com'],
        # recipients=['sangeetha.a@groupteampro.com'],
        cc='',
        sender=None,
        subject=subject,
        message=message,
        attachments=attachments,
    )
def build_xlsx_response_project(filename):
    return make_xlsx_project(filename)
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill, Font, Border
from openpyxl.utils import get_column_letter
from io import BytesIO
from datetime import datetime

def make_xlsx_project(filename, sheet_name=None, wb=None, column_widths=None):
    if wb is None:
        wb = Workbook()
    ws = wb.create_sheet(sheet_name or filename, 0)
    default_column_widths = [8, 30, 15, 43, 43, 15, 15, 15, 15, 34, 18]
    column_widths = column_widths or default_column_widths
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width
    posting_date = datetime.now().strftime("%d-%m-%Y")
    ftitle = "REC : Project – Task Status Report : - " + posting_date
    ws.append([ftitle])
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=17)
    title_cell = ws.cell(row=1, column=1)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    header_fill = PatternFill(start_color="0f1568", end_color="0f1568", fill_type="solid")
    header_font = Font(color="FFFFFF")
    headers = ["SI NO", "CUSTOMER/PROJECT NAME", "Project Priority", "AM Remark", "PM Remark",'SPOC Remark', 'Expected Value', 'Expected PSL', 'Sourcing Status', 'Territory', 'TASK', 'Task Priority', '#VAC', '#SP', '#FP', '#SL', '#PSL', '#LP']
    black_border = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000")
    )
    ws.append(headers)
    header_row = ws[ws.max_row]
    for cell in header_row:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = black_border
    cust = frappe.db.sql("""SELECT * FROM `tabCustomer` WHERE `disabled` = 0 AND service IN ('REC-I','REC-D') ORDER BY `customer_name` ASC""", as_dict=True)
    row = 3
    serial_number = 1
    grand_totals = {'vac':0,'sp': 0,'fp': 0,'sl':0,'psl':0,'custom_lp':0}
    for c in cust:
        priority = {"High": 1, "Medium": 2, "Low": 3}
        pname = frappe.get_all("Project", {"status": ("in", ['Open', 'Enquiry']), "customer": c['name'], "service": ("in", ['REC-I', 'REC-D'])}, ['*'],order_by= "priority ASC")
        if not pname:
            continue
        task_totals = {'vac':0,'sp':0,'fp':0,'sl':0,'psl':0,'custom_lp':0}
        project_data = []
        for p in pname:
            pdata = []
            print(p.project_name)
            taskid = frappe.get_all("Task", {"status": ("in",('Working', 'Open', 'Overdue', 'Pending Review')), "project": p.name}, ['*'],order_by= "priority ASC")
            # print(p['project_name'])
            # for tn in taskid:
                # print(tn.name)
            for t in taskid:
                pdata.append([p['project_name'] if p['project_name'] else "",p['priority'] if p['priority'] else "",p['remark'] if p['remark'] else "",p['account_manager_remark'] if p['account_manager_remark'] else "",p['custom_spoc_remark'] if p['custom_spoc_remark'] else "",p['expected_value'] if p['expected_value'] else "",p['expected_psl'] if p['expected_psl'] else "",p['sourcing_statu'] if p['sourcing_statu'] else "",p['territory'] if p['territory'] else "",t['subject'],t['priority'],t['vac'],t['sp'],t['fp'],t['sl'],t['psl'],t['custom_lp']])
                task_totals['vac'] +=t['vac']
                task_totals['sp'] +=t['sp']
                task_totals['fp']+= t['fp']
                task_totals['sl'] +=t['sl']
                task_totals['psl'] += t['psl']
                task_totals['custom_lp'] += t['custom_lp']
            project_data.append({
                'project_name': p['project_name'],'priority': p['priority'],
                'remark': p['remark'],'account_manager_remark': p['account_manager_remark'],'custom_spoc_remark':p['custom_spoc_remark'],'sourcing_statu': p['sourcing_statu'],'territory': p['territory'],
                'expected_value': p['expected_value'],'expected_psl': p['expected_psl'],'tasks': pdata})
        blue_fill = PatternFill(start_color="98d7f5", end_color="98d7f5", fill_type="solid")
        row_data = [serial_number, c['name']] + [""] * 10 + [task_totals['vac'], task_totals['sp'], task_totals['fp'], task_totals['sl'], task_totals['psl'],task_totals['custom_lp']]
        ws.append(row_data)
        row_to_fill = ws.max_row
        for col, cell in enumerate(ws[row_to_fill], start=1):
            cell.fill = blue_fill
            if col > 11:
                cell.alignment = Alignment(horizontal="center",vertical="center",wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left",vertical="center",wrap_text=True)
            cell.border = black_border
        ws.merge_cells(start_row=row_to_fill, start_column=2, end_row=row_to_fill, end_column=3)
        serial_number += 1
        row += 1
        current_row_start = row
        for project in project_data:
            project_row_start = row
            for task_data in project['tasks']:
                ws.append([""] + task_data)
                for col in range(2, len(task_data) + 2):
                    cell = ws.cell(row=row, column=col)
                    if 2 <= col <= 11:
                        cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                    else:
                        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                    cell.border = black_border
                row += 1
            if project_row_start < row - 1:
                for col in range(2, 10):
                    ws.merge_cells(start_row=project_row_start, start_column=col, end_row=row-1, end_column=col)
                ws.merge_cells(start_row=project_row_start, start_column=1, end_row=row-1, end_column=1)
        grand_totals['vac'] += task_totals['vac']
        grand_totals['sp'] += task_totals['sp']
        grand_totals['fp'] += task_totals['fp']
        grand_totals['sl'] += task_totals['sl']
        grand_totals['psl'] += task_totals['psl']
        grand_totals['custom_lp'] +=task_totals['custom_lp']
    yellow_fill = PatternFill(start_color="0f1568", end_color="0f1568", fill_type="solid")
    ws.append(['Total'] + [''] * 10 + [grand_totals['vac'], grand_totals['sp'], grand_totals['fp'], grand_totals['sl'], grand_totals['psl'],grand_totals['custom_lp']])
    last_row = ws.max_row
    for cell in ws[last_row]:
        cell.fill = yellow_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = black_border
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file

def send_closure_report_with_table_dsr():
    today_date = datetime.today().date()
    formatted_date = today_date.strftime('%d-%m-%Y')
    filename1 = "Closure_Direct_" + formatted_date
    filename2 = "Closure_Indirect_" + formatted_date
    filename3 = "Closure_bdm_" + formatted_date
    xlsx_files = create_multiple_xlsx_closure_dsr()
    
    html_table, total_count , html_table_2, total_count_2, html_table_3, total_count_3 = closure_next_action_dsr()
    if total_count > 0 and total_count_2 > 0 and total_count_3 >0  :
        send_mail_with_attachment_and_html_dsr(html_table, html_table_2,html_table_3 ,filename1,filename2,filename3, xlsx_files)
    elif total_count > 0 and total_count_2 <= 0 and total_count_3 > 0 :
        send_mail_with_attachment_and_html_dsr(html_table,"",html_table_3, filename1,"",filename3, xlsx_files)
    elif total_count_2 > 0 and total_count <= 0 and total_count_3 >0 :
        send_mail_with_attachment_and_html_dsr("",html_table_2,html_table_3,"", filename2,filename3, xlsx_files)
    elif total_count_2 > 0 and total_count > 0 and total_count_3 <=0 :
        send_mail_with_attachment_and_html_dsr(html_table,html_table_2,"", filename1,filename2,"", xlsx_files)
    elif total_count_2 <= 0 and total_count > 0 and total_count_3 <=0 :
        send_mail_with_attachment_and_html_dsr(html_table,"","", filename1,"","", xlsx_files)
    elif total_count_2 > 0 and total_count <= 0 and total_count_3 <=0 :
        send_mail_with_attachment_and_html_dsr("",html_table_2,"","", filename2,"", xlsx_files)
    elif total_count_2 <= 0 and total_count <= 0 and total_count_3 > 0 :
        send_mail_with_attachment_and_html_dsr("","",html_table_3,"","", filename3, xlsx_files)
            
            

def send_mail_with_attachment_and_html_dsr(html_table = None , html_table_2 = None, html_table_3 = None, filename1 =None, filename2 =None, filename3 =None,file_content = None ):
    date_str = nowdate()  

    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    
    formatted_date = date_obj.strftime('%d-%m-%Y')

    
    subject = "DND DSR - %s" % formatted_date
    
    
    message = (
        "Dear Sir/Madam,<br>"
        "Please find attached the attached Report based on Next Action.<br><br>"
        + html_table + "<br>"
        +html_table_2+"<br>"
        +html_table_3+
        "<br>Thanks & Regards,<br>TEAM ERP<br>"
        "This email has been automatically generated. Please do not reply"
    )
    if file_content:
        
        
        attachments = []
        if filename1:
            attachments.append({"fname": filename1 + '.xlsx', "fcontent": file_content[0].getvalue()})
        if filename2:
            attachments.append({"fname": filename2 + '.xlsx', "fcontent": file_content[1].getvalue()})
        if filename3:
            attachments.append({"fname": filename3 + '.xlsx', "fcontent": file_content[2].getvalue()})

            
    
                
                
             
    frappe.sendmail(
        
        recipients=['dc@groupteampro.com','sangeetha.s@groupteampro.com','dineshbabu.k@groupteampro.com'],
        sender=None,
        subject=subject,
        message=message,
        attachments=attachments,
    )

def create_multiple_xlsx_closure_dsr():
    action_date = nowdate()
    
    # action_date = "31-10-2025"
    
    conditions_file1 = {"last_updated_on": action_date,'stamping_vendor':("is", "not set"),"sa_id": ("is", "not set"),'status':("In", ['Final Medical','Biometric','Signed Offer Letter','Ticket','Premedical','PCC','Emigration'])}
    
    conditions_file2 = {"last_updated_on": action_date,'stamping_vendor':("is", "set"),"sa_id": ("is", "set"),'status':("In", ['Final Medical','Biometric','Signed Offer Letter','Ticket','Premedical','PCC','Emigration'])}
    
    conditions_file3 = {"last_updated_on": action_date,'status':("In", ['Visa','Client Offer Letter','Ticket'])}

    filename1 = "Closure_Direct_" + today()
    filename2 = "Closure_Indirect_" + today()
    filename3 = "Closure_bdm_" + today() 
    file1 = make_xlsx_closure_dsr(filename1, custom_conditions=conditions_file1)
    file2 = make_xlsx_closure_dsr(filename2, custom_conditions=conditions_file2)
    file3 = make_xlsx_closure_dsr(filename3, custom_conditions=conditions_file3)
    
    
    return [file1, file2, file3]

def closure_next_action_dsr():
    
    action_date = nowdate()
    # action_date = "31-10-2025"
    
    #Direct2
    # Fetch Closure records for Direct Follow Up
    closures = frappe.get_all(
        "Closure",
        {
            "last_updated_on": action_date,
            'stamping_vendor': ("is", "not set"),
            "sa_id": ("is", "not set"),
            'status': ("in", ['Final Medical', 'Biometric', 'Signed Offer Letter', 'Ticket', 'Premedical', 'PCC', 'Emigration'])
        },
        ["customer", "status", "name"]
    )

    # Fetch DND DPR Records for Direct Follow Up
    dnd_dpr_records = frappe.get_all(
        "DND DPR Records",
        {
            "dpr_date": action_date,
            "follow_up": "Direct Follow Up"
        },
        ["customer", "status", "name"]
    )

    # Group closure records by customer
    closure_data_by_customer = {}
    for c in closures:
        closure_data_by_customer.setdefault(c.customer, []).append(c)

    # Group DND DPR records by customer
    dpr_data_by_customer = {}
    for d in dnd_dpr_records:
        dpr_data_by_customer.setdefault(d.customer, []).append(d)

    # Get union of all customers
    all_customers = set(closure_data_by_customer.keys()).union(dpr_data_by_customer.keys())

    # Start HTML table
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table += '<tr style="background-color: #87CEFA"><td colspan="5" style=" font-weight: bold; text-align: center;">Direct Follow Up</td></tr>'
    table += '<tr style="background-color: #87CEFA">'
    table += '<td style="width: 20%; font-weight: bold; text-align: center;">Customer</td>'
    table += '<td style="width: 20%; font-weight: bold; text-align: center;">Closure Status</td>'
    table += '<td style="width: 10%; font-weight: bold; text-align: center;">Closure Count</td>'
    table += '<td style="width: 20%; font-weight: bold; text-align: center;">DPR Status</td>'
    table += '<td style="width: 10%; font-weight: bold; text-align: center;">DPR Count</td>'
    table += '</tr>'

    total_count = 0

    for customer in all_customers:
        closure_statuses = {}
        for closure in closure_data_by_customer.get(customer, []):
            closure_statuses.setdefault(closure.status, []).append(closure.name)

        dpr_statuses = {}
        for dpr in dpr_data_by_customer.get(customer, []):
            dpr_statuses.setdefault(dpr.status, []).append(dpr.name)

        closure_items = list(closure_statuses.items())
        dpr_items = list(dpr_statuses.items())
        max_rows = max(len(closure_items), len(dpr_items))

        for i in range(max_rows):
            closure_row = closure_items[i] if i < len(closure_items) else ("", [])
            dpr_row = dpr_items[i] if i < len(dpr_items) else ("", [])

            closure_status, closure_ids = closure_row
            dpr_status, dpr_ids = dpr_row

            # Add total closure count
            if closure_status:
                total_count += len(closure_ids)

            table += (
                f"<tr>"
                f"<td>{customer if i == 0 else ''}</td>"
                f"<td>{closure_status}</td><td>{len(closure_ids)}</td>"
                f"<td>{dpr_status}</td><td>{len(dpr_ids)}</td>"
                f"</tr>"
            )

    table += '</table>'

    # Log total closure count
    frappe.log_error(message=str(total_count), title="Total Direct Closure Count")

    

    
        
    #InDirect2
    
    # Indirect Follow up
    closures_indirect = frappe.get_all("Closure", {
        "last_updated_on": action_date,
        'stamping_vendor': ("is", "set"),
        "sa_id": ("is", "set"),
        'status': ("In", ['Final Medical', 'Biometric', 'Signed Offer Letter', 'Ticket', 'Premedical', 'PCC', 'Emigration'])
    }, ["customer", "status", "name"])

    dnd_dpr_records_indirect = frappe.db.get_all("DND DPR Records", {
        "dpr_date": action_date,
        "follow_up": "InDirect Follow Up"
    }, ["customer", "status", "name"])

    # Organize data
    closure_data_by_customer_indirect = {}
    dpr_data_by_customer_indirect = {}

    for c in closures_indirect:
        closure_data_by_customer_indirect.setdefault(c.customer, []).append(c)

    for d in dnd_dpr_records_indirect:
        dpr_data_by_customer_indirect.setdefault(d.customer, []).append(d)

    customers_indirect = set(closure_data_by_customer_indirect.keys()).union(dpr_data_by_customer_indirect.keys())

    table_2 = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table_2 += '<tr style="background-color: #87CEFA"><td colspan="5" style=" font-weight: bold; text-align: center;">InDirect Follow Up</td></tr>'
    table_2 += '<tr style="background-color: #87CEFA"><td style="width: 20%; font-weight: bold;">Customer</td><td style="width: 20%; font-weight: bold;">Closure Status</td><td style="width: 10%; font-weight: bold;">Closure Count</td><td style="width: 20%; font-weight: bold;">DPR Status</td><td style="width: 10%; font-weight: bold;">DPR Count</td></tr>'

    for customer in customers_indirect:
        closure_statuses = {}
        dpr_statuses = {}

        for closure in closure_data_by_customer_indirect.get(customer, []):
            closure_statuses.setdefault(closure.status, []).append(closure.name)

        for dpr in dpr_data_by_customer_indirect.get(customer, []):
            dpr_statuses.setdefault(dpr.status, []).append(dpr.name)

        closure_items = list(closure_statuses.items())
        dpr_items = list(dpr_statuses.items())
        max_rows = max(len(closure_items), len(dpr_items), 1)

        for i in range(max_rows):
            closure_row = closure_items[i] if i < len(closure_items) else ("", [])
            dpr_row = dpr_items[i] if i < len(dpr_items) else ("", [])

            closure_status, closure_ids = closure_row
            dpr_status, dpr_ids = dpr_row

            table_2 += (
                f"<tr>"
                f"<td>{customer if i == 0 else ''}</td>"
                f"<td>{closure_status}</td><td>{len(closure_ids)}</td>"
                f"<td>{dpr_status}</td><td>{len(dpr_ids)}</td>"
                f"</tr>"
            )

    table_2 += '</table>'

    total_count_indirect = sum(len(ids) for statuses in closure_data_by_customer_indirect.values() for ids in statuses)


    
    
    
    #BDM2
    
    # BDM Follow Up
    closures_bdm = frappe.get_all("Closure", {
        "last_updated_on": action_date,
        "status": ("In", ['Visa', 'Client Offer Letter', 'Ticket'])
    }, ["customer", "status", "name"])

    dnd_dpr_records_bdm = frappe.db.get_all("DND DPR Records", {
        "dpr_date": action_date,
        "follow_up": "BDM Follow Up"
    }, ["customer", "status", "name"])

    # Organize data
    closure_data_by_customer_bdm = {}
    dpr_data_by_customer_bdm = {}

    for c in closures_bdm:
        closure_data_by_customer_bdm.setdefault(c.customer, []).append(c)

    for d in dnd_dpr_records_bdm:
        dpr_data_by_customer_bdm.setdefault(d.customer, []).append(d)

    customers_bdm = set(closure_data_by_customer_bdm.keys()).union(dpr_data_by_customer_bdm.keys())

    table_3 = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table_3 += '<tr style="background-color: #87CEFA"><td colspan="5" style=" font-weight: bold; text-align: center;">BDM Follow Up</td></tr>'
    table_3 += '<tr style="background-color: #87CEFA"><td style="width: 20%; font-weight: bold;">Customer</td><td style="width: 20%; font-weight: bold;">Closure Status</td><td style="width: 10%; font-weight: bold;">Closure Count</td><td style="width: 20%; font-weight: bold;">DPR Status</td><td style="width: 10%; font-weight: bold;">DPR Count</td></tr>'

    for customer in customers_bdm:
        closure_statuses = {}
        dpr_statuses = {}

        for closure in closure_data_by_customer_bdm.get(customer, []):
            closure_statuses.setdefault(closure.status, []).append(closure.name)

        for dpr in dpr_data_by_customer_bdm.get(customer, []):
            dpr_statuses.setdefault(dpr.status, []).append(dpr.name)

        closure_items = list(closure_statuses.items())
        dpr_items = list(dpr_statuses.items())
        max_rows = max(len(closure_items), len(dpr_items), 1)

        for i in range(max_rows):
            closure_row = closure_items[i] if i < len(closure_items) else ("", [])
            dpr_row = dpr_items[i] if i < len(dpr_items) else ("", [])

            closure_status, closure_ids = closure_row
            dpr_status, dpr_ids = dpr_row

            table_3 += (
                f"<tr>"
                f"<td>{customer if i == 0 else ''}</td>"
                f"<td>{closure_status}</td><td>{len(closure_ids)}</td>"
                f"<td>{dpr_status}</td><td>{len(dpr_ids)}</td>"
                f"</tr>"
            )

    table_3 += '</table>'

    total_count_bdm = sum(len(ids) for statuses in closure_data_by_customer_bdm.values() for ids in statuses)
    return table, total_count ,table_2, total_count_indirect , table_3, total_count_bdm

def make_xlsx_closure_dsr(filename, sheet_name=None, wb=None, column_widths=None, custom_conditions=None):
    action = nowdate()

    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name or filename, 0)

    default_column_widths = [45, 25, 20, 30, 25, 20, 20]
    column_widths = column_widths or default_column_widths

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    bold_font = Font(bold=True)
    header_fill = PatternFill(start_color="87CEFA", end_color="87CEFA", fill_type="solid")

    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

    ws.merge_cells("A1:G1")
    ws["A1"] = (
        "Direct Follow Up" if "Direct" in filename
        else "In Direct Follow Up" if "Indirect" in filename
        else "BDM Follow Up"
    )
    ws["A1"].fill = header_fill
    ws["A1"].font = bold_font
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 35

    # Table Header
    ws.append([
        "Customer",
        "Closure Status", "Closure Count", "Closure IDs",
        "DPR Status", "DPR Count", "DPR IDs"
    ])
    for cell in ws[2]:
        cell.fill = header_fill
        cell.font = bold_font
        cell.alignment = align_center

    # Get Closure Records
    closures = frappe.get_all("Closure", custom_conditions, ["name", "customer", "status"])

    # Organize closure data by customer
    closure_by_customer = {}
    for c in closures:
        closure_by_customer.setdefault(c.customer, {}).setdefault(c.status, []).append(c.name)

    # ✅ Collect all customers from both Closure and DPR
    all_customers = set(closure_by_customer.keys())
    follow_up_type = (
        "Direct Follow Up" if "Direct" in filename
        else "InDirect Follow Up" if "Indirect" in filename
        else "BDM Follow Up"
    )

    for d in frappe.get_all("DND DPR Records", {
        "dpr_date": action,
        "follow_up": follow_up_type
    }, ["customer"]):
        all_customers.add(d.customer)

    # ✅ Now loop through all customers
    for customer in all_customers:
        closure_statuses = closure_by_customer.get(customer, {})

        dpr_records = frappe.get_all("DND DPR Records", {
            "dpr_date": action,
            "customer": customer,
            "follow_up": follow_up_type
        }, ["name", "status"])

        # Organize DPR records
        dpr_statuses = {}
        for d in dpr_records:
            dpr_statuses.setdefault(d.status, []).append(d.name)

        closure_items = list(closure_statuses.items())
        dpr_items = list(dpr_statuses.items())
        max_rows = max(len(closure_items), len(dpr_items))

        for i in range(max_rows):
            # Closure info
            closure_status, closure_ids = closure_items[i] if i < len(closure_items) else ("", [])
            closure_count = len(closure_ids)
            closure_ids_str = ", ".join(closure_ids)

            # DPR info
            dpr_status, dpr_ids = dpr_items[i] if i < len(dpr_items) else ("", [])
            dpr_count = len(dpr_ids)
            dpr_ids_str = ", ".join(dpr_ids)

            ws.append([
                customer if i == 0 else "",
                closure_status,
                closure_count,
                closure_ids_str,
                dpr_status,
                dpr_count,
                dpr_ids_str
            ])

    # ✅ Add thin border to all cells
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
    for row in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col=7):
        for cell in row:
            cell.border = thin_border
            
            
    for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=1, max_col=7):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(wrap_text=True)
            ws.row_dimensions[cell.row].height = 30

    # Save workbook
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file


def send_closure_report_with_table_dpr():
    next_date = datetime.today().date() + timedelta(days=1)
    formatted_date = next_date.strftime('%d-%m-%Y')
    filename1 = "Closure_Direct_" + formatted_date
    filename2 = "Closure_Indirect_" + formatted_date
    filename3 = "Closure_bdm_" + formatted_date
    xlsx_files = create_multiple_xlsx_closure_dpr()
    
    html_table, total_count , html_table_2, total_count_2, html_table_3, total_count_3 = closure_next_action_dpr()
    if total_count > 0 and total_count_2 > 0 and total_count_3 >0  :
        send_mail_with_attachment_and_html_dpr(html_table, html_table_2,html_table_3 ,filename1,filename2,filename3, xlsx_files)
    elif total_count > 0 and total_count_2 <= 0 and total_count_3 > 0 :
        send_mail_with_attachment_and_html_dpr(html_table,"",html_table_3, filename1,"",filename3, xlsx_files)
    elif total_count_2 > 0 and total_count <= 0 and total_count_3 >0 :
        send_mail_with_attachment_and_html_dpr("",html_table_2,html_table_3,"", filename2,filename3, xlsx_files)
    elif total_count_2 > 0 and total_count > 0 and total_count_3 <=0 :
        send_mail_with_attachment_and_html_dpr(html_table,html_table_2,"", filename1,filename2,"", xlsx_files)
    elif total_count_2 <= 0 and total_count > 0 and total_count_3 <=0 :
        send_mail_with_attachment_and_html_dpr(html_table,"","", filename1,"","", xlsx_files)
    elif total_count_2 > 0 and total_count <= 0 and total_count_3 <=0 :
        send_mail_with_attachment_and_html_dpr("",html_table_2,"","", filename2,"", xlsx_files)
    elif total_count_2 <= 0 and total_count <= 0 and total_count_3 > 0 :
        send_mail_with_attachment_and_html_dpr("","",html_table_3,"","", filename3, xlsx_files)
            
            

def send_mail_with_attachment_and_html_dpr(html_table = None , html_table_2 = None, html_table_3 = None, filename1 =None, filename2 =None, filename3 =None,file_content = None ):
    next_date_str = add_days(nowdate(), 1)

    
    next_date_obj = datetime.strptime(next_date_str, '%Y-%m-%d')

    
    formatted_date = next_date_obj.strftime('%d-%m-%Y')

    
    subject = "DND DPR - %s" % formatted_date
    message = (
        "Dear Sir/Madam,<br>"
        "Please find attached the attached Report based on Next Action.<br><br>"
        + html_table + "<br>"
        +html_table_2+"<br>"
        +html_table_3+
        "<br>Thanks & Regards,<br>TEAM ERP<br>"
        "This email has been automatically generated. Please do not reply"
    )
    if file_content:
       
        attachments = []
        if filename1:
            attachments.append({"fname": filename1 + '.xlsx', "fcontent": file_content[0].getvalue()})
        if filename2:
            attachments.append({"fname": filename2 + '.xlsx', "fcontent": file_content[1].getvalue()})
        if filename3:
            attachments.append({"fname": filename3 + '.xlsx', "fcontent": file_content[2].getvalue()})
            
    
                
                
             
    frappe.sendmail(
        recipients=['dc@groupteampro.com','sangeetha.s@groupteampro.com','dineshbabu.k@groupteampro.com'],
        sender=None,
        subject=subject,
        message=message,
        attachments=attachments,
    )

def create_multiple_xlsx_closure_dpr():
    action_date = add_days(nowdate(), 1)
    conditions_file1 = {"custom_next_follow_up_on": action_date,'stamping_vendor':("is","not set"),"sa_id": ("is", "not set"),'status':("In", ['Final Medical','Biometric','Signed Offer Letter','Ticket','Premedical','PCC','Emigration'])}
    
    conditions_file2 = {"custom_next_follow_up_on": action_date,'stamping_vendor':("is","set"),"sa_id": ("is", "set"),'status':("In", ['Final Medical','Biometric','Signed Offer Letter','Ticket','Premedical','PCC','Emigration'])}
    
    conditions_file3 = {"custom_next_follow_up_on": action_date,'status':("In", ['Visa','Client Offer Letter','Ticket'])}
    
    next_date_str = action_date  
    formatted_date = datetime.strptime(next_date_str, '%Y-%m-%d').strftime('%d-%m-%Y')

    filename1 = "Closure_Direct_" + formatted_date
    filename2 = "Closure_Indirect_" + formatted_date
    filename3 = "Closure_bdm_" + formatted_date 
    file1 = make_xlsx_closure_dpr(filename1, custom_conditions=conditions_file1)
    file2 = make_xlsx_closure_dpr(filename2, custom_conditions=conditions_file2)
    file3 = make_xlsx_closure_dpr(filename3, custom_conditions=conditions_file3)
    
    
    return [file1, file2, file3]

def closure_next_action_dpr():
    
    records_to_delete = frappe.get_all("DND DPR Records", ["name"])
    for record in records_to_delete:
        frappe.delete_doc("DND DPR Records", record.name, ignore_permissions=True)
    
    action_date = add_days(nowdate(), 1)
    #Direct Follow up
    closures = frappe.get_all("Closure", {"custom_next_follow_up_on": action_date,'stamping_vendor':("is","not set"),"sa_id": ("is", "not set"),'status':("In", ['Final Medical','Biometric','Signed Offer Letter','Ticket','Premedical','PCC','Emigration'])}, ["customer", "status","name"])
    customer_status_count = {}
    for closure in closures:
        customer = closure.customer
        status = closure.status
        name = closure.name
        if customer not in customer_status_count:
            customer_status_count[customer] = {}
        if status not in customer_status_count[customer]:
            customer_status_count[customer][status] = []
        customer_status_count[customer][status].append(name)
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table += '<tr style="background-color: #87CEFA"><td colspan="3" style=" font-weight: bold; text-align: center;">Direct Follow Up</td></tr>'
    table += '<tr style="background-color: #87CEFA"><td style="width: 45%; font-weight: bold; text-align: center;">Customer</td><td style="width: 30%; font-weight: bold; text-align: center;">Status</td><td style="width: 25%; font-weight: bold; text-align: center;">Count</td></tr>'
    for customer, statuses,  in customer_status_count.items():
        # total_counts = sum(statuses.values())
        total_counts = sum(len(ids) for ids in statuses.values()) 
        table += '<tr><td><b>%s</b></td><td></td><td><b>%s</b></td></tr>' % (customer, total_counts)        
        for status, closure_ids  in statuses.items():
            count = len(closure_ids)
            table += '<tr><td></td><td>%s</td><td>%s</td></tr>' % (status, count)
            for i in closure_ids:
                # print(f"[DUPLICATE SKIPPED] Closure ID: {i}")
                doc_1 = frappe.new_doc("DND DPR Records")
                doc_1.closure_id = i
                doc_1.dpr_date = action_date
                doc_1.customer = customer
                doc_1.status = status
                doc_1.count = 1
                doc_1.follow_up = "Direct Follow Up"
                doc_1.insert(ignore_permissions=True)
                frappe.db.commit()
            
    table += '</table>'
    # total_count = sum(sum(status.values()) for status in customer_status_count.values())
    total_count = sum(len(ids) for statuses in customer_status_count.values() for ids in statuses.values())

    
    #InDirect Follow up
    closures_indirect = frappe.get_all("Closure", {"custom_next_follow_up_on": action_date,'stamping_vendor':("is","set"),"sa_id": ("is", "set"),'status':("In", ['Final Medical','Biometric','Signed Offer Letter','Ticket','Premedical','PCC','Emigration'])}, ["customer", "status"])
    customer_status_count_indirect = {}
    for closure in closures_indirect:
        customer = closure.customer
        status = closure.status
        if customer not in customer_status_count_indirect:
            customer_status_count_indirect[customer] = {}
        if status not in customer_status_count_indirect[customer]:
            customer_status_count_indirect[customer][status] = []
        customer_status_count_indirect[customer][status].append(name) 
    table_2 = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table_2 += '<tr style="background-color: #87CEFA"><td colspan="3" style=" font-weight: bold; text-align: center;">InDirect Follow Up</td></tr>'
    table_2 += '<tr style="background-color: #87CEFA"><td style="width: 45%; font-weight: bold; text-align: center;">Customer</td><td style="width: 30%; font-weight: bold; text-align: center;">Status</td><td style="width: 25%; font-weight: bold; text-align: center;">Count</td></tr>'
    for customer, statuses in customer_status_count_indirect.items():
        # total_counts_indirect = sum(statuses.values())
        total_counts_indirect = sum(len(ids) for ids in statuses.values()) 
        table_2 += '<tr><td><b>%s</b></td><td></td><td><b>%s</b></td></tr>' % (customer, total_counts_indirect)        
        for status, closure_ids  in statuses.items():
            count = len(closure_ids)
            table_2 += '<tr><td></td><td>%s</td><td>%s</td></tr>' % (status, count)
            for i in closure_ids:
                doc_2 = frappe.new_doc("DND DPR Records")
                doc_2.closure_id = i
                doc_2.dpr_date = action_date
                doc_2.customer = customer
                doc_2.status = status
                doc_2.count = count
                doc_2.follow_up = "InDirect Follow Up"
                doc_2.insert(ignore_permissions=True)
            frappe.db.commit()
    table_2 += '</table>'
    # total_count_indirect = sum(sum(status.values()) for status in customer_status_count_indirect.values())
    total_count_indirect = sum(len(ids) for statuses in customer_status_count_indirect.values() for ids in statuses.values())
    
    #BDM
    closures_bdm = frappe.get_all("Closure", {"custom_next_follow_up_on": action_date,'status':("In", ['Visa','Client Offer Letter','Ticket'])}, ["customer", "status"])
    customer_status_count_bdm = {}
    for closure in closures_bdm:
        customer = closure.customer
        status = closure.status
        if customer not in customer_status_count_bdm:
            customer_status_count_bdm[customer] = {}
        if status not in customer_status_count_bdm[customer]:
            customer_status_count_bdm[customer][status] = []
        customer_status_count_bdm[customer][status].append(name)
    table_3 = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table_3 += '<tr style="background-color: #87CEFA"><td colspan="3" style=" font-weight: bold; text-align: center;">BDM Follow Up</td></tr>'
    table_3 += '<tr style="background-color: #87CEFA"><td style="width: 45%; font-weight: bold; text-align: center;">Customer</td><td style="width: 30%; font-weight: bold; text-align: center;">Status</td><td style="width: 25%; font-weight: bold; text-align: center;">Count</td></tr>'
    for customer, statuses in customer_status_count_bdm.items():
        # total_counts_bdm = sum(statuses.values())
        total_counts_bdm = sum(len(ids) for ids in statuses.values())
        table_3 += '<tr><td><b>%s</b></td><td></td><td><b>%s</b></td></tr>' % (customer, total_counts_bdm)        
        for status, closure_ids in statuses.items():
            count = len(closure_ids)
            table_3 += '<tr><td></td><td>%s</td><td>%s</td></tr>' % (status, count)
            for i in closure_ids:
                doc_3 = frappe.new_doc("DND DPR Records")
                doc_3.closure_id = i
                doc_3.dpr_date = action_date
                doc_3.customer = customer
                doc_3.status = status
                doc_3.count = count
                doc_3.follow_up = "BDM Follow Up"
                doc_3.insert(ignore_permissions=True)
                frappe.db.commit()
    table_3 += '</table>'
    # total_count_bdm = sum(sum(status.values()) for status in customer_status_count_indirect.values())
    total_count_bdm = sum(len(ids) for statuses in customer_status_count_bdm.values() for ids in statuses.values())
    
    
    return table, total_count ,table_2, total_count_indirect , table_3, total_count_bdm


def make_xlsx_closure_dpr(filename, sheet_name=None, wb=None, column_widths=None, custom_conditions=None):
    action = add_days(nowdate(), 1)

    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name or filename, 0)  

    default_column_widths = [15, 35, 45, 25, 25, 40, 25]
    column_widths = column_widths or default_column_widths    

    # === Styles ===
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    bold_font = Font(bold=True)
    header_fill = PatternFill(start_color="87CEFA", end_color="87CEFA", fill_type="solid")

    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width  

    ws.merge_cells("A1:G1")
    
    # === Title Row ===
    formatted_date = datetime.strptime(action, '%Y-%m-%d').strftime('%d-%m-%Y')
    filename1 = "Closure_Direct_" + formatted_date
    filename2 = "Closure_Indirect_" + formatted_date
    filename3 = "Closure_bdm_" + formatted_date
    
    if filename == filename1:
        ws["A1"] = "Direct Follow Up"
    elif filename == filename2:
        ws["A1"] = "In Direct Follow Up"
    else:
        ws["A1"] = "BDM Follow Up"    

    ws["A1"].fill = header_fill
    ws["A1"].font = bold_font
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # === Table Header ===
    ws.append(["ID", "Candidate Name", "Customer", "Status", "Next Action", "Remark", "Next Action Date"])
    for cell in ws[2]:
        cell.fill = header_fill
        cell.font = bold_font
        cell.alignment = align_center

    # === Data Rows ===
    closures = frappe.get_all("Closure", custom_conditions, ['*'])
    if closures:
        for closure in closures:
            next_action_date = ""
            if closure.custom_next_follow_up_on:
                try:
                    next_action_date = closure.custom_next_follow_up_on.strftime("%d-%m-%Y")
                except AttributeError:
                    next_action_date = datetime.strptime(str(closure.custom_next_follow_up_on), "%Y-%m-%d").strftime("%d-%m-%Y")

            ws.append([
                closure.name,
                closure.given_name,
                closure.customer,
                closure.status,
                closure.std_remarks,
                closure.remark,
                next_action_date
            ])

    # === Apply Border, Height & Wrap ===
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    for row in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col=7):
          
        for cell in row:
            cell.border = thin_border
            
    for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=1, max_col=7):
         
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(wrap_text=True)
            ws.row_dimensions[cell.row].height = 30

    

    # === Save Workbook ===
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)    
    return xlsx_file

import openpyxl
from io import BytesIO
@frappe.whitelist()
def dpr_excel_format_bcs():
    filename = "DPR_" + today()
    users = frappe.get_all("User", filters={"role": "BCS User","enabled":1,"name":"thelothamma.r@groupteampro.com"}, fields=["*"])
    for user in users:
        email = user.name
        xlsx_file = build_xlsx_response_file(filename,user.name)
        send_mail_with_dpr_attachment(email, filename, xlsx_file.getvalue())


def send_mail_with_dpr_attachment(recipient, filename, file_content):
    subject = ("DPR-%s-%s"%(nowdate(),recipient) )
    message = "Dear Sir/Madam,<br> Please find attached the Daily Progress Report.<br>Thanks & Regards,<br>TEAM ERP<br>This email has been automatically generated. Please do not reply"
    attachments = [{"fname": filename + '.xlsx', "fcontent": file_content}]
    frappe.sendmail(
        recipients=[recipient],
        cc=['sangeetha.s@gmail.com',"keerthana.b@groupteampro.com"],
        sender=None,  
        subject=subject,
        message=message,
        attachments=attachments,
    )


def build_xlsx_response_file(filename,user_name):
    xlsx_file = make_xlsx_file(filename,user_name)
    return xlsx_file

def make_xlsx_file(filename, user_name, sheet_name=None, wb=None, column_widths=None):
    from collections import defaultdict

    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()
        # Remove the default sheet
        default_sheet = wb.active
        wb.remove(default_sheet)

    # Sheet 1: Main DPR
    ws1 = wb.create_sheet(title="DPR", index=0)
    ws1.append(["ID", "Batch", "Employee Name", "Employee Code", 'Client', 'Case ID', 'Case/Check Type',
                'Case/Check Status', 'Actual Age', 'Allocated To', 'Entry Allocated Date', 'Execution Allocated Date'])
    # Dict to track summary counts by Check Type only
    summary_counts = defaultdict(int)

    # Add Cases
    cases = frappe.get_all("Case", {"case_status": "Draft", "allocated_to": user_name},
                           ['*'], order_by='actual_tat DESC')
    for c in cases:
        ws1.append([
            c.name, c.batch, c.case_name, c.client_employee_code, c.customer, c.name,
            "Case", c.case_status, c.actual_tat, user_name,
            c.custom_allocation_date or '', ''
        ])
        summary_counts["Case"] += 1
    case_id_set = set()
    # Add Checks
    check_types = ["Education Checks", "Family", "Reference Check", "Court", "Social Media", "Criminal", "Employment", "Identity Aadhar", "Address Check"]
    for check in check_types:
        docs = frappe.get_all(check, {"allocated_to": user_name}, ['*'], order_by='actual_tat DESC')
        for d in docs:
            if d.check_status in ["Draft", "Entry QC Completed", "Execution Pending", "Execution Initiated"]:
                row = [
                    d.name, d.batch, d.name1, d.client_employee_code,
                    d.client if check in ["Address Check", "Court", "Employment", "Criminal", "Social Media", "Family"] else d.customer,
                    d.case_id, check, d.check_status, d.actual_tat, user_name,
                    d.custom_allocation_date or '', d.custom_date_of_execution_initiated or ''
                ]
                ws1.append(row)
                summary_counts[check] += 1
                if d.case_id:
                    case_id_set.add(d.case_id)

    # Sheet 2: Horizontal Summary
    ws2 = wb.create_sheet(title="Summary", index=1)
    ws2.append([])
    # Check types to include (as-is)
    check_types = ["Case","Education Checks", "Family", "Reference Check", "Court", "Social Media", "Criminal", "Employment", "Identity Aadhar", "Address Check"]

    # Add header row with original names
    # header_row = ["User"]+check_types
    # Mapping original keys to new column headers
    check_type_labels = {
        "Case": "Draft",
        "Education Checks": "Education Checks",
        "Criminal": "Criminal",
        "Employment": "Employment",
        "Identity Aadhar": "Identity Aadhar",
        "Address Check": "Address Check",
        "Family":"Family",
        "Reference Check":"Reference Check",
         "Court": "Court",
         "Social Media":"Social Media",

    }
    check_types = list(check_type_labels.keys())
    header_row = ["User"] + [check_type_labels[ct] for ct in check_types]

    ws2.append(header_row)

    # Add data row: user name + counts
    summary_row = [user_name] +[summary_counts.get(ct, 0) for ct in check_types]
    ws2.append(summary_row)

    # Apply formatting: bold header, blue fill
    header_fill = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
    bold_font = Font(bold=True)

    for cell in ws2[2]:  # first row (headers)
        cell.font = bold_font
        cell.fill = header_fill
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file

import frappe
from frappe.utils import nowdate

from frappe.utils import nowdate
@frappe.whitelist()
def kt_email():
    
    tasks = frappe.get_all("Task", filters={"kt_confirmed": False, "service": "IT-SW", "type": "OPS", "status": "Working"}, fields=["name", "subject", "customer", "project", "status", "priority", "custom_production_date", "custom_allocated_on", "custom_allocated_to", "project_manager"])

    
    task_details = []
    serial_no = 1  # Initialize serial number

    for task_doc in tasks:
        task = frappe.get_doc("Task", task_doc.name)

      
        if task.service == "IT-SW" and task.type == "OPS" and task.status == "Working":
            production_date = task.custom_production_date.strftime("%d-%m-%Y") if task.custom_production_date else ""
            allocation_date = task.custom_allocated_on.strftime("%d-%m-%Y") if task.custom_allocated_on else ""
            user = task.custom_allocated_to

            # Append task details to the list with a serial number in columns
            task_details.append(f"""
            <tr style='text-align: left;'>
                <td style='border: 1px solid black; text-align: center; padding: 8px;'>{serial_no}</td>
                <td style='border: 1px solid black; text-align: left; padding: 8px;'>{task.name}</td>
                <td style='border: 1px solid black; padding: 8px;'>{task.subject}</td>
                <td style='border: 1px solid black; padding: 8px;'>{task.customer}</td>
                <td style='border: 1px solid black; padding: 8px;'>{task.project}</td>
                <td style='border: 1px solid black; padding: 8px;'>{task.status}</td>
                <td style='border: 1px solid black; padding: 8px;'>{task.priority}</td>
                <td style='border: 1px solid black; padding: 8px;'>{production_date}</td>
                <td style='border: 1px solid black; padding: 8px;'>{allocation_date}</td>
                <td style='border: 1px solid black; padding: 8px;'>{user}</td>
            </tr>
            """)

            serial_no += 1  # Increment serial number for the next task

    # If we have any tasks, send an email
    if task_details:
        # Email Subject
        subject = "KT Not Confirmed Tasks"

        # Prepare HTML content with all task details
        email_body = f"""
        <p><strong>KT Not Confirmed Tasks</strong></p>
        <table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>
            <thead>
                <tr style="background-color: #0f1568; color: white;">
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>S.No</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Task ID</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Subject</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Customer</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Project</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Status</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Priority</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Production Date</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Allocation Date</b></th>
                    <th style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black; padding: 8px;'><b>Allocated To</b></th>
                </tr>
            </thead>
            <tbody>
                {''.join(task_details)}
            </tbody>
        </table>
        """
        

        
        frappe.sendmail(
            recipients=["abdulla.pi@groupteampro.com"],
            subject=subject,
            message=email_body
        )

@frappe.whitelist()
def case_status_report_excel():
    next_date=today()
    next_dates=datetime.strptime(next_date, '%Y-%m-%d')
    filename = "Case_Status_Report" + today() + ".xlsx"
    xlsx_file = make_xlsx_case_status(filename)
    case_status_report(filename, xlsx_file.getvalue())

def make_xlsx_case_status(filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Case Status Report"
    text_wrap_left = Alignment(vertical="center", horizontal="center")
    # Setting column widths
    for col in range(ord('A'), ord('M') + 1):  # Adjust for header range
        ws.column_dimensions[chr(col)].width = 20

    # Adding headers
    headers = [
        "Sr.no", "ID", "Employee Name", "Customer", "Check Package", "Batch", 
        "Case Status", "Case Report", "Client Employee Code", "Initiation Date",
        "Entry Allocated To", "Case Completion Date", "TAT Completion Date",
        "Insufficiency Closed", "Insufficiency Reported", "Actual Age",
        "0 to 5", "6 to 10", "11 to 15", ">15"
    ]
    ws.append(headers)  # Adding headers to the sheet

    # Formatting headers
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")  # White font color for better visibility
        cell.fill = PatternFill(start_color="FF002060", end_color="FF002060", fill_type="solid")  # aRGB format
        cell.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        cell.alignment=text_wrap_left

    # Fetching case details
    case_details = get_case_report_detaiils()

    sr_no = 1
    for case in case_details:
        tat_counts = {
            "0 to 5": "",
            "6 to 10": "",
            "11 to 15": "",
            ">15": ""
        }
        # Determine the age range for `actual_tat`
        tat_range = {
            "0 to 5": 0 <= case["actual_tat"] <= 5,
            "6 to 10": 6 <= case["actual_tat"] <= 10,
            "11 to 15": 11 <= case["actual_tat"] <= 15,
            ">15": case["actual_tat"] > 15
        }

        tat_counts = {key: 1 if condition else 0 for key, condition in tat_range.items()}

        # Append data row
        ws.append([
            sr_no,
            case.get("name"),
            case.get("case_name"),
            case.get("customer"),
            case.get("check_package"),
            case.get("batch"),
            case.get("case_status"),
            case.get("case_report"),
            case.get("client_employee_code"),
            case.get("date_of_initiating"),
            case.get("allocated_to"),
            case.get("case_completion_date"),
            case.get("end_date"),
            case.get("insufficiency_closed"),
            case.get("insufficiency_reported"),
            case.get("actual_tat"),
            tat_counts["0 to 5"] or "",
            tat_counts["6 to 10"] or "",
            tat_counts["11 to 15"] or "",
            tat_counts[">15"] or ""
        ])
        sr_no += 1
        for cell in ws[ws.max_row]:
            cell.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

    # Save to BytesIO object
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file

def get_case_report_detaiils():
    cases=frappe.db.get_all("Case",{"case_status":("not in",["Final-QC","Generate Report","Case Report Completed","Case Completed","To be Billed","SO Created","Drop"])},["*"])
    return cases

@frappe.whitelist()
def case_status_report(filename, file_content):
    data = '<table border="1" style="border-collapse: collapse; width: 100%;">'
    data += '<tr style="background-color: #002060; color: white;">' \
        '<td style="text-align:center; font-weight:bold; color:white;">Customer</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">0-5</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">6-10</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">11-15</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">>15</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">Entry Grand Total</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">Entry-Insuff</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">Execution-Insuff</td>' \
        '<td style="text-align:center; font-weight:bold; color:white;">Grand Total</td>' \
        '</tr>'

    # Fetch all batches with batch_status not "Completed"
    batches = frappe.db.get_all("Batch", {"batch_status": ("!=", "Completed")}, ["name", "customer"])

    customer_data = {}
    grand_totals = {
        "0-5": 0,
        "6-10": 0,
        "11-15": 0,
        ">15": 0,
        "Entry-Insuff": 0,
        "Execution-Insuff": 0
    }

    for batch in batches:
        customer = batch.customer
        if customer not in customer_data:
            customer_data[customer] = {
                "0-5": 0,
                "6-10": 0,
                "11-15": 0,
                ">15": 0,
                "Entry-Insuff": 0,
                "Execution-Insuff": 0
            }

        # Get cases for the current batch
        cases = frappe.db.get_all("Case", {"batch": batch.name}, ["name", "case_status", "actual_tat"])

        for case in cases:
            if case["case_status"] in ["Draft", "Entry Completed", "Entry-QC", "Execution"]:
                if 0 <= case["actual_tat"] <= 5:
                    customer_data[customer]["0-5"] += 1
                elif 6 <= case["actual_tat"] <= 10:
                    customer_data[customer]["6-10"] += 1
                elif 11 <= case["actual_tat"] <= 15:
                    customer_data[customer]["11-15"] += 1
                elif case["actual_tat"] > 15:
                    customer_data[customer][">15"] += 1

            if case["case_status"] == "Entry-Insuff":
                customer_data[customer]["Entry-Insuff"] += 1
            if case["case_status"] == "Execution-Insuff":
                customer_data[customer]["Execution-Insuff"] += 1

    # Populate the table with customer data
    for customer, counts in customer_data.items():
        # Calculate row-level totals
        entry_grand_total = counts["0-5"] + counts["6-10"] + counts["11-15"] + counts[">15"]
        grand_total = counts["Entry-Insuff"] + counts["Execution-Insuff"]

        # Update grand totals
        for key in grand_totals:
            grand_totals[key] += counts[key]

        # Append row data
        data += f'<tr>' \
            f'<td style="text-align:center;">{customer}</td>' \
            f'<td style="text-align:center;">{counts["0-5"] or ""}</td>' \
            f'<td style="text-align:center;">{counts["6-10"] or ""}</td>' \
            f'<td style="text-align:center;">{counts["11-15"] or ""}</td>' \
            f'<td style="text-align:center;">{counts[">15"] or ""}</td>' \
            f'<td style="text-align:center;">{entry_grand_total or ""}</td>' \
            f'<td style="text-align:center;">{counts["Entry-Insuff"] or ""}</td>' \
            f'<td style="text-align:center;">{counts["Execution-Insuff"] or ""}</td>' \
            f'<td style="text-align:center;">{grand_total or ""}</td>' \
            f'</tr>'

    # Append grand total row
    overall_grand_total = grand_totals["Entry-Insuff"] + grand_totals["Execution-Insuff"]
    entry_grand_total_sum = grand_totals["0-5"] + grand_totals["6-10"] + grand_totals["11-15"] + grand_totals[">15"]

    data += f'<tr style="font-weight: bold; background-color: #f2f2f2;">' \
        f'<td style="text-align:center;">Grand Total</td>' \
        f'<td style="text-align:center;">{grand_totals["0-5"] or ""}</td>' \
        f'<td style="text-align:center;">{grand_totals["6-10"] or ""}</td>' \
        f'<td style="text-align:center;">{grand_totals["11-15"] or ""}</td>' \
        f'<td style="text-align:center;">{grand_totals[">15"] or ""}</td>' \
        f'<td style="text-align:center;">{entry_grand_total_sum or ""}</td>' \
        f'<td style="text-align:center;">{grand_totals["Entry-Insuff"] or ""}</td>' \
        f'<td style="text-align:center;">{grand_totals["Execution-Insuff"] or ""}</td>' \
        f'<td style="text-align:center;">{overall_grand_total or ""}</td>' \
        f'</tr>'

    data += '</table>'

    frappe.sendmail(
        recipients=["sangeetha.s@groupteampro.com","dineshbabu.k@groupteampro.com","keerthana.b@groupteampro.com"],
        subject=_("Case Status Report"),
        message=f"""
            Dear Sir/Madam,<br><br>
            Kindly find the below list of Case Status Report:<br>{data}<br>
            Thanks & Regards,<br>
            TEAM ERP<br>
            <i>This email has been automatically generated. Please do not reply.</i>
        """,
        attachments=[
            {"fname": filename, "fcontent": file_content},
        ]
    )

import frappe
from datetime import datetime
from collections import defaultdict

@frappe.whitelist()
def task_mail():
    current_date = datetime.now().strftime("%d-%m-%Y")
    
    
    table_style = 'style="width: 100%; border-collapse: collapse;"'
    th_style = 'style="background-color:#063970; color:white; text-align:center; padding: 5px;"'
    td_style = 'style="text-align:center; padding: 5px;"'    
    open_issues_data_template = '''

    <table {0} border="1">
        <thead>
            <tr>
                <th {1} colspan="5">Open Issues - {2}</th>
            </tr>
            <tr>
                <th {1}>S.NO</th>
                <th {1}>Subject</th>
                <th {1}>Customer</th>
                <th {1}>Project</th>
                <th {1}>Count</th>
            </tr>
        </thead>
        <tbody>
    '''.format(table_style, th_style, current_date)

    assigned_to_list = frappe.db.sql("""
        SELECT project, subject, customer
        FROM `tabIssue`
        WHERE status = 'Open'
    """, as_dict=True)

    issue_counts = {}
    for issue in assigned_to_list:
        project = issue['project']
        if project not in issue_counts:
            issue_counts[project] = {'count': 0, 'subject': issue['subject'], 'customer': issue['customer']}
        issue_counts[project]['count'] += 1

    total_count = 0
    for idx, (project, data) in enumerate(issue_counts.items(), start=1):
        total_count += data['count']
        open_issues_data_template += '''
        <tr>
             <td {0}>{1}</td>
             <td {0}>{2}</td>
             <td {0}>{3}</td>
             <td {0}>{4}</td>
             <td {0}>{5}</td>
        </tr>'''.format(td_style, idx, data['subject'], data['customer'], project, data['count'])

    open_issues_data_template += '''
        <tr>
            <td {0} colspan="4"><strong>Total</strong></td>
            <td {0}><strong>{1}</strong></td>
        </tr>'''.format(td_style, total_count)

    open_issues_data_template += '''
            </tbody>
        </table>
        <br><br>
    '''
    
    
    open_meetings_data_template = '''
    <table {0} border="1">
        <thead>
            <tr>
                <th {1} colspan="3">Open Meetings - {2}</th>
            </tr>
            <tr>
                <th {1}>S.NO</th>
                <th {1}>Project</th>
                <th {1}>Count</th>
            </tr>
        </thead>
        <tbody>
    '''.format(table_style, th_style, current_date)

    assigned_to_list = frappe.db.get_all('Meeting', 
        filters={'status': ['not in', ['Completed', 'Cancelled']], 'custom_department': 'ITS - THIS'}, 
        fields=['project'])

    meeting_counts = {
        item['project']: frappe.db.count('Meeting', 
            filters={'status': ['not in', ['Completed', 'Cancelled']],'custom_department': 'ITS - THIS', 'project': item['project']})
        for item in assigned_to_list
    }

    total_count = 0
    for idx, (project, count) in enumerate(meeting_counts.items(), start=1):
        total_count += count
        open_meetings_data_template += '''
        <tr>
             <td {0}>{1}</td>
             <td {0}>{2}</td>
             <td {0}>{3}</td>
        </tr>'''.format(td_style, idx, project, count)

    open_meetings_data_template += '''
        <tr>
            <td {0} colspan="2"><strong>Total</strong></td>
            <td {0}><strong>{1}</strong></td>
        </tr>'''.format(td_style, total_count)

    open_meetings_data_template += '''
            </tbody>
        </table>
        <br><br>
    '''
    
    
    task_rt_data_template = '''
    <table {0} border="1">
        <thead>
            <tr>
                <th {1} colspan="3">Task Available RT - {2}</th>
            </tr>
            <tr>
                <th {1}>S.NO</th>
                <th {1}>CB</th>
                <th {1}>Count</th>
            </tr>
        </thead>
        <tbody>
    '''.format(table_style, th_style, current_date)
    
    tasks = frappe.db.get_all("Task", filters={'status': ['in', ['Open', 'Overdue', 'Working']], 'cb': ['not in', ['SM', 'JA']], 'service': 'IT-SW'}, fields=["cb", "rt"])
    
    cb_summary = defaultdict(lambda: {'total_rt': 0})
    
    for task in tasks:
        cb = task.get('cb', '')
        rt = task.get('rt', 0)
        
        cb_summary[cb]['total_rt'] += rt
    
    total_rt_overall = 0
    data_rows = ''
    
    for idx, (cb, summary) in enumerate(sorted(cb_summary.items()), start=1):
        total_rt = summary['total_rt']
        total_rt_overall += total_rt
        data_rows += '''
            <tr>
                <td {0}>{1}</td>
                <td {0}>{2}</td>
                <td {0}>{3}</td>
            </tr>
        '''.format(td_style, idx, cb, total_rt)
    
    task_rt_data_template += data_rows
    
    task_rt_data_template += '''
            <tr>
                <td {0} colspan="2"><strong>Total</strong></td>
                <td {0}><strong>{1}</strong></td>
            </tr>
            </tbody>
        </table>
        <br><br>
    '''.format(td_style, total_rt_overall)
    
    
    combined_data = '''
    <html>
    <body>
    '''
    
    combined_data += open_issues_data_template + open_meetings_data_template + task_rt_data_template
    
    combined_data += '''
    </body>
    </html>
    '''
    
    frappe.sendmail(
            recipients=['abdulla.pi@groupteampro.com','dineshbabu.k@groupteampro.com'],
            subject='Task-Issue-Meeting - {}'.format(current_date),
            message=combined_data
        )

import frappe
import openpyxl
from openpyxl.styles import PatternFill
from frappe.utils import nowdate
from io import BytesIO

@frappe.whitelist()
def sales_invoice_follow_up_test():
    def send_sales_report_with_table():
        filename = "Sales_Invoice_Follow_Up_" + nowdate() + ".xlsx"
        xlsx_file = build_xlsx_response_sales(filename)
        html_table, total_count = sales_next_action()
        send_mail_with_attachment_and_html(filename, xlsx_file, html_table)

    def build_xlsx_response_sales(filename):
        return make_xlsx_sales(filename)

    def make_xlsx_sales(filename, sheet_name=None, wb=None, column_widths=None):
        import openpyxl
        from openpyxl.styles import PatternFill
        from io import BytesIO

        if wb is None:
            wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = sheet_name or filename
        default_column_widths = [15, 25, 25, 15, 25, 20]
        column_widths = column_widths or default_column_widths
        for i, width in enumerate(column_widths, start=1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
        
        header_fill = PatternFill(start_color="87CEFA", end_color="87CEFA", fill_type="solid")
        headers = ["ID", "Account Manager", "Service", "Customer Name", "Company", "Date", "Grand Total", "Outstanding Amount", "Age"]
        ws.append(headers)
        for cell in ws[1]:
            cell.fill = header_fill

        sales_invoice = frappe.get_list("Sales Invoice", filters={"status": ["not in", ["Return", "Credit Note Issued", "Paid", "Cancelled"]]}, fields=["name", "company", "customer", "services", "posting_date", "due_date", "grand_total", "outstanding_amount", "account_manager", "delivery_manager"])

        service_summary = {}
        total_outstanding = 0

        for order in sales_invoice:
            todate = date.today()
            grand_total = round(order.grand_total, 2)
            outstanding_amount = round(order.outstanding_amount, 2)
            total_outstanding += outstanding_amount
            postingdate1 =(order.posting_date)
            age = (todate - postingdate1).days

            ws.append([
                order.name, order.account_manager, order.services, order.customer, order.company,
                order.posting_date.strftime("%d-%m-%Y"), grand_total, outstanding_amount, age
            ])

            if order.services not in service_summary:
                service_summary[order.services] = {"grand_total": 0, "outstanding": 0}
            service_summary[order.services]["grand_total"] += grand_total
            service_summary[order.services]["outstanding"] += outstanding_amount

        
        ws.append([""] * 6 + ["Total", round(total_outstanding, 2)])

        with BytesIO() as b:
            wb.save(b)
            b.seek(0)
            return b.read()

    def sales_next_action():
        sales_invoice = frappe.get_list("Sales Invoice", filters={"status": ["not in", ["Return", "Credit Note Issued", "Paid", "Cancelled"]]}, fields=["name", "company", "customer", "services", "posting_date", "due_date", "grand_total", "outstanding_amount", "account_manager", "delivery_manager"])

        service_summary = {}
        detailed_rows = []

        for order in sales_invoice:
            grand_total = round(order.grand_total, 2)
            outstanding_amount = round(order.outstanding_amount, 2)

            if order.services not in service_summary:
                service_summary[order.services] = {"grand_total": 0, "outstanding": 0}
            service_summary[order.services]["grand_total"] += grand_total
            service_summary[order.services]["outstanding"] += outstanding_amount

            transaction_date = (order.posting_date.strftime("%d-%m-%Y"))
            todate = date.today()
            age = (todate - order.posting_date).days
            
            detailed_rows.append('<tr style="font-size:14px"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td style="text-align:left;">{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td></tr>'.format(
                order.name, order.account_manager, order.services, order.customer, order.company,transaction_date, grand_total, outstanding_amount, age))

        summary_table = '<table border=1><tr style="text-align: center"><td style="background-color:#063970;color:white">Services</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding</td></tr>'
        grand_total_amount = 0
        total_outstanding = 0

        for service, amounts in service_summary.items():
            summary_table += '<tr style="font-size:14px"><td>{}</td><td style="text-align:right;">{}</td><td style="text-align:right;">{}</td></tr>'.format(service, round(amounts["grand_total"], 2), round(amounts["outstanding"], 2))
            grand_total_amount += amounts["grand_total"]
            total_outstanding += amounts["outstanding"]

        summary_table += '<tr><td></td><td style="text-align:center;" colspan=1>Total</td><td style="text-align:right;">{}</td></tr>'.format(round(total_outstanding, 2))
        summary_table += '</table>'
        
        details_table = '<table border=1><tr style="text-align: center"><td style="background-color:#063970;color:white">ID</td><td style="background-color:#063970;color:white">Account Manager</td><td style="background-color:#063970;color:white">Service</td><td style="background-color:#063970;color:white">Customer Name</td><td style="background-color:#063970;color:white">Company</td><td style="background-color:#063970;color:white">Date</td><td style="background-color:#063970;color:white">Grand Total</td><td style="background-color:#063970;color:white">Outstanding Amount</td><td style="background-color:#063970;color:white">Age</td></tr>'
        details_table += ''.join(detailed_rows)
        details_table += '<tr><td colspan=6></td><td style="text-align:center;">Total</td><td style="text-align:right;">{}</td></tr>'.format(round(total_outstanding, 2))
        details_table += '</table>'
        
        total_count = len(sales_invoice)
        return summary_table + details_table, total_count

    def send_mail_with_attachment_and_html(filename, file_content, html_content):
        attachments = [{"fname": filename, "fcontent": file_content}]
        frappe.sendmail(
            recipients='dineshbabu.k@groupteampro.com',
            cc=["accounts@groupteampro.com","sangeetha.s@groupteampro.com","sangeetha.a@groupteampro.com","annie.m@groupteampro.com","amirtham.g@groupteampro.com"],
            subject='Collection Follow Up-Sales Invoice Report',
            message="""
            <br>
            <p>Collection Outstanding Report For Further Action.</p>
            REC   : AS/AM<br><br>
            IT-SW : DKB/APP<br><br>
            TFP   : SBMK/AM<br><br>
            BCS   : SBMK<br><br>
            TGT   : SBMK<br><br>
            <br>
            {0}
            <br><br>
            Thanks & Regards,<br>TEAMPRO<br>"This email has been automatically generated. Please do not reply"<br><br>"Initiate further action and intimate a direct manager through email."
            """.format(html_content),
            attachments=attachments,
        )

    send_sales_report_with_table()

# Daily Transaction Report For New Correction
@frappe.whitelist()
def statement_of_account_test_1():
    data = """
    <style>
        .responsive-table {
            width: 100%;
            border-collapse: collapse;
        }
        .responsive-table th, .responsive-table td {
            padding: 8px;
            text-align: center;
        }
        .responsive-table th {
            background-color: #063970;
            color: white;
        }
        .responsive-table td.account {
            text-align: left;
        }
        .company-header {
            text-align: center;
            font-weight: bold;
        }
        @media (max-width: 600px) {
            .responsive-table thead {
                display: none;
            }
            .responsive-table, .responsive-table tbody, .responsive-table tr, .responsive-table td {
                display: block;
                width: 100%;
            }
            .responsive-table tr {
                margin-bottom: 15px;
            }
            .responsive-table td {
                text-align: right;
                padding-left: 50%;
                position: relative;
            }
            .responsive-table td::before {
                content: attr(data-label);
                position: absolute;
                left: 0;
                width: 50%;
                padding-left: 15px;
                text-align: left;
                font-weight: bold;
            }
        }
    </style>
    """
    company_order = [
        'TEAMPRO HR & IT Services Pvt. Ltd.',
        'TEAMPRO General Trading Pvt. Ltd.',
        'TEAMPRO General Trading',
        'TEAMPRO Food Products'
    ]

    company = frappe.db.get_all('Company', {'name': ('Not in', ['TEAMPRO Saudi Arabia'])}, ['*'])
    company_dict = {c.name: c for c in company}

    for company_name in company_order:
        j = company_dict.get(company_name)
        if not j:
            continue

        accounts = []

        if j.name == 'TEAMPRO HR & IT Services Pvt. Ltd.':
            accounts = ['50200054611436 - HDFC - THIS', '777705160983 - ICICI Bank - THIS', 'Cash - THIS']
        elif j.name == 'TEAMPRO General Trading Pvt. Ltd.':
            accounts = ['777705755022 - ICICI Bank - TGTP', 'Cash - TGTP']
        elif j.name == 'TEAMPRO General Trading':
            accounts = ['50200050787897 - HDFC Account - TGT', 'Cash - TGT']
        elif j.name == 'TEAMPRO Food Products':
            accounts = ['50200059117831 - HDFC Bank - TFP', 'Cash - TFP']

        data += f"<br><table class='responsive-table' border=1 style='margin:2px;'><tr class='company-header' style='text-align:center;font-size:10px;background-color:#063970;color:#FFFFFF;'><td width='100%'><b>{j.name}</b></td></tr></table>"
        data += "<table class='responsive-table' border=1 style='margin:2px;'><thead><tr style='font-size:10px;background-color:#063970;color:#FFFFFF;'><th width='10%'><b>Posting Date</b></th><th width='10%'><b>Voucher Type</b></th><th width='10%'><b>Voucher No</b></th><th width='30%'><b>Against Account</b></th><th width='10%'><b>Debit (INR)</b></th><th width='10%'><b>Credit (INR)</b></th><th width='10%'><b>Balance (INR)</b></th></tr></thead><tbody>"

        today_date = frappe.utils.now_datetime().date()

        for a in accounts:
            data += f'<tr style="font-size:10px"><td class="account" colspan=7><b>{a}</b></td></tr>'

            gl_entry = frappe.db.sql("""
                select voucher_type, voucher_no, posting_date, sum(debit) as debit, sum(credit) as credit, account, against
                from `tabGL Entry`
                where account=%s and posting_date=%s and is_cancelled = 0 and company=%s
                group by voucher_type, voucher_no, posting_date, account, against
                order by posting_date
            """, (a, today_date, j.name), as_dict=True)

            gle = frappe.db.sql("""
                select sum(debit) as opening_debit, sum(credit) as opening_credit
                from `tabGL Entry`
                where account=%s and posting_date < %s and is_cancelled = 0 and company=%s
            """, (a, today_date, j.name), as_dict=True)

            opening_balance = round((gle[0].opening_debit or 0) - (gle[0].opening_credit or 0), 2)
            data += f'<tr style="font-size:10px"><td colspan=6 style="text-align:right" data-label="Opening Balance"><b>Opening Balance</b></td><td style="text-align:right" data-label="Opening Balance"><b>{opening_balance}</b></td></tr>'

            balance = opening_balance
            total_debit = 0
            total_credit = 0

            for entry in gl_entry:
                posting_date = entry.posting_date.strftime("%d-%m-%Y") if entry.posting_date else "-"
                debit = round(entry.debit or 0, 2)
                credit = round(entry.credit or 0, 2)
                balance += debit - credit

                data += f'<tr style="font-size:10px"><td data-label="Posting Date">{posting_date}</td><td data-label="Voucher Type">{entry.voucher_type or "-"}</td><td data-label="Voucher No">{entry.voucher_no or "-"}</td><td data-label="Against Account">{entry.against or "-"}</td><td style="text-align:right" data-label="Debit (INR)">{debit}</td><td style="text-align:right" data-label="Credit (INR)">{credit}</td><td style="text-align:right" data-label="Balance (INR)">{round(balance, 2)}</td></tr>'

                total_debit += debit
                total_credit += credit

            total_balance = round(balance, 2)
            data += f'<tr style="font-size:10px"><td colspan=4 style="text-align:right" data-label="Total"><b>Total</b></td><td style="text-align:right" data-label="Total Debit"><b>{round(total_debit, 2)}</b></td><td style="text-align:right" data-label="Total Credit"><b>{round(total_credit, 2)}</b></td><td></td></tr>'
            data += f'<tr style="font-size:10px"><td colspan=6 style="text-align:right" data-label="Closing Balance"><b>Closing Balance</b></td><td style="text-align:right" data-label="Closing Balance"><b>{total_balance}</b></td></tr>'

        data += '</tbody></table><br><br>'


    frappe.sendmail(
        recipients=['dineshbabu.k@groupteampro.com'],
        cc=['sangeetha.a@groupteampro.com', 'sangeetha.s@groupteampro.com', 'accounts@groupteampro.com'],
        subject='Daily Transaction Report',
        message=f"""
            Dear Sir,<br>
            <p>Please find the enclosed details for your reference. Kindly check the Daily Transaction Report</p>
            {data}
            "This email has been automatically generated. PLEASE DONOT REPLY, Initiate further action and intimate your direct manager through email."
            <br><br>
            "With Best Wishes & Regards "
            <br><br>
            <span style="color:#203ed5;">
            "TEN – Auto Mail "
            </span>
            <br><br>
            <span style="color:#203ed5;">
                "Disclaimers:<br>
                This email and any files transmitted with it are confidential and intended solely for the use of the individual or entity to whom they are addressed. If you have received this email in error please notify the system manager. Please note that any views or opinions presented in this email are solely those of the author and do not necessarily represent those of the company. Finally, the recipient should check this email and any attachments for the presence of viruses. The company accepts no liability for any damage caused by any virus transmitted by this email."
            </span>
        """
    )

@frappe.whitelist()
def cases_with_to_be_billed_status():
    cases = frappe.get_all("Case", {"case_status": "To be Billed"}, ['*'])

    if cases:
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '<tr style="background-color: #009dd1;"><td width=5% >S.No</td><td width=15% >Batch</td><td width=15% >Case ID</td><td width=10% >Customer</td><td width=10% >Employee Name</td><td width=10% >Employee Code</td></tr>'
        ind = 0
        for c in cases:	
            ind += 1
            data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                ind, c.batch, c.name, c.customer, c.case_name,c.client_employee_code)

        data += '</table>'
        if ind>0:
            formatted_date = frappe.utils.format_datetime(frappe.utils.nowdate(), "dd-MMM-yyyy")
            frappe.sendmail(
                recipients=['sangeetha.s@groupteampro.com',c.allocated_to_batch_manager,"sangeetha.a@groupteampro.com"],  
                subject=_("Cases in To be Billed- Date: %s" % ( formatted_date)),
                message="""
                    Dear Sir/Madam,<br>Kindly Find the below List of Cases that are in "To be Billed" Status %s<br>
                    Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
                """ % (data)
            )


@frappe.whitelist()
def cases_with_generate_report_status():
    cases = frappe.get_all("Case", {"case_status": "Generate Report"}, ['*'])

    if cases:
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '<tr style="background-color: #009dd1;"><td width=5% >S.No</td><td width=15% >Batch</td><td width=15% >Case ID</td><td width=10% >Customer</td><td width=10% >Employee Name</td><td width=10% >Employee Code</td></tr>'
        ind = 0
        for c in cases:	
            ind += 1
            data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                ind, c.batch, c.name, c.customer, c.case_name,c.client_employee_code)

        data += '</table>'
        if ind>0:
            formatted_date = frappe.utils.format_datetime(frappe.utils.nowdate(), "dd-MMM-yyyy")
            frappe.sendmail(
                recipients=['sangeetha.s@groupteampro.com',c.allocated_to_batch_manager,"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],  
                subject=_("Cases in Generate Report- Date: %s" % ( formatted_date)),
                message="""
                    Dear Sir/Madam,<br>Kindly Find the below List of Cases that are in "Generate Report" Status %s<br>
                    Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
                """ % (data)
            )

@frappe.whitelist()
def insuff_consolidated_mail():
    user = frappe.get_all("User", filters={"role": "BCS User"},  fields=["*"])
    for u in user:
        ind=0
        table = '<table  text-align: center; border="1" width="100%" style="border-collapse: collapse;"><tr><td style="width: 15%; font-weight: bold;">ID</td><td style="width: 15%; font-weight: bold;">Batch</td><td style="width: 15%; font-weight: bold;">Employee Name</td><td style="width: 10%; font-weight: bold;">Employee Code</td><td style="width: 20%; font-weight: bold;">Client</td><td style="width: 10%; font-weight: bold;">Case ID</td><td style="width: 10%; font-weight: bold;">Check Type</td><td style="width: 10%; font-weight: bold;">Check ID</td><td style="width: 10%; font-weight: bold;">Check Status</td><td style="width: 10%; font-weight: bold;">Actual Age</td><td style="width: 20%; font-weight: bold;">Allocated To</td></tr> '
        list = ["Education Checks","Family","Reference Check","Court","Social Media","Criminal","Employment","Identity Aadhar","Address Check"]
        for i in list:
            doc=frappe.get_all(i,{"allocated_to":u.name},['*'],order_by='actual_tat DESC')
            for j in doc:
                if j.clear_insufficiency:
                    if j.clear_insufficiency.strftime('%Y-%m-%d') == today():

                        ind+=1
                        if i == "Address Check":
                            table += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (j.name, j.batch,j.name1,j.client_employee_code,j.client,j.case_id,i,j.name,j.check_status,j.actual_tat, u.name)
                        else:
                            table += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (j.name, j.batch,j.name1,j.client_employee_code,j.customer,j.case_id,i,j.name,j.check_status,j.actual_tat, u.name)
        table += '</table>'
        if ind>0:
            frappe.sendmail(
                recipients=['sangeetha.s@groupteampro.com',u.name,"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],
                subject=_("Insuff Cleared-%s"%(nowdate()) ),
                message="""
                    Dear Sir/Madam,<br>Kindly Find the below attached List of Insuff Cleared Checks, %s<br>
                    Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
                    """%(table)
            )
    return "ok"

@frappe.whitelist()
def cases_with_gr_daily_report():
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '<tr style="background-color: #009dd1;"><td width=5% >S.No</td><td width=70% >Customer</td><td width=25% >Generate Report Count</td></tr>'
    customers_with_cases = frappe.get_all("Case", {
        "case_status": 'Generate Report'
    }, ["customer"], distinct=True, pluck="customer")
    ind = 0
    for customer in customers_with_cases:
        count=0
        ind += 1
        cases = frappe.get_all("Case", {
            "customer": customer,
            "case_status": 'Generate Report'
        }, ['*'])
        if cases:
            for c in cases:
                count+=1			
        data += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                ind, customer, count)
    data += '</table>'	
    formatted_date = frappe.utils.format_datetime(frappe.utils.nowdate(), "dd-MMM-yyyy")
    frappe.sendmail(
        recipients=['sangeetha.s@groupteampro.com',"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],  
        subject=_("Customer-Wise Generate Report Count - %s" % (formatted_date)),
        message="""
            Dear Sir/Madam,<br>Kindly Find the below attached Customer-Wise Generate Report Count %s<br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
        """ % (data)
    )

from datetime import datetime, timedelta
from frappe.utils import add_days
from frappe import _
from datetime import datetime, timedelta

@frappe.whitelist()
def submitted_bg_entry():
    data = '<table  text-align: center; border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    data += '<tr style="font-weight: bold;background-color: #009dd1;"><td width=15%>ID</td><td width=25%>Name</td><td width=15%>DOB</td><td width=25%>Case Type</td><td width=25%>Status</td><td width=25%>Submitted Date</td><td width=25%>Submitted Time</td></tr>'
    today = datetime.now().date()
    prev_date = today - timedelta(days=1)
    start_time = datetime.combine(prev_date, datetime.min.time()) + timedelta(hours=18) 
    end_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=18)   
    saved = frappe.db.sql("""
        SELECT * 
        FROM `tabBG Entry Form` 
        WHERE modified BETWEEN %s AND %s and docstatus = 1 order by experience DESC
    """, (start_time, end_time), as_dict=True)
    ind=0
    print(saved)
    for i in saved:
        print("hi")
        ind+=1
        modified_date = i.modified.date()
        modified_time = i.modified.strftime("%H:%M:%S")
        data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Submitted</td><td>%s</td><td>%s</td></tr>' % (i.name,i.employee_name,i.date_of_birth, i.experience, modified_date,modified_time)
    data += '</table>'
    if ind >= 1:   
        frappe.sendmail(
            recipients=['sangeetha.s@groupteampro.com','hrops@kblservices.in',"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],
            subject=_("KBL New Cases"),
            message="""
                Dear Sir/Madam,<br>
                Kindly Find the below attached KBL New Cases  %s<br>
                Thanks & Regards,<br>
                TEAM ERP<br>
                "This email has been automatically generated. Please do not reply"
            """ % data
        )
    else:
        frappe.sendmail(
            recipients=['sangeetha.s@groupteampro.com','hrops@kblservices.in',"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],
            subject=_("KBL New Cases"),
            message="""
                Dear Sir/Madam,<br>
                No New Cases has been Submitted today  %s<br>
                Thanks & Regards,<br>
                TEAM ERP<br>
                "This email has been automatically generated. Please do not reply"
            """ % today
        )

@frappe.whitelist()
def dsr_mail():
    # current_date = datetime.now().date()
    # previous_day = current_date - timedelta(days=1)
    user = frappe.get_all("User", filters={"role": "BCS User",'enabled':1},  fields=["*"])
    # user = frappe.get_all("User",{"roles":"BCS User"},["*"])
    table = '<table  text-align: center; border="1" width="100%" style="border-collapse: collapse;"><tr><td style="width: 40%; font-weight: bold;">Executive</td><td style="width: 20%; font-weight: bold;">Total Allocated To</td><td style="width: 20%; font-weight: bold;">Completed by Today</td><td style="width: 20%; font-weight: bold;">Total Pending</td></tr> '
    for u in user:
        total_tasks = 0
        pending_tasks = 0
        completed_today = 0
        case=frappe.get_all("Case",{"case_status":("in",['Draft',"Entry Completed"]),"allocated_to":u.name},["*"])
        for c in case:
            total_tasks += 1
            pending_tasks += 1
            if c.date_of_entry_completion.date() == frappe.utils.nowdate():
                completed_today += 1
        list = ["Education Checks","Family","Reference Check","Court","Social Media","Criminal","Employment","Identity Aadhar","Address Check"]
        for i in list:
            doc=frappe.get_all(i,{"allocated_to":u.name},['*'])
            for j in doc:
                if j.check_status in ["Draft","Execution Pending"]:
                    total_tasks += 1
                    pending_tasks += 1
                    # table += '<td></td><td>{}</td><td></td><td>{}</td>'.format(total_tasks, pending_tasks)
                if str(j.date_of_entry_completion) == frappe.utils.nowdate() and j.entered_by == u.name:
                    # if j.date_of_entry_completion == nowdate():
                    # if j.date_of_entry_completion == frappe.utils.add_days(frappe.utils.nowdate(),-1):
                    completed_today += 1
                    total_tasks += 1
                        # table += '<td></td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(total_tasks, completed_today, pending_tasks)
                if str(j.date_of_execution_completion) == frappe.utils.nowdate() and j.execution_by == u.name:
                    # if j.date_of_execution_completion == nowdate():
                    # if j.date_of_execution_completion == frappe.utils.add_days(frappe.utils.nowdate(),-1):
                    completed_today += 1
                    total_tasks += 1
                        # table += '<td></td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(total_tasks, completed_today, pending_tasks)
        table += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (u.name, total_tasks, completed_today, pending_tasks)
    table += '</table>'
    frappe.sendmail(
        recipients=['sangeetha.s@groupteampro.com',"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],
        subject=_("DSR-%s"%(nowdate()) ),
        message="""
            Dear Sir/Madam,<br>Kindly Find the below attached DSR - %s<br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
            """%(table)
    )
    return "ok"   


@frappe.whitelist()
def cases_with_insuff_daily_report():
    customers_with_cases = frappe.get_all("Case", {
        "case_status": ("in", ['Execution-Insuff', 'Entry-Insuff'])
    }, ["customer"], distinct=True, pluck="customer")

    for customer in customers_with_cases:
        cases = frappe.get_all("Case", {
            "customer": customer,
            "case_status": ("in", ['Execution-Insuff', 'Entry-Insuff'])
        }, ['*'])

        if cases:
            cust_mail=''
            batch=''
            cs=''
            data = '<table border="1" width="100%" style="border-collapse: collapse;">'
            data += '<tr style="background-color: #009dd1;"><td width=5% >S.No</td><td width=10% >Insuff Reported On</td><td width=15% >Batch</td><td width=15% >Case ID</td><td width=10% >Customer</td><td width=10% >Employee Name</td><td width=10% >Employee Code</td><td width=10% >Check Type</td><td width=10% >ID</td><td width=15% >Insuff Reported By</td><td width=20% >Remarks</td></tr>'
            ind = 0
            check_types = ["Education Checks", "Family", "Reference Check", "Court", "Social Media", "Criminal", "Employment", "Identity Aadhar", "Address Check"]
            for c in cases:
                batch = c.batch
                cs=c.name
                cust_mail=frappe.db.get_value("Batch",{"name":c.batch},['customer_mail_ids'])
                for check_type in check_types:
                    doc = frappe.get_all(check_type, {
                        "case_id": c.name,
                        "check_status": "Insufficient Data",
                        "insufficiency_date": frappe.utils.nowdate()
                    }, ["name", "workflow_state", "custom_insufficiency_reported_by", "insufficiency_date", "case_id", "batch", 'insufficient_remarks'])

                    for j in doc:
                        ind += 1
                        data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                            ind, j.insufficiency_date or '', j.batch, j.case_id, c.customer, c.case_name,c.client_employee_code, check_type, j.name, j.custom_insufficiency_reported_by or '',  j.insufficient_remarks)

            data += '</table>'
            if ind>0:
                formatted_date = frappe.utils.format_datetime(frappe.utils.nowdate(), "dd-MMM-yyyy")
                frappe.sendmail(
                    # recipients=[cust_mail],
                    # recipients=["giftyannie6@gmail.com"],
                    recipients=['sangeetha.s@groupteampro.com',"sangeetha.a@groupteampro.com","keerthana.b@groupteampro.com"],  
                    subject=_("Insufficiency Report - Customer: %s - Date: %s" % (customer, formatted_date)),
                    message="""
                        Dear Sir/Madam,<br>Kindly Find the below List of Cases that are Reported as Insuff on Today for Customer %s %s<br>
                        Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
                    """ % (customer, data)
                )


import frappe
from frappe.utils import formatdate

@frappe.whitelist()
def cases_with_insuff():
    cases = frappe.get_all(
        "Case",
        filters={"case_status": ("in", ['Execution-Insuff', 'Entry-Insuff'])},
        fields=['*'],
        order_by='insufficiency_reported ASC'
    )
    

    data = '''
    <table border="1" width="100%" style="border-collapse: collapse; text-align: center;">
        <thead style="background-color: #0f1568; color: white;">
            <tr>
                <th width="5%">S.No</th>
                <th width="10%">Insuff Reported On</th>
                <th width="15%">Batch</th>
                <th width="15%">Case ID</th>
                <th width="25%">Customer</th>
                <th width="20%">Employee Name</th>
                <th width="10%">Employee Code</th>
                <th width="10%">Case Status</th>
                <th width="50%">Insuff Check(s)</th>
                <th width="5%">Age of Insufficiency</th>
            </tr>
        </thead>
        <tbody>
    '''
    
    i = 1
    for c in cases:
        check_types = ["Education Checks", "Family", "Reference Check", "Court", "Social Media", "Criminal", "Employment", "Identity Aadhar", "Address Check"]
        checks = []
        
        for check_type in check_types:
            docs = frappe.get_all(
                check_type,
                filters={"case_id": c.name, "check_status": "Insufficient Data"},
                fields=["name"]
            )
            checks.extend([doc.name for doc in docs])
        
        checks_str = ", ".join(checks)
        insuff_reported = formatdate(c.insufficiency_reported) if c.insufficiency_reported else ''
        
        data += f'''
        <tr>
            <td>{i}</td>
            <td>{insuff_reported}</td>
            <td>{c.batch}</td>
            <td>{c.name}</td>
            <td>{c.customer}</td>
            <td>{c.case_name}</td>
            <td>{c.client_employee_code or "-"}</td>
            <td>{c.case_status}</td>
            <td>{checks_str}</td>
            <td>{c.insufficiency_days or "-"}</td>
        </tr>
        '''
        i += 1
    
    
    data += '''
        </tbody>
    </table>
    '''
    
    frappe.sendmail(
        # recipients=['divya.p@groupteampro.com'],
        # recipients="siva.m@groupteampro.com",
        recipients=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','sangeetha.a@groupteampro.com',"keerthana.b@groupteampro.com"],
        cc=[''],
        subject=_("Cases with Insuff"),
        message=f"""
            Dear Madam,<br>Kindly find the below list of cases that are in Insuff status:<br>{data}<br><br>
            Thanks & Regards,<br>TEAMPRO<br>"This email has been automatically generated. Please do not reply"<br><br>"initiate further action and intimate a direct manager through email."
        """
    )
    print(i)

@frappe.whitelist()
def cases_beyond_tat_age_10():
    cases = frappe.get_all("Case", {"batch_age": (">=", 10), "case_status": ("not in", ['Case Report Completed', 'Case Completed', 'Drop','Execution-Insuff','Entry-Insuff','To be Billed','Generate Report','SO Created'])},['*'],order_by='batch_age DESC')
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '<tr style="background-color: #009dd1;"><td width=5% >S.No</td><td width=15% >Batch</td><td width=15% >Case ID</td><td width=25% >Customer</td><td width=20% >Employee Name</td><td width=10% >TAT Age</td><td width=10% >Case Status</td></tr>'
    i=1
    for c in cases:
        data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(i, c.batch, c.name, c.customer, c.case_name, c.batch_age, c.case_status)
        i+=1
    data += '</table>'
    frappe.sendmail(
        recipients=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','sangeetha.a@groupteampro.com',"keerthana.b@groupteampro.com"],
        cc=[''],
        subject=_("Cases having TAT Age 10 and above"),
        message="""
            Dear Sir/Madam,<br>Kindly Find the below List of Cases that are having TAT Age 10 and above %s<br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
            """%(data)
    )
    print(i)

import frappe
from frappe.utils import nowdate, today
import openpyxl
from io import BytesIO
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def candidate_excel_format():
    next_date=today()
    next_dates=datetime.strptime(next_date, '%Y-%m-%d')
    formatted_next_date=next_dates.strftime('%Y-%m-%d')
    filename = "Candidate_Details_" + today() + ".xlsx"
    pdffilename = "Candidate_Details_" + today() + ".pdf"
    candidates = frappe.get_all(
        "Candidate",
        filters={'submitted_date': formatted_next_date},
        fields=["candidate_created_by"],
        group_by='candidate_created_by'
    )

    for user in candidates:
        user_id = user.candidate_created_by
        xlsx_file = make_xlsx_candidate(filename, user_id)
        pdf_content = make_pdf_candidate(pdffilename, user_id)
        candidate_status_mail_test(filename, xlsx_file.getvalue(), pdffilename, pdf_content, user_id)

def candidate_status_mail_test(filename, file_content, pdffilename, pdf_content, user_id):
    next_date=today()
    next_dates=datetime.strptime(next_date, '%Y-%m-%d')
    formatted_next_date=next_dates.strftime('%Y-%m-%d')
    data=""
    s_no = 0
    candidates = frappe.db.sql(
        """
        SELECT c.name, c.passport_number, c.given_name, c.highest_degree,
               c.total_experience, c.overseas_experience, c.current_employer,
               c.current_ctc, c.expected_ctc, c.location, c.notice_period_months,
               c.remarks_1, c.position, c.currency_ctc
        FROM `tabCandidate` c
        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by = %s
        AND cs.status = %s
        AND DATE(cs.sourced_date) = %s
        """,
        (user_id, "Pending QC", formatted_next_date),
        as_dict=True
    )

    grouped_candidates = {}
    for candidate in candidates:
        position = candidate.get("position", "")
        currency = candidate.get("currency_ctc", "")  # Default to SAR
        current_ctc = candidate.get("current_ctc", 0)  # Default to 0
        formatted_ctc = f"{currency} {current_ctc}" if current_ctc else " "

        if position not in grouped_candidates:
            grouped_candidates[position] = []
        grouped_candidates[position].append([
            candidate.get("name", "-"),
            candidate.get("passport_number", "-"),
            candidate.get("given_name", "-"),
            candidate.get("highest_degree", "-"),
            candidate.get("total_experience", "-"),
            candidate.get("overseas_experience", "-"),
            candidate.get("current_employer", "-"),
            formatted_ctc,
            candidate.get("expected_ctc", "-"),
            candidate.get("location", "-"),
            candidate.get("notice_period_months", "-"),
            candidate.get("remarks_1", "-"),
        ])

    # Define headers for the table
    headers = [
        "Candidate ID", "PP Number", "Candidate Name", "Qualification", 
        "Total Yrs of Exp", "Overseas Exp", "Current Employer", 
        "Current Salary", "Exp. Salary", "Current Location", 
        "Notice Period", "Remarks"
    ]

    for position, candidates in grouped_candidates.items():
        # Add position header and start table
        data += f"""
        <table class='table table-bordered' style='border: 1px solid black; border-collapse: collapse; width: 100%;'>
        <tr style='border: 1px solid black; background-color: #0f1568; color: white;'>
        <th colspan="12" style="text-align: center; font-size: 18px;">Position: {position}</th>
        </tr>
        <tr style='border: 1px solid black; background-color: #98D7F5; color: black;'>
        """
        # Add headers to the table
        for header in headers:
            data += f"<th style='border: 1px solid black;'>{header}</th>"
        data += "</tr>"

        # Add rows for each candidate under the position
        for candidate in candidates:
            data += "<tr style='border: 1px solid black;'>"
            for value in candidate:
                data += f"<td style='border: 1px solid black;'>{value}</td>"
            data += "</tr>"
        data += "</table><br>"

    subject = f"Candidates Submitted - {nowdate()}"
    message = f"""
    Dear Sir/Madam,<br><br>
    Kindly find the below list of candidates you submitted today:<br><br>{data if data else ''}<br><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """

    frappe.sendmail(
        recipients=[user_id],
        subject=subject,
        message=message,
        attachments=[
            {"fname": filename, "fcontent": file_content},
            {"fname": pdffilename, "fcontent": pdf_content}
        ]
    )

def make_xlsx_candidate(filename, user_id):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Candidates'
    
    # Define column width
    for col in range(ord('A'), ord('M')):  # Columns A to L
        ws.column_dimensions[chr(col)].width = 20

    # Define headers
    headers = ["Candidate ID", "PP Number", "Candidate Name", "Qualification", 
               "Total Yrs of Exp", "Overseas Exp", "Current Employer", 
               "Current Salary", "Exp. Salary", "Current Location", 
               "Notice Period", "Remarks"]

    # Define border style
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Fetch and group candidates by position
    position_candidates = get_data_grouped_by_position_candidate(user_id)
    
    # Debug: Check if any positions are retrieved
    print(f"Positions found: {len(position_candidates)}")
    
    if not position_candidates:
        print("No candidates found for the given user.")
    
    for position, candidates in position_candidates.items():
        # Add position row
        position_row = ws.max_row + 1
        ws.merge_cells(start_row=position_row, start_column=1, end_row=position_row, end_column=12)
        cell = ws.cell(row=position_row, column=1)
        cell.value = f"{position}"
        cell.fill = PatternFill(start_color="0F1568", end_color="0F1568", fill_type="solid")
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")

        # Add headers
        header_row = ws.max_row + 1
        for col_num, header in enumerate(headers, start=1):
            cell = ws.cell(row=header_row, column=col_num)
            cell.value = header
            cell.fill = PatternFill(start_color="98D7F5", end_color="98D7F5", fill_type="solid")
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        # Add candidate rows
        for candidate in candidates:
            row_num = ws.max_row + 1
            for col_num, value in enumerate(candidate, start=1):
                cell = ws.cell(row=row_num, column=col_num)
                cell.value = value
                cell.border = thin_border  # Apply border to each cell

        # Add an empty row for separation
        ws.append([])

    # Save the file into a BytesIO stream
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file

from frappe.utils.pdf import get_pdf
def make_pdf_candidate(pdffilename, user_id):
    html = """
    <html>
    <head>
    <style>
    table { width: 100%; border-collapse: collapse; }
    table, th, td { border: 1px solid black; }
    th, td { padding: 5px; text-align: left; }
    th { background-color: #98D7F5; color: black; }  /* Header background color */
    td.position { background-color: #0F1568; color: white; } /* Position row background color */
    </style>
    </head>
    <body>
    <h2>Candidate Details</h2>
    """
    
    next_date = today()
    next_dates = datetime.strptime(next_date, '%Y-%m-%d')
    formatted_next_date = next_dates.strftime('%Y-%m-%d')
    
    candidates = frappe.db.sql(
        """
        SELECT c.name, c.passport_number, c.given_name, c.highest_degree,
               c.total_experience, c.overseas_experience, c.current_employer,
               c.current_ctc, c.expected_ctc, c.location, c.notice_period_months,
               c.remarks_1, c.position, c.currency_ctc
        FROM `tabCandidate` c
        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by = %s
        AND cs.status = %s
        AND DATE(cs.sourced_date) = %s
        """,
        (user_id, "Pending QC", formatted_next_date),
        as_dict=True
    )

    # Group candidates by position
    grouped_candidates = {}
    for candidate in candidates:
        position = candidate.get("position", "")
        currency = candidate.get("currency_ctc", "")  # Default to SAR
        current_ctc = candidate.get("current_ctc", 0)  # Default to 0
        formatted_ctc = f"{currency} {current_ctc}" if current_ctc else " "

        if position not in grouped_candidates:
            grouped_candidates[position] = []
        grouped_candidates[position].append([ 
            candidate.get("name", "-"),
            candidate.get("passport_number", "-"),
            candidate.get("given_name", "-"),
            candidate.get("highest_degree", "-"),
            candidate.get("total_experience", "-"),
            candidate.get("overseas_experience", "-"),
            candidate.get("current_employer", "-"),
            formatted_ctc,
            candidate.get("expected_ctc", "-"),
            candidate.get("location", "-"),
            candidate.get("notice_period_months", "-"),
            candidate.get("remarks_1", "-"),
        ])

    # Define table headers
    headers = [
        "Candidate ID", "PP Number", "Candidate Name", "Qualification", 
        "Total Yrs of Exp", "Overseas Exp", "Current Employer", 
        "Current Salary", "Exp. Salary", "Current Location", 
        "Notice Period", "Remarks"
    ]

    # Add data position-wise to the HTML
    for position, candidates in grouped_candidates.items():
        # Add position header with custom color
        html += f"""
        <table>
        <tr>
        <td class="position" colspan="12">{position}</td>
        </tr>
        """
        
        # Add table headers
        html += "<tr>"
        for header in headers:
            html += f"<th>{header}</th>"
        html += "</tr>"

        # Add candidate rows
        for candidate in candidates:
            html += "<tr>"
            for value in candidate:
                html += f"<td>{value}</td>"
            html += "</tr>"
        html += "</table>"

    html += """
    </body>
    </html>
    """

    # Generate PDF from the HTML
    pdf_content = get_pdf(html)
    return pdf_content

def get_data_grouped_by_position_candidate(user_id):
    """
    Fetch candidate data grouped by position using SQL query.
    """
    data = {}
    next_date=today()
    next_dates=datetime.strptime(next_date, '%Y-%m-%d')
    formatted_next_date=next_dates.strftime('%Y-%m-%d')

    # Execute the SQL query to fetch candidates
    candidates = frappe.db.sql(
        """
        SELECT c.name, c.passport_number, c.given_name, c.highest_degree,
               c.total_experience, c.overseas_experience, c.current_employer,
               c.current_ctc, c.expected_ctc, c.location, c.notice_period_months,
               c.remarks_1, c.position, c.currency_ctc
        FROM `tabCandidate` c
        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
        WHERE c.candidate_created_by = %s
        AND cs.status = %s
        AND DATE(cs.sourced_date) = %s
        """,
        (user_id, "Pending QC", formatted_next_date),
        as_dict=True
    )

    # Group candidates by position
    for candidate in candidates:
        position = candidate.get("position", "")
        currency = candidate.get("currency_ctc", "")  # Default to SAR if not specified
        current_ctc = candidate.get("current_ctc", 0)  # Default to 0 if not specified
        formatted_ctc = f"{currency} {current_ctc}" if current_ctc else " "

        if position not in data:
            data[position] = []
        data[position].append([
            candidate.name, candidate.passport_number, candidate.given_name,
            candidate.highest_degree, candidate.total_experience, 
            candidate.overseas_experience, candidate.current_employer,
            formatted_ctc, candidate.expected_ctc, candidate.location, 
            candidate.notice_period_months, candidate.remarks_1
        ])

    return data


#  If the “Next Action Date” is Old date, either LUO or NAD is blank give a mail alert.
from datetime import datetime
import frappe
from frappe.utils import today, getdate

@frappe.whitelist()
def sendmail_luo_nad_alert():
    today_date = getdate()  # This ensures today_date is a date object
    formatted_date = today_date.strftime('%d/%m/%Y')
    
    count = 1
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%'><b>Sr</b></td>
            <td style='width:10%'><b>ID</b></td>
            <td style='width:15%'><b>Passport Number </b></td>
            <td style='width:20%'><b>Given Name/Surname</b></td>
            <td style='width:13%'><b>Status</b></td>
            <td style='width:25%'><b>Customer Name</b></td>
            <td style='width:7%'><b>Position</b></td>
            <td style='width:13%'><b>Next Action</b></td>
            <td style='width:20%'><b>Next Action On</b></td>
            <td style='width:20%'><b>Remarks</b></td>
            <td style='width:20%'><b>Last Updated On</b></td>

        </b></tr>
        '''
        
    closure = frappe.db.get_all("Closure", {"status": ("not in", ["Dropped", "Arrived"])}, ["*"])
    formatted_next_action=''
    formatted_last_action=''
    for i in closure:
        if i.custom_next_follow_up_on:
            formatted_next_action = i.custom_next_follow_up_on.strftime('%d/%m/%Y')
        if i.last_updated_on:
            formatted_last_action=i.last_updated_on.strftime('%d/%m/%Y')
        next_follow_up_date = getdate(i.custom_next_follow_up_on) if i.custom_next_follow_up_on else None
        if next_follow_up_date < today_date or i.last_updated_on is None or next_follow_up_date is None:
            data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.name ,i.passport_no or '-',i.given_name,i.status,i.customer,i.task_subject,i.std_remarks,formatted_next_action or '-',i.remark,formatted_last_action or '-')
            count += 1

    data += '</table>'
    
    frappe.sendmail(
        recipients=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','sangeetha.a@groupteampro.com','dc@groupteampro.com'],
        # recipients='divya.p@groupteampro.com',
        subject=f'Action Required: Closure with Outdated or Missing Follow-Up Details - {formatted_date}',
        message=f"""
        <b>Dear Team,</b><br><br>

        This is a reminder regarding closure records that have outdated or missing follow-up details as of {formatted_date}. 
        Please review the list below and take the necessary action.<br><br>

        {data}<br><br>
        Thanks & Regards,<br>
        TEAM ERP<br><br>

        <i>This email was automatically generated. Please do not reply.</i>
        """
    )

@frappe.whitelist()
def send_closure_mail():
    current_date = datetime.now().strftime("%d-%m-%Y")
    ind=0
    s_no=1
    data = '<table  text-align: center; border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    data += '<tr style="font-weight: bold;background-color: #98d7f5;"><td width=5%>S.No</td><td width=15%>Closure ID</td><td width=25%>Candidate Name</td><td width=15%>Passport Number</td><td width=25%>Customer Name</td><td width=25%>Status</td><td width=35%>Latest Remarks</td></tr>'
    closure=frappe.db.get_all("Closure",{"status":["in",["PSL","Signed Offer Letter","Premedical","PCC","Final Medical","Biometric","Visa Stamping","Emigration"]]},["name","given_name","passport_no","customer","status","remark"])
    for i in closure:
        data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (s_no,i.name,i.given_name,i.passport_no, i.customer, i.status,i.remark)
        ind+=1
        s_no+=1
    data += '</table>'
    subject = "Closure Status Report -  %s" % current_date
    message="""
                Dear Sir/Madam,<br>
                Kindly Find the below attached Closure Status Report  <br>{}<br>
                Thanks & Regards,<br>
                TEAM ERP<br>
                "This email has been automatically generated. Please do not reply"
            """.format(data)
    if ind>0:
        frappe.sendmail(
            # recipients=['divya.p@groupteampro.com'],
            recipients=['sangeetha.s@groupteampro.com','dc@groupteampro.com','sangeetha.a@groupteampro.com','dineshbabu.k@groupteampro.com'],
            subject=subject,
            message=message
        )

@frappe.whitelist() 
def fp_candidate_list_send_mail_to_spoc():
    startdate=nowdate()
    next_day=add_days(startdate,1)
    projects = frappe.get_all("Project", filters={'status': 'Open', 'service': ['in', ['REC-D', 'REC-I']]}, fields=['name', 'spoc'])
    spoc_set = set()
    candidate_count=0
    for project in projects:
        if project.get('spoc'):
            spoc_set.add(project['spoc'])
    spoc_list = list(spoc_set)
    # table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    print(spoc_list)
    for spoc in spoc_list:
        spoc_projects = frappe.get_all("Project", filters={'status': 'Open', 'service': ['in', ['REC-D', 'REC-I']], 'spoc': spoc,'custom_spoc__next_contact_on':next_day}, fields=['*'])
        table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
        for project in spoc_projects:
            tasks = frappe.get_all("Task", filters={'status': ('in', ['Open', 'Working', 'Overdue', 'Pending Review']), 'project': project['name'], 'service': ('in', ['REC-D', 'REC-I'])}, fields=['name'])
            candidate_count = frappe.db.count("Candidate", filters={'project': project['name'], 'pending_for': ('not in', ['IDB', 'Sourced', 'Proposed PSL'])})
            if candidate_count > 0:
                s_no = 0
                row = 0
                table+="""<tr style="text-align: center;"><td style="border-left: none; border-right: none;"colspan=10 %s>%s</td></tr>"""%(row+1,project['project_name'])
                table += '<tr style="background-color: #87CEFA"><td style="width: 15%; font-weight: bold; text-align: center;">S.NO</td><td style="width: 30%; font-weight: bold; text-align: center;">CDID</td><td style="width: 25%; font-weight: bold; text-align: center;">Candidate Status</td><td style="width: 25%; font-weight: bold; text-align: center;">Given Name/Surname</td><td style="width: 30%; font-weight: bold; text-align: center;">Passport No</td><td style="width: 25%; font-weight: bold; text-align: center;">Position</td><td style="width: 30%; font-weight: bold; text-align: center;">Candidate Owner</td><td style="width: 40%; font-weight: bold; text-align: center;">Project ID</td><td style="width: 40%; font-weight: bold; text-align: center;">Customer Name</td><td style="width: 25%; font-weight: bold; text-align: center;">Age</td><td style="width: 30%; font-weight: bold; text-align: center;">Next Contact On</td></tr>'
                for task in tasks:
                    candidates = frappe.get_all("Candidate", filters={'pending_for': ('not in', ['IDB', 'Sourced', 'Proposed PSL']), 'task': task['name']}, fields=['name', 'pending_for', 'given_name','passport_number', 'position', 'candidate_created_by', 'project', 'customer', 'age_of_cv', 'custom_next_contact_on'])
                    for candidate in candidates:
                        row += 1
                        s_no += 1
                        table += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (s_no, candidate['name'], candidate['pending_for'], candidate['given_name'],candidate['passport_number'], candidate['position'], candidate['candidate_created_by'], candidate['project'], candidate['customer'], candidate['age_of_cv'], candidate['custom_next_contact_on'] or '')
        table += '</table>'
        subject = "FP List - %s" % nowdate()
        message = """
        Dear Sir/Madam,<br><br>
        Kindly find the below list of your FP List for Next Contact On<br><br>{}<br><br>
        Thanks & Regards,<br>TEAM ERP<br>
        <i>This email has been automatically generated. Please do not reply</i>
        """.format(table)
        if candidate_count>0:
            frappe.sendmail(
                recipients=[spoc],
                cc=["annie.m@groupteampro.com"],
                subject=subject,
                message=message,
            )

@frappe.whitelist() 
def fp_candidate_to_acc_manager():

    projects = frappe.get_all(
        "Project",
        filters={'status': 'Open', 'service': ['in', ['REC-D', 'REC-I']]},
        fields=['name', 'account_manager']
    )

    spoc_set = set()
    for project in projects:
        if project.get('account_manager'):
            spoc_set.add(project['account_manager'])

    spoc_list = list(spoc_set)

    # frappe.logger().info(spoc_list)

    for spoc in spoc_list:

        spoc_projects = frappe.get_all(
            "Project",
            filters={
                'status': 'Open',
                'service': ['in', ['REC-D', 'REC-I']],
                'account_manager': spoc
            },
            fields=['name', 'project_name']
        )

        table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'

        for project in spoc_projects:

            s_no = 0

            tasks = frappe.get_all(
                "Task",
                filters={
                    'status': ('in', ['Open', 'Working', 'Overdue', 'Pending Review']),
                    'project': project['name'],
                    'service': ('in', ['REC-D', 'REC-I'])
                },
                fields=['name']
            )

            task_names = [t['name'] for t in tasks]

            if not task_names:
                continue

            candidates = frappe.get_all(
                "Candidate",
                filters={
                    'pending_for': ('not in', ['IDB', 'Sourced', 'Proposed PSL']),
                    'task': ('in', task_names)
                },
                fields=[
                    'name', 'pending_for', 'given_name',
                    'passport_number', 'position',
                    'candidate_created_by', 'project',
                    'customer', 'age_of_cv', 'custom_next_contact_on'
                ]
            )

            if not candidates:
                continue
            row = 0

            table += """<tr style="text-align: center;">
                <td style="border-left: none; border-right: none;" colspan=10>%s</td>
            </tr>""" % (project['project_name'])

            table += '''
            <tr style="background-color: #87CEFA">
                <td style="width: 15%; font-weight: bold;">S.NO</td>
                <td style="width: 30%; font-weight: bold;">CDID</td>
                <td style="width: 25%; font-weight: bold;">Candidate Status</td>
                <td style="width: 25%; font-weight: bold;">Given Name/Surname</td>
                <td style="width: 25%; font-weight: bold;">Passport No</td>
                <td style="width: 25%; font-weight: bold;">Position</td>
                <td style="width: 30%; font-weight: bold;">Candidate Owner</td>
                <td style="width: 40%; font-weight: bold;">Project ID</td>
                <td style="width: 40%; font-weight: bold;">Customer Name</td>
                <td style="width: 25%; font-weight: bold;">Age</td>
                <td style="width: 30%; font-weight: bold;">Next Contact On</td>
            </tr>
            '''

            for candidate in candidates:
                row += 1
                s_no += 1

                table += """<tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                </tr>""" % (
                    s_no,
                    candidate['name'],
                    candidate['pending_for'],
                    candidate['given_name'],
                    candidate['passport_number'],
                    candidate['position'],
                    candidate['candidate_created_by'],
                    candidate['project'],
                    candidate['customer'],
                    candidate['age_of_cv'],
                    candidate['custom_next_contact_on'] or ''
                )

        table += '</table>'

        subject = "FP List - %s" % frappe.utils.nowdate()

        message = """
        Dear Sir/Madam,<br><br>
        Kindly find the below list of your FP List:<br><br>{}<br><br>
        Thanks & Regards,<br>TEAM ERP<br>
        <i>This email has been automatically generated. Please do not reply</i>
        """.format(table)

        frappe.sendmail(
            recipients=[spoc],
            cc=["annie.m@groupteampro.com", "cs@groupteampro.com"],
            subject=subject,
            message=message,
        )

@frappe.whitelist()
def fp_candidate_to_spoc():

    projects = frappe.get_all(
        "Project",
        filters={'status': 'Open', 'service': ['in', ['REC-D', 'REC-I']]},
        fields=['name', 'spoc', 'project_name']
    )

    # Group projects by SPOC
    spoc_map = {}
    for p in projects:
        if p.spoc:
            spoc_map.setdefault(p.spoc, []).append(p)

    for spoc, spoc_projects in spoc_map.items():

        table = '<table border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
        has_data = False

        for project in spoc_projects:

            tasks = frappe.get_all(
                "Task",
                filters={
                    'project': project.name,
                    'status': ['in', ['Open', 'Working', 'Overdue', 'Pending Review']],
                    'service': ['in', ['REC-D', 'REC-I']]
                },
                fields=['name']
            )

            task_names = [t.name for t in tasks]

            if not task_names:
                continue

            candidates = frappe.get_all(
                "Candidate",
                filters={
                    'task': ['in', task_names],
                    'pending_for': ['not in', ['IDB', 'Sourced', 'Proposed PSL']]
                },
                fields=[
                    'name', 'pending_for', 'given_name',
                    'passport_number', 'position',
                    'candidate_created_by', 'project',
                    'customer', 'age_of_cv', 'custom_next_contact_on'
                ]
            )

            if not candidates:
                continue

            has_data = True
            table += f"""<tr><td colspan=11><b>{project.project_name}</b></td></tr>"""

            table += '''
            <tr style="background-color: #87CEFA">
                <td>S.NO</td><td>CDID</td><td>Status</td><td>Name</td>
                <td>Passport</td><td>Position</td><td>Owner</td>
                <td>Project</td><td>Customer</td><td>Age</td><td>Next Contact</td>
            </tr>
            '''

            for i, c in enumerate(candidates, 1):
                table += f"""
                <tr>
                    <td>{i}</td>
                    <td>{c.name}</td>
                    <td>{c.pending_for}</td>
                    <td>{c.given_name}</td>
                    <td>{c.passport_number}</td>
                    <td>{c.position}</td>
                    <td>{c.candidate_created_by}</td>
                    <td>{c.project}</td>
                    <td>{c.customer}</td>
                    <td>{c.age_of_cv}</td>
                    <td>{c.custom_next_contact_on or ''}</td>
                </tr>
                """

        table += '</table>'

        if not has_data:
            continue  # skip empty mail

        subject = f"FP List - {frappe.utils.nowdate()}"

        message = f"""
        Dear Sir/Madam,<br><br>
        Kindly find the below list of your FP List:<br><br>
        {table}<br><br>
        Thanks & Regards,<br>TEAM ERP<br>
        <i>This email has been automatically generated. Please do not reply</i>
        """

        recipient_email = "cs@groupteampro.com" if spoc == "tamilarasi.ts@groupteampro.com" else spoc
        # recipient_email = "sivarenisha.m@groupteampro.com" 
        frappe.sendmail(
            recipients=[recipient_email],
            subject=subject,
            message=message,
        )

@frappe.whitelist() 
def fp_candidate_list_send_mails():
    projects=frappe.get_all("Project",{'status':'Open','service':('in',['REC-D','REC-I'])},['*'])
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    for i in projects:
        

        # row=0
        tasks = frappe.get_all("Task", {'status': ('in', ['Open', 'Working','Overdue','Pending Review']),'project':i.name,'service':('in',['REC-D','REC-I'])},['*'])
        # acc_manager=frappe.db.get_value("Task",{'project':i.name},['account_manager'])
        # spoc=frappe.db.get_value("Task",{'project':i.name},['spoc'])
        task_count=frappe.db.count("Task", {'status': ('in', ['Open', 'Working','Overdue','Pending Review']),'project':i.name,'service':('in',['REC-D','REC-I'])})
        candidate_count=frappe.db.count("Candidate", {'project':i.name,'pending_for':('not in',['IDB','Sourced','Proposed PSL'])})
        if candidate_count>0:
            row=0
            s_no=0
            table+="""<tr style="text-align: center;"><td style="border-left: none; border-right: none;"colspan=10 %s>%s</td></tr>"""%(row+1,i.project_name)
            # table += '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
            table += '<tr style="background-color: #87CEFA"><td style="width: 15%; font-weight: bold; text-align: center;">S.NO</td><td style="width: 30%; font-weight: bold; text-align: center;">CDID</td><td style="width: 25%; font-weight: bold; text-align: center;">Candidate Status</td><td style="width: 25%; font-weight: bold; text-align: center;">Given Name/Surname</td><td style="width: 25%; font-weight: bold; text-align: center;">Position</td><td style="width: 30%; font-weight: bold; text-align: center;">Candidate Owner</td><td style="width: 40%; font-weight: bold; text-align: center;">Project ID</td><td style="width: 40%; font-weight: bold; text-align: center;">Customer Name</td><td style="width: 25%; font-weight: bold; text-align: center;">Age</td><td style="width: 30%; font-weight: bold; text-align: center;">Next Contact On</td></tr>'
            for j in tasks:
                
                candidate=frappe.get_all("Candidate",{'pending_for':('not in',['IDB','Sourced','Proposed PSL']),'task':j.name},['name','pending_for','given_name','position','candidate_created_by','project_name','project','customer','age_of_cv','custom_next_contact_on'])
                for ca in candidate:
                    row+=1
                    s_no+=1
                    table+="""<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (s_no,ca.name,ca.pending_for,ca.given_name,ca.position,ca.candidate_created_by,ca.project,ca.customer,ca.age_of_cv,ca.custom_next_contact_on or '')
    table += '</table>'
    subject = "FP List -  %s" % nowdate()
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below list of  your FP List :<br><br>{}<br><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(table)
    # if row>1:
    frappe.sendmail(
        recipients=["sangeetha.s@groupteampro.com"],
        cc=["annie.m@groupteampro.com"],
        # recipients=["riyaz.a@groupteampro.com"],
        subject=subject,
        message=message,
    )
    import frappe
from frappe.utils import today

import frappe
from frappe.utils import today, getdate
from datetime import time

EXCLUDE_EMPLOYEES = {"TI00225", "TI00002", "TI00001"}

def generate_absent_table(data):
    table = """
    <table style="width:100%;border-collapse:collapse;font-family:Calibri,Arial,sans-serif;font-size:13px;">
    <tr style="background:#5B9BD5;color:white;font-weight:bold;">
        <th style="border:1px solid #000;padding:6px;">Sr</th>
        <th style="border:1px solid #000;padding:6px;">Employee Code </th>
        <th style="border:1px solid #000;padding:6px;">Employee Name</th>
        <th style="border:1px solid #000;padding:6px;">Status</th>
         <th style="border:1px solid #000;padding:6px;">Attendance Date</th>
         <th style="border:1px solid #000;padding:6px;">Leave Type</th>
    </tr>
    """
    for i,row in enumerate(data,1):
        color = "#EAF4FF" if i % 2 else "#FFFFFF"
        date_value = row.attendance_date.strftime("%d-%m-%Y") if row.attendance_date else ""
        table += f"""
        <tr style="background:{color};">
            <td style="border:1px solid #000;padding:5px;">{i}</td>
            <td style="border:1px solid #000;padding:5px;">{row.employee or ''}</td>
            <td style="border:1px solid #000;padding:5px;">{row.employee_name or ''}</td>
            <td style="border:1px solid #000;padding:5px;">{row.status or ''}</td>
            <td style="border:1px solid #000;padding:5px;">{date_value}</td>
             <td style="border:1px solid #000;padding:5px;">{row.leave_type or ''}</td>
        </tr>
        """
    table += "</table>"
    return table

def generate_late_table(data):
    table = """
    <table style="width:100%;border-collapse:collapse;font-family:Calibri,Arial,sans-serif;font-size:13px;">
    <tr style="background:#5B9BD5;color:white;font-weight:bold;">
        <th style="border:1px solid #000;padding:6px;">Sr</th>
        <th style="border:1px solid #000;padding:6px;">Employee Code</th>
        <th style="border:1px solid #000;padding:6px;">Employee Name</th>
        <th style="border:1px solid #000;padding:6px;">Status</th>
         <th style="border:1px solid #000;padding:6px;">In Time</th>
        <th style="border:1px solid #000;padding:6px;">Attendance Date</th>
         <th style="border:1px solid #000;padding:6px;">Leave Type</th>
       
    </tr>
    """
    for i,row in enumerate(data,1):
        color = "#EAF4FF" if i % 2 else "#FFFFFF"
        date_value = row.attendance_date.strftime("%d-%m-%Y") if row.attendance_date else ""
        in_time = ""
        if row.in_time:
            in_time = row.in_time.strftime("%H:%M:%S") if hasattr(row.in_time,"strftime") else str(row.in_time).split(" ")[-1]
        table += f"""
        <tr style="background:{color};">
            <td style="border:1px solid #000;padding:5px;">{i}</td>
            <td style="border:1px solid #000;padding:5px;">{row.employee or ''}</td>
            <td style="border:1px solid #000;padding:5px;">{row.employee_name or ''}</td>
            <td style="border:1px solid #000;padding:5px;">{row.status or ''}</td>
             <td style="border:1px solid #000;padding:5px;">{in_time}</td>
            <td style="border:1px solid #000;padding:5px;">{date_value}</td>
            <td style="border:1px solid #000;padding:5px;">{row.leave_type or ''}</td>
        </tr>
        """
    table += "</table>"
    return table

@frappe.whitelist()
def attendance_alert_mail():
    attendance_date = today()
    formatted_date = getdate(attendance_date).strftime("%d-%m-%Y")

    if frappe.db.exists("Holiday", {"holiday_date": attendance_date,"name":"TEAMPRRO-2025"}):
        print("Today is a holiday. Skipping attendance alert mail.")
        return

    attendance = frappe.get_all(
        "Attendance",
        filters={"attendance_date": attendance_date},
        fields=[
            "name","employee","employee_name","status",
            "leave_type","attendance_date","in_time"
        ],
        order_by="employee_name"
    )

    absent_data = []
    late_data = []

    for row in attendance:
        if row.employee in EXCLUDE_EMPLOYEES:
            continue

        if not row.in_time:
            absent_data.append(row)
            continue

        in_time = row.in_time.time() if hasattr(row.in_time, "time") else row.in_time
        if in_time > time(9,30):
            late_data.append(row)

    absent_table = generate_absent_table(absent_data)
    late_table = generate_late_table(late_data)

    frappe.sendmail(
        recipients=["systems@groupteampro.com","sivarenisha.m@groupteampro.com","dineshbabu.k@groupteampro.com"],
        subject=f"Attendance Report - {formatted_date}",
        message=f"""
        Dear Sir/Madam,<br><br>
        Kindly find today's <b>Attendance Report as of 10:00 AM</b>.<br><br>

        <h3>Absent List</h3>
        {absent_table}

        <br><br>

        <h3>Late Entry List</h3>
        {late_table}

        <br><br>
        Thanks & Regards,<br>
        <b>TEAM ERP</b><br><br>

        <i>This email has been automatically generated. Please do not reply.</i>
        """
    )


@frappe.whitelist()
def attendance_alert_mail_1():
    job = frappe.db.exists('Scheduled Job Type','attendance_alert_mail')
    if not job:
        task = frappe.new_doc("Scheduled Job Type")
        task.update({
            "method": 'teampro.email_alerts.attendance_alert_mail',
            "frequency": 'Cron',
            "cron_format": '00 10 * * *'
        })
        task.save(ignore_permissions=True)


import frappe
from frappe.utils import today, getdate

@frappe.whitelist()
def lunch_count_mail():

    attendance_date = today()
    formatted_date = getdate(attendance_date).strftime("%d-%m-%Y")

    # Skip holidays
    if frappe.db.exists("Holiday", {"holiday_date": attendance_date}):
        return

    attendance = frappe.get_all(
        "Attendance",
        filters={
            "attendance_date": attendance_date
        },
        fields=[
            "employee",
            "employee_name",
            "status"
        ],
        order_by="employee_name"
    )

    # Employees to exclude
    exclude_employees = ["TI00225", "TI00002", "TI00001"]

    lunch_data = []

    for row in attendance:

        if row.employee in exclude_employees:
            continue

        # Skip absentees
        if row.status == "Absent":
            continue

        lunch_data.append(row)

    total_count = len(lunch_data)

    table = """
    <table style="width:100%;border-collapse:collapse;font-family:Calibri;font-size:13px;">
    <tr style="background:#5B9BD5;color:white;font-weight:bold;">
        <th style="border:1px solid black;padding:5px;">Sr</th>
        <th style="border:1px solid black;padding:5px;">Employee ID</th>
        <th style="border:1px solid black;padding:5px;">Employee Name</th>
    </tr>
    """

    for i, row in enumerate(lunch_data, start=1):

        color = "#EAF4FF" if i % 2 else "#FFFFFF"

        table += f"""
        <tr style="background:{color};">
            <td style="border:1px solid black;padding:5px;text-align:center;">{i}</td>
            <td style="border:1px solid black;padding:5px;">{row.employee}</td>
            <td style="border:1px solid black;padding:5px;">{row.employee_name}</td>
        </tr>
        """

    table += "</table>"

    frappe.sendmail(
        recipients=["systems@groupteampro.com"],
        subject=f"Lunch Count - {formatted_date}",
        message=f"""
        Dear Sir/Madam,<br><br>

        Kindly find today's <b>Lunch Count as of 10:00 AM</b>.<br><br>

        <b>Total Lunch Count : {total_count}</b><br><br>

        {table}

        <br><br>

        Thanks & Regards,<br>
        <b>TEAM ERP</b><br><br>

        <i>This email has been automatically generated. Please do not reply.</i>
        """
    )

@frappe.whitelist()
def lunch_count_mail_1():

    job = frappe.db.exists(
        "Scheduled Job Type",
        {"method": "teampro.email_alerts.lunch_count_mail"}
    )

    if not job:
        task = frappe.new_doc("Scheduled Job Type")
        task.update({
            "method": "teampro.email_alerts.lunch_count_mail",
            "frequency": "Cron",
            "cron_format": "0 10 * * *"
        })
        task.insert(ignore_permissions=True)
        frappe.db.commit()

    return "Scheduled Job Created"
