# -*- coding: utf-8 -*-
# Copyright (c) 2021, Saru and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt


class TIIP(Document):
    def get_all_employees(self):
        self.target =[]
        self.tiips =[]
        emp = frappe.get_all(
            "Employee", ["employee_name", "name", "prefered_email", "tiips_role"])
        get = []
        si =0
        closure =0
        if self.quarterly == "1":
            start = 1 ;end =3
        elif self.quarterly == "2":
            start = 4 ;end =6
        elif self.quarterly == "3":
            start = 7 ;end =9
        elif self.quarterly == "4":
            start = 10 ;end =12
        for e in emp:
            frappe.errprint(e.employee_name)
            get_bt=frappe.get_value(
                "Tiips", {'parent': e.name,'quarterly':self.quarterly,'year':self.year}, ['quarterly','year','bt'])
            try:
                if e.tiips_role == "Account Manager":
                    si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE account_manager = '%s'  AND month(posting_date) BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND year(posting_date) = '%s'""" % (
                        e.prefered_email,start,end,self.year),as_dict=True)
                    # frappe.errprint(si)
                    closure =frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE account_manager = '%s'  AND month(so_confirmed_date) BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND year(so_confirmed_date) ='%s'""" % (
                        e.prefered_email,start,end,self.year),as_dict=True)
                    # frappe.errprint(closure)
                    
                elif e.tiips_role == "Delivery Manager":
                    si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE delivery_manager = '%s'  AND month(posting_date) BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND year(posting_date) = '%s' """ % (
                        e.prefered_email, start,end,self.year),as_dict=True)
                    closure =frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE candidate_owner = '%s'  AND month(so_confirmed_date) BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND year(so_confirmed_date) ='%s'""" % (
                        e.prefered_email,start,end,self.year),as_dict=True)
                    frappe.errprint("dev")
                    # frappe.errprint(closure)
            except TypeError:
                closure = 0
            ssa = frappe.get_value("Salary Structure Assignment", {
                'employee': e.name}, ['base'])
            # frappe.errprint(ssa)
            ft_time = frappe.get_value(
                "Tiips", {'parent': e.name,"quarterly":self.quarterly,"year":self.year}, ['ft_times'])
            sl = si[0].total
            if ssa:
                if ft_time:
                    quarter = int(ssa) * int(ft_time)
                    total = 0
                    if self.period == "Quarterly":
                        total = quarter
                    elif self.period == "Monthly":
                        total = quarter/3
                    else:
                        total = quarter * 4
                    # if closure[0].charges is not None:
                    self.append("target",{
                        "data_1": e.employee_name,
                        "goal": total,
                        "role": e.tiips_role,
                        "achieved": flt(sl) + flt(closure[0].charges),
                        "pending": flt(total) - flt(sl),
                        "achieved_percentage" :(flt(sl)/flt(total))*100
                        })
                    self.append("tiips",{
                        "employee_name":e.employee_name,
                        "quarterly":get_bt[0],
                        "year":get_bt[1],
                        "bt":get_bt[2]
                    })
                # frappe.errprint(flt(sl))
                # frappe.errprint(flt(total))
                # return goal,achieved


# @frappe.whitelist()
# def get_ft(employee_name, period,name):
#     ssa = frappe.get_value("Salary Structure Assignment", {
#                            'employee_name': employee_name}, ['base'])
#     ft_time = frappe.get_value(
#                 "Tiips", {'parent': name,"quarterly":"1","year":"2020"}, ['ft_times'])
#     frappe.errprint(ft_time)
#     if ssa:
#         if ft_time:
#             quarter = int(ssa) * int(ft_time)
#             return quarter


# @frappe.whitelist()
# def get_achieved(employee_name, period, from_period, to, employee_mail):
#     account_manager = 0
#     delivery_manager = 0
#     am_dm = 0
#     am = frappe.db.sql("""select sum(total) as total from`tabSales Invoice` WHERE account_manager = '%s' AND delivery_manager != '%s' AND posting_date BETWEEN '%s' and '%s' """ % (
#         employee_mail, employee_mail, from_period, to))
#     dm = frappe.db.sql("""select sum(total) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager != '%s' AND posting_date BETWEEN '%s' and '%s' """ % (
#         employee_mail, employee_mail, from_period, to))
#     both = frappe.db.sql("""select sum(total) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager = '%s' AND posting_date BETWEEN '%s' and '%s' """ % (
#         employee_mail, employee_mail, from_period, to))
#     # total=am[0]+dm[0]+both[0]
#     # account_manager = am[0][0]
#     # delivery_manager = dm[0][0]
#     # am_dm = both[0][0]
#     if am[0][0]:
#         account_manager = am[0][0]
#     if dm[0][0]:
#         delivery_manager = dm[0][0]
#     if both[0][0]:
#         am_dm = both[0][0]
#     total = int(account_manager) + int(delivery_manager) + int(am_dm)
#     # frappe.errprint(account_manager)
#     # frappe.errprint(delivery_manager)
#     # frappe.errprint(total)
#     return total

# @frappe.whitelist()
# def get_bt(employee_name):
# 	bt =frappe.get_value("Employee",{'employee_name':employee_name})
# 	frappe.errprint(bt)

# si = 0
            #
            # both = frappe.db.sql("""select sum(total) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager = '%s' AND posting_date BETWEEN '%s' and '%s' """ % (
            #     e.prefered_email, e.prefered_email, self.from_period, self.to))
