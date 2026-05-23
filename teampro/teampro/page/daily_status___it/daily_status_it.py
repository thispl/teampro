import frappe
from frappe.utils import getdate, nowdate
from datetime import datetime

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



@frappe.whitelist()
def get_task_summary():
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
		"open_total_hours": 0,
		"working_total_hours": 0,
		"pr_total_hours": 0,
		"cr_total_hours": 0,
	}

	# Get total count and hours
	total_data = frappe.db.sql("""
		SELECT COUNT(*) AS count, SUM(rt) AS total_hours
		FROM `tabTask`
		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
		AND service = 'IT-SW'
	""", as_dict=True)[0]

	summary["total"] = total_data.count or 0
	summary["total_total_hours"] = total_data.total_hours or 0

	# Fetch grouped data in one go
	grouped_data = frappe.db.sql("""
		SELECT status, COUNT(*) AS count, SUM(rt) AS total_hours
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
		team_logo = frappe.db.get_value("Dev Team", task.custom_dev_team, "logo") or ""
		emp = frappe.get_value("Employee", {"user_id": task.custom_allocated_to}, ["short_code", "name" , 'image'], as_dict=True)
		short_code = emp.short_code if emp else ""
		emp_name = emp.name if emp else ""
		emp_image = emp.image if emp and emp.image else ""
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

			# data.append([
			# 	row.custom_issue, row.project, row.custom_subject_issue, short_code, "Working",
			# 	0, 0, 0, priority, 1,
			# 	current_status, '', dev_team,
			# 	round(today_at, 2), 0,custom_sprint or '',is_tl,0
			# ])

			data.append([
				task.name, task.project, task.subject, short_code, "Working",
				round(task.expected_time or 0, 2), round(task.rt or 0, 2),
				round(actual_time, 2), task.priority, spot_task,
				task.current_status, task.custom_remarks, task.custom_dev_team,
				round(today_at, 2), round(today_rt, 2), task.custom_sprint,
				is_tl, task.kt_confirmed,
				emp_image,      
				team_logo       
			])
		
	

	return data

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

@frappe.whitelist()
def get_tasks_project_pivot():
	status_group_map = {
		"Open": "open",
		"Working": "working",
		"Overdue": "working",
		"Code Review": "cdr",
		"Pending Review": "pr",
		"Client Review": "cr"
	}

	tasks = frappe.db.sql("""
		SELECT 
			t.project,
			p.project_type,
			t.status,
			t.rt
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

		if not group:
			continue

		if project not in pivot:
			pivot[project] = {
				"project": project,
				"project_type": project_type,
				"open": {"tasks": 0, "hours": 0.0},
				"working": {"tasks": 0, "hours": 0.0},
				"pr": {"tasks": 0, "hours": 0.0},
				"cr": {"tasks": 0, "hours": 0.0},
			}


		if group == "cdr":
			group = "working"

		pivot[project][group]["tasks"] += 1
		pivot[project][group]["hours"] += rt

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

	result = []
	for i, data in enumerate(sorted_items, start=1):
		def format_cell(value):
			return f"{value['hours']:.2f}/{value['tasks']}"

		row = {
			"s_no": i,
			"project": data["project"],
			"project_type": data["project_type"],
			"open": format_cell(data["open"]),
			"working": format_cell(data["working"]),
			"pr": format_cell(data["pr"]),
			"cr": format_cell(data["cr"])
		}
		result.append(row)

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
