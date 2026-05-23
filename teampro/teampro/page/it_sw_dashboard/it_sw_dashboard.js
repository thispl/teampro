frappe.pages['it-sw-dashboard'].on_page_load = function(wrapper) {
	frappe.require([
	"https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js",
	"https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css",
	"https://cdn.datatables.net/buttons/2.4.1/js/dataTables.buttons.min.js",
	"https://cdn.datatables.net/buttons/2.4.1/css/buttons.dataTables.min.css",
	"https://cdn.datatables.net/buttons/2.4.1/js/buttons.html5.min.js",
	"https://cdn.datatables.net/buttons/2.4.1/js/buttons.print.min.js",
	"https://cdn.datatables.net/fixedheader/3.4.0/js/dataTables.fixedHeader.min.js"
	], function() {
	setup_dashboard(wrapper);
	});

};

function setup_dashboard(wrapper) {
	if (!$('#custom-loader').length) {
		$('head').append(`
			<style>
			#custom-loader {
				position: fixed;
				top: 0; left: 0; right: 0; bottom: 0;
				background: rgba(255,255,255,0.8);
				z-index: 9999;
				display: flex;
				flex-direction: column;
				justify-content: center;
				align-items: center;
			}
			.loader {
				--d: 22px;
				width: 4px;
				height: 4px;
				border-radius: 50%;
				color: #08105e;
				box-shadow: 
				calc(1*var(--d))      calc(0*var(--d))     0 0,
				calc(0.707*var(--d))  calc(0.707*var(--d)) 0 1px,
				calc(0*var(--d))      calc(1*var(--d))     0 2px,
				calc(-0.707*var(--d)) calc(0.707*var(--d)) 0 3px,
				calc(-1*var(--d))     calc(0*var(--d))     0 4px,
				calc(-0.707*var(--d)) calc(-0.707*var(--d))0 5px,
				calc(0*var(--d))      calc(-1*var(--d))    0 6px;
				animation: l27 1s infinite steps(8);
			}
			@keyframes l27 {
				100% { transform: rotate(1turn); }
			}
			.loader-text {
				margin-top: 20px;
				font-family: sans-serif;
				font-size: 16px;
				color: #08105e;
			}
			</style>
		`);

		$('body').append(`
			<div id="custom-loader" style="display:none;">
			<div class="loader"></div>
			<div class="loader-text">Loading Data. Please wait...</div>
			</div>
		`);
		}


	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'IT-SW Dashboard',
		single_column: true
	});

	const $filtersRow = $(`<div class="row" style="margin-bottom: 15px;"></div>`);
	const $filterCol = $(`<div class="col-sm-4"></div>`);
	$filtersRow.append($filterCol);
	$(page.body).append($filtersRow);

	const $dashboardContainer = $(`<div class="dashboard-html mt-4"></div>`);
	$(page.body).append($dashboardContainer);

	const sprint = frappe.ui.form.make_control({
		df: {
			fieldtype: 'Link',
			label: 'Task Sprint',
			options: 'Task Sprint',
			fieldname: 'sprint',
			placeholder: 'Select Sprint'
		},
		parent: $filterCol,
		render_input: true
	});

	sprint.refresh();

	frappe.db.get_list('Task Sprint', {
		fields: ['name'],
		order_by: 'creation desc',
		limit: 1
	}).then(result => {
		if (result.length > 0) {
			const sprint_name = result[0].name;
			sprint.set_value(sprint_name);
			load_dashboard_html(sprint_name);
		}
	});

	sprint.$input.on('change', function () {
		let sprint_val = sprint.get_value();
		if (sprint_val) {
			load_dashboard_html(sprint_val);
		}
	});
	sprint.$input.on('awesomplete-selectcomplete', function () {
		let sprint_val = sprint.get_value();
		if (sprint_val) {
			load_dashboard_html(sprint_val);
		}
	});

	function load_dashboard_html(sprint_name) {
		// Show custom loader
		$('#custom-loader').fadeIn('fast');

		frappe.call({
			method: 'teampro.teampro.page.it_sw_dashboard.it_sw_page.it_data_summary',
			args: { sprint: sprint_name },
			callback: function (res) {
				// Hide custom loader
				$('#custom-loader').fadeOut('fast');

				if (res.message) {
					$dashboardContainer.hide().html(res.message).fadeIn('slow');
					setTimeout(() => {
						make_all_tables_interactive();
					}, 500);
				} else {
					$dashboardContainer.html(`<div class="text-muted">No data available.</div>`);
				}
			}
		});
	}




	function make_all_tables_interactive() {
		const static_ids = [
			'#task_table',
			'#sprinted_table',
			'#non_sprinted_table',
			'#reopen_tasks_table',
			'#issue_analysis_table',
			'#psr_hour',
			'#psr_count'
		];

		const breakdown_ids = [];
		$('table[id^="sprint_task_breakdown_table"]').each(function () {
			breakdown_ids.push('#' + this.id);
		});

		const all_table_ids = static_ids.concat(breakdown_ids);

		all_table_ids.forEach(id => {
			const $table = $(id);
			if ($table.length && $.fn.DataTable) {
			const rowCount = $table.find('tbody tr').length;

			if (rowCount === 0) {
				$table.after('<div class="text-muted">No records found.</div>');
				return;
			}

			if ($.fn.DataTable.isDataTable($table)) {
				$table.DataTable().clear().destroy();
			}

			$table.DataTable({
				pageLength: 10,
				lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
				scrollY: rowCount > 10 ? '400px' : 'auto',
				scrollCollapse: true,
				paging: true,
				searching: true,
				ordering: true,
				responsive: true,
				dom: 'lBfrtip',
				buttons: [
				'csv'
				]
			});
			}
		});
	}




}
