# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
class TargetManager(Document):
    # pass
    def validate(self):
        incentive_eligibility = frappe.db.get_value("Employee",{'name':self.employee},'custom__invective_eligibility_group')
        if not incentive_eligibility:
            frappe.throw(f"Incentive Eligibility Group is not set for Employee {self.employee}")

            
        if self.target_child:
            tot_ct=0
            tot_tya=0
            tot_ach=0
            tot_revised_ct=0
            total_html=""

            company = frappe.db.get_value("Employee",{"name":self.employee},"company")
            points = frappe.db.get_value("Company Point and value",{"parent": company,"fiscal_year": self.custom_fiscal_year},"value")
            for i in self.target_child:
                if i.ct and i.ct>0:
                    tot_ct+=float(i.ct)
                if i.ct_yta and i.ct_yta>0:
                    tot_tya+=float(i.ct_yta)
                if i.achieved and i.achieved>0:
                    tot_ach+=float(i.achieved)
                if i.ct and i.ct>0:
                    tot_revised_ct+=float(i.ct)
            self.total_ct=tot_ct
            self.total_ct_achieved=tot_ach
            self.total_ct_yta= tot_ct - tot_ach
            self.custom_total_crtarget_inr = tot_revised_ct
            self.custom_sr = (tot_ach/tot_revised_ct)*100 if tot_revised_ct else 0

            self.custom_total_target_point = tot_ct / points
            self.custom_total_achieved_point = tot_ach / points
            self.custom_total_yta_target_point = (tot_ct - tot_ach) / points

            total_html=f"""

            <table>
            
            <tr>
            <td style="text-align:center; font-weight:bold; background-color:#0f1568;">Value/Points</td>
            <td style="text-align:center; font-weight:bold; background-color:#0f1568;">Total Target (INR)</td>
            <td style="text-align:center; font-weight:bold; background-color:#0f1568;">Total Achieved (INR)</td>
            <td style="text-align:center; font-weight:bold; background-color:#0f1568;">Total YTA Target (INR)</td>
            <td style="text-align:center; font-weight:bold; background-color:#0f1568;">SR%</td>
            </tr>
            
            <tr>
            <td style="text-align:center;">Value</td>
            <td style="text-align:right;">{tot_ct}</td>
            <td style="text-align:right;">{tot_ach}</td>
            <td style="text-align:right;">{tot_ct - tot_ach}</td>
            <td rowspan="2" style="text-align:center;" >{self.custom_sr}%</td>
            </tr>

            <tr>
            <td style="text-align:center;">Points</td>
            <td style="text-align:right;" >{tot_ct / points}</td>
            <td style="text-align:right;">{tot_ach / points}</td>
            <td style="text-align:right;">{(tot_ct - tot_ach) / points}</td>
            </tr>


            
            </table>
            
            """

            # self.custom_committed_target_html = total_html

        if (self.target_based_unit == "Sales Invoice" and self.based_on_service == 1 and self.based_on_candidate_owner == 1):
            reportees = [d.reportee for d in self.reportees] if self.reportees else []
            user_list = [self.user_id] + reportees
            user_tuple = tuple(user_list)
            so_pending = frappe.db.sql(
                f"""
                SELECT 
                    SUM(
                        COALESCE(custom_associate_payment_company_currency, 0) +
                        COALESCE(client_payment_company_currency, 0) +
                        COALESCE(candidate_payment_company_currenc, 0)
                    ) AS total_amount
                FROM `tabClosure`
                WHERE candidate_owner IN {user_tuple}
                AND so_created = 0
                AND nationality='Indian'
                AND status NOT IN ("Dropped", "Arrived")
                """
            )
            si_pending = frappe.db.sql(f"""
                SELECT 
                    COALESCE(SUM(s.base_total), 0) -
                    COALESCE(SUM(s.advance_paid), 0) AS pending_amount
                FROM `tabSales Order` s
                INNER JOIN `tabSales Order Item` si ON si.parent = s.name
                WHERE 
                    si.candidate_owner IN {user_tuple}
                    AND s.passport_number IS NOT NULL 
                    AND s.passport_number != ''
                    AND s.status IN ("To Bill", "To Deliver and Bill")
                    AND s.docstatus = 1
                    AND s.service="REC-I"
            """)
            self.si_pending=si_pending[0][0] if si_pending else 0
            self.so_pending = so_pending[0][0] or 0

        

   


@frappe.whitelist()
def test_method():
    # d = frappe.db.sql("select creation from `tabSales Invoice` where delivery_manager = account_manager and month(creation) = 2 ",as_dict=True)
    d = frappe.db.sql("select creation from `tabSales Order` where year(creation) = 6 ",as_dict=True)    
    print(d)

@frappe.whitelist()
def validate_fiscal_year(employee,year,target_based_unit,name):
    if frappe.db.exists("Target Manager",{'name':['!=',name],"employee":employee,"custom_fiscal_year":year,'target_based_unit':target_based_unit}):
        frappe.throw(f"Already target found for this employee for the year {year} based on {target_based_unit}")
        return "ok"



@frappe.whitelist()
def calculate_target_for_manager(name,emp,year):
    tps = frappe.get_all('Target Manager',{"custom_fiscal_year":year,"employee":emp},['*'])
    
    map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    
    mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
                      'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
    
    for tp in tps:
        doc = frappe.get_doc('Target Manager', tp.name)
        doc.target_child = []
        doc.monthly_ft_allocation=[]
        user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
        user_list = [user_id]
        for row in doc.reportees:
            user_list.append(row.reportee)
        user_list_sql = ", ".join(f"'{user}'" for user in user_list)
        service_list = []
        if doc.service_list:
            for serv in doc.service_list:
                service_list.append(serv.service)
        service_list_sql = ", ".join(f"'{ser}'" for ser in service_list)
        if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Order':
        # if tp.target_based_unit == 'Sales Order':
            pending_ct = 0
            pending_ft = 0
            ct=doc.annual_ct / 12
            ft=doc.annual_ft/12
            # Append the months and month numbers to the child table after clearing it
            for month in mapping_months:
                doc.append('target_child', {
                    'month': month,
                    'month_nos': map_months[month] , # Correct mapping for month_no
                    'ct':ct,
                })
            for m in mapping_months:
                doc.append('monthly_ft_allocation',{
                        'month': m,
                        'month_nos': map_months[m] , 
                        'ft':ft
                    })
            # Loop through the child table records
            for tc in doc.target_child:
                
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                # Get the user_id of the employee
                # Check if month is in first quarter (Jan to Mar)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
                    frappe.log_error(title='Target Manager',message=achieved_value)
                else:
                    # Otherwise, use custom year start date
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                    frappe.log_error(title='Target Manager',message=achieved_value)
                # Update values for revised_ct and revised_ft
                tc.revised_ct = tc.ct + pending_ct
                tc.achieved = achieved_value
                tc.ct_yta = tc.revised_ct - achieved_value
                tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
                pending_ct = tc.ct_yta
            for i in doc.monthly_ft_allocation:
                month = map_months.get(i.month)
                month_no = mapping_months.get(i.month)
                # Check if month is in first quarter (Jan to Mar)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                else:
                    # Otherwise, use custom year start date
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                # Update values for revised_ct and revised_ft
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                pending_ft = i.ftyta
                # Save document after changes
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit()
        # 
        if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Invoice':
            pending_ct = 0
            pending_ft = 0
            ct=doc.annual_ct / 12
            ft=doc.annual_ft/12
            for month in mapping_months:
                doc.append('target_child', {
                    'month': month,
                    'month_nos': map_months[month] , # Correct mapping for month_no
                    'ct':ct,
                })
            for m in mapping_months:
                doc.append('monthly_ft_allocation',{
                        'month': m,
                        'month_nos': map_months[m] , 
                        'ft':ft
                    })
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Invoice` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.posting_date) = %s 
                                AND YEAR(so.posting_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
                    frappe.log_error(title='Target Manager',message=achieved_value)
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Invoice` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.posting_date) = %s 
                                AND YEAR(so.posting_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                tc.revised_ct = tc.ct + pending_ct
                tc.achieved = achieved_value
                tc.ct_yta = tc.revised_ct - achieved_value
                tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
                pending_ct = tc.ct_yta
            for i in doc.monthly_ft_allocation:
                month = map_months.get(i.month)
                month_no = mapping_months.get(i.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Invoice` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.posting_date) = %s 
                                AND YEAR(so.posting_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Invoice` AS so
                                WHERE account_manager IN ({user_list_sql}) 
                                AND MONTH(so.posting_date) = %s 
                                AND YEAR(so.posting_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit()
        # elif tp.target_based_unit == 'Sales Invoice':
        #     pending_ct = 0
        #     pending_ft = 0
        #     ct=doc.annual_ct / 12
        #     ft=doc.annual_ft/12
        #     # Append the months and month numbers to the child table after clearing it
        #     for month in mapping_months:
        #         doc.append('target_child', {
        #             'month': month,
        #             'month_nos': map_months[month] , # Correct mapping for month_no
        #             'ct':ct,
        #             'ft':ft
        #         })
        #     for m in mapping_months:
        #         doc.append('monthly_ft_allocation',{
        #                 'month': m,
        #                 'month_nos': map_months[m] , 
        #                 'ft':ft
        #             })
        #     last_idx = len(doc.target_child) - 1
        #     for tc in doc.target_child:
        #         month = map_months.get(tc.month)
        #         month_no = mapping_months.get(tc.month)
        #         if month in ['01', '02', '03']:
        #             year = extract_year(tp.custom_year_end_date)
        #             query = f"""
        #                 SELECT SUM(base_total) AS total
        #                 FROM `tabSales Invoice`
        #                 WHERE account_manager IN ({user_list_sql})
        #                 AND MONTH(creation) = %s
        #                 AND YEAR(creation) = %s
        #                 AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
        #             """

        #             # Execute the query with parameters for month and year
        #             achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
        #         else:
        #             year = extract_year(tp.custom_year_start_date)
        #             query = f"""
        #                 SELECT SUM(base_total) AS total
        #                 FROM `tabSales Invoice`
        #                 WHERE account_manager IN ({user_list_sql})
        #                 AND MONTH(creation) = %s
        #                 AND YEAR(creation) = %s
        #                 AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
        #             """

        #             # Execute the query with parameters for month and year
        #             achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
        #         tc.revised_ct = tc.ct + pending_ct
        #         tc.achieved = achieved_value
        #         tc.ct_yta = tc.revised_ct - achieved_value
        #         tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
        #         pending_ct = tc.ct_yta
        #     for i in doc.monthly_ft_allocation:
        #         month = map_months.get(i.month)
        #         month_no = mapping_months.get(i.month)
        #         # Check if month is in first quarter (Jan to Mar)
        #         if month in ['01', '02', '03']:
        #             year = extract_year(tp.custom_year_end_date)
        #             query = f"""
        #                 SELECT SUM(base_total) AS total
        #                 FROM `tabSales Invoice`
        #                 WHERE account_manager IN ({user_list_sql})
        #                 AND MONTH(creation) = %s
        #                 AND YEAR(creation) = %s
        #                 AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
        #             """

        #             # Execute the query with parameters for month and year
        #             achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
        #         else:
        #             # Otherwise, use custom year start date
        #             year = extract_year(tp.custom_year_start_date)
        #             query = f"""
        #                 SELECT SUM(base_total) AS total
        #                 FROM `tabSales Invoice`
        #                 WHERE account_manager IN ({user_list_sql})
        #                 AND MONTH(creation) = %s
        #                 AND YEAR(creation) = %s
        #                 AND status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
        #             """
        #             achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
        #         i.cr_ft = i.ft + pending_ft
        #         i.f_achieved = achieved_value
        #         i.ftyta = i.cr_ft - achieved_value
        #         pending_ft = i.ftyta
        #         i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
        #         doc.save(ignore_permissions=True)
        #         frappe.db.commit()
        elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Invoice':
            pending_ct = 0
            pending_ft = 0
            ct=doc.annual_ct / 12
            ft=doc.annual_ft/12
            for month in mapping_months:
                doc.append('target_child', {
                    'month': month,
                    'month_nos': map_months[month] ,
                    'ct':ct,
                    'ft':ft
                })
            for m in mapping_months:
                doc.append('monthly_ft_allocation',{
                        'month': m,
                        'month_nos': map_months[m] , 
                        'ft':ft
                    })
            last_idx = len(doc.target_child) - 1
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    # Execute the query with parameters for month and year
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                tc.revised_ct = tc.ct + pending_ct
                tc.achieved = achieved_value
                tc.ct_yta = tc.revised_ct - achieved_value
                tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
                pending_ct = tc.ct_yta
            for i in doc.monthly_ft_allocation:
                month = map_months.get(i.month)
                month_no = mapping_months.get(i.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """

                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                pending_ft = i.ftyta
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        # 
        elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
            pending_ct = 0
            pending_ft = 0
            ct=doc.annual_ct / 12
            ft=doc.annual_ft/12
            for month in mapping_months:
                doc.append('target_child', {
                    'month': month,
                    'month_nos': map_months[month] ,
                    'ct':ct,
                    'ft':ft
                })
            for m in mapping_months:
                doc.append('monthly_ft_allocation',{
                        'month': m,
                        'month_nos': map_months[m] , 
                        'ft':ft
                    })
            last_idx = len(doc.target_child) - 1
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Order` AS si
                    WHERE MONTH(si.transaction_date) = %s
                    AND YEAR(si.transaction_date) = %s
                    AND si.service IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                    """
                    # Execute the query with parameters for month and year
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Order` AS si
                    WHERE MONTH(si.transaction_date) = %s
                    AND YEAR(si.transaction_date) = %s
                    AND si.service IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                tc.revised_ct = tc.ct + pending_ct
                tc.achieved = achieved_value
                tc.ct_yta = tc.revised_ct - achieved_value
                tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
                pending_ct = tc.ct_yta
            for i in doc.monthly_ft_allocation:
                month = map_months.get(i.month)
                month_no = mapping_months.get(i.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Order` AS si
                    WHERE MONTH(si.transaction_date) = %s
                    AND YEAR(si.transaction_date) = %s
                    AND si.service IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                    """

                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Order` AS si
                    WHERE MONTH(si.transaction_date) = %s
                    AND YEAR(si.transaction_date) = %s
                    AND si.service IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                pending_ft = i.ftyta
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        
    return 'OK'





@frappe.whitelist()
def calculate_target_for_manager_inso(doc,method):
    tps = frappe.get_all('Target Manager',['*'])
    
    map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    
    mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
                      'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
    
    for tp in tps:
        doc = frappe.get_doc('Target Manager', tp.name)
        doc.target_child = []
        doc.monthly_ft_allocation=[]
        user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
        user_list = [user_id]
        for row in doc.reportees:
            user_list.append(row.reportee)
        user_list_sql = ", ".join(f"'{user}'" for user in user_list)
        service_list = []
        if doc.service_list:
            for serv in doc.service_list:
                service_list.append(serv.service)
        service_list_sql = ", ".join(f"'{ser}'" for ser in service_list)
        if tp.based_on_account_manager==1:
            pending_ct = 0
            pending_ft = 0
            ct=doc.annual_ct / 12
            ft=doc.annual_ft/12
            # Append the months and month numbers to the child table after clearing it
            for month in mapping_months:
                doc.append('target_child', {
                    'month': month,
                    'month_nos': map_months[month] , # Correct mapping for month_no
                    'ct':ct,
                })
            for m in mapping_months:
                doc.append('monthly_ft_allocation',{
                        'month': m,
                        'month_nos': map_months[m] , 
                        'ft':ft
                    })
            # Loop through the child table records
            for tc in doc.target_child:
                
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                # Get the user_id of the employee
                # Check if month is in first quarter (Jan to Mar)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
                else:
                    # Otherwise, use custom year start date
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                # Update values for revised_ct and revised_ft
                tc.revised_ct = tc.ct + pending_ct
                tc.achieved = achieved_value
                tc.ct_yta = tc.revised_ct - achieved_value
                tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
                pending_ct = tc.ct_yta
            for i in doc.monthly_ft_allocation:
                month = map_months.get(i.month)
                month_no = mapping_months.get(i.month)
                # Check if month is in first quarter (Jan to Mar)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                else:
                    # Otherwise, use custom year start date
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    # Execute the query safely with parameters
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                # Update values for revised_ct and revised_ft
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit()
        
        elif tp.based_on_service ==1:
            pending_ct = 0
            pending_ft = 0
            ct=doc.annual_ct / 12
            ft=doc.annual_ft/12
            for month in mapping_months:
                doc.append('target_child', {
                    'month': month,
                    'month_nos': map_months[month] ,
                    'ct':ct,
                    'ft':ft
                })
            for m in mapping_months:
                doc.append('monthly_ft_allocation',{
                        'month': m,
                        'month_nos': map_months[m] , 
                        'ft':ft
                    })
            last_idx = len(doc.target_child) - 1
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    # Execute the query with parameters for month and year
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                tc.revised_ct = tc.ct + pending_ct
                tc.achieved = achieved_value
                tc.ct_yta = tc.revised_ct - achieved_value
                tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
                pending_ct = tc.ct_yta
            for i in doc.monthly_ft_allocation:
                month = map_months.get(i.month)
                month_no = mapping_months.get(i.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """

                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                    SELECT SUM(si.base_total) AS total
                    FROM `tabSales Invoice` AS si
                    WHERE MONTH(si.posting_date) = %s
                    AND YEAR(si.posting_date) = %s
                    AND si.services IN ({service_list_sql})
                    AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                pending_ft = i.ftyta
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        
    return 'OK'
# from datetime import datetime

# def extract_year(date_string):
#     date_object = datetime.strptime(date_string, '%Y-%m-%d')
#     return date_object.year
from datetime import datetime

def extract_year(date_input):
    if isinstance(date_input, str):
        date_object = datetime.strptime(date_input, '%Y-%m-%d')
    else:
        date_object = date_input
    return date_object.year




@frappe.whitelist()
def get_company_points(employee, fiscal_year):
    company = frappe.db.get_value("Employee", employee, "company")

    return frappe.db.get_value(
        "Company Point and value",
        {"parent": company, "fiscal_year": fiscal_year},
        "value"
    )


