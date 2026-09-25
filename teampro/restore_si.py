import frappe
from erpnext.stock.stock_ledger import update_entries_after

def restore():
    si_name = "TFP/1886"
    posting_date = "2026-08-15"
    posting_time = "16:05:44"
    
    try:
        # === Step 1: Restore Sales Invoice ===
        print("=== Step 1: Restoring Sales Invoice ===")
        frappe.db.sql("""
            UPDATE `tabSales Invoice`
            SET docstatus = 1, status = 'Paid', workflow_state = 'Submitted'
            WHERE name = %s
        """, (si_name,))
        print(f"  Set docstatus=1, status=Paid, workflow_state=Submitted")
        
        # === Step 2: Restore POS Payment child table ===
        print("\n=== Step 2: Restoring POS Payment child ===")
        frappe.db.sql("""
            UPDATE `tabSales Invoice Payment`
            SET docstatus = 1
            WHERE parent = %s
        """, (si_name,))
        print(f"  Set POS Payment docstatus=1")
        
        # === Step 3: Un-cancel original GL entries, delete reversal GL entries ===
        print("\n=== Step 3: Restoring GL entries ===")
        # Un-cancel original GL entries (created on 2026-08-15)
        orig_gle_count = frappe.db.sql("""
            UPDATE `tabGL Entry`
            SET is_cancelled = 0
            WHERE voucher_no = %s AND voucher_type = 'Sales Invoice' AND DATE(creation) = '2026-08-15'
        """, (si_name,))
        print(f"  Un-cancelled original GL entries")
        
        # Delete reversal GL entries (created on 2026-08-21)
        frappe.db.sql("""
            DELETE FROM `tabGL Entry`
            WHERE voucher_no = %s AND voucher_type = 'Sales Invoice' AND DATE(creation) = '2026-08-21'
        """, (si_name,))
        print(f"  Deleted reversal GL entries")
        
        # === Step 4: Un-cancel original SLEs, delete reversal SLEs ===
        print("\n=== Step 4: Restoring Stock Ledger Entries ===")
        # Un-cancel original SLEs (created on 2026-08-15)
        frappe.db.sql("""
            UPDATE `tabStock Ledger Entry`
            SET is_cancelled = 0
            WHERE voucher_no = %s AND DATE(creation) = '2026-08-15'
        """, (si_name,))
        print(f"  Un-cancelled original SLEs")
        
        # Delete reversal SLEs (created on 2026-08-21)
        frappe.db.sql("""
            DELETE FROM `tabStock Ledger Entry`
            WHERE voucher_no = %s AND DATE(creation) = '2026-08-21'
        """, (si_name,))
        print(f"  Deleted reversal SLEs")
        
        # Commit DB changes
        frappe.db.commit()
        print("\n=== DB changes committed ===")
        
        # === Step 5: Recalculate bin balances ===
        print("\n=== Step 5: Recalculating bin balances ===")
        items = frappe.db.sql("""
            SELECT DISTINCT item_code, warehouse FROM `tabStock Ledger Entry`
            WHERE voucher_no = %s AND is_cancelled = 0
        """, (si_name,), as_dict=True)
        
        print(f"  Found {len(items)} item/warehouse combinations to repost")
        
        for item in items:
            try:
                args = {
                    "item_code": item["item_code"],
                    "warehouse": item["warehouse"],
                    "posting_date": posting_date,
                    "posting_time": posting_time,
                }
                update_entries_after(args)
                print(f"  Reposted: {item['item_code']} @ {item['warehouse']}")
            except Exception as e:
                print(f"  ERROR reposting {item['item_code']} @ {item['warehouse']}: {e}")
        
        frappe.db.commit()
        print("\n=== Bin recalculation complete ===")
        
        # === Verification ===
        print("\n=== VERIFICATION ===")
        si = frappe.db.sql("""
            SELECT name, docstatus, status, workflow_state, paid_amount, outstanding_amount
            FROM `tabSales Invoice` WHERE name=%s
        """, (si_name,), as_dict=True)
        print(f"  Invoice: {si}")
        
        gle_count = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabGL Entry`
            WHERE voucher_no=%s AND voucher_type='Sales Invoice' AND is_cancelled=0
        """, (si_name,))[0][0]
        print(f"  Active GL entries: {gle_count}")
        
        sle_count = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabStock Ledger Entry`
            WHERE voucher_no=%s AND is_cancelled=0
        """, (si_name,))[0][0]
        print(f"  Active SLE entries: {sle_count}")
        
        print("\n=== RESTORATION COMPLETE ===")
        
    except Exception as e:
        frappe.db.rollback()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise
