frappe.pages['finance-details'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'TFP Dashboard',
		single_column: true
		
	});
	frappe.breadcrumbs.add('TEAMPRO');
	const style = document.createElement('style');
	style.innerHTML = `
	.dashboard-wrapper {
    background-color: #f5f5f5;
    background-image: none; /* Remove existing background image if any */
}
		@keyframes blink-border {
			0% { border-color:rgb(151, 158, 153); }
			50% { border-color: transparent; }
			100% { border-color: rgb(151, 158, 153); }
		}
		.blink-border {
			animation: blink-border 2s infinite;
			border: 2px solid rgb(151, 158, 153);
		}
			@keyframes blink-order-booking {
		0%, 100% { border-color: #3fbab6; }
		50% { border-color: #70d3d1; }
	}

	@keyframes blink-turnover {
		0%, 100% { border-color: #4cb174; }
		50% { border-color: #6ccf94; }
	}

	@keyframes blink-collection {
		0%, 100% { border-color: #d4a017; }
		50% { border-color: #f4c037; }
	}

	@keyframes blink-payable {
		0%, 100% { border-color: #b22222; }
		50% { border-color: #dc3c3c; }
	}

	@keyframes blink-receivable {
		0%, 100% { border-color: #6a0dad; }
		50% { border-color: #8e3ddf; }
	}
		@keyframes blink-active {
		0%, 100% { border-color: #2e8b57; }
		50% { border-color: #2e8b57;}
	}

		.dashboard-cards {
			display: flex;
			gap: 30px;
			flex-wrap: wrap;
			justify-content: space-between;
		}
		.top-actions {
			position: absolute;
			right: 10px;
			top: 10px;
			display: flex;
			align-items: center;
			gap: 10px;
		}
			.dashboard-cards-finaince > div {
		flex: 1 1 200px;
		padding: 20px;
		border-radius: 12px;
		color: white;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		text-align: center;
		font-size: 18px;
		font-weight: bold;
		min-width: 200px;
	}

	.order-booking-card {
		background-color: #0a9396; /* Teal Blue - calm and modern */
	}

	.turnover-card {
		background-color: #2e8b57; /* Sea Green */
	}
	.collection-card {
		background-color: #b8860b; /* Dark Goldenrod */
	}
	.payable-card {
		background-color: #8b0000; /* Dark Red */
	}
	.receivable-card {
		background-color: #4b0082; /* Indigo - strong but professional */

	}
	.active-customer-card{
	background-color: #2e8b57; /* Sea Green */
	}
	.so-qty-card {
		background-color: #4682b4; /* Steel Blue */
	}

	.opportunity-card {
		background-color: #20b2aa; /* Dark Orange */
	}

	.total-qty-card {
		background-color: #b8860b; /* Slate Blue */
	}


		<style>
	
}


	`;
	document.head.appendChild(style);
	
	
{/* <div class="dashboard-wrapper" style="
			background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url('/files/48eecc75a6Daileemart We Serve 1.png');
		background-size: cover;
		background-position: center;
		min-height: 100vh;
		"></div>
		</div> */}
	$(wrapper).html(`
		
<div class="dashboard-wrapper">
			<div style="position: relative; padding: 10px; text-align: center;">
				<h2 style="font-weight: bold; margin: 0;">TFP Dashboard</h2>
				<div class="top-actions">
					<input type="date" id="tfp-from-date" class="form-control" style="width: 140px;">
					<input type="date" id="tfp-to-date" class="form-control" style="width: 140px;">
					<button id="apply-tfp-filter" class="btn btn-primary">Apply</button>
					<button id="refresh-dashboard" class="btn btn-primary">Refresh</button>
				</div>
				<div id="current-datetime" style="font-size: 16px; color: #666; margin-top: 5px;"></div>
			</div>

			<div class="active-customer-wrapper" style="padding: 20px;">
			<div class="dashboard-cards-finaince" style="display: flex; gap: 55px; flex-wrap: wrap; margin-bottom: 30px;">
				<div class="order-booking-card"></div>
				<div class="turnover-card"></div>
				<div class="collection-card"></div>
				<div class="payable-card"></div>
				<div class="receivable-card"></div>
			</div>
			<div style="display: flex; gap: 20px; margin-top: 20px; width: 100%;">
		<div id="tfp-receivable-table" style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; flex: 1; box-sizing: border-box; position: relative;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px 0;text-align:center">RECEIVABLE</h4>
		<div id="receivable-so-table-content" style="margin-top: 0px;"></div>
	</div>

	<div id="tfp-payable-table" style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; flex: 1; box-sizing: border-box; position: relative;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px 0;text-align:center">PAYABLE</h4>
		<div id="payable-so-table-content" style="margin-top: 0px;"></div>
	</div>

	</div>
	<br><br>
	
				<div class="dashboard-cards-finaince" style="display: flex; gap: 55px; margin-bottom: 30px;">
					<div class="active-customer-card"></div>
					<div class="so-qty-card"></div>
					<div class="opportunity-card"></div>
					<div class="total-qty-card"></div>
				</div>

				<!-- Wrapper to hold both tables side by side -->
	<div style="display: flex; gap: 20px; margin-top: 30px; width: 100%; flex-wrap: wrap;">

	<!-- Customer Last SO Details -->
	<div id="customer-so-table" style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 0px; flex: 1; box-sizing: border-box; position: relative;">
	
	<!-- Block 1: Active Customers -->

	<!-- Block 2: All Customers -->
	
	<div style="margin-bottom: 30px;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 10px; padding: 10px;text-align:center">ACTIVE CUSTOMER LAST SO DETAILS</h4>
		<div id="customer-active-so-table-content" style="margin-top: 20px;"></div>
	</div>

	</div>


	<!-- Opportunity Details -->
	<div id="opportunity-table" style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; flex: 1; box-sizing: border-box; position: relative;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">OPPORTUNITY DETAILS</h4>
		<div id="opportunity-table-content" style="margin-top: 10px;"></div>
	</div>

	</div>

	</div>
				<div id="tfp-so-table" style="max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-top: 30px; position: relative;text-align:center">
				<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">PACKING PLAN (SALES ORDER)</h4>
					<div style="position: absolute; top: 10px; right: 10px; z-index: 1;">
						<button id="download-dashboard" class="btn btn-secondary">Download</button>
					</div>
					<div id="tfp-so-table-content" style="margin-top:0px;"></div>
				</div>
			</div>
			<div id="tfp-so-table" style="max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-top: 30px; position: relative;text-align:center">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">SCHEDULED DETAILS (PINK SLIP)</h4>

			<div id="tfp-so-table-dn-content" style="margin-top: 0px;"></div>
			</div>
			<div style="display: flex; gap: 20px; margin-top: 30px; justify-content: center; flex-wrap: nowrap;">
	<!-- Packed Details -->
	<div class="table-card" style="max-height: 400px; overflow: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; width: 48%; position: relative; text-align: center;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;">PACKED DETAILS</h4>
		<div id="tfp-so-table-dn-packed-content" style="margin-top: 0px; overflow-x: auto; white-space: nowrap;"></div>
	</div>

	<!-- Dispatched Details -->
	<div class="table-card" style="max-height: 400px; overflow: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; width: 48%; position: relative; text-align: center;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;">DISPATCHED DETAILS</h4>
		<div id="tfp-so-table-dn-dispatched-content" style="margin-top: 0px; overflow-x: auto; white-space: nowrap;"></div>
	</div>
</div>



			<div style="display: flex; gap: 20px; margin-top: 30px; flex-wrap: wrap;">
		<div id="tfp-stock-table" style="flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">STORES - TFP (PRODUCT)</h4>
			<div id="tfp-stock-table-content" style="margin-top: 20px;"></div>
		</div>
		<div id="tfp-stock-table-second" style="flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;">
						<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">STORES - TFP (PACKING MATERIAL)</h4>
			<div id="tfp-stock-table-content-packing" style="margin-top: 20px;"></div>
		</div>
		
	</div>
	<div style="display: flex; gap: 20px; margin-top: 30px; flex-wrap: wrap;">
		<div id="second-stock-table" style="flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">VM PRECISION -TFP</h4>

			<div id="second-stock-table-content" style="margin-top: 20px;"></div>
		</div>
		<div id="second-stock-table-vm" style="flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;">
			<div id="variation-content" style="margin-top: 20px;"></div>
		
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
		const path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_plan_excel";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});

	// Apply filter
	$(wrapper).on('click', '#apply-tfp-filter', function() {
		const from_date = $('#tfp-from-date').val();
		const to_date = $('#tfp-to-date').val();
		loadOrderBooking(from_date, to_date);
		loadturnover(from_date, to_date);
		loadtcollection(from_date, to_date);
		// loadpayable(from_date, to_date);
		// loadreceivable(from_date, to_date);
		// loadreceivabletable(from_date, to_date);
		loadpayabletable(from_date, to_date);
		loadtotalsoqty(from_date, to_date);
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
// function loadpayable(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_payable",
			// args: { from_date, to_date },
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
	// }
	// function loadreceivable(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_receivable",
			// args: { from_date, to_date },
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
	// }
	// $('#receivable-so-table-content').html(`<div style="padding: 10px;text-align:center">Loading Receivable details...</div>`);
	// function loadreceivabletable(from_date = null, to_date = null) {
		frappe.call({
		method: 'teampro.teampro.page.finance_details.tfp_dashboard.tfp_receivable_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#receivable-so-table-content').html(r.message);
			}
			else {
				$('#receivable-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	// }
	// $('#payable-so-table-content').html(`<div style="padding: 10px;text-align:center">Loading Payable details...</div>`);
	// function loadpayabletable(from_date = null, to_date = null) {
		frappe.call({
		method: 'teampro.teampro.page.finance_details.tfp_dashboard.tfp_payable_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#payable-so-table-content').html(r.message);
			}
			else {
				$('#payable-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	// }
	function loadtotalsoqty(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_so_qty",
			args: { from_date, to_date },
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
	}
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
	
	$('#customer-active-so-table-content').html(`<div style="padding: 10px;text-align:center">Loading customer SO details...</div>`);

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_customer_last_so_details_active",
		callback: function(r) {
			if (r.message) {
				$('#customer-active-so-table-content').html(r.message);
			} else {
				$('#customer-active-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	// Load Customer SO Table
	// Show loading message before the call
	$('#customer-so-table-content').html(`<div style="padding: 10px;text-align:center">Loading customer SO details...</div>`);

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_customer_last_so_details",
		callback: function(r) {
			if (r.message) {
				$('#customer-so-table-content').html(r.message);
			} else {
				$('#customer-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	

	// frappe.call({
	// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_customer_last_so_details",
	// 	callback: function(r) {
			// const today = new Date();
			// const rows = (r.message || []).map(row => {
			// 	const last_so_date = new Date(row.last_so_on);
			// 	const diff_days = Math.floor((today - last_so_date) / (1000 * 60 * 60 * 24));
			// 	return `
			// 		<tr>
			// 			<td>${row.customer_name}</td>
			// 			<td style="color: ${diff_days > 15 ? 'red' : 'inherit'};">${frappe.datetime.str_to_user(row.last_so_on)}</td>
			// 			<td style="text-align: center;">${row.last_so_qty}</td>
			// 		</tr>`;
			// }).join('');

			// $(wrapper).find('.customer-so-body').html(rows || `<tr><td colspan="3">No data found</td></tr>`);
			
	// 	}
	// });
// 	frappe.call({
// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.opportunity_details",
// 	callback: function(r) {
// 		const rows = (r.message || []).map(row => {
// 			const expectedWeek = row.expected_closing
// 				? moment(row.expected_closing).isoWeek()
// 				: '-';
// 			return `
// 				<tr>
// 					<td>${row.opportunity_from || ''}</td>
// 					<td>${row.organization_name || ''}</td>
// 					<td style="text-align: right;">${format_currency(row.opportunity_amount || 0)}</td>
// 					<td style="text-align: center;">${expectedWeek}</td>
// 					<td style="text-align: center;">${row.custom_expected_quantity || ''}</td>
// 					<td>${row.remark || ''}</td>
// 				</tr>
// 			`;
// 		}).join('');
		
// 		$(wrapper).find('.opportunity-body').html(rows || `<tr><td colspan="6">No data found</td></tr>`);

// 	}
// });
$('#opportunity-table-content').html(`<div style="padding: 10px;text-align:center">Loading Opportuntiy details...</div>`);

frappe.call({
	method: "teampro.teampro.page.finance_details.tfp_dashboard.opportunity_details",
	callback: function(r) {
		if (r.message) {
			$('#opportunity-table-content').html(r.message);
		} else {
			$('#opportunity-table-content').html(`<p>No data found.</p>`);
		}
	}
});


	// loadreceivabletable();
	// loadpayabletable();
	// Load TFP Plan Table
	function packing_plan_so() {
		frappe.call({
			//  method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_plan_update",
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_plan_update_new",
			callback:function(r) {
				if (r.message) {
				$('#tfp-so-table-content').html(r.message || '<p>No data</p>')
				}
			}
		});
	}
	function scheduled_details_pink_slip() {
		frappe.call({
		// method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_schedule_opertaions",
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_schedule_opertaions_new",
		callback: function(r) {
			if (r.message) {
				let wrapper = document.getElementById("tfp-so-table-dn-content");
            wrapper.innerHTML = r.message;

            // Bind the toggle button events after injecting the HTML
            wrapper.querySelectorAll(".toggle-btn").forEach(btn => {
                btn.addEventListener("click", function () {
                    const dos = this.dataset.dos;
                    const rows = wrapper.querySelectorAll(".dos-" + dos);
                    
                    if (!rows.length) return; // 🛡️ Guard: no matching rows, skip

                    const isVisible = rows[0].style.display === "table-row";
                    rows.forEach(row => row.style.display = isVisible ? "none" : "table-row");
                    this.textContent = isVisible ? "+" : "-";
                });
            });
				// $('#tfp-so-table-dn-content').html(r.message || '<p style="color:#888; font-style: italic;">Nothing to show</p>');
			}
		}
	});
	}
	packing_plan_so();
	scheduled_details_pink_slip();
	
	// frappe.call({
	// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_schedule",
	// 	callback: function(r) {
	// 		if (r.message) {
	// 			$('#tfp-so-table-dn-content').html(r.message || '<p style="color:#888; font-style: italic;">Nothing to show</p>');
	// 		}
	// 	}
	// });
	function packed_details() {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_packed_dn_summary_html",
			callback: function(r) {
				if (r.message) {
					$('#tfp-so-table-dn-packed-content').html(r.message || '<p style="color:#888; font-style: italic;">Nothing to show</p>');
				}
			}
		});
	}
	function dispatched_details() {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_packed_dn_summary_dispatched_html",
			callback: function(r) {
				if (r.message) {
					$('#tfp-so-table-dn-dispatched-content').html(r.message || '<p style="color:#888; font-style: italic;">Nothing to show</p>');
				}
			}
		});
	}

	packed_details();
	dispatched_details();

	setInterval(() => {
		packing_plan_so();
		scheduled_details_pink_slip();
		packed_details();
		dispatched_details();
	}, 180000);

	$('#tfp-stock-table-content').html(`<div style="padding: 10px;text-align:center">Loading...</div>`);
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_stock_html",
		callback: function(r) {
			if (r.message) {
				$('#tfp-stock-table-content').html(r.message);
			}
			else {
			$('#tfp-stock-table-content').html(`<p>No data found.</p>`);
		}
		}
	});
	$('#second-stock-table-content').html(`<div style="padding: 10px;text-align:center">Loading...</div>`);
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_vm_stock_html",
		callback: function(r) {
			if (r.message) {
				$('#second-stock-table-content').html(r.message);
			}
			else {
			$('#second-stock-table-content').html(`<p>No data found.</p>`);
		}
		}
	});
	$('#tfp-stock-table-content-packing').html(`<div style="padding: 10px;text-align:center">Loading...</div>`);
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_stores_product",
		callback: function(r) {
			if (r.message) {
				$('#tfp-stock-table-content-packing').html(r.message);
			}
			else {
			$('#tfp-stock-table-content-packing').html(`<p>No data found.</p>`);
		}
		}
	});
	// $('#tfp-stock-table-content-packing1').html(`<div style="padding: 10px;text-align:center">Loading...</div>`);
	// frappe.call({
	// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_vm",
	// 	callback: function(r) {
	// 		if (r.message) {
	// 			$('#tfp-stock-table-content-packing1').html(r.message);
	// 		}
	// 		else {
	// 		$('#tfp-stock-table-content-packing1').html(`<p>No data found.</p>`);
	// 	}
	// 	}
	// });
frappe.call({
    method: "teampro.custom.get_physical_vs_erp_stock_data",
     callback: function(r) {
        const response = r.message;

        if (!response || !response.data || response.data.length === 0) {
            document.getElementById("variation-content").innerHTML = "<p>No data available.</p>";
            return;
        }

        const stockDate = response.date;
        const data = response.data;

       let tableHTML = `
    <div style="margin-bottom: 10px; font-weight: bold; text-align:center">
        LAST STOCK COUNTING DATE: <span style="color: #002060;">${frappe.datetime.str_to_user(stockDate)}</span>
    </div>
    <div style="max-height: 400px; overflow-y: auto;">
        <table style="width: 127%; border-collapse: collapse; text-align: center;">
            <thead style="background-color: #002060; color: white;">
                <tr>
                    <th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">S.No</th>
                    <th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Item</th>
                    <th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Item Name</th>
                    <th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Stock Qty</th>
                    <th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Physical Qty</th>
                    <th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Difference</th>
                    <th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Status</th>
                </tr>
            </thead>
            <tbody>
`;


        data.forEach((row, index) => {
            const statusColor = row.status === "Match" ? "green" : "red";
            tableHTML += `
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc;text-align:left">${index + 1}</td>
                    <td style="padding: 8px; border: 1px solid #ccc;;text-align:left">${row.item}</td>
                    <td style="padding: 8px; border: 1px solid #ccc;;text-align:left">${row.item_name}</td>
                    <td style="padding: 8px; border: 1px solid #ccc;;text-align:right">${Number(row.stock_qty).toFixed(2)}</td>
                    <td style="padding: 8px; border: 1px solid #ccc;;text-align:right">${Number(row.physical_qty).toFixed(2)}</td>
                    <td style="padding: 8px; border: 1px solid #ccc;;text-align:right">${Number(row.difference).toFixed(2)}</td>
                    <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; color: ${statusColor};">
                        ${row.status}
                    </td>
                </tr>
            `;
        });

        tableHTML += `</tbody></table>`;
        document.getElementById("variation-content").innerHTML = tableHTML;
    }
});

	
};

