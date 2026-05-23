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

        cc = [reports_to, allocated,spoc] + ([dev_spoc] if dev_spoc else []) +([tl_mail] if tl_mail else [])
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