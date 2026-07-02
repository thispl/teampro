

import frappe

@frappe.whitelist()
def update_payment_schedule_due_date(doc, method):
    has_sales_order = any(item.sales_order for item in doc.items)

    if has_sales_order:
        for row in doc.payment_schedule:
            if row.due_date != doc.due_date:
                row.due_date = doc.due_date