import frappe
from erpnext.stock.stock_ledger import update_entries_after

def fix_negative_stock_item():
    """Repost the one item that failed due to negative stock validation."""
    si_name = "TFP/1886"
    posting_date = "2026-08-15"
    posting_time = "16:05:44"
    
    item_code = "LL-BK-00031"
    warehouse = "Stores - TFP"
    
    # Check current bin state before repost
    bin_before = frappe.db.sql("""
        SELECT item_code, warehouse, actual_qty, stock_value, valuation_rate
        FROM `tabBin` WHERE item_code=%s AND warehouse=%s
    """, (item_code, warehouse), as_dict=True)
    print(f"Bin BEFORE repost: {bin_before}")
    
    # Check SLEs for this item from this invoice
    sle_count = frappe.db.sql("""
        SELECT COUNT(*) FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s AND item_code=%s AND is_cancelled=0
    """, (si_name, item_code))[0][0]
    print(f"Active SLEs for {item_code} from this invoice: {sle_count}")
    
    # Repost with allow_negative_stock=True
    try:
        args = {
            "item_code": item_code,
            "warehouse": warehouse,
            "posting_date": posting_date,
            "posting_time": posting_time,
        }
        update_entries_after(args, allow_negative_stock=True)
        print(f"Reposted {item_code} with negative stock allowed")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    frappe.db.commit()
    
    # Check bin state after repost
    bin_after = frappe.db.sql("""
        SELECT item_code, warehouse, actual_qty, stock_value, valuation_rate
        FROM `tabBin` WHERE item_code=%s AND warehouse=%s
    """, (item_code, warehouse), as_dict=True)
    print(f"Bin AFTER repost: {bin_after}")
