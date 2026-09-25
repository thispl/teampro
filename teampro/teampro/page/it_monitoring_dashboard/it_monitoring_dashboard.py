# IT Monitoring Dashboard — Page controller
#
# This page reuses the backend endpoints already defined in
# teampro.teampro.page.new_it_dashboard.new_it so that no DB / schema
# changes are introduced.  All data fetching is delegated to that module.
#
# The JS front-end calls the whitelisted methods directly via frappe.call,
# so this Python file intentionally stays minimal.

import frappe
from frappe.utils import getdate, nowdate


@frappe.whitelist()
def get_default_sprint():
    """Return the default (latest in-progress) sprint id for the sprint filter."""
    from teampro.teampro.page.new_it_dashboard.new_it import update_sprint_filter
    return update_sprint_filter()


@frappe.whitelist()
def get_dsr_data(date=None, team=None):
    """Return structured DSR data for the Production Summary section.

    Groups tasks by team → CB and includes per-CB totals (total_rt,
    completed_rt, completed_at, aph) so the front-end can render
    P% / E% and a Total RT column per CB group.
    """
    from collections import defaultdict

    if not date:
        date = nowdate()

    # ---- Dev team order ----
    dev_team_order = {}
    dev_teams = frappe.get_all("Dev Team", fields=["name", "order_for_it_dashboard"])
    for d in dev_teams:
        dev_team_order[d.name] = d.order_for_it_dashboard or 999

    # ---- CB order + APH map ----
    cb_order = {}
    cb_aph_map = {}
    employees = frappe.get_all(
        "Employee",
        {"status": "Active", "department": "IT. Development - THIS"},
        ["short_code", "custom_order_for_it_dashboard", "custom_aph"]
    )
    for e in employees:
        short_code = (e.short_code or "").strip().upper()
        cb_order[short_code] = e.custom_order_for_it_dashboard or 999
        if short_code and e.custom_aph is not None:
            cb_aph_map[short_code] = float(e.custom_aph or 0)

    # ---- Daily Monitor task_details ----
    dm_filters = {"date": date, "service": "IT-SW"}
    if team:
        dm_filters["dev_team"] = team

    daily_monitors = frappe.get_all(
        "Daily Monitor",
        dm_filters,
        ["name", "dev_team", "sprint"]
    )

    all_tasks = []
    for dm in daily_monitors:
        doc = frappe.get_doc("Daily Monitor", dm.name)
        for row in doc.task_details:
            row.dev_team = dm.dev_team
            row.sprint = dm.sprint
            all_tasks.append(row)

    if not all_tasks:
        return {"teams": [], "date": date}

    # ---- Sort ----
    sorted_tasks = sorted(
        all_tasks,
        key=lambda x: (
            dev_team_order.get(x.dev_team, 999),
            cb_order.get((x.cb or "").strip().upper(), 999),
            (x.cb or "").strip().upper(),
            x.project_name or "",
            x.priority or ""
        )
    )

    completed_statuses = ("Completed", "Pending Review", "Client Review")

    # ---- Group by team → CB ----
    team_order_list = []
    team_map = {}
    for t in sorted_tasks:
        tname = t.dev_team or "Unassigned"
        if tname not in team_map:
            team_map[tname] = []
            team_order_list.append(tname)
        team_map[tname].append(t)

    teams_out = []
    for tname in team_order_list:
        tasks = team_map[tname]

        # CB stats for this team
        cb_stats = defaultdict(lambda: {"total_rt": 0, "completed_rt": 0, "completed_at": 0})
        for t in tasks:
            cb = (t.cb or "").strip().upper()
            rt = float(t.rt or 0)
            at = float(t.at_taken or 0)
            cb_stats[cb]["total_rt"] += rt
            if (t.current_status or "") in completed_statuses:
                cb_stats[cb]["completed_rt"] += rt
                cb_stats[cb]["completed_at"] += at

        # Group tasks by CB within this team
        cb_order_list = []
        cb_map = {}
        for t in tasks:
            cb = (t.cb or "").strip().upper()
            if cb not in cb_map:
                cb_map[cb] = {"cb": cb, "aph": cb_aph_map.get(cb, 0), "tasks": []}
                cb_order_list.append(cb)
            cb_map[cb]["tasks"].append({
                "id": t.id,
                "project": t.project_name or "",
                "subject": t.subject or "",
                "cb": t.cb or "",
                "et": float(t.et or 0),
                "rt": float(t.rt or 0),
                "priority": t.priority or "",
                "status": t.current_status or "",
                "at_taken": float(t.at_taken or 0),
            })

        # Add computed totals per CB
        cbs_out = []
        for cb in cb_order_list:
            info = cb_map[cb]
            stats = cb_stats[cb]
            info["total_rt"] = round(stats["total_rt"], 2)
            info["completed_rt"] = round(stats["completed_rt"], 2)
            info["completed_at"] = round(stats["completed_at"], 2)
            info["aph"] = round(info["aph"], 2)
            info["p_pct"] = round(
                (stats["completed_rt"] / info["aph"]) * 100, 2
            ) if info["aph"] else 0
            info["e_pct"] = round(
                (stats["completed_at"] / stats["completed_rt"]) * 100, 2
            ) if stats["completed_rt"] else 0
            cbs_out.append(info)

        teams_out.append({"team": tname, "cbs": cbs_out})

    return {"teams": teams_out, "date": date}
