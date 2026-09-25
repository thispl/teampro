import frappe
import json
from datetime import datetime

def backup():
    si_name = "TFP/1886"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    backup_data = {}
    
    # 1. Sales Invoice
    si = frappe.db.sql("""
        SELECT * FROM `tabSales Invoice` WHERE name=%s
    """, (si_name,), as_dict=True)
    backup_data['sales_invoice'] = si
    
    # 2. Sales Invoice Payment (POS child)
    sip = frappe.db.sql("""
        SELECT * FROM `tabSales Invoice Payment` WHERE parent=%s
    """, (si_name,), as_dict=True)
    backup_data['sales_invoice_payment'] = sip
    
    # 3. GL Entries
    gle = frappe.db.sql("""
        SELECT * FROM `tabGL Entry` WHERE voucher_no=%s AND voucher_type='Sales Invoice'
    """, (si_name,), as_dict=True)
    backup_data['gl_entries'] = gle
    
    # 4. Stock Ledger Entries
    sle = frappe.db.sql("""
        SELECT * FROM `tabStock Ledger Entry` WHERE voucher_no=%s
    """, (si_name,), as_dict=True)
    backup_data['stock_ledger_entries'] = sle
    
    # 5. Bin entries for affected items
    items = frappe.db.sql("""
        SELECT DISTINCT item_code, warehouse FROM `tabStock Ledger Entry`
        WHERE voucher_no=%s
    """, (si_name,), as_dict=True)
    bin_list = []
    for item in items:
        bins = frappe.db.sql("""
            SELECT * FROM `tabBin` WHERE item_code=%s AND warehouse=%s
        """, (item['item_code'], item['warehouse']), as_dict=True)
        bin_list.extend(bins)
    backup_data['bins'] = bin_list
    
    # Write backup to file
    backup_file = f"/home/frappe/teampro-bench/tmp_si_restore/backup_TFP_1886_{timestamp}.json"
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, default=str, indent=2)
    
    print(f"Backup saved to: {backup_file}")
    print(f"  Sales Invoice records: {len(si)}")
    print(f"  POS Payment records: {len(sip)}")
    print(f"  GL Entry records: {len(gle)}")
    print(f"  Stock Ledger Entry records: {len(sle)}")
    print(f"  Bin records: {len(bin_list)}")
    
    return backup_file
