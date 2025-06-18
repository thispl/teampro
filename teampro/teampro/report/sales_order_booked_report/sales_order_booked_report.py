# # Copyright (c) 2024, TeamPRO and contributors
# # For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

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
            SUM(base_grand_total) AS total_booked
        FROM 
            `tabSales Order`
        WHERE 
            status NOT IN ('Cancelled', 'On Hold', 'Closed')
            AND {conditions}
            AND transaction_date BETWEEN %(from_date)s AND %(to_date)s AND company='TEAMPRO HR & IT Services Pvt. Ltd.'
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
# from frappe import _
# import frappe
# from frappe.utils import get_first_day, get_last_day, today

# def execute(filters=None):
#     if not filters:
#         filters = {}

#     # Set default dates if not provided
#     filters.setdefault("from_date", get_first_day(today()))
#     filters.setdefault("to_date", get_last_day(today()))

#     conditions = "1=1"
#     values = {
#         "from_date": filters["from_date"],
#         "to_date": filters["to_date"]
#     }

#     # Include company condition dynamically if provided
#     if filters.get("company"):
#         conditions += " AND company = %(company)s"
#         values["company"] = filters["company"]

#     # SQL query to fetch data for the chart
#     query = f"""
#         SELECT 
#             transaction_date,
#             SUM(base_grand_total) AS total_booked
#         FROM 
#             `tabSales Order`
#         WHERE 
#             status NOT IN ('Cancelled', 'On Hold', 'Closed')
#             AND {conditions}
#             AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
#         GROUP BY transaction_date
#         ORDER BY transaction_date
#     """

#     # Fetch data
#     result = frappe.db.sql(query, values=values, as_dict=True)

#     # Format the data for the chart
#     data = []
#     for row in result:
#         data.append({
#             "transaction_date": row.get("transaction_date"),
#             "total_booked": row.get("total_booked", 0)
#         })

#     columns = get_columns()
#     return columns, data

# def get_columns():
#     return [
#         {
#             "label": _("Date"),
#             "fieldname": "transaction_date",
#             "fieldtype": "Date",
#             "width": 150
#         },
#         {
#             "label": _("Total Booked"),
#             "fieldname": "total_booked",
#             "fieldtype": "Currency",
#             "width": 150
#         }
#     ]

