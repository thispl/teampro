# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe import _
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,get_time,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today, format_date)

class FoodCount(Document):
    def before_save(self):
        today_time = datetime.now()
        current_time = today_time.strftime("%H:%M:%S")
        food_time = get_time('10:30:00')
        if get_time(current_time) > food_time:
            frappe.throw(_('Time Out'))
        else:
            self.duplicate_not_allow()
                

    def duplicate_not_allow(self):
        food_count = frappe.db.exists('Food Count',{'employee':self.employee,'date':self.date})
        if food_count:
            frappe.throw(_('Already food applied'))	
   
@frappe.whitelist()
def create_food_count():
    from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
    holiday_list_name = 'TEAMPRO 2023'
    start_date = getdate(today())
    if not is_holiday(holiday_list_name, start_date):
        emp = ["TI00149"]
        for i in emp:
            if not frappe.db.exists("Food Count",{'employee':i,'date':nowdate()}):
                doc = frappe.new_doc("Food Count")
                doc.employee = i
                doc.department="IT"
                doc.date = nowdate()
                doc.save(ignore_permissions=True)

            