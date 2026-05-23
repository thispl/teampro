// frappe.pages['appraisal-dashboard'].on_page_load = function(wrapper) {

// 	let page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		single_column: true
// 	});

// 	let start = frappe.datetime.month_start();
// 	let end = frappe.datetime.month_end();

// 	$(`<style>
// 		#current-date-time {
//     display:inline-block;
//     background:#1976d2;
//     color:white;
//     padding:6px 18px;
//     border-radius:25px;
//     font-weight:600;
//     font-size:16px;
//     box-shadow:0 4px 15px rgba(0,0,0,0.2);
//     margin-top:8px;
// }

// #current-date-time .date{
//     display:block;
//     font-size:16px;
// }

// #current-date-time .time{
//     display:block;
//     font-size:18px;
//     font-weight:700;
// }
// 	.matrix-title{
// 		text-align:center;
// 		font-size:22px;
// 		font-weight:700;
// 		margin-bottom:20px;
// 	}

// 	.matrix-wrapper{
// 		display:flex;
// 		align-items:center;
// 		justify-content:center;
// 		margin-top:30px;
// 	}

// 	.y-axis{
// 		writing-mode:vertical-rl;
// 		transform:rotate(180deg);
// 		font-weight:700;
// 		margin-right:20px;
// 		font-size:16px;
// 	}

// 	.grid-container{
// 		display:flex;
// 		flex-direction:column;
// 	}

// 	.nine-grid{
// 		display:grid;
// 		grid-template-columns:repeat(3,220px);
// 		grid-template-rows:repeat(3,160px);
// 	}

// 	.box{
// 		border-radius:12px;
// 		color:white;
// 		padding:12px;
// 		position:relative;
// 		cursor:pointer;
// 		transition:all .3s ease;
// 		font-weight:600;
// 		border:3px solid white;
// 	}

// 	.box:hover{
// 		transform:scale(1.06);
// 		box-shadow:0 12px 25px rgba(0,0,0,0.25);
// 	}

// 	.count{
// 		position:absolute;
// 		top:8px;
// 		right:10px;
// 		background:white;
// 		color:black;
// 		border-radius:50%;
// 		width:30px;
// 		height:30px;
// 		text-align:center;
// 		line-height:30px;
// 		font-weight:bold;
// 	}

// 	.box1{background:#1976d2;}
// 	.box2{background:#ef5350;}
// 	.box3{background:#2ecc71;}

// 	.box4{background:#fb8c00;}
// 	.box5{background:#42a5f5;}
// 	.box6{background:#ff5252;}

// 	.box7{background:#546e7a;}
// 	.box8{background:#ffa726;}
// 	.box9{background:#1e88e5;}

// 	.x-axis{
// 		display:grid;
// 		grid-template-columns:repeat(3,220px);
// 		margin-top:10px;
// 		text-align:center;
// 		font-weight:700;
// 	}

// 	.chart-section{
// 		margin:60px auto;
// 		width:1000px;
// 	}

// 	.chart-flex{
// 		display:flex;
// 		gap:40px;
// 		align-items:center;
// 		justify-content:center;
// 	}

// 	.chart-left{
// 		width:700px;
// 	}

// 	.chart-legend{
// 		display:flex;
// 		flex-direction:column;
// 		gap:12px;
// 		font-weight:600;
// 	}

// 	.legend-item{
// 		display:flex;
// 		align-items:center;
// 		gap:10px;
// 	}

// 	.legend-color{
// 		width:18px;
// 		height:18px;
// 		border-radius:3px;
// 		display:inline-block;
// 	}

// 	.poor{background:#ef5350;}
// 	.acceptable{background:#f4b67a;}
// 	.good{background:#f4ef88;}
// 	.verygood{background:#9be084;}
// 	.excellent{background:#5cc46b;}

// 	/* KPI CARDS */
// 	.kpi-container{
// 		display:flex;
// 		justify-content:center;
// 		gap:25px;
// 		margin-bottom:25px;
// 		flex-wrap:wrap;
// 	}

// 	.kpi-card{
// 		color:white;
// 		padding:18px 28px;
// 		border-radius:14px;
// 		min-width:210px;
// 		text-align:center;
// 		box-shadow:0 10px 20px rgba(0,0,0,0.2);
// 		transition:all .35s ease;
// 		position:relative;
// 		overflow:hidden;
// 	}

// 	.kpi-card:nth-child(1){background:linear-gradient(120deg,#667eea,#764ba2);}
// 	.kpi-card:nth-child(2){background:linear-gradient(120deg,#43cea2,#185a9d);}
// 	.kpi-card:nth-child(3){background:linear-gradient(120deg,#f7971e,#ffd200);}
// 	.kpi-card:nth-child(4){background:linear-gradient(120deg,#ff512f,#dd2476);}

// 	.kpi-card:hover{
// 		transform:translateY(-6px) scale(1.03);
// 		box-shadow:0 12px 25px rgba(0,0,0,0.25);
// 	}
// 	.kpi-value{
// 		font-size:28px;
// 		font-weight:700;
// 	}

// 	.kpi-title{
// 		font-size:14px;
// 		opacity:0.9;
// 	}

// 	/* DASHBOARD HEADER */
// 	.dashboard-header{
// 		text-align:center;
// 		margin-bottom:5px;
// 		padding:25px;
// 		border-radius:12px;
// 		color:#333;
// 	}

// 	.dash-title{
// 		font-size:26px;
// 		font-weight:700;
// 	}

// 	.dash-sub{
// 		font-size:16px;
// 		opacity:0.9;
// 		margin-top:5px;
// 	}
// 	</style>`).appendTo("head");
	
// 	$(page.body).html(`
// 	<div class="dashboard-header">
// 		<div class="dash-title">Employee Performance & Potential Analytics</div>
// 	</div>

// 	<div class="kpi-container">

// 		<div class="kpi-card">
// 			<div class="kpi-value" id="total_emp">0</div>
// 			<div class="kpi-title">Employees Appraised</div>
// 		</div>

// 		<div class="kpi-card">
// 			<div class="kpi-value" id="avg_score">0</div>
// 			<div class="kpi-title">Average Score</div>
// 		</div>

// 		<div class="kpi-card">
// 			<div class="kpi-value" id="top_perf">0</div>
// 			<div class="kpi-title">Top Performers</div>
// 		</div>

// 		<div class="kpi-card">
// 			<div class="kpi-value" id="low_perf">0</div>
// 			<div class="kpi-title">Low Performers</div>
// 		</div>

// 	</div>

// 	<div class="matrix-wrapper">

// 		<div class="y-axis">Leadership Potential</div>

// 		<div class="grid-container">

// 			<div class="nine-grid">
// 				<div class="box box1" id="box1">1C<br>Poor Performance<br>High Potential<div class="count">0</div></div>
// 				<div class="box box2" id="box2">1B<br>Good Performance<br>High Potential<div class="count">0</div></div>
// 				<div class="box box3" id="box3">1A<br>Outstanding Performance<br>High Potential<div class="count">0</div></div>

// 				<div class="box box4" id="box4">2C<br>Poor Performance<br>Moderate Potential<div class="count">0</div></div>
// 				<div class="box box5" id="box5">2B<br>Good Performance<br>Moderate Potential<div class="count">0</div></div>
// 				<div class="box box6" id="box6">2A<br>Outstanding Performance<br>Moderate Potential<div class="count">0</div></div>

// 				<div class="box box7" id="box7">3C<br>Poor Performance<br>Limited Potential<div class="count">0</div></div>
// 				<div class="box box8" id="box8">3B<br>Good Performance<br>Limited Potential<div class="count">0</div></div>
// 				<div class="box box9" id="box9">3A<br>Outstanding Performance<br>Limited Potential<div class="count">0</div></div>
// 			</div>

// 			<div class="x-axis">
// 				<div>Poor</div>
// 				<div>Good</div>
// 				<div>Outstanding</div>
// 			</div>

// 			<div style="text-align:center;font-weight:700;margin-top:5px">
// 				Performance
// 			</div>

// 		</div>
// 	</div>

// 	<div class="chart-section">
// 		<h3 style="text-align:center">Performance Rating Bell Distribution</h3>

// 		<div class="chart-flex">
// 			<div class="chart-left">
// 				<canvas id="bellCurveChart"></canvas>
// 			</div>

// 			<div class="chart-legend">
// 				<div class="legend-item"><span class="legend-color poor"></span>Poor</div>
// 				<div class="legend-item"><span class="legend-color acceptable"></span>Acceptable</div>
// 				<div class="legend-item"><span class="legend-color good"></span>Good</div>
// 				<div class="legend-item"><span class="legend-color verygood"></span>Very Good</div>
// 				<div class="legend-item"><span class="legend-color excellent"></span>Excellent</div>
// 			</div>
// 		</div>
		
// 	</div>
	
	
// 	`);

	
// 	frappe.call({
// 		method:"frappe.client.get_list",
// 		args:{
// 			doctype:"Appraisal",
// 			fields:["employee","employee_name","total_score","creation"],
// 			filters:[
// 				["creation","between",[start,end]]
// 			],
// 			limit_page_length:1000
// 		},

// 		callback:function(r){
// 			let data=r.message || [];
// 			let scores=data.map(d=>parseFloat(d.total_score)||0);
// 			let ranges=[
// 				{label:"Poor",min:0,max:2},
// 				{label:"Acceptable",min:2,max:2.75},
// 				{label:"Good",min:2.75,max:3.5},
// 				{label:"Very Good",min:3.5,max:4.25},
// 				{label:"Excellent",min:4.25,max:5}
// 			];

// 			let counts=[0,0,0,0,0];
// 			scores.forEach(score=>{
// 				ranges.forEach((r,i)=>{
// 					if(score>=r.min && score<r.max){
// 						counts[i]++;
// 					}
// 				});
// 			});

// 			let total=scores.length;
// 			let avg_score = total ? (scores.reduce((a,b)=>a+b,0)/total).toFixed(2) : 0;

// 			$("#total_emp").text(total);
// 			$("#avg_score").text(avg_score);
// 			$("#top_perf").text(counts[4]);
// 			$("#low_perf").text(counts[0]);
// 			let percentages=counts.map(c => total ? ((c/total)*100).toFixed(1) : 0);

// 			let boxData={ box1:[], box2:[], box3:[], box4:[], box5:[], box6:[], box7:[], box8:[], box9:[] };

// 			data.forEach(emp=>{
// 				let score=parseFloat(emp.total_score)||0;
// 				let performance = score<2.5 ? "poor" : score<3.5 ? "good" : "outstanding";
// 				let potential = score<2.5 ? "low" : score<3.5 ? "moderate" : "high";
// 				let box="";
// 				if(performance=="poor" && potential=="high") box="box1";
// 				else if(performance=="good" && potential=="high") box="box2";
// 				else if(performance=="outstanding" && potential=="high") box="box3";
// 				else if(performance=="poor" && potential=="moderate") box="box4";
// 				else if(performance=="good" && potential=="moderate") box="box5";
// 				else if(performance=="outstanding" && potential=="moderate") box="box6";
// 				else if(performance=="poor" && potential=="low") box="box7";
// 				else if(performance=="good" && potential=="low") box="box8";
// 				else if(performance=="outstanding" && potential=="low") box="box9";

// 				if(box) boxData[box].push(emp.employee);
// 			});

// 			Object.keys(boxData).forEach(box=>{
// 				let employees = boxData[box];
// 				$(`#${box} .count`).text(employees.length);
// 				$(`#${box}`).off("click").on("click", function(){
// 					if(!employees.length){
// 						frappe.msgprint("No Employees in this category");
// 						return;
// 					}
// 					frappe.set_route("List","Appraisal",{
// 						employee:["in",employees],
// 						creation:["between",[start,end]]
// 					});
// 				});
// 			});

// 			frappe.require("https://cdn.jsdelivr.net/npm/chart.js", function () {
// 				const ctx = document.getElementById("bellCurveChart");
// 				const colors=["#ef5350","#f4b67a","#f4ef88","#9be084","#5cc46b"];
// 				const labelsText=["Poor","Acceptable","Good","Very Good","Excellent"];

// 				function gaussian(x,mean,sigma){ return Math.exp(-0.5*Math.pow((x-mean)/sigma,2)); }

// 				let points=[], labels=[];
// 				for(let x=-3;x<=3;x+=0.1){ points.push(gaussian(x,0,1)); labels.push(x.toFixed(1)); }

// 				const bellPlugin={
// 					id:"bellPlugin",
// 					afterDatasetsDraw(chart){
// 						const {ctx,chartArea:{left,right,top,bottom,width,height}}=chart;
// 						const meta=chart.getDatasetMeta(0);
// 						ctx.save();
// 						ctx.beginPath();
// 						meta.data.forEach((p,i)=>{const {x,y}=p.getProps(['x','y'],true); i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);});
// 						ctx.lineTo(right,bottom); ctx.lineTo(left,bottom); ctx.closePath();
// 						ctx.clip();

// 						let sectionWidth=width/5;
// 						for(let i=0;i<5;i++){ ctx.fillStyle=colors[i]; ctx.globalAlpha=0.85; ctx.fillRect(left+(sectionWidth*i),top,sectionWidth,height);}
// 						ctx.restore();

// 						ctx.save(); ctx.textAlign="center"; ctx.fillStyle="#000";
// 						for(let i=0;i<5;i++){
// 							let xPos=left+(sectionWidth*i)+(sectionWidth/2);
// 							ctx.font="bold 16px Arial"; ctx.fillText(percentages[i]+"%",xPos,top+30);
// 							ctx.font="14px Arial"; ctx.fillText(labelsText[i],xPos,bottom-35);
// 							ctx.fillText("(n="+counts[i]+")",xPos,bottom-18);
// 						}
// 						ctx.restore();
// 					}
// 				};

// 				new Chart(ctx,{
// 					type:"line",
// 					data:{labels:labels,datasets:[{data:points,borderColor:"#000",borderWidth:3,pointRadius:0,tension:0.45}]},
// 					options:{
// 						responsive:true,
// 						animation:{duration:1800,easing:"easeOutQuart"},
// 						interaction:{mode:"nearest",intersect:false},
// 						plugins:{
// 							legend:{display:false},
// 							tooltip:{callbacks:{label:function(context){let index=context.dataIndex; let section=Math.floor(index/(points.length/5)); return section<5? labelsText[section]+": "+counts[section]+" Employees ("+percentages[section]+"%)":"";}}}
// 						},
// 						scales:{y:{display:false},x:{grid:{borderDash:[5,5]},ticks:{callback:function(v,i){let map={0:"-3",10:"-1.5 SD",20:"-0.5 SD",30:"Mean",40:"+0.5 SD",50:"+1.5 SD",60:"+3"}; return map[i]||"";}}}}
// 					},
// 					plugins:[bellPlugin]
// 				});
// 			});
// 		}
// 	});
// 	frappe.call({
//     method: "frappe.client.get_list",
//     args: {
//         doctype: "Appraisal",
//         fields: ["name", "employee", "employee_name", "total_score", "department", "docstatus", "creation"],
//         filters: [["creation", "between", [start, end]]],
//         limit_page_length: 1000
//     },
//     callback: function(r) {
//         let data = r.message || [];
//         let tableData = {};

//         data.forEach(d => {
//             let dept = d.department || "Unknown";
//             if(!tableData[dept]) {
//                 tableData[dept] = {total:0, completed:0, pending:0};
//             }
//             tableData[dept].total += 1;
//             if(d.docstatus === 1) tableData[dept].completed += 1;
//             else tableData[dept].pending += 1;
//         });

//         let currentYear = new Date().getFullYear();
//         let totalAll = {total:0, completed:0, pending:0};

//         // Container flex
//         let html = `<div style="display:flex; gap:30px; justify-content:center; flex-wrap:wrap; margin:40px auto; max-width:1200px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">`;

//         // Table Section
//         let tableHTML = `
//         <div style="flex:1 1 600px; overflow-x:auto; border-radius:10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding:20px;">
//             <div style="text-align:center;margin-bottom:20px;">
//                 <h2 style="color:#2E86C1;">${currentYear} Staff Performance Appraisal Status %</h2>
//             </div>
//             <table class="table" style="width:100%; border-collapse:separate; border-spacing:0; text-align:center;">
//                 <thead style="background:#2E86C1; color:white; font-weight:600;">
//                     <tr>
//                         <th style="padding:12px;">Unit</th>
//                         <th>Total Appraisals Due</th>
//                         <th>Completed (Approved)</th>
//                         <th>Pending (Appraiser)</th>
//                         <th>Appraisals Completed %</th>
//                         <th>Appraisals Pending %</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//         `;

//         Object.keys(tableData).forEach(dept => {
//             let d = tableData[dept];
//             totalAll.total += d.total;
//             totalAll.completed += d.completed;
//             totalAll.pending += d.pending;

//             let completedPct = d.total ? ((d.completed/d.total)*100).toFixed(0) : 0;
//             let pendingPct = d.total ? ((d.pending/d.total)*100).toFixed(0) : 0;

//             tableHTML += `
//                 <tr style="transition: background 0.3s; cursor:pointer;" onmouseover="this.style.background='#f0f8ff'" onmouseout="this.style.background='white'">
//                     <td style="padding:10px;white-space:nowrap;text-align:left;">${dept}</td>
//                     <td>${d.total}</td>
//                     <td><span style="padding:4px 10px; border-radius:12px; background:#28a745; color:white;">${d.completed}</span></td>
//                     <td><span style="padding:4px 10px; border-radius:12px; background:#ffc107; color:#212529;">${d.pending}</span></td>
//                     <td>${completedPct}%</td>
//                     <td>${pendingPct}%</td>
//                 </tr>
//             `;
//         });

//         let totalCompletedPct = totalAll.total ? ((totalAll.completed/totalAll.total)*100).toFixed(0) : 0;
//         let totalPendingPct = totalAll.total ? ((totalAll.pending/totalAll.total)*100).toFixed(0) : 0;

//         tableHTML += `
//             <tr style="font-weight:700; background:#eaf2f8;">
//                 <td style="padding:10px;">Total</td>
//                 <td>${totalAll.total}</td>
//                 <td><span style="padding:4px 10px; border-radius:12px; background:#28a745; color:white;">${totalAll.completed}</span></td>
//                 <td><span style="padding:4px 10px; border-radius:12px; background:#ffc107; color:#212529;">${totalAll.pending}</span></td>
//                 <td>${totalCompletedPct}%</td>
//                 <td>${totalPendingPct}%</td>
//             </tr>
//         `;

//         tableHTML += `</tbody></table></div>`;

//         // Donut Chart Section
//         let chartHTML = `
//         <div style="flex:0 0 400px; text-align:center; padding:20px;">
//             <h3 style="color:#2E86C1; margin-bottom:65px;">Appraisal Completion Status</h3>
//             <canvas id="completionDonutChart" width="400" height="400"></canvas>
//         </div>
//         `;

//         html += tableHTML + chartHTML;
//         html += `</div>`;

//         $(page.body).append(html);

//        frappe.require(["https://cdn.jsdelivr.net/npm/chart.js"], function () {
//     const ctxDonut = document.getElementById('completionDonutChart');

//     const total = totalAll.completed + totalAll.pending;

//     const dataValues = [totalAll.completed, totalAll.pending];
//     const colors = ['#28a745', '#ffc107'];

//     const completionDonut = new Chart(ctxDonut, {
//         type: 'doughnut',
//         data: {
//             labels: ['Completed', 'Pending'],
//             datasets: [{
//                 data: dataValues,
//                 backgroundColor: colors,
//                 borderColor: ['#ffffff', '#ffffff'],
//                 borderWidth: 2
//             }]
//         },
//         options: {
//             responsive: true,
//             plugins: {
//                 legend: { position: 'bottom', labels: { font: { size: 14 }, padding: 20 } },
//                 tooltip: {
//                     callbacks: {
//                         label: function(context) {
//                             let value = context.raw;
//                             let pct = total ? ((value / total) * 100).toFixed(1) : 0;
//                             return context.label + ': ' + value + ' (' + pct + '%)';
//                         }
//                     }
//                 }
//             },
//             cutout: '60%'
//         },
//         plugins: [{
//     id: 'slicePercentage',
//     afterDraw(chart) {
//         const {ctx} = chart;
//         const dataset = chart.data.datasets[0];
//         const meta = chart.getDatasetMeta(0);
//         const total = dataset.data.reduce((a,b)=>a+b,0);

//         ctx.save();
//         ctx.font = 'bold 16px Arial';
//         ctx.fillStyle = '#000'; 
//         ctx.textAlign = 'center';
//         ctx.textBaseline = 'middle';

//         meta.data.forEach((arc, index) => {
//             const value = dataset.data[index];
//             const pct = total ? ((value / total) * 100).toFixed(1) + '%' : '0%';
//             const radiusOffset = 20;
//             const angle = (arc.startAngle + arc.endAngle) / 2;
//             const x = arc.x + Math.cos(angle) * (arc.outerRadius - radiusOffset);
//             const y = arc.y + Math.sin(angle) * (arc.outerRadius - radiusOffset);
//             ctx.fillText(pct, x, y); // always black
//         });

//         ctx.restore();
//     }
// }]
//     });
// });
//     }
// });
	
// };


frappe.pages['appraisal-dashboard'].on_page_load = function(wrapper) {

	let page = frappe.ui.make_app_page({
		parent: wrapper,
		single_column: true
	});

	let start = frappe.datetime.month_start();
	let end = frappe.datetime.month_end();

	$(`<style>
		
		#current-date-time {
    display:inline-block;
    background:#1976d2;
    color:white;
    padding:6px 18px;
    border-radius:25px;
    font-weight:600;
    font-size:16px;
    box-shadow:0 4px 15px rgba(0,0,0,0.2);
    margin-top:8px;
}

#current-date-time .date{
    display:block;
    font-size:16px;
}

#current-date-time .time{
    display:block;
    font-size:18px;
    font-weight:700;
}
	.matrix-title{
		text-align:center;
		font-size:22px;
		font-weight:700;
		margin-bottom:20px;
	}

	.matrix-wrapper{
		display:flex;
		align-items:center;
		justify-content:center;
		margin-top:30px;
	}

	.y-axis{
		writing-mode:vertical-rl;
		transform:rotate(180deg);
		font-weight:700;
		margin-right:20px;
		font-size:16px;
	}

	.grid-container{
		display:flex;
		flex-direction:column;
	}

	.nine-grid{
		display:grid;
		grid-template-columns:repeat(3,220px);
		grid-template-rows:repeat(3,160px);
	}

	.box{
		border-radius:12px;
		color:white;
		padding:12px;
		position:relative;
		cursor:pointer;
		transition:all .3s ease;
		font-weight:600;
		border:3px solid white;
	}

	.box:hover{
		transform:scale(1.06);
		box-shadow:0 12px 25px rgba(0,0,0,0.25);
	}

	.count{
		position:absolute;
		top:8px;
		right:10px;
		background:white;
		color:black;
		border-radius:50%;
		width:30px;
		height:30px;
		text-align:center;
		line-height:30px;
		font-weight:bold;
	}

	.box1{background:#1976d2;}
	.box2{background:#ef5350;}
	.box3{background:#2ecc71;}

	.box4{background:#fb8c00;}
	.box5{background:#42a5f5;}
	.box6{background:#ff5252;}

	.box7{background:#546e7a;}
	.box8{background:#ffa726;}
	.box9{background:#1e88e5;}

	.x-axis{
		display:grid;
		grid-template-columns:repeat(3,220px);
		margin-top:10px;
		text-align:center;
		font-weight:700;
	}

	.chart-section{
		margin:60px auto;
		width:1000px;
	}

	.chart-flex{
		display:flex;
		gap:40px;
		align-items:center;
		justify-content:center;
	}

	.chart-left{
		width:700px;
	}

	.chart-legend{
		display:flex;
		flex-direction:column;
		gap:12px;
		font-weight:600;
	}

	.legend-item{
		display:flex;
		align-items:center;
		gap:10px;
	}

	.legend-color{
		width:18px;
		height:18px;
		border-radius:3px;
		display:inline-block;
	}

	.poor{background:#ef5350;}
	.acceptable{background:#f4b67a;}
	.good{background:#f4ef88;}
	.verygood{background:#9be084;}
	.excellent{background:#5cc46b;}

	/* KPI CARDS */
	.kpi-container{
		display:flex;
		justify-content:center;
		gap:25px;
		margin-bottom:25px;
		flex-wrap:wrap;
	}

	.kpi-card{
		color:white;
		padding:18px 28px;
		border-radius:14px;
		min-width:210px;
		text-align:center;
		box-shadow:0 10px 20px rgba(0,0,0,0.2);
		transition:all .35s ease;
		position:relative;
		overflow:hidden;
	}

	.kpi-card:nth-child(1){background:linear-gradient(120deg,#667eea,#764ba2);}
	.kpi-card:nth-child(2){background:linear-gradient(120deg,#43cea2,#185a9d);}
	.kpi-card:nth-child(3){background:linear-gradient(120deg,#f7971e,#ffd200);}
	.kpi-card:nth-child(4){background:linear-gradient(120deg,#ff512f,#dd2476);}

	.kpi-card:hover{
		transform:translateY(-6px) scale(1.03);
		box-shadow:0 12px 25px rgba(0,0,0,0.25);
	}
	.kpi-value{
		font-size:28px;
		font-weight:700;
	}

	.kpi-title{
		font-size:14px;
		opacity:0.9;
	}

	/* DASHBOARD HEADER */
	.dashboard-header{
		text-align:center;
		margin-bottom:5px;
		padding:25px;
		border-radius:12px;
		color:#333;
	}

	.dash-title{
		font-size:26px;
		font-weight:700;
	}

	.dash-sub{
		font-size:16px;
		opacity:0.9;
		margin-top:5px;
	}
	</style>`).appendTo("head");
	
	$(page.body).html(`
	<div class="dashboard-header">
		<div class="dash-title">Employee Performance & Potential Analytics</div>
	</div>

	<div class="kpi-container">

		<div class="kpi-card">
			<div class="kpi-value" id="total_emp">0</div>
			<div class="kpi-title">Employees Appraised</div>
		</div>

		<div class="kpi-card">
			<div class="kpi-value" id="avg_score">0</div>
			<div class="kpi-title">Average Score</div>
		</div>

		<div class="kpi-card">
			<div class="kpi-value" id="top_perf">0</div>
			<div class="kpi-title">Top Performers</div>
		</div>

		<div class="kpi-card">
			<div class="kpi-value" id="low_perf">0</div>
			<div class="kpi-title">Low Performers</div>
		</div>

	</div>

	
	
	
	`);

	frappe.call({
    method: "frappe.client.get_list",
    args: {
        doctype: "Appraisal",
        fields: ["name", "employee", "employee_name", "total_score", "department", "docstatus", "creation"],
        filters: [["creation", "between", [start, end]]],
        limit_page_length: 1000
    },
    callback: function(r) {
        let data = r.message || [];
        let tableData = {};

        data.forEach(d => {
            let dept = d.department || "Unknown";
            if(!tableData[dept]) {
                tableData[dept] = {total:0, completed:0, pending:0};
            }
            tableData[dept].total += 1;
            if(d.docstatus === 1) tableData[dept].completed += 1;
            else tableData[dept].pending += 1;
        });

        let currentYear = new Date().getFullYear();
        let totalAll = {total:0, completed:0, pending:0};

        // Container flex
        let html = `<div style="display:flex; gap:30px; justify-content:center; flex-wrap:wrap; margin:40px auto; max-width:1200px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">`;

        // Table Section
        let tableHTML = `
        <div style="flex:1 1 600px; overflow-x:auto; border-radius:10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding:20px;">
            <div style="text-align:center;margin-bottom:20px;">
                <h2 style="color:#2E86C1;">${currentYear} Staff Performance Appraisal Status %</h2>
            </div>
            <table class="table" style="width:100%; border-collapse:separate; border-spacing:0; text-align:center;">
                <thead style="background:#2E86C1; color:white; font-weight:600;">
                    <tr>
                        <th style="padding:12px;">Unit</th>
                        <th>Total Appraisals Due</th>
                        <th>Completed (Approved)</th>
                        <th>Pending (Appraiser)</th>
                        <th>Appraisals Completed %</th>
                        <th>Appraisals Pending %</th>
                    </tr>
                </thead>
                <tbody>
        `;

        Object.keys(tableData).forEach(dept => {
            let d = tableData[dept];
            totalAll.total += d.total;
            totalAll.completed += d.completed;
            totalAll.pending += d.pending;

            let completedPct = d.total ? ((d.completed/d.total)*100).toFixed(0) : 0;
            let pendingPct = d.total ? ((d.pending/d.total)*100).toFixed(0) : 0;

            tableHTML += `
                <tr style="transition: background 0.3s; cursor:pointer;" onmouseover="this.style.background='#f0f8ff'" onmouseout="this.style.background='white'">
                    <td style="padding:10px;white-space:nowrap;text-align:left;">${dept}</td>
                    <td>${d.total}</td>
                    <td><span style="padding:4px 10px; border-radius:12px; background:#28a745; color:white;">${d.completed}</span></td>
                    <td><span style="padding:4px 10px; border-radius:12px; background:#ffc107; color:#212529;">${d.pending}</span></td>
                    <td>${completedPct}%</td>
                    <td>${pendingPct}%</td>
                </tr>
            `;
        });

        let totalCompletedPct = totalAll.total ? ((totalAll.completed/totalAll.total)*100).toFixed(0) : 0;
        let totalPendingPct = totalAll.total ? ((totalAll.pending/totalAll.total)*100).toFixed(0) : 0;

        tableHTML += `
            <tr style="font-weight:700; background:#eaf2f8;">
                <td style="padding:10px;">Total</td>
                <td>${totalAll.total}</td>
                <td><span style="padding:4px 10px; border-radius:12px; background:#28a745; color:white;">${totalAll.completed}</span></td>
                <td><span style="padding:4px 10px; border-radius:12px; background:#ffc107; color:#212529;">${totalAll.pending}</span></td>
                <td>${totalCompletedPct}%</td>
                <td>${totalPendingPct}%</td>
            </tr>
        `;

        tableHTML += `</tbody></table></div>`;

        // Donut Chart Section
        let chartHTML = `
        <div style="flex:0 0 400px; text-align:center; padding:20px;">
            <h3 style="color:#2E86C1; margin-bottom:65px;">Appraisal Completion Status</h3>
            <canvas id="completionDonutChart" width="400" height="400"></canvas>
        </div>
        `;

        html += tableHTML + chartHTML;
        html += `</div>`;

        $(page.body).append(html);

       frappe.require(["https://cdn.jsdelivr.net/npm/chart.js"], function () {
    const ctxDonut = document.getElementById('completionDonutChart');

    const total = totalAll.completed + totalAll.pending;

    const dataValues = [totalAll.completed, totalAll.pending];
    const colors = ['#28a745', '#ffc107'];

    const completionDonut = new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
            labels: ['Completed', 'Pending'],
            datasets: [{
                data: dataValues,
                backgroundColor: colors,
                borderColor: ['#ffffff', '#ffffff'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { font: { size: 14 }, padding: 20 } },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let value = context.raw;
                            let pct = total ? ((value / total) * 100).toFixed(1) : 0;
                            return context.label + ': ' + value + ' (' + pct + '%)';
                        }
                    }
                }
            },
            cutout: '60%'
        },
        plugins: [{
    id: 'slicePercentage',
    afterDraw(chart) {
        const {ctx} = chart;
        const dataset = chart.data.datasets[0];
        const meta = chart.getDatasetMeta(0);
        const total = dataset.data.reduce((a,b)=>a+b,0);

        ctx.save();
        ctx.font = 'bold 16px Arial';
        ctx.fillStyle = '#000'; 
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        meta.data.forEach((arc, index) => {
            const value = dataset.data[index];
            const pct = total ? ((value / total) * 100).toFixed(1) + '%' : '0%';
            const radiusOffset = 20;
            const angle = (arc.startAngle + arc.endAngle) / 2;
            const x = arc.x + Math.cos(angle) * (arc.outerRadius - radiusOffset);
            const y = arc.y + Math.sin(angle) * (arc.outerRadius - radiusOffset);
            ctx.fillText(pct, x, y); // always black
        });

        ctx.restore();
    }
}]
    });
});
    }
});
	frappe.call({
		method:"frappe.client.get_list",
		args:{
			doctype:"Appraisal",
			fields:["employee","employee_name","total_score","creation"],
			filters:[
				["creation","between",[start,end]]
			],
			limit_page_length:1000
		},

		callback:function(r){
			// Instead of just $(page.body).append(html);
let bottomSection = `
<div class="matrix-chart-wrapper" style="display:flex; justify-content:center; gap:50px; flex-wrap:wrap; margin-top:50px;">
  <div class="matrix-wrapper"> 
    <div class="y-axis">Leadership Potential</div>
    <div class="grid-container">
      <div class="nine-grid">
        <div class="box box1" id="box1">1C<br>Poor Performance<br>High Potential<div class="count">0</div></div>
        <div class="box box2" id="box2">1B<br>Good Performance<br>High Potential<div class="count">0</div></div>
        <div class="box box3" id="box3">1A<br>Outstanding Performance<br>High Potential<div class="count">0</div></div>
        <div class="box box4" id="box4">2C<br>Poor Performance<br>Moderate Potential<div class="count">0</div></div>
        <div class="box box5" id="box5">2B<br>Good Performance<br>Moderate Potential<div class="count">0</div></div>
        <div class="box box6" id="box6">2A<br>Outstanding Performance<br>Moderate Potential<div class="count">0</div></div>
        <div class="box box7" id="box7">3C<br>Poor Performance<br>Limited Potential<div class="count">0</div></div>
        <div class="box box8" id="box8">3B<br>Good Performance<br>Limited Potential<div class="count">0</div></div>
        <div class="box box9" id="box9">3A<br>Outstanding Performance<br>Limited Potential<div class="count">0</div></div>
      </div>
      <div class="x-axis">
        <div>Poor</div>
        <div>Good</div>
        <div>Outstanding</div>
      </div>
      <div style="text-align:center;font-weight:700;margin-top:5px">Performance</div>
    </div>
  </div>

  <div class="chart-section">
    <h3 style="text-align:center">Performance Rating Bell Distribution</h3>
    <div class="chart-flex">
      <div class="chart-left">
        <canvas id="bellCurveChart"></canvas>
      </div>
      <div class="chart-legend">
        <div class="legend-item"><span class="legend-color poor"></span>Poor</div>
        <div class="legend-item"><span class="legend-color acceptable"></span>Acceptable</div>
        <div class="legend-item"><span class="legend-color good"></span>Good</div>
        <div class="legend-item"><span class="legend-color verygood"></span>Very Good</div>
        <div class="legend-item"><span class="legend-color excellent"></span>Excellent</div>
      </div>
    </div>
  </div>
</div>`;

// Append **after all KPI cards + table/chart**
			let data=r.message || [];
			let scores=data.map(d=>parseFloat(d.total_score)||0);
			let ranges=[
				{label:"Poor",min:0,max:2},
				{label:"Acceptable",min:2,max:2.75},
				{label:"Good",min:2.75,max:3.5},
				{label:"Very Good",min:3.5,max:4.25},
				{label:"Excellent",min:4.25,max:5}
			];

			let counts=[0,0,0,0,0];
			scores.forEach(score=>{
				ranges.forEach((r,i)=>{
					if(score>=r.min && score<r.max){
						counts[i]++;
					}
				});
			});

			let total=scores.length;
			let avg_score = total ? (scores.reduce((a,b)=>a+b,0)/total).toFixed(2) : 0;

			$("#total_emp").text(total);
			$("#avg_score").text(avg_score);
			$("#top_perf").text(counts[4]);
			$("#low_perf").text(counts[0]);
			let percentages=counts.map(c => total ? ((c/total)*100).toFixed(1) : 0);

			let boxData={ box1:[], box2:[], box3:[], box4:[], box5:[], box6:[], box7:[], box8:[], box9:[] };

			data.forEach(emp=>{
				let score=parseFloat(emp.total_score)||0;
				let performance = score<2.5 ? "poor" : score<3.5 ? "good" : "outstanding";
				let potential = score<2.5 ? "low" : score<3.5 ? "moderate" : "high";
				let box="";
				if(performance=="poor" && potential=="high") box="box1";
				else if(performance=="good" && potential=="high") box="box2";
				else if(performance=="outstanding" && potential=="high") box="box3";
				else if(performance=="poor" && potential=="moderate") box="box4";
				else if(performance=="good" && potential=="moderate") box="box5";
				else if(performance=="outstanding" && potential=="moderate") box="box6";
				else if(performance=="poor" && potential=="low") box="box7";
				else if(performance=="good" && potential=="low") box="box8";
				else if(performance=="outstanding" && potential=="low") box="box9";

				if(box) boxData[box].push(emp.employee);
			});

			Object.keys(boxData).forEach(box=>{
				let employees = boxData[box];
				$(`#${box} .count`).text(employees.length);
				$(`#${box}`).off("click").on("click", function(){
					if(!employees.length){
						frappe.msgprint("No Employees in this category");
						return;
					}
					frappe.set_route("List","Appraisal",{
						employee:["in",employees],
						creation:["between",[start,end]]
					});
				});
			});

			frappe.require("https://cdn.jsdelivr.net/npm/chart.js", function () {
				const ctx = document.getElementById("bellCurveChart");
				const colors=["#ef5350","#f4b67a","#f4ef88","#9be084","#5cc46b"];
				const labelsText=["Poor","Acceptable","Good","Very Good","Excellent"];

				function gaussian(x,mean,sigma){ return Math.exp(-0.5*Math.pow((x-mean)/sigma,2)); }

				let points=[], labels=[];
				for(let x=-3;x<=3;x+=0.1){ points.push(gaussian(x,0,1)); labels.push(x.toFixed(1)); }

				const bellPlugin={
					id:"bellPlugin",
					afterDatasetsDraw(chart){
						const {ctx,chartArea:{left,right,top,bottom,width,height}}=chart;
						const meta=chart.getDatasetMeta(0);
						ctx.save();
						ctx.beginPath();
						meta.data.forEach((p,i)=>{const {x,y}=p.getProps(['x','y'],true); i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);});
						ctx.lineTo(right,bottom); ctx.lineTo(left,bottom); ctx.closePath();
						ctx.clip();

						let sectionWidth=width/5;
						for(let i=0;i<5;i++){ ctx.fillStyle=colors[i]; ctx.globalAlpha=0.85; ctx.fillRect(left+(sectionWidth*i),top,sectionWidth,height);}
						ctx.restore();

						ctx.save(); ctx.textAlign="center"; ctx.fillStyle="#000";
						for(let i=0;i<5;i++){
							let xPos=left+(sectionWidth*i)+(sectionWidth/2);
							ctx.font="bold 16px Arial"; ctx.fillText(percentages[i]+"%",xPos,top+30);
							ctx.font="14px Arial"; ctx.fillText(labelsText[i],xPos,bottom-35);
							ctx.fillText("(n="+counts[i]+")",xPos,bottom-18);
						}
						ctx.restore();
					}
				};

				new Chart(ctx,{
					type:"line",
					data:{labels:labels,datasets:[{data:points,borderColor:"#000",borderWidth:3,pointRadius:0,tension:0.45}]},
					options:{
						responsive:true,
						animation:{duration:1800,easing:"easeOutQuart"},
						interaction:{mode:"nearest",intersect:false},
						plugins:{
							legend:{display:false},
							tooltip:{callbacks:{label:function(context){let index=context.dataIndex; let section=Math.floor(index/(points.length/5)); return section<5? labelsText[section]+": "+counts[section]+" Employees ("+percentages[section]+"%)":"";}}}
						},
						scales:{y:{display:false},x:{grid:{borderDash:[5,5]},ticks:{callback:function(v,i){let map={0:"-3",10:"-1.5 SD",20:"-0.5 SD",30:"Mean",40:"+0.5 SD",50:"+1.5 SD",60:"+3"}; return map[i]||"";}}}}
					},
					plugins:[bellPlugin]
				});
			});
$(page.body).append(bottomSection);
			}
	});
	
	
};


