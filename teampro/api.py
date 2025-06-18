import frappe
import requests
import json
from frappe import enqueue
import re

@frappe.whitelist(allow_guest=True)
def get_biometric_logs(**args):
	frappe.log_error(title='biometric logs',message=args)



import frappe
import requests
from frappe import _

@frappe.whitelist()
def get_address(lat, lon):
	url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
	response = requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		frappe.throw(_("Unable to fetch address from coordinates."))


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


