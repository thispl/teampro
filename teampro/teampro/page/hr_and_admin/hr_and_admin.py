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
