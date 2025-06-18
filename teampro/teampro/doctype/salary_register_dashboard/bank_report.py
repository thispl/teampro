# import frappe
# from frappe.utils.csvutils import UnicodeWriter
# from frappe.utils import cstr
# import io

# @frappe.whitelist()
# def get_template():

#     output = frappe.response["result"] = io.StringIO()
#     writer = UnicodeWriter(output)
    
#     writer = add_header(writer)
#     writer = add_data(writer)
    
#     frappe.response['result'] = cstr(writer.getvalue())
#     frappe.response['type'] = 'csv'
#     frappe.response['doctype'] = "Bank Upload"

# def add_header(writer):
#     writer.writerow([
#         "PYMT_PROD_TYPE_CODE", "PYMT_MODE", "DEBIT_ACC_NO", "BNF_NAME", "BENE_ACC_NO",
#         "BENE_IFSC", "AMOUNT", "DEBIT_NARR", "CREDIT_NARR", "MOBILE_NUM", "EMAIL_ID",
#         "REMARK", "PYMT_DATE", "REF_NO", "ADDL_INFO1", "ADDL_INFO2", "ADDL_INFO3",
#         "ADDL_INFO4", "ADDL_INFO5"
#     ])
#     return writer

# def add_data(writer):
#     data = get_data()
#     for row in data:
#         writer.writerow([cstr(value) for value in row])
#     return writer

# def get_data():
#     employees = frappe.db.get_all(
#         "Employee",
#         filters={"status": "Active"},
#         fields=["employee_name", "bank_ac_no", "ifsc_code"]
#     )
#     data = []
#     debit = "777705160983"

#     for emp in employees:
#         salary = frappe.db.get_value(
#             "Salary Slip",
#             filters={"employee_name": emp["employee_name"], "docstatus": ["!=", 2]},
#             fieldname="net_pay"
#         )
#         salary = salary if salary else 0
#         data.append([
#             "PAB_VENDOR",
#             "IMPS",
#             debit,
#             emp["employee_name"],
#             emp["bank_ac_no"] or "",
#             emp["ifsc_code"] or "",
#             salary,
#             "Salary",
#             "Salary",
#             "",
#             "",
#             "",
#             "2024-12-10",
#             "", "", "", "", "", "",
#         ])

#     return data

import frappe
from openpyxl import Workbook
from frappe.utils import cstr
import io

@frappe.whitelist()
def get_template():
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Bank Upload Template"

    add_header(ws)
    add_data(ws)

    wb.save(output)
    output.seek(0)

    frappe.response['filename'] = "Bank_Upload_Template.xlsx"
    frappe.response['filecontent'] = output.getvalue()
    frappe.response['type'] = 'binary'

def add_header(ws):
    ws.append([
        "PYMT_PROD_TYPE_CODE", "PYMT_MODE", "DEBIT_ACC_NO", "BNF_NAME", "BENE_ACC_NO",
        "BENE_IFSC", "AMOUNT", "DEBIT_NARR", "CREDIT_NARR", "MOBILE_NUM", "EMAIL_ID",
        "REMARK", "PYMT_DATE", "REF_NO", "ADDL_INFO1", "ADDL_INFO2", "ADDL_INFO3",
        "ADDL_INFO4", "ADDL_INFO5"
    ])

def add_data(ws):
    data = get_data()
    for row in data:
        ws.append([cstr(value) for value in row])

def get_data():
    employees = frappe.db.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["employee_name", "bank_ac_no", "ifsc_code"]
    )
    data = []
    debit = "777705160983"

    for emp in employees:
        salary = frappe.db.get_value(
            "Salary Slip",
            filters={"employee_name": emp["employee_name"], "docstatus": ["!=", 2]},
            fieldname="net_pay"
        )
        salary = salary if salary else 0
        data.append([
            "PAB_VENDOR", "IMPS", debit, emp["employee_name"], emp["bank_ac_no"] or "", emp["ifsc_code"] or "", salary, "Salary",
            "Salary", "", "", "", "2024-12-10",  "", "", "", "", "", "",
        ])

    return data
