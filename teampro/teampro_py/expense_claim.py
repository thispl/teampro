import frappe
from frappe.utils import (
    add_days,
    cstr,
    flt,
    format_datetime,
    formatdate,
    get_datetime,
    get_first_day,
    get_last_day,
    get_link_to_form,
    get_number_format_info,
    getdate,
    nowdate,
    today,
)
@frappe.whitelist()
def get_meet_logs(employee, expense_date):
    if not employee or not expense_date:
        return []

    from_datetime = get_datetime(f"{expense_date} 00:00:00")
    to_datetime = add_days(from_datetime, 1)

    return frappe.db.sql(
        """
        SELECT ml.name
        FROM `tabMeetLog` ml
        WHERE
            ml.employee = %(employee)s
            AND ml.docstatus = 1
            AND ml.creation BETWEEN %(from_dt)s AND %(to_dt)s
            AND ml.name NOT IN (
                SELECT DISTINCT ecd.custom_meet_log
                FROM `tabExpense Claim Detail` ecd
                WHERE
                    ecd.custom_meet_log IS NOT NULL
                    AND ecd.custom_meet_log != ''
            )
        """,
        {
            "employee": employee,
            "from_dt": from_datetime,
            "to_dt": to_datetime,
        },
        pluck="name",
    )