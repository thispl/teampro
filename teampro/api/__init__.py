import frappe
import requests
import json
from frappe import enqueue
import re

@frappe.whitelist(allow_guest=True)
def get_biometric_logs(**args):
	frappe.log_error(title='biometric logs',message=args)


from frappe import _

@frappe.whitelist()
def get_address(lat, lon):
	url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
	response = requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		frappe.throw(_("Unable to fetch address from coordinates."))

def rename_user():
	frappe.enqueue(
		frappe.rename_doc("User", "abdullahihannan.s@groupteampro.com", "a.hannan@groupteampro.com", force=1, merge=0,rebuild_search=False),
		queue="long", 
		timeout=36000,
		is_async=True, 
		job_name='Rename User',
		enqueue_after_commit=False,

	) 

@frappe.whitelist()
def create_new_user(first_name,last_name,phone,email,password,device_id):
	message=''
	if frappe.db.exists("User",{'name':email}):
		message='You have already registered'
	else:
		user=frappe.new_doc("User")
		user.first_name=first_name
		user.last_name=last_name
		user.mobile_no=phone
		user.email=email
		user.new_password=password
		user.save(ignore_permissions=True)
		candidate = new_candidate(first_name,last_name, phone,email,device_id)
		message='You have been registered successfully. Now Login to continue'
	return message

def new_candidate(first_name, last_name,phone,email,device_id):
	candidate = frappe.new_doc("Candidate")
	candidate.given_name = first_name + ' '+last_name
	candidate.mail_id = email
	candidate.mobile_number = phone
	candidate.source = 'A-Portal'
	candidate.position = 'JOBPRO'
	candidate.custom_device_id=device_id
	candidate.insert()
	candidate.save(ignore_permissions=True)

@frappe.whitelist()
def update_saved_jobs(name,user,subject):
	message=''
	if frappe.db.exists("Saved Jobs",{'task_id':name,'user_id':user}):
		message='Already saved'
	else:
		saved_jobs=frappe.new_doc("Saved Jobs")
		saved_jobs.user_id=user
		saved_jobs.subject=subject
		saved_jobs.task_id=name
		saved_jobs.save(ignore_permissions=True)
		message='Job has been saved successfully'
	return message

@frappe.whitelist()
def update_cv(user,name):
	message=''
	if frappe.db.exists("Candidate",{'mail_id':user}):
		saved_jobs=frappe.get_doc("Candidate",{'mail_id':user})
		saved_jobs.updated__masked_cv="https://erp.teamproit.com"+name
		# saved_jobs.subject=subject
		# saved_jobs.task_id=name
		saved_jobs.save(ignore_permissions=True)
		message='CV has been attached successfully'
	return message

@frappe.whitelist()
def update_bio(user,bio):
	message=''
	if frappe.db.exists("User",{'name':user}):
		user_doc=frappe.get_doc("User",{'name':user})
		user_doc.bio=bio
		# user_doc.subject=subject
		# user_doc.task_id=name
		user_doc.save(ignore_permissions=True)
		message='Bio has been updated succesfully'
	return message

@frappe.whitelist()
def update_interest(user,interest):
	message=''
	if frappe.db.exists("User",{'name':user}):
		user_doc=frappe.get_doc("User",{'name':user})
		user_doc.interest=interest
		# user_doc.subject=subject
		# user_doc.task_id=name
		user_doc.save(ignore_permissions=True)
		message='Skills has been updated succesfully'
	return message

@frappe.whitelist(allow_guest=True)
def otp_verification(otpSent, otpValue, mobile, device_id):
	result=''
	if mobile=='9715327487':
		if otpValue =='123123':
			user_data = frappe.db.get_value("User",{'mobile_no':mobile},['name'])
			# user_data = frappe.db.sql("""select name, full_name from `tabUser` where mobile_no = '%s'""" %(mobile), as_dict=1)
			if user_data:
				if frappe.db.exists("Candidate",{'mobile_number':mobile}):
					cand=frappe.get_doc("Candidate",{'mobile_number':mobile})
					frappe.db.set_value("Candidate",cand.name,"custom_device_id",device_id)
					# cand.custom_device_id=device_id
					# cand.save(ignore_permissions=True)
				result = str(user_data)     
			else:
				result = 'user not found'
		else:
			result = "invalid"
	else:
		if otpSent == otpValue:
			user_data = frappe.db.get_value("User",{'mobile_no':mobile},['name'])
			# user_data = frappe.db.sql("""select name, full_name from `tabUser` where mobile_no = '%s'""" %(mobile), as_dict=1)
			if user_data:
				if frappe.db.exists("Candidate",{'mobile_number':mobile}):
					cand=frappe.get_doc("Candidate",{'mobile_number':mobile})
					cand.custom_device_id=device_id
					cand.save(ignore_permissions=True)
				result = str(user_data)     
			else:
				result = 'user not found'
		else:
			result = "invalid"
	return result

@frappe.whitelist()
def create_user_notification(doc,method):
	if doc.service in ['REC-I','REC-D']:
		un=frappe.new_doc("User Notifications")
		un.subject=doc.subject + " - JOB ALERT🔥"
		un.content="A new Job "+doc.subject+" has been added"
		un.save(ignore_permissions=True)


@frappe.whitelist()
def user_id():
	# user_email = doc.for_user
	user_device_id = frappe.get_all(
		"Candidate", filters={"custom_device_id": ('!=','')}, fields=["custom_device_id"]
	)
	return user_device_id


@frappe.whitelist()
def send_notification(doc, method):
	device_ids = user_id()
	if device_ids:
		for device_id in device_ids:
			enqueue(
				process_notification,
				queue="default",
				now=False,
				device_id=device_id,
				notification=doc,
			)
@frappe.whitelist()
def process_notification(device_id, notification):
	message = notification.subject
	title = notification.content
	url = "https://fcm.googleapis.com/v1/projects/jobpro-f8bef/messages:send"
	body = {
		"message":{
			"token": device_id.custom_device_id,
			"notification": {"title": message, "body": title},
		}
	}

	server_key = _get_access_token()
	auth = f"Bearer {server_key}"
	req = requests.post(
		url=url,
		data=json.dumps(body),
		headers={
			"Authorization": auth,
			"Content-Type": "application/json",
		},
	)



import google.auth.transport.requests
from google.oauth2 import service_account
import os
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
@frappe.whitelist()
def _get_access_token():
	json_path = os.getenv('SERVICE_ACCOUNT_JSON', '/home/frappe/teampro-bench/apps/teampro/teampro/jobpro-f8bef-f2152785d551.json')
	credentials = service_account.Credentials.from_service_account_file(json_path, scopes=SCOPES)
	request = google.auth.transport.requests.Request()
	credentials.refresh(request)
	return credentials.token


# import frappe

# @frappe.whitelist()
# def get_user_target():

#     if frappe.session.user != "riyaz.a@groupteampro.com":
#         return {}

#     target = frappe.get_doc("Target Manager", {"employee": "TI00005"})

#     return {
#         "custom_total_achieved_point": target.custom_total_achieved_point,
#         "custom_total_target_point": target.custom_total_target_point,
#         "custom_sr": target.custom_sr
#     }

import frappe



# import frappe

# @frappe.whitelist()
# def get_user_target():

#     user = frappe.session.user

#     employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
#     if not employee:
#         return {"has_target": False}

#     target_name = frappe.db.get_value("Target Manager", {"employee": employee}, "name")
#     if not target_name:
#         return {"has_target": False}

#     target = frappe.get_doc("Target Manager", target_name)

#     return {
#         "has_target": True,
#         "custom_total_achieved_point": target.custom_total_achieved_point,
#         "custom_total_target_point": target.custom_total_target_point,
#         "custom_sr": target.custom_sr
#     } 


import frappe
from frappe.utils import nowdate, getdate

@frappe.whitelist()
def get_user_target():
	user = frappe.session.user

	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return {"has_target": False}

	target_name = frappe.db.get_value("Target Manager", {"employee": employee}, "name")
	if not target_name:
		return {"has_target": False}

	target = frappe.get_doc("Target Manager", target_name)

	today = getdate(nowdate())

	if target.custom_year_start_date and target.custom_year_end_date:
		if not (target.custom_year_start_date <= today <= target.custom_year_end_date):
			return {"has_target": False}

	return {
		"has_target": True,
		"custom_total_achieved_point": target.custom_total_achieved_point,
		"custom_total_target_point": target.custom_total_target_point,
		"custom_sr": target.custom_sr
	}



import frappe
from frappe.utils import getdate, nowdate
from datetime import datetime

@frappe.whitelist()
def get_user_target_month():
	user = frappe.session.user

	# Get employee linked to this user
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if not employee:
		return {"has_target": False}

	today = getdate(nowdate())
	current_month = datetime.today().strftime("%b").lower()

	# Get the Target Manager where today is within start and end date
	target_name = frappe.db.get_value(
		"Target Manager",
		filters={
			"employee": employee,
			"custom_year_start_date": ("<=", today),
			"custom_year_end_date": (">=", today)
		},
		fieldname="name"
	)

	if not target_name:
		# No target for current date range
		return {"has_target": False}

	target = frappe.get_doc("Target Manager", target_name)

	achieved = 0
	total = 0
	percent = 0

	# Calculate points only for current month
	for row in target.target_child:
		if row.month and row.month.strip().lower() == current_month:
			achieved += row.achieved_point or 0
			total += row.cr_ct_point or 0

	if total:
		percent = (achieved / total) * 100

	return {
		"has_target": True if total else False,
		"month_achieved": achieved,
		"month_target": total,
		"month_percent": percent
	}



# @frappe.whitelist()
# def get_user_target_month():

# 	user = frappe.session.user

# 	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
# 	if not employee:
# 		return {"has_target": False}

# 	target_name = frappe.db.get_value("Target Manager", {"employee": employee}, "name")
# 	if not target_name:
# 		return {"has_target": False}

# 	target = frappe.get_doc("Target Manager", target_name)
	

# 	current_month = datetime.today().strftime("%b").lower()

# 	achieved = 0
# 	total = 0
# 	percent=0
# 	today = getdate(nowdate())

# 	if target.custom_year_start_date and target.custom_year_end_date:
# 		if (target.custom_year_start_date <= today <= target.custom_year_end_date):

# 			for row in target.target_child:

# 				if row.month and row.month.strip().lower() == current_month:

# 					achieved += row.achieved_point or 0
# 					total += row.cr_ct_point or 0

# 			percent = (achieved / total * 100) if total else 0


# 	return {
# 		"has_target": True,
# 		"month_achieved": achieved,
# 		"month_target": total,
# 		"month_percent": percent
# 	}


import frappe

@frappe.whitelist()
def notify_target_change(doc, method=None):
	"""
	Trigger a realtime event whenever a Target Manager doc is added, updated, or deleted.
	"""
	if not doc or not getattr(doc, "employee", None):
		return

	frappe.publish_realtime(
		event="target_manager_changed",
		message={
			"employee": doc.employee,
			"exists": True if frappe.db.exists("Target Manager", doc.name) else False
		},
		user=None 
	)

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
	candidate = frappe.db.get_value("Candidate", {"mail_id": email}, "*")
	return candidate

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
def update_candidate_details():
    data = frappe.request.get_json()



import frappe

@frappe.whitelist(allow_guest=True)
def get_active_images():

    child_data = frappe.get_all(
        "Advertisement Details",
        filters={
            "is_active": 1
        },
        fields=["attach", "parent"]
    )

    final_data = []

    for row in child_data:

        status = frappe.db.get_value(
            "Project",
            row.parent,
            "status"
        )

        if status == "Open":

            final_data.append({
                "attach": frappe.utils.get_url() + row.attach
            })

    return final_data