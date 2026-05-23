// frappe.pages['tfp-retail-flow'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});

// 	page.add_inner_button('Customer', function() {
//         frappe.set_route('Form', 'Retail Customer');
//     });
// }

frappe.pages['tfp-retail-flow'].on_page_load = function(wrapper) {

	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Retail Flow',
		single_column: true
	});

	$(`<style>
		.retail-center {
			display: flex;
			justify-content: center;
			align-items: center;
			height: 50vh;
		}

		.retail-btn, .stock-btn {
			background-color: #4CAF50;
			color: white;
			padding: 20px 60px;
			font-size: 22px;
			border: none;
			border-radius: 12px;
			cursor: pointer;
			box-shadow: 0 4px 10px rgba(0,0,0,0.2);
		}

		.retail-btn:hover, .stock-btn:hover {
			background-color: #45a049;
			transform: scale(1.05);
			transition: 0.3s;
		}
	</style>`).appendTo(wrapper);

	$(wrapper).find('.layout-main-section').html(`
		<div class="retail-center">
			<button class="retail-btn" style="margin-right: 20px;">Customer</button>
			<button class="stock-btn">Stock Movement</button>
		</div>
	`);

	$(wrapper).on('click', '.retail-btn', function() {
		frappe.new_doc('Retail Customer');
	});

	$(wrapper).on('click', '.stock-btn', function() {
		frappe.new_doc('Retail Stock Movement');
	});

}; 