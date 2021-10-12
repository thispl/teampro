from bleach import linkify
import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import get_first_day, get_last_day, format_datetime,get_url_to_form
from frappe.utils import cint
from frappe.utils.data import today,add_days
import datetime

def remove_private():
    cand = frappe.db.sql("""select name,irf from `tabCandidate` where irf != '' """,as_dict=True)
    print(len(cand))
    for can in cand:
        if can.irf:
            print("----------------------")
            print(can.irf)
            frappe.db.set_value("Candidate",can.name,"irf",(can.irf).replace("/private",""))
            print("------------------------")

def bulk_update_from_csv(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    count = 0
    for pp in pps[:5]:
        mobile = pp[0]
        project = pp[1]
        position = pp[2]
        given_name = pp[3]
        customer = pp[4]
        print(mobile,project,position,given_name,customer)
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
        l = frappe.get_doc("Lead",lead.name)
        if not l.contact_date:
            l.contact_date = "2020-08-31 0:00:00"
            l.save(ignore_permissions=True)
            frappe.db.commit()

def update_lead():
    leads = frappe.get_list("Lead",{"organization_lead":"0"})
    for lead in leads:
        doc = frappe.get_doc("Lead",lead.name)
        doc.organization_lead = 1
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        # frappe.errprint(lead.name)

@frappe.whitelist()
def add_project_id(project):
    projects = frappe.db.sql("""select project_id from `tabProject` where project_id is not null order by creation""",as_dict=True)
    project_id = projects[-1].project_id
    return 'PRO' + str(int(project_id.strip('PRO'))+1)

@frappe.whitelist()
def update_task_fields(project):
    tasks = frappe.get_all('Task',{'project':project},['name','project_manager','account_manager','service'])
    proj = frappe.get_doc('Project',{'name':project})
    for t in tasks:
        frappe.errprint('---')
        frappe.errprint(t.account_manager)
        frappe.errprint(proj.account_manager)
        frappe.errprint('---')
        if t.project_manager != proj.project_manager:
            frappe.db.set_value('Task',t.name,'project_manager',proj.project_manager)
        if t.account_manager != proj.account_manager:
            frappe.db.set_value('Task',t.name,'account_manager',proj.account_manager)
        if t.service != proj.service:
            frappe.db.set_value('Task',t.name,'service',proj.service)

@frappe.whitelist()
def opportunity_send_mail(self,method):
    if self.service == 'TGT':
        link = get_url_to_form("Opportunity", self.name)
        subject = 'Reg.Opportunity- %s'%self.name
        content = """Dear Mam<br>Kindly find the new Opportunity.
        Click on <a href='%s'>View</a> to open the opportunity.<br>Thanks & Regards,<br>ERP
        """%link
        frappe.sendmail(recipients=['saraswathi.p@groupteampro.com'],
                        subject=subject,
                        message = content)

@frappe.whitelist()
def checkin_alerts():
    # yesterday = add_days(today(),-2)
    yesterday = add_days(datetime.datetime.today(),-17).date()
    current_month = yesterday.month
    late_checkins = frappe.db.sql("select employee from `tabEmployee Checkin` where date(time) = '%s' and time(time) > '09:35:00' " %(yesterday),as_dict=True)
    frappe.errprint(late_checkins)
    if late_checkins:
        for emp in late_checkins:
            apid = frappe.db.exists('Attendance Permission',{'employee':emp.employee,'month':current_month})
            print(emp)
            if apid:
                pc = frappe.get_value('Attendance Permission',apid,'permission_count')
                if pc < 3:
                    #adding permission
                    ap = frappe.get_doc('Attendance Permission',apid)
                    ap.update({
                        'permission_count': pc + 1
                    })
                    ap.save(ignore_permissions=True)
                    frappe.db.commit()

                    lp = frappe.db.exists('Leave Application',{'employee':emp.employee,'from_date':yesterday,'to_date':yesterday})
                    if lap :
                        pass   
                else:
                    lw = frappe.new_doc('Leave Application')
                    lw.update({
                         'employee' : emp.employee,
                         'leave_type' : "Leave Without Pay",
                         'from_date' : yesterday,
                         'to_date' : yesterday,
                         'description' : 'Auto marked as LWP due to Exceed Monthly Permission Limit'
                          })
                    lw.save(ignore_permissions=True)
                    frappe.db.commit()
                    
            else:
                ap = frappe.new_doc('Attendance Permission')
                ap.update({
                    'employee': emp.employee,
                    'month':current_month,
                    'permission_count': 1
                })
                ap.save(ignore_permissions=True)
                frappe.db.commit()


@frappe.whitelist()
def lwp_alert():
    yesterday = add_days(today(),-19)
    employees = frappe.get_all('Employee',{'status':'Active'},['name','employee_name','employee'])
    for emp in employees:
        lc = frappe.db.sql("select employee from `tabEmployee Checkin` where date(time) = '%s' and employee = '%s'" %(yesterday,emp.name),as_dict=True)
        lap = frappe.db.exists('Leave Application',{'employee':emp.employee,'from_date':yesterday,'to_date':yesterday})
        if lap :
            pass
        if len(lc) < 2:
             lp = frappe.new_doc('Leave Application')
             lp.update({
                 'employee' : emp.employee,
                 'leave_type' : "Leave Without Pay",
                 'from_date' : yesterday,
                 'to_date' : yesterday,
                 'description' : 'Auto marked as LWP due to not responding Miss Punch Alert'
             })
             lp.save()
             frappe.db.commit()
