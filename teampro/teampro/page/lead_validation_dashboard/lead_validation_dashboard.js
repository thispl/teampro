frappe.pages['lead-validation-dashboard'].on_page_load = function (wrapper) {
	try {
		var page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'AI Lead Validation Dashboard',
			single_column: true,
		});
		frappe.breadcrumbs.add('TEAMPRO');

	// Inject CSS
	const style = document.createElement('style');
	style.innerHTML = `
		.lv-dashboard { padding: 20px; }
		.lv-selector-row { display: flex; gap: 12px; align-items: flex-end; margin-bottom: 24px; }
		.lv-selector-row .form-group { flex: 1; }
		.lv-results-card {
			border-radius: 10px;
			padding: 24px;
			margin-bottom: 24px;
			box-shadow: 0 2px 8px rgba(0,0,0,0.08);
			background: #fff;
			display: none;
		}
		.lv-results-card.show { display: block; }
		.lv-score-badge {
			display: inline-flex;
			align-items: center;
			justify-content: center;
			width: 70px; height: 70px;
			border-radius: 50%;
			font-size: 22px; font-weight: 700;
			color: #fff;
		}
		.lv-badge-green  { background: #28a745; }
		.lv-badge-yellow { background: #ffc107; color: #333; }
		.lv-badge-red    { background: #dc3545; }
		.lv-badge-gray   { background: #6c757d; }
		.lv-rating-tag {
			display: inline-block;
			padding: 4px 14px;
			border-radius: 20px;
			font-weight: 600;
			font-size: 14px;
			margin-left: 12px;
		}
		.lv-tag-green  { background: #d4edda; color: #155724; }
		.lv-tag-yellow { background: #fff3cd; color: #856404; }
		.lv-tag-red    { background: #f8d7da; color: #721c24; }
		.lv-tag-gray   { background: #e2e3e5; color: #383d41; }
		.lv-results-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px; }
		.lv-results-grid .lv-section h5 { font-weight: 600; margin-bottom: 8px; color: #555; }
		.lv-results-grid .lv-section p { margin: 0; line-height: 1.6; }
		.lv-validation-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 16px; }
		.lv-validation-item { text-align: center; padding: 12px 8px; border-radius: 8px; border: 1px solid #e0e0e0; }
		.lv-validation-item.pass { background: #d4edda; border-color: #c3e6cb; }
		.lv-validation-item.fail { background: #f8d7da; border-color: #f5c6cb; }
		.lv-validation-item .lv-v-icon { font-size: 20px; margin-bottom: 4px; }
		.lv-validation-item .lv-v-label { font-size: 11px; font-weight: 600; color: #555; }
		.lv-validation-item .lv-v-weight { font-size: 10px; color: #888; }
		.lv-table { width: 100%; margin-top: 10px; }
		.lv-table th { background: #2490ef; color: #fff; padding: 10px; font-size: 13px; }
		.lv-table td { padding: 8px 10px; font-size: 13px; vertical-align: middle; }
		.lv-table tr:nth-child(even) { background: #f8f9fa; }
		.lv-loading {
			display: none;
			text-align: center;
			padding: 40px;
		}
		.lv-loading.show { display: block; }
		.lv-spinner {
			width: 40px; height: 40px;
			border: 4px solid #f3f3f3;
			border-top: 4px solid #2490ef;
			border-radius: 50%;
			animation: lv-spin 1s linear infinite;
			margin: 0 auto 12px;
		}
		@keyframes lv-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
		.lv-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
		.lv-empty-state { text-align: center; padding: 40px; color: #999; }
	`;
	document.head.appendChild(style);

	var $content = $(page.body) || $(wrapper).find('.layout-main-section') || $(wrapper);
	$content.html(`
		<div class="lv-dashboard">
			<div class="lv-header-row">
				<h3 class="fw-bold mb-0">AI Lead Validation Dashboard</h3>
				<button id="lv-refresh-leads" class="btn btn-sm btn-outline-primary">Refresh Lead List</button>
			</div>

			<!-- Lead Selector -->
			<div class="lv-selector-row">
				<div class="form-group" style="margin-bottom: 0; flex: 1;">
					<label class="form-label" style="font-size: 12px; font-weight: 600;">Select Lead</label>
					<div id="lv-lead-selector-wrapper"></div>
				</div>
				<button id="lv-run-validation" class="btn btn-primary" style="white-space: nowrap;">
					⚡ Run AI Validation
				</button>
			</div>

			<!-- Loading indicator -->
			<div id="lv-loading" class="lv-loading">
				<div class="lv-spinner"></div>
				<p class="text-muted">Running AI validation... Please wait.</p>
			</div>

			<!-- Results Card -->
			<div id="lv-results-card" class="lv-results-card">
				<div class="d-flex align-items-center mb-3">
					<div id="lv-score-badge" class="lv-score-badge"></div>
					<div class="ml-3">
						<h4 id="lv-lead-title" class="mb-1"></h4>
						<span id="lv-rating-tag" class="lv-rating-tag"></span>
					</div>
				</div>
				<div class="lv-results-grid">
					<div class="lv-section">
						<h5>AI Summary</h5>
						<p id="lv-summary"></p>
					</div>
					<div class="lv-section">
						<h5>Recommended Next Steps</h5>
						<p id="lv-next-step"></p>
					</div>
				</div>
				<div id="lv-validation-section" style="margin-top: 20px;">
					<h5 style="font-weight: 600; margin-bottom: 10px; color: #555;">Validation Matrix Breakdown <span id="lv-raw-score" style="font-size: 12px; color: #888;"></span></h5>
					<div id="lv-validation-grid" class="lv-validation-grid"></div>
				</div>
			</div>

			<!-- Unvalidated Leads Table -->
			<div class="mt-4">
				<h5 class="fw-bold mb-2">Recent Unvalidated Leads <span id="lv-lead-count" class="badge badge-secondary" style="font-size: 11px;"></span></h5>
				<div style="overflow-x: auto;">
				<table class="table lv-table table-bordered" style="min-width: 1200px;">
					<thead>
						<tr>
							<th>Company Name</th>
							<th>Website</th>
							<th>Industry</th>
							<th>Employee Size</th>
							<th>Location</th>
							<th>Contact Name</th>
							<th>Designation</th>
							<th>Email</th>
							<th>Phone</th>
							<th>Status</th>
							<th>Action</th>
						</tr>
					</thead>
					<tbody id="lv-leads-tbody">
						<tr><td colspan="11" class="text-center text-muted">Loading...</td></tr>
					</tbody>
				</table>
				</div>
			</div>
		</div>
	`);

	// --- State ---
	let selectedLead = null;

	// --- Init lead selector as Link field ---
	try {
		const leadSelector = frappe.ui.form.make_control({
			df: {
				fieldname: 'lv_lead_link',
				fieldtype: 'Link',
				options: 'Lead',
				placeholder: 'Select Lead',
				only_select: true,
			},
			parent: $('#lv-lead-selector-wrapper').empty()[0],
		});
		leadSelector.make();
		leadSelector.$input.on('awesomplete-selectcomplete', function () {
			selectedLead = leadSelector.get_value();
		});
	} catch (e) {
		console.error('Lead selector init error:', e);
		$('#lv-lead-selector-wrapper').html('<input type="text" id="lv-lead-manual" class="form-control" placeholder="Enter Lead ID (e.g. CRM-LEAD-2026-00001)">');
		$('#lv-lead-manual').on('change', function () {
			selectedLead = $(this).val().trim();
		});
	}

	// --- Run Validation ---
	$('#lv-run-validation').on('click', function () {
		if (!selectedLead) {
			frappe.msgprint('Please select a Lead first.');
			return;
		}
		runValidation(selectedLead);
	});

	// --- Refresh leads table ---
	$('#lv-refresh-leads').on('click', loadUnvalidatedLeads);

	// --- Initial load (deferred so page paints first) ---
	setTimeout(loadUnvalidatedLeads, 100);

	// --- Functions ---
	function runValidation(leadId) {
		$('#lv-loading').addClass('show');
		$('#lv-results-card').removeClass('show');

		frappe.call({
			method: 'teampro.lead_validation.validate_lead_ai',
			args: { lead_id: leadId },
			freeze: true,
			freeze_message: 'Running AI Validation...',
			callback: function (r) {
				$('#lv-loading').removeClass('show');
				if (r.exc) {
					frappe.msgprint('Validation failed: ' + (r.exc || 'Unknown error'));
					return;
				}
				showResults(leadId, r.message);
				loadUnvalidatedLeads();
			},
		});
	}

	function showResults(leadId, data) {
		const colorClass = data.color || 'gray';
		const badgeClass = 'lv-badge-' + colorClass;
		const tagClass = 'lv-tag-' + colorClass;

		$('#lv-score-badge')
			.removeClass('lv-badge-green lv-badge-yellow lv-badge-red lv-badge-gray')
			.addClass(badgeClass)
			.text(data.score);

		$('#lv-lead-title').text(leadId);
		$('#lv-rating-tag')
			.removeClass('lv-tag-green lv-tag-yellow lv-tag-red lv-tag-gray')
			.addClass(tagClass)
			.text(data.rating);

		$('#lv-summary').text(data.summary || 'N/A');
		$('#lv-next-step').text(data.next_action || 'N/A');

		// Render validation matrix breakdown
		const v = data.validation || {};
		const criteria = [
			{ key: 'company_validated', label: 'Company Validated', weight: 1 },
			{ key: 'hiring_verified', label: 'Hiring Verified', weight: 2 },
			{ key: 'relevant_contact', label: 'Relevant Contact', weight: 1 },
			{ key: 'industry_fit', label: 'Industry Fit', weight: 1 },
			{ key: 'no_risk_flags', label: 'No Risk Flags', weight: 1 },
		];
		let vHtml = '';
		criteria.forEach(function (c) {
			const passed = v[c.key];
			const cls = passed ? 'pass' : 'fail';
			const icon = passed ? '✓' : '✗';
			vHtml += `
				<div class="lv-validation-item ${cls}">
					<div class="lv-v-icon">${icon}</div>
					<div class="lv-v-label">${c.label}</div>
					<div class="lv-v-weight">weight: ${c.weight}</div>
				</div>
			`;
		});
		$('#lv-validation-grid').html(vHtml);
		$('#lv-raw-score').text(`(Raw Score: ${data.raw_score || 0}/6)`);

		$('#lv-results-card').addClass('show');
	}

	function loadUnvalidatedLeads() {
		$('#lv-leads-tbody').html('<tr><td colspan="11" class="text-center text-muted">Loading...</td></tr>');
		frappe.call({
			method: 'teampro.lead_validation.get_unvalidated_leads',
			callback: function (r) {
				if (r.exc) return;
				const leads = r.message || [];
				$('#lv-lead-count').text(leads.length);
				if (!leads.length) {
					$('#lv-leads-tbody').html(
						'<tr><td colspan="11" class="text-center text-muted">No unvalidated leads found.</td></tr>'
					);
					return;
				}
				let html = '';
				leads.forEach(function (lead) {
					var location = [lead.city, lead.country].filter(Boolean).join(', ') || '-';
					var phone = lead.mobile_no || lead.phone || '-';
					html += `
						<tr>
							<td>${lead.company_name || lead.lead_name || lead.name}</td>
							<td>${lead.website || '-'}</td>
							<td>${lead.industry || '-'}</td>
							<td>${lead.no_of_employees || '-'}</td>
							<td>${location}</td>
							<td>${lead.lead_name || '-'}</td>
							<td>${lead.job_title || '-'}</td>
							<td>${lead.email_id || '-'}</td>
							<td>${phone}</td>
							<td>${lead.status || '-'}</td>
							<td>
								<button class="btn btn-sm btn-primary lv-validate-btn" data-lead="${lead.name}">
									Validate
								</button>
							</td>
						</tr>
					`;
				});
				$('#lv-leads-tbody').html(html);

				$('.lv-validate-btn').on('click', function () {
					const lid = $(this).data('lead');
					runValidation(lid);
				});
			},
		});
	}
	} catch (err) {
		console.error('Lead Validation Dashboard load error:', err);
		$(wrapper).html('<div class="alert alert-danger m-4">Failed to load dashboard: ' + err.message + '</div>');
	}
};
