# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe


def get_context(context):
    context.view = "employee"
    if frappe.has_role("Director"):
        context.view = "director"
    elif frappe.has_role("Manager") or frappe.has_role("HR Manager") or frappe.has_role("Projects Manager"):
        context.view = "manager"
    return context
