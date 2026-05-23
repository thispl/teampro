// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Follow Up Report"] = {
	"filters": [

		{
			'fieldname':"sfp_id",
			'label':__("ID"),
			'fieldtype':'Link',
			'options':"Sales Follow Up"
		},


		{
			'fieldname':"next_contact_by",
			'label':__("Next Contact By"),
			'fieldtype':'Link',
			'options':"User"
			
			
		},

		{
			'fieldname':"territory",
			'label':__("Territory"),
			'fieldtype':'Link',
			'options':"Territory"
			
			
		},


		{
			'fieldname':"has_whatsapp",
			'label':__("Has Whatsapp"),
			'fieldtype':'Check',
			'default':1
			
		},

		

	]
};
