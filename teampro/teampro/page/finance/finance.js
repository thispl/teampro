frappe.pages['finance'].on_page_load = function(wrapper) {
	
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});
// Hide only the Service filter input and its wrapper container

	page.set_title("Finance & Accounts");
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
	padding: 15px;
	border-radius: 12px;
	color: white;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	text-align: center;
	font-size: 14px;
	font-weight: bold;
	min-width: 150px;
	flex-shrink: 0;
}

	.order-booking-card {
		background-color: #0a9396; /* Teal Blue - calm and modern */
	}
	.order-booking-card1 {
		background-color: #0a9396; /* Teal Blue - calm and modern */
	}
	.dashboard-cards-rs >div {
		padding:15px;
		border-radius:12px;
		color:white;
		box-shadow:0 4px 12px rgba(0, 0, 0, 0.1);
		text-align: center;
		font-size: 18px;
		font-weight: bold;
		min-width: 150px;
		flex-shrink: 0;
		}
	.order-booking-card4 {
			background-color: #0a9396; /* Teal Blue - calm and modern */
			}
		
		.turnover-card4 {
		background-color: #2e8b57; /* Sea Green */
		}
	
		.collection-card4 {
		background-color: #b8860b; /* Dark Goldenrod */
		}	

		.receivable-card4 {
		background-color: #4b0082; /* Indigo - strong but professional */
		}

		.tobill-card4 {
		background-color: #8b0000; /* Dark Red */
		}

		.todeliverbill-card4 {
		background-color: #4682b4; /* Dark Red */
		}

	.card-inner {
		background-color: white;
		padding: 20px 10px;
		border-radius: 8px;
		box-shadow: 0 2px 5px rgba(0,0,0,0.1);
	}
	.card-inner h3 {
		margin: 0;
		font-size: 17px;
		font-weight: bold;
		color: #222;
		text-align: center;
		white-space: normal;
	}
	.card-inner .amount {
		font-size: 22px;
		font-weight: bold;
		color: green;
		margin-top: 10px;
		text-align: center;
	}
	.card-inner .avg { font-size: 13px; font-weight: bold; color: red; margin-top: 10px; text-align: center; }
	.todeliverbill-card{
	background-color: #4169e1;
	}
	.todeliverbill-card1{
	background-color: #4169e1;
	}
	.turnover-card {
		background-color: #2e8b57; /* Sea Green */
	}
	.turnover-card1 {
		background-color: #2e8b57; /* Sea Green */
	}
	.po_out {
		background-color: #b8860b; /* Dark Goldenrod */
	}
		.collection-card {
		background-color: #b8860b; /* Dark Goldenrod */
	}
	.collection-card1 {
		background-color: #b8860b; /* Dark Goldenrod */
	}
	.payable-card {
		background-color: #8b0000; /* Dark Red */
	}
	.payable-card1 {
		background-color: #8b0000; /* Dark Red */
	}
	.po_payment {
		background-color: #8b0000; /* Dark Red */
	}
	.receivable-card {
		background-color: #4b0082; /* Indigo - strong but professional */

	}
	@keyframes blink-border {
    0%   { border-color: rgb(151, 158, 153); }
    50%  { border-color: transparent; }
    100% { border-color: rgb(151, 158, 153); }
  }

  .blink-border {
    animation: blink-border 2s infinite;
  }

  @keyframes blink-border-name {
    0%   { border-color: rgb(255, 255, 255); }
    50%  { border-color: transparent; }
    100% { border-color: rgb(255, 255, 255); }
  }

  .blink-border-name {
    animation: blink-border-name 0.2s infinite;
  }
	.receivable-card1 {
		background-color: #4b0082; /* Indigo - strong but professional */

	}
	.active-customer-card{
	background-color: #2e8b57; /* Sea Green */
	}
	.bank{
	background-color: #2e8b57; /* Sea Green */
	}
	.so-qty-card {
		background-color: #4682b4; /* Steel Blue */
	}
	.cash{
		background-color: #4682b4; /* Steel Blue */
	}
	.opportunity-card {
		background-color: #20b2aa; /* Dark Orange */
	}
	.sfd {
		background-color: #20b2aa; /* Dark Orange */
	}
	.total-qty-card {
		background-color: #b8860b; /* Slate Blue */
	}
		.lfd{
		background-color: #b8860b; /* Slate Blue */
	}
	.tobill-card {
	background-color: #006d77; /* Example teal blue, you can change it */
	}
	.tobill-card1 {
	background-color: #006d77; /* Example teal blue, you can change it */
	}
		.po{
	background-color: #006d77; /* Example teal blue, you can change it */
	}
	#chart_3 .graph-legend {
    display: none !important;
}



		<style>
	
}


	`;
	document.head.appendChild(style);
	$(wrapper).html(`
		
<div class="dashboard-wrapper">
			<div style="position: relative; padding: 10px; text-align: center;">
				<h2 style="font-weight: bold; margin: 0;">Finance & Accounts</h2>
				<div class="top-actions">
					<input type="date" id="tfp-from-date" class="form-control" style="width: 140px;">
					<input type="date" id="tfp-to-date" class="form-control" style="width: 140px;">
					<button id="apply-tfp-filter" class="btn btn-primary">Apply</button>
					<button id="refresh-dashboard" class="btn btn-primary">Refresh</button>
			</div>
				<div id="current-datetime" style="font-size: 16px; color: #666; margin-top: 5px;"></div>
			</div>

	<div class="active-customer-wrapper" style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box; margin-left: 15px; margin-right: 15px;">
	<div class="dashboard-cards-finaince" style="display: flex; gap: 30px; flex-wrap: nowrap; overflow-x: auto; justify-content: space-between;">
		
	

    <style>
        .dashboard-cards-finaince{
            display:flex;
            gap:30px;
            flex-wrap:nowrap;
            overflow-x:auto;
            justify-content:space-between;
        }

		.dashboard-card,
		.po_out,
		.po,
		.amount {
			min-width: 200px;
			height: 170px;
			border-radius: 20px;
			background: #ffffff;
			border-top: 5px solid #f59e0b;
			box-shadow: 0 4px 14px rgba(0,0,0,0.08);
			position: relative;
			overflow: hidden;
			padding: 10px;
		}

		.dashboard-card::before,
		.po_out::before,
		.po::before,
		.amount::before {
			content: '';
			position: absolute;
			top: -25px;
			right: -25px;
			width: 80px;
			height: 80px;
			border-radius: 50%;
			background: #fff7ed; /* default orange light */
		}

		.turnover-card1      { border-top-color: #4f46e5; }
		.turnover-card1::before      { background: #ede9fe; } /* purple light */

		.order-booking-card1 { border-top-color: #10b981; }
		.order-booking-card1::before { background: #d1fae5; } /* green light */

		.order-booking-card  { border-top-color: #3b82f6; }
		.order-booking-card::before  { background: #dbeafe; } /* blue light */

		.turnover-card       { border-top-color: #ec4899; }
		.turnover-card::before       { background: #fce7f3; } /* pink light */

		.collection-card     { border-top-color: #f43f5e; }
		.collection-card::before     { background: #ffe4e6; } /* red light */

		.receivable-card     { border-top-color: #8b5cf6; }
		.receivable-card::before     { background: #ede9fe; } /* violet light */

		.po_out              { border-top-color: #14b8a6; }
		.po_out::before              { background: #ccfbf1; } /* teal light */

		.po                  { border-top-color: #f97316; }
		.po::before                  { background: #ffedd5; } /* amber light */

		.amount          { border-top-color: #06b6d4; }
		.amount::before          { background: #cffafe; } /* cyan light */
			
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
</div>

<!-- Flex container for three side-by-side tables -->
<div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 15px; justify-content: space-between;">

  <!-- Collection Outstanding -->
  <div style=" display: none; background-color: #f5f5f5; max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 15px; flex: 1; min-width: 30%; box-sizing: border-box;">
    <h4 style="margin: 10px 0; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">COLLECTION OUTSTANDING</h4>
		<div style="display:flex; gap:10px; margin-top:-20px;">

			<div id="service_filter"></div>

			<div id="am_filter"></div>

			<div id="dm_filter"></div>

		</div>

	<div id="receivable-so-table-content" style="margin-top: -50px;"></div>
  </div>

  <!-- Sales Order O/S (Billing) -->
  <div style=" display: none; background-color: #f5f5f5; max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 15px; flex: 1; min-width: 30%; box-sizing: border-box;">
    <h4 style="margin: 10px 0; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">SALES ORDER O/S (BILLING) - SERVICES</h4>
    <div style="display:flex; gap:10px; margin-bottom:0px;margin-top:-20px;">
        <div id="invoice_service_filter"></div>

        <div id="invoice_am_filter"></div>

        <div id="invoice_dm_filter"></div>

    </div>
	<div id="tobill-so-table-content" style="margin-top: -60px;"></div>
  </div>

  <!-- Sales Order O/S (Collection) -->
  <div style=" display: none; background-color: #f5f5f5; max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 8px; padding: 15px; flex: 1; min-width: 30%; box-sizing: border-box;">
    <h4 style="margin: 10px 0; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">SALES ORDER O/S (COLLECTION) - SERVICES</h4>
    <div id="rec-so-table-content" style="margin-top: 10px;"></div>
  </div>

</div>







<div class="active-customer-wrapper" style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box; margin: 20px 15px 0 15px;width:98%;display:none;">
  <div class="dashboard-cards-finaince" style="display: flex; gap: 30px; overflow-x: auto;">
    <div class="bank"></div>
    <div class="cash" ></div>
    <div class="sfd" ></div>
    <div class="lfd" ></div>
</div>
</div>

<!-- Wrapper for 3 Tables in One Row -->
<div style="display: flex; justify-content: space-between; gap: 20px; padding: 20px 15px; flex-wrap: nowrap;">

  <!-- Table 1 -->
  <div style="display: none;background-color: #f5f5f5; max-height: 400px; border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 33%; box-sizing: border-box; position: relative;">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">CLOSURE - PAYMENT FROM</h4>
     <div style="display:flex; gap:10px; margin-bottom:0px;margin-top:-20px;">
        <div id="closure_service_filter"></div>

        <div id="closure_am_filter"></div>

        <div id="closure_dm_filter"></div>

    </div>
	<div id="so-table-content" style="margin-top: -60px;"></div>
  </div>

  <!-- Table 2 -->
  <div style="display: none;background-color: #f5f5f5; max-height: 400px; border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 33%; box-sizing: border-box; position: relative;">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">FUND IN HAND</h4>
    <div id="so-table" style="margin-top: 10px;"></div>
  </div>

  <!-- Table 3 -->
  <div style="display: none;background-color: #f5f5f5; max-height: 400px; border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 33%; box-sizing: border-box; position: relative;">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">PURCHASE ORDER - BILLING OUTSTANDING</h4>
    <div id="table_two" style="margin-top: 10px;"></div>
  </div>

</div>

<!-- Wrapper for 3 Tables in One Row -->
<div style="display: flex; justify-content: space-between; gap: 20px; padding: 0 15px;flex-wrap: nowrap;">

  <!-- Table 4 -->
  <div style="display: none;background-color: #f5f5f5; max-height: 400px; border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 33%; box-sizing: border-box; position: relative;">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">PURCHASE ORDER O/S (PAYMENT) GR.</h4>
    <div id="table_three" style="margin-top: 10px;"></div>
  </div>

  <!-- Table 5 -->
  <div style="display: none;background-color: #f5f5f5; max-height: 400px; border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 33%; box-sizing: border-box; position: relative;">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">PAYMENT OUTSTANDING ON PURCHASE INVOICE</h4>
    <div id="table_f" style="margin-top: 10px;"></div>
  </div>
	<!-- Table 6 -->
  <div style="display: none;background-color: #f5f5f5; max-height: 400px; border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 33%; box-sizing: border-box; position: relative;">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;"></h4>
    <div id="" style="margin-top: 10px;"></div>
  </div>
</div>



<!-- Chart Wrapper with Padding -->
<div style="padding: 20px 15px;">
  <div style="display: flex; justify-content: space-between; gap: 20px; flex-wrap: nowrap;display:none">

    <!-- Chart 1 -->
    <div style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px;padding: 15px; width: calc((100% - 40px) / 3); box-sizing: border-box;">
      <h4 style="margin: 10px; text-align: center; background: white;">Sales Order O/S (Billing) - Services</h4>
      <div id="chart_scroll_wrapper_1" style="overflow-x: auto; text-align: center;">
        <div id="chart_1" style="min-width: 600px; margin: 0 auto; display: table;"></div>
      </div>
    </div>

    <!-- Chart 2 -->
    <div style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px;padding: 15px; width: calc((100% - 40px) / 3); box-sizing: border-box;">
      <h4 style="margin: 10px; text-align: center; background: white;">SO COLLECTION</h4>
      <div id="chart_scroll_wrapper_2" style="overflow-x: auto; text-align: center;">
        <div id="chart_2" style="min-width: 600px; margin: 0 auto; display: table;"></div>
      </div>
    </div>

    <!-- Chart 3 -->
    <div style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px;padding: 15px; width: calc((100% - 40px) / 3); box-sizing: border-box;">
      <h4 style="margin: 10px; text-align: center; background: white;">PO PAYMENT</h4>
      <div id="chart_scroll_wrapper_3" style="overflow-x: auto; text-align: center;">
        <div id="chart_3" style="min-width: 1000px; margin: 0 auto; display: table;"></div>
      </div>
    </div>

  </div>
</div>




<!-- Chart Row  -->
<div style="display: flex; justify-content: space-between; gap: 20px; padding: 0px 15px; flex-wrap: nowrap;">

  <!-- Chart 4 -->
  <div style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px;padding: 15px; width: calc((100% - 40px) / 3); box-sizing: border-box;display:none">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;">PO PAYMENT</h4>
    <div id="chart_scroll_wrapper_4" style="overflow-x: auto; text-align: center;">
      <div id="chart_4" style="min-width: 1000px; margin: 0 auto; display: table;"></div>
    </div>
  </div>

  <!-- Chart 5 -->
  <div style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px;padding: 15px; width: calc((100% - 40px) / 3); box-sizing: border-box;display:none">
    <h4 style="margin: 10px; text-align: center; background: white;">PI O/S</h4>
    <div id="chart_scroll_wrapper_5" style="overflow-x: auto; text-align: center;">
      <div id="chart_5" style="min-width: 800px; margin: 0 auto; display: table;"></div>
    </div>
  </div>

  <!-- Chart 6 -->
  <div style="background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px;padding: 15px; width: calc((100% - 40px) / 3); box-sizing: border-box;display:none">
    <h4 style="margin: 10px; text-align: center; background: white; position: sticky; top: 0; z-index: 1;"></h4>
    <div id="chart_scroll_wrapper_6" style="overflow-x: auto; text-align: center;">
      <div id="chart_6" style="min-width: 1000px; margin: 0 auto; display: table;"></div>
    </div>
  </div>

	</div>

	
	
		<div style="position: relative; padding: 0px 10px; text-align: center; line-height:1;">

			<div style="
				display:flex;
				justify-content:flex-end;
				align-items:center;
				margin:0;
				padding:0;
				height:auto;
			">

				<div id="overall_service_filter" style="width:200px; margin:0;"></div>

			</div>

		</div>

</div>

			<div class="active-customer-wrapper" style="display: none; background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
			<div class="dashboard-cards-finaince" style="display: flex; gap: 30px; flex-wrap: nowrap; overflow-x: auto; margin-bottom: 30px;">
				
				<div class="dashboard-card collection-card1"></div>
				<div class="dashboard-card receivable-card1"></div>
				<div class="dashboard-card tobill-card1"></div>
				<div class="dashboard-card todeliverbill-card1"></div>
				<div class="dashboard-card payable-card1"></div>
			</div>
			</div>
	<div style="background-color: #f5f5f5;display: flex;gap: 5px;padding-bottom: 10px;margin-top: -90px;margin-left: 15px;margin-right: 15px;border: 1px solid #ddd;border-radius: 8px;">
    
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



<br>
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
<br>









<div style="display: none; justify-content: space-between; gap: 20px; padding: 20px 15px; flex-wrap: nowrap;">

	<div id="rec-i-payment-wrapper" style="width:50%;margin: 40px 20px;border: 1px solid #ddd; border-radius: 8px;background-color: #f5f5f5;margin-left:20px;margin-right:20px;">
		<h4 style="margin-bottom: 15px;text-align:center;background-color:white;margin-top:20px">PAYMENT COLLECTION DETAILS ( RESOURCE ) </h4>
		<!-- 👇 Add your filters here -->
		<div id="rec-i-payment-filters" style="margin-bottom: 20px; display: flex; gap: 15px; flex-wrap: wrap;justify-content: flex-end;">
			<input type="date" id="payment-from-date" class="form-control" style="width: 160px;" placeholder="From Date">
			<input type="date" id="payment-to-date" class="form-control" style="width: 160px;" placeholder="To Date">
			<button class="btn btn-primary btn-sm" id="apply-payment-filter">Apply</button>
			<button id="download8-dashboard" class="btn btn-secondary">Download</button>
			<button id="download-dashboard" class="btn btn-secondary">Details</button>
	</div>

		<!-- 👇 Table container -->
		<div id="epnc-table" style="overflow: auto;max-height: 500px; border: 1px solid #ddd; padding: 10px;"></div>
	</div>

	<div id="epnc-wrapper" style="width:50%;margin: 40px 20px;border: 1px solid #ddd; border-radius: 8px;background-color: #f5f5f5;margin-left:20px;margin-right:20px;">
		<h4 style="margin-bottom: 15px;text-align:center;background-color:white;margin-top:20px"> Energy Point And Non Conformity  </h4>
			<div id="epnc-filters" style="margin-bottom: 20px; display: flex; gap: 15px; flex-wrap: wrap;justify-content: flex-end;">
				<input type="date" id="epnc-from-date" class="form-control" style="width: 160px;" placeholder="From Date">
				<input type="date" id="epnc-to-date" class="form-control" style="width: 160px;" placeholder="To Date">
				<button class="btn btn-primary btn-sm" id="apply-epnc-filter">Apply</button>
			</div>
		<!-- 👇 Table container -->
		<div id="epnc-table-content" style="overflow: auto;max-height: 500px; border: 1px solid #ddd; padding: 10px;"></div>
	</div>

</div>	


		`);




		
loadDashboardData();

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
	loadepnc();
	$(wrapper).on('click', '#apply-epnc-filter', function() {
		const from_date = $('#epnc-from-date').val() || null ;
		const to_date = $('#epnc-to-date').val() || null ;
		loadepnc(from_date, to_date);
	});	

	$('#epnc-table-content').html(`<div style="padding: 10px;text-align:center">EP NC details...</div>`);

	function loadepnc(from_date, to_date) {

	    frappe.call({
		    method: "teampro.teampro.page.finance.finance_dashboard.epnc_table",
			args: {
				from_date: from_date,
				to_date: to_date
			},
		    callback: function(r) {
			    if (r.message) {
				    $('#epnc-table-content').html(r.message);
			    } else {
				    $('#epnc-table-content').html(`<p>No data found.</p>`);
			    }
		    }
	    });
    
	}

	// frappe.call({
	// method: "teampro.teampro.page.finance_details.tfp_dashboard.get_order_booking_overall",
	// callback: function(r) {
	// 	const value = r.message || 0;

    //     // Get current month and year
    //     const now = new Date();
    //     const currentMonth = now.getMonth() + 1; // 1-12
    //     const currentYear = now.getFullYear();

    //     // Calculate current financial month number
    //     // April (4) is month 1, March (3) is month 12
    //     let financialMonth;
    //     if (currentMonth >= 4) {
    //         financialMonth = currentMonth - 3;
    //     } else {
    //         financialMonth = currentMonth + 9;
    //     }

    //     // Calculate average
    //     const avg = value / financialMonth;
	// 	const avg_value=Math.round(avg || 0);

    //     const formattedTotal = parseFloat(value).toLocaleString('en-IN', {
    //         style: 'currency',
    //         currency: 'INR',
    //         maximumFractionDigits: 0 
    //     });
	// 	let arrowSvg = `
	// 	<svg width="70" height="20" viewBox="0 0 60 40">
	// 		<path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
	// 			stroke="black" stroke-width="2" fill="none" 
	// 			stroke-linecap="round" stroke-linejoin="round" 
	// 			style="stroke-dasharray: 4,1;" />
	// 		<polygon points="57,10 52,0 58,0" fill="black"/>
	// 	</svg>`;

	// 			const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
	// 				maximumFractionDigits: 0 
	// 			});


	// 			// Inject HTML into wrapper
	// 			$(wrapper).find('.order-booking-card1').html(`
	// 				<div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:10px;">
	// 					<h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;white-space:nowrap;font-size:14px;">Order Booking HI</h3>
	// 					<div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
	// 					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
	// 					</div>
	// 					<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
	// 				</div>
	// 			`);
				
	// 		}
	// 	});

	frappe.call({
    method: "teampro.teampro.page.finance_details.tfp_dashboard.get_order_booking_overall",
    callback: function(r) {
        const data = r.message || {};
        const value = data.total || 0;
        const groups = data.groups || {};

        const now = new Date();
        const currentMonth = now.getMonth() + 1;
        let financialMonth = currentMonth >= 4 ? currentMonth - 3 : currentMonth + 9;

        function formatToLakhs(val) {
            return '₹' + (val / 100000).toFixed(2) + 'L';
        }

        const groupOrder = ["HRS", "ITS", "CMN", "TFP", "HRIT"];

        const serviceItems = groupOrder.map(key => {
		const val = groups[key] || 0;
		return `
			<div style="display:flex; align-items:center; padding:1px 0;">
				<span style="font-weight:bold; font-size:10px; color:black;">${key}:</span>
				<span style="font-size:10px; color:red; font-weight:bold; margin-left:1px;">${formatToLakhs(val)}</span>
			</div>
		`;
	});

	const gridHtml = `
		<div style="display:flex; justify-content:space-around; gap:15px; margin-top:5px;margin-left:-10px;">
			${serviceItems.slice(0, 3).join('')}
		</div>
		<div style="display:flex; justify-content:space-around; gap:0px; margin-top:5px;">
			${serviceItems.slice(3, 5).join('')}
		</div>
	`;	

        $(wrapper).find('.order-booking-card1').html(`
			<div  style="width:200px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">

				<h3 style="margin:0; text-align:center; margin-top:-20px; white-space:nowrap; font-size:16px;">
					Order Booking
				</h3>

				<div style="text-align:center; margin-top:8px;">
					<div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
						<span style="font-size:16px; font-weight:bold; color:green;">
							${formatToLakhs(value)}
						</span>
					</div>
				</div>

				<div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
					${gridHtml}
				</div>
			</div>
        `);
    }
});

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

// let overall_service_filter = add_filter('#overall_service_filter', {
// 	fieldtype: 'Link',
// 	options: 'Services',
// 	fieldname: 'overall_service',
// 	placeholder: 'Service'
// },load_overall_dashboard);
let closure_service_filter = add_filter('#closure_service_filter', {
	fieldtype: 'Link',
	options: 'Services',
	fieldname: 'closure_service',
	placeholder: 'Service'
}, load_closure_table);

let closure_am_filter = add_filter('#closure_am_filter', {
	fieldtype: 'Link',
	options: 'User',
	fieldname: 'closure_am',
	placeholder: 'AM'
}, load_closure_table);
let closure_dm_filter = add_filter('#closure_dm_filter', {
	fieldtype: 'Link',
	options: 'User',
	fieldname: 'closure_dm',
	placeholder: 'DM'
}, load_closure_table);


let service_filter = add_filter('#service_filter', {
	fieldtype: 'Link',
	options: 'Services',
	fieldname: 'service',
	placeholder: 'Service'
}, load_s_table);

let am_filter = add_filter('#am_filter', {
	fieldtype: 'Link',
	options: 'User',
	fieldname: 'am',
	placeholder: 'AM'
}, load_s_table);

let dm_filter = add_filter('#dm_filter', {
	fieldtype: 'Link',
	options: 'User',
	fieldname: 'dm',
	placeholder: 'DM'
}, load_s_table);
// Invoice
let invoice_service_filter = add_filter('#invoice_service_filter', {
	fieldtype: 'Link',
	options: 'Services',
	fieldname: 'invoice_service',
	placeholder: 'Service'
}, load_so_billing);

let invoice_am_filter = add_filter('#invoice_am_filter', {
	fieldtype: 'Link',
	options: 'User',
	fieldname: 'invoice_am',
	placeholder: 'AM'
}, load_so_billing);
let invoice_dm_filter = add_filter('#invoice_dm_filter', {
	fieldtype: 'Link',
	options: 'User',
	fieldname: 'invoice_dm',
	placeholder: 'DM'
}, load_so_billing);

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




	// frappe.call({
	// 	method: "teampro.teampro.page.finance_details.tfp_dashboard.get_turnover_overall",
	// 	callback: function(r) {
	// 		const data = r.message || {};
	// 		const value = data.total || 0;
	// 		const groups = data.groups || {};

	// 		const now = new Date();
	// 		const currentMonth = now.getMonth() + 1;
	// 		let financialMonth = currentMonth >= 4 ? currentMonth - 3 : currentMonth + 9;

	// 		function formatToLakhs(val) {
	// 			return '₹' + (val / 100000).toFixed(2) + 'L';
	// 		}
			
	// 		const serviceEntries = Object.entries(groups);
	// 		const serviceRows = serviceEntries.map(([key, val]) => `
	// 			<div style="display:flex; justify-content:space-between; align-items:center; padding:2px 4px;">
	// 				<span style="font-weight:bold; font-size:10px; color:black;">${key}:</span>
	// 				<span style="font-size:10px; color:red; font-weight:bold;">${formatToLakhs(val)}</span>
	// 			</div>
	// 		`).join('');

	// 		$(wrapper).find('.turnover-card1').html(`
	// 			<div class="card blink-border-name" style="width:180px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
					
	// 				<h3 style="margin:0; text-align:center;margin-top:-20px; white-space:nowrap; font-size:16px;">
	// 					Turnover
	// 				</h3>

	// 				<div style="text-align:center; margin-top:8px;">
	// 					<div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
	// 						<span  style="font-size:13px; font-weight:bold; color:green;">
	// 							${formatToLakhs(value)}
	// 						</span>
	// 					</div>
	// 				</div>

	// 				<div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px; display:grid; grid-template-columns:1fr 1fr; gap:4px;">
	// 					${serviceRows}
	// 				</div>

	// 			</div>
	// 		`);
	// 	}
	// });


	frappe.call({
    method: "teampro.teampro.page.finance_details.tfp_dashboard.get_turnover_overall",
    callback: function(r) {
        const data = r.message || {};
        const value = data.total || 0;
        const groups = data.groups || {};

        const now = new Date();
        const currentMonth = now.getMonth() + 1;
        let financialMonth = currentMonth >= 4 ? currentMonth - 3 : currentMonth + 9;

        function formatToLakhs(val) {
            return '₹' + (val / 100000).toFixed(2) + 'L';
        }

        const groupOrder = ["HRS", "ITS", "CMN", "TFP", "HRIT"];

        const serviceItems = groupOrder.map(key => {
            const val = groups[key] || 0;
            return `
                <div style="display:flex; align-items:center; gap:2px; padding:2px 0;">
                    <span style="font-weight:bold; font-size:10px; color:black; width:35px; text-align:right;margin-left:-5px;">${key}: </span>
                    <span style="font-size:10px; color:red; font-weight:bold; width:45px; text-align:left;">${formatToLakhs(val)}</span>
                </div>
            `;
        });

        const gridHtml = `
			<div style="display:flex; justify-content:space-around; gap:0px;margin-left:-25px;margin-top:5px;">
				${serviceItems.slice(0, 3).join('')}
			</div>
			<div style="display:flex; justify-content:space-around; gap:0px; margin-top:5px;">
				${serviceItems.slice(3, 5).join('')}
			</div>
		`;
        $(wrapper).find('.turnover-card1').html(`
			
            <div  style="width:200px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
                
                <h3 style="margin:0; text-align:center; margin-top:-20px; white-space:nowrap; font-size:16px;">
                    Turnover
                </h3>

                <div style="text-align:center; margin-top:8px;">
                    <div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
                        <span style="font-size:16px; font-weight:bold; color:green;">
                            ${formatToLakhs(value)}
                        </span>
                    </div>
                </div>

                <div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
                    ${gridHtml}
                </div>

            </div>
        `);
    }
});


	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_collection_value_overall",
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
			$(wrapper).find('.collection-card1').html(`
				<div class="display:none;card blink-border" style="display:none; width: 160px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">Collection</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
               <div style="display: none;font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.receivable_overall",
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
			$(wrapper).find('.receivable-card1').html(`
				<div class="display: none; card blink-border" style="width: 70px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:14px;">Receivable</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.to_bill_value_overall",
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
			$(wrapper).find('.tobill-card1').html(`
				<div class="display: none;card blink-border" style="width: 150px; padding: 15px; border-radius: 8px;">
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
		method: "teampro.teampro.page.finance_details.tfp_dashboard.to_deliver_bill_value_overall",
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
			$(wrapper).find('.todeliverbill-card1').html(`
				<div class="card blink-border" style="width: 168px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">To Deliver and </h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.payable_overall",
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
				$(wrapper).find('.payable-card1').html(`
					<div class="card blink-border" style="width: 160px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;font-size:17px;">Payable</h3>
						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;white-space:nowrap;">${formatted}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
            </div>
				`);
			}
		});
	// Replace the existing frappe.call for receivable_table_overall with:
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
	load_receivable_overall_table();
	// frappe.call({
	// 	method: 'teampro.teampro.page.finance_details.tfp_dashboard.tobill_table_overall',
	// 	// args: { from_date, to_date },
	// 	callback: function(r) {
	// 		if (r.message) {
	// 			$('#tobill-so-table-content1').html(r.message);
	// 		}
	// 		else {
	// 			$('#tobill-so-table-content1').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
	// 		}
	// 	}
	// });

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

load_tobill_overall_table();


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

load_ob_overall_table();
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


load_turnover_overall_table();
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

load_to_book_table();
load_payable_table();
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

	// frappe.call({
	// 	method: 'teampro.teampro.page.finance_details.tfp_dashboard.payable_table_overall',
	// 	// args: { from_date, to_date },
	// 	callback: function(r) {
	// 		if (r.message) {
	// 			$('#payable-so-table-content').html(r.message);
	// 		}
	// 		else {
	// 			$('#payable-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
	// 		}
	// 	}
	// });
	async function load_overall_dashboard() {

	let overall_service = overall_service_filter.get_value();

	let r = await frappe.call({
		method: "teampro.teampro.page.finance_details.tfp_dashboard.get_overall_dashboard_data_combined",
		args: {
			overall_service: overall_service
		}
	});

	let d = r.message;

	const financialMonth = getFinancialMonth();

	// CARDS
	renderCard_new('.order-booking-card1', 'Order Booking', d.order_booking, financialMonth, 160);
	renderCard_new('.turnover-card1', 'Turnover', d.turnover, financialMonth, 160);
	renderCard_new('.receivable-card1', 'Receivable', d.receivable, financialMonth, 150);
	renderCard_new('.tobill-card1', 'To Bill', d.to_bill, financialMonth, 150);
	renderCard_new('.todeliverbill-card1', 'To Deliver and Bill', d.to_deliver_bill, financialMonth, 168);
	renderCard_new('.payable-card1', 'Payable', d.payable, financialMonth, 140);

	// TABLES
	$('#ob-table').html(d.ob_table || noData());
	$('#to-table-content1').html(d.turnover_table || noData());
	$('#receivable-so-table-content1').html(d.receivable_table || noData());
	$('#tobill-so-table-content1').html(d.tobill_table || noData());
	$('#payable-so-table-content').html(d.payable_table || noData());
	$('#tb-table').html(d.to_book_table || noData());
	frappe.dom.unfreeze();
}

function getFinancialMonth() {

	const currentMonth = new Date().getMonth() + 1;

	return currentMonth >= 4
		? currentMonth - 3
		: currentMonth + 9;
}

function formatCurrency(value) {

	return parseFloat(value || 0).toLocaleString('en-IN', {
		style: 'currency',
		currency: 'INR',
		maximumFractionDigits: 0
	});
}

function renderCard_new(selector, title, value, financialMonth, width=160) {

	const avg = Math.round((value || 0) / financialMonth);

	const formattedTotal = formatCurrency(value);

	const formattedAvg = avg.toLocaleString('en-IN');

	$(wrapper).find(selector).html(`
		<div class="card blink-border"
			style="width:${width}px;padding:15px;border-radius:8px;">

			<h3 style="
				margin:0;
				text-align:center;
				font-size:17px;
				white-space:nowrap;
			">
				${title}
			</h3>

			<div style="
				font-size:20px;
				font-weight:bold;
				margin-top:10px;
				color:green;
				text-align:center;
			">
				${formattedTotal}
			</div>

			<div style="
				font-size:12px;
				text-align:center;
				color:red;
				margin-top:5px;
			">
				[${formattedAvg}]
			</div>

			<div style="
				font-size:10px;
				color:black;
				text-align:center;
			">
				[Avg]
			</div>
		</div>
	`);
}

function noData() {
	return `<div style="padding:10px;text-align:center">No data found</div>`;
}
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
	$(wrapper).on('click', '#download-tb', function () {

		const overall_service = tb_service_filter.get_value() || "";
		const account_manager = tb_am_filter.get_value() || "";
		const project_manager = tb_pm_filter.get_value() || "";

		const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_to_book_excel";

		window.location.href = frappe.request.url
			+ '?cmd=' + path
			+ '&overall_service=' + encodeURIComponent(overall_service)
			+ '&account_manager=' + encodeURIComponent(account_manager)
			+ '&project_manager=' + encodeURIComponent(project_manager);

	});

	// $(wrapper).on('click', '#download10-dashboard', function () {
	// 	const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_tobill_excel";
	// 	window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	// });

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
	// $(wrapper).on('click', '#download11-dashboard', function () {
	// 	const path = "teampro.teampro.page.finance_details.tfp_dashboard.download_payable_table1";
	// 	window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
	// });

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
	function renderCard(selector, title, value) {
			const now = new Date();
			const currentMonth = now.getMonth() + 1; // 1–12
			let financialMonth = currentMonth >= 4 ? currentMonth - 3 : currentMonth + 9;

			const avg = value / financialMonth;
			const avg_value = Math.round(avg || 0);

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
			$(wrapper).find(selector).html(`
				<div class="card-inner">
					<h3>${title}</h3>
					<div class="amount">${formatted}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;">[${formattedAvg}]
						</div>
						<div style="font-size: 10px;color:black;text-align: center;">[Avg]</div>
					</div>
			`);
	}
	
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_order_booking_rec",
		callback: r => renderCard('.order-booking-card2', 'Order Booking', r.message || 0)
	});
	
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_turnover_rec",
		callback: r => renderCard('.turnover-card2', 'Turnover', r.message || 0)
	});
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_collection_value_rec",
		callback: r => renderCard('.collection-card2', 'Collection', r.message || 0)
	});
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.rec_receivable",
		callback: r => renderCard('.receivable-card2', 'Receivable', r.message || 0)
	});
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.rec_to_bill_value",
		callback: r => renderCard('.tobill-card2', 'To Bill', r.message || 0)
	});
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.rec_to_deliver_bill_value",
		callback: r => renderCard('.todeliverbill-card2', 'To Deliver and Bill', r.message || 0)
	});
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.rec_payable",
		callback: r => renderCard('.payable-card2', 'Payable', r.message || 0)
	});
	frappe.call({
		method: 'jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.rec_receivable_table',
		callback: function(r) {
			if (r.message) {
				$('#receivable-so-table-content2').html(r.message);
			}
			else {
				$('#receivable-so-table-content2').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	frappe.call({
		method: 'jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.rec_tobill_table',
		callback: function(r) {
			if (r.message) {
				$('#tobill-so-table-content2').html(r.message);
			}
			else {
				$('#tobill-so-table-content2').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	frappe.call({
		method: 'jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.rec_payable_table',
		callback: function(r) {
			if (r.message) {
				$('#payable-so-table-content2').html(r.message);
			}
			else {
				$('#payable-so-table-content2').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	function renderCardFromMethod(selector, label, method, from_date = null, to_date = null) {
		frappe.call({
			method: method,
			args: from_date && to_date ? { from_date, to_date } : {},
			callback: function(r) {
				const value = r.message || 0;
				const formatted = parseFloat(value).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0
				});
				$(selector).html(`
					<div class="card-inner">
						<h3>${label}</h3>
						<div class="amount">${formatted}</div>
					</div>
				`);
			}
		});
	}
	function loadDashboardData(from_date = null, to_date = null) {
		const container = $('.dashboard-wrapper');
		renderCardFromMethod('.order-booking-card3', 'Order Booking', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it", from_date, to_date);
		renderCardFromMethod('.turnover-card3', 'Turnover', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_turnover_it", from_date, to_date);
		renderCardFromMethod('.collection-card3', 'Collection', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_collection_value_it", from_date, to_date);
		renderCardFromMethod('.receivable-card3', 'Receivable', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_receivable");
		renderCardFromMethod('.tobill-card3', 'To Bill', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_bill_value");
		renderCardFromMethod('.todeliverbill-card3', 'To Deliver and Bill', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_deliver_bill_value");
		renderCardFromMethod('.payable-card3', 'Payable', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_payable");
	}
	function loadOrderBooking1(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it",
			args: { from_date, to_date },
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
				const avg = value / financialMonth;
				const avg_value=Math.round(avg || 0);
				const formattedtotal = parseFloat(value).toLocaleString('en-IN', {
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
				$(wrapper).find('.order-booking-card3').html(`
					<div class="card-inner">
						<h3>Order Booking</h3>
						<div class="amount">${formattedtotal}</div>
	<div style="text-align:center; margin-top:5px;">
		<span style="color:red; font-weight:bold; display:block;">[${formattedAvg}]</span>
		<span style="display:inline-block; vertical-align:middle;">${arrowSvg}</span>
	</div>

					</div>
				`);
			}
		});
	}
	frappe.call({
			method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it",
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
                const avg = value / financialMonth;
                const avg_value=Math.round(avg || 0);

				const formattedtotal = parseFloat(value).toLocaleString('en-IN', {
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

				$(wrapper).find('.order-booking-card3').html(`
				<div class="card-inner">
					<h3>Order Booking</h3>
					<div class="amount">${formattedtotal}</div>
                
                <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);

			}
		});
	
	frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_turnover_it",
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
		    const avg_value1=Math.round(avg || 0);
			const formattedtotal1 = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
            const formattedAvg1 = parseFloat(avg_value1).toLocaleString('en-IN', {
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
			$(wrapper).find('.turnover-card3').html(`
				<div class="card-inner">
					<h3>Turnover</h3>
					<div class="amount">${formattedtotal1}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg1}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
                    
			`);
		}
	});
		
	frappe.call({
			method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_collection_value_it",
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
				const avg_value2=Math.round(avg || 0);
				const formattedtotal2 = parseFloat(value).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0
				});
				const formattedAvg2 = parseFloat(avg_value2).toLocaleString('en-IN', {
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
				$(wrapper).find('.collection-card3').html(`
					<div class="card-inner">
						<h3>Collection</h3>
						<div class="amount">${formattedtotal2}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg2}]
					</div>
					<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
				</div>
					
				`);
			}
	});
load_vm_sales();
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

load_retail_sales();
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
	
frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_receivable",
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
		    const avg_value3=Math.round(avg || 0);
			const formattedtotal3 = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
            const formattedAvg3 = parseFloat(avg_value3).toLocaleString('en-IN', {
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
			$(wrapper).find('.receivable-card3').html(`
				<div class="card-inner">
					<h3>Receivable</h3>
					<div class="amount">${formattedtotal3}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg3}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>

			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_bill_value",
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
		    const avg_value4=Math.round(avg || 0);
			const formattedtotal4 = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
            const formattedAvg4 = parseFloat(avg_value4).toLocaleString('en-IN', {
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
			$(wrapper).find('.tobill-card3').html(`
				<div class="card-inner">
					<h3>To Bill</h3>
					<div class="amount">${formattedtotal4}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg4}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_deliver_bill_value",
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
		    const avg_value5=Math.round(avg || 0);
			const formattedtotal5 = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
            const formattedAvg5 = parseFloat(avg_value5).toLocaleString('en-IN', {
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
			$(wrapper).find('.todeliverbill-card3').html(`
				<div class="card-inner">
					<h3>To Deliver and Bill</h3>
					<div class="amount">${formattedtotal5}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg5}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_payable",
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
		    const avg_value6=Math.round(avg || 0);
			const formattedtotal6 = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
            const formattedAvg6 = parseFloat(avg_value6).toLocaleString('en-IN', {
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
			$(wrapper).find('.payable-card3').html(`
				<div class="card-inner">
					<h3>Payable</h3>
					<div class="amount">${formattedtotal6}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg6}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);
		}
	});
	frappe.call({
		method: 'teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.it_receivable_table',
		callback: function(r) {
			$('#receivable-so-table-content3').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
		}
	});
	frappe.call({
		method: 'teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.it_payable_table',
		callback: function(r) {
			$('#payable-so-table-content3').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
		}
	});
	frappe.call({
		method: 'teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.it_tobill_table',
		callback: function(r) {
			$('#tobill-so-table-content3').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
		}
	});
	$(wrapper).on('click', '#fup-btn-apply', function() {
		const call_status = $('#fup-filter-call-status').val();
		const Lfrom_date = $('#fup-last-fdate').val();
		const Lto_date = $('#fup-last-tdate').val();
		const Nfrom_date = $('#fup-next-fdate').val();
		const Nto_date = $('#fup-next-tdate').val();
		loadfupfilter(call_status, Lfrom_date, Lto_date,Nfrom_date, Nto_date);
	})		

		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_order_booking",
			callback: function(r) {
				const total = r.message?.total || 0;
				const avg = r.message?.average || 0;

				const formattedTotal = parseFloat(total).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0
				});

				const formattedAvg = parseFloat(avg).toLocaleString('en-IN', {
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
				$(wrapper).find('.order-booking-card4').html(`
					<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">Order Booking</h3>
						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
				`);

			}
		});
		frappe.call({
		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_turnover",
		callback: function(r) {
			const total1 = r.message?.total || 0;
			const avg1 = r.message?.average || 0;
			const formatted = parseFloat(total1).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
			const formattedAvg1 = parseFloat(avg1).toLocaleString('en-IN', {
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
			$(wrapper).find('.turnover-card4').html(`
				<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">Turnover</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg1}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
				</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_collection_value",
		callback: function(r) {
			const total2 = r.message?.total || 0;
			const avg2 = r.message?.average || 0;
			const formattedtotal2 = parseFloat(total2).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
			const formattedAvg2 = parseFloat(avg2).toLocaleString('en-IN', {
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
			$(wrapper).find('.collection-card4').html(`
				<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">Collection</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedtotal2}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg2}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
			`);
		}
	});
	frappe.call({
		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_receivable",
		callback: function(r) {
			const total3 = r.message?.total || 0;
			const avg3 = r.message?.average || 0;
			const formattedtotal3 = parseFloat(total3).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
				
			});
			const formattedAvg3 = parseFloat(avg3).toLocaleString('en-IN', {
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
			$(wrapper).find('.receivable-card4').html(`
				<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">Receivable</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedtotal3}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg3}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
			`);
		}
	});
	frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_to_bill_value",
			callback: function(r) {
				const total4 = r.message?.total || 0;
					const avg4 = r.message?.average || 0;
					const formattedtotal4 = parseFloat(total4).toLocaleString('en-IN', {
						style: 'currency',
						currency: 'INR',
						maximumFractionDigits: 0 
						
					});
					const formattedAvg4 = parseFloat(avg4).toLocaleString('en-IN', {
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
				$(wrapper).find('.tobill-card4').html(`
					<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;font-size:17px;">To Bill</h3>
						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedtotal4}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg4}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
				`);
			}
		});
		frappe.call({
		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_to_deliver_bill_value",
		callback: function(r) {
			const total5 = r.message?.total || 0;
			const average5 = r.message?.average || 0;

			const formattedTotal5 = parseFloat(total5).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
			});

			const formattedAvg5 = parseFloat(average5).toLocaleString('en-IN', {
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
			$(wrapper).find('.todeliverbill-card4').html(`
				<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">To Deliver and Bill</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal5}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg5}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
			`);
		}
	});
	frappe.call({
		method: 'teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_tobill_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#tobill-so-table-content4').html(r.message);
			}
			else {
				$('#tobill-so-table-content4').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});

	frappe.call({
		method: 'teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_receivable_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#receivable-so-table-content4').html(r.message);
			}
			else {
				$('#receivable-so-table-content4').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	$(wrapper).on('click', '#apply-rs-filter', function() {
		const from_date = $('#rs-from-date').val() || null ;
		const to_date = $('#rs-to-date').val() || null ;
		loadOrderBooking4(from_date, to_date);
		loadturnover4(from_date, to_date);
		loadtcollection4(from_date, to_date);
		loadtreceivable4(from_date, to_date)
		loadtobill4(from_date, to_date);
		loadtodeliverbill4(from_date, to_date);
	});
	
	function loadOrderBooking4(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_order_booking",
			args: { from_date, to_date},
			callback: function(r) {
				
				const total = r.message?.total || 0;
				const avg = r.message?.average || 0;

				const formattedTotal = parseFloat(total).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0
				});

				const formattedAvg = parseFloat(avg).toLocaleString('en-IN', {
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
				$(wrapper).find('.order-booking-card4').html(`
					<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">Order Booking</h3>
						<div style="font-size: 25px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
					</div>
				`);
			}
		});
	}
	function loadturnover4(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_turnover",
			args: { from_date, to_date},
			callback: function(r) {
				const total1 = r.message?.total || 0;
				const avg1 = r.message?.average || 0;
				const formatted = parseFloat(total1).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0
					
				});
				const formattedAvg1 = parseFloat(avg1).toLocaleString('en-IN', {
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
					$(wrapper).find('.turnover-card4').html(`
						<div class="card blink-border" style="width:200px; padding: 15px; border-radius: 8px;">
							<h3 style="margin: 0;text-align:center">Turnover</h3>
							<div style="font-size: 25px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
							<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg1}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
				`);
			}
		});
	}
	function loadtcollection4(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.get_collection_value",
			args: { from_date, to_date },
			callback: function(r) {
				const total2 = r.message?.total || 0;
				const avg2 = r.message?.average || 0;
				const formattedtotal2 = parseFloat(total2).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0 
					
				});
				const formattedAvg2 = parseFloat(avg2).toLocaleString('en-IN', {
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
				$(wrapper).find('.collection-card4').html(`
					<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Collection</h3>
						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedtotal2}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg2}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
				`);
			}
		});
	}
	function loadtreceivable4(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_receivable",
			args: {
			from_date: $('#rs-from-date').val() || null,
			to_date: $('#rs-to-date').val() || null,
			},
			callback: function(r) {
				const total3 = r.message?.total || 0;
				const avg3 = r.message?.average || 0;
				const formattedtotal3 = parseFloat(total3).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0 
					
				});
				const formattedAvg3 = parseFloat(avg3).toLocaleString('en-IN', {
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
				$(wrapper).find('.receivable-card4').html(`
					<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center;font-size:17px;">Receivable</h3>
						<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedtotal3}</div>
						<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg3}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
				`);
			}
		});
	} 	
	function loadtobill4(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_to_bill_value",
		args: {
			from_date,
			to_date
		},
		callback: function(r) {
			console.log("👉 To Bill API Response:", r);

			const total4 = r.message?.total || 0;
			const average4 = r.message?.average || 0;

			const formattedTotal4 = parseFloat(total4).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0 
			});

			const formattedAvg4 = parseFloat(average4).toLocaleString('en-IN', {
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

			$(wrapper).find('.tobill-card4').html(`
				<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">To Bill</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal4}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg4}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
			`);
		}
	});
}
	function loadtodeliverbill4(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.relationship_and_sal.relationship_and_sal.rs_to_deliver_bill_value",
			args: { from_date, to_date },
			callback: function(r) {
				const total5 = r.message?.total || 0;
				const average5 = r.message?.average || 0;

				const formattedTotal5 = parseFloat(total5).toLocaleString('en-IN', {
					style: 'currency',
					currency: 'INR',
					maximumFractionDigits: 0 
				});

				const formattedAvg5 = parseFloat(average5).toLocaleString('en-IN', {
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
				$(wrapper).find('.todeliverbill-card4').html(`
					<div class="card blink-border" style="width: 200px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;font-size:17px;">To Deliver and Bill</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formattedTotal5}</div>
					<div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg5}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
					</div>
				`);
			}
		});
	}
	$(wrapper).on('click', '#apply-tfp-filter1', function() {
		const from_date = $('#tfp-from-date1').val();  
		const to_date = $('#tfp-to-date1').val();
		loadOrderBooking1(from_date, to_date);
		loadturnover1(from_date, to_date);
		loadtcollection1(from_date, to_date);
		// loadpayable(from_date, to_date);
		// loadreceivable(from_date, to_date);
		// loadreceivabletable(from_date, to_date);
		loadpayabletable1(from_date, to_date);
		loadtotalsoqty1(from_date, to_date);
			if (from && to) {
			load_order_booking_table(from, to);
		}
	});
	function loadOrderBooking1(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_order_booking_overall",
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
				$(wrapper).find('.order-booking-card1').html(`
					<div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:10px;">
						<h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;white-space:nowrap;font-size:14px;">Order Booking</h3>
						<div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
	function loadturnover1(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_turnover_overall",
			args: { from_date, to_date },
			callback: function(r) {
				const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
				$(wrapper).find('.turnover-card1').html(`
					<div class="card blink-border" style="width: 250px; padding: 15px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Turnover</h3>
						<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
	function loadtcollection1(from_date = null, to_date = null) {
		frappe.call({
			method: "teampro.teampro.page.finance_details.tfp_dashboard.get_collection_value_overall",
			args: { from_date, to_date },
			callback: function(r) {
				const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
				
			});
				// const count = r.message || 0;
				$(wrapper).find('.collection-card1').html(`
					<div class="card blink-border" style="width: 250px; padding: 20px; border-radius: 8px;">
						<h3 style="margin: 0;text-align:center">Collection</h3>
						<div style="font-size: 32px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
					</div>
				`);
			}
		});
	}
	$(wrapper).on('click', '#apply-tfp-filter2', function () {
		const from_date = $('#tfp-from-date2').val();
		const to_date = $('#tfp-to-date2').val();
		loadOrderBooking2(from_date, to_date);
		loadturnover2(from_date, to_date);
		loadtcollection2(from_date, to_date);
	});
	function loadOrderBooking2(from_date = null, to_date = null) {
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_order_booking_rec",
		args: { from_date, to_date },
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
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
			$(wrapper).find('.order-booking-card2').html(`
				<div class="card-inner">
					<h3>Order Booking</h3>
					<div class="amount">${formatted}</div>
                    <div style="font-size: 12px; text-align: center; color: #555;">[Avg: ${avg_value}]</div>
				</div>
			`);
		}
	});
}

	function loadturnover2(from_date = null, to_date = null) {
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_turnover_rec",
		args: { from_date, to_date },
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
			$(wrapper).find('.turnover-card2').html(`
				<div class="card-inner">
					<h3>Turnover</h3>
					<div class="amount">${formatted}</div>
				</div>
			`);
		}
	});
}

	function loadtcollection2(from_date = null, to_date = null) {
	frappe.call({
		method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_collection_value_rec",
		args: { from_date, to_date },
		callback: function(r) {
			const value = r.message || 0;
			const formatted = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
			$(wrapper).find('.collection-card2').html(`
				<div class="card-inner">
					<h3>Collection</h3>
					<div class="amount">${formatted}</div>
				</div>
			`);
		}
	});
	}
	$(wrapper).on('click', '#apply-tfp-filter3', function () {
		const from_date = $('#tfp-from-date3').val();
		const to_date = $('#tfp-to-date3').val();
		loadOrderBooking3(from_date, to_date);
		loadturnover3(from_date, to_date);
		loadtcollection3(from_date, to_date);
	});
	function loadOrderBooking3(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it",
		args: { from_date, to_date },
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
            const avg = value / financialMonth;
		    const avg_value=Math.round(avg || 0);
			const formattedtotal = parseFloat(value).toLocaleString('en-IN', {
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
			$(wrapper).find('.order-booking-card3').html(`
				<div class="card-inner">
					<h3>Order Booking</h3>
					<div class="amount">${formattedtotal}</div>
<div style="text-align:center; margin-top:5px;">
    <span style="color:red; font-weight:bold; display:block;">[${formattedAvg}]</span>
    <span style="display:inline-block; vertical-align:middle;">${arrowSvg}</span>
</div>

				</div>
			`);
		}
	});
}
function loadturnover3(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_turnover_it",
		args: { from_date, to_date },
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
		    const avg_value1=Math.round(avg || 0);
			const formattedtotal1 = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
            const formattedAvg1 = parseFloat(avg_value1).toLocaleString('en-IN', {
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
			$(wrapper).find('.turnover-card3').html(`
				<div class="card-inner">
					<h3>Turnover</h3>
					<div class="amount">${formattedtotal1}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg1}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
                    

			`);
		}
	});
}
function loadtcollection3(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_collection_value_it",
		args: { from_date, to_date },
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
		    const avg_value2=Math.round(avg || 0);
			const formattedtotal2 = parseFloat(value).toLocaleString('en-IN', {
				style: 'currency',
				currency: 'INR',
				maximumFractionDigits: 0
			});
            const formattedAvg2 = parseFloat(avg_value2).toLocaleString('en-IN', {
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
			$(wrapper).find('.collection-card3').html(`
				<div class="card-inner">
					<h3>Collection</h3>
					<div class="amount">${formattedtotal2}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg2}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>

			`);
		}
	});
}




	
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
  function formatInLakhsOrCrores(value) {

	value = parseFloat(value || 0);

	if (value >= 10000000) {

		return `₹ ${(value / 10000000).toFixed(2)} Cr`;

	} else if (value >= 100000) {

		return `₹ ${(value / 100000).toFixed(2)} L`;

	} else if (value >= 1000) {

		return `₹ ${(value / 1000).toFixed(2)} K`;

	} else {

		return `₹ ${value.toFixed(2)}`;
	}
}
//click
// 	function loadCard(fromDate = null, toDate = null) {
//     frappe.call({
//         method: "teampro.teampro.page.finance.finance_dashboard.card",
//         args: {
//             from_date: fromDate,
//             to_date: toDate
//         },
//         callback: function(r) {
//             const value = r.message || 0;
//             const inLakhs = value / 100000;
//             const formatted = `₹ ${inLakhs.toFixed(2)}L`;

//             $('.order-booking-card').html(`
//                 <div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:10px;">
//                     <h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;white-space:nowrap;font-size:14px;">Receivable</h3>
//                     <div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
//                 </div>
//             `);
//         }
//     });
// }
function loadCard(fromDate = null, toDate = null, overallService = null) {
    frappe.call({
        method: "teampro.teampro.page.finance.finance_dashboard.card",
        args: {
            from_date: fromDate,
            to_date: toDate,
            overall_service: overallService
        },
        callback: function(r) {
            const data = r.message || {};
            const value = data.total || 0;
            const groups = data.groups || {};

            function formatToLakhs(val) {
                return '₹' + (val / 100000).toFixed(2) + 'L';
            }

            const groupOrder = ["HRS", "ITS", "CMN", "TFP", "HRIT"];

            const serviceItems = groupOrder.map(key => {
			const val = groups[key] || 0;
			return `
				<div style="display:flex; align-items:center; padding:1px 0;">
					<span style="font-weight:bold; font-size:10px; color:black;">${key}:</span>
					<span style="font-size:10px; color:red; font-weight:bold; margin-left:1px;">${formatToLakhs(val)}</span>
				</div>
			`;
		});

		const gridHtml = `
			<div style="display:flex; justify-content:space-around; gap:15px; margin-top:5px;margin-left:-22px;">
				${serviceItems.slice(0, 3).join('')}
			</div>
			<div style="display:flex; justify-content:space-around; gap:0px; margin-top:5px;">
				${serviceItems.slice(3, 5).join('')}
			</div>
		`;	

            $('.order-booking-card').html(`
				<div  style="width:200px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
             
                <h3 style="margin:0; text-align:center; margin-top:-20px; white-space:nowrap; font-size:16px;">
                    Receivable
                </h3>

                <div style="text-align:center; margin-top:8px;">
                    <div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
                        <span style="font-size:16px; font-weight:bold; color:green;">
                            ${formatToLakhs(value)}
                        </span>
                    </div>
                </div>

                <div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
                    ${gridHtml}
                </div>
				</div>
            `);
        }
    });
}

// Initial load without filter
loadCard();

// Filter on Apply button click
document.getElementById("apply-tfp-filter").addEventListener("click", function () {
    const fromDate = document.getElementById("tfp-from-date").value;
    const toDate = document.getElementById("tfp-to-date").value;
    loadCard(fromDate, toDate);
});

  //card
// function load_billing_outstanding_card() {
//     const from_date = document.getElementById("tfp-from-date")?.value;
//     const to_date = document.getElementById("tfp-to-date")?.value;

//     const args = {};
//     if (from_date && to_date) {
//         args.from_date = from_date;
//         args.to_date = to_date;
//     }

//     frappe.call({
//         method: "teampro.teampro.page.finance.finance_dashboard.card_1",
//         args: args,
//         callback: function (r) {
//             const value = r.message || 0;
//             const formatted = formatInLakhsOrCrores(value);
//             $(wrapper).find('.turnover-card').html(`
//                 <div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:9px;">
//                     <h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;font-size:14px;">To Bill</h3>
//                     <div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
//                 </div>
//             `);
//         }
//     });
// }

// function load_billing_outstanding_card() {
//     const from_date = document.getElementById("tfp-from-date")?.value;
//     const to_date = document.getElementById("tfp-to-date")?.value;

//     const args = {};
//     if (from_date && to_date) {
//         args.from_date = from_date;
//         args.to_date = to_date;
//     }

//     frappe.call({
//         method: "teampro.teampro.page.finance.finance_dashboard.card_1",
//         args: args,
//         callback: function(r) {
//             const data = r.message || {};
//             const value = data.total || 0;
//             const groups = data.groups || {};
//             const clr = data.clr || 0;
//             const cln = data.cln || 0;

//             function formatToLakhs(val) {
//                 return '₹' + (val / 100000).toFixed(2) + 'L';
//             }

//             function formatToCrores(val) {
//                 return '₹' + (val / 10000000).toFixed(2) + 'Cr';
//             }

//             const groupOrder = ["HRS", "ITS", "CMN", "TFP", "HRIT", "CLR", "CLN"];

// 			const serviceItems = groupOrder.map(key => {
// 				let val = 0;
// 				if (key === "CLR") val = clr;
// 				else if (key === "CLN") val = cln;
// 				else val = groups[key] || 0;

// 				return `
// 					<div style="display:flex; align-items:center; gap:2px; padding:2px 0;">
// 						<span style="font-weight:bold; font-size:10px; color:black; width:35px; text-align:right;">${key}:</span>
// 						<span style="font-size:10px; color:red; font-weight:bold; width:45px; text-align:left;">${formatToLakhs(val)}</span>
// 					</div>
// 				`;
// 			});

// 			const gridHtml = `
// 				<div style="display:flex; justify-content:space-around; gap:1px; margin-top:5px;margin-left:-35px;">
// 					${serviceItems.slice(0, 3).join('')}
// 				</div>
// 				<div style="display:flex; justify-content:space-around; gap:0px; margin-top:5px;margin-left:-37px;">
// 					${serviceItems.slice(3, 6).join('')}
// 				</div>
// 				<div style="display:flex; justify-content:space-around; gap:0px; margin-top:5px;">
// 					${serviceItems.slice(6, 7).join('')}
// 				</div>
// 			`;

//             $(wrapper).find('.turnover-card').html(`
//             <div  style="width:220px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
//                 <h3 style="margin:0; text-align:center; margin-top:-20px; white-space:nowrap; font-size:16px;">
//                     To Bill
//                 </h3>

//                 <div style="text-align:center; margin-top:8px;">
//                     <div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
//                         <span style="font-size:16px; font-weight:bold; color:green;">
//                             ${formatToLakhs(value)}
//                         </span>
//                     </div>
//                 </div>

//                 <div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
//                     ${gridHtml}
//                 </div>
// 				</div>
//             `);
//         }
//     });
// }


function load_billing_outstanding_card() {
    const from_date = document.getElementById("tfp-from-date")?.value;
    const to_date = document.getElementById("tfp-to-date")?.value;

    const args = {};
    if (from_date && to_date) {
        args.from_date = from_date;
        args.to_date = to_date;
    }

    frappe.call({
        method: "teampro.teampro.page.finance.finance_dashboard.card_1",
        args: args,
        callback: function(r) {
            const data = r.message || {};
            const value = data.total || 0;
            const groups = data.groups || {};
            const clr = data.clr || 0;
            const cln = data.cln || 0;

            function formatToLakhs(val) {
                return '₹' + (val / 100000).toFixed(2) + 'L';
            }

            function formatToCrores(val) {
                return '₹' + (val / 10000000).toFixed(2) + 'Cr';
            }

            const groupOrder = ["HRS", "ITS", "CMN", "TFP", "HRIT", "CLR", "CLN"];

			const serviceItems = groupOrder.map(key => {
				let val = 0;
				if (key === "CLR") val = clr;
				else if (key === "CLN") val = cln;
				else val = groups[key] || 0;

				return `
					<div style="display:flex; align-items:center; gap:2px; padding:2px 0;">
						<span style="font-weight:bold; font-size:10px; color:black; width:35px; text-align:right;">${key}:</span>
						<span style="font-size:10px; color:red; font-weight:bold; width:45px; text-align:left;">${formatToLakhs(val)}</span>
					</div>
				`;
			});

			const gridHtml = `
				<div style="display:flex; justify-content:space-around; gap:1px; margin-top:5px;margin-left:-35px;">
					${serviceItems.slice(0, 3).join('')}
				</div>
				<div style="display:flex; justify-content:space-around; gap:0px; margin-top:5px;margin-left:-37px;">
					${serviceItems.slice(3, 6).join('')}
				</div>
				
			`;

            $(wrapper).find('.turnover-card').html(`
            <div  style="width:220px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
                <h3 style="margin:0; text-align:center; margin-top:-15px; white-space:nowrap; font-size:16px;">
                    To Bill
                </h3>

                <div style="text-align:center; margin-top:8px;margin-top:0px;margin-bottom:20px;">
                    <div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
                        <span style="font-size:19px; font-weight:bold; color:green;">
                            ${formatToLakhs(value)}
                        </span>
                    </div>
                </div>

                <div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
                    ${gridHtml}
                </div>
				</div>
            `);
        }
    });
}

// Call on page load
load_billing_outstanding_card();

// Call on filter apply
document.getElementById("apply-tfp-filter").addEventListener("click", load_billing_outstanding_card);

  //card_2
  function load_card_2() {
    const from_date = document.getElementById("tfp-from-date")?.value;
    const to_date = document.getElementById("tfp-to-date")?.value;

    const args = {};
    if (from_date && to_date) {
        args.from_date = from_date;
        args.to_date = to_date;
    }

    frappe.call({
        method: "teampro.teampro.page.finance.finance_dashboard.card_2",
        args: args,
        callback: function (r) {
            const value = r.message || 0;
            const formatted = formatInLakhsOrCrores(value);
            $(wrapper).find('.collection-card').html(`
                <div class="card blink-border-name" style=" width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:8px;">
                    <h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;white-space:nowrap;font-size:14px;">To Bill(C)</h3>
                    <div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
                </div>
            `);
        }
    });
}

function load_all_cards() {
    load_billing_outstanding_card(); // card_1
    load_card_2();                   // card_2
    // You can add more: load_card_3(), load_table_data(), etc.
}

// Initial load
load_all_cards();

// On filter apply
document.getElementById("apply-tfp-filter").addEventListener("click", load_all_cards);


function load_card_3() {
    const from_date = document.getElementById("tfp-from-date")?.value;
    const to_date = document.getElementById("tfp-to-date")?.value;

    const args = {};
    if (from_date && to_date) {
        args.from_date = from_date;
        args.to_date = to_date;
    }

    frappe.call({
        method: "teampro.teampro.page.finance.finance_dashboard.card_3",
        args: args,
        callback: function (r) {
            const value = r.message || 0;
            const formatted = formatInLakhsOrCrores(value);
            document.querySelector('.receivable-card').innerHTML = `
                <div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:10px;">
                    <h3 style="width: 80px; hight: 80px;margin: 0; text-align: center;font-size:14px;white-space:nowrap;">To Bill(CLR)</h3>
                    <div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">
                        ${formatted}
                    </div>
                </div>
            `;
        }
    });
}
// Initial load
load_card_3();

// On Apply button click
document.getElementById("apply-tfp-filter").addEventListener("click", load_card_3);









//table
function load_s_table(from_date = null, to_date = null) {
	frappe.call({
		method: 'teampro.teampro.page.finance.finance_dashboard.s_table',
		args: {
			from_date: from_date,
			to_date: to_date,
			service: service_filter.get_value(),
			am: am_filter.get_value(),
			dm: dm_filter.get_value()
		},
		
		callback: function(r) {
			if (r.message) {
				$('#receivable-so-table-content').html(r.message);
				frappe.dom.unfreeze();
			} else {
				$('#receivable-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
				frappe.dom.unfreeze();
			}
		}
	});
}

// Load all data (default) on page load
load_s_table();

// On date filter Apply button
$('#apply-tfp-filter').on('click', function() {
	let from_date = $('#tfp-from-date').val();
	let to_date = $('#tfp-to-date').val();
	load_s_table(from_date, to_date);
});

function load_so_billing(from_date = null, to_date = null) {
	frappe.call({
		method: 'teampro.teampro.page.finance.finance_dashboard.so_billing',
		args: {
			from_date: from_date,
			to_date: to_date,
			service: invoice_service_filter.get_value(),
			am: invoice_am_filter.get_value(),
			dm: invoice_dm_filter.get_value()
		},
		callback: function(r) {
			if (r.message) {
				$('#tobill-so-table-content').html(r.message);
			} else {
				$('#tobill-so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
			frappe.dom.unfreeze();
		}
	});
}

// On page load (default)
load_so_billing();
load_closure_table();
// On filter apply
$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_so_billing(from_date, to_date);
});
// table_3
function load_so_collection(from_date = null, to_date = null) {
    frappe.call({
        method: 'teampro.teampro.page.finance.finance_dashboard.so_collection',
        args: {
            from_date: from_date,
            to_date: to_date
        },
        callback: function (r) {
            if (r.message) {
                $('#rec-so-table-content').html(r.message);
            } else {
                $('#rec-so-table-content').html(`
                    <div style="padding: 10px; background: #f0f0f0; text-align: center;">
                        No data found
                    </div>`);
            }
        }
    });
}

$(document).ready(function () {
    load_so_collection();
});

$('#apply-tfp-filter').on('click', function () {
    const from_date = $('#tfp-from-date').val();
    const to_date = $('#tfp-to-date').val();
    load_so_collection(from_date, to_date);
});



// table_4
function load_closure_table() {
frappe.call({
		method: 'teampro.teampro.page.finance.finance_dashboard.so_payment',
		args: {
			service: closure_service_filter.get_value(),
			am: closure_am_filter.get_value(),
			dm:closure_dm_filter.get_value()
		},
		callback: function(r) {
			if (r.message) {
				$('#so-table-content').html(r.message);
			}
			else {
				$('#so-table-content').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
			frappe.dom.unfreeze();
		}
	});
}


function load_fund_card(from_date = null, to_date = null) {
    frappe.call({
        method: "teampro.teampro.page.finance.finance_dashboard.fund_card",
        args: { from_date, to_date },
        callback: function (r) {
            const data = r.message || {};
            const bank  = data.bank  || 0;
            const cash  = data.cash  || 0;
            const sfd   = data.sfd   || 0;
            const lfd   = data.lfd   || 0;
            const total = data.total || 0;

            function formatToLakhs(val) {
                return '₹' + (val / 100000).toFixed(2) + 'L';
            }

            const items = [
                { label: "BANK", val: bank },
                { label: "CASH", val: cash },
                { label: "SFD",  val: sfd  },
                { label: "LFD",  val: lfd  },
            ];

            const serviceItems = items.map(item => `
                <div style="display:flex; align-items:center; gap:2px; padding:2px 0;">
                    <span style="font-weight:bold; font-size:10px; color:black; width:35px; text-align:right;">${item.label}:</span>
                    <span style="font-size:10px; color:red; font-weight:bold; width:45px; text-align:left;">${formatToLakhs(item.val)}</span>
                </div>
            `);

            // 2 + 2 layout
            const gridHtml = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:2px; margin-top:5px;">
                    ${serviceItems.join('')}
                </div>
            `;

            $(wrapper).find('.amount').html(`
                <div  style="width:180px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
                    <h3 style="margin:0; text-align:center;margin-top:-20px; font-size:14px; white-space:nowrap;">Fund</h3>
                    <div style="text-align:center; margin-top:8px;">
                        <div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
                            <span style="font-size:16px; font-weight:bold; color:green;">${formatToLakhs(total)}</span>
                        </div>
                    </div>
                    <div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
                        ${gridHtml}
                    </div>
                </div>
            `);
        }
    });
}

	// cards-bank
	function load_bank_balance(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.in_bank",
		args: {
			from_date: from_date,
			to_date: to_date
		},
		callback: function (r) {
			const value = r.message || 0;
			const formatted = formatInLakhsOrCrores(value);
			$(wrapper).find('.bank').html(`
				<div class="card blink-border" style="width: 230px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">Bank</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
}

load_bank_balance();
load_fund_card();

$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_bank_balance(from_date, to_date);
});




	// cards-cash
	function load_cash_balance(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.in_cash",
		args: {
			from_date: from_date,
			to_date: to_date
		},
		callback: function (r) {
			const value = r.message || 0;
			const formatted = formatInLakhsOrCrores(value);
			$(wrapper).find('.cash').html(`
				<div class="card blink-border" style="width: 230px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">Cash</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
}

load_cash_balance();

$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_cash_balance(from_date, to_date);
});



// cards-SFD
	function load_sfd_balance(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.sfd",
		args: {
			from_date: from_date,
			to_date: to_date
		},
		callback: function (r) {
			const value = r.message || 0;
			const formatted = formatInLakhsOrCrores(value);
			$(wrapper).find('.sfd').html(`
				<div class="card blink-border" style="width: 230px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">SFD</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
}

load_sfd_balance();

$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_sfd_balance(from_date, to_date);
});

// cards-LFD
	function load_lfd_balance(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.lfd",
		args: {
			from_date: from_date,
			to_date: to_date
		},
		callback: function (r) {
			const value = r.message || 0;
			const formatted = formatInLakhsOrCrores(value);
			$(wrapper).find('.lfd').html(`
				<div class="card blink-border" style="width: 230px; padding: 15px; border-radius: 8px;">
					<h3 style="margin: 0;text-align:center;white-space:nowrap;font-size:17px;">LFD</h3>
					<div style="font-size: 20px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
}

load_lfd_balance();

$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_lfd_balance(from_date, to_date);
});

	

	// cards-po
// 	function load_po_balance(from_date = null, to_date = null) {
// 	frappe.call({
// 		method: "teampro.teampro.page.finance.finance_dashboard.po",
// 		args: {
// 			from_date: from_date,
// 			to_date: to_date
// 		},
// 		callback: function (r) {
// 			const value = r.message || 0;
// 			const formatted = formatInLakhsOrCrores(value);
// 			$(wrapper).find('.po').html(`
// 				<div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:10px;">
// 					<h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;white-space:nowrap;font-size:14px;">To Book</h3>
// 					<div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
// 				</div>
// 			`);
// 		}
// 	});
// }



function load_po_balance(from_date = null, to_date = null) {
    frappe.call({
        method: "teampro.teampro.page.finance.finance_dashboard.po",
        args: { from_date, to_date },
        callback: function (r) {
            const data = r.message || {};
            const value = data.total || 0;
            const groups = data.groups || {};
            const cln = data.cln || 0;

            function formatToLakhs(val) {
                return '₹' + (val / 100000).toFixed(2) + 'L';
            }

            const groupOrder = ["HRS", "ITS", "CMN", "TFP", "HRIT", "CLN"];

            const serviceItems = groupOrder.map(key => {
                const val = key === "CLN" ? cln : (groups[key] || 0);
                return `
                    <div style="display:flex; align-items:center; gap:2px; padding:2px 0;">
                        <span style="font-weight:bold; font-size:10px; color:black; width:35px; text-align:right;">${key}:</span>
                        <span style="font-size:10px; color:red; font-weight:bold; width:45px; text-align:left;">${formatToLakhs(val)}</span>
                    </div>
                `;
            });

            // 3 + 3 layout (row1: HRS ITS CMN, row2: TFP HR-IT CLN)
            const gridHtml = `
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:2px; margin-top:5px;margin-left:-30px;">
                    ${serviceItems.join('')}
                </div>
            `;

            $(wrapper).find('.po').html(`
                <div  style="width:220px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
                    <h3 style="margin:0; text-align:center; margin-top:-20px; font-size:14px; white-space:nowrap;">To Book</h3>
                    <div style="text-align:center; margin-top:8px;">
                        <div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
                            <span style="font-size:16px; font-weight:bold; color:green;">${formatToLakhs(value)}</span>
                        </div>
                    </div>
                    <div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
                        ${gridHtml}
                    </div>
                </div>
            `);
        }
    });
}


load_po_balance();

$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_po_balance(from_date, to_date);
});

// cards-po_payment
	function load_po_payment_balance(from_date = null, to_date = null) {
	frappe.call({
		method: "teampro.teampro.page.finance.finance_dashboard.po_payment",
		args: {
			from_date: from_date,
			to_date: to_date
		},
		callback: function (r) {
			const value = r.message || 0;
			const formatted = formatInLakhsOrCrores(value);
			$(wrapper).find('.po_payment').html(`
				<div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:10px;">
					<h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;white-space:nowrap;font-size:14px;">To Book(P)</h3>
					<div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
				</div>
			`);
		}
	});
}

load_po_payment_balance();

$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_po_payment_balance(from_date, to_date);
});
	// cards-po_out
// 	function load_po_out_balance(from_date = null, to_date = null) {
// 	frappe.call({
// 		method: "teampro.teampro.page.finance.finance_dashboard.po_out",
// 		args: {
// 			from_date: from_date,
// 			to_date: to_date
// 		},
// 		callback: function (r) {
// 			const value = r.message || 0;
// 			const formatted = formatInLakhsOrCrores(value);
// 			$(wrapper).find('.po_out').html(`
// 				<div class="card blink-border-name" style="width: 100px; hight: 100px; padding: 12px; border-radius: 8px;margin-top:0px;margin-left:10px;">
// 					<h3 style="width: 80px; hight: 80px; margin: 0;text-align:center;white-space:nowrap;font-size:14px;">Payable</h3>
// 					<div class="card blink-border" style="font-size: 12px; font-weight: bold; margin-top: 10px; color: green; text-align: center;">${formatted}</div>
// 				</div>
// 			`);
// 		}
// 	});
// }

function load_po_out_balance(from_date = null, to_date = null) {
    frappe.call({
        method: "teampro.teampro.page.finance.finance_dashboard.po_out",
        args: { from_date, to_date },
        callback: function (r) {
            const data = r.message || {};
            const value = data.total || 0;
            const groups = data.groups || {};

            function formatToLakhs(val) {
                return '₹' + (val / 100000).toFixed(2) + 'L';
            }

            const groupOrder = ["HRS", "ITS", "CMN", "TFP", "HRIT"];

            const serviceItems = groupOrder.map(key => `
                <div style="display:flex; align-items:center; gap:2px; padding:2px 0;">
                    <span style="font-weight:bold; font-size:10px; color:black; width:35px; text-align:right;">${key}:</span>
                    <span style="font-size:10px; color:red; font-weight:bold; width:45px; text-align:left;">${formatToLakhs(groups[key] || 0)}</span>
                </div>
            `);

            const gridHtml = `
				<div style="display:flex; justify-content:space-around; gap:1px; margin-top:5px;margin-left:-30px;">
					${serviceItems.slice(0, 3).join('')}
				</div>
				<div style="display:flex; justify-content:space-around; gap:0px; margin-top:5px;">
					${serviceItems.slice(3, 5).join('')}
				</div>
			`;

            $(wrapper).find('.po_out').html(`
                <div style="width:210px; padding:12px; border-radius:8px; margin-top:0px; margin-left:10px;">
                    <h3 style="margin:0; text-align:center; margin-top:-20px;font-size:14px; white-space:nowrap;">Payable</h3>
                    <div style="text-align:center; margin-top:8px;">
                        <div style="display:inline-block; border-radius:50px; background:#e8f5e9; padding:4px 14px;">
                            <span style="font-size:16px; font-weight:bold; color:green;">${formatToLakhs(value)}</span>
                        </div>
                    </div>
                    <div style="margin-top:10px; border-top:1px solid #eee; padding-top:6px;">
                        ${gridHtml}
                    </div>
                </div>
            `);
        }
    });
}

load_po_out_balance();

$('#apply-tfp-filter').on('click', function () {
	const from_date = $('#tfp-from-date').val();
	const to_date = $('#tfp-to-date').val();
	load_po_out_balance(from_date, to_date);
});
// 	// // FUND IN HAND _table
	frappe.call({
		method: 'teampro.teampro.page.finance.finance_dashboard.in_table',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#so-table').html(r.message);
			}
			else {
				$('#so-table').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	
	

		frappe.call({
		method: 'teampro.teampro.page.finance.finance_dashboard.table_two',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#table_two').html(r.message);
			}
			else {
				$('#table_two').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
	frappe.call({
		method: 'teampro.teampro.page.finance.finance_dashboard.table_three',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#table_three').html(r.message);
			}
			else {
				$('#table_three').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
		frappe.call({
		method: 'teampro.teampro.page.finance.finance_dashboard.out_amount',
		// args: { from_date, to_date },
		callback: function(r) {
			if (r.message) {
				$('#table_f').html(r.message);
			}
			else {
				$('#table_f').html(`<div style="padding: 10px;text-align:center">No data found</div>`);
			}
		}
	});
// Chart 

frappe.call({
    method: 'teampro.teampro.page.finance.finance_dashboard.chart',
    callback: function(r) {
        const data = r.message || [];

        const labels = data.map(d => d.Services);
        const values = data.map(d => Number(d.to_be_billed)); 

        new frappe.Chart("#chart_1", {
            title: "To Be Billed",
            data: {
                labels: labels,
                datasets: [
                    {
                        name: "To Be Billed",
                        values: values
                    }
                ]
            },
            type: 'donut',
            height: 280,
            colors: ['#4caf50', '#f44336', '#ff9800', '#2196f3', '#9c27b0', '#607d8b'] 
        });
        setTimeout(() => {
            const el = document.getElementById("chart_scroll_wrapper_1");
            if (el) {
                el.scrollLeft = (el.scrollWidth - el.clientWidth) / 2;
            }
        }, 300);
    }
});

// chart -2
frappe.call({
    method: 'teampro.teampro.page.finance.finance_dashboard.chart_2',
    callback: function(r) {
        const data = r.message || [];

        // Extract labels and values
        const labels = data.map(d => d.Services);
        const values = data.map(d => Number(d.to_be_billed)); 

        // Create the donut chart
        new frappe.Chart("#chart_2", {
            title: "To Be Billed",
            data: {
                labels: labels,
                datasets: [
                    {
                        name: "To Be Billed",
                        values: values
                    }
                ]
            },
            type: 'donut',
            height: 280,
            colors: ['#00bcd4', '#8bc34a', '#ffc107', '#e91e63', '#3f51b5', '#795548']
        });

        // Auto scroll to center
        setTimeout(() => {
            const el = document.getElementById("chart_scroll_wrapper_2");
            if (el) {
                el.scrollLeft = (el.scrollWidth - el.clientWidth) / 2;
            }
        }, 300);
    }
});

frappe.call({
    method: 'teampro.teampro.page.finance.finance_dashboard.chart_3',
    callback: function(r) {
        const data = r.message || [];
        const labels = data.map(d => d.Services);
        const values = data.map(d => Number(d.to_be_billed)); 

        new frappe.Chart("#chart_3", {
            title: "To Be Billed",
            data: {
                labels: labels,
                datasets: [
                    {
                        name: "To Be Billed",
                        values: values
                    }
                ]
            },
            type: 'donut',
            height: 280,
            colors: ['#673ab7', '#03a9f4', '#cddc39', '#ff5722', '#009688', '#ffeb3b']
        });
        setTimeout(() => {
            const el = document.getElementById("chart_scroll_wrapper_3");
            if (el) {
                el.scrollLeft = (el.scrollWidth - el.clientWidth) / 2;
            }
        }, 300);
    }
});



frappe.call({
    method: 'teampro.teampro.page.finance.finance_dashboard.chart_4',
    callback: function(r) {
        const data = r.message || [];
        const labels = data.map(d => d.Service);
        const values = data.map(d => Number(d.to_be_billed_value));

        new frappe.Chart("#chart_4", {
            title: "To Be Billed",
            data: {
                labels: labels,
                datasets: [
                    {
                        name: "To Be Billed",
                        values: values
                    }
                ]
            },
            type: 'donut',
            height: 280,
            colors: ['#3f51b5', '#e91e63', '#4caf50', '#ff9800', '#9c27b0', '#607d8b']
        });
		setTimeout(() => {
            const el = document.getElementById("chart_scroll_wrapper_4");
            if (el) {
                el.scrollLeft = (el.scrollWidth - el.clientWidth) / 2;
            }
        }, 300);
    }
});

frappe.call({
    method: 'teampro.teampro.page.finance.finance_dashboard.chart_5',
    callback: function(r) {
        const data = r.message || [];
        const labels = data.map(d => d.Service);
        let values = data.map(d => d.outstanding_amount);
		

        new frappe.Chart("#chart_5", {
            title: "To Be Billed (Outstanding)",
            data: {
                labels: labels,
                datasets: [
                    {
                        name: "Outstanding",
                        values: values
                    }
                ]
            },
            type: 'donut',
            height: 280,
            colors: ['#3f51b5', '#e91e63', '#4caf50', '#ff9800', '#9c27b0', '#607d8b']
        });
		setTimeout(() => {
            const el = document.getElementById("chart_scroll_wrapper_5");
            if (el) {
                el.scrollLeft = (el.scrollWidth - el.clientWidth) / 2;
            }
        }, 300);
    }
});

loadPaymentCollectionDetailsonload();


document.addEventListener("DOMContentLoaded", function () {

		const fromDateInput = document.getElementById("payment-from-date");
		const toDateInput = document.getElementById("payment-to-date");

		const today = new Date();
		const sevenDaysAgo = new Date();
		sevenDaysAgo.setDate(today.getDate() - 7);

		fromDateInput.value = sevenDaysAgo.toISOString().split("T")[0];
		toDateInput.value = today.toISOString().split("T")[0];

		loadPaymentCollectionDetails();
	});

	document.getElementById("apply-payment-filter").addEventListener("click", loadPaymentCollectionDetails);

	async function loadPaymentCollectionDetails() {
		const from_date = document.getElementById("payment-from-date").value;
		const to_date = document.getElementById("payment-to-date").value;
		const wrapper = document.getElementById("rec-i-payment-table");
		wrapper.innerHTML = "<p>Loading...</p>";

		if (!from_date || !to_date) {
			wrapper.innerHTML = "<p>Please select both From and To date.</p>";
			return;
		}

		try {
			const res = await frappe.call({
				method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_payment_collection_details",
				args: { from_date, to_date }
			});

			const data = res.message || [];
			if (data.length === 0) {
				wrapper.innerHTML = "<p>No records found.</p>";
				return;
			}

			let html = `
				<table style="width:100%; border-collapse: collapse; background:#fff;">
  <thead style="background:#1E0C6F; color: #fff;">

						<tr>
                        <th style="border: 1px solid #ccc; padding: 8px;">S.No</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Code</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Name</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Department</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Role</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Collection</th>
							<th style="border: 1px solid #ccc; padding: 8px;"background:#1E0C6F; color: #fff;text-align:center">Net</th>
						</tr>
					</thead>
					<tbody>
			`;

			data.forEach((row, index) => {
	const isEven = index % 2 === 0;
	const rowStyle = isEven ? 'background: #f9f9f9;' : 'background: #ffffff;';

	html += `
		<tr style="${rowStyle}">
			<td style="text-align:center">${index + 1}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:left;">${row.employee_code}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:left;">${row.employee_name}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:left;">${row.department || "-"}</td>
			<td style="border: 1px solid #ccc; padding: 8px;">${row.role}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:right;">${(row.collection_value || 0).toLocaleString('en-IN', { style: 'currency', currency: 'INR' })}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:right;">${(row.net_collection || 0).toLocaleString('en-IN', { style: 'currency', currency: 'INR' })}</td>
		</tr>
	`;
});


			html += "</tbody></table>";
			wrapper.innerHTML = html;
		} catch (err) {
			console.error("Error loading data:", err);
			wrapper.innerHTML = "<p>Error loading data.</p>";
		}
	}

async function loadPaymentCollectionDetailsonload() {
		const from_date = document.getElementById("payment-from-date").value;
		const to_date = document.getElementById("payment-to-date").value;
		const wrapper = document.getElementById("rec-i-payment-table");
		wrapper.innerHTML = "<p>Loading...</p>"

		
		try {
			const res = await frappe.call({
				method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_payment_collection_details",
				args: { from_date, to_date }
			});

			const data = res.message || [];
			if (data.length === 0) {
				wrapper.innerHTML = "<p>No records found.</p>";
				return;
			}

			let html = `
				<table style="width:100%; border-collapse: collapse; background:#fff;">
					<thead style="background:#1E0C6F; color: #fff;">
						<tr>
                            <th>S#</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Code</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Name</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Department</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Role</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Collection</th>
							<th style="border: 1px solid #ccc; padding: 8px;background:#1E0C6F; color: #fff;text-align:center">Net</th>
						</tr>
					</thead>
					<tbody>
			`;

			data.forEach((row, index) => {
	const isEven = index % 2 === 0;
	const rowStyle = isEven ? 'background: #f9f9f9;' : 'background: #ffffff;';

	html += `
		<tr style="${rowStyle}">
			<td style="text-align:center">${index + 1}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:left;">${row.employee_code}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:left;">${row.employee_name}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:left;">${row.department || "-"}</td>
			<td style="border: 1px solid #ccc; padding: 8px;">${row.role}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:right;">₹${Number((row.collection_value || 0).toFixed(0)).toLocaleString('en-IN')}</td>
			<td style="border: 1px solid #ccc; padding: 8px; text-align:right;">₹${Number((row.net_collection || 0).toFixed(0)).toLocaleString('en-IN')}</td>
		</tr>
	`;
});


			html += "</tbody></table>";
			wrapper.innerHTML = html;
		} catch (err) {
			console.error("Error loading data:", err);
			wrapper.innerHTML = "<p>Error loading data.</p>";
		}
}

$(wrapper).on('click', '#download8-dashboard', function () {
	const from_date = $('#payment-from-date').val();
	const to_date = $('#payment-to-date').val();

	const path = "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.download_payment_excel";
	const base = frappe.request.url;
	const full_url = `${base}?cmd=${path}&from_date=${from_date}&to_date=${to_date}`;

	window.location.href = full_url;
});
$(wrapper).on('click', '#download-dashboard', function () {
	const from_date = $('#payment-from-date').val();
	const to_date = $('#payment-to-date').val();

	const path = "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.download_payment_details_excel";
	const base = frappe.request.url;
	const full_url = `${base}?cmd=${path}&from_date=${from_date}&to_date=${to_date}`;

	window.location.href = full_url;
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

}


// }