import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import get_first_day, get_last_day, format_datetime, get_url_to_form
from frappe.utils import cint
from frappe.utils.data import date_diff, now_datetime, nowdate, today, add_days
import datetime
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
import frappe,erpnext
from frappe.utils import cint
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
from jobpro.jobpro.doctype.closure.closure import create_sale_order


# @frappe.whitelist()
# def skip_dn_so(doc, method):
# 	skip_delivery_note = 0

# 	for i in doc.items:
# 		maintain_stock = frappe.get_value("Item", i.item_code, "is_stock_item")
# 		if maintain_stock:
# 			skip_delivery_note = 0
# 		else:
# 			skip_delivery_note = 1

# 	doc.skip_delivery_note = skip_delivery_note
# @frappe.whitelist()
# def skip_dn_so(doc, method):
# 	skip_delivery_note = 0

# 	for i in doc.items:
# 		maintain_stock = frappe.get_value("Item", i.item_code, "is_stock_item")
# 		if not maintain_stock:
# 			skip_delivery_note = 1
# 			break
# 	else:
# 		skip_delivery_note = 0

# 	doc.skip_delivery_note = skip_delivery_note


@frappe.whitelist()
def create_project_completion_task(doc, method):
	if doc.service == 'IT-SW':
		task = frappe.db.exists('Task', {'project': doc.name, "subject": (
			"like", 'Project Completion Certificate')})
		if not task:
			task_id = frappe.new_doc('Task')
			task_id.update({
				"subject": "Project Completion Certificate",
				"customer": doc.customer,
				"project": doc.name,
				"service": 'IT-SW',
				"description":"Project Completion Certificate",
				"account_manager": doc.account_manager,
				"project_manager": doc.project_manager,

			})
			task_id.save(ignore_permissions=True)

@frappe.whitelist()
def fetch_start_time(doc,method):
	min_time = frappe.db.sql("""select min(from_time) as min_time from `tabTimesheet Detail` where parent='%s'""" % doc.name,as_dict=1)[0]
	if not doc.start_time:
		frappe.db.set_value("Timesheet",doc.name,"start_time",min_time['min_time'])

@frappe.whitelist()
def intimate_task_pr(task):
	taskid = frappe.get_doc('Task', task)
	message = frappe.render_template(
		"teampro/templates/intimate_task_pr.html",
		{"doc": taskid},
	)
	frappe.sendmail(
		recipients=[taskid.account_manager],
		cc=['it.sw@groupteampro.com',taskid.completed_by],
		message=message,
		subject=_("Task Pending Review - Intimation"),
	)


@frappe.whitelist()
def intimate_task_completion(task):
	taskid = frappe.get_doc('Task', task)
	message = frappe.render_template(
		"teampro/templates/intimate_task_completion.html",
		{"doc": taskid},
	)
	frappe.sendmail(
		recipients=[taskid.account_manager,
					taskid.project_manager, taskid.completed_by],
		cc='it.sw@groupteampro.com',
		message=message,
		subject=_("Task Pending Review - Intimation"),
	)


@frappe.whitelist()
def get_task_name(task):
	frappe.errprint(task)
	task_name = frappe.db.sql(
		"""select name from `tabTask` where status = 'Open' and name = '%s'  """ % (task), as_dict=1)[0]
	return task_name['name']


def create_hooks():
	job = frappe.db.exists('Scheduled Job Type', 'calculate_target')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'teampro.teampro.doctype.target_planner.target_planner.calculate_target',
			"frequency": 'Cron',
			"cron_format": '0 * * * *'
		})
		sjt.save(ignore_permissions=True)


def create_hooks_att():
	job = frappe.db.exists('Scheduled Job Type', 'daily_att_report')
	if not job:
		att = frappe.new_doc("Scheduled Job Type")
		att.update({
			"method": 'teampro.email_alerts.daily_att_report',
			"frequency": 'Cron',
			"cron_format": '30 10 * * *'
		})
		att.save(ignore_permissions=True)


def create_hooks_emc():
	job = frappe.db.exists('Scheduled Job Type', 'daily_emc_report')
	if not job:
		emc = frappe.new_doc("Scheduled Job Type")
		emc.update({
			"method": 'teampro.email_alerts.daily_emc_report',
			"frequency": 'Cron',
			"cron_format": '35 10 * * *'
		})
		emc.save(ignore_permissions=True)
	
def create_hooks_create_update_leave_allocation():
	job = frappe.db.exists('Scheduled Job Type', 'create_update_leave_allocation')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'teampro.utility.create_update_leave_allocation',
			"frequency": 'Monthly',
			# "cron_format": '0 * * * *'
		})
		sjt.save(ignore_permissions=True)

def update_tat_monitor_in_check():
	job = frappe.db.exists('Scheduled Job Type', 'tat_variation')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'checkpro.checkpro.doctype.case.case.tat_variation',
			"frequency":'Daily',
			# "cron_format": '0 * * * *'
		})
		sjt.save(ignore_permissions=True)

def update_tat_monitor_in_case():
	job = frappe.db.exists('Scheduled Job Type', 'tat_calculation')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'checkpro.checkpro.doctype.case.case.tat_calculation',
			"frequency":'Daily',
			# "cron_format": '0 * * * *'
		})
		sjt.save(ignore_permissions=True)

def update_tat_monitor_in_batch():
	job = frappe.db.exists('Scheduled Job Type', 'tat_monitor')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'checkpro.checkpro.doctype.case.case.tat_monitor',
			"frequency":'Daily',
			# "cron_format": '0 * * * *'
		})
		sjt.save(ignore_permissions=True)


def create_hooks_attendance():
	job = frappe.db.exists('Scheduled Job Type', 'mark_att')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'teampro.mark_attendance.mark_att',
			"frequency": 'Cron',
			"cron_format": '00 10 1 * *'
		})
		sjt.save(ignore_permissions=True)


def remove_private():
	cand = frappe.db.sql(
		"""select name,irf from `tabCandidate` where irf != '' """, as_dict=True)
	print(len(cand))
	for can in cand:
		if can.irf:
			print("----------------------")
			print(can.irf)
			frappe.db.set_value("Candidate", can.name, "irf",
								(can.irf).replace("/private", ""))
			print("------------------------")




def bulk_update_from_csv(filename):
	# below is the method to get file from Frappe File manager
	from frappe.utils.file_manager import get_file
	# Method to fetch file using get_doc and stored as _file
	_file = frappe.get_doc("File", {"file_name": filename})
	# Path in the system
	filepath = get_file(filename)
	# CSV Content stored as pps

	pps = read_csv_content(filepath[1])
	count = 0
	for pp in pps[:5]:
		mobile = pp[0]
		project = pp[1]
		position = pp[2]
		given_name = pp[3]
		customer = pp[4]
		print(mobile, project, position, given_name, customer)
		# ld = frappe.db.exists("Lead",{'name':pp[0]})
		# if ld:
		#     # items = frappe.get_all("Lead",{'name':pp[0]})
		#     # for item in items:
		#     i = frappe.get_doc('Lead',pp[0])
		#     if not i.contact_date:
		#         i.contact_date = pp[1]
		#         # i.append("supplier_items",{
		#         #     'supplier' : pp[1]
		#         # })
		#         i.save(ignore_permissions=True)
		#         frappe.db.commit()


def update_nxd():
	leads = frappe.get_list("Lead")
	for lead in leads:
		l = frappe.get_doc("Lead", lead.name)
		if not l.contact_date:
			l.contact_date = "2020-08-31 0:00:00"
			l.save(ignore_permissions=True)
			frappe.db.commit()


def update_lead():
	leads = frappe.get_list("Lead", {"organization_lead": "0"})
	for lead in leads:
		doc = frappe.get_doc("Lead", lead.name)
		doc.organization_lead = 1
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		# frappe.errprint(lead.name)


@frappe.whitelist()
def add_project_id(project):
	projects = frappe.db.sql(
		"""select project_id from `tabProject` where project_id is not null order by creation""", as_dict=True)
	project_id = projects[-1].project_id
	return 'PRO' + str(int(project_id.strip('PRO'))+1)


@frappe.whitelist()
def update_task_fields(project):
	tasks = frappe.get_all('Task', {'project': project}, [
						   'name', 'project_manager', 'account_manager', 'service'])
	proj = frappe.get_doc('Project', {'name': project})
	for t in tasks:
		frappe.errprint('---')
		frappe.errprint(t.account_manager)
		frappe.errprint(proj.account_manager)
		frappe.errprint('---')
		if t.project_manager != proj.project_manager:
			frappe.db.set_value(
				'Task', t.name, 'project_manager', proj.project_manager)
		if t.account_manager != proj.account_manager:
			frappe.db.set_value(
				'Task', t.name, 'account_manager', proj.account_manager)
		if t.service != proj.service:
			frappe.db.set_value('Task', t.name, 'service', proj.service)


@frappe.whitelist()
def opportunity_send_mail(self, method):
	if self.service == 'TGT':
		link = get_url_to_form("Opportunity", self.name)
		subject = 'Reg.Opportunity- %s' % self.name
		content = """Dear Mam<br>Kindly find the new Opportunity.
		Click on <a href='%s'>View</a> to open the opportunity.<br>Thanks & Regards,<br>ERP
		""" % link
		frappe.sendmail(recipients=['saraswathi.p@groupteampro.com'],
						subject=subject,
						message=content)


@frappe.whitelist()
def checkin_alerts():
	# yesterday = add_days(today(),-2)
	yesterday = add_days(datetime.datetime.today(), -17).date()
	current_month = yesterday.month
	late_checkins = frappe.db.sql(
		"select employee from `tabEmployee Checkin` where date(time) = '%s' and time(time) > '09:35:00' " % (yesterday), as_dict=True)
	frappe.errprint(late_checkins)
	if late_checkins:
		for emp in late_checkins:
			apid = frappe.db.exists('Attendance Permission', {
									'employee': emp.employee, 'month': current_month})
			print(emp)
			if apid:
				pc = frappe.get_value(
					'Attendance Permission', apid, 'permission_count')
				if pc < 3:
					# adding permission
					ap = frappe.get_doc('Attendance Permission', apid)
					ap.update({
						'permission_count': pc + 1
					})
					ap.save(ignore_permissions=True)
					frappe.db.commit()

					lp = frappe.db.exists('Leave Application', {
										  'employee': emp.employee, 'from_date': yesterday, 'to_date': yesterday})
					if lap:
						pass
				else:
					lw = frappe.new_doc('Leave Application')
					lw.update({
						'employee': emp.employee,
						'leave_type': "Leave Without Pay",
						'from_date': yesterday,
						'to_date': yesterday,
						'description': 'Auto marked as LWP due to Exceed Monthly Permission Limit'
					})
					lw.save(ignore_permissions=True)
					frappe.db.commit()

			else:
				ap = frappe.new_doc('Attendance Permission')
				ap.update({
					'employee': emp.employee,
					'month': current_month,
					'permission_count': 1
				})
				ap.save(ignore_permissions=True)
				frappe.db.commit()


@frappe.whitelist()
def lwp_alert():
	yesterday = add_days(today(), -19)
	employees = frappe.get_all('Employee', {'status': 'Active'}, [
							   'name', 'employee_name', 'employee'])
	for emp in employees:
		lc = frappe.db.sql("select employee from `tabEmployee Checkin` where date(time) = '%s' and employee = '%s'" % (
			yesterday, emp.name), as_dict=True)
		lap = frappe.db.exists('Leave Application', {
							   'employee': emp.employee, 'from_date': yesterday, 'to_date': yesterday})
		if lap:
			pass
		if len(lc) < 2:
			lp = frappe.new_doc('Leave Application')
			lp.update({
				'employee': emp.employee,
				'leave_type': "Leave Without Pay",
				'from_date': yesterday,
				'to_date': yesterday,
				'description': 'Auto marked as LWP due to not responding Miss Punch Alert'
			})
			lp.save()
			frappe.db.commit()


@frappe.whitelist()
def update_task_count(doc, method):
	if doc.task:
		submitted = frappe.db.count(
			'Candidate', {'task': doc.task, 'pending_for': 'Submitted'}) or 0
		psl = frappe.db.count('Candidate', {'task': doc.task, 'pending_for': (
			'in', ('Client Offered', 'Proposed PSL'))}) or 0
		shortlisted = frappe.db.count(
			'Candidate', {'task': doc.task, 'pending_for': ('in', ('Shortlisted',))}) or 0
		linedup = frappe.db.count(
			'Candidate', {'task': doc.task, 'pending_for': 'Linedup'}) or 0
		interviewed = frappe.db.count(
			'Candidate', {'task': doc.task, 'pending_for': 'Interviewed'}) or 0

		frappe.db.update('Task', doc.task, 'psl', psl)
		frappe.db.update('Task', doc.task, 'fp', submitted + interviewed)
		frappe.db.update('Task', doc.task, 'sl', shortlisted + linedup)

		task_status = frappe.db.get_value('Task', doc.task, 'status')

		if task_status in ('Completed', 'Cancelled'):
			# if pps == 0:
			frappe.db.update('Task', doc.task, 'sp', 0)

		else:
			vac = frappe.db.get_value('Task', doc.task, 'vac')
			prop = frappe.db.get_value('Task', doc.task, 'prop')
			pps = (vac - psl) * prop - (submitted +
										interviewed + shortlisted + linedup)
			frappe.db.set_value('Task', doc.task, 'sp', pps)

# def update_candidate():
#     tasks = frappe.get_all('Task',{'service':('not in',('TGT','IT-SW'))})
#     for task in tasks:
#         task = task.name
#         print(task)
#         submitted = frappe.db.count('Candidate',{'task':task,'pending_for':'Submitted'}) or 0
#         psl = frappe.db.count('Candidate',{'task':task,'pending_for':'Proposed PSL'}) or 0
#         shortlisted = frappe.db.count('Candidate',{'task':task,'pending_for':('in',('Shortlisted','Client Offered'))}) or 0
#         linedup = frappe.db.count('Candidate',{'task':task,'pending_for':'Linedup'}) or 0
#         interviewed = frappe.db.count('Candidate',{'task':task,'pending_for':'Interviewed'}) or 0

#         frappe.db.update('Task',task,'psl',psl)
#         frappe.db.update('Task',task,'fp',submitted + interviewed)
#         frappe.db.update('Task',task,'sl',shortlisted + linedup)

#         print([psl,submitted,interviewed,shortlisted,linedup])

#         task_status = frappe.db.get_value('Task',task,'status')
#         if task_status in ('Completed','Cancelled'):
#             frappe.db.update('Task',task,'sp',0)
#         else:
#             vac = frappe.db.get_value('Task',task,'vac')
#             prop = frappe.db.get_value('Task',task,'prop')
#             pps = (vac - psl) * prop - (submitted + interviewed + shortlisted + linedup)
#             frappe.db.update('Task',task,'sp',pps)


def test_hook():
	frappe.log_error(title='hi', message='ok')


# def update_submission_date(doc, method):
# 	frappe.errprint(nowdate())
# 	frappe.db.set_value("Sales Invoice", doc.name, "posting_date", nowdate())
# 	frappe.db.commit()


@frappe.whitelist()
def attendance():
	att = frappe.db.sql("""update `tabEmployee Checkin` set skip_auto_attendance = 0 where date(time) between '2023-09-01' and '2023-09-30'   """)
	print(att)

@frappe.whitelist()
def get_delivery_note(doc, method):
	# if not frappe.db.exist("Sales Invoice",doc.name)
	# nd= frappe.new_doc("Sales Invoice")
	si = frappe.get_doc("Sales Invoice", {"name": doc.sales_invoice_no})
	si.delivery_note_no = doc.name
	si.save(ignore_permissions=True)


@frappe.whitelist()
def set_customer_group():
	sales = frappe.get_all('Sales Invoice', ["*"])
	for i in sales:
		customer_group = frappe.get_value(
			'Customer', {'name': i.customer}, ['customer_group'])
		frappe.db.set_value('Sales Invoice', i.name,
							'customer_group', customer_group)


@frappe.whitelist()
def date(time):
	print('Hi')
	log_date = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')
	x = log_date.strftime('%Y-%m-%d')

	return x


@frappe.whitelist()
def mark_bulk_drop():
	closure = frappe.db.get_all('Closure', {
								'customer': 'Arabian Castles for General Contracting Co., LLC', 'nationality': 'Nepali'}, ['*'])
	print(closure)
	for ca in closure:
		frappe.db.set_value('Closure', ca.name, 'status', 'Dropped')


@frappe.whitelist()
def organization_name():
	opportunity = frappe.db.get_all('Opportunity', ["*"])
	for i in opportunity:
		print(i.title)
		frappe.db.set_value("Opportunity", i.name,
							"organization_name", i.title)


@frappe.whitelist()
def address_html():
	lead = frappe.db.get_all('Lead', ["*"])
	for i in lead:

		print(i.address)
		frappe.db.set_value("Lead", i.name, "address", i.address)


@frappe.whitelist()
def late():
	late = frappe.db.sql("""delete from `tabLate Penalty` """)
	print(late)


# @frappe.whitelist()
# def update_attendance(doc, method):
# 	if doc.half_day != 1 :
# 		attendance_req = frappe.get_all("Attendance", {'attendance_date': (
# 			'between', (doc.from_date, doc.to_date)), 'employee_name': doc.employee_name}, ['name'])
# 		for att in attendance_req:
# 			if att.name:
# 				at = frappe.get_doc("Attendance", att.name)
# 				at.delete()


@frappe.whitelist()
def get_child(parent):
	if parent:
		so = frappe.get_doc("Candidate", parent)
		if so.table_28:
			return so.table_28


@frappe.whitelist()
def update_location_route():
	cust = frappe.db.get_all('Customer',{'customer_group':'Retail Shops'},['*'])
	for cus in cust:
		if cus.location:
			sales_order = frappe.db.get_all('Sales Order', {'customer': cus.name,'company':'TEAMPRO Food Products'}, ['*'])
			for sales in sales_order:
				frappe.db.set_value('Sales Order',sales.name,'location',cus.location)

@frappe.whitelist()
def update_user():
	user_id = frappe.get_value('Employee',{'employee':'TI00005'},['user_id'])
	print (user_id)
	hod = frappe.get_value('User',{'email':user_id},['name'])
	role = "HOD"
	hod = frappe.get_value('Has Role',{'role':role,'parent':hod})
	if hod:
		print("HI")
	else:
		hod = frappe.get_doc('Has Role',{'parent':user_id},['name'])
		hod.role = "HOD"
		print("HII")

@frappe.whitelist()
def get_item_codes(company_name):
	item_codes = []
	item_defaults = frappe.get_all('Item Default',
		filters={'company': ('in', frappe.get_all('Item Default Company',
			filters={'company': company_name},
			pluck='parent'
		))},
		pluck='item_code'
	)
	item_codes.extend(item_defaults)
	return item_codes
# update route number 
@frappe.whitelist()
def update_route_no():
	route = frappe.db.get_all('Customer',{'customer_group':'Retail Shops'},['*'])
	for ro in route :
		if ro.route_no:
			sales_invoice = frappe.db.get_all('Sales Invoice', {'customer': ro.name}, ['*'])
			for sales in sales_invoice:
				print(ro.name)
				frappe.db.set_value('Sales Invoice', sales.name,'route_no',ro.route_no)

# @frappe.whitelist()
# def get_against_so(doc,method):
#     if doc.is_return == 1 and doc.update_stock == 0:
#         sales_order = frappe.db.sql("""select `tabSales Invoice Item`.sales_order from `tabSales Invoice` left join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent where `tabSales Invoice`.name = '%s' """%(doc.name),as_dict=True)[0]
#         frappe.errprint(sales_order['sales_order'])
#         dn = frappe.db.sql("""select parent from `tabDelivery Note Item` where `tabDelivery Note Item`.against_sales_order = '%s' """%(sales_order['sales_order']),as_dict=True)[0]
#         copy_dn = frappe.get_doc("Delivery Note",dn["parent"])
#         dnr = frappe.copy_doc(copy_dn)
#         dnr.is_return = 1
#         # dnr.return_against = dn["parent"]
#         dnr.set("items",[])
#         for j in doc.items:
#             dnr.append("items",{
#                 "item_code":j.item_code,
#                 "item_name":j.item_name,
#                 "description":j.description,
#                 "qty":j.qty,
#                 "cost_center":j.cost_center,
#                 "uom":j.uom,
#                 "stock_uom":j.uom,
#                 "rate":j.rate,
#                 "conversion_factor":1,
#                 "base_rate":j.base_rate,
#                 "amount":j.amount,
#                 "base_amount":j.base_amount,
#                 "expense_account": "Cost of Goods Sold - TFP"
#             })
#         dn_list = frappe.db.sql("""select parent from `tabDelivery Note Item` where `tabDelivery Note Item`.against_sales_order = '%s' """%(sales_order['sales_order']),as_dict=True)
#         for k in dn_list:
#             do = frappe.get_doc("Delivery Note",k.parent)
#             if do.docstatus == 1:
#                 dnr.append("return_against_dn",{
#                     "delivery_note":k.parent,
#                 })
#         dnr.save(ignore_permissions = True)
#         dnr.submit()

@frappe.whitelist()
def address(lead):
	frappe.errprint(lead)
	if frappe.db.exists('Address',{'address_title':lead}):
		ad = frappe.get_doc('Address',{'address_title':lead})
		ad.address_title = lead
		ad.address_type = frappe.db.get_value('Lead',{'name':lead},['address_type'])
		ad.address_line1 = frappe.db.get_value('Lead',{'name':lead},['address_line_1'])
		ad.address_line2 = frappe.db.get_value('Lead',{'name':lead},['address_line_2'])
		ad.city = frappe.db.get_value('Lead',{'name':lead},['city_town'])
		ad.state = frappe.db.get_value('Lead',{'name':lead},['state__province'])
		ad.country = frappe.db.get_value('Lead',{'name':lead},['country__'])
		ad.pincode = frappe.db.get_value('Lead',{'name':lead},['postal_code'])
		ad.save(ignore_permissions=True)
		frappe.db.commit()
	else:
		ad = frappe.new_doc('Address')
		ad.address_title = lead
		ad.address_type = frappe.db.get_value('Lead',{'name':lead},['address_type'])
		ad.address_line1 = frappe.db.get_value('Lead',{'name':lead},['address_line_1'])
		ad.address_line2 = frappe.db.get_value('Lead',{'name':lead},['address_line_2'])
		ad.city = frappe.db.get_value('Lead',{'name':lead},['city_town'])
		ad.state = frappe.db.get_value('Lead',{'name':lead},['state__province'])
		ad.country = frappe.db.get_value('Lead',{'name':lead},['country__'])
		ad.pincode = frappe.db.get_value('Lead',{'name':lead},['postal_code'])
		ad.save(ignore_permissions=True)
		frappe.db.commit()


@frappe.whitelist()
def contact(lead):
	frappe.errprint(lead)
	co = frappe.db.sql("""select * from `tabLead Contacts` where `tabLead Contacts`.parent = '%s' """%(lead),as_dict=True)
	# frappe.errprint(co)
	for c in co:
		frappe.errprint("HI")
		frappe.errprint(c.person_name)
		frappe.errprint(c.mobile)
		if frappe.db.exists('Contact',{'first_name':c.person_name,'mobile_no':c.mobile}):
			cn = frappe.get_doc('Contact',{'first_name':c.person_name,'mobile_no':c.mobile})
			cn.first_name = c.person_name
			cn.company_name = frappe.db.get_value('Lead',{'name':lead},['company_name'])
			cn.lead = lead
			for i in cn.email_ids:
				frappe.errprint("HI")
				i.append("email_ids",{
					"email_id":c.email_id,
					"is_primary":c.is_primaryemail
				})
			for i in cn.phone_nos:
				frappe.errprint("HI")
				i.append("phone_nos",{
					"phone":c.mobile,
					"is_primary_phone":c.is_primary,
					"has_whatsapp":c.has_whatsapp
				})
			cn.save(ignore_permissions=True)
			frappe.db.commit()
		else:
			cn = frappe.new_doc('Contact')
			cn.first_name = c.person_name
			cn.company_name = frappe.db.get_value('Lead',{'name':lead},['company_name'])
			cn.lead = lead
			for i in cn.email_ids:
				frappe.errprint("HI")
				i.append("email_ids",{
					"email_id":c.email_id,
					"is_primary":c.is_primaryemail
				})
			for i in cn.phone_nos:
				frappe.errprint("HI")
				i.append("phone_nos",{
					"phone":c.mobile,
					"is_primary_phone":c.is_primary,
					"has_whatsapp":c.has_whatsapp
				})
			cn.save(ignore_permissions=True)
			frappe.db.commit()
	
	
@frappe.whitelist()
def calc_cut_off_prize(doc,method):
	for f in doc.items:
		tfp_item = frappe.db.sql("""select tfp from `tabItem` where name = '%s' """%(f.item_code),as_dict=1)[0]
		tfp = tfp_item['tfp']
		if tfp == 1:
			price_list = frappe.db.sql("""select price_list_rate from `tabItem Price` where price_list = 'Cut Off Price' and item_code = '%s' """%(f.item_code),as_dict=1)
			for p in price_list:
				if f.uom == 'Gram':
					item_price = (p.price_list_rate / 1000)
					item_rate = round((item_price),2)
					frappe.errprint(item_rate)
					if f.rate < item_rate:
						frappe.throw(_(' %s Rate is lesser than cut-off price')%(f.item_name))
				elif f.uom == 'Kg':
					if f.rate < p.price_list_rate:
						frappe.throw(_(' %s Rate is lesser than cut-off price')%(f.item_name))	

	
@frappe.whitelist()
def file_list(candidate):
	url_ls =[]
	file_list = frappe.get_all("File",{"attached_to_name": candidate},['file_url'])
	for a in file_list:
		url_ls.append(a.file_url)
	return url_ls


import requests
import io
from frappe import _
import PyPDF2
from frappe.utils.file_manager import get_file
from urllib.parse import urljoin

@frappe.whitelist()
def merge_and_open_pdf(candidate):
	url_list = []
	file_list = frappe.get_all("File", {"attached_to_name": candidate}, ["file_url"])

	merger = PyPDF2.PdfFileMerger()
	for file in file_list:
		base_url = frappe.utils.get_url()
		file_urls = frappe.utils.get_url(file.file_url)
		file_url = urljoin(base_url, file_urls)
		if file_url:
			try:
				response = requests.get(file_url)
				if response.headers.get("content-type") != "application/pdf":
					# Skip non-PDF files
					continue

				temp_file = io.BytesIO(response.content)
				merger.append(temp_file)
			except Exception as e:
				# Log the specific error message
				frappe.log_error(f"Error merging PDF: {str(e)}", _("Merge and Open PDF Error"))
				continue
		else:
			# Failed to retrieve the file, log the error
			frappe.log_error(f"Failed to retrieve file: {file_url}", _("Merge and Open PDF Error"))

	merged_pdf = io.BytesIO()
	merger.write(merged_pdf)
	merger.close()

	if len(merged_pdf.getvalue()) == 0:
		# Merged PDF is empty or invalid
		frappe.log_error("Merged PDF is empty or invalid", _("Merge and Open PDF Error"))
		return None

	return {
		"content": merged_pdf.getvalue(),
		"file_name": "merged_pdf.pdf",
		"file_type": "application/pdf"
	}



def is_valid_pdf(file):
	try:
		pdf_reader = PyPDF2.PdfFileReader(file)
		return pdf_reader.numPages > 0
	except PyPDF2.utils.PdfReadError:
		return False


import json
@frappe.whitelist()
def get_supporting_docs(selected_docs):
	selected_docs = json.loads(selected_docs)
	file_list = []
	for s in selected_docs:
		file_name = frappe.get_value("File", {"file_url": s},"name")
		file_list.append(file_name)
	return file_list


from datetime import datetime
from frappe import throw, _

def validate_date(doc, method):
	current_date = datetime.now().date()
	date_str = doc.posting_date
	frappe.errprint(date_str)
	date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
	frappe.errprint(current_date)
	if date_obj < current_date:
		throw(_("Submitting the Purchase Invoice on back date will have impact on the GST .Please click on the 'Edit Posting Date' and change the Date to Today."))


def validate_date_salesinvoice(doc, method):
	current_date = datetime.now().date()
	date_str = doc.posting_date
	frappe.errprint(date_str)
	date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
	frappe.errprint(current_date)
	if date_obj < current_date:
		throw(_("Submitting the Sales Invoice on a past date will have an impact on the GST. Please click on 'Edit Posting Date' and change the date to today."))


# def validate_date_salesinvoice(doc, method):
# 	today = date.today()
# 	date_str = doc.due_date
# 	frappe.errprint(date_str)
# 	date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
# 	frappe.errprint(today)
# 	if date_obj < today:
# 		throw(_("Submitting the Sales Invoice on back date will have impact on the GST .Please click on the 'Edit Posting Date' and change the Date to Today."))

@frappe.whitelist()
def update_pi():
	doc = frappe.db.sql(""" update `tabPurchase Invoice` set workflow_state = "Cancelled" where name = "ACC-PINV-2023-00076"  """)
	print(doc)


@frappe.whitelist()
def calac_invoice_discount(doc,method):
	discount = 0
	if doc.tfp_items:
		for i in doc.tfp_items:
			discount += (i.discount_amount * i.packet) * i.qty__packet
		frappe.db.set_value("Sales Invoice",doc.name,"tfp_discount",discount)

@frappe.whitelist()
def child_table_calc(doc,method):
	if doc.tfp_items:
		for i in doc.tfp_items:
			i.qty = i.packet * i.qty__packet
			i.rate_packet = round(i.qty__packet * (i.price_list_rate))
			i.special_rate = round(i.rate_packet - (i.rate_packet * (i.discount_percentage/100)))
			i.amount = round(i.special_rate) * i.packet
			for j in doc.items:
				if i.item_code == j.item_code:
					j.amount = i.amount
					j.delivery_date = doc.delivery_date


@frappe.whitelist()
def return_detailed_ts(timesheet):
	timesheet = frappe.db.sql(""" select `tabTimesheet Detail`.task,`tabTimesheet Detail`.subject,`tabTimesheet Detail`.project,sum(`tabTimesheet Detail`.hours) as hours, GROUP_CONCAT(`tabTimesheet Detail`.description separator ', ') as description from `tabTimesheet`
	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where `tabTimesheet`.name = '%s' group by `tabTimesheet Detail`.task"""%(timesheet),as_dict = 1)
	return timesheet
	

#For downloading item table as excel
@frappe.whitelist()
def make_time_sheet():
	args = frappe.local.form_dict
	filename = args.name
	test = build_xlsx_response(filename)

def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
	args = frappe.local.form_dict
	column_widths = column_widths or []
	if wb is None:
		wb = openpyxl.Workbook()
	ws = wb.create_sheet(sheet_name, 0)
	doc = frappe.get_doc("Timesheet",args.name)
	cb = frappe.db.get_value("Employee",doc.employee,['short_code'])
	if doc:
		ws.append(["Task","Subject","Project Name","CB","Status","TU","Description"])
		for i in doc.timesheet_summary:
			ws.append([i.task,i.subject,i.project,cb,i.status,round(i.tu,2),i.description])
	xlsx_file = BytesIO()
	wb.save(xlsx_file)
	return xlsx_file

def build_xlsx_response(filename):
	xlsx_file = make_xlsx(filename)
	frappe.response['filename'] = filename + '.xlsx'
	frappe.response['filecontent'] = xlsx_file.getvalue()
	frappe.response['type'] = 'binary' 	

@frappe.whitelist()
def get_all_quot(doc,method):
	if doc.tfp_items:
		for i in doc.tfp_items:
			i.qty = i.packet * i.qty__packet
			i.rate_packet = round(i.qty__packet * (i.price_list_rate))
			i.special_rate = round(i.rate_packet - (i.rate_packet * (i.discount_percentage/100)))
			i.amount = round(i.special_rate) * i.packet
			for j in doc.items:
				if i.item_code == j.item_code:
					j.amount = i.amount

			
@frappe.whitelist()
def get_all_so(name):
	so = frappe.get_doc("Sales Order",name)
	return so.tfp_items

@frappe.whitelist()
def get_all_quote(name):
	quote = frappe.get_doc("Quotation",name)
	return quote.tfp_items

@frappe.whitelist()
def update_pi():
	print("HI")
   
@frappe.whitelist()
def update_custodian(doc,method):
	if doc.status == "Left":
		asset = frappe.get_all("Asset",{"custodian":doc.name},["name"])
		for i in asset:
			cust = frappe.get_doc("Asset",i.name)
			cust.custodian = ''
			cust.custodian_name = ''
			cust.department = ''
			cust.save(ignore_permissions = True)

@frappe.whitelist()
def create_food_count():
	from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
	holiday_list_name = 'TEAMPRO 2023'
	start_date = getdate(today())
	if not is_holiday(holiday_list_name, start_date):
		emp = ["TI00086"]
		for i in emp:
			if not frappe.db.exists("Food Count",{'employee':i,'date':nowdate()}):
				doc = frappe.new_doc("Food Count")
				doc.employee = i
				doc.date = nowdate()
				doc.save(ignore_permissions=True)

def add_food_count():
	job = frappe.db.exists('Scheduled Job Type', 'create_food_count')
	if not job:
		print("HI")
		sjt = frappe.new_doc("Scheduled Job Type")
	sjt.update({
		"method": 'teampro.custom.create_food_count',
		"frequency": 'Cron',
		"cron_format": '0 9 * * *'
	})
	sjt.save(ignore_permissions=True)
	
@frappe.whitelist()
def delete_document(name,checks_list):
	checks_list = json.loads(checks_list)
	nam = frappe.get_doc("Case",name)
	nam.delete()
	for i in checks_list:
		doc = frappe.get_doc(i["checks"],i["check_id"])
		doc.delete()


@frappe.whitelist()
def update_batch_status(doc,method):
	if doc.get("batch"):
		batch_doc = frappe.get_doc("Batch", doc.get("batch"))
		batch_doc.batch_status = "Proposed SO"
		batch_doc.save()

@frappe.whitelist()
def sales_order_batch(doc, method):
	sales_order = frappe.get_doc("Sales Order", doc.sales_order)
	if hasattr(sales_order, "batch") and sales_order.batch:
		doc.batch = sales_order.batch
		batch_doc = frappe.get_doc("Batch", doc.batch)
		batch_doc.billing_status = "Billed"
		batch_doc.save()

@frappe.whitelist()
def get_po_qty(item,company):
	new_po = frappe.db.sql("""select sum(`tabPurchase Order Item`.qty) as qty,sum(`tabPurchase Order Item`.received_qty) as d_qty from `tabPurchase Order` left join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent where `tabPurchase Order Item`.item_code = '%s' and `tabPurchase Order`.docstatus = 1 and `tabPurchase Order`.company = '%s' """ % (item,company), as_dict=True)[0]
	if not new_po['qty']:
		new_po['qty'] = 0
	if not new_po['d_qty']:
		new_po['d_qty'] = 0
	ppoc_total = new_po['qty'] - new_po['d_qty']
	return ppoc_total


@frappe.whitelist()
def get_salesorder_qty(item,company):
	new_so = frappe.db.sql("""select sum(`tabSales Order Item`.qty *`tabSales Order Item`.conversion_factor) as qty,sum(`tabSales Order Item`.delivered_qty *`tabSales Order Item`.conversion_factor) as d_qty from `tabSales Order` left join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent where `tabSales Order Item`.item_code = '%s' and `tabSales Order`.docstatus = 1 and `tabSales Order`.company = '%s' and status != 'Closed' """ % (item,company), as_dict=True)[0]
	if not new_so['qty']:
		new_so['qty'] = 0
	if not new_so['d_qty']:
		new_so['d_qty'] = 0
	del_total = new_so['qty'] - new_so['d_qty']
	return del_total


@frappe.whitelist()
def del_doc():
	att = frappe.db.sql(""" delete from `tabCourt` where name = 'Court-9166'  """)

@frappe.whitelist()
def get_values(name):
	ch=[]
	# list=["Generate Report","Generate Report with Insuff","Report Completed"]
	case = frappe.db.get_all("Case",{"batch":name,"case_status":["in",["Generate Report","Generate Report with Insuff","Completed"]]},["name"])
	for c in case:
		ch.append({
			"case_id":c.name,

		})
		# row = len(ch)
		# frappe.db.set_value("Batch",name,"rows",row)
	return ch

@frappe.whitelist()
def set_values(name):
	row = frappe.db.count("Case",{"batch":name,"case_status":["in",["Generate Report","Generate Report with Insuff","Completed"]]})
	billed = frappe.db.count("Case",{"batch": name, "billing_status": ["in", ["Billed", "Partially Billed"]]})
	pending_bill = row- billed
	return row,billed,pending_bill

	
@frappe.whitelist()
def create_so(doctype,batch,case_id):
	batch=frappe.get_doc("Batch",batch)
	case=frappe.get_doc("Case",case_id)
	item = frappe.new_doc("Item")
	item.item_code = case_id
	item.item_name= case.case_name
	item.item_group = "BCS Cases"
	item.item_group_code= "BCS"
	item.stock_uom = "Nos"
	item.qty = "1"
	item.gst_hsn_code = '998521'
	item.is_stock_item = "0"
	item.include_item_in_manufacturing = "0"
	dict_list = []
	dict_list.append(frappe._dict({"item_tax_template":"GST 18% - THIS","tax_category":"Tamil Nadu","valid_from": today()}))
	dict_list.append(frappe._dict({"item_tax_template":"I - GST @ 18% - THIS","tax_category":"Inter State","valid_from": today()}))
	for i in dict_list:
		item.append("taxes", {
			"item_tax_template":i.item_tax_template,
			"tax_category":i.tax_category,
			"valid_from": i.valid_from
			})
	item.append("item_defaults", {
				"company": "TeamPRO HR & IT Services Pvt. Ltd.",
				"buying_cost_center":"Main - THIS",
				"selling_cost_center":"Main - THIS",
				"income_account":"Sales - THIS",
				"expense_account":"Cost of Goods Sold - THIS"
			})
	item.insert()
	item.save(ignore_permissions=True)

	so = frappe.new_doc("Sales Order")
	so.company = "TEAMPRO HR & IT Services Pvt. Ltd."
	so.customer = batch.customer
	so.service = "BCS"
	so.order_type = "Sales"
	so.delivery_date = today()  
	so.transaction_date = today() 
	so.po_no = batch.customers_purchase_order
	# so.delivery_manager = batch.delivery_manager
	so.posa_notes:case.case_report
	so.tc_name="Account Details - THIS"
	rate = frappe.db.get_value("Check Package", {"name":batch.check_package},["total_sp"])
	
	so.append('items', {
		'item_code': case_id,
		'item_name':case.case_name,
		'description':batch.name,
		'qty':1,
		'posa_notes':case.case_report,
		'rate':rate,
		})
	case_status=case.case_status
	billing_status = case.billing_status
	if case_status =="Generate Report" or case_status=="Completed":
		frappe.set_value("Case",case_id,"billing_status","Billed")
	if case_status=="Generate Report with insuff":
		frappe.set_value("Case",case_id,"billing_status","Partially Billed")
	
	so.insert()
	so.save(ignore_permissions=True)

def on_task_save(doc, method):
	if doc.service == 'IT-SW':
		if doc.status == "Pending Review":
			issue = frappe.get_doc("Issue", doc.issue)
			task = frappe.db.count("Task",{'issue':doc.issue})
			if task == 1:
				if issue and issue.status != "Resolved":
					issue.status = "Resolved"
					issue.save()

		if doc.status == "Completed":
			issue = frappe.get_doc("Issue", doc.issue)
			if issue and issue.status != "Closed":
				issue.status = "Closed"
				issue.save()

		

@frappe.whitelist()
def issue_status(doc,method):
	if doc.service == 'IT-SW':
		if doc.issue is not None:
			if doc.status in ["Open","Working","Hold"]:
				issue = frappe.get_doc("Issue", doc.issue)
				if issue and issue.status != "Replied":
					issue.status = "Replied"
					issue.task = doc.name
					issue.assigned_to = doc.completed_by
					issue.project = doc.project
					issue.save()
			if doc.status == "Pending Review":
				issue = frappe.get_doc("Issue", doc.issue)
				if issue and issue.status != "Resolved":
					issue.status ="Resolved"
					issue.assigned_to = doc.completed_by
					issue.project = doc.project
					issue.save()
			if doc.status == "Completed":
				issue = frappe.get_doc("Issue", doc.issue)
				if issue and issue.status != "Closed":
					issue.status ="Closed"
					issue.assigned_to = doc.completed_by
					issue.project = doc.project
					issue.save()

@frappe.whitelist()
def update_cb(doc,method):
	if doc.service == 'IT-SW' and doc.completed_by != "":
		cb = frappe.get_value("Employee",{'user_id':doc.completed_by},['short_code'])
		frappe.db.set_value("Task",doc.name,"cb",cb)

@frappe.whitelist()
def return_val():
	total_expected_time= frappe.db.sql(""" select sum(expected_time) as et from `tabTask` where project = '%s' """%("GOTRADEPRO"),as_dict=1)
	frappe.errprint(total_expected_time)
	

@frappe.whitelist()
def update_actual_tat(date1,date2,date3,date4,pac_tat):
	list = ["Education Checks","Family","Reference Check","Court","Social Media","Criminal","Employment","Identity Aadhar","Address Check"]
	actual_tat=0
	tat = 0
	tat_monitor = ''
	date = 0
	dat = 0
	variation = 0
	for i in list:
		doc=frappe.db.get_list(i,["name","workflow_state"])
		for j in doc:
			if(date2 and j.workflow_state=="Report Completed"):
				date=(date_diff(date2,date1))
				dat=(sum([int(date3),int(date4)]))
				actual_tat=date - dat
				variation = int(actual_tat)-int(pac_tat)

				if variation < 0:
					tat=0
					tat_monitor = "In TAT"
				else:
					tat=variation
					tat_monitor = "Out TAT"
			# frappe.errprint(date)
			# frappe.errprint(dat)
			# frappe.errprint(variation)
		return actual_tat,tat,tat_monitor

@frappe.whitelist()
def case_drop_status(name,remark):
	frappe.db.set_value("Case",name,"case_status","Drop")
	frappe.db.set_value("Case",name,"reason_of_drop",remark)
	frappe.db.set_value("Case",name,"dropped",1)

@frappe.whitelist()
def drop_status(name,date,remark):
	frappe.db.set_value("Social Media",name,"workflow_state","Drop")
	frappe.db.set_value("Social Media",name,"drop_date",date)
	frappe.db.set_value("Social Media",name,"remarks3",remark)
	frappe.db.set_value("Social Media",name,"dropped",1)

@frappe.whitelist()
def na_status(name,date,remark):
	frappe.db.set_value("Social Media",name,"workflow_state","Report Completed")
	frappe.db.set_value("Social Media",name,"check_completion_date",today())
	frappe.db.set_value("Social Media",name,"mark_na_on",date)
	frappe.db.set_value("Social Media",name,"remarks2",remark)
	frappe.db.set_value("Social Media",name,"na",1)

@frappe.whitelist()
def check_status(name,date,remark,user):
	frappe.db.set_value("Education Checks",name,"workflow_state","Drop")
	frappe.db.set_value("Education Checks",name,"drop_date",date)
	frappe.db.set_value("Education Checks",name,"remarks3",remark)
	frappe.db.set_value("Education Checks",name,"drop",1)
	frappe.db.set_value("Education Checks",name,"drop_marked_by",user)

@frappe.whitelist()
def app_state(name,date,remark):
	frappe.db.set_value("Education Checks",name,"workflow_state","Report Completed")
	frappe.db.set_value("Education Checks",name,"check_completion_date",today())
	frappe.db.set_value("Education Checks",name,"mark_na_on",date)
	frappe.db.set_value("Education Checks",name,"remarks2",remark)
	frappe.db.set_value("Education Checks",name,"na",1)

@frappe.whitelist()
def drop_value(name,date,remark):
	frappe.db.set_value("Reference Check",name,"workflow_state","Drop")
	frappe.db.set_value("Reference Check",name,"drop_date",date)
	frappe.db.set_value("Reference Check",name,"remarks3",remark)
	frappe.db.set_value("Reference Check",name,"drop",1)

@frappe.whitelist()
def na_value(name,date,remark):
	frappe.db.set_value("Reference Check",name,"workflow_state","Report Completed")
	frappe.db.set_value("Reference Check",name,"check_completion_date",today())
	frappe.db.set_value("Reference Check",name,"mark_na_on",date)
	frappe.db.set_value("Reference Check",name,"remarks2",remark)
	frappe.db.set_value("Reference Check",name,"na",1)



@frappe.whitelist()
def doc_mark(name,date,remark):
	frappe.db.set_value("Family",name,"workflow_state","Drop")
	frappe.db.set_value("Family",name,"drop_date",date)
	frappe.db.set_value("Family",name,"remarks3",remark)
	frappe.db.set_value("Family",name,"drop",1)

@frappe.whitelist()
def report_check(name,date,remark):
	frappe.db.set_value("Family",name,"workflow_state","Report Completed")
	frappe.db.set_value("Family",name,"check_completion_date",today())
	frappe.db.set_value("Family",name,"mark_na_on",date)
	frappe.db.set_value("Family",name,"remarks2",remark)
	frappe.db.set_value("Family",name,"na",1)

@frappe.whitelist()
def status_mark(name,date,remark):
	frappe.db.set_value("Identity Aadhar",name,"workflow_state","Drop")
	frappe.db.set_value("Identity Aadhar",name,"drop_date",date)
	frappe.db.set_value("Identity Aadhar",name,"remarks3",remark)
	frappe.db.set_value("Identity Aadhar",name,"drop",1)

@frappe.whitelist()
def na_applicable(name,date,remark):
	frappe.db.set_value("Identity Aadhar",name,"workflow_state","Report Completed")
	frappe.db.set_value("Identity Aadhar",name,"check_completion_date",today())
	frappe.db.set_value("Identity Aadhar",name,"mark_na_on",date)
	frappe.db.set_value("Identity Aadhar",name,"remarks2",remark)
	frappe.db.set_value("Identity Aadhar",name,"na",1)

@frappe.whitelist()
def document_state(name,date,remark):
	frappe.db.set_value("Employment",name,"workflow_state","Drop")
	frappe.db.set_value("Employment",name,"drop_date",date)
	frappe.db.set_value("Employment",name,"remarks3",remark)
	frappe.db.set_value("Employment",name,"drop",1)

@frappe.whitelist()
def state_report(name,date,remark):
	frappe.db.set_value("Employment",name,"workflow_state","Report Completed")
	frappe.db.set_value("Employment",name,"check_completion_date",today())
	frappe.db.set_value("Employment",name,"mark_na_on",date)
	frappe.db.set_value("Employment",name,"remarks2",remark)
	frappe.db.set_value("Employment",name,"na",1)

@frappe.whitelist()
def update_state(name,date,remark):
	frappe.db.set_value("Court",name,"workflow_state","Drop")
	frappe.db.set_value("Court",name,"drop_date",date)
	frappe.db.set_value("Court",name,"remarks3",remark)
	frappe.db.set_value("Court",name,"drop",1)

@frappe.whitelist()
def update_na(name,date,remark):
	frappe.db.set_value("Court",name,"workflow_state","Report Completed")
	frappe.db.set_value("Court",name,"check_completion_date",today())
	frappe.db.set_value("Court",name,"mark_na_on",date)
	frappe.db.set_value("Court",name,"remarks2",remark)
	frappe.db.set_value("Court",name,"na",1)
@frappe.whitelist()
def set_status(name,date,remark):
	frappe.db.set_value("Criminal",name,"workflow_state","Drop")
	frappe.db.set_value("Criminal",name,"drop_date",date)
	frappe.db.set_value("Criminal",name,"remarks3",remark)
	frappe.db.set_value("Criminal",name,"drop",1)

@frappe.whitelist()
def set_na(name,date,remark):
	frappe.db.set_value("Criminal",name,"workflow_state","Report Completed")
	frappe.db.set_value("Criminal",name,"check_completion_date",today())
	frappe.db.set_value("Criminal",name,"mark_na_on",date)
	frappe.db.set_value("Criminal",name,"remarks2",remark)
	frappe.db.set_value("Criminal",name,"na",1)

@frappe.whitelist()
def get_drop_status(name,date,remark):
	frappe.db.set_value("Address Check",name,"workflow_state","Drop")
	frappe.db.set_value("Address Check",name,"drop_date",date)
	frappe.db.set_value("Address Check",name,"remarks3",remark)
	frappe.db.set_value("Address Check",name,"drop",1)

@frappe.whitelist()
def get_ns_status(name,date,remark):
	frappe.db.set_value("Address Check",name,"workflow_state","Report Completed")
	frappe.db.set_value("Address Check",name,"check_completion_date",today())
	frappe.db.set_value("Address Check",name,"mark_na_on",date)
	frappe.db.set_value("Address Check",name,"remarks2",remark)
	frappe.db.set_value("Address Check",name,"na",1)

@frappe.whitelist()
def update_status_issue():
	# ta = frappe.db.sql("""select count(*) as count from `tabIssue` where  task = '' and status = "Resolved" """,as_dict = True)
	ta = frappe.db.count("Issue",{'task':"",'status':"Resolved"})
	print(ta)
	# task = frappe.db.sql("""select * from `tabIssue` where  task = '' and status = "Resolved" """,as_dict = True)
	# for i in task:
	# 	print(i.name)
		# if not frappe.db.exists("Task",{'issue':i.name}):
		# 	frappe.db.set_value("Issue",i.issue,"status","Closed")
				# if i.status == "Pending Review":
				# 	frappe.db.set_value("Issue",i.issue,"status","Resolved")
				# if i.status == "Completed":
				# 	frappe.db.set_value("Issue",i.issue,"status","Closed")

@frappe.whitelist()
def meeting_mom_mail(meet):
	data = ''
	meet_doc = frappe.get_doc("Meeting",meet)
	data += 'Dear Sir,<br><br>Kindly Find the below List of MOM points against the meeting happened at %s' % formatdate(meet_doc.date)
	for i in meet_doc.minutes:
		data += '<tr><td>%s . %s </td></tr>' % (i.idx,i.description)
	for j in meet_doc.attendees:
		frappe.sendmail(
			recipients=[j.attendee],
			message=data,
			subject=_("Minutes of Meeting -  %s on %s " %(meet_doc.title,formatdate(meet_doc.date))),
		)
	for j in meet_doc.persons_to_be_informed:
		frappe.sendmail(
			recipients=[j.attendee],
			message=data,
			subject=_("Minutes of Meeting -  %s on %s " %(meet_doc.title,formatdate(meet_doc.date))),
		)

@frappe.whitelist()
def update_insuff_days(date1,date2):
	date=(date_diff(date2,date1))
	return date

@frappe.whitelist()
def holidays(date1, date2):
	sql_query = f"""
		SELECT COUNT(*) 
		FROM `tabHoliday` 
		WHERE parent = 'TEAMPRO 2023 - Checkpro' 
		AND holiday_date BETWEEN '{date1}' AND '{date2}'
	"""

	count = frappe.db.sql(sql_query, as_list=True)[0][0]

	return count

@frappe.whitelist()
def tat_calculation(date1,date2,date3,date4,pac_tat):
	actual_tat=0
	tat = 0
	tat_monitor = ''
	date = 0
	dat = 0
	variation = 0
	doc=frappe.db.get_list("Case",["name","case_completion_date","case_status"])
	for i in doc:
		if i.case_completion_date:
			date=(date_diff(date2,date1))
			dat=(sum([int(date3),int(date4)]))
			actual_tat=date - dat
			variation = int(actual_tat)-int(pac_tat)

			if variation < 0:
				tat=0
				tat_monitor = "In TAT"
			else:
				tat=variation
				tat_monitor = "Out TAT"
	# frappe.errprint(date)
	# frappe.errprint(date3)
	frappe.errprint(date4)
	# frappe.errprint(dat)
	# frappe.errprint(variation)
	return actual_tat,tat,tat_monitor


# @frappe.whitelist()
# def update_att():
# 	att = frappe.db.sql("""delete from `tabAttendance` where name = "HR-ATT-2023-10801" """,as_dict = True)
# 	print(att)
# 	att = frappe.db.sql("""delete from `tabAttendance Request` where name = "HR-ARQ-23-11-00016" """,as_dict = True)
# 	print(att)
@frappe.whitelist()
def update_case_status(case):
	list = ["Education Checks","Family","Reference Check","Court","Social Media","Criminal","Employment","Identity Aadhar","Address Check"]
	case_sts=[]
	case_status=''
	# insuff=""
	for i in list:
		doc=frappe.get_all(i,{"case_id":case},["name","workflow_state","detailsof_insufficiency"])
		
		
		for j in doc:
			case_sts.append(j.workflow_state)
			if any(status == "Insufficient Data" for status in case_sts):
				if j.detailsof_insufficiency =="Entry":
					case_status="Entry-Insuff"
				if j.detailsof_insufficiency =="Execution":
					case_status="Execution-Insuff"
			elif all(status == "Entry Completed" for status in case_sts):
				case_status = "Entry Completed"
			elif all(status == "Entry QC Pending" for status in case_sts):
				case_status = "Entry-QC"
			elif all(status == "Execution Pending" for status in case_sts):
				case_status = "Execution"
			elif all(status == "Final QC Pending" for status in case_sts):
				case_status = "Final-QC"
			elif all(status == "Report Completed" for status in case_sts):
				case_status = "Generate Report"
			elif all(status == "Not Applicable" for status in case_sts):
				case_status = "Generate Report"
			elif all(status == "Drop" for status in case_sts):
				case_status = "Drop"
			elif any(status == "Draft" for status in case_sts):
				case_status = "Draft"
			elif any(status == "Entry Completed" for status in case_sts):
				case_status = "Entry Completed"
			elif any(status == "Entry QC Pending" for status in case_sts):
				case_status = "Entry-QC"
			elif any(status == "Entry QC Completed" for status in case_sts):
				case_status = "Entry-QC"
			elif any(status == "Execution Pending" for status in case_sts):
				case_status = "Execution"
			elif any(status == "Execution Completed" for status in case_sts):
				case_status = "Execution"
			elif any(status == "Final QC Pending" for status in case_sts):
				case_status = "Final-QC"
			elif any(status == "Final QC Completed" for status in case_sts):
				case_status = "Final-QC"
			
	frappe.db.set_value("Case",case,"case_status",case_status)


# @frappe.whitelist()
# def update_query():
# 	frappe.db.sql("""update `tabCase` set case_status = 'Generate Report' where name = 'CS-005392'""")

@frappe.whitelist()
def drop_case(case_id):
	list = ["Education Checks","Family","Reference Check","Court","Social Media","Criminal","Employment","Identity Aadhar","Address Check"]
	for i in list:
		checks=frappe.db.get_all(i,{"case_id":case_id},["name"])
		for j in checks:
			frappe.db.set_value(i,j.name,"workflow_state","Drop")
			frappe.db.set_value(i,j.name,"dropped_date",nowdate())

@frappe.whitelist()
def enqueue_check_status_update():
	from frappe.utils.background_jobs import enqueue
	filename = "5bba9ec645"
	enqueue(method=check_status_update, queue="long", timeout=6000, filename=filename)

def check_status_update(filename):
	from frappe.utils.file_manager import get_file
	# filename = frappe.get_value("File",{'file_url':fileurl},'name')
	filepath = get_file(filename)
	pps = read_csv_content(filepath[1])
	for pp in pps:
		if pp[0] == 'Check':
			pass
		else:
			if frappe.db.exists(pp[0],pp[1]):
				frappe.db.set_value(pp[0],pp[1],'workflow_state',pp[2])

# @frappe.whitelist()
# def create_sales_order(filename):
# 	print(filename)
# 	from frappe.utils.file_manager import get_file
# 	filepath = get_file(filename)
# 	# print(filepath)
# 	pps = read_csv_content(filepath[1])
# 	for pp in pps:
# 		if pp[0] == 'ID':
# 			pass
# 		else:
# 			so=frappe.db.get_all("Closure",{'name':pp[0]},['project','customer','task',"given_name",'mobile','payment','candidate_owner','sa_id','billing_currency','territory','associate','passport_no','expected_doj','account_manager','service','sa_id','associate_si','client_si','candidate_si'])
# 			for i in so:
# 				create_sale_order(pp[0],i.project,i.customer,i.task,i.given_name,i.mobile,i.payment,"",i.candidate_owner,i.sa_id,'',i.billing_currency,i.territory,i.associate,i.passport_no,i.expected_doj,i.candidate_owner,i.account_manager,i.service,i.sa_id,i.associate_si,i.client_si,i.candidate_si)

@frappe.whitelist()
def inactive_employee(doc,method):
	if doc.status=="Active":
		if doc.relieving_date:
			throw(_("Please remove the relieving date for the Active Employee."))

@frappe.whitelist()
def ops_mail(project):
	data = ''
	project_doc = frappe.get_doc("Project",project)
	data += 'New Project %s has been created  and Pending for Approval'%(project_doc.name)
	frappe.sendmail(
		recipients=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','sangeetha.a@groupteampro.com'],
		# recipients=["gifty.p@groupteampro.com"],
		message=data,
		subject=_("New Project Created -  %s" %(project_doc.project_name)),
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

# @frappe.whitelist()
# def update_lead():
# 	lead=frappe.get_all("Lead",{"website":('!=',''),'status':'Converted'},['*'])
# 	for i in lead:
# 		print(i.name)
# 		frappe.db.set_value("Lead",i.name,'website__',i.website)

@frappe.whitelist()
def update_batch_age():
	age=0
	doc=frappe.db.get_list("Case",["name","date_of_initiating","case_status"],order_by='date_of_initiating ASC')
	for i in doc:
		if i.case_status not in ("Completed","Case Report Completed","Drop","Generate Report with Insuff",'',"Drop"):
			if i.date_of_initiating:
				date=(date_diff(nowdate(),i.date_of_initiating))
				sql_query = f"""
					SELECT COUNT(*) 
					FROM `tabHoliday` 
					WHERE parent = 'TEAMPRO 2023 - Checkpro' 
					AND holiday_date BETWEEN '{i.date_of_initiating}' AND '{nowdate()}'
				"""
				count = frappe.db.sql(sql_query, as_list=True)[0][0]
				print(count)
				# print(type(count))
				print(date)
				# print(type(date))
				if count==0:
					age=date
				else:
					age = date-count
				print(i.name)
				print(age)
				if age > 15:
					cl = '#f50f0f'
				elif age >10:
					cl = '#EC864B'
				elif age >5:
					
					cl = '#449CF0'
				else:
					cl = '#000000'
				frappe.db.set_value("Case",i.name,"batch_age",age)
				print(cl)
				frappe.db.set_value("Case",i.name,"color",cl)

@frappe.whitelist()
def update_check_age():
	list = ["Education Checks","Family","Reference Check","Court","Social Media","Criminal","Employment","Identity Aadhar","Address Check"]
	age=0
	for i in list:
		doc=frappe.db.get_list(i,["name","check_creation_date","workflow_state"])
		for j in doc:
			if j.workflow_state not in ('Report Completed', '', 'Drop', 'Dropped', 'Not Applicable'):
				if j.check_creation_date:
					date=(date_diff(nowdate(),j.check_creation_date))
					sql_query = f"""
						SELECT COUNT(*) 
						FROM `tabHoliday` 
						WHERE parent = 'TEAMPRO 2023 - Checkpro' 
						AND holiday_date BETWEEN '{j.check_creation_date}' AND '{nowdate()}'
					"""
					count = frappe.db.sql(sql_query, as_list=True)[0][0]
					print(count)
					# print(type(count))
					print(date)
					# print(type(date))
					if count==0:
						age=date
					else:
						age = date-count
					print(j.name)
					print(i)
					frappe.db.set_value(i,j.name,"check_age",age)

@frappe.whitelist()
def get_workflow_state(doctype):
    doc = frappe.get_doc("Workflow", doctype)
    states = [state.state for state in doc.states]
    return states

@frappe.whitelist()
def update_lead_status(doc,method):
	if doc.status=="Lost":
		frappe.db.set_value("Lead", doc.party_name, {"disabled": 0, "docstatus": 0})

@frappe.whitelist()
def update_att():
	att = frappe.db.sql("""update `tabAttendance` set docstatus = 0  where attendance_date between "2023-12-01" and "2023-12-31" """)
	print(att)