
frappe.pages['employee-target-moni'].on_page_load = function(wrapper) {

	let page = frappe.ui.make_app_page({
		parent: wrapper,
		single_column: true
	});

	// ===== FORMAT =====
	function formatINR(val){
		return (val || 0).toLocaleString('en-IN',{maximumFractionDigits:0});
	}

	// ✅ SAFE ID (FIX FOR YOUR ERROR)
	function makeSafeId(text){
		return text.toLowerCase()
			.replace(/\s+/g,"_")
			.replace(/[^a-z0-9_]/g,"");
	}

	$(page.body).html(`
	<style>

.section{
	margin-bottom:16px;
}

/* ===== DEPARTMENT CARD ===== */
.dept-box{
	background: linear-gradient(135deg,#eef2ff,#e3f2fd);
	padding:14px 16px;
	border-radius:12px;
	cursor:pointer;
	font-weight:600;
	display:flex;
	justify-content:space-between;
	align-items:center;
	box-shadow:0 4px 10px rgba(0,0,0,0.05);
	transition:all 0.3s ease;
}

.dept-box:hover{
	transform:translateY(-2px);
	box-shadow:0 6px 16px rgba(0,0,0,0.1);
}

/* arrow */
.dept-left{
	display:flex;
	align-items:center;
	gap:10px;
}

.dept-arrow{
	font-size:14px;
	transition:0.3s;
}

/* rotate arrow */
.dept-box.active .dept-arrow{
	transform:rotate(90deg);
}

/* ===== EMPLOYEE CONTAINER ===== */
.emp-container{
	display:none;
	padding:12px;
	margin-top:8px;
	border-radius:10px;
	background:#fafafa;
	border:1px solid #eee;
}

/* ===== EMPLOYEE CARD ===== */
.employee-card{
	background:#ffffff;
	border-radius:12px;
	padding:10px;
	box-shadow:0 2px 6px rgba(0,0,0,0.08);
	text-align:center;
	cursor:pointer;
	margin:6px;
	width:120px;
	transition:all 0.25s ease;
	border:1px solid transparent;
}

.employee-card:hover{
	transform:translateY(-3px);
	box-shadow:0 6px 14px rgba(0,0,0,0.12);
}

.employee-card.active{
	border:2px solid #1a237e;
	background:#eef2ff;
}
.pill {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    
    width: 150px;          /* ✅ fixed width */
    height: 70px;         /* ✅ fixed height */

    padding: 6px;
    border-radius: 12px;
    box-sizing: border-box;

    font-size: 9px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
    .pill-value {
    font-size: 10px;
    font-weight: 600;
    white-space: nowrap;     /* ✅ no wrap */
    overflow: hidden;
    text-overflow: ellipsis; /* optional */
}
    .pill-top {
    display: flex;
    align-items: center;
    justify-content: center;  /* ✅ center horizontally */
    gap: 5px;
}
    /* 🔥 YTD (Rich Green) */
.pill.ytd {
    background: #0b5d3b;   /* solid deep green */
    color: #00e676;
}

/* 🔥 MTD (Rich Blue) */
.pill.mtd {
    background: #0d2f6b;   /* solid deep blue */
    color: #82b1ff;
}

/* 🔥 INC (Rich Orange/Brown) */
.pill.inc {
    background: #6b3200;   /* solid dark orange */
    color: #ffab40;
}
    .pill-group {
    display: flex;
    gap: 10px;
    align-items: center;   /* ✅ vertical alignment */
}
    /* SPLIT CELL */
.split-cell {
    display: flex;
    width: 100%;
    border-radius: 8px;
    overflow: hidden;
}

/* LEFT = POINT */
.point-box {
    width: 50%;
    background: #e8f5e9; /* light green */
    color: #1b5e20;
    font-weight: 600;
    text-align: center;
    padding: 4px;
}

/* RIGHT = VALUE */
.value-box {
    width: 50%;
    background: #e3f2fd; /* light blue */
    color: #0d47a1;
    text-align: center;
    padding: 4px;
}
/* ===== TABLE ===== */
.target-table{
	width:100%;
	margin-top:15px;
	border-collapse:collapse;
	border-radius:10px;
	overflow:hidden;
}
.emp-grid{
    display:flex;
    flex-wrap:wrap;
    align-items:flex-start;
}

.emp-detail-row{
    width:100%;
}
.target-table th{
	background:linear-gradient(135deg,#0f1568,#1a237e);
	color:#fff;
	padding:10px;
	font-size:13px;
}

.target-table td{
	padding:10px;
	border-bottom:1px solid #eee;
	font-size:13px;
}

.label-cell{
	text-align:center;
	font-weight:600;
	color:#1a237e;
}

.value-cell{
	text-align:right;
	font-weight:500;
	color:#004d40;
}
 .employee-card{
    background:#ffffff;
    border-radius:12px;
    padding:10px;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
    text-align:center;
    cursor:pointer;
    margin:6px;

    width:140px;
    height:200px;              /* ✅ FIXED HEIGHT (important) */

    display:flex;
    flex-direction:column;
    justify-content:space-between; /* ✅ evenly spaced */

    transition:all 0.25s ease;
    border:1px solid transparent;
}

.emp-img-wrap{
    width:75%;
    height:100px;
    overflow:hidden;
    border-radius:10px;
    background:#f5f5f5;
    text-align:center;
    margin: 0 auto;   
}

.emp-img-rect{
    width:100%;
    height:105%;
    object-fit:cover;
}

/* TEXT CONTROL */
.emp-info{
    height:60px;              /* ✅ FIXED TEXT AREA */
    display:flex;
    flex-direction:column;
    justify-content:center;
}

/* NAME - MAX 2 LINES */
.emp-name{
    font-size:13px;
    font-weight:600;
    color:#1a237e;

    display:-webkit-box;
    -webkit-line-clamp:2;     /* ✅ max 2 lines */
    -webkit-box-orient:vertical;
    overflow:hidden;
}

/* DESIGNATION - MAX 1 LINE */
.emp-designation{
    font-size:11px;
    color:#777;

    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;   /* ✅ truncate */
}
    
</style>

	<h3 style="text-align:center;">TARGET MONITOR</h3>
	<div id="current-datetime" style="font-size: 16px; color: #666; text-align: center; margin-top: 5px;"></div>
	<div id="department_section"></div>

	<hr>

	<div id="employee_detail_section"></div>
	`);

	load_departments();
	function updateDateTime() {
		const now = new Date();
		const dateStr = now.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
		const timeStr = now.toLocaleTimeString();
		document.getElementById('current-datetime').innerHTML = `${dateStr} | ${timeStr}`;
	}
	updateDateTime();
	setInterval(updateDateTime, 1000);
	// ===== LOAD DEPARTMENTS =====
// 	function load_departments(){

// 		frappe.call({
// 			method:"teampro.teampro.page.employee_target_moni.employee_target_monitor.get_department_data_all",
// 			callback:function(res){

// 				let html="";

// 				Object.keys(res.message || {}).forEach(dept=>{

// 					let d = res.message[dept];
// 					let safe_id = makeSafeId(dept);

// 					html += `
// <div class="section">

// 	<div class="dept-box" data-dept="${dept}">
		
// 		<div class="dept-left">
// 			<span class="dept-arrow">▶</span>
// 			<span>${dept}</span>
// 		</div>

// 		<div>
// 			<span style="margin-right:15px;">
// 				Target: ₹ ${formatINR(d.hod_target)}
// 			</span>
// 			<span>
// 				Achieved: ₹ ${formatINR(d.hod_achieved)}
// 			</span>
// 		</div>

// 	</div>

// 	<div class="emp-container" id="emp_${safe_id}"></div>

// </div>`;
// 				});

// 				$("#department_section").html(html);

// 				// CLICK DEPARTMENT
// 				$(".dept-box").click(function(){

// 	let dept = $(this).data("dept");
// 	let safe_id = makeSafeId(dept);
// 	let container = $(`#emp_${safe_id}`);

// 	// toggle active class (for arrow rotation)
// 	$(this).toggleClass("active");

// 	// smooth animation
// 	container.stop(true,true).slideToggle(200);

// 	// load only once
// 	if(!container.hasClass("loaded")){
// 		load_employees(dept, container);
// 		container.addClass("loaded");
// 	}
// });
// 			}
// 		});
// 	}
	function load_departments(){

    frappe.call({
        method: "teampro.teampro.page.employee_target_moni.employee_target_monitor.get_department_data_all",
        callback: function(res){

            let html = "";

            // 🔢 % calculator
            function getPercent(a, t){
                return t ? Math.min((a/t)*100, 100) : 0;
            }

            // 🎯 SVG Ring
           function ring(percent, color){

    let r = 16;        // radius
    let stroke = 4;    // thickness

    let size = 40;     // ✅ SVG size (must be > 2*r)
    let center = size / 2;

    let c = 2 * Math.PI * r;
    let offset = c - (percent/100) * c;

    return `
<svg width="${size}" height="${size}" style="transform:rotate(-90deg)">
    
    <!-- Background circle -->
    <circle 
        cx="${center}" 
        cy="${center}" 
        r="${r}" 
        stroke="#1f1f1f" 
        stroke-width="${stroke}" 
        fill="none">
    </circle>

    <!-- Progress circle -->
    <circle 
        cx="${center}" 
        cy="${center}" 
        r="${r}" 
        stroke="${color}" 
        stroke-width="${stroke}"
        fill="none"
        stroke-linecap="round"
        stroke-dasharray="${c}"
        stroke-dashoffset="${offset}"
        style="transition: stroke-dashoffset 0.6s ease;">
    </circle>

    <!-- % text -->
    <text 
        x="${center}" 
        y="${center + 2}" 
        text-anchor="middle"
        font-size="11"
        fill="#ffffff"
        font-weight="bold"
        transform="rotate(90,${center},${center})">
        ${Math.round(percent)}%
    </text>

</svg>`;
            }

            // 🔐 Safe ID generator
            function makeSafeId(text){
                return text.replace(/[^a-zA-Z0-9]/g, "_");
            }

            Object.keys(res.message || {}).forEach(dept => {

                let d = res.message[dept];
                let safe_id = makeSafeId(dept);

                let ytd = getPercent(d.hod_achieved, d.hod_target);
                let mtd = getPercent(d.mtd_achieved, d.mtd_target);
                let inc = 0; // future use

              html += `
                <div class="section">

                    <div class="dept-box" data-dept="${dept}">

                        <!-- LEFT -->
                        <div class="dept-left">
                            <span class="dept-arrow">▶</span>
                            <span class="dept-name">${dept}</span>
                        </div>

                        <!-- RIGHT PILLS -->
                        <div class="pill-group">

                            <!-- YTD -->
                            <div class="pill ytd">
                                <div class="pill-top">
                                    ${ring(ytd, "#00c853")}
                                    <span class="pill-value">
                                       ${(d.hod_achieved || 0).toFixed(2)} / ${(d.hod_target || 0).toFixed(2)}
                                    </span>
                                </div>
                                <div class="pill-label">YTD</div>
                            </div>

                            <!-- MTD -->
                            <div class="pill mtd">
                                <div class="pill-top">
                                    ${ring(mtd, "#2962ff")}
                                    <span class="pill-value">
                                        ${(d.mtd_achieved || 0).toFixed(2)} / ${(d.mtd_target || 0).toFixed(2)}
                                    </span>
                                </div>
                                <div class="pill-label">MTD</div>
                            </div>

                            <!-- INC -->
                            <div class="pill inc">
                                <div class="pill-top">
                                    ${ring(inc, "#ff6f00")}
                                    <span class="pill-value">0 / 0</span>
                                </div>
                                <div class="pill-label">INCENTIVE</div>
                            </div>

                        </div>

                    </div>

            <div class="emp-container" id="emp_${safe_id}" style="display:none;"></div>

        </div>`;
            });

            $("#department_section").html(html);

            // 👉 CLICK EVENT
            $(".dept-box").click(function(){

                let dept = $(this).data("dept");
                let safe_id = makeSafeId(dept);
                let container = $(`#emp_${safe_id}`);

                // rotate arrow
                $(this).find(".dept-arrow").toggleClass("rotate");

                // smooth slide
                container.stop(true,true).slideToggle(200);

                // load once
                if(!container.hasClass("loaded")){
                    load_employees(dept, container);
                    container.addClass("loaded");
                }
            });

        }
    });
}
	// ===== LOAD EMPLOYEES =====
	function load_employees(dept, container){

	frappe.call({
		method:"teampro.teampro.page.employee_target_moni.employee_target_monitor.get_employees_with_targets",
		args:{
			department: dept
		},
		callback:function(r){

			let html = `<div class="emp-grid">`;
			(r.message || []).forEach(emp=>{

				let img = emp.image || "/assets/frappe/images/ui/avatar.png";

				html += `
<div class="employee-card" data-id="${emp.employee}">

    <div class="emp-img-wrap">
        <img src="${img}" class="emp-img-rect">
    </div>

    <div class="emp-divider"></div>

    <div class="emp-info">
        <div class="emp-name">${emp.employee_name}</div>
        <div class="emp-designation">${emp.designation || ""}</div>
    </div>

</div>`;
			});

			html += `</div>`;

			container.html(html);

			// container.find(".employee-card").click(function(){

			// 	let emp = $(this).data("id");

			// 	$(".employee-card").removeClass("active");
			// 	$(this).addClass("active");

			// 	show_employee_details(emp);
			// });
            container.find(".employee-card").click(function(){

    let emp = $(this).data("id");

    $(".employee-card").removeClass("active");
    $(this).addClass("active");

    // remove old detail row
    container.find(".emp-detail-row").remove();

    // ✅ create full-width row
    let detailRow = $('<div class="emp-detail-row"></div>');

    // ✅ append at END (not after card)
    container.find(".emp-grid").append(detailRow);

    // load details
    show_employee_details(emp, detailRow);
});
		}
	});
}

	// ===== EMPLOYEE DETAILS =====
// 	function show_employee_details(employee){

//     let wrapper = $("#employee_detail_section");
//     wrapper.html("<h4>Loading...</h4>");

//     let common_style = `
//     <style>
//     .target-card {
//         background: #ffffff;
//         border-radius: 12px;
//         box-shadow: 0 8px 20px rgba(0,0,0,0.08);
//         margin-bottom:20px;
//         overflow:hidden;
//     }

//     .target-table {
//         width: 100%;
//         border-collapse: separate;
//         border-spacing: 0;
//     }

//     .target-table th {
//         background: linear-gradient(135deg, #0f1568, #1a237e);
//         color: #fff;
//         text-align: center;
//         padding: 14px;
//     }

//     .target-table td {
//         padding: 14px;
//         border-bottom: 1px solid #e0e0e0;
//     }

//     .label-cell {
//         text-align: center;
//         font-weight: 600;
//         color: #1a237e;
//     }

//     .value-cell {
//         text-align: right;
//         font-weight: 500;
//         color: #004d40;
//     }

//     .sr-badge {
//         display: inline-block;
//         padding: 10px 18px;
//         background: linear-gradient(135deg, #00c853, #43a047);
//         color: white;
//         font-weight: 700;
//         border-radius: 50px;
//     }
//         /* MAIN WRAPPER */
// .dual-table {
//     display: flex;
//     gap: 10px;
// }

// /* EACH HALF */
// .half-table {
//     width: 50%;
//     background: #fafafa;
//     border-radius: 10px;
//     padding: 8px;
//     box-shadow: 0 2px 6px rgba(0,0,0,0.05);
// }

// /* POINT TABLE */
// .point-table th {
//     background: #2e7d32;
// }

// /* VALUE TABLE */
// .value-table th {
//     background: #1565c0;
// }

// /* TABLE COMMON */
// .half-table table {
//     width: 100%;
//     border-collapse: collapse;
// }

// .half-table td {
//     text-align: right;
//     padding: 8px;
//     border-bottom: 1px solid #eee;
// }

// .half-table td:first-child {
//     text-align: left;
//     font-weight: 600;
// }
//     /* YEAR TABLE COLORS */
// .year-point {
//     color: rgba(3, 66, 7, 0.6);   /* green 60% */
//     font-weight:bold
// }

// .year-value {
//     color: rgba(10, 84, 194, 0.6);  /* blue 60% */
// }
//     /* SIDE BY SIDE */
// .dual-table-wrapper{
//     display:flex;
//     gap:15px;
//     margin-top:10px;
// }

// /* EACH CARD */
// .half-card{
//     width:50%;
//     background:#f7f9fc;
//     padding:10px;
//     border-radius:12px;
//     box-shadow:0 3px 10px rgba(0,0,0,0.05);
// }

// /* YEAR COLORS */
// .year-point{
//     color:#1b5e20;   /* green */
//     font-weight:600;
// }

// .year-value{
//     color:#1565c0;   /* blue */
//     font-size:12px;
// }

// /* TABLE FIX */
// .target-table{
//     width:100%;
//     font-size:12px;
// }
//     </style>
//     `;

//     wrapper.html(common_style);

//     // ===== YTD =====
//     frappe.call({
//         method:"teampro.teampro.page.employee_target_moni.employee_target_monitor.get_company_points",
//         args:{employee:employee},
//         callback:function(r){

//             let data = r.message || {};

//             let tot_ct = data.total_ct || 0;
//             let tot_ach = data.total_ach || 0;
//             let points = data.point_value || 1;
// 			let revised_ct=data.revised_ct||0;
//             let yta = tot_ct - tot_ach;
//             let sr =(tot_ach/tot_ct)*100||0;

//             let ytd_html = `
//             <h3>YEAR</h3>

//             <div class="target-card">
//             <table class="target-table">

//                 <tr>
//                     <th>YTD</th>
//                     <th>Target</th>
//                     <th>Achieved</th>
//                     <th>YTA</th>
//                     <th>SR%</th>
//                 </tr>

//                 <tr>
//                     <td class="label-cell">Point (Target)</td>
//                     <td class="value-cell">
//                             <span class="year-point">${(tot_ct/points).toFixed(2)}</span>
//                             (
//                             <span class="year-value">₹ ${formatCompactINR(tot_ct)}</span>
//                             )
//                         </td>
//                     <td class="value-cell">
//                             <span class="year-point">${(tot_ach/points).toFixed(2)}</span>
//                             (
//                             <span class="year-value"> ₹ ${formatCompactINR(tot_ach)} </span>
//                             )
//                         </td>
//                     <td class="value-cell">
//                             <span class="year-point">${(yta/points).toFixed(2)}</span>
//                             (
//                             <span class="year-value">₹ ${formatCompactINR(yta)}</span>
//                             )
//                         </td>
                    

//                     <td class="label-cell">
//                         <span class="sr-badge">${sr.toFixed(1)}%</span>
//                     </td>
//                 </tr>

               

//             </table>
//             </div>
//             `;

//             wrapper.append(ytd_html);

//             // ===== MTD AFTER YTD (USES SAME POINT VALUE) =====
//             load_mtd(employee, points);
//         }
//     });

//     function load_mtd(employee, points){

//         frappe.call({
//             method:"teampro.teampro.page.employee_target_moni.employee_target_monitor.get_mtd_data",
//             args:{employee:employee},
//             callback:function(res){

//                 let rows = res.message || [];

//                 let html = `
//                 <h3>MONTH</h3>

//                 <div class="target-card">
//                 <table class="target-table">

//                     <tr>
//                         <th>Month</th>
//                         <th>Target</th>
//                         <th>Achieved</th>
//                         <th>YTA</th>
//                         <th>SR%</th>
//                     </tr>
//                 `;

//                 rows.forEach(d=>{

//                     let ct = d.ct || 0;
//                     let ach = d.achieved || 0;
//                     let yta = d.ct_yta || 0;

//                     let sr = ct ? ((ach / ct) * 100) : 0;

//                     html += `
//                     <tr>
//                         <td class="label-cell">${d.month}</td>
//                         <td class="value-cell">
//                             <span class="year-point">${(ct/points).toFixed(2)}</span>
//                             (
//                             <span class="year-value">₹ ${formatCompactINR(ct)}</span>
//                             )
//                         </td>
//                         <td class="value-cell">
//                             <span class="year-point">${(ach/points).toFixed(2)}</span>
//                             (
//                             <span class="year-value">₹ ${formatCompactINR(ach)}</span>
//                             )
//                         </td>
                       
//                         <td class="value-cell">
//                             <span class="year-point">${(yta/points).toFixed(2)}</span>
//                             (
//                             <span class="year-value">₹ ${formatCompactINR(yta)}</span>
//                             )
//                         </td>
                        
//                         <td class="value-cell">${sr.toFixed(1)}%</td>
                       
//                     </tr>
//                     `;
//                 });

//                 html += `</table></div>`;

//                 $("#employee_detail_section").append(html);
//             }
//         });
//     }
// }
function show_employee_details(employee, wrapper){

    wrapper.html("<h4>Loading...</h4>");

    let style = `
    <style>

    .dual-table-wrapper{
        display:flex;
        gap:15px;
        margin-top:10px;
    }

    .half-card{
        width:50%;
        background:#f7f9fc;
        padding:12px;
        border-radius:12px;
        box-shadow:0 3px 10px rgba(0,0,0,0.06);
    }

    .half-card h4{
        text-align:center;
        margin-bottom:10px;
        color:#333;
    }

    .target-table{
        width:100%;
        border-collapse:collapse;
        font-size:12px;
    }

    .target-table th{
        background:#0d2f6b;
        color:#fff;
        padding:8px;
        text-align:center;
    }

    .target-table td{
        padding:8px;
        border-bottom:1px solid #eee;
        text-align:center;
    }

    /* POINT = GREEN */
    .year-point{
        color:#1b5e20;
        font-weight:600;
    }

    /* VALUE = BLUE */
    .year-value{
        color:#1565c0;
        font-size:11px;
    }

    </style>
    `;

    wrapper.html(style);

    // ===== YTD =====
    frappe.call({
        method:"teampro.teampro.page.employee_target_moni.employee_target_monitor.get_company_points",
        args:{employee:employee},
        callback:function(r){

            let data = r.message || {};

            let tot_ct = data.total_ct || 0;
            let tot_ach = data.total_ach || 0;
            let points = data.point_value || 1;

            let yta = tot_ct - tot_ach;
            let sr = tot_ct ? ((tot_ach/tot_ct)*100) : 0;

            // ===== MTD CALL =====
            frappe.call({
                method:"teampro.teampro.page.employee_target_moni.employee_target_monitor.get_mtd_data",
                args:{employee:employee},
                callback:function(res){

                    let rows = res.message || [];

                    let html = `
                    <div class="dual-table-wrapper">

                        <!-- YEAR -->
                        <div class="half-card">
                            <h4>YEAR</h4>
                            <table class="target-table">
                                <tr>
                                    <th>Target</th>
                                    <th>Achieved</th>
                                    <th>YTA</th>
                                    <th>SR%</th>
                                </tr>

                                <tr>
                                    <td>
    <span class="year-point">
        ${(tot_ct/points).toFixed(2)} 
        (<span class="year-value">₹ ${formatCompactINR(tot_ct)}</span>)
    </span>
</td>

<td>
    <span class="year-point">
        ${(tot_ach/points).toFixed(2)} 
        (<span class="year-value">₹ ${formatCompactINR(tot_ach)}</span>)
    </span>
</td>

<td>
    <span class="year-point">
        ${(yta/points).toFixed(2)} 
        (<span class="year-value">₹ ${formatCompactINR(yta)}</span>)
    </span>
</td>
<td>${sr.toFixed(1)}%</td>
                                </tr>
                            </table>
                        </div>

                        <!-- MONTH -->
                        <div class="half-card">
                            <h4>MONTH</h4>
                            <table class="target-table">
                                <tr>
                                    <th>Month</th>
                                    <th>Target</th>
                                    <th>Achieved</th>
                                    <th>YTA</th>
                                    <th>SR%</th>
                                </tr>

                                ${rows.map(d => {

                                    let ct = d.ct || 0;
                                    let ach = d.achieved || 0;
                                    let yta = d.ct_yta || 0;
                                    let sr = ct ? ((ach / ct) * 100) : 0;

                                    return `
                                    <tr>
                                        <td>${d.month}</td>

                                        <td>
    <span class="year-point">
        ${(ct/points).toFixed(2)} 
        (<span class="year-value">₹ ${formatCompactINR(ct)}</span>)
    </span>
</td>

<td>
    <span class="year-point">
        ${(ach/points).toFixed(2)} 
        (<span class="year-value">₹ ${formatCompactINR(ach)}</span>)
    </span>
</td>

<td>
    <span class="year-point">
        ${(yta/points).toFixed(2)} 
        (<span class="year-value">₹ ${formatCompactINR(yta)}</span>)
    </span>
</td>

                                        <td>${sr.toFixed(1)}%</td>
                                    </tr>`;
                                }).join("")}

                            </table>
                        </div>

                    </div>
                    `;

                    wrapper.html(style + html);
                }
            });
        }
    });
}
};
function formatCompactINR(val){
	val = val || 0;

	if(val >= 10000000){ // Crore
		return (val / 10000000).toFixed(1).replace(/\.0$/,'') + "Cr";
	}
	else if(val >= 100000){ // Lakh
		return (val / 100000).toFixed(1).replace(/\.0$/,'') + "L";
	}
	else if(val >= 1000){ // Thousand
		return (val / 1000).toFixed(1).replace(/\.0$/,'') + "K";
	}
	else{
		return val.toString();
	}
}