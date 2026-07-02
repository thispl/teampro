frappe.pages['hr-&-admin'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});
	page.set_title("HR & Admin");
	frappe.breadcrumbs.add('TEAMPRO');
    $(page.body).append(`
        <div id="epnc-wrapper" style="width:50%;margin:40px 20px;border:1px solid #ddd;border-radius:8px;background-color:#f5f5f5;">
            <h4 style="margin-bottom:15px;text-align:center;background-color:white;margin-top:20px">
                Energy Point And Non Conformity
            </h4>

            <div id="epnc-filters" style="margin-bottom:20px;display:flex;gap:15px;flex-wrap:wrap;justify-content:flex-end;padding:10px;">
                <input type="date" id="epnc-from-date" class="form-control" style="width:160px;">
                <input type="date" id="epnc-to-date" class="form-control" style="width:160px;">
                <button class="btn btn-primary btn-sm" id="apply-epnc-filter">
                    Apply
                </button>
            </div>

            <div id="epnc-table-content"
                 style="overflow:auto;max-height:500px;border:1px solid #ddd;padding:10px;">
            </div>
        </div>
    `);

    load_epnc_data();
};

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
		    method: "teampro.teampro.page.hr_&_admin.hr_&_admin.epnc_table",
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