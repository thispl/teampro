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


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
		_("Employee") + ":Data/:150",
		_("CB") +":Data/:150",
		_("Project") + ":Data/:150",
		_("Task ID") + ":Data/:150",
		_("Subject") + ":Data/:200",
		_("Priority") + ":Data/:200",
		_("Status") + ":Data/:150",
		_("Revisions") + ":Data/:150",
		_("ET") + ":Data/:150",
		_("AT(Total)") + ":Data/:150",
		_("AT(Period)") + ":Data/:150",
		_("ET Vs AT") + ":Data/:150",
		_("ET Vs AT %" )+":Data/:150",
	]
	return columns

def get_data(filters):
	data = []
	if filters.completed_by:
		emp = frappe.get_value("Employee",{'user_id':filters['completed_by'],'status':'Active'},['name'])
		if emp:
			row = []
			timesheet = frappe.db.sql(""" select `tabTimesheet Detail`.task as task,`tabTimesheet Detail`.custom_issue as issue,`tabTimesheet Detail`.custom_meeting as meeting,sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and  employee = '%s' and start_date between '%s' and '%s' group by `tabTimesheet Detail`.task,`tabTimesheet Detail`.custom_issue"""%(emp,filters.from_date,filters.to_date),as_dict = 1)
			for j in timesheet:
				task = frappe.get_value("Task",{'name':j.task},['project','subject','priority','status','revisions','expected_time'])
				issue = frappe.get_value("Issue",{'name':j.issue},['project','subject','priority','status'])
				meeting=frappe.get_value("Meeting",{'name':j.meeting},['project','title','status'])
				emp_short_code=frappe.db.get_value("Employee",{"name":emp},["short_code"])
				if task:	
					actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.task = '%s' """%(j.task),as_dict = 1) or ''
					for at in actual_time:
						atime = at.hours or 0
						ettime=atime-task[5]
						if task[5] and task[5] > 0:
							etper=(atime/task[5])*100
						else:
							etper = 0
						row = [emp,emp_short_code,task[0],j.task,task[1],task[2],task[3],task[4],task[5],round(atime,2),round(j.hours,2),round(ettime,2),round(etper,2)]
						data.append(row)
				if issue:
					actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.custom_issue = '%s' """%(j.issue),as_dict = 1) or ''
					for at in actual_time:
						atime = at.hours or 0
						ettime=0.5-atime
						etper=(atime/0.5)*100
						row = [emp,emp_short_code,issue[0],j.issue,issue[1],issue[2],issue[3],'NA',0.5,round(atime,2),round(j.hours,2),round(ettime,2),round(etper,2)]
						data.append(row)
				if meeting:
					actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.custom_meeting = '%s' """%(j.meeting),as_dict = 1) or ''
					for at in actual_time:
						atime = at.hours or 0
						row = [emp,emp_short_code,meeting[0],j.meeting,meeting[1],'',meeting[2],'NA','',round(atime,2),round(j.hours,2),'','']
						data.append(row)
	else:
		emp = frappe.get_all("Employee",{'department':"IT. Development - THIS",'status':"Active"},['name',"employee_name",'short_code'])
		for e in emp:
			if e.short_code not in ['JA','SM']:
				row = []
				timesheet = frappe.db.sql(""" select `tabTimesheet Detail`.task as task,`tabTimesheet Detail`.custom_issue as issue,`tabTimesheet Detail`.custom_meeting as meeting,sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent  where `tabTimesheet`.docstatus = 1 and employee = '%s' and start_date between '%s' and '%s' group by `tabTimesheet Detail`.task,`tabTimesheet Detail`.custom_issue"""%(e.name,filters.from_date,filters.to_date),as_dict = 1)
				for j in timesheet:
					task = frappe.get_value("Task",{'name':j.task},['project','subject','priority','status','revisions','expected_time'])
					issue = frappe.get_value("Issue",{'name':j.issue},['project','subject','priority','status'])
					meeting=frappe.get_value("Meeting",{'name':j.meeting},['project','title','status'])
					if task:
						actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent  where `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.task = '%s' """%(j.task),as_dict = 1)
						for at in actual_time:
							atime = at.hours or 0
							ettime=atime-task[5]
							if task[5] and task[5] > 0:
								etper=(atime/task[5])*100
							else:
								etper = 0
							row = [e.name or '',e.short_code or '',task[0] or '',j.task or '',task[1] or '',task[2] or '',task[3] or '',task[4] or '',task[5] or '',round(atime,2) or '',round(j.hours,2) or '',round(ettime,2) or '',round(etper,2) or '']
							data.append(row)
					if issue:
						# actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.custom_issue = '%s' """%(j.issue),as_dict = 1) or ''
						actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet` left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.custom_issue = '%s' and `tabTimesheet Detail`.task IS NULL """%(j.issue),as_dict = 1) or ''
						for at in actual_time:
							atime = at.hours or 0
							ettime=0.5-atime
							etper=(atime/0.5)*100
							row = [e.name,e.short_code,issue[0],j.issue,issue[1],issue[2],issue[3],'NA',0.5,round(atime,2),round(j.hours,2),round(ettime,2 ),round(etper,2)]
							data.append(row)
					if meeting:
						actual_time = frappe.db.sql(""" select sum(`tabTimesheet Detail`.hours) as hours from `tabTimesheet`	left join `tabTimesheet Detail` on `tabTimesheet`.name = `tabTimesheet Detail`.parent where  `tabTimesheet`.docstatus = 1 and `tabTimesheet Detail`.activity_type != "Manual Testing" and `tabTimesheet Detail`.custom_meeting = '%s' """%(j.meeting),as_dict = 1) or ''
						for at in actual_time:
							atime = at.hours or 0
							row = [e.name,e.short_code,meeting[0],j.meeting,meeting[1],'',meeting[2],'NA','',round(atime,2),round(j.hours,2),'','']
							data.append(row)

	return data
	
