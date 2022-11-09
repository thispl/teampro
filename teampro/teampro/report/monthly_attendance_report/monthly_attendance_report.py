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
# from __future__ import unicode_literals
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
        _('Payments Days') +':Data:80',
        _('Holiday Days') +':Data:80',
        _('Week Off') +':Data:80',
        _('Working Days') +':Data:80',
        _('Present Days') +':Data:80',
        _('Absent Days') +':Data:80',
        _('On Leave') +':Data:80',
        _('LOP') +':Data:80',
        _('CL/C Off') +':Data:80',
        _('Total Payments Days') +':Data:120',
    ]
    return columns


def get_data(filters):
    data = []
    employee = frappe.db.get_all("Employee",{"status":"Active"},['*'])
    frappe.errprint('hi')
    for emp in employee:
        frappe.errprint(emp.employee)
        present=0
        absent=0
        on_leave=0
        weekoff= 0
        payment_days=0
        working_days=0
        paid_leave=0
        unpaid_leave=0
        gov_holiday = 0
        total_payment_days=0
        # single_punch=0
        # late_entry_days=0
        # late_deduction_days=0
        date_range = pd.date_range(filters.from_date,filters.to_date).tolist()
        # late_days=frappe.get_value("Late Penalty",{'emp_name':emp.employee,'from_date':filters.from_date,"to_date":filters.to_date},['deduction_days','late_days'])
        # if late_days:
        #     late_entry_days=late_days[1]
        #     late_deduction_days =late_days[0]
        holiday_list = frappe.db.exists('Holiday List',{'employee':emp.employee})
        frappe.errprint(holiday_list)
        if holiday_list:
            emp_holiday_list = frappe.get_value('Company',emp.company,'default_holiday_list')
        else:
            emp_holiday_list = frappe.get_value('Company',emp.company,'default_holiday_list')
        for d in date_range:
            payment_days+=1  
            attendance = frappe.db.exists("Attendance",{'employee':emp.employee,"attendance_date":d})
            if attendance:   
                att = frappe.get_doc('Attendance',attendance)
                if att.status=="Present" or att.status=="Work from Home":
                    present += 1    
                if att.status=="Absent":
                    absent += 1
                if att.status== "On Leave" :
                    on_leave +=1 
                if att.status== "On Leave" and att.leave_type == "Casual Leave":
                    paid_leave+=1
                if att.status== "On Leave" and att.leave_type == "Compensatory Off":
                    paid_leave+=1
                if att.status== "On Leave" and att.leave_type == "Leave Without Pay":
                    unpaid_leave+=1 
                # miss_punch= frappe.db.sql("""
                # select
                #     att.employee,
                #     att.employee_name,
                #     att.attendance_date,
                #     att.in_time,
                #     att.out_time,
                #     att.status
                # from
                #     `tabAttendance` att
                #     join `tabEmployee` emp on emp.name = att.employee
                #     where
                #     att.attendance_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
                #     and emp.status = 'Active'
                #     and (in_time or out_time) is null
                # """, as_dict=1)
                # if miss_punch:
                #     single_punch+=1       
            else:
                absent += 1
            holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
            left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(emp_holiday_list,d),as_dict=True)
            if holiday:
                frappe.errprint(holiday[0].weekly_off)  
                if holiday[0].weekly_off ==1:
#              		frappe.errprint(holiday[0].weekly_off)
                    weekoff += 1   
                else:
                    gov_holiday += 1

        get_days = weekoff+gov_holiday
        working_days= payment_days-get_days
        ab_days = present+on_leave
        absent = working_days-ab_days
        total_payment_days=present+weekoff+paid_leave+gov_holiday
        # late_entry_days=late_days[1] 
        # late_deduction_days=late_days[0]   
        row = [emp.name,emp.employee_name,payment_days,gov_holiday,weekoff,working_days,present,absent,on_leave,unpaid_leave,paid_leave,total_payment_days]
        data.append(row)
    return data
                       




   






