frappe.pages['issue-live-status-re'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});
	const formattedDate = new Date().toLocaleDateString('en-GB', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric'
	});
	let html = `
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th colspan="7" style="background: #4c3b69; color: white; text-align: center;">Issue Details</th>
                    <th colspan="2" style="background: #4c3b69; color: white; text-align: right;">Date</th>
					<th colspan="1" style="background: #4c3b69; color: white; text-align: right;">${formattedDate}</th>
                </tr>
                <!-- Table Column Headers -->
                <tr>
                    <th>#</th>
                    <th>Project</th>
                    <th>Project Type</th>
                    <th>CR</th>
                    <th>Hold</th>
                    <th>Open</th>
                    <th>Overdue</th>
                    <th>PR</th>
                    <th>Working</th>
                    <th>Grand Total</th>
                </tr>
            </thead>
            <tbody id="report-table">
                <tr>
                    <td colspan="10">Loading...</td>
                </tr>
            </tbody>
        </table>
    `;
	addCustomStyles();
    $(html).appendTo(page.body);
    fetch_report_data();
}
function fetch_report_data() {
    frappe.call({
        method: "teampro.teampro.page.issue_live_status_re.issue_live_status_re.issue_live_report",
        callback: function(r) {
            if (r.message) {
                render_report_table(r.message);  // Ensure function exists
            }
        },
        error: function(err) {
            console.error("Error fetching report data:", err);
        }
    });
}

function render_report_table(data) {
	addCustomStyles();
    let table_body = $("#report-table");
    table_body.empty();

    if (data.length === 0) {
        table_body.append('<tr><td colspan="10">No data available</td></tr>');
        return;
    }

    // Initialize total counters
    let total_cr = 0, total_hold = 0, total_open = 0, total_overdue = 0;
    let total_pr = 0, total_working = 0, grand_total = 0;

    data.forEach((row, index) => {
        // Convert values to numbers, defaulting to 0 if they are missing
        let cr = row.client_review ? parseInt(row.client_review) : 0;
        let hold = row.hold ? parseInt(row.hold) : 0;
        let open = row.open ? parseInt(row.open) : 0;
        let overdue = row.overdue ? parseInt(row.overdue) : 0;
        let pr = row.pending_review ? parseInt(row.pending_review) : 0;
        let working = row.working ? parseInt(row.working) : 0;
        let total = row.total ? parseInt(row.total) : 0;

        // Update totals
        total_cr += cr;
        total_hold += hold;
        total_open += open;
        total_overdue += overdue;
        total_pr += pr;
        total_working += working;
        grand_total += total;

        // Append row to table
        let table_row = `
            <tr>
                <td>${index + 1}</td>
                <td>${row.project_name}</td>
                <td>${row.type}</td>
                <td>${cr > 0 ? cr : '-'}</td>
                <td>${hold > 0 ? hold : '-'}</td>
                <td>${open > 0 ? open : '-'}</td>
                <td>${overdue > 0 ? overdue : '-'}</td>
                <td>${pr > 0 ? pr : '-'}</td>
                <td>${working > 0 ? working : '-'}</td>
                <td>${total > 0 ? total : '-'}</td>
            </tr>
        `;
        table_body.append(table_row);
    });

    // Append the Grand Total row at the end
    let total_row = `
        <tr style="background: #f4b400; font-weight: bold;">
            <td colspan="3" style="text-align: center;">Grand Total</td>
            <td>${total_cr}</td>
            <td>${total_hold}</td>
            <td>${total_open}</td>
            <td>${total_overdue}</td>
            <td>${total_pr}</td>
            <td>${total_working}</td>
            <td>${grand_total}</td>
        </tr>
    `;
    table_body.append(total_row);
}
// setInterval(function () {
//     location.reload();
// }, 5000);
function addCustomStyles() {
    let style = document.createElement("style");
    style.innerHTML = `
        table {
            width: 100%;
            border-collapse: collapse; /* Ensures proper border rendering */
        }
        table, th, td {
            border: 2px solid black !important; /* Stronger enforcement */
        }
        th, td {
            padding: 8px;
            text-align: center;
        }
        thead th {
            background: #4c3b69;
            color: white;
        }
        tfoot tr {
            background: #f4b400;
            font-weight: bold;
        }
    `;
    
    // Remove any previous styles to avoid duplication
    let existingStyle = document.querySelector("#custom-table-styles");
    if (existingStyle) {
        existingStyle.remove();
    }

    // Set an ID to prevent duplicate styles
    style.id = "custom-table-styles";
    document.head.appendChild(style);
}
