import frappe

def check_pos_payment():
    si_name = "TFP/1886"
    
    # Check Sales Invoice Payment (POS payments child table)
    print("=== POS PAYMENT ENTRIES ===")
    pos_payments = frappe.db.sql("""
        SELECT * FROM `tabSales Invoice Payment` WHERE parent=%s
    """, (si_name,), as_dict=True)
    for p in pos_payments:
        print(f"  {p}")
    
    # Check the original GL entry names (for restoration)
    print("\n=== ORIGINAL GL ENTRY NAMES (2026-08-15) ===")
    orig_gles = frappe.db.sql("""
        SELECT name, account, debit, credit, is_cancelled
        FROM `tabGL Entry`
        WHERE voucher_no=%s AND voucher_type='Sales Invoice' AND DATE(creation)='2026-08-15'
        ORDER BY name
    """, (si_name,), as_dict=True)
    for g in orig_gles:
        print(f"  {g['name']} | {g['account']} | Dr={g['debit']} Cr={g['credit']} | cancelled={g['is_cancelled']}")
    
    print("\n=== REVERSAL GL ENTRY NAMES (2026-08-21) ===")
    rev_gles = frappe.db.sql("""
        SELECT name, account, debit, credit, is_cancelled
        FROM `tabGL Entry`
        WHERE voucher_no=%s AND voucher_type='Sales Invoice' AND DATE(creation)='2026-08-21'
        ORDER BY name
    """, (si_name,), as_dict=True)
    for g in rev_gles:
        print(f"  {g['name']} | {g['account']} | Dr={g['debit']} Cr={g['credit']} | cancelled={g['is_cancelled']}")

    # Check distinct items/warehouses in SLEs for bin recalculation
    print("\n=== DISTINCT ITEMS IN SLEs ===")
    items = frappe.db.sql("""
        SELECT DISTINCT item_code, warehouse 
        FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s AND DATE(creation)='2026-08-15'
    """, (si_name,), as_dict=True)
    print(f"  Distinct item/warehouse combos: {len(items)}")
    for i in items[:5]:
        print(f"  {i}")
    if len(items) > 5:
        print(f"  ... and {len(items)-5} more")
