# Project Monitoring Tab

A management dashboard embedded in the ERPNext **Project** form as a dedicated
**Project Monitoring** tab. Implemented entirely in the `teampro` custom app —
no ERPNext core changes, no new DocTypes, no schema migrations.

## Files

| File | Purpose |
|---|---|
| `teampro/public/js/project_monitoring.js` | Tab injection, dashboard rendering, filters, charts, tables, remarks/daily-update UI |
| `teampro/public/css/project_monitoring.css` | All dashboard styling (loaded via injected `<link>`) |
| `teampro/teampro_py/project_monitoring.py` | Backend API: aggregation, billing, currency conversion, remarks/daily-update writes |
| `teampro/custom/project.json` | Property setter `Project-sales_order-hidden = 0` (unhides the standard SO link) |

`hooks.py` registers the JS via `doctype_js` and the dashboard override
(`get_project_dashboard` adds Meeting to Project dashboard connections).

## Scope / Gating

- Tab is injected **only when `Project.service == "IT-SW"`** (`SERVICE` constant in JS).
- Tasks are filtered by `service` server-side when the field exists.
- **Cancelled tasks are excluded entirely** server-side — they do not appear in
  any count, chart, aging bucket, hours aggregate, assignee option, table row,
  or CSV export. Cancelled meetings are still shown.

## Backend APIs

All in `teampro.teampro_py.project_monitoring`:

- `get_project_monitoring_data(project, service=None, display_currency=None)`
  — single consolidated payload: project meta, KPIs, billing, status/aging
  counts & hours, tasks, meetings, remarks, daily updates, currency list.
- `add_project_remark(project, remark)` — saves a Frappe **Comment**
  (subject `"Project Remark"`) on the Project.
- `add_daily_update(project, progress, completed, issues, plan)` — saves a
  Comment with subject `"Daily Project Update"`; one per day (second submit
  for the same date is rejected).
- `get_project_dashboard(data)` — adds Meeting to Project dashboard links.

Permissions: Task/Meeting/ToDo use `frappe.get_list` (permission-aware);
comments require read permission on the Project.

## Dashboard layout (top → bottom)

1. Header — project name, status/priority/progress badges, customer, project
   manager, **SPOC = `spoc`**, type, dates + currency selector,
   Refresh, Export.
2. **Summary cards** — Open Tasks (hrs+count), Working Tasks (hrs+count),
   Meetings (In Progress/Total), Days to End (shows "Overdue"), Balance Hrs.
3. **Charts** — Task Status donut (by hours), Meeting Status donut (by count),
   Task Aging stacked bars (by hours, per status). Donuts hide statuses listed
   in `CHART_EXCLUDE` (tasks: `["Completed"]`; meetings: `MEETING_CHART_EXCLUDE`
   = `["Completed", "Cancelled"]`, all other statuses shown); excluded statuses
   remain available in the filter dropdown and table.
4. **Estimated vs Actual Hours** — comparison bars + burn-rate vs required
   pace line (left column of a 2-col row).
5. **Project Financials (From Sales Orders)** — label-value rows: SO - Value,
   Billed - Value, To Bill, Collection Pending (right column), plus
   projected final cost and collection aging below the rows.
6. **Project Health** — clickable flag chips: Overdue, Stale >7d, On Hold,
   Client Review >7d, Milestones Overdue, Reopened, High Rework (≥10
   versions), Scope Added (created after project start), Action Items
   Overdue (open Meeting Minutes past `complete_by`).
7. **Task Monitoring** — #, Task, Issue Type, Allocated To, Status, Priority,
   Age, ET, RT, View; **MultiSelectList** filters (status/priority/assignee/
   issue-type/age) + search, sortable columns, pagination (25/page).
   Closed tasks (Completed/Cancelled/Template) are hidden by default; select
   that status in the filter to view.
8. **Meeting Monitoring** — #, Meeting, Date, Owner, Participants, Age,
   Status, View; multiselect status + age filters + search. Completed/
   Cancelled meetings are hidden by default; select the status to view.
9. **Project Remarks** — textarea + Update.
10. **Recent Remarks / Daily Updates** timeline — newest first.

## Billing & currency logic

- **SO value** = `Project.total_sales_amount` (SOs linked via `SO.project`)
  + `base_net_total` of the SO selected in `Project.sales_order`.
- **Billed value** = `total_billed_amount` + `base_net_amount` of SI items
  referencing the selected SO.
- **To Bill** (label; `outstanding_amount` key) = SO value − billed (unbilled).
- **Collection pending** = Σ `outstanding_amount` on submitted SIs (project-
  linked and/or linked to the selected SO via items), converted from the
  receivable-account currency using `conversion_rate`.
- **Display currency**: toolbar dropdown; server converts each amount from its
  own company currency via `tabCurrency Exchange` (latest rate, reverse-rate
  fallback). Missing rates → amber warning note, amount passes unconverted.
- **Collection aging** — outstanding split into 0–30 / 31–60 / 60+ day buckets
  (project-linked and selected-SO invoices combined, converted).
- **Projected final cost** — actual cost + balance hrs × (actual cost ÷ actual
  hrs), shown in the Budget Utilization panel with an over-budget badge.
- **Countdown** — live timer in the header counting down to Expected End Date;
  flips to "Overdue by …" when past.

## Configurable constants

JS (`project_monitoring.js`):
- `HOURS_STATUSES` — statuses on the hours-based charts (site's actual statuses).
- `CHART_EXCLUDE` — statuses hidden from the task donut (`["Completed"]`).
- `MEETING_CHART_EXCLUDE` — statuses hidden from the meeting donut
  (`["Completed", "Cancelled"]`).
- `STATUS_SORT` — default task-table order: Open, Working, Pending Review,
  Code Review, Client Review, Hold, Overdue; unlisted statuses after, closed
  last; ties broken by age desc.
- `STATUS_HEX`, `AGING_HEX`, `PAGE_SIZE` (25), `SERVICE` ("IT-SW").

Python (`project_monitoring.py`):
- `HOURS_STATUSES` — not currently used server-side (JS-side list governs).
- `OPEN_TASK_REQUIRES_NO_ESTIMATE` — Open Tasks card counts all Open tasks'
  estimated hrs+count (default `False`); set `True` to count only tasks with
  empty `expected_time`.
- `AGING_BUCKETS`, `REMARK_SUBJECT`, `DAILY_UPDATE_SUBJECT`.

## Field mappings used

| UI | Source |
|---|---|
| ET / RT | `Task.expected_time` / `max(expected_time − actual_time, 0)` (+overrun shown) |
| Issue Type | `Task.custom_issue_type` (falls back to `Task.type`) |
| Allocated To | `Task.custom_allocated_to` |
| Balance Hrs | `Σ expected_time − Σ actual_time` (can be negative = overrun) |
| Meeting link | `Meeting.project` (custom field) |
| Task/Meeting age | active: `today − (act_start or exp_start or creation)`; closed: `(completed_on or act_end or modified) − start` |
| Remarks/Daily updates | `tabComment` on Project, keyed by `subject` |

## Assumptions / decisions

- "ER"/"Current Review" don't exist on this site → mapped to `Code Review`/
  `Client Review`; status lists are config constants.
- "Open tasks, estimated empty" → `expected_time` empty; flag above.
- SPOC = `spoc` custom field on Project.
- Cross-company SO: converted from the SO's company currency via Currency
  Exchange — requires a rate record for that pair.
- `Project.sales_order` link filter relaxed in JS (stock ERPNext restricts the
  dropdown to matching company/customer).

## Ops notes

- **No `bench migrate` needed** — no schema changes; remarks/updates use Comments.
- After Python changes: `bench restart`. After JS/CSS: hard refresh
  (Ctrl+Shift+R). CSS link carries a `?v=` cache-buster — bump on deploys.
- Asset served at `/assets/teampro/css/project_monitoring.css`
  (`sites/assets/teampro` → `teampro/public` symlink).
