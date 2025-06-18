// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("REC Week Plan", {
	onload(frm) {
        if (frm.is_new()) {
            frm.set_value("posting_date",frappe.datetime.now_datetime())

            frappe.db.get_list('Project', {
                fields: ['name','territory'],
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
                });
                frm.refresh_field("project_details");
            });
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
