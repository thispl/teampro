# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopRC(Document):
	def before_insert(self):
		code = "SHOP"

		last_id = frappe.db.get_value(
			"Shop RC",
			filters={"docstatus":["!=", "2"],'amended_from':["is", "not set"]},
			fieldname="name",
			order_by="creation desc"
		)

		if last_id:
			last_num = int(last_id.split("-")[-1])
			new_num = last_num + 1
		else:
			new_num = 1

		self.customer_id = f"{code}-{new_num:03d}"
		

	def validate(self):
		existing = frappe.db.exists("Shop RC",{"customer_name": self.customer_name, "name": ["!=", self.name]})
		if existing:
			frappe.throw("Customer Name already exists!")

		if self.workflow_state == "Pending for Verification":

			existing = frappe.db.exists("Customer", {
				"customer_name": self.customer_name,
				"customer_group": "Retail Shops",
				"disabled":0,
				"gstin": self.gst_no
			})

			if existing:
				frappe.throw("Customer already exists!!")

	def on_update(self):
		if not self.has_value_changed("status"):
			return

		disable_value = 1 if self.status == "Inactive" else 0

		customers = frappe.get_all(
			"Customer",
			filters={"custom_retail_customer": self.name},
			pluck="name"
		)

		for cust in customers:
			frappe.db.set_value("Customer", cust, "disabled", disable_value)

		warehouses = frappe.get_all(
			"Warehouse",
			filters={"custom_retail_customer": self.name},
			pluck="name"
		)

		for wh in warehouses:
			frappe.db.set_value("Warehouse", wh, "disabled", disable_value)

		address = frappe.get_all(
			"Address",
			filters={"custom_retail_customer": self.name},
			pluck="name"
		)

		for ad in address:
			frappe.db.set_value("Address", ad, "disabled", disable_value)

	def on_update_after_submit(self):
		if not self.has_value_changed("status"):
			return

		disable_value = 1 if self.status == "Inactive" else 0

		customers = frappe.get_all(
			"Customer",
			filters={"custom_retail_customer": self.name},
			pluck="name"
		)

		for cust in customers:
			frappe.db.set_value("Customer", cust, "disabled", disable_value)

		warehouses = frappe.get_all(
			"Warehouse",
			filters={"custom_retail_customer": self.name},
			pluck="name"
		)

		for wh in warehouses:
			frappe.db.set_value("Warehouse", wh, "disabled", disable_value)

		address = frappe.get_all(
			"Address",
			filters={"custom_retail_customer": self.name},
			pluck="name"
		)

		for ad in address:
			frappe.db.set_value("Address", ad, "disabled", disable_value)


	def on_submit(self):
		if not frappe.db.exists("Existing Customer", {"customer_id": self.customer_name}):

			existing_customer = frappe.get_doc({
				"doctype": "Existing Customer",
				"customer_id": self.customer_name
			})
			existing_customer.insert(ignore_permissions=True)
			
		if self.city:
			if not frappe.db.exists("Location", self.city):
				location_doc = frappe.get_doc({
					"doctype": "Location",
					"location_name": self.city
				})
				location_doc.insert(ignore_permissions=True)

		if not frappe.db.exists("Customer", {"customer_name": self.customer_name}):
			gst_category = "Unregistered"
			gstin = ""

			if self.gst_no:
				gst_category = "Registered Regular"
				gstin = self.gst_no

			customer = frappe.get_doc({
				"doctype": "Customer",
				"customer_name": self.customer_name,
				"customer_type": "Individual",
				"customer_group":"Retail Shops",
				"custom_retail_customer":self.name,
				"custom_is_retail_customer":1,
				"account_manager":"amirtham.g@groupteampro.com",
				"territory":self.territory,
				"location":self.city,
				"gst_category":gst_category,
				"gstin": gstin,
				"default_currency":"INR"
			}) 
			customer.insert(ignore_permissions=True)

		if not frappe.db.exists("Address", {"address_title": self.customer_name}):

			address = frappe.get_doc({
				"doctype":"Address",
				"address_title":self.customer_name,
				"address_type":"Billing",
				"address_line1":self.address_line_1,
				"address_line2":self.street,
				"city":self.city,
				"state":self.state,
				"country":self.country,
				"pincode":self.postal_code,
				"phone":self.phone,
				"custom_retail_customer":self.name,
				"custom_is_customer_rc":1
			})
			address.append("links", {
					"link_doctype": "Customer",
					"link_name": self.customer_name
				})
			address.insert(ignore_permissions = True)

		if not frappe.db.exists("Warehouse", {"custom_retail_customer":self.name}):
			warehouse_name = f"WH-{self.name}"

			warehouse = frappe.get_doc({
				"doctype":"Warehouse",
				"warehouse_name":warehouse_name,
				"company":"TEAMPRO Food Products",
				"custom_retail_customer":self.name,
				"parent_warehouse":"Retail Shops - TFP"

			})
			warehouse.insert(ignore_permissions = True)

			

	def on_cancel(self):

		customer_name = frappe.db.get_value(
			"Customer",
			{"custom_retail_customer": self.name},
			"name"
		)

		if customer_name:
			frappe.db.set_value("Customer", customer_name, "disabled", 1)

		warehouse_name = frappe.db.get_value(
			"Warehouse",
			{"custom_retail_customer": self.name},
			"name"
		)

		if warehouse_name:
			frappe.db.set_value("Warehouse", warehouse_name, "disabled", 1)

		address_list = frappe.get_all(
			"Address",
			filters={"custom_retail_customer": self.name},
			pluck="name"
		)

		for address in address_list:
			frappe.db.set_value("Address", address, "disabled", 1)
