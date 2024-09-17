frappe.pages['scan-ca'].on_page_load = function (wrapper) {
    let me = this;
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Scan QR',
        single_column: true,
        card_layout: true
    });

    frappe.breadcrumbs.add('HR');

    
    frappe.call({
        method: 'teampro.teampro.page.scan_ca.ca_utils.get_qr_details',
        callback: function (r) {
            if (r.message) {
                let qr_details = r.message;
                page.main.html(frappe.render_template('scan_ca', { data: qr_details }));
            } else {
                frappe.msgprint(__('No QR details found.'));
            }
        }
    });
};
