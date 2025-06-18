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
    "ToDo":{
        "before_save":"teampro.utility.update_subject_from_description",
        "before_insert":"teampro.utility.set_creation_date",
	},
    "File":{
		"before_save": "teampro.utility.rename_file"
	},
    "Leave Application":{
		"after_insert": "jobpro.custom.restrict_leave"
	},
	"Quotation":{
		"validate": "teampro.custom.calc_cut_off_prize",
        "after_insert":"teampro.custom.set_quotation"
	},
	"Employee":{
		"validate": ["teampro.custom.update_custodian","teampro.custom.inactive_employee"],
        # "after_insert": "checkpro.custom.after_insert_employee_onboarding"
	},
    "Employee Onboarding": {
        "after_insert": "checkpro.custom.after_insert_employee_onboarding",
        "on_submit": "checkpro.custom.on_submit_employee_onboarding"
    },
	"Task":{
        "before_save":"teampro.utility.update_task_subject_from_description",
		"on_update": ["teampro.custom.issue_status","jobpro.custom.update_project_count"],
		"validate": ["teampro.custom.update_issue_wonjin","teampro.custom.update_issue_type","teampro.custom.update_issue_typein_issue","teampro.custom.update_country_flag","jobpro.custom.update_project_count"],
		"after_insert":["teampro.api.create_user_notification","checkpro.custom.send_task_creation_email","teampro.custom.update_criteria_table"]

	},
    "Issue":{
        "after_insert":["teampro.custom.update_project_issue","teampro.custom.update_issueid_wonjin"]
	},
	"User Notifications":{
		"after_insert":"teampro.api.send_notification"
	},
	"Target Manager":{
        "after_insert":"teampro.custom.update_service_tm"
	},
    
    # "Court":{
    #     "on_update":["teampro.custom.update_tat_completion_date_court","teampro.custom.update_tat_completion_date_court_ch"]
	# },
	"Project":{
		"after_insert": "teampro.custom.create_project_completion_task",
        "validate":["teampro.custom.update_sfp_remarks","jobpro.custom.update_sa_details_in_task"],
        "on_update":'teampro.custom.update_table_in_task'
	},
	"Journal Entry": {
		"validate": "teampro.custom.update_cost_center"
	},
	"Timesheet":{
		"on_update": "teampro.custom.fetch_start_time",
		# "before_submit":"teampro.custom.return_detailed_ts"
        "before_submit":"teampro.custom.validate_timesheet",
        "on_submit":"teampro.custom.update_working_remarks",
        # "validate":"teampro.custom.validate_et_vs_at"
	},
	"Sales Order":{
		"on_submit":["teampro.custom.update_batch_status",
               "teampro.teampro.doctype.target_manager.updated_target_manager.calculate_target_for_manager_inso_test",
               "teampro.custom.so_creation_mail_it_sw","teampro.custom.send_mail_so_submission","teampro.custom.update_so_priority_on_submit"],
        "on_cancel": "teampro.custom.update_pi_workflow",
        "validate": ["teampro.custom.calc_cut_off_prize"],
        # "after_insert":"teampro.custom.update_cover_count",
		# "after_submit": "teampro.teampro.doctype.target_manager.target_manager.calculate_target_on_update_manager",
		# "on_update":"teampro.custom.skip_dn_so",
        # "validate":"teampro.custom.child_table_calc"
	},
    # "Target Manager":{
    #     "validate":["teampro.teampro.doctype.target_manager.updated_target_manager.calculate_target_for_manager_inso_test"]
	# },
    "Sales Follow Up":{
        "after_insert": ["teampro.custom.update_lead_contacts_sfp","teampro.custom.update_spf_details_lead"]
	},
	"Opportunity": {
		"after_insert": "teampro.custom.opportunity_send_mail",
        "on_update":["teampro.custom.update_lead_status","teampro.custom.update_sfp_opportunity"]
		# "on_cancel": "method",
		# "on_trash": "method"
	},
    "Daily Monitor":{
        "after_insert":"teampro.teampro.doctype.daily_monitor.daily_monitor.load_sprint_data",
        "validate":"teampro.teampro.doctype.daily_monitor.daily_monitor.update_sprint_avl_time"
	},
    "Sprint":{
        "validate":["teampro.teampro.doctype.sprint.sprint.update_sprint_hours","teampro.teampro.doctype.sprint.sprint.update_allocated_hrs","teampro.teampro.doctype.sprint.sprint.update_sprint_status","teampro.teampro.doctype.sprint.sprint.validate_allocate_hrs"]
	},
	"Candidate": {
		"on_update": ["teampro.custom.update_task_count"]
	},
    "Attendance Permission":{
        "validate":["teampro.custom.validate_permission_request"],
        "on_submit":["teampro.custom.update_permission_req_in_att"],
        "on_cancel":["teampro.custom.update_permission_req_in_att_cancel"],
        "after_insert":["jobpro.custom.mesg_for_permission"]
	},
	# "Payment Entry":{
	# 	"on_submit":"jobpro.jobpro.doctype.closure.closure.closure_payment_entry"
	# },
	"Sales Invoice":{
        # "validate":["teampro.custom.get_all_quot"],
		# "validate": "teampro.custom.sales_order_batch",
		# "after_submit": "teampro.teampro.doctype.target_manager.target_manager.calculate_target_on_update",
		"on_submit": ["teampro.teampro.doctype.target_manager.updated_target_manager.calculate_target_for_manager_inso_test","checkpro.custom.update_case_status_billed"],
        "on_trash":"teampro.utility.si_on_trash",
        "validate": ["teampro.custom.clear_payment_table_si","teampro.custom.validate_maintain_stok_si","teampro.custom.calc_cut_off_prize"]
		# "validate": ["teampro.custom.calc_cut_off_prize","teampro.custom.clear_payment_table_si"]
		# "on_submit": "teampro.custom.get_against_so"
	},
	"Attendance Request":{
		"on_cancel": "teampro.custom.update_wh_att",
        "after_insert": "jobpro.custom.restrict_att_req",
        
	},
	"Purchase Invoice": {
        # "before_submit": "teampro.custom.validate_date",
        "on_update":"teampro.custom.update_workflow_state",
        "validate":"teampro.custom.calc_cost_prize"
    },
    "Purchase Order":{
        "validate":"teampro.custom.calc_cost_prize",
		"on_submit":["teampro.custom.update_ordered_qty", "teampro.custom.update_material_request_status_on_submit"],
        "on_cancel":["teampro.custom.update_ordered_qty_on_cancel"]
	},
    # "Stock Counting":{
    #     "validate":"teampro.custom.validate_stock_counting"
	# },
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
	"Delivery Note":{
	"after_insert": "teampro.custom.get_so_item_details",
    "validate":["teampro.custom.set_totals_in_delivery_note"],
    "on_submit":["teampro.custom.update_so_priority","teampro.custom.create_material_isse"],
    # "on_cancel":"teampro.custom.cancel_material_isse"
	},
    "VM Stock Register":{
        "on_submit":["teampro.teampro.doctype.vm_stock_register.vm_stock_register.create_re_filling_stock_entries","teampro.teampro.doctype.vm_stock_register.vm_stock_register.create_packing_stock_entries"],
        # "validate":"teampro.teampro.doctype.vm_stock_register.vm_stock_register.create_packing_stock_entries",
	},
	"BG Entry Form": {
        "after_insert": "teampro.teampro.doctype.bg_entry_form.bg_entry_form.mark_files_public"
	},
    "Appraisal Cycle" :{
        "after_insert":"teampro.custom.update_month_cycle"
	},
    "Stock Entry":{
        "on_submit":"teampro.teampro.doctype.vm_stock_register.vm_stock_register.update_vm_status",
	},
    
	# "Job Applicant": {
    #     "after_insert": "teampro.utility.mark_files_public"
	# },
    
	# "Attendance":{
    #     "on_cancel":"teampro.mark_attendance.cancel_comp_off",
    #     "on_update":"teampro.mark_attendance.update_coff",
	# },
    "Customer":{
        "after_insert":[ "teampro.custom.update_lead_as_qualified","teampro.custom.update_spf_status"],
        "on_update":["teampro.custom.update_project_dates"],
        "validate":"teampro.custom.set_customer_id"
	},
    "Lead":{
        # "after_insert": ["teampro.custom.update_existing_lead","teampro.custom.update_check_existing_lead"]
        "after_insert": ["teampro.custom.update_check_existing_lead"]
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
        "checkpro.checkpro.doctype.case.case.tat_variation",
        "checkpro.checkpro.doctype.case.case.tat_calculation",
        "checkpro.checkpro.doctype.case.case.tat_monitor",
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
        "00 1 1 * *" : [
			"teampro.utility.update_leave_ledger_entry"
		],
        "00 10 * * 1,4" : [
			"teampro.email_alerts.sales_invoice_overdue_docs"
		],
        "*/55 * * * *" : [
			"teampro.mark_attendance.mark_att"
		],
        "30 00 * * *" : [
			"teampro.email_alerts.validate_for_easytimepro"
		],
        "00 11 * * *" : [
			"jobpro.custom.fp_candidate_to_acc_manager"
		],
        "00 11 * * *" : [
			"jobpro.custom.fp_candidate_to_spoc"
		],
        "00 11 * * *" : [
			"jobpro.custom.fp_candidate_list_send_mails"
		],
        "00 11 * * *" : [
			"jobpro.custom.fp_candidate_list_send_mail_to_spoc"
		],
        "0 18 * * *" : [
			"teampro.email_alerts.send_miss_punch"
		],
        "00 10 1 * *" : [
			"teampro.mark_attendance.mark_att"
		],
        "35 10 * * *" : [
			"teampro.email_alerts.daily_emc_report"
		],
        "30 10 * * *" : [
			"teampro.email_alerts.daily_att_report"
		],
        "0 1 * * *" : [
			"checkpro.custom.task_mail"
		],
        "00 18 * * *" : [
			"checkpro.custom.candidate_excel_format"
		],
        "00 10 * * 1,4" : [
			"checkpro.custom.sales_invoice_follow_up_test"
		],
        "00 10 * * 2,5" : [
			"checkpro.custom.sales_order_follow_up_test"
		],
        "00 10 * * 2,5" : [
			"checkpro.custom.sales_order_follow_up"
		],
        "00 23 * * *" : [
			"checkpro.custom.statement_of_account_test_1"
		],
        "00 18 * * *" : [
			"checkpro.custom.cases_with_generate_report_status"
		],
        "00 18 * * *" : [
			"checkpro.custom.cases_with_to_be_billed_status"
		],
        "00 18 * * *" : [
			"checkpro.custom.cases_with_gr_daily_report"
		],
        "00 18 * * *" : [
			"checkpro.custom.insuff_consolidated_mail"
		],
        "00 18 * * *" : [
			"checkpro.custom.submitted_bg_entry"
		],
        "00 09 * * *" : [
			"checkpro.custom.dpr_excel_format"
		],
        "30 18 * * *" : [
			"checkpro.custom.dsr_mail"
		],
        "00 18 * * *" : [
			"checkpro.custom.cases_with_insuff_daily_report"
		],
        "00 9 * * *" : [
			"checkpro.custom.cases_beyond_tat_age_10"
		],
        "0 18 * * *" : [
			"teampro.custom.send_project_spoc_report_daily"
		],
        "30 9 * * *" : [
			"teampro.custom.update_opportunity_age"
		],
        "30 20 * * *" : [
			"teampro.custom.send_sales_dsr_daily"
		],
		"00 9 * * *" : [
			"teampro.custom.sales_dpr"
		],
        "30 9 * * *" : [
			"teampro.custom.purchase_invoice_beyond_duedate"
		],
        "30 9 * * *" : [
			"teampro.custom.purchase_invoice_due_above"
		],
        "0 0 * * *" : [
			"teampro.custom.update_issue_status"
		],
        "30 10 * * *" : [
			"teampro.custom.dsr_send_alert"
		],
		"30 10 * * *" : [
			"teampro.custom.dpr_send_alert"
		],
		"30 18 * * *" : [
			"teampro.custom.dpnd_excel_format"
		],
        "00 06 * * *" : [
			"teampro.custom.update_cv_age"
		],
        "00 19 * * *" : [
			"teampro.custom.send_project_report"
		],
        "00 07 * * *" : [
			"teampro.custom.update_case_age"
		],
		"30 18 * * *" : [
			"teampro.custom.send_closure_report_with_table"
		],
        "00 9 * * *" : [
			"teampro.custom.create_food_count"
		],
        "00 10 1 * *" : [
			"teampro.mark_attendance.mark_att"
		],
        "00 9 * * *" : [
			"teampro.teampro.doctype.food_count.food_count.create_food_count"
		],
        "35 10 * * *" : [
			"teampro.email_alerts.daily_emc_report"
		],
        "30 10 * * *" : [
			"teampro.email_alerts.daily_att_report"
		],
        "0 * * * *" : [
			"teampro.teampro.doctype.target_manager.target_manager.calculate_target"
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
        "teampro.custom.get_so_delivery_data",
        "teampro.custom.get_packing_slip_table",
        "teampro.custom.get_dn_packing_details",
        "teampro.custom.get_task_details",
        "teampro.teampro.doctype.tfp_production_plan.tfp_production_plan.tfp_production_plan_report",
        "teampro.custom.employee_chc_print",
        "teampro.custom.employee_joining_print",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.batch_status_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.opportunity_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_sales_invoice_outstanding_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_sales_order_outstanding_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.ptsr_report",
		"teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_psr_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_psr_report_for_cust",
        # "jobpro.custom.print_psr_report_for_proj",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_psr_report_for_proj",
		"teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_closure_count_report",
		"teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_closure_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_closure_count_report_so_true",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.print_closure_count_report_so",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.todo_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.appointment_schedule_report",
        "teampro.teampro.doctype.formatted_reports__download.formatted_reports__download.appointment_taken_report",
        "teampro.custom.get_tfp_item",
        
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
# print_formats = {
#     "Employee Onboarding": {
#         "set_data": "checkpro.custom.get_employee_onboarding_data"
#     }
# }

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

override_doctype_class = {
    "Event": "teampro.overrides.customEvent",
    # "Task": "teampro.overrides.customTask",
    "Leave Application": "teampro.overrides.CustomLeaveApplication",
    "Attendance Request": "teampro.overrides.CustomAttendanceRequest",
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# fixtures = ['Client Script','Custom Field','Workspace','Print Format']


