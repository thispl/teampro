# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe


def create_lead_ai_custom_fields():
	"""Create custom AI fields on the Lead doctype if they don't exist."""

	custom_fields = [
		{
			"fieldname": "custom_ai_score",
			"label": "AI Score",
			"fieldtype": "Int",
			"read_only": 1,
			"insert_after": "qualification_status",
			"description": "AI-generated lead score (0-100)",
		},
		{
			"fieldname": "custom_ai_rating",
			"label": "AI Rating",
			"fieldtype": "Select",
			"options": "\nHot\nWarm\nCold\nJob Applicant",
			"read_only": 1,
			"insert_after": "custom_ai_score",
			"description": "AI-generated lead rating",
		},
		{
			"fieldname": "custom_ai_summary",
			"label": "AI Summary",
			"fieldtype": "Small Text",
			"read_only": 1,
			"insert_after": "custom_ai_rating",
			"description": "AI-generated lead evaluation summary",
		},
		{
			"fieldname": "custom_ai_next_step",
			"label": "AI Next Step",
			"fieldtype": "Small Text",
			"read_only": 1,
			"insert_after": "custom_ai_summary",
			"description": "AI-recommended next action",
		},
	]

	for cf in custom_fields:
		existing = frappe.db.get_value(
			"Custom Field",
			{"dt": "Lead", "fieldname": cf["fieldname"]},
			"name",
		)
		if existing:
			continue

		doc = frappe.get_doc(
			{
				"doctype": "Custom Field",
				"dt": "Lead",
				"module": "Teampro",
				**cf,
			}
		)
		doc.insert(ignore_permissions=True)

	frappe.db.commit()
	frappe.clear_cache()
