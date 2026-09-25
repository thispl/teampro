# -*- coding: utf-8 -*-
"""
Payroll Workbench API controller for the teampro app.

Coordinates Attendance, Salary Slips, Journal Entries, and bank payouts
(via the india_banking app) without modifying any core doctypes.
"""

import json
from datetime import date, timedelta

import frappe
from frappe import _
from frappe.utils import (
	add_days,
	cint,
	flt,
	get_first_day,
	get_last_day,
	getdate,
	nowdate,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _daterange(start_date, end_date):
	"""Yield each date (datetime.date) from start_date to end_date inclusive."""
	start = getdate(start_date)
	end = getdate(end_date)
	current = start
	while current <= end:
		yield current
		current += timedelta(days=1)


def _get_company_currency(company):
	return frappe.get_cached_value("Company", company, "default_currency") or "INR"


def _get_payroll_payable_account(company, payroll_entry=None):
	"""Return the payroll payable account for the company / payroll entry."""
	if payroll_entry:
		acc = frappe.db.get_value("Payroll Entry", payroll_entry, "payroll_payable_account")
		if acc:
			return acc
	acc = frappe.db.get_value("Company", company, "default_payroll_payable_account")
	if not acc:
		frappe.throw(
			_("Please set a Default Payroll Payable Account in Company {0}").format(
				frappe.bold(company)
			)
		)
	return acc


def _get_company_cost_center(company):
	"""Return the default cost center for the company."""
	cc = frappe.db.get_value("Company", company, "cost_center")
	if not cc:
		frappe.throw(_("Please set a default Cost Center in Company {0}").format(frappe.bold(company)))
	return cc


def _get_employee_bank_account(employee):
	"""Return the default Bank Account name linked to an employee, if any."""
	return frappe.db.get_value(
		"Bank Account",
		{"party_type": "Employee", "party": employee, "is_default": 1},
		"name",
	) or frappe.db.get_value(
		"Bank Account",
		{"party_type": "Employee", "party": employee},
		"name",
		order_by="modified desc",
	)


def _india_banking_installed():
	return "india_banking" in frappe.get_installed_apps()


def _estimate_late_penalty_days(late_count, offsets=0):
	"""Estimate deduction days from a raw late count and approved offsets.

	Mirrors the slab logic in utility.py:
	  - first 3 late days are allowed
	  - offsets (approved First-Half Permission / On-Duty / Leave entries)
	    further reduce the count
	  - penalty days start once actual late days reach 3.
	"""
	actual_late = max(0, late_count - 3 - offsets)
	if actual_late < 3:
		return 0
	if actual_late <= 5:
		return 0.5
	if actual_late <= 8:
		return 1
	if actual_late <= 11:
		return 1.5
	if actual_late <= 14:
		return 2
	if actual_late <= 17:
		return 2.5
	if actual_late <= 20:
		return 3
	if actual_late <= 23:
		return 3.5
	if actual_late <= 26:
		return 4
	if actual_late <= 29:
		return 4.5
	return 5


# ---------------------------------------------------------------------------
# Step 1 & 2: Attendance Summary & Reactive Grid
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_employees(filters):
	"""Return active employees matching the given filter dict.

	filters keys: company, branch, department, designation, grade,
	              from_date, to_date

	Includes employees who were active during the payroll period, even if
	their status has since changed to 'Notice' or 'Left'. An employee is
	included if:
	  - status = 'Active', OR
	  - status IN ('Notice', 'Left') AND date_of_joining <= to_date
	    AND (relieving_date IS NULL OR relieving_date >= from_date)
	"""
	if isinstance(filters, str):
		filters = json.loads(filters) if filters.strip() else {}
	filters = frappe._dict(filters or {})

	# Build condition: include Active employees, plus Notice/Left employees
	# who were employed during the payroll period.
	# Uses resignation_letter_date (primary) falling back to relieving_date
	# to determine if the employee was still employed during the payroll period:
	#   - COALESCE(resignation_letter_date, relieving_date) >= from_date → include
	#   - COALESCE(resignation_letter_date, relieving_date) < from_date → exclude
	#   - Both dates NULL → exclude (can't confirm employment during period)
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	if from_date and to_date:
		status_condition = (
			"(e.status = 'Active' "
			"    AND e.date_of_joining <= %(to_date)s "
			"OR (e.status IN ('Notice', 'Left')"
			"    AND e.date_of_joining <= %(to_date)s "
			"    AND COALESCE(e.resignation_letter_date, e.relieving_date) IS NOT NULL "
			"    AND COALESCE(e.resignation_letter_date, e.relieving_date) >= %(from_date)s))"
		)
		params = {"from_date": from_date, "to_date": to_date}
	else:
		status_condition = "e.status = 'Active'"
		params = {}

	conditions = [status_condition]

	if filters.company:
		conditions.append("e.company = %(company)s")
		params["company"] = filters.company
	if filters.branch:
		conditions.append("e.branch = %(branch)s")
		params["branch"] = filters.branch
	if filters.department:
		conditions.append("e.department = %(department)s")
		params["department"] = filters.department
	if filters.designation:
		conditions.append("e.designation = %(designation)s")
		params["designation"] = filters.designation
	if filters.grade:
		conditions.append("e.grade = %(grade)s")
		params["grade"] = filters.grade

	employees = frappe.db.sql(
		f"""
		SELECT e.name, e.employee_name, e.employee_number,
		       e.department, e.designation, e.branch, e.grade,
		       e.company, e.bank_ac_no, e.ifsc_code,
		       e.date_of_joining, e.holiday_list, e.status,
		       e.resignation_letter_date
		FROM `tabEmployee` e
		WHERE {' AND '.join(conditions)}
		ORDER BY e.department, e.employee_name
		""",
		params,
		as_dict=True,
	)
	return employees


@frappe.whitelist()
def get_attendance_matrix(employees, from_date, to_date):
	"""Return an attendance matrix {employee: {date_str: {name, status, half_day}}}
	plus summary counts."""
	if isinstance(employees, str):
		employees = json.loads(employees)
	if not employees or not from_date or not to_date:
		return {"matrix": {}, "summary": {}, "days": []}

	records = frappe.db.sql(
		"""
		SELECT name, employee, attendance_date, status,
		       half_day_status, shift, in_time, out_time, late_entry,
		       early_exit, leave_type, leave_application, docstatus
		FROM `tabAttendance`
		WHERE employee IN %(employees)s
		  AND attendance_date BETWEEN %(from_date)s AND %(to_date)s
		  AND docstatus != 2
		ORDER BY attendance_date
		""",
		{
			"employees": tuple(employees),
			"from_date": from_date,
			"to_date": to_date,
		},
		as_dict=True,
	)

	matrix = {emp: {} for emp in employees}
	summary = {"Present": 0, "Absent": 0, "Half Day": 0, "On Leave": 0, "Work From Home": 0, "Unmarked": 0}

	for r in records:
		date_str = str(r.attendance_date)
		matrix.setdefault(r.employee, {})[date_str] = {
			"name": r.name,
			"status": r.status,
			"half_day": bool(r.half_day_status),
			"half_day_status": r.half_day_status,
			"shift": r.shift,
			"in_time": str(r.in_time) if r.in_time else "",
			"out_time": str(r.out_time) if r.out_time else "",
			"late_entry": r.late_entry,
			"early_exit": r.early_exit,
			"leave_type": r.leave_type or "",
			"leave_application": r.leave_application or "",
			"docstatus": r.docstatus,
		}
		if r.status in summary:
			summary[r.status] += 1

	# Count unmarked days
	days = list(_daterange(from_date, to_date))
	total_cells = len(employees) * len(days)
	marked = sum(1 for emp_data in matrix.values() for v in emp_data.values())
	summary["Unmarked"] = max(0, total_cells - marked)

	return {
		"matrix": matrix,
		"summary": summary,
		"days": [str(d) for d in days],
	}


@frappe.whitelist()
def get_attendance_summary(employees, from_date, to_date, company=None):
	"""Return per-employee attendance summary for the Summary View.

	For each employee returns:
	  - calendar_days: total days in the date range
	  - holidays: days that fall on a Holiday (from the employee's Holiday List)
	  - present: Present + Work From Home days (full) + Half Day (0.5)
	  - paid_leave: On Leave days where the leave type is NOT leave-without-pay
	  - absent_unpaid: Absent days + On Leave days where the leave type IS LWP
	  - payment_days: present + paid_leave + holidays - late_penalty_days (capped at calendar_days, min 0)
	  - late_count: days where in_time is later than the cutoff (09:30, 09:45 for HOD)
	  - late_penalty_days: deduction_days from the Late Penalty record, or estimated from late_count
	    minus approved First-Half Permission / On-Duty / Leave offsets
	  - unapproved_leaves: count of Leave Applications in Draft for this employee in the period
	  - unapproved_attendance_requests: count of Attendance Requests in Draft/Open for this employee in the period
	"""
	if isinstance(employees, str):
		employees = json.loads(employees)
	if not employees or not from_date or not to_date:
		return {"rows": [], "totals": {}}

	start = getdate(from_date)
	end = getdate(to_date)
	calendar_days = (end - start).days + 1

	# --- Fetch leave types and classify as LWP or paid ---
	lwp_types = set()
	ppl_types = set()
	for lt in frappe.get_all("Leave Type", fields=["name", "is_lwp", "is_ppl"]):
		if lt.is_lwp:
			lwp_types.add(lt.name)
		if lt.is_ppl:
			ppl_types.add(lt.name)

	# --- Fetch attendance records ---
	records = frappe.db.sql(
		"""
		SELECT employee, attendance_date, status, half_day_status, leave_type
		FROM `tabAttendance`
		WHERE employee IN %(employees)s
		  AND attendance_date BETWEEN %(from_date)s AND %(to_date)s
		  AND docstatus != 2
		""",
		{"employees": tuple(employees), "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	# Group records by employee
	emp_records = {}
	for r in records:
		emp_records.setdefault(r.employee, []).append(r)

	# --- Fetch holiday dates per employee ---
	# Each employee may have their own Holiday List, or fall back to the company default
	holiday_dates_by_emp = {}
	emp_holiday_lists = {}
	for emp in employees:
		hl = frappe.db.get_value("Employee", emp, "holiday_list")
		if not hl and company:
			hl = frappe.db.get_value("Company", company, "default_holiday_list")
		emp_holiday_lists[emp] = hl

	# Batch-fetch holiday dates for each unique holiday list
	hl_cache = {}
	for emp, hl in emp_holiday_lists.items():
		if not hl:
			holiday_dates_by_emp[emp] = set()
			continue
		if hl not in hl_cache:
			hdates = frappe.get_all(
				"Holiday",
				filters={"parent": hl},
				fields=["holiday_date"],
			)
			hl_cache[hl] = {
				getdate(h.holiday_date) for h in hdates if h.holiday_date
			}
		holiday_dates_by_emp[emp] = hl_cache[hl]

	# --- Determine HOD employees (09:45 cutoff) vs others (09:30 cutoff) ---
	hod_users = frappe.db.sql(
		"""
		SELECT DISTINCT parent
		FROM `tabHas Role`
		WHERE role = 'HOD' AND parenttype = 'User'
		""",
		as_dict=True,
	)
	hod_user_set = {row.parent for row in hod_users}
	hod_employees = set()
	if hod_user_set:
		hod_employees = {
			row.name
			for row in frappe.db.sql(
				"""
				SELECT name
				FROM `tabEmployee`
				WHERE user_id IN %(users)s
				""",
				{"users": list(hod_user_set) or [""]},
				as_dict=True,
			)
		}

	# --- Fetch in_time for attendance records to compute late count ---
	# Match the existing Late Penalty logic: exclude holiday dates and
	# attendances linked to a Leave Application from the raw late count.
	att_in_records = frappe.db.sql(
		"""
		SELECT employee, attendance_date, in_time
		FROM `tabAttendance`
		WHERE employee IN %(employees)s
		  AND attendance_date BETWEEN %(from_date)s AND %(to_date)s
		  AND docstatus != 2
		  AND in_time IS NOT NULL
		  AND leave_application IS NULL
		""",
		{"employees": tuple(employees), "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	late_count_by_emp = {}
	for r in att_in_records:
		holidays_set = holiday_dates_by_emp.get(r.employee, set())
		if getdate(r.attendance_date) in holidays_set:
			continue
		in_time_str = str(r.in_time).split(" ")[-1]
		cutoff = "09:45:00" if r.employee in hod_employees else "09:30:00"
		if in_time_str > cutoff:
			late_count_by_emp[r.employee] = late_count_by_emp.get(r.employee, 0) + 1

	# --- Fetch Late Penalty records for the period ---
	penalty_records = frappe.db.sql(
		"""
		SELECT emp_name, deduction_days, late_penalty
		FROM `tabLate Penalty`
		WHERE emp_name IN %(employees)s
		  AND from_date = %(from_date)s
		  AND to_date = %(to_date)s
		""",
		{"employees": tuple(employees), "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)
	penalty_by_emp = {r.emp_name: r for r in penalty_records}

	# --- Fetch latest Salary Structure Assignment per employee for amount estimate ---
	ssa_by_emp = {}
	for ssa in frappe.db.sql(
		"""
		SELECT employee, base, variable
		FROM `tabSalary Structure Assignment`
		WHERE employee IN %(employees)s
		  AND docstatus = 1
		ORDER BY from_date DESC
		""",
		{"employees": tuple(employees)},
		as_dict=True,
	):
		if ssa.employee not in ssa_by_emp:
			ssa_by_emp[ssa.employee] = ssa

	# --- Fetch approved attendance request offsets for late-penalty estimation ---
	emp_list = tuple(employees)

	attendance_perm_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT employee, COUNT(*) as cnt
		FROM `tabAttendance Permission`
		WHERE employee IN %(employees)s
		  AND status IN ('Approved', 'Open')
		  AND permission_date BETWEEN %(from_date)s AND %(to_date)s
		  AND session = 'First Half'
		GROUP BY employee
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		attendance_perm_by_emp[r.employee] = r.cnt

	on_duty_half_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT employee, COUNT(*) as cnt
		FROM `tabAttendance Request`
		WHERE employee IN %(employees)s
		  AND docstatus = 1
		  AND workflow_state = 'Approved'
		  AND half_day_date BETWEEN %(from_date)s AND %(to_date)s
		  AND half_day = 1
		  AND custom_session = 'First Half'
		GROUP BY employee
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		on_duty_half_by_emp[r.employee] = r.cnt

	permission_full_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT employee, COUNT(*) as cnt
		FROM `tabAttendance Request`
		WHERE employee IN %(employees)s
		  AND docstatus = 1
		  AND workflow_state = 'Approved'
		  AND from_date BETWEEN %(from_date)s AND %(to_date)s
		  AND reason = 'Permission'
		  AND custom_permission_session = 'First Half'
		GROUP BY employee
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		permission_full_by_emp[r.employee] = r.cnt

	on_duty_full_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT ar.employee, COUNT(*) as cnt
		FROM `tabAttendance Request` ar
		WHERE ar.employee IN %(employees)s
		  AND ar.docstatus = 1
		  AND ar.from_date BETWEEN %(from_date)s AND %(to_date)s
		  AND ar.reason = 'On Duty Working Day'
		  AND ar.half_day = 0
		  AND ar.workflow_state = 'Approved'
		  AND EXISTS (
			  SELECT 1 FROM `tabAttendance` att
			  WHERE att.attendance_request = ar.name AND att.in_time IS NOT NULL
		  )
		GROUP BY ar.employee
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		on_duty_full_by_emp[r.employee] = r.cnt

	leave_half_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT employee, COUNT(*) as cnt
		FROM `tabLeave Application`
		WHERE employee IN %(employees)s
		  AND docstatus = 1
		  AND half_day = 1
		  AND half_day_date BETWEEN %(from_date)s AND %(to_date)s
		  AND custom_session = 'First Half'
		GROUP BY employee
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		leave_half_by_emp[r.employee] = r.cnt

	# --- Fetch unapproved Leave Applications (docstatus=0) per employee ---
	unapproved_leaves_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT employee, COUNT(*) as cnt
		FROM `tabLeave Application`
		WHERE employee IN %(employees)s
		  AND docstatus = 0
		  AND from_date <= %(to_date)s
		  AND to_date >= %(from_date)s
		GROUP BY employee
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		unapproved_leaves_by_emp[r.employee] = r.cnt

	# --- Fetch unapproved Attendance Requests (docstatus=0) per employee ---
	unapproved_att_req_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT employee, COUNT(*) as cnt
		FROM `tabAttendance Request`
		WHERE employee IN %(employees)s
		  AND docstatus = 0
		  AND from_date <= %(to_date)s
		  AND to_date >= %(from_date)s
		GROUP BY employee
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		unapproved_att_req_by_emp[r.employee] = r.cnt

	# --- Fetch date_of_joining per employee for holiday calculation ---
	doj_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT name, date_of_joining
		FROM `tabEmployee`
		WHERE name IN %(employees)s
		""",
		{"employees": emp_list},
		as_dict=True,
	):
		doj_by_emp[r.name] = getdate(r.date_of_joining) if r.date_of_joining else None

	# --- Fetch approved Leave Applications to check prefix/suffix condition ---
	# For each employee, get the set of leave dates (docstatus=1, non-LWP)
	approved_leave_dates_by_emp = {}
	for r in frappe.db.sql(
		"""
		SELECT la.employee, la.from_date, la.to_date, la.half_day, la.half_day_date
		FROM `tabLeave Application` la
		WHERE la.employee IN %(employees)s
		  AND la.docstatus = 1
		  AND la.from_date <= %(to_date)s
		  AND la.to_date >= %(from_date)s
		""",
		{"employees": emp_list, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	):
		dates = set()
		ld = getdate(r.from_date)
		td = getdate(r.to_date)
		cur = ld
		while cur <= td:
			dates.add(cur)
			cur += timedelta(days=1)
		if r.half_day and r.half_day_date:
			# half-day leave: still counts as "on leave" for prefix/suffix
			dates.add(getdate(r.half_day_date))
		approved_leave_dates_by_emp.setdefault(r.employee, set()).update(dates)

	# --- Build per-employee summary ---
	rows = []
	totals = {
		"calendar_days": 0,
		"holidays": 0,
		"present": 0,
		"paid_leave": 0,
		"absent_unpaid": 0,
		"absent_count": 0,
		"lwp_count": 0,
		"payment_days": 0,
		"late_count": 0,
		"late_penalty_days": 0,
		"unapproved_leaves": 0,
		"unapproved_attendance_requests": 0,
	}

	for emp in employees:
		recs = emp_records.get(emp, [])
		holidays_set = holiday_dates_by_emp.get(emp, set())
		doj = doj_by_emp.get(emp)
		emp_leave_dates = approved_leave_dates_by_emp.get(emp, set())

		# Count holidays within the date range, but only from the employee's
		# date of joining (Req 6), and applying the prefix/suffix condition
		# (Req 7): if the employee was on leave on the day before a holiday
		# (prefix) AND the day after (suffix), the holiday is NOT counted.
		holiday_count = 0
		for d in _daterange(from_date, to_date):
			if d not in holidays_set:
				continue
			# Req 6: only count holidays on or after date of joining
			if doj and d < doj:
				continue
			# Req 7: prefix/suffix — if leave on the day before AND the day after,
			# the holiday is sandwiched by leave and should not be counted as holiday
			prev_day = d - timedelta(days=1)
			next_day = d + timedelta(days=1)
			if prev_day in emp_leave_dates and next_day in emp_leave_dates:
				continue
			holiday_count += 1

		present = 0.0
		paid_leave = 0.0
		absent_unpaid = 0.0
		absent_count = 0.0
		lwp_count = 0.0

		for r in recs:
			# Skip attendance records that fall on holidays (Sundays/weekly offs).
			# Holidays are already counted as paid days via holiday_count.
			# Working on a holiday gives compensatory off (handled separately),
			# so it should NOT add to present. Being absent on a holiday should
			# NOT reduce payment days either.
			if getdate(r.attendance_date) in holidays_set:
				continue

			is_half = bool(r.half_day_status)
			weight = 0.5 if is_half else 1.0

			if r.status in ("Present", "Work From Home"):
				# If status is Present, always count as full present (1.0)
				# regardless of half_day_status — attendance may be manually updated
				present += 1.0
			elif r.status == "Half Day":
				present += 0.5
				# The other half depends on half_day_status and leave_type:
				# - If half_day_status is "Absent" and no leave_type -> absent
				# - If leave_type is LWP -> absent_unpaid
				# - Otherwise (paid leave) -> paid_leave
				if r.half_day_status == "Absent" and not r.leave_type:
					absent_unpaid += 0.5
					absent_count += 0.5
				elif r.leave_type and r.leave_type in lwp_types:
					absent_unpaid += 0.5
					lwp_count += 0.5
				else:
					paid_leave += 0.5
			elif r.status == "On Leave":
				if r.leave_type and r.leave_type in lwp_types:
					absent_unpaid += weight
					lwp_count += weight
				else:
					paid_leave += weight
			elif r.status == "Absent":
				absent_unpaid += weight
				absent_count += weight

		emp_doc = frappe.db.get_value(
			"Employee", emp, ["name", "employee_name", "department", "designation"], as_dict=True
		) or {"name": emp, "employee_name": emp, "department": "", "designation": ""}

		penalty = penalty_by_emp.get(emp, {})
		late_count = late_count_by_emp.get(emp, 0)
		late_penalty_days = flt(penalty.get("deduction_days") or 0)

		# Estimate penalty from late count only when no Late Penalty record
		# exists for this period. A record with deduction_days = 0 means the
		# penalty was explicitly cleared (e.g. corrected), so don't override it.
		if not penalty and late_count:
			offsets = (
				attendance_perm_by_emp.get(emp, 0)
				+ on_duty_half_by_emp.get(emp, 0)
				+ permission_full_by_emp.get(emp, 0)
				+ on_duty_full_by_emp.get(emp, 0)
				+ leave_half_by_emp.get(emp, 0)
			)
			late_penalty_days = _estimate_late_penalty_days(late_count, offsets)

		# Payment days = present + paid_leave + holidays - late_penalty_days (capped at calendar_days, min 0)
		payment_days = present + paid_leave + holiday_count - late_penalty_days
		payment_days = max(0, min(payment_days, calendar_days))

		unapproved_leaves = unapproved_leaves_by_emp.get(emp, 0)
		unapproved_att_req = unapproved_att_req_by_emp.get(emp, 0)

		row = {
			"employee": emp,
			"employee_name": emp_doc.employee_name,
			"department": emp_doc.department or "",
			"designation": emp_doc.designation or "",
			"calendar_days": calendar_days,
			"holidays": holiday_count,
			"present": present,
			"paid_leave": paid_leave,
			"absent_unpaid": absent_unpaid,
			"absent_count": absent_count,
			"lwp_count": lwp_count,
			"payment_days": payment_days,
			"late_count": late_count,
			"late_penalty_days": late_penalty_days,
			"unapproved_leaves": unapproved_leaves,
			"unapproved_attendance_requests": unapproved_att_req,
		}
		rows.append(row)

		totals["calendar_days"] += calendar_days
		totals["holidays"] += holiday_count
		totals["present"] += present
		totals["paid_leave"] += paid_leave
		totals["absent_unpaid"] += absent_unpaid
		totals["absent_count"] += absent_count
		totals["lwp_count"] += lwp_count
		totals["payment_days"] += payment_days
		totals["late_count"] += late_count
		totals["late_penalty_days"] += late_penalty_days
		totals["unapproved_leaves"] += unapproved_leaves
		totals["unapproved_attendance_requests"] += unapproved_att_req

	return {"rows": rows, "totals": totals}


@frappe.whitelist()
def _debug_attendance_summary(employees, from_date, to_date, company=None):
	import json

	if isinstance(employees, str):
		employees = json.loads(employees)

	from collections import defaultdict

	hod_users = frappe.db.sql(
		"""SELECT DISTINCT parent FROM `tabHas Role` WHERE role = 'HOD' AND parenttype = 'User'""",
		as_dict=True,
	)
	hod_user_set = {row.parent for row in hod_users}
	hod_employees = set()
	if hod_user_set:
		hod_employees = {
			row.name
			for row in frappe.db.sql(
				"""SELECT name FROM `tabEmployee` WHERE user_id IN %(users)s""",
				{"users": list(hod_user_set) or [""]},
				as_dict=True,
			)
		}

	att_records = frappe.db.sql(
		"""
		SELECT attendance_date, status, half_day_status, leave_type, in_time, attendance_request, leave_application
		FROM `tabAttendance`
		WHERE employee = %(emp)s AND attendance_date BETWEEN %(from_date)s AND %(to_date)s AND docstatus != 2
		ORDER BY attendance_date
		""",
		{"emp": employees[0], "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	late_count = 0
	late_dates = []
	for r in att_records:
		if not r.in_time:
			continue
		holiday_list = frappe.db.get_value("Employee", employees[0], "holiday_list") or ""
		is_hol = frappe.db.exists("Holiday", {"parent": holiday_list, "holiday_date": r.attendance_date})
		if is_hol or r.leave_application:
			continue
		in_time_str = str(r.in_time).split(" ")[-1]
		cutoff = "09:45:00" if employees[0] in hod_employees else "09:30:00"
		if in_time_str > cutoff:
			late_count += 1
			late_dates.append({"date": str(r.attendance_date), "in_time": in_time_str})

	# offsets
	att_perm = frappe.db.sql(
		"""SELECT permission_date, session, status FROM `tabAttendance Permission` WHERE employee = %(emp)s AND status IN ('Approved','Open') AND permission_date BETWEEN %(from_date)s AND %(to_date)s AND session = 'First Half'""",
		{"emp": employees[0], "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)
	on_duty_half = frappe.db.sql(
		"""SELECT half_day_date, reason FROM `tabAttendance Request` WHERE employee = %(emp)s AND docstatus = 1 AND workflow_state = 'Approved' AND half_day_date BETWEEN %(from_date)s AND %(to_date)s AND half_day = 1 AND custom_session = 'First Half'""",
		{"emp": employees[0], "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)
	perm_full = frappe.db.sql(
		"""SELECT from_date, reason FROM `tabAttendance Request` WHERE employee = %(emp)s AND docstatus = 1 AND workflow_state = 'Approved' AND from_date BETWEEN %(from_date)s AND %(to_date)s AND reason = 'Permission' AND custom_permission_session = 'First Half'""",
		{"emp": employees[0], "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)
	on_duty_full = frappe.db.sql(
		"""SELECT ar.name, ar.from_date FROM `tabAttendance Request` ar WHERE ar.employee = %(emp)s AND ar.docstatus = 1 AND ar.from_date BETWEEN %(from_date)s AND %(to_date)s AND ar.reason = 'On Duty Working Day' AND ar.half_day = 0 AND ar.workflow_state = 'Approved' AND EXISTS (SELECT 1 FROM `tabAttendance` att WHERE att.attendance_request = ar.name AND att.in_time IS NOT NULL)""",
		{"emp": employees[0], "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)
	leave_half = frappe.db.sql(
		"""SELECT half_day_date, leave_type FROM `tabLeave Application` WHERE employee = %(emp)s AND docstatus = 1 AND half_day = 1 AND half_day_date BETWEEN %(from_date)s AND %(to_date)s AND custom_session = 'First Half'""",
		{"emp": employees[0], "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	ssa = frappe.db.sql(
		"""SELECT base, variable FROM `tabSalary Structure Assignment` WHERE employee = %(emp)s AND docstatus = 1 ORDER BY from_date DESC LIMIT 1""",
		{"emp": employees[0]},
		as_dict=True,
	)

	penalty_rec = frappe.db.sql(
		"""SELECT deduction_days, late_penalty FROM `tabLate Penalty` WHERE emp_name = %(emp)s AND from_date = %(from_date)s AND to_date = %(to_date)s""",
		{"emp": employees[0], "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	return {
		"employee": employees[0],
		"late_count": late_count,
		"late_dates": late_dates,
		"offsets": {
			"attendance_permissions_first_half": len(att_perm),
			"on_duty_half_first_half": len(on_duty_half),
			"permission_full_first_half": len(perm_full),
			"on_duty_full_day": len(on_duty_full),
			"leave_half_first_half": len(leave_half),
		},
		"salary_structure_assignment": ssa[0] if ssa else None,
		"late_penalty_record": penalty_rec[0] if penalty_rec else None,
	}


@frappe.whitelist()
def get_attendance_detail(attendance_name):
	"""Return full detail of a single Attendance record for the day-detail modal."""
	doc = frappe.db.get_value(
		"Attendance",
		attendance_name,
		[
			"name", "employee", "employee_name", "attendance_date", "status",
			"half_day_status", "shift", "in_time", "out_time",
			"late_entry", "early_exit", "leave_type", "leave_application",
			"docstatus", "company", "department",
		],
		as_dict=True,
	)
	if not doc:
		frappe.throw(_("Attendance record {0} not found").format(attendance_name))
	if doc.attendance_date:
		doc.attendance_date = str(doc.attendance_date)
	if doc.in_time:
		doc.in_time = str(doc.in_time)
	if doc.out_time:
		doc.out_time = str(doc.out_time)
	return doc


@frappe.whitelist()
def submit_attendance_for_employees(employees, from_date, to_date):
	"""Submit all draft Attendance records for the selected employees in the date range."""
	if isinstance(employees, str):
		employees = json.loads(employees)
	if not employees:
		frappe.throw(_("No employees selected"))

	drafts = frappe.db.sql(
		"""
		SELECT name FROM `tabAttendance`
		WHERE employee IN %(employees)s
		  AND attendance_date BETWEEN %(from_date)s AND %(to_date)s
		  AND docstatus = 0
		""",
		{"employees": tuple(employees), "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	submitted = 0
	errors = []
	for row in drafts:
		try:
			doc = frappe.get_doc("Attendance", row.name)
			doc.submit()
			frappe.db.commit()
			submitted += 1
		except Exception as e:
			frappe.db.rollback()
			errors.append(f"{row.name}: {str(e)}")

	return {"submitted": submitted, "total": len(drafts), "errors": errors}


@frappe.whitelist()
def cancel_attendance_for_employees(employees, from_date, to_date):
	"""Cancel all submitted Attendance records for the selected employees in the date range."""
	if isinstance(employees, str):
		employees = json.loads(employees)
	if not employees:
		frappe.throw(_("No employees selected"))

	submitted = frappe.db.sql(
		"""
		SELECT name FROM `tabAttendance`
		WHERE employee IN %(employees)s
		  AND attendance_date BETWEEN %(from_date)s AND %(to_date)s
		  AND docstatus = 1
		""",
		{"employees": tuple(employees), "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	cancelled = 0
	errors = []
	for row in submitted:
		try:
			doc = frappe.get_doc("Attendance", row.name)
			doc.cancel()
			frappe.db.commit()
			cancelled += 1
		except Exception as e:
			frappe.db.rollback()
			errors.append(f"{row.name}: {str(e)}")

	return {"cancelled": cancelled, "total": len(submitted), "errors": errors}


# ---------------------------------------------------------------------------
# Step 3: On-Demand Payroll Generation & Salary Register
# ---------------------------------------------------------------------------

@frappe.whitelist()
def generate_payroll(
	employees,
	start_date,
	end_date,
	company,
	currency=None,
	payroll_payable_account=None,
	posting_date=None,
	payroll_frequency="Monthly",
):
	"""Generate Draft Salary Slips for the selected employees and period.

	Creates a Draft Payroll Entry (never submitted by this function) and uses
	HRMS's create_salary_slips_for_employees to build the slips.

	Req 1: If any selected employee has a non-cancelled slip for this period,
	generation is BLOCKED. The user must cancel existing slips first (via the
	salary register) before regenerating.
	"""
	if isinstance(employees, str):
		employees = json.loads(employees)
	if not employees:
		frappe.throw(_("No employees selected"))

	if not currency:
		currency = _get_company_currency(company)
	if not payroll_payable_account:
		payroll_payable_account = _get_payroll_payable_account(company)
	if not posting_date:
		posting_date = nowdate()

	# Req 1: Check for existing non-cancelled slips for this period.
	# If any exist, BLOCK generation — user must cancel them first.
	existing = frappe.db.sql(
		"""
		SELECT employee, name, docstatus FROM `tabSalary Slip`
		WHERE employee IN %(employees)s
		  AND start_date = %(start_date)s
		  AND end_date = %(end_date)s
		  AND docstatus != 2
		""",
		{
			"employees": tuple(employees),
			"start_date": start_date,
			"end_date": end_date,
		},
		as_dict=True,
	)
	if existing:
		# Build a readable list of employees with existing slips
		emp_names = {}
		for r in existing:
			ename = frappe.db.get_value("Employee", r.employee, "employee_name") or r.employee
			status_label = "Draft" if r.docstatus == 0 else "Submitted"
			emp_names[r.employee] = f"{ename} ({status_label})"
		details = ", ".join(emp_names.values())
		frappe.throw(
			_(
				"Payroll already exists for this period for {0} employee(s): {1}. "
				"Please cancel their salary slips first (via the Salary Register) "
				"to regenerate payroll."
			).format(len(existing), details)
		)

	to_create = list(employees)

	# Filter out employees without an active Salary Structure Assignment
	# applicable during the payroll period — HRMS will throw otherwise.
	# Note: Use end_date (not start_date) so that employees who join mid-period
	# (SSA from_date after payroll start_date) are still included.
	if to_create:
		ssa_employees = {
			r.employee
			for r in frappe.db.sql(
				"""
				SELECT DISTINCT ssa.employee
				FROM `tabSalary Structure Assignment` ssa
				INNER JOIN `tabSalary Structure` ss
					ON ss.name = ssa.salary_structure
				WHERE ssa.employee IN %(employees)s
				  AND ssa.docstatus = 1
				  AND ssa.from_date <= %(end_date)s
				  AND ss.docstatus = 1
				  AND ss.is_active = 'Yes'
				""",
				{"employees": tuple(to_create), "end_date": end_date},
				as_dict=True,
			)
		}
		no_ssa = [e for e in to_create if e not in ssa_employees]
		to_create = [e for e in to_create if e in ssa_employees]
		if no_ssa:
			emp_names = {
				e: frappe.db.get_value("Employee", e, "employee_name") or e
				for e in no_ssa
			}
			frappe.logger().warning(
				"Payroll Workbench: skipped employees without active Salary Structure "
				f"Assignment for {start_date}: {emp_names}"
			)

	# Find or create a Draft Payroll Entry for this period
	# First, check if any existing slip is already linked to a Payroll Entry
	pe_name = None
	pe_name = frappe.db.get_value(
		"Salary Slip",
		{
			"employee": ["in", employees],
			"start_date": start_date,
			"end_date": end_date,
			"docstatus": ["!=", 2],
			"payroll_entry": ["is", "set"],
		},
		"payroll_entry",
	)

	# If not found via slip, look for ANY existing draft PE for this
	# period+company (regardless of salary_slips_created) to avoid creating
	# a duplicate Payroll Entry when generate_payroll is called again.
	if not pe_name:
		pe_name = frappe.db.get_value(
			"Payroll Entry",
			{
				"company": company,
				"start_date": start_date,
				"end_date": end_date,
				"docstatus": 0,
			},
		)
	if not pe_name:
		pe = frappe.get_doc(
			{
				"doctype": "Payroll Entry",
				"company": company,
				"start_date": start_date,
				"end_date": end_date,
				"posting_date": posting_date,
				"payroll_frequency": payroll_frequency,
				"currency": currency,
				"exchange_rate": 1,
				"payroll_payable_account": payroll_payable_account,
				"salary_slip_based_on_timesheet": 0,
			}
		)
		pe.insert(ignore_permissions=True)
		pe_name = pe.name
	else:
		pe = frappe.get_doc("Payroll Entry", pe_name)

	# Fill employee details into the PE — only if it's still a Draft
	# (cannot modify a submitted PE)
	if pe.docstatus == 0:
		pe.set("employees", [])
		for emp_name in employees:
			emp_doc = frappe.db.get_value(
				"Employee",
				emp_name,
				["name", "employee_name", "department", "designation", "branch", "company"],
				as_dict=True,
			)
			if emp_doc:
				pe.append(
					"employees",
					{
						"employee": emp_doc.name,
						"employee_name": emp_doc.employee_name,
						"department": emp_doc.department,
						"designation": emp_doc.designation,
						"branch": emp_doc.branch,
						"company": emp_doc.company,
					},
				)
		pe.save(ignore_permissions=True)

	created_slips = []
	skipped = []
	skipped_no_ssa = []

	if to_create:
		from hrms.payroll.doctype.payroll_entry.payroll_entry import (
			create_salary_slips_for_employees,
		)

		args = frappe._dict(
			{
				"salary_slip_based_on_timesheet": 0,
				"payroll_frequency": payroll_frequency,
				"start_date": start_date,
				"end_date": end_date,
				"company": company,
				"posting_date": posting_date,
				"deduct_tax_for_unsubmitted_tax_exemption_proof": 0,
				"payroll_entry": pe_name,
				"exchange_rate": 1.0,
				"currency": currency,
			}
		)
		# Temporarily disable the appraisal gate error so we can surface it gracefully
		try:
			create_salary_slips_for_employees(to_create, args, publish_progress=False)
		except Exception as e:
			frappe.log_error(title="Payroll Workbench: generate_payroll failed", message=frappe.get_traceback())
			frappe.throw(_("Salary slip generation failed: {0}").format(str(e)))

		# Fetch newly created draft slips
		created_slips = frappe.db.sql(
			"""
			SELECT name, employee FROM `tabSalary Slip`
			WHERE employee IN %(employees)s
			  AND start_date = %(start_date)s
			  AND end_date = %(end_date)s
			  AND docstatus = 0
			""",
			{
				"employees": tuple(to_create),
				"start_date": start_date,
				"end_date": end_date,
			},
			as_dict=True,
		)

	return {
		"payroll_entry": pe_name,
		"created": [{"name": s.name, "employee": s.employee} for s in created_slips],
		"skipped": skipped,
		"skipped_no_salary_structure": skipped_no_ssa,
	}


@frappe.whitelist()
def cancel_salary_slip(slip_name):
	"""Cancel a single Salary Slip so it can be regenerated.

	Req 1: Allows the user to cancel an individual employee's salary slip
	from the salary register. After cancellation, the employee's payroll
	can be regenerated via generate_payroll.

	- Draft slips (docstatus=0): cancelled directly.
	- Submitted slips (docstatus=1): cancelled via HRMS cancellation flow,
	  which also handles unlinking from the Payroll Entry / JE.
	"""
	slip = frappe.get_doc("Salary Slip", slip_name)
	if slip.docstatus == 2:
		frappe.throw(_("Salary Slip {0} is already cancelled").format(slip_name))
	if slip.docstatus == 0:
		# Draft — cancel directly
		slip.cancel()
	elif slip.docstatus == 1:
		# Submitted — cancel (HRMS handles JE unlinking)
		slip.cancel()
	frappe.db.commit()
	return {"slip": slip_name, "status": "Cancelled"}


@frappe.whitelist()
def submit_single_slip(slip_name):
	"""Submit a single draft Salary Slip."""
	slip = frappe.get_doc("Salary Slip", slip_name)
	if slip.docstatus == 1:
		return {"submitted": False, "error": "Slip is already submitted"}
	if slip.docstatus == 2:
		return {"submitted": False, "error": "Cannot submit a cancelled slip"}
	if slip.net_pay < 0:
		return {"submitted": False, "error": "Net pay is negative — cannot submit"}
	frappe.flags.via_payroll_entry = True
	try:
		slip.submit()
		frappe.db.commit()
		return {"submitted": True, "slip": slip_name}
	except Exception as e:
		frappe.db.rollback()
		return {"submitted": False, "error": str(e)}
	finally:
		frappe.flags.via_payroll_entry = False


@frappe.whitelist()
def submit_draft_slips(payroll_entry_name=None):
	"""Submit all draft salary slips for a Payroll Entry.

	Does NOT create the accrual JE — that's done separately via book_payroll.
	Only submits the slips so they move from Draft to Submitted status.
	"""
	submitted = []
	unsubmitted = []
	errors = []

	# Find draft slips
	if payroll_entry_name:
		draft_slips = frappe.db.sql(
			"""
			SELECT name FROM `tabSalary Slip`
			WHERE payroll_entry = %s AND docstatus = 0
			""",
			(payroll_entry_name,),
			as_dict=True,
		)
	else:
		draft_slips = frappe.db.sql(
			"SELECT name FROM `tabSalary Slip` WHERE docstatus = 0",
			as_dict=True,
		)

	frappe.flags.via_payroll_entry = True
	try:
		for row in draft_slips:
			slip_name = row["name"]
			try:
				slip = frappe.get_doc("Salary Slip", slip_name)
				if slip.net_pay < 0:
					unsubmitted.append(slip_name)
					continue
				slip.submit()
				frappe.db.commit()
				submitted.append(slip_name)
			except Exception as e:
				frappe.db.rollback()
				unsubmitted.append(slip_name)
				errors.append(f"{slip_name}: {str(e)}")
	finally:
		frappe.flags.via_payroll_entry = False

	return {
		"submitted": len(submitted),
		"unsubmitted": len(unsubmitted),
		"errors": errors,
	}


@frappe.whitelist()
def update_slip_arrear(slip_name, component, amount):
	"""Update an Arrear-Pay or Arrear-Deduct amount on a draft Salary Slip.

	Req 3: Only Arrear-Pay and Arrear-Deduct components are editable from
	the salary register. All other components remain read-only (computed
	from the salary structure formula). The slip must be in Draft status.
	"""
	if component not in ("Arrear-Pay", "Arrear-Deduct"):
		frappe.throw(_("Only Arrear-Pay and Arrear-Deduct can be edited from the register"))

	slip = frappe.get_doc("Salary Slip", slip_name)
	if slip.docstatus != 0:
		frappe.throw(_("Can only edit arrears on a Draft salary slip. Slip {0} is not Draft.").format(slip_name))

	amount = flt(amount)
	parentfield = "earnings" if component == "Arrear-Pay" else "deductions"

	# Find the component row
	found = False
	for row in slip.get(parentfield):
		if row.salary_component == component:
			row.amount = amount
			row.amount_based_on_formula = 0
			found = True
			break

	if not found:
		# Component doesn't exist on this slip — append it
		slip.append(parentfield, {
			"salary_component": component,
			"amount": amount,
			"amount_based_on_formula": 0,
		})

	# Recalculate the slip totals
	slip.calculate_net_pay()
	slip.save(ignore_permissions=True)
	frappe.db.commit()

	return {
		"slip": slip_name,
		"component": component,
		"amount": amount,
		"gross_pay": flt(slip.gross_pay),
		"total_deduction": flt(slip.total_deduction),
		"net_pay": flt(slip.net_pay),
		"rounded_total": flt(slip.rounded_total),
	}


@frappe.whitelist()
def get_payroll_period_status(start_date, end_date, company, employees=None):
	"""Return existing payroll state for a period so the workbench can auto-populate.

	Returns:
		payroll_entry: name of the most recent non-cancelled Payroll Entry for the period
		booked_je:     name of the accrual JE linked to that Payroll Entry (if booked)
		slip_counts:   {draft, submitted, paid, total}
		payout_status: {employee: {status, message, reference_number}} for paid slips

	Uses date overlap (not exact match) so that minor start_date differences
	(e.g. user selects June 30, slips created with July 1) still match.
	"""
	if isinstance(employees, str):
		employees = json.loads(employees)

	# Find the most recent non-cancelled Payroll Entry whose dates overlap
	# with the selected period (not just exact match)
	pe_name = frappe.db.sql(
		"""
		SELECT name FROM `tabPayroll Entry`
		WHERE company = %s
		  AND docstatus != 2
		  AND start_date <= %s
		  AND end_date >= %s
		ORDER BY creation DESC
		LIMIT 1
		""",
		[company, end_date, start_date],
	)[0][0] if frappe.db.sql(
		"""
		SELECT name FROM `tabPayroll Entry`
		WHERE company = %s
		  AND docstatus != 2
		  AND start_date <= %s
		  AND end_date >= %s
		ORDER BY creation DESC
		LIMIT 1
		""",
		[company, end_date, start_date],
	) else None

	booked_je = None
	booked_je_docstatus = None
	slip_counts = {"draft": 0, "submitted": 0, "paid": 0, "total": 0}
	payout_status = {}

	if pe_name:
		# Check for accrual JE linked to this PE.
		# The JE is created by _make_accrual_je which does NOT set
		# reference_type/reference_name on JE account rows (to avoid
		# ERPNext reconciliation issues), so we look up the JE from the
		# salary slip's journal_entry field instead.
		je_name_on_slip = frappe.db.get_value(
			"Salary Slip",
			{"payroll_entry": pe_name, "docstatus": 1, "journal_entry": ("!=", "")},
			"journal_entry",
		)
		if je_name_on_slip:
			je_ds = frappe.db.get_value("Journal Entry", je_name_on_slip, "docstatus")
			if je_ds is not None and je_ds != 2:
				booked_je = je_name_on_slip
				booked_je_docstatus = je_ds

	# Count slips whose dates overlap with the selected period
	# (slip.start_date <= selected.end_date AND slip.end_date >= selected.start_date)
	slip_conditions = "docstatus != 2 AND company = %s AND start_date <= %s AND end_date >= %s"
	slip_values = [company, end_date, start_date]
	if employees:
		slip_conditions += " AND employee IN (%s)" % ",".join(["%s"] * len(employees))
		slip_values.extend(employees)

	slips = frappe.db.sql(
		f"""
		SELECT name, employee, docstatus, custom_payment_status, custom_payment_je
		FROM `tabSalary Slip`
		WHERE {slip_conditions}
		""",
		slip_values,
		as_dict=True,
	)
	slip_counts["total"] = len(slips)
	payment_je = None
	payment_je_docstatus = None
	for s in slips:
		if s.docstatus == 0:
			slip_counts["draft"] += 1
		elif s.docstatus == 1:
			slip_counts["submitted"] += 1
			if s.custom_payment_status == "Paid":
				slip_counts["paid"] += 1
				payout_status[s.employee] = {
					"status": "Paid",
					"message": "Payment released",
					"reference_number": "",
				}
				if s.custom_payment_je and not payment_je:
					payment_je = s.custom_payment_je
					payment_je_docstatus = frappe.db.get_value("Journal Entry", payment_je, "docstatus")

	return {
		"payroll_entry": pe_name,
		"booked_je": booked_je,
		"booked_je_docstatus": booked_je_docstatus,
		"payment_je": payment_je,
		"payment_je_docstatus": payment_je_docstatus,
		"slip_counts": slip_counts,
		"payout_status": payout_status,
	}


@frappe.whitelist()
def get_salary_register(start_date, end_date, employees=None, company=None):
	"""Return the salary register: per-employee earnings/deductions breakdown.

	Uses date overlap (not exact match) so minor start_date differences
	between user selection and slip dates still match.
	"""
	if isinstance(employees, str):
		employees = json.loads(employees)

	# Use overlapping date range instead of exact match
	conditions = ["ss.docstatus != 2", "ss.start_date <= %s", "ss.end_date >= %s"]
	values = [end_date, start_date]
	if company:
		conditions.append("ss.company = %s")
		values.append(company)
	if employees:
		placeholders = ",".join(["%s"] * len(employees))
		conditions.append(f"ss.employee IN ({placeholders})")
		values.extend(employees)

	slips = frappe.db.sql(
		f"""
		SELECT ss.name, ss.employee, ss.employee_name, ss.salary_structure,
		       ss.gross_pay, ss.total_deduction, ss.net_pay, ss.rounded_total,
		       ss.payment_days, ss.total_working_days,
		       ss.docstatus, ss.status, ss.start_date, ss.end_date,
		       ss.custom_payment_status, ss.custom_payment_je, ss.journal_entry,
		       e.bank_ac_no, e.ifsc_code
		FROM `tabSalary Slip` ss
		LEFT JOIN `tabEmployee` e ON e.name = ss.employee
		WHERE {' AND '.join(conditions)}
		ORDER BY ss.employee_name
		""",
		values,
		as_dict=True,
	)

	# Collect all unique component names for dynamic columns
	all_earnings = []
	all_deductions = []
	seen_earnings = set()
	seen_deductions = set()

	# Req 4: Components that should be ordered adjacently
	# PF - Employer (earning) should be next to PF - Employee (deduction)
	PF_EMPLOYER = "PF - Employer"
	PF_EMPLOYEE = "PF - Employee"
	PROFESSIONAL_TAX = "Professional Tax"
	ARREAR_DEDUCT = "Arrear-Deduct"
	ARREAR_PAY = "Arrear-Pay"

	for slip in slips:
		slip_doc = frappe.get_doc("Salary Slip", slip.name)
		slip.earnings = []
		slip.deductions = []
		# Compute fixed_gross = full monthly salary (base from SSA + BYOD allowance)
		# This is the unprorated amount the employee would earn for a full month
		ssa_base = frappe.db.get_value("Salary Structure Assignment",
			{"employee": slip.employee, "docstatus": 1, "from_date": ["<=", slip.end_date]},
			"base", order_by="from_date DESC") or 0
		emp_doc = frappe.get_doc("Employee", slip.employee)
		byod = emp_doc.custom_byod_allowance or 0
		slip["fixed_gross"] = flt(ssa_base + byod)
		for e in slip_doc.earnings:
			if not e.statistical_component and not e.do_not_include_in_total:
				slip.earnings.append(
					{"component": e.salary_component, "amount": flt(e.amount)}
				)
				if e.salary_component not in seen_earnings:
					seen_earnings.add(e.salary_component)
					all_earnings.append(e.salary_component)
		for d in slip_doc.deductions:
			if not d.statistical_component and not d.do_not_include_in_total:
				slip.deductions.append(
					{"component": d.salary_component, "amount": flt(d.amount)}
				)
				if d.salary_component not in seen_deductions:
					seen_deductions.add(d.salary_component)
					all_deductions.append(d.salary_component)

		# Req 4: Compute custom Total Deduction =
		# PF - Employer + PF - Employee + Professional Tax + Arrear-Deduct
		def _get_amount(items, comp):
			for item in items:
				if item["component"] == comp:
					return item["amount"]
			return 0.0

		pf_employer = _get_amount(slip.earnings, PF_EMPLOYER)
		pf_employee = _get_amount(slip.deductions, PF_EMPLOYEE)
		prof_tax = _get_amount(slip.deductions, PROFESSIONAL_TAX)
		arrear_deduct = _get_amount(slip.deductions, ARREAR_DEDUCT)
		slip["custom_total_deduction"] = flt(pf_employer + pf_employee + prof_tax + arrear_deduct)

	# Req 3: Always include Arrear-Pay and Arrear-Deduct columns even if no
	# slip currently has them, so the editable input fields always render.
	if ARREAR_PAY not in all_earnings:
		all_earnings.append(ARREAR_PAY)
	if ARREAR_DEDUCT not in all_deductions:
		all_deductions.append(ARREAR_DEDUCT)

	# Req 4: Reorder earnings columns so PF - Employer is last
	# (it will be adjacent to PF - Employee which is first in deductions)
	if PF_EMPLOYER in all_earnings:
		all_earnings.remove(PF_EMPLOYER)
		all_earnings.append(PF_EMPLOYER)

	# Req 4: Reorder deductions columns so PF - Employee is first
	if PF_EMPLOYEE in all_deductions:
		all_deductions.remove(PF_EMPLOYEE)
		all_deductions.insert(0, PF_EMPLOYEE)

	return {
		"slips": slips,
		"earnings_columns": all_earnings,
		"deductions_columns": all_deductions,
	}


@frappe.whitelist()
def recalculate_sheet(start_date, end_date, employees=None):
	"""Re-fetch fresh DB values for the salary register (after user edits slips in another tab)."""
	return get_salary_register(start_date, end_date, employees)


@frappe.whitelist()
def regenerate_payroll(employees, start_date, end_date, company):
	"""Delete existing salary slips and payroll entries for the period and regenerate fresh ones."""
	if employees and isinstance(employees, str):
		employees = json.loads(employees)

	# Delete existing salary slips for this period
	deleted_slips = 0
	existing_slips = frappe.db.sql(
		"""
		SELECT name FROM `tabSalary Slip`
		WHERE start_date <= %s AND end_date >= %s AND docstatus != 2
		""",
		(end_date, start_date),
		as_dict=True,
	)
	for s in existing_slips:
		try:
			slip = frappe.get_doc("Salary Slip", s.name)
			if slip.docstatus == 1:
				slip.cancel()
			frappe.delete_doc("Salary Slip", s.name, ignore_permissions=True)
			deleted_slips += 1
		except Exception:
			pass

	# Delete existing payroll entries for this period
	deleted_payroll_entries = 0
	existing_pes = frappe.db.sql(
		"""
		SELECT name FROM `tabPayroll Entry`
		WHERE start_date <= %s AND end_date >= %s AND docstatus != 2
		""",
		(end_date, start_date),
		as_dict=True,
	)
	for pe in existing_pes:
		try:
			pe_doc = frappe.get_doc("Payroll Entry", pe.name)
			if pe_doc.docstatus == 1:
				pe_doc.cancel()
			frappe.delete_doc("Payroll Entry", pe.name, ignore_permissions=True)
			deleted_payroll_entries += 1
		except Exception:
			pass

	frappe.db.commit()

	# Generate fresh payroll
	result = generate_payroll(
		employees=employees,
		start_date=start_date,
		end_date=end_date,
		company=company,
	)
	return {
		"deleted_slips": deleted_slips,
		"deleted_payroll_entries": deleted_payroll_entries,
		"created": result.get("created", []),
		"skipped_no_salary_structure": result.get("skipped_no_salary_structure", []),
		"payroll_entry": result.get("payroll_entry"),
	}


@frappe.whitelist()
def generate_epf_esi_return(payroll_entry_name, file_type, manual_rows=None):
	"""Generate EPF ECR or ESIC return file for the payroll entry.

	file_type: 'epf' → ECR text file, 'esi' → ESIC return text file.
	manual_rows: JSON string of list of {uan, name, gross, epf_wages, ncp_days}
	             for employees without salary slips (e.g. exited employees).
	Returns {success, file_url, filename, rows}.
	"""
	pe = frappe.get_doc("Payroll Entry", payroll_entry_name)
	company = pe.company

	# Get all submitted salary slips for this payroll entry
	slips = frappe.db.sql("""
		SELECT name, employee, employee_name, gross_pay, payment_days,
		       total_working_days, start_date, end_date
		FROM `tabSalary Slip`
		WHERE payroll_entry = %s AND docstatus = 1
		ORDER BY employee_name
	""", (payroll_entry_name,), as_dict=True)

	# Parse manual rows (for employees without slips, e.g. exited employees)
	manual = []
	if manual_rows:
		import json
		manual = json.loads(manual_rows) if isinstance(manual_rows, str) else manual_rows

	if not slips and not manual:
		frappe.throw(_("No submitted salary slips found for this Payroll Entry"))

	if file_type == "epf":
		return _generate_epf_ecr(pe, slips, company, manual)
	elif file_type == "esi":
		return _generate_esi_return(pe, slips, company)
	else:
		frappe.throw(_("Invalid file_type: must be 'epf' or 'esi'"))


def _generate_epf_ecr(pe, slips, company, manual_rows=None):
	"""Generate EPF ECR 2.0 (Electronic Challan cum Return) text file.

	ECR 2.0 format: #~# delimited, 11 fields per row, no header rows.
	Fields: UAN, Name, Gross, EPF Wages, EPS Wages, EDLI Wages,
	        EE Share, EPS Share, ER Share, NCP, Refund.
	Only employees with PF - Employee deduction and a UAN are included.
	manual_rows: list of dicts with {uan, name, gross, epf_wages, ncp_days}
	             for employees without salary slips (e.g. exited employees).
	"""
	PF_EMPLOYEE_DED = "PF - Employee"
	BASIC = "Basic"
	DA = "Dearness Allowance"
	EPF_WAGE_CAP = 15000  # PF wage ceiling
	DELIM = "#~#"

	rows = []
	summary = {"epf_wages": 0, "ee_share": 0, "eps_share": 0, "er_share": 0}

	for s in slips:
		slip = frappe.get_doc("Salary Slip", s.name)
		pf_employee_ded = 0
		basic = 0
		da = 0

		for d in slip.deductions:
			if d.salary_component == PF_EMPLOYEE_DED:
				pf_employee_ded = flt(d.amount, 2)
		for e in slip.earnings:
			if e.salary_component == BASIC:
				basic = flt(e.amount, 2)
			if e.salary_component == DA:
				da = flt(e.amount, 2)

		# Skip employees with no PF deduction
		if pf_employee_ded <= 0:
			continue

		# Get employee UAN
		emp = frappe.get_doc("Employee", s.employee)
		uan = emp.custom_uan_number or ""
		if not uan:
			continue  # Skip employees without UAN

		# EPF wages derived from actual PF deduction (not Basic+DA), capped at 15000.
		# Company pays PF on full basic (above ceiling), so pf_ded/0.12 gives actual
		# PF wages. ECR reports only the capped (statutory) portion.
		epf_wages = min(pf_employee_ded / 0.12, EPF_WAGE_CAP)
		epf_wages = int(round(epf_wages))

		# EPS wages = same as EPF wages (pension wages)
		eps_wages = epf_wages

		# EDLI wages = same as EPF wages
		edli_wages = epf_wages

		# EE Share (Employee) = 12% of EPF wages
		ee_share = int(round(epf_wages * 0.12))
		# EPS Share (Pension) = 8.33% of EPF wages
		eps_share = int(round(epf_wages * 0.0833))
		# ER Share (Employer PF) = EE Share - EPS Share = 3.67%
		er_share = ee_share - eps_share

		# NCP days = total_working_days - payment_days
		ncp_days = flt(s.total_working_days or 30) - flt(s.payment_days or 30)
		ncp_days = int(ncp_days) if ncp_days > 0 else 0

		# Member name (clean up extra spaces)
		member_name = " ".join(s.employee_name.split())

		# Gross wages
		gross = int(round(flt(s.gross_pay, 2)))

		# ECR 2.0 row: #~# delimited, 11 fields
		row = DELIM.join([
			uan,              # UAN
			member_name,      # Name
			str(gross),       # Gross Wages
			str(epf_wages),   # EPF Wages
			str(eps_wages),   # EPS Wages
			str(edli_wages),  # EDLI Wages
			str(ee_share),    # EE Share (Employee 12%)
			str(eps_share),   # EPS Share (Pension 8.33%)
			str(er_share),    # ER Share (Employer 3.67%)
			str(ncp_days),    # NCP Days
			"0",              # Refund of Advances
		])
		rows.append(row)

		summary["epf_wages"] += epf_wages
		summary["ee_share"] += ee_share
		summary["eps_share"] += eps_share
		summary["er_share"] += er_share

	# Process manual rows (employees without salary slips, e.g. exited employees)
	if manual_rows:
		for m in manual_rows:
			uan = (m.get("uan") or "").strip()
			member_name = " ".join((m.get("name") or "").split())
			gross = int(round(flt(m.get("gross"), 2)))
			epf_wages = int(round(flt(m.get("epf_wages"), 2)))
			ncp_days = int(flt(m.get("ncp_days"), 0))

			if not uan or not member_name or epf_wages <= 0:
				continue

			# EPS/EDLI wages capped at 15000
			eps_wages = min(epf_wages, EPF_WAGE_CAP)
			edli_wages = min(epf_wages, EPF_WAGE_CAP)

			ee_share = int(round(epf_wages * 0.12))
			eps_share = int(round(epf_wages * 0.0833))
			er_share = ee_share - eps_share

			row = DELIM.join([
				uan,
				member_name,
				str(gross),
				str(epf_wages),
				str(eps_wages),
				str(edli_wages),
				str(ee_share),
				str(eps_share),
				str(er_share),
				str(ncp_days),
				"0",
			])
			rows.append(row)

			summary["epf_wages"] += epf_wages
			summary["ee_share"] += ee_share
			summary["eps_share"] += eps_share
			summary["er_share"] += er_share

	if not rows:
		frappe.throw(_("No PF-eligible employees with UAN found in submitted salary slips"))

	# ECR 2.0: no header rows, just data rows
	content = "\n".join(rows) + "\n"

	# Generate filename
	month_year = frappe.utils.formatdate(pe.start_date, "MM-yyyy")
	filename = f"ECR_{company[:10].replace(' ', '_')}_{month_year}.txt"

	# Save as a File in Frappe
	file_url = _save_return_file(content, filename, pe.name)

	# Also return content as base64 for direct browser download
	import base64
	content_b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")

	return {
		"success": True,
		"file_url": file_url,
		"filename": filename,
		"rows": len(rows),
		"summary": summary,
		"content_b64": content_b64,
	}


def _generate_esi_return(pe, slips, company):
	"""Generate ESIC return text file.

	ESIC format: # delimited, one row per IP (Insured Person).
	Only employees with ESI deduction and an ESIC number are included.
	"""
	ESI_COMPONENTS = ["Employee State Insurance", "Employee State Insurance deduction"]
	ESI_WAGE_CAP = 21000  # ESI wage ceiling (monthly gross)

	rows = []
	summary = {"esi_wages": 0, "esi_employee": 0, "esi_employer": 0}

	for s in slips:
		slip = frappe.get_doc("Salary Slip", s.name)
		esi_amount = 0

		for d in slip.deductions:
			if d.salary_component in ESI_COMPONENTS:
				esi_amount += flt(d.amount, 2)

		# Skip employees with no ESI deduction
		if esi_amount <= 0:
			continue

		# Get employee ESIC number
		emp = frappe.get_doc("Employee", s.employee)
		esic_no = emp.esic_number or ""
		if not esic_no:
			continue

		# ESI wages = Gross pay, capped at 21000
		esi_wages = min(flt(s.gross_pay, 2), ESI_WAGE_CAP)
		# Employee share = 0.75% of ESI wages
		esi_employee = flt(round(esi_wages * 0.0075, 2), 2)
		# Employer share = 3.25% of ESI wages
		esi_employer = flt(round(esi_wages * 0.0325, 2), 2)

		# NCP days
		ncp_days = flt(s.total_working_days or 30) - flt(s.payment_days or 30)
		ncp_days = int(ncp_days) if ncp_days > 0 else 0

		member_name = " ".join(s.employee_name.split())

		row = "#".join([
			esic_no,                      # ESIC IP Number
			member_name,                  # IP Name
			str(int(esi_wages)),          # ESI Wages
			str(esi_employee),            # Employee Share (0.75%)
			str(esi_employer),            # Employer Share (3.25%)
			str(ncp_days),                # NCP Days
			"0",                          # Arrears ESI Wages
			"0",                          # Arrears Employee Share
			"0",                          # Arrears Employer Share
		])
		rows.append(row)

		summary["esi_wages"] += esi_wages
		summary["esi_employee"] += esi_employee
		summary["esi_employer"] += esi_employer

	if not rows:
		frappe.throw(_("No ESI-eligible employees with ESIC number found in submitted salary slips"))

	# Build ESIC file content
	header1 = "#".join(["ESIC"] * 9)
	header2 = "#".join([
		"IP Number", "IP Name", "ESI Wages",
		"Employee Share", "Employer Share", "NCP Days",
		"Arrears ESI Wages", "Arrears Employee Share", "Arrears Employer Share",
	])

	content = header1 + "\n" + header2 + "\n" + "\n".join(rows) + "\n"

	month_year = frappe.utils.formatdate(pe.start_date, "MM-yyyy")
	filename = f"ESIC_{company[:10].replace(' ', '_')}_{month_year}.txt"

	file_url = _save_return_file(content, filename, pe.name)

	import base64
	content_b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")

	return {
		"success": True,
		"file_url": file_url,
		"filename": filename,
		"rows": len(rows),
		"summary": summary,
		"content_b64": content_b64,
	}


def _save_return_file(content, filename, payroll_entry_name):
	"""Save text content directly to public/files and create a minimal File record.

	Writes the file directly to disk and inserts a File record via SQL,
	bypassing the slow File doctype validate/on_update hooks.
	"""
	import os
	from frappe.utils import get_files_path

	# Delete any existing File record with the same name for this Payroll Entry
	existing = frappe.db.get_value("File", {
		"attached_to_doctype": "Payroll Entry",
		"attached_to_name": payroll_entry_name,
		"file_name": filename,
	}, "name")
	if existing:
		try:
			frappe.delete_doc("File", existing, ignore_permissions=True, force=True)
			frappe.db.commit()
		except Exception:
			frappe.db.rollback()

	# Ensure unique filename
	unique_suffix = frappe.utils.random_string(6)
	base, ext = os.path.splitext(filename)
	unique_filename = f"{base}{unique_suffix}{ext}"
	file_path_disk = os.path.join(get_files_path(), unique_filename)
	with open(file_path_disk, "w", encoding="utf-8") as f:
		f.write(content)

	file_url = f"/files/{unique_filename}"

	# Insert minimal File record via SQL (bypassing slow hooks)
	frappe.db.sql("""
		INSERT INTO `tabFile`
			(name, file_name, file_url, is_private, is_folder, attached_to_doctype,
			 attached_to_name, folder, creation, modified, modified_by, owner, docstatus)
		VALUES (%s, %s, %s, 0, 0, %s, %s, 'Home', NOW(), NOW(), %s, %s, 0)
	""", (
		unique_filename, unique_filename, file_url,
		"Payroll Entry", payroll_entry_name,
		frappe.session.user, frappe.session.user,
	))
	frappe.db.commit()

	return file_url


# ---------------------------------------------------------------------------
# Step 4: Payable & Expense Voucher Booking
# ---------------------------------------------------------------------------

@frappe.whitelist()
def book_payroll(payroll_entry_name):
	"""Submit salary slips + create the accrual Journal Entry.

	Idempotent: if slips are already submitted and a JE exists, returns the
	existing JE. Otherwise submits draft slips and creates the accrual JE.

	Also handles the case where slips were submitted outside this function
	(e.g. via ERPNext bulk submit) but no accrual JE was created — in that
	case, the JE is created for all already-submitted slips that lack one.
	"""
	pe = frappe.get_doc("Payroll Entry", payroll_entry_name)
	if pe.docstatus == 2:
		frappe.throw(_("Payroll Entry {0} is cancelled").format(payroll_entry_name))

	# Check if already booked — idempotency
	# JE is kept in Draft (docstatus=0) per Req 8
	# Only consider non-cancelled JEs (docstatus 0 or 1) as valid
	if cint(pe.salary_slips_submitted):
		je_name = frappe.db.get_value(
			"Journal Entry Account",
			{"reference_type": "Payroll Entry", "reference_name": payroll_entry_name},
			"parent",
		)
		if je_name:
			je_ds = frappe.db.get_value("Journal Entry", je_name, "docstatus")
			if je_ds is not None and je_ds != 2:
				return {"journal_entry": je_name, "already_booked": True}
			# JE is cancelled (docstatus=2) — clear stale journal_entry links
			# on slips so we can create a fresh accrual JE
			if je_ds == 2:
				frappe.db.sql(
					"""UPDATE `tabSalary Slip` SET journal_entry = ''
					WHERE payroll_entry = %s AND journal_entry = %s""",
					(payroll_entry_name, je_name),
				)

	# Get draft slips linked to this PE
	draft_slips = pe.get_sal_slip_list(ss_status=0)

	# If no slips linked to this PE, look for draft slips in the same period
	# (may be linked to a different/older Payroll Entry)
	if not draft_slips:
		draft_slips_raw = frappe.db.sql(
			"""
			SELECT name, salary_structure FROM `tabSalary Slip`
			WHERE start_date = %(start_date)s
			  AND end_date = %(end_date)s
			  AND company = %(company)s
			  AND docstatus = 0
			""",
			{
				"start_date": pe.start_date,
				"end_date": pe.end_date,
				"company": pe.company,
			},
		)
		# Re-link these slips to the current Payroll Entry
		for row in draft_slips_raw:
			frappe.db.set_value("Salary Slip", row[0], "payroll_entry", payroll_entry_name)
		draft_slips = draft_slips_raw

	# Get already-submitted slips (docstatus=1) for this PE/period that don't
	# have a JE linked yet. This handles the case where slips were submitted
	# via ERPNext's bulk submit (bypassing book_payroll), so no accrual JE
	# was created.
	already_submitted_slips = frappe.db.sql(
		"""
		SELECT name FROM `tabSalary Slip`
		WHERE start_date = %(start_date)s
		  AND end_date = %(end_date)s
		  AND company = %(company)s
		  AND docstatus = 1
		  AND (journal_entry IS NULL OR journal_entry = '')
		ORDER BY employee_name
		""",
		{
			"start_date": pe.start_date,
			"end_date": pe.end_date,
			"company": pe.company,
		},
		as_dict=True,
	)

	if not draft_slips and not already_submitted_slips:
		frappe.throw(_("No draft or unbooked submitted salary slips found for this Payroll Entry"))

	# Note: We do NOT submit the Payroll Entry here because HRMS's before_submit
	# validation rejects duplicate slips (including cancelled ones from prior runs).
	# The slips and JE can be created without submitting the PE itself.

	# Submit each draft slip individually (avoids the silent error-swallowing
	# in HRMS's submit_salary_slips_for_employees)
	frappe.flags.via_payroll_entry = True
	submitted_slips = []
	unsubmitted = []
	errors = []

	try:
		for entry in draft_slips:
			slip_name = entry[0] if isinstance(entry, (list, tuple)) else entry.get("name")
			slip = frappe.get_doc("Salary Slip", slip_name)
			if slip.net_pay < 0:
				unsubmitted.append(slip_name)
				continue
			try:
				slip.submit()
				submitted_slips.append(slip)
				frappe.db.commit()
			except Exception as e:
				frappe.db.rollback()
				unsubmitted.append(slip_name)
				errors.append(f"{slip_name}: {str(e)}")

		# Add already-submitted slips (submitted outside book_payroll) that
		# don't have a JE linked yet — they need to be included in the accrual JE
		for row in already_submitted_slips:
			slip = frappe.get_doc("Salary Slip", row["name"])
			if slip.net_pay >= 0:
				submitted_slips.append(slip)

		# Create the accrual JE directly with full control over party & cost center
		if submitted_slips:
			je_name = _make_accrual_je(pe, submitted_slips)
			# Link JE to salary slips
			for slip in submitted_slips:
				frappe.db.set_value("Salary Slip", slip.name, "journal_entry", je_name)
			pe.db_set({"salary_slips_submitted": 1, "status": "Submitted", "error_message": ""})
			frappe.db.commit()
	except Exception as e:
		frappe.db.rollback()
		frappe.throw(_("Payroll booking failed: {0}").format(str(e)))
	finally:
		frappe.flags.via_payroll_entry = False

	# je_name was set by _make_accrual_je above; no need to look it up
	# (the lookup by reference_type=Payroll Entry can find stale cancelled JEs)

	if errors:
		frappe.msgprint(
			_("Some slips could not be submitted:\n{0}").format("\n".join(errors[:5])),
			title=_("Partial Booking"),
			indicator="orange",
		)

	return {"journal_entry": je_name, "already_booked": False}


def _make_accrual_je(pe, submitted_slips):
	"""Create the accrual Journal Entry for submitted salary slips.

	Structure:
	  Debit:  Single entry to Salary expense account for total gross
	  Credit: Payroll Payable per employee (party) for their net pay
	  Credit: EPF Payable — aggregated PF - Employee deductions
	  Credit: ESI Payable — aggregated ESI deductions
	  Credit: Professional Taxes — aggregated PT deductions
	  Credit: Salary expense account — other deductions (Arrear, Loan, etc.)

	This produces a clean, compact JE with proper payable accounts.
	"""
	company = pe.company
	cost_center = pe.cost_center or _get_company_cost_center(company)
	payroll_payable_account = pe.payroll_payable_account or _get_payroll_payable_account(company)
	currency = _get_company_currency(company)
	precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

	# Override mapping: deduction component → proper payable account
	# These components currently map to "Salary - THIS" in Salary Component Account,
	# but for the accrual JE they should credit their respective payable accounts.
	DEDUCTION_ACCOUNT_OVERRIDE = {
		"PF - Employee": "EPF Payable",
		"Employee State Insurance": "ESI Payable",
		"Professional Tax": "Professional Tax",
	}

	def _resolve_deduction_account(comp, company):
		"""Return the proper payable account for a deduction component."""
		# Check override mapping first
		for key, pattern in DEDUCTION_ACCOUNT_OVERRIDE.items():
			if comp == key:
				# Find account matching the pattern in this company
				acct = frappe.db.sql(
					"""SELECT name FROM `tabAccount`
					WHERE company = %s AND account_name LIKE %s
					  AND is_group = 0
					LIMIT 1""",
					(company, "%%" + pattern + "%%"),
				)
				if acct:
					return acct[0][0]
				# Fall back to component's configured account
		return _get_component_account(comp, company)

	# Salary expense account — use the account from the first earning component
	salary_expense_account = None

	# Aggregate totals
	total_gross = 0
	employee_net_pay = {}  # {employee_id: {"net_pay": x, "employee_name": y}}
	# Aggregated deduction amounts by account (for single credit entries)
	deduction_by_account = {}  # {account: total_amount}

	for slip in submitted_slips:
		emp = slip.employee
		emp_name = slip.employee_name or frappe.db.get_value("Employee", emp, "employee_name") or ""

		for e in slip.earnings:
			comp = e.salary_component
			if _is_statistical_component(comp):
				continue
			if cint(e.do_not_include_in_total):
				continue
			amt = flt(e.amount, precision)
			total_gross += amt
			if not salary_expense_account:
				salary_expense_account = _get_component_account(comp, company)

		for d in slip.deductions:
			comp = d.salary_component
			if _is_statistical_component(comp):
				continue
			if cint(d.do_not_include_in_total):
				continue
			amt = flt(d.amount, precision)
			account = _resolve_deduction_account(comp, company)
			deduction_by_account[account] = amt + deduction_by_account.get(account, 0)

		employee_net_pay[emp] = {"net_pay": flt(slip.net_pay, precision), "name": emp_name}

	# Build JE account rows
	accounts = []

	# 1. Single Debit to Salary expense account for total gross
	if total_gross > 0 and salary_expense_account:
		accounts.append({
			"account": salary_expense_account,
			"debit_in_account_currency": flt(total_gross, precision),
			"cost_center": cost_center,
			"user_remark": "Total Gross Salary",
		})

	# 2. Credit Payroll Payable per employee (with party + name in remark)
	# Note: Do NOT set reference_type/reference_name here, otherwise ERPNext's
	# JE reconciliation validation considers these rows "already matched" and
	# blocks the payment JE from referencing this accrual JE.
	for emp, info in employee_net_pay.items():
		net_pay = info["net_pay"]
		emp_name = info["name"]
		if net_pay > 0:
			accounts.append({
				"account": payroll_payable_account,
				"credit_in_account_currency": flt(net_pay, precision),
				"cost_center": cost_center,
				"party_type": "Employee",
				"party": emp,
				"user_remark": emp_name,
			})

	# 3. Credit deduction payable accounts as single aggregated entries (no party)
	for account, amount in deduction_by_account.items():
		if amount > 0:
			accounts.append({
				"account": account,
				"credit_in_account_currency": flt(amount, precision),
				"cost_center": cost_center,
			})

	# Create the Journal Entry
	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Journal Entry"
	je.company = company
	je.posting_date = pe.end_date
	je.user_remark = _("Accrual Journal Entry for salaries from {0} to {1}").format(
		pe.start_date, pe.end_date
	)
	je.title = payroll_payable_account
	je.party_not_required = False
	je.custom_cost_center = cost_center
	je.set("accounts", accounts)
	je.save(ignore_permissions=True)

	return je.name


def _get_component_account(component, company):
	"""Return the account for a Salary Component for the given company."""
	account = frappe.db.get_value(
		"Salary Component Account",
		{"parent": component, "company": company},
		"account",
	)
	if not account:
		frappe.throw(
			_("Please set account in Salary Component {0} for company {1}").format(
				frappe.bold(component), frappe.bold(company)
			)
		)
	return account


def _is_statistical_component(component):
	"""Check if a Salary Component is statistical (e.g. employer contribution).

	Statistical components appear in the earnings/deductions table but are NOT
	part of gross_pay or net_pay. They should be excluded from the accrual JE.
	"""
	return cint(frappe.db.get_value("Salary Component", component, "statistical_component")) == 1


# ---------------------------------------------------------------------------
# Step 5: Dual-Mode Salary Release & Payout Integration
# ---------------------------------------------------------------------------

def _create_payment_je(slips, bank_account, payroll_entry_name, company,
					   start_date=None, end_date=None, reference_no=None,
					   reference_date=None):
	"""Create a Bank Entry JE for salary payment (Debit Payroll Payable, Credit Bank).

	Used by both release_payment (Manual/Automated) and release_bts (BTS mode)
	to ensure all payment modes create a JE linked to the Payroll Entry.
	The payment JE also references the existing payroll accrual JE via the
	custom_accrual_je field.

	Returns (je_name, total_amount, slip_amounts) where slip_amounts is
	{slip_name: amount}.
	"""
	payroll_payable_account = _get_payroll_payable_account(company, payroll_entry_name)
	cost_center = _get_company_cost_center(company)
	precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

	# Find the existing accrual JE created during payroll booking.
	# The salary slips store the accrual JE name in their journal_entry field.
	accrual_je = None
	if slips:
		accrual_je = frappe.db.get_value(
			"Salary Slip",
			{"name": ["in", [s.name for s in slips]]},
			"journal_entry",
		)
		# Verify it's a Journal Entry type JE and not cancelled
		if accrual_je:
			je_type, je_ds = frappe.db.get_value(
				"Journal Entry", accrual_je, ["voucher_type", "docstatus"]
			)
			if je_type != "Journal Entry" or je_ds == 2:
				accrual_je = None

	accounts = []
	total_amount = 0.0
	slip_amounts = {}

	for slip in slips:
		amount = flt(slip.rounded_total or slip.net_pay, precision)
		if amount <= 0:
			continue

		row = {
			"account": payroll_payable_account,
			"debit_in_account_currency": amount,
			"cost_center": cost_center,
			"party_type": "Employee",
			"party": slip.employee,
		}
		if accrual_je:
			row["reference_type"] = "Journal Entry"
			row["reference_name"] = accrual_je

		accounts.append(row)
		total_amount += amount
		slip_amounts[slip.name] = amount

	if not accounts:
		return None, 0.0, {}

	# Credit the Bank Account
	bank_gl_account = frappe.db.get_value("Bank Account", bank_account, "account")
	if not bank_gl_account:
		frappe.throw(_("No GL Account linked to Bank Account {0}").format(bank_account))

	accounts.append({
		"account": bank_gl_account,
		"credit_in_account_currency": total_amount,
		"bank_account": bank_account,
		"cost_center": cost_center,
	})

	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Bank Entry"
	je.company = company
	je.posting_date = nowdate()
	je.cheque_no = reference_no or ""
	je.cheque_date = reference_date or nowdate()
	remark = _("Payroll payout for {0} to {1}").format(start_date or "", end_date or "")
	if accrual_je:
		remark += f" | Accrual JE: {accrual_je}"
	je.user_remark = remark
	je.set("accounts", accounts)
	je.party_not_required = True
	je.custom_cost_center = cost_center
	je.save(ignore_permissions=True)
	# Keep JE in Draft — do not submit (Req 8)

	return je.name, total_amount, slip_amounts


def _mark_slips_paid(slips, je_name, slip_amounts):
	"""Mark salary slips as Paid and link the payment JE."""
	results = []
	for slip in slips:
		if slip.name not in slip_amounts:
			continue
		frappe.db.set_value("Salary Slip", slip.name, {
			"custom_payment_status": "Paid",
			"custom_payment_je": je_name,
		})
		results.append({
			"employee": slip.employee,
			"employee_name": slip.employee_name,
			"salary_slip": slip.name,
			"amount": slip_amounts[slip.name],
			"status": "Paid",
			"message": "Payment recorded via Bank Entry",
			"journal_entry": je_name,
		})
	return results


@frappe.whitelist()
def release_payment(
	employees,
	mode,
	bank_account,
	payroll_entry_name=None,
	company=None,
	start_date=None,
	end_date=None,
	reference_no=None,
	reference_date=None,
):
	"""Release salary payment to selected employees.

	mode: "Manual" or "Automated"
	 - Manual:   Create a Bank Entry JE (Debit Payroll Payable, Credit Bank),
	            mark slips as Paid.
	 - Automated: Same JE, then delegate to india_banking
	            (make_payment_order + make_payment) for real bank payout.

	Idempotent: skips slips already marked Paid.
	"""
	if isinstance(employees, str):
		employees = json.loads(employees)
	if not employees:
		frappe.throw(_("No employees selected for payment release"))
	if not company:
		company = frappe.db.get_value("Payroll Entry", payroll_entry_name, "company") if payroll_entry_name else None
	if not company:
		frappe.throw(_("Company is required"))

	# Gather submitted salary slips for these employees in the period
	slip_filters = {
		"employee": ["in", employees],
		"docstatus": 1,
		"custom_payment_status": ["!=", "Paid"],
	}
	if start_date and end_date:
		slip_filters["start_date"] = start_date
		slip_filters["end_date"] = end_date
	elif payroll_entry_name:
		slip_filters["payroll_entry"] = payroll_entry_name

	slips = frappe.get_all(
		"Salary Slip",
		filters=slip_filters,
		fields=["name", "employee", "employee_name", "net_pay", "rounded_total", "start_date", "end_date"],
	)

	if not slips:
		return {"journal_entry": None, "payment_order": None, "results": [], "message": "All selected slips are already paid or not submitted."}

	# For Automated mode, attach employee bank accounts to slip objects
	if mode == "Automated":
		for slip in slips:
			slip._emp_bank = _get_employee_bank_account(slip.employee)

	# Create the payment JE (Debit Payroll Payable, Credit Bank)
	je_name, total_amount, slip_amounts = _create_payment_je(
		slips, bank_account, payroll_entry_name, company,
		start_date=start_date, end_date=end_date,
		reference_no=reference_no, reference_date=reference_date,
	)

	if not je_name:
		return {"journal_entry": None, "payment_order": None, "results": [], "message": "No payable amounts found."}

	# Mark slips as Paid
	results = _mark_slips_paid(slips, je_name, slip_amounts)

	payment_order_name = None

	# Automated mode — delegate to india_banking
	if mode == "Automated":
		if not _india_banking_installed():
			frappe.throw(_("india_banking app is not installed. Cannot use Automated mode."))
		try:
			from india_banking.overrides.journal_entry import make_payment_order

			po = make_payment_order(je_name)
			po.posting_date = nowdate()
			# Set default mode of transfer (IMPS is common for salary)
			if not po.default_mode_of_transfer:
				po.default_mode_of_transfer = "IMPS"
			po.save(ignore_permissions=True)
			po.submit()
			payment_order_name = po.name

			# Initiate the bank payment
			from india_banking.india_banking.doctype.india_banking_connector.india_banking_connector import (
				make_payment,
			)

			make_payment(payment_order_name)

			# Read back per-employee status from Payment Order Summary
			summaries = frappe.get_all(
				"Payment Order Summary",
				{"parent": payment_order_name},
				["name", "party", "payment_status", "message", "reference_number"],
			)
			summary_map = {s.party: s for s in summaries}
			for r in results:
				s = summary_map.get(r["employee"])
				if s:
					r["status"] = s.payment_status or "Pending"
					r["message"] = s.message or ""
					r["reference_number"] = s.reference_number or ""
					# Update slip payment status based on bank response
					if s.payment_status == "Processed":
						frappe.db.set_value("Salary Slip", r["salary_slip"], "custom_payment_status", "Paid")
					elif s.payment_status in ("Failed", "Rejected"):
						frappe.db.set_value("Salary Slip", r["salary_slip"], "custom_payment_status", "Unpaid")

		except Exception as e:
			frappe.log_error(
				title="Payroll Workbench: Automated payout failed",
				message=frappe.get_traceback(),
			)
			# Don't throw — return partial results with error info
			for r in results:
				if r["status"] == "Paid":
					r["status"] = "Bank Entry Created (Payout Failed)"
					r["message"] = str(e)

	return {
		"journal_entry": je_name,
		"payment_order": payment_order_name,
		"results": results,
	}


@frappe.whitelist()
def release_bts(
	employees,
	bank_account,
	payroll_entry_name=None,
	company=None,
	start_date=None,
	end_date=None,
	payment_date=None,
	reference_no=None,
	reference_date=None,
):
	"""Generate a Bank Transfer Sheet (BTS) Excel file for selected employees.

	The BTS is in the bank's bulk-payment upload format (PAB_VENDOR / IMPS).
	A "Bank - BTS" row is added/updated in the Statutory Report child table
	with the generated file attached in the `download_return` field.

	Also creates a payment Bank Entry JE (Debit Payroll Payable, Credit Bank)
	linked to the Payroll Entry, and marks the included slips as Paid —
	just like Manual/Automated payment modes.

	Only submitted (docstatus=1) salary slips that are NOT already Paid are
	included.  If a "Bank - BTS" row already exists in the Statutory Report,
	it is updated with the new file (no duplicate rows).
	"""
	import base64
	import io

	if isinstance(employees, str):
		employees = json.loads(employees)
	if not employees:
		frappe.throw(_("No employees selected for BTS generation"))
	if not bank_account:
		frappe.throw(_("Company Bank Account is required for BTS"))
	if not company:
		company = (
			frappe.db.get_value("Payroll Entry", payroll_entry_name, "company")
			if payroll_entry_name
			else None
		)
	if not company:
		frappe.throw(_("Company is required"))

	# Company debit account number
	debit_acc_no = frappe.db.get_value("Bank Account", bank_account, "bank_account_no")
	if not debit_acc_no:
		frappe.throw(_("No bank account number found on Bank Account {0}").format(bank_account))

	# Payment date — default today; format DD-MM-YYYY per bank template
	pmt_date = getdate(payment_date) if payment_date else getdate(nowdate())
	pmt_date_str = pmt_date.strftime("%d-%m-%Y")

	# Gather submitted, non-paid salary slips for the selected employees
	slip_filters = {
		"employee": ["in", employees],
		"docstatus": 1,
		"custom_payment_status": ["!=", "Paid"],
	}
	if start_date and end_date:
		slip_filters["start_date"] = start_date
		slip_filters["end_date"] = end_date
	elif payroll_entry_name:
		slip_filters["payroll_entry"] = payroll_entry_name

	slips = frappe.get_all(
		"Salary Slip",
		filters=slip_filters,
		fields=[
			"name", "employee", "employee_name",
			"net_pay", "rounded_total",
		],
		order_by="employee_name",
	)

	if not slips:
		return {
			"file_url": None,
			"row_count": 0,
			"message": "No eligible (submitted, unpaid) salary slips found for the selected employees.",
		}

	# Fetch employee bank details
	emp_names = [s.employee for s in slips]
	emp_bank = frappe.db.sql(
		"""
		SELECT name, employee_name, bank_ac_no, ifsc_code
		FROM `tabEmployee`
		WHERE name IN %s
		""",
		(tuple(emp_names),),
		as_dict=True,
	)
	emp_map = {e.name: e for e in emp_bank}

	# Build BTS rows
	bts_rows = []
	skipped = []
	for slip in slips:
		emp = emp_map.get(slip.employee)
		if not emp:
			skipped.append({"employee": slip.employee, "reason": "Employee record not found"})
			continue
		if not emp.bank_ac_no:
			skipped.append({"employee": slip.employee, "reason": "No bank account number on employee"})
			continue
		if not emp.ifsc_code:
			skipped.append({"employee": slip.employee, "reason": "No IFSC code on employee"})
			continue

		amount = flt(slip.rounded_total or slip.net_pay, 2)
		if amount <= 0:
			skipped.append({"employee": slip.employee, "reason": "Net payable is zero or negative"})
			continue

		bts_rows.append({
			"slip_name": slip.name,
			"PYMT_PROD_TYPE_CODE": "PAB_VENDOR",
			"PYMT_MODE": "IMPS",
			"DEBIT_ACC_NO": debit_acc_no,
			"BNF_NAME": emp.employee_name,
			"BENE_ACC_NO": emp.bank_ac_no,
			"BENE_IFSC": emp.ifsc_code,
			"AMOUNT": amount,
			"DEBIT_NARR": "Salary ",
			"CREDIT_NARR": "Salary",
			"MOBILE_NUM": "",
			"EMAIL_ID": "",
			"REMARK": "",
			"PYMT_DATE": pmt_date_str,
			"REF_NO": "",
			"ADDL_INFO1": "",
			"ADDL_INFO2": "",
			"ADDL_INFO3": "",
			"ADDL_INFO4": "",
			"ADDL_INFO5": "",
		})

	if not bts_rows:
		return {
			"file_url": None,
			"row_count": 0,
			"skipped": skipped,
			"message": "No employees with complete bank details found.",
		}

	# Generate Excel file with openpyxl
	try:
		from openpyxl import Workbook
	except ImportError:
		frappe.throw(_("openpyxl library is required to generate BTS file"))

	wb = Workbook()
	ws = wb.active
	ws.title = "Sheet1"

	# Header row
	headers = [
		"PYMT_PROD_TYPE_CODE", "PYMT_MODE", "DEBIT_ACC_NO", "BNF_NAME",
		"BENE_ACC_NO", "BENE_IFSC", "AMOUNT", "DEBIT_NARR", "CREDIT_NARR",
		"MOBILE_NUM", "EMAIL_ID", "REMARK", "PYMT_DATE", "REF_NO",
		"ADDL_INFO1", "ADDL_INFO2", "ADDL_INFO3", "ADDL_INFO4", "ADDL_INFO5",
	]
	ws.append(headers)

	for row in bts_rows:
		ws.append([row[h] for h in headers])

	# Write to in-memory buffer
	buf = io.BytesIO()
	wb.save(buf)
	buf.seek(0)
	file_content = buf.read()
	buf.close()

	# Save file directly to public/files directory (bypass File doctype which is very slow)
	import os
	from frappe.utils import get_files_path

	period_label = ""
	if start_date and end_date:
		period_label = f"_{start_date}_to_{end_date}"
	filename = f"BTS_{payment_date or nowdate()}{period_label}.xlsx"

	# Ensure unique filename to avoid collisions
	unique_suffix = frappe.utils.random_string(6)
	base, ext = os.path.splitext(filename)
	unique_filename = f"{base}{unique_suffix}{ext}"
	file_path_disk = os.path.join(get_files_path(), unique_filename)
	with open(file_path_disk, "wb") as f:
		f.write(file_content)

	file_url = f"/files/{unique_filename}"

	# Insert a minimal File record directly via SQL (bypassing slow validate/on_update hooks)
	file_id = frappe.db.sql("""
		INSERT INTO `tabFile`
			(name, file_name, file_url, is_private, is_folder, attached_to_doctype,
			 attached_to_name, folder, creation, modified, modified_by, owner, docstatus)
		VALUES (%s, %s, %s, 0, 0, %s, %s, 'Home', NOW(), NOW(), %s, %s, 0)
	""", (
		unique_filename, unique_filename, file_url,
		"Payroll Entry", payroll_entry_name or "",
		frappe.session.user, frappe.session.user,
	))
	frappe.db.commit()

	# Update or create a "Bank - BTS" row in the Statutory Report child table.
	# If a "Bank - BTS" row already exists, update its download_return file URL
	# instead of appending a duplicate row.
	if payroll_entry_name:
		# Use DB query to avoid caching issues with pe.get()
		existing_bts_name = frappe.db.get_value(
			"Statutory Report",
			{"parent": payroll_entry_name, "parenttype": "Payroll Entry", "title": "Bank - BTS"},
			"name",
		)

		if existing_bts_name:
			# Update existing row's file URL
			frappe.db.set_value("Statutory Report", existing_bts_name, {
				"download_return": file_url,
				"status": "Completed",
			})
			frappe.db.commit()
		else:
			pe_ds = frappe.db.get_value("Payroll Entry", payroll_entry_name, "docstatus")
			if pe_ds == 1:
				# Submitted PE — insert child row directly
				new_row = frappe.get_doc({
					"doctype": "Statutory Report",
					"parent": payroll_entry_name,
					"parenttype": "Payroll Entry",
					"parentfield": "custom_statutory_report",
					"title": "Bank - BTS",
					"download_return": file_url,
					"upload_challan": "",
					"upload_payment": "",
					"status": "Completed",
				})
				new_row.insert(ignore_permissions=True)
				frappe.db.commit()
			else:
				pe = frappe.get_doc("Payroll Entry", payroll_entry_name)
				pe.append("custom_statutory_report", {
					"title": "Bank - BTS",
					"download_return": file_url,
					"upload_challan": "",
					"upload_payment": "",
					"status": "Completed",
				})
				pe.save(ignore_permissions=True)
				frappe.db.commit()

	# Create the payment JE (Debit Payroll Payable, Credit Bank) linked to
	# the Payroll Entry, and mark the included slips as Paid — same as
	# Manual/Automated payment modes.
	je_name = None
	paid_slip_names = [s["slip_name"] for s in bts_rows if s.get("slip_name")]
	paid_slips = [s for s in slips if s.name in paid_slip_names]
	if paid_slips:
		je_name, total_je_amount, slip_amounts = _create_payment_je(
			paid_slips, bank_account, payroll_entry_name, company,
			start_date=start_date, end_date=end_date,
			reference_no=reference_no or f"BTS-{pmt_date_str}",
			reference_date=reference_date or payment_date or nowdate(),
		)
		if je_name:
			_mark_slips_paid(paid_slips, je_name, slip_amounts)

	return {
		"file_url": file_url,
		"journal_entry": je_name,
		"row_count": len(bts_rows),
		"skipped": skipped,
		"debit_acc_no": debit_acc_no,
		"payment_date": pmt_date_str,
		"message": f"BTS generated with {len(bts_rows)} employee(s)." + (f" JE: {je_name}" if je_name else ""),
	}


# ---------------------------------------------------------------------------
# Step 5b: Statutory Payment Release (EPF / ESI)
# ---------------------------------------------------------------------------

# Mapping of statutory payment type → config
# Each entry: payable_account_field, component_names (employee + employer)
_STATUTORY_CONFIG = {
	"EPF": {
		"components": ["PF - Employee", "PF - Employer"],
		"payable_account": "EPF Payable - {company_short}",
		"label": "EPF (Provident Fund)",
	},
	"ESI": {
		"components": ["Employee State Insurance"],
		"payable_account": "ESI Payable - {company_short}",
		"label": "ESI (Employee State Insurance)",
	},
}


def _get_company_short_name(company):
	"""Extract a short identifier from the company name for account suffix matching.
	e.g. 'TEAMPRO HR & IT Services Pvt. Ltd.' → 'THIS'
	"""
	# Try the actual abbreviation stored on the company
	abbr = frappe.db.get_value("Company", company, "abbr")
	if abbr:
		return abbr
	return ""


def _find_account_by_suffix(suffix, company):
	"""Find an account ending with the given suffix for the company."""
	accounts = frappe.db.sql(
		"""
		SELECT name FROM `tabAccount`
		WHERE company = %s AND is_group = 0
		AND name LIKE %s
		ORDER BY name
		""",
		(company, f"%{suffix}%"),
		as_dict=True,
	)
	return accounts[0].name if accounts else None


@frappe.whitelist()
def get_statutory_payment_summary(payment_type, start_date, end_date, company, employees=None):
	"""Return the total statutory amount (EPF or ESI) from submitted salary slips
	in the given period, broken down by component.

	Returns:
		{total, by_component: [{component, amount, count}], slip_count}
	"""
	if isinstance(employees, str):
		employees = json.loads(employees)

	config = _STATUTORY_CONFIG.get(payment_type)
	if not config:
		frappe.throw(_("Unknown payment type: {0}").format(payment_type))

	conditions = ["ss.docstatus = 1", "ss.company = %(company)s"]
	params = {"company": company, "from_date": start_date, "to_date": end_date}

	# Use date overlap matching
	conditions.append("ss.start_date <= %(to_date)s AND ss.end_date >= %(from_date)s")

	if employees:
		conditions.append("ss.employee IN %(employees)s")
		params["employees"] = tuple(employees)

	comp_list = config["components"]
	conditions.append("sd.salary_component IN %(components)s")
	params["components"] = tuple(comp_list)

	rows = frappe.db.sql(
		f"""
		SELECT sd.salary_component, SUM(sd.amount) as amount, COUNT(DISTINCT ss.name) as slip_count
		FROM `tabSalary Detail` sd
		INNER JOIN `tabSalary Slip` ss ON sd.parent = ss.name
		WHERE {' AND '.join(conditions)}
		GROUP BY sd.salary_component
		""",
		params,
		as_dict=True,
	)

	by_component = []
	total = 0.0
	slip_count = 0
	for r in rows:
		by_component.append({
			"component": r.salary_component,
			"amount": flt(r.amount),
			"slip_count": r.slip_count,
		})
		total += flt(r.amount)
		slip_count = max(slip_count, r.slip_count)

	return {
		"payment_type": payment_type,
		"label": config["label"],
		"total": flt(total),
		"by_component": by_component,
		"slip_count": slip_count,
	}


@frappe.whitelist()
def release_statutory_payment(
	payment_type,
	bank_account,
	reference_no,
	reference_date,
	company,
	start_date=None,
	end_date=None,
	employees=None,
	payroll_entry_name=None,
):
	"""Create a Draft Journal Entry for statutory payment (EPF or ESI).

	Debit: Statutory Payable account (EPF Payable / ESI Payable)
	Credit: Bank Account

	The amount is calculated from submitted salary slips in the period,
	summing the relevant salary components (employee + employer contributions).

	The JE is kept in Draft (not submitted) per Req 8.
	"""
	if isinstance(employees, str):
		employees = json.loads(employees)
	if not company:
		company = frappe.db.get_value("Payroll Entry", payroll_entry_name, "company") if payroll_entry_name else None
	if not company:
		frappe.throw(_("Company is required"))

	config = _STATUTORY_CONFIG.get(payment_type)
	if not config:
		frappe.throw(_("Unknown payment type: {0}").format(payment_type))

	# Get the summary of amounts
	summary = get_statutory_payment_summary(
		payment_type, start_date, end_date, company, employees
	)

	total_amount = flt(summary["total"])
	if total_amount <= 0:
		return {
			"journal_entry": None,
			"message": f"No {config['label']} amount found in submitted salary slips for this period.",
			"total": 0,
		}

	# Find the payable account
	company_abbr = _get_company_short_name(company)
	payable_account = None
	if company_abbr:
		# Try "EPF Payable - THIS" pattern
		payable_account = _find_account_by_suffix(f"Payable - {company_abbr}", company)
		# More specific: try the exact payable account name
		if payment_type == "EPF":
			payable_account = frappe.db.get_value(
				"Account",
				{"company": company, "is_group": 0, "name": ["like", f"%EPF%Payable%{company_abbr}%"]},
				"name",
			) or frappe.db.get_value(
				"Account",
				{"company": company, "is_group": 0, "name": ["like", f"%EPF%{company_abbr}%"]},
				"name",
			)
		elif payment_type == "ESI":
			payable_account = frappe.db.get_value(
				"Account",
				{"company": company, "is_group": 0, "name": ["like", f"%ESI%Payable%{company_abbr}%"]},
				"name",
			) or frappe.db.get_value(
				"Account",
				{"company": company, "is_group": 0, "name": ["like", f"%ESI%{company_abbr}%"]},
				"name",
			)

	if not payable_account:
		frappe.throw(
			_("Could not find a Payable account for {0}. Please ensure an account like 'EPF Payable - {1}' or 'ESI Payable - {1}' exists.")
			.format(config["label"], company_abbr or "ABBR")
		)

	# Get the bank GL account
	bank_gl_account = frappe.db.get_value("Bank Account", bank_account, "account")
	if not bank_gl_account:
		frappe.throw(_("No GL Account linked to Bank Account {0}").format(bank_account))

	cost_center = _get_company_cost_center(company)
	precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

	# Build JE: Debit Payable, Credit Bank
	accounts = [
		{
			"account": payable_account,
			"debit_in_account_currency": flt(total_amount, precision),
			"cost_center": cost_center,
		},
		{
			"account": bank_gl_account,
			"credit_in_account_currency": flt(total_amount, precision),
			"bank_account": bank_account,
			"cost_center": cost_center,
		},
	]

	# Build remark with component breakdown
	remark_parts = [f"{c['component']}: {fmt_money_for_remark(c['amount'])}" for c in summary["by_component"]]
	remark = _("{0} payment for salaries {1} to {2} ({3})").format(
		config["label"],
		start_date or "",
		end_date or "",
		", ".join(remark_parts),
	)

	# Create the JE in Draft (not submitted — Req 8)
	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Bank Entry"
	je.company = company
	je.posting_date = nowdate()
	je.cheque_no = reference_no or ""
	je.cheque_date = reference_date or nowdate()
	je.user_remark = remark
	je.set("accounts", accounts)
	je.party_not_required = True
	je.custom_cost_center = cost_center
	je.save(ignore_permissions=True)

	return {
		"journal_entry": je.name,
		"total": total_amount,
		"payable_account": payable_account,
		"by_component": summary["by_component"],
		"message": f"{config['label']} payment JE created in Draft for {fmt_money_for_remark(total_amount)}",
	}


def fmt_money_for_remark(amount):
	"""Format a number for use in JE remarks."""
	return f"{flt(amount):.2f}"


@frappe.whitelist()
def get_payout_status(payment_order_name):
	"""Poll the Payment Order Summary for per-row payout status updates."""
	summaries = frappe.get_all(
		"Payment Order Summary",
		{"parent": payment_order_name},
		["name", "party", "party_type", "payment_status", "message", "reference_number", "payment_date"],
	)
	results = []
	for s in summaries:
		if s.party_type == "Employee":
			results.append(
				{
					"employee": s.party,
					"status": s.payment_status or "Pending",
					"message": s.message or "",
					"reference_number": s.reference_number or "",
					"payment_date": str(s.payment_date) if s.payment_date else "",
				}
			)
			# Sync slip status
			if s.payment_status == "Processed":
				frappe.db.set_value(
					"Salary Slip",
					{"employee": s.party, "custom_payment_je": ["is", "set"]},
					"custom_payment_status",
					"Paid",
				)
			elif s.payment_status in ("Failed", "Rejected"):
				frappe.db.set_value(
					"Salary Slip",
					{"employee": s.party, "custom_payment_je": ["is", "set"]},
					"custom_payment_status",
					"Unpaid",
				)
	return results


# ---------------------------------------------------------------------------
# Utility: get bank accounts for the company (for the Manual mode picker)
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_company_bank_accounts(company):
	"""Return Bank Accounts linked to the company for the payment release picker."""
	accounts = frappe.get_all(
		"Bank Account",
		{"company": company, "is_company_account": 1},
		["name", "bank", "bank_account_no", "account_name", "is_default"],
		order_by="is_default desc, modified desc",
	)
	return accounts


@frappe.whitelist()
def get_companies():
	"""Return all companies for the filter dropdown."""
	return frappe.get_all("Company", ["name", "abbr"], order_by="name")


@frappe.whitelist()
def _debug_setup():
	"""Debug: check existing setup for the new features."""
	company = "TEAMPRO HR & IT Services Pvt. Ltd."
	out = {}

	# 1. Salary Components
	out["components"] = frappe.db.sql(
		"""
		SELECT name, type, statistical_component, do_not_include_in_total
		FROM `tabSalary Component`
		ORDER BY name
		""",
		as_dict=True,
	)

	# 2. Component accounts for THIS company
	out["component_accounts"] = frappe.db.sql(
		"""
		SELECT sca.parent as component, sca.account
		FROM `tabSalary Component Account` sca
		WHERE sca.company = %s
		ORDER BY sca.parent
		""",
		[company],
		as_dict=True,
	)

	# 3. PF/ESI/PT payable accounts
	out["payable_accounts"] = frappe.db.sql(
		"""
		SELECT name, account_name, account_type, parent_account
		FROM `tabAccount`
		WHERE company = %s
		  AND (account_name LIKE '%%PF%%' OR account_name LIKE '%%ESI%%'
		       OR account_name LIKE '%%Provident%%' OR account_name LIKE '%%Professional Tax%%'
		       OR account_name LIKE '%%Payable%%')
		ORDER BY name
		""",
		[company],
		as_dict=True,
	)

	# 4. Active Salary Structures
	out["salary_structures"] = frappe.db.sql(
		"""
		SELECT name, is_active, company, payroll_frequency
		FROM `tabSalary Structure`
		WHERE is_active = 'Yes'
		ORDER BY name
		""",
		as_dict=True,
	)

	# 5. Check for Arrear Salary component
	out["arrear_component"] = frappe.db.get_value(
		"Salary Component", "Arrear Salary",
		["name", "type", "statistical_component", "do_not_include_in_total"],
		as_dict=True,
	)

	# 6. CFO user - check for users with CFO role
	out["cfo_users"] = frappe.db.sql(
		"""
		SELECT u.name, u.email, u.full_name, r.role
		FROM `tabUser` u
		INNER JOIN `tabHas Role` r ON r.parent = u.name
		WHERE r.role IN ('CFO', 'Accounts Manager', 'Accounts User')
		  AND u.enabled = 1
		ORDER BY u.name
		""",
		as_dict=True,
	)

	# 7. Holiday Lists
	out["holiday_lists"] = frappe.db.sql(
		"""
		SELECT name, from_date, to_date
		FROM `tabHoliday List`
		ORDER BY name
		""",
		as_dict=True,
	)

	return out


# ---------------------------------------------------------------------------
# Statutory Report child table
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_statutory_report(payroll_entry_name):
	"""Return the Statutory Report child table rows for a Payroll Entry.

	If no rows exist, returns 3 default rows (Bank - BTS, EPF, ESI) with
	status=Pending — but does NOT save them (the caller can save via
	save_statutory_report if desired).
	"""
	if not payroll_entry_name:
		return []

	rows = frappe.db.sql(
		"""
		SELECT name, title, download_return, upload_challan,
		       upload_payment, status
		FROM `tabStatutory Report`
		WHERE parent = %s AND parenttype = 'Payroll Entry'
		ORDER BY idx
		""",
		(payroll_entry_name,),
		as_dict=True,
	)

	if not rows:
		# Return default rows (not saved)
		rows = [
			{"title": "Bank - BTS", "download_return": "", "upload_challan": "",
			 "upload_payment": "", "status": "Pending"},
			{"title": "EPF", "download_return": "", "upload_challan": "",
			 "upload_payment": "", "status": "Pending"},
			{"title": "ESI", "download_return": "", "upload_challan": "",
			 "upload_payment": "", "status": "Pending"},
		]

	return rows


@frappe.whitelist()
def save_statutory_report(payroll_entry_name, rows):
	"""Save the Statutory Report child table rows for a Payroll Entry.

	`rows` is a list of dicts with keys: title, download_return,
	upload_challan, upload_payment, status.
	If a row has a `name` that starts with the doctype prefix, it's an
	existing row to update; otherwise it's a new row.
	"""
	if isinstance(rows, str):
		rows = json.loads(rows)

	pe = frappe.get_doc("Payroll Entry", payroll_entry_name)
	if pe.docstatus == 1:
		# Submitted PE — delete all existing rows, then re-insert
		frappe.db.delete("Statutory Report", {
			"parent": payroll_entry_name,
			"parenttype": "Payroll Entry",
		})
		frappe.db.commit()

		for idx, row in enumerate(rows, 1):
			new_row = frappe.get_doc({
				"doctype": "Statutory Report",
				"parent": payroll_entry_name,
				"parenttype": "Payroll Entry",
				"parentfield": "custom_statutory_report",
				"idx": idx,
				"title": row.get("title", ""),
				"download_return": row.get("download_return", ""),
				"upload_challan": row.get("upload_challan", ""),
				"upload_payment": row.get("upload_payment", ""),
				"status": row.get("status", "Pending"),
			})
			new_row.insert(ignore_permissions=True)
		frappe.db.commit()
	else:
		# Draft PE — replace all child rows
		pe.set("custom_statutory_report", [])
		for row in rows:
			pe.append("custom_statutory_report", {
				"title": row.get("title", ""),
				"download_return": row.get("download_return", ""),
				"upload_challan": row.get("upload_challan", ""),
				"upload_payment": row.get("upload_payment", ""),
				"status": row.get("status", "Pending"),
			})
		pe.save(ignore_permissions=True)
		frappe.db.commit()

	# Return the saved rows
	return get_statutory_report(payroll_entry_name)


# ---------------------------------------------------------------------------
# Attendance Approval (Payroll Period Approval doctype)
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_attendance_approval_status(company, start_date, end_date):
	"""Return the attendance approval record for the given period, if any."""
	row = frappe.db.sql(
		"""
		SELECT name, company, start_date, end_date, status,
		       requested_by, requested_on, approved_by, approved_on,
		       employee_count, total_payment_days, remarks
		FROM `tabPayroll Period Approval`
		WHERE company = %s AND start_date = %s AND end_date = %s
		  AND docstatus != 2
		ORDER BY creation DESC
		LIMIT 1
		""",
		(company, start_date, end_date),
		as_dict=True,
	)
	if not row:
		return {
			"approval_name": None,
			"status": None,
			"requested_by": None,
			"requested_on": None,
			"approved_by": None,
			"approved_on": None,
			"employee_count": 0,
			"total_payment_days": 0,
		}
	r = row[0]
	return {
		"approval_name": r.name,
		"status": r.status,
		"requested_by": r.requested_by,
		"requested_on": r.requested_on,
		"approved_by": r.approved_by,
		"approved_on": r.approved_on,
		"employee_count": r.employee_count or 0,
		"total_payment_days": r.total_payment_days or 0,
	}


@frappe.whitelist()
def send_attendance_for_approval(company, start_date, end_date, employees=None, employee_count=None, total_payment_days=None, summary_data=None):
	"""Create or update a Payroll Period Approval record and set status to Pending for Approval."""
	existing = frappe.db.get_value(
		"Payroll Period Approval",
		{"company": company, "start_date": start_date, "end_date": end_date, "docstatus": ["!=", 2]},
		"name",
	)
	if existing:
		doc = frappe.get_doc("Payroll Period Approval", existing)
	else:
		doc = frappe.new_doc("Payroll Period Approval")
		doc.company = company
		doc.start_date = start_date
		doc.end_date = end_date

	doc.status = "Pending for Approval"
	doc.requested_by = frappe.session.user
	doc.requested_on = frappe.utils.now()
	# Derive employee_count and total_payment_days from parameters
	if employees and not employee_count:
		emp_list = employees if isinstance(employees, list) else json.loads(employees)
		employee_count = len(emp_list)
	if summary_data and isinstance(summary_data, dict):
		totals = summary_data.get("totals") or {}
		if not total_payment_days and totals.get("payment_days") is not None:
			total_payment_days = totals.get("payment_days")
	if employee_count is not None:
		doc.employee_count = cint(employee_count)
	if total_payment_days is not None:
		doc.total_payment_days = flt(total_payment_days)
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	return {
		"approval_name": doc.name,
		"status": doc.status,
		"message": "Attendance summary sent for approval.",
	}


@frappe.whitelist()
def approve_attendance_summary(approval_name):
	"""Approve the attendance summary — set status to Approved and submit all draft attendance."""
	doc = frappe.get_doc("Payroll Period Approval", approval_name)
	if doc.status == "Approved":
		return {"status": "Approved", "message": "Already approved."}

	doc.status = "Approved"
	doc.approved_by = frappe.session.user
	doc.approved_on = frappe.utils.now()
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	# Submit all draft attendance for employees in this period
	errors = []
	attendance_records = frappe.db.sql(
		"""
		SELECT name FROM `tabAttendance`
		WHERE company = %s AND attendance_date BETWEEN %s AND %s
		  AND docstatus = 0
		""",
		(doc.company, doc.start_date, doc.end_date),
		as_dict=True,
	)
	for att in attendance_records:
		try:
			att_doc = frappe.get_doc("Attendance", att.name)
			att_doc.submit()
		except Exception as e:
			errors.append(f"{att.name}: {str(e)}")

	return {
		"status": "Approved",
		"message": "Attendance summary approved.",
		"errors": errors,
	}


@frappe.whitelist()
def reject_attendance_summary(approval_name, remarks=None):
	"""Reject the attendance summary."""
	doc = frappe.get_doc("Payroll Period Approval", approval_name)
	doc.status = "Rejected"
	doc.remarks = remarks or ""
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	return {
		"status": "Rejected",
		"message": "Attendance summary rejected.",
	}


# ---------------------------------------------------------------------------
# Payroll Booking Approval (Payroll Booking Approval doctype)
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_payroll_booking_approval_status(company, start_date, end_date):
	"""Return the payroll booking approval record for the given period, if any."""
	row = frappe.db.sql(
		"""
		SELECT name, company, start_date, end_date, status,
		       requested_by, requested_on, approved_by, approved_on,
		       payroll_entry, employee_count, total_gross, total_net,
		       total_deductions, remarks
		FROM `tabPayroll Booking Approval`
		WHERE company = %s AND start_date = %s AND end_date = %s
		  AND docstatus != 2
		ORDER BY creation DESC
		LIMIT 1
		""",
		(company, start_date, end_date),
		as_dict=True,
	)
	if not row:
		return {
			"approval_name": None,
			"status": None,
			"requested_by": None,
			"requested_on": None,
			"approved_by": None,
			"approved_on": None,
		}
	r = row[0]
	return {
		"approval_name": r.name,
		"status": r.status,
		"requested_by": r.requested_by,
		"requested_on": r.requested_on,
		"approved_by": r.approved_by,
		"approved_on": r.approved_on,
	}


@frappe.whitelist()
def send_payroll_for_approval(company, start_date, end_date, payroll_entry_name=None, summary_data=None, employee_count=None, total_gross=None, total_net=None, total_deductions=None):
	"""Create or update a Payroll Booking Approval record and set status to Pending for Approval."""
	existing = frappe.db.get_value(
		"Payroll Booking Approval",
		{"company": company, "start_date": start_date, "end_date": end_date, "docstatus": ["!=", 2]},
		"name",
	)
	if existing:
		doc = frappe.get_doc("Payroll Booking Approval", existing)
	else:
		doc = frappe.new_doc("Payroll Booking Approval")
		doc.company = company
		doc.start_date = start_date
		doc.end_date = end_date

	doc.status = "Pending for Approval"
	doc.requested_by = frappe.session.user
	doc.requested_on = frappe.utils.now()
	if payroll_entry_name:
		doc.payroll_entry = payroll_entry_name
	# Parse summary_data if passed as dict
	if summary_data and isinstance(summary_data, dict):
		totals = summary_data.get("totals") or {}
		emp_list = summary_data.get("employees") or []
		if not employee_count and emp_list:
			employee_count = len(emp_list)
		if not total_gross and totals.get("gross_pay") is not None:
			total_gross = totals.get("gross_pay")
		if not total_net and totals.get("net_pay") is not None:
			total_net = totals.get("net_pay")
		if not total_deductions and totals.get("custom_total_deduction") is not None:
			total_deductions = totals.get("custom_total_deduction")
	if employee_count is not None:
		doc.employee_count = cint(employee_count)
	if total_gross is not None:
		doc.total_gross = flt(total_gross)
	if total_net is not None:
		doc.total_net = flt(total_net)
	if total_deductions is not None:
		doc.total_deductions = flt(total_deductions)
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	return {
		"approval_name": doc.name,
		"status": doc.status,
		"message": "Payroll booking sent for approval.",
	}


@frappe.whitelist()
def approve_payroll_booking(approval_name):
	"""Approve the payroll booking — set status to Approved, submit all draft slips, and create accrual JE."""
	doc = frappe.get_doc("Payroll Booking Approval", approval_name)
	if doc.status == "Approved":
		return {"status": "Approved", "message": "Already approved.", "journal_entry": None, "already_booked": True}

	doc.status = "Approved"
	doc.approved_by = frappe.session.user
	doc.approved_on = frappe.utils.now()
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	# Submit all draft salary slips for this period
	errors = []
	je_name = None
	if doc.payroll_entry:
		slips = frappe.db.sql(
			"""
			SELECT name FROM `tabSalary Slip`
			WHERE payroll_entry = %s AND docstatus = 0
			""",
			(doc.payroll_entry,),
			as_dict=True,
		)
		for s in slips:
			try:
				slip = frappe.get_doc("Salary Slip", s.name)
				slip.submit()
			except Exception as e:
				errors.append(f"{s.name}: {str(e)}")

		# Create accrual JE
		try:
			je_name = book_payroll(doc.payroll_entry).get("journal_entry")
		except Exception as e:
			errors.append(f"JE creation: {str(e)}")

	return {
		"status": "Approved",
		"message": "Payroll booking approved.",
		"errors": errors,
		"journal_entry": je_name,
		"already_booked": False,
	}


@frappe.whitelist()
def reject_payroll_booking(approval_name, remarks=None):
	"""Reject the payroll booking."""
	doc = frappe.get_doc("Payroll Booking Approval", approval_name)
	doc.status = "Rejected"
	doc.remarks = remarks or ""
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	return {
		"status": "Rejected",
		"message": "Payroll booking rejected.",
	}


# ---------------------------------------------------------------------------
# Salary Revision Approval (Employee → Salary History table)
# ---------------------------------------------------------------------------

@frappe.whitelist()
def approve_salary_revision(employee, row_name):
	"""Approve a draft salary revision from the Employee's Salary History table.

	Creates a new Salary Structure Assignment with the revised base salary,
	updates the Salary History row to "Approved", and updates the Employee's
	gross_salary field.

	Args:
		employee: Employee ID
		row_name: Name of the Salary History child table row to approve
	"""
	from frappe.utils import getdate, nowdate

	emp = frappe.get_doc("Employee", employee)
	if emp.status == "Left":
		frappe.throw(_("Cannot approve salary revision for a left employee"))

	# Find the draft salary history row
	row = None
	for r in emp.salary_history_table:
		if r.name == row_name and r.status == "Draft":
			row = r
			break

	if not row:
		frappe.throw(_("Draft salary revision row {0} not found for employee {1}").format(
			row_name, employee))

	new_base = flt(row.new_salary)
	if new_base <= 0:
		frappe.throw(_("New salary must be greater than zero"))

	from_date = getdate(row.from_date)

	# Ensure from_date is not before the employee's date of joining
	doj = getdate(emp.date_of_joining) if emp.date_of_joining else None
	if doj and from_date < doj:
		from_date = doj

	# Get the current (latest) Salary Structure Assignment
	current_ssa = frappe.db.get_value(
		"Salary Structure Assignment",
		{"employee": employee, "docstatus": 1},
		["name", "salary_structure", "base", "from_date", "currency"],
		as_dict=True,
		order_by="from_date DESC",
	)

	# Determine which salary structure and currency to use
	if current_ssa:
		salary_structure = current_ssa.salary_structure
		currency = current_ssa.currency or "INR"
	else:
		# No existing SSA — find a suitable salary structure for the company
		# 1. Try the employee's custom_salary_structure field (must be submitted + active)
		salary_structure = None
		custom_ss = getattr(emp, "custom_salary_structure", None)
		if custom_ss:
			ss_ds, ss_active = frappe.db.get_value(
				"Salary Structure", custom_ss, ["docstatus", "is_active"]
			) or (None, None)
			if ss_ds == 1 and ss_active == "Yes":
				salary_structure = custom_ss

		# 2. Fall back to any active submitted salary structure for the company
		if not salary_structure:
			salary_structure = frappe.db.get_value(
				"Salary Structure",
				{"company": emp.company, "is_active": "Yes", "docstatus": 1},
				"name",
				order_by="modified DESC",
			)

		if not salary_structure:
			frappe.throw(_(
				"No active Salary Structure found for company {0}. "
				"Please create and submit a Salary Structure first."
			).format(emp.company))

		# Get currency from the salary structure's company default
		currency = frappe.db.get_value("Company", emp.company, "default_currency") or "INR"

	# Create a new Salary Structure Assignment with the revised base
	new_ssa = frappe.new_doc("Salary Structure Assignment")
	new_ssa.employee = employee
	new_ssa.salary_structure = salary_structure
	new_ssa.base = new_base
	new_ssa.from_date = from_date
	new_ssa.company = emp.company
	new_ssa.currency = currency
	new_ssa.docstatus = 0
	new_ssa.save(ignore_permissions=True)
	new_ssa.submit()

	# Update the Salary History row
	frappe.db.set_value("Salary History", row_name, {
		"status": "Approved",
		"approved_by": frappe.session.user,
		"approved_on": nowdate(),
		"salary_structure_assignment": new_ssa.name,
	})

	# Update Employee's gross_salary
	frappe.db.set_value("Employee", employee, "gross_salary", new_base)

	frappe.db.commit()

	return {
		"success": True,
		"message": f"Salary revised to {new_base} effective {from_date}. New SSA: {new_ssa.name}",
		"new_ssa": new_ssa.name,
	}
