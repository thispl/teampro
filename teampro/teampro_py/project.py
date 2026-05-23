import frappe

@frappe.whitelist()
def update_profile_submission(name=None,date=None,count=None,task=None):
    task=frappe.get_doc("Task",task)
    task.append("custom_project_plan_",{
        "date":date,
        "count":count
    })
    task.save()


@frappe.whitelist()
def project_sa_candidate(project):
    allocated = frappe.db.sql("""
        SELECT sa_agent,sa_agent_name,sa_mobile_number,count(sa_agent) as achieved_count,
        (SELECT COUNT(pending_for) as count1 FROM `tabCandidate` cc WHERE cc.project= '%s' AND cc.pending_for = 'IDB' AND 
        cc.sa_agent = sa.name) as selected,
        (SELECT COUNT(pending_for) as count2 FROM `tabCandidate` cfp WHERE cfp.project= '%s' AND cfp.pending_for IN ('Submitted','Interviewed') AND
        cfp.sa_agent = sa.name) as fp,
        (SELECT COUNT(pending_for) as count3 FROM `tabCandidate` csl WHERE csl.project= '%s' AND csl.pending_for IN ('Linedup','Shortlisted') AND
        csl.sa_agent = sa.name) as sl,
        (SELECT COUNT(pending_for) as count4 FROM `tabCandidate` cpsl WHERE cpsl.project= '%s' AND  cpsl.pending_for ='Proposed PSL' AND 
        cpsl.sa_agent = sa.name) as psl,
        (SELECT COUNT(pending_for) as count5 FROM `tabCandidate` csp WHERE csp.project= '%s' AND csp.pending_for ='Sourced' AND 
        csp.sa_agent = sa.name) as sp,
        (SELECT COUNT(pending_for) as count6 FROM `tabCandidate` tsa WHERE tsa.project= '%s' AND tsa.pending_for IN ('Submitted','Interviewed','Linedup','Shortlisted','IDB','Proposed PSL','Sourced') AND 
        tsa.sa_agent = sa.name) as tsa
        FROM `tabCandidate` c 
        JOIN `tabSAMS` sa ON  sa.name = c.sa_agent 
        WHERE c.project='%s'AND c.sa_agent IS NOT NULL AND c.project IS NOT NULL GROUP BY sa.name
        """ %(project,project,project,project,project,project,project),as_dict=1)
    return(allocated)

@frappe.whitelist()
def count_task(project):
    task = frappe.db.count('Task',{'project':project,'status':('in',["Open","Working","Overdue","Pending Review"])})
    count_vac = frappe.db.sql("""
        SELECT SUM(vac) AS total_vac
        FROM `tabTask`
        WHERE project = %s
        AND status IN ('Open', 'Working', 'Pending Review', 'Overdue')
    """, (project,), as_dict=True)
    count = frappe.db.sql("""
        SELECT SUM(sp) AS total_sp, SUM(fp) AS total_fp, SUM(sl) AS total_sl, SUM(psl) AS total_psl
        FROM `tabTask`
        WHERE project = %s
        AND status IN ('Open', 'Working', 'Pending Review', 'Overdue', 'Completed')
    """, (project,), as_dict=True)
    return task, count_vac, count


@frappe.whitelist()
def task_count(project):
    task_it = frappe.db.count('Task',{'project':project})
    work_it = frappe.db.count('Task',{'project':project,"status":"Working"})
    pending_it = frappe.db.count('Task',{'project':project,"status":"Pending Review"})
    comp_it = frappe.db.count('Task',{'project':project,"status":"Completed"})
    open_it = frappe.db.count('Task',{'project':project,"status":"Open"})
    overdue_it = frappe.db.count('Task',{'project':project,"status":"Overdue"})
    return task_it,work_it,pending_it,comp_it,open_it,overdue_it
