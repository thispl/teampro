# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		_("Employee") + ":Data:100",
		_("CB") + ":Data:100",
		_("Project") + ":Data:200",
		_("Task") + ":Data:150",
		_("Subject") + ":Data:200",
		_("Priority") + ":Data:120",
		_("Status") + ":Data:100",
		_("Revisions") + ":Data:100",
		_("RT") + ":Float:100",
		_("AT(Total)") + ":Float:100",
		_("AT(Period)") + ":Float:100",
		_("ET Vs AT %") + ":Float:100"
	]


def get_data(filters):
	data = []
	if not filters.get("from_date") or not filters.get("to_date"):
		return data

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	dev_team = filters.get("team")
	if filters.get("user"):
		filter_cb=frappe.db.get_value('Employee',{'user_id':filters.get("user")},['short_code'])
	else:
		filter_cb=''
	conditions = """
		workflow_state != 'Cancelled'
		AND (
			(from_date BETWEEN %(from_date)s AND %(to_date)s)
			OR
			(to_date BETWEEN %(from_date)s AND %(to_date)s)
			OR
			(from_date <= %(from_date)s AND to_date >= %(to_date)s)
		)
	"""
	if dev_team:
		conditions += " AND team = %(team)s"
	sql = f"""
		SELECT name
		FROM `tabSprint`
		WHERE {conditions}
	"""
	params = {
		"from_date": from_date,
		"to_date": to_date
	}
	if dev_team:
		params["team"] = dev_team
	sprints = frappe.db.sql(sql, params, as_dict=True)
	sprint_names = [s["name"] for s in sprints]

	if not sprint_names:
		return data
	sql = """
		SELECT 
			`task`,
			`subject`,
			`cb`,
			`cr_status`,
			SUM(`rt`) AS summed_rt,
			SUM(`at_period`) AS at_period,
			`project`,
			`priority`
		FROM `tabSprint Task`
		WHERE parenttype = 'Sprint'
		AND parent IN %(sprint_names)s
		GROUP BY `cb`, `task`, `subject`,  `project`
	"""
	

	tasks = frappe.db.sql(sql, {"sprint_names": tuple(sprint_names)}, as_dict=True)

	for t in tasks:
		if filter_cb and filter_cb!=t.cb:
			continue
		emp_id=''
		if t.cb:
			emp_id=frappe.db.get_value('Employee',{'short_code':t.cb},['name'])
		else:
			emp_id=''
		if frappe.db.exists('Task',{'name':t.task}):
			rev=frappe.db.get_value('Task',{'name':t.task},['revisions'])
			tot_at=frappe.db.get_value('Task',{'name':t.task},['actual_time'])
			cr_status=frappe.db.get_value('Task',{'name':t.task},['status'])
			sub=t.subject
			prior=t.priority
			if t.summed_rt == 0:
				tot_rt=0.5
			else:
				tot_rt=t.summed_rt
		elif frappe.db.exists('Issue',{'name':t.task}):
			rev=0
			tot_at= frappe.db.sql("""
				SELECT SUM(cs.hours) as total FROM `tabTimesheet` c
				INNER JOIN `tabTimesheet Detail` cs ON c.name = cs.parent
				WHERE cs.custom_issue=%s AND c.employee=%s AND c.start_date BETWEEN %s AND %s
			""", (t.task, emp_id,from_date,to_date), as_dict=True)[0].total or 0.0
			cr_status=frappe.db.get_value('Issue',{'name':t.task},['custom_issue_status'])
			sub=frappe.db.get_value('Issue',{'name':t.task},['subject'])
			prior=frappe.db.get_value('Issue',{'name':t.task},['priority'])
			if t.summed_rt == 0:
				tot_rt=0.5
			else:
				tot_rt=t.summed_rt
		else:
			rev=0
			tot_at=0
			cr_status="Completed"
			sub=''
			prior=''
			tot_rt=0.5
		atet=0	
		if t.summed_rt and t.summed_rt>0:
			at=t.at_period if t.at_period else 0
			per=(at/t.summed_rt)*100
			atet=round(per,2)
		row = [
			emp_id,                   
			t.cb,
			t.project,
			t.task,
			sub,
			prior,                   
			cr_status,
			rev,                    
			tot_rt,
			tot_at,                    
			t.at_period,
			atet,                    
		]
		data.append(row)

	return data