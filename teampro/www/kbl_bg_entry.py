import frappe

@frappe.whitelist(allow_guest=True)
def new_kbl_bg(**args):
    frappe.log_error(message=f"Error :{args}",title=("BG Entry"))
    try:
		# if not frappe.db.exists('BG Entry Form',{'email_id':args['email']}):
        ec = frappe.new_doc('BG Entry Form')
        ec.employee_name = args['name']
        ec.gender = args['gender']
        ec.date_of_birth = args['dob']
        ec.email_id = args['email']
        ec.fathers_name = args['father']
        ec.address = str(args['address'])
        ec.contact_number = args['phone']
        ec.register_no_id_no = str(args['regno'])
        ec.college_name = str(args['cname'])
        ec.university_name = str(args['uname'])
        ec.degree = str(args['degree'])
        ec.specialization = str(args['special'])
        ec.course_period = args['courseperiod']
        ec.year_of_passed = args['yearofpass']
        ec.education_document_required = 'https://kbl.teamproit.com/'+args['degcert']
        ec.employment_check = args['employer']
        ec.address_and_contact_details = str(args['addandcont'])
        ec.experience = args['experience']
        if args['experience']=='Experienced':
            ec.employee_code = args['empcode']
            ec.employment_type = args['emptype']
            ec.emp_period = str(args['empperiod'])
            ec.designation = args['empdesig']
            ec.ctc_drawn = args['ctcdrawn']
            ec.documents_required = 'https://kbl.teamproit.com/'+args['appointment']
            ec.data_32 = str(args['reason'])
            ec.data_33 = args['ref1']
            ec.data_34 = args['cont1']
            ec.data_35 = str(args['des1'])
            ec.designation_2 = str(args['des2'])
            ec.reference_name_2 = args['ref2']
            ec.contact_2 = args['cont2']
        ec.criminal_check_address = str(args['address1'])
        ec.state_and_country = args['state']
        ec.city = args['city']
        ec.criminal_check_document_required = 'https://kbl.teamproit.com/'+args['aadhar']
        ec.document_required = 'https://kbl.teamproit.com/'+args['resume']
        ec.name_as_in_proof = args['name']
        ec.date_of_birth_as_in_proof = args['dob']
        ec.scanned_document_required = 'https://kbl.teamproit.com/'+args['aadhar']
        ec.father_name_as_in_proof = args['father']
        ec.customer = "KBL Services Limited"
        ec.save(ignore_permissions=True)

        frappe.db.commit()
        return True
    except Exception as e:
        frappe.log_error(f"Error :{str(e)}",("BG Entry Error"))
