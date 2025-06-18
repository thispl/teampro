# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from datetime import datetime, date
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import calendar

def execute(filters=None):
    if not filters:
        filters = {}
    data = []
    columns = get_column()
    # conditions = get_conditions(filters)
    data = get_employee(filters)
    # for employee in employee_list:
    # 	data.append(employee)
    return columns,data

def get_column():
    return [_("Employee") + "::120",
    _("Employee Name") + "::150",
    _("Achieved") + "::150",
    _("FT-Value") + "::150",
    _("FT-Pending") + "::150",
    _("FT-Strike Rate") + "::150",
    _("AT-Value") + "::150",
    _("AT-Pending") + "::150",
    _("AT-Strike Rate") + "::150",
    _("BT-Value") + "::150",
    _("BT-Pending") + "::150",
    _("BT-Strike Rate") + "::150"
   
    ]

def get_employee(filters):
    row=[]
    employee = frappe.get_all("Employee",{"status": "Active","employment_type":"Full-time"},["*"])
    for emp in employee:
        total_value = 0
        acc_si = []
        dev_si = []
        both_si = []
        services = []
        ft_strike_rate = 0
        bt_strike_rate = 0
        at_strike_rate = 0
        service_closure = 0
        service_si = 0
       
        ft = frappe.get_all("Tiips", {'parent': emp.name}, ['ft_value','bt_value','at_value'])
        from_date = filters.from_date
        to_date = filters.to_date
        if filters.yearly:
            from_date = filters.yearly + '-01-01'
            to_date =  filters.yearly + '-12-31'
        if filters.half_yearly == 'H1':
            from_date = filters.yearly + '-01-01'
            to_date =  filters.yearly + '-06-30'

        if filters.half_yearly == 'H2':
            from_date = filters.yearly + '-07-01'
            to_date =  filters.yearly + '-12-31'
        
        if filters.quarterly == 'Q1':
            from_date = filters.yearly + '-01-01'
            to_date =  filters.yearly + '-03-31'

        if filters.quarterly == 'Q2':
            from_date = filters.yearly + '-04-01'
            to_date =  filters.yearly + '-06-30'
        
        if filters.quarterly == 'Q3':
            from_date = filters.yearly + '-07-01'
            to_date =  filters.yearly + '-09-30'
        
        if filters.quarterly == 'Q4':
            from_date = filters.yearly + '-10-01'
            to_date =  filters.yearly + '-12-31'
        if filters.month:
            total_days_in_month = monthrange(cint(filters.yearly), cint(filters.month))[1]
            # month_range = calendar.monthrange(filters.year, filters.month)
            # start_date = datetime.datetime(1,filters.month,filters.yearly)
            from_date = date(cint(filters.yearly),cint(filters.month),1)
            to_date = date(cint(filters.yearly),cint(filters.month),total_days_in_month)
        # end_date = (total_days_in_month,filters.month,filters.yearly)
        try:
            if emp.based_on_value == "Role Based":
                
                acc_si  = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE account_manager = '%s' AND delivery_manager != '%s'  AND posting_date BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND YEAR(posting_date) = '%s'""" % (
                    emp.prefered_email,emp.prefered_email,from_date,to_date,filters.yearly),as_dict=True)

                dev_si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager != '%s' AND posting_date BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND YEAR(posting_date) = '%s'""" % (
                    emp.prefered_email,emp.prefered_email,from_date,to_date,filters.yearly),as_dict=True)
                
                both_si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager = '%s' AND posting_date BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND YEAR(posting_date) = '%s'""" % (
                    emp.prefered_email,emp.prefered_email,from_date,to_date,filters.yearly),as_dict=True)
                acc_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE account_manager = '%s' AND  candidate_owner != '%s' AND so_confirmed_date BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND YEAR(so_confirmed_date) ='%s'""" % (
                    emp.prefered_email,emp.prefered_email,from_date,to_date,filters.yearly),as_dict=True)

                dev_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE candidate_owner = '%s'  AND account_manager != '%s'AND so_confirmed_date BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND YEAR(so_confirmed_date) ='%s'""" % (
                    emp.prefered_email,emp.prefered_email,from_date,to_date,filters.yearly),as_dict=True)
                total_value =flt(acc_si[0].total )+flt( dev_si[0].total) + flt( both_si[0].total) + flt(acc_closure[0].charges ) + flt(dev_closure[0].charges )

            elif emp.based_on_value == "Service Based":
                
                services = frappe.get_all("Employee services", {'parent': emp.name}, ['services'])
                # s = services[0].services
                service_list = []
                for s in services:
                    service_list.append(s.services)
                str_list = str(service_list).strip('[')
                str_list = str(str_list).strip(']')
                if service_list:
                    
                    # for s in services:
                    service_si  = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE services IN (%s) AND posting_date BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND YEAR(posting_date) = '%s'""" % (
                        str_list,from_date,to_date,filters.yearly),as_dict=True)
                    total_value += flt(service_si[0].total)
                    if set(["REC-I","REC-D"]).intersection(set(service_list)):
                        service_closure = frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE so_confirmed_date BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND YEAR(so_confirmed_date) ='%s'""" % (from_date,to_date,filters.yearly),as_dict=True)
                        
                total_value = flt(service_si[0].total) + flt(service_closure[0].charges)
        
        except TypeError:
            closure = 0
            s = ''

        ft_pending = flt(ft[0].ft_value) - flt(total_value)
        bt_pending = flt(ft[0].bt_value) - flt(total_value)
        at_pending = flt(ft[0].at_value) - flt(total_value)
        if total_value:
            ft_sr = (flt(total_value)/flt(ft[0].ft_value))*100
            ft_strike_rate = round(ft_sr)
            bt_sr = (flt(total_value)/flt(ft[0].bt_value) )*100
            bt_strike_rate = round(bt_sr)
            if flt(ft[0].at_value) > 0:
                at_sr = (flt(total_value)/ flt(ft[0].at_value))*100
                at_strike_rate = round(at_sr)
            else:
                at_strike_rate = 0


        row += [(emp.name,emp.employee_name,round(total_value),
                round(ft[0].ft_value),round(ft_pending),str(ft_strike_rate) + "%",
                (ft[0].at_value),(at_pending),str(at_strike_rate) + "%",
                round(ft[0].bt_value),round(bt_pending),str(bt_strike_rate) + "%"
                )]
    return row

# def get_conditions(filters):
# 	conditions = ""
# 	if filters.get()




#  