// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mass WhatsApp Broadcast", {
	refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Send WhatsApp Message", function() {
                frappe.call({
                    method: "teampro.teampro.doctype.mass_whatsapp_broadcast.mass_whatsapp_broadcast.send_whatsapp_messages",
                    args: {
                        docname: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: "Sending WhatsApp Messages..."
                });
            });
        }
    }
});
