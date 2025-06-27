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
def get_order_booking(from_date=None, to_date=None):
    conditions = ["service = 'TFP'", "docstatus = 1", "status NOT IN ('On Hold', 'Cancelled', 'Closed')"]
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

@frappe.whitelist()
def get_total_so_qty(from_date=None,to_date=None):
    conditions = ["service = 'TFP'", "docstatus = 1", "status NOT IN ('On Hold', 'Completed', 'Cancelled', 'Closed')"]
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

    query = f"""
        SELECT SUM(total_qty)
        FROM `tabSales Order`
        WHERE {' AND '.join(conditions)}
    """
    # frappe.db.sql("""SELECT SUM(total_qty) FROM `tabSales Order` where service='TFP' and docstatus=1 and status NOT IN ('On Hold', 'Completed', 'Cancelled', 'Closed') """)[0][0] or 0

    result = frappe.db.sql(query, {'from_date': from_date, 'to_date': to_date})[0][0] or 0
    return result

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
        'from_date': from_date,
        'to_date': to_date
    }

    # Total Submitted Purchase Invoice Amount
    total_invoice = frappe.db.sql("""
        SELECT SUM(outstanding_amount)
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
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
        'from_date': from_date,
        'to_date': to_date
    }

    # Total Submitted Purchase Invoice Amount
    total_invoice = frappe.db.sql("""
        SELECT SUM(outstanding_amount)
        FROM `tabSales Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
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
    from frappe.utils import today, getdate, nowdate
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
        SELECT name, customer, outstanding_amount, posting_date
        FROM `tabSales Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND outstanding_amount > 0
        ORDER BY posting_date
    """, filters, as_dict=True)

    # html = """<div style='overflow-x: auto;'>
    # <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
    #     <thead>
    #         <tr style="background-color: #002060; color: white;text-align:center">
    #             <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Sales Invoice ID</th>
    #             <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Customer</th>
    #             <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Value</th>
    #             <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Age (days)</th>
    #         </tr>
    #     </thead>
    #     <tbody>
    # """
    html = """
        <div style='max-height: 340px; overflow-y: auto;'>
            <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
                <thead>
                    <tr>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Sales Invoice ID</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Customer</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Value</th>
                        <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Age (days)</th>
                    </tr>
                </thead>
                <tbody>
        """


    today_date = getdate(nowdate())
    for row in data:
        age = (today_date - getdate(row.posting_date)).days
        row_style = "color: red;" if age > 30 else ""  # Apply to whole row
        html += f"""
            <tr style="{row_style}">
                <td>{row.name}</td>
                <td>{row.customer}</td>
                <td style='text-align:right;'>{frappe.utils.fmt_money(row.outstanding_amount)}</td>
                <td style='text-align:right;'>{age}</td>
            </tr>
        """

    # for row in data:
    #     age = (today_date - getdate(row.posting_date)).days
    #     age_color = "red" if age > 30 else "black"
    #     html += f"""
    #         <tr>
    #             <td>{row.name}</td>
    #             <td>{row.customer}</td>
    #             <td style='text-align:right;'>{frappe.utils.fmt_money(row.outstanding_amount)}</td>
    #             <td style='color: {age_color};text-align:right;'>{age}</td>
    #         </tr>
    #     """

    html += "</tbody></table></div>"

    return html

@frappe.whitelist()
def tfp_payable_table():
    from frappe.utils import today, getdate, nowdate
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
        SELECT name, supplier, outstanding_amount, posting_date
        FROM `tabPurchase Invoice`
        WHERE docstatus = 1
          AND company = %(company)s
          AND posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND outstanding_amount > 0
        ORDER BY posting_date
    """, filters, as_dict=True)

    html = """<div style='max-height: 340px; overflow-y: auto;'>
    <table class='table table-bordered' style='width: 100%; border-collapse: collapse;'>
        <thead>
            <tr>
                <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Purchase Invoice ID</th>
                <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Supplier</th>
                <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Value</th>
                <th style="position: sticky; top: 0; background: #002060; color: white; text-align: center;">Age (days)</th>
            </tr>
        </thead>
        <tbody>
    """

    today_date = getdate(nowdate())
    for row in data:
        age = (today_date - getdate(row.posting_date)).days
        row_style = "color: red;" if age > 30 else ""  # Apply to whole row
        html += f"""
            <tr style="{row_style}">
                <td>{row.name}</td>
                <td>{row.supplier}</td>
                <td style='text-align:right;'>{frappe.utils.fmt_money(row.outstanding_amount)}</td>
                <td style='text-align:right;'>{age}</td>
            </tr>
        """

    # for row in data:
    #     age = (today_date - getdate(row.posting_date)).days
    #     age_color = "red" if age > 30 else "black"
    #     html += f"""
    #         <tr>
    #             <td>{row.name}</td>
    #             <td>{row.supplier}</td>
    #             <td style='text-align:right;'>{frappe.utils.fmt_money(row.outstanding_amount)}</td>
    #             <td style='color: {age_color};text-align:right;'>{age}</td>
    #         </tr>
    #     """

    html += "</tbody></table></div>"

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
# from frappe.utils import formatdate

# @frappe.whitelist()
# def get_tfp_stock_html():
#     from frappe.utils import formatdate, nowdate, getdate
#     from datetime import timedelta

#     warehouse = "Stores - TFP"

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
#         JOIN `tabItem` item ON bin.item_code = item.name
#         WHERE bin.warehouse = %s
#         AND bin.actual_qty > 0
#         ORDER BY bin.item_code
#     """, (warehouse, warehouse), as_dict=True)

#     html = """
#     <table class="table table-bordered">
#         <thead>
#             <tr style="background-color: #002060; color: white; text-align:center;">
#                 <th>Item Code</th>
#                 <th>Item Name</th>
#                 <th>Quantity</th>
#                 <th>Stock UOM</th>
#                 <th>Last PR Date</th>
#             </tr>
#         </thead>
#         <tbody>
#     """

#     today = getdate(nowdate())

#     for row in stock_data:
#         pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
#         is_old = pr_date and (today - pr_date).days > 30

#         # Conditional red style
#         red_style = 'style="color: red; font-weight: bold;"' if is_old else ""

#         html += f"""
#             <tr>
#                 <td {red_style}>{row.item_code}</td>
#                 <td>{row.item_name}</td>
#                 <td style="text-align:right">{row.actual_qty}</td>
#                 <td>{row.stock_uom}</td>
#                 <td {red_style}>{formatdate(pr_date) if pr_date else '-'}</td>
#             </tr>
#         """

#     html += "</tbody></table>"

#     return html

import frappe
from frappe.utils import formatdate, nowdate, getdate

@frappe.whitelist()
def get_tfp_stock_html():
    from datetime import timedelta

    warehouse = "Stores - TFP"
    item_group="Food Products"
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
        JOIN `tabItem` item ON bin.item_code = item.name AND item.item_group=%s
        WHERE bin.warehouse = %s
        AND bin.actual_qty > 0
    """, (warehouse,item_group, warehouse), as_dict=True)

    today = getdate(nowdate())
    
    # Add age and is_old to each row
    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        row.age = (today - pr_date).days if pr_date else None
        row.is_old = row.age is not None and row.age > 30

    # Sort: red (old) rows first
    stock_data.sort(key=lambda x: not x.is_old)

    # HTML table with sticky headers
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


# @frappe.whitelist()
# def get_tfp_vm_stock_html():
#     warehouse = "VM1_Precision - TFP"
    
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
#         JOIN `tabItem` item ON bin.item_code = item.name
#         WHERE bin.warehouse = %s
#         AND bin.actual_qty > 0
#         ORDER BY bin.item_code
#     """, (warehouse, warehouse), as_dict=True)

#     html = """
#     <table class="table table-bordered">
#         <thead>
#             <tr style="background-color: #002060; color: white; text-align:center;">
#                 <th>Item Code</th>
#                 <th>Item Name</th>
#                 <th>Quantity</th>
#                 <th>Stock UOM</th>
#                 <th>Last PR Date</th>
#             </tr>
#         </thead>
#         <tbody>
#     """

#     today = getdate(nowdate())

#     for row in stock_data:
#         pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
#         is_old = pr_date and (today - pr_date).days > 30

#         # Conditional red style
#         red_style = 'style="color: red; font-weight: bold;"' if is_old else ""

#         html += f"""
#             <tr>
#                 <td {red_style}>{row.item_code}</td>
#                 <td>{row.item_name}</td>
#                 <td style="text-align:right">{row.actual_qty}</td>
#                 <td>{row.stock_uom}</td>
#                 <td {red_style}>{formatdate(pr_date) if pr_date else '-'}</td>
#             </tr>
#         """

#     html += "</tbody></table>"

#     return html
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
    
    # Add age and is_old to each row
    for row in stock_data:
        pr_date = getdate(row.last_pr_date) if row.last_pr_date else None
        row.age = (today - pr_date).days if pr_date else None
        row.is_old = row.age is not None and row.age > 30

    # Sort: red (old) rows first
    stock_data.sort(key=lambda x: not x.is_old)

    # HTML table with sticky headers
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

        # vm_button_html = f'''
        #     <button class="submit-stock-btn"
        #         data-vm-reg="{register.name}"
        #         style="background-color: #f5f5f5; border: none; outline: none; box-shadow: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; color: {'green' if show_submit else 'red'};">
        #         {"Submit Stock" if show_submit else "Create MR"}
        #     </button>
        # '''
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
                    grand_total_qty += total_vm_qty
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
                        <td style="text-align:center;">Item</td>
                        <td style="text-align:center;">Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">Stock Qty</td>
                        <td style="text-align:center;">UOM</td>
                        <td style="text-align:center;">MRP</td>
                        <td style="text-align:center;" colspan="2">Packing Details</td>
                        <td style="text-align:center;" colspan="2">WRD Details</td>
                        <td style="text-align:center;" colspan="1">Packed Qty</td>
                        <td style="text-align:center;" colspan="1">Name Details</td>
                    </tr>'''
                
            if item.custom_wrd_rate:
                item_rate=f"{float(item.custom_wrd_rate):.2f}"
            else:
                item_rate=''
            # html += f'''
            # <tr class="details-row dos-{item.against_sales_order}" style="display:none;">
            #     <td style="text-align:left;">{item.item_name}</td>
            #     <td style="text-align:center;">{item.qty}</td>
            #     <td style="text-align:center;">{item.uom}</td>
            #     <td style="text-align:center;">{item.stock_qty}</td>
            #     <td style="text-align:center;">{item.stock_uom}</td>
            #     <td style="text-align:right;">{item.mrp}</td>
            #     <td style="text-align:left;" colspan="2">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
            #     <td style="text-align:left;">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
            #     <td style="text-align:center;">{item.custom_name_print or ""}</td>
            # </tr>
            # '''
            html += f'''
                <tr class="details-row dos-{item.against_sales_order}" style="display:none;">
                    <td style="text-align:left;">{item.item_name}</td>
                    <td style="text-align:center;">{item.qty}</td>
                    <td style="text-align:center;">{item.uom}</td>
                    <td style="text-align:center;">{item.stock_qty}</td>
                    <td style="text-align:center;">{item.stock_uom}</td>
                    <td style="text-align:right;">{item.mrp}</td>
                    <td style="text-align:left;" colspan="2">(C): {primary or "None"}: {item.custom_covers or "0"}<br>(B): {secondary or "None"}: {item.custom_bag or "0"}<br>(BX): {tertiary or "None"}: {item.custom_box or "0"}</td>
                    <td style="text-align:left;" colspan="2">(W): {item.custom_wrd_uom or ""}<br>(R): {item_rate or ""}<br>(D): {formatdate(item.custom_mfg_on) if item.custom_mfg_on else ""}</td>
                    <td style="text-align:center;">{item.qty}</td>
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
            <td colspan="7" style="text-align:right;"></td>
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
