frappe.pages['accounts-checklist-manual'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Accounts Checklist - User Manual'),
        single_column: true,
    });

    $(wrapper).find('.layout-main-section').html(
        frappe.render_template('accounts_checklist_manual', {})
    );

    // Smooth scroll for TOC links
    $(wrapper).find('.acc-manual-toc a').on('click', function (e) {
        e.preventDefault();
        var target = $(this).attr('href');
        var $target = $(wrapper).find(target);
        if ($target.length) {
            $(wrapper).find('.acc-manual-body').animate({
                scrollTop: $target.position().top
            }, 400);
        }
    });

    // Print button
    page.add_menu_item(__('Print'), function () {
        window.print();
    });
};
