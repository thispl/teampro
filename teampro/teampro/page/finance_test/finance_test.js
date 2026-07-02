frappe.pages['finance-test'].on_page_load = function (wrapper) {
    frappe.require([
        "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.25/jspdf.plugin.autotable.min.js"

    ]);
    // ---- NON-ALLOCATED: current active view tracker ----
    let currentNonAllocatedView = "overall";

    
    $(document).off("click", ".toggle-btn").on("click", ".toggle-btn", function () {
        $(".toggle-btn").removeClass("active");
        $(this).addClass("active");
        currentNonAllocatedView = $(this).data("view");
        loadNonAllocatedTable();
    });
    // KT filter change
    $(document).off("change", "#kt_confirmed_filter").on("change", "#kt_confirmed_filter", function () {
    loadNonAllocatedTable();   // same function, view stays as currentNonAllocatedView
});
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'IT-SW Dashboard',
        single_column: true
    });
    const style = document.createElement('style');
    style.innerHTML = `
    
    .top-actions { display: flex; gap: 10px; justify-content: flex-end; align-items: center; margin-top: -40px; margin-right: 20px; }
    .dashboard-cards-finaince { display: flex; gap: 25px; flex-wrap: nowrap; overflow-x: auto; padding-bottom: 20px; }
    .dashboard-card { width: 190px; border-radius: 12px; padding: 10px; text-align: center; flex-shrink: 0; }
    .card-inner { background-color: white; padding: 20px 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .card-inner h3 { margin: 0; font-size: 17px; font-weight: bold; color: #222; text-align: center; white-space: normal; }
    .card-inner .amount { font-size: 20px; font-weight: bold; color: green; margin-top: 10px; text-align: center; }
    .card-inner .avg { font-size: 13px; font-weight: bold; color: red; margin-top: 10px; text-align: center; }
    .dashboard-card:hover { transform: scale(1.02); transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important; cursor: pointer; }
    .sticky-top { position: sticky; top: 0; z-index: 10; }
    @keyframes cardPop { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.05); opacity: 0.8; } 100% { transform: scale(1); opacity: 1; } }
    .pop-blink { animation: cardPop 0.3s ease-in-out !important; }
	@keyframes blink-border {
    0%   { border-color: rgb(151, 158, 153); }
    50%  { border-color: transparent; }
    100% { border-color: rgb(151, 158, 153); }
  }

  .blink-border {
    animation: blink-border 2s infinite;
  }
    .dashboard-cards { display: flex; gap: 20px; flex-wrap: wrap; }
    .card h3, .card h5 { font-weight: 600; }
    .table thead th { background-color: #0F1568; color: white; }
    .shadow-sm { box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075); }
	.retro-table-wrapper {
    overflow-x: auto;
    margin-top: 20px;
  }
  .retro-table-wrapper table {
    min-width: 1200px;
    width: 100%;
  }
	#filter-row .control-input-wrapper {
  margin-right: 15
   px;
  margin-top: 20px;
  margin-bottom: 60px;
  margin-left: 60px;
  min-width: 150px;
}



.filter-box{

    background:#fff3e0;       /* mild orange */
    border:2px solid #8e24aa; /* violet border */
    color:#4a148c;
    padding:6px 14px;
    border-radius:20px;       /* round shape */
    font-size:13px;
    outline:none;
    cursor:pointer;
}

.filter-box:hover{

    border-color:#6a1b9a;

}
    #non_allocated_task_table_new table thead {
    background-color: #0F1568;
    color: white;
}

 #amc_table table thead {
    background-color: #0F1568;
    color: white;
}
 
.toggle-btn {
    padding: 4px 12px;
    border: 1px solid #ddd;
    background: #fff;
    cursor: pointer;
    font-size: 12px;
    border-radius: 4px;
    color: #333;
    transition: background 0.2s, color 0.2s, border-color 0.2s;
}

.toggle-btn:hover {
    background: #e8f5e9;
    border-color: #021750;
    color: #021750;
}

.toggle-btn.active {
    background: #021750;   /* green fill */
    color: white;
    border-color: #021750;
    font-weight: bold;
}
.na-view-btn {
    padding: 4px 12px;
    border: 1px solid #ddd;
    background: #fff;
    cursor: pointer;
    font-size: 12px;
    border-radius: 4px;
    color: #333;
    transition: background 0.2s, color 0.2s, border-color 0.2s;
}

.na-view-btn:hover {
    background: #e8f5e9;
    border-color: #021750;
    color: #021750;
}

.na-view-btn.active {
    background: #021750;
    color: white;
    border-color: #021750;
    font-weight: bold;
}
.top-actions-date {
    padding: 8px;           /* optional spacing */
    border-radius: 4px;     /* optional rounded corners */
}




  `;

    document.head.appendChild(style);

    $(wrapper).html(`
    <div class="dashboard-wrapper" style="padding: 0 30px;">
      <div style="position: relative; padding: 10px;">
        <h2 style="text-align: center; font-weight: bold; margin: 0;">IT SERVICES</h2>
		
        <div id="current-datetime" style="font-size: 16px; color: #666; text-align: center; margin-top: 5px;"></div>
		
        
		
      </div>

      
      <div id="dashboard-summary-row" 
        style="display:flex; gap:20px; margin-top:40px; background:#f5f5f5;">

        <!-- LEFT SIDE -->
        <div style="display:flex; flex-direction:column; gap:20px; flex:1;">

            <!-- PROJECT -->
            <div id="project-summary-container"
                style="border:1px solid #2ac1db;border-radius:8px;padding:10px;background:#f5f5f5;">
                <div id="project-summary-wrapper"></div>
            </div>

            <!-- TASK -->
            <div id="task-summary-container"
                style="border:1px solid #2ac1db;border-radius:8px;padding:10px;background:#f5f5f5;">
                <div id="task-summary-wrapper"></div>
            </div>

        </div>

        <!-- RIGHT SIDE -->
        <div id="pivot-project-summary-container"
            style="flex:1;border:1px solid #2ac1db;border-radius:8px;padding:10px;
                    max-height:500px;overflow-y:auto;background:#f5f5f5;">
            <div id="pivot-summary-table-content"></div>
        </div>

    </div>
<br>
<div class="card-container equal-height"
    style="
        margin-right:20px;
        background:#f5f5f5;
        border:1px solid #ddd;
        border-radius:8px;
        padding:8px;
    ">

    <!-- WHITE HEADER BOX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:20px;
        background:white;
        border-radius:8px;
        height:50px;
        padding:0 15px;
        flex-wrap:nowrap;
        overflow-x:auto;
        white-space:nowrap;
    ">

        <!-- LEFT : TITLE -->
        <h4 style="
            margin:0;
            display:flex;
            align-items:center;
            height:100%;
            flex-shrink:0;
        ">
            PRODUCTION SUMMARY
        </h4>

        <!-- CENTER : FILTERS -->
        <div style="
            display:flex;
            align-items:center;
            gap:15px;
            justify-content:center;
            flex:1;
            flex-wrap:nowrap;
            white-space:nowrap;
            min-width:max-content;
            height:100%;
        ">

            <!-- + ALL -->
            <span id="open-all-teams-btn-1"
                style="
                    cursor:pointer;
                    font-weight:bold;
                    flex-shrink:0;
                ">
                + ALL
            </span>

            <!-- Priority -->
            <div style="
                display:flex;
                gap:8px;
                align-items:center;
                flex-shrink:0;
            ">
                <span style="color:green; font-weight:bold;">Priority :</span>
                <span class="filter-btn" data-group="priority" data-filter="Low">Low</span>
                <span class="filter-btn" data-group="priority" data-filter="Medium">Medium</span>
                <span class="filter-btn" data-group="priority" data-filter="High">High</span>
                <span class="filter-btn" data-group="priority" data-filter="Critical">Urgent</span>
            </div>

            <!-- SP -->
            <div style="
                display:flex;
                gap:8px;
                align-items:center;
                flex-shrink:0;
            ">
                <span style="color:green; font-weight:bold;">S/P :</span>
                <span class="filter-btn" data-group="sp" data-filter="S">Spot</span>
                <span class="filter-btn" data-group="sp" data-filter="P">Plan</span>
            </div>

            <!-- RO -->
            <div style="
                display:flex;
                gap:8px;
                align-items:center;
                flex-shrink:0;
            ">
                <span style="color:green; font-weight:bold;">RO :</span>
                <span class="filter-btn" data-group="ro" data-filter="RO">Reopen</span>
            </div>

            <!-- CF -->
            <div style="
                display:flex;
                gap:8px;
                align-items:center;
                flex-shrink:0;
            ">
                <span style="color:green; font-weight:bold;">CF :</span>
                <span class="filter-btn" data-group="cf" data-filter="CF">Carry Forward</span>
            </div>

        </div>

        <!-- RIGHT : DATE -->
        <div style="
            display:flex;
            gap:10px;
            align-items:center;
            height:100%;
            flex-shrink:0;
        ">
            <div class="top-actions-date"></div>
            <div class="top-actions-date1"></div>
        </div>
        

    </div>
    

    <!-- TABLE -->
    <div id="today-task-table-container1"
        class="table-scrollable"
        style="margin-top:10px;">
        Loading...
    </div>

</div>


  <div class="card-container equal-height" style="margin-top:40px; margin-right:0px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
  <div style="margin: 5; padding: 5px 5px; text-align: center; background: white; position: relative;border-radius:8px;">
  <h4 style="margin: 0;">PRODUCTION TABLE</h4>
     <div style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); display: flex; gap: 10px; background: #f5f5f5; padding: 5px; border-radius: 4px;">
    <button id="download-task-table-all"
            style="border: none; color: black; cursor: pointer;">
      ALL
    </button>
    <button 
    id="download-task-table"
    style="border:none;background:none;outline:none;padding:0;cursor:pointer;">
    <img 
        src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
        style="width:16px;height:16px;">
    </button>
    <button id="download-task-table-pdf" style="border: none; color: black; cursor: pointer;">Download PDF</button>
  </div>
 
  </div>
   <br>
    

        <div id="today-task-table-container" class="table-scrollable">Loading...</div>
        </div>



        
    //start

    <div class="card-container equal-height" style="margin-top:40px; margin-right:0px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
    <div style="position: relative; background: white; padding: 10px; border-radius: 6px;">
    
   <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: nowrap; gap: 10px;">

    <!-- LEFT: empty spacer to balance the right side -->
    <div style="flex:1;"></div>

    <!-- CENTER: Title -->
    <h4 style="margin: 0; white-space: nowrap; flex:1; text-align:center;">NON-ALLOCATED TOTAL</h4>

    <!-- RIGHT: Toggle Buttons + KT Filter + Download -->
    <div style="display: flex; align-items: center; gap: 8px; flex-wrap: nowrap; flex:1; justify-content:flex-end;">

        <!-- Toggle Buttons -->
            <button class="toggle-btn active" data-view="overall">Overall</button>
            <button class="toggle-btn" data-view="sprint">NA</button>

        <select id="kt_confirmed_filter" style="width:110px; height:28px;">
            <option value="">KT Confirm</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
        </select>

        <button id="download-non-allocated" style="border:none; background:none; outline:none; padding:0; cursor:pointer; display:flex; align-items:center;">
            <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png" style="width:22px; height:22px;">
        </button>

    </div>
</div>
</div>

    <br>
    <!-- Single container — content swaps based on active view -->
    <div id="non_allocated_task_table_new" class="table-scrollable">Loading Overall...</div>
</div>

//end

    
    <div class="card-container equal-height" style="margin-top:40px; margin-right:0px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
        <div style="position: relative; background: white; padding: 10px; border-radius: 6px; text-align: center;">
    <h4 style="margin: 0;">NON-ALLOCATED TASKS IN LIVE SPRINT</h4>



    <button
        id="download-non-allocated_in_spr"
        style="
            border:none;
            background:none;
            outline:none;
            padding:0;
            cursor:pointer;
            position:absolute;
            right:10px;
            top:50%;
            transform:translateY(-50%);
        "
    >
        <img
            src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
            style="width:22px;height:22px;"
        >
    </button>
</div>

        <br>
        
        <div id="non_allocated_task_in_spr" class="table-scrollable">Loading...</div>
    </div>

    <div class="card-container equal-height" style="margin-top:40px; margin-right:0px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
        <div style="position: relative; background: white; padding: 10px; border-radius: 6px; text-align: center;">
            <h4 style="margin: 0;">AMC PROJECTS</h4>
           <button 
    id="download-amc"
    style="
        border:none;
        background:none;
        outline:none;
        padding:0;
        cursor:pointer;
        position:absolute;
        right:10px;
        top:50%;
        transform:translateY(-50%);
    "
>
    <img 
        src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
        style="width:22px;height:22px;"
    >
</button>
    </div>

        <br>
        <div id="amc_table" class="table-scrollable">Loading...</div>
    </div>

    <div class="card-container equal-height" 
        style="margin-top:40px; margin-right:0px; background:#f5f5f5; border:1px solid #ddd; border-radius:8px; padding:10px;">

        <div style="position:relative;background:white;padding:10px;border-radius:6px;display:flex;align-items:center;justify-content:center;">

            <!-- Center Heading -->
            <h4 style="margin:0;font-weight:600;">DSR SUMMARY</h4>

            <!-- Right Side Date -->
            <div style="position:absolute;right:100px;min-width:180px;">
                <div id="dsr_date_filter"></div>
                
            </div>
            <button 
    id="download-dsr"
    style="
        border:none;
        background:none;
        outline:none;
        padding:0;
        cursor:pointer;
        position:absolute;
        right:10px;
        top:50%;
        transform:translateY(-50%);
    "
>
    <img 
        src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
        style="width:22px;height:22px;"
    >
</button>

        </div>

        <br>

        <div id="dsr_table" class="table-scrollable">
            Loading...
        </div>

    </div>


    <div class="card-container equal-height" style="margin-top:40px; margin-right:0px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;display: none;">
        <div style="position: relative; background: white; padding: 10px; border-radius: 6px; text-align: center;">
            <h4 style="margin: 0;">OPPORTUNITY TABLE</h4>

    </div>

        <br>
        <div id="opp_table" class="table-scrollable">Loading...</div>
    </div>

	  <div id ="filters" style="margin-top: -20px;"></div><br>
      <div id="retro-summary-html" style="overflow-x:auto;overflow-y:auto; margin-top: -30px; margin-left: -30px; margin-right: -30px;"></div>
    </div>
  `);


    get_today_task_data1();
    // load_opportunity_table();
    loadDashboardData();

    get_today_task_data11();
    load_amc_project_sla_table();
    load_dsr_table();

    // setInterval(function () {
    //     get_today_task_data1();
    // }, 300000);

    // setInterval(function () {
    //     get_today_task_data11();
    // }, 300000);


    // ---- Create Frappe Date Controls ----
    let from_date_filter = frappe.ui.form.make_control({
        parent: $('.top-actions-date'),
        df: { fieldtype: "Date", fieldname: "from_date", placeholder: "From Date" },
        render_input: true
    });

    let to_date_filter = frappe.ui.form.make_control({
        parent: $('.top-actions-date1'),
        df: { fieldtype: "Date", fieldname: "to_date", placeholder: "To Date" },
        render_input: true
    });
    to_date_filter.$wrapper.hide();

    // ---- Function to fetch data ----
    function load_dashboard_data(from_date, to_date) {
        get_today_task_data11(from_date, to_date);
        get_today_task_data1(from_date, to_date);
    }

    function loadNonAllocatedTable() {
    const view = currentNonAllocatedView;           // "overall" | "na" | "sprint"
    const kt_confirmed = $("#kt_confirmed_filter").val(); // "" | "Yes" | "No"

    $("#non_allocated_task_table_new").html(`
        <div style="padding:20px; text-align:center;">Loading...</div>
    `);

    frappe.call({
        method: "teampro.teampro.page.new_it_dashboard.new_it.get_non_allocated_tasks_test",
        args: {
            view: view,           // pass to backend
            kt_confirmed: kt_confirmed
        },
        callback: function (r) {
            let $container = $("#non_allocated_task_table_new");

            if (!(r.message && r.message.data && r.message.data.length)) {
                $container.html("<p style='padding:20px;text-align:center;'>No tasks found.</p>");
                return;
            }

            const tasks = r.message.data;

            // Group by project
            grouped = {};
            tasks.forEach(task => {
                const project = task.project || "No Project";
                if (!grouped[project]) grouped[project] = [];
                grouped[project].push(task);
            });

            // Build table
            let grandET = 0, grandRT = 0, grandAT = 0;

            let html = `
            <table class="table table-bordered" style="width:100%; text-align:center; border-collapse:collapse;">
                <thead style="background:#0F1568; color:white;">
                    <tr>
                        <th id="toggle-all-na" style="cursor:pointer;">+ ALL</th>
                        <th>Sprint</th>
                        <th>Task</th>
                        <th>Subject</th>
                        <th>ET</th>
                        <th>RT</th>
                        <th>AT</th>
                        <th>AGE</th>
                        <th>CF</th>
                        <th>Priority</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>`;

            Object.keys(grouped).sort().forEach(project => {
                const projectTasks = grouped[project];
                const projectRowId = "proj-" + project.replace(/[^a-zA-Z0-9]/g, "_");

                const totalET = projectTasks.reduce((s, t) => s + (parseFloat(t.expected_time) || 0), 0);
                const totalRT = projectTasks.reduce((s, t) => s + (parseFloat(t.rt) || 0), 0);
                const totalAT = projectTasks.reduce((s, t) => s + (parseFloat(t.actual_time) || 0), 0);

                grandET += totalET;
                grandRT += totalRT;
                grandAT += totalAT;

                // Project header row
                html += `
                <tr class="na-project-row" data-target="${projectRowId}"
                    style="cursor:pointer; font-weight:bold; background:#85819e; color:#fff;">
                    <td colspan="4" style="text-align:left; padding-left:10px;">
                        <span class="na-toggle-sign">+</span> ${project}
                    </td>
                    <td>${totalET.toFixed(2)}</td>
                    <td>${totalRT.toFixed(2)}</td>
                    <td>${totalAT.toFixed(2)}</td>
                    <td colspan="4"></td>
                </tr>`;

                // Task rows
                projectTasks.forEach((task, idx) => {
                    const bg = idx % 2 === 0 ? "#ffffff" : "#e7e6ec";
                    const age = parseFloat(task.custom_age) || 0;
                    const textColor = age > 3 ? "#f54545" : "#000000";

                    html += `
                    <tr class="na-task-row" data-parent="${projectRowId}"
                        style="display:none; background:${bg}; color:${textColor};">
                        <td>${task.cb || ""}</td>
                        <td>${task.custom_sprint || ""}</td>
                        <td>
                            <a href="/app/task/${task.name}" target="_blank"
                               style="color:inherit; text-decoration:none;">
                                ${task.name}
                            </a>
                        </td>
                        <td style="text-align:left;">${task.subject || ""}</td>
                        <td>${parseFloat(task.expected_time || 0).toFixed(2)}</td>
                        <td>${parseFloat(task.rt || 0).toFixed(2)}</td>
                        <td>${parseFloat(task.actual_time || 0).toFixed(2)}</td>
                        <td>${task.custom_age || ""}</td>
                        <td>${task.custom_production_date_count || ""}</td>
                        <td>${task.priority || ""}</td>
                        <td>${task.status || ""}</td>
                    </tr>`;
                });
            });

            // Grand total row
            html += `
            <tr style="font-weight:bold; background:#0F1568; color:white;">
                <td colspan="4" style="text-align:right;">GRAND TOTAL</td>
                <td>${grandET.toFixed(2)}</td>
                <td>${grandRT.toFixed(2)}</td>
                <td>${grandAT.toFixed(2)}</td>
                <td colspan="4"></td>
            </tr>`;

            html += `</tbody></table>`;
            $container.html(html);

            // ---- Bind toggle events ----
            let allExpanded = false;

            $("#toggle-all-na").off("click").on("click", function () {
                allExpanded = !allExpanded;
                $(".na-task-row").toggle(allExpanded);
                $(".na-toggle-sign").text(allExpanded ? "-" : "+");
                $(this).text(allExpanded ? "- ALL" : "+ ALL");
            });

            $(".na-project-row").off("click").on("click", function () {
                const target = $(this).data("target");
                const $rows = $(`.na-task-row[data-parent="${target}"]`);
                const $sign = $(this).find(".na-toggle-sign");
                const isVisible = $rows.is(":visible");
                $rows.toggle(!isVisible);
                $sign.text(isVisible ? "+" : "-");
            });
        }
    });
}

// Initial load
loadNonAllocatedTable();

    // // From Date change handler
    from_date_filter.$input.on('change', function () {
        const selectedDate = from_date_filter.get_value();
        to_date_filter.set_value(selectedDate);

        // Show full-page overlay like Apply button
        if ($('#fetching-overlay').length === 0) {
            $('body').append(`
            <div id="fetching-overlay" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
                font-size: 24px;
                font-weight: bold;
            ">
                Fetching Data...
            </div>
        `);
        } else {
            $('#fetching-overlay').show();
        }

        // Show overlay
        $('#fetching-overlay').show();

        // Run immediately
        loadOrderBooking(selectedDate, selectedDate);
        loadturnover(selectedDate, selectedDate);
        loadtcollection(selectedDate, selectedDate);
        get_today_task_data11(selectedDate, selectedDate);
        get_today_task_data1(selectedDate, selectedDate);
        load_dashboard_data(selectedDate, selectedDate);

        // Hide overlay after 20 sec (optional)
        setTimeout(function () {
            $('#fetching-overlay').hide();
        }, 20000);
    });





    $(document).ready(function () {
        const today = frappe.datetime.get_today();
        from_date_filter.set_value(today);
        to_date_filter.set_value(today);
        load_dashboard_data(today, today);
    });


    $(document).ready(function () {
        const today = frappe.datetime.get_today();

        // Set both dates to today initially
        $('#tfp-from-date').val(today);
        $('#tfp-to-date').val(today);

        // Load tasks for today
        get_today_task_data11(today, today);
        get_today_task_data1(today, today);


        // When the From Date changes, set To Date to the same value
        $('#tfp-from-date').on('change', function () {
            const selectedDate = $(this).val();
            $('#tfp-to-date').val(selectedDate);

            // Optionally, reload tasks for the selected date
            get_today_task_data11(selectedDate, selectedDate);
            get_today_task_data1(selectedDate, selectedDate);
        });
    });



    // load_retro_summary_html(sprint=null);
    load_retro_summary(sprint = null);
    // load_retro_summary(sprint);
    // load_retro_summary(sprint=null);


    let $filtersSection = $('#filters');

    // Combined container with Sprint filter + Dev Team buttons
    $filtersSection.html(`
    <div id="filter-container" class="row align-items-center flex-wrap gap-3 mb-3 p-3 rounded"
         style="background: #f5f5f5; border:1px solid #dee2e6; margin-left: 0px; margin-right:0px;">
        <div id="sprint-filter-wrapper" class="d-flex align-items-center me-3" style="min-width: 220px; "></div>
        <div id="filter-row" class="d-flex flex-wrap align-items-center gap-2" ></div>
    </div>
`);
    $(document).on('click', '#download-task-table', function () {
        const table = document.getElementById('task-report-table');
        if (!table) {
            frappe.msgprint("No Data found.");
            return;
        }

        // Show hidden rows temporarily for export
        const hiddenRows = $(table).find('tr:hidden');
        hiddenRows.show();

        // Style the table headers
        $(table).find('thead th').each(function () {
            $(this).css({
                'background-color': '#0F1568',
                'color': 'white',
                'text-align': 'center',
                'font-size': '14px',
                'border': '1px solid black'
            });
        });

        // Style the body rows
        $(table).find('tbody tr').each(function () {
            const $row = $(this);

            // Retain row-level styling up to column M
            const isTeamRow = $row.hasClass('toggle-team');
            const isCBRow = $row.hasClass('toggle-cb');

            $row.find('td').each(function (index) {
                let backgroundColor = '#ffffff'; // default white

                if (index <= 13) {
                    if (isTeamRow) {
                        backgroundColor = '#eaf0f6';
                    } else if (isCBRow) {
                        backgroundColor = '#f2f2f2';
                    }
                }

                // For column E (index 4), replace <a> with plain text to avoid underline
                if (index === 4 && !isCBRow && !isTeamRow) {
                    const anchor = $(this).find('a');
                    if (anchor.length) {
                        const text = anchor.text();
                        $(this).html(text);  // Replace anchor with plain text
                    }
                }

                $(this).css({
                    'background-color': backgroundColor,
                    'border': '1px solid black',
                    'font-size': '12px',
                    'text-align': $(this).hasClass('left-align') ? 'left' : 'center'
                });
            });



        });

        // Create Excel-compatible HTML
        const html = `
        <html xmlns:o="urn:schemas-microsoft-com:office:office" 
              xmlns:x="urn:schemas-microsoft-com:office:excel" 
              xmlns="http://www.w3.org/TR/REC-html40">
        <head>
            <!--[if gte mso 9]>
            <xml>
                <x:ExcelWorkbook>
                    <x:ExcelWorksheets>
                        <x:ExcelWorksheet>
                            <x:Name>Production Tasks</x:Name>
                            <x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions>
                        </x:ExcelWorksheet>
                    </x:ExcelWorksheets>
                </x:ExcelWorkbook>
            </xml>
            <![endif]-->
        </head>
        <body>
            ${table.outerHTML}
        </body>
        </html>`;

        const blob = new Blob([html], {
            type: "application/vnd.ms-excel"
        });

        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Production_Tasks_${frappe.datetime.now_date()}.xls`;
        a.click(); // Trigger download
        URL.revokeObjectURL(url); // Clean up

        // Re-hide previously hidden rows
        hiddenRows.hide();
    });

    // PDF Download
    // $(document).on('click', '#download-task-table-pdf', function () {
    //     const table = document.getElementById('task-report-table');
    //     if (!table) {
    //         frappe.msgprint("No Data found.");
    //         return;
    //     }

    //     // Show hidden rows temporarily
    //     const hiddenRows = $(table).find('tr:hidden');
    //     hiddenRows.show();

    //     // Extract headers
    //     const headers = [];
    //     $(table).find('thead th').each(function () {
    //         headers.push($(this).text().trim());
    //     });

    //     // Extract rows
    //     const data = [];
    //     $(table).find('tbody tr').each(function () {
    //         const rowData = [];
    //         $(this).find('td').each(function () {
    //             let cellText = $(this).text().trim();

    //             // If there's an anchor tag, get its text
    //             const anchor = $(this).find('a');
    //             if (anchor.length) {
    //                 cellText = anchor.text().trim();
    //             }

    //             rowData.push(cellText);
    //         });
    //         data.push(rowData);
    //     });

    //     // Create PDF
    //     const { jsPDF } = window.jspdf;
    //     const doc = new jsPDF('l', 'pt', 'a4'); // landscape

    //     doc.text("Production Task Report", 40, 30);
    //     doc.autoTable({
    //         head: [headers],
    //         body: data,
    //         startY: 50,
    //         styles: {
    //             fontSize: 8,
    //             cellPadding: 3,
    //         },
    //         headStyles: {
    //             fillColor: [15, 21, 104], // #0F1568
    //             textColor: 255,
    //             halign: 'center'
    //         },
    //         bodyStyles: {
    //             halign: 'center'
    //         }
    //     });

    //     doc.save(`Production_Tasks_${frappe.datetime.now_date()}.pdf`);

    //     // Re-hide previously hidden rows
    //     hiddenRows.hide();
    // });
    // $(document).on('click', '#download-task-table-pdf', function () {
    //     const table = document.getElementById('task-report-table');
    //     if (!table) {
    //         frappe.msgprint("No Data found.");
    //         return;
    //     }

    //     // Show hidden rows temporarily
    //     const hiddenRows = $(table).find('tr:hidden');
    //     hiddenRows.show();

    //     const { jsPDF } = window.jspdf;
    //     const doc = new jsPDF('l', 'pt', 'a4'); // Landscape mode

    //     const rows = [];
    //     let headers = [];

    //     // Extract table header
    //     $(table).find('thead tr').each(function () {
    //         const headerRow = [];
    //         $(this).find('th').each(function () {
    //             headerRow.push($(this).text().trim());
    //         });
    //         if (headerRow.length) headers = headerRow;
    //     });

    //     // Extract body rows
    //     $(table).find('tbody tr').each(function () {
    //         const $tr = $(this);
    //         const $tds = $tr.find('td');

    //         // Handle group row
    //         const isGroupRow = $tds.length === 1 && $tds.attr('colspan');
    //         if (isGroupRow) {
    //             const colspan = parseInt($tds.attr('colspan')) || headers.length;
    //             const text = $tds.text().trim();

    //             rows.push({
    //                 content: [
    //                     {
    //                         content: text,
    //                         colSpan: colspan,
    //                         styles: {
    //                             fillColor: [245, 245, 245],
    //                             fontStyle: 'bold',
    //                             halign: 'left'
    //                         }
    //                     }
    //                 ]
    //             });
    //         } else {
    //             // Regular row
    //             const rowData = [];
    //             $tds.each(function () {
    //                 let text = $(this).text().trim();
    //                 const anchor = $(this).find('a');
    //                 if (anchor.length) text = anchor.text().trim();
    //                 rowData.push({ content: text });
    //             });
    //             rows.push({ content: rowData });
    //         }
    //     });

    //     // Add title
    //     doc.setFontSize(12);
    //     doc.text("Production Task Report", 40, 30);

    //     // Generate table
    //     doc.autoTable({
    //         head: [headers],
    //         body: rows.map(row => row.content),
    //         startY: 50,
    //         styles: {
    //             fontSize: 8,
    //             cellPadding: 4,
    //             valign: 'middle'
    //         },
    //         headStyles: {
    //             fillColor: [15, 21, 104],
    //             textColor: 255,
    //             halign: 'center'
    //         },
    //         bodyStyles: {
    //             halign: 'center'
    //         },
    //         didParseCell: function (data) {
    //             const row = rows[data.row.index];
    //             if (row && row.content && row.content[0] && row.content[0].styles) {
    //                 Object.assign(data.cell.styles, row.content[0].styles);
    //             }
    //         }
    //     });

    //     // Save PDF
    //     doc.save(`Production_Tasks_${frappe.datetime.now_date()}.pdf`);

    //     // Re-hide rows
    //     hiddenRows.hide();
    // });
    $(document).on('click', '#download-task-table-pdf', function () {
        const doctype = "Task";
        const docname = "TS12590";
        const print_format = "Task Monitor";
        const no_letterhead = 0;

        const url = frappe.urllib.get_full_url(
            `/api/method/frappe.utils.print_format.download_pdf?doctype=${encodeURIComponent(doctype)}`
            + `&name=${encodeURIComponent(docname)}`
            + `&format=${encodeURIComponent(print_format)}`
            + `&no_letterhead=${no_letterhead}`
            + `&trigger_print=1`
        );

        window.open(url);
    });


    $(document)
    .off("click", "#download-task-table-all")
    .on("click", "#download-task-table-all", function () {

        const table = document.getElementById('task-report-table');
        if (!table) {
            frappe.msgprint("No Data found.");
            return;
        }

        let btn = $(this);

        let rows3 = $("#today-task-table-container")
            .find(".toggle-cb, .task-row");

        if (rows3.is(":visible")) {
            rows3.hide();
            btn.text("+ ALL");
        } else {
            rows3.show();
            btn.text("- ALL");
        }

    });


    function add_filter(df) {
        const control = frappe.ui.form.make_control({
            df: Object.assign({
                reqd: 0,
                onchange: function () {
                    // load_retro_summary_html(control.get_value());
                    load_retro_summary(control.get_value());
                }
            }, df),
            parent: $('#sprint-filter-wrapper'),
            render_input: true
        });
        return control;
    }

    // Add Sprint Filter
    let sprint_filter = add_filter({
        fieldtype: 'Link',
        options: 'Task Sprint',
        fieldname: 'sprint',
        placeholder: 'Sprint',
        in_standard_filter: true
    });

    // Set default Sprint value
    frappe.call({
        method: "teampro.teampro.page.new_it_dashboard.new_it.update_sprint_filter",
        callback: function (r) {
            if (r && r.message) {
                sprint_filter.set_value(r.message);
            }
        }
    });

    // Style
    $(`<style>
    #filter-container {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 10px 5px;
        margin-top: 40px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        
    }

    #sprint-filter-wrapper .control-input-wrapper {
        max-width: 250px;
    }

    #filter-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
       
    }
    
  .card-container.equal-height {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    padding: 20px;
    max-height: 600px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-right: 50px;
    }

.table-scrollable {
  overflow-y: auto;
  width: 100%;
}

.dev-team-button.active {
    background-color: black !important;
    color: white !important;
    border-color: black !important;
    box-shadow: none !important;   
    outline: none !important;    
}


</style>`).appendTo("head");

    // Create Dev Team button
    function createDevTeamButton(name) {
        const $button = $(`<button class="btn btn-outline-primary m-1 dev-team-button" data-team="${name}">${name}</button>`);
        $button.on('click', function () {
            // Remove active class from all buttons first
            $('.dev-team-button').removeClass('active');

            // Add active class to clicked button
            $(this).addClass('active');

            let dev_team = name
            let selected_sprint = sprint_filter.get_value();
            if (dev_team === 'ALL') {
                dev_team = ''
            }
            if (dev_team === 'Summary') {
                load_retro_summary(selected_sprint)
                //   frappe.call({
                //     method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_retro_summary_overall",
                //     args:{
                //         name:selected_sprint
                //     },
                //     callback: function(r) {
                //         if (r.message) {
                //             $('#retro-summary-html').html(r.message);
                //         } else {
                //             $('#retro-summary-html').html("No Data Found");
                //         }
                //     }
                // });
            }
            else
                frappe.call({
                    method: "teampro.teampro.page.new_it_dashboard.new_it.get_retro_summary_html",
                    args: {
                        name: selected_sprint,
                        dev_team: dev_team,
                    },
                    callback: function (r) {
                        const data = r.message || [];
                        $('#retro-summary-html').html('');

                        if (data.length === 0) {
                            $('#retro-summary-html').html(`
                        <div class="team-section" style="padding: 0 30px;">
                            <h4>${dev_team}</h4>
                            <strong>No Data Found in this Sprint</strong>
                        </div>
                    `);
                            return;
                        }
                        data.forEach(section => {
                            $('#retro-summary-html').append(`
                            <div class="team-section" style="padding: 0 30px;">
                                <h4>${section.team}</h4>
                                ${section.html}
                                <br>
                            </div>
                        `);
                        });
                    }
                });
        });
        $('#filter-row').append($button);
    }

    // Add "ALL" first
    createDevTeamButton("Summary")
    createDevTeamButton("ALL");



    // Load other Dev Teams from DB (excluding "Others")
    frappe.db.get_list("Dev Team", {
        filters: { name: ["!=", "Others"] },
        fields: ["name"],
        order_by: 'name'
    }).then(dev_teams => {
        dev_teams.forEach(team => {
            createDevTeamButton(team.name);
        });
    });


    const sprintStyle = document.createElement("style");
    sprintStyle.innerHTML = `
        .frappe-control[data-fieldname="sprint"] .control-input-wrapper {
            background-color:rgb(81, 182, 188) !important;
            border: 2px solid rgb(81, 182, 188) !important;
            border-radius: 10px;
            height: 50px !important;
            font-size: 20px !important;
            font-weight: bold;
            padding: 7px 14px;
            color: #003f5c !important;
            width: 260px !important;
        }

        .frappe-control[data-fieldname="sprint"] label {
            font-weight: bold;
            color: #004080 !important;
        }
    `;
    document.head.appendChild(sprintStyle);




    //  setInterval(() => {
    //     frappe.show_alert({ message: 'Refreshing IT-SW Dashboard...', indicator: 'blue' });
    //     loadDashboardData();
    //     get_today_task_data();
    // 	// load_retro_summary_html(sprint=null);
    //     load_retro_summary(sprint=null);
    //   }, 300000);







    // Clock
    function updateDateTime() {
        const now = new Date();
        const dateStr = now.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        const timeStr = now.toLocaleTimeString();
        document.getElementById('current-datetime').innerHTML = `${dateStr} | ${timeStr}`;
    }
    updateDateTime();
    setInterval(updateDateTime, 1000);






    // Reusable function to render cards
    function renderCard(selector, label, value) {
        const formatted = parseFloat(value).toLocaleString('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        });
        $(wrapper).find(selector).html(`
			<div class="card-inner">
				<h3>${label}</h3>
				<div class="amount">${formatted}</div>
			</div>
		`);
    }
    function renderSimpleCard(selector, label, value, color = 'green') {
        $(wrapper).find(selector).html(`
		<div class="card-inner">
			<h3>${label}</h3>
			<div class="amount" style="color: ${color}">${value}</div>
		</div>
	`);
    }

    // 	function loadOrderBooking(from_date = null, to_date = null) {
    // 	frappe.call({
    // 		method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it",
    // 		args: { from_date, to_date },
    // 		callback: function(r) {
    // 			const value = r.message || 0;
    // 			const formatted = parseFloat(value).toLocaleString('en-IN', {
    // 				style: 'currency',
    // 				currency: 'INR',
    // 				maximumFractionDigits: 0
    // 			});
    // 			$(wrapper).find('.order-booking-card').html(`
    // 				<div class="card-inner">
    // 					<h3>Order Booking</h3>
    // 					<div class="amount">${formatted}</div>
    // 				</div>
    // 			`);
    // 		}
    // 	});
    // }

    function loadOrderBooking(from_date = null, to_date = null) {
        frappe.call({
            method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it",
            args: { from_date, to_date },
            callback: function (r) {
                const value = r.message || 0;
                const now = new Date();
                const currentMonth = now.getMonth() + 1; // 1-12
                const currentYear = now.getFullYear();

                // Calculate current financial month number
                // April (4) is month 1, March (3) is month 12
                let financialMonth;
                if (currentMonth >= 4) {
                    financialMonth = currentMonth - 3;
                } else {
                    financialMonth = currentMonth + 9;
                }
                const avg = value / financialMonth;
                const avg_value = Math.round(avg || 0);
                const formattedtotal = parseFloat(value).toLocaleString('en-IN', {
                    style: 'currency',
                    currency: 'INR',
                    maximumFractionDigits: 0
                });
                const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
                    maximumFractionDigits: 0
                });
                let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
                $(wrapper).find('.order-booking-card').html(`
				<div class="card-inner">
					<h3>Order Booking</h3>
					<div class="amount">${formattedtotal}</div>
<div style="text-align:center; margin-top:5px;">
    <span style="color:red; font-weight:bold; display:block;">[${formattedAvg}]</span>
    <span style="display:inline-block; vertical-align:middle;">${arrowSvg}</span>
</div>

				</div>
			`);
            }
        });
    }

    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it",
        callback: function (r) {
            const value = r.message || 0;
            const now = new Date();
            const currentMonth = now.getMonth() + 1; // 1-12
            const currentYear = now.getFullYear();

            // Calculate current financial month number
            // April (4) is month 1, March (3) is month 12
            let financialMonth;
            if (currentMonth >= 4) {
                financialMonth = currentMonth - 3;
            } else {
                financialMonth = currentMonth + 9;
            }
            const avg = value / financialMonth;
            const avg_value = Math.round(avg || 0);

            const formattedtotal = parseFloat(value).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });

            const formattedAvg = parseFloat(avg_value).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });
            let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;

            $(wrapper).find('.order-booking-card').html(`
				<div class="card-inner">
					<h3>Order Booking</h3>
					<div class="amount">${formattedtotal}</div>
                
                <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);

        }
    });

    function loadturnover(from_date = null, to_date = null) {
        frappe.call({
            method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_turnover_it",
            args: { from_date, to_date },
            callback: function (r) {
                const value = r.message || 0;
                const now = new Date();
                const currentMonth = now.getMonth() + 1; // 1-12
                const currentYear = now.getFullYear();

                // Calculate current financial month number
                // April (4) is month 1, March (3) is month 12
                let financialMonth;
                if (currentMonth >= 4) {
                    financialMonth = currentMonth - 3;
                } else {
                    financialMonth = currentMonth + 9;
                }

                // Calculate average
                const avg = value / financialMonth;
                const avg_value1 = Math.round(avg || 0);
                const formattedtotal1 = parseFloat(value).toLocaleString('en-IN', {
                    style: 'currency',
                    currency: 'INR',
                    maximumFractionDigits: 0
                });
                const formattedAvg1 = parseFloat(avg_value1).toLocaleString('en-IN', {
                    maximumFractionDigits: 0
                });
                let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
                $(wrapper).find('.turnover-card').html(`
				<div class="card-inner">
					<h3>Turnover</h3>
					<div class="amount">${formattedtotal1}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg1}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
                    

			`);
            }
        });
    }

    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_turnover_it",
        callback: function (r) {
            const value = r.message || 0;
            const now = new Date();
            const currentMonth = now.getMonth() + 1; // 1-12
            const currentYear = now.getFullYear();

            // Calculate current financial month number
            // April (4) is month 1, March (3) is month 12
            let financialMonth;
            if (currentMonth >= 4) {
                financialMonth = currentMonth - 3;
            } else {
                financialMonth = currentMonth + 9;
            }

            // Calculate average
            const avg = value / financialMonth;
            const avg_value1 = Math.round(avg || 0);
            const formattedtotal1 = parseFloat(value).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });
            const formattedAvg1 = parseFloat(avg_value1).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });
            let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
            $(wrapper).find('.turnover-card').html(`
				<div class="card-inner">
					<h3>Turnover</h3>
					<div class="amount">${formattedtotal1}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg1}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
                    
			`);
        }
    });
    function loadtcollection(from_date = null, to_date = null) {
        frappe.call({
            method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_collection_value_it",
            args: { from_date, to_date },
            callback: function (r) {
                const value = r.message || 0;
                const now = new Date();
                const currentMonth = now.getMonth() + 1; // 1-12
                const currentYear = now.getFullYear();

                // Calculate current financial month number
                // April (4) is month 1, March (3) is month 12
                let financialMonth;
                if (currentMonth >= 4) {
                    financialMonth = currentMonth - 3;
                } else {
                    financialMonth = currentMonth + 9;
                }

                // Calculate average
                const avg = value / financialMonth;
                const avg_value2 = Math.round(avg || 0);
                const formattedtotal2 = parseFloat(value).toLocaleString('en-IN', {
                    style: 'currency',
                    currency: 'INR',
                    maximumFractionDigits: 0
                });
                const formattedAvg2 = parseFloat(avg_value2).toLocaleString('en-IN', {
                    maximumFractionDigits: 0
                });
                let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
                $(wrapper).find('.collection-card').html(`
				<div class="card-inner">
					<h3>Collection</h3>
					<div class="amount">${formattedtotal2}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg2}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>

			`);
            }
        });
    }

    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_collection_value_it",
        callback: function (r) {
            const value = r.message || 0;
            const now = new Date();
            const currentMonth = now.getMonth() + 1; // 1-12
            const currentYear = now.getFullYear();

            // Calculate current financial month number
            // April (4) is month 1, March (3) is month 12
            let financialMonth;
            if (currentMonth >= 4) {
                financialMonth = currentMonth - 3;
            } else {
                financialMonth = currentMonth + 9;
            }

            // Calculate average
            const avg = value / financialMonth;
            const avg_value2 = Math.round(avg || 0);
            const formattedtotal2 = parseFloat(value).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });
            const formattedAvg2 = parseFloat(avg_value2).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });
            let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
            $(wrapper).find('.collection-card').html(`
				<div class="card-inner">
					<h3>Collection</h3>
					<div class="amount">${formattedtotal2}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg2}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
                  
			`);
        }
    });

    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_receivable",
        callback: function (r) {
            const value = r.message || 0;
            const now = new Date();
            const currentMonth = now.getMonth() + 1; // 1-12
            const currentYear = now.getFullYear();

            // Calculate current financial month number
            // April (4) is month 1, March (3) is month 12
            let financialMonth;
            if (currentMonth >= 4) {
                financialMonth = currentMonth - 3;
            } else {
                financialMonth = currentMonth + 9;
            }

            // Calculate average
            const avg = value / financialMonth;
            const avg_value3 = Math.round(avg || 0);
            const formattedtotal3 = parseFloat(value).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });
            const formattedAvg3 = parseFloat(avg_value3).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });
            let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
            $(wrapper).find('.receivable-card').html(`
				<div class="card-inner">
					<h3>Receivable</h3>
					<div class="amount">${formattedtotal3}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg3}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>

			`);
        }
    });

    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_bill_value",
        callback: function (r) {
            const value = r.message || 0;
            const now = new Date();
            const currentMonth = now.getMonth() + 1; // 1-12
            const currentYear = now.getFullYear();

            // Calculate current financial month number
            // April (4) is month 1, March (3) is month 12
            let financialMonth;
            if (currentMonth >= 4) {
                financialMonth = currentMonth - 3;
            } else {
                financialMonth = currentMonth + 9;
            }

            // Calculate average
            const avg = value / financialMonth;
            const avg_value4 = Math.round(avg || 0);
            const formattedtotal4 = parseFloat(value).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });
            const formattedAvg4 = parseFloat(avg_value4).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });
            let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
            $(wrapper).find('.tobill-card').html(`
				<div class="card-inner">
					<h3>To Bill</h3>
					<div class="amount">${formattedtotal4}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg4}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);
        }
    });

    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_deliver_bill_value",
        callback: function (r) {
            const value = r.message || 0;
            const now = new Date();
            const currentMonth = now.getMonth() + 1; // 1-12
            const currentYear = now.getFullYear();

            // Calculate current financial month number
            // April (4) is month 1, March (3) is month 12
            let financialMonth;
            if (currentMonth >= 4) {
                financialMonth = currentMonth - 3;
            } else {
                financialMonth = currentMonth + 9;
            }

            // Calculate average
            const avg = value / financialMonth;
            const avg_value5 = Math.round(avg || 0);
            const formattedtotal5 = parseFloat(value).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });
            const formattedAvg5 = parseFloat(avg_value5).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });
            let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
            $(wrapper).find('.todeliverbill-card').html(`
				<div class="card-inner">
					<h3>To Deliver and Bill</h3>
					<div class="amount">${formattedtotal5}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg5}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);
        }
    });

    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_payable",
        callback: function (r) {
            const value = r.message || 0;
            const now = new Date();
            const currentMonth = now.getMonth() + 1; // 1-12
            const currentYear = now.getFullYear();

            // Calculate current financial month number
            // April (4) is month 1, March (3) is month 12
            let financialMonth;
            if (currentMonth >= 4) {
                financialMonth = currentMonth - 3;
            } else {
                financialMonth = currentMonth + 9;
            }

            // Calculate average
            const avg = value / financialMonth;
            const avg_value6 = Math.round(avg || 0);
            const formattedtotal6 = parseFloat(value).toLocaleString('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            });
            const formattedAvg6 = parseFloat(avg_value6).toLocaleString('en-IN', {
                maximumFractionDigits: 0
            });
            let arrowSvg = `
<svg width="60" height="20" viewBox="0 0 60 40">
    <path d="M5 30 L20 20 L35 25 L50 10 L55 5" 
          stroke="black" stroke-width="2" fill="none" 
          stroke-linecap="round" stroke-linejoin="round" 
          style="stroke-dasharray: 4,1;" />
    <polygon points="57,10 52,0 58,0" fill="black"/>
</svg>`;
            $(wrapper).find('.payable-card').html(`
				<div class="card-inner">
					<h3>Payable</h3>
					<div class="amount">${formattedtotal6}</div>
                    <div style="font-size: 12px; text-align: center;color:red; margin-top: 5px;font-weight:bold">[${formattedAvg6}]
                </div>
				<div style="font-size: 10px;color:black;text-align: center;font-weight:bold">[Avg]</div>
            </div>
			`);
        }
    });

    function loadDashboardData(from_date = null, to_date = null) {
        const container = $('.dashboard-wrapper');
        renderCardFromMethod('.order-booking-card', 'Order Booking', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_order_booking_it", from_date, to_date);
        renderCardFromMethod('.turnover-card', 'Turnover', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_turnover_it", from_date, to_date);
        renderCardFromMethod('.collection-card', 'Collection', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.get_collection_value_it", from_date, to_date);
        renderCardFromMethod('.receivable-card', 'Receivable', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_receivable");
        renderCardFromMethod('.tobill-card', 'To Bill', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_bill_value");
        renderCardFromMethod('.todeliverbill-card', 'To Deliver and Bill', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_to_deliver_bill_value");
        renderCardFromMethod('.payable-card', 'Payable', "teampro.teampro.page.it_sw_dashboard.it_sw_dashboard.it_payable");

        // Tables
        frappe.call({
            method: 'teampro.teampro.page.new_it_dashboard.new_it.it_receivable_table',
            callback: function (r) {
                $('#receivable-so-table-content').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
            }
        });
        frappe.call({
            method: 'teampro.teampro.page.new_it_dashboard.new_it.it_payable_table',
            callback: function (r) {
                $('#payable-so-table-content').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
            }
        });
        frappe.call({
            method: 'teampro.teampro.page.new_it_dashboard.new_it.it_tobill_table',
            callback: function (r) {
                $('#tobill-so-table-content').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
            }
        });
        // Ensure only one set of summary cards is shown
        if (!container.find('#project-summary-wrapper').length) {
            container.append('<div id="project-summary-wrapper"></div>');
        }
        if (!container.find('#task-summary-wrapper').length) {
            container.append('<div id="task-summary-wrapper"></div>');
        }
        // if (!container.find('#sprint-summary-wrapper').length) {
        // 	container.append('<div id="sprint-summary-wrapper"></div>');
        // }



        Promise.all([
            frappe.call({ method: "teampro.teampro.page.new_it_dashboard.new_it.get_project_counts" }),
            frappe.call({ method: "teampro.teampro.page.new_it_dashboard.new_it.get_task_summary" }),
            frappe.call({ method: "teampro.teampro.page.new_it_dashboard.new_it.get_sprint_counts" })
        ]).then(([projRes, taskRes, sprintRes]) => {
            if (projRes.message) {
                const { projects = [], total = 0 } = projRes.message;

                const projectColors = [
                    "#2F8F46", "#C29100", "#540D6E",
                    "#006D77", "#4169e1", "#8B0000",
                    "#f9844a", "#bc5090", "#003f5c"
                ];

                let html = `
    <style>
        .project-cards-container {
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-top: 10px;
        }

        .project-cards-container table {
            width: 100%;
            border-collapse: collapse;
        }

        .project-cards-container th {
            background-color: white;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
            padding: 10px;
            border-bottom: 20px solid #ccc;
        }

        .project-cards-row {
			display: flex;
			overflow-x: auto;
			padding: 10px;
			gap: 40px;
			justify-content: center;
		}

        .project-card {
            min-width: 120px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
            border: 4px solid;
            border-radius: 10px;
            padding: 10px;
            background: #fff;
        }

        .project-card span {
            font-size: 18px;
            display: block;
            margin-top: 5px;
        }
    </style>

    <div class="project-cards-container">
        <table>
        <br>
            <h4 class="sticky-top" style="margin: 0; padding: 0px 0; text-align:center; background: white;">PROJECT COUNT</h4>
            <br>
        </table>
        <div class="project-cards-row">
            <div class="project-card" style="border-color:#0096A6;">
                Total
                <span>${total}</span>
            </div>`;

                projects.forEach((it, i) => {
                    if (it.project_type === "Products") {
                        return;
                    }
                    html += `
                    <div class="project-card" data-type="${it.project_type}" style="border-color:${projectColors[i % projectColors.length]};">
                        ${it.project_type}
                        <span>${it.count}</span>
                    </div>`;
                });

                html += `
                    </div>
                </div>`;

                container.find('#project-summary-wrapper').html(html);
            }

            container.on('click', '.project-card', function () {

                const type = $(this).data('type');
                console.log("Project clicked:", type);
                if (!type || type === "Total") {
                    renderPivotTable(pivotData);
                    return;
                }

                const filtered = pivotData.filter(r =>
                    r.project_type === type
                );

                renderPivotTable(filtered);
            });


            //  2. Task Summary
            if (taskRes.message) {
                const tc = taskRes.message;
                const taskColors = {
                    total: '#0096A6',
                    open: '#2F8F46',
                    working: '#C29100',
                    pr: '#540D6E',
                    cr: '#006D77'
                };

                let html = `
    <style>
    .task-cards-container {
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-top: 20px;
    }

    .task-cards-container table {
        width: 100%;
        border-collapse: collapse;
    }

    .task-cards-container th {
        background-color: white;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        padding: 10px;
        border-bottom: 1px solid #ccc;
    }

    .task-cards-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        padding: 15px;
        justify-content: flex-start;
        align-items: stretch;
        box-sizing: border-box;
    }

    .task-card {
        min-width: 120px;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        border: 4px solid;
        border-radius: 50px;
        padding: 10px;
        background: #fff;
        flex: 1 1 auto; /* Helps the cards wrap correctly */
        box-sizing: border-box;
        cursor: pointer;
    }

    .task-card span {
        font-size: 18px;
        display: block;
        margin-top: 5px;
    }
</style>


    <div class="task-cards-container">
        <table>
        <br>
            <h4 class="sticky-top" style="margin: 0; padding: 0px 0; text-align:center; background: white;">TASK COUNT</h4>
        <br>
            </table>
        <div class="task-cards-row">`;

                ['total', 'open', 'working', 'pr', 'cr'].forEach(key => {
                    let title = key.toUpperCase();
                    if (key === 'total') title = 'Total';
                    if (key === 'working') title = 'Working';
                    if (key === 'pr') title = 'Internal Review';
                    if (key === 'cr') title = 'Client Review';
                    if (key === 'open') title = 'Open';

                    html += `
    <div class="task-card task-card-${key}" style="border-color:${taskColors[key]};">
        ${title}

        <span style="font-size:12px;">
            ${(tc[`${key}_total_hours`] || 0).toFixed(2)} hr/<br>
            ${tc[key] || 0}
            ${key !== 'open' ? `
                <span style="color:red;font-size:12px;font-weight:bold;">
                ${(tc[`${key}_today_hours`] || 0).toFixed(2)} hr /<br>
                ${tc[`${key}_today_count`] || 0}
                </span>
                ` : ''}
            
        </span>
    </div>`;

                });

                html += `
        </div>
    </div>`;

                container.find('#task-summary-wrapper').html(html);

                ['total', 'open', 'working', 'pr', 'cr'].forEach(key => {
                    container.off('click', `.task-card-${key}`);
                    container.on('click', `.task-card-${key}`, () => {
                        frappe.call({
                            method: "teampro.teampro.page.new_it_dashboard.new_it.get_tasks_project_wise",
                            args: { type: key },
                            callback: (r) => {
                                const rows = r.message || [];
                                let tbl = `<div style="max-height:400px;overflow-y:auto;">
                        <table style="width:100%; border-collapse: collapse; border: 1px solid black;">
                            <thead><tr style="background-color: #0F1568; color: white;">
                                <th style="border: 1px solid black;">Project</th>
                                <th style="border: 1px solid black;">Tasks</th>
                                <th style="border: 1px solid black;">Hours</th>
                                <th style="border: 1px solid black;">SPOC</th>
                            </tr></thead><tbody>`;
                                rows.forEach(p => {
                                    tbl += `<tr>
                            <td style="border: 1px solid black;">${p.project || 'No Project'}</td>
                            <td style="border: 1px solid black;">${p.task_count}</td>
                            <td style="border: 1px solid black;">${(p.total_hours || 0).toFixed(2)}</td>
                            <td style="border: 1px solid black;text-align: left;">${p.spoc || 'No Spoc'}</td>
                        </tr>`;
                                });
                                tbl += `</tbody></table></div>`;

                                let title = '';
                                if (key == 'open') title = 'Open';
                                else if (key == 'total') title = 'Total';
                                else if (key == 'working') title = 'Working';
                                else if (key == 'pr') title = 'Internal Review';
                                else if (key == 'cr') title = 'Client Review';

                                new frappe.ui.Dialog({
                                    title: `${title}`,
                                    fields: [{ fieldname: "html_table", fieldtype: "HTML", options: tbl }]
                                }).show();
                            }
                        });
                    });
                });
            }


        });


    }



    function renderCardFromMethod(selector, label, method, from_date = null, to_date = null) {
        frappe.call({
            method: method,
            args: from_date && to_date ? { from_date, to_date } : {},
            callback: function (r) {
                const value = r.message || 0;
                const formatted = parseFloat(value).toLocaleString('en-IN', {
                    style: 'currency',
                    currency: 'INR',
                    maximumFractionDigits: 0
                });
                $(selector).html(`
				<div class="card-inner">
					<h3>${label}</h3>
					<div class="amount">${formatted}</div>
				</div>
			`);
            }
        });
    }


    function get_today_task_data11(from_date = null, to_date = null) {

        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.get_today_task_data11",
            args: {
                from_date: from_date,
                to_date: to_date
            },
            callback: function (r) {

                let $container = $("#today-task-table-container1");

                if (!(r.message && r.message.data)) {
                    $container.html("<p>No data found.</p>");
                    return;
                }

                const data = r.message.data;
                const team_order = r.message.team_order;
                const active_data = data.filter(row => row[3]);

                // -------------------------
                // GROUPING
                // -------------------------
                const grouped = {};

                active_data.forEach(row => {
                    const team = row[12] || "No Team";
                    const cb = row[3] || "No CB";   // âœ… ADD THIS

                    const team_safe = team.replace(/\s+/g, '_');
                    const cb_safe = cb.replace(/\s+/g, '_');

                    const cb_id = `cb-${team_safe}-${cb_safe}`;

                    if (!grouped[team]) grouped[team] = {};
                    if (!grouped[team][cb]) grouped[team][cb] = [];

                    grouped[team][cb].push(row);
                });

                // -------------------------
                // SORT TEAMS
                // -------------------------
                const sorted_teams = team_order.filter(team => grouped[team]);

                // -------------------------
                // HTML + CSS
                // -------------------------
                let html = `
<style>
.team-table {
    border-collapse: collapse;
    margin: auto;
    table-layout: auto;
}

/*  REMOVE ALL BORDERS */
.team-table td {
    border: none !important;
    text-align: center;
    padding: 6px 8px;
    font-size: 12px;
    min-width: 90px;   /*  Increase width â†’ no hiding */
}

/* LABEL COLUMN */
.label-cell {
    font-weight: bold;
    min-width: 70px;
   
}

/* CB IMAGE */
.cb-img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 2px solid #d9e3f0;
    object-fit: cover;
}

/* ðŸŽ¨ COLORS */
.aph-val {
    color: #1aa84b;
    font-weight: bold;
}

.rt-val {
    color: #007bff;
    font-weight: bold;
}

.ut-val {
    color: #e74c3c;
    font-weight: bold;
}

/* TOTAL ROW */
.total-row {
    background: #d4d2d2;        /* row background */
    font-weight: bold;
    color: #030303;
    text-align: center;
    padding: 6px 12px;          /* more horizontal padding for rounded look */
    
    border: 1px solid #b0b0b0; /* lighter border */
    border-radius: 12px;        /* rounded corners */
    
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1); /* subtle shadow for depth */
}

.team-box {
    flex: 1;
    border: none !important;   /*  REMOVE BORDER */
    border-radius: 10px;
    background: #fff;
    overflow-x: visible;
}

.team-header {
    text-align: center;
    padding: 6px;
    background: #0F1568;
}

/* THIS IS THE FIX */
.team-header img {
    width: 35px;
    height: 35px;
    object-fit: contain;
}

.team-header div {
    font-size: 13px;
    margin-top: 4px;
}

.three-table-wrapper {
    display: flex;
    flex-direction: row;   /*  IMPORTANT */
    gap: 15px;
    overflow-x: hidden;      /* scroll if needed */
}

/* Wrapper */
.team-row-wrapper {
    display: flex;
    gap: 15px;
}


.team-row-wrapper {
    display: flex;
    gap: 10px;   /* keep small gap */
    width: max-content;
}

/*  MAIN FIX */
.team-box {
    box-sizing: border-box;
}

/* 50% */
.team-box:first-child {
    flex: 0 0 42%;
}

/* 25% + 25% */
.team-box:nth-child(2),
.team-box:nth-child(3) {
    flex: 0 0 28%;
}

.team-box {
    background: #fff;
    border-radius: 8px;
    padding: 5px;
}

.filter-btn{
    padding:2px 6px;
    font-size:12px;
    border-radius:4px;
    border:0.5px solid #d0d7de;
}

/* hover */
.filter-btn:hover{
    background:#e0e7ff;
    border-color:#0F1568;
}

/* active (selected) */
.filter-btn.active{
    background:#0F1568;
    color:#fff;
    border-color:#0F1568;
}

.filter-btn{
    margin-right:4px;
}

</style>




`;

                html += `
<div style="
    background:#dfe7f5;
    padding:10px;
    margin-bottom:10px;
    border-radius:8px;
    display:flex;
    align-items:center;
    gap:10px;
    flex-wrap:wrap;
    display:none;
">

    <!-- + ALL BUTTON -->
    <span id="open-all-teams-btn-1"
        style="cursor:pointer; font-weight:bold;">
        + ALL
    </span>

    <!-- FILTER BOX -->
    <div style="
        display:flex;
        align-items:center;
        gap:20px;
        background:#f1f3f6;
        padding:6px 10px;
        border-radius:8px;
        flex-wrap:wrap;
        
    ">

        <!-- Priority -->
        <div style="display:flex; gap:8px;">
            <span style="color:green; font-weight:bold;">Priority :</span>
            <span class="filter-btn" data-group="priority" data-filter="Low">Low</span>
            <span class="filter-btn" data-group="priority" data-filter="Medium">Medium</span>
            <span class="filter-btn" data-group="priority" data-filter="High">High</span>
            <span class="filter-btn" data-group="priority" data-filter="Critical">Urgent</span>
        </div>

        <!-- SP -->
        <div style="display:flex; gap:8px;">
            <span style="color:green; font-weight:bold;">S/P :</span>
            <span class="filter-btn" data-group="sp" data-filter="S">Spot</span>
            <span class="filter-btn" data-group="sp" data-filter="P">Plan</span>
        </div>

        <!-- RO -->
        <div style="display:flex; gap:8px;">
            <span style="color:green; font-weight:bold;">RO :</span>
            <span class="filter-btn" data-group="ro" data-filter="RO">Reopen</span>
        </div>

        <!-- CF -->
        <div style="display:flex; gap:8px;">
            <span style="color:green; font-weight:bold;">CF :</span>
            <span class="filter-btn" data-group="cf" data-filter="CF">Carry Forward</span>
        </div>

        <!-- % -->
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="color:green; font-weight:bold;">Time % :</span>
                <span class="filter-btn" data-group="ts" data-filter="blue">Blue</span>
                <span class="filter-btn" data-group="ts" data-filter="orange">Orange</span>
                <span class="filter-btn" data-group="ts" data-filter="red">Red</span>
            </div>

    </div>

</div>
`;


                // -------------------------
                // SPLIT INTO 3
                // -------------------------
                for (let i = 0; i < sorted_teams.length; i += 3) {

                    const chunk = sorted_teams.slice(i, i + 3);

                    html += `<div class="team-row-wrapper">`;

                    chunk.forEach((team) => {

                        const cb_groups = grouped[team];

                        //  SORT CB BASED ON ORDER (index 25)
                        const sorted_cbs = Object.entries(cb_groups).sort((a, b) => {
                            const a_order = a[1][0][25] || 0;
                            const b_order = b[1][0][25] || 0;
                            return a_order - b_order;
                        });

                        const first_task = sorted_cbs[0][1][0];
                        const team_logo = first_task[19] || "/assets/frappe/images/ui/avatar.png";

                        const team_id = `team-${team.replace(/\s+/g, '_')}`;

                        let cb_row = ``;
                        // let aph_row = `<td class="label-cell">APH</td>`;
                        // let rt_row = `<td class="label-cell">RT</td>`;
                        // let ut_row = `<td class="label-cell">UT</td>`;
                        // let value_row = `<td class="label-cell">APH / RT / UT / UT%</td>`;
                        let value_row = ``;

                        let total_aph = 0;
                        let total_rt = 0;
                        let total_ut = 0;

                        sorted_cbs.forEach(([cb, rows]) => {

                            const team_safe = team.replace(/\s+/g, '_');
                            const cb_safe = cb.replace(/\s+/g, '_');
                            const cb_id = `cb-${team_safe}-${cb_safe}`;

                            const task = rows[0];

                            const aph = task[24] || 0;
                            const rt = task[14] || 0;
                            const ut = task[13] || 0;

                            let ut_percent = 0;
                            if (aph > 0) {
                                ut_percent = (ut / aph) * 100;
                            }

                            const cb_img = task[18] || "/assets/frappe/images/ui/avatar.png";

                            total_aph += aph;
                            total_rt += rt;
                            total_ut += ut;

                            //  CB IMAGE INSTEAD OF TEXT
                            cb_row += `
                        <td>
                            <img src="${cb_img}" 
                                class="cb-img cb-click"
                                data-cb="${cb_id}"
                                style="cursor:pointer;">
                        </td>`;

                            // aph_row += `<td class="aph-val">${aph.toFixed(2)}</td>`;
                            // rt_row += `<td class="rt-val">${rt.toFixed(2)}</td>`;
                            // ut_row += `<td class="ut-val">${ut.toFixed(2)}</td>`;
                            // value_row += `
                            // <td style="white-space: nowrap;">
                            //     <span class="aph-val">${aph.toFixed(2)}</span>/<span class="rt-val">${rt.toFixed(2)}</span>/<span class="ut-val">${ut.toFixed(2)}</span>/<span class="utp-val">${ut_percent.toFixed(1)}%</span>
                            // </td>`;

                            value_row += `
                            <td style="white-space: nowrap; line-height:16px;">
                                <div>
                                    <span class="aph-val">${aph.toFixed(2)}</span> /
                                    <span class="rt-val">${rt.toFixed(2)}</span>
                                </div>
                                <div>
                                    <span class="ut-val">${ut.toFixed(2)}</span> /
                                    <span class="utp-val">${ut_percent.toFixed(1)}%</span>
                                </div>
                            </td>`;
                        });
                        let total_utp = 0;

                        if (total_aph > 0) {
                            total_utp = (total_ut / total_aph) * 100;
                        }

                        html += `
<div class="team-box">

    <div class="team-header team-click" 
    data-team="${team_id}"
    style="
        display: flex; 
        align-items: center; 
        justify-content: flex-start; 
        gap: 10px; 
        cursor:pointer; 
        position:relative;
        padding: 6px 10px;
    ">

    <!-- LEFT SIDE -->
    <img src="${team_logo}" style="height:40px; width:40px;">

    <b style="color:white;">${team}</b>

    <!-- RIGHT SIDE (TOTAL - no layout break) -->
        <div style="
        margin-left: auto;   /* ðŸ”¥ push to right */
        font-size: 12px;
        font-weight: bold;
        color: white;
        text-align: right;
        white-space: nowrap;   /* ðŸ”¥ keep in one line */
    ">

        APH: <span class="aph-val">${total_aph.toFixed(2)}</span> |
        RT: <span class="rt-val">${total_rt.toFixed(2)}</span> |
        UT: <span class="ut-val">${total_ut.toFixed(2)}</span> |
        UT%: <span class="utp-val">${total_utp.toFixed(1)}%</span>

    </div>
    </div>
    <table class="team-table">
        <tr class="team-row ${team_id}">${cb_row}</tr>
        <tr class="team-row ${team_id}">${value_row}</tr>

       
    </table>
  

</div>`;
                    });

                    html += `</div>`;
                }

                html += `</div>`;

                $container.html(html);
            }
        });

        $("#today-task-table-container1")
            .off("click", ".team-click")
            .on("click", ".team-click", function () {

                const teamId = $(this).data("team");

                toggleTeamRows(teamId, this);

            });

    }

    function toggleTeamRows(teamId) {

        const $rows = $("#today-task-table-container").find("." + teamId);

        if ($rows.is(":visible")) {
            $rows.hide();
        } else {
            $rows.show();
        }
    }

    $(document)
        .off("click", ".cb-click")
        .on("click", ".cb-click", function () {

            const cbId = $(this).data("cb");

            toggleCBRowsFromOutside(cbId);

        });


    $(document).ready(function () {

        setTimeout(function () {

            $("#today-task-table-container")
                .find(".toggle-cb, .task-row")
                .css("display", "table-row"); // important for table rows

            $("#open-all-teams-btn-1").text("- ALL");
            $("#download-task-table-all").text("- ALL");

        }, 500); // adjust 300–1000ms if needed


        $(document)
            .off("click", "#open-all-teams-btn-1")
            .on("click", "#open-all-teams-btn-1", function () {

                let btn = $(this);

                let rows2 = $("#today-task-table-container")
                    .find(".toggle-cb, .task-row");

                if (rows2.is(":visible")) {
                    rows2.hide();
                    btn.text("+ ALL");
                } else {
                    rows2.show();
                    btn.text("- ALL");
                }

            });

    });

    frappe.after_ajax(function () {
        $("#today-task-table-container")
            .find(".toggle-cb, .task-row")
            .css("display", "table-row");

        $("#open-all-teams-btn-1").text("- ALL");
    });


    // function get_today_task_data1(from_date=null, to_date=null) {
    //     let priority = $("#filter-priority").val();
    //     let sp = $("#filter-sp").val();
    //     let ro = $("#filter-ro").val();
    //     frappe.call({
    //         method: "teampro.teampro.page.new_it_dashboard.new_it.get_today_task_data1",
    //         args: {
    //             priority: priority,
    //             sp: sp,
    //             ro: ro,
    //             from_date : from_date,
    //             to_date : to_date
    //         },
    //         callback: function (r) {
    //             let $container = $("#today-task-table-container");

    //             if (r.message && r.message.data) {

    //                 // const data = r.message;

    //                 const data = r.message.data;
    //                 const team_order = r.message.team_order;
    //                 const active_data = data.filter(row => row[3]);

    //                 let total_et = 0;
    //                 let total_rt = 0;
    //                 let total_at = 0;
    //                 let total_today_rt = 0;
    //                 let total_at_period = 0;

    //                 active_data.forEach(row => {
    //                     total_et += parseFloat(row[5]) || 0;
    //                     total_rt += parseFloat(row[6]) || 0;
    //                     total_at += parseFloat(row[7]) || 0;
    //                     total_today_rt += parseFloat(row[14]) || 0;
    //                     total_at_period += parseFloat(row[13]) || 0;
    //                 });

    //                 let html = `
    // <style>
    // .scrollable-table-container {
    //     max-height: 600px;
    //     overflow-y: auto;
    //     border: 1px solid #ccc;
    //     margin-bottom: 10px;
    // }
    // .export-buttons {
    //     margin-bottom: 10px;
    //     text-align: right;
    // }
    // .export-buttons button {
    //     margin-left: 5px;
    // }
    // #task-report-table {
    //     width:100%;
    //     border-collapse:collapse !important;
    //     table-layout:fixed;
    // }


    // .total-row td {
    //     border: 1px solid black !important;
    // }

    // #task-report-table th,
    // #task-report-table td {
    //     border: 1px solid black;
    //     text-align: center;
    //     padding: 8px;
    //     font-size: 14px;
    // }

    // #task-report-table thead th {
    //     background-color: #0F1568;
    //     color: white;
    //     font-size: 16px;
    //     padding: 10px;
    //     position: sticky;
    //     top: 0;
    //     z-index: 2;
    // }

    // thead th {
    //     background-color: #0F1568 !important;
    //     color: white !important;
    //     text-align: center;
    //     font-size: 16px;
    //     padding: 10px;
    //     position: sticky;
    //     top: 0;
    //     z-index: 2;
    // }
    // td {
    //     padding: 8px;
    //     text-align: center;
    //     font-size: 14px;
    // }
    // .left-align {
    //     text-align: left !important;
    // }

    // .toggle-team {
    //     cursor: pointer;
    //     font-weight: bold;
    //     background-color: #eaf0f6;
    // }
    // .toggle-cb {
    //     cursor: pointer;
    //     font-weight: bold;
    //     background-color: #85819e;
    //     color: white;
    // }

    // .cb-circle{
    //     display:inline-flex;
    //     flex-direction:column;
    //     align-items:center;
    // }

    // .cb-circle img{
    //     width:32px;
    //     height:32px;
    //     border-radius:50%;
    //     border:2px solid #d9e3f0;
    //     object-fit:cover;
    // }



    // .cb-code{
    //     font-size:11px;
    //     margin-top:2px;
    //     font-weight:600;
    // }

    // .team-logo img{
    //     width:45px;
    //     height:45px;
    //     border-radius:8px;
    //     border:2px solid #d9e3f0;
    //     padding:3px;
    //     background:white;
    // }

    // .task-row:nth-child(odd){
    //     background-color: #ffffff;   /* white */
    //     color: #000000;  
    // }

    // .task-row:nth-child(even){
    //     background-color: #eaf0f6;   /* light mild blue */
    //     color: #000000;
    // }

    // .all-team-btn{
    //     background:#0F1568;
    //     color:white;
    //     border:none;
    //     padding:3px 9px;
    //     font-size:14px;
    //     border-radius:6px;
    //     cursor:pointer;
    //     transition:all 0.2s ease;
    // }

    // .all-team-btn:hover{
    //     transform:scale(1.15);
    //     background:#1b238f;
    // }

    // .nav-all-btn{
    //     background:#fff3e0;        /* mild inside color */
    //     color:#e65100;             /* text color */
    //     border:2px solid #ff6f00;  /* strong border */
    //     padding:12px 32px; 
    //     font-size:14px;
    //     border-radius:14px;
    //     cursor:pointer;
    //     margin-right:12px;
    //     margin-left:12px;
    //     font-weight:600;
    //     transition:all 0.25s ease;
    // }

    // .nav-all-btn:hover{
    //     background:#ffe0b2;        /* hover mild */
    //     border-color:#e65100;      /* border darker */
    //     transform:scale(1.15);
    // }

    // .progress-wrapper{
    //     position:relative;
    //     width:100%;
    //     background:#eee;
    //     border-radius:10px;
    //     height:22px;
    //     overflow:hidden;
    //     border:0.5px solid black;
    // }

    // .progress-bar{
    //     height:100%;
    // }

    // .progress-text{
    //     position:absolute;
    //     top:0;
    //     left:0;
    //     width:100%;
    //     height:100%;
    //     display:flex;
    //     align-items:center;
    //     justify-content:center;
    //     font-size:12px;
    //     font-weight:bold;
    //     pointer-events:none;
    // }


    // .hover-text{
    //     display:none;
    // }

    // .progress-wrapper:hover .default-text{
    //     display:none;
    // }

    // .progress-wrapper:hover .hover-text{
    //     display:flex;
    // }

    // .filter-btn{
    //     padding:2px 6px;
    //     font-size:12px;
    //     border-radius:4px;
    //     border:0.5px solid #d0d7de;
    // }

    // /* hover */
    // .filter-btn:hover{
    //     background:#e0e7ff;
    //     border-color:#0F1568;
    // }

    // /* active (selected) */
    // .filter-btn.active{
    //     background:#0F1568;
    //     color:#fff;
    //     border-color:#0F1568;
    // }

    // .filter-btn{
    //     margin-right:4px;
    // }

    // .task-row a{
    //     color: inherit;
    //     text-decoration: none;
    // }

    // .progress-wrapper{
    //     position:relative;
    //     height:22px;
    //     background:#eee;
    //     border-radius:12px;
    //     overflow:hidden;
    // }
    // .progress-bar{
    //     height:100%;
    // }
    // .progress-text{
    //     position:absolute;
    //     width:100%;
    //     text-align:center;
    //     font-size:12px;
    //     top:0;
    // }
    // .status-icon{
    //     display:inline-flex;
    //     align-items:center;
    //     justify-content:center;
    //     width:28px;
    //     height:28px;
    //     border-radius:50%;
    //     font-size:14px;
    //     font-weight:bold;
    //     cursor:pointer;
    //     transition:all 0.2s ease;

    //     border:1.5px solid transparent;  
    // }

    // .tick-icon{
    //     background:#e3f2fd;
    //     color:#0d47a1;
    //     border-color:#90caf9;   /* mild blue border */
    // }

    // .tick-icon:hover{
    //     background:#bbdefb;
    //     border-color:#64b5f6;   /* little stronger on hover */
    //     transform:scale(1.3);
    // }

    // .c-icon{
    //     background:#ffebee;
    //     color:#b71c1c;
    //     border-color:#ef9a9a;   /* mild red border */
    // }

    // .c-icon:hover{
    //     background:#ffcdd2;
    //     border-color:#e57373;   /* little stronger on hover */
    //     transform:scale(1.3);
    // }

    // .progress-container{
    //     display:flex;
    //     flex-direction:column;
    //     align-items:center;
    //     position:relative;
    // }

    // /* âœ… Thin bar */
    // .progress-wrapper{
    //     width:100%;
    //     height:6px;             
    //     background:#eee;
    //     border-radius:10px;
    //     overflow:hidden;
    //     position:relative;
    // }

    // /* âœ… Actual progress */
    // .progress-bar{
    //     height:100%;
    //     border-radius:10px;
    //     transition:width 0.3s ease;
    // }

    // /* âœ… Bottom text */
    // .progress-bottom-text{
    //     margin-top:6px;
    //     font-size:12px;
    //     text-align:center;
    // }

    // /* âœ… Hover text (top) */
    // .progress-hover-text{
    //     position:absolute;
    //     top:-18px;              
    //     font-size:11px;
    //     opacity:0;
    //     transition:0.2s;
    //     white-space:nowrap;
    // }

    // /* âœ… Show on hover */
    // .progress-container:hover .progress-hover-text{
    //     opacity:1;
    // }

    // #today-task-table-container .team-all-btn {
    //     display: none;
    // }


    // .priority-critical{
    //     color: #ff0844;
    //     font-weight: 700;
    //     text-shadow: 0 0 6px rgba(255, 8, 68, 0.4);
    // }

    // /* Royal Violet */
    // .priority-high{
    //     color: #c026ff;
    //     font-weight: 700;
    //     text-shadow: 0 0 6px rgba(192, 38, 255, 0.5);
    // }

    // /* Neon Blue */
    // .priority-medium{
    //     color: #00a8ff;
    //     font-weight: 700;
    //     text-shadow: 0 0 4px rgba(0, 168, 255, 0.3);
    // }

    // /* Golden Yellow */
    // .priority-low{
    //     color: #ffb703;
    //     font-weight: 700;
    //     text-shadow: 0 0 4px rgba(255, 183, 3, 0.3);
    // }


    // </style>



    // <table id="task-report-table">
    // <thead>
    // <tr>
    //     <th style="width:4%">Sl No</th>
    //     <th style="width:8%">Sprint</th>
    //     <th style="width:18%">Project</th>   <!-- smaller -->
    //     <th style="width:9%">Task</th>
    //     <th style="width:20%">Subject</th>  <!-- smaller -->
    //     <th style="width:4%">S/P</th>
    //     <th style="width:4%">RO</th>
    //     <th style="width:4%">CF</th>
    //     <th style="width:5%">ET</th>
    //     <th style="width:5%">AT</th>
    //     <th style="width:5%">Today RT</th>
    //     <th style="width:6%">Priority</th>
    //     <th colspan="2" style="width:12%">Current Status</th> <!-- progress wider -->
    // </tr>
    // </thead>
    // <tbody>
    // `;

    //                 const grouped = {};
    //                 active_data.forEach(row => {
    //                     const team = row[12] || "No Team";
    //                     const cb = row[3] || "No CB";
    //                     const is_tl = row[16] || 0;

    //                     if (!grouped[team]) grouped[team] = {};
    //                     if (!grouped[team][cb]) grouped[team][cb] = { tasks: [], is_tl };
    //                     grouped[team][cb].tasks.push(row);
    //                 });

    //                 const sorted_teams = team_order.filter(team => grouped[team]);

    //                 for (const team of sorted_teams) {
    //                     const team_id = `team-${team.replace(/\s+/g, '_')}`;
    //                     const cb_groups = grouped[team];


    //                     const sorted_cbs = Object.entries(cb_groups).sort((a, b) => {
    //                         const a_order = a[1].tasks[0][25] || 0;
    //                         const b_order = b[1].tasks[0][25] || 0;

    //                         return a_order - b_order; // ascending
    //                     });

    //                     // Team-level totals
    //                     let team_et = 0, team_rt = 0, team_at = 0, team_at_period = 0, team_task_count = 0, team_today_rt=0;

    //                     sorted_cbs.forEach(([cb, cb_data]) => {
    //                         cb_data.tasks.forEach(row => {
    //                             team_et += parseFloat(row[5]) || 0;
    //                             // team_rt += parseFloat(row[6]) || 0;
    //                             team_at += parseFloat(row[7]) || 0;
    //                             // team_at_period += parseFloat(row[13]) || 0;
    //                             team_today_rt += parseFloat(row[14]) || 0;
    //                             team_task_count++;
    //                         });
    //                     });

    //                     // Team header with totals
    //                 let cb_buttons = `<td colspan="7" class="left-align">`;

    //                     cb_buttons += `<span class="team-all-btn" data-team="${team_id}" data-type="all" style="cursor:pointer; font-weight:bold; text-align:center; margin-right:10px;">+ ALL</span>`;


    //                     sorted_cbs.forEach(([cb, cb_data]) => {

    //                     const cb_id = `cb-${team.replace(/\s+/g, '_')}-${cb.replace(/\s+/g, '_')}`;
    //                     const cb_profile = cb_data.tasks[0][18] || "/assets/frappe/images/ui/avatar.png";

    //                     cb_buttons += `
    //                         <span class="cb-btn" data-target="${cb_id}"
    //                             style="
    //                                 cursor:pointer;
    //                                 margin-right:20px;
    //                                 display:inline-flex;
    //                                 flex-direction:column;
    //                                 align-items:center;
    //                             ">

    //                             <img src="${cb_profile}"
    //                                 style="
    //                                     width:35px;
    //                                     height:35px;
    //                                     border-radius:50%;
    //                                     border:2px solid #d9e3f0;
    //                                     margin-bottom:3px;
    //                                 ">


    //                         </span>
    //                         `;

    //                 });

    //                     cb_buttons += `</td>`;

    //                     const first_cb = sorted_cbs[0][1].tasks[0];
    //                     const team_logo = first_cb[19] || "/assets/frappe/images/ui/avatar.png";

    //                     html += `<tr class="toggle-team">
    //                     <td colspan="1" class="left-align">
    //                     <div class="team-logo">
    //                     <img src="${team_logo}">
    //                     </div>
    //                     </td>
    //                     ${cb_buttons}

    //                     <td><b>${team_et.toFixed(2)}</b></td>
    //                     <td><b>${team_at.toFixed(2)}</b></td>
    //                     <td><b>${team_today_rt.toFixed(2)}</b></td>
    //                     <td colspan="3"></td>
    //                     </tr>`;

    //                     for (const [cb, cb_data] of sorted_cbs) {
    //     const tasks = cb_data.tasks;
    //     const cb_id = `cb-${team.replace(/\s+/g, '_')}-${cb.replace(/\s+/g, '_')}`;

    //     let cb_et = 0, cb_rt = 0, cb_at = 0, cb_today_at = 0, cb_today_rt=0
    //     tasks.forEach(row => {
    //         cb_et += parseFloat(row[5]) || 0;
    //         // cb_rt += parseFloat(row[6]) || 0;
    //         cb_at += parseFloat(row[7]) || 0;
    //         cb_today_rt+= parseFloat(row[14]) || 0;
    //         // cb_today_at += parseFloat(row[13]) || 0;
    //     });

    //     const first_row = tasks[0] || [];
    //     html += `<tr class="toggle-cb ${cb_id} ${team_id}" style="display:none;">
    //         <td><span class="toggle-icon">+</span></td>
    //         <td colspan="7" class="left-align" style="color: white;">
    //             ${first_row[24] || ''}
    //         </td>
    //         <td><b>${cb_et.toFixed(2)}</b></td>
    //         <td><b>${cb_at.toFixed(2)}</b></td>
    //         <td><b>${cb_today_rt.toFixed(2)}</b></td>
    //         <td colspan="3"></td>
    //     </tr>`;



    //     // Apply filter inside CB
    //     // let filtered_tasks = tasks.filter(row => {

    //     //     let row_priority = row[8] || "";
    //     //     let row_sp = row[21] == 1 ? "S" : "P";
    //     //     let row_ro = parseInt(row[22]) || 0;

    //     //     if (priority && row_priority !== priority) return false;
    //     //     if (sp && row_sp !== sp) return false;
    //     //     if (ro === "no" && row_ro > 0) return false;   // only show No if row_ro = 0
    //     //     if (ro === "yes" && row_ro === 0) return false;

    //     //     return true;

    //     // });
    //     let filtered_tasks = tasks;

    //     let global_index = 0;
    //     let task_serial = 1;
    //         filtered_tasks.forEach((row) => {
    //             let bg = (global_index % 2 === 0) ? "#FFFFFF" : "#e7e6ec";
    //             let progress = (row[13] > 0 && row[14] > 0) ? ((row[13] / row[14]) * 100).toFixed(0) : 0;
    //             progress = parseFloat(progress);

    //             let ts_color = ""; // empty by default for 0%
    //             if (progress > 100) {
    //                 ts_color = "red";
    //             } else if (progress > 75) {
    //                 ts_color = "orange";
    //             } else if (progress > 0 && progress <= 75) {
    //                 ts_color = "blue";
    //             }
    //             function getPriorityClass(priority) {
    //                 if (!priority) return "";

    //                 priority = priority.toLowerCase();

    //                 if (priority === "critical") {
    //                     return "priority-critical";
    //                 } else if (priority === "high") {
    //                     return "priority-high";
    //                 } else if (priority === "medium") {
    //                     return "priority-medium";
    //                 } else if (priority === "low") {
    //                     return "priority-low";
    //                 }

    //                 return "";
    //             }
    //             let text = "#000000";
    //                 html += `
    //                     <tr class="task-row ${cb_id} ${team_id}"
    //                         data-priority="${row[8]}"
    //                         data-sp="${row[21] == 1 ? 'S' : 'P'}"
    //                         data-ro="${row[22] > 0 ? 'RO' : ''}"
    //                         data-cf="${row[23] > 0 ? 'CF' : ''}"
    //                         ${ts_color ? `data-ts="${ts_color}"` : ""}
    //                         style="display:none; background:${bg}; color:${text};">                   
    //                     <td>${task_serial++}</td>
    //                     <td style="white-space:nowrap;">${row[15]}</td>
    //                     <td class="left-align"><a href="/app/project/${row[1]}" target="_blank">${row[1]}</a></td>
    //                     <td style="white-space:nowrap;">
    //                     <div style="
    //                         display:inline-flex;
    //                         align-items:center;
    //                         gap:6px;
    //                         white-space:nowrap;
    //                     ">

    //                         <!-- 👁 Icon -->
    //                         <span class="task-info-btn"
    //                             data-task="${row[0]}"
    //                             style="cursor:pointer; font-size:16px; color:black; flex-shrink:0;">
    //                             👁
    //                         </span>

    //                         <!-- Task ID -->
    //                         <a href="/app/task/${row[0]}" target="_blank" 
    //                         style="text-decoration:none; color:inherit; flex-shrink:0;">
    //                             ${row[0]}
    //                         </a>

    //                     </div>
    //                 </td>
    //                     <td class="left-align">${row[2]}</td>
    //                     <!-- S/P -->
    //                     <td>
    //                     ${row[21] == 1 
    //                         ? `<span> S </span>`
    //                         : `<span> P </span>`
    //                     }
    //                     </td>
    //                     <!-- RO -->
    //                     <td>
    //                     <span >
    //                     ${row[22] || 0}
    //                     </span>
    //                     </td>

    //                     <!-- CF -->
    //                     <td>${row[23] || 0}</td>
    //                     <td>${row[5]}</td> 
    //                     <td >${row[7]}</td>       
    //                     <td class="total">${row[14]}</td>   
    //                     <td class="completed" style="color:red; display:none;">${row[13]}</td>
    //                     <td class="left-align ${getPriorityClass(row[8])}">
    //                         ${row[8]}
    //                     </td>
    //                     <td colspan="2" class="status-cell" style="width:16%; text-align:center;">
    //                         <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

    //                             ${row[20] == 0 ? `

    //                                 <!-- ✓ Tick -->
    //                                 <span class="confirm-task-btn status-icon tick-icon"
    //                                     data-task="${row[0]}">
    //                                     ✓
    //                                 </span>

    //                             ` : (row[13] > 0 ? (() => {

    //                                 let progress = row[14] > 0 ? ((row[13] / row[14]) * 100).toFixed(0) : 0;
    //                                 progress = parseFloat(progress);

    //                                 let color = "#77e6dc";
    //                                 let text_color = "black";

    //                                 if (progress > 100) {
    //                                     color = "red";
    //                                     text_color = "black";
    //                                 }
    //                                 else if (progress > 75) {
    //                                     color = "orange";
    //                                     text_color = "black";
    //                                 }
    //                                 else if (progress >= 50) {
    //                                     color = "#77e6dc";
    //                                     text_color = "black";
    //                                 }
    //                                 else {
    //                                     color = "#77e6dc";
    //                                     text_color = "black";
    //                                 }
    //                                 let status = (row[10] || "").trim();

    //                                 let status_display = "";

    //                                 if (status === "Working") status_display = "W";
    //                                 else if (status === "Pending Review") status_display = "PR";
    //                                 else if (status === "Client Review") status_display = "CR";
    //                                 else if (status === "Completed") status_display = " ✓";




    //                                 return `
    // <div class="progress-container" style="width:120px;">

    //     <!-- Hover text -->
    //     <div class="progress-hover-text">
    //         ${row[13]}
    //     </div>

    //     <!-- Progress bar -->
    //     <div class="progress-wrapper" style="height:6px;">
    //         <div class="progress-bar" 
    //             style="width:${Math.min(progress,100)}%; background:${color}; height:100%;">
    //         </div>
    //     </div>

    //     <!-- Bottom text -->
    //     <div class="progress-bottom-text"
    //         style="color:${text_color}; font-size:13px;">
    //         ${status_display} ${progress}%
    //     </div>

    // </div>
    // `;

    //                             })() : `

    //                                 <!-- â�Œ C -->
    //                                 <span class="task-unconfirm-btn status-icon c-icon"
    //                                     data-task="${row[0]}">
    //                                     C
    //                                 </span>

    //                             `)}

    //                         </div>
    //                     </td>




    //                 </tr>`;
    //                     global_index++;
    //                     });


    //         }
    //     }    




    //                 html += `</tbody></table>`;
    //                 $container.html(html);

    //                 $(document).off("click", "#open-all-teams-btn").on("click", "#open-all-teams-btn", function(){

    //                     let rows = $container.find(".toggle-cb, .task-row");

    //                     if(rows.is(":visible")){
    //                         rows.hide();
    //                         $(this).text("+ ALL");
    //                     }else{
    //                         rows.show();
    //                         $(this).text("- ALL");
    //                     }

    //                 });

    //                 // Apply Filter


    // $(document).off("click",".filter-btn").on("click",".filter-btn",function(){

    //     let group = $(this).data("group");

    //     // toggle logic
    //     if($(this).hasClass("active")){
    //         $(this).removeClass("active");
    //     }else{

    //         // only one active inside same group
    //         $(`.filter-btn[data-group="${group}"]`).removeClass("active");

    //         $(this).addClass("active");
    //     }

    //     apply_filters();

    // });


    // function apply_filters(){

    //     let priority = $('.filter-btn[data-group="priority"].active').data("filter");
    //     priority = priority ? priority.toString().toLowerCase() : null;
    //     let sp = $('.filter-btn[data-group="sp"].active').data("filter");
    //     let ro = $('.filter-btn[data-group="ro"].active').data("filter");
    //     let cf = $('.filter-btn[data-group="cf"].active').data("filter");
    //     let ts = $('.filter-btn[data-group="ts"].active').data("filter");
    //     ts = ts ? ts.toString().toLowerCase() : null;

    //     $container.find(".task-row").hide();
    //     $container.find(".toggle-cb").hide();

    //     $(".toggle-cb").each(function(){

    //         let cb_row = $(this);
    //         let cb_class = cb_row.attr("class").split(" ")[1];

    //         let tasks = $container.find("." + cb_class + ".task-row");

    //         let matched = tasks.filter(function(){

    //             let p = ($(this).data("priority") || "").toString().toLowerCase();
    //             let s = $(this).data("sp");
    //             let r = $(this).data("ro");
    //             let c = $(this).data("cf");
    //             let t = ($(this).data("ts") || "").toString().toLowerCase();




    //             if(priority && p !== priority) return false;
    //             if(sp && s !== sp) return false;
    //             if(ro && r !== "RO") return false;
    //             if(cf && c !== "CF") return false;
    //             if(ts && (!t || t !== ts)) return false;

    //             return true;

    //         });

    //         if(matched.length){

    //             cb_row.show();

    //             let serial = 1;

    //             matched.each(function(){

    //                 $(this).show();
    //                 $(this).find("td:first").text(serial++);

    //             });

    //         }

    //     });

    // }

    // if($(this).hasClass("active")){
    //     $(".task-row").show();
    //     $(".filter-btn").removeClass("active");
    //     return;
    // }

    //                 // Toggle logic for CB â†’ Task rows
    //                 // Handle individual CB toggle               

    // $container.find('.cb-btn').on('click', function () {

    //     const targetClass = $(this).data('target');
    //     const $rows = $container.find('.' + targetClass);

    //     if ($rows.is(':visible')) {

    //         $rows.hide();

    //     } else {

    //         $rows.show();
    //     }

    // });



    // $(document).on("click", ".task-unconfirm-btn", function (e) {

    //     e.preventDefault();
    //     e.stopPropagation();
    //     e.stopImmediatePropagation();

    //     let btn = $(this);
    //     let task = btn.data("task");
    //     let row = btn.closest("tr");

    //     frappe.call({
    //         method: "teampro.teampro.page.new_it_dashboard.new_it.check_running_timesheet",
    //         args: { task: task },
    //         callback: function(r){

    //             if (r.message) {

    //                 frappe.msgprint({
    //                     title: "Not Allowed",
    //                     message: "This task is already running in a timesheet.",
    //                     indicator: "red"
    //                 });

    //                 return;
    //             }

    //             frappe.db.set_value("Task", task, "is_confirmed", 0).then(() => {

    //                 frappe.show_alert({
    //                     message: "Task Unconfirmed",
    //                     indicator: "orange"
    //                 });

    //                 let status_cell = row.find(".status-cell");
    //                 let progress_cell = row.find(".progress-cell");

    //                 status_cell.html(`
    //                     <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

    //                         <span class="confirm-task-btn status-icon tick-icon"
    //                             data-task="${task}">
    //                             âœ“
    //                         </span>



    //                     </div>
    //                 `);


    //             });

    //         }
    //     });

    // });

    // $(document).on('click', '.confirm-task-btn', function (e) {

    //     e.preventDefault();
    //     e.stopPropagation();
    //     e.stopImmediatePropagation();

    //     const btn = $(this);
    //     const task = btn.data('task');
    //     const row = btn.closest("tr");

    //     frappe.call({
    //         method: "frappe.client.set_value",
    //         args: {
    //             doctype: "Task",
    //             name: task,
    //             fieldname: "is_confirmed",
    //             value: 1
    //         },
    //         callback: function () {

    //             frappe.show_alert({
    //                 message: "Task Confirmed",
    //                 indicator: "green"
    //             });

    //             frappe.db.get_value("Task", task, "status").then(r => {

    //                 let status_text = r.message.status || "";

    //                 let completed = parseFloat(row.find(".completed").text()) || 0;
    //                 let total = parseFloat(row.find(".total").text()) || 0;
    //                 let status_cell = row.find(".status-cell");
    //                 let progress_cell = row.find(".progress-cell");
    //                 let progress = total > 0 ? ((completed / total) * 100).toFixed(0) : 0;

    //                     let color = "#4CAF50";
    //                     let text_color = "black";

    //                     if (progress > 100) {
    //                         color = "red";
    //                         text_color = "black";
    //                     }
    //                     else if (progress > 75) {
    //                         color = "orange";
    //                         text_color = "black";
    //                     }
    //                     else if (progress >= 50) {
    //                         color = "#77e6dc";
    //                         text_color = "black";
    //                     }
    //                     else {
    //                         color = "#77e6dc";
    //                         text_color = "black";
    //                     }

    //                     let status = (status_text || "").trim();

    //                     let status_display = "";

    //                     if (status === "Working") status_display = "";
    //                     else if (status === "Pending Review") status_display = "PR";
    //                     else if (status === "Client Review") status_display = "CR";
    //                     else if (status === "Completed") status_display = "âœ”";

    //                     let hover_color = "#d81b60";

    //                     if (color === "red" || color === "orange") {
    //                         hover_color = "black";
    //                     }

    //                 // âœ… 1st cell update
    //                 status_cell.html(`
    //                     <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

    //                         <span class="task-unconfirm-btn status-icon c-icon"
    //                             data-task="${task}"

    //                             ">
    //                             C
    //                         </span>



    //                     </div>
    //                 `);


    //             });
    //         }
    //     });

    // });

    // $container.off("click", ".task-info-btn").on("click", ".task-info-btn", function () {

    //     const task = $(this).data("task");

    //     frappe.call({
    //         method: "frappe.client.get",
    //         args: {
    //             doctype: "Task",
    //             name: task
    //         },
    //         callback: function(r) {

    //             const t = r.message;


    //             let html = `
    // <div>
    //     <table style="width:100%; border-collapse:collapse; border:1px solid black;">

    //         <tr>
    //             <td style="border:1px solid black;" ><b style="color:red;">Task :</b></td>
    //             <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.name}</span></td>
    //             <td style="border:1px solid black;" ><b style="color:red;">Project :</b></td>
    //             <td style="border:1px solid black;" colspan="3"><span style="color:blue;">${t.project || ""}</span></td>
    //         </tr>

    //         <tr>
    //             <td style="border:1px solid black;" ><b style="color:red;">Subject :</b></td>
    //             <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.subject || ""}</span></td>
    //         </tr>

    //         <tr>
    //             <td style="border:1px solid black;" ><b style="color:red;">Description :</b></td>
    //             <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.description || ""}</span></td>
    //         </tr>

    //         <tr>
    //             <td style="border:1px solid black;" colspan="1"><b style="color:red;">ET :</b></td>
    //             <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.expected_time || ""}</span></td>
    //             <td style="border:1px solid black;" colspan="1"><b style="color:red;">RT :</b></td>
    //             <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.rt || ""}</span></td>
    //             <td style="border:1px solid black;" colspan="1"><b style="color:red;">AT :</b></td>
    //             <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.actual_time || ""}</span></td>
    //         </tr>

    //         <tr>
    //             <td style="border:1px solid black;" ><b style="color:red;">CF :</b></td>
    //             <td style="border:1px solid black;" colspan="2"><span style="color:blue;">${t.custom_production_date_count}</span></td>
    //             <td style="border:1px solid black;" ><b style="color:red;">RO :</b></td>
    //             <td style="border:1px solid black;" colspan="2"><span style="color:blue;">${t.revisions || ""}</span></td>
    //         </tr>

    //         <tr>
    //             <td style="border:1px solid black;" ><b style="color:red;">Created On :</b></td>
    //             <td style="border:1px solid black;" ><span style="color:blue;">
    //                 ${t.creation ? frappe.datetime.str_to_user(t.creation) : ""}
    //             </span></td>

    //             <td style="border:1px solid black;"><b style="color:red;">Allocated On :</b></td>
    //             <td style="border:1px solid black;"><span style="color:blue;">
    //                 ${t.custom_allocated_on ? frappe.datetime.str_to_user(t.custom_allocated_on) : ""}
    //             </span></td>

    //             <td style="border:1px solid black;" ><b style="color:red;">Age :</b></td>
    //             <td style="border:1px solid black;" ><span style="color:blue;">
    //                 ${t.custom_age}
    //             </span></td>
    //         </tr>

    //         <tr>
    //             <td style="border:1px solid black;" ><b style="color:red;">Developer Note :</b></td>
    //             <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.custom_developer_note || ""}</span></td>
    //         </tr>

    //         <tr>
    //             <td style="border:1px solid black;" ><b style="color:red;">Remarks :</b></td>
    //             <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.custom_taskissue_action_taken || ""}</span></td>
    //         </tr>

    //     </table>
    // </div>
    // `;

    //             let d = new frappe.ui.Dialog({
    //                 title: "Task Details",
    //                 fields: [
    //                     {
    //                         fieldtype: "HTML",
    //                         fieldname: "task_details",
    //                         options: html
    //                     }
    //                 ]
    //             });

    //             d.show();

    //             $(d.$wrapper).find('.modal-dialog').css({
    //                 "max-width": "900px",  
    //                 "width": "90%"          
    //             });
    //         }
    //     });

    // });





    // // $container.find('span[data-type="all"]').on('click', function () {
    // //     const teamId = $(this).data('team');
    // //     const teamRows = $container.find(`.${teamId}`); // includes both CB + task rows
    // //     const isVisible = teamRows.is(':visible');

    // //     if (isVisible) {
    // //         teamRows.hide();
    // //         $(this).text('+ ALL');
    // //         // Also reset CB buttons text
    // //         $(`span[data-target^="cb-${teamId}"]`).each(function() {
    // //             $(this).text('+ ' + $(this).text().slice(2));
    // //         });
    // //     } else {
    // //         teamRows.show();
    // //         $(this).text('- ALL');
    // //         // Also update CB buttons text
    // //         $(`span[data-target^="cb-${teamId}"]`).each(function() {
    // //             $(this).text('- ' + $(this).text().slice(2));
    // //         });
    // //     }
    // // });


    // $("#today-task-table-container")
    // .off("click", "span[data-type='all']")
    // .on("click", "span[data-type='all']", function () {

    //     const teamId = $(this).data('team');
    //     toggleTeamRows(teamId, this);

    // });


    //             } else {
    //                 $container.html("<p>No data found.</p>");
    //             }
    //         }
    //     });

    // }



    function get_today_task_data1(from_date = null, to_date = null) {
        let priority = $("#filter-priority").val();
        let sp = $("#filter-sp").val();
        let ro = $("#filter-ro").val();
        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.get_today_task_data1",
            args: {
                priority: priority,
                sp: sp,
                ro: ro,
                from_date: from_date,
                to_date: to_date
            },
            callback: function (r) {
                let $container = $("#today-task-table-container");

                if (r.message && r.message.data) {

                    // const data = r.message;

                    const data = r.message.data;
                    console.log(data[0])
                    const team_order = r.message.team_order;
                    const active_data = data;
                    console.log(data)

                    let total_et = 0;
                    let total_rt = 0;
                    let total_at = 0;
                    let total_today_rt = 0;
                    let total_at_period = 0;

                    active_data.forEach(row => {
                        total_et += parseFloat(row[5]) || 0;
                        total_rt += parseFloat(row[6]) || 0;
                        total_at += parseFloat(row[7]) || 0;
                        total_today_rt += parseFloat(row[14]) || 0;
                        total_at_period += parseFloat(row[13]) || 0;
                    });

                    let html = `
<style>
.scrollable-table-container {
    max-height: 600px;
    overflow-y: auto;
    border: 1px solid #ccc;
    margin-bottom: 10px;
}
.export-buttons {
    margin-bottom: 10px;
    text-align: right;
}
.export-buttons button {
    margin-left: 5px;
}
#task-report-table {
    width:100%;
    border-collapse:collapse !important;
    table-layout:fixed;
}


.total-row td {
    border: 1px solid black !important;
}

#task-report-table th,
#task-report-table td {
    border: 1px solid black;
    text-align: center;
    padding: 8px;
    font-size: 14px;
}

#task-report-table thead th {
    background-color: #0F1568;
    color: white;
    font-size: 16px;
    padding: 10px;
    position: sticky;
    top: 0;
    z-index: 2;
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
    font-size: 14px;
}
.left-align {
    text-align: left !important;
}

.toggle-team {
    cursor: pointer;
    font-weight: bold;
    background-color: #eaf0f6;
}
.toggle-cb {
    cursor: pointer;
    font-weight: bold;
    background-color: #85819e;
    color: white;
}

.cb-circle{
    display:inline-flex;
    flex-direction:column;
    align-items:center;
}

.cb-circle img{
    width:32px;
    height:32px;
    border-radius:50%;
    border:2px solid #d9e3f0;
    object-fit:cover;
}



.cb-code{
    font-size:11px;
    margin-top:2px;
    font-weight:600;
}

.team-logo img{
    width:45px;
    height:45px;
    border-radius:8px;
    border:2px solid #d9e3f0;
    padding:3px;
    background:white;
}

.task-row:nth-child(odd){
    background-color: #ffffff;   /* white */
    color: #000000;  
}

.task-row:nth-child(even){
    background-color: #eaf0f6;   /* light mild blue */
    color: #000000;
}

.all-team-btn{
    background:#0F1568;
    color:white;
    border:none;
    padding:3px 9px;
    font-size:14px;
    border-radius:6px;
    cursor:pointer;
    transition:all 0.2s ease;
}

.all-team-btn:hover{
    transform:scale(1.15);
    background:#1b238f;
}

.nav-all-btn{
    background:#fff3e0;        /* mild inside color */
    color:#e65100;             /* text color */
    border:2px solid #ff6f00;  /* strong border */
    padding:12px 32px; 
    font-size:14px;
    border-radius:14px;
    cursor:pointer;
    margin-right:12px;
    margin-left:12px;
    font-weight:600;
    transition:all 0.25s ease;
}

.nav-all-btn:hover{
    background:#ffe0b2;        /* hover mild */
    border-color:#e65100;      /* border darker */
    transform:scale(1.15);
}

.progress-wrapper{
    position:relative;
    width:100%;
    background:#eee;
    border-radius:10px;
    height:22px;
    overflow:hidden;
    border:0.5px solid black;
}

.progress-bar{
    height:100%;
}

.progress-text{
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:12px;
    font-weight:bold;
    pointer-events:none;
}


.hover-text{
    display:none;
}

.progress-wrapper:hover .default-text{
    display:none;
}

.progress-wrapper:hover .hover-text{
    display:flex;
}

.filter-btn{
    padding:2px 6px;
    font-size:12px;
    border-radius:4px;
    border:0.5px solid #d0d7de;
}

/* hover */
.filter-btn:hover{
    background:#e0e7ff;
    border-color:#0F1568;
}

/* active (selected) */
.filter-btn.active{
    background:#0F1568;
    color:#fff;
    border-color:#0F1568;
}

.filter-btn{
    margin-right:4px;
}

.task-row a{
    color: inherit;
    text-decoration: none;
}

.progress-wrapper{
    position:relative;
    height:22px;
    background:#eee;
    border-radius:12px;
    overflow:hidden;
}
.progress-bar{
    height:100%;
}
.progress-text{
    position:absolute;
    width:100%;
    text-align:center;
    font-size:12px;
    top:0;
}
.status-icon{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    width:28px;
    height:28px;
    border-radius:50%;
    font-size:14px;
    font-weight:bold;
    cursor:pointer;
    transition:all 0.2s ease;

    border:1.5px solid transparent;  
}

.tick-icon{
    background:#e3f2fd;
    color:#0d47a1;
    border-color:#90caf9;   /* mild blue border */
}

.tick-icon:hover{
    background:#bbdefb;
    border-color:#64b5f6;   /* little stronger on hover */
    transform:scale(1.3);
}

.c-icon{
    background:#ffebee;
    color:#b71c1c;
    border-color:#ef9a9a;   /* mild red border */
}

.c-icon:hover{
    background:#ffcdd2;
    border-color:#e57373;   /* little stronger on hover */
    transform:scale(1.3);
}

.progress-container{
    display:flex;
    flex-direction:column;
    align-items:center;
    position:relative;
}

/* âœ… Thin bar */
.progress-wrapper{
    width:100%;
    height:6px;             
    background:#eee;
    border-radius:10px;
    overflow:hidden;
    position:relative;
}

/* âœ… Actual progress */
.progress-bar{
    height:100%;
    border-radius:10px;
    transition:width 0.3s ease;
}

/* âœ… Bottom text */
.progress-bottom-text{
    margin-top:6px;
    font-size:12px;
    text-align:center;
}

/* âœ… Hover text (top) */
.progress-hover-text{
    position:absolute;
    top:-18px;              
    font-size:11px;
    opacity:0;
    transition:0.2s;
    white-space:nowrap;
}

/* âœ… Show on hover */
.progress-container:hover .progress-hover-text{
    opacity:1;
}

#today-task-table-container .team-all-btn {
    display: none;
}


.priority-critical{
    color: #ff0844;
    font-weight: 700;
    text-shadow: 0 0 6px rgba(255, 8, 68, 0.4);
}

/* Royal Violet */
.priority-high{
    color: #c026ff;
    font-weight: 700;
    text-shadow: 0 0 6px rgba(192, 38, 255, 0.5);
}

/* Neon Blue */
.priority-medium{
    color: #00a8ff;
    font-weight: 700;
    text-shadow: 0 0 4px rgba(0, 168, 255, 0.3);
}

/* Golden Yellow */
.priority-low{
    color: #ffb703;
    font-weight: 700;
    text-shadow: 0 0 4px rgba(255, 183, 3, 0.3);
}


</style>



<table id="task-report-table">
<thead>
<tr>
    <th style="width:4%">Sl No</th>
    <th style="width:8%">Sprint</th>
    <th style="width:18%">Project</th>   <!-- smaller -->
    <th style="width:9%">Task</th>
    <th style="width:20%">Subject</th>  <!-- smaller -->
    <th style="width:4%">S/P</th>
    <th style="width:4%">RO</th>
    <th style="width:4%">CF</th>
    <th style="width:5%">ET</th>
    <th style="width:5%">AT</th>
    <th style="width:5%">Today RT</th>
    <th style="width:6%">Priority</th>
    <th colspan="2" style="width:12%">Current Status</th> <!-- progress wider -->
</tr>
</thead>
<tbody>
`;

                    const grouped = {};
                    active_data.forEach(row => {
                        const team = row[12] || "No Team";
                        const cb = row[3] || "No CB";
                        const is_tl = row[16] || 0;

                        if (!grouped[team]) grouped[team] = {};
                        if (!grouped[team][cb]) grouped[team][cb] = { tasks: [], is_tl };
                        grouped[team][cb].tasks.push(row);
                    });

                    const sorted_teams = team_order.filter(team => grouped[team]);

                    for (const team of sorted_teams) {
                        const team_id = `team-${team.replace(/\s+/g, '_')}`;
                        const cb_groups = grouped[team];


                        const sorted_cbs = Object.entries(cb_groups).sort((a, b) => {
                            const a_order = a[1].tasks[0][25] || 0;
                            const b_order = b[1].tasks[0][25] || 0;

                            return a_order - b_order; // ascending
                        });

                        // Team-level totals
                        let team_et = 0, team_rt = 0, team_at = 0, team_at_period = 0, team_task_count = 0, team_today_rt = 0;

                        sorted_cbs.forEach(([cb, cb_data]) => {
                            cb_data.tasks.forEach(row => {
                                team_et += parseFloat(row[5]) || 0;
                                // team_rt += parseFloat(row[6]) || 0;
                                team_at += parseFloat(row[7]) || 0;
                                // team_at_period += parseFloat(row[13]) || 0;
                                team_today_rt += parseFloat(row[14]) || 0;
                                team_task_count++;
                            });
                        });

                        // Team header with totals
                        let cb_buttons = `<td colspan="7" class="left-align">`;

                        cb_buttons += `<span class="team-all-btn" data-team="${team_id}" data-type="all" style="cursor:pointer; font-weight:bold; text-align:center; margin-right:10px;">+ ALL</span>`;


                        sorted_cbs.forEach(([cb, cb_data]) => {

                            const cb_id = `cb-${team.replace(/\s+/g, '_')}-${cb.replace(/\s+/g, '_')}`;
                            const cb_profile = cb_data.tasks[0][18] || "/assets/frappe/images/ui/avatar.png";

                            cb_buttons += `
                        <span class="cb-btn" data-target="${cb_id}"
                            style="
                                cursor:pointer;
                                margin-right:20px;
                                display:inline-flex;
                                flex-direction:column;
                                align-items:center;
                            ">
                            
                            <img src="${cb_profile}"
                                style="
                                    width:35px;
                                    height:35px;
                                    border-radius:50%;
                                    border:2px solid #d9e3f0;
                                    margin-bottom:3px;
                                ">

                            
                        </span>
                        `;

                        });

                        cb_buttons += `</td>`;

                        const first_cb = sorted_cbs[0][1].tasks[0];
                        const team_logo = first_cb[19] || "/assets/frappe/images/ui/avatar.png";

                        html += `<tr class="toggle-team">
                    <td colspan="1" class="left-align">
                    <div class="team-logo">
                    <img src="${team_logo}">
                    </div>
                    </td>
                    ${cb_buttons}
                    
                    <td><b>${team_et.toFixed(2)}</b></td>
                    <td><b>${team_at.toFixed(2)}</b></td>
                    <td><b>${team_today_rt.toFixed(2)}</b></td>
                    <td colspan="3"></td>
                    </tr>`;

                        for (const [cb, cb_data] of sorted_cbs) {
                            const tasks = cb_data.tasks;
                            const cb_id = `cb-${team.replace(/\s+/g, '_')}-${cb.replace(/\s+/g, '_')}`;

                            let cb_et = 0, cb_rt = 0, cb_at = 0, cb_today_at = 0, cb_today_rt = 0
                            tasks.forEach(row => {
                                cb_et += parseFloat(row[5]) || 0;
                                // cb_rt += parseFloat(row[6]) || 0;
                                cb_at += parseFloat(row[7]) || 0;
                                cb_today_rt += parseFloat(row[14]) || 0;
                                // cb_today_at += parseFloat(row[13]) || 0;
                            });

                            const first_row = tasks[0] || [];
                            html += `<tr class="toggle-cb ${cb_id} ${team_id}" style="display:none;">
        <td><span class="toggle-icon">+</span></td>
        <td colspan="7" class="left-align" style="color: white;">
            ${first_row[24] || ''}
        </td>
        <td><b>${cb_et.toFixed(2)}</b></td>
        <td><b>${cb_at.toFixed(2)}</b></td>
        <td><b>${cb_today_rt.toFixed(2)}</b></td>
        <td colspan="3"></td>
    </tr>`;



                            // Apply filter inside CB
                            // let filtered_tasks = tasks.filter(row => {

                            //     let row_priority = row[8] || "";
                            //     let row_sp = row[21] == 1 ? "S" : "P";
                            //     let row_ro = parseInt(row[22]) || 0;

                            //     if (priority && row_priority !== priority) return false;
                            //     if (sp && row_sp !== sp) return false;
                            //     if (ro === "no" && row_ro > 0) return false;   // only show No if row_ro = 0
                            //     if (ro === "yes" && row_ro === 0) return false;

                            //     return true;

                            // });
                            let filtered_tasks = tasks;

                            let global_index = 0;
                            let task_serial = 1;
                            filtered_tasks.forEach((row) => {
                                let bg = (global_index % 2 === 0) ? "#FFFFFF" : "#e7e6ec";
                                let progress = (row[13] > 0 && row[14] > 0) ? ((row[13] / row[14]) * 100).toFixed(0) : 0;
                                progress = parseFloat(progress);

                                let ts_color = ""; // empty by default for 0%
                                if (progress > 100) {
                                    ts_color = "red";
                                } else if (progress > 75) {
                                    ts_color = "orange";
                                } else if (progress > 0 && progress <= 75) {
                                    ts_color = "blue";
                                }
                                function getPriorityClass(priority) {
                                    if (!priority) return "";

                                    priority = priority.toLowerCase();

                                    if (priority === "critical") {
                                        return "priority-critical";
                                    } else if (priority === "high") {
                                        return "priority-high";
                                    } else if (priority === "medium") {
                                        return "priority-medium";
                                    } else if (priority === "low") {
                                        return "priority-low";
                                    }

                                    return "";
                                }
                                let text = "#000000";
                                html += `
                    <tr class="task-row ${cb_id} ${team_id}"
                        data-priority="${row[8]}"
                        data-sp="${row[21] == 1 ? 'S' : 'P'}"
                        data-ro="${row[22] > 0 ? 'RO' : ''}"
                        data-cf="${row[23] > 0 ? 'CF' : ''}"
                        ${ts_color ? `data-ts="${ts_color}"` : ""}
                        style="display:none; background:${bg}; color:${text};">                   
                    <td>${task_serial++}</td>
                    <td style="white-space:nowrap;">${row[15]}</td>
                    <td class="left-align"><a href="/app/project/${row[1]}" target="_blank">${row[1]}</a></td>
                    <td style="white-space:nowrap;">
                    <div style="
                        display:inline-flex;
                        align-items:center;
                        gap:6px;
                        white-space:nowrap;
                    ">

                        <!-- 👁 Icon -->
                        <span class="task-info-btn"
                            data-task="${row[0]}"
                            style="cursor:pointer; font-size:16px; color:black; flex-shrink:0;">
                            👁
                        </span>

                        <!-- Task ID -->
                        <a href="/app/task/${row[0]}" target="_blank" 
                        style="text-decoration:none; color:inherit; flex-shrink:0;">
                            ${row[0]}
                        </a>

                    </div>
                </td>
                    <td class="left-align">${row[2]}</td>
                    <!-- S/P -->
                    <td>
                    ${row[21] == 1
                                        ? `<span> S </span>`
                                        : `<span> P </span>`
                                    }
                    </td>
                    <!-- RO -->
                    <td>
                    <span >
                    ${row[22] || 0}
                    </span>
                    </td>

                    <!-- CF -->
                    <td>${row[23] || 0}</td>
                    <td>${row[5]}</td> 
                    <td >${row[7]}</td>       
                    <td class="total">${row[14]}</td>   
                    <td class="completed" style="color:red; display:none;">${row[13]}</td>
                    <td class="left-align ${getPriorityClass(row[8])}">
                        ${row[8]}
                    </td>
                    <td colspan="2" class="status-cell" style="width:16%; text-align:center;">
                        <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

                            ${row[20] == 0 ? `

                                <!-- ✓ Tick -->
                                <span class="confirm-task-btn status-icon tick-icon"
                                    data-task="${row[0]}">
                                    ✓
                                </span>

                            ` : (row[13] > 0 ? (() => {

                                        let progress = row[14] > 0 ? ((row[13] / row[14]) * 100).toFixed(0) : 0;
                                        progress = parseFloat(progress);

                                        let color = "#77e6dc";
                                        let text_color = "black";

                                        if (progress > 100) {
                                            color = "red";
                                            text_color = "black";
                                        }
                                        else if (progress > 75) {
                                            color = "orange";
                                            text_color = "black";
                                        }
                                        else if (progress >= 50) {
                                            color = "#77e6dc";
                                            text_color = "black";
                                        }
                                        else {
                                            color = "#77e6dc";
                                            text_color = "black";
                                        }
                                        let status = (row[10] || "").trim();

                                        let status_display = "";

                                        if (status === "Working") status_display = "W";
                                        else if (status === "Pending Review") status_display = "PR";
                                        else if (status === "Client Review") status_display = "CR";
                                        else if (status === "Completed") status_display = " ✓";




                                        return `
<div class="progress-container" style="width:120px;">

    <!-- Hover text -->
    <div class="progress-hover-text">
        ${row[13]}
    </div>

    <!-- Progress bar -->
    <div class="progress-wrapper" style="height:6px;">
        <div class="progress-bar" 
            style="width:${Math.min(progress, 100)}%; background:${color}; height:100%;">
        </div>
    </div>

    <!-- Bottom text -->
    <div class="progress-bottom-text"
        style="color:${text_color}; font-size:13px;">
        ${status_display} ${progress}%
    </div>

</div>
`;

                                    })() : `

                                <!--C -->
                                <span class="task-unconfirm-btn status-icon c-icon"
                                    data-task="${row[0]}">
                                    C
                                </span>

                            `)}

                        </div>
                    </td>

                    


                </tr>`;
                                global_index++;
                            });


                        }
                    }




                    html += `</tbody></table>`;
                    $container.html(html);

                    $(document).off("click", "#open-all-teams-btn").on("click", "#open-all-teams-btn", function () {

                        let rows = $container.find(".toggle-cb, .task-row");

                        if (rows.is(":visible")) {
                            rows.hide();
                            $(this).text("+ ALL");
                        } else {
                            rows.show();
                            $(this).text("- ALL");
                        }

                    });

                    // Apply Filter


                    $(document).off("click", ".filter-btn").on("click", ".filter-btn", function () {

                        let group = $(this).data("group");

                        // toggle logic
                        if ($(this).hasClass("active")) {
                            $(this).removeClass("active");
                        } else {

                            // only one active inside same group
                            $(`.filter-btn[data-group="${group}"]`).removeClass("active");

                            $(this).addClass("active");
                        }

                        apply_filters();

                    });


                    function apply_filters() {

                        let priority = $('.filter-btn[data-group="priority"].active').data("filter");
                        priority = priority ? priority.toString().toLowerCase() : null;
                        let sp = $('.filter-btn[data-group="sp"].active').data("filter");
                        let ro = $('.filter-btn[data-group="ro"].active').data("filter");
                        let cf = $('.filter-btn[data-group="cf"].active').data("filter");
                        let ts = $('.filter-btn[data-group="ts"].active').data("filter");
                        ts = ts ? ts.toString().toLowerCase() : null;

                        $container.find(".task-row").hide();
                        $container.find(".toggle-cb").hide();

                        $(".toggle-cb").each(function () {

                            let cb_row = $(this);
                            let cb_class = cb_row.attr("class").split(" ")[1];

                            let tasks = $container.find("." + cb_class + ".task-row");

                            let matched = tasks.filter(function () {

                                let p = ($(this).data("priority") || "").toString().toLowerCase();
                                let s = $(this).data("sp");
                                let r = $(this).data("ro");
                                let c = $(this).data("cf");
                                let t = ($(this).data("ts") || "").toString().toLowerCase();




                                if (priority && p !== priority) return false;
                                if (sp && s !== sp) return false;
                                if (ro && r !== "RO") return false;
                                if (cf && c !== "CF") return false;
                                if (ts && (!t || t !== ts)) return false;

                                return true;

                            });

                            if (matched.length) {

                                cb_row.show();

                                let serial = 1;

                                matched.each(function () {

                                    $(this).show();
                                    $(this).find("td:first").text(serial++);

                                });

                            }

                        });

                    }

                    if ($(this).hasClass("active")) {
                        $(".task-row").show();
                        $(".filter-btn").removeClass("active");
                        return;
                    }

                    // Toggle logic for CB â†’ Task rows
                    // Handle individual CB toggle               

                    $container.find('.cb-btn').on('click', function () {

                        const targetClass = $(this).data('target');
                        const $rows = $container.find('.' + targetClass);

                        if ($rows.is(':visible')) {

                            $rows.hide();

                        } else {

                            $rows.show();
                        }

                    });



                    $(document).on("click", ".task-unconfirm-btn", function (e) {

                        e.preventDefault();
                        e.stopPropagation();
                        e.stopImmediatePropagation();

                        let btn = $(this);
                        let task = btn.data("task");
                        let row = btn.closest("tr");

                        frappe.call({
                            method: "teampro.teampro.page.new_it_dashboard.new_it.check_running_timesheet",
                            args: { task: task },
                            callback: function (r) {

                                if (r.message) {

                                    frappe.msgprint({
                                        title: "Not Allowed",
                                        message: "This task is already running in a timesheet.",
                                        indicator: "red"
                                    });

                                    return;
                                }

                                frappe.db.set_value("Task", task, "is_confirmed", 0).then(() => {

                                    frappe.show_alert({
                                        message: "Task Unconfirmed",
                                        indicator: "orange"
                                    });

                                    let status_cell = row.find(".status-cell");
                                    let progress_cell = row.find(".progress-cell");

                                    status_cell.html(`
                    <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

                        <span class="confirm-task-btn status-icon tick-icon"
                            data-task="${task}">
                            ✓
                        </span>

                        

                    </div>
                `);


                                });

                            }
                        });

                    });

                    $(document).on('click', '.confirm-task-btn', function (e) {

                        e.preventDefault();
                        e.stopPropagation();
                        e.stopImmediatePropagation();

                        const btn = $(this);
                        const task = btn.data('task');
                        const row = btn.closest("tr");

                        frappe.call({
                            method: "frappe.client.set_value",
                            args: {
                                doctype: "Task",
                                name: task,
                                fieldname: "is_confirmed",
                                value: 1
                            },
                            callback: function () {

                                frappe.show_alert({
                                    message: "Task Confirmed",
                                    indicator: "green"
                                });

                                frappe.db.get_value("Task", task, "status").then(r => {

                                    let status_text = r.message.status || "";

                                    let completed = parseFloat(row.find(".completed").text()) || 0;
                                    let total = parseFloat(row.find(".total").text()) || 0;
                                    let status_cell = row.find(".status-cell");
                                    let progress_cell = row.find(".progress-cell");
                                    let progress = total > 0 ? ((completed / total) * 100).toFixed(0) : 0;

                                    let color = "#4CAF50";
                                    let text_color = "black";

                                    if (progress > 100) {
                                        color = "red";
                                        text_color = "black";
                                    }
                                    else if (progress > 75) {
                                        color = "orange";
                                        text_color = "black";
                                    }
                                    else if (progress >= 50) {
                                        color = "#77e6dc";
                                        text_color = "black";
                                    }
                                    else {
                                        color = "#77e6dc";
                                        text_color = "black";
                                    }

                                    let status = (status_text || "").trim();

                                    let status_display = "";

                                    if (status === "Working") status_display = "";
                                    else if (status === "Pending Review") status_display = "PR";
                                    else if (status === "Client Review") status_display = "CR";
                                    else if (status === "Completed") status_display = "âœ”";

                                    let hover_color = "#d81b60";

                                    if (color === "red" || color === "orange") {
                                        hover_color = "black";
                                    }

                                    status_cell.html(`
                    <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

                        <span class="task-unconfirm-btn status-icon c-icon"
                            data-task="${task}"
                            
                            ">
                            C
                        </span>

                        

                    </div>
                `);


                                });
                            }
                        });

                    });

                    $container.off("click", ".task-info-btn").on("click", ".task-info-btn", function () {

                        const task = $(this).data("task");

                        frappe.call({
                            method: "frappe.client.get",
                            args: {
                                doctype: "Task",
                                name: task
                            },
                            callback: function (r) {

                                const t = r.message;


                                let html = `
<div>
    <table style="width:100%; border-collapse:collapse; border:1px solid black;">

        <tr>
            <td style="border:1px solid black;" ><b style="color:red;">Task :</b></td>
            <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.name}</span></td>
            <td style="border:1px solid black;" ><b style="color:red;">Project :</b></td>
            <td style="border:1px solid black;" colspan="3"><span style="color:blue;">${t.project || ""}</span></td>
        </tr>

        <tr>
            <td style="border:1px solid black;" ><b style="color:red;">Subject :</b></td>
            <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.subject || ""}</span></td>
        </tr>

        <tr>
            <td style="border:1px solid black;" ><b style="color:red;">Description :</b></td>
            <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.description || ""}</span></td>
        </tr>

        <tr>
            <td style="border:1px solid black;" colspan="1"><b style="color:red;">ET :</b></td>
            <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.expected_time || ""}</span></td>
            <td style="border:1px solid black;" colspan="1"><b style="color:red;">RT :</b></td>
            <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.rt || ""}</span></td>
            <td style="border:1px solid black;" colspan="1"><b style="color:red;">AT :</b></td>
            <td style="border:1px solid black;" colspan="1"><span style="color:blue;">${t.actual_time || ""}</span></td>
        </tr>

        <tr>
            <td style="border:1px solid black;" ><b style="color:red;">CF :</b></td>
            <td style="border:1px solid black;" colspan="2"><span style="color:blue;">${t.custom_production_date_count}</span></td>
            <td style="border:1px solid black;" ><b style="color:red;">RO :</b></td>
            <td style="border:1px solid black;" colspan="2"><span style="color:blue;">${t.revisions || ""}</span></td>
        </tr>

        <tr>
            <td style="border:1px solid black;" ><b style="color:red;">Created On :</b></td>
            <td style="border:1px solid black;" ><span style="color:blue;">
                ${t.creation ? frappe.datetime.str_to_user(t.creation) : ""}
            </span></td>

            <td style="border:1px solid black;"><b style="color:red;">Allocated On :</b></td>
            <td style="border:1px solid black;"><span style="color:blue;">
                ${t.custom_allocated_on ? frappe.datetime.str_to_user(t.custom_allocated_on) : ""}
            </span></td>

            <td style="border:1px solid black;" ><b style="color:red;">Age :</b></td>
            <td style="border:1px solid black;" ><span style="color:blue;">
                ${t.custom_age}
            </span></td>
        </tr>

        <tr>
            <td style="border:1px solid black;" ><b style="color:red;">Developer Note :</b></td>
            <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.custom_developer_note || ""}</span></td>
        </tr>

        <tr>
            <td style="border:1px solid black;" ><b style="color:red;">Remarks :</b></td>
            <td style="border:1px solid black;" colspan="5"><span style="color:blue;">${t.custom_taskissue_action_taken || ""}</span></td>
        </tr>

    </table>
</div>
`;

                                let d = new frappe.ui.Dialog({
                                    title: "Task Details",
                                    fields: [
                                        {
                                            fieldtype: "HTML",
                                            fieldname: "task_details",
                                            options: html
                                        }
                                    ]
                                });

                                d.show();

                                $(d.$wrapper).find('.modal-dialog').css({
                                    "max-width": "900px",
                                    "width": "90%"
                                });
                            }
                        });

                    });





                    // $container.find('span[data-type="all"]').on('click', function () {
                    //     const teamId = $(this).data('team');
                    //     const teamRows = $container.find(`.${teamId}`); // includes both CB + task rows
                    //     const isVisible = teamRows.is(':visible');

                    //     if (isVisible) {
                    //         teamRows.hide();
                    //         $(this).text('+ ALL');
                    //         // Also reset CB buttons text
                    //         $(`span[data-target^="cb-${teamId}"]`).each(function() {
                    //             $(this).text('+ ' + $(this).text().slice(2));
                    //         });
                    //     } else {
                    //         teamRows.show();
                    //         $(this).text('- ALL');
                    //         // Also update CB buttons text
                    //         $(`span[data-target^="cb-${teamId}"]`).each(function() {
                    //             $(this).text('- ' + $(this).text().slice(2));
                    //         });
                    //     }
                    // });


                    $("#today-task-table-container")
                        .off("click", "span[data-type='all']")
                        .on("click", "span[data-type='all']", function () {

                            const teamId = $(this).data('team');
                            toggleTeamRows(teamId, this);

                        });


                } else {
                    $container.html("<p>No data found.</p>");
                }
            }
        });

    }


    function load_non_allocated_tasks_in_live_sprint() {

        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.get_non_allocated_tasks_in_live_sprint",
            callback: function (r) {

                const data = r.message || [];

                if (!data.length) {
                    $("#non_allocated_task_in_spr").html(
                        `<div class="text-center" style="padding:20px;">No Data Found</div>`
                    );
                    return;
                }

                const grouped = {};

                let grandET = 0;
                let grandRT = 0;
                let grandAT = 0;

                data.forEach(row => {

                    const project = row.project || "No Project";

                    if (!grouped[project]) {
                        grouped[project] = [];
                    }

                    grouped[project].push(row);

                    grandET += parseFloat(row.et || 0);
                    grandRT += parseFloat(row.rt || 0);
                    grandAT += parseFloat(row.at || 0);
                });

                let html = `
                <table class="table table-bordered" style="margin-bottom:0; table-layout:fixed; width:100%;">
                    <thead>
                        <tr style="background:#6c6a80;color:#fff;">

                            <th id="toggle-all-projects"
                                style="cursor:pointer;width:80px;min-width:80px;white-space:nowrap;">
                                + ALL
                            </th>

                            <th style="width:70px;min-width:70px;white-space:nowrap;">Sprint</th>

                            <th style="width:70px;min-width:70px;white-space:nowrap;">Task</th>

                            <th style="width:350px;min-width:350px;white-space:nowrap;">Subject</th>

                            <th style="width:50px;min-width:50px;white-space:nowrap;">ET</th>

                            <th style="width:50px;min-width:50px;white-space:nowrap;">RT</th>

                            <th style="width:50px;min-width:50px;white-space:nowrap;">AT</th>

                            <th style="width:50px;min-width:50px;white-space:nowrap;">AGE</th>

                            <th style="width:50px;min-width:50px;white-space:nowrap;">CF</th>

                            <th style="width:70px;min-width:70px;white-space:nowrap;">Priority</th>

                            <th style="width:70px;min-width:70px;white-space:nowrap;">Status</th>

                        </tr>
                    </thead>
                    <tbody>
                `;

                Object.keys(grouped)
                    .sort()
                    .forEach(project => {

                        const projectRows = grouped[project];

                        let projectET = 0;
                        let projectRT = 0;
                        let projectAT = 0;

                        projectRows.forEach(row => {
                            projectET += parseFloat(row.et || 0);
                            projectRT += parseFloat(row.rt || 0);
                            projectAT += parseFloat(row.at || 0);
                        });

                        const safeProject = project.replace(/[^a-zA-Z0-9]/g, "_");

                        // Project Header Row

                        html += `
                        <tr class="project-row"
                            data-project="${safeProject}"
                            style="
                                background:#85819e;
                                color:#fff;
                                font-weight:bold;
                                cursor:pointer;
                            ">
                            
                            <td colspan="4" style="text-align:left;">
                                <span class="toggle-icon">+</span>
                                ${project}
                            </td>

                            <td>${projectET.toFixed(2)}</td>
                            <td>${projectRT.toFixed(2)}</td>
                            <td>${projectAT.toFixed(2)}</td>

                            <td colspan="4"></td>

                        </tr>
                    `;

                        projectRows.forEach((row, idx) => {

                            const age = parseFloat(row.age || 0);

                            html += `
                            <tr class="task-row task-${safeProject}"
                                style="
                                    display:none;
                                    background:${idx % 2 === 0 ? '#ffffff' : '#e7e6ec'};
                                    color:${age > 3 ? 'red' : 'black'};
                                    font-weight:${age > 3 ? 'bold' : 'normal'};
                                ">

                                <td ">${row.cb || ""}</td>

                                <td style="text-align:left;">${row.sprint || ""}</td>

                                <td style="text-align:left;">
                                    <a href="/app/task/${row.task}"
                                    target="_blank"
                                    style="color:inherit;text-decoration:none;">
                                        ${row.task}
                                    </a>
                                </td>

                                <td style="text-align:left;">${row.subject || ""}</td>

                                <td>${parseFloat(row.et || 0).toFixed(2)}</td>
                                <td>${parseFloat(row.rt || 0).toFixed(2)}</td>
                                <td>${parseFloat(row.at || 0).toFixed(2)}</td>

                                <td>${row.age || 0}</td>
                                <td>${row.cf || ""}</td>
                                <td>${row.priority || ""}</td>
                                <td>${row.status || ""}</td>

                            </tr>
                            `;


                        });
                    });

                html += `
                <tr style="
                    background:#d9d9d9;
                    font-weight:bold;
                ">

                    <td colspan="4" style="text-align:left;">
                        GRAND TOTAL
                    </td>

                    <td>${grandET.toFixed(2)}</td>
                    <td>${grandRT.toFixed(2)}</td>
                    <td>${grandAT.toFixed(2)}</td>

                    <td colspan="4"></td>

                </tr>
                `;

                html += `
                    </tbody>
                </table>
            `;

                $("#non_allocated_task_in_spr").html(html);

                bind_non_allocated_events();
            }
        });
    }


    function bind_non_allocated_events() {

        let allExpanded = false;

        $("#toggle-all-projects")
            .off("click")
            .on("click", function () {

                allExpanded = !allExpanded;

                if (allExpanded) {

                    $(".task-row").show();

                    $(".project-row .toggle-icon").text("-");

                    $(this).text("- ALL");

                } else {

                    $(".task-row").hide();

                    $(".project-row .toggle-icon").text("+");

                    $(this).text("+ ALL");
                }
            });

        $(".project-row")
            .off("click")
            .on("click", function () {

                const project = $(this).data("project");

                const rows = $(".task-" + project);

                const icon = $(this).find(".toggle-icon");

                if (rows.is(":visible")) {

                    rows.hide();
                    icon.text("+");

                } else {

                    rows.show();
                    icon.text("-");
                }
            });
    }


    // Call on page load
    load_non_allocated_tasks_in_live_sprint();


    function toggleCBRowsFromOutside(cbId) {

        let $container = $("#today-task-table-container");

        const $rows = $container.find("." + cbId);

        if ($rows.length === 0) {
            // console.warn("No rows found for:", cbId);
            return;
        }

        if ($rows.is(":visible")) {
            $rows.hide();
        } else {
            $rows.show();
        }

    }


    $("#kt_confirmed_filter").off("change").on("change", function () {
        getNonAllocatedTasksNew();
    });




    let grouped = {};

    function getNonAllocatedTasksNew() {
        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.get_non_allocated_tasks",
            args: {},
            callback: function (r) {
                let $container = $("#non_allocated_task_table_new");

                if (!(r.message && r.message.data && r.message.data.length)) {
                    $container.html("<p>No tasks found.</p>");
                    return;
                }

                const tasks = r.message.data;

                // Filter tasks
                const today = frappe.datetime.get_today();
                const filtered = tasks.filter(task =>
                    ["Open", "Working"].includes(task.status) &&
                    task.custom_production_date !== today &&
                    task.service === "IT-SW"
                );

                // Sort by Project alphabetically
                filtered.sort((a, b) => (a.project || "").localeCompare(b.project || ""));

                // Group by project
                grouped = {}; // assign to global variable
                filtered.forEach(task => {
                    const project = task.project || "No Project";
                    if (!grouped[project]) grouped[project] = [];
                    grouped[project].push(task);
                });

                // Build HTML table
                let html = `
            <table class="table table-bordered" style="width:100%; text-align:center; border:1px solid #ccc; border-collapse: collapse;">
                <thead style="background:#0F1568; color:white;">
                    <tr>
                        <th style="cursor:pointer;" id="toggle-all-projects">+ ALL</th>
                        <th>Sprint</th>
                        <th>Task</th>
                        <th>Subject</th>
                        <th>ET</th>
                        <th>RT</th>
                        <th>AT</th>
                        <th>AGE</th>
                        <th>CF</th>
                        <th>Priority</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>`;
                let grandET = 0;
                let grandRT = 0;
                let grandAT = 0;
                Object.keys(grouped).sort().forEach(project => {
                    const projectTasks = grouped[project];
                    const projectRowId = "proj-" + project.replace(/\s+/g, "_");

                    // Project header row styling
                    const projectBg = "#85819e";
                    const projectBorder = "1px solid #192b2c";
                    const projectColor = "#FFFFFF";

                    const totalET = projectTasks.reduce((sum, t) => {
                        return sum + (parseFloat(t.expected_time) || 0);
                    }, 0);
                    const totalRT = projectTasks.reduce((sum, t) => {
                        return sum + (parseFloat(t.rt) || 0);
                    }, 0);

                    const totalAT = projectTasks.reduce((sum, t) => {
                        return sum + (parseFloat(t.actual_time) || 0);
                    }, 0);

                    grandET += totalET;
                    grandRT += totalRT;
                    grandAT += totalAT;

                    html += `<tr class="project-row" data-target="${projectRowId}" 
                            style="cursor:pointer; font-weight:bold; background:${projectBg}; color:${projectColor}; border-bottom:${projectBorder};">

                            <td colspan="4" style="text-align:left; padding-left:10px;">
                                <span class="toggle-sign">+</span> ${project}
                            </td>

                            <td colspan="1" style="text-align:center;">
                                ${totalET.toFixed(2)}
                            </td>

                            <td colspan="1" style="text-align:center;">
                                ${totalRT.toFixed(2)}
                            </td>

                            <td colspan="1" style="text-align:center;">
                                ${totalAT.toFixed(2)}
                            </td>

                            <td colspan="4" style="text-align:right; padding-right:10px;">
                            </td>

                        </tr>`;

                    // Task rows


                    projectTasks.forEach((task, idx) => {

                        const bg = (idx % 2 === 0) ? "#FFFFFF" : "#e7e6ec";

                        let textColor = "#000000";

                        let ageValue = parseFloat(task.custom_age) || 0;
                        let status = (task.status || "").toLowerCase();

                        if (ageValue > 3) {
                            textColor = "#f54545";
                        }

                        html += `<tr class="task-row" data-parent="${projectRowId}" 
                                data-kt="${task.kt_confirmed ? 'Yes' : 'No'}"
                                style="display:none; background:${bg}; color:${textColor};">

                                <td>${task.cb || "No Cb"}</td> 
                                <td>${task.custom_sprint || ""}</td>
                                <td>
                                    <a href="/app/task/${task.name}" target="_blank">${task.name || ""}</a>
                                </td>
                                <td style="text-align:left;">${task.subject || ""}</td>
                                <td>${task.expected_time || ""}</td>
                                <td>${task.rt || ""}</td>
                                <td>${task.actual_time ? parseFloat(task.actual_time).toFixed(2) : ""}</td>
                                <td>${task.custom_age || ""}</td>
                                <td>${task.custom_production_date_count || ""}</td>
                                <td>${task.priority || ""}</td>
                                <td>${task.status || ""}</td>
                            </tr>`;

                        $("#kt_confirmed_filter").off("change").on("change", function () {

                            const selected = $(this).val();

                            $("#non_allocated_task_table_new .task-row").each(function () {

                                const ktValue = $(this).attr("data-kt");

                                if (!selected || selected === ktValue) {
                                    $(this).show();
                                } else {
                                    $(this).hide();
                                }

                            });
                        });

                    });

                });

                html += `
                    <tr style="
                        font-weight:bold;
                        background:#0F1568;
                        color:white;
                    ">
                        <td colspan="4" style="text-align:right;">
                            GRAND TOTAL
                        </td>

                        <td>${grandET.toFixed(2)}</td>
                        <td>${grandRT.toFixed(2)}</td>
                        <td>${grandAT.toFixed(2)}</td>

                        <td colspan="4"></td>
                    </tr>`;

                html += `</tbody></table>`;
                $container.html(html);

                // Toggle all projects
                let allExpanded = false;
                $("#toggle-all-projects").off("click").on("click", function () {
                    const $table = $("#non_allocated_task_table_new");
                    if (!allExpanded) {
                        $table.find(".task-row").show();
                        $table.find(".toggle-sign").text("-");
                        $(this).text("- ALL");
                        allExpanded = true;
                    } else {
                        $table.find(".task-row").hide();
                        $table.find(".toggle-sign").text("+");
                        $(this).text("+ ALL");
                        allExpanded = false;
                    }
                });


                $("#non_allocated_task_table_new .project-row").off("click").on("click", function () {
                    const target = $(this).data("target");
                    const $rows = $("#non_allocated_task_table_new .task-row[data-parent='" + target + "']");
                    const $sign = $(this).find(".toggle-sign");

                    if ($rows.is(":visible")) {
                        $rows.hide();
                        $sign.text("+");
                    } else {
                        $rows.show();
                        $sign.text("-");
                    }
                });
            }
        });
    }


    function load_amc_project_sla_table() {

        $("#amc_table").html(`
        <div style="
            padding:20px;
            text-align:center;
        ">
            Loading...
        </div>
    `);

        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.get_amc_project_sla_table",

            callback: function (r) {

                if (r.message) {

                    $("#amc_table").html(r.message);

                } else {

                    $("#amc_table").html(`
                    <div style="
                        padding:20px;
                        text-align:center;
                        color:red;
                    ">
                        No Data Found
                    </div>
                `);

                }
            }
        });
    }


    $(document).on("click", "#download-amc", function () {

        window.open(
            "/api/method/teampro.teampro.page.new_it_dashboard.new_it.download_amc_project_sla_excel"
        );

    });

    $(document).on("click", "#download-dsr", function () {

        let raw_date = $("#dsr_date_filter input").val();

        let selected_date = raw_date
            ? frappe.datetime.user_to_str(raw_date)
            : frappe.datetime.add_days(
                frappe.datetime.get_today(),
                -1
            );

        window.open(
            `/api/method/teampro.teampro.page.new_it_dashboard.new_it.download_dsr_excel?date=${selected_date}`
        );

    });


    frappe.ui.form.make_control({
        parent: document.querySelector("#dsr_date_filter"),
        df: {
            fieldtype: "Date",
            fieldname: "dsr_date_filter",
            placeholder: "Select Date",
            default: frappe.datetime.get_today(),
            change: function () {
                load_dsr_table();
            }
        },
        render_input: true
    });

    function load_dsr_table() {

        // Get displayed date
        let raw_date = $("#dsr_date_filter input").val();


        // Convert DD-MM-YYYY -> YYYY-MM-DD
        let selected_date = frappe.datetime.str_to_user(raw_date)
            ? frappe.datetime.user_to_str(raw_date)
            : raw_date;


        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.dsr_table",
            args: {
                date: selected_date
            },
            callback: function (r) {

                $("#dsr_table").html(
                    r.message || `
                    <div style="
                        padding:20px;
                        text-align:center;
                        color:red;
                    ">
                        No Data Found
                    </div>
                `
                );

            }
        });
    }

    // Initial Load
    setTimeout(() => {
        load_dsr_table();
    }, 500);


    function downloadCSV(filename, rows) {
        const csvContent = rows.map(e => e.map(a => `"${a}"`).join(",")).join("\n");
        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }

    // Download button click handler
    // $("#download-non-allocated").off("click").on("click", function () {
    //     if (!grouped || Object.keys(grouped).length === 0) {
    //         frappe.msgprint("No data available to download");
    //         return;
    //     }

    //     const rows = [];
    //     rows.push(["Project","CB", "Sprint", "Task", "Subject", "ET", "RT","AT", "Priority", "Status"]);

    //     Object.keys(grouped).sort().forEach(project => {
    //         const projectTasks = grouped[project];
    //         projectTasks.forEach(task => {
    //             rows.push([
    //                 project,
    //                 task.cb || "",
    //                 task.custom_sprint || "",
    //                 task.name || "",
    //                 task.subject || "",
    //                 task.expected_time || "",
    //                 task.rt || "" ,
    //                 task.actual_time ? parseFloat(task.actual_time).toFixed(2) : "",
    //                 task.priority || "",
    //                 task.status || ""
    //             ]);
    //         });
    //     });

    //     downloadCSV("NonAllocatedTasks.csv", rows);
    // });

    $("#download-non-allocated_in_spr").off("click").on("click", function () {

        if (!grouped || Object.keys(grouped).length === 0) {
            frappe.msgprint("No data available to download");
            return;
        }

        let rows = [];

        // HEADER
        rows.push([
            "Project",
            "CB",
            "Sprint",
            "Task",
            "Subject",
            "ET",
            "RT",
            "AT",
            "AGE",
            "CF",
            "Priority",
            "Status"
        ]);

        let grandET = 0;
        let grandRT = 0;
        let grandAT = 0;

        Object.keys(grouped).forEach(project => {

            grouped[project].forEach(row => {

                const et = parseFloat(row.et || 0);
                const rt = parseFloat(row.rt || 0);
                const at = parseFloat(row.at || 0);

                grandET += et;
                grandRT += rt;
                grandAT += at;

                rows.push([
                    project,
                    row.cb || "",
                    row.custom_sprint || "",
                    row.name || "",
                    row.subject || "",
                    et,
                    rt,
                    at,
                    row.custom_age || "",
                    row.custom_production_date_count || "",
                    row.priority || "",
                    row.status || ""
                ]);
            });
        });

        // GRAND TOTAL ROW
        rows.push([
            "GRAND TOTAL",
            "",
            "",
            "",
            grandET.toFixed(2),
            grandRT.toFixed(2),
            grandAT.toFixed(2),
            "",
            "",
            "",
            ""
        ]);

        // CREATE EXCEL
        let ws = XLSX.utils.aoa_to_sheet(rows);
        let wb = XLSX.utils.book_new();

        XLSX.utils.book_append_sheet(wb, ws, "Non Allocated Tasks");

        XLSX.writeFile(wb, "NonAllocatedTasks.xlsx");
    });

    $("#download-non-allocated").off("click").on("click", function () {

        if (!grouped || Object.keys(grouped).length === 0) {
            frappe.msgprint("No data available to download");
            return;
        }

        const ktFilter = $("#kt_confirmed_filter").val();

        const rows = [];
        let totalET = 0;
        let totalRT = 0;
        let totalAT = 0;

        rows.push([
            "Project",
            "CB",
            "Sprint",
            "Task",
            "Subject",
            "ET",
            "RT",
            "AT",
            "AGE",
            "CF",
            "Priority",
            "Status"
        ]);

        Object.keys(grouped).sort().forEach(project => {

            const projectTasks = grouped[project];

            projectTasks.forEach(task => {

                // Apply same filter used in UI
                if (ktFilter === "Yes" && !task.kt_confirmed) {
                    return;
                }

                if (ktFilter === "No" && task.kt_confirmed) {
                    return;
                }
                totalET += parseFloat(task.expected_time || 0);
                totalRT += parseFloat(task.rt || 0);
                totalAT += parseFloat(task.actual_time || 0);


                rows.push([
                    project,
                    task.cb || "",
                    task.custom_sprint || "",
                    task.name || "",
                    task.subject || "",
                    task.expected_time || "",
                    task.rt || "",
                    task.actual_time
                        ? parseFloat(task.actual_time).toFixed(2)
                        : "",
                    task.custom_age || "",
                    task.custom_production_date_count || "",
                    task.priority || "",
                    task.status || ""
                ]);
            });
        });


        rows.push([
            "TOTAL",
            "",
            "",
            "",
            "",
            totalET.toFixed(2),
            totalRT.toFixed(2),
            totalAT.toFixed(2),
            "",
            "",
            "",
            ""
        ]);

        downloadCSV("NonAllocatedTasks.csv", rows);
    });

    $(document).ready(function () {
        getNonAllocatedTasksNew();
    });



    function load_opportunity_table() {
        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.get_opportunity_table",
            callback: function (r) {
                if (r.message) {
                    document.getElementById("opp_table").innerHTML = r.message;
                }
            }
        });
    }


    function load_retro_summary_html(sprint) {
        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.get_retro_summary_html_test",
            args: {
                name: sprint
            },
            callback: function (r) {
                const data = r.message || [];
                $('#retro-summary-html').html('');
                data.forEach(section => {
                    $('#retro-summary-html').append(`
                <div class="team-section" style="padding: 0 30px;">
                    <h4>${section.team}</h4>
                    ${section.html}
                    <hr>
                </div>
            `);
                });
            }
        });
    }

    function load_retro_summary(sprint) {
        frappe.call({
            method: "teampro.teampro.page.new_it_dashboard.new_it.summary_total",
            args: {
                name: sprint
            },
            callback: function (r) {
                if (r.message) {
                    $('#retro-summary-html').html(r.message);
                } else {
                    $('#retro-summary-html').html("No Data Found");
                }
            }
        });
    }


    frappe.call({
        method: "teampro.teampro.page.new_it_dashboard.new_it.get_tasks_project_pivot",
        callback: function (r) {
            const data = r.message || [];
            // pivotData = data;   
            // renderPivotTable(pivotData);

            let pivot_html = `
<style>
    #pivot-summary {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-family: Arial, sans-serif;
        font-size: 12px;
    }
    #pivot-summary th, #pivot-summary td {
        border: 1px solid #444;
        padding: 6px 10px;
        text-align: center;
        white-space: nowrap;
    }
    #pivot-summary thead th {
        background-color: #2a4d69;
        color: white;
    }
    #pivot-summary tbody tr:nth-child(odd) {
        background-color: #FFFFFF;   /* white */
        color: #000000;              /* black text */
    }

    #pivot-summary tbody tr:nth-child(even) {
        background-color: #e7e6ec;   /* light mild blue */
        color: #000000;              /* black text */
    }
    .left-align {
        text-align: left;
    }
        .psr-toggle.active{
    background:#0F1568 !important;
    color:#fff !important;
}
</style>



<div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;">
    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:white;
    border-bottom:1px solid #ddd;
    padding:5px 10px;
">
    
    <h4 style="
        margin:0;
        
    ">
        PROJECT STATUS REPORT(PSR) 
    </h4>
     <style>
.psr-toggle.active{
    background:#0F1568 !important;
    color:white !important;
    border-radius:4px;
}
</style>
<span class="psr-toggle active" data-view="overall"
      style="padding:4px 10px;border:1px solid #ccc;cursor:pointer;">
    Overall
</span>

<span class="psr-toggle" data-view="current"
      style="padding:4px 10px;border:1px solid #ccc;cursor:pointer;">
    Current
</span>
    <button 
    id="download-psr-btn"
    style="border:none;background:none;outline:none;padding:0;cursor:pointer;">
    <img 
        src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
        style="width:22px;height:22px;"
    >
</button>

</div>      <table id="pivot-summary">
        <thead>
            <tr class="sticky-top">
                <th>S. No</th>
                <th>Project Name</th>
                <th>Project<br>Type</th>
                <th>Open<br>(hr/ #)</th>
                <th>W<br>(hr/ #)</th>
                <th>PR<br>(hr/ #)</th>
                <th>CR<br>(hr/ #)</th>
            </tr>
        </thead>
        <tbody>
`;

            let total_open_hours = 0, total_open_tasks = 0;
            let total_working_hours = 0, total_working_tasks = 0;
            let total_pr_hours = 0, total_pr_tasks = 0;
            let total_cr_hours = 0, total_cr_tasks = 0;

            let td_total_open_hours = 0, td_total_open_tasks = 0;
            let td_total_working_hours = 0, td_total_working_tasks = 0;
            let td_total_pr_hours = 0, td_total_pr_tasks = 0;
            let td_total_cr_hours = 0, td_total_cr_tasks = 0;

            data.forEach(row => {
                const [open_hr, open_task] = row.open.split("/").map(Number);
                const [open_td_hr, open_td_task] = row.open_td.split("/").map(Number);

                const [work_hr, work_task] = row.working.split("/").map(Number);
                const [work_td_hr, work_td_task] = row.working_td.split("/").map(Number);

                const [pr_hr, pr_task] = row.pr.split("/").map(Number);
                const [pr_td_hr, pr_td_task] = row.pr_td.split("/").map(Number);

                const [cr_hr, cr_task] = row.cr.split("/").map(Number);
                const [cr_td_hr, cr_td_task] = row.cr_td.split("/").map(Number);
                pivot_html += `
            <tr>
                <td>${row.s_no}</td>
                <td class="left-align">
                    <a href="/app/project/${row.project}" target="_blank">
                        ${row.project}
                    </a>
                    </td>       
                <td class="left-align">${row.project_type}</td>
<td>${open_hr.toFixed(2)}/${open_task}</td>

<td>
    <span class="overall-col">${work_hr.toFixed(2)}/${work_task}</span>
    <span class="current-col" style="display:none;color:">
        ${work_td_hr.toFixed(2)}/${work_td_task}
    </span>
</td>

<td>
    <span class="overall-col">${pr_hr.toFixed(2)}/${pr_task}</span>
    <span class="current-col" style="display:none;color:">
        ${pr_td_hr.toFixed(2)}/${pr_td_task}
    </span>
</td>

<td>
    <span class="overall-col">${cr_hr.toFixed(2)}/${cr_task}</span>
    <span class="current-col" style="display:none;color:">
        ${cr_td_hr.toFixed(2)}/${cr_td_task}
    </span>
</td>
               
            </tr>`;



                total_open_hours += open_hr;
                total_open_tasks += open_task;
                total_working_hours += work_hr;
                total_working_tasks += work_task;
                total_pr_hours += pr_hr;
                total_pr_tasks += pr_task;
                total_cr_hours += cr_hr;
                total_cr_tasks += cr_task;

                td_total_open_hours += open_td_hr;
                td_total_open_tasks += open_td_task;
                td_total_working_hours += work_td_hr;
                td_total_working_tasks += work_td_task;
                td_total_pr_hours += pr_td_hr;
                td_total_pr_tasks += pr_td_task;
                td_total_cr_hours += cr_td_hr;
                td_total_cr_tasks += cr_td_task;
            });

            pivot_html += `
<tr style="font-weight:bold; background-color:#0F1568; color:white;">

    <td colspan="3" style="text-align:center;">
        Total
    </td>

    <td>
        ${total_open_hours.toFixed(2)}/${total_open_tasks}
    </td>

    <td>
        <span class="overall-col">
            ${total_working_hours.toFixed(2)}/${total_working_tasks}
        </span>

        <span class="current-col" style="display:none;color:white;">
            ${td_total_working_hours.toFixed(2)}/${td_total_working_tasks}
        </span>
    </td>

    <td>
        <span class="overall-col">
            ${total_pr_hours.toFixed(2)}/${total_pr_tasks}
        </span>

        <span class="current-col" style="display:none;color:white;">
            ${td_total_pr_hours.toFixed(2)}/${td_total_pr_tasks}
        </span>
    </td>

    <td>
        <span class="overall-col">
            ${total_cr_hours.toFixed(2)}/${total_cr_tasks}
        </span>

        <span class="current-col" style="display:none;color:white;">
            ${td_total_cr_hours.toFixed(2)}/${td_total_cr_tasks}
        </span>
    </td>

</tr>`;

            pivot_html += `</tbody></table>`;

            $("#pivot-project-summary-container").html(pivot_html);
            // Default state
            $(".current-col").hide();
            $(".overall-col").show();
            

            $(document).off("click", ".psr-toggle");

            $(document).on("click", ".psr-toggle", function () {

                $(".psr-toggle").removeClass("active");
                $(this).addClass("active");

                console.log("clicked", $(this).text());

                let view = $(this).data("view");

                if (view === "overall") {
                    $(".overall-col").show();
                    $(".current-col").hide();
                } else {
                    $(".overall-col").hide();
                    $(".current-col").show();
                }
            });

        }


    });



//     function renderPivotTable(data) {

//         let pivot_html = `
// <style>
//     #pivot-summary {
//         width: 100%;
//         border-collapse: collapse;
//         margin-top: 10px;
//         font-family: Arial, sans-serif;
//         font-size: 12px;
//     }
//     #pivot-summary th, #pivot-summary td {
//         border: 1px solid #444;
//         padding: 6px 10px;
//         text-align: center;
//         white-space: nowrap;
//     }
//     #pivot-summary thead th {
//         background-color: #2a4d69;
//         color: white;
//     }
//     #pivot-summary tbody tr:nth-child(odd) {
//         background-color: #FFFFFF;   /* white */
//         color: #000000;              /* black text */
//     }

//     #pivot-summary tbody tr:nth-child(even) {
//         background-color: #e7e6ec;   /* light mild blue */
//         color: #000000;              /* black text */
//     }
//     .left-align {
//         text-align: left;
//     }
// </style>

// <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;">
//     <div style="
//     display:flex;
//     justify-content:space-between;
//     align-items:center;
//     background:white;
//     border-bottom:1px solid #ddd;
//     padding:5px 10px;
// ">
    
//     <h4 style="
//         margin:0;
        
//     ">
//         PROJECT STATUS REPORT(PSR)
//     </h4>
//  <div style="display:flex; gap:8px;">
            
//             <span class="filter-btn" data-group="priority" data-filter="Low">Overall</span>
//             <span class="filter-btn" data-group="priority" data-filter="Medium">Current</span>
//         </div>
//     <button 
//     id="download-psr-btn"
//     style="border:none;background:none;outline:none;padding:0;cursor:pointer;">
//     <img 
//         src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
//         style="width:22px;height:22px;"
//     >
// </button>

// </div>  
//     <table id="pivot-summary">
//         <thead>
//             <tr class="sticky-top">
//                 <th>S. No</th>
//                 <th>Project Name</th>
//                 <th>Project<br>Type</th>
//                 <th>Open<br>(hr/ #)</th>
//                 <th>TD Open<br>(hr/ #)</th>
//                 <th>W<br>(hr/ #)</th>
//                 <th>TD W<br>(hr/ #)</th>
//                 <th>PR<br>(hr/ #)</th>
//                 <th>TD PR<br>(hr/ #)</th>
//                 <th>CR<br>(hr/ #)</th>
//                 <th>TD CR<br>(hr/ #)</th>
//             </tr>
//         </thead>
//         <tbody>
// `;
//         let total_open_hr = 0, total_open_task = 0;
//         let total_open_td_hr = 0, total_open_td_task = 0;

//         let total_work_hr = 0, total_work_task = 0;
//         let total_work_td_hr = 0, total_work_td_task = 0;

//         let total_pr_hr = 0, total_pr_task = 0;
//         let total_pr_td_hr = 0, total_pr_td_task = 0;

//         let total_cr_hr = 0, total_cr_task = 0;
//         let total_cr_td_hr = 0, total_cr_td_task = 0;
//         data.forEach(row => {
//             const [open_hr, open_task] = row.open.split("/").map(Number);
//             const [open_td_hr, open_td_task] = row.open_td.split("/").map(Number);

//             const [work_hr, work_task] = row.working.split("/").map(Number);
//             const [work_td_hr, work_td_task] = row.working_td.split("/").map(Number);

//             const [pr_hr, pr_task] = row.pr.split("/").map(Number);
//             const [pr_td_hr, pr_td_task] = row.pr_td.split("/").map(Number);

//             const [cr_hr, cr_task] = row.cr.split("/").map(Number);
//             const [cr_td_hr, cr_td_task] = row.cr_td.split("/").map(Number);

//             total_open_hr += open_hr;
//             total_open_task += open_task;

//             total_open_td_hr += open_td_hr;
//             total_open_td_task += open_td_task;

//             total_work_hr += work_hr;
//             total_work_task += work_task;

//             total_work_td_hr += work_td_hr;
//             total_work_td_task += work_td_task;

//             total_pr_hr += pr_hr;
//             total_pr_task += pr_task;

//             total_pr_td_hr += pr_td_hr;
//             total_pr_td_task += pr_td_task;

//             total_cr_hr += cr_hr;
//             total_cr_task += cr_task;

//             total_cr_td_hr += cr_td_hr;
//             total_cr_td_task += cr_td_task;

//             pivot_html += `
//         <tr>
//             <td>${row.s_no}</td>
//             <td class="left-align">
//                 <a href="/app/project/${row.project}" target="_blank">
//                     ${row.project}
//                 </a>
//             </td>
//             <td class="left-align">${row.project_type}</td>

//             <td>${open_hr.toFixed(2)}/${open_task}</td>
//             <td style="color:">${open_td_hr.toFixed(2)}/${open_td_task}</td>

//             <td>${work_hr.toFixed(2)}/${work_task}</td>
//             <td style="color:">${work_td_hr.toFixed(2)}/${work_td_task}</td>

//             <td>${pr_hr.toFixed(2)}/${pr_task}</td>
//             <td style="color:">${pr_td_hr.toFixed(2)}/${pr_td_task}</td>

//             <td>${cr_hr.toFixed(2)}/${cr_task}</td>
//             <td style="color:">${cr_td_hr.toFixed(2)}/${cr_td_task}</td>
//         </tr>`;
//         });

//         pivot_html += `
//             <tr style="font-weight:bold;background:#0F1568;color:white;">
//                 <td colspan="3">Total</td>

//                 <td>${total_open_hr.toFixed(2)}/${total_open_task}</td>
//                 <td style="color:">${total_open_td_hr.toFixed(2)}/${total_open_td_task}</td>

//                 <td>${total_work_hr.toFixed(2)}/${total_work_task}</td>
//                 <td style="color:">${total_work_td_hr.toFixed(2)}/${total_work_td_task}</td>

//                 <td>${total_pr_hr.toFixed(2)}/${total_pr_task}</td>
//                 <td style="color:">${total_pr_td_hr.toFixed(2)}/${total_pr_td_task}</td>

//                 <td>${total_cr_hr.toFixed(2)}/${total_cr_task}</td>
//             </tr>

//             </tbody>
//             </table>`;

//         pivot_html += `</tbody></table>`;
//         $("#pivot-project-summary-container").html(pivot_html);
//     }


    function renderPivotTable(data) {

    let pivot_html = `
<style>
    #pivot-summary {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-family: Arial, sans-serif;
        font-size: 12px;
    }
    #pivot-summary th, #pivot-summary td {
        border: 1px solid #444;
        padding: 6px 10px;
        text-align: center;
        white-space: nowrap;
    }
    #pivot-summary thead th {
        background-color: #2a4d69;
        color: white;
    }
    #pivot-summary tbody tr:nth-child(odd) {
        background-color: #FFFFFF;   /* white */
        color: #000000;              /* black text */
    }

    #pivot-summary tbody tr:nth-child(even) {
        background-color: #e7e6ec;   /* light mild blue */
        color: #000000;              /* black text */
    }
    .left-align {
        text-align: left;
    }
    .psr-toggle.active{
        background:#0F1568 !important;
        color:#fff !important;
    }
</style>

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;">
    <div style="display:flex; justify-content:space-between; align-items:center; background:white; border-bottom:1px solid #ddd; padding:5px 10px;">
        <h4 style="margin:0;">
            PROJECT STATUS REPORT(PSR)
        </h4>
        <style>
            .psr-toggle.active{
                background:#0F1568 !important;
                color:white !important;
                border-radius:4px;
            }
        </style>
        <div style="display:flex; gap:8px;">
            <span class="psr-toggle active" data-view="overall" style="cursor:pointer; padding:2px 8px;">
                Overall
            </span>
            <span class="psr-toggle" data-view="current" style="cursor:pointer; padding:2px 8px;">
                Current
            </span>
            <button id="download-psr-btn" style="border:none;background:none;outline:none;padding:0;cursor:pointer;">
                <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png" style="width:22px;height:22px;">
            </button>
        </div>
    </div>  
    <table id="pivot-summary">
        <thead>
            <tr class="sticky-top">
                <th>S. No</th>
                <th>Project Name</th>
                <th>Project<br>Type</th>
                <th>Open<br>(hr/ #)</th>
                <th>W<br>(hr/ #)</th>
                <th>PR<br>(hr/ #)</th>
                <th>CR<br>(hr/ #)</th>
            </tr>
        </thead>
        <tbody>
`;

    let total_open_hr = 0, total_open_task = 0;
    let total_open_td_hr = 0, total_open_td_task = 0;

    let total_work_hr = 0, total_work_task = 0;
    let total_work_td_hr = 0, total_work_td_task = 0;

    let total_pr_hr = 0, total_pr_task = 0;
    let total_pr_td_hr = 0, total_pr_td_task = 0;

    let total_cr_hr = 0, total_cr_task = 0;
    let total_cr_td_hr = 0, total_cr_td_task = 0;

    data.forEach((row, index) => {
        const [open_hr, open_task] = row.open.split("/").map(Number);
        const [open_td_hr, open_td_task] = row.open_td.split("/").map(Number);

        const [work_hr, work_task] = row.working.split("/").map(Number);
        const [work_td_hr, work_td_task] = row.working_td.split("/").map(Number);

        const [pr_hr, pr_task] = row.pr.split("/").map(Number);
        const [pr_td_hr, pr_td_task] = row.pr_td.split("/").map(Number);

        const [cr_hr, cr_task] = row.cr.split("/").map(Number);
        const [cr_td_hr, cr_td_task] = row.cr_td.split("/").map(Number);

        total_open_hr += open_hr;
        total_open_task += open_task;

        total_open_td_hr += open_td_hr;
        total_open_td_task += open_td_task;

        total_work_hr += work_hr;
        total_work_task += work_task;

        total_work_td_hr += work_td_hr;
        total_work_td_task += work_td_task;

        total_pr_hr += pr_hr;
        total_pr_task += pr_task;

        total_pr_td_hr += pr_td_hr;
        total_pr_td_task += pr_td_task;

        total_cr_hr += cr_hr;
        total_cr_task += cr_task;

        total_cr_td_hr += cr_td_hr;
        total_cr_td_task += cr_td_task;

        pivot_html += `
        <tr>
            <td>${index + 1}</td>
            <td class="left-align">
                <a href="/app/project/${row.project}" target="_blank">
                    ${row.project}
                </a>
            </td>
            <td class="left-align">${row.project_type}</td>

            <td>${open_hr.toFixed(2)}/${open_task}</td>

            <td>
                <span class="overall-col">${work_hr.toFixed(2)}/${work_task}</span>
                <span class="current-col" style="display:none;">
                    ${work_td_hr.toFixed(2)}/${work_td_task}
                </span>
            </td>

            <td>
                <span class="overall-col">${pr_hr.toFixed(2)}/${pr_task}</span>
                <span class="current-col" style="display:none;">
                    ${pr_td_hr.toFixed(2)}/${pr_td_task}
                </span>
            </td>

            <td>
                <span class="overall-col">${cr_hr.toFixed(2)}/${cr_task}</span>
                <span class="current-col" style="display:none;">
                    ${cr_td_hr.toFixed(2)}/${cr_td_task}
                </span>
            </td>
        </tr>`;
    });

    pivot_html += `
        <tr style="font-weight:bold;background:#0F1568;color:white;">
            <td colspan="3">Total</td>

            <td>${total_open_hr.toFixed(2)}/${total_open_task}</td>

            <td>
                <span class="overall-col">
                    ${total_work_hr.toFixed(2)}/${total_work_task}
                </span>

                <span class="current-col" style="display:none;color:white;">
                    ${total_work_td_hr.toFixed(2)}/${total_work_td_task}
                </span>
            </td>

            <td>
                <span class="overall-col">
                    ${total_pr_hr.toFixed(2)}/${total_pr_task}
                </span>

                <span class="current-col" style="display:none;color:white;">
                    ${total_pr_td_hr.toFixed(2)}/${total_pr_td_task}
                </span>
            </td>

            <td>
                <span class="overall-col">
                    ${total_cr_hr.toFixed(2)}/${total_cr_task}
                </span>

                <span class="current-col" style="display:none;color:white;">
                    ${total_cr_td_hr.toFixed(2)}/${total_cr_td_task}
                </span>
            </td>
        </tr>
    </tbody>
</table>
</div>`;

    $("#pivot-project-summary-container").html(pivot_html);
    
    // Default visibility toggles
    $(".current-col").hide();
    $(".overall-col").show();

    $(document).off("click", ".psr-toggle");
    $(document).on("click", ".psr-toggle", function () {
        $(".psr-toggle").removeClass("active");
        $(this).addClass("active");

        let view = $(this).data("view");
        if (view === "overall") {
            $(".overall-col").show();
            $(".current-col").hide();
        } else {
            $(".overall-col").hide();
            $(".current-col").show();
        }
    });
}




    $(document).on("click", "#download-psr-btn", function () {

        let project_list = [];

        $("#pivot-summary tbody tr").each(function () {

            let project = $(this).find("td:eq(1) a").text().trim();

            if (project) {
                project_list.push(project);
            }
        });

        window.open(
            frappe.urllib.get_full_url(
                "/api/method/teampro.teampro.page.new_it_dashboard.new_it.download"
                + "?projects=" + encodeURIComponent(JSON.stringify(project_list))
            )
        );

    });





    frappe.call({
        method: "teampro.teampro.page.new_it_dashboard.new_it.get_tasks_project_pivot",
        callback: function (r) {

            const data = r.message || [];

            pivotData = data;

            renderPivotTable(pivotData);  // ONLY THIS
        }
    });


}



