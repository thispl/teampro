# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class AccountsChecklistTemplate(Document):
    def validate(self):
        # ensure at least one item per frequency that is referenced
        seen = set()
        for row in self.items:
            key = (row.item_title, row.frequency)
            if key in seen:
                frappe.throw(frappe._("Duplicate item '{0}' for frequency {1}").format(row.item_title, row.frequency))
            seen.add(key)

    def get_items_for_frequency(self, frequency, period_date):
        """Return template items applicable for the given frequency and date (month aware)."""
        month = frappe.utils.getdate(period_date).month
        month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                     7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        out = []
        for row in self.items:
            if row.frequency != frequency:
                continue
            months = (row.applicable_months or "All").strip()
            if months and months.lower() != "all":
                applicable = [m.strip() for m in months.split(",")]
                if month_map.get(month) not in applicable:
                    continue
            out.append(row)
        return out
