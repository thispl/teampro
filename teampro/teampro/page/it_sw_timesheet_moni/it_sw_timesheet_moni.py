from __future__ import unicode_literals
import frappe
import json

@frappe.whitelist()
def get_data(args):
	if isinstance(args, str):
		args = json.loads(args)

	filters = []
	values = []
	filters.append("service = %s")
	values.append("IT-SW")

	if args.get("production_date"):
		filters.append("custom_production_date = %s")
		values.append(args["production_date"])

	if args.get("dev_team"):
		filters.append("custom_dev_team = %s")
		values.append(args["dev_team"])

	if args.get("allocated_to"):
		filters.append("custom_allocated_to = %s")
		values.append(args["allocated_to"])

	where_clause = " AND ".join(filters) if filters else "1=1"

	query = f"""
		SELECT name, project, subject, custom_allocated_to, status,
			   expected_time, rt, actual_time, priority, custom_spot_task,
			   status as current_status, custom_remarks, custom_dev_team, custom_sprint
		FROM `tabTask`
		WHERE {where_clause}
		ORDER BY custom_dev_team, custom_allocated_to, priority, project
	"""

	task_data = frappe.db.sql(query, values, as_dict=1)
	data = []
	allocated_task_names = [task.name for task in task_data]

	employee_list = set()

	for task in task_data:
		emp = frappe.get_value("Employee", {"user_id": task.custom_allocated_to}, ["short_code", "name"], as_dict=True)
		short_code = emp.short_code if emp else ""
		emp_name = emp.name if emp else ""
		spot_task=task.custom_spot_task
		spot_task = frappe.db.get_value('Sprint Task',{'production_date':args.get("production_date"),'task':task.name,'cb':short_code},['spot_task']) or 1

		if emp_name:
			employee_list.add(emp_name)

		actual_time = frappe.db.sql("""
			SELECT SUM(d.hours) AS hours
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus = 1 AND t.employee = %s AND d.task = %s
		""", (emp_name, task.name), as_dict=1)[0].hours or 0

		today_at = frappe.db.sql("""
			SELECT SUM(d.hours) AS hours
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
		""", (args["production_date"], emp_name, task.name), as_dict=1)[0].hours or 0

		today_rt = frappe.db.sql("""
			SELECT SUM(a.today_rt) AS hours
			FROM `tabAllocated Tasks` a
			JOIN `tabDaily Monitor` m ON a.parent = m.name
			WHERE m.docstatus != 2 AND m.date = %s AND m.dev_team = %s AND a.id = %s AND m.sprint = %s
		""", (args["production_date"], task.custom_dev_team, task.name, task.custom_sprint), as_dict=1)[0].hours or 0

		data.append([
			task.name, task.project, task.subject, short_code, "Working",
			round(task.expected_time or 0, 2), round(task.rt or 0, 2),
			round(actual_time, 2), task.priority, task.custom_spot_task,
			task.current_status, task.custom_remarks, task.custom_dev_team,
			round(today_at, 2), round(today_rt, 2)
		])

	# ----------------------------------------
	# Additional Timesheet Tasks and Issues
	# ----------------------------------------
	for emp_name in set(employee_list):
		if not emp_name:
			continue

		short_code = frappe.get_value("Employee", emp_name, "short_code") or ""
		dev_team = frappe.get_value("Employee", emp_name, "custom_dev_team") or ""
		not_in_tasks = tuple(allocated_task_names) if allocated_task_names else ("",)

		# Additional Timesheet Tasks
		timesheet_tasks = frappe.db.sql("""
			SELECT DISTINCT d.task, d.activity_type, d.project, d.subject, d.task_status
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task NOT IN %s
		""", (args["production_date"], emp_name, not_in_tasks), as_dict=True)

		for row in timesheet_tasks:
			priority = frappe.get_value("Task", row.task, "priority") or ''
			spot_task = frappe.get_value("Task", row.task, "custom_spot_task") or ''
			spot_task = frappe.db.get_value('Sprint Task',{'production_date':args.get("production_date"),'task':row.name,'cb':short_code},['spot_task']) or 1
			today_at = frappe.db.sql("""
				SELECT SUM(d.hours) AS hours
				FROM `tabTimesheet Detail` d
				JOIN `tabTimesheet` t ON d.parent = t.name
				WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
			""", (args["production_date"], emp_name, row.task), as_dict=1)[0].hours or 0

			if row.activity_type == "Manual Testing":
				status = "Pending Review"
			elif row.activity_type == "Code Review":
				status = "Code Review"
			else:
				status = "Working"

			data.append([
				row.task, row.project, row.subject, short_code, status,
				0, 0, 0, priority, spot_task,
				row.task_status, '', dev_team,
				round(today_at, 2), 0
			])

		# Timesheet Issues
		timesheet_issues = frappe.db.sql("""
			SELECT DISTINCT d.custom_issue, d.activity_type, d.project, d.custom_subject_issue
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.custom_issue IS NOT NULL
		""", (args["production_date"], emp_name), as_dict=True)

		for row in timesheet_issues:
			priority = frappe.get_value("Issue", row.custom_issue, "priority") or ''
			current_status = frappe.get_value("Issue", row.custom_issue, "status") or ''
			today_at = frappe.db.sql("""
				SELECT SUM(d.hours) AS hours
				FROM `tabTimesheet Detail` d
				JOIN `tabTimesheet` t ON d.parent = t.name
				WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.custom_issue = %s
			""", (args["production_date"], emp_name, row.custom_issue), as_dict=1)[0].hours or 0

			data.append([
				row.custom_issue, row.project, row.custom_subject_issue, short_code, "Working",
				0, 0, 0, priority, 1,
				current_status, '', dev_team,
				round(today_at, 2), 0
			])

	return data
