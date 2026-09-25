import frappe
import json
import sys

site = sys.argv[1] if len(sys.argv) > 1 else "erp.teamproit.com"
so_name = sys.argv[2] if len(sys.argv) > 2 else "SO2601338-1"

frappe.init(site=site, sites_path="/home/frappe/teampro-bench/sites")
frappe.connect()

try:
    # First try to find by name
    so = None
    try:
        so = frappe.get_doc("Sales Order", so_name)
    except frappe.DoesNotExistError:
        # Try a name search
        names = frappe.db.sql_list(
            "select name from `tabSales Order` where name like %s order by name desc limit 20",
            ("%" + so_name + "%",),
        )
        print(json.dumps({"site": site, "search": so_name, "matches": names}, indent=2))
        if names:
            so = frappe.get_doc("Sales Order", names[0])

    if so:
        # Inspect custom fields on the SO itself
        so_meta = frappe.get_meta("Sales Order")
        custom_fields = [f.fieldname for f in so_meta.fields if f.fieldname and ("bag" in f.fieldname.lower() or "box" in f.fieldname.lower() or "bb" in f.fieldname.lower())]

        # Inspect child item fields
        item_meta = frappe.get_meta("Sales Order Item")
        item_custom_fields = [f.fieldname for f in item_meta.fields if f.fieldname and ("bag" in f.fieldname.lower() or "box" in f.fieldname.lower() or "bb" in f.fieldname.lower())]

        out = {
            "site": site,
            "name": so.name,
            "status": so.status,
            "docstatus": so.docstatus,
            "customer": so.customer,
            "transaction_date": str(so.transaction_date),
            "so_custom_bag_box_fields": custom_fields,
            "so_item_custom_bag_box_fields": item_custom_fields,
            "so_custom_values": {f: so.get(f) for f in custom_fields},
            "items": [],
        }
        for i in so.items:
            out["items"].append({
                "item_code": i.item_code,
                "item_name": i.item_name,
                "qty": float(i.qty),
                "uom": i.uom,
                "warehouse": i.warehouse,
                "rate": float(i.rate),
                "amount": float(i.amount),
                "custom_values": {f: i.get(f) for f in item_custom_fields},
            })
        print(json.dumps(out, indent=2, default=str))
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error: {e}")
finally:
    frappe.destroy()
