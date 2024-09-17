import frappe
from datetime import datetime
from frappe import _
from frappe.utils import getdate, get_timespan_date_range,flt,today,nowdate
import json
from datetime import date, timedelta
import pandas as pd

@frappe.whitelist()
def get_ct_ft():
    date = datetime.strptime(today(),'%Y-%m-%d')
    mon = datetime.strftime(date,'%b')
    year = datetime.strftime(date,'%Y')
    hr_tp = frappe.db.get_value('Target Manager',{'employee':'TI00003'},'name')
    hr = frappe.db.get_all('Target Child',{'parent':hr_tp,'month':mon},['ct','ft','achieved','ct_yta','ft_yta','parent'])
    it_tp = frappe.db.get_value('Target Manager',{'employee':'TI00005'},'name')
    it = frappe.db.get_all('Target Child',{'parent':'TA-0002','month':mon},['ct','ft','achieved','ct_yta','ft_yta','parent'])
    td_tp = frappe.db.get_value('Target Manager',{'employee':'TI00002'},'name')
    td = frappe.db.get_all('Target Child',{'parent':td_tp,'month':mon},['ct','ft','achieved','ct_yta','ft_yta','parent'])
    fp_tp = frappe.db.get_value('Target Manager',{'employee':'TI00002'},'name')
    fp = frappe.db.get_all('Target Child',{'parent':fp_tp,'month':mon},['ct','ft','achieved','ct_yta','ft_yta','parent'])
    return hr,it,td,fp


# @frappe.whitelist()
# def get_sc_value(month=None,year =None):
#     try :
#         data = []
#         add = 0
#         sr = 0
#         total_dec = frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` where month(creation)= '%s' and status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") and year(creation) = '%s' """ %(month,year),as_dict=True)
#         closure = frappe.db.sql("""select sum(candidate_service_charge) as closure from `tabClosure` where month(so_confirmed_date) = '%s' and so_created = 1 AND YEAR(so_confirmed_date) ='%s'""" % (month,year),as_dict=True)
#         total= round(flt(total_dec[0].total)+ flt(closure[0].closure))
#         # get_at_api = frappe.db.sql("""select at_value from `tabTiips` where employee_id = "TI00005" """)
#         # get_at_sbmk = frappe.db.sql("""select at_value from `tabTiips` where employee_id = "TI00002" """)  
#         # at_api= flt(get_at_api[0][0])/flt(12)
#         # at_sbmk = flt(get_at_sbmk[0][0])/flt(12)
#         # add = flt(at_api)+ flt(at_sbmk) ##R
#         last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
#         short_code = ['AS','API','SP','SBMK']
#         for sc in short_code:
#             emp = frappe.get_doc("Employee",{'status':'Active','tiip_employee':'1','short_code':sc})
#             emp_dict = {}
#             content = []
#             at_yearly = frappe.get_all("Tiips", {'parent': emp.name}, ['at_value'])[0]
#             april_month = (datetime.today()).strftime("%Y-04-01")
#             now = datetime.now()
#             # today_date = now.strftime("%Y-%m-%d")
#             if emp.short_code =='API':
#                 acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` WHERE services in ("IT-SW","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]

#             if emp.short_code == 'SBMK':
#                 acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` WHERE services ="TFP" AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
              
#             if emp.short_code == 'SP':
#                 acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` WHERE services in ("EMS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
               
#             if emp.short_code == 'AS':
#                 acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from `tabSales Invoice` WHERE services not in ("TFP","IT-SW","TGT","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
             
#             at = at_yearly['at_value']
#             month_april = datetime.strptime(april_month,"%Y-%m-%d")
            
#             today_date = now.strftime("%Y-%m-%d")
#             today = datetime.strptime(today_date,"%Y-%m-%d")
            
#             balance_months = (today.year - month_april.year) * 12 + (today.month - month_april.month)
#             balance = 12 - balance_months
            
#             if acheieved_till_date['total']:
#                 at_actual = (at - acheieved_till_date['total'])/ balance
#                 add += at_actual
#             else:
#                 at_actual = (at - 0)/ balance
                
#                 add += round(at_actual)
                
#         get_sr = (flt(total)/flt(add)) *100 ##Q/R*100
#         sr = (round(get_sr))
        
#     except TypeError:
#         total = 0
#     data += round(total),round(add),sr
    
#     employee_data = []
#     short_code = ['AS','API','SP','SBMK']
#     for sc in short_code:
#         emp = frappe.get_doc("Employee",{'status':'Active','tiip_employee':'1','short_code':sc})
#         emp_dict = {}
#         content = []
#         at_yearly = frappe.get_all("Tiips", {'parent': emp.name}, ['at_value'])[0]
#         april_month = (datetime.today()).strftime("%Y-04-01")
#         # previous_month = frappe.utils.add_months(datetime.today(), -1).strftime("%Y-%m-%d")
#         last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
#         # now = datetime.now()
#         # today_date = now.strftime("%Y-%m-%d")
#         if emp.short_code =='API':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services in ("IT-SW","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
            
#         if emp.short_code == 'SBMK':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services ="TFP" AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
            
#         if emp.short_code == 'SP':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services in ("TGT","EMS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
           
#         if emp.short_code == 'AS':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services not in ("TFP","IT-SW","TGT","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
         
#         at = at_yearly['at_value']
#         month_april = datetime.strptime(april_month,"%Y-%m-%d")
#         now = datetime.now()
#         today_date = now.strftime("%Y-%m-%d")
#         today = datetime.strptime(today_date,"%Y-%m-%d")
        
#         balance_months = (today.year - month_april.year) * 12 + (today.month - month_april.month)
#         balance = 12 - balance_months
#         if acheieved_till_date['total']:
#             at_actual = (at - acheieved_till_date['total'])/ balance
#         else :
#             at_actual = (at - 0)/ balance
#         at_monthly = round(at_actual,2)
     
#         d = 0
#         e = 0
#         service_closure = 0
#         service_si = 0
#         total_value = 0
#         acc_si = []
#         dev_si = []
#         both_si = []
#         services = []
        
#         try:
#             if emp.based_on_value == "Role Based":
                
#                 acc_si  = frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE account_manager = '%s' AND delivery_manager != '%s'  AND month(creation) ='%s' AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND YEAR(creation) = '%s'""" % (
#                     emp.prefered_email,emp.prefered_email,month,year),as_dict=True)

#                 dev_si = frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager != '%s' AND month(creation) ='%s'  AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND YEAR(creation) = '%s'""" % (
#                     emp.prefered_email,emp.prefered_email,month,year),as_dict=True)
               
                
#                 both_si = frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager = '%s' AND month(creation) ='%s' AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND YEAR(creation) = '%s'""" % (
#                     emp.prefered_email,emp.prefered_email,month,year),as_dict=True)
               
#                 acc_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE account_manager = '%s' AND  candidate_owner != '%s' AND month(so_confirmed_date) = '%s' AND so_created = 1 AND YEAR(so_confirmed_date) ='%s'""" % (
#                     emp.prefered_email,emp.prefered_email,month,year),as_dict=True)

#                 dev_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE candidate_owner = '%s'  AND account_manager != '%s'AND month(so_confirmed_date) = '%s' AND so_created = 1 AND YEAR(so_confirmed_date) ='%s'""" % (
#                     emp.prefered_email,emp.prefered_email,month,year),as_dict=True)
                
#                 total_value =flt(acc_si[0].total )+flt( dev_si[0].total) + flt( both_si[0].total) + flt(acc_closure[0].charges ) + flt(dev_closure[0].charges )

#             elif emp.based_on_value == "Service Based":
#                 services = frappe.get_all("Employee services", {'parent': emp.name}, ['services'])
                               
#                 service_list = []
#                 for s in services:
#                     service_list.append(s.services)
#                 str_list = str(service_list).strip('[')
#                 str_list = str(str_list).strip(']')
                
#                 if service_list:
#                     service_si  = frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services IN (%s) AND month(creation) = '%s' AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND YEAR(creation) = '%s'""" % (
#                         str_list,month,year),as_dict=True)
                    
#                     total_value += flt(service_si[0].total)
                    
#                     if set(["REC-I","REC-D"]).intersection(set(service_list)):
#                         service_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE month(so_confirmed_date) = '%s' AND so_created = 1 AND YEAR(so_confirmed_date) ='%s'""" % 
#                         (month,year),as_dict=True)
                        
#                 total_value = flt(service_si[0].total) + flt(service_closure[0].charges) #C
                
#         except TypeError:
#             closure = 0
#             s = ''
#         if total_value and at_monthly:
#             d = int(total_value) - int(at_monthly) #C-B
#             e = (int(total_value) /int(at_monthly))*100  #C-B *100
#         emp_dict['image'] = emp.image
#         emp_dict['at_monthly'] = round(at_monthly)
#         emp_dict['total_value'] = round(total_value)
#         emp_dict['d'] = round(d)
#         emp_dict['e'] = round(e)
#         for key, value in emp_dict.items() :
#             print (key, value)
#         employee_data.append(emp_dict.copy())
        

#     data += employee_data

#     return data

# @frappe.whitelist()
# def get_sc_value_ft(month=None,year =None):
#     data = []
#     employee_data = []
#     short_code = ['AS','API','SP','SBMK']
#     for sc in short_code:
#         emp = frappe.get_doc("Employee",{'status':'Active','tiip_employee':'1','short_code':sc})
#         emp_dict = {}
#         content = []
#         ft_yearly = frappe.get_all("Tiips", {'parent': emp.name}, ['ft_value'])[0]
#         april_month = (datetime.today()).strftime("%Y-04-01")
#         last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
#         if emp.short_code =='API':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services in ("IT-SW","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
            
#         if emp.short_code == 'SBMK':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services ="TFP" AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
           
#         if emp.short_code == 'SP':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services  in ("TGT","EMS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
           
#         if emp.short_code == 'AS':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services not in ("TFP","IT-SW","TGT","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
         
#         ft = ft_yearly['ft_value']
#         month_april = datetime.strptime(april_month,"%Y-%m-%d")
#         now = datetime.now()
#         today_date = now.strftime("%Y-%m-%d")
#         today = datetime.strptime(today_date,"%Y-%m-%d")
        
#         balance_months = (today.year - month_april.year) * 12 + (today.month - month_april.month)
#         balance = 12 - balance_months
#         if acheieved_till_date['total']:
#             ft_actual = (ft - acheieved_till_date['total'])/ balance
#         else :
#             ft_actual = (ft - 0)/ balance
#         ft_monthly = round(ft_actual,2)
     
#         d = 0
#         e = 0
#         service_closure = 0
#         service_si = 0
#         total_value = 0
#         acc_si = []
#         dev_si = []
#         both_si = []
#         services = []
        
#         try:
#             if emp.based_on_value == "Service Based":
#                 services = frappe.get_all("Employee services", {'parent': emp.name}, ['services'])
                               
#                 service_list = []
#                 for s in services:
#                     service_list.append(s.services)
#                 str_list = str(service_list).strip('[')
#                 str_list = str(str_list).strip(']')
                
#                 if service_list:
#                     service_si  = frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services IN (%s) AND month(creation) = '%s' AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND YEAR(creation) = '%s'""" % (
#                         str_list,month,year),as_dict=True)
                    
#                     total_value += flt(service_si[0].total)
                    
#                     if set(["REC-I","REC-D"]).intersection(set(service_list)):
#                         service_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE month(so_confirmed_date) = '%s' AND so_created = 1 AND YEAR(so_confirmed_date) ='%s'""" % 
#                         (month,year),as_dict=True)
                        
#                 total_value = flt(service_si[0].total) + flt(service_closure[0].charges) #C
                
#         except TypeError:
#             closure = 0
#             s = ''
#         if total_value and ft_monthly:
#             d = int(total_value) - int(ft_monthly) #C-B
#             e = (int(total_value) /int(ft_monthly))*100  #C-B *100
#         emp_dict['image'] = emp.image
#         emp_dict['ft_monthly'] = round(ft_monthly)
#         emp_dict['total_value'] = round(total_value)
#         emp_dict['d'] = round(d)
#         emp_dict['e'] = round(e)
#         for key, value in emp_dict.items() :
#             print (key, value)
#         employee_data.append(emp_dict.copy())
        
        

#     data += employee_data
   
#     return data

# @frappe.whitelist()
# def get_sc_value_bt(month=None,year =None):
#     data = []
#     employee_data = []
#     short_code = ['AS','API','SP','SBMK']
#     for sc in short_code:
#         emp = frappe.get_doc("Employee",{'status':'Active','tiip_employee':'1','short_code':sc})
#         emp_dict = {}
#         content = []
#         bt_yearly = frappe.get_all("Tiips", {'parent': emp.name}, ['bt_value'])[0]
#         april_month = (datetime.today()).strftime("%Y-04-01")
#         last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
#         if emp.short_code =='API':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services in ("IT-SW","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
            
#         if emp.short_code == 'SBMK':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services ="TFP" AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
           
#         if emp.short_code == 'SP':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services in ("TGT","EMS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
#         if emp.short_code == 'AS':
#             acheieved_till_date =frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services not in ("TFP","IT-SW","TGT","IT-IS") AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND creation between '%s' and '%s' """ %(april_month,last_day_of_prev_month),as_dict=True)[0]
         
#         bt = bt_yearly['bt_value']
#         month_april = datetime.strptime(april_month,"%Y-%m-%d")
#         now = datetime.now()
#         today_date = now.strftime("%Y-%m-%d")
#         today = datetime.strptime(today_date,"%Y-%m-%d")
        
#         balance_months = (today.year - month_april.year) * 12 + (today.month - month_april.month)
#         balance = 12 - balance_months
#         if acheieved_till_date['total']:
#             bt_actual = (bt - acheieved_till_date['total'])/ balance
#         else :
#             bt_actual = (bt - 0)/ balance
#         bt_monthly = round(bt_actual,2)
     
#         d = 0
#         e = 0
#         service_closure = 0
#         service_si = 0
#         total_value = 0
#         acc_si = []
#         dev_si = []
#         both_si = []
#         services = []
        
#         try:
#             if emp.based_on_value == "Service Based":
#                 services = frappe.get_all("Employee services", {'parent': emp.name}, ['services'])
                               
#                 service_list = []
#                 for s in services:
#                     service_list.append(s.services)
#                 str_list = str(service_list).strip('[')
#                 str_list = str(str_list).strip(']')
                
#                 if service_list:
#                     service_si  = frappe.db.sql("""select sum(total_sc_company_currency) as total from`tabSales Invoice` WHERE services IN (%s) AND month(creation) = '%s' AND status in ("Paid","Overdue","Unpaid","Partly Paid","Draft") AND YEAR(creation) = '%s'""" % (
#                         str_list,month,year),as_dict=True)
                    
#                     total_value += flt(service_si[0].total)
                    
#                     if set(["REC-I","REC-D"]).intersection(set(service_list)):
#                         service_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE month(so_confirmed_date) = '%s' AND so_created = 1 AND YEAR(so_confirmed_date) ='%s'""" % 
#                         (month,year),as_dict=True)
                        
#                 total_value = flt(service_si[0].total) + flt(service_closure[0].charges) #C
                
#         except TypeError:
#             closure = 0
#             s = ''
#         if total_value and bt_monthly:
#             d = int(total_value) - int(bt_monthly) #C-B
#             e = (int(total_value) /int(bt_monthly))*100  #C-B *100
#         emp_dict['image'] = emp.image
#         emp_dict['bt_monthly'] = round(bt_monthly)
#         emp_dict['total_value'] = round(total_value)
#         emp_dict['d'] = round(d)
#         emp_dict['e'] = round(e)
#         for key, value in emp_dict.items() :
#             print (key, value)
#         employee_data.append(emp_dict.copy())
        

#     data += employee_data
#     return data