import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def get_employees():

    employees = frappe.get_all(
        "Employee",
        fields=[
            "name",
            "employee_name",
            "image",
            "designation",
            "department"
        ]
    )

    return employees


# @frappe.whitelist()
# def get_department_data_all():
#     data = {}

#     records = frappe.db.sql("""
#         SELECT 
#             e.department,
#             SUM(t.annual_ct) as target,
#             SUM(t.total_ct_achieved) as achieved
#         FROM `tabTarget Manager` t
#         INNER JOIN `tabEmployee` e ON e.name = t.employee
#         WHERE e.designation IN ('Director', 'Deputy General Manager','Deputy Manager')
#         GROUP BY e.department
#     """, as_dict=1)

#     for r in records:
#         data[r.department] = {
#             "hod_target": r.target or 0,
#             "hod_achieved": r.achieved or 0
#         }

#     return data

@frappe.whitelist()
def get_department_data_all():
    data = {}

    from frappe.utils import nowdate, now_datetime

    # ✅ Fiscal Year
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        {"year_start_date": ["<=", nowdate()], "year_end_date": [">=", nowdate()]},
        "name"
    )

    # 🔥 Month Mapping (FY order)
    mapping_months = {
        'Apr': 12, 'May': 11, 'Jun': 10, 'Jul': 9,
        'Aug': 8, 'Sep': 7, 'Oct': 6, 'Nov': 5,
        'Dec': 4, 'Jan': 3, 'Feb': 2, 'Mar': 1
    }

    current_month = now_datetime().strftime("%b")  # Apr, May...
    current_order = mapping_months.get(current_month, 0)

    # ✅ YTD DATA
    records = frappe.db.sql("""
        SELECT 
            e.department,
            SUM(t.custom_total_target_point) as target,
            SUM(t.custom_total_achieved_point) as achieved
        FROM `tabTarget Manager` t
        INNER JOIN `tabEmployee` e ON e.name = t.employee
        WHERE e.designation IN ('Director', 'Deputy General Manager','Deputy Manager')
        GROUP BY e.department
    """, as_dict=1)

    for r in records:
        data[r.department] = {
            "hod_target": r.target or 0,
            "hod_achieved": r.achieved or 0,
            "mtd_target": 0,
            "mtd_achieved": 0
        }

    # ✅ MTD DATA (FROM CHILD TABLE using MONTH STRING)
    mtd_records = frappe.db.sql("""
        SELECT
            e.department,
            tc.month,
            tc.ct_point,
            tc.achieved_point
        FROM `tabTarget Child` tc
        INNER JOIN `tabTarget Manager` tm ON tm.name = tc.parent
        INNER JOIN `tabEmployee` e ON e.name = tm.employee
        WHERE tm.custom_fiscal_year = %s
          AND e.designation IN ('Director', 'Deputy General Manager','Deputy Manager')
    """, (fiscal_year), as_dict=1)

    # 🔥 Filter till current month & sum
    for r in mtd_records:
        dept = r.department
        m = r.month

        if m == current_month:
            if dept not in data:
                data[dept] = {
                    "hod_target": 0,
                    "hod_achieved": 0,
                    "mtd_target": 0,
                    "mtd_achieved": 0
                }

            data[dept]["mtd_target"] += r.ct_point or 0
            data[dept]["mtd_achieved"] += r.achieved_point or 0

    return data

@frappe.whitelist()
def get_employees_with_targets(department, fiscal_year=None):

    filters = {
        "department": department
    }
    if not fiscal_year:
        fiscal_year = frappe.db.get_value(
            "Fiscal Year",
            {"year_start_date": ["<=", nowdate()], "year_end_date": [">=", nowdate()]},
            "name"
        )
    if fiscal_year:
        filters["custom_fiscal_year"] = fiscal_year


    data = frappe.db.sql("""
            SELECT DISTINCT 
                tm.employee,
                e.employee_name,
                e.image,
                e.designation
            FROM `tabTarget Manager` tm
            INNER JOIN `tabEmployee` e 
                ON e.name = tm.employee
            WHERE e.department = %s
            AND e.status = 'Active'
            AND tm.custom_fiscal_year = %s
        """, (department, fiscal_year), as_dict=1)

    return data


@frappe.whitelist()
def get_employee_targets(employee):

    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        {"year_start_date": ["<=", nowdate()], "year_end_date": [">=", nowdate()]},
        "name"
    )

    targets = frappe.get_all(
        "Target Manager",
        filters={
            "employee": employee,
            "fiscal_year": fiscal_year
        },
        fields=[
            "name",
            "target_type",
            "target_value",
            "achieved_value"
        ]
    )

    return targets

@frappe.whitelist()
def get_mtd_data(employee):

    from frappe.utils import nowdate, now_datetime

    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        {"year_start_date": ["<=", nowdate()], "year_end_date": [">=", nowdate()]},
        "name"
    )

    # 🔥 Your mapping (April → March order)
    mapping_months = {
        'Apr': 12, 'May': 11, 'Jun': 10, 'Jul': 9,
        'Aug': 8, 'Sep': 7, 'Oct': 6, 'Nov': 5,
        'Dec': 4, 'Jan': 3, 'Feb': 2, 'Mar': 1
    }

    # Current month (convert to short)
    current_month_full = now_datetime().strftime("%b")  # Apr, May...
    current_order = mapping_months.get(current_month_full, 0)

    data = frappe.db.sql("""
        SELECT 
            tc.month,
            tc.ct,
            tc.achieved,
            tc.ct_yta
        FROM `tabTarget Child` tc
        INNER JOIN `tabTarget Manager` tm 
            ON tc.parent = tm.name
        WHERE tm.employee = %s
        AND tm.custom_fiscal_year = %s
    """, (employee, fiscal_year), as_dict=1)

    # 🔥 Filter + Sort
    filtered = []
    for d in data:
        m = d.get("month")
        order = mapping_months.get(m, 0)

        # include only till current month
        if order >= current_order:
            d["order"] = order
            filtered.append(d)

    # sort in correct FY order
    filtered.sort(key=lambda x: x["order"], reverse=True)

    return filtered

@frappe.whitelist()
def get_company_points(employee, fiscal_year=None):

    if not fiscal_year:
        from frappe.utils import nowdate
        fiscal_year = frappe.db.get_value(
            "Fiscal Year",
            {"year_start_date": ["<=", nowdate()], "year_end_date": [">=", nowdate()]},
            "name"
        )

    # Get employee company
    company = frappe.db.get_value("Employee", employee, "company")

    # 🔥 GET POINT VALUE
    point_value = frappe.db.get_value(
        "Company Point and value",
        {
            "parent": company,
            "fiscal_year": fiscal_year
        },
        "value"
    ) or 1

    # YTD totals
    result = frappe.db.sql("""
        SELECT 
            tm.total_ct,
            tm.total_ach,
            td.revised_ct
        FROM
            (SELECT 
                SUM(annual_ct) as total_ct,
                SUM(total_ct_achieved) as total_ach
            FROM `tabTarget Manager`
            WHERE employee = %s
            AND custom_fiscal_year = %s
            ) tm
        LEFT JOIN
            (SELECT 
                SUM(revised_ct) as revised_ct
            FROM `tabTarget Child` tc
            INNER JOIN `tabTarget Manager` tmm 
                ON tc.parent = tmm.name
            WHERE tmm.employee = %s
            AND tmm.custom_fiscal_year = %s
            ) td
        ON 1=1
    """, (employee, fiscal_year, employee, fiscal_year), as_dict=1)

    data = result[0] if result else {}

    return {
        "total_ct": data.get("total_ct") or 0,
        "total_ach": data.get("total_ach") or 0,
        "revised_ct": data.get("revised_ct") or 0,
        "point_value": point_value
    }