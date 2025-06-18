
let updatedProjects = {}; // Store modified projects
let updatedTaskPriorities = {}; 
frappe.pages['ptsr-live-monitor'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'PTSR Live Status Report',
        single_column: true
    });
   
    let $headerContainer = $('<div class="form-group" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">')
    .appendTo(page.main);

// Left section (for filter)
let $leftSection = $('<div>').css({
    display: 'flex',
    gap: '1px',
    flex: '1'
}).appendTo($headerContainer);

// Right section (for button)
let $rightSection = $('<div>').css({
    flexShrink: '0'
}).appendTo($headerContainer);

// Service Filter
let service_filter = frappe.ui.form.make_control({
    df: {
        fieldtype: 'Link',
        options: 'Services',
        fieldname: 'service_filter',
        placeholder: 'Select a Service',
        default: "REC-I"
    },
    parent: $leftSection,
    render_input: true
});

service_filter.refresh();
service_filter.set_value("REC-I");
service_filter.$input.on("change", function() {
    let selected_service = service_filter.get_value();
    if (selected_service && selected_service !== "REC-I") {
        frappe.msgprint({
            title: "Under Development",
            message: `
                <div style="text-align: center;">
                    <img src="https://cdn-icons-png.flaticon.com/512/190/190718.png" 
                         style="width: 100px; height: 100px; margin-bottom: 10px;">
                    <p style="font-size: 16px; font-weight: bold;">Developers are working on it. Stay tuned!</p>
                </div>
            `,
            primary_action: {
                label: "OK",
                action() { frappe.hide_msgprint(); }
            }
        });
    }
});

// Submit Button
let submit_btn = $('<button class="btn btn-primary">Submit</button>')
    .click(() => {
        submitUpdatedProjects();
        submitUpdatedTaskPriorities();
    })
    .appendTo($rightSection);
    let $container = $('<div id="ptsr-table-container">').appendTo(page.main);


       // let $headerContainer = $('<div class="form-group" style="display: flex; justify-content: flex-end; align-items: center; gap: 15px; margin-bottom: 10px;">')
    //     .appendTo(page.main);  
    // Add Service Filter (Link Field)
    // let service_filter = frappe.ui.form.make_control({
    //     df: {
    //         fieldtype: 'Link',
    //         options: 'Services',  // Link to your 'Services' Doctype
    //         fieldname: 'service_filter',
    //         placeholder: 'Select a Service',
    //         default: "REC-I"
    //     },
    //     parent: $headerContainer,
    //     render_input: true
    // });
    // Add Service Filter (Link Field)
    
    // service_filter.refresh();  // Ensure control is properly initialized
    // service_filter.set_value("REC-I");
    // service_filter.$input.on("change", function() {
    //     let selected_service = service_filter.get_value();
    //     if (selected_service && selected_service !== "REC-I") {
    //         frappe.msgprint({
    //             title: "Under Development",
    //             message: `
    //                 <div style="text-align: center;">
    //                     <img src="https://cdn-icons-png.flaticon.com/512/190/190718.png" 
    //                          style="width: 100px; height: 100px; margin-bottom: 10px;">
    //                     <p style="font-size: 16px; font-weight: bold;">Developers are working on it. Stay tuned!</p>
    //                 </div>
    //             `,
    //             primary_action: {
    //                 label: "OK",
    //                 action() { frappe.hide_msgprint(); }
    //             }
    //         });
    //     }
    // });

    // Add Submit Button
    // let submit_btn = $('<button class="btn btn-primary">Submit</button>')
    //     .click(() => {
    //         submitUpdatedProjects();
    //         submitUpdatedTaskPriorities();
    //     })
    //     .appendTo($headerContainer);  // Place next to filter

    // let $container = $('<div>').appendTo(page.main); // Main content container

    // Add Submit Button
   

    frappe.call({
        method: "teampro.teampro.page.ptsr_live_monitor.ptsr_live_monitor.get_ptsr_data",
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
                            background-color: #0F1568 !important;
                            color: white !important;
                            text-align: center;
                            padding: 10px;
                        }
                        td {
                            padding: 8px;
                            text-align: center;
                        }
                        .customer-row {
                            background-color: #add8e6 !important;
                            font-weight: bold;
                            text-align: left;
                        }
                        .editable-span {
                            cursor: pointer;
                            display: inline-block;
                            width: 100%;
                            text-align: center;
                        }
                        .editable-input {
                            width: 100%;
                            border: none;
                            background: white;
                            text-align: center;
                            outline: 1px solid #0F1568;
                        }
                        .left-align {
                            text-align: left !important;
                            vertical-align: middle !important;
                        }
                        .expected-value {
                            text-align: right !important;
                        }
                        td[colspan="1"]:nth-child(4), /* AM Remark */
                        td[colspan="1"]:nth-child(5), /* PM Remark */
                        td[colspan="1"]:nth-child(6)  /* SPOC Remark */ {
                            min-width: 100px !important;
                            max-width: 100px !important;
                            word-wrap: break-word;
                            white-space: normal;
                        }

                        /* Increase input size inside these columns */
                        td[colspan="1"]:nth-child(4) .editable-input,
                        td[colspan="1"]:nth-child(5) .editable-input,
                        td[colspan="1"]:nth-child(6) .editable-input {
                            width: 100%;
                            min-height: 100px;
                            max-height: 300px;
                            font-size: 16px;
                            padding: 8px;
                        }

                    </style>
                    <table class="table">
                        <thead>
                            <tr>
                                <th rowspan="2">SI NO</th>
                                <th rowspan="2">Customer Name / Project Name</th>
                                <th rowspan="2">Project Priority</th>
                                <th rowspan="2">AM Remark</th>
                                <th rowspan="2">PM Remark</th>
                                <th rowspan="2">SPOC Remark</th>
                                <th rowspan="2">EV</th>
                                <th rowspan="2">Ex PSL</th>
                                <th rowspan="2">SS</th>
                            </tr>
                            <tr>
                                <th>Task</th>
                                <th>Task Priority</th>
                                <th>VAC</th>
                                <th>SP</th>
                                <th>FP</th>
                                <th>SL</th>
                                <th>LP</th>
                                <th>PSL</th>
                                
                            </tr>
                        </thead>
                        <tbody>
                `;

                let serial_no = 1;
                let total_vac = 0, total_sp = 0, total_fp = 0, total_sl = 0,  total_lp = 0,total_psl = 0;

                data.forEach((customer) => {
                    if (!customer.customer_name) return;

                    let customerRowAdded = false;

                    customer.projects.forEach((project) => {
                        let project_vac = 0, project_sp = 0, project_fp = 0, project_sl = 0,project_lp = 0, project_psl = 0;

                        project.tasks.forEach((task) => {
                            project_vac += task.vac || 0;
                            project_sp += task.sp || 0;
                            project_fp += task.fp || 0;
                            project_sl += task.sl || 0;
                            project_lp += task.custom_lp || 0;
                            project_psl += task.psl || 0;
                            
                        });

                        if (!customerRowAdded) {
                            html += `
                                <tr class="customer-row">
                                    <td colspan="5" style='text-align:left'>${customer.customer_name}-${project.territory}</td>
                                    <td colspan="6"></td>
                                    <td>${project_vac}</td>
                                    <td>${project_sp}</td>
                                    <td>${project_fp}</td>
                                    <td>${project_sl}</td>
                                    <td>${project_lp}</td>
                                    <td>${project_psl}</td>
                                    
                                </tr>
                            `;
                            customerRowAdded = true;
                        }

                        let firstRow = true;
                        project.tasks.forEach((task) => {
                            html += `
                                <tr>
                                    ${firstRow ? `<td rowspan="${project.tasks.length}">${serial_no++}</td>` : ''}
                                    ${firstRow ? `<td rowspan="${project.tasks.length}">${project.project_name}</td>` : ''}
                                     ${firstRow ? `<td rowspan="${project.tasks.length}" onclick="makeEditable(this, '${project.name}', 'priority')">
                                        <span class="editable-span left-align">${project.priority || '-'}</span>
                                    </td>` : ''}

                                    ${firstRow ? `<td rowspan="${project.tasks.length}" onclick="makeEditable(this, '${project.name}', 'remark')" style="min-width: 250px; max-width: 250px; word-wrap: break-word;">
                                        <span class="editable-span left-align">${project.remark || '-'}</span>
                                    </td>` : ''}
                                    
                                    ${firstRow ? `<td rowspan="${project.tasks.length}" onclick="makeEditable(this, '${project.name}', 'account_manager_remark')" style="min-width: 250px; max-width: 250px; word-wrap: break-word;">
                                        <span class="editable-span left-align">${project.account_manager_remark || '-'}</span>
                                    </td>` : ''}

                                    ${firstRow ? `<td rowspan="${project.tasks.length}" onclick="makeEditable(this, '${project.name}', 'custom_spoc_remark')" style="min-width: 250px; max-width: 250px; word-wrap: break-word;">
                                        <span class="editable-span left-align">${project.custom_spoc_remark || '-'}</span>
                                    </td>` : ''}
                                    ${firstRow ? `<td rowspan="${project.tasks.length}" onclick="makeEditable(this, '${project.name}', 'expected_value')">
                                        <span class="editable-span left-align">${project.expected_value || '-'}</span>
                                    </td>` : ''}

                                    ${firstRow ? `<td rowspan="${project.tasks.length}" onclick="makeEditable(this, '${project.name}', 'expected_psl')">
                                        <span class="editable-span left-align">${project.expected_psl || '-'}</span>
                                    </td>` : ''}
                                 ${firstRow ? `<td rowspan="${project.tasks.length}" onclick="makeEditable(this, '${project.name}', 'sourcing_statu')">
                                    <span class="editable-span left-align">${project.sourcing_statu || '-'}</span>
                                </td>` : ''}
                                    <td class="left-align">
                                        <a href="/app/task/${task.name}" target="_blank" style="text-decoration: none;">
                                            ${task.task_name || '-'}
                                        </a>
                                    </td>

                                    <td onclick="makeEditable(this, '${project.name}', 'priority', '${task.name}')">
    <span class="editable-span">${task.task_priority || '-'}</span>
</td>
                                
                                    <td>${task.vac || '0'}</td>
                                    <td>${task.sp || '0'}</td>
                                    <td>${task.fp || '0'}</td>
                                    <td>${task.sl || '0'}</td>
                                    <td>${task.custom_lp || '0'}</td>
                                    <td>${task.psl || '0'}</td>
                                    
                                </tr>
                            `;

                            firstRow = false;
                        });
                        total_vac += project_vac;
                        total_sp += project_sp;
                        total_fp += project_fp;
                        total_sl += project_sl;
                        total_lp += project_lp;
                        total_psl += project_psl;
                        
                    });
                });

                html += `</tbody></table>`;
                $container.html(html);
            }
        }
    });
};




// Function to submit only updated projects
function makeEditable(element, projectName, field, taskName = null) {
    let span = element.querySelector('.editable-span');
    let value = span.innerText.trim();

    element.innerHTML = ''; // Clear the element

    // Check if the field is 'sourcing_statu' to show a dropdown
    if (field === 'sourcing_statu') {
        let select = document.createElement('select');
        select.classList.add('editable-input');

        let options = ['-', 'SP', 'FP', 'SP/FP'];
        options.forEach(opt => {
            let option = document.createElement('option');
            option.value = opt;
            option.text = opt;
            if (opt === value) option.selected = true;
            select.appendChild(option);
        });

        select.onblur = function () {
            let newValue = select.value.trim();
            span.innerText = newValue;
            element.innerHTML = '';
            element.appendChild(span);

            // Save to the update list
            if (projectName) {
                if (!updatedProjects[projectName]) {
                    updatedProjects[projectName] = {};
                }
                updatedProjects[projectName][field] = newValue;
            }
        };

        element.appendChild(select);
        select.focus();
    } else {
        // Default behavior for remarks or task priority: use textarea
        let textarea = document.createElement('textarea');
        textarea.value = value;
        textarea.classList.add('editable-input');
        textarea.style.width = '100%';
        textarea.style.minHeight = '100px';
        textarea.style.maxHeight = '500px';
        textarea.style.resize = 'both';
        textarea.style.overflow = 'auto';
        textarea.style.border = '1px solid #0F1568';
        textarea.style.padding = '5px';
        textarea.style.fontSize = '16px';

        textarea.oninput = function () {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        };

        textarea.onblur = function () {
            let newValue = textarea.value.trim();
            span.innerText = newValue;
            element.innerHTML = '';
            element.appendChild(span);

            if (taskName) {
                if (!updatedTaskPriorities[taskName]) {
                    updatedTaskPriorities[taskName] = {};
                }
                updatedTaskPriorities[taskName][field] = newValue;
            }
            if (projectName) {
                if (!updatedProjects[projectName]) {
                    updatedProjects[projectName] = {};
                }
                updatedProjects[projectName][field] = newValue;
            }
        };

        element.appendChild(textarea);
        textarea.focus();
        textarea.select();
    }
}

function submitUpdatedProjects() {
    if (Object.keys(updatedProjects).length === 0) {
        frappe.msgprint("No updates to submit.");
        return;
    }
    console.log(updatedProjects)
    frappe.call({
        method: "teampro.teampro.page.ptsr_live_monitor.ptsr_live_monitor.update_project_remark",
        args: {
            projects: updatedProjects
        },
        callback: function(response) {
            if (response.message) {
                frappe.msgprint("Projects Updated Successfully");
                updatedProjects = {}; // Clear updated projects after submission
            }
        }
    });
}

function submitUpdatedTaskPriorities() {
    if (Object.keys(updatedTaskPriorities).length === 0) {
        frappe.msgprint("No task priority updates to submit.");
        return;
    }

    console.log(updatedTaskPriorities);

    frappe.call({
        method: "teampro.teampro.page.ptsr_live_monitor.ptsr_live_monitor.update_task_priority",
        args: {
            tasks: updatedTaskPriorities
        },
        callback: function(response) {
            if (response.message) {
                frappe.msgprint("Task priorities updated successfully.");
                updatedTaskPriorities = {}; // Clear task updates after submission
            }
        }
    });
}

