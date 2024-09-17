# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
class TargetManager(Document):
    def validate(self):
        if frappe.db.exists("Target Allocation",{'year':self.year,'employee':self.employee}):
            frappe.throw("Target for %s is already Allocated for %s "%(self.employee_name,self.year))
    # def on_update(self):
    #     calculate_target_for_manager()

# @frappe.whitelist()
# def calculate_target_on_update(self,method):
#     calculate_target()

# @frappe.whitelist()
# def calculate_target():
#     tps = frappe.get_all('Target Manager',['*'])
#     # map_months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
#     map_months = {'Apr':12,'May':11,'Jun':10,'Jul':9,'Aug':8,'Sep':7,'Oct':6,'Nov':5,'Dec':4,'Jan':3,'Feb':2,'Mar':1}
#     mapping_months = {'Apr':12,'May':11,'Jun':10,'Jul':9,'Aug':8,'Sep':7,'Oct':6,'Nov':5,'Dec':4,'Jan':3,'Feb':2,'Mar':1}   
#     for tp in tps:
#         doc = frappe.get_doc('Target Manager',tp.name)
#         if tp.target_based_unit == 'Service Based':
#             servs = frappe.get_all('Employee services',{'parent':tp.name},['services'])
#             service_list = []
#             for serv in servs:
#                 service_list.append(serv.services)
#             service_list = (str(service_list).replace('[','')).replace(']','')
#             pending_ct = 0
#             pending_ft = 0
#             for tc in doc.target_child:
#                 month = map_months.get(tc.month)
#                 month_no = mapping_months.get(tc.month)
#                 frappe.errprint([tp.custom_year_start_date, type(tp.custom_year_start_date)])
    #             if month in ['01','02','03']:
    #                 year = extract_year(tp.custom_year_end_date)
    #                 achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in  ('Cancelled','Credit Note Issued','Return') """%(service_list,month,year),as_dict=True)[0].total or 0
    #             else:
                    
    #                 year = extract_year(tp.custom_year_start_date)
    #                 print(year)
    #                 achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in  ('Cancelled','Credit Note Issued','Return') """%(service_list,month,year),as_dict=True)[0].total or 0
    #             tc.revised_ct = tc.ct + pending_ct
    #             tc.revised_ft = tc.ft + pending_ft
    #             tc.achieved = achieved
    #             tc.ytct = (tc.ct - achieved) / int(month_no)
    #             tc.ytft = (tc.ft - achieved) / int(month_no)
    #             tc.ct_yta = tc.revised_ct - achieved
    #             tc.ft_yta = tc.revised_ft - achieved
    #             pending_ct = tc.revised_ct - achieved
    #             pending_ft = tc.revised_ft - achieved
    #             doc.save(ignore_permissions=True)
    #             frappe.db.commit()
    #     elif tp.target_based_unit == 'Account Based':
    #         ac = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
    #         if ac:
    #             pending_ct = 0
    #             pending_ft = 0
    #             for tc in doc.target_child:
    #                 month = map_months.get(tc.month)
    #                 month_no = mapping_months.get(tc.month)
    #                 if month in ['01','02','03']:
    #                     year = extract_year(tp.custom_year_end_date)
    #                     am_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where account_manager = '%s' and delivery_manager != '%s' and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(ac,ac,month,year),as_dict=True)[0].total or 0
    #                     dm_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where delivery_manager = '%s' and account_manager != '%s' and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(ac,ac,month,year),as_dict=True)[0].total or 0
    #                     am_dm_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where delivery_manager = '%s' and account_manager = '%s' and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(ac,ac,month,year),as_dict=True)[0].total or 0
    #                 else:
    #                     year = extract_year(tp.custom_year_start_date)
    #                     am_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where account_manager = '%s' and delivery_manager != '%s' and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(ac,ac,month,year),as_dict=True)[0].total or 0
    #                     dm_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where delivery_manager = '%s' and account_manager != '%s' and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(ac,ac,month,year),as_dict=True)[0].total or 0
    #                     am_dm_achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where delivery_manager = '%s' and account_manager = '%s' and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(ac,ac,month,year),as_dict=True)[0].total or 0
    #                 tc.revised_ct = tc.ct + pending_ct
    #                 tc.revised_ft = tc.ft + pending_ft
    #                 achieved = am_achieved + dm_achieved + am_dm_achieved
    #                 tc.achieved = achieved
    #                 tc.ytct = (tc.ct - achieved) / int(month_no)
    #                 tc.ytft = (tc.ft - achieved) / int(month_no)
    #                 tc.ct_yta = tc.revised_ct - achieved
    #                 tc.ft_yta = tc.revised_ft - achieved
    #                 pending_ct = tc.revised_ct - achieved
    #                 pending_ft = tc.revised_ft - achieved
    #                 doc.save(ignore_permissions=True)
    #                 frappe.db.commit()
    #     # elif tp.target_based_unit == 'Sales Invoice on TO':
    #     # 		pending_ct = 0
    #     # 		pending_ft = 0
    #     # 		user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
    #     # 		for tc in doc.target_child:
    #     # 			month = map_months.get(tc.month)
    #     # 			month_no = mapping_months.get(tc.month)
    #     # 			year = tp.year
    #     # 			achieved = frappe.db.sql("""select sum(base_total) as total from `tabSales Invoice` where account_manager = (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(user_id,month,year),as_dict=True)[0].total or 0
    #     # 			tc.revised_ct = tc.ct + pending_ct
    #     # 			tc.revised_ft = tc.ft + pending_ft
    #     # 			tc.achieved = achieved
    #     # 			tc.ytct = (tc.ct - achieved) / int(month_no)
    #     # 			tc.ytft = (tc.ft - achieved) / int(month_no)
    #     # 			tc.ct_yta = tc.revised_ct - achieved
    #     # 			tc.ft_yta = tc.revised_ft - achieved
    #     # 			pending_ct = tc.revised_ct - achieved
    #     # 			pending_ft = tc.revised_ft - achieved
    #     # 			doc.save(ignore_permissions=True)
    #     # 			frappe.db.commit()
    #     elif tp.target_based_unit == 'Sales Invoice on SC (Service)':
    #         servs = frappe.get_all('Employee services',{'parent':tp.name},['services'])
    #         service_list = []
    #         for serv in servs:
    #             service_list.append(serv.services)
    #         service_list = (str(service_list).replace('[','')).replace(']','')
    #         pending_ct = 0
    #         pending_ft = 0
    #         user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
    #         for tc in doc.target_child:
    #             month = map_months.get(tc.month)
    #             month_no = mapping_months.get(tc.month)
    #             if month in ['01','02','03']:
    #                 year = extract_year(tp.custom_year_end_date)
    #                 achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(user_id,service_list,month,year),as_dict=True)[0].total or 0
    #             else:
    #                 year = extract_year(tp.custom_year_start_date)
    #                 achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(user_id,service_list,month,year),as_dict=True)[0].total or 0
    #             tc.revised_ct = tc.ct + pending_ct
    #             tc.revised_ft = tc.ft + pending_ft
    #             tc.achieved = achieved
    #             tc.ytct = (tc.ct - achieved) / int(month_no)
    #             tc.ytft = (tc.ft - achieved) / int(month_no)
    #             tc.ct_yta = tc.revised_ct - achieved
    #             tc.ft_yta = tc.revised_ft - achieved
    #             pending_ct = tc.revised_ct - achieved
    #             pending_ft = tc.revised_ft - achieved
    #             doc.save(ignore_permissions=True)
    #             frappe.db.commit()
    #     elif tp.target_based_unit == 'Sales Invoice on SC (Item)':
    #         pending_ct = 0
    #         pending_ft = 0
    #         for tc in doc.target_child:
    #             month = map_months.get(tc.month)
    #             month_no = mapping_months.get(tc.month)
    #             if month in ['01','02','03']:
    #                 year = extract_year(tp.custom_year_end_date)
    #                 achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice Item` c inner join `tabSales Invoice` p on p.name = c.parent where p.month(creation) = %s and where c.candidate_owner = %s p.year(creation) = %s and p.status not in ('Cancelled','Credit Note Issued','Return') """%(month,user_id,year),as_dict=True)[0].total or 0
    #             else:
    #                 year = extract_year(tp.custom_year_start_date)
    #                 achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice Item` c inner join `tabSales Invoice` p on p.name = c.parent where p.month(creation) = %s and where c.candidate_owner = %s p.year(creation) = %s and p.status not in ('Cancelled','Credit Note Issued','Return') """%(month,user_id,year),as_dict=True)[0].total or 0
    #             tc.revised_ct = tc.ct + pending_ct
    #             tc.revised_ft = tc.ft + pending_ft
    #             tc.achieved = achieved
    #             tc.ytct = (tc.ct - achieved) / int(month_no)
    #             tc.ytft = (tc.ft - achieved) / int(month_no)
    #             tc.ct_yta = tc.revised_ct - achieved
    #             tc.ft_yta = tc.revised_ft - achieved
    #             pending_ct = tc.revised_ct - achieved
    #             pending_ft = tc.revised_ft - achieved
    #             doc.save(ignore_permissions=True)
    #             frappe.db.commit()

    # return 'OK'

    @frappe.whitelist()
    def test_method():
        # d = frappe.db.sql("select creation from `tabSales Invoice` where delivery_manager = account_manager and month(creation) = 2 ",as_dict=True)
        d = frappe.db.sql("select creation from `tabSales Order` where year(creation) = 6 ",as_dict=True)    
        print(d)


def calculate_target_on_update_manager(doc,method):
    update_achieved_in_tm()

@frappe.whitelist()
def calculate_target_for_manager():
    tps = frappe.get_all('Target Manager',['*'])
    map_months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    mapping_months = {'Apr':'12','May':'11','Jun':'10','Jul':'9','Aug':'8','Sep':'7','Oct':'6','Nov':'5','Dec':'4','Jan':'3','Feb':'2','Mar':'1'}
    current_month = datetime.now().month  # Get the current month number
    current_year = datetime.now().year  # Get the current year
    for tp in tps:
        doc = frappe.get_doc('Target Manager',tp.name)
        if tp.target_based_unit == 'Sales Order on TO':
            pending_ct = 0
            pending_ft = 0
            balance_ct=0
            balance_ft=0
            # for tc in doc.target_child:
            last_idx = len(doc.target_child) - 1 
            for idx, tc in enumerate(doc.target_child):
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
                if month in ['01','02','03']:
                    year = extract_year(tp.custom_year_end_date)
                    achieved = frappe.db.sql("""select sum(total) as total from `tabSales Order` where account_manager = '%s' and month(creation) = '%s' and year(creation) = '%s' and status not in ('Cancelled','Credit Note Issued','Return') """ %(user_id,month,year),as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    achieved = frappe.db.sql("""select sum(total) as total from `tabSales Order` where account_manager = '%s' and month(creation) = '%s' and year(creation) = '%s' and status not in ('Cancelled','Credit Note Issued','Return') """ %(user_id,month,year),as_dict=True)[0].total or 0
                tc.achieved = achieved
                if int(month) == current_month and int(year) == current_year:
                    tc.revised_ct = tc.ct + pending_ct
                    tc.revised_ft = tc.ft + pending_ft
                    # tc.achieved = achieved
                    tc.ytct = (tc.ct - achieved) / int(month_no)
                    frappe.errprint(month_no)
                    tc.ytft = (tc.ft - achieved) / int(month_no)
                    tc.ct=tc.ct + balance_ct
                    tc.ft= tc.ft + balance_ft
                    # tc.ct_yta = tc.revised_ct - achieved
                    # tc.ft_yta = tc.revised_ft - achieved
                    original_ct = tc.ct
                    original_ft = tc.ft
                    tc.ct_yta = tc.ct - achieved
                    tc.ft_yta = tc.ft - achieved
                    pending_ct = tc.revised_ct - achieved
                    pending_ft = tc.revised_ft - achieved
                    balance_ct=tc.ct_yta 
                    balance_ft=tc.ft_yta
                    if idx > 0 and not tc.get('is_yta_added'):
                        prev_tc = doc.target_child[idx - 1]
                        if tc.ct == original_ct and tc.ft == original_ft:
                            tc.ct += prev_tc.ct_yta
                            tc.ft += prev_tc.ft_yta
                            tc.is_yta_added = 1
                        if tc.ct_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ct += tc.ct_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ct += tc.ct_yta
                        if tc.ft_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ft += tc.ft_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ft += tc.ft_yta
                        if tc.ct_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ct += tc.ct_yta
                        if tc.ft_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ft += tc.ft_yta
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
        elif tp.target_based_unit == 'Sales Invoice on TO':
            pending_ct = 0
            pending_ft = 0
            balance_ct=0
            balance_ft=0
            # for tc in doc.target_child:
            last_idx = len(doc.target_child) - 1 
            for idx, tc in enumerate(doc.target_child):
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
                if month in ['01','02','03']:
                    year = extract_year(tp.custom_year_end_date)
                    achieved = frappe.db.sql("""select sum(total) as total from `tabSales Invoice` where account_manager = '%s' and month(creation) = '%s' and year(creation) = '%s' and status not in ('Cancelled','Credit Note Issued','Return') """ %(user_id,month,year),as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    achieved = frappe.db.sql("""select sum(total) as total from `tabSales Invoice` where account_manager = '%s' and month(creation) = '%s' and year(creation) = '%s' and status not in ('Cancelled','Credit Note Issued','Return') """ %(user_id,month,year),as_dict=True)[0].total or 0
                tc.achieved = achieved
                if int(month) == current_month and int(year) == current_year:
                    tc.revised_ct = tc.ct + pending_ct
                    tc.revised_ft = tc.ft + pending_ft
                    # tc.achieved = achieved
                    tc.ytct = (tc.ct - achieved) / int(month_no)
                    frappe.errprint(month_no)
                    tc.ytft = (tc.ft - achieved) / int(month_no)
                    tc.ct=tc.ct + balance_ct
                    tc.ft= tc.ft + balance_ft
                    # tc.ct_yta = tc.revised_ct - achieved
                    # tc.ft_yta = tc.revised_ft - achieved
                    original_ct = tc.ct
                    original_ft = tc.ft
                    tc.ct_yta = tc.ct - achieved
                    tc.ft_yta = tc.ft - achieved
                    # pending_ct = tc.revised_ct - achieved
                    # pending_ft = tc.revised_ft - achieved
                    pending_ct = (tc.ct - achieved) / int(month_no)
                    pending_ft = (tc.ft - achieved) / int(month_no)
                    balance_ct=tc.ct_yta 
                    balance_ft=tc.ft_yta
                    if idx > 0 and not tc.get('is_yta_added'):
                        prev_tc = doc.target_child[idx - 1]
                        if tc.ct == original_ct and tc.ft == original_ft:
                            tc.ct += prev_tc.ct_yta
                            tc.ft += prev_tc.ft_yta
                            tc.is_yta_added = 1
                        if tc.ct_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ct += tc.ct_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ct += tc.ct_yta
                        if tc.ft_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ft += tc.ft_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ft += tc.ft_yta
                        if tc.ct_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ct += tc.ct_yta
                        if tc.ft_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ft += tc.ft_yta
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
        elif tp.target_based_unit == 'Sales Invoice on SC (Item)':
            pending_ct = 0
            pending_ft = 0
            balance_ct=0
            balance_ft=0
            last_idx = len(doc.target_child) - 1 
            # for tc in doc.target_child:
            for idx, tc in enumerate(doc.target_child):
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
                if month in ['01','02','03']:
                    year = extract_year(tp.custom_year_end_date)
                    achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice` Item c inner join tabSales Invoice p on p.name = c.parent where month(p.creation) = '%s' and c.candidate_owner = '%s' and year(p.creation) = '%s' and p.status not in ('Cancelled','Credit Note Issued','Return') """%(month,user_id,year),as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice` Item c inner join tabSales Invoice p on p.name = c.parent where month(p.creation) = '%s' and c.candidate_owner = '%s' and year(p.creation) = '%s' and p.status not in ('Cancelled','Credit Note Issued','Return') """%(month,user_id,year),as_dict=True)[0].total or 0
                    print(achieved)
                tc.achieved = achieved
                if int(month) == current_month and int(year) == current_year:
                    tc.revised_ct = tc.ct + pending_ct
                    tc.revised_ft = tc.ft + pending_ft
                    # tc.achieved = achieved
                    tc.ytct = (tc.ct - achieved) / int(month_no)
                    frappe.errprint(month_no)
                    tc.ytft = (tc.ft - achieved) / int(month_no)
                    tc.ct=tc.ct + balance_ct
                    tc.ft= tc.ft + balance_ft
                    # tc.ct_yta = tc.revised_ct - achieved
                    # tc.ft_yta = tc.revised_ft - achieved
                    original_ct = tc.ct
                    original_ft = tc.ft
                    tc.ct_yta = tc.ct - achieved
                    tc.ft_yta = tc.ft - achieved
                    # pending_ct = tc.revised_ct - achieved
                    # pending_ft = tc.revised_ft - achieved
                    pending_ct = (tc.ct - achieved) / int(month_no)
                    pending_ft = (tc.ft - achieved) / int(month_no)
                    balance_ct=tc.ct_yta 
                    balance_ft=tc.ft_yta
                    if idx > 0 and not tc.get('is_yta_added'):
                        prev_tc = doc.target_child[idx - 1]
                        if tc.ct == original_ct and tc.ft == original_ft:
                            tc.ct += prev_tc.ct_yta
                            tc.ft += prev_tc.ft_yta
                            tc.is_yta_added = 1
                        if tc.ct_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ct += tc.ct_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ct += tc.ct_yta
                        if tc.ft_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ft += tc.ft_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ft += tc.ft_yta
                        if tc.ct_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ct += tc.ct_yta
                        if tc.ft_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ft += tc.ft_yta
                # if int(month) == current_month and int(year) == current_year:
                #     tc.revised_ct = tc.ct + pending_ct
                #     tc.revised_ft = tc.ft + pending_ft
                #     # tc.achieved = achieved
                #     tc.ytct = (tc.ct - achieved) / int(month_no)
                #     tc.ytft = (tc.ft - achieved) / int(month_no)
                #     # tc.ct_yta = tc.revised_ct - achieved
                #     # tc.ft_yta = tc.revised_ft - achieved
                #     tc.ct_yta = tc.ct - achieved
                #     tc.ft_yta = tc.ft - achieved
                #     pending_ct = tc.revised_ct - achieved
                #     pending_ft = tc.revised_ft - achieved
                #     tc.ct=tc.ct + tc.ytct
                #     tc.ft=tc.ft + tc.ytft
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
        elif tp.target_based_unit == 'Sales Invoice on SC (Service)':
            servs = frappe.get_all('Employee services',{'parent':tp.name},['services'])
            service_list = []
            for serv in servs:
                service_list.append(serv.services)
            service_list = (str(service_list).replace('[','')).replace(']','')
            pending_ct = 0
            pending_ft = 0
            balance_ct=0
            balance_ft=0
            user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
            last_idx = len(doc.target_child) - 1 
            # for tc in doc.target_child:
            for idx, tc in enumerate(doc.target_child):
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01','02','03']:
                    year = extract_year(tp.custom_year_end_date)
                    achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(service_list,month,year),as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(service_list,month,year),as_dict=True)[0].total or 0
                tc.achieved = achieved
                if int(month) == current_month and int(year) == current_year:
                    tc.revised_ct = tc.ct + pending_ct
                    tc.revised_ft = tc.ft + pending_ft
                    # tc.achieved = achieved
                    tc.ytct = (tc.ct - achieved) / int(month_no)
                    frappe.errprint(month_no)
                    tc.ytft = (tc.ft - achieved) / int(month_no)
                    tc.ct=tc.ct + balance_ct
                    tc.ft= tc.ft + balance_ft
                    # tc.ct_yta = tc.revised_ct - achieved
                    # tc.ft_yta = tc.revised_ft - achieved
                    original_ct = tc.ct
                    original_ft = tc.ft
                    tc.ct_yta = tc.ct - achieved
                    tc.ft_yta = tc.ft - achieved
                    # pending_ct = tc.revised_ct - achieved
                    # pending_ft = tc.revised_ft - achieved
                    pending_ct = (tc.ct - achieved) / int(month_no)
                    pending_ft = (tc.ft - achieved) / int(month_no)
                    balance_ct=tc.ct_yta 
                    balance_ft=tc.ft_yta
                    if idx > 0 and not tc.get('is_yta_added'):
                        prev_tc = doc.target_child[idx - 1]
                        if tc.ct == original_ct and tc.ft == original_ft:
                            tc.ct += prev_tc.ct_yta
                            tc.ft += prev_tc.ft_yta
                            tc.is_yta_added = 1
                        if tc.ct_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ct += tc.ct_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ct += tc.ct_yta
                        if tc.ft_yta > 0 :
                            if idx + 1 <= last_idx:
                                next_tc = doc.target_child[idx + 1]
                                next_tc.ft += tc.ft_yta
                            else:
                                last_tc = doc.target_child[last_idx]
                                last_tc.ft += tc.ft_yta
                        if tc.ct_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ct += tc.ct_yta
                        if tc.ft_yta < 0:
                            last_tc = doc.target_child[last_idx]
                            last_tc.ft += tc.ft_yta
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
    

    return 'OK'

@frappe.whitelist()
def update_achieved_in_tm():
    # frappe.msgprint("hi")
    tps = frappe.get_all('Target Manager',['*'])
    # map_months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    map_months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    mapping_months = {'Apr':'12','May':'11','Jun':'10','Jul':'9','Aug':'8','Sep':'7','Oct':'6','Nov':'5','Dec':'4','Jan':'3','Feb':'2','Mar':'1'}
    for tp in tps:
        doc = frappe.get_doc('Target Manager',tp.name)
        # ac = frappe.db.get_value('Employee',{'name':doc.employee},'gross_salary')
        # ac = int(ac)
        # frappe.errprint(tp.custom_year_start_date)
        # for i in doc.target_child:
        #     ft=ac*6
        #     i.ft=ft
        #     ct=ac/12
        #     i.ct=ct
        if tp.target_based_unit == 'Sales Order on TO':
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
                if month in ['01','02','03']:
                    year = extract_year(tp.custom_year_end_date)
                    achieved = frappe.db.sql("""select sum(total) as total from `tabSales Order` where account_manager = '%s' and month(creation) = '%s' and year(creation) = '%s' and status not in ('Cancelled','Credit Note Issued','Return') """ %(user_id,month,year),as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    achieved = frappe.db.sql("""select sum(total) as total from `tabSales Order` where account_manager = '%s' and month(creation) = '%s' and year(creation) = '%s' and status not in ('Cancelled','Credit Note Issued','Return') """ %(user_id,month,year),as_dict=True)[0].total or 0
                tc.achieved = achieved
                doc.save(ignore_permissions=True)
                frappe.db.commit()
        elif tp.target_based_unit == 'Sales Invoice on SC (Item)':
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
                if month in ['01','02','03']:
                    year = extract_year(tp.custom_year_end_date)
                    achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice` Item c inner join tabSales Invoice p on p.name = c.parent where month(p.creation) = '%s' and c.candidate_owner = '%s' and year(p.creation) = '%s' and p.status not in ('Cancelled','Credit Note Issued','Return') """%(month,user_id,year),as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice` Item c inner join tabSales Invoice p on p.name = c.parent where month(p.creation) = '%s' and c.candidate_owner = '%s' and year(p.creation) = '%s' and p.status not in ('Cancelled','Credit Note Issued','Return') """%(month,user_id,year),as_dict=True)[0].total or 0
                    print(achieved)
                tc.achieved = achieved
                doc.save(ignore_permissions=True)
                frappe.db.commit()
        elif tp.target_based_unit == 'Sales Invoice on SC (Service)':
            servs = frappe.get_all('Employee services',{'parent':tp.name},['services'])
            service_list = []
            for serv in servs:
                service_list.append(serv.services)
            service_list = (str(service_list).replace('[','')).replace(']','')
            user_id = frappe.db.get_value('Employee',{'name':doc.employee},'user_id')
            for tc in doc.target_child:
                month = map_months.get(tc.month)
                month_no = mapping_months.get(tc.month)
                if month in ['01','02','03']:
                    year = extract_year(tp.custom_year_end_date)
                    achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(service_list,month,year),as_dict=True)[0].total or 0
                else:
                    year = extract_year(tp.custom_year_start_date)
                    achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return') """%(service_list,month,year),as_dict=True)[0].total or 0
                tc.achieved = achieved
                doc.save(ignore_permissions=True)
                frappe.db.commit()
      

    return 'OK'

# @frappe.whitelist()
# def calculate_target_for_manager():
#     frappe.errprint("Starting calculation")
#     try:
#         tps = frappe.get_all('Target Manager', ['*'])
#         map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
#         mapping_months = {'Apr': 12, 'May': 11, 'Jun': 10, 'Jul': 9, 'Aug': 8, 'Sep': 7, 'Oct': 6, 'Nov': 5, 'Dec': 4, 'Jan': 3, 'Feb': 2, 'Mar': 1}

#         for tp in tps:
#             frappe.errprint(f"Processing Target Manager: {tp.name}")
#             doc = frappe.get_doc('Target Manager', tp.name)
#             if not doc:
#                 frappe.errprint(f"Target Manager {tp.name} not found")
#                 continue

#             if tp.target_based_unit == 'Sales Order on TO':
#                 pending_ct = 0
#                 pending_ft = 0
#                 for tc in doc.target_child:
#                     month = map_months.get(tc.month)
#                     month_no = mapping_months.get(tc.month)
#                     user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
#                     if month in ['01', '02', '03']:
#                         year = extract_year(tp.custom_year_end_date)
#                         achieved = frappe.db.sql("""select sum(total) as total from `tabSales Order` where account_manager = %s and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return')""", (user_id, month, year), as_dict=True)[0].total or 0
#                     else:
#                         year = extract_year(tp.custom_year_start_date)
#                         achieved = frappe.db.sql("""select sum(total) as total from `tabSales Order` where account_manager = %s and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return')""", (user_id, month, year), as_dict=True)[0].total or 0
#                     tc.revised_ct = tc.ct + pending_ct
#                     tc.revised_ft = tc.ft + pending_ft
#                     tc.achieved = achieved
#                     tc.ytct = (tc.ct - achieved) / int(month_no)
#                     tc.ytft = (tc.ft - achieved) / int(month_no)
#                     tc.ct_yta = tc.revised_ct - achieved
#                     tc.ft_yta = tc.revised_ft - achieved
#                     pending_ct = tc.revised_ct - achieved
#                     pending_ft = tc.revised_ft - achieved
#                     doc.save(ignore_permissions=True)
#                     frappe.db.commit()

#             elif tp.target_based_unit == 'Sales Invoice on SC (Item)':
#                 pending_ct = 0
#                 pending_ft = 0
#                 for tc in doc.target_child:
#                     month = map_months.get(tc.month)
#                     month_no = mapping_months.get(tc.month)
#                     user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
#                     if month in ['01', '02', '03']:
#                         year = extract_year(tp.custom_year_end_date)
#                         achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice Item` c inner join tabSales Invoice p on p.name = c.parent where month(p.creation) = %s and c.candidate_owner = %s and year(p.creation) = %s and p.status not in ('Cancelled','Credit Note Issued','Return')""", (month, user_id, year), as_dict=True)[0].total or 0
#                     else:
#                         year = extract_year(tp.custom_year_start_date)
#                         achieved = frappe.db.sql("""select sum(c.sc_company_currency) as total from `tabSales Invoice Item` c inner join tabSales Invoice p on p.name = c.parent where month(p.creation) = %s and c.candidate_owner = %s and year(p.creation) = %s and p.status not in ('Cancelled','Credit Note Issued','Return')""", (month, user_id, year), as_dict=True)[0].total or 0
#                     tc.revised_ct = tc.ct + pending_ct
#                     tc.revised_ft = tc.ft + pending_ft
#                     tc.achieved = achieved
#                     tc.ytct = (tc.ct - achieved) / int(month_no)
#                     tc.ytft = (tc.ft - achieved) / int(month_no)
#                     tc.ct_yta = tc.revised_ct - achieved
#                     tc.ft_yta = tc.revised_ft - achieved
#                     pending_ct = tc.revised_ct - achieved
#                     pending_ft = tc.revised_ft - achieved
#                     doc.save(ignore_permissions=True)
#                     frappe.db.commit()

#             elif tp.target_based_unit == 'Sales Invoice on SC (Service)':
#                 servs = frappe.get_all('Employee services', {'parent': tp.name}, ['services'])
#                 service_list = [serv.services for serv in servs]
#                 service_list = (str(service_list).replace('[', '')).replace(']', '')
#                 pending_ct = 0
#                 pending_ft = 0
#                 user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
#                 for tc in doc.target_child:
#                     month = map_months.get(tc.month)
#                     month_no = mapping_months.get(tc.month)
#                     if month in ['01', '02', '03']:
#                         year = extract_year(tp.custom_year_end_date)
#                         achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return')""", (service_list, month, year), as_dict=True)[0].total or 0
#                     else:
#                         year = extract_year(tp.custom_year_start_date)
#                         achieved = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where services in (%s) and month(creation) = %s and year(creation) = %s and status not in ('Cancelled','Credit Note Issued','Return')""", (service_list, month, year), as_dict=True)[0].total or 0
#                     tc.revised_ct = tc.ct + pending_ct
#                     tc.revised_ft = tc.ft + pending_ft
#                     tc.achieved = achieved
#                     tc.ytct = (tc.ct - achieved) / int(month_no)
#                     tc.ytft = (tc.ft - achieved) / int(month_no)
#                     tc.ct_yta = tc.revised_ct - achieved
#                     tc.ft_yta = tc.revised_ft - achieved
#                     pending_ct = tc.revised_ct - achieved
#                     pending_ft = tc.revised_ft - achieved
#                     doc.save(ignore_permissions=True)
#                     frappe.db.commit()

#     except Exception as e:
#         frappe.log_error(message=str(e), title="Error in calculate_target_for_manager")

#     return 'OK'


from datetime import datetime

def extract_year(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    return date_object.year

