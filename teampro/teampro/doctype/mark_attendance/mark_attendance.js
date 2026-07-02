frappe.ui.form.on('Mark Attendance', {
    onload: function (frm) {
        if (!frm.doc.attendance_date) {
            frm.set_value('attendance_date', frappe.datetime.get_today());
        }
        navigator.geolocation.getCurrentPosition(
            function (position) {
                const { latitude, longitude } = position.coords;

                frm.set_value('latitude', latitude);
                frm.set_value('longitude', longitude);


                const geocoder = new google.maps.Geocoder();
                geocoder.geocode(
                    { location: { lat: latitude, lng: longitude } },
                    function (results, status) {
                        if (status === 'OK' && results[0]) {
                            frm.set_value('address', results[0].formatted_address);
                        } else {
                            frappe.dom.unfreeze();
                            frappe.msgprint(__('Unable to fetch address. Try again.'));
                        }
                    }
                );
            },
            function (error) {

                if (error.code === error.TIMEOUT && !retry) {
                    setTimeout(() => get_high_accuracy_location(true), 5000);
                    return;
                }

                frappe.throw(__('Unable to capture GPS location. Move outdoors and retry.'));
            },
            {
                enableHighAccuracy: true,
                timeout: 30000,
                maximumAge: 0
            }
        );
    },
    refresh: function (frm) {
        const html_content = `
            <style>
                .checkin-container { background-color: #FDF2E2; padding: 25px 15px; display: flex; justify-content: center; align-items: center; border-radius: 12px; font-family: sans-serif; }
                .checkin-card { background: white; border-radius: 24px; padding: 30px 20px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.06); width: 100%; max-width: 500px; }
                #emp-photo { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; border: 5px solid #ffffff; box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin-bottom: 15px; }
                .greeting-text { font-size: 22px; font-weight: 700; color: #2d2d2d; margin: 5px 0 2px 0; }
                .att-link { font-size: 13px; color: #3B82F6; text-decoration: none; font-weight: 600; display: block; margin-bottom: 15px; }
                .att-link:hover { text-decoration: underline; }
                .status-label-top { font-weight: 800; font-size: 12px; letter-spacing: 1px; margin-bottom: 10px; color: #3B82F6; }
                .split-panel { display: flex; gap: 10px; margin-top: 10px; text-align: left; }
                .panel-box { flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; font-size: 11px; min-height: 120px; }
                .panel-title { font-weight: bold; border-bottom: 1px solid #e2e8f0; margin-bottom: 8px; color: #64748b; font-size: 10px; text-transform: uppercase; }
                .data-row { margin-bottom: 5px; line-height: 1.4; }
                .data-label { color: #94a3b8; font-weight: 600; font-size: 9px; display: block; text-transform: uppercase; }
                .data-val { color: #1e293b; font-weight: 500; word-break: break-all; display: block; }
                #btn-checkin { background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%); color: white; border: none; padding: 16px; border-radius: 15px; font-weight: 600; font-size: 16px; width: 100%; cursor: pointer; margin-top: 15px; }
                .btn-checkout { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important; }
            </style>

            <div class="checkin-container">
                <div class="checkin-card">
                    <div class="status-label-top" id="doc-status">READY</div>
                    <img id="emp-photo" src="/assets/frappe/images/default-avatar.png">
                    <div class="greeting-text" id="emp-greeting">Hello!</div>
                    <a id="att-id-link" class="att-link" href="#">-</a>
                    <div class="split-panel">
                        <div class="panel-box" id="panel-in">
                            <div class="panel-title">IN DETAILS</div>
                            <div id="content-in"><span style="color:#cbd5e1">No Record</span></div>
                        </div>
                        <div class="panel-box" id="panel-out">
                            <div class="panel-title">OUT DETAILS</div>
                            <div id="content-out"><span style="color:#cbd5e1">No Record</span></div>
                        </div>
                    </div>
                    <button id="btn-checkin" type="button">Check-in Now</button>
                </div>
            </div>
        `;

        $(frm.fields_dict.html.wrapper).html(html_content);

        frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, ['name', 'employee_name', 'image'], (r) => {
            if (r) {
                frm.set_value('employee', r.name);
                if (r.image) $(frm.wrapper).find('#emp-photo').attr('src', r.image);
                $(frm.wrapper).find('#emp-greeting').text(r.employee_name);

                frappe.db.get_value('Attendance', {
                    'employee': r.name,
                    'docstatus': ['!=', 2],
                    'attendance_date': frm.doc.attendance_date
                }, 'name', (att) => {
                    const link_element = $(frm.wrapper).find('#att-id-link');
                    if (att && att.name) {
                        link_element.text(att.name)
                            .attr('href', `/app/attendance/${att.name}`)
                            .css('visibility', 'visible');
                    } else {
                        link_element.text("No Attendance Record Yet").css('color', '#94a3b8');
                        link_element.removeAttr('href');
                    }
                });

                _update_ui_from_history(frm);
            }
        });

        $(frm.fields_dict.html.wrapper).on('click', '#btn-checkin', () => {
            if (frm.is_new()) {
                frm.save().then(() => open_attachment_dialog(frm));
            } else {
                open_attachment_dialog(frm);
            }
        });
    }
});

/**
 * CORE LOCATION UPDATE
 * Address is resolved SERVER-SIDE only.
 * We pass lat/lng to the backend; the backend calls Google Geocoding API.
 */

function _process_checkin_with_location(frm, employee_id, score) {
    frappe.show_alert({ message: __('Fetching High-Accuracy Location...'), indicator: 'blue' });

    navigator.geolocation.getCurrentPosition(
        async function (pos) {
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;

            console.log("Accuracy: " + pos.coords.accuracy + " meters");

            // Address is now resolved entirely server-side via Google Maps Geocoding API.
            // We pass empty string here; backend will resolve it.
            frappe.show_alert({ message: __('Marking Attendance...'), indicator: 'blue' });

            frappe.call({
                method: 'hrpro.hrpro.doctype.mark_attendance.mark_attendance.create_employee_checkin',
                args: {
                    employee_id: employee_id,
                    selfie_url: frm.doc.check_in,
                    score: score,
                    latitude: lat,
                    longitude: lng,
                    address: frm.doc.address,       // Always let server resolve address
                    device_id: _getDeviceId()
                },
                callback: function (r) {
                    if (r.message && r.message.status === 'success') {
                        _update_ui_from_history(frm);
                        frappe.show_alert({ message: __('Attendance marked successfully'), indicator: 'green' });
                    }
                }
            });
        },
        function (error) {
            handle_location_errors(error, frm, employee_id, score);
        },
        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }
    );
}

function handle_location_errors(error, frm, employee_id, score) {
    if (error.code === error.PERMISSION_DENIED) {
        frappe.msgprint(__('Location permission denied. Please enable location in your browser settings.'));
    } else if (error.code === error.TIMEOUT) {
        frappe.show_alert({ message: __('GPS Timeout. Retrying...'), indicator: 'orange' });
        setTimeout(() => _process_checkin_with_location(frm, employee_id, score), 1000);
    } else {
        frappe.msgprint(__('Unable to determine location. Please move to an open area.'));
    }
}

function _update_ui_from_history(frm) {
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Employee Checkin',
            filters: {
                employee: frm.doc.employee,
                time: ['between', [frappe.datetime.now_date() + ' 00:00:00', frappe.datetime.now_date() + ' 23:59:59']]
            },
            fields: ['log_type', 'time', 'latitude', 'longitude', 'custom_address', 'custom_distance_from_office'],
            order_by: 'time asc'
        },
        callback: function (r) {
            let has_in = false;
            let has_out = false;
            const $w = $(frm.wrapper);

            if (r.message) {
                r.message.forEach(log => {
                    let detail_html = `
                        <div class="data-row"><span class="data-label">DateTime</span><span class="data-val">${frappe.datetime.str_to_user(log.time)}</span></div>
                        <div class="data-row"><span class="data-label">Location</span><span class="data-val">${log.latitude}, ${log.longitude}</span></div>
                        <div class="data-row"><span class="data-label">Distance</span><span class="data-val">${log.custom_distance_from_office || '0'} km</span></div>
                        <div class="data-row"><span class="data-label">Address</span><span class="data-val">${log.custom_address || 'N/A'}</span></div>
                    `;

                    if (log.log_type === 'IN') {
                        has_in = true;
                        $w.find('#content-in').html(detail_html);
                        $w.find('#doc-status').text('CHECK IN MARKED').css('color', '#10b981');
                    } else if (log.log_type === 'OUT') {
                        has_out = true;
                        $w.find('#content-out').html(detail_html);
                        $w.find('#doc-status').text('CHECK OUT MARKED').css('color', '#ef4444');
                    }
                });
            }

            const checkin_btn = $w.find('#btn-checkin');
            if (!has_in) {
                checkin_btn.text('Check-in Now').removeClass('btn-checkout').show();
            } else if (has_in && !has_out) {
                checkin_btn.text('Check-out Now').addClass('btn-checkout').show();
            } else {
                checkin_btn.hide();
            }
        }
    });
}

function open_attachment_dialog(frm) {
    new frappe.ui.FileUploader({
        doctype: frm.doctype,
        docname: frm.docname,
        on_success: (file) => {
            const selfie_url = file.file_url;
            const field_to_update = !frm.doc.check_in ? "check_in" : "check_out";

            frm.set_value(field_to_update, selfie_url);
            frm.save().then(() => {
                frappe.call({
                    method: 'hrpro.hrpro.doctype.mark_attendance.mark_attendance.identify_employee_from_image',
                    args: { selfie_url: selfie_url },
                    freeze: true,
                    freeze_message: __("Verifying Face..."),
                    callback: function (r) {
                        if (r.message && r.message.status === 'success') {
                            _process_checkin_with_location(frm, r.message.employee_id, r.message.match_score);
                        } else {
                            frappe.msgprint(r.message ? r.message.message : __('Face not recognized.'));
                        }
                    }
                });
            });
        }
    });
}

function _getDeviceId() {
    let id = localStorage.getItem('att_device_id') || 'dev_' + Math.random().toString(36).substring(2, 15);
    localStorage.setItem('att_device_id', id);
    return id;
}