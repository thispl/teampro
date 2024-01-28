# Copyright (c) 2023, TeamPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils import money_in_words
from frappe.model.document import Document

class CustomerPayment(Document):
	def validate(self):
		self.in_words = money_in_words(self.payment_received)
