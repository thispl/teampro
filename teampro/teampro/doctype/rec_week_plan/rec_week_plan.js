// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("REC Week Plan", {
	onload(frm) {
        if (frm.is_new()) {
            frm.set_value("posting_date",frappe.datetime.now_datetime())

            frappe.db.get_list('Project', {
                fields: ['name','territory','status','tvac','tsp','tfp','tsl','tpsl'],
                filters: {
                    status: ['in', ['Open', 'Enquiry']],
                    service: ['in', ['REC-I', 'REC-D']]
                },
                limit: 100
            }).then(projects => {
                frm.clear_table("project_details");
                projects.forEach(project => {
                    let row = frm.add_child("project_details");
                    row.project = project.name;
                    row.territory=project.territory;
                    row.status=project.status;
                    row.vac=project.tvac;
                    row.sp=project.tsp;
                    row.fp=project.tfp;
                    row.sl=project.tsl;
                    row.psl=project.tpsl;

                });
                frm.refresh_field("project_details");
            });
        }
    },
    from_date: function(frm) {
        frm.trigger("options");
    },
    to_date: function(frm) {
        frm.trigger("options");
    },
   options: function(frm) {
        if (frm.doc.options === "DPR") {
            frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dpr_collapsible_html",
                args: {
                    name: frm.doc.name,
                    start_date: frm.doc.from_date,
                    end_date: frm.doc.to_date
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
            frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dsr_collapsible_html",
                args: {
                    name: frm.doc.name,
                    start_date: frm.doc.from_date,
                    end_date: frm.doc.to_date
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

