
import frappe
import json

def execute():
    ws = frappe.get_doc("Workspace", "Internal Dashboards")
    existing = [s for s in ws.shortcuts if s.label == "Finance and Accounts"]
    if not existing:
        ws.append("shortcuts", {
            "label": "Finance and Accounts",
            "type": "URL",
            "url": "https://erp.teamproit.com/app/finance_accounts",
            "col": 3
        })
        content = json.loads(ws.content) if ws.content else []
        content.append({
            "id": "finacc01",
            "type": "shortcut",
            "data": {
                "shortcut_name": "Finance and Accounts",
                "col": 3
            }
        })
        ws.content = json.dumps(content)
        ws.save()
        frappe.db.commit()
        print("Shortcut added successfully")
    else:
        print("Shortcut already exists")
