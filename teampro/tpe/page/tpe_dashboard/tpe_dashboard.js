frappe.pages['tpe-dashboard'].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: __('TPE Performance Dashboard'),
    single_column: true,
  });

  // Determine view based on roles
  var view = 'employee';
  if (frappe.user.has_role('Director')) view = 'director';
  else if (frappe.user.has_role('Manager') || frappe.user.has_role('HR Manager') || frappe.user.has_role('Projects Manager')) view = 'manager';

  $(wrapper).find('.layout-main-section').html(
    frappe.render_template('tpe_dashboard', { view: view })
  );

  var $container = $(wrapper).find('.tpe-dashboard');

  // Period selector
  page.add_field({
    fieldname: 'period',
    label: __('Period'),
    fieldtype: 'Select',
    options: 'Monthly\nQuarterly\nHalf Yearly\nYearly',
    default: 'Monthly',
    change: function () { load(); },
  });

  function load() {
    var period = page.get_field('period').get_value();
    var method = 'tpe.api.' + view + '_view';
    frappe.call({
      method: method,
      args: { period: period },
      callback: function (r) {
        if (!r || !r.message) return;
        render(view, r.message);
      },
    });
  }

  function render(v, data) {
    var html = '';
    if (v === 'employee') html = render_employee(data);
    else if (v === 'manager') html = render_manager(data);
    else html = render_director(data);
    $container.html(html);
  }

  function render_employee(d) {
    var r = d.rating || {};
    if (!r.name) return '<div class="text-muted">' + __('No performance rating found for this period. Click Calculate to generate.') + '</div>' +
      '<button class="btn btn-primary btn-sm mt-2" onclick="tpe_calculate()">' + __('Calculate Now') + '</button>';
    var trend = (d.trend || []).map(function (t) { return t.pr || 0; }).join(',');
    var kra = (r.kra_scores || []).map(function (k) {
      return '<tr><td>' + k.kra_name + '</td><td class="text-right">' + (k.score || 0) + '</td><td class="text-right">' + (k.weightage || 0) + '</td></tr>';
    }).join('');
    return '' +
      '<div class="row">' +
        '<div class="col-md-3"><div class="tpe-card"><div class="tpe-label">' + __('Overall PR') + '</div><div class="tpe-value">' + (r.overall_pr || 0) + '</div></div></div>' +
        '<div class="col-md-3"><div class="tpe-card"><div class="tpe-label">' + __('Department Rank') + '</div><div class="tpe-value">' + (d.rank || '-') + '</div></div></div>' +
        '<div class="col-md-3"><div class="tpe-card"><div class="tpe-label">' + __('Energy Points') + '</div><div class="tpe-value">' + (r.energy_points || 0) + '</div></div></div>' +
        '<div class="col-md-3"><div class="tpe-card"><div class="tpe-label">' + __('Non Conformities') + '</div><div class="tpe-value">' + (r.non_conformities || 0) + '</div></div></div>' +
      '</div>' +
      '<div class="row mt-3"><div class="col-md-6"><canvas id="tpe-trend" height="120"></canvas></div>' +
      '<div class="col-md-6"><div class="tpe-sub">' + __('Strength') + '</div><div>' + (r.strength || '-') + '</div>' +
      '<div class="tpe-sub mt-2">' + __('Improvement Area') + '</div><div>' + (r.improvement_area || '-') + '</div></div></div>' +
      '<h6 class="mt-3">' + __('KRA Scores') + '</h6><table class="table table-sm"><thead><tr><th>KRA</th><th class="text-right">Score</th><th class="text-right">Weightage</th></tr></thead><tbody>' + kra + '</tbody></table>' +
      '<button class="btn btn-secondary btn-sm mt-2" onclick="tpe_calculate()">' + __('Recalculate') + '</button>';
  }

  function render_manager(d) {
    var rows = (d.reportees || []).map(function (e) {
      return '<tr><td>' + e.employee_name + '</td><td class="text-right">' + (e.current_pr != null ? e.current_pr : '-') + '</td><td class="text-right">' + (e.rank != null ? e.rank : '-') + '</td><td>' + (e.strength || '-') + '</td><td>' + (e.improvement_area || '-') + '</td></tr>';
    }).join('');
    return '' +
      '<div class="row"><div class="col-md-4"><div class="tpe-card"><div class="tpe-label">' + __('Reportees') + '</div><div class="tpe-value">' + (d.reportees || []).length + '</div></div></div>' +
      '<div class="col-md-4"><div class="tpe-card"><div class="tpe-label">' + __('Department Average') + '</div><div class="tpe-value">' + (d.department_average || 0) + '</div></div></div>' +
      '<div class="col-md-4"><div class="tpe-card"><div class="tpe-label">' + __('Pending Reviews') + '</div><div class="tpe-value">' + (d.pending_reviews || []).length + '</div></div></div></div>' +
      '<h6 class="mt-3">' + __('Reportees') + '</h6><table class="table table-sm"><thead><tr><th>Employee</th><th class="text-right">PR</th><th class="text-right">Rank</th><th>Strength</th><th>Improvement Area</th></tr></thead><tbody>' + rows + '</tbody></table>';
  }

  function render_director(d) {
    var dist = (d.distribution || []).map(function (b) {
      return '<div class="tpe-band"><span>' + b.band + '</span><span class="badge">' + b.count + '</span></div>';
    }).join('');
    var top = (d.top_10 || []).map(function (e) {
      return '<tr><td>' + e.employee_name + '</td><td>' + (e.department || '-') + '</td><td class="text-right">' + (e.overall_pr || 0) + '</td></tr>';
    }).join('');
    var bottom = (d.bottom_10 || []).map(function (e) {
      return '<tr><td>' + e.employee_name + '</td><td>' + (e.department || '-') + '</td><td class="text-right">' + (e.overall_pr || 0) + '</td></tr>';
    }).join('');
    return '' +
      '<div class="row"><div class="col-md-4"><div class="tpe-card"><div class="tpe-label">' + __('Total Rated') + '</div><div class="tpe-value">' + (d.total_rated || 0) + '</div></div></div>' +
      '<div class="col-md-8"><div class="tpe-card"><div class="tpe-label">' + __('Distribution') + '</div>' + dist + '</div></div></div>' +
      '<div class="row mt-3"><div class="col-md-6"><h6>' + __('Top 10') + '</h6><table class="table table-sm"><thead><tr><th>Employee</th><th>Dept</th><th class="text-right">PR</th></tr></thead><tbody>' + top + '</tbody></table></div>' +
      '<div class="col-md-6"><h6>' + __('Bottom 10') + '</h6><table class="table table-sm"><thead><tr><th>Employee</th><th>Dept</th><th class="text-right">PR</th></tr></thead><tbody>' + bottom + '</tbody></table></div></div>';
  }

  load();
};

window.tpe_calculate = function () {
  frappe.call({
    method: 'tpe.api.calculate',
    args: { period: 'Monthly' },
    freeze: true,
    callback: function (r) {
      if (r && r.message) {
        frappe.msgprint(__('Calculation complete'));
        frappe.pages['tpe-dashboard'].on_page_load($('.tpe-dashboard').closest('.page-container')[0]);
      }
    },
  });
};
