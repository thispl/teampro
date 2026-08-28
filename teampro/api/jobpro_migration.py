import frappe
import json
import requests
from frappe.utils import cint, now_datetime

@frappe.whitelist()
def get_candidate_settings():
    """Returns saved JobPro connection settings."""
    settings = frappe.get_single("Candidate Settings")
    return {
        "jobpro_server_url": settings.get("jobpro_server_url") or "https://jobpro.in",
        "jobpro_api_key": settings.get("jobpro_api_key") or "",
        "has_api_secret": bool(settings.get("jobpro_api_secret")),
        "last_migration_date": str(settings.get("last_migration_date") or "")
    }

@frappe.whitelist()
def start_candidate_migration_to_jobpro(limit=10):
    """
    Enqueues candidate migration for a specified batch limit (default: latest 10).
    """
    settings = frappe.get_single("Candidate Settings")
    server_url = (settings.get("jobpro_server_url") or "https://jobpro.in").strip().rstrip("/")
    if not server_url:
        frappe.throw("JobPro Server URL is not configured. Please configure it in Candidate Settings.")

    limit = cint(limit)
    if limit is None:
        limit = 10

    unmigrated_count = frappe.db.count("Candidate", filters={"migrated": ["in", [0, None]]})
    if unmigrated_count == 0:
        return {
            "status": "completed",
            "message": "All candidates are already marked as Migrated (Migrated ? = 1)."
        }

    target_count = min(limit, unmigrated_count) if limit > 0 else unmigrated_count

    # Enqueue background worker with limit
    frappe.enqueue(
        "teampro.api.jobpro_migration.run_migration_background_worker",
        queue="long",
        timeout=7200,
        limit=limit,
        user=frappe.session.user
    )

    return {
        "status": "queued",
        "total": target_count,
        "message": f"Started migration of latest {target_count} candidate(s) in the background."
    }


def run_migration_background_worker(limit=10, user=None):
    """Background task executing migration for the specified candidate batch."""
    settings = frappe.get_single("Candidate Settings")
    server_url = (settings.get("jobpro_server_url") or "https://jobpro.in").strip().rstrip("/")
    auth_key = settings.get("jobpro_api_key") or ""
    auth_secret = settings.get_password("jobpro_api_secret") or ""

    target_endpoint = f"{server_url}/api/method/jobpro.api.candidate_sync.receive_candidate_from_teampro"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if auth_key and auth_secret:
        headers["Authorization"] = f"token {auth_key.strip()}:{auth_secret.strip()}"

    limit = cint(limit)
    limit_clause = f"LIMIT {limit}" if limit > 0 else ""

    # Fetch latest unmigrated candidates by creation DESC
    candidate_names = frappe.db.sql_list(f"""
        SELECT name FROM `tabCandidate`
        WHERE IFNULL(migrated, 0) = 0
        ORDER BY creation DESC
        {limit_clause}
    """)

    total = len(candidate_names)
    migrated_count = 0
    error_count = 0
    current_site_url = frappe.utils.get_url()

    for cand_name in candidate_names:
        try:
            doc = frappe.get_doc("Candidate", cand_name)
            cand_dict = doc.as_dict()
            cand_dict["site_url"] = current_site_url

            # Serialize child tables
            if hasattr(doc, "table_28") and doc.table_28:
                cand_dict["table_28"] = [child.as_dict() for child in doc.table_28]
            if hasattr(doc, "payment_details") and doc.payment_details:
                cand_dict["payment_details"] = [child.as_dict() for child in doc.payment_details]

            resp = requests.post(
                target_endpoint,
                headers=headers,
                data=json.dumps({"candidate_data": cand_dict, "site_url": current_site_url}, default=str),
                timeout=60
            )

            if resp.status_code == 200:
                res_data = resp.json()
                msg = res_data.get("message") or {}
                if msg.get("status") == "success" or res_data.get("status") == "success":
                    frappe.db.set_value("Candidate", cand_name, {
                        "migrated": 1,
                        "error_log": ""
                    }, update_modified=False)
                    frappe.db.commit()
                    migrated_count += 1
                else:
                    error_msg = msg.get("message") or str(res_data)
                    frappe.db.set_value("Candidate", cand_name, {
                        "migrated": 0,
                        "error_log": f"JobPro Response Error: {error_msg}"
                    }, update_modified=False)
                    frappe.db.commit()
                    error_count += 1
            else:
                error_msg = f"HTTP {resp.status_code}: {resp.text[:300]}"
                frappe.db.set_value("Candidate", cand_name, {
                    "migrated": 0,
                    "error_log": error_msg
                }, update_modified=False)
                frappe.db.commit()
                error_count += 1

        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            frappe.log_error(f"Migration error for {cand_name}: {error_msg}", "Candidate Migration")
            frappe.db.set_value("Candidate", cand_name, {
                "migrated": 0,
                "error_log": error_msg
            }, update_modified=False)
            frappe.db.commit()
            error_count += 1

    # Update Candidate Settings with statistics
    try:
        settings.last_migration_date = now_datetime()
        settings.last_migration_summary = f"Tested Batch: {total}, Migrated: {migrated_count}, Errors: {error_count}"
        settings.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        pass

    # Send completion popup to user
    if user:
        frappe.publish_realtime(
            event="msgprint",
            message=f"Candidate Batch Migration Complete! Migrated: {migrated_count}, Errors: {error_count} (out of {total} candidates).",
            user=user
        )
