
import frappe
from frappe import _

@frappe.whitelist()
def get_leave_applications():

    user = frappe.session.user

    if "Leave Approver" not in frappe.get_roles(user):
        return []

    data = frappe.get_all(
        "Leave Application",
        filters={
            "workflow_state": "Pending for HOD",
            "leave_approver": user
        },
        fields=[
            "name",
            "employee",
            "employee_name",
            "from_date",
            "to_date",
            "total_leave_days",
            "leave_type",
            "description",
            "workflow_state",
            "creation",
            "half_day",
            "half_day_date"
        ],
        order_by="creation desc"
    )

    return data


@frappe.whitelist()
def approve_leave(docname):

    doc = frappe.get_doc("Leave Application", docname)

    doc.workflow_state = "Approved"
    doc.save(ignore_permissions=True)

    frappe.db.commit()

    return "Approved"


@frappe.whitelist()
def reject_leave(docname):

    doc = frappe.get_doc("Leave Application", docname)

    doc.workflow_state = "Rejected"
    doc.save(ignore_permissions=True)

    frappe.db.commit()

    return "Rejected"


@frappe.whitelist()
def get_leave_details(docname):

    doc = frappe.get_doc("Leave Application", docname)

    return {
        "name": doc.name,
        "employee": doc.employee,
        "employee_name": doc.employee_name,
        "from_date": doc.from_date,
        "to_date": doc.to_date,
        "creation": doc.creation,
        "total_leave_days": doc.total_leave_days,
        "leave_type": doc.leave_type,
        "description": doc.description,
        "status": doc.workflow_state,
        "half_day": doc.half_day,
        "half_day_date": doc.half_day_date,
        "custom_session":doc.custom_session
    }

@frappe.whitelist()
def bulk_approve(docs):

    import json

    if isinstance(docs, str):
        docs = json.loads(docs)

    from frappe.model.workflow import apply_workflow

    for docname in docs:

        doc = frappe.get_doc(
            "Leave Application",
            docname
        )

        apply_workflow(doc, "Approve")

    frappe.db.commit()

    return True

@frappe.whitelist()
def bulk_reject(docs):

    import json

    if isinstance(docs, str):
        docs = json.loads(docs)

    from frappe.model.workflow import apply_workflow

    for docname in docs:

        doc = frappe.get_doc(
            "Leave Application",
            docname
        )

        apply_workflow(doc, "Reject")

    frappe.db.commit()

    return True


# @frappe.whitelist()
# def get_expense_claims():

#     user = frappe.session.user
#     roles = frappe.get_roles(user)

#     states = []

#     if "HOD" in roles:
#         states.append("Pending for HOD")

#     if "Accounts Manager" in roles:
#         states.append("Pending for Accounts")

#     if "CEO" in roles:
#         states.append("Pending for CEO")

#     if not states:
#         return []

#     return frappe.get_all(
#         "Expense Claim",
#         filters={
#             "workflow_state": ["in", states]
#         },
#         fields=[
#             "name",
#             "employee",
#             "employee_name",
#             "grand_total",
#             "workflow_state"
#         ],
#         order_by="creation desc"
#     )

@frappe.whitelist()
def get_expense_claims():

    user = frappe.session.user
    roles = frappe.get_roles(user)

    # Priority order — CEO > Accounts Manager > HOD
    if "CEO" in roles:
        state = "Pending for CEO"
    elif "Accounts Manager" in roles:
        state = "Pending for Accounts"
    elif "HOD" in roles:
        state = "Pending for HOD"
    else:
        return []

    return frappe.get_all(
        "Expense Claim",
        filters={
            "workflow_state": state
        },
        fields=[
            "name",
            "employee",
            "employee_name",
            "grand_total",
            "workflow_state"
        ],
        order_by="creation desc"
    )
@frappe.whitelist()
def get_expense_details(docname):
    doc = frappe.get_doc("Expense Claim", docname)
    
    expenses = []
    for row in doc.expenses:
        expenses.append({
            "expense_date": row.expense_date,
            "description": row.description,
            "expense_type": row.expense_type,
            "custom_meet_log": row.custom_meet_log,
            "custom_meetlog_distance": row.custom_meetlog_distance,
            "amount": row.amount
        })
    
    return {
        "name": doc.name,
        "employee": doc.employee,
        "employee_name": doc.employee_name,
        "grand_total": doc.grand_total,
        "workflow_state": doc.workflow_state,
        "expenses": expenses
    }


@frappe.whitelist()
def expense_approve(docs):

    import json
    from frappe.model.workflow import apply_workflow

    if isinstance(docs, str):
        docs = json.loads(docs)

    for name in docs:

        doc = frappe.get_doc(
            "Expense Claim",
            name
        )

        action = None

        if doc.workflow_state == "Pending for HOD":
            action = "Send to Accounts"

        elif doc.workflow_state == "Pending for Accounts":
            action = "Send to CEO"

        elif doc.workflow_state == "Pending for CEO":
            action = "Approve"

        if action:
            apply_workflow(doc, action)

    frappe.db.commit()

    return True

@frappe.whitelist()
def expense_reject(docs):

    import json
    from frappe.model.workflow import apply_workflow

    if isinstance(docs, str):
        docs = json.loads(docs)

    for name in docs:

        doc = frappe.get_doc(
            "Expense Claim",
            name
        )

        apply_workflow(doc, "Reject")

    frappe.db.commit()

    return True



@frappe.whitelist()
def get_att_applications():

    user = frappe.session.user

    if "HOD" not in frappe.get_roles(user):
        return []

    data = frappe.get_all(
        "Attendance Request",
        filters={
            "workflow_state": "Pending for HOD",
            "approver": user
        },
        fields=[
            "name",
            "employee",
            "employee_name",
            "from_date",
            "to_date",
            "total_days",
            "reason",
            "explanation",
            "workflow_state",
            "half_day",
            "half_day_date"
        ],
        order_by="creation desc"
    )

    return data


@frappe.whitelist()
def approve_att(docname):

    doc = frappe.get_doc("Attendance Request", docname)

    doc.workflow_state = "Approved"
    doc.save(ignore_permissions=True)
    doc.submit()

    frappe.db.commit()

    return "Approved"


@frappe.whitelist()
def reject_att(docname):

    doc = frappe.get_doc("Attendance Request", docname)

    doc.workflow_state = "Rejected"
    doc.save(ignore_permissions=True)

    frappe.db.commit()

    return "Rejected"


@frappe.whitelist()
def get_att_details(docname):

    doc = frappe.get_doc("Attendance Request", docname)

    return {
        "name": doc.name,
        "employee": doc.employee,
        "employee_name": doc.employee_name,
        "from_date": doc.from_date,
        "to_date": doc.to_date,
        "explanation": doc.explanation,
        "total_days":doc.total_days,
        "reason": doc.reason,
        "status": doc.workflow_state,
        "half_day": doc.half_day,
        "half_day_date": doc.half_day_date,
        "custom_session":doc.custom_session
    }

@frappe.whitelist()
def bulk_approve_att(docs):

    import json

    if isinstance(docs, str):
        docs = json.loads(docs)

    from frappe.model.workflow import apply_workflow

    for docname in docs:

        doc = frappe.get_doc(
            "Attendance Request",
            docname
        )

        apply_workflow(doc, "Approve")

    frappe.db.commit()

    return True

@frappe.whitelist()
def bulk_reject_att(docs):

    import json

    if isinstance(docs, str):
        docs = json.loads(docs)

    from frappe.model.workflow import apply_workflow

    for docname in docs:

        doc = frappe.get_doc(
            "Attendance Request",
            docname
        )

        apply_workflow(doc, "Reject")

    frappe.db.commit()

    return True




@frappe.whitelist()
def get_pur_applications():

    user = frappe.session.user

    if "Approver" not in frappe.get_roles(user):
        return []

    data = frappe.get_all(
        "Purchase Order",
        filters={
            "workflow_state": "Pending for CEO",
        },
        fields=[
            "name",
            "supplier",
            "purchase_type",
            "transaction_date",
            "schedule_date",
            "payment_type",
            "custom_service",
            "total_qty",
            "workflow_state",
            "total",
            "status"
        ],
        order_by="creation desc"
    )

    return data


from frappe.model.workflow import apply_workflow
import frappe

@frappe.whitelist()
def approve_pur(docname):

    doc = frappe.get_doc("Purchase Order", docname)

    if doc.workflow_state == "Preview":
        apply_workflow(doc, "Send to Submit")

    elif doc.workflow_state == "Pending for CEO":
        apply_workflow(doc, "Approve")

    frappe.db.commit()

    return True



@frappe.whitelist()
def reject_pur(docname):

    doc = frappe.get_doc("Purchase Order", docname)

    if doc.workflow_state == "Pending for CEO":
        apply_workflow(doc, "Revoke")


    frappe.db.commit()

    return True


@frappe.whitelist()
def get_pur_details(docname):
    doc = frappe.get_doc("Purchase Order", docname)

    items = []
    for row in doc.items:
        items.append({
            "item_code": row.item_code,
            "item_name": row.item_name,
            "schedule_date": row.schedule_date,
            "expected_delivery_date": row.expected_delivery_date,
            "qty": row.qty,
            "uom": row.uom,
            "rate": row.rate,
            "amount": row.amount,
            "image_view": row.get("image_view") or row.get("image") or None
        })

    # ✅ Attachments fetch
    attachments = frappe.get_all(
        "File",
        filters={
            "attached_to_doctype": "Purchase Order",
            "attached_to_name": docname
        },
        fields=["file_name", "file_url"]
    )

    return {
        "name": doc.name,
        "supplier": doc.supplier,
        "purchase_type": doc.purchase_type,
        "transaction_date": doc.transaction_date,
        "schedule_date": doc.schedule_date,
        "payment_type": doc.payment_type,
        "custom_service": doc.custom_service,
        "total_qty": doc.total_qty,
        "workflow_state": doc.workflow_state,
        "status": doc.status,
        "total": doc.total,
        "items": items,
        "attachments": attachments  
    }


@frappe.whitelist()
def bulk_approve_pur(docs):

    import json

    if isinstance(docs, str):
        docs = json.loads(docs)

    from frappe.model.workflow import apply_workflow

    for docname in docs:

        doc = frappe.get_doc(
            "Purchase Order",
            docname
        )

        if doc.workflow_state == "Preview":
            apply_workflow(doc, "Send to Submit")

        elif doc.workflow_state == "Pending for CEO":
            apply_workflow(doc, "Approve")

    frappe.db.commit()

    return True

@frappe.whitelist()
def bulk_reject_pur(docs):

    import json

    if isinstance(docs, str):
        docs = json.loads(docs)

    from frappe.model.workflow import apply_workflow

    for docname in docs:

        doc = frappe.get_doc(
            "Purchase Order",
            docname
        )

        if doc.workflow_state == "Pending for CEO":
            apply_workflow(doc, "Revoke")

    frappe.db.commit()

    return True


@frappe.whitelist()
def get_pur_inv_applications():
    user = frappe.session.user
    roles = frappe.get_roles(user)

    if "CEO" not in roles:
        return []

    return frappe.get_all(
        "Purchase Invoice",
        filters={
            "workflow_state": "Pending for CEO"
        },
        fields=[
            "name",
            "supplier",
            "posting_date",
            "posting_time",
            "due_date",
            "services",
            "bill_no",
            "total",
            "workflow_state"
        ],
        order_by="creation desc"
    )


@frappe.whitelist()
def approve_pur_inv(docname):
    doc = frappe.get_doc("Purchase Invoice", docname)
    doc.workflow_state = "Approved"
    doc.save(ignore_permissions=True)
    doc.submit()
    frappe.db.commit()
    return "ok"



@frappe.whitelist()
def get_pur_inv_details(docname):
    doc = frappe.get_doc("Purchase Invoice", docname)

    items = []
    for row in doc.items:
        items.append({
            "item_code": row.item_code,
            "item_name": row.item_name,
            "qty": row.qty,
            "uom": row.uom,
            "rate": row.rate,
            "amount": row.amount
        })

    # ✅ Attachments fetch
    attachments = frappe.get_all(
        "File",
        filters={
            "attached_to_doctype": "Purchase Invoice",
            "attached_to_name": docname
        },
        fields=["file_name", "file_url"]
    )

    return {
        "name": doc.name,
        "supplier": doc.supplier,
        "posting_date": str(doc.posting_date),
        "posting_time": str(doc.posting_time),
        "due_date": str(doc.due_date) if doc.due_date else None,
        "services": doc.services if hasattr(doc, 'services') else None,
        "bill_no": doc.bill_no if hasattr(doc, 'bill_no') else None,
        "total": doc.total,
        "workflow_state": doc.workflow_state,
        "items": items,
        "attachments": attachments
    }


@frappe.whitelist()
def get_sal_inv_applications():
    user = frappe.session.user
    roles = frappe.get_roles(user)

    if "Director" in roles:
        states = ["Reviewed by Accounts"]
    # elif "Sales Manager" in roles:
    #     states = ["Draft by Account user"]
    # elif "Accounts Manager" in roles:
    #     states = ["Draft by Account user", "Draft"]
    else:
        return []

    return frappe.get_all(
        "Sales Invoice",
        filters={
             "workflow_state": ["in", states]
        },
        fields=[
            "name",
            "customer",
            "posting_date",
            "custom_rc_invoice_",
            "pos_profile",
            "services",
            "company",
            "total_qty",
            "total",
            "workflow_state"
        ],
        order_by="creation desc"
    )


@frappe.whitelist()
def approve_sal_inv(docname):
    user = frappe.session.user
    roles = frappe.get_roles(user)

    doc = frappe.get_doc("Sales Invoice", docname)

    if "Director" in roles:
        doc.workflow_state = "Approved"
        doc.save(ignore_permissions=True)
        doc.submit()
    # elif "Sales Manager" in roles:
    #     doc.workflow_state = "Reviewed by Sales Manager"
    #     doc.save(ignore_permissions=True)
    elif "Accounts Manager" in roles:
        doc.workflow_state = "Reviewed by Accounts"
        doc.save(ignore_permissions=True)
    else:
        frappe.throw("Not authorized")

    frappe.db.commit()
    return "ok"


# @frappe.whitelist()
# def reject_sal_inv(docname):
#     user = frappe.session.user
#     roles = frappe.get_roles(user)

#     doc = frappe.get_doc("Sales Invoice", docname)

#     if "Director" in roles:
#         doc.workflow_state = "Rejected by Director"
#     elif "Sales Manager" in roles:
#         doc.workflow_state = "Rejected by Sales Manager"
#     else:
#         frappe.throw("Not authorized")

#     doc.save(ignore_permissions=True)
#     frappe.db.commit()
#     return "ok"



@frappe.whitelist()
def get_sal_inv_details(docname):
    doc = frappe.get_doc("Sales Invoice", docname)

    items = []
    for row in doc.items:
        items.append({
            "item_code": row.item_code,
            "item_name": row.item_name,
            "image_view": row.get("image_view") or row.get("image") or None,
            "qty": row.qty,
            "uom": row.uom,
            "stock_qty": row.stock_qty,
            "rate": row.rate,
            "amount":row.amount,
            "mrp":row.mrp,
            "base_net_amount":row.base_net_amount
        })

    taxes = []
    for row in doc.taxes:
        taxes.append({
            "charge_type": row.charge_type,
            "account_head": row.account_head,
            "description": row.description,
            "rate": row.rate,
            "base_total": row.base_total
        })

    # ✅ Attachments
    attachments = frappe.get_all(
        "File",
        filters={
            "attached_to_doctype": "Sales Invoice",
            "attached_to_name": docname
        },
        fields=["file_name", "file_url"]
    )

    return {
        "name": doc.name,
        "customer": doc.customer,
        "posting_date": str(doc.posting_date),
        "custom_rc_invoice_": doc.custom_rc_invoice_ if hasattr(doc, 'custom_rc_invoice_') else None,
        "pos_profile": doc.pos_profile,
        "services": doc.services if hasattr(doc, 'services') else None,
        "company": doc.company,
        "total_qty": doc.total_qty,
        "total": doc.total,
        "workflow_state": doc.workflow_state,
        "items": items,
        "taxes": taxes,
        "attachments": attachments  
    }




