import frappe
from erpnext.projects.doctype.task.task import Task
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day

class CustomTask(Task):
    def update_status(self):
        if self.status not in ('Cancelled', 'Completed','Hold','Pending Review') and self.exp_end_date:
            from datetime import datetime
            if self.exp_end_date < datetime.now().date():
                self.db_set('status', 'Overdue', update_modified=False)
                self.update_project()