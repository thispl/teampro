/* ============================================================
   IT Monitoring Dashboard
   Three tabs: Project | Sprint | Day
   Reuses backend endpoints from new_it_dashboard.new_it
   ============================================================ */
 
frappe.pages['it-monitoring-dashboard'].on_page_load = function (wrapper) {
 
    /* ---- Backend method prefix ---- */
    var M = "teampro.teampro.page.new_it_dashboard.new_it.";
 
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'IT Monitoring Dashboard',
        single_column: true
    });
 
    /* ---- Load the presentable stylesheet ---- */
    /* Frappe auto-bundles it_monitoring_dashboard.css for standard pages.
       We also inject a <link> fallback with cache-busting in case assets
       aren't built yet or the browser has a stale cached copy. */
    if (!document.getElementById('itm-dashboard-css')) {
        var cssLink = document.createElement('link');
        cssLink.id = 'itm-dashboard-css';
        cssLink.rel = 'stylesheet';
        cssLink.href = '/assets/teampro/css/it_monitoring_dashboard.css?v=' + Date.now();
        cssLink.onerror = function () { /* silently ignore — page CSS may already be bundled */ };
        document.head.appendChild(cssLink);
    }
 
    /* ============================================================
       PAGE SHELL — header + tab bar + three tab panels
       ============================================================ */
    $(wrapper).html(`
    <div class="itm-wrapper">
        <div class="itm-header">
            <h2>IT MONITORING DASHBOARD</h2>
            <div id="itm-datetime" class="itm-datetime"></div>
        </div>
 
        <div class="itm-tab-bar">
            <div class="itm-tab active" data-tab="project">Project</div>
            <div class="itm-tab" data-tab="sprint">Sprint</div>
            <div class="itm-tab" data-tab="day">Day</div>
        </div>
 
        <!-- ============== PROJECT TAB ============== -->
        <div id="itm-project-content" class="itm-tab-content">

            <!-- Summary row: left (Project + Task cards stacked) | right (PSR pivot) -->
            <div id="itm-project-summary-row" style="display:flex; gap:20px; margin-top:10px; background:#f5f5f5;">

                <!-- LEFT SIDE: Project count + Task count stacked vertically -->
                <div style="display:flex; flex-direction:column; gap:20px; flex:1;">
                    <div style="border:1px solid #2ac1db; border-radius:8px; padding:10px; background:#f5f5f5;">
                        <div id="itm-project-cards"></div>
                    </div>
                    <div style="border:1px solid #2ac1db; border-radius:8px; padding:10px; background:#f5f5f5;">
                        <div id="itm-task-cards"></div>
                    </div>
                </div>

                <!-- RIGHT SIDE: PSR pivot table -->
                <div style="flex:1; border:1px solid #2ac1db; border-radius:8px; padding:10px; max-height:580px; overflow-y:auto; background:#f5f5f5;">
                    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
                        <h4 style="margin:0; font-weight:600; color:#0F1568;">PROJECT STATUS REPORT (PSR)</h4>
                        <div style="display:flex; gap:8px;">
                            <span class="itm-psr-toggle active" data-view="overall" style="cursor:pointer; padding:4px 12px; border-radius:4px; background:#0F1568; color:white; font-size:12px;">Overall</span>
                            <span class="itm-psr-toggle" data-view="current" style="cursor:pointer; padding:4px 12px; border-radius:4px; background:white; color:#0F1568; border:1px solid #0F1568; font-size:12px;">Current</span>
                        </div>
                    </div>
                    <div id="itm-psr-table"></div>
                </div>

            </div>

        </div>
 
        <!-- ============== SPRINT TAB ============== -->
        <div id="itm-sprint-content" class="itm-tab-content" style="display:none;">
 
            <!-- Sprint filters -->
            <div class="itm-section">
                <div class="itm-section-header">
                    <h4>SPRINT FILTERS</h4>
                    <div class="itm-actions">
                        <div id="itm-sprint-team-filter" style="min-width:180px;"></div>
                        <div id="itm-sprint-filter" style="min-width:180px;"></div>
                    </div>
                </div>
            </div>
 
            <!-- Sprint Progress -->
            <div class="itm-section">
                <div class="itm-section-header"><h4>SPRINT PROGRESS</h4></div>
                <div id="itm-sprint-chart" class="itm-loading">Loading...</div>
            </div>
 
            <!-- Overall Team Summary — Productivity & Efficiency vs KRA -->
            <div class="itm-section">
                <div class="itm-section-header">
                    <h4>OVERALL TEAM SUMMARY — PRODUCTIVITY &amp; EFFICIENCY (KRA)</h4>
                </div>
                <div id="itm-sprint-overall" class="itm-table-scroll itm-loading">Loading...</div>
            </div>
 
            <!-- 4 & 5. RT Vs AT % > 150% (Completed & Working) side by side -->
            <div style="display:flex; gap:15px; margin-top:24px; flex-wrap:wrap;">
                <div class="card-container equal-height"
                    style="flex:1; min-width:48%; margin-right:0px; background:#f5f5f5; border:1px solid #ddd; border-radius:8px; padding:10px;">
                    <div style="background:white;padding:10px;border-radius:6px;display:flex;align-items:center;justify-content:center;">
                        <h4 style="margin:0;font-weight:600;">RT Vs AT %(Completed Tasks) &gt; 150%</h4>
                    </div>
                    <br>
                    <div id="itm-rtat-completed" style="background:white;padding:15px;border-radius:6px;overflow-x:auto;">Loading...</div>
                </div>

                <div class="card-container equal-height"
                    style="flex:1; min-width:48%; margin-right:0px; background:#f5f5f5; border:1px solid #ddd; border-radius:8px; padding:10px;">
                    <div style="background:white;padding:10px;border-radius:6px;display:flex;align-items:center;justify-content:center;">
                        <h4 style="margin:0;font-weight:600;">RT Vs AT % (Working) &gt; 150%</h4>
                    </div>
                    <br>
                    <div id="itm-rtat-working" style="background:white;padding:15px;border-radius:6px;overflow-x:auto;">Loading...</div>
                </div>
            </div>

            <!-- 6 & 7. NT Tasks Priority High/Urgent side by side -->
            <div style="display:flex; gap:15px; margin-top:24px; flex-wrap:wrap; margin-bottom:24px;">
                <div class="card-container equal-height"
                    style="flex:1; min-width:48%; margin-right:0px; background:#f5f5f5; border:1px solid #ddd; border-radius:8px; padding:10px;">
                    <div style="background:white;padding:10px;border-radius:6px;display:flex;align-items:center;justify-content:center;">
                        <h4 style="margin:0;font-weight:600;">NT Tasks with Priority High/Urgent in any sprint</h4>
                    </div>
                    <br>
                    <div id="itm-nt-any" style="background:white;padding:15px;border-radius:6px;overflow-x:auto;">Loading...</div>
                </div>

                <div class="card-container equal-height"
                    style="flex:1; min-width:48%; margin-right:0px; background:#f5f5f5; border:1px solid #ddd; border-radius:8px; padding:10px;">
                    <div style="background:white;padding:10px;border-radius:6px;display:flex;align-items:center;justify-content:center;">
                        <h4 style="margin:0;font-weight:600;">NT Tasks with Priority High/Urgent</h4>
                    </div>
                    <br>
                    <div id="itm-nt-current" style="background:white;padding:15px;border-radius:6px;overflow-x:auto;">Loading...</div>
                </div>
            </div>

            <!-- Non-Allocated Tasks (moved from Day tab) -->
            <div class="itm-section">
                <div class="itm-section-header">
                    <h4>NON-ALLOCATED TASKS</h4>
                    <div class="itm-actions">
                        <button class="itm-toggle-btn active" data-view="overall">Overall</button>
                        <button class="itm-toggle-btn" data-view="sprint">NA</button>
                        <select id="itm-kt-filter" style="height:28px;border-radius:6px;border:1px solid #d0d7de;">
                            <option value="">KT Confirm</option>
                            <option value="Yes">Yes</option>
                            <option value="No">No</option>
                        </select>
                    </div>
                </div>
                <div id="itm-non-allocated" class="itm-table-scroll itm-loading">Loading...</div>
            </div>

            <!-- Re-Open & Developer Error Summary with EP&NC links -->
            <div class="itm-section" style="margin-top:24px;">
                <div class="itm-section-header">
                    <h4>RE-OPEN &amp; DEVELOPER ERROR SUMMARY (EP&amp;NC)</h4>
                </div>
                <div id="itm-reopen-de-summary" class="itm-table-scroll itm-loading">Loading...</div>
            </div>

        </div>

        <!-- ============== DAY TAB ============== -->
        <div id="itm-day-content" class="itm-tab-content" style="display:none;">

            <!-- Day filters -->
            <div class="itm-section">
                <div class="itm-section-header">
                    <h4>DAY FILTERS</h4>
                    <div class="itm-actions">
                        <div id="itm-day-team-filter" style="min-width:180px;"></div>
                        <div id="itm-day-date-filter" style="min-width:180px;"></div>
                    </div>
                </div>
            </div>

            <!-- Production Table (same DSR columns + grouped Team/CB structure) -->
            <div class="itm-section">
                <div class="itm-section-header">
                    <h4>PRODUCTION TABLE</h4>
                    <div class="itm-actions" id="itm-production-filters">
                        <button id="itm-dsr-download" class="itm-download-btn" title="Download Excel" style="border:1px solid #d0d7de;background:#fff;border-radius:6px;padding:4px 10px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;font-size:12px;">
                            <i class="fa fa-download" style="font-size:13px;color:#0F1568;"></i> Excel
                        </button>
                        <span id="itm-open-all-teams-btn" style="cursor:pointer;font-weight:bold;flex-shrink:0;">+ ALL</span>
                        <span class="itm-filter-label" style="color:green;font-weight:bold;">Priority :</span>
                        <span class="itm-filter-btn" data-group="priority" data-filter="Low">Low</span>
                        <span class="itm-filter-btn" data-group="priority" data-filter="Medium">Medium</span>
                        <span class="itm-filter-btn" data-group="priority" data-filter="High">High</span>
                        <span class="itm-filter-btn" data-group="priority" data-filter="Critical">Urgent</span>
                        <span class="itm-filter-label" style="margin-left:12px;color:green;font-weight:bold;">S/P :</span>
                        <span class="itm-filter-btn" data-group="sp" data-filter="S">Spot</span>
                        <span class="itm-filter-btn" data-group="sp" data-filter="P">Plan</span>
                        <span class="itm-filter-label" style="margin-left:12px;color:green;font-weight:bold;">RO :</span>
                        <span class="itm-filter-btn" data-group="ro" data-filter="RO">Reopen</span>
                        <span class="itm-filter-label" style="margin-left:12px;color:green;font-weight:bold;">CF :</span>
                        <span class="itm-filter-btn" data-group="cf" data-filter="CF">Carry Forward</span>
                    </div>
                </div>
                <div id="itm-production-table" class="itm-table-scroll itm-loading">Loading...</div>
            </div>

            <!-- DPR Summary -->
            <div class="itm-dpr-card">
                <div class="itm-dpr-header">
                    <h4>DPR SUMMARY</h4>
                    <button id="itm-dpr-download" class="itm-download-btn" title="Download DPR Excel" style="border:1px solid #d0d7de;background:#fff;border-radius:6px;padding:4px 10px;cursor:pointer;display:none;align-items:center;gap:5px;font-size:12px;">
                        <i class="fa fa-download" style="font-size:13px;color:#0F1568;"></i> Excel
                    </button>
                </div>
                <div id="itm-dpr-table" class="itm-dpr-scroll">Loading...</div>
            </div>

        </div>
 
    </div>`);
 
    /* ============================================================
       LIVE CLOCK
       ============================================================ */
    function updateClock() {
        var now = new Date();
        var d = now.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        var t = now.toLocaleTimeString();
        $('#itm-datetime').text(d + '  •  ' + t);
    }
    updateClock();
    setInterval(updateClock, 1000);
 
    /* ============================================================
       ICON MAPS
       ============================================================ */
    var projectIcons = {
        "Total": "fa fa-chart-pie",
        "External": "fa fa-globe",
        "AMC": "fa fa-cogs",
        "Enquiry": "fa fa-search",
        "Internal": "fa fa-building"
    };
    var taskIcons = {
        "Total": "fa fa-list",
        "Open": "fa fa-folder-open",
        "Working": "fa fa-spinner",
        "Internal Review": "fa fa-user",
        "Client Review": "fa fa-users"
    };
 
    /* ============================================================
       TAB SWITCHING
       ============================================================ */
    var sprintTabLoaded = false;
    var dayTabLoaded = false;
 
    $(document).off('click', '.itm-tab').on('click', '.itm-tab', function () {
        $('.itm-tab').removeClass('active');
        $(this).addClass('active');
        var tab = $(this).data('tab');
 
        $('#itm-project-content').hide();
        $('#itm-sprint-content').hide();
        $('#itm-day-content').hide();
 
        if (tab === 'project') {
            $('#itm-project-content').show();
        } else if (tab === 'sprint') {
            $('#itm-sprint-content').show();
            if (!sprintTabLoaded) {
                sprintTabLoaded = true;
                loadSprintChart();
                loadSprintOverall();
                loadRTATException();
                loadNTAny();
                loadNTCurrent();
                loadRetroSummary(null);
                loadNonAllocated();
                loadReopenDESummary();
            }
        } else if (tab === 'day') {
            $('#itm-day-content').show();
            if (!dayTabLoaded) {
                dayTabLoaded = true;
                loadProductionSummary();
                loadDPR();
            }
        }
    });
 
    /* ============================================================
       HELPER — render summary card group
       ============================================================ */
    function renderCardGroup(selector, cards, onClick, headerTitle) {
        var html = '';
        if (headerTitle) {
            html += '<h4 style="margin:0; padding:10px 0; text-align:center; background:white; border-radius:6px; margin-bottom:10px; font-weight:600; color:#0F1568;">' + headerTitle + '</h4>';
        }
        html += '<div style="display:flex;flex-wrap:wrap;gap:5px;justify-content:flex-start;box-sizing:border-box;">';
        cards.forEach(function (c) {
            html += '<div class="itm-card" data-key="' + c.key + '">'
                + '<div class="itm-card-top" style="background:' + c.color + ';"></div>'
                + '<div class="itm-card-body">'
                + '<div class="itm-card-icon" style="background:' + c.color + '20;">'
                + '<i class="' + c.icon + '" style="color:' + c.color + ';"></i></div>'
                + '<div class="itm-card-title">' + c.title + '</div>'
                + '<div class="itm-card-value" style="color:' + c.color + ';">' + c.value + '</div>'
                + (c.hours !== undefined ? '<div class="itm-card-hours">' + (c.hours).toFixed(2) + ' hr</div>' : '')
                + (c.subtitle ? '<div class="itm-card-subtitle">' + c.subtitle + '</div>' : '')
                + '</div></div>';
        });
        html += '</div>';
        $(selector).html(html);
        if (onClick) {
            $(selector).off('click', '.itm-card').on('click', '.itm-card', function () {
                onClick($(this).data('key'));
            });
        }
    }
 
    /* ============================================================
       PROJECT TAB
       ============================================================ */
    var pivotData = [];
 
    function loadProjectTab() {
        Promise.all([
            frappe.call({ method: M + "get_project_counts" }),
            frappe.call({ method: M + "get_task_summary" }),
            frappe.call({ method: M + "get_tasks_project_pivot" })
        ]).then(function (results) {
            var projRes = results[0], taskRes = results[1], pivotRes = results[2];
 
            /* ---- Project cards ---- */
            if (projRes.message) {
                var projects = projRes.message.projects || [];
                var total = projRes.message.total || 0;
                var colors = ["#0096A6", "#2F8F46", "#C29100", "#540D6E", "#006D77", "#4169e1", "#8B0000", "#f9844a", "#bc5090", "#003f5c"];
                var cards = [{ key: "Total", title: "Total", value: total, color: "#0096A6", icon: "fa fa-chart-pie", subtitle: "All Projects" }];
                projects.forEach(function (it, i) {
                    if (it.project_type === "Products") return;
                    cards.push({
                        key: it.project_type,
                        title: it.project_type,
                        value: it.count,
                        color: colors[(i + 1) % colors.length],
                        icon: projectIcons[it.project_type] || "fa fa-folder",
                        subtitle: it.project_type + " type"
                    });
                });
                renderCardGroup('#itm-project-cards', cards, function (key) {
                    if (!key || key === "Total") {
                        renderPSR(pivotData);
                    } else {
                        renderPSR(pivotData.filter(function (r) { return r.project_type === key; }));
                    }
                }, 'PROJECT COUNT');
            }
 
            /* ---- Task cards ---- */
            if (taskRes.message) {
                var tc = taskRes.message;
                var taskColors = { total: '#0096A6', open: '#2F8F46', working: '#C29100', pr: '#540D6E', cr: '#006D77' };
                var taskTitles = { total: 'Total', open: 'Open', working: 'Working', pr: 'Internal Review', cr: 'Client Review' };
                var taskSubs = { total: 'Total tasks', open: 'Not yet started', working: 'In progress', pr: 'Awaiting internal review', cr: 'Awaiting client review' };
                var taskCards = ['total', 'open', 'working', 'pr', 'cr'].map(function (k) {
                    return {
                        key: k, title: taskTitles[k], value: tc[k] || 0, color: taskColors[k],
                        icon: taskIcons[taskTitles[k]] || "fa fa-tasks",
                        hours: tc[k + '_total_hours'] || 0, subtitle: taskSubs[k]
                    };
                });
                renderCardGroup('#itm-task-cards', taskCards, function (key) {
                    frappe.call({
                        method: M + "get_tasks_project_wise",
                        args: { type: key },
                        callback: function (r) {
                            var rows = r.message || [];
                            var tbl = '<div style="max-height:420px;overflow-y:auto;">'
                                + '<table class="itm-table"><thead><tr>'
                                + '<th>Project</th><th>Tasks</th><th>Hours</th><th>SPOC</th>'
                                + '</tr></thead><tbody>';
                            rows.forEach(function (p) {
                                tbl += '<tr><td class="left-align">' + (p.project || 'No Project') + '</td>'
                                    + '<td>' + p.task_count + '</td>'
                                    + '<td>' + (p.total_hours || 0).toFixed(2) + '</td>'
                                    + '<td class="left-align">' + (p.spoc || 'No Spoc') + '</td></tr>';
                            });
                            tbl += '</tbody></table></div>';
                            new frappe.ui.Dialog({
                                title: taskTitles[key] + ' — Task Allocation',
                                fields: [{ fieldname: "html_table", fieldtype: "HTML", options: tbl }]
                            }).show();
                        }
                    });
                }, 'TASK ALLOCATION STATUS');
            }
 
            /* ---- PSR pivot ---- */
            pivotData = pivotRes.message || [];
            renderPSR(pivotData);
        });
    }
 
    /* ---- PSR pivot rendering ---- */
    function renderPSR(data) {
        if (!data || data.length === 0) {
            $('#itm-psr-table').html('<div class="itm-empty">No data found</div>');
            return;
        }
        var html = '<table class="itm-table" id="itm-pivot-summary"><thead><tr>'
            + '<th>S.No</th><th>Project Name</th><th>Project Type</th>'
            + '<th>Open (hr/#)</th><th>W (hr/#)</th><th>PR (hr/#)</th><th>CR (hr/#)</th>'
            + '</tr></thead><tbody>';
 
        var t = { o_h: 0, o_t: 0, o_td_h: 0, o_td_t: 0, w_h: 0, w_t: 0, w_td_h: 0, w_td_t: 0, p_h: 0, p_t: 0, p_td_h: 0, p_td_t: 0, c_h: 0, c_t: 0, c_td_h: 0, c_td_t: 0 };
 
        data.forEach(function (row, idx) {
            var o = row.open.split("/").map(Number);
            var otd = row.open_td.split("/").map(Number);
            var w = row.working.split("/").map(Number);
            var wtd = row.working_td.split("/").map(Number);
            var p = row.pr.split("/").map(Number);
            var ptd = row.pr_td.split("/").map(Number);
            var c = row.cr.split("/").map(Number);
            var ctd = row.cr_td.split("/").map(Number);
 
            t.o_h += o[0]; t.o_t += o[1]; t.o_td_h += otd[0]; t.o_td_t += otd[1];
            t.w_h += w[0]; t.w_t += w[1]; t.w_td_h += wtd[0]; t.w_td_t += wtd[1];
            t.p_h += p[0]; t.p_t += p[1]; t.p_td_h += ptd[0]; t.p_td_t += ptd[1];
            t.c_h += c[0]; t.c_t += c[1]; t.c_td_h += ctd[0]; t.c_td_t += ctd[1];
 
            html += '<tr><td>' + (idx + 1) + '</td>'
                + '<td class="left-align"><a href="/app/project/' + row.project + '" target="_blank">' + row.project + '</a></td>'
                + '<td class="left-align">' + row.project_type + '</td>'
                + '<td>' + o[0].toFixed(2) + '/' + o[1] + '</td>'
                + '<td><span class="overall-col">' + w[0].toFixed(2) + '/' + w[1] + '</span>'
                + '<span class="current-col" style="display:none;">' + wtd[0].toFixed(2) + '/' + wtd[1] + '</span></td>'
                + '<td><span class="overall-col">' + p[0].toFixed(2) + '/' + p[1] + '</span>'
                + '<span class="current-col" style="display:none;">' + ptd[0].toFixed(2) + '/' + ptd[1] + '</span></td>'
                + '<td><span class="overall-col">' + c[0].toFixed(2) + '/' + c[1] + '</span>'
                + '<span class="current-col" style="display:none;">' + ctd[0].toFixed(2) + '/' + ctd[1] + '</span></td>'
                + '</tr>';
        });
 
        html += '<tr style="font-weight:bold;background:#0F1568;color:#fff;">'
            + '<td colspan="3">Total</td>'
            + '<td>' + t.o_h.toFixed(2) + '/' + t.o_t + '</td>'
            + '<td><span class="overall-col" style="color:#fff;">' + t.w_h.toFixed(2) + '/' + t.w_t + '</span>'
            + '<span class="current-col" style="display:none;color:#fff;">' + t.w_td_h.toFixed(2) + '/' + t.w_td_t + '</span></td>'
            + '<td><span class="overall-col" style="color:#fff;">' + t.p_h.toFixed(2) + '/' + t.p_t + '</span>'
            + '<span class="current-col" style="display:none;color:#fff;">' + t.p_td_h.toFixed(2) + '/' + t.p_td_t + '</span></td>'
            + '<td><span class="overall-col" style="color:#fff;">' + t.c_h.toFixed(2) + '/' + t.c_t + '</span>'
            + '<span class="current-col" style="display:none;color:#fff;">' + t.c_td_h.toFixed(2) + '/' + t.c_td_t + '</span></td>'
            + '</tr></tbody></table>';
 
        $('#itm-psr-table').html(html);
 
        /* PSR overall / current toggle */
        $('.itm-psr-toggle').off('click').on('click', function () {
            $('.itm-psr-toggle').removeClass('active');
            $(this).addClass('active');
            if ($(this).data('view') === 'overall') {
                $('.overall-col').show();
                $('.current-col').hide();
            } else {
                $('.overall-col').hide();
                $('.current-col').show();
            }
        });
    }
 
    /* ============================================================
       SPRINT TAB
       ============================================================ */
 
    /* ---- Sprint filters ---- */
    var sprintTeamCtrl = frappe.ui.form.make_control({
        parent: document.querySelector("#itm-sprint-team-filter"),
        df: { fieldtype: "Link", fieldname: "sprint_team", options: "Dev Team", placeholder: "Select Team", onchange: reloadSprint },
        render_input: true
    });
    var sprintFilterCtrl = frappe.ui.form.make_control({
        parent: document.querySelector("#itm-sprint-filter"),
        df: { fieldtype: "Link", fieldname: "sprint", options: "Task Sprint", placeholder: "Select Sprint", onchange: reloadSprint },
        render_input: true
    });
    $(document).off("change", "#itm-sprint-team-filter input").on("change", "#itm-sprint-team-filter input", reloadSprint);
    $(document).off("change", "#itm-sprint-filter input").on("change", "#itm-sprint-filter input", reloadSprint);
 
    /* Set default sprint */
    frappe.call({
        method: M + "update_sprint_filter",
        callback: function (r) {
            if (r && r.message) sprintFilterCtrl.set_value(r.message);
        }
    });
 
    function getSprintTeam() {
        return (sprintTeamCtrl && sprintTeamCtrl.get_value && sprintTeamCtrl.get_value()) || $("#itm-sprint-team-filter input").val() || "";
    }
    function getSprint() {
        return (sprintFilterCtrl && sprintFilterCtrl.get_value && sprintFilterCtrl.get_value()) || $("#itm-sprint-filter input").val() || "";
    }
 
    function reloadSprint() {
        loadSprintChart();
        loadSprintOverall();
        loadRTATException();
        loadNTAny();
        loadNTCurrent();
        loadReopenDESummary();
    }
 
    /* ---- Sprint Progress ---- */
    function loadSprintChart() {
        // Fetch overall summary first to get per-CB P%/E% data
        frappe.call({
            method: M + "get_sprint_teamwise_summary",
            args: { team: getSprintTeam(), sprint: getSprint() },
            callback: function (summaryRes) {
                frappe.call({
                    method: M + "get_sprint_chart_data",
                    args: { team: getSprintTeam(), sprint: getSprint() },
                    callback: function (r) {
                        if (!r.message || !r.message.labels || r.message.labels.length === 0) {
                            $("#itm-sprint-chart").html('<div class="itm-empty itm-empty-error">No Sprint Data Found</div>');
                            return;
                        }
                        renderSprintProgress(r.message, summaryRes && summaryRes.message);
                    }
                });
            }
        });
    }
 
    function renderSprintProgress(msg, summary) {
        var labels = msg.labels, avl = msg.available_hours, exp = msg.expected_hours, rt = msg.sprint_avl_time;
        var teams = msg.teams || [], sprintIds = msg.sprint_ids || [], images = msg.images || [];
        var teamTotals = msg.team_totals || [];
        var teamOrder = [], teamMap = {};

        // Build CB metrics lookup from Overall Summary (same calc as Sprint Summary)
        var cbMetrics = {};
        if (summary && summary.teams) {
            summary.teams.forEach(function (t) {
                (t.cbs || []).forEach(function (c) {
                    var sc = (c.cb || '').trim().toUpperCase();
                    cbMetrics[sc] = c;
                });
            });
        }

        // Build team-level lookup with sprint totals and logo
        teamTotals.forEach(function (t) {
            teamMap[t.team || "Unassigned"] = {
                aph: parseFloat(t.aph || 0),
                rt: parseFloat(t.rt || 0),
                logo: t.logo || "",
                cbs: [],
                sprint_id: ""
            };
        });

        labels.forEach(function (sc, i) {
            var team = teams[i] || "Unassigned";
            if (!teamMap[team]) { teamMap[team] = { aph: 0, rt: 0, logo: "", cbs: [], sprint_id: "" }; }
            if (teamOrder.indexOf(team) === -1) { teamOrder.push(team); }
            var c = { sc: sc, a: parseFloat(avl[i] || 0), e: parseFloat(exp[i] || 0), rv: parseFloat(rt[i] || 0), img: images[i] || "" };
            var m = cbMetrics[sc] || {};
            c.cr = parseFloat(m.completed_rt || 0);
            c.ca = parseFloat(m.completed_at || 0);
            c.pct = c.a ? (c.cr / c.a) * 100 : 0;
            c.eff = c.cr ? (c.ca / c.cr) * 100 : 0;
            teamMap[team].cbs.push(c);
            if (!teamMap[team].sprint_id) teamMap[team].sprint_id = sprintIds[i] || "";
        });

        function teamLogo(logo, team) {
            if (logo) {
                return '<div class="sprint-team-logo-wrap" data-logo="' + logo + '" data-team="' + team + '"></div>';
            }
            return '<div class="sprint-team-logo-circle">' + (team ? team[0].toUpperCase() : '?') + '</div>';
        }

        function cbAvatar(sc, img) {
            if (img) {
                return '<div class="sprint-cb-avatar-wrap" data-sc="' + sc + '" data-img="' + img + '"></div>';
            }
            var initials = sc.split(/[-_\s]+/).filter(function (s) { return s.length > 0; }).slice(0, 2).map(function (s) { return s[0].toUpperCase(); }).join("");
            if (initials.length === 0) initials = sc.substring(0, 2).toUpperCase();
            return '<div class="sprint-cb-avatar-circle">' + initials + '</div>';
        }

        function statusDot(rt, aph) {
            var ratio = aph ? rt / aph : 0;
            var color;
            if (ratio >= 0.9) color = '#4caf50';
            else if (ratio >= 0.5) color = '#ff9800';
            else color = '#f44336';
            return '<span class="sprint-cb-status-dot" style="background:' + color + ';"></span>';
        }

        function combinedBar(c) {
            var aph = c.a;
            var lifespan = c.e;
            var rtVal = c.rv;
            var rtPct = aph ? (rtVal / aph) * 100 : 0;
            var lifespanPct = aph ? (lifespan / aph) * 100 : 0;
            rtPct = Math.max(rtPct, 0);
            lifespanPct = Math.max(lifespanPct, 0);
            var rtWidth = Math.min(rtPct, 100);
            var markerLeft = Math.min(lifespanPct, 100);
            var showRtPct = rtPct >= 15;

            return '<div class="sprint-combined-bar">' +
                '<div class="sprint-combined-aph-label">' +
                    '<span class="sprint-combined-aph-val">' + aph.toFixed(1) + '</span>' +
                    '<span class="sprint-combined-aph-tag">APH</span>' +
                '</div>' +
                '<div class="sprint-combined-track">' +
                    '<div class="sprint-combined-fill" style="width:0%;" data-target-width="' + rtWidth.toFixed(1) + '%">' +
                        (showRtPct ? '<span class="sprint-combined-fill-pct">RT ' + rtPct.toFixed(0) + '%</span>' : '') +
                    '</div>' +
                    '<div class="sprint-combined-marker" style="left:0%;" data-target-left="' + markerLeft.toFixed(1) + '%">' +
                        '<div class="sprint-combined-marker-line"></div>' +
                        '<div class="sprint-combined-marker-flag">L ' + lifespan.toFixed(1) + 'h</div>' +
                    '</div>' +
                '</div>' +
                '<div class="sprint-combined-rt-label">' +
                    '<span class="sprint-combined-rt-val">' + rtVal.toFixed(1) + '</span>' +
                    '<span class="sprint-combined-rt-tag">RT</span>' +
                '</div>' +
            '</div>';
        }

        var teamBlocks = teamOrder.map(function (team) {
            var info = teamMap[team];
            var totalCr = info.cbs.reduce(function (sum, c) { return sum + c.cr; }, 0);
            var totalCa = info.cbs.reduce(function (sum, c) { return sum + c.ca; }, 0);
            var totalPct = info.aph ? (totalCr / info.aph) * 100 : 0;
            var totalEff = totalCr ? (totalCa / totalCr) * 100 : 0;

            var cards = info.cbs.map(function (c) {
                var pctStyle = 'color:' + (c.pct < 50 ? '#f44336' : '#4caf50') + ';';
                var effStyle = 'color:' + (c.eff <= 100 ? '#4caf50' : '#f44336') + ';';
                return '<div class="sprint-cb-avatar-card">'
                    + cbAvatar(c.sc, c.img)
                    + '<div class="sprint-cb-avatar-name">' + c.sc + '</div>'
                    + combinedBar(c)
                    + '<div class="sprint-cb-summary">'
                    + '<div class="sprint-cb-summary-item"><span class="label">P%:</span><span class="value" style="' + pctStyle + '">' + c.pct.toFixed(1) + '%</span></div>'
                    + '<div class="sprint-cb-summary-item"><span class="label">E%:</span><span class="value" style="' + effStyle + '">' + c.eff.toFixed(1) + '%</span></div>'
                    + '</div>'
                    + '</div>';
            });

            return '<div class="sprint-team-panel">'
                + '<div class="sprint-team-bar">'
                + '<div class="sprint-team-bar-left">'
                + teamLogo(info.logo, team)
                + '<span class="sprint-team-bar-name">' + team + '</span>'
                + '</div>'
                + '<div class="sprint-team-bar-stats">'
                + '<span>APH: <b>' + info.aph.toFixed(2) + '</b></span>'
                + '<span>RT: <b>' + info.rt.toFixed(2) + '</b></span>'
                + '<span style="color:' + (totalPct < 50 ? '#f44336' : '#4caf50') + ';">P%: <b>' + totalPct.toFixed(1) + '%</b></span>'
                + '<span style="color:' + (totalEff <= 100 ? '#4caf50' : '#f44336') + ';">E%: <b>' + totalEff.toFixed(1) + '%</b></span>'
                + '</div>'
                + '</div>'
                + '<div class="sprint-cb-avatars">' + cards.join('') + '</div></div>';
        });

        $('#itm-sprint-chart').html('<div class="sprint-progress-grid" style="padding:10px;">' + teamBlocks.join('') + '</div>');

        /* Animate bars like new_it_dashboard */
        setTimeout(function () {
            $('#itm-sprint-chart .sprint-combined-fill').each(function () {
                var target = $(this).data('target-width');
                if (target !== undefined) { $(this).css('width', target); }
            });
            $('#itm-sprint-chart .sprint-combined-marker').each(function () {
                var target = $(this).data('target-left');
                if (target !== undefined) { $(this).css('left', target); }
            });
        }, 50);

        /* Load team logos after render; fall back to initial on error */
        $('#itm-sprint-chart .sprint-team-logo-wrap').each(function () {
            var $w = $(this);
            var team = $w.data('team');
            var logo = $w.data('logo');
            var $img = $('<img class="sprint-team-logo-img" src="' + logo + '" alt="' + team + '">');
            $img.on('error', function () {
                $w.html('<div class="sprint-team-logo-circle">' + (team ? team[0].toUpperCase() : '?') + '</div>');
            });
            $img.on('load', function () { $w.html($img); });
        });

        /* Load employee images after render; fall back to initials on error */
        $('#itm-sprint-chart .sprint-cb-avatar-wrap').each(function () {
            var $w = $(this);
            var sc = $w.data('sc');
            var img = $w.data('img');
            var $img = $('<img class="sprint-cb-avatar-img" src="' + img + '" alt="' + sc + '">');
            $img.on('error', function () {
                var initials = sc.split(/[-_\s]+/).filter(function (s) { return s.length > 0; }).slice(0, 2).map(function (s) { return s[0].toUpperCase(); }).join('');
                if (initials.length === 0) initials = sc.substring(0, 2).toUpperCase();
                $w.html('<div class="sprint-cb-avatar-circle">' + initials + '</div>');
            });
            $img.on('load', function () { $w.html($img); });
        });
    }
    /* ---- Overall Team Summary (Productivity & Efficiency) ---- */
    function loadSprintOverall() {
        frappe.call({
            method: M + "get_sprint_teamwise_summary",
            args: { team: getSprintTeam(), sprint: getSprint() },
            callback: function (r) {
                if (!r.message || !r.message.teams || r.message.teams.length === 0) {
                    $("#itm-sprint-overall").html('<div class="itm-empty itm-empty-error">No Sprint Data Found</div>');
                    return;
                }
                renderSprintOverall(r.message.teams);
            }
        });
    }
 
    function renderSprintOverall(teams) {
        var C = {
            comp: '#2e7d32',      // green
            work: '#ef6c00',      // orange
            nt: '#c62828',        // red
            head: '#0F1568',
            subhead: '#283593'
        };
        function cs(color) { return ' style="background:' + color + ';color:#fff;"'; }
        function pctCell(pct) {
            if (pct < 50) return ' style="color:#c62828;font-weight:bold;"';
            return '';
        }

        var html = '<table class="itm-table" style="min-width:1500px;"><thead>'
            + '<tr style="background:' + C.head + ';color:#fff;">'
            + '<th rowspan="2" style="vertical-align:middle;width:30px;background:' + C.head + ';"></th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">S.No</th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">Team</th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">Sprint ID</th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">APH</th>'
            + '<th colspan="4" style="background:' + C.subhead + ';color:#fff;">PLAN</th>'
            + '<th colspan="4" style="background:' + C.subhead + ';color:#fff;">SPOT</th>'
            + '<th colspan="9" style="background:' + C.subhead + ';color:#fff;">TOTAL</th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">Biometric Hrs</th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">NC RT</th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">Reopen RT</th>'
            + '<th rowspan="2" style="vertical-align:middle;background:' + C.head + ';">DE RT</th>'
            + '</tr><tr style="background:' + C.subhead + ';color:#fff;">'
            + '<th>Planned RT</th><th>Comp RT</th><th>Work RT</th><th>NT RT</th>'
            + '<th>Spot RT</th><th>Spot Comp RT</th><th>Spot Work RT</th><th>Spot NT RT</th>'
            + '<th>Total RT</th><th>AT</th><th' + cs(C.comp) + '>Completed RT</th><th' + cs(C.comp) + '>Completed AT</th><th' + cs(C.work) + '>Working RT</th><th' + cs(C.work) + '>Working AT</th><th' + cs(C.nt) + '>Total NT RT</th><th>Productivity %</th><th>Efficiency %</th>'
            + '</tr></thead><tbody>';

        var grand = { aph: 0, planned_rt: 0, comp_rt: 0, work_rt: 0, nt_rt: 0, spot_rt: 0, spot_comp_rt: 0, spot_work_rt: 0, spot_nt_rt: 0, total_rt: 0, at: 0, completed_rt: 0, completed_at: 0, working_rt: 0, working_at: 0, total_nt_hours: 0, biometric_hrs: 0, nc_rt: 0, reopen_rt: 0, de_rt: 0 };

        teams.forEach(function (t, idx) {
            var tot = t.totals || {};
            var prod = tot.aph ? (tot.completed_rt / tot.aph) * 100 : 0;
            var eff = tot.completed_rt ? (tot.completed_at / tot.completed_rt) * 100 : 0;
            var teamKey = 'itm_team_' + idx;

            html += '<tr style="background:#f0f4ff;font-weight:bold;" id="row_' + teamKey + '">'
                + '<td style="cursor:pointer;color:#0F1568;" onclick="itmToggleTeam(\'' + teamKey + '\')"><span id="btn_' + teamKey + '">+</span></td>'
                + '<td>' + (idx + 1) + '</td><td style="color:#0F1568;">' + t.team + '</td><td>' + (t.sprint_id || '-') + '</td>'
                + '<td>' + (tot.aph || 0).toFixed(2) + '</td>'
                + '<td>' + (tot.planned_rt || 0).toFixed(2) + '</td><td>' + (tot.comp_rt || 0).toFixed(2) + '</td><td>' + (tot.work_rt || 0).toFixed(2) + '</td><td>' + (tot.nt_rt || 0).toFixed(2) + '</td>'
                + '<td>' + (tot.spot_rt || 0).toFixed(2) + '</td><td>' + (tot.spot_comp_rt || 0).toFixed(2) + '</td><td>' + (tot.spot_work_rt || 0).toFixed(2) + '</td><td>' + (tot.spot_nt_rt || 0).toFixed(2) + '</td>'
                + '<td>' + (tot.total_rt || 0).toFixed(2) + '</td><td>' + (tot.at || 0).toFixed(2) + '</td>'
                + '<td' + cs(C.comp) + '>' + (tot.completed_rt || 0).toFixed(2) + '</td><td' + cs(C.comp) + '>' + (tot.completed_at || 0).toFixed(2) + '</td>'
                + '<td' + cs(C.work) + '>' + (tot.working_rt || 0).toFixed(2) + '</td><td' + cs(C.work) + '>' + (tot.working_at || 0).toFixed(2) + '</td>'
                + '<td' + cs(C.nt) + '>' + (tot.total_nt_hours || 0).toFixed(2) + '</td>'
                + '<td' + pctCell(prod) + '>' + prod.toFixed(2) + '%</td><td>' + eff.toFixed(2) + '%</td>'
                + '<td>' + (tot.biometric_hrs || 0).toFixed(2) + '</td><td>' + (tot.nc_rt || 0).toFixed(2) + '</td>'
                + '<td>' + (tot.reopen_rt || 0).toFixed(2) + '</td><td>' + (tot.de_rt || 0).toFixed(2) + '</td>'
                + '</tr>';

            (t.cbs || []).forEach(function (c, ci) {
                var cp = c.aph ? (c.completed_rt / c.aph) * 100 : 0;
                var ce = c.completed_rt ? (c.completed_at / c.completed_rt) * 100 : 0;
                var bg = ci % 2 === 0 ? '#ffffff' : '#f5f7fa';
                html += '<tr id="detail_' + teamKey + '_' + ci + '" class="detail_' + teamKey + '" style="display:none;background:' + bg + ';">'
                    + '<td></td><td></td><td style="padding-left:25px;font-style:italic;color:#555;">' + c.cb + '</td><td></td>'
                    + '<td>' + (c.aph || 0).toFixed(2) + '</td>'
                    + '<td>' + c.planned_rt.toFixed(2) + '</td><td>' + c.comp_rt.toFixed(2) + '</td><td>' + c.work_rt.toFixed(2) + '</td><td>' + c.nt_rt.toFixed(2) + '</td>'
                    + '<td>' + c.spot_rt.toFixed(2) + '</td><td>' + c.spot_comp_rt.toFixed(2) + '</td><td>' + c.spot_work_rt.toFixed(2) + '</td><td>' + c.spot_nt_rt.toFixed(2) + '</td>'
                    + '<td>' + c.total_rt.toFixed(2) + '</td><td>' + c.at.toFixed(2) + '</td>'
                    + '<td' + cs(C.comp) + '>' + c.completed_rt.toFixed(2) + '</td><td' + cs(C.comp) + '>' + c.completed_at.toFixed(2) + '</td>'
                    + '<td' + cs(C.work) + '>' + c.working_rt.toFixed(2) + '</td><td' + cs(C.work) + '>' + c.working_at.toFixed(2) + '</td>'
                    + '<td' + cs(C.nt) + '>' + c.total_nt_hours.toFixed(2) + '</td>'
                    + '<td' + pctCell(cp) + '>' + cp.toFixed(2) + '%</td><td>' + ce.toFixed(2) + '%</td>'
                    + '<td>' + c.biometric_hrs.toFixed(2) + '</td><td>' + c.nc_rt.toFixed(2) + '</td>'
                    + '<td>' + c.reopen_rt.toFixed(2) + '</td><td>' + c.de_rt.toFixed(2) + '</td>'
                    + '</tr>';
            });

            Object.keys(grand).forEach(function (k) { grand[k] += (tot[k] || 0); });
        });

        var gp = grand.aph ? (grand.completed_rt / grand.aph) * 100 : 0;
        var ge = grand.completed_rt ? (grand.completed_at / grand.completed_rt) * 100 : 0;
        html += '<tr style="background:' + C.head + ';color:#fff;font-weight:bold;">'
            + '<td></td><td colspan="3">GRAND TOTAL</td>'
            + '<td>' + grand.aph.toFixed(2) + '</td>'
            + '<td>' + grand.planned_rt.toFixed(2) + '</td><td>' + grand.comp_rt.toFixed(2) + '</td><td>' + grand.work_rt.toFixed(2) + '</td><td>' + grand.nt_rt.toFixed(2) + '</td>'
            + '<td>' + grand.spot_rt.toFixed(2) + '</td><td>' + grand.spot_comp_rt.toFixed(2) + '</td><td>' + grand.spot_work_rt.toFixed(2) + '</td><td>' + grand.spot_nt_rt.toFixed(2) + '</td>'
            + '<td>' + grand.total_rt.toFixed(2) + '</td><td>' + grand.at.toFixed(2) + '</td>'
            + '<td>' + grand.completed_rt.toFixed(2) + '</td><td>' + grand.completed_at.toFixed(2) + '</td>'
            + '<td>' + grand.working_rt.toFixed(2) + '</td><td>' + grand.working_at.toFixed(2) + '</td>'
            + '<td>' + grand.total_nt_hours.toFixed(2) + '</td>'
            + '<td' + pctCell(gp) + '>' + gp.toFixed(2) + '%</td><td>' + ge.toFixed(2) + '%</td>'
            + '<td>' + grand.biometric_hrs.toFixed(2) + '</td><td>' + grand.nc_rt.toFixed(2) + '</td>'
            + '<td>' + grand.reopen_rt.toFixed(2) + '</td><td>' + grand.de_rt.toFixed(2) + '</td>'
            + '</tr></tbody></table>';

        $('#itm-sprint-overall').html(html);
    }

    /* Drill-down toggle for team detail rows */
    window.itmToggleTeam = function (teamKey) {
        var btn = $('#btn_' + teamKey);
        var details = $('.detail_' + teamKey);
        if (details.is(':visible')) { details.hide(); btn.text('+'); }
        else { details.show(); btn.text('-'); }
    };

    /* ---- Sprint Reports / Retro Summary ---- */
    var retroTeamButtonsBuilt = false;

    function buildRetroTeamButtons() {
        if (retroTeamButtonsBuilt) return;
        retroTeamButtonsBuilt = true;
        var $wrap = $('#itm-retro-team-buttons');
        /* Summary + ALL buttons */
        ['Summary', 'ALL'].forEach(function (name) {
            $wrap.append('<button class="itm-toggle-btn itm-retro-btn" data-team="' + name + '">' + name + '</button>');
        });
        /* Dev teams from DB */
        frappe.db.get_list("Dev Team", {
            filters: { name: ["!=", "Others"] },
            fields: ["name"],
            order_by: 'name'
        }).then(function (dev_teams) {
            dev_teams.forEach(function (team) {
                $wrap.append('<button class="itm-toggle-btn itm-retro-btn" data-team="' + team.name + '">' + team.name + '</button>');
            });
        });
    }

    function loadRetroSummary(sprint) {
        buildRetroTeamButtons();
        /* Default to Summary view */
        $('#itm-retro-summary').html('<div class="itm-loading">Loading sprint report...</div>');
        frappe.call({
            method: M + "summary_total_hrs_cols",
            args: { name: sprint },
            callback: function (r) {
                if (r.message) {
                    $('#itm-retro-summary').html(r.message);
                } else {
                    $('#itm-retro-summary').html('<div class="itm-empty">No Data Found</div>');
                }
            }
        });
    }

    /* Retro team button click → per-team retro html */
    $(document).off('click', '.itm-retro-btn').on('click', '.itm-retro-btn', function () {
        $('.itm-retro-btn').removeClass('active');
        $(this).addClass('active');
        var dev_team = $(this).data('team');
        var selected_sprint = getSprint();
        if (dev_team === 'Summary') {
            loadRetroSummary(selected_sprint);
            return;
        }
        if (dev_team === 'ALL') dev_team = '';
        frappe.call({
            method: M + "get_retro_summary_html",
            args: { name: selected_sprint, dev_team: dev_team },
            callback: function (r) {
                var data = r.message || [];
                $('#itm-retro-summary').html('');
                if (data.length === 0) {
                    $('#itm-retro-summary').html('<div class="itm-empty">No Data Found in this Sprint</div>');
                    return;
                }
                data.forEach(function (section) {
                    $('#itm-retro-summary').append(
                        '<div style="padding:0 10px;margin-bottom:16px;">'
                        + '<h4 style="color:#0F1568;margin:8px 0;">' + section.team + '</h4>'
                        + section.html + '<br></div>'
                    );
                });
            }
        });
    });

    /* ---- RT vs AT % > 150% ---- */
    function loadRTATException() {
        frappe.call({
            method: M + "get_rtat_exception_data",
            args: { team: getSprintTeam(), sprint: getSprint() },
            callback: function (r) {
                if (!r.message) {
                    $("#itm-rtat-completed").html('<div class="itm-empty itm-empty-error">No Data</div>');
                    $("#itm-rtat-working").html('<div class="itm-empty itm-empty-error">No Data</div>');
                    return;
                }
                renderRTATSection("itm-rtat-completed", r.message.completed);
                renderRTATSection("itm-rtat-working", r.message.working);
            }
        });
    }

    function renderRTATSection(containerId, teams) {
        if (!teams || teams.length === 0) {
            $('#' + containerId).html('<div style="padding:20px;text-align:center;color:#888;font-weight:600;">No exceptions found</div>');
            return;
        }
        var html = '<table class="table table-bordered" style="width:100%;border-collapse:collapse;font-size:12px;">'
            + '<thead style="background:#0F1568;color:white;text-align:center;">'
            + '<tr><th>Team</th><th>Sum of RT</th><th>Sum of AT Period</th><th>Count of Task</th></tr>'
            + '</thead><tbody style="text-align:center;">';
        var gRt = 0, gAt = 0, gCnt = 0;
        teams.forEach(function (t) {
            html += '<tr style="background:#e8eaf6;font-weight:bold;">'
                + '<td>' + t.team + '</td>'
                + '<td>' + t.total_rt.toFixed(2) + '</td>'
                + '<td>' + t.total_at.toFixed(2) + '</td>'
                + '<td>' + t.total_count + '</td></tr>';
            (t.cbs || []).forEach(function (c, idx) {
                var bg = idx % 2 === 0 ? '#ffffff' : '#f5f5f5';
                html += '<tr style="background:' + bg + ';"><td style="padding-left:20px;">' + c.cb + '</td>'
                    + '<td>' + c.sum_rt.toFixed(2) + '</td><td>' + c.sum_at.toFixed(2) + '</td><td>' + c.task_count + '</td></tr>';
            });
            gRt += t.total_rt; gAt += t.total_at; gCnt += t.total_count;
        });
        html += '<tr style="background:#0F1568;color:#fff;font-weight:bold;"><td>Grand Total</td>'
            + '<td>' + gRt.toFixed(2) + '</td><td>' + gAt.toFixed(2) + '</td><td>' + gCnt + '</td></tr>';
        html += '</tbody></table>';
        $('#' + containerId).html(html);
    }

    /* ---- NT Tasks Priority High/Urgent ---- */
    function loadNTAny() {
        frappe.call({
            method: M + "get_nt_priority_tasks",
            args: { team: getSprintTeam(), sprint: getSprint(), any_sprint: 1 },
            callback: function (r) {
                if (!r.message || !r.message.teams || r.message.teams.length === 0) {
                    $("#itm-nt-any").html('<div style="padding:20px;text-align:center;color:#888;font-weight:600;">No NT tasks with High/Urgent priority found</div>');
                    return;
                }
                renderNTPriority("itm-nt-any", r.message.teams);
            }
        });
    }

    function loadNTCurrent() {
        frappe.call({
            method: M + "get_nt_priority_tasks",
            args: { team: getSprintTeam(), sprint: getSprint(), any_sprint: 0 },
            callback: function (r) {
                if (!r.message || !r.message.teams || r.message.teams.length === 0) {
                    $("#itm-nt-current").html('<div style="padding:20px;text-align:center;color:#888;font-weight:600;">No NT tasks with High/Urgent priority found</div>');
                    return;
                }
                renderNTPriority("itm-nt-current", r.message.teams);
            }
        });
    }

    function renderNTPriority(containerId, teams) {
        var html = '<table class="table table-bordered" style="width:100%;border-collapse:collapse;font-size:12px;">'
            + '<thead style="background:#0F1568;color:white;text-align:center;">'
            + '<tr>'
            + '<th rowspan="2">Team</th>'
            + '<th colspan="2" style="background:#1a237e;color:white;">Sum of RT</th>'
            + '<th colspan="2" style="background:#4a148c;color:white;">Count of Task</th>'
            + '</tr>'
            + '<tr><th>High</th><th>Urgent</th><th>High</th><th>Urgent</th></tr>'
            + '</thead><tbody style="text-align:center;">';
        var gHr = 0, gHc = 0, gUr = 0, gUc = 0;
        teams.forEach(function (t) {
            html += '<tr style="background:#e8eaf6;font-weight:bold;"><td>' + t.team + '</td>'
                + '<td>' + t.high_rt.toFixed(2) + '</td><td>' + t.urgent_rt.toFixed(2) + '</td>'
                + '<td>' + t.high_count + '</td><td>' + t.urgent_count + '</td></tr>';
            (t.cbs || []).forEach(function (c, idx) {
                var bg = idx % 2 === 0 ? '#ffffff' : '#f5f5f5';
                html += '<tr style="background:' + bg + ';"><td style="padding-left:20px;">' + c.cb + '</td>'
                    + '<td>' + c.high_rt.toFixed(2) + '</td><td>' + c.urgent_rt.toFixed(2) + '</td>'
                    + '<td>' + c.high_count + '</td><td>' + c.urgent_count + '</td></tr>';
            });
            gHr += t.high_rt; gHc += t.high_count; gUr += t.urgent_rt; gUc += t.urgent_count;
        });
        html += '<tr style="background:#0F1568;color:white;font-weight:bold;"><td>Grand Total</td>'
            + '<td>' + gHr.toFixed(2) + '</td><td>' + gUr.toFixed(2) + '</td>'
            + '<td>' + gHc + '</td><td>' + gUc + '</td></tr>';
        html += '</tbody></table>';
        $('#' + containerId).html(html);
    }

    /* ============================================================
       DAY TAB
       ============================================================ */

    /* ---- Day team filter ---- */
    var dayTeamCtrl = frappe.ui.form.make_control({
        parent: document.querySelector("#itm-day-team-filter"),
        df: { fieldtype: "Link", fieldname: "day_team", options: "Dev Team", placeholder: "Select Team", onchange: reloadDay },
        render_input: true
    });
    $(document).off("change", "#itm-day-team-filter input").on("change", "#itm-day-team-filter input", reloadDay);

    function getDayTeam() {
        return (dayTeamCtrl && dayTeamCtrl.get_value && dayTeamCtrl.get_value()) || $("#itm-day-team-filter input").val() || "";
    }

    /* ---- Day date filter ---- */
    /* Default date: yesterday if current time is before 2 PM, else today */
    function defaultDayDate() {
        var now = new Date();
        if (now.getHours() >= 14) return frappe.datetime.get_today();
        var y = new Date(now.getTime() - 24 * 60 * 60 * 1000);
        var m = ('' + (y.getMonth() + 1)).padStart(2, '0');
        var d = ('' + y.getDate()).padStart(2, '0');
        return y.getFullYear() + '-' + m + '-' + d;
    }

    var dayDateCtrl = frappe.ui.form.make_control({
        parent: document.querySelector("#itm-day-date-filter"),
        df: {
            fieldtype: "Date", fieldname: "day_date", placeholder: "Select Date",
            default: defaultDayDate()
        },
        render_input: true
    });
    // Explicitly set the default date (today if before 2pm, else yesterday)
    // Frappe's Date control auto-fills today, so we must override it
    dayDateCtrl.set_value(defaultDayDate());
    // Bind change directly on the control's input (same approach as new_it_dashboard)
    dayDateCtrl.$input.on("change", function () {
        reloadDay();
    });

    function getDayDate() {
        var val = (dayDateCtrl && dayDateCtrl.get_value && dayDateCtrl.get_value());
        if (val) return val;
        var raw = $("#itm-day-date-filter input").val();
        if (!raw) return defaultDayDate();
        return frappe.datetime.user_to_str(raw) || raw;
    }

    function reloadDay() {
        loadProductionSummary();
        loadDPR();
    }

    /* ---- Non-allocated toggle + KT filter ---- */
    var naView = "overall";
    $(document).off('click', '.itm-toggle-btn[data-view]').on('click', '.itm-toggle-btn[data-view]', function () {
        $('.itm-toggle-btn[data-view]').removeClass('active');
        $(this).addClass('active');
        naView = $(this).data('view');
        loadNonAllocated();
    });
    $(document).off('change', '#itm-kt-filter').on('change', '#itm-kt-filter', function () {
        loadNonAllocated();
    });

    /* ---- Day tab shared task cache ---- */
    var dayTaskData = null;

    function loadProductionSummary() {
        $("#itm-production-table").html('<div class="itm-empty">Loading...</div>');
        frappe.call({
            method: M + "get_today_task_data1",
            args: { from_date: getDayDate(), to_date: getDayDate(), team: getDayTeam() },
            callback: function (r) {
                if (!r || !r.message || !r.message.data || !r.message.data.length) {
                    $("#itm-production-table").html('<div class="itm-empty">No data found</div>');
                    dayTaskData = null;
                    return;
                }
                dayTaskData = r.message.data;
                window._itmTeamOrder = r.message.team_order || [];
                renderProductionTable(dayTaskData);
                applyProductionFilters();
            },
            error: function () {
                $("#itm-production-table").html('<div class="itm-empty">Error loading data</div>');
            }
        });
    }

    /* ---- Excel download for Production Table (DSR) ---- */
    $(document).off('click', '#itm-dsr-download').on('click', '#itm-dsr-download', function () {
        var date = getDayDate();
        var team = getDayTeam();
        var params = { cmd: M + 'download_dsr_excel', date: date };
        if (team) params.team = team;
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/api/method';
        form.style.display = 'none';
        form.target = '_blank';
        // Add CSRF token
        var csrf = document.createElement('input');
        csrf.type = 'hidden';
        csrf.name = 'csrf_token';
        csrf.value = frappe.csrf_token || '';
        form.appendChild(csrf);
        Object.keys(params).forEach(function (k) {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = k;
            input.value = params[k];
            form.appendChild(input);
        });
        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    });

    /* ---- Production Table: grouped by Team → CB (matches new_it_dashboard original) ---- */
    function loadProductionTable() {
        if (dayTaskData) {
            renderProductionTable(dayTaskData);
            applyProductionFilters();
        }
    }

    function getPriorityClass(priority) {
        if (!priority) return '';
        var p = priority.toLowerCase();
        if (p === 'critical') return 'itm-priority-critical';
        if (p === 'high') return 'itm-priority-high';
        if (p === 'medium') return 'itm-priority-medium';
        if (p === 'low') return 'itm-priority-low';
        return '';
    }

    function renderProductionTable(data) {
        var $c = $("#itm-production-table");
        if (!data || !data.length) { $c.html('<div class="itm-empty">No data found</div>'); return; }

        var team_order = (window._itmTeamOrder && window._itmTeamOrder.length) ? window._itmTeamOrder : [];
        var completed_statuses = ["Completed", "Pending Review", "Client Review"];

        /* Group by team → cb */
        var grouped = {};
        data.forEach(function (row) {
            var team = row[12] || "No Team";
            var cb = row[3] || "No CB";
            var is_tl = row[16] || 0;
            if (!grouped[team]) grouped[team] = {};
            if (!grouped[team][cb]) grouped[team][cb] = { tasks: [], is_tl: is_tl };
            grouped[team][cb].tasks.push(row);
        });

        var sorted_teams = team_order.filter(function (t) { return grouped[t]; });
        Object.keys(grouped).forEach(function (t) {
            if (sorted_teams.indexOf(t) === -1) sorted_teams.push(t);
        });

        var html = '<style>'
            + '#itm-production-table .scrollable-table-container { max-height:600px; overflow-y:auto; border:1px solid #ccc; margin-bottom:10px; }'
            + '#itm-production-table #itm-task-report-table { width:100%; border-collapse:collapse !important; table-layout:fixed; }'
            + '#itm-production-table #itm-task-report-table th, #itm-production-table #itm-task-report-table td { border:1px solid black; text-align:center; padding:8px; font-size:13px; }'
            + '#itm-production-table #itm-task-report-table thead th { background-color:#0F1568; color:white; font-size:13px; padding:8px; position:sticky; top:0; z-index:2; }'
            + '#itm-production-table .left-align { text-align:left !important; }'
            + '#itm-production-table .toggle-team { cursor:pointer; font-weight:bold; background-color:#eaf0f6; color:#0F1568; }'
            + '#itm-production-table .toggle-team td b { color:#0F1568; }'
            + '#itm-production-table .toggle-cb { cursor:pointer; font-weight:bold; background-color:#85819e; color:white; }'
            + '#itm-production-table .toggle-cb td b { color:white; }'
            + '#itm-production-table .team-logo img { width:45px; height:45px; border-radius:8px; border:2px solid #d9e3f0; padding:3px; background:white; }'
            + '#itm-production-table .task-row:nth-child(odd) { background-color:#ffffff; color:#000000; }'
            + '#itm-production-table .task-row:nth-child(even) { background-color:#eaf0f6; color:#000000; }'
            + '#itm-production-table .task-row a { color:inherit; text-decoration:none; }'
            + '#itm-production-table .progress-wrapper { position:relative; width:100%; height:6px; background:#eee; border-radius:10px; overflow:hidden; }'
            + '#itm-production-table .progress-bar { height:100%; border-radius:10px; transition:width 0.3s ease; }'
            + '#itm-production-table .progress-container { display:flex; flex-direction:column; align-items:center; position:relative; }'
            + '#itm-production-table .progress-bottom-text { margin-top:6px; font-size:12px; text-align:center; }'
            + '#itm-production-table .progress-hover-text { position:absolute; top:-18px; font-size:11px; opacity:0; transition:0.2s; white-space:nowrap; }'
            + '#itm-production-table .progress-container:hover .progress-hover-text { opacity:1; }'
            + '#itm-production-table .status-icon { display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; font-size:14px; font-weight:bold; cursor:pointer; transition:all 0.2s ease; border:1.5px solid transparent; }'
            + '#itm-production-table .tick-icon { background:#e3f2fd; color:#0d47a1; border-color:#90caf9; }'
            + '#itm-production-table .tick-icon:hover { background:#bbdefb; border-color:#64b5f6; transform:scale(1.3); }'
            + '#itm-production-table .c-icon { background:#ffebee; color:#b71c1c; border-color:#ef9a9a; }'
            + '#itm-production-table .c-icon:hover { background:#ffcdd2; border-color:#e57373; transform:scale(1.3); }'
            + '#itm-production-table .itm-priority-critical { color:#ff0844; font-weight:700; text-shadow:0 0 6px rgba(255,8,68,0.4); }'
            + '#itm-production-table .itm-priority-high { color:#c026ff; font-weight:700; text-shadow:0 0 6px rgba(192,38,255,0.5); }'
            + '#itm-production-table .itm-priority-medium { color:#00a8ff; font-weight:700; text-shadow:0 0 4px rgba(0,168,255,0.3); }'
            + '#itm-production-table .itm-priority-low { color:#ffb703; font-weight:700; text-shadow:0 0 4px rgba(255,183,3,0.3); }'
            + '</style>';

        /* 16 physical columns: S.No, Team, ID, Project Name, Subject, CB, ET, RT, Total RT, Priority, Status(2), AT taken, AT%, P%, E% */
        html += '<div class="scrollable-table-container"><table id="itm-task-report-table"><thead><tr>'
            + '<th style="width:3%">S.No</th>'
            + '<th style="width:6%">Team</th>'
            + '<th style="width:7%">ID</th>'
            + '<th style="width:15%">Project Name</th>'
            + '<th style="width:15%">Subject</th>'
            + '<th style="width:4%">CB</th>'
            + '<th style="width:4%">ET</th>'
            + '<th style="width:4%">RT</th>'
            + '<th style="width:5%">Total RT</th>'
            + '<th style="width:5%">Priority</th>'
            + '<th colspan="2" style="width:10%">Current Status</th>'
            + '<th style="width:5%">AT taken</th>'
            + '<th style="width:4%">AT%</th>'
            + '<th style="width:4%">P%</th>'
            + '<th style="width:4%">E%</th>'
            + '</tr></thead><tbody>';

        sorted_teams.forEach(function (team) {
            var team_id = 'itm-team-' + team.replace(/\s+/g, '_');
            var cb_groups = grouped[team];

            var sorted_cbs = Object.keys(cb_groups).map(function (cb) {
                return [cb, cb_groups[cb]];
            }).sort(function (a, b) {
                var a_order = (a[1].tasks[0][25] || 0);
                var b_order = (b[1].tasks[0][25] || 0);
                return a_order - b_order;
            });

            /* Team-level totals */
            var team_et = 0, team_rt = 0;
            sorted_cbs.forEach(function (pair) {
                pair[1].tasks.forEach(function (row) {
                    team_et += parseFloat(row[5]) || 0;
                    team_rt += parseFloat(row[14]) || 0;
                });
            });

            /* Team header with CB avatar buttons */
            var cb_buttons = '<td colspan="5" class="left-align">';
            cb_buttons += '<span class="itm-team-all-btn" data-team="' + team_id + '" data-type="all" style="cursor:pointer;font-weight:bold;text-align:center;margin-right:10px;">+ ALL</span>';
            sorted_cbs.forEach(function (pair) {
                var cb = pair[0];
                var cb_id = 'itm-cb-' + team.replace(/\s+/g, '_') + '-' + cb.replace(/\s+/g, '_');
                var cb_profile = (pair[1].tasks[0][18]) || '/assets/frappe/images/ui/avatar.png';
                cb_buttons += '<span class="itm-cb-btn" data-target="' + cb_id + '" style="cursor:pointer;margin-right:20px;display:inline-flex;flex-direction:column;align-items:center;">'
                    + '<img src="' + cb_profile + '" style="width:35px;height:35px;border-radius:50%;border:2px solid #d9e3f0;margin-bottom:3px;">'
                    + '</span>';
            });
            cb_buttons += '</td>';

            var first_cb = sorted_cbs[0][1].tasks[0];
            var team_logo = first_cb[19] || '/assets/frappe/images/ui/avatar.png';

            /* Team header: logo(1) + cb_buttons(6) + ET(1) + RT(1) + TotalRT(1) + empty(6) = 15 */
            html += '<tr class="toggle-team">'
                + '<td colspan="1" class="left-align"><div class="team-logo"><img src="' + team_logo + '"></div></td>'
                + cb_buttons
                + '<td><b>' + team_et.toFixed(2) + '</b></td>'
                + '<td><b>' + team_rt.toFixed(2) + '</b></td>'
                + '<td><b>' + team_rt.toFixed(2) + '</b></td>'
                + '<td colspan="7"></td>'
                + '</tr>';

            sorted_cbs.forEach(function (pair) {
                var cb = pair[0];
                var tasks = pair[1].tasks;
                var cb_id = 'itm-cb-' + team.replace(/\s+/g, '_') + '-' + cb.replace(/\s+/g, '_');

                /* CB-level totals and P%/E% calculation */
                var cb_et = 0, cb_rt = 0, cb_completed_rt = 0, cb_completed_at = 0;
                tasks.forEach(function (row) {
                    cb_et += parseFloat(row[5]) || 0;
                    cb_rt += parseFloat(row[14]) || 0;
                    var status = (row[10] || '').trim();
                    if (completed_statuses.indexOf(status) !== -1) {
                        cb_completed_rt += parseFloat(row[14]) || 0;
                        cb_completed_at += parseFloat(row[13]) || 0;
                    }
                });
                var cb_total_rt = cb_rt;
                var p_pct = cb_rt > 0 ? Math.round((cb_completed_rt / cb_rt) * 100 * 100) / 100 : 0;
                var e_pct = cb_completed_rt > 0 ? Math.round((cb_completed_at / cb_completed_rt) * 100 * 100) / 100 : 0;
                var cb_rowspan = tasks.length;

                var first_row = tasks[0] || [];
                /* CB header: toggle(1) + CB name(6) + ET(1) + RT(1) + TotalRT(1) + empty(6) = 15 */
                html += '<tr class="toggle-cb ' + cb_id + ' ' + team_id + '" style="display:none;">'
                    + '<td><span class="toggle-icon">+</span></td>'
                    + '<td colspan="5" class="left-align" style="color:white;">' + (first_row[24] || '') + '</td>'
                    + '<td><b>' + cb_et.toFixed(2) + '</b></td>'
                    + '<td><b>' + cb_rt.toFixed(2) + '</b></td>'
                    + '<td><b>' + cb_total_rt.toFixed(2) + '</b></td>'
                    + '<td colspan="7"></td>'
                    + '</tr>';

                var global_index = 0;
                var task_serial = 1;
                tasks.forEach(function (row, taskIdx) {
                    var bg = (global_index % 2 === 0) ? '#FFFFFF' : '#e7e6ec';
                    var rt = parseFloat(row[14]) || 0;
                    var at_taken = parseFloat(row[13]) || 0;
                    var at_pct = rt > 0 ? Math.round((at_taken / rt) * 100 * 100) / 100 : 0;
                    var progress = (at_taken > 0 && rt > 0) ? ((at_taken / rt) * 100).toFixed(0) : 0;
                    progress = parseFloat(progress);

                    var ts_color = "";
                    if (progress > 100) ts_color = "red";
                    else if (progress > 75) ts_color = "orange";
                    else if (progress > 0 && progress <= 75) ts_color = "blue";

                    var isFirstInCb = (taskIdx === 0);

                    html += '<tr class="task-row ' + cb_id + ' ' + team_id + '"'
                        + ' data-priority="' + (row[8] || '') + '"'
                        + ' data-sp="' + (row[21] == 1 ? 'S' : 'P') + '"'
                        + ' data-ro="' + (row[22] > 0 ? 'RO' : '') + '"'
                        + ' data-cf="' + (row[23] > 0 ? 'CF' : '') + '"'
                        + (ts_color ? ' data-ts="' + ts_color + '"' : '')
                        + ' style="display:none; background:' + bg + '; color:#000000;">'
                        + '<td>' + (task_serial++) + '</td>'
                        + '<td>' + (row[12] || '') + '</td>'
                        /* ID column — keep eye icon + link CSS */
                        + '<td style="white-space:nowrap;">'
                        + '<div style="display:inline-flex;align-items:center;gap:6px;white-space:nowrap;">'
                        + '<span class="itm-task-info-btn" data-task="' + row[0] + '" style="cursor:pointer;font-size:16px;color:black;flex-shrink:0;">&#128065;</span>'
                        + '<a href="/app/task/' + row[0] + '" target="_blank" style="text-decoration:none;color:inherit;flex-shrink:0;">' + row[0] + '</a>'
                        + '</div></td>'
                        + '<td class="left-align" style="word-break:break-word;overflow:hidden;"><a href="/app/project/' + (row[1] || '') + '" target="_blank" style="word-break:break-word;">' + (row[1] || '') + '</a></td>'
                        + '<td class="left-align">' + (row[2] || '') + '</td>'
                        + '<td>' + (row[3] || '') + '</td>'
                        + '<td>' + (parseFloat(row[5]) || 0).toFixed(2) + '</td>'
                        + '<td class="total">' + rt.toFixed(2) + '</td>'
                        /* Total RT — rowspan per CB group */
                        + (isFirstInCb ? '<td rowspan="' + cb_rowspan + '" style="font-weight:bold;">' + cb_total_rt.toFixed(2) + '</td>' : '')
                        + '<td class="left-align ' + getPriorityClass(row[8]) + '">' + (row[8] || '') + '</td>'
                        /* Current Status — keep progress bar CSS */
                        + '<td colspan="2" class="status-cell" style="text-align:center;">'
                        + '<div style="display:flex;align-items:center;gap:8px;justify-content:center;">';

                    if (row[20] == 0) {
                        html += '<span class="itm-confirm-task-btn status-icon tick-icon" data-task="' + row[0] + '">&#10003;</span>';
                    } else if (at_taken > 0) {
                        var prog = rt > 0 ? ((at_taken / rt) * 100).toFixed(0) : 0;
                        prog = parseFloat(prog);
                        var color = '#77e6dc';
                        if (prog > 100) color = 'red';
                        else if (prog > 75) color = 'orange';
                        var status = (row[10] || '').trim();
                        var status_display = '';
                        if (status === 'Working') status_display = 'W';
                        else if (status === 'Pending Review') status_display = 'PR';
                        else if (status === 'Client Review') status_display = 'CR';
                        else if (status === 'Completed') status_display = ' \u2713';
                        html += '<div class="progress-container" style="width:120px;">'
                            + '<div class="progress-hover-text">' + at_taken + '</div>'
                            + '<div class="progress-wrapper" style="height:6px;">'
                            + '<div class="progress-bar" style="width:' + Math.min(prog, 100) + '%; background:' + color + '; height:100%;"></div>'
                            + '</div>'
                            + '<div class="progress-bottom-text" style="color:black;font-size:13px;">' + status_display + ' ' + prog + '%</div>'
                            + '</div>';
                    } else {
                        html += '<span class="itm-task-unconfirm-btn status-icon c-icon" data-task="' + row[0] + '">C</span>';
                    }

                    html += '</div></td>'
                        + '<td>' + at_taken.toFixed(2) + '</td>'
                        + '<td>' + at_pct + '%</td>'
                        /* P% and E% — rowspan per CB group */
                        + (isFirstInCb ? '<td rowspan="' + cb_rowspan + '" style="font-weight:bold;">' + p_pct + '%</td>' : '')
                        + (isFirstInCb ? '<td rowspan="' + cb_rowspan + '" style="font-weight:bold;">' + e_pct + '%</td>' : '')
                        + '</tr>';
                    global_index++;
                });
            });
        });

        html += '</tbody></table></div>';
        $c.html(html);

        /* + ALL toggle */
        $c.find("#itm-open-all-teams-btn").off("click").on("click", function () {
            var rows = $c.find(".toggle-cb, .task-row");
            if (rows.is(":visible")) {
                rows.hide();
                $(this).text("+ ALL");
            } else {
                rows.show();
                $(this).text("- ALL");
            }
        });

        /* Per-team + ALL */
        $c.find('.itm-team-all-btn').off('click').on('click', function () {
            var teamId = $(this).data('team');
            var $rows = $c.find('.' + teamId);
            if ($rows.is(':visible')) {
                $rows.hide();
                $(this).text('+ ALL');
            } else {
                $rows.show();
                $(this).text('- ALL');
            }
        });

        /* Per-CB toggle */
        $c.find('.itm-cb-btn').off('click').on('click', function () {
            var targetClass = $(this).data('target');
            var $rows = $c.find('.' + targetClass);
            if ($rows.is(':visible')) $rows.hide();
            else $rows.show();
        });
    }

    /* ---- DSR table collapse (delegated, since HTML is injected) ---- */
    $(document).off('click', '.itm-dsr-team-btn').on('click', '.itm-dsr-team-btn', function () {
        var teamId = $(this).data('team');
        var $cbRows = $('.' + teamId).filter('.itm-dsr-cb-row');
        var $taskRows = $('.' + teamId).filter('.itm-dsr-task-row');
        if ($cbRows.is(':visible')) {
            $cbRows.hide();
            $taskRows.hide();
            $(this).text('+');
            $('.' + teamId).filter('.itm-dsr-cb-row').find('.itm-dsr-cb-btn').text('+');
        } else {
            $cbRows.show();
            $(this).text('−');
        }
    });
    $(document).off('click', '.itm-dsr-cb-btn').on('click', '.itm-dsr-cb-btn', function () {
        var cbId = $(this).data('cb');
        var $rows = $('.' + cbId).filter('.itm-dsr-task-row');
        if ($rows.is(':visible')) {
            $rows.hide();
            $(this).text('+');
        } else {
            $rows.show();
            $(this).text('−');
        }
    });

    /* ---- Production table filter chips ---- */
    $(document).off('click', '#itm-production-filters .itm-filter-btn').on('click', '#itm-production-filters .itm-filter-btn', function () {
        var group = $(this).data('group');
        var sameGroup = $('#itm-production-filters .itm-filter-btn[data-group="' + group + '"]');
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
        } else {
            sameGroup.removeClass('active');
            $(this).addClass('active');
        }
        applyProductionFilters();
    });

    function applyProductionFilters() {
        var $c = $("#itm-production-table");
        var priority = $('#itm-production-filters .itm-filter-btn[data-group="priority"].active').data('filter');
        priority = priority ? priority.toString().toLowerCase() : null;
        var sp = $('#itm-production-filters .itm-filter-btn[data-group="sp"].active').data('filter');
        var ro = $('#itm-production-filters .itm-filter-btn[data-group="ro"].active').data('filter');
        var cf = $('#itm-production-filters .itm-filter-btn[data-group="cf"].active').data('filter');

        $c.find(".task-row").hide();
        $c.find(".toggle-cb").hide();

        $c.find(".toggle-cb").each(function () {
            var cb_row = $(this);
            var cb_class = cb_row.attr('class').split(' ')[1];
            var tasks = $c.find('.' + cb_class + '.task-row');

            var matched = tasks.filter(function () {
                var p = ($(this).data('priority') || '').toString().toLowerCase();
                var s = $(this).data('sp');
                var r = $(this).data('ro');
                var c = $(this).data('cf');
                if (priority && p !== priority) return false;
                if (sp && s !== sp) return false;
                if (ro && r !== "RO") return false;
                if (cf && c !== "CF") return false;
                return true;
            });

            if (matched.length) {
                cb_row.show();
                var serial = 1;
                matched.each(function () {
                    $(this).show();
                    $(this).find("td:first").text(serial++);
                });
            }
        });
    }

    /* ---- Non-Allocated Tasks ---- */
    function loadNonAllocated() {
        var kt = $("#itm-kt-filter").val();
        $("#itm-non-allocated").html('<div class="itm-loading">Loading...</div>');
        frappe.call({
            method: M + "get_non_allocated_tasks_test",
            args: { view: naView, kt_confirmed: kt },
            callback: function (r) {
                var $c = $("#itm-non-allocated");
                if (!(r.message && r.message.data && r.message.data.length)) {
                    $c.html('<div class="itm-empty">No tasks found</div>'); return;
                }
                var tasks = r.message.data;
                var grouped = {};
                tasks.forEach(function (t) {
                    var p = t.project || "No Project";
                    if (!grouped[p]) grouped[p] = [];
                    grouped[p].push(t);
                });

                var gEt = 0, gRt = 0, gAt = 0;
                var html = '<table class="itm-table"><thead><tr>'
                    + '<th id="itm-na-toggle-all" style="cursor:pointer;">+ ALL</th><th>Sprint</th><th>Task</th><th>Subject</th>'
                    + '<th>ET</th><th>RT</th><th>AT</th><th>AGE</th><th>CF</th><th>Priority</th><th>Status</th>'
                    + '</tr></thead><tbody>';

                Object.keys(grouped).sort().forEach(function (project) {
                    var pTasks = grouped[project];
                    var pRowId = "itm_na_proj_" + project.replace(/[^a-zA-Z0-9]/g, "_");
                    var tEt = 0, tRt = 0, tAt = 0;
                    pTasks.forEach(function (t) {
                        tEt += parseFloat(t.expected_time) || 0;
                        tRt += parseFloat(t.rt) || 0;
                        tAt += parseFloat(t.actual_time) || 0;
                    });
                    gEt += tEt; gRt += tRt; gAt += tAt;

                    html += '<tr class="itm-na-project-row" data-target="' + pRowId + '" style="cursor:pointer;font-weight:bold;background:#85819e;color:#fff;">'
                        + '<td colspan="4" style="text-align:left;padding-left:10px;"><span class="itm-na-toggle-sign">+</span> ' + project + '</td>'
                        + '<td>' + tEt.toFixed(2) + '</td><td>' + tRt.toFixed(2) + '</td><td>' + tAt.toFixed(2) + '</td>'
                        + '<td colspan="4"></td></tr>';

                    pTasks.forEach(function (task, idx) {
                        var bg = idx % 2 === 0 ? '#ffffff' : '#e7e6ec';
                        var age = parseFloat(task.custom_age) || 0;
                        var ageColor = age > 3 ? '#f54545' : '#000000';
                        html += '<tr class="itm-na-task-row" data-parent="' + pRowId + '" style="display:none;background:' + bg + ';color:' + ageColor + ';">'
                            + '<td>' + (task.cb || '') + '</td><td>' + (task.custom_sprint || '') + '</td>'
                            + '<td><a href="/app/task/' + task.name + '" target="_blank">' + task.name + '</a></td>'
                            + '<td class="left-align">' + (task.subject || '') + '</td>'
                            + '<td>' + (parseFloat(task.expected_time) || 0).toFixed(2) + '</td>'
                            + '<td>' + (parseFloat(task.rt) || 0).toFixed(2) + '</td>'
                            + '<td>' + (parseFloat(task.actual_time) || 0).toFixed(2) + '</td>'
                            + '<td>' + (task.custom_age || '') + '</td>'
                            + '<td>' + (task.custom_production_date_count || '') + '</td>'
                            + '<td>' + (task.priority || '') + '</td><td>' + (task.status || '') + '</td>'
                            + '</tr>';
                    });
                });

                html += '<tr style="font-weight:bold;background:#0F1568;color:#fff;">'
                    + '<td colspan="4" style="text-align:right;">GRAND TOTAL</td>'
                    + '<td>' + gEt.toFixed(2) + '</td><td>' + gRt.toFixed(2) + '</td><td>' + gAt.toFixed(2) + '</td>'
                    + '<td colspan="4"></td></tr>';
                html += '</tbody></table>';
                $c.html(html);

                /* toggle all */
                var allExpanded = false;
                $("#itm-na-toggle-all").off("click").on("click", function () {
                    allExpanded = !allExpanded;
                    $(".itm-na-task-row").toggle(allExpanded);
                    $(".itm-na-toggle-sign").text(allExpanded ? "-" : "+");
                    $(this).text(allExpanded ? "- ALL" : "+ ALL");
                });
                /* per-project toggle */
                $(".itm-na-project-row").off("click").on("click", function () {
                    var target = $(this).data("target");
                    var $rows = $(".itm-na-task-row[data-parent='" + target + "']");
                    var $sign = $(this).find(".itm-na-toggle-sign");
                    if ($rows.is(":visible")) { $rows.hide(); $sign.text("+"); }
                    else { $rows.show(); $sign.text("-"); }
                });
            }
        });
    }

    /* ---- Re-Open & Developer Error Summary with EP&NC links ---- */
    function loadReopenDESummary() {
        var $c = $("#itm-reopen-de-summary");
        $c.html('<div class="itm-loading">Loading...</div>');
        frappe.call({
            method: M + "get_reopen_de_summary",
            args: { team: getSprintTeam(), sprint: getSprint() },
            callback: function (r) {
                var data = r.message;
                if (!data || (!data.reopen_count && !data.de_count)) {
                    $c.html('<div class="itm-empty">No Re-Open or Developer Error tasks in this sprint</div>');
                    return;
                }
                $c.html(renderReopenDESummary(data));
            }
        });
    }

    function renderReopenDESummary(data) {
        function epncBadge(epnc) {
            if (!epnc || !epnc.length) return '<span style="color:#999;font-size:11px;">—</span>';
            return epnc.map(function (e) {
                var isEP = (e.action || "").indexOf("Energy Point") !== -1;
                var color = isEP ? '#28a745' : '#dc3545';
                var label = isEP ? 'EP' : 'NC';
                var score = isEP ? (e.energy_score || e.total || '') : (e.nc_score || e.total_nc || '');
                var cls = isEP ? (e.ep_class_proposed || '') : (e.class_proposed || '');
                var txt = label + (score ? ' ' + score : '') + (cls ? ' (' + cls + ')' : '');
                var link = '/app/energy-point-and-non-conformity/' + encodeURIComponent(e.name);
                return '<a href="' + link + '" target="_blank" title="' + (e.emp_name || '') +
                    '" style="display:inline-block;margin:1px 3px;padding:1px 6px;border-radius:3px;' +
                    'background:' + color + ';color:white;font-size:10px;text-decoration:none;font-weight:600;">' +
                    txt + '</a>';
            }).join('');
        }

        function taskLink(task) {
            if (!task) return '—';
            return '<a href="/app/task/' + encodeURIComponent(task) + '" target="_blank" style="color:#0F1568;font-weight:600;text-decoration:none;">' + task + '</a>';
        }

        function reasonText(epnc) {
            if (!epnc || !epnc.length) return '<span style="color:#999;">—</span>';
            return epnc.map(function (e) {
                var reason = (e.reason_of_ep || '').trim();
                if (!reason) return '';
                var isEP = (e.action || "").indexOf("Energy Point") !== -1;
                var prefix = isEP ? 'EP' : 'NC';
                var link = '/app/energy-point-and-non-conformity/' + encodeURIComponent(e.name);
                return '<div style="margin-bottom:3px;"><a href="' + link + '" target="_blank" style="color:#0F1568;text-decoration:none;font-weight:600;">[' + prefix + ']</a> ' +
                    '<span style="color:#333;">' + reason + '</span></div>';
            }).filter(function (s) { return s; }).join('') || '<span style="color:#999;">—</span>';
        }

        function buildTable(title, rows, color, totalCount, totalRt) {
            var html = '<div style="margin-bottom:20px;">';
            html += '<div style="background:' + color + ';padding:8px 12px;border-radius:6px 6px 0 0;display:flex;justify-content:space-between;align-items:center;">';
            html += '<h4 style="margin:0;color:white;font-weight:600;font-size:13px;">' + title + '</h4>';
            html += '<span style="color:white;font-size:12px;font-weight:600;">Count: ' + totalCount + ' | RT: ' + totalRt + '</span>';
            html += '</div>';
            if (!rows.length) {
                html += '<div style="padding:12px;text-align:center;color:#999;border:1px solid #ddd;border-top:none;border-radius:0 0 6px 6px;">No ' + title.toLowerCase() + ' tasks</div>';
                html += '</div>';
                return html;
            }
            html += '<table border="1" width="100%" style="border-collapse:collapse;font-size:11px;background:white;border:1px solid #ddd;border-top:none;border-radius:0 0 6px 6px;table-layout:fixed;">';
            html += '<thead><tr style="background:#f0f0f0;color:#333;text-align:center;">';
            html += '<th style="width:8%;padding:6px;">Task</th>';
            html += '<th style="width:20%;padding:6px;">Subject</th>';
            html += '<th style="width:5%;padding:6px;">CB</th>';
            html += '<th style="width:5%;padding:6px;">RT</th>';
            html += '<th style="width:7%;padding:6px;">Revisions</th>';
            html += '<th style="width:9%;padding:6px;">CR Status</th>';
            html += '<th style="width:14%;padding:6px;">EP&amp;NC</th>';
            html += '<th style="width:32%;padding:6px;">Reason</th>';
            html += '</tr></thead><tbody>';
            rows.forEach(function (r, i) {
                var bg = i % 2 === 0 ? '#ffffff' : '#f7f7f7';
                html += '<tr style="background:' + bg + ';">';
                html += '<td style="padding:5px;text-align:center;">' + taskLink(r.task) + '</td>';
                html += '<td style="padding:5px;word-wrap:break-word;">' + (r.subject || '—') + '</td>';
                html += '<td style="padding:5px;text-align:center;">' + (r.cb || '—') + '</td>';
                html += '<td style="padding:5px;text-align:center;">' + (r.rt || 0) + '</td>';
                html += '<td style="padding:5px;text-align:center;">' + (r.revisions || 0) + '</td>';
                html += '<td style="padding:5px;text-align:center;">' + (r.cr_status || '—') + '</td>';
                html += '<td style="padding:5px;">' + epncBadge(r.epnc) + '</td>';
                html += '<td style="padding:5px;word-wrap:break-word;">' + reasonText(r.epnc) + '</td>';
                html += '</tr>';
            });
            html += '</tbody></table>';
            html += '</div>';
            return html;
        }

        var html = '';
        html += buildTable('RE-OPEN TASKS', data.reopen || [], '#dc3545', data.reopen_count, data.reopen_rt);
        html += buildTable('DEVELOPER ERROR TASKS', data.de || [], '#fd7e14', data.de_count, data.de_rt);
        return html;
    }

    /* ---- DPR Summary ---- */
    function loadDPR() {
        frappe.call({
            method: M + "dpr_table",
            args: { date: getDayDate(), team: getDayTeam() },
            callback: function (r) {
                var msg = r.message || "";
                var hasData = msg.indexOf("No Data Found") === -1 && msg.trim() !== "";
                if (hasData) {
                    $("#itm-dpr-table").html(msg);
                    $("#itm-dpr-table").closest(".itm-dpr-card").show();
                    $("#itm-dpr-download").css("display", "inline-flex");
                } else {
                    $("#itm-dpr-table").closest(".itm-dpr-card").hide();
                    $("#itm-dpr-download").hide();
                }
            }
        });
    }

    /* ---- Excel download for DPR Summary ---- */
    $(document).off('click', '#itm-dpr-download').on('click', '#itm-dpr-download', function () {
        var date = getDayDate();
        var params = { cmd: M + 'download_dpr_excel', date: date };
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/api/method';
        form.style.display = 'none';
        form.target = '_blank';
        var csrf = document.createElement('input');
        csrf.type = 'hidden';
        csrf.name = 'csrf_token';
        csrf.value = frappe.csrf_token || '';
        form.appendChild(csrf);
        Object.keys(params).forEach(function (k) {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = k;
            input.value = params[k];
            form.appendChild(input);
        });
        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    });

    /* ---- Task confirm / unconfirm actions ---- */
    $(document).off("click", ".itm-confirm-task-btn").on("click", ".itm-confirm-task-btn", function (e) {
        e.preventDefault(); e.stopPropagation();
        var btn = $(this);
        var task = btn.data("task");
        var row = btn.closest("tr");
        frappe.call({
            method: "frappe.client.set_value",
            args: { doctype: "Task", name: task, fieldname: "is_confirmed", value: 1 },
            callback: function () {
                frappe.show_alert({ message: "Task Confirmed", indicator: "green" });
                frappe.db.get_value("Task", task, "status").then(function (r) {
                    var status_text = (r.message && r.message.status) || "";
                    var completed = parseFloat(row.find(".completed").text()) || 0;
                    var total = parseFloat(row.find(".total").text()) || 0;
                    var status_cell = row.find(".status-cell");
                    var progress = total > 0 ? ((completed / total) * 100).toFixed(0) : 0;
                    var color = "#77e6dc";
                    if (progress > 100) color = "red";
                    else if (progress > 75) color = "orange";
                    var status = (status_text || "").trim();
                    var status_display = "";
                    if (status === "Working") status_display = "";
                    else if (status === "Pending Review") status_display = "PR";
                    else if (status === "Client Review") status_display = "CR";
                    else if (status === "Completed") status_display = " \u2713";
                    status_cell.html('<div style="display:flex;align-items:center;gap:8px;justify-content:center;">'
                        + '<span class="itm-task-unconfirm-btn status-icon c-icon" data-task="' + task + '">C</span>'
                        + '</div>');
                });
            }
        });
    });

    $(document).off("click", ".itm-task-unconfirm-btn").on("click", ".itm-task-unconfirm-btn", function (e) {
        e.preventDefault(); e.stopPropagation();
        var btn = $(this);
        var task = btn.data("task");
        var row = btn.closest("tr");
        frappe.call({
            method: M + "check_running_timesheet",
            args: { task: task },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint({ title: "Not Allowed", message: "This task is already running in a timesheet.", indicator: "red" });
                    return;
                }
                frappe.db.set_value("Task", task, "is_confirmed", 0).then(function () {
                    frappe.show_alert({ message: "Task Unconfirmed", indicator: "orange" });
                    var status_cell = row.find(".status-cell");
                    status_cell.html('<div style="display:flex;align-items:center;gap:8px;justify-content:center;">'
                        + '<span class="itm-confirm-task-btn status-icon tick-icon" data-task="' + task + '">&#10003;</span>'
                        + '</div>');
                });
            }
        });
    });

    /* ---- Task info dialog (👁) ---- */
    $(document).off("click", ".itm-task-info-btn").on("click", ".itm-task-info-btn", function (e) {
        e.preventDefault(); e.stopPropagation();
        var task = $(this).data("task");
        frappe.call({
            method: "frappe.client.get",
            args: { doctype: "Task", name: task },
            callback: function (r) {
                var t = r.message;
                if (!t) return;
                var html = '<div><table style="width:100%;border-collapse:collapse;border:1px solid black;">'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">Task :</b></td><td style="border:1px solid black;"><span style="color:blue;">' + (t.name || '') + '</span></td>'
                    + '<td style="border:1px solid black;"><b style="color:red;">Project :</b></td><td style="border:1px solid black;" colspan="3"><span style="color:blue;">' + (t.project || '') + '</span></td></tr>'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">Subject :</b></td><td style="border:1px solid black;" colspan="5"><span style="color:blue;">' + (t.subject || '') + '</span></td></tr>'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">Description :</b></td><td style="border:1px solid black;" colspan="5"><span style="color:blue;">' + (t.description || '') + '</span></td></tr>'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">ET :</b></td><td style="border:1px solid black;"><span style="color:blue;">' + (t.expected_time || '') + '</span></td>'
                    + '<td style="border:1px solid black;"><b style="color:red;">RT :</b></td><td style="border:1px solid black;"><span style="color:blue;">' + (t.rt || '') + '</span></td>'
                    + '<td style="border:1px solid black;"><b style="color:red;">AT :</b></td><td style="border:1px solid black;"><span style="color:blue;">' + (t.actual_time || '') + '</span></td></tr>'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">CF :</b></td><td style="border:1px solid black;" colspan="2"><span style="color:blue;">' + (t.custom_production_date_count || '') + '</span></td>'
                    + '<td style="border:1px solid black;"><b style="color:red;">RO :</b></td><td style="border:1px solid black;" colspan="2"><span style="color:blue;">' + (t.revisions || '') + '</span></td></tr>'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">Created On :</b></td><td style="border:1px solid black;"><span style="color:blue;">' + (t.creation ? frappe.datetime.str_to_user(t.creation) : '') + '</span></td>'
                    + '<td style="border:1px solid black;"><b style="color:red;">Allocated On :</b></td><td style="border:1px solid black;"><span style="color:blue;">' + (t.custom_allocated_on ? frappe.datetime.str_to_user(t.custom_allocated_on) : '') + '</span></td>'
                    + '<td style="border:1px solid black;"><b style="color:red;">Age :</b></td><td style="border:1px solid black;"><span style="color:blue;">' + (t.custom_age || '') + '</span></td></tr>'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">Developer Note :</b></td><td style="border:1px solid black;" colspan="5"><span style="color:blue;">' + (t.custom_developer_note || '') + '</span></td></tr>'
                    + '<tr><td style="border:1px solid black;"><b style="color:red;">Remarks :</b></td><td style="border:1px solid black;" colspan="5"><span style="color:blue;">' + (t.custom_taskissue_action_taken || '') + '</span></td></tr>'
                    + '</table></div>';
                var d = new frappe.ui.Dialog({
                    title: "Task Details",
                    fields: [{ fieldtype: "HTML", fieldname: "task_details", options: html }]
                });
                d.show();
                $(d.$wrapper).find('.modal-dialog').css({ "max-width": "900px", "width": "90%" });
            }
        });
    });

    /* ============================================================
       INITIAL LOAD — Project tab is active by default
       ============================================================ */
    loadProjectTab();

};