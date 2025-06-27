// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("REC Week Plan", {
	onload(frm) {
        if (frm.is_new()) {
            frm.set_value("posting_date",frappe.datetime.now_datetime())

            frappe.db.get_list('Project', {
                fields: ['name','territory','sourcing_statu','tvac','tsp','tfp','tsl','tpsl','project_name'],
                filters: {
                    status: ['in', ['Open', 'Enquiry','Draft']],
                    service: ['in', ['REC-I', 'REC-D']]
                },
                limit: 100
            }).then(projects => {
                frm.clear_table("project_details");
                projects.forEach(project => {
                    let row = frm.add_child("project_details");
                    row.project = project.name;
                    row.project_name=project.project_name;
                    row.territory=project.territory;
                    row.status=project.sourcing_statu;
                    row.vac=project.tvac;
                    row.sp=project.tsp;
                    row.fp=project.tfp;
                    row.sl=project.tsl;
                    row.psl=project.tpsl;

                });
                frm.refresh_field("project_details");
                frm.fields_dict.project_details.grid.grid_rows.forEach((row, index) => {
            row.wrapper.css('background-color', index % 2 === 1 ? '#f2f2f2' : '');
        });
            });
             
        }
    },
    validate(frm){
        if (!frm.is_new()) {
            if(frm.doc.start_date){
                frm.set_value("from_date",frm.doc.start_date)
            }
            if(frm.doc.end_date){
                frm.set_value("to_date",frm.doc.end_date)
            }
    }
       
    },
    start_date(frm){
        if (!frm.is_new()) {
            frm.set_value("from_date",frm.doc.start_date)
        }
    },
    end_date(frm){
        if (!frm.is_new()) {
            frm.set_value("to_date",frm.doc.end_date)
        }
    },
    from_date: function(frm) {
        frm.trigger("options");
    },
    to_date: function(frm) {
        frm.trigger("options");
    },
    executive: function(frm) {
        frm.trigger("options");
    },
   options: function(frm) {
        if (frm.doc.options === "DPR") {
            frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dpr_collapsible_html",
                args: {
                    name: frm.doc.name,
                    start_date: frm.doc.from_date,
                    end_date: frm.doc.to_date,
                    executive:frm.doc.executive
                },
                callback: function(r) {
                    if (r.message) {
                        let data = r.message;
                        let html = `
                            <style>
                                table {
                                    width: 100%;
                                    border-collapse: collapse !important;
                                }
                                table, th, td {
                                    border: 1px solid black !important;
                                }
                                th {
                                    background-color:rgb(30, 12, 111) !important;
                                    color: white !important;
                                    text-align: center;
                                    padding: 10px;
                                }
                                td {
                                    padding: 8px;
                                    text-align: center;
                                }
                                .left-align {
                                    text-align: left !important;
                                    padding-left: 10px !important;
                                }
                                .parent-row {
                                    cursor: pointer;
                                    background-color: #e0e0e0;
                                    font-weight: bold;
                                }
                                .child-row {
                                    background-color: #f9f9f9;
                                }
                                .toggle-icon {
                                    float: right;
                                    font-weight: bold;
                                    color: #5E3B63;
                                }
                            </style>
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Executive</th>
                                        <th>Position</th>
                                        <th>RC</th>
                                    </tr>
                                </thead>
                                <tbody>
                        `;

                        let groupIdCounter = 1;

                        Object.keys(data).forEach((exe, idx) => {
                            let groupId = `group-${groupIdCounter++}`;
                            let taskList = data[exe];
                            let totalTasks = taskList.length;
                            let totalRC = taskList.reduce((sum, row) => sum + (parseFloat(row.rc) || 0), 0);
                            // html += `
                            //     <tr class="parent-row" data-group="${groupId}">
                            //         <td>${idx + 1}</td>
                            //         <td class="left-align" colspan="3">${exe} <span class="toggle-icon">[+]</span></td>
                            //     </tr>
                            // `;
                            html += `
                            <tr class="parent-row" data-group="${groupId}">
                                <td><span class="toggle-icon">[+]</span></td>
                                <td class="left-align">${exe}</td>
                               <td>${totalTasks}</td>
                                <td>${totalRC}</td>
                            </tr>
                        `;


                            data[exe].forEach(row => {
                                html += `
                                    <tr class="child-row ${groupId}" style="display: none;">
                                        <td></td>
                                        <td class="left-align">${row.task}</td>
                                        <td class="left-align">${row.subject}</td>
                                        <td style="text-align:center">${row.rc}</td>
                                    </tr>
                                `;
                            });
                        });

                        html += `</tbody></table>`;

                        let $wrapper = frm.fields_dict.dpr.$wrapper;
                        $wrapper.html(html);

                        $('.parent-row').click(function () {
                            let groupId = $(this).data('group');
                            let icon = $(this).find('.toggle-icon');
                            $(`.${groupId}`).toggle();
                            icon.text(icon.text() === '[+]' ? '[-]' : '[+]');
                        });
                    }
                }
            });
        }
        else if (frm.doc.options === "DSR") {
//  frappe.call({
//     method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dsr_collapsible_html",
//     args: {
//         name: frm.doc.name,
//         start_date: frm.doc.from_date,
//         end_date: frm.doc.to_date,
//         executive: frm.doc.executive
//     },
//     callback: function (r) {
//         if (r.message) {
//             const { date_headers, raw_dates, data } = r.message;

//             let html = `
//                 <style>
//                     table {
//                         width: 100%;
//                         border-collapse: collapse !important;
//                     }
//                     table, th, td {
//                         border: 1px solid black !important;
//                     }
//                     th {
//                         background-color: rgb(30, 12, 111) !important;
//                         color: white !important;
//                         text-align: center;
//                         padding: 10px;
//                     }
//                     td {
//                         padding: 8px;
//                         text-align: center;
//                     }
//                     .left-align {
//                         text-align: left !important;
//                         padding-left: 10px !important;
//                     }
//                     .parent-row {
//                         cursor: pointer;
//                         background-color: #e0e0e0;
//                         font-weight: bold;
//                     }
//                     .child-row {
//                         background-color: #f9f9f9;
//                     }
//                     .toggle-icon {
//                         float: right;
//                         font-weight: bold;
//                         color: #5E3B63;
//                     }
//                 </style>
//                 <table class="table table-bordered">
//                     <thead>
//                         <tr>
//                             <th rowspan="2">#</th>
//                             <th rowspan="2">EXE</th>
//                             <th rowspan="2">Task</th>
//                             <th rowspan="2">Subject</th>
//                             <th colspan="${date_headers.length * 2}">RC / AC</th>
//                         </tr>
//                         <tr>`;

//             date_headers.forEach(d => {
//                 html += `<th>${d} RC</th><th>${d} AC</th>`;
//             });

//             html += `</tr></thead><tbody>`;

//             let groupIdCounter = 1;
//             let rowCount = 1;

//             Object.keys(data).forEach((exe) => {
//                 let groupId = `group-${groupIdCounter++}`;
//                 let tasks = data[exe];
//                 let totalTasks = Object.keys(tasks).length;

//                 let exe_rt_totals = {};
//                 let exe_ac_totals = {};
//                 raw_dates.forEach(d => {
//                     exe_rt_totals[d] = 0;
//                     exe_ac_totals[d] = 0;
//                 });

//                 for (let task in tasks) {
//                     raw_dates.forEach(d => {
//                         exe_rt_totals[d] += tasks[task].dates[d]?.rt || 0;
//                         exe_ac_totals[d] += tasks[task].dates[d]?.ac || 0;
//                     });
//                 }

//                 // âœ… Parent Row: Executive Name
//                html += `
//     <tr class="parent-row" data-group="${groupId}">
//         <td><span class="toggle-icon">[+]</span></td>
//         <td class="left-align">${exe}</td>
//         <td>${totalTasks}</td>
//         <td></td>`;



//                 raw_dates.forEach(d => {
//                     html += `<td><b>${exe_rt_totals[d]}</b></td><td><b>${exe_ac_totals[d]}</b></td>`;
//                 });

//                 html += `</tr>`;

//                 // âœ… Child Rows: Show project, task, subject â€” NOT executive
//                 for (let task in tasks) {
//                     let taskData = tasks[task];
//                     html += `<tr class="child-row ${groupId}" style="display: none;">
//                         <td>${rowCount++}</td>
//                         <td class="left-align">${taskData.project || ""}${taskData.project_name ? ' - ' + taskData.project_name : ''}</td>
//                         <td class="left-align">${task}</td>
//                         <td class="left-align">${taskData.subject || ""}</td>`;

//                     raw_dates.forEach(d => {
//                         html += `<td>${taskData.dates[d]?.rt || 0}</td><td>${taskData.dates[d]?.ac || 0}</td>`;
//                     });

//                     html += `</tr>`;
//                 }
//             });

//             html += `</tbody></table>`;

//             let $wrapper = frm.fields_dict.dsr_view.$wrapper;
//             $wrapper.html(html);

//             $('.parent-row').click(function () {
//                 let groupId = $(this).data('group');
//                 let icon = $(this).find('.toggle-icon');
//                 $(`.${groupId}`).toggle();
//                 icon.text(icon.text() === '[+]' ? '[-]' : '[+]');
//             });
//         }
//     }
// });
frappe.call({
    method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dsr_collapsible_html",
    args: {
        name: frm.doc.name,
        start_date: frm.doc.from_date,
        end_date: frm.doc.to_date,
        executive: frm.doc.executive
    },
    callback: function (r) {
        if (r.message) {
            const { date_headers, raw_dates, data } = r.message;

            let html = `
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse !important;
                        font-family: "Segoe UI", sans-serif;
                    }
                    table, th, td {
                        border: 1px solid #ced4da !important;
                    }
                    th {
                        background-color:rgb(30, 12, 111) !important;
                        color: white !important;
                        text-align: center;
                        padding: 10px;
                    }
                    td {
                        padding: 8px;
                        text-align: center;
                        font-size: 13px;
                    }
                    .left-align {
                        text-align: left !important;
                        padding-left: 10px !important;
                    }
                    .parent-row {
                        cursor: pointer;
                        background-color: #e0e0e0 !important;
                        font-weight: bold;
                    }
                    .child-row:nth-child(even) {
                        background-color: #f8f9fa !important;
                    }
                    .toggle-icon {
                        float: right;
                        font-weight: bold;
                        color: #6c757d;
                    }
                    .rc-header {
                        background-color: 		#bbdefb !important;
                        color: black !important;
                    }
                    .ac-header {
                       background-color:	#e1f5fe !important;
                        color: black !important;
                    }
                    .footer-row {
                        background-color: #e9ecef !important;
                        font-weight: bold;
                    }
                </style>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th rowspan="2">#</th>
                            <th rowspan="2">EXE</th>
                            <th rowspan="2">Task</th>
                            <th rowspan="2">Subject</th>
                            <th rowspan="2">Total RC</th>`;

            date_headers.forEach(d => {
                html += `<th colspan="2">${d}</th>`;
            });

            html += `</tr><tr>`;

            raw_dates.forEach(() => {
                html += `
                    <th class="rc-header">RC</th>
                    <th class="ac-header">AC</th>`;
            });

            html += `</tr></thead><tbody>`;

            let groupIdCounter = 1;
            let rowCount = 1;
            let overall_total_rc = 0;

            Object.keys(data).forEach((exe) => {
                let groupId = `group-${groupIdCounter++}`;
                let tasks = data[exe];
                let totalTasks = Object.keys(tasks).length;

                let exe_rt_totals = {};
                let exe_ac_totals = {};
                let exe_total_rc = 0;

                raw_dates.forEach(d => {
                    exe_rt_totals[d] = 0;
                    exe_ac_totals[d] = 0;
                });

                for (let task in tasks) {
                    raw_dates.forEach(d => {
                        exe_rt_totals[d] += tasks[task].dates[d]?.rt || 0;
                        exe_ac_totals[d] += tasks[task].dates[d]?.ac || 0;
                        exe_total_rc += tasks[task].dates[d]?.rt || 0;
                    });
                }

                overall_total_rc += exe_total_rc;

                // Parent row for Executive
                html += `
                    <tr class="parent-row" data-group="${groupId}">
                        <td><span class="toggle-icon">[+]</span></td>
                        <td class="left-align">${exe}</td>
                        <td>${totalTasks}</td>
                        <td></td>
                        <td><b>${exe_total_rc}</b></td>`;

                raw_dates.forEach(d => {
                    html += `<td><b>${exe_rt_totals[d]}</b></td><td><b>${exe_ac_totals[d]}</b></td>`;
                });

                html += `</tr>`;

                // Child rows
                for (let task in tasks) {
                    let taskData = tasks[task];
                    let task_total_rc = 0;
                    raw_dates.forEach(d => {
                        task_total_rc += taskData.dates[d]?.rt || 0;
                    });

                    html += `<tr class="child-row ${groupId}" style="display: none;">
                        <td>${rowCount++}</td>
                        <td class="left-align">${taskData.project || ""}${taskData.project_name ? ' - ' + taskData.project_name : ''}</td>
                        <td class="left-align">${task}</td>
                        <td class="left-align">${taskData.subject || ""}</td>
                        <td>${task_total_rc}</td>`;

                    raw_dates.forEach(d => {
                        html += `<td>${taskData.dates[d]?.rt || 0}</td><td>${taskData.dates[d]?.ac || 0}</td>`;
                    });

                    html += `</tr>`;
                }
            });

            // Overall Total RC Row
            html += `
                <tr class="footer-row">
                    <td colspan="4" style="text-align:center">Overall Total RC</td>
                    <td><b>${overall_total_rc}</b></td>
                    <td colspan="${raw_dates.length * 2}"></td>
                </tr>`;

            html += `</tbody></table>`;

            // Render HTML
            let $wrapper = frm.fields_dict.dsr_view.$wrapper;
            $wrapper.html(html);

            // Toggle rows
            $('.parent-row').click(function () {
                let groupId = $(this).data('group');
                let icon = $(this).find('.toggle-icon');
                $(`.${groupId}`).toggle();
                icon.text(icon.text() === '[+]' ? '[-]' : '[+]');
            });
        }
    }
});

        } else {
            frm.fields_dict.dpr.$wrapper.html("");
        }
    }
});
function allocate_tasks(frm, project_name) {
    if (!project_name) {
        frappe.msgprint("Please select a Project first.");
        return;
    }
    frm.clear_table("task_allocation");
    frappe.db.get_list('Task', {
        fields: ['name','priority','vac','sp','subject'],
        filters: {
            project: project_name,
            status: ['in', ['Working', 'Open', 'Overdue', 'Pending Review']]
        },
        limit: 100  // optional
    }).then(tasks => {
        if (!tasks.length) {
            frappe.msgprint("No matching tasks found for this project.");
            return;
        }
        tasks.forEach(task => {
            let new_row = frm.add_child("task_allocation");
            new_row.task = task.name;
            new_row.priority=task.priority;
            new_row.vac=task.vac;
            new_row.sp=task.sp;
            new_row.subject=task.subject;

        });

        frm.refresh_field("task_allocation");
        // frappe.msgprint("Tasks Updated Successfully")
        frappe.msgprint("Tasks Updated Successfully")
        frm.save()
        frm.scroll_to_field("task_allocation");
    });
}

frappe.ui.form.on("REC Project Details", {
    allocate: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        allocate_tasks(frm, row.project);
    }
});

frappe.ui.form.on("Project Details Allocated", {
    allocate: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        allocate_tasks(frm, row.project);
    }
});

