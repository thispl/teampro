# -*- coding: utf-8 -*-
"""TPE Dashboard data services.

Exposes whitelisted methods consumed by the TPE dashboard pages and REST API.
"""
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import add_months, flt, getdate, today

from .calculator import get_period_label, get_period_range


@frappe.whitelist()
def employee_view(employee=None, period="Monthly", ref_date=None):
    """Employee self-view: overall PR, dept rank, trend, KRA/KPI scores, EP/NC."""
    employee = employee or frappe.db.get_value("Employee", {"user_id": frappe.session.user})
    if not employee:
        frappe.throw(_("No employee linked to this user"))
    rating = frappe.db.get_value(
        "Performance Rating",
        {"employee": employee, "period": period,
         "period_label": get_period_label(period, ref_date or today())},
        "name",
    )
    if not rating:
        return {"message": {"rating": None, "trend": [], "rank": None}}
    doc = frappe.get_doc("Performance Rating", rating)
    trend = _trend(employee, period, 12)
    return {
        "message": {
            "rating": doc.as_dict(),
            "trend": trend,
            "rank": doc.department_rank,
        }
    }


@frappe.whitelist()
def manager_view(manager=None, period="Monthly", ref_date=None):
    """Manager dashboard: all reportees, current PR, dept avg, top/bottom, pending."""
    manager = manager or frappe.db.get_value("Employee", {"user_id": frappe.session.user})
    if not manager:
        frappe.throw(_("No employee linked to this user"))
    period_label = get_period_label(period, ref_date or today())
    reportees = frappe.db.get_all("Employee", {"reports_to": manager}, ["name", "employee_name"])
    rows = []
    for r in reportees:
        rating = frappe.db.get_value(
            "Performance Rating",
            {"employee": r.name, "period_label": period_label},
            ["name", "overall_pr", "department_rank", "strength", "improvement_area"],
            as_dict=True,
        )
        rows.append({
            "employee": r.name,
            "employee_name": r.employee_name,
            "current_pr": flt(rating.overall_pr, 2) if rating else None,
            "rank": rating.department_rank if rating else None,
            "strength": rating.strength if rating else None,
            "improvement_area": rating.improvement_area if rating else None,
        })
    prs = [x["current_pr"] for x in rows if x["current_pr"] is not None]
    dept_avg = flt(sum(prs) / len(prs), 2) if prs else 0.0
    sorted_rows = sorted([x for x in rows if x["current_pr"] is not None],
                         key=lambda x: x["current_pr"], reverse=True)
    return {
        "message": {
            "reportees": rows,
            "department_average": dept_avg,
            "top_performers": sorted_rows[:5],
            "low_performers": list(reversed(sorted_rows[-5:])) if sorted_rows else [],
            "pending_reviews": _pending_reviews(manager, period_label),
        }
    }


@frappe.whitelist()
def director_view(period="Monthly", ref_date=None, company=None, department=None,
                  branch=None, designation=None):
    """Director dashboard: aggregated performance across divisions/depts/branches."""
    period_label = get_period_label(period, ref_date or today())
    filters = {"period_label": period_label}
    if department:
        filters["department"] = department
    if designation:
        filters["designation"] = designation
    ratings = frappe.db.get_all(
        "Performance Rating", filters,
        ["employee", "employee_name", "department", "designation", "overall_pr", "department_rank"],
    )
    # company / branch filter via Employee
    if company or branch:
        keep = []
        for r in ratings:
            emp = frappe.db.get_value("Employee", r.employee, ["company", "branch"], as_dict=True)
            if company and emp.company != company:
                continue
            if branch and emp.branch != branch:
                continue
            keep.append(r)
        ratings = keep

    distribution = _distribution(ratings)
    top10 = sorted(ratings, key=lambda x: x.overall_pr, reverse=True)[:10]
    bottom10 = sorted(ratings, key=lambda x: x.overall_pr)[:10]
    return {
        "message": {
            "period_label": period_label,
            "total_rated": len(ratings),
            "distribution": distribution,
            "top_10": top10,
            "bottom_10": bottom10,
            "by_department": _group_by(ratings, "department"),
            "by_designation": _group_by(ratings, "designation"),
        }
    }


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _trend(employee, period, months):
    out = []
    ref = getdate(today())
    for i in range(months):
        d = add_months(ref, -i)
        label = get_period_label(period, d)
        pr = frappe.db.get_value(
            "Performance Rating",
            {"employee": employee, "period_label": label}, "overall_pr",
        )
        out.append({"period_label": label, "pr": flt(pr, 2) if pr else None})
    out.reverse()
    return out


def _pending_reviews(manager, period_label):
    reportees = frappe.db.get_all("Employee", {"reports_to": manager}, ["name"])
    pending = []
    for r in reportees:
        if not frappe.db.exists("Performance Rating",
                                {"employee": r.name, "period_label": period_label}):
            pending.append(r.name)
    return pending


def _distribution(ratings):
    bands = [
        ("Outstanding", 90, 100),
        ("Excellent", 80, 89.99),
        ("Good", 70, 79.99),
        ("Average", 50, 69.99),
        ("Below Average", 0, 49.99),
    ]
    out = []
    for label, lo, hi in bands:
        n = len([r for r in ratings if lo <= flt(r.overall_pr) <= hi])
        out.append({"band": label, "count": n})
    return out


def _group_by(ratings, key):
    groups = {}
    for r in ratings:
        k = r.get(key) or "Unassigned"
        groups.setdefault(k, []).append(flt(r.overall_pr))
    return [{"key": k, "count": len(v), "average": flt(sum(v) / len(v), 2)}
            for k, v in groups.items()]
