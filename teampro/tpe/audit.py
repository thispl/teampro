# -*- coding: utf-8 -*-
"""TPE Audit Trail helper."""
from __future__ import unicode_literals

import json

import frappe
from frappe.utils import now


def log(doctype, docname, action, details=None):
    try:
        frappe.get_doc({
            "doctype": "TPE Audit Log",
            "user": frappe.session.user,
            "doctype": doctype,
            "docname": str(docname),
            "action": action,
            "timestamp": now(),
            "details": json.dumps(details or {}, default=str),
        }).insert(ignore_permissions=True)
    except Exception as e:
        frappe.log_error(title="TPE audit log error", message=str(e))


def log_update(doc, method=None):
    log(doc.doctype, doc.name, "Update",
        {f: doc.get(f) for f in (doc.flags.track_fields or [])})


def log_trash(doc, method=None):
    log(doc.doctype, doc.name, "Delete")
