# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import time_diff_in_hours
from frappe.model.document import Document


class TaskTimesheet(Document):
    def validate(self):
        if self.from_time and self.to_time:
            self.hours = time_diff_in_hours(self.to_time, self.from_time)
