import frappe
import json


def check_so(so_name="SO2601338-1"):
    names = frappe.db.sql_list(
        "select name from `tabSales Order` where name like %s order by name desc limit 30",
        ("%" + so_name + "%",),
    )
    print("MATCHES:", json.dumps(names))
    if not names:
        return
    so = frappe.get_doc("Sales Order", names[0])
    item_meta = frappe.get_meta("Sales Order Item")
    bag_box_fields = [
        f.fieldname for f in item_meta.fields
        if f.fieldname and any(
            k in f.fieldname.lower()
            for k in ["bag", "box", "cover", "per_2p", "per_3p", "last_", "wrd", "mfg", "packing", "tertiary", "print_", "remarks"]
        )
    ]
    out = {"name": so.name, "customer": so.customer, "items": []}
    for i in so.items:
        out["items"].append({
            "item_code": i.item_code,
            "item_name": i.item_name,
            "qty": float(i.qty),
            "uom": i.uom,
            "custom_values": {f: i.get(f) for f in bag_box_fields},
        })
    print(json.dumps(out, indent=2, default=str))
