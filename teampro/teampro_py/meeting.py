import frappe
import openpyxl
from io import BytesIO

@frappe.whitelist()
def update_meeting_id(meet):
    meeting=frappe.get_doc("Meeting",meet)
    for i in meeting.minutes:
        if i.custom_action == "Task" and i.custom_id:
            frappe.db.set_value("Task",i.custom_id,'custom_meeting_id',meet)
        elif i.custom_action == "To Do" and i.custom_id:
            frappe.db.set_value("ToDo",i.custom_id,'custom_meeting_id',meet)

import bleach
from frappe.utils import strip
@frappe.whitelist()
def make_minutes_for_mom_points():
    args = frappe.local.form_dict
    filename = args.name
    test = build_xlsx_response_mom(filename)

def make_xlsx_mom(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name, 0)
    doc = frappe.get_doc("Meeting",args.name)
    if doc:
        ws.append(["Description","Action","Task"])
        for i in doc.minutes:
            description_without_html = bleach.clean(i.description, tags=[], strip=True)
            ws.append([description_without_html, i.custom_action, i.custom_id])
            # ws.append([i.description,i.custom_action,i.custom_id])
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file

def build_xlsx_response_mom(filename):
    xlsx_file = make_xlsx_mom(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'