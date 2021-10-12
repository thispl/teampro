# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe.model.document import Document
from datetime import date

class TIIPEmployee(Document):
    def get_all_employees(self):
    #     self.sales_invoice =[]
    #     self.analytical_section =[]
    #     email = frappe.db.get_value("Employee",self.employee_id,["prefered_email"])
    #     get_si = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer from`tabSales Invoice` WHERE account_manager = '%s' or delivery_manager = '%s' """ % (email,email),as_dict=True)
    #     for get in get_si:
    #         self.append("sales_invoice",{
    #             "si_no": get.name,
    #             "grand_total":get.total,
    #             "total_sc":get.total_dec,
    #             "date":get.posting_date,
    #             "client_name":get.customer,
    #             "outstanding_amount":get.outstanding_amount
    #         }).save(ignore_permissions=True)
    #     frappe.db.commit()
        get_tiip = frappe.get_value("Tiips", {'parent': self.employee_id}, ['year','ft_value','bt_value','at_value'])
        # frappe.errprint(get_tiip[0])
        self.append("analytical_section",{
            "year":get_tiip[0],
            "ft":get_tiip[1],
            "bt":get_tiip[2],
            "at":get_tiip[3]
        }).save(ignore_permissions=True)
        frappe.db.commit()
    def get_data(self):
        self.sales_invoice =[]
        service = frappe.db.get_value("Employee",self.employee_id,["based_on_value"])
        if service == "Role Based":
            email = frappe.db.get_value("Employee",self.employee_id,["prefered_email"])
            get_si = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
            from`tabSales Invoice` 
            WHERE (account_manager = '%s' 
            AND posting_date BETWEEN '%s' and '%s'
            AND status in ("Paid","Overdue","Unpaid") )
            OR (delivery_manager = '%s' 
            AND posting_date BETWEEN '%s' and '%s'
            AND status in ("Paid","Overdue","Unpaid") )"""
                % (email,self.from_date,self.to_date,email,self.from_date,self.to_date),as_dict=True)
            # get_si = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
            # from`tabSales Invoice` 
            # WHERE (account_manager = '%s' 
            # AND posting_date BETWEEN '%s' and '%s'
            # AND status in ("Paid","Overdue","Unpaid") )
            # AND (delivery_manager = '%s' 
            # AND posting_date BETWEEN '%s' and '%s'
            # AND status in ("Paid","Overdue","Unpaid") )"""
            #     % (email,self.from_date,self.to_date,email,self.from_date,self.to_date),as_dict=True)
            get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si 
            from `tabClosure` 
            WHERE (candidate_owner = '%s'
            AND so_confirmed_date BETWEEN '%s' and '%s' 
            AND collection_status in ("PAID"))
            OR (account_manager = '%s' 
            AND so_confirmed_date BETWEEN '%s' and '%s' 
            AND collection_status in ("PAID"))""" 
            % (email,self.from_date,self.to_date,email,self.from_date,self.to_date),as_dict=True)
        elif service == "Service Based":
            frappe.errprint("service")
            services = frappe.get_all("Employee services",  {'parent': self.employee_id},['services'])
            frappe.errprint(services)
            # s = services[0].services
            service_list = []
            for s in services:
                service_list.append(s.services)
            str_list = str(service_list).strip('[')
            str_list = str(str_list).strip(']')
            # frappe.errprint(str_list)
            if service_list:
                get_closure = 0
                get_si = 0
                # for s in services:
                # frappe.errprint(s.services)
                get_si  = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
                from`tabSales Invoice` 
                WHERE services IN (%s) 
                AND posting_date BETWEEN '%s' and '%s' 
                AND status in ("Paid","Overdue","Unpaid") """ % (
                    str_list,self.from_date,self.to_date),as_dict=True)
                frappe.errprint(get_si)
                # total_value += flt(service_si[0].total)
                # frappe.errprint(total_value)
                if set(["REC-I","REC-D"]).intersection(set(service_list)):
                    get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si
                    from `tabClosure` 
                    WHERE so_confirmed_date BETWEEN '%s' and '%s' 
                    AND collection_status in ("PAID")""" 
                    % (self.from_date,self.to_date),as_dict=True)

        # frappe.errprint(get_si[0])
        for get in get_si:
            self.append("sales_invoice",{
                "si_no": get.name,
                "grand_total":get.total,
                "total_sc":get.total_dec,
                "date":get.posting_date,
                "client_name":get.customer,
                "outstanding_amount":get.outstanding_amount
            }).save(ignore_permissions=True)
        frappe.db.commit()
        if get_closure:
            for get in get_closure:
                self.append("sales_invoice",{
                    "si_no": get.given_name,
                    "grand_total":get.candidate_si,
                    "total_sc":get.candidate_service_charge,
                    "date":get.so_confirmed_date,
                    "client_name":get.customer,
                    "outstanding_amount":get.outstanding_amount
                }).save(ignore_permissions=True)
            frappe.db.commit()

    def get_data_monthly(self):
        # value = 0
        self.sales_invoice =[]
        today = date.today()
        year = today.year
        if self.monthly == "Jan":
            value = 1
        elif self.monthly == "Feb":
            value = 2
        elif self.monthly == "March":
            value = 3
        
        elif self.monthly == "April":
            value = 4
        
        elif self.monthly == "May":
            value = 5
        
        elif self.monthly == "June":
            value = 6
        

        elif self.monthly == "July":
            value = 7
        
        elif self.monthly == "Aug":
            value = 8
        
        elif self.monthly == "Sep":
            value = 9
        
        elif self.monthly == "Oct":
            value = 10
        
        elif self.monthly == "Nov":
            value = 11
        
        elif self.monthly == "Dec":
            value = 12
        
        service = frappe.db.get_value("Employee",self.employee_id,["based_on_value"])
        if service == "Role Based":
            email = frappe.db.get_value("Employee",self.employee_id,["prefered_email"])
            get_si = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
            from`tabSales Invoice` 
            WHERE (account_manager = '%s' 
            AND month(posting_date) = '%s'
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )
            OR (delivery_manager = '%s' 
            AND month(posting_date) = '%s'
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )"""
                % (email,value,year,email,value,year),as_dict=True)
            get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si 
            from `tabClosure` 
            WHERE (candidate_owner = '%s'
            AND month(so_confirmed_date) = '%s'
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))
            OR (account_manager = '%s' 
            AND month(so_confirmed_date) = '%s'
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))""" 
            % (email,value,year,email,value,year),as_dict=True)
        elif service == "Service Based":
            frappe.errprint("service")
            services = frappe.get_all("Employee services",  {'parent': self.employee_id},['services'])
            frappe.errprint(services)
            # s = services[0].services
            service_list = []
            for s in services:
                service_list.append(s.services)
            str_list = str(service_list).strip('[')
            str_list = str(str_list).strip(']')
            # frappe.errprint(str_list)
            if service_list:
                get_closure = 0
                get_si = 0
                # for s in services:
                # frappe.errprint(s.services)
                get_si  = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
                from`tabSales Invoice` 
                WHERE services IN (%s) 
                AND month(posting_date) = '%s'
                AND year(posting_date) = '%s'
                AND status in ("Paid","Overdue","Unpaid") """ % (
                    str_list,value,year),as_dict=True)
                frappe.errprint(get_si)
                # total_value += flt(service_si[0].total)
                # frappe.errprint(total_value)
                if set(["REC-I","REC-D"]).intersection(set(service_list)):
                    get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si
                    from `tabClosure` WHERE
                    month(so_confirmed_date) = '%s'
                    AND year(so_confirmed_date) = '%s'
                    AND collection_status in ("PAID")""" 
                    % (value,year),as_dict=True)
        # frappe.errprint(get_si)
        for get in get_si:
            self.append("sales_invoice",{
                "si_no": get.name,
                "grand_total":get.total,
                "total_sc":get.total_dec,
                "date":get.posting_date,
                "client_name":get.customer,
                "outstanding_amount":get.outstanding_amount
            }).save(ignore_permissions=True)
        frappe.db.commit()
        if get_closure:
            for get in get_closure:
                self.append("sales_invoice",{
                    "si_no": get.given_name,
                    "grand_total":get.candidate_si,
                    "total_sc":get.candidate_service_charge,
                    "date":get.so_confirmed_date,
                    "client_name":get.customer,
                    "outstanding_amount":get.outstanding_amount
                }).save(ignore_permissions=True)
            frappe.db.commit()

    def get_data_quarterly(self):
        # value = 0
        self.sales_invoice =[]
        today = date.today()
        year = today.year
        if self.quarterly == "Q1":
            start = 1 ;end =3
        elif self.quarterly == "Q2":
            start = 4 ;end =6
        elif self.quarterly == "Q3":
            start = 7 ;end =9
        elif self.quarterly == "Q4":
            start = 10 ;end =12
        service = frappe.db.get_value("Employee",self.employee_id,["based_on_value"])
        if service == "Role Based":
            email = frappe.db.get_value("Employee",self.employee_id,["prefered_email"])
            get_si = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
            from`tabSales Invoice` 
            WHERE (account_manager = '%s' 
            AND month(posting_date) BETWEEN '%s' and '%s'
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )
            OR (delivery_manager = '%s' 
            AND month(posting_date) BETWEEN '%s' and '%s'
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )"""
                % (email,start,end,year,email,start,end,year),as_dict=True)
            get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si 
            from `tabClosure` 
            WHERE (candidate_owner = '%s'
            AND month(so_confirmed_date) BETWEEN '%s' and '%s'
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))
            OR (account_manager = '%s' 
            AND month(so_confirmed_date) BETWEEN '%s' and '%s'
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))""" 
            % (email,start,end,year,email,start,end,year),as_dict=True)
        elif service == "Service Based":
            frappe.errprint("service")
            services = frappe.get_all("Employee services",  {'parent': self.employee_id},['services'])
            frappe.errprint(services)
            # s = services[0].services
            service_list = []
            for s in services:
                service_list.append(s.services)
                frappe.errprint(service_list)
            str_list = str(service_list).strip('[')
            str_list = str(str_list).strip(']')
            # frappe.errprint(str_list)
            if service_list:
                get_closure = 0
                get_si = 0
                # for s in services:
                # frappe.errprint(s.services)
                get_si  = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
                from`tabSales Invoice` 
                WHERE services IN (%s) 
                AND month(posting_date) BETWEEN '%s' and '%s'
                And year(posting_date) = '%s'
                AND status in ("Paid","Overdue","Unpaid") """ % (
                    str_list,start,end,year),as_dict=True)
                frappe.errprint(get_si)
                # total_value += flt(service_si[0].total)
                # frappe.errprint(total_value)
                frappe.errprint(service_list)
                if set(["REC-I","REC-D"]).intersection(set(service_list)):
                    frappe.errprint("hiii")
                    get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si
                    from `tabClosure` WHERE
                    month(so_confirmed_date) BETWEEN '%s' and '%s'
                    AND year(so_confirmed_date) = '%s'
                    AND collection_status in ("PAID")""" 
                    % (start,end,year),as_dict=True)
                    frappe.errprint(get_closure)
        for get in get_si:
            self.append("sales_invoice",{
                "si_no": get.name,
                "grand_total":get.total,
                "total_sc":get.total_dec,
                "date":get.posting_date,
                "client_name":get.customer,
                "outstanding_amount":get.outstanding_amount
            }).save(ignore_permissions=True)
        frappe.db.commit()
        if get_closure:
            for get in get_closure:
                self.append("sales_invoice",{
                    "si_no": get.given_name,
                    "grand_total":get.candidate_si,
                    "total_sc":get.candidate_service_charge,
                    "date":get.so_confirmed_date,
                    "client_name":get.customer,
                    "outstanding_amount":get.outstanding_amount
                }).save(ignore_permissions=True)
            frappe.db.commit()
    def get_data_half_yearly(self):
        # value = 0
        self.sales_invoice =[]
        today = date.today()
        year = today.year
        if self.half_yearly == "H1":
            start = 1 ;end =6
        elif self.half_yearly == "H2":
            start = 7 ;end =12
        service = frappe.db.get_value("Employee",self.employee_id,["based_on_value"])
        if service == "Role Based":
            email = frappe.db.get_value("Employee",self.employee_id,["prefered_email"])
            get_si = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
            from`tabSales Invoice` 
            WHERE (account_manager = '%s' 
            AND month(posting_date) BETWEEN '%s' and '%s'
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )
            OR (delivery_manager = '%s' 
            AND month(posting_date) BETWEEN '%s' and '%s'
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )"""
                % (email,start,end,year,email,start,end,year),as_dict=True)
            get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si 
            from `tabClosure` 
            WHERE (candidate_owner = '%s'
            AND month(so_confirmed_date) BETWEEN '%s' and '%s'
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))
            OR (account_manager = '%s' 
            AND month(so_confirmed_date) BETWEEN '%s' and '%s'
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))""" 
            % (email,start,end,year,email,start,end,year),as_dict=True)
        elif service == "Service Based":
            frappe.errprint("service")
            services = frappe.get_all("Employee services",  {'parent': self.employee_id},['services'])
            frappe.errprint(services)
            # s = services[0].services
            service_list = []
            for s in services:
                service_list.append(s.services)
            str_list = str(service_list).strip('[')
            str_list = str(str_list).strip(']')
            frappe.errprint(str_list)
            if service_list:
                get_closure = 0
                get_si = 0
                # for s in services:
                # frappe.errprint(s.services)
                get_si  = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
                from`tabSales Invoice` 
                WHERE services IN (%s) 
                AND month(posting_date) BETWEEN '%s' and '%s'
                And year(posting_date) = '%s'
                AND status in ("Paid","Overdue","Unpaid") """ % (
                    str_list,start,end,year),as_dict=True)
                frappe.errprint(get_si)
                # total_value += flt(service_si[0].total)
                # frappe.errprint(total_value)
                if set(["REC-I","REC-D"]).intersection(set(service_list)):
                    frappe.errprint("hi rec")
                    get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si
                    from `tabClosure` WHERE
                    month(so_confirmed_date) BETWEEN '%s' and '%s'
                    AND year(so_confirmed_date) = '%s'
                    AND collection_status in ("PAID")""" 
                    % (start,end,year),as_dict=True)
        # frappe.errprint(get_si)
        for get in get_si:
            self.append("sales_invoice",{
                "si_no": get.name,
                "grand_total":get.total,
                "total_sc":get.total_dec,
                "date":get.posting_date,
                "client_name":get.customer,
                "outstanding_amount":get.outstanding_amount
            }).save(ignore_permissions=True)
        frappe.db.commit()
        if get_closure:
            for get in get_closure:
                self.append("sales_invoice",{
                    "si_no": get.given_name,
                    "grand_total":get.candidate_si,
                    "total_sc":get.candidate_service_charge,
                    "date":get.so_confirmed_date,
                    "client_name":get.customer,
                    "outstanding_amount":get.outstanding_amount
                }).save(ignore_permissions=True)
            frappe.db.commit()
    def get_data_yearly(self):
        
        self.sales_invoice =[]
      
        service = frappe.db.get_value("Employee",self.employee_id,["based_on_value"])
        if service == "Role Based":
            email = frappe.db.get_value("Employee",self.employee_id,["prefered_email"])
            get_si = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
            from`tabSales Invoice` 
            WHERE (account_manager = '%s' 
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )
            OR (delivery_manager = '%s' 
            And year(posting_date) = '%s'
            AND status in ("Paid","Overdue","Unpaid") )"""
                % (email,self.yearly,email,self.yearly),as_dict=True)
            get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si 
            from `tabClosure` 
            WHERE (candidate_owner = '%s'
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))
            OR (account_manager = '%s' 
            AND year(so_confirmed_date) = '%s'
            AND collection_status in ("PAID"))""" 
            % (email,self.yearly,email,self.yearly),as_dict=True)
        elif service == "Service Based":
            frappe.errprint("service")
            services = frappe.get_all("Employee services",  {'parent': self.employee_id},['services'])
            frappe.errprint(services)
            # s = services[0].services
            service_list = []
            for s in services:
                service_list.append(s.services)
            str_list = str(service_list).strip('[')
            str_list = str(str_list).strip(']')
            # frappe.errprint(str_list)
            if service_list:
                get_closure = 0
                get_si = 0
                # for s in services:
                # frappe.errprint(s.services)
                get_si  = frappe.db.sql("""select total_dec,name,total,posting_date,outstanding_amount,customer 
                from`tabSales Invoice` 
                WHERE services IN (%s) 
                And year(posting_date) = '%s'
                AND status in ("Paid","Overdue","Unpaid") """ % (
                    str_list,self.yearly),as_dict=True)
                frappe.errprint(get_si)
                # total_value += flt(service_si[0].total)
                # frappe.errprint(total_value)
                if set(["REC-I","REC-D"]).intersection(set(service_list)):
                    get_closure = frappe.db.sql("""select candidate_service_charge,given_name,customer,so_confirmed_date,outstanding_amount,candidate_si
                    from `tabClosure` WHERE
                    year(so_confirmed_date) = '%s'
                    AND collection_status in ("PAID")""" 
                    % (self.yearly),as_dict=True)
        # frappe.errprint(get_si)
        for get in get_si:
            self.append("sales_invoice",{
                "si_no": get.name,
                "grand_total":get.total,
                "total_sc":get.total_dec,
                "date":get.posting_date,
                "client_name":get.customer,
                "outstanding_amount":get.outstanding_amount
            }).save(ignore_permissions=True)
        frappe.db.commit()
        if get_closure:
            for get in get_closure:
                self.append("sales_invoice",{
                    "si_no": get.given_name,
                    "grand_total":get.candidate_si,
                    "total_sc":get.candidate_service_charge,
                    "date":get.so_confirmed_date,
                    "client_name":get.customer,
                    "outstanding_amount":get.outstanding_amount
                }).save(ignore_permissions=True)
            frappe.db.commit()