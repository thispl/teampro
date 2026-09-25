import frappe
from frappe import _
from frappe.utils import cint, get_url


def _get_file_attachments(doctype: str, docname: str) -> list:
	"""
	Collects all files attached to a given document.
	Generates absolute URLs so external sites like JobPro can easily download them.
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


def _get_customer_payload(customer_name: str) -> dict:
	"""
	Fetches the Customer document, its child tables, and resolves
	associated Address and Contact documents linked via Dynamic Link.
	"""
	if not customer_name or not frappe.db.exists("Customer", customer_name):
		return {}

	cust_doc = frappe.get_doc("Customer", customer_name)
	cust_dict = cust_doc.as_dict()

	# 1. Fetch Addresses linked to this Customer
	address_names = frappe.db.sql_list("""
		SELECT dl.parent
		FROM `tabDynamic Link` dl
		WHERE dl.parenttype = 'Address'
		  AND dl.link_doctype = 'Customer'
		  AND dl.link_name = %s
	""", (customer_name,))

	addresses = []
	for addr_name in address_names:
		try:
			addr_doc = frappe.get_doc("Address", addr_name)
			addresses.append(addr_doc.as_dict())
		except Exception:
			continue
	cust_dict["addresses"] = addresses

	# 2. Fetch Contacts linked to this Customer (SPOCs)
	contact_names = frappe.db.sql_list("""
		SELECT dl.parent
		FROM `tabDynamic Link` dl
		WHERE dl.parenttype = 'Contact'
		  AND dl.link_doctype = 'Customer'
		  AND dl.link_name = %s
	""", (customer_name,))

	contacts = []
	for contact_name in contact_names:
		try:
			contact_doc = frappe.get_doc("Contact", contact_name)
			contacts.append(contact_doc.as_dict())
		except Exception:
			continue
	cust_dict["contacts"] = contacts

	return cust_dict


def _get_project_payload(project_id: str) -> dict:
	"""
	Fetches the Project document and its child tables.
	Also fetches any Criteria rows associated with the project.
	"""
	if not project_id or not frappe.db.exists("Project", project_id):
		return {}

	proj_doc = frappe.get_doc("Project", project_id)
	proj_dict = proj_doc.as_dict()

	# If Criteria rows are attached directly to Project
	if not proj_dict.get("custom_criteria_table"):
		criteria_rows = frappe.db.get_all(
			"Criteria",
			filters={"parent": project_id, "parenttype": "Project"},
			fields=["name", "scheduling_criteria", "scheduling_parameter", "criteria_data", "criteria_float", "criteria_select"],
			order_by="idx asc",
		)
		if criteria_rows:
			proj_dict["custom_criteria_table"] = criteria_rows

	return proj_dict


@frappe.whitelist()
def get_project_for_jobpro(project_id: str):
	"""
	Whitelisted API method for JobPro to import a Project.
	Fetches Project, resolves its linked Customer with Addresses/Contacts,
	and collects all file attachments (contracts, SLAs, rate cards, etc.).

	Endpoint:
	/api/method/teampro.jobpro_export.get_project_for_jobpro
	"""
	if not project_id:
		frappe.throw(_("Parameter 'project_id' is required."), frappe.MandatoryError)

	if not frappe.db.exists("Project", project_id):
		frappe.throw(_("Project '{0}' not found on TEAMPRO ERP.").format(project_id), frappe.DoesNotExistError)

	# 1. Fetch Project
	project_data = _get_project_payload(project_id)

	# 2. Fetch linked Customer
	customer_id = project_data.get("customer")
	customer_data = _get_customer_payload(customer_id) if customer_id else {}

	# 3. Collect Attachments from Project and Customer
	attachments = []
	attachments.extend(_get_file_attachments("Project", project_id))
	if customer_id:
		attachments.extend(_get_file_attachments("Customer", customer_id))

	return {
		"status": "success",
		"project": project_data,
		"customer": customer_data,
		"attachments": attachments,
	}


@frappe.whitelist()
def get_task_opening_for_jobpro(task_id: str):
	"""
	Whitelisted API method for JobPro to import a Job Opening (Task).
	Validates that task.service is 'REC-I' or 'REC-D'.
	Fetches Task, its parent Project, its grandparent Customer,
	and collects all file attachments (JD PDF, requirements specs).

	Endpoint:
	/api/method/teampro.jobpro_export.get_task_opening_for_jobpro
	"""
	if not task_id:
		frappe.throw(_("Parameter 'task_id' is required."), frappe.MandatoryError)

	if not frappe.db.exists("Task", task_id):
		frappe.throw(_("Task '{0}' not found on TEAMPRO ERP.").format(task_id), frappe.DoesNotExistError)

	task_doc = frappe.get_doc("Task", task_id)

	# 1. Validate service
	service = task_doc.get("service") or ""
	if service not in ("REC-I", "REC-D"):
		frappe.throw(
			_("Task '{0}' is not a Recruitment Opening. Its service is '{1}', but must be 'REC-I' or 'REC-D'.").format(
				task_id, service
			),
			frappe.ValidationError,
		)

	task_dict = task_doc.as_dict()

	# Ensure Criteria table is attached
	if not task_dict.get("custom_criteria_table"):
		criteria_rows = frappe.db.get_all(
			"Criteria",
			filters={"parent": task_id, "parenttype": "Task"},
			fields=["name", "scheduling_criteria", "scheduling_parameter", "criteria_data", "criteria_float", "criteria_select"],
			order_by="idx asc",
		)
		if criteria_rows:
			task_dict["custom_criteria_table"] = criteria_rows

	# 2. Fetch parent Project
	project_id = task_dict.get("project")
	project_data = _get_project_payload(project_id) if project_id else {}

	# 3. Fetch grandparent Customer (from Task or parent Project)
	customer_id = task_dict.get("customer") or project_data.get("customer")
	customer_data = _get_customer_payload(customer_id) if customer_id else {}

	# 4. Collect Attachments
	attachments = []
	# Task attachments (JD, specs, salary annexures)
	attachments.extend(_get_file_attachments("Task", task_id))
	# Parent Project attachments (contracts, SLAs, rate cards)
	if project_id:
		attachments.extend(_get_file_attachments("Project", project_id))
	# Customer attachments
	if customer_id:
		attachments.extend(_get_file_attachments("Customer", customer_id))

	return {
		"status": "success",
		"task": task_dict,
		"project": project_data,
		"customer": customer_data,
		"attachments": attachments,
	}


@frappe.whitelist()
def get_customer_for_jobpro(customer_name: str):
	"""
	Whitelisted API method for JobPro to import a single Customer directly.
	Fetches Customer document along with linked Addresses and Contacts/SPOCs.

	Endpoint:
	/api/method/teampro.jobpro_export.get_customer_for_jobpro
	"""
	if not customer_name:
		frappe.throw(_("Parameter 'customer_name' is required."), frappe.MandatoryError)

	if not frappe.db.exists("Customer", customer_name):
		# Fallback check by short_code or customer_name
		matched = frappe.db.get_value("Customer", {"customer_name": customer_name}, "name")
		if not matched and frappe.db.has_column("Customer", "short_code"):
			matched = frappe.db.get_value("Customer", {"short_code": customer_name}, "name")
		if matched:
			customer_name = matched
		else:
			frappe.throw(_("Customer '{0}' not found on TEAMPRO ERP.").format(customer_name), frappe.DoesNotExistError)

	customer_data = _get_customer_payload(customer_name)
	attachments = _get_file_attachments("Customer", customer_name)

	return {
		"status": "success",
		"customer": customer_data,
		"attachments": attachments,
	}


@frappe.whitelist()
def get_candidates_for_jobpro(limit_start=0, limit_page_length=50, last_sync_date=None):
	"""
	Export unmigrated or recently modified Candidate records to JobPro.
	"""
	limit_start = cint(limit_start)
	limit_page_length = cint(limit_page_length) or 50

	filters = [
		["Candidate", "is_migrate", "!=", 1],
		["Candidate", "migrated", "!=", 1]
	]

	if last_sync_date and str(last_sync_date).strip() and not str(last_sync_date).startswith("0001"):
		filters.append(["Candidate", "modified", ">", str(last_sync_date).strip()])

	total_count = frappe.db.count("Candidate", filters=filters)

	candidate_names = frappe.get_all(
		"Candidate",
		filters=filters,
		pluck="name",
		start=limit_start,
		page_length=limit_page_length,
		order_by="creation desc"
	)

	candidates = []
	for c_name in candidate_names:
		try:
			doc = frappe.get_doc("Candidate", c_name)
			doc_dict = doc.as_dict()
			doc_dict["site_url"] = "https://erp.teamproit.com"
			candidates.append(doc_dict)
		except Exception:
			continue

	return {
		"total_count": total_count,
		"candidates": candidates
	}

