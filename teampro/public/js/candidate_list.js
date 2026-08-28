frappe.provide('frappe.listview_settings');

frappe.listview_settings['Candidate'] = {
    onload: function (listview) {
        listview.page.add_action_item(__('Migrate'), function () {
            show_candidate_migration_dialog(listview);
        });
        listview.page.add_inner_button(__('Migrate'), function () {
            show_candidate_migration_dialog(listview);
        });
    },
    refresh: function (listview) {
        if (!listview.page.custom_actions.find('button:contains("Migrate")').length && !listview.page.inner_toolbar.find('button:contains("Migrate")').length) {
            listview.page.add_inner_button(__('Migrate'), function () {
                show_candidate_migration_dialog(listview);
            });
        }
    }
};

function show_candidate_migration_dialog(listview) {
    frappe.call({
        method: 'teampro.api.jobpro_migration.get_candidate_settings',
        callback: function (r) {
            let settings = r.message || {};
            let server_url = settings.jobpro_server_url || 'https://jobpro.in';
            let description_html = `
                <div style="padding: 10px; font-size: 13px; line-height: 1.6;">
                    <div style="margin-bottom: 12px; font-weight: 600; color: var(--text-color, #1f272e);">
                        ${__('Candidate Migration to JOBPRO Server')}
                    </div>
                    <p style="margin-bottom: 10px; color: var(--text-muted, #6c7680);">
                        ${__('This process runs in the background. It will migrate the latest unmigrated candidates (<code>Migrated ? = 0</code>) to the target JOBPRO server.')}
                    </p>
                    <ul style="margin-bottom: 12px; padding-left: 20px; color: var(--text-muted, #6c7680);">
                        <li><b>${__('Target Server')}</b>: <code>${server_url}</code></li>
                        <li><b>${__('Execution Mode')}</b>: ${__('Background Job (Non-blocking)')}</li>
                        <li><b>${__('Target Scope')}</b>: ${__('Latest unmigrated candidates by creation date.')}</li>
                        <li><b>${__('Error Handling')}</b>: ${__('Recorded in the candidate\'s <code>Error Log</code> field.')}</li>
                        <li><b>${__('Success Update')}</b>: ${__('Marked as <code>Migrated ? = 1</code>.')}</li>
                    </ul>
                    <div class="alert alert-warning" style="margin-bottom: 0; padding: 8px 12px; font-size: 12px; border-radius: 4px;">
                        ${__('Are you sure you want to start the background candidate migration?')}
                    </div>
                </div>
            `;
            let d = new frappe.ui.Dialog({
                title: __('Migrate Candidates to JOBPRO'),
                fields: [
                    {
                        fieldtype: 'HTML',
                        fieldname: 'migration_description',
                        options: description_html
                    },
                    {
                        fieldtype: 'Section Break'
                    },
                    {
                        fieldtype: 'Int',
                        fieldname: 'batch_limit',
                        label: __('Batch Limit (Latest Candidates)'),
                        default: 10,
                        description: __('Enter 0 to migrate all unmigrated candidates.')
                    }
                ],
                primary_action_label: __('Confirm & Migrate in Background'),
                primary_action: function (values) {
                    d.hide();
                    frappe.call({
                        method: 'teampro.api.jobpro_migration.start_candidate_migration_to_jobpro',
                        args: {
                            limit: values ? values.batch_limit : 10
                        },
                        callback: function (res) {
                            if (res.message) {
                                let r = res.message;
                                frappe.show_alert({
                                    message: __(r.message),
                                    indicator: r.status === 'completed' ? 'green' : 'blue'
                                }, 10);
                                if (listview) {
                                    listview.refresh();
                                }
                            }
                        }
                    });
                },
                secondary_action_label: __('Configure Settings'),
                secondary_action: function () {
                    d.hide();
                    frappe.set_route('Form', 'Candidate Settings');
                }
            });
            d.show();
        }
    });
}

$(document).on('page-change', function () {
    if (frappe.get_route && frappe.get_route()[0] === 'List' && frappe.get_route()[1] === 'Candidate') {
        if (window.cur_list && cur_list.doctype === 'Candidate' && cur_list.page) {
            if (!cur_list.page.custom_actions.find('button:contains("Migrate")').length && !cur_list.page.inner_toolbar.find('button:contains("Migrate")').length) {
                cur_list.page.add_inner_button(__('Migrate'), function () {
                    show_candidate_migration_dialog(cur_list);
                });
            }
        }
    }
});
