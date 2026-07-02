import frappe
from frappe import _
from frappe.utils import flt, today
import hashlib


@frappe.whitelist()
def get_leave_summary():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return []

	from frappe.utils import getdate
	current_year = getdate(today()).year
	year_start = f"{current_year}-01-01"
	year_end = f"{current_year}-12-31"

	# Active allocations only (for available balance)
	active_allocations = frappe.get_all("Leave Allocation",
		filters={
			"employee": employee,
			"docstatus": 1,
			"from_date": ["<=", today()],
			"to_date": [">=", today()]
		},
		fields=["leave_type", "total_leaves_allocated", "from_date", "to_date"]
	)

	COLOR_PALETTE = [
		"#3b82f6",  # blue
		"#f59e0b",  # amber
		"#10b981",  # emerald
		"#ef4444",  # red
		"#8b5cf6",  # violet
		"#06b6d4",  # cyan
		"#f97316",  # orange
		"#84cc16",  # lime
		"#ec4899",  # pink
		"#14b8a6",  # teal
	]

	def get_color(leave_type):
		index = int(hashlib.md5(leave_type.encode()).hexdigest(), 16) % len(COLOR_PALETTE)
		return COLOR_PALETTE[index]

	def get_all_time_booked(leave_type):
		result = frappe.db.sql("""
			SELECT SUM(leaves)
			FROM `tabLeave Ledger Entry`
			WHERE employee = %s
			  AND leave_type = %s
			  AND docstatus = 1
			  AND leaves < 0
		""", (employee, leave_type))
		return abs(flt(result[0][0])) if result and result[0][0] else 0

	def get_active_consumed(leave_type, from_date, to_date):
		result = frappe.db.sql("""
			SELECT SUM(leaves)
			FROM `tabLeave Ledger Entry`
			WHERE employee = %s
			  AND leave_type = %s
			  AND docstatus = 1
			  AND leaves < 0
			  AND from_date >= %s
			  AND from_date <= %s
		""", (employee, leave_type, from_date, to_date))
		return abs(flt(result[0][0])) if result and result[0][0] else 0

	summary = []
	allocated_types = set()

	for alloc in active_allocations:
		allocated_types.add(alloc.leave_type)

		booked = get_all_time_booked(alloc.leave_type)
		active_consumed = get_active_consumed(alloc.leave_type, alloc.from_date, alloc.to_date)
		allocated = flt(alloc.total_leaves_allocated)
		available = max(0, allocated - active_consumed)  

		policy = frappe.db.get_value(
			"Leave Type", alloc.leave_type, "custom_policy_details"
		) or _("No specific policy details provided.")

		summary.append({
			"leave_type": alloc.leave_type,
			"available": available,
			"booked": booked,
			"color": get_color(alloc.leave_type),
			"policy_details": policy
		})

	
	unallocated_result = frappe.db.sql("""
		SELECT leave_type, SUM(leaves)
		FROM `tabLeave Ledger Entry`
		WHERE employee = %s
		  AND docstatus = 1
		  AND leaves < 0
		  AND transaction_type = 'Leave Application'
		GROUP BY leave_type
	""", (employee,))

	for row in unallocated_result:
		lt, consumed = row
		if lt not in allocated_types:
			policy = frappe.db.get_value(
				"Leave Type", lt, "custom_policy_details"
			) or _("No specific policy details provided.")

			summary.append({
				"leave_type": lt,
				"available": 0,
				"booked": abs(flt(consumed)),
				"color": get_color(lt),
				"policy_details": policy
			})

	return summary


@frappe.whitelist()
def get_leave_calendar():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return []

	leaves = frappe.get_all("Leave Application",
		filters={
			"employee": employee,
			"docstatus": ["not in", [2]],
			"status": ["in", ["Approved", "Open"]]
		},
		fields=["leave_type", "from_date", "to_date", "status", "total_leave_days"]
	)

	return [
		{
			"leave_type": l.leave_type,
			"from_date": str(l.from_date),
			"to_date": str(l.to_date),
			"status": l.status,
			"days": l.total_leave_days
		}
		for l in leaves
	]


@frappe.whitelist()
def get_all_holidays():
	"""All holidays for the year — used to overlay on the calendar."""
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, ["holiday_list", "company"], as_dict=True)
	if not employee:
		return []

	holiday_list = employee.get("holiday_list")
	if not holiday_list:
		holiday_list = frappe.db.get_value("Company", employee.get("company"), "default_holiday_list")
	if not holiday_list:
		return []

	
	import datetime
	year = datetime.date.today().year

	holidays = frappe.get_all("Holiday",
		filters={
			"parent": holiday_list,
			"holiday_date": ["between", [f"{year}-01-01", f"{year}-12-31"]]
		},
		fields=["holiday_date", "description"],
		order_by="holiday_date asc",
	)

	return [{"date": str(h.holiday_date), "description": h.description} for h in holidays]


@frappe.whitelist()
def get_upcoming_holidays():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, ["holiday_list", "company"], as_dict=True)
	if not employee:
		return []

	
	holiday_list = employee.get("holiday_list")
	if not holiday_list:
		holiday_list = frappe.db.get_value("Company", employee.get("company"), "default_holiday_list")
	if not holiday_list:
		return []

	holidays = frappe.get_all("Holiday",
		filters={
			"parent": holiday_list,
			"holiday_date": [">=", today()]
		},
		fields=["holiday_date", "description"],
		order_by="holiday_date asc",
		
	)

	return [{"date": str(h.holiday_date), "description": h.description} for h in holidays]


@frappe.whitelist()
def get_absent_count():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return 0

	import datetime
	year = datetime.date.today().year

	count = frappe.db.count("Attendance", filters={
		"employee": employee,
		"status": "Absent",
		"docstatus": "!=2",
		"attendance_date": ["between", [f"{year}-01-01", f"{year}-12-31"]]
	})

	return count or 0



@frappe.whitelist()
def get_job_openings():
	openings = frappe.get_all("Job Opening",
		filters={"status": ["in", ["Open", "On Hold"]]},
		fields=["name", "job_title", "department", "company", "status", "posted_on","route","publish"],
		order_by="posted_on desc"
	)

	result = []
	for job in openings:
		count = frappe.db.count("Job Applicant", {"job_title": job.name})
		result.append({
			"name": job.name,
			"job_title": job.job_title,
			"department": job.department,
			"company": job.company,
			"status": job.status,
			"posted_on": frappe.format(job.posted_on, {"fieldtype": "Date"}) if job.posted_on else "",
			"applicant_count": count,
			"route": job.route,
			"publish": job.publish
		})

	return result



@frappe.whitelist()
def get_appraisal_data():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return {"goals": [], "appraisals": [], "overall_rating": None}

	appraisals = frappe.get_all("Appraisal",
		filters={"employee": employee, "docstatus": 1},
		fields=["name", "final_score", "total_score", "appraisal_cycle", "start_date", "end_date"],
		order_by="modified desc",
		limit=5
	)

	goals = []
	overall_rating = None

	if appraisals:
		latest = appraisals[0]
		overall_rating = flt(latest.get("final_score") or latest.get("total_score") or 0)

		appraisal_doc = frappe.get_doc("Appraisal", latest.name)
		for goal in (appraisal_doc.goals or []):
			goals.append({
				"kra": goal.kra,
				"score": flt(goal.score),
				"weightage": flt(goal.per_weightage),
				"score_earned": flt(goal.score_earned)
			})

	return {
		"goals": goals,
		"appraisals": [
			{
				"name": a.name,
				"overall_score": flt(a.get("final_score") or a.get("total_score") or 0),
				"appraisal_cycle": a.get("appraisal_cycle") or "",
				"period": f"{frappe.format(a.start_date, {'fieldtype': 'Date'})} → {frappe.format(a.end_date, {'fieldtype': 'Date'})}" if a.start_date else ""
			}
			for a in appraisals
		],
		"overall_rating": overall_rating
	}


@frappe.whitelist()
def get_payroll_data():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return {}

	import datetime
	year = datetime.date.today().year

	# Last 6 submitted salary slips
	slips = frappe.get_all("Salary Slip",
		filters={
			"employee": employee,
			"docstatus": ["!=", 2]
		},
		fields=[
			"name", "start_date", "end_date", "posting_date",
			"gross_pay", "total_deduction", "net_pay", "rounded_total",
			"payment_days", "total_working_days",
			"year_to_date", "gross_year_to_date",
			"currency", "total_in_words"
		],
		order_by="end_date desc",
		limit=6
	)

	if not slips:
		return {"slips": [], "current": None, "ytd": {}}

	current = slips[0]

	# Fetch earnings and deductions for the latest slip
	slip_doc = frappe.get_doc("Salary Slip", current.name)

	earnings = [
		{"component": e.salary_component, "amount": flt(e.amount)}
		for e in slip_doc.earnings
		if not e.statistical_component and not e.do_not_include_in_total
	]
	deductions = [
		{"component": d.salary_component, "amount": flt(d.amount)}
		for d in slip_doc.deductions
		if not d.statistical_component and not d.do_not_include_in_total
	]

	return {
		"current": {
			"name": current.name,
			"start_date": str(current.start_date),
			"end_date": str(current.end_date),
			"gross_pay": flt(current.gross_pay),
			"total_deduction": flt(current.total_deduction),
			"net_pay": flt(current.net_pay),
			"payment_days": flt(current.payment_days),
			"total_working_days": flt(current.total_working_days),
			"currency": current.currency or "INR",
			"total_in_words": current.total_in_words or "",
			"earnings": earnings,
			"deductions": deductions,
		},
		"ytd": {
			"net": flt(current.year_to_date),
			"gross": flt(current.gross_year_to_date),
		},
		"slips": [
			{
				"name": s.name,
				"start_date": str(s.start_date),
				"end_date": str(s.end_date),
				"net_pay": flt(s.net_pay),
				"gross_pay": flt(s.gross_pay),
				"total_deduction": flt(s.total_deduction),
				"currency": s.currency or "INR",
			}
			for s in slips
		]
	}


@frappe.whitelist()
def get_employee_documents():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return []

	
	files = frappe.get_all("File",
		filters={
			"attached_to_doctype": "Employee",
			"attached_to_name": employee
		},
		fields=["name", "file_name", "file_url", "file_size",
				"file_type", "creation", "is_private"],
		order_by="creation desc"
	)

	def fmt_size(size):
		if not size:
			return ""
		size = int(size)
		if size < 1024:
			return f"{size} B"
		elif size < 1024 * 1024:
			return f"{size // 1024} KB"
		return f"{size // (1024*1024)} MB"

	return [
		{
			"name": f.name,
			"file_name": f.file_name or "Unnamed",
			"file_url": f.file_url,
			"file_size": fmt_size(f.file_size),
			"file_type": (f.file_type or "").upper(),
			"uploaded_on": frappe.format(f.creation, {"fieldtype": "Date"}),
			"is_private": f.is_private
		}
		for f in files
	]


@frappe.whitelist(allow_guest=True)
def get_pending_leave_requests():
	user = frappe.session.user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return []

	leaves = frappe.get_all("Leave Application",
		filters={
			"employee": employee,
			"workflow_state": ["not in", ["Approved", "Rejected", "Cancelled"]]
		},
		fields=["name", "leave_type", "from_date", "to_date", "status", "total_leave_days", "workflow_state"]
	)

	return [
		{
			"name": l.name,
			"leave_type": l.leave_type,
			"from_date": str(l.from_date),
			"to_date": str(l.to_date),
			"status": l.status,
			"days": l.total_leave_days,
			"workflow_state": l.workflow_state
		}
		for l in leaves
	]




@frappe.whitelist(allow_guest=True)
def get_permission_data():
	try:
		employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
		if not employee:
			return []

		permissions = frappe.get_list(
			"Attendance Permission",
			filters={
				"employee": employee,
				"docstatus": 1,
				"permission_date": ["between", [
					frappe.utils.get_first_day(frappe.utils.nowdate()),
					frappe.utils.get_last_day(frappe.utils.nowdate())
				]]
			},
			fields=["total_time"],
			ignore_permissions=True   
		)
		return permissions
	except Exception:
		return []


@frappe.whitelist()
def get_approval_data():
	try:
		expense = frappe.get_list("Expense Claim",
			filters={"expense_approver": frappe.session.user, "approval_status": "Draft"},
			fields=["name", "employee_name", "total_claimed_amount", "posting_date"],
			ignore_permissions=True
		)
		leave = frappe.get_list("Leave Application",
			filters={"leave_approver": frappe.session.user, "status": "Open"},
			fields=["name", "employee_name", "leave_type", "total_leave_days"],
			ignore_permissions=True
		)
		shift = frappe.get_list("Shift Request",
			filters={"approver": frappe.session.user, "status": "Draft"},
			fields=["name", "employee_name", "shift_type", "from_date"],
			ignore_permissions=True
		)
		return {"expense": expense, "leave": leave, "shift": shift}
	except Exception:
		return {"expense": [], "leave": [], "shift": []}