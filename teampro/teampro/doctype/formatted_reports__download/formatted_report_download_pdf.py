import frappe
from frappe.utils.pdf import get_pdf
from datetime import datetime

@frappe.whitelist()
def download_pdf(customer=None, project=None):
    filename = "PR_02_Project_Status_Report.pdf"
    pdf_content = make_pdf(customer, project)

    frappe.local.response.filename = filename
    frappe.local.response.filecontent = pdf_content
    frappe.local.response.type = "binary"

def make_pdf(customer=None, project=None):
    filters = {"docstatus": ("!=", "2"), "service": "IT-SW"}
    filters_1 = {"status": ("not in", ["Hold", "Completed", "Cancelled"]), "service": "IT-SW"}

    if customer and not project:
        filters["customer"] = customer  
    elif project and not customer:
        filters_1["name"] = project  
    elif customer and project:
        filters["customer"] = customer
        filters["name"] = project  

    report = frappe.db.get_all(
        "Project",
        filters=filters_1,
        fields=["name", "project_name", "account_manager_remark", "remark", "custom_spoc_remark",
                "no_of_task", "open", "working", "pr"]
    )

    current_date = datetime.today().strftime("%d-%m-%Y")

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 12px;
            }}
            h2 {{
                text-align: center;
                background-color: #000080;
                color: white;
                padding: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th {{
                background-color: #00BFFF;
                color: black;
                padding: 5px;
                border: 1px solid black;
                text-align: center;
            }}
            td {{
                padding: 5px;
                border: 1px solid black;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h2>IT - SW Project Status Report (As on {current_date})</h2>
        <table>
            <thead>
                <tr>
                    <th>Project Name</th>
                    <th>Account Manager Remark</th>
                    <th>Project Manager Remark</th>
                    <th>SPOC Remark</th>
                    <th># Task</th>
                    <th># Open</th>
                    <th># Working</th>
                    <th># PR</th>
                    <th># CR</th>
                    <th>SO Value</th>
                    <th>Pending Billing</th>
                </tr>
            </thead>
            <tbody>
    """

    for row in report:
        task_count = frappe.db.count(
            "Task",
            filters={"docstatus": ("!=", "2"), "project": row.name, "status": "Client Review", "service": "IT-SW"}
        )

        so_value = frappe.db.sql("""
            SELECT SUM(grand_total) 
            FROM `tabSales Order`
            WHERE project = %s AND docstatus != 2
        """, (row.name,))[0][0] or 0.0  

        sales_order = frappe.db.sql("""
            SELECT 
                s.base_grand_total AS base_grand_total,
                s.per_billed AS per_billed,
                s.advance_paid AS advance_paid
            FROM 
                `tabSales Order` s
            WHERE 
                s.status NOT IN ('To Deliver', 'On Hold', 'Closed', 'Cancelled', 'Completed') 
                AND s.project=%s
        """, (row.name,), as_dict=True)

        if sales_order:
            base_grand_total = sales_order[0].get("base_grand_total", 0.0)  
            per_billed = sales_order[0].get("per_billed", 0.0) or 0  
            advance_paid = sales_order[0].get("advance_paid", 0.0) or 0  

            amount_billed = (base_grand_total * per_billed) / 100  
            pending_billing = base_grand_total - (amount_billed + advance_paid)  
        else:
            pending_billing = 0.0

        html_content += f"""
            <tr>
                <td>{row.project_name}</td>
                <td>{row.account_manager_remark or ''}</td>
                <td>{row.remark or ''}</td>
                <td>{row.custom_spoc_remark or ''}</td>
                <td>{row.no_of_task}</td>
                <td>{row.open}</td>
                <td>{row.working}</td>
                <td>{row.pr}</td>
                <td>{task_count}</td>
                <td>₹ {so_value:,.2f}</td>
                <td>₹ {pending_billing:,.2f}</td>
            </tr>
        """

    html_content += "</tbody></table></body></html>"

    return get_pdf(html_content)
