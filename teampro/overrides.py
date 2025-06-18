import frappe

import datetime
from frappe.utils import nowdate
import frappe

from erpnext.projects.doctype.task.task import Task
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication
from hrms.hr.doctype.attendance_request.attendance_request import AttendanceRequest
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from frappe.desk.doctype.event.event import Event
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day,today

class CustomTask(Task):
    def update_status(self):
        if self.status not in ('Cancelled', 'Completed','Hold','Pending Review','Code Review') and self.exp_end_date:
            from datetime import datetime
            if self.exp_end_date < datetime.now().date():
                self.db_set('status', 'Overdue', update_modified=False)
                self.update_project()

class customEvent(Event):
    def has_permission(self,user=None):
        user=frappe.session.user
        if self.event_type == "Public" or self.owner == user:
            return True
        return True


    
class CustomLeaveApplication(LeaveApplication):
    def validate(self):
        current_time = datetime.datetime.now()
        current_date = today()
        if isinstance(current_date, str): 
            current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
        current_month = current_time.month
        current_year = current_time.year
        if current_month == 1:
            previous_month = 12
            previous_month_year = current_year - 1
        else:
            previous_month = current_month - 1
            previous_month_year = current_year
        if self.from_date: 
            if isinstance(self.from_date, str):
                from_date = datetime.datetime.strptime(self.from_date, "%Y-%m-%d").date()
            else:
                from_date = self.from_date
            if from_date < current_date:
                # if current_date.day == 1:
                #     # from_date = datetime.datetime.strptime(self.from_date, "%Y-%m-%d")
                #     if from_date.year == previous_month_year and from_date.month == previous_month:
                #         if current_time.hour >= 10 and current_time.minute > 0:
                #             frappe.throw("Leave applications for the previous month are not allowed.")
                # else:
                #     if current_date.day > 1 and from_date.year == previous_month_year and from_date.month == previous_month:
                #         frappe.throw("Leave applications for the previous month are not allowed.")
                first_date = datetime.date(current_year, current_month, 1)
                check_date = first_date
                while check_holiday(check_date, self.employee):
                    check_date = add_days(check_date, 1)

                if current_date == check_date:
                    if from_date.year == previous_month_year and from_date.month == previous_month:
                        if current_time.hour >= 10 and current_time.minute > 0:
                            frappe.throw("Leave applications for the previous month are not allowed.")
                else:
                    if current_date.day > check_date.day and from_date.year == previous_month_year and from_date.month == previous_month:
                        frappe.throw("Leave applications for the previous month are not allowed.")


class CustomAttendanceRequest(AttendanceRequest):
    def validate(self):
        current_time = datetime.datetime.now()
        current_date = today()
        if isinstance(current_date, str): 
            current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
        current_month = current_time.month
        current_year = current_time.year
        if current_month == 1:
            previous_month = 12
            previous_month_year = current_year - 1
        else:
            previous_month = current_month - 1
            previous_month_year = current_year
        if self.from_date:
            if isinstance(self.from_date, str):
                from_date = datetime.datetime.strptime(self.from_date, "%Y-%m-%d").date()
            else:
                from_date = self.from_date
            if from_date < current_date:
                # if current_date.day == 1:
                #     if from_date.year == previous_month_year and from_date.month == previous_month:
                #         if current_time.hour >= 10 and current_time.minute > 0:
                #             frappe.throw("Attendance Request for the previous month are not allowed.")
                # else:
                #     if current_date.day > 1 and from_date.year == previous_month_year and from_date.month == previous_month:
                #         frappe.throw("Attendance Request for the previous month are not allowed")
                first_date = datetime.date(current_year, current_month, 1)
                check_date = first_date
                while check_holiday(check_date, self.employee):
                    check_date = add_days(check_date, 1)

                if current_date == check_date:
                    if from_date.year == previous_month_year and from_date.month == previous_month:
                        if current_time.hour >= 10 and current_time.minute > 0:
                            frappe.throw("Attendance Request for the previous month are not allowed")
                else:
                    if current_date.day > check_date.day and from_date.year == previous_month_year and from_date.month == previous_month:
                        frappe.throw("Attendance Request for the previous month are not allowed")

@frappe.whitelist()
def check_holiday(date, emp):
    holiday_list = frappe.db.get_value('Employee', emp, 'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return True
        else:
            return True
    else:
        return False  