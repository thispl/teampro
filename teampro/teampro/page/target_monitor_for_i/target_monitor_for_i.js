
frappe.pages['target-monitor-for-i'].on_page_load = function(wrapper) {
    frappe.breadcrumbs.add("HR");
    let me = this;

    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Target Monitor For Individuals',
        single_column: true
    });

    $(page.body).append(`
        <div id="filtersContainer" style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <div style="flex: 1;">
                <label></label>
                <div id="employeeFilterContainer"></div>
            </div>
            <div style="flex: 1;">
                <label></label>
                <select id="fiscalYearFilter" class="form-control" style="width: 100%; height: calc(1.5em + 0.75rem + 2px);">
                    <option value="">-- Select Fiscal Year --</option>
                    ${generateFiscalYearOptions()}
                </select>
            </div>
            <div style="flex: 1;">
                <label></label>
                <select id="monthFilter" class="form-control" style="width: 100%; height: calc(1.5em + 0.75rem + 2px);">
                    <option value="">-- Select Month --</option>
                    ${generateMonthOptions()}
                </select>
            </div>
            <div style="flex: 1;">
                <label></label>
                <div id="serviceFilterContainer"></div>
            </div>
        </div>
        <div style="margin-bottom: 5px; text-align: center;">
                <div style="font-size: 2.8em;font-weight: bold;class="mt-0"">COMMITED TARGET-CT</div>
                <div id="currentMonth" style="font-size: 2.2em; flex: 1;" class="mt-2"></div>
            </div>
        <div id="slideContainer" style="display: flex; align-items: flex-start;">
            <div class="employee-info" style="margin-right: 20px; text-align: center;">
                <img id="employeeImage" src="" alt="Employee Image" style="width: 100px; height: 100px; margin-bottom: 10px;"/>
                <h4 id="employeeName"></h4>
                <p id="employeeDesignation"></p>
            </div>
            <div style="flex-grow: 1;">
                <div class="slide" style="display: none;"></div>
            </div>
            <div style="flex: 1; text-align: left; display: flex; align-items: center;">
                <div id="currentMonth" style="font-size: 1.5em; margin-bottom: 20px; margin-right: 10px;"></div>
            </div>
        </div>
    `);
    $('#fiscalYearFilter').change(function() {
        fetchTargetData(); // Fetch data for the selected fiscal year, month, and employee
    });
    
    function generateFiscalYearOptions() {
        const currentYear = new Date().getFullYear();
        let options = '';
        for (let i = 0; i < 5; i++) {
            const startYear = currentYear - i;
            const endYear = startYear + 1;
            options += `<option value="${startYear}-${endYear}">${startYear}-${endYear}</option>`;
        }
        return options;
    }
    
    var employeeFilter = new frappe.ui.form.ControlLink({
        parent: $('#employeeFilterContainer'),
        df: {
            fieldtype: "Link",
            options: "Employee",
            placeholder: "Select Employee",
            onchange: function() {
                fetchTargetData(); // Fetch data for the selected employee and month
            }
        },
        render: true
    });

    employeeFilter.refresh();

    $('#monthFilter').change(function() {
        fetchTargetData(); // Fetch data for the selected month and employee
    });
    var serviceFilter = new frappe.ui.form.ControlLink({
        parent: $('#serviceFilterContainer'),
        df: {
            fieldtype: "Link",
            options: "Services",
            placeholder: "Service",
            onchange: function() {
                fetchTargetData(); // Fetch data for the selected service and month
            }
        },
        render: true
    });

    serviceFilter.refresh();
    function generateMonthOptions() {
        const monthFullNames = [
            "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December","January", "February","March"
        ];
        const monthShortNames = [
            "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec","Jan", "Feb", "Mar"
        ];

        return monthFullNames.map((month, index) => `
            <option value="${monthShortNames[index]}">${month}</option>
        `).join('');
    }

    function displaySelectedMonth(selectedMonth) {
        const monthFullNames = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ];
        const monthShortNames = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ];

        const monthIndex = monthShortNames.indexOf(selectedMonth);
        $('#currentMonth').text(`Month: ${monthFullNames[monthIndex]}`);
        
    }

    function displayCurrentMonth() {
        const options = { month: 'long' };
        const currentMonth = new Date().toLocaleDateString('en-US', options);
        // $('#currentMonth').text(currentMonth);
        $('#currentMonth').text(`Month: ${currentMonth}`);
    }

    function fetchTargetData() {
        const selectedEmployee = employeeFilter.get_value();
        const selectedMonth = $('#monthFilter').val();
        const selectedFiscalYear = $('#fiscalYearFilter').val(); 
        const selectedservice =serviceFilter.get_value();
        // Display selected month in UI
        if (selectedMonth) {
            displaySelectedMonth(selectedMonth);
        }
        else {
            // If no month is selected, display the current month
            displayCurrentMonth();
        }
        
        let filters = {
            month: selectedMonth ,// This will now pass the short form of the month
            fiscal_year: selectedFiscalYear
        };
        if (selectedservice){
            filters.services=selectedservice;

            $('#slideContainer').show();
            frappe.call({
                method: "teampro.teampro.page.target_monitor_for_i.target_monitor_for_i.get_target_manager_data_for_services",
                args: {
                    service: selectedservice, // Pass the selected employee ID
                    month: selectedMonth,         // Pass the selected short form month
                    fiscal_year: selectedFiscalYear

                },
                callback: function(response) {
                    console.log("Response message:datas");
                    if (response.message === "No data for that fiscal year for service") {
                        frappe.msgprint({
                            title: __('Information'),
                            message: __('No data is available for that fiscal year for Service'),
                            indicator: 'orange' // Use 'green', 'red', 'orange', or 'blue' for different types of messages
                        });
                    } else if (response.message && response.message.length > 0) {
                        var targetManagerserviceData = response.message;
                        var slideIndex = 0;
                        displaySlide(targetManagerserviceData, slideIndex);
                    }
                }
            });
        }
        else {
            // Hide the slide and employee info container if no employee is selected
            $('#slideContainer').hide();
        }
        if (selectedEmployee) {
            filters.employee = selectedEmployee;

            // Show the slide and employee info container
            $('#slideContainer').show();
            
            frappe.call({
                method: "teampro.teampro.page.target_monitor_for_i.target_monitor_for_i.get_target_manager_data",
                args: {
                    employee: selectedEmployee, // Pass the selected employee ID
                    month: selectedMonth,         // Pass the selected short form month
                    fiscal_year: selectedFiscalYear
                },
                callback: function(response) {
                    console.log("Response message:", response.message);
                    // $('#slideContainer').empty();
                    if (response.message === "No data for that fiscal year for employee") {
                        frappe.msgprint({
                            title: __('Information'),
                            message: __('No data is available for that fiscal year for employee'),
                            indicator: 'orange' // Use 'green', 'red', 'orange', or 'blue' for different types of messages
                        });
                    } else if (response.message && response.message.length > 0) {
                        var targetManagerData = response.message;
                        var slideIndex = 0;
                        displaySlides(targetManagerData, slideIndex);
                    }
                }
            });
        }
        // else {
        //     // Hide the slide and employee info container if no employee is selected
        //     $('#slideContainer').hide();
        // }
    }

    function displaySlides(targetManagerData, index) {
        var slide = targetManagerData[index];
        const defaultImage = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg'; 
        const baseUrl = window.location.origin;
    
        // $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage);
        $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage).css({
            'width': '250px',  // Set your desired width here
            'height': '300px',  // Set your desired height here
            'background-image': 'cover',
            'margin-top': '-70px',
        });
        $('#employeeName').text(slide.employee_name).css({
            'font-size':'20px'
        });
        $('#employeeDesignation').text(slide.employee_designation).css({
            'font-size':'10px'
        });

        
        // Add company information above the table
    
        var slideContent = `
            <div style="margin-bottom: 20px;">
                <table style="width: 100%;height: 300px;margin-top:-70px;border-collapse: collapse;">
                    <tr>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">TARGET</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">MTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">QTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YOL</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;">Target</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.data.map(item => item.revised_ct || '0').join(', ')}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.qtd_target_ct || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.ytd_target_ct || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.annual_ct || '0'}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">Achieved</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.data.map(item => item.achieved || '0').join(', ')}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.qtd_achieved || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.ytd_achieved || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.yol_ytd_achieved || '0'}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;">YTA</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.data.map(item => item.ct_yta || '0').join(', ')}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.yta_qtd || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.yta_ytd || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.yol_yta_ytd || '0'}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;">SR(%)</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.data.map(item => item.mtd_sr || '0').join(', ')}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.qtd_sr || '0'}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.ytd_sr || '0'}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.yol_sr || '0'}%</td>
                    </tr>
                </table>
            </div>
        `;
    
        slideContent += `
            <div style="padding-top: 10px; display: flex; justify-content: space-between;">
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
    
        $('#slideContainer .slide').fadeOut(500, function() {
            $(this).html(slideContent).fadeIn(500);
        });
    }
    // 
    function displaySlide(targetManagerserviceData, index) {
        var slide = targetManagerserviceData[index];
        const defaultImage = '/file/d5fa45439e/878d2ca25auser_default_image.jpeg'; 
        const baseUrl = window.location.origin;
    
        // $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage);
        $('#employeeImage').attr('src', slide.employee_image ? baseUrl + slide.employee_image : defaultImage).css({
            'width': '250px',  // Set your desired width here
            'height': '300px',  // Set your desired height here
            'background-image': 'cover',
            'margin-top': '-70px',
        });

        
        // Add company information above the table
    
        var slideContent = `
            <div style="margin-bottom: 20px;">
                <table style="width: 100%;height: 300px;margin-top:-70px;border-collapse: collapse;">
                    <tr>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">TARGET</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">MTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">QTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YTD</td>
                        <td style="background-color: #0f1568; color: white;border: 1px solid #ccc; padding: 8px;text-align:center">YOL</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;">Target</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.data.map(item => item.revised_ct || '0').join(', ')}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.qtd_target_ct || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.ytd_target_ct || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.annual_ct || '0'}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">Achieved</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.data.map(item => item.achieved || '0').join(', ')}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.qtd_achieved || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.ytd_achieved || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;color:blue;font-size:20px">&#8377;${slide.yol_ytd_achieved || '0'}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;">YTA</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.data.map(item => item.ct_yta || '0').join(', ')}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.yta_qtd || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.yta_ytd || '0'}</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">&#8377;${slide.yol_yta_ytd || '0'}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ccc; padding: 8px;">SR(%)</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.data.map(item => item.mtd_sr || '0').join(', ')}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.qtd_sr || '0'}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.ytd_sr || '0'}%</td>
                        <td style="border: 1px solid #ccc; padding: 8px;">${slide.yol_sr || '0'}%</td>
                    </tr>
                </table>
            </div>
        `;
    
        slideContent += `
            <div style="padding-top: 10px; display: flex; justify-content: space-between;">
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
    
        $('#slideContainer .slide').fadeOut(500, function() {
            $(this).html(slideContent).fadeIn(500);
        });
    }

    fetchTargetData();
    displayCurrentMonth();
};
