# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.stock.utils import get_stock_balance
from frappe.utils import nowdate
from frappe.utils import flt



class RetailStockMovement(Document):
	def validate(self):
		if not self.dispatch_warehouse:
			frappe.throw("Please select Dispatch Warehouse")

		for row in self.items:

			if not row.item_code:
				continue

			available_qty = get_stock_balance(
				row.item_code,
				self.dispatch_warehouse
			)
			required_qty = flt(row.qty)

			if flt(available_qty) < required_qty:
				frappe.throw(
					f"""
					Insufficient Stock for Item: {row.item_code}<br>
					Warehouse: {self.dispatch_warehouse}<br>
					Available Qty: {available_qty}<br>
					Required Qty: {row.qty}
					"""
				)

	def on_submit(self):
		stock_available = True

		for row in self.items:
			available_qty = get_stock_balance(
				row.item_code,
				self.dispatch_warehouse
			)

			required_qty = flt(row.qty)

			if flt(available_qty) < required_qty:
				stock_available = False
				frappe.throw(f"Not enough stock for Item {row.item_code} in {self.dispatch_warehouse}. Available: {available_qty}, Required: {row.qty}")

		if stock_available:
			se = frappe.get_doc({
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Transfer",
				"posting_date": nowdate(),
				"company":"TEAMPRO Food Products",
				"custom_rc_delivery":self.name,
				"items": []
			})

			for item in self.items:
				se.append("items", {
					"item_code": item.item_code,
					"qty": item.qty,
					"uom": item.uom,
					"s_warehouse": self.dispatch_warehouse,
					"t_warehouse": self.customer_warehouse
				})

			se.insert()
			frappe.msgprint(f"Stock Entry {se.name} created.")

	def on_cancel(self):
		stock_entries = frappe.get_all(
			"Stock Entry",
			filters={"custom_rc_delivery": self.name},
			fields=["name", "docstatus"]
		)

		for se in stock_entries:
			se_doc = frappe.get_doc("Stock Entry", se.name)
			if se_doc.docstatus == 1:
				se_doc.cancel() 

