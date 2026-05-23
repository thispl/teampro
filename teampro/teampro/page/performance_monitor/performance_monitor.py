import frappe
from collections import defaultdict

@frappe.whitelist()
def get_active_employees_by_department():
    # ✅ List of departments to show
    allowed_departments = [
        "IT. Development - THIS",
        "Recruitment - THIS",
        "Finance & Accountant - THIS",
        "R&S - IT Services - THIS",
        "R&S - HR Service - THIS",
        "TFP - Factroy - TFP",
        "BCS - THIS",
        "CS & DND - THIS"
    ]

    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "employee_name", "department"]
    )

    data = defaultdict(list)

    for emp in employees:
        department = emp.department
        if department in allowed_departments:
            data[department].append({
                "emp_id": emp.name,
                "emp_name": emp.employee_name
            })

    return data
