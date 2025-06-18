# Copyright (c) 2023, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
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
from frappe.utils import getdate



def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
		_("S.No") + ":Data/:150",
		_("Employee ID") + ":Data/:200",
		_("Employee Name") + ":Data/:150",
		_("Opt-in for Food") + ":Data/:150",
		_("Attendance") + ":Data/:150",
		_("Food Request") + ":Data/:150",
	]
	return columns

def get_data(filters):
	data = []
	emp = frappe.db.sql("""select * from `tabEmployee` where status = 'Active'""",as_dict = 1)
	if emp:
		i=1
		for e in emp:
			row = []
			opt_in = ''
			att = ''
			food = ""
			if e.opt_in_for_food == 1:
				opt_in = 'Y'
			else:
				opt_in = 'N'
			date = "%"+filters.date+"%"
			if frappe.db.exists("Employee Checkin",{"employee": e.name,"time":["like",date]}):

				att = "Y"
			else:
				att = "N"
			if frappe.db.exists("Food Count",{"date":filters.date,"employee":e.name}):
				food = "Y"
			else:
				food = "N"


			row = [i,e.name,e.employee_name,opt_in,att,food]
			i += 1
			data.append(row)
		
		
	return data