frappe.pages['personal-dashboard'].on_page_load = function(wrapper) {

	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Amar Karthick P",
		single_column: true
	});

	page.body.innerHTML = `<div id="vue-root"></div>`

	frappe.require([
		"https://unpkg.com/vue@3/dist/vue.global.js",
		"https://cdn.tailwindcss.com",
		"/assets/your_app/js/personal_dashboard_vue.js"
	], () => {

		mountPersonalDashboard("#vue-root")

	})

}