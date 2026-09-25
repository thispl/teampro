# Copyright (c) 2026, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, cstr


def execute(filters=None):
	filters = frappe._dict(filters or {})
	validate(filters)
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def validate(filters):
	if not filters.company:
		frappe.throw(_("Company is required"))
	if not filters.party_type:
		frappe.throw(_("Party Type is required"))
	if not filters.party:
		frappe.throw(_("Party is required"))


def get_columns():
	return [
		{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 90},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "fieldtype": "Data", "width": 110},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 140,
		},
		{"label": _("Supplier Invoice No"), "fieldname": "bill_no", "fieldtype": "Data", "width": 120},
		{"label": _("Remarks"), "fieldname": "remarks", "fieldtype": "Text", "width": 200},
		{"label": _("Debit"), "fieldname": "debit", "fieldtype": "Currency", "width": 110},
		{"label": _("Credit"), "fieldname": "credit", "fieldtype": "Currency", "width": 110},
		{"label": _("Balance"), "fieldname": "balance", "fieldtype": "Currency", "width": 120},
		{"label": _("Settled Against"), "fieldname": "settled_against", "fieldtype": "Text", "width": 200},
	]


def get_data(filters):
	company = filters.company
	party_type = filters.party_type
	party = filters.party
	from_date = filters.from_date or None
	to_date = filters.to_date or getdate()

	# Resolve the party's receivable/payable account
	party_account = get_party_account(company, party_type, party)
	if not party_account:
		return []

	# Opening balance as of from_date
	opening = 0.0
	if from_date:
		opening = flt(
			frappe.db.sql(
				"""
				SELECT SUM(debit - credit)
				FROM `tabGL Entry`
				WHERE company = %s AND account = %s AND party = %s
				  AND is_cancelled = 0 AND posting_date < %s
				""",
				(company, party_account, party, from_date),
			)[0][0]
		)
	else:
		opening = flt(
			frappe.db.sql(
				"""
				SELECT SUM(debit - credit)
				FROM `tabGL Entry`
				WHERE company = %s AND account = %s AND party = %s
				  AND is_cancelled = 0 AND posting_date < %s
				""",
				(company, party_account, party, getdate()),
			)[0][0]
		)

	# Fetch GL entries on the party account, grouped by voucher
	conditions = "company = %s AND account = %s AND party = %s AND is_cancelled = 0"
	params = [company, party_account, party]
	if from_date:
		conditions += " AND posting_date >= %s"
		params.append(from_date)
	conditions += " AND posting_date <= %s"
	params.append(to_date)

	rows = frappe.db.sql(
		f"""
		SELECT
			posting_date,
			voucher_type,
			voucher_no,
			MAX(bill_no) AS bill_no,
			MAX(remarks) AS remarks,
			SUM(debit) AS debit,
			SUM(credit) AS credit,
			GROUP_CONCAT(DISTINCT against_voucher) AS against_vouchers
		FROM `tabGL Entry`
		WHERE {conditions}
		GROUP BY voucher_type, voucher_no, posting_date
		ORDER BY posting_date, voucher_no
		""",
		params,
		as_dict=True,
	)

	# Collect all Payment Entry voucher numbers for batch reference fetch
	pe_names = [r.voucher_no for r in rows if r.voucher_type == "Payment Entry"]
	pe_refs = {}
	if pe_names:
		refs = frappe.db.get_all(
			"Payment Entry Reference",
			filters={"parent": ["in", pe_names], "parenttype": "Payment Entry"},
			fields=[
				"parent",
				"reference_doctype",
				"reference_name",
				"allocated_amount",
				"total_amount",
				"outstanding_amount",
				"due_date",
				"bill_no",
			],
			order_by="parent, idx",
		)
		for ref in refs:
			pe_refs.setdefault(ref.parent, []).append(ref)

	data = []

	# Opening balance row
	if opening != 0 or from_date:
		data.append(
			{
				"posting_date": from_date or "",
				"voucher_type": "",
				"voucher_no": "",
				"bill_no": "",
				"remarks": _("Opening Balance"),
				"debit": opening if opening > 0 else 0,
				"credit": abs(opening) if opening < 0 else 0,
				"balance": opening,
				"settled_against": "",
				"is_opening": 1,
			}
		)

	running = opening
	for r in rows:
		debit = flt(r.debit)
		credit = flt(r.credit)
		running += debit - credit

		settled_str = ""
		settlements = []
		if r.voucher_type == "Payment Entry" and r.voucher_no in pe_refs:
			parts = []
			for ref in pe_refs[r.voucher_no]:
				label = ref.reference_name or ""
				if ref.bill_no:
					label = f"{ref.bill_no} ({ref.reference_name})"
				parts.append(f"{label} [{fmt_money(ref.allocated_amount)}]")
				settlements.append(
					{
						"reference_doctype": ref.reference_doctype,
						"reference_name": ref.reference_name,
						"bill_no": ref.bill_no or "",
						"allocated_amount": flt(ref.allocated_amount),
						"total_amount": flt(ref.total_amount),
						"outstanding_amount": flt(ref.outstanding_amount),
						"due_date": cstr(ref.due_date) if ref.due_date else "",
					}
				)
			settled_str = ", ".join(parts)

		data.append(
			{
				"posting_date": r.posting_date,
				"voucher_type": r.voucher_type,
				"voucher_no": r.voucher_no,
				"bill_no": r.bill_no or "",
				"remarks": r.remarks or "",
				"debit": debit,
				"credit": credit,
				"balance": running,
				"settled_against": settled_str,
				"settlements": settlements,
				"against_vouchers": r.against_vouchers or "",
			}
		)

	return data


def get_party_account(company, party_type, party):
	"""Return the default receivable/payable account for the party."""
	account_field = "receivable_account" if party_type == "Customer" else "payable_account"
	if party_type == "Customer":
		acc = frappe.db.get_value("Customer", party, account_field)
	elif party_type == "Supplier":
		acc = frappe.db.get_value("Supplier", party, account_field)
	else:
		# Fallback: find the party's GL entries' account
		acc = frappe.db.get_value(
			"GL Entry",
			{"party_type": party_type, "party": party, "company": company, "is_cancelled": 0},
			"account",
		)
	if not acc:
		# Fallback: find from default account in company
		if party_type == "Customer":
			acc = frappe.get_cached_value("Company", company, "default_receivable_account")
		elif party_type == "Supplier":
			acc = frappe.get_cached_value("Company", company, "default_payable_account")
	return acc


def fmt_money(val):
	val = flt(val)
	return f"{val:,.2f}"
