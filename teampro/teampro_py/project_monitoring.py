import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate, nowdate

CLOSED_TASK_STATUSES = ("Completed", "Cancelled", "Template")
CLOSED_MINUTE_STATUSES = ("Completed", "Closed", "Cancelled")

# Statuses shown on the hours-based task status donut / aging stack.
# Extend or reorder to match the site's Task status options.
HOURS_STATUSES = ["Open", "Working", "Code Review", "Pending Review", "Client Review"]

# Card 1 counts Open tasks and their estimated hours.
# Set to True to count only Open tasks whose estimated hours are empty.
OPEN_TASK_REQUIRES_NO_ESTIMATE = False

REMARK_SUBJECT = "Project Remark"
DAILY_UPDATE_SUBJECT = "Daily Project Update"

AGING_BUCKETS = [
    ("0-3 Days", 0, 3),
    ("4-7 Days", 4, 7),
    ("8-15 Days", 8, 15),
    ("16-30 Days", 16, 30),
    ("30+ Days", 30, None),
]


def _task_age(task, today):
    start = task.act_start_date or task.exp_start_date or getdate(task.creation)
    if task.status in CLOSED_TASK_STATUSES:
        end = task.completed_on or task.act_end_date or getdate(task.modified)
    else:
        end = today
    return max(date_diff(end, start), 0)


def _aging_bucket(age):
    for label, low, high in AGING_BUCKETS:
        if age >= low and (high is None or age <= high):
            return label
    return "30+ Days"


@frappe.whitelist()
def get_project_monitoring_data(project, service=None, display_currency=None):
    if not project:
        frappe.throw(_("Project is required"))

    meta = frappe.get_meta("Project")
    project_fields = [
        "name", "project_name", "customer", "status", "priority",
        "percent_complete", "expected_start_date", "expected_end_date",
        "actual_start_date", "actual_end_date", "project_type",
        "department", "company", "estimated_costing", "total_costing_amount",
        "total_purchase_cost", "total_sales_amount", "total_billable_amount",
        "total_billed_amount", "gross_margin", "per_gross_margin",
        "sales_order",
    ]
    if meta.has_field("project_manager"):
        project_fields.append("project_manager")
    if meta.has_field("account_manager"):
        project_fields.append("account_manager")
    if meta.has_field("spoc"):
        project_fields.append("spoc")
    if meta.has_field("custom_estimated_hours"):
        project_fields.append("custom_estimated_hours")
    for f in ("contract_period_years", "contract_period_months", "billing_status",
              "expected_billing_date", "custom_spoc__next_contact_on",
              "custom_spoc_remark", "custom_spoc_remark_date",
              "remark", "custom_am_remark_date"):
        if meta.has_field(f):
            project_fields.append(f)

    project_doc = frappe.db.get_value(
        "Project", project, project_fields, as_dict=True
    )
    if not project_doc:
        frappe.throw(_("Project {0} not found").format(project))

    today = getdate(nowdate())

    task_filters = {"project": project}
    if service and frappe.get_meta("Task").has_field("service"):
        task_filters["service"] = service

    task_meta = frappe.get_meta("Task")
    task_fields = [
        "name", "subject", "status", "priority", "exp_start_date",
        "exp_end_date", "act_start_date", "act_end_date", "completed_on",
        "progress", "is_group", "creation", "modified",
        "expected_time", "actual_time", "is_milestone",
    ]
    if task_meta.has_field("type"):
        task_fields.append("type")
    if task_meta.has_field("custom_issue_type"):
        task_fields.append("custom_issue_type")
    if task_meta.has_field("custom_allocated_to"):
        task_fields.append("custom_allocated_to")

    tasks = frappe.get_list(
        "Task",
        filters=task_filters,
        fields=task_fields,
        order_by="modified desc",
        limit_page_length=0,
    )

    task_names = [t.name for t in tasks]
    revisions = _get_task_revisions(task_names)
    status_counts = {}
    status_hours = {}
    bucket_counts = {label: 0 for label, _low, _high in AGING_BUCKETS}
    aging_hours = {label: {} for label, _low, _high in AGING_BUCKETS}
    open_tasks = {"count": 0, "hours": 0.0}
    working_tasks = {"count": 0, "hours": 0.0}
    est_total = 0.0
    act_total = 0.0
    task_rows = []

    for task in tasks:
        if task.status == "Cancelled":
            continue
        closed = task.status in CLOSED_TASK_STATUSES
        age = _task_age(task, today)
        overdue = bool(
            task.exp_end_date
            and getdate(task.exp_end_date) < today
            and not closed
        )
        bucket = _aging_bucket(age)
        display_status = "Overdue" if overdue else task.status
        et = task.expected_time or 0
        at = task.actual_time or 0
        est_total += et
        act_total += at

        status_counts[display_status] = status_counts.get(display_status, 0) + 1
        sh = status_hours.setdefault(display_status, {"count": 0, "hours": 0.0})
        sh["count"] += 1
        sh["hours"] += et

        if not closed:
            bucket_counts[bucket] += 1
            aging_hours[bucket][display_status] = (
                aging_hours[bucket].get(display_status, 0) + et
            )

        if task.status == "Open" and (
            not OPEN_TASK_REQUIRES_NO_ESTIMATE or not task.expected_time
        ):
            open_tasks["count"] += 1
            open_tasks["hours"] += et
        if task.status == "Working":
            working_tasks["count"] += 1
            working_tasks["hours"] += et

        task_rows.append({
            "name": task.name,
            "subject": task.subject,
            "status": display_status,
            "priority": task.priority,
            "task_type": task.get("custom_issue_type") or task.get("type"),
            "allocated_to": task.get("custom_allocated_to"),
            "exp_start_date": task.exp_start_date,
            "exp_end_date": task.exp_end_date,
            "progress": task.progress or 0,
            "is_group": task.is_group,
            "age": age,
            "aging_bucket": bucket,
            "overdue": overdue,
            "et": et,
            "at": at,
            "rt": max(et - at, 0),
            "overrun": max(at - et, 0),
            "is_milestone": task.is_milestone,
            "completed_on": task.completed_on,
            "creation": task.creation,
            "modified": task.modified,
            "revisions": revisions.get(task.name, 0),
        })

    if frappe.db.table_exists("Meeting"):
        meetings, meeting_kpis = _get_meeting_data(project, today)
    else:
        meetings, meeting_kpis = [], {
            "total": 0, "scheduled": 0, "in_progress": 0,
            "completed": 0, "cancelled": 0,
        }

    is_amc = (project_doc.get("project_type") or "") == "AMC"
    sla = _get_amc_sla(project_doc) if is_amc else {}

    total_tasks = len(task_rows)
    completed_tasks = status_counts.get("Completed", 0)
    task_completion = round(completed_tasks / total_tasks * 100) if total_tasks else 0

    return {
        "project": project_doc,
        "pace": _get_pace(project_doc, today),
        "billing": (_get_amc_billing(project_doc, display_currency, sla)
                    if is_amc else _get_billing(project_doc, display_currency)),
        "kpis": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": sum(
                status_counts.get(s, 0)
                for s in ("Working", "Code Review", "Pending Review", "Client Review", "In Progress")
            ),
            "on_hold_tasks": status_counts.get("Hold", 0),
            "overdue_tasks": status_counts.get("Overdue", 0),
            "task_completion": task_completion,
            "project_progress": project_doc.percent_complete or 0,
            "meeting_total": meeting_kpis.get("total", 0),
            "meeting_completed": meeting_kpis.get("completed", 0),
            "meeting_completion": round(
                meeting_kpis.get("completed", 0) / meeting_kpis.get("total", 1) * 100
            ) if meeting_kpis.get("total") else 0,
        },
        "status_counts": status_counts,
        "status_hours": status_hours,
        "aging_buckets": [
            {"label": label, "count": bucket_counts[label]}
            for label, _low, _high in AGING_BUCKETS
        ],
        "aging_hours": [
            {
                "label": label,
                "total": sum(aging_hours[label].values()),
                "segments": aging_hours[label],
            }
            for label, _low, _high in AGING_BUCKETS
        ],
        "is_amc": is_amc,
        "contract": {
            "years": project_doc.get("contract_period_years"),
            "months": project_doc.get("contract_period_months"),
            "billing_status": project_doc.get("billing_status"),
            "expected_billing_date": project_doc.get("expected_billing_date"),
            "next_contact_on": project_doc.get("custom_spoc__next_contact_on"),
            "sla_from": sla.get("sla_from_date"),
            "sla_to": sla.get("sla_to_date"),
            "sla_status": sla.get("status"),
        },
        "open_tasks": open_tasks,
        "working_tasks": working_tasks,
        "hours": {
            # Estimated prefers the project-level custom_estimated_hours
            # (e.g. SO value / rate); falls back to the task-hour sum.
            "estimated": flt(project_doc.get("custom_estimated_hours")) or est_total,
            "task_estimated": est_total,
            "actual": act_total,
            "balance": (flt(project_doc.get("custom_estimated_hours")) or est_total) - act_total,
            "overrun": max(act_total - (flt(project_doc.get("custom_estimated_hours")) or est_total), 0),
        },
        "remarks": _get_project_remarks(project, REMARK_SUBJECT),
        "daily_updates": _get_project_remarks(project, DAILY_UPDATE_SUBJECT),
        "today_update": _get_today_update(project, today),
        "currencies": frappe.get_all(
            "Currency", filters={"enabled": 1}, pluck="name", order_by="name"
        ),
        "tasks": task_rows,
        "meetings": meetings,
        "meeting_kpis": meeting_kpis,
    }


def _get_pace(project_doc, today):
    start, end = project_doc.expected_start_date, project_doc.expected_end_date
    if not (start and end):
        return None
    start, end = getdate(start), getdate(end)
    total_days = date_diff(end, start)
    if total_days <= 0:
        return None
    elapsed = min(max(date_diff(today, start), 0), total_days)
    expected_pct = round(elapsed / total_days * 100)
    actual_pct = project_doc.percent_complete or 0
    return {
        "expected_pct": expected_pct,
        "actual_pct": actual_pct,
        "days_diff": round((expected_pct - actual_pct) / 100 * total_days),
    }


def _company_ccy(company):
    ccy = None
    if company:
        ccy = frappe.get_cached_value("Company", company, "default_currency")
    return ccy or frappe.get_cached_value(
        "Global Defaults", "Global Defaults", "default_currency"
    )


def _exchange_rate(from_ccy, to_ccy):
    row = frappe.get_all(
        "Currency Exchange",
        filters={"from_currency": from_ccy, "to_currency": to_ccy},
        fields=["exchange_rate"],
        order_by="date desc",
        limit=1,
    )
    if row and row[0].exchange_rate:
        return row[0].exchange_rate
    rev = frappe.get_all(
        "Currency Exchange",
        filters={"from_currency": to_ccy, "to_currency": from_ccy},
        fields=["exchange_rate"],
        order_by="date desc",
        limit=1,
    )
    if rev and rev[0].exchange_rate:
        return 1 / rev[0].exchange_rate
    return None


def _outstanding_sql(company_ccy, where, params):
    """Sum submitted-SI outstanding converted to company_ccy.

    outstanding_amount is stored in the receivable (party) account currency;
    apply conversion_rate when that account is foreign.
    """
    return frappe.db.sql(
        f"""
        SELECT COALESCE(SUM(
            CASE
                WHEN acc.account_currency IS NULL OR acc.account_currency = %s
                    THEN si.outstanding_amount
                ELSE si.outstanding_amount * si.conversion_rate
            END
        ), 0)
        FROM `tabSales Invoice` si
        LEFT JOIN `tabAccount` acc ON acc.name = si.debit_to
        WHERE si.docstatus = 1 AND {where}
        """,
        (company_ccy, *params),
    )[0][0] or 0


def _si_aging(company_ccy, where, params):
    """Outstanding bucketed by invoice age (0-30 / 31-60 / 60+), in
    company_ccy."""
    rows = frappe.db.sql(
        f"""
        SELECT
            CASE
                WHEN DATEDIFF(CURDATE(), si.posting_date) <= 30 THEN '0-30'
                WHEN DATEDIFF(CURDATE(), si.posting_date) <= 60 THEN '31-60'
                ELSE '60+'
            END AS bucket,
            COALESCE(SUM(
                CASE
                    WHEN acc.account_currency IS NULL OR acc.account_currency = %s
                        THEN si.outstanding_amount
                    ELSE si.outstanding_amount * si.conversion_rate
                END
            ), 0) AS amt
        FROM `tabSales Invoice` si
        LEFT JOIN `tabAccount` acc ON acc.name = si.debit_to
        WHERE si.docstatus = 1 AND si.outstanding_amount > 0 AND {where}
        GROUP BY bucket
        """,
        (company_ccy, *params),
        as_dict=True,
    )
    return {r.bucket: r.amt for r in rows}


def _get_billing(project_doc, display_currency):
    # Amounts are computed in each document's own company currency first
    # (base_* fields already carry the document conversion_rate), then
    # converted to the requested display currency via Currency Exchange rates.
    proj_ccy = _company_ccy(project_doc.company)
    display_ccy = display_currency or proj_ccy
    missing_rates = set()

    def conv(amount, from_ccy):
        amount = amount or 0
        if not amount or not from_ccy or not display_ccy or from_ccy == display_ccy:
            return amount
        rate = _exchange_rate(from_ccy, display_ccy)
        if rate is None:
            missing_rates.add("{0} → {1}".format(from_ccy, display_ccy))
            return amount
        return amount * rate

    # --- project-company amounts ---
    p_so = project_doc.total_sales_amount or 0
    p_billed = project_doc.total_billed_amount or 0
    p_coll = _outstanding_sql(proj_ccy, "si.project = %s", (project_doc.name,))
    p_aging = _si_aging(proj_ccy, "si.project = %s", (project_doc.name,))
    p_est = project_doc.estimated_costing or 0
    p_cost = project_doc.total_costing_amount or 0
    p_purchase = project_doc.total_purchase_cost or 0
    p_billable = project_doc.total_billable_amount or 0

    # --- amounts from the Sales Order selected on the project (possibly a
    # different company/currency) ---
    s_so = s_billed = s_coll = 0
    s_aging = {}
    s_ccy = proj_ccy
    selected_so = project_doc.get("sales_order")
    if selected_so:
        so = frappe.db.get_value(
            "Sales Order",
            selected_so,
            ["base_net_total", "project", "company"],
            as_dict=True,
        )
        if so and so.project != project_doc.name:
            s_ccy = _company_ccy(so.company)
            s_so = so.base_net_total or 0
            s_billed = frappe.db.sql(
                """
                SELECT COALESCE(SUM(sii.base_net_amount), 0)
                FROM `tabSales Invoice` si
                JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
                WHERE si.docstatus = 1
                  AND (si.project IS NULL OR si.project != %s)
                  AND sii.sales_order = %s
                """,
                (project_doc.name, selected_so),
            )[0][0] or 0
            s_coll = _outstanding_sql(
                s_ccy,
                """(si.project IS NULL OR si.project != %s)
                   AND si.name IN (
                       SELECT DISTINCT parent FROM `tabSales Invoice Item`
                       WHERE sales_order = %s
                   )""",
                (project_doc.name, selected_so),
            )
            s_aging = _si_aging(
                s_ccy,
                """(si.project IS NULL OR si.project != %s)
                   AND si.name IN (
                       SELECT DISTINCT parent FROM `tabSales Invoice Item`
                       WHERE sales_order = %s
                   )""",
                (project_doc.name, selected_so),
            )

    so_value = conv(p_so, proj_ccy) + conv(s_so, s_ccy)
    billed = conv(p_billed, proj_ccy) + conv(s_billed, s_ccy)
    collection_pending = conv(p_coll, proj_ccy) + conv(s_coll, s_ccy)
    collection_aging = {
        label: conv(p_aging.get(label, 0), proj_ccy) + conv(s_aging.get(label, 0), s_ccy)
        for label in ("0-30", "31-60", "60+")
    }

    return {
        "estimated_costing": conv(p_est, proj_ccy),
        "total_costing_amount": conv(p_cost, proj_ccy),
        "total_purchase_cost": conv(p_purchase, proj_ccy),
        "total_billable_amount": conv(p_billable, proj_ccy),
        "gross_margin": project_doc.gross_margin or 0,
        "per_gross_margin": project_doc.per_gross_margin or 0,
        "so_value": so_value,
        "billed_value": billed,
        "outstanding_amount": max(so_value - billed, 0),
        "collection_pending": collection_pending,
        "collection_aging": collection_aging,
        "display_currency": display_ccy,
        "source_currencies": sorted({c for c in (proj_ccy, s_ccy) if c}),
        "missing_rates": sorted(missing_rates),
    }


def _get_amc_billing(project_doc, display_currency, sla):
    """Financials for AMC projects: only Sales Orders carrying an AMC item
    (item_code LIKE '%AMC%') against this project. When SLA dates exist,
    prefers SOs raised inside the SLA window; otherwise the latest AMC SO.
    Billed / collection come from invoices tied to those SOs.
    """
    proj_ccy = _company_ccy(project_doc.company)
    display_ccy = display_currency or proj_ccy
    missing_rates = set()

    def conv(amount, from_ccy):
        amount = amount or 0
        if not amount or not from_ccy or not display_ccy or from_ccy == display_ccy:
            return amount
        rate = _exchange_rate(from_ccy, display_ccy)
        if rate is None:
            missing_rates.add("{0} → {1}".format(from_ccy, display_ccy))
            return amount
        return amount * rate

    amc_sos = frappe.db.sql(
        """
        SELECT DISTINCT so.name, so.company, so.transaction_date, so.base_net_total
        FROM `tabSales Order` so
        WHERE so.project = %s AND so.docstatus = 1
          AND EXISTS (
              SELECT 1 FROM `tabSales Order Item` soi
              WHERE soi.parent = so.name AND soi.item_code LIKE %s
          )
        ORDER BY so.transaction_date
        """,
        (project_doc.name, "%AMC%"),
        as_dict=True,
    )

    sla_from, sla_to = sla.get("sla_from_date"), sla.get("sla_to_date")
    if sla_from and sla_to:
        in_win = [
            r for r in amc_sos
            if r.transaction_date and sla_from <= getdate(r.transaction_date) <= sla_to
        ]
        chosen = in_win or amc_sos[-1:]
    else:
        chosen = amc_sos

    so_names = [r.name for r in chosen]
    so_value = sum(conv(r.base_net_total, _company_ccy(r.company)) for r in chosen)

    billed = collection = 0.0
    aging = {}
    if so_names:
        sos = tuple(so_names)
        for comp in {r.company for r in chosen}:
            ccy = _company_ccy(comp)
            billed += conv(
                frappe.db.sql(
                    """
                    SELECT COALESCE(SUM(sii.base_net_amount), 0)
                    FROM `tabSales Invoice` si
                    JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
                    WHERE si.docstatus = 1 AND si.company = %s
                      AND sii.sales_order IN %s
                    """,
                    (comp, sos),
                )[0][0],
                ccy,
            )
            where = (
                "si.company = %s AND si.name IN ("
                "SELECT DISTINCT parent FROM `tabSales Invoice Item` "
                "WHERE sales_order IN %s)"
            )
            params = (comp, sos)
            collection += conv(_outstanding_sql(ccy, where, params), ccy)
            for bk, amt in _si_aging(ccy, where, params).items():
                aging[bk] = aging.get(bk, 0) + conv(amt, ccy)

    return {
        "estimated_costing": conv(project_doc.estimated_costing or 0, proj_ccy),
        "total_costing_amount": conv(project_doc.total_costing_amount or 0, proj_ccy),
        "total_purchase_cost": conv(project_doc.total_purchase_cost or 0, proj_ccy),
        "total_billable_amount": conv(project_doc.total_billable_amount or 0, proj_ccy),
        "gross_margin": project_doc.gross_margin or 0,
        "per_gross_margin": project_doc.per_gross_margin or 0,
        "so_value": so_value,
        "billed_value": billed,
        "outstanding_amount": max(so_value - billed, 0),
        "collection_pending": collection,
        "collection_aging": aging,
        "display_currency": display_ccy,
        "source_currencies": sorted({c for c in {proj_ccy, display_ccy} if c}),
        "missing_rates": sorted(missing_rates),
        "amc_sos": so_names,
    }


def _get_task_revisions(task_names):
    """Version count per task — proxy for rework/reopen churn."""
    if not task_names or len(task_names) > 2000:
        return {}
    rows = frappe.db.sql(
        """
        SELECT docname, COUNT(*) AS c
        FROM `tabVersion`
        WHERE ref_doctype = 'Task' AND docname IN %(names)s
        GROUP BY docname
        """,
        {"names": task_names},
        as_dict=True,
    )
    return {r.docname: r.c for r in rows}


def _get_meeting_data(project, today):
    meetings = frappe.get_list(
        "Meeting",
        filters={"project": project},
        fields=[
            "name", "title", "status", "date", "from_time", "to_time",
            "organized_by", "creation", "modified",
        ],
        order_by="date desc",
        limit_page_length=0,
    )

    participants = {}
    open_items = {}
    overdue_items = {}
    if meetings:
        names = [m.name for m in meetings]
        for child_dt in ("Meeting Attendee", "External Attendees"):
            if frappe.db.table_exists(child_dt):
                for row in frappe.get_all(
                    child_dt,
                    filters={"parenttype": "Meeting", "parent": ["in", names]},
                    fields=["parent"],
                ):
                    participants[row.parent] = participants.get(row.parent, 0) + 1
        if frappe.db.table_exists("Meeting Minute"):
            for row in frappe.get_all(
                "Meeting Minute",
                filters={"parenttype": "Meeting", "parent": ["in", names]},
                fields=["parent", "status", "complete_by"],
            ):
                if row.status in CLOSED_MINUTE_STATUSES:
                    continue
                open_items[row.parent] = open_items.get(row.parent, 0) + 1
                if row.complete_by and getdate(row.complete_by) < today:
                    overdue_items[row.parent] = overdue_items.get(row.parent, 0) + 1

    kpis = {
        "total": len(meetings), "scheduled": 0, "in_progress": 0,
        "completed": 0, "cancelled": 0,
    }
    rows = []

    for meeting in meetings:
        if meeting.status in ("Planned", "Invitation Sent", "Scheduled"):
            kpis["scheduled"] += 1
        elif meeting.status in ("In Progress",):
            kpis["in_progress"] += 1
        elif meeting.status == "Completed":
            kpis["completed"] += 1
        elif meeting.status == "Cancelled":
            kpis["cancelled"] += 1

        meeting_date = getdate(meeting.date) if meeting.date else getdate(meeting.creation)
        if meeting.status in ("Completed", "Cancelled"):
            age = max(date_diff(meeting_date, getdate(meeting.creation)), 0)
        else:
            age = max(date_diff(today, getdate(meeting.creation)), 0)

        rows.append({
            "name": meeting.name,
            "title": meeting.title,
            "status": meeting.status,
            "age": age,
            "date": meeting.date,
            "from_time": meeting.from_time,
            "to_time": meeting.to_time,
            "organized_by": meeting.organized_by,
            "participants": participants.get(meeting.name, 0),
            "open_items": open_items.get(meeting.name, 0),
            "overdue_items": overdue_items.get(meeting.name, 0),
        })

    return rows, kpis


def get_project_dashboard(data):
    for group in data.get("transactions", []):
        if group.get("label") == _("Project") and "Meeting" not in group.get("items", []):
            group["items"].append("Meeting")
    return data


# ---------- Remarks & Daily Updates (stored as Frappe Comments) ----------

def _get_project_remarks(project, subject, limit=30):
    return frappe.get_all(
        "Comment",
        filters={
            "reference_doctype": "Project",
            "reference_name": project,
            "comment_type": "Comment",
            "subject": subject,
        },
        fields=["name", "content", "comment_by", "comment_email", "creation"],
        order_by="creation desc",
        limit=limit,
    )


def _get_today_update(project, today):
    rows = frappe.get_all(
        "Comment",
        filters={
            "reference_doctype": "Project",
            "reference_name": project,
            "comment_type": "Comment",
            "subject": DAILY_UPDATE_SUBJECT,
        },
        fields=["name", "content", "comment_by", "creation"],
        order_by="creation desc",
        limit=10,
    )
    for row in rows:
        if getdate(row.creation) == today:
            return row
    return None


def _add_comment(project, subject, content):
    if not frappe.has_permission("Project", "read", project):
        frappe.throw(_("Not permitted to update this project"), frappe.PermissionError)
    user = frappe.session.user
    comment = frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Comment",
        "reference_doctype": "Project",
        "reference_name": project,
        "comment_email": user,
        "comment_by": frappe.utils.get_fullname(user),
        "subject": subject,
        "content": content,
    })
    comment.insert(ignore_permissions=True)
    return comment.name


@frappe.whitelist()
def add_project_remark(project, remark):
    if not remark or not remark.strip():
        frappe.throw(_("Remark cannot be empty"))
    _add_comment(project, REMARK_SUBJECT, frappe.utils.escape_html(remark.strip()))
    return {"ok": True}


@frappe.whitelist()
def add_daily_update(project, progress="", completed="", issues="", plan=""):
    if not (progress or completed or issues or plan):
        frappe.throw(_("Daily update cannot be empty"))

    today = getdate(nowdate())
    if _get_today_update(project, today):
        frappe.throw(_("Today's update has already been submitted."))

    esc = frappe.utils.escape_html
    content = (
        "<b>{0}:</b><br>{1}<br><br>"
        "<b>{2}:</b><br>{3}<br><br>"
        "<b>{4}:</b><br>{5}<br><br>"
        "<b>{6}:</b><br>{7}"
    ).format(
        _("Today's Progress"), esc(progress or "-").replace("\n", "<br>"),
        _("Completed Today"), esc(completed or "-").replace("\n", "<br>"),
        _("Issues / Blockers"), esc(issues or "-").replace("\n", "<br>"),
        _("Tomorrow's Plan"), esc(plan or "-").replace("\n", "<br>"),
    )
    _add_comment(project, DAILY_UPDATE_SUBJECT, content)
    return {"ok": True}


def _get_amc_sla(project_doc):
    """Active SLA Details row on the customer for this project's service.

    SLA Details rows live on Customer.custom_sla_details (current) /
    custom_sla_history (past). Match sla_type=AMC + the project's service,
    preferring the row that links back to this project.
    """
    if not project_doc.customer or not frappe.db.exists("DocType", "SLA Details"):
        return {}
    filters = {
        "parent": project_doc.customer,
        "parentfield": "custom_sla_details",
        "sla_type": "AMC",
        "service": project_doc.get("service") or "IT-SW",
    }
    try:
        rows = frappe.get_all(
            "SLA Details",
            filters=filters,
            fields=["sla_from_date", "sla_to_date", "status", "project"],
            order_by="sla_to_date desc",
            limit_page_length=0,
        )
    except Exception:
        return {}
    for r in rows:
        if r.project == project_doc.name:
            return r
    return rows[0] if rows else {}
