# -*- coding: utf-8 -*-
"""TPE Task Benchmark Engine.

Every completed TPE Task updates a benchmark database keyed by
(module, feature, complexity). Future estimations query the benchmark to
recommend a suggested number of hours using the historical average.
"""
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt, today


def update_benchmark(task):
    """Called on completion of a TPE Task. Upserts a Task Benchmark row."""
    if not task.module or not task.complexity:
        return
    existing = frappe.db.get_value(
        "Task Benchmark",
        {"module": task.module, "feature": task.feature or "", "complexity": task.complexity},
        "name",
    )
    completed_rt = flt(task.required_time)
    completed_at = flt(task.actual_time)
    if existing:
        bench = frappe.get_doc("Task Benchmark", existing)
        bench.completed_count = (bench.completed_count or 0) + 1
        bench.total_rt = flt(bench.total_rt or 0) + completed_rt
        bench.total_at = flt(bench.total_at or 0) + completed_at
        bench.avg_rt = flt(bench.total_rt / bench.completed_count, 2)
        bench.avg_at = flt(bench.total_at / bench.completed_count, 2)
        bench.last_updated = today()
        bench.flags.ignore_validate = True
        bench.save(ignore_permissions=True)
    else:
        frappe.get_doc({
            "doctype": "Task Benchmark",
            "module": task.module,
            "feature": task.feature or "",
            "complexity": task.complexity,
            "completed_count": 1,
            "total_rt": completed_rt,
            "total_at": completed_at,
            "avg_rt": flt(completed_rt, 2),
            "avg_at": flt(completed_at, 2),
            "last_updated": today(),
        }).insert(ignore_permissions=True)


@frappe.whitelist()
def recommend_estimated_time(module, feature=None, complexity=None):
    """Recommend an estimated time (hours) using historical benchmarks.

    Falls back to broader matches (feature -> module -> complexity) when no
    exact match exists. Returns 0 if no history is available.
    """
    def _avg(filters):
        row = frappe.db.get_value(
            "Task Benchmark", filters,
            ["avg_rt", "completed_count"], as_dict=True,
        )
        if row and row.completed_count:
            return flt(row.avg_rt, 2)
        return None

    for f in (
        {"module": module, "feature": feature, "complexity": complexity},
        {"module": module, "complexity": complexity},
        {"module": module, "feature": feature},
        {"module": module},
    ):
        clean = {k: v for k, v in f.items() if v}
        val = _avg(clean)
        if val:
            return {"recommended_time": val, "based_on": clean}
    return {"recommended_time": 0.0, "based_on": {}}
