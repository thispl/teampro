frappe.pages['daily-status---it'].on_page_load = function(wrapper) {
    frappe.require([
        "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.25/jspdf.plugin.autotable.min.js"

    ]);

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
    .table thead th { background-color: #0d6efd; color: white; }
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





  `;
  
  document.head.appendChild(style);

  $(wrapper).html(`
    <div class="dashboard-wrapper" style="padding: 0 30px;">
      <div style="position: relative; padding: 10px;">
        <h2 style="text-align: center; font-weight: bold; margin: 0;">IT SERVICES</h2>
		
        <div id="current-datetime" style="font-size: 16px; color: #666; text-align: center; margin-top: 5px;"></div>
		
        <div class="top-actions">
          <input type="date" id="tfp-from-date" class="form-control" style="width: 140px;">
          <input type="date" id="tfp-to-date" class="form-control" style="width: 140px;">
          <button id="apply-tfp-filter" class="btn btn-dark">Apply</button>
          <button id="refresh-dashboard" class="btn btn-dark">Refresh</button>
        </div>
		
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

    <div class="card-container equal-height" style="margin-top:40px; margin-right:0px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
        <div style="margin: 0; padding: 0px 0; text-align: center; background: white; position: relative;">
            <h4 style="margin: 0;">PRODUCTION SUMMARY</h4>
                
            </div>
            
        <br>
    

        <div id="today-task-table-container1" class="table-scrollable">Loading...</div>
        </div>

        <br>

    <div class="card-container equal-height" style="margin-top:40px; margin-right:0px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 10px;">
  <div style="margin: 0; padding: 0px 0; text-align: center; background: white; position: relative;">
  <h4 style="margin: 0;">PRODUCTION TABLE</h4>
     <div style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); display: flex; gap: 10px; background: #f5f5f5; padding: 5px; border-radius: 4px;">
    <button id="download-task-table-all"
            style="border: none; color: black; cursor: pointer;">
      ALL
    </button>
    <button id="download-task-table"
            style="border: none; color: black; cursor: pointer;">
      Download
    </button>
    <button id="download-task-table-pdf" style="border: none; color: black; cursor: pointer;">Download PDF</button>
  </div>
  </div>
  
  <br>
    

        <div id="today-task-table-container" class="table-scrollable">Loading...</div>
        </div>
	  <div id ="filters" style="margin-top: -20px;"></div><br>
      <div id="retro-summary-html" style="overflow-x:auto;overflow-y:auto; margin-top: -30px; margin-left: -30px; margin-right: -30px;"></div>
    </div>
  `);




loadDashboardData();
get_today_task_data1();
get_today_task_data11();

setInterval(function () {
    get_today_task_data1();
}, 300000);

setInterval(function () {
    get_today_task_data11();
}, 300000);

$(document).ready(function () {
    const today = frappe.datetime.get_today();

    $('#tfp-from-date').val(today);
    $('#tfp-to-date').val(today);

    get_today_task_data11(today, today);
    get_today_task_data1(today, today);
});


// load_retro_summary_html(sprint=null);
load_retro_summary(sprint=null);
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


$(document).on('click', '#download-task-table-all', function () {
    const table = document.getElementById('task-report-table');
    if (!table) {
        frappe.msgprint("No Data found.");
        return;
    }

    const hiddenRows = $(table).find('tr:hidden');
    hiddenRows.show();  

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
    method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.update_sprint_filter",
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

        let dev_team= name
        let selected_sprint = sprint_filter.get_value();
        if (dev_team ==='ALL'){
            dev_team =''
        }
        if (dev_team === 'Summary'){
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
                method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_retro_summary_html",
                args:{
                    name:selected_sprint,
                    dev_team:dev_team,
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

	// Buttons
	// $(wrapper).on('click', '#refresh-dashboard', () => location.reload());
    $(wrapper).on('click', '#refresh-dashboard', function () {

        const today = frappe.datetime.get_today();
        $('#tfp-from-date').val(today);
        $('#tfp-to-date').val(today);
        get_today_task_data11(today, today);
        get_today_task_data1(today, today);
    });

	$(wrapper).on('click', '#apply-tfp-filter', function () {
		const from_date = $('#tfp-from-date').val();
		const to_date = $('#tfp-to-date').val();
		loadOrderBooking(from_date, to_date);
		loadturnover(from_date, to_date);
		loadtcollection(from_date, to_date);
        get_today_task_data11(from_date, to_date);
        get_today_task_data1(from_date, to_date);
	});

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
		callback: function(r) {
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
		    const avg_value=Math.round(avg || 0);
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
			callback: function(r) {
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
                const avg_value=Math.round(avg || 0);

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
		callback: function(r) {
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
		    const avg_value1=Math.round(avg || 0);
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
		callback: function(r) {
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
		    const avg_value1=Math.round(avg || 0);
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
		callback: function(r) {
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
		    const avg_value2=Math.round(avg || 0);
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
		callback: function(r) {
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
		    const avg_value2=Math.round(avg || 0);
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
		callback: function(r) {
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
		    const avg_value3=Math.round(avg || 0);
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
		callback: function(r) {
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
		    const avg_value4=Math.round(avg || 0);
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
		callback: function(r) {
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
		    const avg_value5=Math.round(avg || 0);
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
		callback: function(r) {
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
		    const avg_value6=Math.round(avg || 0);
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
		method: 'teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.it_receivable_table',
		callback: function(r) {
			$('#receivable-so-table-content').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
		}
	});
	frappe.call({
		method: 'teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.it_payable_table',
		callback: function(r) {
			$('#payable-so-table-content').html(r.message || `<div style="padding: 10px;text-align:center">No data found</div>`);
		}
	});
	frappe.call({
		method: 'teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.it_tobill_table',
		callback: function(r) {
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
		frappe.call({ method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_project_counts" }),
		frappe.call({ method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_task_summary" }),
		frappe.call({ method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_sprint_counts" })
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
                    <div class="project-card" style="border-color:${projectColors[i % projectColors.length]};">
                        ${it.project_type}
                        <span>${it.count}</span>
                    </div>`;
            });

            html += `
                    </div>
                </div>`;

		container.find('#project-summary-wrapper').html(html);
	}

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
            <span>${(tc[`${key}_total_hours`] || 0).toFixed(2)} hr/<br>${tc[key] || 0}</span>
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
                method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_tasks_project_wise",
                args: { type: key },
                callback: (r) => {
                    const rows = r.message || [];
                    let tbl = `<div style="max-height:400px;overflow-y:auto;">
                        <table style="width:100%; border-collapse: collapse; border: 1px solid black;">
                            <thead><tr style="background-color: #0F1568; color: white;">
                                <th style="border: 1px solid black;">Project</th>
                                <th style="border: 1px solid black;">Tasks</th>
                                <th style="border: 1px solid black;">Hours</th>
                            </tr></thead><tbody>`;
                    rows.forEach(p => {
                        tbl += `<tr>
                            <td style="border: 1px solid black;">${p.project || 'No Project'}</td>
                            <td style="border: 1px solid black;">${p.task_count}</td>
                            <td style="border: 1px solid black;">${(p.total_hours || 0).toFixed(2)}</td>
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

		//  3. Sprint Summary
// 		if (sprintRes.message && sprintRes.message.sprints) {
//     const sprints = sprintRes.message.sprints;
//     const palette = ["#0096A6", "#2F8F46", "#C29100", "#540D6E", "#006D77", "#4169e1", "#003f5c"];
//     let colorMap = {}, idx = 0;
    
//     let html = `
//     <style>
//         .task-cards-container {
//             border: 1px solid #ccc;
//             border-radius: 5px;
//             margin-top: 20px;
//         }

//         .task-cards-container table {
//             width: 100%;
//             border-collapse: collapse;
//         }

//         .task-cards-container th {
//             background-color: white;
//             text-align: center;
//             font-weight: bold;
//             font-size: 16px;
//             padding: 10px;
//             border-bottom: 20px solid #ccc;
//         }

//         .task-cards-row {
//             display: flex;
//             overflow-x: auto;
//             padding: 10px;
//             gap: 10px;
//         }

//         .task-card {
//             min-width: 120px;
//             text-align: center;
//             font-weight: bold;
//             font-size: 14px;
//             border: 4px solid;
//             border-radius: 10px;
//             padding: 10px;
//             background: #fff;
//             cursor: pointer;
//         }

//         .task-card span {
//             font-size: 18px;
//             display: block;
//             margin-top: 5px;
//         }
//     </style>

//     // <div class="task-cards-container">
//     //     <table>
//     //     <br>
//     //         <h4 class="sticky-top" style="margin: 0; padding: 0px 0; text-align:center; background: white;">SPRINT CARDS </h4>
//     //     <br>
//     //     </table>
//     //     <div class="task-cards-row">`;

//     // sprints.forEach(item => {
//     //     if (!colorMap[item.team]) {
//     //         colorMap[item.team] = palette[idx++ % palette.length];
//     //     }

//     //     html += `
//     //     <div class="dashboard-card sprint-card" style="
//     //         background-color:${colorMap[item.team]};
//     //         flex: 0 0 calc(25% - 10px);
//     //         box-sizing: border-box;
//     //     ">
//     //         <div class="card-inner">
//     //             <h3 style="margin-bottom: 5px;">${item.team}</h3>
//     //             <div class="sprint-link" style="font-size:13px; cursor:pointer;" 
//     //                 data-sprint="${item.active}" data-team="${item.team}" data-type="active">
//     //                 Active: <b>${item.active || '-'}</b>
//     //             </div>
//     //             <div class="sprint-link" style="font-size:13px; cursor:pointer;" 
//     //                 data-sprint="${item.in_progress}" data-team="${item.team}" data-type="in_progress">
//     //                 Pending: <b>${item.in_progress || '-'}</b>
//     //             </div>
//     //         </div>
//     //     </div>`;
//     // });

//     html += `</div>`;
//     container.find('#sprint-summary-wrapper').html(html);

// 	// Delegate the click handler AFTER the HTML is added
// 	container.find('.sprint-link').on('click', function () {
// 		const sprint = $(this).data('sprint');
// 		const team = $(this).data('team');
// 		const type = $(this).data('type');

// 		if (sprint) {
// 			frappe.db.get_value('Sprint', { sprint_id: sprint, team }, ['name']).then(r => {
// 				if (r.message && r.message.name) {
// 					frappe.set_route('Form', 'Sprint', r.message.name);
// 				}
// 			});
// 		}
// 	});
// }

	});


}
function renderCardFromMethod(selector, label, method, from_date = null, to_date = null) {
	frappe.call({
		method: method,
		args: from_date && to_date ? { from_date, to_date } : {},
		callback: function(r) {
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
	


function get_today_task_data11(from_date=null, to_date=null) {
    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_today_task_data11",
        args: {
            from_date: from_date,
            to_date: to_date
        },
        callback: function (r) {
            let $container = $("#today-task-table-container1");

            if (r.message && r.message.data) {
                console.log(r.message)
                const data = r.message.data;
                const team_order = r.message.team_order;
                
                

                const active_data = data.filter(row => row[3]);

                let total_aph = 0;
                let total_rt = 0;
                let total_ut = 0;
                const seenCB = new Set();

                active_data.forEach(row => {

                    const cb = row[3];

                    if(!seenCB.has(cb)){
                        total_aph += row[24] || 0;
                        total_rt += row[14] || 0;
                        total_ut += row[13] || 0;

                        seenCB.add(cb);
                    }

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
    font-size: 14px;
}
.left-align {
    text-align: left !important;
}

.toggle-team {
    cursor: pointer;
    font-weight: bold;
    background-color: #eaf0f6;;
}
.toggle-cb {
    cursor: pointer;
    font-weight: bold;
    background-color: #f2f2f2;
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


.cb-circle1 img{
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
    width:35px;
    height:35px;
    border-radius:8px;
    border:2px solid #d9e3f0;
    padding:3px;
    background:white;
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

.cb-odd {
    background-color: #ffffff;
    color: #000000;
}

.cb-even {
    background-color: #e6f0ff;
    color: #000000;
}




</style>



<table id="task-report-table">
<thead>
<tr>
    <th style="width:7%">Team</th>
    <th colspan="10" style="width:50%">Employee</th>
    <th style="width:15%">APH</th>
    <th style="width:15%">Today RT</th>  
    <th style="width:15%">UT</th>
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

                    // Team header with totals
                   let cb_buttons = `<td colspan="10" class="left-align">`;

                    cb_buttons += `<span class="team-all-btn-11" data-team="${team_id}" data-type="all" style="cursor:pointer; font-weight:bold; margin-right:10px;">+ ALL</span>`;


					sorted_cbs.forEach(([cb, cb_data]) => {

					const cb_id = `cb-${team.replace(/\s+/g, '_')}-${cb.replace(/\s+/g, '_')}`;
					const cb_profile = cb_data.tasks[0][18] || "/assets/frappe/images/ui/avatar.png";

					cb_buttons += `
						<span class="cb-btn-11" data-target="${cb_id}"
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

                    let team_aph = 0;
                    let team_today_rt = 0;
                    let team_ut = 0;

                    Object.values(cb_groups).forEach(cb_data => {

                        const task = cb_data.tasks[0];   // CB ku first row

                        team_aph += task[24] || 0;
                        team_today_rt += task[14] || 0;
                        team_ut += task[13] || 0;

                    });

					html += `<tr class="team-row" style="background-color:#fff9fa">
                        <td colspan="1" class="center-align">
                            <div class="team-logo">
                                <img src="${team_logo}">
                            </div>
                        </td>
                        <td colspan="10" class="left-align">
                            <div style="display:flex; align-items:center; justify-content:center;">
                                <b>${team}</b>
                            </div>
                        </td>
                        <td><b>${team_aph.toFixed(2)}</b></td>
                        <td><b>${team_today_rt.toFixed(2)}</b></td>
                        <td><b>${team_ut.toFixed(2)}</b></td>
                    </tr>`;
                    let cb_index = 0;

            
                    for (const [cb, cb_data] of sorted_cbs) {
                        cb_index++;
                        const row_class = (cb_index % 2 === 1) ? "cb-odd" : "cb-even";
                        const tasks = cb_data.tasks;
                        const first_row = tasks[0] || [];
                        html += `<tr class="cb-row ${row_class}">
                            <td>${cb_index}</td>
                            <td colspan="10" class="left-align">
                                <div class="cb-circle1" style="display:flex; align-items:center;gap: 15px;padding-left:10px;">
                                    <img src="${tasks[0][18]}" style="width:30px; height:30px; margin-right:10px;">
                                    <span>${first_row[26] || ''}</span>
                                </div>
                            </td>
                            <td><b>${tasks[0][24]}</b></td>
                            <td><b>${tasks[0][14]}</b></td>
                            <td><b>${tasks[0][13]}</b></td>
                        </tr>`;
                    }
    }    

    html += `
            <tr style="background:#e0e0e0; font-weight:bold; text-align:center;">

                <td>
                    <img src="/assets/frappe/images/all_teams.png"
                    style="width:45px;height:45px;">
                </td>

                <td colspan="10" style="padding:12px 8px; text-align:center;">
                    <div style="display:flex; justify-content:center; align-items:center;">
                        <span id="open-all-teams1"
                            style="cursor:pointer; font-weight:bold;font-size:18px;">
                            Total 
                        </span>
                    </div>
                </td>

                <td><b>${total_aph.toFixed(2)}</b></td>
                <td><b>${total_rt.toFixed(2)}</b></td>
                <td><b>${total_ut.toFixed(2)}</b></td>

            </tr>
            `;

                html += `</tbody></table>`;
                $container.html(html);

                




if($(this).hasClass("active")){
    $(".task-row").show();
    $(".filter-btn").removeClass("active");
    return;
}


                
            } else {
                $container.html("<p>No data found.</p>");
            }
        }
    });

}


function get_today_task_data1(from_date=null, to_date=null) {
    let priority = $("#filter-priority").val();
    let sp = $("#filter-sp").val();
    let ro = $("#filter-ro").val();
    frappe.call({
        method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_today_task_data1",
        args: {
            priority: priority,
            sp: sp,
            ro: ro,
            from_date : from_date,
            to_date : to_date
        },
        callback: function (r) {
            let $container = $("#today-task-table-container");

            if (r.message && r.message.data) {
                
                // const data = r.message;
                const data = r.message.data;
                const team_order = r.message.team_order;
                const active_data = data.filter(row => row[3]);
                
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
    font-size: 14px;
}
.left-align {
    text-align: left !important;
}

.toggle-team {
    cursor: pointer;
    font-weight: bold;
    background-color: #eaf0f6;;
}
.toggle-cb {
    cursor: pointer;
    font-weight: bold;
    background-color: #f2f2f2;
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

/* ✅ Thin bar */
.progress-wrapper{
    width:100%;
    height:6px;             
    background:#eee;
    border-radius:10px;
    overflow:hidden;
    position:relative;
}

/* ✅ Actual progress */
.progress-bar{
    height:100%;
    border-radius:10px;
    transition:width 0.3s ease;
}

/* ✅ Bottom text */
.progress-bottom-text{
    margin-top:6px;
    font-size:12px;
    text-align:center;
}

/* ✅ Hover text (top) */
.progress-hover-text{
    position:absolute;
    top:-18px;              
    font-size:11px;
    opacity:0;
    transition:0.2s;
    white-space:nowrap;
}

/* ✅ Show on hover */
.progress-container:hover .progress-hover-text{
    opacity:1;
}

</style>



<table id="task-report-table">
<thead>
<tr>
    <th style="width:4%">Sl No</th>
    <th style="width:5%">Sprint</th>
    <th style="width:16%">Project</th>   <!-- smaller -->
    <th style="width:6%">Task</th>
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

            html += `
            <tr style="background:#dfe7f5; font-weight:bold;">
<td colspan="8" style="padding:12px 8px;">

    <div style="display:flex; align-items:center; gap:10px;">

        <!-- + ALL -->
        <span id="open-all-teams-btn"
            style="cursor:pointer; font-weight:bold; margin-right:10px;">
            + ALL
        </span>

        <!-- 🔲 FILTER CONTAINER (gray box) -->
        <div style="
            display:flex;
            align-items:center;
            gap:15px;
            background:#f1f3f6;
            padding:6px 10px;
            border-radius:8px;
        ">

            <!-- Priority -->
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="color:green; font-weight:bold;">Priority :</span>
                <span class="filter-btn" data-group="priority" data-filter="Low">Low</span>
                <span class="filter-btn" data-group="priority" data-filter="Medium">Medium</span>
                <span class="filter-btn" data-group="priority" data-filter="High">High</span>
                <span class="filter-btn" data-group="priority" data-filter="Critical">Urgent</span>
            </div>

            <!-- SP -->
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="color:green; font-weight:bold;">S/P :</span>
                <span class="filter-btn" data-group="sp" data-filter="S">Spot</span>
                <span class="filter-btn" data-group="sp" data-filter="P">Plan</span>
            </div>

            <!-- RO -->
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="color:green; font-weight:bold;">RO :</span>
                <span class="filter-btn" data-group="ro" data-filter="RO">Reopen</span>
            </div>

            <!-- CF -->
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="color:green; font-weight:bold;">CF :</span>
                <span class="filter-btn" data-group="cf" data-filter="CF">Carry Forward</span>
            </div>

        </div>

    </div>

</td>

            <td>${total_et.toFixed(2)}</td>


            <td>${total_at.toFixed(2)}</td>

            <td>${total_today_rt.toFixed(2)}</td>


            <td colspan="3"></td>

            </tr>
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
                    let team_et = 0, team_rt = 0, team_at = 0, team_at_period = 0, team_task_count = 0, team_today_rt=0;

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

                    cb_buttons += `<span data-team="${team_id}" data-type="all" style="cursor:pointer; font-weight:bold; text-align:center; margin-right:10px;">+ ALL</span>`;


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

    let cb_et = 0, cb_rt = 0, cb_at = 0, cb_today_at = 0, cb_today_rt=0
    tasks.forEach(row => {
        cb_et += parseFloat(row[5]) || 0;
        // cb_rt += parseFloat(row[6]) || 0;
        cb_at += parseFloat(row[7]) || 0;
        cb_today_rt+= parseFloat(row[14]) || 0;
        // cb_today_at += parseFloat(row[13]) || 0;
    });

    const first_row = tasks[0] || [];
    html += `<tr class="toggle-cb ${cb_id} ${team_id}" style="display:none;">
        <td><span class="toggle-icon">+</span></td>
        <td colspan="7" class="left-align" style="color:#000;">
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
            
            let bg = (global_index % 2 === 0) ? "#ffffff" : "#eaf0f6";
            let text = "#000000";
                html += `
                    <tr class="task-row ${cb_id} ${team_id}"
                        data-priority="${row[8]}"
                        data-sp="${row[21] == 1 ? 'S' : 'P'}"
                        data-ro="${row[22] > 0 ? 'RO' : ''}"
                        data-cf="${row[23] > 0 ? 'CF' : ''}"
                        style="display:none; background:${bg}; color:${text};">                   
                    <td>${task_serial++}</td>
                    <td>${row[15]}</td>
                    <td class="left-align"><a href="/app/project/${row[1]}" target="_blank">${row[1]}</a></td>
                    <td><a href="/app/task/${row[0]}" target="_blank">${row[0]}</a></td>
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
                    <td class="left-align">${row[8]}</td>
                    <td class="status-cell" style="width:6%; text-align:center;">

                        <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

                        ${row[20] == 0 ? `

                            <!-- Tick -->
                            <span class="confirm-task-btn status-icon tick-icon"
                                data-task="${row[0]}"
                            
                                ">
                                ✓
                            </span>

                        ` : `

                            <!-- C (click to unconfirm) -->
                            <span class="task-unconfirm-btn status-icon c-icon"
                                data-task="${row[0]}"
                            
                                ">
                                C
                            </span>

                        `}

                            <!-- 👁 always -->
                            <span class="task-info-btn"
                                data-task="${row[0]}"
                                style="cursor:pointer; font-size:20px; color:black">
                                👁
                            </span>

                        </div>

                    </td>


                    <td class="progress-cell" style="width:16%; text-align:center;">

                    ${row[20] == 1 ? (() => {

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

                                if (status === "Working") status_display = "";
                                else if (status === "Pending Review") status_display = "PR";
                                else if (status === "Client Review") status_display = "CR";
                                else if (status === "Completed") status_display = " ✔";

                                let hover_color = "#d81b60"; // dark pink default

                                if (color === "red") {
                                    hover_color = "black";
                                }

                                if (color === "orange") {
                                    hover_color = "black";
                                }


                                return `
<div class="progress-container">

    <!-- Hover text (top) -->
    <div class="progress-hover-text">
        ${row[13]}
    </div>

    <!-- Progress bar -->
    <div class="progress-wrapper">
        <div class="progress-bar" 
            style="width:${Math.min(progress,100)}%; background:${color};">
        </div>
    </div>

    <!-- Bottom text -->
    <div class="progress-bottom-text"
        style="color:${text_color};">
        ${status_display} ${progress}%
    </div>

</div>
`;

                    })() : ``}

                    </td>

                        </div>

                        </td>
                </tr>`;
                    global_index++;
                    });
                    
    
        }
    }    


    

                html += `</tbody></table>`;
                $container.html(html);

                $(document).off("click", "#open-all-teams-btn").on("click", "#open-all-teams-btn", function(){

                    let rows = $container.find(".toggle-cb, .task-row");

                    if(rows.is(":visible")){
                        rows.hide();
                        $(this).text("+ ALL");
                    }else{
                        rows.show();
                        $(this).text("- ALL");
                    }

                });

                // Apply Filter


$(document).off("click",".filter-btn").on("click",".filter-btn",function(){

    let group = $(this).data("group");

    // toggle logic
    if($(this).hasClass("active")){
        $(this).removeClass("active");
    }else{

        // only one active inside same group
        $(`.filter-btn[data-group="${group}"]`).removeClass("active");

        $(this).addClass("active");
    }

    apply_filters();

});


function apply_filters(){

    let priority = $('.filter-btn[data-group="priority"].active').data("filter");
    priority = priority ? priority.toString().toLowerCase() : null;
    let sp = $('.filter-btn[data-group="sp"].active').data("filter");
    let ro = $('.filter-btn[data-group="ro"].active').data("filter");
    let cf = $('.filter-btn[data-group="cf"].active').data("filter");

    $container.find(".task-row").hide();
    $container.find(".toggle-cb").hide();

    $(".toggle-cb").each(function(){

        let cb_row = $(this);
        let cb_class = cb_row.attr("class").split(" ")[1];

        let tasks = $container.find("." + cb_class + ".task-row");

        let matched = tasks.filter(function(){

            let p = ($(this).data("priority") || "").toString().toLowerCase();
            let s = $(this).data("sp");
            let r = $(this).data("ro");
            let c = $(this).data("cf");

            if(priority && p !== priority) return false;
            if(sp && s !== sp) return false;
            if(ro && r !== "RO") return false;
            if(cf && c !== "CF") return false;

            return true;

        });

        if(matched.length){

            cb_row.show();

            let serial = 1;

            matched.each(function(){

                $(this).show();
                $(this).find("td:first").text(serial++);

            });

        }

    });

}

if($(this).hasClass("active")){
    $(".task-row").show();
    $(".filter-btn").removeClass("active");
    return;
}

                // Toggle logic for CB → Task rows
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
        method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.check_running_timesheet",
        args: { task: task },
        callback: function(r){

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

                        <span class="task-info-btn"
                            data-task="${task}"
                            style="cursor:pointer; font-size:20px; color:black;">
                            👁
                        </span>

                    </div>
                `);

                // ✅ clear progress
                progress_cell.html("");

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
                    else if (status === "Completed") status_display = "✔";

                    let hover_color = "#d81b60";

                    if (color === "red" || color === "orange") {
                        hover_color = "black";
                    }

                // ✅ 1st cell update
                status_cell.html(`
                    <div style="display:flex; align-items:center; gap:8px; justify-content:center;">

                        <span class="task-unconfirm-btn status-icon c-icon"
                            data-task="${task}"
                            
                            ">
                            C
                        </span>

                        <span class="task-info-btn"
                            data-task="${task}"
                            style="cursor:pointer; font-size:20px; color:black">
                            👁
                        </span>

                    </div>
                `);

                // ✅ 2nd cell update
                progress_cell.html(`
                    <div class="progress-container">

    <!-- Hover text (top) -->
    <div class="progress-hover-text">
        ${completed}
    </div>

    <!-- Progress bar -->
    <div class="progress-wrapper">
        <div class="progress-bar" 
            style="width:${Math.min(progress,100)}%; background:${color};">
        </div>
    </div>

    <!-- Bottom text -->
    <div class="progress-bottom-text"
        style="color:${text_color};">
        ${status_display} ${progress}%
    </div>

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
        callback: function(r) {

            const t = r.message;


            let html = `
<div>
    <table style="width:100%; border-collapse:collapse;">

        <tr>
            <td><b style="color:red;">Task :</b></td>
            <td colspan="1"><span style="color:blue;">${t.name}</span></td>
            <td><b style="color:red;">Project :</b></td>
            <td colspan="3"><span style="color:blue;">${t.project || ""}</span></td>
        </tr>

        <tr>
            <td><b style="color:red;">Subject :</b></td>
            <td colspan="5"><span style="color:blue;">${t.subject || ""}</span></td>
        </tr>

        <tr>
            <td><b style="color:red;">Description :</b></td>
            <td colspan="5"><span style="color:blue;">${t.description || ""}</span></td>
        </tr>

        <tr>
            <td colspan="1"><b style="color:red;">ET :</b></td>
            <td colspan="1"><span style="color:blue;">${t.expected_time || ""}</span></td>
            <td colspan="1"><b style="color:red;">RT :</b></td>
            <td colspan="1"><span style="color:blue;">${t.rt || ""}</span></td>
            <td colspan="1"><b style="color:red;">AT :</b></td>
            <td colspan="1"><span style="color:blue;">${t.actual_time || ""}</span></td>
        </tr>

        <tr>
            <td><b style="color:red;">CF :</b></td>
            <td colspan="2"><span style="color:blue;">${t.custom_production_date_count}</span></td>
            <td><b style="color:red;">RO :</b></td>
            <td colspan="2"><span style="color:blue;">${t.revisions || ""}</span></td>
        </tr>

        <tr>
            <td><b style="color:red;">Created On :</b></td>
            <td><span style="color:blue;">
                ${t.creation ? frappe.datetime.str_to_user(t.creation) : ""}
            </span></td>

            <td><b style="color:red;">Allocated On :</b></td>
            <td><span style="color:blue;">
                ${t.custom_allocated_on ? frappe.datetime.str_to_user(t.custom_allocated_on) : ""}
            </span></td>

            <td><b style="color:red;">Age :</b></td>
            <td><span style="color:blue;">
                ${t.custom_age}
            </span></td>
        </tr>

        <tr>
            <td><b style="color:red;">Developer Note :</b></td>
            <td colspan="5"><span style="color:blue;">${t.custom_developer_note || ""}</span></td>
        </tr>

        <tr>
            <td><b style="color:red;">Remarks :</b></td>
            <td colspan="5"><span style="color:blue;">${t.custom_taskissue_action_taken || ""}</span></td>
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
        }
    });

});



$container.find('span[data-type="all"]').on('click', function () {
    const teamId = $(this).data('team');
    const teamRows = $container.find(`.${teamId}`); // includes both CB + task rows
    const isVisible = teamRows.is(':visible');

    if (isVisible) {
        teamRows.hide();
        $(this).text('+ ALL');
        // Also reset CB buttons text
        $(`span[data-target^="cb-${teamId}"]`).each(function() {
            $(this).text('+ ' + $(this).text().slice(2));
        });
    } else {
        teamRows.show();
        $(this).text('- ALL');
        // Also update CB buttons text
        $(`span[data-target^="cb-${teamId}"]`).each(function() {
            $(this).text('- ' + $(this).text().slice(2));
        });
    }
});

                
            } else {
                $container.html("<p>No data found.</p>");
            }
        }
    });

}


function load_retro_summary_html(sprint) {
    frappe.call({
    method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_retro_summary_html_test",
	args:{
	    name:sprint 
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
                method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.summary_total",
                args:{
                    name:sprint
                },
                callback: function(r) {
                    if (r.message) {
                        $('#retro-summary-html').html(r.message);
                    } else {
                        $('#retro-summary-html').html("No Data Found");
                    }
                }
            });
}


frappe.call({
    method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_tasks_project_pivot",
    callback: function (r) {
        const data = r.message || [];

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
        background-color: #ffffff;   /* white */
        color: #000000;              /* black text */
    }

    #pivot-summary tbody tr:nth-child(even) {
        background-color: #eaf0f6;   /* light mild blue */
        color: #000000;              /* black text */
    }
    .left-align {
        text-align: left;
    }
</style>

<div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; box-sizing: border-box;">
<br>
    <h4 style="margin: 0; padding: px 0; text-align: center; background: white;">PROJECT STATUS REPORT(PSR)</h4>
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

        let total_open_hours = 0, total_open_tasks = 0;
        let total_working_hours = 0, total_working_tasks = 0;
        let total_pr_hours = 0, total_pr_tasks = 0;
        let total_cr_hours = 0, total_cr_tasks = 0;

        data.forEach(row => {
            const [open_hr, open_task] = row.open.split("/").map(Number);
            const [work_hr, work_task] = row.working.split("/").map(Number);
            const [pr_hr, pr_task] = row.pr.split("/").map(Number);
            const [cr_hr, cr_task] = row.cr.split("/").map(Number);

            pivot_html += `
            <tr>
                <td>${row.s_no}</td>
                <td class="left-align">${row.project}</td>
                <td class="left-align">${row.project_type}</td>
                <td>${open_hr.toFixed(2)}/<br>${open_task}</td>
                <td>${work_hr.toFixed(2)}/<br>${work_task}</td>
                <td>${pr_hr.toFixed(2)}/<br>${pr_task}</td>
                <td>${cr_hr.toFixed(2)}/<br>${cr_task}</td>
            </tr>`;

            total_open_hours += open_hr;
            total_open_tasks += open_task;
            total_working_hours += work_hr;
            total_working_tasks += work_task;
            total_pr_hours += pr_hr;
            total_pr_tasks += pr_task;
            total_cr_hours += cr_hr;
            total_cr_tasks += cr_task;
        });

        pivot_html += `
        <tr style="font-weight:bold; background-color: #0F1568; color: white;">
            <td colspan="3" style="text-align: center;">Total</td>
            <td>${total_open_hours.toFixed(2)}/<br>${total_open_tasks}</td>
            <td>${total_working_hours.toFixed(2)}/<br>${total_working_tasks}</td>
            <td>${total_pr_hours.toFixed(2)}/<br>${total_pr_tasks}</td>
            <td>${total_cr_hours.toFixed(2)}/<br>${total_cr_tasks}</td>
        </tr>`;

        pivot_html += `</tbody></table>`;

        $("#pivot-project-summary-container").html(pivot_html);
    }
});


// function createDevTeamButton() {
//             frappe.call({
//                 method: "teampro.teampro.page.it_sw_dashboard_1.it_sw_dashbord_1.get_retro_summary_overall",
//                 callback: function(r) {
//                     if (r.message) {
//                         $('#overall-summary-html').html(r.message);
//                     } else {
//                         $('#overall-summary-html').html("No Data Found");
//                     }
//                 }
//             });
//         }

}



