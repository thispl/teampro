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
//                     // }, 20000); // 5000 ms = 5 seconds
//                     },5000);
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


//original
// frappe.pages['target-monitor'].on_page_load = function (wrapper) {
//     frappe.breadcrumbs.add("HR");
//     let me = this;

//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Target Monitor',
//         single_column: true
//     });

//     $(page.body).append(`
//         <div style="margin-bottom: 10px; text-align: center;">
//             <div style="font-size: 3.5em;font-weight: bold;">COMMITED TARGET-CT</div>
//             <div id="currentMonth" style="font-size: 2.2em;"></div>
//         </div>
//         <div id="slideContainer" style="display: flex; align-items: flex-start;" class="blinking-container">
//             <div class="employee-info" style="margin-right: 20px; text-align: center; flex-shrink: 0;">
//                 <img id="employeeImage" src="" alt="Employee Image" style="width: 250px; height: 300px; margin-bottom: 10px; margin-top: -30px;"/>
//                 <h4 id="employeeName" style="font-size: 30px;"></h4>
//                 <p id="employeeDesignation" style="font-size: 15px;"></p>
//             </div>
//             <div style="flex-grow: 1;">
//                 <div class="slide" style="font-size: 20px; margin-top: 15px; font-weight: 500; color: #333;">Fetching Target Data... Please wait</div>
//             </div>
//         </div>
//     `);

//     function displayCurrentMonth() {
//         const options = { month: 'long', day: 'numeric', year: 'numeric' };
//         const currentDate = new Date();
//         const formattedDate = currentDate.toLocaleDateString('en-US', options);
//         const formattedTime = currentDate.toLocaleTimeString('en-US', {
//             hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true
//         });
//         $('#currentMonth').html(`Date: ${formattedDate} | Time: <span id="currentTime">${formattedTime}</span>`);
//     }

//     setInterval(() => {
//         const currentTime = new Date().toLocaleTimeString('en-US', {
//             hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true
//         });
//         $('#currentTime').text(currentTime);
//     }, 1000);

//     function getCurrentFiscalYear() {
//         const currentDate = new Date();
//         const month = currentDate.getMonth();
//         const year = currentDate.getFullYear();
//         return month >= 3 ? `${year}-${year + 1}` : `${year - 1}-${year}`;
//     }

//     function fetchTargetData() {
//         const fiscalYear = getCurrentFiscalYear();

//         Promise.all([
//             frappe.call({ method: "teampro.teampro.page.target_monitor.target_monitor.get_slide_attachments" }),
//             frappe.call({
//                 method: "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",
//                 args: { fiscal_year: fiscalYear }
//             })
//         ]).then(([attachmentsResponse, targetsResponse]) => {
//             const attachments = attachmentsResponse.message || [];
//             const targets = targetsResponse.message || [];
//             let slides = [];
//             const hasMultipleAttachments = attachments.length > 1;
//             const singleAttachment = attachments.length === 1 ? attachments[0] : null;

//             for (let i = 0; i < targets.length; i++) {
//                 slides.push(targets[i]);
//                 let attachment = hasMultipleAttachments ? attachments[i % attachments.length] : singleAttachment;
//                 if (attachment) {
//                     slides.push({
//                         is_attachment_slide: true,
//                         file_url: attachment.file_url,
//                         file_name: attachment.file_name
//                     });
//                 }
//             }

//             let index = 0;

//             function renderSlide() {
//                 const slide = slides[index];
//                 const defaultImg = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg';
//                 const base = window.location.origin;

//                 if (slide.is_attachment_slide) {
//                      $('#slideContainer').removeClass('blinking-container');
//         $('#currentMonth').prev().html("Today Events 🎉");
//                     $('#employeeImage, #employeeName, #employeeDesignation').hide();
// $(".slide").html(`
//     <div style="margin-top: -90px; display: flex; justify-content: center; align-items: center;">
//         <img src="${slide.file_url}" alt="Attachment Image" style="height: 40%; width: 65%; border: 1px solid #ccc;" />
//     </div>
// `).fadeIn();

//                 } else {
//                      $('#slideContainer').addClass('blinking-container');
//         $('#currentMonth').prev().html("COMMITED TARGET-CT");

//                     $('#employeeImage, #employeeName, #employeeDesignation').show();
//                     $('#employeeImage').attr('src', slide.employee_image ? base + slide.employee_image : defaultImg);
//                     $('#employeeName').text(slide.employee_name);
//                     $('#employeeDesignation').text(slide.employee_designation);

//                     let content = `
// <div style="margin-bottom: 20px; margin-top: -30px;">
//     <table style="width: 100%;height: 300px; border-collapse: collapse;box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);">
//         <tr>
//             <td style="background-color: #0f1568; color: white; border: 1px solid #ccc; padding: 8px; text-align:center">TARGET</td>
//             <td style="background-color: #0f1568; color: white; border: 1px solid #ccc; padding: 8px; text-align:center">MTD</td>
//             <td style="background-color: #0f1568; color: white; border: 1px solid #ccc; padding: 8px; text-align:center">QTD</td>
//             <td style="background-color: #0f1568; color: white; border: 1px solid #ccc; padding: 8px; text-align:center">YTD</td>
//             <td style="background-color: #0f1568; color: white; border: 1px solid #ccc; padding: 8px; text-align:center">YOL</td>
//         </tr>
//         <tr>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4;font-size: 20px;">Target</td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4;font-size: 20px; text-align:right;">
//                 &#8377;${slide.data.map(item => 
//                     (Number(item.revised_ct?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')
//                 ).join(', ')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.qtd_target_ct?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.ytd_target_ct?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.annual_ct?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//         </tr>
//         <tr>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; color: blue;font-size: 20px;">Achieved</td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; color: blue;font-size: 20px; text-align:right;">
//                 &#8377;${slide.data.map(item => 
//                     (Number(item.achieved?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')
//                 ).join(', ')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; color: blue; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.qtd_achieved?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; color: blue; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.ytd_achieved?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; color: blue; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.yol_ytd_achieved?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//         </tr>
//         <tr>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4;font-size: 20px;">YTA</td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4; text-align:right;font-size: 20px;">
//                 &#8377;${slide.data.map(item => 
//                     (Number(item.ct_yta?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')
//                 ).join(', ')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.yta_qtd?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.yta_ytd?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #f4f4f4; text-align:right;font-size: 20px;">
//                 &#8377;${(Number(slide.yol_yta_ytd?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}
//             </td>
//         </tr>
//         <tr>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa;font-size: 20px;">SR(%)</td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; text-align:right;font-size: 20px;">
//                 ${slide.data.map(item => item.mtd_sr || '0').join(', ')}%
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; text-align:right;font-size: 20px;">
//                 ${slide.qtd_sr || '0'}%
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; text-align:right;font-size: 20px;">
//                 ${slide.ytd_sr || '0'}%
//             </td>
//             <td style="border: 1px solid #ccc; padding: 8px; background-color: #e0f7fa; text-align:right;font-size: 20px;">
//                 ${slide.ytd_sr || '0'}%
//             </td>
//         </tr>
//     </table>
// </div>
// <div style="padding-top: 25px; display: flex; justify-content: space-between;">
//     <div style="flex: 1; text-align: left; white-space: nowrap; font-weight: 500; font-size: 14px;">
//         Target:<span style="font-size: 10.5px;"> ${slide.target || '0'}</span>
//     </div>
//     <div style="flex: 1; text-align: left; font-weight: 500; font-size: 14px;">
//         Fiscal Year:<span style="font-size: 10.5px;"> ${slide.fiscal_year || '0'}</span>
//     </div>
//     <div style="flex: 1; text-align: center; font-weight: 500; font-size: 14px;">
//         Annual CT:<span style="font-size: 10.5px;"> &#8377;${(Number(slide.annual_ct?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}</span>
//     </div>
//     <div style="flex: 1; text-align: right; font-weight: 500; font-size: 14px;">
//         Annual FT:<span style="font-size: 10.5px;"> &#8377;${(Number(slide.annual_ft?.toString().replace(/,/g, '')) || 0).toLocaleString('en-IN')}</span>
//     </div>
// </div>

//                     `;
//                     $(".slide").html(content).fadeIn();
//                 }

//                 displayCurrentMonth();
                
//                 index = (index + 1) % slides.length;
//             }

//             renderSlide();
//             setInterval(renderSlide, 20000);
//         });
//     }

//     $('<style>')
//     .prop('type', 'text/css')
//     .html(`
//         @keyframes blinkEffect {
//             0%   { background-color: #f5f5f5; }
//             50%  { background-color: #e8f5e9; }
//             100% { background-color: #f5f5f5; }
//         }
//         .blinking-container {
//             animation: blinkEffect 1.2s infinite;
//             padding: 10px;
//             border-radius: 10px;
//         }
//     `)
//     .appendTo('head');

//     fetchTargetData();
// };


//gold theme

// frappe.pages['target-monitor'].on_page_load = function (wrapper) {
//     frappe.breadcrumbs.add("HR");

//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Target Monitor',
//         single_column: true
//     });

//     $(page.body).append(`

//         <div class="tm-page-bg">

//             <!-- FILTERS -->
//             <div class="tm-filter-bar">

//                 <select id="employeeFilter" class="tm-filter-box">
//                     <option value="">All Employees</option>
//                 </select>

//                 <select id="departmentFilter" class="tm-filter-box">
//                     <option value="">All Departments</option>
//                 </select>

//                 <select id="serviceFilter" class="tm-filter-box">
//                     <option value="">All Services</option>
//                 </select>

//             </div>

//             <div class="target-monitor-wrapper">

//                 <!-- HEADER BAND -->
//                 <div class="tm-header-band">

//                     <div class="tm-emp-left">
//                         <div class="tm-emp-avatar" id="employeeAvatarInitials">--</div>
//                         <img id="employeeImage" class="tm-emp-img" style="display:none;" />
//                         <div class="tm-emp-text">
//                             <div class="tm-emp-name" id="employeeName"></div>
//                             <div class="tm-emp-desig" id="employeeDesignation"></div>
//                         </div>
//                     </div>

//                     <div class="tm-title-right">
//                         <div class="tm-main-title" id="mainTitle">PERFORMANCE MONITOR</div>
//                         <div class="tm-datetime" id="currentMonth"></div>
//                     </div>

//                 </div>

               
//                 <!-- TABLE AREA -->
//                 <div id="slideContainer" class="tm-table-wrap">
//                     <div class="slide">Fetching Target Data...</div>
//                 </div>

//             </div>
//         </div>

//     `);


//     // ──────────────────────────────────────────
//     // FILTERS
//     // ──────────────────────────────────────────
//     function loadFilters() {

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: { doctype: "Employee", filters: { status: "Active" }, fields: ["name", "employee_name"], limit_page_length: 1000 },
//             callback: function(r) {
//                 (r.message || []).forEach(emp => {
//                     $('#employeeFilter').append(`<option value="${emp.name}">${emp.employee_name}</option>`);
//                 });
//             }
//         });

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: { doctype: "Department", fields: ["name"], limit_page_length: 1000 },
//             callback: function(r) {
//                 (r.message || []).forEach(dep => {
//                     $('#departmentFilter').append(`<option value="${dep.name}">${dep.name}</option>`);
//                 });
//             }
//         });

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: { doctype: "Services", fields: ["name"], limit_page_length: 1000 },
//             callback: function(r) {
//                 (r.message || []).forEach(service => {
//                     $('#serviceFilter').append(`<option value="${service.name}">${service.name}</option>`);
//                 });
//             }
//         });
//     }

//     loadFilters();

//     $('#employeeFilter, #departmentFilter, #serviceFilter').on('change', function () {
//         applyFilter();
//     });


//     // ──────────────────────────────────────────
//     // CLOCK
//     // ──────────────────────────────────────────
//     function displayCurrentMonth() {
//         const options = { month: 'long', day: 'numeric', year: 'numeric' };
//         const formattedDate = new Date().toLocaleDateString('en-US', options);
//         const formattedTime = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
//         $('#currentMonth').html(`Date: ${formattedDate} &nbsp;|&nbsp; Time: <span id="currentTime">${formattedTime}</span>`);
//     }

//     setInterval(() => {
//         const t = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
//         $('#currentTime').text(t);
//     }, 1000);


//     // ──────────────────────────────────────────
//     // FISCAL YEAR
//     // ──────────────────────────────────────────
//     function getCurrentFiscalYear() {
//         const d = new Date(), m = d.getMonth(), y = d.getFullYear();
//         return m >= 3 ? `${y}-${y + 1}` : `${y - 1}-${y}`;
//     }


//     // ──────────────────────────────────────────
//     // FILTER APPLY
//     // ──────────────────────────────────────────
//     function applyFilter() {
//         fetchTargetData(
//             $('#employeeFilter').val() || null,
//             $('#departmentFilter').val() || null,
//             $('#serviceFilter').val() || null
//         );
//     }


//     // ──────────────────────────────────────────
//     // PERFORMANCE BADGE HELPER
//     // ──────────────────────────────────────────
//     function perfBadge(label) {
//         const map = {
//             'Outstanding': 'tm-b-outstanding',
//             'Excellent':   'tm-b-excellent',
//             'Good':        'tm-b-good',
//             'Average':     'tm-b-average'
//         };
//         const cls = map[label] || 'tm-b-below';
//         return `<span class="tm-badge ${cls}">${label || '-'}</span>`;
//     }

//     function perfIndexColor(label) {
//         return label === 'Outstanding' ? '#1b5e20' :
//                label === 'Excellent'   ? '#1565c0' :
//                label === 'Good'        ? '#2e7d32' :
//                label === 'Average'     ? '#4527a0' : '#c62828';
//     }


//     // ──────────────────────────────────────────
//     // FETCH & RENDER
//     // ──────────────────────────────────────────
//     let slideInterval = null;

//     function fetchTargetData(employee=null, department=null, service=null) {

//         if (slideInterval) { clearInterval(slideInterval); slideInterval = null; }

//         const fiscalYear = getCurrentFiscalYear();

//         Promise.all([
//             frappe.call({ method: "teampro.teampro.page.target_monitor.target_monitor.get_slide_attachments" }),
//             frappe.call({
//                 method: "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",
//                 args: { fiscal_year: fiscalYear, employee, department, service }
//             })
//         ]).then(([attachmentsResponse, targetsResponse]) => {

//             const attachments = attachmentsResponse.message || [];
//             const targets     = targetsResponse.message || [];

//             let slides = [];

//             targets.forEach(t => slides.push(t));

//             if (!employee) {
//                 attachments.forEach(att => slides.push({
//                     is_attachment_slide: true,
//                     file_url: att.file_url,
//                     file_name: att.file_name
//                 }));
//             }

//             let index = 0;
//             const base = window.location.origin;
//             const defaultImg = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg';

//             function renderSlide() {

//                 const slide = slides[index];

//                 // ── ATTACHMENT SLIDE ──
//                 if (slide.is_attachment_slide) {

//                     $('#mainTitle').html("Today Events &#127881;");
//                     $('#employeeAvatarInitials').hide();
//                     $('#employeeImage').hide();
//                     $('#employeeName').hide();
//                     $('#employeeDesignation').hide();

//                     $('.slide').html(`
//                         <div style="display:flex;justify-content:center;align-items:center;padding:20px;">
//                             <img src="${slide.file_url}" class="tm-event-img" />
//                         </div>
//                     `);

//                 } else {

//                     // ── PERFORMANCE SLIDE ──
//                     $('#mainTitle').html("PERFORMANCE MONITOR");
//                     $('#employeeName').show();
//                     $('#employeeDesignation').show();
//                     $('#employeeName').text(slide.employee_name || '');
//                     $('#employeeDesignation').text(slide.employee_designation || '');

//                     if (slide.employee_image) {
//                         $('#employeeImage').attr('src', base + slide.employee_image).show();
//                         $('#employeeAvatarInitials').hide();
//                     } else {
//                         const initials = (slide.employee_name || '--').split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2);
//                         $('#employeeAvatarInitials').text(initials).show();
//                         $('#employeeImage').hide();
//                     }

//                     // ── TABLE ──
//                     const rows = [
//                         {
//                             cls: 'tm-row-mtd', rowName: 'MTD',
//                             ct:  slide.data.map(i => i.revised_ct || 0).join(', '),
//                             ach: slide.data.map(i => i.achieved || 0).join(', '),
//                             yta: slide.data.map(i => i.ct_yta || 0).join(', '),
//                             sr:  slide.data.map(i => i.mtd_sr || 0).join(', '),
//                             ep:  slide.ep || 0,
//                             nc:  slide.nc || 0,
//                             tes: slide.mtd_tes || 0,
//                             pr:  slide.mtd_pr || 0,
//                             prs: slide.mtd_prs || 0,
//                             idx: slide.mtd_performance_index || 0,
//                             perfLabel: slide.mtd_performance_label || ''
//                         },
//                         {
//                             cls: 'tm-row-qtd', rowName: 'QTD',
//                             ct:  slide.qtd_target_ct || 0,
//                             ach: slide.qtd_achieved || 0,
//                             yta: slide.yta_qtd || 0,
//                             sr:  slide.qtd_sr || 0,
//                             ep:  slide.qtd_ep_score || 0,
//                             nc:  slide.qtd_ep_score || 0,
//                             tes: slide.qtd_tes || 0,
//                             pr:  slide.qtd_pr || 0,
//                             prs: slide.qtd_prs || 0,
//                             idx: slide.qtd_performance_index || 0,
//                             perfLabel: slide.qtd_performance_label || ''
//                         },
//                         {
//                             cls: 'tm-row-ytd', rowName: 'YTD',
//                             ct:  slide.ytd_target_ct || 0,
//                             ach: slide.ytd_achieved || 0,
//                             yta: slide.yta_ytd || 0,
//                             sr:  slide.ytd_sr || 0,
//                             ep:  slide.ytd_ep_score || 0,
//                             nc:  slide.ytd_nc_score || 0,
//                             tes: slide.ytd_tes || 0,
//                             pr:  slide.ytd_pr || 0,
//                             prs: slide.ytd_prs || 0,
//                             idx: slide.ytd_performance_index || 0,
//                             perfLabel: slide.ytd_performance_label || ''
//                         },
//                         {
//                             cls: 'tm-row-yol', rowName: 'YOL',
//                             ct:  slide.annual_ct || 0,
//                             ach: slide.yol_ytd_achieved || 0,
//                             yta: slide.yol_yta_ytd || 0,
//                             sr:  slide.ytd_sr || 0,
//                             ep:  slide.yol_ep_score || 0,
//                             nc:  slide.yol_nc_score || 0,
//                             tes: slide.yol_tes || 0,
//                             pr:  slide.yol_pr || 0,
//                             prs: slide.yol_prs || 0,
//                             idx: slide.yol_performance_index || 0,
//                             perfLabel: slide.yol_performance_label || ''
//                         }
//                     ];

//                     const tableRows = rows.map(r => `
//                         <tr class="${r.cls}">
//                             <td class="tm-lbl-cell">${r.rowName}</td>
//                             <td class="tm-val-ct">&#8377;${r.ct}</td>
//                             <td class="tm-val-ach">&#8377;${r.ach}</td>
//                             <td class="tm-val-yta">&#8377;${r.yta}</td>
//                             <td class="tm-val-sr">${r.sr}%</td>
//                             <td class="tm-val-ep">${r.ep}</td>
//                             <td class="tm-val-nc">${r.nc}</td>
//                             <td class="tm-val-tes">${r.tes}%</td>
//                             <td class="tm-val-pr">${r.pr}</td>
//                             <td class="tm-val-prs">${r.prs}%</td>
//                             <td class="tm-val-idx" style="color:${perfIndexColor(r.perfLabel)}">${r.idx}%</td>
//                             <td>${perfBadge(r.perfLabel)}</td>
//                         </tr>
//                     `).join('');

//                     $('.slide').html(`
//                         <table class="tm-perf-table">
//                             <thead>
//                                 <tr>
//                                     <th>MONITOR</th>
//                                     <th>CT</th>
//                                     <th>ACH</th>
//                                     <th>YTA</th>
//                                     <th>CT_SR</th>
//                                     <th>EP</th>
//                                     <th>NC</th>
//                                     <th>TES (%)</th>
//                                     <th>PR</th>
//                                     <th>PRS</th>
//                                     <th colspan="2">PERFORMANCE INDEX</th>
//                                 </tr>
//                             </thead>
//                             <tbody>${tableRows}</tbody>
//                         </table>
//                     `);
//                 }

//                 displayCurrentMonth();
//                 index = (index + 1) % slides.length;
//             }

//             renderSlide();

//             if (!employee && slides.length > 1) {
//                 slideInterval = setInterval(renderSlide, 20000);
//             }
//         });
//     }


//     // ──────────────────────────────────────────
//     // STYLES
//     // ──────────────────────────────────────────
//     $('<style>').prop('type', 'text/css').html(`

//         /* ── PAGE BACKGROUND ── */
//         .tm-page-bg {
//             background: #fff8f0;
//             padding: 3px;
//             min-height: 100vh;
//             font-family: 'Poppins', sans-serif;
//         }

//         /* ── REMOVE FRAPPE PADDING ── */
//         .layout-main-section-wrapper,
//         .layout-main-section,
//         .page-body,
//         .page-content,
//         .main-section {
//             padding: 0 !important;
//             margin: 0 !important;
//             background: #fff8f0 !important;
//         }

//         body {
//             background: #fff8f0 !important;
//             overflow-x: hidden;
//         }

//         /* ── FILTERS ── */
//         .tm-filter-bar {
//             display: flex;
//             gap: 12px;
//             justify-content: flex-end;
//             margin-bottom: 14px;
//         }

//         .tm-filter-box {
//             padding: 8px 14px;
//             border-radius: 8px;
//             border: 1.5px solid #c9a84c;
//             font-size: 13px;
//             background: #fff;
//             color: #7a5c1e;
//             min-width: 180px;
//             cursor: pointer;
//             font-weight: 600;
//         }

//         /* ── WRAPPER ── */
//         .target-monitor-wrapper {
//             width: 100%;
//             min-height: calc(100vh - 140px);
//             display: flex;
//             flex-direction: column;

//         }

//         /* ── HEADER BAND ── */
//         .tm-header-band {
//             display: flex;
//             justify-content: space-between;
//             align-items: center;
//             background: #fff3d6;
//             border: 2px solid #c9a84c;
//             padding: 18px 28px;
//             border-radius: 16px;
//             margin-bottom: 16px;
//             box-shadow: 0 4px 18px rgba(180,130,0,0.10);
//         }

//         /* ── EMPLOYEE LEFT ── */
//         .tm-emp-left {
//             display: flex;
//             align-items: center;
//             gap: 16px;
//         }

//         .tm-emp-avatar {
//             width: 90px;
//             height: 90px;
//             border-radius: 50%;
//             background: #fde68a;
//             border: 3px solid #c9a84c;
//             display: flex;
//             align-items: center;
//             justify-content: center;
//             font-size: 26px;
//             font-weight: 900;
//             color: #92400e;
//             flex-shrink: 0;
//         }

//         .tm-emp-img {
//             width: 90px;
//             height: 90px;
//             border-radius: 50%;
//             object-fit: cover;
//             border: 3px solid #c9a84c;
//             flex-shrink: 0;
//         }

//         .tm-emp-name {
//             font-size: 22px;
//             font-weight: 800;
//             color: #92400e;
//         }

//         .tm-emp-desig {
//             font-size: 14px;
//             color: #b45309;
//             margin-top: 3px;
//             font-weight: 600;
//         }

//         /* ── TITLE RIGHT ── */
//         .tm-title-right {
//             text-align: right;
//         }

//         .tm-main-title {
//             font-size: 28px;
//             font-weight: 900;
//             color: #7c2d12;
//             letter-spacing: 2px;
//         }

//         .tm-datetime {
//             font-size: 13px;
//             color: #b45309;
//             margin-top: 5px;
//             font-weight: 600;
//         }

//         /* ── SUMMARY LABEL ── */
//         .tm-summary-label {
//             font-size: 13px;
//             font-weight: 800;
//             color: #b45309;
//             letter-spacing: 2px;
//             text-align: right;
//             margin-bottom: 10px;
//         }

//         /* ── SUMMARY CARDS ── */
//         .tm-summary-grid {
//             display: grid;
//             grid-template-columns: repeat(5, 1fr);
//             gap: 12px;
//             margin-bottom: 18px;
//         }

//         .tm-s-card {
//             border-radius: 14px;
//             border: 2px solid #c9a84c;
//             background: #fffde7;
//             padding: 20px 12px;
//             text-align: center;
//             display: flex;
//             flex-direction: column;
//             align-items: center;
//             gap: 8px;
//         }

//         .tm-s-card.tm-s-overdue {
//             background: #fff0f0;
//             border-color: #e57373;
//         }

//         .tm-s-icon {
//             font-size: 28px;
//             color: #c9a84c;
//         }

//         .tm-s-overdue .tm-s-icon {
//             color: #e53935;
//         }

//         .tm-s-label {
//             font-size: 11px;
//             font-weight: 800;
//             color: #b45309;
//             letter-spacing: 1px;
//             line-height: 1.4;
//             text-align: center;
//         }

//         .tm-s-overdue .tm-s-label {
//             color: #c62828;
//         }

//         .tm-s-value {
//             font-size: 34px;
//             font-weight: 900;
//             color: #c9a84c;
//             line-height: 1;
//         }

//         .tm-s-overdue .tm-s-value {
//             color: #e53935;
//         }

//         /* ── TABLE CONTAINER ── */
//         .tm-table-wrap {
//             border-radius: 14px;
//             overflow: hidden;
//             border: 2px solid #c9a84c;
//             width: 100%;
//             padding: 0px !important;
//             margin: 0;
//             display: flex;
//             align-items: stretch;
//         }

//         .slide {
//             width: 100%;
//             height: 100%;
//             margin: 0;
//             padding: 0;
//         }

//         /* ── PERFORMANCE TABLE ── */
//         .tm-perf-table {
//             width: 100%;
//             height: 100%;
//             border-collapse: collapse;
//             table-layout: auto;
//             margin: 0;
//         }

//         .tm-perf-table thead th {
//             background: #c9a84c;
//             color: #fff;
//             padding: 14px 10px;
//             font-size: 14px;
//             font-weight: 800;
//             text-align: center;
//             letter-spacing: 0.5px;
//             border-right: 1px solid #e6c56a;
//             white-space: nowrap;
//         }

//         .tm-perf-table thead th:first-child {
//             background: #a0760c;
//             border-right: 1px solid #c9a84c;
//         }

//         .tm-perf-table tbody tr td {
//             height: 68px;
//         }
//         /* ── ROW LABEL CELLS ── */
//         .tm-lbl-cell {
//             font-weight: 900 !important;
//             font-size: 16px !important;
//             letter-spacing: 1px;
//             color: #fff !important;
//             white-space: nowrap;
//         }

//         .tm-row-mtd td            { background: #fff8f0; }
//         .tm-row-mtd .tm-lbl-cell  { background: #c0392b; }

//         .tm-row-qtd td            { background: #fffde7; }
//         .tm-row-qtd .tm-lbl-cell  { background: #e67e22; }

//         .tm-row-ytd td            { background: #f0fff4; }
//         .tm-row-ytd .tm-lbl-cell  { background: #27ae60; }

//         .tm-row-yol td            { background: #f0f4ff; }
//         .tm-row-yol .tm-lbl-cell  { background: #2980b9; }

//         /* ── TABLE CELLS ── */
//         .tm-perf-table td {
//             padding: 13px 10px;
//             font-size: 14px;
//             text-align: center;
//             border-right: 1px solid #f0d88a;
//             border-bottom: 1px solid #f0d88a;
//             font-weight: 700;
//             white-space: nowrap;
//         }

//         /* ── VALUE COLORS ── */
//         .tm-val-ct  { color: #1a237e; font-weight: 800; }
//         .tm-val-ach { color: #1565c0; font-weight: 800; }
//         .tm-val-yta { color: #5d4037; }
//         .tm-val-sr  { color: #c62828; font-weight: 800; }
//         .tm-val-ep  { color: #0277bd; }
//         .tm-val-nc  { color: #6a1b9a; }
//         .tm-val-tes { color: #c62828; font-weight: 800; }
//         .tm-val-pr  { color: #00695c; }
//         .tm-val-prs { color: #ad1457; font-weight: 800; }
//         .tm-val-idx { font-weight: 900; font-size: 16px; }

//         /* ── PERFORMANCE BADGES ── */
//         .tm-badge {
//             display: inline-block;
//             padding: 5px 14px;
//             border-radius: 20px;
//             font-size: 12px;
//             font-weight: 800;
//             letter-spacing: 0.5px;
//             white-space: nowrap;
//         }

//         .tm-b-outstanding { background: #d4edda; color: #155724; }
//         .tm-b-excellent   { background: #d1ecf1; color: #0c5460; }
//         .tm-b-good        { background: #d4edda; color: #155724; }
//         .tm-b-average     { background: #ede7f6; color: #4527a0; }
//         .tm-b-below       { background: #fde8e8; color: #b71c1c; }

//         /* ── EVENT IMAGE ── */
//         .tm-event-img {
//             max-width: 100%;
//             max-height: 580px;
//             object-fit: contain;
//             border-radius: 18px;
//             border: 2px solid #c9a84c;
//         }

//         /* ── RESPONSIVE ── */
//         @media (max-width: 1200px) {
//             .tm-header-band {
//                 flex-direction: column;
//                 gap: 12px;
//                 text-align: center;
//             }
//             .tm-title-right { text-align: center; }
//             .tm-emp-left    { justify-content: center; }
//             .tm-summary-grid { grid-template-columns: repeat(3, 1fr); }
//         }

//         @media (max-width: 768px) {
//             .tm-summary-grid { grid-template-columns: repeat(2, 1fr); }
//             .tm-perf-table th,
//             .tm-perf-table td { font-size: 12px; padding: 9px 6px; }
//         }
            

//     `).appendTo('head');

//     fetchTargetData(null, null, null);

// };


//blue theme


frappe.pages['target-monitor'].on_page_load = function (wrapper) {
    frappe.breadcrumbs.add("HR");

    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Target Monitor',
        single_column: true
    });

    $(page.body).append(`

        <div class="tm-page-bg">

            <!-- FILTERS -->
            <div class="tm-filter-bar">

                <select id="employeeFilter" class="tm-filter-box">
                    <option value="">All Employees</option>
                </select>

                <select id="departmentFilter" class="tm-filter-box">
                    <option value="">All Departments</option>
                </select>

                <select id="serviceFilter" class="tm-filter-box">
                    <option value="">All Services</option>
                </select>

            </div>

            <div class="target-monitor-wrapper">

                <!-- HEADER BAND -->
                <div class="tm-header-band">

                    <div class="tm-emp-left">
                        <div class="tm-emp-avatar" id="employeeAvatarInitials">--</div>
                        <img id="employeeImage" class="tm-emp-img" style="display:none;" />
                        <div class="tm-emp-text">
                            <div class="tm-emp-name" id="employeeName"></div>
                            <div class="tm-emp-desig" id="employeeDesignation"></div>
                        </div>
                    </div>

                    <div class="tm-title-right">
                        <div class="tm-main-title" id="mainTitle">PERFORMANCE MONITOR</div>
                        <div class="tm-datetime" id="currentMonth"></div>
                    </div>

                </div>

               
                <!-- TABLE AREA -->
                <div id="slideContainer" class="tm-table-wrap" style="margin-left:-30px !important;border-top:none !important;border-bottom:none !important;border-right:none;!important;">
                    <div class="slide" >Fetching Target Data...</div>
                </div>

            </div>
        </div>

    `);


    // ──────────────────────────────────────────
    // FILTERS
    // ──────────────────────────────────────────
    function loadFilters() {

        frappe.call({
            method: "frappe.client.get_list",
            args: { doctype: "Employee", filters: { status: "Active" }, fields: ["name", "employee_name"], limit_page_length: 1000 },
            callback: function(r) {
                (r.message || []).forEach(emp => {
                    $('#employeeFilter').append(`<option value="${emp.name}">${emp.employee_name}</option>`);
                });
            }
        });

        frappe.call({
            method: "frappe.client.get_list",
            args: { doctype: "Department", fields: ["name"], limit_page_length: 1000 },
            callback: function(r) {
                (r.message || []).forEach(dep => {
                    $('#departmentFilter').append(`<option value="${dep.name}">${dep.name}</option>`);
                });
            }
        });

        frappe.call({
            method: "frappe.client.get_list",
            args: { doctype: "Services", fields: ["name"], limit_page_length: 1000 },
            callback: function(r) {
                (r.message || []).forEach(service => {
                    $('#serviceFilter').append(`<option value="${service.name}">${service.name}</option>`);
                });
            }
        });
    }

    loadFilters();

    $('#employeeFilter, #departmentFilter, #serviceFilter').on('change', function () {
        applyFilter();
    });


    // ──────────────────────────────────────────
    // CLOCK
    // ──────────────────────────────────────────
    function displayCurrentMonth() {
        const options = { month: 'long', day: 'numeric', year: 'numeric' };
        const formattedDate = new Date().toLocaleDateString('en-US', options);
        const formattedTime = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
        $('#currentMonth').html(`Date: ${formattedDate} &nbsp;|&nbsp; Time: <span id="currentTime">${formattedTime}</span>`);
    }

    setInterval(() => {
        const t = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
        $('#currentTime').text(t);
    }, 1000);


    // ──────────────────────────────────────────
    // FISCAL YEAR
    // ──────────────────────────────────────────
    function getCurrentFiscalYear() {
        const d = new Date(), m = d.getMonth(), y = d.getFullYear();
        return m >= 3 ? `${y}-${y + 1}` : `${y - 1}-${y}`;
    }


    // ──────────────────────────────────────────
    // FILTER APPLY
    // ──────────────────────────────────────────
    function applyFilter() {
        fetchTargetData(
            $('#employeeFilter').val() || null,
            $('#departmentFilter').val() || null,
            $('#serviceFilter').val() || null
        );
    }


    // ──────────────────────────────────────────
    // PERFORMANCE BADGE HELPER
    // ──────────────────────────────────────────
    function perfBadge(label) {
        const map = {
            'Outstanding': 'tm-b-outstanding',
            'Excellent':   'tm-b-excellent',
            'Good':        'tm-b-good',
            'Average':     'tm-b-average'
        };
        const cls = map[label] || 'tm-b-below';
        return `<span class="tm-badge ${cls}">${label || '-'}</span>`;
    }

    function perfIndexColor(label) {
        return label === 'Outstanding' ? '#1b5e20' :
               label === 'Excellent'   ? '#1565c0' :
               label === 'Good'        ? '#2e7d32' :
               label === 'Average'     ? '#4527a0' : '#c62828';
    }


    // ──────────────────────────────────────────
    // FETCH & RENDER
    // ──────────────────────────────────────────
    let slideInterval = null;

    function fetchTargetData(employee=null, department=null, service=null) {

        if (slideInterval) { clearInterval(slideInterval); slideInterval = null; }

        const fiscalYear = getCurrentFiscalYear();

        Promise.all([
            frappe.call({ method: "teampro.teampro.page.target_monitor.target_monitor.get_slide_attachments" }),
            frappe.call({
                method: "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",
                args: { fiscal_year: fiscalYear, employee, department, service }
            })
        ]).then(([attachmentsResponse, targetsResponse]) => {

            const attachments = attachmentsResponse.message || [];
            const targets     = targetsResponse.message || [];

            let slides = [];

            targets.forEach(t => slides.push(t));

            if (!employee) {
                attachments.forEach(att => slides.push({
                    is_attachment_slide: true,
                    file_url: att.file_url,
                    file_name: att.file_name
                }));
            }

            let index = 0;
            const base = window.location.origin;
            const defaultImg = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg';

            function renderSlide() {

                const slide = slides[index];

                // ── ATTACHMENT SLIDE ──
                if (slide.is_attachment_slide) {

                    $('#mainTitle').html("Today Events &#127881;");
                    $('#employeeAvatarInitials').hide();
                    $('#employeeImage').hide();
                    $('#employeeName').hide();
                    $('#employeeDesignation').hide();

                    $('.slide').html(`
                        <div style="display:flex;justify-content:center;align-items:center;padding:20px;">
                            <img src="${slide.file_url}" class="tm-event-img" />
                        </div>
                    `);

                } else {

                    // ── PERFORMANCE SLIDE ──
                    $('#mainTitle').html("PERFORMANCE MONITOR");
                    $('#employeeName').show();
                    $('#employeeDesignation').show();
                    $('#employeeName').text(slide.employee_name || '');
                    $('#employeeDesignation').text(slide.employee_designation || '');

                    if (slide.employee_image) {
                        $('#employeeImage').attr('src', base + slide.employee_image).show();
                        $('#employeeAvatarInitials').hide();
                    } else {
                        const initials = (slide.employee_name || '--').split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2);
                        $('#employeeAvatarInitials').text(initials).show();
                        $('#employeeImage').hide();
                    }

                    // ── TABLE ──
                    const rows = [
                        {
                            cls: 'tm-row-mtd', rowName: 'MTD',
                            ct:  slide.data.map(i => i.revised_ct || 0).join(', '),
                            ach: slide.data.map(i => i.achieved || 0).join(', '),
                            yta: slide.data.map(i => i.ct_yta || 0).join(', '),
                            sr:  slide.data.map(i => i.mtd_sr || 0).join(', '),
                            ep:  slide.ep || 0,
                            nc:  slide.nc || 0,
                            tes: slide.mtd_tes || 0,
                            pr:  slide.mtd_pr || 0,
                            prs: slide.mtd_prs || 0,
                            idx: slide.mtd_performance_index || 0,
                            perfLabel: slide.mtd_performance_label || ''
                        },
                        {
                            cls: 'tm-row-qtd', rowName: 'QTD',
                            ct:  slide.qtd_target_ct || 0,
                            ach: slide.qtd_achieved || 0,
                            yta: slide.yta_qtd || 0,
                            sr:  slide.qtd_sr || 0,
                            ep:  slide.qtd_ep_score || 0,
                            nc:  slide.qtd_ep_score || 0,
                            tes: slide.qtd_tes || 0,
                            pr:  slide.qtd_pr || 0,
                            prs: slide.qtd_prs || 0,
                            idx: slide.qtd_performance_index || 0,
                            perfLabel: slide.qtd_performance_label || ''
                        },
                        {
                            cls: 'tm-row-ytd', rowName: 'YTD',
                            ct:  slide.ytd_target_ct || 0,
                            ach: slide.ytd_achieved || 0,
                            yta: slide.yta_ytd || 0,
                            sr:  slide.ytd_sr || 0,
                            ep:  slide.ytd_ep_score || 0,
                            nc:  slide.ytd_nc_score || 0,
                            tes: slide.ytd_tes || 0,
                            pr:  slide.ytd_pr || 0,
                            prs: slide.ytd_prs || 0,
                            idx: slide.ytd_performance_index || 0,
                            perfLabel: slide.ytd_performance_label || ''
                        },
                        {
                            cls: 'tm-row-yol', rowName: 'YOL',
                            ct:  slide.annual_ct || 0,
                            ach: slide.yol_ytd_achieved || 0,
                            yta: slide.yol_yta_ytd || 0,
                            sr:  slide.ytd_sr || 0,
                            ep:  slide.yol_ep_score || 0,
                            nc:  slide.yol_nc_score || 0,
                            tes: slide.yol_tes || 0,
                            pr:  slide.yol_pr || 0,
                            prs: slide.yol_prs || 0,
                            idx: slide.yol_performance_index || 0,
                            perfLabel: slide.yol_performance_label || ''
                        }
                    ];

                    const tableRows = rows.map(r => `
                        <tr class="${r.cls}">
                            <td class="tm-lbl-cell">${r.rowName}</td>
                            <td class="tm-val-ct">&#8377;${r.ct}</td>
                            <td class="tm-val-ach">&#8377;${r.ach}</td>
                            <td class="tm-val-yta">&#8377;${r.yta}</td>
                            <td class="tm-val-sr">${r.sr}%</td>
                            <td class="tm-val-ep">${r.ep}</td>
                            <td class="tm-val-nc">${r.nc}</td>
                            <td class="tm-val-tes">${r.tes}%</td>
                            <td class="tm-val-pr">${r.pr}</td>
                            <td class="tm-val-prs">${r.prs}%</td>
                            <td class="tm-val-idx" style="color:${perfIndexColor(r.perfLabel)}">${r.idx}%</td>
                            <td>
                                <span class="tm-badge"
                                    style="
                                        color:${perfIndexColor(r.perfLabel)};
                                        border:2px solid ${perfIndexColor(r.perfLabel)};
                                        background:transparent;
                                    ">
                                    ${r.perfLabel}
                                </span>
                            </td>
                        </tr>
                    `).join('');

                    $('.slide').html(`
                        <table class="tm-perf-table">
                            <thead>
                                <tr>
                                    <th>MONITOR</th>
                                    <th>CT</th>
                                    <th>ACH</th>
                                    <th>YTA</th>
                                    <th>CT_SR</th>
                                    <th>EP</th>
                                    <th>NC</th>
                                    <th>TES (%)</th>
                                    <th>PR</th>
                                    <th>PRS</th>
                                    <th colspan="2">PERFORMANCE INDEX</th>
                                </tr>
                            </thead>
                            <tbody>${tableRows}</tbody>
                        </table>
                    `);
                }

                displayCurrentMonth();
                index = (index + 1) % slides.length;
            }

            renderSlide();

            if (!employee && slides.length > 1) {
                slideInterval = setInterval(renderSlide, 20000);
            }
        });
    }


    // ──────────────────────────────────────────
    // STYLES
    // ──────────────────────────────────────────
    $('<style>').prop('type', 'text/css').html(`

           /* ───────────────── PAGE ───────────────── */
.tm-page-bg{
    padding:10px;
    min-height:100vh;
    font-family:'Poppins',sans-serif;
}



/* ───────────────── FILTERS ───────────────── */
.tm-filter-bar{
    display:flex;
    justify-content:flex-end;   /* right side move */
    gap:10px;
    margin-bottom:14px;
}

/* FILTER BOX SMALL SIZE */
.tm-filter-box{
    width:190px;               /* reduce size */
    height:42px;

    border-radius:10px;
    background:#fff;

    padding:0 14px;

    font-size:13px;
    font-weight:700;

    color:#222;
    outline:none;

}

/* ───────────────── WRAPPER ───────────────── */
.target-monitor-wrapper{
    width:100%;
    display:flex;
    flex-direction:column;
    gap:18px;
}

/* ───────────────── HEADER ───────────────── */
.tm-header-band{
    width:100%;
    position:relative;
    overflow:hidden;

    background:
        radial-gradient(circle at 18% 50%, rgba(255,215,90,0.12) 0%, transparent 18%),
        radial-gradient(circle at 78% 50%, rgba(255,255,255,0.10) 0%, transparent 22%),
        linear-gradient(90deg,
            #041c4a 0%,
            #082f8f 28%,
            #1f63c6 58%,
            #8ea8d8 100%
        );

    border-radius:32px;
    padding:28px 38px;
    display:flex;
    justify-content:space-between;
    align-items:center;

    border:4px solid #b88a1d;

    box-shadow:
    -15px 0 40px rgba(140, 40, 40, 0.38),
    0 0 25px rgba(120, 20, 20, 0.22);
}



/* ───────────────── EMPLOYEE ───────────────── */
.tm-emp-left{
    display:flex;
    align-items:center;
    gap:24px;
    z-index:2;
}

.tm-emp-avatar,
.tm-emp-img{
    width:105px;
    height:105px;
    border-radius:50%;
    border:4px solid #d8ad3d;

    object-fit:cover;
    flex-shrink:0;

    box-shadow:
        0 0 0 8px rgba(216,173,61,0.15),
        0 8px 18px rgba(0,0,0,0.28);
}


.tm-emp-avatar{
    background:linear-gradient(135deg,#143d91,#1f63c6);

    display:flex;
    align-items:center;
    justify-content:center;

    font-size:42px;
    font-weight:800;
    color:#e1b84b;
    font-family:'Georgia',serif;
}

/* EMPLOYEE NAME */
.tm-emp-name{
    font-size:30px;
    font-weight:800;
    color:#ffffff;
    line-height:1;
    letter-spacing:1px;
    text-transform:uppercase;

    text-shadow:0 2px 6px rgba(0,0,0,0.28);
}

/* DESIGNATION */
.tm-emp-desig{
    margin-top:10px;
    font-size:18px;
    font-weight:600;
    color:#d9d9d9;
}
/* ───────────────── TITLE ───────────────── */

.tm-title-right{
    text-align:right;
    z-index:2;
}

.tm-main-title{
    font-size:40px;
    font-weight:900;

    color:#f0c14d;

    text-shadow:
        0 3px 10px rgba(0,0,0,0.35);

    letter-spacing:2px;
    line-height:1;
}

/* DATE TIME */
.tm-datetime{
    margin-top:12px;

    font-size:16px;
    font-weight:600;

    color:#ffffff;
    opacity:0.95;
}

/* ───────────────── TABLE WRAP ───────────────── */
.tm-table-wrap{
    width:100%;
    
    overflow:hidden;
    border:3px solid #d4a62a;
   

    padding:0 !important;
    margin:0 !important;
}

.tm-perf-table{
    width:100%;
    min-width:100%;
    border-collapse:collapse;
    table-layout:auto;
    margin:0;
}

.tm-perf-table thead th:first-child,
.tm-perf-table tbody td:first-child{
    border-left:none !important;
}

.slide{
    width:100%;
}


/* ───────────────── HEADER ───────────────── */
.tm-perf-table thead th{

    background:linear-gradient(
        180deg,
        #d9aa2b 0%,
        #c18b12 100%
    );

    color:#ffffff;

    font-size:17px;
    font-weight:800;

    padding:22px 12px;

    text-align:center;
    white-space:nowrap;

    border:1px solid rgba(255,255,255,0.15);

    text-shadow:0 1px 4px rgba(0,0,0,0.25);
}

.tm-perf-table thead th:first-child{
    background:linear-gradient(180deg,#c48d00,#9f6d00);
}

/* ───────────────── BODY ───────────────── */
.tm-perf-table td{
    padding:24px 12px;
    text-align:center;
    font-size:18px;
    font-weight:700;
    border:1px solid #edd48b;
}

/* ───────────────── LABEL COLUMN ───────────────── */
.tm-lbl-cell{
    color:#fff !important;
    font-size:24px !important;
    font-weight:900 !important;
    letter-spacing:1px;
}

/* ───────────────── ROW COLORS ───────────────── */
.tm-row-mtd td{
    background:#f5f0fb;
}
.tm-row-mtd .tm-lbl-cell{
    background:linear-gradient(135deg,#8a00ff,#cc66ff);
}

.tm-row-qtd td{
    background:#edf5ff;
}
.tm-row-qtd .tm-lbl-cell{
    background:linear-gradient(135deg,#0072ce,#26a6ff);
}

.tm-row-ytd td{
    background:#eefcf4;
}
.tm-row-ytd .tm-lbl-cell{
    background:linear-gradient(135deg,#00a651,#00db67);
}

.tm-row-yol td{
    background:#fff8eb;
}
.tm-row-yol .tm-lbl-cell{
    background:linear-gradient(135deg,#d67b00,#ffbc00);
}

/* ───────────────── VALUE COLORS ───────────────── */
.tm-val-ct{
    color:#1747d1;
    font-weight:800;
}

.tm-val-ach{
    color:#0087a8;
    font-weight:800;
}

.tm-val-yta{
    color:#2f3542;
}

.tm-val-sr{
    color:#ff1f1f;
    font-weight:800;
}

.tm-val-ep{
    color:#005f99;
}

.tm-val-nc{
    color:#7a00ff;
}

.tm-val-tes{
    color:#ff1f1f;
    font-weight:800;
}

.tm-val-pr{
    color:#00695c;
}

.tm-val-prs{
    color:#7c2cff;
    font-weight:800;
}

.tm-val-idx{
    font-weight:900;
    color:#312e81;
}

/* ───────────────── BADGES ───────────────── */
.tm-badge{
    display:inline-block;
    padding:8px 18px;
    border-radius:999px;
    font-size:13px;
    font-weight:800;
    background:#efe3ff;
    color:#7c2cff;
}

/* ───────────────── EVENT IMAGE ───────────────── */
.tm-event-img{
    width:100%;
    max-height:600px;
    object-fit:contain;
    border-radius:18px;
}

/* ───────────────── RESPONSIVE ───────────────── */
@media(max-width:992px){

    .tm-header-band{
        flex-direction:column;
        text-align:center;
        gap:18px;
    }

    .tm-title-right{
        text-align:center;
    }

    .tm-main-title{
        font-size:34px;
    }

    .tm-filter-bar{
        flex-direction:column;
    }
}

@media(max-width:768px){

    .tm-perf-table th,
    .tm-perf-table td{
        font-size:12px;
        padding:10px 6px;
    }

    .tm-lbl-cell{
        font-size:16px !important;
    }

    .tm-emp-name{
        font-size:22px;
    }
}
    `).appendTo('head');

    fetchTargetData(null, null, null);

};








// original


// frappe.pages['target-monitor'].on_page_load = function (wrapper) {
//     frappe.breadcrumbs.add("HR");

//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Target Monitor',
//         single_column: true
//     });

//     $(page.body).append(`

//         <div class="filter-section" style="text-align:right;">

//             <select id="employeeFilter" class="filter-box">
//                 <option value="">All Employees</option>
//             </select>

//             <select id="departmentFilter" class="filter-box">
//                 <option value="">All Departments</option>
//             </select>

//             <select id="serviceFilter" class="filter-box">
//                 <option value="">All Services</option>
//             </select>

//         </div>

//             <div class="target-monitor-wrapper">

//     <!-- HEADER ROW -->
//     <div class="header-section">

//         <!-- LEFT: EMPLOYEE -->
//         <div class="employee-header-left">

//             <img id="employeeImage" class="employee-image-small" />

//             <div class="emp-text">
//                 <h2 id="employeeName"></h2>
//                 <p id="employeeDesignation"></p>
//             </div>

//         </div>

//         <!-- RIGHT: TITLE -->
//         <div class="header-right">

//             <div id="mainTitle" class="main-title">
//                PERFORMANCE MONITOR
//             </div>

//             <div id="currentMonth" class="date-time"></div>

//         </div>

//     </div>

//     <!-- TABLE AREA -->
//     <div id="slideContainer" class="table-container">

//         <div class="slide">
//             Fetching Target Data...
//         </div>

//     </div>

// </div>
//         `);


//     function loadFilters() {

//         // Employee list
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Employee",
//                 filters: {
//                     status: "Active"
//                 },
//                 fields: ["name", "employee_name"],
//                 limit_page_length: 1000
//             },
//             callback: function(r) {
//                 let data = r.message || [];

//                 data.forEach(emp => {
//                     $('#employeeFilter').append(
//                         `<option value="${emp.name}">${emp.employee_name}</option>`
//                     );
//                 });
//             }
//         });

//         // Department list
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Department",
//                 fields: ["name"],
//                 limit_page_length: 1000
//             },
//             callback: function(r) {
//                 let data = r.message || [];

//                 data.forEach(dep => {
//                     $('#departmentFilter').append(
//                         `<option value="${dep.name}">${dep.name}</option>`
//                     );
//                 });
//             }
//         });

//         // Service list
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Services",
//                 fields: ["name"],
//                 limit_page_length: 1000
//             },
//             callback: function(r) {

//                 let data = r.message || [];

//                 data.forEach(service => {

//                     $('#serviceFilter').append(
//                         `<option value="${service.name}">
//                             ${service.name}
//                         </option>`
//                     );

//                 });
//             }
//         });
//     }

//     loadFilters();

//         $('#employeeFilter, #departmentFilter, #serviceFilter').on('change', function () {
//             applyFilter();
//         });

//     let intervalId;

//    function applyFilter() {
//         fetchTargetData(
//             $('#employeeFilter').val() || null,
//             $('#departmentFilter').val() || null,
//              $('#serviceFilter').val() || null
//         );
//     }

//     // CURRENT DATE & TIME
//     function displayCurrentMonth() {

//         const options = {
//             month: 'long',
//             day: 'numeric',
//             year: 'numeric'
//         };

//         const currentDate = new Date();

//         const formattedDate = currentDate.toLocaleDateString(
//             'en-US',
//             options
//         );

//         const formattedTime = currentDate.toLocaleTimeString(
//             'en-US',
//             {
//                 hour: '2-digit',
//                 minute: '2-digit',
//                 second: '2-digit',
//                 hour12: true
//             }
//         );

//         $('#currentMonth').html(`
//             Date: ${formattedDate}
//             |
//             Time:
//             <span id="currentTime">${formattedTime}</span>
//         `);
//     }

//     setInterval(() => {

//         const currentTime = new Date().toLocaleTimeString(
//             'en-US',
//             {
//                 hour: '2-digit',
//                 minute: '2-digit',
//                 second: '2-digit',
//                 hour12: true
//             }
//         );

//         $('#currentTime').text(currentTime);

//     }, 1000);

//     // FISCAL YEAR
//     function getCurrentFiscalYear() {

//         const currentDate = new Date();
//         const month = currentDate.getMonth();
//         const year = currentDate.getFullYear();

//         return month >= 3
//             ? `${year}-${year + 1}`
//             : `${year - 1}-${year}`;
//     }

//     // FETCH DATA
//     let slideInterval = null;
//     function fetchTargetData(employee=null, department=null, service=null) {
//         if (slideInterval) {
//             clearInterval(slideInterval);
//             slideInterval = null;
//         }

//         const fiscalYear = getCurrentFiscalYear();

//         Promise.all([

//             frappe.call({
//                 method:
//                 "teampro.teampro.page.target_monitor.target_monitor.get_slide_attachments"
//             }),
            

//             frappe.call({
//                 method:
//                 "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",

//                 args: {
//                         fiscal_year: fiscalYear,
//                         employee: employee,
//                         department: department,
//                         service: service
//                     },
//             })

//         ]).then(([attachmentsResponse, targetsResponse]) => {

//             const attachments = attachmentsResponse.message || [];
//             const targets = targetsResponse.message || [];
//             let filteredTargets = targets;

//             let slides = [];

//             if (employee) {

//                 // Selected employee only
//                 slides = filteredTargets;

//             } else if (department) {

//                 // Department employees slideshow
//                 filteredTargets.forEach(target => {
//                     slides.push(target);
//                 });

//                 // Add event slides
//                 attachments.forEach(att => {
//                     slides.push({
//                         is_attachment_slide: true,
//                         file_url: att.file_url,
//                         file_name: att.file_name
//                     });
//                 });

//             } else {

//                 // All employees slideshow
//                 filteredTargets.forEach(target => {
//                     slides.push(target);
//                 });

//                 // Add event slides
//                 attachments.forEach(att => {
//                     slides.push({
//                         is_attachment_slide: true,
//                         file_url: att.file_url,
//                         file_name: att.file_name
//                     });
//                 });
//             }

//             let index = 0;
            
//             let isSingleEmployee = employee && !department;
//             function renderSlide() {

//                 const slide = slides[index];

//                 const defaultImg =
//                     '/file/d5fa45439e/878d2ca25auser_default_image.jpeg';

//                 const base = window.location.origin;

//                 // ATTACHMENT SLIDE
//                 if (slide.is_attachment_slide) {

//                     $('#slideContainer')
//                         .removeClass('blinking-container');

//                     $('#mainTitle').html("Today Events 🎉");

//                     $('#employeeImage').hide();
//                     $('#employeeName').hide();
//                     $('#employeeDesignation').hide();

//                     $(".slide").html(`
//                         <div style="
//                             display:flex;
//                             justify-content:center;
//                             align-items:center;
//                             margin-top:-70px;
//                         ">

//                             <img src="${slide.file_url}"
//                                 class="event-image" />

//                         </div>
//                     `);

//                 } else {

//                     $('#slideContainer')
//                         .addClass('blinking-container');

//                     $('#mainTitle').html("PERFORMANCE MONITOR");

//                     $('#employeeImage').show();
//                     $('#employeeName').show();
//                     $('#employeeDesignation').show();

//                     $('#employeeImage').attr(
//                         'src',
//                         slide.employee_image
//                         ? base + slide.employee_image
//                         : defaultImg
//                     );

//                     $('#employeeName')
//                         .text(slide.employee_name || '');

//                     $('#employeeDesignation')
//                         .text(slide.employee_designation || '');

//                     // TABLE CONTENT
//                     let content = `


// <table class="performance-table">

//     <!-- HEADER -->

//     <tr>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             MONITOR
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             CT
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             ACH
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             YTA
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             CT_SR
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             EP
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             NC
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             TES (%)
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             PR
//         </th>

//         <th style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             PRS
//         </th>

//         <th colspan="2" style="
//             background:#0b1e5b;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-size:18px;
//         ">
//             PERFORMANCE INDEX
//         </th>

//     </tr>

//     <!-- MTD -->

//     <tr>

//         <td style="
//             background:#6a1b9a;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             font-size:18px;
//         ">
//             MTD
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right">
//             &#8377;${slide.data.map(item => item.revised_ct || 0).join(', ')}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
//             &#8377;${slide.data.map(item => item.achieved || 0).join(', ')}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;">
//             &#8377;${slide.data.map(item => item.ct_yta || 0).join(', ')}
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             color:red;
//             font-weight:bold;
//         ">
//             ${slide.data.map(item => item.mtd_sr || 0).join(', ')}%
//         </td>

//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.ep || 0}
//         </td>

//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.nc || 0}
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             color:red;
//             font-weight:bold;
//         ">
//             ${slide.mtd_tes || 0}%
//         </td>

//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.mtd_pr || 0}
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             color:red;
//             font-weight:bold;
//         ">
//             ${slide.mtd_prs || 0}%
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.mtd_performance_label == 'Outstanding' ? '#008000' :
//                 slide.mtd_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.mtd_performance_label == 'Good' ? '#43a047' :
//                 slide.mtd_performance_label == 'Average' ? '#9C27B0' :
//                 '#e53935'
//             };
//         ">
//             ${slide.mtd_performance_index || 0}%
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.mtd_performance_label == 'Outstanding' ? '#008000' :
//                 slide.mtd_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.mtd_performance_label == 'Good' ? '#43a047' :
//                 slide.mtd_performance_label == 'Average' ? '#9C27B0' :
//                 '#e53935'
//             };
//         ">
//             ${slide.mtd_performance_label || ''}
//         </td>

//     </tr>

//     <!-- QTD -->

//     <tr>

//         <td style="
//             background:#6a1b9a;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             font-size:18px;
//         ">
//             QTD
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;">
//            &#8377;${slide.qtd_target_ct || 0}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
//             &#8377;${slide.qtd_achieved || 0}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;">
//             &#8377;${slide.yta_qtd || 0}
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             color:red;
//             font-weight:bold;
//         ">
//             ${slide.qtd_sr || 0}%
//         </td>
//          <td style="padding:14px; border:1px solid #999;">
//             ${slide.qtd_ep_score || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.qtd_ep_score || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;color:red;">
//             ${slide.qtd_tes || 0}%
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.qtd_pr || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;color:red;">
//             ${slide.qtd_prs || 0}%
//         </td>
//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.qtd_performance_label == 'Outstanding' ? '#008000' :
//                 slide.qtd_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.qtd_performance_label == 'Good' ? '#43a047' :
//                 slide.qtd_performance_label == 'Average' ? '#9C27B0' :
//                 '#e53935'
//             };
//         ">
//             ${slide.qtd_performance_index || 0}%
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.qtd_performance_label == 'Outstanding' ? '#008000' :
//                 slide.qtd_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.qtd_performance_label == 'Good' ? '#43a047' :
//                 slide.qtd_performance_label == 'Average' ? '#9C27B0' :
//                 '#e53935'
//             };
//         ">
//             ${slide.qtd_performance_label || ''}
//         </td>

        

//     </tr>

//     <!-- YTD -->

//     <tr>

//         <td style="
//             background:#6a1b9a;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             font-size:18px;
//         ">
//             YTD
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;">
//             &#8377;${slide.ytd_target_ct || 0}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
//             &#8377;${slide.ytd_achieved || 0}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;">
//             &#8377;${slide.yta_ytd || 0}
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             color:red;
//             font-weight:bold;
//         ">
//             ${slide.ytd_sr || 0}%
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.ytd_ep_score || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.ytd_nc_score || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;color:red;">
//             ${slide.ytd_tes || 0}%
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.ytd_pr || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;color:red;">
//             ${slide.ytd_prs || 0}%
//         </td>
//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.ytd_performance_label == 'Outstanding' ? '#008000' :
//                 slide.ytd_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.ytd_performance_label == 'Good' ? '#43a047' :
//                 slide.ytd_performance_label == 'Average' ? '#9C27B0' :
//                 '#e53935'
//             };
//         ">
//             ${slide.ytd_performance_index || 0}%
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.ytd_performance_label == 'Outstanding' ? '#008000' :
//                 slide.ytd_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.ytd_performance_label == 'Good' ? '#43a047' :
//                 slide.ytd_performance_label == 'Average' ? '#9C27B0':
//                 '#e53935'
//             };
//         ">
//             ${slide.ytd_performance_label || ''}
//         </td>

//     </tr>

//     <!-- YOL -->

//     <tr>

//         <td style="
//             background:#6a1b9a;
//             color:white;
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             font-size:18px;
//         ">
//             YOL
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;">
//             &#8377;${slide.annual_ct || 0}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
//             &#8377;${slide.yol_ytd_achieved || 0}
//         </td>

//         <td style="padding:14px; border:1px solid #999;text-align:right;">
//             &#8377;${slide.yol_yta_ytd || 0}
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             color:red;
//             font-weight:bold;
//         ">
//             ${slide.ytd_sr || 0}%
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.yol_ep_score || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.yol_nc_score || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;color:red;">
//             ${slide.yol_tes || 0}%
//         </td>
//         <td style="padding:14px; border:1px solid #999;">
//             ${slide.yol_pr || 0}
//         </td>
//         <td style="padding:14px; border:1px solid #999;color:red;">
//             ${slide.yol_prs || 0}%
//         </td>
//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.yol_performance_label == 'Outstanding' ? '#008000' :
//                 slide.yol_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.yol_performance_label == 'Good' ? '#43a047' :
//                 slide.yol_performance_label == 'Average' ? '#9C27B0' :
//                 '#e53935'
//             };
//         ">
//             ${slide.yol_performance_index || 0}%
//         </td>

//         <td style="
//             padding:14px;
//             border:1px solid #999;
//             font-weight:bold;
//             color:${
//                 slide.yol_performance_label == 'Outstanding' ? '#008000' :
//                 slide.yol_performance_label == 'Excellent' ? '#1e88e5' :
//                 slide.yol_performance_label == 'Good' ? '#43a047' :
//                 slide.yol_performance_label == 'Average' ? '#9C27B0' :
//                 '#e53935'
//             };
//         ">
//             ${slide.yol_performance_label || ''}
//         </td>

//     </tr>

// </table>

// </div>
// `;

//                     $(".slide").html(content);
//                 }

//                 displayCurrentMonth();

//                 index = (index + 1) % slides.length;
//             }

//             renderSlide();


//             // Employee selected -> no slideshow
//             if (employee) {
//                 return;
//             }

//             // Department / All Employees -> slideshow
//             if (slides.length > 1) {

//                 slideInterval = setInterval(() => {

//                     renderSlide();

//                 }, 20000);
//             }
//         });
//     }

//     // BLINK EFFECT
//     $('<style>')
//         .prop('type', 'text/css')
//         .html(`
//             body{
//     background:linear-gradient(135deg,#eef4ff,#dce8ff);
//     font-family:'Poppins',sans-serif;
// }

// /* ===================== */
// /* MAIN WRAPPER */
// /* ===================== */

// .target-monitor-wrapper{
//     padding:0px;
//     margin:0px;
// }
// /* ===================== */
// /* HEADER (LEFT EMP + RIGHT TITLE) */
// /* ===================== */

// .header-section{
//     display:flex;
//     justify-content:space-between;
//     align-items:center;
//     background:linear-gradient(90deg,#081c5c,#2348b6);
//     padding:18px 25px;
//     border-radius:20px;
//     margin-bottom:20px;
//     box-shadow:0 10px 25px rgba(0,0,0,0.12);
//     margin-left:60px;
// }

// /* LEFT EMPLOYEE */
// .employee-header-left{
//     display:flex;
//     align-items:center;
//     gap:15px;
// }

// /* EMP IMAGE SMALL */
// .employee-image-small{
//     width:120px;
//     height:120px;
//     border-radius:50%;
//     object-fit:cover;
//     border:3px solid white;
//     box-shadow:0 5px 12px rgba(0,0,0,0.25);
// }

// /* EMP TEXT */
// .emp-text h2{
//     color:white;
//     font-size:24px;
//     font-weight:700;
//     margin:0;
// }

// .emp-text p{
//     color:#dcdcdc;
//     font-size:18px;
//     margin:0;
// }

// /* RIGHT SIDE TITLE */
// .header-right{
//     text-align:right;
// }

// .main-title{
//     font-size:32px;
//     font-weight:800;
//     color:white;
//     letter-spacing:1px;
// }

// .date-time{
//     color:white;
//     font-size:14px;
//     margin-top:5px;
//     opacity:0.9;
// }

// /* ===================== */
// /* TABLE CONTAINER */
// /* ===================== */

// .table-container {
//     flex: 1;
//     width: 100%;
//     margin-right: -10px !important;
//     padding: 0 !important;
//     border-radius: 0 !important;
//     overflow: hidden;
// }

// /* ===================== */
// /* TABLE */
// /* ===================== */

// .performance-table{
//     width:100%;
//     height:400px;
//     border-collapse:collapse;
//     overflow:hidden;
// }

// /* HEADER */
// .performance-table th{
//     background:linear-gradient(90deg,#081c5c,#2348b6);
//     color:white;
//     padding:14px 10px;
//     font-size:19px;
//     font-weight:700;
//     text-align:center;
//     white-space:nowrap;
// }

// /* CELLS */
// .performance-table td{
//     padding:12px 10px;
//     font-size:19px;
//     text-align:center;
//     border-bottom:1px solid #e8ecf7;
//     white-space:nowrap;
//     font-weight:600;
// }




// /* ===================== */
// /* EVENT IMAGE */
// /* ===================== */

// .event-image{
//     width:100%;
//     max-height:700px;
//     object-fit:contain;
//     border-radius:20px;
// }

// /* ===================== */
// /* RESPONSIVE (TV + LAPTOP) */
// /* ===================== */

// @media (max-width:1200px){

//     .header-section{
//         flex-direction:column;
//         gap:10px;
//         text-align:center;
//     }

//     .header-right{
//         text-align:center;
//     }

//     .employee-header-left{
//         justify-content:center;
//     }
// }

// .filter-section{
//     display:flex;
//     gap:15px;
//     justify-content:right;
//     margin-bottom:10px;
// }

// .filter-box{
//     padding:8px;
//     border-radius:6px;
//     border:1px solid #ccc;
//     min-width:200px;
// }

// /* FULL PAGE WIDTH REMOVE LEFT/RIGHT SPACE */

// .layout-main-section {
//     padding: 0 !important;
//     margin: 0 !important;
// }

// .page-body {
//     padding: 0 !important;
//     margin: 0 !important;
// }

// .page-content {
//     padding: 0 !important;
//     margin: 0 !important;
// }

// /* REMOVE BLUE EMPTY AREA BELOW */

// body {
//     background: #ffffff !important;
//     overflow-x: hidden;
// }

// /* TABLE FULL WIDTH */

// .target-monitor-wrapper {
//     width: 100% !important;
//     margin: 0 !important;
//     padding: 0 !important;
// }

// .table-container {
//     width: 100% !important;
//     margin: 0 !important;
//     padding: 0 !important;
// }

// /* REMOVE LEFT WHITE GAP */

// .performance-table {
//     width: 100% !important;
//     margin-left: 0 !important;
//     border-collapse: collapse;
// }

// /* REMOVE FRAPPE PAGE PADDING */

// .layout-main-section-wrapper,
// .layout-main-section,
// .page-body,
// .page-content,
// .main-section {
//     padding: 0 !important;
//     margin: 0 !important;
// }

// /* FULL WIDTH CONTAINER */

// .target-monitor-wrapper{
//     width:100vw !important;
//     max-width:100vw !important;
//     margin:0 !important;
//     padding:0 20px !important;
//     box-sizing:border-box;
// }

// /* TABLE CENTER FIX */

// .table-container{
//     width:100% !important;
//     margin:0 auto !important;
//     padding:0 !important;
//     overflow-x:auto;
// }

// /* TABLE FULL WIDTH */

// .performance-table{
//     width:100% !important;
//     margin:0 !important;
//     table-layout:auto;
//     border-collapse:collapse;
// }

// /* REMOVE BOTTOM BLUE AREA */

// body{
//     background:#fff !important;
//     overflow-x:hidden;
// }

// html, body{
//     margin:0 !important;
//     padding:0 !important;
// }

// /* Alternate Row Colors */

// .performance-table tr:nth-child(even) td {
//     background: #eef4ff;
// }

// .performance-table tr:nth-child(odd) td {
//     background: #ffffff;
// }
          

//         `)
//         .appendTo('head');

//     fetchTargetData(null, null, null);
// };

