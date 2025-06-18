frappe.pages['tfp-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});
frappe.breadcrumbs.add('TEAMPRO');

	const style = document.createElement('style');
	style.innerHTML = `
		@keyframes blink-border {
			0% { border-color:rgb(151, 158, 153); }
			50% { border-color: transparent; }
			100% { border-color: rgb(151, 158, 153); }
		}
		.blink-border {
			animation: blink-border 2s infinite;
			border: 2px solid rgb(151, 158, 153);
		}
		.dashboard-cards {
			display: flex;
			gap: 20px;
			flex-wrap: wrap;
		}
		.top-actions {
			position: absolute;
			right: 10px;
			top: 10px;
			display: flex;
			align-items: center;
			gap: 10px;
		}
			.card h3, .card h5 {
    font-weight: 600;
  }

  .table thead th {
    background-color: #0d6efd;
    color: white;
  }

  .sticky-top {
    position: sticky;
    top: 0;
    z-index: 1020;
  }

  .shadow-sm {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  }
	`;
	document.head.appendChild(style);
$(wrapper).html(`
  <style>
    .card:hover {
      transform: scale(1.02);
      transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
      cursor: pointer;
    }
    .sticky-top {
      position: sticky;
      top: 0;
      z-index: 10;
    }
  </style>

  <div class="container-fluid mt-3">
    <!-- Page Title and Actions -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="fw-bold">TFP Dashboard</h2>
      <div class="d-flex gap-2">
        <input type="date" id="tfp-from-date" class="form-control form-control-sm" style="width: 140px;">
        <input type="date" id="tfp-to-date" class="form-control form-control-sm" style="width: 140px;">
        <button id="apply-tfp-filter" class="btn btn-sm btn-primary">Apply</button>
        <button id="refresh-dashboard" class="btn btn-sm btn-outline-primary">Refresh</button>
      </div>
    </div>

    <div id="current-datetime" class="text-muted mb-4" style="font-size: 14px;"></div>

    <!-- First Card Row -->
    <div class="row g-3 mb-4">
  <div class="col">
    <div class="order-booking-card"></div>
  </div>
  <div class="col">
    <div class="turnover-card"></div>
  </div>
  <div class="col">
    <div class="collection-card"></div>
  </div>
  <div class="col">
    <div class="payable-card"></div>
  </div>
  <div class="col">
    <div class="receivable-card"></div>
  </div>
</div>


    <!-- Receivable and Payable Tables -->
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-warning text-white">Receivable</div>
          <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
            <table class="table table-sm table-hover mb-0">
              
              <tbody id="receivable-so-table-content"><tr><td colspan="2">Loading...</td></tr></tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-warning text-white">Payable</div>
          <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
            <table class="table table-sm table-hover mb-0">
              
              <tbody id="payable-so-table-content"><tr><td colspan="2">Loading...</td></tr></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Second Card Row -->
    <div class="row g-3 mb-4">
  <div class="col">
    <div class="active-customer-card"></div>
  </div>
  <div class="col">
    <div class="so-qty-card"></div>
  </div>
  <div class="col">
    <div class="opportunity-card"></div>
  </div>
  <div class="col">
    <div class="total-qty-card"></div>
  </div>
  <div class="col">
    <div class="tfp-sales-value-card"></div>
  </div>
</div>


    <!-- SO & Opportunity Tables -->
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-info text-white">Customer Last SO Details</div>
          <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
            <table class="table table-sm table-hover mb-0">
              <thead class="table-info sticky-top">
                <tr>
                  <th>Customer Name</th>
                  <th>Last SO On</th>
                  <th>Last SO Quantity</th>
                </tr>
              </thead>
              <tbody class="customer-so-body">
                <tr><td colspan="3">Loading...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-warning text-white">Opportunity Details</div>
          <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
            <table class="table table-sm table-hover mb-0">
              <thead class="table-warning sticky-top">
                <tr>
                  <th>Opportunity From</th>
                  <th>Organization Name</th>
                  <th>Expected Value</th>
                  <th>Expected Week</th>
                  <th>Expected Quantity</th>
                  <th>Cr. Remark</th>
                </tr>
              </thead>
              <tbody class="opportunity-body">
                <tr><td colspan="6">Loading...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- TFP Production Plan -->
    <!-- TFP Production Plan -->
<div class="card shadow-sm mb-4">
  <div class="card-header d-flex justify-content-between align-items-center">
    <div class="fw-bold">TFP Production Plan</div>
    <button id="download-dashboard" class="btn btn-sm btn-secondary">Download</button>
  </div>
  <div class="card-body p-0" style="max-height: 400px; overflow-y: auto; overflow-x: auto;">
    <table class="table table-sm table-hover mb-0" style="width: 200%;">
      <thead class="table-light sticky-top">
      <tbody id="tfp-so-table-content"><tr><td colspan="3">Loading...</td></tr></tbody>
    </table>
  </div>
</div>

    <!-- Stock Tables -->
    <div class="row g-3">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-success text-white">Stores – TFP</div>
          <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
            <table class="table table-sm table-hover mb-0">
              
              <tbody id="tfp-stock-table-content"><tr><td colspan="2">Loading...</td></tr></tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-secondary text-white">VM Precision – TFP</div>
          <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
            <table class="table table-sm table-hover mb-0">
              
              <tbody id="second-stock-table-content"><tr><td colspan="2">Loading...</td></tr></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
	<div id="second-stock-table-vms" style="flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;">
			<div id="tfp-stock-table-content-packing1" style="margin-top: 20px;"></div>
		
		</div>
  </div>
`);



	// DateTime
	function updateDateTime() {
		const now = new Date();
		const dateStr = now.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
		const timeStr = now.toLocaleTimeString();
		document.getElementById('current-datetime').innerHTML = `${dateStr} | ${timeStr}`;
	}
	updateDateTime();
	setInterval(updateDateTime, 1000);

	// Refresh
	$(wrapper).on('click', '#refresh-dashboard', () => location.reload());

	// Download
	$(wrapper).on('click', '#download-dashboard', function () {
		const path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_production_plan_excel";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});

	// Apply filter
	$(wrapper).on('click', '#apply-tfp-filter', function() {
		const from_date = $('#tfp-from-date').val();
		const to_date = $('#tfp-to-date').val();
		loadOrderBooking(from_date, to_date);
		loadturnover(from_date, to_date);
		loadtcollection(from_date, to_date);
		loadpayable(from_date, to_date);
		loadreceivable(from_date, to_date);
		loadreceivabletable(from_date, to_date);
		loadpayabletable(from_date, to_date);
	});


	// Load Dashboard Cards
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_active_customers_count",
		callback: function(r) {
			const count = r.message || 0;
			$(wrapper).find('.active-customer-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Active Customers</h3>
					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${count}</div>
				</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_order_booking",
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
			$(wrapper).find('.order-booking-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Order Booking</h3>
					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_turnover",
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
				// const count = r.message || 0;
			$(wrapper).find('.turnover-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Turnover</h3>
					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_collection_value",
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
				// const count = r.message || 0;
			$(wrapper).find('.collection-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Collection</h3>
					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_payable",
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
				// const count = r.message || 0;
			$(wrapper).find('.payable-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Payable</h3>
					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_receivable",
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
				// const count = r.message || 0;
			$(wrapper).find('.receivable-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Receivable</h3>
					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
	function loadOrderBooking(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_order_booking",
			args: { from_date, to_date },
			callback: function(r) {
				const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
				$(wrapper).find('.order-booking-card').html(`
					<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Order Booking</h3>
						<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
	function loadturnover(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_turnover",
			args: { from_date, to_date },
			callback: function(r) {
				const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
				$(wrapper).find('.turnover-card').html(`
					<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Turnover</h3>
						<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
	function loadtcollection(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_collection_value",
			args: { from_date, to_date },
			callback: function(r) {
				const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
				$(wrapper).find('.collection-card').html(`
					<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Collection</h3>
						<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
function loadpayable(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_payable",
			args: { from_date, to_date },
			callback: function(r) {
				const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
				$(wrapper).find('.payable-card').html(`
					<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Payable</h3>
						<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
	function loadreceivable(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_receivable",
			args: { from_date, to_date },
			callback: function(r) {
				const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
				$(wrapper).find('.receivable-card').html(`
					<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Receivable</h3>
						<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
	function loadreceivabletable(from_date = null, to_date = null) {
		frappe.call({
		method: 'teampro.teampro.page.finance_details.tfp_dashboard.tfp_receivable_table',
		args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#receivable-so-table-content').html(r.message);
			}
		}
	});
	}
	function loadpayabletable(from_date = null, to_date = null) {
		frappe.call({
		method: 'teampro.teampro.page.finance_details.tfp_dashboard.tfp_payable_table',
		args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#payable-so-table-content').html(r.message);
			}
		}
	});
	}

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_so_qty",
		callback: function(r) {
			const qty = r.message || 0;
			$(wrapper).find('.so-qty-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Total SO Qty</h3>
					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${qty}</div>
				</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.total_exp_value",
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
			// const value = r.message || 0;
			$(wrapper).find('.opportunity-card').html(`
				<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
			<h3 style="margin: 0;text-align:center">Total Expected Value</h3>
			<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
		</div>
			`);
		}
	});

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.total_opp_qty",
		callback: function(r) {
			
			const value = r.message || 0;
			$(wrapper).find('.total-qty-card').html(`
					<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
			<h3 style="margin: 0;text-align:center">Total Qty</h3>
			<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${value}</div>
		</div>
			`);
		}
	});
	
	// Load Customer SO Table
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_customer_last_so_details",
		callback: function(r) {
			const today = new Date();
			const rows = (r.message || []).map(row => {
				const last_so_date = new Date(row.last_so_on);
				const diff_days = Math.floor((today - last_so_date) / (1000 * 60 * 60 * 24));
				return `
					<tr>
						<td>${row.customer_name}</td>
						<td style="color: ${diff_days > 15 ? 'red' : 'inherit'};">${frappe.datetime.str_to_user(row.last_so_on)}</td>
						<td style="text-align: center;">${row.last_so_qty}</td>
					</tr>`;
			}).join('');

			$(wrapper).find('.customer-so-body').html(rows || `<tr><td colspan="3">No data found</td></tr>`);
		}
	});
	$('#tfp-stock-table-content-packing1').html(`<div style="padding: 10px;text-align:center">Loading...</div>`);
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_plan_update_stock",
		callback: function(r) {
			if (r.message) {
				$('#tfp-stock-table-content-packing1').html(r.message);
			}
			else {
			$('#tfp-stock-table-content-packing1').html(`<p>No data found.</p>`);
		}
		}
	});
	frappe.call({
	method: "teampro.teampro.page.finance_details.tfp_dashboard.opportunity_details",
	callback: function(r) {
		const rows = (r.message || []).map(row => {
			const expectedWeek = row.expected_closing
				? moment(row.expected_closing).isoWeek()
				: '-';
			return `
				<tr>
					<td>${row.opportunity_from || ''}</td>
					<td>${row.organization_name || ''}</td>
					<td style="text-align: right;">${format_currency(row.opportunity_amount || 0)}</td>
					<td style="text-align: center;">${expectedWeek}</td>
					<td style="text-align: center;">${row.custom_expected_quantity || ''}</td>
					<td>${row.remark || ''}</td>
				</tr>
			`;
		}).join('');
		
		$(wrapper).find('.opportunity-body').html(rows || `<tr><td colspan="6">No data found</td></tr>`);

	}
});

	loadreceivabletable();
	loadpayabletable();
	// Load TFP Plan Table
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html",
		callback: function(r) {
			if (r.message) {
				$('#tfp-so-table-content').html(r.message);
			}
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_stock_html",
		callback: function(r) {
			if (r.message) {
				$('#tfp-stock-table-content').html(r.message);
			}
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_vm_stock_html",
		callback: function(r) {
			if (r.message) {
				$('#second-stock-table-content').html(r.message);
			}
		}
	});
	
};

