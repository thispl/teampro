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
        cc=[taskid.spoc,taskid.custom_allocated_to],
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
                    taskid.project_manager, taskid.custom_allocated_to],
        cc=[taskid.spoc],
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
            "method": 'teampro.teampro.doctype.target_manager.target_manager.calculate_target',
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
        submit_spoc = frappe.db.count(
            'Candidate', {'task': doc.task, 'pending_for': 'Submit(SPOC)'}) or 0
        submit_client = frappe.db.count(
            'Candidate', {'task': doc.task, 'pending_for': 'Submitted(Client)'}) or 0
        psl = frappe.db.count('Candidate', {'task': doc.task, 'pending_for': (
            'in', ('Client Offered', 'Proposed PSL'))}) or 0
        shortlisted = frappe.db.count(
            'Candidate', {'task': doc.task, 'pending_for':'Shortlisted'}) or 0
        linedup = frappe.db.count(
            'Candidate', {'task': doc.task, 'pending_for': 'Linedup'}) or 0
        interviewed = frappe.db.count(
            'Candidate', {'task': doc.task, 'pending_for': 'Interviewed'}) or 0
        result_pending =frappe.db.count('Candidate',{'task':doc.task,'pending_for':'Result Pending'}) or 0
        # submit_interviewed=(submitted + interviewed)
        # frappe.errprint(submitted)
        frappe.db.set_value('Task', doc.task, 'psl', psl)
        frappe.db.set_value('Task', doc.task, 'fp',(submit_spoc + interviewed + submit_client))
        frappe.db.set_value('Task',doc.task,'custom_rp',result_pending)
        frappe.db.set_value('Task', doc.task, 'sl', shortlisted)
        frappe.db.set_value('Task', doc.task, 'custom_lp',linedup)

        task_status = frappe.db.get_value('Task', doc.task, 'status')

        if task_status in ('Completed', 'Cancelled'):
            # if pps == 0:
            frappe.db.set_value('Task', doc.task, 'sp', 0)

        else:
            vac = frappe.db.get_value('Task', doc.task, 'vac')
            prop = frappe.db.get_value('Task', doc.task, 'prop')
            pps = (vac - psl) * prop - (submit_spoc + submit_client+
                                        interviewed + shortlisted +linedup)
            frappe.db.set_value('Task', doc.task, 'sp', pps)

def update_candidate_tcount():
    tasks = frappe.get_all('Task',{'service':('in',('REC-I', 'REC-D'))})
    for task in tasks:
        # task = task.name
#         print(task)
        shortlisted = frappe.db.count('Candidate',{'task':task.name,'pending_for':'Shortlisted'}) or 0
        linedup = frappe.db.count('Candidate',{'task':task.name,'pending_for':'Linedup'}) or 0
        # interviewed = frappe.db.count('Candidate',{'task':task,'pending_for':'Interviewed'}) or 0
        print(task.name)
        print(shortlisted)
        print(linedup)
        frappe.db.sql(""" update `tabTask` set sl='%s' 
                    where name = '%s' """%(shortlisted,task.name),as_dict=True)
        # frappe.db.update('Task',task,'custom_lp',linedup)
        # frappe.db.update('Task',task,'fp',submitted + interviewed)
        # frappe.db.update('Task',task,'sl',shortlisted)

        # print([psl,submitted,interviewed,shortlisted,linedup])

        # task_status = frappe.db.get_value('Task',task,'status')
        # if task_status in ('Completed','Cancelled'):
        #     frappe.db.update('Task',task,'sp',0)
        # else:
        #     vac = frappe.db.get_value('Task',task,'vac')
        #     prop = frappe.db.get_value('Task',task,'prop')
        #     pps = (vac - psl) * prop - (submitted + interviewed + shortlisted + linedup)
        #     frappe.db.update('Task',task,'sp',pps)


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
    if isinstance(date_str, str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_obj =date_str
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


# @frappe.whitelist()
# def return_detailed_ts(timesheet):
    # timesheet = frappe.db.sql(""" select `tabTimesheet Detail`.task,`tabTimesheet Detail`.subject,`tabTimesheet Detail`.project,sum(`tabTimesheet Detail`.hours) as hours, GROUP_CONCAT(`tabTimesheet Detail`.description separator ', ') as description from `tabTimesheet`
    # left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where `tabTimesheet`.name = '%s' group by `tabTimesheet Detail`.task"""%(timesheet),as_dict = 1)
#     return timesheet
    
# @frappe.whitelist()
# def return_detailed_ts(timesheet):
#     task = frappe.db.sql(""" select `tabTimesheet Detail`.task,`tabTimesheet Detail`.subject,`tabTimesheet Detail`.project,sum(`tabTimesheet Detail`.hours) as hours, GROUP_CONCAT(`tabTimesheet Detail`.description separator ', ') as description from `tabTimesheet`
#     left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where `tabTimesheet Detail`.task is not null and `tabTimesheet`.name = '%s' group by `tabTimesheet Detail`.task"""%(timesheet),as_dict = 1)
#     # if time
#     meeting = frappe.db.sql(""" select `tabTimesheet Detail`.custom_meeting,`tabTimesheet Detail`.custom_subject_meeting, sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`
#     left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where `tabTimesheet Detail`.custom_meeting is not null and `tabTimesheet Detail`.task`tabTimesheet`.name = '%s' group by `tabTimesheet Detail`.custom_meeting"""%(timesheet),as_dict = 1)
#     issue = frappe.db.sql(""" select `tabTimesheet Detail`.custom_issue,`tabTimesheet Detail`.custom_subject_issue,`tabTimesheet Detail`.project,sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`
#     left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where tabTimesheet Detail`.custom_issue is not null and `tabTimesheet`.name = '%s' group by `tabTimesheet Detail`.custom_issue"""%(timesheet),as_dict = 1)
#     return task,meeting,issue
@frappe.whitelist()
def return_detailed_ts(timesheet):
    # Parameterized query for tasks
    task_query = """
        SELECT `tabTimesheet Detail`.task,
               `tabTimesheet Detail`.subject,
               `tabTimesheet Detail`.project,
               SUM(`tabTimesheet Detail`.hours) AS hours,
               GROUP_CONCAT(`tabTimesheet Detail`.description SEPARATOR ', ') AS description
        FROM `tabTimesheet`
        LEFT JOIN `tabTimesheet Detail` 
        ON `tabTimesheet`.name = `tabTimesheet Detail`.parent
        WHERE `tabTimesheet Detail`.task IS NOT NULL 
          AND `tabTimesheet`.name = %s
        GROUP BY `tabTimesheet Detail`.task
    """
    task = frappe.db.sql(task_query, (timesheet,), as_dict=True)
    
    # Parameterized query for meetings
    meeting_query = """
        SELECT `tabTimesheet Detail`.custom_meeting,
               `tabTimesheet Detail`.custom_subject_meeting,
               `tabTimesheet Detail`.project,
               SUM(`tabTimesheet Detail`.hours) AS hours
        FROM `tabTimesheet`
        LEFT JOIN `tabTimesheet Detail`
        ON `tabTimesheet`.name = `tabTimesheet Detail`.parent
        WHERE `tabTimesheet Detail`.custom_meeting IS NOT NULL 
          AND `tabTimesheet`.name = %s
        GROUP BY `tabTimesheet Detail`.custom_meeting
    """
    meeting = frappe.db.sql(meeting_query, (timesheet,), as_dict=True)
    
    # Parameterized query for issues
    issue_query = """
        SELECT `tabTimesheet Detail`.custom_issue,
               `tabTimesheet Detail`.custom_subject_issue,
               `tabTimesheet Detail`.project,
               SUM(`tabTimesheet Detail`.hours) AS hours
        FROM `tabTimesheet`
        LEFT JOIN `tabTimesheet Detail`
        ON `tabTimesheet`.name = `tabTimesheet Detail`.parent
        WHERE `tabTimesheet Detail`.custom_issue IS NOT NULL 
          AND `tabTimesheet`.name = %s
        GROUP BY `tabTimesheet Detail`.custom_issue
    """
    issue = frappe.db.sql(issue_query, (timesheet,), as_dict=True)
    
    return task, meeting, issue





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
    cb = frappe.db.get_value("Purchase Order",doc.name,['short_code'])
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

import bleach
from frappe.utils import strip
@frappe.whitelist()
def make_minutes_for_mom_points():
    args = frappe.local.form_dict
    filename = args.name
    test = build_xlsx_response_mom(filename)

def make_xlsx_mom(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name, 0)
    doc = frappe.get_doc("Meeting",args.name)
    if doc:
        ws.append(["Description","Action","Task"])
        for i in doc.minutes:
            description_without_html = bleach.clean(i.description, tags=[], strip=True)
            ws.append([description_without_html, i.custom_action, i.custom_id])
            # ws.append([i.description,i.custom_action,i.custom_id])
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file

def build_xlsx_response_mom(filename):
    xlsx_file = make_xlsx_mom(filename)
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
        emp = ["TI00150","TI00149"]
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
        "cron_format": '00 9 * * *'
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
    frappe.errprint("inside of method")
    if doc.service == 'IT-SW':
        frappe.errprint("inside of if")
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
                frappe.errprint("hi")
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
        cb = frappe.get_value("Employee",{'user_id':doc.custom_allocated_to},['short_code'])
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
                date=(date_diff(date2,date1))+1
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
    frappe.db.set_value("Case",name,"case_report","Drop")  

@frappe.whitelist()
def drop_status(name,date,remark):
    frappe.db.set_value("Social Media",name,"workflow_state","Drop")
    frappe.db.set_value("Social Media",name,"check_status","Drop")
    frappe.db.set_value("Social Media",name,"drop_date",date)
    frappe.db.set_value("Social Media",name,"remarks3",remark)
    frappe.db.set_value("Social Media",name,"dropped",1)
    frappe.db.set_value("Social Media",name,"report_status","Drop")

@frappe.whitelist()
def na_status(name,date,remark):
    frappe.db.set_value("Social Media",name,"workflow_state","Report Completed")
    frappe.db.set_value("Social Media",name,"check_completion_date",today())
    frappe.db.set_value("Social Media",name,"mark_na_on",date)
    frappe.db.set_value("Social Media",name,"remarks2",remark)
    frappe.db.set_value("Social Media",name,"na",1)
    frappe.db.set_value("Social Media",name,"report_status","Not Applicable")

@frappe.whitelist()
def check_status(name,date,remark):
    frappe.db.set_value("Education Checks",name,"workflow_state","Drop")
    frappe.db.set_value("Education Checks",name,"check_status","Drop")
    frappe.db.set_value("Education Checks",name,"drop_date",date)
    frappe.db.set_value("Education Checks",name,"remarks3",remark)
    frappe.db.set_value("Education Checks",name,"drop",1)
    frappe.db.set_value("Education Checks",name,"report_status","Drop")

@frappe.whitelist()
def app_state(name,date,remark):
    frappe.db.set_value("Education Checks",name,"workflow_state","Report Completed")
    frappe.db.set_value("Education Checks",name,"check_completion_date",today())
    frappe.db.set_value("Education Checks",name,"mark_na_on",date)
    frappe.db.set_value("Education Checks",name,"remarks2",remark)
    frappe.db.set_value("Education Checks",name,"na",1)
    frappe.db.set_value("Education Checks",name,"report_status","Not Applicable")

@frappe.whitelist()
def drop_value(name,date,remark):
    frappe.db.set_value("Reference Check",name,"workflow_state","Drop")
    frappe.db.set_value("Reference Check",name,"check_status","Drop")
    frappe.db.set_value("Reference Check",name,"drop_date",date)
    frappe.db.set_value("Reference Check",name,"remarks3",remark)
    frappe.db.set_value("Reference Check",name,"drop",1)
    frappe.db.set_value("Reference Check",name,"report_status","Drop")

@frappe.whitelist()
def na_value(name,date,remark):
    frappe.db.set_value("Reference Check",name,"workflow_state","Report Completed")
    frappe.db.set_value("Reference Check",name,"check_completion_date",today())
    frappe.db.set_value("Reference Check",name,"mark_na_on",date)
    frappe.db.set_value("Reference Check",name,"remarks2",remark)
    frappe.db.set_value("Reference Check",name,"na",1)
    frappe.db.set_value("Reference Check",name,"report_status","Not Applicable")




@frappe.whitelist()
def doc_mark(name,date,remark):
    frappe.db.set_value("Family",name,"workflow_state","Drop")
    frappe.db.set_value("Family",name,"check_status","Drop")
    frappe.db.set_value("Family",name,"drop_date",date)
    frappe.db.set_value("Family",name,"remarks3",remark)
    frappe.db.set_value("Family",name,"drop",1)
    frappe.db.set_value("Family",name,"report_status","Drop")

@frappe.whitelist()
def report_check(name,date,remark):
    frappe.db.set_value("Family",name,"workflow_state","Report Completed")
    frappe.db.set_value("Family",name,"check_completion_date",today())
    frappe.db.set_value("Family",name,"mark_na_on",date)
    frappe.db.set_value("Family",name,"remarks2",remark)
    frappe.db.set_value("Family",name,"na",1)
    frappe.db.set_value("Family",name,"report_status","Not Applicable")


@frappe.whitelist()
def status_mark(name,date,remark):
    frappe.db.set_value("Identity Aadhar",name,"workflow_state","Drop")
    frappe.db.set_value("Identity Aadhar",name,"check_status","Drop")
    frappe.db.set_value("Identity Aadhar",name,"drop_date",date)
    frappe.db.set_value("Identity Aadhar",name,"remarks3",remark)
    frappe.db.set_value("Identity Aadhar",name,"drop",1)
    frappe.db.set_value("Identity Aadhar",name,"report_status","Drop")

@frappe.whitelist()
def na_applicable(name,date,remark):
    frappe.db.set_value("Identity Aadhar",name,"workflow_state","Report Completed")
    frappe.db.set_value("Identity Aadhar",name,"check_completion_date",today())
    frappe.db.set_value("Identity Aadhar",name,"mark_na_on",date)
    frappe.db.set_value("Identity Aadhar",name,"remarks2",remark)
    frappe.db.set_value("Identity Aadhar",name,"na",1)
    frappe.db.set_value("Identity Aadhar",name,"report_status","Not Applicable")


@frappe.whitelist()
def document_state(name,date,remark):
    frappe.db.set_value("Employment",name,"workflow_state","Drop")
    frappe.db.set_value("Employment",name,"check_status","Drop")
    frappe.db.set_value("Employment",name,"drop_date",date)
    frappe.db.set_value("Employment",name,"remarks3",remark)
    frappe.db.set_value("Employment",name,"drop",1)
    frappe.db.set_value("Employment",name,"report_status","Drop")

@frappe.whitelist()
def state_report(name,date,remark):
    frappe.db.set_value("Employment",name,"workflow_state","Report Completed")
    frappe.db.set_value("Employment",name,"check_completion_date",today())
    frappe.db.set_value("Employment",name,"mark_na_on",date)
    frappe.db.set_value("Employment",name,"remarks2",remark)
    frappe.db.set_value("Employment",name,"na",1)
    frappe.db.set_value("Employment",name,"report_status","Not Applicable")


@frappe.whitelist()
def update_state(name,date,remark):
    frappe.db.set_value("Court",name,"workflow_state","Drop")
    frappe.db.set_value("Court",name,"check_status","Drop")
    frappe.db.set_value("Court",name,"drop_date",date)
    frappe.db.set_value("Court",name,"remarks3",remark)
    frappe.db.set_value("Court",name,"drop",1)
    frappe.db.set_value("Court",name,"report_status","Drop")

@frappe.whitelist()
def update_na(name,date,remark):
    frappe.db.set_value("Court",name,"workflow_state","Report Completed")
    frappe.db.set_value("Court",name,"check_completion_date",today())
    frappe.db.set_value("Court",name,"mark_na_on",date)
    frappe.db.set_value("Court",name,"remarks2",remark)
    frappe.db.set_value("Court",name,"na",1)
    frappe.db.set_value("Court",name,"report_status","Not Applicable")

@frappe.whitelist()
def set_status(name,date,remark):
    frappe.db.set_value("Criminal",name,"workflow_state","Drop")
    frappe.db.set_value("Criminal",name,"check_status","Drop")
    frappe.db.set_value("Criminal",name,"drop_date",date)
    frappe.db.set_value("Criminal",name,"remarks3",remark)
    frappe.db.set_value("Criminal",name,"drop",1)
    frappe.db.set_value("Criminal",name,"report_status","Drop")

@frappe.whitelist()
def set_na(name,date,remark):
    frappe.db.set_value("Criminal",name,"workflow_state","Report Completed")
    frappe.db.set_value("Criminal",name,"check_completion_date",today())
    frappe.db.set_value("Criminal",name,"mark_na_on",date)
    frappe.db.set_value("Criminal",name,"remarks2",remark)
    frappe.db.set_value("Criminal",name,"na",1)
    frappe.db.set_value("Criminal",name,"report_status","Not Applicable")


@frappe.whitelist()
def get_drop_status(name,date,remark):
    frappe.db.set_value("Address Check",name,"workflow_state","Drop")
    frappe.db.set_value("Address Check",name,"check_status","Drop")
    frappe.db.set_value("Address Check",name,"drop_date",date)
    frappe.db.set_value("Address Check",name,"remarks3",remark)
    frappe.db.set_value("Address Check",name,"drop",1)
    frappe.db.set_value("Address Check",name,"report_status","Drop")

@frappe.whitelist()
def get_ns_status(name,date,remark):
    frappe.db.set_value("Address Check",name,"workflow_state","Report Completed")
    frappe.db.set_value("Address Check",name,"check_completion_date",today())
    frappe.db.set_value("Address Check",name,"mark_na_on",date)
    frappe.db.set_value("Address Check",name,"remarks2",remark)
    frappe.db.set_value("Address Check",name,"na",1)
    frappe.db.set_value("Address Check",name,"report_status","Not Applicable")


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
    sql_query = f"""
        SELECT COUNT(*) 
        FROM `tabHoliday` 
        WHERE parent = 'TEAMPRO 2023 - Checkpro' 
        AND holiday_date BETWEEN '{date1}' AND '{date2}'
    """
    count = frappe.db.sql(sql_query, as_list=True)[0][0]
    frappe.errprint(count)
    frappe.errprint(date)
    date1 = (date-count)+1
    return date1

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
            date=(date_diff(date2,date1))+1
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
            frappe.errprint(i)
            case_sts.append(j.workflow_state)
            if any(status == "Insufficient Data" for status in case_sts):
                if j.detailsof_insufficiency =="Entry":
                    case_status="Entry-Insuff"
                if j.detailsof_insufficiency =="Execution":
                    case_status="Execution-Insuff"
            elif all(status == "Entry Completed" for status in case_sts):
                case_status = "Entry Completed"
                frappe.db.set_value("Case",case,"date_of_entry_completion",frappe.utils.now())
            elif all(status == "Entry QC Pending" for status in case_sts):
                case_status = "Entry-QC"
            elif all(status == "Execution Initiated" for status in case_sts):
                case_status = "Execution"
            elif all(status == "Execution Pending" for status in case_sts):
                case_status = "Execution"
            elif all(status == "Final QC Pending" for status in case_sts):
                case_status = "Final-QC"
            elif all(status == "Report Completed" for status in case_sts):
                case_status = "Generate Report"
                frappe.db.set_value("Case",case,"date_of_execution_completion",frappe.utils.now())
                frappe.db.set_value("Case",case,"date_of_final_qc_completion",frappe.utils.now())
                frappe.db.set_value("Case",case,"date_of_generate_report",frappe.utils.now())
            elif all(status == "Not Applicable" for status in case_sts):
                case_status = "Generate Report"
            elif all(status == "Drop" for status in case_sts):
                case_status = "Drop"
            elif any(status == "Draft" for status in case_sts):
                case_status = "Draft"
            elif any(status == "Entry Completed" for status in case_sts):
                case_status = "Entry Completed"
                frappe.db.set_value("Case",case,"date_of_entry_completion",frappe.utils.now())
            elif any(status == "Entry QC Pending" for status in case_sts):
                case_status = "Entry-QC"
            elif any(status == "Entry QC Completed" for status in case_sts):
                case_status = "Entry-QC"
                frappe.db.set_value("Case",case,"date_of_entry_completion",frappe.utils.now())
                frappe.db.set_value("Case",case,"date_of_entry_qc_completion",frappe.utils.now())
            elif any(status == "Execution Initiated" for status in case_sts):
                case_status = "Execution"
            elif any(status == "Execution Pending" for status in case_sts):
                case_status = "Execution"
            elif any(status == "Execution Completed" for status in case_sts):
                case_status = "Execution"
                frappe.db.set_value("Case",case,"date_of_execution_completion",frappe.utils.now())
            elif any(status == "Final QC Pending" for status in case_sts):
                case_status = "Final-QC"
            elif any(status == "Final QC Completed" for status in case_sts):
                case_status = "Final-QC"
                frappe.db.set_value("Case",case,"date_of_final_qc_completion",frappe.utils.now())
    frappe.errprint(case_status)
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

@frappe.whitelist()
def case_report_update(filename):
    print(filename)
    from frappe.utils.file_manager import get_file
    filepath = get_file(filename)
    print(filepath)
    pps = read_csv_content(filepath[1])
    # for pp in pps:
    # 	if pp[0] == 'ID':
    # 		pass
    # 	else:
    # 		so=frappe.db.get_all("Closure",{'name':pp[0]},['project','customer','task',"given_name",'mobile','payment','candidate_owner','sa_id','billing_currency','territory','associate','passport_no','expected_doj','account_manager','service','sa_id','associate_si','client_si','candidate_si'])
    # 		for i in so:
    # 			create_sale_order(pp[0],i.project,i.customer,i.task,i.given_name,i.mobile,i.payment,"",i.candidate_owner,i.sa_id,'',i.billing_currency,i.territory,i.associate,i.passport_no,i.expected_doj,i.candidate_owner,i.account_manager,i.service,i.sa_id,i.associate_si,i.client_si,i.candidate_si)

@frappe.whitelist()
def case_status_update_from_csv(filename):
    print(filename)
    from frappe.utils.file_manager import get_file
    filepath = get_file(filename)
    print(filepath)
    pps = read_csv_content(filepath[1])
    i=1
    for pp in pps:
        if pp[0] != 'ID':
            i+=1
            print(pp[0])
            # frappe.db.sql("""update `tabCase` set case_status = %s where name = %s""",(pp[1],pp[0]))
            # frappe.db.sql("""delete from `tabEmployment` where name = %s""",(pp[0]),as_dict=True)

    print(i)

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
    tat_var=0
    tat_mon=''
    tat_sts=''
    doc=frappe.db.get_list("Batch",["name","expected_start_date","batch_status",'package_tat'])
    for i in doc:
        if i.batch_status not in ("Completed",'',"Drop",'Proposed SO'):
            if i.expected_start_date:
                date=(date_diff(nowdate(),i.expected_start_date))+1
                sql_query = f"""
                    SELECT COUNT(*) 
                    FROM `tabHoliday` 
                    WHERE parent = 'TEAMPRO 2023 - Checkpro' 
                    AND holiday_date BETWEEN '{i.expected_start_date}' AND '{nowdate()}'
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
                tat_var=i.package_tat-age
                if tat_var>0:
                    tat_mon='In TAT'
                else:
                    tat_mon='Out TAT'
                if age<(0.4*i.package_tat):
                    tat_sts='Regular'
                elif age<(0.65*i.package_tat):
                    tat_sts='Critical'
                else:
                    tat_sts='Most Critical'
                frappe.db.set_value("Batch",i.name,"actual_tat",age)
                frappe.db.set_value("Batch",i.name,"custom_holidays",count)
                frappe.db.set_value("Batch",i.name,"tat_variation",tat_var)
                frappe.db.set_value("Batch",i.name,"tat__monitor",tat_mon)
                frappe.db.set_value("Batch",i.name,"custom_tat_status",tat_sts)

def create_update_cv_age():
    job = frappe.db.exists('Scheduled Job Type', 'update_cv_age')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'teampro.custom.update_cv_age',
            "frequency": 'Cron',
            "cron_format": '00 06 * * *'
        })
        sjt.save(ignore_permissions=True)

@frappe.whitelist()
def update_case_age():
    age=0
    tat_var=0
    tat_mon=''
    tat_sts=''
    doc=frappe.db.get_list("Case",["name","date_of_initiating","case_status",'insufficiency_days','package_tat'],order_by='date_of_initiating ASC')
    for i in doc:
        if i.case_status not in ("Case Completed","Drop","Generate Report with Insuff",'',"Drop"):
            if i.date_of_initiating:
                date=(date_diff(nowdate(),i.date_of_initiating))+1
                sql_query = f"""
                    SELECT COUNT(*) 
                    FROM `tabHoliday` 
                    WHERE parent = 'TEAMPRO 2023 - Checkpro' 
                    AND holiday_date BETWEEN '{i.date_of_initiating}' AND '{nowdate()}'
                """
                count = frappe.db.sql(sql_query, as_list=True)[0][0]
                if count==0:
                    age=date-i.insufficiency_days
                else:
                    age = (date-(count+i.insufficiency_days))
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
                tat_var=i.package_tat-age
                if tat_var>0:
                    tat_mon='In TAT'
                else:
                    tat_mon='Out TAT'
                if age<(0.4*i.package_tat):
                    tat_sts='Regular'
                elif age<(0.65*i.package_tat):
                    tat_sts='Critical'
                else:
                    tat_sts='Most Critical'
                frappe.db.set_value("Case",i.name,"actual_tat",age)
                print(cl)
                frappe.db.set_value("Case",i.name,"color",cl)
                frappe.db.set_value("Case",i.name,"holidays",count)
                frappe.db.set_value("Case",i.name,"tat_variation",tat_var)
                frappe.db.set_value("Case",i.name,"tat_monitor",tat_mon)
                frappe.db.set_value("Case",i.name,"custom_tat_status",tat_sts)

def create_update_case_age():
    job = frappe.db.exists('Scheduled Job Type', 'update_case_age')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'teampro.custom.update_case_age',
            "frequency": 'Cron',
            "cron_format": '00 07 * * *'
        })
        sjt.save(ignore_permissions=True)


@frappe.whitelist()
def update_check_age():
    list = ["Education Checks","Employment","Address Check","Criminal","Reference Check","Court","Identity Aadhar","Family","Social Media"]
    
    age=0
    tat_var=0
    tat_mon=''
    tat_sts=''
    for i in list:
        doc=frappe.db.get_list(i,["name","check_creation_date","workflow_state",'package_tat','insufficiency_days'])
        for j in doc:
            if j.workflow_state not in ('Report Completed', '', 'Drop', 'Dropped', 'Not Applicable'):
                if j.check_creation_date:
                    date=(date_diff(nowdate(),j.check_creation_date))+1
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
                        age=date-j.insufficiency_days
                    else:
                        age = date-(count+j.insufficiency_days)
                    tat_var=int(j.package_tat)-age
                    if tat_var>0:
                        tat_mon='In TAT'
                    else:
                        tat_mon='Out TAT'
                    if age<(0.4*int(j.package_tat)):
                        tat_sts='Regular'
                    elif age<(0.65*int(j.package_tat)):
                        tat_sts='Critical'
                    else:
                        tat_sts='Most Critical'
                    print(j.name)
                    print(i)
                    frappe.db.set_value(i,j.name,"actual_tat",age)
                    frappe.db.set_value(i,j.name,"holidays",count)
                    frappe.db.set_value(i,j.name,"tat_variation",tat_var)
                    frappe.db.set_value(i,j.name,"tat_monitor",tat_mon)
                    frappe.db.set_value(i,j.name,"custom_tat_status",tat_sts)

def update_cv_age():
    age=0
    ind=0
    cand=0
    doc=frappe.db.get_list("Candidate",{"pending_for":("not in",['IDB','Sourced','Proposed PSL'])},["name","source","submitted_date"],)
    for i in doc:
        cand+=1
        if i.submitted_date:
            ind+=1
            age=(date_diff(nowdate(),i.submitted_date))
            print(date)
            print(i.name)
            print(age)
            frappe.db.set_value("Candidate",i.name,"age_of_cv",age)



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

@frappe.whitelist()
def update_mandatory(doctype,status):
    settings = frappe.get_doc("Checkpro Settings")
    key_value_pairs_list = []

    for child in settings.get("settings"):
        if child.check_type == doctype and child.status == status:
            reqd_fields = child.mandatory_fields
            field_list = reqd_fields.split(',')
            for field in field_list:
                key, value = field.split('-')
                key = key.strip()
                value = value.strip()
                key_value_pairs_list.append({key: value})

    return key_value_pairs_list

@frappe.whitelist()
def update_meeting_id(meet):
    meeting=frappe.get_doc("Meeting",meet)
    for i in meeting.minutes:
        if i.custom_action == "Task":
            frappe.db.set_value("Task",i.custom_id,'custom_meeting_id',meet)
        elif i.custom_action == "To Do":
            frappe.db.set_value("ToDo",i.custom_id,'custom_meeting_id',meet)

from frappe import _

@frappe.whitelist()
def meeting_mail(meet):
    meet_doc = frappe.get_doc("Meeting",meet)
    data = '<table border="1" width="100%" style="border-collapse: collapse;">'
    data += '''
<tr style="background-color: #063970;">
    <td width="5%" style="text-align:center;">S.No</td>
    <td width="75%" style="text-align:center;">Description</td>
    <td width="10%" style="text-align:center;">Action</td>
    <td width="10%" style="text-align:center;">ID</td>
</tr>
'''

    ind = 1
    recipients = []
    cc = []
    for i in meet_doc.minutes:
        data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(ind, i.description, i.custom_action or '', i.custom_id)
        ind += 1
    data += '</table>'
    for j in meet_doc.attendees:
        if j.attended == '1':
            recipients.append(j.attendee)
        else:
            cc.append(j.attendee)
    frappe.sendmail(
        recipients=recipients,
        cc=cc,
        subject=_("Minutes of Meeting -  %s on %s " % (meet_doc.title, formatdate(meet_doc.date))),
        message="""
            Dear Sir/Madam,<br>Kindly Find the below List of MOM points against the meeting happened at {} {}<br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
            """.format(formatdate(meet_doc.date), data)
    )
    return "Ok"


@frappe.whitelist()
def get_task_details(name):
    data = ''
    data += "<table width=100% style='border:1px solid black' ><tr><td colspan=6 style='text-align:center;background-color:#009dd1;font-size:17px;border:1px solid black'><b>Task Details</b></td></tr>"
    data += "<tr style='font-size:17px;border:1px solid black'><td style='border:1px solid black'><b>Position</b></td><td style='border:1px solid black'><b># Vac</b></td><td style='border:1px solid black'><b># SP</b></td><td style='border:1px solid black'><b># FP</b></td><td style='border:1px solid black'><b>#SL</b></td><td style='border:1px solid black'><b>#PSL</b></td>"
    
    tasks = frappe.get_all("Task",{"project":name},['*'])
    for i in tasks:
        data += "<tr style='font-size:17px'><td style='border:1px solid black'>%s - %s</td><td style='border:1px solid black'>%s</td><td style='border:1px solid black'>%s</td><td style='border:1px solid black'>%s</td><td style='border:1px solid black'>%s</td><td style='border:1px solid black'>%s</td></tr>"%(i.name,i.subject,i.vac,i.sp,i.fp,i.sl,i.psl)
    data += "</table>"
    return data

# @frappe.whitelist()
# def update_att():
# 	att = frappe.db.sql("""
# 		UPDATE `tabClosure`
# 		SET visa_status = "Visa Received"
# 		WHERE name = "CL02458"
# 	""")
# 	print(att)




@frappe.whitelist(allow_guest=True)
def val_pass(passcode,email):	
    if frappe.db.exists("BG Entry Passcode",{'passcode':passcode,'email_id':email}):
        frappe.errprint("Hi")
        return "Yes"
    else:
        return "No"
    
@frappe.whitelist(allow_guest=True)
def submission_mail(email,name):
    frappe.sendmail(
        recipients=['anil.p@groupteampro.com'],
        subject=_("Proceed BGV"),
        message="""
            Dear Sir/madam,<br>Candidate %s with the Email ID %s has been applied for BGV. Kindly initate the BGV<br><br><br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
            """%(name, email)

        )
@frappe.whitelist(allow_guest=True)
def submission_mail2(email,name):
    frappe.sendmail(
        recipients=['anil.p@groupteampro.com'],
        subject=_("Applied for BGV"),
        message="""
            Dear ,<br>Candidate %s with the Email ID %s has submitted the documents successfully. BGV initiated for the Candidate<br><br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
            """%(name,email)
        )

@frappe.whitelist()
def update_pi_workflow(doc,method):
    pi=frappe.get_all("Purchase Invoice",{'sales_order':doc.name},['workflow_state','name'])
    for i in pi:
        frappe.db.sql("update `tabPurchase Invoice` set workflow_state='Cancelled' where name=%s",(i.name))

@frappe.whitelist()
def check_supplier(supplier):
    supp=frappe.get_doc("Supplier",supplier)
    if supp.custom_is_lead == 1:
        return "OK"
    
@frappe.whitelist()
def update_workflow_state(doc,method):
    if doc.workflow_state:
        frappe.db.sql("""update `tabPurchase Invoice` set custom_status = %s where name = %s""",(doc.workflow_state,doc.name))

@frappe.whitelist()
def update_bg_entry():
    
    frappe.db.sql("""update `tabEmployment` set entry_allocation_date = '2024-03-21' where name = 'Employment-2500'""")


def send_closure_report_with_table():
    filename = "Closure_" + today()
    xlsx_file = build_xlsx_response_closure(filename)
    html_table, total_count = closure_next_action()
    if total_count > 0:
        send_mail_with_attachment_and_html(filename, xlsx_file.getvalue(), html_table)

def send_mail_with_attachment_and_html(filename, file_content, html_table):
    subject = "DND DPR - %s" % nowdate()
    message = (
        "Dear Sir/Madam,<br>"
        "Please find attached the attached Report based on Next Action.<br><br>"
        + html_table +
        "<br>Thanks & Regards,<br>TEAM ERP<br>"
        "This email has been automatically generated. Please do not reply"
    )
    attachments = [{"fname": filename + '.xlsx', "fcontent": file_content}]
    frappe.sendmail(
        # recipients=['jeniba.a@groupteampro.com'],
        recipients=['dc@groupteampro.com','jeniba.a@groupteampro.com','divya.p@groupteampro.com'],
        cc=['sangeetha.a@groupteampro.com','sangeetha.s@groupteampro.com','dineshbabu.k@groupteampro.com'],
        sender=None,
        subject=subject,
        message=message,
        attachments=attachments,
    )

def build_xlsx_response_closure(filename):
    return make_xlsx_closure(filename)

def make_xlsx_closure(filename, sheet_name=None, wb=None, column_widths=None):
    action = add_days(nowdate(), 1)
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name or filename, 0)  
    default_column_widths = [15, 25, 25, 15, 25, 20]
    column_widths = column_widths or default_column_widths    
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width  
    header_fill = PatternFill(start_color="87CEFA", end_color="87CEFA", fill_type="solid")
    ws.append(["ID", "Candidate Name", "Customer", "Status", "Next Action", "Remark", "Next Action Date"])
    for cell in ws[1]: 
        cell.fill = header_fill
    closures = frappe.get_all("Closure", {"custom_next_follow_up_on":action,'status':["Not In", ['Onboarded','Dropped']]}, ['*'])
    if closures:
        for closure in closures:
            ws.append([closure.name, closure.given_name, closure.customer, closure.status, closure.std_remarks, closure.remark, closure.custom_next_follow_up_on])
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)    
    return xlsx_file

def closure_next_action():
    action_date = add_days(nowdate(), 1)
    closures = frappe.get_all("Closure", {"custom_next_follow_up_on": action_date,'status':("Not In", ['Onboarded','Dropped'])}, ["customer", "status"])
    customer_status_count = {}
    for closure in closures:
        customer = closure.customer
        status = closure.status
        if customer not in customer_status_count:
            customer_status_count[customer] = {}
        if status not in customer_status_count[customer]:
            customer_status_count[customer][status] = 0
        customer_status_count[customer][status] += 1
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: center;">'
    table += '<tr style="background-color: #87CEFA"><td style="width: 45%; font-weight: bold; text-align: center;">Customer</td><td style="width: 30%; font-weight: bold; text-align: center;">Status</td><td style="width: 25%; font-weight: bold; text-align: center;">Count</td></tr>'
    for customer, statuses in customer_status_count.items():
        total_counts = sum(statuses.values())
        table += '<tr><td><b>%s</b></td><td></td><td><b>%s</b></td></tr>' % (customer, total_counts)        
        for status, count in statuses.items():
            table += '<tr><td></td><td>%s</td><td>%s</td></tr>' % (status, count)
    table += '</table>'
    total_count = sum(sum(status.values()) for status in customer_status_count.values())
    return table, total_count

@frappe.whitelist()
def create_mail_for_dnd_dpr():
    job = frappe.db.exists('Scheduled Job Type', 'send_closure_report_with_table')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'teampro.custom.send_closure_report_with_table',
            "frequency": 'Cron',
            "cron_format": '30 18 * * *'
        })
        sjt.save(ignore_permissions=True) 


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
        recipients=["dineshbabu.k@groupteampro.com","sangeetha.a@groupteampro.com","sangeetha.s@groupteampro.com","annie.m@groupteampro.com","vijiyalakshmi.k@groupteampro.com"],
        # recipients=["divya.p@groupteampro.com"],
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
    headers = ["SI NO", "CUSTOMER/PROJECT NAME", "Project Priority", "AM Remark", "PM Remark", 'Expected Value', 'Expected PSL', 'Sourcing Status', 'Territory', 'TASK', 'Task Priority', '#VAC', '#SP', '#FP', '#SL', '#PSL', '#LP']
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
                pdata.append([p['project_name'] if p['project_name'] else "",p['priority'] if p['priority'] else "",p['remark'] if p['remark'] else "",p['account_manager_remark'] if p['account_manager_remark'] else "",p['expected_value'] if p['expected_value'] else "",p['expected_psl'] if p['expected_psl'] else "",p['sourcing_statu'] if p['sourcing_statu'] else "",p['territory'] if p['territory'] else "",t['subject'],t['priority'],t['vac'],t['sp'],t['fp'],t['sl'],t['psl'],t['custom_lp']])
                task_totals['vac'] +=t['vac']
                task_totals['sp'] +=t['sp']
                task_totals['fp']+= t['fp']
                task_totals['sl'] +=t['sl']
                task_totals['psl'] += t['psl']
                task_totals['custom_lp'] += t['custom_lp']
            project_data.append({
                'project_name': p['project_name'],'priority': p['priority'],
                'remark': p['remark'],'account_manager_remark': p['account_manager_remark'],'sourcing_statu': p['sourcing_statu'],'territory': p['territory'],
                'expected_value': p['expected_value'],'expected_psl': p['expected_psl'],'tasks': pdata})
        blue_fill = PatternFill(start_color="98d7f5", end_color="98d7f5", fill_type="solid")
        row_data = [serial_number, c['name']] + [""] * 9 + [task_totals['vac'], task_totals['sp'], task_totals['fp'], task_totals['sl'], task_totals['psl'],task_totals['custom_lp']]
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


@frappe.whitelist()
def create_mail_for_project_report():
    job = frappe.db.exists('Scheduled Job Type', 'send_project_report')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'teampro.custom.send_project_report',
            "frequency": 'Cron',
            "cron_format": '00 19 * * *'
        })
        sjt.save(ignore_permissions=True) 



@frappe.whitelist()
def update_check_box(check,name):
    candidate=frappe.get_all("Candidate",{"task":name},["name"])
    for i in candidate:
        if check=='1':
            frappe.db.set_value("Candidate",i.name,"custom_experience_and_education_certificates_required",check)
        else:
            frappe.db.set_value("Candidate",i.name,"custom_experience_and_education_certificates_required",check)

@frappe.whitelist()
def update_check_box_mask(check,name):
    candidate=frappe.get_all("Candidate",{"task":name},["name"])
    for i in candidate:
        if check=='1':
            frappe.db.set_value("Candidate",i.name,"custom_non_masked_cvs",check)
        else:
            frappe.db.set_value("Candidate",i.name,"custom_non_masked_cvs",check)

@frappe.whitelist()
def update_check_box_in_task(check,name):
    tasks=frappe.get_all("Task",{"project":name},["name"])
    for i in tasks:
        if check=='1':
            frappe.db.set_value("Task",i.name,"custom_experience_and_education_certificates_required",check)
        else:
            frappe.db.set_value("Task",i.name,"custom_experience_and_education_certificates_required",check)

@frappe.whitelist()
def update_check_box_task_mask(check,name):
    candidate=frappe.get_all("Task",{"project":name},["name"])
    for i in candidate:
        if check=='1':
            frappe.db.set_value("Task",i.name,"custom_non_masked_cvs",check)
        else:
            frappe.db.set_value("Task",i.name,"custom_non_masked_cvs",check)



# def validate_date1():
#     doc=frappe.get_doc("Purchase Invoice",'ACC-PINV-2024-00498')
#     current_date = datetime.now().date()
#     date_str = doc.posting_date
#     print(type(current_date))
#     date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
#     print(type(date_obj))
#     # if date_str < current_date:
#         throw(_("Submitting the Purchase Invoice on back date will have impact on the GST .Please click on the 'Edit Posting Date' and change the Date to Today."))


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff,format_datetime
from datetime import date, timedelta, datetime, time
from frappe.utils import (
    add_days,
    cstr,
    flt,
    format_datetime,
    formatdate,
    get_datetime,
    get_first_day,
    get_last_day,
    get_link_to_form,
    get_number_format_info,
    getdate,
    nowdate,
    today,
)
def ep_mail():
    first_date=get_first_day(add_days(today(),-1))
    last_date=get_last_day(add_days(today(),-1))
    j=0
    ep = frappe.db.sql(
        """
        SELECT sum(total) as total,sum(total_nc) as total_nc, emp_name as emp_name,emp,employee_mail,reporting_manager_mail from `tabEnergy Point  Non Conformity` where date(creation) BETWEEN %s AND %s AND docstatus=1 group by emp""",(first_date, last_date), as_dict=True)
    s_no=0
    for i in ep:
        s_no+=1
        j+=1
        data = """<table class='table table-bordered' style='border-collapse: collapse; width: 100%;'><tr style='border: 1px solid black; background-color: #0f1568; color: white;'><th>S No</th><th>Employee ID</th><th>Employee Name</th><th>Energy Score</th><th>NC Score</th></tr>""" 

        data += """<tr style='border: 1px solid black;'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %( s_no,i.emp,i.emp_name,i['total'] or "-",i['total_nc'] or "-" )
        data += "</table>"
        subject = "Energy Point(EP) And Non Conformity(NC) List-  %s" % nowdate()
        message = """
        Dear Sir/Madam,<br><br>
        Kindly find the below Monthly Energy Point And Non Conformity List<br><br>{}<br><br>
        Thanks & Regards,<br>TEAM ERP<br>
        <i>This email has been automatically generated. Please do not reply</i>
        """.format(data)
        if j>0:
            frappe.sendmail(
            recipients=[i.reporting_manager_mail,i.employee_mail],
            subject=subject,
            message=message,
        
        )


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff,format_datetime
from datetime import date, timedelta, datetime, time
from frappe.utils import (
    add_days,
    cstr,
    flt,
    format_datetime,
    formatdate,
    get_datetime,
    get_first_day,
    get_last_day,
    get_link_to_form,
    get_number_format_info,
    getdate,
    nowdate,
    today,
)
def epnc_send_mail():
    first_date=get_first_day(add_days(today(),-1))
    last_date=get_last_day(add_days(today(),-1))
    j=0
    ep = frappe.db.sql(
        """
        SELECT sum(total) as total,sum(total_nc) as total_nc, emp_name as emp_name,emp,employee_mail,reporting_manager_mail from `tabEnergy Point  Non Conformity` where date(creation) BETWEEN %s AND %s AND docstatus=1 group by emp""",(first_date, last_date), as_dict=True)
    s_no=0
    data = """<table class='table table-bordered' style='border-collapse: collapse; width: 100%;'><tr style='border: 1px solid black; background-color: #0f1568; color: white;'><th>S No</th><th>Employee ID</th><th>Employee Name</th><th>Energy Score</th><th>NC Score</th></tr>""" 
    for i in ep:
        s_no+=1
        j+=1
    # data = """<table class='table table-bordered' style='border-collapse: collapse; width: 100%;'><tr style='border: 1px solid black; background-color: #0f1568; color: white;'><th>S No</th><th>Employee ID</th><th>Employee Name</th><th>Energy Score</th><th>NC Score</th></tr>""" 
        data += """<tr style='border: 1px solid black;'><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %( s_no,i.emp,i.emp_name,i['total'] or "-",i['total_nc'] or "-" )
    data += "</table>"
    subject = "Energy Point(EP) And Non Conformity(NC) List-  %s" % nowdate()
    message = """
    Dear Sir/Madam,<br><br>
    Kindly find the below Monthly Energy Point And Non Conformity List<br><br>{}<br><br>
    Thanks & Regards,<br>TEAM ERP<br>
    <i>This email has been automatically generated. Please do not reply</i>
    """.format(data)
    if j>0:
        frappe.sendmail(
        recipients=['dineshbabu.k@groupteampro.com','sangeetha.s@groupteampro.com','sangeetha.a@groupteampro.com'],
        subject=subject,
        message=message,

        )

@frappe.whitelist()
def closure_mail(subject,id,action_taken,live,et,at,revision,service,proof,allocated=None,project=None,issue=None,domain=None,spoc=None,reason=None):
    if service=='IT-SW':
        percentage=et_at_calculation(id, et, at, allocated,subject)
        reports=frappe.db.get_value("Employee",{'user_id':allocated},['reports_to'])
        reports_to=frappe.db.get_value("Employee",{'name':reports},['user_id'])
        et_rate= 'ET : %s and AT : %s'%(et,percentage)
        if issue:
            raised_by=frappe.db.get_value("Issue",{'name':issue},['raised_by'])
        else:
            raised_by='None'
        data = ''
        data += f"<table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>\
        <tr><td colspan='2' style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black;'><b>Task / Issue Pending Review Note</b></td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Task ID</b></td><td style='border: 1px solid black;'>{id}</td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Project</b></td><td style='border: 1px solid black;'>{project}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task Raised By</b></td><td style='border: 1px solid black;'>{reports_to}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue ID</b></td><td style='border: 1px solid black;'>{issue}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Raised By</b></td><td style='border: 1px solid black;'>{raised_by}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Statement</b></td><td style='border: 1px solid black;'>{subject}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Action Taken</b></td><td style='border: 1px solid black;'>{action_taken}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Live At</b></td><td style='border: 1px solid black;'>{live}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Domain</b></td><td style='border: 1px solid black;'>{domain}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Proof</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/{proof}' target='_blank'>Link to Proof</a></td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>ET & AT</b></td><td style='border: 1px solid black;'>{et_rate}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Re-Open Count</b></td><td style='border: 1px solid black;'>{revision}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Cause of Re-Open</b></td><td style='border: 1px solid black;'>{reason}</td></tr></table>"

        frappe.sendmail(
            sender=allocated,
            # recipients=allocated,
            # recipients='pavithra.s@groupteampro.com',
            recipients=spoc,
            cc=[reports_to,allocated,'anil.p@groupteampro.com','dineshbabu.k@groupteampro.com'],
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
def nc_for_reopen(subject,cause=None,id=None,allocated=None):
    if allocated:
        emp_id=frappe.db.get_value("Employee",{'user_id':allocated},['name'])
        reopen_cause='Task : %s - (%s) Re-Open ' % (id,subject)
        nc = frappe.new_doc('Energy Point And Non Conformity')
        nc.emp = emp_id
        nc.action='Non Conformity(NC)'
        # nc.nc_reported_by = 'Administrator'
        nc.class_proposed = 'Critical'
        nc.reason_of_ep = reopen_cause
        nc.save(ignore_permissions=True)
        frappe.db.commit()

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

    if overall_at > 1.5 * float(et):
        reopen_cause='Task : %s - (%s) AT is 150 times greater than its ET'% (id,subject)
        nc = frappe.new_doc('Energy Point And Non Conformity')
        nc.emp = emp_id
        # nc.nc_reported_by = 'Administrator'
        nc.class_proposed = 'Major'
        nc.action='Non Conformity(NC)'
        nc.reason_of_ep = reopen_cause
        nc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.errprint("greater than expected")
    # else:
    #     total_hours = 0.0
    #     total_time_taken=float(at)
    #     total_time_taken_et=1.5 * float(et)
    #     if float(at)>total_time_taken_et:
    #         reopen_cause='Task : %s AT is 150 times greater than its ET'% id
    #         nc = frappe.new_doc('Energy Point And Non Conformity')
    #         nc.emp = emp_id
    #         # nc.nc_reported_by = 'Administrator'
    #         nc.class_proposed = 'Major'
    #         nc.action='Non Conformity(NC)'
    #         nc.reason_of_ep = reopen_cause
    #         nc.save(ignore_permissions=True)
            # frappe.db.commit()
    return overall_at


# @frappe.whitelist()
# def dpr_mail():
#     current_date = datetime.now().strftime("%Y-%m-%d")
    
#     data = '''
#     <html>
#     <body>
#         <table border="1" cellpadding="5" cellspacing="0">
#             <thead>
#                 <tr>
#                     <th>S.NO</th>
#                     <th>Task Name</th>
#                     <th>Project Name</th>
#                     <th>Subject</th>
#                     <th>CB</th>
#                     <th>Priority</th>
#                     <th>Status</th>
#                     <th>Revisions</th>
#                     <th>Actual Time</th>
#                     <th>Expected Time</th>
#                     <th>RT</th>
#                     <th>Custom Allocated On</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 <tr>
#                     <td>DPR ({})</td>
#                     <td colspan="10"></td>
#                 </tr>
#     '''.format(current_date)
    
#     tasks = frappe.db.get_all("Task", filters={'status': 'Working', 'service': 'IT-SW'}, fields=["name", "project_name", "subject", "cb", "status", "revisions", "actual_time", "expected_time", "rt", "priority", "custom_allocated_on"])
    
#     # Sort tasks by cb, project_name, and priority
#     tasks_sorted = sorted(tasks, key=lambda x: (x.get('cb', ''), x.get('project_name', ''), x.get('priority', '')))
    
#     for idx, task in enumerate(tasks_sorted, start=2):
#         data += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
#             idx, task.get('name', ''), task.get('project_name', ''), task.get('subject', ''), task.get('cb', ''), 
#             task.get('priority', ''), task.get('status', ''), task.get('revisions', ''), task.get('actual_time', ''), 
#             task.get('expected_time', ''), task.get('rt', ''), task.get('custom_allocated_on', '')
#         )
    
#     data += '''
#             </tbody>
#         </table>
#     </body>
#     </html>
#     '''
    
#     frappe.sendmail(
#         recipients='siva.m@groupteampro.com',
#         message=data
#     )


# @frappe.whitelist()
# def send_dsr_report():
#     total_open=0
#     total_working=0
#     total_pr=0
#     total_cr=0
#     total_overdue=0
#     mail = frappe.get_all("Project",{'spoc':"sivarenisha.m@groupteampro.com"},["name"])
#     for i in mail:
#         task_status=['Open','Working','Pending Review','Overdue','Client Review']
#         for a in task_status:
#             task_priority=['High','Low','Medium']
def auto_dnd_transition():
    job = frappe.db.exists('Scheduled Job Type', 'dpnd_excel_format')
    if not job:
        sjr = frappe.new_doc("Scheduled Job Type")
        sjr.update({
            "method": 'teampro.custom.dpnd_excel_format',
            "frequency": 'Cron',
            "cron_format": '30 18 * * *'
        })
        sjr.save(ignore_permissions=True)

@frappe.whitelist()
def dpnd_excel_format():
    filename = "DND Details_" + today() +".xlsx"
    xlsx_file = build_xlsx_response(filename)
    dnd_report(filename, xlsx_file.getvalue())

def dnd_report(filename,file_content):
    task=frappe.db.get_all("Closure",{"custom_status_transition":nowdate()},["*"],order_by='project')
    count=0
    closure_status=["PSL","Sales Order","Client Offer Letter","Signed Offer Letter","Visa","Premedical","PCC","Certificate Attestation","Final Medical","Biometric","Visa Stamping","Emigration","Ticket","Onboarding","Onboarded","Concluded","Dropped","Waitlisted"]
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
            recipients=["dc@groupteampro.com","sangeetha.a@groupteampro.com","divya.p@groupteampro.com"],
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
    closure_status=["PSL","Sales Order","Client Offer Letter","Signed Offer Letter","Visa","Premedical","PCC","Certificate Attestation","Final Medical","Biometric","Visa Stamping","Emigration","Ticket","Onboarding","Onboarded","Concluded","Dropped","Waitlisted"]
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


@frappe.whitelist()
def closure_mail_client(client_email,subject,id,action_taken,live,et,at,revision,service,proof,allocated=None,project=None,issue=None,domain=None,spoc=None,reason=None):
    if service=='IT-SW':
        percentage=et_at_calculation(id, et, at, allocated,subject)
        reports=frappe.db.get_value("Employee",{'user_id':allocated},['reports_to'])
        reports_to=frappe.db.get_value("Employee",{'name':reports},['user_id'])
        if issue:
            raised_by=frappe.db.get_value("Issue",{'name':issue},['raised_by'])
        else:
            raised_by='None'
        data = ''
        data += f"<table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>\
        <tr><td colspan='2' style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black;'><b>Task / Issue Client Review Note</b></td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Task ID</b></td><td style='border: 1px solid black;'>{id}</td></tr>\
        <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Project</b></td><td style='border: 1px solid black;'>{project}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task Raised By</b></td><td style='border: 1px solid black;'>{reports_to}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue ID</b></td><td style='border: 1px solid black;'>{issue}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Raised By</b></td><td style='border: 1px solid black;'>{raised_by}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Statement</b></td><td style='border: 1px solid black;'>{subject}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Task / Issue Action Taken</b></td><td style='border: 1px solid black;'>{action_taken}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Live At</b></td><td style='border: 1px solid black;'>{live}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Domain</b></td><td style='border: 1px solid black;'>{domain}</td></tr>\
        <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Proof</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/{proof}' target='_blank'>Link to Proof</a></td></tr>\
        </table>"

        frappe.sendmail(
            sender=allocated,
            # recipients=client_email,
            recipients=client_email,
            cc=[spoc,allocated,reports_to,'anil.p@groupteampro.com','dineshbabu.k@groupteampro.com'],
            subject='Task : %s Client Review : Forward for Review to Mark Completion or Re-Open' % id,
            message = """
            <b>Dear Patron,<br><br>Greeting !!!</b><br><br>
           The attached Task has been completed by Development and forwarded for your kind review, please confirm if it satisfies all your requirement and Mark the Task Status as Completed or if you feel it is still pending for some action please give your remark for Re-open <br><br>
           {}<br><br>
            Thanks & Regards,<br>TEAM ERP<br>
            
            <i>This email has been automatically generated. Please do not reply</i>
            """.format(data)
        )
        

@frappe.whitelist()
def get_allocated_tasks(date,name,service,type):
    frappe.errprint("details")
    total=0
    percent=0
    if type:
        task_id=frappe.db.get_all("Task",{"custom_production_date":date,"service":service,"type":type},['*'],order_by='cb asc, project asc, priority asc')
    else:
        task_id=frappe.db.get_all("Task",{"custom_production_date":date,"service":service},['*'],order_by='cb asc, project asc, priority asc')

    task_det=frappe.db.get_all("Task",{"custom_production_date":date,"service":service},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
    parent_doc = frappe.get_doc("Daily Monitor", name)
    parent_doc.task_details=[]
    parent_doc.dm_summary=[]
    issue_id=''
    for i in task_id:
        parent_doc.append("task_details", {"id": i.name,"a_task_type":i.type,"cb":i.cb})
        employee_id=frappe.db.get_value('Employee',{'short_code':i.cb},['user_id'])
        issue_id=frappe.db.get_all("Issue",{'assigned_to':employee_id,'status':'Open'},['*'])
    for j in issue_id:
        issue_list=frappe.db.get_value("Employee",{'user_id':j.assigned_to},['short_code'])
        frappe.errprint(issue_list)
        parent_doc.append("task_details", {"id": j.name,"project_name":j.project,"subject":j.subject,"cb":issue_list,"status":j.status})
    for k in task_det:
        actual_aph=frappe.db.get_value('Employee',{'short_code':k.cb},['custom_aph'])
        sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s group by cb""",(k.custom_allocated_to,date), as_dict=True)
        emp_cb=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['short_code'])
        total+=sum_et[0].et
        if actual_aph is not None:
            percent=(float(sum_et[0].et)/float(actual_aph))*100
            parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph or '8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0'})
            frappe.errprint(emp_cb)
            frappe.errprint(round(percent,2))
            frappe.errprint("hello")
        else:
            frappe.errprint("hi")
            percent=(float(sum_et[0].et)/8)*100
            parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':'8','d_rt':sum_et[0].et,'d_actual_time_taken':'','rt_vs_aph_':round(percent,2) or '0'})
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value("Daily Monitor",name,'dm_status',"DPR Pending")
    # frappe.db.set_value("Daily Monitor",name,'workflow_state',"DPR Pending")

    # return data



@frappe.whitelist()
def update_dsr(date, name,service,type):
    parent_doc = frappe.get_doc("Daily Monitor",name)
    frappe.errprint("hi")
    parent_doc.task_details = []
    if type:
        task_id_list = frappe.db.get_all("Task", {"custom_production_date":date,"service":service,"type":type}, ['*'], order_by='custom_allocated_to asc, project asc, priority asc')
    else:
        task_id_list = frappe.db.get_all("Task", {"custom_production_date": date,"service":service}, ['*'], order_by='custom_allocated_to asc, project asc, priority asc')
       
    task_list = frappe.db.get_all("Task", {"custom_production_date":date}, ['*'], order_by='cb asc, project asc, priority asc',group_by='custom_allocated_to asc')
    issues = []
    meetings = []
    tasks = []
    appended_issues = set()
    appended_meetings = set()
    parent_doc.dm_summary=[]
    for task in task_id_list:
        frappe.errprint("hello")
        emp_id = frappe.db.get_value("Employee", {'user_id': task.custom_allocated_to}, ['name'])
        emp_short_code= frappe.db.get_value("Employee", {'name': emp_id},['short_code'])
        timesheet = frappe.db.get_value("Timesheet", {'start_date':date, 'employee': emp_id},['name'])   
        frappe.errprint(timesheet)  
        task_hours_total = 0.0 
        if timesheet:
            frappe.errprint("inside of if timesheet")
            issue_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_issue': ['!=', '']}, fields=['*'])
            i_taken=0.0
            for issue in issue_logs:
                i_taken+=issue.hours
                if issue.custom_issue not in appended_issues:
                    frappe.errprint("inside of custom issue")
                    short_code=frappe.db.get_value("Employee",{'name':emp_id},['short_code'])
                    prior = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['priority'])
                    i_id = frappe.db.get_value("Issue", {'name': issue.custom_issue}, ['status'])
                    issues.append({
                        "id": issue.custom_issue,
                        "at_taken": issue.hours,
                        'project_name': issue.project_name,
                        'subject': issue.custom_subject_issue,
                        'status': i_id,
                        'cb':short_code,
                        'priority':prior
                    })
                    appended_issues.add(issue.custom_issue)            
            meeting_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'custom_meeting': ['!=', '']}, fields=['*'])
            for meeting in meeting_logs:
                if meeting.custom_meeting not in appended_meetings:
                    frappe.errprint("inside of meetings")
                    m_id = frappe.db.get_value("Issue", {'name': meeting.custom_meeting}, ['status'])
                    short_code=frappe.db.get_value("Employee",{'name':emp_id},['short_code'])
                    meetings.append({
                        "id": meeting.custom_meeting,
                        "at_taken": meeting.hours,
                        'subject':meeting.custom_subject_meeting,
                        'cb':short_code
                    })
                    appended_meetings.add(meeting.custom_meeting)  
            # task_hours_total = 0.0
            task_logs = frappe.get_all("Timesheet Detail", filters={'parent': timesheet, 'task': task.name}, fields=['hours'])
            # timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':emp_id}, ['total_hours'])      
            for log in task_logs:
                task_hours_total += log.hours
        tasks.append({
            "id": task.name,
            "at_taken": task_hours_total,
            "a_task_type":task.type,
            "cb":emp_short_code,
            "current_status":task.status
        })
    for d in issues:
        frappe.errprint("issue parent")
        parent_doc.append("task_details", d)
    for meeting in meetings:
        frappe.errprint("issue meeting")
        parent_doc.append("task_details", meeting)
    for task in tasks:
        frappe.errprint("issue task")
        parent_doc.append("task_details", task)
    parent_doc.dsr_check = 1
    for j in task_list:
            employee_id=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['name'])
            emp_cb=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['short_code'])
            timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])      
            actual_aph=frappe.db.get_value('Employee',{'name':employee_id},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
            if timesheet and actual_aph is not None:
                percent=(float(timesheet)/float(actual_aph))*100
                parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0','d_actual_time_taken':round(timesheet,2),'rt_vs_aph_':round(percent,2)})
            else:
                parent_doc.append("dm_summary",{'d_cb':emp_cb,'d_aph':actual_aph,'d_rt':sum_et[0].et if sum_et else '0' ,'d_actual_time_taken':'0','rt_vs_aph_':'0'})
    parent_doc.save()
    frappe.db.commit()
    frappe.db.set_value('Daily Monitor',name,'dm_status','DSR Pending')

@frappe.whitelist()
def dpr_task_mail(name,date,service,task_type):
    total=0
    total_count=0
    percent=0
    or_count=0
    pr_count=0
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')
    emp=frappe.db.get_all("Employee",{'status':'Active','reports_to':'TI00005'},['*'])
    recievers=[]
    for i in emp:
        recievers.append(i.user_id)
    recievers.append('abdulla.pi@groupteampro.com')
    recievers.append('dineshbabu.k@groupteampro.com')
    frappe.errprint(recievers)
    task_data=frappe.get_doc("Daily Monitor",name)
    # # priority = {"High": 1, "Medium": 2, "Low": 3}
    task=frappe.db.get_all("Task",{"custom_production_date":date},['*'],group_by='custom_allocated_to asc',order_by='cb asc, project asc, priority asc')
    total_at=0
    if task_data.dsr_check==1:
        count=1
        aph_totals=0
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
            <td style='width:4%'><b>SI NO</b></td>
            <td style='width:6%'><b>Task/Issue ID</b></td>
            <td style='width:12%'><b>Project </b></td>
            <td style='width:18%'><b>Subject</b></td>
            <td style='width:4%'><b>CB</b></td>
            <td style='width:7%'><b>Status</b></td>
            <td style='width:4%'><b>Revision</b></td>
            <td style='width:4%'><b>AT</b></td>
            <td style='width:4%'><b>ET</b></td>
            <td style='width:4%'><b>RT</b></td>
            <td style='width:6%'><b>Priority</b></td>
           <td style='width:8%'><b>Allocated On</b></td>
           <td style='width:4%'><b>Time Taken</b></td>
           <td style='width:10%'><b>Remarks</b></td>
           <td style='width:9%'><b>TL Remarks</b></td>
        </tr>
        '''
        table = '<table border="1" width="70%" style="border-collapse: collapse;text-align:center;">'
        table += '''
        <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
            <td style='width:1%'><b>CB</b></td>
            <td style='width:1%'><b>APH</b></td>
            <td style='width:1%'><b>RT</b></td>
            <td style='width:1%'><b>Actual Time Taken</b></td>
            <td style='width:1%'><b>RT Vs APH %</b></td>
            <td style='width:1%'><b>OR</b></td>
            <td style='width:1%'><b>PR</b></td>
        </tr>
        '''
        sorted_task_details = sorted(task_data.task_details, key=lambda i: i.cb)
        count = 1
        for i in sorted_task_details:
    #         # emp_cb=frappe.db.get_value('Employee',)
            vtaken = float(i.at)
            value_taken = round(vtaken, 3)
            if i.at_taken:
                t_taken = float(i.at_taken)
                today_taken = round(t_taken, 3)
            else:
                t_taken='0'
                today_taken='0'
            remark = '-' if i.remark is None else i.remark
            tl_remark = '-' if i.tl_remark is None else i.tl_remark
            if i.id is not None:
                id=i.id
            elif i.issue is not None:
                id=i.issue
            elif i.meeting is not None:
                id=i.meeting
            else:
                id='-'
            data += '<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'% (count,id, i.project_name, i.subject, i.cb, i.status, i.revisions, value_taken,i.et, i.rt, i.priority, i.allocated_on, today_taken, remark, tl_remark)
            count += 1
        data += '</table>'
        for j in task:
            employee_id=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['name'])
            emp_cb=frappe.db.get_value('Employee',{'user_id':j.custom_allocated_to},['short_code'])
            timesheet = frappe.db.get_value("Timesheet", {'start_date': date, 'employee':employee_id}, ['total_hours'])  
            actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and service="IT-SW" group by custom_allocated_to""",(j.custom_allocated_to,date), as_dict=True)
            if sum_et:
                total+=sum_et[0].et
            if actual_aph is not None:
                aph_totals+=float(actual_aph)
            if timesheet is not None:
                total_at+=float(timesheet)
            if actual_aph and timesheet:
                percent=(float(timesheet)/float(actual_aph))*100
                value=actual_aph
                total_count=float(total)/float(aph_totals)*100
                or_count=float(timesheet)/float(value)*100
                pr_count=float(sum_et[0].et)/float(timesheet)*100
                or_total=float(total_at)/float(aph_totals)*100
                pr_total=float(total)/float(total_at)*100
            if percent:
                frappe.errprint("hi")
                table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et[0].et if sum_et else '0',round(timesheet,2) if timesheet is not None else '0',round(percent,2) if timesheet is not None else '0',round(or_count) if timesheet is not None else '0',round(pr_count) if timesheet is not None else '0')
            else:
                frappe.errprint("hello")
                table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '8',sum_et[0].et if sum_et else '0',round(timesheet,2) if timesheet is not None else'0','0',round(or_count,2) or '0',round(pr_count,2) or '0')
        table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_totals,total,round(total_at,2),round(total_count,2),round(or_total),round(pr_total))
        table += "</table>"
           
        
        frappe.sendmail(
                # sender='abdulla.pi@groupteampro.com',
                # recipients='dineshbabu.k@groupteampro.com',
                # cc='abdulla.pi@groupteampro.com',
                # recipients='divya.p@groupteampro.com',
                subject='DSR %s -Reg' % formatted_date,
                message = """
               <b>Dear Team,</b><br><br>
                Please find the below DSR for {} for your kind reference.<br><br>
                {}<br><br>
                {}<br><br>
                Thanks & Regards,<br>TEAM ERP<br>
                <i>This email has been automatically generated. Please do not reply</i>
                """.format(formatted_date,table,data)
            )
        frappe.msgprint("DSR mail has been successfully sent.")
        frappe.db.set_value('Daily Monitor',name,'dm_status','Submitted')
        frappe.db.set_value("Daily Monitor",name,'dsr_submitted_on',today())
    else:
        count=1
        aph_total=0
        data = '<table border="1" width="100%" style="border-collapse: collapse;">'
        data += '''
        <tr style="background-color: #0f1568 ;text-align:center;color: white;"><b>
            <td style='width:5%'><b>SI NO</b></td>
            <td style='width:10%'><b>ID</b></td>
            <td style='width:15%'><b>Project </b></td>
            <td style='width:20%'><b>Subject</b></td>
            <td style='width:5%'><b>CB</b></td>
            <td style='width:10%'><b>Status</b></td>
            <td style='width:5%'><b>Revision</b></td>
            <td style='width:5%'><b>AT</b></td>
            <td style='width:5%'><b>ET</b></td>
            <td style='width:5%'><b>RT</b></td>
            <td style='width:7%'><b>Priority</b></td>
            <td style='width:13%'><b>Allocated On</b></td>
        </b></tr>
        '''
        table = '<table border="1" width="50%" style="border-collapse: collapse;text-align:center;">'
        table += '''
        <tr style="background-color: #0f1568 ;color: white;text-align:center;font-size: 12px;">
            <td style='width:1%'><b>CB</b></td>
            <td style='width:1%'><b>APH</b></td>
            <td style='width:1%'><b>RT</b></td>
            <td style='width:1%'><b>RT Vs APH%</b></td>
        </tr>
        '''
        for i in task_data.task_details:
            value_taken = round(i.at, 3)
            data+='<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'%(count,i.id or i.issue,i.project_name or '-',i.subject,i.cb,i.status,i.revisions,value_taken,i.et,i.rt,i.priority,i.allocated_on or '')
            count+=1
        data += '</table>'
        task_det=frappe.db.get_all("Task",{"custom_production_date":date,"type":task_type,"service":service},['*'],order_by='cb asc',group_by='custom_allocated_to asc')
        for k in task_det:
            employee_id=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['user_id'])
            emp_cb=frappe.db.get_value('Employee',{'user_id':k.custom_allocated_to},['short_code'])
            actual_aph=frappe.db.get_value('Employee',{'short_code':emp_cb},['custom_aph'])
            sum_et=frappe.db.sql("""select sum(rt) as et from `tabTask` where custom_allocated_to=%s and custom_production_date=%s and service="IT-SW" group by custom_allocated_to""",(k.custom_allocated_to,date), as_dict=True)
            if sum_et:
                total+=sum_et[0].et
            if actual_aph is not None and sum_et:
                percent=(float(sum_et[0].et)/float(actual_aph))*100
                value=actual_aph
                aph_total+=float(value)
            total_count=float(total)/float(aph_total)*100
            # print(employee_id)
            if percent:
                table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,value or '8',sum_et[0].et if sum_et else '0',round(percent,2) or '-')
            else:
                table+='<tr style="font-size: 14px;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' %(emp_cb,actual_aph or '',sum_et[0].et if sum_et else '0',round(percent,2) or '-')
        table+='<tr style="font-size: 14px;" ><td colspan=1>Total</td><td>%s</td><td>%s</td><td>%s</td>'%(aph_total,total,round(total_count,2))
        table+='</table>'
        frappe.sendmail(
                # sender='abdulla.pi@groupteampro.com',
                # recipients=recievers,
                # recipients='divya.p@groupteampro.com',
                subject='DPR %s -Reg' % formatted_date,
                message = """
                <b>Dear Team,</b><br><br>
Please find the below DPR for {} for your kind reference and action, ensure all the Tasks allocated on time and as per the requirement, for each Revision and AT going beyond 150% there will be NC applied and accumulated NC will be reviewed every week and directly affects your Performance.<br><br>

            {}<br><br>
            {}<br><br>
                Thanks & Regards,<br>TEAM ERP<br>
                
                <i>This email has been automatically generated. Please do not reply</i>
                """.format(formatted_date,table,data)
            )
        frappe.msgprint("DPR mail has been successfully sent")
        frappe.db.set_value('Daily Monitor',name,'dm_status','DPR Completed')
        frappe.db.set_value('Daily Monitor',name,'dpr_submitted_on',today())


@frappe.whitelist()
def reverse_revision(user):
    role = frappe.db.sql("""
        SELECT `tabUser`.name as name
        FROM `tabUser`
        LEFT JOIN `tabHas Role` ON `tabHas Role`.parent = `tabUser`.name
        WHERE `tabHas Role`.role = 'Customer Executive'
        AND `tabUser`.enabled = 1
        AND `tabUser`.name = %s
    """, (user,), as_dict=True)

    if role:
        return role[0].get('name')
    else:
        return None

@frappe.whitelist()
def reverse_revision_nc(name):
    reason = frappe.db.get_value("Energy Point And Non Conformity", {'reason_of_ep': ['like', '%'+name+'%']}, "name")

    if reason:
        nc = frappe.get_doc("Energy Point And Non Conformity", reason)
        nc.delete()

@frappe.whitelist()
def task_type_updates(name,id):
    cb=frappe.db.get_value("Employee",{"user_id":name},["short_code"])
    # frappe.db.set_value("Task",id,'cb',cb)
    return cb


@frappe.whitelist()
def dpr_send_alert():
    date = datetime.strptime(today(), '%Y-%m-%d')
    formatted_date = date.strftime('%d/%m/%Y')
    today_date=today()
    doc_name = frappe.db.get_value("Daily Monitor",{"date": today_date},["name"])
    if doc_name:
        print("hi")
        parent_doc = frappe.get_doc("Daily Monitor", doc_name)
        if parent_doc.dpr_submitted_on is None:
            hod_mail=frappe.db.get_value("Services",{"name":"IT-SW"},['hod'])
            frappe.sendmail(
                recipients=[hod_mail,"divya.p@groupteampro.com"],
                # recipients="divya.p@groupteampro.com",
                subject= "DPR Reminder - %s" % formatted_date,
                message=""" Dear Sir,<br><br>
                The DPR is not updated today.Kindly update the DPR<br><br>
                Thanks & Regards,<br>TEAM ERP<br>"""
            )
    else:
        print("hello")
        hod_mail=frappe.db.get_value("Services",{"name":"IT-SW"},['hod'])
        frappe.sendmail(
            recipients=[hod_mail,"divya.p@groupteampro.com"],
            # recipients="divya.p@groupteampro.com",
            subject= "Daily Monitor Reminder - %s" % formatted_date,
            message=""" Dear Sir,<br><br>
            The Daily Monitor  is not created today.Kindly create the Daily Monitor<br><br>
            Thanks & Regards,<br>TEAM ERP<br>"""
        )

@frappe.whitelist()
def dsr_send_alert():
    date = datetime.strptime(add_days(today(),-1), '%Y-%m-%d')
    formatted_date = date.strftime('%d/%m/%Y')
    dates = datetime.strptime(today(), '%Y-%m-%d')
    formatted_dates = dates.strftime('%d/%m/%Y')
    previous_date = add_days(today(),-1)
    doc_name = frappe.db.get_value("Daily Monitor",{"date": previous_date},["name"])
    print(doc_name)
    if doc_name:
        parent_doc = frappe.get_doc("Daily Monitor", doc_name)
        if parent_doc.dsr_submitted_on is None:
            hod_mail=frappe.db.get_value("Services",{"name":"IT-SW"},['hod'])
            frappe.sendmail(
                recipients=[hod_mail,"divya.p@groupteampro.com"],
                # recipients="divya.p@groupteampro.com",
                subject= "DSR Reminder - %s" % formatted_dates,
                message=""" Dear Sir,<br><br>
                The DSR is not updated for -%s.Kindly update the DSR.<br><br>
                Thanks & Regards,<br>TEAM ERP<br>""" % formatted_date
            )

def auto_dpr_reminder():
    job = frappe.db.exists('Scheduled Job Type', 'dpr_send_alert')
    if not job:
        sjr = frappe.new_doc("Scheduled Job Type")
        sjr.update({
            "method": 'teampro.custom.dpr_send_alert',
            "frequency": 'Cron',
            "cron_format": '30 10 * * *'
        })
        sjr.save(ignore_permissions=True)

def auto_dsr_reminder():
    job = frappe.db.exists('Scheduled Job Type', 'dsr_send_alert')
    if not job:
        sjr = frappe.new_doc("Scheduled Job Type")
        sjr.update({
            "method": 'teampro.custom.dsr_send_alert',
            "frequency": 'Cron',
            "cron_format": '30 10 * * *'
        })
        sjr.save(ignore_permissions=True)






@frappe.whitelist()
def update_tat_completion_date(name):
    doc=frappe.get_doc("Case",name)
    if doc.insufficiency_closed:
        from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
        holiday_list_name = 'TEAMPRO 2023 - Checkpro'
        start_date = doc.insufficiency_closed
        working_days = int(frappe.db.get_value("Check Package",{'name':doc.check_package},['package_tat']))
        current_date = start_date
        holiday = []
        while working_days > 0:
            if not is_holiday(holiday_list_name, current_date):
                holiday.append(current_date)
                working_days -= 1
            current_date = add_days(current_date, 1)
        sql_query = f"""
            SELECT COUNT(*) 
            FROM `tabHoliday` 
            WHERE parent = 'TEAMPRO 2023 - Checkpro' 
            AND holiday_date BETWEEN '{doc.insufficiency_closed}' AND '{holiday[-1]}'
        """
        count = frappe.db.sql(sql_query, as_list=True)[0][0]
        return holiday[-1],count

@frappe.whitelist()
def update_issue_type(doc,method):
    frappe.db.set_value("Issue",doc.issue,"custom_issue_status",doc.status)
    frappe.db.set_value("Issue",doc.issue,"issue_type",doc.custom_issue_type)
    # if doc.status in ["Open","Overdue","Hold"]:
    #     frappe.db.set_value("Issue",doc.issue,"status","Open")
    # elif doc.status in ["Working"]:
    #     frappe.db.set_value("Issue",doc.issue,"status","Replied")
    # elif doc.status in ["Pending Review","Client Review"]:
    #     frappe.db.set_value("Issue",doc.issue,"status","Resolved")
    # elif doc.status in ["Completed","Cancelled"]:
    #     frappe.db.set_value("Issue",doc.issue,"status","Closed")

       

@frappe.whitelist()
def update_issue_typein_issue(doc,method):
    frappe.db.set_value("Issue",doc.issue,"task",doc.name)  

from datetime import datetime
@frappe.whitelist()
def update_issue_status():
    issues=frappe.get_all("Issue",{'custom_issue_status':('in',['Open' ,'Working'])},['custom_expected_end_date','name',"custom_issue_status"])
    for issue in issues:
        if issue.custom_expected_end_date < datetime.now().date():
            frappe.db.set_value("Issue",issue.name,"custom_issue_status","Overdue")

def auto_update_issue_status():
    job = frappe.db.exists('Scheduled Job Type', 'update_issue_status')
    if not job:
        sj = frappe.new_doc("Scheduled Job Type")
        sj.update({
            "method": 'teampro.custom.update_issue_status',
            "frequency": 'Cron',
            "cron_format": '0 0 * * *'
        })
        sj.save(ignore_permissions=True)


@frappe.whitelist()
def client_reviwew_mail(client_email,subject,created_by,action_taken,issue,live,proof,project=None,domain=None):
    data = ''
    data += f"<table width='100%' style='border-collapse: collapse; border: 1px solid black; text-align: center;'>\
    <tr><td colspan='2' style='text-align: center; background-color: #0f1568;color: white; font-size: 17px; border: 1px solid black;'><b>Issue Client Review Note</b></td></tr>\
    <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Issue ID</b></td><td style='border: 1px solid black;'>{issue}</td></tr>\
    <tr style='text-align: left;'><td width='25%'style='border: 1px solid black;'><b>Project</b></td><td style='border: 1px solid black;'>{project}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Raised By</b></td><td style='border: 1px solid black;'>{created_by}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Statement</b></td><td style='border: 1px solid black;'>{subject}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Issue Action Taken</b></td><td style='border: 1px solid black;'>{action_taken}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Live At</b></td><td style='border: 1px solid black;'>{live}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Domain</b></td><td style='border: 1px solid black;'>{domain}</td></tr>\
    <tr style='text-align: left;'><td style='border: 1px solid black;'><b>Proof</b></td><td style='border: 1px solid black;'><a href='https://erp.teamproit.com/{proof}' target='_blank'>Link to Proof</a></td></tr>\
    </table>"

    frappe.sendmail(
        sender=created_by,
        # recipients=["divya.p@groupteampro.com"],
        recipients=client_email,
        # cc=[allocated,reports_to,'anil.p@groupteampro.com','dineshbabu.k@groupteampro.com'],
        subject='Task : %s Client Review : Forward for Review to Mark Completion' % issue,
        message = """
        <b>Dear Patron,<br><br>Greeting !!!</b><br><br>
        The attached Issue has been completed by Development and forwarded for your kind review, please confirm if it satisfies all your requirement and Mark the Issue Status as Completed  <br><br>
        {}<br><br>
        Thanks & Regards,<br>TEAM ERP<br>
        
        <i>This email has been automatically generated. Please do not reply</i>
        """.format(data)
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
    
    frappe.sendmail(
        # recipients='dineshbabu.k@groupteampro.com',
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
            # recipients='dineshbabu.k@groupteampro.com',
            subject='Purchase Invoice-Beyond Due Date',
            message="""
            <b>Dear Sir/Mam,</b><br><br>
            Please find the below purchase invoice list for your kind reference and action.<br><br>
            {}<br><br>
            Thanks & Regards,<br>TEAM ERP<br>
            <i>This email has been automatically generated. Please do not reply</i>
            """.format(data)
        )




    