frappe.pages['acgc-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'ACGC Dashboard',
		single_column: true
	});
	frappe.breadcrumbs.add("Setup");
	$(frappe.render_template('acgc_dashboard')).appendTo(page.main);
}
