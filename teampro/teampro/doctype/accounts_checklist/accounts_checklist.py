# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
from datetime import date, timedelta

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate, get_datetime, now, cint


FREQUENCIES = ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"]


class AccountsChecklist(Document):
    def validate(self):
        self._compute_summary()
        self._compute_status()
        self._stamp_completion()

    def before_save(self):
        # auto-set completed_by / completed_on when status flips to Completed
        for row in self.items:
            if row.status == "Completed":
                if not row.completed_by:
                    row.completed_by = frappe.session.user
                if not row.completed_on:
                    row.completed_on = get_datetime()
            else:
                row.completed_by = None
                row.completed_on = None

    def _compute_summary(self):
        total = len(self.items)
        completed = sum(1 for r in self.items if r.status == "Completed")
        pending = sum(1 for r in self.items if r.status in ("Pending", "In Progress"))
        na = sum(1 for r in self.items if r.status == "Not Applicable")
        overdue = sum(1 for r in self.items if r.status == "Overdue")
        self.total_items = total
        self.completed_items = completed
        self.pending_items = pending
        self.overdue_items = overdue
        self.not_applicable_items = na
        denom = total - na
        self.completion_pct = round((completed / denom * 100), 2) if denom > 0 else 0

    def _compute_status(self):
        if self.total_items and self.completed_items + self.not_applicable_items >= self.total_items:
            self.status = "Completed"
        elif self.completed_items > 0 or any(r.status == "In Progress" for r in self.items):
            self.status = "In Progress"
        elif any(r.status == "Overdue" for r in self.items):
            self.status = "Overdue"
        else:
            self.status = "Open"

    def _stamp_completion(self):
        if self.status == "Completed" and not self.completed_on:
            self.completed_on = get_datetime()
        if self.status != "Completed":
            self.completed_on = None


# ---------------------------------------------------------------------------
# Period helpers
# ---------------------------------------------------------------------------

def get_period(frequency, ref_date=None):
    """Return (period_start, period_end, period_label) for a frequency."""
    d = getdate(ref_date) if ref_date else getdate()

    if frequency == "Daily":
        return d, d, d.strftime("%d-%b-%Y")

    if frequency == "Weekly":
        start = d - timedelta(days=d.weekday())  # Monday
        end = start + timedelta(days=6)
        return start, end, "Week %s" % start.strftime("%d-%b-%Y")

    if frequency == "Monthly":
        start = date(d.year, d.month, 1)
        end = date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])
        return start, end, d.strftime("%b %Y")

    if frequency == "Quarterly":
        q = (d.month - 1) // 3 + 1
        start_month = (q - 1) * 3 + 1
        start = date(d.year, start_month, 1)
        end = date(d.year, start_month + 2, calendar.monthrange(d.year, start_month + 2)[1])
        return start, end, "Q%d %d" % (q, d.year)

    if frequency == "Yearly":
        # Indian fiscal year: Apr 1 -> Mar 31
        fy_start = date(d.year, 4, 1) if d.month >= 4 else date(d.year - 1, 4, 1)
        fy_end = date(fy_start.year + 1, 3, 31)
        return fy_start, fy_end, "FY%d-%d" % (fy_start.year, fy_start.year + 1)

    frappe.throw(_("Unknown frequency: {0}").format(frequency))


def _due_date_for(template_item, period_start, period_end):
    due_day = cint(template_item.statutory_due_day)
    if due_day > 0:
        try:
            return date(period_start.year, period_start.month, min(due_day, calendar.monthrange(period_start.year, period_start.month)[1]))
        except ValueError:
            return period_end
    return period_end


def _resolve_assignee(template_item, settings):
    if template_item.assigned_to_user:
        return template_item.assigned_to_user
    if template_item.assigned_to_role:
        users = frappe.get_all("Has Role", filters={"role": template_item.assigned_to_role, "parenttype": "User"}, fields=["parent"], limit=1)
        if users:
            return users[0].parent
    return settings.default_owner if settings else None


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def _exists(template, frequency, period_start, period_end):
    return frappe.db.exists(
        "Accounts Checklist",
        {
            "template": template,
            "frequency": frequency,
            "period_start": period_start,
            "period_end": period_end,
        },
    )


def generate(frequency, ref_date=None, template_name=None):
    """Generate (or return existing) Accounts Checklist for a frequency & date.

    Returns the name of the Accounts Checklist document (or None if no items).
    """
    settings = frappe.get_single("Accounts Checklist Settings")
    if not template_name:
        template_name = settings.default_template
    if not template_name:
        # fall back to first active template
        tpl = frappe.get_all("Accounts Checklist Template", filters={"is_active": 1}, limit=1, order_by="name")
        if not tpl:
            return None
        template_name = tpl[0].name

    template = frappe.get_doc("Accounts Checklist Template", template_name)
    period_start, period_end, period_label = get_period(frequency, ref_date)

    existing = _exists(template.name, frequency, period_start, period_end)
    if existing:
        return existing

    items = template.get_items_for_frequency(frequency, period_start)
    if not items:
        return None

    doc = frappe.new_doc("Accounts Checklist")
    doc.company = template.company or settings.default_company
    doc.template = template.name
    doc.frequency = frequency
    doc.period_start = period_start
    doc.period_end = period_end
    doc.period_label = period_label
    doc.generated_by = frappe.session.user
    doc.generated_on = get_datetime()

    for t in items:
        doc.append(
            "items",
            {
                "item_title": t.item_title,
                "category": t.category,
                "is_statutory": t.is_statutory,
                "compliance_reference": t.compliance_reference,
                "priority": t.priority,
                "status": "Pending",
                "due_date": _due_date_for(t, period_start, period_end),
                "assigned_to": _resolve_assignee(t, settings),
                "template_item": t.name,
                "remarks": t.description,
            },
        )

    doc.insert(ignore_permissions=True)
    return doc.name


# ---------------------------------------------------------------------------
# Whitelisted methods (called from UI buttons & scheduler)
# ---------------------------------------------------------------------------

@frappe.whitelist()
def generate_for_today():
    """Server action on Settings: generate all frequencies applicable today."""
    out = []
    for f in FREQUENCIES:
        name = generate(f)
        if name:
            out.append((f, name))
    frappe.db.commit()
    return out


@frappe.whitelist()
def generate_from_template(template=None, frequency=None, ref_date=None):
    """Server action on Template: generate a checklist for a chosen period."""
    if not frequency:
        frappe.throw(_("Frequency is required"))
    name = generate(frequency, ref_date=ref_date, template_name=template)
    frappe.db.commit()
    return name


@frappe.whitelist()
def mark_in_progress(name=None):
    """Mark all pending items of a checklist as In Progress."""
    if not name:
        return
    doc = frappe.get_doc("Accounts Checklist", name)
    for row in doc.items:
        if row.status == "Pending":
            row.status = "In Progress"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


@frappe.whitelist()
def generate_manual(frequency, ref_date=None, template=None):
    """Generic manual generation endpoint."""
    name = generate(frequency, ref_date=ref_date, template_name=template)
    frappe.db.commit()
    return name


# ---------------------------------------------------------------------------
# Scheduler entry points
# ---------------------------------------------------------------------------

def _auto_enabled():
    try:
        s = frappe.get_single("Accounts Checklist Settings")
        return bool(s.enable_auto_generation)
    except Exception:
        return False


def generate_daily():
    if _auto_enabled():
        generate("Daily")


def generate_weekly():
    if _auto_enabled():
        generate("Weekly")


def generate_monthly():
    if _auto_enabled():
        generate("Monthly")


def generate_quarterly():
    if _auto_enabled():
        generate("Quarterly")


def generate_yearly():
    if _auto_enabled():
        generate("Yearly")


def mark_overdue():
    """Sweep: mark pending items past due as Overdue."""
    today = getdate()
    checklists = frappe.get_all(
        "Accounts Checklist",
        filters={"status": ["in", ["Open", "In Progress"]], "docstatus": ["<", 2]},
        fields=["name"],
    )
    updated = 0
    for c in checklists:
        doc = frappe.get_doc("Accounts Checklist", c.name)
        changed = False
        for row in doc.items:
            if row.status in ("Pending", "In Progress") and row.due_date and getdate(row.due_date) < today:
                row.status = "Overdue"
                changed = True
        if changed:
            doc.save(ignore_permissions=True)
            updated += 1
    if updated:
        frappe.db.commit()
    return updated


# ---------------------------------------------------------------------------
# Seed (called by patch + after_install)
# ---------------------------------------------------------------------------

def seed_default_template():
    """Create the Default Accounts Checklist Template with common items if missing."""
    if frappe.db.exists("Accounts Checklist Template", "Default Accounts Checklist"):
        return

    template = frappe.get_doc(
        {
            "doctype": "Accounts Checklist Template",
            "template_name": "Default Accounts Checklist",
            "is_active": 1,
            "items": _default_items(),
        }
    )
    template.insert(ignore_permissions=True)
    frappe.db.commit()


def _default_items():
    items = []

    def add(title, category, frequency, statutory=0, ref="", priority="Medium", due_day=None, months="All"):
        items.append(
            {
                "item_title": title,
                "category": category,
                "frequency": frequency,
                "is_statutory": statutory,
                "compliance_reference": ref,
                "priority": priority,
                "statutory_due_day": due_day or 0,
                "applicable_months": months,
            }
        )

    # Daily / Internal Accounts
    add("Bank balance & movement review", "Internal Accounts", "Daily")
    add("Petty cash reconciliation", "Internal Accounts", "Daily")
    add("Voucher posting & verification", "Internal Accounts", "Daily")
    add("Sales & purchase register review", "Internal Accounts", "Daily")
    add("Receipt & payment entry checking", "Internal Accounts", "Daily")
    # Weekly / Internal + MIS
    add("Bank reconciliation (BRS) update", "Internal Accounts", "Weekly")
    add("Debtor aging review", "Management MIS", "Weekly")
    add("Creditor aging review", "Management MIS", "Weekly")
    add("Cash flow summary to management", "Management MIS", "Weekly")
    add("Pending invoice / GRN matching", "Internal Accounts", "Weekly")
    # Monthly / Internal + Statutory + MIS
    add("Books finalization & ledger review", "Internal Accounts", "Monthly")
    add("Fixed asset depreciation posting", "Internal Accounts", "Monthly")
    add("Prepaid & accrual entries", "Internal Accounts", "Monthly")
    add("Stock ledger & valuation check", "Internal Accounts", "Monthly")
    add("GSTR-1 filing", "Statutory", "Monthly", statutory=1, ref="GSTR-1", due_day=11)
    add("GSTR-3B filing", "Statutory", "Monthly", statutory=1, ref="GSTR-3B", due_day=20)
    add("TDS return (24Q/26Q) deposit & return", "Statutory", "Monthly", statutory=1, ref="TDS", due_day=7)
    add("EPF challan & return", "Statutory", "Monthly", statutory=1, ref="EPF", due_day=15)
    add("ESI challan & return", "Statutory", "Monthly", statutory=1, ref="ESI", due_day=15)
    add("Professional Tax return", "Statutory", "Monthly", statutory=1, ref="PT", due_day=20)
    add("Advance tax computation", "Statutory", "Monthly", statutory=1, ref="Advance Tax", due_day=15)
    add("MIS - P&L and Balance Sheet snapshot", "Management MIS", "Monthly")
    add("Budget vs Actual - monthly review", "Management MIS", "Monthly")
    # Quarterly
    add("Quarterly GSTR-9 / 9C preparation", "Statutory", "Quarterly", statutory=1, ref="GSTR-9")
    add("TDS quarterly return filing", "Statutory", "Quarterly", statutory=1, ref="TDS Q")
    add("Quarterly board pack / financials", "Management MIS", "Quarterly")
    add("GST reconciliation with books", "Internal Accounts", "Quarterly")
    # Yearly / Audit & Year-end
    add("Annual books closure", "Internal Accounts", "Yearly")
    add("Fixed asset register & physical verification", "Audit Year-end", "Yearly", statutory=1, ref="FAR")
    add("Stock taking / physical inventory", "Audit Year-end", "Yearly")
    add("Form 16 issuance", "Statutory", "Yearly", statutory=1, ref="Form 16", due_day=15, months="Jun")
    add("Form 26AS / AIS reconciliation", "Statutory", "Yearly", statutory=1, ref="26AS")
    add("Income Tax Return filing", "Statutory", "Yearly", statutory=1, ref="ITR", due_day=31, months="Oct")
    add("GSTR-9 / 9C annual return", "Statutory", "Yearly", statutory=1, ref="GSTR-9C", due_day=31, months="Dec")
    add("Statutory audit coordination", "Audit Year-end", "Yearly")
    add("Tax audit (Form 3CD) preparation", "Audit Year-end", "Yearly", statutory=1, ref="3CD")
    add("Year-end MIS & annual report", "Management MIS", "Yearly")
    return items
