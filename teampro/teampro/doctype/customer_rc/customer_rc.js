// Copyright (c) 2026, TeamPRO and contributors
// For license information, please see license.txt

const TCS_REGEX = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[C]{1}[0-9A-Z]{1}$/;
const PAN_REGEX = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
frappe.ui.form.on("Customer RC", {
	onload(frm) {
        if(!frm.doc.whatsapp_no){

            frm.set_value("whatsapp_no", "+91-");
        }
        if(!frm.doc.contact_person_number){
            frm.set_value("contact_person_number", "+91-");
        }
        
        if (!frm.doc.__islocal) return;
        if (frm.doc.latitude && frm.doc.longitude) return;

        if (!navigator.geolocation) {
            frappe.throw(__('Geolocation is not supported by your browser.'));
        }

        // Set local datetime
        const now = new Date();
        frm.set_value('date_and_time', frappe.datetime.now_datetime());

        function get_high_accuracy_location(retry = false) {
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

                                const components = results[0].address_components;

                                let street = "";
                                let area = "";
                                let city = "";
                                let state = "";
                                let pincode = "";
                                let country = "";

                                components.forEach(component => {
                                    const types = component.types;

                                    if (types.includes("street_number")) {
                                        street = component.long_name + " ";
                                    }

                                    if (types.includes("route")) {
                                        street += component.long_name;
                                    }
                                    if (
                                        types.includes("sublocality") ||
                                        types.includes("sublocality_level_1") ||
                                        types.includes("sublocality_level_2") ||
                                        types.includes("sublocality_level_3")
                                    ) {
                                        area += component.long_name + ", ";
                                    }

                                    if (types.includes("locality")) {
                                        city = component.long_name;
                                    }

                                    if (types.includes("administrative_area_level_1")) {
                                        state = component.long_name;
                                    }

                                    if (types.includes("postal_code")) {
                                        pincode = component.long_name;
                                    }

                                    if (types.includes("country")) {
                                        country = component.long_name;
                                    }
                                });

                                if (!frm.doc.latitude) {
                                    frm.set_value('latitude', latitude);
                                }

                                if (!frm.doc.longitude) {
                                    frm.set_value('longitude', longitude);
                                }

                                if (!street || street.trim() === "") {
                                    let full_address = results[0].formatted_address;
                                    let parts = full_address.split(",").map(p => p.trim());

                                    if (parts.length >= 2) {
                                        street = parts[0] + ", " + parts[1];
                                    } else {
                                        street = parts[0];
                                    }
                                }

                                if (!frm.doc.address_line_1) {
                                    frm.set_value('address_line_1', street);
                                    frm.refresh_field('address_line_1');
                                }

                                if (!frm.doc.street) {
                                    frm.set_value('street', area);
                                    frm.refresh_field("street");
                                }

                                if (!frm.doc.city) {
                                    frm.set_value('city', city);
                                    frm.refresh_field('city');
                                }

                                if (!frm.doc.state) {
                                    frm.set_value('state', state);
                                    frm.refresh_field('state');
                                }

                                if (!frm.doc.postal_code) {
                                    frm.set_value('postal_code', pincode);
                                    frm.refresh_field('postal_code')
                                }

                                if (!frm.doc.country) {
                                    frm.set_value('country', country);
                                }

                                frm.set_value('gprs_location', results[0].formatted_address);

                            } else {
                                frappe.msgprint(__('Unable to fetch address. Try again.'));
                            }
                        }
                    );
                    
                },
                function (error) {
                    if (error.code === error.PERMISSION_DENIED) {
                        const siteSettingsUrl =
                            "chrome://settings/content/siteDetails?site=https%3A%2F%2Ferp.teamproit.com";
                    
                        window.copySiteSettingsLink = function () {
                            if (window.__site_settings_copied) return;
                    
                            navigator.clipboard.writeText(siteSettingsUrl).then(() => {
                                window.__site_settings_copied = true;
                    
                                const el = document.getElementById("site-settings-msg");
                                if (el) {
                                    el.innerHTML = "✔ Link copied! Paste it in Chrome address bar";
                                    el.style.color = "#16a34a"; 
                                    el.style.fontWeight = "600";
                                }
                            });
                        };
                    
                        frappe.throw({
                            title: __('Location Access Blocked'),
                            message: __(
                                'Location access is required to create this record.<br><br>' +
                                '<b>How to enable:</b><br>' +
                                '1. Open <b><a href="#" onclick="copySiteSettingsLink(); return false;">Site Settings</a></b><br>' +
                                '2. Enable <b>Location</b> for this site<br>' +
                                '3. Also make sure <b>Location</b> enabled in device<br>' +
                                '4. Refresh the page and try again<br><br>' +
                                '<div id="site-settings-msg" style="color:#6b7280;"></div>'
                            )
                        });
                    }



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
        }

        setTimeout(() => {
            get_high_accuracy_location();
        }, 2000);
    },
    before_save(frm) {
        if (!frm.doc.latitude || !frm.doc.longitude || !frm.doc.gprs_location) {
            frappe.throw(
                __('Location not captured. Please enable GPS and allow location access.Try Again')
            );
        }
    },
    wp(frm){
        window.location.href = "https://api.whatsapp.com/send?phone="+ frm.doc.whatsapp_no
    },
    wp_(frm){
        window.location.href = "https://api.whatsapp.com/send?phone="+ frm.doc.contact_person_number
    },
    // gst_no(frm){
    //     if (!frm.doc.gst_no || frm.doc.gst_no.length !== 15) {
    //         return; // DO NOT validate early
    //     }

    //     if (!TCS_REGEX.test(frm.doc.gst_no)) {
    //         frappe.throw("Invalid GSTIN format.");
    //     }
    // }
    
    gst_no(frm) {
            let gstin  = frm.doc.gst_no;

            // TODO: remove below condition once event is fixed in frappe
            if (!gstin || gstin.length < 15) return;

            if (gstin.length > 15) {
                frappe.throw(__("GSTIN/UIN should be 15 characters long"));
            }

            gstin = india_compliance.validate_gstin(gstin);
            console.log(gstin);

            if (TCS_REGEX.test(gstin)) {
                frappe.throw(__("e-Commerce Operator (TCS) GSTIN is not allowed to be set in Party/Address"));
            }

            frm.doc.gst_no = gstin;
            frm.refresh_field("gst_no");
            if (frm.get_field("gst_no")){
                india_compliance.set_gstin_status(frm.get_field("gst_no"));
            }

    
        },
    refresh(frm){
        if(!frm.doc.whatsapp_no){

            frm.set_value("whatsapp_no", "+91-");
        }
        if(!frm.doc.contact_person_number){
            frm.set_value("contact_person_number", "+91-");
        }
    }

});
