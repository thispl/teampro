frappe.pages['target-monitor'].on_page_load = function (wrapper) {
	frappe.breadcrumbs.add("HR");
	let me = this;
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Target Monitor',
		single_column: true
	});

	let data = 0;
	let d = new Date();
	let month = d.getMonth() + 1;
	let year = d.getFullYear();

	page.main.html('')
	frappe.xcall(
		'teampro.teampro.page.target_monitor.target_monitor.get_sc_value',
		{
			month: month,
			year: year,
		}
	).then(sc_value => {
		total_sc = sc_value[0] - sc_value[1]
		total = getFormatted(sc_value[0])
		total_at = getFormatted(sc_value[1])
		total_sr = sc_value[2]
		as_data = sc_value[3]
		api_data = sc_value[4]
		sp_data = sc_value[5]
		sbmk_data = sc_value[6]
		const monthNames = ["January", "February", "March", "April", "May", "June",
		"July", "August", "September", "October", "November", "December"
		];
		const d = new Date();
		month_name = monthNames[d.getMonth()] 
		total_sc = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(total_sc)
		as_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data['at_monthly'])
		as_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data['total_value'])
		as_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data['d'])
		api_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data['at_monthly'])
		api_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data['total_value'])
		api_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data['d'])
		sp_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data['at_monthly'])
		sp_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data['total_value'])
		sp_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data['d'])
		sbmk_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data['at_monthly'])
		sbmk_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data['total_value'])
		sbmk_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data['d'])
		$(frappe.render_template('target_monitor', { total_sc: total_sc,total: total, total_at: total_at, total_sr: total_sr,as_data: as_data,api_data: api_data, sp_data: sp_data,sbmk_data: sbmk_data ,month_name:month_name})).appendTo(page.main)
		// console.log(sc_value[0])
	});
	let getFormatted = function (value) {
		return Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(value);
	}
	
	frappe.xcall(
		'teampro.teampro.page.target_monitor.target_monitor.get_sc_value_ft',
		{
			month: month,
			year: year,
		}
	).then(sc_value => {
		as_data_ft = sc_value[0]
		api_data_ft = sc_value[1]
		sp_data_ft = sc_value[2]
		sbmk_data_ft = sc_value[3]
		as_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data_ft['ft_monthly'])
		as_data_ft['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data_ft['total_value'])
		as_data_ft['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data_ft['d'])
		api_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data_ft['ft_monthly'])
		api_data_ft['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data_ft['total_value'])
		api_data_ft['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data_ft['d'])
		sp_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data_ft['ft_monthly'])
		sp_data_ft['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data_ft['total_value'])
		sp_data_ft['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data_ft['d'])
		sbmk_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data_ft['ft_monthly'])
		sbmk_data_ft['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data_ft['total_value'])
		sbmk_data_ft['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data_ft['d'])
		$(frappe.render_template('target_monitor', { as_data_ft: as_data_ft,api_data_ft: api_data_ft, sp_data_ft: sp_data_ft,sbmk_data_ft: sbmk_data_ft })).appendTo(page.main)
		// console.log(sc_value)
	});

	frappe.xcall(
		'teampro.teampro.page.target_monitor.target_monitor.get_sc_value_bt',
		{
			month: month,
			year: year,
		}
	).then(sc_value => {
		as_data_bt = sc_value[0]
		api_data_bt = sc_value[1]
		sp_data_bt = sc_value[2]
		sbmk_data_bt = sc_value[3]
		as_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data_bt['bt_monthly'])
		as_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data_bt['total_value'])
		as_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(as_data_bt['d'])
		
		api_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data_bt['bt_monthly'])
		api_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data_bt['total_value'])
		api_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(api_data_bt['d'])
		
		sp_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data_bt['bt_monthly'])
		sp_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data_bt['total_value'])
		sp_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sp_data_bt['d'])
		
		sbmk_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data_bt['bt_monthly'])
		sbmk_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data_bt['total_value'])
		sbmk_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
		maximumFractionDigits: 0, }).format(sbmk_data_bt['d'])
		$(frappe.render_template('target_monitor', { as_data_bt: as_data_bt,api_data_bt: api_data_bt, sp_data_bt: sp_data_bt,sbmk_data_bt:sbmk_data_bt})).appendTo(page.main)
		console.log(sc_value)
	});


}
