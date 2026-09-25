import frappe

def verify():
    si_name = "TFP/1886"
    
    print("=" * 60)
    print("FINAL VERIFICATION FOR Sales Invoice TFP/1886")
    print("=" * 60)
    
    # 1. Invoice status
    print("\n--- 1. Sales Invoice Status ---")
    si = frappe.db.sql("""
        SELECT name, docstatus, status, workflow_state, is_pos,
               grand_total, paid_amount, outstanding_amount,
               customer, posting_date, company
        FROM `tabSales Invoice` WHERE name=%s
    """, (si_name,), as_dict=True)
    for s in si:
        print(f"  docstatus: {s['docstatus']} (1=Submitted)")
        print(f"  status: {s['status']}")
        print(f"  workflow_state: {s['workflow_state']}")
        print(f"  is_pos: {s['is_pos']}")
        print(f"  grand_total: {s['grand_total']}")
        print(f"  paid_amount: {s['paid_amount']}")
        print(f"  outstanding_amount: {s['outstanding_amount']}")
        print(f"  customer: {s['customer']}")
        print(f"  posting_date: {s['posting_date']}")
    
    # 2. POS Payment
    print("\n--- 2. POS Payment ---")
    pos = frappe.db.sql("""
        SELECT name, docstatus, mode_of_payment, amount, account
        FROM `tabSales Invoice Payment` WHERE parent=%s
    """, (si_name,), as_dict=True)
    for p in pos:
        print(f"  docstatus: {p['docstatus']}, mode: {p['mode_of_payment']}, amount: {p['amount']}, account: {p['account']}")
    
    # 3. GL Entries
    print("\n--- 3. GL Entries ---")
    gles = frappe.db.sql("""
        SELECT name, account, debit, credit, is_cancelled
        FROM `tabGL Entry`
        WHERE voucher_no=%s AND voucher_type='Sales Invoice'
        ORDER BY name
    """, (si_name,), as_dict=True)
    total_dr = 0
    total_cr = 0
    for g in gles:
        print(f"  {g['name']} | {g['account']} | Dr={g['debit']} Cr={g['credit']} | cancelled={g['is_cancelled']}")
        total_dr += float(g['debit'] or 0)
        total_cr += float(g['credit'] or 0)
    print(f"  Total: Dr={total_dr}, Cr={total_cr}, Balanced={total_dr == total_cr}")
    print(f"  Total GL entries: {len(gles)} (should be 6, all is_cancelled=0)")
    
    # 4. Stock Ledger Entries
    print("\n--- 4. Stock Ledger Entries ---")
    sle_active = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s AND is_cancelled=0
    """, (si_name,))[0][0]
    sle_cancelled = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s AND is_cancelled=1
    """, (si_name,))[0][0]
    print(f"  Active SLEs: {sle_active} (should be 99)")
    print(f"  Cancelled SLEs: {sle_cancelled} (should be 0)")
    
    # 5. Check no reversal entries remain
    print("\n--- 5. Reversal Entries Check ---")
    rev_gle = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabGL Entry`
        WHERE voucher_no=%s AND voucher_type='Sales Invoice' AND DATE(creation)='2026-08-21'
    """, (si_name,))[0][0]
    rev_sle = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s AND DATE(creation)='2026-08-21'
    """, (si_name,))[0][0]
    print(f"  Reversal GL entries (2026-08-21): {rev_gle} (should be 0)")
    print(f"  Reversal SLEs (2026-08-21): {rev_sle} (should be 0)")
    
    # 6. Bin balances for affected items
    print("\n--- 6. Bin Balances (sample) ---")
    bins = frappe.db.sql("""
        SELECT b.item_code, b.warehouse, b.actual_qty, b.stock_value, b.valuation_rate
        FROM `tabBin` b
        INNER JOIN (
            SELECT DISTINCT item_code FROM `tabStock Ledger Entry`
            WHERE voucher_no=%s AND is_cancelled=0
        ) s ON b.item_code = s.item_code
        WHERE b.warehouse = 'Stores - TFP'
        ORDER BY b.item_code
    """, (si_name,), as_dict=True)
    for b in bins[:5]:
        print(f"  {b['item_code']}: qty={b['actual_qty']}, value={b['stock_value']}, rate={b['valuation_rate']}")
    print(f"  ... total {len(bins)} bins updated")
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
