import frappe
from datetime import datetime
from frappe import _
from frappe.utils import getdate, get_timespan_date_range,flt,today,nowdate,add_months,fmt_money
import json
from datetime import date, timedelta
import pandas as pd


@frappe.whitelist()
def get_ct_ft(fiscal_year):
    from datetime import datetime
    from frappe.utils import today
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

    # Get all Target Manager documents
    target_managers = frappe.db.get_all('Target Manager',{"custom_fiscal_year":fiscal_year} ,["*"])  
    slides = []

    # Loop through each Target Manager and fetch child table data
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
        yol_sr=0
        # Fetch child data for current month only
        child_data = frappe.db.get_all(
            'Target Child', 
            {'parent': doc.name, 'month': current_month}, 
            ['ct', 'achieved', 'ct_yta', 'revised_ct']
        )
        
        child_data1 = frappe.db.get_all(
            'Target FT Child',
            {"parent": doc.name, "month": current_month},
            ["ft", "cr_ft", "f_achieved", "ftyta"]
        )
        employee = frappe.get_doc("Employee", doc.employee)  # Fetch employee using the ID from Target Manager
        if employee.status == "Active":

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
                    # qtd_target_ct += round(data.ct,2) if data.ct else 0
                    qtd_target_ct += round(data.revised_ct) if data.revised_ct else 0
                    qtd_achieved += round(data.achieved) if data.achieved else 0
                    revised_qtd+=round(data.revised_ct) if data.revised_ct else 0
                    yta_qtd += round(data.ct_yta) if data.ct_yta else 0
                    if revised_qtd!= 0:
                        qtd_sr = round(((qtd_achieved / revised_qtd) * 100)) if revised_qtd else 0

            # Loop through fiscal year months and calculate YTD totals
            for month in months_to_include:
                ytd_data = frappe.db.get_all(
                    'Target Child', 
                    {'parent': doc.name, 'month': month}, 
                    ['ct', 'achieved', 'ct_yta', 'revised_ct']
                )
                for p in ytd_data:
                    # ytd_target_ct += round(p.ct,2) if p.ct else 0
                    ytd_target_ct += round(p.revised_ct) if p.revised_ct else 0
                    ytd_achieved += round(p.achieved) if p.achieved else 0
                    revised_tot+=round(p.revised_ct) if p.revised_ct else 0
                    yta_ytd += round(p.ct_yta) if p.ct_yta else 0
                    if revised_tot != 0:
                        ytd_sr = round(((ytd_achieved / revised_tot) * 100)) if revised_tot else 0
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
                    yol_ytd_achieved += round(p.achieved or 0) if p.achieved else 0
                    yol_revised_tot += round(p.revised_ct or 0)
                    yol_yta_ytd += round(p.ct_yta or 0) if p.ct_yta else 0
                    if yol_revised_tot!=0:
                        yol_sr = round(((yol_ytd_achieved / yol_revised_tot) * 100)) if yol_revised_tot else 0
            combined_data = []
            for i in range(max(len(child_data), len(child_data1))):
                entry = {}
                if i < len(child_data):
                    mtd_sr = round(((child_data[i].achieved / child_data[i].revised_ct) * 100),2) if child_data[i].revised_ct != 0 else 0
                    entry.update({
                        'ct': fmt_money(int(child_data[i].ct)) if child_data[i].ct is not None else 0,
                        'achieved': fmt_money(int(child_data[i].achieved)) if child_data[i].achieved is not None else 0,
                        'ct_yta': fmt_money(int(child_data[i].ct_yta)) if child_data[i].ct_yta is not None else 0,
                        'revised_ct': fmt_money(int(child_data[i].revised_ct)) if child_data[i].revised_ct is not None else 0,
                        'mtd_sr': mtd_sr
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
                    'manager': doc.name,  # Target Manager Document
                    'data': combined_data,  # Combined data from both child tables
                    'employee_name': employee.employee_name,
                    'employee_image': employee.image,
                    'employee_designation': employee.designation,
                    'target':doc.target_based_unit,
                    'fiscal_year': doc.custom_fiscal_year,
                    'annual_ct':  fmt_money((doc.annual_ct)),
                    'annual_ft': fmt_money((doc.annual_ft)),
                    'ytd_target_ct':fmt_money((ytd_target_ct)),
                    'qtd_target_ct':  fmt_money((qtd_target_ct)),
                    'qtd_achieved': fmt_money((qtd_achieved)),
                    'ytd_achieved': fmt_money((ytd_achieved)),
                    'yta_qtd':fmt_money((yta_qtd)),
                    'yta_ytd':fmt_money((yta_ytd)),
                    'ytd_sr':ytd_sr,
                    'qtd_sr':qtd_sr,
                    'yol_ytd_target_ct':fmt_money(yol_ytd_target_ct),
                    'yol_ytd_achieved':fmt_money(yol_ytd_achieved),
                    'yol_revised_tot':fmt_money(yol_revised_tot),
                    'yol_yta_ytd':fmt_money(yol_yta_ytd),
                    'yol_sr':fmt_money(yol_sr)
                })
                
    return slides





