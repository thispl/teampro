frappe.pages['target-monitor'].on_page_load = function (wrapper) {
	frappe.breadcrumbs.add("HR");
	let me = this;
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Target Monitor',
		single_column: true
	});
	page.main.html('')

	let d = new Date();
	const monthNames = ["January", "February", "March", "April", "May", "June",
		"July", "August", "September", "October", "November", "December"
	];
	month = monthNames[d.getMonth()]
	year = d.getFullYear();

	frappe.xcall(
		'teampro.teampro.page.target_monitor.target_monitor.get_ct_ft',
	).then(r => {
		var total_achieved = fmt_money(Math.round(r[0][0]['achieved'] + r[1][0]['achieved'] + r[2][0]['achieved'] + r[3][0]['achieved']))
		var total_achv = Math.round(r[0][0]['achieved'] + r[1][0]['achieved'] + r[2][0]['achieved'] + r[3][0]['achieved'])
		var total_target = fmt_money(Math.round(r[0][0]['ct'] + r[1][0]['ct'] + r[2][0]['ct'] + r[3][0]['ct']))
		var total_tar = Math.round(r[0][0]['ct'] + r[1][0]['ct'] + r[2][0]['ct'] + r[3][0]['ct'])
		var total_yta = fmt_money(total_achv - total_tar,0)
		var total_sr = Math.round((total_achv/total_tar)*100,2)

		var as_data = r[0]
		as_data["ct_sr"] = Math.round((r[0][0]['achieved']/r[0][0]['ct'])*100)
		as_data["ft_sr"] = Math.round((r[0][0]['achieved']/r[0][0]['ft'])*100)
		as_data['ct'] = fmt_money(Math.round(r[0][0]['ct']))
		as_data['ft'] = fmt_money(Math.round(r[0][0]['ft']))
		as_data['achieved'] = fmt_money(Math.round(r[0][0]['achieved']))
		as_data['ct_yta'] = fmt_money(Math.round(r[0][0]['ct_yta']))
		as_data['ft_yta'] = fmt_money(Math.round(r[0][0]['ft_yta']))
		console.log(as_data)

		var api_data = r[1]
		api_data["ct_sr"] = Math.round((r[1][0]['achieved']/r[1][0]['ct'])*100)
		api_data["ft_sr"] = Math.round((r[1][0]['achieved']/r[1][0]['ft'])*100)
		api_data['ct'] = fmt_money(Math.round(r[1][0]['ct']))
		api_data['ft'] = fmt_money(Math.round(r[1][0]['ft']))
		api_data['achieved'] = fmt_money(Math.round(r[1][0]['achieved']))
		api_data['ct_yta'] = fmt_money(Math.round(r[1][0]['ct_yta']))
		api_data['ft_yta'] = fmt_money(Math.round(r[1][0]['ft_yta']))
		console.log(api_data)

		var sp_data = r[2][0]
		sp_data["ct_sr"] = Math.round((r[2][0]['achieved']/r[2][0]['ct'])*100)
		sp_data["ft_sr"] = Math.round((r[2][0]['achieved']/r[2][0]['ft'])*100)
		sp_data['ct'] = fmt_money(Math.round(r[2][0]['ct']))
		sp_data['ft'] = fmt_money(Math.round(r[2][0]['ft']))
		sp_data['achieved'] = fmt_money(Math.round(r[2][0]['achieved']))
		sp_data['ct_yta'] = fmt_money(Math.round(r[2][0]['ct_yta']))
		sp_data['ft_yta'] = fmt_money(Math.round(r[2][0]['ft_yta']))
		

		var sbmk_data = r[3][0]
		sbmk_data["ct_sr"] = Math.round((r[3][0]['achieved']/r[3][0]['ct'])*100)
		sbmk_data["ft_sr"] = Math.round((r[3][0]['achieved']/r[3][0]['ft'])*100)
		sbmk_data['ct'] = fmt_money(Math.round(r[3][0]['ct']))
		sbmk_data['ft'] = fmt_money(Math.round(r[3][0]['ft']))
		sbmk_data['achieved'] = fmt_money(Math.round(r[3][0]['achieved']))
		sbmk_data['ct_yta'] = fmt_money(Math.round(r[3][0]['ct_yta']))
		sbmk_data['ft_yta'] = fmt_money(Math.round(r[3][0]['ft_yta']))

		$(frappe.render_template('target_monitor', { total_achieved: total_achieved, total_target: total_target, total_yta: total_yta, total_sr: total_sr, as_data: as_data, api_data: api_data, sp_data: sp_data, sbmk_data: sbmk_data, month_name: month, year: year })).appendTo(page.main)
	})

	// frappe.xcall(
	// 	'teampro.teampro.page.target_monitor.target_monitor.get_ft',
	// ).then(r => {
	// 	console.log(r[0][0]["ft"])
	// 	$(frappe.render_template('target_monitor', { total_sc: total_sc, total: total, total_at: total_at, total_sr: total_sr, as_data: r[0][0]["ft"], api_data: r[1][0], sp_data: r[2][0], sbmk_data: r[3][0], month_name: month, year: year })).appendTo(page.main)
	// })




	// frappe.xcall(
	// 	'teampro.teampro.page.target_monitor.target_monitor.get_sc_value',
	// 	{
	// 		month: month,
	// 		year: year,
	// 	}
	// ).then(sc_value => {
	// 	total_sc = sc_value[0] - sc_value[1]
	// 	total = getFormatted(sc_value[0])
	// 	total_at = getFormatted(sc_value[1])
	// 	total_sr = sc_value[2]
	// 	as_data = sc_value[3]
	// 	api_data = sc_value[4]
	// 	sp_data = sc_value[5]
	// 	sbmk_data = sc_value[6]
	// 	const monthNames = ["January", "February", "March", "April", "May", "June",
	// 	"July", "August", "September", "October", "November", "December"
	// 	];
	// 	const d = new Date();
	// 	month_name = monthNames[d.getMonth()]
	// 	year = d.getFullYear();
	// 	total_sc = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(total_sc)
	// 	as_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(as_data['at_monthly'])
	// 	as_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(as_data['total_value'])
	// 	as_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(as_data['d'])
	// 	api_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(api_data['at_monthly'])
	// 	api_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(api_data['total_value'])
	// 	api_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(api_data['d'])
	// 	sp_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sp_data['at_monthly'])
	// 	sp_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sp_data['total_value'])
	// 	sp_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sp_data['d'])
	// 	sbmk_data['at_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sbmk_data['at_monthly'])
	// 	sbmk_data['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sbmk_data['total_value'])
	// 	sbmk_data['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sbmk_data['d'])
	// 	$(frappe.render_template('target_monitor', { total_sc: total_sc,total: total, total_at: total_at, total_sr: total_sr,as_data: as_data,api_data: api_data, sp_data: sp_data,sbmk_data: sbmk_data ,month_name:month_name, year:year})).appendTo(page.main)
	// });
	// let getFormatted = function (value) {
	// 	return Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(value);
	// }

	// frappe.xcall(
	// 	'teampro.teampro.page.target_monitor.target_monitor.get_sc_value_ft',
	// 	{
	// 		month: month,
	// 		year: year,
	// 	}
	// ).then(sc_value => {
	// 	as_data_ft = sc_value[0]
	// 	api_data_ft = sc_value[1]
	// 	sp_data_ft = sc_value[2]
	// 	sbmk_data_ft = sc_value[3]
	// 	as_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(as_data_ft['ft_monthly'])
	// 	as_data_ft['total_value'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(as_data_ft['total_value'])
	// 	as_data_ft['d'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(as_data_ft['d'])
	// 	api_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(api_data_ft['ft_monthly'])
	// 	api_data_ft['total_value'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(api_data_ft['total_value'])
	// 	api_data_ft['d'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(api_data_ft['d'])
	// 	sp_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(sp_data_ft['ft_monthly'])
	// 	sp_data_ft['total_value'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(sp_data_ft['total_value'])
	// 	sp_data_ft['d'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(sp_data_ft['d'])
	// 	sbmk_data_ft['ft_monthly'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(sbmk_data_ft['ft_monthly'])
	// 	sbmk_data_ft['total_value'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(sbmk_data_ft['total_value'])
	// 	sbmk_data_ft['d'] = Intl.NumberFormat('en-IN', {
	// 		style: 'currency', currency: 'INR', minimumFractionDigits: 0,
	// 		maximumFractionDigits: 0,
	// 	}).format(sbmk_data_ft['d'])
	// 	// $(frappe.render_template('target_monitor', { as_data_ft: as_data_ft,api_data_ft: api_data_ft, sp_data_ft: sp_data_ft,sbmk_data_ft: sbmk_data_ft })).appendTo(page.main)
	// });

	// frappe.xcall(
	// 	'teampro.teampro.page.target_monitor.target_monitor.get_sc_value_bt',
	// 	{
	// 		month: month,
	// 		year: year,
	// 	}
	// ).then(sc_value => {
	// 	as_data_bt = sc_value[0]
	// 	api_data_bt = sc_value[1]
	// 	sp_data_bt = sc_value[2]
	// 	sbmk_data_bt = sc_value[3]
	// 	as_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(as_data_bt['bt_monthly'])
	// 	as_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(as_data_bt['total_value'])
	// 	as_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(as_data_bt['d'])

	// 	api_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(api_data_bt['bt_monthly'])
	// 	api_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(api_data_bt['total_value'])
	// 	api_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(api_data_bt['d'])

	// 	sp_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sp_data_bt['bt_monthly'])
	// 	sp_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sp_data_bt['total_value'])
	// 	sp_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sp_data_bt['d'])

	// 	sbmk_data_bt['bt_monthly'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sbmk_data_bt['bt_monthly'])
	// 	sbmk_data_bt['total_value'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sbmk_data_bt['total_value'])
	// 	sbmk_data_bt['d'] = Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR',  minimumFractionDigits: 0,
	// 	maximumFractionDigits: 0, }).format(sbmk_data_bt['d'])
	// 	$(frappe.render_template('target_monitor', { as_data_bt: as_data_bt,api_data_bt: api_data_bt, sp_data_bt: sp_data_bt,sbmk_data_bt:sbmk_data_bt})).appendTo(page.main)
	// });


}
