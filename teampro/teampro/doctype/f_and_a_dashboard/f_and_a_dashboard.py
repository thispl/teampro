# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FandADashboard(Document):
	pass

@frappe.whitelist()
def bcs_report():
	data = '<table border="1" style="border-collapse: collapse; width: 100%;">'
	data += '<tr style="background-color: #002060; color: white;">' \
			'<td style="text-align:center; font-weight:bold; color:white;">Customer</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">Batch</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">#Cases</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">0 to 5</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">5 to 10</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">10 to 15</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">15+</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">#Insuff</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">#Data Entry</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">#Execution</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">#Completed</td>' \
			'</tr>'
	batch=frappe.db.get_all("Batch",{"batch_status":"Open"},["*"])
	for i in batch:
		no_of_cases=frappe.db.count("Case",{"batch":i.name})
		age_0_to_5=frappe.db.count("Case",{"batch":i.name,"actual_tat":("between",[0,5])})
		age_5_to_10=frappe.db.count("Case",{"batch":i.name,"actual_tat":("between",[5,10])})
		age_10_to_15=frappe.db.count("Case",{"batch":i.name,"actual_tat":("between",[10,15])})
		age_15_above=frappe.db.count("Case",{"batch":i.name,"actual_tat":(">",15)})
		no_of_insuff=frappe.db.count("Case",{"batch":i.name,"case_status":("in",["Entry-Insuff","Execution-Insuff"])})
		no_of_entry=frappe.db.count("Case",{"batch":i.name,"case_status":("in",["Draft","Entry Completed","Entry-QC"])})
		no_of_exe=frappe.db.count("Case",{"batch":i.name,"case_status":("in",["Execution"])})
		no_of_comp=frappe.db.count("Case",{"batch":i.name,"case_status":("in",["To be Billed","SO Created"])})
		data += f'<tr>' \
			f'<td style="text-align:center;">{i.customer}</td>' \
			f'<td style="text-align:center;">{i.name}</td>' \
			f'<td style="text-align:center;">{no_of_cases}</td>' \
			f'<td style="text-align:center;">{age_0_to_5}</td>' \
			f'<td style="text-align:center;">{age_5_to_10}</td>' \
			f'<td style="text-align:center;">{age_10_to_15}</td>' \
			f'<td style="text-align:center;">{age_15_above}</td>' \
			f'<td style="text-align:center;">{no_of_insuff}</td>' \
			f'<td style="text-align:center;">{no_of_entry}</td>' \
			f'<td style="text-align:center;">{no_of_exe}</td>' \
			f'<td style="text-align:center;">{no_of_comp}</td>' \
			'</tr>'
	data += '</table>'
	return data

@frappe.whitelist()
def tfp_report():
	data = '<table border="1" style="border-collapse: collapse; width: 100%;">'
	data += '<tr style="background-color: #002060; color: white;">' \
			'<td style="text-align:center; font-weight:bold; color:white;">Customer</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">SI</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">#Kg</td>' \
			'<td style="text-align:center; font-weight:bold; color:white;">#Package</td>' \
			'</tr>'
	sales_invoice=frappe.db.get_all("Sales Invoice",{"services":"TFP"},["*"],order_by= "posting_date DESC")
	for i in sales_invoice:
		doc = frappe.get_doc("Sales Invoice", i.name)
		total_qty = 0
		total_stock_qty = 0
		if doc.items:
			for item in doc.items:
				total_qty += item.qty
				total_stock_qty += item.stock_qty
			data += f'<tr>' \
                f'<td style="text-align:center;">{i["customer"]}</td>' \
                f'<td style="text-align:center;">{i["name"]}</td>' \
                f'<td style="text-align:center;">{round(total_stock_qty,1)}</td>' \
                f'<td style="text-align:center;">{total_qty}</td>' \
                '</tr>'
	data += '</table>'
	return data