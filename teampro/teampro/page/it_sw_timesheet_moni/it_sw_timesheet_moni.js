frappe.pages['it-sw-timesheet-moni'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'IT-SW Timesheet Monitor',
        single_column: true
    });
    const filters = {
    production_date: frappe.datetime.get_today(),
    dev_team: '',
    allocated_to: ''
};
fetch_timesheet_data(filters);

let $headerContainer = $('<div class="form-group d-flex justify-content-between align-items-end mb-3" style="gap: 20px;">')
    .appendTo(page.main);

// Left: Filters section
let $filtersSection = $('<div class="d-flex" style="gap: 15px; flex-wrap: wrap;">').appendTo($headerContainer);

// Right: Buttons section
let $buttonsSection = $('<div class="d-flex" style="gap: 10px;">').appendTo($headerContainer);


    // Filters
    // Filters go to the left
let production_date = frappe.ui.form.make_control({
    df: {
        fieldtype: 'Date',
        label: 'Production Date',
        fieldname: 'production_date',
        placeholder: 'Select Date'
    },
    parent: $filtersSection,
    render_input: true
});
production_date.set_value(frappe.datetime.get_today());

let dev_team = frappe.ui.form.make_control({
    df: {
        fieldtype: 'Link',
        label: 'Dev Team',
        options: 'Dev Team',
        fieldname: 'dev_team',
        placeholder: 'Select a Dev Team'
    },
    parent: $filtersSection,
    render_input: true
});

let allocated_to = frappe.ui.form.make_control({
    df: {
        fieldtype: 'Link',
        label: 'Allocated To',
        options: 'User',
        fieldname: 'allocated_to',
        placeholder: 'Select a CB'
    },
    parent: $filtersSection,
    render_input: true
});

frappe.db.get_list("Employee", {
    filters: { department: "IT. Development - THIS" },
    fields: ["user_id"]
}).then(userList => {
    const allowedUsers = userList.map(u => u.user_id);

    allocated_to.df.get_query = () => {
        return {
            filters: {
                name: ["in", allowedUsers]
            }
        };
    };
});





    // Buttons
    let applyBtn = $(`
    <button class="btn btn-primary" title="Apply Filters">
        <i class="fa fa-filter"></i> Filter
    </button>
`).appendTo($buttonsSection);

let clearBtn = $(`
    <button class="btn btn-secondary" title="Clear Filters" style="font-size: 18px;">
        &#x2715;
    </button>
`).appendTo($buttonsSection);


    // Table container
    let $container = $('<div class="mt-4">').appendTo(page.main);

    // Fetch data on apply
    applyBtn.on("click", function () {
        const filters = {
            production_date: production_date.get_value(),
            dev_team: dev_team.get_value(),
            allocated_to: allocated_to.get_value()
        };
        fetch_timesheet_data(filters, $container);
    });

    // Clear filters
    clearBtn.on("click", function () {
        dev_team.set_value("");
        allocated_to.set_value("");
        $container.empty();
        fetch_timesheet_data(filters, $container);
    });
// 	production_date.$input.on("change", function () {
//     const filters = {
//         production_date: production_date.get_value(),
//         dev_team: dev_team.get_value(),
//         allocated_to: allocated_to.get_value()
//     };
//     fetch_timesheet_data(filters);
// });
// setInterval(() => {
//     console.log('Refreshing Timesheet Monitor.')
//     frappe.show_alert({ message: 'Refreshing Timesheet Monitor...', indicator: 'blue' });
//     const filters = {
//     production_date: frappe.datetime.get_today(),
//     dev_team: '',
//     allocated_to: ''
// };
//     fetch_timesheet_data(filters);
// }, 300000);



function fetch_timesheet_data(filters) {
    frappe.call({
        method: "teampro.teampro.page.it_sw_timesheet_moni.it_sw_timesheet_moni.get_data",
        args: { args: filters },
        callback: function (r) {
            if (r.message && Array.isArray(r.message)) {
                let data = r.message;

                let html = `
<style>
    .scrollable-table-container {
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #ccc;
    }

    table {
        width: 100%;
        border-collapse: collapse !important;
    }

    table, th, td {
        border: 1px solid black !important;
    }

    thead th {
        background-color: #0F1568 !important;
        color: white !important;
        text-align: center;
        font-size: 16px;
        padding: 10px;
        position: sticky;
        top: 0;
        z-index: 2;
    }

    td {
        padding: 8px;
        text-align: center;
        font-size: 16px;
    }

    .left-align {
        text-align: left !important;
        vertical-align: middle !important;
    }
</style>
<div class="scrollable-table-container">
<table>

                        <thead>
                            <tr>
                                <th>Sl No</th>
                                <th>Task ID</th>
                                <th>Project</th>
                                <th>Subject</th>
                                <th>CB</th>
                                <th>Status</th>
                                <th>Expected Time</th>
                                <th>RT</th>
                                <th>Actual Time</th>
                                <th>Today RT</th>
                                <th>Today AT</th>
                                <th>Priority</th>
                                <th>Spot Task</th>
                                <th>Current Status</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                let serial = 1;

                // Step 1: Group data by Dev Team -> CB
                let groupedByDevTeam = {};
                data.forEach(row => {
                    let dev_team = row[12] || "Unknown Team";
                    let cb = row[3] || "Unknown CB";
                    if (!groupedByDevTeam[dev_team]) {
                        groupedByDevTeam[dev_team] = {};
                    }
                    if (!groupedByDevTeam[dev_team][cb]) {
                        groupedByDevTeam[dev_team][cb] = [];
                    }
                    groupedByDevTeam[dev_team][cb].push(row);
                });

                // Step 2: Loop through Dev Teams
 
                for (let dev_team in groupedByDevTeam) {
                    let dev_et = 0, dev_rt = 0, dev_at = 0,dev_today_at=0,dev_today_rt =0;
                    let total_tasks = 0;

                    // First, calculate Dev Team totals
                    for (let cb in groupedByDevTeam[dev_team]) {
                        groupedByDevTeam[dev_team][cb].forEach(row => {
                            const expected = row[5] || 0;
                            const rt = row[6] || 0;
                            const at = row[7] || 0;
							const today_rt = row[14] || 0;
                            const today_at = row[13] || 0;

                            dev_et += expected;
                            dev_rt += rt;
                            dev_at += at;
							dev_today_rt += today_rt;
                            dev_today_at += today_at;
                            total_tasks += 1;
                        });
                    }

                    // Dev Team row (aligned with table columns)
                    html += `
                        <tr style="background-color:#add8e6; font-weight:bold;">
                            <td colspan="6" style="text-align:left;">${dev_team}</td>
                            <td style="text-align:right;">${dev_et}</td>
                            <td style="text-align:right;">${dev_rt}</td>
                            <td style="text-align:right;">${dev_at.toFixed(2)}</td>
                            <td style="text-align:right;">${dev_today_rt}</td>
                            <td style="text-align:right;color:red;">${dev_today_at.toFixed(2)}</td>
                            <td colspan="3"></td>
                        </tr>
                    `;

                    // Step 3: Loop through CBs under each Dev Team
                    for (let cb in groupedByDevTeam[dev_team]) {
                        let cb_et = 0, cb_rt = 0, cb_at = 0,cb_today_rt =0,cb_today_at =0;

                        groupedByDevTeam[dev_team][cb].forEach(row => {
                            const expected = row[5] || 0;
                            const rt = row[6] || 0;
                            const at = row[7] || 0;
							const today_rt = row[14] || 0;
                            const today_at = row[13] || 0;

                            cb_et += expected;
                            cb_rt += rt;
                            cb_at += at;
							cb_today_rt +=today_rt;
							cb_today_at +=today_at;
                            // <td><a href="/app/task/${row[0]}" target="_blank">${row[0]}</a></td>

                            html += `
                                <tr>
                                    <td>${serial++}</td>
                                    <td>${row[0]}</td>
                                    <td style="text-align:left;">${row[1]}</td>
                                    <td style="text-align:left;">${row[2]}</td>
                                    <td>${row[3]}</td>
                                    <td>${row[4]}</td>
                                    <td style="text-align:right;">${expected}</td>
                                    <td style="text-align:right;">${rt}</td>
                                    <td style="text-align:right;">${at}</td>
                                    <td style="text-align:right;">${today_rt}</td>
                                    <td style="text-align:right;color:red;">${today_at}</td>
                                    <td>${row[8]}</td>
                                    <td>${row[9]}</td>
                                    <td>${row[10]}</td>
                                </tr>
                            `;
                        });

                        html += `
                            <tr style="font-weight:bold; background-color:#f2f2f2;">
                                <td colspan="6" style="text-align:right;">Total for ${cb}</td>
                                <td style="text-align:right;">${cb_et}</td>
                                <td style="text-align:right;">${cb_rt}</td>
                                <td style="text-align:right;">${cb_at.toFixed(2)}</td>
                                <td style="text-align:right;">${cb_today_rt}</td>
                                <td style="text-align:right;color:red;">${cb_today_at.toFixed(2)}</td>
                                <td colspan="3"></td>
                            </tr>
                        `;
                    }
                }
                html += `</tbody></table></div>`;
                $container.html(html);
            } else {
                $container.html("<p>No data found.</p>");
            }
        }
    });
}




    


};


