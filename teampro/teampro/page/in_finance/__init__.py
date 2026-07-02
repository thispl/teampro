import frappe
from frappe import _

@frappe.whitelist()
def get_performance_summary_data(from_date=None, to_date=None, company=None):
	"""
	Fetch monthly data for Turnover, Order Booking, and Payables.

	Date filter logic:
	- If no filters: current financial year
	- If only From Date: from selected date to current date
	- If only To Date: from start of current financial year to selected date
	- If both: selected date range
	"""

	# Determine date range based on filters
	today = frappe.utils.today()

	if not from_date and not to_date:
		# Current financial year
		fiscal_year = frappe.db.get_value("Fiscal Year",
			filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
			as_dict=True
		)
		if fiscal_year:
			from_date = fiscal_year["year_start_date"]
			to_date = fiscal_year["year_end_date"]
		else:
			# Fallback to current year
			from_date = frappe.datetime.year_start()
			to_date = frappe.datetime.year_end()
	elif from_date and not to_date:
		# From selected date to current date
		to_date = today
	elif not from_date and to_date:
		# From start of current financial year to selected date
		fiscal_year = frappe.db.get_value("Fiscal Year",
			filters={"year_start_date": ["<=", today], "year_end_date": [">=", today]},
			as_dict=True
		)
		if fiscal_year:
			from_date = fiscal_year["year_start_date"]
		else:
			from_date = frappe.datetime.year_start()

	# Fetch monthly Turnover (Sales Invoice)
	turnover_query = """
		SELECT
			DATE_TRUNC('month', posting_date) as month,
			SUM(base_net_total) as total
		FROM `tabSales Invoice`
		WHERE docstatus = 1
			AND status NOT IN ('Return', 'Credit Note Issued', 'Cancelled')
			AND posting_date >= %s
			AND posting_date <= %s
			{company_condition}
		GROUP BY DATE_TRUNC('month', posting_date)
		ORDER BY month
	"""

	company_condition = ""
	params = [from_date, to_date]
	if company:
		company_condition = "AND company = %s"
		params.append(company)

	turnover_data = frappe.db.sql(turnover_query.format(company_condition=company_condition), params, as_dict=True)

	# Fetch monthly Order Booking (Sales Order)
	order_booking_query = """
		SELECT
			DATE_TRUNC('month', transaction_date) as month,
			SUM(base_net_total) as total
		FROM `tabSales Order`
		WHERE docstatus = 1
			AND status NOT IN ('On Hold', 'Cancelled', 'Closed', 'Completed')
			AND transaction_date >= %s
			AND transaction_date <= %s
			{company_condition}
		GROUP BY DATE_TRUNC('month', transaction_date)
		ORDER BY month
	"""

	params_ob = [from_date, to_date]
	if company:
		params_ob.append(company)

	order_booking_data = frappe.db.sql(order_booking_query.format(company_condition=company_condition), params_ob, as_dict=True)

	# Fetch monthly Payables (Purchase Invoice outstanding)
	payables_query = """
		SELECT
			DATE_TRUNC('month', posting_date) as month,
			SUM(outstanding_amount) as total
		FROM `tabPurchase Invoice`
		WHERE docstatus = 1
			AND status NOT IN ('Return', 'Debit Note Issued', 'Paid', 'Cancelled')
			AND posting_date >= %s
			AND posting_date <= %s
			{company_condition}
		GROUP BY DATE_TRUNC('month', posting_date)
		ORDER BY month
	"""

	params_pi = [from_date, to_date]
	if company:
		params_pi.append(company)

	payables_data = frappe.db.sql(payables_query.format(company_condition=company_condition), params_pi, as_dict=True)

	# Format month to YYYY-MM format for consistency
	def format_month(date_obj):
		if date_obj:
			return date_obj.strftime('%Y-%m')
		return None

	for row in turnover_data:
		row.month = format_month(row.month)
	for row in order_booking_data:
		row.month = format_month(row.month)
	for row in payables_data:
		row.month = format_month(row.month)

	return {
		'turnover': turnover_data,
		'order_booking': order_booking_data,
		'payables': payables_data,
		'from_date': from_date,
		'to_date': to_date
	}
