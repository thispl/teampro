frappe.pages['dnd-dashboard'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: '',
        single_column: true
    });








    const style = document.createElement('style');
    style.innerHTML = `
   
    .monitor-toggle-card.btn-outline-primary:hover {
    background-color: #3399FF !important;
    color: white !important;
    border-color: #3399FF !important;
}

#select-all-cards:hover{


    background-color: #3399FF !important;
    color: white !important;
    border-color: #3399FF !important;


}

#all_download:hover{

 background-color: #3399FF !important;
    color: white !important;
    border-color: #3399FF !important;



}
    
    .top-actions {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
        align-items: center;
        margin-top: -40px;
        margin-right: 20px;
    }
    .dashboard-cards-finaince {
        padding: 15px;
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    min-width: 150px;
    flex-shrink: 0;
    }
    .dashboard-card {
        width: 190px;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        flex-shrink: 0;
    }
    .card-inner {
        background-color: white;
        padding: 20px 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .card-inner h3 {
        margin: 0;
        font-size: 17px;
        font-weight: bold;
        color: #222;
        text-align: center;
        white-space: normal;
    }
    .card-inner .amount {
        font-size: 22px;
        font-weight: bold;
        color: green;
        margin-top: 10px;
        text-align: center;
    }
      .monitor-toggle-card.selected-card {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    transform: scale(1.05);
    transition: all 0.2s ease-in-out;
    background-color: #000000 !important;  /* black background */
    color: #ffffff !important;             /* white text */
    border-color: #000000 !important;      /* match border */
    font-weight: bold;
}

        
`;
    document.head.appendChild(style);
    style.innerHTML += `
    @keyframes cardPop {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.05);
            opacity: 0.8;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    .pop-blink {
        animation: cardPop 0.3s ease-in-out;
    }
        #select-all-cards.selected-card {
        background-color: black !important;
        color: white !important;
        border-color: black !important;
        font-weight: bold;
    }
    #deselect-all-cards.selected-card {
        background-color: red !important;
        color: white !important;
        border-color: red !important;
        font-weight: bold;
    }
        
`;
    $(wrapper).html(`
        <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>

        <div class="dashboard-wrapper" style="margin-bottom:100px;">
            <div style="position: relative; padding: 10px;">
                <h2 style="text-align: center; font-weight: bold; margin: 0;">DND DASHBOARD</h2>
                <div id="current-datetime" style="font-size: 16px; color: #666; text-align: center; margin-top: 5px;"></div>
            </div>
            <div id="rec-i-metrics-cards" style="display: flex; justify-content:space-around; gap: 10px; margin: 30px 20px 0; flex-wrap: nowrap;background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;">
                <div class="dashboard-card teampro-closure-count-card" style="background-color: #007BFF; width:11%; height:125px; "></div>
                <div class="dashboard-card candidate-agent-closure-count-card" style="background-color: #6C757D; width:11%; height:125px; "></div>
                <div class="dashboard-card agent-closure-count-card" style="background-color: #8c7bf4ff; width:11%; height:125px; "></div>
                <div class="dashboard-card supp-closure-count-card" style="background-color: #5ee274ff; width:11%; height:125px; "></div>
                <div class="dashboard-card client-closure-count-card" style="background-color: #17A2B8; width:11%; height:125px; "></div>
                <div class="dashboard-card so_pending" style="background-color: #171fb8ff; width:11%; height:125px; "></div>
                <div class="dashboard-card nepal-closure-count-card" style="background-color: #e9ff40ff; width:11%; height:125px; "></div>
                <div class="dashboard-card srilanka-closure-count-card" style="background-color: #f079f9ff; width:11%; height:125px; "></div>
                
            </div>

            <div id="closure-matrix-container" style="margin: 40px 20px;border: 1px solid #ddd; border-radius: 8px;background-color: #f5f5f5;margin-left:20px;margin-right:20px;">
            
                <h4 style="margin-bottom: 10px; text-align:left; margin-left:10px; margin-right:10px;  margin-top:15px; position: relative;">
                   TERRITORY-WISE CLOSURE STATUS

                <div style="position: absolute; top: -5px; right: 10px; z-index: 10;">
                <button id="download-closure-table" style="background-color:black; color:white;" class="btn btn-secondary">Download</button> 
                </div>
                

                <div id="closure-matrix-table" style="margin-top: 0px;"></div>
                    
            </div>

            <div id="closure-matrix-container"
                    style="margin:40px 20px;border:1px solid #ddd;border-radius:8px;background-color:#f5f5f5;">
                    <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 15px;flex-wrap:nowrap;">
                        <h4 style="margin:0;white-space:nowrap;">
                            Candidate Project Summary (Task / Candidate)
                        </h4>
                        <div style="display:flex;align-items:center;gap:15px;">
                            <button id="task-view-btn"
                                class="btn btn-primary btn-sm"
                                style="
                                    background-color:#1E3A8A;
                                    border-color:#334155;
                                ">
                                <img src="https://cdn-icons-png.flaticon.com/128/2921/2921222.png"
                                style="width:20px;height:20px;filter:brightness(0) invert(1);">
                            </button>
                            <select id="pending-status-filter"
                                    class="form-control"
                                    style="
                                        width:220px;
                                        display:none;
                                    ">

                                    <option value="">Pending with All</option>
                                    <option value="Customer">Customer </option>
                                    <option value="TEAMPRO">TEAMPRO </option>
                                    <option value="Candidate">Candidate</option>
                                    <option value="Supplier">Supplier </option>

                            </select>
                            <button id="closure-view-btn"
                                class="btn btn-primary btn-sm"
                                style="
                                    background-color:#0F766E;
                                    border-color:#334155;
                                ">
                                <img src="https://cdn-icons-png.flaticon.com/128/681/681494.png"
                style="width:22px;height:22px;filter:brightness(0) invert(1);">
                            </button>

                            <select id="closure-status-filter"
                                class="form-control"
                                style="
                                    width:220px;
                                    display:none;
                                ">

                                <option value="">All Status</option>

                            </select>
                            <button id="download-excel" title="Download Excel"
                                style="background:none;border:none;width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;">
                                <img src="https://cdn-icons-png.flaticon.com/128/724/724933.png"
                                    style="width:24px;height:24px;">
                            </button>

                        </div>

                    </div>

                    <div id="closure-unified-container"
                    style="
                        margin-top:0px;
                        height:90vh;
                        overflow-y:auto;
                        border:1px solid #ddd;
                    ">
                </div>
                </div>
                    
                

                
                    
            </div>   


        
<!-- SO Details -->
<div class="closure-matrix-container" style="display: flex; gap: 20px; margin: 20px;">
    <!-- Table 1 -->
    <div style="flex: 1; background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
        <!-- Heading + Download -->
        <div style="display:flex;justify-content:space-between;align-items:center;background-color:white;margin-top:20px;margin-bottom:15px;padding:10px 15px;border-radius:6px;">
            <h4 style="margin:0;text-align:left;font-size:16px;font-weight:600;">
                CLOSURE "DROPPED" - SALES ORDER NOT UPDATED
            </h4>
            <button id="download_closure_btn"
                style="background-color:black;color:white;border:none;padding:6px 14px;border-radius:5px;cursor:pointer;font-size:13px;font-weight:500;">
                Download
            </button>
        </div>
        <div id="monitor-table-1"
            style="overflow:auto;max-height:400px;border:1px solid #ddd;padding:10px;">
        </div>
    </div>

    <!-- Table 2 -->
    <div style="flex: 1; background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
        <!-- Heading + Download -->
        <div style="display:flex;justify-content:space-between;align-items:center;background-color:white;margin-top:20px;margin-bottom:15px;padding:10px 15px;border-radius:6px;">
            <h4 style="margin:0;text-align:left;font-size:16px;font-weight:600;">
                CLOSURE "ARRIVED" - SALES ORDER NOT UPDATED
            </h4>
            <button id="download_arrived_btn"
                style="background-color:black;color:white;border:none;padding:6px 14px;border-radius:5px;cursor:pointer;font-size:13px;font-weight:500;">
                Download
            </button>
        </div>
        <div id="monitor-table-2"
            style="overflow:auto;max-height:400px;border:1px solid #ddd;padding:10px;">
        </div>
        <span id="loading-table-2"
            style="font-size:16px;color:#555;display:block;text-align:center;">
            Loading data...
        </span>
    </div>

</div>


            <div id="ptsr-sections-wrapper" style="margin-right: 20px; margin-left: 20px; margin-bottom:100px;" ></div>

            
            

        </div>
                `);



    $(wrapper).find('#monitor-toggle-cards').after(`
    <!-- Monitor Group Sections -->
    <div id="teampro" class="ptsr-filter-section"></div>
    <div id="candidate_agent" class="ptsr-filter-section"></div>
    <div id="agent" class="ptsr-filter-section"></div>
    <div id="client" class="ptsr-filter-section"></div>
    <div id="kickoff-section" class="ptsr-filter-section"></div>
    <div id="submission-section" class="ptsr-filter-section"></div>
    <div id="submission-feedback-section" class="ptsr-filter-section"></div>
    <div id="feedback-section" class="ptsr-filter-section"></div>
`);

//     $(wrapper).find('#monitor-toggle-cards').before(`
//     <div style="margin-top:30px;margin-bottom:30px; display: flex;  align-items: center; justify-content: center;gap: 15px;border: 1px solid #ddd; border-radius: 8px;background-color: #f5f5f5;margin-left:20px;margin-right:20px;">

//         <button class="btn btn-sm btn-outline-primary" id="select-all-cards" style="margin-top:10px;margin-bottom:10px;">Select All</button>
//         <button class="btn btn-sm btn-outline-danger" id="deselect-all-cards">Deselect All</button>

//         <!-- Monitor Toggle Buttons Inline -->
//         <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#teampro">INTERNAL</button>
//         <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#candidate_agent">CANDIDATE</button>
//         <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#agent">AGENT</button>
//         <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#supp_follow_up">SUPPLIER</button>
//         <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#client">CLIENT</button>
//         <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#nepal">NEPAL</button>
//         <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#srilanka">SRILANKA</button>
        
        
//         <button type="button" class="btn btn-sm btn-outline-primary monitor-toggle-card"
         
       
//     </div>
// `);
    // Add unified control + toggle card bar
    $(wrapper).find('#ptsr-sections-wrapper').before(`

    <div id="monitor-toggle-cards" style="display: flex; gap: 25px; justify-content: center; align-items: center; margin-top:30px;margin-bottom:30px;displan:none" >
   
    <div id="monitor-toggle-cards" style="margin-top:30px;margin-bottom:30px;display: flex; gap: 35px;justify-content: center; align-items: center;border: 1px solid #ddd; border-radius: 8px;background-color: #f5f5f5;margin-left:20px;display:none;">

        <button class="btn btn-sm btn-outline-primary" id="select-all-cards" style="margin-top:10px;margin-bottom:10px; margin-left:10px;">Select All</button>
        

        <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" style="margin-top:10px;margin-bottom:10px;  " data-target="#teampro" data-key="teampro">INTERNAL</button>
        <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#candidate_agent" data-key="candidate_agent">CANDIDATE</button>
        <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#agent" data-key="agent">AGENT</button>
        <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#supp_follow_up" data-key="supp_follow_up">SUPPLIER</button>
        <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#client" data-key="client">CLIENT</button>
        <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#nepal"
        data-key="nepal">NEPAL</button>
        <button type="button" class="btn btn-sm btn-sm btn-outline-primary monitor-toggle-card" data-target="#srilanka" data-key="srilanka" style="margin-right:10px;">SRILANKA</button>
 
        
    </div>


    <div id"monitor-toggle-cards" style="border:1px solid lightgrey; background-color:#f5f5f5; padding:10px; border-radius:8px;display:none;">
        <button type="button" class="btn btn-sm btn-sm btn-outline-primary " id="all_download" data-target="#all_download" >Download</button>
         
        </div>
    
   </div>
    
`);
    // Add the monitor group section containers (hidden by default, shown when toggle is clicked)
    $(wrapper).find('#monitor-toggle-cards').after(`
    <div id="teampro" class="ptsr-filter-section" style="display:none;" ></div>
    <div id="candidate_agent" class="ptsr-filter-section" style="display:none;"></div>
    <div id="agent" class="ptsr-filter-section" style="display:none;"></div>
    <div id="supp_follow_up" class="ptsr-filter-section" style="display:none;"></div>
    <div id="client" class="ptsr-filter-section" style="display:none;"></div>
    <div id="nepal" class="ptsr-filter-section" style="display:none;"></div>
    <div id="srilanka" class="ptsr-filter-section" style="display:none;"></div>
    <div id="kickoff-section" class="ptsr-filter-section"></div>
    <div id="submission-section" class="ptsr-filter-section"></div>
    <div id="submission-feedback-section" class="ptsr-filter-section"></div>
    <div id="feedback-section" class="ptsr-filter-section"></div>

`);

$(document).on("click", "#download-excel", function () {

    let d = new frappe.ui.Dialog({
        title: "Download Options",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "options_html"
            }
        ]
    });

    d.fields_dict.options_html.$wrapper.html(`
        <div style="text-align:center; padding:10px;">

            <p style="
                margin-bottom:20px;
                font-size:14px;
                font-weight:500;
            ">
                What do you want to download?
            </p>

            <div style="
                display:flex;
                justify-content:center;
                align-items:center;
                gap:20px;
            ">

                <!-- TASK BUTTON -->
                <button class="btn btn-primary" id="download-task" title="Task Download"
                    style="background-color:#1E3A8A;border:none;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;padding:0;">

                    <img src="https://cdn-icons-png.flaticon.com/128/2921/2921222.png"
                        style="width:20px;height:20x;object-fit:contain;filter:brightness(0) invert(1);display:block;margin:auto;">
                </button>

                <!-- CANDIDATE BUTTON -->
                <button class="btn btn-primary" id="download-candidate" title="Candidate Download"
                    style="background-color:#0F766E;border:none;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;padding:0;">
                    <img src="https://cdn-icons-png.flaticon.com/128/681/681494.png"
                        style="width:20px;height:20px;object-fit:contain;filter:brightness(0) invert(1);display:block;margin:auto;">
                </button>
            </div>

        </div>
    `);

    d.show();

    
    $(document).on("click", "#download-task", function () {

        d.hide();

                    window.open("/api/method/jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.download_task_summary");


    });

    d.$wrapper.on("click", "#download-candidate", function () {

        d.hide();

        window.open(
            "/api/method/jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.download_candidate_summary"
        );

    });

});


frappe.call({
    method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_dropped_closure_active_so",
    callback: function(r) {
        let data = r.message || [];
        render_table("monitor-table-1", data);
    }
});



$("#download_closure_btn").off("click").on("click", function () {

    window.open(
        "/api/method/jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.download_dropped_closure_active_so_excel"
    );

});

document.getElementById("loading-table-2").style.display = "block";

frappe.call({
    method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_arrived_closure_active_so",
    callback: function(r) {

        let data = r.message || [];

        render_table("monitor-table-2", data);
        document.getElementById("loading-table-2").style.display = "none";
    }
});

$("#download_arrived_btn").off("click").on("click", function () {

    window.open(
        "/api/method/jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.download_arrived_closure_active_so_excel"
    );

});



// function render_table(container_id, data) {

//     let container = document.getElementById(container_id);

//     if (!container) return;

//     if (!data || data.length === 0) {
//         container.innerHTML = `<p style="text-align:center;">No Data Available</p>`;
//         return;
//     }

//     let html = `
//         <div class="custom-table-wrapper">
//             <table class="custom-table">
//                 <thead>
//                     <tr>
//                         <th>S#</th>
//                         <th>Cl#</th>
//                         <th>PP#</th>
//                         <th>Name</th>
//                         <th>Client</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//     `;
//     let s_no = 1

//     data.forEach(row => {
//         html += `
//             <tr>
//                 <td>${s_no++}</td>
//                 <td>
//                     <a href="/app/closure/${row.closure_id}" target="_blank">
//                         ${row.closure_id || "-"}
//                     </a>
//                 </td>
//                 <td>${row.passport_number || "-"}</td>
//                 <td style="text-align:left;">${row.name || "-"}</td>
//                 <td style="text-align:left;">${row.client || "-"}</td>
//             </tr>
//         `;
        
//     });
    

//     html += `
//                 </tbody>
//             </table>
//         </div>
//     `;

//     container.innerHTML = html;
// }

function render_table(container_id, data) {

    let container = document.getElementById(container_id);

    if (!container) return;

    if (!data || data.length === 0) {
        container.innerHTML = `<p style="text-align:center;">No Data Available</p>`;
        return;
    }

    let html = `
        <div class="custom-table-wrapper">
            <table class="custom-table" style="
                width:100%;
                border-collapse:collapse;
            ">
                <thead>
                    <tr style="
                        background:#0F1568;
                        color:white;
                    ">
                        <th style="padding:8px; border:1px solid #ccc;">S#</th>

                        <th style="padding:8px; border:1px solid #ccc;">
                            Cl#
                        </th>

                        <th style="padding:8px; border:1px solid #ccc;">
                            PP#
                        </th>

                        <th style="padding:8px; border:1px solid #ccc;">
                            Name
                        </th>

                        <th style="padding:8px; border:1px solid #ccc;">
                            Client
                        </th>
                    </tr>
                </thead>

                <tbody>
    `;

    let s_no = 1;

    data.forEach((row, index) => {

        // ODD / EVEN ROW COLOR
        let bg = (index % 2 === 0)
            ? "#FFFFFF"
            : "#E7E6EC";

        html += `
            <tr style="background:${bg};">

                <td style="
                    padding:8px;
                    border:1px solid #ccc;
                    text-align:center;
                ">
                    ${s_no++}
                </td>

                <td style="
                    padding:8px;
                    border:1px solid #ccc;
                    text-align:center;
                ">
                    <a href="/app/closure/${row.closure_id}"
                        target="_blank"
                        style="text-decoration:none;">

                        ${row.closure_id || "-"}

                    </a>
                </td>

                <td style="
                    padding:8px;
                    border:1px solid #ccc;
                    text-align:center;
                ">
                    ${row.passport_number || "-"}
                </td>

                <td style="
                    padding:8px;
                    border:1px solid #ccc;
                    text-align:left;
                ">
                    ${row.name || "-"}
                </td>

                <td style="
                    padding:8px;
                    border:1px solid #ccc;
                    text-align:left;
                ">
                    ${row.client || "-"}
                </td>

            </tr>
        `;
    });

    html += `
                </tbody>
            </table>
        </div>
    `;

    container.innerHTML = html;
}

    //Select All
    // $('#select-all-cards').on('click', function () {
    //     $(this).addClass('selected-card');
    //     $('#deselect-all-cards').removeClass('selected-card');

    //     $('.monitor-toggle-card').each(function () {
    //         const $card = $(this);
    //         const target = $card.data("target");
    //         $card.addClass('selected-card');
    //         $(target).show();
    //     });
    // });



    let selectAllToggled = false;

    $('#select-all-cards').on('click', function () {
        const lastSelected = localStorage.getItem("lastSelectedMonitorTab") || "teampro";

        if (!selectAllToggled) {

            selectAllToggled = true;

            $(this).addClass('selected-card');
            $('#deselect-all-cards').removeClass('selected-card');

            $('.monitor-toggle-card').each(function () {
                const $card = $(this);
                const target = $card.data("target");

                $card.addClass('selected-card');
                $(target).show();
            });
        } else {

            selectAllToggled = false;

            $('#select-all-cards').removeClass('selected-card');
            $('.monitor-toggle-card').removeClass('selected-card btn-primary').addClass('btn-outline-primary');
            $(".ptsr-filter-section").hide();


            const $last = $(`.monitor-toggle-card[data-key="${lastSelected}"]`);
            $last.addClass("selected-card btn-primary").removeClass("btn-outline-primary");

            const target = $last.data("target");
            $(target).show();
        }
    });






    //Deselect All
    $('#deselect-all-cards').on('click', function () {
        $(this).addClass('selected-card');
        $('#select-all-cards').removeClass('selected-card');

        $('.monitor-toggle-card').each(function () {
            const $card = $(this);
            const target = $card.data("target");
            $card.removeClass('selected-card');
            $(target).hide();
        });
    });


    // Manually show specific sections and highlight the toggle buttons without triggering any clicks
    const defaultVisibleSections = [
        //     "#teampro",
        //     "#candidate_agent",
        //     "#agent",
        //     "#supp_follow_up",
        //     "#client",
        //     "#nepal",
        //     "srilanka"

    ];

    defaultVisibleSections.forEach(selector => {
        $(selector).show(); // show section directly

    });

    const toggleCardStyle = document.createElement("style");
    toggleCardStyle.innerHTML = `
    .monitor-toggle-card.selected-card {
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        transform: scale(1.05);
        transition: all 0.2s ease-in-out;
    }
`;
    document.head.appendChild(toggleCardStyle);

    // Override section appending to correct div based on group title
    const targetMap = {
        "INTERNAL": "#teampro",
        "CANDIDATE": "#candidate_agent",
        "AGENT": "#agent",
        "SUPPLIER": "#supp_follow_up",
        "CLIENT": "#client",
        "NEPAL": "#nepal",
        "SRILANKA": "#srilanka",

    };
    const filterGroups = [
        { title: "INTERNAL", status: ["PSL", "Emigration", "Ticket", "Onboarding"] },
        { title: "CANDIDATE", status: ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"] },
        { title: "AGENT", status: ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"] },
        { title: "SUPPLIER", status: ["Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"] },
        { title: "CLIENT", status: ["Client Offer Letter", "Visa"] },
        { title: "NEPAL", status: ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"] },
        { title: "SRILANKA", status: ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"] },

    ];

    const downloadBtn = document.getElementById("all_download");
    if (downloadBtn) {
        downloadBtn.addEventListener("click", downloadAllClosureExcel);
    }


    function loadDefaultTeamproData() {
        const statusList = ["PSL", "Emigration", "Ticket", "Onboarding"];
        const selectedTerritory = "";
        const selectedClient = "";



        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
            args: {
                status: JSON.stringify(statusList),
                territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateTeamproTable(data, "INTERNAL")
                    : `<div style="min-height:600px;"><div style="margin-top: 30px;">No Data Available</div></div>`;

                const targetSelector = targetMap["INTERNAL"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);


                populateTerritoryDropdown();
                populateClientDropdown();

                // Now that table (and apply button) is rendered, attach filter handler
                attachTeamproFilterHandler();

                const downloadBtn = document.getElementById("download-closure-teampro");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadTeamproExcel);
                }
            }
        });
    }

    //     function loadDefaultTeamproData() {

    //     const statusList = ["PSL", "Emigration", "Ticket", "Onboarding"];
    //     const selectedClient = "";
    //     const selectedTerritory = "";

    //     frappe.call({
    //         method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
    //         args: {
    //             status: JSON.stringify(statusList),
    //             territory: selectedTerritory,
    //             client: selectedClient
    //         },
    //         callback: function (r) {

    //             const data = r.message?.closure || [];

    //             const sectionHtml = data.length > 0
    //                 ? generateTeamproTable(data, "INTERNAL")
    //                 : `<div style="min-height:600px;text-align:center;margin-top:30px;">
    //                     No Data Available
    //                    </div>`;

    //             const targetSelector = targetMap["INTERNAL"];

    //             $(wrapper).find(targetSelector).html(sectionHtml);
    //             setTimeout(() => {

    //                 populateTerritoryDropdown();
    //                 populateClientDropdown();

    //                 const tableSection = $(wrapper).find('#teampro');

    //                 tableSection.find("#status-select-teampro").select2({
    //                     placeholder: "Select Status",
    //                     width: "resolve"
    //                 });
    //                 tableSection.find("#client-select-teampro").select2({
    //                     placeholder: "Select Client",
    //                     width: "resolve",

    //                 });

    //                 // tableSection.off("change", "#status-select-teampro, #client-select-teampro");

    //                 tableSection.on("change", "#status-select-teampro, #client-select-teampro", function () {

    //                     const selectedStatus = tableSection.find("#status-select-teampro").val();
    //                     const selectedClient = tableSection.find("#client-select-teampro").val();

    //                     const newStatusList = selectedStatus
    //                         ? [selectedStatus]
    //                         : ["PSL", "Emigration", "Ticket", "Onboarding"];

    //                     frappe.call({
    //                         method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
    //                         args: {
    //                             status: JSON.stringify(newStatusList),
    //                             client: selectedClient
    //                         },
    //                         callback: function (res) {

    //                             const newData = res.message?.closure || [];

    //                             const newHtml = newData.length > 0
    //                                 ? generateTeamproTable(newData, "INTERNAL")
    //                                 : `<div style="min-height:600px;text-align:center;margin-top:30px;">
    //                                     No Data Available
    //                                    </div>`;

    //                             $(wrapper).find(targetSelector).html(newHtml);
    //                         }
    //                     });

    //                 });

    //             }, 100);

    //             const downloadBtn = document.getElementById("download-closure-teampro");
    //             if (downloadBtn) {
    //                 downloadBtn.addEventListener("click", downloadTeamproExcel);
    //             }

    //         }
    //     });
    // }


    function attachTeamproFilterHandler() {
    const applyFilter = () => {
        const selectedStatus = $('#status-select-teampro').val();
        const selectedClient = $('#client-select-teampro').val();
        const selectedTerritory = $('#territory-select-teampro')?.val() || "";

        const statusList = selectedStatus
            ? [selectedStatus]
            : ["PSL", "Emigration", "Ticket", "Onboarding"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
            args: {
                status: JSON.stringify(statusList),
                territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateTeamproTable(data, "INTERNAL")
                    : `<div style="min-height:600px;">
                        <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
                        <button id="back-teampro" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary">Back</button>
                      </div>`;

                const targetSelector = targetMap["INTERNAL"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);

                // Repopulate dropdowns after re-render
                populateTerritoryDropdown();
                populateClientDropdown();

                // Re-attach change listeners using delegation
                $('#teampro').off('change', '#status-select-teampro, #client-select-teampro, #territory-select-teampro');
                $('#teampro').on('change', '#status-select-teampro, #client-select-teampro, #territory-select-teampro', applyFilter);

                // Back button
                document.getElementById("back-teampro")?.addEventListener("click", loadDefaultTeamproData);
                attachTeamproFilterHandler();

                // Download button
                const downloadBtn = document.getElementById("download-closure-teampro");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadTeamproExcel);
                }
            }
        });
    };

    // Initial binding (when page loads)
    $('#teampro').off('change', '#status-select-teampro, #client-select-teampro, #territory-select-teampro');
    $('#teampro').on('change', '#status-select-teampro, #client-select-teampro, #territory-select-teampro', applyFilter);
}


    // function attachTeamproFilterHandler() {
    //     const applyBtn = document.getElementById("apply-filter-teampro");

    //     if (!applyBtn) {
    //         console.warn("Apply button not found. Delaying binding.");
    //         return;
    //     }

    //     // Remove previous handler if needed (optional safety)
    //     applyBtn.replaceWith(applyBtn.cloneNode(true));
    //     const newApplyBtn = document.getElementById("apply-filter-teampro");

    //     newApplyBtn.addEventListener("click", function () {
    //         const selectedStatus = document.getElementById("status-select-teampro").value;
    //         // const selectedTerritory = document.getElementById("territory-select-teampro").value;
    //         const selectedClient = document.getElementById("client-select-teampro").value;

    //         const statusList = selectedStatus
    //             ? [selectedStatus]
    //             : ["PSL", "Emigration", "Ticket", "Onboarding"];

    //         console.log("Sending filters (user-selected):", {
    //             status: statusList,
    //             // territory: selectedTerritory,
    //             client: selectedClient
    //         });

    //         frappe.call({
    //             method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
    //             args: {
    //                 status: JSON.stringify(statusList),
    //                 // territory: selectedTerritory,
    //                 client: selectedClient
    //             },
    //             callback: function (r) {
    //                 const data = r.message?.closure || [];
    //                 const sectionHtml = data.length > 0
    //                     ? generateTeamproTable(data, "INTERNAL")
    //                     : `<div style="min-height:600px;" >
    //                     <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
    //                    <button id="back-teampro" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

    //                 const targetSelector = targetMap["INTERNAL"] || "#ptsr-sections-wrapper";
    //                 $(wrapper).find(targetSelector).html(sectionHtml);


    //                 populateTerritoryDropdown();
    //                 populateClientDropdown();

    //                 document.getElementById("back-teampro")?.addEventListener("click", loadDefaultTeamproData);

    //                 // Re-bind the filter handler again since table is re-rendered
    //                 attachTeamproFilterHandler();

    //                 const downloadBtn = document.getElementById("download-closure-teampro");
    //                 if (downloadBtn) {
    //                     downloadBtn.addEventListener("click", downloadTeamproExcel);
    //                 }
    //             }
    //         });
    //     });
    //     document.getElementById("status-select-teampro")
    //         ?.addEventListener("change", () => newApplyBtn.click());

    //     document.getElementById("client-select-teampro")
    //         ?.addEventListener("change", () => newApplyBtn.click());
    // }



    // ✅ Initial call on page load
    loadDefaultTeamproData();

    function populateTerritoryDropdown() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_territories",
            callback: function (res) {
                if (res.message) {
                    $('#territory-select-teampro').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Territory</option>');
                        res.message.forEach(ter => {
                            select.append(`<option value="${ter.name}">${ter.name}</option>`);
                        });
                    });
                    $('#territory-select-teampro').select2({
                        placeholder: "Select Territory",
                        width: '20%'
                    });
                }
            }
        });
    }

    function populateClientDropdown() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_client",
            callback: function (res) {
                if (res.message) {
                    $('#client-select-teampro').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Client</option>');
                        res.message.forEach(cli => {
                            select.append(`<option value="${cli.name}">${cli.name}</option>`);
                        });
                    });
                    $('#client-select-teampro').select2({
                        placeholder: "Select Client",
                        width: '20%'
                    });
                }
            }
        });
    }

    function loadDefaultCandidateData() {
        const statusList = ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];
        const selectedTerritory = "";
        const selectedClient = "";

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_candidate",
            args: {
                status: JSON.stringify(statusList),
                territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateCandidateAgentTable(data, "CANDIDATE")
                    : `<div style="min-height:600px;"><div style="margin-top: 30px;">No Data Available</div></div>`;

                const targetSelector = targetMap["CANDIDATE"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);


                populateTerritoryDropdowncan();
                populateClientDropdowncan();


                // Now that table (and apply button) is rendered, attach filter handler
                attachCandidateFilterHandler();

                const downloadBtn = document.getElementById("download-closure-candidate");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadCandidateExcel);
                }
                $(document).on("click", "#send-wp-candidate", function () {
                    sendMassWhatsAppForCandidates();
                });
            }
        });
    }
    function sendMassWhatsAppForCandidates() {

        let rows = $(".candidate-row");

        if (rows.length === 0) {
            frappe.msgprint("No candidates available.");
            return;
        }

        rows.each(function () {

            let candidate_name = $(this).data("candidate_name");
            let mobile_number = $(this).data("mobile_number");

            if (!mobile_number) return;

            let doc = frappe.model.get_new_doc("Mass WhatsApp Broadcast");

            // Main fields
            doc.title = candidate_name;
            doc.template = "hr_recruiter-";
            doc.recipient_type = "Individual";

            // Add child row
            let child = frappe.model.add_child(
                doc,
                "WP Recipient Data",
                "recipients"
            );

            child.mobile_number = mobile_number;
            child.recipient_name = candidate_name;

            frappe.call({
                method: "frappe.client.insert",
                args: { doc: doc },
                callback: function (r) {
                    if (r.message) {
                        frappe.show_alert({
                            message: `WhatsApp Broadcast created for ${candidate_name}`,
                            indicator: "green"
                        });
                    }
                }
            });

        });

        frappe.msgprint("WhatsApp Broadcast creation started.");
    }

    // function attachCandidateFilterHandler() {
    //     const applyBtn = document.getElementById("apply-filter-candidate");

    //     if (!applyBtn) {
    //         console.warn("Apply button not found. Delaying binding.");
    //         return;
    //     }

    //     // Remove previous handler if needed (optional safety)
    //     applyBtn.replaceWith(applyBtn.cloneNode(true));
    //     const newApplyBtn = document.getElementById("apply-filter-candidate");

    //     newApplyBtn.addEventListener("click", function () {
    //         const selectedStatus = document.getElementById("status-select-candidate").value;
    //         // const selectedTerritory = document.getElementById("territory-select-candidate").value;
    //         const selectedClient = document.getElementById("client-select-candidate").value;

    //         const statusList = selectedStatus
    //             ? [selectedStatus]
    //             : ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];

    //         console.log("Sending filters (user-selected):", {
    //             status: statusList,
    //             // territory: selectedTerritory,
    //             client: selectedClient
    //         });

    //         frappe.call({
    //             method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_candidate",
    //             args: {
    //                 status: JSON.stringify(statusList),
    //                 // territory: selectedTerritory,
    //                 client: selectedClient
    //             },
    //             callback: function (r) {
    //                 const data = r.message?.closure || [];
    //                 const sectionHtml = data.length > 0
    //                     ? generateCandidateAgentTable(data, "CANDIDATE")
    //                     : `<div style="min-height:600px;" >
    //                     <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
    //                    <button id="back-candidate" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

    //                 const targetSelector = targetMap["CANDIDATE"] || "#ptsr-sections-wrapper";
    //                 $(wrapper).find(targetSelector).html(sectionHtml);


    //                 populateTerritoryDropdowncan();
    //                 populateClientDropdowncan();

    //                 document.getElementById("back-candidate")?.addEventListener("click", loadDefaultCandidateData);


    //                 // Re-bind the filter handler again since table is re-rendered
    //                 attachCandidateFilterHandler();

    //                 const downloadBtn = document.getElementById("download-closure-candidate");
    //                 if (downloadBtn) {
    //                     downloadBtn.addEventListener("click", downloadCandidateExcel);
    //                 }
    //             }
    //         });
    //     });
    // }

    function attachCandidateFilterHandler(){
    const applyFilter = () => {
        const selectedStatus = $('#status-select-candidate').val();
        const selectedClient = $('#client-select-candidate').val();

        const statusList = selectedStatus
                ? [selectedStatus]
                : ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];

        frappe.call({
                method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_candidate",
                args: {
                    status: JSON.stringify(statusList),
                    // territory: selectedTerritory,
                    client: selectedClient
                },
                callback: function (r) {
                    const data = r.message?.closure || [];
                    const sectionHtml = data.length > 0
                        ? generateCandidateAgentTable(data, "CANDIDATE")
                        : `<div style="min-height:600px;" >
                        <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
                       <button id="back-candidate" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

                    const targetSelector = targetMap["CANDIDATE"] || "#ptsr-sections-wrapper";
                    $(wrapper).find(targetSelector).html(sectionHtml);

            populateTerritoryDropdowncan();
            populateClientDropdowncan();

            $('#candidate_agent').off('change', '#status-select-candidate, #client-select-candidate');
            $('#candidate_agent').on('change', '#status-select-candidate, #client-select-candidate', applyFilter);


            document.getElementById("back-candidate")?.addEventListener("click", loadDefaultCandidateData);

            attachCandidateFilterHandler();

            const downloadBtn = document.getElementById("download-closure-candidate");
            if (downloadBtn) {
                downloadBtn.addEventListener("click", downloadCandidateExcel);
            }
            }
        });

    };
    $('#candidate_agent').off('change', '#status-select-candidate, #client-select-candidate');
    $('#candidate_agent').on('change', '#status-select-candidate, #client-select-candidate', applyFilter);

}

    


    // ✅ Initial call on page load
    loadDefaultCandidateData();

    function populateTerritoryDropdowncan() {

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_territories",
            callback: function (res) {
                if (res.message) {
                    $('#territory-select-candidate').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Territory</option>');
                        res.message.forEach(ter => {
                            select.append(`<option value="${ter.name}">${ter.name}</option>`);
                        });
                    });
                    $('#territory-select-candidate').select2({
                        placeholder: "Select Territory",
                        width: '20%'
                    });
                }
            }
        });
    }

    function populateClientDropdowncan() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_client",
            callback: function (res) {
                if (res.message) {
                    $('#client-select-candidate').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Client</option>');
                        res.message.forEach(cli => {
                            select.append(`<option value="${cli.name}">${cli.name}</option>`);
                        });
                    });
                    $('#client-select-candidate').select2({
                        placeholder: "Select Client",
                        width: '20%'
                    });
                }
            }
        });
    }

    //AGENT

    function loadDefaultAgentData() {
        const statusList = ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];
        const selectedTerritory = "";
        const selectedClient = "";



        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_agent",
            args: {
                status: JSON.stringify(statusList),
                territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateAgentTable(data, "AGENT")
                    : `<div style="min-height:600px" ><div style="margin-top: 30px;">No Data Available</div></div>`;

                const targetSelector = targetMap["AGENT"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);


                populateTerritoryDropdownage();
                populateClientDropdownage();


                // Now that table (and apply button) is rendered, attach filter handler
                attachAgentFilterHandler();

                const downloadBtn = document.getElementById("download-closure-agent");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadAgentExcel);
                }
            }
        });
    }

    // function attachAgentFilterHandler() {
    //     const applyBtn = document.getElementById("apply-filter-agent");

    //     if (!applyBtn) {
    //         console.warn("Apply button not found. Delaying binding.");
    //         return;
    //     }

    //     // Remove previous handler if needed (optional safety)
    //     applyBtn.replaceWith(applyBtn.cloneNode(true));
    //     const newApplyBtn = document.getElementById("apply-filter-agent");

    //     newApplyBtn.addEventListener("click", function () {
    //         const selectedStatus = document.getElementById("status-select-agent").value;
    //         // const selectedTerritory = document.getElementById("territory-select-candidate").value;
    //         const selectedClient = document.getElementById("client-select-agent").value;

    //         const statusList = selectedStatus
    //             ? [selectedStatus]
    //             : ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];

    //         console.log("Sending filters (user-selected):", {
    //             status: statusList,
    //             // territory: selectedTerritory,
    //             client: selectedClient
    //         });

    //         frappe.call({
    //             method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_agent",
    //             args: {
    //                 status: JSON.stringify(statusList),
    //                 // territory: selectedTerritory,
    //                 client: selectedClient
    //             },
    //             callback: function (r) {
    //                 const data = r.message?.closure || [];
    //                 const sectionHtml = data.length > 0
    //                     ? generateAgentTable(data, "AGENT")
    //                     : `<div style="min-height:600px;" >
    //                     <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
    //                    <button id="back-agent" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

    //                 const targetSelector = targetMap["AGENT"] || "#ptsr-sections-wrapper";
    //                 $(wrapper).find(targetSelector).html(sectionHtml);


    //                 populateTerritoryDropdownage();
    //                 populateClientDropdownage();

    //                 document.getElementById("back-agent")?.addEventListener("click", loadDefaultAgentData);


    //                 // Re-bind the filter handler again since table is re-rendered
    //                 attachAgentFilterHandler();

    //                 const downloadBtn = document.getElementById("download-closure-agent");
    //                 if (downloadBtn) {
    //                     downloadBtn.addEventListener("click", downloadAgentExcel);
    //                 }
    //             }
    //         });
    //     });
    // }



    function attachAgentFilterHandler() {
    const applyFilter = () => {
        const selectedStatus = document.getElementById("status-select-agent").value;
        const selectedClient = document.getElementById("client-select-agent").value;

        const statusList = selectedStatus
            ? [selectedStatus]
            : ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_agent",
            args: {
                status: JSON.stringify(statusList),
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                        ? generateAgentTable(data, "AGENT")
                        : `<div style="min-height:600px;" >
                        <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
                       <button id="back-agent" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

                // Render table inside #agent
                $('#agent').html(sectionHtml);

                // Repopulate dropdowns
                populateTerritoryDropdownage();
                populateClientDropdownage();

                // Bind change events inside #agent only
                $('#agent').off('change', '#status-select-agent, #client-select-agent');
                $('#agent').on('change', '#status-select-agent, #client-select-agent', applyFilter);

                document.getElementById("back-agent")?.addEventListener("click", loadDefaultAgentData);
                attachAgentFilterHandler(); // re-attach after default load

                // Download button
                $('#download-closure-agent').off('click').on('click', downloadAgentExcel);
            }
        });
    };

    // Initial binding inside #agent
    $('#agent').off('change', '#status-select-agent, #client-select-agent');
    $('#agent').on('change', '#status-select-agent, #client-select-agent', applyFilter);
}

    // ✅ Initial call on page load
    loadDefaultAgentData();

    function populateTerritoryDropdownage() {

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_territories",
            callback: function (res) {
                if (res.message) {
                    $('#territory-select-agent').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Territory</option>');
                        res.message.forEach(ter => {
                            select.append(`<option value="${ter.name}">${ter.name}</option>`);
                        });
                    });
                    $('#territory-select-agent').select2({
                        placeholder: "Select Territory",
                        width: '20%'
                    });
                }
            }
        });
    }

    function populateClientDropdownage() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_client",
            callback: function (res) {
                if (res.message) {
                    $('#client-select-agent').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Client</option>');
                        res.message.forEach(cli => {
                            select.append(`<option value="${cli.name}">${cli.name}</option>`);
                        });
                    });
                    $('#client-select-agent').select2({
                        placeholder: "Select Client",
                        width: '20%'
                    });
                }
            }
        });
    }

    //SFU

    function loadDefaultSFUData() {
        const statusList = ["Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];
        const selectedTerritory = "";
        const selectedClient = "";



        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
            args: {
                status: JSON.stringify(statusList),
                territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateSFUTable(data, "SUPPLIER")
                    : `<div style="min-height:600px;"><div style="margin-top: 30px;">No Data Available</div></div>`;

                const targetSelector = targetMap["SUPPLIER"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);


                populateTerritoryDropdownsfu();
                populateClientDropdownsfu();


                // Now that table (and apply button) is rendered, attach filter handler
                attachSFUFilterHandler();

                const downloadBtn = document.getElementById("download-closure-sfu");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadSupplierExcel);
                }
            }
        });
    }

    // function attachSFUFilterHandler() {
    //     const applyBtn = document.getElementById("apply-filter-sfu");

    //     if (!applyBtn) {
    //         console.warn("Apply button not found. Delaying binding.");
    //         return;
    //     }

    //     // Remove previous handler if needed (optional safety)
    //     applyBtn.replaceWith(applyBtn.cloneNode(true));
    //     const newApplyBtn = document.getElementById("apply-filter-sfu");

    //     newApplyBtn.addEventListener("click", function () {
    //         const selectedStatus = document.getElementById("status-select-sfu").value;
    //         // const selectedTerritory = document.getElementById("territory-select-candidate").value;
    //         const selectedClient = document.getElementById("client-select-sfu").value;

    //         const statusList = selectedStatus
    //             ? [selectedStatus]
    //             : ["Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

    //         console.log("Sending filters (user-selected):", {
    //             status: statusList,
    //             // territory: selectedTerritory,
    //             client: selectedClient
    //         });

    //         frappe.call({
    //             method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
    //             args: {
    //                 status: JSON.stringify(statusList),
    //                 // territory: selectedTerritory,
    //                 client: selectedClient
    //             },
    //             callback: function (r) {
    //                 const data = r.message?.closure || [];
    //                 const sectionHtml = data.length > 0
    //                     ? generateSFUTable(data, "SUPPLIER")
    //                     : `<div style="min-height:600px;">
    //                 <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
    //                    <button id="back-sfu" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

    //                 const targetSelector = targetMap["SUPPLIER"] || "#ptsr-sections-wrapper";
    //                 $(wrapper).find(targetSelector).html(sectionHtml);


    //                 populateTerritoryDropdownsfu();
    //                 populateClientDropdownsfu();

    //                 document.getElementById("back-sfu")?.addEventListener("click", loadDefaultSFUData);


    //                 // Re-bind the filter handler again since table is re-rendered
    //                 attachSFUFilterHandler();

    //                 const downloadBtn = document.getElementById("download-closure-sfu");
    //                 if (downloadBtn) {
    //                     downloadBtn.addEventListener("click", downloadSupplierExcel);
    //                 }
    //             }
    //         });
    //     });
    // }



    function attachSFUFilterHandler() {
    const applyFilter = () => {
        const selectedStatus = document.getElementById("status-select-sfu").value;
        const selectedClient = document.getElementById("client-select-sfu").value;

         const statusList = selectedStatus
                ? [selectedStatus]
                : ["Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
            args: {
                status: JSON.stringify(statusList),
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                        ? generateSFUTable(data, "SUPPLIER")
                        : `<div style="min-height:600px;" >
                        <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
                       <button id="back-agent" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

                // Render table inside #agent
                $('#supp_follow_up').html(sectionHtml);

                populateTerritoryDropdownsfu();
                populateClientDropdownsfu();

                // Bind change events inside #agent only
                $('#supp_follow_up').off('change', '#status-select-agent, #client-select-agent');
                $('#supp_follow_up').on('change', '#status-select-agent, #client-select-agent', applyFilter);

                document.getElementById("back-agent")?.addEventListener("click", loadDefaultSFUData);
                attachSFUFilterHandler(); // re-attach after default load

                // Download button
                $('#download-closure-sfu').off('click').on('click', downloadSupplierExcel);
            }
        });
    };

    // Initial binding inside #agent
    $('#supp_follow_up').off('change', '#status-select-sfu, #client-select-sfu');
    $('#supp_follow_up').on('change', '#status-select-sfu, #client-select-sfu', applyFilter);
}

    // ✅ Initial call on page load
    loadDefaultSFUData();

    function populateTerritoryDropdownsfu() {

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_territories",
            callback: function (res) {
                if (res.message) {
                    $('#territory-select-sfu').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Territory</option>');
                        res.message.forEach(ter => {
                            select.append(`<option value="${ter.name}">${ter.name}</option>`);
                        });
                    });
                    $('#territory-select-sfu').select2({
                        placeholder: "Select Territory",
                        width: '20%'
                    });
                }
            }
        });
    }

    function populateClientDropdownsfu() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_client",
            callback: function (res) {
                if (res.message) {
                    $('#client-select-sfu').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Client</option>');
                        res.message.forEach(cli => {
                            select.append(`<option value="${cli.name}">${cli.name}</option>`);
                        });
                    });
                    $('#client-select-sfu').select2({
                        placeholder: "Select Client",
                        width: '20%'
                    });
                }
            }
        });
    }

    function loadDefaultClientData() {
        const statusList = ["Client Offer Letter", "Visa"];
        const selectedTerritory = "";
        const selectedClient = "";



        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
            args: {
                status: JSON.stringify(statusList),
                territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {


                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateClientTable(data, "CLIENT")
                    : `<div style="min-height:600px;"><div style="margin-top: 30px;">No Data Available</div></div>`;

                const targetSelector = targetMap["CLIENT"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);


                populateTerritoryDropdowncli();
                populateClientDropdowncli();


                // Now that table (and apply button) is rendered, attach filter handler
                attachClientFilterHandler();

                const downloadBtn = document.getElementById("download-closure-client");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadClientExcel);
                }
            }
        });
    }

    // function attachClientFilterHandler() {
    //     const applyBtn = document.getElementById("apply-filter-client");

    //     if (!applyBtn) {
    //         console.warn("Apply button not found. Delaying binding.");
    //         return;
    //     }

    //     // Remove previous handler if needed (optional safety)
    //     applyBtn.replaceWith(applyBtn.cloneNode(true));
    //     const newApplyBtn = document.getElementById("apply-filter-client");

    //     newApplyBtn.addEventListener("click", function () {
    //         const selectedStatus = document.getElementById("status-select-client").value;
    //         // const selectedTerritory = document.getElementById("territory-select-client").value;
    //         const selectedClient = document.getElementById("client-select-client").value;

    //         const statusList = selectedStatus
    //             ? [selectedStatus]
    //             : ["Client Offer Letter", "Visa"];

    //         console.log("Sending filters (user-selected):", {
    //             status: statusList,
    //             // territory: selectedTerritory,
    //             client: selectedClient
    //         });

    //         frappe.call({
    //             method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
    //             args: {
    //                 status: JSON.stringify(statusList),
    //                 // territory: selectedTerritory,
    //                 client: selectedClient
    //             },
    //             callback: function (r) {
    //                 const data = r.message?.closure || [];
    //                 const sectionHtml = data.length > 0
    //                     ? generateClientTable(data, "CLIENT")
    //                     : `<div style="min-height:600px;">
    //                     <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
    //                    <button id="back-client" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;


    //                 const targetSelector = targetMap["CLIENT"] || "#ptsr-sections-wrapper";
    //                 $(wrapper).find(targetSelector).html(sectionHtml);


    //                 populateTerritoryDropdowncli();
    //                 populateClientDropdowncli();

    //                 document.getElementById("back-client")?.addEventListener("click", loadDefaultClientData);


    //                 // Re-bind the filter handler again since table is re-rendered
    //                 attachClientFilterHandler();

    //                 const downloadBtn = document.getElementById("download-closure-client");
    //                 if (downloadBtn) {
    //                     downloadBtn.addEventListener("click", downloadClientExcel);
    //                 }
    //             }
    //         });
    //     });
    // }


    function attachClientFilterHandler() {
    const applyFilter = () => {
        const selectedStatus = document.getElementById("status-select-client").value;
        const selectedClient = document.getElementById("client-select-client").value;

        const statusList = selectedStatus
                ? [selectedStatus]
                : ["Client Offer Letter", "Visa"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise",
            args: {
                status: JSON.stringify(statusList),
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                        ? generateClientTable(data, "CLIENT")
                        : `<div style="min-height:600px;" >
                        <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
                       <button id="back-client" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

                // Render table inside #agent
                $('#client').html(sectionHtml);

                populateTerritoryDropdowncli();
                populateClientDropdowncli();

                // Bind change events inside #agent only
                $('#client').off('change', '#status-select-client, #client-select-client');
                $('#client').on('change', '#status-select-client, #client-select-client', applyFilter);

                document.getElementById("back-client")?.addEventListener("click", loadDefaultClientData);
                attachClientFilterHandler(); // re-attach after default load

                // Download button
                $('#download-closure-client').off('click').on('click', downloadClientExcel);
            }
        });
    };

    // Initial binding inside #agent
    $('#client').off('change', '#status-select-client, #client-select-client');
    $('#client').on('change', '#status-select-client, #client-select-client', applyFilter);
}

    // ✅ Initial call on page load
    loadDefaultClientData();


    function populateTerritoryDropdowncli() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_territories",
            callback: function (res) {
                if (res.message) {
                    $('#territory-select-client').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Territory</option>');
                        res.message.forEach(ter => {
                            select.append(`<option value="${ter.name}">${ter.name}</option>`);
                        });
                    });

                    $('#territory-select-client').select2({
                        placeholder: "Select Territory",
                        width: '20%'
                    });
                }
            }
        });
    }

    function populateClientDropdowncli() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_client",
            callback: function (res) {
                if (res.message) {
                    $('#client-select-client').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Client</option>');
                        res.message.forEach(cli => {
                            select.append(`<option value="${cli.name}">${cli.name}</option>`);
                        });
                    });

                    $('#client-select-client').select2({
                        placeholder: "Select Client",
                        width: '20%'
                    });
                }
            }
        });
    }

    //nepal


    function loadDefaultNepalData() {
        const statusList = ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];
        const selectedTerritory = "";
        const selectedClient = "";



        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_nepal",
            args: {
                status: JSON.stringify(statusList),
                // territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {


                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateNepalTable(data, "NEPAL")
                    : `
                <div style="min-height:100px; position:relative; z-index:0;">
                    <div style="margin-top:30px; text-align:center;">No Data Available</div>

                    
                </div>
                
                `;

                const targetSelector = targetMap["NEPAL"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);


                populateTerritoryDropdownnep();
                populateClientDropdownnep();


                // Now that table (and apply button) is rendered, attach filter handler
                attachNepalFilterHandler();

                const downloadBtn = document.getElementById("download-closure-nepal");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadNepalExcel);
                }
            }
        });
    }

    // function attachNepalFilterHandler() {
    //     const applyBtn = document.getElementById("apply-filter-nepal");

    //     if (!applyBtn) {
    //         console.warn("Apply button not found. Delaying binding.");
    //         return;
    //     }

    //     // Remove previous handler if needed (optional safety)
    //     applyBtn.replaceWith(applyBtn.cloneNode(true));
    //     const newApplyBtn = document.getElementById("apply-filter-nepal");

    //     newApplyBtn.addEventListener("click", function () {
    //         const selectedStatus = document.getElementById("status-select-nepal").value;
    //         // const selectedTerritory = document.getElementById("territory-select-nepal").value;
    //         const selectedClient = document.getElementById("client-select-nepal").value;

    //         const statusList = selectedStatus
    //             ? [selectedStatus]
    //             : ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

    //         console.log("Sending filters (user-selected):", {
    //             status: statusList,
    //             // territory: selectedTerritory,
    //             client: selectedClient
    //         });

    //         frappe.call({
    //             method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_nepal",
    //             args: {
    //                 status: JSON.stringify(statusList),
    //                 // territory: selectedTerritory,
    //                 client: selectedClient
    //             },
    //             callback: function (r) {
    //                 const data = r.message?.closure || [];
    //                 const sectionHtml = data.length > 0
    //                     ? generateNepalTable(data, "NEPAL")
    //                     : `<div style="min-height:600px;">
    //                    <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
    //                    <button id="back-nepal" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button>
    //                    </div>`;


    //                 const targetSelector = targetMap["NEPAL"] || "#ptsr-sections-wrapper";
    //                 $(wrapper).find(targetSelector).html(sectionHtml);


    //                 populateTerritoryDropdowncli();
    //                 populateClientDropdowncli();

    //                 document.getElementById("back-nepal")?.addEventListener("click", loadDefaultNepalData);


    //                 // Re-bind the filter handler again since table is re-rendered
    //                 attachNepalFilterHandler();

    //                 const downloadBtn = document.getElementById("download-closure-nepal");
    //                 if (downloadBtn) {
    //                     downloadBtn.addEventListener("click", downloadNepalExcel);
    //                 }
    //             }
    //         });
    //     });
    // }


    function attachNepalFilterHandler() {
    const applyFilter = () => {
        const selectedStatus = document.getElementById("status-select-nepal").value;
        const selectedClient = document.getElementById("client-select-nepal").value;

        const statusList = selectedStatus
                ? [selectedStatus]
                : ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_nepal",
            args: {
                status: JSON.stringify(statusList),
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                        ? generateNepalTable(data, "NEPAL")
                        : `<div style="min-height:600px;" >
                        <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
                       <button id="back-nepal" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

                // Render table inside #agent
                $('#nepal').html(sectionHtml);

                populateTerritoryDropdownnep();
                populateClientDropdownnep();

                // Bind change events inside #agent only
                $('#nepal').off('change', '#status-select-nepal, #client-select-nepal');
                $('#nepal').on('change', '#status-select-nepal, #client-select-nepal', applyFilter);

                document.getElementById("back-nepal")?.addEventListener("click", loadDefaultNepalData);
                attachNepalFilterHandler(); // re-attach after default load

                // Download button
                $('download-closure-nepal').off('click').on('click', downloadNepalExcel);
            }
        });
    };

    // Initial binding inside #agent
    $('#nepal').off('change', '#status-select-nepal, #client-select-nepal');
    $('#nepal').on('change', '#status-select-nepal, #client-select-nepal', applyFilter);
}

    // ✅ Initial call on page load
    loadDefaultNepalData();


    function populateTerritoryDropdownnep() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_territories",
            callback: function (res) {
                if (res.message) {
                    $('#territory-select-client').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Territory</option>');
                        res.message.forEach(ter => {
                            select.append(`<option value="${ter.name}">${ter.name}</option>`);
                        });
                    });

                    $('#territory-select-client').select2({
                        placeholder: "Select Territory",
                        width: '20%'
                    });
                }
            }
        });
    }

    function populateClientDropdownnep() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_client",
            callback: function (res) {
                if (res.message) {
                    $('#client-select-nepal').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Client</option>');
                        res.message.forEach(cli => {
                            select.append(`<option value="${cli.name}">${cli.name}</option>`);
                        });
                    });

                    $('#client-select-nepal').select2({
                        placeholder: "Select Client",
                        width: '20%'
                    });
                }
            }
        });
    }

    //srilanka


    function loadDefaultSrilankaData() {
        const statusList = ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];
        const selectedTerritory = "";
        const selectedClient = "";



        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_srilanka",
            args: {
                status: JSON.stringify(statusList),
                territory: selectedTerritory,
                client: selectedClient
            },
            callback: function (r) {


                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                    ? generateSrilankaTable(data, "SRILANKA")
                    : `<div style="min-height:600px;">
                <div style="margin-top: 30px; text-align:center;">No Data Available</div>
                </div>`;

                const targetSelector = targetMap["SRILANKA"] || "#ptsr-sections-wrapper";
                $(wrapper).find(targetSelector).html(sectionHtml);


                populateTerritoryDropdownsri();
                populateClientDropdownsri();


                // Now that table (and apply button) is rendered, attach filter handler
                attachSrilankaFilterHandler();

                const downloadBtn = document.getElementById("download-closure-srilanka");
                if (downloadBtn) {
                    downloadBtn.addEventListener("click", downloadSrilankaExcel);
                }
            }
        });
    }

    // function attachSrilankaFilterHandler() {
    //     const applyBtn = document.getElementById("apply-filter-srilanka");

    //     if (!applyBtn) {
    //         console.warn("Apply button not found. Delaying binding.");
    //         return;
    //     }

    //     // Remove previous handler if needed (optional safety)
    //     applyBtn.replaceWith(applyBtn.cloneNode(true));
    //     const newApplyBtn = document.getElementById("apply-filter-srilanka");

    //     newApplyBtn.addEventListener("click", function () {
    //         const selectedStatus = document.getElementById("status-select-srilanka").value;
    //         // const selectedTerritory = document.getElementById("territory-select-srilanka").value;
    //         const selectedClient = document.getElementById("client-select-srilanka").value;

    //         const statusList = selectedStatus
    //             ? [selectedStatus]
    //             : ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

    //         console.log("Sending filters (user-selected):", {
    //             status: statusList,
    //             // territory: selectedTerritory,
    //             client: selectedClient
    //         });

    //         frappe.call({
    //             method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_srilanka",
    //             args: {
    //                 status: JSON.stringify(statusList),
    //                 // territory: selectedTerritory,
    //                 client: selectedClient
    //             },
    //             callback: function (r) {
    //                 const data = r.message?.closure || [];
    //                 const sectionHtml = data.length > 0
    //                     ? generateSrilankaTable(data, "SRILANKA")
    //                     : `<div style="min-height:600px;">
                        
    //                     <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
    //                    <button id="back-srilanka" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button>
    //                    </div>`;


    //                 const targetSelector = targetMap["SRILANKA"] || "#ptsr-sections-wrapper";
    //                 $(wrapper).find(targetSelector).html(sectionHtml);


    //                 populateTerritoryDropdowncli();
    //                 populateClientDropdowncli();

    //                 document.getElementById("back-srilanka")?.addEventListener("click", loadDefaultSrilankaData);


    //                 // Re-bind the filter handler again since table is re-rendered
    //                 attachClientFilterHandler();

    //                 const downloadBtn = document.getElementById("download-closure-srilanka");
    //                 if (downloadBtn) {
    //                     downloadBtn.addEventListener("click", downloadSrilankaExcel);
    //                 }
    //             }
    //         });
    //     });
    // }


     function attachSrilankaFilterHandler() {
    const applyFilter = () => {
        const selectedStatus = document.getElementById("status-select-srilanka").value;
        const selectedClient = document.getElementById("client-select-srilanka").value;

        const statusList = selectedStatus
                ? [selectedStatus]
                : ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_srilanka",
            args: {
                status: JSON.stringify(statusList),
                client: selectedClient
            },
            callback: function (r) {
                const data = r.message?.closure || [];
                const sectionHtml = data.length > 0
                        ? generateSrilankaTable(data, "SRILANKA")
                        : `<div style="min-height:600px;" >
                        <div style="margin-top: 30px; text-align:center; font-weight:bold;">No Data Available</div>
                       <button id="back-nepal" style="margin-left:725px; margin-top:5px; margin-bottom:5px;" class="btn btn-primary" >Back</button></div>`;

                // Render table inside #agent
                $('#srilanka').html(sectionHtml);

                populateTerritoryDropdownsri();
                populateClientDropdownsri();

                // Bind change events inside #agent only
                $('#srilanka').off('change', '#status-select-srilanka, #client-select-srilanka');
                $('#srilanka').on('change', '#status-select-srilanka, #client-select-srilanka', applyFilter);

                document.getElementById("back-srilanka")?.addEventListener("click", loadDefaultSrilankaData);
                attachSrilankaFilterHandler(); // re-attach after default load

                // Download button
                $('download-closure-srilanka').off('click').on('click', downloadSrilankaExcel);
            }
        });
    };

    // Initial binding inside #agent
    $('#srilanka').off('change', '#status-select-srilanka, #client-select-srilanka');
    $('#srilanka').on('change', '#status-select-srilanka, #client-select-srilanka', applyFilter);
}

    // ✅ Initial call on page load
    loadDefaultSrilankaData();


    function populateTerritoryDropdownsri() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_territories",
            callback: function (res) {
                if (res.message) {
                    $('#territory-select-srilanka').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Territory</option>');
                        res.message.forEach(ter => {
                            select.append(`<option value="${ter.name}">${ter.name}</option>`);
                        });
                    });

                    $('#territory-select-srilanka').select2({
                        placeholder: "Select Territory",
                        width: '20%'
                    });
                }
            }
        });
    }

    function populateClientDropdownsri() {
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_client",
            callback: function (res) {
                if (res.message) {
                    $('#client-select-srilanka').each(function () {
                        const select = $(this);
                        select.empty().append('<option value="">Select Client</option>');
                        res.message.forEach(cli => {
                            select.append(`<option value="${cli.name}">${cli.name}</option>`);
                        });
                    });

                    $('#client-select-srilanka').select2({
                        placeholder: "Select Client",
                        width: '20%'
                    });
                }
            }
        });
    }


    function generateTeamproTable(data, title) {
        data.sort((a, b) => calculateAgeClosure(b.custom_history) - calculateAgeClosure(a.custom_history));

        let groupedData = {};

        data.forEach(item => {
            let client = item.customer || "";
            if (!groupedData[client]) {
                groupedData[client] = [];
            }
            groupedData[client].push(item);
        });

        let html = `

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div  class="ptsr-table-section" data-group-title="${title}">	
            <style>

               .structure-container{
                   min-height: 600px;
                 }


                 .ptsr-scroll-container {
                    
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }

                 .editable-span {
                            cursor: pointer;
                            display: inline-block;
                            width: 100%;
                            text-align: left;
                        }
                        .editable-input {
                            width: 100%;
                            border: none;
                            background: white;
                            text-align: center;
                            outline: 1px solid #0F1568;
                        }

            </style>
            <div class="structure-container" >
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">

         
                 <h4 style="margin-right: 750px;">${title}</h4>
                
                

                <select id="status-select-teampro" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="PSL">PSL</option>
                    <option value="Emigration">Emigration</option>
                    <option value="Ticket">Ticket</option>
                    <option value="Onboarding">Onboarding</option>
                    
                </select>

                <script>
                    $(document).ready(function() {
                        $('#status-select-teampro').select2({
                            placeholder: "Select Status",
                            width: 'resolve'
                        });
                    });

                    
                    </script>

                 

                


                <select   id="client-select-teampro"  class=" client-select form-control" style="width: 20%; border:1px solid black;  " >
                    <option value="">Select Client</option>

                </select>
                <button id="update-closure-teampro" class="btn btn-primary" onclick="submitUpdatedClosures();">Update</button>
                <button id="download-closure-teampro" class="btn btn-primary">Download</button>
            </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr style="white-space:nowrap;">
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Candidate Contact</th>
                    <th>Status</th>
                    <th>Age</th>
                    <th>Last Update On</th>
                    <th>Next Action</th>
                    <th>Next Action On</th>
                    <th>Latest Remark</th>
                    
                    
                    
                </tr>
            </thead>
            <tbody>`;


        const statusList = [
            "Signed Offer Letter",
            "Premedical",
            "Final Medical",
            "Biometric",
            "QVP",
            "Trade Test",
            "Visa Stamping",
            "Emigration",
            "Ticket",
            "Onboarding"
        ];

        let summaryData = {};

        let grandTotal = {
            "Signed Offer Letter": 0,
            "Premedical": 0,
            "PCC / Visa": 0,
            "Final Medical": 0,
            "Biometric": 0,
            "QVP": 0,
            "Trade Test": 0,
            "Visa Stamping": 0,
            "Emigration": 0,
            "Ticket": 0,
            "Onboarding": 0
        };

        data.forEach(item => {
            let client = item.customer || "-";

            if (!summaryData[client]) {
                summaryData[client] = {
                    "Signed Offer Letter": 0,
                    "Premedical": 0,
                    "PCC / Visa": 0,   // merged column
                    "Final Medical": 0,
                    "Biometric": 0,
                    "QVP": 0,
                    "Trade Test": 0,
                    "Visa Stamping": 0,
                    "Emigration": 0,
                    "Ticket": 0,
                    "Onboarding": 0
                };
            }

            // ✅ Normal statuses
            if (statusList.includes(item.status)) {
                summaryData[client][item.status]++;
            }

            // ✅ Merge PCC + Visa into one column
            if (item.status === "PCC" || item.status === "Visa") {
                summaryData[client]["PCC / Visa"]++;
            }

            // ✅ Emigration (if separate logic needed, adjust here)
            // if (item.status === "Emigration") {
            //     summaryData[client]["Emigration"]++;
            // }
        });

        if (data.length > 0) {

            let serialNo = 1;
            let clientSerialNo = 1

                Object.keys(groupedData).forEach(client => {

                    let safeKey = btoa(client).replace(/=/g, "");
                    

                    // Client header row
                    html += `
                    <tr style="background-color:#d3d3d3; font-weight:bold;">
                        <td>${clientSerialNo++}</td>
                        <td colspan="10" style="text-align:left;">
                            <span class="toggle-btn" data-client="${safeKey}" style="cursor:pointer;">+</span>
                            ${client}
                        </td>
                    </tr>
                    `;

                    groupedData[client].forEach((closure, index) => {

                        let rowColor = (serialNo % 2 === 0) ? "#ffffff" : "#e6f2f1";

                            html += `
                            <tr class="client-row-${safeKey}" style="display:none; background-color:${rowColor};">
                                <td>${serialNo++}</td>
                                <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
                                <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
                                <td>${closure.passport_no || '-'}</td>

                            <td>
                                    ${closure.mobile
                                            ? (() => {
                                                const cleanNumber = closure.mobile.replace(/\D/g, '');
                                                return `${closure.mobile}
                                                <a href="https://wa.me/${cleanNumber}" target="_blank">
                                                    <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
                                                </a>`;
                                            })()
                                            : '-'
                                        }
                                </td>

                                <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
                                    class="status-cell" 
                                    data-name="${closure.name}" 
                                    data-status="${closure.status}">
                                    ${closure.status || '-'}
                                </td>
                                <td>${calculateAgeClosure(closure.custom_history)}</td>
                                <td>${formatDate(closure.last_updated_on) || '-'}</td>

                                <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
                                    <span class="editable-span">${closure.std_remarks || '-'}</span>
                                </td>

                                <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
                                <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
                                
                                <span class="editable-span">${closure.remark || '-'}</span>
                                </td>
                            </tr>`;
                                                });

                });


        //     data.forEach((closure, index) => {


        //         let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

        //         // let standard_remarks = "";
        //         // frappe.db.get_value("Standard Remarks", { "name": closure.standard_remarks }, "standard_remarks").then(r => {

        //         //     if (r.message.standard_remarks) {
        //         //         standard_remarks = r.message.standard_remarks;
        //         //     }
        //         // })


        //         html += `
        // <tr class="project-header" style="background-color:${color};">
        //     <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
        //     <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
        //     <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
        //     <td>${closure.passport_no || '-'}</td>

        //    <td>
        //         ${closure.mobile
        //                 ? (() => {
        //                     const cleanNumber = closure.mobile.replace(/\D/g, '');
        //                     return `${closure.mobile}
        //                     <a href="https://wa.me/${cleanNumber}" target="_blank">
        //                         <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
        //                     </a>`;
        //                 })()
        //                 : '-'
        //             }
        //     </td>


        //     <td style="text-align:left !important;" >${closure.customer || '-'}</td>
        //     <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
        //         class="status-cell" 
        //         data-name="${closure.name}" 
        //         data-status="${closure.status}">
        //         ${closure.status || '-'}
        //     </td>
        //     <td>${calculateAgeClosure(closure.custom_history)}</td>
        //     <td>${formatDate(closure.last_updated_on) || '-'}</td>

        //     <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
        //         <span class="editable-span">${closure.std_remarks || '-'}</span>
        //     </td>

        //     <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
        //     <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
            
        //     <span class="editable-span">${closure.remark || '-'}</span>
        //     </td>
            
        // </tr>`;


            // });


        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="11"><center>No Data Available</center></td>
            </tr>`;
        }

        html += `</tbody></table></div></div></div></div>`;

        let summaryHtml = `
            <div class="border rounded p-3 mt-2" style="border-color:#e0e0e0;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 class="text-muted mb-0">Internal Summary</h3>

                    <button class="btn btn-sm btn-primary" onclick="downloadClosureSummaryTable()">
                        Download
                    </button>
                </div>

                <div class="ptsr-horizontal-scroll">
                <table id="closure-summary-table">
                    <thead>
                        <tr>
                            <th>Customer</th>
                            <th>SOL</th>
                            <th>Premedical</th>
                            <th>PCC / Visa</th>
                            <th>Final Medical</th>
                            <th>Biometric</th>
                            <th>QVP</th>
                            <th>Trade Test</th>
                            <th>Visa Stamping</th>
                            <th>Emigration</th>
                            <th>Ticket</th>
                            <th>Onboarding</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            Object.keys(summaryData).forEach(client => {
                let row = summaryData[client];
                Object.keys(grandTotal).forEach(key => {
                    grandTotal[key] += row[key] || 0;
                });

                summaryHtml += `
                    <tr>
                        <td style="text-align:left;">${client}</td>
                        <td>${row["Signed Offer Letter"] || "-"}</td>
                        <td>${row["Premedical"] || "-"}</td>
                        <td>${row["PCC / Visa"] || "-"}</td>
                        <td>${row["Final Medical"] || "-"}</td>
                        <td>${row["Biometric"] || "-"}</td>
                        <td>${row["QVP"] || "-"}</td>
                        <td>${row["Trade Test"] || "-"}</td>
                        <td>${row["Visa Stamping"] || "-"}</td>
                        <td>${row["Emigration"] || "-"}</td>
                        <td>${row["Ticket"] || "-"}</td>
                        <td>${row["Onboarding"] || "-"}</td>
                    </tr>
                `;
            });

            summaryHtml += `
                <tr style="font-weight:bold; background:#f0f0f0;">
                    <td>Total</td>
                    <td>${grandTotal["Signed Offer Letter"] || "-"}</td>
                    <td>${grandTotal["Premedical"] || "-"}</td>
                    <td>${grandTotal["PCC / Visa"] || "-"}</td>
                    <td>${grandTotal["Final Medical"] || "-"}</td>
                    <td>${grandTotal["Biometric"] || "-"}</td>
                    <td>${grandTotal["QVP"] || "-"}</td>
                    <td>${grandTotal["Trade Test"] || "-"}</td>
                    <td>${grandTotal["Visa Stamping"] || "-"}</td>
                    <td>${grandTotal["Emigration"] || "-"}</td>
                    <td>${grandTotal["Ticket"] || "-"}</td>
                    <td>${grandTotal["Onboarding"] || "-"}</td>
                </tr>
`;

            summaryHtml += `</tbody></table></div></div>`;
        

        html += summaryHtml;


        return html;
    }
    window.downloadClosureSummaryTable = function () {
    let table = document.getElementById("closure-summary-table");

    if (!table) {
        alert("Summary table not found");
        return;
    }

    let csv = [];

    let rows = table.querySelectorAll("tr");

    rows.forEach(row => {
        let cols = row.querySelectorAll("th, td");
        let rowData = [];

        cols.forEach(col => {
            let text = col.innerText.replace(/\n/g, " ").replace(/,/g, "");
            rowData.push(`"${text}"`);
        });

        csv.push(rowData.join(","));
    });

    let csvContent = csv.join("\n");

    let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

    let link = document.createElement("a");
    let url = URL.createObjectURL(blob);

    link.setAttribute("href", url);
    link.setAttribute("download", "closure_summary.csv");

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
}



    document.addEventListener("click", function (e) {

            if (!e.target.classList.contains("toggle-btn")) return;

            const key = e.target.dataset.client;
            const rows = document.querySelectorAll(".client-row-" + key);

            const isVisible = rows[0].style.display === "table-row";

            rows.forEach(row => {
                row.style.display = isVisible ? "none" : "table-row";
            });

            e.target.textContent = isVisible ? "+" : "-";
        });



    function generateCandidateAgentTable(data, title) {
        data.sort((a, b) => calculateAgeClosure(b.custom_history) - calculateAgeClosure(a.custom_history));

        let groupedData = {};

        data.forEach(item => {
            let client = item.customer || "-";

            if (!groupedData[client]) {
                groupedData[client] = [];
            }

            groupedData[client].push(item);
        });

        let summaryData = {};
        let grandTotal = {
            "Signed Offer Letter": 0,
            "Premedical": 0,
            "PCC": 0,
            "Final Medical": 0
        };

        data.forEach(item => {

            let client = item.customer || "-";
            let status = item.status || "-";

            // init client object
            if (!summaryData[client]) {
                summaryData[client] = {
                    "Signed Offer Letter": 0,
                    "Premedical": 0,
                    "PCC": 0,
                    "Final Medical": 0
                };
            }

            if (summaryData[client][status] !== undefined) {
                summaryData[client][status]++;
            }

            if (grandTotal[status] !== undefined) {
                grandTotal[status]++;
            }
        });

        let html = `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div class="ptsr-table-section" data-group-title="${title}">	
            <style>

                .structure-container{
                   min-height: 600px;
                 }

                 .ptsr-scroll-container {
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    .project-row:nth-of-type(odd) {
                    background-color: #e6f2f1;
                }
                .project-row:nth-of-type(even) {
                    background-color: #ffffff;
                }
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }
            </style>
            <div class="structure-container" >
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            <div class="ptsr-horizontal-scroll" style="max-height:600px; overflow-y:auto;position: sticky; top: 0; z-index: 1;"" >
                
                    


                     

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">
                
               <h4 style="margin-right: 750px;">${title}</h4>

                <select id="status-select-candidate" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="Signed Offer Letter">Signed Offer Letter</option>
                    <option value="Premedical">Premedical</option>
                    <option value="PCC">PCC</option>
                    <option value="Final Medical">Final Medical</option>
                    
                </select>

                <script>
                    $(document).ready(function() {
                        $('#status-select-candidate').select2({
                        placeholder: "Select Status",
                        width: 'resolve' 
                        });
                    });
                </script>

                 

                


                <select id="client-select-candidate"   class=" client-select form-control" style="width: 20%; border:1px solid black;" >
                    <option value="">Select Client</option>

                </select>
                <button id="update-closure-candidate" class="btn btn-primary" onclick="submitUpdatedClosures();">Update</button>
                <button id="download-closure-candidate" class="btn btn-primary">Download</button>
                <button id="send-wp-candidate" class="btn btn-success">
                <i class="fa fa-whatsapp"></i>
            </button>
                        </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr style="white-space:nowrap;">
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Candidate Contact</th>
                    <th>Status</th>
                    <th>Age</th>
                    <th>Last Update On</th>
                    <th>Next Action</th>
                    <th>Next Action On</th>
                    <th>Latest Remark</th>
                    
                    
                    
                    
                </tr>
            </thead>
            <tbody>`;


        if (data.length > 0) {

            let serialNo = 1;
            let clientSerialNo = 1;

                Object.keys(groupedData).forEach(client => {

                    let safeKey = btoa(client).replace(/=/g, "");
                    

                    // Client header row
                    html += `
                    <tr style="background-color:#d3d3d3; font-weight:bold;">
                        <td>${clientSerialNo++}</td>
                        <td colspan="11" style="text-align:left;">
                            <span class="toggle-btn" data-client="${safeKey}" style="cursor:pointer;">+</span>
                            ${client}
                        </td>
                    </tr>
                    `;

                    groupedData[client].forEach((closure, index) => {

                        let rowColor = (serialNo % 2 === 0) ? "#ffffff" : "#e6f2f1";

                            html += `
                            <tr class="client-row-${safeKey}" style="display:none; background-color:${rowColor};">
                                <td>${serialNo++}</td>
                                <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
                                <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
                                <td>${closure.passport_no || '-'}</td>

                                <td>
                                    ${closure.mobile
                                            ? (() => {
                                                const cleanNumber = closure.mobile.replace(/\D/g, '');
                                                return `${closure.mobile}
                                                <a href="https://wa.me/${cleanNumber}" target="_blank">
                                                    <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
                                                </a>`;
                                            })()
                                            : '-'
                                        }
                                </td>


                                <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
                                    class="status-cell" 
                                    data-name="${closure.name}" 
                                    data-status="${closure.status}">
                                    ${closure.status || '-'}
                                </td>
                                <td>${calculateAgeClosure(closure.custom_history)}</td>
                                <td>${formatDate(closure.last_updated_on) || '-'}</td>
                                
                                <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
                                    <span class="editable-span">${closure.std_remarks || '-'}</span>
                                </td>

                                <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
                                <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
                                
                                <span class="editable-span">${closure.remark || '-'}</span>
                                </td>
                                
                            </tr>`;
                                                });

                });


        //     data.forEach((closure, index) => {


        //         let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

        //         html += `
        // <tr class="project-header candidate-row"
        //         data-candidate_name="${closure.given_name || ''}"
        //         data-mobile_number="${closure.mobile || ''}"
        //         style="background-color:${color};">
        //     <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
        //     <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
        //     <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
        //     <td>${closure.passport_no || '-'}</td>

        //      <td>
        //         ${closure.mobile
        //                 ? (() => {
        //                     const cleanNumber = closure.mobile.replace(/\D/g, '');
        //                     return `${closure.mobile}
        //                     <a href="https://wa.me/${cleanNumber}" target="_blank">
        //                         <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
        //                     </a>`;
        //                 })()
        //                 : '-'
        //             }
        //     </td>




        //     <td style="text-align:left !important;" >${closure.customer || '-'}</td>
        //     <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
        //         class="status-cell" 
        //         data-name="${closure.name}" 
        //         data-status="${closure.status}">
        //         ${closure.status || '-'}
        //     </td>
        //     <td>${calculateAgeClosure(closure.custom_history)}</td>
        //     <td>${formatDate(closure.last_updated_on) || '-'}</td>
            
        //     <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
        //         <span class="editable-span">${closure.std_remarks || '-'}</span>
        //     </td>

        //     <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
        //     <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
            
        //     <span class="editable-span">${closure.remark || '-'}</span>
        //     </td>
            
            
        // </tr>`;


        //     });



        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="12"><center>No Data Available</center></td>
            </tr>`;
        }

        html += `</tbody></table></div></div></div></div>`;

        let summaryHtml = `
            <div class="border rounded p-3 mt-3">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 class="text-muted mb-0">Candidate Summary</h3>

                    <button class="btn btn-sm btn-primary" onclick="downloadClosureSummaryTablecan()">
                        Download
                    </button>
                </div>

                <div class="ptsr-horizontal-scroll">
                <table id="candidate-summary-table">

                    <thead>
                        <tr style="background:#0F1568;color:white;">
                            <th style="text-align:left; width:40%;">Customer</th>

                            <th style="text-align:center; width:15%;">Signed Offer Letter</th>
                            <th style="text-align:center; width:15%;">Premedical</th>
                            <th style="text-align:center; width:15%;">PCC</th>
                            <th style="text-align:center; width:15%;">Final Medical</th>
                        </tr>
                    </thead>

                    <tbody>
            `;

        Object.keys(summaryData).forEach(client => {

            let row = summaryData[client];

            summaryHtml += `
                <tr>
                    <td style="text-align:left;">${client}</td>
                    <td style="text-align:center;">${row["Signed Offer Letter"] || "-"}</td>
                    <td style="text-align:center;">${row["Premedical"] || "-"}</td>
                    <td style="text-align:center;">${row["PCC"] || "-" }</td>
                    <td style="text-align:center;">${row["Final Medical"] || "-"}</td>
                </tr>
            `;
        });

        summaryHtml += `
            <tr style="font-weight:bold;background:#f0f0f0;">
                <td style="text-align:left;">Total</td>
                <td style="text-align:center;">${grandTotal["Signed Offer Letter"] || "-"}</td>
                <td style="text-align:center;">${grandTotal["Premedical"] || "-"}</td>
                <td style="text-align:center;">${grandTotal["PCC"] || "-"}</td>
                <td style="text-align:center;">${grandTotal["Final Medical"] || "-"}</td>
            </tr>
            `;

        summaryHtml += `</tbody></table></div></div>`;

        html += summaryHtml;
        return html;
    }
    window.downloadClosureSummaryTablecan = function () {
        let table = document.getElementById("candidate-summary-table");

        if (!table) {
            alert("Summary table not found");
            return;
        }

        let csv = [];

        let rows = table.querySelectorAll("tr");

        rows.forEach(row => {
            let cols = row.querySelectorAll("th, td");
            let rowData = [];

            cols.forEach(col => {
                let text = col.innerText.replace(/\n/g, " ").replace(/,/g, "");
                rowData.push(`"${text}"`);
            });

            csv.push(rowData.join(","));
        });

        let csvContent = csv.join("\n");

        let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

        let link = document.createElement("a");
        let url = URL.createObjectURL(blob);

        link.setAttribute("href", url);
        link.setAttribute("download", "closure_summary.csv");

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
    }



    function generateAgentTable(data, title) {
        data.sort((a, b) => calculateAgeClosure(b.custom_history) - calculateAgeClosure(a.custom_history));

        let groupedData = {};

        data.forEach(item => {
            let client = item.customer || "";
            if (!groupedData[client]) {
                groupedData[client] = [];
            }
            groupedData[client].push(item);
        });
        let summaryData = {};
        let grandTotal = {
            "Signed Offer Letter": 0,
            "Premedical": 0,
            "PCC": 0,
            "Final Medical": 0
        };

        data.forEach(item => {

            let client = item.customer || "-";
            let status = item.status || "-";

            // init client bucket
            if (!summaryData[client]) {
                summaryData[client] = {
                    "Signed Offer Letter": 0,
                    "Premedical": 0,
                    "PCC": 0,
                    "Final Medical": 0
                };
            }

            // count only valid columns
            if (summaryData[client][status] !== undefined) {
                summaryData[client][status]++;
            }

            // grand total
            if (grandTotal[status] !== undefined) {
                grandTotal[status]++;
            }
        });

        let html = `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div class="ptsr-table-section" data-group-title="${title}">	
            <style>
                .structure-container{
                   min-height: 600px;
                 }


                 .ptsr-scroll-container {
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    .project-row:nth-of-type(odd) {
                    background-color: #e6f2f1;
                }
                .project-row:nth-of-type(even) {
                    background-color: #ffffff;
                }
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }
            </style>
            <div class="structure-container" >
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            <div class="ptsr-horizontal-scroll" style="max-height:600px; overflow-y:auto;position: sticky; top: 0; z-index: 1;"" >
                
                    


                     

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">
                
               <h4 style="margin-right: 750px;">${title}</h4>

                <select id="status-select-agent" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="Signed Offer Letter">Signed Offer Letter</option>
                    <option value="Premedical">Premedical</option>
                    <option value="PCC">PCC</option>
                    <option value="Final Medical">Final Medical</option>
                    
                </select>

                <script>
                    $(document).ready(function() {
                        $('#status-select-agent').select2({
                        placeholder: "Select Status",
                        width: 'resolve' 
                        });
                    });
                </script>

                 

                


                <select id="client-select-agent"   class=" client-select form-control" style="width: 20%; border:1px solid black;" >
                    <option value="">Select Client</option>

                </select>
                <button id="update-closure-agent" class="btn btn-primary" onclick="submitUpdatedClosures();">Update</button>
                <button id="download-closure-agent" class="btn btn-primary">Download</button>
            </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr style="white-space:nowrap;">
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Candidate Contact</th>
                    <th>Status</th>
                    <th>Age</th>
                    <th>Last Update On</th>
                    <th>Next Action</th>
                    <th>Next Action On</th>
                    <th>Latest Remark</th>
                    <th>Agent</th>
                    <th>Contact</th>
                    
                    
                    
                </tr>
            </thead>
            <tbody>`;


        if (data.length > 0) {


            let serialNo = 1;
            let clientSerialNo = 1;

                Object.keys(groupedData).forEach(client => {

                    let safeKey = btoa(client).replace(/=/g, "");
                    

                    // Client header row
                    html += `
                    <tr style="background-color:#d3d3d3; font-weight:bold;">
                        <td>${clientSerialNo++}</td>
                        <td colspan="13" style="text-align:left;">
                            <span class="toggle-btn" data-client="${safeKey}" style="cursor:pointer;">+</span>
                            ${client}
                        </td>
                    </tr>
                    `;

                    groupedData[client].forEach((closure, index) => {

                        let rowColor = (serialNo % 2 === 0) ? "#ffffff" : "#e6f2f1";

                            html += `
                            <tr class="client-row-${safeKey}" style="display:none; background-color:${rowColor};">
                                <td>${serialNo++}</td>
                                <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
                                <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
                                <td>${closure.passport_no || '-'}</td>

                                <td>
                                    ${closure.mobile
                                            ? (() => {
                                                const cleanNumber = closure.mobile.replace(/\D/g, '');
                                                return `${closure.mobile}
                                                <a href="https://wa.me/${cleanNumber}" target="_blank">
                                                    <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
                                                </a>`;
                                            })()
                                            : '-'
                                        }
                                </td>





                                <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
                                    class="status-cell" 
                                    data-name="${closure.name}" 
                                    data-status="${closure.status}">
                                    ${closure.status || '-'}
                                </td>
                                <td>${calculateAgeClosure(closure.custom_history)}</td>
                                <td>${formatDate(closure.last_updated_on) || '-'}</td>
                                
                                <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
                                    <span class="editable-span">${closure.std_remarks || '-'}</span>
                                </td>

                                <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
                                <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
                                
                                <span class="editable-span">${closure.remark || '-'}</span>
                                </td>


                                <td style="text-align:left !important;" >${closure.sa_name || '-'}</td>
                                <td style="text-align:left !important;" >${closure.sa_mobile_number || '-'}</td>
                            </tr>`;
                                                });

                });


        //     data.forEach((closure, index) => {


        //         let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

        //         html += `
        // <tr class="project-header" style="background-color:${color};">
        //     <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
        //     <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
        //     <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
        //     <td>${closure.passport_no || '-'}</td>

        //      <td>
        //         ${closure.mobile
        //                 ? (() => {
        //                     const cleanNumber = closure.mobile.replace(/\D/g, '');
        //                     return `${closure.mobile}
        //                     <a href="https://wa.me/${cleanNumber}" target="_blank">
        //                         <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
        //                     </a>`;
        //                 })()
        //                 : '-'
        //             }
        //     </td>





        //     <td style="text-align:left !important;" >${closure.customer || '-'}</td>
        //     <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
        //         class="status-cell" 
        //         data-name="${closure.name}" 
        //         data-status="${closure.status}">
        //         ${closure.status || '-'}
        //     </td>
        //     <td>${calculateAgeClosure(closure.custom_history)}</td>
        //     <td>${formatDate(closure.last_updated_on) || '-'}</td>
            
        //     <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
        //         <span class="editable-span">${closure.std_remarks || '-'}</span>
        //     </td>

        //     <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
        //     <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
            
        //     <span class="editable-span">${closure.remark || '-'}</span>
        //     </td>


        //     <td style="text-align:left !important;" >${closure.sa_name || '-'}</td>
        //     <td style="text-align:left !important;" >${closure.sa_mobile_number || '-'}</td>
            
        // </tr>`;


            // });



        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="14"><center>No Data Available</center></td>
            </tr>`;
        }



        html += `</tbody></table></div></div></div></div>`;

        let summaryHtml = `
        <div class="border rounded p-3 mt-3">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <h3 class="text-muted mb-0">Agent Summary</h3>

                <button class="btn btn-sm btn-primary" onclick="downloadClosureSummaryTableAg()">
                    Download
                </button>
            </div>

            <div class="ptsr-horizontal-scroll">
            <table id="agent-summary-table">

                <thead>
                    <tr style="background:#0F1568;color:white;">
                        <th style="width:40%;">Customer</th>
                        <th style="width:15%;">Signed Offer Letter</th>
                        <th style="width:15%;">Premedical</th>
                        <th style="width:15%;">PCC</th>
                        <th style="width:15%;">Final Medical</th>
                    </tr>
                </thead>

                <tbody>
        `;

        Object.keys(summaryData).forEach(client => {

            let row = summaryData[client];

            summaryHtml += `
                <tr>
                    <td style="text-align:left;">${client}</td>
                    <td>${row["Signed Offer Letter"] || "-"}</td>
                    <td>${row["Premedical"] || "-"}</td>
                    <td>${row["PCC"] || "-"}</td>
                    <td>${row["Final Medical"] || "-"}</td>
                </tr>
            `;
        });

        summaryHtml += `
            <tr style="font-weight:bold;background:#f0f0f0;">
                <td style="text-align:left;">TOTAL</td>
                <td>${grandTotal["Signed Offer Letter"] || "-"}</td>
                <td>${grandTotal["Premedical"] || "-"}</td>
                <td>${grandTotal["PCC"] || "-"}</td>
                <td>${grandTotal["Final Medical"] || "-"}</td>
            </tr>
        `;
        summaryHtml += `</tbody></table></div></div>`;

    html += summaryHtml;

        return html;
    }
    window.downloadClosureSummaryTableAg = function () {
        let table = document.getElementById("agent-summary-table");

        if (!table) {
            alert("Summary table not found");
            return;
        }

        let csv = [];

        let rows = table.querySelectorAll("tr");

        rows.forEach(row => {
            let cols = row.querySelectorAll("th, td");
            let rowData = [];

            cols.forEach(col => {
                let text = col.innerText.replace(/\n/g, " ").replace(/,/g, "");
                rowData.push(`"${text}"`);
            });

            csv.push(rowData.join(","));
        });

        let csvContent = csv.join("\n");

        let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

        let link = document.createElement("a");
        let url = URL.createObjectURL(blob);

        link.setAttribute("href", url);
        link.setAttribute("download", "closure_summary.csv");

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
    }


    function generateSFUTable(data, title) {
        data.sort((a, b) => calculateAgeClosure(b.custom_history) - calculateAgeClosure(a.custom_history));
        let groupedData = {};

        data.forEach(item => {
            let client = item.customer || "";
            if (!groupedData[client]) {
                groupedData[client] = [];
            }
            groupedData[client].push(item);
        });

        let summaryData = {};
        let grandTotal = {
            "Certificate Attestation": 0,
            "Biometric": 0,
            "Trade Test": 0,
            "Visa Stamping": 0
        };

        data.forEach(item => {

            let client = item.customer || "-";
            let status = item.status || "-";

            if (!summaryData[client]) {
                summaryData[client] = {
                    "Certificate Attestation": 0,
                    "Biometric": 0,
                    "Trade Test": 0,
                    "Visa Stamping": 0
                };
            }

            if (summaryData[client][status] !== undefined) {
                summaryData[client][status]++;
            }

            if (grandTotal[status] !== undefined) {
                grandTotal[status]++;
            }
        });
    

        let html = `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div class="ptsr-table-section" data-group-title="${title}">	
            <style>

                .structure-container{
                   min-height: 600px;
                 }

                 .ptsr-scroll-container {
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    .project-row:nth-of-type(odd) {
                    background-color: #e6f2f1;
                }
                .project-row:nth-of-type(even) {
                    background-color: #ffffff;
                }
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }
            </style>
            <div class="structure-container" >
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            <div class="ptsr-horizontal-scroll" style="max-height:600px; overflow-y:auto;position: sticky; top: 0; z-index: 1;"" >
                
                    


                   

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">
                
               <h4 style="margin-right: 750px;">${title}</h4>

                <select id="status-select-sfu" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="Certificate Attestation">Certificate Attestation</option>
                    <option value="Biometric">Biometric</option>
                    <option value="Trade Test">Trade Test</option>
                    <option value="Visa Stamping">Visa Stamping</option>
                    
                </select>

                

                <script>
                    $(document).ready(function() {
                        $('#status-select-sfu').select2({
                        placeholder: "Select Status",
                        width: 'resolve' 
                        });
                    });
                </script>

                 

                


                <select id="client-select-sfu"   class=" client-select form-control" style="width: 20%; border:1px solid black;" >
                    <option value="">Select Client</option>

                </select>
                <button id="update-closure-sfu" class="btn btn-primary" onclick="submitUpdatedClosures();">Update</button>
                <button id="download-closure-sfu" class="btn btn-primary">Download</button>
            </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr style="white-space:nowrap;">
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Candidate Contact</th>
                    <th>Status</th>
                    <th>Age</th>
                    <th>Last Update On</th>
                    <th>Next Action</th>
                    <th>Next Action On</th>
                    <th>Latest Remark</th>
                    <th>Supplier</th>
                    <th>Contact</th>
                    
                    
                    
                </tr>
            </thead>
            <tbody>`;


        if (data.length > 0) {

            let serialNo = 1;
            let clientSerialNo = 1;

                Object.keys(groupedData).forEach(client => {

                    let safeKey = btoa(client).replace(/=/g, "");
                    

                    // Client header row
                    html += `
                    <tr style="background-color:#d3d3d3; font-weight:bold;">
                        <td>${clientSerialNo++}</td>
                        <td colspan="13" style="text-align:left;">
                            <span class="toggle-btn" data-client="${safeKey}" style="cursor:pointer;">+</span>
                            ${client}
                        </td>
                    </tr>
                    `;

                    groupedData[client].forEach((closure, index) => {

                        let rowColor = (serialNo % 2 === 0) ? "#ffffff" : "#e6f2f1";

                        let con = ""

                        frappe.db.get_value("Supplier", { "name": closure.associate }, "mobile_no").then(r => {

                            if (r.message && r.message.mobile_no) {
                                con = r.message.mobile_no
                            }
                            else {
                                con = ""
                            }

                        })

                            html += `
                            <tr class="client-row-${safeKey}" style="display:none; background-color:${rowColor};">
                                <td>${serialNo++}</td>
                                <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
                                <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
                                <td>${closure.passport_no || '-'}</td>

                                <td>
                                    ${closure.mobile
                                            ? (() => {
                                                const cleanNumber = closure.mobile.replace(/\D/g, '');
                                                return `${closure.mobile}
                                                <a href="https://wa.me/${cleanNumber}" target="_blank">
                                                    <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
                                                </a>`;
                                            })()
                                            : '-'
                                        }
                                </td>

                                <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
                                    class="status-cell" 
                                    data-name="${closure.name}" 
                                    data-status="${closure.status}">
                                    ${closure.status || '-'}
                                </td>
                                <td>${calculateAgeClosure(closure.custom_history)}</td>
                                <td>${formatDate(closure.last_updated_on) || '-'}</td>

                                <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
                                    <span class="editable-span">${closure.std_remarks || '-'}</span>
                                </td>

                                <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
                                <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
                                
                                <span class="editable-span">${closure.remark || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" >${closure.associate || '-'}</td>
                                <td style="text-align:left !important;" >${con || '-'}</td>
                            </tr>`;
                                                });

                });


        //     data.forEach((closure, index) => {


        //         let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

                // let con = ""

                // frappe.db.get_value("Supplier", { "name": closure.associate }, "mobile_no").then(r => {

                //     if (r.message && r.message.mobile_no) {
                //         con = r.message.mobile_no
                //     }
                //     else {
                //         con = ""
                //     }

                // })

        //         html += `
        // <tr class="project-header" style="background-color:${color};">
        //     <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
        //     <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
        //     <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
        //     <td>${closure.passport_no || '-'}</td>

        //      <td>
        //         ${closure.mobile
        //                 ? (() => {
        //                     const cleanNumber = closure.mobile.replace(/\D/g, '');
        //                     return `${closure.mobile}
        //                     <a href="https://wa.me/${cleanNumber}" target="_blank">
        //                         <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
        //                     </a>`;
        //                 })()
        //                 : '-'
        //             }
        //     </td>





        //     <td style="text-align:left !important;" >${closure.customer || '-'}</td>
        //     <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
        //         class="status-cell" 
        //         data-name="${closure.name}" 
        //         data-status="${closure.status}">
        //         ${closure.status || '-'}
        //     </td>
        //     <td>${calculateAgeClosure(closure.custom_history)}</td>
        //     <td>${formatDate(closure.last_updated_on) || '-'}</td>

        //     <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
        //         <span class="editable-span">${closure.std_remarks || '-'}</span>
        //     </td>

        //     <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
        //     <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
            
        //     <span class="editable-span">${closure.remark || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" >${closure.associate || '-'}</td>
        //     <td style="text-align:left !important;" >${con || '-'}</td>
            
        // </tr>`;


            // });



        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="14"><center>No Data Available</center></td>
            </tr>`;
        }
        html += `</tbody></table></div></div></div></div>`;
        let summaryHtml = `
            <div class="border rounded p-3 mt-3">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 class="text-muted mb-0">Supplier Summary</h3>

                    <button class="btn btn-sm btn-primary" onclick="downloadClosureSummaryTablesup()">
                        Download
                    </button>
                </div>

                <div class="ptsr-horizontal-scroll">
                <table id="sup-summary-table">

                    <thead>
                        <tr style="background:#0F1568;color:white;">
                            <th style="width:40%;">Customer</th>
                            <th style="width:15%;">Certificate Attestation</th>
                            <th style="width:15%;">Biometric</th>
                            <th style="width:15%;">Trade Test</th>
                            <th style="width:15%;">Visa Stamping</th>
                        </tr>
                    </thead>

                    <tbody>
            `;

        Object.keys(summaryData).forEach(client => {

            let row = summaryData[client];

            summaryHtml += `
                <tr>
                    <td style="text-align:left;">${client}</td>
                    <td>${row["Certificate Attestation"] || "-"}</td>
                    <td>${row["Biometric"] || "-"}</td>
                    <td>${row["Trade Test"] || "-"}</td>
                    <td>${row["Visa Stamping"] || "-"}</td>
                </tr>
            `;
        });

        summaryHtml += `
            <tr style="font-weight:bold;background:#f0f0f0;">
                <td style="text-align:left;">TOTAL</td>
                <td>${grandTotal["Certificate Attestation"]|| "-"}</td>
                <td>${grandTotal["Biometric"]|| "-"}</td>
                <td>${grandTotal["Trade Test"]|| "-"}</td>
                <td>${grandTotal["Visa Stamping"]|| "-"}</td>
            </tr>
        `;

        summaryHtml += `</tbody></table></div></div>`;

        html += summaryHtml;
        return html;
    }
    window.downloadClosureSummaryTablesup = function () {
        let table = document.getElementById("sup-summary-table");

        if (!table) {
            alert("Summary table not found");
            return;
        }

        let csv = [];

        let rows = table.querySelectorAll("tr");

        rows.forEach(row => {
            let cols = row.querySelectorAll("th, td");
            let rowData = [];

            cols.forEach(col => {
                let text = col.innerText.replace(/\n/g, " ").replace(/,/g, "");
                rowData.push(`"${text}"`);
            });

            csv.push(rowData.join(","));
        });

        let csvContent = csv.join("\n");

        let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

        let link = document.createElement("a");
        let url = URL.createObjectURL(blob);

        link.setAttribute("href", url);
        link.setAttribute("download", "closure_summary.csv");

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
    }



    function generateClientTable(data, title) {
        data.sort((a, b) => calculateAgeClosure(b.custom_history) - calculateAgeClosure(a.custom_history));

        let groupedData = {};

        data.forEach(item => {
            let client = item.customer || "";
            if (!groupedData[client]) {
                groupedData[client] = [];
            }
            groupedData[client].push(item);
        });
        let summaryData = {};
        let grandTotal = {
            "Client Offer Letter": 0,
            "Visa": 0
        };
        data.forEach(item => {
            let client = item.customer || "-";
            let status = item.status || "-";

            if (!summaryData[client]) {
                summaryData[client] = {
                    "Client Offer Letter": 0,
                    "Visa": 0
                };
            }

            if (summaryData[client][status] !== undefined) {
                summaryData[client][status]++;
            }

            if (grandTotal[status] !== undefined) {
                grandTotal[status]++;
            }
        });

        let html = `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div class="ptsr-table-section" data-group-title="${title}">	
            <style>

                .structure-container{
                   min-height: 600px;
                 }

                 .ptsr-scroll-container {
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    .project-row:nth-of-type(odd) {
                    background-color: #e6f2f1;
                }
                .project-row:nth-of-type(even) {
                    background-color: #ffffff;
                }
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }
            </style>
            <div class="structure-container" >
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            <div class="ptsr-horizontal-scroll" style="max-height:600px; overflow-y:auto;position: sticky; top: 0; z-index: 1;"" >
                
                    


                   

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">
                
                <h4 style="margin-right: 750px;">${title}</h4>

                <select id="status-select-client" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="Client Offer Letter">Client Offer Letter</option>
                    <option value="Visa">Visa</option>
                </select>

                <script>
                    $(document).ready(function() {
                        $('#status-select-client').select2({
                        placeholder: "Select Status",
                        width: 'resolve' 
                        });
                    });
                </script>

                 

                


                <select id="client-select-client"   class=" client-select form-control" style="width: 20%; border:1px solid black;" >
                    <option value="">Select Client</option>

                </select>
                <button id="update-closure-client" class="btn btn-primary" onclick="submitUpdatedClosures();">Update</button>
                <button id="download-closure-client" class="btn btn-primary">Download</button>
            </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr style="white-space:nowrap;">
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Candidate Contact</th>
                    <th>Status</th>
                    <th>Age</th>
                    <th>Last Update On</th>
                    <th>Next Action</th>
                    <th>Next Action On</th>
                    <th>Latest Remark</th>
                    
                    
                    
                </tr>
            </thead>
            <tbody>`;


        if (data.length > 0) {


            let serialNo = 1;
            let clientSerialNo = 1;

                Object.keys(groupedData).forEach(client => {

                    let safeKey = btoa(client).replace(/=/g, "");
                    

                    // Client header row
                    html += `
                    <tr style="background-color:#d3d3d3; font-weight:bold;">
                        <td>${clientSerialNo++}</td>
                        <td colspan="11" style="text-align:left;">
                            <span class="toggle-btn" data-client="${safeKey}" style="cursor:pointer;">+</span>
                            ${client}
                        </td>
                    </tr>
                    `;

                    groupedData[client].forEach((closure, index) => {

                        let rowColor = (serialNo % 2 === 0) ? "#ffffff" : "#e6f2f1";

                            html += `
                            <tr class="client-row-${safeKey}" style="display:none; background-color:${rowColor};">
                                <td>${serialNo++}</td>
                                <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
                                <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
                                <td>${closure.passport_no || '-'}</td>

                                <td>
                                    ${closure.mobile
                                            ? (() => {
                                                const cleanNumber = closure.mobile.replace(/\D/g, '');
                                                return `${closure.mobile}
                                                <a href="https://wa.me/${cleanNumber}" target="_blank">
                                                    <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
                                                </a>`;
                                            })()
                                            : '-'
                                        }
                                </td>
                                <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
                                    class="status-cell" 
                                    data-name="${closure.name}" 
                                    data-status="${closure.status}">
                                    ${closure.status || '-'}
                                </td>
                                <td>${calculateAgeClosure(closure.custom_history)}</td>
                                <td>${formatDate(closure.last_updated_on) || '-'}</td>

                                <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
                                    <span class="editable-span">${closure.std_remarks || '-'}</span>
                                </td>

                                <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
                                <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
                                
                                <span class="editable-span">${closure.remark || '-'}</span>
                                </td>
                            </tr>`;
                                                });

                });


            // data.forEach((closure, index) => {


        //         let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

        //         html += `
        // <tr class="project-header" style="background-color:${color};">
        //     <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
        //     <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
        //     <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
        //     <td>${closure.passport_no || '-'}</td>

        //      <td>
        //         ${closure.mobile
        //                 ? (() => {
        //                     const cleanNumber = closure.mobile.replace(/\D/g, '');
        //                     return `${closure.mobile}
        //                     <a href="https://wa.me/${cleanNumber}" target="_blank">
        //                         <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
        //                     </a>`;
        //                 })()
        //                 : '-'
        //             }
        //     </td>





        //     <td style="text-align:left !important;" >${closure.customer || '-'}</td>
        //     <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
        //         class="status-cell" 
        //         data-name="${closure.name}" 
        //         data-status="${closure.status}">
        //         ${closure.status || '-'}
        //     </td>
        //     <td>${calculateAgeClosure(closure.custom_history)}</td>
        //     <td>${formatDate(closure.last_updated_on) || '-'}</td>

        //     <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
        //         <span class="editable-span">${closure.std_remarks || '-'}</span>
        //     </td>

        //     <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
        //     <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
            
        //     <span class="editable-span">${closure.remark || '-'}</span>
        //     </td>
            
        // </tr>`;


        //     });



        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="12"><center>No Data Available</center></td>
            </tr>`;
        }

        html += `</tbody></table></div></div></div></div>`;

        let summaryHtml = `
        <div class="border rounded p-3 mt-3">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <h3 class="text-muted mb-0">Client Summary</h3>

                <button class="btn btn-sm btn-primary" onclick="downloadClosureSummaryTableC()">
                    Download
                </button>
            </div>

            <div class="ptsr-horizontal-scroll">
            <table id="client-summary-table">

                <thead>
                    <tr style="background:#0F1568;color:white;">
                        <th style="text-align:left;width:200px;">Customer</th>
                        <th style="width:200px;">Client Offer Letter</th>
                        <th style="width:200px;">Visa</th>
                    </tr>
                </thead>

                <tbody>
        `;
        Object.keys(summaryData).forEach(client => {

            let row = summaryData[client];

            summaryHtml += `
                <tr>
                    <td style="text-align:left;width:200px;">${client}</td>
                    <td style="text-align:center;width:200px;">${row["Client Offer Letter"]|| "-"}</td>
                    <td style="text-align:center;width:200px;">${row["Visa"] || "-"}</td>
                </tr>
            `;
        });
        summaryHtml += `
            <tr style="font-weight:bold;background:#f0f0f0;">
                <td style="text-align:left;width:200px;">Total</td>
                <td style="text-align:center;width:200px;">${grandTotal["Client Offer Letter"] || "-"}</td>
                <td style="text-align:center;width:200px;">${grandTotal["Visa"] || "-"}</td>
            </tr>
        `;

        summaryHtml += `</tbody></table></div></div>`;
        html += summaryHtml;
        return html;
    }
    window.downloadClosureSummaryTableC = function () {
        let table = document.getElementById("client-summary-table");

        if (!table) {
            alert("Summary table not found");
            return;
        }

        let csv = [];

        let rows = table.querySelectorAll("tr");

        rows.forEach(row => {
            let cols = row.querySelectorAll("th, td");
            let rowData = [];

            cols.forEach(col => {
                let text = col.innerText.replace(/\n/g, " ").replace(/,/g, "");
                rowData.push(`"${text}"`);
            });

            csv.push(rowData.join(","));
        });

        let csvContent = csv.join("\n");

        let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

        let link = document.createElement("a");
        let url = URL.createObjectURL(blob);

        link.setAttribute("href", url);
        link.setAttribute("download", "closure_summary.csv");

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
    }


    function generateNepalTable(data, title) {
        data.sort((a, b) => calculateAgeClosure(b.custom_history) - calculateAgeClosure(a.custom_history));

        let groupedData = {};

        data.forEach(item => {
            let client = item.customer || "";
            if (!groupedData[client]) {
                groupedData[client] = [];
            }
            groupedData[client].push(item);
        });
        let summaryData = {};
        let grandTotal = {
            "PSL": 0,
            "Emigration": 0,
            "Ticket": 0,
            "Onboarding": 0,
            "Signed Offer Letter": 0,
            "Premedical": 0,
            "PCC": 0,
            "Final Medical": 0,
            "Certificate Attestation": 0,
            "Biometric": 0,
            "Trade Test": 0,
            "Visa Stamping": 0
        };
        data.forEach(item => {
        let client = item.customer || "-";
        let status = item.status || "-";

        if (!summaryData[client]) {
            summaryData[client] = {
                "PSL": 0,
                "Emigration": 0,
                "Ticket": 0,
                "Onboarding": 0,
                "Signed Offer Letter": 0,
                "Premedical": 0,
                "PCC": 0,
                "Final Medical": 0,
                "Certificate Attestation": 0,
                "Biometric": 0,
                "Trade Test": 0,
                "Visa Stamping": 0
            };
        }

        if (summaryData[client][status] !== undefined) {
            summaryData[client][status]++;
        }

        if (grandTotal[status] !== undefined) {
            grandTotal[status]++;
        }
    });

        let html = `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div class="ptsr-table-section" data-group-title="${title}">	
            <style>
                .structure-container{
                   min-height: 600px;
                 }
                
                 .ptsr-scroll-container {
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    .project-row:nth-of-type(odd) {
                    background-color: #e6f2f1;
                }
                .project-row:nth-of-type(even) {
                    background-color: #ffffff;
                }
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }
            </style>

            <div class="structure-container" >
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            <div class="ptsr-horizontal-scroll" style="max-height:600px; overflow-y:auto;position: sticky; top: 0; z-index: 1;"" >
                
                    


                   

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">
                
                <h4 style="margin-right: 750px;">${title}</h4>

                <select id="status-select-nepal" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="PSL">PSL</option>
                    <option value="Emigration">Emigration</option>
                    <option value="Ticket">Ticket</option>
                    <option value="Onboarding">Onboarding</option>
                    <option value="Signed Offer Letter">Signed Offer Letter</option>
                    <option value="Premedical">Premedical</option>
                    <option value="PCC">PCC</option>
                    <option value="Final Medical">Final Medical</option>
                    <option value="Certificate Attestation">Certificate Attestation</option>
                    <option value="Biometric">Biometric</option>
                    <option value="Trade Test">Trade Test</option>
                    <option value="Visa Stamping">Visa Stamping</option>
                </select>

              
                <script>
                    $(document).ready(function() {
                        $('#status-select-nepal').select2({
                        placeholder: "Select Status",
                        width: 'resolve' 
                        });
                    });
                </script>

                 

                


                <select id="client-select-nepal"   class=" client-select form-control" style="width: 20%; border:1px solid black;" >
                    <option value="">Select Client</option>

                </select>
                <button id="update-closure-nepal" class="btn btn-primary" onclick="submitUpdatedClosures();">Update</button>
                <button id="download-closure-nepal" class="btn btn-primary">Download</button>
            </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr style="white-space:nowrap;">
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Candidate Contact</th>
                    <th>Status</th>
                    <th>Age</th>
                    <th>Last Update On</th>
                    <th>Next Action</th>
                    <th>Next Action On</th>
                    <th>Latest Remark</th>
                    
                    
                    
                </tr>
            </thead>
            <tbody>`;


        if (data.length > 0) {

            let serialNo = 1;
            let clientSerialNo = 1;

                Object.keys(groupedData).forEach(client => {

                    let safeKey = btoa(client).replace(/=/g, "");
                    

                    // Client header row
                    html += `
                    <tr style="background-color:#d3d3d3; font-weight:bold;">
                        <td>${clientSerialNo++}</td>
                        <td colspan="11" style="text-align:left;">
                            <span class="toggle-btn" data-client="${safeKey}" style="cursor:pointer;">+</span>
                            ${client}
                        </td>
                    </tr>
                    `;

                    groupedData[client].forEach((closure, index) => {

                        let rowColor = (serialNo % 2 === 0) ? "#ffffff" : "#e6f2f1";

                            html += `
                            <tr class="client-row-${safeKey}" style="display:none; background-color:${rowColor};">
                                <td>${serialNo++}</td>
                                 <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
                                <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
                                <td>${closure.passport_no || '-'}</td>

                                <td>
                                    ${closure.mobile
                                            ? (() => {
                                                const cleanNumber = closure.mobile.replace(/\D/g, '');
                                                return `${closure.mobile}
                                                <a href="https://wa.me/${cleanNumber}" target="_blank">
                                                    <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
                                                </a>`;
                                            })()
                                            : '-'
                                        }
                                </td>
                                <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
                                    class="status-cell" 
                                    data-name="${closure.name}" 
                                    data-status="${closure.status}">
                                    ${closure.status || '-'}
                                </td>
                                <td>${calculateAgeClosure(closure.custom_history)}</td>
                                <td>${formatDate(closure.last_updated_on) || '-'}</td>

                                <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
                                    <span class="editable-span">${closure.std_remarks || '-'}</span>
                                </td>

                                <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
                                <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
                                
                                <span class="editable-span">${closure.remark || '-'}</span>
                                </td>
                            </tr>`;
                                                });

                });



        //     data.forEach((closure, index) => {


        //         let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

        //         html += `
        // <tr class="project-header" style="background-color:${color};">
        //     <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
        //     <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
        //     <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
        //     <td>${closure.passport_no || '-'}</td>

        //      <td>
        //         ${closure.mobile
        //                 ? (() => {
        //                     const cleanNumber = closure.mobile.replace(/\D/g, '');
        //                     return `${closure.mobile}
        //                     <a href="https://wa.me/${cleanNumber}" target="_blank">
        //                         <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
        //                     </a>`;
        //                 })()
        //                 : '-'
        //             }
        //     </td>





        //     <td style="text-align:left !important;" >${closure.customer || '-'}</td>
        //     <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
        //         class="status-cell" 
        //         data-name="${closure.name}" 
        //         data-status="${closure.status}">
        //         ${closure.status || '-'}
        //     </td>
        //     <td>${calculateAgeClosure(closure.custom_history)}</td>
        //     <td>${formatDate(closure.last_updated_on) || '-'}</td>

        //     <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
        //         <span class="editable-span">${closure.std_remarks || '-'}</span>
        //     </td>

        //     <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
        //     <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
            
        //     <span class="editable-span">${closure.remark || '-'}</span>
        //     </td>
            
        // </tr>`;


        //     });



        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="12"><center>No Data Available</center></td>
            </tr>`;
        }

        html += `</tbody></table></div></div></div></div>`;
        let summaryHtml = `
        <div class="border rounded p-3 mt-3">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 class="text-muted mb-0">Nepal Summary</h3>

                    <button class="btn btn-sm btn-primary" onclick="downloadClosureSummaryTableN()">
                        Download
                    </button>
                </div>

            <div class="ptsr-horizontal-scroll">
            <table id="nepal-summary-table">

                <thead>
                    <tr style="background:#0F1568;color:white;">
                        <th style="text-align:left;">Customer</th>
                        <th>PSL</th>
                        <th>Emigration</th>
                        <th>Ticket</th>
                        <th>Onboarding</th>
                        <th>Signed Offer Letter</th>
                        <th>Premedical</th>
                        <th>PCC</th>
                        <th>Final Medical</th>
                        <th>Certificate Attestation</th>
                        <th>Biometric</th>
                        <th>Trade Test</th>
                        <th>Visa Stamping</th>
                    </tr>
                </thead>

                <tbody>
        `;
        Object.keys(summaryData).forEach(client => {
            let row = summaryData[client];

            summaryHtml += `
                <tr>
                    <td style="text-align:left;">${client}</td>
                    <td>${row["PSL"] || "-"}</td>
                    <td>${row["Emigration"] || "-"}</td>
                    <td>${row["Ticket"] || "-"}</td>
                    <td>${row["Onboarding"] || "-"}</td>
                    <td>${row["Signed Offer Letter"] || "-"}</td>
                    <td>${row["Premedical"] || "-"}</td>
                    <td>${row["PCC"] || "-"}</td>
                    <td>${row["Final Medical"] || "-"}</td>
                    <td>${row["Certificate Attestation"] || "-"}</td>
                    <td>${row["Biometric"] || "-"}</td>
                    <td>${row["Trade Test"] || "-"}</td>
                    <td>${row["Visa Stamping"] || "-"}</td>
                </tr>
            `;
        });

        summaryHtml += `
            <tr style="font-weight:bold;background:#f0f0f0;">
                <td style="text-align:left;">TOTAL</td>
                <td>${grandTotal["PSL"] || "-"}</td>
                <td>${grandTotal["Emigration"] || "-"}</td>
                <td>${grandTotal["Ticket"] || "-"}</td>
                <td>${grandTotal["Onboarding"] || "-"}</td>
                <td>${grandTotal["Signed Offer Letter"] || "-"}</td>
                <td>${grandTotal["Premedical"] || "-"}</td>
                <td>${grandTotal["PCC"] || "-"}</td>
                <td>${grandTotal["Final Medical"] || "-"}</td>
                <td>${grandTotal["Certificate Attestation"] || "-"}</td>
                <td>${grandTotal["Biometric"] || "-"}</td>
                <td>${grandTotal["Trade Test"] || "-"}</td>
                <td>${grandTotal["Visa Stamping"] || "-"}</td>
            </tr>
        `;
        summaryHtml += `</tbody></table></div></div>`;

        html += summaryHtml;
        return html;
    }
    window.downloadClosureSummaryTableN = function () {
        let table = document.getElementById("nepal-summary-table");

        if (!table) {
            alert("Summary table not found");
            return;
        }

        let csv = [];

        let rows = table.querySelectorAll("tr");

        rows.forEach(row => {
            let cols = row.querySelectorAll("th, td");
            let rowData = [];

            cols.forEach(col => {
                let text = col.innerText.replace(/\n/g, " ").replace(/,/g, "");
                rowData.push(`"${text}"`);
            });

            csv.push(rowData.join(","));
        });

        let csvContent = csv.join("\n");

        let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

        let link = document.createElement("a");
        let url = URL.createObjectURL(blob);

        link.setAttribute("href", url);
        link.setAttribute("download", "closure_summary.csv");

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
    }


    function generateSrilankaTable(data, title) {
        data.sort((a, b) => calculateAgeClosure(b.custom_history) - calculateAgeClosure(a.custom_history));
        let groupedData = {};

        data.forEach(item => {
            let client = item.customer || "";
            if (!groupedData[client]) {
                groupedData[client] = [];
            }
            groupedData[client].push(item);
        });
        let summaryData = {};
        let grandTotal = {
            "PSL": 0,
            "Emigration": 0,
            "Ticket": 0,
            "Onboarding": 0,
            "Signed Offer Letter": 0,
            "Premedical": 0,
            "PCC": 0,
            "Final Medical": 0,
            "Certificate Attestation": 0,
            "Biometric": 0,
            "Trade Test": 0,
            "Visa Stamping": 0
        };
        data.forEach(item => {
            let client = item.customer || "-";
            let status = (item.status || "").trim();

            if (!summaryData[client]) {
                summaryData[client] = {
                    "PSL": 0,
                    "Emigration": 0,
                    "Ticket": 0,
                    "Onboarding": 0,
                    "Signed Offer Letter": 0,
                    "Premedical": 0,
                    "PCC": 0,
                    "Final Medical": 0,
                    "Certificate Attestation": 0,
                    "Biometric": 0,
                    "Trade Test": 0,
                    "Visa Stamping": 0
                };
            }

            if (summaryData[client][status] !== undefined) {
                summaryData[client][status]++;
            }

            if (grandTotal[status] !== undefined) {
                grandTotal[status]++;
            }
        });


        let html = `
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <div  class="ptsr-table-section" data-group-title="${title}">	
            <style>
                 .structure-container{
                   min-height: 600px;
                 }

                 .ptsr-scroll-container {
                    
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    .project-row:nth-of-type(odd) {
                    background-color: #e6f2f1;
                }
                .project-row:nth-of-type(even) {
                    background-color: #ffffff;
                }
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }
            </style>

            <div class="structure-container" >
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            <div class="ptsr-horizontal-scroll" style="max-height:600px; overflow-y:auto;position: sticky; top: 0; z-index: 1;"" >
                
                    


                   

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">
                
                <h4 style="margin-right: 750px;">${title}</h4>

                <select id="status-select-srilanka" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="PSL">PSL</option>
                    <option value="Emigration">Emigration</option>
                    <option value="Ticket">Ticket</option>
                    <option value="Onboarding">Onboarding</option>
                    <option value="Signed Offer Letter">Signed Offer Letter</option>
                    <option value="Premedical">Premedical</option>
                    <option value="PCC">PCC</option>
                    <option value="Final Medical">Final Medical</option>
                    <option value="Certificate Attestation">Certificate Attestation</option>
                    <option value="Biometric">Biometric</option>
                    <option value="Trade Test">Trade Test</option>
                    <option value="Visa Stamping">Visa Stamping</option>
                </select>

                <script>
                    $(document).ready(function() {
                        $('#status-select-srilanka').select2({
                        placeholder: "Select Status",
                        width: 'resolve' 
                        });
                    });
                </script>

                 

                


                <select id="client-select-srilanka"   class=" client-select form-control" style="width: 20%; border:1px solid black;" >
                    <option value="">Select Client</option>

                </select>
                <button id="update-closure-srilanka" class="btn btn-primary" onclick="submitUpdatedClosures();">Update</button>
                <button id="download-closure-srilanka" class="btn btn-primary">Download</button>
            </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr style="white-space:nowrap;">
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Candidate Contact</th>
                    <th>Status</th>
                    <th>Age</th>
                    <th>Last Update On</th>
                    <th>Latest Remark</th>
                    
                    
                    
                </tr>
            </thead>
            <tbody>`;


        if (data.length > 0) {

            let serialNo = 1;
            let clientSerialNo = 1;

                Object.keys(groupedData).forEach(client => {

                    let safeKey = btoa(client).replace(/=/g, "");
                    

                    // Client header row
                    html += `
                    <tr style="background-color:#d3d3d3; font-weight:bold;">
                        <td>${clientSerialNo++}</td>
                        <td colspan="9" style="text-align:left;">
                            <span class="toggle-btn" data-client="${safeKey}" style="cursor:pointer;">+</span>
                            ${client}
                        </td>
                    </tr>
                    `;

                    groupedData[client].forEach((closure, index) => {

                        let rowColor = (serialNo % 2 === 0) ? "#ffffff" : "#e6f2f1";

                            html += `
                            <tr class="client-row-${safeKey}" style="display:none; background-color:${rowColor};">
                                <td>${serialNo++}</td>
                                <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
                                <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
                                <td>${closure.passport_no || '-'}</td>

                                <td>
                                    ${closure.mobile
                                            ? (() => {
                                                const cleanNumber = closure.mobile.replace(/\D/g, '');
                                                return `${closure.mobile}
                                                <a href="https://wa.me/${cleanNumber}" target="_blank">
                                                    <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
                                                </a>`;
                                            })()
                                            : '-'
                                        }
                                </td>

                                <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
                                    class="status-cell" 
                                    data-name="${closure.name}" 
                                    data-status="${closure.status}">
                                    ${closure.status || '-'}
                                </td>
                                <td>${calculateAgeClosure(closure.custom_history)}</td>
                                <td>${formatDate(closure.last_updated_on) || '-'}</td>

                                <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
                                    <span class="editable-span">${closure.std_remarks || '-'}</span>
                                </td>

                                <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
                                <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
                                </td>

                                <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
                                
                                <span class="editable-span">${closure.remark || '-'}</span>
                                </td>
                            </tr>`;
                                                });

                });



        //     data.forEach((closure, index) => {


        //         let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

        //         html += `
        // <tr class="project-header" style="background-color:${color};">
        //     <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
        //     <td  ><a href="https://erp.teamproit.com/app/closure/${closure.name}">${closure.name || '-'}</a></td>
        //     <td style="text-align:left !important;" >${closure.given_name || '-'}</td>
        //     <td>${closure.passport_no || '-'}</td>

        //      <td>
        //         ${closure.mobile
        //                 ? (() => {
        //                     const cleanNumber = closure.mobile.replace(/\D/g, '');
        //                     return `${closure.mobile}
        //                     <a href="https://wa.me/${cleanNumber}" target="_blank">
        //                         <i class="fa fa-whatsapp" style="font-size:24px; color:green;"></i>
        //                     </a>`;
        //                 })()
        //                 : '-'
        //             }
        //     </td>






        //     <td style="text-align:left !important;" >${closure.customer || '-'}</td>
        //     <td style="text-align:left !important; cursor:pointer;  font-weight:bold;" 
        //         class="status-cell" 
        //         data-name="${closure.name}" 
        //         data-status="${closure.status}">
        //         ${closure.status || '-'}
        //     </td>
        //     <td>${calculateAgeClosure(closure.custom_history)}</td>
        //     <td>${formatDate(closure.last_updated_on) || '-'}</td>

        //     <td style="white-space:nowrap;" onclick="makeEditable(this, '${closure.name}', 'standard_remarks')">
        //         <span class="editable-span">${closure.std_remarks || '-'}</span>
        //     </td>

        //     <td onclick="makeEditable(this, '${closure.name}', 'custom_next_follow_up_on')">
        //     <span class="editable-span">${formatDate(closure.custom_next_follow_up_on) || '-'}</span>
        //     </td>

        //     <td style="text-align:left !important;" onclick="makeEditable(this, '${closure.name}', 'remark')" >
            
        //     <span class="editable-span">${closure.remark || '-'}</span>
        //     </td>
            
        // </tr>`;


        //     });



        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="12"><center>No Data Available</center></td>
            </tr>`;
        }

        html += `</tbody></table></div></div></div></div>`;
        let summaryHtml = "";

if (data.length === 0) {

    summaryHtml = `
        <div class="border rounded p-3 mt-3">
            <h5 style="margin-bottom:10px;">Sri Lanka Summary</h5>
            <div style="text-align:center;margin-top:20px;">
                No Data Available
            </div>
        </div>
    `;
}
else {

    summaryHtml = `
    <div class="border rounded p-3 mt-3">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <h3 class="text-muted mb-0">Srilanka Summary</h3>

            <button class="btn btn-sm btn-primary" onclick="downloadClosureSummaryTableS()">
                Download
            </button>
        </div>

        <div class="ptsr-horizontal-scroll">
        <table id="sri-summary-table">

            <thead>
                <tr style="background:#0F1568;color:white;">
                    <th style="text-align:left;">Customer</th>
                    <th>PSL</th>
                    <th>Emigration</th>
                    <th>Ticket</th>
                    <th>Onboarding</th>
                    <th>Signed Offer Letter</th>
                    <th>Premedical</th>
                    <th>PCC</th>
                    <th>Final Medical</th>
                    <th>Certificate Attestation</th>
                    <th>Biometric</th>
                    <th>Trade Test</th>
                    <th>Visa Stamping</th>
                </tr>
            </thead>

            <tbody>
    `;

    Object.keys(summaryData).forEach(client => {
        let row = summaryData[client];

        summaryHtml += `
            <tr>
                <td style="text-align:left;">${client}</td>
                <td>${row["PSL"] || "-"}</td>
                <td>${row["Emigration"] || "-"}</td>
                <td>${row["Ticket"] || "-"}</td>
                <td>${row["Onboarding"] || "-"}</td>
                <td>${row["Signed Offer Letter"] || "-"}</td>
                <td>${row["Premedical"] || "-"}</td>
                <td>${row["PCC"] || "-"}</td>
                <td>${row["Final Medical"] || "-"}</td>
                <td>${row["Certificate Attestation"] || "-"}</td>
                <td>${row["Biometric"] || "-"}</td>
                <td>${row["Trade Test"] || "-"}</td>
                <td>${row["Visa Stamping"] || "-"}</td>
            </tr>
        `;
    });

    summaryHtml += `
        <tr style="font-weight:bold;background:#f0f0f0;">
            <td style="text-align:left;">TOTAL</td>
            <td>${grandTotal["PSL"] || "-"}</td>
            <td>${grandTotal["Emigration"] || "-"}</td>
            <td>${grandTotal["Ticket"] || "-"}</td>
            <td>${grandTotal["Onboarding"] || "-"}</td>
            <td>${grandTotal["Signed Offer Letter"] || "-"}</td>
            <td>${grandTotal["Premedical"] || "-"}</td>
            <td>${grandTotal["PCC"] || "-"}</td>
            <td>${grandTotal["Final Medical"] || "-"}</td>
            <td>${grandTotal["Certificate Attestation" ] || "-"}</td>
            <td>${grandTotal["Biometric"] || "-"}</td>
            <td>${grandTotal["Trade Test"] || "-"}</td>
            <td>${grandTotal["Visa Stamping"] || "-"}</td>
        </tr>
    `;

    summaryHtml += `
            </tbody>
        </table>
        </div>
    </div>
    `;
}

        return html + summaryHtml;
    }
    window.downloadClosureSummaryTableS = function () {
        let table = document.getElementById("sri-summary-table");

        if (!table) {
            alert("Summary table not found");
            return;
        }

        let csv = [];

        let rows = table.querySelectorAll("tr");

        rows.forEach(row => {
            let cols = row.querySelectorAll("th, td");
            let rowData = [];

            cols.forEach(col => {
                let text = col.innerText.replace(/\n/g, " ").replace(/,/g, "");
                rowData.push(`"${text}"`);
            });

            csv.push(rowData.join(","));
        });

        let csvContent = csv.join("\n");

        let blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

        let link = document.createElement("a");
        let url = URL.createObjectURL(blob);

        link.setAttribute("href", url);
        link.setAttribute("download", "closure_summary.csv");

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
    }


    $(document).on('click', '.status-cell', function () {
        const closureName = $(this).data('name');
        const closureStatus = $(this).data('status');


        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Closure",
                name: closureName
            },
            callback: function (r) {
                if (!r.message) {
                    frappe.msgprint("Unable to fetch Closure details");
                    return;
                }

                const closure = r.message;
                const territory = closure.territory || "";
                const status = closure.status || "";
                const parent_territory = closure.parent_territory || "";
                const nationality = closure.nationality || "";
                const visa_state = closure.visa_state || "";
                const passport_no = closure.passport_no || "";
                const customer_so = closure.so_not_needed || "";




                let fields = [
                    {
                        label: 'Closure ID',
                        fieldname: 'closure_id',
                        fieldtype: 'Data',
                        read_only: 1,
                        default: closureName
                    },
                    {
                        label: 'Territory',
                        fieldname: 'territory',
                        fieldtype: 'Data',
                        read_only: 1,
                        default: territory
                    },
                    {
                        label: 'Current Status',
                        fieldname: 'current_status',
                        fieldtype: 'Data',
                        read_only: 1,
                        default: status
                    },
                    {
                        label: 'Passport Number',
                        fieldname: 'passport_no',
                        fieldtype: 'Data',
                        read_only: 1,
                        default: passport_no
                    },


                ];


                //fields based on territory 

                //Qatar

                if (territory === "Qatar") {

                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },

                        )

                    }

                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },



                        )


                    }
                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },



                        )


                    }
                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Declaration',
                                fieldname: 'declaration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },



                        );
                    }
                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },




                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },


                        )

                    }




                }

                //UAE and Abudhabi

                else if (territory === "UAE" && visa_state === "Abudhabi") {

                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },

                        )

                    }

                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status === "Final Medical") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa Stamping'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Visa Stamping") {

                        fields.push(

                            {
                                label: 'Stamped Visa',
                                fieldname: 'visa_stamping',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Declaration',
                                fieldname: 'declaration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },


                        );
                    }

                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },



                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }




                }

                //UAE && Dubai

                else if (territory === "UAE" && visa_state == "Dubai") {


                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },

                        )

                    }

                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Final Medical") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Final Medical Not Applicable',
                                fieldtype: 'Check',
                                fieldname: 'final_medical_not_applicable',
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Declaration',
                                fieldname: 'declaration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },


                        );
                    }

                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },




                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }






                }

                //Oman

                else if (territory === "Oman") {

                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },

                        )

                    }

                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Final Medical") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Declaration',
                                fieldname: 'declaration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },


                        );
                    }

                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },



                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }




                }

                //Kuwait customer_so == 0
                else if (territory === "Kuwait" && customer_so == 0) {

                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },

                        )

                    }
                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Premedical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Premedical") {

                        fields.push(

                            {
                                label: 'Pre-Medical',
                                fieldname: 'premedical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Final Medical") {

                        fields.push(

                            {
                                label: 'Medical Proof',
                                fieldname: 'custom_medical_proof',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa Stamping'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    // else if(status ==="Biometric"){

                    // fields.push(

                    //         {
                    //             label: 'Final Medical',
                    //             fieldname: 'final_medical',
                    //             fieldtype: 'Attach',
                    //             reqd:1
                    //         },


                    // )


                    // }

                    else if (status === "Visa Stamping") {

                        fields.push(

                            {
                                label: 'Stamped Visa',
                                fieldname: 'visa_stamping',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Declaration',
                                fieldname: 'declaration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },


                        );
                    }

                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }
                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },



                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }






                }



                //Kuwait customer_so == 1

                else if (territory === "Kuwait" && customer_so == 1) {

                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },

                        )

                    }
                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Premedical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Premedical") {

                        fields.push(

                            {
                                label: 'Pre-Medical',
                                fieldname: 'premedical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Final Medical") {

                        fields.push(

                            {
                                label: 'Medical Proof',
                                fieldname: 'custom_medical_proof',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Biometric'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Biometric") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa Stamping'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Visa Stamping") {

                        fields.push(

                            {
                                label: 'Stamped Visa',
                                fieldname: 'visa_stamping',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    // else if(status === "Emigration") {
                    //         fields.push(
                    //         {
                    //             label: 'Emigration',
                    //             fieldname: 'emigration',
                    //             fieldtype: 'Attach',
                    //             reqd:1
                    //         },

                    //         {
                    //             label: 'Declaration',
                    //             fieldname: 'declaration',
                    //             fieldtype: 'Attach',
                    //             reqd:1
                    //         },
                    //         {
                    //             label: 'Insurance',
                    //             fieldname: 'attach_insurance',
                    //             fieldtype: 'Attach',
                    //             reqd:1
                    //         },


                    //         {
                    //             label: 'Employment Contract',
                    //             fieldname: 'employment_contract',
                    //             fieldtype: 'Attach',
                    //             reqd:1
                    //         },

                    //         {
                    //             label: 'Candidate Feedback Form',
                    //             fieldname: 'candidate_feedback_form',
                    //             fieldtype: 'Attach',
                    //             reqd:1
                    //         },

                    //          {
                    //             label: 'Next Action',
                    //             fieldtype: 'Link',
                    //             fieldname: 'standard_remarks',
                    //             options:"Standard Remarks",
                    //             reqd: 1,
                    //             get_query: () => {
                    //                 return {
                    //                     filters: {
                    //                         status: 'Ticket'
                    //                     }
                    //                 };
                    //             }
                    //         },


                    //         );
                    //     }

                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },



                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }






                }




                //KSA

                else if (territory === "KSA") {


                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status === "Visa Stamping") {

                        fields.push(

                            {
                                label: 'Stamped Visa',
                                fieldname: 'visa_stamping',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }


                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Final Medical") {

                        fields.push(

                            {
                                label: 'Medical Proof',
                                fieldname: 'custom_medical_proof',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Biometric'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Final Medical" && nationality != "Indian") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                        )


                    }
                    else if (status == "Biometric") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Trade Test'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Declaration',
                                fieldname: 'declaration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },


                        );
                    }


                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },



                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }
                    else if (status === "Trade Test") {
                        fields.push(

                            {
                                label: 'Trade Test Attachment',
                                fieldname: 'custom_attachment',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa Stamping'
                                        }
                                    };
                                }
                            },

                        )

                    }







                }


                //Dammam,Jeddah,Riyadh

                else if (territory === "Dammam" || territory === "Jeddah" || territory === "Riyadh") {


                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Visa") {

                        fields.push(

                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'PCC'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "PCC") {

                        fields.push(

                            {
                                label: 'Pcc',
                                fieldname: 'pcc',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Final Medical") {

                        fields.push(

                            {
                                label: 'Medical Proof',
                                fieldname: 'custom_medical_proof',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Biometric'
                                        }
                                    };
                                }
                            },


                        )


                    }


                    else if (status == "Biometric") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa Stamping'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Visa Stamping") {

                        fields.push(

                            {
                                label: 'Stamped Visa',
                                fieldname: 'visa_stamping',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Declaration',
                                fieldname: 'declaration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },


                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },


                        );
                    }



                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },



                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }





                }



                //Iraq    

                else if (territory === "Iraq") {


                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Visa") {

                        fields.push(
                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },

                        );
                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },


                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },


                        )

                    }



                }


                //Bahrain

                else if (territory === "Bahrain") {

                    if (status === "PSL") {

                        fields.push(

                            {
                                label: 'IAF / CV / Client Form',
                                fieldname: 'irf',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Passport',
                                fieldname: 'passport',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Photo',
                                fieldname: 'photo',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Client Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status == "Client Offer Letter") {

                        fields.push(

                            {
                                label: 'Client Offer Letter',
                                fieldname: 'offer_letter',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Signed Offer Letter'
                                        }
                                    };
                                }
                            },


                        )


                    }
                    else if (status == "Signed Offer Letter") {

                        fields.push(

                            {
                                label: 'Signed Offer Letter',
                                fieldname: 'sol',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Final Medical'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Final Medical") {

                        fields.push(

                            {
                                label: 'Final Medical',
                                fieldname: 'final_medical',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Visa'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Visa") {

                        fields.push(
                            {
                                label: 'Entry Visa',
                                fieldname: 'visa',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Emigration'
                                        }
                                    };
                                }
                            },


                        )


                    }

                    else if (status === "Emigration") {
                        fields.push(
                            {
                                label: 'Emigration',
                                fieldname: 'emigration',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Insurance',
                                fieldname: 'attach_insurance',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Employment Contract',
                                fieldname: 'employment_contract',
                                fieldtype: 'Attach',
                                reqd: 1
                            },
                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Ticket'
                                        }
                                    };
                                }
                            },





                        );
                    }

                    else if (status === "Ticket") {

                        fields.push(

                            {
                                label: 'Ticket',
                                fieldname: 'ticket',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarding'
                                        }
                                    };
                                }
                            },



                        )


                    }

                    else if (status === "Onboarding") {
                        fields.push(

                            {
                                label: 'Candidate Feedback Form',
                                fieldname: 'candidate_feedback_form',
                                fieldtype: 'Attach',
                                reqd: 1
                            },

                            {
                                label: 'Onboarded',
                                fieldname: 'onboarded',
                                fieldtype: 'Check',
                                reqd: 1
                            },



                            {
                                label: 'Next Action',
                                fieldtype: 'Link',
                                fieldname: 'standard_remarks',
                                options: "Standard Remarks",
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: {
                                            status: 'Onboarded'
                                        }
                                    };
                                }
                            },

                        )

                    }







                }

                //dialog








                let d = new frappe.ui.Dialog({
                    title: status + ' Attachment',
                    fields: fields,
                    primary_action_label: 'Save',

                    async primary_action(values) {
                        try {

                            const overlay = document.createElement('div');
                            overlay.id = 'freeze-overlay';
                            Object.assign(overlay.style, {
                                position: 'fixed',
                                top: '0',
                                left: '0',
                                width: '100%',
                                height: '100%',
                                backgroundColor: 'rgba(0,0,0,0.5)',
                                zIndex: '9999',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'white',
                                fontSize: '24px'
                            });
                            overlay.innerText = 'Please wait...';
                            document.body.appendChild(overlay);

                            for (let f of Object.keys(values)) {
                                const value = values[f];
                                if (!value) continue;

                                if (d.fields_dict[f].df.fieldtype === 'Attach') {
                                    // Insert file first
                                    await frappe.call({
                                        method: "frappe.client.insert",
                                        args: {
                                            doc: {
                                                doctype: "File",
                                                file_url: value,
                                                attached_to_doctype: "Closure",
                                                attached_to_name: closureName,
                                                is_private: 0
                                            }
                                        }
                                    });
                                }

                                // Update field in Closure sequentially
                                await frappe.db.set_value("Closure", closureName, f, value);
                            }

                            frappe.show_alert({ message: __("Saved successfully!"), indicator: "green" });
                            d.hide();

                            if (status == "Visa") {
                                await frappe.db.get_value("Closure", { "name": closureName }, ["name", "so_created", "payment", "client_si", "candidate_si", "associate_si", "project", "customer", "account_manager", "candidate_owner", "task", "given_name", "mobile", "billing_currency", "custom_associate_billing_currency", "custom_client_billing_currency", "territory", "passport_no", "candidate_owner", "sa_id", "expected_doj", "service", "associate"]).then(r => {
                                    if (!r.message.so_created || r.message.so_created == 0) {
                                        if (r.message.payment === 'Client' && r.message.client_si <= 0) {
                                            msgprint("Please Enter Client Service Charge Value");
                                            setTimeout(() => {
                                                location.reload();
                                            }, 1000);
                                            return;
                                        }
                                        if (r.message.payment === 'Candidate' && r.message.candidate_si <= 0) {
                                            msgprint("Please Enter Candidate Service Charge Value");
                                            setTimeout(() => {
                                                location.reload();
                                            }, 1000);
                                            return;
                                        }
                                        if (r.message.payment === 'Associate' && r.message.associate_si <= 0) {
                                            msgprint("Please Enter Associate Service Charge Value");
                                            setTimeout(() => {
                                                location.reload();
                                            }, 1000);
                                            return;
                                        }
                                        if (r.message.payment === 'Both' &&
                                            (r.message.client_si <= 0 || r.message.candidate_si <= 0)) {
                                            msgprint("Please Enter Client and Candidate Service Charge Value");
                                            setTimeout(() => {
                                                location.reload();
                                            }, 1000);
                                            return;
                                        }
                                        frappe.confirm('Did you verify the payment terms?', function () {

                                            frappe.call({
                                                method: "jobpro.jobpro.doctype.closure.closure.create_sale_order",
                                                freeze: true,
                                                freeze_message: __("Creating Sales Order..."),
                                                args: {
                                                    closure: r.message.name,
                                                    project: r.message.project,
                                                    customer: r.message.customer,
                                                    reference_customer_: r.message.customer,
                                                    account_manager: r.message.account_manager,
                                                    delivery_manager: r.message.candidate_owner || '',
                                                    task: r.message.task,
                                                    candidate_name: r.message.given_name,
                                                    contact: r.message.mobile,
                                                    payment: r.message.payment,
                                                    billing_currency: r.message.billing_currency,
                                                    // client_sc: r.message.client_sc || '',
                                                    associate_cur: r.message.custom_associate_billing_currency,
                                                    client_cur: r.message.custom_client_billing_currency,
                                                    // candidate_sc: r.message.candidate_sc || '',
                                                    territory: r.message.territory,
                                                    passport_no: r.message.passport_no || '',
                                                    candidate_owner: r.message.candidate_owner || '',
                                                    sa_id: r.message.sa_id || '',
                                                    passport_number: r.message.passport_no,
                                                    expected_doj: r.message.expected_doj || '',
                                                    supplier: r.message.sa_id || '',
                                                    service: r.message.service,
                                                    // sc: r.message.candidate_sc ,
                                                    client_si: r.message.client_si,
                                                    candidate_si: r.message.candidate_si,
                                                    associate: r.message.associate || '',
                                                    associate_sc: r.message.associate_si || '',
                                                    associate_si: r.message.associate_si,
                                                },
                                                callback: function (i) {
                                                    frappe.msgprint(i.message);
                                                    frappe.db.set_value("Closure", closureName, "so_created", 1)
                                                        .then(() => {
                                                            frappe.show_alert("Sales Order created successfully")

                                                            setTimeout(() => {
                                                                location.reload();
                                                            }, 1000);


                                                        });
                                                }
                                            });

                                        });

                                    }
                                })


                            }
                            else {
                                location.reload();
                            }


                        } catch (err) {
                            frappe.msgprint({
                                title: __('Error'),
                                indicator: 'red',
                                message: err.message || err
                            });
                        } finally {
                            // Remove freeze overlay
                            const overlay = document.getElementById('freeze-overlay');
                            if (overlay) overlay.remove();



                        }
                    },

                    secondary_action_label: 'Cancel',
                    secondary_action() { d.hide(); }
                });




















                d.show();




            }
        });



    });




let GLOBAL_DATA = [];
loadUnifiedClosureData();

function loadUnifiedClosureData() {

    $("#closure-unified-container").html(`
        <div style="
            padding:20px;
            text-align:center;
        ">
            Loading...
        </div>
    `);

    frappe.call({

        method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.get_ptsr_data_closure_wise_all",

        callback: function(r) {

            let data = r.message || {};

            // =========================================
            // STATUS FILTER
            // =========================================

            let statuses = new Set();

            Object.keys(data).forEach(section => {

                (data[section] || []).forEach(row => {

                    if (row.status) {
                        statuses.add(row.status);
                    }

                });

            });

            $("#closure-status-filter").empty();

            $("#closure-status-filter").append(`
                <option value="">All Status</option>
            `);

            [...statuses].sort().forEach(status => {

                $("#closure-status-filter").append(`
                    <option value="${status}">
                        ${status}
                    </option>
                `);

            });

            // =========================================
            // MERGE DATA
            // =========================================

            const sections = [
                { key: "internal" },
                { key: "candidate" },
                { key: "agent" },
                { key: "supplier" },
                { key: "client" },
                { key: "nepal" },
                { key: "srilanka" }
            ];

            let mergedData = [];

            sections.forEach(sec => {

                if (data[sec.key] && data[sec.key].length) {

                    mergedData = mergedData.concat(data[sec.key]);

                }

            });

            // =========================================
            // TABLE HTML
            // =========================================

            let html = `
                <table class="table table-bordered">

                    <thead style="
                        position:sticky;
                        top:0;
                        background:#0F1568;
                        color:white;
                        z-index:10;
                    ">

                        <tr>

                            <th style="width:80px;">
                                S.NO
                            </th>

                            <th>
                                Customer
                            </th>

                            <th>VAC</th>
                            <th>SP</th>
                            <th>FP</th>
                            <th>SL</th>
                            <th>LP</th>

                        </tr>

                    </thead>

                    <tbody>
            `;

            if (mergedData.length) {

                html += buildInternalTable(mergedData);

            } else {

                html += `
                    <tr>
                        <td colspan="7"
                            style="
                                text-align:center;
                                color:red;
                                padding:20px;
                            ">
                            No Data Available
                        </td>
                    </tr>
                `;
            }

            html += `
                    </tbody>
                </table>
            `;

            $("#closure-unified-container").html(html);
        }

    });

}

// =========================================
// GROUP CUSTOMER
// =========================================

function groupByCustomer(data) {

    let grouped = {};

    data.forEach(d => {

        let key = d.customer || "Unknown";

        if (!grouped[key]) {

            grouped[key] = [];

        }

        grouped[key].push(d);

    });

    return grouped;

}

// =========================================
// MAIN BUILD
// =========================================

function buildInternalTable(data){

    let grouped = groupByCustomer(data);

    let html = "";

    let customerIndex = 1;

    Object.keys(grouped)
    .sort((a, b) => a.localeCompare(b))
    .forEach(customer => {

        let customerKey =
            "C_" + btoa(customer).replace(/=/g, "");

        let rows = grouped[customer];

        // =========================================
        // TOTALS
        // =========================================

        let totals = {
            tvac: 0,
            tsp: 0,
            tfp: 0,
            tsl: 0,
            tlp: 0
        };

        // PROJECT UNIQUE
        let projectMap = {};

        rows.forEach(r => {

            let pid =
                r.project_id ||
                r.project_name;

            if (!projectMap[pid]) {

                projectMap[pid] = r;

            }

        });

        Object.values(projectMap).forEach(p => {

            totals.tvac += Number(p.tvac || 0);
            totals.tsp  += Number(p.tsp || 0);
            totals.tfp  += Number(p.tfp || 0);
            totals.tsl  += Number(p.tsl || 0);
            totals.tlp  += Number(p.custom_t_lp || 0);

        });

        // =========================================
        // COUNTS
        // =========================================

        let totalTaskCount = rows.length;
        let totalClosureCount = rows.length;

        // =========================================
        // CUSTOMER ROW
        // =========================================

        html += `

        <tr style="
            background:#85819e;
            color:white;
            font-weight:bold;
        ">

            <td>
                ${customerIndex++}
            </td>

            <td style="text-align:left;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        ${customer}
                    </div>
                    <div>
                    <span class="customer-task-toggle" data-key="${customerKey}"
                        style="cursor:pointer;margin-right:20px;display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:#1E3A8A;" title="Task View">
                        <img src="https://cdn-icons-png.flaticon.com/128/2921/2921222.png"
                            style="width:18px;height:18px;filter:brightness(0) invert(1);">
                    </span>
                    <span class="customer-closure-toggle" data-key="${customerKey}"
                        style="cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:#0F766E;" title="Closure View">
                        <img src="https://cdn-icons-png.flaticon.com/128/681/681494.png"
                            style="width:18px;height:18px;filter:brightness(0) invert(1);">
                    </span>
                    </div>
                </div>
            </td>
            <td>${totals.tvac}</td>
            <td>${totals.tsp}</td>
            <td>${totals.tfp}</td>
            <td>${totals.tsl}</td>
            <td>${totals.tlp}</td>
        </tr>
        `;

        // =========================================
        // TASK TABLE
        // =========================================

        html += `

        <tr class="
            task-table-row
            customer-task-${customerKey}
        "
        style="display:none;">

            <td colspan="7">

                <div class="ptsr-horizontal-scroll">

                    <table class="
                        table table-bordered table-sm
                    ">

                        <thead style="
                            background:#99ccff !important;
                            color:black !important;
                        ">

                            <tr>

                                <th>S.No</th>
                                <th>Project</th>
                                <th>Position</th>

                                <th>PSL</th>
                                <th>COL</th>
                                <th>SOL</th>
                                <th>VISA</th>
                                <th>PM</th>
                                <th>PCC</th>
                                <th>CA</th>
                                <th>FM</th>
                                <th>BIO</th>
                                <th>QVP</th>
                                <th>TT</th>
                                <th>VS</th>
                                <th>POE</th>
                                <th>TKT</th>
                                <th>OB</th>
                                <th>OD</th>

                            </tr>

                        </thead>

                        <tbody>
        `;

        // =========================================
        // TASK GROUP
        // =========================================

        let taskGrouped = {};

        rows.forEach(r => {

            let key =
                (r.project_name || "") +
                "##" +
                (r.task_subject || "");

            if (!taskGrouped[key]) {

                taskGrouped[key] = [];

            }

            taskGrouped[key].push(r);

        });

        let taskIndex = 1;

        Object.keys(taskGrouped).forEach(key => {

            let taskRows = taskGrouped[key];

            let first = taskRows[0];

            function getCount(statusName) {

                return taskRows.filter(r =>
                    (r.status || "").trim()
                    === statusName
                ).length;

            }

            function statusCell(value) {

                if (value > 0) {

                    return `
                        <span style="
                            color:green;
                            font-weight:bold;
                        ">
                            ${value}
                        </span>
                    `;

                }

                return "-";

            }

            html += `

            <tr class="task-data-row" 
            data-filter=" 
            ${getCount('PSL') > 0 ? 'PSL TEAMPRO' : ''} 
            ${getCount('Client Offer Letter') > 0 ? 'POL Customer' : ''} 
            ${getCount('Signed Offer Letter') > 0 ? 'SOL Candidate' : ''} 
            ${getCount('Visa') > 0 ? 'VISA Customer' : ''} 
            ${getCount('Premedical') > 0 ? 'PM Candidate' : ''} 
            ${getCount('PCC') > 0 ? 'PCC Candidate' : ''} 
            ${getCount('Certificate Attestation') > 0 ? 'CA TEAMPRO' : ''} 
            ${getCount('Final Medical') > 0 ? 'FM Candidate' : ''} 
            ${getCount('Biometric') > 0 ? 'BIO Candidate' : ''} 
            ${getCount('QVP') > 0 ? 'QVP Candidate' : ''} 
            ${getCount('Trade Test') > 0 ? 'TT Candidate' : ''} 
            ${getCount('Visa Stamping') > 0 ? 'VS Supplier' : ''} 
            ${getCount('Emigration') > 0 ? 'POE TEAMPRO' : ''} 
            ${getCount('Ticket') > 0 ? 'TKT TEAMPRO' : ''} 
            ${getCount('Onboarding') > 0 ? 'OB TEAMPRO' : ''} 
            ${getCount('Onboarded') > 0 ? 'OD TEAMPRO' : ''} ">

                <td>
                    ${taskIndex++}
                </td>

                <td>
                    ${first.project_name || '-'}
                </td>

                <td>
                    ${first.task_subject || '-'}
                </td>

                <td>${statusCell(getCount("PSL"))}</td>

                <td>${statusCell(getCount("Client Offer Letter"))}</td>

                <td>${statusCell(getCount("Signed Offer Letter"))}</td>

                <td>${statusCell(getCount("Visa"))}</td>

                <td>${statusCell(getCount("Premedical"))}</td>

                <td>${statusCell(getCount("PCC"))}</td>

                <td>${statusCell(getCount("Certificate Attestation"))}</td>

                <td>${statusCell(getCount("Final Medical"))}</td>

                <td>${statusCell(getCount("Biometric"))}</td>

                <td>${statusCell(getCount("QVP"))}</td>

                <td>${statusCell(getCount("Trade Test"))}</td>

                <td>${statusCell(getCount("Visa Stamping"))}</td>

                <td>${statusCell(getCount("Emigration"))}</td>

                <td>${statusCell(getCount("Ticket"))}</td>

                <td>${statusCell(getCount("Onboarding"))}</td>

                <td>${statusCell(getCount("Onboarded"))}</td>

            </tr>
            `;

        });

        html += `

                        </tbody>

                    </table>

                </div>

            </td>

        </tr>
        `;

        // =========================================
        // CLOSURE TABLE
        // =========================================

        html += `

        <tr class="
            closure-table-row
            customer-closure-${customerKey}
        "
        style="display:none;">

            <td colspan="7">

                <div class="ptsr-horizontal-scroll">

                    <table class="
                        table table-sm table-bordered
                    ">

                        <thead style="
                            background:#99ccff !important;
                            color:black !important;
                        ">

                            <tr>

                                <th>S.No</th>
                                <th>Project</th>
                                <th>CLID</th>
                                <th>Name</th>
                                <th>PP Number</th>
                                <th>Contact</th>
                                <th>Status</th>
                                <th>Age</th>
                                <th>Last Update</th>
                                <th>Next Action</th>
                                <th>Next Action On</th>
                                <th>Remark</th>

                            </tr>

                        </thead>

                        <tbody>
        `;

        let subIndex = 1;

        rows.forEach(row => {

            html += `

            <tr class="closure-data-row"
                data-status="${row.status || ''}">

                <td>
                    ${subIndex++}
                </td>

                <td>
                    ${row.project_name || '-'}
                </td>

                <td>

                    <a href="
                        https://erp.teamproit.com/app/closure/${row.name}
                    "
                    target="_blank">

                        ${row.name || '-'}

                    </a>

                </td>

                <td>
                    ${row.given_name || '-'}
                </td>

                <td>
                    ${row.passport_no || '-'}
                </td>

                <td>
                    ${row.mobile || '-'}
                </td>

                <td>
                    ${row.status || '-'}
                </td>

                <td>
                    ${calculateAgeClosure(
                        row.custom_history
                    ) || '-'}
                </td>

                <td>
                    ${formatDate(
                        row.last_updated_on
                    ) || '-'}
                </td>

                <td>
                    ${row.std_remarks || '-'}
                </td>

                <td>
                    ${formatDate(
                        row.custom_next_follow_up_on
                    ) || '-'}
                </td>

                <td>
                    ${row.remark || '-'}
                </td>

            </tr>
            `;

        });

        html += `

                        </tbody>

                    </table>

                </div>

            </td>

        </tr>
        `;

    });

    return html;

}

// =========================================
// CUSTOMER EXPAND
// =========================================

$(document).on("click", ".toggle", function () {

    let key = $(this).data("key");

    let isOpen =
        $(".customer-task-" + key).is(":visible") ||
        $(".customer-closure-" + key).is(":visible");

    if (isOpen) {

        $(".customer-task-" + key).hide();
        $(".customer-closure-" + key).hide();

        $(this).text("+");

    } else {

        $(".customer-task-" + key).show();

        $(this).text("-");

    }

});

// =========================================
// CUSTOMER TASK TOGGLE
// =========================================

$(document).on("click", ".customer-task-toggle", function () {

    let key = $(this).data("key");

    $(".customer-closure-" + key).hide();

    $(".customer-task-" + key).toggle();

});

// =========================================
// CUSTOMER CLOSURE TOGGLE
// =========================================

$(document).on("click", ".customer-closure-toggle", function () {

    let key = $(this).data("key");

    $(".customer-task-" + key).hide();

    $(".customer-closure-" + key).toggle();

});

// =========================================
// TOP TASK VIEW BUTTON
// =========================================

let allTaskOpened = false;

$(document).on("click", "#task-view-btn", function () {

    allTaskOpened = !allTaskOpened;

    if (allTaskOpened) {

        $(".task-table-row").show();

        $(".closure-table-row").hide();

        $(".toggle").text("-");

        $("#pending-status-filter").show();

    } else {

        $(".task-table-row").hide();

        $(".toggle").text("+");

        $("#pending-status-filter").hide();

    }

});

// =========================================
// TOP CLOSURE VIEW BUTTON
// =========================================

let allClosureOpened = false;

$(document).on("click", "#closure-view-btn", function () {

    allClosureOpened = !allClosureOpened;

    if (allClosureOpened) {

        $(".closure-table-row").show();

        $(".task-table-row").hide();

        $(".toggle").text("-");

        $("#closure-status-filter").show();

    } else {

        $(".closure-table-row").hide();

        $(".toggle").text("+");

        $("#closure-status-filter").hide();

    }

});

// =========================================
// STATUS FILTER
// =========================================

$(document).on("change", "#closure-status-filter", function () {

    let selected =
        $(this).val().trim();

    if (!selected) {

        $(".closure-data-row").show();

        return;
    }

    $(".closure-data-row").hide();

    $(`.closure-data-row[data-status="${selected}"]`).show();

});

// =========================================
// PENDING STATUS FILTER
// =========================================

$(document).on("change", "#pending-status-filter", function () {

    let selected = $(this).val().trim();

    // SHOW ALL
    if (!selected) {

        $(".task-data-row").show();

        return;
    }

    // HIDE ALL FIRST
    $(".task-data-row").hide();

    // SHOW ONLY MATCHED ROWS
    $(`.task-data-row[data-filter*="${selected}"]`).show();

});




    function calculateAgeInDays(creationDate) {
        if (!creationDate) return '-';
        const created = new Date(creationDate);
        const today = new Date();
        const diffTime = today - created;
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        return `${diffDays}`;
    }




    function calculateAgeClosure(custom_history) {
        if (!custom_history || custom_history.length === 0) return '-';

        try {

            const validDates = custom_history
                .map(item => item.date)
                .filter(date => !!date)
                .map(date => new Date(date));

            if (validDates.length === 0) return '-';


            const latestDate = new Date(Math.max(...validDates.map(d => d.getTime())));


            const today = new Date();
            const todayDateOnly = new Date(today.getFullYear(), today.getMonth(), today.getDate());
            const latestDateOnly = new Date(latestDate.getFullYear(), latestDate.getMonth(), latestDate.getDate());

            const diffTime = todayDateOnly - latestDateOnly;
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            return `${diffDays}`;
        } catch (error) {
            console.error("Error calculating age:", error);
            return '-';
        }
    }




    function generatePTSRTablesothers(data, title) {

        let html = `
        <div class="ptsr-table-section" data-group-title="${title}">	
            <style>
                 .ptsr-scroll-container {
                    max-height: 600px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                }

                .ptsr-horizontal-scroll {
                    overflow-x: auto;
                    overflow-y: auto;
                    width: 100%;
                }

                .ptsr-horizontal-scroll table {
                    min-width: 100px; 
                    border-collapse: collapse;
                    width: 100%;}
  
                table { width: 100%; border-collapse: collapse !important;overflow-y: auto;overflow-x: auto; }
                table, th, td { border: 1px solid black !important; padding: 8px; text-align: center; }
                

                th { background-color: #0F1568 !important; position: sticky; top: 0; color: white !important; z-index: 2; }
                
                    .project-row:nth-of-type(odd) {
                    background-color: #e6f2f1;
                }
                .project-row:nth-of-type(even) {
                    background-color: #ffffff;
                }
                   /* Table cell default */
table td {
    max-width: 250px;
    overflow: auto;
    text-overflow: ellipsis;
    vertical-align: middle;
}


                .task-header td { position: sticky; top: 41px; background-color: #d3d3d3 !important; z-index: 1; }
                .left-align { text-align: left !important; }
                .toggle-btn { cursor: pointer; font-weight: bold; color: #0F1568; }
            </style>
            <div class="ptsr-scroll-container" style="background-color: #f5f5f5;border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;margin-left: 15px;margin-right: 15px;">
            <div class="ptsr-horizontal-scroll" style="max-height:600px; overflow-y:auto;position: sticky; top: 0; z-index: 1;"" >
                
                    


                     <div style="display: flex;  justify-content: space-between; align-items: center; background: white; padding: 10px;">
            <h4 style="margin-left: 700px;">${title}</h4>


                
            
        </div>

        <div style="display: flex; gap: 10px; align-items: center; justify-content:end; margin:5px;">
                
                <select   class=" territory-select form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Territory</option>
                </select>

                <select id="status-select" class="form-control" style="width: 180px; border:1px solid black;">
                    <option value="">Select Status</option>
                    <option value="PSL">PSL</option>
                    <option value="Emigration">Emigration</option>
                    <option value="Visa Stamping">Visa Stamping</option>
                    <option value="Onboarding">Onboarding</option>
                    <option value="Signed Offer Letter">Signed Offer Letter</option>
                    <option value="Premedical">Premedical</option>
                    <option value="PCC">PCC</option>
                    <option value="Final Medical">Final Medical</option>
                    <option value="Client Offer Letter">Client Offer Letter</option>
                    <option value="Visa">Visa</option>
                    <option value="Ticket">Ticket</option>






                </select>

                 

                


                <select   class=" client-select form-control" style="width: 600px; border:1px solid black;" >
                    <option value="">Select Client</option>

                </select>
                <button id="apply-filter" class="btn btn-primary">Apply</button>
                <button id="download-closure" class="btn btn-primary">Download</button>
            </div>

    
                    
                    
                    
                    </span>
                    </h4>
                    
                    

            <table ">
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>CLID</th>
                    <th>Name</th>
                    <th>PP Number</th>
                    <th>Territory</th>
                    <th>Status</th>
                    <th>Client</th>
                    <th>Age</th>
                </tr>
            </thead>
            <tbody>`;


        if (data.length > 0) {


            data.forEach((closure, index) => {


                let color = (index % 2 === 0) ? "#ffffff" : "#e6f2f1";

                html += `
        <tr class="project-header" style="background-color:${color};">
            <td>${index + 1}</td>  <!-- Serial number is simply the index + 1 -->
            <td>${closure.name || '-'}</td>
            <td>${closure.given_name || '-'}</td>
            <td>${closure.passport_no || '-'}</td>
            <td>${closure.territory || '-'}</td>
            <td>${closure.status || '-'}</td>
            <td style="text-align:left !important;" >${closure.customer || '-'}</td>
            <td>${calculateAgeClosure(closure.custom_history)}</td>
            
        </tr>`;


            });



        }

        else {
            html += `
            <tr style="font-weight:bold; background-color:#d0d0d0;">
            <td colspan="8"><center>No Data Available</center></td>
            </tr>`;
        }

        html += `</tbody></table></div></div></div>`;
        return html;
    }







    function updateDateTime() {
        const now = new Date();
        const dateStr = now.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        const timeStr = now.toLocaleTimeString();
        document.getElementById('current-datetime').innerHTML = `${dateStr} | ${timeStr}`;
    }
    updateDateTime();
    setInterval(updateDateTime, 1000);
    function renderSimpleCard(selector, label, value, curr = null, color = 'green') {

        if (curr) {
            const formattedTotal = formatMoney(curr);

            $(wrapper).find(selector).html(`
        <div class="card-inner">
            <h3>${label}</h3>
            <div class="amount" style="color: ${color}">${value}(${formattedTotal})</div>
        </div>
    `);
        }
        else {

            $(wrapper).find(selector).html(`
        <div class="card-inner">
            <h3>${label}</h3>
            <div class="amount" style="color: ${color}">${value}</div>
        </div>
    `);

        }
    }


    function formatMoney(value) {
        if (value >= 10000000) {
            return (value / 10000000).toFixed(1) + ' Cr';
        } else if (value >= 100000) {
            return (value / 100000).toFixed(1) + ' L';
        } else if (value >= 1000) {
            return (value / 1000).toFixed(1) + ' K';
        } else {
            return value;
        }
    }

    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_teampro_closure_count",
        callback: r => renderSimpleCard('.teampro-closure-count-card', 'Internal', r.message || 0)
    });

    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_candidate_agent_closure_count",
        callback: r => renderSimpleCard('.candidate-agent-closure-count-card', 'Candidate', r.message || 0)
    });
    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_agent_closure_count",
        callback: r => renderSimpleCard('.agent-closure-count-card', 'Agent', r.message || 0)
    });
    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_supp_agent_closure_count",
        callback: r => renderSimpleCard('.supp-closure-count-card', 'Supplier', r.message || 0)
    });

    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_client_closure_count",
        callback: r => renderSimpleCard('.client-closure-count-card', 'Client', r.message || 0)
    });

    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_so_pending_count",
        callback: r => renderSimpleCard('.so_pending', 'SO Pending', r.message.count || 0, r.message.total || 0)
    });

    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_nepal_closure_count",
        callback: r => renderSimpleCard('.nepal-closure-count-card', 'Nepal', r.message || 0)
    });
    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_srilanka_closure_count",
        callback: r => renderSimpleCard('.srilanka-closure-count-card', 'Srilanka', r.message || 0)
    });










    function renderTatCrossedCandidateTable() {
        $("#candidate-matrix-table").html(`<div style="padding: 20px; font-weight: bold;">Loading TAT Crossed Candidates...</div>`);

        frappe.call({
            method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_candidates_tat_crossed_from_history",
            callback: function (r) {
                if (r.message && Object.keys(r.message).length > 0) {
                    let html = `<table class="table table-bordered" style="font-size: 13px; margin-top: 20px;">
                    <thead style="background-color: #002060;color: white;">
                        <tr>
                            <th>Project Name</th>
                            <th>Territory</th>
                            <th>Status</th>
                            <th>Subject</th>
                            <th>#TAT Crossed</th>
                        </tr>
                    </thead>
                    <tbody>`;

                    Object.entries(r.message).forEach(([project_name, data]) => {
                        (data.status_map || []).forEach(statusData => {
                            const subject = statusData.subject || "-";
                            const count = statusData.count || 0;
                            const ids = statusData.candidates.map(c => `"${c.closure_id}"`); // wrap each ID in quotes

                            html += `
                            <tr>
                                <td style="color:#002060; font-weight: 600;">${project_name}</td>
                                <td>${data.territory || "-"}</td>
                                <td>${statusData.status}</td>
                                <td>${subject}</td>
                                <td style="text-align:center;">
                                    <a href="javascript:void(0)" onclick='frappe.set_route("List", "Candidate", { "name": ["in", [${ids.join(",")}] ] })' style="font-weight:bold;">
                                        ${count}
                                    </a>
                                </td>
                            </tr>`;
                        });
                    });

                    html += `</tbody></table>`;
                    $("#candidate-matrix-table").html(html);
                } else {
                    $("#candidate-matrix-table").html(`<div style="padding: 20px; font-weight: bold; color: #888;">No TAT Crossed Candidates Found</div>`);
                }
            }
        });
    }





    function formatDate(dateStr) {
        if (!dateStr) return "";
        const d = new Date(dateStr);
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0'); // Month is 0-based
        const year = d.getFullYear();
        return `${day}-${month}-${year}`;
    }

    function renderClosureMatrix(data) {
        const statuses = [
            "PSL", "Waitlisted", "Sales Order", "Client Offer Letter", "Signed Offer Letter",
            "Visa", "Premedical", "PCC", "Certificate Attestation", "Trade Test", "Final Medical",
            "Biometric", "Visa Stamping", "Emigration", "Ticket", "Onboarding", "Onboarded"
        ];

        const statusShortCodes = {
            "PSL": "PSL", "Waitlisted": "WL", "Sales Order": "SO", "Client Offer Letter": "COL",
            "Signed Offer Letter": "SOL", "Visa": "Visa", "Premedical": "PM", "PCC": "PCC",
            "Certificate Attestation": "CA", "Trade Test": "TT", "Final Medical": "FM",
            "Biometric": "BIO", "Visa Stamping": "VS", "Emigration": "POE", "Ticket": "TKT",
            "Onboarding": "OB", "Onboarded": "OBD"
        };

        const territoryMap = {};
        const closureMap = {};

        data.forEach(row => {
            const terr = row.territory;
            const status = row.status;
            if (!territoryMap[terr]) territoryMap[terr] = {};
            territoryMap[terr][status] = {
                count: row.count || 0,
                tat_crossed_count: row.tat_crossed_count || 0,
                so_not_created_count: row.so_not_created_count || 0,
                closure_ids: row.closure_ids || []
            };
            const key = `${terr}__${status}`;
            closureMap[key] = row.closure_ids || [];
        });

        let html = `
<style>
    #closure-matrix-wrapper {
        overflow: auto;
        width: 100%;
        max-height: 500px;
    }
    #closure-matrix-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: auto;
    }
    #closure-matrix-table thead th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: #002060;
        color: white;
        text-align: center;
    }
    #closure-matrix-table td, #closure-matrix-table th {
        text-align: center;
        padding: 6px;
        border: 1px solid #ccc;
    }
    #closure-matrix-table tbody tr:nth-child(odd) {
        background-color: #d9d9d9;
    }
    .project-row td {
        background-color: #f1f9ff;
    }
    #closure-matrix-table tfoot tr {
        background-color: #d0e3f0;
        color: #000;
        font-weight: bold;
    }
    




</style>

<div id="closure-matrix-wrapper">
<table class="table table-bordered" id="closure-matrix-table" style="font-size: 13px; white-space: nowrap;">
    <thead>
        <tr>
            <th>Territory</th>
            ${statuses.map(s => `<th title="${s}">${statusShortCodes[s] || s}</th>`).join('')}
            <th>Total</th>
        </tr>
    </thead>
    <tbody>`;

        for (let terr in territoryMap) {
            let rowTotal = 0;
            let rowSoNotCreatedTotal = 0;
            let rowTotals = 0;
            statuses.forEach(status => {
                const count = territoryMap[terr][status]?.count || 0;
                rowTotals += count;
            });
            if (rowTotals === 0) continue;

            html += `<tr>
            <td class="territory-cell" style="cursor:pointer; text-align:left;" data-territory="${terr}">
                <span class="toggle-icon" style="font-weight:bold; color:#002060; margin-right:4px;float:left;">[+]</span>
                <strong>${terr}</strong>
            </td>`;

            statuses.forEach(status => {
                const statusData = territoryMap[terr][status] || { count: 0, tat_crossed_count: 0 };
                const count = statusData.count;
                const crossed = statusData.tat_crossed_count;
                const soNotCreated = statusData.so_not_created_count || 0;
                const key = `${terr}__${status}`;
                rowTotal += count;
                rowSoNotCreatedTotal += soNotCreated;



                const displayCount = count === 0 ? "-" : count;
                const displayCrossed = crossed === 0 ? "-" : crossed;

                const displaySoNotCreated = soNotCreated === 0 ? "-" : soNotCreated;





                if (crossed > 0) {
                    html += `<td>${displayCount} / <a href="#" class="tat-link" data-key="${key}" style="color:red;font-weight:bold;">${displayCrossed}</a>&nbsp;<span style="color:#0070C0;">(${displaySoNotCreated})</span></td>`;
                } else {
                    html += `<td>${displayCount} / <span style="color:gray;">${displayCrossed}</span>&nbsp;<span style="color:#0070C0;">(${displaySoNotCreated})</span></td>`;
                }
            });


            const displayRowSoNotCreated = rowSoNotCreatedTotal === 0 ? "-" : rowSoNotCreatedTotal;

            html += `<td style="font-weight: bold;">${rowTotal === 0 ? "-" : rowTotal}&nbsp;<span style="color:#0070C0;">(${displayRowSoNotCreated})</span></td></tr>`;
        }

        // Grand totals
        let grandTotals = {};
        let grandSoNotCreatedTotals = {};
        let grandTotalSum = 0;
        let grandSoNotCreatedSum = 0;
        statuses.forEach(status => {
            grandTotals[status] = 0,
                grandSoNotCreatedTotals[status] = 0;
        }
        );
        for (let terr in territoryMap) {
            statuses.forEach(status => {
                const count = territoryMap[terr][status]?.count || 0;
                const soNotCreated = territoryMap[terr][status]?.so_not_created_count || 0;
                grandTotals[status] += count;
                grandSoNotCreatedTotals[status] += soNotCreated;
                grandTotalSum += count;
                grandSoNotCreatedSum += soNotCreated;
            });
        }

        html += `</tbody>
    <tfoot><tr>
        <td>Grand Total</td>
        ${statuses.map(status => `<td>${grandTotals[status] === 0 ? "-" : grandTotals[status]}&nbsp;<span style="color:#0070C0;">(${grandSoNotCreatedTotals[status] === 0 ? "-" : grandSoNotCreatedTotals[status]})</span></td>`).join("")}
        <td>${grandTotalSum === 0 ? "-" : grandTotalSum}&nbsp;<span style="color:#0070C0;">(${grandSoNotCreatedSum === 0 ? "-" : grandSoNotCreatedSum})</span></td>
    </tr></tfoot>
</table></div>`;

        $("#closure-matrix-table").html(html);

        // TAT crossed link (territory-level)
        $(".tat-link").on("click", function (e) {

            e.preventDefault();
            const key = $(this).data("key");
            const ids = closureMap[key] || [];
            if (!ids.length) return frappe.msgprint("No TAT crossed Closure records.");
            frappe.set_route("List", "Closure", { name: ["in", ids] });
        });


        $(".territory-cell").on("click", function () {
            const $cell = $(this);
            const $row = $cell.closest("tr");
            const territory = $cell.data("territory");
            const $icon = $cell.find(".toggle-icon");

            // Collapse if open
            if ($row.next().hasClass("project-row")) {
                while ($row.next().hasClass("project-row")) {
                    $row.next().remove();
                }
                $icon.text("[+]");
                return;
            }

            $(".project-row").remove();
            $(".toggle-icon").text("[+]");

            $icon.text("[−]");

            frappe.call({
                method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_project_details_for_territory",
                args: { territory },
                callback: function (r) {
                    if (r.message && r.message.length) {
                        let projectMap = {};
                        let projectClosureMap = {};
                        let rowSoNotCreatedTotal_e = 0

                        r.message.forEach(row => {
                            const projectId = row.project;
                            const status = row.status;

                            if (!projectMap[projectId]) {
                                projectMap[projectId] = {
                                    name: row.project_name || row.project,
                                    statusCounts: {}
                                };
                            }
                            projectMap[projectId].statusCounts[status] = {
                                count: row.count || 0,
                                tat_crossed_count: row.tat_crossed_count || 0,
                                closure_ids: row.closure_ids || [],
                                so_not_created_count: row.so_not_created_count || 0
                            };
                            projectClosureMap[`${projectId}__${status}`] = row.closure_ids || [];
                        });

                        Object.entries(projectMap).forEach(([projectId, data]) => {
                            const { name, statusCounts } = data;
                            let total = 0;
                            let rowSoNotCreatedTotal_e = 0;

                            statuses.forEach(status => {
                                total += statusCounts[status]?.count || 0;
                            });
                            if (total === 0) return;

                            let breakdownRow = `<tr class="project-row">`;
                            breakdownRow += `<td style="text-align:left;padding-left:20px;">
                            <a href="/app/project/${projectId}" target="_blank" style="font-weight:bold;">${name}</a>
                        </td>`;

                            statuses.forEach(status => {
                                const count = statusCounts[status]?.count || 0;
                                const crossed = statusCounts[status]?.tat_crossed_count || 0;
                                const key = `${projectId}__${status}`;
                                const soNotCreated_e = statusCounts[status]?.so_not_created_count || 0;

                                const displayCount_e = count === 0 ? "-" : count;
                                const displayCrossed_e = crossed === 0 ? "-" : crossed;

                                const displaySoNotCreated_e = soNotCreated_e === 0 ? "-" : soNotCreated_e;

                                rowSoNotCreatedTotal_e += soNotCreated_e;



                                if (crossed > 0) {
                                    breakdownRow += `<td>${displayCount_e} / <a href="#" class="tat-link-pro" data-key="${key}" style="color:red;font-weight:bold;">${displayCrossed_e}</a>&nbsp;<span style="color:#0070C0;">(${displaySoNotCreated_e})</span></td>`;
                                } else {
                                    breakdownRow += `<td>${displayCount_e} / <span style="color:gray;">${displayCrossed_e}</span>&nbsp;<span style="color:#0070C0;">(${displaySoNotCreated_e})</span></td>`;
                                }
                            });

                            const displayRowSoNotCreated_e = rowSoNotCreatedTotal_e === 0 ? "-" : rowSoNotCreatedTotal_e;

                            breakdownRow += `<td style="font-weight:bold;">${total === 0 ? "-" : total}&nbsp;<span style="color:#0070C0;">(${displayRowSoNotCreated_e})</span></td></tr>`;
                            $row.after(breakdownRow);
                        });

                        // Project-level TAT links
                        $(".tat-link-pro").off("click").on("click", function (e) {
                            e.preventDefault();
                            const key = $(this).data("key");
                            const ids = projectClosureMap[key] || [];
                            if (!ids.length) return frappe.msgprint("No TAT crossed Closure records.");
                            frappe.set_route("List", "Closure", {
                                name: ["in", ids]
                            });
                        });
                    } else {
                        frappe.msgprint("No project data for this territory.");
                    }
                }
            });
        });



        // Populate ALL territory dropdowns



    }
    frappe.call({
        method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.get_territory_status_matrix",
        callback: function (r) {
            if (r.message) {
                renderClosureMatrix(r.message);
            } else {
                $("#closure-matrix-table").html("No data found.");
            }
        }
    });
    document.getElementById("download-closure-table").addEventListener("click", function () {
        frappe.call({
            method: "jobpro.jobpro.page.rec_i_dashboard.rec_i_dashboard.download_closure_matrix_with_projects",
            callback: function (r) {
                if (r.message) {
                    var element = document.createElement('a');
                    element.setAttribute('href', 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + r.message);
                    element.setAttribute('download', 'Closure_Matrix.xlsx');
                    document.body.appendChild(element);
                    element.click();
                    document.body.removeChild(element);
                }
            }
        });
    });



    function downloadTeamproExcel() {
        const status = ["PSL", "Emigration", "Ticket", "Onboarding"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_teampro_excel",
            args: {
                status: JSON.stringify(status)
            },
            callback: function (r) {
                if (r.message && r.message.data) {
                    const link = document.createElement("a");
                    link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
                    link.download = r.message.filename || "teampro_closure.xlsx";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    frappe.msgprint("No data received for download.");
                }
            },
            error: function (err) {
                console.error("Download error:", err);
                frappe.msgprint("Something went wrong during download.");
            }
        });
    }

    function downloadCandidateExcel() {
        const status = ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_candidate_excel",
            args: {
                status: JSON.stringify(status)
            },
            callback: function (r) {
                if (r.message && r.message.data) {
                    const link = document.createElement("a");
                    link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
                    link.download = r.message.filename || "candidate_closure.xlsx";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    frappe.msgprint("No data received for download.");
                }
            },
            error: function (err) {
                console.error("Download error:", err);
                frappe.msgprint("Something went wrong during download.");
            }
        });
    }
    function downloadAgentExcel() {
        const status = ["Signed Offer Letter", "Premedical", "PCC", "Final Medical"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_agent_excel",
            args: {
                status: JSON.stringify(status)
            },
            callback: function (r) {
                if (r.message && r.message.data) {
                    const link = document.createElement("a");
                    link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
                    link.download = r.message.filename || "agent_closure.xlsx";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    frappe.msgprint("No data received for download.");
                }
            },
            error: function (err) {
                console.error("Download error:", err);
                frappe.msgprint("Something went wrong during download.");
            }
        });
    }
    function downloadSupplierExcel() {
        const status = ["Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_supplier_excel",
            args: {
                status: JSON.stringify(status)
            },
            callback: function (r) {
                if (r.message && r.message.data) {
                    const link = document.createElement("a");
                    link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
                    link.download = r.message.filename || "candidate_closure.xlsx";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    frappe.msgprint("No data received for download.");
                }
            },
            error: function (err) {
                console.error("Download error:", err);
                frappe.msgprint("Something went wrong during download.");
            }
        });
    }


    function downloadClientExcel() {
        const status = ["Client Offer Letter", "Visa"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_client_excel",
            args: {
                status: JSON.stringify(status)
            },
            callback: function (r) {
                if (r.message && r.message.data) {
                    const link = document.createElement("a");
                    link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
                    link.download = r.message.filename || "client_closure.xlsx";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    frappe.msgprint("No data received for download.");
                }
            },
            error: function (err) {
                console.error("Download error:", err);
                frappe.msgprint("Something went wrong during download.");
            }
        });
    }


    function downloadNepalExcel() {
        const status = ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_nepal_excel",
            args: {
                status: JSON.stringify(status)
            },
            callback: function (r) {
                if (r.message && r.message.data) {
                    const link = document.createElement("a");
                    link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
                    link.download = r.message.filename || "nepal_closure.xlsx";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    frappe.msgprint("No data received for download.");
                }
            },
            error: function (err) {
                console.error("Download error:", err);
                frappe.msgprint("Something went wrong during download.");
            }
        });
    }


    function downloadSrilankaExcel() {
        const status = ["PSL", "Emigration", "Ticket", "Onboarding", "Signed Offer Letter", "Premedical", "PCC", "Final Medical", "Certificate Attestation", "Biometric", "Trade Test", "Visa Stamping"];

        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_srilanka_excel",
            args: {
                status: JSON.stringify(status)
            },
            callback: function (r) {
                if (r.message && r.message.data) {
                    const link = document.createElement("a");
                    link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
                    link.download = r.message.filename || "srilanka_closure.xlsx";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    frappe.msgprint("No data received for download.");
                }
            },
            error: function (err) {
                console.error("Download error:", err);
                frappe.msgprint("Something went wrong during download.");
            }
        });
    }

    function downloadAllClosureExcel() {

        // frappe.call({
        //     method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_all_closures_excel",

        //      callback: function (r) {
        //         if (r.message && r.message.data) {
        //             const link = document.createElement("a");
        //             link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${r.message.data}`;
        //             link.download = r.message.filename || "all_closure.xlsx";
        //             document.body.appendChild(link);
        //             link.click();
        //             document.body.removeChild(link);
        //         } else {
        //             frappe.msgprint("No data received for download.");
        //         }
        //     },
        //     error: function (err) {
        //         console.error("Download error:", err);
        //         frappe.msgprint("Something went wrong during download.");
        //     }




        //     })

        window.open(
            window.location.href = repl(
                "/api/method/jobpro.jobpro.page.rec_dashboard.rec_dashboard.download_all_closures_excel"
            )
        );

    }

    let updatedClosure = {}


    window.makeEditable = function (element, closureID, field) {

        if (element.querySelector('.editable-input')) {
            return;
        }

        let span = element.querySelector('.editable-span');
        if (!span) return;

        let value = span.innerText.trim();

        element.innerHTML = '';


        if (field === 'custom_next_follow_up_on') {
            let input = document.createElement('input');
            input.classList.add('editable-input');
            input.type = 'date';
            input.value = toISODate(value);
            input.style.width = '100%';
            input.style.padding = '5px';
            input.style.fontSize = '16px';
            input.style.border = '1px solid #0F1568';
            input.style.borderRadius = '4px';
            input.style.boxSizing = 'border-box';



            input.onblur = function () {
                let newValue = input.value.trim();
                span.innerText = formatDate(newValue);
                element.innerHTML = '';
                element.appendChild(span);

                // Save to the update list
                if (closureID) {
                    if (!updatedClosure[closureID]) {
                        updatedClosure[closureID] = {};
                    }
                    updatedClosure[closureID][field] = newValue;
                }
            };

            element.appendChild(input);
            input.focus();
        }

        else if (field === 'standard_remarks') {

            let select = document.createElement('select');
            select.classList.add('editable-input');
            select.style.width = '100%';
            select.style.height = '30px';


            let loadingOption = document.createElement('option');
            loadingOption.text = "Loading...";
            loadingOption.value = "";
            select.appendChild(loadingOption);

            element.appendChild(select);
            select.focus();


            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Standard Remarks",
                    fields: ["standard_remarks"],
                    limit_page_length: 1000
                },
                callback: function (r) {

                    select.innerHTML = "";

                    if (r.message && r.message.length) {


                        let emptyOption = document.createElement('option');
                        emptyOption.value = "";
                        emptyOption.text = "-";
                        select.appendChild(emptyOption);

                        r.message.forEach(row => {
                            let option = document.createElement('option');
                            option.value = row.standard_remarks;
                            option.text = row.standard_remarks;

                            if (row.standard_remarks === value) {
                                option.selected = true;
                            }

                            select.appendChild(option);
                        });

                    } else {
                        let noData = document.createElement('option');
                        noData.text = "No Records Found";
                        select.appendChild(noData);
                    }
                }
            });



            $(select).select2({
                placeholder: "Select Standard Remark",
                width: '100%',
                dropdownAutoWidth: true
            });

            $(select).on('select2:close', function () {
                let newValue = select.value.trim();

                span.innerText = newValue || "-";

                $(select).select2('destroy');
                element.innerHTML = '';
                element.appendChild(span);

                if (closureID) {
                    if (!updatedClosure[closureID]) {
                        updatedClosure[closureID] = {};
                    }
                    updatedClosure[closureID][field] = newValue;
                }
            });



        }
        else {
            // Default behavior for remarks or task priority: use textarea
            let textarea = document.createElement('textarea');
            textarea.value = value;
            textarea.classList.add('editable-input');
            textarea.style.width = '200px';
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

                if (closureID) {
                    if (!updatedClosure[closureID]) {
                        updatedClosure[closureID] = {};
                    }
                    updatedClosure[closureID][field] = newValue;
                }
            };

            element.appendChild(textarea);
            textarea.focus();
            textarea.select();
        }
    }

    window.submitUpdatedClosures = function () {
        if (Object.keys(updatedClosure).length === 0) {
            frappe.msgprint("No updates to submit.");
            return;
        }
        frappe.call({
            method: "jobpro.jobpro.page.rec_dashboard.rec_dashboard.update_closure_remark",
            args: {
                closures: updatedClosure
            },
            callback: function (response) {
                if (response.message) {
                    frappe.msgprint("Closures Updated Successfully");
                    updatedClosure = {};
                }
            }
        });
    }

    function toISODate(dateStr) {
        if (!dateStr || dateStr === '-') return '';

        const parts = dateStr.split('-');
        if (parts.length !== 3) return '';

        return `${parts[2]}-${parts[1]}-${parts[0]}`;
    }








}














