# Copyright (c) 2025, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RECWeekPlan(Document):
	# pass
    def validate(self):
        self.update_task_allocation_totals()
    def update_task_allocation_totals(self):
        task_exe_totals = {}
        for row in self.allocation:
            key = (row.task, row.exe)
            task_exe_totals[key] = task_exe_totals.get(key, 0) + (row.ac or 0)
        for row in self.task_allocation:
            key = (row.task, row.exe)
            if key in task_exe_totals:
                row.ac = task_exe_totals[key]


@frappe.whitelist()
def get_teampro_holidays(start_date, end_date):
    return frappe.get_all("Holiday", 
        filters={
            "parent": "TEAMPRO 2023",
            "holiday_date": ["between", [start_date, end_date]]
        },
        fields=["holiday_date"]
    )


@frappe.whitelist()
def update_allocation_actual_count(docname):
    doc = frappe.get_doc("REC Week Plan", docname)  # Replace with actual DocType name

    for row in doc.allocation:  # Replace 'allocation' with your actual child table fieldname
        task = row.task
        exe = row.exe
        date = row.date

        if task and exe and date:
            count = frappe.db.sql("""
                SELECT COUNT(DISTINCT c.name) AS status_count
                FROM `tabCandidate` c
                INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                WHERE DATE(cs.sourced_date) = %s
                AND cs.sourced_by = %s
                AND c.candidate_created_by = %s
                AND cs.task = %s
                AND cs.status IN (%s, %s)
            """, (date, exe, exe, task, "Submitted(Client)", "Submit(SPOC)"))

            row.ac = count[0][0] if count else 0

    doc.save()
    frappe.db.commit()
    return "AC updated successfully"