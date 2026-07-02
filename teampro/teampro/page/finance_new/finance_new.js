frappe.pages['finance-new'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Finance',
		single_column: true
	});

	
	$(wrapper).html(`
		
	<div class="dashboard-wrapper">
		<div style="position: relative; padding: 10px; text-align: center;">
			<h2 style="font-weight: bold; margin: 0;">Finance & Accounts</h2>
			
			<div id="current-datetime" style="font-size: 16px; color: #666; margin-top: 5px;"></div>
		</div>
		<div style="background-color: #f5f5f5;margin-left:20px;margin-right:20px; max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 15px; flex: 1; min-width: 30%; box-sizing: border-box;">
   
			<div class="dashboard-cards-finaince">
				<div class="dashboard-card turnover-card1"></div>
				<div class="dashboard-card order-booking-card1"></div>
				<div class="dashboard-card order-booking-card"></div>
				<div class="dashboard-card turnover-card"></div>
				<div class="po_out"></div>
				<div class="po"></div>
				<div class="amount"></div>
			</div>
		</div>

		<br>
		<div style="background-color: #f5f5f5;display: flex;gap: 5px;padding-bottom: 10px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd;border-radius: 8px;">
    
			<div id="tfp-receivable-table1" style="width: 100%;border: 1px solid #ddd;border-radius: 8px;padding: 10px;box-sizing: border-box;margin: 15px;position: relative;">
				
				<div style="display: flex; align-items: center; justify-content: space-between; height:50px; background: white; position: sticky; top: 0; z-index: 1; padding: 2px 10px; margin-bottom: -15px;">
					
					<h3 style="margin: 0;">TURNOVER</h3>
					
					<div style="display: flex; align-items: center; gap: 10px;">
						<div id="to_service_filter" style="margin: 0; padding: 0;"></div>
						<div id="to_am_filter" style="margin: 0; padding: 0;"></div>
						<div id="to_pm_filter" style="margin: 0; padding: 0;"></div>
						<button id="download-to-dashboard" class="btn btn-secondary">Download</button>
					</div>

				</div>

				<div id="to-table-content1" style="width: 100%; margin-top: 15px;"></div>
			</div>
		</div>
		<br>
		<div style="background-color: #f5f5f5;display: flex;gap: 5px;padding-bottom: 10px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd;border-radius: 8px;">
			<div id="tfp-receivable-table2" style="width: 98%;border: 1px solid #ddd;border-radius: 8px;padding: 10px;box-sizing: border-box;margin: 15px;position: relative;">
				
				<div style="display: flex; align-items: center; justify-content: space-between; height:50px; background: white; position: sticky; top: 0; z-index: 1; padding: 2px 10px; margin-bottom: -15px;">
					
					<h3 style="margin: 0;">ORDER BOOKING</h3>

					<div style="display: flex; align-items: center; gap: 10px;">
						<div id="ob_service_filter" style="margin: 0; padding: 0;"></div>
						<div id="ob_am_filter" style="margin: 0; padding: 0;"></div>
						<div id="ob_pm_filter" style="margin: 0; padding: 0;"></div>
						<button id="download-ob" class="btn btn-secondary">Download</button>
					</div>

				</div>
				<div id="ob-table" style="width: 100%; margin-top: 15px;"></div>
			</div>
		</div>
		<br>		
		<div style="background-color: #f5f5f5;display: flex;gap: 5px;padding-bottom: 10px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd;border-radius: 8px;">
			<div id="tfp-receivable-table3" style="width: 100%;border: 1px solid #ddd;border-radius: 8px;padding: 10px;box-sizing: border-box;margin: 15px;position: relative;">
				
				<div style="display: flex; align-items: center; justify-content: space-between; height:50px; background: white; position: sticky; top: 0; z-index: 1; padding: 2px 10px; margin-bottom: -15px;">
					
					<h3 style="margin: 0;">RECEIVABLE</h3>

					<div style="display: flex; align-items: center; gap: 10px;">
						<div id="rec_service_filter" style="margin: 0; padding: 0;"></div>
						<div id="rec_am_filter" style="margin: 0; padding: 0;"></div>
						<div id="rec_pm_filter" style="margin: 0; padding: 0;"></div>
						<button id="download9-dashboard" class="btn btn-secondary">Download</button>
					</div>

				</div>
				<div id="receivable-so-table-content1" style="width: 100%; margin-top: 15px;"></div>
			</div>
		</div>
		<br>
		<div style="background-color: #f5f5f5;display: flex;gap: 5px;margin-top: 5px;padding-bottom: 10px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd;border-radius: 8px;">
			<div id="tfp-receivable-table4" style="width: 100%;width:98%; border: 1px solid #ddd;border-radius: 8px;padding: 10px;box-sizing: border-box;margin: 15px;position: relative;">
				
				<div style="display: flex; align-items: center; justify-content: space-between; height:50px; background: white; position: sticky; top: 0; z-index: 1; padding: 2px 10px; margin-bottom: -15px;">
					
					<h3 style="margin: 0;">TO BILL</h3>
					
					<div style="display: flex; align-items: center; gap: 10px;">
						<div id="bill_service_filter" style="margin: 0; padding: 0;"></div>
						<div id="bill_am_filter" style="margin: 0; padding: 0;"></div>
						<div id="bill_pm_filter" style="margin: 0; padding: 0;"></div>
						<button id="download10-dashboard" class="btn btn-secondary">Download</button>
					</div>

				</div>

				<div id="tobill-so-table-content1" style="width: 100%; margin-top: 15px;"></div>
			</div>
		</div>
		<br>
		<div style="background-color: #f5f5f5;display: flex;gap: 5px;margin-top: 5px;padding-bottom: 10px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd;border-radius: 8px;">
			<div id="tfp-receivable-table5" style="width: 100%;width:98%; border: 1px solid #ddd;border-radius: 8px;padding: 10px;box-sizing: border-box;margin: 15px;position: relative;">
				
				<div style="display: flex; align-items: center; justify-content: space-between; height:50px; background: white; position: sticky; top: 0; z-index: 1; padding: 2px 10px; margin-bottom: -15px;">
					
					<h3 style="margin: 0;">PAYABLE</h3>
					
					<div style="display: flex; align-items: center; gap: 10px;">
						<div id="pay_service_filter" style="margin: 0; padding: 0;"></div>
						<div id="pay_am_filter" style="margin: 0; padding: 0;"></div>
						<div id="pay_pm_filter" style="margin: 0; padding: 0;"></div>
						<button id="download11-dashboard" class="btn btn-secondary">Download</button>
					</div>

				</div>

				<div id="payable-so-table-content" style="width: 100%; margin-top: 15px;"></div>
			</div>
		</div>
		<br>
		<div style="background-color: #f5f5f5;display: flex;gap: 5px;margin-top: 5px;padding-bottom: 10px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd;border-radius: 8px;">
			<div id="tfp-receivable-table6" style="width: 100%;width:98%; border: 1px solid #ddd;border-radius: 8px;padding: 10px;box-sizing: border-box;margin: 15px;position: relative;">
				
				<div style="display: flex; align-items: center; justify-content: space-between; height:50px; background: white; position: sticky; top: 0; z-index: 1; padding: 2px 10px; margin-bottom: -15px;">
					
					<h3 style="margin: 0;">TO BOOK</h3>
					
					<div style="display: flex; align-items: center; gap: 10px;">
						<div id="tb_service_filter" style="margin: 0; padding: 0;"></div>
						<div id="tb_am_filter" style="margin: 0; padding: 0;"></div>
						<div id="tb_pm_filter" style="margin: 0; padding: 0;"></div>
						<button id="download-tb" class="btn btn-secondary">Download</button>
					</div>

				</div>

				<div id="tb-table" style="width: 100%; margin-top: 15px;"></div>
			</div>
		</div>
		<div style="background-color:#f5f5f5; display:flex; gap:20px; margin:30px 15px; padding:10px; border:1px solid #ddd; border-radius:8px;">
			<!-- VM SALES -->
			<div style="flex:1; border:1px solid #ddd; border-radius:8px; padding:10px; box-sizing:border-box; display:flex; flex-direction:column; min-width:0;">
				<h4 style="margin:10px; text-align:center; background:white; position:sticky; top:0; z-index:2;">
					VENDING MACHINE SALES
				</h4>
				<div style="max-height:400px; overflow:auto;">
					<div id="vm-sales"></div>
				</div>
			</div>
			<!-- RETAIL SALES -->
			<div style="flex:1; border:1px solid #ddd; border-radius:8px; padding:10px; box-sizing:border-box; display:flex; flex-direction:column; min-width:0;">
				<h4 style="margin:10px; text-align:center; background:white; position:sticky; top:0; z-index:2;">
					RETAIL SHOP SALES
				</h4>
				<div style="max-height:400px; overflow:auto;">
					<div id="retail-sales"></div>
				</div>
			</div>
		</div>
		<!-- TARGET VS ACHIEVEMENT REPORT -->
		<div style="margin:30px 15px; border:1px solid #ddd; border-radius:8px; padding:10px; background-color:#f5f5f5;">

		<!-- Header -->
		<div style="
			display:flex;
			justify-content:space-between;
			align-items:center;
			background:white;
			border-radius:5px;
			padding:12px 15px;
			margin-bottom:10px;
		">

			<!-- Title -->
			<h3 style="
				margin:0;
				font-size:18px;
				font-weight:700;
				color:#000;
			">
				TARGET VS ACHIEVEMENT REPORT
			</h3>

			<!-- Filters and Download -->
			<div style="display:flex; align-items:center; gap:10px;">

				<div id="tb_service_filter" style="min-width:180px;"></div>

				<div id="tb_employee_filter" style="min-width:180px;"></div>

				<div id="tb_target_filter" style="min-width:180px;"></div>

				<button id="download_target_achievement"
						class="btn btn-secondary">
					Download
				</button>

			</div>

		</div>

		<!-- Table -->
		<div style="overflow:auto; max-height:400px;">
			<table class="table table-bordered" style="margin-bottom:0;">
				<thead style="position:sticky; top:0; z-index:2;">
					<tr>
						<th style="background:#002060; color:white;">ID</th>
						<th style="background:#002060; color:white;">Employee</th>
						<th style="background:#002060; color:white;">Employee Name</th>
						<th style="background:#002060; color:white;">Target Based On</th>
						<th style="background:#002060; color:white;">Target (INR)</th>
						<th style="background:#002060; color:white;">Total YTA Target (INR)</th>
						<th style="background:#002060; color:white;">Total Target (INR)</th>
						<th style="background:#002060; color:white;">Total Target (Point)</th>
						<th style="background:#002060; color:white;">Total Achieved (INR)</th>
						<th style="background:#002060; color:white;">Total Achieved (Point)</th>
					</tr>
				</thead>
				<tbody id="target-vs-achievement-body">
				</tbody>
			</table>
		</div>

	</div>

	</div>	

	<style>
		.dashboard-cards-finaince{
			display:flex;
			gap:20px;
			flex-wrap:nowrap;
			overflow-x:auto;
			padding:10px;
		}

		.dashboard-card,
		.po_out,
		.po,
		.amount{
			min-width:240px;
			min-height:170px;
			height:auto;
			border-radius:20px;
			background:#fff;
			border-top:5px solid #f59e0b;
			box-shadow:0 4px 14px rgba(0,0,0,.08);
			position:relative;
			overflow:hidden;
			padding:12px;
		}

		.dashboard-card::before,
		.po_out::before,
		.po::before,
		.amount::before{
			content:'';
			position:absolute;
			top:-25px;
			right:-25px;
			width:80px;
			height:80px;
			border-radius:50%;
		}

		.turnover-card1{border-top-color:#4f46e5;}
		.turnover-card1::before{background:#ede9fe;}

		.order-booking-card1{border-top-color:#10b981;}
		.order-booking-card1::before{background:#d1fae5;}

		.order-booking-card{border-top-color:#3b82f6;}
		.order-booking-card::before{background:#dbeafe;}

		.turnover-card{border-top-color:#ec4899;}
		.turnover-card::before{background:#fce7f3;}

		.po_out{border-top-color:#14b8a6;}
		.po_out::before{background:#ccfbf1;}

		.po{border-top-color:#f97316;}
		.po::before{background:#ffedd5;}

		.amount{border-top-color:#06b6d4;}
		.amount::before{background:#cffafe;}

		.card-title{
			text-align:center;
			font-size:16px;
			font-weight:bold;
			margin-bottom:10px;
		}

		.card-total{
			text-align:center;
			margin-bottom:15px;
			margin-bottom:15px;
		}

		.card-total span{
			display:inline-block;
			background:#e8f5e9;
			padding:4px 14px;
			border-radius:50px;
			color:green;
			font-weight:bold;
			font-size:22px;
		}

		.service-grid{
			border-top:1px solid #eee;
			padding-top:8px;

			display:grid;
			grid-template-columns:repeat(3,1fr);

			column-gap:0px;
			row-gap:6px;

			width:100%;
		}


		.service-row{
			display:flex;
			align-items:center;
			justify-content:flex-start;

			min-width:0;
			white-space:nowrap;
		}

		.service-name{
			font-size:10px;
			font-weight:bold;
			color:black;
			margin-right:1px;
		}

		.service-value{
			font-size:10px;
			color:red;
			font-weight:bold;
		}
		#rec_service_filter .frappe-control,
		#rec_am_filter .frappe-control,
		#rec_pm_filter .frappe-control {
			margin-bottom: 0 !important;
			padding-bottom: 0 !important;
		}

		#rec_service_filter .form-group,
		#rec_am_filter .form-group,
		#rec_pm_filter .form-group {
				margin-bottom: 0 !important;
		}

		#rec_service_filter input,
		#rec_am_filter input,
		#rec_pm_filter input {
			height: 30px !important;
			font-size: 12px !important;
			padding: 4px 8px !important;
			min-width: 120px;
		}
			#to_service_filter .frappe-control,
			#to_am_filter .frappe-control,
			#to_pm_filter .frappe-control {
				margin-bottom: 0 !important;
				padding-bottom: 0 !important;
			}

			#to_service_filter .form-group,
			#to_am_filter .form-group,
			#to_pm_filter .form-group {
				margin-bottom: 0 !important;
			}

			#to_service_filter input,
			#to_am_filter input,
			#to_pm_filter input {
				height: 30px !important;
				font-size: 12px !important;
				padding: 4px 8px !important;
				min-width: 120px;
			}
		#bill_service_filter .frappe-control,
		#bill_am_filter .frappe-control,
		#bill_pm_filter .frappe-control {
			margin-bottom: 0 !important;
			padding-bottom: 0 !important;
		}

		#bill_service_filter .form-group,
		#bill_am_filter .form-group,
		#bill_pm_filter .form-group {
			margin-bottom: 0 !important;
		}

		#bill_service_filter input,
		#bill_am_filter input,
		#bill_pm_filter input {
			height: 30px !important;
			font-size: 12px !important;
			padding: 4px 8px !important;
			min-width: 120px;
		}
		#ob_service_filter .frappe-control,
		#ob_am_filter .frappe-control,
		#ob_pm_filter .frappe-control {
			margin-bottom: 0 !important;
			padding-bottom: 0 !important;
		}

		#ob_service_filter .form-group,
		#ob_am_filter .form-group,
		#ob_pm_filter .form-group {
			margin-bottom: 0 !important;
		}

		#ob_service_filter input,
		#ob_am_filter input,
		#ob_pm_filter input {
			height: 30px !important;
			font-size: 12px !important;
			padding: 4px 8px !important;
			min-width: 120px;
		}
		#tb_service_filter .frappe-control,
		#tb_am_filter .frappe-control,
		#tb_pm_filter .frappe-control {
			margin-bottom: 0 !important;
			padding-bottom: 0 !important;
		}

		#tb_service_filter .form-group,
		#tb_am_filter .form-group,
		#tb_pm_filter .form-group {
			margin-bottom: 0 !important;
		}

		#tb_service_filter input,
		#tb_am_filter input,
		#tb_pm_filter input {
			height: 30px !important;
			font-size: 12px !important;
			padding: 4px 8px !important;
			min-width: 120px;
		}
		#pay_service_filter .frappe-control,
		#pay_am_filter .frappe-control,
		#pay_pm_filter .frappe-control {
			margin-bottom: 0 !important;
			padding-bottom: 0 !important;
		}

		#pay_service_filter .form-group,
		#pay_am_filter .form-group,
		#pay_pm_filter .form-group {
				margin-bottom: 0 !important;
		}

		#pay_service_filter input,
		#pay_am_filter input,
		#payc_pm_filter input {
			height: 30px !important;
			font-size: 12px !important;
			padding: 4px 8px !important;
			min-width: 120px;
		}

</style>

	

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


	function formatToLakhs(val){
		return '₹' + (val / 100000).toFixed(2) + 'L';
	}

	function buildServiceGrid(groups, order){

		const rows = order
			.filter(key => (groups[key] || 0) > 0)
			.map(key => `
				<div class="service-row">
					<span class="service-name">${key}:</span>
					<span class="service-value">
						${formatToLakhs(groups[key])}
					</span>
				</div>
			`);

		return rows.join('');
	}

	// function buildServiceGrid(groups, order){
	// 	return order.map(key => `
	// 		<div class="service-row">
	// 			<span class="service-name">${key}:</span>
	// 			<span class="service-value">
	// 				${formatToLakhs(groups[key] || 0)}
	// 			</span>
	// 		</div>
	// 	`).join('');
	// }

	function renderCard(selector, title, total, groups, order){
		
		const gridHtml = buildServiceGrid(groups, order);

		$(wrapper).find(selector).html(`
			<div class="card-title">${title}</div>

			<div class="card-total">
				<span>${formatToLakhs(total)}</span>
			</div>

			<div class="service-grid">
				${gridHtml}
			</div>
		`);
	}

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_turnover_overall",
		callback: function(r) {

			const data = r.message || {};
			const value = data.total || 0;
			const groups = data.groups || {};

			renderCard(
				'.turnover-card1',
				'Turnover',
				value,
				groups,
				["HRS","ITS","CMN","TFP","HRIT"]
			);
		}
	});

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_order_booking_overall",
		callback: function(r) {

			const data = r.message || {};
			const value = data.total || 0;
			const groups = data.groups || {};

			renderCard(
				'.order-booking-card1',
				'Order Booking',
				value,
				groups,
				["HRS","ITS","CMN","TFP","HRIT"]
			);
		}
	});
	loadCard();
	function loadCard() {

		frappe.call({
			method: "teampro.teampro.page.finance.finance_dashboard.card",
			callback: function(r) {

				const data = r.message || {};

				renderCard(
					'.order-booking-card',
					'Receivable',
					data.total || 0,
					data.groups || {},
					["HRS","ITS","CMN","TFP","HRIT"]
				);
			}
		});
	}
	load_billing_outstanding_card();
	function load_billing_outstanding_card(){

		frappe.call({
			method:"teampro.teampro.page.finance.finance_dashboard.card_1",
			callback:function(r){

				const data = r.message || {};

				let groups = data.groups || {};

				groups.CLR = data.clr || 0;
				groups.CLN = data.cln || 0;

				renderCard(
					'.turnover-card',
					'To Bill',
					data.total || 0,
					groups,
					["HRS","ITS","CMN","TFP","HRIT","CLR","CLN"]
				);
			}
		});
	}
	load_po_out_balance();
	function load_po_out_balance() {

		frappe.call({
			method: "teampro.teampro.page.finance.finance_dashboard.po_out",
			callback: function(r) {

				const data = r.message || {};

				renderCard(
					'.po_out',
					'Payable',
					data.total || 0,
					data.groups || {},
					["HRS","ITS","CMN","TFP","HRIT"]
				);
			}
		});
	}
	load_po_balance();
	function load_po_balance() {

		frappe.call({
			method: "teampro.teampro.page.finance.finance_dashboard.po",
			callback: function(r) {

				const data = r.message || {};
				let groups = data.groups || {};

				groups.CLN = data.cln || 0;

				renderCard(
					'.po',
					'To Book',
					data.total || 0,
					groups,
					["HRS","ITS","CMN","TFP","HRIT","CLN"]
				);
			}
		});
	}
	load_fund_card();
	function load_fund_card() {

		frappe.call({
			method: "teampro.teampro.page.finance.finance_dashboard.fund_card",
			callback: function(r) {

				const data = r.message || {};

				renderCard(
					'.amount',
					'Fund',
					data.total || 0,
					{
						BANK: data.bank || 0,
						CASH: data.cash || 0,
						SFD: data.sfd || 0,
						LFD: data.lfd || 0
					},
					["BANK","CASH","SFD","LFD"]
				);
			}
		});
	}

	function add_filter(parent_id, df, callback_function = null) {

		$(parent_id).empty();

		const control = frappe.ui.form.make_control({
			parent: $(parent_id),

			df: Object.assign({
				reqd: 0,

				onchange: function () {

					frappe.dom.freeze('Loading data...');

					if (callback_function) {
						Promise.resolve(callback_function()).finally(function () {
							frappe.dom.unfreeze();
						});
					} else {
						frappe.dom.unfreeze();
					}
				}

			}, df),

			render_input: true
		});

		control.make();
		control.refresh();

		return control;
	}
	
	let rec_service_filter = add_filter('#rec_service_filter', {
		fieldtype: 'Link',
		options: 'Services',
		fieldname: 'rec_service',
		placeholder: 'Service'
	}, load_receivable_overall_table);

	let rec_am_filter = add_filter('#rec_am_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'rec_am',
		placeholder: 'AM'
	}, load_receivable_overall_table);

	let rec_pm_filter = add_filter('#rec_pm_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'rec_pm',
		placeholder: 'PM'
	}, load_receivable_overall_table);

	let to_service_filter = add_filter('#to_service_filter', {
		fieldtype: 'Link',
		options: 'Services',
		fieldname: 'to_service',
		placeholder: 'Service'
	}, load_turnover_overall_table);

	let to_am_filter = add_filter('#to_am_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'to_am',
		placeholder: 'AM'
	}, load_turnover_overall_table);

	let to_pm_filter = add_filter('#to_pm_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'to_pm',
		placeholder: 'PM'
	}, load_turnover_overall_table);

	let bill_service_filter = add_filter('#bill_service_filter', {
		fieldtype: 'Link',
		options: 'Services',
		fieldname: 'bill_service',
		placeholder: 'Service'
	}, load_tobill_overall_table);

	let bill_am_filter = add_filter('#bill_am_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'bill_am',
		placeholder: 'AM'
	}, load_tobill_overall_table);

	let bill_pm_filter = add_filter('#bill_pm_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'bill_pm',
		placeholder: 'PM'
	}, load_tobill_overall_table);

	let ob_service_filter = add_filter('#ob_service_filter', {
		fieldtype: 'Link',
		options: 'Services',
		fieldname: 'ob_service',
		placeholder: 'Service'
	}, load_ob_overall_table);

	let ob_am_filter = add_filter('#ob_am_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'ob_am',
		placeholder: 'AM'
	}, load_ob_overall_table);

	let ob_pm_filter = add_filter('#ob_pm_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'ob_pm',
		placeholder: 'PM'
	}, load_ob_overall_table);


	let tb_service_filter = add_filter('#tb_service_filter', {
		fieldtype: 'Link',
		options: 'Services',
		fieldname: 'tb_service',
		placeholder: 'Service'
	}, load_to_book_table);

	let tb_am_filter = add_filter('#tb_am_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'tb_am',
		placeholder: 'AM'
	}, load_to_book_table);

	let tb_pm_filter = add_filter('#tb_pm_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'tb_pm',
		placeholder: 'PM'
	}, load_to_book_table);

	$('#tb_am_filter').hide();
	$('#tb_pm_filter').hide();

	let pay_service_filter = add_filter('#pay_service_filter', {
		fieldtype: 'Link',
		options: 'Services',
		fieldname: 'pay_service',
		placeholder: 'Service'
	}, load_payable_table);

	let pay_am_filter = add_filter('#pay_am_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'payc_am',
		placeholder: 'AM'
	}, load_payable_table);

	let pay_pm_filter = add_filter('#pay_pm_filter', {
		fieldtype: 'Link',
		options: 'User',
		fieldname: 'pay_pm',
		placeholder: 'PM'
	}, load_payable_table);

	$('#pay_am_filter').hide();
	$('#pay_pm_filter').hide();


	
load_turnover_overall_table();
load_ob_overall_table();
load_receivable_overall_table();
load_tobill_overall_table();
load_payable_table();
load_to_book_table();

function load_to_book_table() {
    let service = tb_service_filter.get_value();
    let am = tb_am_filter.get_value();
    let pm = tb_pm_filter.get_value();

    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.to_book_table_overall",
        args: {
            overall_service: service,
            account_manager: am,
            project_manager: pm
        },
        callback: function(r) {
            if (r.message) {
                $("#tb-table").html(r.message.html);
            } else {
                $("#tb-table").html(
                    `<div style="padding:10px;text-align:center">No data found</div>`
                );
            }
        }
    });
}
function load_turnover_overall_table() {

    let service = to_service_filter.get_value();
    let am = to_am_filter.get_value();
    let pm = to_pm_filter.get_value();

    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.download_to_table_overall",
        args: {
            overall_service: service,
            account_manager: am,
            project_manager: pm
        },
        callback: function(r) {
			if (r.message) {
				
                $("#to-table-content1").html(r.message.html);
            }
            else {
                $("#to-table-content1").html(
                    `<div style="padding:10px;text-align:center">
                        No data found
                    </div>`
                );
            }
        }
    });
}
function load_ob_overall_table() {

    let service = ob_service_filter.get_value();
    let am = ob_am_filter.get_value();
    let pm = ob_pm_filter.get_value();

    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.ob_table_overall",
        args: {
            overall_service: service,
            account_manager: am,
            project_manager: pm
        },
        callback: function(r) {

            if (r.message) {
                $("#ob-table").html(r.message.html);
            }
            else {
                $("#ob-table").html(
                    `<div style="padding:10px;text-align:center">
                        No data found
                    </div>`
                );
            }
        }
    });
}
function load_receivable_overall_table() {
	frappe.call({
		method: 'teampro.teampro.page.finance_details.tfp_dashboard.receivable_table_overall',
		args: {
			service: rec_service_filter.get_value() || null,
			am: rec_am_filter.get_value() || null,
			pm: rec_pm_filter.get_value() || null
		},
		callback: function(r) {
			if (r.message) {
				$('#receivable-so-table-content1').html(r.message);
			} else {
				$('#receivable-so-table-content1').html(
					`<div style="padding: 10px; text-align:center">No data found</div>`
				);
			}
			frappe.dom.unfreeze();
		},
		error: function() {
			frappe.dom.unfreeze();
		}
	});
}
function load_tobill_overall_table() {

    let service = bill_service_filter.get_value();
    let am = bill_am_filter.get_value();
    let pm = bill_pm_filter.get_value();

    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.tobill_table_overall",
        args: {
            overall_service: service,
            account_manager: am,
            project_manager: pm
        },
        callback: function(r) {

            if (r.message) {
                $("#tobill-so-table-content1").html(r.message.html);
            }
            else {
                $("#tobill-so-table-content1").html(
                    `<div style="padding:10px;text-align:center">
                        No data found
                    </div>`
                );
            }
        }
    });
}
function load_payable_table() {
	let service = pay_service_filter.get_value();
	let am = pay_am_filter.get_value();
	let pm = pay_pm_filter.get_value();

	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.payable_table_overall",
		args: {
			overall_service: service,
			account_manager: am,
			project_manager: pm
		},
		callback: function(r) {
			if (r.message) {
				$("#payable-so-table-content").html(r.message);
			} else {
				$("#payable-so-table-content").html(
					`<div style="padding:10px;text-align:center">No data found</div>`
				);
			}
		}
	});
}



$(wrapper).on('click', '#download-to-dashboard', function () {

	const overall_service = to_service_filter.get_value() || "";
	const account_manager = to_am_filter.get_value() || "";
	const project_manager = to_pm_filter.get_value() || "";

	const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_to_table_overall_excel";

	window.location.href = frappe.request.url
		+ '?cmd=' + path
		+ '&overall_service=' + encodeURIComponent(overall_service)
		+ '&account_manager=' + encodeURIComponent(account_manager)
		+ '&project_manager=' + encodeURIComponent(project_manager);

});

$(wrapper).on('click', '#download-ob', function () {

	const overall_service = ob_service_filter.get_value() || "";
	const account_manager = ob_am_filter.get_value() || "";
	const project_manager = ob_pm_filter.get_value() || "";

	const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_ob_excel";

	window.location.href = frappe.request.url
		+ '?cmd=' + path
		+ '&overall_service=' + encodeURIComponent(overall_service)
		+ '&account_manager=' + encodeURIComponent(account_manager)
		+ '&project_manager=' + encodeURIComponent(project_manager);

});

$(wrapper).on('click', '#download9-dashboard', function () {
	const service = rec_service_filter.get_value() || "";
	const am = rec_am_filter.get_value() || "";
	const pm = rec_pm_filter.get_value() || "";

	const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_receivable_table_overall";
	window.location.href = frappe.request.url
		+ '?cmd=' + path
		+ '&service=' + encodeURIComponent(service)
		+ '&am=' + encodeURIComponent(am)
		+ '&pm=' + encodeURIComponent(pm);
});

$(wrapper).on('click', '#download10-dashboard', function () {

	const overall_service = bill_service_filter.get_value() || "";
	const account_manager = bill_am_filter.get_value() || "";
	const project_manager = bill_pm_filter.get_value() || "";

	const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_tobill_excel";

	window.location.href = frappe.request.url
		+ '?cmd=' + path
		+ '&overall_service=' + encodeURIComponent(overall_service)
		+ '&account_manager=' + encodeURIComponent(account_manager)
		+ '&project_manager=' + encodeURIComponent(project_manager);

});

$(wrapper).on('click', '#download11-dashboard', function () {

	const overall_service = pay_service_filter.get_value() || "";
	const account_manager = pay_am_filter.get_value() || "";
	const project_manager = pay_pm_filter.get_value() || "";

	const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_payable_table1";

	window.location.href = frappe.request.url
		+ '?cmd=' + path
		+ '&overall_service=' + encodeURIComponent(overall_service)
		+ '&account_manager=' + encodeURIComponent(account_manager)
		+ '&project_manager=' + encodeURIComponent(project_manager);

});




$(document).off("click", ".po_out").on("click", ".po_out", function (e) {
    e.preventDefault();

    const targetElement = document.getElementById("tfp-receivable-table5");

    if (targetElement) {
        const targetSection = targetElement.parentElement;

        //  Approvals model standard block native layout configuration override calculation
        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        setTimeout(function() {
            let $frappeScroll = $('.layout-main-section, .page-container, .layout-main-section-html');
            if ($frappeScroll.scrollTop() === 0) {
                let elementTopOffset = $(targetSection).offset().top;
                $frappeScroll.stop().animate({
                    scrollTop: elementTopOffset - 20
                }, 400);
            }
        }, 100);

    } else {
        console.warn("PAYABLE Table matrix reference element structure is currently missing.");
    }
});

$(document).off("click", ".turnover-card1").on("click", ".turnover-card1", function (e) {
    e.preventDefault();

    const targetElement = document.getElementById("tfp-receivable-table1");

    if (targetElement) {
        const targetSection = targetElement.parentElement;

        //  Approvals model standard block native layout configuration override calculation
        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        setTimeout(function() {
            let $frappeScroll = $('.layout-main-section, .page-container, .layout-main-section-html');
            if ($frappeScroll.scrollTop() === 0) {
                let elementTopOffset = $(targetSection).offset().top;
                $frappeScroll.stop().animate({
                    scrollTop: elementTopOffset - 20
                }, 400);
            }
        }, 100);

    } else {
        console.warn("TURNOVER Table matrix reference element structure is currently missing.");
    }
});

$(document).off("click", ".order-booking-card1").on("click", ".order-booking-card1", function (e) {
    e.preventDefault();

    const targetElement = document.getElementById("tfp-receivable-table2");

    if (targetElement) {
        const targetSection = targetElement.parentElement;

        //  Approvals model standard block native layout configuration override calculation
        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        setTimeout(function() {
            let $frappeScroll = $('.layout-main-section, .page-container, .layout-main-section-html');
            if ($frappeScroll.scrollTop() === 0) {
                let elementTopOffset = $(targetSection).offset().top;
                $frappeScroll.stop().animate({
                    scrollTop: elementTopOffset - 20
                }, 400);
            }
        }, 100);

    } else {
        console.warn("ORDER BOOKING Table matrix reference element structure is currently missing.");
    }
});

$(document).off("click", ".order-booking-card").on("click", ".order-booking-card", function (e) {
    e.preventDefault();

    const targetElement = document.getElementById("tfp-receivable-table3");

    if (targetElement) {
        const targetSection = targetElement.parentElement;

        //  Approvals model standard block native layout configuration override calculation
        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        setTimeout(function() {
            let $frappeScroll = $('.layout-main-section, .page-container, .layout-main-section-html');
            if ($frappeScroll.scrollTop() === 0) {
                let elementTopOffset = $(targetSection).offset().top;
                $frappeScroll.stop().animate({
                    scrollTop: elementTopOffset - 20
                }, 400);
            }
        }, 100);

    } else {
        console.warn("RECEIVABLE Table matrix reference element structure is currently missing.");
    }
});


$(document).off("click", ".turnover-card").on("click", ".turnover-card", function (e) {
    e.preventDefault();

    const targetElement = document.getElementById("tfp-receivable-table4");

    if (targetElement) {
        const targetSection = targetElement.parentElement;

        //  Approvals model standard block native layout configuration override calculation
        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        setTimeout(function() {
            let $frappeScroll = $('.layout-main-section, .page-container, .layout-main-section-html');
            if ($frappeScroll.scrollTop() === 0) {
                let elementTopOffset = $(targetSection).offset().top;
                $frappeScroll.stop().animate({
                    scrollTop: elementTopOffset - 20
                }, 400);
            }
        }, 100);

    } else {
        console.warn("TO BILL Table matrix reference element structure is currently missing.");
    }
});

$(document).off("click", ".po").on("click", ".po", function (e) {
    e.preventDefault();

    const targetElement = document.getElementById("tfp-receivable-table6");

    if (targetElement) {
        const targetSection = targetElement.parentElement;

        //  Approvals model standard block native layout configuration override calculation
        targetSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        setTimeout(function() {
            let $frappeScroll = $('.layout-main-section, .page-container, .layout-main-section-html');
            if ($frappeScroll.scrollTop() === 0) {
                let elementTopOffset = $(targetSection).offset().top;
                $frappeScroll.stop().animate({
                    scrollTop: elementTopOffset - 20
                }, 400);
            }
        }, 100);

    } else {
        console.warn("TO BOOK Table matrix reference element structure is currently missing.");
    }
});

$(document).on("click", "#download_target_achievement", function () {
	window.location.href =
		"/api/method/teampro.teampro.page.finance.finance_dashboard.download_target_achievement";
});


load_vm_sales();
load_retail_sales();
load_target_vs_achievement();

function load_vm_sales() {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.vm_sales",
		callback: function (r) {

			if (r.message) {
				$('#vm-sales').html(r.message);
			} else {
				$('#vm-sales').html(`<div style="padding:10px;text-align:center">No data found</div>`);
			}

		}
	});
}

function load_retail_sales() {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.retail_shops",
		callback: function (r) {

			if (r.message) {
				$('#retail-sales').html(r.message);
			} else {
				$('#retail-sales').html(`<div style="padding:10px;text-align:center">No data found</div>`);
			}

		}
	});
}

function load_target_vs_achievement() {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.target_vs_achievement",
		callback: function(r) {

			if (r.message) {
				$('#target-vs-achievement-body').html(r.message);
			} else {
				$('#target-vs-achievement-body').html(
					`<tr><td colspan="6" style="text-align:center">No data found</td></tr>`
				);
			}

		}
	});
}

}


