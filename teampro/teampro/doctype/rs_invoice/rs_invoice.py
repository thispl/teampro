# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import frappe
from frappe.model.document import Document
from erpnext.stock.utils import get_stock_balance
from frappe.utils import nowdate


class RSInvoice(Document):
        
    def after_insert(self):
        if self.invoice_items:
            return

        # Check required fields
        if self.customer and self.customer_warehouse:

            # items = get_transferred_items_with_qty(
            # 	self.customer,
            # 	self.customer_warehouse
            # )
            items = transferred_items_with_qty(
                self.customer,
                self.customer_warehouse
            )
            if items:
                for item in items:
                    self.append("invoice_items", {
                        "item_code": item.get("item_code"),
                        "item_name": item.get("item_name"),
                        "uom": item.get("uom"),
                        "customer_qty": item.get("customer_qty")
                    })

                self.db_update()

            else:
                frappe.msgprint("No items found for this customer and warehouse.")


    def on_submit(self):
        stock_available = True
        for row in self.return_items:
            if row.return_qty <=0:
                frappe.throw("Return Quantity must be a postive number")
        
        if self.is_return == 1 and self.return_items:

            for row in self.return_items:
                available_qty = get_stock_balance(
                    row.item_code,
                    self.customer_warehouse
                )

                if available_qty < row.return_qty:
                    stock_available = False
                    frappe.throw(f"Not enough stock for Item {row.item_code} in {self.customer_warehouse}. Available: {available_qty}, Required: {row.return_qty}")

            if stock_available:
                se = frappe.get_doc({
                    "doctype": "Stock Entry",
                    "stock_entry_type": "Material Transfer",
                    "posting_date": nowdate(),
                    "company":"TEAMPRO Food Products",
                    "custom_rc_invoice":self.name,
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

        # if not self.customer_signature:
        # 	frappe.throw("Customer Signature is mandatory. Please upload signature before submitting.")

        if self.is_return == 0:

            remaining_paid = self.paid_amount or 0
            references = []

            for row in self.outstanding:

                if remaining_paid <= 0:
                    break

                if row.payable_amount and row.payable_amount > 0:

                    linked_si = frappe.db.get_value(
                        "Sales Invoice",
                        {"custom_rc_invoice_": row.invoice},
                        "name"
                    )

                    if linked_si:

                        allocate_amount = min(remaining_paid, row.payable_amount)

                        references.append({
                            "reference_name": linked_si,
                            "allocated_amount": allocate_amount
                        })

                        remaining_paid -= allocate_amount


            current_si_name = frappe.db.get_value(
                "Sales Invoice",
                {"custom_rc_invoice_": self.name, "docstatus":["!=",2]},
                "name"
            )

            if not current_si_name:
                current_si = create_sales_invoice(self)
            else:
                current_si = frappe.get_doc("Sales Invoice", current_si_name)


            if current_si.grand_total > 0 and remaining_paid > 0:

                existing = [d["reference_name"] for d in references]

                if current_si.name not in existing:

                    references.append({
                        "reference_name": current_si.name,
                        "allocated_amount": remaining_paid
                    })


            if references:
                create_payment_entry(self.customer, references, self.name, self.paid_amount)

        # if self.is_return == 0:
        # 	remaining_paid = self.paid_amount or 0
        # 	for row in self.outstanding:

        # 		if remaining_paid <= 0:
        # 			break

        # 		if row.payable_amount and row.payable_amount > 0:
        # 			linked_si = frappe.db.get_value(
        # 				"Sales Invoice",
        # 				{"custom_rc_invoice_": row.invoice},
        # 				"name"
        # 			)

        # 			if linked_si:
        # 				allocate_amount = min(remaining_paid, row.payable_amount)

        # 				create_payment_entry(
        # 					self.customer,
        # 					linked_si,
        # 					allocate_amount,
        # 					self.name
        # 				)

        # 				remaining_paid -= allocate_amount

        # 	current_si_name = frappe.db.get_value(
        # 		"Sales Invoice",
        # 		{"custom_rc_invoice_": self.name, "docstatus":["!=",2]},
        # 		"name"
        # 	)

        # 	if not current_si_name:
        # 		current_si = create_sales_invoice(self)
        # 	else:
        # 		current_si = frappe.get_doc("Sales Invoice", current_si_name)
        # 	if current_si.grand_total > 0 and remaining_paid > 0:

        # 		create_payment_entry(
        # 			self.customer,
        # 			current_si.name,
        # 			remaining_paid,
        # 			self.name
        # 		)

    def on_cancel(self):
        if self.is_return == 0:
            current_si_name = frappe.db.get_value(
                "Sales Invoice",
                {"custom_rc_invoice_": self.name, "docstatus": ["!=", 2]},
                "name"
            )
            if current_si_name:
                pe_list = frappe.get_all(
                    "Payment Entry",
                    filters={"reference_name": current_si_name, "custom_rc_invoice": self.name, "docstatus": 1},
                    fields=["name"]
                )
                for pe in pe_list:
                    frappe.get_doc("Payment Entry", pe.name).cancel()
                frappe.get_doc("Sales Invoice", current_si_name).cancel()
            for row in self.outstanding:
                if row.invoice:
                    linked_si_name = frappe.db.get_value(
                        "Sales Invoice",
                        {"custom_rc_invoice_": row.invoice, "docstatus": ["!=", 2]},
                        "name"
                    )
                    if linked_si_name:
                        pe_list = frappe.get_all(
                            "Payment Entry",
                            filters={"reference_name": linked_si_name, "custom_rc_invoice": self.name, "docstatus": 1},
                            fields=["name"]
                        )
                        for pe in pe_list:
                            frappe.get_doc("Payment Entry", pe.name).cancel()


    def validate(self):
        if self.vat_amount == 0:
            self.total_amount = self.billable_amount

        if self.is_return:
            for row in self.return_items:
                if row.return_qty is None:
                    continue 
                original = frappe.get_doc("RS Invoice", self.return_from)

                original_item = next((i for i in original.invoice_items if i.item_code == row.item_code), None)
                if not original_item:
                    frappe.throw(f"Item {row.item_code} not found in original invoice {self.return_from}")

                original_balance = original_item.balance_available_qty 
                total_returned = 0
                previous_returns = frappe.get_all(
                    "RS Invoice",
                    filters={"return_from": original.name, "is_return": 1, "name": ["!=", self.name]},
                    fields=["name"]
                )
                for ret in previous_returns:
                    ret_doc = frappe.get_doc("RS Invoice", ret.name)
                    for ret_row in ret_doc.return_items:
                        if ret_row.item_code == row.item_code:
                            total_returned += ret_row.return_qty  

                remaining_qty = original_balance - total_returned
                if row.return_qty > remaining_qty:
                    frappe.throw(
                        f"Cannot return {row.return_qty} of {row.item_code}. Remaining allowed qty to return: {remaining_qty}"
                    )

        # if not self.customer_signature_:
        # 	frappe.throw("Customer Signature is mandatory. Please add signature.")



# @frappe.whitelist()
# def create_return_invoice(original_invoice_name):
#     original = frappe.get_doc("RC Invoice", original_invoice_name)
#     new_invoice = frappe.get_doc({
#         "doctype": "RC Invoice",
#         "customer": original.customer,
#         "return_from": original.name,
# 		"customer_warehouse":original.customer_warehouse,
# 		"dispatch_warehouse":original.dispatch_warehouse,
#         "is_return": 1, 
#         "return_items": []
#     })

#     for row in original.invoice_items:
#         new_invoice.append("return_items", {
#             "item_code": row.item_code,
#             "item_name": row.item_name,
#             "customer_qty": row.customer_qty,
#         })
#     new_invoice.insert()
#     return new_invoice.name



# @frappe.whitelist()
# def create_return_invoice(original_invoice_name):
# 	original = frappe.get_doc("RC Invoice", original_invoice_name)
# 	new_invoice = frappe.get_doc({
# 		"doctype": "RC Invoice",
# 		"customer": original.customer,
# 		"return_from": original.name,
# 		"customer_warehouse": original.customer_warehouse,
# 		"dispatch_warehouse": original.dispatch_warehouse,
# 		"is_return": 1, 
# 		"delivered_date":original.delivered_date,
# 		"return_items": []
# 	})

# 	for row in original.invoice_items:
# 		total_returned = 0
# 		return_invoices = frappe.get_all("RC Invoice",
# 										 filters={"return_from": original.name, "is_return": 1},
# 										 fields=["name"])
# 		for ret in return_invoices:
# 			ret_doc = frappe.get_doc("RC Invoice", ret.name)
# 			for ret_row in ret_doc.return_items:
# 				if ret_row.item_code == row.item_code:
# 					total_returned += ret_row.return_qty
        
# 		balance_qty = row.balance_available_qty - total_returned

# 		if balance_qty > 0:
# 			new_invoice.append("return_items", {
# 				"item_code": row.item_code,
# 				"item_name": row.item_name,
# 				"customer_qty": row.customer_qty 
# 			})

# 	if not new_invoice.return_items:
# 		frappe.throw("No items available for return.")

# 	new_invoice.insert()
# 	return new_invoice.name



# import frappe

# @frappe.whitelist()
# def get_transferred_items(customer, delivered_date, dispatch_warehouse, customer_warehouse):
# 	stock_entries = frappe.db.sql("""
# 		SELECT 
# 			ste.item_code,
# 			ste.item_name,
# 			SUM(ste.qty) AS qty,
# 			ste.uom
# 		FROM `tabStock Entry Detail` ste
# 		JOIN `tabStock Entry` se ON se.name = ste.parent
# 		WHERE se.stock_entry_type = 'Material Transfer'
# 		  AND ste.s_warehouse = %s
# 		  AND ste.t_warehouse = %s
# 		  AND DATE(se.posting_date) = %s
# 		  AND se.docstatus = 1
# 		GROUP BY ste.item_code, ste.item_name, ste.uom
# 	""", (dispatch_warehouse, customer_warehouse, delivered_date), as_dict=1)

# 	return stock_entries



import frappe

# @frappe.whitelist()
# def get_transferred_items(customer, customer_warehouse):
# 	stock_items = frappe.db.sql("""
# 		SELECT 
# 			bin.item_code,
# 			bin.warehouse,
# 			bin.actual_qty AS qty,
# 			item.item_name,
# 			item.stock_uom AS uom
# 		FROM `tabBin` bin
# 		JOIN `tabItem` item ON item.name = bin.item_code
# 		WHERE bin.warehouse = %s
# 		  AND bin.actual_qty > 0
# 		ORDER BY bin.item_code
# 	""", (customer_warehouse,), as_dict=1)

# 	return stock_items or []
@frappe.whitelist()
def transferred_items_with_qty(customer, customer_warehouse):

    stock_items = frappe.db.sql("""
        SELECT 
            bin.item_code,
            bin.warehouse,
            bin.actual_qty AS qty,
            item.item_name,
            item.stock_uom
        FROM `tabBin` bin
        JOIN `tabItem` item ON item.name = bin.item_code
        WHERE bin.warehouse = %s
          AND bin.actual_qty > 0
        ORDER BY bin.item_code
    """, (customer_warehouse,), as_dict=1)

    for item in stock_items:
        item_code = item.get("item_code")
        qty = item.get("qty", 0)
        uom = item.get("stock_uom")
        conversion_factor = 1
        retail_uom = frappe.get_all("UOM Conversion Detail",filters={"parent": item_code,"parenttype": "Item","custom_is_retail_uom": 1},fields=["uom", "conversion_factor"],limit=1)
        if retail_uom:
            uom = retail_uom[0].uom
            conversion_factor = retail_uom[0].conversion_factor or 1
        customer_qty = qty / conversion_factor if conversion_factor else qty
        item["customer_qty"] = int(customer_qty)
        item["uom"] = uom
        item["conversion_factor"] = conversion_factor

    return stock_items or []

@frappe.whitelist()
def get_transferred_items_with_qty(customer, customer_warehouse):
    # fetch stock items from warehouse
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

    # pack size mapping in grams
    pack_map = {
        "LL-SV-00002": 100,
        "LL-CH-00002": 80,
        "LL-CH-00033": 80,
        "LL-SV-00080": 100,
        "LL-SV-00114": 100,
        "LL-GI-00053":200
    }

    # uom mapping (optional)
    uom_map = {
        "LL-SV-00002": "100gm",
        "LL-CH-00002": "80gm",
        "LL-CH-00033": "80gm",
        "LL-SV-00080": "100gm",
        "LL-SV-00114": "100gm",
        "LL-GI-00053":"200gm"
    }
    # add customer_qty
    for item in stock_items:
        item_code = item.get("item_code")
        qty_kg = item.get("qty", 0)

        pack_size = pack_map.get(item_code, 0)
        total_grams = qty_kg * 1000  # remove *1000 if qty is already in grams
        customer_qty = int(total_grams // pack_size) if pack_size else qty_kg

        item["customer_qty"] = customer_qty
        item["uom"] = uom_map.get(item_code, item.get("uom"))

    return stock_items or []


@frappe.whitelist()
def get_latest_selling_price(item_code, uom, posting_date):

    price = frappe.db.sql("""
        SELECT price_list_rate
        FROM `tabItem Price`
        WHERE item_code = %s
          AND price_list = 'MRP'
          AND selling = 1
          AND uom = %s
          AND valid_from <= %s
        ORDER BY valid_from DESC
        LIMIT 1
    """, (item_code, uom, posting_date), as_dict=1)

    return price[0].price_list_rate if price else 0


@frappe.whitelist()
def create_sales_invoice_from_button(rc_invoice):
    doc = frappe.get_doc("RS Invoice", rc_invoice)
    
    existing = frappe.db.get_value(
        "Sales Invoice",
        {"custom_rc_invoice_": rc_invoice, "docstatus": ["!=", 2]},
        "name"
    )
    if existing:
        frappe.throw(f"Sales Invoice already exists : {existing}")

    si = create_sales_invoice(doc)
    
    return {"name": si.name, "message": f"Sales Invoice {si.name} Created & Submitted"}

@frappe.whitelist()
def create_sales_invoice(doc):
    if isinstance(doc, str):
        doc = frappe.get_doc("RS Invoice", doc)

    si = frappe.new_doc("Sales Invoice")
    si.customer = doc.customer
    si.posting_date = nowdate()
    si.custom_rc_invoice_ = doc.name  
    si.company = "TEAMPRO Food Products"
    si.services = "TFP" 
    si.account_manager = "dineshbabu.k@groupteampro.com"
    si.update_stock = 1
    si.set_warehouse = doc.customer_warehouse

    si.place_of_supply = "33-Tamil Nadu"
    si.taxes_and_charges = "Output GST In-state - TFP"

    valid_item_found = False
    total_tax = 0

    for item in doc.invoice_items:

        if not item.billable_qty or item.billable_qty <= 0:
            continue

        valid_item_found = True

        si.append("items", {
            "item_code": item.item_code,
            "qty": item.billable_qty,
            "rate": item.rate,
            "amount": item.amount,
            "uom":item.uom

        })

        gst_percent = item.gst or 0
        amount = item.amount or (item.billable_qty * item.rate)

        gst_value = (amount * gst_percent) / 100
        total_tax += gst_value

    if not valid_item_found:
        frappe.throw("Sales Invoice not created. No valid items.")

    cgst = total_tax / 2
    sgst = total_tax / 2

    si.set_taxes()
    si.taxes = []
    total_tax = doc.vat_amount or 0 

    si.insert(ignore_permissions=True)
    si.submit()

    return si


# @frappe.whitelist()
# def create_sales_invoice(doc):
# 	if isinstance(doc, str):
# 		doc = frappe.get_doc("RS Invoice", doc)

# 	si = frappe.new_doc("Sales Invoice")
# 	si.customer = doc.customer
# 	si.posting_date = nowdate()
# 	si.custom_rc_invoice_ = doc.name  
# 	si.company = "TEAMPRO Food Products"
# 	si.services = "TFP" 
# 	si.account_manager = "dineshbabu.k@groupteampro.com"
# 	si.update_stock = 1
# 	si.set_warehouse = doc.customer_warehouse
# 	si.taxes_and_charges = "Output GST Out-state - TFP"

# 	valid_item_found = False

# 	for item in doc.invoice_items:

# 		if not item.billable_qty or item.billable_qty <= 0:
# 			continue

# 		valid_item_found = True
# 		tax_template = None

# 		if item.gst == 5:
# 			tax_template = "GST 5% - TFP"

# 		elif item.gst == 18:
# 			tax_template = "GST 18% - TFP"

# 		si.append("items", {
# 			"item_code": item.item_code,
# 			"qty": item.billable_qty,
# 			"rate": item.rate,
# 			"item_tax_template": tax_template  ,
# 			"amount": item.amount,
# 		})

# 	if not valid_item_found:
# 		frappe.throw("Sales Invoice not created. No valid items.")
# 	si.set_taxes()
# 	si.calculate_taxes_and_totals()
# 	si.insert(ignore_permissions=True)
# 	# si.submit()  

# 	return si

# @frappe.whitelist()
# def create_sales_invoice(doc):

#     si = frappe.new_doc("Sales Invoice")
#     si.customer = doc.customer
#     si.posting_date = nowdate()
#     si.custom_rc_invoice_ = doc.name  
#     si.company = "TEAMPRO Food Products"
#     si.services = "TFP" 
#     si.account_manager = "dineshbabu.k@groupteampro.com"
#     si.update_stock = 1
#     si.set_warehouse = doc.customer_warehouse

#     skipped_items = []
#     valid_item_found = False

#     gst_rates = set()   # ✅ store unique GST %

#     for item in doc.invoice_items:

#         # Skip if billable qty is 0
#         if not item.billable_qty or item.billable_qty <= 0:
#             skipped_items.append(item.item_code)
#             continue

#         valid_item_found = True

#         si.append("items", {
#             "item_code": item.item_code,
#             "qty": item.billable_qty,
#             "rate": item.rate
#         })

#         # ✅ collect GST %
#         if item.gst:   # assuming field name is gst
#             gst_rates.add(item.gst)

#     if not valid_item_found:
#         frappe.throw("Sales Invoice not created.")

#     # ✅ Add GST dynamically
#     for gst in gst_rates:

#         if gst == 5:
#             si.append("taxes", {
#                 "charge_type": "Actual",
#                 "account_head": "GST 5% - TFP",
#                 "rate": 5,
#                 "description": "GST 5%"
#             })

#         elif gst == 18:
#             si.append("taxes", {
#                 "charge_type": "Actual",
#                 "account_head": "GST 18% - TFP",
#                 "rate": 18,
#                 "description": "GST 18%"
#             })

#     si.insert(ignore_permissions=True)
#     # si.submit()
#     return si


@frappe.whitelist()
def cancel_sales_invoice(rc_invoice):

    si_name = frappe.db.get_value(
        "Sales Invoice",
        {"custom_rc_invoice_": rc_invoice, "docstatus": 1},
        "name"
    )

    if not si_name:
        frappe.throw("No Submitted Sales Invoice Found")

    si = frappe.get_doc("Sales Invoice", si_name)
    si.cancel()

    return "Cancelled"





# from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

# def create_payment_entry(customer, references, rc_invoice):

# 	first_invoice = references[0]["reference_name"]

# 	pe = get_payment_entry("Sales Invoice", first_invoice)

# 	pe.custom_rc_invoice = rc_invoice
# 	pe.references = []

# 	total_amount = 0

# 	for ref in references:

# 		si = frappe.get_doc("Sales Invoice", ref["reference_name"])
# 		si.reload()

# 		if si.outstanding_amount <= 0:
# 			continue

# 		allocate_amount = ref["allocated_amount"]

# 		pe.append("references", {
# 			"reference_doctype": "Sales Invoice",
# 			"reference_name": ref["reference_name"],
# 			"allocated_amount": allocate_amount
# 		})

# 		total_amount += allocate_amount

# 	pe.paid_amount = total_amount
# 	pe.received_amount = total_amount

# 	pe.insert(ignore_permissions=True)
# 	pe.submit()


from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

def create_payment_entry(customer, references, rc_invoice, paid_amount):

    first_invoice = references[0]["reference_name"]

    pe = get_payment_entry("Sales Invoice", first_invoice)

    pe.custom_rc_invoice = rc_invoice
    pe.references = []
    mode_of_payment =frappe.db.get_value("RS Invoice", rc_invoice, "mode_of_payment")
    bank_account = frappe.db.get_value("RS Invoice", rc_invoice, "bank")
    if mode_of_payment:
        pe.mode_of_payment = mode_of_payment
    if bank_account:
        pe.bank_account = bank_account
    total_amount = 0

    for ref in references:

        si = frappe.get_doc("Sales Invoice", ref["reference_name"])
        si.reload()

        if si.outstanding_amount <= 0:
            continue

        allocate_amount = ref["allocated_amount"]

        pe.append("references", {
            "reference_doctype": "Sales Invoice",
            "reference_name": ref["reference_name"],
            "allocated_amount": allocate_amount
        })

        total_amount += allocate_amount


    pe.paid_amount = paid_amount
    pe.received_amount = paid_amount

    pe.insert(ignore_permissions=True)
    pe.submit()

@frappe.whitelist()
def get_customer_pending_invoices(customer):

    invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "customer": customer,
            "docstatus": 1,
            "outstanding_amount": [">", 0]
        },
        fields=["custom_rc_invoice_", "outstanding_amount"]
    )

    result = []

    for inv in invoices:

        if not inv.custom_rc_invoice_:
            continue

        result.append({
            "invoice": inv.custom_rc_invoice_,  
            "outstanding_amount": inv.outstanding_amount
        })

    return result


@frappe.whitelist()
def process_invoice(docname):
    doc = frappe.get_doc("RS Invoice", docname)

    remaining_paid = doc.paid_amount or 0

    current_si_name = frappe.db.get_value(
        "Sales Invoice",
        {"custom_rc_invoice_": doc.name, "docstatus": ["!=", 2]},
        "name"
    )

    if not current_si_name:
        create_sales_invoice(doc)

    return "Invoice Created"



@frappe.whitelist()
def check_sales_invoice(rc_invoice):

    si = frappe.db.get_value(
        "Sales Invoice",
        {"custom_rc_invoice_": rc_invoice, "docstatus": ["!=", 2]},
        "name"
    )

    return si


@frappe.whitelist()
def calculate_customer_qty(item_code, qty):

    # Map of pack sizes in grams
    pack_size_map = {
        "LL-SV-00002": 100,
        "LL-CH-00002": 80,
        "LL-CH-00033": 80,
        "LL-SV-00080": 100,
        "LL-SV-00114": 100
    }

    pack_size = pack_size_map.get(item_code, 0)

    if pack_size > 0:
        # Convert qty to grams if it's in kg
        total_grams = qty * 1000  # remove *1000 if qty is already in grams
        packets = total_grams // pack_size  # integer division
    else:
        packets = qty  # fallback to original qty

    return int(packets)



