frappe.pages['finance-details'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'TFP Dashboard',
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
			gap: 10px;
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
	padding: 15px;
	border-radius: 12px;
	color: white;
	text-align: center;
	font-size: 18px;
	font-weight: bold;
	min-width: 150px;
	flex-shrink: 0;
}

	.order-booking-card {
		background-color: #0a9396; /* Teal Blue - calm and modern */
	}
	.todeliverbill-card{
	background-color: #4169e1;
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
	.dashboard-wrapper{
		display:flex;
		flex-direction:column;
		gap:20px;
	}

		.dashboard-cards-finaince{
    display:flex;
    flex-wrap:wrap;
    gap:20px;
    padding:15px;
    border:1px solid #ddd;
    border-radius:10px;
    background:#f5f5f5;
	display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:20px;
}
	.dashboard-cards-finaince > div{
    width:100%;
}

.dashboard-card{
    position:relative;
    background:#fff;
    border-radius:12px;
    overflow:hidden;   /* IMPORTANT */
}

.card-top-line{
    height:4px;
    width:100%;
}

.card-body{
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    height:calc(100% - 4px);
}

.card-icon{
    font-size:24px;
    margin-bottom:8px;
}

.card-title{
    font-size:15px;
    font-weight:700;
	color:black;
}

.card-value{
    font-size:26px;
    font-weight:bold;
    color:green;
    margin-top:10px;
}

/* Combined Card */


.summary-card{
    width:100%;
}

.summary-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}

.summary-item{
    position:relative;
    padding:15px;
    background:#fff;
    border-radius:10px;
    text-align:center;
    border:1px solid #eee;
}

.summary-line{
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:4px;
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
				<h2 style="font-weight: bold; margin: 0;">FOOD PRODUCTS</h2>
				<div class="top-actions">
					<input type="date" id="tfp-from-date" class="form-control" style="width: 140px;">
					<input type="date" id="tfp-to-date" class="form-control" style="width: 140px;">
					<button id="apply-tfp-filter" class="btn btn-primary">Apply</button>
					<button id="refresh-dashboard" class="btn btn-primary">Refresh</button>
				</div>
				<div id="current-datetime" style="font-size: 16px; color: #666; margin-top: 5px;"></div>
			</div>
	<br><br>	
	<div class="dashboard-wrapper" >
		<div class="dashboard-cards-finaince" style="margin-left:20px; margin-right:20px;" >

			<div class="active-customer-card" style="
				margin-left:10px;
				flex:0 0 auto;
			"></div>

			<div class="so-qty-card" style="
				flex:0 0 auto;
			"></div>

			<div class="tot-stock-qty-card" style="
				flex:0 0 auto;
			"></div>

			<div class="opportunity-card" style="
				flex:0 0 auto;
			"></div>

			<div class="opportunity-count-card" style="
				flex:0 0 auto;
			"></div>

			<div class="delivery-summary-card" style="
				flex:0 0 auto;
			"></div>

			<div class="total-customer-card" style="
				margin-right:50px;
				flex:0 0 auto;
			"></div>
		</div>
		
	<div style="display: flex; gap: 20px; margin-top: 30px; width: 100%; flex-wrap: wrap;">

	<!-- Customer Last SO Details -->
	<div id="customer-so-table" style="background-color: #f5f5f5;max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding:10px; flex: 1; box-sizing: border-box; position: relative;margin-left: 15px;">
	
	<div style="margin-bottom: 30px;margin-left: 15px;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">ACTIVE CUSTOMER LAST SO DETAILS</h4>
		<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download7-dashboard" class="btn btn-secondary">Download</button>
					</div>
		<div id="customer-active-so-table-content" style="margin-top: 10px;"></div>
	</div>

	</div>


	<!-- Opportunity Details -->
	<div id="opportunity-table" style="background-color: #f5f5f5;max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; flex: 1; box-sizing: border-box; position: relative;margin-right: 15px;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">OPPORTUNITY DETAILS</h4>
		<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download6-dashboard" class="btn btn-secondary">Download</button>
					</div>
		<div id="opportunity-table-content" style="margin-top: 10px;"></div>
	</div>

	</div>

	</div>
				<div id="tfp-so-table" style="background-color: #f5f5f5;max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-top: 30px; position: relative;text-align:center;margin-left: 15px;margin-right: 15px;">
				<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">PACKING PLAN (SALES ORDER)</h4>
					<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download-dashboard" class="btn btn-secondary">Download</button>
					</div>
					<div id="tfp-so-table-content" style="margin-top:0px;"></div>
				</div>
			</div>
			<div id="tfp-so-table" style="background-color: #f5f5f5;max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-top: 30px; position: relative;text-align:center;margin-left: 15px;margin-right: 15px;">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">SCHEDULED DETAILS (PINK SLIP)</h4>
			<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download11-dashboard" class="btn btn-secondary">Download</button>
					</div>
			<div id="tfp-so-table-dn-content" style="margin-top: 0px;"></div>
			</div>
			<div style="display: flex; gap: 20px; margin-top: 30px; justify-content: center; flex-wrap: nowrap;">
	<!-- Packed Details -->
	<div class="table-card" style="background-color: #f5f5f5;max-height: 400px; overflow: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; width: 48%; position: relative; text-align: center;margin-left: 15px;margin-right: 15px;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;">PACKED DETAILS</h4>
		<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download5-dashboard" class="btn btn-secondary">Download</button>
					</div>
		<div id="tfp-so-table-dn-packed-content" style="margin-top: 0px; overflow-x: auto; white-space: nowrap;"></div>
	</div>

	<!-- Dispatched Details -->
	<div class="table-card" style="background-color: #f5f5f5;max-height: 400px; overflow: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; width: 48%; position: relative; text-align: center;margin-left: 15px;margin-right: 15px;">
		<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;">DISPATCHED DETAILS</h4>
			<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download4-dashboard" class="btn btn-secondary">Download</button>
					</div>
		<div id="tfp-so-table-dn-dispatched-content" style="margin-top: 0px; overflow-x: auto; white-space: nowrap;"></div>
	</div>
</div>



			<div style="display: flex; gap: 20px; margin-top: 30px; flex-wrap: wrap;">
		<div id="tfp-stock-table" style="background-color: #f5f5f5;flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;margin-left: 15px;">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">STORES - TFP (PRODUCT)</h4>
			<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download3-dashboard" class="btn btn-secondary">Download</button>
					</div>
			<div id="tfp-stock-table-content" style="margin-top: 20px;"></div>
		</div>
		<div id="tfp-stock-table-second" style="background-color: #f5f5f5;flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;margin-right: 15px;">
						<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">STORES - TFP (PACKING MATERIAL)</h4>
						<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download2-dashboard" class="btn btn-secondary">Download</button>
					</div>	
						<div id="tfp-stock-table-content-packing" style="margin-top: 20px;"></div>
		</div>
		
	</div>
	<div style="display: flex; gap: 20px; margin-top: 30px; flex-wrap: wrap;">
		<div id="second-stock-table" style="background-color: #f5f5f5;flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;margin-left: 15px;">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">LSVM STOCK STATUS</h4>
			<div style="position: absolute; top: 0px; right: 10px; z-index: 1;">
						<button id="download1-dashboard" class="btn btn-secondary">Download</button>
					</div>
			<div id="second-stock-table-content" style="margin-top: 20px;"></div>
		</div>
		<div id="second-stock-table-vm" style="background-color: #f5f5f5;flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;margin-right: 15px;">
			<div id="variation-content" style="margin-top: 20px;"></div>
		
		</div>
		
		</div>
		<div id="second-stock-table-vms" style="flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;margin-right: 15px;">
			<div id="tfp-stock-table-content-packing1" style="margin-top: 20px;"></div>
		
		</div>
		
		<div style="display: flex; gap: 20px; margin-top: 30px; flex-wrap: wrap;">
		<div id="second-stock-table" style="background-color: #f5f5f5;flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;margin-left: 15px;">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">RETAIL SHOP AVAILABILITY</h4>
			
			<div id="retail-shop-availability" style="margin-top: 20px;"></div>
		</div>
		<div id="retail-payment" style="background-color: #f5f5f5;flex: 1; min-width: 400px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;margin-right: 15px;">
			<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">RETAIL SHOP PAYMENT OUTSTANDING REPORT</h4>
			<div id="retail-payment-content" style="margin-top: 20px;"></div>
		
		</div>
		
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
		// const path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_plan_excel";
		const path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_plan_excel_update";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});

	$(wrapper).on('click', '#download1-dashboard', function () {
		// const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_vm_precision_tfp";
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_vm_precision_tfp_data";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});

	$(wrapper).on('click', '#download2-dashboard', function () { 
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_stores_tfp";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download3-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_stores_tfp_product";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download4-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_dispatched_details";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download5-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_packed_details";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download6-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_opportunity_details";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download7-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_active_cutomer_last_so_details";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download8-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_receivable_table";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download9-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_tobill_table";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download10-dashboard', function () {
		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_payable_table1";
		window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	});
	$(wrapper).on('click', '#download11-dashboard', function () {
		// const path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_plan_excel";
		const path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_scheduled_excel_update";
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
	frappe.call({
	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_delivery_status_summary",

	callback: function(r) {

		let d = r.message;

		// let card = `

		// 	<div class="dashboard-card" style="
		// 		width:250px;
		// 		padding:5px;
		// 		border-radius:10px;
		// 		background:white;
		// 		box-shadow:0 2px 6px rgba(0,0,0,0.08);
		// 	">
		// 	<div class="card-top-line" style="background:#292cc9"></div>
		// 		<div style="
		// 			display:grid;
		// 			grid-template-columns:1fr 1fr;
		// 			border:1px solid #e5e7eb;
		// 			border-radius:6px;
		// 			overflow:hidden;
		// 		">

		// 			<!-- PACKING -->
		// 			<div style="
		// 				padding:7px;
		// 				text-align:center;
		// 				border-right:1px solid #e5e7eb;
		// 				border-bottom:1px solid #e5e7eb;
		// 			">

		// 				<div style="
		// 					font-size:11px;
		// 					font-weight:700;
		// 					color:#2196f3;
		// 					margin-top:3px;
		// 				">
		// 					📦Packing
		// 				</div>

		// 				<span style="background:#e3f2fd;color:#1565c0;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					${d.packing.count}
		// 				</span>
		// 				<span style="margin-left:4px;background:#fce4ec;color:#ad1457;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					Qty: ${d.packing.qty}
		// 				</span>


		// 			</div>

		// 			<!-- SCHEDULED -->
		// 			<div style="
		// 				padding:7px;
		// 				text-align:center;
		// 				border-bottom:1px solid #e5e7eb;
		// 			">

		// 				<div style="
		// 					font-size:11px;
		// 					font-weight:700;
		// 					color:#ff9800;
		// 					margin-top:3px;
		// 				">
		// 					📅Scheduled
		// 				</div>

		// 				<span style="background:#fff3e0;color:#ef6c00;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					${d.scheduled.count}
		// 				</span>
		// 				<span style="margin-left:4px;background:#ede7f6;color:#5e35b1;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					Qty: ${d.scheduled.qty}
		// 				</span>

		// 			</div>

		// 			<!-- PACKED -->
		// 			<div style="
		// 				padding:7px;
		// 				text-align:center;
		// 				border-right:1px solid #e5e7eb;
		// 			">

		// 				<div style="
		// 					font-size:11px;
		// 					font-weight:700;
		// 					color:#9c27b0;
		// 					margin-top:3px;
		// 				">
		// 					✅Packed
		// 				</div>

		// 				<span style="background:#e8f5e9;color:#2e7d32;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					${d.packed.count}
		// 				</span>
		// 				<span style="margin-left:4px;background:#f3e5f5;color:#6a1b9a;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					Qty: ${d.packed.qty}
		// 				</span>

		// 			</div>

		// 			<div style="
		// 				padding:7px;
		// 				text-align:center;
		// 			">
		// 				<div style="
		// 					font-size:11px;
		// 					font-weight:700;
		// 					color:#4caf50;
		// 					margin-top:3px;
		// 				">
		// 					🚚Dispatched
		// 				</div>

		// 				<span style="background:#e0f7fa;color:#00838f;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					${d.dispatched.count}
		// 				</span>
		// 				<span style="margin-left:4px;background:#f1f8e9;color:#558b2f;padding:2px 6px;border-radius:6px;font-size:11px;">
		// 					Qty: ${d.dispatched.qty}
		// 				</span>

		// 			</div>

		// 		</div>

		// 	</div>
		// `;
		let card = `
<div class="dashboard-card">

    <div class="card-top-line" style="background:#ff66a3"></div>

    <div class="card-body" style="padding:10px;">

        <div style="
            display:grid;
            grid-template-columns:repeat(2,1fr);
            border:1px solid #e5e7eb;
            border-radius:8px;
            overflow:hidden;
        ">

            <!-- Packing -->
            <div style="padding:12px;border-right:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">📦</div>
                <div class="card-title" style="color:#2196f3;">Packing</div>

                <div style="margin-top:8px;">
                    <span style="background:#e3f2fd;color:#1565c0;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.packing.count}
                    </span>
                </div>

                <div style="margin-top:6px;font-size:12px;color:#666;">
                    Qty : <b>${d.packing.qty}</b>
                </div>
            </div>

            <!-- Scheduled -->
            <div style="padding:12px;border-bottom:1px solid #e5e7eb;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">📅</div>
                <div class="card-title" style="color:#ff9800;">Scheduled</div>

                <div style="margin-top:8px;">
                    <span style="background:#fff3e0;color:#ef6c00;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.scheduled.count}
                    </span>
                </div>

                <div style="margin-top:6px;font-size:12px;color:#666;">
                    Qty : <b>${d.scheduled.qty}</b>
                </div>
            </div>

            <!-- Packed -->
            <div style="padding:12px;border-right:1px solid #e5e7eb;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">✅</div>
                <div class="card-title" style="color:#9c27b0;">Packed</div>

                <div style="margin-top:8px;">
                    <span style="background:#e8f5e9;color:#2e7d32;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.packed.count}
                    </span>
                </div>

                <div style="margin-top:6px;font-size:12px;color:#666;">
                    Qty : <b>${d.packed.qty}</b>
                </div>
            </div>

            <!-- Dispatched -->
            <div style="padding:12px;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">🚚</div>
                <div class="card-title" style="color:#4caf50;">Dispatched</div>

                <div style="margin-top:8px;">
                    <span style="background:#e0f7fa;color:#00838f;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.dispatched.count}
                    </span>
                </div>

                <div style="margin-top:6px;font-size:12px;color:#666;">
                    Qty : <b>${d.dispatched.qty}</b>
                </div>
            </div>

        </div>

    </div>

</div>
`;

		$(wrapper).find('.delivery-summary-card').html(card);

	}
});
	frappe.call({
	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_stock_qty_value",

	callback: function(r) {

		const stock_qty = r.message.total_stock_qty || 0;
		const stock_value = r.message.total_stock_value || 0;

		$(wrapper).find('.tot-stock-qty-card').html(`
		<div class="dashboard-card">
			<div class="card-top-line" style="background:#4b0082;"></div>

			<div class="card-body">
				<div class="card-icon">📦</div>

				<div class="card-title">
					Total Stock Qty
				</div>

				<div class="card-value">
					${stock_qty.toFixed(2)}
				</div>

				<div style="
					font-size:14px;
					margin-top:6px;
					color:#555;
					font-weight:600;
				">
					${format_currency(stock_value)}
				</div>
			</div>
		</div>
	`);
		}
	});

		// Load Dashboard Cards
		frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_active_customers_count",

		callback: function(r) {

			const count = r.message || 0;

			$(wrapper).find('.active-customer-card').html(`
				<div class="dashboard-card">
					<div class="card-top-line" style="background:#2e8b57"></div>

					<div class="card-body">
						<div class="card-icon">👥</div>
						<div class="card-title">Active Customers</div>
						<div class="card-value">${count}</div>
					</div>
				</div>
			`);
		}
});
	// frappe.call({
	// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_customer_detalils",
	// 	callback(r) {

	// 		let data = r.message;

	// 		let card = `
	// 			<div class="card blink-border" style="
	// 				width: 250px;
	// 				padding: 20px;
	// 				height: 190px;
	// 				border-radius: 8px;
	// 				background: white;
	// 				border: 2px solid #4b0082;
	// 				box-shadow: 0 4px 12px rgba(0,0,0,0.1);
	// 			">

	// 				<div style="
	// 					font-size:30px;
	// 					font-weight:bold;
	// 					color:#2490ef;
	// 					text-align:center;
	// 					line-height:1;
	// 				">
	// 					${data.overall_customer_count}
	// 				</div>

	// 				<div style="
	// 					font-size:15px;
	// 					font-weight:bold;
	// 					text-align:center;
	// 					margin-top:5px;
	// 					margin-bottom:12px;
	// 					color:#333;
	// 				">
	// 					Overall Customers
	// 				</div>

	// 				<div style="
	// 					display:flex;
	// 					justify-content:space-between;
	// 					gap:6px;
	// 					font-size:12px;
	// 				">

	// 					<div style="
	// 						flex:1;
	// 						padding:5px;
	// 						border-left:4px solid #0a9396;
	// 						background:#f7f7f7;
	// 						border-radius:4px;
	// 						text-align:center;
	// 						color:#444;
	// 					">
	// 						<div><b>Corporate</b></div>
	// 						<div>${data.total_corporate_customers}</div>
	// 					</div>

	// 					<div style="
	// 						flex:1;
	// 						padding:5px;
	// 						border-left:4px solid #20b2aa;
	// 						background:#f7f7f7;
	// 						border-radius:4px;
	// 						text-align:center;
	// 						color:#444;
	// 					">
	// 						<div><b>Retail</b></div>
	// 						<div>${data.total_retail_shops}</div>
	// 					</div>

	// 					<div style="
	// 						flex:1;
	// 						padding:5px;
	// 						border-left:4px solid #b8860b;
	// 						background:#f7f7f7;
	// 						border-radius:4px;
	// 						text-align:center;
	// 						color:#444;
	// 					">
	// 						<div><b>Vending</b></div>
	// 						<div>${data.total_vending_machines}</div>
	// 					</div>

	// 				</div>

	// 			</div>
	// 		`;
	// 		$(wrapper).find('.total-customer-card').html(card);
	// 	}
	// });
	frappe.call({
	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_customer_detalils",
	callback(r) {

		let d = r.message;

		// let card = `
		// 	<div  style="
		// 		width:200px;
		// 		padding:6px;
		// 		border-radius:10px;
		// 		background:white;
		// 		box-shadow:0 2px 6px rgba(0,0,0,0.08);
		// 	">

		// 		<div style="
		// 			display:grid;
		// 			grid-template-columns:1fr 1fr;
		// 			border:1px solid #e5e7eb;
		// 			border-radius:6px;
		// 			overflow:hidden;
		// 		">

		// 			<!-- CS -->
		// 			<div style="
		// 				padding:8px;
		// 				text-align:center;
		// 				border-right:1px solid #e5e7eb;
		// 				border-bottom:1px solid #e5e7eb;
		// 			">
		// 				<div style="font-size:11px;font-weight:700;color:#0a9396;">
		// 					👥 CS
		// 				</div>

		// 				<span style="
		// 					display:inline-block;
		// 					margin-top:6px;
		// 					padding:3px 8px;
		// 					border-radius:6px;
		// 					background:#fde2e4;
		// 					color:#d6336c;
		// 					font-size:11px;
		// 					font-weight:700;
		// 				">
		// 					${d.total_corporate_customers}
		// 				</span>
		// 			</div>

		// 			<!-- RS -->
		// 			<div style="
		// 				padding:8px;
		// 				text-align:center;
		// 				border-bottom:1px solid #e5e7eb;
		// 			">
		// 				<div style="font-size:11px;font-weight:700;color:#20b2aa;">
		// 					🏪 RS
		// 				</div>

		// 				<span style="
		// 					display:inline-block;
		// 					margin-top:6px;
		// 					padding:3px 8px;
		// 					border-radius:6px;
		// 					background:#e8f0fe;
		// 					color:#1a73e8;
		// 					font-size:11px;
		// 					font-weight:700;
		// 				">
		// 					${d.total_retail_shops}
		// 				</span>
		// 			</div>

		// 			<!-- LSVM -->
		// 			<div style="
		// 				padding:8px;
		// 				text-align:center;
		// 				border-right:1px solid #e5e7eb;
		// 			">
		// 				<div style="font-size:11px;font-weight:700;color:#b8860b;">
		// 					🤖 LSVM
		// 				</div>

		// 				<span style="
		// 					display:inline-block;
		// 					margin-top:6px;
		// 					padding:3px 8px;
		// 					border-radius:6px;
		// 					background:#e7f7ee;
		// 					color:#1b7f3a;
		// 					font-size:11px;
		// 					font-weight:700;
		// 				">
		// 					${d.total_vending_machines}
		// 				</span>
		// 			</div>

		// 			<!-- OVERALL -->
		// 			<div style="
		// 				padding:8px;
		// 				text-align:center;
		// 			">
		// 				<div style="font-size:11px;font-weight:700;color:#2490ef;">
		// 					📊 Overall
		// 				</div>

		// 				<span style="
		// 					display:inline-block;
		// 					margin-top:6px;
		// 					padding:3px 8px;
		// 					border-radius:6px;
		// 					background:#f1f1f1;
		// 					color:#333;
		// 					font-size:11px;
		// 					font-weight:700;
		// 				">
		// 					${d.overall_customer_count}
		// 				</span>
		// 			</div>

		// 		</div>
		// 	</div>
		// `;
		let card = `
<div class="dashboard-card">

    <div class="card-top-line" style="background:#ffd11a"></div>

    <div class="card-body" style="padding:10px;">

        <div style="
            display:grid;
            grid-template-columns:repeat(2,1fr);
            border:1px solid #e5e7eb;
            border-radius:8px;
            overflow:hidden;
        ">

            <!-- CS -->
            <div style="padding:12px;border-right:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">👥</div>
                <div class="card-title" style="color:#0a9396;">CS</div>

                <div style="margin-top:8px;">
                    <span style="background:#fde2e4;color:#d6336c;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.total_corporate_customers}
                    </span>
                </div>
            </div>

            <!-- RS -->
            <div style="padding:12px;border-bottom:1px solid #e5e7eb;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">🏪</div>
                <div class="card-title" style="color:#20b2aa;">RS</div>

                <div style="margin-top:8px;">
                    <span style="background:#e8f0fe;color:#1a73e8;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.total_retail_shops}
                    </span>
                </div>
            </div>

            <!-- LSVM -->
            <div style="padding:12px;border-right:1px solid #e5e7eb;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">🤖</div>
                <div class="card-title" style="color:#b8860b;">LSVM</div>

                <div style="margin-top:8px;">
                    <span style="background:#e7f7ee;color:#1b7f3a;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.total_vending_machines}
                    </span>
                </div>
            </div>

            <!-- Overall -->
            <div style="padding:12px;text-align:center;">
                <div class="card-icon" style="margin-bottom:4px;">📊</div>
                <div class="card-title" style="color:#2490ef;">Overall</div>

                <div style="margin-top:8px;">
                    <span style="background:#f1f1f1;color:#333;padding:4px 10px;border-radius:8px;font-weight:600;">
                        ${d.overall_customer_count}
                    </span>
                </div>
            </div>

        </div>

    </div>

</div>
`;

		$(wrapper).find('.total-customer-card').html(card);
	}
});
	frappe.call({
	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_opportunity_count",

	callback: function(r) {

		const count = r.message || 0;

		$(wrapper).find('.opportunity-count-card').html(`
    <div class="dashboard-card">
        <div class="card-top-line" style="background:#292cc9"></div>

        <div class="card-body">
            <div class="card-icon">🎯</div>
            <div class="card-title">OPP Count</div>
            <div class="card-value">${count}</div>
        </div>
    </div>
`);
	}
});
	frappe.call({
	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_order_booking",
	callback: function(r) {
		const value = r.message || 0;

        // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);

        const formattedTotal = parseFloat(value).toLocaleString('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0 
        });

        // const formattedAvg = parseFloat(avg).toLocaleString('en-IN', {
        //     style: 'currency',
        //     currency: 'INR',
        //     maximumFractionDigits: 0 
        // });
		let arrowSvg = `
<svg width="70" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;

		const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });


		// Inject HTML into wrapper
		$(wrapper).find('.order-booking-card').html(`
			<div class="card blink-border" style="width: 160px; padding: 15px; border-radius: 8px;">
				<h3 style="margin: 0; text-align:center; white-space:nowrap; font-size:17px;">Order Booking</h3>
				<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
				<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
		`);
		
	}
});

	
	frappe.call({
    method: "teampro.teampro.page.finance_details.tfp_dashboard.get_turnover",
    callback: function(r) {
        const value = r.message || 0;

        // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);

        const formattedTotal = parseFloat(value).toLocaleString('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0 
        });
		let arrowSvg = `
<svg width="70" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;

        // const formattedAvg = parseFloat(avg).toLocaleString('en-IN', {
        //     style: 'currency',
        //     currency: 'INR',
        //     maximumFractionDigits: 0 
        // });
		const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });


        // $(wrapper).find('.turnover-card').html(`
        //     <div class="card blink-border" style="width: 160px; padding: 15px; border-radius: 8px;">
        //         <h3 style="margin: 0;text-align:center;font-size:17px;">Turnover</h3>
        //         <div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
        //         <div style="font-size: 14px; text-align: center; margin-top: 5px;">
        //             <span style="color:red; font-weight:bold;font-size:13px;">[${formattedAvg}]</span>
        //             <span style="display:inline-block; vertical-align:middle;">${arrowSvg}</span>
        //         </div>
        //     </div>
        // `);
		$(wrapper).find('.turnover-card').html(`
            <div class="card blink-border" style="width: 160px; padding: 15px; border-radius: 8px;">
                <h3 style="margin: 0;text-align:center;font-size:17px;">Turnover</h3>
                <div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
                <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
        `);
    }
});

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_collection_value",
		callback: function(r) {
			const value = r.message || 0;

        // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);
        const formattedTotal = parseFloat(value).toLocaleString('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0 
        });

        // const formattedAvg = parseFloat(avg).toLocaleString('en-IN', {
        //     style: 'currency',
        //     currency: 'INR',
        //     maximumFractionDigits: 0 
        // });
		const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
		let arrowSvg = `
<svg width="70" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;

				// const count = r.message || 0;
			$(wrapper).find('.collection-card').html(`
				<div class="card blink-border" style="width: 160px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">Collection</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
               <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_payable",
		callback: function(r) {
			// const value = r.message || 0;
			const value = r.message || 0;

        // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);

        
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
			let arrowSvg = `
<svg width="70" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
				// const count = r.message || 0;
			$(wrapper).find('.payable-card').html(`
				<div class="card blink-border" style="width: 150px; padding: 20px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center">Payable</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
			`);
		}
	});
	// frappe.call({
	// 		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_so_qty",
	// 		callback: function(r) {
	// 			const qty = r.message || 0;
	// 			$(wrapper).find('.so-qty-card').html(`
	// 				<div class="card blink-border" style="width: 250px; padding: 35px; border-radius: 8px;">
	// 					<h3 style="margin: 0;text-align:center">Total SO Qty</h3>
	// 					<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${qty}</div>
	// 				</div>
	// 			`);
				
	// 		}
			
	// 	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_so_qty",
		callback: function(r) {

			const total_qty = r.message.total_qty || 0;
			const average_qty = r.message.average_qty || 0;

			$(wrapper).find('.so-qty-card').html(`
    <div class="dashboard-card">
        <div class="card-top-line" style="background:#4682b4"></div>

        <div class="card-body">
            <div class="card-icon">📦</div>
            <div class="card-title">Total SO Qty</div>
            <div class="card-value">${total_qty}</div>
        </div>
    </div>
`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_receivable",
		callback: function(r) {
			// const value = r.message || 0;
			const value = r.message || 0;

        // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);
		console.log(avg_value)
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
		let arrowSvg = `
<svg width="70" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
				// const count = r.message || 0;
			$(wrapper).find('.receivable-card').html(`
				<div class="card blink-border" style="width: 150px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">Receivable</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_to_bill_value",
		callback: function(r) {
			const value = r.message || 0;
			const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
		let arrowSvg = `
<svg width="70" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
				// const count = r.message || 0;
			$(wrapper).find('.tobill-card').html(`
				<div class="card blink-border" style="width: 150px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">To Bill</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.tfp_to_deliver_bill_value",
		callback: function(r) {
			const value = r.message || 0;
			const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
		let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
				// const count = r.message || 0;
			$(wrapper).find('.todeliverbill-card').html(`
				<div class="card blink-border" style="width: 168px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">To Deliver and Bill</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
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
			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
		let arrowSvg = `
<svg width="70" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
				// const count = r.message || 0;
				$(wrapper).find('.order-booking-card').html(`
					<div class="card blink-border" style="width: 250px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;font-size:17px;">Order Booking</h3>
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
					<div class="card blink-border" style="width: 250px; padding: 15px; border-radius: 8px;">
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
				// const value = r.message || 0;
				const value = r.message || 0;

        // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);

			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
			let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
				// const count = r.message || 0;
				$(wrapper).find('.payable-card').html(`
					<div class="card blink-border" style="width: 140px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;font-size:17px;">Payable</h3>
						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
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
				 // Get current month and year
        const now = new Date();
        const currentMonth = now.getMonth() + 1; // 1-12
        const currentYear = now.getFullYear();

        // Calculate current financial month number
        // April (4) is month 1, March (3) is month 12
        let financialMonth;
        if (currentMonth >= 4) {
            financialMonth = currentMonth - 3;
        } else {
            financialMonth = currentMonth + 9;
        }

        // Calculate average
        const avg = value / financialMonth;
		const avg_value=Math.round(avg || 0);

			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
            maximumFractionDigits: 0 
        });
		let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
				// const count = r.message || 0;
				$(wrapper).find('.receivable-card').html(`
					<div class="card blink-border" style="width: 140px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;font-size:17px;">Receivable</h3>
						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
				`);
			}
		});

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
	frappe.call({
		method: 'teampro.teampro.page.finance_details.tfp_dashboard.tfp_tobill_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#tobill-so-table-content').html(r.message);
			}
			else {
				$('#tobill-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	
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
	function loadtotalsoqty(from_date = null, to_date = null) {
		// frappe.call({
		// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_so_qty",
		// 	args: { from_date, to_date },
		// 	callback: function(r) {
		// 		const qty = r.message || 0;
		// 		$(wrapper).find('.so-qty-card').html(`
		// 			<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
		// 				<h3 style="margin: 0;text-align:center">Total SO Qty</h3>
		// 				<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${qty}</div>
		// 			</div>
		// 		`);
				
		// 	}
			
		// });
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_total_so_qty",
			args: { from_date, to_date },
			callback: function(r) {

				const total_qty = r.message.total_qty || 0;
				const average_qty = r.message.average_qty || 0;

				$(wrapper).find('.so-qty-card').html(`
					<div class="card blink-border"
						style="width: 300px; padding: 35px; border-radius: 8px;">

						<h3 style="margin: 0; text-align:center;">
							Total SO Qty
						</h3>

						<div style="
							font-size: 32px;
							font-weight: bold;
							margin-top: 10px;
							color: green;
							text-align: center;
						">
							${total_qty}
						</div>

						<div style="
							margin-top: 15px;
							font-size: 16px;
							text-align: center;
							color: #555;
						">
							Average / Month : <b>${average_qty}</b>
						</div>

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

		$(wrapper).find('.opportunity-card').html(`
		<div class="dashboard-card">
			<div class="card-top-line" style="background:#20b2aa;"></div>

			<div class="card-body">
				<div class="card-icon">🎯</div>

				<div class="card-title">
					Total Expected Value
				</div>

				<div class="card-value">
					${formatted}
				</div>
			</div>
		</div>
	`);
		}
});

// 	frappe.call({
// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.total_opp_qty",

// 	callback: function(r) {

// 		const value = r.message || 0;

// 		$(wrapper).find('.total-qty-card').html(`

// 			<div class="card blink-border"
// 				style="
// 					width: 180px;
// 					height: 160px;
// 					padding: 20px;
// 					border-radius: 12px;
// 					background:white;
// 					display: flex;
// 					flex-direction: column;
// 					justify-content: center;
// 					align-items: center;
// 					box-sizing: border-box;
// 				">

// 				<h3 style="
// 					margin: 0;
// 					text-align: center;
// 					font-size: 18px;
// 					white-space: nowrap;
// 					color: black;
// 				">
// 					Total Qty
// 				</h3>

// 				<div style="
// 					font-size: 24px;
// 					font-weight: bold;
// 					margin-top: 15px;
// 					color: green;
// 					text-align: center;
// 				">
// 					${value}
// 				</div>

// 			</div>

// 		`);
// 	}
// });
	
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
		// method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_vm_stock_html",
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_stock_html_data",
		callback: function(r) {
			if (r.message) {
				$('#second-stock-table-content').html(r.message);
			}
			else {
			$('#second-stock-table-content').html(`<p>No data found.</p>`);
		}
		}
	});
	// Retail
	$('#retail-shop-availability').html(`<div style="padding: 10px;text-align:center">Loading...</div>`);
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_shop_stock_html_data",
		callback: function(r) {
			if (r.message) {
				$('#retail-shop-availability').html(r.message);
			}
			else {
			$('#retail-shop-availability').html(`<p>No data found.</p>`);
		}
		}
	});
	// RS Invoice
	$('#retail-payment-content').html(`<div style="padding: 10px;text-align:center">Loading...</div>`);
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_payment_outstanding_html_data",
		callback: function(r) {
			if (r.message) {
				$('#retail-payment-content').html(r.message);
			}
			else {
			$('#retail-payment-content').html(`<p>No data found.</p>`);
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
	$(wrapper).on('click', '#download-dashboard-stock', function () {
    window.open("/api/method/teampro.teampro.page.finance_details.tfp_dashboard.download_physical_vs_erp_stock_csv");
});

frappe.call({
    method: "teampro.teampro.page.finance_details.tfp_dashboard.get_physical_vs_erp_stock_data",
     callback: function(r) {
        const response = r.message;

        if (!response || !response.data || response.data.length === 0) {
            document.getElementById("variation-content").innerHTML = "<p>No data available.</p>";
            return;
        }

        const stockDate = response.date;
        const data = response.data;

       	let tableHTML = `
			<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;margin-top: -23px;">
			<div style="font-weight: bold; text-align: center; flex: 1;background: white;font-size:16px; ">
				LAST STOCK COUNTING DATE: 
				<span style="color: #002060;">
					${frappe.datetime.str_to_user(stockDate)}
				</span>
			</div>
			<button id="download-dashboard-stock" class="btn btn-secondary btn-sm">
				Download
			</button>
		</div>

		<div style="max-height: 400px; overflow-y: auto;">
			<table style="width: 127%; border-collapse: collapse; text-align: center;">
				<thead style="background-color: #002060; color: white;">
					<tr>
						<th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">S.No</th>
						<th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Item</th>
						<th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Item Name</th>
						<th style="padding: 8px; border: 1px solid #ccc; position: sticky; top: 0; background-color: #002060; z-index: 1;">Item Group</th>
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
						<td style="padding: 8px; border: 1px solid #ccc;;text-align:left;color: ${statusColor};">${row.item}</td>
						<td style="padding: 8px; border: 1px solid #ccc;;text-align:left">${row.item_name}</td>
						<td style="padding: 8px; border: 1px solid #ccc;;text-align:left">${row.item_group}</td>
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

