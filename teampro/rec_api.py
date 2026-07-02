
import frappe

@frappe.whitelist(allow_guest=True)
def get_active_images():

    child_data = frappe.get_all(
        "Advertisement Details",
        filters={
            "is_active": 1
        },
        fields=["attach", "parent"]
    )

    final_data = []

    for row in child_data:

        status = frappe.db.get_value(
            "Project",
            row.parent,
            "status"
        )

        if status == "Open":

            final_data.append({
                "attach": frappe.utils.get_url() + row.attach
            })

    return final_data