import frappe
from frappe.utils import getdate, nowdate

@frappe.whitelist()
def get_active_customers_count():
    customers = frappe.db.sql("""
        SELECT COUNT(DISTINCT c.name)
        FROM `tabCustomer` c
        JOIN `tabSLA Details` s ON s.parent = c.name
        WHERE c.disabled = 0
        AND s.service = 'TFP'
    """, as_dict=True)

    return customers[0]['COUNT(DISTINCT c.name)']

@frappe.whitelist()
def total_exp_value():
    return frappe.db.sql(""" SELECT SUM(opportunity_amount) from `tabOpportunity` where status not in("Lost") and service='TFP' """)[0][0] or 0

@frappe.whitelist()
def total_opp_qty():
    return frappe.db.sql(""" SELECT SUM(custom_expected_quantity) from `tabOpportunity` where status not in("Lost") and service='TFP' """)[0][0] or 0

@frappe.whitelist()
def get_total_customer_detalils():

    total_customers = frappe.db.sql("""
        SELECT COUNT(DISTINCT c.name) AS count
        FROM `tabCustomer` c
        JOIN `tabSLA Details` s ON s.parent = c.name
        WHERE c.disabled = 0
        AND s.service = 'TFP'
    """, as_dict=True)[0].count

    total_corporate_cust = frappe.db.sql("""
        SELECT COUNT(DISTINCT c.name) AS count
        FROM `tabCustomer` c
        JOIN `tabSLA Details` s ON s.parent = c.name
        WHERE c.disabled = 0
        AND s.service = 'TFP'
        AND c.customer_group != "Retail Shops"
    """, as_dict=True)[0].count

    total_retail_cust = frappe.db.sql("""
        SELECT COUNT(DISTINCT c.name) AS count
        FROM `tabCustomer` c
        WHERE c.disabled = 0
        AND c.customer_group = "Retail Shops"
    """, as_dict=True)[0].count

    total_vending = frappe.db.sql("""
        SELECT COUNT(DISTINCT w.name) AS count
        FROM `tabWarehouse` w
        WHERE w.disabled = 0
        AND w.company = 'TEAMPRO Food Products'
        AND w.parent_warehouse = "LSVM - Vending Machines - TFP"
    """, as_dict=True)[0].count
    overall_total= total_vending+total_retail_cust+total_corporate_cust
    return {
        "overall_customer_count": overall_total,
        "total_corporate_customers": total_corporate_cust,
        "total_retail_shops": total_retail_cust,
        "total_vending_machines": total_vending,

    }

@frappe.whitelist()
def get_order_booking(from_date=None, to_date=None):
    conditions = ["service = 'TFP'", "docstatus = 1", "status NOT IN ('On Hold', 'Cancelled', 'Closed','Completed')"]
    # if not from_date and not to_date:
    #     today = frappe.utils.today()
    #     fiscal_year = frappe.db.get_value("Fiscal Year", 
    #         filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
    #         fieldname=["year_start_date", "year_end_date"],
    #         as_dict=True
    #     )
    #     from_date = fiscal_year["year_start_date"]
    #     to_date = fiscal_year["year_end_date"]
    if from_date:
        conditions.append("transaction_date >= %(from_date)s")
    if to_date:
        conditions.append("transaction_date <= %(to_date)s")

    query = f"""
        SELECT SUM(base_net_total)
        FROM `tabSales Order`
        WHERE {' AND '.join(conditions)}
    """

    result = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})[0][0] or 0
    return result

@frappe.whitelist()
def get_turnover(from_date=None, to_date=None):
    conditions = ["services = 'TFP'", "docstatus = 1", "status NOT IN ('Return', 'Credit Note Issued', 'Cancelled')"]
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

# @frappe.whitelist()
# def get_total_so_qty(from_date=None,to_date=None):
#     conditions = ["service = 'TFP'", "docstatus = 1", "status NOT IN ('On Hold', 'Completed', 'Cancelled', 'Closed')"]
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

#     query = f"""
#         SELECT SUM(total_qty)
#         FROM `tabSales Order`
#         WHERE {' AND '.join(conditions)}
#     """

#     result = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})[0][0] or 0
#     return result

@frappe.whitelist()
def get_total_so_qty(from_date=None, to_date=None):

    from frappe.utils import today, getdate
    from dateutil.relativedelta import relativedelta
    conditions = [
        "service = 'TFP'",
        "docstatus = 1",
        "status NOT IN ('On Hold', 'Completed', 'Cancelled', 'Closed')"
    ]
    if not from_date and not to_date:
        today_date = today()
        fiscal_year = frappe.db.get_value(
            "Fiscal Year",
            filters={
                "year_start_date": ["<=", today_date],
                "year_end_date": [">=", today_date]
            },
            fieldname=["year_start_date", "year_end_date"],
            as_dict=True
        )
        from_date = fiscal_year["year_start_date"]
        to_date = fiscal_year["year_end_date"]
    if from_date:
        conditions.append("transaction_date >= %(from_date)s")
    if to_date:
        conditions.append("transaction_date <= %(to_date)s")
    query = f"""
        SELECT COALESCE(SUM(total_qty), 0)
        FROM `tabSales Order`
        WHERE {' AND '.join(conditions)}
    """
    total_qty = frappe.db.sql(
        query,
        {
            'from_date': from_date,
            'to_date': to_date
        }
    )[0][0] or 0
    start_date = getdate(from_date)
    current_date = getdate(today())
    months = (
        (current_date.year - start_date.year) * 12
        + current_date.month - start_date.month
        + 1
    )
    average_qty = total_qty / months if months else 0
    return {
        "total_qty": total_qty,
        "average_qty": round(average_qty, 2)
    }

@frappe.whitelist()
def get_collection_value(from_date=None, to_date=None):
    # Default to current fiscal year if dates are not provided
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
        "pe.company = 'TEAMPRO Food Products'",
        "pe.payment_type = 'Receive'",
        "pe.docstatus = 1",
        "per.service = 'TFP'"
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
def rececivable_count(from_date=None, to_date=None):
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



@frappe.whitelist()
def tfp_payable():
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
        'company': 'TEAMPRO Food Products',
        # 'from_date': from_date,
        # 'to_date': to_date
    }

    # Total Submitted Purchase Invoice Amount
    total_invoice = frappe.db.sql("""
        SELECT SUM(outstanding_amount)
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1
        AND services='TFP'
          AND company = %(company)s
          AND outstanding_amount>0
    """, filters)[0][0] or 0

    

    return total_invoice

@frappe.whitelist()
def tfp_receivable():
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
        'company': 'TEAMPRO Food Products',
        # 'from_date': from_date,
        # 'to_date': to_date
    }

    # Total Submitted Purchase Invoice Amount
    total_invoice = frappe.db.sql("""
        SELECT SUM(outstanding_amount)
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND services='TFP'
         AND status NOT IN ('Cancelled', 'Paid', 'Credit Note Issued', 'Return')
          AND company = %(company)s
    """, filters)[0][0] or 0

    

    return total_invoice

@frappe.whitelist()
def tfp_to_bill_value():
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
        'company': 'TEAMPRO Food Products',
        # 'from_date': from_date,
        # 'to_date': to_date
    }

    # Total Submitted Purchase Invoice Amount
    total_invoice = frappe.db.sql("""
        SELECT SUM(base_grand_total)
        FROM `tabSales Order`
        WHERE docstatus = 1
          AND service='TFP'
          AND status='To Bill'
          AND company = %(company)s
    """, filters)[0][0] or 0    

    return total_invoice

@frappe.whitelist()
def tfp_to_deliver_bill_value():
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
        'company': 'TEAMPRO Food Products',
        # 'from_date': from_date,
        # 'to_date': to_date
    }

    # Total Submitted Purchase Invoice Amount
    total_invoice = frappe.db.sql("""
        SELECT SUM(base_grand_total)
        FROM `tabSales Order`
        WHERE docstatus = 1
          AND service='TFP'
          AND status='To Deliver and Bill'
          AND company = %(company)s
    """, filters)[0][0] or 0    

    return total_invoice

# @frappe.whitelist()
# def get_customer_last_so_details():
#     data = frappe.db.sql("""
#         SELECT 
#             so.customer_name,
#             so.transaction_date AS last_so_on,
#             SUM(sod.qty) AS last_so_qty
#         FROM `tabSales Order` so
#         JOIN `tabSales Order Item` sod ON so.name = sod.parent
#         WHERE so.docstatus = 1
#         AND so.status NOT IN ('On Hold', 'Cancelled') 
#         AND so.service='TFP'
#         AND so.transaction_date = (
#             SELECT MAX(so_inner.transaction_date)
#             FROM `tabSales Order` so_inner
#             WHERE so_inner.customer_name = so.customer_name
#             AND so_inner.docstatus = 1
#             AND so_inner.status NOT IN ('On Hold', 'Cancelled')
#             AND so_inner.service='TFP'
#         )
#         GROUP BY so.customer_name, so.transaction_date
#         ORDER BY so.transaction_date DESC
#     """, as_dict=True)
#     return data

@frappe.whitelist()
def get_customer_last_so_details():
    from frappe.utils import getdate, nowdate

    data = frappe.db.sql("""
        SELECT 
            so.customer_name,
            so.transaction_date AS last_so_on,
            SUM(sod.qty) AS last_so_qty
        FROM `tabSales Order` so
        JOIN `tabSales Order Item` sod ON so.name = sod.parent
        WHERE so.docstatus = 1
        AND so.status NOT IN ('On Hold', 'Cancelled') 
        AND so.service='TFP'
        AND so.transaction_date = (
            SELECT MAX(so_inner.transaction_date)
            FROM `tabSales Order` so_inner
            WHERE so_inner.customer_name = so.customer_name
            AND so_inner.docstatus = 1
            AND so_inner.status NOT IN ('On Hold', 'Cancelled')
            AND so_inner.service='TFP'
        )
        GROUP BY so.customer_name, so.transaction_date
        ORDER BY so.transaction_date DESC
    """, as_dict=True)

    today = getdate(nowdate())
    old_rows = []
    recent_rows = []

    for row in data:
        so_date = getdate(row.last_so_on)
        age = (today - so_date).days
        row_html = f"""
            <tr style="{'color: red;' if age > 15 else ''}">
                <td>{row.customer_name}</td>
                <td>{frappe.utils.formatdate(row.last_so_on)}</td>
                <td style='text-align: right;'>{row.last_so_qty}</td>
            </tr>
        """
        if age > 15:
            old_rows.append(row_html)
        else:
            recent_rows.append(row_html)

    html = """
    <div style='max-height: 340px; overflow-y: auto;'>
        <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
            <thead>
                <tr>
                    <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center; z-index: 1;">Customer Name</th>
                    <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center; z-index: 1;">Last SO On</th>
                    <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center; z-index: 1;">Last SO Quantity</th>
                </tr>
            </thead>
            <tbody>
    """

    html += "".join(old_rows + recent_rows)  # Red rows first
    html += "</tbody></table></div>"

    return html




@frappe.whitelist()
def get_tfp_sales_value(from_date=None, to_date=None):
    conditions = ["service = 'TFP'", "docstatus = 1"]

    if from_date:
        conditions.append(f"transaction_date >= '{from_date}'")
    if to_date:
        conditions.append(f"transaction_date <= '{to_date}'")

    condition_str = " AND ".join(conditions)
    total = frappe.db.sql(f"""
        SELECT SUM(base_total) FROM `tabSales Order`
        WHERE {condition_str}
    """)[0][0] or 0

    return total

@frappe.whitelist()
def tfp_receivable_table():
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
        'company': 'TEAMPRO Food Products',
        # 'from_date': from_date,
        # 'to_date': to_date
    }

    data = frappe.db.sql("""
        SELECT name, customer, outstanding_amount, posting_date
        FROM `tabSales Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
        AND status NOT IN ('Cancelled', 'Paid', 'Credit Note Issued', 'Return')
          AND services='TFP'
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
def tfp_tobill_table():
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
        'company': 'TEAMPRO Food Products',
        'from_date': from_date,
        'to_date': to_date
    }

    data = frappe.db.sql("""
        SELECT name, customer, base_grand_total, transaction_date
        FROM `tabSales Order`
        WHERE docstatus = 1
          AND company = %(company)s
          AND service='TFP'
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
    # html += "</tbody></table></div>"

    return html

@frappe.whitelist()
def tfp_payable_table():
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
        'company': 'TEAMPRO Food Products',
        # 'from_date': from_date,
        # 'to_date': to_date
    }

    data = frappe.db.sql("""
        SELECT name, supplier, outstanding_amount, posting_date
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND services='TFP'
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
    # html += "</tbody></table></div>"

    return html

# @frappe.whitelist()
# def opportunity_details():
#     data = frappe.db.sql("""
#         SELECT 
#             opportunity_from,
#             organization_name,
#             opportunity_amount,
#             expected_closing,
#             custom_expected_quantity,
#             remark
#         FROM `tabOpportunity`
#         WHERE status NOT IN ('Lost') 
#         AND service = 'TFP'
#     """, as_dict=True)

#     # Optional: Add expected week in backend (ISO week number)
#     for row in data:
#         if row.expected_closing:
#             row.expected_week = frappe.utils.getdate(row.expected_closing).isocalendar()[1]
#         else:
#             row.expected_week = None
#     return data

@frappe.whitelist()
def opportunity_details():
    from frappe.utils import getdate, fmt_money
    import html

    data = frappe.db.sql("""
        SELECT 
            opportunity_from,
            organization_name,
            opportunity_amount,
            expected_closing,
            custom_expected_quantity,
            remark
        FROM `tabOpportunity`
        WHERE status NOT IN ('Lost') 
        AND service = 'TFP'
    """, as_dict=True)

    # Start HTML table
    html_table = """
    <div style='max-height: 340px; overflow-y: auto;'>
        <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
            <thead>
                <tr style="background: #002060; color: white; text-align: center;">
                    <th style="position: sticky; top: 0; background: #002060;">From</th>
                    <th style="position: sticky; top: 0; background: #002060;">Organization</th>
                    <th style="position: sticky; top: 0; background: #002060;">Amount</th>
                    <th style="position: sticky; top: 0; background: #002060;">Exp.Week</th>
                    <th style="position: sticky; top: 0; background: #002060;">Exp.Qty</th>
                    <th style="position: sticky; top: 0; background: #002060;">Remarks</th>
                </tr>
            </thead>
            <tbody>
    """

    for row in data:
        expected_week = getdate(row.expected_closing).isocalendar()[1] if row.expected_closing else '-'
        html_table += f"""
            <tr>
                <td>{row.opportunity_from or ''}</td>
                <td>{row.organization_name or ''}</td>
                <td style="text-align: right;">{frappe.utils.fmt_money(row.opportunity_amount or 0)}</td>
                <td style="text-align: center;">{expected_week}</td>
                <td style="text-align: center;">{row.custom_expected_quantity or ''}</td>
                <td>{row.remark or ''}</td>
            </tr>
        """


    html_table += "</tbody></table></div>"

    return html_table




# import frappe
# from frappe.utils import formatdate, nowdate, getdate

# @frappe.whitelist()
# def get_tfp_stock_html():
#     from datetime import timedelta

#     warehouse = "Stores - TFP"
#     item_group="Food Products"
#     stock_data = frappe.db.sql("""
#         SELECT 
#             bin.item_code,
#             item.item_name,
#             bin.actual_qty,
#             item.stock_uom,
#             (
#                 SELECT MAX(pr.creation)
#                 FROM `tabPurchase Receipt Item` pri
#                 JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
#                 WHERE pri.item_code = bin.item_code
#                 AND pri.warehouse = %s
#             ) AS last_pr_date
#         FROM `tabBin` bin
#         JOIN `tabItem` item ON bin.item_code = item.name AND item.item_group=%s
#         WHERE bin.warehouse = %s
#         AND bin.actual_qty > 0
#     """, (warehouse,item_group, warehouse), as_dict=True)

#     today = getdate(nowdate())
    
#     # Add age and is_old to each row
#     for row in stock_data:
#         pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
#         row.age = (today - pr_date).days if pr_date else None
#         row.is_old = row.age is not None and row.age > 30

#     # Sort: red (old) rows first
#     stock_data.sort(key=lambda x: not x.is_old)

#     # HTML table with sticky headers
#     html = """
#     <div style='max-height: 340px; overflow-y: auto; border: 1px solid #ccc; border-radius: 6px;'>
#     <table class="table table-bordered" style="width: 100%; border-collapse: collapse;">
#         <thead>
#             <tr style="text-align:center;">
#                 <th style="position: sticky; top: 0; background: #002060;color:white">Item Code</th>
#                 <th style="position: sticky; top: 0; background: #002060;color:white">Item Name</th>
#                 <th style="position: sticky; top: 0; background: #002060;color:white">Quantity</th>
#                 <th style="position: sticky; top: 0; background: #002060;color:white">Stock UOM</th>
#                 <th style="position: sticky; top: 0; background: #002060;color:white">Last PR Date</th>
#             </tr>
#         </thead>
#         <tbody>
#     """

#     for row in stock_data:
#         pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
#         red_row_style = 'style="color: red;"' if row.is_old else ""

#         html += f"""
#             <tr {red_row_style}>
#                 <td>{row.item_code}</td>
#                 <td>{row.item_name}</td>
#                 <td style="text-align:right">{row.actual_qty}</td>
#                 <td style="text-align:center">{row.stock_uom}</td>
#                 <td>{formatdate(pr_date) if pr_date else '-'}</td>
#             </tr>
#         """

#     html += "</tbody></table></div>"

#     return html

import frappe
from frappe.utils import formatdate

@frappe.whitelist()
def get_tfp_stock_html_data():

    vm_data = frappe.db.sql("""
        SELECT
            name AS vm_id,
            machine_id,
            status,
            total_new_stock_qty,
            next_filling,
            DATE(posting_date) AS posting_date
        FROM `tabVM Stock Register`
        WHERE docstatus != 2
        AND machine_id IS NOT NULL
        ORDER BY posting_date DESC
    """, as_dict=True)

    html = """
    <style>

    .vm-container{
        max-height:600px;
        overflow-y:auto;
        border:1px solid #cbd5e1;
        background:#e5e7eb;
    }

    .main-table{
        width:100%;
        border-collapse:collapse;
        font-size:13px;
        font-family: Arial, sans-serif;
        background:#e5e7eb;
    }

    /* MAIN HEADER STICKY */
    .main-table th{
        background:#002060;
        color:white;
        border:1px solid #cbd5e1;
        padding:8px;
        text-align:center;
        font-weight:bold;
        position: sticky;
        top: 0;
        z-index: 10;
    }

    .main-table td{
        border:1px solid #cbd5e1;
        padding:7px;
    }

    .parent-even{
        background:#f3f4f6;
    }

    .parent-odd{
        background:#e5e7eb;
    }

    .child-table{
        width:100%;
        border-collapse:collapse;
        background:#f3f4f6;
    }

    /* CHILD HEADER STICKY */
    .child-table th{
        background:#d9e1f2;
        color:#1e293b;
        border:1px solid #cbd5e1;
        padding:7px;
        text-align:center;
        font-weight:bold;
        position: sticky;
        top: 35px;
        z-index: 9;
    }

    .child-table td{
        border:1px solid #cbd5e1;
        padding:6px;
    }

    .child-even{
        background:#ffffff;
    }

    .child-odd{
        background:#f1f5f9;
    }

    .vm-link{
        cursor:pointer;
        color:#111827;
        font-weight:bold;
    }

    .vm-link:hover{
        text-decoration:underline;
    }

    .qty{
        text-align:right;
    }

    .center{
        text-align:center;
    }

    </style>

    <div class="vm-container">

    <table class="main-table">

        <thead>
            <tr>
                <th style="width:5%">Sr</th>
                <th style="width:18%">VM ID</th>
                <th style="width:22%">Vending Machine</th>
                <th style="width:12%">Status</th>
                <th style="width:12%">Total Quantity</th>
                <th style="width:15%">Last Filling</th>
                <th style="width:16%">Next Filling</th>
            </tr>
        </thead>

        <tbody>
    """

    sr = 1

    for d in vm_data:

        parent_class = "parent-even" if sr % 2 == 0 else "parent-odd"

        child_data = frappe.db.sql("""
            SELECT
                item_code,
                item_name,
                new_stock_qty,
                new_stockuom,
                stock_uom
            FROM `tabVM Stock Details`
            WHERE parent = %s
            AND new_stock_qty > 0
        """, (d.vm_id,), as_dict=True)

        child_rows = ""
        child_sr = 1

        for row in child_data:

            child_class = "child-even" if child_sr % 2 == 0 else "child-odd"

            child_rows += f"""
                <tr class="{child_class}">
                    <td>{row.item_code or ''}</td>
                    <td>{row.item_name or ''}</td>
                    <td class="qty">{row.new_stock_qty or 0}</td>
                    <td class="center">{row.stock_uom or ''}</td>
                    <td class="center">{row.new_stockuom or ''}</td>
                </tr>
            """
            child_sr += 1

        if not child_rows:
            child_rows = """
                <tr class="child-even">
                    <td colspan="5" style="text-align:center;">
                        No Stock Available
                    </td>
                </tr>
            """

        html += f"""
            <tr class="{parent_class}">
                <td class="center">{sr}</td>

                <td>

                        <span id="icon_{d.vm_id}"
                            onclick="toggle_vm_details('{d.vm_id}')"
                            style="
                                    cursor:pointer;
                                    font-weight:bold;
                                    margin-right:8px;
                                    font-size:16px;
                                    color:#111827;
                            ">
                            +
                        </span>

                        <a href="/app/vm-stock-register/{d.vm_id}"
                        target="_blank"
                        style="
                                color:#2563eb;
                                font-weight:bold;
                                text-decoration:none;
                        ">

                            {d.vm_id}

                        </a>

                    </td>

                <td>{d.machine_id or ''}</td>

                <td class="center">{d.status or ''}</td>

                <td class="qty">{d.total_new_stock_qty or 0}</td>

                <td class="center">
                    {formatdate(d.posting_date) if d.posting_date else ''}
                </td>

                <td class="center">{formatdate(d.next_filling) if d.next_filling else ''}</td>
            </tr>

            <tr id="detail_{d.vm_id}"
                style="display:none; background:#f8fafc;">

                <td colspan="7" style="padding:0px;">

                    <table class="child-table">
                        <thead>
                            <tr>
                                <th>Item Code</th>
                                <th>Item Name</th>
                                <th>Quantity</th>
                                <th>Stock UOM</th>
                                <th>UOM</th>
                            </tr>
                        </thead>

                        <tbody>
                            {child_rows}
                        </tbody>
                    </table>

                </td>
            </tr>
        """

        sr += 1

    html += """
        </tbody>
    </table>
    </div>

    <script>

    function toggle_vm_details(id){

        let row = document.getElementById("detail_" + id);
        let icon = document.getElementById("icon_" + id);

        if(row.style.display === "none"){
            row.style.display = "table-row";
            icon.innerHTML = "-";
        } else {
            row.style.display = "none";
            icon.innerHTML = "+";
        }
    }

    </script>
    """

    return html

@frappe.whitelist()
def get_tfp_vm_stock_html():
    from datetime import timedelta

    warehouse = "VM1_Precision - TFP"

    stock_data = frappe.db.sql("""
        SELECT 
            bin.item_code,
            item.item_name,
            bin.actual_qty,
            item.stock_uom,
            (
                SELECT MAX(pr.creation)
                FROM `tabPurchase Receipt Item` pri
                JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
                WHERE pri.item_code = bin.item_code
                AND pri.warehouse = %s
            ) AS last_pr_date
        FROM `tabBin` bin
        JOIN `tabItem` item ON bin.item_code = item.name
        WHERE bin.warehouse = %s
        AND bin.actual_qty > 0
    """, (warehouse, warehouse), as_dict=True)

    today = getdate(nowdate())
    
    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        row.age = (today - pr_date).days if pr_date else None
        row.is_old = row.age is not None and row.age > 30

    stock_data.sort(key=lambda x: not x.is_old)

    html = """
    <div style='max-height: 340px; overflow-y: auto; border: 1px solid #ccc; border-radius: 6px;'>
    <table class="table table-bordered" style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="text-align:center;">
                <th style="position: sticky; top: 0; background: #002060;color:white">Item Code</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Item Name</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Quantity</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Stock UOM</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Last PR Date</th>
            </tr>
        </thead>
        <tbody>
    """

    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        red_row_style = 'style="color: red;"' if row.is_old else ""

        html += f"""
            <tr {red_row_style}>
                <td>{row.item_code}</td>
                <td>{row.item_name}</td>
                <td style="text-align:right">{row.actual_qty}</td>
                <td style="text-align:center">{row.stock_uom}</td>
                <td>{formatdate(pr_date) if pr_date else '-'}</td>
            </tr>
        """

    html += "</tbody></table></div>"

    return html


@frappe.whitelist()
def get_tfp_stores_product():
    from datetime import timedelta

    warehouse = "Stores - TFP"
    child_groups = frappe.get_all("Item Group", filters={"parent_item_group": "Packing Material"}, pluck="name")
    item_groups = ["Packing Material"] + child_groups

    if not item_groups:
        return []

    # Step 2: Format item_groups for SQL IN clause
    format_strings = ','.join(['%s'] * len(item_groups))
    stock_data = frappe.db.sql(f"""
        SELECT 
            bin.item_code,
            item.item_name,
            bin.actual_qty,
            item.stock_uom,
            (
                SELECT MAX(pr.creation)
                FROM `tabPurchase Receipt Item` pri
                JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
                WHERE pri.item_code = bin.item_code
                AND pri.warehouse = %s
            ) AS last_pr_date
        FROM `tabBin` bin
        JOIN `tabItem` item ON bin.item_code = item.name
        WHERE bin.warehouse = %s
        AND bin.actual_qty > 0
        AND item.item_group IN ({format_strings})
    """, [warehouse, warehouse] + item_groups, as_dict=True)

    # stock_data = frappe.db.sql("""
    #     SELECT 
    #         bin.item_code,
    #         item.item_name,
    #         bin.actual_qty,
    #         item.stock_uom,
    #         (
    #             SELECT MAX(pr.creation)
    #             FROM `tabPurchase Receipt Item` pri
    #             JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
    #             WHERE pri.item_code = bin.item_code
    #             AND pri.warehouse = %s
    #         ) AS last_pr_date
    #     FROM `tabBin` bin
    #     JOIN `tabItem` item ON bin.item_code = item.name AND item.item_group= %s
    #     WHERE bin.warehouse = %s
    #     AND bin.actual_qty > 0
    # """, (warehouse, item_group,warehouse), as_dict=True)
    
    today = getdate(nowdate())
    
    # Add age and is_old to each row
    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        row.age = (today - pr_date).days if pr_date else None
        row.is_old = row.age is not None and row.age > 30

    # Sort: red (old) rows first
    stock_data.sort(key=lambda x: not x.is_old)

    # HTML table with sticky headers
    # html = """
    # <div style='max-height: 340px; overflow-y: auto; border: 1px solid #ccc; border-radius: 6px;'>
    # <table class="table table-bordered" style="width: 100%; border-collapse: collapse;">
    #     <thead>
    #         <tr style="text-align:center;">
    #             <th style="position: sticky; top: 0; background: #002060;color:white">Item Code</th>
    #             <th style="position: sticky; top: 0; background: #002060;color:white">Item Name</th>
    #             <th style="position: sticky; top: 0; background: #002060;color:white">Quantity</th>
    #             <th style="position: sticky; top: 0; background: #002060;color:white">Stock UOM</th>
    #             <th style="position: sticky; top: 0; background: #002060;color:white">Last PR Date</th>
    #         </tr>
    #     </thead>
    #     <tbody>
    # """
    html = """
    <div style='max-height: 340px; overflow-y: auto; border: 1px solid #ccc; border-radius: 6px;'>
    <table class="table table-bordered" style="width: 125%; border-collapse: collapse;">
        <thead>
            <tr style="text-align:center;">
                <th style="position: sticky; top: 0; background: #002060;color:white;white-space: nowrap;">Item Code</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Item Name</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Quantity</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Stock UOM</th>
                <th style="position: sticky; top: 0; background: #002060;color:white;white-space: nowrap;">Last PR Date</th>
            </tr>
        </thead>
        <tbody>
    """

    if not stock_data:
        html += '<tr><td colspan="5" style="text-align:center; border: 1px solid #ccc;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html
    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        red_row_style = 'style="color: red;"' if row.is_old else ""

        html += f"""
            <tr {red_row_style}>
                <td>{row.item_code}</td>
                <td>{row.item_name}</td>
                <td style="text-align:right">{row.actual_qty}</td>
                <td style="text-align:center">{row.stock_uom}</td>
                <td>{formatdate(pr_date) if pr_date else '-'}</td>
            </tr>
        """

    html += "</tbody></table></div>"

    return html


@frappe.whitelist()
def get_tfp_plan_html():
    from frappe.utils import formatdate, flt

    headers = [
        "Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery", "Item Name", "QTY", "UOM",
        "St.QTY", "CR. Stock", "Stock Status", "UOM", "MRP", "Packing Details", "WRD Details",
        "Name Print"
    ]

    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <table class="table table-bordered" style="border-collapse: collapse; width: 250%; table-layout: auto;">
    '''

    html += '<thead><tr style="background-color: #002060; color: white; text-align: center;">'
    for h in headers:
        if h in ["CR. Stock", "Stock Status"]:
            header_style = "background-color: #C00000; color: white;"  # Dark Red background, white text
        else:
            header_style = "background-color: #002060; color: white;"  # Default dark blue

        # header_style = "color: white;" if h not in ["CR. Stock", "Stock Status"] else "color: red;"
        html += f'''
            <th style="
                padding: 8px;
                border: 1px solid #ccc;
                position: sticky;
                top: 0;
                background: #002060;
                z-index: 1;
                {header_style}
            ">{h}</th>'''
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = 0
    grand_total_stock_qty = 0
    grand_total_covers = 0
    grand_total_2p = 0
    grand_total_bag = 0
    grand_total_box = 0

    so_list = frappe.db.get_all("Sales Order", {
        "service": "TFP",
        "status": "To Deliver and Bill"
    }, ["name", "customer", "custom_packing_on", "delivery_date"])
    if not so_list:
        html += '<tr><td colspan="17" style="text-align:center; border: 1px solid #ccc;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html
    for so in so_list:
        items = frappe.db.get_all("Sales Order Item", {"parent": so.name}, [
            "item_code", "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p",
            "custom_2nd_packing", "custom_name_print", "custom_tertiary_packingbox", "custom_bag", "custom_box",
            "custom_wrd_uom", "custom_wrd_rate", "custom_packing_on"
        ])

        rowspan = len(items)
        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = 0
        stock_status_list = []
        for idx, item in enumerate(items):
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)

            primary = frappe.db.get_value("Item", item.custom_cover_type, "item_name") or '' if item.custom_cover_type else ''
            secondary = frappe.db.get_value("Item", item.custom_packing_type, "item_name") or '' if item.custom_packing_type else ''
            tertiary = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or '' if item.custom_tertiary_packingbox else ''

            cr_stock = frappe.db.get_value("Bin", {
                "item_code": item.item_code,
                "warehouse": "Stores - TFP"
            }, "actual_qty") or 0

            stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                if flt(item.stock_qty) <= cr_stock \
                else '<span style="color: red; font-weight: bold;">Out of Stock</span>'
            stock_status_list.append(stock_status)
            html += '<tr>'
            if idx == 0:
                html += f'<td rowspan="{rowspan}" style="text-align: center; border: 1px solid #ccc;vertical-align: middle; text-align: left;">{s_no}</td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">{so.name}</td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc;"></td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">{so.customer}</td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc;vertical-align: middle; text-align: center;">{formatdate(so.custom_packing_on)}</td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc;vertical-align: middle; text-align: center;">{formatdate(so.delivery_date)}</td>'

            html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">{item.item_name or ""}</td>'
            html += f'<td style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{item.qty or ""}</td>'
            html += f'<td style="border: 1px solid #ccc; text-align: center;vertical-align: middle;">{item.uom or ""}</td>'

            html += f'<td style="text-align:right; border: 1px solid #ccc;vertical-align: middle;">{item.stock_qty or ""}</td>'
            html += f'<td style="text-align:right; border: 1px solid #ccc;vertical-align: middle;">{cr_stock}</td>'
            html += f'<td style="border: 1px solid #ccc; text-align: center;vertical-align: middle;">{stock_status}</td>'

            html += f'<td style="border: 1px solid #ccc; text-align: center;vertical-align: middle;">{item.stock_uom or ""}</td>'
            html += f'<td style="text-align:right; border: 1px solid #ccc;vertical-align: middle;">{item.mrp or ""}</td>'
            html += f'<td style="border: 1px solid #ccc; text-align: left;vertical-align: middle;">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>'
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            html += f'''
                <td style="border: 1px solid #ccc; text-align: left; padding: 10px; line-height: 1.6;">
                    <div style="margin-bottom: 4px;">(W): {item.custom_wrd_uom or ""}</div>
                    <div style="margin-bottom: 4px;">(R): {item_rate or ""}</div>
                    <div>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</div>
                </td>'''

            html += f'<td style="border: 1px solid #ccc;vertical-align: middle;">{item.custom_name_print or ""}</td>'


            html += '</tr>'
        all_in_stock = all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        )
        go_status = "CREATE DN" if all_in_stock else "CREATE MR"

        html += f'''
            <tr style="background-color: #e0e0e0; font-weight: bold;">
                <td colspan="7" style="text-align:right; border: 1px solid #ccc;"></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:right; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{go_status}</td>
                <td></td>
                <td colspan="{len(headers) - 5}" style="border: 1px solid #ccc;"></td>
            </tr>
        '''
        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1

    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
            <td colspan="7" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:right; border: 1px solid #ccc;">{grand_total_stock_qty}</td>
            <td colspan="2" style="border: 1px solid #ccc;"></td>
            <td colspan="{len(headers) - 5}" style="border: 1px solid #ccc;"></td>
        </tr>
    '''

    html += '</tbody></table></div>'
    return html

# @frappe.whitelist()
# def get_tfp_plan_html_new():
#     from frappe.utils import formatdate, flt

#     headers = ["Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery"]

#     html = '''
#     <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
#     <style>
#         .tfp-table-wrapper td, .tfp-table-wrapper th {
#             padding: 6px;
#             vertical-align: middle;
#             border: 1px solid #ccc;
#         }
#     </style>
#     <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
#     '''
#     html += f''' <tr style="background-color: #002060; color: white;">
#             <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Sr</th>
#             <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">SO</th>
#             <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">PRT</th>
#             <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">Customer</th>
#             <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Packing</th>
#             <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="2">Delivery</th>
#         </tr>'''
    
#     html += '</tr></thead><tbody>'

#     s_no = 1
#     grand_total_qty = 0
#     grand_total_stock_qty = 0
#     grand_total_covers = 0
#     grand_total_2p = 0
#     grand_total_bag = 0
#     grand_total_box = 0

#     so_list = frappe.db.get_all("Sales Order", {
#         "service": "TFP",
#         "status": "To Deliver and Bill"
#     }, ["name", "customer", "custom_packing_on", "delivery_date"])

#     if not so_list:
#         html += '<tr><td colspan="6" style="text-align:center;">Nothing to show</td></tr>'
#         html += '</tbody></table></div>'
#         return html

#     for so in so_list:
#         items = frappe.db.get_all("Sales Order Item", {"parent": so.name}, [
#             "item_code", "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
#             "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p",
#             "custom_2nd_packing", "custom_name_print", "custom_tertiary_packingbox", "custom_bag", "custom_box",
#             "custom_wrd_uom", "custom_wrd_rate", "custom_packing_on"
#         ])

#         html += f'''
#         <tr style="font-weight:bold; background-color:#f2f2f2;">
#             <td style="text-align:center;"colspan="1">
#                 <button class="toggle-btn" data-so="{so.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button> {s_no}
#             </td>
#             <td colspan="3">{so.name}</td>
#             <td colspan="1"></td>
#             <td colspan="3">{so.customer}</td>
#             <td style="text-align:center;"colspan="1">{formatdate(so.custom_packing_on)}</td>
#             <td style="text-align:center;"colspan="2">{formatdate(so.delivery_date)}</td>
#         </tr>
#         <tr class="details-row so-{so.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
#             <td style="text-align:center;">Item</td>
#             <td style="text-align:center;">Qty</td>
#             <td style="text-align:center;">UOM</td>
#             <td style="text-align:center;">Stock Qty</td>
#             <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
#             <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
#             <td style="text-align:center;">UOM</td>
#             <td style="text-align:center;">MRP</td>
#             <td style="text-align:center;">Packing Details</td>
#             <td style="text-align:center;">WRD Details</td>
#             <td style="text-align:center;">Name Details</td>
#         </tr>
#         '''

#         total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = 0
#         for item in items:
#             total_qty += flt(item.qty)
#             total_stock_qty += flt(item.stock_qty)
#             total_covers += flt(item.custom_covers)
#             total_2p += flt(item.custom_2nd_packing)
#             total_bag += flt(item.custom_bag)
#             total_box += flt(item.custom_box)

#             primary = frappe.db.get_value("Item", item.custom_cover_type, "item_name") or ''
#             secondary = frappe.db.get_value("Item", item.custom_packing_type, "item_name") or ''
#             tertiary = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

#             cr_stock = frappe.db.get_value("Bin", {
#                 "item_code": item.item_code,
#                 "warehouse": "Stores - TFP"
#             }, "actual_qty") or 0

#             stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
#                 if flt(item.stock_qty) <= cr_stock else \
#                 '<span style="color: red; font-weight: bold;">Out of Stock</span>'
#             if item.custom_wrd_rate:
#                 item_rate=f"{float(item.custom_wrd_rate):.2f}"
#             else:
#                 item_rate=''

#             html += f'''
#             <tr class="details-row so-{so.name}" style="display:none;">
#                 <td style="text-align:left;">{item.item_name}</td>
#                 <td style="text-align:center;">{item.qty}</td>
#                 <td style="text-align:center;">{item.uom}</td>
#                 <td style="text-align:right;">{item.stock_qty}</td>
#                 <td style="text-align:right;">{cr_stock}</td>
#                 <td style="text-align:center;">{stock_status}</td>
#                 <td style="text-align:center;">{item.stock_uom}</td>
#                 <td style="text-align:right;">{item.mrp}</td>
#                 <td style="text-align:left;">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
#                 <td style="text-align:left;">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
#                 <td style="text-align:center;">{item.custom_name_print or ""}</td>
#             </tr>
#             '''

#         go_status = "CREATE DN" if all(
#             flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
#             for it in items
#         ) else "CREATE MR"

#         html += f'''
#         <tr class="details-row so-{so.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
#         <td colspan="1" style="text-align:right; border: 1px solid #ccc;">Total</td>
#                 <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
#                 <td></td>
#                 <td style="text-align:right; border: 1px solid #ccc;">{total_stock_qty}</td>
#                 <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{go_status}</td>
#                 <td></td>
#             <td colspan="5" style="text-align:right;"></td>
#         </tr>
#         '''

#         grand_total_qty += total_qty
#         grand_total_stock_qty += total_stock_qty
#         grand_total_covers += total_covers
#         grand_total_2p += total_2p
#         grand_total_bag += total_bag
#         grand_total_box += total_box
#         s_no += 1

#     html += f'''
#         <tr style="background-color: #002060; font-weight: bold; color: white;">
#          <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
#             <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
#             <td style="border: 1px solid #ccc;"></td>
#             <td style="text-align:right; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
#             <td colspan="7" style="border: 1px solid #ccc;"></td>
#         </tr>
#     </tbody></table></div>
#     <script>
#         document.querySelectorAll(".toggle-btn").forEach(btn => {{
#             btn.addEventListener("click", function() {{
#                 const so = this.dataset.so;
#                 const rows = document.querySelectorAll(".so-" + so);
#                 const isVisible = rows[0].style.display === "table-row";
#                 rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
#                 this.textContent = isVisible ? "+" : "-";
#             }});
#         }});
#     </script>
#     '''

#     return html


# @frappe.whitelist()
# def get_customer_last_so_details_active():
#     from frappe.utils import getdate, nowdate

#     data = frappe.db.sql("""
#         SELECT 
#             so.customer_name,
#             so.transaction_date AS last_so_on,
#             SUM(sod.qty) AS last_so_qty
#         FROM `tabSales Order` so
#         JOIN `tabSales Order Item` sod ON so.name = sod.parent
#         JOIN `tabCustomer` c ON c.name = so.customer
#         JOIN `tabSLA Details` s ON s.parent = c.name
#         WHERE so.docstatus = 1
#         AND so.status NOT IN ('On Hold', 'Cancelled') 
#         AND so.service = 'TFP'
#         AND s.service = 'TFP'
#         AND c.disabled = 0
#         AND so.transaction_date = (
#             SELECT MAX(so_inner.transaction_date)
#             FROM `tabSales Order` so_inner
#             WHERE so_inner.customer_name = so.customer_name
#             AND so_inner.docstatus = 1
#             AND so_inner.status NOT IN ('On Hold', 'Cancelled')
#             AND so_inner.service = 'TFP'
#         )
#         GROUP BY so.customer_name, so.transaction_date
#         ORDER BY so.transaction_date DESC
#     """, as_dict=True)

#     today = getdate(nowdate())
#     old_rows = []
#     recent_rows = []

#     for row in data:
#         so_date = getdate(row.last_so_on)
#         age = (today - so_date).days
#         row_html = f"""
#             <tr style="{'color: red;' if age > 15 else ''}">
#                 <td>{row.customer_name}</td>
#                 <td>{frappe.utils.formatdate(row.last_so_on)}</td>
#                 <td style='text-align: right;'>{row.last_so_qty}</td>
#             </tr>
#         """
#         if age > 15:
#             old_rows.append(row_html)
#         else:
#             recent_rows.append(row_html)

#     html = """
#     <div style='max-height: 340px; overflow-y: auto;'>
#         <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
#             <thead>
#                 <tr>
#                     <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center;">Customer Name</th>
#                     <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center;">Last SO On</th>
#                     <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center;">Last SO Quantity</th>
#                 </tr>
#             </thead>
#             <tbody>
#     """
#     html += "".join(old_rows + recent_rows)
#     html += "</tbody></table></div>"

#     return html

@frappe.whitelist()
def get_customer_last_so_details_active():
    from frappe.utils import getdate, nowdate, formatdate

    today = getdate(nowdate())

    data = frappe.db.sql("""
        SELECT 
            so.customer_name,
            so.transaction_date AS last_so_on,
            SUM(sod.qty) AS last_so_qty
        FROM `tabSales Order` so
        JOIN `tabSales Order Item` sod ON so.name = sod.parent
        JOIN `tabCustomer` c ON c.name = so.customer
        WHERE so.docstatus = 1
        AND so.status NOT IN ('On Hold', 'Cancelled') 
        AND so.service = 'TFP'
        AND c.disabled = 0
        AND EXISTS (
            SELECT 1 FROM `tabSLA Details` s
            WHERE s.parent = c.name AND s.service = 'TFP'
            LIMIT 1
        )
        AND so.transaction_date = (
            SELECT MAX(so_inner.transaction_date)
            FROM `tabSales Order` so_inner
            WHERE so_inner.customer_name = so.customer_name
            AND so_inner.docstatus = 1
            AND so_inner.status NOT IN ('On Hold', 'Cancelled')
            AND so_inner.service = 'TFP'
        )
        GROUP BY so.customer_name, so.transaction_date
        ORDER BY so.transaction_date DESC
    """, as_dict=True)

    old_rows = []
    recent_rows = []

    for row in data:
        so_date = getdate(row.last_so_on)
        age_days = (today - so_date).days
        highlight = 'color: red;' if age_days > 15 else ''

        row_html = f"""
            <tr style="{highlight}">
                <td>{row.customer_name}</td>
                <td>{formatdate(row.last_so_on)}</td>
                <td style='text-align: right;'>{row.last_so_qty}</td>
                <td style='text-align: right;'>{age_days}</td>
            </tr>
        """

        if age_days > 15:
            old_rows.append(row_html)
        else:
            recent_rows.append(row_html)

    html = """
    <div style='max-height: 340px; overflow-y: auto;'>
        <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
            <thead>
                <tr>
                    <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center;">Customer Name</th>
                    <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center;">Last SO On</th>
                    <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center;">Last SO Quantity</th>
                    <th style="position: sticky; top: 0; background: #092779; color: white; text-align: center;">Age (Days)</th>
                </tr>
            </thead>
            <tbody>
    """
    html += "".join(old_rows + recent_rows)
    html += "</tbody></table></div>"

    return html



@frappe.whitelist()
def get_tfp_plan_html_plan_new():
    from frappe.utils import formatdate, flt

    headers = ["Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery"]

    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Sr</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">SO</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">PRT</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">Customer</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Packing</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="2">Delivery</th>
        </tr>'''
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = 0
    grand_total_stock_qty = 0
    grand_total_covers = 0
    grand_total_2p = 0
    grand_total_bag = 0
    grand_total_box = 0

    so_list = frappe.db.get_all("Sales Order", {
        "service": "TFP",
        "status": "To Deliver and Bill"
    }, ["name", "customer", "custom_packing_on", "delivery_date"])

    if not so_list:
        html += '<tr><td colspan="6" style="text-align:center;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html

    for so in so_list:
        items = frappe.db.get_all("Sales Order Item", {"parent": so.name}, [
            "item_code", "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p",
            "custom_2nd_packing", "custom_name_print", "custom_tertiary_packingbox", "custom_bag", "custom_box",
            "custom_wrd_uom", "custom_wrd_rate", "custom_packing_on"
        ])

        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td style="text-align:center;"colspan="1">
                <button class="toggle-btn" data-sos="{so.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button> {s_no}
            </td>
            <td colspan="3">{so.name}</td>
            <td colspan="1"></td>
            <td colspan="3">{so.customer}</td>
            <td style="text-align:center;"colspan="1">{formatdate(so.custom_packing_on)}</td>
            <td style="text-align:center;"colspan="2">{formatdate(so.delivery_date)}</td>
        </tr>
        <tr class="details-row sos-{so.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">Stock Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;">WRD Details</td>
            <td style="text-align:center;">Name Details</td>
        </tr>
        '''

        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = 0
        for item in items:
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)

            primary = frappe.db.get_value("Item", item.custom_cover_type, "item_name") or ''
            secondary = frappe.db.get_value("Item", item.custom_packing_type, "item_name") or ''
            tertiary = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

            cr_stock = frappe.db.get_value("Bin", {
                "item_code": item.item_code,
                "warehouse": "Stores - TFP"
            }, "actual_qty") or 0

            stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                if flt(item.stock_qty) <= cr_stock else \
                '<span style="color: red; font-weight: bold;">Out of Stock</span>'
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''

            html += f'''
            <tr class="details-row sos-{so.name}" style="display:none;">
                <td style="text-align:left;">{item.item_name}</td>
                <td style="text-align:center;">{item.qty}</td>
                <td style="text-align:center;">{item.uom}</td>
                <td style="text-align:right;">{item.stock_qty}</td>
                <td style="text-align:right;">{cr_stock}</td>
                <td style="text-align:center;">{stock_status}</td>
                <td style="text-align:center;">{item.stock_uom}</td>
                <td style="text-align:right;">{item.mrp}</td>
                <td style="text-align:left;">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                <td style="text-align:left;">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                <td style="text-align:center;">{item.custom_name_print or ""}</td>
            </tr>
            '''

        go_status = "CREATE DN" if all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        ) else "CREATE MR"

        html += f'''
        <tr class="details-row sos-{so.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:right; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:right; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{go_status}</td>
                <td></td>
            <td colspan="5" style="text-align:right;"></td>
        </tr>
        '''

        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1

    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:right; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="7" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const sos = this.dataset.sos;
                const rows = document.querySelectorAll(".sos-" + sos);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
    </script>
    '''
    

    return html
    


@frappe.whitelist()
def get_tfp_plan_html_schedule_new():
    from frappe.utils import formatdate, flt

    headers = [
        "Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery", "Item Name", "QTY", "UOM",
        "St.QTY", "UOM","MRP","Packing Details","WRD Details",
        "Name Print"
    ]
    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Sr</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">SO</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">PRT</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">Customer</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Packing</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="2">Delivery</th>
        </tr>'''
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = grand_total_stock_qty = grand_total_covers = grand_total_2p = grand_total_bag = grand_total_box = 0

    dn_list = frappe.db.get_all("Delivery Note", {
        "custom_delivery_status_new": "Schedule","docstatus":1,
    }, ["name", "customer", "custom_delivery_date","custom_packing_on","custom_priority"],order_by='custom_packing_on asc')

    for dn in dn_list:
        items = frappe.db.get_all("Delivery Note Item", {
            "parent": dn.name
        }, [
            "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p","custom_name_print","custom_tertiary_packingbox","custom_bag","custom_box",
            "custom_wrd_uom","custom_wrd_rate","custom_packing_on", "against_sales_order","custom_per_3p"
        ])

        if not items:
            continue

        rowspan = len(items)
        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = 0
        primary=''
        secondary=''
        tertiary=''
        for idx, item in enumerate(items):
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)
            if item.custom_cover_type:
                primary=frappe.db.get_value("Item",item.custom_cover_type,"item_name") or ''
            if item.custom_packing_type:
                secondary=frappe.db.get_value("Item",item.custom_packing_type,"item_name") or ''
            if item.custom_tertiary_packingbox:
                tertiary=frappe.db.get_value("Item",item.custom_tertiary_packingbox,"item_name") or ''
            html += '<tr>'
            if idx == 0:
                html += f'''
                    <tr style="font-weight:bold; background-color:#f2f2f2;">
                        <td style="text-align:left;"colspan="1">
                             {s_no}
                        </td>
                        <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-so="{item.against_sales_order}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{item.against_sales_order}</td>
                        <td colspan="1" style="text-align:center;">{dn.custom_priority}</td>
                        <td colspan="3" style="text-align:left;">{dn.customer}</td>
                        <td style="text-align:center;"colspan="1">{formatdate(dn.custom_packing_on)}</td>
                        <td style="text-align:center;"colspan="2">{formatdate(dn.custom_delivery_date)}</td>
                    
                    </tr>
                    <tr class="details-row so-{item.against_sales_order}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
                        <td style="text-align:center;">Item</td>
                        <td style="text-align:center;">Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">Stock Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">MRP</td>
                        <td style="text-align:center;" colspan="2">Packing Details</td>
                        <td style="text-align:center;">WRD Details</td>
                        <td style="text-align:center;">Name Details</td>
                    </tr>'''
                
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            html += f'''
            <tr class="details-row so-{item.against_sales_order}" style="display:none;">
                <td style="text-align:left;">{item.item_name}</td>
                <td style="text-align:center;">{item.qty}</td>
                <td style="text-align:center;">{item.uom}</td>
                <td style="text-align:center;">{item.stock_qty}</td>
                <td style="text-align:center;">{item.stock_uom}</td>
                <td style="text-align:right;">{item.mrp}</td>
                <td style="text-align:left;" colspan="2">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                <td style="text-align:left;">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                <td style="text-align:center;">{item.custom_name_print or ""}</td>
            </tr>
            '''
            

        html += f'''
        <tr class="details-row so-{item.against_sales_order}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:right; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;"></td>
                <td></td>
            <td colspan="5" style="text-align:right;"></td>
        </tr>
        '''


        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1

    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="7" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const so = this.dataset.so;
                const rows = document.querySelectorAll(".so-" + so);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
    </script>
    '''
    return html

@frappe.whitelist()
def get_tfp_plan_html_schedule_opertaions():
    from frappe.utils import formatdate, flt

    headers = [
        "Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery", "Item Name", "QTY", "UOM",
        "St.QTY", "UOM","MRP","Packing Details","WRD Details",
        "Name Print"
    ]
    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Sr</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">SO</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">PRT</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">Customer</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Packing Date</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="2">Delivery Date</th>
        </tr>'''
    
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = grand_total_stock_qty = grand_total_covers = grand_total_2p = grand_total_bag = grand_total_box = 0

    dn_list = frappe.db.get_all("Delivery Note", {
        "custom_delivery_status_new": "Schedule","docstatus":1
    }, ["name", "customer", "custom_delivery_date","custom_packing_on","custom_priority"], order_by="custom_packing_on asc")

    for dn in dn_list:
        balance_qty=0
        items = frappe.db.get_all("Delivery Note Item", {
            "parent": dn.name
        }, [
            "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p","custom_name_print","custom_tertiary_packingbox","custom_bag","custom_box",
            "custom_wrd_uom","custom_wrd_rate","custom_packing_on", "against_sales_order","custom_per_3p",""
        ])

        if not items:
            continue
        for i in items:
            balance_qty += flt(i.qty or 0)
        rowspan = len(items)
        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = 0
        primary=''
        secondary=''
        tertiary=''
        for idx, item in enumerate(items):
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)
            if item.custom_cover_type:
                primary=frappe.db.get_value("Item",item.custom_cover_type,"item_name") or ''
            if item.custom_packing_type:
                secondary=frappe.db.get_value("Item",item.custom_packing_type,"item_name") or ''
            if item.custom_tertiary_packingbox:
                tertiary=frappe.db.get_value("Item",item.custom_tertiary_packingbox,"item_name") or ''
            html += '<tr>'
            if idx == 0:
                
                html += f'''
                    <tr style="font-weight:bold; background-color:#f2f2f2;">
                        <td style="text-align:left;"colspan="1">
                            {s_no}
                        </td>
                        <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-dos="{item.against_sales_order}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button> {item.against_sales_order}</td>
                        <td colspan="1" style="text-align:center">{dn.custom_priority or ""}</td>
                        <td colspan="3" style="text-align:left;">{dn.customer}</td>
                        <td style="text-align:center;"colspan="1">{formatdate(dn.custom_packing_on)}</td>
                        <td style="text-align:center;"colspan="2">{formatdate(dn.custom_delivery_date)}</td>
                    
                    </tr>
                    <tr class="details-row dos-{item.against_sales_order}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
                        <td style="text-align:center;">Item</td>
                        <td style="text-align:center;">Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">Stock Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">MRP</td>
                        <td style="text-align:center;" colspan="2">Packing Details</td>
                        <td style="text-align:center;">WRD Details</td>
                        <td style="text-align:center;">Name Details</td>
                    </tr>'''
                
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            html += f'''
            <tr class="details-row dos-{item.against_sales_order}" style="display:none;">
                <td style="text-align:left;">{item.item_name}</td>
                <td style="text-align:center;">{item.qty}</td>
                <td style="text-align:center;">{item.uom}</td>
                <td style="text-align:center;">{item.stock_qty}</td>
                <td style="text-align:center;">{item.stock_uom}</td>
                <td style="text-align:right;">{item.mrp}</td>
                <td style="text-align:left;" colspan="2">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                <td style="text-align:left;">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                <td style="text-align:center;">{item.custom_name_print or ""}</td>
            </tr>
            '''
            

        html += f'''
        <tr class="details-row dos-{item.against_sales_order}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:right; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;"></td>
                <td></td>
            <td colspan="5" style="text-align:right;"></td>
        </tr>
        '''


        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1

    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="7" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const dos = this.dataset.dos;
                const rows = document.querySelectorAll(".dos-" + dos);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
    </script>
    '''
    return html

@frappe.whitelist()
def get_tfp_plan_html_schedule():
    from frappe.utils import formatdate, flt

    headers = [
        "Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery", "Item Name", "QTY", "UOM",
        "St.QTY", "UOM","MRP","Packing Details","WRD Details",
        "Name Print"
    ]

    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <table class="table table-bordered" style="border-collapse: collapse; width: 250%; table-layout: auto;">
    '''

    html += '<thead><tr style="background-color: #002060; color: white; text-align: center;">'
    for h in headers:
        html += f'''
            <th style="
                padding: 8px;
                border: 1px solid #ccc;
                position: sticky;
                top: 0;
                background: #002060;
                z-index: 1;
                color: white;
            ">{h}</th>'''
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = grand_total_stock_qty = grand_total_covers = grand_total_2p = grand_total_bag = grand_total_box = 0

    dn_list = frappe.db.get_all("Delivery Note", {
        "custom_delivery_status_new": "Schedule"
    }, ["name", "customer", "posting_date"])

    for dn in dn_list:
        items = frappe.db.get_all("Delivery Note Item", {
            "parent": dn.name
        }, [
            "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p","custom_name_print","custom_tertiary_packingbox","custom_bag","custom_box",
            "custom_wrd_uom","custom_wrd_rate","custom_packing_on", "against_sales_order","custom_per_3p"
        ])

        if not items:
            continue

        rowspan = len(items)
        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = 0
        primary=''
        secondary=''
        tertiary=''
        per_bag=''
        per_box=''
        for idx, item in enumerate(items):
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)
            if item.custom_cover_type:
                primary=frappe.db.get_value("Item",item.custom_cover_type,"item_name") or ''
            if item.custom_packing_type:
                secondary=frappe.db.get_value("Item",item.custom_packing_type,"item_name") or ''
            if item.custom_tertiary_packingbox:
                tertiary=frappe.db.get_value("Item",item.custom_tertiary_packingbox,"item_name") or ''
            # if item.custom_bag!=0:
            #     per_bag=(item.custom_per_2p/item.custom_bag)
            # if item.custom_box!=0:
            #     per_box=(item.custom_per_3p/item.custom_box)
            html += '<tr>'
            if idx == 0:
                html += f'<td rowspan="{rowspan}" style="text-align: center; border: 1px solid #ccc;vertical-align: middle;">{s_no}</td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc; vertical-align: middle;text-align:left">{item.against_sales_order or ""}</td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc;"></td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc; vertical-align: middle;text-align:left">{dn.customer}</td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc; text-align: center;"></td>'
                html += f'<td rowspan="{rowspan}" style="border: 1px solid #ccc; text-align: center;vertical-align: middle;">{formatdate(dn.posting_date)}</td>'

            html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">{item.item_name or ""}</td>'
            html += f'<td style="text-align:center; border: 1px solid #ccc;vertical-align: middle; text-align: center;">{item.qty or ""}</td>'
            html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: center;">{item.uom or ""}</td>'
            html += f'<td style="text-align:right; border: 1px solid #ccc;vertical-align: middle; text-align: center;">{item.stock_qty or ""}</td>'
            html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: center;">{item.stock_uom or ""}</td>'
            html += f'<td style="text-align:right; border: 1px solid #ccc;vertical-align: middle; text-align: right;">{item.mrp or ""}</td>'
            html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">(C):&nbsp;{primary or "None"}:&nbsp;{item.custom_covers or "0"}<br>(B):&nbsp;{secondary or "None"}:&nbsp;{item.custom_bag or "0"}<br>(BX):&nbsp;{tertiary or "None"}:&nbsp;{item.custom_box or "0"}</td>'
            # html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">(C):{primary or ""}:{item.custom_covers or ""}<br>(B):{secondary or ""}:{item.custom_bag or ""}<br>(BX):{tertiary or ""}:{item.custom_box or ""}</td>'
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">(W):&nbsp;{item.custom_wrd_uom or ""}<br>(R):&nbsp;{item_rate or ""}<br>(D):&nbsp;{formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>'
            html += f'<td style="border: 1px solid #ccc;vertical-align: middle; text-align: left;">{item.custom_name_print or ""}</td>'


            
            html += '</tr>'

        html += f'''
            <tr style="background-color: #e0e0e0; font-weight: bold;">
                <td colspan="7" style="text-align:right; border: 1px solid #ccc;"></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td style="border: 1px solid #ccc;"></td>
                <td style="text-align:right; border: 1px solid #ccc;vertical-align: middle; text-align: center;">{total_stock_qty}</td>
               <td style="border: 1px solid #ccc;"></td>
            <td colspan="1" style="border: 1px solid #ccc;"></td>
            <td style="border: 1px solid #ccc;"></td>
             <td style="border: 1px solid #ccc;"></td>
            <td style="border: 1px solid #ccc;"></td>
                          </tr>
        '''

        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1

    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
            <td colspan="7" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:right; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td colspan="1" style="border: 1px solid #ccc;"></td>
            <td style="border: 1px solid #ccc;"></td>
             <td style="border: 1px solid #ccc;"></td>
            <td style="border: 1px solid #ccc;"></td>
        </tr>
    '''

    html += '</tbody></table></div>'
    return html

@frappe.whitelist()
def get_packed_dn_summary_html():
    from frappe.utils import formatdate, flt

    html = '<div class="tfp-summary-table" style="overflow-x:auto;">'
    html += '<table class="table table-bordered" style="border-collapse: collapse; width: 100%;">'

    headers = ["DN ID", "SO ID", "Customer", "Delivery Date", "Total QTY", "Total Covers"]
    html += '<thead><tr style="background-color: #002060; color: white; text-align: center;">'
    for h in headers:
        html += f'<th style="padding: 8px; border: 1px solid #ccc;">{h}</th>'
    html += '</tr></thead><tbody>'

    # Step 1: Get all Packed Delivery Notes
    packed_dns = frappe.db.get_all("Delivery Note",
        filters={"custom_delivery_status_new": "Packed", "docstatus": 1},
        fields=["name", "custom_delivery_date", "total_qty", "custom_total_covers"],order_by="custom_delivery_date asc"
    )

    
    # Step 2: Get all DN Items linked to SO
    dn_names = [d.name for d in packed_dns]
    dn_items = frappe.db.get_all("Delivery Note Item",
        filters={"parent": ["in", dn_names], "against_sales_order": ["!=", ""]},
        fields=["parent", "against_sales_order"]
    )

    # Step 3: Build Summary Data
    summary = {}
    grand_total_qty = 0
    grand_total_covers = 0

    for dn_doc in packed_dns:
        dn = dn_doc.name
        dn_date = dn_doc.custom_delivery_date
        total_qty = flt(dn_doc.total_qty)
        total_covers = flt(dn_doc.custom_total_covers)

        grand_total_qty += total_qty
        grand_total_covers += total_covers

        # Get all SOs linked to this DN
        linked_sos = list(set([
            d.against_sales_order for d in dn_items if d.parent == dn and d.against_sales_order
        ]))

        if not linked_sos:
            key = (dn, "")
            summary[key] = {
                "dn": dn,
                "so": "",
                "customer": "",
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }

        for so in linked_sos:
            customer = frappe.db.get_value("Sales Order", so, "customer") or ""
            key = (dn, so)

            summary[key] = {
                "dn": dn,
                "so": so,
                "customer": customer,
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }

    # Step 4: Render HTML rows
    for (dn, so), data in summary.items():
        html += '<tr>'
        html+=f'<td style="text-align:left;"><a href="/app/delivery-note/{data["dn"]}" target="_blank">{data["dn"]}</a></td>'
        html += f'<td style="border: 1px solid #ccc;text-align:left">{data["so"]}</td>'
        html += f'<td style="border: 1px solid #ccc;text-align:left">{data["customer"]}</td>'
        html += f'<td style="border: 1px solid #ccc;">{formatdate(data["dn_date"]) if data["dn_date"] else ""}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{data["total_qty"]}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{data["total_covers"]}</td>'
        html += '</tr>'
    stock_entry=frappe.db.get_all("VM Stock Register",{"status":"Packed","docstatus":1},["name"])
    for i in stock_entry:
        if not i.name:
            continue
        register = frappe.get_doc("VM Stock Register", i.name)
        html += '<tr>'
        html+=f'<td style="text-align:left;" colspan="2"><a href="/app/vm-stock-register/{i.name}" target="_blank">{i.name}</a></td>'
        html += f'<td style="border: 1px solid #ccc;text-align:left">Precision-Employee</td>'
        html += f'<td style="border: 1px solid #ccc;">{formatdate(register.delivery_date) if register.delivery_date else ""}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{register.total_new_stock_qty}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{float(register.total_covers or 0):.2f}</td>'
        html += '</tr>'
        grand_total_qty += register.total_new_stock_qty
    if not packed_dns and not stock_entry:
        html += '<tr><td colspan="6" style="text-align:center; border: 1px solid #ccc;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html

    # Step 5: Add Grand Total Row
    html += '<tr style="background-color: #f0f0f0; font-weight: bold;">'
    html += '<td colspan="4" style="border: 1px solid #ccc; text-align:center">Grand Total</td>'
    html += f'<td style="text-align:right; border: 1px solid #ccc;">{grand_total_qty}</td>'
    html += f'<td style="text-align:right; border: 1px solid #ccc;">{grand_total_covers}</td>'
    html += '</tr>'

    html += '</tbody></table></div>'
    return html


@frappe.whitelist()
def get_packed_dn_summary_dispatched_html():
    from frappe.utils import formatdate, flt

    html = '<div class="tfp-summary-table" style="overflow-x:auto;">'
    html += '<table class="table table-bordered" style="border-collapse: collapse; width: 100%;">'

    headers = ["DN ID", "SO ID", "Customer", "Delivery Date", "Total QTY", "Total Covers"]
    html += '<thead><tr style="background-color: #002060; color: white; text-align: center;">'
    for h in headers:
        html += f'<th style="padding: 8px; border: 1px solid #ccc;">{h}</th>'
    html += '</tr></thead><tbody>'

    # Step 1: Get all Packed Delivery Notes
    packed_dns = frappe.db.get_all("Delivery Note",
        filters={"custom_delivery_status_new": "Dispatched", "docstatus": 1},
        fields=["name", "custom_delivery_date", "total_qty", "custom_total_covers"],order_by="custom_delivery_date asc"
    )


    # Step 2: Get all DN Items linked to SO
    dn_names = [d.name for d in packed_dns]
    dn_items = frappe.db.get_all("Delivery Note Item",
        filters={"parent": ["in", dn_names], "against_sales_order": ["!=", ""]},
        fields=["parent", "against_sales_order"]
    )

    # Step 3: Build Summary Data
    summary = {}
    grand_total_qty = 0
    grand_total_covers = 0

    for dn_doc in packed_dns:
        dn = dn_doc.name
        dn_date = dn_doc.custom_delivery_date
        total_qty = flt(dn_doc.total_qty)
        total_covers = flt(dn_doc.custom_total_covers)

        grand_total_qty += total_qty
        grand_total_covers += total_covers

        # Get all SOs linked to this DN
        linked_sos = list(set([
            d.against_sales_order for d in dn_items if d.parent == dn and d.against_sales_order
        ]))

        if not linked_sos:
            key = (dn, "")
            summary[key] = {
                "dn": dn,
                "so": "",
                "customer": "",
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }

        for so in linked_sos:
            customer = frappe.db.get_value("Sales Order", so, "customer") or ""
            key = (dn, so)

            summary[key] = {
                "dn": dn,
                "so": so,
                "customer": customer,
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }

    # Step 4: Render HTML rows
    for (dn, so), data in summary.items():
        html += '<tr>'
        html+=f'<td style="text-align:left;"><a href="/app/delivery-note/{data["dn"]}" target="_blank">{data["dn"]}</a></td>'
        html += f'<td style="border: 1px solid #ccc;text-align:left">{data["so"]}</td>'
        html += f'<td style="border: 1px solid #ccc;text-align:left">{data["customer"]}</td>'
        html += f'<td style="border: 1px solid #ccc;">{formatdate(data["dn_date"]) if data["dn_date"] else ""}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{data["total_qty"]}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{data["total_covers"]}</td>'
        html += '</tr>'
    stock_entry = frappe.db.get_all("VM Stock Register", {"status": "Dispatched","docstatus":1}, ["name"])
    for i in stock_entry:
        if not i["name"]:
            continue
        register = frappe.get_doc("VM Stock Register", i["name"])
        html += '<tr>'
        html += f'<td style="text-align:left;" colspan="2"><a href="/app/vm-stock-register/{i["name"]}" target="_blank">{i["name"]}</a></td>'
        html += f'<td style="border: 1px solid #ccc;text-align:left">Precision-Employee</td>'
        html += f'<td style="border: 1px solid #ccc;">{formatdate(register.delivery_date) if register.delivery_date else ""}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{register.total_new_stock_qty}</td>'
        html += f'<td style="text-align:right; border: 1px solid #ccc;">{float(register.total_covers or 0):.2f}</td>'
        html += '</tr>'
        grand_total_qty += register.total_new_stock_qty
        grand_total_covers += register.total_covers
    if not packed_dns and not stock_entry:
        html += '<tr><td colspan="6" style="text-align:center; border: 1px solid #ccc;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html
    # Step 5: Add Grand Total Row
    html += '<tr style="background-color: #f0f0f0; font-weight: bold;">'
    html += '<td colspan="4" style="border: 1px solid #ccc; text-align:right">Grand Total</td>'
    html += f'<td style="text-align:right; border: 1px solid #ccc;">{grand_total_qty}</td>'
    html += f'<td style="text-align:right; border: 1px solid #ccc;">{grand_total_covers}</td>'
    html += '</tr>'

    html += '</tbody></table></div>'
    return html

@frappe.whitelist()
def get_tfp_plan_html_plan_update():
    from frappe.utils import formatdate, flt

    headers = ["Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery"]

    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th colspan="1">Sr</th>
            <th colspan="3">SO</th>
            <th colspan="1">PRT</th>
            <th colspan="3">Customer</th>
            <th colspan="1">Packing</th>
            <th colspan="2">Delivery</th>
            <th colspan="2">Action</th>
        </tr>'''
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = 0
    grand_total_stock_qty = 0
    grand_total_covers = 0
    grand_total_2p = 0
    grand_total_bag = 0
    grand_total_box = 0

    so_list = frappe.db.get_all("Sales Order", {
        "service": "TFP",
        "status": "To Deliver and Bill"
    }, ["name", "customer", "custom_packing_on", "delivery_date","custom_priority"])

    if not so_list:
        html += '<tr><td colspan="6" style="text-align:center;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html

    for so in so_list:
        items = frappe.db.get_all("Sales Order Item", {"parent": so.name}, [
            "item_code", "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p",
            "custom_2nd_packing", "custom_name_print", "custom_tertiary_packingbox", "custom_bag", "custom_box",
            "custom_wrd_uom", "custom_wrd_rate", "custom_packing_on"
        ])
        show_dn = all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        )

        # button_html = f'''
        #     <button class="action-btn {'create-dn-btn' if show_dn else 'create-mr-btn'}" data-so="{so.name}">
        #         {"Create DN" if show_dn else "Create MR"}
        #     </button>
        # '''
        button_html = f'''
    <button class="action-btn {'create-dn-btn' if show_dn else 'create-mr-btn'}" data-so="{so.name}"
        style="background-color: #f5f5f5 ; border: none; outline: none; box-shadow: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">
        {"Create DN" if show_dn else "Create MR"}
    </button>
'''


        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-sos="{so.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{so.name}</td>
            <td colspan="1"></td>
            <td colspan="3" style="text-align:left;">{so.customer}</td>
            <td colspan="1" style="text-align:center;">{formatdate(so.custom_packing_on)}</td>
            <td colspan="2" style="text-align:center;">{formatdate(so.delivery_date)}</td>
            <td colspan="2" style="text-align:center;">{button_html}</td>
        </tr>
        <tr class="details-row sos-{so.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">Stock Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="2">WRD Details</td>
            <td style="text-align:center;" colspan="2">Name Details</td>
        </tr>
        '''


        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = 0
        for item in items:
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)

            primary = frappe.db.get_value("Item", item.custom_cover_type, "item_name") or ''
            secondary = frappe.db.get_value("Item", item.custom_packing_type, "item_name") or ''
            tertiary = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

            cr_stock = frappe.db.get_value("Bin", {
                "item_code": item.item_code,
                "warehouse": "Stores - TFP"
            }, "actual_qty") or 0

            stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                if flt(item.stock_qty) <= cr_stock else \
                '<span style="color: red; font-weight: bold;">Out of Stock</span>'
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''

            html += f'''
            <tr class="details-row sos-{so.name}" style="display:none;">
                <td style="text-align:left;">{item.item_name}</td>
                <td style="text-align:right;">{item.qty}</td>
                <td style="text-align:center;">{item.uom}</td>
                <td style="text-align:right;">{item.stock_qty}</td>
                <td style="text-align:right;">{cr_stock}</td>
                <td style="text-align:center;">{stock_status}</td>
                <td style="text-align:center;">{item.stock_uom}</td>
                <td style="text-align:right;">{item.mrp}</td>
                <td style="text-align:left;">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                <td style="text-align:left;" colspan="2">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                <td style="text-align:center;" colspan="2">{item.custom_name_print or ""}</td>
            </tr>
            '''

        go_status = "CREATE DN" if all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        ) else "CREATE MR"

        html += f'''
        <tr class="details-row sos-{so.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:right; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{go_status}</td>
                <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''

        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1

    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:right; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="10" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const sos = this.dataset.sos;
                const rows = document.querySelectorAll(".sos-" + sos);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
        document.querySelectorAll(".create-dn-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_dn_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Delivery Note created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});

        document.querySelectorAll(".create-mr-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_mr_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Material Request created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});
    </script>
    '''
    

    return html


@frappe.whitelist()
def get_tfp_plan_html_plan_update_new():
    from frappe.utils import formatdate, flt

    headers = ["Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery"]

    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th colspan="1">Sr</th>
            <th colspan="3">SO</th>
            <th colspan="1">PRT</th>
            <th colspan="3">Customer</th>
            <th colspan="1">Packing Date</th>
            <th colspan="1">Delivery Date</th>
            <th colspan="1">Balance Qty</th>
            <th colspan="2">Action</th>
        </tr>'''
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = 0
    grand_total_stock_qty = 0
    grand_total_covers = 0
    grand_total_2p = 0
    grand_total_bag = 0
    grand_total_box = 0
    so_list = frappe.db.get_all("Sales Order", {
        "service": "TFP",
        "status": "To Deliver and Bill"
    }, ["name", "customer", "custom_packing_on", "delivery_date","per_delivered","custom_priority"], order_by="custom_packing_on asc")

    if not so_list:
        html += '<tr><td colspan="12" style="text-align:center;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html

    for so in so_list:
        balance_qty=0
        items = frappe.db.get_all("Sales Order Item", {"parent": so.name}, [
            "item_code", "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p",
            "custom_2nd_packing", "custom_name_print", "custom_tertiary_packingbox", "custom_bag", "custom_box",
            "custom_wrd_uom", "custom_wrd_rate", "custom_packing_on","delivered_qty","ordered_qty"
        ])
        show_dn = all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        )
        for i in items:
            item_qty = flt(i.qty or 0)
            delivered = flt(i.delivered_qty or 0)
            item_balanced_qty = item_qty - delivered
            balance_qty += item_balanced_qty
            

        button_html = f'''
    <button class="action-btn {'create-dn-btn' if show_dn else 'create-mr-btn'}" data-so="{so.name}"
        style="background-color: #f5f5f5 ; border: none; outline: none; box-shadow: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;color: {'green' if show_dn else 'red'};">
        {"Create DN" if show_dn else "Create MR"}
    </button>
'''


        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-sos="{so.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{so.name}</td>
            <td colspan="1" style="text-align:center">{so.custom_priority or ""}</td>
            <td colspan="3" style="text-align:left;">{so.customer}</td>
            <td colspan="1" style="text-align:center;">{formatdate(so.custom_packing_on)}</td>
            <td colspan="1" style="text-align:center;">{formatdate(so.delivery_date)}</td>
            <td colspan="1" style="text-align:center;">{float(balance_qty):.2f}</td>
            <td colspan="2" style="text-align:center;">{button_html}</td>
        </tr>
        <tr class="details-row sos-{so.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
             <td style="text-align:center;">PO Qty</td>
            <td style="text-align:center;">Req. Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="1">WRD Details</td>
            <td style="text-align:center;" colspan="1">Balance Qty</td>
            <td style="text-align:center;" colspan="1">Name Details</td>
            
        </tr>
        '''


        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = total_vm_qty=total_vm_stock=total_po_qty=0
        for item in items:
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_po_qty+=flt(item.ordered_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)
            primary=''
            secondary=''
            tertiary=''
            if item.custom_cover_type:
                primary = frappe.db.get_value("Item", item.custom_cover_type, "item_name") or ''
            if item.custom_packing_type:
                secondary = frappe.db.get_value("Item", item.custom_packing_type, "item_name") or ''
            if item.custom_tertiary_packingbox:
                tertiary = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

            cr_stock = frappe.db.get_value("Bin", {
                "item_code": item.item_code,
                "warehouse": "Stores - TFP"
            }, "actual_qty") or 0

            stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                if flt(item.stock_qty) <= cr_stock else \
                '<span style="color: red; font-weight: bold;">Out of Stock</span>'
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            if (item.qty - (item.delivered_qty or 0)) > 0:
                item_balance_qty = flt(item.qty - (item.delivered_qty or 0))

                html += f'''
                <tr class="details-row sos-{so.name}" style="display:none;">
                    <td style="text-align:left;">{item.item_name}</td>
                    <td style="text-align:center;">{item.qty}</td>
                    <td style="text-align:center;">{item.uom}</td>
                    <td style="text-align:center;">{item.ordered_qty}</td>
                    <td style="text-align:center;">{item.stock_qty}</td>
                    <td style="text-align:center;">{cr_stock}</td>
                    <td style="text-align:center;">{stock_status}</td>
                    <td style="text-align:center;">{item.stock_uom}</td>
                    <td style="text-align:right;">{item.mrp}</td>
                    <td style="text-align:left;">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                    <td style="text-align:left;" colspan="1">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                    <td style="text-align:center;" colspan="1">{item_balance_qty:.2f}</td>
                    <td style="text-align:center;" colspan="1">{item.custom_name_print or ""}</td>
                    
                </tr>
                '''

        go_status = "CREATE DN" if all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        ) else "CREATE MR"

        html += f'''
        <tr class="details-row sos-{so.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_po_qty}</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{go_status}</td>
                <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''

        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1
    stock_entry=frappe.db.get_all("Stock Entry",{"custom_vm_stock_register":("!=",""),"docstatus":0,"stock_entry_type":"Material Transfer"},["name","custom_vm_stock_register"])
    slot_tables = ["slot_a", "slot_b", "slot_c", "slot_d", "slot_e", "slot_f"]

    for i in stock_entry:
        if not i.custom_vm_stock_register:
            continue
        register = frappe.get_doc("VM Stock Register", i.custom_vm_stock_register)
        vm_items = [item for table in slot_tables for item in register.get(table)]
        show_submit = all(
            flt(item.stock_qty or 0) <= (frappe.db.get_value("Bin", {"item_code": item.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for item in vm_items if item.item_code
        )

       
        vm_button_html = f'''
            <button class="{"submit-stock-btn" if show_submit else "create-mr-vm-batch-btn"}"
                data-vm-reg="{register.name}"
                style="background-color: #f5f5f5; border: none; outline: none; box-shadow: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; color: {'green' if show_submit else 'red'};">
                {"Submit Stock" if show_submit else "Create MR"}
            </button>
        '''


        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-sos="{register.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{register.name}</td>
            <td colspan="1" style="text-align:center"></td>
            <td colspan="3" style="text-align:left;">Precision-Employee</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.packing_date) if register.packing_date else ""}</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.delivery_date) if register.delivery_date else ""}</td>
            <td colspan="1" style="text-align:center;">{float(register.total_new_stock_qty):.2f}</td>
            <td colspan="2" style="text-align:center;">{vm_button_html}</td>
        </tr>
        <tr class="details-row sos-{register.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">PO Qty</td>
            <td style="text-align:center;">Req .Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="2">WRD Details</td>
            <td style="text-align:center;" colspan="1">Name Details</td>
        </tr>
        '''

        for table in slot_tables:
            for item in register.get(table):
                cr_stock = frappe.db.get_value("Bin", {
                    "item_code": item.item_code,
                    "warehouse": "Stores - TFP"
                }, "actual_qty") or 0

                total_grams = flt(item.new_stock_qty) * flt(item.new_stockuom)

                uom = (item.stock_uom or "").lower()
                if "gm" in uom:
                    total_kg = total_grams / 1000
                else:
                    total_kg = total_grams

                
                stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                    if total_kg <= cr_stock else \
                    '<span style="color: red; font-weight: bold;">Out of Stock</span>'
                primary_1=''
                secondary_1=''
                tertiary_1=''
                
                if item.custom_primary_packing_cover:
                    primary_1 = frappe.db.get_value("Item", item.custom_primary_packing_cover, "item_name") or ''
                if item.custom_secondary_packing_bag:
                    secondary_1 = frappe.db.get_value("Item", item.custom_secondary_packing_bag, "item_name") or ''
                if item.custom_tertiary_packingbox:
                    tertiary_1 = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

                item_rate = f"{float(item.custom_mrp_r):.2f}" if item.custom_mrp_r else ""
                balance_qty = flt(item.new_stock_qty or 0)
                if item.item_code:
                    total_vm_qty+= flt(item.new_stock_qty)
                    grand_total_qty += total_vm_qty
                    total_vm_stock+= flt(item.stock_qty)
                    html += f'''
                    <tr class="details-row sos-{register.name}" style="display:none;">
                        <td style="text-align:left;">{item.item_name}</td>
                        <td style="text-align:center;">{item.new_stock_qty}</td>
                        <td style="text-align:center;">{item.new_stockuom}</td>
                         <td style="text-align:center;">0</td>
                        <td style="text-align:center;">{item.stock_qty}</td>
                        <td style="text-align:center;">{cr_stock}</td>
                        <td style="text-align:center;">{stock_status}</td>
                        <td style="text-align:center;">{item.stock_uom or ""}</td>
                        <td style="text-align:right;">{item.custom_mrp}</td>
                        <td style="text-align:left;">(C): {primary_1 or "None"}: {item.custom_covers or "0"}<br>(B): {secondary_1 or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary_1 or "None"}: {item.custom_box or "0"}</td>
                        <td style="text-align:left;" colspan="2">(W): {item.custom_weight_w or ""}<br>(R): {item_rate}<br>(D): {formatdate(item.custom_manufactured_date_d) if item.custom_manufactured_date_d else ""}</td>
                        <td style="text-align:center;" colspan="1">{item.custom_name_print or ""}</td>
                    </tr>
                    '''
        html += f'''
        <tr class="details-row sos-{register.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_vm_qty}</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_po_qty}</td>
                <td style="text-align:center; border: 1px solid #ccc;">0</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_vm_stock}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;"></td>
                <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''
        s_no += 1
    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="10" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const sos = this.dataset.sos;
                const rows = document.querySelectorAll(".sos-" + sos);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
        document.querySelectorAll(".create-dn-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_dn_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Delivery Note created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});

        document.querySelectorAll(".create-mr-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_mr_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Material Request created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});
        document.querySelectorAll(".submit-stock-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const vm_stock_reg = this.dataset.vmReg;
                frappe.call({{
                    method: "teampro.teampro.page.finance_details.tfp_dashboard.submit_stock_entry_from_vm_register",
                    args: {{ vm_stock_register: vm_stock_reg }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Stock Entry submitted: " + r.message);
                        }} else {{
                            frappe.msgprint("Failed to submit stock entry.");
                        }}
                    }}
                }});
            }});
        }});
        document.querySelectorAll(".create-mr-vm-batch-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const vm_stock_reg = this.dataset.vmReg;
                frappe.call({{
                    method: "teampro.teampro.page.finance_details.tfp_dashboard.create_mr_from_vm_item",
                    args: {{ vm_stock_register: vm_stock_reg }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Material Request created: " + r.message);
                        }} else {{
                            frappe.msgprint("Failed to create MR.");
                        }}
                    }}
                }});
            }});
        }});

    </script>
    '''
    

    return html

@frappe.whitelist()
def get_tfp_plan_html_schedule_opertaions_new():
    from frappe.utils import formatdate, flt

    headers = [
        "Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery", "Item Name", "QTY", "UOM",
        "St.QTY", "UOM","MRP","Packing Details","WRD Details",
        "Name Print"
    ]
    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Sr</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">SO</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">PRT</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="3">Customer</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Packing Date</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Delivery Date</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">Packed Qty</th>
            <th style="position: sticky; top: 0; text-align: center;background-color: #002060; color: white;" colspan="1">DN</th>

        </tr>'''
    
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = grand_total_stock_qty = grand_total_covers = grand_total_2p = grand_total_bag = grand_total_box = 0

    dn_list = frappe.db.get_all("Delivery Note", {
        "custom_delivery_status_new": "Schedule","docstatus":1,"is_return":0
    }, ["name", "customer", "custom_delivery_date","custom_packing_on","custom_priority"], order_by="custom_packing_on asc")
    if not dn_list:
        html += '<tr><td colspan="12" style="text-align:center;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html
    for dn in dn_list:
        balance_qty=0
        items = frappe.db.get_all("Delivery Note Item", {
            "parent": dn.name
        }, [
            "item_name","item_code", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p","custom_name_print","custom_tertiary_packingbox","custom_bag","custom_box",
            "custom_wrd_uom","custom_wrd_rate","custom_packing_on", "against_sales_order","custom_per_3p",""
        ])

        if not items:
            continue
        for i in items:
            balance_qty += flt(i.qty or 0)
        rowspan = len(items)
        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box =0
        primary=''
        secondary=''
        tertiary=''
        for idx, item in enumerate(items):
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)
            if item.custom_cover_type:
                primary=frappe.db.get_value("Item",item.custom_cover_type,"item_name") or ''
            if item.custom_packing_type:
                secondary=frappe.db.get_value("Item",item.custom_packing_type,"item_name") or ''
            if item.custom_tertiary_packingbox:
                tertiary=frappe.db.get_value("Item",item.custom_tertiary_packingbox,"item_name") or ''
            html += '<tr>'
            if idx == 0:
                
                html += f'''
                    <tr style="font-weight:bold; background-color:#f2f2f2;">
                        <td style="text-align:left;"colspan="1">
                            {s_no}
                        </td>
                        <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-dos="{item.against_sales_order}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button> {item.against_sales_order}</td>
                        <td colspan="1" style="text-align:center">{dn.custom_priority or ""}</td>
                        <td colspan="3" style="text-align:left;">{dn.customer}</td>
                        <td style="text-align:center;"colspan="1">{formatdate(dn.custom_packing_on)}</td>
                        <td style="text-align:center;" colspan="1">{formatdate(dn.custom_delivery_date)}</td>
                        <td style="text-align:center;" colspan="1">{balance_qty}</td>
                        <td style="text-align:center;" colspan="1">
                            <a href="/app/delivery-note/{ dn.name }" target="_blank">{ dn.name }</a>
                        </td>


                    </tr>
                    <tr class="details-row dos-{item.against_sales_order}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
                        <td style="text-align:center;">Item Code</td>
                        <td style="text-align:center;">Item Name</td>
                        <td style="text-align:center;">Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">Stock Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">MRP</td>
                        <td style="text-align:center;" colspan="2">Packing Details</td>
                        <td style="text-align:center;" colspan="1">WRD Details</td>
                        <td style="text-align:center;" colspan="1">Packed Qty</td>
                        <td style="text-align:center;" colspan="1">Name Details</td>
                    </tr>'''
                
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
           
            html += f'''
                <tr class="details-row dos-{item.against_sales_order}" style="display:none;">
                    <td style="text-align:left;">{item.item_code}</td>
                    <td style="text-align:left;">{item.item_name}</td>
                    <td style="text-align:center;">{item.qty}</td>
                    <td style="text-align:center;">{item.uom}</td>
                    <td style="text-align:center;">{item.stock_qty}</td>
                    <td style="text-align:center;">{item.stock_uom}</td>
                    <td style="text-align:right;">{item.mrp}</td>
                    <td style="text-align:left;" colspan="2">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                    <td style="text-align:left;" colspan="1">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                    <td style="text-align:center;">{item.qty}</td>
                    <td style="text-align:center;">{item.custom_name_print or ""}</td>
                    
                </tr>
                '''
            

        html += f'''
        <tr class="details-row dos-{item.against_sales_order}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="2" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="3" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;"></td>
            <td colspan="6" style="text-align:right;"></td>
        </tr>
        '''


        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1
    stock_entry=frappe.db.get_all("VM Stock Register",{"status":"Schedule","docstatus":1},["name"])
    slot_tables = ["slot_a", "slot_b", "slot_c", "slot_d", "slot_e", "slot_f"]

    for i in stock_entry:
        stock=frappe.db.get_value("Stock Entry",{"docstatus":1,"custom_vm_stock_register":i.name},["name"])
        total_vm_qty=total_vm_stock=0
        if not i.name:
            continue
        register = frappe.get_doc("VM Stock Register", i.name)
        
        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-dos="{register.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{register.name}</td>
            <td colspan="1" style="text-align:center"></td>
            <td colspan="3" style="text-align:left;">Precision-Employee</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.packing_date) if register.packing_date else ""}</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.delivery_date) if register.delivery_date else ""}</td>
            <td colspan="1" style="text-align:center;">{float(register.total_new_stock_qty):.2f}</td>
            <td colspan="2" style="text-align:center;"><a href="/app/stock-entry/{ stock }" target="_blank">{ stock }</a></td>
            
        </tr>
        <tr class="details-row dos-{register.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">Stock Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="2">WRD Details</td>
            <td style="text-align:center;" colspan="1">Name Details</td>
        </tr>
        '''

        for table in slot_tables:
            for item in register.get(table):
                cr_stock = frappe.db.get_value("Bin", {
                    "item_code": item.item_code,
                    "warehouse": "Stores - TFP"
                }, "actual_qty") or 0

                stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                    if flt(item.stock_qty) <= cr_stock else \
                    '<span style="color: red; font-weight: bold;">Out of Stock</span>'
                primary_1=''
                secondary_1=''
                tertiary_1=''
                if item.custom_primary_packing_cover:
                    primary_1 = frappe.db.get_value("Item", item.custom_primary_packing_cover, "item_name") or ''
                if item.custom_secondary_packing_bag:
                    secondary_1 = frappe.db.get_value("Item", item.custom_secondary_packing_bag, "item_name") or ''
                if item.custom_tertiary_packingbox:
                    tertiary_1 = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

                item_rate = f"{float(item.custom_mrp_r):.2f}" if item.custom_mrp_r else ""
                balance_qty = flt(item.new_stock_qty or 0)
                if item.item_code:
                    total_vm_qty+= flt(item.new_stock_qty)
                    total_vm_stock+= flt(item.stock_qty)
                    html += f'''
                    <tr class="details-row dos-{register.name}" style="display:none;">
                        <td style="text-align:left;">{item.item_name}</td>
                        <td style="text-align:center;">{item.new_stock_qty}</td>
                        <td style="text-align:center;">{item.new_stockuom}</td>
                        <td style="text-align:center;">{item.stock_qty}</td>
                        <td style="text-align:center;">{cr_stock}</td>
                        <td style="text-align:center;">{stock_status}</td>
                        <td style="text-align:center;">{item.stock_uom or ""}</td>
                        <td style="text-align:right;">{item.custom_mrp}</td>
                        <td style="text-align:left;">(C): {primary_1 or "None"}: {item.custom_covers or "0"}<br>(B): {secondary_1 or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary_1 or "None"}: {item.custom_box or "0"}</td>
                        <td style="text-align:left;" colspan="2">(W): {item.custom_weight_w or ""}<br>(R): {item_rate}<br>(D): {formatdate(item.custom_manufactured_date_d) if item.custom_manufactured_date_d else ""}</td>
                        <td style="text-align:center;" colspan="1">{item.custom_name_print or ""}</td>
                    </tr>
                    '''
        html += f'''
        <tr class="details-row dos-{register.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_vm_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_vm_stock}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;"></td>
                <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''
        s_no += 1

    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="8" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const dos = this.dataset.dos;
                const rows = document.querySelectorAll(".dos-" + dos);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
    </script>
    '''
    return html

@frappe.whitelist()
def get_tfp_plan_html_plan_update_stock():
    from frappe.utils import formatdate, flt
    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th colspan="1">Sr</th>
            <th colspan="3">SO</th>
            <th colspan="1">PRT</th>
            <th colspan="3">Customer</th>
            <th colspan="1">Packing Date</th>
            <th colspan="1">Delivery Date</th>
            <th colspan="1">Balance Qty</th>
            <th colspan="2">Action</th>
        </tr>'''
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = 0
    grand_total_stock_qty = 0
    grand_total_covers = 0
    grand_total_2p = 0
    grand_total_bag = 0
    grand_total_box = 0
    so_list = frappe.db.get_all("Sales Order", {
        "service": "TFP",
        "status": "To Deliver and Bill"
    }, ["name", "customer", "custom_packing_on", "delivery_date","per_delivered","custom_priority"], order_by="custom_packing_on asc")

    if not so_list:
        html += '<tr><td colspan="6" style="text-align:center;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html

    for so in so_list:
        balance_qty=0
        items = frappe.db.get_all("Sales Order Item", {"parent": so.name}, [
            "item_code", "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p",
            "custom_2nd_packing", "custom_name_print", "custom_tertiary_packingbox", "custom_bag", "custom_box",
            "custom_wrd_uom", "custom_wrd_rate", "custom_packing_on","delivered_qty"
        ])
        show_dn = all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        )
        for i in items:
            item_qty = flt(i.qty or 0)
            delivered = flt(i.delivered_qty or 0)
            item_balanced_qty = item_qty - delivered
            balance_qty += item_balanced_qty
            

        button_html = f'''
    <button class="action-btn {'create-dn-btn' if show_dn else 'create-mr-btn'}" data-so="{so.name}"
        style="background-color: #f5f5f5 ; border: none; outline: none; box-shadow: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;color: {'green' if show_dn else 'red'};">
        {"Create DN" if show_dn else "Create MR"}
    </button>
'''


        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-sos="{so.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{so.name}</td>
            <td colspan="1" style="text-align:center">{so.custom_priority or ""}</td>
            <td colspan="3" style="text-align:left;">{so.customer}</td>
            <td colspan="1" style="text-align:center;">{formatdate(so.custom_packing_on)}</td>
            <td colspan="1" style="text-align:center;">{formatdate(so.delivery_date)}</td>
            <td colspan="1" style="text-align:center;">{float(balance_qty):.2f}</td>
            <td colspan="2" style="text-align:center;">{button_html}</td>
        </tr>
        <tr class="details-row sos-{so.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">Stock Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="1">WRD Details</td>
            <td style="text-align:center;" colspan="1">Balance Qty</td>
            <td style="text-align:center;" colspan="1">Name Details</td>
            
        </tr>
        '''


        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = total_vm_qty=total_vm_stock=0
        for item in items:
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)

            primary = frappe.db.get_value("Item", item.custom_cover_type, "item_name") or ''
            secondary = frappe.db.get_value("Item", item.custom_packing_type, "item_name") or ''
            tertiary = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

            cr_stock = frappe.db.get_value("Bin", {
                "item_code": item.item_code,
                "warehouse": "Stores - TFP"
            }, "actual_qty") or 0

            stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                if flt(item.stock_qty) <= cr_stock else \
                '<span style="color: red; font-weight: bold;">Out of Stock</span>'
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            if (item.qty - (item.delivered_qty or 0)) > 0:
                item_balance_qty = flt(item.qty - (item.delivered_qty or 0))

                html += f'''
                <tr class="details-row sos-{so.name}" style="display:none;">
                    <td style="text-align:left;">{item.item_name}</td>
                    <td style="text-align:center;">{item.qty}</td>
                    <td style="text-align:center;">{item.uom}</td>
                    <td style="text-align:center;">{item.stock_qty}</td>
                    <td style="text-align:center;">{cr_stock}</td>
                    <td style="text-align:center;">{stock_status}</td>
                    <td style="text-align:center;">{item.stock_uom}</td>
                    <td style="text-align:right;">{item.mrp}</td>
                    <td style="text-align:left;">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                    <td style="text-align:left;" colspan="1">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                    <td style="text-align:center;" colspan="1">{item_balance_qty:.2f}</td>
                    <td style="text-align:center;" colspan="1">{item.custom_name_print or ""}</td>
                    
                </tr>
                '''

        go_status = "CREATE DN" if all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        ) else "CREATE MR"

        html += f'''
        <tr class="details-row sos-{so.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{go_status}</td>
                <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''

        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1
    
    stock_entry=frappe.db.get_all("VM Stock Register",{"status":"Schedule"},["name"])
    slot_tables = ["slot_a", "slot_b", "slot_c", "slot_d", "slot_e", "slot_f"]

    for i in stock_entry:
        if not i.custom_vm_stock_register:
            continue
        register = frappe.get_doc("VM Stock Register", i.custom_vm_stock_register)
        
        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-sos="{register.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{register.name}</td>
            <td colspan="1" style="text-align:center"></td>
            <td colspan="3" style="text-align:left;">Precision-Employee</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.packing_date) if register.packing_date else ""}</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.delivery_date) if register.delivery_date else ""}</td>
            <td colspan="1" style="text-align:center;"></td>
            <td colspan="2" style="text-align:center;"></td>
        </tr>
        <tr class="details-row sos-{register.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">Stock Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="2">WRD Details</td>
            <td style="text-align:center;" colspan="1">Name Details</td>
        </tr>
        '''

        for table in slot_tables:
            for item in register.get(table):
                cr_stock = frappe.db.get_value("Bin", {
                    "item_code": item.item_code,
                    "warehouse": "Stores - TFP"
                }, "actual_qty") or 0

                stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                    if flt(item.stock_qty) <= cr_stock else \
                    '<span style="color: red; font-weight: bold;">Out of Stock</span>'
                primary_1=''
                secondary_1=''
                tertiary_1=''
                if item.custom_primary_packing_cover:
                    primary_1 = frappe.db.get_value("Item", item.custom_primary_packing_cover, "item_name") or ''
                if item.custom_secondary_packing_bag:
                    secondary_1 = frappe.db.get_value("Item", item.custom_secondary_packing_bag, "item_name") or ''
                if item.custom_tertiary_packingbox:
                    tertiary_1 = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

                item_rate = f"{float(item.custom_mrp_r):.2f}" if item.custom_mrp_r else ""
                balance_qty = flt(item.new_stock_qty or 0)
                if item.item_code:
                    total_vm_qty+= flt(item.new_stock_qty)
                    total_vm_stock+= flt(item.stock_qty)
                    html += f'''
                    <tr class="details-row sos-{register.name}" style="display:none;">
                        <td style="text-align:left;">{item.item_name}</td>
                        <td style="text-align:center;">{item.new_stock_qty}</td>
                        <td style="text-align:center;">{item.new_stockuom}</td>
                        <td style="text-align:center;">{item.stock_qty}</td>
                        <td style="text-align:center;">{cr_stock}</td>
                        <td style="text-align:center;">{stock_status}</td>
                        <td style="text-align:center;">{item.stock_uom or ""}</td>
                        <td style="text-align:right;">{item.custom_mrp}</td>
                        <td style="text-align:left;">(C): {primary_1 or "None"}: {item.custom_covers or "0"}<br>(B): {secondary_1 or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary_1 or "None"}: {item.custom_box or "0"}</td>
                        <td style="text-align:left;" colspan="2">(W): {item.custom_weight_w or ""}<br>(R): {item_rate}<br>(D): {formatdate(item.custom_manufactured_date_d) if item.custom_manufactured_date_d else ""}</td>
                        <td style="text-align:center;" colspan="1">{item.custom_name_print or ""}</td>
                    </tr>
                    '''
        html += f'''
        <tr class="details-row sos-{register.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_vm_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_vm_stock}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;"></td>
                <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''
        s_no += 1


    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="10" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const sos = this.dataset.sos;
                const rows = document.querySelectorAll(".sos-" + sos);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
        document.querySelectorAll(".create-dn-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_dn_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Delivery Note created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});

        document.querySelectorAll(".create-mr-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_mr_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Material Request created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});
    </script>
    '''
    

    return html

@frappe.whitelist()
def get_tfp_plan_html_vm():
    from frappe.utils import formatdate, flt

    headers = ["Sr", "SO ID", "PRT", "Customer Name", "Packing", "Delivery"]

    html = '''
    <div class="tfp-table-wrapper" style="max-height: 600px; overflow: auto; display: block; border: 1px solid #ccc;">
    <style>
        .tfp-table-wrapper td, .tfp-table-wrapper th {
            padding: 6px;
            vertical-align: middle;
            border: 1px solid #ccc;
        }
    </style>
    <table class="table table-bordered" style="border-collapse: collapse; width: 100%; table-layout: auto;">
    '''
    html += f''' <tr style="background-color: #002060; color: white;">
            <th colspan="1">Sr</th>
            <th colspan="3">SO</th>
            <th colspan="1">PRT</th>
            <th colspan="3">Customer</th>
            <th colspan="1">Packing Date</th>
            <th colspan="1">Delivery Date</th>
            <th colspan="1">Balance Qty</th>
            <th colspan="2">Action</th>
        </tr>'''
    
    html += '</tr></thead><tbody>'

    s_no = 1
    grand_total_qty = 0
    grand_total_stock_qty = 0
    grand_total_covers = 0
    grand_total_2p = 0
    grand_total_bag = 0
    grand_total_box = 0
    so_list = frappe.db.get_all("Sales Order", {
        "service": "TFP",
        "status": "To Deliver and Bill"
    }, ["name", "customer", "custom_packing_on", "delivery_date","per_delivered","custom_priority"], order_by="custom_packing_on asc")

    if not so_list:
        html += '<tr><td colspan="6" style="text-align:center;">Nothing to show</td></tr>'
        html += '</tbody></table></div>'
        return html

    for so in so_list:
        balance_qty=0
        items = frappe.db.get_all("Sales Order Item", {"parent": so.name}, [
            "item_code", "item_name", "qty", "uom", "stock_qty", "stock_uom", "custom_cover_type", "mrp",
            "custom_mfg_on", "custom_covers", "custom_packing_type", "custom_per_2p",
            "custom_2nd_packing", "custom_name_print", "custom_tertiary_packingbox", "custom_bag", "custom_box",
            "custom_wrd_uom", "custom_wrd_rate", "custom_packing_on","delivered_qty"
        ])
        show_dn = all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        )
        for i in items:
            item_qty = flt(i.qty or 0)
            delivered = flt(i.delivered_qty or 0)
            item_balanced_qty = item_qty - delivered
            balance_qty += item_balanced_qty
            

        button_html = f'''
    <button class="action-btn {'create-dn-btn' if show_dn else 'create-mr-btn'}" data-so="{so.name}"
        style="background-color: #f5f5f5 ; border: none; outline: none; box-shadow: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;color: {'green' if show_dn else 'red'};">
        {"Create DN" if show_dn else "Create MR"}
    </button>
'''


        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;"><button class="toggle-btn" data-sos="{so.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>{so.name}</td>
            <td colspan="1" style="text-align:center">{so.custom_priority or ""}</td>
            <td colspan="3" style="text-align:left;">{so.customer}</td>
            <td colspan="1" style="text-align:center;">{formatdate(so.custom_packing_on)}</td>
            <td colspan="1" style="text-align:center;">{formatdate(so.delivery_date)}</td>
            <td colspan="1" style="text-align:center;">{float(balance_qty):.2f}</td>
            <td colspan="2" style="text-align:center;">{button_html}</td>
        </tr>
        <tr class="details-row sos-{so.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">Stock Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="1">WRD Details</td>
            <td style="text-align:center;" colspan="1">Balance Qty</td>
            <td style="text-align:center;" colspan="1">Name Details</td>
            
        </tr>
        '''


        total_qty = total_stock_qty = total_covers = total_2p = total_bag = total_box = total_vm_qty=total_vm_stock=0
        for item in items:
            total_qty += flt(item.qty)
            total_stock_qty += flt(item.stock_qty)
            total_covers += flt(item.custom_covers)
            total_2p += flt(item.custom_2nd_packing)
            total_bag += flt(item.custom_bag)
            total_box += flt(item.custom_box)
            primary=''
            secondary=''
            tertiary=''
            if item.custom_cover_type:
                primary = frappe.db.get_value("Item", item.custom_cover_type, "item_name") or ''
            if item.custom_packing_type:
                secondary = frappe.db.get_value("Item", item.custom_packing_type, "item_name") or ''
            if item.custom_tertiary_packingbox:
                tertiary = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") or ''

            cr_stock = frappe.db.get_value("Bin", {
                "item_code": item.item_code,
                "warehouse": "Stores - TFP"
            }, "actual_qty") or 0

            stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' \
                if flt(item.stock_qty) <= cr_stock else \
                '<span style="color: red; font-weight: bold;">Out of Stock</span>'
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            if (item.qty - (item.delivered_qty or 0)) > 0:
                item_balance_qty = flt(item.qty - (item.delivered_qty or 0))

                html += f'''
                <tr class="details-row sos-{so.name}" style="display:none;">
                    <td style="text-align:left;">{item.item_name}</td>
                    <td style="text-align:center;">{item.qty}</td>
                    <td style="text-align:center;">{item.uom}</td>
                    <td style="text-align:center;">{item.stock_qty}</td>
                    <td style="text-align:center;">{cr_stock}</td>
                    <td style="text-align:center;">{stock_status}</td>
                    <td style="text-align:center;">{item.stock_uom}</td>
                    <td style="text-align:right;">{item.mrp}</td>
                    <td style="text-align:left;">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                    <td style="text-align:left;" colspan="1">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                    <td style="text-align:center;" colspan="1">{item_balance_qty:.2f}</td>
                    <td style="text-align:center;" colspan="1">{item.custom_name_print or ""}</td>
                    
                </tr>
                '''

        go_status = "CREATE DN" if all(
            flt(it.stock_qty) <= (frappe.db.get_value("Bin", {"item_code": it.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for it in items
        ) else "CREATE MR"

        html += f'''
        <tr class="details-row sos-{so.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
        <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_qty}</td>
                <td></td>
                <td style="text-align:center; border: 1px solid #ccc;">{total_stock_qty}</td>
                <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;">{go_status}</td>
                <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''

        grand_total_qty += total_qty
        grand_total_stock_qty += total_stock_qty
        grand_total_covers += total_covers
        grand_total_2p += total_2p
        grand_total_bag += total_bag
        grand_total_box += total_box
        s_no += 1
    stock_entry = frappe.db.get_all("Stock Entry", {
        "custom_vm_stock_register": ("!=", ""),
        "docstatus": 0,
        "stock_entry_type": "Material Transfer"
    }, ["name", "custom_vm_stock_register"])

    slot_tables = ["slot_a", "slot_b", "slot_c", "slot_d", "slot_e", "slot_f"]

    for i in stock_entry:
        if not i.custom_vm_stock_register:
            continue
        register = frappe.get_doc("VM Stock Register", i.custom_vm_stock_register)

        # Check if all VM items are in stock
        vm_items = [item for table in slot_tables for item in register.get(table)]
        show_submit = all(
            flt(item.stock_qty or 0) <= (frappe.db.get_value("Bin", {"item_code": item.item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0)
            for item in vm_items if item.item_code
        )

        vm_button_html = f'''
            <button class="vm-create-mr-btn"
                data-vm-reg="{register.name}"
                style="background-color: #f5f5f5; border: none; outline: none; box-shadow: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; color: {'green' if show_submit else 'red'};">
                {"Submit Stock" if show_submit else "Create MR"}
            </button>
        '''


        html += f'''
        <tr style="font-weight:bold; background-color:#f2f2f2;">
            <td colspan="1" style="text-align:left;"> {s_no}</td>
            <td colspan="3" style="text-align:left;">
                <button class="toggle-btn" data-sos="{register.name}" style="background:none; border:none; font-weight:bold; cursor:pointer;">+</button>
                {register.name}
            </td>
            <td colspan="1" style="text-align:center"></td>
            <td colspan="3" style="text-align:left;">Precision-Employee</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.packing_date) if register.packing_date else ""}</td>
            <td colspan="1" style="text-align:center;">{formatdate(register.delivery_date) if register.delivery_date else ""}</td>
            <td colspan="1" style="text-align:center;">{float(register.total_new_stock_qty):.2f}</td>
            <td colspan="2" style="text-align:center;">{vm_button_html}</td>
        </tr>
        '''

        html += f'''
        <tr class="details-row sos-{register.name}" style="display:none; background-color: #d9e1f2; font-weight: bold;">
            <td style="text-align:center;">Item</td>
            <td style="text-align:center;">Qty</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">Stock Qty</td>
            <td style="text-align:center;background-color: #C00000; color: white;">CR. Stock</td>
            <td style="text-align:center;background-color: #C00000; color: white;">Stock Status</td>
            <td style="text-align:center;">UOM</td>
            <td style="text-align:center;">MRP</td>
            <td style="text-align:center;">Packing Details</td>
            <td style="text-align:center;" colspan="2">WRD Details</td>
            <td style="text-align:center;" colspan="1">Name Details</td>
        </tr>
        '''

        total_vm_qty = 0
        total_vm_stock = 0

        for table in slot_tables:
            for item in register.get(table):
                cr_stock = frappe.db.get_value("Bin", {
                    "item_code": item.item_code,
                    "warehouse": "Stores - TFP"
                }, "actual_qty") or 0

                stock_status = '<span style="color: green; font-weight: bold;">In Stock</span>' if flt(item.stock_qty) <= cr_stock else '<span style="color: red; font-weight: bold;">Out of Stock</span>'

                primary_1 = frappe.db.get_value("Item", item.custom_primary_packing_cover, "item_name") if item.custom_primary_packing_cover else ''
                secondary_1 = frappe.db.get_value("Item", item.custom_secondary_packing_bag, "item_name") if item.custom_secondary_packing_bag else ''
                tertiary_1 = frappe.db.get_value("Item", item.custom_tertiary_packingbox, "item_name") if item.custom_tertiary_packingbox else ''

                item_rate = f"{float(item.custom_mrp_r):.2f}" if item.custom_mrp_r else ""
                total_vm_qty += flt(item.new_stock_qty)
                total_vm_stock += flt(item.stock_qty)

                html += f'''
                <tr class="details-row sos-{register.name}" style="display:none;">
                    <td style="text-align:left;">{item.item_name}</td>
                    <td style="text-align:center;">{item.new_stock_qty}</td>
                    <td style="text-align:center;">{item.new_stockuom}</td>
                    <td style="text-align:center;">{item.stock_qty}</td>
                    <td style="text-align:center;">{cr_stock}</td>
                    <td style="text-align:center;">{stock_status}</td>
                    <td style="text-align:center;">{item.stock_uom or ""}</td>
                    <td style="text-align:right;">{item.custom_mrp}</td>
                    <td style="text-align:left;">(C): {primary_1 or "None"}: {item.custom_covers or "0"}<br>(B): {secondary_1 or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary_1 or "None"}: {item.custom_box or "0"}</td>
                    <td style="text-align:left;" colspan="2">(W): {item.custom_weight_w or ""}<br>(R): {item_rate}<br>(D): {formatdate(item.custom_manufactured_date_d) if item.custom_manufactured_date_d else ""}</td>
                    <td style="text-align:center;" colspan="1">{item.custom_name_print or ""}</td>
                </tr>
                '''

        html += f'''
        <tr class="details-row sos-{register.name}" style="display:none; font-weight:bold; background-color: #d9e1f2;">
            <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{total_vm_qty}</td>
            <td></td>
            <td style="text-align:center; border: 1px solid #ccc;">{total_vm_stock}</td>
            <td colspan="2" style="text-align:center; border: 1px solid #ccc;vertical-align: middle;"></td>
            <td></td>
            <td colspan="10" style="text-align:right;"></td>
        </tr>
        '''
        grand_total_qty += total_vm_qty
        grand_total_stock_qty += total_vm_stock
        s_no += 1
    html += f'''
        <tr style="background-color: #002060; font-weight: bold; color: white;">
         <td colspan="1" style="text-align:center; border: 1px solid #ccc;">Grand Total</td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_qty}</td>
            <td style="border: 1px solid #ccc;"></td>
            <td style="text-align:center; border: 1px solid #ccc;">{grand_total_stock_qty:.2f}</td>
            <td colspan="10" style="border: 1px solid #ccc;"></td>
        </tr>
    </tbody></table></div>
    <script>
        document.querySelectorAll(".toggle-btn").forEach(btn => {{
            btn.addEventListener("click", function() {{
                const sos = this.dataset.sos;
                const rows = document.querySelectorAll(".sos-" + sos);
                const isVisible = rows[0].style.display === "table-row";
                rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                this.textContent = isVisible ? "+" : "-";
            }});
        }});
        document.querySelectorAll(".create-dn-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_dn_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Delivery Note created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});

        document.querySelectorAll(".create-mr-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const so = this.dataset.so;
                frappe.call({{
                    method: "teampro.custom.create_mr_from_so",
                    args: {{ sales_order: so }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Material Request created: " + r.message);
                        }}
                    }}
                }});
            }});
        }});
        document.querySelectorAll(".submit-stock-btn").forEach(btn => {{
            btn.addEventListener("click", function () {{
                const vm_stock_reg = this.dataset.vmReg;
                frappe.call({{
                    method: "teampro.teampro.page.finance_details.tfp_dashboard.submit_stock_entry_from_vm_register",
                    args: {{ vm_stock_register: vm_stock_reg }},
                    callback: function (r) {{
                        if (!r.exc) {{
                            frappe.msgprint("Stock Entry submitted: " + r.message);
                        }} else {{
                            frappe.msgprint("Failed to submit stock entry.");
                        }}
                    }}
                }});
            }});
        }});
        
    </script>
    '''
    

    return html

import frappe

@frappe.whitelist()
def submit_stock_entry_from_vm_register(vm_stock_register):
    stock_entry_name = frappe.db.get_value("Stock Entry", {
        "custom_vm_stock_register": vm_stock_register,
        "stock_entry_type": "Material Transfer",
        "company": "TEAMPRO Food Products",
        "docstatus": 0
    }, "name")

    if not stock_entry_name:
        frappe.throw(f"No draft Stock Entry found for: {vm_stock_register}")

    stock_entry = frappe.get_doc("Stock Entry", stock_entry_name)
    stock_entry.set_posting_time=1
    stock_entry.save()
    # stock_entry.submit()
    return stock_entry.name

import frappe
from frappe.utils import nowdate, flt

@frappe.whitelist()
def create_mr_from_vm_item(vm_stock_register):
    from frappe.utils import nowdate
    from frappe.model.document import Document
    import json

    doc = frappe.get_doc("VM Stock Register", vm_stock_register)
    slot_tables = ["slot_a", "slot_b", "slot_c", "slot_d", "slot_e", "slot_f"]

    items = []
    for table in slot_tables:
        for row in doc.get(table):
            actual_qty = flt(frappe.db.get_value("Bin", {
                "item_code": row.item_code,
                "warehouse": "Stores - TFP"
            }, "actual_qty") or 0)

            if row.item_code:
                items.append({
                    "item_code": row.item_code,
                    "qty": row.new_stock_qty,
                    "schedule_date": nowdate(),
                    "uom": row.new_stockuom,
                    "warehouse": "Stores - TFP"
                })
    mr = frappe.get_doc({
        "doctype": "Material Request",
        "material_request_type": "Purchase",
        "company":"Teampro Food Products",
        "set_warehouse" : "Stores - TFP",
        "schedule_date": nowdate(),
        "items": items
    })
    mr.insert(ignore_permissions=True)
    # mr.submit()
    return mr.name

# @frappe.whitelist()
# def download_physical_vs_erp_stock_csv():
#     import csv
#     import io
#     from frappe.utils import flt

#     result = frappe.call("teampro.custom.get_physical_vs_erp_stock_data")
#     data = result.get("data", [])
#     latest_date = result.get("date")

#     output = io.StringIO()
#     writer = csv.writer(output)

#     # Write header
#     writer.writerow(["S.No", "Item", "Item Name", "Stock Qty", "Physical Qty", "Difference", "Status"])

#     for idx, row in enumerate(data):
#         writer.writerow([
#             idx + 1,
#             row["item"],
#             row["item_name"],
#             flt(row["stock_qty"]),
#             flt(row["physical_qty"]),
#             flt(row["difference"]),
#             row["status"]
#         ])

#     frappe.response["filename"] = f"Physical_vs_ERP_Stock_{latest_date}.csv"
#     frappe.response["filecontent"] = output.getvalue()
#     frappe.response["type"] = "download"  # ✅ This avoids needing doctype

import frappe
import openpyxl
from openpyxl.styles import Alignment, Font, Border, Side
from frappe.utils import flt
from io import BytesIO

@frappe.whitelist()
def download_physical_vs_erp_stock_csv():
    result = frappe.call("teampro.custom.get_physical_vs_erp_stock_data")
    data = result.get("data", [])
    latest_date = result.get("date")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stock Counting"

    # Define header style
    header_font = Font(bold=True, color="FFFFFF") 
    border = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000"),
    )
    header_fill = PatternFill(start_color="FF0000",
                              end_color="FF0000",
                              fill_type="solid")
    alignment = Alignment(horizontal="center", vertical="center")
    alignment_left = Alignment(horizontal="left", vertical="center")
    alignment_right = Alignment(horizontal="right", vertical="center")

    headers = ["S.No", "Item", "Item Name","Item Group", "Stock Qty", "Physical Qty", "Difference", "Status"]
    # Set specific column widths
    ws.column_dimensions['C'].width = 15  # Item Name (Column C)
    ws.column_dimensions['G'].width = 5  # Difference (Column G)

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = alignment
        cell.border = border

    # Write data rows
    for idx, row in enumerate(data, start=2):
        ws.cell(row=idx, column=1, value=idx - 1)  # S.No
        ws.cell(row=idx, column=2, value=row["item"])
        ws.cell(row=idx, column=3, value=row["item_name"])
        ws.cell(row=idx, column=4, value=row["item_group"])
        ws.cell(row=idx, column=5, value=flt(row["stock_qty"]))
        ws.cell(row=idx, column=6, value=flt(row["physical_qty"]))
        ws.cell(row=idx, column=7, value=flt(row["difference"]))

        status_cell = ws.cell(row=idx, column=8, value=row["status"])
        if row["status"] == "Match":
            status_cell.font = Font(color="008000")  # Green
        else:
            status_cell.font = Font(color="FF0000")  # Red

        # Optional: apply border and alignment to entire row
        for col in range(1, 9):
            cell = ws.cell(row=idx, column=col)
            cell.border = border
            if col in [2, 3, 4]:  # Item, Item Name, Item Group
                cell.alignment = alignment_left
            elif col in [5, 6, 7]:  # Stock Qty, Physical Qty, Difference
                cell.alignment = alignment_right
            else:
                cell.alignment = alignment


    # Adjust column widths (optional)
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 3

    # Save to response
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    frappe.response['filename'] = f"Stock_Counting_{latest_date}.xlsx"
    frappe.response['filecontent'] = output.getvalue()
    frappe.response['type'] = 'binary'


@frappe.whitelist()
def download_vm_precision_tfp():
    filename = "VM PRECISION - TFP" 
    xlsx_file = make_xlsx_tfp7(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime

def make_xlsx_tfp7(sheet_name="VM PRECISION - TFP", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "VM PRECISION - TFP"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")

    headers = [
        "Sr","Item Code", "Item Name","Quantity","Stock UOM","Last PR Date"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
        1: 8,     
        2: 25,    
        3: 40,    
        4: 10,    
        5: 10,
        6: 10   
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    row_idx = 2    
    s_no = 1
    warehouse = "VM1_Precision - TFP"

    stock_data = frappe.db.sql("""
        SELECT 
            bin.item_code,
            item.item_name,
            bin.actual_qty,
            item.stock_uom,
            (
                SELECT DATE_FORMAT(MAX(pr.creation), '%%d-%%m-%%Y')
                FROM `tabPurchase Receipt Item` pri
                JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
                WHERE pri.item_code = bin.item_code
                AND pri.warehouse = %s
            ) AS last_pr_date
        FROM `tabBin` bin
        JOIN `tabItem` item ON bin.item_code = item.name
        WHERE bin.warehouse = %s
        AND bin.actual_qty > 0
    """, (warehouse, warehouse), as_dict=True)

    
    today = getdate(nowdate())
    
    # Add age and is_old to each row
    red_rows = []
    normal_rows = []

    today = getdate(nowdate())

    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None  
        ws.cell(row=row_idx, column=1, value=s_no or "")
        ws.cell(row=row_idx, column=2, value=row.item_code or "")
        ws.cell(row=row_idx, column=3, value=row.item_name or "")
        ws.cell(row=row_idx, column=4, value=row.actual_qty or "")
        ws.cell(row=row_idx, column=5, value=row.stock_uom or "")
        ws.cell(row=row_idx, column=6, value=row.last_pr_date or "")

        for col in range(1, 7):
            ws.cell(row=row_idx, column=col).border = border   

        row_idx += 1
        s_no += 1

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()


@frappe.whitelist()
def download_stores_tfp():
    filename = "STORES - TFP (PACKING MATERIAL)" 
    xlsx_file = make_xlsx_tfp6(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime
from frappe.utils import getdate, nowdate

def make_xlsx_tfp6(sheet_name="STORES - TFP (PACKING MATERIAL)", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "STORES - TFP (PACKING MATERIAL)"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")


    headers = [
        "S.No","Item Code", "Item Name","Quantity","Stock UOM","Last PR Date"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
        1: 8,     
        2: 25,    
        3: 40,    
        4: 10,    
        5: 10,
        6: 10   
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    
    row_idx = 2    
    s_no = 1
    warehouse = "Stores - TFP"

    child_groups = frappe.get_all("Item Group", filters={"parent_item_group": "Packing Material"}, pluck="name")
    item_groups = ["Packing Material"] + child_groups

    if not item_groups:
        return []

    format_strings = ','.join(['%s'] * len(item_groups))
    stock_data = frappe.db.sql(f"""
        SELECT 
            bin.item_code,
            item.item_name,
            bin.actual_qty,
            item.stock_uom,
            (
                SELECT DATE_FORMAT(MAX(pr.creation), '%%d-%%m-%%Y')
                FROM `tabPurchase Receipt Item` pri
                JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
                WHERE pri.item_code = bin.item_code
                AND pri.warehouse = %s
            ) AS last_pr_date
        FROM `tabBin` bin
        JOIN `tabItem` item ON bin.item_code = item.name
        WHERE bin.warehouse = %s
        AND bin.actual_qty > 0
        AND item.item_group IN ({format_strings})
    """, [warehouse, warehouse] + item_groups, as_dict=True)

    today = getdate(nowdate())
    
    red_rows = []
    normal_rows = []

    today = getdate(nowdate())

    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None

        if row.last_pr_date:
            red_rows.append(row)  
        else:
            normal_rows.append(row)


    final_rows = red_rows + normal_rows

    s_no = 1
    for row in final_rows:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        red_font = Font(color="FFFF0000") if pr_date else Font()

        ws.cell(row=row_idx, column=1, value=s_no or "").font = red_font
        ws.cell(row=row_idx, column=2, value=row.item_code or "").font = red_font
        ws.cell(row=row_idx, column=3, value=row.item_name or "").font = red_font
        ws.cell(row=row_idx, column=4, value=row.actual_qty or "").font = red_font
        ws.cell(row=row_idx, column=5, value=row.stock_uom or "").font = red_font
        ws.cell(row=row_idx, column=6, value=row.last_pr_date or "").font = red_font

        ws.cell(row=row_idx, column=5).alignment = center_align

        for col in range(1, 7):
            ws.cell(row=row_idx, column=col).border = border

        row_idx += 1
        s_no += 1


    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

@frappe.whitelist()
def download_stores_tfp_product():
    filename = "STORES - TFP (PRODUCT)" 
    xlsx_file = make_xlsx_tfp5(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime

def make_xlsx_tfp5(sheet_name="STORES - TFP (PRODUCT)", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "STORES - TFP (PRODUCT)"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")

    headers = [
        "S.No","Item Code", "Item Name","Quantity","Stock UOM","Last PR Date"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
        1: 8,     
        2: 25,    
        3: 35,    
        4: 10,    
        5: 10,
        6: 10   
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    row_idx = 2    
    s_no = 1
    warehouse = "Stores - TFP"
    parent_item_group = "Food Products"
    
    # Fetch child item groups of "Food Products"
    child_item_groups = frappe.db.get_all(
        "Item Group",
        filters={"parent_item_group": parent_item_group},
        pluck="name"
    )

    placeholders = ", ".join(["%s"] * len(child_item_groups))

    stock_data = frappe.db.sql(f"""
        SELECT 
            bin.item_code,
            item.item_name,
            bin.actual_qty,
            item.stock_uom,
            (
                SELECT DATE_FORMAT(MAX(pr.creation), '%%d-%%m-%%Y')
                FROM `tabPurchase Receipt Item` pri
                JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
                WHERE pri.item_code = bin.item_code
                AND pri.warehouse = %s
            ) AS last_pr_date
        FROM `tabBin` bin
        JOIN `tabItem` item ON bin.item_code = item.name
        WHERE bin.warehouse = %s
        AND bin.actual_qty > 0
        AND item.item_group IN ({placeholders})
    """, [warehouse, warehouse] + child_item_groups, as_dict=True)

    today = getdate(nowdate())
    
    # Add age and is_old to each row
    red_rows = []
    normal_rows = []

    today = getdate(nowdate())

    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        age = (today - pr_date).days if pr_date else None

        if age is not None and age > 30:
            red_rows.append(row)
        else:
            normal_rows.append(row)


    # Combine red rows first, then normal
    final_rows = red_rows + normal_rows

    # Now write to Excel
    s_no = 1
    for row in final_rows:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        # age = (today - pr_date).days if pr_date else None
        # is_old = age is not None and age > 30

        age = (today - pr_date).days if pr_date else None
        red_font = Font(color="FFFF0000") if age is not None and age > 30 else Font()
        ws.cell(row=row_idx, column=1, value=s_no or "").font = red_font
        ws.cell(row=row_idx, column=2, value=row.item_code or "").font = red_font
        ws.cell(row=row_idx, column=3, value=row.item_name or "").font = red_font
        ws.cell(row=row_idx, column=4, value=row.actual_qty or "").font = red_font
        ws.cell(row=row_idx, column=5, value=row.stock_uom or "").font = red_font
        ws.cell(row=row_idx, column=6, value=row.last_pr_date or "").font = red_font

        ws.cell(row=row_idx, column=5).alignment = center_align
        
        for col in range(1, 7):
            ws.cell(row=row_idx, column=col).border = border 

        row_idx += 1
        s_no += 1   

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()


@frappe.whitelist()
def download_dispatched_details():
    filename = "DISPATCHED DETAILS" 
    xlsx_file = make_xlsx_tfp4(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime

def make_xlsx_tfp4(sheet_name="DISPATCHED DETAILS", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "DISPATCHED DETAILS"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    headers = [
        "S.No","DN ID","SO ID","Customer","Delivery Date","Total QTY","Total Covers"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
        1: 8,     
        2: 25,    
        3: 25,    
        4: 40,    
        5: 15,
        6: 10,
        7: 10   
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    row_idx = 2    
    s_no = 1
    packed_dns = frappe.db.get_all("Delivery Note",
        filters={"custom_delivery_status_new": "Dispatched", "docstatus": 1},
        fields=["name", "custom_delivery_date", "total_qty", "custom_total_covers"],order_by="custom_delivery_date asc"
    )


    # Step 2: Get all DN Items linked to SO
    dn_names = [d.name for d in packed_dns]
    dn_items = frappe.db.get_all("Delivery Note Item",
        filters={"parent": ["in", dn_names], "against_sales_order": ["!=", ""]},
        fields=["parent", "against_sales_order"]
    )

    # Step 3: Build Summary Data
    summary = {}
    grand_total_qty = 0
    grand_total_covers = 0

    for dn_doc in packed_dns:
        dn = dn_doc.name
        dn_date = dn_doc.custom_delivery_date
        total_qty = flt(dn_doc.total_qty)
        total_covers = flt(dn_doc.custom_total_covers)

        grand_total_qty += total_qty
        grand_total_covers += total_covers

        # Get all SOs linked to this DN
        linked_sos = list(set([
            d.against_sales_order for d in dn_items if d.parent == dn and d.against_sales_order
        ]))

        if not linked_sos:
            key = (dn, "")
            summary[key] = {
                "dn": dn,
                "so": "",
                "customer": "",
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }

        for so in linked_sos:
            customer = frappe.db.get_value("Sales Order", so, "customer") or ""
            key = (dn, so)

            summary[key] = {
                "dn": dn,
                "so": so,
                "customer": customer,
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }

            ws.cell(row=row_idx, column=1, value=s_no or "")
            ws.cell(row=row_idx, column=2, value=dn or "")
            ws.cell(row=row_idx, column=3, value=so or "")
            ws.cell(row=row_idx, column=4, value=customer or "")
            ws.cell(row=row_idx, column=5, value=dn_date or "")
            ws.cell(row=row_idx, column=6, value=total_qty or "")
            ws.cell(row=row_idx, column=7, value=total_covers or "")

        for col in range(1, 8):
            ws.cell(row=row_idx, column=col).border = border  

        row_idx += 1
        s_no += 1

    ws.cell(row=row_idx, column=1, value="Grand Total").alignment = center_align
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=4)
    ws.cell(row=row_idx, column=5, value="").alignment = center_align
    ws.cell(row=row_idx, column=6, value=grand_total_qty).alignment = right_align
    ws.cell(row=row_idx, column=7, value=grand_total_covers).alignment = right_align

    for col in range(1, 8):
        cell = ws.cell(row=row_idx, column=col)
        cell.border = border
        cell.font = Font(bold=True)
        cell.fill = fill_total   


    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

@frappe.whitelist()
def download_packed_details():
    filename = "PACKED DETAILS" 
    xlsx_file = make_xlsx_tfp3(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime

def make_xlsx_tfp3(sheet_name="PACKED DETAILS", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "PACKED DETAILS"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    headers = [
        "S.No","DN ID","SO ID","Customer","Delivery Date","Total QTY","Total Covers"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
        1: 8,     
        2: 25,    
        3: 25,    
        4: 40,    
        5: 15,
        6: 10,
        7: 10   
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    row_idx = 2    
    s_no = 1
    # Step 1: Get all Packed Delivery Notes
    packed_dns = frappe.db.get_all("Delivery Note",
        filters={"custom_delivery_status_new": "Packed", "docstatus": 1},
        fields=["name", "custom_delivery_date", "total_qty", "custom_total_covers"],order_by="custom_delivery_date asc"
    )

    
    # Step 2: Get all DN Items linked to SO
    dn_names = [d.name for d in packed_dns]
    dn_items = frappe.db.get_all("Delivery Note Item",
        filters={"parent": ["in", dn_names], "against_sales_order": ["!=", ""]},
        fields=["parent", "against_sales_order"]
    )

    # Step 3: Build Summary Data
    summary = {}
    grand_total_qty = 0
    grand_total_covers = 0

    for dn_doc in packed_dns:
        dn = dn_doc.name
        dn_date = dn_doc.custom_delivery_date
        total_qty = flt(dn_doc.total_qty)
        total_covers = flt(dn_doc.custom_total_covers)

        grand_total_qty += total_qty
        grand_total_covers += total_covers

        # Get all SOs linked to this DN
        linked_sos = list(set([
            d.against_sales_order for d in dn_items if d.parent == dn and d.against_sales_order
        ]))

        if not linked_sos:
            key = (dn, "")
            summary[key] = {
                "dn": dn,
                "so": "",
                "customer": "",
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }

        for so in linked_sos:
            customer = frappe.db.get_value("Sales Order", so, "customer") or ""
            key = (dn, so)

            summary[key] = {
                "dn": dn,
                "so": so,
                "customer": customer,
                "dn_date": dn_date,
                "total_qty": total_qty,
                "total_covers": total_covers
            }
            ws.cell(row=row_idx, column=1, value=s_no or "")
            ws.cell(row=row_idx, column=2, value=dn or "")
            ws.cell(row=row_idx, column=3, value=so or "")
            ws.cell(row=row_idx, column=4, value=customer or "")
            ws.cell(row=row_idx, column=5, value=dn_date or "")
            ws.cell(row=row_idx, column=6, value=total_qty or "")
            ws.cell(row=row_idx, column=7, value=total_covers or "")

        for col in range(1, 8):
            ws.cell(row=row_idx, column=col).border = border  

        row_idx += 1
        s_no += 1

    ws.cell(row=row_idx, column=1, value="Grand Total").alignment = center_align
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=4)
    ws.cell(row=row_idx, column=5, value="").alignment = center_align
    ws.cell(row=row_idx, column=6, value=grand_total_qty).alignment = right_align
    ws.cell(row=row_idx, column=7, value=grand_total_covers).alignment = right_align

    for col in range(1, 8):
        cell = ws.cell(row=row_idx, column=col)
        cell.border = border
        cell.font = Font(bold=True)
        cell.fill = fill_total    

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

@frappe.whitelist()
def download_opportunity_details():
    filename = "OPPORTUNITY DETAILS" 
    xlsx_file = make_xlsx_tfp1(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime
from frappe.utils import getdate, fmt_money

def make_xlsx_tfp1(sheet_name="OPPORTUNITY DETAILS", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "OPPORTUNITY DETAILS"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    headers = [
        "S.No","From", "Organization","Amount","Exp.Week","Exp.Qty","Remarks"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
        1: 8,     
        2: 15,    
        3: 30,    
        4: 10,    
        5: 10,
        6: 10,
        7: 70   
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    row_idx = 2    
    s_no = 1
    data = frappe.db.sql("""
        SELECT 
            opportunity_from,
            organization_name,
            opportunity_amount,
            expected_closing,
            custom_expected_quantity,
            remark
        FROM `tabOpportunity`
        WHERE status NOT IN ('Lost') 
        AND service = 'TFP'
    """, as_dict=True)


    today = getdate(nowdate())
    
    for row in data:
        expected_week = getdate(row.expected_closing).isocalendar()[1] if row.expected_closing else '-'
        ws.cell(row=row_idx, column=1, value=s_no or "")
        ws.cell(row=row_idx, column=2, value=row.opportunity_from or "")
        ws.cell(row=row_idx, column=3, value=row.organization_name or "")
        ws.cell(row=row_idx, column=4, value=row.opportunity_amount or "")
        ws.cell(row=row_idx, column=5, value=row.expected_closing.strftime("%d-%m-%Y") if row.expected_closing else "")
        ws.cell(row=row_idx, column=6, value=row.custom_expected_quantity or "")
        ws.cell(row=row_idx, column=7, value=row.remark or "")

        for col in range(1, 8):
            ws.cell(row=row_idx, column=col).border = border  

        row_idx += 1
        s_no += 1

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

@frappe.whitelist()
def download_active_cutomer_last_so_details():
    filename = "ACTIVE CUSTOMER LAST SO DETAILS" 
    xlsx_file = make_xlsx_tfp2(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime
from frappe.utils import getdate, fmt_money,nowdate, formatdate

def make_xlsx_tfp2(sheet_name="ACTIVE CUSTOMER LAST SO DETAILS", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "ACTIVE CUSTOMER LAST SO DETAILS"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    # fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    headers = [
        "S.No","Customer Name", "Last SO On","Last SO Quantity","Age (Days)"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
        1: 8,     
        2: 40,    
        3: 15,    
        4: 10,    
        5: 15     
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width    

    row_idx = 2    
    s_no = 1
    today = getdate(nowdate())

    data = frappe.db.sql("""
        SELECT 
            so.customer_name,
            so.transaction_date AS last_so_on,
            SUM(sod.qty) AS last_so_qty
        FROM `tabSales Order` so
        JOIN `tabSales Order Item` sod ON so.name = sod.parent
        JOIN `tabCustomer` c ON c.name = so.customer
        WHERE so.docstatus = 1
        AND so.status NOT IN ('On Hold', 'Cancelled') 
        AND so.service = 'TFP'
        AND c.disabled = 0
        AND EXISTS (
            SELECT 1 FROM `tabSLA Details` s
            WHERE s.parent = c.name AND s.service = 'TFP'
            LIMIT 1
        )
        AND so.transaction_date = (
            SELECT MAX(so_inner.transaction_date)
            FROM `tabSales Order` so_inner
            WHERE so_inner.customer_name = so.customer_name
            AND so_inner.docstatus = 1
            AND so_inner.status NOT IN ('On Hold', 'Cancelled')
            AND so_inner.service = 'TFP'
        )
        GROUP BY so.customer_name, so.transaction_date
        ORDER BY so.transaction_date DESC
    """, as_dict=True)

    old_rows = []
    recent_rows = []

    for row in data:
        so_date = getdate(row.last_so_on)
        age_days = (today - so_date).days
        red_font = Font(color="FF0000") if age_days > 15 else Font()
        # total_outstanding += row.outstanding_amount or 0
        ws.cell(row=row_idx, column=1, value=s_no or "").font = red_font
        ws.cell(row=row_idx, column=2, value=row.customer_name or "").font = red_font
        ws.cell(row=row_idx, column=3, value=row.last_so_on.strftime("%d-%m-%Y") if row.last_so_on else "").font = red_font
        ws.cell(row=row_idx, column=4, value=row.last_so_qty or "").font = red_font
        ws.cell(row=row_idx, column=5, value=age_days or "").font = red_font

        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).border = border 

        row_idx += 1
        s_no += 1

    # ws.cell(row=row_idx, column=1, value="Total").alignment = center_align
    # ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)
    # ws.cell(row=row_idx, column=3, value=total_outstanding).alignment = right_align

    # for col in range(1, 6):
    #     cell = ws.cell(row=row_idx, column=col)
    #     cell.border = border
    #     cell.font = Font(bold=True)
    #     cell.fill = fill_total    

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

@frappe.whitelist()
def download_receivable_table():
    filename = "RECEIVABLE" 
    xlsx_file = make_xlsx_tfp8(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime
from frappe.utils import getdate, fmt_money,nowdate, formatdate,today

def make_xlsx_tfp8(sheet_name="RECEIVABLE", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "RECEIVABLE"  

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")
    headers = [
        "S.No","Customer ", "Value","Age","Sales Invoice"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
    1: 8,     # S.No
    2: 40,    # Customer
    3: 15,    # Value
    4: 10,    # Age
    5: 25     # Sales Invoice
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width    

    row_idx = 2    
    s_no = 1
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today()], "year_end_date": [">=", today()]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )

    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    filters = {
        'company': 'TEAMPRO Food Products',
        'from_date': from_date,
        'to_date': to_date
    }

    data = frappe.db.sql("""
        SELECT name, customer, outstanding_amount, posting_date
        FROM `tabSales Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND outstanding_amount > 0
        ORDER BY posting_date
    """, filters, as_dict=True)

    total_outstanding = 0
    today_date = getdate(nowdate())

    for row in data:
        age = (today_date - getdate(row.posting_date)).days
        red_font = Font(color="FF0000") if age > 30 else Font()
        total_outstanding += row.outstanding_amount or 0
        ws.cell(row=row_idx, column=1, value=s_no or "").font = red_font
        ws.cell(row=row_idx, column=2, value=row.customer or "").font = red_font
        ws.cell(row=row_idx, column=3, value=row.outstanding_amount or "").font = red_font
        ws.cell(row=row_idx, column=4, value=age or "").font = red_font
        ws.cell(row=row_idx, column=5, value=row.name or "").font = red_font

        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).border = border

        row_idx += 1
        s_no += 1


    ws.cell(row=row_idx, column=1, value="Total").alignment = center_align
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)
    ws.cell(row=row_idx, column=3, value=total_outstanding).alignment = right_align

    for col in range(1, 6):
        cell = ws.cell(row=row_idx, column=col)
        cell.border = border
        cell.font = Font(bold=True)
        cell.fill = fill_total

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

@frappe.whitelist()
def download_tobill_table():
    filename = "TO BILL" 
    xlsx_file = make_xlsx_tfp9(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime
from frappe.utils import getdate, fmt_money,nowdate, formatdate,today

def make_xlsx_tfp9(sheet_name="TO BILL", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "TO BILL"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    headers = [
        "S.No","Customer ", "Value","Age","Sales Order"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
    1: 8,     
    2: 40,    
    3: 15,    
    4: 10,    
    5: 25     
    }
    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width 

    row_idx = 2    
    s_no = 1
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today()], "year_end_date": [">=", today()]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )
    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    filters = {
        'company': 'TEAMPRO Food Products',
        'from_date': from_date,
        'to_date': to_date
    }

    data = frappe.db.sql("""
        SELECT name, customer, base_grand_total, transaction_date
        FROM `tabSales Order`
        WHERE docstatus = 1
          AND company = %(company)s
          AND service='TFP'
          AND status='To Bill'
          AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
          AND base_grand_total > 0
        ORDER BY transaction_date
    """, filters, as_dict=True)


    total_outstanding = 0
    today_date = getdate(nowdate())

    for row in data:
        age = (today_date - getdate(row.transaction_date)).days
        red_font = Font(color="FF0000") if age > 30 else Font()
        total_outstanding += row.base_grand_total or 0
        ws.cell(row=row_idx, column=1, value=s_no or "").font = red_font
        ws.cell(row=row_idx, column=2, value=row.customer or "").font = red_font
        ws.cell(row=row_idx, column=3, value=row.base_grand_total or "").font = red_font
        ws.cell(row=row_idx, column=4, value=age or "").font = red_font
        ws.cell(row=row_idx, column=5, value=row.name or "").font = red_font


        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).border = border

        row_idx += 1
        s_no += 1

    ws.cell(row=row_idx, column=1, value="Total").alignment = center_align
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)
    ws.cell(row=row_idx, column=3, value=total_outstanding).alignment = right_align

    for col in range(1, 6):
        cell = ws.cell(row=row_idx, column=col)
        cell.border = border
        cell.font = Font(bold=True)
        cell.fill = fill_total

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

@frappe.whitelist()
def download_payable_table1():
    filename = "PAYABLE" 
    xlsx_file = make_xlsx_tfp10(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'

import openpyxl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import frappe
import io
from datetime import datetime
from frappe.utils import getdate, fmt_money,nowdate, formatdate,today

def make_xlsx_tfp10(sheet_name="PAYABLE", wb=None, column_widths=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")
    ws.title = "PAYABLE"

    header_font = Font(bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    fill_total = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    headers = [
        "S.No","Supplier Name", "Value","AGE","Purchase Invoice"
    ]


    for col_num,header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num,value=header)
        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border

    column_widths = {
    1: 8,     
    2: 40,    
    3: 15,    
    4: 10,    
    5: 25     
    }
    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    row_idx = 2    
    s_no = 1
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters={"year_start_date": ["<=", today()], "year_end_date": [">=", today()]},
        fieldname=["year_start_date", "year_end_date"],
        as_dict=True
    )
    from_date = fiscal_year["year_start_date"]
    to_date = fiscal_year["year_end_date"]

    filters = {
        'company': 'TEAMPRO Food Products',
        'from_date': from_date,
        'to_date': to_date
    }

    data = frappe.db.sql("""
        SELECT name, supplier, outstanding_amount, posting_date
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND outstanding_amount > 0
        ORDER BY posting_date
    """, filters, as_dict=True)

    today_date = getdate(nowdate())
    total_outstanding = 0

    for row in data:
        age = (today_date - getdate(row.posting_date)).days
        red_font = Font(color="FF0000") if age > 30 else Font()
        total_outstanding += row.outstanding_amount or 0
        ws.cell(row=row_idx, column=1, value=s_no or "").font = red_font
        ws.cell(row=row_idx, column=2, value=row.supplier or "").font = red_font
        ws.cell(row=row_idx, column=3, value=row.outstanding_amount or "").font = red_font
        ws.cell(row=row_idx, column=4, value=age or "").font = red_font
        ws.cell(row=row_idx, column=5, value=row.name or "").font = red_font

        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).border = border

        row_idx += 1
        s_no += 1

    ws.cell(row=row_idx, column=1, value="Total").alignment = center_align
    ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)
    ws.cell(row=row_idx, column=3, value=total_outstanding).alignment = right_align

    for col in range(1, 6):
        cell = ws.cell(row=row_idx, column=col)
        cell.border = border
        cell.font = Font(bold=True)
        cell.fill = fill_total

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()


import frappe
from frappe.utils import formatdate, nowdate, getdate

@frappe.whitelist()
def get_tfp_stock_html():
    from datetime import timedelta

    warehouse = "Stores - TFP"
    parent_item_group = "Food Products"
    
    # Fetch child item groups of "Food Products"
    child_item_groups = frappe.db.get_all(
        "Item Group",
        filters={"parent_item_group": parent_item_group},
        pluck="name"
    )

    if not child_item_groups:
        return "<p>No item groups found under 'Food Products'</p>"

    # Prepare SQL-compatible list
    placeholders = ", ".join(["%s"] * len(child_item_groups))

    stock_data = frappe.db.sql(f"""
        SELECT 
            bin.item_code,
            item.item_name,
            bin.actual_qty,
            item.stock_uom,
            (
                SELECT MAX(pr.creation)
                FROM `tabPurchase Receipt Item` pri
                JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
                WHERE pri.item_code = bin.item_code
                AND pri.warehouse = %s
            ) AS last_pr_date
        FROM `tabBin` bin
        JOIN `tabItem` item ON bin.item_code = item.name
        WHERE bin.warehouse = %s
        AND bin.actual_qty > 0
        AND item.item_group IN ({placeholders})
    """, [warehouse, warehouse] + child_item_groups, as_dict=True)

    today = getdate(nowdate())
    
    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        row.age = (today - pr_date).days if pr_date else None
        row.is_old = row.age is not None and row.age > 30

    stock_data.sort(key=lambda x: not x.is_old)

    html = """
    <div style='max-height: 340px; overflow-y: auto; border: 1px solid #ccc; border-radius: 6px;'>
    <table class="table table-bordered" style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="text-align:center;">
                <th style="position: sticky; top: 0; background: #002060;color:white">Item Code</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Item Name</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Quantity</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Stock UOM</th>
                <th style="position: sticky; top: 0; background: #002060;color:white">Last PR Date</th>
            </tr>
        </thead>
        <tbody>
    """

    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        red_row_style = 'style="color: red;"' if row.is_old else ""

        html += f"""
            <tr {red_row_style}>
                <td>{row.item_code}</td>
                <td>{row.item_name}</td>
                <td style="text-align:right">{row.actual_qty}</td>
                <td style="text-align:center">{row.stock_uom}</td>
                <td>{formatdate(pr_date) if pr_date else '-'}</td>
            </tr>
        """

    html += "</tbody></table></div>"

    return html

import frappe
import io
import openpyxl

from frappe.utils import formatdate

from openpyxl.styles import (
    PatternFill,
    Border,
    Side,
    Alignment,
    Font
)

from openpyxl.utils import get_column_letter


@frappe.whitelist()
def download_vm_precision_tfp_data():

    filename = "LSVM Stock Data"

    xlsx_file = make_lsvm_data(filename)

    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file
    frappe.response['type'] = 'binary'


def make_lsvm_data(sheet_name="LSVM Stock Data", wb=None):

    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = sheet_name.replace(":", "-")

    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    bold_font = Font(
        bold=True
    )

    center_align = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )

    left_align = Alignment(
        horizontal="left",
        vertical="center",
        wrap_text=True
    )

    right_align = Alignment(
        horizontal="right",
        vertical="center",
        wrap_text=True
    )

    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    fill_header = PatternFill(
        start_color="002060",
        end_color="002060",
        fill_type="solid"
    )

    parent_even_fill = PatternFill(
        start_color="F3F4F6",
        end_color="F3F4F6",
        fill_type="solid"
    )

    parent_odd_fill = PatternFill(
        start_color="E5E7EB",
        end_color="E5E7EB",
        fill_type="solid"
    )

    child_even_fill = PatternFill(
        start_color="FFFFFF",
        end_color="FFFFFF",
        fill_type="solid"
    )

    child_odd_fill = PatternFill(
        start_color="F1F5F9",
        end_color="F1F5F9",
        fill_type="solid"
    )

    child_header_fill = PatternFill(
        start_color="D9E1F2",
        end_color="D9E1F2",
        fill_type="solid"
    )


    headers = [
        "Sr",
        "VM ID",
        "Vending Machine",
        "Status",
        "Total Quantity",
        "Last Filling",
        "Next Filling"
    ]

    for col_num, header in enumerate(headers, 1):

        cell = ws.cell(
            row=1,
            column=col_num,
            value=header
        )

        cell.font = header_font
        cell.alignment = center_align
        cell.fill = fill_header
        cell.border = border


    column_widths = {
        1: 8,
        2: 25,
        3: 30,
        4: 15,
        5: 18,
        6: 18,
        7: 18
    }

    for col_idx, width in column_widths.items():

        ws.column_dimensions[
            get_column_letter(col_idx)
        ].width = width


    vm_data = frappe.db.sql("""
        SELECT
            name AS vm_id,
            machine_id,
            status,
            total_new_stock_qty,
            DATE(posting_date) AS posting_date
        FROM `tabVM Stock Register`
        WHERE docstatus != 2
        AND machine_id IS NOT NULL
        ORDER BY posting_date DESC
    """, as_dict=True)

    row_idx = 2
    sr = 1

    for d in vm_data:
        parent_fill = (
            parent_even_fill
            if sr % 2 == 0
            else parent_odd_fill
        )
        parent_values = [
            sr,
            d.vm_id,
            d.machine_id,
            d.status,
            d.total_new_stock_qty,
            formatdate(d.posting_date)
                if d.posting_date else "",
            ""
        ]
        for col_num, value in enumerate(parent_values, 1):
            cell = ws.cell(
                row=row_idx,
                column=col_num,
                value=value
            )
            cell.border = border
            cell.fill = parent_fill
            cell.alignment = center_align
            if col_num in [2, 3]:
                cell.alignment = left_align
            if col_num == 5:
                cell.alignment = right_align
            if col_num == 2:
                cell.font = bold_font
        row_idx += 1
        child_header_map = {
            2: "Item Code",
            3: "Item Name",
            4: "Quantity",
            5: "Stock UOM",
            6: "New Stock UOM"
        }

        for col_num, header in child_header_map.items():

            cell = ws.cell(
                row=row_idx,
                column=col_num,
                value=header
            )

            cell.font = bold_font
            cell.fill = child_header_fill
            cell.border = border
            cell.alignment = center_align

        ws.merge_cells(
            start_row=row_idx,
            start_column=6,
            end_row=row_idx,
            end_column=7
        )

        merge_cell = ws.cell(
            row=row_idx,
            column=6
        )

        merge_cell.value = "New Stock UOM"
        merge_cell.font = bold_font
        merge_cell.fill = child_header_fill
        merge_cell.border = border
        merge_cell.alignment = center_align

        ws.cell(row=row_idx, column=7).border = border
        ws.cell(row=row_idx, column=7).fill = child_header_fill

        row_idx += 1
        child_data = frappe.db.sql("""
            SELECT
                item_code,
                item_name,
                new_stock_qty,
                stock_uom,
                new_stockuom
            FROM `tabVM Stock Details`
            WHERE parent = %s
            AND new_stock_qty > 0
        """, (d.vm_id,), as_dict=True)

        child_sr = 1

        for row in child_data:

            child_fill = (child_even_fill
                if child_sr % 2 == 0
                else child_odd_fill
            )
            cell = ws.cell(row=row_idx,column=2,value=row.item_code)
            cell.border = border
            cell.fill = child_fill
            cell.alignment = left_align
            cell = ws.cell(row=row_idx,column=3,value=row.item_name)
            cell.border = border
            cell.fill = child_fill
            cell.alignment = left_align
            cell = ws.cell(row=row_idx,column=4,value=row.new_stock_qty)
            cell.border = border
            cell.fill = child_fill
            cell.alignment = right_align
            cell = ws.cell(row=row_idx,column=5,value=row.stock_uom)
            cell.border = border
            cell.fill = child_fill
            cell.alignment = center_align
            ws.merge_cells(start_row=row_idx,start_column=6,end_row=row_idx,end_column=7)
            cell = ws.cell(row=row_idx,column=6,value=row.new_stockuom)
            cell.border = border
            cell.fill = child_fill
            cell.alignment = center_align
            ws.cell(row=row_idx,column=7).border = border
            ws.cell(row=row_idx,column=7).fill = child_fill
            row_idx += 1
            child_sr += 1
        row_idx += 1
        sr += 1
    ws.freeze_panes = "A2"
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

import frappe
from frappe.utils import getdate, nowdate, formatdate
@frappe.whitelist()
def get_shop_stock_html_data():
    shop_data = frappe.get_all(
        "Shop RC",filters={"workflow_state": "Approved"},fields=["name","customer_name","city"],order_by="name asc")
    html = """

    <style>

    .shop-container{
        max-height:650px;
        overflow-y:auto;
        border:1px solid #cbd5e1;
        background:#e5e7eb;
    }

    .main-table{
        width:100%;
        border-collapse:collapse;
        font-size:13px;
        font-family:Arial,sans-serif;
        background:#e5e7eb;
    }

    .main-table thead th{
        position:sticky;
        top:0;
        z-index:100;
        background:#002060;
        color:white;
        border:1px solid #cbd5e1;
        padding:8px;
        text-align:center;
        font-weight:bold;
    }

    .main-table td{
        border:1px solid #cbd5e1;
        padding:7px;
    }

    .parent-even{
        background:#f3f4f6;
    }

    .parent-odd{
        background:#e5e7eb;
    }

    .child-table{
        width:100%;
        border-collapse:collapse;
        background:#f8fafc;
    }

    .child-table thead th{
        background:#d9e1f2;
        color:#111827;
        border:1px solid #cbd5e1;
        padding:7px;
        text-align:center;
        font-weight:bold;
        position:sticky;
        top:40px;
        z-index:99;
    }

    .child-table td{
        border:1px solid #cbd5e1;
        padding:6px;
    }

    .child-even{
        background:#ffffff;
    }

    .child-odd{
        background:#f1f5f9;
    }

    .toggle-icon{
        cursor:pointer;
        font-weight:bold;
        font-size:16px;
        margin-right:6px;
    }

    .qty{
        text-align:right;
    }

    .center{
        text-align:center;
    }

    .shop-link{
        font-weight:bold;
        text-decoration:none;
        color:#111827;
    }

    .shop-link:hover{
        text-decoration:underline;
    }

    </style>
    <div class="shop-container">
        <table class="main-table">
            <thead>
                <tr>
                    <th style="width:5%">Sr</th>
                    <th style="width:12%">Shop ID</th>
                    <th style="width:20%">Shop Name</th>
                    <th style="width:22%">Location</th>
                    <th style="width:10%"> Stock Qty</th>
                    <th style="width:10%">UOM</th>
                    <th style="width:10%">Age Of Delivery</th>
                    <th style="width:11%">Next Delivery</th>
                </tr>
            </thead>
            <tbody>
    """
    sr = 1
    for shop in shop_data:
        customer_id = frappe.db.get_value("Customer",{"custom_retail_customer": shop.name},"name")
        if not customer_id:
            continue
        warehouse = frappe.db.get_value("Warehouse",{"custom_retail_customer": shop.name,"disabled": 0},["name"],as_dict=True)
        if not warehouse:
            continue
        warehouse_name = warehouse.name
        stock_summary = frappe.db.sql("""
            SELECT
                SUM(actual_qty) as total_qty,
                MAX(stock_uom) as stock_uom
            FROM `tabBin`
            WHERE warehouse = %s
            AND actual_qty > 0
        """, (warehouse_name,), as_dict=True)
        total_qty = stock_summary[0].total_qty or 0
        last_delivery = frappe.db.get_value("RS Delivery",{"customer": customer_id,"docstatus": 1},["delivered_date"],order_by="delivered_date desc")
        next_delivery = frappe.db.get_value(
            "RS Delivery",
            {
                "customer": customer_id,
                "docstatus": 1,
                "next_delivery_date": ["is", "set"]
            },
            "next_delivery_date",
            order_by="next_delivery_date asc"
        )
        age_days = ""
        if last_delivery:
            age_days = (
                getdate(nowdate()) -
                getdate(last_delivery)
            ).days

            age_days = str(age_days) + " Days"
        child_data = frappe.db.sql("""
            SELECT
                bin.item_code,
                item.item_name,
                bin.actual_qty,
                item.stock_uom
            FROM `tabBin` bin
            INNER JOIN `tabItem` item
                ON item.name = bin.item_code
            WHERE bin.warehouse = %s
            AND bin.actual_qty > 0
            ORDER BY item.item_name
        """, (warehouse_name,), as_dict=True)
        child_rows = ""
        child_sr = 1
        for row in child_data:
            child_class = (
                "child-even"
                if child_sr % 2 == 0
                else "child-odd"
            )
            child_rows += f"""
                <tr class="{child_class}">
                    <td>{row.item_code or ''}</td>
                    <td>{row.item_name or ''}
                    </td>
                    <td class="qty">{row.actual_qty or 0}</td>
                    <td class="center">{row.stock_uom or ''}</td>
                </tr>
            """
            child_sr += 1
        if not child_rows:
            child_rows = """
                <tr class="child-even">
                    <td colspan="4" class="center">No Stock Available</td>
                </tr>
            """
        parent_class = (
            "parent-even"
            if sr % 2 == 0
            else "parent-odd"
        )
        html += f"""
            <tr class="{parent_class}">
                <td class="center">{sr}</td>
                <td><span class="toggle-icon" onclick="toggle_shop_details('{shop.name}', this)">

                        +

                    </span>

                    <a href="/app/shop-rc/{shop.name}"
                       target="_blank"
                       class="shop-link">

                        {shop.name}

                    </a>

                </td>

                <td>
                    {shop.customer_name or ''}
                </td>

                <td>
                    {shop.city or ''}
                </td>

                <td class="qty">
                    {total_qty}
                </td>

                <td class="center">
                    
                </td>

                <td class="center">
                    {age_days}
                </td>

                <td class="center">
                    {formatdate(getdate(next_delivery)) if next_delivery else ''}
                </td>

            </tr>

            <tr id="detail_{shop.name}"
                style="display:none;">

                <td colspan="8" style="padding:0px;">
                    <table class="child-table">
                        <thead>
                            <tr>
                                <th> Item Code</th>
                                <th> Item Name</th>

                                <th>
                                    Quantity
                                </th>

                                <th>
                                    UOM
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {child_rows}

                        </tbody>

                    </table>

                </td>

            </tr>
        """

        sr += 1
    html += """

            </tbody>

        </table>

    </div>

    <script>

    function toggle_shop_details(id, element){

        let row = document.getElementById(
            "detail_" + id
        );

        if(row.style.display === "none"){

            row.style.display = "table-row";

            element.innerHTML = "-";
        }
        else{

            row.style.display = "none";

            element.innerHTML = "+";
        }
    }
    </script>
    """
    return html


import frappe
from frappe.utils import getdate, nowdate, formatdate


@frappe.whitelist()
def get_payment_outstanding_html_data():

    shop_data = frappe.get_all(
        "Shop RC",
        filters={
            "workflow_state": "Approved"
        },
        fields=[
            "name",
            "customer_name",
            "city"
        ],
        order_by="name asc"
    )

    html = """

    <style>

    .payment-container{
        max-height:650px;
        overflow-y:auto;
        border:1px solid #cbd5e1;
        background:#e5e7eb;
    }

    .payment-table{
        width:100%;
        border-collapse:collapse;
        font-size:13px;
        font-family:Arial,sans-serif;
        background:#e5e7eb;
    }

    .payment-table thead th{
        position:sticky;
        top:0;
        z-index:100;
        background:#002060;
        color:white;
        border:1px solid #cbd5e1;
        padding:8px;
        text-align:center;
        font-weight:bold;
    }

    .payment-table td{
        border:1px solid #cbd5e1;
        padding:7px;
    }

    .parent-even{
        background:#f3f4f6;
    }

    .parent-odd{
        background:#e5e7eb;
    }

    .child-payment-table{
        width:100%;
        border-collapse:collapse;
        background:#f8fafc;
    }

    .child-payment-table thead th{
        background:#d9e1f2;
        color:#111827;
        border:1px solid #cbd5e1;
        padding:7px;
        text-align:center;
        font-weight:bold;
        position:sticky;
        top:40px;
        z-index:99;
    }

    .child-payment-table td{
        border:1px solid #cbd5e1;
        padding:6px;
    }

    .child-even{
        background:#ffffff;
    }

    .child-odd{
        background:#f1f5f9;
    }

    .toggle-icon{
        cursor:pointer;
        font-weight:bold;
        font-size:16px;
        margin-right:6px;
    }

    .qty{
        text-align:right;
    }

    .center{
        text-align:center;
    }

    .shop-link{
        font-weight:bold;
        text-decoration:none;
        color:#111827;
    }

    .shop-link:hover{
        text-decoration:underline;
    }

    </style>

    <div class="payment-container">

        <table class="payment-table">

            <thead>

                <tr>

                    <th style="width:5%">Sr</th>

                    <th style="width:12%">
                        Shop ID
                    </th>

                    <th style="width:20%">
                        Shop Name
                    </th>

                    <th style="width:18%">
                        Location
                    </th>

                    <th style="width:15%">
                        Billed
                    </th>

                    <th style="width:15%">
                        Outstanding
                    </th>

                </tr>

            </thead>

            <tbody>
    """

    sr = 1

    for shop in shop_data:

        # --------------------------------------------------
        # CUSTOMER
        # --------------------------------------------------

        customer_id = frappe.db.get_value(
            "Customer",
            {
                "custom_retail_customer": shop.name
            },
            "name"
        )

        if not customer_id:
            continue

        # --------------------------------------------------
        # BILL SUMMARY
        # --------------------------------------------------

        bill_summary = frappe.db.sql("""

            SELECT

                SUM(total_amount) as billed,
                SUM(total_amount - paid_amount) as outstanding

            FROM `tabRS Invoice`

            WHERE customer = %s
            AND docstatus = 1

        """, (customer_id,), as_dict=True)

        billed = bill_summary[0].billed or 0
        outstanding = bill_summary[0].outstanding or 0

        # ONLY BILLED > 0

        if billed <= 0:
            continue

        # --------------------------------------------------
        # CHILD TABLE DATA
        # --------------------------------------------------

        invoice_data = frappe.db.sql("""

            SELECT

                name,
                invoice_date,
                total_amount,
                paid_amount,
                (total_amount - paid_amount) as outstanding

            FROM `tabRS Invoice`

            WHERE customer = %s
            AND docstatus = 1

            ORDER BY invoice_date desc

        """, (customer_id,), as_dict=True)

        child_rows = ""
        child_sr = 1

        for row in invoice_data:

            child_class = (
                "child-even"
                if child_sr % 2 == 0
                else "child-odd"
            )

            age = ""

            if row.invoice_date:

                age = (
                    getdate(nowdate()) -
                    getdate(row.invoice_date)
                ).days

                age = str(age) + " Days"

            child_rows += f"""

                <tr class="{child_class}">

                    <td>

                        <a href="/app/rs-invoice/{row.name}"
                           target="_blank"
                           class="shop-link">

                            {row.name}

                        </a>

                    </td>

                    <td class="center">

                        {formatdate(row.invoice_date)
                            if row.invoice_date else ''}

                    </td>

                    <td class="qty">

                        {round(row.total_amount or 0, 2)}

                    </td>

                    <td class="qty">

                        {round(row.outstanding or 0, 2)}

                    </td>

                    <td class="center">

                        {age}

                    </td>

                </tr>

            """

            child_sr += 1

        # --------------------------------------------------
        # NO DATA
        # --------------------------------------------------

        if not child_rows:

            child_rows = """

                <tr class="child-even">

                    <td colspan="5"
                        class="center">

                        No Invoice Available

                    </td>

                </tr>

            """

        # --------------------------------------------------
        # ROW COLOR
        # --------------------------------------------------

        parent_class = (
            "parent-even"
            if sr % 2 == 0
            else "parent-odd"
        )

        # --------------------------------------------------
        # MAIN TABLE ROW
        # --------------------------------------------------

        html += f"""

            <tr class="{parent_class}">

                <td class="center">

                    {sr}

                </td>

                <td>

                    <span class="toggle-icon"
                        onclick="toggle_payment_details('{shop.name}', this)">

                        +

                    </span>

                    <a href="/app/shop-rc/{shop.name}"
                       target="_blank"
                       class="shop-link">

                        {shop.name}

                    </a>

                </td>

                <td>

                    {shop.customer_name or ''}

                </td>

                <td>

                    {shop.city or ''}

                </td>

                <td class="qty">

                     ₹ {format(round(billed, 2), ",.2f")}

                </td>

                <td class="qty">

                     ₹ {format(round(outstanding, 2), ",.2f")}

                </td>

            </tr>

            <tr id="payment_detail_{shop.name}"
                style="display:none;">

                <td colspan="6"
                    style="padding:0px;">

                    <table class="child-payment-table">

                        <thead>

                            <tr>

                                <th>
                                    Bill Number
                                </th>

                                <th>
                                    Invoice Date
                                </th>

                                <th>
                                    Billed
                                </th>

                                <th>
                                    Outstanding
                                </th>

                                <th>
                                    Age
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {child_rows}

                        </tbody>

                    </table>

                </td>

            </tr>

        """

        sr += 1

    html += """

            </tbody>

        </table>

    </div>

    <script>

    function toggle_payment_details(id, element){

        let row = document.getElementById(
            "payment_detail_" + id
        );

        if(row.style.display === "none"){

            row.style.display = "table-row";

            element.innerHTML = "-";
        }
        else{

            row.style.display = "none";

            element.innerHTML = "+";
        }
    }

    </script>

    """

    return html
@frappe.whitelist()
def get_total_stock_qty_value():

    result = frappe.db.sql("""
        SELECT
            COALESCE(SUM(bin.actual_qty), 0) AS total_stock_qty,

            COALESCE(
                SUM(bin.actual_qty * bin.valuation_rate),
            0) AS total_stock_value

        FROM `tabBin` bin

        INNER JOIN `tabWarehouse` wh
            ON wh.name = bin.warehouse

        WHERE wh.company = 'TEAMPRO Food Products'
    """, as_dict=1)

    return result[0] if result else {
        "total_stock_qty": 0,
        "total_stock_value": 0
    }

@frappe.whitelist()
def get_opportunity_count():

    count = frappe.db.sql("""
        SELECT COUNT(name)
        FROM `tabOpportunity`
        WHERE status NOT IN ('Lost', 'Closed')
        AND service='TFP'
    """)[0][0] or 0

    return count

@frappe.whitelist()
def get_delivery_status_summary():

    data = {}

    # PACKING
    packing = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT so.name) AS count,
            COALESCE(SUM(soi.qty), 0) AS qty

        FROM `tabSales Order` so

        INNER JOIN `tabSales Order Item` soi
            ON soi.parent = so.name

        WHERE so.docstatus = 1
        AND so.status = 'To Deliver and Bill'
        AND so.company = 'TEAMPRO Food Products'
        AND so.service = 'TFP'
    """, as_dict=1)[0]

    data["packing"] = packing

    # SCHEDULED
    scheduled = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT dn.name) AS count,
            COALESCE(SUM(dni.qty), 0) AS qty

        FROM `tabDelivery Note` dn

        INNER JOIN `tabDelivery Note Item` dni
            ON dni.parent = dn.name

        WHERE dn.docstatus = 1
        AND dn.company = 'TEAMPRO Food Products'
        AND dn.custom_delivery_status_new = 'Schedule'
        AND IFNULL(dn.is_return, 0) = 0
    """, as_dict=1)[0]

    data["scheduled"] = scheduled

    # PACKED
    packed = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT dn.name) AS count,
            COALESCE(SUM(dni.qty), 0) AS qty

        FROM `tabDelivery Note` dn

        INNER JOIN `tabDelivery Note Item` dni
            ON dni.parent = dn.name

        WHERE dn.docstatus = 1
        AND dn.company = 'TEAMPRO Food Products'
        AND dn.custom_delivery_status_new = 'Packed'
        AND IFNULL(dn.is_return, 0) = 0
    """, as_dict=1)[0]

    data["packed"] = packed

    # DISPATCHED
    dispatched = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT dn.name) AS count,
            COALESCE(SUM(dni.qty), 0) AS qty

        FROM `tabDelivery Note` dn

        INNER JOIN `tabDelivery Note Item` dni
            ON dni.parent = dn.name

        WHERE dn.docstatus = 1
        AND dn.company = 'TEAMPRO Food Products'
        AND dn.custom_delivery_status_new = 'Dispatched'
        AND IFNULL(dn.is_return, 0) = 0
    """, as_dict=1)[0]

    data["dispatched"] = dispatched

    return data