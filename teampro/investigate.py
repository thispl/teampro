import frappe

def investigate():
    si_name = "TFP/1886"

    # Full invoice details
    print("=== FULL INVOICE DETAILS ===")
    si = frappe.db.sql("""
        SELECT name, docstatus, status, workflow_state, is_pos, is_return,
               grand_total, paid_amount, outstanding_amount, base_grand_total,
               customer, customer_name, posting_date, company, update_stock,
               set_warehouse, total_taxes_and_charges
        FROM `tabSales Invoice` WHERE name=%s
    """, (si_name,), as_dict=True)
    for s in si:
        print(f"  {s}")

    # Count original vs reversal GL entries by date
    print("\n=== GL ENTRY COUNTS ===")
    orig_gle = frappe.db.sql("""
        SELECT COUNT(*) as cnt FROM `tabGL Entry`
        WHERE voucher_no=%s AND voucher_type='Sales Invoice' AND DATE(creation)='2026-08-15'
    """, (si_name,))[0][0]
    print(f"  Original GL entries (2026-08-15): {orig_gle}")

    rev_gle = frappe.db.sql("""
        SELECT COUNT(*) as cnt FROM `tabGL Entry`
        WHERE voucher_no=%s AND voucher_type='Sales Invoice' AND DATE(creation)='2026-08-21'
    """, (si_name,))[0][0]
    print(f"  Reversal GL entries (2026-08-21): {rev_gle}")

    # Count original vs reversal SLEs by date
    print("\n=== SLE COUNTS ===")
    orig_sle = frappe.db.sql("""
        SELECT COUNT(*) as cnt FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s AND DATE(creation)='2026-08-15'
    """, (si_name,))[0][0]
    print(f"  Original SLEs (2026-08-15): {orig_sle}")

    rev_sle = frappe.db.sql("""
        SELECT COUNT(*) as cnt FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s AND DATE(creation)='2026-08-21'
    """, (si_name,))[0][0]
    print(f"  Reversal SLEs (2026-08-21): {rev_sle}")

    # Check if there's a Payment Entry with reference to this invoice
    print("\n=== PAYMENT ENTRY REFERENCE CHECK ===")
    pe_refs = frappe.db.sql("""
        SELECT per.parent, per.reference_name, per.allocated_amount
        FROM `tabPayment Entry Reference` per
        WHERE per.reference_name=%s
    """, (si_name,), as_dict=True)
    print(f"  Payment Entry References: {pe_refs}")

    # Check the items in the invoice
    print("\n=== INVOICE ITEMS COUNT ===")
    items_cnt = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabSales Invoice Item` WHERE parent=%s
    """, (si_name,))[0][0]
    print(f"  Items: {items_cnt}")

    # Check Serial No entries
    print("\n=== SERIAL NO ENTRIES ===")
    sns_cnt = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabSerial No` WHERE sales_invoice=%s
    """, (si_name,))[0][0]
    print(f"  Serial nos linked: {sns_cnt}")
