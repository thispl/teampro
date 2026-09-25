import frappe

def compare_old_new():
    from_date = "2026-09-05"
    to_date = "2026-09-05"
    task = "TS24348"
    emp_name = "GP"
    emp = frappe.db.get_value("Employee", {"short_code": emp_name}, "name")

    # Old approach 1: actual_map (submitted hours)
    old_actual = frappe.db.sql("""
        SELECT SUM(d.hours) as hours
        FROM `tabTimesheet Detail` d
        JOIN `tabTimesheet` t ON d.parent = t.name
        WHERE t.docstatus = 1
        AND d.from_time BETWEEN %s AND DATE_ADD(%s, INTERVAL 1 DAY)
        AND d.task = %s AND t.employee = %s
    """, (from_date, to_date, task, emp), as_dict=True)

    # Old approach 2: today_at_map
    old_today = frappe.db.sql("""
        SELECT SUM(TIMESTAMPDIFF(SECOND, d.from_time, IFNULL(d.to_time, NOW()))) / 3600 as hours
        FROM `tabTimesheet Detail` d
        JOIN `tabTimesheet` t ON d.parent = t.name
        WHERE t.docstatus != 2
        AND d.from_time BETWEEN %s AND DATE_ADD(%s, INTERVAL 1 DAY)
        AND d.task = %s AND t.employee = %s
    """, (from_date, to_date, task, emp), as_dict=True)

    # New approach
    parents = frappe.db.sql("""
        SELECT name FROM `tabTimesheet`
        WHERE docstatus != 2 AND start_date <= %s AND end_date >= %s
    """, (to_date, from_date), as_list=True)
    parent_names = [p[0] for p in parents]
    new_result = frappe.db.sql("""
        SELECT
            SUM(CASE WHEN t.docstatus = 1 THEN d.hours ELSE 0 END) as submitted_hours,
            SUM(CASE WHEN t.docstatus != 2 THEN
                CASE WHEN d.to_time IS NOT NULL THEN d.hours
                ELSE TIMESTAMPDIFF(SECOND, d.from_time, NOW()) / 3600 END
                ELSE 0 END) as total_hours
        FROM `tabTimesheet Detail` d
        JOIN `tabTimesheet` t ON d.parent = t.name
        WHERE d.parent IN %s
        AND d.from_time BETWEEN %s AND DATE_ADD(%s, INTERVAL 1 DAY)
        AND d.task = %s AND t.employee = %s
    """, (tuple(parent_names), from_date, to_date, task, emp), as_dict=True)

    print(f"Task {task}, Emp {emp_name} ({emp}):")
    print(f"  Old actual (submitted): {old_actual[0].hours}")
    print(f"  Old today_at: {old_today[0].hours}")
    print(f"  New submitted: {new_result[0].submitted_hours}")
    print(f"  New total (today_at): {new_result[0].total_hours}")
