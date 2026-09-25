# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class KRAMaster(Document):
    def validate(self):
        total = sum(r.weightage or 0 for r in self.kpi_mapping)
        if total <= 0:
            frappe.throw(_("KPI weightages must sum to more than 0"))
        for row in self.kpi_mapping:
            if row.kpi:
                kpi_dept = frappe.db.get_value("KPI Master", row.kpi, "department")
                if kpi_dept and kpi_dept != self.department:
                    frappe.throw(_("KPI {0} belongs to a different department").format(row.kpi))
