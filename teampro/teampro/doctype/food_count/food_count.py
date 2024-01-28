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
			