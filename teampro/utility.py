import math
import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,datetime,get_first_day,get_last_day,today)



# def change_ends_on_date():
#     leads = frappe.get_all("Lead")
#     print(len(leads))
#     for l in leads:
#         print(l.name)
#         frappe.db.set_value("Lead",l.name,"ends_on","2295-12-31 00:00:00")


# def change_validation():
#     leads = frappe.get_all("Lead")
#     print(len(leads))
#     for l in leads:
#         print(l.name)
#         frappe.db.set_value("Lead",l.name,"validation_status","Invalid")


# def transfer_website():
#     leads = frappe.get_all("Lead",['name','website'])
#     for l in leads:
#         frappe.db.set_value("Lead",l.name,"web",l.website)

# @frappe.whitelist()
# def transfer_contacts():
    # leads = frappe.get_all('Contact',['name','temp_mobile_no'])
    # for lead in leads:
#     contacts = frappe.db.sql("""select `tabContact`.name,`tabContact`.first_name,`tabContact`.middle_name,`tabContact`.last_name,`tabDynamic Link`.link_doctype, `tabDynamic Link`.link_name,`tabContact Email`.email_id
#     from `tabContact` Left Join `tabDynamic Link` on `tabContact`.name = `tabDynamic Link`.parent
#     Left Join `tabContact Email` on `tabContact`.name = `tabContact Email`.parent where `tabDynamic Link`.link_doctype = 'Lead'  """,as_dict=True)
#     for contact in contacts:
#         lead = frappe.get_doc('Lead',contact.link_name)
#         if not contact.last_name:
#             person_name = contact.first_name
#         else:
#             person_name = contact.first_name + contact.last_name
#         lead.append('lead_contacts',{
#             'person_name': person_name,
#             'mobile': lead.temp_mobile_no,
#             'email_id': contact.email_id
#         })
#         lead.save(ignore_permissions=True)
#         frappe.db.commit()
#         print(lead.name,person_name,lead.temp_mobile_no,contact.email_id)

# # @frappe.whitelist()
# def transfer_address():
#     addresses = frappe.db.sql("""select `tabAddress`.address_line1,`tabAddress`.address_line2,`tabAddress`.city,`tabAddress`.phone,`tabAddress`.state,`tabAddress`.country,`tabDynamic Link`.link_doctype, `tabDynamic Link`.link_name
#     from `tabAddress` Left Join `tabDynamic Link` on `tabAddress`.name = `tabDynamic Link`.parent where `tabDynamic Link`.link_doctype = 'Lead' """,as_dict=True)
#     for address in addresses:
#         lead = frappe.get_doc('Lead',address.link_name)
#         addr = ''
#         addr += address.address_line1 or '' + "\n"
#         addr += address.address_line2 or '' + "\n"
#         addr += address.city or '' + "\n"
#         addr += address.state or '' + "\n"
#         addr += address.country or '' + "\n"
#         addr += address.phone or '' + "\n"
#         lead.address = addr
#         lead.save(ignore_permissions=True)
#         frappe.db.commit()
        # print(addr)
    # print(lead.name,person_name,lead.temp_mobile_no,contact.email_id)


# @frappe.whitelist()
# def change_lead_owner():
#     leads = frappe.get_all("Lead",{'contact_by':'sr@groupteampro.com','territory':'Tamil Nadu'})
#     print(len(leads))
#     # for l in leads:
#     #     print(l.name)
#     #     # frappe.db.set_value("Lead",l.name,"contact_by","sales@groupteampro.com")
    #     frappe.db.set_value("Lead",l.name,"lead_owner","anil.p@groupteampro.com")

# def change_sams_owner(filename):
#     from frappe.utils.file_manager import get_file
#     filepath = get_file(filename)
#     pps = read_csv_content(filepath[1])
#     for pp in pps:
#         if pp[0]:
#             print(pp[0],pp[1])
#             frappe.db.set_value('SAMS',pp[0],'sa_owner',pp[1])


@frappe.whitelist()
def attendance_calc():
    employees = frappe.get_all("Employee",{"status":"Active"},["*"])

    from_date = '2022-07-01'
    to_date = '2022-07-31'
    # from_date = get_first_day(add_months(today(),-1))
    # to_date = add_days(today(),-1)
    for emp in employees:
        late_list = frappe.db.sql("""select count(name) as count from `tabAttendance` where employee = '%s' and time(in_time) > '09:30:00' and attendance_date between '%s' and '%s' """%(emp.name,from_date,to_date),as_dict=True)[0].count or 0
        attendance_perm = frappe.db.sql("""select count(*) as count from `tabAttendance Permission` where employee = '%s' and status in ('Approved','Open') and permission_date between '%s' and '%s' """%(emp.name,from_date,to_date),as_dict=True)[0].count or 0 
        on_duty = frappe.db.sql("""select sum(total_days) as count from `tabAttendance Request` where employee = '%s' and docstatus=1 and from_date between '%s' and '%s' """%(emp.name,from_date,to_date),as_dict=True)[0].count or 0 
        emp_base = frappe.db.sql("""select per_day_salary, max(from_date) from `tabSalary Structure Assignment` where employee = '%s'  """%(emp.name,),as_dict=True)[0].per_day_salary
        per_day_amount = 0
        late_penalty = 0
        allowed_late = 3
        actual_late = late_list - (allowed_late + attendance_perm + on_duty)
        if actual_late > 0 :
            exceed_late = math.ceil(actual_late/3)
        else:
            exceed_late = 0
            actual_late = 0
        
        if emp_base :
            per_day_amount = round(emp_base)
        if exceed_late > 3:
            late_penalty = round(per_day_amount * exceed_late) 
        adsl = frappe.new_doc("Late Penalty")
        adsl.emp_name = emp.name
        adsl.deduction_amount = late_penalty
        adsl.deduction_days = exceed_late
        adsl.late_days = actual_late
        adsl.permissions = attendance_perm
        adsl.save()
        # It will create additional salary after late penalty is created
        if exceed_late > 3:
            if frappe.db.exists("Salary Structure Assignment",{'employee':emp.name}):
                ad = frappe.new_doc('Additional Salary')
                ad.employee = emp.name
                ad.salary_component = "Late Penalty"
                ad.company = emp.company
                ad.amount = late_penalty
                ad.payroll_date = nowdate()
                ad.save(ignore_permissions=True)
            
        # print(late_list)
        # print(exceed_late)
        # print(per_day_amount)
        # print(emp.name)
        # print(attendance_perm)
        # print(actual_late)

@frappe.whitelist()
def bulk_update_closure_status():
    count = 0
    closures = frappe.get_all('Closure',{'status':'PCC'},['visa','name'])
    for cl in closures:
        if not cl.visa:
            frappe.db.set_value('Closure',cl.name,'status','Visa')
            frappe.db.commit()        
    