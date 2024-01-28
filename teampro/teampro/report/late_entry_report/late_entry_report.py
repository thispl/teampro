# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six import string_types
import frappe
from datetime import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,format_date)
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from itertools import count
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta


def execute(filters=None):
	data = []
	columns = get_columns()
	attendance = get_attendance(filters)
	for att in attendance:
		data.append(att)
	return columns, data

def get_columns():
	columns = [
		_("Employee") + ":Data:100",
		_("Employee Name") + ":Data:150",
		_("Date") + ":Data:140",
		_("Shift Time") + ":Data:100",
		_("In Time") + ":Data:100",
		_("Late Time") + ":Data:100"
	]
	return columns

def get_attendance(filters):
	data = []
	if filters.employee:
		user_id = frappe.get_value('Employee',{'employee':filters.employee},['user_id'])
		hod = frappe.get_value('User',{'email':user_id},['name'])
		role = "HOD"
		hod = frappe.get_value('Has Role',{'role':role,'parent':hod})
		if hod:
			if user_id in ['accounts@groupteampro.com','veeramayandi.p@groupteampro.com','rohit.p@groupteampro.com','gayathri.r@groupteampro.com','janisha.g@groupteampro.com','mohamedshajith.j@groupteampro.com','sahayasterwin.a@groupteampro.com','narayanan.m@groupteampro.com','jenisha.p@groupteampro.com','gifty.p@groupteampro.com'] :		
				attendance = frappe.db.sql("""select * from `tabAttendance` where employee = '%s' and time(in_time) > '09:30:00' and attendance_date between '%s' and '%s' """%(filters.employee,filters.from_date,filters.to_date),as_dict=True)
			else:
				attendance = frappe.db.sql("""select * from `tabAttendance` where employee = '%s' and time(in_time) > '09:45:00' and attendance_date between '%s' and '%s' """%(filters.employee,filters.from_date,filters.to_date),as_dict=True)
		else:
			attendance = frappe.db.sql("""select * from `tabAttendance` where employee = '%s' and time(in_time) > '09:30:00' and attendance_date between '%s' and '%s' """%(filters.employee,filters.from_date,filters.to_date),as_dict=True)
		for att in attendance:
			frappe.errprint(att.name)
			if not frappe.db.exists("Attendance Permission",{'employee':att.employee,'permission_date':att.attendance_date,'session':'First Half','workflow_state':'Approved'}):
				att_req = frappe.get_value("Attendance",{'employee':att.employee,'attendance_date':att.attendance_date,'docstatus':1},['attendance_request']) or ''
				leave_app = frappe.get_value("Attendance",{'employee':att.employee,'attendance_date':att.attendance_date,'docstatus':1},['leave_application']) or ''
				if att_req == '' :
					if leave_app == '' :
						if hod:
							if user_id in ['accounts@groupteampro.com','veeramayandi.p@groupteampro.com','rohit.p@groupteampro.com','gayathri.r@groupteampro.com','janisha.g@groupteampro.com','mohamedshajith.j@groupteampro.com','sahayasterwin.a@groupteampro.com','narayanan.m@groupteampro.com','jenisha.p@groupteampro.com','gifty.p@groupteampro.com'] :
								if att.shift and att.in_time:
									shift_time = frappe.get_value("Shift Type",{'name':att.shift},["start_time"])
									get_time = datetime.strptime(str(shift_time),'%H:%M:%S').strftime('%H:%M:%S')
									shift_start_time = dt.datetime.strptime(str(get_time),"%H:%M:%S")
									start_time = dt.datetime.combine(att.attendance_date,shift_start_time.time())
									st_time = start_time.strftime('%H:%M:%S')
									at_time = att.in_time.strftime('%H:%M:%S')
									if att.in_time > start_time:
										late_time = att.in_time - start_time
										row = [att.employee,
										att.employee_name,
										format_date(att.attendance_date),
										st_time,
										at_time,
										late_time]
										data.append(row)
							else:
								if att.shift and att.in_time:
									shift_time = frappe.get_value("Shift Type",{'name':att.shift},["start_time"])
									get_time = datetime.strptime(str(shift_time),'%H:%M:%S').strftime('%H:%M:%S')
									shift_start_time = dt.datetime.strptime(str(get_time),"%H:%M:%S")
									start_time = dt.datetime.combine(att.attendance_date,shift_start_time.time())
									shift_start_plus_15 = start_time + timedelta(minutes=15)
									st_time = start_time.strftime('%H:%M:%S')
									at_time = att.in_time.strftime('%H:%M:%S')
									if att.in_time > start_time:
										late_time = att.in_time - shift_start_plus_15
										row = [att.employee,
										att.employee_name,
										format_date(att.attendance_date),
										"09:45:00",
										at_time,
										late_time]
										data.append(row)
						else:
							if att.shift and att.in_time:
								shift_time = frappe.get_value("Shift Type",{'name':att.shift},["start_time"])
								get_time = datetime.strptime(str(shift_time),'%H:%M:%S').strftime('%H:%M:%S')
								shift_start_time = dt.datetime.strptime(str(get_time),"%H:%M:%S")
								start_time = dt.datetime.combine(att.attendance_date,shift_start_time.time())
								st_time = start_time.strftime('%H:%M:%S')
								at_time = att.in_time.strftime('%H:%M:%S')
								if att.in_time > start_time:
									late_time = att.in_time - start_time
									row = [att.employee,
									att.employee_name,
									format_date(att.attendance_date),
									st_time,
									at_time,
									late_time]
									data.append(row)
	return data