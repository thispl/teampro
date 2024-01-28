# Copyright (c) 2023, TeamPRO and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.utils import flt
import erpnext

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
		_("Sales Order") + ":Link/Sales Order:300",
		_("Outstanding Grand Total") + ":Currency:200"

	]
	return columns

def get_data(filters):
	data = []
	if filters.sales_order:
		frappe.errprint(filters.sales_order)
		sales_orders = frappe.db.get_all("Sales Order",{'name':filters.sales_order},['*'])
	else:
		sales_orders = frappe.db.get_all("Sales Order",['*'])

	for i in sales_orders:
		total = i.base_grand_total
		bill = i.per_billed
		paid = i.advance_paid
		outstanding = total -( (total * bill / 100) + paid)
		row = [i.name, outstanding]
		data.append(row)
	return data