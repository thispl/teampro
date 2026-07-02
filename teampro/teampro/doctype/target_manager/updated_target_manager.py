import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import datetime

def extract_year(date_input):
	if isinstance(date_input, str):
		date_object = datetime.strptime(date_input, '%Y-%m-%d')
	else:
		date_object = date_input
	return date_object.year



@frappe.whitelist()
def calculate_target_for_manager_test(name,emp,year):
	def get_month_range(start_date, end_date):
		current = start_date.replace(day=1)
		end = end_date.replace(day=1)
		months = []
		while current <= end:
			months.append(current)
			current += relativedelta(months=1)
		return months

	tps = frappe.get_all('Target Manager',{"custom_fiscal_year":year,"employee":emp},['*'])
	
	map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
				  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
	
	mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
					  'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
	
	for tp in tps:
		doc = frappe.get_doc('Target Manager', tp.name)
		doc.target_child = []
		doc.monthly_ft_allocation=[]
		user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
		user_list = [user_id]
		for row in doc.reportees:
			user_list.append(row.reportee)
		user_list_sql = ", ".join(f"'{user}'" for user in user_list)
		service_list = []
		if doc.service_list:
			for serv in doc.service_list:
				service_list.append(serv.service)
		service_list_sql = ", ".join(f"'{ser}'" for ser in service_list)
		if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Order':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft
				})
		   
			total_months = len(doc.target_child)
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				# Save document after changes
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
		# 
		if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft
				})
		   
			total_months = len(doc.target_child)
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
	   
		elif tp.based_on_service ==1 and tp.based_on_candidate_owner ==0 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft
				})
			
			total_months = len(doc.target_child)
			
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""

					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit() 
		# 
		elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft
				})
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					# Execute the query with parameters for month and year
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""

					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit() 
		elif tp.based_on_candidate_owner ==1 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			num_months = len(months)
			# ct = doc.annual_ct / num_months if num_months else 0
			# ft = doc.annual_ft / num_months if num_months else 0
			# for dt in months:
			#     month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
			#     month_num = dt.strftime('%m')   # '01', '02', etc.

			#     doc.append('target_child', {
			#         'month': month_name,
			#         'month_nos': month_num,
			#         'ct': ct
			#     })
			#     doc.append('monthly_ft_allocation', {
			#         'month': month_name,
			#         'month_nos': month_num,
			#         'ft': ft
			#     })
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0

			for dt in months:
				month_name = dt.strftime('%b')
				month_num = dt.strftime('%m')
				override_ct = ct 
				override_ft=ft
				if tp.custom_fiscal_year == "2025-2026":
					special_months = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar'] 
					if month_name in special_months: 
						if tp.user_id== "aruna.g@groupteampro.com":
							override_ct = 1200000
							override_ft=1200000
						if tp.user_id== "lokeshkumar.a@groupteampro.com":
							override_ct = 900000
							override_ft=900000

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': override_ct    
				})

				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': override_ft
				})
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit() 
		
	return 'OK'

from frappe.utils import nowdate, getdate
from frappe.utils.background_jobs import enqueue
@frappe.whitelist()
def enqueue_so_submission(doc, method):
	
	enqueue(method=calculate_target_for_manager_inso_test, queue="long", timeout=96000)
	
@frappe.whitelist()
def calculate_target_for_manager_inso_test():
	today = getdate(nowdate())

	current_fy = frappe.db.get_value(
		"Fiscal Year",
		{
			"year_start_date": ("<=", today),
			"year_end_date": (">=", today)
		},
		"name"
	)

	tps = frappe.get_all('Target Manager',filters={'custom_fiscal_year': current_fy},fields=['*'])
	def get_month_range(start_date, end_date):
		current = start_date.replace(day=1)
		end = end_date.replace(day=1)
		months = []
		while current <= end:
			months.append(current)
			current += relativedelta(months=1)
		return months
	map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
				  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
	
	mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
					  'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
	
	filtered_tps=[]
	for tp in tps:
		if tp.based_on_account_manager or tp.based_on_service or tp.based_on_candidate_owner:
			filtered_tps.append(tp)
	
	for tp in filtered_tps:
		doc = frappe.get_doc('Target Manager', tp.name)
		doc.target_child = []
		doc.achieved_data = []
		doc.monthly_ft_allocation=[]
		user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
		user_list = [user_id]
		for row in doc.reportees:
			user_list.append(row.reportee)
		user_list_sql = ", ".join(f"'{user}'" for user in user_list)
		service_list = []
		if doc.service_list:
			for serv in doc.service_list:
				service_list.append(serv.service)
		service_list_sql = ", ".join(f"'{ser}'" for ser in service_list)
		if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Order':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			num_months = len(months)
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				})
		   
			total_months = len(doc.target_child)
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
							SELECT
							so.name,
							so.transaction_date,
							so.service,
							so.customer,
							so.base_total
							FROM `tabSales Order` AS so
							WHERE so.account_manager IN ({user_list_sql}) 
							AND MONTH(so.transaction_date) = %s 
							AND YEAR(so.transaction_date) = %s 
							AND so.docstatus=1
							AND so.status NOT IN ('Cancelled')
							"""
				records = frappe.db.sql(query, (month, year), as_dict=True)
				achieved_value = 0
				for asor in records:
					achieved_value += asor.base_total
					doc.append("achieved_data", {
						"date": asor.transaction_date,
						"document_type": "Sales Order",
						"id": asor.name,
						"service": asor.service,
						"amount_cc": asor.base_total,
						"customer": asor.customer
					})
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
							SELECT sum(so.base_total) as total
							FROM `tabSales Order` AS so
							WHERE account_manager IN ({user_list_sql}) 
							AND MONTH(so.transaction_date) = %s 
							AND YEAR(so.transaction_date) = %s 
							AND so.docstatus=1
							AND so.status NOT IN ('Cancelled')
							"""
				achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0

				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				# Save document after changes
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.set_user("Administrator")
		# 
		if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				})
		   
			total_months = len(doc.target_child)
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)  
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
							SELECT so.base_total, so.posting_date, so.services, so.name, so.customer
							FROM `tabSales Invoice` AS so
							WHERE so.account_manager IN ({user_list_sql}) 
							AND MONTH(so.posting_date) = %s 
							AND YEAR(so.posting_date) = %s 
							AND so.docstatus=1
							AND so.status NOT IN ('Cancelled')
							"""
				achieved_si_records = frappe.db.sql(query, (month, year), as_dict=True)  
				achieved_value = 0
				for asir in achieved_si_records:
					achieved_value += asir.base_total
					doc.append("achieved_data", {
						"date": asir.posting_date,
						"document_type": "Sales Invoice",
						"id": asir.name,
						"service": asir.services,
						"amount_cc": asir.base_total,
						"customer": asir.customer,
					})

				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
							SELECT SUM(so.base_total) as total
							FROM `tabSales Invoice` AS so
							WHERE account_manager IN ({user_list_sql}) 
							AND MONTH(so.posting_date) = %s 
							AND YEAR(so.posting_date) = %s 
							AND so.docstatus=1
							AND so.status NOT IN ('Cancelled')
							"""
				achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0

				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.set_user("Administrator")
	   
		elif tp.based_on_service ==1 and tp.based_on_candidate_owner ==0 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				})
			

			total_months = len(doc.target_child)
			
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
					
				query = f"""
					SELECT si.base_total, si.name, si.services, si.posting_date, si.customer
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
				"""
				achieved_si_records = frappe.db.sql(query, (month, year), as_dict=True)
				achieved_value = 0
				for asir in achieved_si_records:
					achieved_value += asir.base_total
					doc.append("achieved_data", {
						"date": asir.posting_date,
						"document_type": "Sales Invoice",
						"id": asir.name,
						"service": asir.services,
						"amount_cc": asir.base_total,
						"customer": asir.customer
					})

				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
					SELECT SUM(si.base_total) as total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
				"""
				achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0

				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.set_user("Administrator")
		# 
		elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				})
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
					
				query = f"""
				SELECT si.base_total, si.transaction_date, si.name, si.service, si.customer
				FROM `tabSales Order` AS si
				WHERE MONTH(si.transaction_date) = %s
				AND YEAR(si.transaction_date) = %s
				AND si.service IN ({service_list_sql})
				AND si.docstatus=1
				AND si.status NOT IN ('Cancelled')
				"""
				achieved_so_records = frappe.db.sql(query, (month, year), as_dict=True)
				achieved_value = 0
				for asor in achieved_so_records:
					achieved_value += asor.base_total
					doc.append("achieved_data", {
						"date": asor.transaction_date,
						"document_type": "Sales Order",
						"id": asor.name,
						"service": asor.service,
						"amount_cc": asor.base_total,
						"customer": asor.customer
					})

				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
				SELECT SUM(si.base_total) as total
				FROM `tabSales Order` AS si
				WHERE MONTH(si.transaction_date) = %s
				AND YEAR(si.transaction_date) = %s
				AND si.service IN ({service_list_sql})
				AND si.docstatus=1
				AND si.status NOT IN ('Cancelled')
				"""
				achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0

				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit() 
				frappe.set_user("Administrator")
		elif tp.based_on_candidate_owner ==1 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			months = get_month_range(start_date, end_date)
			num_months = len(months)
			
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')
				month_num = dt.strftime('%m')
				override_ct = ct 
				override_ft=ft
				
				if tp.custom_fiscal_year == "2025-2026":
					special_months = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar'] 
					if month_name in special_months: 
						if tp.user_id== "aruna.g@groupteampro.com":
							override_ct = 1200000 
							override_ft=1200000
						if tp.user_id== "lokeshkumar.a@groupteampro.com":
							override_ct = 900000
							override_ft=900000
				override_annual_ct_point=(override_ct / point_value) if point_value else 0
				override_annual_ft_point=(override_ft / point_value) if point_value else 0
				override_monthly_ct_point = override_annual_ct_point / num_months if num_months else 0
				override_monthly_ft_point = override_annual_ft_point / num_months if num_months else 0
				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': override_ct,
					'ct_point':override_monthly_ct_point
				})

				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': override_ft,
					'ft_point':override_monthly_ft_point
				})
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
					SELECT sii.base_amount, si.name, si.posting_date, si.services, sii.item_code, si.customer
					FROM `tabSales Invoice` AS si
					INNER JOIN `tabSales Invoice Item` AS sii
					ON si.name = sii.parent
					WHERE sii.candidate_owner IN ({user_list_sql})
					AND MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services='REC-I'
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
				"""
				achieved_si_records = frappe.db.sql(query, (month, year), as_dict=True)
				achieved_value = 0
				for asir in achieved_si_records:
					achieved_value += asir.base_amount
					doc.append("achieved_data", {
						"date": asir.posting_date,
						"document_type": "Sales Invoice",
						"id": asir.name,
						"service": asir.services,
						"item_code": asir.item_code,
						"amount_cc": asir.base_amount,
						"customer": asir.customer,
					})
					
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
				
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
				else:
					year = extract_year(tp.custom_year_start_date)
				query = f"""
					SELECT SUM(sii.base_amount) AS total
					FROM `tabSales Invoice` AS si
					INNER JOIN `tabSales Invoice Item` AS sii
					ON si.name = sii.parent
					WHERE sii.candidate_owner IN ({user_list_sql})
					AND MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services='REC-I'
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
				"""
				achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.set_user("Administrator") 
		
			
	return 'OK'

import frappe

@frappe.whitelist()
def get_point_value(company, fiscal_year):
	value = frappe.db.get_value(
		"Company Point and value",
		{
			"parent": company,
			"fiscal_year": fiscal_year
		},
		"value"
	)
	return value

@frappe.whitelist()
def calculate_target_for_manager_point(name,emp,year):
	def get_month_range(start_date, end_date):
		current = start_date.replace(day=1)
		end = end_date.replace(day=1)
		months = []
		while current <= end:
			months.append(current)
			current += relativedelta(months=1)
		return months

	tps = frappe.get_all('Target Manager',{"custom_fiscal_year":year,"employee":emp},['*'])
	
	map_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
				  'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
	
	mapping_months = {'Apr': '12', 'May': '11', 'Jun': '10', 'Jul': '9', 'Aug': '8', 'Sep': '7', 
					  'Oct': '6', 'Nov': '5', 'Dec': '4', 'Jan': '3', 'Feb': '2', 'Mar': '1'}
	
	for tp in tps:
		doc = frappe.get_doc('Target Manager', tp.name)
		doc.target_child = []
		doc.monthly_ft_allocation=[]
		user_id = frappe.db.get_value('Employee', {'name': doc.employee}, 'user_id')
		user_list = [user_id]
		for row in doc.reportees:
			user_list.append(row.reportee)
		user_list_sql = ", ".join(f"'{user}'" for user in user_list)
		service_list = []
		if doc.service_list:
			for serv in doc.service_list:
				service_list.append(serv.service)
		service_list_sql = ", ".join(f"'{ser}'" for ser in service_list)
		if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Order':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				   
				})
		   
			total_months = len(doc.target_child)
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Order` AS so
								WHERE account_manager IN ({user_list_sql}) 
								AND MONTH(so.transaction_date) = %s 
								AND YEAR(so.transaction_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				# Save document after changes
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
		# 
		if tp.based_on_account_manager==1 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				})
		   
			total_months = len(doc.target_child)
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0    
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE so.account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
								SELECT SUM(so.base_total) AS total 
								FROM `tabSales Invoice` AS so
								WHERE account_manager IN ({user_list_sql}) 
								AND MONTH(so.posting_date) = %s 
								AND YEAR(so.posting_date) = %s 
								AND so.docstatus=1
								AND so.status NOT IN ('Cancelled')
								"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0  
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit()
	   
		elif tp.based_on_service ==1 and tp.based_on_candidate_owner ==0 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date

			months = get_month_range(start_date, end_date)
			num_months = len(months)
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  
				month_num = dt.strftime('%m')  

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				})
			
			total_months = len(doc.target_child)
			
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""

					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Invoice` AS si
					WHERE MONTH(si.posting_date) = %s
					AND YEAR(si.posting_date) = %s
					AND si.services IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit() 
		# 
		elif tp.based_on_service ==1 and tp.target_based_unit == 'Sales Order':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			months = get_month_range(start_date, end_date)
			num_months = len(months)
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
				month_num = dt.strftime('%m')   # '01', '02', etc.

				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': ct,
					'ct_point':monthly_ct_point
				})
				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': ft,
					'ft_point':monthly_ft_point
				})
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					# Execute the query with parameters for month and year
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""

					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
					SELECT SUM(si.base_total) AS total
					FROM `tabSales Order` AS si
					WHERE MONTH(si.transaction_date) = %s
					AND YEAR(si.transaction_date) = %s
					AND si.service IN ({service_list_sql})
					AND si.docstatus=1
					AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit() 
		elif tp.based_on_candidate_owner ==1 and tp.target_based_unit == 'Sales Invoice':
			pending_ct = 0
			pending_ft = 0
			start_date = tp.custom_year_start_date
			end_date = tp.custom_year_end_date
			point_value = frappe.db.get_value(
				"Company Point and value",
				{
					"parent": doc.custom_company,
					"fiscal_year": doc.custom_fiscal_year
				},
				"value"
			) or 1
			months = get_month_range(start_date, end_date)
			num_months = len(months)
			# ct = doc.annual_ct / num_months if num_months else 0
			# ft = doc.annual_ft / num_months if num_months else 0
			# for dt in months:
			#     month_name = dt.strftime('%b')  # 'Jan', 'Feb', etc.
			#     month_num = dt.strftime('%m')   # '01', '02', etc.

			#     doc.append('target_child', {
			#         'month': month_name,
			#         'month_nos': month_num,
			#         'ct': ct
			#     })
			#     doc.append('monthly_ft_allocation', {
			#         'month': month_name,
			#         'month_nos': month_num,
			#         'ft': ft
			#     })
			ct = doc.annual_ct / num_months if num_months else 0
			ft = doc.annual_ft / num_months if num_months else 0
			annual_ct_point = (doc.annual_ct / point_value) if point_value else 0
			monthly_ct_point = annual_ct_point / num_months if num_months else 0
			annual_ft_point = (doc.annual_ft / point_value) if point_value else 0
			monthly_ft_point = annual_ft_point / num_months if num_months else 0
			for dt in months:
				month_name = dt.strftime('%b')
				month_num = dt.strftime('%m')
				override_ct = ct 
				override_ft=ft
				if tp.custom_fiscal_year == "2025-2026":
					special_months = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar'] 
					if month_name in special_months: 
						if tp.user_id== "aruna.g@groupteampro.com":
							override_ct = 1200000
							override_ft=1200000
						if tp.user_id== "lokeshkumar.a@groupteampro.com":
							override_ct = 900000
							override_ft=900000
				override_annual_ct_point=(override_ct / point_value) if point_value else 0
				override_annual_ft_point=(override_ft / point_value) if point_value else 0
				override_monthly_ct_point = override_annual_ct_point / num_months if num_months else 0
				override_monthly_ft_point = override_annual_ft_point / num_months if num_months else 0
				doc.append('target_child', {
					'month': month_name,
					'month_nos': month_num,
					'ct': override_ct,
					'ct_point':override_monthly_ct_point    
				})

				doc.append('monthly_ft_allocation', {
					'month': month_name,
					'month_nos': month_num,
					'ft': override_ft,
					'ft_point':override_monthly_ft_point
				})
			for tc in doc.target_child:
				month = map_months.get(tc.month)
				month_no = mapping_months.get(tc.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				tc.revised_ct = tc.ct + pending_ct
				tc.achieved = achieved_value
				tc.ct_yta = tc.revised_ct - achieved_value
				tc.cr_ct_point = (tc.revised_ct / point_value) if point_value else 0
				tc.ct_yta_point = (tc.ct_yta / point_value) if point_value else 0
				tc.achieved_point=(tc.achieved/point_value) if point_value else 0
				tc.sr=(achieved_value/tc.revised_ct)*100 if tc.revised_ct else 0
				pending_ct = tc.ct_yta
			for i in doc.monthly_ft_allocation:
				month = map_months.get(i.month)
				month_no = mapping_months.get(i.month)
				if month in ['01', '02', '03']:
					year = extract_year(tp.custom_year_end_date)
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				else:
					year = extract_year(tp.custom_year_start_date)
					query = f"""
						SELECT SUM(sii.base_amount) AS total
						FROM `tabSales Invoice` AS si
						INNER JOIN `tabSales Invoice Item` AS sii
						ON si.name = sii.parent
						WHERE sii.candidate_owner IN ({user_list_sql})
						AND MONTH(si.posting_date) = %s
						AND YEAR(si.posting_date) = %s
						AND si.services='REC-I'
						AND si.docstatus=1
						AND si.status NOT IN ('Cancelled')
					"""
					achieved_value = frappe.db.sql(query, (month, year), as_dict=True)[0].total or 0
				i.cr_ft = i.ft + pending_ft
				i.f_achieved = achieved_value
				i.ftyta = i.cr_ft - achieved_value
				pending_ft = i.ftyta
				i.cr_ft_point = (i.cr_ft / point_value) if point_value else 0
				i.ft_yta_point = (i.ftyta / point_value) if point_value else 0
				i.achieved_point=(i.f_achieved/point_value) if point_value else 0
				i.sr=(achieved_value/i.cr_ft)*100 if i.cr_ft else 0
				doc.save(ignore_permissions=True)
				frappe.db.commit() 
		
	return 'OK'