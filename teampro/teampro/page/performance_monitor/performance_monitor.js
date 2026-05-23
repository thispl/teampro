frappe.pages['performance-monitor'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Performance Monitor',
        single_column: true
    });

    $(wrapper).find('.layout-main-section').css({
        "background-color": "rgba(173, 216, 230, 0.2)",
        "backdrop-filter": "blur(6px)",
        "-webkit-backdrop-filter": "blur(6px)",
        "border-radius": "12px",
        "padding": "20px"
    });

    const html = `
    <div style="text-align: center; padding: 10px;">
        <h1 style="text-transform: uppercase; margin: 0; color: #222;font-family: 'Times New Roman', Times, serif; font-size: 32px; font-weight: bold;">PERFORMANCE MONITOR</h1>
        <div id="arrow-loader" style="font-weight: bold; font-size: 20px; color: gold; margin-top: 8px; font-family: monospace;"></div>
        <div id="datetime" style="font-size: 20px; font-weight: bold; margin-top: 5px;"></div>
    </div>
    <hr>

    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <div>
            <label for="emp-name-filter" style="font-weight: bold;">Employee Name:</label><br>
            <select id="emp-name-filter" style="padding: 6px; width: 200px;">
                <option value="">All</option>
            </select>
        </div>
        <div>
            <label for="date-filter" style="font-weight: bold;">Select Date:</label><br>
            <input type="date" id="date-filter" style="padding: 6px; width: 200px;" />
        </div>
    </div>

    <!-- 👇 Department name on top, full width -->
    <div id="department-name" style="text-align: left; font-size: 25px; font-weight: bold; color: #444; margin-bottom: 10px;"></div>

    <!-- 👇 Perfect aligned two-column layout -->
    <div style="display: flex; gap: 20px; align-items: flex-start;">
        <div id="employee-box" style="width: 27%; height: 260px; background-color: #f0f0f0; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: bold; color: #333;"></div>
        <div id="left-table" style="width: 100%;"></div>
        <div id="right-table" style="flex: 1;"></div>
    </div>
`;


    $(wrapper).find('.layout-main-section').html(html);

    let arrowPatterns = ["--", "----", "-------", "----------", "---------------", "-----------------", "----------------------", "------------------------"];
    let arrowIndex = 0;
    setInterval(() => {
        document.getElementById("arrow-loader").textContent = arrowPatterns[arrowIndex];
        arrowIndex = (arrowIndex + 1) % arrowPatterns.length;
    }, 300);

    function updateDateTime() {
        const now = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
        let dateTimeString = now.toLocaleDateString('en-IN', options).replace(',', ' | Time:').replace(/am|pm/i, match => match.toUpperCase());
        document.getElementById('datetime').textContent = `Date: ${dateTimeString}`;
    }
    updateDateTime();
    setInterval(updateDateTime, 1000);

    let departmentData = {};
    let departmentKeys = [];
    let currentDeptIndex = 0;
    let currentEmpIndex = 0;

    frappe.call({
        method: "teampro.teampro.page.performance_monitor.performance_monitor.get_active_employees_by_department",
        callback: function(r) {
            departmentData = r.message;
            departmentKeys = Object.keys(departmentData);

            let employeeNames = new Set();
            Object.values(departmentData).forEach(deptList => {
                deptList.forEach(emp => {
                    employeeNames.add(`${emp.emp_id} - ${emp.emp_name}`);
                });
            });

            const empFilter = document.getElementById('emp-name-filter');
            employeeNames.forEach(name => {
                const opt = document.createElement("option");
                opt.value = name;
                opt.textContent = name;
                empFilter.appendChild(opt);
            });

            document.getElementById("emp-name-filter").addEventListener("change", rotateEmployees);
            document.getElementById("date-filter").addEventListener("change", rotateEmployees);

            rotateEmployees();

            // Auto rotate when All is selected
            setInterval(() => {
                if (document.getElementById("emp-name-filter").value === "") {
                    rotateEmployees();
                }
            }, 1000);
        }
    });

    function rotateEmployees() {
        const selectedName = document.getElementById("emp-name-filter").value;
        if (!selectedName) {
            const currentDept = departmentKeys[currentDeptIndex];
            const employees = departmentData[currentDept];
            const emp = employees[currentEmpIndex];

            document.getElementById("employee-box").innerHTML = `${emp.emp_id} - ${emp.emp_name}`;
            document.getElementById("department-name").textContent = `${currentDept}`;

            renderBasedOnDept(currentDept);

            currentEmpIndex++;
            if (currentEmpIndex >= employees.length) {
                currentEmpIndex = 0;
                currentDeptIndex++;
                if (currentDeptIndex >= departmentKeys.length) {
                    currentDeptIndex = 0;
                }
            }
        } else {
            for (let dept of departmentKeys) {
                const employees = departmentData[dept];
                for (let emp of employees) {
                    const fullName = `${emp.emp_id} - ${emp.emp_name}`;
                    if (fullName === selectedName) {
                        document.getElementById("employee-box").innerHTML = fullName;
                        document.getElementById("department-name").textContent = `${dept}`;
                        renderBasedOnDept(dept);
                        return;
                    }
                }
            }
            document.getElementById("employee-box").innerHTML = "No Matching Employee";
            document.getElementById("department-name").textContent = "-";
            document.getElementById("left-table").innerHTML = "<div style='text-align:center;color:red;font-weight:bold;'>No data for selected filter</div>";
        }
    }

    function renderBasedOnDept(dept) {
        if (["IT. Development - THIS", "Recruitment - THIS", "Finance & Accountant - THIS"].includes(dept)) {
            renderTableFormat1();
        } else if (["R&S - IT Services - THIS","R&S - HR Service - THIS"].includes(dept)) {
            renderTableFormat2();
        } else if (["TFP - Factroy - TFP"].includes(dept)) {
            renderTableFormat3();
        } else if (["BCS - THIS"].includes(dept)) {
            renderTableFormat4();
        } else {
            renderTableFormat5();
        }
    }

function renderTableFormat1() {
    const data = [
        {
            sno: 1,
            task_id: "TS-001",
            status: "In Progress",
            rc_rt: "05-Aug",
            ac_at: "03-May"
        },
        {
            sno: 2,
            task_id: "TS-002",
            status: "In Progress",
            rc_rt: "04-Jun",
            ac_at: "02-Apr"
        },
        // Add more rows here if needed
    ];

    let tableRows = data.map((row, index) => {
        const bgColor = index % 2 === 0 ? '#ffe6f0' : '#e6e6ff';  // Light pink / light violet
        return `
            <tr style="background-color: ${bgColor};">
                <td style="border: 1px solid #fff; padding: 8px; text-align: center;">${row.sno}</td>
                <td style="border: 1px solid #fff; padding: 8px;">${row.task_id}</td>
                <td style="border: 1px solid #fff; padding: 8px;">${row.status}</td>
                <td style="border: 1px solid #fff; padding: 8px;">${row.rc_rt}</td>
                <td style="border: 1px solid #fff; padding: 8px;">${row.ac_at}</td>
                ${index === 0 ? `
                    <td style="border: 1px solid #fff; padding: 8px;" rowspan="${data.length}">
                        <div style="text-align: center; font-weight: bold; color: #444;">
                            SR Yesterday :<br><br><br>
                            SR Today Plan :
                        </div>
                    </td>` : ''}
            </tr>
        `;
    }).join('');

    document.getElementById("left-table").innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <thead>
                <tr style="background-color: #00008B;">
                    <th style="border: 1px solid #fff; padding: 8px; text-align: center; color: #f0f0f0;">S.No</th>
                    <th style="border: 1px solid #fff; padding: 8px; text-align: center; color: #f0f0f0;">Task / Position ID</th>
                    <th style="border: 1px solid #fff; padding: 8px; text-align: center; color: #f0f0f0;">Current Status</th>
                    <th style="border: 1px solid #fff; padding: 8px; text-align: center; color: #f0f0f0;">RC / RT</th>
                    <th style="border: 1px solid #fff; padding: 8px; text-align: center; color: #f0f0f0;">AC / AT</th>
                    <th style="border: 1px solid #fff; padding: 8px; text-align: center; color: #f0f0f0;">SR Remarks</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}




    // Format 2
    function renderTableFormat2() {
    const rows = ["Effective Followup", "Appointment Fixed", "Appointment Taken", "CC/Lead Generated", "SR%"];
    let tableRows = rows.map((row, index) => {
        const bgColor = index % 2 === 0 ? '#ffe6f0' : '#e6e6ff';  // light pink and light violet
        return `
        <tr style="background-color: ${bgColor};">
            <td style="border: 1px solid #fff; padding: 8px; text-align: center;">${index + 1}</td>
            <td style="border: 1px solid #fff; padding: 8px;">${row}</td>
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Today -->
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Yesterday -->
            ${index === 0 ? `<td style="border: 1px solid #fff; padding: 8px;" rowspan="${rows.length}">
            <div style="text-align: center; font-weight: bold; color: #444;">
                            Followup :<br><br><br>
                            Appointment Plan :
                        </div>
            </td>` : ``}
        </tr>
    `}).join('');

    document.getElementById("left-table").innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <thead>
                <tr style="background-color: #00008B;">
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">S.No</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Title</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Today</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Yesterday</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Day Plan</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}


    // Format 3
    function renderTableFormat3() {
    const rows = ["Packing Plan", "Schedule plan", "Packed", "Dispatch Stock"];
    let tableRows = rows.map((row, index) => {
        const bgColor = index % 2 === 0 ? '#ffe6f0' : '#e6e6ff'; 
        return `
        <tr style="background-color: ${bgColor};">
            <td style="border: 1px solid #fff; padding: 8px; text-align: center;">${index + 1}</td>
            <td style="border: 1px solid #fff; padding: 8px;">${row}</td>
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Today -->
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Yesterday -->
            ${index === 0 ? `<td style="border: 1px solid #fff; padding: 8px;" rowspan="${rows.length}">
            <div style="text-align: center; font-weight: bold; color: #444;">
                            Packing Plan :<br><br><br>
                            Dispatch Plan :
                        </div>
            </td>` : ``}
        </tr>
    `}).join('');

    document.getElementById("left-table").innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <thead>
                <tr style="background-color: #00008B;">
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">S.No</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Title</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Today</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Yesterday</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Day Plan</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}

// Format 4
    function renderTableFormat4() {
    const rows = ["Entry Completed", "Followup", "Submit", "SR"];
    let tableRows = rows.map((row, index) => {
        const bgColor = index % 2 === 0 ? '#ffe6f0' : '#e6e6ff';
        return `
        <tr style="background-color: ${bgColor};">
            <td style="border: 1px solid #fff; padding: 8px; text-align: center;">${index + 1}</td>
            <td style="border: 1px solid #fff; padding: 8px;">${row}</td>
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Today -->
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Yesterday -->
            ${index === 0 ? `<td style="border: 1px solid #fff; padding: 8px;" rowspan="${rows.length}">
            <div style="text-align: center; font-weight: bold; color: #444;">
                            Entry Plan :<br><br><br>
                            Submittion :
                        </div>
            </td>` : ``}
        </tr>
    `}).join('');

    document.getElementById("left-table").innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <thead>
                <tr style="background-color: #00008B;">
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">S.No</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Title</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Today</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Yesterday</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Day Plan</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}

// Format 5
    function renderTableFormat5() {
    const rows = ["PS Completed", "Followup", "Status Updated","Onboard", "SR"];
    let tableRows = rows.map((row, index) => {
        const bgColor = index % 2 === 0 ? '#ffe6f0' : '#e6e6ff';
        return `
        <tr style="background-color: ${bgColor};">
            <td style="border: 1px solid #fff; padding: 8px; text-align: center;">${index + 1}</td>
            <td style="border: 1px solid #fff; padding: 8px;">${row}</td>
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Today -->
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Yesterday -->
            ${index === 0 ? `<td style="border: 1px solid #fff; padding: 8px;" rowspan="${rows.length}">
            <div style="text-align: center; font-weight: bold; color: #444;">
                            Entry Plan :<br><br><br>
                            Submittion :
                        </div>
            </td>` : ``}
        </tr>
    `}).join('');

    document.getElementById("left-table").innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <thead>
                <tr style="background-color: #00008B;">
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">S.No</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Title</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Today</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Yesterday</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Day Plan</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}

// Format 6
    function renderTableFormat6() {
    const rows = ["Followup", "SP", "FP","PSL", "SO Created", "SRL"];
    let tableRows = rows.map((row, index) => {
        const bgColor = index % 2 === 0 ? '#ffe6f0' : '#e6e6ff';
        return `
        <tr style="background-color: ${bgColor};">
            <td style="border: 1px solid #fff; padding: 8px; text-align: center;">${index + 1}</td>
            <td style="border: 1px solid #fff; padding: 8px;">${row}</td>
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Today -->
            <td style="border: 1px solid #fff; padding: 8px;"></td> <!-- Yesterday -->
            ${index === 0 ? `<td style="border: 1px solid #fff; padding: 8px;" rowspan="${rows.length}">
            <div style="text-align: center; font-weight: bold; color: #444;">
                            Entry Plan :<br><br><br>
                            Submittion :
                        </div>
            </td>` : ``}
        </tr>
    `}).join('');

    document.getElementById("left-table").innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <thead>
                <tr style="background-color: #00008B;">
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">S.No</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Title</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Today</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Yesterday</th>
                    <th style="border: 1px solid #fff; padding: 8px;text-align: center; color: #f0f0f0;">Day Plan</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}


};



// frappe.pages['target-monitor'].on_page_load = function(wrapper) {
//     frappe.breadcrumbs.add("HR");

//     let page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Target Monitor',
//         single_column: true
//     });

//     // Clear existing and add main container
//     $(page.body).html(`
//         <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 5px; border-bottom: 2px solid #ccc; margin-bottom: 5px;">
//             <div style="font-weight: 700; font-size: 28px;">Heading</div>
//             <div style="font-weight: 600; font-size: 18px;">Department Name</div>
//         </div>
//         <div id="timeDisplay" style="font-size: 16px; font-weight: 500; margin-bottom: 10px;">Time</div>

//         <div style="display: flex; gap: 15px;">

//             <!-- Left Column: Employee info block -->
//             <div style="width: 250px; border: 1px solid #ccc; border-radius: 10px; padding: 10px; background: #f9f9f9; text-align: center;">
//                 <div style="background: #0f1568; height: 200px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: center; align-items: center;">
//                     <img id="employeeImage" src="" alt="Employee" style="max-height: 180px; max-width: 100%; object-fit: contain;" />
//                 </div>
//                 <div id="employeeName" style="font-size: 22px; font-weight: 700; margin-bottom: 4px;">Employee Name</div>
//                 <div id="employeeDesignation" style="font-size: 16px; color: #555;">Designation</div>
//             </div>

//             <!-- Middle Column: Target Monitor Table -->
//             <div style="flex-grow: 1; border: 1px solid #ccc; border-radius: 10px; padding: 10px; background: #fff; max-height: 370px; overflow-y: auto;">
//                 <h3 style="color: #0f1568; margin-top: 0; margin-bottom: 10px;">Target Monitor</h3>
//                 <div id="targetMonitorTable">
//                     Loading Target Monitor...
//                 </div>
//             </div>

//             <!-- Right Column: Performance Monitor Table -->
//             <div style="flex-grow: 1; border: 1px solid #ccc; border-radius: 10px; padding: 10px; background: #fff; max-height: 370px; overflow-y: auto;">
//                 <h3 style="color: #0f1568; margin-top: 0; margin-bottom: 10px;">Performance Monitor</h3>
//                 <div id="performanceMonitorTable">
//                     Loading Performance Monitor...
//                 </div>
//             </div>
//         </div>
//     `);

//     // Update current time display every second
//     function updateTime() {
//         let now = new Date();
//         let options = { 
//             year: 'numeric', month: 'long', day: 'numeric', 
//             hour: '2-digit', minute: '2-digit', second: '2-digit',
//             hour12: true
//         };
//         let formatted = now.toLocaleString('en-US', options);
//         $('#timeDisplay').text(formatted);
//     }
//     updateTime();
//     setInterval(updateTime, 1000);

//     // Dummy default employee image url (replace with your default)
//     const defaultImage = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg';
//     const baseUrl = window.location.origin;

//     // Fetch Target Monitor Data
//     function fetchTargetData() {
//         let fiscalYear = getCurrentFiscalYear();

//         frappe.call({
//             method: "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",
//             args: { fiscal_year: fiscalYear },
//             callback: function(r) {
//                 if(r.message && r.message.length > 0) {
//                     let slide = r.message[0];  // Show first slide data as example

//                     // Set employee info
//                     $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage);
//                     $('#employeeName').text(slide.employee_name);
//                     $('#employeeDesignation').text(slide.employee_designation);

//                     // Build Target Monitor table HTML
//                     let targetHTML = buildTargetMonitorTable(slide);
//                     $('#targetMonitorTable').html(targetHTML);

//                     // For demo, fill Performance Monitor with dummy data
//                     $('#performanceMonitorTable').html('<p>Performance Monitor Table content will go here.</p>');
//                 }
//             }
//         });
//     }

//     // Fiscal year calculation helper
//     function getCurrentFiscalYear() {
//         let d = new Date();
//         let y = d.getFullYear();
//         return (d.getMonth() >= 3) ? `${y}-${y+1}` : `${y-1}-${y}`;
//     }

//     // Function to build Target Monitor table HTML from slide data
//     function buildTargetMonitorTable(slide) {
//         let fmtNum = (num) => Number(num || 0).toLocaleString('en-IN', {maximumFractionDigits:0});
//         let data = slide.data || [];

//         return `
//             <table style="width: 100%; border-collapse: collapse;">
//                 <thead>
//                     <tr style="background-color: #0f1568; color: white;">
//                         <th style="padding: 8px; border: 1px solid #ccc;">TARGET</th>
//                         <th style="padding: 8px; border: 1px solid #ccc;">MTD</th>
//                         <th style="padding: 8px; border: 1px solid #ccc;">QTD</th>
//                         <th style="padding: 8px; border: 1px solid #ccc;">YTD</th>
//                         <th style="padding: 8px; border: 1px solid #ccc;">YOL</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                     <tr style="background-color: #f4f4f4; font-weight: 600;">
//                         <td style="padding: 8px; border: 1px solid #ccc;">Target</td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${data.map(d => fmtNum(d.revised_ct)).join(', ')}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.qtd_target_ct)}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.ytd_target_ct)}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.annual_ct)}
//                         </td>
//                     </tr>
//                     <tr style="background-color: #e0f7fa; color: blue; font-weight: 600;">
//                         <td style="padding: 8px; border: 1px solid #ccc;">Achieved</td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${data.map(d => fmtNum(d.achieved)).join(', ')}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.qtd_achieved)}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.ytd_achieved)}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.yol_ytd_achieved)}
//                         </td>
//                     </tr>
//                     <tr style="background-color: #f4f4f4; font-weight: 600;">
//                         <td style="padding: 8px; border: 1px solid #ccc;">YTA</td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${data.map(d => fmtNum(d.ct_yta)).join(', ')}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.yta_qtd)}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.yta_ytd)}
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             &#8377;${fmtNum(slide.yol_yta_ytd)}
//                         </td>
//                     </tr>
//                     <tr style="background-color: #e0f7fa; color: blue; font-weight: 600;">
//                         <td style="padding: 8px; border: 1px solid #ccc;">SR(%)</td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             ${data.map(d => d.mtd_sr || '0').join(', ')}%
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             ${slide.qtd_sr || '0'}%
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             ${slide.ytd_sr || '0'}%
//                         </td>
//                         <td style="padding: 8px; border: 1px solid #ccc; text-align: right;">
//                             ${slide.ytd_sr || '0'}%
//                         </td>
//                     </tr>
//                 </tbody>
//             </table>
//             <div style="margin-top: 12px; display: flex; justify-content: space-between; font-weight: 600; font-size: 14px;">
//                 <div>Target: ${slide.target || '-'}</div>
//                 <div>Fiscal Year: ${slide.fiscal_year || '-'}</div>
//                 <div>Annual CT: ${slide.annual_ct || '-'}</div>
//                 <div>Annual FT: ${slide.annual_ft || '-'}</div>
//             </div>
//         `;
//     }

//     // Call to fetch and display data
//     fetchTargetData();
// }; - its worng


// frappe.pages['target-monitor'].on_page_load = function (wrapper) {
//     frappe.breadcrumbs.add("HR");
//     let me = this;

//     // Create a page layout with a single column
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Target Monitor',
//         single_column: true
//     });

//     // Add a container for the slide content and employee info
//     $(page.body).append(`
//         <div style="margin-bottom: 10px; text-align: center;">
//                 <div style="font-size: 3.5em;font-weight: bold;class="mt-0"">COMMITED TARGET-CT</div>
//                 <div id="currentMonth" style="font-size: 2.2em; flex: 1;" class="mt-2"></div>
//             </div>
//         <div id="slideContainer" style="display: flex; align-items: flex-start; ">
//             <div class="employee-info" style="margin-right: 20px; text-align: center; flex-shrink: 0;">
//                 <img id="employeeImage" src="" alt="Employee Image" style="width: 100px; height: 100px; margin-bottom: 10px;"/>
//                 <h4 id="employeeName"></h4>
//                 <p id="employeeDesignation"></p>
//             </div>
//             <div style="flex-grow: 1;">
//                 <div class="slide" style="display: none;"></div>
//             </div>
//         </div>
//     `);

//     // function displayCurrentMonth() {
//     //     const options = { month: 'long' };
//     //     const currentMonth = new Date().toLocaleDateString('en-US', options);
//     //     $('#currentMonth').text(`Month: ${currentMonth}`);
//     // }
//     function displayCurrentMonth() {
//         const options = { month: 'long', day: 'numeric', year: 'numeric' };
//         const currentDate = new Date();
//         const formattedDate = currentDate.toLocaleDateString('en-US', options);
    
//         // Format time as HH:MM AM/PM
//         const formattedTime = currentDate.toLocaleTimeString('en-US', {
//             hour: '2-digit',
//             minute: '2-digit',
//             second: '2-digit',
//             hour12: true
//         });
    
//         $('#currentMonth').html(`Date: ${formattedDate} | Time: <span id="currentTime">${formattedTime}</span>`);
//     }
    
//     // Update the time every second
//     setInterval(() => {
//         const currentTime = new Date().toLocaleTimeString('en-US', {
//             hour: '2-digit',
//             minute: '2-digit',
//             second: '2-digit',
//             hour12: true
//         });
//         $('#currentTime').text(currentTime);
//     }, 1000);
    

//     function generateMonthOptions() {
//         const months = [
//             "January", "February", "March", "April",
//             "May", "June", "July", "August",
//             "September", "October", "November", "December"
//         ];
//         return months.map((month, index) => `<option value="${index + 1}">${month}</option>`).join('');
//     }
//     function getCurrentFiscalYear() {
//         const currentDate = new Date();
//         const currentMonth = currentDate.getMonth(); // 0 = January, 11 = December
//         const currentYear = currentDate.getFullYear();

//         // Assuming fiscal year starts in April (Month 3, index 3)
//         if (currentMonth >= 3) {
//             // If current month is April or later, the fiscal year is currentYear to currentYear + 1
//             return `${currentYear}-${currentYear + 1}`;
//         } else {
//             // If current month is before April, the fiscal year is previous year to currentYear
//             return `${currentYear - 1}-${currentYear}`;
//         }
//     }
//     function fetchTargetData() {
//         const fiscalYear = getCurrentFiscalYear(); 
//         console.log(fiscalYear)
//         // Only fetch if an employee is selected
//         frappe.call({
//             method: "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",
//             args: {
//                 fiscal_year: fiscalYear, // Pass the selected fiscal year
//             },
//             callback: function(response) {
//                 if (response.message) {
//                     var slidesData = response.message;
//                     var slideIndex = 0;

//                     // Display the first slide initially
//                     displaySlides(slidesData, slideIndex);

//                     // Automatically change slides every 5 seconds
//                     setInterval(function() {
//                         slideIndex = (slideIndex + 1) % slidesData.length;
//                         displaySlides(slidesData, slideIndex);
//                     }, 5000); // 5000 ms = 5 seconds
//                 }
//             }
//         });
//     }
//     $('<style>')
//     .prop('type', 'text/css')
//     .html(`
//         @keyframes blinkEffect {
//             0% { background-color: #e0f7fa; }
//             50% { background-color: #ffeb3b; } /* Change to yellow */
//             100% { background-color: #e0f7fa; }
//         }

//         .blinking {
//             animation: blinkEffect 1s infinite;
//         }
//     `)
//     .appendTo('head');

//     function displaySlides(slidesData, index) {
//         var slide = slidesData[index];
//         const defaultImage = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg'; 
//         const baseUrl = window.location.origin;
//         // <div style="margin-bottom: 10px; "> 
//         //     {slide.employee_image}
//         // </div>
//         var slideContent = `
            
//             `;
//         $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage).css({
//             'width': '250px',  // Set your desired width here
//             'height': '300px',  // Set your desired height here
//             'background-image': 'cover',
//             'margin-top': '-30px',
//         });
//         $('#employeeName').text(slide.employee_name).css({
//             'font-size':'30px'
//         });
//         $('#employeeDesignation').text(slide.employee_designation).css({
//             'font-size':'15px'
//         });
        
//         slideContent += `
            
//             <div style="margin-bottom: 20px; margin-top: -30px;">
//                 <table style="width: 100%;height: 300px; border-collapse: collapse;box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);">
//                     <tr>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">TARGET</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">MTD</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">QTD</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YTD</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YOL</td>
//                     </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">Target</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.data.map(item => item.revised_ct || '0').join(', ')}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.qtd_target_ct || '0'}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.ytd_target_ct || '0'}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.annual_ct || '0'}</td>
//                     </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;">Achieved</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;">&#8377;${slide.data.map(item => item.achieved || '0').join(', ')}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;">&#8377;${slide.qtd_achieved || '0'}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;">&#8377;${slide.ytd_achieved || '0'}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;">&#8377;${slide.ytd_achieved || '0'}</td>
//                     </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">YTA</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.data.map(item => item.ct_yta || '0').join(', ')}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.yta_qtd || '0'}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.yta_ytd || '0'}</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;">&#8377;${slide.yta_ytd || '0'}</td>
//                     </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #e0f7fa;">SR(%)</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #e0f7fa;">${slide.data.map(item => item.mtd_sr || '0').join(', ')}%</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #e0f7fa;">${slide.qtd_sr || '0'}%</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #e0f7fa;">${slide.ytd_sr || '0'}%</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #e0f7fa;">${slide.ytd_sr || '0'}%</td>
//                     </tr>
//                 </table>
//             </div>
//         `;

//         slideContent += `
//             <div style="padding-top: 25px; display: flex; justify-content: space-between;">
//                 <div style="flex: 1; text-align: left; white-space: nowrap; font-weight: 500; font-size: 14px;">
//                     Target:<span style="font-size: 10.5px;"> ${slide.target || '0'}
//                 </span></div>
//                 <div style="flex: 1; text-align: left;font-weight: 500; font-size: 14px;">
//                     Fiscal Year:<span style="font-size: 10.5px;"> ${slide.fiscal_year || '0'}</span>
//                 </div>
//                 <div style="flex: 1; text-align: center;font-weight: 500; font-size: 14px;">
//                     Annual CT:<span style="font-size: 10.5px;"> ${slide.annual_ct || '0'}</span>
//                 </div>
//                 <div style="flex: 1; text-align: right;font-weight: 500; font-size: 14px;">
//                     Annual FT:<span style="font-size: 10.5px;"> ${slide.annual_ft || '0'}</span>
//                 </div>
//             </div>
//         `;
//         $(".slide").html(slideContent).fadeIn();
//         displayCurrentMonth();
//     }

//     fetchTargetData();  // Call this function to fetch and display the data
// };

// frappe.pages['performance-monitor'].on_page_load = function (wrapper) {
//     frappe.breadcrumbs.add("HR");
//     let me = this;

//     // Create a page layout with a single column
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Performance Monitor',
//         single_column: true
//     });

//     // Add a container for the slide content and employee info
//     $(page.body).append(`
//         <div style="margin-bottom: 10px; text-align: left;">
//                 <div style="font-size: 80pm;font-weight: bold;;class="mt-0"">COMMITED TARGET-CT</div>
//                 <div id="currentMonth" style="font-size: 2.2em; flex: 1;" class="mt-2"></div>
//             </div>
//         <div id="slideContainer" style="display: flex; align-items: flex-start; " class="blinking-container">
//             <div class="employee-info" style="margin-right: 20px; text-align: center; flex-shrink: 0;">
//                 <img id="employeeImage" src="" alt="Employee Image" style="width: 100px; height: 100px; margin-bottom: 10px;"/>
//                 <h4 id="employeeName"></h4>
//                 <p id="employeeDesignation"></p>
//             </div>
//             <div style="flex-grow: 1;">
//                 <div class="slide" style="display: none;"></div>
//             </div>
//         </div>
//     `);
    
//     function displayCurrentMonth() {
//         const options = { month: 'long', day: 'numeric', year: 'numeric' };
//         const currentDate = new Date();
//         const formattedDate = currentDate.toLocaleDateString('en-US', options);
    
//         // Format time as HH:MM AM/PM
//         const formattedTime = currentDate.toLocaleTimeString('en-US', {
//             hour: '2-digit',
//             minute: '2-digit',
//             second: '2-digit',
//             hour12: true
//         });
    
//         $('#currentMonth').html(`Date: ${formattedDate} | Time: <span id="currentTime">${formattedTime}</span>`);
//     }
    
//     // Update the time every second
//     setInterval(() => {
//         const currentTime = new Date().toLocaleTimeString('en-US', {
//             hour: '2-digit',
//             minute: '2-digit',
//             second: '2-digit',
//             hour12: true
//         });
//         $('#currentTime').text(currentTime);
//     }, 1000);
    

//     function generateMonthOptions() {
//         const months = [
//             "January", "February", "March", "April",
//             "May", "June", "July", "August",
//             "September", "October", "November", "December"
//         ];
//         return months.map((month, index) => `<option value="${index + 1}">${month}</option>`).join('');
//     }
//     function getCurrentFiscalYear() {
//         const currentDate = new Date();
//         const currentMonth = currentDate.getMonth(); // 0 = January, 11 = December
//         const currentYear = currentDate.getFullYear();

//         // Assuming fiscal year starts in April (Month 3, index 3)
//         if (currentMonth >= 3) {
//             // If current month is April or later, the fiscal year is currentYear to currentYear + 1
//             return `${currentYear}-${currentYear + 1}`;
//         } else {
//             // If current month is before April, the fiscal year is previous year to currentYear
//             return `${currentYear - 1}-${currentYear}`;
//         }
//     }
//     function fetchTargetData() {
//         const fiscalYear = getCurrentFiscalYear(); 
//         console.log(fiscalYear)
//         // Only fetch if an employee is selected
//         frappe.call({
//             method: "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",
//             args: {
//                 fiscal_year: fiscalYear, // Pass the selected fiscal year
//             },
//             callback: function(response) {
//                 if (response.message) {
//                     var slidesData = response.message;
//                     var slideIndex = 0;

//                     // Display the first slide initially
//                     displaySlides(slidesData, slideIndex);

//                     // Automatically change slides every 5 seconds
//                     setInterval(function() {
//                         slideIndex = (slideIndex + 1) % slidesData.length;
//                         displaySlides(slidesData, slideIndex);
//                     }, 20000); // 5000 ms = 5 seconds
//                 }
//             }
//         });
//     }
//     $('<style>')
// .prop('type', 'text/css')
// .html(`
//     @keyframes blinkEffect {
//         0%   { background-color: #f5f5f5; }  /* Light Cyan */
//         50%  { background-color: #e8f5e9; }  /* Light Lavender (soft purple) */
//         100% { background-color: #f5f5f5; }
//     }

//     .blinking-container {
//         animation: blinkEffect 1.2s infinite;
//         padding: 10px;
//         border-radius: 10px;
//     }
// `)
// .appendTo('head');



//     function displaySlides(slidesData, index) {
//         var slide = slidesData[index];
//         const defaultImage = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg'; 
//         const baseUrl = window.location.origin;
//         // <div style="margin-bottom: 10px; "> 
//         //     {slide.employee_image}
//         // </div>
//         var slideContent = `
            
//             `;
//         $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage).css({
//             'width': '250px',  // Set your desired width here
//             'height': '300px',  // Set your desired height here
//             'background-image': 'cover',
//             'margin-top': '-30px',
//         });
//         $('#employeeName').text(slide.employee_name).css({
//             'font-size':'30px'
//         });
//         $('#employeeDesignation').text(slide.employee_designation).css({
//             'font-size':'15px'
//         });
        
//         slideContent += `
            
//             <div class="blinking-container" style="margin-bottom: 20px; margin-top: -30px;">
//                 <table style="width: 100%;height: 300px; border-collapse: collapse;box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);">
//                     <tr>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">TARGET</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">MTD</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">QTD</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YTD</td>
//                         <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YOL</td>
//                     </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;font-size:20px">Target</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size: 20px; background-color: #f4f4f4;text-align:right">
//                             &#8377;${slide.data.map(item => 
//                                 (Number(item.revised_ct?.toString().replace(/,/g, '')) || 0)
//                                 .toLocaleString('en-IN', { maximumFractionDigits: 0 })
//                             ).join(', ')}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
//                             &#8377;${(Number(slide.qtd_target_ct.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
//                             &#8377;${(Number(slide.ytd_target_ct.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
//                         &#8377;${(Number(slide.annual_ct.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                     </td>


//                     </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;">Achieved</td>
//                         <td style="border: 1px solid #ccc; padding: 8px; color: blue; font-size: 20px; background-color: #e0f7fa;text-align:right">
//                             &#8377;${slide.data.map(item => 
//                                 (Number(item.achieved?.toString().replace(/,/g, '')) || 0)
//                                 .toLocaleString('en-IN', { maximumFractionDigits: 0 })
//                             ).join(', ')}
//                         </td>

//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;text-align:right">
//                             &#8377;${(Number(slide.qtd_achieved.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;text-align:right">
//                             &#8377;${(Number(slide.ytd_achieved.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;text-align:right">
//                             &#8377;${(Number(slide.yol_ytd_achieved.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                         </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;font-size:20px">YTA</td>
//                         <td style="border: 1px solid #ccc; padding: 8px; font-size: 20px; background-color: #f4f4f4;text-align:right">
//                             &#8377;${slide.data.map(item => 
//                                 (Number(item.ct_yta?.toString().replace(/,/g, '')) || 0)
//                                 .toLocaleString('en-IN', { maximumFractionDigits: 0 })
//                             ).join(', ')}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
//                             &#8377;${(Number(slide.yta_qtd.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
//                             &#8377;${(Number(slide.yta_ytd.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
//                             &#8377;${(Number(slide.yol_yta_ytd.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
//                         </td>
//                     </tr>
//                     <tr>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;">SR(%)</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.data.map(item => item.mtd_sr || '0').join(', ')}%</td>
                        
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.qtd_sr || '0'}%</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.ytd_sr || '0'}%</td>
//                         <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.ytd_sr || '0'}%</td>
//                     </tr>
//                 </table>
//             </div>
//         `;
//         console.log(slide);
//         console.log(slide.data);
        
//         slideContent += `
//             <div style="padding-top: 25px; display: flex; justify-content: space-between;">
//                 <div style="flex: 1; text-align: left; white-space: nowrap; font-weight: 500; font-size: 14px;">
//                     Target:<span style="font-size: 10.5px;"> ${slide.target || '0'}
//                 </span></div>
//                 <div style="flex: 1; text-align: left;font-weight: 500; font-size: 14px;">
//                     Fiscal Year:<span style="font-size: 10.5px;"> ${slide.fiscal_year || '0'}</span>
//                 </div>
//                 <div style="flex: 1; text-align: center;font-weight: 500; font-size: 14px;">
//                     Annual CT:<span style="font-size: 10.5px;"> ${slide.annual_ct || '0'}</span>
//                 </div>
//                 <div style="flex: 1; text-align: right;font-weight: 500; font-size: 14px;">
//                     Annual FT:<span style="font-size: 10.5px;"> ${slide.annual_ft || '0'}</span>
//                 </div>
//             </div>
//         `;
//         $(".slide").html(slideContent).fadeIn();
//         // let fullContent = slideContent + '<br><hr><br>' + slideContent;  // repeat content with spacing
//         // $(".slide").html(fullContent).fadeIn();

//         displayCurrentMonth();
//     }

//     fetchTargetData();  // Call this function to fetch and display the data
// };

