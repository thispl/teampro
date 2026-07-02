
// frappe.pages['approvals'].on_page_load = function(wrapper) {

// 	let page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'Approvals',
// 		single_column: true
// 	});
    

// 	$(page.body).html(`
//     <div class="approvals-container" style="background-color:white;">

//         <div style="text-align:center; margin-bottom:5px; margin-top:15px;">
//             <h2 style="margin:0; font-weight:bold;">APPROVALS</h2>
//             <div style="font-size:16px; color:#555; margin-top:4px;" id="current-datetime"></div>
//         </div>

//         <div style="background:#f2f2f2; padding:10px; border-radius:8px; margin:15px;">

//             <!-- Leave Application -->
//             <div style="border:1px solid #d1d5db; border-radius:8px; overflow:hidden; margin-bottom:10px;">
//                 <div style="background:#ffffff; height:40px; display:flex; align-items:center; padding:0 15px; border-bottom:1px solid #d1d5db;">
//                     <h4 style="margin:0; font-size:13px; font-weight:700; letter-spacing:1px;">LEAVE APPLICATION</h4>
//                 </div>
//                 <div style="background:#ffffff; padding:10px; overflow-x:auto;">
//                     <div id="leave-table"></div>
//                 </div>
//             </div>

//             <!-- Expense Claim -->
//             <div style="border:1px solid #d1d5db; border-radius:8px; overflow:hidden; margin-bottom:10px;">
//                 <div style="background:#ffffff; height:40px; display:flex; align-items:center; padding:0 15px; border-bottom:1px solid #d1d5db;">
//                     <h4 style="margin:0; font-size:13px; font-weight:700; letter-spacing:1px;">EXPENSE CLAIM</h4>
//                 </div>
//                 <div style="background:#ffffff; padding:10px; overflow-x:auto;">
//                     <div id="expense-table"></div>
//                 </div>
//             </div>

//             <!-- Attendance Request -->
//             <div style="border:1px solid #d1d5db; border-radius:8px; overflow:hidden; margin-bottom:10px;">
//                 <div style="background:#ffffff; height:40px; display:flex; align-items:center; padding:0 15px; border-bottom:1px solid #d1d5db;">
//                     <h4 style="margin:0; font-size:13px; font-weight:700; letter-spacing:1px;">ATTENDANCE REQUEST</h4>
//                 </div>
//                 <div style="background:#ffffff; padding:10px; overflow-x:auto;">
//                     <div id="att-table"></div>
//                 </div>
//             </div>

//             <!-- Purchase Order -->
//             <div style="border:1px solid #d1d5db; border-radius:8px; overflow:hidden; margin-bottom:10px;">
//                 <div style="background:#ffffff; height:40px; display:flex; align-items:center; padding:0 15px; border-bottom:1px solid #d1d5db;">
//                     <h4 style="margin:0; font-size:13px; font-weight:700; letter-spacing:1px;">PURCHASE ORDER</h4>
//                 </div>
//                 <div style="background:#ffffff; padding:10px; overflow-x:auto;">
//                     <div id="pur-table"></div>
//                 </div>
//             </div>

//             <!-- Purchase Invoice -->
//             <div style="border:1px solid #d1d5db; border-radius:8px; overflow:hidden; margin-bottom:10px;">
//                 <div style="background:#ffffff; height:40px; display:flex; align-items:center; padding:0 15px; border-bottom:1px solid #d1d5db;">
//                     <h4 style="margin:0; font-size:13px; font-weight:700; letter-spacing:1px;">PURCHASE INVOICE</h4>
//                 </div>
//                 <div style="background:#ffffff; padding:10px; overflow-x:auto;">
//                     <div id="pur-inv-table"></div>
//                 </div>
//             </div>

//             <!-- Sales Invoice -->
//             <div style="border:1px solid #d1d5db; border-radius:8px; overflow:hidden;">
//                 <div style="background:#ffffff; height:40px; display:flex; align-items:center; padding:0 15px; border-bottom:1px solid #d1d5db;">
//                     <h4 style="margin:0; font-size:13px; font-weight:700; letter-spacing:1px;">SALES INVOICE</h4>
//                 </div>
//                 <div style="background:#ffffff; padding:10px; overflow-x:auto;">
//                     <div id="sal-inv-table"></div>
//                 </div>
//             </div>

//         </div>
//     </div>
// `);

// // ✅ Time format — match R&S style
// function update_datetime() {
//     const now = new Date();
//     const date = now.toLocaleDateString('en-IN', {
//         year: 'numeric', month: 'long', day: 'numeric'
//     });
//     const time = now.toLocaleTimeString('en-IN', {
//         hour: '2-digit', minute: '2-digit', second: '2-digit',
//         hour12: true
//     }).toUpperCase();
//     $('#current-datetime').text(`${date} | ${time}`);
// }
// update_datetime();
// setInterval(update_datetime, 1000);

	
// 	$(`<style>

        

// 		.approvals-container{
// 			padding-left:20px;
// 			padding-right:20px;
// 		}
//         .page-head.flex{
//             display:none !important;
//         }

// 		/* Header */
// 		.approval-table thead th{
// 			background:#0F1568 !important;
// 			color:white !important;
// 			text-align:center;
// 			vertical-align:middle;
// 		}

// 		/* Odd Rows */
// 		.approval-table tbody tr:nth-child(odd){
// 			background:#ffffff;
// 		}

// 		/* Even Rows */
// 		.approval-table tbody tr:nth-child(even){
// 			background:#E7E6EC;
// 		}

// 		/* Hover */
// 		.approval-table tbody tr:hover{
// 			background:#F3C98B !important;
// 			cursor:pointer;
// 			transition:0.2s;
// 		}

// 		/* Cell Alignment */
// 		.approval-table td,
// 		.approval-table th{
// 			text-align:center;
// 			vertical-align:middle;
// 	}

//     .leave-section {
//     border: 1px solid #d1d5db;
//     border-radius: 8px;
//     overflow: hidden;
//     margin-bottom: 20px;
// }

// .leave-section-header {
//     background: #ffffff;
//     height: 40px;
    
//     display: flex;
//     justify-content: space-between;
//     align-items: center;
//     padding: 0 15px;
//     border-bottom: 1px solid #d1d5db;
// }

// .leave-section-body {
//     background: #f2f2f2;
//     padding: 10px;
//     overflow-x: auto;
// }
// 	</style>`).appendTo("head");

// 	load_leave_applications();
// 	load_expense_claims();
// 	load_att_table();
// 	load_pur_table();
//     load_pur_inv_table();
//     load_sal_inv_table();
// };

frappe.pages['approvals'].on_page_load = function(wrapper) {

	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Approvals',
		single_column: true
	});
    

	$(page.body).html(`
    <div class="approvals-container" style="background-color:white;">

        

        <div style="text-align:center; margin-bottom:5px; margin-top:15px;">
            <h2 style="margin:0; font-weight:bold;">APPROVALS</h2>
            <div style="font-size:16px; color:#555; margin-top:5px;" id="current-datetime"></div>

            <div style="margin-top:12px; display:flex; justify-content:center;gap:10px; flex-wrap:wrap;">
                <button class="nav-btn" data-target="leave-section">Leave Application</button>
                <button class="nav-btn" data-target="expense-section">Expense Claim</button>
                <button class="nav-btn" data-target="att-section">Attendance Request</button>
                <button class="nav-btn" data-target="pur-section">Purchase Order</button>
                <button class="nav-btn" data-target="pur-inv-section">Purchase Invoice</button>
                <button class="nav-btn" data-target="sal-inv-section">Sales Invoice</button>
            </div>
        </div>

        <br>
        <div id="approval-cards" style="display:flex;justify-content:center;align-items:center;gap:15px;flex-wrap:wrap;border:1px solid #d1d5db;background:#f2f2f2;border-radius:8px;margin-top:5px;margin-bottom:10px;padding-top:8px;padding-bottom:8px;">

            <div id="leave-card"></div>
            <div id="expense-card"></div>
            <div id="attendance-card"></div>
            <div id="po-card"></div>
            <div id="pi-card"></div>
            <div id="si-card"></div>

        </div>

        <br>
        <!-- Leave Application -->
        <div id="leave-section" style="border:1px solid #d1d5db;background:#f2f2f2; border-radius:8px; overflow:hidden;margin-top:5px; margin-bottom:10px;">
            <br>   
            <div style="border:1px solid #ffffff; background:#ffffff;height:40px;width:1240px;margin-left:10px; display:flex; justify-content:center; align-items:center; padding:0 6px; border-radius:2px;">
                <h2 style="margin:0;font-size:16px; font-weight:700;">LEAVE APPLICATION</h2>
            </div>
            <div style="background:#f2f2f2; padding:10px; overflow-x:auto;">
                <div id="leave-table"></div>
            </div>
        </div>

        <!-- Expense Claim -->
        <div id="expense-section" style="border:1px solid #d1d5db;background:#f2f2f2; border-radius:8px; overflow:hidden; margin-bottom:10px;">
            <br>   
            <div style="border:1px solid #ffffff; background:#ffffff;height:40px;width:1240px;margin-left:10px; display:flex; justify-content:center; align-items:center; padding:0 6px; border-radius:2px;">
                <h2 style="margin:0;font-size:16px; font-weight:700;">EXPENSE CLAIM</h2>
            </div>
            <div style="background:#f2f2f2; padding:10px; overflow-x:auto;">
                <div id="expense-table"></div>
            </div>
        </div> 

        <!-- Attendance Request -->
        <div id="att-section" style="border:1px solid #d1d5db;background:#f2f2f2; border-radius:8px; overflow:hidden; margin-bottom:10px;">
            <br>   
            <div style="border:1px solid #ffffff; background:#ffffff;height:40px;width:1240px;margin-left:10px; display:flex; justify-content:center; align-items:center; padding:0 6px; border-radius:2px;">
                <h2 style="margin:0;font-size:16px; font-weight:700;">ATTENDANCE REQUEST</h2>
            </div>
            <div style="background:#f2f2f2; padding:10px; overflow-x:auto;">
                <div id="att-table"></div>
            </div>
        </div> 


        <!-- Purchase Order -->
        <div id="pur-section" style="border:1px solid #d1d5db;background:#f2f2f2; border-radius:8px; overflow:hidden; margin-bottom:10px;">
            <br>   
            <div style="border:1px solid #ffffff; background:#ffffff;height:40px;width:1240px;margin-left:10px; display:flex; justify-content:center; align-items:center; padding:0 6px; border-radius:2px;">
                <h2 style="margin:0;font-size:16px; font-weight:700;">PURCHASE ORDER</h2>
            </div>
            <div style="background:#f2f2f2; padding:10px; overflow-x:auto;">
                <div id="pur-table"></div>
            </div>
        </div> 

        <!-- Purchase Invoice -->
        <div id="pur-inv-section" style="border:1px solid #d1d5db;background:#f2f2f2; border-radius:8px; overflow:hidden; margin-bottom:10px;">
            <br>   
            <div style="border:1px solid #ffffff; background:#ffffff;height:40px;width:1240px;margin-left:10px; display:flex; justify-content:center; align-items:center; padding:0 6px; border-radius:2px;">
                <h2 style="margin:0;font-size:16px; font-weight:700;">PURCHASE INVOICE</h2>
            </div>
            <div style="background:#f2f2f2; padding:10px; overflow-x:auto;">
                <div id="pur-inv-table"></div>
            </div>
        </div> 

        <!-- Sales Invoice -->
         <div id="sal-inv-section" style="border:1px solid #d1d5db;background:#f2f2f2; border-radius:8px; overflow:hidden; margin-bottom:10px;">
            <br>   
            <div style="border:1px solid #ffffff; background:#ffffff;height:40px;width:1240px;margin-left:10px; display:flex; justify-content:center; align-items:center; padding:0 6px; border-radius:2px;">
                <h2 style="margin:0;font-size:16px; font-weight:700;">SALES INVOICE</h2>
            </div>
            <div style="background:#f2f2f2; padding:10px; overflow-x:auto;">
                <div id="sal-inv-table"></div>
            </div>
        </div> 



    </div>
`);

// ✅ Time format — match R&S style
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
update_datetime();
setInterval(update_datetime, 1000);

$(document).on("click", ".nav-btn", function () {
    const target = $(this).data("target");

    document.getElementById(target).scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
});

	
	$(`<style>

        .nav-btn{
            background:#0F1568;
            color:white;
            border:none;
            padding:8px 14px;
            border-radius:5px;
            cursor:pointer;
            font-weight:600;
        }

        .nav-btn:hover{
            opacity:0.9;
        }

		.approvals-container{
			padding-left:20px;
			padding-right:20px;
		}
        .page-head.flex{
            display:none !important;
        }

		/* Header */
		.approval-table thead th{
			background:#0F1568 !important;
			color:white !important;
			text-align:center;
			vertical-align:middle;
		}

		/* Odd Rows */
		.approval-table tbody tr:nth-child(odd){
			background:#ffffff;
		}

		/* Even Rows */
		.approval-table tbody tr:nth-child(even){
			background:#E7E6EC;
		}

		/* Hover */
		.approval-table tbody tr:hover{
			background:#F3C98B !important;
			cursor:pointer;
			transition:0.2s;
		}

		/* Cell Alignment */
		.approval-table td,
		.approval-table th{
			text-align:center;
			vertical-align:middle;
	}

    .leave-section {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
}

.leave-section-header {
    background: #ffffff;
    height: 40px;
    
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 15px;
    border-bottom: 1px solid #d1d5db;
}

.leave-section-body {
    background: #f2f2f2;
    padding: 10px;
    overflow-x: auto;
}
	</style>`).appendTo("head");

	load_leave_applications();
	load_expense_claims();
	load_att_table();
	load_pur_table();
    load_pur_inv_table();
    load_sal_inv_table();
};

$(document).on("click", ".nav-btn", function () {

    let target = $(this).data("target");

    if (target === "leave-section"){

        if ($("#leave-section").is(":hidden")) {
            frappe.msgprint({
                title: __("Information"),
                message: __("No Leave Applications are pending for approval."),
                indicator: "orange"
            });
            return;
        }
    }
    else if (target === "expense-section"){

        if ($("#expense-section").is(":hidden")) {
            frappe.msgprint({
                title: __("Information"),
                message: __("No Expense Claims are pending for approval."),
                indicator: "orange"
            });
            return;
        }
    }
    else if (target === "att-section"){

        if ($("#att-section").is(":hidden")) {
            frappe.msgprint({
                title: __("Information"),
                message: __("No Attendance Requests are pending for approval."),
                indicator: "orange"
            });
            return;
        }
    }
    else if (target === "pur-section"){

        if ($("#pur-section").is(":hidden")) {
            frappe.msgprint({
                title: __("Information"),
                message: __("No Purchase Orders are pending for approval."),
                indicator: "orange"
            });
            return;
        }
    }
    else if (target === "pur-inv-section"){

        if ($("#pur-inv-section").is(":hidden")) {
            frappe.msgprint({
                title: __("Information"),
                message: __("No Purchase Invoices are pending for approval."),
                indicator: "orange"
            });
            return;
        }
    }
    else if (target === "sal-inv-section"){

        if ($("#sal-inv-section").is(":hidden")) {
            frappe.msgprint({
                title: __("Information"),
                message: __("No Sales Invoices are pending for approval."),
                indicator: "orange"
            });
            return;
        }
    }

    $("html, body").animate({
        scrollTop: $("#" + target).offset().top
    }, 500);
});


function renderSimpleCard(selector, label, value, color="#0d6efd", icon="fa fa-chart-bar") {

    $(selector).html(`
        <div style="
            width:220px;
            background:#fff;
            border-radius:10px;
            box-shadow:0 2px 8px rgba(0,0,0,.1);
            overflow:hidden;">

            <div style="height:5px;background:${color};"></div>

            <div style="padding:20px;text-align:center;">

                <i class="${icon}" style="font-size:30px;color:${color};"></i>

                <div style="margin-top:10px;font-size:15px;font-weight:600;">
                    ${label}
                </div>

                <div style="margin-top:8px;font-size:28px;font-weight:bold;color:${color};">
                    ${value}
                </div>

            </div>
        </div>
    `);
}

function load_leave_applications() {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_leave_applications",
        callback: function(r) {
            let data = r.message || [];

            // Leave Application
            renderSimpleCard(
                "#leave-card",
                "Leave Applications",
                data.length,
                "#198754",
                "fa fa-calendar-o"
            );

            if (data.length === 0) {
                $("#leave-section").hide();
                return;
            } else {
                $("#leave-section").show();
            }

            let html = `
                <table class="table table-bordered approval-table">
                    <thead>
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">ID</th>
                            <th style="text-align:center;">Emp ID</th>
                            <th style="text-align:center;">Emp Name</th>
                            <th style="text-align:center;">From Date</th>
                            <th style="text-align:center;">To Date</th>
                            <th style="text-align:center;">Total</th>
                            <th style="text-align:center;">Leave Type</th>
                            <th style="text-align:center;">Reason</th>
                            <th style="text-align:center;">Info</th>
                            <th style="text-align:center;">Approve</th>
                            <th style="text-align:center;">Reject</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            function format_date(date) {
                if (!date) return "-";
                return frappe.datetime.str_to_user(date);
            }

            data.forEach((row, idx) => {
                html += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/leave-application/${row.name}" target="_blank">
                                ${row.name}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.employee || "-"}</td>
                        <td style="text-align:left;">${row.employee_name || "-"}</td>
                        <td style="text-align:center;">${format_date(row.from_date)}</td>
                        <td style="text-align:center;">${format_date(row.to_date)}</td>
                        <td style="text-align:center;">${row.total_leave_days || "-"}</td>
                        <td style="text-align:left;">${row.leave_type || "-"}</td>
                        <td style="text-align:left;">${row.description || "-"}</td>
                        <td style="text-align:center;">
                            <button class="btn btn-xs btn-info"
                                onclick="show_leave_details('${row.name}')">
                                <i class="fa fa-info-circle"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-success btn-xs"
                                onclick="approve_leave('${row.name}')">
                                <i class="fa fa-check"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-danger btn-xs"
                                onclick="reject_leave('${row.name}')">
                                <i class="fa fa-times"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            $("#leave-table").html(html);
        }
    });
}
$(document).on("change", "#select_all", function() {

    let checked = $(this).prop("checked");

    $(".leave-check").prop("checked", checked);

});
// All ticed the top check auto tic
$(document).on("change", ".leave-check", function() {

    let total = $(".leave-check").length;
    let checked = $(".leave-check:checked").length;

    $("#select_all").prop("checked", total === checked);

});

window.bulk_approve = function(){

    let selected = [];

    $(".leave-check:checked").each(function(){

        selected.push($(this).val());

    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one document."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.bulk_approve",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Documents Approved",
                indicator:"green"
            });

            load_leave_applications();
        }
    });

}

window.bulk_reject = function(){

    let selected = [];

    $(".leave-check:checked").each(function(){

        selected.push($(this).val());

    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one document."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.bulk_reject",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Documents Rejected",
                indicator:"red"
            });

            load_leave_applications();
        }
    });

}


window.approve_leave = function(docname){

	frappe.call({
		method:"teampro.teampro.page.approvals.approvals.bulk_approve",
		args:{
			docs:[docname]
		},
		callback:function(r){

			frappe.show_alert({
				message:"Approved",
				indicator:"green"
			});

			load_leave_applications();
		}
	});
}

window.reject_leave = function(docname){

	frappe.call({
		method:"teampro.teampro.page.approvals.approvals.bulk_reject",
		args:{
			docs:[docname]
		},
		callback:function(r){

			frappe.show_alert({
				message:"Rejected",
				indicator:"red"
			});

			load_leave_applications();
		}
	});
}

window.show_leave_details = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_leave_details",
        args: { docname: docname },
        callback: function(r) {
            if (!r.message) {
                frappe.msgprint("No Details Found");
                return;
            }

            let d = r.message;

            let dialog = new frappe.ui.Dialog({
                title: "Leave Application Details",
                size: "large",
                fields: [
                    { fieldtype: "HTML", fieldname: "details" }
                ]
            });

            dialog.fields_dict.details.$wrapper.html(`
                <table class="table table-bordered">
                    <tr>
                        <th style="width:25%;">Application ID</th>
                        <td style="width:25%; text-align:left;">
                            <a href="/app/leave-application/${d.name}" target="_blank">${d.name || "-"}</a>
                        </td>
                        <th style="width:25%;">Status</th>
                        <td style="text-align:left;">${d.status || "-"}</td>
                    </tr>
                    <tr>
                        <th>Employee ID</th>
                        <td style="text-align:left;">${d.employee || "-"}</td>
                        <th>Employee Name</th>
                        <td style="text-align:left;">${d.employee_name || "-"}</td>
                    </tr>
                    <tr>
                        <th>From Date</th>
                        <td style="text-align:center;">${d.from_date ? frappe.datetime.str_to_user(d.from_date) : "-"}</td>
                        <th>To Date</th>
                        <td style="text-align:center;">${d.to_date ? frappe.datetime.str_to_user(d.to_date) : "-"}</td>
                    </tr>
                    <tr>
                        <th>Total Days</th>
                        <td style="text-align:center;">${d.total_leave_days || "-"}</td>
                        <th>Leave Type</th>
                        <td style="text-align:left;">${d.leave_type || "-"}</td>
                    </tr>
                    <tr>
                        <th>Half Day</th>
                        <td style="text-align:center;">${d.half_day ? "Yes" : "No"}</td>
                        <th>Half Day Date</th>
                        <td style="text-align:center;">${d.half_day_date ? frappe.datetime.str_to_user(d.half_day_date) : "-"}</td>
                    </tr>
                    <tr>
                        <th>Session</th>
                        <td style="text-align:left;">${d.custom_session || "-"}</td>
                        <th>Reason</th>
                        <td style="text-align:left;">${d.description || "-"}</td>
                    </tr>
                </table>
            `);

            dialog.show();
        }
    });
}

function load_expense_claims() {

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.get_expense_claims",
        callback:function(r){

            let data = r.message || [];
            renderSimpleCard("#expense-card","Expense Claims",data.length,"#fd7e14","fa fa-money");

             if (data.length === 0) {
                $("#expense-section").hide();
                return;
            } else {
                $("#expense-section").show();
            }


            let html = `
        <table class="table table-bordered approval-table">
            <thead>
                <tr>
                    <th style="text-align:center;">S#</th>
                    <th style="text-align:center;">ID</th>
                    <th style="text-align:center;">Emp ID</th>
                    <th style="text-align:center;">Emp Name</th>
                    <th style="text-align:center;">Status</th>
                    <th style="text-align:center;">Grand Total</th>
                    <th style="text-align:center;">Info</th>
                    <th style="text-align:center;">Approve</th>
                    <th style="text-align:center;">Reject</th>
                </tr>
            </thead>
            <tbody>
        `;

        data.forEach((row, idx) => {
            html += `
            <tr>
                <td style="text-align:center;">${idx + 1}</td>
                <td style="text-align:left;">
                    <a href="/app/expense-claim/${row.name}" target="_blank">
                        ${row.name}
                    </a>
                </td>
                <td style="text-align:left;">${row.employee}</td>
                <td style="text-align:left;">${row.employee_name}</td>
                <td style="text-align:left;">${row.workflow_state}</td>
                <td style="text-align:right;">₹${parseFloat(row.grand_total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                <td style="text-align:center;">
                    <button class="btn btn-xs btn-info"
                        onclick="show_expense_details('${row.name}')">
                        <i class="fa fa-info-circle"></i>
                    </button>
                </td>
                <td style="text-align:center;">
                    <button class="btn btn-success btn-xs"
                        onclick="approve_expense('${row.name}')">
                        <i class="fa fa-check"></i>
                    </button>
                </td>
                <td style="text-align:center;">
                    <button class="btn btn-danger btn-xs"
                        onclick="reject_expense('${row.name}')">
                        <i class="fa fa-times"></i>
                    </button>
                </td>
            </tr>
            `;
        });

        html += `</tbody></table>`;

                    $("#expense-table").html(html);
                }
            });
        }

$(document).on("change", "#expense_select_all", function(){

    $(".expense-check").prop(
        "checked",
        $(this).prop("checked")
    );

});

window.show_expense_details = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_expense_details",
        args: { docname: docname },
        callback: function(r) {
            if (!r.message) {
                frappe.msgprint("No Details Found");
                return;
            }

            let d = r.message;

            // Child table rows
            let expenseRows = "";
            (d.expenses || []).forEach((row, idx) => {
                const meetLogLink = row.custom_meet_log
                    ? `<a href="/app/meet-log/${row.custom_meet_log}" target="_blank">${row.custom_meet_log}</a>`
                    : "-";

                expenseRows += `
                    <tr>
                        <td>${idx + 1}</td>
                        <td>${row.expense_date ? frappe.datetime.str_to_user(row.expense_date) : "-"}</td>
                        <td>${row.expense_type || "-"}</td>
                        <td>${row.description || "-"}</td>
                        <td>${meetLogLink}</td>
                        <td>${row.custom_meetlog_distance || "-"}</td>
                        <td>${row.amount || "-"}</td>
                    </tr>
                `;
            });

            let dialog = new frappe.ui.Dialog({
                title: "Expense Claim Details",
                size: "extra-large",
                fields: [
                    { fieldtype: "HTML", fieldname: "details" }
                ]
            });

            dialog.fields_dict.details.$wrapper.html(`
                <!-- Main Info -->
                <table class="table table-bordered" style="margin-bottom:16px;">
                    <tr>
                        <th style="width:30%;">Claim ID</th>
                        <td>${d.name || "-"}</td>
                        <th style="width:30%;">Status</th>
                        <td>${d.workflow_state || "-"}</td>
                    </tr>
                    <tr>
                        <th>Employee ID</th>
                        <td>${d.employee || "-"}</td>
                        <th>Employee Name</th>
                        <td>${d.employee_name || "-"}</td>
                    </tr>
                    <tr>
                        <th>Grand Total</th>
                        <td colspan="3"><strong>₹${d.grand_total || 0}</strong></td>
                    </tr>
                </table>

                <!-- Expense Lines -->
                <h4 style="font-weight:bold; margin-bottom:8px;">Expense Claims</h4>
                <table class="table table-bordered table-sm text-center">
                    <thead style="background:#002060; color:white;">
                        <tr>
                            <th>S#</th>
                            <th>Date</th>
                            <th>Type</th>
                            <th>Description</th>
                            <th>Meet Log</th>
                            <th>Distance</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${expenseRows || '<tr><td colspan="7">No expense lines found</td></tr>'}
                    </tbody>
                </table>
            `);

            dialog.show();
        }
    });
};

$(document).on("change", ".expense-check", function(){

    let total = $(".expense-check").length;
    let checked = $(".expense-check:checked").length;

    $("#expense_select_all").prop(
        "checked",
        total === checked
    );

});

window.bulk_expense_approve = function(){

    let selected = [];

    $(".expense-check:checked").each(function(){

        selected.push($(this).val());

    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one Expense Claim."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.expense_approve",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Expense Claims Processed",
                indicator:"green"
            });

            load_expense_claims();
        }
    });

}

window.bulk_expense_reject = function(){

    let selected = [];

    $(".expense-check:checked").each(function(){
        selected.push($(this).val());
    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one Expense Claim."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.expense_reject",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Expense Claims Rejected",
                indicator:"red"
            });

            load_expense_claims();
        }
    });

}

window.approve_expense = function(docname){

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.expense_approve",
        args:{
            docs:[docname]
        },
        callback:function(r){

            frappe.show_alert({
                message:"Expense Claim Approved",
                indicator:"green"
            });

            load_expense_claims();
        }
    });

}

window.reject_expense = function(docname){

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.expense_reject",
        args:{
            docs:[docname]
        },
        callback:function(r){

            frappe.show_alert({
                message:"Expense Claim Rejected",
                indicator:"red"
            });

            load_expense_claims();
        }
    });

}

function load_att_table() {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_att_applications",
        callback: function(r) {
            let data = r.message || [];

            renderSimpleCard(
                "#attendance-card",
                "Attendance Requests",
                data.length,
                "#0dcaf0",
                "fa fa-calendar"
            );

            if (data.length === 0) {
                $("#att-section").hide();
                return;
            } else {
                $("#att-section").show();
            }

            let html = `
                <table class="table table-bordered approval-table">
                    <thead>
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">ID</th>
                            <th style="text-align:center;">Emp ID</th>
                            <th style="text-align:center;">Emp Name</th>
                            <th style="text-align:center;">From Date</th>
                            <th style="text-align:center;">To Date</th>
                            <th style="text-align:center;">Total</th>
                            <th style="text-align:center;">Reason</th>
                            <th style="text-align:center;">Status</th>
                            <th style="text-align:center;">Info</th>
                            <th style="text-align:center;">Approve</th>
                            <th style="text-align:center;">Reject</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            function format_date(date) {
                if (!date) return "-";
                return frappe.datetime.str_to_user(date);
            }

            data.forEach((row, idx) => {
                html += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/attendance-request/${row.name}" target="_blank">
                                ${row.name}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.employee || "-"}</td>
                        <td style="text-align:left;">${row.employee_name || "-"}</td>
                        <td style="text-align:center;">${format_date(row.from_date)}</td>
                        <td style="text-align:center;">${format_date(row.to_date)}</td>
                        <td style="text-align:center;">${row.total_days || "-"}</td>
                        <td style="text-align:left;">${row.reason || "-"}</td>
                        <td style="text-align:left;">${row.workflow_state || "-"}</td>
                        <td style="text-align:center;">
                            <button class="btn btn-xs btn-info"
                                onclick="show_att_details('${row.name}')">
                                <i class="fa fa-info-circle"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-success btn-xs"
                                onclick="approve_att('${row.name}')">
                                <i class="fa fa-check"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-danger btn-xs"
                                onclick="reject_att('${row.name}')">
                                <i class="fa fa-times"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            $("#att-table").html(html);
        }
    });
}
$(document).on("change", "#att_select_all", function() {

    let checked = $(this).prop("checked");

    
    
    $(".att-check").prop("checked", checked);

});
// All ticed the top check auto tic
$(document).on("change", ".att-check", function() {

    let total = $(".att-check").length;
    let checked = $(".att-check:checked").length;

    $("#att_select_all").prop("checked", total === checked);

});

window.bulk_att_approve = function(){

    let selected = [];

    $(".att-check:checked").each(function(){

        selected.push($(this).val());

    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one document."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.bulk_approve_att",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Documents Approved",
                indicator:"green"
            });

            load_att_table();
        }
    });

}

window.bulk_att_reject = function(){

    let selected = [];

    $(".att-check:checked").each(function(){

        selected.push($(this).val());

    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one document."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.bulk_reject_att",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Documents Rejected",
                indicator:"red"
            });

            load_att_table();
        }
    });

}

window.approve_att = function(docname){

	frappe.call({
		method:"teampro.teampro.page.approvals.approvals.approve_att",
		args:{
			docname:docname
		},
		callback:function(r){

			frappe.show_alert({
				message:"Approved",
				indicator:"green"
			});

			load_att_table();
		}
	});
}

window.reject_att = function(docname){

	frappe.call({
		method:"teampro.teampro.page.approvals.approvals.reject_att",
		args:{
			docname:docname
		},
		callback:function(r){

			frappe.show_alert({
				message:"Rejected",
				indicator:"red"
			});

			load_att_table();
		}
	});
}
window.show_att_details = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_att_details",
        args: { docname: docname },
        callback: function(r) {
            if (!r.message) {
                frappe.msgprint("No Details Found");
                return;
            }

            let d = r.message;

            let dialog = new frappe.ui.Dialog({
                title: "Attendance Request Details",
                size: "large",
                fields: [
                    { fieldtype: "HTML", fieldname: "details" }
                ]
            });

            dialog.fields_dict.details.$wrapper.html(`
                <table class="table table-bordered">
                    <tr>
                        <th style="width:25%;">Application ID</th>
                            <td style="width:25%;">
                                <a href="/app/attendance-request/${d.name}" target="_blank">${d.name || "-"}</a>
                            </td>
                        <th style="width:25%;">Status</th>
                        <td>${d.status || "-"}</td>
                    </tr>
                    <tr>
                        <th>Employee ID</th>
                        <td>${d.employee || "-"}</td>
                        <th>Employee Name</th>
                        <td>${d.employee_name || "-"}</td>
                    </tr>
                    <tr>
                        <th>From Date</th>
                        <td>${d.from_date ? frappe.datetime.str_to_user(d.from_date) : "-"}</td>
                        <th>To Date</th>
                        <td>${d.to_date ? frappe.datetime.str_to_user(d.to_date) : "-"}</td>
                    </tr>
                    <tr>
                        <th>Total Days</th>
                        <td>${d.total_days || "-"}</td>
                        <th>Reason</th>
                        <td>${d.reason || "-"}</td>
                    </tr>
                    <tr>
                        <th>Half Day</th>
                        <td>${d.half_day ? "Yes" : "No"}</td>
                        <th>Half Day Date</th>
                        <td>${d.half_day_date ? frappe.datetime.str_to_user(d.half_day_date) : "-"}</td>
                    </tr>
                    <tr>
                        <th>Session</th>
                        <td>${d.custom_session || "-"}</td>
                        <th>Explanation</th>
                        <td>${d.explanation || "-"}</td>
                    </tr>
                </table>
            `);

            dialog.show();
        }
    });
}

function load_pur_table() {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_pur_applications",
        callback: function(r) {
            let data = r.message || [];

            renderSimpleCard("#po-card","Purchase Orders",data.length,"#6f42c1","fa fa-shopping-cart");

            if (data.length === 0) {
                $("#pur-section").hide();
                return;
            } else {
                $("#pur-section").show();
            }

            let html = `
                <table class="table table-bordered approval-table">
                    <thead>
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">ID</th>
                            <th style="text-align:center;">Supplier</th>
                            <th style="text-align:center;">Date</th>
                            <th style="text-align:center;">Required Date</th>
                            <th style="text-align:center;">Service</th>
                            <th style="text-align:center;">Qty</th>
                            <th style="text-align:center;">Total</th>
                            <th style="text-align:center;">Status</th>
                            <th style="text-align:center;">Info</th>
                            <th style="text-align:center;">Approve</th>
                            <th style="text-align:center;">Reject</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            function format_date(date) {
                if (!date) return "-";
                return frappe.datetime.str_to_user(date);
            }

            data.forEach((row, idx) => {
                html += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/purchase-order/${row.name}" target="_blank">
                                ${row.name}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.supplier || "-"}</td>
                        <td style="text-align:center;">${format_date(row.transaction_date)}</td>
                        <td style="text-align:center;">${format_date(row.schedule_date)}</td>
                        <td style="text-align:left;">${row.custom_service || "-"}</td>
                        <td style="text-align:center;">${row.total_qty || "-"}</td>
                        <td style="text-align:right;">₹${parseFloat(row.total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                        <td style="text-align:left;">${row.status || "-"}</td>
                        <td style="text-align:center;">
                            <button class="btn btn-xs btn-info"
                                onclick="show_pur_details('${row.name}')">
                                <i class="fa fa-info-circle"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-success btn-xs"
                                onclick="approve_pur('${row.name}')">
                                <i class="fa fa-check"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-danger btn-xs"
                                onclick="reject_pur('${row.name}')">
                                <i class="fa fa-times"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            $("#pur-table").html(html);
        }
    });
}

$(document).on("change", "#pur_select_all", function() {

    let checked = $(this).prop("checked");

    
    
    
    $(".pur-check").prop("checked", checked);

});
// All ticed the top check auto tic
$(document).on("change", ".pur-check", function() {

    let total = $(".pur-check").length;
    let checked = $(".pur-check:checked").length;

    $("#pur_select_all").prop("checked", total === checked);

});

window.bulk_pur_approve = function(){

    let selected = [];

    $(".pur-check:checked").each(function(){

        selected.push($(this).val());

    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one document."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.bulk_approve_pur",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Documents Approved",
                indicator:"green"
            });

            load_pur_table();
        }
    });

}

window.bulk_pur_reject = function(){

    let selected = [];

    $(".pur-check:checked").each(function(){

        selected.push($(this).val());

    });

    if(selected.length == 0){

        frappe.msgprint({
            title:"Message",
            indicator:"red",
            message:"Please select at least one document."
        });

        return;
    }

    frappe.call({
        method:"teampro.teampro.page.approvals.approvals.bulk_reject_pur",
        args:{
            docs:selected
        },
        freeze:true,
        callback:function(r){

            frappe.show_alert({
                message:"Documents Rejected",
                indicator:"red"
            });

            load_pur_table();
        }
    });

}

window.approve_pur = function(docname){

	frappe.call({
		method:"teampro.teampro.page.approvals.approvals.approve_pur",
		args:{
			docname:docname
		},
		callback:function(r){

			frappe.show_alert({
				message:"Approved",
				indicator:"green"
			});

			load_pur_table();
		}
	});
}

window.reject_pur = function(docname){

	frappe.call({
		method:"teampro.teampro.page.approvals.approvals.reject_pur",
		args:{
			docname:docname
		},
		callback:function(r){

			frappe.show_alert({
				message:"Rejected",
				indicator:"red"
			});

			load_pur_table();
		}
	});
}

window.show_pur_details = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_pur_details",
        args: { docname: docname },
        callback: function(r) {
            if (!r.message) {
                frappe.msgprint("No Details Found");
                return;
            }

            let d = r.message;

            // ✅ Attachments
            window._current_attachments = d.attachments || [];

            let attachmentBadges = "-";
            if (d.attachments && d.attachments.length > 0) {
                attachmentBadges = d.attachments.map((att, i) => `
                    <span
                        onclick="open_attachment_preview(${i})"
                        style="
                            display:inline-block;
                            background:#4f46e5;
                            color:white;
                            border-radius:50%;
                            width:24px; height:24px;
                            line-height:24px;
                            text-align:center;
                            font-size:11px;
                            font-weight:bold;
                            cursor:pointer;
                            margin-right:4px;
                        "
                        title="${att.file_name}"
                    >${i + 1}</span>
                `).join('');
            }

            let itemRows = "";
            (d.items || []).forEach((row, idx) => {
                let imageCell = "-";
                if (row.image_view) {
                    imageCell = `
                        <a href="${row.image_view}" target="_blank" title="View Image">
                            <i class="fa fa-eye" style="font-size:15px; color:#4f46e5; cursor:pointer;"></i>
                        </a>
                    `;
                }
                itemRows += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/item/${row.item_code}" target="_blank">
                                ${row.item_code || "-"}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.item_name || "-"}</td>
                        <td style="text-align:left;">${row.schedule_date ? frappe.datetime.str_to_user(row.schedule_date) : "-"}</td>
                        <td style="text-align:left;">${row.expected_delivery_date ? frappe.datetime.str_to_user(row.expected_delivery_date) : "-"}</td>
                        <td style="text-align:center;">${row.qty || "-"}</td>
                        <td style="text-align:left;">${row.uom || "-"}</td>
                        <td style="text-align:right;">₹${parseFloat(row.rate || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                        <td style="text-align:right;">₹${parseFloat(row.amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                    </tr>
                `;
            });

            let dialog = new frappe.ui.Dialog({
                title: "Purchase Order Details",
                size: "extra-large",
                fields: [{ fieldtype: "HTML", fieldname: "details" }]
            });

            dialog.fields_dict.details.$wrapper.html(`
                <table class="table table-bordered" style="margin-bottom:16px;">
                    <tr>
                        <th style="width:25%;">Application ID</th>
                        <td style="width:25%; text-align:left;">
                            <a href="/app/purchase-order/${d.name}" target="_blank">${d.name || "-"}</a>
                        </td>
                        <th style="width:25%;">Status</th>
                        <td style="text-align:left;">${d.status || "-"}</td>
                    </tr>
                    <tr>
                        <th>Supplier</th>
                        <td style="text-align:left;">${d.supplier || "-"}</td>
                        <th>Workflow</th>
                        <td style="text-align:left;">${d.workflow_state || "-"}</td>
                    </tr>
                    <tr>
                        <th>Purchase Type</th>
                        <td style="text-align:left;">${d.purchase_type || "-"}</td>
                        <th>Payment Type</th>
                        <td style="text-align:left;">${d.payment_type || "-"}</td>
                    </tr>
                    <tr>
                        <th>Date</th>
                        <td style="text-align:left;">${d.transaction_date ? frappe.datetime.str_to_user(d.transaction_date) : "-"}</td>
                        <th>Required By</th>
                        <td style="text-align:left;">${d.schedule_date ? frappe.datetime.str_to_user(d.schedule_date) : "-"}</td>
                    </tr>
                    <tr>
                        <th>Service</th>
                        <td style="text-align:left;">${d.custom_service || "-"}</td>
                        <th>Total Qty</th>
                        <td style="text-align:center;">${d.total_qty || "-"}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <td><strong>₹${parseFloat(d.total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</strong></td>
                        <th>Attachments</th>
                        <td>${attachmentBadges}</td>
                    </tr>
                </table>

                <h4 style="font-weight:bold; margin-bottom:8px;">Items</h4>
                <table class="table table-bordered table-sm">
                    <thead style="background:#002060; color:white;">
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">Item Code</th>
                            <th style="text-align:center;">Item Name</th>
                            <th style="text-align:center;">Schedule Date</th>
                            <th style="text-align:center;">Expected Delivery</th>
                            <th style="text-align:center;">Qty</th>
                            <th style="text-align:center;">UOM</th>
                            <th style="text-align:center;">Rate</th>
                            <th style="text-align:center;">Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${itemRows || '<tr><td colspan="10" style="text-align:center;">No items found</td></tr>'}
                    </tbody>
                </table>
            `);

            dialog.show();
        }
    });
}



function load_pur_inv_table() {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_pur_inv_applications",
        callback: function(r) {
            let data = r.message || [];
            renderSimpleCard("#pi-card","Purchase Invoices",data.length,"#dc3545","fa fa-file-text");

            if (data.length === 0) {
                $("#pur-inv-section").hide();
                return;
            } else {
                $("#pur-inv-section").show();
            }

            let html = `
                <table class="table table-bordered approval-table">
                    <thead>
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">ID</th>
                            <th style="text-align:center;">Supplier</th>
                            <th style="text-align:center;">Date</th>
                            <th style="text-align:center;">Due Date</th>
                            <th style="text-align:center;">Service</th>
                            <th style="text-align:center;">Bill No</th>
                            <th style="text-align:center;">Total</th>
                            <th style="text-align:center;">Info</th>
                            <th style="text-align:center;">Approve</th>
                            <th style="text-align:center;">Reject</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            function format_date(date) {
                if (!date) return "-";
                return frappe.datetime.str_to_user(date);
            }

            data.forEach((row, idx) => {
                html += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/purchase-invoice/${row.name}" target="_blank">
                                ${row.name}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.supplier || "-"}</td>
                        <td style="text-align:center;">${format_date(row.posting_date)}</td>
                        <td style="text-align:center;">${format_date(row.due_date)}</td>
                        <td style="text-align:left;">${row.services || "-"}</td>
                        <td style="text-align:left;">${row.bill_no || "-"}</td>
                        <td style="text-align:right;">₹${parseFloat(row.total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                        <td style="text-align:center;">
                            <button class="btn btn-xs btn-info"
                                onclick="show_pur_inv_details('${row.name}')">
                                <i class="fa fa-info-circle"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-success btn-xs"
                                onclick="approve_pur_inv('${row.name}')">
                                <i class="fa fa-check"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-danger btn-xs"
                                onclick="reject_pur_inv('${row.name}')">
                                <i class="fa fa-times"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            $("#pur-inv-table").html(html);
        }
    });
}


window.show_pur_inv_details = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_pur_inv_details",
        args: { docname: docname },
        callback: function(r) {
            if (!r.message) {
                frappe.msgprint("No Details Found");
                return;
            }

            let d = r.message;

            // ✅ Once declare, no duplicate
            window._current_attachments = d.attachments || [];

            let attachmentBadges = "-";
            if (d.attachments && d.attachments.length > 0) {
                attachmentBadges = d.attachments.map((att, i) => `
                    <span 
                        onclick="open_attachment_preview(${i})"
                        style="
                            display:inline-block;
                            background:#4f46e5;
                            color:white;
                            border-radius:50%;
                            width:24px; height:24px;
                            line-height:24px;
                            text-align:center;
                            font-size:11px;
                            font-weight:bold;
                            cursor:pointer;
                            margin-right:4px;
                        "
                        title="${att.file_name}"
                    >${i + 1}</span>
                `).join('');
            }

            let itemRows = "";
            (d.items || []).forEach((row, idx) => {
                itemRows += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/item/${row.item_code}" target="_blank">
                                ${row.item_code || "-"}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.item_name || "-"}</td>
                        <td style="text-align:center;">${row.qty || "-"}</td>
                        <td style="text-align:left;">${row.uom || "-"}</td>
                        <td style="text-align:right;">₹${parseFloat(row.rate || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                        <td style="text-align:right;">₹${parseFloat(row.amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                    </tr>
                `;
            });

            let dialog = new frappe.ui.Dialog({
                title: "Purchase Invoice Details",
                size: "extra-large",
                fields: [{ fieldtype: "HTML", fieldname: "details" }]
            });

            dialog.fields_dict.details.$wrapper.html(`
                <table class="table table-bordered" style="margin-bottom:16px;">
                    <tr>
                        <th style="width:25%;">Invoice ID</th>
                        <td style="width:25%; text-align:left;">
                            <a href="/app/purchase-invoice/${d.name}" target="_blank">${d.name || "-"}</a>
                        </td>
                        <th style="width:25%;">Workflow</th>
                        <td style="text-align:left;">${d.workflow_state || "-"}</td>
                    </tr>
                    <tr>
                        <th>Supplier</th>
                        <td style="text-align:left;">${d.supplier || "-"}</td>
                        <th>Bill No</th>
                        <td style="text-align:left;">${d.bill_no || "-"}</td>
                    </tr>
                    <tr>
                        <th>Posting Date</th>
                        <td style="text-align:left;">${d.posting_date ? frappe.datetime.str_to_user(d.posting_date) : "-"}</td>
                        <th>Posting Time</th>
                        <td style="text-align:left;">${d.posting_time || "-"}</td>
                    </tr>
                    <tr>
                        <th>Due Date</th>
                        <td style="text-align:left;">${d.due_date ? frappe.datetime.str_to_user(d.due_date) : "-"}</td>
                        <th>Service</th>
                        <td style="text-align:left;">${d.services || "-"}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <td><strong>₹${parseFloat(d.total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</strong></td>
                        <th>Attachments</th>
                        <td>${attachmentBadges}</td>
                    </tr>
                </table>

                <h4 style="font-weight:bold; margin-bottom:8px;">Items</h4>
                <table class="table table-bordered table-sm">
                    <thead style="background:#002060; color:white;">
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">Item Code</th>
                            <th style="text-align:center;">Item Name</th>
                            <th style="text-align:center;">Qty</th>
                            <th style="text-align:center;">UOM</th>
                            <th style="text-align:center;">Rate</th>
                            <th style="text-align:center;">Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${itemRows || '<tr><td colspan="7" style="text-align:center;">No items found</td></tr>'}
                    </tbody>
                </table>
            `);

            dialog.show();
        }
    });
}

window.open_attachment_preview = function(index) {
    const att = window._current_attachments[index];
    if (!att) return;

    const file_url = att.file_url;
    const full_url = file_url.startsWith('http') ? file_url : window.location.origin + file_url;

    // ✅ Direct open — no dialog, no confirm
    window.open(full_url, '_blank');
}

// opne pdf via , the pdf is open in new tab

// window.open_attachment_preview = function(index) {
//     const att = window._current_attachments[index];
//     if (!att) return;

//     const file_url = att.file_url;
//     const file_name = att.file_name;
//     const full_url = file_url.startsWith('http') ? file_url : window.location.origin + file_url;

//     const isPdf = file_name.toLowerCase().endsWith('.pdf');
//     const isImage = /\.(png|jpg|jpeg|gif|webp)$/i.test(file_name);

//     let preview_html = "";

//     if (isPdf) {
//         preview_html = `
//             <div style="text-align:center; padding:30px;">
//                 <i class="fa fa-file-pdf-o" style="font-size:40px; color:#ef4444;"></i>
//                 <p style="margin-top:10px; font-weight:bold;">${file_name}</p>
//                 <a href="${full_url}" target="_blank" class="btn btn-primary btn-sm">
//                     <i class="fa fa-external-link"></i> Open PDF
//                 </a>
//             </div>
//         `;
//     } else if (isImage) {
//         preview_html = `
//             <img src="${full_url}" style="max-width:100%; max-height:500px; display:block; margin:auto;">
//         `;
//     } else {
//         preview_html = `
//             <div style="text-align:center; padding:30px;">
//                 <i class="fa fa-file" style="font-size:40px; color:#4f46e5;"></i>
//                 <p style="margin-top:10px; font-weight:bold;">${file_name}</p>
//                 <a href="${full_url}" target="_blank" class="btn btn-primary btn-sm">
//                     <i class="fa fa-download"></i> Download
//                 </a>
//             </div>
//         `;
//     }

//     let att_dialog = new frappe.ui.Dialog({
//         title: "Attachment",
//         size: "large",
//         fields: [{ fieldtype: "HTML", fieldname: "preview" }]
//     });

//     att_dialog.fields_dict.preview.$wrapper.html(preview_html);
//     att_dialog.show();
// }

window.approve_pur_inv = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.approve_pur_inv",
        args: { docname: docname },
        callback: function(r) {
            if (r.message === "ok") {
                frappe.show_alert({
                    message: `${docname} Approved`,
                    indicator: "green"
                });
                load_pur_inv_table();
            }
        }
    });
}


function load_sal_inv_table() {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_sal_inv_applications",
        callback: function(r) {
            let data = r.message || [];
            renderSimpleCard("#si-card","Sales Invoices",data.length,"#20c997","fa fa-file");

            if (data.length === 0) {
                $("#sal-inv-section").hide();
                return;
            } else {
                $("#sal-inv-section").show();
            }

            let html = `
                <table class="table table-bordered approval-table">
                    <thead>
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">ID</th>
                            <th style="text-align:center;">Customer</th>
                            <th style="text-align:center;">Posting Date</th>
                            <th style="text-align:center;">RC Invoice</th>
                            <th style="text-align:center;">POS Profile</th>
                            <th style="text-align:center;">Service</th>
                            <th style="text-align:center;">Company</th>
                            <th style="text-align:center;">Total Qty</th>
                            <th style="text-align:center;">Total</th>
                            <th style="text-align:center;">Info</th>
                            <th style="text-align:center;">Approve</th>
                            <th style="text-align:center;">Reject</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            function format_date(date) {
                if (!date) return "-";
                return frappe.datetime.str_to_user(date);
            }

            data.forEach((row, idx) => {
                html += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/sales-invoice/${row.name}" target="_blank">
                                ${row.name}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.customer || "-"}</td>
                        <td style="text-align:center;">${format_date(row.posting_date)}</td>
                        <td style="text-align:left;">${row.custom_rc_invoice_ || "-"}</td>
                        <td style="text-align:left;">${row.pos_profile || "-"}</td>
                        <td style="text-align:left;">${row.services || "-"}</td>
                        <td style="text-align:left;">${row.company || "-"}</td>
                        <td style="text-align:center;">${row.total_qty || "-"}</td>
                        <td style="text-align:right;">₹${parseFloat(row.total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                        <td style="text-align:center;">
                            <button class="btn btn-xs btn-info"
                                onclick="show_sal_inv_details('${row.name}')">
                                <i class="fa fa-info-circle"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-success btn-xs"
                                onclick="approve_sal_inv('${row.name}')">
                                <i class="fa fa-check"></i>
                            </button>
                        </td>
                        <td style="text-align:center;">
                            <button class="btn btn-danger btn-xs"
                                onclick="reject_sal_inv('${row.name}')">
                                <i class="fa fa-times"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            $("#sal-inv-table").html(html);
        }
    });
}

window.approve_sal_inv = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.approve_sal_inv",
        args: { docname: docname },
        callback: function(r) {
            if (r.message === "ok") {
                frappe.show_alert({
                    message: `${docname} Approved`,
                    indicator: "green"
                });
                load_sal_inv_table();
            }
        }
    });
}


// window.show_sal_inv_details = function(docname) {
//     frappe.call({
//         method: "teampro.teampro.page.approvals.approvals.get_sal_inv_details",
//         args: { docname: docname },
//         callback: function(r) {
//             if (!r.message) {
//                 frappe.msgprint("No Details Found");
//                 return;
//             }

//             let d = r.message;

//             function fmt_date(date) {
//                 return date ? frappe.datetime.str_to_user(date) : "-";
//             }

//             // Items table
//             let itemRows = "";
//             (d.items || []).forEach((row, idx) => {

//                 let imageCell = "-";
//                 if (row.image_view) {
//                     imageCell = `
//                         <a href="${row.image_view}" target="_blank" title="View Image">
//                             <i class="fa fa-eye" style="font-size:15px; color:#4f46e5; cursor:pointer;"></i>
//                         </a>
//                     `;
//                 }

//                 itemRows += `
//                     <tr>
//                         <td style="text-align:center;">${idx + 1}</td>
//                         <td style="text-align:left;">
//                             <a href="/app/item/${row.item_code}" target="_blank">
//                                 ${row.item_code || "-"}
//                             </a>
//                         </td>
//                         <td style="text-align:left;">${row.item_name || "-"}</td>
//                         <td style="text-align:center;">${row.qty || "-"}</td>
//                         <td style="text-align:left;">${row.uom || "-"}</td>
//                         <td style="text-align:center;">${row.stock_qty || "-"}</td>
//                         <td style="text-align:right;">₹${parseFloat(row.rate || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
//                     </tr>
//                 `;
//             });

//             // Taxes table
//             let taxRows = "";
//             (d.taxes || []).forEach((row, idx) => {
//                 taxRows += `
//                     <tr>
//                         <td style="text-align:center;">${idx + 1}</td>
//                         <td style="text-align:left;">${row.charge_type || "-"}</td>
//                         <td style="text-align:left;">${row.account_head || "-"}</td>
//                         <td style="text-align:left;">${row.description || "-"}</td>
//                         <td style="text-align:center;">${row.rate || "-"}%</td>
//                         <td style="text-align:right;">₹${parseFloat(row.base_total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
//                     </tr>
//                 `;
//             });

//             let dialog = new frappe.ui.Dialog({
//                 title: "Sales Invoice Details",
//                 size: "extra-large",
//                 fields: [
//                     { fieldtype: "HTML", fieldname: "details" }
//                 ]
//             });

//             dialog.fields_dict.details.$wrapper.html(`
//                 <!-- Main Info -->
//                 <table class="table table-bordered" style="margin-bottom:16px;">
//                     <tr>
//                         <th style="width:25%;">Invoice ID</th>
//                         <td style="width:25%; text-align:left;">
//                             <a href="/app/sales-invoice/${d.name}" target="_blank">${d.name || "-"}</a>
//                         </td>
//                         <th style="width:25%;">Workflow</th>
//                         <td style="text-align:left;">${d.workflow_state || "-"}</td>
//                     </tr>
//                     <tr>
//                         <th>Customer</th>
//                         <td style="text-align:left;">${d.customer || "-"}</td>
//                         <th>Company</th>
//                         <td style="text-align:left;">${d.company || "-"}</td>
//                     </tr>
//                     <tr>
//                         <th>Posting Date</th>
//                         <td style="text-align:left;">${fmt_date(d.posting_date)}</td>
//                         <th>RC Invoice</th>
//                         <td style="text-align:left;">${d.custom_rc_invoice_ || "-"}</td>
//                     </tr>
//                     <tr>
//                         <th>POS Profile</th>
//                         <td style="text-align:left;">${d.pos_profile || "-"}</td>
//                         <th>Service</th>
//                         <td style="text-align:left;">${d.services || "-"}</td>
//                     </tr>
//                     <tr>
//                         <th>Total Qty</th>
//                         <td style="text-align:center;">${d.total_qty || "-"}</td>
//                         <th>Total</th>
//                         <td style="text-align:right;">
//                             <strong>₹${parseFloat(d.total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</strong>
//                         </td>
//                     </tr>
//                 </table>

//                 <!-- Items Table -->
//                 <h4 style="font-weight:bold; margin-bottom:8px;">Items</h4>
//                 <table class="table table-bordered table-sm" style="margin-bottom:16px;">
//                     <thead style="background:#002060; color:white;">
//                         <tr>
//                             <th style="text-align:center;">S#</th>
//                             <th style="text-align:center;">Item Code</th>
//                             <th style="text-align:center;">Item Name</th>
//                             <th style="text-align:center;">Qty</th>
//                             <th style="text-align:center;">UOM</th>
//                             <th style="text-align:center;">Stock Qty</th>
//                             <th style="text-align:center;">Rate</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         ${itemRows || '<tr><td colspan="8" style="text-align:center;">No items found</td></tr>'}
//                     </tbody>
//                 </table>

                
//             `);

//             dialog.show();
//         }
//     });
// }


window.show_sal_inv_details = function(docname) {
    frappe.call({
        method: "teampro.teampro.page.approvals.approvals.get_sal_inv_details",
        args: { docname: docname },
        callback: function(r) {
            if (!r.message) {
                frappe.msgprint("No Details Found");
                return;
            }

            let d = r.message;

            function fmt_date(date) {
                return date ? frappe.datetime.str_to_user(date) : "-";
            }

            // ✅ Attachments
            window._current_attachments = d.attachments || [];

            let attachmentBadges = "-";
            if (d.attachments && d.attachments.length > 0) {
                attachmentBadges = d.attachments.map((att, i) => `
                    <span
                        onclick="open_attachment_preview(${i})"
                        style="
                            display:inline-block;
                            background:#4f46e5;
                            color:white;
                            border-radius:50%;
                            width:24px; height:24px;
                            line-height:24px;
                            text-align:center;
                            font-size:11px;
                            font-weight:bold;
                            cursor:pointer;
                            margin-right:4px;
                        "
                        title="${att.file_name}"
                    >${i + 1}</span>
                `).join('');
            }

            // Items table
            let itemRows = "";
            (d.items || []).forEach((row, idx) => {
                let imageCell = "-";
                if (row.image_view) {
                    imageCell = `
                        <a href="${row.image_view}" target="_blank" title="View Image">
                            <i class="fa fa-eye" style="font-size:15px; color:#4f46e5; cursor:pointer;"></i>
                        </a>
                    `;
                }
                itemRows += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">
                            <a href="/app/item/${row.item_code}" target="_blank">
                                ${row.item_code || "-"}
                            </a>
                        </td>
                        <td style="text-align:left;">${row.item_name || "-"}</td>
                        <td style="text-align:center;">${row.qty || "-"}</td>
                        <td style="text-align:left;">${row.uom || "-"}</td>
                        <td style="text-align:center;">₹${row.mrp || "-"}</td>
                        <td style="text-align:right;">₹${parseFloat(row.base_net_amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                    </tr>
                `;
            });

            // Taxes table
            let taxRows = "";
            (d.taxes || []).forEach((row, idx) => {
                taxRows += `
                    <tr>
                        <td style="text-align:center;">${idx + 1}</td>
                        <td style="text-align:left;">${row.charge_type || "-"}</td>
                        <td style="text-align:left;">${row.account_head || "-"}</td>
                        <td style="text-align:left;">${row.description || "-"}</td>
                        <td style="text-align:center;">${row.rate || "-"}%</td>
                        <td style="text-align:right;">₹${parseFloat(row.base_total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                    </tr>
                `;
            });

            let dialog = new frappe.ui.Dialog({
                title: "Sales Invoice Details",
                size: "extra-large",
                fields: [{ fieldtype: "HTML", fieldname: "details" }]
            });

            dialog.fields_dict.details.$wrapper.html(`
                <table class="table table-bordered" style="margin-bottom:16px;">
                    <tr>
                        <th style="width:25%;">Invoice ID</th>
                        <td style="width:25%; text-align:left;">
                            <a href="/app/sales-invoice/${d.name}" target="_blank">${d.name || "-"}</a>
                        </td>
                        <th style="width:25%;">Workflow</th>
                        <td style="text-align:left;">${d.workflow_state || "-"}</td>
                    </tr>
                    <tr>
                        <th>Customer</th>
                        <td style="text-align:left;">${d.customer || "-"}</td>
                        <th>Company</th>
                        <td style="text-align:left;">${d.company || "-"}</td>
                    </tr>
                    <tr>
                        <th>Posting Date</th>
                        <td style="text-align:left;">${fmt_date(d.posting_date)}</td>
                        <th>RC Invoice</th>
                        <td style="text-align:left;">${d.custom_rc_invoice_ || "-"}</td>
                    </tr>
                    <tr>
                        <th>Service</th>
                        <td style="text-align:left;">${d.services || "-"}</td>
                        <th>Total Qty</th>
                        <td style="text-align:center;">${d.total_qty || "-"}</td>
                    </tr>
                    <tr>
                        <th>Total</th>
                        <td style="text-align:right;">
                            <strong>₹${parseFloat(d.total || 0).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</strong>
                        </td>
                        <th>Attachments</th>
                        <td>${attachmentBadges}</td>
                    </tr>
                    
                </table>

                <h4 style="font-weight:bold; margin-bottom:8px;">Items</h4>
                <table class="table table-bordered table-sm" style="margin-bottom:16px;">
                    <thead style="background:#002060; color:white;">
                        <tr>
                            <th style="text-align:center;">S#</th>
                            <th style="text-align:center;">Item Code</th>
                            <th style="text-align:center;">Item Name</th>
                            <th style="text-align:center;">Qty</th>
                            <th style="text-align:center;">UOM</th>
                            <th style="text-align:center;">MRP</th>
                            <th style="text-align:center;">Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${itemRows || '<tr><td colspan="8" style="text-align:center;">No items found</td></tr>'}
                    </tbody>
                </table>

                
            `);

            dialog.show();
        }
    });
}

