# Copyright (c) 2026, TeamPRO
# For license information, please see license.txt

"""Automated WhatsApp Lunch Attendance.

This module reuses the existing WhatsApp integration from the `frappe_whatsapp`
app for credentials / settings (``WhatsApp Account`` doctype and
``frappe_whatsapp.utils.get_whatsapp_account``) and the standard Frappe
``make_post_request`` helper to dispatch messages to the Meta Cloud API.

It does NOT create a duplicate WhatsApp API wrapper. Credentials, phone_id,
graph URL and version are all read from the ``WhatsApp Account`` doctype that
is already maintained on site (e.g. the ``TEAMPRO`` account).
"""

import json

import frappe
from frappe import _
from frappe.integrations.utils import make_post_request
from frappe.utils import getdate, nowtime, now_datetime, cint

try:
    from frappe_whatsapp.utils import get_whatsapp_account
except Exception:  # pragma: no cover - frappe_whatsapp is an app dependency
    get_whatsapp_account = None


# ---------------------------------------------------------------------------
# Quick reply matching
# ---------------------------------------------------------------------------
# Meta auto-generates Quick-Reply button payloads (ids) at template creation
# time; you cannot set them to LUNCH_YES / LUNCH_NO. The webhook returns both
# ``button_reply.id`` (auto-generated) and ``button_reply.title`` (the label
# you set in Meta - "Yes" / "No" for the lunch_attendance template).
#
# We therefore match on the button TITLE, with the LUNCH_YES_/LUNCH_NO_ payload
# prefix kept as a fallback for tests / any future template that does support
# custom payloads.
LUNCH_YES_PAYLOAD = "LUNCH_YES"
LUNCH_NO_PAYLOAD = "LUNCH_NO"
LUNCH_PAYLOAD_PREFIXES = (LUNCH_YES_PAYLOAD, LUNCH_NO_PAYLOAD)
LUNCH_YES_TITLES = ("yes", "y")
LUNCH_NO_TITLES = ("no", "n")

# Food Count department mapping.
# Employee.department is a Link whose values look like "SubDept - Division - Company"
# (e.g. "Recruitment - THIS", "Accounts - TFP"). Food Count.department is a Select
# with short codes (IT, BCS, REC, R&S, F&A, DND, TFP, Common THIS). We map by
# matching the FIRST segment of the Employee.department string.
DEPARTMENT_KEYWORD_MAP = [
    ("IT", "IT"),
    ("IT. DEVELOPMENT", "IT"),
    ("BCS", "BCS"),
    ("RECRUITMENT", "REC"),
    ("R&S", "R&S"),
    ("ACCOUNTS", "F&A"),
    ("FINANCE", "F&A"),
    ("DND", "DND"),
    ("TFP", "TFP"),
    ("FACTORY", "TFP"),
    ("SUPPORT TEAM", "Common THIS"),
    ("GENERAL", "Common THIS"),
]
DEFAULT_FOOD_COUNT_DEPARTMENT = "Common THIS"


# ---------------------------------------------------------------------------
# Settings helpers
# ---------------------------------------------------------------------------
def get_settings():
    """Return the Lunch Attendance Settings single doc as a dict-like object."""
    return frappe.get_single("Lunch Attendance Settings")


def is_enabled():
    return cint(get_settings().enabled) == 1


# ---------------------------------------------------------------------------
# Eligibility / holiday helpers
# ---------------------------------------------------------------------------
def get_eligible_employees(settings=None):
    """Return list of active eligible employees with their mobile number."""
    settings = settings or get_settings()

    filters = {"status": "Active"}
    if settings.eligibility_filter == "By Department" and settings.department:
        filters["department"] = settings.department
    elif settings.eligibility_filter == "By Employment Type" and settings.employment_type:
        filters["employment_type"] = settings.employment_type
    elif (
        settings.eligibility_filter == "Is Food Eligible Flag"
        and cint(settings.use_food_eligible_flag)
    ):
        filters["custom_is_food_eligible"] = 1

    employees = frappe.get_all(
        "Employee",
        filters=filters,
        fields=["name", "employee_name", "cell_number", "holiday_list"],
    )
    # Only employees with a mobile number can be messaged.
    return [e for e in employees if (e.get("cell_number") or "").strip()]


def is_holiday(today=None, employee_holiday_list=None):
    """Check whether ``today`` is a holiday for the given holiday list."""
    today = getdate(today) if today else getdate()
    settings = get_settings()
    holiday_list = settings.holiday_list or employee_holiday_list
    if not holiday_list:
        return False

    return frappe.db.exists(
        "Holiday",
        {"parent": holiday_list, "holiday_date": today},
    )


# ---------------------------------------------------------------------------
# Sending helpers (reuse WhatsApp Account credentials)
# ---------------------------------------------------------------------------
def _get_account(settings):
    """Resolve the WhatsApp Account to use for sending.

    Reuses ``frappe_whatsapp.utils.get_whatsapp_account`` so credentials are
    never duplicated or hardcoded.
    """
    if settings.whatsapp_account:
        return frappe.get_doc("WhatsApp Account", settings.whatsapp_account)
    if get_whatsapp_account is None:
        frappe.throw(_("frappe_whatsapp app is required for Lunch Attendance"))
    account = get_whatsapp_account(account_type="outgoing")
    if not account:
        frappe.throw(_("Please set a default outgoing WhatsApp Account"))
    return account


def _normalize_number(number):
    """Strip whitespace / leading + / dashes so Meta accepts the number."""
    if not number:
        return number
    number = number.strip().replace(" ", "").replace("-", "")
    if number.startswith("+"):
        number = number[1:]
    return number


def _post_to_graph(account, payload):
    """POST a message payload to the Meta Graph API using account credentials."""
    token = account.get_password("token")
    headers = {
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    url = f"{account.url}/{account.version}/{account.phone_id}/messages"
    return make_post_request(url, headers=headers, data=json.dumps(payload))


def send_lunch_template(account, to_number, template, language_code, employee_name):
    """Send the lunch utility template with the employee name as body param.

    ``template`` is a ``WhatsApp Templates`` document. Quick-Reply buttons are
    part of the template definition on Meta's side, so no button parameters are
    sent here - the static payloads (``LUNCH_YES`` / ``LUNCH_NO``) are returned
    in the inbound webhook.
    """
    payload = {
        "messaging_product": "whatsapp",
        "to": _normalize_number(to_number),
        "type": "template",
        "template": {
            "name": template.actual_name or template.template_name,
            "language": {"code": language_code or template.language_code or "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": employee_name or ""}
                    ],
                }
            ],
        },
    }
    response = _post_to_graph(account, payload)
    message_id = None
    try:
        message_id = response["messages"][0]["id"]
    except (KeyError, TypeError, IndexError):
        pass
    return message_id, response


def send_free_form_text(account, to_number, text):
    """Send a free-form text message inside the 24-hr customer service window."""
    payload = {
        "messaging_product": "whatsapp",
        "to": _normalize_number(to_number),
        "type": "text",
        "text": {"body": text},
    }
    return _post_to_graph(account, payload)


# ---------------------------------------------------------------------------
# Scheduled daily outbound trigger
# ---------------------------------------------------------------------------
def send_daily_lunch_attendance():
    """Daily scheduled job: create Pending logs and dispatch the template.

    Registered in ``hooks.py`` under ``scheduler_events`` (cron 09:00). Skips
    holidays and disabled state. Idempotent: if a log already exists for an
    employee today it is not re-created.
    """
    settings = get_settings()
    if not cint(settings.enabled):
        return

    today = getdate()
    # Skip weekends (Saturday=5, Sunday=6) - Monday..Saturday per spec means
    # we only skip Sunday. Cron already runs daily, so we gate Sunday here.
    if today.weekday() == 6:  # Sunday
        return

    if not settings.whatsapp_template_name:
        frappe.log_error(
            title="Lunch Attendance: no template configured",
            message="Lunch Attendance Settings has no WhatsApp Template set.",
        )
        return

    template = frappe.get_doc("WhatsApp Templates", settings.whatsapp_template_name)
    account = _get_account(settings)

    for emp in get_eligible_employees(settings):
        # Holiday exclusion: per-employee holiday list takes precedence if set.
        if is_holiday(today, emp.get("holiday_list")):
            continue

        # Idempotency: skip if a log already exists for today.
        existing = frappe.db.exists(
            "Lunch Attendance Log",
            {"employee": emp.name, "date": today},
        )
        if existing:
            continue

        log = frappe.get_doc(
            {
                "doctype": "Lunch Attendance Log",
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "mobile_number": emp.cell_number,
                "date": today,
                "response": "Pending",
            }
        )
        try:
            log.insert(ignore_permissions=True)
        except frappe.DuplicateEntryError:
            # Race condition - another worker created it first.
            frappe.db.rollback()
            continue

        try:
            message_id, _ = send_lunch_template(
                account,
                emp.cell_number,
                template,
                settings.language_code,
                emp.employee_name,
            )
            log.db_set(
                {
                    "template_sent": 1,
                    "whatsapp_message_id": message_id,
                },
                notify=False,
            )
        except Exception:
            log.db_set(
                {"error_log": frappe.get_traceback()},
                notify=False,
            )
            frappe.log_error(
                title=f"Lunch Attendance send failed for {emp.name}",
                message=frappe.get_traceback(),
            )

    frappe.db.commit()


def mark_expired_logs():
    """Mark Pending logs past the cutoff time as Expired.

    Registered as a separate cron job (after cutoff). Idempotent.
    """
    settings = get_settings()
    if not cint(settings.enabled):
        return

    today = getdate()
    cutoff = settings.cutoff_time or "10:00:00"
    now = nowtime()

    frappe.db.sql(
        """
        UPDATE `tabLunch Attendance Log`
        SET response = 'Expired'
        WHERE date = %(date)s
          AND response = 'Pending'
          AND %(now)s > %(cutoff)s
        """,
        {"date": today, "now": now, "cutoff": cutoff},
    )
    frappe.db.commit()


# ---------------------------------------------------------------------------
# Consolidated count notification (scheduled at consolidation_time, e.g. 10:30)
# ---------------------------------------------------------------------------
def send_consolidated_lunch_count():
    """Send a consolidated lunch count breakdown to the admin via WhatsApp.

    Scheduled daily at ``consolidation_time`` (default 10:30). Groups today's
    ``Yes`` responses by department (auto-mapped from Employee.department) and
    sends a free-form WhatsApp text message to ``admin_mobile_number``.
    """
    settings = get_settings()
    if not cint(settings.enabled):
        return

    admin_number = (settings.admin_mobile_number or "").strip()
    if not admin_number:
        return

    today = getdate()

    # Gather all responses for today with employee department.
    logs = frappe.db.sql(
        """
        SELECT l.employee, l.employee_name, l.response, e.department
        FROM `tabLunch Attendance Log` l
        LEFT JOIN `tabEmployee` e ON e.name = l.employee
        WHERE l.date = %(date)s
        """,
        {"date": today},
        as_dict=True,
    )

    if not logs:
        return

    yes_by_dept = {}
    total_yes = 0
    total_no = 0
    total_pending = 0
    total_expired = 0

    for row in logs:
        resp = row["response"] or "Pending"
        if resp == "Yes":
            total_yes += 1
            dept = _map_department(row.get("department"))
            yes_by_dept[dept] = yes_by_dept.get(dept, 0) + 1
        elif resp == "No":
            total_no += 1
        elif resp == "Pending":
            total_pending += 1
        elif resp == "Expired":
            total_expired += 1

    # Build the message text.
    date_str = today.strftime("%d-%m-%Y")
    lines = [f"TEAMPRO Lunch Count - {date_str}", ""]
    if yes_by_dept:
        for dept in sorted(yes_by_dept.keys()):
            lines.append(f"  {dept}: {yes_by_dept[dept]}")
        lines.append("")
    lines.append(f"Total Yes: {total_yes}")
    lines.append(f"Total No: {total_no}")
    if total_pending:
        lines.append(f"Pending: {total_pending}")
    if total_expired:
        lines.append(f"Expired: {total_expired}")
    lines.append("")
    lines.append("Please place the order accordingly.")
    message = "\n".join(lines)

    try:
        account = _get_account(settings)
        send_free_form_text(account, admin_number, message)
    except Exception:
        frappe.log_error(
            title="Lunch Attendance consolidated count send failed",
            message=frappe.get_traceback(),
        )


# ---------------------------------------------------------------------------
# Webhook / inbound response handling
# ---------------------------------------------------------------------------
def _extract_button_title():
    """Extract the Quick-Reply button title from the raw Meta webhook payload.

    The ``frappe_whatsapp`` webhook stores only ``button_reply.id`` (which Meta
    auto-generates) in ``WhatsApp Message.message``. The button **title** -
    which is the only thing we control when creating the template - is present
    in the original webhook body at
    ``entry[].changes[].value.messages[].interactive.button_reply.title``.

    During the ``after_insert`` doc_event the raw payload is still available on
    ``frappe.local.form_dict``. Returns ``None`` if it cannot be found.
    """
    form_dict = getattr(frappe.local, "form_dict", None)
    if not form_dict:
        return None

    try:
        entries = form_dict.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for message in value.get("messages", []):
                    interactive = message.get("interactive")
                    if not interactive:
                        continue
                    button_reply = interactive.get("button_reply")
                    if button_reply and button_reply.get("title"):
                        return button_reply["title"]
    except (AttributeError, KeyError, TypeError):
        return None
    return None


def _resolve_response(doc):
    """Resolve an inbound button tap to 'Yes' / 'No' / None.

    Matching priority:
      1. Button title from the raw webhook payload (``Yes`` / ``No``) - this is
         what production uses, since Meta auto-generates button payloads.
      2. The stored ``WhatsApp Message.message`` field, which for Quick-Reply
         buttons contains the button title (e.g. ``Yes`` / ``No``) when Meta
         auto-generates the payload id.
      3. Fallback: ``LUNCH_YES_`` / ``LUNCH_NO_`` payload prefix on the stored
         ``WhatsApp Message.message`` field (used by tests and any future
         template that supports custom payloads).
    """
    title = _extract_button_title()
    if title:
        t = title.strip().lower()
        if t in LUNCH_YES_TITLES:
            return "Yes"
        if t in LUNCH_NO_TITLES:
            return "No"

    payload = (doc.message or "").strip()
    # Meta Quick-Reply buttons store the button TITLE as the message content
    # (the payload id is auto-generated and not configurable). Match it directly.
    t = payload.lower()
    if t in LUNCH_YES_TITLES:
        return "Yes"
    if t in LUNCH_NO_TITLES:
        return "No"
    # Legacy / custom-payload fallback.
    if payload.startswith(LUNCH_YES_PAYLOAD):
        return "Yes"
    if payload.startswith(LUNCH_NO_PAYLOAD):
        return "No"

    return None


def handle_incoming_whatsapp_message(doc, method=None):
    """doc_events hook on ``WhatsApp Message`` (after_insert).

    The ``frappe_whatsapp`` webhook already persists every inbound interactive
    button_reply as a ``WhatsApp Message`` (Incoming, content_type='button',
    ``from`` = sender phone, ``message`` = button_reply.id payload). We inspect
    those records here and update the matching Lunch Attendance Log.
    """
    if not is_enabled():
        return
    if doc.doctype != "WhatsApp Message":
        return
    if doc.type != "Incoming":
        return
    if doc.content_type != "button":
        return

    # Deduplicate webhook retries: if another WhatsApp Message with the same
    # Meta message_id was already processed earlier, skip this one.
    if doc.message_id:
        existing = frappe.db.sql(
            """
            SELECT name FROM `tabWhatsApp Message`
            WHERE message_id = %s AND `from` = %s
            AND name != %s
            AND creation < %s
            AND type = 'Incoming' AND content_type = 'button'
            LIMIT 1
            """,
            (doc.message_id, doc.get("from"), doc.name, doc.creation),
        )
        if existing:
            return

    new_response = _resolve_response(doc)
    if not new_response:
        return

    settings = get_settings()
    today = getdate()
    sender_phone = _normalize_number(doc.get("from"))

    # Match today's log by mobile number. Meta sends the full international
    # format (e.g. ``919715327487``) while Employee.cell_number may store only
    # the national number (e.g. ``9715327487``). Match in both directions:
    # either the log's number ends with the sender's, or vice-versa.
    logs_today = frappe.get_all(
        "Lunch Attendance Log",
        filters={"date": today, "response": "Pending"},
        fields=["name", "mobile_number"],
        order_by="creation desc",
    )
    log_name = None
    for l in logs_today:
        stored = _normalize_number(l.get("mobile_number"))
        if not stored or not sender_phone:
            continue
        if stored.endswith(sender_phone) or sender_phone.endswith(stored):
            log_name = l["name"]
            break
    if not log_name:
        # Nothing to update - no pending log for this sender today.
        return

    # Atomic update: only set the response if the log is still Pending.
    # If another hook already updated it, rowcount will be 0 and we skip.
    responded_at = now_datetime()
    frappe.db.sql(
        """
        UPDATE `tabLunch Attendance Log`
        SET response = %s, responded_at = %s
        WHERE name = %s AND response = 'Pending'
        """,
        (new_response, responded_at, log_name),
    )

    log = frappe.get_doc("Lunch Attendance Log", log_name)
    if log.response == "Expired":
        # Already marked expired by mark_expired_logs; nothing to do.
        return

    # If the atomic update did not actually change this row, another worker
    # already processed this (or a duplicate) message. Stop here.
    if log.response != new_response:
        return

    # Cutoff enforcement.
    cutoff = settings.cutoff_time or "10:00:00"
    if nowtime() > cutoff:
        # Revert the response back to Expired if it arrived after cutoff.
        log.db_set({"response": "Expired", "responded_at": None}, notify=False)
        try:
            account = _get_account(settings)
            send_free_form_text(
                account,
                sender_phone,
                _("Sorry! The cutoff time ({0}) for today's lunch request has passed.").format(
                    cutoff
                ),
            )
        except Exception:
            frappe.log_error(
                title="Lunch Attendance cutoff reply failed",
                message=frappe.get_traceback(),
            )
        frappe.db.commit()
        return

    # Optional ERP document creation on "Yes".
    if new_response == "Yes" and cint(settings.create_lunch_entry_on_yes):
        _create_lunch_entry(settings, log)

    # Free-form confirmation reply inside the 24-hr service window.
    if cint(settings.send_confirmation_reply):
        try:
            account = _get_account(settings)
            send_free_form_text(
                account,
                sender_phone,
                _("Thank you! Your lunch preference for today has been updated to: {0}.").format(
                    new_response
                ),
            )
        except Exception:
            frappe.log_error(
                title="Lunch Attendance confirmation reply failed",
                message=frappe.get_traceback(),
            )

    frappe.db.commit()


def _map_department(employee_dept):
    """Map an Employee.department (Link) value to a Food Count.department (Select) code.

    Employee.department strings look like ``SubDept - Division - Company``
    (e.g. ``Recruitment - THIS``, ``Accounts - TFP``). We match the first
    segment against known keywords and fall back to ``Common THIS``.
    """
    if not employee_dept:
        return DEFAULT_FOOD_COUNT_DEPARTMENT
    first_segment = employee_dept.split(" - ")[0].strip().upper()
    for keyword, food_count_dept in DEPARTMENT_KEYWORD_MAP:
        if keyword in first_segment:
            return food_count_dept
    return DEFAULT_FOOD_COUNT_DEPARTMENT


def _create_lunch_entry(settings, log):
    """Create the configured ERP document when an employee replies Yes.

    For the ``Food Count`` DocType, this also populates ``department`` (auto-mapped
    from Employee.department) and ``food_type`` (from Employee if available).
    The Food Count ``before_save`` validation enforces a 10:00 AM cutoff —
    responses arriving after that will fail to create a Food Count and the
    error is logged (per the "keep the 10:00 limit" requirement).
    """
    doctype = settings.lunch_entry_doctype
    if not doctype or not frappe.db.exists("DocType", doctype):
        return

    try:
        doc_dict = {
            "doctype": doctype,
            "employee": log.employee,
            "employee_name": log.employee_name,
            "date": log.date,
        }

        meta = frappe.get_meta(doctype)
        if meta.get_field("mobile_number"):
            doc_dict["mobile_number"] = log.mobile_number

        # Food Count-specific fields.
        if doctype == "Food Count":
            emp_dept = frappe.db.get_value("Employee", log.employee, "department")
            doc_dict["department"] = _map_department(emp_dept)
            # food_type: fetch from Employee custom field if it exists.
            emp_meta = frappe.get_meta("Employee")
            if emp_meta.get_field("custom_food_type"):
                food_type = frappe.db.get_value("Employee", log.employee, "custom_food_type")
                if food_type:
                    doc_dict["food_type"] = food_type
            # requested_by: use the system user.
            doc_dict["requested_by"] = "Administrator"

        entry = frappe.get_doc(doc_dict)
        entry.insert(ignore_permissions=True)
        log.db_set(
            {
                "lunch_entry_ref_doctype": doctype,
                "lunch_entry_ref_name": entry.name,
            },
            notify=False,
        )
    except Exception:
        frappe.log_error(
            title=f"Lunch Entry creation failed for {log.employee}",
            message=frappe.get_traceback(),
        )


# ---------------------------------------------------------------------------
# Manual trigger (whitelisted for testing / admin)
# ---------------------------------------------------------------------------
@frappe.whitelist()
def trigger_daily_send():
    """Manually trigger the daily lunch attendance send (admin/testing)."""
    send_daily_lunch_attendance()
    return _("Daily lunch attendance send triggered.")
