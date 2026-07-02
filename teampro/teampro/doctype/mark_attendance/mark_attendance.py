import frappe
from datetime import date

@frappe.whitelist()
def get_shift_distribution():
    today = date.today().isoformat()

    
    scheduled_records = frappe.db.sql("""
        SELECT
            sa.shift_type,
            COUNT(sa.employee) AS scheduled
        FROM `tabShift Assignment` sa
        WHERE
            sa.docstatus = 1
            AND sa.status = 'Active'
            AND sa.start_date <= %(today)s
            AND (sa.end_date IS NULL OR sa.end_date >= %(today)s)
        GROUP BY sa.shift_type
    """, {"today": today}, as_dict=True)

    
    checkin_records = frappe.db.sql("""
        SELECT
            sa.shift_type,
            COUNT(DISTINCT ec.employee) AS checked_in
        FROM `tabEmployee Checkin` ec
        JOIN `tabShift Assignment` sa
            ON ec.employee = sa.employee
            AND sa.docstatus = 1
            AND sa.status = 'Active'
            AND sa.start_date <= %(today)s
            AND (sa.end_date IS NULL OR sa.end_date >= %(today)s)
        WHERE
            ec.log_type = 'IN'
            AND DATE(ec.time) = %(today)s
        GROUP BY sa.shift_type
    """, {"today": today}, as_dict=True)

    
    checkin_map = {r.shift_type: r.checked_in for r in checkin_records}

    total_scheduled = 0
    total_in = 0
    shift_rows = []

    for row in scheduled_records:
        s = row.scheduled
        i = checkin_map.get(row.shift_type, 0)
        total_scheduled += s
        total_in += i
        shift_rows.append({
            "label": row.shift_type,
            "scheduled": s,
            "in": i
        })

    return {
        "total_scheduled": total_scheduled,
        "total_in": total_in,
        "shifts": shift_rows
    }


@frappe.whitelist()
def get_attendance_permission_stats():
    from datetime import date
    import calendar

    today = date.today()
    month_start = today.replace(day=1).isoformat()
    month_end = today.replace(day=calendar.monthrange(today.year, today.month)[1]).isoformat()

    
    total_employees = frappe.db.count('Employee', filters={
        'status': 'Active',
        'docstatus': ['!=', 2]
    })

    HOURS_PER_EMPLOYEE = 4.0
    total_allocated = total_employees * HOURS_PER_EMPLOYEE

    
    approved = frappe.db.sql("""
        SELECT
            employee,
            SUM(total_time) AS hours_used
        FROM `tabAttendance Permission`
        WHERE
            workflow_state = 'Approved'
            AND permission_date BETWEEN %(start)s AND %(end)s
        GROUP BY employee
    """, {"start": month_start, "end": month_end}, as_dict=True)

    total_hours_used = sum(r.hours_used or 0 for r in approved)
    employees_applied = len(approved)

    
    flagged = sum(1 for r in approved if (r.hours_used or 0) >= (HOURS_PER_EMPLOYEE * 0.8))

    utilization_pct = round((total_hours_used / total_allocated * 100), 1) if total_allocated else 0

    return {
        "total_allocated": total_allocated,
        "total_hours_used": round(total_hours_used, 1),
        "employees_applied": employees_applied,
        "utilization_pct": utilization_pct,
        "flagged": flagged,
        "total_employees": total_employees,
        "month_label": today.strftime("%B %Y")
    }


@frappe.whitelist()
def get_activity_effort():
    from datetime import date
    import calendar

    today = date.today()
    month_start = today.replace(day=1).isoformat()
    month_end = today.replace(
        day=calendar.monthrange(today.year, today.month)[1]
    ).isoformat()

    rows = frappe.db.sql("""
        SELECT
            tsd.activity_type,
            e.department,
            SUM(tsd.hours) AS total_hours
        FROM `tabTimesheet Detail` tsd
        JOIN `tabTimesheet` ts
            ON tsd.parent = ts.name
        JOIN `tabEmployee` e
            ON ts.employee = e.name
        WHERE
            ts.docstatus = 1
            AND tsd.activity_type IS NOT NULL
            AND tsd.activity_type != ''
            AND DATE(tsd.from_time) BETWEEN %(start)s AND %(end)s
        GROUP BY
            tsd.activity_type,
            e.department
        ORDER BY
            tsd.activity_type,
            e.department
    """, {"start": month_start, "end": month_end}, as_dict=True)

    
    activities = []
    departments = []
    data_map = {}

    for row in rows:
        act = row.activity_type
        dept = row.department or 'Unassigned'
        hrs = round(float(row.total_hours or 0), 1)

        if act not in activities:
            activities.append(act)
        if dept not in departments:
            departments.append(dept)

        if act not in data_map:
            data_map[act] = {}
        data_map[act][dept] = hrs

   
    result = []
    for dept in departments:
        dept_data = []
        for act in activities:
            dept_data.append(data_map.get(act, {}).get(dept, 0))
        result.append({
            "department": dept,
            "data": dept_data
        })

    return {
        "activities": activities,
        "datasets": result,
        "month_label": today.strftime("%B %Y")
    }

@frappe.whitelist()
def get_live_checkins():
    from datetime import date

    today = date.today().isoformat()

    rows = frappe.db.sql("""
        SELECT
            ec.name,
            ec.employee,
            ec.employee_name,
            ec.log_type,
            ec.time,
            ec.shift
        FROM `tabEmployee Checkin` ec
        WHERE
            DATE(ec.time) = %(today)s
        ORDER BY
            ec.time DESC
        LIMIT 20
    """, {"today": today}, as_dict=True)

    result = []
    for row in rows:
        
        t = row.time
        time_str = t.strftime("%I:%M %p") if t else "—"

        doc_url = '/app/employee-checkin/{}'.format(row.name)

        result.append({
            "time": time_str,
            "employee_name": row.employee_name or row.employee or "—",
            "log_type": row.log_type or "—",
            "shift": row.shift or "—",
            "doc_url": doc_url,
        })

    return result


@frappe.whitelist()
def get_request_queue():

    shift_requests = frappe.db.sql("""
        SELECT
            name,
            employee_name,
            workflow_state,
            creation,
            'Shift Request' AS request_type
        FROM `tabShift Request`
        WHERE
            workflow_state = 'Pending for HOD'
        ORDER BY creation DESC
        LIMIT 20
    """, as_dict=True)

    
    attendance_requests = frappe.db.sql("""
        SELECT
            name,
            employee_name,
            workflow_state,
            creation,
            'Attendance Request' AS request_type
        FROM `tabAttendance Request`
        WHERE
            workflow_state = 'Pending for HOD'
        ORDER BY creation DESC
        LIMIT 20
    """, as_dict=True)

   
    combined = shift_requests + attendance_requests
    combined.sort(key=lambda x: x.creation, reverse=True)
    combined = combined[:20]

    result = []
    for row in combined:
        # Format creation date
        created = row.creation
        date_str = created.strftime("%d %b %Y") if created else "—"

        # Build doc URL
        doctype_slug = row.request_type.lower().replace(' ', '-')
        doc_url = '/app/{}/{}'.format(doctype_slug, row.name)

        result.append({
            "name":         row.name,
            "employee_name": row.employee_name or "—",
            "request_type": row.request_type,
            "workflow_state": row.workflow_state,
            "created":      date_str,
            "doc_url":      doc_url,
        })

    return result


@frappe.whitelist()
def get_exceptions_summary():
    from datetime import date

    today = date.today().isoformat()

    
    absent_count = frappe.db.count('Attendance', filters={
        'attendance_date': today,
        'status': 'Absent',
        'docstatus': ["!=", 2]
    })

    
    late_count = frappe.db.count('Attendance', filters={
        'attendance_date': today,
        'late_entry': 1,
        'docstatus': ["!=", 2]
    })

    
    regularization_count = frappe.db.count('Attendance Request', filters={
        'workflow_state': 'Pending for HOD'
    })

    return {
        "absent":         absent_count or 0,
        "late":           late_count or 0,
        "regularization": regularization_count or 0,
        "date_label":     date.today().strftime("%d %B %Y")
    }