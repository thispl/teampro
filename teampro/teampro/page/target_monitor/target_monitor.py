import frappe
from datetime import datetime
from frappe import _
from frappe.utils import getdate, get_timespan_date_range,flt,today,nowdate,add_months,fmt_money
import json
from datetime import date, timedelta
import pandas as pd

@frappe.whitelist()
def get_slide_attachments():
    try:
        doc = frappe.get_doc("Today Events", "Today Events")  # For single doctype, name = doctype name
    except frappe.DoesNotExistError:
        return []

    attachments = []

    for row in doc.events_details:
        if row.attach:
            file_doc = frappe.get_doc("File", {"file_url": row.attach})
            attachments.append({
                "file_url": file_doc.file_url,
                "file_name": file_doc.file_name
            })

    return attachments


    
# @frappe.whitelist()
# def get_ct_ft(fiscal_year):
#     from datetime import datetime
#     from frappe.utils import today
#     # Get current date information
#     date = datetime.strptime(today(), '%Y-%m-%d')
#     current_month = datetime.strftime(date, '%b')
    
#     # Define quarter months
#     quarters = {
#         'Q1': ['Apr', 'May', 'Jun'],
#         'Q2': ['Jul', 'Aug', 'Sep'],
#         'Q3': ['Oct', 'Nov', 'Dec'],
#         'Q4': ['Jan', 'Feb', 'Mar']
#     }

#     # Determine the quarter the current month falls into
#     current_quarter = None
#     for quarter, months in quarters.items():
#         if current_month in months:
#             current_quarter = quarter
#             break

#     # Get all Target Manager documents
#     target_managers = frappe.db.get_all('Target Manager',{"custom_fiscal_year":fiscal_year} ,["*"])  
#     slides = []

#     # Loop through each Target Manager and fetch child table data
#     for target in target_managers:
#         doc = frappe.get_doc('Target Manager', target['name'])
        
#         fiscal_year = doc.custom_fiscal_year
#         fiscal_year_months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
#         months_to_include = fiscal_year_months[:fiscal_year_months.index(current_month) + 1]
        
#         # Initialize variables for YTD and QTD
#         qtd_target_ct = 0  
#         qtd_achieved = 0  
#         ytd_target_ct = 0  
#         ytd_achieved = 0  
#         yta_qtd = 0  
#         yta_ytd = 0  
#         qtd_sr = 0  
#         ytd_sr = 0  
#         revised_tot=0
#         revised_qtd=0
#         yol_sr=0
#         # Fetch child data for current month only
#         child_data = frappe.db.get_all(
#             'Target Child', 
#             {'parent': doc.name, 'month': current_month}, 
#             ['ct', 'achieved', 'ct_yta', 'revised_ct']
#         )
        
#         child_data1 = frappe.db.get_all(
#             'Target FT Child',
#             {"parent": doc.name, "month": current_month},
#             ["ft", "cr_ft", "f_achieved", "ftyta"]
#         )
#         employee = frappe.get_doc("Employee", doc.employee)  # Fetch employee using the ID from Target Manager
#         if employee.status == "Active":

#             if current_quarter == 'Q3':  # For Quarter 3 (Oct, Nov, Dec)
#                 if current_month == 'Oct':
#                     # Add October, November, and December
#                     months_in_quarter = ['Oct', 'Nov', 'Dec']
#                 elif current_month == 'Nov':
#                     # Add November and December
#                     months_in_quarter = ['Oct', 'Nov', 'Dec']
#                 elif current_month == 'Dec':
#                     # Add December only
#                     months_in_quarter = ['Oct', 'Nov', 'Dec']
#                 # For other quarters (Q1, Q2, Q4), you can add similar logic if needed
#             if current_quarter == 'Q1':  # For Quarter 3 (Oct, Nov, Dec)
#                 if current_month == 'Apr':
#                     # Add October, November, and December
#                     months_in_quarter = ['Apr', 'May', 'Jun']
#                 elif current_month == 'May':
#                     # Add November and December
#                     months_in_quarter = ['Apr', 'May', 'Jun']
#                 elif current_month == 'Jun':
#                     # Add December only
#                     months_in_quarter = ['Apr', 'May', 'Jun']
#             if current_quarter == 'Q2':  # For Quarter 3 (Oct, Nov, Dec)
#                 if current_month == 'Jul':
#                     # Add October, November, and December
#                     months_in_quarter = ['Jul', 'Aug', 'Sep']
#                 elif current_month == 'Aug':
#                     # Add November and December
#                     months_in_quarter = ['Jul', 'Aug', 'Sep']
#                 elif current_month == 'Sep':
#                     # Add December only
#                     months_in_quarter = ['Jul', 'Aug', 'Sep']
#             if current_quarter == 'Q4':  # For Quarter 3 (Oct, Nov, Dec)
#                 if current_month == 'Jan':
#                     # Add October, November, and December
#                     months_in_quarter = ['Jan', 'Feb', 'Mar']
#                 elif current_month == 'Feb':
#                     # Add November and December
#                     months_in_quarter =['Jan', 'Feb', 'Mar']
#                 elif current_month == 'Mar':
#                     months_in_quarter =['Jan', 'Feb', 'Mar']


#             for month in months_in_quarter:

#                 quarter_data = frappe.db.get_all(
#                     'Target Child', 
#                     {'parent': doc.name, 'month': month}, 
#                     ['ct', 'achieved', 'ct_yta', 'revised_ct']
#                 )
#                 for data in quarter_data:
#                     # qtd_target_ct += round(data.ct,2) if data.ct else 0
#                     qtd_target_ct += round(data.revised_ct) if data.revised_ct else 0
#                     qtd_achieved += round(data.achieved) if data.achieved else 0
#                     revised_qtd+=round(data.revised_ct) if data.revised_ct else 0
#                     yta_qtd += round(data.ct_yta) if data.ct_yta else 0
#                     if revised_qtd!= 0:
#                         qtd_sr = round(((qtd_achieved / revised_qtd) * 100)) if revised_qtd else 0

#             # Loop through fiscal year months and calculate YTD totals
#             for month in months_to_include:
#                 ytd_data = frappe.db.get_all(
#                     'Target Child', 
#                     {'parent': doc.name, 'month': month}, 
#                     ['ct', 'achieved', 'ct_yta', 'revised_ct']
#                 )
#                 for p in ytd_data:
#                     # ytd_target_ct += round(p.ct,2) if p.ct else 0
#                     ytd_target_ct += round(p.revised_ct) if p.revised_ct else 0
#                     ytd_achieved += round(p.achieved) if p.achieved else 0
#                     revised_tot+=round(p.revised_ct) if p.revised_ct else 0
#                     yta_ytd += round(p.ct_yta) if p.ct_yta else 0
#                     if revised_tot != 0:
#                         ytd_sr = round(((ytd_achieved / revised_tot) * 100)) if revised_tot else 0
#             yol_ytd_target_ct = yol_ytd_achieved = yol_revised_tot = yol_yta_ytd = 0
#             for m in fiscal_year_months:
#                 # Retrieve data for each month in the YOL calculation
#                 yol_data = frappe.db.get_all(
#                     'Target Child', 
#                     {'parent': doc.name, 'month': m}, 
#                     ['ct', 'achieved', 'ct_yta', 'revised_ct']
#                 )
                
#                 # Summing up the values to calculate YOL totals
#                 for p in yol_data:
#                     yol_ytd_target_ct += round(p.revised_ct or 0)
#                     yol_ytd_achieved += round(p.achieved or 0) if p.achieved else 0
#                     yol_revised_tot += round(p.revised_ct or 0)
#                     yol_yta_ytd += round(p.ct_yta or 0) if p.ct_yta else 0
#                     if yol_revised_tot!=0:
#                         yol_sr = round(((yol_ytd_achieved / yol_revised_tot) * 100)) if yol_revised_tot else 0
#             combined_data = []
#             for i in range(max(len(child_data), len(child_data1))):
#                 entry = {}
#                 if i < len(child_data):
#                     mtd_sr = round(((child_data[i].achieved / child_data[i].revised_ct) * 100),2) if child_data[i].revised_ct != 0 else 0
#                     entry.update({
#                         'ct': fmt_money(int(child_data[i].ct)) if child_data[i].ct is not None else 0,
#                         'achieved': fmt_money(int(child_data[i].achieved)) if child_data[i].achieved is not None else 0,
#                         'ct_yta': fmt_money(int(child_data[i].ct_yta)) if child_data[i].ct_yta is not None else 0,
#                         'revised_ct': fmt_money(int(child_data[i].revised_ct)) if child_data[i].revised_ct is not None else 0,
#                         'mtd_sr': mtd_sr
#                     })
#                 if i < len(child_data1):
#                     entry.update({
#                         'ft': round(child_data1[i].ft, 2) if child_data1[i].ft is not None else 0,
#                         'cr_ft': round(child_data1[i].cr_ft, 2) if child_data1[i].cr_ft is not None else 0,
#                         'f_achieved': round(child_data1[i].f_achieved, 2) if child_data1[i].f_achieved is not None else 0,
#                         'ftyta': round(child_data1[i].ftyta, 2) if child_data1[i].ftyta is not None else 0
#                     })
#                 combined_data.append(entry)

#                 slides.append({
#                     'manager': doc.name,  # Target Manager Document
#                     'data': combined_data,  # Combined data from both child tables
#                     'employee_name': employee.employee_name,
#                     'employee_image': employee.image,
#                     'employee_designation': employee.designation,
#                     'target':doc.target_based_unit,
#                     'fiscal_year': doc.custom_fiscal_year,
#                     'annual_ct':  fmt_money((doc.annual_ct)),
#                     'annual_ft': fmt_money((doc.annual_ft)),
#                     'ytd_target_ct':fmt_money((ytd_target_ct)),
#                     'qtd_target_ct':  fmt_money((qtd_target_ct)),
#                     'qtd_achieved': fmt_money((qtd_achieved)),
#                     'ytd_achieved': fmt_money((ytd_achieved)),
#                     'yta_qtd':fmt_money((yta_qtd)),
#                     'yta_ytd':fmt_money((yta_ytd)),
#                     'ytd_sr':ytd_sr,
#                     'qtd_sr':qtd_sr,
#                     'yol_ytd_target_ct':fmt_money(yol_ytd_target_ct),
#                     'yol_ytd_achieved':fmt_money(yol_ytd_achieved),
#                     'yol_revised_tot':fmt_money(yol_revised_tot),
#                     'yol_yta_ytd':fmt_money(yol_yta_ytd),
#                     'yol_sr':fmt_money(yol_sr)
#                 })
                
#     return slides




@frappe.whitelist()
def get_ct_ft(fiscal_year, employee=None, department=None, service=None):

    from datetime import datetime
    from frappe.utils import today
    from frappe.utils.data import fmt_money

    # Get current date
    date = datetime.strptime(today(), '%Y-%m-%d')
    current_month = datetime.strftime(date, '%b')


    filters = {"custom_fiscal_year": fiscal_year}

    if employee:
        filters["employee"] = employee

    if department:
        filters["department"] = department

    if service:
        filters["service"] = service


    month_map = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    quarters = {
        'Q1': ['Apr', 'May', 'Jun'],
        'Q2': ['Jul', 'Aug', 'Sep'],
        'Q3': ['Oct', 'Nov', 'Dec'],
        'Q4': ['Jan', 'Feb', 'Mar']
    }

    current_quarter = None

    for quarter, months in quarters.items():
        if current_month in months:
            current_quarter = quarter
            break

    frappe.log_error(str(filters), "Target Monitor Filters")

    target_managers = frappe.db.get_all(
        "Target Manager",
        filters,
        ["*"]
    )


    slides = []

    for target in target_managers:

        doc = frappe.get_doc('Target Manager', target['name'])

        employee = frappe.get_doc("Employee", doc.employee)
    

        if employee.status != "Active":
            continue

        fiscal_year_months = [
            'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec',
            'Jan', 'Feb', 'Mar'
        ]

        fy = frappe.get_doc("Fiscal Year", fiscal_year)

        from_date = fy.year_start_date
        to_date = fy.year_end_date

        months_to_include = fiscal_year_months[
            :fiscal_year_months.index(current_month) + 1
        ]

        # Quarter Months
        months_in_quarter = quarters.get(current_quarter, [])

        qtd_target_ct = 0
        qtd_achieved = 0
        ytd_target_ct = 0
        ytd_achieved = 0

        yta_qtd = 0
        yta_ytd = 0

        qtd_sr = 0
        ytd_sr = 0
        yol_sr = 0

        revised_tot = 0
        revised_qtd = 0

        # NEW VARIABLES
        ep_score = 0
        nc_score = 0

        qtd_ep_score = 0
        qtd_nc_score = 0

        ytd_ep_score = 0
        ytd_nc_score = 0


        child_data = frappe.db.get_all(
            'Target Child',
            {
                'parent': doc.name,
                'month': current_month
            },
            ['ct', 'achieved', 'ct_yta', 'revised_ct']
        )

        child_data1 = frappe.db.get_all(
            'Target FT Child',
            {
                "parent": doc.name,
                "month": current_month
            },
            ["ft", "cr_ft", "f_achieved", "ftyta"]
        )

        # CURRENT MONTH EP & NC

        current_month_no = month_map[current_month]

        ep_score = frappe.db.sql("""
            SELECT IFNULL(SUM(energy_score), 0)
            FROM `tabEnergy Point And Non Conformity`
            WHERE emp = %s
            AND docstatus = 1
            AND MONTH(creation) = %s
            AND DATE(creation) BETWEEN %s AND %s
        """, (
            doc.employee,
            current_month_no,
            from_date,
            to_date
        ))[0][0] or 0


        nc_score = frappe.db.sql("""
            SELECT IFNULL(SUM(nc_score), 0)
            FROM `tabEnergy Point And Non Conformity`
            WHERE emp = %s
            AND docstatus = 1
            AND MONTH(creation) = %s
            AND DATE(creation) BETWEEN %s AND %s
        """, (
            doc.employee,
            current_month_no,
            from_date,
            to_date
        ))[0][0] or 0
    


        # QTD CALCULATION

        for month in months_in_quarter:

            quarter_data = frappe.db.get_all(
                'Target Child',
                {
                    'parent': doc.name,
                    'month': month
                },
                ['ct', 'achieved', 'ct_yta', 'revised_ct']
            )

            for data in quarter_data:

                qtd_target_ct += round(data.revised_ct or 0)
                qtd_achieved += round(data.achieved or 0)
                revised_qtd += round(data.revised_ct or 0)
                yta_qtd += round(data.ct_yta or 0)


            month_no = month_map[month]

            qtd_ep = frappe.db.sql("""
                SELECT IFNULL(SUM(energy_score), 0)
                FROM `tabEnergy Point And Non Conformity`
                WHERE emp = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (doc.employee, month_no, from_date, to_date))[0][0] or 0

            qtd_ep_score += qtd_ep


            qtd_nc = frappe.db.sql("""
                SELECT IFNULL(SUM(nc_score), 0)
                FROM `tabEnergy Point And Non Conformity`
                WHERE emp = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (doc.employee, month_no, from_date, to_date))[0][0] or 0

            qtd_nc_score += qtd_nc

        if revised_qtd != 0:
            qtd_sr = round((qtd_achieved / revised_qtd) * 100)

        # YTD CALCULATION
        for month in months_to_include:

            ytd_data = frappe.db.get_all(
                'Target Child',
                {
                    'parent': doc.name,
                    'month': month
                },
                ['ct', 'achieved', 'ct_yta', 'revised_ct']
            )

            for p in ytd_data:

                ytd_target_ct += round(p.revised_ct or 0)
                ytd_achieved += round(p.achieved or 0)
                revised_tot += round(p.revised_ct or 0)
                yta_ytd += round(p.ct_yta or 0)

            # YTD EP
            month_no = month_map[month]

            # YTD EP
            ytd_ep = frappe.db.sql("""
                SELECT IFNULL(SUM(energy_score), 0)
                FROM `tabEnergy Point And Non Conformity`
                WHERE emp = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (doc.employee, month_no, from_date, to_date))[0][0] or 0

            ytd_ep_score += ytd_ep


            # YTD NC
            ytd_nc = frappe.db.sql("""
                SELECT IFNULL(SUM(nc_score), 0)
                FROM `tabEnergy Point And Non Conformity`
                WHERE emp = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (doc.employee, month_no, from_date, to_date))[0][0] or 0

            ytd_nc_score += ytd_nc

        if revised_tot != 0:
            ytd_sr = round((ytd_achieved / revised_tot) * 100)

        # =========================
        # YOL CALCULATION
        # =========================

        yol_ytd_target_ct = 0
        yol_ytd_achieved = 0
        yol_revised_tot = 0
        yol_yta_ytd = 0
        yol_ep_score = 0
        yol_nc_score = 0

        for m in fiscal_year_months:

            yol_data = frappe.db.get_all(
                'Target Child',
                {
                    'parent': doc.name,
                    'month': m
                },
                ['ct', 'achieved', 'ct_yta', 'revised_ct']
            )

            for p in yol_data:

                yol_ytd_target_ct += round(p.revised_ct or 0)
                yol_ytd_achieved += round(p.achieved or 0)
                yol_revised_tot += round(p.revised_ct or 0)
                yol_yta_ytd += round(p.ct_yta or 0)
            

            month_no = month_map[m]

            yol_ep = frappe.db.sql("""
                SELECT IFNULL(SUM(energy_score),0)
                FROM `tabEnergy Point And Non Conformity`
                WHERE emp = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (doc.employee, month_no, from_date, to_date))[0][0] or 0

            yol_ep_score += yol_ep


            # YOL NC
            yol_nc = frappe.db.sql("""
                SELECT IFNULL(SUM(nc_score),0)
                FROM `tabEnergy Point And Non Conformity`
                WHERE emp = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (doc.employee, month_no, from_date, to_date))[0][0] or 0

            yol_nc_score += yol_nc

        if yol_revised_tot != 0:
            yol_sr = round((yol_ytd_achieved / yol_revised_tot) * 100)

        # =========================
        # COMBINED DATA
        # =========================

        combined_data = []

        for i in range(max(len(child_data), len(child_data1))):

            entry = {}

            if i < len(child_data):

                mtd_sr = round(
                    (
                        child_data[i].achieved /
                        child_data[i].revised_ct
                    ) * 100,
                    2
                ) if child_data[i].revised_ct else 0

                entry.update({

                    'ct': fmt_money(int(child_data[i].ct), precision=0)
                    if child_data[i].ct else 0,

                    'achieved': fmt_money(int(child_data[i].achieved), precision=0)
                    if child_data[i].achieved else 0,

                    'ct_yta': fmt_money(int(child_data[i].ct_yta), precision=0)
                    if child_data[i].ct_yta else 0,

                    'revised_ct': fmt_money(int(child_data[i].revised_ct), precision=0)
                    if child_data[i].revised_ct else 0,

                    'mtd_sr': mtd_sr
                })

            if i < len(child_data1):

                entry.update({

                    'ft': round(child_data1[i].ft or 0, 2),

                    'cr_ft': round(child_data1[i].cr_ft or 0, 2),

                    'f_achieved': round(child_data1[i].f_achieved or 0, 2),

                    'ftyta': round(child_data1[i].ftyta or 0, 2)
                })

            combined_data.append(entry)

        # =========================
        # PR SCORE
        # =========================

        # MTD PR
        mtd_pr = frappe.db.sql("""
            SELECT IFNULL(SUM(total_score),0)
            FROM `tabAppraisal`
            WHERE employee = %s
            AND docstatus = 1
            AND MONTH(creation) = %s
            AND DATE(creation) BETWEEN %s AND %s
        """, (
            doc.employee,
            current_month_no,
            from_date,
            to_date
        ))[0][0] or 0


        # QTD PR
        qtd_pr = 0

        for month in months_in_quarter:

            month_no = month_map[month]

            pr = frappe.db.sql("""
                SELECT IFNULL(SUM(total_score),0)
                FROM `tabAppraisal`
                WHERE employee = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (
                doc.employee,
                month_no,
                from_date,
                to_date
            ))[0][0] or 0

            qtd_pr += pr


        # YTD PR
        ytd_pr = 0

        for month in months_to_include:

            month_no = month_map[month]

            pr = frappe.db.sql("""
                SELECT IFNULL(SUM(total_score),0)
                FROM `tabAppraisal`
                WHERE employee = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (
                doc.employee,
                month_no,
                from_date,
                to_date
            ))[0][0] or 0

            ytd_pr += pr


        # YOL PR
        yol_pr = 0

        for month in fiscal_year_months:

            month_no = month_map[month]

            pr = frappe.db.sql("""
                SELECT IFNULL(SUM(total_score),0)
                FROM `tabAppraisal`
                WHERE employee = %s
                AND docstatus = 1
                AND MONTH(creation) = %s
                AND DATE(creation) BETWEEN %s AND %s
            """, (
                doc.employee,
                month_no,
                from_date,
                to_date
            ))[0][0] or 0

            yol_pr += pr



        mtd_prs = round((mtd_pr / 5) * 100, 2) if mtd_pr else 0

        qtd_prs = round((qtd_pr / 5) * 100, 2) if qtd_pr else 0

        ytd_prs = round((ytd_pr / 5) * 100, 2) if ytd_pr else 0

        yol_prs = round((yol_pr / 5) * 100, 2) if yol_pr else 0



        # MTD TES
        mtd_total = (ep_score or 0) + (nc_score or 0)

        if mtd_total > 10:
            mtd_tes = 100
        elif mtd_total >= 5:
            mtd_tes = 75
        elif mtd_total >= 0:
            mtd_tes = 50
        elif mtd_total >= -3:
            mtd_tes = 25
        else:
            mtd_tes = 0


        # QTD TES
        qtd_total = (qtd_ep_score or 0) + (qtd_nc_score or 0)

        if qtd_total > 10:
            qtd_tes = 100
        elif qtd_total >= 5:
            qtd_tes = 75
        elif qtd_total >= 0:
            qtd_tes = 50
        elif qtd_total >= -3:
            qtd_tes = 25
        else:
            qtd_tes = 0


        # YTD TES
        ytd_total = (ytd_ep_score or 0) + (ytd_nc_score or 0)

        if ytd_total > 10:
            ytd_tes = 100
        elif ytd_total >= 5:
            ytd_tes = 75
        elif ytd_total >= 0:
            ytd_tes = 50
        elif ytd_total >= -3:
            ytd_tes = 25
        else:
            ytd_tes = 0


        # YOL TES
        yol_total = (yol_ep_score or 0) + (yol_nc_score or 0)

        if yol_total > 10:
            yol_tes = 100
        elif yol_total >= 5:
            yol_tes = 75
        elif yol_total >= 0:
            yol_tes = 50
        elif yol_total >= -3:
            yol_tes = 25
        else:
            yol_tes = 0


        mtd_performance_index = round(
            (
                (float(mtd_sr) * 0.4) +
                (float(mtd_tes) * 0.3) +
                (float(mtd_prs) * 0.3)
            ),
            2
        )

        qtd_performance_index = round(
            (
                (float(qtd_sr) * 0.4) +
                (float(qtd_tes) * 0.3) +
                (float(qtd_prs) * 0.3)
            ),
            2
        )

        ytd_performance_index = round(
            (
                (float(ytd_sr) * 0.4) +
                (float(ytd_tes) * 0.3) +
                (float(ytd_prs) * 0.3)
            ),
            2
        )

        yol_performance_index = round(
            (
                (float(yol_sr) * 0.4) +
                (float(yol_tes) * 0.3) +
                (float(yol_prs) * 0.3)
            ),
            2
        )

        mtd_performance_label = get_performance_label(mtd_performance_index)

        qtd_performance_label = get_performance_label(qtd_performance_index)

        ytd_performance_label = get_performance_label(ytd_performance_index)

        yol_performance_label = get_performance_label(yol_performance_index)

        

        slides.append({

            'manager': doc.name,

            'data': combined_data,

            'employee_name': employee.employee_name,

            'employee_image': employee.image,

            'employee_designation': employee.designation,

            'target': doc.target_based_unit,

            'fiscal_year': doc.custom_fiscal_year,

            'annual_ct': fmt_money(doc.annual_ct, precision=0),

            'annual_ft': fmt_money(doc.annual_ft),

            # QTD
            'qtd_target_ct': fmt_money(qtd_target_ct, precision=0),
            'qtd_achieved': fmt_money(qtd_achieved, precision=0),
            'yta_qtd': fmt_money(yta_qtd, precision=0),
            'qtd_sr': qtd_sr,
            'qtd_ep_score': qtd_ep_score,
            'qtd_nc_score': qtd_nc_score,

            # YTD
            'ytd_target_ct': fmt_money(ytd_target_ct, precision=0),
            'ytd_achieved': fmt_money(ytd_achieved, precision=0),
            'yta_ytd': fmt_money(yta_ytd, precision=0),
            'ytd_sr': ytd_sr,
            'ytd_ep_score': ytd_ep_score,
            'ytd_nc_score': ytd_nc_score,

            # YOL
            'yol_ytd_target_ct': fmt_money(yol_ytd_target_ct, precision=0),
            'yol_ytd_achieved': fmt_money(yol_ytd_achieved, precision=0),
            'yol_revised_tot': fmt_money(yol_revised_tot, precision=0),
            'yol_yta_ytd': fmt_money(yol_yta_ytd, precision=0),
            'yol_sr': yol_sr,
            'yol_ep_score': yol_ep_score,
            'yol_nc_score': yol_nc_score,

            # CURRENT MONTH
            'ep': ep_score,
            'nc': nc_score,


            # TES
            'mtd_tes': mtd_tes,
            'qtd_tes': qtd_tes,
            'ytd_tes': ytd_tes,
            'yol_tes': yol_tes,

            # PR
            'mtd_pr': round(mtd_pr, 2),
            'qtd_pr': round(qtd_pr, 2),
            'ytd_pr': round(ytd_pr, 2),
            'yol_pr': round(yol_pr, 2),

            # PRS
            'mtd_prs': mtd_prs,
            'qtd_prs': qtd_prs,
            'ytd_prs': ytd_prs,
            'yol_prs': yol_prs,


            'mtd_performance_index': mtd_performance_index,
            'qtd_performance_index': qtd_performance_index,
            'ytd_performance_index': ytd_performance_index,
            'yol_performance_index': yol_performance_index,

            'mtd_performance_label': mtd_performance_label,
            'qtd_performance_label': qtd_performance_label,
            'ytd_performance_label': ytd_performance_label,
            'yol_performance_label': yol_performance_label,

            'employee': doc.employee,
            'department': doc.department,
        })

    return slides


def get_performance_label(score):

    if score >= 100:
        return "Outstanding"

    elif score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"
    
    elif score >= 30:
        return "Average"

    else:
        return "Needs Improvement"