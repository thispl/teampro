# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CaseSummary(Document):
    pass
@frappe.whitelist()
def get_batch_data_table(batch=None, from_date=None, to_date=None, company=None,case=None,report=None,empname=None,empid=None):
    filters = {}
    if company:
        filters['customer'] = company
    if case:
        filters['case_status'] = case
    if report:
        filters['case_report'] = report
    if empname:
        filters['case_name'] = empname
    if empid:
        filters['client_employee_code'] = empid
    if batch:
        filters['batch'] = batch
    if from_date and to_date:
        filters['date_of_initiating'] = ['between', [from_date, to_date]]
    elif from_date:
        filters['date_of_initiating'] = ['>=', from_date]
    elif to_date:
        filters['date_of_initiating'] = ['<=', to_date]
    cases = frappe.get_list('Case', filters,
                            ['name', 'case_name', 'batch',
                             'date_of_initiating', 'end_date',
                             'case_report', 'case_status','client_employee_code','actual_tat'],
                            order_by="date_of_initiating desc")
    if not cases:
        return "<center><h2>No cases found for the specified criteria</h2></center>"
    data = '<html><head><script src="//cdn.datatables.net/2.0.8/js/dataTables.min.js"></script><script>let table = new DataTable("#caseSummary");</script><link rel="stylesheet" href="//cdn.datatables.net/2.0.8/css/dataTables.dataTables.min.css"></head><body>'
    data += "<table class='table table-bordered' id='caseSummary' style='border-collapse: collapse; width: 100%; border: 1px solid black;'>"
    data += "<tr style='border: 1px solid black; background-color: #0f1568; color: white;'>"
    data += "<th style='width:2%'>SI NO</th><th style='width:15%'>Case ID</th><th style='width:8%'>ID</th><th style='width:10%'>Name</th><th style='width:10%'>Batch</th>"
    data += "<th style='width:11%'>Date of Initiation</th><th style='width:11%'>Completion Date</th><th style='width:7%'>Age</th><th style='width:18%'>Case Status</th>"
    data += "<th style='width:15%'>Report Status</th><th>Check Report</th><th style='width:13%'>Check Status</th></tr>"
    for count, case in enumerate(cases, start=1):
        formatted_initiation_date = case.date_of_initiating.strftime('%d-%m-%Y') if case.date_of_initiating else ''
        formatted_end_date = case.end_date.strftime('%d-%m-%Y') if case.end_date else ''        
        if case.case_report == 'Positive':
            report_status_color = 'color: blue;'
        elif case.case_report == 'Negative':
            report_status_color = 'color: red;'
        elif case.case_report == 'Dilemma':
            report_status_color = 'color: orange;'
        else:
            report_status_color = 'color: black;'  
        data += "<tr style='border: 1px solid black;'>"
        data += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (
            count, case.name,case.client_employee_code, case.case_name, case.batch)
        data += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (
            formatted_initiation_date, formatted_end_date, case.actual_tat, case.case_status)
        data += "<td style='%s'>%s</td>" % (report_status_color, case.case_report)
        data += "<td><button onclick=\"downloadReport('%s')\">Download</button></td>" % case.name
        data += "<td><button onclick=\"viewCaseStatus('%s')\">Case Status</button></td>" % case.name
        data += "</tr>"
    return_report_options(batch=None, from_date=None, to_date=None, company=None)
    data += "</table></body></html>"
    return data

@frappe.whitelist()
def get_batch_data(batch=None, from_date=None, to_date=None, company=None, case=None, report=None, empname=None, empid=None):
    filters = {}
    if company:
        filters['customer']=company
    if case:
        filters['case_status']=case
    if report:
        filters['case_report']=report
    if empname:
        filters['case_name']=empname
    if empid:
        filters['client_employee_code']=empid
    if batch:
        filters['batch']=batch
    if from_date and to_date:
        filters['date_of_initiating']=['between',[from_date,to_date]]
    elif from_date:
        filters['date_of_initiating']=['>=',from_date]
    elif to_date:
        filters['date_of_initiating']=['<=',to_date]
    cases=frappe.get_list('Case',filters,['name','case_name','batch','date_of_initiating','end_date','case_report', 'case_status', 'client_employee_code', 'actual_tat'],order_by="date_of_initiating desc")
    data=[]
    count=1
    for case in cases:
        formatted_initiation_date = case.date_of_initiating.strftime('%d-%m-%Y') if case.date_of_initiating else ''
        formatted_end_date = case.end_date.strftime('%d-%m-%Y') if case.end_date else ''
        if case.case_report == 'Positive':
            report_status_color = 'blue'
        elif case.case_report == 'Negative':
            report_status_color = 'red'
        elif case.case_report == 'Dilemma':
            report_status_color = 'orange'
        else:
            report_status_color = 'black'
        data.append({'s_no':count,'case_name':case.name,'id':case.client_employee_code,'name':case.case_name,'batch':case.batch,'initiation':formatted_initiation_date,'completion':formatted_end_date,'age':case.actual_tat,'case_status':case.case_status,'report_status':case.case_report})

        # ,'ID':case.client_employee_code,'Name':case.case_name,
        #     'Batch':case.batch,'Date of Initiation':formatted_initiation_date,'Completion Date':formatted_end_date,
        #     'Age':case.actual_tat,'Case Status':case.case_status,'Report Status':case.case_report,'Report Status Color': report_status_color
        count += 1 
    return data

@frappe.whitelist()
def return_report_options(batch=None, from_date=None, to_date=None, company=None, case=None, report=None, empname=None, empid=None):
    filters={}
    if company:
        filters['customer']=company
    if case:
        filters['case_status']=case
    if report:
        filters['case_report']=report
    if empname:
        filters['case_name']=empname
    if empid:
        filters['client_employee_code']=empid
    if batch:
        filters['batch']=batch
    if from_date and to_date:
        filters['date_of_initiating']=['between',[from_date,to_date]]
    elif from_date:
        filters['date_of_initiating']=['>=',from_date]
    elif to_date:
        filters['date_of_initiating']=['<=',to_date]    
    fields_to_fetch=['case_report','case_status']
    cases=frappe.get_list('Case',filters,fields_to_fetch)
    if not cases:
        return []
    unique_reports=[" "]
    unique_statuses=[" "]
    seen_reports=set()
    seen_statuses=set()
    for case in cases:
        report=case.case_report
        status=case.case_status
        if report and report not in seen_reports:
            unique_reports.append(report)
            seen_reports.add(report)
        if status and status not in seen_statuses:
            unique_statuses.append(status)
            seen_statuses.add(status)
    return {
        "report_options": unique_reports,
        "status_options": unique_statuses
    }

@frappe.whitelist()
def check_status_table(name):
    case = frappe.get_doc("Case", name)
    checks = case.get("checkwise_status")  
    data = """
    <table class='table table-bordered' style='border-collapse: collapse; width: 100%;'><tr style='border: 1px solid black; background-color: #0f1568; color: white;'><th><b>SI NO</b></th><th><b>Checks</b></th><th><b>Check ID</b></th><th><b>Check Status</b></th><th><b>Check Report</b></th></tr>"""
    sno = 0
    for check in checks:
        sno += 1
        data += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"""%(sno, check.checks, check.check_id, check.checks_status, check.check_report)
    data += "</table>"
    return data


