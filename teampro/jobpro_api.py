import frappe
import json
from frappe.utils.file_manager import save_file

@frappe.whitelist(allow_guest=True)
def get_options(doctype, fields):
	"""
		JOBPRO: gets the options for the specified fields of a doctype and returns them as a dictionary.
		- doctype: the name of the doctype to fetch options for
		- fields: a list of field names (or a JSON string that can be parsed into a list) for which to fetch options
		Returns a dictionary where each key is a field name and the value is a list of options for that field. If a field does not exist or has no options, it will return an empty list for that field. 
	"""
	if isinstance(fields, str):
		fields = json.loads(fields)
		
	meta = frappe.get_meta(doctype)
	result = {}
	for fieldname in fields:
		field = meta.get_field(fieldname)
		result[fieldname] = (
			field.options.split("\n")
			if field and field.options
			else []
		)
	return result

@frappe.whitelist(allow_guest=True)
def get_candidate(email):
	"""
	Fetches the Candidate document associated with the given email address.
	- email: The email address to search for in the Candidate doctype.
	Returns the Candidate document as a dictionary if found, otherwise returns None.
	"""
	candidate_name = frappe.db.get_value(
		"Candidate",
		{"mail_id": email},
		"name"
	)

	if not candidate_name:
		return None

	candidate = frappe.get_doc("Candidate", candidate_name)

	return candidate.as_dict()

@frappe.whitelist(allow_guest=True)
def get_nationality():
	"""
	Fetches all Nationality documents and returns their names.
	Returns a list of nationality names.
	"""
	nationality = frappe.db.get_all("Nationality", pluck="name")
	return nationality

@frappe.whitelist(allow_guest=True)
def get_districts():
	"""
	Fetches all Districts documents and returns their names.
	Returns a list of districts names.
	"""
	districts = frappe.db.get_all("Districts", pluck="name")
	return districts

@frappe.whitelist(allow_guest=True)
def get_states():
	"""
	Fetch distinct states from Districts doctype.
	Returns a unique list of states.
	"""

	states = frappe.db.sql("""
		SELECT DISTINCT state
		FROM `tabDistricts`
		WHERE state IS NOT NULL
		AND state != ''
		ORDER BY state ASC
	""", pluck=True)

	return states

@frappe.whitelist(allow_guest=True)
def get_country():
	"""
	Fetches all Country documents and returns their names.
	Returns a list of country names.
	"""
	country = frappe.db.get_all("Country", pluck="name")
	return country

@frappe.whitelist(allow_guest=True)
def get_currency():
	"""
	Fetches all Currency documents and returns their names.
	Returns a list of currency names.
	"""
	currency = frappe.db.get_all("Currency", {"enabled": 1}, pluck="name")
	return currency

@frappe.whitelist(allow_guest=True)
def get_highest_degree():
	"""
	Fetches all Highest Degree documents and returns their names.
	Returns a list of Highest Degree names.
	"""
	degree = frappe.db.get_all("Qualification", pluck="name")
	return degree

@frappe.whitelist(allow_guest=True)
def get_specialization():
	"""
	Fetches all Specialization documents and returns their names.
	Returns a list of specialization names.
	"""
	specialization = frappe.db.get_all("Specialization", pluck="name")
	return specialization

@frappe.whitelist(allow_guest=True)
def update_candidate_details():
	data = frappe.request.get_json()
	frappe.db.set_value("Candidate", data.get("name"), data)
	return {"message": "Candidate details updated successfully."}

@frappe.whitelist(allow_guest=True)
def update_user_details():
	data = frappe.request.get_json()
	frappe.db.set_value("User", data.get("name"), data)
	return {"message": "User details updated successfully."}

@frappe.whitelist(allow_guest=True)
def upload_file():
	file = frappe.request.files.get("file")

	if not file:
		frappe.throw("No file uploaded")

	docname = frappe.form_dict.get("docname")
	doctype = frappe.form_dict.get("doctype")
	fieldname = frappe.form_dict.get("fieldname")

	saved_file = save_file(
		fname=file.filename,
		content=file.stream.read(),
		dt=doctype,
		dn=docname,
		df=fieldname,
		is_private=0
	)

	frappe.db.set_value(
		doctype,
		docname,
		fieldname,
		saved_file.file_url
	)

	return {
		"status": "success",
		"file_url": saved_file.file_url
	}
 
@frappe.whitelist(allow_guest=True)
def delete_file():
	docname = frappe.form_dict.get("docname")
	doctype = frappe.form_dict.get("doctype")
	fieldname = frappe.form_dict.get("fieldname")

	frappe.db.set_value(
		doctype,
		docname,
		fieldname,
		""
	)

	return {
		"status": "success"
	}
	
@frappe.whitelist(allow_guest=1)
def get_applied_jobs(candidate=None):
	if not candidate:
		return []
	
	tasks = frappe.db.sql("""
		SELECT 
			c.applied_on, c.status, 
			p.name, p.subject, p.territory, p.created_on, p.currency,
			p.amount, p.custom_country_flag, p.customer, p.custom_free_recruitment,
			p.food, p.accommodation, p.joining_ticket, p.transportation,
			p.custom_customer_location_image, p.qualification_type, 
			p.specialization, p.minimum_experience,
			p.maximum_experience, p.gulf_experience, p.description, 
			p.custom_about_customer,
			p.custom_customer_website, p.custom_major_key_skills, 
			p.vac, p.total_experience
		FROM 
			`tabTask` p
		INNER JOIN 
			`tabJOBPRO Candidate` c
		ON 
			p.name = c.parent
		WHERE 
			p.service IN ('REC-I', 'REC-D')
			AND p.status IN ('Overdue', 'Working', 'Open', 'Pending Review')
			AND c.candidate = %s
	""", (candidate), as_dict=1)
	
	return tasks

@frappe.whitelist()
def get_candidate_status(candidate, task):

	if not candidate or not task:
		return []

	workflow = [
		"Sourced",
		"Pending QC",
		"Submit(SPOC)",
		"Submitted(Client)",
		"Shortlisted",
		"Linedup",
		"Linedup Confirmed",
		"Reported",
		"Interviewed",
		"Proposed PSL",
		"Result Pending"
	]
 
	status_mapping = {
		"Sourced": "Received CV",
		"Pending QC": "Under Review",
		"Submit(SPOC)": "Shared with Recruiter",
		"Submitted(Client)": "Sent to Employer",
		"Shortlisted": "Shortlisted",
		"Linedup": "Interview Scheduled",
		"Linedup Confirmed": "Interview Confirmed",
		"Reported": "Joined Interview",
		"Interviewed": "Interview Completed",
		"Proposed PSL": "Offer in Progress",
		"Result Pending": "Awaiting Feedback"
	}

	candidate_statuses = frappe.db.get_all(
		"Candidate status",
		{
			"parent": candidate,
			"task": task
		},
		["status", "sourced_date", "remarks"],
		order_by="sourced_date asc"
	)

	# Default tracker
	tracker = {
		status: {
			"label": status_mapping.get(status, status),
			"state": "pending",
			"datetime": None,
			"remarks": None
		}
		for status in workflow
	}

	# Sourced always completed
	tracker["Sourced"]["state"] = "completed"

	last_completed_index = 0

	for row in candidate_statuses:

		status = row.status

		# Ignore unknown statuses
		if status not in workflow and status != "IDB":
			continue

		# Handle rejection
		if status == "IDB":

			failed_index = last_completed_index

			if failed_index < len(workflow):

				failed_status = workflow[failed_index]

				tracker[failed_status]["state"] = "failed"

				tracker[failed_status]["datetime"] = row.sourced_date

				tracker[failed_status]["remarks"] = row.remarks

			continue

		# Normal progression
		current_index = workflow.index(status)

		# Reset everything after current status
		for future_status in workflow[current_index + 1:]:

			tracker[future_status]["state"] = "pending"

			tracker[future_status]["datetime"] = None

			tracker[future_status]["remarks"] = None

		# Complete current status
		tracker[status]["state"] = "completed"

		tracker[status]["datetime"] = row.sourced_date

		tracker[status]["remarks"] = row.remarks

		last_completed_index = current_index

		# Clear failure if restarted
		next_index = current_index + 1

		if next_index < len(workflow):

			next_status = workflow[next_index]

			if tracker[next_status]["state"] == "failed":

				tracker[next_status]["state"] = "pending"

				tracker[next_status]["datetime"] = None

				tracker[next_status]["remarks"] = None

	# Get latest transition
	latest_transition = candidate_statuses[-1] if candidate_statuses else None

	if latest_transition:

		# Latest transition is rejection
		if latest_transition.status == "IDB":

			# Find previous workflow status
			previous_workflow_status = None

			for row in reversed(candidate_statuses[:-1]):

				if row.status in workflow:

					previous_workflow_status = row
					break

			if previous_workflow_status:

				failed_status = previous_workflow_status.status

				tracker[failed_status]["state"] = "failed"

				tracker[failed_status]["datetime"] = latest_transition.sourced_date

				tracker[failed_status]["remarks"] = "Better luck next time"

				failed_index = workflow.index(failed_status)

				# Previous statuses completed
				for previous_status in workflow[:failed_index]:

					tracker[previous_status]["state"] = "completed"

		# Normal active workflow
		else:

			current_status = latest_transition.status

			if current_status in workflow:

				tracker[current_status]["state"] = "current"

				current_index = workflow.index(current_status)

				# Previous statuses completed
				for previous_status in workflow[:current_index]:

					tracker[previous_status]["state"] = "completed"
	return list(tracker.values())

@frappe.whitelist()
def apply_job(candidate, task):
	if not frappe.db.exists("JOBPRO Candidate", {"parent": task, "candidate": candidate}):
		applied_count = frappe.db.count(
			"JOBPRO Candidate",
			{"parent": task}
		)

		doc = frappe.get_doc({
			"doctype": "JOBPRO Candidate",
			"parent": task,
			"parenttype": "Task",
			"parentfield": "custom_jobpro_candidates",
			"idx": applied_count + 1,
			"candidate": candidate,
			"status": "Sourced"
		})

		doc.insert(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def get_tasks(additional_filters=None, candidate=None):
	conditions = [
		"t.status IN ('Open', 'Overdue', 'Pending Review', 'Working')",
		"t.service IN ('REC-I', 'REC-D')"
	]

	values = {}

	if additional_filters:
		if isinstance(additional_filters, str):
			additional_filters = json.loads(additional_filters)

		for idx, f in enumerate(additional_filters):
			field, operator, value = f

			key = f"value_{idx}"

			if operator.lower() == "in":

				placeholders = []

				for i, v in enumerate(value):
					sub_key = f"{key}_{i}"
					values[sub_key] = v
					placeholders.append(f"%({sub_key})s")

				conditions.append(
					f"t.{field} IN ({', '.join(placeholders)})"
				)

			else:
				conditions.append(f"t.{field} {operator} %({key})s")
				values[key] = value

	where_clause = " AND ".join(conditions)

	values["candidate"] = candidate

	query = f"""
		SELECT
			t.name,
			t.subject,
			t.territory,
			t.created_on,
			t.currency,
			t.amount,
			t.custom_country_flag,
			t.customer,
			t.custom_free_recruitment,
			t.food,
			t.accommodation,
			t.joining_ticket,
			t.transportation,
			t.custom_customer_location_image,
			t.qualification_type,
			t.specialization,
			t.minimum_experience,
			t.maximum_experience,
			t.gulf_experience,
			t.description,
			t.custom_about_customer,
			t.custom_customer_website,
			t.custom_major_key_skills,
			t.vac,
			t.total_experience,

			CASE
				WHEN jc.candidate IS NOT NULL THEN 1
				ELSE 0
			END AS already_applied

		FROM `tabTask` t

		LEFT JOIN `tabJOBPRO Candidate` jc
			ON jc.parent = t.name
			AND jc.candidate = %(candidate)s

		WHERE {where_clause}

		ORDER BY t.created_on DESC
		LIMIT 1000
	"""
	return frappe.db.sql(query, values, as_dict=True)

@frappe.whitelist()
def create_candidate(
	given_name=None,
	mail_id=None,
	mobile_number=None,
	source=None,
	gender=None,
	date_of_birth=None,
	custom_sourced_by=None,
	position=None,
	candidate_image=None
):

	try:

		candidate_name = frappe.db.get_value(
			"Candidate",
			{"mail_id": mail_id}
		)
		
		frappe.log_error("Candidate Name", [candidate_name, "feknkefn", candidate_image])

		if candidate_name:
			doc = frappe.get_doc("Candidate", candidate_name)
		else:
			doc = frappe.new_doc("Candidate")

		doc.given_name = given_name
		doc.mail_id = mail_id
		doc.mobile_number = mobile_number
		doc.source = source
		doc.gender = gender
		doc.date_of_birth = date_of_birth
		doc.custom_sourced_by = custom_sourced_by
		doc.position = position
		doc.candidate_image = candidate_image
		doc.flags.ignore_mandatory = True

		if doc.is_new():
			doc.insert(ignore_permissions=True)
		else:
			doc.save(ignore_permissions=True)

		frappe.db.commit()

		return {
			"status": "success",
			"name": doc.name
		}

	except Exception:

		frappe.log_error(
			title="Create Candidate API Error",
			message=frappe.get_traceback()
		)

		return {
			"status": "error",
			"message": str(frappe.get_traceback())
		}
  
def test_check():
    tasks = frappe.get_all("Task", {"service": "REC-I", "custom_country_flag": ["is", "not set"]}, ["name", "territory"])
    for task in tasks:
        flag = frappe.db.get_value("Territory", task.territory, "custom_country_flag")
        frappe.db.set_value("Task", task.name, "custom_country_flag", flag)
        print([task.territory, flag])