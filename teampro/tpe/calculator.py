# -*- coding: utf-8 -*-
"""TPE Performance Calculator.

Computes, for a given employee and period:
  - each KPI score (via formula_engine)
  - each KRA score (weighted average of its KPIs)
  - overall Performance Rating (PR) (weighted average of KRAs)
  - department rank
  - EP / NC / continuous-improvement components
  - cascading manager / TL / director scores

Results are persisted in the *Performance Rating* doctype. A scheduled job
runs the monthly calculation automatically; on-demand calculation is exposed
via whitelisted methods for the UI and REST API.
"""
from __future__ import unicode_literals

import calendar
import datetime
import json

import frappe
from frappe import _
from frappe.utils import add_days, add_months, cint, cstr, flt, getdate, today

from . import formula_engine


# ---------------------------------------------------------------------------
# Period helpers
# ---------------------------------------------------------------------------

PERIODS = ["Monthly", "Quarterly", "Half Yearly", "Yearly"]


def get_period_range(period, ref_date=None):
    """Return (from_date, to_date) for a period containing ref_date."""
    ref = getdate(ref_date or today())
    if period == "Monthly":
        from_date = ref.replace(day=1)
        to_date = ref.replace(day=calendar.monthrange(ref.year, ref.month)[1])
    elif period == "Quarterly":
        q = (ref.month - 1) // 3
        from_date = ref.replace(month=q * 3 + 1, day=1)
        to_date = getdate(add_days(
            ref.replace(month=q * 3 + 3, day=calendar.monthrange(ref.year, q * 3 + 3)[1]), 0))
    elif period == "Half Yearly":
        if ref.month <= 6:
            from_date = ref.replace(month=1, day=1)
            to_date = ref.replace(month=6, day=30)
        else:
            from_date = ref.replace(month=7, day=1)
            to_date = ref.replace(month=12, day=31)
    else:  # Yearly
        from_date = ref.replace(month=1, day=1)
        to_date = ref.replace(month=12, day=31)
    return from_date, to_date


def get_period_label(period, ref_date):
    ref = getdate(ref_date)
    if period == "Monthly":
        return "{0}-{1:02d}".format(ref.year, ref.month)
    if period == "Quarterly":
        q = (ref.month - 1) // 3 + 1
        return "{0}-Q{1}".format(ref.year, q)
    if period == "Half Yearly":
        h = 1 if ref.month <= 6 else 2
        return "{0}-H{1}".format(ref.year, h)
    return cstr(ref.year)


# ---------------------------------------------------------------------------
# Core calculation
# ---------------------------------------------------------------------------

def get_active_kras(department, designation):
    """Return active KRA Master docs applicable to dept/designation."""
    filters = {"department": department, "active": 1}
    kras = frappe.db.get_all(
        "KRA Master", filters=filters, fields=["name", "kra_name", "weightage"],
        order_by="weightage desc",
    )
    # Filter by designation if KRA has a designation restriction
    result = []
    for kra in kras:
        designations = frappe.db.get_all(
            "KRA Designation", {"parent": kra.name}, pluck="designation"
        )
        if not designations or designation in designations:
            result.append(kra)
    return result


def get_kpis_for_kra(kra_name):
    """Return KPI Master docs mapped to a KRA, with their weightage in the KRA."""
    rows = frappe.db.get_all(
        "KRA KPI Mapping", {"parent": kra_name},
        ["kpi", "weightage"],
    )
    kpis = []
    for r in rows:
        kpi_doc = frappe.db.get_value(
            "KPI Master", r.kpi,
            ["name", "kpi_name", "formula", "max_score", "weightage", "frequency", "active"],
            as_dict=True,
        )
        if kpi_doc and kpi_doc.active:
            kpi_doc.kra_weightage = flt(r.weightage or kpi_doc.weightage or 0)
            kpis.append(kpi_doc)
    return kpis


def calculate_employee(employee, period, ref_date=None, persist=True):
    """Calculate the full Performance Rating for an employee/period.

    Returns the Performance Rating doc (dict).
    """
    emp = frappe.db.get_value(
        "Employee", employee,
        ["name", "employee_name", "department", "designation", "reports_to", "user_id"],
        as_dict=True,
    )
    if not emp:
        frappe.throw(_("Employee {0} not found").format(employee))

    from_date, to_date = get_period_range(period, ref_date)
    period_label = get_period_label(period, ref_date or today())

    kras = get_active_kras(emp.department, emp.designation)

    kra_rows = []
    kpi_rows = []
    total_kra_weight = 0.0
    weighted_kra_sum = 0.0

    for kra in kras:
        kpis = get_kpis_for_kra(kra.name)
        if not kpis:
            continue
        kpi_weight_sum = sum(k.kra_weightage for k in kpis) or 1.0
        weighted_kpi_sum = 0.0
        for kpi in kpis:
            kpi_doc = frappe.get_doc("KPI Master", kpi.name)
            score = formula_engine.compute_kpi(kpi_doc, employee, from_date, to_date)
            max_score = flt(kpi.max_score or 100)
            norm = (score / max_score * 100.0) if max_score else 0.0
            kpi_rows.append({
                "kra": kra.name,
                "kpi": kpi.name,
                "kpi_name": kpi.kpi_name,
                "score": flt(score, 2),
                "max_score": max_score,
                "normalized_score": flt(norm, 2),
                "weightage": flt(kpi.kra_weightage, 2),
            })
            weighted_kpi_sum += norm * flt(kpi.kra_weightage)
        kra_score = weighted_kpi_sum / kpi_weight_sum
        kra_rows.append({
            "kra": kra.name,
            "kra_name": kra.kra_name,
            "score": flt(kra_score, 2),
            "weightage": flt(kra.weightage, 2),
        })
        weighted_kra_sum += kra_score * flt(kra.weightage)
        total_kra_weight += flt(kra.weightage)

    overall_pr = (weighted_kra_sum / total_kra_weight) if total_kra_weight else 0.0

    # Continuous improvement components
    ep, nc, leadership, improvement = _continuous_improvement(employee, from_date, to_date)
    overall_pr = _apply_continuous_improvement(overall_pr, ep, nc, leadership, improvement)

    # Strength / improvement area
    strength, improvement_area = _derive_strength_weakness(kra_rows)

    doc = {
        "doctype": "Performance Rating",
        "employee": employee,
        "employee_name": emp.employee_name,
        "department": emp.department,
        "designation": emp.designation,
        "period": period,
        "period_label": period_label,
        "from_date": from_date,
        "to_date": to_date,
        "overall_pr": flt(overall_pr, 2),
        "energy_points": flt(ep, 2),
        "non_conformities": cint(nc),
        "leadership_score": flt(leadership, 2),
        "improvement_score": flt(improvement, 2),
        "strength": strength,
        "improvement_area": improvement_area,
        "kra_scores": kra_rows,
        "kpi_scores": kpi_rows,
        "calculation_date": today(),
    }

    if persist:
        doc = _save_rating(doc)
    return doc


def _save_rating(doc):
    """Insert or update the Performance Rating for the same employee/period."""
    existing = frappe.db.get_value(
        "Performance Rating",
        {"employee": doc["employee"], "period_label": doc["period_label"]},
        "name",
    )
    payload = dict(doc)
    payload.pop("doctype", None)
    child_payload = {
        "kra_scores": payload.pop("kra_scores", []),
        "kpi_scores": payload.pop("kpi_scores", []),
    }
    if existing:
        rating = frappe.get_doc("Performance Rating", existing)
        rating.update(payload)
        rating.set("kra_scores", [])
        rating.set("kpi_scores", [])
        for r in child_payload["kra_scores"]:
            rating.append("kra_scores", r)
        for r in child_payload["kpi_scores"]:
            rating.append("kpi_scores", r)
        rating.flags.ignore_validate = True
        rating.save(ignore_permissions=True)
    else:
        rating = frappe.get_doc({"doctype": "Performance Rating", **payload})
        for r in child_payload["kra_scores"]:
            rating.append("kra_scores", r)
        for r in child_payload["kpi_scores"]:
            rating.append("kpi_scores", r)
        rating.flags.ignore_validate = True
        rating.insert(ignore_permissions=True)
    _update_rank(rating.department, rating.period_label)
    _cascade_scores(rating.employee, rating.period_label)
    return rating.as_dict()


# ---------------------------------------------------------------------------
# Continuous improvement
# ---------------------------------------------------------------------------

def _continuous_improvement(employee, from_date, to_date):
    filters = {"employee": employee, "date": ["between", [from_date, to_date]]}
    ep = frappe.db.get_all(
        "Continuous Improvement Entry",
        {**filters, "type": "Energy Point"}, ["points"],
    )
    nc = frappe.db.count("Continuous Improvement Entry", {**filters, "type": "Non Conformity"})
    awards = frappe.db.get_all(
        "Continuous Improvement Entry",
        {**filters, "type": "Award"}, ["points"],
    )
    training = frappe.db.get_all(
        "Continuous Improvement Entry",
        {**filters, "type": "Training"}, ["points"],
    )
    suggestions = frappe.db.count(
        "Continuous Improvement Entry",
        {**filters, "type": "Approved Suggestion"},
    )
    knowledge = frappe.db.count(
        "Continuous Improvement Entry",
        {**filters, "type": "Knowledge Sharing"},
    )
    attendance = frappe.db.count(
        "Continuous Improvement Entry",
        {**filters, "type": "Attendance Discipline"},
    )

    ep_total = flt(sum(r.points for r in ep))
    leadership = flt(sum(r.points for r in awards)) + (knowledge * 2)
    improvement = flt(sum(r.points for r in training)) + (suggestions * 3) + (attendance * 1)
    return ep_total, nc, leadership, improvement


def _apply_continuous_improvement(pr, ep, nc, leadership, improvement):
    settings = frappe.db.get_value(
        "TPE Settings", "TPE Settings",
        ["ep_weight", "nc_penalty", "leadership_weight", "improvement_weight"],
        as_dict=True,
    ) or {}
    ep_w = flt(settings.get("ep_weight") if isinstance(settings, dict) else settings.ep_weight, 2) or 0.5
    nc_p = flt(settings.get("nc_penalty") if isinstance(settings, dict) else settings.nc_penalty, 2) or 2.0
    lead_w = flt(settings.get("leadership_weight") if isinstance(settings, dict) else settings.leadership_weight, 2) or 0.2
    imp_w = flt(settings.get("improvement_weight") if isinstance(settings, dict) else settings.improvement_weight, 2) or 0.2

    pr = pr + (ep * ep_w) + (leadership * lead_w) + (improvement * imp_w)
    pr = pr - (nc * nc_p)
    if pr < 0:
        pr = 0.0
    if pr > 100:
        pr = 100.0
    return pr


def _derive_strength_weakness(kra_rows):
    if not kra_rows:
        return "", ""
    sorted_kras = sorted(kra_rows, key=lambda r: r["score"], reverse=True)
    strength = sorted_kras[0]["kra_name"]
    improvement_area = sorted_kras[-1]["kra_name"]
    return strength, improvement_area


# ---------------------------------------------------------------------------
# Ranking & cascading scores
# ---------------------------------------------------------------------------

def _update_rank(department, period_label):
    """Recompute department_rank for all ratings in a dept/period."""
    ratings = frappe.db.get_all(
        "Performance Rating",
        {"department": department, "period_label": period_label},
        ["name", "overall_pr"],
        order_by="overall_pr desc",
    )
    for i, r in enumerate(ratings, 1):
        frappe.db.set_value("Performance Rating", r.name, "department_rank", i)


def _cascade_scores(employee, period_label):
    """Cascade scores up the hierarchy: TL <- team, Manager <- reportees, Director <- managers."""
    # Team Leader score = average PR of team members where employee is TL
    team = frappe.db.get_all(
        "Employee", {"reports_to": employee}, ["name"],
    )
    if team:
        prs = frappe.db.get_all(
            "Performance Rating",
            {"employee": ("in", [t.name for t in team]), "period_label": period_label},
            ["overall_pr"],
        )
        if prs:
            avg = flt(sum(r.overall_pr for r in prs) / len(prs), 2)
            _upsert_cascade(employee, period_label, "Team Leader", avg)

    # Manager score = average PR of direct reportees
    reportees = frappe.db.get_all(
        "Employee", {"reports_to": employee}, ["name"],
    )
    if reportees:
        prs = frappe.db.get_all(
            "Performance Rating",
            {"employee": ("in", [r.name for r in reportees]), "period_label": period_label},
            ["overall_pr"],
        )
        if prs:
            avg = flt(sum(r.overall_pr for r in prs) / len(prs), 2)
            _upsert_cascade(employee, period_label, "Manager", avg)


def _upsert_cascade(employee, period_label, role, score):
    existing = frappe.db.get_value(
        "Team Performance",
        {"employee": employee, "period_label": period_label, "role": role},
        "name",
    )
    if existing:
        frappe.db.set_value("Team Performance", existing, "score", score)
    else:
        frappe.get_doc({
            "doctype": "Team Performance",
            "employee": employee,
            "period_label": period_label,
            "role": role,
            "score": score,
        }).insert(ignore_permissions=True)


# ---------------------------------------------------------------------------
# Bulk / scheduled calculation
# ---------------------------------------------------------------------------

def calculate_department(department, period, ref_date=None):
    employees = frappe.db.get_all(
        "Employee", {"department": department, "status": "Active"}, ["name"],
    )
    for emp in employees:
        try:
            calculate_employee(emp.name, period, ref_date)
        except Exception as e:
            frappe.log_error(title="TPE calc error {0}".format(emp.name), message=str(e))
    return len(employees)


def calculate_all(period, ref_date=None):
    departments = frappe.db.get_all("Department", ["name"])
    total = 0
    for d in departments:
        total += calculate_department(d.name, period, ref_date)
    return total


@frappe.whitelist()
def calculate(employee=None, department=None, period="Monthly", ref_date=None):
    """On-demand calculation entrypoint (UI/API)."""
    if employee:
        return calculate_employee(employee, period, ref_date)
    if department:
        n = calculate_department(department, period, ref_date)
        return {"calculated": n}
    n = calculate_all(period, ref_date)
    return {"calculated": n}


def scheduled_monthly_calculation():
    """Hooked to a cron job (see hooks.py). Runs on the 1st of each month for the previous month."""
    ref = add_months(today(), -1)
    calculate_all("Monthly", ref)
