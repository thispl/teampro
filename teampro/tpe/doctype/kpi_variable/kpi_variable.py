# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document


class KPIVariable(Document):
    def validate(self):
        if self.aggregation_type in ("Sum", "Average", "Min", "Max") and not self.value_field:
            frappe.throw(_("Value Field is required for {0} aggregation").format(self.aggregation_type))
        if self.aggregation_type == "Date Difference" and "," not in (self.value_field or ""):
            frappe.throw(_("For Date Difference, Value Field must be 'start_field,end_field'"))
        if self.employee_link_field and not self.employee_field_type:
            self.employee_field_type = "Employee"
