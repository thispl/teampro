import json
import requests
import frappe
from frappe import _
from frappe.utils import get_url


def _get_file_attachments(doctype: str, docname: str) -> list:
	"""
	Collects all files attached to a given document with absolute download URLs.
	"""
	if not doctype or not docname:
		return []

	files = frappe.get_all(
		"File",
		filters={
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
		},
		fields=["name", "file_name", "file_url", "is_private", "file_size"],
		order_by="creation desc",
	)

	results = []
	for f in files:
		file_url = f.get("file_url") or ""
		full_url = get_url(file_url) if file_url.startswith("/") else file_url
		if full_url:
			full_url = full_url.replace("http://", "https://")
		results.append({
			"file_name": f.get("file_name") or "",
			"file_url": file_url,
			"download_url": full_url,
			"is_private": bool(f.get("is_private")),
			"file_size": f.get("file_size"),
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
		})

	return results


def get_jobpro_credentials() -> tuple:
	"""
	Retrieves JobPro connection settings (URL, API Key, API Secret) from available configuration
	sources with the following priority:
	1. frappe.conf
	2. JobPro Settings (Single DocType if present)
	3. Candidate Settings (Single DocType if present)
	4. Default JobPro URL (https://jobpro.groupteampro.com)
	"""
	# 1. Check frappe.conf
	jobpro_url = (
		frappe.conf.get("jobpro_url")
		or frappe.conf.get("jobpro_server_url")
	)
	api_key = frappe.conf.get("jobpro_api_key")
	api_secret = frappe.conf.get("jobpro_api_secret")

	# 2. Check JobPro Settings (Single DocType)
	if frappe.db.exists("DocType", "JobPro Settings"):
		if not jobpro_url:
			jobpro_url = frappe.db.get_single_value("JobPro Settings", "jobpro_url")
		if not api_key:
			api_key = frappe.db.get_single_value("JobPro Settings", "jobpro_api_key")
		if not api_secret:
			api_secret = frappe.db.get_single_value("JobPro Settings", "jobpro_api_secret")

	# 3. Check Candidate Settings (Single DocType)
	if frappe.db.exists("DocType", "Candidate Settings"):
		if not jobpro_url:
			jobpro_url = frappe.db.get_single_value("Candidate Settings", "jobpro_server_url")
		if not api_key:
			api_key = frappe.db.get_single_value("Candidate Settings", "jobpro_api_key")
		if not api_secret:
			try:
				cand_settings = frappe.get_single("Candidate Settings")
				api_secret = cand_settings.get_password("jobpro_api_secret")
			except Exception:
				pass

	# 4. Fallback URL
	if not jobpro_url:
		jobpro_url = "https://jobpro.groupteampro.com"

	return (jobpro_url.strip().rstrip("/"), (api_key or "").strip(), (api_secret or "").strip())


def _is_migrated(doc) -> bool:
	return bool(doc.get("migrated") or doc.get("is_migrate"))


def _set_candidate_migrated(doc):
	if doc.meta.has_field("migrated") or hasattr(doc, "migrated") or frappe.db.has_column("Candidate", "migrated"):
		doc.db_set("migrated", 1)
	if doc.meta.has_field("is_migrate") or hasattr(doc, "is_migrate") or frappe.db.has_column("Candidate", "is_migrate"):
		doc.db_set("is_migrate", 1)
	frappe.db.commit()


def push_candidate_to_jobpro(doc, method=None):
	"""
	Triggered on Candidate after_insert hook.
	Enqueues background task to sync candidate to JobPro without blocking form save.
	"""
	if _is_migrated(doc):
		return

	frappe.enqueue(
		"teampro.custom_sync._enqueue_candidate_push",
		queue="short",
		candidate_name=doc.name,
		now=frappe.flags.in_test,
	)


def _enqueue_candidate_push(candidate_name: str):
	"""
	Background worker executing the push of a Candidate record to JobPro.
	"""
	try:
		if not frappe.db.exists("Candidate", candidate_name):
			return

		doc = frappe.get_doc("Candidate", candidate_name)
		if _is_migrated(doc):
			return

		candidate_data = doc.as_dict()

		# Ensure child tables are fully serialized
		if hasattr(doc, "table_28") and doc.table_28:
			candidate_data["table_28"] = [child.as_dict() for child in doc.table_28]
		if hasattr(doc, "payment_details") and doc.payment_details:
			candidate_data["payment_details"] = [child.as_dict() for child in doc.payment_details]

		# Collect attachment metadata
		attachments = _get_file_attachments("Candidate", candidate_name)
		if attachments:
			candidate_data["attachments"] = attachments

		# Retrieve JobPro credentials
		jobpro_url, api_key, api_secret = get_jobpro_credentials()

		if not api_key or not api_secret:
			frappe.log_error(
				title="JobPro Candidate Push Failed",
				message=f"JobPro API credentials missing when attempting to push Candidate {candidate_name}.",
			)
			return

		headers = {
			"Authorization": f"token {api_key}:{api_secret}",
			"Content-Type": "application/json",
			"Accept": "application/json",
		}

		endpoint = f"{jobpro_url}/api/method/jobpro.api.candidate_sync.receive_candidate_from_teampro"
		site_url = (frappe.utils.get_url() or "https://erp.teamproit.com").replace("http://", "https://")

		candidate_data["site_url"] = site_url
		payload = {
			"candidate_data": candidate_data,
			"site_url": site_url,
		}

		# Use default=str to cleanly serialize date/datetime/decimal objects
		payload_json = json.dumps(payload, default=str).replace("http://", "https://")

		resp = requests.post(
			endpoint,
			data=payload_json,
			headers=headers,
			timeout=45,
		)

		if resp.status_code == 200:
			try:
				resp_body = resp.json()
			except Exception:
				resp_body = {}

			msg = resp_body.get("message") or {}
			is_success = (
				(isinstance(msg, dict) and msg.get("status") == "success")
				or resp_body.get("status") == "success"
			)

			if is_success:
				_set_candidate_migrated(doc)
			else:
				frappe.log_error(
					title="JobPro Candidate Push Failed",
					message=f"JobPro sync for {candidate_name} returned non-success: {resp.text}",
				)
		else:
			frappe.log_error(
				title="JobPro Candidate Push Failed",
				message=f"JobPro sync for {candidate_name} failed HTTP {resp.status_code}: {resp.text[:500]}",
			)

	except Exception as e:
		frappe.log_error(
			title="JobPro Candidate Push Failed",
			message=f"Exception during candidate push to JobPro for {candidate_name}: {str(e)}\n{frappe.get_traceback()}",
		)


@frappe.whitelist()
def mark_candidate_as_migrated(candidate_name=None):
	"""
	Whitelisted callback endpoint for JobPro to confirm that a candidate has been successfully received.
	Can be called via authenticated RPC method or REST API.
	"""
	if not candidate_name:
		candidate_name = frappe.form_dict.get("candidate_name") or (
			frappe.local.form_dict.get("candidate_name") if hasattr(frappe.local, "form_dict") else None
		)

	if not candidate_name and hasattr(frappe, "request") and frappe.request and getattr(frappe.request, "data", None):
		try:
			import json
			data = json.loads(frappe.request.data.decode("utf-8"))
			candidate_name = data.get("candidate_name")
		except Exception:
			pass

	if not candidate_name:
		return {"status": "error", "message": "candidate_name is required"}

	if frappe.db.exists("Candidate", candidate_name):
		update_values = {}
		if frappe.db.has_column("Candidate", "migrated"):
			update_values["migrated"] = 1
		if frappe.db.has_column("Candidate", "is_migrate"):
			update_values["is_migrate"] = 1
		if not update_values:
			update_values = {"migrated": 1, "is_migrate": 1}

		frappe.db.set_value("Candidate", candidate_name, update_values, update_modified=False)
		frappe.db.commit()
		return {"status": "success", "candidate": candidate_name}

	return {"status": "not_found", "candidate": candidate_name}


def check_sync_health():
	print("\n" + "=" * 50)
	print("TEAMPRO ERP -> JOBPRO SYNC HEALTH CHECK")
	print("=" * 50)

	# 1. Check Candidate Schema Fields
	has_migrated = frappe.db.has_column("Candidate", "migrated")
	has_is_migrate = frappe.db.has_column("Candidate", "is_migrate")
	print(f"[1] Schema Check: 'migrated' column exists: {has_migrated}")
	print(f"    Schema Check: 'is_migrate' column exists: {has_is_migrate}")
	if not has_migrated and not has_is_migrate:
		print("    --> WARNING: Neither 'migrated' nor 'is_migrate' field was found in Candidate DocType!")

	# 2. Check hooks.py doc_events
	candidate_hooks = frappe.get_hooks("doc_events", {}).get("Candidate", {})
	after_insert_hook = candidate_hooks.get("after_insert")
	print(f"\n[2] Hook Check: Candidate after_insert hook: {after_insert_hook}")
	if not after_insert_hook or "teampro.custom_sync.push_candidate_to_jobpro" not in str(after_insert_hook):
		print("    --> ERROR: 'teampro.custom_sync.push_candidate_to_jobpro' is NOT active in after_insert!")

	# 3. Check Credentials Resolution
	try:
		from teampro.custom_sync import get_jobpro_credentials
		jobpro_url, api_key, api_secret = get_jobpro_credentials()
		print(f"\n[3] Credential Check:")
		print(f"    JobPro URL: {jobpro_url}")
		print(f"    API Key present: {bool(api_key)} ({api_key[:6]}... if present)")
		print(f"    API Secret present: {bool(api_secret)}")
		if not (jobpro_url and api_key and api_secret):
			print("    --> ERROR: Missing JobPro URL or API credentials!")
	except Exception as e:
		print(f"    --> ERROR loading get_jobpro_credentials: {str(e)}")
		return

	# 4. Probe JobPro Endpoint Connectivity
	print(f"\n[4] Network & Auth Check to JobPro:")
	endpoint = f"{jobpro_url.rstrip('/')}/api/method/jobpro.api.candidate_sync.receive_candidate_from_teampro"
	headers = {
		"Authorization": f"token {api_key}:{api_secret}",
		"Content-Type": "application/json",
		"Accept": "application/json",
	}

	try:
		# Probe with invalid empty payload to verify reachability and auth (should return HTTP 417 or error json, NOT 401/403/404)
		resp = requests.post(endpoint, json={"candidate_data": {}}, headers=headers, timeout=15)
		print(f"    Target Endpoint: {endpoint}")
		print(f"    HTTP Status Code: {resp.status_code}")
		if resp.status_code in (401, 403):
			print("    --> ERROR: Authentication failed with JobPro. Check jobpro_api_key and jobpro_api_secret.")
		elif resp.status_code == 404:
			print("    --> ERROR: Endpoint not found on JobPro. Verify JobPro URL.")
		elif resp.status_code in (200, 417, 500):
			print("    --> SUCCESS: JobPro endpoint reached and authentication confirmed!")
	except Exception as e:
		print(f"    --> ERROR connecting to JobPro: {str(e)}")

	# 5. Check Whitelisted Callback Endpoint
	print(f"\n[5] Local Callback Endpoint Check:")
	try:
		from teampro.custom_sync import mark_candidate_as_migrated
		print("    --> SUCCESS: 'mark_candidate_as_migrated' is imported and available.")
	except Exception as e:
		print(f"    --> ERROR importing 'mark_candidate_as_migrated': {str(e)}")

	print("\n" + "=" * 50)
	print("HEALTH CHECK COMPLETED")
	print("=" * 50 + "\n")

