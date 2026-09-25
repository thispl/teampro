frappe.pages['payroll-workbench'].on_page_load = function (wrapper) {

	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Payroll Workbench',
		single_column: true
	});

	frappe.breadcrumbs.add('HR', 'payroll-workbench');

	// Use page.body which may be jQuery; get raw DOM element
	let bodyEl = page.body[0] || page.body;
	bodyEl.innerHTML = `<div id="pw-root"></div>`;

	frappe.require([
		"https://unpkg.com/vue@3/dist/vue.global.js",
		"/assets/teampro/css/tailwind.css"
	], () => {
		// Re-create root if it was cleared by desk framework
		let mountEl = document.getElementById('pw-root');
		if (!mountEl) {
			mountEl = document.createElement('div');
			mountEl.id = 'pw-root';
			bodyEl.appendChild(mountEl);
		}
		mountPayrollWorkbench(mountEl);
	});
};

function mountPayrollWorkbench(mountEl) {

	const { createApp, ref, reactive, computed, onMounted, onUnmounted, watch } = Vue;

	const API = "teampro.api.payroll_workbench";

	function call(method, args) {
		return new Promise((resolve, reject) => {
			frappe.call({
				method: `${API}.${method}`,
				args: args || {},
				silent: true,  // suppress frappe's built-in error dialog — we handle errors in catch
				callback: (r) => {
					if (r.exc) {
						reject(r.exc);
					} else {
						resolve(r.message);
					}
				},
				error: (e) => reject(e)
			});
		});
	}

	const STATUS_COLORS = {
		"Present": "#10b981",
		"Absent": "#ef4444",
		"Half Day": "#f59e0b",
		"On Leave": "#3b82f6",
		"Work From Home": "#8b5cf6",
		"Unmarked": "#e5e7eb"
	};

	const STATUS_SHORT = {
		"Present": "P",
		"Absent": "A",
		"Half Day": "HD",
		"On Leave": "L",
		"Work From Home": "WFH",
		"Unmarked": "-"
	};

	// Helper: extract error message from frappe error object
	// frappe.call rejects with r.exc which can be:
	//   - a string (JSON or plain text)
	//   - an array of JSON strings
	//   - an Error object with .message
	function errMsg(e) {
		if (!e) return '';
		// Array: take first element and recurse
		if (Array.isArray(e)) return errMsg(e[0]);
		if (typeof e === 'string') {
			try { const r = JSON.parse(e); return r.message || e; } catch (_) { return e; }
		}
		if (e.message) {
			try { const r = JSON.parse(e.message); return r.message || e.message; } catch (_) { return e.message; }
		}
		if (e.responseText) {
			try { const r = JSON.parse(e.responseText); return r.message || e.responseText; } catch (_) {}
		}
		if (e._server_messages) {
			try { const msgs = JSON.parse(e._server_messages); return typeof msgs[0] === 'string' ? JSON.parse(msgs[0]).message || msgs[0] : msgs[0]; } catch (_) {}
		}
		return String(e);
	}

	// Helper: show error in a frappe dialog
	function showErrorDialog(title, e) {
		const msg = errMsg(e);
		frappe.msgprint({
			title: title || 'Error',
			message: msg,
			indicator: 'red'
		});
	}

	const app = createApp({
		setup() {
			// ---------- State ----------
			const loading = ref(false);
			const actionLoading = ref(false);
			const companies = ref([]);
			const bankAccounts = ref([]);

			const filters = reactive({
				company: "TEAMPRO HR & IT Services Pvt. Ltd.",
				branch: "",
				department: "",
				designation: "",
				grade: "",
				month: "",      // 1-12
				year: "",       // e.g. 2026
				from_date: "",
				to_date: ""
			});

			const monthOptions = [
				{ value: 1, label: 'January' },
				{ value: 2, label: 'February' },
				{ value: 3, label: 'March' },
				{ value: 4, label: 'April' },
				{ value: 5, label: 'May' },
				{ value: 6, label: 'June' },
				{ value: 7, label: 'July' },
				{ value: 8, label: 'August' },
				{ value: 9, label: 'September' },
				{ value: 10, label: 'October' },
				{ value: 11, label: 'November' },
				{ value: 12, label: 'December' }
			];

			const yearOptions = computed(() => {
				const currentYear = new Date().getFullYear();
				const years = [];
				for (let y = currentYear - 2; y <= currentYear + 1; y++) {
					years.push(y);
				}
				return years;
			});

			// When month or year changes, recompute from_date / to_date
			watch(() => [filters.month, filters.year], () => {
				if (filters.month && filters.year) {
					const m = parseInt(filters.month);
					const y = parseInt(filters.year);
					const first = new Date(y, m - 1, 1);
					const last = new Date(y, m, 0);
					filters.from_date = y + '-' +
						String(m).padStart(2, '0') + '-' +
						String(first.getDate()).padStart(2, '0');
					filters.to_date = y + '-' +
						String(m).padStart(2, '0') + '-' +
						String(last.getDate()).padStart(2, '0');
				}
			});

			const employees = ref([]);
			const selectedEmployees = ref(new Set());

			const showManual = ref(false);
			function openManual() { showManual.value = true; }
			function closeManual() { showManual.value = false; }

			const attendance = reactive({
				matrix: {},
				summary: {},
				days: []
			});

			const attendanceViewMode = ref('summary'); // 'matrix' or 'summary'
			const attendanceSummary = reactive({
				rows: [],
				totals: {}
			});

			const attendanceModal = reactive({
				show: false,
				data: null
			});

			const salaryRegister = reactive({
				slips: [],
				earnings_columns: [],
				deductions_columns: []
			});
			const selectedSlips = ref(new Set()); // slip names selected via checkbox

			const payrollEntry = ref(null);
			const bookedJE = ref(null);
			const bookedJEStatus = ref(null); // docstatus: 0=Draft, 1=Submitted
			const paymentJE = ref(null);
			const paymentJEStatus = ref(null); // docstatus: 0=Draft, 1=Submitted
			const payoutStatus = reactive({}); // employee -> status

			// Attendance approval state (Req 8: approval flow)
			const attendanceApproval = reactive({
				approval_name: null,
				status: null,       // null | "Draft" | "Pending for Approval" | "Approved" | "Rejected"
				requested_by: null,
				requested_on: null,
				approved_by: null,
				approved_on: null,
				employee_count: 0,
				total_payment_days: 0,
				sending: false,
			});

			// Computed: true when attendance is approved (salary register can load)
			const attendanceApproved = computed(() => attendanceApproval.status === 'Approved');

			// Computed: true when current user can approve attendance (Accounts Manager role)
			const canApproveAttendance = computed(() => {
				return !!(frappe.user && frappe.user.has_role && frappe.user.has_role('Accounts Manager'));
			});

			// Payroll booking approval state
			const payrollApproval = reactive({
				approval_name: null,
				status: null,       // null | "Draft" | "Pending for Approval" | "Approved" | "Rejected"
				requested_by: null,
				requested_on: null,
				approved_by: null,
				approved_on: null,
				sending: false,
			});

			// Computed: true when payroll booking is approved
			const payrollBookingApproved = computed(() => payrollApproval.status === 'Approved');

			// Computed: true when current user can approve payroll booking (CEO role)
			const canApprovePayrollBooking = computed(() => {
				return !!(frappe.user && frappe.user.has_role && frappe.user.has_role('CEO'));
			});

			// Dropdown state for the combined "Send for Approval / Regenerate Payroll" actions menu
			const showRegisterActions = ref(false);
			function toggleRegisterActions() {
				showRegisterActions.value = !showRegisterActions.value;
			}
			function _closeRegisterActionsOnOutsideClick(e) {
				if (!e.target.closest('.pw-register-actions')) {
					showRegisterActions.value = false;
				}
			}
			onMounted(() => document.addEventListener('click', _closeRegisterActionsOnOutsideClick));
			onUnmounted(() => document.removeEventListener('click', _closeRegisterActionsOnOutsideClick));

			const releaseModal = reactive({
				show: false,
				mode: "Manual",       // "Manual" | "Automated" | "BTS"
				bank_account: "",
				reference_no: "",
				reference_date: "",
				payment_date: "",
				processing: false,
				employees: [],       // list of {employee, employee_name, net_pay, rounded_total, bank_ac_no, ifsc_code, selected}
				selectedAll: true,
			});

			// BTS is now a mode within the Release Payment modal

			// Payment Release tab state
			const paymentTab = ref('employee'); // 'employee' | 'epf' | 'esi'
			const statutorySummary = reactive({
				epf: null,
				esi: null,
			});
			const statutoryJE = reactive({
				epf: null,
				esi: null,
			});
			const statutoryModal = reactive({
				show: false,
				payment_type: "EPF",
				bank_account: "",
				reference_no: "",
				reference_date: "",
				processing: false,
			});

			// Statutory Report child table
			const statutoryReport = ref([]);
			const statutoryReportSaving = ref(false);

			// Req 2: Search filters for tables
			const attendanceSearchQuery = ref('');
			const salaryRegisterSearchQuery = ref('');

			// Attendance selection state
			const selectedAttendanceEmployees = ref(new Set());

			// Per-column filters for attendance summary table
			const attendanceColumnFilters = reactive({
				employee_name: '',
				department: '',
				calendar_days: '',
				holidays: '',
				present: '',
				paid_leave: '',
				absent_unpaid: '',
				late_count: '',
				late_penalty_days: '',
				late_penalty_amount: '',
				unapproved_leaves: '',
				unapproved_attendance_requests: '',
				payment_days: '',
			});

			function clearAttendanceColumnFilters() {
				for (const k in attendanceColumnFilters) attendanceColumnFilters[k] = '';
			}

			function _matchNum(val, filterVal) {
				if (filterVal === '' || filterVal === null || filterVal === undefined) return true;
				const f = parseFloat(filterVal);
				if (isNaN(f)) return true;
				return (val || 0) >= f;
			}

			// Req 2: Filtered rows for attendance summary
			const filteredAttendanceRows = computed(() => {
				const q = attendanceSearchQuery.value.toLowerCase().trim();
				const cf = attendanceColumnFilters;
				return attendanceSummary.rows.filter(r => {
					if (q && !(r.employee_name || '').toLowerCase().includes(q) && !(r.employee || '').toLowerCase().includes(q)) return false;
					if (cf.employee_name && !(r.employee_name || '').toLowerCase().includes(cf.employee_name.toLowerCase())) return false;
					if (cf.department && !(r.department || '').toLowerCase().includes(cf.department.toLowerCase())) return false;
					if (!_matchNum(r.calendar_days, cf.calendar_days)) return false;
					if (!_matchNum(r.holidays, cf.holidays)) return false;
					if (!_matchNum(r.present, cf.present)) return false;
					if (!_matchNum(r.paid_leave, cf.paid_leave)) return false;
					if (!_matchNum(r.absent_unpaid, cf.absent_unpaid)) return false;
					if (!_matchNum(r.late_count, cf.late_count)) return false;
					if (!_matchNum(r.late_penalty_days, cf.late_penalty_days)) return false;
					if (!_matchNum(r.late_penalty_amount, cf.late_penalty_amount)) return false;
					if (!_matchNum(r.unapproved_leaves, cf.unapproved_leaves)) return false;
					if (!_matchNum(r.unapproved_attendance_requests, cf.unapproved_attendance_requests)) return false;
					if (!_matchNum(r.payment_days, cf.payment_days)) return false;
					return true;
				});
			});

			// Req 2: Filtered rows for salary register
			const filteredSalarySlips = computed(() => {
				const q = salaryRegisterSearchQuery.value.toLowerCase().trim();
				if (!q) return salaryRegister.slips;
				return salaryRegister.slips.filter(s =>
					(s.employee_name || '').toLowerCase().includes(q) ||
					(s.employee || '').toLowerCase().includes(q)
				);
			});

			// Req: Column display name mapping (short names)
			const COLUMN_LABELS = {
				'House Rent Allowance': 'HRA',
				'Dearness Allowance': 'DA',
				'Laptop Allowance': 'LA',
				'Fixed Annual Incentive': 'FAI',
				'Professional Tax': 'PT',
				'PF - Employer': 'PF - Employer',
				'PF - Employee': 'Total EPF',
				'Arrear-Pay': 'Arrear-Pay',
				'Arrear-Deduct': 'Arrear-Deduct',
			};
			function colLabel(col) {
				return COLUMN_LABELS[col] || col;
			}

			// Shared helper: aggregate component-wise totals across a list of slips
			function _computeSlipTotals(slips) {
				if (!slips.length) return null;
				const totals = {
					earnings: {},
					deductions: {},
					gross_pay: 0,
					custom_total_deduction: 0,
					net_pay: 0,
					count: slips.length,
				};
				for (const slip of slips) {
					for (const e of (slip.earnings || [])) {
						totals.earnings[e.component] = (totals.earnings[e.component] || 0) + (e.amount || 0);
					}
					for (const d of (slip.deductions || [])) {
						totals.deductions[d.component] = (totals.deductions[d.component] || 0) + (d.amount || 0);
					}
					totals.gross_pay += slip.gross_pay || 0;
					totals.custom_total_deduction += slip.custom_total_deduction || 0;
					totals.net_pay += slip.net_pay || 0;
				}
				return totals;
			}

			// Req: Totals row for salary register (respects search filter)
			const salaryRegisterTotals = computed(() => _computeSlipTotals(filteredSalarySlips.value));

			// Component-wise totals reflecting the Salary Register (respects search filter),
			// shown in the Payroll Summary section after booking.
			const salaryComponentSummary = computed(() => _computeSlipTotals(filteredSalarySlips.value));

			// Man-hours & time cost metrics (office time 0930–1830 = 9 hrs/day)
			const WORK_HOURS_PER_DAY = 9;
			const payrollMetrics = computed(() => {
				const t = salaryComponentSummary.value;
				if (!t) return null;
				const totalPaymentDays = filteredSalarySlips.value.reduce((sum, s) => sum + (s.payment_days || 0), 0);
				const totalManHours = totalPaymentDays * WORK_HOURS_PER_DAY;
				const totalGross = t.gross_pay || 0;
				const totalNet = t.net_pay || 0;
				const costPerDay = totalPaymentDays > 0 ? totalGross / totalPaymentDays : 0;
				const costPerHour = totalManHours > 0 ? totalGross / totalManHours : 0;
				const costPerMinute = costPerHour / 60;
				return {
					totalPaymentDays,
					totalManHours,
					totalGross,
					totalNet,
					costPerDay,
					costPerHour,
					costPerMinute,
				};
			});

			// Slip selection helpers
			const selectedSlipList = computed(() => Array.from(selectedSlips.value));
			const selectedDraftSlips = computed(() =>
				salaryRegister.slips.filter(s => selectedSlips.value.has(s.name) && s.docstatus === 0)
			);
			const selectedSubmittedSlips = computed(() =>
				salaryRegister.slips.filter(s => selectedSlips.value.has(s.name) && s.docstatus === 1)
			);
			// Cancelled slips that need regeneration (docstatus=2)
			const cancelledSlips = computed(() =>
				salaryRegister.slips.filter(s => s.docstatus === 2)
			);
			function toggleSlipSelection(slipName) {
				const next = new Set(selectedSlips.value);
				if (next.has(slipName)) next.delete(slipName);
				else next.add(slipName);
				selectedSlips.value = next;
			}
			function toggleAllSlips() {
				if (selectedSlips.value.size === filteredSalarySlips.value.length) {
					selectedSlips.value = new Set();
				} else {
					selectedSlips.value = new Set(filteredSalarySlips.value.map(s => s.name));
				}
			}

			// Attendance selection helpers
			function toggleAttendanceSelection(empName) {
				const next = new Set(selectedAttendanceEmployees.value);
				if (next.has(empName)) next.delete(empName);
				else next.add(empName);
				selectedAttendanceEmployees.value = next;
			}
			function toggleAllAttendance() {
				if (selectedAttendanceEmployees.value.size === filteredAttendanceRows.value.length) {
					selectedAttendanceEmployees.value = new Set();
				} else {
					selectedAttendanceEmployees.value = new Set(filteredAttendanceRows.value.map(r => r.employee));
				}
			}

			// ---------- Computed ----------
			const totalEmployees = computed(() => employees.value.length);
			const selectedCount = computed(() => selectedEmployees.value.size);
			const selectedEmployeeList = computed(() =>
				employees.value.filter(e => selectedEmployees.value.has(e.name)).map(e => e.name)
			);

			const monthDays = computed(() => attendance.days || []);

			// Req 3: block progression if any employee has unapproved leaves or attendance requests
			// DISABLED for now — payroll can proceed even with unapproved items
			const hasUnapprovedItems = computed(() => {
				return false;
			});
			const unapprovedTotal = computed(() => {
				let leaves = 0, attReqs = 0;
				attendanceSummary.rows.forEach(r => {
					leaves += (r.unapproved_leaves || 0);
					attReqs += (r.unapproved_attendance_requests || 0);
				});
				return { leaves, attReqs, total: leaves + attReqs };
			});

			// ---------- Helpers ----------
			function fmtDate(d) {
				if (!d) return "";
				const date = new Date(d);
				return date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' });
			}

			function fmtMoney(v) {
				if (v == null || isNaN(v)) return "0";
				return Number(v).toLocaleString('en-IN', { maximumFractionDigits: 0 });
			}

			function jeStatusLabel(docstatus) {
				if (docstatus === 1) return 'Submitted';
				if (docstatus === 2) return 'Cancelled';
				return 'Draft';
			}

			// ---------- Excel Export ----------
			function _downloadExcel(htmlContent, filename) {
				const blob = new Blob(['\ufeff' + htmlContent], { type: 'application/vnd.ms-excel' });
				const url = URL.createObjectURL(blob);
				const a = document.createElement('a');
				a.href = url;
				a.download = filename;
				document.body.appendChild(a);
				a.click();
				document.body.removeChild(a);
				URL.revokeObjectURL(url);
			}

			function _excelHeaderRow(headers, bg, fg) {
				let html = '<tr>';
				headers.forEach(h => {
					html += `<th style="background:${bg};color:${fg};font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">${h}</th>`;
				});
				html += '</tr>';
				return html;
			}

			function _excelTitleBlock(title, subtitle, colSpan) {
				return `<tr><td colspan="${colSpan}" style="background:#1e293b;color:#fff;font-size:18px;font-weight:bold;padding:10px 14px;text-align:center;border:1px solid #334155;">${title}</td></tr>`
					+ `<tr><td colspan="${colSpan}" style="background:#f1f5f9;color:#475569;font-size:12px;padding:6px 14px;text-align:center;border:1px solid #cbd5e1;">${subtitle}</td></tr>`
					+ `<tr><td colspan="${colSpan}" style="font-size:2px;line-height:2px;">&nbsp;</td></tr>`;
			}

			function exportAttendanceExcel() {
				if (!filteredAttendanceRows.value.length) {
					frappe.msgprint("No attendance data to export");
					return;
				}
				const rows = filteredAttendanceRows.value;
				const headers = ['Employee ID', 'Employee Name', 'Department', 'Calendar Days', 'Holidays',
					'Present', 'Paid Leave', 'Absent / Unpaid', 'Late Count', 'Late Penalty Days',
					'Penalty Amount', 'Unapproved Leaves', 'Unapproved Att. Requests', 'Payment Days'];
				const colCount = headers.length;
				const periodStr = `${fmtDate(filters.from_date)} — ${fmtDate(filters.to_date)}`;
				const companyStr = filters.company || '';
				const generatedStr = new Date().toLocaleString('en-IN');

				let html = '<table border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse;font-family:Calibri,Arial,sans-serif;font-size:11px;">';
				// Title block
				html += _excelTitleBlock('Attendance Summary Report', `${companyStr} &nbsp;|&nbsp; Period: ${periodStr} &nbsp;|&nbsp; Generated: ${generatedStr}`, colCount);
				// Header row
				html += '<thead>' + _excelHeaderRow(headers, '#1e40af', '#fff') + '</thead><tbody>';
				// Data rows
				rows.forEach((r, idx) => {
					const rowBg = idx % 2 === 0 ? '#ffffff' : '#f8fafc';
					html += `<tr style="background:${rowBg};">`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;">${r.employee || ''}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;font-weight:600;">${r.employee_name || ''}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;color:#64748b;">${r.department || ''}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;">${r.calendar_days || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#7c3aed;">${r.holidays || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#059669;font-weight:600;">${r.present || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#2563eb;">${r.paid_leave || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#dc2626;">${r.absent_unpaid || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;">${r.late_count || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#d97706;font-weight:600;">${r.late_penalty_days || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;">${fmtMoney(r.late_penalty_amount || 0)}</td>`;
					const ulColor = (r.unapproved_leaves > 0) ? 'color:#dc2626;font-weight:700;' : 'color:#94a3b8;';
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;${ulColor}">${r.unapproved_leaves || 0}</td>`;
					const arColor = (r.unapproved_attendance_requests > 0) ? 'color:#dc2626;font-weight:700;' : 'color:#94a3b8;';
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;${arColor}">${r.unapproved_attendance_requests || 0}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;font-weight:bold;font-size:13px;background:#f0fdf4;color:#166534;">${r.payment_days || 0}</td>`;
					html += '</tr>';
				});
				// Totals row
				if (attendanceSummary.totals && attendanceSummary.totals.calendar_days) {
					const t = attendanceSummary.totals;
					html += '<tr style="font-weight:bold;background:#1e293b;color:#fff;">';
					html += `<td style="padding:6px 10px;border:1px solid #334155;" colspan="3">TOTALS (${rows.length} employees)</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.calendar_days || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.holidays || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.present || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.paid_leave || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.absent_unpaid || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.late_count || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.late_penalty_days || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${fmtMoney(t.late_penalty_amount || 0)}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.unapproved_leaves || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${t.unapproved_attendance_requests || 0}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;font-size:14px;background:#166534;">${t.payment_days || 0}</td>`;
					html += '</tr>';
				}
				// Footer note
				html += `<tr><td colspan="${colCount}" style="font-size:10px;color:#94a3b8;padding:8px 14px;border:1px solid #e2e8f0;">Payment Days = Present + Paid Leave + Holidays - Late Penalty Days. Holidays are counted from the Holiday List only after Date of Joining and exclude holidays sandwiched between leave days.</td></tr>`;
				html += '</tbody></table>';
				const fname = `Attendance_Summary_${filters.from_date}_to_${filters.to_date}.xls`;
				_downloadExcel(html, fname);
			}

			function exportSalaryRegisterExcel() {
				if (!filteredSalarySlips.value.length) {
					frappe.msgprint("No salary register data to export");
					return;
				}
				const slips = filteredSalarySlips.value;
				const earnCols = salaryRegister.earnings_columns || [];
				const dedCols = salaryRegister.deductions_columns || [];
				const headers = ['Emp ID', 'Employee Name', 'Fixed Gross', 'Days'];
				earnCols.forEach(c => headers.push(colLabel(c)));
				dedCols.forEach(c => headers.push(colLabel(c)));
				headers.push('Gross CTC', 'Total Deduction', 'Net Total', 'Status');
				const colCount = headers.length;
				const periodStr = `${fmtDate(filters.from_date)} — ${fmtDate(filters.to_date)}`;
				const companyStr = filters.company || '';
				const generatedStr = new Date().toLocaleString('en-IN');

				let html = '<table border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse;font-family:Calibri,Arial,sans-serif;font-size:11px;">';
				// Title block
				html += _excelTitleBlock('Salary Register Report', `${companyStr} &nbsp;|&nbsp; Period: ${periodStr} &nbsp;|&nbsp; Generated: ${generatedStr}`, colCount);
				// Earnings / Deductions section header
				const earnSpan = earnCols.length;
				const dedSpan = dedCols.length;
				html += '<thead>';
				// Group header row
				html += '<tr>';
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Emp ID</th>`;
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Employee Name</th>`;
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Fixed Gross</th>`;
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Days</th>`;
				if (earnSpan > 0) html += `<th colspan="${earnSpan}" style="background:#166534;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:12px;">EARNINGS</th>`;
				if (dedSpan > 0) html += `<th colspan="${dedSpan}" style="background:#991b1b;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:12px;">DEDUCTIONS</th>`;
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Gross CTC</th>`;
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Total Deduction</th>`;
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Net Total</th>`;
				html += `<th rowspan="2" style="background:#0f172a;color:#fff;font-weight:bold;padding:6px 10px;border:1px solid #334155;text-align:center;font-size:11px;">Status</th>`;
				html += '</tr>';
				// Column header row
				html += _excelHeaderRow(headers.slice(4), '#1e40af', '#fff');
				html += '</thead><tbody>';

				slips.forEach((s, idx) => {
					const rowBg = idx % 2 === 0 ? '#ffffff' : '#f8fafc';
					html += `<tr style="background:${rowBg};">`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;">${s.employee || ''}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;font-weight:600;">${s.employee_name || ''}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;">${fmtMoney(s.fixed_gross || 0)}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:center;">${s.payment_days || 0}</td>`;
					// Earnings
					earnCols.forEach(col => {
						const val = (s.earnings || []).find(e => e.component === col)?.amount || 0;
						html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#059669;">${fmtMoney(val)}</td>`;
					});
					// Deductions
					dedCols.forEach(col => {
						const val = (s.deductions || []).find(d => d.component === col)?.amount || 0;
						html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#dc2626;">${fmtMoney(val)}</td>`;
					});
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;font-weight:600;">${fmtMoney(s.gross_pay || 0)}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;color:#dc2626;">${fmtMoney(s.total_deduction || 0)}</td>`;
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:right;font-weight:bold;font-size:12px;color:#166534;">${fmtMoney(s.net_pay || 0)}</td>`;
					const statusLabel = s.docstatus === 0 ? 'Draft' : (s.docstatus === 1 ? 'Submitted' : 'Cancelled');
					const statusColor = s.docstatus === 1 ? '#166534' : (s.docstatus === 2 ? '#dc2626' : '#92400e');
					html += `<td style="padding:4px 8px;border:1px solid #e2e8f0;text-align:center;color:${statusColor};font-weight:600;">${statusLabel}</td>`;
					html += '</tr>';
				});

				// Totals row
				if (salaryRegisterTotals.value) {
					const t = salaryRegisterTotals.value;
					html += '<tr style="font-weight:bold;background:#1e293b;color:#fff;">';
					html += `<td style="padding:6px 10px;border:1px solid #334155;" colspan="3">TOTAL (${t.count} employees)</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:center;">—</td>`;
					earnCols.forEach(col => {
						html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${fmtMoney(t.earnings[col] || 0)}</td>`;
					});
					dedCols.forEach(col => {
						html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${fmtMoney(t.deductions[col] || 0)}</td>`;
					});
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${fmtMoney(t.gross_pay || 0)}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;">${fmtMoney(t.custom_total_deduction || 0)}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:right;font-size:13px;background:#166534;">${fmtMoney(t.net_pay || 0)}</td>`;
					html += `<td style="padding:6px 10px;border:1px solid #334155;text-align:center;">—</td>`;
					html += '</tr>';
				}

				// Footer note
				html += `<tr><td colspan="${colCount}" style="font-size:10px;color:#94a3b8;padding:8px 14px;border:1px solid #e2e8f0;">Total Deduction = PF - Employer + PF - Employee + Professional Tax + Arrear-Deduct. Amounts in INR. Generated by Payroll Workbench.</td></tr>`;
				html += '</tbody></table>';
				const fname = `Salary_Register_${filters.from_date}_to_${filters.to_date}.xls`;
				_downloadExcel(html, fname);
			}

			function statusColor(status) {
				return STATUS_COLORS[status] || STATUS_COLORS["Unmarked"];
			}

			function statusShort(status) {
				return STATUS_SHORT[status] || "-";
			}

			function cellData(emp, day) {
				return attendance.matrix[emp] && attendance.matrix[emp][day]
					? attendance.matrix[emp][day] : null;
			}

			function openSlipInNewTab(name) {
				window.open('/app/salary-slip/' + encodeURIComponent(name), '_blank');
			}

			function openAttendanceInNewTab(name) {
				window.open('/app/attendance/' + encodeURIComponent(name), '_blank');
			}

			// Req 4: open filtered list views in a new tab
			function openFilteredList(doctype, filters) {
				// Build a URL like /app/leave-application?docstatus=0&from_date=["Between",["2026-07-01","2026-07-31"]]
				const slug = doctype.toLowerCase().replace(/ /g, '-');
				let url = '/app/' + slug;
				const parts = [];
				for (const [key, val] of Object.entries(filters)) {
					if (val === undefined || val === null || val === '') continue;
					// Array value is passed as JSON (frappe desk filter format)
					// e.g. ["Between",["2026-07-01","2026-07-31"]] or ["<=", "2026-07-31"]
					if (Array.isArray(val)) {
						parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(JSON.stringify(val)));
					} else {
						parts.push(encodeURIComponent(key) + '=' + encodeURIComponent(String(val)));
					}
				}
				if (parts.length) url += '?' + parts.join('&');
				window.open(url, '_blank');
			}

			function openUnapprovedLeaves(emp) {
				// Draft leaves (not Rejected/Cancelled) overlapping with the selected period
				openFilteredList('Leave Application', {
					employee: emp,
					docstatus: 0,
					from_date: ['Between', [filters.from_date, filters.to_date]],
					workflow_state: ['!=', 'Rejected']
				});
			}

			function openUnapprovedAttRequests(emp) {
				openFilteredList('Attendance Request', {
					employee: emp,
					workflow_state: 'Draft',
					from_date: ['Between', [filters.from_date, filters.to_date]]
				});
			}

			function openLeaveList(emp) {
				openFilteredList('Leave Application', {
					employee: emp,
					from_date: ['Between', [filters.from_date, filters.to_date]],
				});
			}

			function openAttendanceList(emp, status) {
				const f = {
					employee: emp,
					attendance_date: ['Between', [filters.from_date, filters.to_date]],
				};
				if (status) f.status = status;
				openFilteredList('Attendance', f);
			}

			// Smart click for Absent/Unpaid: opens Attendance (Absent) if absent_count > 0,
			// and Leave Application (LWP) if lwp_count > 0.
			function openAbsentList(emp, row) {
				if (row.absent_count > 0) {
					openFilteredList('Attendance', {
						employee: emp,
						status: 'Absent',
						attendance_date: ['Between', [filters.from_date, filters.to_date]],
					});
				}
				if (row.lwp_count > 0) {
					openFilteredList('Leave Application', {
						employee: emp,
						from_date: ['Between', [filters.from_date, filters.to_date]],
						leave_type: ['=', 'Leave Without Pay'],
					});
				}
			}

			function openLatePenaltyList(emp) {
				openFilteredList('Late Penalty', { emp_name: emp });
			}

			function openLatePenaltyDoc(name) {
				window.open(`/app/late-penalty/${name}`, '_blank');
			}

			// File upload helpers for Statutory Report
			function triggerFileInput(refName) {
				const el = this.$refs[refName];
				if (el) el.click();
			}

			async function uploadStatutoryFile(file, row, field) {
				try {
					const file_url = await new Promise((resolve, reject) => {
						const reader = new FileReader();
						reader.onload = () => {
							frappe.call({
								method: 'uploadfile',
								args: {
									filedata: reader.result,
									filename: file.name,
									from_form: 1,
									doctype: 'Payroll Entry',
									docname: payrollEntry.value || '',
								},
								callback: (r) => {
									if (r.exc) reject(r.exc);
									else resolve(r.message || r.values?.file_url);
								},
								error: (e) => reject(e)
							});
						};
						reader.onerror = () => reject(reader.error);
						reader.readAsDataURL(file);
					});
					row[field] = file_url;
					frappe.show_alert({ message: 'File uploaded', indicator: 'green' });
				} catch (e) {
					frappe.msgprint({ title: 'Upload Failed', message: errMsg(e), indicator: 'red' });
				}
			}

			async function generateReturnFile(row, fileType) {
				if (!payrollEntry.value) {
					frappe.msgprint({ title: 'Error', message: 'Generate payroll first.', indicator: 'red' });
					return;
				}
				if (fileType === 'epf') {
					showManualEcrDialog(row, fileType);
				} else {
					doGenerateReturnFile(row, fileType, []);
				}
			}

			function showManualEcrDialog(row, fileType) {
				let manualRows = [];
				let dialog = new frappe.ui.Dialog({
					title: 'Generate EPF ECR',
					fields: [
						{
							fieldtype: 'HTML',
							options: '<p>Manual rows are for employees without salary slips (e.g. exited employees). Leave empty if not needed.</p>',
						},
						{
							fieldname: 'manual_rows_html',
							fieldtype: 'HTML',
						},
					],
					primary_action_label: 'Generate ECR',
					primary_action: function() {
						// Collect manual rows from the table
						let rows = [];
						$(dialog.wrapper).find('.manual-ecr-row').each(function() {
							let uan = $(this).find('.ecr-uan').val().trim();
							let name = $(this).find('.ecr-name').val().trim();
							let gross = parseFloat($(this).find('.ecr-gross').val()) || 0;
							let epf = parseFloat($(this).find('.ecr-epf').val()) || 0;
							let ncp = parseInt($(this).find('.ecr-ncp').val()) || 0;
							if (uan && name && epf > 0) {
								rows.push({ uan: uan, name: name, gross: gross, epf_wages: epf, ncp_days: ncp });
							}
						});
						dialog.hide();
						doGenerateReturnFile(row, fileType, rows);
					},
				});
				dialog.show();

				// Build manual rows table inside the dialog
				let html = '<div class="manual-ecr-container">' +
					'<table class="table table-bordered">' +
					'<thead><tr><th>UAN</th><th>Name</th><th>Gross</th><th>EPF Wages</th><th>NCP Days</th><th></th></tr></thead>' +
					'<tbody class="manual-ecr-body"></tbody></table>' +
					'<button class="btn btn-sm btn-default add-ecr-row-btn">+ Add Row</button>' +
					'</div>';
				$(dialog.wrapper).find('[data-fieldname="manual_rows_html"]').html(html);

				function addManualRow(data) {
					data = data || {};
					let tr = '<tr class="manual-ecr-row">' +
						'<td><input class="form-control ecr-uan" type="text" value="' + (data.uan || '') + '" placeholder="UAN"></td>' +
						'<td><input class="form-control ecr-name" type="text" value="' + (data.name || '') + '" placeholder="Name"></td>' +
						'<td><input class="form-control ecr-gross" type="number" value="' + (data.gross || '') + '" placeholder="Gross"></td>' +
						'<td><input class="form-control ecr-epf" type="number" value="' + (data.epf_wages || '') + '" placeholder="EPF Wages"></td>' +
						'<td><input class="form-control ecr-ncp" type="number" value="' + (data.ncp_days || 0) + '" placeholder="0"></td>' +
						'<td><button class="btn btn-xs btn-danger remove-ecr-row">x</button></td>' +
						'</tr>';
					$(dialog.wrapper).find('.manual-ecr-body').append(tr);
				}

				$(dialog.wrapper).find('.add-ecr-row-btn').on('click', function() { addManualRow(); });
				$(dialog.wrapper).on('click', '.remove-ecr-row', function() { $(this).closest('tr').remove(); });
			}

			function doGenerateReturnFile(row, fileType, manualRows) {
				frappe.show_progress('Generating ' + (fileType === 'epf' ? 'EPF ECR' : 'ESIC Return') + ' file...', 50, 'Please wait...');
				frappe.call({
					method: "teampro.api.payroll_workbench.generate_epf_esi_return",
					args: {
						payroll_entry_name: payrollEntry.value,
						file_type: fileType,
						manual_rows: fileType === 'epf' ? JSON.stringify(manualRows) : null,
					},
					callback: function(r) {
						frappe.hide_progress();
						if (r.message && r.message.success) {
							var res = r.message;
							row.download_return = res.file_url;
							frappe.show_alert({
								message: (fileType === 'epf' ? 'EPF ECR' : 'ESIC Return') + ' generated: ' + res.rows + ' rows',
								indicator: 'green',
							}, 5);
							// Download via base64 data URL (most reliable for .txt files)
						if (res.content_b64) {
							var dataUrl = 'data:text/plain;charset=utf-8;base64,' + res.content_b64;
							var a = document.createElement('a');
							a.href = dataUrl;
							a.download = res.filename || 'return_file.txt';
							document.body.appendChild(a);
							a.click();
							document.body.removeChild(a);
						} else {
							var fullUrl = window.location.origin + res.file_url;
							var a = document.createElement('a');
							a.href = fullUrl;
							a.download = res.filename || '';
							document.body.appendChild(a);
							a.click();
							document.body.removeChild(a);
						}
						} else {
							frappe.msgprint({ title: 'Generation Failed', message: 'No file was generated. Check if eligible employees exist.', indicator: 'red' });
						}
					},
					error: function(e) {
						frappe.hide_progress();
						frappe.msgprint({ title: 'Generation Failed', message: 'Server error: ' + (e && e.message ? e.message : 'Unknown error'), indicator: 'red' });
					}
				});
			}

			// ---------- Actions ----------
			async function loadCompanies() {
				try {
					const res = await call("get_companies");
					companies.value = res || [];
					if (companies.value.length && !filters.company) {
						filters.company = companies.value[0].name;
					}
				} catch (e) { console.error(e); }
			}

			async function loadBankAccounts() {
				if (!filters.company) return;
				try {
					bankAccounts.value = await call("get_company_bank_accounts", { company: filters.company });
				} catch (e) { console.error(e); }
			}

			function defaultMonthRange() {
				const now = new Date();
				filters.month = String(now.getMonth() + 1);  // 1-12
				filters.year = String(now.getFullYear());
				// watch on [month, year] will set from_date / to_date
			}

			async function loadEmployees() {
				if (!filters.company || !filters.from_date || !filters.to_date) {
					frappe.msgprint("Please select Company and Date range");
					return;
				}
				loading.value = true;
				try {
					employees.value = await call("get_employees", { filters: filters });
					selectedEmployees.value = new Set(employees.value.map(e => e.name));
					await loadAttendance();
					await loadBankAccounts();
					// Load attendance approval status (Req 8)
					await loadAttendanceApproval();
					// Always load payroll state — existing slips/JE should be visible
					// even if attendance approval record is missing or not yet approved
					await loadPayrollState();
					// Auto-generate draft slips only if attendance is approved and no slips exist yet
					if (attendanceApproved.value && selectedEmployeeList.value.length && !salaryRegister.slips.length && !hasUnapprovedItems.value) {
						await generatePayroll();
					}
				} catch (e) {
					frappe.msgprint({ title: "Error", message: errMsg(e), indicator: 'red' });
				} finally {
					loading.value = false;
				}
			}

			async function loadPayrollState() {
				if (!selectedEmployeeList.value.length) return;
				try {
					// Load attendance approval status first (Req 8)
					await loadAttendanceApproval();
					// Always load payroll state — existing slips/JE should be visible
					// even if attendance approval record is missing or not yet approved

					const res = await call("get_payroll_period_status", {
						start_date: filters.from_date,
						end_date: filters.to_date,
						company: filters.company,
						employees: selectedEmployeeList.value
					});
					payrollEntry.value = res.payroll_entry || null;
					bookedJE.value = res.booked_je || null;
					bookedJEStatus.value = res.booked_je_docstatus != null ? res.booked_je_docstatus : null;
					paymentJE.value = res.payment_je || null;
					paymentJEStatus.value = res.payment_je_docstatus != null ? res.payment_je_docstatus : null;
					// Merge payout status
					if (res.payout_status) {
						Object.assign(payoutStatus, res.payout_status);
					}
					// Load salary register if slips exist
					if (res.slip_counts && res.slip_counts.total > 0) {
						await loadSalaryRegister();
					}
					// Load payroll booking approval status
					await loadPayrollApproval();
					// Load statutory payment summaries
					await loadStatutorySummary();
					// Load statutory report child table
					await loadStatutoryReport();
				} catch (e) {
					console.error("loadPayrollState error:", e);
				}
			}

			async function loadAttendance() {
				if (!selectedEmployeeList.value.length) {
					attendance.matrix = {};
					attendance.summary = {};
					attendance.days = [];
					return;
				}
				try {
					const res = await call("get_attendance_matrix", {
						employees: selectedEmployeeList.value,
						from_date: filters.from_date,
						to_date: filters.to_date
					});
					attendance.matrix = res.matrix || {};
					attendance.summary = res.summary || {};
					attendance.days = res.days || [];
					// Also load summary data if in summary mode
					if (attendanceViewMode.value === 'summary') {
						await loadAttendanceSummary();
					}
				} catch (e) {
					console.error(e);
				}
			}

			async function loadAttendanceSummary() {
				if (!selectedEmployeeList.value.length) {
					attendanceSummary.rows = [];
					attendanceSummary.totals = {};
					return;
				}
				try {
					const res = await call("get_attendance_summary", {
						employees: selectedEmployeeList.value,
						from_date: filters.from_date,
						to_date: filters.to_date,
						company: filters.company
					});
					attendanceSummary.rows = res.rows || [];
					attendanceSummary.totals = res.totals || {};
				} catch (e) {
					console.error(e);
					frappe.show_alert({ message: "Failed to load summary: " + errMsg(e), indicator: 'red' });
				}
			}

			// ---------- Attendance Approval (Req 8: approval flow) ----------
			async function loadAttendanceApproval() {
				if (!filters.company || !filters.from_date || !filters.to_date) return;
				try {
					const res = await call("get_attendance_approval_status", {
						company: filters.company,
						start_date: filters.from_date,
						end_date: filters.to_date
					});
					attendanceApproval.approval_name = res.approval_name;
					attendanceApproval.status = res.status;
					attendanceApproval.requested_by = res.requested_by;
					attendanceApproval.requested_on = res.requested_on;
					attendanceApproval.approved_by = res.approved_by;
					attendanceApproval.approved_on = res.approved_on;
					attendanceApproval.employee_count = res.employee_count;
					attendanceApproval.total_payment_days = res.total_payment_days;
				} catch (e) {
					console.error("loadAttendanceApproval error:", e);
				}
			}

			async function sendForApproval() {
				if (!attendanceSummary.rows.length) {
					frappe.msgprint("Load attendance summary first before sending for approval.");
					return;
				}
				if (hasUnapprovedItems.value) {
					const u = unapprovedTotal.value;
					frappe.msgprint({
						title: "Cannot Send for Approval",
						message: `There are ${u.leaves} unapproved Leave(s) and ${u.attReqs} unapproved Attendance Request(s). ` +
							"All items must be resolved before sending for approval.",
						indicator: 'red'
					});
					return;
				}
				if (!confirm(`Send attendance summary for approval?\n\nCompany: ${filters.company}\nPeriod: ${filters.from_date} to ${filters.to_date}\nEmployees: ${attendanceSummary.rows.length}`)) return;
				attendanceApproval.sending = true;
				try {
					const res = await call("send_attendance_for_approval", {
						company: filters.company,
						start_date: filters.from_date,
						end_date: filters.to_date,
						employees: selectedEmployeeList.value,
						summary_data: {
							totals: attendanceSummary.totals
						}
					});
					attendanceApproval.approval_name = res.approval_name;
					attendanceApproval.status = res.status;
					frappe.show_alert({ message: res.message, indicator: 'blue' });
				} catch (e) {
					frappe.msgprint({ title: "Failed to Send", message: errMsg(e), indicator: 'red' });
				} finally {
					attendanceApproval.sending = false;
				}
			}

			async function approveAttendance() {
				if (!attendanceApproval.approval_name) return;
				if (!confirm("Approve this attendance summary?\n\nAll draft attendance records will be submitted in the backend.")) return;
				attendanceApproval.sending = true;
				try {
					const res = await call("approve_attendance_summary", {
						approval_name: attendanceApproval.approval_name
					});
					attendanceApproval.status = res.status;
					attendanceApproval.approved_by = frappe.session.user;
					frappe.show_alert({
						message: res.message + (res.errors && res.errors.length ? ` (${res.errors.length} errors)` : ''),
						indicator: 'green'
					});
					if (res.errors && res.errors.length) {
						frappe.msgprint({
							title: "Some attendance records failed to submit",
							message: res.errors.join('<br>'),
							indicator: 'orange',
							wide: true
						});
					}
					// Reload attendance to reflect submitted status
					await loadAttendance();
				} catch (e) {
					frappe.msgprint({ title: "Approval Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					attendanceApproval.sending = false;
				}
			}

			async function rejectAttendance() {
				if (!attendanceApproval.approval_name) return;
				const remarks = prompt("Reason for rejection (optional):");
				if (remarks === null) return; // cancelled
				attendanceApproval.sending = true;
				try {
					const res = await call("reject_attendance_summary", {
						approval_name: attendanceApproval.approval_name,
						remarks: remarks
					});
					attendanceApproval.status = res.status;
					frappe.show_alert({ message: res.message, indicator: 'red' });
				} catch (e) {
					frappe.msgprint({ title: "Rejection Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					attendanceApproval.sending = false;
				}
			}

			// ---------- Payroll Booking Approval Flow ----------
			async function loadPayrollApproval() {
				if (!filters.company || !filters.from_date || !filters.to_date) return;
				try {
					const res = await call("get_payroll_booking_approval_status", {
						company: filters.company,
						start_date: filters.from_date,
						end_date: filters.to_date
					});
					payrollApproval.approval_name = res.approval_name;
					payrollApproval.status = res.status;
					payrollApproval.requested_by = res.requested_by;
					payrollApproval.requested_on = res.requested_on;
					payrollApproval.approved_by = res.approved_by;
					payrollApproval.approved_on = res.approved_on;
				} catch (e) {
					console.error("loadPayrollApproval error:", e);
				}
			}

			async function sendPayrollForApproval() {
				if (!payrollEntry.value) {
					frappe.msgprint("Generate payroll first before sending for approval.");
					return;
				}
				if (!confirm(`Send payroll booking for approval?\n\nCompany: ${filters.company}\nPeriod: ${filters.from_date} to ${filters.to_date}\nEmployees: ${salaryRegister.slips.length}`)) return;
				payrollApproval.sending = true;
				try {
					const res = await call("send_payroll_for_approval", {
						company: filters.company,
						start_date: filters.from_date,
						end_date: filters.to_date,
						payroll_entry_name: payrollEntry.value,
						summary_data: {
							employees: salaryRegister.slips.map(s => s.employee),
							totals: salaryRegisterTotals.value
						}
					});
					payrollApproval.approval_name = res.approval_name;
					payrollApproval.status = res.status;
					frappe.show_alert({ message: res.message, indicator: 'blue' });
				} catch (e) {
					frappe.msgprint({ title: "Failed to Send", message: errMsg(e), indicator: 'red' });
				} finally {
					payrollApproval.sending = false;
				}
			}

			async function approvePayrollBooking() {
				if (!payrollApproval.approval_name) return;
				if (!confirm("Approve this payroll booking?\n\nThis will submit ALL draft salary slips and generate the accrual Journal Entry.")) return;
				payrollApproval.sending = true;
				try {
					// Step 1: Approve the payroll booking
					const res = await call("approve_payroll_booking", {
						approval_name: payrollApproval.approval_name
					});
					payrollApproval.status = res.status;
					payrollApproval.approved_by = frappe.session.user;
					frappe.show_alert({ message: "Payroll approved. Submitting slips and booking JE...", indicator: 'blue' });

					// Step 2: Submit all draft slips + create JE
					if (payrollEntry.value) {
						const bookRes = await call("book_payroll", { payroll_entry_name: payrollEntry.value });
						bookedJE.value = bookRes.journal_entry;
						frappe.show_alert({
							message: `Payroll approved & booked. JE: ${bookRes.journal_entry || 'N/A'}`,
							indicator: 'green'
						});
					}
					await loadSalaryRegister();
					await loadPayrollState();
				} catch (e) {
					frappe.msgprint({ title: "Approval Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					payrollApproval.sending = false;
				}
			}

			async function rejectPayrollBooking() {
				if (!payrollApproval.approval_name) return;
				const remarks = prompt("Reason for rejection (optional):");
				if (remarks === null) return;
				payrollApproval.sending = true;
				try {
					const res = await call("reject_payroll_booking", {
						approval_name: payrollApproval.approval_name,
						remarks: remarks
					});
					payrollApproval.status = res.status;
					frappe.show_alert({ message: res.message, indicator: 'red' });
				} catch (e) {
					frappe.msgprint({ title: "Rejection Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					payrollApproval.sending = false;
				}
			}

			async function toggleAttendanceView() {
				attendanceViewMode.value = attendanceViewMode.value === 'matrix' ? 'summary' : 'matrix';
				if (attendanceViewMode.value === 'summary' && !attendanceSummary.rows.length) {
					await loadAttendanceSummary();
				}
			}

			async function refreshSheet() {
				loading.value = true;
				try {
					await loadAttendance();
					await loadPayrollState();
					frappe.show_alert({ message: "Sheet refreshed", indicator: 'green' });
				} catch (e) {
					frappe.msgprint({ title: "Error", message: errMsg(e), indicator: 'red' });
				} finally {
					loading.value = false;
				}
			}

			async function showAttendanceDetail(emp, day) {
				const cell = cellData(emp, day);
				if (!cell) {
					frappe.msgprint("No attendance record for this day");
					return;
				}
				try {
					attendanceModal.data = await call("get_attendance_detail", { attendance_name: cell.name });
					attendanceModal.show = true;
				} catch (e) {
					frappe.msgprint({ title: "Error", message: errMsg(e), indicator: 'red' });
				}
			}

			function closeAttendanceModal() {
				attendanceModal.show = false;
				attendanceModal.data = null;
			}

			function toggleEmployee(name) {
				if (selectedEmployees.value.has(name)) {
					selectedEmployees.value.delete(name);
				} else {
					selectedEmployees.value.add(name);
				}
				selectedEmployees.value = new Set(selectedEmployees.value);
			}

			function selectAllEmployees() {
				selectedEmployees.value = new Set(employees.value.map(e => e.name));
			}

			function deselectAllEmployees() {
				selectedEmployees.value = new Set();
			}

			// ---------- Payroll Generation ----------
			async function generatePayroll() {
				if (!selectedEmployeeList.value.length) {
					frappe.msgprint("Select at least one employee");
					return;
				}
				// Req 8: block if attendance is not approved
				if (!attendanceApproved.value) {
					frappe.msgprint({
						title: "Attendance Not Approved",
						message: "Attendance summary must be approved before generating payroll. " +
							"Click 'Send for Approval' in the Attendance Summary section.",
						indicator: 'orange'
					});
					return;
				}
				// Req 3: block if any unapproved leaves or attendance requests exist
				if (hasUnapprovedItems.value) {
					const u = unapprovedTotal.value;
					frappe.msgprint({
						title: "Cannot Generate Payroll",
						message: `There are <b>${u.leaves} unapproved Leave Application(s)</b> and ` +
							`<b>${u.attReqs} unapproved Attendance Request(s)</b>.<br><br>` +
							`All leaves and attendance requests must be approved before payroll can be generated. ` +
							`Click the numbers in the Attendance Summary to open and approve them.`,
						indicator: 'red',
						wide: true
					});
					return;
				}
				actionLoading.value = true;
				try {
					const res = await call("generate_payroll", {
						employees: selectedEmployeeList.value,
						start_date: filters.from_date,
						end_date: filters.to_date,
						company: filters.company
					});
					payrollEntry.value = res.payroll_entry;
					let msg = `${res.created.length} salary slip(s) created in Draft`;
					let indicator = 'green';
					if (res.skipped && res.skipped.length) {
						msg += `, ${res.skipped.length} already existed (skipped)`;
						indicator = 'orange';
					}
					frappe.show_alert({ message: msg, indicator });

					// Prominent notification for employees skipped due to missing Salary Structure
					if (res.skipped_no_salary_structure && res.skipped_no_salary_structure.length) {
						const skippedList = res.skipped_no_salary_structure.join(', ');
						frappe.msgprint({
							title: "Action Required: Skipped Employees",
							message: `The following employees were <b>skipped</b> because they have no active Salary Structure Assignment:<br><br>
								<b>${skippedList}</b><br><br>
								Please assign a Salary Structure to these employees and click <b>Generate Payroll</b> again to include them.`,
							indicator: 'orange',
							wide: true
						});
					}
					await loadSalaryRegister();
				} catch (e) {
					const msg = errMsg(e);
					// Req 1: Check if this is the "payroll already exists" error
					if (msg.includes('Payroll already exists')) {
						frappe.msgprint({
							title: "Payroll Already Exists",
							message: msg + '<br><br><b>To regenerate:</b> Click the "Regenerate Payroll" button to delete existing slips and create fresh ones.',
							indicator: 'orange',
							wide: true
						});
					} else {
						frappe.msgprint({ title: "Payroll Generation Failed", message: msg, indicator: 'red' });
					}
				} finally {
					actionLoading.value = false;
				}
			}

			async function regeneratePayroll() {
				if (!selectedEmployeeList.value.length) {
					frappe.msgprint("Select at least one employee");
					return;
				}
				if (!attendanceApproved.value) {
					frappe.msgprint({
						title: "Attendance Not Approved",
						message: "Attendance summary must be approved before generating payroll.",
						indicator: 'orange'
					});
					return;
				}
				if (hasUnapprovedItems.value) {
					frappe.msgprint({
						title: "Cannot Regenerate Payroll",
						message: "There are unapproved leaves or attendance requests. Resolve them first.",
						indicator: 'red'
					});
					return;
				}
				if (!confirm(
					"Regenerate Payroll?\n\n" +
					"This will DELETE ALL existing salary slips and payroll entries for this period (across ALL companies) and create fresh ones.\n\n" +
					"Are you sure you want to continue?"
				)) return;
				actionLoading.value = true;
				try {
					const res = await call("regenerate_payroll", {
						employees: selectedEmployeeList.value,
						start_date: filters.from_date,
						end_date: filters.to_date,
						company: filters.company
					});
					payrollEntry.value = res.payroll_entry;
					bookedJE.value = null;
					let msg = `Payroll regenerated: ${res.deleted_slips} slip(s) deleted, ${res.deleted_payroll_entries} payroll entry/entries deleted, ${res.created.length} new slip(s) created`;
					frappe.show_alert({ message: msg, indicator: 'green' });

					if (res.skipped_no_salary_structure && res.skipped_no_salary_structure.length) {
						const skippedList = res.skipped_no_salary_structure.join(', ');
						frappe.msgprint({
							title: "Action Required: Skipped Employees",
							message: `The following employees were <b>skipped</b> because they have no active Salary Structure Assignment:<br><br>
								<b>${skippedList}</b><br><br>
								Please assign a Salary Structure to these employees and click <b>Generate Payroll</b> again to include them.`,
							indicator: 'orange',
							wide: true
						});
					}
					await loadSalaryRegister();
				} catch (e) {
					frappe.msgprint({ title: "Regeneration Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			// Submit attendance for selected employees
			async function submitSelectedAttendance() {
				const emps = Array.from(selectedAttendanceEmployees.value);
				if (!emps.length) {
					frappe.msgprint("Select employees using the checkboxes first.");
					return;
				}
				if (!confirm(`Submit all draft attendance records for ${emps.length} selected employee(s)?`)) return;
				actionLoading.value = true;
				try {
					const res = await call("submit_attendance_for_employees", {
						employees: emps,
						from_date: filters.from_date,
						to_date: filters.to_date
					});
					frappe.show_alert({
						message: `${res.submitted} attendance record(s) submitted`,
						indicator: 'green'
					});
					if (res.errors && res.errors.length) {
						frappe.msgprint({
							title: "Some records failed",
							message: res.errors.join('<br>'),
							indicator: 'orange',
							wide: true
						});
					}
					await loadAttendanceSummary();
				} catch (e) {
					frappe.msgprint({ title: "Submit Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			// Cancel attendance for selected employees
			async function cancelSelectedAttendance() {
				const emps = Array.from(selectedAttendanceEmployees.value);
				if (!emps.length) {
					frappe.msgprint("Select employees using the checkboxes first.");
					return;
				}
				if (!confirm(`Cancel all submitted attendance records for ${emps.length} selected employee(s)?`)) return;
				actionLoading.value = true;
				try {
					const res = await call("cancel_attendance_for_employees", {
						employees: emps,
						from_date: filters.from_date,
						to_date: filters.to_date
					});
					frappe.show_alert({
						message: `${res.cancelled} attendance record(s) cancelled`,
						indicator: 'orange'
					});
					if (res.errors && res.errors.length) {
						frappe.msgprint({
							title: "Some records failed",
							message: res.errors.join('<br>'),
							indicator: 'orange',
							wide: true
						});
					}
					await loadAttendanceSummary();
				} catch (e) {
					frappe.msgprint({ title: "Cancel Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			async function loadSalaryRegister() {
				try {
					const res = await call("get_salary_register", {
						start_date: filters.from_date,
						end_date: filters.to_date,
						company: filters.company,
					});
					salaryRegister.slips = res.slips || [];
					salaryRegister.earnings_columns = res.earnings_columns || [];
					salaryRegister.deductions_columns = res.deductions_columns || [];
				} catch (e) {
					console.error(e);
				}
			}

			// Req 1: Cancel individual salary slip
			async function cancelSlip(slipName, employeeName) {
				if (!confirm(`Cancel salary slip for ${employeeName}?\n\nAfter cancellation, you can regenerate payroll for this employee.`)) {
					return;
				}
				actionLoading.value = true;
				try {
					await call("cancel_salary_slip", { slip_name: slipName });
					frappe.show_alert({ message: `Salary slip cancelled for ${employeeName}`, indicator: 'orange' });
					await loadSalaryRegister();
					await loadPayrollState();
				} catch (e) {
					frappe.msgprint({ title: "Cancel Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			// Req 3: Update Arrear-Pay or Arrear-Deduct on a draft slip
			async function updateArrear(slipName, component, amount) {
				try {
					const res = await call("update_slip_arrear", {
						slip_name: slipName,
						component: component,
						amount: parseFloat(amount) || 0
					});
					// Update the slip in the local state
					const slip = salaryRegister.slips.find(s => s.name === slipName);
					if (slip) {
						// Update the arrear amount in earnings/deductions
						const list = component === 'Arrear-Pay' ? slip.earnings : slip.deductions;
						let found = false;
						for (let item of list) {
							if (item.component === component) {
								item.amount = parseFloat(amount) || 0;
								found = true;
								break;
							}
						}
						if (!found) {
							list.push({ component: component, amount: parseFloat(amount) || 0 });
						}
						slip.gross_pay = res.gross_pay;
						slip.total_deduction = res.total_deduction;
						slip.net_pay = res.net_pay;
						slip.rounded_total = res.rounded_total;
						// Recompute custom_total_deduction
						const pfEmp = (slip.earnings || []).find(e => e.component === 'PF - Employer')?.amount || 0;
						const pfEe = (slip.deductions || []).find(d => d.component === 'PF - Employee')?.amount || 0;
						const pt = (slip.deductions || []).find(d => d.component === 'Professional Tax')?.amount || 0;
						const ad = (slip.deductions || []).find(d => d.component === 'Arrear-Deduct')?.amount || 0;
						slip.custom_total_deduction = pfEmp + pfEe + pt + ad;
					}
					frappe.show_alert({ message: `${component} updated`, indicator: 'green' });
				} catch (e) {
					frappe.msgprint({ title: "Update Failed", message: errMsg(e), indicator: 'red' });
					await loadSalaryRegister();
				}
			}

			// Submit all draft salary slips
			async function submitDrafts() {
				const draftSlips = salaryRegister.slips.filter(s => s.docstatus === 0);
				if (!draftSlips.length) {
					frappe.msgprint("No draft salary slips to submit");
					return;
				}
				if (!confirm(`Submit ${draftSlips.length} draft salary slip(s)?\n\nThis will submit them and create/update the accrual Journal Entry (Draft).`)) {
					return;
				}
				actionLoading.value = true;
				try {
					const res = await call("submit_draft_slips", {
						payroll_entry_name: payrollEntry.value || '',
					});
					frappe.show_alert({
						message: `${res.submitted} slip(s) submitted${res.journal_entry ? ', JE: ' + res.journal_entry : ''}`,
						indicator: res.unsubmitted > 0 ? 'orange' : 'green'
					});
					if (res.errors && res.errors.length) {
						frappe.msgprint({
							title: "Some slips could not be submitted",
							message: res.errors.join('<br>'),
							indicator: 'orange',
							wide: true
						});
					}
					await loadSalaryRegister();
					await loadPayrollState();
				} catch (e) {
					frappe.msgprint({ title: "Submit Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			// Submit a single draft salary slip
			async function submitSingleSlip(slipName, employeeName) {
				actionLoading.value = true;
				try {
					const res = await call("submit_single_slip", { slip_name: slipName });
					if (res.submitted) {
						frappe.show_alert({ message: `Slip submitted for ${employeeName}`, indicator: 'green' });
					} else {
						frappe.msgprint({ title: "Submit Failed", message: res.error || 'Unknown error', indicator: 'red' });
					}
					await loadSalaryRegister();
					await loadPayrollState();
				} catch (e) {
					frappe.msgprint({ title: "Submit Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			// Submit selected draft slips
			async function submitSelectedSlips() {
				const drafts = selectedDraftSlips.value;
				if (!drafts.length) {
					frappe.msgprint("No selected draft slips to submit. Select slips using the checkboxes.");
					return;
				}
				if (!confirm(`Submit ${drafts.length} selected draft slip(s)?`)) return;
				actionLoading.value = true;
				let ok = 0, fail = 0;
				const errors = [];
				try {
					for (const slip of drafts) {
						try {
							await call("submit_single_slip", { slip_name: slip.name });
							ok++;
						} catch (e) {
							fail++;
							errors.push(`${slip.employee_name}: ${errMsg(e)}`);
						}
					}
					frappe.show_alert({
						message: `${ok} submitted, ${fail} failed`,
						indicator: fail > 0 ? 'orange' : 'green'
					});
					if (errors.length) {
						frappe.msgprint({ title: "Some slips failed", message: errors.join('<br>'), indicator: 'orange', wide: true });
					}
					selectedSlips.value = new Set();
					await loadSalaryRegister();
					await loadPayrollState();
				} finally {
					actionLoading.value = false;
				}
			}

			// Cancel selected submitted slips
			async function cancelSelectedSlips() {
				const submitted = selectedSubmittedSlips.value;
				if (!submitted.length) {
					frappe.msgprint("No selected submitted slips to cancel. Select slips using the checkboxes.");
					return;
				}
				if (!confirm(`Cancel ${submitted.length} selected submitted slip(s)?\n\nAfter cancellation, you can regenerate payroll for these employees.`)) return;
				actionLoading.value = true;
				let ok = 0, fail = 0;
				const errors = [];
				const reversalJEs = [];
				let jeRebuilt = false;
				try {
					for (const slip of submitted) {
						try {
							const res = await call("cancel_salary_slip", { slip_name: slip.name });
							ok++;
							if (res.reversal_je) reversalJEs.push(res.reversal_je);
							if (res.je_rebuilt) jeRebuilt = true;
						} catch (e) {
							fail++;
							errors.push(`${slip.employee_name}: ${errMsg(e)}`);
						}
					}
					let msg = `${ok} cancelled, ${fail} failed`;
					if (jeRebuilt) msg += ' — accrual JE rebuilt';
					if (reversalJEs.length) msg += ` — reversal JE(s): ${reversalJEs.join(', ')}`;
					frappe.show_alert({
						message: msg,
						indicator: fail > 0 ? 'orange' : 'green'
					});
					if (errors.length) {
						frappe.msgprint({ title: "Some slips failed", message: errors.join('<br>'), indicator: 'orange', wide: true });
					}
					selectedSlips.value = new Set();
					await loadSalaryRegister();
					await loadPayrollState();
				} finally {
					actionLoading.value = false;
				}
			}

			// Generate payroll for selected employees only (from salary register selection)
			async function generateForSelected() {
				const selectedEmps = salaryRegister.slips
					.filter(s => selectedSlips.value.has(s.name))
					.map(s => s.employee);
				if (!selectedEmps.length) {
					frappe.msgprint("Select slips using the checkboxes first.");
					return;
				}
				actionLoading.value = true;
				try {
					const res = await call("generate_payroll", {
						employees: selectedEmps,
						start_date: filters.from_date,
						end_date: filters.to_date,
						company: filters.company
					});
					payrollEntry.value = res.payroll_entry;
					frappe.show_alert({
						message: `${res.created.length} slip(s) created in Draft`,
						indicator: 'green'
					});
					selectedSlips.value = new Set();
					await loadSalaryRegister();
					await loadPayrollState();
				} catch (e) {
					const msg = errMsg(e);
					if (msg.includes('Payroll already exists')) {
						frappe.msgprint({
							title: "Payroll Already Exists",
							message: msg + '<br><br>Cancel the existing slip(s) first, then regenerate.',
							indicator: 'orange',
							wide: true
						});
					} else {
						frappe.msgprint({ title: "Payroll Generation Failed", message: msg, indicator: 'red' });
					}
				} finally {
					actionLoading.value = false;
				}
			}

			// Generate payroll for employees with cancelled slips (after approval)
			async function generatePending() {
				const cancelled = cancelledSlips.value;
				if (!cancelled.length) {
					frappe.msgprint("No cancelled slips found to regenerate.");
					return;
				}
				// Only generate for employees who have ONLY cancelled slips (no draft or submitted)
				const cancelledEmps = new Set(cancelled.map(s => s.employee));
				const hasActiveSlip = new Set(
					salaryRegister.slips
						.filter(s => (s.docstatus === 0 || s.docstatus === 1) && cancelledEmps.has(s.employee))
						.map(s => s.employee)
				);
				const toGenerate = cancelled.filter(s => !hasActiveSlip.has(s.employee));
				const alreadyExists = cancelled.filter(s => hasActiveSlip.has(s.employee));

				if (!toGenerate.length) {
					frappe.msgprint({
						title: "Nothing to Generate",
						message: `All cancelled employees already have a Draft or Submitted slip for this period.<br><br>
							${alreadyExists.map(s => s.employee_name).join(', ')}`,
						indicator: 'blue'
					});
					return;
				}

				const empList = toGenerate.map(s => `${s.employee_name} (${s.employee})`).join('\n');
				let confirmMsg = `Regenerate salary slip(s) for ${toGenerate.length} cancelled employee(s)?\n\n${empList}`;
				if (alreadyExists.length) {
					confirmMsg += `\n\nNote: ${alreadyExists.length} employee(s) already have a Draft/Submitted slip and will be skipped.`;
				}
				if (!confirm(confirmMsg)) return;

				const employees = toGenerate.map(s => s.employee);
				actionLoading.value = true;
				try {
					const res = await call("generate_payroll", {
						employees: employees,
						start_date: filters.from_date,
						end_date: filters.to_date,
						company: filters.company
					});
					payrollEntry.value = res.payroll_entry;
					let msg = `${res.created.length} slip(s) regenerated in Draft`;
					if (res.skipped && res.skipped.length) {
						msg += `, ${res.skipped.length} skipped`;
					}
					frappe.show_alert({ message: msg, indicator: 'green' });
					await loadSalaryRegister();
					await loadPayrollState();
				} catch (e) {
					frappe.msgprint({ title: "Generation Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			// ---------- Booking ----------
			async function bookPayroll() {
				if (!payrollEntry.value) {
					frappe.msgprint("Generate payroll first");
					return;
				}
				// Block if payroll booking not approved
				if (!payrollBookingApproved.value) {
					frappe.msgprint({
						title: "Payroll Booking Not Approved",
						message: "Payroll booking must be approved before booking. " +
							"Click 'Send for Approval' in the Payroll Booking section.",
						indicator: 'orange'
					});
					return;
				}
				// Req 3: block if any unapproved leaves or attendance requests exist
				if (hasUnapprovedItems.value) {
					const u = unapprovedTotal.value;
					frappe.msgprint({
						title: "Cannot Book Payroll",
						message: `There are <b>${u.leaves} unapproved Leave Application(s)</b> and ` +
							`<b>${u.attReqs} unapproved Attendance Request(s)</b>.<br><br>` +
							`All leaves and attendance requests must be approved before payroll can be booked.`,
						indicator: 'red',
						wide: true
					});
					return;
				}
				actionLoading.value = true;
				try {
					const res = await call("book_payroll", { payroll_entry_name: payrollEntry.value });
					bookedJE.value = res.journal_entry;
					if (res.already_booked) {
						frappe.show_alert({ message: "Payroll was already booked", indicator: 'blue' });
					} else {
						frappe.show_alert({ message: "Payroll booked successfully", indicator: 'green' });
					}
					await loadSalaryRegister();
				} catch (e) {
					frappe.msgprint({ title: "Booking Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					actionLoading.value = false;
				}
			}

			// ---------- Payment Release ----------
			function openReleaseModal() {
				if (!salaryRegister.slips.length) {
					frappe.msgprint("Generate and view salary register first");
					return;
				}
				const unpaidSlips = salaryRegister.slips.filter(s => s.custom_payment_status !== "Paid");
				if (!unpaidSlips.length) {
					frappe.msgprint("All slips are already paid");
					return;
				}
				// Build employee list with net payable + bank details from salary register
				releaseModal.employees = unpaidSlips.map(s => ({
					employee: s.employee,
					employee_name: s.employee_name,
					net_pay: s.net_pay,
					rounded_total: s.rounded_total,
					bank_ac_no: s.bank_ac_no || '',
					ifsc_code: s.ifsc_code || '',
					selected: true,
				}));
				releaseModal.selectedAll = true;
				releaseModal.show = true;
				releaseModal.mode = "Manual";
				releaseModal.bank_account = bankAccounts.value.find(b => b.is_default)?.name || "";
				releaseModal.reference_no = "";
				releaseModal.reference_date = frappe.datetime.get_today();
				releaseModal.payment_date = frappe.datetime.get_today();
			}

			function toggleReleaseEmployee(emp) {
				const row = releaseModal.employees.find(e => e.employee === emp);
				if (row) {
					row.selected = !row.selected;
					releaseModal.selectedAll = releaseModal.employees.every(e => e.selected);
				}
			}

			function toggleReleaseSelectAll() {
				const newVal = !releaseModal.selectedAll;
				releaseModal.selectedAll = newVal;
				releaseModal.employees.forEach(e => e.selected = newVal);
			}

			const releaseSelectedTotal = computed(() => {
				return releaseModal.employees
					.filter(e => e.selected)
					.reduce((sum, e) => sum + (e.rounded_total || e.net_pay || 0), 0);
			});

			const releaseSelectedCount = computed(() =>
				releaseModal.employees.filter(e => e.selected).length
			);

			function closeReleaseModal() {
				releaseModal.show = false;
				releaseModal.processing = false;
			}

			async function confirmReleasePayment() {
				if (!releaseModal.bank_account) {
					frappe.msgprint("Select a bank account");
					return;
				}
				const emps = releaseModal.employees
					.filter(e => e.selected)
					.map(e => e.employee);
				if (!emps.length) {
					frappe.msgprint("Select at least one employee to release payment");
					return;
				}

				// BTS mode — generate Bank Transfer Sheet
				if (releaseModal.mode === "BTS") {
					if (!releaseModal.payment_date) {
						frappe.msgprint("Payment Date is required for BTS");
						return;
					}
					releaseModal.processing = true;
					frappe.call({
						method: "teampro.api.payroll_workbench.release_bts",
						args: {
							employees: emps,
							bank_account: releaseModal.bank_account,
							payroll_entry_name: payrollEntry.value,
							company: filters.company,
							start_date: filters.from_date,
							end_date: filters.to_date,
							payment_date: releaseModal.payment_date,
						},
						callback: function(r) {
							releaseModal.processing = false;
							if (r.message) {
								var res = r.message;
								if (res.skipped && res.skipped.length) {
									const skipMsg = res.skipped.map(s => `${s.employee}: ${s.reason}`).join('<br>');
									frappe.msgprint({
										title: "BTS Generated (some employees skipped)",
										message: `${res.message}<br><br>Skipped:<br>${skipMsg}`,
										indicator: 'orange',
									});
								} else {
									frappe.show_alert({
										message: res.message || "BTS generated",
										indicator: 'green',
									});
								}
								// Set the payment JE from BTS response
								if (res.journal_entry) {
									paymentJE.value = res.journal_entry;
								}
								// Download the BTS Excel file via anchor tag
								if (res.file_url) {
									var fullUrl = window.location.origin + res.file_url;
									var a = document.createElement('a');
									a.href = fullUrl;
									a.download = res.file_url.split('/').pop();
									document.body.appendChild(a);
									a.click();
									document.body.removeChild(a);
								}
								closeReleaseModal();
								loadSalaryRegister();
								loadStatutoryReport();
							} else {
								frappe.msgprint({ title: "BTS Generation Failed", message: "No response from server.", indicator: 'red' });
							}
						},
						error: function(e) {
							releaseModal.processing = false;
							frappe.msgprint({ title: "BTS Generation Failed", message: errMsg(e), indicator: 'red' });
						}
					});
					return;
				}

				// Manual / Automated mode — release payment via JE
				if (!releaseModal.reference_no) {
					frappe.msgprint("Reference No is required for Bank Entry");
					return;
				}
				if (!releaseModal.reference_date) {
					frappe.msgprint("Reference Date is required for Bank Entry");
					return;
				}
				releaseModal.processing = true;
				try {
					const res = await call("release_payment", {
						employees: emps,
						mode: releaseModal.mode,
						bank_account: releaseModal.bank_account,
						reference_no: releaseModal.reference_no,
						reference_date: releaseModal.reference_date,
						payroll_entry_name: payrollEntry.value,
						company: filters.company,
						start_date: filters.from_date,
						end_date: filters.to_date
					});
					if (res.results) {
						res.results.forEach(r => {
							payoutStatus[r.employee] = {
								status: r.status,
								message: r.message,
								reference_number: r.reference_number || ""
							};
						});
					}
					frappe.show_alert({
						message: `Payment released (${releaseModal.mode}). JE: ${res.journal_entry}`,
						indicator: 'green'
					});
					paymentJE.value = res.journal_entry;
					closeReleaseModal();
					await loadSalaryRegister();
				} catch (e) {
					frappe.msgprint({ title: "Payment Release Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					releaseModal.processing = false;
				}
			}

			async function refreshPayoutStatus() {
				// Find the latest payment order if automated mode was used
				// We don't track PO name in UI state directly; reload register to sync
				await loadSalaryRegister();
				frappe.show_alert({ message: "Payout status refreshed", indicator: 'blue' });
			}

			// ---------- Statutory Payment (EPF / ESI) ----------
			async function loadStatutorySummary() {
				if (!filters.company || !filters.from_date || !filters.to_date) return;
				try {
					for (const ptype of ['EPF', 'ESI']) {
						const res = await call("get_statutory_payment_summary", {
							payment_type: ptype,
							start_date: filters.from_date,
							end_date: filters.to_date,
							company: filters.company,
							employees: selectedEmployeeList.value.length ? selectedEmployeeList.value : undefined,
						});
						statutorySummary[ptype.toLowerCase()] = res;
					}
				} catch (e) {
					console.error("loadStatutorySummary error:", e);
				}
			}

			function openStatutoryModal(payment_type) {
				const key = payment_type.toLowerCase();
				const summary = statutorySummary[key];
				if (!summary || summary.total <= 0) {
					frappe.msgprint(`No ${payment_type} amount found in submitted salary slips for this period.`);
					return;
				}
				statutoryModal.show = true;
				statutoryModal.payment_type = payment_type;
				statutoryModal.bank_account = bankAccounts.value.find(b => b.is_default)?.name || "";
				statutoryModal.reference_no = "";
				statutoryModal.reference_date = frappe.datetime.get_today();
				statutoryModal.processing = false;
			}

			function closeStatutoryModal() {
				statutoryModal.show = false;
				statutoryModal.processing = false;
			}

			async function confirmStatutoryRelease() {
				if (!statutoryModal.bank_account) {
					frappe.msgprint("Select a bank account");
					return;
				}
				if (!statutoryModal.reference_no) {
					frappe.msgprint("Reference No is required");
					return;
				}
				statutoryModal.processing = true;
				try {
					const res = await call("release_statutory_payment", {
						payment_type: statutoryModal.payment_type,
						bank_account: statutoryModal.bank_account,
						reference_no: statutoryModal.reference_no,
						reference_date: statutoryModal.reference_date,
						company: filters.company,
						start_date: filters.from_date,
						end_date: filters.to_date,
						employees: selectedEmployeeList.value.length ? selectedEmployeeList.value : undefined,
					});
					if (res.journal_entry) {
						const key = statutoryModal.payment_type.toLowerCase();
						statutoryJE[key] = res.journal_entry;
						frappe.show_alert({
							message: `${statutoryModal.payment_type} payment JE created (Draft): ${res.journal_entry} — ${fmtMoney(res.total)}`,
							indicator: 'green'
						});
					} else {
						frappe.msgprint(res.message || "No amount found for this payment type.");
					}
					closeStatutoryModal();
				} catch (e) {
					frappe.msgprint({ title: "Statutory Payment Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					statutoryModal.processing = false;
				}
			}

			// ---------- Statutory Report child table ----------
			async function loadStatutoryReport() {
				if (!payrollEntry.value) {
					statutoryReport.value = [];
					return;
				}
				try {
					const res = await call("get_statutory_report", {
						payroll_entry_name: payrollEntry.value
					});
					statutoryReport.value = res || [];
				} catch (e) {
					console.error("loadStatutoryReport error:", e);
					statutoryReport.value = [];
				}
			}

			async function saveStatutoryReport() {
				if (!payrollEntry.value) {
					frappe.msgprint("Generate payroll first to save statutory report");
					return;
				}
				statutoryReportSaving.value = true;
				try {
					const res = await call("save_statutory_report", {
						payroll_entry_name: payrollEntry.value,
						rows: statutoryReport.value
					});
					statutoryReport.value = res || [];
					frappe.show_alert({ message: "Statutory Report saved", indicator: 'green' });
				} catch (e) {
					frappe.msgprint({ title: "Save Failed", message: errMsg(e), indicator: 'red' });
				} finally {
					statutoryReportSaving.value = false;
				}
			}

			// ---------- Lifecycle ----------
			onMounted(async () => {
				defaultMonthRange();
				await loadCompanies();
				// Do NOT auto-load employees or payroll state on page load.
				// User must click "Load Employees" manually to avoid any
				// unintended JE-related actions on page load.
			});

			watch(() => filters.company, (nv) => {
				if (nv) loadBankAccounts();
			});

			// ---------- Return ----------
			return {
				loading, actionLoading, companies, bankAccounts,
				filters, employees, selectedEmployees,
				monthOptions, yearOptions,
				attendance, attendanceModal,
				attendanceViewMode, attendanceSummary,
				salaryRegister, payrollEntry, bookedJE, bookedJEStatus, paymentJE, paymentJEStatus, payoutStatus,
				showManual, openManual, closeManual,
				attendanceApproval, attendanceApproved, canApproveAttendance,
				sendForApproval, approveAttendance, rejectAttendance,
				payrollApproval, payrollBookingApproved, canApprovePayrollBooking,
				sendPayrollForApproval, approvePayrollBooking, rejectPayrollBooking,
				showRegisterActions, toggleRegisterActions, salaryComponentSummary, payrollMetrics,
				releaseModal,
				paymentTab, statutorySummary, statutoryJE, statutoryModal,
				statutoryReport, statutoryReportSaving,
				totalEmployees, selectedCount, selectedEmployeeList, monthDays,
				hasUnapprovedItems, unapprovedTotal,
				fmtDate, fmtMoney, statusColor, statusShort, cellData,
				openSlipInNewTab, openAttendanceInNewTab,
				openFilteredList, openUnapprovedLeaves, openUnapprovedAttRequests,
				openLeaveList, openAttendanceList, openAbsentList, openLatePenaltyList, openLatePenaltyDoc,
				loadEmployees, refreshSheet, loadPayrollState,
				showAttendanceDetail, closeAttendanceModal,
				toggleEmployee, selectAllEmployees, deselectAllEmployees,
				toggleAttendanceView, loadAttendanceSummary,
				generatePayroll, regeneratePayroll,
				bookPayroll, openReleaseModal, closeReleaseModal,
				confirmReleasePayment, refreshPayoutStatus,
				toggleReleaseEmployee, toggleReleaseSelectAll,
				releaseSelectedTotal, releaseSelectedCount,
				loadStatutorySummary, openStatutoryModal, closeStatutoryModal,
				confirmStatutoryRelease,
				loadStatutoryReport, saveStatutoryReport,
				triggerFileInput, uploadStatutoryFile, generateReturnFile,
				attendanceSearchQuery, salaryRegisterSearchQuery,
				filteredAttendanceRows, filteredSalarySlips,
				cancelSlip, updateArrear, submitDrafts,
				submitSingleSlip, submitSelectedSlips, cancelSelectedSlips, generateForSelected,
				generatePending,
				selectedSlips, toggleSlipSelection, toggleAllSlips,
				selectedDraftSlips, selectedSubmittedSlips, cancelledSlips,
				selectedAttendanceEmployees, toggleAttendanceSelection, toggleAllAttendance,
				submitSelectedAttendance, cancelSelectedAttendance,
				colLabel, salaryRegisterTotals, jeStatusLabel,
				STATUS_COLORS,
				attendanceColumnFilters, clearAttendanceColumnFilters,
				exportAttendanceExcel, exportSalaryRegisterExcel
			};
		},

		template: `
<div class="pw-container" style="padding: 15px; background: #f8fafc; min-height: calc(100vh - 60px);">

	<!-- Header / Filters -->
	<div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:15px; margin-bottom:15px;">
		<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
			<h2 style="margin:0; font-weight:700; color:#1e293b;">Payroll Workbench</h2>
			<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
				<span v-if="attendanceApproval.status === 'Approved'" style="background:#dcfce7; color:#166534; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Attendance Approved ✓
				</span>
				<span v-else-if="attendanceApproval.status === 'Pending for Approval'" style="background:#fef3c7; color:#92400e; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Attendance Pending Approval
				</span>
				<span v-else-if="attendanceApproval.status === 'Rejected'" style="background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Attendance Rejected
				</span>
				<span v-else-if="attendanceApproval.status === 'Draft'" style="background:#f1f5f9; color:#475569; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Attendance Draft
				</span>
				<span v-if="payrollApproval.status === 'Approved'" style="background:#dcfce7; color:#166534; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Payroll Approved ✓
				</span>
				<span v-else-if="payrollApproval.status === 'Pending for Approval'" style="background:#fef3c7; color:#92400e; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Payroll Pending Approval
				</span>
				<span v-else-if="payrollApproval.status === 'Rejected'" style="background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Payroll Rejected
				</span>
				<span v-else-if="payrollApproval.status === 'Draft'" style="background:#f1f5f9; color:#475569; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600;">
					Payroll Draft
				</span>
				<span v-if="bookedJE" :style="{ background: bookedJEStatus === 1 ? '#dcfce7' : '#dbeafe', color: bookedJEStatus === 1 ? '#166534' : '#1e40af', padding: '4px 12px', borderRadius: '6px', fontSize: '12px', fontWeight: '600' }">
					Payroll Booked: {{ bookedJE }} ({{ jeStatusLabel(bookedJEStatus) }})
				</span>
				<span v-if="paymentJE" :style="{ background: paymentJEStatus === 1 ? '#dcfce7' : '#dbeafe', color: paymentJEStatus === 1 ? '#166534' : '#1e40af', padding: '4px 12px', borderRadius: '6px', fontSize: '12px', fontWeight: '600' }">
					Salary Released: {{ paymentJE }} ({{ jeStatusLabel(paymentJEStatus) }})
				</span>
				<button class="btn btn-secondary btn-sm" @click="refreshSheet" :disabled="loading">
					Refresh Sheet
				</button>
				<button class="btn btn-info btn-sm" @click="openManual" style="color:#fff; background:#0ea5e9; border-color:#0ea5e9;">
					<i class="fa fa-book"></i> User Manual
				</button>
			</div>
		</div>

		<div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:12px;">
			<div style="display:flex; flex-direction:column;">
				<label style="font-size:11px; color:#64748b; margin-bottom:2px;">Company</label>
				<select v-model="filters.company" class="form-control" style="width:160px; height:32px; line-height:20px; padding:5px 8px;">
					<option value="">-- Select --</option>
					<option v-for="c in companies" :key="c.name" :value="c.name">{{ c.name }}</option>
				</select>
			</div>
			<div style="display:flex; flex-direction:column;">
				<label style="font-size:11px; color:#64748b; margin-bottom:2px;">Branch</label>
				<input v-model="filters.branch" class="form-control" style="width:140px; height:32px; line-height:20px; padding:5px 8px;" placeholder="Branch">
			</div>
			<div style="display:flex; flex-direction:column;">
				<label style="font-size:11px; color:#64748b; margin-bottom:2px;">Department</label>
				<input v-model="filters.department" class="form-control" style="width:140px; height:32px; line-height:20px; padding:5px 8px;" placeholder="Department">
			</div>
			<div style="display:flex; flex-direction:column;">
				<label style="font-size:11px; color:#64748b; margin-bottom:2px;">Designation</label>
				<input v-model="filters.designation" class="form-control" style="width:140px; height:32px; line-height:20px; padding:5px 8px;" placeholder="Designation">
			</div>
			<div style="display:flex; flex-direction:column;">
				<label style="font-size:11px; color:#64748b; margin-bottom:2px;">Grade</label>
				<input v-model="filters.grade" class="form-control" style="width:120px; height:32px; line-height:20px; padding:5px 8px;" placeholder="Grade">
			</div>
			<div style="display:flex; flex-direction:column;">
				<label style="font-size:11px; color:#64748b; margin-bottom:2px;">Month</label>
				<select v-model="filters.month" class="form-control" style="width:130px; height:32px; line-height:20px; padding:5px 8px;">
					<option value="" disabled>Select Month</option>
					<option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
				</select>
			</div>
			<div style="display:flex; flex-direction:column;">
				<label style="font-size:11px; color:#64748b; margin-bottom:2px;">Year</label>
				<select v-model="filters.year" class="form-control" style="width:100px; height:32px; line-height:20px; padding:5px 8px;">
					<option value="" disabled>Year</option>
					<option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
				</select>
			</div>
			<div style="display:flex; align-items:flex-end;">
				<button class="btn btn-primary" @click="loadEmployees" :disabled="loading">
					{{ loading ? 'Loading...' : 'Load Employees' }}
				</button>
			</div>
		</div>
	</div>

	<!-- Loading overlay -->
	<div v-if="loading" style="text-align:center; padding:40px; color:#64748b;">
		<i class="fa fa-spinner fa-spin" style="font-size:24px;"></i>
		<p style="margin-top:10px;">Loading data...</p>
	</div>

	<!-- Section A: Attendance -->
	<div v-if="employees.length && !loading" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:15px; margin-bottom:15px;">
		<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
			<h3 style="margin:0; font-size:16px; font-weight:700; color:#1e293b;">
				{{ attendanceViewMode === 'matrix' ? 'Attendance Matrix' : 'Attendance Summary' }}
				<span style="font-size:12px; color:#64748b; font-weight:400;">
					({{ totalEmployees }} employees, {{ monthDays.length }} days)
				</span>
			</h3>
			<div style="display:flex; gap:6px; align-items:center;">
				<button class="btn btn-default btn-sm" :class="{ 'btn-primary': attendanceViewMode === 'matrix' }"
					@click="toggleAttendanceView" :disabled="loading">
					{{ attendanceViewMode === 'matrix' ? 'Switch to Summary View' : 'Switch to Matrix View' }}
				</button>
				<button class="btn btn-default btn-sm" @click="selectAllEmployees">Select All</button>
				<button class="btn btn-default btn-sm" @click="deselectAllEmployees">Clear</button>
				<span style="font-size:12px; color:#64748b;">
					{{ selectedCount }} selected
				</span>
			</div>
		</div>

		<!-- ===== Matrix View ===== -->
		<template v-if="attendanceViewMode === 'matrix'">
			<!-- Summary Cards -->
			<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
				<div v-for="(count, status) in attendance.summary" :key="status"
					style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 14px; min-width:100px;">
					<div style="font-size:11px; color:#64748b;">{{ status }}</div>
					<div style="font-size:18px; font-weight:700;" :style="{ color: statusColor(status) }">{{ count }}</div>
				</div>
			</div>

			<!-- Matrix Table -->
			<div style="overflow:auto; max-height:500px; border:1px solid #e2e8f0; border-radius:6px;">
				<table style="border-collapse:collapse; width:100%; font-size:12px;">
					<thead style="position:sticky; top:0; z-index:10;">
						<tr style="background:#1e293b; color:#fff;">
							<th style="padding:6px; border:1px solid #334155; position:sticky; left:0; z-index:11; background:#1e293b; min-width:180px; text-align:left;">
								Employee
							</th>
							<th style="padding:6px; border:1px solid #334155; min-width:40px;">✓</th>
							<th v-for="day in monthDays" :key="day" style="padding:4px; border:1px solid #334155; min-width:36px; text-align:center;">
								{{ day.split('-')[2] }}
							</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="emp in employees" :key="emp.name"
							style="background:#fff;" :style="{ background: selectedEmployees.has(emp.name) ? '#fff' : '#f1f5f9' }">
							<td style="padding:6px; border:1px solid #e2e8f0; position:sticky; left:0; background:inherit; font-weight:500;">
								{{ emp.employee_name }}
								<div style="font-size:10px; color:#94a3b8;">{{ emp.name }}</div>
							</td>
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center;">
								<input type="checkbox" :checked="selectedEmployees.has(emp.name)"
									@change="toggleEmployee(emp.name)">
							</td>
							<td v-for="day in monthDays" :key="day"
								@click="showAttendanceDetail(emp.name, day)"
								style="padding:2px; border:1px solid #e2e8f0; text-align:center; cursor:pointer; font-weight:600; font-size:11px;"
								:style="{ background: cellData(emp.name, day) ? statusColor(cellData(emp.name, day).status) : statusColor('Unmarked'), color: cellData(emp.name, day) ? '#fff' : '#94a3b8' }"
								:title="cellData(emp.name, day) ? cellData(emp.name, day).status : 'Unmarked'">
								{{ cellData(emp.name, day) ? statusShort(cellData(emp.name, day).status) : '-' }}
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<!-- Legend -->
			<div style="display:flex; gap:12px; margin-top:8px; flex-wrap:wrap;">
				<span v-for="(color, status) in STATUS_COLORS" :key="status" style="display:flex; align-items:center; gap:4px; font-size:11px;">
					<span :style="{ background: color, width: '12px', height: '12px', borderRadius: '3px', display:'inline-block' }"></span>
					{{ status }} ({{ statusShort(status) }})
				</span>
			</div>
		</template>

		<!-- ===== Summary View ===== -->
		<template v-if="attendanceViewMode === 'summary'">
			<p style="font-size:12px; color:#64748b; margin-bottom:10px;">
				Per-employee attendance totals for the selected period. Payment Days = Present + Paid Leave + Holidays - Late Penalty Days.
			</p>

			<!-- Req 2: Search by name + attendance actions -->
			<div style="margin-bottom:10px; display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
				<input type="text" v-model="attendanceSearchQuery" placeholder="Search by employee name or ID..."
					style="padding:6px 10px; border:1px solid #cbd5e1; border-radius:4px; font-size:12px; width:280px;" />
				<span v-if="attendanceSearchQuery" style="font-size:11px; color:#64748b;">
					Showing {{ filteredAttendanceRows.length }} of {{ attendanceSummary.rows.length }}
				</span>
				<button v-if="attendanceSummary.rows.length"
					class="btn btn-default btn-sm" @click="exportAttendanceExcel"
					title="Download attendance summary as Excel">
					<i class="fa fa-file-excel-o" style="color:#10b981;"></i> Excel
				</button>
				<span v-if="selectedAttendanceEmployees.size" style="font-size:11px; color:#1e40af; font-weight:600;">
					{{ selectedAttendanceEmployees.size }} selected
				</span>
				<button v-if="selectedAttendanceEmployees.size"
					class="btn btn-success btn-sm" @click="submitSelectedAttendance"
					:disabled="actionLoading"
					title="Submit all draft attendance for selected employees">
					Submit Attendance
				</button>
				<button v-if="selectedAttendanceEmployees.size"
					class="btn btn-warning btn-sm" @click="cancelSelectedAttendance"
					:disabled="actionLoading"
					title="Cancel all submitted attendance for selected employees">
					Cancel Attendance
				</button>
				<!-- Approval actions -->
				<div style="margin-left:auto; display:flex; gap:8px; align-items:center;">
					<span v-if="attendanceApproval.status === 'Approved'" style="font-size:12px; color:#166534;">
						Approved by {{ attendanceApproval.approved_by }}
					</span>
					<span v-else-if="attendanceApproval.status === 'Pending for Approval'" style="font-size:12px; color:#92400e;">
						Sent on {{ attendanceApproval.requested_on }}
					</span>
					<!-- Send button: visible when not approved and not pending -->
					<button v-if="!attendanceApproval.status || attendanceApproval.status === 'Draft' || attendanceApproval.status === 'Rejected'"
						class="btn btn-info btn-sm"
						@click="sendForApproval"
						:disabled="attendanceApproval.sending || !attendanceSummary.rows.length || hasUnapprovedItems"
						:title="hasUnapprovedItems ? 'Resolve all unapproved items first' : 'Send attendance summary for approval'">
						{{ attendanceApproval.sending ? 'Sending...' : 'Send for Approval' }}
					</button>
					<!-- Approve / Reject buttons: visible when pending -->
					<template v-if="attendanceApproval.status === 'Pending for Approval'">
						<button class="btn btn-success btn-sm"
							@click="approveAttendance"
							:disabled="attendanceApproval.sending">
							{{ attendanceApproval.sending ? 'Processing...' : 'Approve' }}
						</button>
						<button class="btn btn-danger btn-sm"
							@click="rejectAttendance"
							:disabled="attendanceApproval.sending">
							Reject
						</button>
					</template>
				</div>
			</div>

			<!-- Req 3: Unapproved items warning banner -->
			<div v-if="hasUnapprovedItems" style="background:#fef2f2; border:1px solid #fecaca; border-radius:6px; padding:10px 14px; margin-bottom:10px; display:flex; align-items:center; gap:10px;">
				<i class="fa fa-exclamation-triangle" style="color:#dc2626; font-size:16px;"></i>
				<span style="font-size:13px; color:#991b1b;">
					<b>Cannot proceed with payroll:</b> {{ unapprovedTotal.leaves }} unapproved Leave Application(s) and
					{{ unapprovedTotal.attReqs }} unapproved Attendance Request(s).
					Click the red numbers below to open and approve them. All unapproved items must be resolved (zero) before Generate/Book Payroll.
				</span>
			</div>

			<div style="overflow:auto; max-height:500px; border:1px solid #e2e8f0; border-radius:6px;">
				<table style="border-collapse:collapse; width:100%; font-size:12px;">
					<thead style="position:sticky; top:0; z-index:10;">
						<tr style="background:#1e293b; color:#fff;">
							<th style="padding:6px 10px; border:1px solid #334155; min-width:40px; text-align:center;">
								<input type="checkbox" @change="toggleAllAttendance"
									:checked="selectedAttendanceEmployees.size === filteredAttendanceRows.length && filteredAttendanceRows.length > 0" />
							</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:160px; text-align:left;">Employee</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:80px; text-align:left;">Department</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:90px; text-align:right;">Calendar Days</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:70px; text-align:right;">Holidays</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:70px; text-align:right;">Present</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:80px; text-align:right;">Paid Leave</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:90px; text-align:right;">Absent / Unpaid</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:80px; text-align:right;">Late Count</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:100px; text-align:right;">Late Penalty Days</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:110px; text-align:right;">Penalty Amount</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:110px; text-align:right; background:#7f1d1d;">Unapproved Leaves</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:130px; text-align:right; background:#7f1d1d;">Unapproved Att. Requests</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:90px; text-align:right; background:#0f172a;">Payment Days</th>
						</tr>
						<!-- Column filter row -->
						<tr style="background:#334155;">
							<th style="padding:3px; border:1px solid #334155; text-align:center;">
								<button class="btn btn-xs btn-default" @click="clearAttendanceColumnFilters" title="Clear all filters"
									style="padding:2px 6px; font-size:10px;">×</button>
							</th>
							<th style="padding:3px; border:1px solid #334155;"><input v-model="attendanceColumnFilters.employee_name" placeholder="Filter..." style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input v-model="attendanceColumnFilters.department" placeholder="Filter..." style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.calendar_days" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.holidays" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.present" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.paid_leave" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.absent_unpaid" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.late_count" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.late_penalty_days" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155;"><input type="number" v-model="attendanceColumnFilters.late_penalty_amount" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155; background:#7f1d1d;"><input type="number" v-model="attendanceColumnFilters.unapproved_leaves" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155; background:#7f1d1d;"><input type="number" v-model="attendanceColumnFilters.unapproved_attendance_requests" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
							<th style="padding:3px; border:1px solid #334155; background:#0f172a;"><input type="number" v-model="attendanceColumnFilters.payment_days" placeholder="≥" style="width:100%; padding:3px 6px; font-size:11px; border:1px solid #475569; border-radius:3px; background:#1e293b; color:#e2e8f0;"></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="row in filteredAttendanceRows" :key="row.employee"
							:style="{ background: selectedAttendanceEmployees.has(row.employee) ? '#eff6ff' : (selectedEmployees.has(row.employee) ? '#fff' : '#f1f5f9') }">
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:center;">
								<input type="checkbox" :checked="selectedAttendanceEmployees.has(row.employee)"
									@change="toggleAttendanceSelection(row.employee)" />
							</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; font-weight:500;">
								{{ row.employee_name }}
								<div style="font-size:10px; color:#94a3b8;">{{ row.employee }}</div>
							</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; color:#64748b;">{{ row.department }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right;">{{ row.calendar_days }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; color:#8b5cf6; font-weight:600;">{{ row.holidays }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; color:#10b981; font-weight:600; cursor:pointer;" @click="openAttendanceList(row.employee, 'Present')">{{ row.present }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; color:#3b82f6; font-weight:600; cursor:pointer;" @click="openLeaveList(row.employee)">{{ row.paid_leave }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; color:#ef4444; font-weight:600; cursor:pointer;" @click="openAbsentList(row.employee, row)">{{ row.absent_unpaid }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; font-weight:600;">{{ row.late_count }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; color:#f59e0b; font-weight:600; cursor:pointer;"
								@click="row.late_penalty_name ? openLatePenaltyDoc(row.late_penalty_name) : openLatePenaltyList(row.employee)"
								:title="row.late_penalty_name ? 'Click to edit Late Penalty record' : 'No Late Penalty record — click to open list'">
								{{ row.late_penalty_days }}
							</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; color:#f59e0b; font-weight:600; cursor:pointer;"
								@click="row.late_penalty_name ? openLatePenaltyDoc(row.late_penalty_name) : openLatePenaltyList(row.employee)">
								{{ fmtMoney(row.late_penalty_amount || 0) }}
							</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; font-weight:600; cursor:pointer;"
								:style="{ color: row.unapproved_leaves > 0 ? '#dc2626' : '#94a3b8', textDecoration: row.unapproved_leaves > 0 ? 'underline' : 'none' }"
								@click="row.unapproved_leaves > 0 && openUnapprovedLeaves(row.employee)">
								{{ row.unapproved_leaves }}
							</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; font-weight:600; cursor:pointer;"
								:style="{ color: row.unapproved_attendance_requests > 0 ? '#dc2626' : '#94a3b8', textDecoration: row.unapproved_attendance_requests > 0 ? 'underline' : 'none' }"
								@click="row.unapproved_attendance_requests > 0 && openUnapprovedAttRequests(row.employee)">
								{{ row.unapproved_attendance_requests }}
							</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; font-weight:700; font-size:14px; background:#f0fdf4; color:#166534;">
								{{ row.payment_days }}
							</td>
						</tr>
					</tbody>
					<tfoot v-if="attendanceSummary.totals && attendanceSummary.totals.calendar_days">
						<tr style="background:#1e293b; color:#fff; font-weight:700;">
							<td style="padding:6px 10px; border:1px solid #334155;" colspan="3">TOTALS</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ attendanceSummary.totals.calendar_days }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ attendanceSummary.totals.holidays }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ attendanceSummary.totals.present }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ attendanceSummary.totals.paid_leave }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ attendanceSummary.totals.absent_unpaid }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ attendanceSummary.totals.late_count }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ attendanceSummary.totals.late_penalty_days }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right;">{{ fmtMoney(attendanceSummary.totals.late_penalty_amount || 0) }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right; background:#7f1d1d;">{{ attendanceSummary.totals.unapproved_leaves }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right; background:#7f1d1d;">{{ attendanceSummary.totals.unapproved_attendance_requests }}</td>
							<td style="padding:6px 10px; border:1px solid #334155; text-align:right; background:#0f172a;">{{ attendanceSummary.totals.payment_days }}</td>
						</tr>
					</tfoot>
				</table>
			</div>

			<!-- Summary legend -->
			<div style="margin-top:8px; font-size:11px; color:#64748b; line-height:1.6;">
				<strong style="color:#8b5cf6;">Holidays</strong>: From Holiday List, only after Date of Joining; excludes holidays sandwiched between leave days &nbsp;|&nbsp;
				<strong style="color:#10b981;">Present</strong>: Present + WFH + Half Day (0.5) — click to open Attendance list &nbsp;|&nbsp;
				<strong style="color:#3b82f6;">Paid Leave</strong>: On Leave with non-LWP leave type — click to open Leave list &nbsp;|&nbsp;
				<strong style="color:#ef4444;">Absent / Unpaid</strong>: Absent + LWP leave — click to open Attendance list &nbsp;|&nbsp;
				<strong style="color:#f59e0b;">Late Penalty Days / Amount</strong>: From Late Penalty document — click to open and edit the record &nbsp;|&nbsp;
				<strong style="color:#dc2626;">Unapproved Leaves / Att. Requests</strong>: Click red numbers to open and approve. Must be zero before payroll. &nbsp;|&nbsp;
				<strong style="color:#166534;">Payment Days</strong>: Present + Paid Leave + Holidays - Late Penalty Days
			</div>
		</template>
	</div>

	<!-- Attendance not approved notice (only shows when no salary slips exist yet AND attendance not approved) -->
	<div v-if="employees.length && !loading && !attendanceApproved && !salaryRegister.slips.length" style="background:#fef3c7; border:1px solid #fde68a; border-radius:8px; padding:20px; margin-bottom:15px; text-align:center;">
		<i class="fa fa-info-circle" style="font-size:24px; color:#92400e; margin-bottom:10px;"></i>
		<h3 style="margin:0 0 8px; font-size:16px; font-weight:700; color:#92400e;">Salary Register Yet to Generate</h3>
		<p style="font-size:13px; color:#92400e; margin:0;">
			Attendance summary must be approved before payroll can be generated.
			<br>Click <b>"Send for Approval"</b> in the Attendance Summary above to start the approval process.
		</p>
	</div>

	<!-- Section B: Salary Register (shows when attendance approved OR salary slips already exist) -->
	<div v-if="employees.length && !loading && (attendanceApproved || salaryRegister.slips.length)" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:15px; margin-bottom:15px;">
		<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
			<h3 style="margin:0; font-size:16px; font-weight:700; color:#1e293b;">Salary Register</h3>
			<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
				<button v-if="!payrollEntry" class="btn btn-primary" @click="generatePayroll"
					:disabled="actionLoading || hasUnapprovedItems"
					:title="hasUnapprovedItems ? 'Resolve all unapproved leaves and attendance requests first' : ''">
					{{ actionLoading ? 'Processing...' : 'Generate Payroll' }}
				</button>

				<!-- Payroll booking approval status badge -->
				<span v-if="payrollApproval.status === 'Approved'" style="background:#dcfce7; color:#166534; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600;">
					Payroll Booking Approved ✓
				</span>
				<span v-else-if="payrollApproval.status === 'Pending for Approval'" style="background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600;">
					Pending Approval
				</span>
				<span v-else-if="payrollApproval.status === 'Rejected'" style="background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600;">
					Rejected
				</span>

				<!-- Combined "Send for Approval / Regenerate Payroll" actions menu — only before the
				     booking has been sent/approved -->
				<div v-if="payrollEntry && (!payrollApproval.status || payrollApproval.status === 'Draft' || payrollApproval.status === 'Rejected')"
					class="pw-register-actions" style="position:relative;">
					<button class="btn btn-default" @click="toggleRegisterActions"
						:disabled="actionLoading || hasUnapprovedItems">
						Actions <i class="fa fa-caret-down"></i>
					</button>
					<div v-if="showRegisterActions" style="position:absolute; right:0; top:100%; margin-top:4px; background:#fff; border:1px solid #e2e8f0; border-radius:6px; box-shadow:0 2px 10px rgba(0,0,0,0.15); z-index:50; min-width:190px; overflow:hidden;">
						<a href="#" @click.prevent="showRegisterActions = false; sendPayrollForApproval()"
							style="display:block; padding:8px 12px; font-size:12px; color:#1e293b; text-decoration:none;"
							title="Send payroll for CEO approval">
							{{ payrollApproval.sending ? 'Sending...' : 'Send for Approval' }}
						</a>
						<a href="#" @click.prevent="showRegisterActions = false; regeneratePayroll()"
							style="display:block; padding:8px 12px; font-size:12px; color:#1e293b; text-decoration:none; border-top:1px solid #f1f5f9;"
							title="Delete all existing slips and payroll entries for this period and create fresh ones">
							Regenerate Payroll
						</a>
					</div>
				</div>

				<!-- Approve / Reject — only visible to CEO role while pending -->
				<template v-if="payrollApproval.status === 'Pending for Approval' && canApprovePayrollBooking">
					<button class="btn btn-success btn-sm"
						@click="approvePayrollBooking"
						:disabled="payrollApproval.sending">
						{{ payrollApproval.sending ? 'Processing...' : 'Approve' }}
					</button>
					<button class="btn btn-danger btn-sm"
						@click="rejectPayrollBooking"
						:disabled="payrollApproval.sending">
						Reject
					</button>
				</template>

				<!-- Submit Selected — available to CEO (no prior approval needed) or after booking approved -->
				<template v-if="canApprovePayrollBooking || payrollBookingApproved">
					<button v-if="selectedDraftSlips.length"
						class="btn btn-success btn-sm" @click="submitSelectedSlips"
						:disabled="actionLoading"
						title="Submit selected draft slips and create/update accrual JE">
						Submit Selected ({{ selectedDraftSlips.length }})
					</button>
				</template>
				<button v-if="selectedSubmittedSlips.length"
					class="btn btn-warning btn-sm" @click="cancelSelectedSlips"
					:disabled="actionLoading"
					title="Cancel selected submitted slips">
					Cancel Selected ({{ selectedSubmittedSlips.length }})
				</button>
				<button v-if="selectedSlips.size"
					class="btn btn-primary btn-sm" @click="generateForSelected"
					:disabled="actionLoading"
					title="Regenerate payroll for selected employees (after cancelling)">
					Regenerate Selected
				</button>
				<!-- Generate Pending — shows when there are cancelled slips that need regeneration -->
				<button v-if="cancelledSlips.length && (canApprovePayrollBooking || payrollBookingApproved)"
					class="btn btn-primary btn-sm" @click="generatePending"
					:disabled="actionLoading"
					title="Generate salary slips for employees with cancelled slips">
					Generate Pending ({{ cancelledSlips.length }})
				</button>
				<span v-if="!payrollBookingApproved && !canApprovePayrollBooking && payrollEntry && salaryRegister.slips.some(s => s.docstatus === 0)" style="font-size:11px; color:#dc2626;">
					<i class="fa fa-lock"></i> Approval required to submit slips
				</span>
				<span v-if="hasUnapprovedItems" style="font-size:11px; color:#dc2626;">
					<i class="fa fa-lock"></i> Blocked — unapproved items pending
				</span>
			</div>
		</div>

		<p style="font-size:12px; color:#64748b; margin:0 0 10px;">
			CEO can approve payroll in two ways: (1) Click <b>Approve</b> to submit all draft slips and generate the accrual JE at once, or (2) Select individual slips via checkboxes and click <b>Submit Selected</b> to submit only those. A Draft accrual JE (Salary Expense debit, EPF/PT/Payable credits) is created/updated automatically.
		</p>

		<div v-if="payrollEntry" style="font-size:12px; color:#64748b; margin-bottom:8px;">
			Payroll Entry: <a :href="'/app/payroll-entry/' + payrollEntry" target="_blank">{{ payrollEntry }}</a>
		</div>

		<div v-if="salaryRegister.slips.length === 0" style="padding:20px; text-align:center; color:#94a3b8;">
			No salary slips generated yet. Click "Generate Payroll" to create draft slips.
		</div>

		<div v-else>
			<!-- Req 2: Search by name -->
			<div style="margin-bottom:10px; display:flex; align-items:center; gap:8px;">
				<input type="text" v-model="salaryRegisterSearchQuery" placeholder="Search by employee name or ID..."
					style="padding:6px 10px; border:1px solid #cbd5e1; border-radius:4px; font-size:12px; width:280px;" />
				<span v-if="salaryRegisterSearchQuery" style="font-size:11px; color:#64748b;">
					Showing {{ filteredSalarySlips.length }} of {{ salaryRegister.slips.length }}
				</span>
				<button class="btn btn-default btn-sm" @click="exportSalaryRegisterExcel"
					title="Download salary register as Excel">
					<i class="fa fa-file-excel-o" style="color:#10b981;"></i> Excel
				</button>
			</div>

			<div style="overflow:auto; max-height:450px; border:1px solid #e2e8f0; border-radius:6px;">
				<table style="border-collapse:collapse; width:100%; font-size:12px;">
					<thead style="position:sticky; top:0; z-index:10;">
						<tr style="background:#1e293b; color:#fff;">
							<th style="padding:6px; border:1px solid #334155; min-width:40px; text-align:center;">
								<input type="checkbox" @change="toggleAllSlips"
									:checked="selectedSlips.size === filteredSalarySlips.length && filteredSalarySlips.length > 0" />
							</th>
							<th style="padding:6px; border:1px solid #334155; min-width:100px; text-align:left;">Emp ID</th>
							<th style="padding:6px; border:1px solid #334155; min-width:150px; text-align:left;">Employee Name</th>
							<th style="padding:6px; border:1px solid #334155; min-width:100px; text-align:right;">Fixed Gross</th>
							<th style="padding:6px; border:1px solid #334155; min-width:70px; text-align:center;">Days</th>
							<th v-for="col in salaryRegister.earnings_columns" :key="'e-'+col" style="padding:6px; border:1px solid #334155; min-width:90px; text-align:right;"
								:style="{ background: col === 'Arrear-Pay' ? '#1e3a5f' : '' }">
								{{ colLabel(col) }}
							</th>
							<th v-for="col in salaryRegister.deductions_columns" :key="'d-'+col" style="padding:6px; border:1px solid #334155; min-width:90px; text-align:right;"
								:style="{ background: col === 'Arrear-Deduct' ? '#1e3a5f' : '' }">
								{{ colLabel(col) }}
							</th>
							<th style="padding:6px; border:1px solid #334155; min-width:90px; text-align:right;">Gross CTC</th>
							<th style="padding:6px; border:1px solid #334155; min-width:100px; text-align:right;">Total Deduction</th>
							<th style="padding:6px; border:1px solid #334155; min-width:90px; text-align:right; background:#3730a3;">Net Total</th>
							<th style="padding:6px; border:1px solid #334155; min-width:80px; text-align:center;">Status</th>
							<th style="padding:6px; border:1px solid #334155; min-width:90px; text-align:center;">Payment</th>
							<th style="padding:6px; border:1px solid #334155; min-width:80px; text-align:center;">Slip</th>
							<th style="padding:6px; border:1px solid #334155; min-width:80px; text-align:center;">Submit</th>
							<th style="padding:6px; border:1px solid #334155; min-width:80px; text-align:center;">Cancel</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="slip in filteredSalarySlips" :key="slip.name"
							:style="{ background: slip.docstatus === 2 ? '#fef2f2' : (selectedSlips.has(slip.name) ? '#eff6ff' : '#fff'), opacity: slip.docstatus === 2 ? 0.6 : 1 }">
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center;">
								<input type="checkbox" :checked="selectedSlips.has(slip.name)"
									@change="toggleSlipSelection(slip.name)" />
							</td>
							<td style="padding:6px; border:1px solid #e2e8f0;">{{ slip.employee }}</td>
							<td style="padding:6px; border:1px solid #e2e8f0;">{{ slip.employee_name }}</td>
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:right; color:#475569; font-weight:500;">{{ fmtMoney(slip.fixed_gross) }}</td>
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center; color:#475569;">{{ slip.payment_days }}</td>
							<template v-for="col in salaryRegister.earnings_columns" :key="'e-'+col">
								<!-- Req 3: Arrear-Pay is editable when slip is Draft -->
								<td v-if="col === 'Arrear-Pay' && slip.docstatus === 0"
									style="padding:4px; border:1px solid #e2e8f0; text-align:right; background:#eff6ff;">
									<input type="number" step="0.01" min="0"
										:value="(slip.earnings || []).find(e => e.component === col)?.amount || 0"
										@change="updateArrear(slip.name, 'Arrear-Pay', $event.target.value)"
										style="width:80px; text-align:right; border:1px solid #93c5fd; border-radius:3px; padding:2px 4px; font-size:11px;" />
								</td>
								<td v-else style="padding:6px; border:1px solid #e2e8f0; text-align:right;">
									{{ fmtMoney((slip.earnings || []).find(e => e.component === col)?.amount) }}
								</td>
							</template>
							<template v-for="col in salaryRegister.deductions_columns" :key="'d-'+col">
								<!-- Req 3: Arrear-Deduct is editable when slip is Draft -->
								<td v-if="col === 'Arrear-Deduct' && slip.docstatus === 0"
									style="padding:4px; border:1px solid #e2e8f0; text-align:right; background:#eff6ff;">
									<input type="number" step="0.01" min="0"
										:value="(slip.deductions || []).find(d => d.component === col)?.amount || 0"
										@change="updateArrear(slip.name, 'Arrear-Deduct', $event.target.value)"
										style="width:80px; text-align:right; border:1px solid #93c5fd; border-radius:3px; padding:2px 4px; font-size:11px;" />
								</td>
								<td v-else style="padding:6px; border:1px solid #e2e8f0; text-align:right;">
									{{ fmtMoney((slip.deductions || []).find(d => d.component === col)?.amount) }}
								</td>
							</template>
							<!-- Req 4: Gross Pay renamed to Gross CTC -->
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:right; font-weight:600;">{{ fmtMoney(slip.gross_pay) }}</td>
							<!-- Req 4: Total Deduction column (custom: PF-Employer + PF-Employee + PT + Arrear-Deduct) -->
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:right; font-weight:600;">{{ fmtMoney(slip.custom_total_deduction) }}</td>
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:right; font-weight:700; color:#166534; background:#eef2ff;">{{ fmtMoney(slip.net_pay) }}</td>
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center;">
								<span style="font-size:10px; padding:2px 6px; border-radius:4px;"
									:style="{
										background: slip.docstatus === 1 ? '#dcfce7' : (slip.docstatus === 2 ? '#fee2e2' : '#fef9c3'),
										color: slip.docstatus === 1 ? '#166534' : (slip.docstatus === 2 ? '#991b1b' : '#854d0e')
									}">
									{{ slip.status }}
								</span>
							</td>
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center;">
								<span style="font-size:10px; padding:2px 6px; border-radius:4px;"
									:style="{
										background: slip.custom_payment_status === 'Paid' ? '#dcfce7' : '#fee2e2',
										color: slip.custom_payment_status === 'Paid' ? '#166534' : '#991b1b'
									}">
									{{ slip.custom_payment_status || 'Unpaid' }}
								</span>
								<div v-if="payoutStatus[slip.employee]" style="font-size:10px; color:#64748b; margin-top:2px;">
									{{ payoutStatus[slip.employee].status }}
								</div>
							</td>
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center;">
								<a href="javascript:void(0)" @click="openSlipInNewTab(slip.name)" style="color:#2563eb; text-decoration:underline;">
									Open
								</a>
							</td>
							<!-- Submit button (only for draft slips, gated by payroll approval) -->
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center;">
								<button v-if="slip.docstatus === 0"
									class="btn btn-xs btn-success" style="font-size:10px; padding:2px 8px;"
									@click="submitSingleSlip(slip.name, slip.employee_name)"
									:disabled="actionLoading || (!payrollBookingApproved && !canApprovePayrollBooking)"
									:title="(!payrollBookingApproved && !canApprovePayrollBooking) ? 'Payroll must be approved by CEO first' : 'Submit this draft slip'">
									Submit
								</button>
								<span v-else-if="slip.docstatus === 1" style="font-size:10px; color:#166534;">Submitted</span>
								<span v-else style="font-size:10px; color:#991b1b;">Cancelled</span>
							</td>
							<!-- Cancel button (for draft and submitted slips) -->
							<td style="padding:6px; border:1px solid #e2e8f0; text-align:center;">
								<button v-if="slip.docstatus !== 2"
									class="btn btn-xs btn-danger" style="font-size:10px; padding:2px 8px;"
									@click="cancelSlip(slip.name, slip.employee_name)"
									:disabled="actionLoading"
									title="Cancel this slip to allow regeneration">
									Cancel
								</button>
								<span v-else style="font-size:10px; color:#991b1b;">Cancelled</span>
							</td>
						</tr>
					</tbody>
					<tfoot v-if="salaryRegisterTotals" style="position:sticky; bottom:0; z-index:10;">
						<tr style="background:#1e293b; color:#fff; font-weight:700;">
							<td style="padding:6px; border:1px solid #334155;" colspan="5">TOTAL ({{ salaryRegisterTotals.count }} employees)</td>
							<td v-for="col in salaryRegister.earnings_columns" :key="'te-'+col" style="padding:6px; border:1px solid #334155; text-align:right;">
								{{ fmtMoney(salaryRegisterTotals.earnings[col] || 0) }}
							</td>
							<td v-for="col in salaryRegister.deductions_columns" :key="'td-'+col" style="padding:6px; border:1px solid #334155; text-align:right;">
								{{ fmtMoney(salaryRegisterTotals.deductions[col] || 0) }}
							</td>
							<td style="padding:6px; border:1px solid #334155; text-align:right;">{{ fmtMoney(salaryRegisterTotals.gross_pay) }}</td>
							<td style="padding:6px; border:1px solid #334155; text-align:right;">{{ fmtMoney(salaryRegisterTotals.custom_total_deduction) }}</td>
							<td style="padding:6px; border:1px solid #334155; text-align:right; background:#3730a3;">{{ fmtMoney(salaryRegisterTotals.net_pay) }}</td>
							<td style="padding:6px; border:1px solid #334155;" colspan="5"></td>
						</tr>
					</tfoot>
				</table>
			</div>
		</div>
	</div>

	<!-- Section C & D: Booking & Release (only after attendance approved) -->
	<div v-if="employees.length && !loading && attendanceApproved" style="display:flex; gap:15px; flex-wrap:wrap;">
		<div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:15px; flex:1; min-width:300px;">
			<h3 style="margin:0 0 10px; font-size:16px; font-weight:700; color:#1e293b;">Payroll Summary</h3>

			<!-- Approval status badge -->
			<div style="margin-bottom:10px;">
				<span v-if="payrollApproval.status === 'Approved'" style="background:#dcfce7; color:#166534; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600;">
					Payroll Booking Approved ✓
				</span>
				<span v-else-if="payrollApproval.status === 'Pending for Approval'" style="background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600;">
					Pending Approval
				</span>
				<span v-else-if="payrollApproval.status === 'Rejected'" style="background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600;">
					Rejected
				</span>
			</div>

			<!-- Approve / Reject: visible only to CEO role while pending -->
			<div v-if="payrollApproval.status === 'Pending for Approval' && canApprovePayrollBooking" style="display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:10px;">
				<button class="btn btn-success btn-sm"
					@click="approvePayrollBooking"
					:disabled="payrollApproval.sending">
					{{ payrollApproval.sending ? 'Processing...' : 'Approve' }}
				</button>
				<button class="btn btn-danger btn-sm"
					@click="rejectPayrollBooking"
					:disabled="payrollApproval.sending">
					Reject
				</button>
			</div>
			<div v-else-if="payrollApproval.status === 'Pending for Approval'" style="font-size:11px; color:#92400e; margin-bottom:10px;">
				<i class="fa fa-hourglass-half"></i> Waiting for CEO to approve.
			</div>

			<span v-if="!payrollBookingApproved && payrollEntry" style="font-size:11px; color:#dc2626;">
				<i class="fa fa-lock"></i> CEO approval required to submit slips
			</span>
			<div v-if="bookedJE" style="margin-top:10px; font-size:12px;">
				Accrual Journal Entry: <a :href="'/app/journal-entry/' + bookedJE" target="_blank" style="color:#2563eb;">{{ bookedJE }}</a>
				<strong :style="{ color: bookedJEStatus === 1 ? '#166534' : '#92400e' }">({{ jeStatusLabel(bookedJEStatus) }})</strong>
			</div>

			<!-- Payable summary, shown once the accrual JE has been created -->
			<div v-if="bookedJE && salaryComponentSummary" style="margin-top:14px;">
				<h4 style="margin:0 0 8px; font-size:13px; font-weight:700; color:#1e293b;">Payroll Summary ({{ salaryComponentSummary.count }} employees)</h4>
				<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:12px 16px;">
					<p style="font-size:13px; color:#1e293b; line-height:1.9; margin:0;">
						Based on <strong>{{ salaryComponentSummary.count }}</strong> employees,
						the <strong>Total Salary Payable</strong> is <strong style="color:#166534;">{{ fmtMoney(salaryComponentSummary.net_pay) }}</strong>.
						This comprises a <strong>PF Payable</strong> of <strong style="color:#1e40af;">{{ fmtMoney((salaryComponentSummary.deductions['PF - Employee'] || 0) + (salaryComponentSummary.deductions['PF - Employer'] || 0)) }}</strong>
						(including PF - Employee and PF - Employer),
						an <strong>ESI Payable</strong> of <strong style="color:#1e40af;">{{ fmtMoney(salaryComponentSummary.deductions['Employee State Insurance'] || 0) }}</strong>,
						and a <strong>PT Payable</strong> of <strong style="color:#1e40af;">{{ fmtMoney(salaryComponentSummary.deductions['Professional Tax'] || 0) }}</strong>.
					</p>
				</div>
			</div>

			<!-- Man-hours & Time Cost metrics -->
			<div v-if="payrollMetrics" style="margin-top:14px;">
				<h4 style="margin:0 0 8px; font-size:13px; font-weight:700; color:#1e293b;">Man-Hours &amp; Time Cost</h4>
				<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:12px 16px;">
					<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px 20px; font-size:12px;">
						<div>
							<span style="color:#64748b;">Total Payment Days:</span>
							<strong style="color:#1e293b;">{{ payrollMetrics.totalPaymentDays.toFixed(0) }} days</strong>
						</div>
						<div>
							<span style="color:#64748b;">Total Man-Hours:</span>
							<strong style="color:#1e293b;">{{ payrollMetrics.totalManHours.toFixed(0) }} hrs</strong>
							<span style="color:#94a3b8; font-size:10px;">(9 hrs/day, 0930–1830)</span>
						</div>
						<div>
							<span style="color:#64748b;">Cost per Day:</span>
							<strong style="color:#1e40af;">&#8377; {{ fmtMoney(payrollMetrics.costPerDay) }}</strong>
						</div>
						<div>
							<span style="color:#64748b;">Cost per Hour:</span>
							<strong style="color:#1e40af;">&#8377; {{ fmtMoney(payrollMetrics.costPerHour) }}</strong>
						</div>
						<div>
							<span style="color:#64748b;">Cost per Minute:</span>
							<strong style="color:#1e40af;">&#8377; {{ payrollMetrics.costPerMinute.toFixed(2) }}</strong>
						</div>
						<div>
							<span style="color:#64748b;">Total Gross CTC:</span>
							<strong style="color:#166534;">&#8377; {{ fmtMoney(payrollMetrics.totalGross) }}</strong>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:15px; flex:1; min-width:350px;">
			<h3 style="margin:0 0 10px; font-size:16px; font-weight:700; color:#1e293b;">Payment Release</h3>

			<!-- Sub-menu tabs -->
			<div style="display:flex; gap:4px; margin-bottom:12px; border-bottom:2px solid #e2e8f0;">
				<button class="btn btn-sm" :class="paymentTab === 'employee' ? 'btn-primary' : 'btn-default'"
					@click="paymentTab = 'employee'" style="border-radius:4px 4px 0 0; border-bottom:none;">
					Employee Payment
				</button>
				<button class="btn btn-sm" :class="paymentTab === 'epf' ? 'btn-primary' : 'btn-default'"
					@click="paymentTab = 'epf'" style="border-radius:4px 4px 0 0; border-bottom:none;">
					EPF Payment
				</button>
				<button class="btn btn-sm" :class="paymentTab === 'esi' ? 'btn-primary' : 'btn-default'"
					@click="paymentTab = 'esi'" style="border-radius:4px 4px 0 0; border-bottom:none;">
					ESI Payment
				</button>
			</div>

			<!-- Employee Payment tab -->
			<div v-if="paymentTab === 'employee'">
				<p style="font-size:12px; color:#64748b; margin-bottom:12px;">
					Release net salary payment to employees via Manual Bank Entry or Automated bank payout (india_banking). JE is kept in Draft.
				</p>
				<div style="display:flex; gap:8px;">
					<button class="btn"
						:class="paymentJE ? 'btn-success' : 'btn-primary'"
						@click="openReleaseModal" :disabled="!salaryRegister.slips.length">
						{{ paymentJE ? 'Payment Released ✓' : 'Release Payment' }}
					</button>
					<button class="btn btn-secondary btn-sm" @click="refreshPayoutStatus">
						Refresh Status
					</button>
				</div>
				<div v-if="paymentJE" style="margin-top:10px; font-size:12px;">
					Bank Entry: <a :href="'/app/journal-entry/' + paymentJE" target="_blank" style="color:#2563eb;">{{ paymentJE }}</a>
					<strong :style="{ color: paymentJEStatus === 1 ? '#166534' : '#92400e' }">({{ jeStatusLabel(paymentJEStatus) }})</strong>
				</div>
			</div>

			<!-- EPF Payment tab -->
			<div v-if="paymentTab === 'epf'">
				<p style="font-size:12px; color:#64748b; margin-bottom:12px;">
					Release EPF (Provident Fund) payment — includes employee + employer PF contributions. JE: Debit EPF Payable, Credit Bank. Kept in Draft.
				</p>
				<div v-if="statutorySummary.epf" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; margin-bottom:12px; font-size:12px;">
					<div style="font-weight:600; margin-bottom:6px;">EPF Summary (submitted slips):</div>
					<div v-for="c in statutorySummary.epf.by_component" :key="c.component" style="display:flex; justify-content:space-between;">
						<span style="color:#64748b;">{{ c.component }} ({{ c.slip_count }} slips)</span>
						<span style="font-weight:600;">{{ fmtMoney(c.amount) }}</span>
					</div>
					<div style="display:flex; justify-content:space-between; margin-top:6px; padding-top:6px; border-top:1px solid #e2e8f0;">
						<span style="font-weight:700;">Total EPF</span>
						<span style="font-weight:700; color:#dc2626;">{{ fmtMoney(statutorySummary.epf.total) }}</span>
					</div>
				</div>
				<div style="display:flex; gap:8px;">
					<button class="btn btn-primary"
						@click="openStatutoryModal('EPF')"
						:disabled="!statutorySummary.epf || statutorySummary.epf.total <= 0">
						{{ statutoryJE.epf ? 'EPF JE Created ✓' : 'Release EPF Payment' }}
					</button>
				</div>
				<div v-if="statutoryJE.epf" style="margin-top:10px; font-size:12px;">
					EPF Bank Entry: <a :href="'/app/journal-entry/' + statutoryJE.epf" target="_blank" style="color:#2563eb;">{{ statutoryJE.epf }}</a>
				</div>
			</div>

			<!-- ESI Payment tab -->
			<div v-if="paymentTab === 'esi'">
				<p style="font-size:12px; color:#64748b; margin-bottom:12px;">
					Release ESI (Employee State Insurance) payment. JE: Debit ESI Payable, Credit Bank. Kept in Draft.
				</p>
				<div v-if="statutorySummary.esi" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; margin-bottom:12px; font-size:12px;">
					<div style="font-weight:600; margin-bottom:6px;">ESI Summary (submitted slips):</div>
					<div v-for="c in statutorySummary.esi.by_component" :key="c.component" style="display:flex; justify-content:space-between;">
						<span style="color:#64748b;">{{ c.component }} ({{ c.slip_count }} slips)</span>
						<span style="font-weight:600;">{{ fmtMoney(c.amount) }}</span>
					</div>
					<div style="display:flex; justify-content:space-between; margin-top:6px; padding-top:6px; border-top:1px solid #e2e8f0;">
						<span style="font-weight:700;">Total ESI</span>
						<span style="font-weight:700; color:#dc2626;">{{ fmtMoney(statutorySummary.esi.total) }}</span>
					</div>
				</div>
				<div style="display:flex; gap:8px;">
					<button class="btn btn-primary"
						@click="openStatutoryModal('ESI')"
						:disabled="!statutorySummary.esi || statutorySummary.esi.total <= 0">
						{{ statutoryJE.esi ? 'ESI JE Created ✓' : 'Release ESI Payment' }}
					</button>
				</div>
				<div v-if="statutoryJE.esi" style="margin-top:10px; font-size:12px;">
					ESI Bank Entry: <a :href="'/app/journal-entry/' + statutoryJE.esi" target="_blank" style="color:#2563eb;">{{ statutoryJE.esi }}</a>
				</div>
			</div>
		</div>
	</div>

	<!-- Section E: Statutory Report (only after attendance approved) -->
	<div v-if="employees.length && !loading && attendanceApproved" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:15px; margin-bottom:15px;">
		<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
			<h3 style="margin:0; font-size:16px; font-weight:700; color:#1e293b;">Statutory Report</h3>
			<button class="btn btn-primary btn-sm" @click="saveStatutoryReport"
				:disabled="statutoryReportSaving || !payrollEntry">
				{{ statutoryReportSaving ? 'Saving...' : 'Save Statutory Report' }}
			</button>
		</div>
		<p v-if="!payrollEntry" style="font-size:12px; color:#94a3b8; padding:10px 0;">
			Generate payroll first to manage the statutory report.
		</p>
		<div v-else style="overflow:auto; border:1px solid #e2e8f0; border-radius:6px;">
			<table style="border-collapse:collapse; width:100%; font-size:12px;">
				<thead style="position:sticky; top:0; z-index:10;">
					<tr style="background:#1e293b; color:#fff;">
						<th style="padding:6px 10px; border:1px solid #334155; min-width:120px; text-align:left;">Title</th>
						<th style="padding:6px 10px; border:1px solid #334155; min-width:140px; text-align:center;">Download Return</th>
						<th style="padding:6px 10px; border:1px solid #334155; min-width:140px; text-align:center;">Upload Challan</th>
						<th style="padding:6px 10px; border:1px solid #334155; min-width:140px; text-align:center;">Upload Payment</th>
						<th style="padding:6px 10px; border:1px solid #334155; min-width:120px; text-align:center;">Status</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(row, idx) in statutoryReport" :key="idx" style="background:#fff;">
						<td style="padding:6px 10px; border:1px solid #e2e8f0; font-weight:500;">
							<select v-model="row.title" class="form-control" style="width:100%; font-size:12px;">
								<option value="Bank - BTS">Bank - BTS</option>
								<option value="EPF">EPF</option>
								<option value="ESI">ESI</option>
							</select>
						</td>
						<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:center;">
							<!-- EPF / ESI: Generate & Download button -->
							<template v-if="row.title === 'EPF' || row.title === 'ESI'">
								<div style="display:flex; align-items:center; gap:6px; justify-content:center;">
									<span v-if="row.download_return" style="font-size:11px; color:#2563eb; max-width:100px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
										<a :href="row.download_return" target="_blank">{{ row.download_return.split('/').pop() }}</a>
									</span>
									<button class="btn btn-primary btn-xs" @click="generateReturnFile(row, row.title === 'EPF' ? 'epf' : 'esi')">
										<i class="fa fa-download"></i> Download
									</button>
								</div>
							</template>
							<!-- Bank - BTS: File upload (renamed to Download) -->
							<template v-else>
								<input type="file" @change="(e) => { if (e.target.files[0]) { uploadStatutoryFile(e.target.files[0], row, 'download_return'); } }" style="display:none;" :ref="'file_dl_' + idx">
								<div style="display:flex; align-items:center; gap:6px; justify-content:center;">
									<span v-if="row.download_return" style="font-size:11px; color:#2563eb; max-width:100px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
										<a :href="row.download_return" target="_blank">{{ row.download_return.split('/').pop() }}</a>
									</span>
									<button class="btn btn-default btn-xs" @click="triggerFileInput('file_dl_' + idx)">
										{{ row.download_return ? 'Change' : 'Download' }}
									</button>
								</div>
							</template>
						</td>
						<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:center;">
							<input type="file" @change="(e) => { if (e.target.files[0]) { uploadStatutoryFile(e.target.files[0], row, 'upload_challan'); } }" style="display:none;" :ref="'file_uc_' + idx">
							<div style="display:flex; align-items:center; gap:6px; justify-content:center;">
								<span v-if="row.upload_challan" style="font-size:11px; color:#2563eb; max-width:100px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
									<a :href="row.upload_challan" target="_blank">{{ row.upload_challan.split('/').pop() }}</a>
								</span>
								<button class="btn btn-default btn-xs" @click="triggerFileInput('file_uc_' + idx)">
									{{ row.upload_challan ? 'Change' : 'Upload' }}
								</button>
							</div>
						</td>
						<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:center;">
							<input type="file" @change="(e) => { if (e.target.files[0]) { uploadStatutoryFile(e.target.files[0], row, 'upload_payment'); } }" style="display:none;" :ref="'file_up_' + idx">
							<div style="display:flex; align-items:center; gap:6px; justify-content:center;">
								<span v-if="row.upload_payment" style="font-size:11px; color:#2563eb; max-width:100px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
									<a :href="row.upload_payment" target="_blank">{{ row.upload_payment.split('/').pop() }}</a>
								</span>
								<button class="btn btn-default btn-xs" @click="triggerFileInput('file_up_' + idx)">
									{{ row.upload_payment ? 'Change' : 'Upload' }}
								</button>
							</div>
						</td>
						<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:center;">
							<select v-model="row.status" class="form-control" style="width:100%; font-size:12px;"
								:style="{ color: row.status === 'Completed' ? '#166534' : row.status === 'In Process' ? '#92400e' : '#991b1b', fontWeight: 600 }">
								<option value="Pending">Pending</option>
								<option value="In Process">In Process</option>
								<option value="Completed">Completed</option>
							</select>
						</td>
					</tr>
					<tr v-if="statutoryReport.length === 0">
						<td colspan="5" style="padding:20px; text-align:center; color:#94a3b8;">
							No statutory report rows. Generate payroll to initialize.
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>

	<!-- Attendance Detail Modal -->
	<div v-if="attendanceModal.show" style="position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:1000; display:flex; align-items:center; justify-content:center;" @click.self="closeAttendanceModal">
		<div style="background:#fff; border-radius:8px; padding:20px; width:500px; max-width:90vw; max-height:80vh; overflow:auto;">
			<div v-if="attendanceModal.data">
				<h3 style="margin:0 0 15px; font-size:16px; font-weight:700;">
					Attendance Detail
				</h3>
				<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:13px;">
					<div><strong>Employee:</strong> {{ attendanceModal.data.employee_name }}</div>
					<div><strong>Date:</strong> {{ attendanceModal.data.attendance_date }}</div>
					<div><strong>Status:</strong>
						<span style="padding:2px 8px; border-radius:4px; color:#fff;"
							:style="{ background: statusColor(attendanceModal.data.status) }">
							{{ attendanceModal.data.status }}
						</span>
					</div>
					<div><strong>Shift:</strong> {{ attendanceModal.data.shift || '-' }}</div>
					<div><strong>In Time:</strong> {{ attendanceModal.data.in_time || '-' }}</div>
					<div><strong>Out Time:</strong> {{ attendanceModal.data.out_time || '-' }}</div>
					<div><strong>Half Day:</strong> {{ attendanceModal.data.half_day ? 'Yes' : 'No' }}</div>
					<div><strong>Half Day Status:</strong> {{ attendanceModal.data.half_day_status || '-' }}</div>
					<div><strong>Late Entry:</strong> {{ attendanceModal.data.late_entry ? 'Yes' : 'No' }}</div>
					<div><strong>Early Exit:</strong> {{ attendanceModal.data.early_exit ? 'Yes' : 'No' }}</div>
					<div v-if="attendanceModal.data.leave_type"><strong>Leave Type:</strong> {{ attendanceModal.data.leave_type }}</div>
					<div><strong>DocStatus:</strong> {{ attendanceModal.data.docstatus === 1 ? 'Submitted' : 'Draft' }}</div>
				</div>
				<div style="margin-top:15px; display:flex; gap:8px;">
					<button class="btn btn-primary" @click="openAttendanceInNewTab(attendanceModal.data.name)">
						Update to Present (Open in new tab)
					</button>
					<button class="btn btn-default" @click="closeAttendanceModal">Close</button>
				</div>
			</div>
		</div>
	</div>

	<!-- Release Payment Modal -->
	<div v-if="releaseModal.show" style="position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:1000; display:flex; align-items:center; justify-content:center;" @click.self="closeReleaseModal">
		<div style="background:#fff; border-radius:8px; padding:20px; width:800px; max-width:95vw; max-height:90vh; overflow:auto;">
			<h3 style="margin:0 0 15px; font-size:16px; font-weight:700;">Release Payment — Select Employees</h3>

			<!-- Employee selection table -->
			<div style="margin-bottom:12px; border:1px solid #e2e8f0; border-radius:6px; max-height:300px; overflow:auto;">
				<table style="border-collapse:collapse; width:100%; font-size:12px;">
					<thead style="position:sticky; top:0; z-index:10;">
						<tr style="background:#1e293b; color:#fff;">
							<th style="padding:6px 10px; border:1px solid #334155; width:40px; text-align:center;">
								<input type="checkbox" :checked="releaseModal.selectedAll" @change="toggleReleaseSelectAll">
							</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:100px; text-align:left;">Emp ID</th>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:160px; text-align:left;">Employee Name</th>
							<template v-if="releaseModal.mode === 'BTS'">
								<th style="padding:6px 10px; border:1px solid #334155; min-width:120px; text-align:left;">Bank A/C No</th>
								<th style="padding:6px 10px; border:1px solid #334155; min-width:100px; text-align:left;">IFSC</th>
							</template>
							<th style="padding:6px 10px; border:1px solid #334155; min-width:120px; text-align:right;">Net Payable</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="emp in releaseModal.employees" :key="emp.employee"
							:style="{ background: emp.selected ? '#fff' : '#f1f5f9' }">
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:center;">
								<input type="checkbox" :checked="emp.selected" @change="toggleReleaseEmployee(emp.employee)">
							</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0;">{{ emp.employee }}</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0;">{{ emp.employee_name }}</td>
							<template v-if="releaseModal.mode === 'BTS'">
								<td style="padding:6px 10px; border:1px solid #e2e8f0; font-size:11px;">
									{{ emp.bank_ac_no || '(not set)' }}
								</td>
								<td style="padding:6px 10px; border:1px solid #e2e8f0; font-size:11px;">
									{{ emp.ifsc_code || '(not set)' }}
								</td>
							</template>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; font-weight:600; color:#166534;">
								{{ fmtMoney(emp.rounded_total || emp.net_pay) }}
							</td>
						</tr>
					</tbody>
					<tfoot>
						<tr style="background:#f0fdf4; font-weight:700;">
							<td :colspan="releaseModal.mode === 'BTS' ? 2 : 2" style="padding:6px 10px; border:1px solid #e2e8f0;">
								{{ releaseSelectedCount }} selected
							</td>
							<td :colspan="releaseModal.mode === 'BTS' ? 3 : 1" style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right;">Total:</td>
							<td style="padding:6px 10px; border:1px solid #e2e8f0; text-align:right; color:#166534; font-size:14px;">
								{{ fmtMoney(releaseSelectedTotal) }}
							</td>
						</tr>
					</tfoot>
				</table>
			</div>

			<!-- Payment mode -->
			<div style="margin-bottom:12px;">
				<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Payment Mode</label>
				<div style="display:flex; gap:12px;">
					<label style="display:flex; align-items:center; gap:4px; font-size:13px;">
						<input type="radio" v-model="releaseModal.mode" value="Manual"> Manual (Bank Entry only)
					</label>
					<label style="display:flex; align-items:center; gap:4px; font-size:13px;">
						<input type="radio" v-model="releaseModal.mode" value="Automated"> Automated (Bank API)
					</label>
					<label style="display:flex; align-items:center; gap:4px; font-size:13px;">
						<input type="radio" v-model="releaseModal.mode" value="BTS"> BTS (Bank Transfer Sheet)
					</label>
				</div>
			</div>

			<div style="margin-bottom:12px;">
				<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Company Bank Account</label>
				<select v-model="releaseModal.bank_account" class="form-control" style="width:100%;">
					<option value="">-- Select Bank Account --</option>
					<option v-for="b in bankAccounts" :key="b.name" :value="b.name">
						{{ b.bank }} - {{ b.bank_account_no }}{{ b.is_default ? ' (Default)' : '' }}
					</option>
				</select>
			</div>

			<!-- Reference fields for Manual/Automated mode -->
			<div v-if="releaseModal.mode !== 'BTS'" style="display:flex; gap:8px; margin-bottom:12px;">
				<div style="flex:1;">
					<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Reference No <span style="color:#ef4444;">*</span></label>
					<input type="text" v-model="releaseModal.reference_no" class="form-control" style="width:100%;" placeholder="Enter reference / cheque no">
				</div>
				<div style="flex:1;">
					<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Reference Date <span style="color:#ef4444;">*</span></label>
					<input type="date" v-model="releaseModal.reference_date" class="form-control" style="width:100%;">
				</div>
			</div>

			<!-- Payment date for BTS mode -->
			<div v-if="releaseModal.mode === 'BTS'" style="margin-bottom:12px;">
				<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Payment Date <span style="color:#ef4444;">*</span></label>
				<input type="date" v-model="releaseModal.payment_date" class="form-control" style="width:100%;">
			</div>

			<div v-if="releaseModal.mode === 'Automated'" style="background:#fef3c7; border:1px solid #fde68a; border-radius:6px; padding:8px; margin-bottom:12px; font-size:11px; color:#92400e;">
				Automated mode will create a Payment Order and initiate a real bank payout via the india_banking app.
				Each employee must have a Bank Account linked.
			</div>

			<div v-if="releaseModal.mode === 'BTS'" style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:6px; padding:8px; margin-bottom:12px; font-size:11px; color:#1e40af;">
				BTS generates a Bank Transfer Sheet (Excel) in the bank's bulk-payment format (IMPS).
				Employees with missing bank account number or IFSC code will be skipped.
				The file will be attached to the Statutory Report under "Bank - BTS".
			</div>

			<div style="display:flex; gap:8px; justify-content:flex-end;">
				<button class="btn btn-default" @click="closeReleaseModal" :disabled="releaseModal.processing">Cancel</button>
				<button class="btn btn-primary" @click="confirmReleasePayment" :disabled="releaseModal.processing || releaseSelectedCount === 0">
					{{ releaseModal.processing ? 'Processing...' : (releaseModal.mode === 'BTS' ? 'Generate BTS for ' + releaseSelectedCount + ' Employee(s)' : 'Release Payment to ' + releaseSelectedCount + ' Employee(s)') }}
				</button>
			</div>
		</div>
	</div>

	<!-- Statutory Payment Modal (EPF / ESI) -->
	<div v-if="statutoryModal.show" style="position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:1000; display:flex; align-items:center; justify-content:center;" @click.self="closeStatutoryModal">
		<div style="background:#fff; border-radius:8px; padding:20px; width:450px; max-width:90vw;">
			<h3 style="margin:0 0 15px; font-size:16px; font-weight:700;">{{ statutoryModal.payment_type }} Payment Release</h3>

			<div v-if="statutorySummary[statutoryModal.payment_type.toLowerCase()]" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px; margin-bottom:12px; font-size:12px;">
				<div v-for="c in statutorySummary[statutoryModal.payment_type.toLowerCase()].by_component" :key="c.component" style="display:flex; justify-content:space-between; margin-bottom:4px;">
					<span style="color:#64748b;">{{ c.component }}</span>
					<span style="font-weight:600;">{{ fmtMoney(c.amount) }}</span>
				</div>
				<div style="display:flex; justify-content:space-between; margin-top:6px; padding-top:6px; border-top:1px solid #e2e8f0;">
					<span style="font-weight:700;">Total</span>
					<span style="font-weight:700; color:#dc2626; font-size:14px;">{{ fmtMoney(statutorySummary[statutoryModal.payment_type.toLowerCase()].total) }}</span>
				</div>
			</div>

			<div style="margin-bottom:12px;">
				<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Company Bank Account</label>
				<select v-model="statutoryModal.bank_account" class="form-control" style="width:100%;">
					<option value="">-- Select Bank Account --</option>
					<option v-for="b in bankAccounts" :key="b.name" :value="b.name">
						{{ b.bank }} - {{ b.bank_account_no }}{{ b.is_default ? ' (Default)' : '' }}
					</option>
				</select>
			</div>

			<div style="margin-bottom:12px;">
				<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Reference No <span style="color:#ef4444;">*</span></label>
				<input type="text" v-model="statutoryModal.reference_no" class="form-control" style="width:100%;" placeholder="Enter reference / cheque no">
			</div>

			<div style="margin-bottom:12px;">
				<label style="font-size:12px; color:#64748b; display:block; margin-bottom:4px;">Reference Date <span style="color:#ef4444;">*</span></label>
				<input type="date" v-model="statutoryModal.reference_date" class="form-control" style="width:100%;">
			</div>

			<div style="background:#fef3c7; border:1px solid #fde68a; border-radius:6px; padding:8px; margin-bottom:12px; font-size:11px; color:#92400e;">
				A Draft Journal Entry will be created (Debit {{ statutoryModal.payment_type }} Payable, Credit Bank). Review and submit it manually.
			</div>

			<div style="display:flex; gap:8px; justify-content:flex-end;">
				<button class="btn btn-default" @click="closeStatutoryModal" :disabled="statutoryModal.processing">Cancel</button>
				<button class="btn btn-primary" @click="confirmStatutoryRelease" :disabled="statutoryModal.processing">
					{{ statutoryModal.processing ? 'Processing...' : 'Confirm ' + statutoryModal.payment_type + ' Payment' }}
				</button>
			</div>
		</div>
	</div>

	<!-- ===== User Manual Modal ===== -->
	<div v-if="showManual" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:9998; display:flex; align-items:flex-start; justify-content:center; overflow-y:auto; padding:20px 10px;" @click.self="closeManual">
		<div style="background:#fff; border-radius:10px; max-width:900px; width:100%; margin:20px 0; box-shadow:0 8px 30px rgba(0,0,0,0.3);">
			<div style="display:flex; justify-content:space-between; align-items:center; padding:18px 24px; border-bottom:2px solid #e2e8f0; border-radius:10px 10px 0 0; background:#1e293b;">
				<h2 style="margin:0; font-size:20px; font-weight:700; color:#fff;">Payroll Workbench — User Manual</h2>
				<button class="btn btn-sm" @click="closeManual" style="background:transparent; border:none; color:#fff; font-size:22px; cursor:pointer; padding:0 8px;">&times;</button>
			</div>
			<div style="padding:24px 30px; max-height:75vh; overflow-y:auto; font-size:14px; line-height:1.7; color:#334155;">

				<h3 style="color:#1e40af; border-bottom:2px solid #dbeafe; padding-bottom:6px; margin-top:0;">Overview</h3>
				<p>The <strong>Payroll Workbench</strong> is a single-page tool to manage the entire monthly payroll cycle — from attendance to salary disbursement to statutory compliance. It replaces the need to navigate multiple Frappe/ERPNext screens.</p>
				<p style="background:#eff6ff; border-left:4px solid #3b82f6; padding:10px 14px; border-radius:4px;">
					<strong>URL:</strong> <a href="/app/payroll-workbench" style="color:#1d4ed8;">/app/payroll-workbench</a><br>
					<strong>Roles:</strong> HR Manager, Finance User, CEO (Approver)
				</p>

				<h3 style="color:#1e40af; border-bottom:2px solid #dbeafe; padding-bottom:6px; margin-top:28px;">Payroll Cycle — Step by Step</h3>
				<p>The monthly payroll cycle consists of <strong>6 steps</strong>. Complete them in order:</p>

				<div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:16px; margin:12px 0;">
					<h4 style="margin:0 0 8px; color:#166534; font-size:15px;">Step 1: Select Filters &amp; Load Employees</h4>
					<ol style="margin:0; padding-left:20px;">
						<li>Select <strong>Company</strong> from the dropdown (e.g., TEAMPRO HR &amp; IT Services Pvt. Ltd.)</li>
						<li>Optionally filter by <strong>Branch</strong>, <strong>Department</strong>, <strong>Designation</strong>, or <strong>Grade</strong></li>
						<li>Select the <strong>Month</strong> and <strong>Year</strong> for the payroll period</li>
						<li>Click <strong>Load Employees</strong> — this fetches the employee list and their attendance data</li>
					</ol>
				</div>

				<div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:16px; margin:12px 0;">
					<h4 style="margin:0 0 8px; color:#92400e; font-size:15px;">Step 2: Review &amp; Approve Attendance</h4>
					<ol style="margin:0; padding-left:20px;">
						<li>Switch between <strong>Matrix View</strong> (day-by-day grid) and <strong>Summary View</strong> (totals per employee) using the toggle button</li>
						<li>In Matrix View, click any cell to see attendance details for that day</li>
						<li>In Summary View, review each employee's Present, Absent, Leave, and Half-Day counts</li>
						<li>Check for <strong>Unapproved Leave</strong> or <strong>Attendance Requests</strong> — a warning banner will appear if any exist. Resolve them in the Leave/Attendance modules before proceeding</li>
						<li>Once all attendance is clean, click <strong>Send for Approval</strong></li>
						<li>The <strong>CEO / Approver</strong> will see <strong>Approve</strong> and <strong>Reject</strong> buttons. Click <strong>Approve</strong> to lock attendance</li>
						<li>Once approved, the <strong>"Attendance Approved"</strong> badge appears in the header</li>
					</ol>
					<p style="background:#fef2f2; border-left:3px solid #ef4444; padding:6px 10px; border-radius:4px; margin:8px 0 0; font-size:13px;">
						<strong>Note:</strong> Salary slips cannot be generated until attendance is approved.
					</p>
				</div>

				<div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:16px; margin:12px 0;">
					<h4 style="margin:0 0 8px; color:#1e40af; font-size:15px;">Step 3: Generate Salary Slips (Salary Register)</h4>
					<ol style="margin:0; padding-left:20px;">
						<li>Once attendance is approved, the <strong>Salary Register</strong> section appears automatically</li>
						<li>Click <strong>Generate Payroll</strong> to create draft salary slips for all employees</li>
						<li>The register shows: <strong>Fixed Gross</strong> (full monthly salary), <strong>Days</strong> (payment days), individual <strong>Earnings</strong> and <strong>Deductions</strong> columns, <strong>Gross CTC</strong> (prorated gross), <strong>Total Deduction</strong>, and <strong>Net Total</strong></li>
						<li>For draft slips, <strong>Arrear-Pay</strong> and <strong>Arrear-Deduct</strong> columns are editable — click the cell to update values</li>
						<li>Use the search box to filter employees by name</li>
						<li>Click <strong>Export Excel</strong> to download the salary register as a spreadsheet</li>
						<li>Click any slip name to open it in a new tab for detailed review</li>
					</ol>
					<p style="background:#f0f9ff; border-left:3px solid #0ea5e9; padding:6px 10px; border-radius:4px; margin:8px 0 0; font-size:13px;">
						<strong>Tip:</strong> If an employee's slip was cancelled, use <strong>Generate Pending</strong> to regenerate only the missing slips.
					</p>
				</div>

				<div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:16px; margin:12px 0;">
					<h4 style="margin:0 0 8px; color:#166534; font-size:15px;">Step 4: Send Payroll for Approval &amp; Book</h4>
					<ol style="margin:0; padding-left:20px;">
						<li>In the <strong>Payroll Summary</strong> section, review the total Gross, Deductions, and Net Pay</li>
						<li>Click <strong>Send for Approval</strong> to send the payroll booking request to the CEO</li>
						<li>The CEO sees <strong>Approve</strong> / <strong>Reject</strong> buttons. On approval, the system automatically:
							<ul>
								<li>Submits all draft salary slips</li>
								<li>Creates the accrual <strong>Journal Entry</strong> (debit to Salary expense, credit to Payroll Payable, EPF, ESI, PT)</li>
							</ul>
						</li>
						<li>The <strong>"Payroll Booked"</strong> badge appears in the header with the JE number</li>
					</ol>
					<p style="background:#fef2f2; border-left:3px solid #ef4444; padding:6px 10px; border-radius:4px; margin:8px 0 0; font-size:13px;">
						<strong>Note:</strong> Only the CEO role can approve payroll booking. HR/Finance users can only send for approval.
					</p>
				</div>

				<div style="background:#fdf4ff; border:1px solid #e9d5ff; border-radius:8px; padding:16px; margin:12px 0;">
					<h4 style="margin:0 0 8px; color:#7e22ce; font-size:15px;">Step 5: Release Salary Payment</h4>
					<ol style="margin:0; padding-left:20px;">
						<li>In the <strong>Payroll Summary</strong> section, click <strong>Release Payment</strong></li>
						<li>A modal opens showing all employees with their net pay amounts</li>
						<li>Select the employees to pay (or select all)</li>
						<li>Choose the <strong>Payment Mode</strong>:
							<ul>
								<li><strong>Bank Entry</strong> — Manual bank transfer (requires Bank Account, Reference No, and Reference Date)</li>
								<li><strong>Automated</strong> — Creates a Payment Order for bank processing</li>
							</ul>
						</li>
						<li>Click <strong>Confirm Release Payment</strong></li>
						<li>The system creates a <strong>Payment Journal Entry</strong> debiting Payroll Payable and crediting the Bank account</li>
						<li>The <strong>"Salary Released"</strong> badge appears in the header</li>
					</ol>
					<p style="background:#faf5ff; border-left:3px solid #8b5cf6; padding:6px 10px; border-radius:4px; margin:8px 0 0; font-size:13px;">
						<strong>BTS (Bank Transfer Sheet):</strong> In the <strong>Release Payment</strong> modal, select <strong>BTS</strong> mode to generate a bank transfer sheet for employees paid via separate bank transfers.
					</p>
				</div>

				<div style="background:#fff7ed; border:1px solid #fed7aa; border-radius:8px; padding:16px; margin:12px 0;">
					<h4 style="margin:0 0 8px; color:#c2410c; font-size:15px;">Step 6: Statutory Compliance — EPF, ESI &amp; Professional Tax</h4>
					<p>The <strong>Statutory Report</strong> section has three sub-tabs:</p>
					<div style="margin:8px 0;">
						<strong style="color:#9a3412;">A. Employee Payment Tab</strong>
						<ul>
							<li>Shows the salary payment JE and payout status per employee</li>
							<li>Use <strong>Release Payment</strong> → BTS mode to generate the Bank Transfer Sheet</li>
						</ul>
					</div>
					<div style="margin:8px 0;">
						<strong style="color:#9a3412;">B. EPF Tab</strong>
						<ul>
							<li>Shows the EPF payment JE (if created) and statutory summary</li>
							<li>Click <strong>Release EPF Payment</strong> to create the EPF payment JE</li>
							<li>In the Statutory Report table below, click <strong>Download</strong> next to EPF to generate and download the <strong>ECR (Electronic Challan cum Return)</strong> text file</li>
							<li>The ECR file contains one row per PF-eligible employee with UAN, EPF wages, and contribution breakdown</li>
							<li>Upload this file to the EPFO portal</li>
						</ul>
					</div>
					<div style="margin:8px 0;">
						<strong style="color:#9a3412;">C. ESI Tab</strong>
						<ul>
							<li>Shows the ESI payment JE (if created) and statutory summary</li>
							<li>Click <strong>Release ESI Payment</strong> to create the ESI payment JE</li>
							<li>Click <strong>Download</strong> next to ESI to generate the ESIC return text file</li>
						</ul>
					</div>
					<div style="margin:8px 0;">
						<strong style="color:#9a3412;">D. Statutory Report Table</strong>
						<ul>
							<li>For <strong>Professional Tax</strong> and <strong>Bank - BTS</strong>, upload the relevant file using the <strong>Download/Change</strong> button</li>
							<li>Click <strong>Save Report</strong> to save the statutory report data</li>
						</ul>
					</div>
				</div>

				<h3 style="color:#1e40af; border-bottom:2px solid #dbeafe; padding-bottom:6px; margin-top:28px;">Header Status Badges</h3>
				<p>The header shows real-time status badges for the current payroll cycle:</p>
				<table style="width:100%; border-collapse:collapse; margin:10px 0;">
					<thead>
						<tr style="background:#f1f5f9;">
							<th style="padding:8px 12px; border:1px solid #e2e8f0; text-align:left; font-size:13px;">Badge</th>
							<th style="padding:8px 12px; border:1px solid #e2e8f0; text-align:left; font-size:13px;">Meaning</th>
						</tr>
					</thead>
					<tbody>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px;">Attendance Draft</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Attendance loaded but not yet sent for approval</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:4px;">Attendance Pending Approval</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Sent to CEO, awaiting approval</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#dcfce7; color:#166534; padding:2px 8px; border-radius:4px;">Attendance Approved</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Attendance locked — payroll can proceed</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px;">Payroll Draft</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Salary slips generated but not yet sent for booking approval</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:4px;">Payroll Pending Approval</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Payroll booking sent to CEO, awaiting approval</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#dcfce7; color:#166534; padding:2px 8px; border-radius:4px;">Payroll Approved</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Payroll booking approved, JE created</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#dbeafe; color:#1e40af; padding:2px 8px; border-radius:4px;">Payroll Booked: ACC-JV-XXXX</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Accrual Journal Entry created (Salary expense booked)</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><span style="background:#dbeafe; color:#1e40af; padding:2px 8px; border-radius:4px;">Salary Released: ACC-JV-XXXX</span></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Payment Journal Entry created (Salary paid to employees)</td></tr>
					</tbody>
				</table>

				<h3 style="color:#1e40af; border-bottom:2px solid #dbeafe; padding-bottom:6px; margin-top:28px;">Salary Register Columns Explained</h3>
				<table style="width:100%; border-collapse:collapse; margin:10px 0;">
					<thead>
						<tr style="background:#f1f5f9;">
							<th style="padding:8px 12px; border:1px solid #e2e8f0; text-align:left; font-size:13px;">Column</th>
							<th style="padding:8px 12px; border:1px solid #e2e8f0; text-align:left; font-size:13px;">Description</th>
						</tr>
					</thead>
					<tbody>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Fixed Gross</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Full monthly salary (base + allowances) before proration</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Days</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Payment days / Total working days (e.g., 28/31)</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Earnings</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Individual earning components (Basic, HRA, Special Allowance, etc.) — prorated based on payment days</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Deductions</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Individual deduction components (Total EPF, PT, ESI, etc.)</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Gross CTC</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Prorated gross pay (= Fixed Gross &times; Days / Working Days)</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Total Deduction</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">PF-Employer + PF-Employee + Professional Tax + Arrear-Deduct</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Net Total</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Gross CTC - Total Deduction (amount paid to employee)</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;"><strong>Status</strong></td><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Draft, Submitted, or Cancelled</td></tr>
					</tbody>
				</table>

				<h3 style="color:#1e40af; border-bottom:2px solid #dbeafe; padding-bottom:6px; margin-top:28px;">Roles &amp; Permissions</h3>
				<table style="width:100%; border-collapse:collapse; margin:10px 0;">
					<thead>
						<tr style="background:#f1f5f9;">
							<th style="padding:8px 12px; border:1px solid #e2e8f0; text-align:left; font-size:13px;">Action</th>
							<th style="padding:8px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">HR / Finance</th>
							<th style="padding:8px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">CEO</th>
						</tr>
					</thead>
					<tbody>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Load Employees &amp; Attendance</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Send Attendance for Approval</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Approve / Reject Attendance</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">No</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px; font-weight:600; color:#166534;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Generate Payroll</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Edit Arrears (Draft slips)</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Send Payroll for Approval</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Approve / Reject Payroll Booking</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">No</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px; font-weight:600; color:#166534;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Release Salary Payment</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Generate EPF/ESI Return Files</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
						<tr><td style="padding:6px 12px; border:1px solid #e2e8f0; font-size:13px;">Release EPF/ESI Payment</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td><td style="padding:6px 12px; border:1px solid #e2e8f0; text-align:center; font-size:13px;">Yes</td></tr>
					</tbody>
				</table>

				<h3 style="color:#1e40af; border-bottom:2px solid #dbeafe; padding-bottom:6px; margin-top:28px;">Quick Reference — Complete Cycle</h3>
				<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:16px; font-size:13px;">
					<ol style="margin:0; padding-left:20px; line-height:2.2;">
						<li><strong>Select Company + Month</strong> &rarr; Click <strong>Load Employees</strong></li>
						<li>Review attendance &rarr; Click <strong>Send for Approval</strong></li>
						<li>CEO: Click <strong>Approve</strong> attendance</li>
						<li>Click <strong>Generate Payroll</strong> &rarr; Review salary slips</li>
						<li>Edit arrears if needed &rarr; Click <strong>Send for Approval</strong> (Payroll Booking)</li>
						<li>CEO: Click <strong>Approve</strong> payroll &rarr; JE auto-created</li>
						<li>Click <strong>Release Payment</strong> &rarr; Select employees &rarr; Confirm</li>
						<li>Go to <strong>Statutory Report</strong> &rarr; Download EPF ECR file &rarr; Upload to EPFO</li>
						<li>Release EPF/ESI payments if applicable</li>
						<li>Save Statutory Report</li>
					</ol>
				</div>

				<h3 style="color:#1e40af; border-bottom:2px solid #dbeafe; padding-bottom:6px; margin-top:28px;">Troubleshooting</h3>
				<div style="font-size:13px;">
					<p><strong>Q: Salary Register not showing?</strong><br>A: Attendance must be approved first. Check the "Attendance Approved" badge in the header.</p>
					<p><strong>Q: "Generate Payroll" button not visible?</strong><br>A: This appears only after attendance is approved. If slips already exist, the register loads automatically.</p>
					<p><strong>Q: EPF Download not working?</strong><br>A: Ensure payroll is booked (JE created) and there are PF-eligible employees with UAN numbers. Hard-refresh the page (Ctrl+Shift+R) and try again.</p>
					<p><strong>Q: Cannot submit salary slips?</strong><br>A: Payroll booking must be approved by the CEO first. Click "Send for Approval" in the Payroll Summary section.</p>
					<p><strong>Q: Values look wrong for an employee?</strong><br>A: Check the employee's Salary Structure Assignment (base salary) and custom_byod_allowance field. Contact the admin if corrections are needed.</p>
				</div>

				<hr style="margin:28px 0; border:none; border-top:1px solid #e2e8f0;">
				<p style="text-align:center; color:#94a3b8; font-size:12px;">
					Payroll Workbench User Manual &mdash; TEAMPRO HR &amp; IT Services Pvt. Ltd.<br>
					For support, contact the system administrator.
				</p>

			</div>
		</div>
	</div>

</div>
`
	});

	app.mount(mountEl);
}
