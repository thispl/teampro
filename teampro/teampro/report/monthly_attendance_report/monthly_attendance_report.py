# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from select import select
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import pandas as pd
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide
import pandas as pd

def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters): 
	columns = [
		_('Emp ID') +':Link/Employee:80',
		_('Emp Name') +':Data:100',
		_('Month Days') +':Float:120',
     	_('Present Days') +':Float:120',
     	_('Leave With Pay') +':Float:120',
	    _('Paid Holidays') +':Float:120',

        _('Leave without Pay') +':Float:120',
        _('Absent Days') +':Float:120',
       	_('Late Deduction Days') +':Float:120',
        _('Final Paid Days') +':Float:120',

		# _('Total Payments Days') +':Float:120',
		# _('Holiday Days') +':Float:120',
		# _('Week Off') +':Float:120',
		# _('Working Days') +':Float:120',
		# _('On Leave') +':Float:120',
		# _('Paid Leave') +':Float:120',
		# _('On Duty/WFH') +':Float:120',
		# _('ATT Permission') +':Float:120',
		# # _('Miss Punch') +':Float:120',
		# _('Late Entry Days') +':Float:120',
		# _('Date of Joining') +':Data:120'
	]
	return columns

def get_data(filters):
	data = []
	# employee = frappe.db.get_all("Employee",{"status":"Active",'date_of_joining':['>=',filters.to_date]},['*'])
	employee = frappe.db.sql("""select * from `tabEmployee` where status = 'Active' and date_of_joining < '%s'"""%(filters.to_date),as_dict = True)
	for emp in employee:
		frappe.errprint(emp.name)
		month_days= 0
		payment_days = 0
		total_payment_days = 0
		late_deduction_days=0
		final_paid_days = 0
		gov_holiday = 0
		weekoff= 0
		working_days=0
		present=0
		absent=0
		on_leave=0
		paid_leave=0
		unpaid_leave=0
		on_duty = 0
		attendance_perm = 0
		# miss_punch = 0
		late_entry_days=0
		dates = get_dates(filters.from_date,filters.to_date)
		late_days=frappe.get_value("Late Penalty",{'emp_name':emp.employee,'from_date':filters.from_date,"to_date":filters.to_date},['deduction_days','late_days','on_duty','permissions','miss_punch'])
		if late_days:
			late_deduction_days =late_days[0]
			late_entry_days=late_days[1]
			on_duty = late_days[2]
			attendance_perm = late_days[3]
			miss_punch = late_days[4]
		for d in dates:
			holiday_list = frappe.db.get_value('Employee',{'name':emp.name},'holiday_list')
			holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
			left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,d),as_dict=True)
			doj= frappe.db.get_value("Employee",{'name':emp.name},"date_of_joining")
			if holiday :
				if doj < holiday[0].holiday_date:
					attendance = frappe.db.exists("Attendance",{'employee':emp.employee,"attendance_date":d,'docstatus':1})
					if attendance: 
						payment_days += 1
						att = frappe.get_doc('Attendance',attendance)
						if att.status=="Present": 
							present += 1 
						if att.status=="Work From Home": 
							present += 1 
						if att.status=="Absent":
							absent += 1
						if att.status== "Half Day" and att.leave_type != "Leave Without Pay":
							present += 1
						if att.status== "Half Day" and att.leave_type == "Leave Without Pay":
							present += 0.5
							unpaid_leave += 0.5
						if att.status== "On Leave":
							on_leave +=1 
						if att.status== "On Leave" and att.leave_type != "Leave Without Pay":
							paid_leave+=1
						if att.status== "On Leave" and att.leave_type == "Leave Without Pay":
							unpaid_leave+=1
					else:
						if holiday[0].weekly_off == 1:
							weekoff += 1 
						else:
							gov_holiday += 1

			else:
				attendance = frappe.db.exists("Attendance",{'employee':emp.employee,"attendance_date":d,'docstatus':1})
				if attendance: 
					payment_days += 1
					att = frappe.get_doc('Attendance',attendance)
					if att.status=="Present": 
						present += 1 
					if att.status=="Work From Home": 
						present += 1 
					if att.status=="Absent":
						absent += 1
					if att.status== "Half Day" and att.leave_type != "Leave Without Pay":
						present += 1
					if att.status== "Half Day" and att.leave_type == "Leave Without Pay":
						present += 0.5
						unpaid_leave += 0.5
					if att.status== "On Leave":
						on_leave +=1 
					if att.status== "On Leave" and att.leave_type != "Leave Without Pay":
						paid_leave+=1
					if att.status== "On Leave" and att.leave_type == "Leave Without Pay":
						unpaid_leave+=1 
				
		working_days= payment_days 
		month_days = payment_days + weekoff + gov_holiday
		total_payment_days=(present+weekoff+paid_leave+gov_holiday)
		final_paid_days = total_payment_days - late_deduction_days
		paid_holiday=weekoff+gov_holiday
		row = [emp.name,
				emp.employee_name,
				month_days,
				present,
				paid_leave,
				paid_holiday,
				unpaid_leave,
				absent,
				late_deduction_days,
            	final_paid_days,

				# total_payment_days,
				# late_deduction_days,
				# final_paid_days,
				# gov_holiday,
				# weekoff,
				# working_days,
				
				# absent,
				# on_leave,
				# unpaid_leave,
				# on_duty,
				# attendance_perm,
				# miss_punch,
				# late_entry_days,
				# emp.date_of_joining
				]
		data.append(row)
	return data

def get_dates(from_date,to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
	return dates

# def check_holiday(date,emp.name):
#     holiday_list = frappe.db.get_value('Employee',{'name':emp.name},'holiday_list')
#     holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
#     left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
#     doj= frappe.db.get_value("Employee",{'name':emp.name},"date_of_joining")
#     status = ''
#     if holiday :
#         if doj < holiday[0].holiday_date:
#             if holiday[0].weekly_off == 1:
#                 status = "WW"     
#             else:
#                 status = "HH"
#         else:
#             status = 'Not Joined'
#     return status









