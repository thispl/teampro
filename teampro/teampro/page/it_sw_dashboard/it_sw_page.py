import frappe
from frappe.utils.data import date_diff, today
from collections import defaultdict
from teampro.teampro.doctype.psr_report_dashboard.psr_report_dashboard import get_data
from teampro.teampro.doctype.psr_report_dashboard.psr_report_dashboard import make_html_report
from teampro.teampro.doctype.psr_report_dashboard.psr_report_dashboard import get_data_with_hour
from teampro.teampro.doctype.psr_report_dashboard.psr_report_dashboard import make_html_report_with_hour

@frappe.whitelist()
def it_data_summary(sprint=None):
	data = ""

	# number cards
	project_live = frappe.db.count('Project', {'service': 'IT-SW', 'status': 'Open', 'project_type': ['!=', 'AMC']})
	project_amc = frappe.db.count('Project', {'service': 'IT-SW', 'status': 'Open', 'project_type': 'AMC'})
	task_count = frappe.db.count('Task', {'service': 'IT-SW', 'status': ['in', ['Open', 'Working', 'Code Review']], 'custom_sprint': sprint})

	style = """
		<style>
			.number-card {
				flex: 1;
				background: linear-gradient(135deg, #f9f9f9, #fff);
				padding: 20px;
				border-radius: 16px;
				text-align: center;
				box-shadow: 0 4px 12px rgba(0,0,0,0.05);
				transition: transform 0.3s ease, box-shadow 0.3s ease;
				cursor: pointer;
			}
			.number-card:hover {
				transform: translateY(-8px) scale(1.02);
				box-shadow: 0 12px 24px rgba(0,0,0,0.15);
			}
			.number-card-title {
				margin: 0;
				font-weight: 600;
				font-size: 16px;
				color: #333;
			}
			.number-card-count {
				font-size: 32px;
				font-weight: 700;
				color: #0b0e30;
				margin-top: 12px;
			}
			/* --- Table Wrapper Styling --- */
			.table {
				width: 100%;
				border-collapse: collapse;
			}

			.table th {
				background: #0b0e30;
				color: #fff;
			}

			.table td, .table th {
				padding: 10px;
				border: 1px solid #ddd;
				transition: background 0.3s ease;
			}

			.table tbody tr:hover {
				background-color: #f1f1f1;
				cursor: pointer;
				transition: background 0.3s ease;
			}
		</style>
		"""


	number_cards_html = f"""
	{style}
	<div class="table-wrapper" style="display: flex; gap: 20px; justify-content: space-around; margin-top: 20px;">
		<div class="number-card"><div class="number-card-title">Live Projects</div><div class="number-card-count">{project_live}</div></div>
		<div class="number-card"><div class="number-card-title">AMC Projects</div><div class="number-card-count">{project_amc}</div></div>
		<div class="number-card"><div class="number-card-title">Tasks</div><div class="number-card-count">{task_count}</div></div>
	</div><br>
	"""

	# tasks + issues in current sprint
	tasks = frappe.db.get_all(
		'Task',
		{'service': 'IT-SW', 'status': ['in', ['Open', 'Working', 'Code Review']], 'custom_sprint': sprint},
		['name', 'subject', 'project', 'creation', 'status']
	)
	issues = frappe.db.get_all(
		'Issue',
		{'status': ['in', ['Open', 'Working', 'Code Review']], 'task': '', 'custom_sprint': sprint},
		['name', 'subject', 'project', 'creation', 'custom_issue_status']
	)

	if tasks or issues:
		table_html = """
		<h3>Task and Issue List</h3>
		<style>
		
		#task_table thead th {
			background-color: #0b0e30;
			color: white;
		}
		</style>
		<table id="task_table" class="table table-bordered" style="width:100%; border-collapse: collapse; border: 1px solid black; margin-top: 30px;">
		<thead>
			<tr>
			<th>Sr No</th><th>ID</th><th>Type</th><th>Subject</th><th>Project</th><th>Created On</th><th>Status</th><th>Age</th>
			</tr>
		</thead>
		<tbody>
		"""

		sr = 1
		for t in tasks:
			creation = t.creation.date()
			age = date_diff(today(), creation)
			table_html += f"""
			<tr>
			<td>{sr}</td>
			<td onclick="window.open('/app/task/{t.name}', '_blank')">{t.name}</td>
			<td>Task</td>
			<td>{t.subject}</td>
			<td>{t.project}</td>
			<td>{creation}</td>
			<td>{t.status}</td>
			<td>{age}</td>
			</tr>"""
			sr += 1

		for i in issues:
			creation = i.creation.date()
			age = date_diff(today(), creation)
			table_html += f"""
			<tr>
			<td>{sr}</td>
			<td onclick="window.open('/app/issue/{i.name}', '_blank')">{i.name}</td>
			<td>Issue</td>
			<td>{i.subject}</td>
			<td>{i.project}</td>
			<td>{creation}</td>
			<td>{i.custom_issue_status}</td>
			<td>{age}</td>
			</tr>"""
			sr += 1


		table_html += "</tbody></table>"
	else:
		table_html = ''

	# sprinted tasks
	task_data_s = frappe.db.get_all('Task',
		filters={'service': 'IT-SW', 'status': ['in', ['Open', 'Working', 'Code Review']], 'custom_sprint': sprint},
		fields=['project', 'custom_allocated_to', 'rt'],
		order_by='custom_allocated_to asc')

	grouped_rt = defaultdict(float)
	for task in task_data_s:
		grouped_rt[(task.get('project') or '-', task.get('custom_allocated_to') or '-')] += task.get('rt') or 0

	sorted_data = sorted(grouped_rt.items(), key=lambda x: x[0][1].lower() if x[0][1] else '')
	if sorted_data:
		table2 = """<h3>Sprinted Tasks</h3><div class="table-wrapper"><table id="sprinted_table" class="table table-bordered" style="width:100%; border-collapse: collapse; border: 1px solid black;">
			<thead><tr style="background-color: #0b0e30; color: white;"><th>Sr No</th><th>Project</th><th>Team</th><th>CB</th><th>RT</th></tr></thead><tbody>"""

		total_rt = 0
		
		for i, ((project, person), rt_sum) in enumerate(sorted_data, 1):
			total_rt += rt_sum
			emp = frappe.db.get_value('Employee', {'user_id': person}, ['custom_dev_team', 'short_code'], as_dict=True) or {}
			table2 += f"""<tr><td>{i}</td><td>{project}</td><td>{emp.get('custom_dev_team', '-')}</td><td>{emp.get('short_code', '-')}</td><td style="text-align:right;">{round(rt_sum, 2)}</td></tr>"""
	else:
		table2 =''
	table2 += f"""</tbody></table></div>"""
	# non sprinted task
	ns_tasks = frappe.db.sql("""
		SELECT project, SUM(rt) AS rt,COUNT(name) AS count
		FROM `tabTask`
		WHERE service = 'IT-SW' AND status = 'Open' AND project != '' 'Open' AND (custom_sprint IS NULL OR custom_sprint = '')
		GROUP BY project
	""", as_dict=True)
	if ns_tasks:

		table3 = """<h3>Non Sprinted Tasks</h3><div class="table-wrapper"><table id="non_sprinted_table" class="table table-bordered" style="width:100%; border-collapse: collapse; border: 1px solid black;">
			<thead><tr style="background-color: #0b0e30; color: white;"><th>Sr No</th><th>Project</th><th>RT</th><th>Count</th></tr></thead><tbody>"""
		non_total = 0
		for i, row in enumerate(ns_tasks, 1):
			non_total += row.rt or 0
			table3 += f"""<tr><td>{i}</td><td>{row.project}</td><td style="text-align:right;">{round(row.rt, 2)}</td><td style="text-align:right;">{row.count}</td></tr>"""

		table3 += f"""</tbody></table></div>"""
	else:
		table3 =''

	# merge sprinted and non sprinted in single div tag
	if sorted_data and ns_tasks:
		tables_2_and_3 = f"""
		<div class="table-wrapper">
		<div style="display: flex; gap: 20px; margin-top: 20px;">
			<div style="flex: 1; width: 50%;">{table2}</div>
			<div style="flex: 1; width: 50%;">{table3}</div>
		</div>
		</div>
		"""
	elif sorted_data:
		tables_2_and_3 = f"""
		<div class="table-wrapper" style='width:100%'>{table2}</div>
		"""
	elif ns_tasks:
		tables_2_and_3 = f"""
		<div class="table-wrapper" style='width:100%'>{table3}</div>
		"""
	else:
		tables_2_and_3 = ''

	# Sprint tasks split up

	table4 = ""
	current_sprint = frappe.db.get_all('Sprint', {'sprint_id': sprint, 'workflow_state': ('!=','Cancelled')}, ['name'])
	count=0
	for c in current_sprint:
		count+=1
		s_doc = frappe.get_doc('Sprint', c.name)
		unique_id = f"sprint_task_breakdown_table_{count}"
		table4 += f"""<h3>{s_doc.team}-{s_doc.sprint_id}</h3>
		<div class="table-wrapper"><table id="{unique_id}" class="table table-bordered" style="width:100%; border-collapse: collapse; border: 1px solid black;">
			<thead><tr style="background-color: #0b0e30; color: white;">
				<th>Sr No</th><th>ID</th><th>Subject</th><th>Project</th><th>CB</th><th>Status</th><th>ET</th><th>AT</th><th>RT</th><th>AT Period</th><th>Spot</th>
			</tr></thead><tbody>
		"""

		sr = 1
		for st in s_doc.sprint_task:
			emp = frappe.db.get_value('Employee', {'short_code': st.cb}, 'name')
			if frappe.db.exists('Task', {'name': st.task}):
				sub = frappe.db.get_value('Task', st.task, 'subject')
				et = frappe.db.get_value('Task', st.task, 'expected_time') or 0
				at = frappe.db.get_value('Task', st.task, 'actual_time') or 0
				rt = frappe.db.get_value('Task', st.task, 'rt') or 0
				spot = frappe.db.get_value('Task', st.task, 'custom_spot_task') or 0
				at_p = frappe.db.sql("""SELECT SUM(tsd.hours) FROM `tabTimesheet Detail` tsd JOIN `tabTimesheet` ts ON ts.name = tsd.parent WHERE ts.employee = %s AND ts.start_date BETWEEN %s AND %s AND tsd.task = %s""", (emp, s_doc.from_date, s_doc.to_date, st.task))[0][0] or 0
				status = frappe.db.get_value('Task', st.task, 'status')
				table4 += f"""<tr><td>{sr}</td><td onclick="window.open('/app/task/{st.task}', '_blank')">{st.task}</td><td>{sub}</td><td>{st.project}</td><td>{st.cb}</td><td>{status}</td><td>{round(et,2)}</td><td>{round(at,2)}</td><td>{round(rt,2)}</td><td>{round(at_p,2)}</td><td>{spot}</td></tr>"""
			elif frappe.db.exists('Issue', {'name': st.task}):
				sub = frappe.db.get_value('Issue', st.task, 'subject')
				et, rt, spot = 0.5, 0.5, 1
				at = frappe.db.sql("""SELECT SUM(tsd.hours) FROM `tabTimesheet Detail` tsd JOIN `tabTimesheet` ts ON ts.name = tsd.parent WHERE ts.employee = %s AND tsd.custom_issue = %s""", (emp, st.task))[0][0] or 0
				at_p = at
				status = frappe.db.get_value('Issue', st.task, 'custom_issue_status')
				table4 += f"""<tr><td>{sr}</td><td onclick="window.open('/app/issue/{st.task}', '_blank')">{st.task}</td><td>{sub}</td><td>{st.project}</td><td>{st.cb}</td><td>{status}</td><td>{round(et,2)}</td><td>{round(at,2)}</td><td>{round(rt,2)}</td><td>{round(at_p,2)}</td><td>{spot}</td></tr>"""
			else:
				sub, et, at, rt, spot, at_p, status = '-', 0, 0, 0, 0, 0, '-'
				table4 += f"""<tr><td>{sr}</td><td>{st.task}</td><td>{sub}</td><td>{st.project}</td><td>{st.cb}</td><td>{status}</td><td>{round(et,2)}</td><td>{round(at,2)}</td><td>{round(rt,2)}</td><td>{round(at_p,2)}</td><td>{spot}</td></tr>"""
			
			sr += 1

		table4 += "</tbody></table></div>"
	# --- Table 5: Reopen Tasks ---
	revision = frappe.db.get_all('Task', {'custom_sprint': sprint, 'revisions': ('>', 0)}, ['name', 'revisions', 'project', 'subject', 'custom_cause_of_reopen', 'custom_allocated_to'])
	table5 = ""
	if revision:
		table5 = """<h3>Revision Details</h3><div class="table-wrapper"><table id="reopen_tasks_table" class="table table-bordered" style="width:100%; border-collapse: collapse; border: 1px solid black;">
			<thead><tr style="background-color: #0b0e30; color: white;"><th>Sr No</th><th>ID</th><th>Subject</th><th>Project</th><th>CB</th><th>Count</th><th>Reason</th></tr></thead><tbody>"""
		for sr, rev in enumerate(revision, 1):
			cb = frappe.db.get_value('Employee', {'user_id': rev.custom_allocated_to}, 'short_code') or '-'
			table5 += f"""<tr><td>{sr}</td><td onclick="window.open('/app/task/{rev.name}', '_blank')">{rev.name}</td><td>{rev.subject}</td><td>{rev.project}</td><td>{cb}</td><td>{rev.revisions}</td><td>{rev.custom_cause_of_reopen}</td></tr>"""
		table5 += "</tbody></table></div>"

	# --- Table 6: Issue Linked ---
	issue_linked = frappe.db.get_all('Task', {'custom_sprint': sprint, 'issue': ('!=', '')}, ['name', 'issue', 'project', 'subject', 'custom_issue_type', 'custom_allocated_to'])
	table6 = ""
	if issue_linked:
		table6 = """<h3>Issue Analysis</h3><div class="table-wrapper"><table id="issue_analysis_table" class="table table-bordered" style="width:100%; border-collapse: collapse; border: 1px solid black;">
			<thead><tr style="background-color: #0b0e30; color: white;"><th>Sr No</th><th>ID</th><th>Subject</th><th>CB</th><th>Project</th><th>Issue</th><th>Type</th></tr></thead><tbody>"""
		for sr, iss in enumerate(issue_linked, 1):
			cb = frappe.db.get_value('Employee', {'user_id': iss.custom_allocated_to}, 'short_code') or '-'
			table6 += f"""<tr><td>{sr}</td><td onclick="window.open('/app/task/{iss.name}', '_blank')">{iss.name}</td><td>{iss.subject}</td><td>{cb}</td><td>{iss.project}</td><td onclick="window.open('/app/issue/{iss.issue}', '_blank')">{iss.issue}</td><td>{iss.custom_issue_type}</td></tr>"""
		table6 += "</tbody></table></div>"
	# PSR Count Report
	psr_count = get_data()
	title = 'Daily PSR Report-Count'
	data_1 = make_html_report(title, psr_count)

	psr_hour = get_data_with_hour()
	title = 'Daily PSR Report-Hour'
	data_2 = make_html_report_with_hour(title, psr_hour)
	data = number_cards_html +data_1 +data_2+ table_html +tables_2_and_3 + table4 + table6 + table5 
	return data