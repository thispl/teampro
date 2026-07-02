# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StockCounting(Document):
	pass

from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,datetime,get_first_day,get_last_day,today,fmt_money)

@frappe.whitelist()
def get_previous_count(name,date):
    prev_date=add_days(date,-1)
    result = frappe.db.sql("""
        SELECT SUM(sd.count)
        FROM `tabStock Counting` sc
        JOIN `tabStock Counting Details` sd ON sc.name = sd.parent
        WHERE sc.date = %s AND sd.item = %s AND DATE(sd.date_and_time)=%s
    """, (prev_date, name,prev_date))

    return result[0][0] or 0


import frappe
from frappe.utils import nowdate, flt, today
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from datetime import datetime
from io import BytesIO
import base64

@frappe.whitelist()
def stock_counting_report_excel():
    formatted_date = frappe.utils.format_datetime(frappe.utils.nowdate(), "dd-MM-yyyy")
    filename = "Physical_Vs_ERP_Stock_balance_" + formatted_date
    xlsx_file = build_xlsx_response_stock(filename)
    send_mail_with_attachment_stock(filename, xlsx_file.getvalue())


def send_mail_with_attachment_stock(filename,file_content):
    formatted_date = frappe.utils.format_datetime(frappe.utils.nowdate(), "dd-MM-yyyy")
    attachments = [{"fname": filename + '.xlsx', "fcontent": file_content}]
    frappe.sendmail(
        recipients=["divya.p@groupteampro.com","dineshbabu.k@groupteampro.com"],  # Change to real recipient
        cc=["sangeetha.s@groupteampro.com","tfp@groupteampro.com"],
        subject="Physical Vs ERP Stock Balance - " + formatted_date,
        message="Please find attached the Physical Vs ERP Stock Balance report.",
        attachments=attachments,

    )

def build_xlsx_response_stock(filename):
    return make_xlsx_physical_stock(filename)

def make_xlsx_physical_stock(filename, sheet_name=None, wb=None, column_widths=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Physical Vs ERP Stock Balance"

    # Styles
    text_wrap_left = Alignment(vertical="center", horizontal="center", wrap_text=True)
    text_wrap_center = Alignment(vertical="center", horizontal="center", wrap_text=True)
    bold_white_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="FF002060", end_color="FF002060", fill_type="solid")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Set column widths (A to F now)
    # for col in range(2, 8):  # A to F
    #     ws.column_dimensions[chr(64 + col)].width = 20

    ws.column_dimensions['A'].width = 10   # S.No
    ws.column_dimensions['B'].width = 20   # Item Code
    ws.column_dimensions['C'].width = 40   # Item Name
    ws.column_dimensions['D'].width = 10   # Stock Qty
    ws.column_dimensions['E'].width = 10   # Physical Qty
    ws.column_dimensions['F'].width = 10   # Difference
    ws.column_dimensions['G'].width = 10   # Status


    # Headers with status
    headers = ["S.No", "Item","Item Name", "Stock Qty", "Physical Qty", "Difference", "Status"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = bold_white_font
        cell.fill = header_fill
        cell.border = border
        cell.alignment = text_wrap_left

    # Data
    data = get_stock_data()
    for i, row in enumerate(data, start=1):
        status = "Match" if row["difference"] == 0 else "Variance"
        ws.append([
            i,
            row["item"],
            row["item_name"],
            row["stock_qty"],
            row["physical_qty"],
            row["difference"],
            status
        ])
        for j in range(1, 8):  # columns A to F
            cell = ws.cell(row=i+1, column=j)
            # cell.alignment = text_wrap_center
            # cell.border = border
            if j in [1, 2, 3, 7]:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
            cell.border = border
            if j == 7:  # Status column
                if status == "Match":
                    cell.font = Font(bold=True, color="008000")  # Green
                else:
                    cell.font = Font(bold=True, color="FF0000")  # Red

    # Save to in-memory file
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file

def get_stock_data():
    today = nowdate()
    latest_stock_counting = frappe.get_all(
        "Stock Counting",
        filters={"docstatus": 1},
        fields=["name", "date"],
        order_by="date desc",
        limit=1
    )

    if not latest_stock_counting:
        return []

    latest_date = latest_stock_counting[0].date

    items = frappe.get_all("Item", filters={"tfp": 1, "disabled": 0}, fields=["*"])
    data = []

    for item in items:
        item_code = item.name
        result = frappe.db.sql("""
            SELECT SUM(sd.count) AS physical_qty
            FROM `tabStock Counting Details` sd
            JOIN `tabStock Counting` sc ON sd.parent = sc.name
            WHERE sd.item = %(item_code)s
            AND sc.date = %(date)s
            AND sc.docstatus = 1
        """, {"item_code": item_code, "date": latest_date}, as_dict=True)

        physical_qty = flt(result[0].physical_qty) if result and result[0].physical_qty else 0
        stock_qty = frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0
        diff = flt(stock_qty) - flt(physical_qty)
        if physical_qty > 0 or stock_qty > 0:
            data.append({
                "item": item_code,
                "item_name":item.item_name,
                "stock_qty": round(stock_qty,2),
                "physical_qty": round(physical_qty,2),
                "difference": round(diff,2),
            })

    return data