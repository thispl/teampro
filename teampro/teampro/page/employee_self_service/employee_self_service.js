frappe.pages['employee-self-service'].on_page_load = function (wrapper) {



	frappe.require("/assets/teampro/css/tailwind.css");
	frappe.require("https://cdn.jsdelivr.net/npm/chart.js");




	let employee_data = {
		name: "Administrator",
		image: "https://i.postimg.cc/ryxWSm4x/no-profile-img.jpg",
		employee_name: "----",
		status: "----",
		department: "----",
		designation: "----",
		phone: "----",
		email: "-----",
		date_of_birth: "----",
		gender: "----",
		date_of_joining: "----",
		age: "----",
		emergency_contact_name: "----",
		emergency_phone: "-----",
		relation: "----",
		employment_type: "----",
		grade: "----",
		company: "----",
		branch: "----",
		company_email: "-----",
	};

	let attendance_data = {
		name: "----",
		attendance_date: "----",
		in_time: "----",
		out_time: "----",
		status: "----",
		department: "----",
		designation: "----",
		shift: "----",
	}

	let approval_data = {
		expense: [],
		leave: [],
		shift: []
	};

	let permission_data = [];


	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Employee Self Service',
		single_column: true
	});






	$(page.main).empty().html(`
        <div class="flex h-screen overflow-hidden bg-gray-100 relative">

            <!-- Sidebar (Persistent) -->
            <div class=" !hidden md:!block flex flex-col  w-[100px] bg-[#1d2551] items-center py-4 space-y-8 text-white " >

                <div class="nav-item cursor-pointer p-2 flex flex-col items-center" data-target="home">
					<div class="icon-box p-2 transition-all duration-200">
						<img src="https://i.postimg.cc/kXGsT2Zg/home.png" class="w-9 h-9 object-contain" />
					</div>
                    <div class="text-xs mt-1">Home</div>
                </div>

                <div class="nav-item cursor-pointer p-2 flex flex-col items-center" data-target="checkin">
					<div class="icon-box p-2 transition-all duration-200">
						<img src="https://i.postimg.cc/hP9fPLPp/point.png" class="w-9 h-9 object-contain" />
					</div>
                    <div class="text-xs mt-1">Check In</div>
                </div>

                <div class="nav-item cursor-pointer p-2 flex flex-col items-center" data-target="leave">
				 <div class="icon-box p-2 transition-all duration-200">
                    <img src="https://i.postimg.cc/L65DxJ7s/calendar.png" class="w-9 h-9 object-contain" />
				 </div>
                    <div class="text-xs text-center mt-1">Leave Tracker</div>
                </div>

                <div class="nav-item cursor-pointer p-2 flex flex-col items-center " data-target="recruitment">
				 <div class="icon-box p-2 transition-all duration-200">
                    <img src="https://i.postimg.cc/65P0g9Jx/recruitment.png" class="w-9 h-9 object-contain" />
				 </div>	
                    <div class="text-xs text-center mt-1">Recruitment & Performance</div>
                </div>

            </div>

            


            <!-- Content Area (Dynamic) -->
            <div id="ess-content-root" class="flex-1 overflow-y-auto ">
            </div>


			<!-- Bottom Bar (mobile only) -->
		<div class="!flex md:!hidden fixed bottom-0 left-0 right-0 flex-row w-full h-[75px] bg-[#1d2551] items-center justify-around text-white z-50">
			<div class="nav-item cursor-pointer p-2 flex flex-col items-center" data-target="home">
				<div class="icon-box p-2 transition-all duration-200">
					<img src="https://i.postimg.cc/kXGsT2Zg/home.png" class="w-7 h-7 object-contain" />
				</div>
				<div class="text-[10px] mt-1">Home</div>
			</div>
			<div class="nav-item cursor-pointer p-2 flex flex-col items-center" data-target="checkin">
				<div class="icon-box p-2 transition-all duration-200">
					<img src="https://i.postimg.cc/hP9fPLPp/point.png" class="w-7 h-7 object-contain" />
				</div>
				<div class="text-[10px] mt-1">Check In</div>
			</div>
			<div class="nav-item cursor-pointer p-2 flex flex-col items-center" data-target="leave">
				<div class="icon-box p-2 transition-all duration-200">
					<img src="https://i.postimg.cc/L65DxJ7s/calendar.png" class="w-7 h-7 object-contain" />
				</div>
				<div class="text-[10px] text-center mt-1">Leave Tracker</div>
			</div>
			<div class="nav-item cursor-pointer p-2 flex flex-col items-center" data-target="recruitment">
				<div class="icon-box p-2 transition-all duration-200">
					<img src="https://i.postimg.cc/65P0g9Jx/recruitment.png" class="w-7 h-7 object-contain" />
				</div>
				<div class="text-[10px] text-center mt-1">Recruitment</div>
			</div>
		</div>





        </div>
    `);

	const getWeatherIcon = (condition) => {
		const icons = {
			'Clear': 'https://i.postimg.cc/jSQ6QF05/sun.png',
			'Clouds': 'https://i.postimg.cc/wjc5cG8M/cloudy.png',
			'Rain': 'https://i.postimg.cc/8zBdB0QJ/storm.png',
			'Snow': 'https://i.postimg.cc/jSQ6QF0D/snow.png',
			'Drizzle': 'https://i.postimg.cc/MK0fhfsR/drizzle.png'
		};
		return icons[condition] || icons['Clear'];
	};




	const fetchWeather = async () => {
		return new Promise((resolve) => {

			if (!navigator.geolocation) {
				console.error("Geolocation is not supported by this browser.");
				return resolve({ temp: "--", condition: 'Clear', location: '--' });
			}

			navigator.geolocation.getCurrentPosition(
				async (position) => {


					const lat = position.coords.latitude;
					const lon = position.coords.longitude;
					const apiKey = "f117ac4a10b6abbe61a8f3b01d688521";

					try {
						const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}`);
						const data = await response.json();

						console.log("Weather API Response:", data);
						resolve({
							temp: Math.round(data.main.temp),
							condition: data.weather[0].main,
							location: data.name
						});
					} catch (e) {
						console.error("Fetch Error:", e);
						resolve({ temp: "--", condition: 'Clear', location: '--' });
					}
				},
				(error) => {

					resolve({ temp: "--", condition: 'Clear', location: '--' });
				},
				{
					enableHighAccuracy: true,
					timeout: 5000,
					maximumAge: 0
				}
			);
		});
	};


	const render_component = (target) => {
		const $root = $(page.main).find('#ess-content-root');
		$root.empty();

		if (target === 'home') {
			$root.html(`
				<div class=" home-nav-bar bg-white h-12 p-[6px] pl-3 pb-0 shadow-md rounded-xs mt-0 mx-0 flex items-center justify-start gap-10 ">

					<!-- Dashboard -->
					<div class=" home-nav-bar-item cursor-pointer text-[20px] text-black-500 pt-1   font-bold" data-target="dashboard">
						<p class="text-[16px] mb-[4px]">Dashboard</p>
						<div class="home-nav-bar-item-selector bg-blue-500 rounded-full  "></div>
					</div>

					<!-- Employee Profile -->
					<div class=" home-nav-bar-item cursor-pointer text-[20px] text-black-500 text-sm pt-1  font-bold" data-target="employee-profile">
						<p class="text-[16px] mb-[4px]">Employee Profile</p>
						<div class="home-nav-bar-item-selector bg-blue-500 rounded-full  "></div>
					</div>

				</div>

				<div id="home-content-area" class="home-content-area bg-[#edeef3]  w-full min-h-[2300px]  md:!min-h-[1000px] mt-2 shadow-sm relative pb-[100px] " >	
				</div>

				
				`);

			render_home_page_component('dashboard');
			const $dashboardSubNav = $(page.main).find('.home-nav-bar-item[data-target="dashboard"]');
			$dashboardSubNav.find('.home-nav-bar-item-selector').addClass("w-full h-[3px]");
		}


		else if (target === 'leave') {

			$root.html(`
        <div class="leave-tracker-container p-6 bg-[#edeef3] min-h-full">

            <!-- Header -->
            <div class="flex  justify-between md:items-center items-start mb-8">
                <div class=" flex flex-col md:flex-row gap-2 md:gap-8  ">
                    <div class="flex flex-col">
                        <span class="text-[12px] md:text-xs font-semibold text-gray-500 uppercase tracking-wider">Total Leave booked</span>
                        <span class="text-2xl font-bold text-gray-800" id="booked-count">0 Days</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[12px] md:text-xs font-semibold text-gray-500 uppercase tracking-wider">Absent</span>
                        <span class="text-2xl font-bold text-red-600" id="absent-count">0</span>
                    </div>
                </div>
                <button
                    onclick="frappe.set_route('List', 'Leave Application', 'List')"
                    class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white md:px-5 px-3 md:py-2.5 py-1.5 rounded-lg  font-small md:font-medium transition-all shadow-sm active:scale-95">
                    <i class="fa fa-plus text-xs"></i> Apply Leave
                </button>
            </div>

            <!-- Leave Balance Cards -->
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 mb-8" id="leave-balance-container">
                <!-- skeleton -->
                <div class="animate-pulse bg-white p-4 rounded-xl border border-gray-100 flex flex-col items-center gap-3">
                    <div class="rounded-full bg-gray-200 h-20 w-20"></div>
                    <div class="h-3 bg-gray-200 rounded w-3/4"></div>
                    <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
            </div>

            <!-- Bottom: Pending Leave Requests + Holidays -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-[100px]">

                <!-- Pending Leave Requests -->
                <div class="lg:col-span-2 bg-white rounded-xl border border-gray-200 shadow-sm p-5">
                    <div class="flex items-center justify-between mb-4">
                        <h5 class="text-base font-bold text-gray-800" id="cal-month-label">Pending Leave Requests</h5>
                    </div>

					<div id="pending-leave-list-container" class="h-[250px] overflow-y-auto pr-2">
						<div class="text-gray-300 text-sm text-center mt-12">No Pending Leave Requests</div>
					</div>

                    
                </div>

                <!-- Upcoming Holidays -->
                <div class="bg-white rounded-xl border border-gray-200 h-[450px]  shadow-sm p-5 flex flex-col">
                    <h6 class="text-base font-bold text-gray-800 mb-4">
                        <i class="fa fa-sun-o text-amber-400 mr-1"></i> Upcoming Holidays
                    </h6>
                    <div id="holiday-list" class="flex flex-col gap-3 flex-1 overflow-y-auto">
                        <div class="text-gray-300 text-sm text-center mt-12">Loading...</div>
                    </div>
                </div>

            </div>
        </div>
    `);


			let calYear = new Date().getFullYear();
			let calMonth = new Date().getMonth();
			let leaveMap = {};
			let holidaySet = {};

			const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
				'July', 'August', 'September', 'October', 'November', 'December'];

			function buildLeaveMap(leaves) {
				leaveMap = {};
				leaves.forEach(lv => {
					let cur = new Date(lv.from_date);
					const end = new Date(lv.to_date);
					while (cur <= end) {
						const key = cur.toISOString().slice(0, 10);
						leaveMap[key] = { status: lv.status, leave_type: lv.leave_type };
						cur.setDate(cur.getDate() + 1);
					}
				});
			}

			function renderCalendar() {
				const label = document.getElementById('cal-month-label');
				const grid = document.getElementById('cal-grid');
				const todayKey = new Date().toISOString().slice(0, 10);

				if (!label || !grid) return;

				label.textContent = `${MONTHS[calMonth]} ${calYear}`;
				grid.innerHTML = '';

				const firstDay = new Date(calYear, calMonth, 1).getDay();
				const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();


				for (let i = 0; i < firstDay; i++) {
					grid.insertAdjacentHTML('beforeend', `<div></div>`);
				}

				for (let d = 1; d <= daysInMonth; d++) {
					const mm = String(calMonth + 1).padStart(2, '0');
					const dd = String(d).padStart(2, '0');
					const key = `${calYear}-${mm}-${dd}`;

					const isToday = key === todayKey;
					const leaveInfo = leaveMap[key];
					const holDesc = holidaySet[key];
					const dow = new Date(calYear, calMonth, d).getDay();
					const isWeekend = dow === 0 || dow === 6;

					let cellStyle = `
			    display:flex;align-items:center;justify-content:center;
			    height:36px;border-radius:8px;font-size:13px;
			    position:relative;cursor:default;
			`;
					let textColor = isWeekend ? '#94a3b8' : '#374151';
					let dotColor = '';
					let title = '';

					if (isToday) {
						cellStyle += 'background:#eff6ff;border:1px solid #93c5fd;font-weight:600;';
						textColor = '#1d4ed8';
					} else if (leaveInfo) {
						const isApproved = leaveInfo.status === 'Approved';
						cellStyle += isApproved
							? 'background:#dbeafe;'
							: 'background:#fef3c7;';
						textColor = isApproved ? '#1e40af' : '#92400e';
						dotColor = isApproved ? '#3b82f6' : '#f59e0b';
						title = `${leaveInfo.leave_type} (${leaveInfo.status})`;
					} else if (holDesc) {
						cellStyle += 'background:#fee2e2;';
						textColor = '#991b1b';
						dotColor = '#f87171';
						title = holDesc;
					}


					grid.insertAdjacentHTML('beforeend', `
			    <div style="${cellStyle}color:${textColor}" title="${title}">
			        ${d}
			        ${dotColor ? `<span style="position:absolute;bottom:3px;left:50%;transform:translateX(-50%);
			            width:4px;height:4px;border-radius:50%;background:${dotColor}"></span>` : ''}
			    </div>
			`);
				}
			}

			function renderHolidays(holidays) {
				const list = document.getElementById('holiday-list');
				if (!list) return;

				if (!holidays.length) {
					list.innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                            flex:1;text-align:center;padding:2rem 0;">
                    <div style="width:56px;height:56px;border-radius:50%;background:#fef3c7;
                                display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                        <i class="fa fa-calendar-o" style="font-size:24px;color:#f59e0b;"></i>
                    </div>
                    <p style="color:#9ca3af;font-size:13px;font-weight:500;margin:0;">No upcoming holidays</p>
                    <p style="color:#d1d5db;font-size:12px;margin:4px 0 0;">Enjoy your workdays!</p>
                </div>`;
					return;
				}

				list.innerHTML = holidays.map(h => {
					const date = new Date(h.date);
					const day = date.toLocaleDateString('en-IN', { weekday: 'short' });
					const dd = date.getDate();
					const mon = date.toLocaleDateString('en-IN', { month: 'short' });
					return `
                <div style="display:flex;align-items:center;gap:12px;padding:8px 10px;
                            border-radius:10px;transition:background 0.15s;"
                     onmouseover="this.style.background='#f9fafb'"
                     onmouseout="this.style.background='transparent'">
                    <div style="min-width:44px;height:44px;border-radius:10px;background:#fef3c7;
                                display:flex;flex-direction:column;align-items:center;
                                justify-content:center;flex-shrink:0;">
                        <span style="font-size:14px;font-weight:700;color:#d97706;line-height:1">${dd}</span>
                        <span style="font-size:10px;color:#f59e0b;line-height:1;margin-top:2px">${mon}</span>
                    </div>
                    <div style="flex:1;min-width:0;">
                        <p style="font-size:13px;font-weight:600;color:#374151;margin:0;
                                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                            ${h.description}
                        </p>
                        <p style="font-size:11px;color:#9ca3af;margin:2px 0 0;">${day}</p>
                    </div>
                </div>`;
				}).join('');
			}

			frappe.call({
				method: "teampro.api.employee_self_service.get_pending_leave_requests",
				callback: (r) => {
					const pending_leave_requests = r.message || [];
					renderPendingLeaveRequests(pending_leave_requests);
				}
			});

			function renderPendingLeaveRequests(pending_leave_requests) {

				const container = $('#pending-leave-list-container');
				container.empty();

				if (!pending_leave_requests || pending_leave_requests.length === 0) {
					container.append(`
                <div style="padding:20px;text-align:center;color:#9ca3af;">
                    No pending leave requests
                </div>
            `);
					return;
				}

				pending_leave_requests.forEach(leave => {
					container.append(`
                <div onclick="frappe.set_route('Form', 'Leave Application', '${leave.name}')" style="display:flex;align-items:center;gap:12px;padding:8px 10px;
                            border-radius:10px;transition:background 0.15s;"
                     onmouseover="this.style.background='#f9fafb'"
                     onmouseout="this.style.background='transparent'" class="cursor-pointer">
                    <div style="min-width:44px;height:44px;border-radius:10px;background:#fef3c7;
                                display:flex;flex-direction:column;align-items:center;
                                justify-content:center;flex-shrink:0;">
                        <span style="font-size:14px;font-weight:700;color:#d97706;line-height:1">${leave.days}</span>
                        <span style="font-size:10px;color:#f59e0b;line-height:1;margin-top:2px">days</span>
                    </div>
                    <div style="flex:1;min-width:0;">
                        <p style="font-size:13px;font-weight:600;color:#374151;margin:0;
                                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                            ${leave.leave_type}
                        </p>
                        <p style="font-size:11px;color:#9ca3af;margin:2px 0 0;">
                            ${frappe.format(leave.from_date, { "fieldtype": "Date" })} to ${frappe.format(leave.to_date, { "fieldtype": "Date" })}
                        </p>
                    </div>
                </div>
            `);
				});

			}


			$root.on('click', '#cal-prev', () => {
				if (calMonth === 0) { calMonth = 11; calYear--; }
				else calMonth--;
				renderCalendar();
			});

			$root.on('click', '#cal-next', () => {
				if (calMonth === 11) { calMonth = 0; calYear++; }
				else calMonth++;
				renderCalendar();
			});


			frappe.call({
				method: "teampro.api.employee_self_service.get_leave_summary",
				callback: (r) => {
					if (!r.message) return;

					const container = $('#leave-balance-container');
					container.empty();

					let totalBooked = 0;
					const R = 30, CX = 40, CY = 40;
					const circ = 2 * Math.PI * R;

					r.message.forEach(leave => {
						const color = leave.color || '#378ADD';
						const total = (leave.available || 0) + (leave.booked || 0);
						totalBooked += (leave.booked || 0);

						const pct = total > 0 ? Math.max(0, Math.min(1, leave.available / total)) : 0;
						const dash = (pct * circ).toFixed(1);

						container.append(`
							<div class="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md
										transition-shadow p-4 flex flex-col items-center gap-2 relative">

								<i class="fa fa-info-circle absolute top-2 right-2 text-gray-300
										hover:text-blue-400 cursor-pointer text-sm leave-policy-info"
								data-policy="${(leave.policy_details || '').replace(/"/g, '&quot;')}"
								data-leave="${leave.leave_type}"></i>

								<div style="position:relative;width:80px;height:80px;">
									<svg viewBox="0 0 80 80" width="80" height="80" style="transform:rotate(-90deg)">
										<circle cx="${CX}" cy="${CY}" r="${R}" fill="none"
												stroke="#f1f5f9" stroke-width="10"/>
										<circle cx="${CX}" cy="${CY}" r="${R}" fill="none"
												stroke="${color}" stroke-width="10"
												stroke-dasharray="${dash} ${circ.toFixed(1)}"
												stroke-linecap="round"/>
									</svg>
									<div style="position:absolute;inset:0;display:flex;flex-direction:column;
												align-items:center;justify-content:center;">
										<span style="font-size:20px;font-weight:600;color:${color};line-height:1">
											${leave.available}
										</span>
										<span style="font-size:9px;color:#94a3b8;text-transform:uppercase;
													letter-spacing:0.05em">avail</span>
									</div>
								</div>

								<span style="font-size:12px;font-weight:600;color:#374151;text-align:center;
											line-height:1.3">${leave.leave_type}</span>
								<span style="font-size:11px;color:#9ca3af;background:#f3f4f6;
											padding:2px 10px;border-radius:999px;">
									Booked: ${leave.booked}
								</span>
							</div>
						`);



					});

					$('#booked-count').text(totalBooked + ' Days');

					$('#leave-balance-container').off('click', '.leave-policy-info')
						.on('click', '.leave-policy-info', function (e) {

							e.stopPropagation();

							const $el = $(this);

							$('.leave-policy-info').not($el).popover('hide');

							if (!$el.data('bs.popover')) {
								$el.popover({
									title: `<strong>${$el.data('leave')}</strong> — Policy`,
									content: $el.data('policy'),
									placement: 'top',
									trigger: 'manual',
									html: true,
									container: 'body'
								});
							}


							$el.popover('toggle');

							$(document).one('click', function (e) {
								if (!$(e.target).closest('.popover, .leave-policy-info').length) {
									$('.leave-policy-info').popover('hide');
								}
							});


						});




				}
			});


			frappe.call({
				method: "teampro.api.employee_self_service.get_leave_calendar",
				callback: (r) => {
					buildLeaveMap(r.message || []);
					renderCalendar();
				}
			});


			frappe.call({
				method: "teampro.api.employee_self_service.get_all_holidays",
				callback: (r) => {
					(r.message || []).forEach(h => { holidaySet[h.date] = h.description; });
					renderCalendar();
				}
			});


			frappe.call({
				method: "teampro.api.employee_self_service.get_upcoming_holidays",
				callback: (r) => {
					const holidays = r.message || [];
					holidays.forEach(h => { holidaySet[h.date] = h.description; });
					renderCalendar();
					renderHolidays(holidays);
				}
			});



			frappe.call({
				method: "teampro.api.employee_self_service.get_absent_count",
				callback: (r) => {
					$('#absent-count').text(r.message || 0);
				}
			});


		}

		else if (target === 'recruitment') {

			$root.html(`
        <div class="recruitment-container bg-[#edeef3] min-h-full">

            <!-- Sub Nav -->
            <div class="bg-white h-12 px-6 shadow-sm flex items-center gap-8 border-b border-gray-100">
                <div class="rec-nav-item cursor-pointer flex flex-col items-center pt-3" data-tab="openings">
                    <span class="text-[14px] font-bold text-gray-700">Job Openings</span>
                    <div class="rec-nav-selector mt-2 h-[3px] rounded-full bg-blue-500 w-0 transition-all duration-200"></div>
                </div>
                <div class="rec-nav-item cursor-pointer flex flex-col items-center pt-3" data-tab="appraisals">
                    <span class="text-[14px] font-bold text-gray-700">Appraisals</span>
                    <div class="rec-nav-selector mt-2 h-[3px] rounded-full bg-blue-500 w-0 transition-all duration-200"></div>
                </div>
            </div>

            <!-- Content Area -->
            <div id="rec-content-area" class="p-6"></div>
        </div>
    `);

			// ── Tab switching ────────────────────────────────────────────
			$root.on('click', '.rec-nav-item', function () {
				$root.find('.rec-nav-selector').css('width', '0');
				$(this).find('.rec-nav-selector').css('width', '100%');
				render_rec_tab($(this).data('tab'));
			});

			// ── Activate default tab ─────────────────────────────────────
			const $firstTab = $root.find('.rec-nav-item[data-tab="openings"]');
			$firstTab.find('.rec-nav-selector').css('width', '100%');
			render_rec_tab('openings');

			// ── Tab renderers ────────────────────────────────────────────
			function render_rec_tab(tab) {
				const $area = $root.find('#rec-content-area');
				$area.empty();

				if (tab === 'openings') {
					render_openings($area);
				} else {
					render_appraisals($area);
				}
			}

			// ── Job Openings ─────────────────────────────────────────────
			function render_openings($area) {
				$area.html(`
            <div class="flex items-center justify-between mb-6">
                <h5 class=" text-base font-bold text-gray-800 ">Active Job Openings</h5>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-[100px] md:mb-0" id="job-openings-grid">
                ${[1, 2, 3, 4].map(() => `
                    <div class="animate-pulse bg-white rounded-xl border border-gray-100 p-5 flex flex-col gap-3">
                        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                        <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                        <div class="h-3 bg-gray-200 rounded w-2/3"></div>
                        <div class="h-6 bg-gray-200 rounded w-1/3 mt-2"></div>
                    </div>
                `).join('')}
            </div>
        `);

				frappe.call({
					method: "teampro.api.employee_self_service.get_job_openings",
					callback: (r) => {
						const grid = $root.find('#job-openings-grid');
						grid.empty();
						const jobs = r.message || [];

						if (!jobs.length) {
							grid.html(`
                        <div class="col-span-4 flex flex-col items-center justify-center py-20 text-center">
                            <div style="width:64px;height:64px;border-radius:50%;background:#eff6ff;
                                        display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                                <i class="fa fa-briefcase" style="font-size:26px;color:#3b82f6;"></i>
                            </div>
                            <p class="text-gray-500 font-medium">No active job openings</p>
                        </div>
                    `);
							return;
						}

						jobs.forEach(job => {
							const statusColor = job.status === 'Open'
								? { bg: '#dcfce7', text: '#15803d', label: 'Active' }
								: { bg: '#fef3c7', text: '#b45309', label: 'On Hold' };

							const card = $(`
                        <div class="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md
                                    transition-shadow p-5 flex flex-col gap-2 cursor-pointer">

                            <div class="flex items-start justify-between gap-2">
                                <div class="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                                     style="background:#eff6ff;">
                                    <i class="fa fa-briefcase" style="color:#3b82f6;font-size:16px;"></i>
                                </div>
                                <span style="background:${statusColor.bg};color:${statusColor.text};
                                             font-size:11px;font-weight:600;padding:3px 10px;
                                             border-radius:999px;">
                                    ${statusColor.label}
                                </span>
                            </div>

                            <p style="font-size:14px;font-weight:700;color:#1e293b;margin:4px 0 0;
                                      line-height:1.3;">${job.job_title || job.name}</p>

                            <p style="font-size:12px;color:#64748b;margin:0;">
                                <i class="fa fa-building-o mr-1"></i>${job.department || '—'}
                            </p>
                            <p style="font-size:12px;color:#64748b;margin:0;">
                                <i class="fa fa-map-marker mr-1"></i>${job.company || '—'}
                            </p>

                            <div class="mt-auto pt-3 border-t border-gray-100 flex items-center justify-between">
                                <span style="font-size:12px;color:#3b82f6;font-weight:600;">
                                    <i class="fa fa-users mr-1"></i>${job.applicant_count || 0} Applicants
                                </span>
                                <span style="font-size:11px;color:#94a3b8;">${job.posted_on || ''}</span>
                            </div>
                        </div>
                    `);


							card.on('click', function () {
								if (job.publish && job.route) {
									window.location.href = '/' + job.route;
								} else {
									frappe.set_route('Form', 'Job Opening', job.name);
								}
							});

							grid.append(card);
						});
					}
				});
			}

			// ── Appraisals ───────────────────────────────────────────────
			function render_appraisals($area) {
				$area.html(`
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-3 ">

                <!-- Left: Skill bars + radar -->
                <div class="lg:col-span-3 flex flex-col gap-6">

                    <!-- Current Appraisal Cycle -->
                    <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
                        <h5 class="text-base font-bold text-gray-800 mb-4">Current Appraisal Cycle</h5>
                        <div id="appraisal-bars" class="flex flex-col gap-4">
                            <div class="text-gray-300 text-sm text-center py-6">Loading...</div>
                        </div>
                    </div>

                    <!-- Radar Chart -->
                    <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
                        <p class="text-xs font-semibold text-gray-500 uppercase mb-4">KRA Performance</p>
                        <div style="position:relative;height:280px;">
                            <canvas id="radar-chart-main"></canvas>
                        </div>
                    </div>

                </div>

                <!-- Right: Summary card -->
                <div class="flex flex-col gap-6 ">
                    <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex flex-col items-center justify-center text-center"
                         style="min-height:220px;">
                        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Overall Rating</p>
                        <span id="overall-rating"
                              style="font-size:56px;font-weight:700;color:#10b981;line-height:1;">—</span>
                        <p class="text-sm text-gray-400 mt-2">out of 10</p>
                        <div id="rating-badge" class="mt-4 px-4 py-1 rounded-full text-sm font-semibold"
                             style="background:#dcfce7;color:#15803d;display:none;">Excellent</div>
                    </div>

                    <!-- Appraisal list -->
                    <div class="bg-white rounded-xl border border-gray-100  shadow-sm p-5 h-[460px] md:!h-[495px] mb-[100px] md:mb-0">
                        <h5 class="text-sm font-bold text-gray-700 mb-3">My Appraisals</h5>
                        <div id="appraisal-list" class="flex flex-col gap-2">
                            <div class="text-gray-300 text-sm text-center py-4">Loading...</div>
                        </div>
                    </div>
                </div>

            </div>
        `);

				frappe.call({
					method: "teampro.api.employee_self_service.get_appraisal_data",
					callback: (r) => {
						const data = r.message || {};
						const goals = data.goals || [];
						const appraisals = data.appraisals || [];

						// ── Skill bars ───────────────────────────────────
						const barsEl = document.getElementById('appraisal-bars');
						if (goals.length) {
							barsEl.innerHTML = goals.map(g => {
								const pct = Math.min(100, (g.score / 5) * 100).toFixed(0);
								const barColor = g.score >= 4 ? '#10b981'
									: g.score >= 3 ? '#3b82f6'
										: g.score >= 2 ? '#f59e0b' : '#ef4444';
								return `
                            <div>
                                <div class="flex justify-between mb-1">
                                    <span style="font-size:13px;color:#374151;font-weight:500;">${g.kra}</span>
                                    <span style="font-size:13px;font-weight:700;color:${barColor};">${g.score}</span>
                                </div>
                                <div style="height:8px;background:#f1f5f9;border-radius:999px;overflow:hidden;">
                                    <div style="height:100%;width:${pct}%;background:${barColor};
                                                border-radius:999px;transition:width 0.6s ease;"></div>
                                </div>
                            </div>`;
							}).join('');
						} else {
							barsEl.innerHTML = `
                        <div class="flex flex-col items-center py-8 text-center">
                            <i class="fa fa-bar-chart" style="font-size:28px;color:#e2e8f0;margin-bottom:8px;"></i>
                            <p style="color:#94a3b8;font-size:13px;">No appraisal data found</p>
                        </div>`;
						}

						// ── Overall rating ───────────────────────────────

						if (data.overall_rating) {
							const rating = parseFloat(data.overall_rating).toFixed(1);
							document.getElementById('overall-rating').textContent = rating;
							const badge = document.getElementById('rating-badge');
							badge.style.display = 'block';


							if (rating >= 80) { badge.textContent = 'Excellent'; badge.style.background = '#dcfce7'; badge.style.color = '#15803d'; }
							else if (rating >= 60) { badge.textContent = 'Good'; badge.style.background = '#dbeafe'; badge.style.color = '#1d4ed8'; }
							else if (rating >= 40) { badge.textContent = 'Average'; badge.style.background = '#fef3c7'; badge.style.color = '#b45309'; }
							else { badge.textContent = 'Needs Improvement'; badge.style.background = '#fee2e2'; badge.style.color = '#b91c1c'; }
						}

						// ── Appraisal list ───────────────────────────────
						const listEl = document.getElementById('appraisal-list');
						if (appraisals.length) {

							listEl.innerHTML = appraisals.map(a => `
								<div class="border-b border-gray-200" style="display:flex;  align-items:center;justify-content:space-between;
											padding:8px 10px;border-radius:8px;cursor:pointer;transition:background 0.15s;"
									onmouseover="this.style.background='#f8fafc'"
									onmouseout="this.style.background='transparent'"
									onclick="frappe.set_route('Form', 'Appraisal', '${a.name}')">
									<div>
										<p style="font-size:13px;font-weight:600;color:#1e293b;margin:0;">${a.name}</p>
										<p style="font-size:11px;color:#94a3b8;margin:2px 0 0;">
											${a.appraisal_cycle || a.period || ''}
										</p>
									</div>
									<span style="font-size:13px;font-weight:700;color:#10b981;">
										${parseFloat(a.overall_score || 0).toFixed(1)}
									</span>
								</div>
							`).join('');

						} else {
							listEl.innerHTML = `<p style="color:#94a3b8;font-size:13px;text-align:center;padding:1rem 0;">No appraisals found</p>`;
						}

						// ── Radar charts (Chart.js) ──────────────────────
						const radarLabels = goals.length
							? goals.map(g => g.kra)
							: ['Technical', 'Communication', 'Teamwork', 'Competence', 'Leadership'];

						const radarScores = goals.length
							? goals.map(g => g.score)
							: [0, 0, 0, 0, 0];

						const radarConfigs = [
							{ id: 'radar-chart-1', color: '#3b82f6' },
							{ id: 'radar-chart-2', color: '#ef4444' },
							{ id: 'radar-chart-3', color: '#10b981' },
						];



						const canvas = document.getElementById('radar-chart-main');
						if (canvas && radarLabels.length) {
							new Chart(canvas.getContext('2d'), {
								type: 'radar',
								data: {
									labels: radarLabels,
									datasets: [{
										label: 'Your Score',
										data: radarScores,
										backgroundColor: '#3b82f622',
										borderColor: '#3b82f6',
										borderWidth: 2,
										pointBackgroundColor: '#3b82f6',
										pointRadius: 4,
									}]
								},
								options: {
									scales: {
										r: {
											min: 0, max: 5,
											ticks: { stepSize: 0.5, font: { size: 9 }, color: '#000000ff' },
											grid: { color: '#c7c7c7' },
											pointLabels: { font: { size: 11 }, color: '#374151' }
										}
									},
									plugins: { legend: { display: false } },
									maintainAspectRatio: false,
									responsive: true,
								}
							});
						}



					}
				});
			}
		}




		else if (target === 'checkin') {

			$root.html(`
        <div class="min-h-full bg-[#edeef3] flex items-start md:items-center justify-center p-3 ">
            <div class="bg-white rounded-2xl shadow-lg w-full p-3 md:p-5 mt-[20px] mb-[100px] flex flex-col items-center gap-3" style="max-width:700px;">

                <!-- Status badge -->
                <div id="ci-status-badge"
                     style="font-size:11px;font-weight:700;letter-spacing:0.08em;
                            padding:4px 14px;border-radius:999px;
                            background:#eff6ff;color:#3b82f6;">
                    LOADING...
                </div>

                <!-- Profile photo -->
                <div style="position:relative;">
                    <img id="ci-emp-photo"
                         src="https://i.postimg.cc/ryxWSm4x/no-profile-img.jpg"
                         style="width:110px;height:110px;border-radius:50%;object-fit:cover;
                                border:4px solid #e2e8f0;box-shadow:0 4px 16px rgba(0,0,0,0.08);">
                    <div id="ci-status-dot"
                         style="position:absolute;bottom:6px;right:6px;width:16px;height:16px;
                                border-radius:50%;background:#94a3b8;border:2px solid white;"></div>
                </div>

                <!-- Name -->
                <div style="text-align:center;">
                    <p id="ci-emp-name" style="font-size:20px;font-weight:700;color:#1e293b;margin:0;">
                        Loading...
                    </p>
                    <a id="ci-att-link" href="#"
                       style="font-size:12px;color:#3b82f6;font-weight:600;
                              text-decoration:none;display:block;margin-top:4px;">
                        —
                    </a>
                </div>

                <!-- IN / OUT panels -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;width:100%;">
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:12px;">
                        <p style="font-size:9px;font-weight:700;color:#94a3b8;
                                  text-transform:uppercase;letter-spacing:0.06em;
                                  border-bottom:1px solid #e2e8f0;padding-bottom:6px;margin-bottom:8px;">
                            In Details
                        </p>
                        <div id="ci-panel-in">
                            <span style="font-size:12px;color:#cbd5e1;">No record</span>
                        </div>
                    </div>
                    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:12px;">
                        <p style="font-size:9px;font-weight:700;color:#94a3b8;
                                  text-transform:uppercase;letter-spacing:0.06em;
                                  border-bottom:1px solid #e2e8f0;padding-bottom:6px;margin-bottom:8px;">
                            Out Details
                        </p>
                        <div id="ci-panel-out">
                            <span style="font-size:12px;color:#cbd5e1;">No record</span>
                        </div>
                    </div>
                </div>

                <!-- Camera preview (hidden until capture) -->
                <div id="ci-camera-wrap"
                     style="display:none;width:100%;border-radius:16px;
                            overflow:hidden;border:2px solid #e2e8f0;">
                    <video id="ci-video" autoplay playsinline
                           style="width:100%;max-height:260px;object-fit:cover;display:block;"></video>
                    <canvas id="ci-canvas" style="display:none;"></canvas>
                </div>

                <!-- Action button -->
                <button id="ci-btn"
                        style="width:100%;padding:16px;border-radius:14px;border:none;
                               font-size:16px;font-weight:700;color:white;cursor:pointer;
                               background:linear-gradient(135deg,#3b82f6,#2563eb);
                               transition:opacity 0.2s,transform 0.1s;"
                        onmouseover="this.style.opacity='0.9'"
                        onmouseout="this.style.opacity='1'"
                        onmousedown="this.style.transform='scale(0.98)'"
                        onmouseup="this.style.transform='scale(1)'">
                    Check In Now
                </button>

            </div>
        </div>
    `);

			// ── State ────────────────────────────────────────────────────
			let _employee_id = null;
			let _has_in = false;
			let _has_out = false;
			let _stream = null;
			let _step = 'idle';   // idle | camera | verifying | done
			let _has_image = false;

			// ── Helpers ──────────────────────────────────────────────────
			function detail_html(log) {
				const time = frappe.datetime.str_to_user(log.time);
				return `
            <div style="font-size:11px;line-height:1.8;">
                <span style="color:#94a3b8;font-size:9px;text-transform:uppercase;">DATE & TIME</span><br>
                <strong style="color:#1e293b;">${time}</strong><br>
                <span style="color:#94a3b8;font-size:9px;text-transform:uppercase;">LOCATION</span><br>
                <strong style="color:#1e293b;">${log.latitude + ' , ' + log.longitude || 'N/A'}</strong><br>
                <span style="color:#94a3b8;font-size:9px;text-transform:uppercase;">DISTANCE</span><br>
                <strong style="color:#1e293b;">${log.custom_distance_from_office || '0'} km</strong><br>
                <span style="color:#94a3b8;font-size:9px;text-transform:uppercase;">ADDRESS</span><br>
                <span style="color:#475569;">${log.custom_address || 'N/A'}</span>
            </div>`;
			}

			function set_badge(text, color) {
				const badge = document.getElementById('ci-status-badge');
				const dot = document.getElementById('ci-status-dot');
				if (!badge) return;
				badge.textContent = text;
				badge.style.background = color + '22';
				badge.style.color = color;
				if (dot) dot.style.background = color;
			}

			function set_btn(text, gradient, disabled) {
				const btn = document.getElementById('ci-btn');
				if (!btn) return;
				btn.textContent = text;
				btn.style.background = gradient;
				btn.disabled = disabled || false;
				btn.style.opacity = disabled ? '0.6' : '1';
				btn.style.cursor = disabled ? 'not-allowed' : 'pointer';
			}

			function stop_camera() {
				if (_stream) {
					_stream.getTracks().forEach(t => t.stop());
					_stream = null;
				}
				const wrap = document.getElementById('ci-camera-wrap');
				if (wrap) wrap.style.display = 'none';
			}

			// ── Load today's checkins ────────────────────────────────────
			function refresh_ui() {
				if (!_employee_id) return;

				frappe.call({
					method: 'frappe.client.get_list',
					args: {
						doctype: 'Employee Checkin',
						filters: {
							employee: _employee_id,
							time: ['between', [
								frappe.datetime.now_date() + ' 00:00:00',
								frappe.datetime.now_date() + ' 23:59:59'
							]]
						},
						fields: ['log_type', 'time', 'latitude', 'longitude',
							'custom_address', 'custom_distance_from_office'],
						order_by: 'time asc'
					},
					callback(r) {
						_has_in = false;
						_has_out = false;

						(r.message || []).forEach(log => {
							if (log.log_type === 'IN') {
								_has_in = true;
								const el = document.getElementById('ci-panel-in');
								if (el) el.innerHTML = detail_html(log);
							} else if (log.log_type === 'OUT') {
								_has_out = true;
								const el = document.getElementById('ci-panel-out');
								if (el) el.innerHTML = detail_html(log);
							}
						});

						if (!_has_in) {
							set_badge('READY', '#3b82f6');
							set_btn('Check In Now',
								'linear-gradient(135deg,#3b82f6,#2563eb)', false);
						} else if (_has_in && !_has_out) {
							set_badge('CHECKED IN', '#10b981');
							set_btn('Check Out Now',
								'linear-gradient(135deg,#ef4444,#dc2626)', false);
						} else {
							set_badge('COMPLETED', '#8b5cf6');
							set_btn('All Done for Today', '#94a3b8', true);
						}

						if (!_has_image) {
							set_btn('No profile photo — contact HR', '#94a3b8', true);
						}


						_step = 'idle';
					}
				});

				// Refresh attendance link
				frappe.db.get_value('Attendance', {
					employee: _employee_id,
					attendance_date: frappe.datetime.get_today(),
					docstatus: ['!=', 2]
				}, 'name', (att) => {
					const link = document.getElementById('ci-att-link');
					if (!link) return;
					if (att && att.name) {
						link.textContent = att.name;
						link.href = `/app/attendance/${att.name}`;
					} else {
						link.textContent = 'No attendance record yet';
						link.style.color = '#94a3b8';
					}
				});


			}

			// ── Init: load employee ──────────────────────────────────────
			frappe.db.get_value('Employee',
				{ user_id: frappe.session.user },
				['name', 'employee_name', 'image'],
				(r) => {
					if (!r || !r.name) {
						set_badge('NOT FOUND', '#ef4444');
						set_btn('Employee record not found', '#94a3b8', true);
						return;
					}

					_employee_id = r.name;
					_has_image = !!r.image;

					const photo = document.getElementById('ci-emp-photo');
					const name = document.getElementById('ci-emp-name');
					if (photo && r.image) photo.src = r.image;
					if (name) name.textContent = r.employee_name;


					refresh_ui();
				}
			);

			// ── Button click flow ────────────────────────────────────────
			// ── Single unified button click handler ──────────────────────
			$root.on('click', '#ci-btn', function () {

				// Step: idle → open camera
				if (_step === 'idle') {
					if (!_employee_id) return;
					_step = 'camera';
					set_btn('Opening camera...', 'linear-gradient(135deg,#6366f1,#4f46e5)', true);

					const wrap = document.getElementById('ci-camera-wrap');
					const video = document.getElementById('ci-video');

					navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false })
						.then(stream => {
							_stream = stream;
							video.srcObject = stream;
							wrap.style.display = 'block';
							set_btn('📸  Capture Photo', 'linear-gradient(135deg,#6366f1,#4f46e5)', false);
							_step = 'capture';
						})
						.catch(() => {
							frappe.msgprint('Camera access denied. Please allow camera in browser settings.');
							_step = 'idle';
							refresh_ui();
						});
					return;
				}

				// Step: capture → take photo and process
				if (_step === 'capture') {
					const video = document.getElementById('ci-video');
					const canvas = document.getElementById('ci-canvas');
					canvas.width = video.videoWidth;
					canvas.height = video.videoHeight;
					canvas.getContext('2d').drawImage(video, 0, 0);

					stop_camera();
					_step = 'verifying';
					set_btn('Verifying face...', 'linear-gradient(135deg,#f59e0b,#d97706)', true);

					canvas.toBlob(blob => {
						const filename = `selfie_${_employee_id}_${Date.now()}.jpg`;
						const form_data = new FormData();
						form_data.append('file', blob, filename);
						form_data.append('is_private', '1');
						form_data.append('folder', 'Home/Attachments');

						fetch('/api/method/upload_file', {
							method: 'POST',
							headers: { 'X-Frappe-CSRF-Token': frappe.csrf_token },
							body: form_data
						})
							.then(res => res.json())
							.then(data => {
								const file_url = data.message?.file_url;
								if (!file_url) throw new Error('Upload failed');

								frappe.call({
									method: 'teampro.teampro.doctype.mark_attendance.mark_attendance.identify_employee_from_image',
									args: { selfie_url: file_url },
									callback(r) {
										if (!r.message || r.message.status !== 'success') {
											frappe.show_alert({
												message: r.message?.message || 'Face not recognized. Try again.',
												indicator: 'red'
											});
											_step = 'idle';
											refresh_ui();
											return;
										}

										set_btn('Getting location...', 'linear-gradient(135deg,#10b981,#059669)', true);

										navigator.geolocation.getCurrentPosition(
											pos => {
												set_btn('Marking attendance...', 'linear-gradient(135deg,#10b981,#059669)', true);

												frappe.call({
													method: 'teampro.teampro.doctype.mark_attendance.mark_attendance.create_employee_checkin',
													args: {
														employee_id: r.message.employee_id,
														selfie_url: file_url,
														score: r.message.match_score,
														latitude: pos.coords.latitude,
														longitude: pos.coords.longitude,
														address: '',
														device_id: _getDeviceId()
													},
													callback(res) {
														// res.message.status = attendance status ("Present"/"Absent")
														// success is indicated by presence of "attendance" key
														if (res.message && res.message.attendance) {
															const action = _has_in ? 'Check Out' : 'Check In';
															frappe.show_alert({
																message: `${action} marked successfully!`,
																indicator: 'green'
															});
														} else {
															frappe.show_alert({
																message: 'Could not mark attendance. Try again.',
																indicator: 'red'
															});
															_step = 'idle';
														}
														refresh_ui();
													},
													error(err) {
														console.error('Checkin error:', err);
														frappe.show_alert({
															message: 'Server error. Check console.',
															indicator: 'red'
														});
														_step = 'idle';
														refresh_ui();
													}
												});
											},
											err => {
												frappe.msgprint('Location access denied. Please enable location and try again.');
												_step = 'idle';
												refresh_ui();
											},
											{ enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
										);
									}
								});
							})
							.catch(err => {
								console.error('Upload error:', err);
								frappe.msgprint('Failed to upload photo. Try again.');
								_step = 'idle';
								refresh_ui();
							});
					}, 'image/jpeg', 0.85);
					return;
				}
			});

			// ── Device ID helper (reuse from mark_attendance.js) ─────────
			function _getDeviceId() {
				let id = localStorage.getItem('att_device_id') ||
					'dev_' + Math.random().toString(36).substring(2, 15);
				localStorage.setItem('att_device_id', id);
				return id;
			}
		}


	};


	const render_home_page_component = async (target) => {
		const $root = $(page.main).find('#home-content-area');
		$root.empty();


		if (target === 'dashboard') {

			const initialTemp = "--";
			const initialIcon = getWeatherIcon('Clear');
			const now = new Date();


			let greeting = (now.getHours() < 12) ? "Good morning" : (now.getHours() < 17) ? "Good afternoon" : "Good evening";


			let approval_items_html = "";
			const all_approvals = [
				...(approval_data.expense).map(d => ({
					title: `Expense: ${d.name}`,
					sub: `${d.employee_name} - ₹${d.total_claimed_amount}`,
					route: 'Expense Claim'
				})),
				...(approval_data.leave).map(d => ({
					title: `Leave: ${d.name}`,
					sub: `${d.employee_name} (${d.leave_type})`,
					route: 'Leave Application'
				})),
				...(approval_data.shift).map(d => ({
					title: `Shift: ${d.name}`,
					sub: `${d.employee_name} (${d.shift_type})`,
					route: 'Shift Request'
				}))
			];

			if (all_approvals.length > 0) {
				approval_items_html = all_approvals.map(item => `
				<div class="approval-item p-2 border-b border-gray-200 hover:bg-gray-50 cursor-pointer transition-all" 
					onclick="frappe.set_route('Form', '${item.route}', '${item.title.split(': ')[1]}')">
					<p class="text-sm font-bold text-gray-800">${item.title}</p>
					<p class="text-xs text-gray-500">${item.sub}</p>
				</div>
			`).join('');
			} else {
				approval_items_html = `<div class="flex flex-col items-center justify-center h-full opacity-40">
				<p class="text-sm mt-2">All caught up!</p>
			</div>`;
			}





			$root.html(`



		<div class=" dashboard-container grid grid-cols-1 md:grid-cols-3 gap-4 w-full bg-[#edeef3] px-3 pt-2  md:!pt-4 md:!px-4   ">


				<!--Weather and Quick Access Container-->
				
				<div id="weather-card" class="weather-widget  col-span-1 md:!col-span-2 h-[180px]  rounded-2xl p-8 flex justify-between items-center text-white relative overflow-hidden shadow-lg transition-all duration-500" 
					style="background: linear-gradient(135deg, #6e8efb, #a777e3); opacity: 0.8;">
					
					<div class="z-10">
						<div class="flex items-start">
							<span id="widget-temp" class="text-6xl font-bold leading-none">${initialTemp}</span>
							<span class="text-3xl font-medium">°</span>
						</div>
						<div class="mt-4">
							<p class="text-xl md:!text-2xl font-semibold opacity-90">${greeting},</p>
							<p class="text-2xl md:!text-3xl font-bold">${employee_data.employee_name.split(' ')[0]}!</p>
						</div>
					</div>

					<div class="text-right z-10 flex flex-col items-end">
						<!-- Added IDs here for updating -->
						<div class=" text-sm md:!text-lg font-medium opacity-80 mb-2">
							<span id="widget-day"></span> <span class="mx-2">|</span> <span id="widget-time"></span>
						</div>
						<img id="widget-icon" src="${initialIcon}" class="w-32 h-32 object-contain -mr-4 animate-pulse" alt="loading">
					</div>

					<div class="absolute -right-10 -bottom-10 w-64 h-64 bg-white opacity-10 rounded-full"></div>
				</div>

				<div class="dashboard-quick-access col-span-1  h-[180px] bg-white shadow-lg rounded-2xl pl-4 p-3">
					<p class="text-xl text-black-500 font-bold">Quick Access</p>
					<div class="dashboard-quick-access-items mt-4 grid grid-cols-2 gap-3">
						<a href="#" class="dashboard-quick-access-item" data-route="timesheet">Timesheet ↗</a>
						<a href="#" class="dashboard-quick-access-item" data-route="task">Task ↗</a>
						<a href="#" class="dashboard-quick-access-item" data-route="attendance">Attendance ↗</a>
						<a href="#" class="dashboard-quick-access-item" data-route="attendance-request">Attendance Request ↗</a>
						<a href="#" class="dashboard-quick-access-item" data-route="leave-application">Leave Application ↗</a>
					</div>
				</div>



				<div class="dashboard-today-attendance bg-white col-span-1  min-h-[370px] md:!h-[350px]  rounded-2xl p-8  shadow-lg ">
					<p class="text-xl text-black-500 font-bold">Today's Attendance</p>
					<div class="attendance-content w-full h-full grid grid-cols-2 gap-4 pt-4">

					 

						<div class="flex flex-col justify-start items-start mt-3 gap-2">
							<p class="text-black-500 font-bold">Date</p>
							<p>${attendance_data.attendance_date || "--"}</p>
							<p class="text-black-500 font-bold">In Time</p>
							<p>${attendance_data.in_time.split(' ')[1] || "--"}</p>
							<p class="text-black-500 font-bold">Status</p>
							<p>${attendance_data.status || "--"}</p>
						</div>

						<div class="flex flex-col justify-start items-start mt-3 gap-2">
							<p class="text-black-500 font-bold">Out Time</p>
							<p>${attendance_data.out_time.split(' ')[1] || "--"}</p>
							<p class="text-black-500 font-bold">Shift</p>
							<p>${attendance_data.shift || "--"}</p>
						</div>
					
					</div>
				</div>

				<div class="dashboard-attendance-permission bg-white col-span-1  min-h-[350px]  rounded-2xl p-8   shadow-lg ">
					<p class="text-xl text-black-500 font-bold">Attendance Permission</p>
					<div class="relative w-[220px] h-[220px] mt-5 ml-[30px] md:ml-[60px]"> 
						<canvas id="permissionChart"></canvas>
						<div class="absolute inset-0 flex flex-col items-center justify-center">
							<span id="remainingHoursText" class="text-2xl font-bold text-gray-800">0</span>
							<span class="text-xs text-gray-500 font-medium">Hours Left</span>
						</div>
					</div>
				</div>

				<div class="dashboard-approval bg-white col-span-1  min-h-[350px]  rounded-2xl p-8  shadow-lg ">
					<p class="text-xl text-black-500 font-bold">Approvals</p>
					<div class="approval-list-container h-[250px] overflow-y-auto pr-2">
						${approval_items_html}
					</div>
				</div>



				<!-- Calendar -->
					<div class="bg-white rounded-xl border border-gray-200 shadow-lg p-5 col-span-1 md:!col-span-3    mb-[100px] ">
						<div class="flex items-center justify-between mb-4">
							<h6 class="text-base font-bold text-gray-800" id="dash-cal-month-label"></h6>
							<div class="flex gap-2">
								<button id="dash-cal-prev" class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 hover:bg-gray-50 text-gray-500 font-bold">&#8249;</button>
								<button id="dash-cal-next" class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 hover:bg-gray-50 text-gray-500 font-bold">&#8250;</button>
							</div>
						</div>

						<!-- Day headers -->
						<div class="grid grid-cols-7 mb-1">
							${['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d =>
				`<div class="text-center text-xs font-semibold text-gray-400 py-1">${d}</div>`
			).join('')}
						</div>

						<!-- Day cells -->
						<div class="grid grid-cols-7 gap-y-1 gap-x-1" id="dash-cal-grid"></div>

						<!-- Legend -->
						<div class="flex items-center gap-4 mt-4 pt-3 border-t border-gray-100 flex-wrap">
							<span class="flex items-center gap-1.5 text-xs text-gray-500">
								<span class="w-3 h-3 rounded-full bg-blue-500 inline-block"></span> Approved
							</span>
							<span class="flex items-center gap-1.5 text-xs text-gray-500">
								<span class="w-3 h-3 rounded-full bg-amber-400 inline-block"></span> Pending
							</span>
							<span class="flex items-center gap-1.5 text-xs text-gray-500">
								<span class="w-3 h-3 rounded-full bg-red-400 inline-block"></span> Holiday
							</span>
							<span class="flex items-center gap-1.5 text-xs text-gray-500">
								<span class="w-3 h-3 rounded-sm bg-blue-100 border border-blue-300 inline-block"></span> Today
							</span>
						</div>
					</div>

				
			



				

		
		
		
		</div>	
    `);


			const updateDateTime = () => {
				const currentTime = new Date();
				const timeString = currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
				const dayName = currentTime.toLocaleDateString('en-US', { weekday: 'long' });

				$root.find('#widget-time').text(timeString);
				$root.find('#widget-day').text(dayName);
			};


			updateDateTime();

			const timeInterval = setInterval(() => {
				if ($('#weather-card').length === 0) {
					clearInterval(timeInterval);
					return;
				}
				updateDateTime();

				fetchWeather().then(weather => {
					const weatherIcon = getWeatherIcon(weather.condition);
					$root.find('#widget-temp').text(weather.temp);
					$root.find('#widget-icon').attr('src', weatherIcon).removeClass('animate-pulse');
					$root.find('#weather-card').css('opacity', '1');
				});

			}, 60000);

			fetchWeather().then(weather => {
				const weatherIcon = getWeatherIcon(weather.condition);
				$root.find('#widget-temp').text(weather.temp);
				$root.find('#widget-icon').attr('src', weatherIcon).removeClass('animate-pulse');
				$root.find('#weather-card').css('opacity', '1');
			});


			const renderPermissionChart = (permission_res) => {
				const canvas = document.getElementById('permissionChart');
				if (!canvas) return;
				const ctx = canvas.getContext('2d');


				const usedHours = (permission_res || []).reduce((sum, d) => {
					let hours = 0;
					if (d.total_time !== undefined && d.total_time !== null) {

						if (typeof d.total_time === 'number') {
							hours = d.total_time > 24 ? d.total_time / 3600 : d.total_time;
						}

						else if (typeof d.total_time === 'string') {
							if (d.total_time.includes(':')) {
								const parts = d.total_time.split(':');
								hours = parseInt(parts[0]) + (parseInt(parts[1]) / 60);
							} else {
								hours = parseFloat(d.total_time) || 0;
							}
						}
					}
					return sum + hours;
				}, 0);

				const totalAllowed = 2;
				const remainingHours = Math.max(0, totalAllowed - usedHours);


				$('#remainingHoursText').text(remainingHours.toFixed(1));


				if (window.myPermissionChart) {
					window.myPermissionChart.destroy();
				}

				window.myPermissionChart = new Chart(ctx, {
					type: 'doughnut',
					data: {
						labels: ['Used', 'Remaining'],
						datasets: [{
							data: [usedHours, remainingHours],
							backgroundColor: ['#6e8efb', '#f3f4f6'],
							borderWidth: 0,
							borderRadius: 10,
							hoverOffset: 4
						}]
					},
					options: {
						cutout: '80%',
						plugins: {
							legend: { display: false },
							tooltip: {
								callbacks: {
									label: (context) => `${context.label}: ${context.raw.toFixed(1)} hrs`
								}
							}
						},
						maintainAspectRatio: false,
						responsive: true
					}
				});
			};


			renderPermissionChart(permission_data);


			let dashCalYear = new Date().getFullYear();
			let dashCalMonth = new Date().getMonth();
			let dashLeaveMap = {};
			let dashHolidaySet = {};

			const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
				'July', 'August', 'September', 'October', 'November', 'December'];

			function renderDashCalendar() {
				const label = document.getElementById('dash-cal-month-label');
				const grid = document.getElementById('dash-cal-grid');
				if (!label || !grid) return;

				const todayKey = new Date().toISOString().slice(0, 10);
				label.textContent = `${MONTHS[dashCalMonth]} ${dashCalYear}`;
				grid.innerHTML = '';

				const firstDay = new Date(dashCalYear, dashCalMonth, 1).getDay();
				const daysInMonth = new Date(dashCalYear, dashCalMonth + 1, 0).getDate();

				for (let i = 0; i < firstDay; i++) {
					grid.insertAdjacentHTML('beforeend', `<div></div>`);
				}

				for (let d = 1; d <= daysInMonth; d++) {
					const mm = String(dashCalMonth + 1).padStart(2, '0');
					const dd = String(d).padStart(2, '0');
					const key = `${dashCalYear}-${mm}-${dd}`;

					const isToday = key === todayKey;
					const leaveInfo = dashLeaveMap[key];
					const holDesc = dashHolidaySet[key];
					const dow = new Date(dashCalYear, dashCalMonth, d).getDay();
					const isWeekend = dow === 0 || dow === 6;

					let cellStyle = `display:flex;align-items:center;justify-content:center;
            height:36px;border-radius:8px;font-size:13px;position:relative;cursor:default;`;
					let textColor = isWeekend ? '#94a3b8' : '#374151';
					let dotColor = '';
					let title = '';

					if (isToday) {
						cellStyle += 'background:#eff6ff;border:1px solid #93c5fd;font-weight:600;';
						textColor = '#1d4ed8';
					} else if (leaveInfo) {
						const isApproved = leaveInfo.status === 'Approved';
						cellStyle += isApproved ? 'background:#dbeafe;' : 'background:#fef3c7;';
						textColor = isApproved ? '#1e40af' : '#92400e';
						dotColor = isApproved ? '#3b82f6' : '#f59e0b';
						title = `${leaveInfo.leave_type} (${leaveInfo.status})`;
					} else if (holDesc) {
						cellStyle += 'background:#fee2e2;';
						textColor = '#991b1b';
						dotColor = '#f87171';
						title = holDesc;
					}

					grid.insertAdjacentHTML('beforeend', `
            <div style="${cellStyle}color:${textColor}" title="${title}">
                ${d}
                ${dotColor ? `<span style="position:absolute;bottom:3px;left:50%;
                    transform:translateX(-50%);width:4px;height:4px;border-radius:50%;
                    background:${dotColor}"></span>` : ''}
            </div>`);
				}
			}

			// Prev/Next buttons
			$root.on('click', '#dash-cal-prev', () => {
				if (dashCalMonth === 0) { dashCalMonth = 11; dashCalYear--; }
				else dashCalMonth--;
				renderDashCalendar();
			});
			$root.on('click', '#dash-cal-next', () => {
				if (dashCalMonth === 11) { dashCalMonth = 0; dashCalYear++; }
				else dashCalMonth++;
				renderDashCalendar();
			});

			// Load leave + holiday data
			frappe.call({
				method: "teampro.api.employee_self_service.get_leave_calendar",
				callback: (r) => {
					(r.message || []).forEach(lv => {
						let cur = new Date(lv.from_date);
						const end = new Date(lv.to_date);
						while (cur <= end) {
							const k = cur.toISOString().slice(0, 10);
							dashLeaveMap[k] = { status: lv.status, leave_type: lv.leave_type };
							cur.setDate(cur.getDate() + 1);
						}
					});
					renderDashCalendar();
				}
			});

			frappe.call({
				method: "teampro.api.employee_self_service.get_all_holidays",
				callback: (r) => {
					(r.message || []).forEach(h => { dashHolidaySet[h.date] = h.description; });
					renderDashCalendar();
				}
			});

			// Initial render
			renderDashCalendar();




		}

		else if (target === 'employee-profile') {

			$root.html(`

				<!-- Cover Picture -->
					<div class=" cover-picture w-full h-[150px] bg-[#adb6bd] p-0 ">

						<img src="https://i.postimg.cc/j2p5Q55s/cover-image.png" class="w-full h-full object-cover" />

					</div>

					<div class="Profile-name-box w-[90%] md:!w-[400px] h-[100px] bg-white absolute shadow-md rounded-md top-[125px] left-4 md:!left-5 flex items-center justify-center">

						<div class=" text-[12px] md:!text-[14px] text-black-500   font-bold">${employee_data.name}</div>

					</div>

					<div class="profile-picture w-[100px] h-[100px] bg-white absolute shadow-md rounded-lg top-[60px] left-35 md:!left-40 flex items-center justify-center">
						<img src="${employee_data.image}" class="w-full h-full rounded-lg object-cover" />
					</div>

					<div class="profile-sub-nav-bar w-[95%] md:!w-[890px] h-[60px]  bg-white absolute shadow-md rounded-md top-[240px] md:!top-[125px] left-2 md:!left-110 flex items-center justify-center md:!justify-start  md:!pl-5 pt-[20px] gap-10  pb-0 ">
					
						<!--Overview-->
						<div class="profile-sub-nav-bar-item  text-md md:!text-lg text-black-500 font-bold m-0 flex flex-col items-center justify-center cursor-pointer  p-0 " data-target="overview" >
							<p>Overview</p>
							<div class="profile-sub-nav-bar-item-selector w-full  mt-[2px]   bg-blue-500 rounded-full  "></div>
						</div>

						<!--My Documents-->
						<div class="profile-sub-nav-bar-item  text-md md:!text-lg text-black-500 font-bold m-0 flex flex-col items-center justify-center cursor-pointer  p-0 " data-target="my-documents" >
							<p>My Documents</p>
							<div class="profile-sub-nav-bar-item-selector w-full   mt-[2px]   bg-blue-500 rounded-full  "></div>
						</div>

						<!--Payroll-->
						<div class="profile-sub-nav-bar-item  text-md md:!text-lg text-black-500 font-bold m-0 flex flex-col items-center justify-center cursor-pointer  p-0 " data-target="payroll"  >
							<p>Payroll</p>
							<div class="profile-sub-nav-bar-item-selector w-full   mt-[2px]   bg-blue-500 rounded-full  "></div>
						</div>

					
					</div>	
					
					
					<div id="employee-profile-sub-nav-content-area" class="sub-nav-content-area w-[890px] min-h-screen  absolute top-[320px] md:!top-[195px] left-2 md:!left-110 " ></div>

				
				`);

			render_employee_profile_sub_nav_bar_component('overview');

			const $overviewSubNav = $(page.main).find('.profile-sub-nav-bar-item[data-target="overview"]');
			$overviewSubNav.find('.profile-sub-nav-bar-item-selector').addClass("h-[3px]");
		}
	}




	const render_employee_profile_sub_nav_bar_component = (target) => {
		const $root = $(page.main).find('#employee-profile-sub-nav-content-area');
		$root.empty();

		if (target === 'overview') {
			$root.html(`
			<div class="relative w-full" style="min-height: 720px; padding: 20px; mb-[100px]">		
				<div class="personal-info-box w-[41%] md:!w-[550px] h-[750px] md:!h-[420px] bg-white shadow-md rounded-md absolute top-[0px] left-[0px] flex flex-col items-start justify-start pl-[15px] pt-[20px] pb-0">
					<p class="text-[20px] pl-[10px] text-black-500 font-bold">Personal Info</p>
					<hr class="w-full h-[2px] bg-gray-300 absolute top-[50px] left-0">
					<div class="personal-info-box-content w-full flex flex-col md:!flex-row gap-[10px] md:!gap-[120px] items-start justify-start pl-[25px] pt-[20px] absolute top-[65px] left-0 pb-0">
						<div>
							<p class="font-bold text-lg">Personal Name</p><p>${employee_data.employee_name}</p><br>
							<p class="font-bold text-lg">Status</p><p>${employee_data.status}</p><br>
							<p class="font-bold text-lg">Company</p><p>${employee_data.company}</p><br>
							<p class="font-bold text-lg">Employment Type</p><p>${employee_data.employment_type}</p>
						</div>
						<div>
							<p class="font-bold text-lg">Department</p><p>${employee_data.department}</p><br>
							<p class="font-bold text-lg">Designation</p><p>${employee_data.designation}</p><br>
							<p class="font-bold text-lg">Branch</p><p>${employee_data.branch}</p><br>
							<p class="font-bold text-lg">Grade</p><p>${employee_data.grade}</p>
						</div>
					</div>
				</div>

				<div class="contact-details-box w-[41%] md:!w-[310px] h-[360px] bg-white shadow-md rounded-md absolute top-[770px] md:!top-[0px] left-[0px] md:!left-[580px] flex flex-col items-start justify-start pl-[10px] pt-[20px] pb-0">
					<p class="text-[20px] pl-[10px] font-bold">Contact Details</p>
					<hr class="w-full h-[2px] bg-gray-300 absolute top-[50px] left-0">
					<div class="mt-4 ml-3 pt-6">
						<p class="font-bold text-lg">Phone</p><p>${employee_data.phone}</p><br>
						<p class="font-bold text-lg">Personal Email</p><p>${employee_data.email}</p><br>
						<p class="font-bold text-lg">Company Email</p><p>${employee_data.company_email}</p>
					</div>
				</div>

				<div class="other-details-box w-[41%] md:!w-[550px] h-[400px] md:!h-[270px] bg-white shadow-md rounded-md absolute top-[1145px] md:!top-[430px] left-[0px] flex flex-col items-start justify-start pl-[15px] pt-[20px] pb-0">
					<p class="text-[20px] pl-[10px] font-bold">Other Details</p>
					<hr class="w-full h-[2px] bg-gray-300 absolute top-[50px] left-0">
					<div class="personal-info-box-content w-full flex flex-col md:!flex-row gap-[10px] md:!gap-[200px] items-start justify-start pl-[25px] pt-[20px] absolute top-[65px] left-0 pb-0">
						<div>
							<p class="font-bold text-lg">Date of Birth</p><p>${employee_data.date_of_birth}</p><br>
							<p class="font-bold text-lg">Gender</p><p>${employee_data.gender}</p>
						</div>
						<div>
							<p class="font-bold text-lg">Date of Joining</p><p>${employee_data.date_of_joining}</p><br>
							<p class="font-bold text-lg">Age</p><p>${employee_data.age}</p>
						</div>
					</div>
				</div>

				<div class="emergency-contact-details-box w-[41%] md:!w-[310px] h-[330px] bg-white shadow-md rounded-md absolute top-[1560px] md:!top-[370px] left-[0px] md:!left-[580px] flex flex-col items-start justify-start pl-[10px] pt-[20px] pb-0">
					<p class="text-[20px] pl-[10px] font-bold">Emergency Contact Details</p>
					<hr class="w-full h-[2px] bg-gray-300 absolute top-[50px] left-0">
					<div class="mt-4 ml-3 pt-2">
						<p class="font-bold text-lg">Emergency Contact Name</p><p>${employee_data.emergency_contact_name}</p><br>
						<p class="font-bold text-lg">Emergency Phone</p><p>${employee_data.emergency_phone}</p><br>
						<p class="font-bold text-lg">Relation</p><p>${employee_data.relation}</p>
					</div>
				</div>
			</div>	
        `);
		}

		// ── My Documents ─────────────────────────────────────────────
		else if (target === 'my-documents') {
			$root.html(`
            <div class="w-[100%]  pt-2 mb-[100px] ">
                <div class="flex flex-col  items-start  justify-between mb-5 mr-5">
                    <h5 class="text-base font-bold text-gray-800">My Documents</h5>
                    <span class="text-xs text-gray-400">Files attached to your employee record by HR</span>
                </div>
                <div id="docs-grid" class="grid grid-cols-1 md:!grid-cols-2 lg:!grid-cols-3 gap-1 md:!gap-4">
                    ${[1, 2, 3].map(() => `
                        <div class="animate-pulse   bg-white rounded-xl border border-gray-100 p-4 flex gap-3 items-center">
                            <div class="w-10 h-10 bg-gray-200 rounded-lg shrink-0"></div>
                            <div class="flex-1 space-y-2">
                                <div class="h-3 bg-gray-200 rounded w-3/4"></div>
                                <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `);

			frappe.call({
				method: "teampro.api.employee_self_service.get_employee_documents",
				callback: (r) => {
					const grid = $root.find('#docs-grid');
					grid.empty();
					const docs = r.message || [];

					if (!docs.length) {
						grid.html(`
                        <div class=" hidden md:!flex col-span-1 md:col-span-3  flex-col items-center justify-center py-16 px-10 text-center">
                            <div style="width:60px;height:60px;border-radius:50%;background:#f1f5f9;
                                        display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
                                <i class="fa fa-folder-open-o" style="font-size:26px;color:#94a3b8;"></i>
                            </div>
                            <p style="color:#64748b;font-size:13px;font-weight:500;">No documents uploaded yet</p>
                            <p style="color:#94a3b8;font-size:12px;margin-top:4px;">Contact HR to upload your employment documents</p>
                        </div>`);
						return;
					}

					// File type → icon + color
					function fileStyle(type) {
						const t = (type || '').toUpperCase();
						if (t === 'PDF') return { icon: 'fa-file-pdf-o', bg: '#fee2e2', color: '#dc2626' };
						if (['DOC', 'DOCX'].includes(t)) return { icon: 'fa-file-word-o', bg: '#dbeafe', color: '#2563eb' };
						if (['XLS', 'XLSX'].includes(t)) return { icon: 'fa-file-excel-o', bg: '#dcfce7', color: '#16a34a' };
						if (['JPG', 'JPEG', 'PNG'].includes(t)) return { icon: 'fa-file-image-o', bg: '#fef3c7', color: '#d97706' };
						return { icon: 'fa-file-o', bg: '#f1f5f9', color: '#64748b' };
					}




					docs.forEach(doc => {
						const style = fileStyle(doc.file_type);
						grid.append(`
							<a href="${doc.file_url}" target="_blank" 
							class="bg-white w-[43%] md:!w-full rounded-xl border border-gray-100 shadow-sm hover:shadow-md
									hover:border-blue-200 transition-all cursor-pointer p-4 flex items-center gap-3 group"
							style="text-decoration:none;">
								<div style="width:44px;height:44px;border-radius:10px;background:${style.bg};
											display:flex;align-items:center;justify-content:center;flex-shrink:0;">
									<i class="fa ${style.icon}" style="font-size:20px;color:${style.color};"></i>
								</div>
								<div class="flex-1 min-w-0">
									<p style="font-size:13px;font-weight:600;color:#1e293b;margin:0;
											white-space:nowrap;overflow:hidden;text-overflow:ellipsis;"
									title="${doc.file_name}">${doc.file_name}</p>
									<p style="font-size:11px;color:#94a3b8;margin:3px 0 0;">
										${doc.file_type || 'File'} ${doc.file_size ? '· ' + doc.file_size : ''} · ${doc.uploaded_on}
									</p>
								</div>
								<div style="opacity:0;transition:opacity 0.15s;flex-shrink:0;"
									class="group-hover:!opacity-100">
									<div style="width:32px;height:32px;border-radius:8px;background:#f1f5f9;
												display:flex;align-items:center;justify-content:center;">
										<i class="fa fa-external-link" style="font-size:13px;color:#475569;"></i>
									</div>
								</div>
							</a>
						`);
					});


				}
			});
		}

		// ── Payroll ──────────────────────────────────────────────────
		else if (target === 'payroll') {
			$root.html(`
            <div class="w-full h-full pr-5 pt-2  ">

                <!-- Summary cards row -->
                <div class="grid grid-cols-1 md:!grid-cols-4 lg:grid-cols-4 gap-4 mb-6 w-[43%] md:!w-full " id="payroll-summary-cards">
                    ${[1, 2, 3, 4].map(() => `
                        <div class="animate-pulse bg-white rounded-xl border border-gray-100 p-4">
                            <div class="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
                            <div class="h-6 bg-gray-200 rounded w-3/4"></div>
                        </div>`).join('')}
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 ">

                    <!-- Earnings & Deductions breakdown -->
                    <div class="lg:col-span-2 w-[43%] h-[500px] md:!w-full bg-white rounded-xl border border-gray-100 shadow-sm p-5 ">
                        <h5 class="text-sm font-bold text-gray-700 mb-4" id="payroll-slip-period">
                            Current Salary Slip
                        </h5>
                        <div class="grid grid-cols-2 gap-6" id="payroll-breakdown">
                            <div class="text-gray-300 text-sm col-span-2 text-center py-8">Loading...</div>
                        </div>
                        <div class="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
                            <span style="font-size:12px;color:#64748b;" id="payroll-in-words"></span>
                            <a id="payroll-download-btn" href="#" target="_blank"
                               class="flex items-center gap-1.5 text-xs font-semibold text-blue-600
                                      hover:text-blue-700 transition-colors">
                                <i class="fa fa-download"></i> Download Slip
                            </a>
                        </div>
                    </div>

                    <!-- YTD + history -->
                    <div class="flex flex-col gap-4 w-[43%] md:!w-full">
                        <!-- YTD Card -->
                        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
                            <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                                Year to Date
                            </p>
                            <div class="flex flex-col gap-3" id="ytd-section">
                                <div class="animate-pulse h-4 bg-gray-200 rounded w-3/4"></div>
                                <div class="animate-pulse h-4 bg-gray-200 rounded w-1/2"></div>
                            </div>
                        </div>

                        <!-- Slip history -->
                        <div class="bg-white rounded-xl h-[280px] border border-gray-100 shadow-sm p-5 ">
                            <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                                Payslip History
                            </p>
                            <div id="slip-history" class=" h-[200px] mb-2 flex flex-col  gap-2 overflow-y-auto " style="scrollbar-width:none; -ms-overflow-style:none;">
                                <div class="text-gray-300 text-sm text-center py-4">Loading...</div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        `);

			frappe.call({
				method: "teampro.api.employee_self_service.get_payroll_data",
				callback: (r) => {
					const data = r.message || {};
					const current = data.current;
					const slips = data.slips || [];
					const ytd = data.ytd || {};

					const fmt = (n, cur) =>
						new Intl.NumberFormat('en-IN', {
							style: 'currency', currency: cur || 'INR',
							maximumFractionDigits: 0
						}).format(n || 0);

					// ── Summary cards ────────────────────────────────
					const cards = $root.find('#payroll-summary-cards');
					if (current) {
						cards.html(`
                        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
                            <p style="font-size:11px;color:#64748b;font-weight:500;text-transform:uppercase;
                                      letter-spacing:0.05em;">Gross Pay</p>
                            <p style="font-size:20px;font-weight:700;color:#1e293b;margin-top:4px;">
                                ${fmt(current.gross_pay, current.currency)}
                            </p>
                        </div>
                        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
                            <p style="font-size:11px;color:#64748b;font-weight:500;text-transform:uppercase;
                                      letter-spacing:0.05em;">Deductions</p>
                            <p style="font-size:20px;font-weight:700;color:#ef4444;margin-top:4px;">
                                ${fmt(current.total_deduction, current.currency)}
                            </p>
                        </div>
                        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
                            <p style="font-size:11px;color:#64748b;font-weight:500;text-transform:uppercase;
                                      letter-spacing:0.05em;">Net Pay</p>
                            <p style="font-size:20px;font-weight:700;color:#10b981;margin-top:4px;">
                                ${fmt(current.net_pay, current.currency)}
                            </p>
                        </div>
                        <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
                            <p style="font-size:11px;color:#64748b;font-weight:500;text-transform:uppercase;
                                      letter-spacing:0.05em;">Payment Days</p>
                            <p style="font-size:20px;font-weight:700;color:#1e293b;margin-top:4px;">
                                ${current.payment_days} / ${current.total_working_days}
                            </p>
                        </div>
                    `);

						// ── Period label ─────────────────────────────
						const sd = new Date(current.start_date).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' });
						const ed = new Date(current.end_date).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' });
						$root.find('#payroll-slip-period').text(`Salary Slip — ${sd} to ${ed}`);
						$root.find('#payroll-in-words').text(current.total_in_words);
						$root.find('#payroll-download-btn').attr(
							'href',
							`/printview?doctype=Salary+Slip&name=${encodeURIComponent(current.name)}&format=Standard`
						);

						// ── Earnings & Deductions breakdown ──────────
						const breakdown = $root.find('#payroll-breakdown');
						const earningsHtml = `
                        <div>
                            <p style="font-size:12px;font-weight:700;color:#10b981;
                                      text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;">
                                <i class="fa fa-arrow-up mr-1"></i>Earnings
                            </p>
                            ${(current.earnings || []).map(e => `
                                <div style="display:flex;justify-content:space-between;
                                            padding:6px 0;border-bottom:1px solid #f8fafc;">
                                    <span style="font-size:12px;color:#475569;">${e.component}</span>
                                    <span style="font-size:12px;font-weight:600;color:#1e293b;">
                                        ${fmt(e.amount, current.currency)}
                                    </span>
                                </div>`).join('')}
                        </div>`;

						const deductionsHtml = `
                        <div>
                            <p style="font-size:12px;font-weight:700;color:#ef4444;
                                      text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;">
                                <i class="fa fa-arrow-down mr-1"></i>Deductions
                            </p>
                            ${(current.deductions || []).map(d => `
                                <div style="display:flex;justify-content:space-between;
                                            padding:6px 0;border-bottom:1px solid #f8fafc;">
                                    <span style="font-size:12px;color:#475569;">${d.component}</span>
                                    <span style="font-size:12px;font-weight:600;color:#ef4444;">
                                        - ${fmt(d.amount, current.currency)}
                                    </span>
                                </div>`).join('')}
                        </div>`;

						breakdown.html(earningsHtml + deductionsHtml);

					} else {
						cards.html(`
                        <div class="col-span-4 text-center py-8 text-gray-400 text-sm">
                            No salary slip found
                        </div>`);
					}

					// ── YTD ──────────────────────────────────────────
					const ytdEl = $root.find('#ytd-section');
					ytdEl.html(`
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                padding:8px 0;border-bottom:1px solid #f8fafc;">
                        <span style="font-size:12px;color:#64748b;">Gross YTD</span>
                        <span style="font-size:13px;font-weight:700;color:#1e293b;">
                            ${fmt(ytd.gross, current?.currency)}
                        </span>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;">
                        <span style="font-size:12px;color:#64748b;">Net YTD</span>
                        <span style="font-size:13px;font-weight:700;color:#10b981;">
                            ${fmt(ytd.net, current?.currency)}
                        </span>
                    </div>
                `);

					// ── Slip history ─────────────────────────────────
					const histEl = $root.find('#slip-history');
					if (slips.length) {
						histEl.html(slips.map((s, i) => {
							const mon = new Date(s.end_date).toLocaleDateString('en-IN',
								{ month: 'short', year: 'numeric' });
							const isLatest = i === 0;
							return `
                            <div  style="display:flex;align-items:center;justify-content:space-between;
                                        padding:8px 10px;border-radius:8px;transition:background 0.15s;
                                        ${isLatest ? 'background:#f0fdf4;' : ''}"
                                 onmouseover="this.style.background='#f8fafc'"
                                 onmouseout="this.style.background='${isLatest ? '#f0fdf4' : 'transparent'}'">
                                <div>
                                    <p style="font-size:13px;font-weight:600;color:#1e293b;margin:0;">
                                        ${mon} ${isLatest ? '<span style="font-size:10px;background:#dcfce7;color:#15803d;padding:1px 6px;border-radius:999px;margin-left:4px;">Latest</span>' : ''}
                                    </p>
                                    <p style="font-size:11px;color:#94a3b8;margin:2px 0 0;">
                                        Net: ${fmt(s.net_pay, s.currency)}
                                    </p>
                                </div>
                                <a href="/printview?doctype=Salary+Slip&name=${encodeURIComponent(s.name)}&format=Standard"
                                   target="_blank"
                                   style="width:28px;height:28px;border-radius:6px;background:#f1f5f9;
                                          display:flex;align-items:center;justify-content:center;
                                          text-decoration:none;"
                                   title="Download">
                                    <i class="fa fa-download" style="font-size:12px;color:#475569;"></i>
                                </a>
                            </div>`;
						}).join(''));
					} else {
						histEl.html(`<p style="color:#94a3b8;font-size:13px;text-align:center;padding:1rem 0;">
                        No payslip history found</p>`);
					}
				}
			});
		}
	};




	$(page.main).on('click', '.nav-item', function () {
		const activeBoxClasses = "bg-[#0079ef] rounded-lg shadow-md";
		const activeText = "text-white font-medium";
		const inactiveText = "text-gray-300";

		const $all_items = $(page.main).find('.nav-item');


		$all_items.find('.icon-box').removeClass(activeBoxClasses);
		$all_items.find('div.text-xs').removeClass(activeText).addClass(inactiveText);
		$all_items.find('img').removeClass('brightness-0 invert');


		const $current = $(this);
		$current.find('.icon-box').addClass(activeBoxClasses);
		$current.find('div.text-xs').removeClass(inactiveText).addClass(activeText);
		$current.find('img').addClass('brightness-0 invert');


		render_component($current.attr('data-target'));
	});

	$(page.main).on('click', '.home-nav-bar-item', function () {
		const active_selector_line = "w-full h-[3px]";


		const $all_items = $(page.main).find('.home-nav-bar-item');


		$all_items.find('.home-nav-bar-item-selector').removeClass(active_selector_line);



		const $current = $(this);
		$current.find('.home-nav-bar-item-selector').addClass(active_selector_line);



		render_home_page_component($current.attr('data-target'));
	});


	$(page.main).on('click', '.profile-sub-nav-bar-item', function () {
		const active_selector_line = "h-[3px]";


		const $all_items = $(page.main).find('.profile-sub-nav-bar-item');


		$all_items.find('.profile-sub-nav-bar-item-selector').removeClass(active_selector_line);


		const $current = $(this);
		$current.find('.profile-sub-nav-bar-item-selector').addClass(active_selector_line);



		render_employee_profile_sub_nav_bar_component($current.attr('data-target'));
	});



	$(page.main).on('click', '.dashboard-quick-access-item', function (e) {
		e.preventDefault();
		const target_route = $(this).attr('data-route');

		if (target_route) {

			frappe.set_route('List', target_route);
		}
	});




	Promise.all([
		frappe.db.get_value("User", frappe.session.user, "full_name"),
		frappe.db.get_value("Employee", { "user_id": frappe.session.user }, ['name', 'image', 'employee_name', 'status', 'department', 'designation', 'personal_email', 'user_id', 'company_email', 'cell_number', 'date_of_birth', 'gender', 'date_of_joining', 'age', 'person_to_be_contacted', 'emergency_phone_number', 'relation', 'employment_type', 'grade', 'company', 'branch'])
	]).then(([user_res, emp_res]) => {

		const employee_id = emp_res.message?.name;

		if (employee_id) {
			return Promise.all([

				frappe.db.get_value("Attendance", {
					"employee": employee_id,
					"attendance_date": frappe.datetime.get_today()
				}, ["name", "attendance_date", "in_time", "out_time", "status", "department", "status", "shift"]),

				// frappe.db.get_list("Expense Claim", {
				// 	filters: { "expense_approver": frappe.session.user, "approval_status": "Draft" },
				// 	fields: ["name", "employee_name", "total_claimed_amount", "posting_date"]
				// }),


				// frappe.db.get_list("Leave Application", {
				// 	filters: { "leave_approver": frappe.session.user, "status": "Open" },
				// 	fields: ["name", "employee_name", "leave_type", "total_leave_days"]
				// }),


				// frappe.db.get_list("Shift Request", {
				// 	filters: { "approver": frappe.session.user, "status": "Draft" },
				// 	fields: ["name", "employee_name", "shift_type", "from_date"]
				// }),

				new Promise((resolve) => {
					frappe.call({
						method: "teampro.api.employee_self_service.get_approval_data",
						callback: function (r) {
							resolve(r.message || { expense: [], leave: [], shift: [] });
						},
						error: function () {
							resolve({ expense: [], leave: [], shift: [] });
						}
					});
				}),





				new Promise((resolve) => {
					frappe.call({
						method: "teampro.api.employee_self_service.get_permission_data",
						callback: function (r) {
							resolve(r.message || []);
						},
						error: function () {
							resolve([]);
						}
					});
				})


			]).then(([att_res, approval_res, permission_res]) => {
				return [user_res, emp_res, att_res, approval_res, permission_res];
			});
		}
		return [user_res, emp_res, { message: {} }];

	}).then(([user_res, emp_res, att_res, approval_res, permission_res]) => {

		let name = emp_res.message?.employee_name || user_res.message?.full_name || "Administrator";
		let status = emp_res.message?.status || "";
		let department = emp_res.message?.department || "";
		let designation = emp_res.message?.designation || "";
		let email = emp_res.message?.personal_email || emp_res.message?.user_id || "";
		let company_email = emp_res.message?.company_email || "";
		let phone = emp_res.message?.cell_number || "";
		let date_of_birth = emp_res.message?.date_of_birth || "";
		let gender = emp_res.message?.gender || "";
		let date_of_joining = emp_res.message?.date_of_joining || "";
		let age = emp_res.message?.age || "";
		let emergency_contact_name = emp_res.message?.person_to_be_contacted || "";
		let emergency_phone = emp_res.message?.emergency_phone_number || "";
		let relation = emp_res.message?.relation || "";
		let employment_type = emp_res.message?.employment_type || "";
		let grade = emp_res.message?.grade || "";
		let company = emp_res.message?.company || "";
		let branch = emp_res.message?.branch || "";
		let attendance = att_res.message?.name || "";
		let attendance_date = att_res.message?.attendance_date || "";
		let in_time = att_res.message?.in_time || "";
		let out_time = att_res.message?.out_time || "";
		let attendance_status = att_res.message?.status || "";
		let attendance_department = att_res.message?.department || "";
		let attendance_shift = att_res.message?.shift || "";

		if (designation && name !== "Administrator") {
			employee_data.name = `${name} - ${designation}`;
		} else {
			employee_data.name = name;
		}

		employee_data.employee_name = name;
		employee_data.status = status;
		employee_data.department = department;
		employee_data.designation = designation;
		employee_data.email = email;
		employee_data.company_email = company_email;
		employee_data.phone = phone;
		employee_data.date_of_birth = frappe.format(date_of_birth, { "fieldtype": "Date" });
		employee_data.gender = gender;
		employee_data.date_of_joining = frappe.format(date_of_joining, { "fieldtype": "Date" });
		employee_data.age = age;
		employee_data.emergency_contact_name = emergency_contact_name;
		employee_data.emergency_phone = emergency_phone;
		employee_data.relation = relation;
		employee_data.employment_type = employment_type;
		employee_data.grade = grade;
		employee_data.company = company;
		employee_data.branch = branch;

		employee_data.image = emp_res.message?.image || "https://i.postimg.cc/ryxWSm4x/no-profile-img.jpg";


		attendance_data.name = attendance;
		attendance_data.attendance_date = frappe.format(attendance_date, { fieldtype: "Date" });
		attendance_data.in_time = frappe.format(in_time, { fieldtype: "Datetime" });
		attendance_data.out_time = frappe.format(out_time, { fieldtype: "Datetime" });
		attendance_data.status = attendance_status;
		attendance_data.department = attendance_department;
		attendance_data.shift = attendance_shift;

		approval_data.expense = approval_res.expense || [];
		approval_data.leave = approval_res.leave || [];
		approval_data.shift = approval_res.shift || [];

		permission_data = permission_res || [];


		render_component('home');
		render_home_page_component('dashboard');

		const $homeNav = $(page.main).find('.nav-item[data-target="home"]');
		$homeNav.find('.icon-box').addClass("bg-[#0079ef] rounded-lg shadow-md");
		$homeNav.find('div.text-xs').removeClass("text-gray-300").addClass("text-white font-medium");
		$homeNav.find('img').addClass('brightness-0 invert');


		const $dashboardSubNav = $(page.main).find('.home-nav-bar-item[data-target="dashboard"]');
		$dashboardSubNav.find('.home-nav-bar-item-selector').addClass("w-full h-[3px]");


		if (!attendance_data.name) {
			const $attendancecontent = $(page.main).find('.attendance-content');
			$attendancecontent.empty();
			$attendancecontent.removeClass("grid grid-cols-2 gap-4 pt-4");
			$attendancecontent.html(`
				<div class="flex flex-col items-center justify-center h-full">
					<div class="text-gray-500">No attendance data available</div>
				</div>
			`);
		}
	})



}


frappe.pages['employee-self-service'].on_page_show = function (wrapper) {

	$('.body-sidebar-container').hide();
	$('.body-sidebar-placeholder').hide();

	setTimeout(() => {
		$('.body-sidebar-container').hide();
		$('.body-sidebar-placeholder').hide();
		$('.main-section').css('padding-left', '0');
	}, 100);

	setTimeout(() => {
		$('.body-sidebar-container').hide();
		$('.body-sidebar-placeholder').hide();
	}, 500);
};

frappe.pages['employee-self-service'].on_page_hide = function (wrapper) {
	$('.body-sidebar-container').show();
	$('.body-sidebar-placeholder').show();

	$('.main-section').css('padding-left', '');
};