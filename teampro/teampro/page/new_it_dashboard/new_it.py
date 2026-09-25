import frappe
from frappe.utils import getdate, nowdate, formatdate, add_days, flt
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
    dev_teams = frappe.db.get_all('Dev Team',{"team_name": ["!=", "Others"]},["team_name"],order_by='order_for_it_dashboard')
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
def get_dashboard_summary():
    # ---------------- PROJECT COUNTS ----------------
    total_filters = {
        "status": ["not in", ["Hold", "Completed", "Cancelled"]],
        "service": "IT-SW",
        "project_type": ["is", "set"]
    }
    project_total = frappe.db.count("Project", filters=total_filters)

    project_types = frappe.db.get_all(
        'Project Type',
        {'sequence_number': ['!=', 0]},
        ['name'],
        order_by='sequence_number'
    )

    projects = []
    for project_type in project_types:
        filters = {
            "status": ["not in", ["Hold", "Completed", "Cancelled"]],
            "service": "IT-SW",
            "project_type": project_type.name
        }
        count = frappe.db.count("Project", filters=filters)
        projects.append({
            "project_type": project_type.name,
            "count": count
        })

    # ---------------- TASK SUMMARY ----------------
    from frappe.utils import nowdate
    today = nowdate()

    status_map = {
        "Open": "open",
        "Working": "working",
        "Overdue": "working",
        "Code Review": "working",
        "Pending Review": "pr",
        "Client Review": "cr"
    }

    task_summary = {
        "total": 0, "open": 0, "working": 0, "pr": 0, "cr": 0,
        "total_total_hours": 0, "open_total_hours": 0, "working_total_hours": 0,
        "pr_total_hours": 0, "cr_total_hours": 0,
        "total_today_count": 0, "open_today_count": 0, "working_today_count": 0,
        "pr_today_count": 0, "cr_today_count": 0,
        "total_today_hours": 0, "open_today_hours": 0, "working_today_hours": 0,
        "pr_today_hours": 0, "cr_today_hours": 0,
    }

    total_data = frappe.db.sql("""
        SELECT COUNT(*) AS count, COALESCE(SUM(rt),0) AS total_hours
        FROM `tabTask`
        WHERE status NOT IN ('Completed', 'Cancelled','Hold')
        AND service = 'IT-SW'
    """, as_dict=True)[0]

    task_summary["total"] = total_data.count or 0
    task_summary["total_total_hours"] = float(total_data.total_hours or 0)

    today_total_data = frappe.db.sql("""
        SELECT COUNT(*) AS count, COALESCE(SUM(rt),0) AS total_hours
        FROM `tabTask`
        WHERE status NOT IN ('Completed', 'Cancelled','Hold')
        AND service = 'IT-SW'
        AND DATE(custom_production_date) = %s
    """, today, as_dict=True)[0]

    task_summary["total_today_count"] = today_total_data.count or 0
    task_summary["total_today_hours"] = float(today_total_data.total_hours or 0)

    grouped_data = frappe.db.sql("""
        SELECT status, COUNT(*) AS count, COALESCE(SUM(rt),0) AS total_hours
        FROM `tabTask`
        WHERE status NOT IN ('Completed', 'Cancelled','Hold')
        AND service = 'IT-SW'
        GROUP BY status
    """, as_dict=True)

    for row in grouped_data:
        key = status_map.get(row.status)
        if key:
            task_summary[key] += row.count or 0
            task_summary[f"{key}_total_hours"] += float(row.total_hours or 0)

    today_grouped_data = frappe.db.sql("""
        SELECT status, COUNT(*) AS count, COALESCE(SUM(rt),0) AS total_hours
        FROM `tabTask`
        WHERE status NOT IN ('Completed', 'Cancelled','Hold')
        AND service = 'IT-SW'
        AND DATE(custom_production_date) = %s
        GROUP BY status
    """, today, as_dict=True)

    for row in today_grouped_data:
        key = status_map.get(row.status)
        if key:
            task_summary[f"{key}_today_count"] += row.count or 0
            task_summary[f"{key}_today_hours"] += float(row.total_hours or 0)

    return {
        "project_total": project_total,
        "projects": projects,
        "tasks": task_summary
    }

@frappe.whitelist()
def get_tasks_project_wise(type=None):
    status_map = {
        "open": ["Open"],
        "working": ["Working", "Overdue", "Code Review"],
        "pr": ["Pending Review"],
        "cr": ["Client Review"]
    }

    # if type == "total":
    # 	return frappe.db.sql("""
    # 		SELECT project, COUNT(name) AS task_count, SUM(rt) AS total_hours
    # 		FROM `tabTask`
    # 		WHERE status NOT IN ('Completed', 'Cancelled','Hold')
    # 		AND service = 'IT-SW'
    # 		GROUP BY project
        # """, as_dict=True)

    # if type in status_map:
    # 	return frappe.db.sql("""
    # 		SELECT project, COUNT(name) AS task_count, SUM(rt) AS total_hours, spoc
    # 		FROM `tabTask`
    # 		WHERE status IN %(statuses)s
    # 		AND status NOT IN ('Completed', 'Cancelled','Hold')
    # 		AND service = 'IT-SW'
    # 		GROUP BY project
    # 	""", {"statuses": status_map[type]}, as_dict=True)

    if type == "total":
        return frappe.db.sql("""
            SELECT
                t.project,
                COUNT(t.name) AS task_count,
                SUM(t.rt) AS total_hours,
                p.spoc
            FROM `tabTask` t
            LEFT JOIN `tabProject` p
                ON p.name = t.project
            WHERE t.status NOT IN ('Completed', 'Cancelled', 'Hold')
                AND t.service = 'IT-SW'
            GROUP BY t.project, p.spoc
        """, as_dict=True)


    if type in status_map:
        return frappe.db.sql("""
            SELECT
                t.project,
                COUNT(t.name) AS task_count,
                SUM(t.rt) AS total_hours,
                p.spoc
            FROM `tabTask` t
            LEFT JOIN `tabProject` p
                ON p.name = t.project
            WHERE t.status IN %(statuses)s
                AND t.status NOT IN ('Completed', 'Cancelled', 'Hold')
                AND t.service = 'IT-SW'
            GROUP BY t.project, p.spoc
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
def get_today_task_data1(priority=None, sp=None, ro=None, from_date=None, to_date=None, team=None):

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

    if team:
        conditions += " AND m.dev_team = %s"
        values.append(team)

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
            "custom_order_for_it_dashboard": [">=", 0]
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
            "order_for_it_dashboard": [">=", 0],
            "name": ["!=", "Others"]
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
            c.rt,

            c.priority,
            c.spot_task,
            c.current_status,
            c.remark,

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
    # Timesheet Actual Time (submitted) and Today AT (all non-cancelled)
    # Optimized: filter Timesheet parents by start/end date first, then join
    # to Timesheet Detail. This avoids a full scan of the large child table.
    # ------------------------------
    relevant_parents = frappe.db.sql(
        """
        SELECT name
        FROM `tabTimesheet`
        WHERE docstatus != 2
        AND start_date <= %s
        AND end_date >= %s
        """,
        (to_date, from_date),
        as_list=True,
    )
    parent_names = [p[0] for p in relevant_parents]

    actual_map = {}
    today_at_map = {}

    if parent_names:
        timesheet_hours = frappe.db.sql(
            """
            SELECT
                d.task,
                t.employee,
                SUM(CASE WHEN t.docstatus = 1 THEN d.hours ELSE 0 END) as submitted_hours,
                SUM(CASE WHEN t.docstatus != 2 THEN
                    CASE
                        WHEN d.to_time IS NOT NULL THEN d.hours
                        ELSE TIMESTAMPDIFF(SECOND, d.from_time, NOW()) / 3600
                    END
                    ELSE 0 END) as total_hours
            FROM `tabTimesheet Detail` d
            JOIN `tabTimesheet` t ON d.parent = t.name
            WHERE d.parent IN %s
            AND d.from_time BETWEEN %s AND DATE_ADD(%s, INTERVAL 1 DAY)
            GROUP BY d.task, t.employee
            """,
            (tuple(parent_names), from_date, to_date),
            as_dict=True,
        )

        for a in timesheet_hours:
            key = (a.task, a.employee)
            actual_map[key] = a.submitted_hours or 0
            today_at_map[key] = a.total_hours or 0

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
        today_rt = task.rt or 0

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
            task.remark or "",

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
        filters={"custom_order_for_it_dashboard": [">=", 0]},
        order_by="custom_order_for_it_dashboard asc"
    )

    emp_map = {e.short_code: e for e in employees}

    # ------------------------------
    # Teams
    # ------------------------------
    teams = frappe.get_all(
        "Dev Team",
        filters={"order_for_it_dashboard": [">=", 0], "name": ["!=", "Others"]},
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
        AND m.service = 'IT-SW'
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
        fields=["name","cb", "kt_confirmed", "project", "custom_sprint", "subject", "expected_time", "actual_time", "priority", "status", "custom_allocated_to", "custom_production_date", "service",'custom_age', 'custom_production_date_count',"rt"]
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
    dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='order_for_it_dashboard')
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
        table_html = build_retro_table_for_sprint_hrs_col(sprint_name)

        all_tables.append({
            'team': team_name,
            'html': table_html
        })

    return all_tables



from frappe.utils import flt
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
        <td rowspan="2" style="background:#d9edf7;">APH</td>
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
    overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=tot_aph=0
    sr_no = 1
    for cb in cb_list:
        emp = frappe.db.get_value('Employee', {'short_code': cb}, ['name'])
        aph = frappe.db.get_value('Employee', {'short_code': cb , "department": "IT. Development - THIS" ,"status": "Active" }, ['custom_aph'])
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
          
        tot_aph += flt(aph)
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
            <td>{aph}</td>
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
        <td style="background:#020c59;color:white;">{tot_aph}</td>
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


from frappe.utils import flt
@frappe.whitelist()
def build_retro_table_for_sprint_hrs_col(name):
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
        <td rowspan="2" style="background:#d9edf7;">APH</td>
        <td class="hrs-col" colspan="4" style="background:#d9edf7;">Sprint (Hrs)</td>
        <td class="hrs-col" colspan="4" style="background:#fcf8e3;">Others (Hrs)</td>
        <td class="hrs-col" colspan="6" style="background:#f0b616;">Total (Hrs)</td>
        <td class="hrs-col" colspan="2" style="background:#f0b616;">Observation</td>
        <td class="count-col" colspan="4" style="background:#d9edf7;">Sprint (Count)</td>
        <td class="count-col" colspan="4" style="background:#fcf8e3;">Others (Count)</td>
        <td class="count-col" colspan="6" style="background:#f0b616;">Total (Count)</td>
        <td class="count-col" colspan="2" style="background:#f0b616;">Observation</td>
    </tr>
    <tr>
        <!-- Hrs Sprint -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Hrs Others -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Hrs Total -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Attd</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Used</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Observation Hrs -->
        <td class="hrs-col" style="background:#020c59;color:white;">NC</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Reopen</td>
        <!-- Count Sprint -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Count Others -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Count Total -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Attd</td>
        <td class="count-col" style="background:#020c59;color:white;">Used</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Observation Count -->
        <td class="count-col" style="background:#020c59;color:white;">NC</td>
        <td class="count-col" style="background:#020c59;color:white;">Reopen</td>
    </tr>

    """

    sub_total_rt = sub_tot_comp_rt = sub_tot_work_rt = sub_nt_rt = 0
    sub_total_s_rt = sub_tot_comp_srt = sub_tot_work_srt = sub_nt_srt = sub_bt_hours = 0
    sub_used_percent = sub_comp_per = sub_ncomp_per = tot_bt_hrs = tot_reopen_count = 0
    tot_c = tot_nc = tot_spr_chrs = tot_spr_whrs = tot_spot_chrs = tot_spot_whrs = tot_nc_rt = 0
    sub_total_count = sub_tot_comp_count =sub_tot_work_count =sub_nt_count =sub_total_s_count =0
    sub_tot_comp_scount = sub_tot_work_scount=sub_nt_scount=sub_total=overall_comp=0
    overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=tot_aph=0
    sr_no = 1
    for cb in cb_list:
        emp = frappe.db.get_value('Employee', {'short_code': cb}, ['name'])
        aph = frappe.db.get_value('Employee', {'short_code': cb , "department": "IT. Development - THIS" ,"status": "Active" }, ['custom_aph'])
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
          
        tot_aph += flt(aph)
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
            <td>{aph}</td>
            <td class="hrs-col">{total_rt}</td>
            <td class="hrs-col">{spr_comp_s}</td>
            <td class="hrs-col">{spr_ncomp_s}</td>
            <td class="hrs-col">{nt_rt}</td>
            <td class="hrs-col">{total_s_rt}</td>
            <td class="hrs-col">{spot_comp_s}</td>
            <td class="hrs-col">{spot_ncomp_s}</td>
            <td class="hrs-col">{nt_srt}</td>
            <td class="hrs-col">{total_rt + total_s_rt}</td>
            <td class="hrs-col">{bt_hours}</td>
            <td class="hrs-col" style="color: {att_color};">{used_percent_str}</td>
            <td class="hrs-col" style="color: {font_color};">{comp_percent_str}</td>
            <td class="hrs-col">{ncomp_percent_str}</td>
            <td class="hrs-col">{round(nt_rt + nt_srt, 2)}</td>
            <td class="hrs-col">{nc_rt}</td>
            <td class="hrs-col">{round(reopen_count, 2)}</td>
            <td class="count-col">{total_count}</td>
            <td class="count-col">{tot_comp_count}</td>
            <td class="count-col">{tot_work_count}</td>
            <td class="count-col">{nt_count}</td>
            <td class="count-col">{total_s_count}</td>
            <td class="count-col">{tot_comp_scount}</td>
            <td class="count-col">{tot_work_scount}</td>
            <td class="count-col">{nt_scount}</td>
            <td class="count-col">{total_count + total_s_count}</td>
            <td class="count-col">-</td>
            <td class="count-col">-</td>
            <td class="count-col">{tot_comp_count + tot_comp_scount}</td>
            <td class="count-col">{tot_work_count + tot_work_scount}</td>
            <td class="count-col">{nt_count + nt_scount}</td>
            <td class="count-col">{nc_count}</td>
            <td class="count-col">{reopen_count}</td>
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
        <td style="background:#020c59;color:white;">{tot_aph}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/<br>{round(tot_spr_chrs, 2)}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/<br>{round(tot_spr_whrs, 2)}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{sub_nt_rt}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{sub_total_s_rt}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/<br>{round(tot_spot_chrs, 2)}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/<br>{round(tot_spot_whrs, 2)}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{sub_nt_srt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{sub_total_rt + sub_total_s_rt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
        <td class="hrs-col" style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
        <td class="hrs-col" style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{sub_work_str}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">-</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">-</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_comp}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_work}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_nt}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
        
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
# 	from frappe.utils import today

# 	status_group_map = {
# 		"Open": "open",
# 		"Working": "working",
# 		"Overdue": "working",
# 		"Code Review": "cdr",
# 		"Pending Review": "pr",
# 		"Client Review": "cr"
# 	}

# 	today_date = today()

# 	# tasks = frappe.db.sql("""
# 	# 	SELECT 
# 	# 		t.project,
# 	# 		p.project_type,
# 	# 		t.status,
# 	# 		t.rt,
# 	# 		DATE(t.custom_production_date) as production_date
# 	# 	FROM `tabTask` t
# 	# 	LEFT JOIN `tabProject` p ON t.project = p.name
# 	# 	WHERE t.status NOT IN ('Completed', 'Cancelled', 'Hold') ,
# 	# 	AND t.service = 'IT-SW'
# 	# """, as_dict=True)

# 	tasks = frappe.db.sql("""
# 		SELECT
# 			p.name AS project,
# 			p.project_type,
# 			t.name AS task,
# 			t.status,
# 			IFNULL(t.rt,0) AS rt,
# 			DATE(t.custom_production_date) AS production_date
# 		FROM `tabProject` p
# 		LEFT JOIN `tabTask` t
# 			ON t.project = p.name
# 			AND t.status NOT IN ('Completed', 'Cancelled', 'Hold')
# 		WHERE p.status NOT IN ('Completed', 'Cancelled', 'Hold')
# 			AND p.service = 'IT-SW'
# 			AND IFNULL(p.project_type, '') != ''
# 		ORDER BY p.project_type, p.name
# 	""", as_dict=True)

# 	pivot = {}

# 	for task in tasks:

# 		project = task.project or "No Project"
# 		project_type = (task.project_type or "Unknown").strip()
# 		status = task.status or "Unknown"
# 		group = status_group_map.get(status)
# 		rt = task.rt or 0.0
# 		is_today = (str(task.production_date) == today_date)

# 		if not group:
# 			continue

# 		if project not in pivot:
# 			pivot[project] = {
# 				"project": project,
# 				"project_type": project_type,

# 				"open": {"tasks": 0, "hours": 0.0},
# 				"open_td": {"tasks": 0, "hours": 0.0},

# 				"working": {"tasks": 0, "hours": 0.0},
# 				"working_td": {"tasks": 0, "hours": 0.0},

# 				"pr": {"tasks": 0, "hours": 0.0},
# 				"pr_td": {"tasks": 0, "hours": 0.0},

# 				"cr": {"tasks": 0, "hours": 0.0},
# 				"cr_td": {"tasks": 0, "hours": 0.0},
# 			}

# 		if not task.task:
# 			continue

# 		# convert cdr → working
# 		if group == "cdr":
# 			group = "working"

# 		# =========================
# 		# TOTAL
# 		# =========================
# 		pivot[project][group]["tasks"] += 1
# 		pivot[project][group]["hours"] += rt

# 		# =========================
# 		# TODAY
# 		# =========================
# 		if is_today:
# 			pivot[project][f"{group}_td"]["tasks"] += 1
# 			pivot[project][f"{group}_td"]["hours"] += rt

# 	# sorting
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

# 	def fmt(v):
# 		return f"{v['hours']:.2f}/{v['tasks']}"

# 	result = []

# 	for i, data in enumerate(sorted_items, start=1):

# 		result.append({
# 			"s_no": i,
# 			"project": data["project"],
# 			"project_type": data["project_type"],

# 			"open": fmt(data["open"]),
# 			"open_td": fmt(data["open_td"]),

# 			"working": fmt(data["working"]),
# 			"working_td": fmt(data["working_td"]),

# 			"pr": fmt(data["pr"]),
# 			"pr_td": fmt(data["pr_td"]),

# 			"cr": fmt(data["cr"]),
# 			"cr_td": fmt(data["cr_td"])
# 		})

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
            p.name AS project,
            p.project_type,
            t.name AS task,
            t.status,
            IFNULL(t.rt, 0) AS rt,
            DATE(t.custom_production_date) AS production_date
        FROM `tabProject` p
        LEFT JOIN `tabTask` t
            ON t.project = p.name
            AND t.status NOT IN ('Completed', 'Cancelled', 'Hold')
        WHERE p.status NOT IN ('Completed', 'Cancelled', 'Hold')
            AND p.service = 'IT-SW'
            AND IFNULL(p.project_type, '') != ''
        ORDER BY p.project_type, p.name
    """, as_dict=True)

    pivot = {}

    for task in tasks:

        project = task.project or "No Project"
        project_type = (task.project_type or "Unknown").strip()

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

        if not task.task:
            continue

        status = task.status or "Unknown"
        group = status_group_map.get(status)

        if not group:
            continue

        if group == "cdr":
            group = "working"

        rt = task.rt or 0.0
        is_today = str(task.production_date) == today_date

        # Total
        pivot[project][group]["tasks"] += 1
        pivot[project][group]["hours"] += rt

        # Today
        if is_today:
            pivot[project][f"{group}_td"]["tasks"] += 1
            pivot[project][f"{group}_td"]["hours"] += rt

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
        dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='order_for_it_dashboard')

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

        
        table_html = build_retro_table_for_sprint_hrs_col(sprint_name)

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
    # Return the last/most recent sprint ID (default for filters)
    sprint_name = frappe.db.get_value(
        'Sprint',
        {'status': 'In Progress'},
        'sprint_id',
        order_by='creation desc'
    )
    return sprint_name


@frappe.whitelist()
def get_retro_summary_overall(name=None):
    dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='order_for_it_dashboard')

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

        table_html = build_retro_table_for_sprint_summary_hrs_cols(sprint_docname)
        
        
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
        <td rowspan="2" style="color:red;">APH</td>
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
        <td rowspan="2" style="color:red;">APH</td>
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
def build_retro_table_for_sprint_summary_hrs_cols(name):
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
        <td rowspan="2" style="color:red;">APH</td>
        <td class="hrs-col" colspan="4" style="background:#d9edf7;">Sprint (Hrs)</td>
        <td class="hrs-col" colspan="4" style="background:#fcf8e3;">Others (Hrs)</td>
        <td class="hrs-col" colspan="6" style="background:#f0b616;">Total (Hrs)</td>
        <td class="hrs-col" colspan="2" style="background:#f0b616;">Observation</td>
        <td class="count-col" colspan="4" style="background:#d9edf7;">Sprint (Count)</td>
        <td class="count-col" colspan="4" style="background:#fcf8e3;">Others (Count)</td>
        <td class="count-col" colspan="6" style="background:#f0b616;">Total (Count)</td>
        <td class="count-col" colspan="2" style="background:#f0b616;">Observation</td>
    </tr>
    <tr>
        <!-- Hrs Sprint -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Hrs Others -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Hrs Total -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Attd</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Used</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Observation Hrs -->
        <td class="hrs-col" style="background:#020c59;color:white;">NC</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Reopen</td>
        <!-- Count Sprint -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Count Others -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Count Total -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Attd</td>
        <td class="count-col" style="background:#020c59;color:white;">Used</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Observation Count -->
        <td class="count-col" style="background:#020c59;color:white;">NC</td>
        <td class="count-col" style="background:#020c59;color:white;">Reopen</td>
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
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/<br>{round(tot_spr_chrs, 2)}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/<br>{round(tot_spr_whrs, 2)}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{sub_nt_rt}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{sub_total_s_rt}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/<br>{round(tot_spot_chrs, 2)}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/<br>{round(tot_spot_whrs, 2)}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{sub_nt_srt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{sub_total_rt + sub_total_s_rt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
        <td class="hrs-col" style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
        <td class="hrs-col" style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{sub_work_str}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">-</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">-</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_comp}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_work}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_nt}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
        
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

    dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='order_for_it_dashboard')

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
        <td rowspan="2" style="color:red;">APH Summary</td>
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
    overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=tot_aph=team_aph=0
    sr_no = 1
    # print(dev_teams)
    # dev_teams =['ALPHA']
    for team_name in dev_teams:
        sprint_name = frappe.db.get_value('Sprint', {'sprint_id': previous_sprint_id,'team':team_name}, 'name')
        if sprint_name:
            sprint = frappe.get_doc('Sprint', sprint_name)
            # aph = frappe.db.get_value('Employee', {'custom_dev_team': team_name,'status':'Active','department':'IT. Development - THIS'}, ['custom_aph'])
            aph = frappe.db.sql("""
                SELECT IFNULL(SUM(custom_aph), 0)
                FROM `tabEmployee`
                WHERE custom_dev_team = %s
                AND status = 'Active'
                AND department = 'IT. Development - THIS'
            """, (team_name,))[0][0]


            team_list = frappe.db.get_all('Employee', {'custom_dev_team': team_name, 'status': 'Active','department':'IT. Development - THIS'}, pluck='short_code') or ['']
            emp_list = frappe.db.get_all('Employee', {'custom_dev_team': team_name, 'status':'Active','department':'IT. Development - THIS'}, pluck='name')
            # print(team_list)
            # print(sprint.name)
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
            tot_aph = flt(aph)
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
                <td>{tot_aph}</td>
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
            team_aph+=tot_aph
        
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
        <td style="background:#020c59;color:white;">{team_aph}</td>
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
def summary_total_hrs_cols(name):
    # dev_team =None
    # name ='SPRINT 21'
    all_tables = []

    dev_teams = frappe.get_all('Dev Team', filters={"team_name": ["!=", "Others"]}, pluck="team_name", order_by='order_for_it_dashboard')

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
        <td rowspan="2" style="color:red;">APH Summary</td>
        <td class="hrs-col" colspan="4" style="background:#d9edf7;">Sprint (Hrs)</td>
        <td class="hrs-col" colspan="4" style="background:#fcf8e3;">Others (Hrs)</td>
        <td class="hrs-col" colspan="6" style="background:#f0b616;">Total (Hrs)</td>
        <td class="hrs-col" colspan="2" style="background:#f0b616;">Observation</td>
        <td class="count-col" colspan="4" style="background:#d9edf7;">Sprint (Count)</td>
        <td class="count-col" colspan="4" style="background:#fcf8e3;">Others (Count)</td>
        <td class="count-col" colspan="6" style="background:#f0b616;">Total (Count)</td>
        <td class="count-col" colspan="2" style="background:#f0b616;">Observation</td>
    </tr>
    <tr>
        <!-- Hrs Sprint -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Hrs Others -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Hrs Total -->
        <td class="hrs-col" style="background:#020c59;color:white;">Plan</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Attd</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Used</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Comp</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Work</td>
        <td class="hrs-col" style="background:#020c59;color:white;">NT</td>
        <!-- Observation Hrs -->
        <td class="hrs-col" style="background:#020c59;color:white;">NC</td>
        <td class="hrs-col" style="background:#020c59;color:white;">Reopen</td>
        <!-- Count Sprint -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Count Others -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp.</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Count Total -->
        <td class="count-col" style="background:#020c59;color:white;">Plan</td>
        <td class="count-col" style="background:#020c59;color:white;">Attd</td>
        <td class="count-col" style="background:#020c59;color:white;">Used</td>
        <td class="count-col" style="background:#020c59;color:white;">Comp</td>
        <td class="count-col" style="background:#020c59;color:white;">Work</td>
        <td class="count-col" style="background:#020c59;color:white;">NT</td>
        <!-- Observation Count -->
        <td class="count-col" style="background:#020c59;color:white;">NC</td>
        <td class="count-col" style="background:#020c59;color:white;">Reopen</td>
    </tr>

    """

    sub_total_rt = sub_tot_comp_rt = sub_tot_work_rt = sub_nt_rt = 0
    sub_total_s_rt = sub_tot_comp_srt = sub_tot_work_srt = sub_nt_srt = sub_bt_hours = 0
    sub_used_percent = sub_comp_per = sub_ncomp_per = tot_bt_hrs = tot_reopen_count = 0
    tot_c = tot_nc = tot_spr_chrs = tot_spr_whrs = tot_spot_chrs = tot_spot_whrs = tot_nc_rt = 0
    sub_total_count = sub_tot_comp_count =sub_tot_work_count =sub_nt_count =sub_total_s_count =0
    sub_tot_comp_scount = sub_tot_work_scount=sub_nt_scount=sub_total=overall_comp=0
    overall_work=overall_nt=sub_total_reopen_count=tot_nc_count=tot_aph=team_aph=0
    sr_no = 1
    # print(dev_teams)
    # dev_teams =['ALPHA']
    for team_name in dev_teams:
        sprint_name = frappe.db.get_value('Sprint', {'sprint_id': previous_sprint_id,'team':team_name}, 'name')
        if sprint_name:
            sprint = frappe.get_doc('Sprint', sprint_name)
            # aph = frappe.db.get_value('Employee', {'custom_dev_team': team_name,'status':'Active','department':'IT. Development - THIS'}, ['custom_aph'])
            aph = frappe.db.sql("""
                SELECT IFNULL(SUM(custom_aph), 0)
                FROM `tabEmployee`
                WHERE custom_dev_team = %s
                AND status = 'Active'
                AND department = 'IT. Development - THIS'
            """, (team_name,))[0][0]


            team_list = frappe.db.get_all('Employee', {'custom_dev_team': team_name, 'status': 'Active','department':'IT. Development - THIS'}, pluck='short_code') or ['']
            emp_list = frappe.db.get_all('Employee', {'custom_dev_team': team_name, 'status':'Active','department':'IT. Development - THIS'}, pluck='name')
            # print(team_list)
            # print(sprint.name)
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
            tot_aph = flt(aph)
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
                <td>{tot_aph}</td>
                <td class="hrs-col">{total_rt}</td>
                <td class="hrs-col">{spr_comp_s}</td>
                <td class="hrs-col">{spr_ncomp_s}</td>
                <td class="hrs-col">{nt_rt}</td>
                <td class="hrs-col">{total_s_rt}</td>
                <td class="hrs-col">{spot_comp_s}</td>
                <td class="hrs-col">{spot_ncomp_s}</td>
                <td class="hrs-col">{nt_srt}</td>
                <td class="hrs-col">{total_rt + total_s_rt}</td>
                <td class="hrs-col">{bt_hours}</td>
                <td class="hrs-col"  style="color: {att_color};">{used_percent_str}</td>
                <td  class="hrs-col"style="color: {font_color};">{comp_percent_str}</td>
                <td class="hrs-col">{ncomp_percent_str}</td>
                <td class="hrs-col">{round(nt_rt + nt_srt, 2)}</td>
                <td class="hrs-col">{nc_rt}</td>
                <td class="hrs-col">{round(reopen_count, 2)}</td>
                <td class="count-col">{total_count}</td>
                <td class="count-col">{tot_comp_count}</td>
                <td class="count-col">{tot_work_count}</td>
                <td class="count-col">{nt_count}</td>
                <td class="count-col">{total_s_count}</td>
                <td class="count-col">{tot_comp_scount}</td>
                <td class="count-col">{tot_work_scount}</td>
                <td class="count-col">{nt_scount}</td>
                <td class="count-col">{total_count + total_s_count}</td>
                <td class="count-col">-</td>
                <td class="count-col">-</td>
                <td class="count-col">{tot_comp_count + tot_comp_scount}</td>
                <td class="count-col">{tot_work_count + tot_work_scount}</td>
                <td class="count-col">{nt_count + nt_scount}</td>
                <td class="count-col">{nc_count}</td>
                <td class="count-col">{reopen_count}</td>
            </tr>
            """
            # print(table)

            sr_no += 1
            team_aph+=tot_aph
        
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
        <td style="background:#020c59;color:white;">{team_aph}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{sub_total_rt}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{round(sub_tot_comp_rt, 2)}/<br>{round(tot_spr_chrs, 2)}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{round(sub_tot_work_rt, 2)}/<br>{round(tot_spr_whrs, 2)}</td>
        <td class="hrs-col" style="background:#d9edf7;color:#110404;">{sub_nt_rt}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{sub_total_s_rt}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{round(sub_tot_comp_srt, 2)}/<br>{round(tot_spot_chrs, 2)}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{round(sub_tot_work_srt, 2)}/<br>{round(tot_spot_whrs, 2)}</td>
        <td class="hrs-col" style="background:#fcf8e3;color:#110404;">{sub_nt_srt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{sub_total_rt + sub_total_s_rt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{round(sub_bt_hours, 2)}</td>
        <td class="hrs-col" style="background:#f0b616;color: {att_color};">{sub_used_str}</td>
        <td class="hrs-col" class="hrs-col" style="background:#f0b616;color: {font_color};">{sub_comp_str}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{sub_work_str}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{round(sub_nt_rt + sub_nt_srt, 2)}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{tot_nc_rt}</td>
        <td class="hrs-col" style="background:#f0b616;color:#110404;">{tot_reopen_count}</td>
        <td class="count-col" class="count-col" style="background:#d9edf7;color:#110404;">{sub_total_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_tot_comp_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_tot_work_count}</td>
        <td class="count-col" style="background:#d9edf7;color:#110404;">{sub_nt_count}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_total_s_count}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_tot_comp_scount}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_tot_work_scount}</td>
        <td class="count-col" style="background:#fcf8e3;color:#110404;">{sub_nt_scount}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{sub_total_count + sub_total_s_count}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">-</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">-</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_comp}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_work}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{overall_nt}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{tot_nc_count}</td>
        <td class="count-col" style="background:#f0b616;color:#110404;">{sub_total_reopen_count}</td>
        
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
def dsr_table(date=None, team=None):

    from collections import defaultdict
    from datetime import datetime, timedelta

    if not date:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Format date for title (e.g. "18/8")
    dt = getdate(date)
    date_label = f"{dt.day}/{dt.month}"

    # =====================================================
    # Orders
    # =====================================================
    dev_team_order = {}
    dev_teams = frappe.get_all("Dev Team", fields=["name", "order_for_it_dashboard"])
    for d in dev_teams:
        dev_team_order[d.name] = d.order_for_it_dashboard if d.order_for_it_dashboard is not None else 999

    cb_order = {}
    cb_aph_map = {}  # cb -> aph (from Employee MIS)
    employees = frappe.get_all(
        "Employee",
        {"status": "Active", "department": "IT. Development - THIS"},
        ["short_code", "custom_order_for_it_dashboard", "custom_aph"]
    )
    for e in employees:
        short_code = (e.short_code or "").strip().upper()
        cb_order[short_code] = e.custom_order_for_it_dashboard if e.custom_order_for_it_dashboard is not None else 999
        if short_code and e.custom_aph is not None:
            cb_aph_map[short_code] = float(e.custom_aph or 0)

    # =====================================================
    # Daily Monitor Data
    # =====================================================
    dm_filters = {"date": date, "service": "IT-SW"}
    if team:
        dm_filters["dev_team"] = team
    daily_monitors = frappe.get_all(
        "Daily Monitor",
        dm_filters,
        ["name", "dev_team", "sprint"]
    )

    all_tasks = []
    for dm in daily_monitors:
        doc = frappe.get_doc("Daily Monitor", dm.name)
        for row in doc.task_details:
            row.dev_team = dm.dev_team
            all_tasks.append(row)

    if not all_tasks:
        return """
        <div style="padding:20px;text-align:center;color:red;font-weight:bold;">
            No Data Found
        </div>
        """

    # Status priority order for sorting
    status_order = {
        "Working": 0, "Open": 1, "Pending Review": 2,
        "Client Review": 3, "Completed": 4,
    }
    # Sort by team order, status, CB order, CB name, project, priority
    sorted_tasks = sorted(
        all_tasks,
        key=lambda x: (
            dev_team_order.get(x.dev_team, 999),
            status_order.get((x.current_status or "").strip(), 5),
            cb_order.get((x.cb or "").strip().upper(), 999),
            (x.cb or "").strip().upper(),
            x.project_name or "",
            x.priority or ""
        )
    )

    # =====================================================
    # Group by team
    # =====================================================
    team_order_list = []
    team_map = {}
    for t in sorted_tasks:
        team = t.dev_team or "Unassigned"
        if team not in team_map:
            team_map[team] = []
            team_order_list.append(team)
        team_map[team].append(t)

    completed_statuses = ("Completed", "Pending Review", "Client Review")

    # =====================================================
    # Build HTML per team
    # =====================================================
    final_html = ""

    for team in team_order_list:
        tasks = team_map[team]
        team_title = f"{team.upper()} - DSR - {date_label}"

        # Calculate P% and E% per CB, and total RT per CB group
        cb_stats = defaultdict(lambda: {"total_rt": 0, "completed_rt": 0, "completed_at": 0})
        for t in tasks:
            cb = (t.cb or "").strip().upper()
            rt = float(t.rt or 0)
            at = float(t.at_taken or 0)
            cb_stats[cb]["total_rt"] += rt
            if (t.current_status or "") in completed_statuses:
                cb_stats[cb]["completed_rt"] += rt
                cb_stats[cb]["completed_at"] += at

        # Determine CB group boundaries for P%/E%/Total RT merged cells
        # Track which rows belong to which CB
        cb_groups = []  # list of (cb_name, start_idx, end_idx, total_rt)
        prev_cb = None
        group_start = 0
        group_rt = 0.0
        for i, t in enumerate(tasks):
            cb = (t.cb or "").strip().upper()
            rt = float(t.rt or 0)
            if cb != prev_cb:
                if prev_cb is not None:
                    cb_groups.append((prev_cb, group_start, i - 1, round(group_rt, 2)))
                prev_cb = cb
                group_start = i
                group_rt = rt
            else:
                group_rt += rt
        if prev_cb is not None:
            cb_groups.append((prev_cb, group_start, len(tasks) - 1, round(group_rt, 2)))

        # Build collapsible table
        team_id = "itm-dsr-team-" + team.replace(" ", "_").replace("&", "_")
        team_et = sum(float(t.et or 0) for t in tasks)
        team_rt = sum(float(t.rt or 0) for t in tasks)

        # Group tasks by CB (ordered)
        cb_task_map = defaultdict(list)
        for t in tasks:
            cb = (t.cb or "").strip().upper()
            cb_task_map[cb].append(t)
        sorted_cbs = sorted(cb_task_map.keys(), key=lambda c: (cb_order.get(c, 999), c))

        html = f"""
        <div style="margin-bottom:30px;">
            <div style="background:#0F1568;padding:10px 15px;border-radius:8px;margin-bottom:10px;text-align:center;">
                <h4 style="margin:0;font-weight:600;color:white;">{team_title}</h4>
            </div>
            <table border="1" width="100%" style="border-collapse:collapse;font-size:11px;background:white;table-layout:fixed;">
                <tr style="background:#0F1568;color:white;text-align:center;position:sticky;top:0;z-index:2;">
                    <th style="width:4%;padding:6px;">S.No</th>
                    <th style="width:7%;padding:6px;">Team</th>
                    <th style="width:8%;padding:6px;">ID</th>
                    <th style="width:15%;padding:6px;">Project Name</th>
                    <th style="width:25%;padding:6px;">Subject</th>
                    <th style="width:5%;padding:6px;">CB</th>
                    <th style="width:5%;padding:6px;">ET</th>
                    <th style="width:5%;padding:6px;">RT</th>
                    <th style="width:7%;padding:6px;">Total RT</th>
                    <th style="width:7%;padding:6px;">Priority</th>
                    <th style="width:10%;padding:6px;">Current status</th>
                    <th style="width:6%;padding:6px;">AT taken</th>
                    <th style="width:5%;padding:6px;">AT%</th>
                    <th style="width:5%;padding:6px;">P%</th>
                    <th style="width:5%;padding:6px;">E%</th>
                </tr>
        """

        # Team header row — always visible
        html += (
            f'<tr style="background:#d0d8f5;text-align:center;font-weight:bold;">'
            f'<td><span class="itm-dsr-team-btn" data-team="{team_id}" style="cursor:pointer;font-size:14px;">+</span></td>'
            f'<td colspan="5" style="text-align:left;padding:4px;">{team}</td>'
            f'<td>{team_et:.2f}</td>'
            f'<td>{team_rt:.2f}</td>'
            f'<td>{team_rt:.2f}</td>'
            f'<td colspan="7"></td>'
            f'</tr>'
        )

        for cb in sorted_cbs:
            cb_tasks = cb_task_map[cb]
            cb_id = "itm-dsr-cb-" + team_id + "-" + cb.replace(" ", "_").replace("&", "_")
            stats = cb_stats.get(cb, {"total_rt": 0, "completed_rt": 0, "completed_at": 0})
            cb_et = sum(float(t.et or 0) for t in cb_tasks)
            cb_rt = sum(float(t.rt or 0) for t in cb_tasks)
            aph = cb_aph_map.get(cb, 0)
            p_pct = round((stats["completed_rt"] / aph) * 100, 2) if aph else 0
            e_pct = round((stats["completed_at"] / stats["completed_rt"]) * 100, 2) if stats["completed_rt"] else 0

            # CB header row — hidden, toggled by team
            html += (
                f'<tr class="itm-dsr-cb-row {team_id}" data-cb="{cb_id}" style="display:none;background:#e8eaf6;text-align:center;font-weight:bold;">'
                f'<td><span class="itm-dsr-cb-btn" data-cb="{cb_id}" style="cursor:pointer;font-size:14px;">+</span></td>'
                f'<td colspan="5" style="text-align:left;padding:4px;">{cb}</td>'
                f'<td>{cb_et:.2f}</td>'
                f'<td>{cb_rt:.2f}</td>'
                f'<td>{cb_rt:.2f}</td>'
                f'<td colspan="3"></td>'
                f'<td>{p_pct}%</td>'
                f'<td>{e_pct}%</td>'
                f'</tr>'
            )

            for idx, t in enumerate(cb_tasks, start=1):
                bg = "#ffffff" if idx % 2 else "#f2f2f7"
                et = float(t.et or 0)
                rt = float(t.rt or 0)
                at_taken = float(t.at_taken or 0)
                at_pct = round((at_taken / rt) * 100, 2) if rt else 0

                # Progress bar for Current Status
                prog = round((at_taken / rt) * 100, 0) if rt and at_taken > 0 else 0
                prog = min(prog, 100)
                bar_color = '#77e6dc'
                if prog > 100:
                    bar_color = '#ff6b6b'
                elif prog > 75:
                    bar_color = '#ffa726'
                elif prog > 0:
                    bar_color = '#4dabf7'

                status = (t.current_status or "").strip()
                status_display = ''
                if status == 'Working': status_display = 'W'
                elif status == 'Pending Review': status_display = 'PR'
                elif status == 'Client Review': status_display = 'CR'
                elif status == 'Completed': status_display = '&#10003;'
                else: status_display = status[:4] if status else '-'

                status_cell = (
                    f'<div style="display:flex;align-items:center;gap:6px;justify-content:center;">'
                    f'<div style="flex:1;max-width:80px;">'
                    f'<div style="height:6px;background:#e0e0e0;border-radius:3px;overflow:hidden;">'
                    f'<div style="width:{prog}%;background:{bar_color};height:100%;border-radius:3px;"></div>'
                    f'</div></div>'
                    f'<span style="font-size:11px;white-space:nowrap;">{status_display} {prog}%</span>'
                    f'</div>'
                )

                html += f"""
                <tr class="itm-dsr-task-row {cb_id} {team_id}" style="display:none;background:{bg};text-align:center;color:black;">
                    <td style="padding:4px;">{idx}</td>
                    <td style="padding:4px;">{team}</td>
                    <td style="padding:4px;white-space:nowrap;">
                        <div style="display:inline-flex;align-items:center;gap:6px;">
                            <span class="itm-task-info-btn" data-task="{t.id}" style="cursor:pointer;font-size:14px;color:#333;">&#128065;</span>
                            <a href="/app/task/{t.id}" target="_blank" style="text-decoration:none;color:black;">{t.id or '-'}</a>
                        </div>
                    </td>
                    <td style="padding:4px;word-break:break-word;text-align:left;">{t.project_name or '-'}</td>
                    <td style="padding:4px;word-break:break-word;text-align:left;">{t.subject or '-'}</td>
                    <td style="padding:4px;">{t.cb or '-'}</td>
                    <td style="padding:4px;">{et}</td>
                    <td style="padding:4px;">{rt}</td>
                    <td style="padding:4px;"></td>
                    <td style="padding:4px;">{t.priority or '-'}</td>
                    <td style="padding:4px;">{status_cell}</td>
                    <td style="padding:4px;">{round(at_taken, 2)}</td>
                    <td style="padding:4px;">{at_pct}%</td>
                    <td style="padding:4px;"></td>
                    <td style="padding:4px;"></td>
                </tr>
                """

        html += "</table></div>"
        final_html += html

    return final_html


@frappe.whitelist()
def dpr_table(date=None, team=None):

    from collections import defaultdict
    from datetime import datetime, timedelta

    if not date:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # DPR is for the NEXT day (next day's allocation)
    dpr_date = add_days(date, 1)

    # Format date for title (e.g. "19/8")
    dt = getdate(dpr_date)
    date_label = f"{dt.day}/{dt.month}"

    # =====================================================
    # Orders
    # =====================================================
    dev_team_order = {}
    dev_teams = frappe.get_all("Dev Team", fields=["name", "order_for_it_dashboard"])
    for d in dev_teams:
        dev_team_order[d.name] = d.order_for_it_dashboard if d.order_for_it_dashboard is not None else 999

    cb_order = {}
    employees = frappe.get_all(
        "Employee",
        {"status": "Active", "department": "IT. Development - THIS"},
        ["short_code", "custom_order_for_it_dashboard"]
    )
    for e in employees:
        short_code = (e.short_code or "").strip().upper()
        cb_order[short_code] = e.custom_order_for_it_dashboard if e.custom_order_for_it_dashboard is not None else 999

    # =====================================================
    # Daily Monitor Data — same records as DSR (dsr_check = 1)
    # DPR shows the allocation view (no AT/P%/E% columns)
    # =====================================================
    dm_filters = {"date": dpr_date, "service": "IT-SW"}
    if team:
        dm_filters["dev_team"] = team
    daily_monitors = frappe.get_all(
        "Daily Monitor",
        dm_filters,
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
        <div style="padding:20px;text-align:center;color:red;font-weight:bold;">
            No Data Found
        </div>
        """

    # Sort by team order, CB order, CB name, project, priority
    sorted_tasks = sorted(
        all_tasks,
        key=lambda x: (
            dev_team_order.get(x.dev_team, 999),
            cb_order.get((x.cb or "").strip().upper(), 999),
            (x.cb or "").strip().upper(),
            x.project_name or "",
            x.priority or ""
        )
    )

    # =====================================================
    # Total RT per contiguous CB group (per team, since sorted by team then CB)
    # =====================================================
    # Determine CB group boundaries and total RT per group
    cb_groups = []  # list of (cb_name, start, end, total_rt)
    prev_cb = None
    group_start = 0
    group_rt = 0.0
    for i, t in enumerate(sorted_tasks):
        cb = (t.cb or "").strip().upper()
        rt = float(t.rt or 0)
        if cb != prev_cb:
            if prev_cb is not None:
                cb_groups.append((prev_cb, group_start, i - 1, round(group_rt, 2)))
            prev_cb = cb
            group_start = i
            group_rt = rt
        else:
            group_rt += rt
    if prev_cb is not None:
        cb_groups.append((prev_cb, group_start, len(sorted_tasks) - 1, round(group_rt, 2)))

    # Map each row index to its group info
    row_group = {}  # row_idx -> (is_first, rowspan, total_rt)
    for cb_name, start, end, total_rt in cb_groups:
        rowspan = end - start + 1
        row_group[start] = (True, rowspan, total_rt)

    # =====================================================
    # Build single HTML table — all teams, continuous S.No
    # =====================================================
    html = f"""
    <div style="margin-bottom:30px;">
        <div style="background:#0F1568;padding:10px 15px;border-radius:8px;margin-bottom:10px;text-align:center;">
            <h4 style="margin:0;font-weight:600;color:white;">DPR - {date_label}</h4>
        </div>
        <table border="1" width="100%" style="border-collapse:collapse;font-size:11px;background:white;table-layout:fixed;">
            <tr style="background:#0F1568;color:white;text-align:center;position:sticky;top:0;z-index:2;">
                <th style="width:4%;padding:6px;">S.No</th>
                <th style="width:7%;padding:6px;">Team</th>
                <th style="width:8%;padding:6px;">ID</th>
                <th style="width:15%;padding:6px;">Project Name</th>
                <th style="width:25%;padding:6px;">Subject</th>
                <th style="width:5%;padding:6px;">CB</th>
                <th style="width:10%;padding:6px;">Status</th>
                <th style="width:5%;padding:6px;">RT</th>
                <th style="width:7%;padding:6px;">Total RT</th>
                <th style="width:7%;padding:6px;">Priority</th>
            </tr>
    """

    for idx, t in enumerate(sorted_tasks, start=1):
        bg = "#ffffff" if idx % 2 else "#e7e6ec"
        team = t.dev_team or "Unassigned"
        rt = float(t.rt or 0)
        status = t.status or t.current_status or "-"

        row_idx = idx - 1
        group_info = row_group.get(row_idx)
        total_rt_cell = ""
        if group_info:
            _, rowspan, total_rt = group_info
            total_rt_cell = f'<td rowspan="{rowspan}" style="padding:6px;text-align:center;font-weight:bold;">{total_rt}</td>'

        html += f"""
            <tr style="background:{bg};text-align:center;color:black;">
                <td style="padding:4px;">{idx}</td>
                <td style="padding:4px;">{team}</td>
                <td style="padding:4px;">
                    <a href="/app/task/{t.id}" target="_blank" style="text-decoration:none;color:black;">{t.id or '-'}</a>
                </td>
                <td style="padding:4px;word-break:break-word;text-align:left;">{t.project_name or '-'}</td>
                <td style="padding:4px;word-break:break-word;text-align:left;">{t.subject or '-'}</td>
                <td style="padding:4px;">{t.cb or '-'}</td>
                <td style="padding:4px;">{status}</td>
                <td style="padding:4px;">{rt}</td>
                {total_rt_cell}
                <td style="padding:4px;">{t.priority or '-'}</td>
            </tr>
        """

    html += "</table></div>"
    return html


@frappe.whitelist()
def download_dsr_excel(date=None, team=None):

    import io
    from collections import defaultdict
    from datetime import datetime, timedelta

    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
    from openpyxl.utils import get_column_letter

    if not date:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    dt = getdate(date)
    date_label = f"{dt.day}/{dt.month}"

    # =====================================================
    # Orders
    # =====================================================
    dev_team_order = {}
    dev_teams = frappe.get_all("Dev Team", fields=["name", "order_for_it_dashboard"])
    for d in dev_teams:
        dev_team_order[d.name] = d.order_for_it_dashboard if d.order_for_it_dashboard is not None else 999

    cb_order = {}
    cb_aph_map = {}  # cb -> aph (from Employee MIS)
    employees = frappe.get_all(
        "Employee",
        {"status": "Active", "department": "IT. Development - THIS"},
        ["short_code", "custom_order_for_it_dashboard", "custom_aph"]
    )
    for e in employees:
        short_code = (e.short_code or "").strip().upper()
        cb_order[short_code] = e.custom_order_for_it_dashboard if e.custom_order_for_it_dashboard is not None else 999
        if short_code and e.custom_aph is not None:
            cb_aph_map[short_code] = float(e.custom_aph or 0)

    # =====================================================
    # Daily Monitor Data
    # =====================================================
    dm_filters = {"date": date, "service": "IT-SW", "dsr_check": 1}
    if team:
        dm_filters["dev_team"] = team
    daily_monitors = frappe.get_all(
        "Daily Monitor",
        dm_filters,
        ["name", "dev_team", "sprint"]
    )

    all_tasks = []
    for dm in daily_monitors:
        doc = frappe.get_doc("Daily Monitor", dm.name)
        for row in doc.task_details:
            row.dev_team = dm.dev_team
            all_tasks.append(row)

    if not all_tasks:
        # Return empty workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "No Data"
        ws.cell(row=1, column=1, value="No Data Found")
        output = io.BytesIO()
        wb.save(output)
        frappe.response.filename = f"DSR_Report_{date}.xlsx"
        frappe.response.filecontent = output.getvalue()
        frappe.response.type = "binary"
        return

    # Sort by team order, CB order, CB name, project, priority
    sorted_tasks = sorted(
        all_tasks,
        key=lambda x: (
            dev_team_order.get(x.dev_team, 999),
            cb_order.get((x.cb or "").strip().upper(), 999),
            (x.cb or "").strip().upper(),
            x.project_name or "",
            x.priority or ""
        )
    )

    completed_statuses = ("Completed", "Pending Review", "Client Review")

    # =====================================================
    # Styles
    # =====================================================
    header_fill = PatternFill(start_color="0F1568", end_color="0F1568", fill_type="solid")
    odd_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    even_fill = PatternFill(start_color="E7E6EC", end_color="E7E6EC", fill_type="solid")
    title_fill = PatternFill(start_color="0F1568", end_color="0F1568", fill_type="solid")

    thin = Side(style="thin", color="CCCCCC")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    header_font = Font(bold=True, color="FFFFFF", size=11)
    title_font = Font(bold=True, color="FFFFFF", size=14)
    normal_font = Font(color="000000", size=10)
    bold_font = Font(bold=True, color="000000", size=10)

    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # =====================================================
    # Workbook — single sheet, all teams in one continuous table
    # =====================================================
    wb = Workbook()
    ws = wb.active
    ws.title = "DSR"

    headers = [
        "S.No", "Team", "ID", "Project Name", "Subject", "CB",
        "ET", "RT", "Total RT", "Priority", "Current status", "AT taken", "AT%",
        "P%", "E%", "Working Remarks"
    ]

    col_widths = [6, 10, 12, 25, 35, 8, 8, 8, 10, 10, 15, 10, 8, 10, 10, 30]

    # Use the full sorted task list (already ordered by team, CB, project, priority)
    # Calculate P% and E% per CB across all teams
    cb_stats = defaultdict(lambda: {"total_rt": 0, "completed_rt": 0, "completed_at": 0})
    for t in sorted_tasks:
        cb = (t.cb or "").strip().upper()
        rt = float(t.rt or 0)
        at = float(t.at_taken or 0)
        cb_stats[cb]["total_rt"] += rt
        if (t.current_status or "") in completed_statuses:
            cb_stats[cb]["completed_rt"] += rt
            cb_stats[cb]["completed_at"] += at

    # Determine CB group boundaries across the full sorted list
    cb_groups = []
    prev_cb = None
    group_start = 0
    group_rt = 0.0
    for i, t in enumerate(sorted_tasks):
        cb = (t.cb or "").strip().upper()
        rt = float(t.rt or 0)
        if cb != prev_cb:
            if prev_cb is not None:
                cb_groups.append((prev_cb, group_start, i - 1, round(group_rt, 2)))
            prev_cb = cb
            group_start = i
            group_rt = rt
        else:
            group_rt += rt
    if prev_cb is not None:
        cb_groups.append((prev_cb, group_start, len(sorted_tasks) - 1, round(group_rt, 2)))

    cb_group_map = {}
    for cb_name, start, end, total_rt in cb_groups:
        cb_group_map[cb_name] = (start, end, total_rt)

    # Row 1: Title (merged A1:O1 — 15 columns)
    title_text = f"DSR - {date_label}"
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=16)
    title_cell = ws.cell(row=1, column=1, value=title_text)
    title_cell.fill = title_fill
    title_cell.font = title_font
    title_cell.alignment = center_align
    ws.row_dimensions[1].height = 30

    # Row 2: Headers
    for col_num, header in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_num, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = center_align
    ws.row_dimensions[2].height = 25

    # Data rows (starting row 3) — continuous S.No across all teams
    for idx, t in enumerate(sorted_tasks, start=1):
        row_num = idx + 2  # row 1=title, row 2=header
        fill = odd_fill if idx % 2 == 0 else even_fill
        team = t.dev_team or "Unassigned"

        et = float(t.et or 0)
        rt = float(t.rt or 0)
        at_taken = float(t.at_taken or 0)
        at_pct = round((at_taken / rt) * 100, 2) if rt else 0

        cb = (t.cb or "").strip().upper()
        stats = cb_stats.get(cb, {"total_rt": 0, "completed_rt": 0, "completed_at": 0})
        aph = cb_aph_map.get(cb, 0)
        p_pct = round((stats["completed_rt"] / aph) * 100, 2) if aph else 0
        e_pct = round((stats["completed_at"] / stats["completed_rt"]) * 100, 2) if stats["completed_rt"] else 0

        status_val = (t.current_status or "").strip()
        remarks_val = (t.remark or "").strip() if status_val == "Working" else ""
        row_data = [
            idx,
            team,
            t.id or "-",
            t.project_name or "-",
            t.subject or "-",
            t.cb or "-",
            et,
            rt,
            None,  # Total RT — will be set with merge
            t.priority or "-",
            status_val or "-",
            round(at_taken, 2),
            at_pct,
            None,  # P% — will be set with merge
            None,  # E% — will be set with merge
            remarks_val,
        ]

        for col_num, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_num, column=col_num, value=value)
            cell.fill = fill
            cell.border = border
            cell.font = normal_font
            if col_num in (4, 5):  # Project Name, Subject
                cell.alignment = left_align
            else:
                cell.alignment = center_align

        # Total RT, P% and E% — merged cells per CB group
        group_info = cb_group_map.get(cb)
        if group_info and group_info[0] == (idx - 1):
            # First row of CB group — set value and merge
            pe_start_row = group_info[0] + 3  # +3 because data starts at row 3
            pe_end_row = group_info[1] + 3
            total_rt_val = group_info[2]

            trt_cell = ws.cell(row=pe_start_row, column=9, value=total_rt_val)
            trt_cell.fill = fill
            trt_cell.border = border
            trt_cell.font = bold_font
            trt_cell.alignment = center_align

            p_cell = ws.cell(row=pe_start_row, column=14, value=p_pct)
            p_cell.fill = fill
            p_cell.border = border
            p_cell.font = bold_font
            p_cell.alignment = center_align

            e_cell = ws.cell(row=pe_start_row, column=15, value=e_pct)
            e_cell.fill = fill
            e_cell.border = border
            e_cell.font = bold_font
            e_cell.alignment = center_align

            if pe_end_row > pe_start_row:
                ws.merge_cells(
                    start_row=pe_start_row, start_column=9,
                    end_row=pe_end_row, end_column=9
                )
                ws.merge_cells(
                    start_row=pe_start_row, start_column=14,
                    end_row=pe_end_row, end_column=14
                )
                ws.merge_cells(
                    start_row=pe_start_row, start_column=15,
                    end_row=pe_end_row, end_column=15
                )

        ws.row_dimensions[row_num].height = 30

    # Column widths
    for col_num, width in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(col_num)].width = width

    # Freeze panes (freeze header row)
    ws.freeze_panes = "A3"

    # =====================================================
    # Save and return
    # =====================================================
    output = io.BytesIO()
    wb.save(output)
    frappe.response.filename = f"DSR_Report_{date}.xlsx"
    frappe.response.filecontent = output.getvalue()
    frappe.response.type = "binary"


@frappe.whitelist()
def download_dpr_excel(date=None):

    import io
    from datetime import datetime, timedelta

    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
    from openpyxl.utils import get_column_letter

    if not date:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # DPR is for the NEXT day (next day's allocation)
    dpr_date = add_days(date, 1)

    dt = getdate(dpr_date)
    date_label = f"{dt.day}/{dt.month}"

    # =====================================================
    # Orders
    # =====================================================
    dev_team_order = {}
    dev_teams = frappe.get_all("Dev Team", fields=["name", "order_for_it_dashboard"])
    for d in dev_teams:
        dev_team_order[d.name] = d.order_for_it_dashboard if d.order_for_it_dashboard is not None else 999

    cb_order = {}
    employees = frappe.get_all(
        "Employee",
        {"status": "Active", "department": "IT. Development - THIS"},
        ["short_code", "custom_order_for_it_dashboard"]
    )
    for e in employees:
        short_code = (e.short_code or "").strip().upper()
        cb_order[short_code] = e.custom_order_for_it_dashboard if e.custom_order_for_it_dashboard is not None else 999

    # =====================================================
    # Daily Monitor Data — same records as DSR (dsr_check = 1)
    # DPR shows the allocation view (no AT/P%/E% columns)
    # =====================================================
    daily_monitors = frappe.get_all(
        "Daily Monitor",
        {"date": dpr_date, "service": "IT-SW"},
        ["name", "dev_team"]
    )

    all_tasks = []
    for dm in daily_monitors:
        doc = frappe.get_doc("Daily Monitor", dm.name)
        for row in doc.task_details:
            row.dev_team = dm.dev_team
            all_tasks.append(row)

    if not all_tasks:
        # Return empty workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "No Data"
        ws.cell(row=1, column=1, value="No Data Found")
        output = io.BytesIO()
        wb.save(output)
        frappe.response.filename = f"DPR_Report_{dpr_date}.xlsx"
        frappe.response.filecontent = output.getvalue()
        frappe.response.type = "binary"
        return

    # Sort by team order, CB order, CB name, project, priority
    sorted_tasks = sorted(
        all_tasks,
        key=lambda x: (
            dev_team_order.get(x.dev_team, 999),
            cb_order.get((x.cb or "").strip().upper(), 999),
            (x.cb or "").strip().upper(),
            x.project_name or "",
            x.priority or ""
        )
    )

    # =====================================================
    # Styles
    # =====================================================
    header_fill = PatternFill(start_color="0F1568", end_color="0F1568", fill_type="solid")
    odd_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    even_fill = PatternFill(start_color="E7E6EC", end_color="E7E6EC", fill_type="solid")
    title_fill = PatternFill(start_color="0F1568", end_color="0F1568", fill_type="solid")

    thin = Side(style="thin", color="CCCCCC")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    header_font = Font(bold=True, color="FFFFFF", size=11)
    title_font = Font(bold=True, color="FFFFFF", size=14)
    normal_font = Font(color="000000", size=10)
    bold_font = Font(bold=True, color="000000", size=10)

    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # =====================================================
    # Total RT per contiguous CB group (per team, since sorted by team then CB)
    # =====================================================
    # Determine CB group boundaries and total RT per group
    cb_groups = []  # list of (cb_name, start, end, total_rt)
    prev_cb = None
    group_start = 0
    group_rt = 0.0
    for i, t in enumerate(sorted_tasks):
        cb = (t.cb or "").strip().upper()
        rt = float(t.rt or 0)
        if cb != prev_cb:
            if prev_cb is not None:
                cb_groups.append((prev_cb, group_start, i - 1, round(group_rt, 2)))
            prev_cb = cb
            group_start = i
            group_rt = rt
        else:
            group_rt += rt
    if prev_cb is not None:
        cb_groups.append((prev_cb, group_start, len(sorted_tasks) - 1, round(group_rt, 2)))

    # Map each row index to its group info
    row_group = {}  # row_idx -> (start, end, total_rt)
    for cb_name, start, end, total_rt in cb_groups:
        row_group[start] = (start, end, total_rt)

    # =====================================================
    # Workbook — single sheet, all teams in one continuous table
    # =====================================================
    wb = Workbook()
    ws = wb.active
    ws.title = "DPR"

    headers = [
        "S.No", "Team", "ID", "Project Name", "Subject", "CB",
        "Status", "RT", "Total RT", "Priority"
    ]

    col_widths = [6, 10, 12, 25, 40, 8, 15, 8, 10, 10]

    # Row 1: Title (merged A1:J1)
    title_text = f"DPR - {date_label}"
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=10)
    title_cell = ws.cell(row=1, column=1, value=title_text)
    title_cell.fill = title_fill
    title_cell.font = title_font
    title_cell.alignment = center_align
    ws.row_dimensions[1].height = 30

    # Row 2: Headers
    for col_num, header in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_num, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = center_align
    ws.row_dimensions[2].height = 25

    # Data rows (starting row 3) — continuous S.No across all teams
    for idx, t in enumerate(sorted_tasks, start=1):
        row_num = idx + 2  # row 1=title, row 2=header
        fill = odd_fill if idx % 2 == 0 else even_fill
        team = t.dev_team or "Unassigned"

        rt = float(t.rt or 0)

        row_data = [
            idx,
            team,
            t.id or "-",
            t.project_name or "-",
            t.subject or "-",
            t.cb or "-",
            t.status or t.current_status or "-",
            rt,
            None,  # Total RT — will be set with merge
            t.priority or "-",
        ]

        for col_num, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_num, column=col_num, value=value)
            cell.fill = fill
            cell.border = border
            cell.font = normal_font
            if col_num in (4, 5):  # Project Name, Subject
                cell.alignment = left_align
            else:
                cell.alignment = center_align

        # Total RT — merged cells per CB group (per contiguous group)
        row_idx = idx - 1
        group_info = row_group.get(row_idx)
        if group_info:
            start, end, total_rt = group_info
            trt_start_row = start + 3  # +3 because data starts at row 3
            trt_end_row = end + 3

            trt_cell = ws.cell(row=trt_start_row, column=9, value=total_rt)
            trt_cell.fill = fill
            trt_cell.border = border
            trt_cell.font = bold_font
            trt_cell.alignment = center_align

            if trt_end_row > trt_start_row:
                ws.merge_cells(
                    start_row=trt_start_row, start_column=9,
                    end_row=trt_end_row, end_column=9
                )

        ws.row_dimensions[row_num].height = 30

    # Column widths
    for col_num, width in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(col_num)].width = width

    # Freeze panes (freeze header row)
    ws.freeze_panes = "A3"

    # =====================================================
    # Save and return
    # =====================================================
    output = io.BytesIO()
    wb.save(output)
    frappe.response.filename = f"DPR_Report_{dpr_date}.xlsx"
    frappe.response.filecontent = output.getvalue()
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



# @frappe.whitelist()
# def get_non_allocated_tasks_in_live_sprint():
#     today = frappe.utils.today()

#     result = []

#     sprints = frappe.get_all(
#         "Sprint",
#         filters={
#             "from_date": ["<=", today],
#             "to_date": [">=", today]
#         },
#         fields=["name", "team"]
#     )

#     for sprint in sprints:

#         allocated_tasks = frappe.get_all(
#             "Sprint Task",
#             filters={"parent": sprint.name},
#             pluck="task"
#         )

#         task_filters = {
#             "custom_dev_team": sprint.team,
#             "status": ["in", ["Open", "Working"]],
#         }
#         frappe.errprint(sprint)
#         if allocated_tasks:
#             task_filters["name"] = ["not in", allocated_tasks]

#         tasks = frappe.get_all(
#             "Task",
#             filters=task_filters,
#             fields=[
#                 "project",
#                 "custom_sprint",
#                 "name",
#                 "subject",
#                 "expected_time",
#                 "rt",
#                 "actual_time",
#                 "priority",
#                 "status",
#                 "creation",
#                 "kt_confirmed",
# 				"custom_age",
# 				"cb"
#             ]
#         )

#         for task in tasks:
#             result.append({
#                 "project": task.project,
#                 "sprint": task.custom_sprint,
#                 "task": task.name,
#                 "subject": task.subject,
#                 "et": task.expected_time,
#                 "rt": task.rt,
#                 "at": task.actual_time,
#                 "age": task.custom_age,
#                 "cf": task.kt_confirmed,
#                 "priority": task.priority,
#                 "status": task.status,
# 				"cb":task.cb
#             })

#     return result

@frappe.whitelist()
def get_non_allocated_tasks_in_live_sprint():

    today = frappe.utils.today()
    result = []

    sprints = frappe.get_all(
        "Sprint",
        filters={
            "from_date": ["<=", today],
            "to_date": [">=", today]
        },
        fields=["name", "team","sprint_id"]
    )

    for sprint in sprints:

        # Current sprint allocated tasks
        allocated_tasks = frappe.get_all(
            "Sprint Task",
            filters={"parent": sprint.name},
            pluck="task"
        )

        task_filters = {
            "custom_dev_team": sprint.team,
            "status": ["in", ["Open", "Working"]],
            "custom_sprint": ["!=", sprint.sprint_id]
        }

        if allocated_tasks:
            task_filters["name"] = ["not in", allocated_tasks]

        tasks = frappe.get_all(
            "Task",
            filters=task_filters,
            fields=[
                "project",
                "custom_sprint",
                "name",
                "subject",
                "expected_time",
                "rt",
                "actual_time",
                "priority",
                "status",
                "creation",
                "kt_confirmed",
                "custom_age",
                "cb"
            ]
        )

        for task in tasks:

            result.append({
                "team": sprint.team,
                "project": task.project,
                "sprint": task.custom_sprint,
                "task": task.name,
                "subject": task.subject,
                "et": task.expected_time,
                "rt": task.rt,
                "at": task.actual_time,
                "age": task.custom_age,
                "cf": task.kt_confirmed,
                "priority": task.priority,
                "status": task.status,
                "cb": task.cb
            })
        
    return result



@frappe.whitelist()
def get_non_allocated_tasks_test(view="overall", kt_confirmed=""):
    today = frappe.utils.today()

    filters = {
        "status": ["in", ["Open", "Working"]],
        "custom_production_date": ["!=", today],
        "service": "IT-SW",
    }

    if view == "sprint":
        result = []
        sprints = frappe.get_all(
            "Sprint",
            filters={
                "from_date": ["<=", today],
                "to_date": [">=", today]
            },
            fields=["name", "team","sprint_id"]
        )
        if sprints:
            for spr in sprints:
                result.append(spr.sprint_id)
        if result:
            filters["custom_sprint"] = ["not in",result]
        else:
            filters["custom_sprint"] = ''
       

    if kt_confirmed == "Yes":
        filters["kt_confirmed"] = 1
    elif kt_confirmed == "No":
        filters["kt_confirmed"] = ["in", [0, None]]

    tasks = frappe.get_all(
        "Task",
        filters=filters,
        fields=[
            "name", "subject", "project", "status",
            "expected_time", "actual_time", "priority",
            "custom_sprint", "custom_age",
            "custom_production_date_count",
            "kt_confirmed", "cb", "rt"
        ],
        order_by="project asc"
    )

    return {"data": tasks}


@frappe.whitelist()
def get_sprint_chart_data(team=None, sprint=None):
    from frappe.utils import nowdate, getdate, date_diff, add_days
    from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday

    today = getdate(nowdate())
    holiday_list_name = "TEAMPRO-2025"

    if sprint:
        sprint_filters = {
            "sprint_id": sprint,
            "docstatus": ["!=", 2],
        }
        if team:
            sprint_filters["team"] = team
    else:
        # No sprint selected — use last sprint ID
        sprint = _get_last_sprint_id()
        if sprint:
            sprint_filters = {
                "sprint_id": sprint,
                "docstatus": ["!=", 2],
            }
            if team:
                sprint_filters["team"] = team
        else:
            sprint_filters = {
                "from_date": ["<=", today],
                "to_date": [">=", today],
                "docstatus": ["!=", 2],
            }
            if team:
                sprint_filters["team"] = team

    sprints = frappe.get_all(
        "Sprint",
        filters=sprint_filters,
        fields=["name", "sprint_id", "from_date", "to_date", "team", "sprint_hours", "allocated_hours"],
    )

    if not sprints:
        return {
            "labels": [],
            "available_hours": [],
            "expected_hours": [],
            "sprint_avl_time": [],
        }

    sprint_names = [sp.name for sp in sprints]

    # Batch: fetch all sprint_avl_time rows for all sprints in one query
    avl_rows = frappe.db.sql(
        """
        SELECT parent, short_code, available_hours, allocated_hours
        FROM `tabSprint Avl Time`
        WHERE parent IN %s
        """,
        (tuple(sprint_names),),
        as_dict=True,
    )

    # Pre-compute working days per sprint (batch holiday check)
    sprint_working_days = {}
    for sp in sprints:
        sp_from = getdate(sp.from_date)
        sp_to = getdate(sp.to_date)
        total_days = date_diff(sp_to, sp_from) + 1
        total_working_days = 0
        working_days_till_today = 0
        for i in range(total_days):
            current_date = add_days(sp_from, i)
            if not is_holiday(holiday_list_name, current_date):
                total_working_days += 1
                if current_date <= today:
                    working_days_till_today += 1
        sprint_working_days[sp.name] = (total_working_days, working_days_till_today)

    # Group avl rows by sprint
    sprint_avl_map = {}
    for r in avl_rows:
        sprint_avl_map.setdefault(r.parent, []).append(r)

    # Fetch Dev Team logos
    team_names = list({sp.team for sp in sprints if sp.team})
    dev_team_logos = {}
    if team_names:
        for dt in frappe.get_all("Dev Team", {"name": ["in", team_names]}, ["name", "logo"]):
            dev_team_logos[dt.name] = dt.logo or ""

    # Team-level sprint totals
    team_sprint_totals = {}

    cb_data = {}

    for sp in sprints:
        sp_from = getdate(sp.from_date)
        sp_to = getdate(sp.to_date)
        total_working_days, working_days_till_today = sprint_working_days[sp.name]

        # Team-level sprint totals (against the Sprint)
        team_sprint_totals[sp.team or "Unassigned"] = {
            "aph": float(sp.sprint_hours or 0),
            "rt": float(sp.allocated_hours or 0),
            "logo": dev_team_logos.get(sp.team, ""),
        }

        rows = sprint_avl_map.get(sp.name, [])
        for row in rows:
            sc = (row.short_code or "").strip().upper()
            if not sc:
                continue

            avl_hrs = float(row.available_hours or 0)
            alloc_hrs = float(row.allocated_hours or 0)

            if total_working_days > 0:
                daily_avl = avl_hrs / total_working_days
                expected_hrs = daily_avl * working_days_till_today
            else:
                expected_hrs = 0

            cb_data[sc] = {
                "available_hours": round(avl_hrs, 2),
                "expected_hours": round(expected_hrs, 2),
                "sprint_avl_time": round(alloc_hrs, 2),
                "team": sp.team or "",
                "sprint_id": sp.sprint_id or sp.name or "",
            }

    employees = frappe.get_all(
        "Employee",
        filters={
            "status": "Active",
            "department": "IT. Development - THIS",
        },
        fields=["name", "short_code", "custom_order_for_it_dashboard", "custom_dev_team", "image"],
    )

    emp_order = {}
    emp_team = {}
    emp_image = {}
    emp_name = {}
    for emp in employees:
        sc = (emp.short_code or "").strip().upper()
        if sc:
            emp_order[sc] = emp.custom_order_for_it_dashboard if emp.custom_order_for_it_dashboard is not None else 999
            emp_team[sc] = emp.custom_dev_team or ""
            emp_image[sc] = emp.image or ""
            emp_name[sc] = emp.name

    # Timesheet hours per employee across the sprint period(s)
    min_from = min([getdate(sp.from_date) for sp in sprints])
    max_to = max([getdate(sp.to_date) for sp in sprints])
    timesheet_data = frappe.db.sql("""
        SELECT t.employee, SUM(t.total_hours) as hours
        FROM `tabTimesheet` t
        WHERE t.docstatus != 2
        AND DATE(t.creation) BETWEEN %s AND %s
        GROUP BY t.employee
    """, (min_from, max_to), as_dict=True)
    ts_hours_by_emp = {t.employee: (t.hours or 0) for t in timesheet_data}

    dev_teams = frappe.get_all(
        "Dev Team", fields=["name", "order_for_it_dashboard"]
    )
    team_order = {}
    for dt in dev_teams:
        team_order[dt.name] = dt.order_for_it_dashboard if dt.order_for_it_dashboard is not None else 999

    ordered_cbs = sorted(
        cb_data.keys(),
        key=lambda sc: (
            team_order.get(emp_team.get(sc, ""), 999),
            emp_order.get(sc, 999),
        ),
    )

    # Order team-level totals by first-seen team order
    ordered_teams = []
    for sc in ordered_cbs:
        team = cb_data[sc]["team"]
        if team not in ordered_teams:
            ordered_teams.append(team)
    team_totals_list = []
    for t in ordered_teams:
        tinfo = team_sprint_totals.get(t, {"aph": 0, "rt": 0, "logo": ""})
        team_totals_list.append({"team": t, "aph": tinfo["aph"], "rt": tinfo["rt"], "logo": tinfo["logo"]})

    return {
        "labels": ordered_cbs,
        "available_hours": [cb_data[sc]["available_hours"] for sc in ordered_cbs],
        "expected_hours": [cb_data[sc]["expected_hours"] for sc in ordered_cbs],
        "sprint_avl_time": [cb_data[sc]["sprint_avl_time"] for sc in ordered_cbs],
        "teams": [cb_data[sc]["team"] for sc in ordered_cbs],
        "sprint_ids": [cb_data[sc]["sprint_id"] for sc in ordered_cbs],
        "images": [emp_image.get(sc, "") for sc in ordered_cbs],
        "team_totals": team_totals_list,
        "timesheet_hours": [ts_hours_by_emp.get(emp_name.get(sc, ""), 0) for sc in ordered_cbs],
    }


@frappe.whitelist()
def get_sprint_teamwise_summary(team=None, sprint=None):
    """Teamwise CB-level sprint summary for the Analytics tab.

    Definitions (per user):
      Planned RT  = RT of planned (spot_task=0) tasks in the sprint
      Comp RT     = RT of planned tasks with cr_status in (Completed, Pending Review, Client Review)
      Work RT     = RT of planned tasks with cr_status in (Working, Open) AND at_period > 0
      NT RT       = RT of planned tasks with cr_status in (Working, Open) AND at_period = 0
      Spot RT / Spot Comp RT / Spot Work RT / Spot NT RT = same logic for spot_task=1
      AT          = at_period (timesheet hours during sprint period)
      Biometric Hrs = bt_difference from Attendance during sprint period
      NC RT       = RT of tasks linked to Energy Point And Non Conformity
      Reopen RT   = RT of tasks with revisions > 0
      DE RT       = RT of tasks with issue_type = 'Developer Error'
    """
    from frappe.utils import nowdate, getdate

    today = getdate(nowdate())

    if sprint:
        sprint_filters = {
            "sprint_id": sprint,
            "docstatus": ["!=", 2],
        }
        if team:
            sprint_filters["team"] = team
    else:
        # No sprint selected — use last sprint ID
        sprint = _get_last_sprint_id()
        if sprint:
            sprint_filters = {
                "sprint_id": sprint,
                "docstatus": ["!=", 2],
            }
            if team:
                sprint_filters["team"] = team
        else:
            sprint_filters = {
                "from_date": ["<=", today],
                "to_date": [">=", today],
                "docstatus": ["!=", 2],
            }
            if team:
                sprint_filters["team"] = team

    sprints = frappe.get_all(
        "Sprint",
        filters=sprint_filters,
        fields=["name", "sprint_id", "from_date", "to_date", "team"],
        order_by="team asc",
    )

    if not sprints:
        return {"teams": []}

    sprint_names = [sp.name for sp in sprints]

    # Employee short_code -> employee name (for NC/biometric lookup)
    # Also short_code -> custom_order for CB sorting
    emp_map = {}
    emp_order_map = {}
    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active", "department": "IT. Development - THIS"},
        fields=["name", "short_code", "custom_order_for_it_dashboard", "custom_dev_team"],
    )
    for emp in employees:
        sc = (emp.short_code or "").strip().upper()
        if sc:
            emp_map[sc] = emp.name
            emp_order_map[sc] = emp.custom_order_for_it_dashboard if emp.custom_order_for_it_dashboard is not None else 999

    # Dev Team ordering
    dev_teams = frappe.get_all("Dev Team", fields=["name", "order_for_it_dashboard"])
    team_order = {}
    for dt in dev_teams:
        team_order[dt.name] = dt.order_for_it_dashboard if dt.order_for_it_dashboard is not None else 999

    completed_statuses = ("Completed", "Pending Review", "Client Review")
    working_statuses = ("Working", "Open")

    # ---- Batch: APH per CB per sprint (from sprint_avl_time child table) ----
    avl_rows = frappe.db.sql(
        """
        SELECT parent, short_code, available_hours
        FROM `tabSprint Avl Time`
        WHERE parent IN %s
        """,
        (tuple(sprint_names),),
        as_dict=True,
    )
    # sprint_name -> {cb: aph}
    sprint_aph_map = {}
    for r in avl_rows:
        sc = (r.short_code or "").strip().upper()
        if sc:
            sprint_aph_map.setdefault(r.parent, {})[sc] = float(r.available_hours or 0)

    # ---- Batch: Main metrics grouped by sprint + cb (single query) ----
    metric_rows = frappe.db.sql(
        """
        SELECT
            parent,
            cb,
            SUM(CASE WHEN spot_task = 0 THEN rt ELSE 0 END) AS planned_rt,
            SUM(CASE WHEN spot_task = 0 AND cr_status IN %s AND IFNULL(at_period,0) > 0 THEN rt ELSE 0 END) AS comp_rt,
            SUM(CASE WHEN spot_task = 0 AND cr_status IN %s AND IFNULL(at_period,0) > 0 THEN rt ELSE 0 END) AS work_rt,
            SUM(CASE WHEN spot_task = 0 AND cr_status IN %s AND IFNULL(at_period,0) = 0 AND IFNULL(kt_confirmed,0) = 1 THEN rt ELSE 0 END) AS nt_rt,
            SUM(CASE WHEN spot_task = 1 THEN rt ELSE 0 END) AS spot_rt,
            SUM(CASE WHEN spot_task = 1 AND cr_status IN %s AND IFNULL(at_period,0) > 0 THEN rt ELSE 0 END) AS spot_comp_rt,
            SUM(CASE WHEN spot_task = 1 AND cr_status IN %s AND IFNULL(at_period,0) > 0 THEN rt ELSE 0 END) AS spot_work_rt,
            SUM(CASE WHEN spot_task = 1 AND cr_status IN %s AND IFNULL(at_period,0) = 0 AND IFNULL(kt_confirmed,0) = 1 THEN rt ELSE 0 END) AS spot_nt_rt,
            SUM(CASE WHEN cr_status IN %s AND IFNULL(at_period,0) > 0 THEN at_period ELSE 0 END) AS completed_at,
            SUM(CASE WHEN cr_status IN %s AND IFNULL(at_period,0) > 0 THEN at_period ELSE 0 END) AS working_at,
            SUM(IFNULL(at_period, 0)) AS total_at,
            SUM(CASE WHEN revisions > 0 THEN rt ELSE 0 END) AS reopen_rt,
            SUM(CASE WHEN issue_type = 'Developer\u00a0Error' THEN rt ELSE 0 END) AS de_rt
        FROM `tabSprint Task`
        WHERE parent IN %s AND IFNULL(cb, '') != ''
        GROUP BY parent, cb
        """,
        (
            completed_statuses, working_statuses, working_statuses,
            completed_statuses, working_statuses, working_statuses,
            completed_statuses, working_statuses,
            tuple(sprint_names),
        ),
        as_dict=True,
    )
    # sprint_name -> {cb -> metric dict}
    sprint_metrics_map = {}
    for r in metric_rows:
        sprint_metrics_map.setdefault(r.parent, {})[r.cb] = r

    # ---- Batch: NC RT grouped by sprint + cb (single query) ----
    # Build emp_name -> short_code reverse map for matching
    nc_rows = frappe.db.sql(
        """
        SELECT st.parent, st.cb, e.emp, IFNULL(SUM(st.rt), 0) AS nc_rt
        FROM `tabSprint Task` st
        JOIN `tabEnergy Point And Non Conformity` e ON e.task = st.task
        WHERE st.parent IN %s AND e.docstatus != 2
        GROUP BY st.parent, st.cb, e.emp
        """,
        (tuple(sprint_names),),
        as_dict=True,
    )
    # sprint_name -> {cb -> nc_rt} (only for matching emp)
    sprint_nc_map = {}
    for r in nc_rows:
        # Only count if the emp matches the CB's employee
        sc = None
        for short_code, emp_name in emp_map.items():
            if emp_name == r.emp:
                sc = short_code
                break
        if sc and sc == (r.cb or "").strip().upper():
            sprint_nc_map.setdefault(r.parent, {})[r.cb] = float(r.nc_rt or 0)

    # ---- Batch: Biometric hours from Attendance (single query per sprint date range) ----
    # Collect all emp_names and their sprint date ranges
    sprint_bt_map = {}  # sprint_name -> {cb -> bt_hours}
    for sp in sprints:
        sp_from = getdate(sp.from_date)
        sp_to = getdate(sp.to_date)
        emp_names = [emp_map[cb] for cb in emp_map if emp_map[cb]]
        if not emp_names:
            continue
        bt_rows = frappe.db.sql(
            """
            SELECT employee, IFNULL(SUM(bt_difference), 0) AS bt_hours
            FROM `tabAttendance`
            WHERE employee IN %s AND docstatus != 2
            AND attendance_date BETWEEN %s AND %s
            GROUP BY employee
            """,
            (tuple(emp_names), sp_from, sp_to),
            as_dict=True,
        )
        # Reverse map: emp_name -> short_code
        emp_to_sc = {emp_name: sc for sc, emp_name in emp_map.items()}
        bt_by_cb = {}
        for r in bt_rows:
            sc = emp_to_sc.get(r.employee)
            if sc:
                bt_by_cb[sc] = round(float(r.bt_hours or 0), 2)
        sprint_bt_map[sp.name] = bt_by_cb

    result_teams = []

    for sp in sprints:
        sprint_name = sp.name
        sprint_id_label = sp.sprint_id or sp.name
        team_name = sp.team or "Unassigned"
        sp_from = getdate(sp.from_date)
        sp_to = getdate(sp.to_date)

        cb_aph_map = sprint_aph_map.get(sprint_name, {})
        metrics_map = sprint_metrics_map.get(sprint_name, {})
        nc_map = sprint_nc_map.get(sprint_name, {})
        bt_map = sprint_bt_map.get(sprint_name, {})

        # Get all CBs for this sprint, sorted by employee order
        cb_list = sorted(
            metrics_map.keys(),
            key=lambda c: emp_order_map.get((c or "").strip().upper(), 999),
        )

        cb_data_list = []

        for cb in cb_list:
            m = metrics_map.get(cb)
            if not m:
                continue

            planned_rt = float(m.planned_rt or 0)
            comp_rt = float(m.comp_rt or 0)
            work_rt = float(m.work_rt or 0)
            nt_rt = float(m.nt_rt or 0)
            spot_rt = float(m.spot_rt or 0)
            spot_comp_rt = float(m.spot_comp_rt or 0)
            spot_work_rt = float(m.spot_work_rt or 0)
            spot_nt_rt = float(m.spot_nt_rt or 0)
            completed_at = float(m.completed_at or 0)
            working_at = float(m.working_at or 0)
            total_at = float(m.total_at or 0)
            reopen_rt = float(m.reopen_rt or 0)
            de_rt = float(m.de_rt or 0)

            total_rt = planned_rt + spot_rt
            total_comp_rt = comp_rt + spot_comp_rt
            total_work_rt = work_rt + spot_work_rt
            total_nt_hours = nt_rt + spot_nt_rt

            nc_rt = nc_map.get(cb, 0.0)
            bt_hours = bt_map.get((cb or "").strip().upper(), 0.0)
            aph = cb_aph_map.get((cb or "").strip().upper(), 0.0)

            cb_data_list.append({
                "cb": cb,
                "aph": round(aph, 2),
                "planned_rt": round(planned_rt, 2),
                "comp_rt": round(comp_rt, 2),
                "work_rt": round(work_rt, 2),
                "nt_rt": round(nt_rt, 2),
                "spot_rt": round(spot_rt, 2),
                "spot_comp_rt": round(spot_comp_rt, 2),
                "spot_work_rt": round(spot_work_rt, 2),
                "spot_nt_rt": round(spot_nt_rt, 2),
                "total_rt": round(total_rt, 2),
                "biometric_hrs": bt_hours,
                "at": round(total_at, 2),
                "completed_rt": round(total_comp_rt, 2),
                "completed_at": round(completed_at, 2),
                "working_rt": round(total_work_rt, 2),
                "working_at": round(working_at, 2),
                "total_nt_hours": round(total_nt_hours, 2),
                "nc_rt": round(nc_rt, 2),
                "reopen_rt": round(reopen_rt, 2),
                "de_rt": round(de_rt, 2),
            })

        # Compute team-level totals (same columns as CB-level)
        team_totals = {
            "aph": 0,
            "planned_rt": 0, "comp_rt": 0, "work_rt": 0, "nt_rt": 0,
            "spot_rt": 0, "spot_comp_rt": 0, "spot_work_rt": 0, "spot_nt_rt": 0,
            "total_rt": 0, "at": 0, "completed_rt": 0, "completed_at": 0,
            "working_rt": 0, "working_at": 0, "total_nt_hours": 0,
            "biometric_hrs": 0, "nc_rt": 0, "reopen_rt": 0, "de_rt": 0,
        }
        for c in cb_data_list:
            for k in team_totals:
                team_totals[k] += c[k]

        # Round team totals
        for k in team_totals:
            team_totals[k] = round(team_totals[k], 2)

        result_teams.append({
            "team": team_name,
            "sprint_id": sprint_id_label,
            "sprint_name": sprint_name,
            "from_date": str(sp_from),
            "to_date": str(sp_to),
            "cbs": cb_data_list,
            "totals": team_totals,
            "order": team_order.get(team_name, 999),
        })

    result_teams.sort(key=lambda x: x["order"])
    return {"teams": result_teams}


def _get_last_sprint_id():
    """Get the last sprint ID (previous sprint) using same logic as update_sprint_filter."""
    sprint_name = frappe.db.get_value(
        'Sprint',
        {'team': 'ALPHA', 'status': 'In Progress'},
        'sprint_id',
        order_by='creation desc'
    )

    previous_sprint_id = None
    today = datetime.today()

    if today.strftime('%A') == 'Monday':
        previous_sprint_id = sprint_name
    else:
        if sprint_name and sprint_name.startswith("SPRINT"):
            current_number = int(sprint_name.replace("SPRINT", "").strip())
            previous_sprint_id = f"SPRINT {current_number}"

    return previous_sprint_id


@frappe.whitelist()
def get_reopen_de_summary(team=None, sprint=None):
    """Fetch Re-Open and Developer Error tasks for a sprint, with linked
    Energy Point & Non Conformity (EP&NC) records.

    Re-Open      = Sprint Task rows with revisions > 0
    Developer Error = Sprint Task rows with issue_type = 'Developer\\xa0Error'

    Returns a dict:
      {
        "reopen":  [ {task, subject, cb, rt, revisions, cr_status, epnc: [{name, action, ...}]}, ... ],
        "de":      [ {task, subject, cb, rt, revisions, cr_status, epnc: [{name, action, ...}]}, ... ],
        "reopen_count": N, "de_count": N,
        "reopen_rt": X, "de_rt": Y
      }
    """
    from frappe.utils import nowdate, getdate

    today = getdate(nowdate())

    # ---- Resolve sprint filter (same logic as get_sprint_teamwise_summary) ----
    if sprint:
        sprint_filters = {"sprint_id": sprint, "docstatus": ["!=", 2]}
        if team:
            sprint_filters["team"] = team
    else:
        sprint = _get_last_sprint_id()
        if sprint:
            sprint_filters = {"sprint_id": sprint, "docstatus": ["!=", 2]}
            if team:
                sprint_filters["team"] = team
        else:
            sprint_filters = {
                "from_date": ["<=", today],
                "to_date": [">=", today],
                "docstatus": ["!=", 2],
            }
            if team:
                sprint_filters["team"] = team

    sprints = frappe.get_all(
        "Sprint",
        filters=sprint_filters,
        fields=["name"],
        order_by="team asc",
    )

    if not sprints:
        return {"reopen": [], "de": [], "reopen_count": 0, "de_count": 0,
                "reopen_rt": 0, "de_rt": 0}

    sprint_names = [sp.name for sp in sprints]

    # Developer Error issue_type uses a non-breaking space (\\xa0) in stored data
    DE_ISSUE_TYPE = "Developer\u00a0Error"

    # ---- Fetch Sprint Task rows that are Re-Open or Developer Error ----
    rows = frappe.db.sql(
        """
        SELECT parent, name, task, subject, cb, rt, revisions, cr_status,
               issue_type, spot_task, project
        FROM `tabSprint Task`
        WHERE parent IN %s
          AND (revisions > 0 OR issue_type = %s)
        ORDER BY parent, cb, task
        """,
        (tuple(sprint_names), DE_ISSUE_TYPE),
        as_dict=True,
    )

    if not rows:
        return {"reopen": [], "de": [], "reopen_count": 0, "de_count": 0,
                "reopen_rt": 0, "de_rt": 0}

    # ---- Collect all task ids for EP&NC batch lookup ----
    task_ids = list({r.task for r in rows if r.task})

    # Batch fetch EP&NC records linked to these tasks.
    # EP&NC records may link via the `task` field OR only mention the task ID
    # inside `reason_of_ep` (e.g. "TS23712 - Developer Error"), so we match both.
    epnc_map = {}  # task -> [ {name, action, emp_name, class_proposed, ...}, ... ]
    if task_ids:
        # 1) Records linked via the `task` link field
        epnc_rows = frappe.db.sql(
            """
            SELECT name, task, action, emp, emp_name,
                   class_proposed, ep_class_proposed,
                   nc_score, energy_score, total, total_nc,
                   reason_of_ep, docstatus
            FROM `tabEnergy Point And Non Conformity`
            WHERE task IN %s AND docstatus != 2
            """,
            (tuple(task_ids),),
            as_dict=True,
        )
        for e in epnc_rows:
            epnc_map.setdefault(e.task, []).append({
                "name": e.name,
                "action": e.action or "",
                "emp": e.emp or "",
                "emp_name": e.emp_name or "",
                "class_proposed": e.class_proposed or "",
                "ep_class_proposed": e.ep_class_proposed or "",
                "nc_score": e.nc_score or "",
                "energy_score": e.energy_score or "",
                "total": e.total or 0,
                "total_nc": e.total_nc or 0,
                "reason_of_ep": e.reason_of_ep or "",
                "docstatus": e.docstatus,
            })

        # 2) Records where the task ID appears in reason_of_ep (task link empty)
        #    Use a single query with OR LIKE conditions per task id.
        like_clauses = " OR ".join(
            ["reason_of_ep LIKE %s"] * len(task_ids)
        )
        like_params = ["%" + tid + "%" for tid in task_ids]
        epnc_like_rows = frappe.db.sql(
            """
            SELECT name, task, action, emp, emp_name,
                   class_proposed, ep_class_proposed,
                   nc_score, energy_score, total, total_nc,
                   reason_of_ep, docstatus
            FROM `tabEnergy Point And Non Conformity`
            WHERE (task IS NULL OR task = '') AND docstatus != 2
              AND ({clauses})
            """.format(clauses=like_clauses),
            tuple(like_params),
            as_dict=True,
        )
        for e in epnc_like_rows:
            # Match the reason text back to the specific task id(s)
            reason = (e.reason_of_ep or "")
            for tid in task_ids:
                if tid in reason:
                    # Avoid duplicate if already matched via task field
                    existing_names = {x["name"] for x in epnc_map.get(tid, [])}
                    if e.name not in existing_names:
                        epnc_map.setdefault(tid, []).append({
                            "name": e.name,
                            "action": e.action or "",
                            "emp": e.emp or "",
                            "emp_name": e.emp_name or "",
                            "class_proposed": e.class_proposed or "",
                            "ep_class_proposed": e.ep_class_proposed or "",
                            "nc_score": e.nc_score or "",
                            "energy_score": e.energy_score or "",
                            "total": e.total or 0,
                            "total_nc": e.total_nc or 0,
                            "reason_of_ep": e.reason_of_ep or "",
                            "docstatus": e.docstatus,
                        })

    # ---- Split into Re-Open and Developer Error lists ----
    reopen_list = []
    de_list = []
    reopen_rt = 0.0
    de_rt = 0.0

    seen_reopen = set()
    seen_de = set()

    for r in rows:
        rt = float(r.rt or 0)
        is_reopen = (r.revisions or 0) > 0
        is_de = (r.issue_type or "") == DE_ISSUE_TYPE

        entry = {
            "task": r.task or "",
            "subject": r.subject or "",
            "cb": r.cb or "",
            "rt": round(rt, 2),
            "revisions": r.revisions or 0,
            "cr_status": r.cr_status or "",
            "spot_task": r.spot_task or 0,
            "project": r.project or "",
            "epnc": epnc_map.get(r.task, []),
        }

        if is_reopen:
            key = (r.task, r.cb)
            if key not in seen_reopen:
                seen_reopen.add(key)
                reopen_list.append(entry)
                reopen_rt += rt

        if is_de:
            key = (r.task, r.cb)
            if key not in seen_de:
                seen_de.add(key)
                de_list.append(entry)
                de_rt += rt

    return {
        "reopen": reopen_list,
        "de": de_list,
        "reopen_count": len(reopen_list),
        "de_count": len(de_list),
        "reopen_rt": round(reopen_rt, 2),
        "de_rt": round(de_rt, 2),
    }


@frappe.whitelist()
def get_rtat_exception_data(team=None, sprint=None):
    """RT Vs AT % > 150% for Completed and Working tasks.

    Section 1: Completed Tasks (cr_status in Completed/Pending Review/Client Review) where at_period/rt*100 > 150
    Section 2: Working Tasks (cr_status in Open/Working) where at_period/rt*100 > 150
    Grouped by Team -> CB, with Sum of RT, Sum of AT Period, Count of Task.
    """
    from frappe.utils import nowdate, getdate

    today = getdate(nowdate())

    if sprint:
        sprint_filters = {"sprint_id": sprint, "docstatus": ["!=", 2]}
        if team:
            sprint_filters["team"] = team
    else:
        # No sprint selected — use last sprint ID
        sprint = _get_last_sprint_id()
        if sprint:
            sprint_filters = {"sprint_id": sprint, "docstatus": ["!=", 2]}
            if team:
                sprint_filters["team"] = team
        else:
            sprint_filters = {
                "from_date": ["<=", today],
                "to_date": [">=", today],
                "docstatus": ["!=", 2],
            }
            if team:
                sprint_filters["team"] = team

    sprints = frappe.get_all(
        "Sprint",
        filters=sprint_filters,
        fields=["name", "team"],
    )

    if not sprints:
        return {"completed": [], "working": []}

    sprint_names = [sp.name for sp in sprints]
    sprint_team_map = {sp.name: sp.team or "Unassigned" for sp in sprints}

    completed_statuses = ("Completed", "Pending Review", "Client Review")
    working_statuses = ("Open", "Working")

    # Dev Team ordering
    dev_teams = frappe.get_all("Dev Team", fields=["name", "order_for_it_dashboard"])
    team_order = {dt.name: dt.order_for_it_dashboard if dt.order_for_it_dashboard is not None else 999 for dt in dev_teams}

    def build_section(statuses):
        rows = frappe.db.sql(
            """
            SELECT
                st.parent,
                st.cb,
                SUM(st.rt) AS sum_rt,
                SUM(st.at_period) AS sum_at,
                COUNT(st.task) AS task_count
            FROM `tabSprint Task` st
            WHERE st.parent IN %s
              AND st.cr_status IN %s
              AND IFNULL(st.rt, 0) > 0
              AND IFNULL(st.at_period, 0) > 0
              AND (st.at_period / st.rt) * 100 > 150
            GROUP BY st.parent, st.cb
            """,
            (tuple(sprint_names), statuses),
            as_dict=True,
        )

        # Group by team -> cb
        team_map = {}
        for r in rows:
            t = sprint_team_map.get(r.parent, "Unassigned")
            if t not in team_map:
                team_map[t] = []
            team_map[t].append({
                "cb": r.cb or "",
                "sum_rt": round(float(r.sum_rt or 0), 2),
                "sum_at": round(float(r.sum_at or 0), 2),
                "task_count": int(r.task_count or 0),
            })

        # Sort teams by order, sort CBs within team
        result = []
        for t in sorted(team_map.keys(), key=lambda x: team_order.get(x, 999)):
            cbs = sorted(team_map[t], key=lambda c: c["cb"])
            tot_rt = sum(c["sum_rt"] for c in cbs)
            tot_at = sum(c["sum_at"] for c in cbs)
            tot_count = sum(c["task_count"] for c in cbs)
            result.append({
                "team": t,
                "cbs": cbs,
                "total_rt": round(tot_rt, 2),
                "total_at": round(tot_at, 2),
                "total_count": tot_count,
            })

        return result

    return {
        "completed": build_section(completed_statuses),
        "working": build_section(working_statuses),
    }


@frappe.whitelist()
def get_nt_priority_tasks(team=None, sprint=None, any_sprint=False):
    """
    Get NT (Not Taken) Tasks with High/Urgent priority.

    Uses the selected sprint (same as previous sections).

    any_sprint=True (AT Zero):
        - Sprint Task.at = 0 (no AT ever logged)

    any_sprint=False (AT Period Zero, Previous AT Exists):
        - Sprint Task.at > 0 (AT logged in previous sprints)
        - Sprint Task.at_period = 0 (no AT in this sprint period)

    Both:
        - Sprint Task.cr_status in (Open, Working)
        - Sprint Task.kt_confirmed = 1
        - Sprint Task.priority in (High, Urgent)

    Results grouped by Team -> CB.
    """
    from frappe.utils import nowdate, getdate

    # Convert string to bool (frappe passes "0"/"1" from frontend)
    if isinstance(any_sprint, str):
        any_sprint = any_sprint.strip().lower() in ("1", "true", "yes")

    today = getdate(nowdate())

    # ---------------------------------------------------------
    # Get Dev Team ordering
    # ---------------------------------------------------------

    dev_teams = frappe.get_all(
        "Dev Team",
        fields=["name", "order_for_it_dashboard"]
    )

    team_order = {
        dt.name: dt.order_for_it_dashboard if dt.order_for_it_dashboard is not None else 999
        for dt in dev_teams
    }

    # ---------------------------------------------------------
    # Get Sprints — always use the selected sprint (same as previous sections)
    # ---------------------------------------------------------

    if sprint:
        sprint_filters = {
            "sprint_id": sprint,
            "docstatus": ["!=", 2]
        }

        if team:
            sprint_filters["team"] = team
    else:
        # No sprint selected — use last sprint ID
        sprint = _get_last_sprint_id()
        if sprint:
            sprint_filters = {
                "sprint_id": sprint,
                "docstatus": ["!=", 2]
            }

            if team:
                sprint_filters["team"] = team
        else:
            # Fallback to current sprint
            sprint_filters = {
                "from_date": ["<=", today],
                "to_date": [">=", today],
                "docstatus": ["!=", 2]
            }

            if team:
                sprint_filters["team"] = team

    sprints = frappe.get_all(
        "Sprint",
        filters=sprint_filters,
        fields=["name", "sprint_id", "team"]
    )

    if not sprints:
        return {"teams": []}

    sprint_names = [sp.name for sp in sprints]

    sprint_team_map = {
        sp.name: sp.team or "Unassigned"
        for sp in sprints
    }

    sprint_id_map = {
        sp.name: sp.sprint_id or sp.name
        for sp in sprints
    }

    # ---------------------------------------------------------
    # NT TASK CONDITION
    # ---------------------------------------------------------
    #
    # Any Sprint:
    #     Sprint Task.at = 0
    #
    # In Sprint:
    #     Sprint Task.at > 0
    #     AND Sprint Task.at_period = 0
    #
    # ---------------------------------------------------------

    if any_sprint:

        nt_condition = """
            IFNULL(st.at, 0) = 0
        """

    else:

        nt_condition = """
            IFNULL(st.at, 0) > 0
            AND IFNULL(st.at_period, 0) = 0
        """

    # ---------------------------------------------------------
    # Get NT Tasks (grouped by parent sprint + CB + priority)
    # ---------------------------------------------------------

    rows = frappe.db.sql(
        f"""
        SELECT
            st.parent,
            st.cb,
            st.priority,
            SUM(st.rt) AS sum_rt,
            COUNT(st.task) AS task_count

        FROM `tabSprint Task` st

        WHERE st.parent IN %s

          AND {nt_condition}

          AND st.cr_status IN ('Open', 'Working')

          AND st.kt_confirmed = 1

          AND st.priority IN ('High', 'Urgent')

        GROUP BY
            st.parent,
            st.cb,
            st.priority
        """,
        (tuple(sprint_names),),
        as_dict=True,
    )

    # ---------------------------------------------------------
    # Group by Team -> CB
    # ---------------------------------------------------------

    team_data = {}

    for row in rows:

        team_name = sprint_team_map.get(
            row.parent,
            "Unassigned"
        )

        # st.parent -> Sprint ID
        sprint_id = sprint_id_map.get(
            row.parent,
            ""
        )

        if team_name not in team_data:
            team_data[team_name] = {
                "parent": sprint_id,
                "high_rt": 0,
                "urgent_rt": 0,
                "high_count": 0,
                "urgent_count": 0,
                "cbs": {}
            }

        cb = row.cb or "?"

        if cb not in team_data[team_name]["cbs"]:
            team_data[team_name]["cbs"][cb] = {
                "high_rt": 0,
                "urgent_rt": 0,
                "high_count": 0,
                "urgent_count": 0
            }

        if row.priority == "High":

            team_data[team_name]["high_rt"] += float(
                row.sum_rt or 0
            )

            team_data[team_name]["high_count"] += int(
                row.task_count or 0
            )

            team_data[team_name]["cbs"][cb]["high_rt"] += float(
                row.sum_rt or 0
            )

            team_data[team_name]["cbs"][cb]["high_count"] += int(
                row.task_count or 0
            )

        elif row.priority == "Urgent":

            team_data[team_name]["urgent_rt"] += float(
                row.sum_rt or 0
            )

            team_data[team_name]["urgent_count"] += int(
                row.task_count or 0
            )

            team_data[team_name]["cbs"][cb]["urgent_rt"] += float(
                row.sum_rt or 0
            )

            team_data[team_name]["cbs"][cb]["urgent_count"] += int(
                row.task_count or 0
            )

    # ---------------------------------------------------------
    # Sort Teams
    # ---------------------------------------------------------

    result = []

    for team_name in sorted(
        team_data.keys(),
        key=lambda x: team_order.get(x, 999)
    ):

        data = team_data[team_name]

        # Convert cbs dict to sorted list
        cbs_list = []
        for cb_name in sorted(data["cbs"].keys()):
            cb_data = data["cbs"][cb_name]
            cbs_list.append({
                "cb": cb_name,
                "high_rt": round(cb_data["high_rt"], 2),
                "urgent_rt": round(cb_data["urgent_rt"], 2),
                "high_count": cb_data["high_count"],
                "urgent_count": cb_data["urgent_count"],
            })

        result.append({
            "team": team_name,

            # st.parent represented as Sprint ID
            "parent": data["parent"],

            "high_rt": round(data["high_rt"], 2),
            "urgent_rt": round(data["urgent_rt"], 2),
            "high_count": data["high_count"],
            "urgent_count": data["urgent_count"],

            "cbs": cbs_list,
        })

    return {
        "teams": result
    }


@frappe.whitelist()
def get_live_status(date=None):
    """Plan vs actual: the day's Daily Monitor plan compared with that day's
    timesheet activity — flags planned tasks with no work logged and
    unplanned work logged outside the DM. Defaults to today; `date` selects
    another day.
    """
    from frappe.utils import flt, now

    today = getdate(date) if date else nowdate()

    dev_teams = frappe.get_all(
        "Dev Team",
        filters={"team_name": ["!=", "Others"], "order_for_it_dashboard": [">=", 0]},
        fields=["name", "logo"],
        order_by="order_for_it_dashboard",
    )
    team_order = [t.name for t in dev_teams]
    team_logo = {t.name: t.logo for t in dev_teams}

    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active", "department": "IT. Development - THIS"},
        fields=["name", "short_code", "employee_name", "custom_emp_image",
                "custom_dev_team", "custom_order_for_it_dashboard", "custom_is_tl"],
    )
    emp_by_cb = {}
    for e in employees:
        cb = (e.short_code or "").strip().upper()
        if cb:
            emp_by_cb[cb] = e
    emp_name_by_cb = {cb: e.name for cb, e in emp_by_cb.items()}

    def cb_order(cb):
        e = emp_by_cb.get(cb)
        return e.custom_order_for_it_dashboard if e and e.custom_order_for_it_dashboard is not None else 999

    status_order = {"Working": 0, "Open": 1, "Pending Review": 2,
                    "Client Review": 3, "Hold": 4}

    def member_entry(cb):
        emp = emp_by_cb.get(cb)
        return {
            "cb": cb,
            "employee": emp.employee_name if emp else cb,
            "image": emp.custom_emp_image if emp else "",
            "is_tl": emp.custom_is_tl if emp else 0,
            "today_hours": 0,
            "aph": 0,
            "planned": 0,
            "worked": 0,
            "tasks": [],
            "unplanned": [],
        }

    # ---- today's timesheet activity: (employee, task) -> hours ----
    ts_rows = frappe.db.sql("""
        SELECT c.employee, cs.task, SUM(cs.hours) AS hours
        FROM `tabTimesheet` c
        JOIN `tabTimesheet Detail` cs ON cs.parent = c.name
        WHERE c.docstatus != 2 AND DATE(cs.from_time) = %s
        GROUP BY c.employee, cs.task
    """, today, as_dict=True)

    emp_today = {}
    task_today = {}   # (emp_name, task) -> hours
    for r in ts_rows:
        h = r.hours or 0
        emp_today[r.employee] = emp_today.get(r.employee, 0) + h
        if r.task:
            task_today[(r.employee, r.task)] = task_today.get((r.employee, r.task), 0) + h

    dms = frappe.get_all(
        "Daily Monitor",
        filters={"date": today, "service": "IT-SW", "docstatus": ["!=", 2]},
        fields=["name", "dev_team", "sprint"],
    )

    grouped = {}  # team -> cb -> member dict
    planned_keys = set()  # (emp_name, task) pairs covered by a DM

    if dms:
        task_at = {}
        for dm in dms:
            doc = frappe.get_doc("Daily Monitor", dm.name)
            team = dm.dev_team or "Unassigned"
            members = grouped.setdefault(team, {})

            for avl in doc.sprint_avl_time or []:
                cb = (avl.short_code or "").strip().upper()
                if not cb:
                    continue
                m = members.setdefault(cb, member_entry(cb))
                m["aph"] = round(flt(avl.available_hours), 2)

            for row in doc.task_details or []:
                cb = (row.cb or "").strip().upper()
                if not cb:
                    continue
                m = members.setdefault(cb, member_entry(cb))
                task_id = row.id
                emp_name = emp_name_by_cb.get(cb)
                if task_id and task_id not in task_at:
                    task_at[task_id] = flt(frappe.db.get_value("Task", task_id, "actual_time"))
                t_hrs = task_today.get((emp_name, task_id), 0) if emp_name else 0
                planned_keys.add((emp_name, task_id))
                m["planned"] += 1
                if t_hrs:
                    m["worked"] += 1
                m["tasks"].append({
                    "name": task_id,
                    "subject": row.subject,
                    "project": row.project_name,
                    "status": row.current_status or row.status,
                    "priority": row.priority,
                    "sprint": dm.sprint,
                    "et": flt(row.et),
                    "at": task_at.get(task_id, 0),
                    "rt": flt(row.rt),
                    "today": round(t_hrs, 2),
                })
    else:
        tasks = frappe.get_all(
            "Task",
            filters={
                "service": "IT-SW",
                "status": ["not in", ["Completed", "Cancelled"]],
            },
            or_filters=[
                ["status", "=", "Working"],
                ["custom_production_date", "=", today],
            ],
            fields=["name", "subject", "cb", "custom_dev_team", "status", "priority",
                    "project", "expected_time", "actual_time", "rt",
                    "custom_sprint", "custom_production_date"],
        )
        for t in tasks:
            cb = (t.cb or "").strip().upper()
            emp = emp_by_cb.get(cb)
            team = t.custom_dev_team or (emp.custom_dev_team if emp else "") or "Unassigned"
            m = grouped.setdefault(team, {}).setdefault(cb, member_entry(cb))
            planned_keys.add((emp.name if emp else None, t.name))
            m["planned"] += 1
            t_hrs = task_today.get((emp.name, t.name), 0) if emp else 0
            if t_hrs:
                m["worked"] += 1
            m["tasks"].append({
                "name": t.name,
                "subject": t.subject,
                "project": t.project,
                "status": t.status,
                "priority": t.priority,
                "sprint": t.custom_sprint,
                "et": flt(t.expected_time),
                "at": flt(t.actual_time),
                "rt": flt(t.rt),
                "today": round(t_hrs, 2),
            })

    # ---- unplanned work: timesheet rows today on tasks not in the DM plan ----
    unplanned_task_ids = {task for (emp, task) in task_today if (emp, task) not in planned_keys}
    if unplanned_task_ids:
        meta = {t.name: t for t in frappe.get_all(
            "Task",
            filters={"name": ["in", list(unplanned_task_ids)]},
            fields=["name", "subject", "project", "status", "priority", "cb", "custom_dev_team"],
        )}
        for (emp_name, task_id), hrs in task_today.items():
            if (emp_name, task_id) in planned_keys:
                continue
            t = meta.get(task_id)
            cb = (t.cb or "").strip().upper() if t else ""
            emp = emp_by_cb.get(cb) or frappe._dict(name=emp_name, short_code=cb,
                                                    employee_name=cb, custom_emp_image="",
                                                    custom_dev_team="", custom_order_for_it_dashboard=999,
                                                    custom_is_tl=0)
            cb = (emp.short_code or "").strip().upper()
            team = (t.custom_dev_team if t and t.custom_dev_team else "") or emp.custom_dev_team or "Unassigned"
            m = grouped.setdefault(team, {}).setdefault(cb, member_entry(cb))
            m["unplanned"].append({
                "name": task_id,
                "subject": t.subject if t else task_id,
                "project": t.project if t else "",
                "status": t.status if t else "",
                "today": round(hrs, 2),
            })

    result = []
    ordered = [t for t in team_order if t in grouped]
    ordered += [t for t in grouped if t not in team_order]

    for team in ordered:
        members = []
        for cb, m in sorted(grouped[team].items(), key=lambda kv: (cb_order(kv[0]), kv[0])):
            emp = emp_by_cb.get(cb)
            m["today_hours"] = round(emp_today.get(emp.name, 0), 2) if emp else 0
            m["tasks"] = sorted(
                m["tasks"],
                key=lambda t: (status_order.get(t["status"], 5), t["priority"] or "", t["name"] or ""),
            )
            members.append(m)
        result.append({
            "team": team,
            "logo": team_logo.get(team, ""),
            "members": members,
        })

    return {
        "generated_at": now(),
        "date": today,
        "from_dm": bool(dms),
        "teams": result,
    }


@frappe.whitelist()
def get_project_wip(project=None, project_type=None):
    """Per-project WIP rollup for the IT-SW dashboard 'Project WIP' tab.

    Filters: project (Link or comma-separated list), project_type.
    SLA window for AMC projects comes from the customer's SLA Details row.
    """
    from teampro.teampro_py.project_monitoring import _get_amc_sla

    pf = {"service": "IT-SW"}
    if project:
        plist = [p.strip() for p in str(project).split(",") if p.strip()]
        if plist:
            pf["name"] = ["in", plist]
    if project_type:
        pf["project_type"] = project_type

    projects = frappe.get_all(
        "Project",
        filters=pf,
        fields=["name", "project_name", "project_type", "customer", "status",
                "spoc", "sales_order", "total_sales_amount", "total_billed_amount",
                "expected_start_date", "expected_end_date"],
        order_by="project_name",
        limit_page_length=0,
    )
    if not projects:
        return {"rows": [], "types": []}

    names = [p.name for p in projects]
    today_d = getdate(nowdate())

    task_map = {r.project: r for r in frappe.db.sql(
        """
        SELECT project,
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open_ct,
            SUM(CASE WHEN status = 'Working' THEN 1 ELSE 0 END) AS working,
            SUM(CASE WHEN status IN ('Pending Review','Code Review','Client Review')
                THEN 1 ELSE 0 END) AS review,
            SUM(CASE WHEN status = 'Hold' THEN 1 ELSE 0 END) AS hold,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN status NOT IN ('Completed','Cancelled','Template')
                     AND exp_end_date IS NOT NULL AND exp_end_date < %(today)s
                THEN 1 ELSE 0 END) AS overdue,
            COALESCE(SUM(expected_time), 0) AS et,
            COALESCE(SUM(actual_time), 0) AS act
        FROM `tabTask`
        WHERE project IN %(ps)s AND is_template = 0
        GROUP BY project
        """,
        {"today": today_d, "ps": names},
        as_dict=True,
    )}

    meeting_map = {}
    if frappe.db.table_exists("Meeting"):
        meeting_map = {r.project: r for r in frappe.db.sql(
            """
            SELECT project, COUNT(*) AS total,
                SUM(CASE WHEN status IN ('Completed','Closed') THEN 1 ELSE 0 END) AS done
            FROM `tabMeeting`
            WHERE project IN %(ps)s
            GROUP BY project
            """,
            {"ps": names},
            as_dict=True,
        )}

    rows = []
    for p in projects:
        t = task_map.get(p.name) or {}
        m = meeting_map.get(p.name) or {}
        sla = _get_amc_sla(p) if p.project_type == "AMC" else {}
        rows.append({
            "name": p.name,
            "project_name": p.project_name or p.name,
            "project_type": p.project_type,
            "customer": p.customer,
            "status": p.status,
            "spoc": p.spoc,
            "expected_end_date": p.expected_end_date,
            "sla_from": sla.get("sla_from_date"),
            "sla_to": sla.get("sla_to_date"),
            "total": t.get("total") or 0,
            "open": t.get("open_ct") or 0,
            "working": t.get("working") or 0,
            "review": t.get("review") or 0,
            "hold": t.get("hold") or 0,
            "completed": t.get("completed") or 0,
            "overdue": t.get("overdue") or 0,
            "et": flt(t.get("et")),
            "at": flt(t.get("act")),
            "meetings": m.get("total") or 0,
            "meetings_done": m.get("done") or 0,
            "so_value": flt(p.total_sales_amount),
            "billed": flt(p.total_billed_amount),
        })

    types = sorted({r["project_type"] for r in rows if r["project_type"]})
    return {"rows": rows, "types": types}
