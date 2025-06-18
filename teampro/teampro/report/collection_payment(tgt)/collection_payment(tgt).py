# # Copyright (c) 2024, TeamPRO and contributors
# # For license information, please see license.txt

from frappe import _ 
import frappe
from frappe.utils import get_first_day, get_last_day, today

def execute(filters=None):
    if not filters:
        filters = {}

    # Set default dates if not provided
    filters.setdefault("from_date", get_first_day(today()))
    filters.setdefault("to_date", get_last_day(today()))

    conditions = "1=1"
    values = {
        "from_date": filters["from_date"],
        "to_date": filters["to_date"]
    }

    # if filters.get("company"):
    #     conditions += " AND company = %(company)s"
    #     values["company"] = filters["company"]

    # SQL query with dynamic conditions
    query = f"""
        SELECT 
            SUM(paid_amount) AS total_booked
        FROM 
            `tabPayment Entry`
        WHERE 
            status NOT IN ('Draft','Cancelled')
            AND payment_type = 'Pay'
            AND {conditions}
            AND posting_date BETWEEN %(from_date)s AND %(to_date)s AND company='TEAMPRO General Trading'
    """

    # Fetch data
    result = frappe.db.sql(query, values=values, as_dict=True)

    # Format data for report
    total_booked = result[0]["total_booked"] if result and result[0].get("total_booked") else 0

    data = [{
        "total_booked": total_booked
    }]

    columns = get_columns()
    return columns, data

def get_columns():
    return [
        {
            "label": _("Total Booked"),
            "fieldname": "total_booked",
            "fieldtype": "Currency",
            "width": 150
        }
    ]
