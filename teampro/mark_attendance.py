import frappe
from datetime import datetime
import datetime
from frappe.utils.data import today, add_days, add_years
from dateutil.relativedelta import relativedelta
from datetime import timedelta, time,date
from frappe.utils import time_diff_in_hours, formatdate, get_first_day,get_last_day, nowdate, now_datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe.utils import time_diff


@frappe.whitelist()
def cron_job():
    job = frappe.db.exists('Scheduled Job Type', 'mark_att')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")  
        sjt.update({
            "method" : 'teampro.mark_attendance.mark_att',
            "frequency" : 'Cron',
            "cron_format" : '*/55 * * * *'
        })
        sjt.save(ignore_permissions=True)

@frappe.whitelist()
def mark_att():
    # from_date='2024-09-01'
    # to_date='2024-09-13'
    from_date = add_days(today(),-1)  
    to_date = today()
    dates = get_dates(from_date,to_date)
    for date in dates:
        from_date = add_days(date,-1)
        to_date = date
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=1)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:  
            mark_attendance_from_checkin(c.name,c.employee,c.time)
    mark_absent(from_date,to_date)                                

def mark_attendance_from_checkin(checkin,employee,time):
    att_time = time.time()
    att_date = time.date()
    in_time = ''
    out_time = ''
    checkins = frappe.db.sql("""select name,time from `tabEmployee Checkin` where employee = "%s" and date(time) = '%s' order by time """%(employee,att_date),as_dict=True)
    if checkins:
        if len(checkins) >= 2:
            in_time = checkins[0].time
            out_time = checkins[-1].time
        elif len(checkins) == 1:
            in_time = checkins[0].time
        status = "Absent"
        if in_time and out_time:  
            value = time_diff(out_time,in_time)
            if frappe.db.exists('Attendance Permission',{'employee':employee,'permission_date':att_date,'docstatus':1}):
                frappe.errprint(employee)
                att_per=frappe.db.get_value("Attendance Permission",{'employee':employee,'permission_date':att_date,'docstatus':1},['total_time'])
                print(employee)
                val = float(att_per) + (value.total_seconds() / 3600)
            elif frappe.db.exists('Attendance Request',{'employee': employee,'docstatus': 1,'from_date': ['<=', att_date],'to_date': ['>=', att_date]}):
                att_req=frappe.db.get_value('Attendance Request',{'employee': employee,'docstatus': 1,'from_date': ['<=', att_date],'to_date': ['>=', att_date]},['half_day'])
                if att_req==1:
                    req_time=4
                    val = value.total_seconds() / 3600 + float(req_time)
                else:
                    req_time=8
                    val = float(req_time)
            else:
                val = value.total_seconds() / 3600
            frappe.errprint(type(val))
            print(att_date)
            if val < 4 :
                status = "Absent"
            elif val > 4 and val < 8 :
                status = "Half Day"
                if val > 6 :
                    day_of_week = att_date.weekday()
                    week_number = (att_date.day - 1) // 7 + 1
                    if day_of_week == 5 and (week_number == 2 or week_number == 4):
                        status = 'Present'
                else:
                    status = "Half Day"
            elif val >= 8:
                status = "Present"	
        else:
            
            if frappe.db.exists('Attendance Request',{'employee': employee,'docstatus': 1,'from_date': ['<=', att_date],'to_date': ['>=', att_date]}):
                att_req=frappe.db.get_value('Attendance Request',{'employee': employee,'docstatus': 1,'from_date': ['<=', att_date],'to_date': ['>=', att_date]},['half_day'])
                if att_req==1:
                    req_time=4
                    
                else:
                    req_time=8
                    val = float(req_time)
                if val < 4 :
                    status = "Absent"
                elif val > 4 and val < 8 :
                    status = "Half Day"
                    if val > 6 :
                        day_of_week = att_date.weekday()
                        week_number = (att_date.day - 1) // 7 + 1
                        if day_of_week == 5 and (week_number == 2 or week_number == 4):
                            status = 'Present'
                    else:
                        status = "Half Day"
                elif val >= 8:
                    status = "Present"
            else:
                val = 0.0
                status = "Absent"
            
        att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':("!=",2)})
        if not att:
            att = frappe.new_doc("Attendance")
            att.employee = employee
            att.attendance_date = att_date
            att.shift = 'G'
            att.status = status
            att.in_time = in_time
            att.out_time = out_time
            att.bt_difference = val
            att.save(ignore_permissions=True)
            # if status =='Present':
            # 	# att.submit()
            # 	update_coff(att_date,employee)	
            frappe.db.commit()
            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            frappe.db.set_value('Employee Checkin',checkin,'attendance',att.name)
            print(att.name)
            return att.name
        else:
            if in_time:
                frappe.db.set_value("Attendance",att,'in_time',in_time)
            if out_time:
                frappe.db.set_value("Attendance",att,'out_time',out_time)
            frappe.db.set_value("Attendance",att,'shift','G')
            frappe.db.set_value("Attendance",att,'bt_difference',val)
            frappe.db.set_value("Attendance",att,'status',status)
            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            # if status == "Present":
            # 	# frappe.db.set_value("Attendance",att,'docstatus',1)
            # 	update_coff(att_date,employee)
            frappe.db.commit()
            frappe.db.set_value('Employee Checkin',checkin,'attendance',att)
            print(att)
            return att
    else:
        status='Absent'
        if frappe.db.exists('Attendance Request',{'employee': employee,'docstatus': 1,'from_date': ['<=', att_date],'to_date': ['>=', att_date]}):
                att_req=frappe.db.get_value('Attendance Request',{'employee': employee,'docstatus': 1,'from_date': ['<=', att_date],'to_date': ['>=', att_date]},['half_day'])
                if att_req==1:
                    req_time=4
                    val = float(req_time)
                    status='Half Day'
                else:
                    req_time=8
                    val = float(req_time)
                    status='Present'
        att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':("!=",2)})
        if not att:
            att = frappe.new_doc("Attendance")
            att.employee = employee
            att.attendance_date = att_date
            att.shift = 'G'
            att.status = status
            att.bt_difference = val
            att.save(ignore_permissions=True)
            # if status =='Present':
            # 	# att.submit()
            # 	update_coff(att_date,employee)	
            frappe.db.commit()
            
        else:
            frappe.db.set_value("Attendance",att,'shift','G')
            frappe.db.set_value("Attendance",att,'bt_difference',val)
            frappe.db.set_value("Attendance",att,'status',status)
           
            frappe.db.commit()
            print(att)
            return att
       

@frappe.whitelist()    
def mark_absent(from_date,to_date):
    dates = get_dates(from_date,to_date)
    for date in dates:
        employee = frappe.db.get_all('Employee',{'status':'Active','date_of_joining':['<=',date]},['*'])
        for emp in employee:
            hh = check_holiday(date,emp.name)
            if not hh:
                if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')}):
                    att = frappe.new_doc('Attendance')
                    att.employee = emp.name
                    att.status = 'Absent'
                    att.attendance_date = date
                    att.save(ignore_permissions=True)
                    frappe.db.commit()   

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
@frappe.whitelist()
def update_coff(date, emp):
    holiday_list = frappe.get_value('Employee', emp, 'holiday_list')
    holiday = frappe.get_all('Holiday',filters={'parent': holiday_list, 'holiday_date': date},fields=['holiday_date', 'weekly_off'])
    if holiday:
        current_year = datetime.datetime.now().year
        end_date = datetime.date(current_year, 12, 31)
        att = frappe.get_doc("Attendance", {"attendance_date": date, "employee": emp})
        if att:
            frappe.errprint("Hello 1")
            if att.status=='Present':
                frappe.errprint("Hello2")
                if att.custom_comp_off == 0:
                    frappe.errprint("Hello3")
                    
                    if frappe.db.exists("Leave Allocation",{"employee": emp, "leave_type": "Compensatory Off","from_date": ('<=', date), "to_date": ('>=', date)}):
                        leave = frappe.get_doc("Leave Allocation",{"employee": emp, "leave_type": "Compensatory Off","from_date": ('<=', date), "to_date": ('>=', date)})
                        leave.new_leaves_allocated += 1
                        leave.save(ignore_permissions=True)
                        if leave.docstatus != 1:
                            leave.submit()
                        frappe.db.commit()
                    else:
                        leave = frappe.new_doc("Leave Allocation")
                        leave.employee = emp
                        leave.from_date = date
                        leave.to_date = end_date
                        leave.new_leaves_allocated = 1
                        leave.leave_type = "Compensatory Off"
                        leave.save(ignore_permissions=True)
                        leave.submit()
                        frappe.db.commit()
                    att = frappe.get_doc("Attendance", {"attendance_date": date, "employee": emp})
                    att.custom_comp_off = 1
                    att.custom_leave_allocation = leave.name
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
            if att.status=='Half Day':
                frappe.errprint("Hello 1")
                if att.custom_comp_off == 0:
                    frappe.errprint("Hello 1")
                    
                    if frappe.db.exists("Leave Allocation",{"employee": emp, "leave_type": "Compensatory Off","from_date": ('<=', date), "to_date": ('>=', date)}):
                        leave = frappe.get_doc("Leave Allocation",{"employee": emp, "leave_type": "Compensatory Off","from_date": ('<=', date), "to_date": ('>=', date)})
                        leave.new_leaves_allocated += 0.5
                        leave.save(ignore_permissions=True)
                        if leave.docstatus != 1:
                            leave.submit()
                        frappe.db.commit()
                    else:
                        leave = frappe.new_doc("Leave Allocation")
                        leave.employee = emp
                        leave.from_date = date
                        leave.to_date = end_date
                        leave.new_leaves_allocated = 0.5
                        leave.leave_type = "Compensatory Off"
                        leave.save(ignore_permissions=True)
                        leave.submit()
                        frappe.db.commit()
                    att = frappe.get_doc("Attendance", {"attendance_date": date, "employee": emp})
                    att.custom_comp_off = 1
                    att.custom_leave_allocation = leave.name
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
        

@frappe.whitelist()
def cancel_comp_off(doc, method):
    if doc.custom_comp_off == 1:
        if frappe.db.exists("Leave Allocation",{"employee": doc.employee, "leave_type": "Compensatory Off","from_date": ('<=', doc.attendance_date), "to_date": ('>=', doc.attendance_date)}):
            leave = frappe.get_doc("Leave Allocation",{"employee": doc.employee, "leave_type": "Compensatory Off","from_date": ('<=', doc.attendance_date), "to_date": ('>=', doc.attendance_date)})
            leave.new_leaves_allocated -= 1
            leave.save(ignore_permissions=True)
            frappe.db.commit()
            att = frappe.get_doc("Attendance", {"attendance_date": doc.attendance_date, "employee": doc.employee})
            att.custom_comp_off = 0
            att.custom_leave_allocation = ''
            att.save(ignore_permissions=True)
            frappe.db.commit()



@frappe.whitelist()
def new_mark_att():
    from_date ='2024-06-01'
    to_date ='2024-06-30'
    attendance =frappe.db.sql("""select name,shift,in_time,out_time,bt_difference,status,leave_application,attendance_request from `tabAttendance` where attendance_date between %s and %s order by attendance_date asc """,(from_date,to_date), as_dict=True)
    for i in attendance:
        # print(i.name)
        frappe.db.set_value('Attendance',i['name'],'shift',"")
        frappe.db.set_value('Attendance',i['name'],'in_time',"00:00:00")
        frappe.db.set_value('Attendance',i['name'],'out_time',"00:00:00")
        frappe.db.set_value('Attendance',i['name'],'bt_difference',"0.0")
        if i.leave_application:
            frappe.db.set_value('Attendance',i['name'],'status',"On Leave")
        elif i.attendance_request:
            frappe.db.set_value('Attendance',i['name'],'status',"Present")
        else:
            frappe.db.set_value('Attendance',i['name'],'status',"Absent")
    print("Ok")





# # # # # # Attendance Permission Correction# # # # # # # 
# @frappe.whitelist()
# def mark_att_manual():
# 	from_date = '2024-06-10'
# 	to_date = '2024-06-10'
# 	# from_date = add_days(today(), -35)  
# 	# to_date = today()
# 	dates = get_dates(from_date, to_date)
# 	for date in dates:
# 		from_date = add_days(date, -1)
# 		to_date = date
# 		checkins = frappe.db.sql("""SELECT * FROM `tabEmployee Checkin` WHERE DATE(time) BETWEEN %s AND %s ORDER BY time""", (from_date, to_date), as_dict=1)
# 		for c in checkins:
# 			employee = frappe.db.exists('Employee', {'status': 'Active', 'date_of_joining': ['<=', from_date], 'name': c.employee})
# 			if employee:
# 				mark_attendance_from_checkin(c.name, c.employee, c.time)
# 	mark_absent(from_date, to_date)



@frappe.whitelist()
def mark_att_present():
    emp_list = frappe.db.get_all('Employee', {'status': 'Active'}, ['name'])
    for emp in emp_list:
        emp_name = emp['name']    
        attendance = frappe.db.get_value('Attendance', {
            'employee': emp_name,
            'attendance_date': '2024-07-15' 
        }, ['name'])
        if attendance:
            att_in = frappe.db.get_value("Attendance", {'name': attendance}, ['in_time'])
            if att_in is not None:
                frappe.db.set_value('Attendance', attendance, 'status', "Present")
        
