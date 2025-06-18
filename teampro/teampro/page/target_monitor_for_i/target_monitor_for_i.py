import frappe
from datetime import datetime
from frappe import _
from frappe.utils import getdate, get_timespan_date_range,flt,today,nowdate,fmt_money
import json
from datetime import date, timedelta

@frappe.whitelist()
def get_ct_ft(employee=None):
    from datetime import datetime
    from frappe.utils import today

    date = datetime.strptime(today(), '%Y-%m-%d')
    mon = datetime.strftime(date, '%b')

    # Get all Target Manager documents, filter by employee if provided
    filters = {}
    if employee:
        filters['employee'] = employee  # Assuming 'employee' is the field in 'Target Manager'
    
    target_managers = frappe.db.get_all('Target Manager', filters, ["*"])
    slides = []

    for target in target_managers:
        doc = frappe.get_doc('Target Manager', target['name'])

        # Fetch child table data for the month
        child_data = frappe.db.get_all(
            'Target Child', 
            {'parent': doc.name, 'month': mon}, 
            ['ct', 'achieved', 'ct_yta', 'revised_ct']
        )

        child_data1 = frappe.db.get_all(
            'Target FT Child',
            {"parent": doc.name, "month": mon},
            ["ft", "cr_ft", "f_achieved", "ftyta"]
        )

        # Fetch employee details
        employee_doc = frappe.get_doc("Employee", doc.employee)
        if employee_doc.status == "Active":
            if child_data or child_data1:  # Check if either child_data or child_data1 has entries
                combined_data = []

                # Combine both child data sets
                for i in range(max(len(child_data), len(child_data1))):
                    entry = {}

                    if i < len(child_data):
                        entry.update({
                            'ct': round(child_data[i].ct, 2) if child_data[i].ct is not None else 0,
                            'achieved': round(child_data[i].achieved, 2) if child_data[i].achieved is not None else 0,
                            'ct_yta': round(child_data[i].ct_yta, 2) if child_data[i].ct_yta is not None else 0,
                            'revised_ct': round(child_data[i].revised_ct, 2) if child_data[i].revised_ct is not None else 0
                        })

                    if i < len(child_data1):
                        entry.update({
                            'ft': round(child_data1[i].ft, 2) if child_data1[i].ft is not None else 0,
                            'cr_ft': round(child_data1[i].cr_ft, 2) if child_data1[i].cr_ft is not None else 0,
                            'f_achieved': round(child_data1[i].f_achieved, 2) if child_data1[i].f_achieved is not None else 0,
                            'ftyta': round(child_data1[i].ftyta, 2) if child_data1[i].ftyta is not None else 0
                        })

                    combined_data.append(entry)

                slides.append({
                    'manager': doc.name,
                    'data': combined_data,
                    'employee_name': employee_doc.employee_name,
                    'employee_image': employee_doc.image,
                    'employee_designation': employee_doc.designation,
                    'fiscal_year': doc.custom_fiscal_year,
                    'annual_ct': round(doc.annual_ct, 2) if doc.annual_ct is not None else 0,
                    'annual_ft': round(doc.annual_ft, 2) if doc.annual_ft is not None else 0,
                    'target': doc.target_based_unit
                })

    return slides

import frappe
from datetime import datetime
from frappe.utils import today
@frappe.whitelist()
def get_target_manager_data(employee=None, month=None, fiscal_year=None):
    """
    Fetch CT and FT data for the selected employee and month.
    If no employee is provided, fetch data for all employees.
    If no month is provided, use the current month.
    """

    # If month is not provided, default to the current month
    if not month:
        current_date = datetime.strptime(today(), '%Y-%m-%d')
        month = datetime.strftime(current_date, '%b')  # Default to current month

    # Debug: Print the received month

    # Prepare filters
    filters = {}
    if employee:
        filters['employee'] = employee  # Filter by employee if provided
    if fiscal_year:
        filters['custom_fiscal_year'] = fiscal_year

    # Get Target Manager documents with optional employee filter
    target_managers = frappe.db.get_all('Target Manager', filters, ["*"])

    slides = []
    # Get current date information
    date = datetime.strptime(today(), '%Y-%m-%d')
    current_month = datetime.strftime(date, '%b')
    
    # Define quarter months
    quarters = {
        'Q1': ['Apr', 'May', 'Jun'],
        'Q2': ['Jul', 'Aug', 'Sep'],
        'Q3': ['Oct', 'Nov', 'Dec'],
        'Q4': ['Jan', 'Feb', 'Mar']
    }

    # Determine the quarter the current month falls into
    current_quarter = None
    for quarter, months in quarters.items():
        if current_month in months:
            current_quarter = quarter
            break

    for target in target_managers:
        doc = frappe.get_doc('Target Manager', target['name'])
        fiscal_year = doc.custom_fiscal_year
        fiscal_year_months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        months_to_include = fiscal_year_months[:fiscal_year_months.index(current_month) + 1]
        
        # Initialize variables for YTD and QTD
        qtd_target_ct = 0  
        qtd_achieved = 0  
        ytd_target_ct = 0  
        ytd_achieved = 0  
        yta_qtd = 0  
        yta_ytd = 0  
        qtd_sr = 0  
        ytd_sr = 0  
        revised_tot=0
        revised_qtd=0
        # Fetch data from Target Child table for the selected month
        child_data = frappe.db.get_all(
            'Target Child', 
            {'parent': doc.name, 'month': month},  # Apply the month filter here
            ['ct', 'achieved', 'ct_yta', 'revised_ct']
        )

        # Debug: Check if child_data is being populated

        # Fetch data from Target FT Child table for the selected month
        child_data1 = frappe.db.get_all(
            'Target FT Child',
            {"parent": doc.name, "month": month},  # Apply the month filter here
            ["ft", "cr_ft", "f_achieved", "ftyta"]
        )

        # Debug: Check if child_data1 is being populated

        # Get employee details
        employee_doc = frappe.get_doc("Employee", doc.employee)
        
        if employee_doc.status == "Active":

            if current_quarter == 'Q3':  # For Quarter 3 (Oct, Nov, Dec)
                if current_month == 'Oct':
                    # Add October, November, and December
                    months_in_quarter = ['Oct', 'Nov', 'Dec']
                elif current_month == 'Nov':
                    # Add November and December
                    months_in_quarter = ['Oct', 'Nov', 'Dec']
                elif current_month == 'Dec':
                    # Add December only
                    months_in_quarter = ['Oct', 'Nov', 'Dec']
                # For other quarters (Q1, Q2, Q4), you can add similar logic if needed
            if current_quarter == 'Q1':  # For Quarter 3 (Oct, Nov, Dec)
                if current_month == 'Apr':
                    # Add October, November, and December
                    months_in_quarter = ['Apr', 'May', 'Jun']
                elif current_month == 'May':
                    # Add November and December
                    months_in_quarter = ['Apr', 'May', 'Jun']
                elif current_month == 'Jun':
                    # Add December only
                    months_in_quarter = ['Apr', 'May', 'Jun']
            if current_quarter == 'Q2':  # For Quarter 3 (Oct, Nov, Dec)
                if current_month == 'Jul':
                    # Add October, November, and December
                    months_in_quarter = ['Jul', 'Aug', 'Sep']
                elif current_month == 'Aug':
                    # Add November and December
                    months_in_quarter = ['Jul', 'Aug', 'Sep']
                elif current_month == 'Sep':
                    # Add December only
                    months_in_quarter = ['Jul', 'Aug', 'Sep']
            if current_quarter == 'Q4':  # For Quarter 3 (Oct, Nov, Dec)
                if current_month == 'Jan':
                    # Add October, November, and December
                    months_in_quarter = ['Jan', 'Feb', 'Mar']
                elif current_month == 'Feb':
                    # Add November and December
                    months_in_quarter =['Jan', 'Feb', 'Mar']
                elif current_month == 'Mar':
                    months_in_quarter =['Jan', 'Feb', 'Mar']

            for month in months_in_quarter:

                quarter_data = frappe.db.get_all(
                    'Target Child', 
                    {'parent': doc.name, 'month': month}, 
                    ['ct', 'achieved', 'ct_yta', 'revised_ct']
                )
                for data in quarter_data:
                    qtd_target_ct += round(data.revised_ct,2) if data.revised_ct else 0
                    qtd_achieved += round(data.achieved,2) if data.achieved else 0
                    revised_qtd+=round(data.revised_ct,2) if data.revised_ct else 0
                    yta_qtd += round(data.ct_yta,2) if data.ct_yta else 0
                    if revised_qtd!= 0:
                        qtd_sr = round(((qtd_achieved / revised_qtd) * 100),2) if revised_qtd else 0

            # Loop through fiscal year months and calculate YTD totals
            for month in months_to_include:
                ytd_data = frappe.db.get_all(
                    'Target Child', 
                    {'parent': doc.name, 'month': month}, 
                    ['ct', 'achieved', 'ct_yta', 'revised_ct']
                )
                for p in ytd_data:
                    ytd_target_ct += round(p.revised_ct,2) if p.revised_ct else 0
                    ytd_achieved += round(p.achieved,2) if p.achieved else 0
                    revised_tot+=round(p.revised_ct,2) if p.revised_ct else 0
                    yta_ytd += round(p.ct_yta,2) if p.ct_yta else 0
                    if revised_tot != 0:
                        ytd_sr = round(((ytd_achieved / revised_tot) * 100),2) if revised_tot else 0
            yol_ytd_target_ct = yol_ytd_achieved = yol_revised_tot = yol_yta_ytd = 0
            for m in fiscal_year_months:
                # Retrieve data for each month in the YOL calculation
                yol_data = frappe.db.get_all(
                    'Target Child', 
                    {'parent': doc.name, 'month': m}, 
                    ['ct', 'achieved', 'ct_yta', 'revised_ct']
                )
                
                # Summing up the values to calculate YOL totals
                for p in yol_data:
                    yol_ytd_target_ct += round(p.revised_ct or 0)
                    yol_ytd_achieved += round(p.achieved or 0)
                    yol_revised_tot += round(p.revised_ct or 0)
                    yol_yta_ytd += round(p.ct_yta or 0)
                    if yol_revised_tot!=0:
                        yol_sr = round(((yol_ytd_achieved / yol_revised_tot) * 100)) if yol_revised_tot else 0
            # Only process if there's data in either child_data or child_data1
            if child_data or child_data1:
                combined_data = []

                # Combine data from both child tables (handle lists of different lengths)
                for i in range(max(len(child_data), len(child_data1))):
                    entry = {}
                    mtd_sr = round(((child_data[i].achieved / child_data[i].revised_ct) * 100),2) if child_data[i].revised_ct != 0 else 0

                    if i < len(child_data):
                        entry.update({
                            'ct': fmt_money(child_data[i].ct) if child_data[i].ct is not None else 0,
                            'achieved': fmt_money(child_data[i].achieved) if child_data[i].achieved is not None else 0,
                            'ct_yta': fmt_money(child_data[i].ct_yta) if child_data[i].ct_yta is not None else 0,
                            'revised_ct': fmt_money(child_data[i].revised_ct) if child_data[i].revised_ct is not None else 0,
                            'mtd_sr': mtd_sr,
                        })

                    if i < len(child_data1):
                        entry.update({
                            'ft': round(child_data1[i].ft, 2) if child_data1[i].ft is not None else 0,
                            'cr_ft': round(child_data1[i].cr_ft, 2) if child_data1[i].cr_ft is not None else 0,
                            'f_achieved': round(child_data1[i].f_achieved, 2) if child_data1[i].f_achieved is not None else 0,
                            'ftyta': round(child_data1[i].ftyta, 2) if child_data1[i].ftyta is not None else 0
                        })

                    combined_data.append(entry)

                # Append the data to the slides list
                slides.append({
                    'manager': doc.name,
                    'data': combined_data,
                    'employee_name': employee_doc.employee_name,
                    'employee_image': employee_doc.image,
                    'employee_designation': employee_doc.designation,
                    'fiscal_year': doc.custom_fiscal_year,
                    'annual_ct': fmt_money(doc.annual_ct, 2) if doc.annual_ct is not None else 0,
                    'annual_ft': fmt_money(doc.annual_ft, 2) if doc.annual_ft is not None else 0,
                    'target': doc.target_based_unit,
                    'company': employee_doc.company,
                    'ytd_target_ct': fmt_money(ytd_target_ct),
                    'qtd_target_ct': fmt_money(qtd_target_ct),
                    'qtd_achieved': fmt_money(qtd_achieved),
                    'ytd_achieved': fmt_money(ytd_achieved),
                    'yta_qtd':fmt_money(yta_qtd),
                    'yta_ytd':fmt_money(yta_ytd),
                    'ytd_sr':fmt_money(ytd_sr),
                    'qtd_sr':fmt_money(qtd_sr),
                    'yol_ytd_target_ct':fmt_money(yol_ytd_target_ct),
                    'yol_ytd_achieved':fmt_money(yol_ytd_achieved),
                    'yol_revised_tot':fmt_money(yol_revised_tot),
                    'yol_yta_ytd':fmt_money(yol_yta_ytd),
                    'yol_sr':fmt_money(yol_sr)
                })

    # Check if slides list is empty and return a message if no data is found
    if not slides:
        return "No data for that fiscal year for employee"

    return slides

import frappe
from datetime import datetime
from frappe.utils import today
import frappe
from frappe.utils import today
from datetime import datetime

@frappe.whitelist()
def get_target_manager_data_for_services(service=None, month=None, fiscal_year=None):
    from datetime import datetime
    from frappe.utils import today, fmt_money

    # Ensure year is specified
    if not fiscal_year:
        frappe.throw("Fiscal year is required")
    
    # If month is not provided, default to the current month
    if not month:
        current_date = datetime.strptime(today(), '%Y-%m-%d')
        month = datetime.strftime(current_date, '%b')  # Default to current month


    # Set the employee ID based on the service
    if service in ['REC-I', 'REC-D', 'BCS']:
        employee = 'TI00003'
    elif service == 'IT-SW':
        employee = 'TI00005'
    elif service == 'TFP':
        employee = 'TI00002'
    else:
        frappe.throw("Invalid service provided")

    # Prepare filters
    filters = [service, fiscal_year, employee]

    # Start building the query
    query = """
        SELECT tm.* 
        FROM `tabTarget Manager` tm
        LEFT JOIN `tabEmployee services` tms ON tms.parent = tm.name
        WHERE tms.services = %s AND tm.custom_fiscal_year = %s AND tm.employee = %s
    """

    target_managers = frappe.db.sql(query, filters, as_dict=True)

    slides = []
    date = datetime.strptime(today(), '%Y-%m-%d')
    current_month = datetime.strftime(date, '%b')
    map_months = {
    'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
    'Oct': 10, 'Nov': 11, 'Dec': 12, 'Jan': 1, 'Feb': 2, 'Mar': 3
}
    quarters = {
        'Q1': ['Apr', 'May', 'Jun'],
        'Q2': ['Jul', 'Aug', 'Sep'],
        'Q3': ['Oct', 'Nov', 'Dec'],
        'Q4': ['Jan', 'Feb', 'Mar']
    }

    # Determine current quarter
    current_quarter = next(
        (qtr for qtr, months in quarters.items() if current_month in months),
        None
    )

    for target in target_managers:
        doc = frappe.get_doc('Target Manager', target['name'])
        fiscal_year_months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        months_to_include = fiscal_year_months[:fiscal_year_months.index(current_month) + 1]

        # Initialize YTD and QTD variables
        qtd_target_ct = qtd_achieved = ytd_target_ct = ytd_achieved = 0
        yta_qtd = yta_ytd = qtd_sr = ytd_sr = revised_tot = revised_qtd = 0

        # Fetch monthly data from Target Child and Target FT Child tables
        child_data = frappe.db.get_all(
            'Target Child', 
            {'parent': doc.name, 'month': month},
            ['ct', 'achieved', 'ct_yta', 'revised_ct']
        )

        child_data1 = frappe.db.get_all(
            'Target FT Child',
            {"parent": doc.name, "month": month},
            ["ft", "cr_ft", "f_achieved", "ftyta"]
        )

        # Calculate QTD and YTD metrics
        for m in quarters.get(current_quarter, []):
            quarter_data = frappe.db.get_all(
                'Target Child', 
                {'parent': doc.name, 'month': m}, 
                ['ct', 'achieved', 'ct_yta', 'revised_ct']
            )
            for data in quarter_data:
                qtd_target_ct += round(data.revised_ct) or 0
                qtd_achieved += round(data.achieved) or 0
                revised_qtd += round(data.revised_ct) or 0
                yta_qtd += round(data.ct_yta) or 0
                if revised_qtd!=0:
                    qtd_sr = round(((qtd_achieved / revised_qtd )* 100)) if revised_qtd else 0

        # Loop through fiscal year months and calculate YTD totals
        for m in months_to_include:
            ytd_data = frappe.db.get_all(
                'Target Child', 
                {'parent': doc.name, 'month': m}, 
                ['ct', 'achieved', 'ct_yta', 'revised_ct']
            )
            for p in ytd_data:
                ytd_target_ct += round(p.revised_ct) or 0
                ytd_achieved +=round( p.achieved) or 0
                revised_tot += round(p.revised_ct) or 0
                yta_ytd += round(p.ct_yta) or 0
                if revised_tot!=0:
                    ytd_sr = round(((ytd_achieved / revised_tot) * 100)) if revised_tot else 0

        # Combine child data for MTD, QTD, YTD

        yol_ytd_target_ct = yol_ytd_achieved = yol_revised_tot = yol_yta_ytd = 0
        for m in fiscal_year_months:
            # Retrieve data for each month in the YOL calculation
            yol_data = frappe.db.get_all(
                'Target Child', 
                {'parent': doc.name, 'month': m}, 
                ['ct', 'achieved', 'ct_yta', 'revised_ct']
            )
            
            # Summing up the values to calculate YOL totals
            for p in yol_data:
                yol_ytd_target_ct += round(p.revised_ct or 0)
                yol_ytd_achieved += round(p.achieved or 0)
                yol_revised_tot += round(p.revised_ct or 0)
                yol_yta_ytd += round(p.ct_yta or 0)
                if yol_revised_tot!=0:
                    # Calculate YOL Service Rate (YOL_SR)
                    yol_sr = round(((yol_ytd_achieved / yol_revised_tot) * 100)) if yol_revised_tot else 0


        combined_data = []
        for i in range(max(len(child_data), len(child_data1))):
            entry = {}
            if i < len(child_data):
                mtd_sr = round((child_data[i].achieved / child_data[i].revised_ct * 100),2) if child_data[i].revised_ct else 0
                entry.update({
                    'ct': fmt_money(round(child_data[i].ct)) or 0,
                    'achieved': fmt_money(round(child_data[i].achieved)) or 0,
                    'ct_yta': fmt_money(round(child_data[i].ct_yta)) or 0,
                    'revised_ct': fmt_money(round(child_data[i].revised_ct)) or 0,
                    'mtd_sr': mtd_sr
                })
            if i < len(child_data1):
                entry.update({
                    'ft': child_data1[i].ft or 0,
                    'cr_ft': child_data1[i].cr_ft or 0,
                    'f_achieved': child_data1[i].f_achieved or 0,
                    'ftyta': child_data1[i].ftyta or 0
                })
            combined_data.append(entry)

        slides.append({
            'manager': doc.name,
            'data': combined_data,
            'employee_image': frappe.get_value("Services", service, "logo"),
            'fiscal_year': doc.custom_fiscal_year,
            'annual_ct': fmt_money(doc.annual_ct) or 0,
            'annual_ft': fmt_money(doc.annual_ft) or 0,
            'target': doc.target_based_unit,
            'company': frappe.get_value("Employee", doc.employee, "company"),
            'ytd_target_ct': fmt_money(ytd_target_ct),
            'qtd_target_ct': fmt_money(qtd_target_ct),
            'qtd_achieved': fmt_money(qtd_achieved),
            'ytd_achieved': fmt_money(ytd_achieved),
            'yta_qtd': fmt_money(yta_qtd),
            'yol_ytd_target_ct':fmt_money(yol_ytd_target_ct),
            'yol_ytd_achieved':fmt_money(yol_ytd_achieved),
            'yol_revised_tot':fmt_money(yol_revised_tot),
            'yol_yta_ytd':fmt_money(yol_yta_ytd),
            'yol_sr':fmt_money(yol_sr),
            'yta_ytd': fmt_money(yta_ytd),
            'ytd_sr': fmt_money(ytd_sr),
            'qtd_sr': fmt_money(qtd_sr)
        })

    return slides if slides else "No data for that fiscal year for service"

# from datetime import datetime
# import frappe
# from frappe.utils import today

# @frappe.whitelist()
# def get_target_manager_data_for_services(service=None, month=None, fiscal_year=None):
#     # Set default month if not provided
#     if not month:
#         current_date = datetime.strptime(today(), '%Y-%m-%d')
#         month = datetime.strftime(current_date, '%b')  # Current month in short format
#     # Map months to numbers for SQL query
#     map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
#                   'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
#     # Convert month to the numeric format for querying
#     month_number = map_months.get(month)
#     slides = []
#     # Ensure year is specified
#     if not fiscal_year:
#         frappe.throw("Fiscal year is required")
    
#     # Use DATE_FORMAT to specify the exact date format in SQL
#     achieved_value = frappe.db.sql("""
#         SELECT SUM(total_sc_company_currency) AS total 
#         FROM `tabSales Invoice` 
#         WHERE services = %s 
#             AND DATE_FORMAT(creation, '%%m') = %s
#             AND DATE_FORMAT(creation, '%%Y') = %s 
#             AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#     """, (service, month_number, fiscal_year), as_dict=True)
#     services = frappe.get_doc("Services", service)
    

#     quarters = {
#         'Q1': ['Apr', 'May', 'Jun'],
#         'Q2': ['Jul', 'Aug', 'Sep'],
#         'Q3': ['Oct', 'Nov', 'Dec'],
#         'Q4': ['Jan', 'Feb', 'Mar']
#     }
#     fiscal_year_months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
    
    
#     # Determine the YTD months in the fiscal year up to the selected month
#     if month not in fiscal_year_months:
#         frappe.throw("Invalid month selection.")

#     months_up_to_selected = fiscal_year_months[:fiscal_year_months.index(month) + 1]
#     ytd_month_numbers = [map_months[m] for m in months_up_to_selected]

#     # Calculate QTD achieved based on selected month within the quarter
#     current_quarter = None
#     months_in_quarter = []
#     for quarter, months in quarters.items():
#         if month in months:
#             current_quarter = quarter
#             months_in_quarter = months[:months.index(month) + 1]  # Include months up to the selected month in the quarter
#             break

#     # Calculate QTD achieved
#     qtd_achieved = frappe.db.sql("""
#         SELECT SUM(total_sc_company_currency) AS total
#         FROM `tabSales Invoice`
#         WHERE services = %s
#             AND MONTH(creation) IN ({})
#             AND YEAR(creation) = %s
#             AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#     """.format(', '.join(months_in_quarter)), (service, fiscal_year), as_dict=True)[0].total or 0

#     # Calculate YTD achieved for the current fiscal year
#     ytd_achieved = frappe.db.sql("""
#         SELECT SUM(total_sc_company_currency) AS total
#         FROM `tabSales Invoice`
#         WHERE services = %s
#             AND MONTH(creation) IN ({})
#             AND YEAR(creation) = %s
#             AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#     """.format(', '.join(ytd_month_numbers)), (service, fiscal_year), as_dict=True)[0].total or 0

#     # Calculate YOL achieved for all previous fiscal years until the selected month
#     yol_month_numbers = [map_months[m] for m in fiscal_year_months]  # Include all months in the fiscal year for YOL calculation
#     yol_achieved = frappe.db.sql("""
#         SELECT SUM(total_sc_company_currency) AS total
#         FROM `tabSales Invoice`
#         WHERE services = %s
#             AND MONTH(creation) IN ({})
#             AND YEAR(creation) < %s
#             AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#     """.format(', '.join(yol_month_numbers)), (service, fiscal_year), as_dict=True)[0].total or 0



 


#     slides.append({
#         'achieved':achieved_value[0].total or 0,
#         'employee_image': services.logo,
#         'qtd_achieved':qtd_achieved[0].total or 0,
#         'ytd_achieved':ytd_achieved[0].total or 0,
#         'yol_achieved':yol_achieved[0].total or 0
#     })
#     if not slides:
#         return "No data for that fiscal year for service"
#     return slides

