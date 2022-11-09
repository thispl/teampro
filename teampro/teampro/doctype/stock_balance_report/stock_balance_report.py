# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.stock.utils import get_stock_balance


class StockBalanceReport(Document):
	@frappe.whitelist()
	def get_data(self):
		stock_bal = get_stock_balance("TFP-983302201","Stores - TFP")
		frappe.errprint(stock_bal)
		return "hi" 
