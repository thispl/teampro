# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class PerformanceRating(Document):
    def before_save(self):
        if not self.period_label and self.from_date:
            import datetime
            d = datetime.date.fromisoformat(str(self.from_date))
            if self.period == "Monthly":
                self.period_label = "{0}-{1:02d}".format(d.year, d.month)
            elif self.period == "Quarterly":
                self.period_label = "{0}-Q{1}".format(d.year, (d.month - 1) // 3 + 1)
            elif self.period == "Half Yearly":
                self.period_label = "{0}-H{1}".format(d.year, 1 if d.month <= 6 else 2)
            else:
                self.period_label = str(d.year)

    def on_trash(self):
        if self.department and self.period_label:
            frappe.enqueue("teampro.tpe.calculator._update_rank", queue="default",
                           department=self.department, period_label=self.period_label)
