// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("REC Week Plan", {
    setup: function (frm) {
        // SP
        frm.set_query("task", function () {

            let filters = [
                ["Task", "service", "in", ["REC-I", "REC-D"]],

            ];

            if (frm.doc.project_filter) {
                filters.push(["Task", "project", "=", frm.doc.project_filter]);
            }

            return {
                filters: filters
            };
        });
        frm.set_query("project_filter", function () {
            return {
                filters: [
                    ["Project", "status", "=", ["Open"]],
                    ["Project", "service", "in", ["REC-I", "REC-D"]],
                ]
            };
        });
        // SP,FP Table
        frm.set_query("sp_fp_task", function () {

            let filters = [
                ["Task", "service", "in", ["REC-I", "REC-D"]],

            ];

            if (frm.doc.sp_fp_project) {
                filters.push(["Task", "project", "=", frm.doc.sp_fp_project]);
            }

            return {
                filters: filters
            };
        });
        frm.set_query("sp_fp_project", function () {
            return {
                filters: [
                    ["Project", "status", "=", ["Open"]],
                    ["Project", "service", "in", ["REC-I", "REC-D"]],
                ]
            };
        });
        // FP Table
        frm.set_query("fp_task", function () {

            let filters = [
                ["Task", "service", "in", ["REC-I", "REC-D"]],

            ];

            if (frm.doc.fp_project) {
                filters.push(["Task", "project", "=", frm.doc.fp_project]);
            }

            return {
                filters: filters
            };
        });
        frm.set_query("fp_project", function () {
            return {
                filters: [
                    ["Project", "status", "=", ["Open"]],
                    ["Project", "service", "in", ["REC-I", "REC-D"]],
                ]
            };
        });
        // PND
        frm.set_query("pnd_task", function () {
            let filters = [
                ["Task", "service", "in", ["REC-I", "REC-D"]],

            ];
            if (frm.doc.pnd_project) {
                filters.push(["Task", "project", "=", frm.doc.pnd_project]);
            }
            return {
                filters: filters
            };
        });
        frm.set_query("pnd_project", function () {
            return {
                filters: [
                    ["Project", "status", "=", ["Open"]],
                    ["Project", "service", "in", ["REC-I", "REC-D"]],
                ]
            };
        });
        // All Table
        frm.set_query("task_collapsible", function () {
            let filters = [
                ["Task", "service", "in", ["REC-I", "REC-D"]],

            ];
            if (frm.doc.project_collapsible) {
                filters.push(["Task", "project", "=", frm.doc.project_collapsible]);
            }
            return {
                filters: filters
            };
        });
        frm.set_query("project_collapsible", function () {
            return {
                filters: [
                    ["Project", "status", "=", "Open"],
                    ["Project", "service", "in", ["REC-I", "REC-D"]],
                    ["Project", "customer", "=", frm.doc.customer]
                ]
            };
        });
    },
    customer(frm) {
        build_master_table(frm)
    },
    project_collapsible(frm) {
        build_master_table(frm)
    },
    src_s(frm) {
        build_master_table(frm)
    },
    task_collapsible(frm) {
        build_master_table(frm)
    },
    // pnd_project: function(frm) {
    //     build_pnd_html(frm);
    // },
    // pnd_task: function(frm) {
    //     build_pnd_html(frm);
    // },
    // fp_task: function(frm) {
    //     build_fp_html(frm);
    // },
    // fp_project: function(frm) {
    //     build_fp_html(frm);
    // },
    // sp_fp_project: function(frm) {
    //     build_spfp_html(frm);
    // },
    // sp_fp_task: function(frm) {
    //     build_spfp_html(frm);
    // },
    // project_filter: function(frm) {
    //     build_sp_html(frm)
    // },
    // task: function(frm) {
    //     build_sp_html(frm)
    // },
    after_save: function (frm) {
        frm.refresh_field('project_details');
        frm.reload_doc()
    },
    refresh(frm) {
        if (frm.doc.workflow_state == "Project Allocation") {
            let pa_status_btn = frm.add_custom_button(__('PA Completion'), null, 'Action');
            pa_status_btn.css({
                'background-color': '#138d8d',
                'color': '#fff',
                'font-weight': 'bold'
            });
            pa_status_btn.addClass('disabled-button');
            frm.add_custom_button("PA ALPHA Completed", function () {
                frm.set_value("pa_alpha_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "PA ALPHA Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
            frm.add_custom_button("PA BRAVO Completed", function () {
                frm.set_value("pa_bravo_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "PA BRAVO Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
            frm.add_custom_button("PA CHARLIE Completed", function () {
                frm.set_value("pa_charlie_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "PA CHARLIE Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
            frm.add_custom_button("PA DELTA Completed", function () {
                frm.set_value("pa_delta_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "PA DELTA Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
        }
        if (frm.doc.workflow_state == "Task Allocation") {

            let ta_status_btn = frm.add_custom_button(__('TA Completion'), null, 'Action');
            ta_status_btn.css({
                'background-color': '#138d8d',
                'color': '#fff',
                'font-weight': 'bold'
            });
            ta_status_btn.addClass('disabled-button');
            frm.add_custom_button("TA ALPHA Completed", function () {
                frm.set_value("ta_alpha_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "TA ALPHA Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
            frm.add_custom_button("TA BRAVO Completed", function () {
                frm.set_value("ta_bravo_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "TA BRAVO Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
            frm.add_custom_button("TA CHARLIE Completed", function () {
                frm.set_value("ta_charlie_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "TA CHARLIE Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
            frm.add_custom_button("TA DELTA Completed", function () {
                frm.set_value("ta_delta_completed", 1)
                frm.add_child("status_transition", {
                    "user": frappe.session.user,
                    "status": "TA DELTA Completed",
                    "date": frappe.datetime.now_datetime(),
                })
                frm.save()
            }, "Action")
        }
        let status_btn = frm.add_custom_button(__('Update'), null, 'Action');
        status_btn.css({
            'background-color': '#138d8d',
            'color': '#fff',
            'font-weight': 'bold'
        });
        status_btn.addClass('disabled-button');
        frm.add_custom_button("Refresh", function () {

            if (frm.is_dirty()) {
                frappe.msgprint("Please click Update before Refresh");
                return;
            }

            frm.clear_table("rec_task_planner");

            frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_rec_task_data",
                freeze: true,
                freeze_message: "Loading...",
                callback(r) {

                    if (!r.message) return;

                    r.message.forEach(row => {
                        frm.add_child("rec_task_planner", {
                            project: row.project,
                            project_name: row.project_name,
                            task: row.subject,
                            task_id: row.task,
                            territory: row.territory,
                            priority: row.priority,
                            spoc: row.spoc_short_code,
                            vac: row.vac,
                            src_s: row.src_s,
                            sp: row.sp,
                            fp: row.fp,
                            client: row.customer,
                            sl: row.sl,
                            lp: row.lp,
                            psl: row.psl,
                            src: row.src,
                            moi: row.moi,
                            cc: row.sp,
                            am: row.account_manager_short_code,
                            pm: row.project_manager_short_code,
                            status:row.status

                        });
                    });

                    frm.refresh_field("rec_task_planner");

                    frm.save().then(() => {
                        build_sp_html(frm);
                        build_spfp_html(frm);
                        build_fp_html(frm);
                        build_pnd_html(frm);
                    });
                }
            });

        }, "Action");

        frm.set_query("employee", 'task_allocation', function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                    ['Employee', 'status', '=', 'Active']
                ]
            };
        });
        frm.set_query("sams", 'task_allocation_agent', function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                    ['SAMS', 'sa_status', '!=', 'Do Not Contact']
                ]
            };
        });
        frm.set_query("employee", 'task_allocation_agent', function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                    ['Employee', 'status', '=', 'Active']
                ]
            };
        });
        render_employee_strip(frm, null);
        update_day_labels(frm);
        apply_team_date_filter(frm);
        // build_sp_html(frm);
        // build_spfp_html(frm);
        // build_fp_html(frm)
        // build_pnd_html(frm)
        build_master_table(frm)
        let button_html = `
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <button id="download_excel" 
                        style="
                            background: linear-gradient(45deg, #0056b3, #0056b3);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 6px;
                            font-weight: bold;
                            cursor: pointer;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                        ">
                        Download
                    </button>
                </div>`;


        frm.fields_dict.download_button.$wrapper.html(button_html);

        $("#download_excel").off("click").on("click", function () {

            let url = "/api/method/teampro.teampro.doctype.rec_week_plan.rec_week_plan.download_dsr_excel"
                + "?name=" + encodeURIComponent(cur_frm.doc.name)
                + "&start_date=" + encodeURIComponent(cur_frm.doc.from_date || "")
                + "&end_date=" + encodeURIComponent(cur_frm.doc.to_date || "")
                + "&executive=" + encodeURIComponent(cur_frm.doc.executive || "")
                + "&team_type=" + encodeURIComponent(cur_frm.doc.team_type || "");

            window.open(url);
        });

        frm.fields_dict.download && frm.fields_dict.download.$input.on("click", function () {
            trigger_download(frm);
        });

        if (frm.fields_dict.allocation && frm.fields_dict.allocation.grid) {
            let $bulk = frm.fields_dict.allocation.grid.wrapper.find(".grid-bulk-actions");
            if ($bulk.length && !$bulk.find(".allocation-excel-download").length) {
                $bulk.find(".grid-download").before(`
                    <button type="button" class="btn btn-xs btn-secondary allocation-excel-download" style="margin-right:5px;">
                        ${__("Download Excel")}
                    </button>
                `);
                $bulk.find(".allocation-excel-download").on("click", function () {
                    window.open(
                        `/api/method/teampro.teampro.doctype.rec_week_plan.rec_week_plan.download_allocation_internal_excel?docname=${encodeURIComponent(frm.doc.name)}`
                    );
                });
            }
        }

    },

    onload(frm) {
        if (!frm.is_new()) {


            render_dev_team_logos(frm);

        }
        if (frm.is_new()) {
            frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_rec_task_data",
                freeze: true,
                freeze_message: "Loading...",
                callback(r) {
                    if (r.message && r.message.length) {

                        r.message.forEach(row => {
                            let moi = "";
                            if (row.moi === "Direct") {
                                moi = "DCI";
                            } else if (row.moi === "Direct Internal Interview") {
                                moi = "DII";
                            } else if (row.moi === "CV Selection") {
                                moi = "CVS";
                            } else if (row.moi === "Wire Selection") {
                                moi = "WS";
                            }
                            frm.add_child("rec_task_planner", {
                                project: row.project,
                                project_name: row.project_name,
                                task: row.subject,
                                task_id: row.task,
                                territory: row.territory,
                                priority: row.priority,
                                spoc: row.spoc_short_code,
                                vac: row.vac,
                                src_s: row.src_s,
                                client: row.customer,
                                sp: row.sp,
                                fp: row.fp,
                                sl: row.sl,
                                lp: row.lp,
                                psl: row.psl,
                                src: row.src,
                                moi: moi,
                                cc: row.sp,
                                am: row.account_manager_short_code,
                                pm: row.project_manager_short_code,
                                status:row.status
                            });
                        });

                        frm.refresh_field("rec_task_planner");
                    }
                }
            });
            build_sp_html(frm)
            build_spfp_html(frm);
            build_fp_html(frm)
            build_pnd_html(frm)

            frm.save()
            frm.set_value("posting_date", frappe.datetime.now_datetime())

            frappe.db.get_list('Project', {
                fields: ['name', 'territory', 'sourcing_statu', 'tvac', 'tsp', 'tfp', 'tsl', 'tpsl', 'project_name'],
                filters: {
                    status: ['not in', ['Draft', 'Enquiry', 'Hold', 'Completed', 'Cancelled']],
                    service: ['in', ['REC-I', 'REC-D']],
                    sourcing_statu: ['in', ['SP', 'SP/FP']]
                },
                limit: 100
            }).then(projects => {
                frm.clear_table("project_details");
                projects.forEach(project => {
                    let row = frm.add_child("project_details");
                    row.project = project.name;
                    row.project_name = project.project_name;
                    row.territory = project.territory;
                    row.status = project.sourcing_statu;
                    row.vac = project.tvac;
                    row.sp = project.tsp;
                    row.fp = project.tfp;
                    row.sl = project.tsl;
                    row.psl = project.tpsl;

                });
                frm.refresh_field("project_details");
                frm.fields_dict.project_details.grid.grid_rows.forEach((row, index) => {
                    row.wrapper.css('background-color', index % 2 === 1 ? '#f2f2f2' : '');
                });
            });

        }
    },
    validate(frm) {
        if (!frm.is_new()) {

            if (!frm.doc.start_date) return;

            const start = frappe.datetime.str_to_obj(frm.doc.start_date);
            const allocation = frm.doc.allocation || [];

            const existing_keys = new Set();
            allocation.forEach(a => {
                const key = `${a.task}::${a.employee}::${a.date}`;
                existing_keys.add(key);
            });

            const task_allocation = frm.doc.task_allocation || [];
            const date_map = {};

            for (let i = 0; i < 7; i++) {
                const d = frappe.datetime.add_days(start, i);
                const field = `day_${i + 1}`;
                date_map[field] = frappe.datetime.obj_to_str(frappe.datetime.str_to_obj(d));
            }

            task_allocation.forEach(row => {
                for (let i = 1; i <= 7; i++) {
                    const day_field = `day_${i}`;
                    const rc_val = row[day_field];
                    const alloc_date = date_map[day_field];

                    if (rc_val && alloc_date) {
                        const key = `${row.task}::${row.employee}::${alloc_date}`;

                        if (!existing_keys.has(key)) {
                            const child = frm.add_child("allocation");
                            child.task = row.task;
                            child.employee = row.employee;
                            child.exe = row.exe;
                            child.date = alloc_date;
                            child.rc = rc_val;
                            child.allocated = 1;

                            existing_keys.add(key);
                        }
                    }
                }
            });

            frm.refresh_field("allocation");
            // Agent
            const start_date = frm.doc.start_date;
            const allocation_agent = frm.doc.allocation_agent || [];
            const existing_key = new Set();

            allocation_agent.forEach(a => {
                const keys = `${a.task}::${a.sams}::${a.date}`;
                existing_key.add(keys);
            });

            const task_allocation_agent = frm.doc.task_allocation_agent || [];
            const date_maps = {};

            for (let i = 0; i < 7; i++) {
                const d = frappe.datetime.add_days(start_date, i); // already yyyy-mm-dd
                const field = `day_${i + 1}`;
                date_maps[field] = d;
            }

            task_allocation_agent.forEach(row => {
                for (let i = 1; i <= 7; i++) {
                    const day_field = `day_${i}`;
                    const rc_val = row[day_field];
                    const alloc_date = date_maps[day_field];

                    if (rc_val && alloc_date) {
                        const keys = `${row.task}::${row.sams}::${alloc_date}`;

                        if (!existing_key.has(keys)) {
                            const child = frm.add_child("allocation_agent");
                            child.task = row.task;
                            child.sams = row.sams;
                            child.employee = row.employee;
                            child.date = alloc_date;
                            child.rc = rc_val;
                            child.allocated = 1;

                            existing_key.add(keys);
                        }
                    }
                }
            });

            frm.refresh_field("allocation_agent");


        }

    },
    start_date(frm) {
        if (!frm.is_new()) {
            frm.set_value("from_date", frm.doc.start_date)
            update_day_labels(frm);
        }
    },
    end_date(frm) {
        if (!frm.is_new()) {
            frm.set_value("to_date", frm.doc.end_date)
            update_day_labels(frm);
        }
    },

    rec_team(frm) {
        apply_team_date_filter(frm);
    },
    date(frm) {
        apply_team_date_filter(frm);
    },
    date_to(frm) {
        apply_team_date_filter(frm);
    },
    after_save(frm) {
        apply_team_date_filter(frm);
    },


    from_date: function (frm) {
        frm.trigger("options");
    },
    to_date: function (frm) {
        frm.trigger("options");
    },
    executive: function (frm) {
        frm.trigger("options");
    },
    sams: function (frm) {
        frm.trigger("options");
    },
    team_type: function (frm) {
        frm.trigger("options");
    },
    options: function (frm) {



        frappe.call({
            method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dsr_collapsible_html",
            args: {
                name: frm.doc.name,
                start_date: frm.doc.from_date,
                end_date: frm.doc.to_date,
                executive: frm.doc.executive,
                team_type: frm.doc.team_type
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
                        background-color: #bbdefb !important;
                        color: black !important;
                    }
                    .ac-header {
                        background-color: #e1f5fe !important;
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
                            <th rowspan="2">Total RC</th>
                            <th rowspan="2">Total AC</th>`;

                    date_headers.forEach(d => {
                        html += `<th colspan="2">${d}</th>`;
                    });

                    html += `</tr><tr>`;
                    raw_dates.forEach(() => {
                        html += `<th class="rc-header">RC</th><th class="ac-header">AC</th>`;
                    });

                    html += `</tr></thead><tbody>`;

                    let groupIdCounter = 1;
                    let rowCount = 1;
                    let overall_total_rc = 0;
                    let overall_total_ac = 0;

                    let daywise_rc_totals = {};
                    let daywise_ac_totals = {};

                    raw_dates.forEach(d => {
                        daywise_rc_totals[d] = 0;
                        daywise_ac_totals[d] = 0;
                    });

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
                                let rt = tasks[task].dates[d]?.rt || 0;
                                let ac = tasks[task].dates[d]?.ac || 0;

                                exe_rt_totals[d] += rt;
                                exe_ac_totals[d] += ac;
                                exe_total_rc += rt;

                                daywise_rc_totals[d] += rt;
                                daywise_ac_totals[d] += ac;
                            });
                        }

                        overall_total_rc += exe_total_rc;
                        overall_total_ac += Object.values(exe_ac_totals).reduce((a, b) => a + b, 0);

                        html += `
                    <tr class="parent-row" data-group="${groupId}">
                        <td><span class="toggle-icon">[+]</span></td>
                        <td class="left-align">${exe}</td>
                        <td>${totalTasks}</td>
                        <td></td>
                        <td><b>${exe_total_rc}</b></td>
                        <td><b>${Object.values(exe_ac_totals).reduce((a, b) => a + b, 0)}</b></td>`;

                        raw_dates.forEach(d => {
                            html += `<td><b>${exe_rt_totals[d]}</b></td><td><b>${exe_ac_totals[d]}</b></td>`;
                        });

                        html += `</tr>`;

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
                        <td>${task_total_rc}</td>
                        <td></td>`;

                            raw_dates.forEach(d => {
                                html += `<td>${taskData.dates[d]?.rt || 0}</td><td>${taskData.dates[d]?.ac || 0}</td>`;
                            });

                            html += `</tr>`;
                        }
                    });

                    html += `
                <tr class="footer-row">
                    <td colspan="4" style="text-align:center">Overall Totals</td>
                    <td><b>${overall_total_rc}</b></td>
                    <td><b>${overall_total_ac}</b></td>`;

                    raw_dates.forEach(d => {
                        html += `<td><b>${daywise_rc_totals[d]}</b></td><td><b>${daywise_ac_totals[d]}</b></td>`;
                    });

                    html += `</tr>`;

                    html += `</tbody></table>`;

                    let $wrapper = frm.fields_dict.dsr_view.$wrapper;
                    $wrapper.html(html);
                    $wrapper.find(".team-multi").each(function () {

                        $(this).select2({
                            width: "140px",
                            placeholder: "Select Team"
                        });

                    });
                    $wrapper.find('.parent-row').click(function () {
                        let groupId = $(this).data('group');
                        let icon = $(this).find('.toggle-icon');
                        $wrapper.find(`.${groupId}`).toggle();
                        icon.text(icon.text() === '[+]' ? '[-]' : '[+]');
                    });

                } else {
                    frm.fields_dict.dsr_view.$wrapper.html("");
                }
            }
        });


        frappe.call({
            method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dsr_collapsible_html_sams",
            args: {
                name: frm.doc.name,
                start_date: frm.doc.from_date,
                end_date: frm.doc.to_date,
                sams: frm.doc.sams
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
                        background-color: rgb(30, 12, 111) !important;
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
                        background-color: #bbdefb !important;
                        color: black !important;
                    }
                    .ac-header {
                        background-color: #e1f5fe !important;
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
                            <th rowspan="2">SAMS</th> 
                            <th rowspan="2">Task</th>
                            <th rowspan="2">Subject</th>
                            <th rowspan="2">Total RC</th>
                            <th rowspan="2">Total AC</th>`;

                    date_headers.forEach(d => {
                        html += `<th colspan="2">${d}</th>`;
                    });

                    html += `</tr><tr>`;
                    raw_dates.forEach(() => {
                        html += `<th class="rc-header">RC</th><th class="ac-header">AC</th>`;
                    });

                    html += `</tr></thead><tbody>`;

                    let groupIdCounter = 1;
                    let rowCount = 1;
                    let overall_total_rc = 0;
                    let overall_total_ac = 0;

                    let daywise_rc_totals = {};
                    let daywise_ac_totals = {};

                    raw_dates.forEach(d => {
                        daywise_rc_totals[d] = 0;
                        daywise_ac_totals[d] = 0;
                    });

                    Object.keys(data).forEach((sams_id) => {
                        let groupId = `group-${groupIdCounter++}`;
                        let tasks = data[sams_id];
                        let totalTasks = Object.keys(tasks).length;

                        let sams_rt_totals = {};
                        let sams_ac_totals = {};
                        let sams_total_rc = 0;

                        raw_dates.forEach(d => {
                            sams_rt_totals[d] = 0;
                            sams_ac_totals[d] = 0;
                        });

                        for (let task in tasks) {
                            raw_dates.forEach(d => {
                                let rt = tasks[task].dates[d]?.rt || 0;
                                let ac = tasks[task].dates[d]?.ac || 0;

                                sams_rt_totals[d] += rt;
                                sams_ac_totals[d] += ac;
                                sams_total_rc += rt;

                                daywise_rc_totals[d] += rt;
                                daywise_ac_totals[d] += ac;
                            });
                        }

                        overall_total_rc += sams_total_rc;
                        overall_total_ac += Object.values(sams_ac_totals).reduce((a, b) => a + b, 0);

                        html += `
                    <tr class="parent-row" data-group="${groupId}">
                        <td><span class="toggle-icon">[+]</span></td>
                        <td class="left-align">${sams_id}</td>
                        <td>${totalTasks}</td>
                        <td></td>
                        <td><b>${sams_total_rc}</b></td>
                        <td><b>${Object.values(sams_ac_totals).reduce((a, b) => a + b, 0)}</b></td>`;

                        raw_dates.forEach(d => {
                            html += `<td><b>${sams_rt_totals[d]}</b></td><td><b>${sams_ac_totals[d]}</b></td>`;
                        });

                        html += `</tr>`;

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
                        <td>${task_total_rc}</td>
                        <td></td>`;

                            raw_dates.forEach(d => {
                                html += `<td>${taskData.dates[d]?.rt || 0}</td><td>${taskData.dates[d]?.ac || 0}</td>`;
                            });

                            html += `</tr>`;
                        }
                    });

                    html += `
                <tr class="footer-row">
                    <td colspan="4" style="text-align:center">Overall Totals</td>
                    <td><b>${overall_total_rc}</b></td>
                    <td><b>${overall_total_ac}</b></td>`;

                    raw_dates.forEach(d => {
                        html += `<td><b>${daywise_rc_totals[d]}</b></td><td><b>${daywise_ac_totals[d]}</b></td>`;
                    });

                    html += `</tr></tbody></table>`;

                    let $wrapper = frm.fields_dict.dpr.$wrapper;
                    $wrapper.html(html);

                    $wrapper.find('.parent-row').click(function () {
                        let groupId = $(this).data('group');
                        let icon = $(this).find('.toggle-icon');
                        $wrapper.find(`.${groupId}`).toggle();
                        icon.text(icon.text() === '[+]' ? '[-]' : '[+]');
                    });

                } else {
                    frm.fields_dict.dpr.$wrapper.html("");
                }
            }
        });

    }
});
function update_day_labels(frm) {
    if (!frm.doc.start_date) return;

    let start_date = frappe.datetime.str_to_obj(frm.doc.start_date);

    for (let i = 0; i < 7; i++) {
        let date_str = frappe.datetime.add_days(frm.doc.start_date, i);
        let date = frappe.datetime.str_to_obj(date_str);

        let label = format_custom_date(date);

        let fieldname = `day_${i + 1}`;
        frm.fields_dict.task_allocation.grid.update_docfield_property(fieldname, "label", label);
        frm.fields_dict.task_allocation_agent.grid.update_docfield_property(fieldname, "label", label);
        frm.fields_dict.task_allocation_team_wise.grid.update_docfield_property(fieldname, "label", label);
    }

    frm.fields_dict.task_allocation.grid.refresh();
    frm.fields_dict.task_allocation_agent.grid.refresh();
    frm.fields_dict.task_allocation_team_wise.grid.refresh();
}

function format_custom_date(date) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const day = date.getDate();
    const month = months[date.getMonth()];
    return `${day} ${month}`;
}
function allocate_tasks(frm, project_name) {
    if (!project_name) {
        frappe.msgprint("Please select a Project first.");
        return;
    }

    is_bulk_allocating = true;

    frm.clear_table("task_allocation");
    frm.clear_table("task_allocation_team_wise");
    frm.clear_table("task_allocation_agent");
    frm.set_df_property("task_allocation_team_wise", "hidden", 0)
    let planner_rows = frm.doc.rec_task_planner || [];

    // filter planner rows by project
    let matched_tasks = planner_rows.filter(r => r.project === project_name);

    if (!matched_tasks.length) {
        frappe.msgprint("No matching tasks found in REC Task Planner for this project.");
        return;
    }

    matched_tasks.forEach(row => {

        // ---- TASK ALLOCATION ----
        let alloc = frm.add_child("task_allocation");
        alloc.task = row.task_id;
        alloc.priority = row.priority;
        alloc.vac = row.vac;
        alloc.sp = row.sp;
        alloc.subject = row.task;
        alloc.project = row.project;

        // ---- TASK ALLOCATION AGENT ----
        let agent = frm.add_child("task_allocation_agent");
        agent.task = row.task_id;
        agent.priority = row.priority;
        agent.vac = row.vac;
        agent.sp = row.sp;
        agent.subject = row.task;
        agent.project = row.project;
        let team = frm.add_child("task_allocation_team_wise");
        team.task = row.task_id;
        team.priority = row.priority;
        team.vac = row.vac;
        team.sp = row.sp;
        team.subject = row.task;
        team.project = row.project;
    });

    frm.refresh_field("task_allocation");
    frm.refresh_field("task_allocation_team_wise");
    frm.refresh_field("task_allocation_agent");

    frappe.msgprint("Tasks Updated Successfully");

    frm.save();

    // frappe.call({
    //     method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_project_html",
    //     args: { project_name },
    //     callback(r) {
    //         frm.get_field("project").$wrapper.html(r.message);
    //     }
    // });

    apply_grid_stripes(frm, "task_allocation");
    apply_grid_stripes(frm, "task_allocation_agent");
    apply_grid_stripes(frm, "task_allocation_team_wise");

    frm.scroll_to_field("task_allocation");
}
function apply_grid_stripes(frm, fieldname) {
    setTimeout(() => {
        let grid = frm.fields_dict[fieldname]?.grid;
        if (!grid) return;

        grid.grid_rows.forEach((row, index) => {
            $(row.wrapper).css({
                "background-color": index % 2 ? "#f2f2f2" : "transparent",
                "transition": "background-color 0.5s ease"
            });
        });
    }, 500);
}


function render_employee_strip(frm, selected_team = null) {
    let source_rows = [];

    if (selected_team) {
        source_rows = (frm.doc.allocation || []).filter(r =>
            r.team &&
            r.team.toLowerCase().trim() === selected_team.toLowerCase().trim()
        );
    } else {
        source_rows = frm.doc.allocation || [];
    }

    const employees = Array.from(
        new Set(
            source_rows
                .map(r => r.employee)
                .filter(Boolean)
        )
    );
    let sams_source = [];

    if (selected_team) {
        sams_source = (frm.doc.allocation_agent || []).filter(r =>
            r.team &&
            r.team.toLowerCase().trim() === selected_team.toLowerCase().trim()
        );
    } else {
        sams_source = frm.doc.allocation_agent || [];
    }

    const sams_ids = Array.from(
        new Set(
            sams_source
                .map(r => r.sams)
                .filter(Boolean)
        )
    );

    if (employees.length === 0 && sams_ids.length === 0) {
        frm.get_field("employee").$wrapper.html("<p>No employees or SAMS in allocation.</p>");
        return;
    }

    // RC maps
    const emp_rc_map = {};
    const sams_rc_map = {};

    (frm.doc.task_allocation || []).forEach(row => {
        if (!row.employee) return;
        emp_rc_map[row.employee] = (emp_rc_map[row.employee] || 0);
    });

    (frm.doc.allocation || []).forEach(row => {
        if (!row.employee) return;
        emp_rc_map[row.employee] = (emp_rc_map[row.employee] || 0) + (row.rc || 0);
    });
    (frm.doc.allocation_agent || []).forEach(row => {
        if (!row.sams) return;
        sams_rc_map[row.sams] = (sams_rc_map[row.sams] || 0) + (row.rc || 0);
    });
    (frm.doc.task_allocation_agent || []).forEach(row => {
        if (!row.sams) return;
        sams_rc_map[row.sams] = (sams_rc_map[row.sams] || 0);
    });


    // fetch employees
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Employee",
            filters: [
                ["name", "in", employees],
                ["department", "=", "Recruitment - THIS"]
            ],
            fields: ["name", "employee_name", "image", "department", "user_id"]
        },
        callback: function (r) {
            const data = r.message || [];

            let emp_html = "";
            if (data.length) {
                // emp_html = data.map(emp => {
                //     const total_rc = emp_rc_map[emp.name] || 0;
                //     return `
                //         <div style="display: inline-block; text-align: center; margin-right: 15px;">
                //             <img src="${emp.image || '/files/default-avatar.png'}"
                //                 style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%; border: 2px solid #007BFF;" />
                //             <div style="font-size: 12px; margin-top: 4px;">${emp.employee_name}</div>
                //             <div style="font-size: 11px; color: #555;">RC: ${total_rc}</div>
                //         </div>
                //     `;
                // }).join("");
                emp_html = data.map(emp => {
                    const total_rc = emp_rc_map[emp.name] || 0;
                    return `
                        <div class="emp-circle" 
                            data-employee="${emp.name}"
                            data-user="${emp.user_id || ''}"
                            style="display: inline-block; text-align: center; margin-right: 15px; cursor:pointer;">
                            
                            <img src="${emp.image || '/files/default-avatar.png'}"
                                style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%; border: 2px solid #007BFF;" />
                            
                            <div style="font-size: 12px; margin-top: 4px;">${emp.employee_name}</div>
                            <div style="font-size: 11px; color: #555;">RC: ${total_rc}</div>
                        </div>
                    `;
                }).join("");
            }

            // render sams ids
            let sams_html = "";
            if (sams_ids.length) {
                sams_html = sams_ids.map(sid => {
                    const total_rc = sams_rc_map[sid] || 0;
                    return `
                        <div style="display: inline-block; text-align: center; margin-right: 15px;">
                            <div style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid #28a745;
                                        display: flex; align-items: center; justify-content: center; overflow: hidden; background: #fff;">
                                <img src="/files/57ebc5e853default-avatar-icon-of-social-media-user-vector.jpg"
                                    style="width: 100%; height: 100%; object-fit: cover;" />
                            </div>

                            <div style="font-size: 12px; margin-top: 4px; font-weight: 600;">${sid}</div>
                            <div style="font-size: 11px; color: #555;">RC: ${total_rc}</div>
                        </div>
                    `;
                }).join("");
            }

            // frm.get_field("employee").$wrapper.html(`
            //     <div style="white-space: nowrap; overflow-x: auto; margin-top: 10px;">
            //         ${emp_html}
            //         ${sams_html}
            //     </div>
            // `);
            frm.get_field("employee").$wrapper.html(`
                <div class="emp-strip" style="white-space: nowrap; overflow-x: auto; margin-top: 10px;">
                    ${emp_html}
                    ${sams_html}
                </div>
            `);
            frm.get_field("employee").$wrapper
                .find(".emp-circle")
                .on("click", function () {

                    // let selected_employee = $(this).data("employee");
                    let selected_user = $(this).data("user");
                    frm.clear_table("task_allocation");

                    const start_date = frm.doc.start_date;
                    const allocation = frm.doc.allocation || [];
                    const task_map = {};
                    const date_map = {};

                    // Create date map (same as your team logic)
                    for (let i = 0; i < 7; i++) {
                        date_map[
                            frappe.datetime.add_days(start_date, i)
                        ] = `day_${i + 1}`;
                    }

                    allocation
                        .filter(r => r.exe === selected_user)
                        .forEach(task => {

                            const day_field = date_map[task.date];
                            if (!day_field) return;

                            const key = `${task.task}`;

                            let row = task_map[key];
                            if (!row) {
                                row = frm.add_child("task_allocation");
                                row.task = task.task;
                                row.subject = task.subject;
                                row.employee = task.employee;
                                row.rc = 0;
                                task_map[key] = row;
                            }

                            row[day_field] =
                                (row[day_field] || 0) + (task.rc || 0);

                            row.rc = Array.from({ length: 7 }, (_, i) =>
                                row[`day_${i + 1}`] || 0
                            ).reduce((a, b) => a + b, 0);
                        });

                    frm.refresh_field("task_allocation");
                });
        }
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

frappe.ui.form.on('REC Task Details', {
    rc(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },
    day_1(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },
    day_2(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },
    day_3(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },
    day_4(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },
    day_5(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },
    day_6(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },
    day_7(frm, cdt, cdn) {
        render_employee_strip(frm, null);
    },


})
frappe.ui.form.on('REC Agent Task Details', {
    rc(frm, cdt, cdn) {
        render_employee_strip(frm);
    },
    day_1(frm, cdt, cdn) {
        render_employee_strip(frm);
    },
    day_2(frm, cdt, cdn) {
        render_employee_strip(frm);
    },
    day_3(frm, cdt, cdn) {
        render_employee_strip(frm);
    },
    day_4(frm, cdt, cdn) {
        render_employee_strip(frm);
    },
    day_5(frm, cdt, cdn) {
        render_employee_strip(frm);
    },
    day_6(frm, cdt, cdn) {
        render_employee_strip(frm);
    },
    day_7(frm, cdt, cdn) {
        render_employee_strip(frm);
    },


})



function get_date_range(start, end) {
    let dates = [];
    let current = moment(start);
    let last = moment(end);

    while (current <= last) {
        dates.push({
            key: current.format("YYYY_MM_DD"), // field key
            label: current.format("D MMM")     // header label
        });
        current.add(1, "days");
    }
    return dates;
}


function format_custom_dates(date) {
    return moment(date).format("DD-MMM (ddd)");
}


function render_dev_team_logos(frm) {
    if (!frm.fields_dict.team) return;

    if (!document.getElementById("team-logo-style")) {
        $("head").append(`
            <style id="team-logo-style">
                .team-logo-row {
                    display: flex;
                    gap: 18px;
                    padding: 20px;
                    overflow-x: auto;
                    background: linear-gradient(135deg, #eef2f7, #dbe2ef);
                    border-radius: 12px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    margin: 15px 0;
                }
                .team-logo-circle {
                    width: 90px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    cursor: pointer;
                    transition: transform 0.3s;
                }
                .team-logo-circle:hover {
                    transform: scale(1.1);
                }
                .img-wrapper {
                    width: 90px;
                    height: 90px;
                    border-radius: 50%;
                    border: 2px solid #cbd5e1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                }
                .img-wrapper img {
                    width: 85%;
                    height: 85%;
                    border-radius: 50%;
                }
                .team-logo-rc {
                    margin-top: 6px;
                    font-weight: bold;
                    background: #2563eb;
                    color: #fff;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 12px;
                }
            </style>
        `);
    }

    const is_system_manager = frappe.user.has_role("System Manager");
    let team_wise_data = frm.doc.team_wise || [];

    /* ---------- GET USER TEAM ---------- */
    frappe.db.get_value(
        "Employee",
        { user_id: frappe.session.user },
        "custom_dev_team"
    ).then(res => {

        const user_team = res.message?.custom_dev_team || null;
        /* ---------- GET TEAM LOGOS ---------- */
        frappe.call({
            method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_dev_team_logos",
            args: { service: "REC-I" },
            callback(r) {

                if (!r.message || !r.message.length) {
                    frm.fields_dict.team.$wrapper.html(
                        "<p style='text-align:center;color:#888;'>No teams found</p>"
                    );
                    return;
                }

                let html = `<div class="team-logo-row">

                <div class="team-logo-circle" data-team="all_teams">
                            <div class="img-wrapper"   >
                                <img src="/assets/frappe/images/all_teams.png" style="width:135% !important; height:120% !important; margin-top:5px; ">
                            </div>
                            
                        </div>
                
                
                `;

                r.message.forEach(row => {

                    /* ---------- TEAM VISIBILITY RULE ---------- */
                    if (!is_system_manager && user_team) {
                        if (
                            row.name?.toLowerCase().trim() !==
                            user_team.toLowerCase().trim()
                        ) return;
                    }

                    let total_rc = team_wise_data
                        .filter(t =>
                            t.team &&
                            row.name &&
                            t.team.toLowerCase().trim() ===
                            row.name.toLowerCase().trim()
                        )
                        .reduce((sum, t) => sum + (t.rc || 0), 0);

                    let capacity = row.rec_capacity_per_day || 0;

                    html += `
                        <div class="team-logo-circle" data-team="${row.name}">
                            <div class="img-wrapper">
                                <img src="${row.logo}">
                            </div>
                            <div class="team-logo-rc">
                                ${total_rc} / ${capacity}
                            </div>
                        </div>
                    `;
                });

                html += `</div>`;
                frm.fields_dict.team.$wrapper.html(html);

                /* ---------- CLICK HANDLER ---------- */
                frm.fields_dict.team.$wrapper
                    .find(".team-logo-circle")
                    .on("click", function () {

                        frm.set_df_property(
                            "task_allocation_team_wise",
                            "hidden",
                            1
                        );

                        let clicked_team = $(this).data("team");

                        if (clicked_team === "all_teams") {
                            clicked_team = null;
                        }
                        frm.clear_table("task_allocation");

                        const start_date = frm.doc.start_date;
                        const allocation = frm.doc.team_wise || {};
                        const task_map = {};
                        const date_map = {};

                        for (let i = 0; i < 7; i++) {
                            date_map[
                                frappe.datetime.add_days(start_date, i)
                            ] = `day_${i + 1}`;
                        }


                        if (clicked_team) {
                            allocation
                                .filter(t =>
                                    t.team?.toLowerCase().trim() ===
                                    clicked_team.toLowerCase().trim()
                                )
                                .forEach(task => {

                                    const day_field = date_map[task.date];
                                    if (!day_field) return;

                                    const key = `${task.task}::${task.team}`;

                                    let row = task_map[key];
                                    if (!row) {
                                        row = frm.add_child("task_allocation");
                                        row.task = task.task;
                                        row.subject = task.subject;
                                        row.rc = 0;
                                        task_map[key] = row;
                                    }

                                    row[day_field] =
                                        (row[day_field] || 0) + (task.rc || 0);

                                    row.rc = Array.from({ length: 7 }, (_, i) =>
                                        row[`day_${i + 1}`] || 0
                                    ).reduce((a, b) => a + b, 0);
                                });
                        }
                        else {

                            allocation
                                .forEach(task => {

                                    const day_field = date_map[task.date];
                                    if (!day_field) return;

                                    const key = `${task.task}::${task.team}`;

                                    let row = task_map[key];
                                    if (!row) {
                                        row = frm.add_child("task_allocation");
                                        row.task = task.task;
                                        row.subject = task.subject;
                                        row.rc = 0;
                                        task_map[key] = row;
                                    }

                                    row[day_field] =
                                        (row[day_field] || 0) + (task.rc || 0);

                                    row.rc = Array.from({ length: 7 }, (_, i) =>
                                        row[`day_${i + 1}`] || 0
                                    ).reduce((a, b) => a + b, 0);
                                });
                        }




                        frm.refresh_field("task_allocation");
                        render_employee_strip(frm, clicked_team);
                    });
            }
        });
    });
}


async function build_sp_html(frm) {
    if (!frm.doc.start_date || !frm.doc.end_date) {
        frm.get_field("sp_html").$wrapper.html(
            "<b>Please select Start Date and End Date</b>"
        );
        return;
    }

    const headers = [
        "S.No", "SRC_S", "Project",
        "Task", "Territory", "SRC",
        "VAC", "FP", "SP", "SL", "LP", "PSL", "CC", "Team"
    ];
    const teams = await frappe.db.get_list('Dev Team', {
        fields: ['name']
    });

    const teamOptions = teams.map(t => t.name);

    const srcSOptions = ["", "SP", "FP", "SP/FP", "HLD", "JP"];
    const srcOptions = ["", "Portal", "Promo", "Agent", "PND"];

    const date_columns = get_date_range(
        frm.doc.start_date,
        frm.doc.end_date
    );

    const buildSelect = (options, value, field) => {
        let html = `<select class="form-control input-xs" data-field="${field}">`;
        options.forEach(opt => {
            html += `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt}</option>`;
        });
        html += `</select>`;
        return html;
    };

    let html = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <b>SUBMISSION (SP)</b>
            <div id="project_filter_link" style="width:200px;"></div>
            <div id="task_filter_link" style="width:180px;"></div>
            <button class="btn btn-primary btn-xs" onclick="update_sp_rows()">Update</button>
        </div>

        <div style="max-height:500px; overflow-y:auto; overflow-x:auto; border:1px solid #000; width:100%;">
<table style="width:max-content; min-width:100%; border-collapse:collapse; font-size:13px;">

        <thead style="position:sticky; top:0; background:#222; color:#fff;">
        <tr>
    `;

    // Static headers
    headers.forEach(h => {
        html += `<th style="border:1px solid #000; padding:6px;">${h}</th>`;
    });

    // Dynamic date headers
    date_columns.forEach(d => {
        html += `<th style="border:1px solid #000; padding:6px;">${d.label}</th>`;
    });

    html += `</tr></thead><tbody>`;

    let idx = 0;
    const selected_project = frm.doc.project_filter;
    const selected_task = frm.doc.task;
    (frm.doc.rec_task_planner || []).forEach(row => {

        if (row.src_s !== "SP") return;
        if (selected_project && row.project !== selected_project) return;
        if (selected_task && row.task_id !== selected_task) return;
        idx++;
        const bg = idx % 2 === 0 ? "#FDE9D9" : "#FFFFFF";

        html += `
            <tr data-row-name="${row.name}"
                style="background:${bg}; color:#000;">
                
                <td style="border:1px solid #000; text-align:center;">${idx}</td>

                <td style="border:1px solid #000;">
                    ${buildSelect(srcSOptions, row.src_s, "src_s")}
                </td>

                <td style="border:1px solid #000;text-align:left">${row.project_name || ""}</td>
                <td style="border:1px solid #000;width:90px; min-width:80px;text-align:left">${row.task || ""}</td>
                <td style="border:1px solid #000;">${row.territory || ""}</td>

                <td style="border:1px solid #000;">
                    ${buildSelect(srcOptions, row.src, "src")}
                </td>

                <td style="border:1px solid #000; text-align:center;">${row.vac || 0}</td>
                <td style="border:1px solid #000; text-align:center;">${row.fp || 0}</td>
                <td style="border:1px solid #000; text-align:center;">${row.sp || 0}</td>
                <td style="border:1px solid #000; text-align:center;">${row.sl || 0}</td>
                <td style="border:1px solid #000; text-align:center;">${row.lp || 0}</td>
                <td style="border:1px solid #000; text-align:center;">${row.psl || 0}</td>

                <td style="border:1px solid #000;width:50px; min-width:50px;">
                    <input class="form-control input-xs"
                        data-field="cc"
                        value="${row.cc || ""}">
                </td>
                <td>
                <select class="form-control input-xs" data-field="team">
                    <option value="">Select Team</option>
                    ${teamOptions.map(t =>
            `<option value="${t}" ${t === row.team ? "selected" : ""}>${t}</option>`
        ).join("")}
                </select>
            </td>
        `;

        // Date editable cells – INTEGER ONLY
        date_columns.forEach(d => {
            const fieldname = `day_${d.key}`;
            html += `
        <td style="border:1px solid #000;width:50px; min-width:50px;">
            <input type="text"
                class="form-control input-xs int-only"
                data-field="${fieldname}"
                value="${row[fieldname] || ""}">
        </td>`;
        });


        html += `</tr>`;
    });

    html += `</tbody></table></div>`;
    frm.get_field("sp_html").$wrapper
        .off("input", ".int-only")
        .on("input", ".int-only", function () {
            this.value = this.value.replace(/[^0-9]/g, '');
        });

    frm.get_field("sp_html").$wrapper.html(html);
}

async function build_spfp_html(frm) {

    if (!frm.doc.start_date || !frm.doc.end_date) {
        frm.get_field("spfp_html").$wrapper.html(
            "<b>Please select Start Date and End Date</b>"
        );
        return;
    }

    const headers = [
        "S.No", "SRC_S", "Project", "Task", "Territory", "SRC",
        "VAC", "FP", "SP", "SL", "LP", "PSL", "CC", "Team"
    ];

    const teams = await frappe.db.get_list("Dev Team", { fields: ["name"] });
    const teamOptions = teams.map(t => t.name);

    const srcSOptions = ["", "SP", "FP", "SP/FP", "HLD", "JP"];
    const srcOptions = ["", "Portal", "Promo", "Agent", "PND"];

    const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);

    const buildSelect = (options, value, field) => {
        let html = `<select class="form-control input-xs" data-field="${field}">`;
        options.forEach(opt => {
            html += `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt}</option>`;
        });
        html += `</select>`;
        return html;
    };

    let html = `
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <b>SUBMISSION / FEEDBACK (SP/FP)</b>
            
            <button class="btn btn-primary btn-xs" onclick="update_spfp_rows()">Update</button>
        </div>

       <div style="max-height:500px; overflow-y:auto; overflow-x:auto; border:1px solid #000; width:100%;">
        <table style="width:max-content; min-width:100%; border-collapse:collapse; font-size:13px;">

        <thead style="position:sticky; top:0; background:#222; color:#fff;">
        <tr>
    `;

    headers.forEach(h => html += `<th>${h}</th>`);
    date_columns.forEach(d => html += `<th>${d.label}</th>`);

    html += `</tr></thead><tbody>`;

    let idx = 0;
    const selected_project = frm.doc.sp_fp_project;
    const selected_task = frm.doc.sp_fp_task;
    (frm.doc.rec_task_planner || []).forEach(row => {

        if (row.src_s !== "SP/FP") return;
        if (selected_project && row.project !== selected_project) return;
        if (selected_task && row.task_id !== selected_task) return;
        idx++;
        const bg = idx % 2 === 0 ? "#FDE9D9" : "#FFFFFF";
        html += `
        <tr data-row-name="${row.name}" style="background:${bg}; color:#000;">
            <td style="border:1px solid #000; text-align:center;">${idx}</td>
            <td style="border:1px solid #000; text-align:center;">${buildSelect(srcSOptions, row.src_s, "src_s")}</td>
            <td style="border:1px solid #000; text-align:center;">${row.project_name || ""}</td>
            <td style="border:1px solid #000; text-align:center;width:90px; min-width:80px;text-align:left"">${row.task || ""}</td>
            <td style="border:1px solid #000; text-align:center;">${row.territory || ""}</td>
            <td style="border:1px solid #000; text-align:center;">${buildSelect(srcOptions, row.src, "src")}</td>
            <td style="border:1px solid #000; text-align:center;">${row.vac || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.fp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.sp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.sl || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.lp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.psl || 0}</td>

            <td style="border:1px solid #000; text-align:center;width:50px; min-width:50px;">
                <input class="form-control input-xs"
                    data-field="cc"
                    value="${row.cc || ""}">
            </td>

            <td style="border:1px solid #000; text-align:center;">
                <select class="form-control input-xs" data-field="team">
                    <option value="">Select Team</option>
                    ${teamOptions.map(t =>
            `<option value="${t}" ${t === row.team ? "selected" : ""}>${t}</option>`
        ).join("")}
                </select>
            </td>
        `;

        date_columns.forEach(d => {
            const field = `day_${d.key}`;
            html += `
                <td style="border:1px solid #000;width:60px; min-width:60px;">
                    <input type="text"
                        class="form-control input-xs int-only"
                        data-field="${field}"
                        value="${row[field] || ""}">
                </td>
            `;
        });

        html += `</tr>`;
    });

    html += `</tbody></table></div>`;

    frm.get_field("spfp_html").$wrapper.html(html);

    frm.get_field("spfp_html").$wrapper
        .off("input", ".int-only")
        .on("input", ".int-only", function () {
            this.value = this.value.replace(/[^0-9]/g, "");
        });
}

async function build_fp_html(frm) {

    if (!frm.doc.start_date || !frm.doc.end_date) {
        frm.get_field("spfp_html").$wrapper.html(
            "<b>Please select Start Date and End Date</b>"
        );
        return;
    }

    const headers = [
        "S.No", "SRC_S", "Project", "Task", "Territory", "SRC",
        "VAC", "FP", "SP", "SL", "LP", "PSL"
    ];

    const teams = await frappe.db.get_list("Dev Team", { fields: ["name"] });
    const teamOptions = teams.map(t => t.name);

    const srcSOptions = ["", "SP", "FP", "SP/FP", "HLD", "JP"];
    const srcOptions = ["", "Portal", "Promo", "Agent", "PND"];

    const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);

    const buildSelect = (options, value, field) => {
        let html = `<select class="form-control input-xs" data-field="${field}">`;
        options.forEach(opt => {
            html += `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt}</option>`;
        });
        html += `</select>`;
        return html;
    };

    let html = `
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <b>FEEDBACK (FP)</b>
            <button class="btn btn-primary btn-xs" onclick="update_fp_rows()">Update</button>
        </div>

        <div style="max-height:500px; overflow-y:auto; overflow-x:auto; border:1px solid #000; width:100%;">
<table style="width:max-content; min-width:100%; border-collapse:collapse; font-size:13px;">

        <thead style="position:sticky; top:0; background:#222; color:#fff;">
        <tr>
    `;

    headers.forEach(h => html += `<th>${h}</th>`);
    // date_columns.forEach(d => html += `<th>${d.label}</th>`);

    html += `</tr></thead><tbody>`;

    let idx = 0;
    const selected_project = frm.doc.fp_project;
    const selected_task = frm.doc.fp_task;
    (frm.doc.rec_task_planner || []).forEach(row => {

        if (row.src_s !== "FP") return;
        if (selected_project && row.project !== selected_project) return;
        if (selected_task && row.task_id !== selected_task) return;
        idx++;
        const bg = idx % 2 === 0 ? "#FDE9D9" : "#FFFFFF";
        html += `
        <tr data-row-name="${row.name}" style="background:${bg}; color:#000;">
            <td style="border:1px solid #000; text-align:center;">${idx}</td>
            <td style="border:1px solid #000; text-align:center;">${buildSelect(srcSOptions, row.src_s, "src_s")}</td>
            <td style="border:1px solid #000; text-align:center;">${row.project_name || ""}</td>
            <td style="border:1px solid #000; text-align:center;width:90px; min-width:80px;text-align:left"">${row.task || ""}</td>
            <td style="border:1px solid #000; text-align:center;">${row.territory || ""}</td>
            <td style="border:1px solid #000; text-align:center;">${buildSelect(srcOptions, row.src, "src")}</td>
            <td style="border:1px solid #000; text-align:center;">${row.vac || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.fp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.sp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.sl || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.lp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.psl || 0}</td>

            
        `;



        html += `</tr>`;
    });

    html += `</tbody></table></div>`;

    frm.get_field("fp_html").$wrapper.html(html);

    frm.get_field("fp_html").$wrapper
        .off("input", ".int-only")
        .on("input", ".int-only", function () {
            this.value = this.value.replace(/[^0-9]/g, "");
        });
}
async function build_pnd_html(frm) {

    if (!frm.doc.start_date || !frm.doc.end_date) {
        frm.get_field("spfp_html").$wrapper.html(
            "<b>Please select Start Date and End Date</b>"
        );
        return;
    }

    const headers = [
        "S.No", "SRC_S", "Project", "Task", "Territory", "SRC",
        "VAC", "FP", "SP", "SL", "LP", "PSL"
    ];

    const teams = await frappe.db.get_list("Dev Team", { fields: ["name"] });
    const teamOptions = teams.map(t => t.name);

    const srcSOptions = ["", "SP", "FP", "SP/FP", "HLD", "JP"];
    const srcOptions = ["", "Portal", "Promo", "Agent", "PND"];

    const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);

    const buildSelect = (options, value, field) => {
        let html = `<select class="form-control input-xs" data-field="${field}">`;
        options.forEach(opt => {
            html += `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt}</option>`;
        });
        html += `</select>`;
        return html;
    };

    let html = `
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <b>PENDING (PND)</b>
            <button class="btn btn-primary btn-xs" onclick="update_pnd_rows()">Update</button>
        </div>

        <div style="max-height:500px; overflow-y:auto; overflow-x:auto; border:1px solid #000; width:100%;">
<table style="width:max-content; min-width:100%; border-collapse:collapse; font-size:13px;">

           <thead style="position:sticky; top:0; background:#222; color:#fff;">
        <tr>
    `;

    headers.forEach(h => html += `<th>${h}</th>`);
    // date_columns.forEach(d => html += `<th>${d.label}</th>`);

    html += `</tr></thead><tbody>`;

    let idx = 0;
    const selected_project = frm.doc.pnd_project;
    const selected_task = frm.doc.pnd_task;
    (frm.doc.rec_task_planner || []).forEach(row => {

        if (row.src_s !== "HLD") return;
        if (selected_project && row.project !== selected_project) return;
        if (selected_task && row.task_id !== selected_task) return;

        idx++;
        const bg = idx % 2 === 0 ? "#FDE9D9" : "#FFFFFF";
        html += `
        <tr data-row-name="${row.name}"  style="background:${bg}; color:#000;">
            <td style="border:1px solid #000; text-align:center;">${idx}</td>
            <td style="border:1px solid #000; text-align:center;">${buildSelect(srcSOptions, row.src_s, "src_s")}</td>
            <td style="border:1px solid #000; text-align:center;">${row.project_name || ""}</td>
            <td style="border:1px solid #000; text-align:center;width:90px; min-width:80px;text-align:left"">${row.task || ""}</td>
            <td style="border:1px solid #000; text-align:center;">${row.territory || ""}</td>
            <td style="border:1px solid #000; text-align:center;">${buildSelect(srcOptions, row.src, "src")}</td>
            <td style="border:1px solid #000; text-align:center;">${row.vac || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.fp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.sp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.sl || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.lp || 0}</td>
            <td style="border:1px solid #000; text-align:center;">${row.psl || 0}</td>

            
        `;


        html += `</tr>`;
    });

    html += `</tbody></table></div>`;

    frm.get_field("pnd_html").$wrapper.html(html);

    frm.get_field("pnd_html").$wrapper
        .off("input", ".int-only")
        .on("input", ".int-only", function () {
            this.value = this.value.replace(/[^0-9]/g, "");
        });
}

window.update_sp_rows = async function () {

    const frm = cur_frm;
    frappe.dom.freeze(__("Updating Team-wise allocation..."));
    try {
        document.querySelectorAll("tr[data-row-name]").forEach(tr => {
            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child) return;

            tr.querySelectorAll("select, input").forEach(el => {
                const field = el.getAttribute("data-field");
                if (field) child[field] = el.value;
            });
        });

        frm.dirty();

        const existing = new Set();
        (frm.doc.team_wise || []).forEach(r => {
            existing.add(`${r.task}::${r.team}::${r.date}`);
        });

        const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);
        const date_map = {};

        date_columns.forEach((d, i) => {
            date_map[`day_${d.key}`] = frappe.datetime.add_days(frm.doc.start_date, i);
        });
        const task_updates = [];
        document.querySelectorAll("tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child) return;

            const team = tr.querySelector('select[data-field="team"]')?.value;
            task_updates.push({
                task_id: child.task_id,
                src: child.src,
                src_s: child.src_s,
                cc: child.cc,
                efd: child.efd || ""
            });
            if (!team) return;

            Object.keys(date_map).forEach(day_field => {

                const input = tr.querySelector(`input[data-field="${day_field}"]`);
                if (!input) return;

                const rc = cint(input.value);
                if (!rc || rc <= 0) return;

                const date = date_map[day_field];
                const key = `${child.task}::${team}::${date}`;

                const task_id = child.task_id;
                const task_subject = child.task;


                if (!existing.has(key)) {
                    const alloc = frm.add_child("team_wise");
                    alloc.task = task_id;
                    alloc.subject = task_subject;
                    alloc.team = team;
                    alloc.date = date;
                    alloc.rc = rc;
                    alloc.allocated = 1;

                    existing.add(key);
                }

            });
        });

        await frm.save();

        frm.refresh_field("team_wise");
        if (task_updates.length) {
            console.log("Updating task sources for:", task_updates);
            await frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.update_task_src",
                args: {
                    tasks: task_updates
                }
            });
        }
        build_sp_html(frm);

        frappe.show_alert({
            message: __("SP & Team-wise allocation updated successfully"),
            indicator: "green"
        });
    } finally {
        frappe.dom.unfreeze();
    }
};
window.update_spfp_rows = async function () {

    const frm = cur_frm;
    frappe.dom.freeze(__("Updating Team-wise allocation..."));
    /* Save HTML → child table */
    try {
        document.querySelectorAll("#spfp_html tr[data-row-name], tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child || child.src_s !== "SP/FP") return;

            tr.querySelectorAll("select, input").forEach(el => {
                const field = el.getAttribute("data-field");
                if (field) child[field] = el.value;
            });
        });
        frm.dirty();
        /* Existing keys */
        const existing = new Set();
        (frm.doc.team_wise || []).forEach(r => {
            existing.add(`${r.task}::${r.team}::${r.date}`);
        });

        const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);
        const date_map = {};

        date_columns.forEach((d, i) => {
            date_map[`day_${d.key}`] = frappe.datetime.add_days(frm.doc.start_date, i);
        });
        const task_updates = [];
        /* Read LIVE HTML */
        document.querySelectorAll("tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child || child.src_s !== "SP/FP") return;

            const team = tr.querySelector('select[data-field="team"]')?.value;
            task_updates.push({
                task_id: child.task_id,
                src: child.src,
                src_s: child.src_s,
                cc: child.cc,
                efd: child.efd || ""
            });
            if (!team) return;

            Object.keys(date_map).forEach(day_field => {

                const input = tr.querySelector(`input[data-field="${day_field}"]`);
                if (!input) return;

                const rc = cint(input.value);
                if (!rc || rc <= 0) return;

                const date = date_map[day_field];
                const task_id = child.task_id;
                const key = `${task_id}::${team}::${date}`;

                if (!existing.has(key)) {
                    const alloc = frm.add_child("team_wise");
                    alloc.task = task_id;
                    alloc.subject = child.task;
                    alloc.team = team;
                    alloc.date = date;
                    alloc.rc = rc;
                    alloc.allocated = 1;

                    existing.add(key);
                }
            });
        });

        await frm.save();

        frm.refresh_field("team_wise");
        if (task_updates.length) {
            await frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.update_task_src",
                args: {
                    tasks: task_updates
                }
            });
        }
        build_spfp_html(frm);
        build_sp_html(frm);

        frappe.show_alert({
            message: __("SP/FP rows updated successfully"),
            indicator: "green"
        });
    } finally {
        frappe.dom.unfreeze();
    }
};
window.update_fp_rows = async function () {

    const frm = cur_frm;
    frappe.dom.freeze(__("Updating Team-wise allocation..."));
    /* Save HTML → child table */
    try {
        document.querySelectorAll("#spfp_html tr[data-row-name], tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child || child.src_s !== "FP") return;

            tr.querySelectorAll("select, input").forEach(el => {
                const field = el.getAttribute("data-field");
                if (field) child[field] = el.value;
            });
        });
        frm.dirty();
        /* Existing keys */
        const existing = new Set();
        (frm.doc.team_wise || []).forEach(r => {
            existing.add(`${r.task}::${r.team}::${r.date}`);
        });

        const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);
        const date_map = {};

        date_columns.forEach((d, i) => {
            date_map[`day_${d.key}`] = frappe.datetime.add_days(frm.doc.start_date, i);
        });
        const task_updates = [];
        /* Read LIVE HTML */
        document.querySelectorAll("tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child || child.src_s !== "FP") return;

            const team = tr.querySelector('select[data-field="team"]')?.value;
            task_updates.push({
                task_id: child.task_id,
                src: child.src,
                src_s: child.src_s,
                cc: child.cc,
                efd: child.efd || ""
            });
            if (!team) return;

            Object.keys(date_map).forEach(day_field => {

                const input = tr.querySelector(`input[data-field="${day_field}"]`);
                if (!input) return;

                const rc = cint(input.value);
                if (!rc || rc <= 0) return;

                const date = date_map[day_field];
                const task_id = child.task_id;
                const key = `${task_id}::${team}::${date}`;

                if (!existing.has(key)) {
                    const alloc = frm.add_child("team_wise");
                    alloc.task = task_id;
                    alloc.subject = child.task;
                    alloc.team = team;
                    alloc.date = date;
                    alloc.rc = rc;
                    alloc.allocated = 1;

                    existing.add(key);
                }
            });
        });

        await frm.save();

        frm.refresh_field("team_wise");
        if (task_updates.length) {
            await frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.update_task_src",
                args: {
                    tasks: task_updates
                }
            });
        }
        build_fp_html(frm);

        frappe.show_alert({
            message: __("FP rows updated successfully"),
            indicator: "green"
        });
    } finally {
        frappe.dom.unfreeze();
    }
};
window.update_pnd_rows = async function () {

    const frm = cur_frm;
    frappe.dom.freeze(__("Updating Team-wise allocation..."));
    /* ---------------- Save HTML → child table ---------------- */
    try {
        document.querySelectorAll("tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child || child.src_s !== "HLD") return;

            tr.querySelectorAll("select, input").forEach(el => {
                const field = el.getAttribute("data-field");
                if (field) child[field] = el.value;
            });
        });

        frm.dirty();

        /* ---------------- Existing team_wise keys ---------------- */
        const existing = new Set();
        (frm.doc.team_wise || []).forEach(r => {
            existing.add(`${r.task}::${r.team}::${r.date}`);
        });

        /* ---------------- Date map ---------------- */
        const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);
        const date_map = {};

        date_columns.forEach((d, i) => {
            date_map[`day_${d.key}`] = frappe.datetime.add_days(frm.doc.start_date, i);
        });

        /* ---------------- Collect task updates ---------------- */
        const task_updates = [];

        document.querySelectorAll("tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            if (!child || child.src_s !== "HLD") return;

            const team = tr.querySelector('select[data-field="team"]')?.value;
            task_updates.push({
                task_id: child.task_id,
                src: child.src,
                src_s: child.src_s,
                cc: child.cc,
                efd: child.efd || ""
            });
            if (!team) return;



            Object.keys(date_map).forEach(day_field => {

                const input = tr.querySelector(`input[data-field="${day_field}"]`);
                if (!input) return;

                const rc = cint(input.value);
                if (!rc || rc <= 0) return;

                const date = date_map[day_field];
                const key = `${child.task_id}::${team}::${date}`;

                if (!existing.has(key)) {
                    const alloc = frm.add_child("team_wise");
                    alloc.task = child.task_id;
                    alloc.subject = child.task;
                    alloc.team = team;
                    alloc.date = date;
                    alloc.rc = rc;
                    alloc.allocated = 1;

                    existing.add(key);
                }
            });
        });

        /* ---------------- Save document ---------------- */
        await frm.save();
        frm.refresh_field("team_wise");

        /* ---------------- Update Task SRC & SRC_S ---------------- */
        if (task_updates.length) {
            await frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.update_task_src",
                args: {
                    tasks: task_updates
                }
            });
        }

        build_pnd_html(frm);

        frappe.show_alert({
            message: __("HLD rows updated successfully"),
            indicator: "green"
        });
    } finally {
        frappe.dom.unfreeze();
    }
};


async function build_master_table(frm) {

    console.log(frm.doc.rec_task_planner);
    if (!frm.doc.start_date || !frm.doc.end_date) {
        frm.get_field("client_html").$wrapper.html(
            "<b>Please select Start Date and End Date</b>"
        );
        return;
    }

    const selected_customer = frm.doc.customer || "";
    const selected_project = frm.doc.project_collapsible || "";
    const selected_task = frm.doc.task_collapsible || "";
    const selected_src = frm.doc.src_s || "";

    const teamOptions = [
        { code: "A", name: "ALPHA" },
        { code: "B", name: "BRAVO" },
        { code: "C", name: "CHARLIE" },
        { code: "D", name: "DELTA" }
    ];

    const srcSOptions = ["", "SP", "FP", "SP/FP", "HLD", "JP"];
    const statusOptions = ["", "Open", "Ready", "Working", "Code Review", "Pending Review", "Client Review", "Overdue", "Template", "Hold", "Completed", "Cancelled"];
    const sourcingMethods = await frappe.db.get_list("Sourcing Method", { fields: ["name"], limit: 100 });
    const sourcingMethodOptions = sourcingMethods.map(r => r.name);

    const taskIds = (frm.doc.rec_task_planner || []).map(r => r.task_id).filter(Boolean);
    const taskFields = {};
    if (taskIds.length) {
        const tasks = await frappe.db.get_list("Task", {
            filters: { name: ["in", taskIds] },
            fields: ["name", "status", "custom_task_sourcing_status"],
            limit: taskIds.length
        });
        tasks.forEach(t => {
            taskFields[t.name] = {
                status: t.status || "",
                src_s: t.custom_task_sourcing_status || "",
                sources: ""
            };
        });
        // custom_sourcing_method_multi is a Table MultiSelect on Task (Source Method
        // Child). End users usually lack read permission on that child DocType, so
        // fetch the values via the whitelisted server helper instead of querying the
        // child table directly from the client.
        const sourcesByTask = await frappe.call({
            method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_task_sources",
            args: { task_ids: taskIds },
            freeze: false
        }).then(r => (r.message || {}));
        Object.keys(taskFields).forEach(name => {
            taskFields[name].sources = sourcesByTask[name] || "";
        });
    }
    (frm.doc.rec_task_planner || []).forEach(row => {
        const tf = taskFields[row.task_id];
        if (tf) {
            row.status = tf.status;
            // SRC_S must always reflect the value stored on the Task document
            // (custom_task_sourcing_status), not the stale child-table copy.
            row.src_s = tf.src_s;
            row.sources = tf.sources;
        }
    });

    const ROW_HEIGHT = "42px";
    const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);


    const td_left =
        "border:1px solid #ccc;padding:2px 4px;height:26px;vertical-align:middle;text-align:left;";

    const td_center =
        "border:1px solid #ccc;padding:2px 4px;height:26px;vertical-align:middle;text-align:center;";
    const th_style = "border:1px solid #ccc;padding:5px;text-align:center;background:#2b177a;color:#fff;";
    const sub_th_style = `border:1px solid #ccc;padding:5px;text-align:center;background:#ff8c1a !important;color:#fff !important;font-weight:600;`;
    const ccStyle = (bg) => `height:30px;width:50px;min-height:20px;padding:1px 3px;text-align:center;background:${bg};border:1px solid #ffdab3;margin:auto;border-radius:6px;border: 2px solid orange !important;appearance:none;`;

    const dateStyle = (bg) => `width:50px;height:30px;text-align:center;margin:auto;background:${bg};border:1px solid #ffdab3;border-radius:6px;padding:0 4px;border: 2px solid orange !important;appearance:none;`;
    const buildStatusSelect = (value, bg) => {
        let html = `
    <select
        class="form-control input-xs"
        data-field="status"
        style="
            ${ccStyle(bg)}
            border: 2px solid orange !important;
            appearance:none;
            text-align:left;
        ">
    `;
        statusOptions.forEach(opt => {
            html += `<option value="${opt}" ${opt == value ? "selected" : ""}>${opt}</option>`;
        });
        html += `</select>`;
        return html;
    };

    const buildSourcesMultiSelect = (row, bg) => {
        const selectedValues = (row.sources || "").split(",").map(v => v.trim()).filter(Boolean);
        let html = `<div class="sources-multi-box" data-row-name="${row.name}" style="position:relative;">`;
        html += `<div class="sources-multi-display" style="height:30px;min-width:50px;max-width:180px;padding:1px 6px;text-align:center;background:${bg};border-radius:6px;border:2px solid orange !important;appearance:none;cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:inline-block;">`;
        html += selectedValues.join(",") || "Select";
        html += `</div>`;
        html += `</div>`;
        return html;
    };

    const buildSrcSelect = (value, bg) => {

        // let html = `
        // <select
        //     class="form-control input-xs"
        //     data-field="src_s"
        //     style="
        //         ${ccStyle(bg)}
        //         appearance:none;
        //     ">
        // `;

        // srcSOptions.forEach(opt => {
        //     html += `<option value="${opt}" ${opt == value ? "selected" : ""}>${opt}</option>`;
        // });


        // html += `</select>`;

        let html = `
    <select
        class="form-control input-xs"
        data-field="src_s"
        style="
            ${ccStyle(bg)}
            border: 2px solid orange !important;
            appearance:none;
        ">
    `;

        srcSOptions.forEach(opt => {
            html += `<option value="${opt}" ${opt == value ? "selected" : ""}>${opt}</option>`;
        });


        html += `</select>`;

        return html;
    };

    const grouped = {};

    (frm.doc.rec_task_planner || []).forEach(row => {

        if (selected_customer && row.client !== selected_customer) return;
        if (selected_project && row.project !== selected_project) return;
        if (selected_task && row.task_id !== selected_task) return;
        if (selected_src && row.src_s !== selected_src) return;

        const client = row.client || "No Client";
        const project = row.project_name || "No Project";

        // if (!grouped[client]) grouped[client] = {};
        if (!grouped[client]) {
            grouped[client] = {
                am: row.am || "",
                pm: row.pm || "",
                projects: {}
            };
        }
        if (!grouped[client].projects[project]) {
            grouped[client].projects[project] = [];
        }

        grouped[client].projects[project].push(row);
    });

    const headers = ["S.No", "Customer / Project", "AM/PM", "VAC", "SP", "FP", "SL", "LP", "PSL"];
    const widths = [
        "40px",   // S.No
        "370px",  // Customer / Project
        "70px",  // AM/PM
        "50px",   // VAC
        "50px",   // SP
        "50px",   // FP
        "50px",   // SL
        "50px",   // LP
        "50px"    // PSL
    ];
    let html = `

<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">

    <!-- LEFT SIDE -->
    <b style="font-size:15px; margin:0;">PROJECT PLANNER</b>

    <!-- RIGHT SIDE -->
    <div style="display:flex; gap:8px;">

        <button id="expand_toggle_btn" class="btn btn-primary btn-xs" onclick="toggle_expand_all()" style="padding:2px 6px;">
            Expand All
        </button>

        <button class="btn btn-success btn-xs" onclick="export_master_excel()" style="padding:2px 6px;">
            Export Excel
        </button>

        <button class="btn btn-primary btn-xs" onclick="update_master_table()" style="padding:2px 6px;">
            Update
        </button>
    </div>

</div>

<div style="
border:1px solid #ccc;
overflow:auto;
max-height:650px;
margin-top:15px;
position:relative;
background:#fff;
">

<table style="border-collapse:collapse;width:100%;font-size:13px;">

<thead style="background:#ff8c1a;">
<tr>`;

    // headers.forEach(h => {
    //     html += `<th style="${th_style}">${h}</th>`;
    // });

    headers.forEach((header, i) => {
        html += `
            <th style="${sub_th_style} width:${widths[i]}; min-width:${widths[i]};">
                ${header}
            </th>
        `;
    });

    html += `</tr></thead><tbody>`;

    let clientIdx = 0;

    Object.keys(grouped).forEach(client => {

        clientIdx++;
        const amcode = grouped[client].am || "NO AM";
        const pmcode = grouped[client].pm || "NO PM";
        // const clientColor = clientIdx % 2 === 0 ? "#f9fafb" : "#e3f2fd";
        // const clientColor = clientIdx % 2 === 0 ? "#ffffff" : "#fafafa";
        // const clientColor = clientIdx % 2 === 0 ? "#ffffff" : "#f0f0f0";
        const clientColor = clientIdx % 2 === 0 ? "#ffffff" : "#ffe6cc";
        let clientTotals = { vac: 0, sp: 0, fp: 0, sl: 0, lp: 0, psl: 0 };

        Object.keys(grouped[client].projects).forEach(project => {

            grouped[client].projects[project].forEach(r => {

                clientTotals.vac += cint(r.vac);
                clientTotals.sp += cint(r.sp);
                clientTotals.fp += cint(r.fp);
                clientTotals.sl += cint(r.sl);
                clientTotals.lp += cint(r.lp);
                clientTotals.psl += cint(r.psl);

            });

        });

        html += `
<tr class="client-row" data-client="${client}"
style="background:${clientColor};font-weight:bold;cursor:pointer;">

<td style="${td_center}">${clientIdx}</td>

<td style="${td_left}">
    <div style="display:flex;align-items:center;justify-content:flex-start;">
        <span class="toggle-icon"
              style="color:#0b3d91;font-size:18px;font-weight:bold;width:14px;text-align:center;">
            +
        </span>
        <span class="client-text" style="margin-left:6px;">
            ${client}
        </span>
    </div>
</td>
<td style="${td_center}">${amcode}</td>
<td style="${td_center}">${clientTotals.vac}</td>
<td style="${td_center}">${clientTotals.sp}</td>
<td style="${td_center}">${clientTotals.fp}</td>
<td style="${td_center}">${clientTotals.sl}</td>
<td style="${td_center}">${clientTotals.lp}</td>
<td style="${td_center}">${clientTotals.psl}</td>

</tr>`;

        let projectIdx = 0;

        Object.keys(grouped[client].projects).forEach(project => {

            projectIdx++;

            // const projectColor = projectIdx % 2 === 0 ? "#d1c4e9" : "#ede7f6";
            // const projectColor = projectIdx % 2 === 0 ? "#e6f2ff" : "#e5ecff";
            const projectColor = projectIdx % 2 === 0 ? "#ffffff" : "#fafafa";
            let projectTotals = { vac: 0, sp: 0, fp: 0, sl: 0, lp: 0, psl: 0 };

            grouped[client].projects[project].forEach(r => {

                projectTotals.vac += cint(r.vac);
                projectTotals.sp += cint(r.sp);
                projectTotals.fp += cint(r.fp);
                projectTotals.sl += cint(r.sl);
                projectTotals.lp += cint(r.lp);
                projectTotals.psl += cint(r.psl);

            });

            html += `
<tr class="project-row"
data-client="${client}"
data-project="${project}"
style="display:none;background:${projectColor};font-weight:bold;cursor:pointer;">

<td style="${td_center}">${projectIdx}</td>

<td style="${td_left};padding-left:20px;">
    <div style="display:flex;align-items:center;justify-content:flex-start;">
        <span class="toggle-icon"
              style="color:#0b3d91;font-size:18px;font-weight:bold;width:14px;text-align:center;">
            +
        </span>
        <span class="project-text" style="margin-left:6px;">
            ${project}
        </span>
    </div>
</td>
<td style="${td_center}">${pmcode}</td>

<td style="${td_center}">${projectTotals.vac}</td>
<td style="${td_center}">${projectTotals.sp}</td>
<td style="${td_center}">${projectTotals.fp}</td>
<td style="${td_center}">${projectTotals.sl}</td>
<td style="${td_center}">${projectTotals.lp}</td>
<td style="${td_center}">${projectTotals.psl}</td>

</tr>`;

            html += `
<tr class="task-table-row"
data-client="${client}"
data-project="${project}"
style="display:none;">

<td colspan="9" style="padding:0;">

<div style="overflow-x:auto;width:100%;">

<table
    style="
        border-collapse:collapse;
        table-layout:fixed;
        width:860px;
        min-width:860px;
        font-size:12px;
    ">

<thead>
<tr>

<th style="${sub_th_style}width:40px;">S.No</th>
<th style="${sub_th_style}width:70px;">Task</th>
<th style="${sub_th_style}width:210px;">Subject</th>
<th style="${sub_th_style}width:70px;">Territory</th>

<th style="${sub_th_style}width:90px;">Status</th>

<th style="${sub_th_style}width:150px;">Sources</th>

<th style="${sub_th_style}width:70px;">SRC_S</th>

<th style="${sub_th_style}width:40px;">VAC</th>
<th style="${sub_th_style}width:40px;">FP</th>
<th style="${sub_th_style}width:40px;">SP</th>
<th style="${sub_th_style}width:40px;">SL</th>
<th style="${sub_th_style}width:40px;">LP</th>
<th style="${sub_th_style}width:40px;">PSL</th>

<th style="${sub_th_style}width:100px;">CC/EFD</th>

<th
    class="bulk-team-allocation"
    style="
        ${sub_th_style}
        width:80px;
        cursor:pointer;
        text-decoration:underline;
        
    ">
    TEAM
</th>
`;

            // date_columns.forEach(d => {
            //     html += `<th style="${th_style}width:40px;">${d.label}</th>`;
            // });

            html += `</tr></thead><tbody>`;

            let taskIdx = 0;

            grouped[client].projects[project].forEach((row, i) => {

                taskIdx++;

                // const rowColor = i % 2 === 0 ? "#f3f3f3" : "#e7d2bf";
                // const rowColor = i % 2 === 0 ? "#e6e6e6" : "#dcdcdc";
                const rowColor = i % 2 === 0 ? "#ffffff" : "#ffdab3";
                const inputBg = i % 2 === 0 ? "#ffdab3" : "#ffffff";
                const inputBorder = "#ffdab3";


                html += `
<tr data-row-name="${row.name}" style="background:${rowColor};">

<td style="${td_center}">${taskIdx}</td>

<td style="${td_center}">
    <a href="/app/task/${encodeURIComponent(row.task_id)}" target="_blank">
        ${row.task_id || ""}
    </a>
</td>

<td style="${td_left}">${row.task || ""}</td>

<td style="${td_center}">${row.territory || ""}</td>

<td style="${td_center}">
${buildStatusSelect(row.status, inputBg)}
</td>

<td style="${td_center}">
${buildSourcesMultiSelect(row, inputBg)}
</td>

<td style="${td_center}">
${buildSrcSelect(row.src_s, inputBg)}
</td>

<td style="${td_center}">${row.vac || 0}</td>
<td style="${td_center}">${row.fp || 0}</td>
<td style="${td_center}">${row.sp || 0}</td>
<td style="${td_center}">${row.sl || 0}</td>
<td style="${td_center}">${row.lp || 0}</td>
<td style="${td_center}">${row.psl || 0}</td>

<td style="
    border:1px solid #ccc;
    text-align:center;
    vertical-align:middle;
    padding:0;
    height:32px;
">

${row.src_s === "FP"
                        ? `<div class="fp-date"
            data-value="${row.efd || ""}"
            style="
                height:${ROW_HEIGHT};
                display:flex;
                align-items:center;
                justify-content:center;
                
            ">
       </div>`
                        : `<input
        type="text"
        class="form-control input-xs"
        data-field="cc"
        value="${row.cc || ""}"
        style="${ccStyle(inputBg)}">`
                    }

</td>


<td
    style="
        border:1px solid #ccc;
        text-align:center;
        cursor:pointer;
        width:80px;
        font-size:11px;
        
    "
    class="team-select"
    data-row="${row.name}">

    <div style="
        width:60px;
        height:30px;
        line-height:30px;
        margin:auto;
        border:1px solid #ffdab3;
        border-radius:6px;
        background:${inputBg};
        text-align:center;
        border: 2px solid orange !important;
        appearance:none;
    ">
        ${(row.team || "")
                        .split(",")
                        .map(t => teamOptions.find(o => o.name === t)?.code || "")
                        .join(",") || "Select"
                    }
    </div>

</td>
`;


                html += `</tr>`;
            });

            html += `</tbody></table></div></td></tr>`;
        });
    });

    html += `</tbody></table></div>`;

    const wrapper = frm.get_field("client_html").$wrapper;
    wrapper.attr("id", "client_html");
    wrapper.html(html);



    // wrapper.find(".fp-date").each(function () {

    //     const control = frappe.ui.form.make_control({
    //         parent: this,
    //         df: {
    //             fieldtype: "Date",
    //             fieldname: "efd"
    //         },
    //         render_input: true
    //     });

    //     control.set_value($(this).data("value"));

    //     const rowName = $(this).closest("tr").data("row-name");
    //     const child = frappe.model.get_doc("REC Task Planner", rowName);

    //     control.$input.on("change", function () {
    //         child.efd = control.get_value();
    //         console.log("Page Load FP Date:", child.efd);
    //     });
    //     $(control.$wrapper).css({
    //         "margin": "0",
    //         "padding": "0"
    //     });

    //     $(control.$input).attr("style", dateStyle);

    // });



    wrapper.find(".fp-date").each(function () {

        const control = frappe.ui.form.make_control({
            parent: this,
            df: {
                fieldtype: "Date",
                fieldname: "efd"
            },
            render_input: true
        });

        const rowName = $(this).closest("tr").data("row-name");
        const child = frappe.model.get_doc("REC Task Planner", rowName);

        control.set_value($(this).data("value"));

        // Display DD-MM on page load
        if (child.efd) {
            setTimeout(() => {
                const [year, month, day] = child.efd.split("-");
                control.$input[0].value = `${day}-${month}`;
            }, 0);
        }

        control.$input.on("change", function () {

            child.efd = control.get_value();

            console.log("Stored:", child.efd);

            if (child.efd) {
                setTimeout(() => {
                    const [year, month, day] = child.efd.split("-");
                    control.$input[0].value = `${day}-${month}`;
                }, 0);
            }

        });

        $(control.$wrapper).css({
            display: "flex",
            "align-items": "center",
            "justify-content": "center",
            height: "100%",
            margin: "0",
            padding: "0"
        });

        $(control.$wrapper).find(".frappe-control").css({
            margin: "0",
            padding: "0",
            minHeight: "0",
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        });

        $(control.$wrapper).find(".control-input-wrapper").css({
            margin: "0",
            padding: "0",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
        });

        $(control.$wrapper).css({
            display: "flex",
            "align-items": "center",
            "justify-content": "center",
            height: "100%",
            margin: "0",
            padding: "0"
        });

        const tr = $(this).closest("tr");
        const inputBg = tr.index() % 2 === 0 ? "#ffdab3" : "#ffffff";

        $(control.$input).css({
            width: "70px",
            height: "30px",
            margin: "0",
            padding: "0 4px",
            lineHeight: "30px",
            textAlign: "center",
            background: inputBg,
            border: "1px solid #ffdab3",
            borderRadius: "6px"
        });
        const td = $(this).closest("td");

        td.css({
            height: "42px",
            minHeight: "42px",
            padding: "0",
            verticalAlign: "middle"
        });




        $(control.$input).attr("style", dateStyle(inputBg));

    });

    wrapper.off("input", ".int-only").on("input", ".int-only", function () {
        this.value = this.value.replace(/[^0-9]/g, "");
    });

    wrapper.off("click", ".sources-multi-display").on("click", ".sources-multi-display", function (e) {
        e.stopPropagation();
        const box = $(this).closest(".sources-multi-box");
        const rowName = box.data("row-name");
        $(".sources-multi-dropdown").hide();
        let dropdown = $("#sources-dropdown-global");
        if (dropdown.length && dropdown.data("row-name") === rowName && dropdown.is(":visible")) {
            dropdown.hide();
            return;
        }
        if (!dropdown.length) {
            dropdown = $('<div id="sources-dropdown-global" class="sources-multi-dropdown" style="display:none; position:fixed; z-index:99999; background:#fff; border:1px solid #ffdab3; border-radius:6px; padding:4px; max-height:150px; overflow-y:auto; min-width:120px; box-shadow:0 4px 12px rgba(0,0,0,0.3);"></div>');
            $("body").append(dropdown);
        }
        const child = frappe.model.get_doc("REC Task Planner", rowName);
        const selectedValues = (child && child.sources || "").split(",").map(v => v.trim()).filter(Boolean);
        dropdown.empty();
        dropdown.data("row-name", rowName);
        sourcingMethodOptions.forEach(opt => {
            const checked = selectedValues.includes(opt) ? "checked" : "";
            dropdown.append(`<label style="display:block; padding:2px 4px; font-size:11px; white-space:nowrap;"><input type="checkbox" class="sources-multi-checkbox" value="${opt}" ${checked} style="margin-right:4px;">${opt}</label>`);
        });
        const rect = this.getBoundingClientRect();
        dropdown.css({
            top: rect.bottom + window.scrollY,
            left: rect.left + window.scrollX
        }).show();
    });

    $(document).off("change.sources-multi", ".sources-multi-checkbox").on("change.sources-multi", ".sources-multi-checkbox", function () {
        const dropdown = $("#sources-dropdown-global");
        const rowName = dropdown.data("row-name");
        const checked = dropdown.find(".sources-multi-checkbox:checked");
        const values = Array.from(checked).map(c => c.value);
        const child = frappe.model.get_doc("REC Task Planner", rowName);
        if (child) {
            child.sources = values.join(",");
        }
        const box = $(`.sources-multi-box[data-row-name="${rowName}"]`);
        const display = box.find(".sources-multi-display");
        display.text(values.join(",") || "Select");
    });

    $(document).off("click.sources-multi").on("click.sources-multi", function (e) {
        if (!$(e.target).closest(".sources-multi-box").length && !$(e.target).closest("#sources-dropdown-global").length) {
            $("#sources-dropdown-global").hide();
        }
    });

    wrapper.off("change", "select[data-field='src_s']")
        .on("change", "select[data-field='src_s']", function () {

            const src = $(this).val();

            const tr = $(this).closest("tr");
            const rowName = tr.data("row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);
            const ccCell = tr.find("td").eq(13);
            const efdCell = tr.find("td").eq(14);

            if (src === "HLD" || src === "JP") {
                ccCell.empty();
                // ccCell.hide();
                efdCell.hide();
                // efdCell.empty();
                ccCell.css({
                    height: "42px",
                    minHeight: "42px",
                    padding: "0",
                    verticalAlign: "middle",
                    border: "1px solid #ccc"
                });
                efdCell.css({
                    height: "42px",
                    minHeight: "42px",
                    padding: "0",
                    verticalAlign: "middle",
                    border: "1px solid #ccc"
                });
                return;
            }

            ccCell.show();
            efdCell.show();
            ccCell.empty();

            if (src === "FP") {

                efdCell.hide();
                const div = $('<div style="margin:0;padding:0;"></div>').appendTo(ccCell);

                const control = frappe.ui.form.make_control({
                    parent: div,
                    df: {
                        fieldtype: "Date",
                        fieldname: "efd"
                    },
                    render_input: true
                });

                control.refresh();

                ccCell.css({
                    height: "42px",
                    minHeight: "42px",
                    padding: "0",
                    verticalAlign: "middle"
                });

                $(control.$wrapper).css({
                    height: "42px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center"
                });

                // If value already exists, show DD-MM
                if (child.efd) {
                    control.set_value(child.efd);

                    setTimeout(() => {
                        const [year, month, day] = child.efd.split("-");
                        control.$input[0].value = `${day}-${month}`;
                    }, 0);
                }

                control.$input.on("change", function () {

                    // Store full date
                    child.efd = control.get_value();

                    console.log("EFD :", child.efd);

                    // Display only DD-MM
                    if (child.efd) {
                        setTimeout(() => {
                            const [year, month, day] = child.efd.split("-");
                            control.$input[0].value = `${day}-${month}`;
                        }, 0);
                    }

                });

                $(control.wrapper).css({
                    margin: "0",
                    padding: "0",
                    "min-height": "20px"
                });

                $(control.wrapper).find(".control-input-wrapper").css({
                    margin: "0",
                    padding: "0"
                });

                const tr = $(this).closest("tr");
                const inputBg = tr.index() % 2 === 0 ? "#ffdab3" : "#ffffff";

                $(control.$input).css({
                    width: "70px",
                    height: "30px",
                    margin: "0",
                    padding: "0 4px",
                    lineHeight: "30px",
                    textAlign: "center",
                    background: inputBg,
                    border: "1px solid #ffdab3",
                    borderRadius: "6px"
                });

                // $(control.$input).attr("style", dateStyle);
                $(control.$input).attr("style", dateStyle(inputBg));

            } else {

                const tr = $(this).closest("tr");
                const inputBg = tr.index() % 2 === 0 ? "#ffdab3" : "#ffffff";

                ccCell.html(`
                    <input
                        type="text"
                        class="form-control input-xs"
                        data-field="cc"
                        value="${child.cc || ""}"
                        style="${ccStyle(inputBg)}">
                `);

                // Fixed row height
                ccCell.css({
                    height: "42px",
                    minHeight: "42px",
                    padding: "0",
                    verticalAlign: "middle"
                });

            }

        });


    wrapper.off("click", ".client-row").on("click", ".client-row", function () {

        const client = $(this).data("client");

        const projectRows = $(`.project-row[data-client="${client}"]`);
        const taskRows = $(`.task-table-row[data-client="${client}"]`);

        const icon = $(this).find(".toggle-icon");

        if (projectRows.is(":visible")) {

            projectRows.hide();
            taskRows.hide();

            // Reset all project icons
            projectRows.each(function () {
                $(this).find(".toggle-icon").text("+");
            });

            icon.text("+");

        } else {

            projectRows.show();
            icon.text("−");

        }

    });

    wrapper.off("click", ".project-row").on("click", ".project-row", function () {

        const client = $(this).data("client");
        const project = $(this).data("project");

        const rows = $(`.task-table-row[data-client="${client}"][data-project="${project}"]`);

        rows.toggle();

        const icon = $(this).find(".toggle-icon");

        if (rows.is(":visible")) {
            icon.text("−");
        } else {
            icon.text("+");
        }

    });
    wrapper.off("click", ".team-select").on("click", ".team-select", async function () {

        const rowname = $(this).data("row");
        const child = frappe.model.get_doc("REC Task Planner", rowname);

        const existing = (child.team || "").split(",");

        let fields = [];
        const r = await frappe.call({
            method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_holidays",
            args: {
                start_date: frm.doc.start_date,
                end_date: frm.doc.end_date
            }
        });

        const holidaySet = new Set(
            (r.message || []).map(d => d.holiday_date)
        );
        /* Show Selected Position */

        fields.push({
            fieldtype: "HTML",
            fieldname: "position_html"
        });

        fields.push({ fieldtype: "Section Break" });

        /* Team Selection */

        fields.push({
            fieldtype: "MultiCheck",
            fieldname: "teams",
            label: "Select Teams",
            columns: 4,
            options: teamOptions.map(t => ({
                label: t.name,
                value: t.name,
                checked: existing.includes(t.name)
            }))
        });

        fields.push({ fieldtype: "Section Break" });


        date_columns.forEach((d, i) => {

            const date = frappe.datetime.add_days(frm.doc.start_date, i);

            const label = holidaySet.has(date)
                ? `${d.label} (H)`
                : d.label;

            fields.push({
                fieldtype: "Int",
                label: label,
                fieldname: `rc_${i}`,
                default: 0
            });

            if ((i + 1) % 6 === 0 && i !== date_columns.length - 1) {
                fields.push({ fieldtype: "Section Break" });
            } else {
                fields.push({ fieldtype: "Column Break" });
            }

        });


        const dialog = new frappe.ui.Dialog({

            title: "RC Allocation",
            size: "large",
            fields: fields,
            primary_action_label: "Add Allocation",

            async primary_action(values) {

                frappe.dom.freeze("Creating Team Allocation...");

                try {

                    const teams = values.teams || [];
                    // ---------------- Holiday RC Validation ----------------

                    const ccValue = cint(child.cc || 0);

                    if (ccValue > 0) {

                        // let totalRC = 0;

                        // date_columns.forEach((d, i) => {

                        //     const rc = cint(dialog.get_value(`rc_${i}`) || 0);

                        //     console.log(
                        //         frappe.datetime.add_days(frm.doc.start_date, i),
                        //         rc
                        //     );

                        //     totalRC += rc;
                        // });

                        // Existing RC from team_wise
                        let existingRC = 0;

                        (frm.doc.team_wise || []).forEach(r => {

                            // Current task-க்கு மட்டும்
                            if (r.task === child.task_id) {
                                existingRC += cint(r.rc || 0);
                            }

                        });

                        // New RC entered in dialog
                        let newRC = 0;

                        date_columns.forEach((d, i) => {
                            newRC += cint(dialog.get_value(`rc_${i}`) || 0);
                        });

                        // Existing + New
                        const totalRC = existingRC + newRC;

                        console.log("Existing RC :", existingRC);
                        console.log("New RC :", newRC);
                        console.log("Total RC :", totalRC);
                        console.log("CC :", ccValue);

                        // const isCEO = frappe.user_roles.includes("CEO");
                        // if (!isCEO && newRC < ccValue) {

                        //     frappe.msgprint({
                        //         title: __("Validation Error"),
                        //         indicator: "red",
                        //         message: __(
                        //             `Total RC Allocation (${newRC}) cannot be less than CC (${ccValue}).`
                        //         )
                        //     });

                        //     return;
                        // }
                        const allowedUsers = [
                            "sangeetha.s@groupteampro.com",
                            "aruna.g@groupteampro.com",
                            "lokeshkumar.a@groupteampro.com",
                            "mercy@groupteampro.com"
                        ];

                        const hasAccess = allowedUsers.includes(frappe.session.user);

                        if (!hasAccess && newRC < ccValue) {
                            frappe.msgprint({
                                title: __("Validation Error"),
                                indicator: "red",
                                message: __(
                                    `Total RC Allocation (${newRC}) cannot be less than CC (${ccValue}).`
                                )
                            });

                            return;
                        }
                    }

                    if (!teams.length) {
                        frappe.msgprint("Please select at least one team");
                        return;
                    }

                    child.team = teams.join(",");

                    /* existing allocation set */

                    const existing = new Set();

                    (frm.doc.team_wise || []).forEach(r => {
                        existing.add(`${r.task}::${r.team}::${r.date}`);
                    });

                    date_columns.forEach((d, i) => {

                        const rc = cint(values[`rc_${i}`]);
                        if (!rc) return;

                        const date = frappe.datetime.add_days(frm.doc.start_date, i);

                        teams.forEach(team => {

                            const key = `${child.task_id}::${team}::${date}`;


                            const existingRow = (frm.doc.team_wise || []).find(r =>
                                r.task === child.task_id &&
                                r.team === team &&
                                r.date === date
                            );

                            if (existingRow) {
                                existingRow.rc = cint(existingRow.rc || 0) + rc;
                                existingRow.allocated = 1;

                                return;
                            }

                            const alloc = frm.add_child("team_wise");

                            alloc.task = child.task_id;
                            alloc.subject = child.task;
                            alloc.team = team;
                            alloc.date = date;
                            alloc.rc = rc;
                            alloc.allocated = 1;

                            existing.add(key);

                        });

                    });

                    frm.refresh_field("team_wise");

                    frappe.show_alert({
                        message: "Team allocation created",
                        indicator: "green"
                    });

                    dialog.hide();

                }
                finally {

                    frappe.dom.unfreeze();

                }

            }

        });

        dialog.show();
        dialog.$wrapper.find(".control-label").each(function () {

            const txt = $(this).text();

            if (txt.includes("(H)")) {

                $(this).html(
                    txt.replace(
                        "(H)",
                        '<span style="color:#ff0000;font-weight:bold;">(H)</span>'
                    )
                );

            }

        });

        dialog.fields_dict.position_html.$wrapper.html(
            `<div style="
            font-size:15px;
            font-weight:600;
            margin-bottom:10px;
            color:#2b177a;">
            Position : ${child.task || ""}
        </div>`
        );

    });



    wrapper.off("click", ".bulk-team-allocation")
        .on("click", ".bulk-team-allocation", async function () {
            const children = [];

            const table = $(this).closest("table");

            table.find("tbody tr[data-row-name]").each(function () {

                const child = frappe.model.get_doc(
                    "REC Task Planner",
                    $(this).data("row-name")
                );

                if (child) {
                    children.push(child);
                }

            });

            console.log(children.length);
            if (!children.length) {

                frappe.msgprint("No Tasks Found");
                return;

            }
            open_bulk_team_allocation(frm, children);
        });


}


async function open_bulk_team_allocation(frm, children) {

    const existing = (children[0]?.team || "").split(",");

    let fields = [];

    const r = await frappe.call({
        method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.get_holidays",
        args: {
            start_date: frm.doc.start_date,
            end_date: frm.doc.end_date
        }
    });

    const holidaySet = new Set(
        (r.message || []).map(d => d.holiday_date)
    );

    const date_columns = get_date_range(
        frm.doc.start_date,
        frm.doc.end_date
    );

    const teamOptions = [
        { code: "A", name: "ALPHA" },
        { code: "B", name: "BRAVO" },
        { code: "C", name: "CHARLIE" },
        { code: "D", name: "DELTA" }
    ];

    /* Position */

    fields.push({
        fieldtype: "HTML",
        fieldname: "position_html"
    });

    fields.push({ fieldtype: "Section Break" });

    /* Team Selection */

    fields.push({
        fieldtype: "MultiCheck",
        fieldname: "teams",
        label: "Select Teams",
        columns: 4,
        options: teamOptions.map(t => ({
            label: t.name,
            value: t.name,
            checked: existing.includes(t.name)
        }))
    });

    fields.push({ fieldtype: "Section Break" });

    /* Date Fields */

    date_columns.forEach((d, i) => {

        const date = frappe.datetime.add_days(frm.doc.start_date, i);

        const label = holidaySet.has(date)
            ? `${d.label} (H)`
            : d.label;

        fields.push({
            fieldtype: "Int",
            label: label,
            fieldname: `rc_${i}`,
            default: 0
        });

        if ((i + 1) % 6 === 0 && i !== date_columns.length - 1) {
            fields.push({ fieldtype: "Section Break" });
        } else {
            fields.push({ fieldtype: "Column Break" });
        }

    });

    const dialog = new frappe.ui.Dialog({

        title: "RC Allocation",
        size: "large",
        fields: fields,
        primary_action_label: "Add Allocation",

        async primary_action(values) {

            frappe.dom.freeze("Creating Team Allocation...");

            try {

                const teams = values.teams || [];

                // ---------- Bulk CC Validation ----------

                const totalCC = children
                    .filter(r => (r.src_s || "").trim() !== "FP")
                    .reduce((total, r) => {
                        return total + cint(r.cc || 0);
                    }, 0);

                let totalRC = 0;

                date_columns.forEach((d, i) => {
                    totalRC += cint(dialog.get_value(`rc_${i}`) || 0);
                });

                console.log("Total CC :", totalCC);
                console.log("Total RC :", totalRC);
                const isCEO = frappe.user_roles.includes("CEO");
                if (!isCEO && totalRC < totalCC) {

                    frappe.msgprint({
                        title: __("Validation Error"),
                        indicator: "red",
                        message: __(
                            `Total RC Allocation (${totalRC}) cannot be less than Total CC (${totalCC}).`
                        )
                    });

                    return;
                }

                if (!teams.length) {
                    frappe.msgprint("Please select at least one team");
                    return;
                }

                children.forEach(child => {
                    child.team = teams.join(",");
                    console.log(r.task, r.src_s, r.cc);
                });

                // const existing = new Set();

                // (frm.doc.team_wise || []).forEach(r => {
                //     existing.add(`${r.task}::${r.team}::${r.date}`);
                // });

                children.forEach(child => {

                    date_columns.forEach((d, i) => {

                        const rc = cint(values[`rc_${i}`]);
                        if (!rc) return;

                        const date = frappe.datetime.add_days(frm.doc.start_date, i);

                        teams.forEach(team => {

                            const key = `${child.task_id}::${team}::${date}`;

                            const existingRow = (frm.doc.team_wise || []).find(r =>
                                r.task === child.task_id &&
                                r.team === team &&
                                r.date === date
                            );

                            if (existingRow) {

                                // Already exists -> Add the new RC to existing RC
                                existingRow.rc = cint(existingRow.rc || 0) + rc;
                                existingRow.allocated = 1;

                            } else {

                                const alloc = frm.add_child("team_wise");

                                alloc.task = child.task_id;
                                alloc.subject = child.task;
                                alloc.team = team;
                                alloc.date = date;
                                alloc.rc = rc;
                                alloc.allocated = 1;

                            }

                        });

                    });

                });

                frm.refresh_field("team_wise");

                frappe.show_alert({
                    message: "Team Allocation Created",
                    indicator: "green"
                });

                dialog.hide();

            }
            finally {
                frappe.dom.unfreeze();
            }

        }

    });

    dialog.show();

    dialog.$wrapper.find(".control-label").each(function () {

        const txt = $(this).text();

        if (txt.includes("(H)")) {

            $(this).html(
                txt.replace(
                    "(H)",
                    '<span style="color:#ff0000;font-weight:bold;">(H)</span>'
                )
            );

        }

    });

    dialog.fields_dict.position_html.$wrapper.html(
        `<div style="
            font-size:15px;
            font-weight:600;
            margin-bottom:10px;
            color:#2b177a;">
            Position : ${children.length} Tasks
        </div>`
    );



}

window.toggle_expand_all = function () {
    const anyHidden = $('.project-row:hidden').length > 0;
    if (anyHidden) {
        $('.project-row').show();
        $('.task-table-row').show();
        $('.client-row, .project-row').each(function () {
            const cell = $(this).find('td').eq(1);
            cell.html(cell.html().replace('➕', '➖'));
        });
        $('#expand_toggle_btn').text('Collapse All');

    } else {
        $('.project-row').hide();
        $('.task-table-row').hide();
        $('.client-row, .project-row').each(function () {
            const cell = $(this).find('td').eq(1);
            cell.html(cell.html().replace('➖', '➕'));
        });
        $('#expand_toggle_btn').text('Expand All');
    }

};

window.update_master_table = async function () {

    const frm = cur_frm;

    frappe.dom.freeze(__("Updating Recruitment Planner..."));

    try {


        document.querySelectorAll("tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);

            if (!child) return;

            tr.querySelectorAll("select, input").forEach(el => {

                const field = el.getAttribute("data-field");
                if (!field) return;


                if (el.classList.contains("team-multi")) {

                    const checked = tr.querySelectorAll('.team-multi-box input[type="checkbox"]:checked');
                    const values = Array.from(checked).map(c => c.value);
                    child[field] = values.join(",");

                } else {

                    child[field] = el.value;

                }

            });

        });

        frm.dirty();


        const existing = new Set();

        (frm.doc.team_wise || []).forEach(r => {
            existing.add(`${r.task}::${r.team}::${r.date}`);
        });


        const date_columns = get_date_range(frm.doc.start_date, frm.doc.end_date);

        const date_map = {};

        date_columns.forEach((d, i) => {
            date_map[`day_${d.key}`] = frappe.datetime.add_days(frm.doc.start_date, i);
        });


        const task_updates = [];

        document.querySelectorAll("tr[data-row-name]").forEach(tr => {

            const rowName = tr.getAttribute("data-row-name");
            const child = frappe.model.get_doc("REC Task Planner", rowName);

            console.log("Child EFD:", child.efd);
            console.log(task_updates.length);
            task_updates.push({
                task_id: child.task_id,
                src: child.src,
                src_s: child.src_s,
                cc: child.cc,
                efd: child.efd || "",
                status: child.status || "",
                custom_sourcing_method_multi: child.sources || ""
            });

        });


        await frm.save();

        frm.refresh_field("team_wise");
        console.log("Task Updates:", task_updates);
        if (task_updates.length) {
            await frappe.call({
                method: "teampro.teampro.doctype.rec_week_plan.rec_week_plan.update_task_src",
                args: {
                    tasks: task_updates
                }
            });

        }


        if (typeof build_master_table === "function") {
            build_master_table(frm);
        }

        frappe.show_alert({
            message: __("Planner Updated Successfully"),
            indicator: "green"
        });

    }

    finally {

        frappe.dom.unfreeze();

    }

};
window.export_master_excel = function () {

    const name = cur_frm.doc.name;

    window.open(
        `/api/method/teampro.teampro.doctype.rec_week_plan.rec_week_plan.download_master_excel?name=${name}`
    );

};


// function apply_team_date_filter(frm) {
//     const grid = frm.fields_dict["team_wise"].grid;
//     if (!grid) return;

//     const total_rows = (frm.doc.team_wise || []).length;
//     grid.grid_pagination.page_length = total_rows || 20;
//     grid.refresh();

//     setTimeout(() => {
//         if (!grid.grid_rows) return;

//         let visible_count = 0;

//         grid.grid_rows.forEach(row => {
//             const d = row.doc;
//             let show = true;

//             if (frm.doc.rec_team && d.team !== frm.doc.rec_team) {
//                 show = false;
//             }
//             if (frm.doc.date && d.date !== frm.doc.date) {
//                 show = false;
//             }

//             if (row.wrapper) {
//                 row.wrapper.toggle(show);
//             }

//             // Renumber the "No." column for visible rows only
//             if (show && row.wrapper) {
//                 visible_count++;
//                 const index_cell = row.wrapper.find(".row-index, .row-check + .row-index");
//                 if (index_cell.length) {
//                     index_cell.find("span").text(visible_count);
//                 }
//             }
//         });

//         if (grid.wrapper) {
//             grid.wrapper.find(".grid-pagination, .grid-footer .btn-group").hide();
//         }
//     }, 100);
// }

function apply_team_date_filter(frm) {
    const grid = frm.fields_dict["team_wise"].grid;
    if (!grid) return;

    const total_rows = (frm.doc.team_wise || []).length;
    grid.grid_pagination.page_length = total_rows || 20;
    grid.refresh();

    setTimeout(() => {
        if (!grid.grid_rows) return;

        const from_date = frm.doc.date ? frappe.datetime.str_to_obj(frm.doc.date) : null;
        const to_date = frm.doc.date_to ? frappe.datetime.str_to_obj(frm.doc.date_to) : null;

        let visible_count = 0;

        grid.grid_rows.forEach(row => {
            const d = row.doc;
            let show = true;

            if (frm.doc.rec_team && d.team !== frm.doc.rec_team) {
                show = false;
            }

            if (show && (from_date || to_date)) {
                const row_date = d.date ? frappe.datetime.str_to_obj(d.date) : null;

                if (!row_date) {
                    show = false;
                } else if (from_date && to_date) {
                    if (row_date < from_date || row_date > to_date) {
                        show = false;
                    }
                } else if (from_date) {
                    if (row_date < from_date) {
                        show = false;
                    }
                } else if (to_date) {
                    if (row_date > to_date) {
                        show = false;
                    }
                }
            }

            if (row.wrapper) {
                row.wrapper.toggle(show);
            }

            if (show && row.wrapper) {
                visible_count++;
                const index_cell = row.wrapper.find(".row-index, .row-check + .row-index");
                if (index_cell.length) {
                    index_cell.find("span").text(visible_count);
                }
            }
        });

        if (grid.wrapper) {
            grid.wrapper.find(".grid-pagination, .grid-footer .btn-group").hide();
        }
    }, 100);
}


function trigger_download(frm) {
    const proceed = () => {
        const params = new URLSearchParams({
            docname: frm.doc.name,
            team: frm.doc.rec_team || "",
            date: frm.doc.date || "",
            date_to: frm.doc.date_to || ""
        });

        window.open(
            `/api/method/teampro.teampro.doctype.rec_week_plan.rec_week_plan.download_team_wise_excel?${params.toString()}`
        );
    };

    if (frm.is_dirty()) {
        frm.save().then(() => proceed());
    } else {
        proceed();
    }
}


