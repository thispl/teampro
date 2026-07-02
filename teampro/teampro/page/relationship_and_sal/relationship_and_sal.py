import frappe
import json
from frappe.utils import getdate, nowdate
import urllib.parse 

@frappe.whitelist()
def get_order_booking(from_date=None, to_date=None, employee_ids=None, services=None):

    import json
    from frappe.utils import getdate, today

    # -------------------------
    # PARSE INPUTS
    # -------------------------
    if employee_ids:
        employee_ids = json.loads(employee_ids)
    else:
        employee_ids = []

    if services:
        services = json.loads(services)
    else:
        services = []

    # -------------------------
    # DEFAULT EMPLOYEES
    # -------------------------
    # if not/rn {"total": 0, "average": 0}

    # -------------------------
    # DEFAULT ACCOUNT MANAGERS
    # -------------------------

    if not employee_ids:

        sales_orders = frappe.get_all(

                        "Sales Order",

                        filters={
                            "docstatus": 1
                        },

                        fields=["account_manager"]

                    )

        employee_ids = [
            d.account_manager
            for d in sales_orders
            if d.account_manager
        ]

    # -------------------------
    # DATE LOGIC
    # -------------------------
    today_date = getdate(today())

    if from_date and to_date:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    else:
        from_date = getdate(f"{today_date.year if today_date.month >= 4 else today_date.year - 1}-04-01")
        to_date = today_date

    month_count = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 1

    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        "account_manager IN %(employee_ids)s",
        "docstatus = 1",
        "status NOT IN ('On Hold', 'Cancelled', 'Closed')",
        "transaction_date >= %(from_date)s",
        "transaction_date <= %(to_date)s"
    ]

    if services:
        conditions.append("service IN %(services)s")

    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT SUM(base_net_total)
        FROM `tabSales Order`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {
        "employee_ids": tuple(employee_ids),
        "services": tuple(services) if services else None,
        "from_date": from_date,
        "to_date": to_date
    })

    total = result[0][0] or 0
    average = round(total / month_count) if month_count > 0 else 0
    frappe.errprint(f"Fiscal Month Count:  Total: {total}, Average: {average}")
    return {
        "total": total,
        "average": average
    }



@frappe.whitelist()
def get_turnover(from_date=None, to_date=None, employee_ids=None, services=None):

    import json
    from frappe.utils import getdate, today

    # -------------------------
    # PARSE INPUTS
    # -------------------------
    if employee_ids:
        employee_ids = json.loads(employee_ids)
    else:
        employee_ids = []

    if services:
        services = json.loads(services)
    else:
        services = []

    # -------------------------
    # DEFAULT ACCOUNT MANAGERS
    # -------------------------

    if not employee_ids:

        sales_invoice = frappe.get_all(

            "Sales Invoice",

            filters={
                "docstatus": 1
            },

            fields=["account_manager"]

        )

        employee_ids = [
            d.account_manager
            for d in sales_invoice
            if d.account_manager
        ]

    if not employee_ids:
        return {"total": 0, "average": 0}

    # -------------------------
    # DATE LOGIC (same as OB)
    # -------------------------
    today_date = getdate(today())

    if from_date and to_date:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    else:
        from_date = getdate(f"{today_date.year if today_date.month >= 4 else today_date.year - 1}-04-01")
        to_date = today_date

    month_count = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 1

    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        "account_manager IN %(employee_ids)s",
        "docstatus = 1",
        "status NOT IN ('Return', 'Credit Note Issued', 'Cancelled')",
        # "posting_date >= %(from_date)s",
        # "posting_date <= %(to_date)s"
    ]

    if services:
        conditions.append("services IN %(services)s")

    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT SUM(base_net_total)
        FROM `tabSales Invoice`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {
        "employee_ids": tuple(employee_ids),
        "services": tuple(services) if services else None,
        "from_date": from_date,
        "to_date": to_date
    })

    total = result[0][0] or 0
    average = round(total / month_count) if month_count > 0 else 0

    return {
        "total": total,
        "average": average
    }


@frappe.whitelist()
def get_collection_value(from_date=None, to_date=None, employee_ids=None, services=None):

    import json
    from frappe.utils import getdate, today

    # -------------------------
    # PARSE INPUTS
    # -------------------------
    if employee_ids:
        employee_ids = json.loads(employee_ids)
    else:
        employee_ids = []

    if services:
        services = json.loads(services)
    else:
        services = []

    today_date = getdate(today())

    if from_date and to_date:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    else:
        from_date = getdate(f"{today_date.year if today_date.month >= 4 else today_date.year - 1}-04-01")
        to_date = today_date

    month_count = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 1

    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        "pe.company = 'TEAMPRO Food Products'",
        "pe.payment_type = 'Receive'",
        "pe.docstatus = 1",
        "per.service = 'TFP'",
        "pe.posting_date >= %(from_date)s",
        "pe.posting_date <= %(to_date)s"
    ]

    if employee_ids:
        conditions.append("pe.owner IN %(employee_ids)s")

    if services:
        conditions.append("per.service IN %(services)s")

    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT SUM(pe.paid_amount)
        FROM `tabPayment Entry` pe
        INNER JOIN `tabPayment Entry Reference` per ON per.parent = pe.name
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {
        "employee_ids": tuple(employee_ids),
        "services": tuple(services) if services else None,
        "from_date": from_date,
        "to_date": to_date
    })

    total = result[0][0] or 0
    average = round(total / month_count) if month_count > 0 else 0

    return {
        "total": total,
        "average": average
    }

@frappe.whitelist()
def rs_receivable(from_date=None, to_date=None, employee_ids=None, services=None):

    import json
    from frappe.utils import getdate, today


    # -------------------------
    # PARSE EMPLOYEE FILTER
    # -------------------------
    if employee_ids:
        try:
            employee_ids = json.loads(employee_ids)
        except:
            employee_ids = []
    else:
        employee_ids = []

    # -------------------------
    # PARSE SERVICE FILTER (ONLY ONCE)
    # -------------------------
    if services:
        try:
            services = json.loads(services)
        except:
            services = []
    else:
        services = []

    # -------------------------
    # GET EMPLOYEE EMAILS
    # -------------------------
    if employee_ids:
        rs_employees = frappe.get_all(
            "Employee",
            filters={"user_id": ["in", employee_ids]},
            fields=["user_id"]
        )
        rs_emails = [emp.user_id for emp in rs_employees if emp.user_id]

    else:

        invoices = frappe.get_all(

            "Sales Invoice",

            filters={
                "docstatus": 1
            },

            fields=["account_manager"]

        )

        rs_emails = [
            d.account_manager
            for d in invoices
            if d.account_manager
        ]

    if not rs_emails:
        return {"total": 0, "average": 0}


    # -------------------------
    # DATE LOGIC
    # -------------------------
    today_date = getdate(today())

    if from_date and to_date:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    else:
        from_date = getdate(f"{today_date.year if today_date.month >= 4 else today_date.year - 1}-04-01")
        to_date = today_date

    month_count = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 1

    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        "account_manager IN %(rs_emails)s",
        "docstatus = 1",
        "outstanding_amount > 0",
        # "posting_date >= %(from_date)s",
        # "posting_date <= %(to_date)s"
    ]

    if employee_ids:
        conditions.append("account_manager IN %(rs_emails)s")

    if services:
        conditions.append("services IN %(services)s")

    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT SUM(base_grand_total)
        FROM `tabSales Invoice`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {
        "rs_emails": tuple(rs_emails),
        "services": tuple(services) if services else None,
        "from_date": from_date,
        "to_date": to_date
    })

    total = result[0][0] or 0
    average = round(total / month_count) if month_count > 0 else 0

    return {
        "total": total,
        "average": average
    }


@frappe.whitelist()
def rs_to_bill_value(from_date=None, to_date=None, employee_ids=None, services=None):

    import json
    from frappe.utils import getdate, today


    # -------------------------
    # PARSE EMPLOYEE IDS (USER_ID)
    # -------------------------
    if employee_ids:
        try:
            employee_ids = json.loads(employee_ids)
        except:
            employee_ids = []
    else:
        employee_ids = []

    # -------------------------
    # PARSE SERVICES
    # -------------------------
    if services:
        try:
            services = json.loads(services)
        except:
            services = []
    else:
        services = []

    # -------------------------
    # GET EMPLOYEES (USER_ID ONLY)
    # -------------------------
    if employee_ids:
        rs_employees = frappe.get_all(
            "Employee",
            filters={"user_id": ["in", employee_ids]},
            fields=["user_id"]
        )
        rs_emails = [e.user_id for e in rs_employees if e.user_id]
    else:

        invoices = frappe.get_all(

            "Sales Order",

            filters={
                "docstatus": 1
            },

            fields=["account_manager"]

        )

        rs_emails = [
            d.account_manager
            for d in invoices
            if d.account_manager
        ]

    

    if not rs_emails:
        return {"total": 0, "average": 0}


    # -------------------------
    # DATE LOGIC
    # -------------------------
    today_date = getdate(today())

    if from_date and to_date:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    else:
        from_date = getdate(
            f"{today_date.year if today_date.month >= 4 else today_date.year - 1}-04-01"
        )
        to_date = today_date

    month_count = (
        (to_date.year - from_date.year) * 12 +
        (to_date.month - from_date.month) + 1
    )

    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        "account_manager IN %(rs_emails)s",
        "docstatus = 1",
        "status IN ('To Bill', 'To Deliver and Bill')",
        "transaction_date >= %(from_date)s",
        "transaction_date <= %(to_date)s"
    ]

    if employee_ids:
        conditions.append("account_manager IN %(rs_emails)s")
    if services:
        conditions.append("service IN %(services)s")

    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT SUM(base_grand_total)
        FROM `tabSales Order`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {
        "rs_emails": tuple(rs_emails),
        "services": tuple(services) if services else None,
        "from_date": from_date,
        "to_date": to_date
    })

    total = result[0][0] or 0
    average = round(total / month_count) if month_count > 0 else 0

    return {
        "total": total,
        "average": average
    }


@frappe.whitelist()
def oppcount(employee_ids=None, services=None):

    import json
    from frappe.utils import getdate, today

    # -------------------------
    # PARSE EMPLOYEE IDS
    # -------------------------
    if employee_ids:
        try:
            employee_ids = json.loads(employee_ids)
        except:
            employee_ids = []
    else:
        employee_ids = []

    # -------------------------
    # PARSE SERVICES
    # -------------------------
    if services:
        try:
            services = json.loads(services)
        except:
            services = []
    else:
        services = []

    # -------------------------
    # GET EMPLOYEES
    # -------------------------
    if employee_ids:
        rs_employees = frappe.get_all(
            "Employee",
            filters={"user_id": ["in", employee_ids]},
            fields=["user_id"]
        )
        rs_emails = [e.user_id for e in rs_employees if e.user_id]
    else:

        invoices = frappe.get_all(

            "Opportunity",

            filters={
                "status": ["not in", ["Lost", "Closed"]]
            },

            # fields=["distinct lead_owner"]
            fields=["lead_owner"],
            distinct=True

        )

        rs_emails = [
            d.lead_owner
            for d in invoices
            if d.lead_owner
        ]


    if not rs_emails:
        return {"count": 0, "amount": 0}

    
    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        "lead_owner IN %(rs_emails)s",
        "status NOT IN ('Lost', 'Closed')"
    ]

    if employee_ids:
        conditions.append("lead_owner IN %(rs_emails)s")

    if services:
        conditions.append("service IN %(services)s")

    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT 
            COUNT(name) as count,
            SUM(opportunity_amount) as amount
        FROM `tabOpportunity`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {
        "rs_emails": tuple(rs_emails),
        "services": tuple(services) if services else None,
    }, as_dict=True)

    return {
        "count": result[0].count or 0,
        "amount": result[0].amount or 0
    }

@frappe.whitelist()
def rs_to_deliver_bill_value(from_date=None, to_date=None, employee_ids=None, services=None):

    import json
    from frappe.utils import getdate, today


    # -------------------------
    # PARSE EMPLOYEE IDS
    # -------------------------
    if employee_ids:
        try:
            employee_ids = json.loads(employee_ids)
        except:
            employee_ids = []
    else:
        employee_ids = []

    # -------------------------
    # PARSE SERVICES
    # -------------------------
    if services:
        try:
            services = json.loads(services)
        except:
            services = []
    else:
        services = []

    # -------------------------
    # GET EMPLOYEES (USER_ID ONLY)
    # -------------------------
    if employee_ids:
        rs_employees = frappe.get_all(
            "Employee",
            filters={"user_id": ["in", employee_ids]},
            fields=["user_id"]
        )
    else:
        rs_employees = frappe.get_all(
            "Employee",
            filters={
                "department": ["in", [
                    "R&S - IT Services - THIS",
                    "R&S - THIS",
                    "R&S - TGT",
                    "R&S - HR Service - THIS",
                    "TFP - R&S  - TFP"
                ]],
                "status": "Active"
            },
            fields=["user_id"]
        )

    rs_emails = [e.user_id for e in rs_employees if e.user_id]

    if not rs_emails:
        return {"total": 0, "average": 0}

    # -------------------------
    # DATE LOGIC (SAME STYLE AS TO BILL)
    # -------------------------
    today_date = getdate(today())

    if from_date and to_date:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    else:
        from_date = getdate(
            f"{today_date.year if today_date.month >= 4 else today_date.year - 1}-04-01"
        )
        to_date = today_date

    month_count = (
        (to_date.year - from_date.year) * 12 +
        (to_date.month - from_date.month) + 1
    )

    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        "account_manager IN %(rs_emails)s",
        "docstatus = 1",
        "status = 'To Deliver and Bill'",
        "transaction_date >= %(from_date)s",
        "transaction_date <= %(to_date)s"
    ]

    if employee_ids:
        conditions.append("account_manager IN %(rs_emails)s")
    if services:
        conditions.append("service IN %(services)s")  

    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT SUM(base_grand_total)
        FROM `tabSales Order`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {
        "rs_emails": tuple(rs_emails),
        "services": tuple(services) if services else None,
        "from_date": from_date,
        "to_date": to_date
    })

    total = result[0][0] or 0
    average = round(total / month_count) if month_count > 0 else 0

    return {
        "total": total,
        "average": average
    }


@frappe.whitelist()
def rs_tobill_table():
    from frappe.utils import today, getdate, nowdate
    from datetime import datetime
    from frappe.utils import today, getdate, nowdate, fmt_money
    from datetime import datetime

    rs_employees = frappe.get_all("Employee",
        filters={
            "department": ["in",[
				"R&S - IT Services - THIS",
				"R&S - THIS",
				"R&S - TGT",
				"R&S - HR Service - THIS",
				"TFP - R&S  - TFP"
				]],
            "status": "Active",
        },
        fields=["user_id"]
    )

    rs_emails = [emp.user_id for emp in rs_employees if emp.user_id]

    if not rs_emails:
        return 0

    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today()], "year_end_date": [">=", today()]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )
    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    data = frappe.db.sql("""
        SELECT name, customer, base_grand_total, transaction_date
        FROM `tabSales Order`
        WHERE docstatus = 1
            AND status = 'To Bill'
            AND account_manager IN %(rs_emails)s
            AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
            AND base_grand_total > 0
        ORDER BY transaction_date
    """, {
        "from_date": from_date,
        "to_date": to_date,
        "rs_emails": tuple(rs_emails) 
        }, as_dict=True)

    html = """
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
        name_style = "color: red;" if age > 30 else ""
        total_outstanding += row.base_grand_total or 0
        html += f"""
            <tr style="{row_style}">
                <td style="text-align: center;">{idx}</td>
                <td style="white-space: nowrap;">{row.customer}</td>
                <td style='text-align:right;'>{frappe.utils.fmt_money(row.base_grand_total)}</td>
                <td style='text-align:right;'>{age}</td>
                <td style="white-space: nowrap;"><a href="/app/sales-order/{ row.name }" target="_blank" style="{name_style}">{ row.name }</a></td>
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
    # html += "</tbody></table></div>"

    return html

@frappe.whitelist()
def rs_receivable_table(from_date=None, to_date=None):
    from frappe.utils import today, getdate, nowdate, fmt_money
    from datetime import datetime

    rs_employees = frappe.get_all("Employee",
        filters={
            "department": ["in",[
				"R&S - IT Services - THIS",
				"R&S - THIS",
				"R&S - TGT",
				"R&S - HR Service - THIS",
				"TFP - R&S  - TFP"
				]],
            "status": "Active",
        },
        fields=["user_id"]
    )

    rs_emails = [emp.user_id for emp in rs_employees if emp.user_id]

    if not rs_emails:
        return 0

    conditions = [
        "account_manager IN %(rs_emails)s",
        "docstatus = 1",
        "outstanding_amount > 0"
    ]

    if from_date:
        conditions.append("posting_date >= %(from_date)s")
    if to_date:
        conditions.append("posting_date <= %(to_date)s")

    condition_str = " AND ".join(conditions)    

    query = f"""
        SELECT name, customer, outstanding_amount, posting_date
        FROM `tabSales Invoice`
        WHERE {condition_str}
        ORDER BY posting_date
    """
    result = frappe.db.sql(query, {
        "from_date": from_date,
        "to_date": to_date,
        "rs_emails": tuple(rs_emails)
    }, as_dict=True)

    total_outstanding = 0
    today_date = getdate(nowdate())

    html = """
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

    for idx, row in enumerate(result, 1):
        age = (today_date - getdate(row.posting_date)).days
        row_style = "color: red;" if age > 30 else ""
        name_style = "color: red;" if age > 30 else ""
        total_outstanding += row.outstanding_amount or 0

        html += f"""
            <tr style="{row_style}">
                <td style="text-align: center;">{idx}</td>
                <td style="white-space: nowrap;">{row.customer}</td>
                <td style='text-align:right;'>{fmt_money(row.outstanding_amount)}</td>
                <td style='text-align:right;'>{age}</td>
                <td style="white-space: nowrap;"><a href="/app/sales-invoice/{ row.name }" target="_blank" style="{name_style}">{ row.name }</a></td>
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
def get_service_card_data():

    import frappe

    data = frappe.db.sql("""

        SELECT
            custom_sales_follow_up AS sales_follow_up,
            service,
            COUNT(name) AS total

        FROM `tabOpportunity`

        WHERE
            custom_sales_follow_up IS NOT NULL
            AND custom_sales_follow_up != ''
            AND service IS NOT NULL
            AND service != ''
            AND status NOT IN ('Lost', 'Closed')

        GROUP BY service

        ORDER BY service

    """, as_dict=True)

    return data



@frappe.whitelist()
def get_sfp_status_cards():
    import frappe

    customers = frappe.db.get_all(
        "Sales Follow Up",
        filters={"status": "Converted" , "follow_up_to": "Customer" , "party_name": ["is", "set"]},
        pluck="party_name"
    )

    customers = list(set(customers))  


    active_customers = 0
    inactive_customers = 0

    for customer in customers:
        project_exists = frappe.db.exists(
            "Project",
            {
                "customer": customer,
                "status": "Open"
            }
        )

        so_exists = frappe.db.exists(
            "Sales Order",
            {
                "customer": customer,
                "status": ["not in", ["Closed", "Cancelled","Completed"]]
            }
        )

        if project_exists or so_exists:
            active_customers += 1
        else:
            inactive_customers += 1


    interested = frappe.db.count("Sales Follow Up", {"status": "Interested", "docstatus": ["!=", 2]})
    replied = frappe.db.count("Sales Follow Up", {"status": "Replied", "docstatus": ["!=", 2]})
    open_count = frappe.db.count("Sales Follow Up", {"status": "Open", "docstatus": ["!=", 2]})
    lead = frappe.db.count("Sales Follow Up", {"status": "Lead", "docstatus": ["!=", 2]})

    return {
        "active_customer": active_customers,
        "inactive_customer": inactive_customers,
        "interested": interested,
        "replied": replied,
        "open": open_count,
        "lead": lead
    }


@frappe.whitelist()
def get_active_inactive_customer_report():

    import frappe

    sfp_list = frappe.db.sql("""

        SELECT
            sfp.name,
            sfp.party_name,
            sfp.account_manager_lead_owner,
            sfp.organization_name,
            sfp.sfp_territory,
            sfp.remarks,
            sfp.service,
            emp.short_code

        FROM `tabSales Follow Up` sfp

        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = sfp.account_manager_lead_owner

        WHERE
            sfp.status = 'Converted'
            AND sfp.follow_up_to = 'Customer'
            AND sfp.party_name IS NOT NULL
            AND sfp.party_name != ''

        ORDER BY
            CASE
                WHEN emp.short_code IS NULL OR emp.short_code = '' THEN 1
                ELSE 0
            END,
            emp.short_code ASC

    """, as_dict=True)

    unique_customers = {}

    for row in sfp_list:

        customer = row.party_name

        if customer not in unique_customers:
            unique_customers[customer] = row


    active_html = '''
        <table style="border-collapse:collapse; width:100%; table-layout:fixed;border:1px solid #ffffff;">

            <tr style="background:#002060; color:white; position:sticky; top:0; z-index:1;">
                <td style="text-align:center; font-weight:bold; width:60px; border:1px solid #ffffff;">Sr</td>
                <td style="text-align:center; font-weight:bold; width:100px; border:1px solid #ffffff;">Sales Follow Up ID</td>
                <td style="text-align:center; font-weight:bold; width:80px; border:1px solid #ffffff;">AM</td>
                <td style="text-align:center; font-weight:bold; width:70px; border:1px solid #ffffff;">SVC</td>
                <td style="text-align:center; font-weight:bold; width:180px; border:1px solid #ffffff;">Project & SO ID</td>
                <td style="text-align:center; font-weight:bold; width:220px; ">Organization</td>
                <td style="text-align:center; font-weight:bold; width:140px; border:1px solid #ffffff;">Territory</td>
                <td style="text-align:center; font-weight:bold; width:350px; border:1px solid #ffffff;">Remark</td>
            </tr>
    '''

    inactive_html = '''
        <table style="border-collapse:collapse; width:100%;border:1px solid #ffffff;">

            <tr style="background:#002060; color:white; position:sticky; top:0; z-index:1;">
                <td style="text-align:center; font-weight:bold; width:60px; border:1px solid #ffffff;">Sr</td>
                <td style="text-align:center; font-weight:bold; border:1px solid #ffffff;">Sales Follow Up ID</td>
                <td style="text-align:center; font-weight:bold; border:1px solid #ffffff;">AM</td>
                <td style="text-align:center; font-weight:bold; border:1px solid #ffffff;">SVC</td>
                <td style="text-align:center; font-weight:bold; border:1px solid #ffffff;">Organization</td>
                <td style="text-align:center; font-weight:bold; border:1px solid #ffffff;">Territory</td>
                <td style="text-align:center; font-weight:bold; border:1px solid #ffffff;">Remark</td>
            </tr>
    '''

    active_row = 0
    inactive_row = 0

    for customer, row in unique_customers.items():
        employee = frappe.db.get_value(
            "Employee",
            {"user_id": row.account_manager_lead_owner},
            ["short_code"],
            as_dict=True
        )

        am_shortcode = employee.short_code if employee else ""
        project = frappe.db.get_value(
            "Project",
            {
                "customer": customer,
                "status": "Open"
            },
            "name"
        )

        sales_order = frappe.db.get_value(
            "Sales Order",
            {
                "customer": customer,
                "status": ["not in", ["Closed", "Cancelled","Completed"]]
            },
            "name"
        )

        project_so = project if project else sales_order

        if project or sales_order:

            active_row += 1

            bg = "#ffffff" if active_row % 2 != 0 else "#e7e6ec"

            active_html += f'''
            <tr style="background:{bg};border:1px solid #ffffff;">
                <td style="text-align:center; width:60px; border:1px solid #ffffff">
                    {active_row}
                </td>
                <td style="text-align:center; width:100px; border:1px solid #ffffff"><a href="/app/sales-follow-up/{row.name}" target="_blank">{row.name or ""}</a></td>
                <td style="text-align:center; width:80px; border:1px solid #ffffff">{am_shortcode}</td>
                <td style="text-align:center; width:90px; border:1px solid #ffffff">{row.service or ""}</td>
                <td style="text-align:left; width:180px; border:1px solid #ffffff"><a href="/app/{'project' if project else 'sales-order'}/{project_so}" target="_blank">{project_so or ""}</a></td>
                <td style="text-align:left; width:220px; border:1px solid #ffffff">{row.organization_name or ""}</td>
                <td style="text-align:center; width:140px; border:1px solid #ffffff">{row.sfp_territory or ""}</td>
                <td style="text-align:left;width:350px;padding-left:10px; border:1px solid #ffffff">{row.remarks or ""}</td>
            </tr>
            '''

        else:

            inactive_row += 1

            bg = "#ffffff" if inactive_row % 2 != 0 else "#e7e6ec"

            inactive_html += f'''
            <tr style="background:{bg};border:1px solid #ffffff;">
                <td style="text-align:center; width:60px; border:1px solid #ffffff">
                    {inactive_row}
                </td>
                <td style="text-align:center; width:140px; border:1px solid #ffffff"><a href="/app/sales-follow-up/{row.name}" target="_blank">{row.name or ""}</a></td>
                <td style="text-align:center; width:80px; border:1px solid #ffffff">{am_shortcode}</td>
                <td style="text-align:center; width:70px; border:1px solid #ffffff">{row.service or ""}</td>
                <td style="text-align:left; width:220px; border:1px solid #ffffff">{row.organization_name or ""}</td>
                <td style="text-align:center; width:140px; border:1px solid #ffffff">{row.sfp_territory or ""}</td>
                <td style="text-align:left;width:350px;padding-left:10px; border:1px solid #ffffff">{row.remarks or ""}</td>
            </tr>
            '''

    active_html += '</table>'
    inactive_html += '</table>'

    return {
        "active_html": active_html,
        "inactive_html": inactive_html
    }


@frappe.whitelist()
def download_active_customer_report():

    import frappe
    import openpyxl

    from io import BytesIO
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Active Customer Report"

    headers = [
        "Sr",
        "Sales Follow Up ID",
        "AM",
        "SVC",
        "Project & SO ID",
        "Organization",
        "Territory",
        "Remark"
    ]

    ws.append(headers)

    header_fill = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    sfp_list = frappe.db.sql("""

        SELECT
            sfp.name,
            sfp.party_name,
            sfp.account_manager_lead_owner,
            sfp.organization_name,
            sfp.sfp_territory,
            sfp.remarks,
            sfp.service,
            emp.short_code

        FROM `tabSales Follow Up` sfp

        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = sfp.account_manager_lead_owner

        WHERE
            sfp.status = 'Converted'
            AND sfp.follow_up_to = 'Customer'
            AND sfp.party_name IS NOT NULL
            AND sfp.party_name != ''

        ORDER BY
            CASE
                WHEN emp.short_code IS NULL OR emp.short_code = '' THEN 1
                ELSE 0
            END,
            emp.short_code ASC

    """, as_dict=True)


    unique_customers = {}

    for row in sfp_list:

        customer = row.party_name

        if customer not in unique_customers:
            unique_customers[customer] = row

    row_no = 2
    sr_no = 1

    for customer, row in unique_customers.items():

        project = frappe.db.get_value(
            "Project",
            {
                "customer": customer,
                "status": "Open"
            },
            "name"
        )

        sales_order = frappe.db.get_value(
            "Sales Order",
            {
                "customer": customer,
                "status": ["not in", ["Closed", "Cancelled"]]
            },
            "name"
        )

        if not (project or sales_order):
            continue

        employee = frappe.db.get_value(
            "Employee",
            {"user_id": row.account_manager_lead_owner},
            ["short_code"],
            as_dict=True
        )

        am_shortcode = employee.short_code if employee else ""

        project_so = project if project else sales_order

        ws.append([
            sr_no,
            row.name or "",
            am_shortcode,
            row.service or "",
            project_so or "",
            row.organization_name or "",
            row.sfp_territory or "",
            row.remarks or ""
        ])

        row_fill = "FFFFFF" if row_no % 2 == 0 else "E7E6EC"

        for cell in ws[row_no]:
            cell.fill = PatternFill(
                start_color=row_fill,
                end_color=row_fill,
                fill_type="solid"
            )

            alignment_type = "center" if cell.column in [1, 2] else "left"

            cell.alignment = Alignment(
                horizontal=alignment_type,
                vertical="center",
                wrap_text=True
            )

            cell.border = thin_border

        row_no += 1
        sr_no += 1

    column_widths = {
        "A": 10,
        "B": 28,
        "B": 12,
        "D": 10,
        "E": 28,
        "F": 35,
        "G": 20,
        "H": 50
    }

    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    frappe.response['filename'] = 'Active Customer Report.xlsx'
    frappe.response['filecontent'] = output.getvalue()
    frappe.response['type'] = 'binary'


@frappe.whitelist()
def download_inactive_customer_report():

    import frappe
    import openpyxl

    from io import BytesIO
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inactive Customer Report"

    headers = [
        "Sr",
        "Sales Follow Up ID",
        "AM",
        "SVC",
        "Organization",
        "Territory",
        "Remark"
    ]

    ws.append(headers)

    header_fill = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    sfp_list = frappe.db.sql("""

        SELECT
            sfp.name,
            sfp.party_name,
            sfp.account_manager_lead_owner,
            sfp.organization_name,
            sfp.sfp_territory,
            sfp.remarks,
            sfp.service,
            emp.short_code

        FROM `tabSales Follow Up` sfp

        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = sfp.account_manager_lead_owner

        WHERE
            sfp.status = 'Converted'
            AND sfp.follow_up_to = 'Customer'
            AND sfp.party_name IS NOT NULL
            AND sfp.party_name != ''

        ORDER BY
            CASE
                WHEN emp.short_code IS NULL OR emp.short_code = '' THEN 1
                ELSE 0
            END,
            emp.short_code ASC

    """, as_dict=True)


    unique_customers = {}

    for row in sfp_list:

        customer = row.party_name

        if customer not in unique_customers:
            unique_customers[customer] = row

    row_no = 2
    s_no=1

    for customer, row in unique_customers.items():

        project = frappe.db.get_value(
            "Project",
            {
                "customer": customer,
                "status": "Open"
            },
            "name"
        )

        sales_order = frappe.db.get_value(
            "Sales Order",
            {
                "customer": customer,
                "status": ["not in", ["Closed", "Cancelled"]]
            },
            "name"
        )

        if project or sales_order:
            continue

        employee = frappe.db.get_value(
            "Employee",
            {"user_id": row.account_manager_lead_owner},
            ["short_code"],
            as_dict=True
        )

        am_shortcode = employee.short_code if employee else ""

        ws.append([
            s_no,
            row.name or "",
            am_shortcode,
            row.service or "",
            row.organization_name or "",
            row.sfp_territory or "",
            row.remarks or ""
        ])

        row_fill = "FFFFFF" if row_no % 2 == 0 else "E7E6EC"

        for cell in ws[row_no]:
            cell.fill = PatternFill(
                start_color=row_fill,
                end_color=row_fill,
                fill_type="solid"
            )

            alignment_type = "center" if cell.column in [1, 2] else "left"

            cell.alignment = Alignment(
                horizontal=alignment_type,
                vertical="center",
                wrap_text=True
            )

            cell.border = thin_border

        row_no += 1
        s_no+=1

    column_widths = {
        "A": 10,
        "B": 28,
        "B": 12,
        "D": 10,
        "E": 28,
        "F": 35,
        "G": 20,
        "H": 50
    }

    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    frappe.response['filename'] = 'Inactive Customer Report.xlsx'
    frappe.response['filecontent'] = output.getvalue()
    frappe.response['type'] = 'binary'

@frappe.whitelist()
def opportunity_details(owner=None, services=None, weeks=None):
    from frappe.utils import getdate, nowdate, formatdate
    import json

    try:
        owner = json.loads(owner) if owner else []
        services = json.loads(services) if services else []
        weeks = json.loads(weeks) if weeks else []
    except:
        owner, services, weeks = [], [], []

    weeks = [w.strip().upper().replace(" ", "") for w in weeks]

    # -------------------------
    # GET USER IDS
    # -------------------------
    if owner:
        rs_user_ids = owner
    else:
        rs_employees = frappe.get_all("Employee", filters={
            "status": "Active"
        }, fields=["user_id"])

        rs_user_ids = [emp.user_id for emp in rs_employees if emp.user_id]

    if not rs_user_ids and not owner:
        lead_owner_condition = "1=1"
    else:
        lead_owner_condition = "lead_owner IN %(user_ids)s"

    # -------------------------
    # CONDITIONS
    # -------------------------
    conditions = [
        lead_owner_condition,
        "opp.docstatus != 2",
        "opp.status NOT IN ('Lost','Closed','Converted')",
        "IFNULL(opp.service, '') != ''"
    ]

    if services:
        conditions.append("opp.service IN %(services)s")

    if weeks:
        conditions.append("opp.expected_week IN %(weeks)s")

    condition_str = " AND ".join(conditions)

    # -------------------------
    # MAIN QUERY
    # -------------------------
    query = f"""
        SELECT 
            opp.name,
            opp.lead_owner,
            emp.short_code,
            opp.transaction_date,
            opp.opportunity_from,
            opp.service,
            opp.status,
            opp.organization_name,
            opp.opportunity_amount,
            opp.probability,
            opp.expected_closing,
            opp.remark,
            opp.expected_week,
            opp.custom_type,
            opp.territory,
            opp.custom_sales_follow_up
        FROM `tabOpportunity` opp
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = opp.lead_owner
        WHERE {condition_str}
        ORDER BY emp.short_code ASC , opp.service
    """

    data = frappe.db.sql(query, {
        "user_ids": tuple(rs_user_ids),
        "services": tuple(services),
        "weeks": tuple(weeks)
    }, as_dict=True)

    # -------------------------
    # FETCH QUOTATIONS (BULK)
    # -------------------------
    opp_ids = [row.name for row in data]

    quote_map = {}

    if opp_ids:
        quotations = frappe.get_all(
            "Quotation",
            filters={
                "custom_opportunity": ["in", opp_ids],
                "status": ["not in", ["Lost", "Closed","Cancelled","Expired"]]
            },
            fields=["name", "custom_opportunity"]
        )

        for q in quotations:
            quote_map.setdefault(q.custom_opportunity, []).append(q.name)

    # -------------------------
    # HTML START
    # -------------------------
    html = """
    <div style='width: 100%; height: 340px; overflow-y: auto;'>
    <table class='table table-bordered' style='width:100%;min-width: 900px; border-collapse:collapse;'>
        <thead>
            <tr style='background:#002060; color:white; text-align:center;'>
                <th style="position: sticky; top: 0; background: #002060; width:40px;">Sr</th>
                <th style="position: sticky; top: 0; background: #002060; width:20px;">Opp. ID</th>
                <th style="position: sticky; top: 0; background: #002060; width:40px;">AM</th>
                <th style="position: sticky; top: 0; background: #002060; width:60px;">SVC</th>
                <th style="position: sticky; top: 0; background: #002060; width:60px;">From</th>
                <th style="position: sticky; top: 0; background: #002060; width:80px;">Status</th>
                <th style="position: sticky; top: 0; background: #002060; width:150px;">Organization</th>
                <th style="position: sticky; top: 0; background: #002060; width:100px;">Date</th>
                <th style="position: sticky; top: 0; background: #002060; width:40px;">Age</th>
                <th style="position: sticky; top: 0; background: #002060; width:70px;">Amount</th>
                <th style="position: sticky; top: 0; background: #002060; width:70px;">PB%</th>
                <th style="position: sticky; top: 0; background: #002060; width:100px;">ECD</th>
                <th style="position: sticky; top: 0; background: #002060; width:200px;">Remarks</th>
                <th style="position: sticky; top: 0; background: #002060; width:70px;">Type</th>
                <th style="position: sticky; top: 0; background: #002060; width:50px;">Territory</th>
                <th style="position: sticky; top: 0; background: #002060; width:90px;">Quo. ID</th>
            </tr>
        </thead>
        <tbody>
    """

    # -------------------------
    # ROW BUILD
    # -------------------------
    today = getdate(nowdate())

    for i, row in enumerate(data, 1):

        age = (today - getdate(row.transaction_date)).days if row.transaction_date else 0
        bg_color = "#ffffff" if i % 2 != 0 else "#e7e6ec"
        row_style = "color:red;" if age > 30 else ""

        quotes = quote_map.get(row.name, [])

        if quotes:
            quote_links = ", ".join([
                f'<a href="/app/quotation/{q}" target="_blank">{q}</a>'
                for q in quotes
            ])
        else:
            quote_links = "-"

        html += f"""
        <tr style="background:{bg_color};">
            <td style="text-align:center;">{i}</td>
     <td style="text-align: center; color: #000000; width: 110px; max-width: 110px; padding: 6px 4px; font-size: 12px; line-height: 1.3;">
    <a href="/desk/opportunity/{row.name}" 
       target="_blank" 
       style="color: #000000; 
              text-decoration: none; 
              display: inline-block; 
              max-width: 100px; 
              word-break: normal; 
              line-height: 1.3;">
        {row.name}
    </a>
    
    <div style="color: #000000; margin: 1px 0; font-weight: normal;">/</div>

    <a href="/desk/sales-follow-up/{row.custom_sales_follow_up}" 
       target="_blank" 
       style="color: #000000; 
              text-decoration: none;
              display: inline-block; 
              max-width: 100px;">
        {row.custom_sales_follow_up}
    </a>
</td>
            <td style="text-align:center;">{row.short_code or row.lead_owner or ''}</td>
            <td style="text-align:center;">{row.service or ''}</td>
            <td style="text-align:center;">{row.opportunity_from or ''}</td>
            <td style="text-align:center;">{row.status or ''}</td>
            <td>{row.organization_name or ''}</td>
            <td style="text-align:center;">{formatdate(row.transaction_date, "dd-MM-yyyy") if row.transaction_date else ''}</td>
            <td style="text-align:center;">
                <a href="/app/opportunity/{row.name}" target="_blank" style="{row_style}">
                    {age}
                </a>
            </td>
            <td style="text-align:center;">{row.opportunity_amount or ''}</td>
            <td style="text-align:center;">{row.probability or ''}</td>
            <td style="text-align:center;">{formatdate(row.expected_closing, "dd-MM-yyyy") if row.expected_closing else ''}</td>
            <td>{row.remark or ''}</td>
            <td>{row.custom_type or ''}</td>
            <td>{row.territory or ''}</td>
            <td style="text-align:center;">
                {quote_links}
            </td>
        </tr>
        """

    html += "</tbody></table></div>"

    return html


@frappe.whitelist()
def download_opportunity_excel(owner=None, services=None, weeks=None, opportunity_type=None):

    import frappe
    import json
    import openpyxl

    from io import BytesIO
    from frappe.utils import formatdate, getdate, nowdate
    from openpyxl.styles import Font, PatternFill, Alignment

    # 1. Parse all 4 incoming arguments safely within the validation block
    try:
        owner = json.loads(owner) if owner else []
        services = json.loads(services) if services else []
        weeks = json.loads(weeks) if weeks else []
        opportunity_type = json.loads(opportunity_type) if opportunity_type else []
    except:
        owner, services, weeks, opportunity_type = [], [], [], []

    weeks = [w.strip().upper().replace(" ", "") for w in weeks]

    # ---------------------------------
    # USER IDS
    # ---------------------------------
    if owner:
        rs_user_ids = owner
    else:
        rs_employees = frappe.get_all(
            "Employee",
            filters={"status": "Active"},
            fields=["user_id"]
        )
        rs_user_ids = [emp.user_id for emp in rs_employees if emp.user_id]

    if not rs_user_ids and not owner:
        lead_owner_condition = "1=1"
    else:
        lead_owner_condition = "lead_owner IN %(user_ids)s"

    # ---------------------------------
    # CONDITIONS ASSEMBLY
    # ---------------------------------
    conditions = [
        lead_owner_condition,
        "opp.docstatus != 2",
        "opp.status NOT IN ('Lost','Closed','Converted')",
        "IFNULL(opp.service, '') != ''"
    ]

    if services:
        conditions.append("opp.service IN %(services)s")

    if weeks:
        conditions.append("opp.expected_week IN %(weeks)s")

    if opportunity_type:
        conditions.append("opp.custom_type IN %(opportunity_type)s")

    condition_str = " AND ".join(conditions)

    # ---------------------------------
    # SQL QUERY
    # ---------------------------------
    query = f"""
        SELECT 
            opp.name,
            opp.lead_owner,
            emp.short_code,
            opp.transaction_date,
            opp.opportunity_from,
            opp.service,
            opp.status,
            opp.organization_name,
            opp.opportunity_amount,
            opp.probability,
            opp.expected_closing,
            opp.remark,
            opp.expected_week,
            opp.custom_type,
            opp.territory,
            opp.custom_sales_follow_up
        FROM `tabOpportunity` opp
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = opp.lead_owner
        WHERE {condition_str}
        ORDER BY emp.short_code ASC, opp.service
    """

    data = frappe.db.sql(query, {
        "user_ids": tuple(rs_user_ids),
        "services": tuple(services),
        "weeks": tuple(weeks),
        "opportunity_type": tuple(opportunity_type)
    }, as_dict=True)

    # ---------------------------------
    # QUOTATIONS
    # ---------------------------------
    opp_ids = [row.name for row in data]
    quote_map = {}

    if opp_ids:
        quotations = frappe.get_all(
            "Quotation",
            filters={
                "custom_opportunity": ["in", opp_ids],
                "status": ["not in", ["Lost", "Closed", "Cancelled", "Expired"]]
            },
            fields=["name", "custom_opportunity"]
        )
        for q in quotations:
            quote_map.setdefault(q.custom_opportunity, []).append(q.name)

    # ---------------------------------
    # EXCEL GENERATION
    # ---------------------------------
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Opportunity Details"

    headers = [
        "Sr", "Opp ID", "AM", "SVC", "From", "Status", "Organization", 
        "Date", "Age", "Amount", "PB%", "ECD", "Remarks", "Type", "Territory", "Quo ID"
    ]
    ws.append(headers)

    header_fill = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center")

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align

    # ---------------------------------
    # ROWS INJECTION
    # ---------------------------------
    today = getdate(nowdate())
    odd_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    even_fill = PatternFill(start_color="E7E6EC", end_color="E7E6EC", fill_type="solid")

    for idx, row in enumerate(data, start=1):
        age = (today - getdate(row.transaction_date)).days if row.transaction_date else 0
        quotes = quote_map.get(row.name, [])
        quote_links = ", ".join(quotes) if quotes else "-"

        # 🌟 FIXED: Format Opp ID cleanly across multiple lines inside a single cell variable
        opp_id_raw = row.name or ""
        sfp_id_raw = row.custom_sales_follow_up or ""
        
        if len(opp_id_raw) > 13:
            opp_formatted = f"{opp_id_raw[:13]}\n{opp_id_raw[13:]}"
        else:
            opp_formatted = opp_id_raw

        # Combine Opportunity, slash line break, and Sales Follow-Up data string
        combined_opp_cell = f"{opp_formatted}\n/\n{sfp_id_raw}" if sfp_id_raw else opp_formatted

        ws.append([
            idx,
            combined_opp_cell,  # 👈 Dynamic multi-line cell injected here
            row.short_code or row.lead_owner or "",
            row.service or "",
            row.opportunity_from or "",
            row.status or "",
            row.organization_name or "",
            formatdate(row.transaction_date, "dd-MM-yyyy") if row.transaction_date else "",
            age,
            row.opportunity_amount or "",
            row.probability or "",
            formatdate(row.expected_closing, "dd-MM-yyyy") if row.expected_closing else "",
            row.remark or "",
            row.custom_type or "",
            row.territory or "",
            quote_links
        ])

        fill = odd_fill if idx % 2 != 0 else even_fill
        for cell in ws[idx + 1]:
            cell.fill = fill
            cell.alignment = Alignment(horizontal="left", vertical="center")

    # 🌟 FIXED: Iterate down column B (Opp ID) and force alignment wrap_text to True
    for excel_row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for cell in excel_row:
            cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

    # Column Width Auto-Fit Calculation
    for column_cells in ws.columns:
        # Avoid breaking sizes based on cells containing long newline layout breaks
        length = max(len(max(str(cell.value or " ").split('\n'), key=len)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 5

    xlsx_file = BytesIO()
    wb.save(xlsx_file)

    frappe.response["filename"] = "Opportunity_Details.xlsx"
    frappe.response["filecontent"] = xlsx_file.getvalue()
    frappe.response["type"] = "download"

@frappe.whitelist()
def get_opportunity_logo():
    service_names = ["IT-SW", "IT-IS", "TFP", "REC-I","BCS"]
    service_images = []

    for service in service_names:
        service_data = frappe.db.get_value("Services", {"name": service}, ["logo"], as_dict=True)
        if service_data and service_data.get("logo"):
            # Get full URL for web rendering
            image_url =service_data.get("logo")
        else:
            # Optional: fallback image if not found
            image_url = ""
        service_images.append({"name": service, "image": image_url})
    html = '''
              <div style="display:flex; gap:30px; margin-top:10px; margin-bottom:15px; flex-wrap:wrap; justify-content:flex-start;">
    '''
    for s in service_images:
        html += f'''
            <div style="display:flex;  flex-direction:column; align-items:center;">
                <img src="{s['image']}" alt="{s['name']}"
                     style="height:50px; width:50px; border-radius:50%; object-fit:contain;">
                <span style="font-size:12px; margin-top:5px; color:#555;">{s['name']}</span>
            </div>
        '''

   
    html += '''
        </div> 

    
    '''

    return html

# NON COLLAPSABLE CODE
@frappe.whitelist()
def quotation_details(owner=None, services=None, from_date=None, to_date=None):
    import json
    from frappe.utils import getdate, nowdate

    try:
        owner = json.loads(owner) if owner else []
        services = json.loads(services) if services else [] 
    except:
        owner, services = [], []

    if owner:
        rs_user_ids = owner
    else:
        rs_employees = frappe.get_all("Employee", filters={
            "department": ["in", [
                "R&S - IT Services - THIS",
                "R&S - THIS",
                "R&S - TGT",
                "R&S - HR Service - THIS",
                "TFP - R&S  - TFP"
            ]],
            "status": "Active"
        }, fields=["user_id"])
        rs_user_ids = [emp.user_id for emp in rs_employees if emp.user_id]

    if not rs_user_ids and not owner:
        acc_owner_condition = "1=1"
    else:
        acc_owner_condition = "q.account_manager IN %(user_ids)s"

    conditions = [
        acc_owner_condition,
        "q.docstatus != 2",
        "q.status NOT IN ('Lost','Closed')"
    ]

    if services:
        conditions.append("q.service_name IN %(services)s")

    condition_str = " AND ".join(conditions)

    query = f"""
        SELECT 
            q.quotation_to,
            q.customer_name,
            q.account_manager,
            emp.short_code,
            q.service_name,
            q.status,
            q.grand_total
        FROM `tabQuotation` q
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = q.account_manager
        WHERE {condition_str}
        ORDER BY q.account_manager, q.service_name
    """ 

    result = frappe.db.sql(query, {
        "user_ids": tuple(rs_user_ids),
        "services": tuple(services),
        "from_date": from_date,
        "to_date": to_date
    }, as_dict=True)

    html_table = """
    <div style='max-height: 340px; min-width: 500px;'>
        <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
            <thead>
                <tr style="background: #002060; color: white; text-align: center;">
                    <th style="position: sticky; top: 0; background: #002060; z-index: 1;">S.NO</th>
                    <th style="position: sticky; top: 0; background: #002060; z-index: 1;">Account Manager</th>
                    <th style="position: sticky; top: 0; background: #002060; z-index: 1;">Service</th>
                    <th style="position: sticky; top: 0; background: #002060; z-index: 1;">Quotation To</th>
                    <th style="position: sticky; top: 0; background: #002060; z-index: 1;">Customer</th>
                    <th style="position: sticky; top: 0; background: #002060; z-index: 1;">Status</th>
                    <th style="position: sticky; top: 0; background: #002060; z-index: 1;">Grand Total</th>
                </tr>
            </thead>
            <tbody>
    """


    for i, row in enumerate(result, 1):
        bg_color = "#ffffff" if i % 2 != 0 else "#e7e6ec"
        html_table += f"""
            <tr style="background:{bg_color}; color:black;">
                <td style="text-align: center; vertical-align: middle;">{i}</td>
                <td style="text-align: center; vertical-align: middle;">{row.short_code or row.account_manager or ''}</td>
                <td style="text-align: center; vertical-align: middle;">{row.service_name or ''}</td>
                <td style="text-align: center; vertical-align: middle;">{row.quotation_to or ''}</td>
                <td>{row.customer_name or ''}</td>
                <td style="text-align: center; vertical-align: middle;">{row.status or ''}</td>
                <td style="text-align: center; vertical-align: middle;">{row.grand_total or ''}</td>
            </tr>
        """

    html_table += "</tbody></table></div>"

    return html_table


@frappe.whitelist()
def appointment_details(owner=None, services=None, from_date=None, to_date=None):
    from frappe.utils import getdate, nowdate
    import json
    from collections import defaultdict
    from frappe.utils import formatdate

    try:
        owner = json.loads(owner) if owner else []
        services = json.loads(services) if services else []
    except:
        owner, services = [], []

    if owner:
        rs_user_ids = owner
    else:
        rs_employees = frappe.get_all("Employee", filters={
            "status": "Active"
        }, fields=["user_id"])
        rs_user_ids = [emp.user_id for emp in rs_employees if emp.user_id]

    if not rs_user_ids and not owner:
        acc_owner_condition = "1=1"
    else:
        acc_owner_condition = "f.account_manager_lead_owner IN %(user_ids)s"

    conditions = [
        acc_owner_condition,
        "f.app_status IN ('Scheduled')"
    ]

    if services:
        conditions.append("f.service IN %(services)s")
    if from_date:
        conditions.append("f.appointment_fixed_on >= %(from_date)s")
    if to_date:
        conditions.append("f.appointment_fixed_on <= %(to_date)s")
    
    condition_str = " AND ".join(conditions)

    query = f"""
        SELECT 
            f.name,
            f.account_manager_lead_owner,
            emp.short_code,
            f.service,
            f.party_from,
            f.organization_name,
            f.territory,
            f.appointment_fixed_on,
            f.custom_appointment_mode
        FROM `tabSales Follow Up` f
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = f.account_manager_lead_owner
        WHERE {condition_str}
        ORDER BY emp.short_code ASC, f.appointment_fixed_on DESC
    """

    data = frappe.db.sql(query, {
        "user_ids": tuple(rs_user_ids),
        "services": tuple(services),
        "from_date": from_date,
        "to_date": to_date
    }, as_dict=True)

    # Group data by lead_owner
    grouped_data = defaultdict(list)
    today = getdate(nowdate())
    for row in data:
        grouped_data[row.account_manager_lead_owner or "Unknown"].append(row)

    # Build HTML
    html = """
        <div style='height:300px; overflow-y:auto;'>
        <table class='table table-bordered'
            style='width:100%; border-collapse:collapse; table-layout:fixed;'>

        <thead>
        <tr style="background:#002060; color:white; text-align:center;">
            <th style="width:30px; position:sticky; top:0; z-index:10; background:#002060;">Sr</th>
            <th style="width:90px; position:sticky; top:0; z-index:10; background:#002060;">ID</th>
            <th style="width:30px; position:sticky; top:0; z-index:10; background:#002060;">AM</th>
            <th style="width:40px; position:sticky; top:0; z-index:10; background:#002060;">SVC</th>
            <th style="width:70px; position:sticky; top:0; z-index:10; background:#002060;">Follow Up From</th>
            <th style="width:150px; position:sticky; top:0; z-index:10; background:#002060;">Organization Name</th>
            <th style="width:70px; position:sticky; top:0; z-index:10; background:#002060;">Territory</th>
            <th style="width:90px; position:sticky; top:0; z-index:10; background:#002060;">Appo. On</th>
            <th style="width:90px; position:sticky; top:0; z-index:10; background:#002060;">Appo. Mode</th>
        </tr>
        </thead>

        <tbody>
        """

    s_no = 1
    today = getdate(nowdate())

    for row in data:

        bg_color = "#ffffff" if s_no % 2 != 0 else "#e7e6ec"

        html += f"""
        <tr style="background:{bg_color};">
            <td style="text-align:center;">{s_no}</td>
            <td style="text-align:center;">
                <a href="/app/sales-follow-up/{row.name}" target="_blank">
                    {row.name or ""}
                </a>
            </td>
            <td>{row.short_code or row.account_manager_lead_owner or ''}</td>
            <td>{row.service or ''}</td>
            <td>{row.party_from or ''}</td>
            <td>{row.organization_name or ''}</td>
            <td>{row.territory or ''}</td>
            <td>{formatdate(row.appointment_fixed_on) if row.appointment_fixed_on else ''}</td>
            <td>{row.custom_appointment_mode or ''}</td>
        </tr>
        """
        s_no += 1
    html += f'''    
    </tbody>
    </table>
    </div>

    '''

    return html


@frappe.whitelist()
def download_appointment_excel(
    owner=None,
    services=None,
    from_date=None,
    to_date=None
):

    import frappe
    import json
    import openpyxl

    from io import BytesIO
    from frappe.utils import formatdate
    from openpyxl.styles import Font, PatternFill, Alignment

    try:
        owner = json.loads(owner) if owner else []
        services = json.loads(services) if services else []

    except:
        owner, services = [], []

    if owner:
        rs_user_ids = owner

    else:
        rs_employees = frappe.get_all(
            "Employee",
            filters={"status": "Active"},
            fields=["user_id"]
        )

        rs_user_ids = [
            emp.user_id for emp in rs_employees
            if emp.user_id
        ]

    if not rs_user_ids and not owner:
        acc_owner_condition = "1=1"

    else:
        acc_owner_condition = \
            "f.account_manager_lead_owner IN %(user_ids)s"

    conditions = [
        acc_owner_condition,
        "f.app_status IN ('Scheduled')"
    ]

    if services:
        conditions.append("f.service IN %(services)s")

    if from_date:
        conditions.append(
            "f.appointment_fixed_on >= %(from_date)s"
        )

    if to_date:
        conditions.append(
            "f.appointment_fixed_on <= %(to_date)s"
        )

    condition_str = " AND ".join(conditions)

    query = f"""
        SELECT 
            f.account_manager_lead_owner,
            emp.short_code,
            f.service,
            f.party_from,
            f.organization_name,
            f.territory,
            f.appointment_fixed_on,
            f.custom_appointment_mode
        FROM `tabSales Follow Up` f
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = f.account_manager_lead_owner
        WHERE {condition_str}
        ORDER BY emp.short_code ASC,
                 f.appointment_fixed_on DESC
    """

    data = frappe.db.sql(query, {
        "user_ids": tuple(rs_user_ids),
        "services": tuple(services),
        "from_date": from_date,
        "to_date": to_date
    }, as_dict=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Appointment Details"

    headers = [
        "Sr",
        "AM",
        "SVC",
        "Follow Up From",
        "Organization Name",
        "Territory",
        "Appo. On",
        "Appo. Mode"
    ]

    ws.append(headers)

    # HEADER STYLE

    header_fill = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )

    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    for cell in ws[1]:

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    odd_fill = PatternFill(
        start_color="FFFFFF",
        end_color="FFFFFF",
        fill_type="solid"
    )

    even_fill = PatternFill(
        start_color="E7E6EC",
        end_color="E7E6EC",
        fill_type="solid"
    )

    s_no = 1

    for row in data:

        ws.append([
            s_no,
            row.short_code or
            row.account_manager_lead_owner or "",
            row.service or "",
            row.party_from or "",
            row.organization_name or "",
            row.territory or "",
            formatdate(row.appointment_fixed_on)
                if row.appointment_fixed_on else "",
            row.custom_appointment_mode or ""
        ])

        fill = odd_fill if s_no % 2 != 0 else even_fill

        for cell in ws[s_no + 1]:

            cell.fill = fill

            cell.alignment = Alignment(
                horizontal="left",
                vertical="center"
            )

        s_no += 1

    for column_cells in ws.columns:

        length = max(
            len(str(cell.value or ""))
            for cell in column_cells
        )

        ws.column_dimensions[
            column_cells[0].column_letter
        ].width = length + 5

    xlsx_file = BytesIO()

    wb.save(xlsx_file)

    frappe.response["filename"] = \
        "Appointment_Details.xlsx"

    frappe.response["filecontent"] = \
        xlsx_file.getvalue()

    frappe.response["type"] = "download"



@frappe.whitelist()
def todo_details(owner=None, services=None):
    from frappe.utils import getdate, nowdate
    import json
    from collections import defaultdict
    from frappe.utils import formatdate

    try:
        owner = json.loads(owner) if owner else []
        services = json.loads(services) if services else []
    except:
        owner, services = [], []

    if owner:
        rs_user_ids = owner
    else:
        rs_employees = frappe.get_all("Employee", filters={
            "status": "Active"
        }, fields=["user_id"])
        rs_user_ids = [emp.user_id for emp in rs_employees if emp.user_id]

    if not rs_user_ids and not owner:
        acc_owner_condition = "1=1"
    else:
        acc_owner_condition = "t.allocated_to IN %(user_ids)s"

    conditions = [
        acc_owner_condition,
        "t.docstatus != 2",
        "t.status NOT IN ('Cancelled','Closed')"
    ]

    if services:
        conditions.append("t.custom_todo_type IN %(services)s")
    condition_str = " AND ".join(conditions)

    query = f"""
        SELECT 
            t.name,
            t.allocated_to,
            emp.short_code,
            t.custom_subject,
            t.custom_todo_type,
            t.created_on,
            t.status
        FROM `tabToDo` t
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = t.allocated_to
        WHERE {condition_str}
        ORDER BY emp.short_code ASC
    """


    data = frappe.db.sql(query, {
        "user_ids": tuple(rs_user_ids),
        "services": tuple(services)
    }, as_dict=True)

    # Group data by lead_owner
    grouped_data = defaultdict(list)
    today = getdate(nowdate())
    for row in data:
        grouped_data[row.allocated_to or "Unknown"].append(row)
        
    # Build HTML
    
    html = """
        <div style='height:300px; overflow-y:auto;'>
        <table class='table table-bordered' style='width:100%; table-layout: fixed; border-collapse:collapse;'>

        <thead>
        <tr style="background:#002060; color:white; text-align:center;">
            <th style="width:30px; position:sticky; top:0; z-index:10; background:#002060;">Sr</th>
            <th style="width:30px; position:sticky; top:0; z-index:10; background:#002060;">AM</th>
            <th style="width:50px; position:sticky; top:0; z-index:10; background:#002060;">Status</th>
            <th style="width:160px; position:sticky; top:0; z-index:10; background:#002060;">Subject</th>
            <th style="width:60px; position:sticky; top:0; z-index:10; background:#002060;">ToDo Type</th>
            <th style="width:70px; position:sticky; top:0; z-index:10; background:#002060;">Cre. On</th>
            <th style="width:30px; position:sticky; top:0; z-index:10; background:#002060;">Age</th>
        </tr>
        </thead>

        <tbody>
        """

    s_no = 1
    today = getdate(nowdate())

    for row in data:
        age = (today - getdate(row.created_on)).days
        row_style = "color:red;" if age > 30 else ""
        bg_color = "#ffffff" if s_no % 2 != 0 else "#e7e6ec"
            
        html += f"""
        <tr style="background:{bg_color}; color:black;">
            <td style="text-align: center; vertical-align: middle;">{s_no}</td>
            <td style="text-align: center; vertical-align: middle;">{row.short_code or row.allocated_to or ''}</td>
            <td style="text-align: center; vertical-align: middle;">{row.status or ''}</td>
            <td>{row.custom_subject or ''}</td>
            <td style="text-align: center; vertical-align: middle;">{row.custom_todo_type or ''}</td>
            <td style="text-align: center; vertical-align: middle;">
            {formatdate(row.created_on) if row.created_on else ''}</td>
            <td style="text-align: center; vertical-align: middle;">
                <a href="/app/todo/{row.name}" target="_blank" style="{row_style}">
                    {age}
                </a>
            </td>
        </tr>
        """
        s_no += 1

    html += f'''
    </tbody>
    </table>
    </div>

    '''
    return html


@frappe.whitelist()
def fup_details(call_status=None,
                Lfrom_date=None, Lto_date=None,
                Nfrom_date=None, Nto_date=None,
                owner=None, service=None):

    import frappe
    import json
    from frappe.utils import nowdate
    import urllib.parse
    from frappe.utils import add_days, nowdate

    today = nowdate()
    yesterday = add_days(today, -1)
    # today = nowdate()

    owner = json.loads(owner) if owner else []
    service = json.loads(service) if service else []

    rs_employees = frappe.get_all("Employee",
        filters={"status": "Active"},
        fields=["user_id"]
    )

    default_user_ids = [emp.user_id for emp in rs_employees if emp.user_id]
    user_ids = owner if owner else default_user_ids

    query = """
        SELECT 
            f.next_contact_by,
            emp.short_code,
            f.status,

            SUM(CASE WHEN DATE(f.next_contact_date) = %(today)s THEN 1 ELSE 0 END) AS A,
            SUM(CASE WHEN DATE(f.last_contacted_on) = %(today)s THEN 1 ELSE 0 END) AS B,
            COUNT(*) AS C,
            SUM(
                CASE
                    WHEN DATE(f.next_contact_date) < %(today)s
                    THEN 1
                    ELSE 0
                END
            ) AS D

        FROM `tabSales Follow Up` f
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = f.next_contact_by

        WHERE f.docstatus != 2
        AND f.status IN ('Lead', 'Open', 'Opportunity', 'Converted', 'Interested', 'Replied')
        AND f.next_contact_by IS NOT NULL
        AND f.next_contact_by != ''

        GROUP BY f.next_contact_by, f.status
    """

    raw_data = frappe.db.sql(query, {
        "today": today
    }, as_dict=True)

    result = {}

    for row in raw_data:
        status = (row.status or "").lower()
        short = row.short_code or "NA"
        # short = row.next_contact_by or "NA"

        if short not in result:
            result[short] = {
                "lead": {}, "open": {}, "replied": {},
                "opportunity": {}, "interested": {}, "converted": {}
            }

        result[short][status] = {
            "A": int(row.A or 0),
            "B": int(row.B or 0),
            "C": int(row.C or 0),
            "D": int(row.D or 0),
            "user_id": row.next_contact_by
        }

    result = dict(sorted(result.items(), key=lambda x: str(x[0] or "").lower()))

    totals = {
        "lead": {"A":0,"B":0,"C":0,"D":0},
        "open": {"A":0,"B":0,"C":0,"D":0},
        "replied": {"A":0,"B":0,"C":0,"D":0},
        "opportunity": {"A":0,"B":0,"C":0,"D":0},
        "interested": {"A":0,"B":0,"C":0,"D":0},
        "converted": {"A":0,"B":0,"C":0,"D":0}
    }

    totals_all = {"A":0,"B":0,"C":0,"D":0}

    
    def cell(val, user=None, status=None):
        if not val:
            return """
            <td>-</td>
            <td>-</td>
            """

        A = int(val.get('A',0))
        B = int(val.get('B',0))
        C = int(val.get('C',0))
        D = int(val.get('D',0))
        def make_link(count, color, key):

            if count == 0:
                return f"""<span style="color:{color};">-</span>"""

            base_url = "/app/sales-follow-up?"

            params = {
                "status1": json.dumps(["!=", "Do Not Contact"])
            }

            # Status Filter
            if status:
                params["status"] = status.title()
            else:
                params["status"] = json.dumps([
                    "in",
                    [
                        "Lead",
                        "Open",
                        "Opportunity",
                        "Converted",
                        "Interested",
                        "Replied"
                    ]
                ])

            if user:
                params["next_contact_by"] = val.get("user_id")

            # A
            if key == "A":
                params["next_contact_date"] = today

            # B
            elif key == "B":
                params["last_contacted_on"] = today

            # C
            elif key == "C":
                pass

            # D
            # elif key == "D":
            #     params["next_contact_date"] = json.dumps(["<", today])

            elif key == "D":
                params["next_contact_date"] = json.dumps(
                    ["between", ["1900-01-01", yesterday]]
                )

            query_string = urllib.parse.urlencode(params)

            url = base_url + query_string

            return f"""
            <a href="{url}" target="_blank" style="color:{color}; text-decoration:none;">
                {count}
            </a>
            """

        
        # def make_link(count, color, key):

        #     if count == 0:
        #         return f"""<span style="color:{color};">-</span>"""

        #     base_url = "/app/sales-follow-up?"

        #     params = {
        #         "status1": json.dumps(["!=", "Do Not Contact"])
        #     }

        #     if status:
        #         params["status"] = status.title()

        #     if user:
        #         params["next_contact_by"] = val.get("user_id")

        #     # A
        #     if key == "A":
        #         params["next_contact_date"] = today

        #     # B
        #     elif key == "B":
        #         params["last_contacted_on"] = today

        #     # C
        #     elif key == "C":
        #         pass

        #     # D
        #     elif key == "D":
        #         params["next_contact_date"] = json.dumps(["<", today])

        #     query_string = urllib.parse.urlencode(params)

        #     url = base_url + query_string

        #     return f"""
        #     <a href="{url}" target="_blank" style="color:{color}; text-decoration:none;">
        #         {count}
        #     </a>
        #     """

        dsm = f"""
        {make_link(A, 'orange', 'A')}
        <span style="color:black;"> / </span>
        {make_link(B, 'green', 'B')}
        """

        all_val = f"""
        {make_link(C, 'blue', 'C')}
        <span style="color:black;"> / </span>
        {make_link(D, 'red', 'D')}
        """

        return f"""
        <td>{dsm}</td>
        <td>{all_val}</td>
        """

    html = """

    <style>
        .hover-table tbody tr:hover {
            background-color: #ffe6b3 !important;
            cursor: pointer;
        }

        .hover-table tbody tr {
            transition: background 0.2s ease;
        }

        .hover-table thead tr:nth-child(1) th {
            position: sticky;
            top: 0;
            background: #002060;
            color: white;
            z-index: 3;
        }

        .hover-table thead tr:nth-child(2) th {
            position: sticky;
            top: 35px;  
            background: #002060;
            color: white;
            z-index: 3;
        }
    </style>

    <div style="width:100%; max-height:70vh; overflow:auto;">

    <table class='table table-bordered hover-table'
        style='width:100%; min-width:1400px; border-collapse:collapse; text-align:center;'>

    <thead>

    <tr>
        <th rowspan="1" style="
                width:180px;
                position:sticky;
                left:0;
                top:0;
                background:#002060;
                color:white;
                z-index:5;
                white-space:nowrap;
            ">
                Service based
            </th>

        <th colspan="2">Lead</th>
        <th colspan="2">Open</th>
        <th colspan="2">Replied</th>
        <th colspan="2">Opportunity</th>
        <th colspan="2">Interested</th>
        <th colspan="2">Converted</th>

        <th colspan="2">Total</th>
    </tr>

    <tr>
    """
    html += """
    <th style="
        width:150px;
        min-width:90px;
        position:sticky;
        left:0;
        top:25;
        background:#002060;
        color:white;
        z-index:5;
    ">
        AM
    </th>
    """
    for i in range(6):
        html += "<th>DSM</th><th>ALL</th>"

    html += "<th>DSM</th><th>ALL</th>"

    html += "</tr></thead><tbody>"

    # -----------------------------
    # ROWS
    # -----------------------------
    row_index = 0

    for user, val in result.items():
        
        row_total = {"A":0,"B":0,"C":0,"D":0}
        row_index += 1

        bg = "#ffffff" if row_index % 2 else "#e7e6ec"

        html += f'''
            <tr style="background:{bg};">
            <td style="
                position:sticky;
                left:0;
                background:{bg};
                z-index:4;
                white-space:nowrap;
            ">
                {user}
            </td>
            '''

        for key in totals.keys():
            data = val.get(key)
            html += cell(data, user=user, status=key)

            if data:
                A = int(data.get("A",0))
                B = int(data.get("B",0))
                C = int(data.get("C",0))
                D = int(data.get("D",0))

                totals[key]["A"] += A
                totals[key]["B"] += B
                totals[key]["C"] += C
                totals[key]["D"] += D

                row_total["A"] += A
                row_total["B"] += B
                row_total["C"] += C
                row_total["D"] += D

        # TOTAL COLUMN (no "-")
        # html += f"""
        # <td style="font-weight:bold;">
        #     <span style="color:orange;">{row_total['A']}</span>
        #     <span style="color:black;"> / </span>
        #     <span style="color:green;">{row_total['B']}</span>
        # </td>

        # <td style="font-weight:bold;">
        #     <span style="color:blue;">{row_total['C']}</span>
        #     <span style="color:black;"> / </span>
        #     <span style="color:red;">{row_total['D']}</span>
        # </td>
        # """ 
        user_id = None
        for status_data in val.values():
            if isinstance(status_data, dict) and status_data.get("user_id"):
                user_id = status_data.get("user_id")
                break

        html += cell({
            "A": row_total["A"],
            "B": row_total["B"],
            "C": row_total["C"],
            "D": row_total["D"],
            "user_id": user_id
        }, user=user)

        totals_all["A"] += row_total["A"]
        totals_all["B"] += row_total["B"]
        totals_all["C"] += row_total["C"]
        totals_all["D"] += row_total["D"]

        html += "</tr>"

    # -----------------------------
    # TOTAL ROW
    # -----------------------------
    html += '<tr style="background:#c9c6e3; font-weight:bold;">'
    html += "<td>Total</td>"

    for key in totals.keys():
        html += cell(totals[key])

    # html += f"""
    # <td>
    #     <span style="color:orange;">{totals_all['A']}</span>
    #     <span style="color:black;"> / </span>
    #     <span style="color:green;">{totals_all['B']}</span>
    # </td>

    # <td>
    #     <span style="color:blue;">{totals_all['C']}</span>
    #     <span style="color:black;"> / </span>
    #     <span style="color:red;">{totals_all['D']}</span>
    # </td>
    # """
    html += cell({
            "A": totals_all["A"],
            "B": totals_all["B"],
            "C": totals_all["C"],
            "D": totals_all["D"]
        })

    html += "</tr>"

    html += "</tbody></table>"

    return html




@frappe.whitelist()
def fup_details_terr(call_status=None,
                Lfrom_date=None, Lto_date=None,
                Nfrom_date=None, Nto_date=None,
                owner=None, service=None):

    import frappe
    import json
    from frappe.utils import nowdate

    today = nowdate()

    owner = json.loads(owner) if owner else []
    service = json.loads(service) if service else []

    # -----------------------------
    # USERS
    # -----------------------------
    rs_employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["user_id", "short_code"]
    )

    default_user_ids = [e.user_id for e in rs_employees if e.user_id]
    user_ids = owner if owner else default_user_ids

    # -----------------------------
    # TERRITORIES
    # -----------------------------
    all_territories = frappe.get_all(
        "Sales Follow Up",
        filters={
            "sfp_territory": ["!=", ""],
        },
        fields=["sfp_territory as territory"],
        distinct = True
    )

    territories = sorted([t.territory for t in all_territories if t.territory])

    # -----------------------------
    # QUERY
    # -----------------------------
    query = """
        SELECT 
            f.next_contact_by,
            emp.short_code,
            f.sfp_territory,
            f.service,

            SUM(CASE WHEN DATE(f.next_contact_date) = %(today)s THEN 1 ELSE 0 END) AS A,
            SUM(CASE WHEN DATE(f.last_contacted_on) = %(today)s THEN 1 ELSE 0 END) AS B,
            COUNT(*) AS C,
            SUM(CASE WHEN DATE(f.next_contact_date) < %(today)s THEN 1 ELSE 0 END) AS D

        FROM `tabSales Follow Up` f
        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = f.next_contact_by

        WHERE f.docstatus != 2
        AND f.status IN ('Lead', 'Open', 'Opportunity', 'Converted', 'Interested', 'Replied')
        AND f.next_contact_by IS NOT NULL
        AND f.next_contact_by != ''

        GROUP BY f.next_contact_by, f.sfp_territory,f.service, emp.short_code
    """

    data = frappe.db.sql(query, {
        "user_ids": tuple(user_ids),
        "today": today
    }, as_dict=True)

    # -----------------------------
    # BUILD MATRIX
    # -----------------------------
    result = {}

    # -----------------------------
    # REMOVE EMPTY TERRITORIES
    # -----------------------------

    valid_territories = []

    for terr in territories:

        has_value = False

        for row in data:

            row_terr = row.sfp_territory or "Others"

            if row_terr != terr:
                continue

            A = int(row.A or 0)
            B = int(row.B or 0)
            C = int(row.C or 0)
            D = int(row.D or 0)

            # any one value > 0
            if A > 0 or B > 0 or C > 0 or D > 0:

                has_value = True
                break

        if has_value:
            valid_territories.append(terr)

    territories = valid_territories

    for row in data:
        user = row.next_contact_by
        terr = row.sfp_territory or "Others"
        short = row.short_code or "NA"

        if not short:
            continue

        service_val = row.service or "Others"

        if user not in result:
            result[user] = {
                "short_code": short,
                "services": {}
            }

        if service_val not in result[user]["services"]:
            result[user]["services"][service_val] = {}

        if terr not in result[user]["services"][service_val]:
            result[user]["services"][service_val][terr] = {
                "A": 0,
                "B": 0,
                "C": 0,
                "D": 0,
                "user_id": user,
                "territory": terr,
                "service": service_val
            }

        result[user]["services"][service_val][terr]["A"] += int(row.A or 0)
        result[user]["services"][service_val][terr]["B"] += int(row.B or 0)
        result[user]["services"][service_val][terr]["C"] += int(row.C or 0)
        result[user]["services"][service_val][terr]["D"] += int(row.D or 0)

    # -----------------------------
    # FORMAT CELL (4 COLUMN STYLE)
    # -----------------------------
    
    def cell(val):

        if not val:
            return """
            <td>-</td>
            <td>-</td>
            """

        A = int(val.get('A',0))
        B = int(val.get('B',0))
        C = int(val.get('C',0))
        D = int(val.get('D',0))

        user = val.get("user_id")
        territory = val.get("territory")
        service = val.get("service")

        def make_link(count, color, key):

            if count == 0:
                return f"""<span style="color:{color};">-</span>"""

            base_url = "/app/sales-follow-up?"

            params = {
                "status": json.dumps(["!=", "Do Not Contact"])
            }

            if user:
                params["next_contact_by"] = user

            if territory:
                params["sfp_territory"] = territory

            if service:
                params["service"] = service

            # A
            if key == "A":
                params["next_contact_date"] = today

            # B
            elif key == "B":
                params["last_contacted_on"] = today

            # C
            elif key == "C":
                pass

            # D
            elif key == "D":
                params["next_contact_date"] = json.dumps(["<", today])

            query_string = urllib.parse.urlencode(params)

            url = base_url + query_string

            return f"""
            <a href="{url}" target="_blank"
                style="color:{color}; text-decoration:none;">
                {count}
            </a>
            """

        
        dsm = f"""
        {make_link(A, 'orange', 'A')}
        <span style="color:black;"> / </span>
        {make_link(B, 'green', 'B')}
        """

        all_val = f"""
        {make_link(C, 'blue', 'C')}
        <span style="color:black;"> / </span>
        {make_link(D, 'red', 'D')}
        """

        return f"""
        <td>{dsm}</td>
        <td>{all_val}</td>
        """

    def total_cell(val, user_id=None, service_val=None):

        if not val:
            return "<td>-</td><td>-</td>"

        A = int(val.get('A', 0))
        B = int(val.get('B', 0))
        C = int(val.get('C', 0))
        D = int(val.get('D', 0))

        def make_link(count, color, key):
            if count == 0:
                return f'<span style="color:{color};">-</span>'

            base_url = "/app/sales-follow-up?"
            params = {"status": json.dumps(["!=", "Do Not Contact"])}

            if user_id:
                params["next_contact_by"] = user_id
            if service_val:
                params["service"] = service_val

            if key == "A":
                params["next_contact_date"] = today
            elif key == "B":
                params["last_contacted_on"] = today
            elif key == "D":
                params["filters"] = json.dumps([
                    ["next_contact_date", "<", today],
                    ["next_contact_date", "is", "set"]
                ])

            url = base_url + urllib.parse.urlencode(params)
            return f'<a href="{url}" target="_blank" style="color:{color}; text-decoration:none;">{count}</a>'

        dsm = f'{make_link(A, "orange", "A")} <span style="color:black;"> / </span> {make_link(B, "green", "B")}'
        all_val = f'{make_link(C, "blue", "C")} <span style="color:black;"> / </span> {make_link(D, "red", "D")}'

        return f"<td>{dsm}</td><td>{all_val}</td>"

    # -----------------------------
    # INIT TOTALS
    # -----------------------------
    totals = {}
    for terr in territories:
        totals[terr] = {"A":0,"B":0,"C":0,"D":0}

    # -----------------------------
    # HTML START
    # -----------------------------
    html = """
    <style>
        .hover-table tbody tr:hover {
            background-color: #ffe6b3 !important;
            cursor: pointer;
        }

        .hover-table tbody tr {
            transition: background 0.2s ease;
        }

        .hover-table thead tr:nth-child(1) th {
            position: sticky;
            top: 0;
            background: #002060;
            color: white;
            z-index: 3;
        }

        .hover-table thead tr:nth-child(2) th {
            position: sticky;
            top: 35px;  
            background: #002060;
            color: white;
            z-index: 3;
        }
    </style>


    <div style="width:100%; max-height:70vh; overflow:auto;">

    <table class='table table-bordered hover-table'
        style='width:100%; min-width:1400px;border-collapse:collapse; text-align:center;'>

    <thead>
        <tr>
            <th colspan="2" style="
                width:90px;
                position:sticky;
                left:0;
                top:0;
                background:#002060;
                color:white;
                z-index:5;
                white-space:nowrap;
            ">
                Territory & SVR
            </th>
            
    """

    for terr in territories:
        html += f"""
            <th colspan='2' style="white-space: nowrap;">
                {terr}
            </th>
        """

    html += """
        <th colspan="2">Total</th>
    """

    html += "</tr><tr>"
    html += """
        <th style="
            width:150px;
            min-width:90px;
            position:sticky;
            left:0;
            top:20;
            background:#002060;
            color:white;
            z-index:5;
        ">
            AM
        </th>
        """

    html += """
        <th style="
            width:150px;
            min-width:80px;
            position:sticky;
            left:80px;
            top:20;
            background:#002060;
            color:white;
            z-index:5;
        ">
            SVR
        </th>
        """
    for _ in territories:
        html += '<th style="width:150px; min-width:90px;">DSM</th>'
        html += '<th style="width:150px; min-width:90px;">ALL</th>'

    html += '<th style="width:180px; min-width:90px;">DSM</th>'
    html += '<th style="width:180px; min-width:90px;">ALL</th>'

    html += "</tr></thead><tbody>"

    # -----------------------------
    # ROWS
    # -----------------------------
    
    result = dict(sorted(
        result.items(),
        key=lambda x: str(x[1].get("short_code") or "").lower()
    ))
    row_index = 0

    
    for user, val in result.items():

        services = val.get("services", {})
        
        for service, terrs in services.items():

            row_total = {"A":0,"B":0,"C":0,"D":0}

            row_index += 1
            bg = "#ffffff" if row_index % 2 else "#e7e6ec"

            html += f'<tr style="background:{bg};">'

            html += f"""
            <td style="
                position:sticky;
                left:0;
                background:{bg};
                z-index:3;
                font-weight:500;
            ">
                {val.get("short_code") or "NA"}
            </td>
            """

            # SERVICE COLUMN
            html += f"""
            <td style="
                padding-left:15px;
                position:sticky;
                left:90px;
                background:{bg};
                z-index:3;
            ">
                {service}
            </td>
            """

            for terr in territories:

                data = terrs.get(terr)
                html += cell(data)

                if data:
                    A = data.get("A",0)
                    B = data.get("B",0)
                    C = data.get("C",0)
                    D = data.get("D",0)

                    totals[terr]["A"] += A
                    totals[terr]["B"] += B
                    totals[terr]["C"] += C
                    totals[terr]["D"] += D

                    row_total["A"] += A
                    row_total["B"] += B
                    row_total["C"] += C
                    row_total["D"] += D

            html += total_cell(row_total, user_id=user, service_val=service)

            html += "</tr>"

    # -----------------------------
    # TOTAL ROW
    # -----------------------------
    totals_all = {"A":0,"B":0,"C":0,"D":0}

    for terr in territories:
        totals_all["A"] += totals[terr]["A"]
        totals_all["B"] += totals[terr]["B"]
        totals_all["C"] += totals[terr]["C"]
        totals_all["D"] += totals[terr]["D"]
    
    html += """
    <tr style="background:#e0e6eb; font-weight:bold;">
        <td colspan="2" style="position:sticky; left:0; background:#e0e6eb;">
            Total
        </td>
    """

    for terr in territories:
        html += cell(totals[terr])

    html += f"""
        <td style="white-space:nowrap;">
            <span style="color:orange;">{int(totals_all['A'])}</span>
            <span style="color:black;"> / </span>
            <span style="color:green;">{int(totals_all['B'])}</span>
        </td>

        <td style="white-space:nowrap;">
            <span style="color:blue;">{int(totals_all['C'])}</span>
            <span style="color:black;"> / </span>
            <span style="color:red;">{int(totals_all['D'])}</span>
        </td>
        """

    html += "</tr>"

    html += "</tbody></table></div>"

    return html




@frappe.whitelist()
def download_fup_excel(owner=None, service=None):

    import frappe
    import json
    import openpyxl

    from io import BytesIO
    from openpyxl.styles import (
        Font,
        PatternFill,
        Alignment,
        Border,
        Side
    )
    from openpyxl.utils import get_column_letter

    owner = json.loads(owner) if owner else []
    service = json.loads(service) if service else []

    query = """
        SELECT 
            emp.short_code,
            f.status,

            SUM(CASE WHEN DATE(f.next_contact_date)=CURDATE() THEN 1 ELSE 0 END) AS A,
            SUM(CASE WHEN DATE(f.last_contacted_on)=CURDATE() THEN 1 ELSE 0 END) AS B,
            COUNT(*) AS C,
            SUM(CASE WHEN DATE(f.next_contact_date)<CURDATE() THEN 1 ELSE 0 END) AS D

        FROM `tabSales Follow Up` f

        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = f.next_contact_by

        WHERE f.docstatus != 2

        GROUP BY emp.short_code, f.status

        ORDER BY emp.short_code
    """

    raw_data = frappe.db.sql(query, as_dict=True)

    
    result = {}

    statuses = [
        "lead",
        "open",
        "replied",
        "opportunity",
        "interested",
        "converted"
    ]

    for row in raw_data:

        user = row.short_code or "NA"
        status = (row.status or "").lower()

        if user not in result:

            result[user] = {}

        result[user][status] = {
            "A": row.A or 0,
            "B": row.B or 0,
            "C": row.C or 0,
            "D": row.D or 0
        }

    wb = openpyxl.Workbook()
    ws = wb.active

    ws.title = "Service Followup"

    header_fill = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )

    white_font = Font(
        color="FFFFFF",
        bold=True
    )

    center = Alignment(
        horizontal="center",
        vertical="center"
    )

    thin = Side(style="thin")

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin
    )

    ws.merge_cells("A1:A2")

    ws["A1"] = "AM"

    headers = [
        "Lead",
        "Open",
        "Replied",
        "Opportunity",
        "Interested",
        "Converted",
        "Total"
    ]

    col = 2

    for head in headers:

        ws.merge_cells(
            start_row=1,
            start_column=col,
            end_row=1,
            end_column=col + 1
        )

        ws.cell(1, col).value = head

        ws.cell(2, col).value = "DSM"
        ws.cell(2, col + 1).value = "ALL"

        col += 2

    for row in ws.iter_rows(min_row=1, max_row=2):

        for cell in row:

            cell.fill = header_fill
            cell.font = white_font
            cell.alignment = center
            cell.border = border

    row_no = 3

    for user, values in result.items():

        col = 2

        total_A = total_B = total_C = total_D = 0

        row_values = []   

        ws.cell(row_no, 1).value = user

        for st in statuses:

            data = values.get(st, {})

            A = int(data.get("A", 0))
            B = int(data.get("B", 0))
            C = int(data.get("C", 0))
            D = int(data.get("D", 0))

            
            row_values += [A, B, C, D]

            
            total_A += A
            total_B += B
            total_C += C
            total_D += D

          
            dsm_val = f"{A if A else '-'} / {B if B else '-'}"
            all_val = f"{C if C else '-'} / {D if D else '-'}"

            ws.cell(row_no, col).value = dsm_val
            ws.cell(row_no, col + 1).value = all_val

            col += 2

        ws.cell(row_no, col).value = f"{total_A if total_A else '-'} / {total_B if total_B else '-'}"
        ws.cell(row_no, col + 1).value = f"{total_C if total_C else '-'} / {total_D if total_D else '-'}"

        row_values += [total_A, total_B, total_C, total_D]

        if all(v == 0 for v in row_values):

            ws.row_dimensions[row_no].hidden = True

        else:

            bg = "FFFFFF" if row_no % 2 else "FFFFFF"

            fill = PatternFill(
                start_color=bg,
                end_color=bg,
                fill_type="solid"
            )

            for c in ws[row_no]:

                c.fill = fill
                c.alignment = center
                c.border = border

        row_no += 1

    
    # ====================================================
    # WIDTH
    # ====================================================


    for col_idx in range(1, ws.max_column + 1):

        max_length = 0

        col_letter = get_column_letter(col_idx)

        for row in ws.iter_rows(min_col=col_idx, max_col=col_idx):

            for cell in row:

                if cell.value:

                    max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[col_letter].width = max_length + 5
    

    # ====================================================
    # FINAL TOTAL ROW
    # ====================================================

    ws.cell(row_no, 1).value = "TOTAL"

    ws.cell(row_no, 1).alignment = center

    grand_A = grand_B = grand_C = grand_D = 0

    col = 2

    for st in statuses:

        A = B = C = D = 0

        for user, values in result.items():

            data = values.get(st, {})

            A += int(data.get("A", 0))
            B += int(data.get("B", 0))
            C += int(data.get("C", 0))
            D += int(data.get("D", 0))

        grand_A += A
        grand_B += B
        grand_C += C
        grand_D += D

        ws.cell(row_no, col).value = f"{A if A else '-'} / {B if B else '-'}"
        ws.cell(row_no, col + 1).value = f"{C if C else '-'} / {D if D else '-'}"

        col += 2

    # TOTAL COLUMN
    ws.cell(row_no, col).value = f"{grand_A if grand_A else '-'} / {grand_B if grand_B else '-'}"
    ws.cell(row_no, col + 1).value = f"{grand_C if grand_C else '-'} / {grand_D if grand_D else '-'}"

    fill = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )

    for c in ws[row_no]:

        c.fill = fill
        c.font = white_font
        c.alignment = center
        c.border = border

    # ====================================================
    # DOWNLOAD
    # ====================================================

    xlsx_file = BytesIO()

    wb.save(xlsx_file)

    frappe.response["filename"] = "Service_Followup.xlsx"

    frappe.response["filecontent"] = xlsx_file.getvalue()

    frappe.response["type"] = "binary"


@frappe.whitelist()
def download_fup_terr_excel(owner=None, service=None):

    import frappe
    import json
    import openpyxl

    from io import BytesIO

    from openpyxl.styles import (
        Font,
        PatternFill,
        Alignment,
        Border,
        Side
    )

    from openpyxl.utils import get_column_letter

    owner = json.loads(owner) if owner else []
    service = json.loads(service) if service else []

    # =====================================================
    # QUERY
    # =====================================================

    query = """
        SELECT
            emp.short_code,
            f.service,
            f.sfp_territory,

            SUM(CASE WHEN DATE(f.next_contact_date)=CURDATE() THEN 1 ELSE 0 END) AS A,
            SUM(CASE WHEN DATE(f.last_contacted_on)=CURDATE() THEN 1 ELSE 0 END) AS B,
            COUNT(*) AS C,
            SUM(CASE WHEN DATE(f.next_contact_date)<CURDATE() THEN 1 ELSE 0 END) AS D

        FROM `tabSales Follow Up` f

        LEFT JOIN `tabEmployee` emp
            ON emp.user_id = f.next_contact_by

        WHERE f.docstatus != 2
        AND f.status IN (
            'Lead',
            'Open',
            'Opportunity',
            'Converted',
            'Interested',
            'Replied'
        )

        GROUP BY
            emp.short_code,
            f.service,
            f.sfp_territory

        ORDER BY emp.short_code
    """

    raw_data = frappe.db.sql(query, as_dict=True)

    # =====================================================
    # TERRITORIES
    # =====================================================

    territories = sorted(list(set([
        d.sfp_territory
        for d in raw_data
        if d.sfp_territory
    ])))

    # =====================================================
    # BUILD RESULT
    # =====================================================

    result = {}

    for row in raw_data:

        user = row.short_code or "NA"
        service_name = row.service or "Others"
        territory = row.sfp_territory or "Others"

        if user not in result:

            result[user] = {}

        if service_name not in result[user]:

            result[user][service_name] = {}

        result[user][service_name][territory] = {

            "A": int(row.A or 0),
            "B": int(row.B or 0),
            "C": int(row.C or 0),
            "D": int(row.D or 0)

        }

    # =====================================================
    # EXCEL
    # =====================================================

    wb = openpyxl.Workbook()

    ws = wb.active

    ws.title = "Territory Followup"

    # =====================================================
    # STYLES
    # =====================================================

    header_fill = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )

    white_font = Font(
        color="FFFFFF",
        bold=True
    )

    center = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )

    thin = Side(style="thin")

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin
    )

    total_fill = PatternFill(
        start_color="E0E6EB",
        end_color="E0E6EB",
        fill_type="solid"
    )

    # =====================================================
    # HEADER
    # =====================================================

    ws.merge_cells("A1:A2")
    ws.merge_cells("B1:B2")

    ws["A1"] = "AM"
    ws["B1"] = "SVR"

    col = 3

    for terr in territories:

        ws.merge_cells(
            start_row=1,
            start_column=col,
            end_row=1,
            end_column=col + 1
        )

        ws.cell(1, col).value = terr

        ws.cell(2, col).value = "DSM"
        ws.cell(2, col + 1).value = "ALL"

        col += 2

    # TOTAL
    ws.merge_cells(
        start_row=1,
        start_column=col,
        end_row=1,
        end_column=col + 1
    )

    ws.cell(1, col).value = "Total"

    ws.cell(2, col).value = "DSM"
    ws.cell(2, col + 1).value = "ALL"

    # =====================================================
    # HEADER STYLE
    # =====================================================

    for row in ws.iter_rows(min_row=1, max_row=2):

        for cell in row:

            cell.fill = header_fill
            cell.font = white_font
            cell.alignment = center
            cell.border = border

    # =====================================================
    # DATA
    # =====================================================

    row_no = 3

    visible_idx = 0

    totals = {}

    for terr in territories:

        totals[terr] = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0
        }

    result = dict(sorted(
        result.items(),
        key=lambda x: str(x[0]).lower()
    ))

    for user, services in result.items():

        for service_name, terrs in services.items():

            row_total = {
                "A": 0,
                "B": 0,
                "C": 0,
                "D": 0
            }

            row_values = []

            ws.cell(row_no, 1).value = user
            ws.cell(row_no, 2).value = service_name

            col = 3

            for terr in territories:

                data = terrs.get(terr, {})

                A = int(data.get("A", 0))
                B = int(data.get("B", 0))
                C = int(data.get("C", 0))
                D = int(data.get("D", 0))

                row_values += [A, B, C, D]

                row_total["A"] += A
                row_total["B"] += B
                row_total["C"] += C
                row_total["D"] += D

                totals[terr]["A"] += A
                totals[terr]["B"] += B
                totals[terr]["C"] += C
                totals[terr]["D"] += D

                dsm_val = f"{A if A else '-'} / {B if B else '-'}"

                all_val = f"{C if C else '-'} / {D if D else '-'}"

                ws.cell(row_no, col).value = dsm_val
                ws.cell(row_no, col + 1).value = all_val

                col += 2

            # TOTAL COLUMN

            ws.cell(row_no, col).value = (
                f"{row_total['A'] if row_total['A'] else '-'} / "
                f"{row_total['B'] if row_total['B'] else '-'}"
            )

            ws.cell(row_no, col + 1).value = (
                f"{row_total['C'] if row_total['C'] else '-'} / "
                f"{row_total['D'] if row_total['D'] else '-'}"
            )

            row_values += [
                row_total["A"],
                row_total["B"],
                row_total["C"],
                row_total["D"]
            ]

            # =====================================================
            # HIDE EMPTY ROW
            # =====================================================

            if all(v == 0 for v in row_values):

                ws.row_dimensions[row_no].hidden = True

            else:

                visible_idx += 1

                bg = "FFFFFF" if visible_idx % 2 else "E7E6EC"

                fill = PatternFill(
                    start_color=bg,
                    end_color=bg,
                    fill_type="solid"
                )

                for c in ws[row_no]:

                    c.fill = fill
                    c.alignment = center
                    c.border = border

            row_no += 1

    # =====================================================
    # TOTAL ROW
    # =====================================================

    totals_all = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0
    }

    ws.cell(row_no, 1).value = "TOTAL"

    ws.merge_cells(
        start_row=row_no,
        start_column=1,
        end_row=row_no,
        end_column=2
    )

    col = 3

    for terr in territories:

        A = totals[terr]["A"]
        B = totals[terr]["B"]
        C = totals[terr]["C"]
        D = totals[terr]["D"]

        totals_all["A"] += A
        totals_all["B"] += B
        totals_all["C"] += C
        totals_all["D"] += D

        ws.cell(row_no, col).value = (
            f"{A if A else '-'} / {B if B else '-'}"
        )

        ws.cell(row_no, col + 1).value = (
            f"{C if C else '-'} / {D if D else '-'}"
        )

        col += 2

    ws.cell(row_no, col).value = (
        f"{totals_all['A'] if totals_all['A'] else '-'} / "
        f"{totals_all['B'] if totals_all['B'] else '-'}"
    )

    ws.cell(row_no, col + 1).value = (
        f"{totals_all['C'] if totals_all['C'] else '-'} / "
        f"{totals_all['D'] if totals_all['D'] else '-'}"
    )

    for c in ws[row_no]:

        c.fill = total_fill
        c.font = Font(bold=True)
        c.alignment = center
        c.border = border

    # =====================================================
    # COLUMN WIDTH
    # =====================================================

    for col_idx in range(1, ws.max_column + 1):

        max_length = 0

        col_letter = get_column_letter(col_idx)

        for row in ws.iter_rows(
            min_col=col_idx,
            max_col=col_idx
        ):

            for cell in row:

                if cell.value:

                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

        ws.column_dimensions[col_letter].width = max_length + 5

    # =====================================================
    # DOWNLOAD
    # =====================================================

    xlsx_file = BytesIO()

    wb.save(xlsx_file)

    frappe.response["filename"] = "Territory_Followup.xlsx"

    frappe.response["filecontent"] = xlsx_file.getvalue()

    frappe.response["type"] = "binary"



@frappe.whitelist()
def get_meetlog_table(from_date=None,to_date=None,employee=None):

    import frappe

    filters = {}

    # =====================================
    # DATE FILTER
    # =====================================

    if from_date and to_date:

        filters["date_and_time"] = [
            "between",
            [
                f"{from_date} 00:00:00",
                f"{to_date} 23:59:59"
            ]
        ]

    elif from_date:

        filters["date_and_time"] = [
            ">=",
            f"{from_date} 00:00:00"
        ]

    elif to_date:

        filters["date_and_time"] = [
            "<=",
            f"{to_date} 23:59:59"
        ]

    # =====================================
    # EMPLOYEE FILTER
    # =====================================

    if employee:

        filters["employee"] = employee

    # =====================================
    # GET DATA
    # =====================================

    meetlogs = frappe.get_all(

        "MeetLog",

        filters=filters,

        fields=[
            "name",
            "gprs_location",
            "reached_location",
            "submitted_location",
            "employee_name",
            "sales_follow_up",
            "visit_type",
            "date_and_time",
            "completed_time"
        ],

        order_by="date_and_time desc"
    )

    # =====================================
    # NO DATA
    # =====================================

    if not meetlogs:

        return """
            <div style="
                padding:20px;
                text-align:center;
                color:red;
                font-weight:bold;
            ">
                No Data Found
            </div>
        """

    # =====================================
    # TABLE
    # =====================================

    data = """
    <table border="1" width="100%" style="
        border-collapse:collapse;
        background:white;
        font-size:12px;
        table-layout:auto;
    ">

        <tr style="
            background:#0F1568;
            color:white;
            text-align:center;
            position:sticky;
            top:0;
            z-index:5;
        ">

            <th style="padding:8px;">ML ID</th>
            <th style="padding:8px;">Status</th>
            <th style="padding:8px;">Employee Name</th>
            <th style="padding:8px;">Sales Follow Up</th>
            <th style="padding:8px;">Reached Area</th>
            <th style="padding:8px;">Visit Type</th>
            <th style="padding:8px;">Date and Time</th>
            <th style="padding:8px;">Completed Time</th>

        </tr>
    """

    for idx, row in enumerate(meetlogs, start=1):

        bg = "#FFFFFF" if idx % 2 else "#E7E6EC"

        # =====================================
        # STATUS
        # =====================================

        status = "Pending"

        if row.gprs_location:
            status = "Start"

        if row.reached_location:
            status = "Reached"

        if row.submitted_location:
            status = "Completed"

        # =====================================
        # ROW
        # =====================================

        data += f"""

        <tr style="
            background:{bg};
            color:black;
        ">

            <td style="
                padding:8px;
                text-align:center;
            ">

                <a href="/app/meetlog/{row.name}"
                    target="_blank"
                    style="
                        text-decoration:none;
                        color:black;
                        
                    ">

                    {row.name}

                </a>

            </td>

            <td style="
                padding:8px;
                text-align:center;
            ">
                {status}
            </td>

            <td style="
                padding:8px;
                text-align:left;
            ">
                {row.employee_name or ""}
            </td>

            <td style="
                padding:8px;
                text-align:left;
            ">
                {
                    frappe.db.get_value(
                        "Sales Follow Up",
                        row.sales_follow_up,
                        "organization_name"
                    ) if row.sales_follow_up else ""
                }
            </td>

            <td style="
                padding:8px;
                text-align:left;
            ">
                {row.reached_location or ""}
            </td>

            <td style="
                padding:8px;
                text-align:center;
            ">
                {row.visit_type or ""}
            </td>

            <td style="
                padding:8px;
                text-align:center;
            ">
                {frappe.utils.format_datetime(row.date_and_time) if row.date_and_time else ""}
            </td>

            <td style="
                padding:8px;
                text-align:center;
            ">
                {frappe.utils.format_datetime(row.completed_time) if row.completed_time else ""}
            </td>

        </tr>
        """

    data += "</table>"

    data = f"""
    <div style="
        height:280px;
        overflow-y:auto;
        overflow-x:auto;
    ">
        {data}
    </div>
    """

    return data



@frappe.whitelist()
def download_meetlog_excel(
    from_date=None,
    to_date=None,
    employee=None
):

    import frappe
    import openpyxl

    from io import BytesIO
    from openpyxl.styles import (
        Font,
        PatternFill,
        Alignment
    )

    filters = {}

    # -----------------------------
    # DATE FILTER
    # -----------------------------

    if from_date and to_date:

        filters["date_and_time"] = [
            "between",
            [
                f"{from_date} 00:00:00",
                f"{to_date} 23:59:59"
            ]
        ]

    elif from_date:

        filters["date_and_time"] = [
            ">=",
            f"{from_date} 00:00:00"
        ]

    elif to_date:

        filters["date_and_time"] = [
            "<=",
            f"{to_date} 23:59:59"
        ]

    # -----------------------------
    # EMPLOYEE FILTER
    # -----------------------------

    if employee:
        filters["employee"] = employee

    # -----------------------------
    # GET DATA
    # -----------------------------

    meetlogs = frappe.get_all(

        "MeetLog",

        filters=filters,

        fields=[
            "name",
            "gprs_location",
            "reached_location",
            "submitted_location",
            "employee_name",
            "sales_follow_up",
            "visit_type",
            "date_and_time",
            "completed_time"
        ],

        order_by="date_and_time desc"
    )

    # -----------------------------
    # WORKBOOK
    # -----------------------------

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "MeetLog Report"

    headers = [
        "ML ID",
        "Status",
        "Employee Name",
        "Sales Follow Up",
        "Reached Area",
        "Visit Type",
        "Date and Time",
        "Completed Time"
    ]

    ws.append(headers)

    # -----------------------------
    # HEADER STYLE
    # -----------------------------

    header_fill = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )

    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    for cell in ws[1]:

        cell.fill = header_fill
        cell.font = header_font

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # -----------------------------
    # ROW STYLE
    # -----------------------------

    odd_fill = PatternFill(
        start_color="FFFFFF",
        end_color="FFFFFF",
        fill_type="solid"
    )

    even_fill = PatternFill(
        start_color="E7E6EC",
        end_color="E7E6EC",
        fill_type="solid"
    )

    # -----------------------------
    # DATA ROWS
    # -----------------------------

    for idx, row in enumerate(meetlogs, start=1):

        status = "Pending"

        if row.gprs_location:
            status = "Start"

        if row.reached_location:
            status = "Reached"

        if row.submitted_location:
            status = "Completed"

        sales_follow_up = ""

        if row.sales_follow_up:

            sales_follow_up = frappe.db.get_value(
                "Sales Follow Up",
                row.sales_follow_up,
                "organization_name"
            )

        ws.append([
            row.name,
            status,
            row.employee_name or "",
            sales_follow_up or "",
            row.reached_location or "",
            row.visit_type or "",
            str(row.date_and_time or ""),
            str(row.completed_time or "")
        ])

        fill = odd_fill if idx % 2 != 0 else even_fill

        for cell in ws[idx + 1]:

            cell.fill = fill

            cell.alignment = Alignment(
                horizontal="left",
                vertical="center"
            )

    # -----------------------------
    # AUTO WIDTH
    # -----------------------------

    for column_cells in ws.columns:

        length = max(
            len(str(cell.value or ""))
            for cell in column_cells
        )

        ws.column_dimensions[
            column_cells[0].column_letter
        ].width = length + 5

    # -----------------------------
    # RESPONSE
    # -----------------------------

    xlsx_file = BytesIO()

    wb.save(xlsx_file)

    frappe.response["filename"] = \
        "MeetLog_Report.xlsx"

    frappe.response["filecontent"] = \
        xlsx_file.getvalue()

    frappe.response["type"] = "download"



@frappe.whitelist()
def get_fup_card_counts(employee_ids=None, services=None):

    import json
    import frappe

    # -------------------------
    # PARSE INPUTS (SAFE)
    # -------------------------
    try:
        employee_ids = json.loads(employee_ids) if employee_ids else []
    except:
        employee_ids = employee_ids or []

    try:
        services = json.loads(services) if services else []
    except:
        services = services or []

    # -------------------------
    # ENSURE LIST FORMAT
    # -------------------------
    if isinstance(employee_ids, str):
        employee_ids = [employee_ids]

    if isinstance(services, str):
        services = [services]

    # -------------------------
    # CLEAN VALUES (IMPORTANT FIX)
    # -------------------------
    clean_emp = []
    for emp in employee_ids:
        if emp:
            parts = str(emp).split(",")   # handle comma வந்தா split
            for p in parts:
                val = p.strip()
                if val:
                    clean_emp.append(val)

    employee_ids = clean_emp

    clean_services = []
    for s in services:
        if s:
            parts = str(s).split(",")
            for p in parts:
                val = p.strip()
                if val:
                    clean_services.append(val)

    services = clean_services

    # -------------------------
    # GET DEFAULT EMPLOYEES
    # -------------------------
    rs_employees = frappe.get_all("Employee",
        filters={
            "department": ["in", [
                "R&S - IT Services - THIS",
                "R&S - THIS",
                "R&S - TGT",
                "R&S - HR Service - THIS",
                "TFP - R&S  - TFP"
            ]],
            "status": "Active"
        },
        fields=["user_id"]
    )

    default_user_ids = [emp.user_id for emp in rs_employees if emp.user_id]

    # -------------------------
    # PRIORITY LOGIC
    # -------------------------
    user_ids = employee_ids if employee_ids else default_user_ids

    # -------------------------
    # DEBUG
    # -------------------------

    conditions = []
    filters = {}

    # -------------------------
    # BASE CONDITIONS
    # -------------------------
    conditions.append("account_manager_lead_owner IN %(user_ids)s")
    conditions.append("docstatus != 2")
    conditions.append("app_status = 'Scheduled'")
    conditions.append("call_status = 'Effective'")

    filters["user_ids"] = tuple(user_ids)

    # -------------------------
    # SERVICE FILTER
    # -------------------------
    if services:
        conditions.append("service IN %(services)s")
        filters["services"] = tuple(services)

    # -------------------------
    # WHERE CLAUSE
    # -------------------------
    where_clause = " AND ".join(conditions)
    where_clause = "WHERE " + where_clause


    # -------------------------
    # QUERY
    # -------------------------
    query = f"""
        SELECT
            COUNT(*) as active,
            SUM(CASE WHEN status = 'Opportunity' THEN 1 ELSE 0 END) as opportunity,
            SUM(CASE WHEN status = 'Replied' THEN 1 ELSE 0 END) as replied,
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open,
            SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) as closed
        FROM `tabSales Follow Up`
        {where_clause}
    """


    # -------------------------
    # EXECUTE
    # -------------------------
    result = frappe.db.sql(query, filters, as_dict=True)


    return result[0] if result else {}


