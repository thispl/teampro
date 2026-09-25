# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document

from teampro.tpe.formula_engine import evaluate, FormulaError


class KPIMaster(Document):
    def validate(self):
        aliases = set()
        for row in self.variables:
            alias = (row.alias or row.kpi_variable).strip()
            if alias in aliases:
                frappe.throw(_("Duplicate variable alias: {0}").format(alias))
            aliases.add(alias)
            row.alias = alias
        if self.formula:
            try:
                evaluate(self.formula, {a: 1 for a in aliases})
            except FormulaError as e:
                frappe.throw(_("Formula error: {0}").format(e))
