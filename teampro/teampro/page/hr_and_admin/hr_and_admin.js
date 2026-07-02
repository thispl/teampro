frappe.pages['hr-and-admin'].on_page_load = function(wrapper) {

    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: '',
        single_column: true
    });

    frappe.breadcrumbs.add('TEAMPRO');

    $(page.body).html(`
        <div class="hr-admin-container" style="background-color:white; padding:20px; min-height:100vh;">

            <div style="text-align:center; margin-bottom:20px; margin-top:0px; padding-top:0px;">
                <h2 style="margin:0; font-weight:600; letter-spacing:0.5px;">HR & Admin</h2>
                <div style="font-size:16px; color:#555; margin-top:5px;" id="current-datetime"></div>
            </div>


            <div id="ddbox-cards" style="border:1px solid #d1d8dd;border-radius:8px;padding:15px;margin-bottom:20px;background:#f2f2f2;">
                <div id="hr-summary-cards" style="
                    display:flex;
                    gap:16px;
                    flex-wrap:nowrap;
                    overflow-x:auto;
                    padding-bottom:4px;">
                </div>
            </div>
            
            <div id="ddbox-att" style="border:1px solid #d1d8dd;border-radius:8px;padding:15px;margin-bottom:20px;background:#f2f2f2;">
                <div style="background:white;color:black;font-size:18px;font-weight:bold;text-align:center;padding:10px;border-radius:6px;margin-bottom:10px;">
                    ATTENDANCE DETAILS
                </div>
                <div id="att-table"></div>
            </div>

            <!-- Chart + side table section -->
            <div id="ddbox-chart" style="border:1px solid #d1d8dd;border-radius:8px;padding:15px;margin-bottom:20px;background:#f2f2f2;">
                <div style="background:white;color:black;font-size:18px;font-weight:bold;text-align:center;padding:10px;border-radius:6px;margin-bottom:10px;">
                    WEEKLY ATTENDANCE
                </div>

                <div id="attendance-chart-page" style="display:flex; gap:16px;">

                    <div id="att-side-table" style="width:280px;min-width:280px;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:14px;max-height:400px;overflow-y:auto;">
                        <div style="text-align:center; color:#9ca3af; padding:30px 10px; font-size:13px;">
                            Loading today's attendance...
                        </div>
                    </div>

                    <div style="flex:1;background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:24px;">
                    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
                        <div>
                            <h3 style="margin:0 0 4px 0; font-weight:700;">Data Activity</h3>
                            <p style="margin:0; font-size:12px; color:#9ca3af;" id="chart-subtitle">
                                Present attendance for this week
                            </p>
                        </div>
                        <select id="att-status-filter" class="form-control" style="width:140px; height:34px; font-size:13px;">
                            <option value="Present" selected>Present</option>
                            <option value="Absent">Absent</option>
                            <option value="Half Day">Half Day</option>
                        </select>
                    </div>
                        <canvas id="attendanceChart" height="120"></canvas>
                    </div>

                </div>
            </div>

            

            <div id="ddbox-att" style="border:1px solid #d1d8dd;border-radius:8px;padding:15px;margin-bottom:20px;background:#f2f2f2; display:flex; gap:16px;">

                <!-- Left — Late Punch -->
                <div style="flex:1; background:#f2f2f2; border-radius:8px; padding:12px;border:1px solid #d1d8dd;">
                    <div style="background:white; padding:10px 15px; border-radius:6px; margin-bottom:10px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">

                    <h4 style="margin:0; margin-left:130px; font-size:18px; font-weight:bold; color:black; text-transform:uppercase; text-align:center;">
                        LATE PUNCH (This Month)
                    </h4>
                    </div>
                    <div id="late-punch-table" style="max-height:300px; overflow-y:auto;"></div>
                </div>

                <!-- Right — Leave Applications -->
                <div style="flex:1; background:#f2f2f2; border-radius:8px; padding:12px;border:1px solid #d1d8dd;">
                    <div style="background:white; padding:10px 15px; border-radius:6px; margin-bottom:10px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">

                    <h4 style="margin:0; margin-left:130px; font-size:18px; font-weight:bold; color:black; text-transform:uppercase; text-align:center;">
                        LEAVE APPLICATIONS (This Month)
                    </h4>
                    </div>
                    <div id="month-leave-table" style="max-height:300px; overflow-y:auto;"></div>
                </div>

            </div>

            <div id="ddbox-charts" style="border:1px solid #d1d8dd; border-radius:8px; padding:15px; margin-bottom:20px; background:#f2f2f2; display:flex; gap:16px;">

            <!-- Left — Experience Chart -->
            <div style="flex:1; background:white; border-radius:8px; padding:16px; border:1px solid #d1d8dd;">
                <h4 style="margin:0 0 16px 0; font-size:15px; font-weight:bold; text-align:center; text-transform:uppercase;">
                    Employees by Experience
                </h4>
                <canvas id="experienceChart" height="200"></canvas>
            </div>

            <!-- Right — Salary Distribution -->
            <div style="flex:1; background:white; border-radius:8px; padding:16px; border:1px solid #d1d8dd;">
                <h4 style="margin:0 0 16px 0; font-size:15px; font-weight:bold; text-align:center; text-transform:uppercase;">
                    Payroll Distribution by Gender
                </h4>
                <canvas id="salaryChart" height="200"></canvas>
            </div>

        </div>

        <!-- Add below charts section -->
        <div id="ddbox-att-req" style="border:1px solid #d1d8dd; border-radius:8px; padding:15px; margin-bottom:20px; background:#f2f2f2;">

            <div style="background:white; padding:10px 15px; border-radius:6px; margin-bottom:10px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
                <h4 style="margin:0; font-size:16px; font-weight:bold; text-transform:uppercase;">
                    Attendance Requests (This Month)
                </h4>
                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                    <button id="btn-permission" class="btn btn-sm att-req-btn"
                        onclick="load_att_request_table('Permission')"
                        style="background:#0F1568; color:white; border:none; border-radius:6px; padding:6px 14px;">
                        Permission
                    </button>
                    <button id="btn-misspunch" class="btn btn-sm att-req-btn"
                        onclick="load_att_request_table('Miss Punch')"
                        style="background:#e5e7eb; color:#374151; border:none; border-radius:6px; padding:6px 14px;">
                        Miss Punch
                    </button>
                    <button id="btn-onduty" class="btn btn-sm att-req-btn"
                        onclick="load_att_request_table('On Duty Working Day')"
                        style="background:#e5e7eb; color:#374151; border:none; border-radius:6px; padding:6px 14px;">
                        On Duty Working Day
                    </button>
                    <button id="btn-compoff-od" class="btn btn-sm att-req-btn"
                        onclick="load_att_request_table('Comp Off On Duty Holiday')"
                        style="background:#e5e7eb; color:#374151; border:none; border-radius:6px; padding:6px 14px;">
                        Comp Off - On Duty Holiday
                    </button>
                    <button id="btn-compoff-ph" class="btn btn-sm att-req-btn"
                        onclick="load_att_request_table('Comp Off Present Holiday')"
                        style="background:#e5e7eb; color:#374151; border:none; border-radius:6px; padding:6px 14px;">
                        Comp Off - Present Holiday
                    </button>
                </div>
            </div>

            <div id="att-req-table" style="max-height:350px; overflow-y:auto;"></div>

        </div>

            <div id="epnc-wrapper" style="border:1px solid #d1d8dd; border-radius:8px; padding:15px; margin-bottom:20px; background:#f2f2f2;">

                <div style="background:white; padding:10px 15px; border-radius:6px; margin-bottom:10px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">

                    <h4 style="margin:0; margin-left:300px; font-size:18px; font-weight:bold; color:black; text-transform:uppercase; text-align:center; flex-grow: 1;">
                        Energy Point And Non Conformity
                    </h4>

                    <div id="epnc-filters" style="display:flex; align-items:center; gap:10px;">
                        <input type="date" id="epnc-from-date" class="form-control" style="width:140px; height:32px; padding:4px 8px;">
                        <input type="date" id="epnc-to-date" class="form-control" style="width:140px; height:32px; padding:4px 8px;">
                        <button class="btn btn-primary btn-sm" id="apply-epnc-filter" style="height:32px; line-height:1;">Apply</button>
                    </div>

                </div>

                <div id="epnc-table-content" style="overflow:auto; max-height:500px; padding:5px;">
                    <div style="text-align:center; padding:20px;">Loading...</div>
                </div>

            </div>

        </div>
    `);

    $(`<style>
        .page-head.flex, .page-head {
            display: none !important;
        }
        .hr-admin-container {
            padding-top: 5px !important;
        }

        .hr-stat-card {
            min-width: 220px;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            cursor: pointer;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            position: relative;
            overflow: hidden;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            padding: 14px 18px;
            gap: 14px;
            border-right: 5px solid transparent;
        }
        .hr-stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
        .hr-stat-icon-wrap {
            width: 48px;
            height: 48px;
            min-width: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .hr-stat-text {
            display: flex;
            flex-direction: column;
        }
        .hr-stat-label {
            font-size: 11px;
            color: black;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
        }
        .hr-stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #111827;
            margin-top: 2px;
        }

        #hr-summary-cards {
        display: flex;
        gap: 16px;
        flex-wrap: nowrap;
        padding: 8px 4px;
    }
    .hr-stat-card {
        min-width: 140px;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        cursor: pointer;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        border-top: 4px solid transparent;
        padding: 20px 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .hr-stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    .card-active  { border-top-color: #16a34a; }
    .card-male    { border-top-color: #2563eb; }
    .card-female  { border-top-color: #db2777; }
    .card-present { border-top-color: #0d9488; }
    .card-absent  { border-top-color: #dc2626; }

        #epnc-table-content table thead th {
            background: #0F1568 !important;
            color: white !important;
            text-align: center;
            vertical-align: middle;
            padding: 10px;
        }

        #epnc-table-content table tbody tr:nth-child(odd) {
            background: #ffffff !important;
        }

        #epnc-table-content table tbody tr:nth-child(even) {
            background: #E7E6EC !important;
        }

        #epnc-table-content table td {
            text-align: center;
            vertical-align: middle;
            padding: 8px;
        }
    </style>`).appendTo('head');

    

    let attendanceChartInstance = null;
    let weeklyChartData = [];
    let currentStatusFilter = "Present";

    const statusColors = {
        "Present": { line: "#10b981", grad: "16, 185, 129" },
        "Absent": { line: "#dc2626", grad: "220, 38, 38" },
        "Half Day": { line: "#f59e0b", grad: "245, 158, 11" }
    };

    function load_attendance_chart(status = "Present") {
        currentStatusFilter = status;

        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_weekly_attendance_chart",
            args: { status_filter: status },
            callback: function(r) {
                if (!r.message) return;
                weeklyChartData = r.message;
                render_attendance_chart(weeklyChartData, status);

                $('#chart-subtitle').text(`${status} attendance for this week`);

                // Default — today's data
                const today = frappe.datetime.get_today();
                const todayItem = weeklyChartData.find(d => d.date === today);
                if (todayItem) {
                    load_attendance_side_table(todayItem.date, todayItem.label, status);
                }
            }
        });
    }

    function render_attendance_chart(data, status) {
        const ctx = document.getElementById('attendanceChart').getContext('2d');

        const labels = data.map(d => d.label);
        const counts = data.map(d => d.count);
        const colors = statusColors[status];

        if (attendanceChartInstance) {
            attendanceChartInstance.destroy();
        }

        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, `rgba(${colors.grad}, 0.25)`);
        gradient.addColorStop(1, `rgba(${colors.grad}, 0)`);

        attendanceChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: status,
                    data: counts,
                    borderColor: colors.line,
                    backgroundColor: gradient,
                    borderWidth: 2.5,
                    tension: 0.45,
                    fill: true,
                    pointRadius: 5,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: colors.line,
                    pointBorderWidth: 2,
                    pointHoverRadius: 7,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#ffffff',
                        titleColor: '#111827',
                        bodyColor: '#6b7280',
                        borderColor: '#e5e7eb',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            title: function(ctx) {
                                return `${ctx[0].parsed.y} ${currentStatusFilter}`;
                            },
                            label: function(ctx) {
                                return weeklyChartData[ctx.dataIndex].date;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f3f4f6' },
                        ticks: { color: '#9ca3af' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#9ca3af' }
                    }
                },
                onClick: function(evt, elements) {
                    if (elements.length > 0) {
                        const idx = elements[0].index;
                        const clickedDate = weeklyChartData[idx].date;
                        load_attendance_side_table(clickedDate, weeklyChartData[idx].label, currentStatusFilter);
                    }
                },
                onHover: function(evt, elements) {
                    evt.native.target.style.cursor = elements.length ? 'pointer' : 'default';
                }
            }
        });
    }

    function load_attendance_side_table(date, label, status_filter) {
        $('#att-side-table').html(`<div style="text-align:center;padding:30px;">Loading...</div>`);

        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_attendance_by_date",
            args: { date: date, status_filter: status_filter },
            callback: function(r) {
                const data = r.message || [];

                let rows = data.map((row, idx) => {
                    let badgeColor = "#dcfce7", textColor = "#16a34a", displayStatus = row.status;;
                    if (row.status === "Absent") { badgeColor = "#fee2e2"; textColor = "#dc2626"; }
                    else if (row.status === "Half Day") { badgeColor = "#fef3c7"; textColor = "#d97706"; displayStatus = "HD"; }

                    return `
                        <tr>
                            <td style="text-align:center; padding:6px 4px; font-size:12px;">${idx + 1}</td>
                            <td style="text-align:left; padding:6px 4px; font-size:12px;">${row.employee_name}</td>
                            <td style="text-align:center; padding:6px 4px; font-size:12px;">
                                <span style="
                                    padding:2px 8px;
                                    border-radius:10px;
                                    font-size:10px;
                                    font-weight:600;
                                    background:${badgeColor};
                                    color:${textColor};
                                ">${displayStatus}</span>
                            </td>
                        </tr>
                    `;
                }).join('');

                $('#att-side-table').html(`
                    <div style="font-weight:700; font-size:13px; margin-bottom:10px; color:#111827;">
                        ${label}
                    </div>
                    <table style="width:100%; border-collapse:collapse;">
                        <thead>
                            <tr style="border-bottom:1px solid #e5e7eb;">
                                <th style="text-align:center; font-size:11px; color:#9ca3af; padding:6px 4px;">S#</th>
                                <th style="text-align:left; font-size:11px; color:#9ca3af; padding:6px 4px;">Name</th>
                                <th style="text-align:center; font-size:11px; color:#9ca3af; padding:6px 4px;">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rows || '<tr><td colspan="3" style="text-align:center;padding:20px;color:#9ca3af;">No records</td></tr>'}
                        </tbody>
                    </table>
                `);
            }
        });
    }

    // ✅ Filter dropdown change event
    $(wrapper).on('change', '#att-status-filter', function() {
        const status = $(this).val();
        load_attendance_chart(status);
    });

    // function render_summary_cards(data) {
    //     const cards = [
    //         { key: "active", label: "Active", icon: "fa-user-o", color: "#16a34a", circle: "#dcfce7", cls: "card-active" },
    //         { key: "male", label: "Male", icon: "fa-mars", color: "#2563eb", circle: "#dbeafe", cls: "card-male" },
    //         { key: "female", label: "Female", icon: "fa-venus", color: "#db2777", circle: "#fce7f3", cls: "card-female" },
    //         { key: "present", label: "Today Present", icon: "fa-calendar-check-o", color: "#0d9488", circle: "#ccfbf1", cls: "card-present" },
    //         { key: "absent", label: "Today Absent", icon: "fa-calendar-times-o", color: "#dc2626", circle: "#fee2e2", cls: "card-absent" }
    //     ];

    //     let html = cards.map(c => {
    //         const stat = data[c.key] || { total: 0, departments: [] };
    //         return `
    //             <div class="hr-stat-card ${c.cls}" onclick='show_dept_breakdown("${c.key}", "${c.label}")'>
    //                 <div class="hr-stat-icon-wrap" style="background:${c.circle}; color:${c.color};">
    //                     <i class="fa ${c.icon}"></i>
    //                 </div>
    //                 <div class="hr-stat-text">
    //                     <div class="hr-stat-label">${c.label}</div>
    //                     <div class="hr-stat-value">${stat.total}</div>
    //                 </div>
    //             </div>
    //         `;
    //     }).join('');

    //     $('#hr-summary-cards').html(html);
    //     window._hr_summary_data = data;
    // }

    function render_summary_cards(data) {
        const cards = [
            { key: "active",  cls: "card-active",  title: "ACTIVE",        icon: "fa-user-o",           color: "#16a34a", circle: "#dcfce7" },
            { key: "male",    cls: "card-male",    title: "MALE",          icon: "fa-mars",             color: "#2563eb", circle: "#dbeafe" },
            { key: "female",  cls: "card-female",  title: "FEMALE",        icon: "fa-venus",            color: "#db2777", circle: "#fce7f3" },
            { key: "present", cls: "card-present", title: "TODAY PRESENT", icon: "fa-calendar-check-o", color: "#0d9488", circle: "#ccfbf1" },
            { key: "absent",  cls: "card-absent",  title: "TODAY ABSENT",  icon: "fa-calendar-times-o", color: "#dc2626", circle: "#fee2e2" }
        ];

        let html = cards.map(c => {
            const stat = data[c.key] || { total: 0 };
            return `
                <div class="hr-stat-card ${c.cls}" onclick='show_dept_breakdown("${c.key}", "${c.title}")'>

                    <!-- Icon center -->
                    <div style="
                        width: 44px; height: 44px;
                        border-radius: 12px;
                        background: ${c.circle};
                        color: ${c.color};
                        display: flex; align-items: center; justify-content: center;
                        font-size: 18px;
                        margin-bottom: 12px;
                    ">
                        <i class="fa ${c.icon}"></i>
                    </div>

                    <!-- Heading -->
                    <div style="font-size:13px; font-weight:700; color:#111827; letter-spacing:0.5px; margin-bottom:6px;">
                        ${c.title}
                    </div>

                    <!-- Value -->
                    <div style="font-size:28px; font-weight:800; color:${c.color}; line-height:1;">
                        ${stat.total}
                    </div>

                </div>
            `;
        }).join('');

        $('#hr-summary-cards').html(html);
        window._hr_summary_data = data;
    }

    function load_summary_cards() {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_hr_summary_cards",
            callback: function(r) {
                if (r.message) {
                    render_summary_cards(r.message);
                }
            }
        });
    }

    window.show_dept_breakdown = function(key, label) {
        const stat = window._hr_summary_data[key];
        if (!stat) return;

        let rows = "";
        (stat.departments || []).forEach((d, idx) => {
            rows += `
                <tr>
                    <td style="text-align:center;">${idx + 1}</td>
                    <td style="text-align:left;">${d.department || "Not Set"}</td>
                    <td style="text-align:center;">${d.count}</td>
                </tr>
            `;
        });

        let dialog = new frappe.ui.Dialog({
            title: `${label} — Department`,
            size: "small",
            fields: [{ fieldtype: "HTML", fieldname: "details" }]
        });

        dialog.fields_dict.details.$wrapper.html(`
            <table class="table table-bordered table-sm">
                <thead style="background:#002060; color:white;">
                    <tr>
                        <th style="text-align:center;">S#</th>
                        <th style="text-align:center;">Department</th>
                        <th style="text-align:center;">Count</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows || '<tr><td colspan="3" style="text-align:center;">No data found</td></tr>'}
                </tbody>
                <tfoot>
                    <tr style="background:#f0f0f0; font-weight:bold;">
                        <td colspan="2" style="text-align:center;">Total</td>
                        <td style="text-align:center;">${stat.total}</td>
                    </tr>
                </tfoot>
            </table>
        `);

        dialog.show();
    };

    function loadepnc(from_date = null, to_date = null) {
        $('#epnc-table-content').html(`<div style="text-align:center;padding:20px;">Loading...</div>`);

        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.epnc_table",
            args: { from_date: from_date, to_date: to_date },
            callback: function(r) {
                if (r.message) {
                    $('#epnc-table-content').html(r.message);
                } else {
                    $('#epnc-table-content').html(`<div style="text-align:center;padding:20px;">No Data Found</div>`);
                }
            }
        });
    }

    function load_att_table() {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_today_attendance",
            callback: function(r) {

                let data = r.message || [];
                let rows = "";

                data.forEach((d, i) => {

                    let status_html = "";

                    if (d.status === "Present") {
                        status_html = `<span style="color:green;font-weight:bold;">Present</span>`;
                    }
                    else if (d.status === "Half Day") {
                        status_html = `<span style="color:orange;font-weight:bold;">Half Day</span>`;
                    }
                    else {
                        status_html = `<span style="color:red;font-weight:bold;">Absent</span>`;
                    }

                    let row_bg = (i % 2 === 0) ? "#ffffff" : "#e7e6ec";

                    rows += `
                        <tr style="background:${row_bg};">
                            <td style="text-align:center;">${i + 1}</td>
                            <td style="text-align:center;">${d.employee || ""}</td>
                            <td>${d.employee_name || ""}</td>
                            <td style="text-align:center;">
                                ${d.attendance_date ? frappe.datetime.str_to_user(d.attendance_date) : ""}
                            </td>
                            <td style="text-align:center;">${d.in_time || "-"}</td>
                            <td style="text-align:center;">${d.out_time || "-"}</td>
                            <td style="text-align:center;">${d.bt_difference || "-"}</td>
                            <td style="text-align:center;">${status_html}</td>
                        </tr>
                    `;
                });

                let html = `
                    <div style="height:300px; overflow-y:auto;">
                        <table class="table table-bordered" style="margin-bottom:0; width:100%; border-collapse:collapse;">
                            <thead>
                                <tr>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">S#</th>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Emp ID</th>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Emp Name</th>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Date</th>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">In Time</th>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Out Time</th>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">BT Difference</th>
                                    <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${rows}
                            </tbody>
                        </table>
                    </div>
                `;

                $("#att-table").html(html);
            }
        });
    }

    function update_datetime() {
        const now = new Date();
        const date = now.toLocaleDateString('en-IN', {
            year: 'numeric', month: 'long', day: 'numeric'
        });
        const time = now.toLocaleTimeString('en-IN', {
            hour: '2-digit', minute: '2-digit', second: '2-digit',
            hour12: true
        }).toUpperCase();
        $('#current-datetime').text(`${date} | ${time}`);
    }   

    function ensure_chartjs_loaded(callback) {
        if (window.Chart) {
            callback();
        } else {
            $.getScript('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js')
                .done(function() {
                    callback();
                })
                .fail(function() {
                    console.error("Failed to load Chart.js");
                    $('#attendanceChart').closest('div').html(
                        '<div style="text-align:center;color:red;padding:20px;">Chart library failed to load</div>'
                    );
                });
        }
    }

    // Init calls
    update_datetime();
    setInterval(update_datetime, 1000);

    load_summary_cards();
    ensure_chartjs_loaded(function() {
        load_attendance_chart();
    });
    load_att_table();
    loadepnc();

    $(wrapper).on('click', '#apply-epnc-filter', function() {
        let from_date = $('#epnc-from-date').val() || null;
        let to_date = $('#epnc-to-date').val() || null;
        loadepnc(from_date, to_date);
    });

    function load_late_punch_table() {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_late_punch_summary",
            callback: function(r) {
                const data = r.message || [];
                window._late_punch_data = data;

                let rows = data.map((row, i) => {
                    let row_bg = (i % 2 === 0) ? "#ffffff" : "#e7e6ec";
                    return `
                        <tr style="background:${row_bg};">
                            <td style="text-align:center; padding:8px;">${i + 1}</td>
                            <td style="text-align:left; padding:8px;">${row.employee_name}</td>
                            <td style="text-align:center; padding:8px;">
                                <span onclick="show_late_dates(${i})" style="
                                    display:inline-flex;
                                    align-items:center;
                                    justify-content:center;
                                    width:27px;
                                    height:20px;
                                    border-radius:50%;
                                    background:#fee2e2;
                                    color:#dc2626;
                                    font-weight:700;
                                    font-size:13px;
                                    cursor:pointer;
                                ">${row.late_count}</span>
                            </td>
                        </tr>
                    `;
                }).join('');

                $('#late-punch-table').html(`
                    <table class="table table-bordered" style="margin-bottom:0; width:100%; border-collapse:collapse;">
                        <thead>
                            <tr>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">S#</th>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:left; z-index:10;">Emp Name</th>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Late Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rows || '<tr><td colspan="3" style="text-align:center;padding:20px;">No records</td></tr>'}
                        </tbody>
                    </table>
                `);
            }
        });
    }

    function load_month_leave_table() {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_month_leave_applications",
            callback: function(r) {
                const data = r.message || [];

                let rows = data.map((row, i) => {
                    let row_bg = (i % 2 === 0) ? "#ffffff" : "#e7e6ec";
                    const isApproved = (row.workflow_state || '').toLowerCase().includes('approved');
                    return `
                        <tr style="background:${row_bg};">
                            <td style="text-align:center; padding:8px;">${i + 1}</td>
                            <td style="text-align:left; padding:8px;">${row.employee_name}</td>
                            <td style="text-align:center; padding:8px;">${frappe.datetime.str_to_user(row.from_date)}</td>
                            <td style="text-align:center; padding:8px;">${frappe.datetime.str_to_user(row.to_date)}</td>
                            <td style="text-align:center; padding:8px;">${row.total_leave_days}</td>
                            <td style="text-align:center; padding:8px;">
                                <span style="
                                    padding:3px 10px;
                                    border-radius:10px;
                                    font-size:11px;
                                    font-weight:600;
                                    background:${isApproved ? '#dcfce7' : '#fef3c7'};
                                    color:${isApproved ? '#16a34a' : '#d97706'};
                                ">${row.workflow_state || '-'}</span>
                            </td>
                        </tr>
                    `;
                }).join('');

                $('#month-leave-table').html(`
                    <table class="table table-bordered" style="margin-bottom:0; width:100%; border-collapse:collapse;">
                        <thead>
                            <tr>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">S#</th>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:left; z-index:10;">Emp Name</th>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">From</th>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">To</th>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Days</th>
                                <th style="position:sticky; top:0; background:#0F1568; color:white; text-align:center; z-index:10;">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rows || '<tr><td colspan="6" style="text-align:center;padding:20px;">No records</td></tr>'}
                        </tbody>
                    </table>
                `);
            }
        });
    }

    window.show_late_dates = function(idx) {
        const row = window._late_punch_data[idx];
        if (!row) return;

        // ✅ Sort dates + times together by date
        const combined = row.dates.map((d, i) => ({ date: d, time: row.times[i] }));
        combined.sort((a, b) => new Date(a.date) - new Date(b.date));

        let dateRows = combined.map((item, i) => `
            <tr>
                <td style="text-align:center; padding:6px;">${i + 1}</td>
                <td style="text-align:center; padding:6px;">${frappe.datetime.str_to_user(item.date)}</td>
                <td style="text-align:center; padding:6px;">${item.time}</td>
            </tr>
        `).join('');

        let dialog = new frappe.ui.Dialog({
            title: `Late Punch Dates — ${row.employee_name}`,
            size: "small",
            fields: [{ fieldtype: "HTML", fieldname: "details" }]
        });

        dialog.fields_dict.details.$wrapper.html(`
            <table class="table table-bordered table-sm">
                <thead style="background:#002060; color:white;">
                    <tr>
                        <th style="text-align:center;">S#</th>
                        <th style="text-align:center;">Date</th>
                        <th style="text-align:center;">In Time</th>
                    </tr>
                </thead>
                <tbody>
                    ${dateRows}
                </tbody>
            </table>
        `);

        dialog.show();
    };

    // Init calls
    load_late_punch_table();
    load_month_leave_table();

    
    function load_experience_chart() {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_experience_chart_data",
            callback: function(r) {
                if (!r.message) return;
                const data = r.message;

                const labels = Object.keys(data);
                const maleData = labels.map(l => data[l]["Male"]);
                const femaleData = labels.map(l => data[l]["Female"]);

                const ctx = document.getElementById('experienceChart').getContext('2d');

                // new Chart(ctx, {
                //     type: 'bar',
                //     data: {
                //         labels: labels,
                //         datasets: [
                //             { label: 'Male', data: maleData, backgroundColor: '#3b82f6', borderRadius: 4 },
                //             { label: 'Female', data: femaleData, backgroundColor: '#2dd4bf', borderRadius: 4 }
                //         ]
                //     },
                //     options: {
                //         responsive: true,
                //         plugins: {
                //             legend: { position: 'top', labels: { usePointStyle: true } }
                //         },
                //         scales: {
                //             x: { stacked: true, grid: { display: false } },
                //             y: { stacked: true, beginAtZero: true, grid: { color: '#f3f4f6' } }
                //         },
                //         // ✅ Click handler
                //         onClick: function(evt, elements) {
                //             if (elements.length > 0) {
                //                 const el = elements[0];
                //                 const bucket = labels[el.index];
                //                 const gender = el.datasetIndex === 0 ? "Male" : "Female";
                //                 show_experience_employees(bucket, gender);
                //             }
                //         },
                //         onHover: function(evt, elements) {
                //             evt.native.target.style.cursor = elements.length ? 'pointer' : 'default';
                //         }
                //     }
                // });
                new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'Male', data: maleData, backgroundColor: '#3b82f6', borderRadius: 4 },
                        { label: 'Female', data: femaleData, backgroundColor: '#2dd4bf', borderRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top', labels: { usePointStyle: true } },
                        tooltip: {
                            callbacks: {
                                label: function(ctx) {
                                    return `${ctx.dataset.label}: ${ctx.parsed.y}`;
                                },
                                title: function(ctx) {
                                    return ctx[0].label;
                                }
                            }
                        }
                    },
                    scales: {
                        x: { stacked: false, grid: { display: false } },
                        y: { stacked: false, beginAtZero: true, grid: { color: '#f3f4f6' } }
                    },
                    onClick: function(evt, elements) {
                        if (elements.length > 0) {
                            const el = elements[0];
                            const bucket = labels[el.index];
                            const gender = el.datasetIndex === 0 ? "Male" : "Female";
                            show_experience_employees(bucket, gender);
                        }
                    },
                    onHover: function(evt, elements) {
                        evt.native.target.style.cursor = elements.length ? 'pointer' : 'default';
                    }
                }
            });
            }
        });
    }

    function load_salary_chart() {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_salary_distribution",
            callback: function(r) {
                if (!r.message) return;
                const data = r.message;

                const labels = Object.keys(data);
                const maleData = labels.map(l => data[l]["Male"]);
                const femaleData = labels.map(l => data[l]["Female"]);

                const ctx = document.getElementById('salaryChart').getContext('2d');

                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            { label: 'Female', data: femaleData, backgroundColor: '#f97316', borderRadius: 4 },
                            { label: 'Male', data: maleData, backgroundColor: '#eab308', borderRadius: 4 }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'top', labels: { usePointStyle: true } }
                        },
                        scales: {
                            x: { beginAtZero: true, grid: { color: '#f3f4f6' } },
                            y: { grid: { display: false } }
                        },
                        // ✅ Click handler
                        onClick: function(evt, elements) {
                            if (elements.length > 0) {
                                const el = elements[0];
                                const bucket = labels[el.index];
                                const gender = el.datasetIndex === 0 ? "Female" : "Male";
                                show_salary_employees(bucket, gender);
                            }
                        },
                        onHover: function(evt, elements) {
                            evt.native.target.style.cursor = elements.length ? 'pointer' : 'default';
                        }
                    }
                });
            }
        });
    }
    

    window.show_experience_employees = function(bucket, gender) {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_experience_employees",
            args: { bucket: bucket, gender: gender },
            callback: function(r) {
                const data = r.message || [];

                let rows = data.map((row, idx) => `
                    <tr>
                        <td style="text-align:center; padding:6px;">${idx + 1}</td>
                        <td style="text-align:left; padding:6px;">${row.employee}</td>
                        <td style="text-align:left; padding:6px;">${row.employee_name}</td>
                        <td style="text-align:left; padding:6px;">${row.department || '-'}</td>
                        <td style="text-align:center; padding:6px;">${row.experience} yrs</td>
                        <td style="text-align:center; padding:6px;">
                            <span style="
                                padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600;
                                background:${row.gender === 'Male' ? '#dbeafe' : '#fce7f3'};
                                color:${row.gender === 'Male' ? '#2563eb' : '#db2777'};
                            ">${row.gender}</span>
                        </td>
                    </tr>
                `).join('');

                let dialog = new frappe.ui.Dialog({
                    title: `${gender} — ${bucket} (${data.length} employees)`,
                    size: "large",
                    fields: [{ fieldtype: "HTML", fieldname: "details" }]
                });

                dialog.fields_dict.details.$wrapper.html(`
                    <table class="table table-bordered table-sm">
                        <thead style="background:#002060; color:white;">
                            <tr>
                                <th style="text-align:center;">S#</th>
                                <th style="text-align:center;">Emp ID</th>
                                <th style="text-align:center;">Name</th>
                                <th style="text-align:center;">Department</th>
                                <th style="text-align:center;">Experience</th>
                                <th style="text-align:center;">Gender</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rows || '<tr><td colspan="6" style="text-align:center;padding:20px;">No records</td></tr>'}
                        </tbody>
                    </table>
                `);

                dialog.show();
            }
        });
    };

    window.show_salary_employees = function(bucket, gender) {
        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_salary_employees",
            args: { bucket: bucket, gender: gender },
            callback: function(r) {
                const data = r.message || [];

                let rows = data.map((row, idx) => `
                    <tr>
                        <td style="text-align:center; padding:6px;">${idx + 1}</td>
                        <td style="text-align:left; padding:6px;">${row.employee}</td>
                        <td style="text-align:left; padding:6px;">${row.employee_name}</td>
                        <td style="text-align:left; padding:6px;">${row.department || '-'}</td>
                        <td style="text-align:right; padding:6px;">₹${parseFloat(row.net_pay || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}</td>
                        <td style="text-align:center; padding:6px;">
                            <span style="
                                padding:2px 8px; border-radius:10px; font-size:10px; font-weight:600;
                                background:${row.gender === 'Male' ? '#dbeafe' : '#fce7f3'};
                                color:${row.gender === 'Male' ? '#2563eb' : '#db2777'};
                            ">${row.gender}</span>
                        </td>
                    </tr>
                `).join('');

                let dialog = new frappe.ui.Dialog({
                    title: `${gender} — ${bucket} Salary Range (${data.length} employees)`,
                    size: "large",
                    fields: [{ fieldtype: "HTML", fieldname: "details" }]
                });

                dialog.fields_dict.details.$wrapper.html(`
                    <table class="table table-bordered table-sm">
                        <thead style="background:#002060; color:white;">
                            <tr>
                                <th style="text-align:center;">S#</th>
                                <th style="text-align:center;">Emp ID</th>
                                <th style="text-align:center;">Name</th>
                                <th style="text-align:center;">Department</th>
                                <th style="text-align:center;">Base Salary</th>
                                <th style="text-align:center;">Gender</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rows || '<tr><td colspan="6" style="text-align:center;padding:20px;">No records</td></tr>'}
                        </tbody>
                    </table>
                `);

                dialog.show();
            }
        });
    };

    ensure_chartjs_loaded(function() {
        load_experience_chart();
        load_salary_chart();
    });



    window.load_att_request_table = function(request_type) {

        $('.att-req-btn').css({ background: '#e5e7eb', color: '#374151' });

        const btnMap = {
            "Permission":              "#btn-permission",
            "Miss Punch":              "#btn-misspunch",
            "On Duty Working Day":     "#btn-onduty",
            "Comp Off On Duty Holiday":"#btn-compoff-od",
            "Comp Off Present Holiday":"#btn-compoff-ph"
        };
        $(btnMap[request_type]).css({ background: '#0F1568', color: 'white' });

        $('#att-req-table').html(`<div style="text-align:center; padding:20px;">Loading...</div>`);

        frappe.call({
            method: "teampro.teampro.page.hr_and_admin.hr_and_admin.get_attendance_requests",
            args: { request_type: request_type },
            callback: function(r) {
                const data = r.message || [];

                let headers = "";
                let rows = "";

                if (request_type === "Permission") {
                    headers = `
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:30px;">S#</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:80px;">Emp ID</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:120px;">Name</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:100px;">Dept</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:80px;">Date</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:80px;">Session</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:90px;">Evening Time</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:80px;">Total Time</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:200px;">Explanation</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;width:70px;">Approver</th>
                    `;
                    rows = data.map((row, i) => {
                        let bg = i % 2 === 0 ? "#ffffff" : "#e7e6ec";
                        return `
                            <tr style="background:${bg};">
                                <td style="text-align:center;padding:7px;">${i + 1}</td>
                                <td style="text-align:center;padding:7px;">${row.employee || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.employee_name || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.department || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.from_date ? frappe.datetime.str_to_user(row.from_date) : '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.custom_permission_session || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.custom_evening_time || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.custom_total_time || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.explanation || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.approver_code || '-'}</td>
                            </tr>
                        `;
                    }).join('');

                } else if (request_type === "Miss Punch") {
                    // ✅ Miss Punch — separate table
                    headers = `
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">S#</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Emp ID</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:left;padding:8px;">Name</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:left;padding:8px;">Dept</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Date</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:left;padding:8px;">Explanation</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Approver</th>
                    `;
                    rows = data.map((row, i) => {
                        let bg = i % 2 === 0 ? "#ffffff" : "#e7e6ec";
                        return `
                            <tr style="background:${bg};">
                                <td style="text-align:center;padding:7px;">${i + 1}</td>
                                <td style="text-align:center;padding:7px;">${row.employee || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.employee_name || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.department || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.from_date ? frappe.datetime.str_to_user(row.from_date) : '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.explanation || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.approver_code || '-'}</td>
                            </tr>
                        `;
                    }).join('');

                } else {
                    // ✅ On Duty / Comp Off — same table format
                    headers = `
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">S#</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Emp ID</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:left;padding:8px;">Name</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:left;padding:8px;">Dept</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">From Date</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">To Date</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Total Days</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Half Day</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Session</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:left;padding:8px;">Explanation</th>
                        <th style="position:sticky;top:0;background:#0F1568;color:white;text-align:center;padding:8px;">Approver</th>
                    `;
                    rows = data.map((row, i) => {
                        let bg = i % 2 === 0 ? "#ffffff" : "#e7e6ec";
                        return `
                            <tr style="background:${bg};">
                                <td style="text-align:center;padding:7px;">${i + 1}</td>
                                <td style="text-align:center;padding:7px;">${row.employee || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.employee_name || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.department || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.from_date ? frappe.datetime.str_to_user(row.from_date) : '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.to_date ? frappe.datetime.str_to_user(row.to_date) : '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.total_days || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.half_day ? "Yes" : "No"}</td>
                                <td style="text-align:center;padding:7px;">${row.custom_session || '-'}</td>
                                <td style="text-align:left;padding:7px;">${row.explanation || '-'}</td>
                                <td style="text-align:center;padding:7px;">${row.approver_code || '-'}</td>
                            </tr>
                        `;
                    }).join('');
                }

                const colspan = request_type === "Permission" ? 10 : request_type === "Miss Punch" ? 7 : 11;

                $('#att-req-table').html(`
                    <table class="table table-bordered" style="margin-bottom:0; width:100%; border-collapse:collapse;">
                        <thead><tr>${headers}</tr></thead>
                        <tbody>
                            ${rows || `<tr><td colspan="${colspan}" style="text-align:center;padding:20px;">No records found</td></tr>`}
                        </tbody>
                    </table>
                `);
            }
        });
    }

load_att_request_table('Permission');

};



