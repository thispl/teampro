# -*- coding: utf-8 -*-
"""TPE installation / seed data.

Creates the TPE module def, default TPE Settings, and seeds the IT Developer
KPIs/KRAs described in the SRS (Development Delivery Excellence, Development
Quality, Productivity, Documentation Compliance, Customer Relationship
Excellence).
"""
from __future__ import unicode_literals

import frappe
from frappe import _


def after_install():
    _ensure_module()
    _ensure_settings()
    _seed_it_developer_kpis()
    _seed_it_developer_kras()


def _ensure_module():
    if not frappe.db.exists("Module Def", "TPE"):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "TPE",
            "app_name": "teampro",
            "label": "TPE",
        }).insert(ignore_permissions=True)


def _ensure_settings():
    if not frappe.db.exists("TPE Settings", "TPE Settings"):
        frappe.get_doc({"doctype": "TPE Settings", "name": "TPE Settings"}) \
            .insert(ignore_permissions=True)


def _find_department(name):
    """Find a department by name, handling company-suffixed names."""
    # Try exact match first
    if frappe.db.exists("Department", name):
        return name
    # Try like match (IT Services - THIS, IT Services - TFP, etc.)
    result = frappe.db.get_all("Department",
                               filters={"department_name": name},
                               fields=["name"], limit=1)
    if result:
        return result[0].name
    # Try like on the full name
    result = frappe.db.get_all("Department",
                               filters={"name": ["like", "%{0}%".format(name)]},
                               fields=["name"], limit=1)
    if result:
        return result[0].name
    return None


def _kpi_variable(name, **kwargs):
    if frappe.db.exists("KPI Variable", name):
        return
    frappe.get_doc({"doctype": "KPI Variable", "variable_name": name, "active": 1, **kwargs}) \
        .insert(ignore_permissions=True)


def _kpi(name, **kwargs):
    if frappe.db.exists("KPI Master", name):
        return
    frappe.get_doc({"doctype": "KPI Master", "kpi_name": name, "active": 1,
                    "auto_calculation": 1, "max_score": 100, **kwargs}) \
        .insert(ignore_permissions=True)


def _kra(name, **kwargs):
    if frappe.db.exists("KRA Master", name):
        return
    frappe.get_doc({"doctype": "KRA Master", "kra_name": name, "active": 1, **kwargs}) \
        .insert(ignore_permissions=True)


def _seed_it_developer_kpis():
    dept = _find_department("IT Services")
    if not dept:
        frappe.log_error(title="TPE install: IT Services department not found",
                         message="Skipping IT Developer KPI seed")
        return
    # Variables bound to the TPE Task doctype
    _kpi_variable("completed_rt",
                  description="Sum of Required Time for completed TPE Tasks",
                  target_doctype="TPE Task", employee_link_field="developer",
                  employee_field_type="Employee", date_field="completed_date",
                  aggregation_type="Sum", value_field="required_time",
                  filter_json='{"status": "Completed", "docstatus": 1}')
    _kpi_variable("completed_at",
                  description="Sum of Actual Time for completed TPE Tasks",
                  target_doctype="TPE Task", employee_link_field="developer",
                  employee_field_type="Employee", date_field="completed_date",
                  aggregation_type="Sum", value_field="actual_time",
                  filter_json='{"status": "Completed", "docstatus": 1}')
    _kpi_variable("assigned_rt",
                  description="Sum of Required Time for all assigned TPE Tasks",
                  target_doctype="TPE Task", employee_link_field="developer",
                  employee_field_type="Employee", date_field="allocated_date",
                  aggregation_type="Sum", value_field="required_time")
    _kpi_variable("completed_tasks",
                  description="Count of completed TPE Tasks",
                  target_doctype="TPE Task", employee_link_field="developer",
                  employee_field_type="Employee", date_field="completed_date",
                  aggregation_type="Count",
                  filter_json='{"status": "Completed", "docstatus": 1}')
    _kpi_variable("first_time_accepted_tasks",
                  description="Completed tasks with zero reopen count",
                  target_doctype="TPE Task", employee_link_field="developer",
                  employee_field_type="Employee", date_field="completed_date",
                  aggregation_type="Count", value_field="",
                  filter_json='{"status": "Completed", "docstatus": 1, "reopened_count": 0}')
    _kpi_variable("completed_documentation",
                  description="Completed tasks with documentation marked done",
                  target_doctype="TPE Task", employee_link_field="developer",
                  employee_field_type="Employee", date_field="completed_date",
                  aggregation_type="Count",
                  filter_json='{"status": "Completed", "docstatus": 1, "remarks": ["like", "%documentation done%"]}')
    _kpi_variable("required_documentation",
                  description="All completed tasks (documentation required baseline)",
                  target_doctype="TPE Task", employee_link_field="developer",
                  employee_field_type="Employee", date_field="completed_date",
                  aggregation_type="Count",
                  filter_json='{"status": "Completed", "docstatus": 1}')
    _kpi_variable("avg_customer_rating",
                  description="Average overall customer rating (1-5)",
                  target_doctype="Customer Rating", employee_link_field="employee",
                  employee_field_type="Employee", date_field="rating_date",
                  aggregation_type="Average", value_field="overall_rating")

    # KPIs
    _kpi("Development Delivery Excellence",
         department=dept,
         frequency="Monthly",
         weightage=30,
         formula="(completed_rt / completed_at) * 100",
         data_source="TPE Task (completed)",
         variables=[
             {"kpi_variable": "completed_rt", "alias": "completed_rt"},
             {"kpi_variable": "completed_at", "alias": "completed_at"},
         ])

    _kpi("Development Quality",
         department=dept,
         frequency="Monthly",
         weightage=25,
         formula="(first_time_accepted_tasks / completed_tasks) * 100",
         data_source="TPE Task (reopened count)",
         variables=[
             {"kpi_variable": "first_time_accepted_tasks", "alias": "first_time_accepted_tasks"},
             {"kpi_variable": "completed_tasks", "alias": "completed_tasks"},
         ])

    _kpi("Productivity",
         department=dept,
         frequency="Monthly",
         weightage=25,
         formula="(completed_rt / assigned_rt) * 100",
         data_source="TPE Task (assigned vs completed)",
         variables=[
             {"kpi_variable": "completed_rt", "alias": "completed_rt"},
             {"kpi_variable": "assigned_rt", "alias": "assigned_rt"},
         ])

    _kpi("Documentation Compliance",
         department=dept,
         frequency="Monthly",
         weightage=10,
         formula="(completed_documentation / required_documentation) * 100",
         data_source="TPE Task (documentation)",
         variables=[
             {"kpi_variable": "completed_documentation", "alias": "completed_documentation"},
             {"kpi_variable": "required_documentation", "alias": "required_documentation"},
         ])

    _kpi("Customer Relationship Excellence",
         department=dept,
         frequency="Monthly",
         weightage=10,
         formula="(avg_customer_rating / 5) * 100",
         data_source="Customer Rating",
         variables=[
             {"kpi_variable": "avg_customer_rating", "alias": "avg_customer_rating"},
         ])


def _seed_it_developer_kras():
    dept = _find_department("IT Services")
    if not dept:
        return
    _kra("Development Delivery Excellence",
         department=dept, weightage=30,
         kpi_mapping=[{"kpi": "Development Delivery Excellence", "weightage": 100}])
    _kra("Development Quality",
         department=dept, weightage=25,
         kpi_mapping=[{"kpi": "Development Quality", "weightage": 100}])
    _kra("Productivity",
         department=dept, weightage=25,
         kpi_mapping=[{"kpi": "Productivity", "weightage": 100}])
    _kra("Documentation Compliance",
         department=dept, weightage=10,
         kpi_mapping=[{"kpi": "Documentation Compliance", "weightage": 100}])
    _kra("Customer Relationship Excellence",
         department=dept, weightage=10,
         kpi_mapping=[{"kpi": "Customer Relationship Excellence", "weightage": 100}])
