# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt



import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 200},
         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
        {"label": "Stock Quantity", "fieldname": "stock_qty", "fieldtype": "Float", "width": 150},
        {"label": "Physical Quantity", "fieldname": "physical_qty", "fieldtype": "Float", "width": 150},
        {"label": "Difference", "fieldname": "difference", "fieldtype": "Float", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
        
    ]


from frappe.utils import flt

def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND DATE(sd.date_and_time) BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters["from_date"]
        values["to_date"] = filters["to_date"]
    items = frappe.get_all("Item", filters={"tfp": 1, "disabled": 0}, fields=["*"])
    data = []

    for item in items:
        item_code = item.name
        
        result = frappe.db.sql(f"""
            SELECT SUM(sd.count) AS physical_qty
            FROM `tabStock Counting Details` sd
            WHERE sd.item = %(item_code)s {conditions}
        """, {**values, "item_code": item_code}, as_dict=True)

        physical_qty = flt(result[0].physical_qty) if result and result[0].physical_qty else 0
        stock_qty = frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": "Stores - TFP"}, "actual_qty") or 0
        diff = flt(stock_qty) - flt(physical_qty)
        status = "Match" if diff == 0 else "Variance"
        if physical_qty > 0 or stock_qty > 0:
            data.append({
                "item": item_code,
                "item_name":item.item_name,
                "stock_qty": stock_qty,
                "physical_qty": physical_qty,
                "difference": diff,
                "status":status
            })

    return data
                