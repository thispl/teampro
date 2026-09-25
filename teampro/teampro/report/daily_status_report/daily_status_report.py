# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    cols = [
        {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 110},
        {"label": _("Frequency"), "fieldname": "frequency", "fieldtype": "Data", "width": 90},
        {"label": _("Period"), "fieldname": "period_label", "fieldtype": "Data", "width": 120},
        {"label": _("Checklists"), "fieldname": "checklist_count", "fieldtype": "Int", "width": 90},
        {"label": _("Total Items"), "fieldname": "total_items", "fieldtype": "Int", "width": 100},
        {"label": _("Completed"), "fieldname": "completed", "fieldtype": "Int", "width": 100},
        {"label": _("Pending"), "fieldname": "pending", "fieldtype": "Int", "width": 90},
        {"label": _("Overdue"), "fieldname": "overdue", "fieldtype": "Int", "width": 90},
        {"label": _("N/A"), "fieldname": "not_applicable", "fieldtype": "Int", "width": 70},
        {"label": _("Completion %"), "fieldname": "completion_pct", "fieldtype": "Percent", "width": 110},
    ]
    for cat in ["Internal Accounts", "Statutory", "Management MIS", "Audit Year-end"]:
        cols.append({"label": _(cat), "fieldname": cat.lower().replace(" ", "_").replace("-", "_"), "fieldtype": "Int", "width": 110})
        cols.append({"label": _("%s Done" % cat), "fieldname": cat.lower().replace(" ", "_").replace("-", "_") + "_done", "fieldtype": "Int", "width": 90})
    return cols


def get_data(filters):
    filters = filters or {}
    cond, values = build_conditions(filters)

    rows = frappe.db.sql(
        """
        select
            c.period_start as date, c.frequency, c.period_label,
            c.name as checklist, c.total_items, c.completed_items,
            c.pending_items, c.overdue_items, c.not_applicable_items,
            c.completion_pct, ci.category, ci.status
        from `tabAccounts Checklist` c
        left join `tabAccounts Checklist Item` ci on ci.parent = c.name
        where c.docstatus < 2 {cond}
        """.format(cond=cond),
        values,
        as_dict=True,
    )

    # group by (date, frequency, period_label, checklist)
    groups = {}
    for r in rows:
        key = (r.date, r.frequency, r.period_label, r.checklist)
        g = groups.setdefault(key, {
            "date": r.date, "frequency": r.frequency, "period_label": r.period_label,
            "checklist": r.checklist, "checklist_count": 1,
            "total_items": r.total_items, "completed": r.completed_items,
            "pending": r.pending_items, "overdue": r.overdue_items,
            "not_applicable": r.not_applicable_items, "completion_pct": r.completion_pct,
            "internal_accounts": 0, "internal_accounts_done": 0,
            "statutory": 0, "statutory_done": 0,
            "management_mis": 0, "management_mis_done": 0,
            "audit_year_end": 0, "audit_year_end_done": 0,
        })
        if not r.category:
            continue
        cat_key = r.category.lower().replace(" ", "_").replace("-", "_")
        if cat_key in g:
            g[cat_key] = g.get(cat_key, 0) + 1
            if r.status == "Completed":
                g[cat_key + "_done"] = g.get(cat_key + "_done", 0) + 1

    out = [v for v in groups.values()]
    out.sort(key=lambda x: (x["date"], x["frequency"]), reverse=True)
    return out


def build_conditions(filters):
    cond = ""
    values = {}
    if filters.get("from_date"):
        cond += " and c.period_start >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        cond += " and c.period_end <= %(to_date)s"
        values["to_date"] = filters["to_date"]
    if filters.get("frequency"):
        cond += " and c.frequency = %(frequency)s"
        values["frequency"] = filters["frequency"]
    return cond, values


def get_chart(data):
    if not data:
        return None
    labels = [d["period_label"] for d in data[:15]][::-1]
    completed = [d["completed"] for d in data[:15]][::-1]
    pending = [d["pending"] for d in data[:15]][::-1]
    overdue = [d["overdue"] for d in data[:15]][::-1]
    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": _("Completed"), "values": completed, "chartType": "bar"},
                {"name": _("Pending"), "values": pending, "chartType": "bar"},
                {"name": _("Overdue"), "values": overdue, "chartType": "bar"},
            ],
        },
        "type": "bar",
        "colors": ["#7cd992", "#f7c96b", "#ff6b6b"],
    }
