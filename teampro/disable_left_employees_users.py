#!/usr/bin/env python
"""
Script to disable users for employees who have left the company.
This script checks all employees with status 'Left' and disables their linked users.
"""

import frappe

def disable_users_for_left_employees():
    """
    Find all employees with status 'Left' and disable their linked users.
    """
    # Get all employees with status 'Left' who have a user_id
    left_employees = frappe.get_all(
        "Employee",
        filters={
            "status": "Left",
            "user_id": ["!=", ""]
        },
        fields=["name", "employee_name", "user_id"]
    )
    
    if not left_employees:
        return "No employees with 'Left' status and linked users found."
    
    result = f"Found {len(left_employees)} employees with 'Left' status and linked users.\n"
    
    disabled_count = 0
    already_disabled_count = 0
    
    for employee in left_employees:
        user_id = employee.user_id
        employee_name = employee.employee_name
        employee_id = employee.name
        
        # Check if user exists and is enabled
        user_enabled = frappe.db.get_value("User", user_id, "enabled")
        
        if user_enabled is None:
            result += f"Warning: User {user_id} not found for employee {employee_name} ({employee_id})\n"
            continue
        
        if user_enabled == 1:
            # Disable the user
            try:
                frappe.db.set_value("User", user_id, "enabled", 0)
                result += f"Disabled user {user_id} for employee {employee_name} ({employee_id})\n"
                disabled_count += 1
            except Exception as e:
                result += f"Error disabling user {user_id}: {str(e)}\n"
        else:
            result += f"User {user_id} already disabled for employee {employee_name} ({employee_id})\n"
            already_disabled_count += 1
    
    result += f"\nSummary: Total employees processed: {len(left_employees)}, Users disabled: {disabled_count}, Users already disabled: {already_disabled_count}"
    return result