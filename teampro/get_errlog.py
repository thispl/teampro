import frappe

def check_perms():
    user = "bhuvaneswari.a@groupteampro.com"
    roles = frappe.get_roles(user)
    print("ROLES:", roles)

    # Check standard permissions
    from frappe.permissions import get_role_permissions
    meta = frappe.get_meta("Sales Invoice")
    for role in roles:
        perms = frappe.db.get_values(
            "Custom DocPerm",
            {"parent": "Sales Invoice", "role": role},
            ["read", "write", "create", "submit", "cancel", "amend", "if_owner", "permlevel"],
            as_dict=True,
        )
        if perms:
            print(f"\nCustom DocPerm for role {role}:")
            for p in perms:
                print(f"  {p}")

        perms2 = frappe.db.get_values(
            "DocPerm",
            {"parent": "Sales Invoice", "role": role},
            ["read", "write", "create", "submit", "cancel", "amend", "if_owner", "permlevel"],
            as_dict=True,
        )
        if perms2:
            print(f"\nDocPerm for role {role}:")
            for p in perms2:
                print(f"  {p}")

    # Check if user has permission
    print("\nhas_permission read:", frappe.has_permission("Sales Invoice", "read", user=user))
    print("has_permission write:", frappe.has_permission("Sales Invoice", "write", user=user))
    print("has_permission create:", frappe.has_permission("Sales Invoice", "create", user=user))

    # Check role permissions for Sales Invoice
    print("\n=== Role Permissions for all roles of user ===")
    for role in roles:
        rp = get_role_permissions(frappe.get_meta("Sales Invoice"), role)
        if any(rp.values()):
            print(f"Role {role}: {rp}")
