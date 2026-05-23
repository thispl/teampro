import frappe
from frappe.utils import today
from datetime import datetime, timedelta

@frappe.whitelist()
def get_details(user):
    if user == "amar.p@groupteampro.com":
        user_image = "https://erp.teamproit.com/file/377a03c98c/9230dea7a1Amar Karthick P.jpeg"
    else:
        user_image = frappe.db.get_value("User", user, "user_image")
    full_name = frappe.db.get_value("User", user, "full_name")
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    designation = frappe.db.get_value("Employee", employee, "designation") if employee else None
    
    # Meeting Details
    meetings = frappe.db.get_all("Meeting", filters={"owner": user}, fields=["name", "title", "status", "from_time", "to_time", "project", "creation"], order_by="creation desc", limit=2)
    meeting_html = ""
    meeting_idx = 1
    for meeting in meetings:
        if meeting_idx == 1:
            meeting_html += f"""
                <div class="d-flex">
                    <p class="meeting-date pr-1">{frappe.utils.formatdate(meeting.creation.date(), "mm-dd-yyyy")}</p>
            """
        else:
            meeting_html += f"""
                <div class="d-flex  mt-2">
                    <p class="meeting-date pr-1">{frappe.utils.formatdate(meeting.creation.date(), "mm-dd-yyyy")}</p>
            """
        meeting_html += f"""
                    <div class="flex-line"></div>
                </div>
                <div class="meeting-details p-2" onclick="frappe.set_route('Form','Meeting','{meeting.name}')">
                    <div class="d-flex">
                        <p class="meeting-title">{meeting.title}</p>
                        """
        if meeting.status in ("Completed", "Planned"):
            meeting_html += f"""
                        <p class="meeting-status-{(meeting.status).lower()} mt-1 ml-auto">{meeting.status}</p>
                        """
        else:
            meeting_html += f"""
                        <p class="meeting-status mt-1 ml-auto">{meeting.status}</p>
                        """
        meeting_html += f"""
                    </div>
                    <p class="meeting-project">{meeting.project}</p>
                </div>
        """
        meeting_idx += 1
        
    # Team Details
    team_name = frappe.db.get_value("Employee", employee, "custom_dev_team") if employee else None
    department = frappe.db.get_value("Employee", employee, "department") if employee else None
    team_members = frappe.db.get_all("Employee", filters={"custom_dev_team": team_name, "status": "Active", "department": department, "user_id": ["!=", user]}, fields=["name", "employee_name", "user_id", "short_code", "image"], order_by="date_of_joining") if team_name else []
    
    team_members_html = f"""
        <div class="d-flex">
            <h4>{team_name}</h4>
            <button class="add-button ml-auto mb-0" onclick="frappe.set_route('List','Sprint')">Sprint</button>
            <button class="add-button ml-2 mb-0" onclick="frappe.set_route('List','Daily Monitor')">DPR</button>
        </div>
    """
    team_idx = 1
    for team_member in team_members:
        team_member_image = team_member.image or "https://erp.teamproit.com/file/a519df35fd/0b5e45fdccempty-female-avatar.jpg"
        
        if team_idx == 1:
            team_members_html += f"""<div class="team-member p-1 pl-3" onclick="frappe.set_route('Form','Employee','{team_member.name}')">"""
        else:
            team_members_html += f"""<div class="team-member p-1 pl-3 mt-2" onclick="frappe.set_route('Form','Employee','{team_member.name}')">"""
            
        team_members_html += f"""
                <div>
                    <img class="rounded-image" src="{team_member_image}" alt="{team_member.short_code}" />
                </div>
                <div class="mb-0">
                    <p class="team-member-name mb-0">{team_member.employee_name} <span class="team-member-shortcode">({team_member.short_code})</span></p>
                    <a href="/app/user/{team_member.user_id}" class="team-member-user mb-0">{team_member.user_id}</a>
                </div>
            </div>
        """
        
        team_idx += 1
        
    # Task Details
    tasks = frappe.db.get_all("Task", {"custom_allocated_to":user, "custom_production_date": today()}, ["name", "project", "subject", "status", "expected_time"])
    
    tasks_html = f"""
        <div style="min-height: 5px; max-height: 5px; background-color: white; position: sticky; top: 0px;"></div>
        <div class="d-flex flex-row justify-content-center pl-4 task-header" width=100%>
            <p style="width: 10%; text-align: left; font-weight: 600;">S#</p>
            <p style="width: 15%; text-align: left; font-weight: 600;">ID</p>
            <p style="width: 43%; text-align: left; font-weight: 600;">Project</p>
            <p style="width: 13%; text-align: left; font-weight: 600;">ET</p>
            <p style="width: 25%; text-align: left; font-weight: 600;">Status</p>
        </div>
    """
    task_idx = 1
    for task in tasks:
        tasks_html += f"""
            <div title="{task.subject}" class="d-flex flex-row justify-content-center pl-4 task-data border-bottom" width=100%>
                <p style="width: 10%; text-align: left;">{task_idx}</p>
                <p onclick="frappe.set_route('Form','Task','{task.name}')" class="task-link" style="width: 15%; text-align: left;">{task.name}</p>
                <p style="width: 43%; text-align: left;">{task.project}-01-01</p>
                <p style="width: 13%; text-align: left;">{task.expected_time}</p>
                <p style="width: 25%; text-align: left;">{task.status}</p>
            </div>
        """
        task_idx += 1
    
    summary_html = """<div class="simple-bar-chart">"""
    for d in get_summary_details(user):
        summary_html += f"""
            <div class="day-group">
                <div class="bars">
                    <div class="bar" title="{d['timesheet']}" style="--value:{d['timesheet'] * 5}"></div>
                    <div class="att-bar" title="{d['attendance']}" style="--value:{d['attendance'] * 5}"></div>
                </div>
                <span>{d['day']}</span>
            </div>
    """
    summary_html += """
        </div>
    """
    return {
        "full_name": full_name,
        "user_image": user_image,
        "employee": employee,
        "designation": designation,
        "meeting": meeting_html,
        "team": team_members_html,
        "task": tasks_html,
        "summary": summary_html,
    }
    
def test_check():
    print(get_summary_details("amar.p@groupteampro.com"))
    
def get_summary_details(user):
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    today = datetime.today()

    # JS getDay equivalent
    js_day = (today.weekday() + 1) % 7
    monday_offset = -6 if js_day == 0 else 1 - js_day
    monday = today + timedelta(days=monday_offset)

    day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

    week_list = []

    for i in range(7):
        d = monday + timedelta(days=i)
        date = d.strftime("%Y-%m-%d")

        attendance = frappe.db.get_value(
            "Attendance",
            {"employee": employee, "attendance_date": date},
            "bt_difference"
        ) or 0

        timesheet = frappe.db.get_value(
            "Timesheet",
            {"employee": employee, "start_date": date},
            "total_hours"
        ) or 0

        week_list.append({
            "date": date,
            "day": day_names[i],
            "attendance": attendance,
            "timesheet": timesheet
        })

    return week_list