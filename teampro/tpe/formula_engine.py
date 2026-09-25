# -*- coding: utf-8 -*-
"""TPE Formula / Rule Engine.

Evaluates KPI formulas expressed as plain arithmetic expressions over named
*variables*. Each variable resolves to a numeric value for a given employee and
date window via the KPI Variable master (see ``resolve_variables``).

Supported operations (per SRS): addition, subtraction, average, weighted
average, percentage, ratio, date difference, count, sum, conditional logic and
custom formula. These are realised through a small, safe expression grammar
(``ast`` based) plus a few helper functions exposed to formulas:

    avg(a, b, c)            -> arithmetic mean
    wavg(values; weights)   -> weighted average  (semicolon-separated lists)
    pct(numerator, denominator) -> (num/den)*100  (null-safe)
    ratio(n, d)             -> n / d              (null-safe)
    days(d1, d2)            -> date difference in days (strings YYYY-MM-DD)
    count(...)              -> count of non-null args
    sum(...)                -> sum of args
    if(cond, then, else)    -> conditional
    min(...), max(...)      -> usual
    round(x, n)             -> usual

A formula such as ``(completed_rt / completed_at) * 100`` is evaluated with the
variables ``completed_rt`` and ``completed_at`` bound to their resolved values.
"""
from __future__ import unicode_literals

import ast
import datetime
import json
import math
import operator

import frappe
from frappe import _


# ---------------------------------------------------------------------------
# Safe expression evaluation
# ---------------------------------------------------------------------------

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: lambda a, b: (a / b) if b else 0.0,
    ast.FloorDiv: lambda a, b: (a // b) if b else 0.0,
    ast.Mod: lambda a, b: (a % b) if b else 0.0,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}

_BOOL_OPS = {ast.And: all, ast.Or: any}


def _to_number(v):
    if v is None or v == "":
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _helper_avg(*args):
    nums = [_to_number(a) for a in args if a is not None and a != ""]
    return sum(nums) / len(nums) if nums else 0.0


def _helper_wavg(values, weights):
    values = [_to_number(v) for v in (values or [])]
    weights = [_to_number(w) for w in (weights or [])]
    if not values or not weights or len(values) != len(weights):
        return 0.0
    denom = sum(weights)
    if not denom:
        return 0.0
    return sum(v * w for v, w in zip(values, weights)) / denom


def _helper_pct(num, den):
    num = _to_number(num)
    den = _to_number(den)
    return (num / den * 100.0) if den else 0.0


def _helper_ratio(num, den):
    num = _to_number(num)
    den = _to_number(den)
    return (num / den) if den else 0.0


def _helper_days(d1, d2):
    try:
        a = datetime.datetime.strptime(str(d1)[:10], "%Y-%m-%d").date()
        b = datetime.datetime.strptime(str(d2)[:10], "%Y-%m-%d").date()
        return abs((b - a).days)
    except Exception:
        return 0.0


def _helper_if(cond, then, else_=None):
    return then if cond else else_


def _helper_count(*args):
    return len([a for a in args if a is not None and a != ""])


def _helper_sum(*args):
    return sum(_to_number(a) for a in args)


def _helper_min(*args):
    nums = [_to_number(a) for a in args]
    return min(nums) if nums else 0.0


def _helper_max(*args):
    nums = [_to_number(a) for a in args]
    return max(nums) if nums else 0.0


def _helper_round(x, n=0):
    return round(_to_number(x), int(_to_number(n)))


HELPERS = {
    "avg": _helper_avg,
    "mean": _helper_avg,
    "wavg": _helper_wavg,
    "pct": _helper_pct,
    "ratio": _helper_ratio,
    "days": _helper_days,
    "if": _helper_if,
    "count": _helper_count,
    "sum": _helper_sum,
    "min": _helper_min,
    "max": _helper_max,
    "round": _helper_round,
    "abs": abs,
    "ceil": math.ceil,
    "floor": math.floor,
}

_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp,
    ast.Constant, ast.Name, ast.Load, ast.Call,
    ast.Tuple, ast.List, ast.keyword, ast.IfExp,
    ast.operator, ast.cmpop, ast.boolop, ast.unaryop,
)
# ast.Num was removed in Python 3.12+; keep compat for older runtimes
if hasattr(ast, "Num"):
    _ALLOWED_NODES = _ALLOWED_NODES + (ast.Num,)


class FormulaError(Exception):
    pass


def evaluate(formula, variables):
    """Evaluate ``formula`` (string) against ``variables`` (dict name->value).

    Returns a float. Raises FormulaError on invalid / unsafe input.
    """
    if not formula or not formula.strip():
        return 0.0
    # Normalise: allow ``if(...)`` even though it is a Python keyword by
    # rewriting the helper name to ``_if`` for the AST pass.
    safe = formula.strip()
    try:
        tree = ast.parse(safe, mode="eval")
    except SyntaxError as e:
        raise FormulaError(_("Invalid formula syntax: {0}").format(e))

    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise FormulaError(
                _("Disallowed expression element: {0}").format(type(node).__name__)
            )

    env = dict(HELPERS)
    env["if"] = _helper_if
    env.update({k: _to_number(v) for k, v in (variables or {}).items()})

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if hasattr(ast, "Num") and isinstance(node, ast.Num):  # py<3.12 compat
            return node.n
        if isinstance(node, ast.Name):
            if node.id in env:
                return env[node.id]
            raise FormulaError(_("Unknown variable in formula: {0}").format(node.id))
        if isinstance(node, ast.BinOp):
            op = _BIN_OPS.get(type(node.op))
            if not op:
                raise FormulaError(_("Unsupported operator: {0}").format(type(node.op).__name__))
            return op(_to_number(_eval(node.left)), _to_number(_eval(node.right)))
        if isinstance(node, ast.UnaryOp):
            op = _UNARY_OPS.get(type(node.op))
            if not op:
                raise FormulaError(_("Unsupported unary operator"))
            return op(_to_number(_eval(node.operand)))
        if isinstance(node, ast.Compare):
            left = _eval(node.left)
            result = True
            for op_node, comp in zip(node.ops, node.comparators):
                cmp = _CMP_OPS.get(type(op_node))
                if not cmp:
                    raise FormulaError(_("Unsupported comparison"))
                result = result and cmp(left, _eval(comp))
                left = _eval(comp)
            return result
        if isinstance(node, ast.BoolOp):
            op = _BOOL_OPS.get(type(node.op))
            vals = [_eval(v) for v in node.values]
            return op(vals)
        if isinstance(node, ast.IfExp):
            return _eval(node.body) if _eval(node.test) else _eval(node.orelse)
        if isinstance(node, (ast.Tuple, ast.List)):
            return [_eval(e) for e in node.elts]
        if isinstance(node, ast.Call):
            fn = env.get(node.func.id) if isinstance(node.func, ast.Name) else None
            if not fn:
                raise FormulaError(_("Unknown function: {0}").format(getattr(node.func, "id", "?")))
            args = [_eval(a) for a in node.args]
            kwargs = {kw.arg: _eval(kw.value) for kw in node.keywords if kw.arg}
            return fn(*args, **kwargs)
        raise FormulaError(_("Cannot evaluate node: {0}").format(type(node).__name__))

    try:
        val = _eval(tree)
    except FormulaError:
        raise
    except Exception as e:
        raise FormulaError(_("Formula evaluation error: {0}").format(e))
    return _to_number(val)


# ---------------------------------------------------------------------------
# Variable resolution
# ---------------------------------------------------------------------------

def resolve_variables(kpi, employee, from_date, to_date):
    """Resolve all variables declared on a KPI Master for an employee/period.

    Returns dict {alias: float_value}.
    """
    values = {}
    for row in kpi.get("variables") or []:
        var_name = row.get("variable") or row.get("kpi_variable")
        alias = row.get("alias") or var_name
        if not var_name:
            continue
        values[alias] = resolve_variable(var_name, employee, from_date, to_date)
    return values


def resolve_variable(variable_name, employee, from_date, to_date):
    """Resolve a single KPI Variable to a number for the employee/period."""
    if not frappe.db.exists("KPI Variable", variable_name):
        return 0.0

    var = frappe.db.get_value(
        "KPI Variable", variable_name,
        ["target_doctype", "date_field", "employee_link_field",
         "aggregation_type", "value_field", "filter_json", "employee_field_type"],
        as_dict=True,
    )
    if not var or not var.target_doctype:
        return 0.0

    filters = {}
    # date window
    if var.date_field:
        filters[var.date_field] = ["between", [from_date, to_date]]

    # employee filter
    emp_value = _employee_filter_value(employee, var.employee_field_type)
    if var.employee_link_field and emp_value:
        filters[var.employee_link_field] = emp_value

    # extra filters
    if var.filter_json:
        try:
            extra = json.loads(var.filter_json)
            if isinstance(extra, dict):
                filters.update(extra)
        except (ValueError, TypeError):
            frappe.log_error(
                title="TPE: bad filter_json on KPI Variable {0}".format(variable_name),
                message=var.filter_json,
            )

    agg = (var.aggregation_type or "Count").lower()
    try:
        if agg == "count":
            return float(frappe.db.count(var.target_doctype, filters))
        if agg == "sum":
            return _to_number(_aggregate(var.target_doctype, var.value_field, filters, "sum"))
        if agg in ("avg", "average"):
            return _to_number(_aggregate(var.target_doctype, var.value_field, filters, "avg"))
        if agg == "min":
            return _to_number(_aggregate(var.target_doctype, var.value_field, filters, "min"))
        if agg == "max":
            return _to_number(_aggregate(var.target_doctype, var.value_field, filters, "max"))
        if agg == "datediff":
            return _to_number(_aggregate(var.target_doctype, var.value_field, filters, "datediff"))
    except Exception as e:
        frappe.log_error(title="TPE variable resolve error", message=str(e))
    return 0.0


def _employee_filter_value(employee, employee_field_type):
    if not employee:
        return None
    if employee_field_type == "User":
        user = frappe.db.get_value("Employee", employee, "user_id")
        return user or None
    return employee


def _aggregate(doctype, fieldname, filters, fn):
    if not fieldname:
        return 0.0
    if fn == "datediff":
        # fieldname is expected to be "start_field,end_field"
        parts = [p.strip() for p in fieldname.split(",")]
        if len(parts) != 2:
            return 0.0
        rows = frappe.db.get_all(doctype, filters=filters, fields=[parts[0], parts[1]])
        total = 0.0
        for r in rows:
            total += _helper_days(r.get(parts[0]), r.get(parts[1]))
        return total
    col = "sum(`tab{0}`.`{1}`)".format(doctype, fieldname) if fn == "sum" else \
          "avg(`tab{0}`.`{1}`)".format(doctype, fieldname) if fn == "avg" else \
          "min(`tab{0}`.`{1}`)".format(doctype, fieldname) if fn == "min" else \
          "max(`tab{0}`.`{1}`)".format(doctype, fieldname)
    val = frappe.db.get_value(doctype, filters, col)
    return _to_number(val)


def compute_kpi(kpi, employee, from_date, to_date):
    """Compute a single KPI score (0..max_score) for an employee/period."""
    variables = resolve_variables(kpi, employee, from_date, to_date)
    formula = kpi.get("formula") or ""
    try:
        raw = evaluate(formula, variables)
    except FormulaError as e:
        frappe.log_error(title="TPE formula error for KPI {0}".format(kpi.get("name")),
                         message=str(e))
        raw = 0.0
    max_score = _to_number(kpi.get("max_score") or 100)
    if max_score and raw > max_score:
        raw = max_score
    if raw < 0:
        raw = 0.0
    return raw
