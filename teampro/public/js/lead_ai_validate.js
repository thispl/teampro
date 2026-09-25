frappe.ui.form.on('Lead', {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('⚡ AI Validate Lead'), function () {
				frappe.call({
					method: 'teampro.lead_validation.validate_lead_ai',
					args: {
						lead_id: frm.doc.name,
					},
					freeze: true,
					freeze_message: __('Running AI Validation...'),
					callback: function (r) {
						if (r.exc) {
							frappe.msgprint(__('AI Validation failed: {0}', [r.exc]));
							return;
						}
						var result = r.message;
						var colorMap = {
							'green': 'green',
							'yellow': 'orange',
							'red': 'red',
							'gray': 'gray',
						};
						var indicator = colorMap[result.color] || 'gray';
						frappe.show_alert({
							message: __('AI Score: {0}/100 | Rating: {1} | Raw: {2}/6 | {3}', [result.score, result.rating, result.raw_score || 0, result.next_action]),
							indicator: indicator,
						}, 7);
						frm.reload_doc();
					},
				});
			}, __('Actions'));
		}
	},
});
