# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe 
from frappe import _, msgprint
from datetime import *
from frappe.utils import data, format_datetime, add_days, today,time_diff


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        _("Employee ID") + ":Data:120",
        _("Employee Name") + ":Data:200",
        _("Department") + ":Data:200",
        _("IN Time") + ":Data:200",
        _("LATE BY") + ":Data:200",
    ]
    return columns

def get_data(filters):
    data = []
    if filters.employee:
        employees = frappe.get_all('Employee',{'status':'Active','name':filters.employee},['name','employee_name','department'])
    else:
        employees = frappe.get_all('Employee',{'status':'Active'},['name','employee_name','department'])
    for emp in employees:
        in_checkin = frappe.db.sql("""select employee,time,shift from `tabEmployee Checkin` where employee= '%s' and date(time) = '%s' order by time""" %(emp.name,filters.date),as_dict=True)
        # in_checkin = frappe.get_all("Employee Checkin",{'employee':emp.name,'log_type':'IN','log_date':filters.date},['employee','time','shift'],order_by='time')
        shift = "G"
        shift_hours = frappe.get_value("Shift Type",{'name':shift},['start_time','end_time'])
        if in_checkin:
            in_time = ''
            late = ''
            start_time = shift_hours[0]
            end_time = shift_hours[1]
            s_time = datetime.strptime(str(start_time),'%H:%M:%S').time()
            e_time = datetime.strptime(str(end_time),'%H:%M:%S').time()
            s_hours = str(s_time) + " - " + str(e_time)
            in_time = (in_checkin[0].time).time()
            if in_time > s_time:
                in_time = str(in_time)
                s_time = str(start_time)
                late_by = time_diff_in_minutes(in_time,s_time)
                late = round(late_by)
                if late >1:
                    late = str(late) + " minutes " 
                    data.append([emp.name,emp.employee_name,emp.department,in_time,late])
    return data

def time_diff_in_minutes(in_time, s_time):
    return time_diff(in_time, s_time).total_seconds() / 60
    

