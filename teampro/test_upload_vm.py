def run():
    import frappe

    # Check if company was renamed
    print("--- Company rename history ---")
    # Check version log for company rename
    renames = frappe.db.sql("select name, creation, owner from tabVersion where ref_doctype='Company' and docname='TEAMPRO Food Products' order by creation desc limit 5", as_dict=True)
    print("Company versions:", renames)

    # Check user defaults for company
    print("\n--- User defaults ---")
    user_defaults = frappe.db.sql("select defkey, defvalue from `tabDefaultValue` where parent='bhuvaneswari.a@groupteampro.com' and defkey='Company'", as_dict=True)
    print("User company defaults:", user_defaults)

    # Check global defaults
    print("\n--- Global defaults ---")
    global_defaults = frappe.db.sql("select defkey, defvalue from `tabDefaultValue` where parent='__default' and defkey='Company'", as_dict=True)
    print("Global company defaults:", global_defaults)

    # Check ALL default values for this user
    print("\n--- All user defaults ---")
    all_defaults = frappe.db.sql("select defkey, defvalue from `tabDefaultValue` where parent='bhuvaneswari.a@groupteampro.com'", as_dict=True)
    for d in all_defaults:
        print(f"  {d['defkey']}: {d['defvalue']!r}")

    # Check if there's a POS profile that sets the company
    print("\n--- POS Profile VM1_Precision ---")
    pos = frappe.db.get_value("POS Profile", "VM1_Precision", ["company", "name"], as_dict=True)
    print("POS Profile:", pos)

    # Check existing Sales Invoices for this company - what company value do they use?
    print("\n--- Recent SI company values ---")
    recent = frappe.db.sql("select name, company from `tabSales Invoice` where company like '%FOOD%' or company like '%Food%' limit 5", as_dict=True)
    for r in recent:
        print(f"  {r['name']}: company={r['company']!r}")
