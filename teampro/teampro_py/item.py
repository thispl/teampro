import frappe
@frappe.whitelist()
def create_website_item(name):
    item = frappe.get_doc("Item", name)

    # Only required fields
    params = {
        "item_code": item.name,
        "item_name": item.item_name,
        "item_group": item.item_group,
        "stock_uom": item.stock_uom
    }

    frappe.errprint(f"Payload Sending: {params}")

    url = "https://daileemart.com/api/method/daileemart.www.update_items.create_from_task"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "token a718baed40f219b:81fd1cf12e6d4fe"
    }

    try:
        response = requests.post(url, headers=headers, json=params, timeout=10, verify=False)
        res = response.json()
        return res

    except Exception as e:
        frappe.throw(f"Sync failed: {str(e)}")

