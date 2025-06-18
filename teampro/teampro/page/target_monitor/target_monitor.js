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

frappe.pages['target-monitor'].on_page_load = function (wrapper) {
    frappe.breadcrumbs.add("HR");
    let me = this;

    // Create a page layout with a single column
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Target Monitor',
        single_column: true
    });

    // Add a container for the slide content and employee info
    $(page.body).append(`
        <div style="margin-bottom: 10px; text-align: center;">
                <div style="font-size: 3.5em;font-weight: bold;class="mt-0"">COMMITED TARGET-CT</div>
                <div id="currentMonth" style="font-size: 2.2em; flex: 1;" class="mt-2"></div>
            </div>
        <div id="slideContainer" style="display: flex; align-items: flex-start; " class="blinking-container">
            <div class="employee-info" style="margin-right: 20px; text-align: center; flex-shrink: 0;">
                <img id="employeeImage" src="" alt="Employee Image" style="width: 100px; height: 100px; margin-bottom: 10px;"/>
                <h4 id="employeeName"></h4>
                <p id="employeeDesignation"></p>
            </div>
            <div style="flex-grow: 1;">
                <div class="slide" style="display: none;"></div>
            </div>
        </div>
    `);
    
    function displayCurrentMonth() {
        const options = { month: 'long', day: 'numeric', year: 'numeric' };
        const currentDate = new Date();
        const formattedDate = currentDate.toLocaleDateString('en-US', options);
    
        // Format time as HH:MM AM/PM
        const formattedTime = currentDate.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });
    
        $('#currentMonth').html(`Date: ${formattedDate} | Time: <span id="currentTime">${formattedTime}</span>`);
    }
    
    // Update the time every second
    setInterval(() => {
        const currentTime = new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });
        $('#currentTime').text(currentTime);
    }, 1000);
    

    function generateMonthOptions() {
        const months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ];
        return months.map((month, index) => `<option value="${index + 1}">${month}</option>`).join('');
    }
    function getCurrentFiscalYear() {
        const currentDate = new Date();
        const currentMonth = currentDate.getMonth(); // 0 = January, 11 = December
        const currentYear = currentDate.getFullYear();

        // Assuming fiscal year starts in April (Month 3, index 3)
        if (currentMonth >= 3) {
            // If current month is April or later, the fiscal year is currentYear to currentYear + 1
            return `${currentYear}-${currentYear + 1}`;
        } else {
            // If current month is before April, the fiscal year is previous year to currentYear
            return `${currentYear - 1}-${currentYear}`;
        }
    }
    function fetchTargetData() {
        const fiscalYear = getCurrentFiscalYear(); 
        console.log(fiscalYear)
        // Only fetch if an employee is selected
        frappe.call({
            method: "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",
            args: {
                fiscal_year: fiscalYear, // Pass the selected fiscal year
            },
            callback: function(response) {
                if (response.message) {
                    var slidesData = response.message;
                    var slideIndex = 0;

                    // Display the first slide initially
                    displaySlides(slidesData, slideIndex);

                    // Automatically change slides every 5 seconds
                    setInterval(function() {
                        slideIndex = (slideIndex + 1) % slidesData.length;
                        displaySlides(slidesData, slideIndex);
                    }, 20000); // 5000 ms = 5 seconds
                }
            }
        });
    }
    $('<style>')
.prop('type', 'text/css')
.html(`
    @keyframes blinkEffect {
        0%   { background-color: #f5f5f5; }  /* Light Cyan */
        50%  { background-color: #e8f5e9; }  /* Light Lavender (soft purple) */
        100% { background-color: #f5f5f5; }
    }

    .blinking-container {
        animation: blinkEffect 1.2s infinite;
        padding: 10px;
        border-radius: 10px;
    }
`)
.appendTo('head');



    function displaySlides(slidesData, index) {
        var slide = slidesData[index];
        const defaultImage = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg'; 
        const baseUrl = window.location.origin;
        // <div style="margin-bottom: 10px; "> 
        //     {slide.employee_image}
        // </div>
        var slideContent = `
            
            `;
        $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage).css({
            'width': '250px',  // Set your desired width here
            'height': '300px',  // Set your desired height here
            'background-image': 'cover',
            'margin-top': '-30px',
        });
        $('#employeeName').text(slide.employee_name).css({
            'font-size':'30px'
        });
        $('#employeeDesignation').text(slide.employee_designation).css({
            'font-size':'15px'
        });
        
        slideContent += `
            
            <div class="blinking-container" style="margin-bottom: 20px; margin-top: -30px;">
                <table style="width: 100%;height: 300px; border-collapse: collapse;box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);">
                    <tr>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">TARGET</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">MTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">QTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YOL</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;font-size:20px">Target</td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size: 20px; background-color: #f4f4f4;text-align:right">
                            &#8377;${slide.data.map(item => 
                                (Number(item.revised_ct?.toString().replace(/,/g, '')) || 0)
                                .toLocaleString('en-IN', { maximumFractionDigits: 0 })
                            ).join(', ')}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
                            &#8377;${(Number(slide.qtd_target_ct.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
                            &#8377;${(Number(slide.ytd_target_ct.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
                        &#8377;${(Number(slide.annual_ct.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                    </td>


                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;">Achieved</td>
                        <td style="border: 1px solid #ccc; padding: 8px; color: blue; font-size: 20px; background-color: #e0f7fa;text-align:right">
                            &#8377;${slide.data.map(item => 
                                (Number(item.achieved?.toString().replace(/,/g, '')) || 0)
                                .toLocaleString('en-IN', { maximumFractionDigits: 0 })
                            ).join(', ')}
                        </td>

                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;text-align:right">
                            &#8377;${(Number(slide.qtd_achieved.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;text-align:right">
                            &#8377;${(Number(slide.ytd_achieved.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px;background-color: #e0f7fa;text-align:right">
                            &#8377;${(Number(slide.yol_ytd_achieved.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                        </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;background-color: #f4f4f4;font-size:20px">YTA</td>
                        <td style="border: 1px solid #ccc; padding: 8px; font-size: 20px; background-color: #f4f4f4;text-align:right">
                            &#8377;${slide.data.map(item => 
                                (Number(item.ct_yta?.toString().replace(/,/g, '')) || 0)
                                .toLocaleString('en-IN', { maximumFractionDigits: 0 })
                            ).join(', ')}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
                            &#8377;${(Number(slide.yta_qtd.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
                            &#8377;${(Number(slide.yta_ytd.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #f4f4f4;text-align:right">
                            &#8377;${(Number(slide.yol_yta_ytd.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;">SR(%)</td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.data.map(item => item.mtd_sr || '0').join(', ')}%</td>
                        
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.qtd_sr || '0'}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.ytd_sr || '0'}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;font-size:20px;background-color: #e0f7fa;text-align:right">${slide.ytd_sr || '0'}%</td>
                    </tr>
                </table>
            </div>
        `;
        console.log(slide);
        console.log(slide.data);
        
        slideContent += `
            <div style="padding-top: 25px; display: flex; justify-content: space-between;">
                <div style="flex: 1; text-align: left; white-space: nowrap; font-weight: 500; font-size: 14px;">
                    Target:<span style="font-size: 10.5px;"> ${slide.target || '0'}
                </span></div>
                <div style="flex: 1; text-align: left;font-weight: 500; font-size: 14px;">
                    Fiscal Year:<span style="font-size: 10.5px;"> ${slide.fiscal_year || '0'}</span>
                </div>
                <div style="flex: 1; text-align: center;font-weight: 500; font-size: 14px;">
                    Annual CT:<span style="font-size: 10.5px;"> ${slide.annual_ct || '0'}</span>
                </div>
                <div style="flex: 1; text-align: right;font-weight: 500; font-size: 14px;">
                    Annual FT:<span style="font-size: 10.5px;"> ${slide.annual_ft || '0'}</span>
                </div>
            </div>
        `;
        $(".slide").html(slideContent).fadeIn();
        displayCurrentMonth();
    }

    fetchTargetData();  // Call this function to fetch and display the data
};
