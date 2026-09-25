frappe.provide("teampro.project_monitoring");

frappe.ui.form.on("Project", {
	refresh(frm) {
		if (frm.is_new()) return;
		// Allow linking any non-cancelled Sales Order regardless of the
		// project's company/customer (stock ERPNext restricts the dropdown).
		frm.set_query("sales_order", () => ({
			filters: { docstatus: ["!=", 2] },
		}));
		teampro.project_monitoring.setup_tab(frm);
	},
});

teampro.project_monitoring = {
	TAB_FIELDNAME: "pm_monitoring_tab",
	SERVICE: "IT-SW",
	PAGE_SIZE: 25,

	// Statuses shown on the hours-based charts. Extra statuses found in data
	// are appended automatically.
	HOURS_STATUSES: ["Open", "Working", "Code Review", "Pending Review", "Client Review"],
	MEETING_STATUSES: ["Planned", "Invitation Sent", "In Progress", "Completed", "Cancelled"],
	// Statuses hidden from the status donuts (still available in filters/tables)
	CHART_EXCLUDE: ["Completed"],
	MEETING_CHART_EXCLUDE: ["Completed", "Cancelled"],

	// Default task table order — unlisted statuses sort after these, closed last.
	STATUS_SORT: {
		Open: 0, Working: 1, "Pending Review": 2, "Code Review": 3,
		"Client Review": 4, Hold: 5, Overdue: 6,
	},

	CLOSED_TASK: ["Completed", "Cancelled", "Template"],
	CLOSED_MEETING: ["Completed", "Cancelled"],
	CLOSED_PROJECT: ["Completed", "Cancelled"],

	STATUS_SHORT: { "Pending Review": "PR", "Code Review": "CR", "Client Review": "CR" },

	STATUS_HEX: {
		Open: "#94a3b8",
		Ready: "#14b8a6",
		Working: "#3b82f6",
		"Code Review": "#8b5cf6",
		"Pending Review": "#eab308",
		"Client Review": "#f97316",
		Overdue: "#ef4444",
		Hold: "#f59e0b",
		Completed: "#22c55e",
		Cancelled: "#9ca3af",
		Template: "#9ca3af",
		Planned: "#3b82f6",
		"Invitation Sent": "#14a8a0",
		"In Progress": "#eab308",
	},

	AGING_BUCKETS: [
		["0-3 Days", 0, 3],
		["4-7 Days", 4, 7],
		["8-15 Days", 8, 15],
		["16-30 Days", 16, 30],
		["30+ Days", 30, null],
	],
	AGING_HEX: ["#22c55e", "#3b82f6", "#eab308", "#f97316", "#ef4444"],

	PRIORITY_ORDER: { Urgent: 0, High: 1, Medium: 2, Low: 3 },

	hr(v) {
		return Math.round((Number(v) || 0) * 100) / 100;
	},

	load_css() {
		if (this._css_loaded) return;
		this._css_loaded = true;
		$('<link rel="stylesheet" type="text/css" href="/assets/teampro/css/project_monitoring.css?v=20260921-12">').appendTo(
			document.head
		);
	},

	setup_tab(frm) {
		this.load_css();
		const layout = frm.layout;
		if (!layout || !layout.is_tabbed_layout || !layout.is_tabbed_layout()) return;
		if (!layout.tab_link_container || !layout.tabs_content) return;

		if (frm._pm_tab && layout.tabs && layout.tabs.includes(frm._pm_tab)) {
			frm._pm_tab.toggle(frm.doc.service === this.SERVICE);
			return;
		}

		const me = this;
		const fieldname = this.TAB_FIELDNAME;
		const id = `${frappe.scrub(frm.doctype, "-")}-${fieldname}`;

		const tab_link = $(`
			<li class="nav-item">
				<button class="nav-link" id="${id}-tab" data-fieldname="${fieldname}"
					type="button" role="tab" aria-controls="${id}">
					${__("Project Monitoring")}
				</button>
			</li>
		`).appendTo(layout.tab_link_container);

		const wrapper = $(`<div class="tab-pane fade" id="${id}" role="tabpanel"
			aria-labelledby="${id}-tab">`).appendTo(layout.tabs_content);

		const tab = {
			df: { fieldname: fieldname, label: __("Project Monitoring") },
			tab_link: tab_link,
			wrapper: wrapper,
			hidden: false,
			set_active() {
				(layout.tabs || []).forEach((t) => {
					if (t !== tab) {
						t.tab_link.find(".nav-link").removeClass("active");
						t.wrapper.removeClass("show active");
					}
				});
				tab_link.find(".nav-link").addClass("active");
				wrapper.addClass("show active");
				frm.set_active_tab && frm.set_active_tab(tab);
				me.load(frm);
			},
			is_active() {
				return wrapper.hasClass("active");
			},
			is_hidden() {
				return wrapper.hasClass("hide") && tab_link.hasClass("hide");
			},
			refresh() {
				this.toggle(frm.doc.service === me.SERVICE);
			},
			toggle(show) {
				tab_link.toggleClass("hide", !show);
				wrapper.toggleClass("hide", !show);
				tab_link.toggleClass("show", show);
				wrapper.toggleClass("show", show);
				tab.hidden = !show;
			},
			show() { tab_link.show(); },
			hide() { tab_link.hide(); },
			add_field() {},
			replace_field() {},
		};

		tab_link.find(".nav-link").on("click", (e) => {
			e.preventDefault();
			tab.set_active();
		});

		layout.tabs.push(tab);
		frm._pm_tab = tab;
		tab.toggle(frm.doc.service === this.SERVICE);
	},

	load(frm, force) {
		const tab = frm._pm_tab;
		if (!tab) return;
		if (frm._pm_timer) {
			clearInterval(frm._pm_timer);
			frm._pm_timer = null;
		}
		if (!force && frm._pm_data && frm._pm_data_project === frm.doc.name) {
			this.render(frm);
			return;
		}
		tab.wrapper.html(this.loading_html());
		frappe.call({
			method: "teampro.teampro_py.project_monitoring.get_project_monitoring_data",
			args: {
				project: frm.doc.name,
				service: frm.doc.service,
				display_currency: frm._pm_currency,
			},
			callback: (r) => {
				if (frm._pm_tab !== tab) return;
				frm._pm_data = r.message;
				frm._pm_data_project = frm.doc.name;
				frm._pm_filters = {
					status: [], bucket: [], assignee: [], priority: [], task_type: [],
					search: "", overdue_only: false,
					meeting_status: [], meeting_search: "", meeting_bucket: [],
					flag: null, meeting_flag: null,
					sort_key: "status_order", sort_dir: 1, page: 1,
				};
				this.render(frm);
			},
			error: () => {
				tab.wrapper.html(
					`<div class="pm-empty">${__("Unable to load monitoring data.")}</div>`
				);
			},
		});
	},

	loading_html() {
		return `<div class="pm-empty"><i class="fa fa-spinner fa-spin"></i> ${__("Loading project monitoring...")}</div>`;
	},

	render(frm) {
		const d = frm._pm_data;
		const tab = frm._pm_tab;
		if (!d || !tab) return;
		const p = d.project || {};
		(d.tasks || []).forEach((t) => (t._scope_start = p.expected_start_date));

		// AMC: scope all task widgets to the SLA period (customer SLA Details)
		d._sla_scoped = false;
		if (d.is_amc) {
			const c = d.contract || {};
			if (c.sla_from && c.sla_to) {
				d._all_tasks = d.tasks || [];
				d.tasks = d._all_tasks.filter((t) => {
					const cd = String(t.creation || "").slice(0, 10);
					return cd >= c.sla_from && cd <= c.sla_to;
				});
				d._sla_scoped = true;
				d._amc_stats = {};
				d.tasks.forEach((t) => {
					const s = d._amc_stats[t.status] = d._amc_stats[t.status] || { count: 0, hrs: 0 };
					s.count += 1;
					s.hrs += t.et || 0;
				});
				d._all_meetings = d.meetings || [];
				d.meetings = d._all_meetings.filter((m) => {
					const md = String(m.date || m.creation || "").slice(0, 10);
					return md >= c.sla_from && md <= c.sla_to;
				});
			}
		}

		const $html = $(
			`<div class="pm-wrap">${this.head_html(frm, d)}` +
			`${d.is_amc ? this.amc_body_html(d) : this.impl_body_html()}</div>`
		);
		tab.wrapper.empty().append($html);
		this.wire_common($html, frm, d);
	},

	head_html(frm, d) {
		const p = d.project || {};
		const c = d.contract || {};
		const status_badge = p.status
			? `<span class="pm-badge ${this.status_badge_class(p.status)}">${__(p.status)}</span>`
			: "";
		const priority_badge = p.priority
			? `<span class="pm-badge pm-b-red">${__(p.priority)} ${__("priority")}</span>`
			: "";
		const progress_badge = `<span class="pm-badge pm-b-blue">${(d.kpis && d.kpis.task_completion) || 0}%</span>`;

		const ctx = [];
		if (p.customer) ctx.push(`${__("Customer")}: <b>${frappe.utils.escape_html(p.customer)}</b>`);
		if (p.account_manager)
			ctx.push(`${__("AM")}: <b>${frappe.utils.escape_html(p.account_manager)}</b>`);
		if (p.spoc)
			ctx.push(`${__("SPOC")}: <b>${frappe.utils.escape_html(p.spoc)}</b>`);
		if (p.project_type) ctx.push(`${__("Type")}: <b>${frappe.utils.escape_html(p.project_type)}</b>`);
		if (d.is_amc) {
			if (c.sla_from && c.sla_to)
				ctx.push(`${__("SLA")}: <b>${frappe.datetime.str_to_user(c.sla_from)} → ${frappe.datetime.str_to_user(c.sla_to)}</b>`);
			const period = [c.years && c.years !== "00" ? c.years + "y" : "",
				c.months && c.months !== "00" ? c.months + "m" : ""]
				.filter(Boolean).join(" ");
			if (period) ctx.push(`${__("Contract")}: <b>${frappe.utils.escape_html(period)}</b>`);
			if (c.billing_status)
				ctx.push(`${__("Billing")}: <b>${frappe.utils.escape_html(c.billing_status)}</b>`);
			if (c.expected_billing_date)
				ctx.push(`${__("Next Bill")}: <b>${frappe.datetime.str_to_user(c.expected_billing_date)}</b>`);
		}
		if (!d.is_amc) {
			if (p.expected_start_date)
				ctx.push(`${__("Start")}: <b>${frappe.datetime.str_to_user(p.expected_start_date)}</b>`);
			if (p.expected_end_date)
				ctx.push(`${__("Expected End")}: <b>${frappe.datetime.str_to_user(p.expected_end_date)}</b>`);
		}

		return `
			<div class="pm-head">
				<div class="pm-title">
					<span class="pm-title-text">${frappe.utils.escape_html(p.project_name || p.name || "")}</span>
					${status_badge} ${priority_badge} ${progress_badge}
				</div>
				<div class="pm-toolbar">
					<div class="pm-countdown" title="${__("Time remaining to Expected End Date")}"></div>
					<select class="pm-currency form-control input-xs" title="${__("Display currency")}"></select>
					<button class="btn btn-xs btn-default pm-refresh">&#8635; ${__("Refresh")}</button>
					<button class="btn btn-xs btn-default pm-export">&#8681; ${__("Export")}</button>
				</div>
			</div>
			<div class="pm-context">${ctx.join(" &nbsp;&middot;&nbsp; ")}</div>`;
	},

	impl_body_html() {
		return `
				<div class="pm-kpi-grid"></div>

				<div class="pm-chart-grid">
					<div class="pm-section pm-chart-card">
						<div class="pm-section-title">${__("Task Status")} <span class="pm-sub">(${__("Based on Hours")})</span></div>
						<div class="pm-donut-row pm-task-donut"></div>
					</div>
					<div class="pm-section pm-chart-card">
						<div class="pm-section-title">${__("Meeting Status")} <span class="pm-sub">(${__("Based on Count")})</span></div>
						<div class="pm-donut-row pm-meeting-donut"></div>
					</div>
					<div class="pm-section pm-chart-card pm-cost-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-amber">&#8377;</span>${__("Project Financials")} <span class="pm-sub">(${__("From Sales Orders")})</span></div>
						<div class="pm-fin-list"></div>
						<div class="pm-fin-extra"></div>
					</div>
				</div>

				<div class="pm-duo-grid">
					<div class="pm-section pm-hours-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-teal">&#9201;</span>${__("Estimated vs Actual Hours")}</div>
						<div class="pm-hours-body"></div>
					</div>
					<div class="pm-section pm-chart-card">
						<div class="pm-section-title">${__("Task Aging by Status")} <span class="pm-sub">(${__("Based on Hours")})</span></div>
						<div class="pm-aging-bars"></div>
					</div>
				</div>

				<div class="pm-section">
					<div class="pm-section-title"><span class="pm-sec-icon pm-i-red">&#10084;</span>${__("Project Health")} <span class="pm-sub">(${__("click a flag to filter")})</span></div>
					<div class="pm-health-grid"></div>
				</div>

				<div class="pm-section">
					<div class="pm-section-title pm-sec-head">
						<span>${__("Task Monitoring")}</span>
						<div class="pm-sec-controls">
							<div class="pm-f-status pm-ms"></div>
							<div class="pm-f-priority pm-ms"></div>
							<div class="pm-f-assignee pm-ms"></div>
							<div class="pm-f-type pm-ms"></div>
							<div class="pm-f-aging pm-ms"></div>
							<input class="pm-f-search form-control input-xs" placeholder="${__("Search Tasks...")}">
							<button class="btn btn-xs btn-primary pm-view-tasks">${__("View All")}</button>
						</div>
					</div>
					<div class="pm-tasks"></div>
					<div class="pm-pager"></div>
				</div>

				<div class="pm-section">
					<div class="pm-section-title pm-sec-head">
						<span>${__("Meeting Monitoring")}</span>
						<div class="pm-sec-controls">
							<div class="pm-f-mstatus pm-ms"></div>
							<div class="pm-f-maging pm-ms"></div>
							<input class="pm-f-msearch form-control input-xs" placeholder="${__("Search Meetings...")}">
							<button class="btn btn-xs btn-primary pm-view-meetings">${__("View All")}</button>
						</div>
					</div>
					<div class="pm-meetings"></div>
				</div>

				<div class="pm-duo-grid">
					<div class="pm-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-blue">&#128100;</span>${__("SPOC Remark")}<span class="pm-note-date pm-spoc-remark-date"></span></div>
						<div class="pm-note pm-spoc-remark"></div>
					</div>
					<div class="pm-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-teal">&#128100;</span>${__("AM Remark")}<span class="pm-note-date pm-am-remark-date"></span></div>
						<div class="pm-note pm-am-remark"></div>
					</div>
				</div>

				<div class="pm-duo-grid">
					<div class="pm-section pm-remark-card">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-purple">&#9998;</span>${__("Project Remarks")}</div>
						<div class="pm-remark-body">
							<textarea class="form-control pm-remark-input" rows="3" placeholder="${__("Add review remarks...")}"></textarea>
							<div class="pm-remark-actions"><button class="btn btn-xs btn-primary pm-remark-btn">${__("Update")}</button></div>
						</div>
					</div>
					<div class="pm-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-green">&#128337;</span>${__("Recent Remarks / Daily Updates")}</div>
						<div class="pm-timeline"></div>
					</div>
				</div>
		`;
	},

	amc_body_html(d) {
		const sla_note = d && d._sla_scoped
			? ` <span class="pm-sub">(${__("SLA period")}: ${frappe.datetime.str_to_user(d.contract.sla_from)} → ${frappe.datetime.str_to_user(d.contract.sla_to)})</span>`
			: "";
		return `
				<div class="pm-kpi-grid"></div>

				<div class="pm-chart-grid">
					<div class="pm-section pm-chart-card">
						<div class="pm-section-title">${__("Task Status")} <span class="pm-sub">(${__("Based on Hrs")})</span>${sla_note}</div>
						<div class="pm-donut-row pm-amc-donut"></div>
					</div>
					<div class="pm-section pm-chart-card">
						<div class="pm-section-title">${__("Meeting Status")} <span class="pm-sub">(${__("Based on Count")})</span></div>
						<div class="pm-donut-row pm-meeting-donut"></div>
					</div>
					<div class="pm-section pm-chart-card pm-cost-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-amber">&#8377;</span>${__("Project Financials")} <span class="pm-sub">(${__("From Sales Orders")})</span></div>
						<div class="pm-fin-list"></div>
						<div class="pm-fin-extra"></div>
					</div>
				</div>

				<div class="pm-duo-grid">
					<div class="pm-section pm-chart-card">
						<div class="pm-section-title">${__("Tasks Raised vs Completed")} <span class="pm-sub">(${__("Monthly")})</span></div>
						<div class="pm-task-monthly"></div>
					</div>
					<div class="pm-section pm-chart-card">
						<div class="pm-section-title">${__("Task Aging by Status")} <span class="pm-sub">(${__("Based on Hrs")})</span></div>
						<div class="pm-amc-aging"></div>
					</div>
				</div>

				<div class="pm-section">
					<div class="pm-section-title"><span class="pm-sec-icon pm-i-red">&#10084;</span>${__("Task Health")} <span class="pm-sub">(${__("click a flag to filter")})</span></div>
					<div class="pm-health-grid"></div>
				</div>

				<div class="pm-section">
					<div class="pm-section-title pm-sec-head">
						<span>${__("Task Monitoring")}${sla_note}</span>
						<div class="pm-sec-controls">
							<div class="pm-f-status pm-ms"></div>
							<div class="pm-f-priority pm-ms"></div>
							<div class="pm-f-assignee pm-ms"></div>
							<div class="pm-f-type pm-ms"></div>
							<div class="pm-f-aging pm-ms"></div>
							<input class="pm-f-search form-control input-xs" placeholder="${__("Search Tasks...")}">
							<button class="btn btn-xs btn-primary pm-view-tasks">${__("View All")}</button>
						</div>
					</div>
					<div class="pm-tasks"></div>
					<div class="pm-pager"></div>
				</div>

				<div class="pm-section">
					<div class="pm-section-title pm-sec-head">
						<span>${__("Meeting Monitoring")}</span>
						<div class="pm-sec-controls">
							<div class="pm-f-mstatus pm-ms"></div>
							<div class="pm-f-maging pm-ms"></div>
							<input class="pm-f-msearch form-control input-xs" placeholder="${__("Search Meetings...")}">
							<button class="btn btn-xs btn-primary pm-view-meetings">${__("View All")}</button>
						</div>
					</div>
					<div class="pm-meetings"></div>
				</div>

				<div class="pm-duo-grid">
					<div class="pm-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-blue">&#128100;</span>${__("SPOC Remark")}<span class="pm-note-date pm-spoc-remark-date"></span></div>
						<div class="pm-note pm-spoc-remark"></div>
					</div>
					<div class="pm-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-teal">&#128100;</span>${__("AM Remark")}<span class="pm-note-date pm-am-remark-date"></span></div>
						<div class="pm-note pm-am-remark"></div>
					</div>
				</div>

				<div class="pm-duo-grid">
					<div class="pm-section pm-remark-card">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-purple">&#9998;</span>${__("Project Remarks")}</div>
						<div class="pm-remark-body">
							<textarea class="form-control pm-remark-input" rows="3" placeholder="${__("Add review remarks...")}"></textarea>
							<div class="pm-remark-actions"><button class="btn btn-xs btn-primary pm-remark-btn">${__("Update")}</button></div>
						</div>
					</div>
					<div class="pm-section">
						<div class="pm-section-title"><span class="pm-sec-icon pm-i-green">&#128337;</span>${__("Recent Remarks / Daily Updates")}</div>
						<div class="pm-timeline"></div>
					</div>
				</div>
		`;
	},

	wire_common($html, frm, d) {
		const p = d.project || {};

		const $cur = $html.find(".pm-currency");
		(d.currencies || []).forEach((c) =>
			$cur.append(`<option value="${frappe.utils.escape_html(c)}">${frappe.utils.escape_html(c)}</option>`)
		);
		$cur.val((d.billing && d.billing.display_currency) || "");
		$cur.on("change", () => {
			frm._pm_currency = $cur.val();
			this.load(frm, true);
		});

		this.render_cost($html, d.billing || {}, d);
		const sla_end = d.is_amc ? (d.contract || {}).sla_to : null;
		this.render_countdown($html, frm, p, sla_end, sla_end ? __("to SLA End") : null);
		this.render_meeting_donut($html, frm, d);
		this.render_timeline($html, d);
		this.render_project_notes($html, d);
		this.render_remark_controls($html, frm, d);
		this.render_meeting_controls($html, frm, d);
		this.render_meetings($html, frm, d);
		if (d.is_amc) {
			this.render_amc_kpis($html, frm, d);
			this.render_amc_task_donut($html, frm, d);
			this.render_task_monthly($html, d);
			this.render_amc_aging($html, frm, d);
			this.render_health($html, frm, d);
			this.render_task_controls($html, frm, d);
			this.render_tasks($html, frm, d);
		} else {
			this.render_kpis($html, frm, d);
			this.render_task_donut($html, frm, d);
			this.render_aging_bars($html, frm, d);
			this.render_hours($html, d);
			this.render_health($html, frm, d);
			this.render_task_controls($html, frm, d);
			this.render_tasks($html, frm, d);
		}

		$html.find(".pm-refresh").on("click", () => this.load(frm, true));
		$html.find(".pm-export").on("click", () => this.export_csv(frm));
		$html.find(".pm-view-tasks").on("click", () => {
			frappe.route_options = { project: frm.doc.name, service: frm.doc.service };
			frappe.set_route("List", "Task");
		});
		$html.find(".pm-view-issues").on("click", () => {
			frappe.route_options = { project: frm.doc.name };
			frappe.set_route("List", "Issue");
		});
		$html.find(".pm-view-meetings").on("click", () => {
			frappe.route_options = { project: frm.doc.name };
			frappe.set_route("List", "Meeting");
		});
	},

	// ---------- Cost & Billing ----------

	render_cost($html, b, d) {
		const ccy = b.display_currency;
		const fmt = (v) => format_currency(v || 0, ccy);
		if ((b.missing_rates || []).length) {
			$html.find(".pm-cost-section .pm-section-title").append(
				`<span class="pm-sub" style="color:#b25e09;">&#9888; ${__("No exchange rate for")} ${frappe.utils.escape_html(b.missing_rates.join(", "))}</span>`
			);
		}
		const rows = [
			{ label: __("SO - Value"), val: b.so_value },
			{ label: __("Billed - Value"), val: b.billed_value },
			{ label: __("To Bill"), val: b.outstanding_amount },
			{ label: __("Collection Pending"), val: b.collection_pending },
		];
		$html.find(".pm-fin-list").html(
			rows
				.map(
					(r) => `<div class="pm-fin-row">
						<span class="pm-fin-label">${r.label}</span>
						<span class="pm-fin-colon">:</span>
						<b class="pm-fin-val">${fmt(r.val)}</b>
					</div>`
				)
				.join("")
		);

		const est = b.estimated_costing || 0;
		const actual = b.total_costing_amount || 0;

		// Projected final cost = actual + balance hrs * avg cost/hr
		const hrs = (d && d.hours) || {};
		if (hrs.actual && actual) {
			const rate = actual / hrs.actual;
			const projected = actual + Math.max(hrs.balance || 0, 0) * rate;
			const over = projected - est;
			$html.find(".pm-fin-extra").append(
				`<div class="pm-cost-proj">${__("Projected final cost")}: <b>${fmt(projected)}</b>` +
				(est && over > 0
					? ` <span class="pm-badge pm-b-red">+${fmt(over)} ${__("over")}</span>`
					: "") + `</div>`
			);
		}

		// Collection aging strip
		const ca = b.collection_aging || {};
		const catotal = (ca["0-30"] || 0) + (ca["31-60"] || 0) + (ca["60+"] || 0);
		if (catotal) {
			const colors = { "0-30": "#22c55e", "31-60": "#eab308", "60+": "#ef4444" };
			const segs = Object.keys(colors)
				.filter((k) => ca[k] > 0)
				.map((k) => `<span class="pm-age-seg" style="width:${(ca[k] / catotal) * 100}%;background:${colors[k]}" title="${k} ${__("days")}: ${fmt(ca[k])}"></span>`)
				.join("");
			const labels = Object.keys(colors)
				.map((k) => `<span><span class="pm-legend-dot" style="background:${colors[k]}"></span>${k}d <b>${fmt(ca[k] || 0)}</b></span>`)
				.join("");
			$html.find(".pm-fin-extra").append(
				`<div class="pm-cost-proj">${__("Collection aging")}</div>
				<div class="pm-cost-bar">${segs}</div>
				<div class="pm-legend-inline">${labels}</div>`
			);
		}
	},

	// ---------- Countdown to Expected End ----------

	render_countdown($html, frm, p, end_date, end_label) {
		const $el = $html.find(".pm-countdown");
		if (frm._pm_timer) {
			clearInterval(frm._pm_timer);
			frm._pm_timer = null;
		}
		const end = end_date || p.expected_end_date;
		if (!end) {
			$el.html(`<span class="pm-cd-label">${__("No end date")}</span>`);
			return;
		}
		if (this.CLOSED_PROJECT.includes(p.status)) {
			$el.html(`<span class="pm-cd-label">${__(p.status)}</span>`);
			return;
		}
		const label = end_label || __("to Expected End");
		const target = new Date(`${end}T23:59:59`).getTime();
		const pad = (n) => String(n).padStart(2, "0");
		const tick = () => {
			const diff = target - Date.now();
			const abs = Math.abs(diff);
			const days = Math.floor(abs / 86400000);
			const hrs = Math.floor((abs % 86400000) / 3600000);
			const min = Math.floor((abs % 3600000) / 60000);
			const sec = Math.floor((abs % 60000) / 1000);
			if (diff >= 0) {
				$el.removeClass("pm-cd-over").html(
					`<span class="pm-cd-label">${label}</span>` +
					` <b>${days}</b>d <b>${pad(hrs)}</b>h <b>${pad(min)}</b>m <b>${pad(sec)}</b>s`);
			} else {
				$el.addClass("pm-cd-over").html(
					`<span class="pm-cd-label">${__("Overdue by")}</span>` +
					` <b>${days}</b>d <b>${pad(hrs)}</b>h <b>${pad(min)}</b>m <b>${pad(sec)}</b>s`);
			}
		};
		tick();
		frm._pm_timer = setInterval(tick, 1000);
	},

	// ---------- KPI row (spec: 5 cards) ----------

	render_kpis($html, frm, d) {
		const k = d.kpis || {};
		const mk = d.meeting_kpis || {};
		const p = d.project || {};
		const ot = d.open_tasks || {};
		const wt = d.working_tasks || {};
		const hrs = d.hours || {};
		const fh = (v) => `${this.hr(v)} ${__("Hrs")}`;

		let days_val, days_note, days_cls = "pm-kpi-violet";
		if (this.CLOSED_PROJECT.includes(p.status)) {
			days_val = p.status;
			days_note = __("Project closed");
		} else if (!p.expected_end_date) {
			days_val = "-";
			days_note = __("No end date");
		} else {
			const diff = frappe.datetime.get_diff(
				p.expected_end_date, frappe.datetime.get_today());
			if (diff < 0) {
				days_val = __("Overdue");
				days_note = `${Math.abs(diff)} ${__("days past end date")}`;
				days_cls = "pm-kpi-red";
			} else {
				days_val = diff;
				days_note = __("Days Remaining");
			}
		}

		const bal_note = hrs.overrun
			? `${__("Overrun")} ${fh(hrs.overrun)}`
			: __("Remaining");

		$html.find(".pm-kpi-grid").html(`
			<div class="pm-kpi">
				<span class="pm-kpi-icon pm-i-gray">&#128194;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Open Tasks")}</div>
					<div class="pm-kpi-value">${fh(ot.hours)} <span class="pm-sub">(${ot.count || 0})</span></div>
					<div class="pm-kpi-note">${__("Estimated hours on open tasks")}</div>
				</div>
			</div>
			<div class="pm-kpi">
				<span class="pm-kpi-icon pm-i-blue">&#9881;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Working Tasks")}</div>
					<div class="pm-kpi-value">${fh(wt.hours)} <span class="pm-sub">(${wt.count || 0})</span></div>
					<div class="pm-kpi-note">${__("Estimated hours in progress")}</div>
				</div>
			</div>
			<div class="pm-kpi">
				<span class="pm-kpi-icon pm-i-teal">&#x1F4C5;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Meetings")}</div>
					<div class="pm-kpi-value">${mk.in_progress || 0} <span class="pm-sub">/ ${mk.total || 0}</span></div>
					<div class="pm-kpi-note">${__("In Progress / Total")}</div>
				</div>
			</div>
			<div class="pm-kpi ${days_cls}">
				<span class="pm-kpi-icon ${days_cls === "pm-kpi-red" ? "pm-i-red" : "pm-i-purple"}">&#9200;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Days to End")}</div>
					<div class="pm-kpi-value">${days_val}</div>
					<div class="pm-kpi-note">${days_note}</div>
				</div>
			</div>
			<div class="pm-kpi ${hrs.balance < 0 ? "pm-kpi-red" : ""}">
				<span class="pm-kpi-icon ${hrs.balance < 0 ? "pm-i-red" : "pm-i-green"}">&#9201;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Balance Hrs")}</div>
					<div class="pm-kpi-value ${hrs.balance < 0 ? "pm-neg" : ""}">${fh(hrs.balance)}</div>
					<div class="pm-kpi-note">${bal_note}</div>
				</div>
			</div>
		`);
	},

	// ---------- Donut charts ----------

	donut(el, labels, values, colors, size) {
		if (!el) return;
		const total = values.reduce((a, v) => a + (Number(v) || 0), 0);
		const safeTotal = total || 1;
		let cursor = 0;
		const stops = [];
		values.forEach((value, i) => {
			const pct = ((Number(value) || 0) / safeTotal) * 100;
			const start = cursor;
			const end = cursor + pct;
			stops.push(`${colors[i] || "#cbd5e1"} ${start}% ${end}%`);
			cursor = end;
		});
		if (!stops.length) stops.push("#e2e8f0 0% 100%");
		el.innerHTML = `<div class="pm-css-donut" style="--pm-donut-bg: conic-gradient(${stops.join(",")}); --pm-donut-size:${size || 150}px;"><div class="pm-css-donut-hole"></div></div>`;
	},

	hours_statuses(status_hours) {
		const keys = Object.keys(status_hours || {});
		return [
			...this.HOURS_STATUSES,
			...keys.filter((s) => !this.HOURS_STATUSES.includes(s)),
		].filter((s) => status_hours[s]);
	},

	render_task_donut($html, frm, d) {
		const me = this;
		const sh = d.status_hours || {};
		const statuses = this.hours_statuses(sh)
			.filter((s) => !this.CHART_EXCLUDE.includes(s));
		const total_hrs = statuses.reduce((a, s) => a + (sh[s].hours || 0), 0);

		const $row = $html.find(".pm-task-donut").empty();
		const $wrap = $('<div class="pm-donut-wrap"><div class="pm-donut-chart" style="width:148px;height:148px;"></div>' +
			`<div class="pm-donut-center">${this.hr(total_hrs)}<small>${__("Hrs")}</small></div></div>`);
		const $legend = $('<div class="pm-legend pm-task-legend"></div>');
		$row.append($wrap).append($legend);

		this.donut($wrap.find(".pm-donut-chart")[0], statuses,
			statuses.map((s) => sh[s].hours),
			statuses.map((s) => this.STATUS_HEX[s] || "#94a3b8"), 150);

		statuses.forEach((s) => {
			const pct = total_hrs ? Math.round((sh[s].hours / total_hrs) * 100) : 0;
			const $it = $(`<div class="pm-legend-item" data-status="${s}">
				<span class="pm-legend-dot" style="background:${this.STATUS_HEX[s] || "#94a3b8"}"></span>
				<span class="pm-legend-name">${__(s)}</span>
				<span class="pm-legend-val">${this.hr(sh[s].hours)} ${__("Hrs")} (${pct}%)</span>
			</div>`);
			$it.on("click", () => {
				const cur = frm._pm_filters.status || [];
				me.set_status_filter($html, frm, d,
					cur.includes(s) ? cur.filter((x) => x !== s) : [...cur, s]);
			});
			$legend.append($it);
		});
	},

	render_meeting_donut($html, frm, d) {
		const me = this;
		const counts = {};
		(d.meetings || []).forEach((m) => (counts[m.status] = (counts[m.status] || 0) + 1));
		const statuses = this.MEETING_STATUSES.filter((s) => counts[s])
			.concat(Object.keys(counts).filter((s) => !this.MEETING_STATUSES.includes(s)))
			.filter((s) => !this.MEETING_CHART_EXCLUDE.includes(s));
		const total = statuses.reduce((a, s) => a + counts[s], 0);

		const $row = $html.find(".pm-meeting-donut").empty();
		const $wrap = $('<div class="pm-donut-wrap"><div class="pm-donut-chart" style="width:148px;height:148px;"></div>' +
			`<div class="pm-donut-center">${total}<small>${__("Meetings")}</small></div></div>`);
		const $legend = $('<div class="pm-legend pm-meeting-legend"></div>');
		$row.append($wrap).append($legend);

		this.donut($wrap.find(".pm-donut-chart")[0], statuses,
			statuses.map((s) => counts[s]),
			statuses.map((s) => this.meeting_status_color(s)), 150);

		statuses.forEach((s) => {
			const pct = total ? Math.round((counts[s] / total) * 100) : 0;
			const $it = $(`<div class="pm-legend-item" data-status="${s}">
				<span class="pm-legend-dot" style="background:${this.meeting_status_color(s)}"></span>
				<span class="pm-legend-name">${__(s)}</span>
				<span class="pm-legend-val">${counts[s]} (${pct}%)</span>
			</div>`);
			$it.on("click", () => {
				const cur = frm._pm_filters.meeting_status || [];
				me.set_meeting_filter($html, frm, d,
					cur.includes(s) ? cur.filter((x) => x !== s) : [...cur, s]);
			});
			$legend.append($it);
		});
	},

	// ---------- Task aging (stacked by status, based on hours) ----------

	render_aging_bars($html, frm, d) {
		const me = this;
		const $wrap = $html.find(".pm-aging-bars").empty();
		const rows = d.aging_hours || [];
		const max = Math.max(1, ...rows.map((b) => b.total));
		rows.forEach((b, i) => {
			const segs = Object.entries(b.segments || {})
				.filter(([, hrs]) => hrs > 0)
				.map(
					([status, hrs]) =>
						`<span class="pm-age-seg" style="width:${Math.max((hrs / max) * 100, 1)}%;` +
						`background:${this.STATUS_HEX[status] || "#94a3b8"}" ` +
						`title="${frappe.utils.escape_html(status)}: ${this.hr(hrs)} ${__("Hrs")}"></span>`
				)
				.join("");
			const $row = $(`<div class="pm-age-row" data-bucket="${b.label}">
				<span>${__(b.label)}</span>
				<span class="pm-age-track">${segs || '<span class="pm-age-seg" style="width:0%"></span>'}</span>
				<span class="pm-age-num">${this.hr(b.total)}<small>${__("Hrs")}</small></span>
			</div>`);
			$row.on("click", () => {
				const cur = frm._pm_filters.bucket || [];
				me.set_bucket_filter($html, frm, d,
					cur.includes(b.label) ? cur.filter((x) => x !== b.label) : [...cur, b.label]);
			});
			$wrap.append($row);
		});

		const seg_statuses = [...new Set(rows.flatMap((b) => Object.keys(b.segments || {})))]
			.sort((a, b) => (this.STATUS_SORT[a] ?? 100) - (this.STATUS_SORT[b] ?? 100));
		const SHORT = { "Pending Review": "PR", "Code Review": "CR", "Client Review": "CR" };
		const seg_counts = {};
		(d.tasks || []).forEach((t) => {
			if (!this.CLOSED_TASK.includes(t.status))
				seg_counts[t.status] = (seg_counts[t.status] || 0) + 1;
		});
		if (seg_statuses.length) {
			const $leg = $('<div class="pm-aging-legend"></div>');
			seg_statuses.forEach((s) => {
				const $it = $(`<div class="pm-legend-item pm-aging-leg ${(frm._pm_filters.status || []).includes(s) ? "pm-active" : ""}">
					<span class="pm-legend-dot" style="background:${this.STATUS_HEX[s] || "#94a3b8"}"></span>
					<span class="pm-legend-name" title="${frappe.utils.escape_html(s)}">${__(SHORT[s] || s)}</span>
					<span class="pm-legend-val">(${seg_counts[s] || 0})</span>
				</div>`);
				$it.on("click", () => {
					const cur = frm._pm_filters.status || [];
					me.set_status_filter($html, frm, d,
						cur.includes(s) ? cur.filter((x) => x !== s) : [...cur, s]);
				});
				$leg.append($it);
			});
			$wrap.append($leg);
		}
	},

	// ---------- Estimated vs Actual hours ----------

	render_hours($html, d) {
		const h = d.hours || {};
		const est = h.estimated || 0;
		const act = h.actual || 0;
		const base = Math.max(est, act, 1);
		const bar = (label, val, color) => `
			<div class="pm-hours-row">
				<span class="pm-hours-label">${label}</span>
				<span class="pm-hours-track"><span class="pm-age-seg" style="width:${(Math.max(val, 0) / base) * 100}%;background:${color}"></span></span>
				<span class="pm-hours-val">${this.hr(val)} ${__("Hrs")}</span>
			</div>`;
		const from_project = h.task_estimated != null && Math.abs((h.task_estimated || 0) - est) > 0.004;
		$html.find(".pm-hours-body").html(`
			${bar(__("Estimated Hours"), est, "#3b82f6")}
			${bar(__("Actual Hours"), act, act > est ? "#ef4444" : "#22c55e")}
			${bar(__("Balance Hours"), h.balance || 0, (h.balance || 0) < 0 ? "#ef4444" : "#8b5cf6")}
			${from_project ? `<div class="pm-sub" style="margin-top:4px;">${__("Estimated from Project")} &middot; ${__("task total")}: ${this.hr(h.task_estimated)} ${__("Hrs")}</div>` : ""}
		`);

		// Burn rate vs required pace
		const p = d.project || {};
		const today = frappe.datetime.get_today();
		if (p.expected_start_date && p.expected_end_date && act) {
			const elapsed = Math.max(frappe.datetime.get_diff(today, p.expected_start_date), 1);
			const left = Math.max(frappe.datetime.get_diff(p.expected_end_date, today), 1);
			const burn = act / elapsed;
			const required = Math.max(h.balance || 0, 0) / left;
			const behind = required > burn * 1.1;
			$html.find(".pm-hours-body").append(
				`<div class="pm-burn ${behind ? "pm-burn-bad" : ""}">` +
				`${__("Burn")}: <b>${this.hr(burn)} ${__("hrs/day")}</b> &middot; ` +
				`${__("Required pace")}: <b>${this.hr(required)} ${__("hrs/day")}</b>` +
				(behind ? ` &middot; <span class="pm-badge pm-b-red">${__("Behind pace")}</span>` : "") +
				`</div>`
			);
		}
	},

	// ---------- Project Health flags ----------

	task_flags(t) {
		if (t._flags) return t._flags;
		const flags = [];
		const closed = this.CLOSED_TASK.includes(t.status);
		const today = frappe.datetime.get_today();
		const stale_days = (dt) =>
			dt ? frappe.datetime.get_diff(today, String(dt).slice(0, 10)) : 0;
		if (!closed) {
			if (t.overdue) flags.push("overdue");
			if (stale_days(t.modified) > 7) flags.push("stale");
			if (t.status === "Hold") flags.push("hold");
			if (t.status === "Client Review" && stale_days(t.modified) > 7) flags.push("client_stale");
			if (t.is_milestone && t.exp_end_date && t.exp_end_date < today) flags.push("milestone");
			if ((t.revisions || 0) >= 10) flags.push("churn");
			if (t._scope_start && t.creation && String(t.creation).slice(0, 10) > t._scope_start)
				flags.push("scope");
		}
		if (t.completed_on && !closed) flags.push("reopened");
		t._flags = flags;
		return flags;
	},

	render_health($html, frm, d) {
		const me = this;
		const tasks = d.tasks || [];
		const meetings = d.meetings || [];
		const chips = [
			{ key: "overdue", label: __("Overdue Tasks"), cls: "pm-h-red" },
			{ key: "stale", label: __("Stale >7d"), cls: "pm-h-amber" },
			{ key: "hold", label: __("On Hold"), cls: "pm-h-amber" },
			{ key: "client_stale", label: __("Client Review >7d"), cls: "pm-h-orange" },
			{ key: "milestone", label: __("Milestones Overdue"), cls: "pm-h-red" },
			{ key: "reopened", label: __("Reopened"), cls: "pm-h-blue" },
			{ key: "churn", label: __("High Rework"), cls: "pm-h-purple" },
			{ key: "scope", label: __("Scope Added"), cls: "pm-h-teal" },
		];
		const action_overdue = meetings.reduce((a, m) => a + (m.overdue_items || 0), 0);
		const action_open = meetings.reduce((a, m) => a + (m.open_items || 0), 0);

		const $grid = $html.find(".pm-health-grid").empty();
		chips.forEach((c) => {
			const count = tasks.filter((t) => me.task_flags(t).includes(c.key)).length;
			const $chip = $(`<div class="pm-health-chip ${c.cls} ${count ? "" : "pm-h-zero"} ${frm._pm_filters.flag === c.key ? "pm-active" : ""}">
				<span class="pm-h-count">${count}</span><span>${c.label}</span>
			</div>`);
			$chip.on("click", () => {
				const f = frm._pm_filters;
				f.flag = f.flag === c.key ? null : c.key;
				f.page = 1;
				$grid.find(".pm-health-chip").removeClass("pm-active");
				if (f.flag) $chip.addClass("pm-active");
				me.render_tasks($html, frm, d);
				$html.find(".pm-tasks")[0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
			});
			$grid.append($chip);
		});

		const $ai = $(`<div class="pm-health-chip pm-h-red ${action_overdue ? "" : "pm-h-zero"} ${frm._pm_filters.meeting_flag === "action_overdue" ? "pm-active" : ""}">
			<span class="pm-h-count">${action_overdue}</span><span>${__("Action Items Overdue")}</span>
			<span class="pm-sub">(${action_open} ${__("open")})</span>
		</div>`);
		$ai.on("click", () => {
			const f = frm._pm_filters;
			f.meeting_flag = f.meeting_flag === "action_overdue" ? null : "action_overdue";
			$html.find(".pm-health-chip").removeClass("pm-active");
			if (f.meeting_flag) $ai.addClass("pm-active");
			me.render_meetings($html, frm, d);
			$html.find(".pm-meetings")[0]?.scrollIntoView({ behavior: "smooth", block: "nearest" });
		});
		$grid.append($ai);
	},

	// ---------- Remarks / timeline ----------

	render_remark_controls($html, frm, d) {
		const me = this;
		const $ta = $html.find(".pm-remark-input");
		$html.find(".pm-remark-btn").on("click", () => {
			const remark = ($ta.val() || "").trim();
			if (!remark) {
				frappe.show_alert({ message: __("Please enter a remark"), indicator: "orange" });
				return;
			}
			frappe.call({
				method: "teampro.teampro_py.project_monitoring.add_project_remark",
				args: { project: frm.doc.name, remark },
				callback: () => {
					frappe.show_alert({ message: __("Remark saved"), indicator: "green" });
					$ta.val("");
					me.load(frm, true);
				},
			});
		});
	},

	render_project_notes($html, d) {
		const p = d.project || {};
		const note = (sel, dateSel, text, dt) => {
			const $el = $html.find(sel);
			if (dt) {
				$html.find(dateSel).html(`&nbsp;&mdash;&nbsp;${frappe.datetime.str_to_user(dt)}`);
			}
			if (!text) {
				$el.html(`<div class="pm-empty">${__("No remark")}</div>`);
				return;
			}
			$el.html(`<div class="pm-note-text">${frappe.utils.escape_html(text)}</div>`);
		};
		note(".pm-spoc-remark", ".pm-spoc-remark-date", p.custom_spoc_remark, p.custom_spoc_remark_date);
		note(".pm-am-remark", ".pm-am-remark-date", p.remark, p.custom_am_remark_date);
	},

	render_timeline($html, d) {
		const entries = [
			...(d.remarks || []).map((r) => ({ ...r, kind: "Remark", cls: "pm-b-purple" })),
			...(d.daily_updates || []).map((r) => ({ ...r, kind: "Daily Update", cls: "pm-b-blue" })),
		].sort((a, b) => (a.creation < b.creation ? 1 : -1));

		const $tl = $html.find(".pm-timeline").empty();
		if (!entries.length) {
			$tl.html(`<div class="pm-empty">${__("No remarks or updates yet.")}</div>`);
			return;
		}
		entries.slice(0, 15).forEach((e) => {
			const parts = String(e.creation || "").split(" ");
			const date = frappe.datetime.str_to_user(parts[0] || e.creation);
			const time = parts[1] ? parts[1].substring(0, 5) : "";
			$tl.append(`
				<div class="pm-tl-item">
					<div class="pm-tl-meta">
						<b>${date}</b> <span class="pm-sub">${time}</span>
						<span class="pm-badge ${e.cls}">${__(e.kind)}</span>
						<span class="pm-sub">${frappe.utils.escape_html(e.comment_by || e.comment_email || "")}</span>
					</div>
					<div class="pm-tl-content">${e.content || ""}</div>
				</div>`);
		});
	},

	// ---------- Filters ----------

	bucket_for(age) {
		for (const [label, low, high] of this.AGING_BUCKETS) {
			if (age >= low && (high === null || age <= high)) return label;
		}
		return "30+ Days";
	},

	multiselect($html, sel, placeholder, get_options, on_change) {
		const ctrl = frappe.ui.form.make_control({
			parent: $html.find(sel),
			df: {
				fieldtype: "MultiSelectList",
				fieldname: sel.replace(/[^a-z]/g, "_"),
				placeholder: placeholder,
				get_data: (txt) =>
					(get_options() || [])
						.filter((o) => !txt || o.toLowerCase().includes(txt.toLowerCase())),
				onchange: () => on_change(ctrl.get_value() || []),
			},
			render_input: true,
			only_input: true,
		});
		ctrl.refresh();
		return ctrl;
	},

	sync_ms(frm, key, values) {
		const ctrl = frm._pm_ctrl && frm._pm_ctrl[key];
		if (ctrl && JSON.stringify(ctrl.get_value() || []) !== JSON.stringify(values)) {
			ctrl.set_value(values);
		}
	},

	set_status_filter($html, frm, d, statuses) {
		const f = frm._pm_filters;
		f.status = statuses || [];
		f.overdue_only = false;
		f.page = 1;
		this.sync_ms(frm, "status", f.status);
		$html.find(".pm-task-legend .pm-legend-item").removeClass("pm-active");
		f.status.forEach((s) =>
			$html.find(`.pm-task-legend .pm-legend-item[data-status="${s}"]`).addClass("pm-active"));
		this.render_tasks($html, frm, d);
	},

	set_bucket_filter($html, frm, d, buckets) {
		const f = frm._pm_filters;
		f.bucket = buckets || [];
		f.page = 1;
		this.sync_ms(frm, "bucket", f.bucket);
		$html.find(".pm-age-row").removeClass("pm-active");
		f.bucket.forEach((b) =>
			$html.find(`.pm-age-row[data-bucket="${b}"]`).addClass("pm-active"));
		this.render_tasks($html, frm, d);
	},

	set_meeting_filter($html, frm, d, statuses) {
		const f = frm._pm_filters;
		f.meeting_status = statuses || [];
		this.sync_ms(frm, "meeting_status", f.meeting_status);
		$html.find(".pm-meeting-legend .pm-legend-item").removeClass("pm-active");
		f.meeting_status.forEach((s) =>
			$html.find(`.pm-meeting-legend .pm-legend-item[data-status="${s}"]`).addClass("pm-active"));
		this.render_meetings($html, frm, d);
	},

	set_filter($html, frm, d, key, values) {
		const f = frm._pm_filters;
		f[key] = values || [];
		f.page = 1;
		this.sync_ms(frm, key, f[key]);
		if (key.indexOf("meeting") === 0) this.render_meetings($html, frm, d);
		else this.render_tasks($html, frm, d);
	},

	task_matches(t, f, except) {
		if (f.flag && !this.task_flags(t).includes(f.flag)) return false;
		if (f.overdue_only && !t.overdue) return false;
		if (except !== "status" && f.status.length && !f.status.includes(t.status)) return false;
		if (!f.status.length && this.CLOSED_TASK.includes(t.status)) return false;
		if (except !== "bucket" && f.bucket.length &&
			(!f.bucket.includes(t.aging_bucket) || this.CLOSED_TASK.includes(t.status))) return false;
		if (except !== "assignee" && f.assignee.length &&
			!f.assignee.includes(t.allocated_to)) return false;
		if (except !== "priority" && f.priority.length && !f.priority.includes(t.priority)) return false;
		if (except !== "task_type" && f.task_type.length && !f.task_type.includes(t.task_type)) return false;
		if (f.search) {
			const hay = `${t.name} ${t.subject || ""}`.toLowerCase();
			if (!hay.includes(f.search)) return false;
		}
		return true;
	},

	render_task_controls($html, frm, d) {
		const me = this;
		const statuses = this.hours_statuses(d.status_hours || d.status_counts || {});
		const priorities = [...new Set((d.tasks || []).map((t) => t.priority).filter(Boolean))].sort();
		const types = [...new Set((d.tasks || []).map((t) => t.task_type).filter(Boolean))].sort();
		const buckets = (d.aging_buckets || []).map((b) => b.label);
		const f = frm._pm_filters;

		const cascade_assignees = () => {
			const set = new Set();
			(d.tasks || [])
				.filter((t) => me.task_matches(t, f, "assignee"))
				.forEach((t) => t.allocated_to && set.add(t.allocated_to));
			return [...set].sort();
		};

		frm._pm_ctrl = frm._pm_ctrl || {};
		frm._pm_ctrl.status = this.multiselect($html, ".pm-f-status", __("All Status"),
			() => statuses, (v) => me.set_status_filter($html, frm, d, v));
		frm._pm_ctrl.priority = this.multiselect($html, ".pm-f-priority", __("All Priority"),
			() => priorities, (v) => me.set_filter($html, frm, d, "priority", v));
		frm._pm_ctrl.assignee = this.multiselect($html, ".pm-f-assignee", __("All Assignees"),
			cascade_assignees, (v) => me.set_filter($html, frm, d, "assignee", v));
		frm._pm_ctrl.task_type = this.multiselect($html, ".pm-f-type", __("All Issue Type"),
			() => types, (v) => me.set_filter($html, frm, d, "task_type", v));
		frm._pm_ctrl.bucket = this.multiselect($html, ".pm-f-aging", __("Age Filter"),
			() => buckets, (v) => me.set_bucket_filter($html, frm, d, v));

		$html.find(".pm-f-search").on("input", function () {
			f.search = ($(this).val() || "").toLowerCase();
			f.page = 1;
			me.render_tasks($html, frm, d);
		});
	},

	filtered_tasks(frm, d) {
		const f = frm._pm_filters || {};
		const rows = (d.tasks || []).filter((t) => this.task_matches(t, f));

		const dir = f.sort_dir || 1;
		const key = f.sort_key || "status_order";
		const pri = (t) => this.PRIORITY_ORDER[t.priority] != null ? this.PRIORITY_ORDER[t.priority] : 9;
		const getters = {
			age: (t) => t.age || 0,
			et: (t) => t.et || 0,
			rt: (t) => t.rt || 0,
			status: (t) => t.status || "",
			status_order: (t) => {
				const r = this.STATUS_SORT[t.status];
				if (r != null) return r;
				return this.CLOSED_TASK.includes(t.status) ? 200 : 100;
			},
			priority: pri,
			task_type: (t) => t.task_type || "",
			subject: (t) => (t.subject || t.name || "").toLowerCase(),
		};
		const get = getters[key] || getters.status_order;
		rows.sort((a, b) => {
			const va = get(a);
			const vb = get(b);
			let cmp = typeof va === "string" ? va.localeCompare(vb) * -dir : (va - vb) * dir;
			if (!cmp) cmp = (b.age || 0) - (a.age || 0);
			return cmp;
		});
		return rows;
	},

	filtered_meetings(frm, d) {
		const f = frm._pm_filters || {};
		return (d.meetings || []).filter((m) => {
			if (f.meeting_flag === "action_overdue" && !(m.overdue_items > 0)) return false;
			if (f.meeting_status.length && !f.meeting_status.includes(m.status)) return false;
			if (!f.meeting_status.length && this.CLOSED_MEETING.includes(m.status)) return false;
			if (f.meeting_bucket.length && !f.meeting_bucket.includes(this.bucket_for(m.age))) return false;
			if (f.meeting_search) {
				const hay = `${m.name} ${m.title || ""} ${m.organized_by || ""}`.toLowerCase();
				if (!hay.includes(f.meeting_search)) return false;
			}
			return true;
		});
	},

	status_badge_class(status, context) {
		const map = {
			Completed: "pm-b-green",
			Closed: "pm-b-green",
			Cancelled: "pm-b-gray",
			Overdue: "pm-b-red",
			Working: "pm-b-blue",
			"In Progress": "pm-b-blue",
			"Code Review": "pm-b-purple",
			"Pending Review": "pm-b-yellow",
			"Client Review": "pm-b-orange",
			Ready: "pm-b-teal",
			Planned: "pm-b-blue",
			"Invitation Sent": "pm-b-teal",
			Hold: "pm-b-yellow",
			Template: "pm-b-gray",
			Open: "pm-b-gray",
		};
		return map[status] || "pm-b-gray";
	},

	status_badge(status, context) {
		return `<span class="pm-badge ${this.status_badge_class(status, context)}">${__(status)}</span>`;
	},

	meeting_status_color(status) {
		return this.STATUS_HEX[status] || "#94a3b8";
	},

	avatar(user) {
		const palette = ["#2d9cdb", "#6b46c1", "#1a7f4b", "#b25e09", "#c53030", "#0f766e"];
		let hash = 0;
		for (let i = 0; i < user.length; i++) hash = (hash * 31 + user.charCodeAt(i)) % 997;
		const color = palette[hash % palette.length];
		const name = user.split("@")[0].replace(/[._]/g, " ");
		const initials = name
			.split(" ")
			.filter(Boolean)
			.slice(0, 2)
			.map((w) => w[0].toUpperCase())
			.join("");
		return `<span class="pm-avatar" style="background:${color}">${initials || "?"}</span>${frappe.utils.escape_html(name)}`;
	},

	// ---------- Task table ----------

	sortable_th(label, key, frm, pfx) {
		const f = frm._pm_filters || {};
		pfx = pfx || "";
		const arrow = f[pfx + "sort_key"] === key ? (f[pfx + "sort_dir"] === 1 ? " &#9650;" : " &#9660;") : "";
		return `<th class="pm-sort" data-key="${key}">${label}${arrow}</th>`;
	},

	render_tasks($html, frm, d) {
		const me = this;
		const tasks = this.filtered_tasks(frm, d);
		const f = frm._pm_filters || {};
		if (!tasks.length) {
			$html.find(".pm-tasks").html(`<div class="pm-empty">${__("No tasks match the current filters.")}</div>`);
			$html.find(".pm-pager").empty();
			return;
		}

		const pages = Math.ceil(tasks.length / this.PAGE_SIZE);
		f.page = Math.min(Math.max(f.page || 1, 1), pages);
		const slice = tasks.slice((f.page - 1) * this.PAGE_SIZE, f.page * this.PAGE_SIZE);
		const offset = (f.page - 1) * this.PAGE_SIZE;

		const rows = slice
			.map(
				(t, i) => `<tr>
				<td>${offset + i + 1}</td>
				<td class="pm-task-cell"><a href="/app/task/${encodeURIComponent(t.name)}">${frappe.utils.escape_html(t.subject || t.name)}</a>
					${t.is_group ? ' <span class="pm-badge pm-b-gray">Grp</span>' : ""}</td>
				<td>${frappe.utils.escape_html(t.task_type || "-")}</td>
				<td>${t.allocated_to ? this.avatar(t.allocated_to) : "-"}</td>
				<td>${this.status_badge(t.status)}</td>
				<td>${t.priority || "-"}</td>
				<td class="${t.age > 7 && !this.CLOSED_TASK.includes(t.status) ? "pm-age-hot" : ""}">${t.age}</td>
				<td>${this.hr(t.et)}</td>
				<td>${this.hr(t.rt)}${t.overrun ? ` <span class="pm-sub" title="${__("Overrun")}">(+${this.hr(t.overrun)})</span>` : ""}</td>
				<td><a href="/app/task/${encodeURIComponent(t.name)}" class="pm-badge pm-b-blue">${__("View")}</a></td>
			</tr>`
			)
			.join("");

		$html.find(".pm-tasks").html(`
			<div class="pm-table-wrap">
			<table class="pm-table">
				<thead><tr>
					<th>#</th>
					${this.sortable_th(__("Task"), "subject", frm)}
					${this.sortable_th(__("Issue Type"), "task_type", frm)}
					<th>${__("Allocated To")}</th>
					${this.sortable_th(__("Status"), "status", frm)}
					${this.sortable_th(__("Priority"), "priority", frm)}
					${this.sortable_th(__("Age (Days)"), "age", frm)}
					${this.sortable_th(__("ET (Hrs)"), "et", frm)}
					${this.sortable_th(__("RT (Hrs)"), "rt", frm)}
					<th>${__("Action")}</th>
				</tr></thead>
				<tbody>${rows}</tbody>
			</table></div>`);

		$html.find(".pm-tasks .pm-sort").on("click", function () {
			const key = $(this).data("key");
			if (f.sort_key === key) f.sort_dir = -(f.sort_dir || -1);
			else {
				f.sort_key = key;
				f.sort_dir = -1;
			}
			f.page = 1;
			me.render_tasks($html, frm, d);
		});

		const $pager = $html.find(".pm-pager").empty();
		if (pages > 1) {
			$pager.html(`
				<button class="btn btn-xs btn-default pm-pg-prev" ${f.page === 1 ? "disabled" : ""}>&lsaquo; ${__("Prev")}</button>
				<span class="pm-sub">${__("Page")} ${f.page} / ${pages} &middot; ${tasks.length} ${__("tasks")}</span>
				<button class="btn btn-xs btn-default pm-pg-next" ${f.page === pages ? "disabled" : ""}>${__("Next")} &rsaquo;</button>`);
			$pager.find(".pm-pg-prev").on("click", () => {
				f.page -= 1;
				me.render_tasks($html, frm, d);
			});
			$pager.find(".pm-pg-next").on("click", () => {
				f.page += 1;
				me.render_tasks($html, frm, d);
			});
		}
	},

	// ---------- Meeting table ----------

	render_meeting_controls($html, frm, d) {
		const me = this;
		const f = frm._pm_filters;
		const present = new Set((d.meetings || []).map((m) => m.status));
		const mstatuses = this.MEETING_STATUSES.concat(
			[...present].filter((s) => !this.MEETING_STATUSES.includes(s))
		);
		const buckets = this.AGING_BUCKETS.map(([label]) => label);

		frm._pm_ctrl = frm._pm_ctrl || {};
		frm._pm_ctrl.meeting_status = this.multiselect($html, ".pm-f-mstatus", __("All Status"),
			() => mstatuses, (v) => me.set_meeting_filter($html, frm, d, v));
		frm._pm_ctrl.meeting_bucket = this.multiselect($html, ".pm-f-maging", __("Age Filter"),
			() => buckets, (v) => me.set_filter($html, frm, d, "meeting_bucket", v));

		$html.find(".pm-f-msearch").on("input", function () {
			frm._pm_filters.meeting_search = ($(this).val() || "").toLowerCase();
			me.render_meetings($html, frm, d);
		});
	},

	render_meetings($html, frm, d) {
		const meetings = this.filtered_meetings(frm, d);
		if (!meetings.length) {
			$html.find(".pm-meetings").html(`<div class="pm-empty">${__("No meetings match the current filter.")}</div>`);
			return;
		}
		const rows = meetings
			.map((m, i) => `<tr>
				<td>${i + 1}</td>
				<td class="pm-task-cell"><a href="/app/meeting/${encodeURIComponent(m.name)}">${frappe.utils.escape_html(m.title || m.name)}</a></td>
				<td>${m.date ? frappe.datetime.str_to_user(m.date) : "-"}</td>
				<td>${m.organized_by ? this.avatar(m.organized_by) : "-"}</td>
				<td>${m.participants != null ? m.participants : "-"}</td>
				<td class="${m.age > 7 && !this.CLOSED_MEETING.includes(m.status) ? "pm-age-hot" : ""}">${m.age}</td>
				<td>${this.status_badge(m.status, "meeting")}</td>
				<td><a href="/app/meeting/${encodeURIComponent(m.name)}" class="pm-badge pm-b-blue">${__("View")}</a></td>
			</tr>`)
			.join("");
		$html.find(".pm-meetings").html(`
			<div class="pm-table-wrap">
			<table class="pm-table">
				<thead><tr>
					<th>#</th><th>${__("Meeting")}</th><th>${__("Date")}</th><th>${__("Meeting Owner")}</th>
					<th>${__("Participants")}</th><th>${__("Age (Days)")}</th><th>${__("Status")}</th><th>${__("Action")}</th>
				</tr></thead>
				<tbody>${rows}</tbody>
			</table></div>`);
	},

	// ---------- AMC: task-based layout ----------

	render_amc_kpis($html, frm, d) {
		const p = d.project || {};
		const tasks = d.tasks || [];
		const month = frappe.datetime.get_today().slice(0, 7);
		const done = tasks.filter((t) =>
			this.CLOSED_TASK.includes(t.status) && (t.completed_on || "").slice(0, 7) === month);
		const open = tasks.filter((t) => t.status === "Open");
		const work = tasks.filter((t) => t.status === "Working");
		const hrs = (list) => list.reduce((a, t) => a + (t.et || 0), 0);
		const fh = (list) => `${this.hr(hrs(list))} ${__("Hrs")} <span class="pm-sub">(${list.length})</span>`;
		const sla_end = (d.contract || {}).sla_to || p.expected_end_date;

		let days_val, days_note, days_cls = "pm-kpi-violet";
		if (this.CLOSED_PROJECT.includes(p.status)) {
			days_val = p.status;
			days_note = __("Contract closed");
		} else if (!sla_end) {
			days_val = "-";
			days_note = __("No SLA end date");
		} else {
			const diff = frappe.datetime.get_diff(
				sla_end, frappe.datetime.get_today());
			if (diff < 0) {
				days_val = __("Overdue");
				days_note = `${Math.abs(diff)} ${__("days past contract end")}`;
				days_cls = "pm-kpi-red";
			} else {
				days_val = diff;
				days_note = __("Days Remaining");
			}
		}

		$html.find(".pm-kpi-grid").html(`
			<div class="pm-kpi">
				<span class="pm-kpi-icon pm-i-gray">&#128194;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Open Tasks")}</div>
					<div class="pm-kpi-value">${fh(open)}</div>
					<div class="pm-kpi-note">${tasks.length} ${__("total")}${d._sla_scoped ? " (" + __("SLA period") + ")" : ""}</div>
				</div>
			</div>
			<div class="pm-kpi">
				<span class="pm-kpi-icon pm-i-blue">&#9881;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Working Tasks")}</div>
					<div class="pm-kpi-value">${fh(work)}</div>
					<div class="pm-kpi-note">${__("In progress")}</div>
				</div>
			</div>
			<div class="pm-kpi">
				<span class="pm-kpi-icon pm-i-green">&#10003;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Completed This Month")}</div>
					<div class="pm-kpi-value">${fh(done)}</div>
					<div class="pm-kpi-note">${__("Tasks closed this month")}</div>
				</div>
			</div>
			<div class="pm-kpi ${days_cls}">
				<span class="pm-kpi-icon ${days_cls === "pm-kpi-red" ? "pm-i-red" : "pm-i-purple"}">&#9200;</span>
				<div class="pm-kpi-body">
					<div class="pm-kpi-label">${__("Contract Days Left")}</div>
					<div class="pm-kpi-value">${days_val}</div>
					<div class="pm-kpi-note">${days_note}</div>
				</div>
			</div>
		`);
	},

	render_amc_task_donut($html, frm, d) {
		const me = this;
		// per-status {count, hrs} — scoped when SLA-scoped, else derive from all tasks
		const stats = d._amc_stats || (() => {
			const m = {};
			(d.tasks || []).forEach((t) => {
				const s = m[t.status] = m[t.status] || { count: 0, hrs: 0 };
				s.count += 1;
				s.hrs += t.et || 0;
			});
			return m;
		})();
		const statuses = Object.keys(stats)
			.filter((s) => stats[s].count > 0)
			.filter((s) => !this.CHART_EXCLUDE.includes(s))
			.sort((a, b) => (this.STATUS_SORT[a] ?? 100) - (this.STATUS_SORT[b] ?? 100));
		const total_hrs = statuses.reduce((a, s) => a + stats[s].hrs, 0);

		const $row = $html.find(".pm-amc-donut").empty();
		const $wrap = $('<div class="pm-donut-wrap"><div class="pm-donut-chart" style="width:148px;height:148px;"></div>' +
			`<div class="pm-donut-center">${this.hr(total_hrs)}<small>${__("Hrs")}</small></div></div>`);
		const $legend = $('<div class="pm-legend pm-task-legend"></div>');
		$row.append($wrap).append($legend);

		this.donut($wrap.find(".pm-donut-chart")[0], statuses,
			statuses.map((s) => stats[s].hrs),
			statuses.map((s) => this.STATUS_HEX[s] || "#94a3b8"), 150);

		statuses.forEach((s) => {
			const pct = total_hrs ? Math.round((stats[s].hrs / total_hrs) * 100) : 0;
			const $it = $(`<div class="pm-legend-item" data-status="${frappe.utils.escape_html(s)}">
				<span class="pm-legend-dot" style="background:${this.STATUS_HEX[s] || "#94a3b8"}"></span>
				<span class="pm-legend-name">${__(s)}</span>
				<span class="pm-legend-val">${this.hr(stats[s].hrs)}h (${stats[s].count}) &middot; ${pct}%</span>
			</div>`);
			$it.on("click", () => {
				const cur = frm._pm_filters.status || [];
				me.set_status_filter($html, frm, d,
					cur.includes(s) ? cur.filter((x) => x !== s) : [...cur, s]);
			});
			$legend.append($it);
		});
	},

	render_task_monthly($html, d) {
		const tasks = d.tasks || [];
		const buckets = {};
		const months = [];
		const MNAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
			"Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
		const c = d.contract || {};
		if (d._sla_scoped && c.sla_from && c.sla_to) {
			// months covering the SLA period
			let cur = c.sla_from.slice(0, 7);
			const end = c.sla_to.slice(0, 7);
			while (cur <= end && months.length < 36) {
				months.push(cur);
				const [y, m] = cur.split("-").map(Number);
				cur = `${m === 12 ? y + 1 : y}-${String(m === 12 ? 1 : m + 1).padStart(2, "0")}`;
			}
		} else {
			for (let k = 5; k >= 0; k--) {
				months.push(frappe.datetime.add_months(frappe.datetime.get_today(), -k).slice(0, 7));
			}
		}
		months.forEach((key) => {
			const [y, m] = key.split("-");
			buckets[key] = { label: `${MNAMES[+m - 1]} ${y}`, raised: 0, done: 0 };
		});
		tasks.forEach((t) => {
			const ck = (t.creation || "").slice(0, 7);
			if (buckets[ck]) buckets[ck].raised += 1;
			const dk = (t.completed_on || "").slice(0, 7);
			if (buckets[dk]) buckets[dk].done += 1;
		});
		const rows = months.map((k) => buckets[k]);
		const max = Math.max(1, ...rows.flatMap((m) => [m.raised, m.done]));
		$html.find(".pm-task-monthly").html(`
			<div class="pm-mn-chart">
				${rows.map((m) => `
					<div class="pm-mn-col">
						<div class="pm-mn-bars">
							<span class="pm-mn-bar" style="height:${Math.max((m.raised / max) * 100, 2)}%;background:#3b82f6" title="${m.label}: ${m.raised} ${__("raised")}"></span>
							<span class="pm-mn-bar" style="height:${Math.max((m.done / max) * 100, 2)}%;background:#22c55e" title="${m.label}: ${m.done} ${__("completed")}"></span>
						</div>
						<div class="pm-mn-label">${m.label}</div>
					</div>`).join("")}
			</div>
			<div class="pm-legend-inline">
				<span><span class="pm-legend-dot" style="background:#3b82f6"></span>${__("Raised")}</span>
				<span><span class="pm-legend-dot" style="background:#22c55e"></span>${__("Completed")}</span>
			</div>`);
	},

	render_amc_aging($html, frm, d) {
		const me = this;
		const $wrap = $html.find(".pm-amc-aging").empty();
		const order = this.AGING_BUCKETS.map(([label]) => label);
		const rows = order.map((label) => ({ label, hrs: 0, count: 0, segments: {} }));
		const by_label = Object.fromEntries(rows.map((r) => [r.label, r]));
		(d.tasks || []).forEach((t) => {
			if (this.CLOSED_TASK.includes(t.status)) return;
			const r = by_label[t.aging_bucket];
			if (!r) return;
			const h = t.et || 0;
			r.hrs += h;
			r.count += 1;
			const seg = r.segments[t.status] = r.segments[t.status] || { hrs: 0, count: 0 };
			seg.hrs += h;
			seg.count += 1;
		});
		const max = Math.max(1, ...rows.map((b) => b.hrs));
		rows.forEach((b) => {
			const segs = Object.entries(b.segments)
				.sort((a, b2) => (this.STATUS_SORT[a[0]] ?? 100) - (this.STATUS_SORT[b2[0]] ?? 100))
				.map(([s, n]) =>
					`<span class="pm-age-seg" style="width:${Math.max((n.hrs / max) * 100, 1)}%;` +
					`background:${this.STATUS_HEX[s] || "#94a3b8"}" ` +
					`title="${frappe.utils.escape_html(s)}: ${this.hr(n.hrs)}h (${n.count})"></span>`)
				.join("");
			const $row = $(`<div class="pm-age-row" data-bucket="${b.label}">
				<span>${__(b.label)}</span>
				<span class="pm-age-track">${segs || '<span class="pm-age-seg" style="width:0%"></span>'}</span>
				<span class="pm-age-num">${this.hr(b.hrs)}h (${b.count})</span>
			</div>`);
			$row.on("click", () => {
				const cur = frm._pm_filters.bucket || [];
				me.set_bucket_filter($html, frm, d,
					cur.includes(b.label) ? cur.filter((x) => x !== b.label) : [...cur, b.label]);
			});
			$wrap.append($row);
		});

		const seg_statuses = [...new Set(rows.flatMap((b) => Object.keys(b.segments)))]
			.sort((a, b) => (this.STATUS_SORT[a] ?? 100) - (this.STATUS_SORT[b] ?? 100));
		if (seg_statuses.length) {
			const $leg = $('<div class="pm-aging-legend"></div>');
			seg_statuses.forEach((s) => {
				const seg = (d._amc_stats || {})[s] || {};
				const $it = $(`<div class="pm-legend-item pm-aging-leg ${(frm._pm_filters.status || []).includes(s) ? "pm-active" : ""}">
					<span class="pm-legend-dot" style="background:${this.STATUS_HEX[s] || "#94a3b8"}"></span>
					<span class="pm-legend-name" title="${frappe.utils.escape_html(s)}">${__(this.STATUS_SHORT[s] || s)}</span>
					<span class="pm-legend-val">${this.hr(seg.hrs || 0)}h (${seg.count || 0})</span>
				</div>`);
				$it.on("click", () => {
					const cur = frm._pm_filters.status || [];
					me.set_status_filter($html, frm, d,
						cur.includes(s) ? cur.filter((x) => x !== s) : [...cur, s]);
				});
				$leg.append($it);
			});
			$wrap.append($leg);
		}
	},

	// ---------- Export ----------

	export_csv(frm) {
		const d = frm._pm_data;
		if (!d) return;
		const tasks = this.filtered_tasks(frm, d);
		const header = ["Task", "Subject", "Issue Type", "Allocated To", "Status", "Priority", "Age (days)", "ET (Hrs)", "RT (Hrs)", "Overdue"];
		const rows = tasks.map((t) => [
			t.name,
			t.subject || "",
			t.task_type || "",
			t.allocated_to || "",
			t.status,
			t.priority || "",
			t.age,
			this.hr(t.et),
			this.hr(t.rt),
			t.overdue ? "Yes" : "No",
		]);
		const csv = [header, ...rows]
			.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(","))
			.join("\n");
		const blob = new Blob([csv], { type: "text/csv" });
		const a = document.createElement("a");
		a.href = URL.createObjectURL(blob);
		a.download = `${frm.doc.name}-tasks.csv`;
		a.click();
	},
};
