# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class CustomerRating(Document):
    def validate(self):
        for r in self.parameters:
            if not (1 <= r.rating <= 5):
                frappe.throw(_("Rating for {0} must be between 1 and 5").format(r.parameter))
        if self.parameters:
            self.overall_rating = round(sum(r.rating for r in self.parameters) / len(self.parameters), 2)
