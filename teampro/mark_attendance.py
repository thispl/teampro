import frappe
from datetime import datetime
from frappe.utils.data import today, add_days, add_years
from dateutil.relativedelta import relativedelta
from datetime import timedelta, time,date
from frappe.utils import time_diff_in_hours, formatdate, get_first_day,get_last_day, nowdate, now_datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe.utils import time_diff


@frappe.whitelist()
def cron_job1():
	job = frappe.db.exists('Scheduled Job Type', 'mark_att')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'teampro.mark_attendance.mark_att',
			"frequency" : 'Cron',
			"cron_format" : '*/10 * * * *'
		})
		sjt.save(ignore_permissions=True)

@frappe.whitelist()
def mark_att():
	# from_date = '2023-10-01'
	# to_date = '2023-10-30'
	from_date = add_days(today(),-40)  
	to_date = today()
	dates = get_dates(from_date,to_date)
	for date in dates:
		from_date = add_days(date,-1)
		to_date = date
		checkins = frappe.db.sql(
			"""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=1)
		for c in checkins:
			employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
			if employee:  
				print(c.name)
				mark_attendance_from_checkin(c.name,c.employee,c.time)
	mark_absent(from_date,to_date)                                

def mark_attendance_from_checkin(checkin,employee,time):
	att_time = time.time()
	att_date = time.date()
	print(att_date)
	in_time = ''
	out_time = ''
	checkins = frappe.db.sql("""select name,time from `tabEmployee Checkin` where employee = "%s" and date(time) = '%s' order by time """%(employee,att_date),as_dict=True)
	if checkins:
		if len(checkins) >= 2:
			in_time = checkins[0].time
			out_time = checkins[-1].time
		elif len(checkins) == 1:
			in_time = checkins[0].time
		att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date})
		status = "Absent"
		if not att:
			if in_time and out_time:  
				value = time_diff(out_time,in_time)
				val = value.total_seconds() / 3600
				frappe.errprint(type(val))
				if val < 4 :
					status = "Absent"
				elif val > 4 and val < 8 :
					status = "Half Day"	
				elif val > 8:
					status = "Present"	
			else:
				val = 0.0
				status = "Absent"
			att = frappe.new_doc("Attendance")
			att.employee = employee
			att.attendance_date = att_date
			att.shift = 'G'
			att.status = status
			att.in_time = in_time
			att.out_time = out_time
			att.bt_difference = val
			att.save(ignore_permissions=True)
			frappe.db.commit()
			frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
			frappe.db.set_value('Employee Checkin',checkin,'attendance',att.name)
			return att.name
		else:
			if in_time:
				frappe.db.set_value("Attendance",att,'in_time',in_time)
			if out_time:
				frappe.db.set_value("Attendance",att,'out_time',out_time)
			if in_time and out_time:  
				value = time_diff(out_time,in_time)
				val = value.total_seconds() / 3600
				frappe.errprint(type(val))
				if val < 4 :
					status = "Absent"
				elif val > 4 :
					status = "Present"
			else:
				val = 0.0
				status = "Absent"
			frappe.db.set_value("Attendance",att,'shift','G')
			frappe.db.set_value("Attendance",att,'bt_difference',val)
			frappe.db.set_value("Attendance",att,'status',status)
			frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
			frappe.db.commit()
			frappe.db.set_value('Employee Checkin',checkin,'attendance',att)
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
