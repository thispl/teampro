# -*- coding: utf-8 -*-
"""TPE public API — whitelisted methods used by the UI, REST endpoints and
DocType server actions.
"""
from __future__ import unicode_literals

import frappe
from frappe import _

from tpe import calculator, benchmark
from teampro.tpe.formula_engine import evaluate, FormulaError


@frappe.whitelist()
def calculate(employee=None, department=None, period="Monthly", ref_date=None):
    """Trigger a performance calculation on demand."""
    res = calculator.calculate(employee=employee, department=department,
                               period=period, ref_date=ref_date)
    from teampro.tpe.audit import log
    log("Performance Rating", res.get("name") if isinstance(res, dict) else res,
        "Calculate", {"period": period, "ref_date": ref_date})
    return res


@frappe.whitelist()
def recalculate_rating(name):
    """Recalculate an existing Performance Rating."""
    rating = frappe.get_doc("Performance Rating", name)
    res = calculator.calculate_employee(
        rating.employee, rating.period, ref_date=rating.from_date)
    return res


@frappe.whitelist()
def test_kpi_formula(name):
    """Validate a KPI Master formula by evaluating it with dummy variables."""
    doc = frappe.get_doc("KPI Master", name)
    aliases = [r.alias or r.kpi_variable for r in doc.variables]
    try:
        val = evaluate(doc.formula, {a: 1 for a in aliases})
        return {"ok": True, "value": val, "variables": aliases}
    except FormulaError as e:
        return {"ok": False, "error": str(e)}


@frappe.whitelist()
def recommend_task_time(module, feature=None, complexity=None):
    return benchmark.recommend_estimated_time(module, feature, complexity)


# Dashboard endpoints (re-exported under tpe.api for stable dotted paths)
@frappe.whitelist()
def employee_view(employee=None, period="Monthly", ref_date=None):
    from teampro.tpe.dashboard import employee_view as _ev
    return _ev(employee, period, ref_date)


@frappe.whitelist()
def manager_view(manager=None, period="Monthly", ref_date=None):
    from teampro.tpe.dashboard import manager_view as _mv
    return _mv(manager, period, ref_date)


@frappe.whitelist()
def director_view(period="Monthly", ref_date=None, **kwargs):
    from teampro.tpe.dashboard import director_view as _dv
    return _dv(period=period, ref_date=ref_date, **kwargs)


@frappe.whitelist()
def get_rating(employee, period="Monthly", ref_date=None):
    """Fetch the latest Performance Rating for an employee/period."""
    from teampro.tpe.calculator import get_period_label
    from frappe.utils import today
    label = get_period_label(period, ref_date or today())
    name = frappe.db.get_value("Performance Rating",
                               {"employee": employee, "period_label": label}, "name")
    if not name:
        return {"exists": False}
    return {"exists": True, "rating": frappe.get_doc("Performance Rating", name).as_dict()}
