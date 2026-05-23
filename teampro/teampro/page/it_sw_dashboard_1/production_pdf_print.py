import frappe
from frappe.utils import getdate, nowdate
from datetime import datetime
from collections import defaultdict
from html import escape

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
					'custom_dev_team': team
				}, ['user_id'])
				if team_tl:
					allocated_persons.append(team_tl)
					cdr_employees = frappe.db.get_all(
						'Employee', 
						{'custom_is_tl': 0, 'custom_tl': emp_name}, 
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
		
	
		
	grouped = defaultdict(lambda: defaultdict(lambda: {"tasks": [], "is_tl": 0}))

	for row in data:
		team = row[12] or "No Team"
		cb = row[3] or "No CB"
		is_tl = row[16] or 0
		grouped[team][cb]["tasks"].append(row)
		grouped[team][cb]["is_tl"] = is_tl

	sorted_teams = sorted(grouped.keys())

	html = '''
	
	<table id="task-report-table" style="width: 100%; border-collapse: collapse;" border="1">
		<thead>
			<tr>
				<th style="background-color:#0F1568;color:black;">Sl No</th>
				<th style="background-color:#0F1568;color:black;">Sprint</th>
				<th style="background-color:#0F1568;color:black;">Team</th>
				<th style="background-color:#0F1568;color:black;">Project</th>
				<th style="background-color:#0F1568;color:black;">Task</th>
				<th style="background-color:#0F1568;color:black;">Subject</th>
				<th style="background-color:#0F1568;color:black;">KT Confirmed</th>
				<th style="background-color:#0F1568;color:black;">ET</th>
				<th style="background-color:#0F1568;color:black;">RT</th>
				<th style="background-color:#0F1568;color:black;">AT</th>
				<th style="background-color:#0F1568;color:black;">Today RT</th>
				<th style="background-color:#0F1568;color:black;">AT Period</th>
				<th style="background-color:#0F1568;color:black;">Priority</th>
				<th style="background-color:#0F1568;color:black;">Status</th>
			</tr>
		</thead>

	<tbody>
	'''

	task_serial = 1
	for team in sorted_teams:
		team_id = f"team-{team.replace(' ', '_')}"
		cb_groups = grouped[team]

		sorted_cbs = sorted(cb_groups.items(), key=lambda x: (-x[1]["is_tl"], x[0]))

		team_et = team_rt = team_at = team_at_period = team_task_count = team_today_rt = 0
		for cb, cb_data in sorted_cbs:
			for row in cb_data["tasks"]:
				team_et += float(row[5] or 0)
				team_rt += float(row[6] or 0)
				team_at += float(row[7] or 0)
				team_at_period += float(row[13] or 0)
				team_today_rt += float(row[14] or 0)
				team_task_count += 1

		cb_buttons = f'<td colspan="6" class="left-align"><span data-team="{team_id}" data-type="all" style="cursor:pointer; font-weight:bold; margin-right:10px;">+ ALL</span>'
		for cb in cb_groups.keys():
			cb_id = f"cb-{team.replace(' ', '_')}-{cb.replace(' ', '_')}"
			cb_buttons += f'<span data-target="{cb_id}" style="cursor:pointer; font-weight:bold; margin-right:10px;">+ {cb}</span>'
		cb_buttons += '</td>'

		html += f'''
		<tr class="toggle-team">
			<td colspan="1" class="left-align"><b>{escape(team)}</b></td>
			{cb_buttons}
			<td><b>{team_et:.2f}</b></td>
			<td><b>{team_rt:.2f}</b></td>
			<td><b>{team_at:.2f}</b></td>
			<td><b>{team_today_rt:.2f}</b></td>
			<td><b>{team_at_period:.2f}</b></td>
			<td colspan="2"></td>
		</tr>
		'''

		# for cb, cb_data in sorted_cbs:
		# 	tasks = cb_data["tasks"]
		# 	cb_id = f"cb-{team.replace(' ', '_')}-{cb.replace(' ', '_')}"

		# 	cb_et = cb_rt = cb_at = cb_today_at = cb_today_rt = 0
		# 	for row in tasks:
		# 		cb_et += float(row[5] or 0)
		# 		cb_rt += float(row[6] or 0)
		# 		cb_at += float(row[7] or 0)
		# 		cb_today_rt += float(row[14] or 0)
		# 		cb_today_at += float(row[13] or 0)

		# 	html += f'''
		# 	<tr class="toggle-cb {cb_id} {team_id}" style="display:none;">
		# 		<td><span class="toggle-icon">+</span></td>
		# 		<td colspan="6" class="left-align"><b>{escape(cb)}</b></td>
		# 		<td><b>{cb_et:.2f}</b></td>
		# 		<td><b>{cb_rt:.2f}</b></td>
		# 		<td><b>{cb_at:.2f}</b></td>
		# 		<td><b>{cb_today_rt:.2f}</b></td>
		# 		<td><b>{cb_today_at:.2f}</b></td>
		# 		<td colspan="2"></td>
		# 	</tr>
		# 	'''

		# 	for row in tasks:
		# 		html += f'''
		# 		<tr class="task-row {cb_id} {team_id}" style="display:none;">
		# 			<td>{task_serial}</td>
		# 			<td>{row[15]}</td>
		# 			<td>{row[12]}</td>
		# 			<td class="left-align">{escape(row[1])}</td>
		# 			<td><a href="/app/task/{row[0]}" target="_blank">{row[0]}</a></td>
		# 			<td class="left-align">{escape(row[2])}</td>
		# 			<td>{row[17]}</td>
		# 			<td>{row[5]}</td>
		# 			<td>{row[6]}</td>
		# 			<td>{row[7]}</td>
		# 			<td>{row[14]}</td>
		# 			<td style="color:red;">{row[13]}</td>
		# 			<td class="left-align">{row[8]}</td>
		# 			<td class="left-align">{row[10]}</td>
		# 		</tr>
		# 		'''
		# 		task_serial += 1
		for cb, cb_data in sorted_cbs:
			tasks = cb_data["tasks"]
			cb_id = f"cb-{team.replace(' ', '_')}-{cb.replace(' ', '_')}"

			cb_et = cb_rt = cb_at = cb_today_at = cb_today_rt = 0
			for row in tasks:
				cb_et += float(row[5] or 0)
				cb_rt += float(row[6] or 0)
				cb_at += float(row[7] or 0)
				cb_today_rt += float(row[14] or 0)
				cb_today_at += float(row[13] or 0)

			html += f'''
			<tr class="toggle-cb {cb_id} {team_id}">
				<td></td>
				<td colspan="6" class="left-align"><b>{escape(cb)}</b></td>
				<td><b>{cb_et:.2f}</b></td>
				<td><b>{cb_rt:.2f}</b></td>
				<td><b>{cb_at:.2f}</b></td>
				<td><b>{cb_today_rt:.2f}</b></td>
				<td><b>{cb_today_at:.2f}</b></td>
				<td colspan="2"></td>
			</tr>
			'''

			for row in tasks:
				html += f'''
				<tr class="task-row {cb_id} {team_id}">
					<td>{task_serial}</td>
					<td>{row[15]}</td>
					<td>{row[12]}</td>
					<td class="left-align">{escape(row[1])}</td>
					<td><a href="/app/task/{row[0]}" target="_blank">{row[0]}</a></td>
					<td class="left-align">{escape(row[2])}</td>
					<td>{row[17]}</td>
					<td>{row[5]}</td>
					<td>{row[6]}</td>
					<td>{row[7]}</td>
					<td>{row[14]}</td>
					<td style="color:red;">{row[13]}</td>
					<td class="left-align">{row[8]}</td>
					<td class="left-align">{row[10]}</td>
				</tr>
				'''
				task_serial += 1


	html += '</tbody></table>'
	# print(html)
	return html