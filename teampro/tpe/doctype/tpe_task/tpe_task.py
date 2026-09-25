# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now, today

from teampro.tpe.benchmark import update_benchmark


STATUS_DATES = {
    "Allocated": "allocated_date",
    "Working": "started_date",
    "Pending Review": "review_date",
    "Completed": "completed_date",
}


class TPETask(Document):
    def before_validate(self):
        if not self.task_id:
            self.task_id = self.name

    def before_save(self):
        prev = self.get_doc_before_save()
        prev_status = prev.status if prev else None
        if self.status != prev_status:
            self._stamp_status_date(self.status)
            if self.status == "Reopened":
                self.reopened_count = (self.reopened_count or 0) + 1
                self.status = "Working"
                self._stamp_status_date("Working")

    def on_submit(self):
        if self.status != "Completed":
            self.status = "Completed"
            self.completed_date = now()
            self.db_update()
        try:
            update_benchmark(self)
        except Exception as e:
            frappe.log_error(title="TPE benchmark update error", message=str(e))

    def _stamp_status_date(self, status):
        field = STATUS_DATES.get(status)
        if field and not self.get(field):
            self.set(field, now())
