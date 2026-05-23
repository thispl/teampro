// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sprint", {
	before_workflow_action(frm) {
		if (frm.doc.workflow_state === 'Completed') {
			const tasks = frm.doc.sprint_task || [];
			for (let row of tasks) {
				if (row.cr_status === 'Code Review') {
					frappe.throw(__('You cannot complete this workflow. Some tasks are still in Code Review.'));
				}
			}
		}
	},

	validate(frm) {
		// if(frm.doc.__islocal){
		// if(frm.doc.from_date && frm.doc.to_date){
		// 	frappe.call({
		// 		method:"teampro.teampro.doctype.sprint.sprint.get_working_days",
		// 		args:{
		// 			from_date:frm.doc.from_date,
		// 			to_date:frm.doc.to_date
		// 		},
		// 		callback(r){
		// 			if(r.message){
		// 				frm.doc.sprint_avl_time.forEach(row => {
		// 					if (row.tl == 1) {
		// 						row.available_hours = r.message * 6;
		// 					} else {
		// 						row.available_hours = r.message * 8;
		// 					}
		// 				});
		// 				frm.refresh_field('sprint_avl_time');
		// 			}
		// 		}
		// 	})
			
			// const fromDate = frappe.datetime.str_to_obj(frm.doc.from_date);
			// const toDate = frappe.datetime.str_to_obj(frm.doc.to_date);
			// const diffTime = toDate - fromDate; 
			// const diffDays = diffTime / (1000 * 60 * 60 * 24); 
			//     frm.doc.sprint_avl_time.forEach(row => {
			//     if (row.tl == 1) {
			//         row.available_hours = diffDays * 5;
			//     } else {
			//         row.available_hours = diffDays * 6;
			//     }
			// });
			// frm.refresh_field('sprint_avl_time');
		// }
		
	// }
	},

	from_date(frm){


		if(frm.doc.from_date && frm.doc.to_date){
			frappe.call({
				method:"teampro.teampro.doctype.sprint.sprint.get_working_days",
				args:{
					from_date:frm.doc.from_date,
					to_date:frm.doc.to_date
				},
				callback(r){
					if(r.message){
						console.log(r.message)
						frm.doc.sprint_avl_time.forEach(row => {
							if (row.tl == 1) {
								row.available_hours = r.message * 6;
							} else {
								row.available_hours = r.message * 8;
							}
						});
						frm.refresh_field('sprint_avl_time');
					}
				}
			})
            }

	},

	to_date(frm){


		if(frm.doc.from_date && frm.doc.to_date){
			frappe.call({
				method:"teampro.teampro.doctype.sprint.sprint.get_working_days",
				args:{
					from_date:frm.doc.from_date,
					to_date:frm.doc.to_date
				},
				callback(r){
					if(r.message){
						console.log(r.message)
						frm.doc.sprint_avl_time.forEach(row => {
							if (row.tl == 1) {
								row.available_hours = r.message * 6;
							} else {
								row.available_hours = r.message * 8;
							}
						});
						frm.refresh_field('sprint_avl_time');
					}
				}
			})
            }



	},
	
	team(frm){
		if(frm.doc.team){
			frappe.call({
				method:"teampro.teampro.doctype.sprint.sprint.update_sprint",
				args:{
					name:frm.doc.name,
					team:frm.doc.team
				},
				callback(r){
					if(r.message){
						frm.set_value("sprint_id",r.message)
					}
				}
			})
		}
	},
	before_workflow_action: async (frm) => {
		if (frm.doc.workflow_state == "Draft" && frm.selected_workflow_action == "Planned") {
				try {
					await frappe.call({
						freeze: true,
						freeze_message: 'Loading',
						method: 'teampro.teampro.doctype.daily_monitor.dm_it_dev.send_sprint_panned_mail',
						args: {
							name: frm.doc.name,
							sprint_id:frm.doc.sprint_id,
							team:frm.doc.team
						},
						callback(r){
							frappe.msgprint("SPM has been sent successfully.")
						}
					});
				} catch (err) {
					frappe.throw(`Failed to send DPR: ${err.message || err}`);
				}
			}
	},
	refresh(frm){
		if(frappe.session.user == "bhuvaneswari.a@groupteampro.com"){
			frm.add_custom_button('Update Tasks Sprint', function() {


				frappe.call({
					method: "teampro.teampro.doctype.sprint.sprint.update_tasks_sprint",
					args: {
						sprint: frm.doc.name
					},
					callback: function(r) {
						if (!r.exc) {
							frappe.msgprint("Tasks updated successfully");
							frm.reload_doc();
						}
					}
				});

			});
		}
		const sprint_rows = frm.doc.sprint_avl_time || [];

if (sprint_rows.length === 0) {
	frm.get_field("employee").$wrapper.html("<p>No sprint data available.</p>");
	return;
}

const short_codes = sprint_rows
	.map(row => row.short_code)
	.filter(Boolean);


if (short_codes.length === 0) {
	frm.get_field("employee").$wrapper.html("<p>No short codes found in sprint rows.</p>");
	return;
}



if (frm.doc.service =='CMN'){
	console.log(short_codes)
	frappe.call({
	method: "frappe.client.get_list",
	args: {
		doctype: "Employee",
		filters: {
			short_code: ["in", short_codes],
			department: "Support Team - THIS",
			designation:'Graphic Designer'
		},
		fields: ["name", "employee_name", "image", "short_code", "custom_is_tl", "custom_dev_team", "department"]
	},
	callback: function (r) {
		let employees = r.message || [];
		console.log("Employees Fetched:", employees);

		if (!employees.length) {
			frm.get_field("employee").$wrapper.html("<p>No employees found matching short codes, team, and department.</p>");
			return;
		}

		employees = employees.filter(emp =>
			sprint_rows.some(row => row.short_code === emp.short_code)
		);

		console.log("Employees After Sprint Match Filter:", employees);

		if (!employees.length) {
			frm.get_field("employee").$wrapper.html("<p>No employees match sprint rows for this team and department.</p>");
			return;
		}

		employees.sort((a, b) => {
			if (a.custom_is_tl && !b.custom_is_tl) return -1;
			if (!a.custom_is_tl && b.custom_is_tl) return 1;
			return a.employee_name.localeCompare(b.employee_name);
		});

		const html = employees.map(emp => {
			const row = sprint_rows.find(r => r.short_code === emp.short_code) || {};
			return `
				<div style="display: inline-block; text-align: center; margin: 0 10px 10px 0;">
					<div style="font-weight: bold; color: #555;">APH: ${row.available_hours || 0} hrs</div>
					<img 
						src="${emp.image || 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'}"
						title="${emp.employee_name}"
						style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%; border: 2px solid #007BFF; cursor: pointer;" 
					/>
					<div style="color: #555;">${emp.short_code}</div>
					<div style="color: #555;">RT: ${row.allocated_hours || 0} hrs</div>
				</div>
			`;
		}).join('');

		frm.get_field("employee").$wrapper.html(html);
	}
});
}
else{
	frappe.call({
	method: "frappe.client.get_list",
	args: {
		doctype: "Employee",
		filters: {
			short_code: ["in", short_codes],
			custom_dev_team: frm.doc.team,
			department: "IT. Development - THIS"
		},
		fields: ["name", "employee_name", "image", "short_code", "custom_is_tl", "custom_dev_team", "department"]
	},
	callback: function (r) {
		let employees = r.message || [];
		console.log("Employees Fetched:", employees);

		if (!employees.length) {
			frm.get_field("employee").$wrapper.html("<p>No employees found matching short codes, team, and department.</p>");
			return;
		}

		employees = employees.filter(emp =>
			sprint_rows.some(row => row.short_code === emp.short_code)
		);

		console.log("Employees After Sprint Match Filter:", employees);

		if (!employees.length) {
			frm.get_field("employee").$wrapper.html("<p>No employees match sprint rows for this team and department.</p>");
			return;
		}

		employees.sort((a, b) => {
			if (a.custom_is_tl && !b.custom_is_tl) return -1;
			if (!a.custom_is_tl && b.custom_is_tl) return 1;
			return a.employee_name.localeCompare(b.employee_name);
		});

		const html = employees.map(emp => {
			const row = sprint_rows.find(r => r.short_code === emp.short_code) || {};
			return `
				<div style="display: inline-block; text-align: center; margin: 0 10px 10px 0;">
					<div style="font-weight: bold; color: #555;">APH: ${row.available_hours || 0} hrs</div>
					<img 
						src="${emp.image || 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'}"
						title="${emp.employee_name}"
						style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%; border: 2px solid #007BFF; cursor: pointer;" 
					/>
					<div style="color: #555;">${emp.short_code}</div>
					<div style="color: #555;">RT: ${row.allocated_hours || 0} hrs</div>
				</div>
			`;
		}).join('');

		frm.get_field("employee").$wrapper.html(html);
	}
});
}
		if (frm.doc.status=="In Progress"){
			if (frm.doc.service === 'CMN') {
			frm.add_custom_button(__("Create DPR"), function () {
				frappe.model.with_doctype('Daily Monitor', function () {
				let sfu = frappe.model.get_new_doc('Daily Monitor');
				sfu.service = frm.doc.service;
				frappe.db.insert(sfu).then(doc => {
					frappe.set_route("Form", "Daily Monitor", doc.name);
				});
			});
			})
			}
			else{
			frm.add_custom_button(__("Create DPR"), function () {
				frappe.model.with_doctype('Daily Monitor', function () {
				let sfu = frappe.model.get_new_doc('Daily Monitor');
				sfu.service = "IT-SW";
				// sfu.task_type = "OPS";
				sfu.dev_team = frm.doc.team;
				sfu.sprint = frm.doc.sprint_id;
				frappe.db.insert(sfu).then(doc => {
					frappe.set_route("Form", "Daily Monitor", doc.name);
				});
			});
			})
		}
		}
		if (frm.doc.service !== 'CMN') {
		frm.add_custom_button(__("Send Planned Mail"),function(){

			frappe.call({
						freeze: true,
						freeze_message: 'Loading',
						method: 'teampro.teampro.doctype.daily_monitor.dm_it_dev.send_sprint_panned_mail',
						args: {
							name: frm.doc.name,
							sprint_id:frm.doc.sprint_id,
							team:frm.doc.team
						}
					});

			
		})
		}
	},
	// render_employee_strip(frm) {
	//     console.log('HI')
		
	// }

});

 