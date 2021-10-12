import frappe
from datetime import datetime
from frappe.utils.data import today, add_days, add_years
from dateutil.relativedelta import relativedelta
from datetime import timedelta, time,date
from frappe.utils import time_diff_in_hours, formatdate, get_first_day,get_last_day, nowdate, now_datetime


@frappe.whitelist()
def previous_mark_att():
    nowday = add_days(nowdate(),-1)
    from_date=get_first_day(nowday)
    to_date=get_last_day(nowday)
    frappe.errprint(from_date)
    frappe.errprint(to_date)
    checkins = frappe.db.sql(
        """select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=1)
    if checkins:
        for c in checkins:
            att = mark_attendance_from_checkin(c.name,c.employee,c.time)
            if att:
                frappe.db.set_value("Employee Checkin",
                                    c.name, "skip_auto_attendance", "1")

@frappe.whitelist()
def mark_att():
    from_date=get_first_day(nowdate())
    to_date=nowdate()
    checkins = frappe.db.sql(
        """select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=1)
    if checkins:
        for c in checkins:
            att = mark_attendance_from_checkin(c.name,c.employee,c.time)
            if att:
                frappe.db.set_value("Employee Checkin",
                                    c.name, "skip_auto_attendance", "1")

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
        if in_time and out_time:
            status = 'Present'
        else:
            status = 'Absent'
        att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':0})
        if not att:
            att = frappe.new_doc("Attendance")
            att.employee = employee
            att.attendance_date = att_date
            att.shift = 'G'
            att.status = status
            att.in_time = in_time
            att.out_time = out_time
            att.save(ignore_permissions=True)
            frappe.db.commit()
            return att.name
        else:
            if in_time:
                frappe.db.set_value("Attendance",att,'in_time',in_time)
            if out_time:
                frappe.db.set_value("Attendance",att,'out_time',out_time)
            frappe.db.set_value("Attendance",att,'shift','G')
            frappe.db.set_value("Attendance",att,'status',status)
            return att