import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta

# @frappe.whitelist()
# def calculate_target_for_manager_test(name,emp,year):
#     def get_month_range(start_date, end_date):
#         current = start_date.replace(day=1)
#         end = end_date.replace(day=1)
#         months = []
#         while current <= end:
#             months.append(current)
#             current += relativedelta(months=1)
#         return months

#     tps = frappe.get_all('Target Manager',{"custom_fiscal_year":year,"employee":emp},['*'])
    
#     map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
#                   'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    
#     mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
#                       'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
    
#     for tp in tps:
#         doc = frappe.get_doc('Target Manager', tp.name)
#         doc.target_child = []
#         doc.monthly_ft_allocation=[]
#         user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
#         user_list = [user_id]
#         for row in doc.reportees:
#             user_list.append(row.reportee)
#         user_list_sql = ", ".join(f"'{user}'" for user in user_list)
#         service_list = []
#         if doc.service_list:
#             for serv in doc.service_list:
#                 service_list.append(serv.service)
#         service_list_sql = ", ".join(f"'{ser}'" for ser in service_list)
#         if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Order':
#             pending_ct = 0
#             pending_ft = 0
#             start_date = tp.custom_year_start_date
#             end_date = tp.custom_year_end_date

#             months = get_month_range(start_date, end_date)
#             num_months = len(months)
#             ct = doc.annual_ct / num_months if num_months else 0
#             ft = doc.annual_ft / num_months if num_months else 0
#             for dt in months:
#                 month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
#                 month_num = dt.strftime('%m')   # '01', '02', etc.

#                 doc.append('target_child', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ct': ct
#                 })
#                 doc.append('monthly_ft_allocation', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ft': ft
#                 })
           
#             total_months = len(doc.target_child)
#             for tc in doc.target_child:
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 tc.revised_ct = tc.ct + pending_ct
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
#                 pending_ct = tc.ct_yta
#             for i in doc.monthly_ft_allocation:
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 i.cr_ft = i.ft + pending_ft
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 pending_ft = i.ftyta
#                 # Save document after changes
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit()
#         # 
#         if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Invoice':
#             pending_ct = 0
#             pending_ft = 0
#             start_date = tp.custom_year_start_date
#             end_date = tp.custom_year_end_date

#             months = get_month_range(start_date, end_date)
#             num_months = len(months)
#             ct = doc.annual_ct / num_months if num_months else 0
#             ft = doc.annual_ft / num_months if num_months else 0
#             for dt in months:
#                 month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
#                 month_num = dt.strftime('%m')   # '01', '02', etc.

#                 doc.append('target_child', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ct': ct
#                 })
#                 doc.append('monthly_ft_allocation', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ft': ft
#                 })
           
#             total_months = len(doc.target_child)
#             revised_ct_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for tc in doc.target_child:
#                 tc.revised_ct = tc.ct
#                 revised_ct_list.append(tc)
#             revised_ft_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for i in doc.monthly_ft_allocation:
#                 i.cr_ft = i.ft
#                 revised_ft_list.append(i)
#             for idx, tc in enumerate(revised_ct_list):
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
#                 pending_ct = tc.ct_yta
#                 remaining = revised_ct_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ct = pending_ct / num_remaining
#                     for next_tc in remaining:
#                         next_tc.revised_ct += redistributed_ct
#             for idx, i in enumerate(revised_ft_list):
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 pending_ft = i.ftyta
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 remaining = revised_ft_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ft = pending_ft / num_remaining
#                     for next_tc in remaining:
#                         next_tc.cr_ft += redistributed_ft
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit()
       
#         elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Invoice':
#             pending_ct = 0
#             pending_ft = 0
#             start_date = tp.custom_year_start_date
#             end_date = tp.custom_year_end_date

#             months = get_month_range(start_date, end_date)
#             num_months = len(months)
#             ct = doc.annual_ct / num_months if num_months else 0
#             ft = doc.annual_ft / num_months if num_months else 0
#             for dt in months:
#                 month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
#                 month_num = dt.strftime('%m')   # '01', '02', etc.

#                 doc.append('target_child', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ct': ct
#                 })
#                 doc.append('monthly_ft_allocation', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ft': ft
#                 })
            
#             total_months = len(doc.target_child)
#             revised_ct_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for tc in doc.target_child:
#                 tc.revised_ct = tc.ct
#                 revised_ct_list.append(tc)
#             revised_ft_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for i in doc.monthly_ft_allocation:
#                 i.cr_ft = i.ft
#                 revised_ft_list.append(i)
#             for idx, tc in enumerate(revised_ct_list):
#             # for idx, tc in enumerate(doc.target_child):
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
                    
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr = (achieved_value / tc.revised_ct) * 100 if tc.revised_ct else 0

#                 pending_ct = tc.ct_yta
#                 remaining = revised_ct_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ct = pending_ct / num_remaining
#                     for next_tc in remaining:
#                         next_tc.revised_ct += redistributed_ct

          
#             for idx, i in enumerate(revised_ft_list):
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """

#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 pending_ft = i.ftyta
#                 remaining = revised_ft_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ft = pending_ft / num_remaining
#                     for next_tc in remaining:
#                         next_tc.cr_ft += redistributed_ft
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit() 
#         # 
#         elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
#             pending_ct = 0
#             pending_ft = 0
#             start_date = tp.custom_year_start_date
#             end_date = tp.custom_year_end_date

#             months = get_month_range(start_date, end_date)
#             num_months = len(months)
#             ct = doc.annual_ct / num_months if num_months else 0
#             ft = doc.annual_ft / num_months if num_months else 0
#             for dt in months:
#                 month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
#                 month_num = dt.strftime('%m')   # '01', '02', etc.

#                 doc.append('target_child', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ct': ct
#                 })
#                 doc.append('monthly_ft_allocation', {
#                     'month': month_name,
#                     'month_nos': month_num,
#                     'ft': ft
#                 })
#             total_months = len(doc.target_child)
#             revised_ct_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for tc in doc.target_child:
#                 tc.revised_ct = tc.ct
#                 revised_ct_list.append(tc)
#             revised_ft_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for i in doc.monthly_ft_allocation:
#                 i.cr_ft = i.ft
#                 revised_ft_list.append(i)
#             last_idx = len(doc.target_child) - 1
#             for idx, tc in enumerate(revised_ct_list):
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """
#                     # Execute the query with parameters for month and year
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
                    
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
#                 pending_ct = tc.ct_yta
#                 remaining = revised_ct_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ct = pending_ct / num_remaining
#                     for next_tc in remaining:
#                         next_tc.revised_ct += redistributed_ct
#             for idx, i in enumerate(revised_ft_list):
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """

#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 pending_ft = i.ftyta
#                 remaining = revised_ft_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ft = pending_ft / num_remaining
#                     for next_tc in remaining:
#                         next_tc.cr_ft += redistributed_ft
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit() 
        
#     return 'OK'

from datetime import datetime

def extract_year(date_input):
    if isinstance(date_input, str):
        date_object = datetime.strptime(date_input, '%Y-%m-%d')
    else:
        date_object = date_input
    return date_object.year

# @frappe.whitelist()
# def calculate_target_for_manager_inso_test(doc,method):
#     tps = frappe.get_all('Target Manager',['*'])
    
#     map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
#                   'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    
#     mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
#                       'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
    
#     for tp in tps:
#         doc = frappe.get_doc('Target Manager', tp.name)
#         doc.target_child = []
#         doc.monthly_ft_allocation=[]
#         user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
#         user_list = [user_id]
#         for row in doc.reportees:
#             user_list.append(row.reportee)
#         user_list_sql = ", ".join(f"'{user}'" for user in user_list)
#         service_list = []
#         if doc.service_list:
#             for serv in doc.service_list:
#                 service_list.append(serv.service)
#         service_list_sql = ", ".join(f"'{ser}'" for ser in service_list)
#         if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Order':
#             pending_ct = 0
#             pending_ft = 0
#             ct=doc.annual_ct / 12
#             ft=doc.annual_ft/12
#             for month in mapping_months:
#                 doc.append('target_child', {
#                     'month': month,
#                     'month_nos': map_months[month] , # Correct mapping for month_no
#                     'ct':ct,
#                 })
#             for m in mapping_months:
#                 doc.append('monthly_ft_allocation',{
#                         'month': m,
#                         'month_nos': map_months[m] , 
#                         'ft':ft
#                     })
#             total_months = len(doc.target_child)
#             revised_ct_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for tc in doc.target_child:
#                 tc.revised_ct = tc.ct
#                 revised_ct_list.append(tc)
#             revised_ft_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for i in doc.monthly_ft_allocation:
#                 i.cr_ft = i.ft
#                 revised_ft_list.append(i)
#             for idx, tc in enumerate(revised_ct_list):
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
#                 pending_ct = tc.ct_yta
#                 remaining = revised_ct_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ct = pending_ct / num_remaining
#                     for next_tc in remaining:
#                         next_tc.revised_ct += redistributed_ct
#             for idx, i in enumerate(revised_ft_list):
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Order` AS so
#                                 WHERE account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.transaction_date) = %s 
#                                 AND YEAR(so.transaction_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 pending_ft = i.ftyta
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 remaining = revised_ft_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ft = pending_ft / num_remaining
#                     for next_tc in remaining:
#                         next_tc.cr_ft += redistributed_ft
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit()
#         # 
#         if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Invoice':
#             pending_ct = 0
#             pending_ft = 0
#             ct=doc.annual_ct / 12
#             ft=doc.annual_ft/12
#             for month in mapping_months:
#                 doc.append('target_child', {
#                     'month': month,
#                     'month_nos': map_months[month] , # Correct mapping for month_no
#                     'ct':ct,
#                 })
#             for m in mapping_months:
#                 doc.append('monthly_ft_allocation',{
#                         'month': m,
#                         'month_nos': map_months[m] , 
#                         'ft':ft
#                     })
#             total_months = len(doc.target_child)
#             revised_ct_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for tc in doc.target_child:
#                 tc.revised_ct = tc.ct
#                 revised_ct_list.append(tc)
#             revised_ft_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for i in doc.monthly_ft_allocation:
#                 i.cr_ft = i.ft
#                 revised_ft_list.append(i)
#             for idx, tc in enumerate(revised_ct_list):
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
#                 pending_ct = tc.ct_yta
#                 remaining = revised_ct_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ct = pending_ct / num_remaining
#                     for next_tc in remaining:
#                         next_tc.revised_ct += redistributed_ct
#             for idx, i in enumerate(revised_ft_list):
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE so.account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                                 SELECT SUM(so.base_total) AS total 
#                                 FROM `tabSales Invoice` AS so
#                                 WHERE account_manager IN ({user_list_sql}) 
#                                 AND MONTH(so.posting_date) = %s 
#                                 AND YEAR(so.posting_date) = %s 
#                                 AND so.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                                 """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 pending_ft = i.ftyta
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 remaining = revised_ft_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ft = pending_ft / num_remaining
#                     for next_tc in remaining:
#                         next_tc.cr_ft += redistributed_ft
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit()
       
#         elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Invoice':
#             pending_ct = 0
#             pending_ft = 0
#             ct=doc.annual_ct / 12
#             ft=doc.annual_ft/12
#             for month in mapping_months:
#                 doc.append('target_child', {
#                     'month': month,
#                     'month_nos': map_months[month] , # Correct mapping for month_no
#                     'ct':ct,
#                 })
#             for m in mapping_months:
#                 doc.append('monthly_ft_allocation',{
#                         'month': m,
#                         'month_nos': map_months[m] , 
#                         'ft':ft
#                     })
#             total_months = len(doc.target_child)
#             revised_ct_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for tc in doc.target_child:
#                 tc.revised_ct = tc.ct
#                 revised_ct_list.append(tc)
#             revised_ft_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for i in doc.monthly_ft_allocation:
#                 i.cr_ft = i.ft
#                 revised_ft_list.append(i)
#             for idx, tc in enumerate(revised_ct_list):
#             # for idx, tc in enumerate(doc.target_child):
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
                    
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr = (achieved_value / tc.revised_ct) * 100 if tc.revised_ct else 0

#                 pending_ct = tc.ct_yta
#                 remaining = revised_ct_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ct = pending_ct / num_remaining
#                     for next_tc in remaining:
#                         next_tc.revised_ct += redistributed_ct

          
#             for idx, i in enumerate(revised_ft_list):
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """

#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Invoice` AS si
#                     WHERE MONTH(si.posting_date) = %s
#                     AND YEAR(si.posting_date) = %s
#                     AND si.services IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 pending_ft = i.ftyta
#                 remaining = revised_ft_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ft = pending_ft / num_remaining
#                     for next_tc in remaining:
#                         next_tc.cr_ft += redistributed_ft
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit() 
#         # 
#         elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
#             pending_ct = 0
#             pending_ft = 0
#             ct=doc.annual_ct / 12
#             ft=doc.annual_ft/12
#             for month in mapping_months:
#                 doc.append('target_child', {
#                     'month': month,
#                     'month_nos': map_months[month] ,
#                     'ct':ct,
#                     'ft':ft
#                 })
#             for m in mapping_months:
#                 doc.append('monthly_ft_allocation',{
#                         'month': m,
#                         'month_nos': map_months[m] , 
#                         'ft':ft
#                     })
#             total_months = len(doc.target_child)
#             revised_ct_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for tc in doc.target_child:
#                 tc.revised_ct = tc.ct
#                 revised_ct_list.append(tc)
#             revised_ft_list = []
#             # First pass: initialize revised_ct with ct for all rows
#             for i in doc.monthly_ft_allocation:
#                 i.cr_ft = i.ft
#                 revised_ft_list.append(i)
#             last_idx = len(doc.target_child) - 1
#             for idx, tc in enumerate(revised_ct_list):
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """
#                     # Execute the query with parameters for month and year
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
                    
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 tc.achieved = achieved_value
#                 tc.ct_yta = tc.revised_ct - achieved_value
#                 tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
#                 pending_ct = tc.ct_yta
#                 remaining = revised_ct_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ct = pending_ct / num_remaining
#                     for next_tc in remaining:
#                         next_tc.revised_ct += redistributed_ct
#             for idx, i in enumerate(revised_ft_list):
#                 month = map_months.get(i.month)
#                 month_no = mapping_months.get(i.month)
#                 if month in ['01', '02', '03']:
#                     year = extract_year(tp.custom_year_end_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """

#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 else:
#                     year = extract_year(tp.custom_year_start_date)
#                     query = f"""
#                     SELECT SUM(si.base_total) AS total
#                     FROM `tabSales Order` AS si
#                     WHERE MONTH(si.transaction_date) = %s
#                     AND YEAR(si.transaction_date) = %s
#                     AND si.service IN ({service_list_sql})
#                     AND si.status NOT IN ('Cancelled', 'Closed', 'On Hold')
#                     """
#                     achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
#                 i.f_achieved = achieved_value
#                 i.ftyta = i.cr_ft - achieved_value
#                 i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
#                 pending_ft = i.ftyta
#                 remaining = revised_ft_list[idx+1:]
#                 num_remaining = len(remaining)
#                 if num_remaining:
#                     redistributed_ft = pending_ft / num_remaining
#                     for next_tc in remaining:
#                         next_tc.cr_ft += redistributed_ft
#                 doc.save(ignore_permissions=True)
#                 frappe.db.commit() 
        
#     return 'OK'


@frappe.whitelist()
def calculate_target_for_manager_test(name,emp,year):
    def get_month_range(start_date, end_date):
        current = start_date.replace(day=1)
        end = end_date.replace(day=1)
        months = []
        while current <= end:
            months.append(current)
            current += relativedelta(months=1)
        return months

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
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
           
            total_months = len(doc.target_child)
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
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
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
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
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
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
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
           
            total_months = len(doc.target_child)
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
       
        elif tp.based_on_service ==1 and tp.based_on_candidate_owner ==0 and tp.target_based_unit == 'Sales Invoice':
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
            
            total_months = len(doc.target_child)
            
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
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        # 
        elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
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
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        elif tp.based_on_candidate_owner ==1 and tp.target_based_unit == 'Sales Invoice':
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
                        AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    
                    query = f"""
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
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
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
                        AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
                        AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        
    return 'OK'


# 
@frappe.whitelist()
def calculate_target_for_manager_inso_test(doc,method):
    tps = frappe.get_all('Target Manager',['*'])
    def get_month_range(start_date, end_date):
        current = start_date.replace(day=1)
        end = end_date.replace(day=1)
        months = []
        while current <= end:
            months.append(current)
            current += relativedelta(months=1)
        return months
    map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    
    mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
                      'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
    
    for tp in tps:
        doc = frappe.get_doc('Target Manager', tp.name)
        # doc = frappe.get_doc('Target Manager',"TA-0027")
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
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
           
            total_months = len(doc.target_child)
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
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
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
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
                                FROM `tabSales Order` AS so
                                WHERE so.account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                                SELECT SUM(so.base_total) AS total 
                                FROM `tabSales Order` AS so
                                WHERE account_manager IN ({user_list_sql}) 
                                AND MONTH(so.transaction_date) = %s 
                                AND YEAR(so.transaction_date) = %s 
                                AND so.status NOT IN ('Cancelled', 'Closed', 'On Hold')
                                """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
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
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
           
            total_months = len(doc.target_child)
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
       
        elif tp.based_on_service ==1 and tp.based_on_candidate_owner ==0 and tp.target_based_unit == 'Sales Invoice':
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
            
            total_months = len(doc.target_child)
            
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
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        # 
        elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
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
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        elif tp.based_on_candidate_owner ==1 and tp.target_based_unit == 'Sales Invoice':
            pending_ct = 0
            pending_ft = 0
            start_date = tp.custom_year_start_date
            end_date = tp.custom_year_end_date

            months = get_month_range(start_date, end_date)
            num_months = len(months)
            ct = doc.annual_ct / num_months if num_months else 0
            ft = doc.annual_ft / num_months if num_months else 0
            for dt in months:
                month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
                month_num = dt.strftime('%m')   # '01', '02', etc.

                doc.append('target_child', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ct': ct
                })
                doc.append('monthly_ft_allocation', {
                    'month': month_name,
                    'month_nos': month_num,
                    'ft': ft
                })
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
                        AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    
                    query = f"""
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
                        AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                tc.revised_ct = tc.ct + pending_ct
                tc.achieved = achieved_value
                tc.ct_yta = tc.revised_ct - achieved_value
                tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
                pending_ct = tc.ct_yta
                # frappe.db.set_value("Target Child", tc.name, "revised_ct", tc.revised_ct)
                # frappe.db.set_value("Target Child", tc.name, "achieved", tc.achieved)
                # frappe.db.set_value("Target Child", tc.name, "ct_yta", tc.ct_yta)
                # frappe.db.set_value("Target Child", tc.name, "sr", tc.sr)
            for i in doc.monthly_ft_allocation:
                month = map_months.get(i.month)
                month_no = mapping_months.get(i.month)
                if month in ['01', '02', '03']:
                    year = extract_year(tp.custom_year_end_date)
                    query = f"""
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
                        AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    query = f"""
                        SELECT SUM(sii.base_amount) AS total
                        FROM `tabSales Invoice` AS si
                        INNER JOIN `tabSales Invoice Item` AS sii
                        ON si.name = sii.parent
                        WHERE sii.candidate_owner IN ({user_list_sql})
                        AND MONTH(si.posting_date) = %s
                        AND YEAR(si.posting_date) = %s
                        AND si.services='REC-I'
                        AND si.status NOT IN ('Cancelled', 'Credit Note Issued', 'Return')
                    """
                    achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
                i.cr_ft = i.ft + pending_ft
                i.f_achieved = achieved_value
                i.ftyta = i.cr_ft - achieved_value
                pending_ft = i.ftyta
                i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
                doc.save(ignore_permissions=True)
                frappe.db.commit() 
        
    return 'OK'
