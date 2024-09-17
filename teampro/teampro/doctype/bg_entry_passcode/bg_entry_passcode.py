# Copyright (c) 2024, TeamPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BGEntryPasscode(Document):
	pass
@frappe.whitelist()
def val_bg_pass(email_id):
    if frappe.db.exists("BG Entry Passcode",{"email_id":email_id}):
        return "No"
    
@frappe.whitelist()
def passcode(email_id,name):
    import string
    import random
    all_characters = string.ascii_letters + string.digits
    length = 6
    password = ''.join(random.choices(all_characters, k=length))
    link='https://erp.teamproit.com/bg-entry-form/new'
    passcode=password
    frappe.sendmail(
        # recipients=['giftyannie6@gmail.com'],
        recipients=[email_id],
        subject=_("Passcode"),
        message="""
            Dear %s,<br>Kindly Find the below attached Link to fill BG Form using the given Passcode,<br> Url: %s<br>Email ID: %s <br>Passcode: %s<br>
            Thanks & Regards,<br>TEAM ERP<br>"This email has been automatically generated. Please do not reply"
            """%(name,link,email_id,passcode)
        )
    return password