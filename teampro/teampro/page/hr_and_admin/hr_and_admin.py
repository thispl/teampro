import frappe

@frappe.whitelist()
def epnc_table(from_date=None, to_date=None):
    from frappe.utils import get_first_day, get_last_day, today, getdate

    if not from_date or not to_date:
        from_date = get_first_day(today())
        to_date = get_last_day(today())

    active_emps = frappe.get_all("Employee",filters={"status": "Active"},pluck="name")

    if not active_emps:
        return "<p>No active employees found.</p>"

 
    data = frappe.db.sql("""
        SELECT
            emp,
            MAX(emp_name) AS emp_name,
            MAX(department) AS department,
            SUM(energy_score) AS ep_score,
            SUM(nc_score) AS nc_score
        FROM `tabEnergy Point And Non Conformity`
        WHERE
            docstatus = 1
            AND emp IN %(emp_list)s
            AND DATE(creation) BETWEEN %(start)s AND %(end)s
        GROUP BY emp
        ORDER BY emp_name
    """, {
        "emp_list": tuple(active_emps),
        "start": from_date,
        "end": to_date
    }, as_dict=True)



    html = """
    <div style='max-height: 340px; overflow-y: auto; overflow-x: auto;'>
        <div style='min-width: 500px;'>
            <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
                <thead>
                    <tr>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">S.No</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center; white-space: nowrap;">Employee ID</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Employee Name</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">EP Score</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center; white-space: nowrap;">NP Score</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">ENS</th>
                    </tr>
                </thead>
                <tbody>
    """

    for i, row in enumerate(data, start=1):
        total = (row.ep_score or 0) + (row.nc_score or 0)
        html += f"""
        <tr>
            <td style="text-align:center;">{i}</td>
            <td>{row.emp}</td>
            <td>{row.emp_name}</td>
            <td style="text-align:center; color:{'green' if row.ep_score > 0 else 'black'};">{row.ep_score or 0}</td>
            <td style="text-align:center; color:{'red' if row.nc_score < 0 else 'black'};">{row.nc_score or 0}</td>
            <td style="text-align:center; color:{'green' if total > 0 else 'red' if total < 0 else 'black'};">{total}</td>
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
# def get_hr_summary_cards():
#     active_data = frappe.db.sql("""
#         SELECT department, COUNT(*) as count
#         FROM `tabEmployee`
#         WHERE status = 'Active'
#         GROUP BY department
#         ORDER BY department
#     """, as_dict=True)

#     male_data = frappe.db.sql("""
#         SELECT department, COUNT(*) as count
#         FROM `tabEmployee`
#         WHERE status = 'Active' AND gender = 'Male'
#         GROUP BY department
#         ORDER BY department
#     """, as_dict=True)

#     female_data = frappe.db.sql("""
#         SELECT department, COUNT(*) as count
#         FROM `tabEmployee`
#         WHERE status = 'Active' AND gender = 'Female'
#         GROUP BY department
#         ORDER BY department
#     """, as_dict=True)

#     today = frappe.utils.today()

#     # ✅ Active employees list with department
#     all_active_emp = frappe.db.sql("""
#         SELECT name, department
#         FROM `tabEmployee`
#         WHERE status = 'Active'
#     """, as_dict=True)

#     # ✅ Employees who have in_time set today (Employee Checkin)
#     checked_in_employees = frappe.db.sql("""
#         SELECT DISTINCT employee
#         FROM `tabEmployee Checkin`
#         WHERE DATE(time) = %(today)s
#             AND log_type = 'IN'
#     """, {"today": today}, as_dict=True)

#     checked_in_set = {row.employee for row in checked_in_employees}

#     present_dept_count = {}
#     absent_dept_count = {}

#     for emp in all_active_emp:
#         dept = emp.department or "Not Set"
#         if emp.name in checked_in_set:
#             present_dept_count[dept] = present_dept_count.get(dept, 0) + 1
#         else:
#             absent_dept_count[dept] = absent_dept_count.get(dept, 0) + 1

#     present_data = [{"department": k, "count": v} for k, v in sorted(present_dept_count.items())]
#     absent_data = [{"department": k, "count": v} for k, v in sorted(absent_dept_count.items())]

#     def total(data):
#         return sum(d.count for d in data) if isinstance(data[0], dict) and "count" in data[0] else sum(d["count"] for d in data) if data else 0

#     def total_list(data):
#         return sum(d["count"] for d in data) if data else 0

#     return {
#         "active": {"total": total_list(active_data), "departments": active_data},
#         "male": {"total": total_list(male_data), "departments": male_data},
#         "female": {"total": total_list(female_data), "departments": female_data},
#         "present": {"total": total_list(present_data), "departments": present_data},
#         "absent": {"total": total_list(absent_data), "departments": absent_data},
#     }


@frappe.whitelist()
def get_hr_summary_cards():
    active_data = frappe.db.sql("""
        SELECT department, COUNT(*) as count
        FROM `tabEmployee`
        WHERE status = 'Active'
        GROUP BY department
        ORDER BY department
    """, as_dict=True)

    male_data = frappe.db.sql("""
        SELECT department, COUNT(*) as count
        FROM `tabEmployee`
        WHERE status = 'Active' AND gender = 'Male'
        GROUP BY department
        ORDER BY department
    """, as_dict=True)

    female_data = frappe.db.sql("""
        SELECT department, COUNT(*) as count
        FROM `tabEmployee`
        WHERE status = 'Active' AND gender = 'Female'
        GROUP BY department
        ORDER BY department
    """, as_dict=True)

    today = frappe.utils.today()

    # ✅ All active employees
    all_active_emp = frappe.db.sql("""
        SELECT name, department
        FROM `tabEmployee`
        WHERE status = 'Active'
    """, as_dict=True)

    # ✅ Employees with Present status today
    present_employees = frappe.db.sql("""
        SELECT DISTINCT employee
        FROM `tabAttendance`
        WHERE attendance_date = %(today)s
            AND status = 'Present'
            AND docstatus != 2
    """, {"today": today}, as_dict=True)

    # ✅ Employees with Absent status today — separate query
    absent_employees = frappe.db.sql("""
        SELECT DISTINCT employee
        FROM `tabAttendance`
        WHERE attendance_date = %(today)s
            AND status = 'Absent'
            AND docstatus != 2
    """, {"today": today}, as_dict=True)

    present_set = {row.employee for row in present_employees}
    absent_set = {row.employee for row in absent_employees}

    present_dept_count = {}
    absent_dept_count = {}

    for emp in all_active_emp:
        dept = emp.department or "Not Set"

        if emp.name in present_set:
            present_dept_count[dept] = present_dept_count.get(dept, 0) + 1

        if emp.name in absent_set:
            absent_dept_count[dept] = absent_dept_count.get(dept, 0) + 1

    present_data = [{"department": k, "count": v} for k, v in sorted(present_dept_count.items())]
    absent_data = [{"department": k, "count": v} for k, v in sorted(absent_dept_count.items())]

    def total_list(data):
        return sum(d["count"] for d in data) if data else 0

    return {
        "active": {"total": total_list(active_data), "departments": active_data},
        "male": {"total": total_list(male_data), "departments": male_data},
        "female": {"total": total_list(female_data), "departments": female_data},
        "present": {"total": total_list(present_data), "departments": present_data},
        "absent": {"total": total_list(absent_data), "departments": absent_data},
    }


@frappe.whitelist()
def get_today_attendance():

    today = frappe.utils.today()

    data = frappe.db.sql("""
        SELECT
            employee,
            employee_name,
            attendance_date,
            in_time,
            out_time,
            bt_difference,
            status
        FROM `tabAttendance`
        WHERE attendance_date = %s
        AND docstatus != 2
        ORDER BY employee_name
    """, (today,), as_dict=True)

    return data


@frappe.whitelist()
def get_weekly_attendance_chart(status_filter="Present"):
    from frappe.utils import getdate, nowdate, add_days

    today = getdate(nowdate())
    weekday = today.weekday()
    monday = add_days(today, -weekday)

    days = [add_days(monday, i) for i in range(6)]
    chart_data = []

    for day in days:
        count = frappe.db.sql("""
            SELECT COUNT(DISTINCT employee) as cnt
            FROM `tabAttendance`
            WHERE attendance_date = %(day)s
                AND status = %(status)s
                AND docstatus != 2
        """, {"day": day, "status": status_filter}, as_dict=True)

        chart_data.append({
            "date": str(day),
            "label": frappe.utils.formatdate(day, "MMM d"),
            "count": count[0].cnt if count else 0
        })

    return chart_data


@frappe.whitelist()
def get_attendance_by_date(date, status_filter=None):
    condition = ""
    filters = {"date": date}

    if status_filter:
        condition = "AND a.status = %(status_filter)s"
        filters["status_filter"] = status_filter

    data = frappe.db.sql(f"""
        SELECT a.employee, e.employee_name, a.status
        FROM `tabAttendance` a
        INNER JOIN `tabEmployee` e ON e.name = a.employee
        WHERE a.attendance_date = %(date)s
        AND a.docstatus != 2
            {condition}
        ORDER BY e.employee_name
    """, filters, as_dict=True)

    return data

# @frappe.whitelist()
# def get_late_punch_summary():
#     from frappe.utils import nowdate, get_first_day, get_last_day

#     today = nowdate()
#     first_day = get_first_day(today)
#     last_day = get_last_day(today)

#     data = frappe.db.sql("""
#         SELECT
#             a.employee, e.employee_name,
#             a.attendance_date, a.in_time
#         FROM `tabAttendance` a
#         INNER JOIN `tabEmployee` e ON e.name = a.employee
#         WHERE a.attendance_date BETWEEN %(first_day)s AND %(last_day)s
#             AND a.docstatus != 2
#             AND a.in_time IS NOT NULL
#             AND TIME(a.in_time) > '09:30:00'
#         ORDER BY e.employee_name
#     """, {"first_day": first_day, "last_day": last_day}, as_dict=True)

#     emp_summary = {}
#     for row in data:
#         key = row.employee
#         if key not in emp_summary:
#             emp_summary[key] = {
#                 "employee": row.employee,
#                 "employee_name": row.employee_name,
#                 "late_count": 0,
#                 "dates": []
#             }
#         emp_summary[key]["late_count"] += 1
#         emp_summary[key]["dates"].append(str(row.attendance_date))

#     result = list(emp_summary.values())
#     result.sort(key=lambda x: x["employee_name"])

#     return result


@frappe.whitelist()
def get_late_punch_summary():
    from frappe.utils import nowdate, get_first_day, get_last_day

    today = nowdate()
    first_day = get_first_day(today)
    last_day = get_last_day(today)

    # ✅ Get employees whose linked user has HOD role
    hod_users = frappe.db.sql("""
        SELECT DISTINCT parent
        FROM `tabHas Role`
        WHERE role = 'HOD'
            AND parenttype = 'User'
    """, as_dict=True)
    hod_user_set = {row.parent for row in hod_users}

    hod_employees = frappe.db.sql("""
        SELECT name
        FROM `tabEmployee`
        WHERE user_id IN %(users)s
    """, {"users": list(hod_user_set) or [""]}, as_dict=True)
    hod_employee_set = {row.name for row in hod_employees}

    data = frappe.db.sql("""
        SELECT
            a.employee, e.employee_name,
            a.attendance_date, a.in_time
        FROM `tabAttendance` a
        INNER JOIN `tabEmployee` e ON e.name = a.employee
        WHERE a.attendance_date BETWEEN %(first_day)s AND %(last_day)s
            AND a.docstatus != 2
            AND a.in_time IS NOT NULL
        ORDER BY e.employee_name, a.attendance_date
    """, {"first_day": first_day, "last_day": last_day}, as_dict=True)

    emp_summary = {}
    for row in data:
        # ✅ HOD employees → 09:45 cutoff, others → 09:30 cutoff
        cutoff = "09:45:00" if row.employee in hod_employee_set else "09:30:00"
        in_time_str = str(row.in_time).split(" ")[-1] if row.in_time else None

        if not in_time_str or in_time_str <= cutoff:
            continue  # not late, skip

        key = row.employee
        if key not in emp_summary:
            emp_summary[key] = {
                "employee": row.employee,
                "employee_name": row.employee_name,
                "late_count": 0,
                "dates": [],
                "times": []
            }
        emp_summary[key]["late_count"] += 1
        emp_summary[key]["dates"].append(str(row.attendance_date))
        emp_summary[key]["times"].append(in_time_str)

    result = list(emp_summary.values())
    result.sort(key=lambda x: x["employee_name"])

    return result


@frappe.whitelist()
def get_month_leave_applications():
    from frappe.utils import nowdate, get_first_day, get_last_day

    today = nowdate()
    first_day = get_first_day(today)
    last_day = get_last_day(today)

    data = frappe.db.sql("""
        SELECT
            employee, employee_name, from_date, to_date,
            total_leave_days, workflow_state
        FROM `tabLeave Application`
        WHERE from_date <= %(last_day)s
            AND to_date >= %(first_day)s
    """, {"first_day": first_day, "last_day": last_day}, as_dict=True)

    # Pending first, Approved last, alphabetical within each group
    def sort_key(row):
        state = (row.workflow_state or "").lower()
        is_approved = 1 if "approved" in state else 0
        return (is_approved, (row.employee_name or "").lower())

    data.sort(key=sort_key)

    return data

@frappe.whitelist()
def get_experience_chart_data():
    from frappe.utils import getdate, nowdate, date_diff

    today = getdate(nowdate())

    employees = frappe.db.sql("""
        SELECT name, gender, date_of_joining
        FROM `tabEmployee`
        WHERE status = 'Active'
            AND date_of_joining IS NOT NULL
    """, as_dict=True)

    buckets = {
        "0 - 1 Years": {"Male": 0, "Female": 0},
        "1 - 3 Years": {"Male": 0, "Female": 0},
        "3 - 5 Years": {"Male": 0, "Female": 0},
        "5 - 7 Years": {"Male": 0, "Female": 0},
        "7+ Years":    {"Male": 0, "Female": 0},
    }

    for emp in employees:
        days = date_diff(today, getdate(emp.date_of_joining))
        years = days / 365.25
        gender = emp.gender or "Male"

        if years < 1:
            bucket = "0 - 1 Years"
        elif years < 3:
            bucket = "1 - 3 Years"
        elif years < 5:
            bucket = "3 - 5 Years"
        elif years < 7:
            bucket = "5 - 7 Years"
        else:
            bucket = "7+ Years"

        if gender in buckets[bucket]:
            buckets[bucket][gender] += 1

    return buckets

@frappe.whitelist()
def get_salary_distribution():
    from frappe.utils import get_first_day, get_last_day, add_months, nowdate

    # ✅ Previous month
    prev_month_start = get_first_day(add_months(nowdate(), -1))
    prev_month_end = get_last_day(add_months(nowdate(), -1))

    data = frappe.db.sql("""
        SELECT e.gender, ss.net_pay
        FROM `tabSalary Slip` ss
        INNER JOIN `tabEmployee` e ON e.name = ss.employee
        WHERE ss.docstatus != 2
            AND ss.start_date >= %(start)s
            AND ss.end_date <= %(end)s
            AND e.status = 'Active'
    """, {"start": prev_month_start, "end": prev_month_end}, as_dict=True)

    buckets = {
        "0-10k":     {"Male": 0, "Female": 0},
        "10-20k":    {"Male": 0, "Female": 0},
        "20-30k":    {"Male": 0, "Female": 0},
        "30-40k":    {"Male": 0, "Female": 0},
        "40-50k":    {"Male": 0, "Female": 0},
        "Above 50k": {"Male": 0, "Female": 0},
    }

    for row in data:
        gender = row.gender or "Male"
        sal = row.net_pay or 0

        if sal < 10000:
            bucket = "0-10k"
        elif sal < 20000:
            bucket = "10-20k"
        elif sal < 30000:
            bucket = "20-30k"
        elif sal < 40000:
            bucket = "30-40k"
        elif sal < 50000:
            bucket = "40-50k"
        else:
            bucket = "Above 50k"

        if gender in buckets[bucket]:
            buckets[bucket][gender] += 1

    return buckets


@frappe.whitelist()
def get_experience_employees(bucket, gender=None):
    from frappe.utils import getdate, nowdate, date_diff

    today = getdate(nowdate())

    conditions = "WHERE status = 'Active' AND date_of_joining IS NOT NULL"
    filters = {}

    if gender:
        conditions += " AND gender = %(gender)s"
        filters["gender"] = gender

    employees = frappe.db.sql(f"""
        SELECT name, employee_name, gender, department, date_of_joining
        FROM `tabEmployee`
        {conditions}
    """, filters, as_dict=True)

    bucket_map = {
        "0 - 1 Years": (0, 1),
        "1 - 3 Years": (1, 3),
        "3 - 5 Years": (3, 5),
        "5 - 7 Years": (5, 7),
        "7+ Years":    (7, 999),
    }

    min_y, max_y = bucket_map.get(bucket, (0, 999))
    result = []

    for emp in employees:
        days = date_diff(today, getdate(emp.date_of_joining))
        years = days / 365.25
        if min_y <= years < max_y:
            result.append({
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "gender": emp.gender,
                "department": emp.department,
                "date_of_joining": str(emp.date_of_joining),
                "experience": round(years, 1)
            })

    result.sort(key=lambda x: x["employee_name"])
    return result


@frappe.whitelist()
def get_salary_employees(bucket, gender=None):
    from frappe.utils import get_first_day, get_last_day, add_months, nowdate

    prev_month_start = get_first_day(add_months(nowdate(), -1))
    prev_month_end = get_last_day(add_months(nowdate(), -1))

    conditions = "AND ss.docstatus != 2"
    filters = {
        "start": prev_month_start,
        "end": prev_month_end
    }

    if gender:
        conditions += " AND e.gender = %(gender)s"
        filters["gender"] = gender

    bucket_map = {
        "0-10k":     (0, 10000),
        "10-20k":    (10000, 20000),
        "20-30k":    (20000, 30000),
        "30-40k":    (30000, 40000),
        "40-50k":    (40000, 50000),
        "Above 50k": (50000, 999999999),
    }

    min_sal, max_sal = bucket_map.get(bucket, (0, 999999999))
    filters["min_sal"] = min_sal
    filters["max_sal"] = max_sal

    data = frappe.db.sql(f"""
        SELECT e.name as employee, e.employee_name, e.gender,
               e.department, ss.net_pay
        FROM `tabSalary Slip` ss
        INNER JOIN `tabEmployee` e ON e.name = ss.employee
        WHERE ss.start_date >= %(start)s
            AND ss.end_date <= %(end)s
            AND ss.net_pay >= %(min_sal)s
            AND ss.net_pay < %(max_sal)s
            AND e.status = 'Active'
            {conditions}
        ORDER BY e.employee_name
    """, filters, as_dict=True)

    return data


# @frappe.whitelist()
# def get_attendance_requests(request_type="Permission"):
#     from frappe.utils import nowdate, get_first_day, get_last_day

#     today = nowdate()
#     first_day = get_first_day(today)
#     last_day = get_last_day(today)

#     if request_type == "Permission":
#         reason_filter = "AND ar.reason = 'Permission'"

#     elif request_type == "On Duty":
#         reason_filter = """AND ar.reason IN (
#             'On Duty Working Day',
#             'Comp Off_ On Duty Holiday',
#             'Comp Off_ Present Holiday',
#             'Work From Home'
#         )"""

#     elif request_type == "Miss Punch":
#         reason_filter = "AND ar.reason = 'Mispunch'"

#     else:
#         reason_filter = ""

#     if request_type == "Permission":
#         data = frappe.db.sql(f"""
#             SELECT
#                 ar.employee, e.employee_name, e.department,
#                 ar.from_date, ar.reason,
#                 ar.custom_permission_session,
#                 ar.custom_evening_time,
#                 ar.explanation,
#                 ar.custom_total_time,
#                 ar.approver AS approver
#             FROM `tabAttendance Request` ar
#             INNER JOIN `tabEmployee` e ON e.name = ar.employee
#             WHERE ar.docstatus != 2
#                 AND ar.from_date BETWEEN %(first_day)s AND %(last_day)s
#                 {reason_filter}
#             ORDER BY e.employee_name
#         """, {"first_day": first_day, "last_day": last_day}, as_dict=True)

#     elif request_type == "On Duty":
#         data = frappe.db.sql(f"""
#             SELECT
#                 ar.employee, e.employee_name, e.department,
#                 ar.from_date, ar.to_date,
#                 ar.half_day, ar.half_day_date,
#                 ar.custom_session,
#                 ar.reason, ar.explanation,
#                 ar.approver AS approver,
#                 ar.total_days
#             FROM `tabAttendance Request` ar
#             INNER JOIN `tabEmployee` e ON e.name = ar.employee
#             WHERE ar.docstatus != 2
#                 AND ar.from_date BETWEEN %(first_day)s AND %(last_day)s
#                 {reason_filter}
#             ORDER BY e.employee_name
#         """, {"first_day": first_day, "last_day": last_day}, as_dict=True)

#     elif request_type == "Miss Punch":
#         data = frappe.db.sql(f"""
#             SELECT
#                 ar.employee, e.employee_name, e.department,
#                 ar.from_date, ar.reason,
#                 ar.explanation,
#                 ar.approver AS approver
#             FROM `tabAttendance Request` ar
#             INNER JOIN `tabEmployee` e ON e.name = ar.employee
#             WHERE ar.docstatus != 2
#                 AND ar.from_date BETWEEN %(first_day)s AND %(last_day)s
#                 {reason_filter}
#             ORDER BY e.employee_name
#         """, {"first_day": first_day, "last_day": last_day}, as_dict=True)

#     else:
#         data = []

#     return data

@frappe.whitelist()
def get_attendance_requests(request_type="Permission"):
    from frappe.utils import nowdate, get_first_day, get_last_day

    today = nowdate()
    first_day = get_first_day(today)
    last_day = get_last_day(today)

    reason_map = {
        "Permission": ["Permission"],
        "Miss Punch": ["Mispunch"],
        "On Duty Working Day": ["On Duty Working Day"],
        "Comp Off On Duty Holiday": ["Comp Off_ On Duty Holiday"],
        "Comp Off Present Holiday": ["Comp Off_ Present Holiday"],
    }

    reasons = reason_map.get(request_type, [])
    if not reasons:
        return []

    placeholders = ", ".join([f"%(r{i})s" for i in range(len(reasons))])
    reason_filters = {f"r{i}": reasons[i] for i in range(len(reasons))}
    reason_filters["first_day"] = first_day
    reason_filters["last_day"] = last_day

    data = frappe.db.sql(f"""
        SELECT
            ar.employee, e.employee_name, e.department,
            ar.from_date, ar.to_date,
            ar.half_day, ar.half_day_date,
            ar.custom_session,
            ar.custom_permission_session,
            ar.custom_evening_time,
            ar.custom_total_time,
            ar.reason, ar.explanation,
            ar.approver,
            ar.total_days
        FROM `tabAttendance Request` ar
        INNER JOIN `tabEmployee` e ON e.name = ar.employee
        WHERE ar.docstatus != 2
            AND ar.from_date BETWEEN %(first_day)s AND %(last_day)s
            AND ar.reason IN ({placeholders})
        ORDER BY e.employee_name
    """, reason_filters, as_dict=True)

    for row in data:
        if row.approver:
            row.approver_code = frappe.db.get_value(
                "Employee",
                {"user_id": row.approver},
                "short_code"
            ) or row.approver
        else:
            row.approver_code = "-"

    return data


@frappe.whitelist()
def get_leave_balance_table():
    """Returns an HTML table showing the leave balance (remaining leaves)
    of every active employee for Casual Leave and Compensatory Off,
    along with Date of Joining and Leave Expiry Date."""

    from frappe.utils import today, escape_html, formatdate

    # Only these two leave types are shown
    leave_types = ["Casual Leave", "Compensatory Off"]

    active_emps = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "employee_name", "department", "date_of_joining"],
        order_by="employee_name"
    )

    if not active_emps:
        return "<p style='text-align:center;padding:20px;'>No active employees found.</p>"

    try:
        from hrms.hr.doctype.leave_application.leave_application import get_leave_details
    except Exception:
        return "<p style='text-align:center;padding:20px;color:red;'>HRMS module not available.</p>"

    today_str = today()

    # Pre-fetch latest leave allocation to_date (expiry) per employee per leave type
    expiry_map = {}
    alloc_rows = frappe.db.sql("""
        SELECT employee, leave_type, MAX(to_date) AS expiry_date
        FROM `tabLeave Allocation`
        WHERE docstatus = 1
            AND leave_type IN %(lts)s
            AND employee IN %(emps)s
        GROUP BY employee, leave_type
    """, {
        "lts": tuple(leave_types),
        "emps": tuple([e.name for e in active_emps])
    }, as_dict=True)

    for r in alloc_rows:
        expiry_map.setdefault(r.employee, {})[r.leave_type] = r.expiry_date

    # Build header cells — one column per leave type
    header_cells = "".join([
        f'<th style="position:sticky;top:0;background:#002060;color:white;text-align:center;white-space:nowrap;z-index:10;">{escape_html(lt)}</th>'
        for lt in leave_types
    ])

    # First pass: compute leave details for each employee
    emp_rows = []
    for emp in active_emps:
        try:
            details = get_leave_details(emp.name, today_str)
        except Exception:
            details = {"leave_allocation": {}}

        allocation = details.get("leave_allocation", {}) if isinstance(details, dict) else {}
        emp_expiry = expiry_map.get(emp.name, {})

        casual_alloc = allocation.get("Casual Leave", {})
        casual_total = casual_alloc.get("total_leaves", 0) or 0
        casual_remaining = casual_alloc.get("remaining_leaves", 0) or 0

        emp_rows.append({
            "emp": emp,
            "allocation": allocation,
            "emp_expiry": emp_expiry,
            "casual_total": casual_total,
            "casual_remaining": casual_remaining,
        })

    # Sort: Casual Leave applicable (total > 0) AND remaining > 0 first,
    # then applicable but zero remaining, then not-applicable (total = 0).
    # Within each group, sort by employee_name.
    def sort_key(r):
        if r["casual_total"] > 0 and r["casual_remaining"] > 0:
            tier = 0  # applicable with balance
        elif r["casual_total"] > 0:
            tier = 1  # applicable but zero remaining
        else:
            tier = 2  # not applicable
        return (tier, (r["emp"].employee_name or "").lower())

    emp_rows.sort(key=sort_key)

    rows_html = ""
    for i, r in enumerate(emp_rows, start=1):
        emp = r["emp"]
        allocation = r["allocation"]
        emp_expiry = r["emp_expiry"]

        # Date of Joining
        doj = emp.date_of_joining
        doj_html = f'<td style="text-align:center;">{formatdate(doj) if doj else "-"}</td>'

        # Leave balance cells
        cells = ""
        expiry_dates = []
        for lt in leave_types:
            alloc = allocation.get(lt, {})
            remaining = alloc.get("remaining_leaves", 0) or 0
            total = alloc.get("total_leaves", 0) or 0

            if total > 0:
                disp_remaining = int(remaining) if float(remaining).is_integer() else round(float(remaining), 1)
                disp_total = int(total) if float(total).is_integer() else round(float(total), 1)
                color = "#16a34a" if remaining > 0 else "#dc2626"
                cells += (
                    f'<td style="text-align:center;color:{color};font-weight:600;" '
                    f'title="Remaining {disp_remaining} / Total {disp_total}">{disp_remaining}</td>'
                )
            else:
                cells += '<td style="text-align:center;color:#9ca3af;">-</td>'

            # Collect expiry date for this leave type
            exp = emp_expiry.get(lt)
            if exp:
                expiry_dates.append((lt, exp))

        # Leave Expiry Date — show the earliest upcoming expiry among the leave types
        if expiry_dates:
            expiry_dates.sort(key=lambda x: x[1])
            expiry_label = formatdate(expiry_dates[0][1])
            expiry_title = "; ".join([f"{lt}: {formatdate(d)}" for lt, d in expiry_dates])
            expiry_html = f'<td style="text-align:center;" title="{escape_html(expiry_title)}">{expiry_label}</td>'
        else:
            expiry_html = '<td style="text-align:center;color:#9ca3af;">-</td>'

        row_bg = "#ffffff" if i % 2 == 1 else "#e7e6ec"
        rows_html += f"""
            <tr style="background:{row_bg};">
                <td style="text-align:center;">{i}</td>
                <td style="text-align:center;">{escape_html(emp.name or "")}</td>
                <td style="text-align:left;">{escape_html(emp.employee_name or "")}</td>
                <td style="text-align:left;">{escape_html(emp.department or "-")}</td>
                {doj_html}
                {cells}
                {expiry_html}
            </tr>
        """

    html = f"""
    <div style='max-height: 500px; overflow-y: auto; overflow-x: auto;'>
        <div style='min-width: 900px;'>
            <table class='table table-bordered' style='width: 100%; border-collapse: collapse; margin-bottom:0;'>
                <thead>
                    <tr>
                        <th style="position:sticky;top:0;background:#002060;color:white;text-align:center;z-index:10;">S.No</th>
                        <th style="position:sticky;top:0;background:#002060;color:white;text-align:center;white-space:nowrap;z-index:10;">Employee ID</th>
                        <th style="position:sticky;top:0;background:#002060;color:white;text-align:center;z-index:10;">Employee Name</th>
                        <th style="position:sticky;top:0;background:#002060;color:white;text-align:center;z-index:10;">Department</th>
                        <th style="position:sticky;top:0;background:#002060;color:white;text-align:center;white-space:nowrap;z-index:10;">Date of Joining</th>
                        {header_cells}
                        <th style="position:sticky;top:0;background:#002060;color:white;text-align:center;white-space:nowrap;z-index:10;">Leave Expiry Date</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </div>
    <div style='text-align:right;font-size:11px;color:#6b7280;padding:6px 10px;'>
        Values shown are remaining leaves as of {today_str}. Hover a balance cell to see remaining / total. Hover expiry date to see per leave type.
    </div>
    """

    return html


# ============================================================
# DASHBOARD v2 — PR Scoring, Target Manager, EPNC, HR extras
# ============================================================

FISCAL_YEAR_MONTHS = [
    "Apr", "May", "Jun", "Jul", "Aug", "Sep",
    "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"
]

MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}


def _current_fiscal_year():
    """Return the Fiscal Year doc name covering today."""
    fy = frappe.db.sql("""
        SELECT name FROM `tabFiscal Year`
        WHERE year_start_date <= CURDATE() AND year_end_date >= CURDATE()
        ORDER BY year_start_date DESC LIMIT 1
    """)
    return fy[0][0] if fy else None


@frappe.whitelist()
def get_pr_scoring():
    """Latest PR (Appraisal) scores — leaderboard for the most recent
    submitted appraisal month, plus department averages and YTD totals."""
    from frappe.utils import getdate

    # Latest appraisal month that has submitted records
    latest = frappe.db.sql("""
        SELECT start_date, end_date
        FROM `tabAppraisal`
        WHERE docstatus = 1
        ORDER BY start_date DESC
        LIMIT 1
    """, as_dict=True)

    if not latest:
        return {"month_label": None, "rows": [], "dept_avg": [], "summary": {}}

    start_date = latest[0].start_date
    end_date = latest[0].end_date
    month_label = getdate(start_date).strftime("%B %Y")

    rows = frappe.db.sql("""
        SELECT
            a.name, a.employee, a.employee_name, a.department, a.designation,
            a.total_score, a.final_score, a.custom_grade, a.custom_total_ens,
            a.appraisal_cycle, a.start_date, a.end_date
        FROM `tabAppraisal` a
        WHERE a.docstatus = 1
            AND a.start_date = %(start)s
            AND a.end_date = %(end)s
        ORDER BY a.total_score DESC, a.employee_name
    """, {"start": start_date, "end": end_date}, as_dict=True)

    # Rank + PRS%
    for i, r in enumerate(rows, start=1):
        r["rank"] = i
        r["prs"] = round((float(r.total_score or 0) / 5) * 100, 1)

    # Pending (draft) appraisals for the same month
    pending = frappe.db.sql("""
        SELECT COUNT(*) AS cnt FROM `tabAppraisal`
        WHERE docstatus = 0 AND start_date = %(start)s AND end_date = %(end)s
    """, {"start": start_date, "end": end_date}, as_dict=True)[0].cnt

    # Department averages
    dept_avg = frappe.db.sql("""
        SELECT department, ROUND(AVG(total_score), 2) AS avg_pr,
               COUNT(*) AS emp_count
        FROM `tabAppraisal`
        WHERE docstatus = 1 AND start_date = %(start)s AND end_date = %(end)s
        GROUP BY department
        ORDER BY avg_pr DESC
    """, {"start": start_date, "end": end_date}, as_dict=True)

    # YTD totals per employee (all submitted appraisals this fiscal year)
    fy_name = _current_fiscal_year()
    ytd_map = {}
    if fy_name:
        fy = frappe.get_doc("Fiscal Year", fy_name)
        ytd = frappe.db.sql("""
            SELECT employee, SUM(total_score) AS ytd_pr, COUNT(*) AS cycles
            FROM `tabAppraisal`
            WHERE docstatus = 1
                AND start_date >= %(start)s AND start_date <= %(end)s
            GROUP BY employee
        """, {"start": fy.year_start_date, "end": fy.year_end_date}, as_dict=True)
        ytd_map = {r.employee: r for r in ytd}

    for r in rows:
        y = ytd_map.get(r.employee)
        r["ytd_pr"] = round(float(y.ytd_pr), 2) if y else 0
        r["cycles"] = y.cycles if y else 0

    scores = [float(r.total_score or 0) for r in rows]
    summary = {
        "month_label": month_label,
        "scored": len(rows),
        "pending": pending,
        "avg_pr": round(sum(scores) / len(scores), 2) if scores else 0,
        "top_score": max(scores) if scores else 0,
        "top_employee": rows[0].employee_name if rows else None,
    }

    return {"month_label": month_label, "rows": rows, "dept_avg": dept_avg, "summary": summary}


@frappe.whitelist()
def get_pr_employee_history(employee):
    """Last 8 submitted appraisals for one employee — drill-down."""
    rows = frappe.db.sql("""
        SELECT name, employee, employee_name, department, designation,
               total_score, final_score, custom_grade, custom_total_ens,
               appraisal_cycle, custom_appraisal_cycle_month,
               start_date, end_date, custom_reviewer_remark
        FROM `tabAppraisal`
        WHERE docstatus = 1 AND employee = %(emp)s
        ORDER BY start_date DESC
        LIMIT 8
    """, {"emp": employee}, as_dict=True)

    for r in rows:
        r["prs"] = round((float(r.total_score or 0) / 5) * 100, 1)

    return rows


@frappe.whitelist()
def get_manager_leaderboard():
    """Target Manager leaderboard — committed target vs achieved,
    SR%, reportees, MTD/YTD for the current fiscal year."""
    from frappe.utils import today
    from datetime import datetime

    fy_name = _current_fiscal_year()
    if not fy_name:
        return []

    fy = frappe.get_doc("Fiscal Year", fy_name)
    from_date, to_date = fy.year_start_date, fy.year_end_date

    current_month = datetime.strftime(datetime.strptime(today(), "%Y-%m-%d"), "%b")
    if current_month not in FISCAL_YEAR_MONTHS:
        current_month = "Apr"
    months_to_include = FISCAL_YEAR_MONTHS[:FISCAL_YEAR_MONTHS.index(current_month) + 1]

    managers = frappe.db.sql("""
        SELECT tm.name, tm.employee, tm.employee_name, tm.designation,
               tm.department, tm.service, tm.has_reportees, tm.annual_ct,
               tm.annual_ft, tm.total_ct, tm.total_ct_achieved, tm.custom_sr,
               tm.target_based_unit,
               e.image AS employee_image,
               (SELECT COUNT(*) FROM `tabTarget Manager Reportee` r
                WHERE r.parent = tm.name) AS reportee_count
        FROM `tabTarget Manager` tm
        INNER JOIN `tabEmployee` e ON e.name = tm.employee AND e.status = 'Active'
        WHERE tm.custom_fiscal_year = %(fy)s
        ORDER BY tm.employee_name
    """, {"fy": fy_name}, as_dict=True)

    if not managers:
        return []

    names = [m.name for m in managers]

    # MTD aggregates from Target Child
    mtd_rows = frappe.db.sql("""
        SELECT parent, SUM(revised_ct) AS target, SUM(achieved) AS achieved,
               SUM(ct_yta) AS yta
        FROM `tabTarget Child`
        WHERE parent IN %(parents)s AND month = %(month)s
        GROUP BY parent
    """, {"parents": tuple(names), "month": current_month}, as_dict=True)
    mtd_map = {r.parent: r for r in mtd_rows}

    # YTD aggregates
    ytd_rows = frappe.db.sql("""
        SELECT parent, SUM(revised_ct) AS target, SUM(achieved) AS achieved,
               SUM(ct_yta) AS yta
        FROM `tabTarget Child`
        WHERE parent IN %(parents)s AND month IN %(months)s
        GROUP BY parent
    """, {"parents": tuple(names), "months": tuple(months_to_include)}, as_dict=True)
    ytd_map = {r.parent: r for r in ytd_rows}

    # Month EP / NC per employee
    epnc_rows = frappe.db.sql("""
        SELECT emp, SUM(energy_score) AS ep, SUM(nc_score) AS nc
        FROM `tabEnergy Point And Non Conformity`
        WHERE docstatus = 1
            AND MONTH(creation) = %(mn)s
            AND DATE(creation) BETWEEN %(start)s AND %(end)s
        GROUP BY emp
    """, {"mn": MONTH_MAP[current_month], "start": from_date, "end": to_date}, as_dict=True)
    epnc_map = {r.emp: r for r in epnc_rows}

    out = []
    for m in managers:
        mtd = mtd_map.get(m.name)
        ytd = ytd_map.get(m.name)
        epnc = epnc_map.get(m.employee)

        mtd_target = float(mtd.target or 0) if mtd else 0
        mtd_ach = float(mtd.achieved or 0) if mtd else 0
        ytd_target = float(ytd.target or 0) if ytd else 0
        ytd_ach = float(ytd.achieved or 0) if ytd else 0

        out.append({
            "name": m.name,
            "employee": m.employee,
            "employee_name": m.employee_name,
            "designation": m.designation,
            "department": m.department,
            "service": m.service,
            "employee_image": m.employee_image,
            "has_reportees": m.has_reportees,
            "reportee_count": m.reportee_count,
            "annual_ct": float(m.annual_ct or 0),
            "total_ct": float(m.total_ct or 0),
            "total_ct_achieved": float(m.total_ct_achieved or 0),
            "sr": float(m.custom_sr or 0),
            "target_based_unit": m.target_based_unit,
            "mtd_target": mtd_target,
            "mtd_achieved": mtd_ach,
            "mtd_sr": round((mtd_ach / mtd_target) * 100, 1) if mtd_target else 0,
            "ytd_target": ytd_target,
            "ytd_achieved": ytd_ach,
            "ytd_sr": round((ytd_ach / ytd_target) * 100, 1) if ytd_target else 0,
            "ep": float(epnc.ep or 0) if epnc else 0,
            "nc": float(epnc.nc or 0) if epnc else 0,
        })

    out.sort(key=lambda x: x["mtd_sr"], reverse=True)
    for i, m in enumerate(out, start=1):
        m["rank"] = i

    return out


@frappe.whitelist()
def get_epnc_summary():
    """Current-month EP/NC summary tiles + top performers."""
    from frappe.utils import get_first_day, get_last_day, today

    start = get_first_day(today())
    end = get_last_day(today())

    totals = frappe.db.sql("""
        SELECT
            IFNULL(SUM(energy_score), 0) AS total_ep,
            IFNULL(SUM(nc_score), 0) AS total_nc,
            SUM(CASE WHEN action = 'Energy Point(EP)' THEN 1 ELSE 0 END) AS ep_entries,
            SUM(CASE WHEN action = 'Non Conformity(NC)' THEN 1 ELSE 0 END) AS nc_entries,
            COUNT(DISTINCT emp) AS employees_scored
        FROM `tabEnergy Point And Non Conformity`
        WHERE docstatus = 1 AND DATE(creation) BETWEEN %(start)s AND %(end)s
    """, {"start": start, "end": end}, as_dict=True)[0]

    top_ep = frappe.db.sql("""
        SELECT emp, MAX(emp_name) AS emp_name, MAX(department) AS department,
               SUM(energy_score) AS score
        FROM `tabEnergy Point And Non Conformity`
        WHERE docstatus = 1 AND DATE(creation) BETWEEN %(start)s AND %(end)s
            AND energy_score IS NOT NULL AND energy_score != ''
        GROUP BY emp ORDER BY score DESC LIMIT 3
    """, {"start": start, "end": end}, as_dict=True)

    top_nc = frappe.db.sql("""
        SELECT emp, MAX(emp_name) AS emp_name, MAX(department) AS department,
               SUM(nc_score) AS score
        FROM `tabEnergy Point And Non Conformity`
        WHERE docstatus = 1 AND DATE(creation) BETWEEN %(start)s AND %(end)s
            AND nc_score IS NOT NULL AND nc_score != ''
        GROUP BY emp ORDER BY score ASC LIMIT 3
    """, {"start": start, "end": end}, as_dict=True)

    totals["net"] = float(totals.total_ep or 0) + float(totals.total_nc or 0)
    return {"totals": totals, "top_ep": top_ep, "top_nc": top_nc}


@frappe.whitelist()
def get_extended_hr_stats():
    """Extra HR KPIs — joiners, exits, on-leave today, pending approvals,
    birthdays this month, open job openings."""
    from frappe.utils import get_first_day, get_last_day, today

    today_str = today()
    first_day = get_first_day(today_str)
    last_day = get_last_day(today_str)

    joiners = frappe.db.sql("""
        SELECT COUNT(*) AS c FROM `tabEmployee`
        WHERE status = 'Active'
            AND date_of_joining BETWEEN %(s)s AND %(e)s
    """, {"s": first_day, "e": last_day}, as_dict=True)[0].c

    exits = frappe.db.sql("""
        SELECT COUNT(*) AS c FROM `tabEmployee`
        WHERE status = 'Left'
            AND relieving_date BETWEEN %(s)s AND %(e)s
    """, {"s": first_day, "e": last_day}, as_dict=True)[0].c

    on_leave_today = frappe.db.sql("""
        SELECT COUNT(DISTINCT employee) AS c FROM `tabLeave Application`
        WHERE docstatus = 1 AND %(t)s BETWEEN from_date AND to_date
    """, {"t": today_str}, as_dict=True)[0].c

    pending_leaves = frappe.db.sql("""
        SELECT COUNT(*) AS c FROM `tabLeave Application`
        WHERE docstatus = 0
    """, as_dict=True)[0].c

    pending_att_req = frappe.db.sql("""
        SELECT COUNT(*) AS c FROM `tabAttendance Request`
        WHERE docstatus = 0
    """, as_dict=True)[0].c

    birthdays = frappe.db.sql("""
        SELECT COUNT(*) AS c FROM `tabEmployee`
        WHERE status = 'Active' AND date_of_birth IS NOT NULL
            AND MONTH(date_of_birth) = MONTH(%(t)s)
    """, {"t": today_str}, as_dict=True)[0].c

    try:
        open_positions = frappe.db.sql("""
            SELECT COUNT(*) AS c FROM `tabJob Opening` WHERE status = 'Open'
        """, as_dict=True)[0].c
    except Exception:
        open_positions = 0

    return {
        "joiners": joiners,
        "exits": exits,
        "on_leave_today": on_leave_today,
        "pending_leaves": pending_leaves,
        "pending_att_req": pending_att_req,
        "birthdays": birthdays,
        "open_positions": open_positions,
    }
