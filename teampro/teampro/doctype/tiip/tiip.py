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
            "Employee", {"status":"Active","employment_type":"Full-time"},["employee_name", "name", "prefered_email", "tiips_role","reports_to"])
        get = []
        si =0
        closure =0
        # node_goal =0
        # node_si =0
        # node_closure = 0
        # si_amount = 0
        # closure_amount = 0
        if self.quarterly == "1":
            start = 1 ;end =3
        elif self.quarterly == "2":
            start = 4 ;end =6
        elif self.quarterly == "3":
            start = 7 ;end =9
        elif self.quarterly == "4":
            start = 10 ;end =12
        for e in emp:
            si_amount = 0
            closure_amount = 0
            
            get_bt=frappe.get_value(
                "Tiips", {'parent': e.name,'quarterly':self.quarterly,'year':self.year}, ['quarterly','year','bt'])
            try:
                if e.tiips_role == "Account Manager":
                    si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE account_manager = '%s'  AND month(posting_date) BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND year(posting_date) = '%s'""" % (
                        e.prefered_email,start,end,self.year),as_dict=True)
                    closure =frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE account_manager = '%s'  AND month(so_confirmed_date) BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND year(so_confirmed_date) ='%s'""" % (
                        e.prefered_email,start,end,self.year),as_dict=True)
                    
                elif e.tiips_role == "Delivery Manager":
                    si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE delivery_manager = '%s'  AND month(posting_date) BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND year(posting_date) = '%s' """ % (
                        e.prefered_email, start,end,self.year),as_dict=True)
                    closure =frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE candidate_owner = '%s'  AND month(so_confirmed_date) BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND year(so_confirmed_date) ='%s'""" % (
                        e.prefered_email,start,end,self.year),as_dict=True)
            except TypeError:
                closure = 0
            node_goal =0
            node_si =0
            node_closure = 0
            emp_node = frappe.get_all(
            "Employee", {"status":"Active","employment_type":"Full-time","reports_to":e.name},["employee_name", "name", "prefered_email", "tiips_role","reports_to"])
            for node in emp_node:
                get_bt=frappe.get_value(
                        "Tiips", {'parent': node.name,'quarterly':self.quarterly,'year':self.year}, ['quarterly','year','bt'])
                # try:
                if node.tiips_role == "Account Manager":
                    node_si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE account_manager = '%s'  AND month(posting_date) BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND year(posting_date) = '%s'""" % (
                        node.prefered_email,start,end,self.year),as_dict=True)
                    si_amount += flt(node_si[0].total)
                    node_closure =frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE account_manager = '%s'  AND month(so_confirmed_date) BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND year(so_confirmed_date) ='%s'""" % (
                        node.prefered_email,start,end,self.year),as_dict=True)
                    closure_amount += flt(node_closure[0].charges)
                if node.tiips_role == "Delivery Manager":
                    node_si = frappe.db.sql("""select sum(total_dec) as total from`tabSales Invoice` WHERE delivery_manager = '%s'  AND month(posting_date) BETWEEN '%s' and '%s' AND status in ("Paid","Overdue","Unpaid") AND year(posting_date) = '%s' """ % (
                        node.prefered_email, start,end,self.year),as_dict=True)
                    si_amount += flt(node_si[0].total)
                    node_closure =frappe.db.sql("""select sum(candidate_service_charge) as charges from `tabClosure` WHERE candidate_owner = '%s'  AND month(so_confirmed_date) BETWEEN '%s' and '%s' AND collection_status in ("PAID") AND year(so_confirmed_date) ='%s'""" % (
                        node.prefered_email,start,end,self.year),as_dict=True)
                    closure_amount += flt(node_closure[0].charges)
                ssa = frappe.get_value("Salary Structure Assignment", {'employee': node.name}, ['base'])
                ft_time = frappe.get_value("Tiips", {'parent': node.name,"quarterly":self.quarterly,"year":self.year}, ['ft_times'])
                if ssa:
                    if ft_time:
                        quarter = int(ssa) * int(ft_time)
                        node_goal += 0
                        if self.period == "Quarterly":
                            node_goal += quarter
                        elif self.period == "Monthly":
                            node_goal += quarter/3
                        else:
                            node_goal += quarter * 4
            ssa = frappe.get_value("Salary Structure Assignment", {
                'employee': e.name}, ['base'])
            ft_time = frappe.get_value("Tiips", {'parent': e.name,"quarterly":self.quarterly,"year":self.year}, ['ft_times'])
            # sl = si[0].total
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
                    goal_amount = total + node_goal
                    achieved_amount = flt(si[0].total) + flt(closure[0].charges) + flt(si_amount) + flt(closure_amount)
                    self.append("target",{
                        "data_1": e.employee_name,
                        "goal": flt(goal_amount),
                        "role": e.tiips_role,
                        "achieved": flt(achieved_amount),
                        "pending": flt(goal_amount) - flt(achieved_amount),
                        "achieved_percentage" :(flt(achieved_amount)/flt(goal_amount))*100
                        })
                    self.append("tiips",{
                        "employee_name":e.employee_name,
                        "quarterly":get_bt[0],
                        "year":get_bt[1],
                        "bt":get_bt[2]
                    })
# @frappe.whitelist()
# def get_ft(employee_name, period,name):
#     ssa = frappe.get_value("Salary Structure Assignment", {
#                            'employee_name': employee_name}, ['base'])
#     ft_time = frappe.get_value(
#                 "Tiips", {'parent': name,"quarterly":"1","year":"2020"}, ['ft_times'])
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
#     return total

# @frappe.whitelist()
# def get_bt(employee_name):
# 	bt =frappe.get_value("Employee",{'employee_name':employee_name})

# si = 0
            #
            # both = frappe.db.sql("""select sum(total) as total from`tabSales Invoice` WHERE delivery_manager = '%s' AND account_manager = '%s' AND posting_date BETWEEN '%s' and '%s' """ % (
            #     e.prefered_email, e.prefered_email, self.from_period, self.to))
