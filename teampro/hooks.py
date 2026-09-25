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
# app_include_css = "/assets/teampro/css/custom.css"
app_include_js = [
	"https://maps.googleapis.com/maps/api/js?sensor=false&libraries=places&key=AIzaSyAdaNNXhTh13TRLiZjSa9YYp66gNNj9aZ8",
]

boot_session = "teampro.boot.get_boot_data"			
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
doctype_js = {
	"Project": "public/js/project_monitoring.js"
}
doctype_list_js = {
	"Candidate": "public/js/candidate_list.js"
}
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
	# "Candidate": {
	# 	"after_insert": "teampro.custom_sync.push_candidate_to_jobpro"
	# },
    # "Website Item":{
    #     "after_insert":"teampro.custom.create_website_item",
	# },
    "ToDo":{
        "before_save":"teampro.utility.update_subject_from_description",
        "before_insert":"teampro.utility.set_creation_date",
	},
    "Leave Application":{
	# 	"after_insert": "jobpro.custom.restrict_leave"
		"on_submit":"checkpro.custom.update_session_leave",
		"on_cancel":"checkpro.custom.update_session_leave_cancel",
        "validate":"teampro.utility.update_tot_leave_days"
	},
	"Quotation":{
		"validate": "teampro.sales_invoice_method.calc_cut_off_prize",
        "after_insert":"teampro.teampro_hooks_method.set_quotation"
	},
	"Employee":{
		"validate": ["teampro.teampro_hooks_method.update_custodian","teampro.teampro_hooks_method.inactive_employee","teampro.teampro_hooks_method.emp_short_code_check"],
	},
    "Employee Onboarding": {
        "after_insert": "teampro.teampro_py.employee_onboarding.after_insert_employee_onboarding",
        "on_submit": "teampro.teampro_py.employee_onboarding.on_submit_employee_onboarding"
    },
	"Task":{
        "before_save":"teampro.utility.update_task_subject_from_description",
		"on_update": ["teampro.teampro_hooks_method.update_dm","teampro.teampro_hooks_method.issue_status","teampro.teampro_py.project.update_project_count"],
		
		"validate": ["teampro.teampro_hooks_method.update_issue_type","teampro.teampro_hooks_method.update_issue_typein_issue","teampro.teampro_hooks_method.old_sprint_alert","teampro.teampro_hooks_method.update_country_flag", "teampro.teampro_hooks_method.update_cb_bulk", "teampro.teampro_hooks_method.update_issue_wonjin", "teampro.teampro_py.task.update_prd_sprint_task", "teampro.teampro_py.task.validate_et"],
  
		"after_insert":["teampro.teampro_hooks_method.create_user_notification","teampro.teampro_hooks_method.update_criteria_table", "teampro.teampro.doctype.daily_monitor.dm_it_dev.update_daily_monitor_task"]

	},
    "Issue":{
        "after_insert":["teampro.teampro_hooks_method.update_project_issue","teampro.teampro_hooks_method.update_issueid_wonjin"]
       
	},
	"User Notifications":{
		"after_insert":"teampro.teampro_hooks_method.send_notification"
	},
	"Target Manager":{
        "after_insert":["teampro.teampro_hooks_method.update_service_tm","teampro.api.notify_target_change"],
		"after_delete": "teampro.api.notify_target_change",
        "after_update": "teampro.api.notify_target_change"
	},
    
    
	"Project":{
		"after_insert": ["teampro.teampro_hooks_method.create_project_completion_task","teampro.teampro_hooks_method.update_color_grade"],
        "validate":["teampro.teampro_hooks_method.update_sfp_remarks","teampro.teampro_py.project.update_sa_details_in_task","teampro.teampro_py.project.update_proj_position"],
        "on_update":['teampro.teampro_hooks_method.update_color_grade_specification',"teampro.teampro_hooks_method.update_project_image","teampro.teampro_hooks_method.cascade_status_to_tasks_and_candidates"]
	},
	"Journal Entry": {
		"validate": "teampro.teampro_hooks_method.update_cost_center"
	},
	"Timesheet":{
		"on_update": "teampro.teampro_hooks_method.fetch_start_time",
        "before_submit":"teampro.teampro_hooks_method.validate_timesheet",
        "on_submit":"teampro.teampro_hooks_method.update_working_remarks",
       
	},
	"Sales Order":{
		"on_submit":["teampro.teampro_hooks_method.update_batch_status",
               "teampro.teampro.doctype.target_manager.updated_target_manager.enqueue_so_submission","teampro.teampro_hooks_method.update_so_priority_on_submit"],
        "on_cancel": "teampro.teampro_hooks_method.update_pi_workflow",
        "validate": ["teampro.sales_invoice_method.calc_cut_off_prize","teampro.teampro_hooks_method.propagate_parent_remarks_to_items"],
	},
   
    "Sales Follow Up":{
        "after_insert": ["teampro.teampro_hooks_method.update_lead_contacts_sfp","teampro.teampro_hooks_method.update_spf_details_lead"]
	},
	"Opportunity": {
        "on_update":["teampro.teampro_hooks_method.update_lead_status","teampro.teampro_hooks_method.update_sfp_opportunity"]
		
	},
    "Daily Monitor":{
        "after_insert":"teampro.teampro.doctype.daily_monitor.daily_monitor.load_sprint_data",
        "validate":"teampro.teampro.doctype.daily_monitor.daily_monitor.update_sprint_avl_time"
	},
    "Sprint":{
        "validate":["teampro.teampro.doctype.sprint.sprint.update_sprint_hours","teampro.teampro.doctype.sprint.sprint.update_allocated_hrs","teampro.teampro.doctype.sprint.sprint.update_sprint_status"],
	},
    
	"Sales Invoice":{
       
		"on_submit": ["teampro.teampro.doctype.target_manager.updated_target_manager.enqueue_so_submission","teampro.sales_invoice_method.update_case_status_billed", "teampro.utility.update_submitted_si",],
        "on_trash":"teampro.utility.si_on_trash",
        "on_cancel": "teampro.utility.update_canceled_si",
        "validate": ["teampro.sales_invoice_method.calc_cut_off_prize","teampro.sales_invoice_method.validate_maintain_stok_si", "teampro.teampro_py.sales_invoice.update_payment_schedule_due_date","teampro.teampro_hooks_method.propagate_parent_remarks_to_items"],
        
	},
	"Attendance Request":{
		"on_cancel": ["teampro.teampro_hooks_method.update_wh_att","teampro.att_request.on_cancel_attendance_request","teampro.att_request.update_perm_req_in_att_cancel","checkpro.custom.update_session_ar_cancel","teampro.att_request.update_att_oncancel_mispunch"],
		"on_submit":["checkpro.custom.update_session_ar","teampro.att_request.on_submit_attendance_request","teampro.att_request.update_permission_req_in_att_submission"],
        "validate":["teampro.att_request.validate_att_working_day"],
        
	},
    
	"Purchase Invoice": {
        "validate":"teampro.teampro_hooks_method.calc_cost_prize",
    },
    "Purchase Order":{
        "validate":"teampro.teampro_hooks_method.calc_cost_prize",
		"on_submit":["teampro.teampro_hooks_method.update_ordered_qty", "teampro.teampro_hooks_method.update_material_request_status_on_submit"],
        "on_cancel":["teampro.teampro_hooks_method.update_ordered_qty_on_cancel"]
	},
    
	"Delivery Note":{
	"after_insert": "teampro.delivery_note_method.get_so_item_details",
    "validate":["teampro.delivery_note_method.set_totals_in_delivery_note", "teampro.teampro_hooks_method.propagate_parent_remarks_to_items"],
    "before_submit":["teampro.delivery_note_method.validate_packing_items_on_dn"],
    "on_submit":["teampro.delivery_note_method.update_so_priority","teampro.delivery_note_method.create_material_issue"],
	},
    "Salary Slip":{
        'validate':['teampro.teampro_hooks_method.update_employer_pf','teampro.teampro_hooks_method.override_payment_days_from_attendance']
	},
    "VM Stock Register":{
        "on_cancel":["teampro.teampro_hooks_method.update_stock_against_vm"]
	},
	"BG Entry Form": {
        "after_insert": "teampro.teampro.doctype.bg_entry_form.bg_entry_form.mark_files_public"
	},
    "Appraisal Cycle" :{
        "after_insert":"teampro.teampro_hooks_method.update_month_cycle",
	},
    "Appraisal":{
        "validate":["teampro.teampro_hooks_method.update_ep_nc_appraisal","teampro.teampro_hooks_method.update_grade"],
        "on_submit":"teampro.email_alerts.send_appraisal_mail",
        "before_submit":"teampro.teampro_hooks_method.validate_reviewer_remark",
        "before_insert":"teampro.teampro_hooks_method.update_company_by_employee"

	},
    "Stock Entry":{
        "on_submit":["teampro.teampro_hooks_method.create_packing_issue_stock_entry","teampro.teampro_hooks_method.auto_submit_stock","teampro.teampro.doctype.vm_stock_register.vm_stock_register.update_vm_status"],
		"on_cancel":["teampro.teampro_hooks_method.cancel_packing_issue_stock_entry"]
	},
    
	
    
	"Attendance":{
        "validate":"teampro.mark_attendance.update_att_as_present",
	},
    "Customer":{
        "after_insert":[ "teampro.teampro_hooks_method.update_lead_as_qualified","teampro.teampro_hooks_method.update_spf_status","teampro.utility.update_customer_contact_table","teampro.utility.update_sfp_details_customer"],
        "on_update":["teampro.teampro_hooks_method.update_project_dates", "teampro.utility.update_sfp_details_customer"],
        "validate":["teampro.teampro_hooks_method.set_customer_id"]
	},
    "Lead":{
        # "before_save": ["teampro.lead_ai_validator.validate_lead_with_ai"],
        "after_insert": ["teampro.teampro_hooks_method.update_check_existing_lead"]
	},
    # Lunch Attendance: react to inbound WhatsApp Quick-Reply button taps.
    "WhatsApp Message": {
        "after_insert": "teampro.lunch_attendance.handle_incoming_whatsapp_message"
	},
    # TPE audit trail
    "KPI Master": {"on_update": "teampro.tpe.audit.log_update", "on_trash": "teampro.tpe.audit.log_trash"},
    "KRA Master": {"on_update": "teampro.tpe.audit.log_update", "on_trash": "teampro.tpe.audit.log_trash"},
    "KPI Variable": {"on_update": "teampro.tpe.audit.log_update", "on_trash": "teampro.tpe.audit.log_trash"},
    "TPE Settings": {"on_update": "teampro.tpe.audit.log_update"},
}

# Scheduled Tasks
# ---------------
scheduler_events = {
	"daily": [
		"teampro.tpe.calculator.scheduled_monthly_calculation",
		"teampro.email_alerts.next_contact_alert",
		"teampro.email_alerts.meeting_status_check",
		"teampro.email_alerts.checkin_alert",
        "teampro.teampro.doctype.document_manager.document_manager.update_statuses",
        "checkpro.checkpro.doctype.case.case.update_case_age",
		"checkpro.checkpro.doctype.batch.batch.update_batch_age",
        "checkpro.checkpro.doctype.case.case.update_check_age",
        "jobpro.jobpro.doctype.candidate.candidate.update_cv_age",
        "checkpro.checkpro.doctype.case.case.tat_variation",
        "checkpro.checkpro.doctype.case.case.tat_calculation",
        "checkpro.checkpro.doctype.case.case.tat_monitor",
		"teampro.teampro.doctype.accounts_checklist.accounts_checklist.generate_daily",
	],
	"monthly": [
		"teampro.utility.create_update_leave_allocation",
        "teampro.custom.epnc_send_mail",
        "teampro.custom.ep_mail",
        "teampro.teampro_hooks_method.submit_previous_month_attendance",
		"teampro.teampro.doctype.accounts_checklist.accounts_checklist.generate_monthly",
	],
	"cron": {
		"45 23 * * *": [
			"teampro.teampro_py.project.update_proj_position_value",
		],
		"5 21 * * *": [
			"teampro.email_alerts.send_closure_report_with_table_dpr",
		],
		"00 00 * * 0": [
			"teampro.email_alerts.send_mail_for_expenseapproval_weekly_md",
			"teampro.email_alerts.send_mail_for_expenseapproval_weekly_ceo",
			"teampro.email_alerts.send_mail_for_expenseapproval_weekly_hod",
		],
		"15 15 * * *": [
			"teampro.email_alerts.send_project_spoc_report_weekly",
		],
		"00 00 1 * *": [
			"teampro.email_alerts.send_mail_for_update_checkpro_holiday",
			"teampro.teampro.doctype.energy_point_and_non_conformity.energy_point_and_non_conformity.create_new_epnc_review",
		],
		"00 09 * * *": [
			"teampro.email_alerts.update_sla_status_and_notify",
			"teampro.email_alerts.case_status_report_excel",
			"teampro.teampro.doctype.stock_counting.stock_counting.stock_counting_report_excel",
			"checkpro.custom.dpr_excel_format",
			"jobpro.jobpro.doctype.closure.closure.visa_expiry_alert",
			"jobpro.jobpro.doctype.closure.closure.fm_expiry_alert",
			"teampro.email_alerts.cases_with_insuff",
			"teampro.email_alerts.cases_beyond_tat_age_10",
			"teampro.teampro.doctype.psr_report_dashboard.psr_report_dashboard.send_daily_psr_report_in_htmt_view",
			"teampro.email_alerts.sendmail_luo_nad_alert",
			"teampro.custom.sales_dpr",
		],
		"00 00 * * *": [
			"teampro.teampro_py.task.task_age_calculation",
			"teampro.teampro.energy_point_and_non_conformity.energy_point_and_non_conformity.auto_submit_ep1",
			"checkpro.checkpro.doctype.batch.batch.update_case_status_existing_batch",
			"checkpro.checkpro.doctype.case.case.update_holiday_tat_case",
			"checkpro.checkpro.doctype.case.case.update_tat_case",
			"teampro.email_alerts.check_daily_attendance",
			"teampro.custom.update_issue_status",
		],
		"30 23 * * *": [
			"teampro.teampro.doctype.daily_monitor.dm_it_dev.run_daily_monitor_updates",
			"teampro.teampro_py.project.update_proj_positions_count",
			"teampro.teampro.doctype.rec_week_plan.rec_week_plan.run_week_monitor_dsr",
		],
		"50 23 * * *": [
			"teampro.teampro.doctype.daily_monitor.dm_it_dev.run_daily_monitor_dsr",
			"teampro.teampro_py.customer.update_sla_value",
		],
		"00 20 * * *": [
			"teampro.teampro.doctype.daily_monitor.dm_it_dev.dsr_task_mail_for_cmn_service",
		],
		"30 11 * * *": [
			"teampro.email_alerts.send_daily_candidate_status_alert",
		],
		"00 13 * * *": [
			"teampro.email_alerts.send_daily_candidate_status_alert1",
		],
		"00 15 * * *": [
			"teampro.email_alerts.send_daily_candidate_status_alert2",
		],
		"30 16 * * *": [
			"teampro.email_alerts.send_daily_candidate_status_alert3",
		],
		"00 21 * * *": [
			"teampro.email_alerts.send_daily_candidate_status_alert4",
			"teampro.email_alerts.send_closure_report_with_table_dsr",
			"teampro.email_alerts.send_fp_mail",
		],
		"50 23 * * 0": [
			"teampro.teampro.doctype.rec_week_plan.rec_week_plan.create_nc_for_weekplan",
		],
		"30 18 * * *": [
			"teampro.teampro.doctype.rec_week_plan.rec_week_plan.run_week_monitor_rec_dpr",
			"teampro.email_alerts.dpr_excel_format_bcs",
			"teampro.email_alerts.send_closure_mail",
			"teampro.email_alerts.dsr_mail",
			"teampro.email_alerts.dpnd_excel_format",
			"teampro.custom.send_closure_report_with_table",
			"checkpro.custom.statement_of_account",
		],
		"00 7 * * *": [
			"teampro.email_alerts.kt_email",
			"checkpro.checkpro.doctype.case.case.update_case_age",
		],
		"0 1 * * *": [
			"teampro.utility.create_update_leave_allocation_new",
			"teampro.email_alerts.task_mail",
			"checkpro.custom.task_mail",
			"checkpro.custom.dpr_over_all_task",
			"checkpro.custom.dpr_over_all_meeting",
			"checkpro.custom.dpr_over_all",
		],
		"0 * * * *": [
			"teampro.teampro_py.task.update_task_positions_count_hourly",
			"teampro.teampro_py.project.update_proj_positions_count_hourly",
			"teampro.teampro.doctype.target_manager.target_manager.calculate_target",
		],
		"*/5 * * * *": [
			"teampro.teampro_py.task.update_task_positions_count_min",
			"teampro.teampro_py.project.update_proj_positions_count_min1",
		],
		"0 23 * * *": [
			"teampro.att_request.create_comp_off_requests",
			"teampro.teampro.doctype.daily_monitor.dm_it_dev.send_daily_pr_report",
			"teampro.teampro.doctype.daily_monitor.dm_it_dev.kt_not_confirmed_task",
			"teampro.email_alerts.statement_of_account_test_1",
			"teampro.teampro.doctype.rec_week_plan.rec_week_plan.update_week_plan_ac_by_cron",
		],
		"00 10 * * *": [
			"teampro.teampro.doctype.daily_monitor.dm_it_dev.send_next_contact_by_report",
			"teampro.email_alerts.attendance_alert_mail",
		],
		"00 9 * * 1-6": [
			"teampro.lunch_attendance.send_daily_lunch_attendance",
		],
		"05 10 * * 1-6": [
			"teampro.lunch_attendance.mark_expired_logs",
		],
		"30 10 * * 1-6": [
			"teampro.lunch_attendance.send_consolidated_lunch_count",
		],
		"00 1 1 * *": [
			"teampro.utility.update_leave_ledger_entry",
		],
		"00 10 * * 1,4": [
			"teampro.email_alerts.sales_invoice_overdue_docs",
			"teampro.email_alerts.sales_invoice_follow_up_test",
		],
		"30 00 * * *": [
			"teampro.email_alerts.validate_for_easytimepro",
		],
		"00 11 * * *": [
			"teampro.email_alerts.fp_candidate_to_acc_manager",
			"teampro.email_alerts.fp_candidate_to_spoc",
			"teampro.email_alerts.fp_candidate_list_send_mails",
			"teampro.email_alerts.fp_candidate_list_send_mail_to_spoc",
		],
		"0 18 * * *": [
			"teampro.email_alerts.send_miss_punch",
			# "teampro.custom.send_project_spoc_report_daily",
			"teampro.email_alerts.candidate_excel_format",
			"teampro.email_alerts.cases_with_generate_report_status",
			"teampro.email_alerts.cases_with_to_be_billed_status",
			"teampro.email_alerts.cases_with_gr_daily_report",
			"teampro.email_alerts.insuff_consolidated_mail",
			"teampro.email_alerts.submitted_bg_entry",
			"teampro.email_alerts.cases_with_insuff_daily_report",
		],
		"35 10 * * *": [
			"teampro.email_alerts.daily_emc_report",
		],
		"30 10 * * *": [
			"teampro.email_alerts.daily_att_report",
			"teampro.custom.dsr_send_alert",
			"teampro.custom.dpr_send_alert",
		],
		"00 10 * * 2,5": [
			"checkpro.custom.sales_order_follow_up_test",
			"checkpro.custom.sales_order_follow_up",
		],
		"30 9 * * *": [
			"teampro.teampro_py.opportunity.update_opportunity_age",
			"teampro.email_alerts.purchase_invoice_beyond_duedate",
			"teampro.email_alerts.purchase_invoice_due_above",
		],
		"30 20 * * *": [
			"teampro.custom.send_sales_dsr_daily",
		],
		"00 06 * * *": [
			"jobpro.jobpro.doctype.candidate.candidate.update_cv_age",
		],
		"00 19 * * *": [
			"teampro.custom.send_project_report",
		],
		"*/10 * * * *": [
			"teampro.mark_attendance.mark_att",
		],
		"00 10 * * 1": [
			"checkpro.custom.task_mail_notification",
			"checkpro.custom.task_mail_notification_status",
			"checkpro.custom.sales_order_follow_up_test",
			"checkpro.custom.sales_invoice_follow_up_test",
		],
		"59 23 * * *": [
			"checkpro.custom.statement_of_account_test",
		],
		"0 2 1 * *": [
			"teampro.tpe.calculator.scheduled_monthly_calculation",
		],
	},
	"weekly": [
		"checkpro.custom.task_mail_notification_status",
		"checkpro.custom.sales_order_invoiced",
		"teampro.email_alerts.create_email_sales_invoice_overdue_docs",
		"teampro.teampro.doctype.accounts_checklist.accounts_checklist.generate_weekly",
	]
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
		"teampro.teampro.page.it_sw_dashboard_1.production_pdf_print.get_today_task_data",
        
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
override_doctype_dashboards = {
	"Project": "teampro.teampro_py.project_monitoring.get_project_dashboard"
}

override_doctype_class = {
    "Event": "teampro.overrides.customEvent",
    # "POS Opening Entry": "teampro.overrides.CustomPOSOpeningEntry",
    # "Task": "teampro.overrides.customTask",
    # "Leave Application": "teampro.overrides.CustomLeaveApplication",
    # "Attendance Request": "teampro.overrides.CustomAttendanceRequest",
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = ['Custom Field']

# ============================================================
# TEAMPRO Performance Engine (TPE) hooks
# ============================================================

# Auto-install / seed TPE masters on first install
after_install = "teampro.tpe.install.after_install"

# TPE dashboard page CSS (loaded per-page via Page JS)

# === Accounts Checklist (DPR/DSR) hooks ===
# Added by accounts_checklist deploy. Idempotent.
# NOTE: scheduler entries injected via _inject_hooks.py


# WeasyPrint PDF generator for builder-beta print formats
pdf_generator = "teampro.weasyprint_pdf.weasyprint_pdf_generator"
