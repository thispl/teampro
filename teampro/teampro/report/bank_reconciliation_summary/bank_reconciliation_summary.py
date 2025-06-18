import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = []

    bank_account = filters.get("bank_account")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    # Book Balance
    book_balance = get_book_balance(bank_account, to_date)

    # Unreconciled from ERP (uncleared in GL Entry)
    unreconciled_erp = get_unreconciled_erp(bank_account, from_date, to_date)
    unreconciled_erp_total = sum([row["amount"] for row in unreconciled_erp])

    # Unmatched Bank Transactions (not linked to any ERP doc)
    unmatched_bank_txns = get_unmatched_bank_txns(bank_account, from_date, to_date)
    unmatched_bank_total = sum([row["withdrawal"] - row["deposit"] for row in unmatched_bank_txns])

    # Derived Balance
    derived_book_balance = flt(book_balance) + unreconciled_erp_total

    # Bank Balance (from uploaded bank statement)
    bank_balance = get_bank_balance(bank_account, to_date)

    # Reconciliation Difference
    difference = flt(derived_book_balance) - flt(bank_balance)

    data.append(["Balance as per Books", book_balance])
    data.append(["Add: Cheques/Receipts not cleared in ERP", unreconciled_erp_total])
    data.append(["Derived Book Balance", derived_book_balance])
    data.append(["Bank Balance (from uploaded statement)", bank_balance])
    data.append(["Unreconciled Difference", difference])
    data.append(["", ""])  # Blank Line

    data.append(["Unreconciled Transactions in ERP (not cleared)", ""])
    for row in unreconciled_erp:
        data.append([row["voucher_no"], row["posting_date"], row["amount"], "ERP"])

    data.append(["", ""])  # Blank Line

    data.append(["Unmatched Bank Transactions (not linked to ERP)", ""])
    for row in unmatched_bank_txns:
        amount = flt(row["withdrawal"]) - flt(row["deposit"])
        data.append([row["transaction_date"], row["reference_number"], amount, "BANK"])

    return columns, data


def get_book_balance(account, to_date):
    return frappe.db.sql("""
        SELECT SUM(debit - credit) FROM `tabGL Entry`
        WHERE account=%s AND posting_date <= %s
    """, (account, to_date))[0][0] or 0.0


def get_unreconciled_erp(account, from_date, to_date):
    return frappe.db.sql("""
        SELECT voucher_no, posting_date, debit - credit as amount
        FROM `tabGL Entry`
        WHERE account=%s AND posting_date BETWEEN %s AND %s
        AND (clearance_date IS NULL OR clearance_date = '')
    """, (account, from_date, to_date), as_dict=True)


def get_unmatched_bank_txns(account, from_date, to_date):
    return frappe.db.sql("""
        SELECT transaction_date, reference_number, deposit, withdrawal
        FROM `tabBank Transaction`
        WHERE bank_account=%s
        AND transaction_date BETWEEN %s AND %s
        AND NOT EXISTS (
            SELECT name FROM `tabBank Transaction Reconciliation`
            WHERE bank_transaction=`tabBank Transaction`.name
        )
    """, (account, from_date, to_date), as_dict=True)


def get_bank_balance(account, to_date):
    # Get latest uploaded balance till the to_date
    return frappe.db.sql("""
        SELECT SUM(deposit - withdrawal)
        FROM `tabBank Transaction`
        WHERE bank_account=%s AND transaction_date <= %s
    """, (account, to_date))[0][0] or 0.0


def get_columns():
    return [
        {"label": "Description / Date", "fieldname": "desc", "fieldtype": "Data", "width": 250},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 150},
        {"label": "Source", "fieldname": "source", "fieldtype": "Data", "width": 100},
    ]
