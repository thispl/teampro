import frappe

@frappe.whitelist()
def text_template():
    file_name = "PF.txt"
    file_content = generate_data(frappe.local.form_dict)

    frappe.local.response.filename = file_name
    frappe.local.response.filecontent = file_content
    frappe.local.response.type = "download"

def generate_data(args):
    from_date = args.get("from_date")
    to_date = args.get("to_date")

    if not from_date or not to_date:
        frappe.throw("Please specify both 'from_date' and 'to_date'.")

    headers = ["UAN", "MEMBER NAME", "GROSS WAGES", "EPF WAGES", "EPS WAGES", "EDLI WAGES",
               "EPF CONTRI REMITTED", "EPS CONTRI REMITTED", "EPF EPS DIFF REMITTED", "NCP DAYS",
               "REFUND OF ADVANCES"]

    data = ["\t".join(headers)]

    employees = frappe.db.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "employee_name", "user_id", "custom_uan_number"]
    )

    for emp in employees:
        salary_slips = frappe.db.get_all(
            "Salary Slip",
            filters={
                "employee": emp["name"],
                "docstatus": ["!=", 2],
                "start_date": from_date,
                "end_date": to_date,
            },
            fields=["name", "gross_pay", "leave_without_pay"]
        )

        salary_details = calculate_salary_details(salary_slips)

        eps_wages = "0" if emp["user_id"] == "anil.p@groupteampro.com" else "15000"
        eps_contri_remitted = (salary_details.get('Provident Fund', 0) * 0.70 if emp["user_id"] in ["dc@groupteampro.com", "mariyammal.a@groupteampro.com"] else 1800 * 0.70)
        epf_eps_diff_remitted = (salary_details.get('Provident Fund', 0) * 0.30 if emp["user_id"] in ["dc@groupteampro.com", "mariyammal.a@groupteampro.com"] else 1800 * 0.3)

        for slip in salary_slips:
            data.append("\t".join([
                str(emp["custom_uan_number"] or ""),
                str(emp["employee_name"] or ""),
                f"{slip['gross_pay'] or 0:.2f}",
                "15000",
                str(eps_wages),
                "15000",
                f"{salary_details.get('Provident Fund', 0):.2f}",
                f"{eps_contri_remitted:.2f}",
                f"{epf_eps_diff_remitted:.2f}",
                str(slip["leave_without_pay"] or 0),
                "0"
            ]))


    return "\n".join(data)

def calculate_salary_details(salary_slips):
    salary_details = {}

    for slip in salary_slips:
        for component in ["Provident Fund"]:
            salary_amount = frappe.db.get_value(
                "Salary Detail",
                {"parent": slip["name"], "salary_component": component},
                "amount"
            ) or 0
            salary_details[component] = salary_details.get(component, 0) + salary_amount

    return salary_details
