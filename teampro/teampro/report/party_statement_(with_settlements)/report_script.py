# Party Statement (with Settlements) - report script
# Restricted exec: no imports, no underscore-prefixed names/attributes

flt = frappe.utils.flt
getdate = frappe.utils.getdate
cstr = frappe.utils.cstr

if not isinstance(filters, dict):
	filters = dict(filters or {})

# Validate
if not filters.get("company"):
	frappe.throw("Company is required")
if not filters.get("party_type"):
	frappe.throw("Party Type is required")
if not filters.get("party"):
	frappe.throw("Party is required")

# Columns
columns = [
	{"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 90},
	{"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 110},
	{"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 140},
	{"label": "Supplier Invoice No", "fieldname": "bill_no", "fieldtype": "Data", "width": 120},
	{"label": "Remarks", "fieldname": "remarks", "fieldtype": "Text", "width": 200},
	{"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 110},
	{"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 110},
	{"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 120},
	{"label": "Settled Against", "fieldname": "settled_against", "fieldtype": "Text", "width": 200},
]

company = filters.get("company")
party_type = filters.get("party_type")
party = filters.get("party")
from_date = filters.get("from_date") or None
to_date = filters.get("to_date") or getdate()

# Resolve party account from Party Account child table
party_account = frappe.db.get_value(
	"Party Account",
	{"parent": party, "parenttype": party_type, "company": company},
	"account"
)
if not party_account:
	party_account = frappe.db.get_value(
		"GL Entry",
		{"party_type": party_type, "party": party, "company": company, "is_cancelled": 0},
		"account"
	)
if not party_account:
	if party_type == "Customer":
		party_account = frappe.db.get_value("Company", company, "default_receivable_account")
	elif party_type == "Supplier":
		party_account = frappe.db.get_value("Company", company, "default_payable_account")

if not party_account:
	data = []
else:
	# Opening balance
	opening = flt(frappe.db.sql("""
		SELECT SUM(debit - credit)
		FROM `tabGL Entry`
		WHERE company = %s AND account = %s AND party = %s
		  AND is_cancelled = 0 AND posting_date < %s
	""", (company, party_account, party, from_date or getdate()))[0][0])

	# GL entries grouped by voucher
	conditions = "company = %s AND account = %s AND party = %s AND is_cancelled = 0"
	params = [company, party_account, party]
	if from_date:
		conditions += " AND posting_date >= %s"
		params.append(from_date)
	conditions += " AND posting_date <= %s"
	params.append(to_date)

	rows = frappe.db.sql("""
		SELECT
			posting_date,
			voucher_type,
			voucher_no,
			MAX(remarks) AS remarks,
			SUM(debit) AS debit,
			SUM(credit) AS credit,
			GROUP_CONCAT(DISTINCT against_voucher) AS against_vouchers
		FROM `tabGL Entry`
		WHERE """ + conditions + """
		GROUP BY voucher_type, voucher_no, posting_date
		ORDER BY posting_date, voucher_no
	""", params, as_dict=True)

	# Batch fetch Payment Entry references
	pe_names = [r.voucher_no for r in rows if r.voucher_type == "Payment Entry"]
	pe_refs = {}
	if pe_names:
		refs = frappe.db.get_all(
			"Payment Entry Reference",
			filters={"parent": ["in", pe_names], "parenttype": "Payment Entry"},
			fields=["parent", "reference_doctype", "reference_name", "allocated_amount", "total_amount", "outstanding_amount", "due_date", "bill_no"],
			order_by="parent, idx",
		)
		for ref in refs:
			pe_refs.setdefault(ref.parent, []).append(ref)

	data = []

	# Opening balance row
	if opening != 0 or from_date:
		data.append({
			"posting_date": from_date or "",
			"voucher_type": "",
			"voucher_no": "",
			"bill_no": "",
			"remarks": "Opening Balance",
			"debit": opening if opening > 0 else 0,
			"credit": abs(opening) if opening < 0 else 0,
			"balance": opening,
			"settled_against": "",
			"is_opening": 1,
		})

	running = opening
	total_debit = 0
	total_credit = 0
	for r in rows:
		debit = flt(r.debit)
		credit = flt(r.credit)
		running += debit - credit
		total_debit += debit
		total_credit += credit

		settled_str = ""
		settlements = []
		if r.voucher_type == "Payment Entry" and r.voucher_no in pe_refs:
			parts = []
			for ref in pe_refs[r.voucher_no]:
				label = ref.reference_name or ""
				if ref.bill_no:
					label = ref.bill_no + " (" + ref.reference_name + ")"
				amt = flt(ref.allocated_amount)
				parts.append(label + " [" + str(amt) + "]")
				settlements.append({
					"reference_doctype": ref.reference_doctype,
					"reference_name": ref.reference_name,
					"bill_no": ref.bill_no or "",
					"allocated_amount": flt(ref.allocated_amount),
					"total_amount": flt(ref.total_amount),
					"outstanding_amount": flt(ref.outstanding_amount),
					"due_date": cstr(ref.due_date) if ref.due_date else "",
				})
			settled_str = ", ".join(parts)

		data.append({
			"posting_date": r.posting_date,
			"voucher_type": r.voucher_type,
			"voucher_no": r.voucher_no,
			"bill_no": "",
			"remarks": r.remarks or "",
			"debit": debit,
			"credit": credit,
			"balance": running,
			"settled_against": settled_str,
			"settlements": settlements,
			"against_vouchers": r.against_vouchers or "",
		})

	# Summary / total row
	closing_balance = running
	data.append({
		"posting_date": to_date,
		"voucher_type": "",
		"voucher_no": "",
		"bill_no": "",
		"remarks": "TOTAL",
		"debit": total_debit,
		"credit": total_credit,
		"balance": closing_balance,
		"settled_against": "",
		"is_total": 1,
	})

	# Summary block (for print template) - passed as message
	summary = {
		"opening_balance": opening,
		"total_debit": total_debit,
		"total_credit": total_credit,
		"closing_balance": closing_balance,
		"party": party,
		"party_type": party_type,
		"party_account": party_account,
		"company": company,
		"from_date": from_date or "",
		"to_date": to_date,
	}

	# generate_report_result unpacks: columns, result, message, chart, report_summary, skip_total_row
	# We pass summary as message (index 2) and skip_total_row=1 (index 5) since we add our own total row
	data = [columns, data, summary, None, None, 1]
