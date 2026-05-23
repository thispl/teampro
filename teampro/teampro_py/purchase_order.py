import frappe
@frappe.whitelist()
def check_supplier(supplier):
    supp=frappe.get_doc("Supplier",supplier)
    if supp.custom_is_lead == 1:
        return "OK"


@frappe.whitelist()
def calc_cost_prize_po(docname):
    doc = frappe.get_doc("Purchase Order", docname)  # change doctype if needed
    warnings = []
    for f in doc.items:
        tfp_item = frappe.db.get_value("Item", f.item_code, "tfp")
        if tfp_item == 1:
            price = frappe.db.get_value("Item Price", {
                "price_list": "Cost Price TFP",
                "item_code": f.item_code
            }, "price_list_rate")
            if price:
                item_price = price / 1000 if f.uom == "Gram" else price
                item_rate = round(item_price, 2)
                if f.rate > item_rate:
                    warnings.append(f"{f.item_name}")

    return {"warnings": warnings}


@frappe.whitelist()
def update_po_st(doctype,docname):
    frappe.log_error(title="PO",message=docname)
    frappe.db.sql("""
    UPDATE `tabPurchase Order`
    SET docstatus = 0 , workflow_state = 'Pending for CEO'
    WHERE name = %s
""", (docname))