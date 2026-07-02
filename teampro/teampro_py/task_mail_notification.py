import frappe
@frappe.whitelist()
def task_mail_notification():
    projects=frappe.get_all("Project",{'status':'Open','service':('in',['REC-D','REC-I'])},['*'])
    table = '<table text-align="center" border="1" width="100%" style="border-collapse: collapse;text-align: left;">'
    row=0
    for project in projects:
        tasks = frappe.get_all("Task", {'status': ('in', ['Open', 'Working','Overdue','Pending Review']),'project':project.name,'service':('in',['REC-D','REC-I'])},['*'])
        candidate_count=frappe.db.count("Candidate", {'project':project.name,'pending_for':('not in',['IDB','Sourced','Proposed PSL'])})
        if candidate_count>0:
            if row>0:
                table += """<tr><td style="border: none; border-left: hidden; border-right: hidden; height: 40px;" colspan=6></td></tr>"""
            # table+="""<tr><td style="border-left: hidden; border-right: hidden; border-top:hidden; border-bottom:hidden;"colspan=6></td></tr>"""
            table+="""<tr><td style="border-left: none; border-right: none;text-align: left;"colspan=2>Customer Name</td><td style="text-align: left;" colspan=4>%s</td></tr>"""%(project.customer)
            table+="""<tr><td style="border-left: none; border-right: none;text-align: left;"colspan=2>Spoc</td><td style="text-align: left;"colspan=4>%s</td></tr>"""%(project.spoc)
            table+="""<tr><td style="border-left: none; border-right: none;text-align: left;"colspan=2>Account Manager</td><td style="text-align: left;"colspan=4>%s</td></tr>"""%(project.account_manager)
            table += '<tr style="background-color: #0f1568"><td style="width: 2%; font-weight: bold;color: white;text-align: left;">ID</td><td style="width: 1%; font-weight: bold;color: white;text-align: left;">Status</td><td style="width: 5%; font-weight: bold; color: white;text-align: left;">Given Name</td><td style="width:3%; font-weight: bold; color: white;text-align: left;">Position</td><td style="width: 3%; font-weight: bold;color: white;text-align: left;">Passport Number</td><td style="width: 2%; font-weight: bold;color: white;text-align: left;">Project</td></tr>'
        for j in tasks:
            candidate=frappe.get_all("Candidate",{'pending_for':('not in',['IDB','Sourced','Proposed PSL']),'task':j.name},['name','pending_for','given_name','position','passport_number','project'])
            for ca in candidate:
                table+="""<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (ca.name,ca.pending_for,ca.given_name,ca.position,ca.passport_number or '-',ca.project)
                row+=1
    table += '</table>'
    frappe.sendmail(
        recipients=['sangeetha.a@groupteampro.com','lokeshkumar.a@groupteampro.com'],
        cc=['sangeetha.s@groupteampro.com','dineshbabu.k@groupteampro.com'],
        subject='Candidate Feedback Pending Report',
        message=f"""
        <br>
         <p>As per the mail, Profile feedback pending list.</p>
        
        
          {table}<br><br>
        "This email has been automatically generated. PLEASE DONOT REPLY, Initiate further action and intimate your direct manager through email."
            <br><br>
            "With Best Wishes & Regards "
            <br><br>
            <span style="color:#203ed5;">
            "TEN – Auto Mail "
            </span>
            <br><br>
            <span style="color:#203ed5;">
                "Disclaimers:<br>
                This email and any files transmitted with it are confidential and intended solely for the use of the individual or entity to whom they are addressed. If you have received this email in error please notify the system manager. Please note that any views or opinions presented in this email are solely those of the author and do not necessarily represent those of the company. Finally, the recipient should check this email and any attachments for the presence of viruses. The company accepts no liability for any damage caused by any virus transmitted by this email."
            </span>
        """
    )