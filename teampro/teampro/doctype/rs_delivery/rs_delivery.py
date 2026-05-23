# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.stock.utils import get_stock_balance
from frappe.utils import nowdate
from frappe.utils import flt


import frappe
from frappe.model.document import Document

class RSDelivery(Document):
    def before_submit(self):
        if not self.next_delivery_date:
            frappe.throw("Next Delivery Date is mandatory before submitting the document.")
    def validate(self):
        if self.customer:
            rc = frappe.db.get_value(
                "Shop RC",
                {"customer_name": self.customer},
                ["contact_person_number", "postal_code"],
                as_dict=True
            )

            if rc:
                if not self.custom_contact_number:
                    self.custom_contact_number = rc.contact_person_number or ""

                if not self.custom_pin_code_:
                    self.custom_pin_code_ = rc.postal_code or ""

        total_billable = 0
        vat_amount = 0
        for row in self.items:

            qty = row.qty or 0

            mrp = get_latest_selling_price(row.item_code, row.uom, self.delivered_date)
            row.mrp = mrp

            rc = frappe.db.get_value(
                "Shop RC",
                {"customer_name": self.customer},
                ["margin_percentage", "has_gst"],
                as_dict=True
            )

            margin = (rc.margin_percentage or 0) if rc else 0
            if row.item_code == "LL-GI-00053":
                margin = 20
            gst_flag = (rc.has_gst or 0) if rc else 0

            row.margin_percentage = margin

            discount = mrp * (margin / 100)
            total_rate = mrp - discount

            row.rate = total_rate
            row.amount = float(qty) * total_rate

            if gst_flag:

                gst_rate = frappe.db.get_value(
                    "Item",
                    row.item_code,
                    "custom_gst_rate"
                ) or 0

                gst_value = gst_rate / 100
                gst_amt = mrp * gst_value

                mrp_wo_gst = mrp - gst_amt

                discount = mrp_wo_gst * (margin / 100)
                rate_wo_gst = mrp_wo_gst - discount

                amount_wo_gst = float(qty) * rate_wo_gst

                row.gst = gst_amt
                row.rate_without_gst = rate_wo_gst
                row.amount_without_gst = amount_wo_gst
                row.mrp_without_gst = mrp_wo_gst

                total_billable += amount_wo_gst
                vat_amount += (row.amount - amount_wo_gst)

            else:
                total_billable += row.amount
        self.billable_amount = total_billable
        self.vat_amount = vat_amount
        self.total_amount = total_billable + vat_amount


        if not self.dispatch_warehouse:
            frappe.throw("Please select Dispatch Warehouse")

        if self.customer:
            retail_id = frappe.db.get_value(
                "Customer",
                self.customer,
                "custom_retail_customer"
            )

            if retail_id:
                warehouse = frappe.db.get_value(
                    "Warehouse",
                    {"custom_retail_customer": retail_id},
                    "name"
                )

                if warehouse:
                    self.customer_warehouse = warehouse
                else:
                    self.customer_warehouse = ""
                    frappe.msgprint("Warehouse not found for this Retail Customer")
            else:
                self.customer_warehouse = ""

        for row in self.items:

            if not row.item_code:
                continue
            conversion_factor = get_conversion_factor(row.item_code, row.uom)
            available_qty = get_stock_balance(
                row.item_code,
                self.dispatch_warehouse
            )
            required_qty = round((flt(row.qty)*conversion_factor),2)


            if available_qty < required_qty:
                frappe.throw(
                    f"""
                    Insufficient Stock for Item: {row.item_code}<br>
                    Warehouse: {self.dispatch_warehouse}<br>
                    Available Qty: {available_qty}<br>
                    Required Qty: {row.qty}
                    """
                )
        

    

    def on_submit(self):
        if not self.shop_owner_signature:
            frappe.throw("Shop Owner Signature is mandatory. Please add signature.")

        stock_available = True

        for row in self.items:
            available_qty = get_stock_balance(
                row.item_code,
                self.dispatch_warehouse
            )
            conversion_factor = get_conversion_factor(row.item_code, row.uom)
            required_qty = round((flt(row.qty)*conversion_factor),2)

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
                "custom_internal_transfer_type" : "Retail",
                "to_warehouse":self.customer_warehouse,
                "from_warehouse":self.dispatch_warehouse,
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
            se.submit()
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
@frappe.whitelist()
def get_conversion_factor(item_code, uom):
        cf = frappe.db.get_value(
            "UOM Conversion Detail",
            {"parent": item_code, "uom": uom},
            "conversion_factor"
        )
        return flt(cf) if cf else 1  

import frappe

# @frappe.whitelist()
# def get_retail_items():

#     source_wh = "Stores - TFP"
#     target_wh = "WH-Vehicle-001 - TFP"

#     items = frappe.get_all(
#         "Item",
#         filters={"custom_is_retail_item": 1},
#         fields=["name", "item_name", "stock_uom"]
#     )

#     # uom_map = {
#     #     "LL-SV-00002": ("100gm", 0.1),
#     #     "LL-CH-00002": ("80gm", 0.08),
#     #     "LL-CH-00033": ("80gm", 0.08),
#     #     "LL-SV-00080": ("100gm", 0.1),
#     #     "LL-SV-00114": ("100gm", 0.1),
#     # 	"LL-GI-00053": ("200gm", 0.2)
#     # }

#     data = []

#     for item in items:
#         uom = item.stock_uom
#         cf = 1
#         retail_uoms = frappe.get_all(
#             "UOM Conversion Detail",
#             filters={
#                 "parent": item.name,
#                 "parenttype": "Item",
#                 "custom_is_retail_uom": 1
#             },
#             fields=["uom", "conversion_factor"]
#         )

#         mrp = frappe.db.get_value(
#             "Item Price",
#             {"item_code": item.name, "price_list": "MRP"},
#             "price_list_rate"
#         )

#         if retail_uoms:
#             for u in retail_uoms:
#                 data.append({
#                     "item_code": item.name,
#                     "item_name": item.item_name,
#                     "qty": 1,
#                     "uom": u.uom,
#                     "stock_uom": item.stock_uom,
#                     "conversion_factor": u.conversion_factor,
#                     "s_warehouse": source_wh,
#                     "t_warehouse": target_wh,
#                     "custom_mrp_r": mrp or 0,
#                     "custom_tfp": 1,
#                     "custom_name_print": "Yes",
#                     "custom_wrd_item_name": item.item_name
#                 })

#         else:
#             # fallback if no retail UOM
#             data.append({
#                 "item_code": item.name,
#                 "item_name": item.item_name,
#                 "qty": 1,
#                 "uom": item.stock_uom,
#                 "stock_uom": item.stock_uom,
#                 "conversion_factor": 1,
#                 "s_warehouse": source_wh,
#                 "t_warehouse": target_wh,
#                 "custom_mrp_r": mrp or 0,
#                 "custom_tfp": 1,
#                 "custom_name_print": "Yes",
#                 "custom_wrd_item_name": item.item_name
#             })

#     return data



@frappe.whitelist()
def get_retail_items():

    source_wh = "Stores - TFP"
    target_wh = "WH-Vehicle-001 - TFP"

    # Get all retail items
    items = frappe.get_all(
        "Item",
        filters={"custom_is_retail_item": 1},
        fields=["name", "item_name", "stock_uom"]
    )

    price_list = frappe.get_all(
        "Item Price",
        filters={"price_list": "MRP"},
        fields=["item_code", "price_list_rate"]
    )
    price_map = {p.item_code: p.price_list_rate for p in price_list}

    data = []

    for item in items:

        retail_uoms = frappe.get_all(
            "UOM Conversion Detail",
            filters={
                "parent": item.name,
                "parenttype": "Item",
                "custom_is_retail_uom": 1
            },
            fields=["uom", "conversion_factor"]
        )

        mrp = price_map.get(item.name, 0)
        if retail_uoms:
            for u in retail_uoms:
                data.append({
                    "item_code": item.name,
                    "item_name": item.item_name,
                    "qty": 1,
                    "uom": u.uom,
                    "stock_uom": item.stock_uom,
                    "conversion_factor": u.conversion_factor,
                    "s_warehouse": source_wh,
                    "t_warehouse": target_wh,
                    "custom_mrp_r": mrp,
                    "custom_tfp": 1,
                    "custom_name_print": "Yes",
                    "custom_wrd_item_name": item.item_name
                })

        else:
            data.append({
                "item_code": item.name,
                "item_name": item.item_name,
                "qty": 1,
                "uom": item.stock_uom,
                "stock_uom": item.stock_uom,
                "conversion_factor": 1,
                "s_warehouse": source_wh,
                "t_warehouse": target_wh,
                "custom_mrp_r": mrp,
                "custom_tfp": 1,
                "custom_name_print": "Yes",
                "custom_wrd_item_name": item.item_name
            })

    return data


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