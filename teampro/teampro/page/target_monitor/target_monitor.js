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




frappe.pages['target-monitor'].on_page_load = function (wrapper) {
    frappe.breadcrumbs.add("HR");

    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Target Monitor',
        single_column: true
    });

    $(page.body).append(`

        <div class="filter-section" style="text-align:right;">

            <select id="employeeFilter" class="filter-box">
                <option value="">All Employees</option>
            </select>

            <select id="departmentFilter" class="filter-box">
                <option value="">All Departments</option>
            </select>

            <select id="serviceFilter" class="filter-box">
                <option value="">All Services</option>
            </select>

        </div>

            <div class="target-monitor-wrapper">

    <!-- HEADER ROW -->
    <div class="header-section">

        <!-- LEFT: EMPLOYEE -->
        <div class="employee-header-left">

            <img id="employeeImage" class="employee-image-small" />

            <div class="emp-text">
                <h2 id="employeeName"></h2>
                <p id="employeeDesignation"></p>
            </div>

        </div>

        <!-- RIGHT: TITLE -->
        <div class="header-right">

            <div id="mainTitle" class="main-title">
               PERFORMANCE MONITOR
            </div>

            <div id="currentMonth" class="date-time"></div>

        </div>

    </div>

    <!-- TABLE AREA -->
    <div id="slideContainer" class="table-container">

        <div class="slide">
            Fetching Target Data...
        </div>

    </div>

</div>
        `);


    function loadFilters() {

        // Employee list
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Employee",
                filters: {
                    status: "Active"
                },
                fields: ["name", "employee_name"],
                limit_page_length: 1000
            },
            callback: function(r) {
                let data = r.message || [];

                data.forEach(emp => {
                    $('#employeeFilter').append(
                        `<option value="${emp.name}">${emp.employee_name}</option>`
                    );
                });
            }
        });

        // Department list
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Department",
                fields: ["name"],
                limit_page_length: 1000
            },
            callback: function(r) {
                let data = r.message || [];

                data.forEach(dep => {
                    $('#departmentFilter').append(
                        `<option value="${dep.name}">${dep.name}</option>`
                    );
                });
            }
        });

        // Service list
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Services",
                fields: ["name"],
                limit_page_length: 1000
            },
            callback: function(r) {

                let data = r.message || [];

                data.forEach(service => {

                    $('#serviceFilter').append(
                        `<option value="${service.name}">
                            ${service.name}
                        </option>`
                    );

                });
            }
        });
    }

    loadFilters();

        $('#employeeFilter, #departmentFilter, #serviceFilter').on('change', function () {
            applyFilter();
        });

    let intervalId;

   function applyFilter() {
        fetchTargetData(
            $('#employeeFilter').val() || null,
            $('#departmentFilter').val() || null,
             $('#serviceFilter').val() || null
        );
    }

    // CURRENT DATE & TIME
    function displayCurrentMonth() {

        const options = {
            month: 'long',
            day: 'numeric',
            year: 'numeric'
        };

        const currentDate = new Date();

        const formattedDate = currentDate.toLocaleDateString(
            'en-US',
            options
        );

        const formattedTime = currentDate.toLocaleTimeString(
            'en-US',
            {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            }
        );

        $('#currentMonth').html(`
            Date: ${formattedDate}
            |
            Time:
            <span id="currentTime">${formattedTime}</span>
        `);
    }

    setInterval(() => {

        const currentTime = new Date().toLocaleTimeString(
            'en-US',
            {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            }
        );

        $('#currentTime').text(currentTime);

    }, 1000);

    // FISCAL YEAR
    function getCurrentFiscalYear() {

        const currentDate = new Date();
        const month = currentDate.getMonth();
        const year = currentDate.getFullYear();

        return month >= 3
            ? `${year}-${year + 1}`
            : `${year - 1}-${year}`;
    }

    // FETCH DATA
    let slideInterval = null;
    function fetchTargetData(employee=null, department=null, service=null) {
        if (slideInterval) {
            clearInterval(slideInterval);
            slideInterval = null;
        }

        const fiscalYear = getCurrentFiscalYear();

        Promise.all([

            frappe.call({
                method:
                "teampro.teampro.page.target_monitor.target_monitor.get_slide_attachments"
            }),
            

            frappe.call({
                method:
                "teampro.teampro.page.target_monitor.target_monitor.get_ct_ft",

                args: {
                        fiscal_year: fiscalYear,
                        employee: employee,
                        department: department,
                        service: service
                    },
            })

        ]).then(([attachmentsResponse, targetsResponse]) => {

            const attachments = attachmentsResponse.message || [];
            const targets = targetsResponse.message || [];
            let filteredTargets = targets;

            let slides = [];

            if (employee) {

                // Selected employee only
                slides = filteredTargets;

            } else if (department) {

                // Department employees slideshow
                filteredTargets.forEach(target => {
                    slides.push(target);
                });

                // Add event slides
                attachments.forEach(att => {
                    slides.push({
                        is_attachment_slide: true,
                        file_url: att.file_url,
                        file_name: att.file_name
                    });
                });

            } else {

                // All employees slideshow
                filteredTargets.forEach(target => {
                    slides.push(target);
                });

                // Add event slides
                attachments.forEach(att => {
                    slides.push({
                        is_attachment_slide: true,
                        file_url: att.file_url,
                        file_name: att.file_name
                    });
                });
            }

            let index = 0;
            
            let isSingleEmployee = employee && !department;
            function renderSlide() {

                const slide = slides[index];

                const defaultImg =
                    '/file/d5fa45439e/878d2ca25auser_default_image.jpeg';

                const base = window.location.origin;

                // ATTACHMENT SLIDE
                if (slide.is_attachment_slide) {

                    $('#slideContainer')
                        .removeClass('blinking-container');

                    $('#mainTitle').html("Today Events 🎉");

                    $('#employeeImage').hide();
                    $('#employeeName').hide();
                    $('#employeeDesignation').hide();

                    $(".slide").html(`
                        <div style="
                            display:flex;
                            justify-content:center;
                            align-items:center;
                            margin-top:-70px;
                        ">

                            <img src="${slide.file_url}"
                                class="event-image" />

                        </div>
                    `);

                } else {

                    $('#slideContainer')
                        .addClass('blinking-container');

                    $('#mainTitle').html("PERFORMANCE MONITOR");

                    $('#employeeImage').show();
                    $('#employeeName').show();
                    $('#employeeDesignation').show();

                    $('#employeeImage').attr(
                        'src',
                        slide.employee_image
                        ? base + slide.employee_image
                        : defaultImg
                    );

                    $('#employeeName')
                        .text(slide.employee_name || '');

                    $('#employeeDesignation')
                        .text(slide.employee_designation || '');

                    // TABLE CONTENT
                    let content = `


<table class="performance-table">

    <!-- HEADER -->

    <tr>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            MONITOR
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            CT
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            ACH
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            YTA
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            CT_SR
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            EP
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            NC
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            TES (%)
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            PR
        </th>

        <th style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            PRS
        </th>

        <th colspan="2" style="
            background:#0b1e5b;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-size:18px;
        ">
            PERFORMANCE INDEX
        </th>

    </tr>

    <!-- MTD -->

    <tr>

        <td style="
            background:#6a1b9a;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            font-size:18px;
        ">
            MTD
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right">
            &#8377;${slide.data.map(item => item.revised_ct || 0).join(', ')}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
            &#8377;${slide.data.map(item => item.achieved || 0).join(', ')}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;">
            &#8377;${slide.data.map(item => item.ct_yta || 0).join(', ')}
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            color:red;
            font-weight:bold;
        ">
            ${slide.data.map(item => item.mtd_sr || 0).join(', ')}%
        </td>

        <td style="padding:14px; border:1px solid #999;">
            ${slide.ep || 0}
        </td>

        <td style="padding:14px; border:1px solid #999;">
            ${slide.nc || 0}
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            color:red;
            font-weight:bold;
        ">
            ${slide.mtd_tes || 0}%
        </td>

        <td style="padding:14px; border:1px solid #999;">
            ${slide.mtd_pr || 0}
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            color:red;
            font-weight:bold;
        ">
            ${slide.mtd_prs || 0}%
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.mtd_performance_label == 'Outstanding' ? '#008000' :
                slide.mtd_performance_label == 'Excellent' ? '#1e88e5' :
                slide.mtd_performance_label == 'Good' ? '#43a047' :
                slide.mtd_performance_label == 'Average' ? '#9C27B0' :
                '#e53935'
            };
        ">
            ${slide.mtd_performance_index || 0}%
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.mtd_performance_label == 'Outstanding' ? '#008000' :
                slide.mtd_performance_label == 'Excellent' ? '#1e88e5' :
                slide.mtd_performance_label == 'Good' ? '#43a047' :
                slide.mtd_performance_label == 'Average' ? '#9C27B0' :
                '#e53935'
            };
        ">
            ${slide.mtd_performance_label || ''}
        </td>

    </tr>

    <!-- QTD -->

    <tr>

        <td style="
            background:#6a1b9a;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            font-size:18px;
        ">
            QTD
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;">
           &#8377;${slide.qtd_target_ct || 0}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
            &#8377;${slide.qtd_achieved || 0}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;">
            &#8377;${slide.yta_qtd || 0}
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            color:red;
            font-weight:bold;
        ">
            ${slide.qtd_sr || 0}%
        </td>
         <td style="padding:14px; border:1px solid #999;">
            ${slide.qtd_ep_score || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.qtd_ep_score || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;color:red;">
            ${slide.qtd_tes || 0}%
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.qtd_pr || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;color:red;">
            ${slide.qtd_prs || 0}%
        </td>
        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.qtd_performance_label == 'Outstanding' ? '#008000' :
                slide.qtd_performance_label == 'Excellent' ? '#1e88e5' :
                slide.qtd_performance_label == 'Good' ? '#43a047' :
                slide.qtd_performance_label == 'Average' ? '#9C27B0' :
                '#e53935'
            };
        ">
            ${slide.qtd_performance_index || 0}%
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.qtd_performance_label == 'Outstanding' ? '#008000' :
                slide.qtd_performance_label == 'Excellent' ? '#1e88e5' :
                slide.qtd_performance_label == 'Good' ? '#43a047' :
                slide.qtd_performance_label == 'Average' ? '#9C27B0' :
                '#e53935'
            };
        ">
            ${slide.qtd_performance_label || ''}
        </td>

        

    </tr>

    <!-- YTD -->

    <tr>

        <td style="
            background:#6a1b9a;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            font-size:18px;
        ">
            YTD
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;">
            &#8377;${slide.ytd_target_ct || 0}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
            &#8377;${slide.ytd_achieved || 0}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;">
            &#8377;${slide.yta_ytd || 0}
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            color:red;
            font-weight:bold;
        ">
            ${slide.ytd_sr || 0}%
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.ytd_ep_score || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.ytd_nc_score || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;color:red;">
            ${slide.ytd_tes || 0}%
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.ytd_pr || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;color:red;">
            ${slide.ytd_prs || 0}%
        </td>
        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.ytd_performance_label == 'Outstanding' ? '#008000' :
                slide.ytd_performance_label == 'Excellent' ? '#1e88e5' :
                slide.ytd_performance_label == 'Good' ? '#43a047' :
                slide.ytd_performance_label == 'Average' ? '#9C27B0' :
                '#e53935'
            };
        ">
            ${slide.ytd_performance_index || 0}%
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.ytd_performance_label == 'Outstanding' ? '#008000' :
                slide.ytd_performance_label == 'Excellent' ? '#1e88e5' :
                slide.ytd_performance_label == 'Good' ? '#43a047' :
                slide.ytd_performance_label == 'Average' ? '#9C27B0':
                '#e53935'
            };
        ">
            ${slide.ytd_performance_label || ''}
        </td>

    </tr>

    <!-- YOL -->

    <tr>

        <td style="
            background:#6a1b9a;
            color:white;
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            font-size:18px;
        ">
            YOL
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;">
            &#8377;${slide.annual_ct || 0}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;color:blue;">
            &#8377;${slide.yol_ytd_achieved || 0}
        </td>

        <td style="padding:14px; border:1px solid #999;text-align:right;">
            &#8377;${slide.yol_yta_ytd || 0}
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            color:red;
            font-weight:bold;
        ">
            ${slide.ytd_sr || 0}%
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.yol_ep_score || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.yol_nc_score || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;color:red;">
            ${slide.yol_tes || 0}%
        </td>
        <td style="padding:14px; border:1px solid #999;">
            ${slide.yol_pr || 0}
        </td>
        <td style="padding:14px; border:1px solid #999;color:red;">
            ${slide.yol_prs || 0}%
        </td>
        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.yol_performance_label == 'Outstanding' ? '#008000' :
                slide.yol_performance_label == 'Excellent' ? '#1e88e5' :
                slide.yol_performance_label == 'Good' ? '#43a047' :
                slide.yol_performance_label == 'Average' ? '#9C27B0' :
                '#e53935'
            };
        ">
            ${slide.yol_performance_index || 0}%
        </td>

        <td style="
            padding:14px;
            border:1px solid #999;
            font-weight:bold;
            color:${
                slide.yol_performance_label == 'Outstanding' ? '#008000' :
                slide.yol_performance_label == 'Excellent' ? '#1e88e5' :
                slide.yol_performance_label == 'Good' ? '#43a047' :
                slide.yol_performance_label == 'Average' ? '#9C27B0' :
                '#e53935'
            };
        ">
            ${slide.yol_performance_label || ''}
        </td>

    </tr>

</table>

</div>
`;

                    $(".slide").html(content);
                }

                displayCurrentMonth();

                index = (index + 1) % slides.length;
            }

            renderSlide();


            // Employee selected -> no slideshow
            if (employee) {
                return;
            }

            // Department / All Employees -> slideshow
            if (slides.length > 1) {

                slideInterval = setInterval(() => {

                    renderSlide();

                }, 20000);
            }
        });
    }

    // BLINK EFFECT
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            body{
    background:linear-gradient(135deg,#eef4ff,#dce8ff);
    font-family:'Poppins',sans-serif;
}

/* ===================== */
/* MAIN WRAPPER */
/* ===================== */

.target-monitor-wrapper{
    padding:0px;
    margin:0px;
}
/* ===================== */
/* HEADER (LEFT EMP + RIGHT TITLE) */
/* ===================== */

.header-section{
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:linear-gradient(90deg,#081c5c,#2348b6);
    padding:18px 25px;
    border-radius:20px;
    margin-bottom:20px;
    box-shadow:0 10px 25px rgba(0,0,0,0.12);
    margin-left:60px;
}

/* LEFT EMPLOYEE */
.employee-header-left{
    display:flex;
    align-items:center;
    gap:15px;
}

/* EMP IMAGE SMALL */
.employee-image-small{
    width:120px;
    height:120px;
    border-radius:50%;
    object-fit:cover;
    border:3px solid white;
    box-shadow:0 5px 12px rgba(0,0,0,0.25);
}

/* EMP TEXT */
.emp-text h2{
    color:white;
    font-size:24px;
    font-weight:700;
    margin:0;
}

.emp-text p{
    color:#dcdcdc;
    font-size:18px;
    margin:0;
}

/* RIGHT SIDE TITLE */
.header-right{
    text-align:right;
}

.main-title{
    font-size:32px;
    font-weight:800;
    color:white;
    letter-spacing:1px;
}

.date-time{
    color:white;
    font-size:14px;
    margin-top:5px;
    opacity:0.9;
}

/* ===================== */
/* TABLE CONTAINER */
/* ===================== */

.table-container {
    flex: 1;
    width: 100%;
    margin-right: -10px !important;
    padding: 0 !important;
    border-radius: 0 !important;
    overflow: hidden;
}

/* ===================== */
/* TABLE */
/* ===================== */

.performance-table{
    width:100%;
    height:400px;
    border-collapse:collapse;
    overflow:hidden;
}

/* HEADER */
.performance-table th{
    background:linear-gradient(90deg,#081c5c,#2348b6);
    color:white;
    padding:14px 10px;
    font-size:19px;
    font-weight:700;
    text-align:center;
    white-space:nowrap;
}

/* CELLS */
.performance-table td{
    padding:12px 10px;
    font-size:19px;
    text-align:center;
    border-bottom:1px solid #e8ecf7;
    white-space:nowrap;
    font-weight:600;
}




/* ===================== */
/* EVENT IMAGE */
/* ===================== */

.event-image{
    width:100%;
    max-height:700px;
    object-fit:contain;
    border-radius:20px;
}

/* ===================== */
/* RESPONSIVE (TV + LAPTOP) */
/* ===================== */

@media (max-width:1200px){

    .header-section{
        flex-direction:column;
        gap:10px;
        text-align:center;
    }

    .header-right{
        text-align:center;
    }

    .employee-header-left{
        justify-content:center;
    }
}

.filter-section{
    display:flex;
    gap:15px;
    justify-content:right;
    margin-bottom:10px;
}

.filter-box{
    padding:8px;
    border-radius:6px;
    border:1px solid #ccc;
    min-width:200px;
}

/* FULL PAGE WIDTH REMOVE LEFT/RIGHT SPACE */

.layout-main-section {
    padding: 0 !important;
    margin: 0 !important;
}

.page-body {
    padding: 0 !important;
    margin: 0 !important;
}

.page-content {
    padding: 0 !important;
    margin: 0 !important;
}

/* REMOVE BLUE EMPTY AREA BELOW */

body {
    background: #ffffff !important;
    overflow-x: hidden;
}

/* TABLE FULL WIDTH */

.target-monitor-wrapper {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

.table-container {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* REMOVE LEFT WHITE GAP */

.performance-table {
    width: 100% !important;
    margin-left: 0 !important;
    border-collapse: collapse;
}

/* REMOVE FRAPPE PAGE PADDING */

.layout-main-section-wrapper,
.layout-main-section,
.page-body,
.page-content,
.main-section {
    padding: 0 !important;
    margin: 0 !important;
}

/* FULL WIDTH CONTAINER */

.target-monitor-wrapper{
    width:100vw !important;
    max-width:100vw !important;
    margin:0 !important;
    padding:0 20px !important;
    box-sizing:border-box;
}

/* TABLE CENTER FIX */

.table-container{
    width:100% !important;
    margin:0 auto !important;
    padding:0 !important;
    overflow-x:auto;
}

/* TABLE FULL WIDTH */

.performance-table{
    width:100% !important;
    margin:0 !important;
    table-layout:auto;
    border-collapse:collapse;
}

/* REMOVE BOTTOM BLUE AREA */

body{
    background:#fff !important;
    overflow-x:hidden;
}

html, body{
    margin:0 !important;
    padding:0 !important;
}

/* Alternate Row Colors */

.performance-table tr:nth-child(even) td {
    background: #eef4ff;
}

.performance-table tr:nth-child(odd) td {
    background: #ffffff;
}
          

        `)
        .appendTo('head');

    fetchTargetData(null, null, null);
};

