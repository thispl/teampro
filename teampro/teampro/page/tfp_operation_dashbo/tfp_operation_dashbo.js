frappe.pages['tfp-operation-dashbo'].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'TFP Operation Dashboard',
        single_column: true
    });
    frappe.breadcrumbs.add('TEAMPRO');


    // Custom CSS
    const style = document.createElement('style');
    
   style.innerHTML = `
	.dashboard-wrapper {
    background-color: #f5f5f5;
    background-image: none; /* Remove existing background image if any */
}
		<style>
	
}


	`;
    document.head.appendChild(style);

    // HTML Structure
    $(wrapper).html(`
		<div class="dashboard-wrapper">
        <div style="margin-top: 30px;">
		<div style="position: relative; padding: 10px; text-align: center;">
				<h2 style="font-weight: bold; margin: 0;">TFP OPERATION DASHBOARD</h2>
				<div id="current-datetime" style="font-size: 16px; color: #666; margin-top: 5px;"></div>
            <!-- PACKING PLAN -->
            <div id="tfp-so-table" style="max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-top: 30px; position: relative;text-align:center">
				<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0px;text-align:center">PACKING PLAN (SALES ORDER)</h4>
					<div style="position: absolute; top: 10px; right: 10px; z-index: 1;">
						<button id="download-dashboard" class="btn btn-secondary">Download</button>
					</div>
					<div id="tfp-so-table-content" style="margin-top: 10px;"></div>
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
			
		</div>
		</div>
        <div id="tfp-stock-table-third" style="flex: 1; min-width: 100px; max-height: 400px; overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; padding: 10px; position: relative;">
						<h4 style="position: sticky; top: 0; background: white; z-index: 1; margin: 0; padding: 0;text-align:center">Packing Details</h4>
			<div id="tfp-stock-table-content-packing1" style="margin-top: 20px;"></div>
		</div>
        </div>
		</div>
    `);

    // Time Update
    function updateDateTime() {
        const now = new Date();
        const dateStr = now.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        const timeStr = now.toLocaleTimeString();
        if (document.getElementById('current-datetime')) {
            document.getElementById('current-datetime').innerHTML = `${dateStr} | ${timeStr}`;
        }
    }
    updateDateTime();
    setInterval(updateDateTime, 1000);

    // Events
    $(wrapper).on('click', '#refresh-dashboard', () => location.reload());

    $(wrapper).on('click', '#download-dashboard', function () {
        const path = "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.download_tfp_plan_excel";
        window.location.href = repl(frappe.request.url + '?cmd=%(cmd)s', { cmd: path });
    });

    // Data Loads
    frappe.call({
        //  method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_plan_new",
        // method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_plan_update",
        method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_plan_update_new",
        callback: r => $('#tfp-so-table-content').html(r.message || '<p>No data</p>')
    });
    // frappe.call({
    //     method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_schedule",
    //     callback: r => $('#tfp-so-table-dn-content').html(r.message || '<p>No data</p>')
    // });
    frappe.call({
        // method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_schedule_new",
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

        }
    }
        // callback: r => $('#tfp-so-table-dn-content').html(r.message || '<p>No data</p>')
    });
    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.get_packed_dn_summary_html",
        callback: r => $('#tfp-so-table-dn-packed-content').html(r.message || '<p>No data</p>')
    });
    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.get_packed_dn_summary_dispatched_html",
        callback: r => $('#tfp-so-table-dn-dispatched-content').html(r.message || '<p>No data</p>')
    });
    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_stock_html",
        callback: r => $('#tfp-stock-table-content').html(r.message || '<p>No data</p>')
    });
    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_vm_stock_html",
        callback: r => $('#second-stock-table-content').html(r.message || '<p>No data</p>')
    });
    frappe.call({
        method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_stores_product",
        callback: r => $('#tfp-stock-table-content-packing').html(r.message || '<p>No data</p>')
    });
    frappe.call({
         method: "teampro.teampro.page.finance_details.tfp_dashboard.get_tfp_plan_html_schedule_new",
        callback: r => $('#tfp-stock-table-content-packing1').html(r.message || '<p>No data</p>')
       
    });
};

