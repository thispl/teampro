import frappe
from frappe.utils import getdate, nowdate, formatdate
from datetime import datetime, date
from frappe.utils import today
from io import BytesIO
from itertools import groupby
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side


@frappe.whitelist()
def get_project_counts():
	result = []
	total_filters = {
			"status": ["not in", ["Hold", "Completed", "Cancelled"]],
			"service": "IT-SW",
			"project_type": ["is","set"]
		}
	total = frappe.db.count("Project", filters=total_filters)

	
	project_types = frappe.db.get_all('Project Type', {'sequence_number': ['!=', 0]}, ['name'], order_by='sequence_number')

	for project_type in project_types:
		filters = {
			"status": ["not in", ["Hold", "Completed", "Cancelled"]],
			"service": "IT-SW",
			"project_type": project_type.name
		}
		count = frappe.db.count("Project", filters=filters)
		result.append({
			"project_type": project_type.name,
			"count": count
		})

	return {"total":total ,"projects": result}


@frappe.whitelist()
def get_sprint_counts():
	dev_teams = frappe.db.get_all('Dev Team',{"team_name": ["!=", "Others"]},["team_name"],order_by='team_name')
	sprint_data = []

	for team in dev_teams:
		active_sprint = frappe.db.get_value(
			'Sprint',
			{'team': team.team_name, 'status': 'In Progress'},
			['sprint_id'],
			order_by='creation desc'
		)

		in_progress_sprint = frappe.db.get_value(
			'Sprint',
			{'team': team.team_name, 'status': 'In Progress'},
			['sprint_id'],
			order_by='creation asc'
		)
		if active_sprint == in_progress_sprint :
			in_progress_sprint =''

		sprint_data.append({
			"team": team.team_name,
			"active": active_sprint,
			"in_progress": in_progress_sprint
		})

	return {"sprints": sprint_data}



# @frappe.whitelist()
# def get_task_summary():
# 	# Define mappings
# 	status_map = {
# 		"Open": "open",
# 		"Working": "working",
# 		"Overdue": "working",
# 		"Code Review": "working",
# 		"Pending Review": "pr",
# 		"Client Review": "cr"
# 	}

# 	# Initialize summary
# 	summary = {
# 		"total": 0,
# 		"open": 0,
# 		"working": 0,
# 		"pr": 0,
# 		"cr": 0,
# 		"open_total_hours": 0,
# 		"working_total_hours": 0,
# 		"pr_total_hours": 0,
# 		"cr_total_hours": 0,
# 	}

# 	# Get total count and hours
# 	total_data = frappe.db.sql("""
# 		SELECT COUNT(*) AS count, SUM(rt) AS total_hours
# 		FROM `tabTask`
# 		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
# 		AND service = 'IT-SW'
# 	""", as_dict=True)[0]

# 	summary["total"] = total_data.count or 0
# 	summary["total_total_hours"] = total_data.total_hours or 0

# 	# Fetch grouped data in one go
# 	grouped_data = frappe.db.sql("""
# 		SELECT status, COUNT(*) AS count, SUM(rt) AS total_hours
# 		FROM `tabTask`
# 		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
# 		AND service = 'IT-SW'
# 		GROUP BY status
# 	""", as_dict=True)

# 	for row in grouped_data:
# 		key = status_map.get(row.status)
# 		if key:
# 			summary[key] += row.count or 0
# 			summary[f"{key}_total_hours"] += float(row.total_hours or 0)

# 	return summary


@frappe.whitelist()
def get_task_summary():

	from frappe.utils import nowdate

	today = nowdate()

	# Define mappings
	status_map = {
		"Open": "open",
		"Working": "working",
		"Overdue": "working",
		"Code Review": "working",
		"Pending Review": "pr",
		"Client Review": "cr"
	}

	# Initialize summary
	summary = {
		"total": 0,
		"open": 0,
		"working": 0,
		"pr": 0,
		"cr": 0,

		"total_total_hours": 0,
		"open_total_hours": 0,
		"working_total_hours": 0,
		"pr_total_hours": 0,
		"cr_total_hours": 0,

		# Today Counts
		"total_today_count": 0,
		"open_today_count": 0,
		"working_today_count": 0,
		"pr_today_count": 0,
		"cr_today_count": 0,

		# Today Hours
		"total_today_hours": 0,
		"open_today_hours": 0,
		"working_today_hours": 0,
		"pr_today_hours": 0,
		"cr_today_hours": 0,
	}

	# Overall Total
	total_data = frappe.db.sql("""
		SELECT 
			COUNT(*) AS count, 
			COALESCE(SUM(rt),0) AS total_hours
		FROM `tabTask`
		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
		AND service = 'IT-SW'
	""", as_dict=True)[0]

	summary["total"] = total_data.count or 0
	summary["total_total_hours"] = float(total_data.total_hours or 0)

	# Today Total
	today_total_data = frappe.db.sql("""
		SELECT 
			COUNT(*) AS count,
			COALESCE(SUM(rt),0) AS total_hours
		FROM `tabTask`
		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
		AND service = 'IT-SW'
		AND DATE(custom_production_date) = %s
	""", today, as_dict=True)[0]

	summary["total_today_count"] = today_total_data.count or 0
	summary["total_today_hours"] = float(today_total_data.total_hours or 0)

	# Overall grouped data
	grouped_data = frappe.db.sql("""
		SELECT 
			status,
			COUNT(*) AS count,
			COALESCE(SUM(rt),0) AS total_hours
		FROM `tabTask`
		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
		AND service = 'IT-SW'
		GROUP BY status
	""", as_dict=True)

	for row in grouped_data:
		key = status_map.get(row.status)

		if key:
			summary[key] += row.count or 0
			summary[f"{key}_total_hours"] += float(row.total_hours or 0)

	# Today grouped data
	today_grouped_data = frappe.db.sql("""
		SELECT 
			status,
			COUNT(*) AS count,
			COALESCE(SUM(rt),0) AS total_hours
		FROM `tabTask`
		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
		AND service = 'IT-SW'
		AND DATE(custom_production_date) = %s
		GROUP BY status
	""", today, as_dict=True)

	for row in today_grouped_data:

		key = status_map.get(row.status)

		if key:
			summary[f"{key}_today_count"] += row.count or 0
			summary[f"{key}_today_hours"] += float(row.total_hours or 0)

	return summary


@frappe.whitelist()
def get_tasks_project_wise(type=None):
	status_map = {
		"open": ["Open"],
		"working": ["Working", "Overdue", "Code Review"],
		"pr": ["Pending Review"],
		"cr": ["Client Review"]
	}

	if type == "total":
		return frappe.db.sql("""
			SELECT project, COUNT(name) AS task_count, SUM(rt) AS total_hours
			FROM `tabTask`
			WHERE status NOT IN ('Completed', 'Cancelled','Hold')
			AND service = 'IT-SW'
			GROUP BY project
		""", as_dict=True)

	if type in status_map:
		return frappe.db.sql("""
			SELECT project, COUNT(name) AS task_count, SUM(rt) AS total_hours
			FROM `tabTask`
			WHERE status IN %(statuses)s
			AND status NOT IN ('Completed', 'Cancelled','Hold')
			AND service = 'IT-SW'
			GROUP BY project
		""", {"statuses": status_map[type]}, as_dict=True)

	return []


# @frappe.whitelist()
# def get_tasks_project_wise(type=None):

#     from frappe.utils import nowdate

#     today = nowdate()

#     status_map = {
#         "open": ["Open"],
#         "working": ["Working", "Overdue", "Code Review"],
#         "pr": ["Pending Review"],
#         "cr": ["Client Review"]
#     }

#     condition = """
#         status NOT IN ('Completed', 'Cancelled','Hold')
#         AND service = 'IT-SW'
#     """

#     values = {}

#     if type in status_map:
#         condition += " AND status IN %(statuses)s"
#         values["statuses"] = status_map[type]

#     # Overall
#     overall = frappe.db.sql(f"""
#         SELECT
#             COUNT(name) AS task_count,
#             COALESCE(SUM(rt),0) AS total_hours
#         FROM `tabTask`
#         WHERE {condition}
#     """, values, as_dict=True)[0]

#     # Today
#     today_data = frappe.db.sql(f"""
#         SELECT
#             COUNT(name) AS today_count,
#             COALESCE(SUM(rt),0) AS today_hours , custom_production_date
#         FROM `tabTask`
#         WHERE {condition}
#         AND DATE(custom_production_date) = %(today)s
#     """, {**values, "today": today}, as_dict=True)[0]
#     frappe.errprint(overall.task_count)
#     frappe.errprint(today_data.today_count)
#     frappe.errprint(today_data.custom_production_date)
#     return {
#         "task_count": overall.task_count,
#         "total_hours": overall.total_hours,
#         "today_count": today_data.today_count,
#         "today_hours": today_data.today_hours
#     }


@frappe.whitelist()
def get_today_task_data():
	today = nowdate()
	data = []

	active_sprints = frappe.get_all(
		'Sprint',
		filters={'status': 'In Progress'},
		fields=['sprint_id', 'team']
	)
	sprint_ids = [s.sprint_id for s in active_sprints]

	task_data = frappe.db.sql("""
		SELECT name, project, subject, custom_allocated_to, status,
			   expected_time, rt, actual_time, priority, custom_spot_task,
			   status as current_status, custom_remarks, custom_dev_team, custom_sprint,kt_confirmed
		FROM `tabTask`
		WHERE custom_production_date = %s
		  AND custom_sprint IN %s
		ORDER BY custom_sprint, custom_dev_team, custom_allocated_to, priority, project
	""", (today, tuple(sprint_ids)), as_dict=True)

	allocated_task_names = [t.name for t in task_data]
	employee_list = set()

	for task in task_data:
		emp = frappe.get_value("Employee", {"user_id": task.custom_allocated_to}, ["short_code", "name"], as_dict=True)
		short_code = emp.short_code if emp else ""
		emp_name = emp.name if emp else ""
		employee_list.add(emp_name)
		is_tl = frappe.db.get_value('Employee', emp_name, 'custom_is_tl') or 0

		spot_task = frappe.db.get_value('Sprint Task', {
			'production_date': today, 'task': task.name, 'cb': short_code
		}, 'spot_task') or 1

		actual_time = frappe.db.sql("""
			SELECT SUM(d.hours) as hours
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus = 1 AND t.employee = %s AND d.task = %s
		""", (emp_name, task.name), as_dict=True)[0].hours or 0

		today_at = frappe.db.sql("""
			SELECT SUM(d.hours) as hours
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
		""", (today, emp_name, task.name), as_dict=True)[0].hours or 0

		today_rt = frappe.db.sql("""
			SELECT SUM(a.today_rt) as hours
			FROM `tabAllocated Tasks` a
			JOIN `tabDaily Monitor` m ON a.parent = m.name
			WHERE m.docstatus != 2 AND m.date = %s AND m.dev_team = %s AND a.id = %s AND m.sprint = %s
		""", (today, task.custom_dev_team, task.name, task.custom_sprint), as_dict=True)[0].hours or 0

		data.append([
			task.name, task.project, task.subject, short_code, "Working",
			round(task.expected_time or 0, 2), round(task.rt or 0, 2),
			round(actual_time, 2), task.priority, spot_task,
			task.current_status, task.custom_remarks, task.custom_dev_team,
			round(today_at, 2), round(today_rt, 2), task.custom_sprint,is_tl,task.kt_confirmed
		])

	for emp_name in employee_list:
		if not emp_name:
			continue
		short_code =  frappe.db.get_value("Employee", emp_name,['short_code']) or ""
		dev_team = frappe.db.get_value("Employee", emp_name,['custom_dev_team']) or ""
		priority_order = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
		is_tl = frappe.db.get_value('Employee', {'name': emp_name}, ['custom_is_tl'])
		allocated_persons = []
		if is_tl == 1:
			user = frappe.db.get_value('Employee', {'name': emp_name}, ['user_id'])
			team = frappe.db.get_value('Dev Team', {'code_reviewer': user}, ['name'])
			if team:
				team_tl = frappe.db.get_value('Employee', {
					'status': 'Active',
					'custom_is_tl': 1,
					'custom_dev_team': team,
					'department':'IT. Development - THIS'
				}, ['user_id'])
				if team_tl:
					allocated_persons.append(team_tl)
					cdr_employees = frappe.db.get_all(
						'Employee', 
						{'custom_is_tl': 0, 'custom_tl': emp_name,'department':'IT. Development - THIS'}, 
						['user_id']
					)
					for cdr in cdr_employees:
						allocated_persons.append(cdr.user_id)
					cdr_tasks = frappe.db.get_all(
						'Task',
						filters={
							'custom_allocated_to': ('in', allocated_persons),
							'custom_pr_date': today
						},
						fields=['name', 'subject', 'project', 'status', 'priority','custom_sprint','kt_confirmed']
					)
					cdr_tasks.sort(key=lambda x: priority_order.get(x.get("priority") or "Low", 5))
					for tsk in cdr_tasks:
						today_at = frappe.db.sql("""
				SELECT SUM(d.hours) AS hours
				FROM `tabTimesheet Detail` d
				JOIN `tabTimesheet` t ON d.parent = t.name
				WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
			""", (today, emp_name, tsk['name']), as_dict=True)[0].hours or 0
						data.append([tsk['name'],tsk.get('project', ''),tsk.get('subject', ''), short_code,tsk.get('status', ''),0, 0, 0,
									tsk.get('priority', ''),1,tsk.get('status', ''),'',dev_team,round(today_at, 2), 0.5, tsk['custom_sprint'],is_tl,tsk['kt_confirmed']
						])
						
		
		not_in_tasks = tuple(allocated_task_names) or ("",)

		# Timesheet Tasks not in Task list
		timesheet_tasks = frappe.db.sql("""
			SELECT DISTINCT d.task, d.activity_type, d.project, d.subject, d.task_status
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task IS NOT NULL AND d.task NOT IN %s
		""", (today, emp_name, not_in_tasks), as_dict=True)

		for row in timesheet_tasks:
			priority = frappe.get_value("Task", row.task, "priority") or ""
			custom_sprint = frappe.get_value("Task", row.task, "custom_sprint") or ""
			expected_time = frappe.get_value("Task", row.task, "expected_time") or 0
			
			spot_task = frappe.db.get_value('Sprint Task', {
				'production_date': today, 'task': row.task, 'cb': short_code
			}, 'spot_task') or 1
			actual_time = frappe.db.sql("""
			SELECT SUM(d.hours) as hours
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus = 1 AND t.employee = %s AND d.task = %s
		""", (emp_name, row.task), as_dict=True)[0].hours or 0

			today_at = frappe.db.sql("""
				SELECT SUM(d.hours) AS hours
				FROM `tabTimesheet Detail` d
				JOIN `tabTimesheet` t ON d.parent = t.name
				WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.task = %s
			""", (today, emp_name, row.task), as_dict=True)[0].hours or 0

			status = "Working"
			if row.activity_type == "Manual Testing":
				status = "Pending Review"
			elif row.activity_type == "Code Review":
				status = "Code Review"
				expected_time =0
			kt_confirmed = frappe.db.get_value('Task',{'name':row.task},['kt_confirmed'])
				 
			today_rt = frappe.db.sql("""
			SELECT SUM(a.today_rt) as hours
			FROM `tabAllocated Tasks` a
			JOIN `tabDaily Monitor` m ON a.parent = m.name
			WHERE m.docstatus != 2 AND m.date = %s AND m.dev_team = %s AND a.id = %s AND m.sprint = %s
			""", (today, task.custom_dev_team, row.task, custom_sprint), as_dict=True)[0].hours or 0


			data.append([
				row.task, row.project, row.subject, short_code, status,
				round(expected_time,2), 0, round(actual_time,2), priority, spot_task,
				row.task_status, '', dev_team,
				round(today_at, 2), today_rt, custom_sprint,is_tl,kt_confirmed
			])

		# Timesheet Issues
		timesheet_issues = frappe.db.sql("""
			SELECT DISTINCT d.custom_issue, d.activity_type, d.project, d.custom_subject_issue
			FROM `tabTimesheet Detail` d
			JOIN `tabTimesheet` t ON d.parent = t.name
			WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.custom_issue IS NOT NULL
		""", (today, emp_name), as_dict=True)

		for row in timesheet_issues:
			priority = frappe.get_value("Issue", row.custom_issue, "priority") or ''
			current_status = frappe.get_value("Issue", row.custom_issue, "status") or ''
			custom_sprint = frappe.get_value("Issue", row.custom_issue, "custom_sprint") or ''

			today_at = frappe.db.sql("""
				SELECT SUM(d.hours) AS hours
				FROM `tabTimesheet Detail` d
				JOIN `tabTimesheet` t ON d.parent = t.name
				WHERE t.docstatus != 2 AND t.start_date = %s AND t.employee = %s AND d.custom_issue = %s
			""", (today, emp_name, row.custom_issue), as_dict=True)[0].hours or 0

			data.append([
				row.custom_issue, row.project, row.custom_subject_issue, short_code, "Working",
				0, 0, 0, priority, 1,
				current_status, '', dev_team,
				round(today_at, 2), 0,custom_sprint or '',is_tl,0
			])
		
	

	return data


	
# @frappe.whitelist()
# def get_today_task_data1(priority=None, sp=None, ro=None, from_date=None, to_date=None):

#     from frappe.utils import nowdate

#     # ------------------------------
#     # Default dates
#     # ------------------------------
#     if not from_date:
#         from_date = nowdate()
#     if not to_date:
#         to_date = nowdate()

#     data = []

#     # ------------------------------
#     # Active sprints
#     # ------------------------------
#     active_sprints = frappe.get_all(
#         "Sprint",
#         filters={"status": "In Progress"},
#         fields=["sprint_id", "team"]
#     )

#     sprint_ids = [s.sprint_id for s in active_sprints]

#     if not sprint_ids:
#         return {
#             "data": [],
#             "team_order": []
#         }

#     # ------------------------------
#     # Build conditions
#     # ------------------------------
#     conditions = ""
#     values = [from_date, to_date, tuple(sprint_ids)]

#     if priority:
#         conditions += " AND priority = %s"
#         values.append(priority)

#     if sp:
#         conditions += " AND custom_spot_task = %s"
#         values.append(1 if sp == "S" else 0)

#     if ro == "yes":
#         conditions += " AND revisions >= 1"
#     elif ro == "no":
#         conditions += " AND revisions < 1"

#     # ------------------------------
#     # Fetch tasks (DATE FILTER 🔥)
#     # ------------------------------
#     task_data = frappe.db.sql(f"""
#         SELECT
#             name, project, subject, custom_allocated_to, status,
#             expected_time, rt, actual_time, priority, custom_spot_task,
#             status as current_status, custom_remarks,
#             custom_dev_team, custom_sprint,
#             kt_confirmed, is_confirmed,
#             custom_spot_task, revisions , custom_production_date_count,
#             custom_production_date
#         FROM `tabTask`
#         WHERE custom_production_date BETWEEN %s AND %s
#           AND custom_sprint IN %s
#           {conditions}
#         ORDER BY custom_production_date, custom_sprint, custom_dev_team, custom_allocated_to
#     """, tuple(values), as_dict=True)

#     allocated_task_names = [t.name for t in task_data]

#     # ------------------------------
#     # Employee
#     # ------------------------------
#     employees = frappe.get_all(
#         "Employee",
#         fields=[
#             "name", "user_id", "short_code", "employee_name",
#             "custom_emp_image", "custom_is_tl", "custom_dev_team",
#             "custom_order_for_it_dashboard"
#         ],
#         filters={"custom_order_for_it_dashboard": [">", 0]},
#         order_by="custom_order_for_it_dashboard asc"
#     )

#     emp_map = {e.user_id: e for e in employees}
#     emp_name_map = {e.name: e for e in employees}

#     # ------------------------------
#     # Teams
#     # ------------------------------
#     teams = frappe.get_all(
#         "Dev Team",
#         filters={"order_for_it_dashboard": [">", 0]},
#         fields=["name", "logo", "order_for_it_dashboard"],
#         order_by="order_for_it_dashboard asc"
#     )

#     team_map = {t.name: t.logo for t in teams}
#     ordered_teams = [t.name for t in teams]

#     # ------------------------------
#     # Timesheet actual time
#     # ------------------------------
#     actual_times = frappe.db.sql("""
#         SELECT d.task, t.employee, SUM(d.hours) as hours
#         FROM `tabTimesheet Detail` d
#         JOIN `tabTimesheet` t ON d.parent = t.name
#         WHERE t.docstatus = 1
#         GROUP BY d.task, t.employee
#     """, as_dict=True)

#     actual_map = {(a.task, a.employee): a.hours for a in actual_times}

#     # ------------------------------
#     # Today AT (DATE RANGE )
#     # ------------------------------
#     today_at_data = frappe.db.sql("""
#         SELECT d.task, t.employee,
#             SUM(TIMESTAMPDIFF(SECOND, d.from_time, IFNULL(d.to_time, NOW())))/3600 as hours
#         FROM `tabTimesheet Detail` d
#         JOIN `tabTimesheet` t ON d.parent = t.name
#         WHERE t.docstatus != 2
#         AND d.from_time BETWEEN %s AND DATE_ADD(%s, INTERVAL 1 DAY)
#         GROUP BY d.task, t.employee
#     """, (from_date, to_date), as_dict=True)

#     today_at_map = {(a.task, a.employee): a.hours for a in today_at_data}

#     # ------------------------------
#     # Today RT (DATE RANGE )
#     # ------------------------------
#     today_rt_data = frappe.db.sql("""
#         SELECT a.id as task, m.dev_team, m.sprint, SUM(a.today_rt) as hours
#         FROM `tabAllocated Tasks` a
#         JOIN `tabDaily Monitor` m ON a.parent = m.name
#         WHERE m.docstatus != 2
#         AND m.date BETWEEN %s AND %s
#         GROUP BY a.id, m.dev_team, m.sprint
#     """, (from_date, to_date), as_dict=True)

#     today_rt_map = {(r.task, r.dev_team, r.sprint): r.hours for r in today_rt_data}

#     # ------------------------------
#     # Main Loop
#     # ------------------------------
#     for task in task_data:

#         emp = emp_map.get(task.custom_allocated_to)

#         emp_id = emp.name if emp else ""
#         short_code = emp.short_code if emp else ""
#         emp_name = emp.employee_name if emp else ""
#         order = emp.custom_order_for_it_dashboard if emp else 0

#         emp_display = f"{emp_name} ({short_code})" if emp_name else short_code

#         actual_time = actual_map.get((task.name, emp_id), 0)
#         today_at = today_at_map.get((task.name, emp_id), 0)
#         today_rt = today_rt_map.get((task.name, task.custom_dev_team, task.custom_sprint), 0)

#         data.append([
#             task.name, task.project, task.subject, short_code, "Working",
#             round(task.expected_time or 0, 2),
#             round(task.rt or 0, 2),
#             round(actual_time, 2),
#             task.priority,
#             task.custom_spot_task,
#             task.current_status,
#             task.custom_remarks,
#             task.custom_dev_team,
#             round(today_at, 2),
#             round(today_rt, 2),
#             task.custom_sprint,
#             emp.custom_is_tl if emp else 0,
#             task.kt_confirmed,
#             emp.custom_emp_image if emp else "",
#             team_map.get(task.custom_dev_team, ""),
#             task.is_confirmed,
#             task.custom_spot_task,
#             task.revisions,
#             task.custom_production_date_count,
#             emp_display,
#             order
#         ])

#     return {
#         "data": data,
#         "team_order": ordered_teams
#     }



@frappe.whitelist()
def get_today_task_data1(priority=None, sp=None, ro=None, from_date=None, to_date=None):

    import frappe
    from frappe.utils import nowdate

    # ------------------------------
    # Default Dates
    # ------------------------------
    if not from_date:
        from_date = nowdate()

    if not to_date:
        to_date = nowdate()

    data = []

    # ------------------------------
    # Active Sprints
    # ------------------------------
    active_sprints = frappe.get_all(
        "Sprint",
        filters={"status": "In Progress"},
        fields=["sprint_id"]
    )

    sprint_ids = [d.sprint_id for d in active_sprints]

    if not sprint_ids:
        return {
            "data": [],
            "team_order": []
        }

    # ------------------------------
    # Conditions
    # ------------------------------
    conditions = ""
    values = [from_date, to_date, tuple(sprint_ids)]

    if priority:
        conditions += " AND c.priority = %s"
        values.append(priority)

    if sp:
        conditions += " AND c.spot_task = %s"
        values.append(1 if sp == "S" else 0)

    if ro == "yes":
        conditions += " AND c.revisions >= 1"

    elif ro == "no":
        conditions += " AND c.revisions < 1"

    # ------------------------------
    # Employee
    # ------------------------------
    employees = frappe.get_all(
        "Employee",
        fields=[
            "name",
            "user_id",
            "short_code",
            "employee_name",
            "custom_emp_image",
            "custom_is_tl",
            "custom_order_for_it_dashboard"
        ],
        filters={
            "custom_order_for_it_dashboard": [">", 0]
        },
        order_by="custom_order_for_it_dashboard asc"
    )

    emp_map = {e.user_id: e for e in employees}

    # ------------------------------
    # Teams
    # ------------------------------
    teams = frappe.get_all(
        "Dev Team",
        filters={
            "order_for_it_dashboard": [">", 0]
        },
        fields=[
            "name",
            "logo",
            "order_for_it_dashboard"
        ],
        order_by="order_for_it_dashboard asc"
    )

    team_map = {t.name: t.logo for t in teams}
    ordered_teams = [t.name for t in teams]

    # ------------------------------
    # Task Data
    # Everything from Daily Monitor
    # ------------------------------
    task_data = frappe.db.sql(f"""
        SELECT

            m.dev_team,
            m.sprint,
            m.date,

            c.id as name,
            c.project_name as project,
            c.subject,

            c.cb ,
			c.allocated_to as custom_allocated_to,

            c.et as expected_time,
            c.today_rt,

            c.priority,
            c.spot_task,
            c.current_status,

            c.kt_confirmed,
            c.is_confirmed,

            c.revisions,
            c.production_date_count

        FROM `tabDaily Monitor` m

        JOIN `tabAllocated Tasks` c
            ON c.parent = m.name

        WHERE m.date BETWEEN %s AND %s

        AND m.sprint IN %s

        AND m.docstatus != 2

        {conditions}

        ORDER BY
            m.date,
            m.sprint,
            m.dev_team,
            c.cb

    """, tuple(values), as_dict=True)

    # ------------------------------
    # Timesheet Actual Time
    # KEEP SAME
    # ------------------------------
    actual_times = frappe.db.sql("""
        SELECT
            d.task,
            t.employee,
            SUM(d.hours) as hours

        FROM `tabTimesheet Detail` d

        JOIN `tabTimesheet` t
            ON d.parent = t.name

        WHERE t.docstatus = 1

        GROUP BY
            d.task,
            t.employee

    """, as_dict=True)

    actual_map = {
        (a.task, a.employee): a.hours
        for a in actual_times
    }

    # ------------------------------
    # Today AT
    # KEEP SAME
    # ------------------------------
    today_at_data = frappe.db.sql("""
        SELECT
            d.task,
            t.employee,

            SUM(
                TIMESTAMPDIFF(
                    SECOND,
                    d.from_time,
                    IFNULL(d.to_time, NOW())
                )
            ) / 3600 as hours

        FROM `tabTimesheet Detail` d

        JOIN `tabTimesheet` t
            ON d.parent = t.name

        WHERE t.docstatus != 2

        AND d.from_time BETWEEN %s
        AND DATE_ADD(%s, INTERVAL 1 DAY)

        GROUP BY
            d.task,
            t.employee

    """, (from_date, to_date), as_dict=True)

    today_at_map = {
        (a.task, a.employee): a.hours
        for a in today_at_data
    }

    # ------------------------------
    # Main Loop
    # ------------------------------
    for task in task_data:

        emp = emp_map.get(task.custom_allocated_to)

        emp_id = emp.name if emp else ""

        short_code = emp.short_code if emp else ""

        emp_name = emp.employee_name if emp else ""

        order = (
            emp.custom_order_for_it_dashboard
            if emp else 0
        )

        emp_display = (
            f"{emp_name} ({short_code})"
            if emp_name else short_code
        )

        # ------------------------------
        # Timesheet Values
        # KEEP SAME
        # ------------------------------
        actual_time = actual_map.get(
            (task.name, emp_id),
            0
        )

        today_at = today_at_map.get(
            (task.name, emp_id),
            0
        )

        # ------------------------------
        # Today RT from Daily Monitor
        # ------------------------------
        today_rt = task.today_rt or 0

        data.append([

            # 0
            task.name,

            # 1
            task.project,

            # 2
            task.subject,

            # 3
            short_code,

            # 4
            "Working",

            # 5 ET
            round(task.expected_time or 0, 2),

            # 6 RT
            0,

            # 7 AT
            round(actual_time or 0, 2),

            # 8 Priority
            task.priority,

            # 9 SP
            task.spot_task,

            # 10 Status
            task.current_status,

            # 11 Remarks
            "",

            # 12 Team
            task.dev_team,

            # 13 Today AT
            round(today_at or 0, 2),

            # 14 Today RT
            round(today_rt or 0, 2),

            # 15 Sprint
            task.sprint,

            # 16 TL
            emp.custom_is_tl if emp else 0,

            # 17 KT
            task.kt_confirmed,

            # 18 Emp Image
            emp.custom_emp_image if emp else "",

            # 19 Team Logo
            team_map.get(task.dev_team, ""),

            # 20 Confirm
            task.is_confirmed,

            # 21 SP
            task.spot_task,

            # 22 RO
            task.revisions,

            # 23 CF
            task.production_date_count,

            # 24 Employee Display
            emp_display,

            # 25 Order
            order

        ])

    return {
        "data": data,
        "team_order": ordered_teams
    }
	

@frappe.whitelist()
def get_today_task_data11(from_date=None, to_date=None):

    today = nowdate()
    if not from_date and not to_date:
        from_date = today
        to_date = today

    data = []

    # ------------------------------
    # Employees
    # ------------------------------
    employees = frappe.get_all(
        "Employee",
        fields=[
            "name", "short_code", "employee_name",
            "custom_emp_image", "custom_is_tl",
            "custom_dev_team", "custom_order_for_it_dashboard"
        ],
        filters={"custom_order_for_it_dashboard": [">", 0]},
        order_by="custom_order_for_it_dashboard asc"
    )

    emp_map = {e.short_code: e for e in employees}

    # ------------------------------
    # Teams
    # ------------------------------
    teams = frappe.get_all(
        "Dev Team",
        filters={"order_for_it_dashboard": [">", 0]},
        fields=["name", "logo", "order_for_it_dashboard"],
        order_by="order_for_it_dashboard asc"
    )

    team_map = {t.name: t.logo for t in teams}
    ordered_teams = [t.name for t in teams]

    # ------------------------------
    # Daily Monitor Data
    # ------------------------------
    dm_rows = frappe.db.sql("""
        SELECT 
            m.dev_team,
            m.sprint,
            c.short_code,
            c.available_hours,
            c.allocated_hours
        FROM `tabDaily Monitor` m
        JOIN `tabSprint Avl Time` c ON c.parent = m.name
        WHERE m.date BETWEEN %s AND %s
        AND m.docstatus != 2
    """, (from_date, to_date), as_dict=True)

    # ------------------------------
    # Today AT (UT)
    # ------------------------------
    today_at_data = frappe.db.sql("""
        SELECT t.employee, SUM(t.total_hours) as hours
        FROM `tabTimesheet` t
        WHERE t.docstatus != 2
        AND DATE(t.creation) BETWEEN %s AND %s
        GROUP BY t.employee
    """, (from_date, to_date), as_dict=True)

    today_at_map = {a.employee: a.hours for a in today_at_data}

    # ------------------------------
    # Build Data
    # ------------------------------
    for d in dm_rows:

        emp = emp_map.get(d.short_code)

        if not emp:
            continue

        emp_name = emp.name
        short_code = emp.short_code
        emp_display = f"{emp.employee_name} ({short_code})"
        order = emp.custom_order_for_it_dashboard

        team = d.dev_team
        team_logo = team_map.get(team, "")

        aph = d.available_hours or 0
        rt = d.allocated_hours or 0
        ut = today_at_map.get(emp_name, 0)

        data.append([
            "", "", "",                  # task இல்ல → empty
            short_code,
            "Working",
            0, 0, 0,                    # ET / RT / AT (task based இல்லை)
            "",                         # priority
            1,                          # spot default
            "", "",                     # status / remarks
            team,
            round(ut, 2),               # index 13 → UT
            round(rt, 2),               # index 14 → RT
            "",                         # sprint optional
            emp.custom_is_tl,
            "",                         # kt
            emp.custom_emp_image,
            team_logo,
            "", "",                     # confirm
            0, 0,
            round(aph, 2),              # index 24 → APH
            order,
            emp_display
        ])

    return {
        "data": data,
        "team_order": ordered_teams
    }


@frappe.whitelist()
def get_non_allocated_tasks():
    today = frappe.utils.today()
    tasks = frappe.get_all(
        "Task",
        filters={
            "service": "IT-SW",
            "status": ["in", ["Open", "Working"]],
        },
        fields=["name", "project", "custom_sprint", "subject", "expected_time", "actual_time", "priority", "status", "custom_allocated_to", "custom_production_date", "service",'custom_age', 'custom_production_date_count']
    )

    return {"data": tasks}

@frappe.whitelist()
def check_running_timesheet(task):

    today = frappe.utils.today()

    timesheets = frappe.get_all(
        "Timesheet",
        filters={
            "start_date": today,
            "docstatus": ["!=", 2]
        },
        fields=["name"]
    )

    for ts in timesheets:
        doc = frappe.get_doc("Timesheet", ts.name)

        if doc.time_logs:
            last_row = doc.time_logs[-1]   

            if not last_row.to_time:
                
                if last_row.task == task:
                    return True  

    return False  


@frappe.whitelist()
def get_opportunity_table():
    args = frappe.local.form_dict
    data = get_data_of_opp(args)

    # 🔹 Sort by Owner (2nd column)
    # data.sort(key=lambda x: x[1] or "")

    from itertools import groupby

    html = """
    <style>
        .opp-table {
            width: 100%;
            border-collapse: collapse;
        }
        .opp-table th {
			background: #0F1568;
			color: white;
			font-weight: bold;
			border: 1px solid #ddd;
			padding: 8px;
		}
        .opp-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .opp-table td:first-child {
            text-align: center;
        }
        .even-row {
            background-color: #eaf0f6;
        }
    </style>

    <table class="opp-table">
        <thead>
            <tr>
                <th>S NO</th>
                <th>Owner</th>
                <th>Service</th>
                <th>From</th>
                <th>Status</th>
                <th>Organization Name</th>
                <th>Territory</th>
                <th>Grade</th>
                <th>Date</th>
                <th>Age</th>
                <th>Amount</th>
                <th>PB%</th>
                <th>ECD</th>
                <th>Remark</th>
            </tr>
        </thead>
        <tbody>
    """

    row_index = 0

    for owner, group in groupby(data, key=lambda x: x[1]):
        group_list = list(group)
        rowspan = len(group_list)

        for i, row in enumerate(group_list):
            row_class = "even-row" if row_index % 2 == 1 else ""
            html += f"<tr class='{row_class}'>"

            for col_index, col in enumerate(row):
                if col_index == 1:  
                    if i == 0:
                        html += f"<td rowspan='{rowspan}'>{col}</td>"
                else:
                    align = "center" if col_index == 0 else "left"
                    html += f"<td style='text-align:{align}'>{col or ''}</td>"

            html += "</tr>"
            row_index += 1

    html += "</tbody></table>"

    return html


@frappe.whitelist()
def confirm_task(task):

    doc = frappe.get_doc("Task", task)

    doc.db_set("is_confirmed", 1)

    actual_time = doc.actual_time or 0
    today_rt = doc.today_rt or 0

    return {
        "actual_time": actual_time,
        "today_rt": today_rt
    }

@frappe.whitelist()
def get_retro_summary_html_test(name= None):

	all_tables = []
	dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='team_name')
	sprint_name = frappe.db.get_value(
	'Sprint',
	{'team': 'ALPHA', 'status': 'In Progress'},
	'sprint_id',
	order_by='creation desc'
)

	if sprint_name and sprint_name.startswith("SPRINT"):
		current_number = int(sprint_name.replace("SPRINT", "").strip())
		previous_sprint_id = f"SPRINT {current_number - 1}"
	else:
		previous_sprint_id = None  

	if name:
		frappe.errprint(f"name {name}")
		previous_sprint_id = name
	for team_name in dev_teams:
		sprint_name = frappe.db.get_value(
			'Sprint',
			{'team': team_name, 'sprint_id': previous_sprint_id},
			'name',
			order_by='creation desc'
		)
		if not sprint_name:
			continue
		table_html = build_retro_table_for_sprint(sprint_name)

		all_tables.append({
			'team': team_name,
			'html': table_html
		})

	return all_tables




@frappe.whitelist()
def build_retro_table_for_sprint(name):
	sprint = frappe.get_doc('Sprint', name)
	end_date = sprint.to_date
	original_cb_list = [s.short_code for s in sprint.sprint_avl_time]
	if not original_cb_list:
		return []
	tl_list = []
	non_tl_list = []
	for cb in original_cb_list:
		if frappe.db.exists("Employee", {"short_code": cb, "custom_is_tl": 1}):
			tl_list.append(cb)
		else:
			non_tl_list.append(cb)
	cb_list = tl_list + non_tl_list
	table = f"""
	<div style="overflow-x: auto; margin-top: 20px;">
	<table border="1" cellpadding="5" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: center; min-width: 1200px;">
	<colgroup>
		<col span="33" style="width: 5.88%;">
	</colgroup>
	<tr>
		<td rowspan="2" style="color:red;">{sprint.sprint_id}</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Hrs)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Hrs)</td>
		<td colspan="6" style="background:#f0b616;">Total (Hrs)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Count)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Count)</td>
		<td colspan="6" style="background:#f0b616;">Total (Count)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
	</tr>
	<tr>
		<!-- Hrs Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Hrs -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
		<!-- Count Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Count -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
	</tr>

	"""

	sub_total_rt = sub_tot_comp_rt = sub_tot_work_rt = sub_nt_rt = 0
	sub_total_s_rt = sub_tot_comp_srt = sub_tot_work_srt = sub_nt_srt = sub_bt_hours = 0
	sub_used_percent = sub_comp_per = sub_ncomp_per = tot_bt_hrs = tot_reopen_count = 0
	tot_c = tot_nc = tot_spr_chrs = tot_spr_whrs = tot_spot_chrs = tot_spot_whrs = tot_nc_rt = 0
	sub_total_count = sub_tot_comp_count =sub_tot_work_count =sub_nt_count =sub_total_s_count =0
	sub_tot_comp_scount = sub_tot_work_scount=sub_nt_scount=sub_total=overall_comp=0
	overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=0
	sr_no = 1
	for cb in cb_list:
		emp = frappe.db.get_value('Employee', {'short_code': cb}, ['name'])
		user_id = frappe.db.get_value('Employee', {'short_code': cb}, ['user_id'])
		result = frappe.db.sql("""
			SELECT
				SUM(CASE WHEN spot_task = 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND at_period = 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND at_period = 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN revisions > 0 THEN rt ELSE 0 END)
			FROM `tabSprint Task`
			WHERE parent = %s AND cb = %s
		""", (sprint.name, cb))[0]

		(
			total_rt, tot_comp_rt, spr_comp_hrs, tot_work_rt, spr_wor_hrs, nt_rt,
			total_s_rt, tot_comp_srt, spot_comp_hrs, tot_work_srt, spot_wor_hrs, nt_srt,reopen_count
		) = [x or 0 for x in result]

		completed_hrs = spr_comp_hrs + spot_comp_hrs
		ncompleted_hrs = spr_wor_hrs + spot_wor_hrs
		nc_rt = 0

		for st in sprint.sprint_task:
			if st.cb != cb:
				continue
			if frappe.db.exists('Energy Point And Non Conformity',
				{'task': st.task, 'docstatus': ['!=', 2], 'emp': emp}):
				nc_rt += st.rt or 0

		bt_hours = frappe.db.sql("""
			SELECT IFNULL(SUM(bt_difference), 0)
			FROM `tabAttendance`
			WHERE employee = %s AND docstatus != 2
			AND attendance_date BETWEEN %s AND %s
		""", (emp, sprint.from_date, end_date))[0][0]
		bt_hours = round(bt_hours or 0, 2)

		ts_hours = frappe.db.sql("""
			SELECT IFNULL(SUM(total_hours), 0)
			FROM `tabTimesheet`
			WHERE employee = %s AND docstatus != 2
			AND start_date BETWEEN %s AND %s
		""", (emp, sprint.from_date, end_date))[0][0]
		ts_hours = round(ts_hours or 0, 2)

		used_percent = (ts_hours / bt_hours) * 100 if ts_hours and bt_hours else 0
		comp_percent = (completed_hrs / ts_hours) * 100 if ts_hours and completed_hrs else 0
		ncomp_percent = (ncompleted_hrs / ts_hours) * 100 if ts_hours and ncompleted_hrs else 0
		tot_c += round(completed_hrs, 2)
		tot_nc += round(ncompleted_hrs, 2)
		tot_reopen_count += round(reopen_count, 2)
		tot_bt_hrs += ts_hours
		tot_spr_chrs += spr_comp_hrs
		tot_spr_whrs += spr_wor_hrs
		tot_spot_chrs += spot_comp_hrs
		tot_spot_whrs += spot_wor_hrs

		sub_total_rt += total_rt
		sub_tot_comp_rt += tot_comp_rt
		sub_tot_work_rt += tot_work_rt
		sub_nt_rt += nt_rt
		sub_total_s_rt += total_s_rt
		sub_tot_comp_srt += tot_comp_srt
		sub_tot_work_srt += tot_work_srt
		sub_nt_srt += nt_srt
		sub_bt_hours += bt_hours
		# sub_used_percent += used_percent
		sub_comp_per += comp_percent
		sub_ncomp_per += ncomp_percent
		tot_nc_rt += nc_rt

		spr_comp_s = f"{round(tot_comp_rt, 2)}/<br>{round(spr_comp_hrs, 2)}"
		spr_ncomp_s = f"{round(tot_work_rt, 2)}/<br>{round(spr_wor_hrs, 2)}"
		spot_comp_s = f"{round(tot_comp_srt, 2)}/<br>{round(spot_comp_hrs, 2)}"
		spot_ncomp_s = f"{round(tot_work_srt, 2)}/<br>{round(spot_wor_hrs, 2)}"

		used_percent_str = f"{ts_hours} ({round(used_percent, 2)}%)"
		comp_percent_str = f"{round(completed_hrs, 2)} ({round(comp_percent, 2)}%)"
		ncomp_percent_str = f"{round(ncompleted_hrs, 2)} ({round(ncomp_percent, 2)}%)"
		# if comp_percent < 70:
		font_color= "#f02e0c" if comp_percent < 70 else "#110404"
		att_color="#2059d4" if used_percent < 80 else "#110404"
		row_color = '#e8edea' if sr_no % 2 == 0 else '#ffffff'
		counts = frappe.db.sql("""
			SELECT
				SUM(CASE WHEN st.spot_task = 0 THEN 1 ELSE 0 END) AS total_count,
				SUM(CASE WHEN st.spot_task = 0 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_count,
				SUM(CASE WHEN st.spot_task = 0 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_count,
				SUM(CASE WHEN st.spot_task = 0 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_count,
				SUM(CASE WHEN st.spot_task = 1 THEN 1 ELSE 0 END) AS total_s_count,
				SUM(CASE WHEN st.spot_task = 1 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_scount,
				SUM(CASE WHEN st.spot_task = 1 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_scount,
				SUM(CASE WHEN st.spot_task = 1 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_scount,
				SUM(CASE WHEN st.revisions > 0 THEN revisions ELSE 0 END) AS reopen_count
			FROM `tabSprint Task` st
			WHERE st.parent = %s AND st.cb = %s
		""", (sprint.name, cb), as_dict=1)[0]

		total_count = counts.total_count or 0
		tot_comp_count = counts.tot_comp_count or 0
		tot_work_count = counts.tot_work_count or 0
		nt_count = counts.nt_count or 0
		total_s_count = counts.total_s_count or 0
		tot_comp_scount = counts.tot_comp_scount or 0
		tot_work_scount = counts.tot_work_scount or 0
		nt_scount = counts.nt_scount or 0
		reopen_count=counts.reopen_count or 0


		nc_count = frappe.db.sql("""
			SELECT SUM(e.nc_score)
			FROM `tabSprint Task` st
			JOIN `tabEnergy Point And Non Conformity` e
			ON e.task = st.task
			WHERE st.parent = %s
			AND st.cb = %s
			AND e.emp = %s
			AND e.docstatus != 2
		""", (sprint.name, cb, emp))[0][0] or 0


		sr_no += 1
		if sub_bt_hours > 0:
			sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
		else:
			sub_used_str=0
		if  tot_bt_hrs > 0:
			sub_comp_str=(tot_c/tot_bt_hrs)*100
		else:
			sub_comp_str=0
		if  tot_bt_hrs > 0:
			sub_work_str=(tot_nc/tot_bt_hrs)*100
		else:
			sub_work_str=0
		font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
		att_color="#2059d4" if sub_used_str < 80 else "#110404"
		sub_used_str = f"{round(tot_bt_hrs, 2)} ({round(sub_used_str, 2)})"
		sub_comp_str = f"{round(tot_c, 2)} ({round(sub_comp_str, 2)})"
		sub_work_str = f"{round(tot_nc, 2)} ({round(sub_work_str, 2)})"

		sub_total_count += total_count
		sub_tot_comp_count += tot_comp_count
		sub_tot_work_count += tot_work_count
		sub_nt_count += nt_count
		sub_total_s_count += total_s_count
		sub_tot_comp_scount += tot_comp_scount
		sub_tot_work_scount += tot_work_scount
		sub_nt_scount += nt_scount
		sub_total += total_count + total_s_count
		overall_comp += tot_comp_count + tot_comp_scount
		overall_work += tot_work_count + tot_work_scount
		overall_nt += nt_count + nt_scount
		sub_total_reopen_count += reopen_count
		tot_nc_count += nc_count

		table += f"""
		<tr style="background-color: {row_color};color:#110404;">
			<td>{cb}</td>
			<td>{total_rt}</td>
			<td>{spr_comp_s}</td>
			<td>{spr_ncomp_s}</td>
			<td>{nt_rt}</td>
			<td>{total_s_rt}</td>
			<td>{spot_comp_s}</td>
			<td>{spot_ncomp_s}</td>
			<td>{nt_srt}</td>
			<td>{total_rt + total_s_rt}</td>
			<td>{bt_hours}</td>
			<td  style="color: {att_color};">{used_percent_str}</td>
			<td style="color: {font_color};">{comp_percent_str}</td>
			<td>{ncomp_percent_str}</td>
			<td>{round(nt_rt + nt_srt, 2)}</td>
			<td>{nc_rt}</td>
			<td>{round(reopen_count, 2)}</td>
			<td>{total_count}</td>
			<td>{tot_comp_count}</td>
			<td>{tot_work_count}</td>
			<td>{nt_count}</td>
			<td>{total_s_count}</td>
			<td>{tot_comp_scount}</td>
			<td>{tot_work_scount}</td>
			<td>{nt_scount}</td>
			<td>{total_count + total_s_count}</td>
			<td>-</td>
			<td>-</td>
			<td>{tot_comp_count + tot_comp_scount}</td>
			<td>{tot_work_count + tot_work_scount}</td>
			<td>{nt_count + nt_scount}</td>
			<td>{nc_count}</td>
			<td>{reopen_count}</td>
		</tr>
		"""

		sr_no += 1
	if sub_bt_hours > 0:
		sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
	else:
		sub_used_str=0
	if  tot_bt_hrs > 0:
		sub_comp_str=(tot_c/tot_bt_hrs)*100
	else:
		sub_comp_str=0
	if  tot_bt_hrs > 0:
		sub_work_str=(tot_nc/tot_bt_hrs)*100
	else:
		sub_work_str=0
	font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
	att_color="#2059d4" if sub_used_str < 80 else "#110404"
	sub_used_str = f"{round(tot_bt_hrs, 2)}"
	sub_comp_str = f"{round(tot_c, 2)}"
	sub_work_str = f"{round(tot_nc, 2)}"
	
	table += f"""
	<tr>
		<td style="background:#020c59;color:white;">Total(Hrs)</td>
		<td style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
		<td style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/<br>{round(tot_spr_chrs, 2)}</td>
		<td style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/<br>{round(tot_spr_whrs, 2)}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_nt_rt}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_total_s_rt}</td>
		<td style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/<br>{round(tot_spot_chrs, 2)}</td>
		<td style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/<br>{round(tot_spot_whrs, 2)}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_nt_srt}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_rt + sub_total_s_rt}</td>
		<td style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
		<td style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
		<td style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
		<td style="background:#f0b616;color:#110404;">{sub_work_str}</td>
		<td style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
		<td style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
		<td style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
		<td style="background:#f0b616;color:#110404;">-</td>
		<td style="background:#f0b616;color:#110404;">-</td>
		<td style="background:#f0b616;color:#110404;">{overall_comp}</td>
		<td style="background:#f0b616;color:#110404;">{overall_work}</td>
		<td style="background:#f0b616;color:#110404;">{overall_nt}</td>
		<td style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
		
	</tr>

	"""

	table += """
		</table></div>
	"""
	# print(table)
	return table

@frappe.whitelist()
def it_receivable_table():
	from frappe.utils import today, getdate, nowdate, fmt_money
	from datetime import datetime
	fiscal_year = frappe.db.get_value(
		"Fiscal Year",
		filters={"year_start_date": ["<=", today()], "year_end_date": [">=", today()]},
		fieldname=["year_start_date", "year_end_date"],
		as_dict=True
	)

	from_date = fiscal_year["year_start_date"]
	to_date = fiscal_year["year_end_date"]

	filters = {
		'from_date': from_date,
		'to_date': to_date
	}

	data = frappe.db.sql("""
		SELECT name, customer, outstanding_amount, posting_date
		FROM `tabSales Invoice`
		WHERE docstatus = 1
		  AND services="IT-SW"
		  AND posting_date BETWEEN %(from_date)s AND %(to_date)s
		  AND outstanding_amount > 0
		ORDER BY posting_date
	""", filters, as_dict=True)

	total_outstanding = 0
	today_date = getdate(nowdate())

	html = """
	 <style>
		.odd-row { background-color: #f9f9f9; }
		.even-row { background-color: #eaf0f6; }
	</style>
	<div style='max-height: 340px; overflow-y: auto; overflow-x: auto;'>
		<div style='min-width: 500px;'>
			<table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
				<thead>
					<tr>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">S.No</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Customer</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Value</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Age</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Sales Invoice</th>
					</tr>
				</thead>
				<tbody>
	"""

	for idx, row in enumerate(data, 1):
		age = (today_date - getdate(row.posting_date)).days
		row_style = "color: red;" if age > 30 else ""
		row_class = "even-row" if idx % 2 == 0 else "odd-row"
		name_style = "color: red;" if age > 30 else ""
		total_outstanding += row.outstanding_amount or 0

		html += f"""
			<tr class="{row_class}" style="{row_style}">
				<td style="text-align: center;">{idx}</td>
				<td style="white-space: nowrap; text-align: center;">{row.customer}</td>
				<td style='text-align:right;'>{fmt_money(row.outstanding_amount)}</td>
				<td style='text-align:center;'>{age}</td>
				<td style="white-space: nowrap; text-align: left;"><a href="/app/sales-invoice/{ row.name }" target="_blank" style="{name_style}">{ row.name }</a></td>
			</tr>
		"""

	# Grand Total row
	html += f"""
		<tr style="background: #f0f0f0; font-weight: bold;">
			<td colspan="2" style="text-align: center;">Total</td>
			<td style="text-align: right;">{fmt_money(total_outstanding)}</td>
			<td></td>
			<td></td>
		</tr>
	"""

	html += """
				</tbody>
			</table>
		</div>
	</div>
	"""
	return html

@frappe.whitelist()
def it_payable_table():
	from frappe.utils import today, getdate, nowdate
	from datetime import datetime
	from frappe.utils import today, getdate, nowdate, fmt_money
	fiscal_year = frappe.db.get_value(
		"Fiscal Year",
		filters={"year_start_date": ["<=", today()], "year_end_date": [">=", today()]},
		fieldname=["year_start_date", "year_end_date"],
		as_dict=True
	)
	from_date = fiscal_year["year_start_date"]
	to_date = fiscal_year["year_end_date"]

	filters = {
		'from_date': from_date,
		'to_date': to_date
	}

	data = frappe.db.sql("""
		SELECT name, supplier, outstanding_amount, posting_date
		FROM `tabPurchase Invoice`
		WHERE docstatus = 1
		  AND services="IT-SW"
		  AND posting_date BETWEEN %(from_date)s AND %(to_date)s
		  AND outstanding_amount > 0
		ORDER BY posting_date
	""", filters, as_dict=True)

	html = """
	<style>
		.odd-row { background-color: #f9f9f9; }
		.even-row { background-color: #eaf0f6; }
	</style>
	<div style='max-height: 340px; overflow-y: auto; overflow-x: auto;'>
		<div style='min-width: 500px;'>
			<table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
				<thead>
					<tr>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">S.No</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center; white-space: nowrap;">Supplier</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Value</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Age</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center; white-space: nowrap;">Purchase Invoice</th>
					</tr>
				</thead>
				<tbody>
	"""
	today_date = getdate(nowdate())
	total_outstanding = 0
	for idx, row in enumerate(data, 1):
		age = (today_date - getdate(row.posting_date)).days
		row_style = "color: red;" if age > 30 else ""  # Apply to whole row
		row_class = "even-row" if idx % 2 == 0 else "odd-row"
		name_style = "color: red;" if age > 30 else ""
		total_outstanding += row.outstanding_amount or 0
		html += f"""
			<tr class="{row_class}" style="{row_style}">
			<td style="text-align: center;">{idx}</td>
				<td style="white-space: nowrap; text-align: left;">{row.supplier}</td>
				<td style='text-align:right;'>{frappe.utils.fmt_money(row.outstanding_amount)}</td>
				<td style='text-align:center;'>{age}</td>
				<td style="white-space: nowrap; text-align: left;"><a href="/app/purchase-invoice/{ row.name }" target="_blank" style="{name_style}">{ row.name }</a></td>
			</tr>
		"""
	html += f"""
		<tr style="background: #f0f0f0; font-weight: bold;">
			<td colspan="2" style="text-align: center;">Total</td>
			<td style="text-align: right;">{fmt_money(total_outstanding)}</td>
			<td></td>
			<td></td>
		</tr>
	"""

	html += """
				</tbody>
			</table>
		</div>
	</div>
	"""
	return html


@frappe.whitelist()
def it_tobill_table():
	from frappe.utils import today, getdate, nowdate
	from datetime import datetime
	from frappe.utils import today, getdate, nowdate, fmt_money
	from datetime import datetime
	fiscal_year = frappe.db.get_value(
		"Fiscal Year",
		filters={"year_start_date": ["<=", today()], "year_end_date": [">=", today()]},
		fieldname=["year_start_date", "year_end_date"],
		as_dict=True
	)
	from_date = fiscal_year["year_start_date"]
	to_date = fiscal_year["year_end_date"]

	filters = {
		'from_date': from_date,
		'to_date': to_date
	}

	data = frappe.db.sql("""
		SELECT name, customer, base_grand_total, transaction_date
		FROM `tabSales Order`
		WHERE docstatus = 1
		  AND service='IT-SW'
		  AND status='To Bill'
		  AND base_grand_total > 0
		ORDER BY transaction_date
	""", as_dict=True)

	html = """
	<style>
		.odd-row { background-color: #f9f9f9; }
		.even-row { background-color: #eaf0f6; }
	</style>
	<div style='max-height: 340px; overflow-y: auto; overflow-x: auto;'>
		<div style='min-width: 500px;'>
			<table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
				<thead>
					<tr>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">S.No</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center; white-space: nowrap;">Customer</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Value</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Age</th>
						<th style="position: sticky; top: 0; background: #002060; color: white; text-align: center; white-space: nowrap;">Sales Order</th>
					</tr>
				</thead>
				<tbody>
	"""

	total_outstanding = 0
	today_date = getdate(nowdate())
	for idx, row in enumerate(data, 1):
		age = (today_date - getdate(row.transaction_date)).days
		row_style = "color: red;" if age > 30 else ""  # Apply to whole row
		row_class = "even-row" if idx % 2 == 0 else "odd-row"
		name_style = "color: red;" if age > 30 else ""
		total_outstanding += row.base_grand_total or 0
		html += f"""
			<tr class="{row_class}" style="{row_style}">
				<td style="text-align: center;">{idx}</td>
				<td style="white-space: nowrap; text-align:left;">{row.customer}</td>
				<td style='text-align:right;'>{frappe.utils.fmt_money(row.base_grand_total)}</td>
				<td style='text-align:center;'>{age}</td>
				<td style="white-space: nowrap; text-align:right;"><a href="/app/sales-order/{ row.name }" target="_blank" style="{name_style}">{ row.name }</a></td>
			</tr>
		"""
	html += f"""
		<tr style="background: #f0f0f0; font-weight: bold;">
			<td colspan="2" style="text-align: center;" >Total</td>
			<td style="text-align: right;">{fmt_money(total_outstanding)}</td>
			<td></td>
			<td></td>
		</tr>
	"""

	html += """
				</tbody>
			</table>
		</div>
	</div>
	"""
	return html

# @frappe.whitelist()
# def get_tasks_project_pivot():
# 	status_group_map = {
# 		"Open": "open",
# 		"Working": "working",
# 		"Overdue": "working",
# 		"Code Review": "cdr",
# 		"Pending Review": "pr",
# 		"Client Review": "cr"
# 	}

# 	tasks = frappe.db.sql("""
# 		SELECT 
# 			t.project,
# 			p.project_type,
# 			t.status,
# 			t.rt
# 		FROM `tabTask` t
# 		LEFT JOIN `tabProject` p ON t.project = p.name
# 		WHERE t.status NOT IN ('Completed', 'Cancelled', 'Hold')
# 		AND t.service = 'IT-SW'
# 	""", as_dict=True)

# 	pivot = {}

# 	for task in tasks:
# 		project = task.project or "No Project"
# 		project_type = (task.project_type or "Unknown").strip()
# 		status = task.status or "Unknown"
# 		group = status_group_map.get(status)
# 		rt = task.rt or 0.0

# 		if not group:
# 			continue

# 		if project not in pivot:
# 			pivot[project] = {
# 				"project": project,
# 				"project_type": project_type,
# 				"open": {"tasks": 0, "hours": 0.0},
# 				"working": {"tasks": 0, "hours": 0.0},
# 				"pr": {"tasks": 0, "hours": 0.0},
# 				"cr": {"tasks": 0, "hours": 0.0},
# 			}


# 		if group == "cdr":
# 			group = "working"

# 		pivot[project][group]["tasks"] += 1
# 		pivot[project][group]["hours"] += rt

# 	sort_order = {
# 		"External": 1,
# 		"AMC": 2,
# 		"Support": 3,
# 		"Products": 4,
# 		"Internal": 5,
# 		"Other": 6,
# 		"Unknown": 7
# 	}

# 	sorted_items = sorted(
# 		pivot.values(),
# 		key=lambda x: (sort_order.get(x["project_type"], 999), x["project"])
# 	)

# 	result = []
# 	for i, data in enumerate(sorted_items, start=1):
# 		def format_cell(value):
# 			return f"{value['hours']:.2f}/{value['tasks']}"

# 		row = {
# 			"s_no": i,
# 			"project": data["project"],
# 			"project_type": data["project_type"],
# 			"open": format_cell(data["open"]),
# 			"working": format_cell(data["working"]),
# 			"pr": format_cell(data["pr"]),
# 			"cr": format_cell(data["cr"])
# 		}
# 		result.append(row)

# 	return result

@frappe.whitelist()
def get_tasks_project_pivot():
	from frappe.utils import today

	status_group_map = {
		"Open": "open",
		"Working": "working",
		"Overdue": "working",
		"Code Review": "cdr",
		"Pending Review": "pr",
		"Client Review": "cr"
	}

	today_date = today()

	tasks = frappe.db.sql("""
		SELECT 
			t.project,
			p.project_type,
			t.status,
			t.rt,
			DATE(t.custom_production_date) as production_date
		FROM `tabTask` t
		LEFT JOIN `tabProject` p ON t.project = p.name
		WHERE t.status NOT IN ('Completed', 'Cancelled', 'Hold')
		AND t.service = 'IT-SW'
	""", as_dict=True)

	pivot = {}

	for task in tasks:

		project = task.project or "No Project"
		project_type = (task.project_type or "Unknown").strip()
		status = task.status or "Unknown"
		group = status_group_map.get(status)
		rt = task.rt or 0.0
		is_today = (str(task.production_date) == today_date)

		if not group:
			continue

		if project not in pivot:
			pivot[project] = {
				"project": project,
				"project_type": project_type,

				"open": {"tasks": 0, "hours": 0.0},
				"open_td": {"tasks": 0, "hours": 0.0},

				"working": {"tasks": 0, "hours": 0.0},
				"working_td": {"tasks": 0, "hours": 0.0},

				"pr": {"tasks": 0, "hours": 0.0},
				"pr_td": {"tasks": 0, "hours": 0.0},

				"cr": {"tasks": 0, "hours": 0.0},
				"cr_td": {"tasks": 0, "hours": 0.0},
			}

		# convert cdr → working
		if group == "cdr":
			group = "working"

		# =========================
		# TOTAL
		# =========================
		pivot[project][group]["tasks"] += 1
		pivot[project][group]["hours"] += rt

		# =========================
		# TODAY
		# =========================
		if is_today:
			pivot[project][f"{group}_td"]["tasks"] += 1
			pivot[project][f"{group}_td"]["hours"] += rt

	# sorting
	sort_order = {
		"External": 1,
		"AMC": 2,
		"Support": 3,
		"Products": 4,
		"Internal": 5,
		"Other": 6,
		"Unknown": 7
	}

	sorted_items = sorted(
		pivot.values(),
		key=lambda x: (sort_order.get(x["project_type"], 999), x["project"])
	)

	def fmt(v):
		return f"{v['hours']:.2f}/{v['tasks']}"

	result = []

	for i, data in enumerate(sorted_items, start=1):

		result.append({
			"s_no": i,
			"project": data["project"],
			"project_type": data["project_type"],

			"open": fmt(data["open"]),
			"open_td": fmt(data["open_td"]),

			"working": fmt(data["working"]),
			"working_td": fmt(data["working_td"]),

			"pr": fmt(data["pr"]),
			"pr_td": fmt(data["pr_td"]),

			"cr": fmt(data["cr"]),
			"cr_td": fmt(data["cr_td"])
		})

	return result



@frappe.whitelist()
def get_retro_summary_html(name= None,dev_team= None):

	all_tables = []
	if dev_team:
		dev_teams = [dev_team]
	else:
		dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='team_name')

	sprint_name = frappe.db.get_value(
	'Sprint',
	{'team': 'ALPHA', 'status': 'In Progress'},
	'sprint_id',
	order_by='creation desc'
)

	if sprint_name and sprint_name.startswith("SPRINT"):
		current_number = int(sprint_name.replace("SPRINT", "").strip())
		previous_sprint_id = f"SPRINT {current_number - 1}"
	else:
		previous_sprint_id = None  

	if name:
		frappe.errprint(f"name {name}")
		previous_sprint_id = name
	for team_name in dev_teams:
		sprint_name = frappe.db.get_value(
			'Sprint',
			{'team': team_name, 'sprint_id': previous_sprint_id},
			'name',
			order_by='creation desc'
		)
		if not sprint_name:
			continue

		
		table_html = build_retro_table_for_sprint(sprint_name)

		all_tables.append({
			'team': team_name,
			'html': table_html
		})

	return all_tables


# @frappe.whitelist()
# def get_team_retro_tables(sprint_name=None, name=None, team_filter=None):
#     dev_teams = ["ALPHA", "BETA", "CHARLIE", "DELTA"]
#     all_tables = []

	
#     if sprint_name and sprint_name.startswith("SPRINT"):
#         current_number = int(sprint_name.replace("SPRINT", "").strip())
#         previous_sprint_id = f"SPRINT {current_number - 1}"
#     else:
#         previous_sprint_id = None

	
#     if name:
#         frappe.errprint(f"name {name}")
#         previous_sprint_id = name

#     for team_name in dev_teams:

#         if team_filter and team_filter != team_name:
#             continue

#         sprint_name = frappe.db.get_value(
#             'Sprint',
#             {
#                 'team': team_name,
#                 'sprint_id': previous_sprint_id
#             },
#             'name',
#             order_by='creation desc'
#         )

#         if not sprint_name:
#             continue

#         table_html = build_retro_table_for_sprint_new(sprint_name)

#         all_tables.append({
#             'team': team_name,
#             'html': table_html
#         })

#     return all_tables


@frappe.whitelist()
def update_sprint_filter():
	sprint_name = frappe.db.get_value(
		'Sprint',
		{'team': 'ALPHA', 'status': 'In Progress'},
		'sprint_id',
		order_by='creation desc'
	)

	previous_sprint_id = None
	today = datetime.today()

	if today.strftime('%A') == 'Monday':
		previous_sprint_id =sprint_name
	else:
		if sprint_name and sprint_name.startswith("SPRINT"):
			current_number = int(sprint_name.replace("SPRINT", "").strip())
			previous_sprint_id = f"SPRINT {current_number - 1}"

	return previous_sprint_id


@frappe.whitelist()
def get_retro_summary_overall(name=None):
	dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='team_name')

	# Determine the previous sprint ID to fetch
	if name:
		previous_sprint_id = name
	else:
		sprint_name = frappe.db.get_value(
			'Sprint',
			{'team': 'ALPHA', 'status': 'In Progress'},
			'sprint_id',
			order_by='creation desc'
		)
		if sprint_name and sprint_name.startswith("SPRINT"):
			current_number = int(sprint_name.replace("SPRINT", "").strip())
			previous_sprint_id = f"SPRINT {current_number - 1}"
		else:
			previous_sprint_id = None

	summary_rows = []
	total_data = []
	for team_name in dev_teams:
		sprint_docname = frappe.db.get_value(
			'Sprint',
			{'team': team_name, 'sprint_id': previous_sprint_id},
			'name',
			order_by='creation desc'
		)
		if not sprint_docname:
			continue

		table_html = build_retro_table_for_sprint_summary(sprint_docname)
		
		
		if not table_html:
			continue

		# Extract only the summary row (last <tr>) from the HTML
		summary_row = table_html.split("</tr>")[-2] + "</tr>"
		summary_rows.append((team_name, summary_row))

	   

		# # Extract the last <tr> inside the table
		# rows = table_html.split("<tr>")
		# if len(rows) < 2:
		#     continue

		# last_row = "<tr>" + rows[-1].split("</tr>")[0] + "</tr>"  # Get last row safely
		# cells = [c.split("</td>")[0] for c in last_row.split("<td>")[1:]]  # Skip the first split part (before first <td>)
		# numeric_values = []
		# for val in cells:
		#     try:
		#         numeric_values.append(int(val.strip()))
		#     except:
		#         numeric_values.append(0)

		# # Add to total
		# if not total_data:
		#     total_data = numeric_values
		# else:
		#     total_data = [x + y for x, y in zip(total_data, numeric_values)]

		# summary_rows.append((team_name, numeric_values))

	# Build the overall summary table HTML
	table = f"""
	<div style="overflow-x: auto; margin-top: 20px; margin-left: 30px; margin-right: 30px; padding-right: 30px;">
	<table border="1" cellpadding="5" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: center; min-width: 1200px;">
		<colgroup>
		<col span="33" style="width: 5.88%;">
	</colgroup>
	<tr>
		<td rowspan="2" style="color:red;">{previous_sprint_id}</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Hrs)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Hrs)</td>
		<td colspan="6" style="background:#f0b616;">Total (Hrs)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Count)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Count)</td>
		<td colspan="6" style="background:#f0b616;">Total (Count)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
	</tr>
	<tr>
		<!-- Hrs Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Hrs -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
		<!-- Count Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Count -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
	</tr>
	"""
	for team, row_html in summary_rows:
		table += f"<tr><td style='background:#f0f0f0;font-weight:bold;'>{team}</td>{''.join(row_html.split('<td>')[1:])}"

	# for team, row_html in summary_rows:
	#     table += f"<tr><td style='background:#f0f0f0;font-weight:bold;'>{team}</td>{''.join(row_html.split('<td>')[1:])}"
	# if total_data:
	#     table += f"<tr style='background:#dff0d8;font-weight:bold;'><td>Total</td>" + \
	#             "".join(f"<td>{v}</td>" for v in total_data) + "</tr>"
	table += "</table></div>"
	return table


@frappe.whitelist()
def build_retro_table_for_sprint_summary(name):
	sprint = frappe.get_doc('Sprint', name)
	end_date = sprint.to_date
	original_cb_list = [s.short_code for s in sprint.sprint_avl_time]
	if not original_cb_list:
		return []
	tl_list = []
	non_tl_list = []
	for cb in original_cb_list:
		if frappe.db.exists("Employee", {"short_code": cb, "custom_is_tl": 1}):
			tl_list.append(cb)
		else:
			non_tl_list.append(cb)
	cb_list = tl_list + non_tl_list
	table = f"""
	<div style="overflow-x: auto; margin-top: 20px; margin-left: 30px; margin-right: 30px">
	<table border="1" cellpadding="5" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: center; min-width: 1200px;">
	<colgroup>
		<col span="33" style="width: 5.88%;">
	</colgroup>
	<tr>
		<td rowspan="2" style="color:red;">{sprint.sprint_id}</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Hrs)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Hrs)</td>
		<td colspan="6" style="background:#f0b616;">Total (Hrs)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Count)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Count)</td>
		<td colspan="6" style="background:#f0b616;">Total (Count)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
	</tr>
	<tr>
		<!-- Hrs Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Hrs -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
		<!-- Count Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Count -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
	</tr>

	"""

	sub_total_rt = sub_tot_comp_rt = sub_tot_work_rt = sub_nt_rt = 0
	sub_total_s_rt = sub_tot_comp_srt = sub_tot_work_srt = sub_nt_srt = sub_bt_hours = 0
	sub_used_percent = sub_comp_per = sub_ncomp_per = tot_bt_hrs = tot_reopen_count = 0
	tot_c = tot_nc = tot_spr_chrs = tot_spr_whrs = tot_spot_chrs = tot_spot_whrs = tot_nc_rt = 0
	sub_total_count = sub_tot_comp_count =sub_tot_work_count =sub_nt_count =sub_total_s_count =0
	sub_tot_comp_scount = sub_tot_work_scount=sub_nt_scount=sub_total=overall_comp=0
	overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=0
	sr_no = 1
	for cb in cb_list:
		emp = frappe.db.get_value('Employee', {'short_code': cb}, ['name'])
		user_id = frappe.db.get_value('Employee', {'short_code': cb}, ['user_id'])
		result = frappe.db.sql("""
			SELECT
				SUM(CASE WHEN spot_task = 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 0 AND at_period = 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
				SUM(CASE WHEN spot_task = 1 AND at_period = 0 THEN rt ELSE 0 END),
				SUM(CASE WHEN revisions > 0 THEN rt ELSE 0 END)
			FROM `tabSprint Task`
			WHERE parent = %s AND cb = %s
		""", (sprint.name, cb))[0]

		(
			total_rt, tot_comp_rt, spr_comp_hrs, tot_work_rt, spr_wor_hrs, nt_rt,
			total_s_rt, tot_comp_srt, spot_comp_hrs, tot_work_srt, spot_wor_hrs, nt_srt,reopen_count
		) = [x or 0 for x in result]

		completed_hrs = spr_comp_hrs + spot_comp_hrs
		ncompleted_hrs = spr_wor_hrs + spot_wor_hrs
		nc_rt = 0

		for st in sprint.sprint_task:
			if st.cb != cb:
				continue
			if frappe.db.exists('Energy Point And Non Conformity',
				{'task': st.task, 'docstatus': ['!=', 2], 'emp': emp}):
				nc_rt += st.rt or 0

		bt_hours = frappe.db.sql("""
			SELECT IFNULL(SUM(bt_difference), 0)
			FROM `tabAttendance`
			WHERE employee = %s AND docstatus != 2
			AND attendance_date BETWEEN %s AND %s
		""", (emp, sprint.from_date, end_date))[0][0]
		bt_hours = round(bt_hours or 0, 2)

		ts_hours = frappe.db.sql("""
			SELECT IFNULL(SUM(total_hours), 0)
			FROM `tabTimesheet`
			WHERE employee = %s AND docstatus != 2
			AND start_date BETWEEN %s AND %s
		""", (emp, sprint.from_date, end_date))[0][0]
		ts_hours = round(ts_hours or 0, 2)

		used_percent = (ts_hours / bt_hours) * 100 if ts_hours and bt_hours else 0
		comp_percent = (completed_hrs / ts_hours) * 100 if ts_hours and completed_hrs else 0
		ncomp_percent = (ncompleted_hrs / ts_hours) * 100 if ts_hours and ncompleted_hrs else 0
		tot_c += round(completed_hrs, 2)
		tot_nc += round(ncompleted_hrs, 2)
		tot_reopen_count += round(reopen_count, 2)
		tot_bt_hrs += ts_hours
		tot_spr_chrs += spr_comp_hrs
		tot_spr_whrs += spr_wor_hrs
		tot_spot_chrs += spot_comp_hrs
		tot_spot_whrs += spot_wor_hrs

		sub_total_rt += total_rt
		sub_tot_comp_rt += tot_comp_rt
		sub_tot_work_rt += tot_work_rt
		sub_nt_rt += nt_rt
		sub_total_s_rt += total_s_rt
		sub_tot_comp_srt += tot_comp_srt
		sub_tot_work_srt += tot_work_srt
		sub_nt_srt += nt_srt
		sub_bt_hours += bt_hours
		# sub_used_percent += used_percent
		sub_comp_per += comp_percent
		sub_ncomp_per += ncomp_percent
		tot_nc_rt += nc_rt

		spr_comp_s = f"{round(tot_comp_rt, 2)}/<br>{round(spr_comp_hrs, 2)}"
		spr_ncomp_s = f"{round(tot_work_rt, 2)}/<br>{round(spr_wor_hrs, 2)}"
		spot_comp_s = f"{round(tot_comp_srt, 2)}/<br>{round(spot_comp_hrs, 2)}"
		spot_ncomp_s = f"{round(tot_work_srt, 2)}/<br>{round(spot_wor_hrs, 2)}"

		used_percent_str = f"{ts_hours} ({round(used_percent, 2)}%)"
		comp_percent_str = f"{round(completed_hrs, 2)} ({round(comp_percent, 2)}%)"
		ncomp_percent_str = f"{round(ncompleted_hrs, 2)} ({round(ncomp_percent, 2)}%)"
		# if comp_percent < 70:
		font_color= "#f02e0c" if comp_percent < 70 else "#110404"
		att_color="#2059d4" if used_percent < 80 else "#110404"
		row_color = '#e8edea' if sr_no % 2 == 0 else '#ffffff'
		counts = frappe.db.sql("""
			SELECT
				SUM(CASE WHEN st.spot_task = 0 THEN 1 ELSE 0 END) AS total_count,
				SUM(CASE WHEN st.spot_task = 0 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_count,
				SUM(CASE WHEN st.spot_task = 0 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_count,
				SUM(CASE WHEN st.spot_task = 0 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_count,
				SUM(CASE WHEN st.spot_task = 1 THEN 1 ELSE 0 END) AS total_s_count,
				SUM(CASE WHEN st.spot_task = 1 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_scount,
				SUM(CASE WHEN st.spot_task = 1 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_scount,
				SUM(CASE WHEN st.spot_task = 1 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_scount,
				SUM(CASE WHEN st.revisions > 0 THEN revisions ELSE 0 END) AS reopen_count
			FROM `tabSprint Task` st
			WHERE st.parent = %s AND st.cb = %s
		""", (sprint.name, cb), as_dict=1)[0]

		total_count = counts.total_count or 0
		tot_comp_count = counts.tot_comp_count or 0
		tot_work_count = counts.tot_work_count or 0
		nt_count = counts.nt_count or 0
		total_s_count = counts.total_s_count or 0
		tot_comp_scount = counts.tot_comp_scount or 0
		tot_work_scount = counts.tot_work_scount or 0
		nt_scount = counts.nt_scount or 0
		reopen_count=counts.reopen_count or 0


		nc_count = frappe.db.sql("""
			SELECT SUM(e.nc_score)
			FROM `tabSprint Task` st
			JOIN `tabEnergy Point And Non Conformity` e
			ON e.task = st.task
			WHERE st.parent = %s
			AND st.cb = %s
			AND e.emp = %s
			AND e.docstatus != 2
		""", (sprint.name, cb, emp))[0][0] or 0


		sr_no += 1
		if sub_bt_hours > 0:
			sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
		else:
			sub_used_str=0
		if  tot_bt_hrs > 0:
			sub_comp_str=(tot_c/tot_bt_hrs)*100
		else:
			sub_comp_str=0
		if  tot_bt_hrs > 0:
			sub_work_str=(tot_nc/tot_bt_hrs)*100
		else:
			sub_work_str=0
		font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
		att_color="#2059d4" if sub_used_str < 80 else "#110404"
		sub_used_str = f"{round(tot_bt_hrs, 2)} ({round(sub_used_str, 2)})"
		sub_comp_str = f"{round(tot_c, 2)} ({round(sub_comp_str, 2)})"
		sub_work_str = f"{round(tot_nc, 2)} ({round(sub_work_str, 2)})"

		sub_total_count += total_count
		sub_tot_comp_count += tot_comp_count
		sub_tot_work_count += tot_work_count
		sub_nt_count += nt_count
		sub_total_s_count += total_s_count
		sub_tot_comp_scount += tot_comp_scount
		sub_tot_work_scount += tot_work_scount
		sub_nt_scount += nt_scount
		sub_total += total_count + total_s_count
		overall_comp += tot_comp_count + tot_comp_scount
		overall_work += tot_work_count + tot_work_scount
		overall_nt += nt_count + nt_scount
		sub_total_reopen_count += reopen_count
		tot_nc_count += nc_count

		
		sr_no += 1
	if sub_bt_hours > 0:
		sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
	else:
		sub_used_str=0
	if  tot_bt_hrs > 0:
		sub_comp_str=(tot_c/tot_bt_hrs)*100
	else:
		sub_comp_str=0
	if  tot_bt_hrs > 0:
		sub_work_str=(tot_nc/tot_bt_hrs)*100
	else:
		sub_work_str=0
	font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
	att_color="#2059d4" if sub_used_str < 80 else "#110404"
	sub_used_str = f"{round(tot_bt_hrs, 2)}"
	sub_comp_str = f"{round(tot_c, 2)}"
	sub_work_str = f"{round(tot_nc, 2)}"
	
	table += f"""
	<tr>
		<td style="background:#020c59;color:white;">Dev Team<td>
		<td style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
		<td style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/<br>{round(tot_spr_chrs, 2)}</td>
		<td style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/<br>{round(tot_spr_whrs, 2)}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_nt_rt}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_total_s_rt}</td>
		<td style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/<br>{round(tot_spot_chrs, 2)}</td>
		<td style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/<br>{round(tot_spot_whrs, 2)}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_nt_srt}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_rt + sub_total_s_rt}</td>
		<td style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
		<td style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
		<td style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
		<td style="background:#f0b616;color:#110404;">{sub_work_str}</td>
		<td style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
		<td style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
		<td style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
		<td style="background:#f0b616;color:#110404;">-</td>
		<td style="background:#f0b616;color:#110404;">-</td>
		<td style="background:#f0b616;color:#110404;">{overall_comp}</td>
		<td style="background:#f0b616;color:#110404;">{overall_work}</td>
		<td style="background:#f0b616;color:#110404;">{overall_nt}</td>
		<td style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
		
	</tr>

	"""

	table += """
		</table></div>
	"""
	# print(table)
	return table



@frappe.whitelist()
def summary_total(name):
	# dev_team =None
	# name ='SPRINT 21'
	all_tables = []

	dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='team_name')

	sprint_name = frappe.db.get_value(
	'Sprint',
	{'team': 'ALPHA', 'status': 'In Progress'},
	'sprint_id',
	order_by='creation desc'
	)

	
	if name:
		previous_sprint_id = name
	else:
		today = datetime.today()
		if today.strftime('%A') == 'Monday':
			previous_sprint_id =sprint_name
		else:
			if sprint_name and sprint_name.startswith("SPRINT"):
				current_number = int(sprint_name.replace("SPRINT", "").strip())
				previous_sprint_id = f"SPRINT {current_number - 1}"
			else:
				previous_sprint_id = None  


	table = f"""
	<div style="overflow-x: auto; margin-top: 20px; margin-left: 30px; margin-right: 30px">
	<table border="1" cellpadding="5" cellspacing="0" width="100%" style="border-collapse: collapse; text-align: center; min-width: 1200px;">
	<colgroup>
		<col span="33" style="width: 5.88%;">
	</colgroup>
	<tr>
		<td rowspan="2" style="color:red;">{previous_sprint_id}</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Hrs)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Hrs)</td>
		<td colspan="6" style="background:#f0b616;">Total (Hrs)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
		<td colspan="4" style="background:#d9edf7;">Sprint (Count)</td>
		<td colspan="4" style="background:#fcf8e3;">Others (Count)</td>
		<td colspan="6" style="background:#f0b616;">Total (Count)</td>
		<td colspan="2" style="background:#f0b616;">Observation</td>
	</tr>
	<tr>
		<!-- Hrs Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Hrs Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Hrs -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
		<!-- Count Sprint -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Others -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Comp.</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Count Total -->
		<td style="background:#020c59;color:white;">Plan</td>
		<td style="background:#020c59;color:white;">Attd</td>
		<td style="background:#020c59;color:white;">Used</td>
		<td style="background:#020c59;color:white;">Comp</td>
		<td style="background:#020c59;color:white;">Work</td>
		<td style="background:#020c59;color:white;">NT</td>
		<!-- Observation Count -->
		<td style="background:#020c59;color:white;">NC</td>
		<td style="background:#020c59;color:white;">Reopen</td>
	</tr>

	"""

	sub_total_rt = sub_tot_comp_rt = sub_tot_work_rt = sub_nt_rt = 0
	sub_total_s_rt = sub_tot_comp_srt = sub_tot_work_srt = sub_nt_srt = sub_bt_hours = 0
	sub_used_percent = sub_comp_per = sub_ncomp_per = tot_bt_hrs = tot_reopen_count = 0
	tot_c = tot_nc = tot_spr_chrs = tot_spr_whrs = tot_spot_chrs = tot_spot_whrs = tot_nc_rt = 0
	sub_total_count = sub_tot_comp_count =sub_tot_work_count =sub_nt_count =sub_total_s_count =0
	sub_tot_comp_scount = sub_tot_work_scount=sub_nt_scount=sub_total=overall_comp=0
	overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=0
	sr_no = 1
	# print(dev_teams)
	# dev_teams =['ALPHA']
	for team_name in dev_teams:
		sprint_name = frappe.db.get_value('Sprint', {'sprint_id': previous_sprint_id,'team':team_name}, 'name')
		if sprint_name:
			sprint = frappe.get_doc('Sprint', sprint_name)
			user_id = frappe.db.get_list('Employee', {'custom_dev_team': team_name,'status':'Active','department':'IT. Development - THIS'}, pluck='user_id')
			team_list = frappe.db.get_all('Employee', {'custom_dev_team': team_name, 'status': 'Active','department':'IT. Development - THIS'}, pluck='short_code') or ['']
			emp_list = frappe.db.get_all('Employee', {'custom_dev_team': team_name, 'status':'Active','department':'IT. Development - THIS'}, pluck='name')
			# print(team_list)
			# print(sprint.name)
			frappe.errprint(team_list)
			frappe.errprint(emp_list)
			result = frappe.db.sql("""
				SELECT
					SUM(CASE WHEN spot_task = 0 THEN rt ELSE 0 END),
					SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
					SUM(CASE WHEN spot_task = 0 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
					SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
					SUM(CASE WHEN spot_task = 0 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
					SUM(CASE WHEN spot_task = 0 AND at_period = 0 THEN rt ELSE 0 END),
					SUM(CASE WHEN spot_task = 1 THEN rt ELSE 0 END),
					SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
					SUM(CASE WHEN spot_task = 1 AND cr_status NOT IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
					SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN rt ELSE 0 END),
					SUM(CASE WHEN spot_task = 1 AND cr_status IN ('Open', 'Working', 'Code Review') AND at_period > 0 THEN at_period ELSE 0 END),
					SUM(CASE WHEN spot_task = 1 AND at_period = 0 THEN rt ELSE 0 END),
					SUM(CASE WHEN revisions > 0 THEN rt ELSE 0 END)
				FROM `tabSprint Task`
				WHERE parent = %s AND cb IN %s 
			""", (sprint.name, team_list))[0]
			# print(result)


			(
				total_rt, tot_comp_rt, spr_comp_hrs, tot_work_rt, spr_wor_hrs, nt_rt,
				total_s_rt, tot_comp_srt, spot_comp_hrs, tot_work_srt, spot_wor_hrs, nt_srt,reopen_count
			) = [x or 0 for x in result]

			completed_hrs = spr_comp_hrs + spot_comp_hrs
			ncompleted_hrs = spr_wor_hrs + spot_wor_hrs
			nc_rt = 0

			for st in sprint.sprint_task:
				if frappe.db.exists('Energy Point And Non Conformity',
					{'task': st.task, 'docstatus': ['!=', 2], 'emp': ['in',emp_list]}):
					nc_rt += st.rt or 0
			if emp_list:
				bt_hours = frappe.db.sql("""
					SELECT IFNULL(SUM(bt_difference), 0)
					FROM `tabAttendance`
					WHERE employee IN %s AND docstatus != 2
					AND attendance_date BETWEEN %s AND %s
				""", (emp_list, sprint.from_date, sprint.to_date))[0][0]
				bt_hours = round(bt_hours or 0, 2)

				ts_hours = frappe.db.sql("""
				SELECT IFNULL(SUM(total_hours), 0)
				FROM `tabTimesheet`
				WHERE employee IN %s AND docstatus != 2
				AND start_date BETWEEN %s AND %s
			""", (emp_list, sprint.from_date, sprint.to_date))[0][0]
				ts_hours = round(ts_hours or 0, 2)
			else:
				bt_hours=0
				ts_hours=0

			# ts_hours = frappe.db.sql("""
			# 	SELECT IFNULL(SUM(total_hours), 0)
			# 	FROM `tabTimesheet`
			# 	WHERE employee IN %s AND docstatus != 2
			# 	AND start_date BETWEEN %s AND %s
			# """, (emp_list, sprint.from_date, sprint.to_date))[0][0]
			# ts_hours = round(ts_hours or 0, 2)

			used_percent = (ts_hours / bt_hours) * 100 if ts_hours and bt_hours else 0
			comp_percent = (completed_hrs / ts_hours) * 100 if ts_hours and completed_hrs else 0
			ncomp_percent = (ncompleted_hrs / ts_hours) * 100 if ts_hours and ncompleted_hrs else 0
			tot_c += round(completed_hrs, 2)
			tot_nc += round(ncompleted_hrs, 2)
			tot_reopen_count += round(reopen_count, 2)
			tot_bt_hrs += ts_hours
			tot_spr_chrs += spr_comp_hrs
			tot_spr_whrs += spr_wor_hrs
			tot_spot_chrs += spot_comp_hrs
			tot_spot_whrs += spot_wor_hrs

			sub_total_rt += total_rt
			sub_tot_comp_rt += tot_comp_rt
			sub_tot_work_rt += tot_work_rt
			sub_nt_rt += nt_rt
			sub_total_s_rt += total_s_rt
			sub_tot_comp_srt += tot_comp_srt
			sub_tot_work_srt += tot_work_srt
			sub_nt_srt += nt_srt
			sub_bt_hours += bt_hours
			# sub_used_percent += used_percent
			sub_comp_per += comp_percent
			sub_ncomp_per += ncomp_percent
			tot_nc_rt += nc_rt

			spr_comp_s = f"{round(tot_comp_rt, 2)}/<br>{round(spr_comp_hrs, 2)}"
			spr_ncomp_s = f"{round(tot_work_rt, 2)}/<br>{round(spr_wor_hrs, 2)}"
			spot_comp_s = f"{round(tot_comp_srt, 2)}/<br>{round(spot_comp_hrs, 2)}"
			spot_ncomp_s = f"{round(tot_work_srt, 2)}/<br>{round(spot_wor_hrs, 2)}"

			used_percent_str = f"{ts_hours} ({round(used_percent, 2)}%)"
			comp_percent_str = f"{round(completed_hrs, 2)} ({round(comp_percent, 2)}%)"
			ncomp_percent_str = f"{round(ncompleted_hrs, 2)} ({round(ncomp_percent, 2)}%)"
			# if comp_percent < 70:
			font_color= "#f02e0c" if comp_percent < 70 else "#110404"
			att_color="#2059d4" if used_percent < 80 else "#110404"
			row_color = '#e8edea' if sr_no % 2 == 0 else '#ffffff'
			counts = frappe.db.sql("""
				SELECT
					SUM(CASE WHEN st.spot_task = 0 THEN 1 ELSE 0 END) AS total_count,
					SUM(CASE WHEN st.spot_task = 0 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_count,
					SUM(CASE WHEN st.spot_task = 0 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_count,
					SUM(CASE WHEN st.spot_task = 0 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_count,
					SUM(CASE WHEN st.spot_task = 1 THEN 1 ELSE 0 END) AS total_s_count,
					SUM(CASE WHEN st.spot_task = 1 AND st.cr_status NOT IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_comp_scount,
					SUM(CASE WHEN st.spot_task = 1 AND st.cr_status IN ('Open','Working','Code Review') AND IFNULL(st.at_period, 0) > 0 THEN 1 ELSE 0 END) AS tot_work_scount,
					SUM(CASE WHEN st.spot_task = 1 AND IFNULL(st.at_period, 0) = 0 THEN 1 ELSE 0 END) AS nt_scount,
					SUM(CASE WHEN st.revisions > 0 THEN revisions ELSE 0 END) AS reopen_count
				FROM `tabSprint Task` st
				WHERE st.parent = %s AND st.cb IN %s
			""", (sprint.name, team_list), as_dict=1)[0]

			total_count = counts.total_count or 0
			tot_comp_count = counts.tot_comp_count or 0
			tot_work_count = counts.tot_work_count or 0
			nt_count = counts.nt_count or 0
			total_s_count = counts.total_s_count or 0
			tot_comp_scount = counts.tot_comp_scount or 0
			tot_work_scount = counts.tot_work_scount or 0
			nt_scount = counts.nt_scount or 0
			reopen_count=counts.reopen_count or 0

			if emp_list and team_list:
				nc_count = frappe.db.sql("""
					SELECT SUM(e.nc_score)
					FROM `tabSprint Task` st
					JOIN `tabEnergy Point And Non Conformity` e
					ON e.task = st.task
					WHERE st.parent = %s
					AND st.cb IN %s
					AND e.emp IN %s
					AND e.docstatus != 2
				""", (sprint.name, team_list, emp_list))[0][0] or 0
			else:
				nc_count=0


			sr_no += 1
			if sub_bt_hours > 0:
				sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
			else:
				sub_used_str=0
			if  tot_bt_hrs > 0:
				sub_comp_str=(tot_c/tot_bt_hrs)*100
			else:
				sub_comp_str=0
			if  tot_bt_hrs > 0:
				sub_work_str=(tot_nc/tot_bt_hrs)*100
			else:
				sub_work_str=0
			font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
			att_color="#2059d4" if sub_used_str < 80 else "#110404"
			sub_used_str = f"{round(tot_bt_hrs, 2)} ({round(sub_used_str, 2)})"
			sub_comp_str = f"{round(tot_c, 2)} ({round(sub_comp_str, 2)})"
			sub_work_str = f"{round(tot_nc, 2)} ({round(sub_work_str, 2)})"

			sub_total_count += total_count
			sub_tot_comp_count += tot_comp_count
			sub_tot_work_count += tot_work_count
			sub_nt_count += nt_count
			sub_total_s_count += total_s_count
			sub_tot_comp_scount += tot_comp_scount
			sub_tot_work_scount += tot_work_scount
			sub_nt_scount += nt_scount
			sub_total += total_count + total_s_count
			overall_comp += tot_comp_count + tot_comp_scount
			overall_work += tot_work_count + tot_work_scount
			overall_nt += nt_count + nt_scount
			sub_total_reopen_count += reopen_count
			tot_nc_count += nc_count

			table += f"""
			<tr style="background-color: {row_color};color:#110404;">
				<td>{team_name}</td>
				<td>{total_rt}</td>
				<td>{spr_comp_s}</td>
				<td>{spr_ncomp_s}</td>
				<td>{nt_rt}</td>
				<td>{total_s_rt}</td>
				<td>{spot_comp_s}</td>
				<td>{spot_ncomp_s}</td>
				<td>{nt_srt}</td>
				<td>{total_rt + total_s_rt}</td>
				<td>{bt_hours}</td>
				<td  style="color: {att_color};">{used_percent_str}</td>
				<td style="color: {font_color};">{comp_percent_str}</td>
				<td>{ncomp_percent_str}</td>
				<td>{round(nt_rt + nt_srt, 2)}</td>
				<td>{nc_rt}</td>
				<td>{round(reopen_count, 2)}</td>
				<td>{total_count}</td>
				<td>{tot_comp_count}</td>
				<td>{tot_work_count}</td>
				<td>{nt_count}</td>
				<td>{total_s_count}</td>
				<td>{tot_comp_scount}</td>
				<td>{tot_work_scount}</td>
				<td>{nt_scount}</td>
				<td>{total_count + total_s_count}</td>
				<td>-</td>
				<td>-</td>
				<td>{tot_comp_count + tot_comp_scount}</td>
				<td>{tot_work_count + tot_work_scount}</td>
				<td>{nt_count + nt_scount}</td>
				<td>{nc_count}</td>
				<td>{reopen_count}</td>
			</tr>
			"""
			# print(table)

			sr_no += 1
		
		
	if sub_bt_hours > 0:
		sub_used_str=(tot_bt_hrs/sub_bt_hours)*100
	else:
		sub_used_str=0
	if  tot_bt_hrs > 0:
		sub_comp_str=(tot_c/tot_bt_hrs)*100
	else:
		sub_comp_str=0
	if  tot_bt_hrs > 0:
		sub_work_str=(tot_nc/tot_bt_hrs)*100
	else:
		sub_work_str=0
	font_color= "#f02e0c" if sub_comp_str < 70 else "#110404"
	att_color="#2059d4" if sub_used_str < 80 else "#110404"
	sub_used_str = f"{round(tot_bt_hrs, 2)}"
	sub_comp_str = f"{round(tot_c, 2)}"
	sub_work_str = f"{round(tot_nc, 2)}"
	
	table += f"""
	<tr>
		<td style="background:#020c59;color:white;">Total(Hrs)</td>
		<td style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
		<td style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/<br>{round(tot_spr_chrs, 2)}</td>
		<td style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/<br>{round(tot_spr_whrs, 2)}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_nt_rt}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_total_s_rt}</td>
		<td style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/<br>{round(tot_spot_chrs, 2)}</td>
		<td style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/<br>{round(tot_spot_whrs, 2)}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_nt_srt}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_rt + sub_total_s_rt}</td>
		<td style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
		<td style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
		<td style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
		<td style="background:#f0b616;color:#110404;">{sub_work_str}</td>
		<td style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
		<td style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
		<td style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
		<td style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
		<td style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
		<td style="background:#f0b616;color:#110404;">-</td>
		<td style="background:#f0b616;color:#110404;">-</td>
		<td style="background:#f0b616;color:#110404;">{overall_comp}</td>
		<td style="background:#f0b616;color:#110404;">{overall_work}</td>
		<td style="background:#f0b616;color:#110404;">{overall_nt}</td>
		<td style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
		<td style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
		
	</tr>

	"""

	table += """
		</table></div>
	"""
	# print(table)
	return table


# @frappe.whitelist()
# def summary_total(name=None):
# 	if not name:
# 		continue  # Avoid frappe.throw for CLI usage

# 	result = frappe.db.sql("""
# 		SELECT 
# 			dev_team,
# 			SUM(planned_story_points) AS planned_story_points,
# 			SUM(completed_story_points) AS completed_story_points,
# 			SUM(carry_forward_story_points) AS carry_forward_story_points,
# 			SUM(reopened_story_points) AS reopened_story_points,
# 			SUM(bug_points) AS bug_points,
# 			SUM(completed_bug_points) AS completed_bug_points,
# 			SUM(carry_forward_bug_points) AS carry_forward_bug_points,
# 			SUM(reopened_bug_points) AS reopened_bug_points
# 		FROM `tabRetro Sprint Task`
# 		WHERE parent = %s
# 		GROUP BY dev_team
# 		ORDER BY dev_team
# 	""", (name,), as_dict=1)

# 	total = frappe.db.sql("""
# 		SELECT 
# 			'Total' AS dev_team,
# 			SUM(planned_story_points) AS planned_story_points,
# 			SUM(completed_story_points) AS completed_story_points,
# 			SUM(carry_forward_story_points) AS carry_forward_story_points,
# 			SUM(reopened_story_points) AS reopened_story_points,
# 			SUM(bug_points) AS bug_points,
# 			SUM(completed_bug_points) AS completed_bug_points,
# 			SUM(carry_forward_bug_points) AS carry_forward_bug_points,
# 			SUM(reopened_bug_points) AS reopened_bug_points
# 		FROM `tabRetro Sprint Task`
# 		WHERE parent = %s
# 	""", (name,), as_dict=1)

# 	if total:
# 		result.append(total[0])

# 	return result



@frappe.whitelist()
def opportunity_excel_report():
    posting_date = datetime.now().strftime("%d-%m-%Y")
    filename_opp = "PR:01 – Opportunity Status Report (OSR)_" + posting_date
    build_xlsx_response_opp(filename_opp)


def build_xlsx_response_opp(filename_opp):
    xlsx_file = make_xlsx_opp(filename_opp)
    frappe.response['filename'] = filename_opp + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'


def make_xlsx_opp(data, sheet_name="PR:01 – Opportunity Status Report (OSR)", wb=None, column_widths=None):
    args = frappe.local.form_dict

    # Create workbook and sheet
    if wb is None:
        wb = Workbook()
    valid_sheet_name = sheet_name.replace(":", "-")
    ws = wb.create_sheet(valid_sheet_name, 0)

    # === Styles ===
    text_wrap_left = Alignment(wrap_text=True, vertical="center", horizontal="left")
    fill_color = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    title_font = Font(bold=True, size=14)
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    center_alignment = Alignment(horizontal="center", vertical="center")

    # === Column widths ===
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M','N']
    column_widths = [6, 8, 10, 20, 10, 35, 15,10 ,15 ,6, 13, 13, 15, 45]
    for i, width in enumerate(column_widths):
        ws.column_dimensions[columns[i]].width = width

    # === Title ===
    posting_date = datetime.now().strftime("%d-%m-%Y")
    title = f"PR:01 – Opportunity Status Report (OSR) ({posting_date})"
    ws.merge_cells("A1:N1")
    ws["A1"].value = title
    ws["A1"].font = title_font
    ws["A1"].alignment = center_alignment

    # === Header row ===
    header = ["S NO", "Owner", "Service", "From", "Status", "Organization Name","Territory","Grade",
              "Date", "Age", "Amount", "PB%", "ECD", "Remark"]
    ws.append(header)

    for cell in ws[2]:
        cell.fill = fill_color
        cell.font = header_font
        cell.alignment = center_alignment
        cell.border = thin_border

    # === Data ===
    data1 = get_data_of_opp(args)

    # Sort only for stable grouping (without disturbing data)
    data1.sort(key=lambda x: x[1] or "")

    current_row = 3

    # Group by exact owner to avoid merging similar codes like AP and API
    for owner, group in groupby(data1, key=lambda x: x[1]):
        group_rows = list(group)
        start_row = current_row

        # Write each row
        for row in group_rows:
            ws.append(row)
            for cell in ws[ws.max_row]:
                cell.alignment = text_wrap_left
                cell.border = thin_border
            current_row += 1

        # Merge owner cells only if multiple rows belong to the same owner
        if len(group_rows) > 1:
            ws.merge_cells(start_row=start_row, start_column=2, end_row=current_row - 1, end_column=2)
            ws.cell(row=start_row, column=2).alignment = Alignment(horizontal="left", vertical="center")

    # Adjust row height for readability
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        ws.row_dimensions[row[0].row].height = 45

    # Save workbook
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file

def get_data_of_opp(args):

    own = args.get("opportunity_owner")
    am = args.get("opp_am")
    ser = args.get("opp_service")

    data = []
    s_no = 1
    filters = {
    "status": ["in", ["Open", "Quotation", "Replied"]],
    "opportunity_owner": ["not in", [None, ""]],
	"service": "IT-SW"
}

    if own:
        filters["opportunity_owner"] = own

    if am:
        filters["lead_owner"] = am

    if ser:
        filters["service"] = ser

    opportunity_data = frappe.db.get_all("Opportunity", filters, "*")
    grouped_data = {}
    
    for opportunity in opportunity_data:
        owner = opportunity.get("opportunity_owner")
        if owner not in grouped_data and owner:
            grouped_data[owner] = []
        grouped_data[owner].append(opportunity)
        

    
    for j, opportunities in grouped_data.items():
        for i in opportunities:
            employee_short_code = frappe.db.get_value("Employee", {"user_id": j}, "short_code")
            formatted_transaction_date = frappe.utils.formatdate(i.transaction_date, 'dd-mm-yyyy')
            formatted_ecd_date = frappe.utils.formatdate(i.expected_closing, 'dd-mm-yyyy')
            terr = frappe.db.get_value("Sales Follow Up",{"name":i.custom_sales_follow_up},"sfp_territory") or ""
            market_segment = frappe.db.get_value("Sales Follow Up",{"name":i.custom_sales_follow_up},"market_segment") or ""
            data.append([
                s_no, 
                employee_short_code or '', 
                i.service, 
                i.opportunity_from, 
                i.status, 
                i.organization_name,
                terr,
                market_segment,
                formatted_transaction_date,
                i.custom_opportunity_age, 
                i.opportunity_amount, 
                i.probability, 
                formatted_ecd_date,
                i.remark
            ])
            s_no += 1

    return data 


@frappe.whitelist()
def get_amc_project_sla_table():

    today = getdate(nowdate())

    final_data = []
    seen = set()

    # AMC Projects
    projects = frappe.get_all(
        "Project",
        filters={
            "service": "IT-SW",
            "status": ["!=", "Completed"],
            "project_type": "AMC"
        },
        fields=["name", "project_name", "customer"]
    )

    for proj in projects:

        if not proj.customer:
            continue

        customer = frappe.get_doc("Customer", proj.customer)

        if not customer.custom_sla_details:
            continue

        for sla in customer.custom_sla_details:

            if not sla.sla_to_date:
                continue

            sla_date = getdate(sla.sla_to_date)
            days_remaining = (sla_date - today).days

            # ✅ SHOW ONLY EXPIRED + 0-90 DAYS
            if sla_date < today:
                status = "Expired"
                color = "red"
                order_no = 1

            elif 0 <= days_remaining <= 90:
                status = f"Expiring in {days_remaining} Days"
                color = "blue"
                order_no = 2

            else:
                status = f"{days_remaining} Days Remaining" 
                color = "black" 
                order_no = 3

            key = (
				proj.customer,
				sla.project,
				sla.sla_type,
				sla.sla_to_date
			)

            if key in seen:
                continue

            seen.add(key)

            final_data.append({
				"customer": proj.customer,
                "customer_name": customer.customer_name,
                "project": sla.project,
                "service": sla.service,
                "sla_type": sla.sla_type,
                "sla_from_date": formatdate(sla.sla_from_date, "dd-MM-yyyy") if sla.sla_from_date else "",
                "sla_to_date": formatdate(sla.sla_to_date, "dd-MM-yyyy"),
                "description": sla.description or "",
                "status": status,
                "color": color,
                "order_no": order_no,
                "days_remaining": days_remaining
            })

    # Sorting
    final_data = sorted(final_data, key=lambda x: (x["order_no"], x["days_remaining"]))

    # HTML table
    table_rows = ""

    for idx, row in enumerate(final_data):

        bg_color = "#ffffff" if idx % 2 == 0 else "#e7e6ec"

        table_rows += f"""
            <tr style="background:{bg_color}; color:{row['color']};">

                <td style="padding:8px; border:1px solid #ccc;">
                    {idx + 1}
                </td>

                <td style="padding:8px; border:1px solid #ccc; text-align:left;">
					<a 
						href="/app/customer/{row['customer']}" 
						target="_blank"
						style="color:{row['color']}; text-decoration:none; font-weight:500;"
					>
						{row['customer_name']}
					</a>
				</td>

				<td style="padding:8px; border:1px solid #ccc; text-align:left;">
					<a 
						href="/app/project/{row['project']}" 
						target="_blank"
						style="color:{row['color']}; text-decoration:none; font-weight:500;"
					>
						{row['project']}
					</a>
				</td>

                <td style="padding:8px; border:1px solid #ccc;">
                    {row['sla_type']}
                </td>

                <td style="padding:8px; border:1px solid #ccc;">
                    {row['sla_from_date']}
                </td>

                <td style="padding:8px; border:1px solid #ccc;">
                    {row['sla_to_date']}
                </td>

                <td style="padding:8px; border:1px solid #ccc;">
                    {row['status']}
                </td>

            </tr>
        """

    html_table = f"""
        <table style="width:100%; border-collapse:collapse; font-size:13px;">

            <thead>
                <tr style="background:#d9d9d9; color:black;">
                    <th style="padding:10px; border:1px solid #ccc;">S.No</th>
                    <th style="padding:10px; border:1px solid #ccc;">Customer</th>
                    <th style="padding:10px; border:1px solid #ccc;">Project</th>
                    <th style="padding:10px; border:1px solid #ccc;">SLA Type</th>
                    <th style="padding:10px; border:1px solid #ccc;">From Date</th>
                    <th style="padding:10px; border:1px solid #ccc;">To Date</th>
                    <th style="padding:10px; border:1px solid #ccc;">Status</th>
                </tr>
            </thead>

            <tbody>
                {table_rows}
            </tbody>

        </table>
    """

    return html_table




import frappe
from frappe.utils import getdate, nowdate, formatdate
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from frappe.utils.file_manager import save_file
import io


@frappe.whitelist()
def download_amc_project_sla_excel():

    today = getdate(nowdate())

    final_data = []
    seen = set()

    projects = frappe.get_all(
        "Project",
        filters={
            "service": "IT-SW",
            "status": ["!=", "Completed"],
            "project_type": "AMC"
        },
        fields=["name", "project_name", "customer"]
    )

    for proj in projects:

        if not proj.customer:
            continue

        customer = frappe.get_doc("Customer", proj.customer)

        if not customer.custom_sla_details:
            continue

        for sla in customer.custom_sla_details:

            if not sla.sla_to_date:
                continue

            sla_date = getdate(sla.sla_to_date)
            days_remaining = (sla_date - today).days

            if sla_date < today:
                status = "Expired"
                color = "FF0000"
                order_no = 1

            elif 0 <= days_remaining <= 90:
                status = f"Expiring in {days_remaining} Days"
                color = "0000FF"
                order_no = 2

            else:
                status = f"{days_remaining} Days Remaining"
                color = "000000"
                order_no = 3

            key = (
                proj.customer,
                sla.project,
                sla.sla_type,
                sla.sla_to_date
            )

            if key in seen:
                continue

            seen.add(key)

            final_data.append({
                "customer_name": customer.customer_name,
                "project": sla.project,
                "sla_type": sla.sla_type,
                "sla_from_date": formatdate(sla.sla_from_date, "dd-MM-yyyy") if sla.sla_from_date else "",
                "sla_to_date": formatdate(sla.sla_to_date, "dd-MM-yyyy"),
                "status": status,
                "color": color,
                "order_no": order_no,
                "days_remaining": days_remaining
            })

    final_data = sorted(final_data, key=lambda x: (x["order_no"], x["days_remaining"]))

    wb = Workbook()
    ws = wb.active
    ws.title = "AMC Projects"

    headers = [
        "S.No",
        "Customer",
        "Project",
        "SLA Type",
        "From Date",
        "To Date",
        "Status"
    ]

    # Header Style
    header_fill = PatternFill(start_color="0F1568", end_color="0F1568", fill_type="solid")

    thin = Side(border_style="thin", color="CCCCCC")

    header_font = Font(bold=True,color="FFFFFF")

    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")

    for col_num, header in enumerate(headers, 1):

        cell = ws.cell(row=1, column=col_num, value=header)

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
        cell.border = Border(
            left=thin,
            right=thin,
            top=thin,
            bottom=thin
        )

    # Data Rows
    for idx, row in enumerate(final_data, start=2):

        bg_color = "FFFFFF" if idx % 2 == 0 else "E7E6EC"

        row_fill = PatternFill(
            start_color=bg_color,
            end_color=bg_color,
            fill_type="solid"
        )

        values = [
            idx - 1,
            row["customer_name"],
            row["project"],
            row["sla_type"],
            row["sla_from_date"],
            row["sla_to_date"],
            row["status"]
        ]

        for col_num, value in enumerate(values, 1):

            cell = ws.cell(row=idx, column=col_num, value=value)

            cell.fill = row_fill

            cell.font = Font(color=row["color"])

            cell.border = Border(
                left=thin,
                right=thin,
                top=thin,
                bottom=thin
            )

            if col_num in [2, 3]:
                cell.alignment = left_align
            else:
                cell.alignment = center_align

    # Column Width
    widths = {
        1: 10,
        2: 35,
        3: 30,
        4: 20,
        5: 18,
        6: 18,
        7: 30
    }

    for col, width in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = width

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    frappe.response.filename = "AMC_Projects.xlsx"
    frappe.response.filecontent = output.getvalue()
    frappe.response.type = "binary"


from collections import defaultdict
from datetime import datetime, timedelta
import frappe

@frappe.whitelist()
def dsr_table(date=None):

    from collections import defaultdict
    from datetime import datetime, timedelta

    if not date:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    dev_team_order = {}

    dev_teams = frappe.get_all(
        "Dev Team",
        fields=["name", "order_for_it_dashboard"]
    )

    for d in dev_teams:
        dev_team_order[d.name] = d.order_for_it_dashboard or 999

    cb_order = {}

    employees = frappe.get_all(
		"Employee",
		{
			"status": "Active",
			"department": "IT. Development - THIS"
		},
		["short_code", "custom_order_for_it_dashboard"]
	)

    for e in employees:

        short_code = (e.short_code or "").strip().upper()

        cb_order[short_code] = e.custom_order_for_it_dashboard or 999

    daily_monitors = frappe.get_all(
        "Daily Monitor",
        {
            "date": date,
            "service": "IT-SW",
            "dsr_check": 1
        },
        ["name", "dev_team"]
    )

    all_tasks = []

    for dm in daily_monitors:

        doc = frappe.get_doc("Daily Monitor", dm.name)

        for row in doc.task_details:

            row.dev_team = dm.dev_team

            all_tasks.append(row)

    if not all_tasks:

        return """
        <div style="
            padding:20px;
            text-align:center;
            color:red;
            font-weight:bold;
        ">
            No Data Found
        </div>
        """

    sorted_tasks = sorted(
        all_tasks,
        key=lambda x: (
            dev_team_order.get(x.dev_team, 999),
            cb_order.get((x.cb or "").strip().upper(), 999),
            x.project_name or "",
            x.priority or ""
        )
    )

    cb_summary = defaultdict(lambda: {
        "rt": 0,
        "at": 0
    })

    for i in sorted_tasks:

        # cb = i.cb or "Not Set"
        cb = (i.cb or "Not Set").strip().upper()

        cb_summary[cb]["rt"] += float(i.today_rt or 0)
        cb_summary[cb]["at"] += float(i.at_taken or 0)

    summary_table = """
    <table border="1" width="100%" style="
        border-collapse:collapse;
        background:white;
        font-size:13px;
        text-align:center;
    ">

        <tr style="
            background:#0f1568;
            color:white;
            height:35px;
            position:sticky;
            top:0;
            z-index:2;
        ">
            <th>CB</th>
            <th>APH</th>
            <th>RT</th>
            <th>AT</th>
            <th>RT Vs AT%</th>
        </tr>
    """

    grand_aph = 0
    grand_rt = 0
    grand_at = 0


    summary_sorted = sorted(
		cb_summary.items(),
		key=lambda x: cb_order.get(
			str(x[0]).strip().upper(),
			999
		)
	)

    for idx, (cb, v) in enumerate(summary_sorted, start=1):

        bg = "#ffffff" if idx % 2 else "#e7e6ec"

        aph = 6 if frappe.db.get_value(
            "Employee",
            {
                "short_code": cb,
                "custom_is_tl": 1,
                "custom_is_sub_tl": 0
            },
            "name"
        ) else 8

        rt = min(v["rt"], aph)

        at = v["at"]

        ratio = round((at / rt) * 100, 2) if rt else 0

        grand_aph += aph
        grand_rt += rt
        grand_at += at

        ratio_color = "#f54545" if ratio < 75 else "#000"

        summary_table += f"""
        <tr style="height:32px;color:black">

            <td>{cb}</td>

            <td>{aph}</td>

            <td>{round(rt,2)}</td>

            <td>{round(at,2)}</td>

            <td style="
                color:{ratio_color};
                font-weight:bold;
            ">
                {ratio}
            </td>

        </tr>
        """

    grand_ratio = round((grand_at / grand_rt) * 100, 2) if grand_rt else 0

    grand_ratio_color = "#f54545" if grand_ratio < 75 else "#000"

    summary_table += f"""
        <tr style="
            background:#e7e7e7;
            font-weight:bold;
            height:40px;
			color:black
        ">

            <td>Grand Total</td>

            <td>{grand_aph}</td>

            <td>{round(grand_rt,2)}</td>

            <td>{round(grand_at,2)}</td>

            <td style="color:{grand_ratio_color};">
                {grand_ratio}
            </td>

        </tr>

    </table>
    """

    data = """
    <table border="1" width="100%" style="
        border-collapse:collapse;
        font-size:12px;
        background:white;
        table-layout:fixed;
    ">

        <tr style="
            background:#0f1568;
            color:white;
            text-align:center;
            position:sticky;
            top:0;
            z-index:2;
        ">

            <th style="width:6%;padding:8px;">SI NO</th>
            <th style="width:10%;padding:8px;">Dev Team</th>
            <th style="width:10%;padding:8px;">Task ID</th>
            <th style="width:15%;padding:8px;">Project Name</th>
            <th style="width:22%;padding:8px;">Subject</th>
            <th style="width:7%;padding:8px;">CB</th>
            <th style="width:15%;padding:8px;">Status</th>
            <th style="width:6%;padding:8px;">ET</th>
            <th style="width:6%;padding:8px;">RT</th>
            <th style="width:8%;padding:8px;">AT Total</th>
            <th style="width:9%;padding:8px;">AT Period</th>
            <th style="width:10%;padding:8px;">Priority</th>
            <th style="width:20%;padding:8px;">Working Remarks</th>
            <th style="width:15%;padding:8px;">ET vs AT Remarks</th>
            <th style="width:10%;padding:8px;">TL Remarks</th>

        </tr>
    """

    for idx, i in enumerate(sorted_tasks, start=1):

        bg = "#ffffff" if idx % 2 else "#e7e6ec"

        data += f"""
        <tr style="
            background:{bg};
            text-align:center;
			color:black
        ">

            <td style="padding:6px;">
                {idx}
            </td>

            <td style="padding:6px;">
                {i.dev_team or '-'}
            </td>

            <td style="padding:6px;color:black">

                <a href="/app/task/{i.id}"
                   target="_blank"
                   style="
                        text-decoration:none;
                   ">

                    {i.id or '-'}

                </a>

            </td>

            <td style="padding:6px;word-break:break-word;">
                {i.project_name or '-'}
            </td>

            <td style="padding:6px;word-break:break-word;">
                {i.subject or '-'}
            </td>

            <td style="padding:6px;">
                {i.cb or '-'}
            </td>

            <td style="padding:6px;">
                {i.current_status or '-'}
            </td>

            <td style="padding:6px;">
                {i.et or 0}
            </td>

            <td style="padding:6px;">
                {i.rt or 0}
            </td>

            <td style="padding:6px;">
                {round(float(i.at or 0), 2)}
            </td>

            <td style="padding:6px;">
                {round(float(i.at_taken or 0), 2)}
            </td>

            <td style="padding:6px;">
                {i.priority or '-'}
            </td>

            <td style="padding:6px;word-break:break-word;">
                {i.remark or '-'}
            </td>

            <td style="padding:6px;word-break:break-word;">
                {i.et_vs_at_remark or '-'}
            </td>

            <td style="padding:6px;word-break:break-word;">
                {i.remarks or '-'}
            </td>

        </tr>
        """

    data += "</table>"

    final_html = f"""
    <div style="
        display:flex;
        gap:15px;
        align-items:flex-start;
    ">

        <!-- LEFT SUMMARY -->

        <div style="
            width:30%;
            flex:0 0 30%;
            height:500px;
            overflow:auto;
            position:sticky;
            top:10px;
        ">

            {summary_table}

        </div>

        <!-- RIGHT TABLE -->

        <div style="
            width:100%;
            flex:0 0 100%;
            overflow:auto;
            max-height:500px;
        ">

            {data}

        </div>

    </div>
    """

    return final_html


@frappe.whitelist()
def download_dsr_excel(date=None):

    import io
    import frappe

    from collections import defaultdict
    from datetime import datetime, timedelta

    from openpyxl import Workbook
    from openpyxl.styles import (
        Font,
        PatternFill,
        Border,
        Side,
        Alignment
    )

    from openpyxl.utils import get_column_letter

    if not date:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # =====================================================
    # Orders
    # =====================================================

    dev_team_order = {}

    dev_teams = frappe.get_all(
        "Dev Team",
        fields=["name", "order_for_it_dashboard"]
    )

    for d in dev_teams:
        dev_team_order[d.name] = d.order_for_it_dashboard or 999

    cb_order = {}

    employees = frappe.get_all(
        "Employee",
        {
            "status": "Active",
            "department": "IT. Development - THIS"
        },
        ["short_code", "custom_order_for_it_dashboard"]
    )

    for e in employees:

        short_code = (e.short_code or "").strip().upper()

        cb_order[short_code] = (
            e.custom_order_for_it_dashboard or 999
        )

    # =====================================================
    # Daily Monitor Data
    # =====================================================

    daily_monitors = frappe.get_all(
        "Daily Monitor",
        {
            "date": date,
            "service": "IT-SW",
            "dsr_check": 1
        },
        ["name", "dev_team"]
    )

    all_tasks = []

    for dm in daily_monitors:

        doc = frappe.get_doc(
            "Daily Monitor",
            dm.name
        )

        for row in doc.task_details:

            row.dev_team = dm.dev_team

            all_tasks.append(row)

    # =====================================================
    # Sorting
    # =====================================================

    sorted_tasks = sorted(
        all_tasks,
        key=lambda x: (
            dev_team_order.get(x.dev_team, 999),
            cb_order.get(
                (x.cb or "").strip().upper(),
                999
            ),
            x.project_name or "",
            x.priority or ""
        )
    )

    # =====================================================
    # Workbook
    # =====================================================

    wb = Workbook()

    ws = wb.active

    ws.title = "DSR Report"

    # =====================================================
    # Styles
    # =====================================================

    header_fill = PatternFill(
        start_color="0F1568",
        end_color="0F1568",
        fill_type="solid"
    )

    odd_fill = PatternFill(
        start_color="FFFFFF",
        end_color="FFFFFF",
        fill_type="solid"
    )

    even_fill = PatternFill(
        start_color="E7E6EC",
        end_color="E7E6EC",
        fill_type="solid"
    )

    grand_fill = PatternFill(
        start_color="E7E7E7",
        end_color="E7E7E7",
        fill_type="solid"
    )

    thin = Side(
        style="thin",
        color="CCCCCC"
    )

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin
    )

    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    normal_font = Font(
        color="000000"
    )

    bold_font = Font(
        bold=True,
        color="000000"
    )

    center_align = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )

    left_align = Alignment(
        horizontal="left",
        vertical="top",
        wrap_text=True
    )

    # =====================================================
    # LEFT SUMMARY TABLE
    # =====================================================

    cb_summary = defaultdict(lambda: {
        "rt": 0,
        "at": 0
    })

    for i in sorted_tasks:

        cb = (i.cb or "Not Set").strip().upper()

        cb_summary[cb]["rt"] += float(
            i.today_rt or 0
        )

        cb_summary[cb]["at"] += float(
            i.at_taken or 0
        )

    summary_headers = [
        "CB",
        "APH",
        "RT",
        "AT",
        "RT Vs AT%"
    ]

    summary_start_col = 1

    # Summary Headers
    for col_num, header in enumerate(
        summary_headers,
        summary_start_col
    ):

        cell = ws.cell(
            row=1,
            column=col_num,
            value=header
        )

        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = center_align

    grand_aph = 0
    grand_rt = 0
    grand_at = 0

    summary_sorted = sorted(
        cb_summary.items(),
        key=lambda x: cb_order.get(
            str(x[0]).strip().upper(),
            999
        )
    )

    summary_row = 2

    for idx, (cb, v) in enumerate(
        summary_sorted,
        start=1
    ):

        fill = (
            odd_fill
            if idx % 2 == 0
            else even_fill
        )

        aph = 6 if frappe.db.get_value(
            "Employee",
            {
                "short_code": cb,
                "custom_is_tl": 1,
                "custom_is_sub_tl": 0
            },
            "name"
        ) else 8

        rt = min(v["rt"], aph)

        at = v["at"]

        ratio = round(
            (at / rt) * 100,
            2
        ) if rt else 0

        grand_aph += aph
        grand_rt += rt
        grand_at += at

        values = [
            cb,
            aph,
            round(rt, 2),
            round(at, 2),
            ratio
        ]

        for col_num, value in enumerate(
            values,
            summary_start_col
        ):

            cell = ws.cell(
                row=summary_row,
                column=col_num,
                value=value
            )

            cell.fill = fill
            cell.border = border
            cell.font = normal_font
            cell.alignment = center_align

        summary_row += 1

    # =====================================================
    # Grand Total
    # =====================================================

    grand_ratio = round(
        (grand_at / grand_rt) * 100,
        2
    ) if grand_rt else 0

    grand_values = [
        "Grand Total",
        grand_aph,
        round(grand_rt, 2),
        round(grand_at, 2),
        grand_ratio
    ]

    for col_num, value in enumerate(
        grand_values,
        summary_start_col
    ):

        cell = ws.cell(
            row=summary_row,
            column=col_num,
            value=value
        )

        cell.fill = grand_fill
        cell.border = border
        cell.font = bold_font
        cell.alignment = center_align

    # =====================================================
    # MAIN TABLE
    # =====================================================

    headers = [
        "SI NO",
        "Dev Team",
        "Task ID",
        "Project Name",
        "Subject",
        "CB",
        "Status",
        "ET",
        "RT",
        "AT Total",
        "AT Period",
        "Priority",
        "Working Remarks",
        "ET vs AT Remarks",
        "TL Remarks"
    ]

    main_start_col = 8

    # Main Headers
    for col_num, header in enumerate(
        headers,
        main_start_col
    ):

        cell = ws.cell(
            row=1,
            column=col_num,
            value=header
        )

        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = center_align

    # =====================================================
    # Main Data Rows
    # =====================================================

    for idx, i in enumerate(
        sorted_tasks,
        start=2
    ):

        fill = (
            odd_fill
            if idx % 2 == 0
            else even_fill
        )

        row_data = [
            idx - 1,
            i.dev_team or "-",
            i.id or "-",
            i.project_name or "-",
            i.subject or "-",
            i.cb or "-",
            i.current_status or "-",
            i.et or 0,
            i.rt or 0,
            round(float(i.at or 0), 2),
            round(float(i.at_taken or 0), 2),
            i.priority or "-",
            i.remark or "-",
            i.et_vs_at_remark or "-",
            i.remarks or "-"
        ]

        for col_num, value in enumerate(
            row_data,
            main_start_col
        ):

            cell = ws.cell(
                row=idx,
                column=col_num,
                value=value
            )

            cell.fill = fill
            cell.border = border
            cell.font = normal_font

            actual_col = col_num - main_start_col + 1

            if actual_col in [
                2,3,4,5,7,12,13,14,15
            ]:
                cell.alignment = left_align
            else:
                cell.alignment = center_align

    # =====================================================
    # Summary Widths
    # =====================================================

    summary_widths = {
        1: 12,
        2: 10,
        3: 10,
        4: 10,
        5: 15
    }

    for col_num, width in summary_widths.items():

        ws.column_dimensions[
            get_column_letter(col_num)
        ].width = width

    # =====================================================
    # Main Widths
    # =====================================================

    widths = {
        1: 10,
        2: 18,
        3: 15,
        4: 25,
        5: 40,
        6: 10,
        7: 20,
        8: 10,
        9: 10,
        10: 12,
        11: 12,
        12: 15,
        13: 35,
        14: 35,
        15: 35
    }

    for col_num, width in widths.items():

        actual_col = col_num + 7

        ws.column_dimensions[
            get_column_letter(actual_col)
        ].width = width

    # =====================================================
    # Row Height
    # =====================================================

    for row in ws.iter_rows():

        ws.row_dimensions[
            row[0].row
        ].height = 30

    # =====================================================
    # Freeze
    # =====================================================

    ws.freeze_panes = "H2"

    # =====================================================
    # Download
    # =====================================================

    output = io.BytesIO()

    wb.save(output)

    frappe.response.filename = (
        f"DSR_Report_{date}.xlsx"
    )

    frappe.response.filecontent = (
        output.getvalue()
    )

    frappe.response.type = "binary"





from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from io import BytesIO
import frappe
from datetime import datetime

@frappe.whitelist()
def download(customer=None, project=None, projects=None):

    import json

    if projects:
        projects = json.loads(projects)

    filename = "PR:02 – Project Status Report –(PSR - R)"
    build_xlsx_response(filename, customer, project, projects)

def build_xlsx_response(filename, customer, project, projects=None):
    xlsx_file = make_xlsx(customer, project, projects)
    frappe.response['filename'] = f"{filename}.xlsx"
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'

def make_xlsx(customer=None, project=None, projects=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "IT-SW Project Status Report"

    headers = [
        "Project Name","Project Type", "Account Manager","Account Manager Remark", "Project Manager", "Project Manager Remark","SPOC", "SPOC Remark",
        "# Task", "# Open", "# Working","# CRD","# PR", "# CR","#Issue Open","#Issue Replied", "SO Value", "Pending Billing"
    ]

    header_font = Font(bold=True, color="FFFFFF")
    sub_header_font = Font(bold=True, color="000000")
    
    header_fill = PatternFill(start_color="000080", end_color="000080", fill_type="solid")  # Dark Blue
    sub_header_fill = PatternFill(start_color="00BFFF", end_color="00BFFF", fill_type="solid")  # Sky Blue
    alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    column_widths = [30,20, 30,40, 30,40,30, 40, 10, 10, 10, 10, 10,10,10,10, 15, 20]

    
    current_date = datetime.today().strftime("%d-%m-%Y")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    title_cell = ws.cell(row=1, column=1, value=f"IT - SW Project Status Report (As on {current_date})")
    title_cell.font = header_font
    title_cell.fill = header_fill
    title_cell.alignment = alignment
    title_cell.border = thin_border

    
    for col_num, (header, width) in enumerate(zip(headers, column_widths), 1):
        cell = ws.cell(row=2, column=col_num, value=header)
        cell.font = sub_header_font
        cell.fill = sub_header_fill
        cell.alignment = alignment
        cell.border = thin_border
        ws.column_dimensions[get_column_letter(col_num)].width = width  

    
    
    
    
    project_types =frappe.db.get_all('Project Type',{'sequence_number':['!=',0]},['name'],order_by='sequence_number')
    for project_type in project_types:
        filters = {"docstatus": ("!=", "2"), "service": "IT-SW"}
        filters_1 = {"status": ("not in", ["Hold", "Completed", "Cancelled"]), "service": "IT-SW",'project_type':project_type.name}
        if customer and not project:
            filters["customer"] = customer  
        elif projects:
            filters_1["name"] = ["in", projects] 
        elif project and not customer:
            filters_1["name"] = project
        elif customer and project:
            filters["customer"] = customer
            filters["name"] = project  
        report = frappe.db.get_all(
            "Project",
            filters=filters_1,
            fields=["name", "project_name", "account_manager_remark", "remark", "custom_spoc_remark","status","spoc","project_manager","account_manager"],
            order_by='name'
        )

        row = 3  
        for i in report:
            task_count = frappe.db.count(
                "Task",
                filters={"project": i.name, "status": "Client Review", "service": "IT-SW"}
            )
            overall = frappe.db.count("Task", filters={"project":i.name, "status":("!=", "Cancelled"), "service":"IT-SW"})
            task_open=frappe.db.count("Task",filters={"project":i.name,"status":"Open","service":"IT-SW"})
            task_working=frappe.db.count("Task",filters={"project":i.name,"status":"Working","service":"IT-SW"})
            task_pr=frappe.db.count("Task",filters={"project":i.name,"status":"Pending Review","service":"IT-SW"})
            task_review=frappe.db.count("Task",filters={"project":i.name,"status":"Code Review","service":"IT-SW"})
            issue_open=frappe.db.count("Issue",filters={"project":i.name,"status":"Open"})
            issue_replied=frappe.db.count("Issue",filters={"project":i.name,"status":"Replied"})
            so_value = frappe.db.sql("""
                SELECT SUM(base_grand_total) 
                FROM `tabSales Order`
                WHERE project = %s AND docstatus != 2
            """, (i.name,))[0][0] or 0.0  

            sales_order = frappe.db.sql("""
                SELECT 
                    s.base_grand_total AS base_grand_total,
                    s.per_billed AS per_billed,
                    s.advance_paid AS advance_paid
                FROM 
                    `tabSales Order` s
                WHERE 
                    s.status NOT IN ('To Deliver', 'On Hold', 'Closed', 'Cancelled', 'Completed') 
                    AND s.project=%s
            """, (i.name,), as_dict=True)

            if sales_order:
                base_grand_total = sales_order[0].get("base_grand_total", 0.0)  
                per_billed = sales_order[0].get("per_billed", 0.0) or 0  
                advance_paid = sales_order[0].get("advance_paid", 0.0) or 0  

                amount_billed = (base_grand_total * per_billed) / 100  
                pending_billing = base_grand_total - (amount_billed + advance_paid)  
            else:
                base_grand_total = 0.0
                pending_billing = 0.0

            ws.append([
                i.project_name,project_type.name,i.account_manager, i.remark,i.project_manager, i.account_manager_remark, i.spoc, i.custom_spoc_remark,
                overall, task_open, task_working,task_review,task_pr, task_count, issue_open,issue_replied,
                f"₹ {so_value:,.0f}", f"₹ {pending_billing:,.0f}"
            ])

        
            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=ws.max_row, column=col)
                
                cell.border = thin_border
                if col in (1, 2, 3, 4,5, 6,7,8):
                    cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
                elif col in (17, 18):
                    cell.alignment = Alignment(horizontal='right', vertical='center', wrap_text=True)
                else:
                    cell.alignment = alignment

            row += 1

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file


