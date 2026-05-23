frappe.pages['daily-monitor-status'].on_page_load = function(wrapper) {

	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Daily Monitor Status',
		single_column: true
	});

	setTimeout(() => {

		let title = $(page.wrapper).find('.page-title');

		// Center the title container
		$(page.wrapper).find('.page-head .container')
			.css({
				'text-align': 'center'
			});

		// Style like nav button card
		title.css({
			'display': 'inline-block',
			'width': '30%',                 
			'padding': '14px 0px',          
			'background-color': '#EDE7F6', 
			'border': '3px solid #4A148C',  
			'border-radius': '12px',
			'color': '#4A148C',
			'font-weight': '600',
			'font-size': '18px'
		});

	}, 100);

	// =====================================
	// 🔹 FILTER ROW (Below Heading)
	// =====================================

	let filter_row = $(`
		<div style="
			display:flex;
			gap:10px;
			flex-wrap:wrap;
			align-items:flex-start;
			margin-top:20px;
			margin-bottom:10px;
		">
		</div>
	`).appendTo(page.body);


	// 🔹 TEAM
	let team_field = page.add_field({
		label: 'Team',
		fieldtype: 'Link',
		options: 'Dev Team',
		fieldname: 'team'
	});
	filter_row.append(team_field.$wrapper);


	// 🔹 CB
	let cb_field = page.add_field({
		label: 'CB',
		fieldtype: 'Data',
		fieldname: 'cb'
	});
	filter_row.append(cb_field.$wrapper);


	// 🔹 PROJECT
	let project_field = page.add_field({
		label: 'Project',
		fieldtype: 'Link',
		options: 'Project',
		fieldname: 'project'
	});
	filter_row.append(project_field.$wrapper);


	// 🔹 PRODUCTION DATE
	let prod_date = page.add_field({
		label: 'Production Date',
		fieldtype: 'Date',
		fieldname: 'production_date'
	});
	filter_row.append(prod_date.$wrapper);

	// let status_field = page.add_field({
	// 	label: 'Status',
	// 	fieldtype: 'Select',
	// 	fieldname: 'status',
	// 	options: [
	// 		"",
	// 		"Open",
	// 		"Working",
	// 		"Code Review",
	// 		"Pending Review",
	// 		"Client Review",
	// 		"Overdue",
	// 		"Template",
	// 		"Hold",
	// 		"Completed",
	// 		"Cancelled"
	// 	]
	// });
	// filter_row.append(status_field.$wrapper);
	
	// 🔹 ACTUAL TIME (Circle Filter)
	let actual_time_field = page.add_field({
		label: 'Actual Time',
		fieldtype: 'Select',
		fieldname: 'actual_time',
		options: [
			"",
			"Blue",
			"Orange",
			"Red",
			"None"
]
	});
	filter_row.append(actual_time_field.$wrapper);
	// actual_time_field.set_value(" ");

	// 🔹 APPLY BUTTON
	let apply_btn = page.add_field({
		label: 'Apply',
		fieldtype: 'Button',
		fieldname: 'apply'
	});
	filter_row.append(apply_btn.$wrapper);

	$(apply_btn.$input).css({
		'background-color': '#6A1B9A',
		'color': 'white',
		'border': '2px solid #4A148C',
		'border-radius': '8px',
		'height': '32px',      
		'width': '120px',
		'font-weight': '600',
		'padding': '4px 10px'  
	});

	

	// =====================================
	// 🔹 TABLE CONTAINER
	// =====================================

	let table_container = $(`
		<div style="margin-top:20px;"></div>
	`).appendTo(page.body);
	
	apply_btn.$input.on('click', function() {

		load_daily_monitor_data({
			date: prod_date.get_value() || frappe.datetime.get_today(),
			team: team_field.get_value(),
			cb: cb_field.get_value(),
			project: project_field.get_value(),
			// status: status_field.get_value(),
			actual_time: actual_time_field.get_value()
		});

	});

	load_daily_monitor_data({
		date: frappe.datetime.get_today(),
		team: null,
		cb: null,
		project: null,
		status: null,
		actual_time: null
	});

	function load_daily_monitor_data(filters) {

		table_container.html(""); // clear old table

		// 🔹 Build Parent Filters
		let parent_filters = {};

		// Date (default today)
		parent_filters.date = filters.date || frappe.datetime.get_today();

		// Team filter
		if (filters.team) {
			parent_filters.dev_team = filters.team;
		}

		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Daily Monitor",
				filters: parent_filters,
				fields: ["name", "dev_team"],
				order_by: "dev_team asc",
				limit_page_length: 100
			},
			callback: function(r) {

				if (!r.message || r.message.length === 0) {
					table_container.html("<p>No Data Found</p>");
					return;
				}

				render_table(r.message, filters);
			}
		});
	}



function render_table(parents, filters) {
	console.log("Filters:", filters);
    let all_rows = [];
    let row_promises = [];

    parents.forEach(parent => {

        row_promises.push(
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Daily Monitor",
                    name: parent.name
                }
            }).then(r => {

                let tasks = r.message.task_details || [];

                let filtered_tasks = tasks.filter(task => {

                    if (filters.cb && task.cb !== filters.cb) return false;
                    if (filters.project && task.project_name !== filters.project) return false;
                    return true;
                });

                let task_checks = filtered_tasks.map(task => {

                    return frappe.call({
					method: "frappe.client.get",
					args: {
						doctype: "Task",
						name: task.id
					}
				}).then(res => {

					let task_doc = res.message || {};

					let task_confirmed = Number(task_doc.is_confirmed) === 1;

					let allocated_on = task_doc.custom_allocated_on || "";
					let age = task_doc.custom_age || "";

					all_rows.push({
						team: parent.dev_team || "",
						cb: task.cb || "",
						project: task.project_name || "",
						task_id: task.id || "",
						subject: task.subject || "",
						task_confirmed: task_confirmed,
						allocated_to: task.allocated_to || "",
						today_rt: Number(task.today_rt) || 0,

						expected_time: task_doc.expected_time || 0,
						created_on: task_doc.creation || "",
						allocated_on: allocated_on,
						age: age
					});

				});
                });

                return Promise.all(task_checks);
            })
        );
    });

    Promise.all(row_promises).then(() => {

        // 🔹 Sort Rows
        all_rows.sort((a, b) => {
            let teamCompare = a.team.localeCompare(b.team);
            if (teamCompare !== 0) return teamCompare;
            return a.cb.localeCompare(b.cb);
        });

        // 🔹 Assign unique color per team
        let team_colors = {};
        let color_palette = ["#FFCDD2", "#C8E6C9", "#BBDEFB", "#FFF9C4", "#D1C4E9", "#FFE0B2"];
        let color_index = 0;

        all_rows.forEach(row => {
            if (!team_colors[row.team]) {
                team_colors[row.team] = color_palette[color_index % color_palette.length];
                color_index++;
            }
        });

        // 🔹 Build HTML Table
        let html = `
        <table id="daily-monitor-table" style="width:100%; border-collapse:collapse; border:1px solid #4A148C;">
            <thead>
                <tr>
                    <th style="width:120px; text-align:center; border:1px solid #4A148C;">Team</th>
                    <th style="width:80px; text-align:center; border:1px solid #4A148C;">CB</th>
                    <th style="width:240px; text-align:center; border:1px solid #4A148C;">Project</th>
					<th style="width:340px; text-align:center; border:1px solid #4A148C;">Subject</th>
                    <th style="width:120px; text-align:center; border:1px solid #4A148C;">Status</th>
                    <th style="width:200px; text-align:center; border:1px solid #4A148C;">Is Confirmed</th>
                </tr>
            </thead>
            <tbody>
        `;

        // 🔹 Count rows per team (for rowspan)
        let team_count = {};
        all_rows.forEach(row => {
            if (!team_count[row.team]) team_count[row.team] = 0;
            team_count[row.team]++;
        });

        let last_team = null;

        all_rows.forEach(row => {

            html += `<tr data-team="${row.team}">`;

            // Team Column with unique color + center align + rowspan
            if (row.team !== last_team) {
				html += `<td class="team-cell" rowspan="${team_count[row.team]}" style="text-align:center; vertical-align:middle; background-color:${team_colors[row.team]}; border:1px solid #4A148C;">${row.team}</td>`;                last_team = row.team;
            }

            // CB Column
            html += `<td style="text-align:center; border:1px solid #4A148C;">${row.cb}</td>`;

            // Project Column with wrap text
			function format_date_only(date_string) {

				if (!date_string) return "";

				let d = new Date(date_string);

				let day = ("0" + d.getDate()).slice(-2);
				let month = ("0" + (d.getMonth() + 1)).slice(-2);
				let year = d.getFullYear();

				return `${day}-${month}-${year}`;
			}

			let created_date = format_date_only(row.created_on);
			let allocated_date = format_date_only(row.allocated_on);

			html += `
				<td style="border:1px solid #4A148C; line-height:1.6">

				<b style="color:red;">${row.project}</b><br>

				<b style="color:#1976D2;">Task ID :</b>
				<a href="/app/task/${row.task_id}" target="_blank">
				${row.task_id}
				</a><br>

				<b style="color:#1976D2;">ET :</b> ${row.expected_time}<br>

				<b style="color:#1976D2;">RT :</b> ${row.today_rt}<br>

				<b style="color:#1976D2;">Created On :</b> ${created_date}<br>

				<b style="color:#1976D2;">Allocated On :</b> ${allocated_date}<br>

				<b style="color:#1976D2;">Age :</b> ${row.age}

				</td>
				`;

            // Subject Column with wrap
            html += `<td style="border:1px solid #4A148C; white-space:normal; word-wrap:break-word;">${row.subject}</td>`;

            // Status Column
            html += `
			<td class="status-cell"
				data-employee="${row.allocated_to}"
				data-task="${row.task_id}"
				style="text-align:center; border:1px solid #4A148C;">
				--
			</td>
			`;

            // Is Confirmed Column
            html += `<td style="border:1px solid #4A148C; text-align:center;">`;

            if (row.task_confirmed) {
                let task_id = row.task_id;
                let today_rt = Number(row.today_rt) || 0; 
                html += `
                    <div class="confirm-simple"
                        data-employee="${row.allocated_to}"
                        data-task="${task_id}"
                        data-date="${filters.date}"
                        data-rt="${today_rt}"
                        style="text-align:center;">

                        <span class="status-circle" style="
                            display:inline-block;
                            width:20px;
                            height:20px;
                            border:2px solid #2196F3;
                            border-radius:50%;
                            margin-right:8px;
                        "></span>

                        <span class="rt-display" style="margin-right:8px;">
                            0 / ${row.today_rt}
                        </span>

                        <span class="percent-display">
                            --
                        </span>
                    </div>
                `;
            } else {
                html += `
                    

                    <button class="btn btn-xs btn-success row-submit"
                        data-task="${row.task_id}">
                        Submit
                    </button>
                `;
            }

            html += "</td>";
            html += "</tr>";
        });

        html += `</tbody></table>`;
        table_container.html(html);

        // Fetch Timesheet Hours After Table Render
		let user_set = new Set();

		table_container.find(".confirm-simple").each(function () {
			let user_email = $(this).data("employee");
			if (user_email) user_set.add(user_email);
		});

		let user_list = Array.from(user_set);
		if (!user_list.length) return;

		// 🔥 STEP 2: Convert User → Employee ID
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Employee",
				filters: {
					user_id: ["in", user_list]
				},
				fields: ["name", "user_id"],
				limit_page_length: 500
			},
			callback: function (emp_res) {

				let employees = emp_res.message || [];
				if (!employees.length) return;

				let user_employee_map = {};
				let employee_ids = [];

				employees.forEach(emp => {
					user_employee_map[emp.user_id] = emp.name;
					employee_ids.push(emp.name);
				});

				// 🔥 STEP 3: Get Timesheets covering date
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "Timesheet",
						filters: {
							employee: ["in", employee_ids],
							start_date: ["<=", filters.date],
							end_date: [">=", filters.date]
						},
						fields: ["name", "employee"],
						limit_page_length: 500
					},
					callback: function (ts_res) {

						let timesheets = ts_res.message || [];
						if (!timesheets.length) return;

						// 🔥 STRUCTURE → Employee + Task wise
						let task_hours = {};

						let promises = timesheets.map(ts =>
							frappe.db.get_doc("Timesheet", ts.name)
						);

						Promise.all(promises).then(full_docs => {

							full_docs.forEach(doc => {

								let emp = doc.employee;

								if (!task_hours[emp]) {
									task_hours[emp] = {};
								}

								(doc.time_logs || []).forEach(row => {

								let task_name = row.task;  
								let hours = Number(row.hours) || 0;

								if (!task_hours[emp][task_name]) {
									task_hours[emp][task_name] = {
										hours: 0,
										status: ""
									};
								}

								task_hours[emp][task_name].hours += hours;
								task_hours[emp][task_name].status = row.task_status;

							});

							});

							// 🔥 STEP 4: Update UI per row
							let actual_filter = filters.actual_time;
							table_container.find("tr").removeClass("filtered-row").show();
							table_container.find(".confirm-simple").each(function () {

								let container = $(this);

								let user_email = container.data("employee");
								let task_name = (container.data("task") || "").toString().trim();
								let today_rt = Number(container.data("rt")) || 0;

								let emp_id = user_employee_map[user_email];

								let ts_hours = 0;
								let ts_status = "";

								if (
									task_hours[emp_id] &&
									task_hours[emp_id][task_name]
								) {
									ts_hours = task_hours[emp_id][task_name].hours;
									ts_status = task_hours[emp_id][task_name].status;
								}

								let percentpopulate = 0;

								if (today_rt > 0) {
									percentpopulate = (ts_hours / today_rt) * 100;
								}

								
								
								let show_row = true;

								// 🔵 BLUE
								if (actual_filter === "Blue") {
									if (percentpopulate >= 75) {
										show_row = false;
									}
								}

								// 🟠 ORANGE
								else if (actual_filter === "Orange") {
									if (percentpopulate < 75 || percentpopulate > 100) {
										show_row = false;
									}
								}

								// 🔴 RED
								else if (actual_filter === "Red") {
									if (percentpopulate <= 100) {
										show_row = false;
									}
								}

								// ⚪ NONE → Show only Submit button rows
								else if (actual_filter === "None") {

									let submit_btn = container.closest("tr").find(".row-submit");

									if (!submit_btn.length) {
										show_row = false;
									}

								}

								if (!show_row) {
									container.closest("tr").addClass("filtered-row");
								}

								

								container.find(".rt-display").text(
									ts_hours.toFixed(2) + " / " + today_rt
								);

								container.find(".percent-display").text(
									percentpopulate.toFixed(1) + "%"
								).css("color", "black");

								let circle = container.find(".status-circle");

								if (percentpopulate >= 100) {
									circle.css("border-color", "red");
								}
								else if (percentpopulate >= 75) {
									circle.css("border-color", "orange");
								}
								else {
									circle.css("border-color", "#2196F3");
								}

								let status_filter = filters.status;

								if (status_filter) {
									let ts_status_clean = (ts_status || "").trim().toLowerCase();
    								let filter_status_clean = status_filter.trim().toLowerCase();

									if (ts_status_clean !== filter_status_clean) {
										return;   
									}

								}

							});

							
							table_container.find(".status-cell").each(function () {

							let cell = $(this);

							let user_email = cell.data("employee");
							let task_name = (cell.data("task") || "").toString().trim();

							let emp_id = user_employee_map[user_email];

							let ts_status = "";

							if (
								task_hours[emp_id] &&
								task_hours[emp_id][task_name]
							) {
								ts_status = task_hours[emp_id][task_name].status;
							}

							// 🔹 If Timesheet status not available → call Task status
							if (!ts_status) {

								frappe.db.get_value("Task", task_name, "status")
									.then(r => {

										let task_status = r.message.status || "--";

										let color = "red";

										if (task_status === "Completed") {
											color = "green";
										}
										else if (task_status === "Pending") {
											color = "orange";
										}

										cell.html(`<b style="color:${color};">${task_status}</b>`);

									});

							}
							else {

								let color = "red";

								if (ts_status === "Completed") {
									color = "green";
								}
								else if (ts_status === "Pending") {
									color = "orange";
								}

								cell.html(`<b style="color:${color};">${ts_status}</b>`);
							}

						});

						if (actual_filter && actual_filter !== "None") {

							table_container.find(".row-submit").each(function () {
								$(this).closest("tr").addClass("filtered-row");
							});

						}

						table_container.find(".filtered-row").css("display", "none");
						fix_team_rowspan();
						});
						
					}
				});

			}
		});

		// Submit Click Reload 
		$(".row-submit").on("click", function () {

			let task_name = $(this).data("task");
			let checkbox = $(this).closest("tr").find(".confirm-check");


			frappe.call({
				method: "frappe.client.set_value",
				args: {
					doctype: "Task",
					name: task_name,
					fieldname: "is_confirmed",
					value: 1
				},
				callback: function () {
					frappe.msgprint("Confirmed Successfully");
					load_daily_monitor_data(filters);
				}
			});
		});
    });

}

};

function fix_team_rowspan() {

	let groups = {};

	$("#daily-monitor-table tbody tr").each(function () {

		if ($(this).css("display") === "none") return;

		let team = $(this).data("team");

		if (!groups[team]) {
			groups[team] = [];
		}

		groups[team].push($(this));
	});

	Object.keys(groups).forEach(team => {

		let rows = groups[team];

		rows.forEach((row, index) => {

			let team_cell = row.find(".team-cell");

			if (index === 0) {
				if (!team_cell.length) {
					row.prepend(`<td class="team-cell">${team}</td>`);
					team_cell = row.find(".team-cell");
				}

				team_cell.attr("rowspan", rows.length).show();
			} 
			else {
				row.find(".team-cell").remove();
			}

		});

	});
}