import frappe
@frappe.whitelist()
def update_wp_template_status(temp_name,name):
    import requests

    url = "https://graph.facebook.com/v17.0/114380668325008/message_templates"

    headers = {"authorization": "Bearer EAAIsCk6qqtMBRnZBhmKdyoKts7Q3torzXtjRaDlq0c1ELLDuFwwHmqE5wh2iCyARktB7ez4TlX4WH31AcRkOpxZCdfz2gdBlHfeY918c2vHARZAC7JBOXwvbP2pDLZCFK0CfmAsXUSJ5zYV8JBmqLTw19DarAKJfLjGQB5UQwiHnyb8BQeCbJe55W33M4kmHJEIduA7Ck3Pv04W9Qw5IgoqxxjYHHFibOvPYKskUe6cE4ede38L9puctPc99W30ZAROEsHuYOGZA7rVlxV0wqr"}

    response = requests.get(url, headers=headers)
    value = response.json()
    if "data" in value:
        for i in value["data"]:
            if i.get("name")==temp_name:
                frappe.db.set_value("WhatsApp Templates",name,"status",i.get("status"))

