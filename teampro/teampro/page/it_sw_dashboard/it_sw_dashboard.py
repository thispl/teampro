import frappe
from frappe.utils import getdate, nowdate

@frappe.whitelist()
def get_order_booking_it(from_date=None, to_date=None):
    conditions = ["service = 'IT-SW'", "docstatus = 1", "status NOT IN ('On Hold', 'Cancelled', 'Closed')"]
    if not from_date and not to_date:
        today = frappe.utils.today()
        fiscal_year = frappe.db.get_value("Fiscal Year", 
            filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
            fieldname=["year_start_date", "year_end_date"],
            as_dict=True
        )
        from_date = fiscal_year["year_start_date"]
        to_date = fiscal_year["year_end_date"]
    if from_date:
        conditions.append("transaction_date >= %(from_date)s")
    if to_date:
        conditions.append("transaction_date <= %(to_date)s")
    frappe.errprint(from_date)
    frappe.errprint(to_date)
    query = f"""
        SELECT SUM(base_net_total)
        FROM `tabSales Order`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})[0][0] or 0
    return result

# @frappe.whitelist()
# def get_order_booking_it(from_date=None, to_date=None):
#     import json
#     from frappe.utils import getdate, today
#     from datetime import datetime
#     from frappe.utils import formatdate
#     conditions = ["service = 'IT-SW'", "docstatus = 1", "status NOT IN ('On Hold', 'Cancelled', 'Closed')"]
#     if not from_date and not to_date:
#         today = frappe.utils.today()
#         fiscal_year = frappe.db.get_value("Fiscal Year", 
#             filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
#             fieldname=["year_start_date", "year_end_date"],
#             as_dict=True
#         )
#         from_date = fiscal_year["year_start_date"]
#         to_date = fiscal_year["year_end_date"]
#     if from_date:
#         conditions.append("transaction_date >= %(from_date)s")
#     if to_date:
#         conditions.append("transaction_date <= %(to_date)s")

#     if from_date.month == 4 and from_date.day == 1:
#         current_month_number = to_date.month
#         month_count = current_month_number - 3 if current_month_number >= 4 else current_month_number + 9
#     else:
#         # 🟡 Use month difference for custom date range
#         month_count = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month) + 1    

#     query = f"""
#         SELECT SUM(base_net_total)
#         FROM `tabSales Order`
#         WHERE {' AND '.join(conditions)}
#     """

#     result = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})

#     total = result[0][0] or 0
#     average = round(total / month_count) if month_count > 0 else 0
#     return {
#         "total": total,
#         "average": average
#     }

@frappe.whitelist()
def get_turnover_it(from_date=None, to_date=None):
    conditions = ["services = 'IT-SW'", "docstatus = 1", "status NOT IN ('Return', 'Credit Note Issued', 'Cancelled')"]
    if not from_date and not to_date:
        today = frappe.utils.today()
        fiscal_year = frappe.db.get_value("Fiscal Year", 
            filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
            fieldname=["year_start_date", "year_end_date"],
            as_dict=True
        )
        from_date = fiscal_year["year_start_date"]
        to_date = fiscal_year["year_end_date"]
    if from_date:
        conditions.append("posting_date >= %(from_date)s")
    if to_date:
        conditions.append("posting_date <= %(to_date)s")

    query = f"""
        SELECT SUM(base_net_total)
        FROM `tabSales Invoice`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})[0][0] or 0
    return result

@frappe.whitelist()
def get_collection_value_it(from_date=None, to_date=None):
    if not from_date and not to_date:
        today = frappe.utils.today()
        fiscal_year = frappe.db.get_value(
            "Fiscal Year",
            filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
            fieldname=["year_start_date", "year_end_date"],
            as_dict=True
        )
        from_date = fiscal_year["year_start_date"]
        to_date = fiscal_year["year_end_date"]

    conditions = [
        "pe.payment_type = 'Receive'",
        "pe.docstatus = 1",
        "per.service = 'IT-SW'"
    ]

    if from_date:
        conditions.append("pe.posting_date >= %(from_date)s")
    if to_date:
        conditions.append("pe.posting_date <= %(to_date)s")

    query = f"""
        SELECT SUM(pe.paid_amount)
        FROM `tabPayment Entry` pe
        INNER JOIN `tabPayment Entry Reference` per ON per.parent = pe.name
        WHERE {' AND '.join(conditions)}
    """

    return frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})[0][0] or 0

@frappe.whitelist()
def it_receivable():
    today = frappe.utils.today()
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )
    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    filters = {
        'from_date': from_date,
        'to_date': to_date
    }
    total_invoice = frappe.db.sql("""
        SELECT SUM(outstanding_amount)
        FROM `tabSales Invoice`
        WHERE docstatus = 1
          AND services="IT-SW"
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters)[0][0] or 0
    return total_invoice

@frappe.whitelist()
def it_to_bill_value():
    today = frappe.utils.today()
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )
    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    filters = {
        'from_date': from_date,
        'to_date': to_date
    }
    total_invoice = frappe.db.sql("""
        SELECT SUM(base_grand_total)
        FROM `tabSales Order`
        WHERE docstatus = 1
          AND service='IT-SW'
          AND status='To Bill'
    """, )[0][0] or 0    
    return total_invoice

@frappe.whitelist()
def it_to_deliver_bill_value():
    today = frappe.utils.today()
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )
    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    filters = {
        'from_date': from_date,
        'to_date': to_date
    }

    total_invoice = frappe.db.sql("""
        SELECT SUM(base_grand_total)
        FROM `tabSales Order`
        WHERE docstatus = 1
          AND service='IT-SW'
          AND status='To Deliver and Bill'
          AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters)[0][0] or 0    

    return total_invoice

@frappe.whitelist()
def it_payable():
    # if not from_date and not to_date:
    today = frappe.utils.today()
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )
    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    filters = {
        'from_date': from_date,
        'to_date': to_date
    }

    # Total Submitted Purchase Invoice Amount
    total_invoice = frappe.db.sql("""
        SELECT SUM(outstanding_amount)
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1
          AND services="IT-SW"
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters)[0][0] or 0
    return total_invoice

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
        name_style = "color: red;" if age > 30 else ""
        total_outstanding += row.outstanding_amount or 0
        html += f"""
            <tr style="{row_style}">
            <td style="text-align: center;">{idx}</td>
                <td style="white-space: nowrap;">{row.supplier}</td>
                <td style='text-align:right;'>{frappe.utils.fmt_money(row.outstanding_amount)}</td>
                <td style='text-align:right;'>{age}</td>
                <td style="white-space: nowrap;"><a href="/app/purchase-invoice/{ row.name }" target="_blank" style="{name_style}">{ row.name }</a></td>
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
          AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
          AND base_grand_total > 0
        ORDER BY transaction_date
    """, filters, as_dict=True)

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
    return html