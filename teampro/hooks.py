# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "teampro"
app_title = "Teampro"
app_publisher = "TeamPRO"
app_description = "TeamPRO Custom App"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hr@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/teampro/css/teampro.css"
# app_include_js = "/assets/teampro/js/teampro.js"

# include js, css files in header of web template
# web_include_css = "/assets/teampro/css/teampro.css"
# web_include_js = "/assets/teampro/js/teampro.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "teampro.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "teampro.install.before_install"
# after_install = "teampro.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "teampro.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "File":{
		"before_save": "teampro.utility.rename_file"
	},
	"Quotation":{
		"validate": "teampro.custom.calc_cut_off_prize"
	},
	"Employee":{
		"validate": ["teampro.custom.update_custodian","teampro.custom.inactive_employee"]
	},
	"Task":{
		"on_update": ["teampro.custom.issue_status","jobpro.custom.update_project_count"],
		"validate": ["teampro.custom.update_issue_type","teampro.custom.update_issue_typein_issue"]

	},

	"Project":{
		"after_insert": "teampro.custom.create_project_completion_task",
	},
	"Timesheet":{
		"on_update": "teampro.custom.fetch_start_time",
		# "before_submit":"teampro.custom.return_detailed_ts"
	},
	"Sales Order":{
		"on_submit":["teampro.custom.update_batch_status","teampro.teampro.doctype.target_manager.target_manager.calculate_target_on_update_manager"],
        "on_cancel": "teampro.custom.update_pi_workflow",
		# "after_submit": "teampro.teampro.doctype.target_manager.target_manager.calculate_target_on_update_manager",
		# "on_update":"teampro.custom.skip_dn_so",
        # "validate":"teampro.custom.child_table_calc"
	},
	"Opportunity": {
		"after_insert": "teampro.custom.opportunity_send_mail",
        "on_update":"teampro.custom.update_lead_status",
		# "on_cancel": "method",
		# "on_trash": "method"
	},
	"Candidate": {
		"on_update": ["teampro.custom.update_task_count"]
	},
	# "Payment Entry":{
	# 	"on_submit":"jobpro.jobpro.doctype.closure.closure.closure_payment_entry"
	# },
	"Sales Invoice":{
        # "validate":["teampro.custom.get_all_quot"],
		# "validate": "teampro.custom.sales_order_batch",
		# "after_submit": "teampro.teampro.doctype.target_manager.target_manager.calculate_target_on_update",
		"on_submit": "teampro.teampro.doctype.target_manager.target_manager.calculate_target_on_update_manager",
		# "on_submit": "teampro.custom.get_against_so"
	},
	# "Attendance Request":{
	# 	"before_submit": "teampro.custom.update_attendance"
	# },
	"Purchase Invoice": {
        "before_submit": "teampro.custom.validate_date",
        "on_update":"teampro.custom.update_workflow_state"
    },
    # "Task":{
    #     "validate": ["teampro.custom.update_issue_type","teampro.custom.update_issue_typein_issue"]
	# },
	# "Sales Invoice": {
    #     "on_submit": "teampro.custom.validate_date_salesinvoice"
    # },

	# "Payroll Entry":{
	# 	"before_save": ["teampro.utility.attendance_calc","teampro.utility.additional_salary"]
	# },

	# "Delivery Note":{
	# "after_insert": "teampro.custom.get_delivery_note"
	# },
    
	"BG Entry Form": {
        "after_insert": "teampro.teampro.doctype.bg_entry_form.bg_entry_form.mark_files_public"
	},
    
	# "Job Applicant": {
    #     "after_insert": "teampro.utility.mark_files_public"
	# },
    
	"Attendance":{
        "on_cancel":"teampro.mark_attendance.cancel_comp_off"
	},
	
}

# Scheduled Tasks
# ---------------
scheduler_events = {
	"daily": [
		"teampro.email_alerts.next_contact_alert",
		# "teampro.custom.create_food_count",
		"teampro.mark_attendance.mark_att",
		"teampro.email_alerts.checkin_alert",
        # "checkpro.checkpro.doctype.case.case.tat_monitor",
        "teampro.custom.update_case_age",
		"teampro.custom.update_batch_age",
        "teampro.custom.update_check_age",
        "teampro.custom.update_cv_age",
	],
	"monthly": [
		"teampro.utility.create_update_leave_allocation",
        "teampro.custom.epnc_send_mail",
        "teampro.custom.ep_mail",
	],
	"cron": {
		"00 9 * * *" : [
			"teampro.teampro.doctype.food_count.food_count.create_food_count"
		],
		"*/10 * * * *" : [
			"teampro.mark_attendance.mark_att"
		],
		"00 18 * * *" : [
			"checkpro.custom.cases_with_to_be_billed_status"
		],
		"00 18 * * *" : [
			"checkpro.custom.cases_with_generate_report_status"
		],
		"00 18 * * *" : [
			"checkpro.custom.insuff_consolidated_mail"
		],
		"00 09 * * *" : [
			"checkpro.custom.dpr_excel_format"
		],
		"00 18 * * *" : [
			"checkpro.custom.cases_with_gr_daily_report"
		],
		"00 18 * * *" : [
			"checkpro.custom.submitted_bg_entry"
		],
		"00 09 * * *" : [
			"jobpro.jobpro.doctype.closure.closure.visa_expiry_alert"
		],
		"00 09 * * *" : [
			"jobpro.jobpro.doctype.closure.closure.fm_expiry_alert"
		],
		"30 18 * * *" : [
			"checkpro.custom.dsr_mail"
		],
		"00 18 * * *" : [
			"checkpro.custom.cases_with_insuff_daily_report"
		],
		"00 09 * * *" : [
			"checkpro.custom.cases_with_insuff"
		],
		"00 09 * * *" : [
			"checkpro.custom.cases_beyond_tat_age_10"
		],
		"00 1 1 * *" : [
			"teampro.utility.update_leave_ledger_entry"
		],
        "30 18 * * *" : [
			"checkpro.custom.statement_of_account"
		],'00 10 * * 1,4':[
            'teampro.email_alerts.sales_invoice_overdue_docs'
		],'00 10 * * 1':[
            'checkpro.custom.task_mail_notification'
		],'00 10 * * 2,5':[
            'checkpro.custom.sales_order_follow_up'
		],'00 10 * * 1':[
            'checkpro.custom.task_mail_notification_status'
		],
        "00 23 * * *" : [
			"checkpro.custom.statement_of_account_test_1"
		],"00 10 * * 1":[
            'checkpro.custom.sales_order_follow_up_test'
		],"00 10 * * 1":[
            'checkpro.custom.sales_invoice_follow_up_test'
		],"59 23 * * *":[
            'checkpro.custom.statement_of_account_test'
		],
        # "0 1 * * * ":[
        #     'checkpro.custom.dpr_mail'
		# ],
        "0 1 * * * ":[
            'checkpro.custom.dpr_over_all_task'
		],"0 1 * * * ":[
            'checkpro.custom.dpr_over_all_meeting'
		],"0 1 * * * ":[
            'checkpro.custom.dpr_over_all'
		]
	}
}
jinja = {
	"methods": [
        "teampro.custom.get_task_details"
	]
}
# scheduler_events = {
# 	"all": [
# 		"teampro.tasks.all"
# 	],
# 	"daily": [
# 		"teampro.tasks.daily"
# 	],
# 	"hourly": [
# 		"teampro.tasks.hourly"
# 	],
# 	"weekly": [
# 		"teampro.tasks.weekly"
# 	],
#     "weekly":[
#         "checkpro.custom.task_mail_notification_status"
# 	],
# 	"monthly": [
# 		"teampro.tasks.monthly"
# 	]
# }

scheduler_events={
    "Weekly":[
		"checkpro.custom.task_mail_notification_status"
	],
    "Weekly":[
        "checkpro.custom.sales_order_invoiced"
	],
    "Weekly":[
        "teampro.email_alerts.create_email_sales_invoice_overdue_docs"
	]
}

# Testing
# -------

# before_tests = "teampro.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "teampro.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "teampro.task.get_dashboard_data"
# }



# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# fixtures = ['Client Script','Custom Field','Workspace','Print Format']