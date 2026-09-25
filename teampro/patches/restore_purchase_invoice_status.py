# Copyright (c) 2026, TeamPRO
# For license information, please see license.txt

"""Restore Purchase Invoice status to the core ERPNext behaviour.

Previously the `teampro` app maintained two custom status fields on the
Purchase Invoice doctype:

* ``custom_status`` (label "Workflow State") - a Select that was overwritten
  with the workflow state value (e.g. "Pending for CEO", "Approved") on every
  save via an ``on_update`` hook. It was shown in the list view, so the
  "Status" column displayed workflow-state values instead of the core status.
* ``custom_document_status`` (label "Document Status") - a Select with only
  ``Draft``/``Submitted``/``Cancelled`` options, set on submit and cancel.

Both fields are removed so that the core ERPNext ``status`` field
(Draft / Submitted / Paid / Partly Paid / Unpaid / Overdue / Cancelled /
Internal Transfer / Return / Debit Note Issued) becomes the single source of
truth. The core ``status`` field is already maintained correctly by ERPNext,
including payment-driven updates via ``update_voucher_outstanding`` which a
custom ``on_update`` hook could not reliably mirror.

The corresponding ``on_update`` / ``on_submit`` / ``on_cancel`` hooks have
been removed from ``hooks.py``.

This patch also cleans up:

* Orphaned ``Property Setter`` records that reference the deleted fields
  (per-field setters such as ``in_list_view`` and the doctype-level
  ``field_order`` JSON).
* Per-user saved list/report view settings stored in ``__UserSettings`` that
  still reference the removed fields in their ``fields``, ``filters``,
  ``sort_by`` or ``order_by`` keys. Without this cleanup, browsers keep
  sending the old column config and the server rejects the request with
  ``Field not permitted in query: tabPurchase Invoice.custom_status``.
"""

import json

import frappe


DOCTYPE = "Purchase Invoice"
CUSTOM_FIELDNAMES = ["custom_status", "custom_document_status"]


def execute():
    _delete_custom_fields()
    _delete_orphaned_property_setters()
    _cleanup_field_order()
    _cleanup_user_settings()
    _cleanup_client_scripts()
    _delete_listview_override_client_script()
    _show_workflow_state_in_list_view()


def _delete_listview_override_client_script():
    """Delete the Client Script that overrides Purchase Invoice list view settings.

    A Client Script named ``Purchase Invoice`` (dt = ``Purchase Invoice``)
    was replacing ``frappe.listview_settings['Purchase Invoice']`` entirely
    with a ``docstatus`` formatter, which caused the list view Status column
    to show "Draft / Submitted / Cancelled" (Document Status) instead of the
    core ERPNext status values (Unpaid / Paid / Partly Paid / Overdue / etc.).
    This deletes that Client Script so the core ``purchase_invoice_list.js``
    settings are restored.
    """
    name = frappe.db.get_value("Client Script", {"dt": DOCTYPE, "name": DOCTYPE})
    if name:
        frappe.delete_doc("Client Script", name, ignore_permissions=True)


def _show_workflow_state_in_list_view():
    """Enable ``in_list_view`` on the ``workflow_state`` custom field.

    This adds a separate "Workflow State" indicator column to the list view
    alongside the core "Status" column, so users can see both the payment
    status (Unpaid / Paid / Partly Paid / Overdue / etc.) and the workflow
    state (Pending for CEO / Approved / etc.) simultaneously.
    """
    name = frappe.db.get_value(
        "Custom Field", {"dt": DOCTYPE, "fieldname": "workflow_state"}
    )
    if name:
        frappe.db.set_value("Custom Field", name, "in_list_view", 1)

    # Fix the label Property Setter that was blanking out the column header
    ps_name = f"{DOCTYPE}-workflow_state-label"
    if frappe.db.exists("Property Setter", ps_name):
        frappe.db.set_value("Property Setter", ps_name, "value", "Workflow State")


def _cleanup_client_scripts():
    """Remove references to deleted fields from enabled Client Scripts.

    A manually-created Client Script (``Purchase Invoice-Form``) was setting
    ``custom_status`` on validate. With the field removed, this raises
    ``Field custom_status not found`` on save. Strip such references from any
    Client Script on the affected doctype.
    """
    names = frappe.db.get_list(
        "Client Script", {"dt": DOCTYPE}, pluck="name"
    )
    for name in names:
        script = frappe.db.get_value("Client Script", name, "script") or ""
        if not any(fn in script for fn in CUSTOM_FIELDNAMES):
            continue
        new_lines = [
            line
            for line in script.splitlines()
            if not any(fn in line for fn in CUSTOM_FIELDNAMES)
        ]
        frappe.db.set_value("Client Script", name, "script", "\n".join(new_lines))


def _delete_custom_fields():
    for fieldname in CUSTOM_FIELDNAMES:
        name = frappe.db.get_value(
            "Custom Field", {"dt": DOCTYPE, "fieldname": fieldname}, "name"
        )
        if name:
            frappe.delete_doc("Custom Field", name, ignore_permissions=True)


def _delete_orphaned_property_setters():
    """Remove Property Setters that reference the deleted custom fields."""
    frappe.db.delete(
        "Property Setter",
        {"doc_type": DOCTYPE, "field_name": ["in", CUSTOM_FIELDNAMES]},
    )


def _cleanup_field_order():
    """Remove the deleted fieldnames from the doctype-level ``field_order`` Property Setter."""
    ps_name = f"{DOCTYPE}-main-field_order"
    ps = frappe.db.get_value("Property Setter", ps_name, ["name", "value"])
    if not ps:
        return
    name, value = ps
    try:
        order = json.loads(value)
    except (TypeError, ValueError):
        return
    cleaned = [f for f in order if f not in CUSTOM_FIELDNAMES]
    if cleaned != order:
        frappe.db.set_value("Property Setter", name, "value", json.dumps(cleaned))


def _cleanup_user_settings():
    """Strip references to the removed fields from per-user saved view settings.

    Saved list/report view column configs are stored in the ``__UserSettings``
    cache table. Browsers send the saved config back to the server on each
    list/report load, so any leftover reference to a now-deleted field causes
    ``Field not permitted in query`` errors.
    """
    if not frappe.db.table_exists("__UserSettings"):
        return

    rows = frappe.db.sql(
        """select user, doctype, data from `__UserSettings`
           where data like %s or data like %s""",
        (f"%{CUSTOM_FIELDNAMES[0]}%", f"%{CUSTOM_FIELDNAMES[1]}%"),
        as_dict=True,
    )
    for r in rows:
        try:
            data = json.loads(r["data"])
        except (TypeError, ValueError):
            continue
        cleaned = _clean_user_setting_obj(data)
        new_json = json.dumps(cleaned)
        if new_json != r["data"]:
            frappe.db.sql(
                "update `__UserSettings` set data=%s where user=%s and doctype=%s",
                (new_json, r["user"], r["doctype"]),
            )


def _clean_user_setting_obj(obj):
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            if k == "filters":
                new[k] = _clean_filters(v)
            elif k == "fields":
                new[k] = _clean_fields(v)
            elif k == "sort_by" and isinstance(v, str) and v in CUSTOM_FIELDNAMES:
                new[k] = "creation"
            elif k == "order_by" and isinstance(v, str):
                for fn in CUSTOM_FIELDNAMES:
                    if fn in v:
                        v = "`tabPurchase Invoice`.`creation` desc"
                        break
                new[k] = v
            else:
                new[k] = _clean_user_setting_obj(v)
        return new
    if isinstance(obj, list):
        if obj and isinstance(obj[0], (list, tuple)):
            first = obj[0]
            if (
                len(first) >= 2
                and isinstance(first[1], str)
                and first[1] == DOCTYPE
            ):
                return _clean_fields(obj)
            return _clean_filters(obj)
        return [_clean_user_setting_obj(x) for x in obj]
    return obj


def _clean_filters(filters):
    cleaned = []
    for f in filters or []:
        if not isinstance(f, (list, tuple)) or len(f) < 2:
            cleaned.append(f)
            continue
        if f[1] in CUSTOM_FIELDNAMES:
            continue
        cleaned.append(f)
    return cleaned


def _clean_fields(fields):
    cleaned = []
    for f in fields or []:
        if not isinstance(f, (list, tuple)) or len(f) < 1:
            cleaned.append(f)
            continue
        if f[0] in CUSTOM_FIELDNAMES:
            continue
        cleaned.append(f)
    return cleaned
