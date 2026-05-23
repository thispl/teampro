# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.stock.utils import get_stock_balance
from frappe.utils import nowdate
from frappe.utils import flt


class RCReturn(Document):
	def on_submit(self):
		stock_available = True
		for row in self.return_items:
			if row.return_qty <0:
				frappe.throw("Return Quantity must be a postive number")

				available_qty = get_stock_balance(
					row.item_code,
					self.customer_warehouse
				)
				conversion_factor = get_conversion_factor(row.item_code, row.uom)
				required_qty = flt(row.return_qty) * conversion_factor
				if available_qty:
					if available_qty < required_qty:
						stock_available = False
						frappe.throw(f"Not enough stock for Item {row.item_code} in {self.customer_warehouse}. Available: {available_qty}, Required: {row.return_qty}")

		if stock_available:
			se = frappe.get_doc({
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Transfer",
				"posting_date": nowdate(),
				"company":"TEAMPRO Food Products",
				"custom_rc_return":self.name,
				"from_warehouse":self.customer_warehouse,
				"to_warehouse":self.dispatch_warehouse,
				"items": []
			})

			for item in self.return_items:
				se.append("items", {
					"item_code": item.item_code,
					"qty": item.return_qty,
					"uom": item.uom,
					"s_warehouse": self.customer_warehouse,
					"t_warehouse": self.dispatch_warehouse
				})

			se.insert()
			se.submit()
			frappe.msgprint(f"Stock Entry {se.name} created.")
			rc_se=frappe.new_doc("Stock Entry")
			rc_se.stock_entry_type="Material Transfer"
			rc_se.posting_date=nowdate()
			rc_se.company="TEAMPRO Food Products"
			rc_se.custom_rc_return=self.name
			for item in self.return_items:
				rc_se.append("items", {
						"item_code": item.item_code,
						"qty": item.return_qty,
						"uom": item.uom,
						"s_warehouse": self.dispatch_warehouse,
						"t_warehouse": "Stores - TFP"
					})
			rc_se.insert()
			rc_se.submit()

	def on_cancel(self):
		stock_entries = frappe.get_all(
			"Stock Entry",
			filters={"custom_rc_return": self.name},
			fields=["name", "docstatus"]
		)

		for se in stock_entries:
			se_doc = frappe.get_doc("Stock Entry", se.name)
			if se_doc.docstatus == 1:
				se_doc.cancel() 


@frappe.whitelist()
def get_transferred_items(customer, customer_warehouse):
    stock_items = frappe.db.sql("""
        SELECT 
            bin.item_code,
            bin.warehouse,
            bin.actual_qty AS qty,
            item.item_name,
            item.stock_uom AS uom
        FROM `tabBin` bin
        JOIN `tabItem` item ON item.name = bin.item_code
        WHERE bin.warehouse = %s
          AND bin.actual_qty > 0
        ORDER BY bin.item_code
    """, (customer_warehouse,), as_dict=1)

    return stock_items


@frappe.whitelist()
def get_conversion_factor(item_code, uom):
		cf = frappe.db.get_value(
			"UOM Conversion Detail",
			{"parent": item_code, "uom": uom},
			"conversion_factor"
		)
		return flt(cf) if cf else 1  
