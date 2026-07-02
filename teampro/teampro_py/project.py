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

@frappe.whitelist()
def update_project_count_cron():
    project=frappe.get_all("Project",{'status':'Open','service':('in',['REC-D','REC-I'])},['*'])
    for doc in project:
        if doc.name:
            tot_fp=frappe.db.sql("""SELECT sum(fp) as fp from `tabTask` where project=%s """,(doc.name),as_dict=True)[0]
            tot_psl=frappe.db.sql("""SELECT sum(psl) as psl from `tabTask` where project=%s """,(doc.name),as_dict=True)[0]
            tot_sl=frappe.db.sql("""SELECT sum(sl) as sl from `tabTask` where project=%s """,(doc.name),as_dict=True)[0]
            tot_sp=frappe.db.sql("""SELECT sum(sp) as sp from `tabTask` where project=%s """,(doc.name),as_dict=True)[0]
            tot_lp=frappe.db.sql("""SELECT sum(custom_lp) as lp from `tabTask` where project=%s""",(doc.name),as_dict=True)[0]
            tot_rp=frappe.db.sql("""SELECT sum(custom_rp) as rp from `tabTask` where project=%s""",(doc.name),as_dict=True)[0]
            if tot_fp['fp'] is not None:
                frappe.db.set_value("Project",doc.name,'tfp',tot_fp['fp'])
            if tot_psl['psl'] is not None:
                frappe.db.set_value("Project",doc.name,'tpsl',tot_psl['psl'])
            if tot_sl['sl'] is not None:
                frappe.db.set_value("Project",doc.name,'tsl',tot_sl['sl'])
            if tot_sp['sp'] is not None:
                frappe.db.set_value("Project",doc.name,'tsp',tot_sp['sp'])
            if tot_lp['lp'] is not None:
                frappe.db.set_value("Project",doc.name,'custom_t_lp',tot_lp['lp'])
            if tot_rp['rp'] is not None:
                frappe.db.set_value("Project",doc.name,'custom_t_rp',tot_rp['rp'])


@frappe.whitelist()
def update_proj_positions_count():
    frappe.enqueue(
        update_project_count_cron,
        queue="long",
        timeout=36000,
        is_async=True,
        now=False,
        job_name='Project Update',
        enqueue_after_commit=False,
    )
    
@frappe.whitelist()
def update_proj_positions_count_hourly():
    frappe.enqueue(
        update_project_count_cron,
        queue="long",
        timeout=36000,
        is_async=True,
        now=False,
        job_name='Project Update',
        enqueue_after_commit=False,
    )


@frappe.whitelist()
def update_proj_position_value():
    frappe.enqueue(
        update_count_proj,
        queue="long",
        timeout=36000,
        is_async=True,
        now=False,
        job_name=f"Project Update",
        enqueue_after_commit=True,
    )


@frappe.whitelist()
def update_count_proj():
    projects = frappe.get_all(
        "Project",
        filters={"status": ["in", ["Open", "Enquiry", "Draft", "Kick OFF", "Working", "Overdue"]],"service":"REC-I"},
        pluck="name",  
    )
    # projects = ["PROJ-1869"]
    for project_name in projects:
        project_doc = frappe.get_doc("Project", project_name)

        if not project_doc.custom_profile_submission:
            continue  
        task_rows = {}
        for row in project_doc.custom_profile_submission:
            task_rows.setdefault(row.task, []).append(row)

        for task, rows in task_rows.items():
            rows.sort(key=lambda x: x.date)
            previous_date = None

            for row in rows:
                current_date = row.date

                candidate_count = frappe.db.sql("""
                    SELECT COUNT(DISTINCT c.name)
                    FROM `tabCandidate` c
                    WHERE c.task = %s
                    AND c.project = %s
                    AND c.pending_for IN ('Submit(SPOC)','Submitted(Client)','Interviewed')
                """, (task, project_doc.name))[0][0]

                if previous_date:
                    candidate_achieved_count = frappe.db.sql("""
                        SELECT COUNT(DISTINCT c.name)
                        FROM `tabCandidate` c
                        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                        WHERE DATE(cs.sourced_date) > %s
                        AND DATE(cs.sourced_date) <= %s
                        AND cs.task = %s
                        AND cs.project = %s
                        AND cs.status = 'Submit(SPOC)'
                    """, (previous_date, current_date, task, project_doc.name))[0][0]
                else:
                    candidate_achieved_count = frappe.db.sql("""
                        SELECT COUNT(DISTINCT c.name)
                        FROM `tabCandidate` c
                        INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                        WHERE DATE(cs.sourced_date) <= %s
                        AND cs.task = %s
                        AND cs.project = %s
                        AND cs.status = 'Submit(SPOC)'
                    """, (current_date, task, project_doc.name))[0][0]
                # print(candidate_achieved_count)
                

                row.achieved = candidate_achieved_count or 0
                previous_date = current_date

        project_doc.save(ignore_permissions=True)

    frappe.db.commit()

@frappe.whitelist() 
def update_project_count(doc,method):
    if doc.project and doc.service in ['REC-D','REC-I']:
        tot_fp=frappe.db.sql("""SELECT sum(fp) as fp from `tabTask` where project=%s """,(doc.project),as_dict=True)[0]
        tot_psl=frappe.db.sql("""SELECT sum(psl) as psl from `tabTask` where project=%s """,(doc.project),as_dict=True)[0]
        tot_sl=frappe.db.sql("""SELECT sum(sl) as sl from `tabTask` where project=%s """,(doc.project),as_dict=True)[0]
        tot_sp=frappe.db.sql("""SELECT sum(sp) as sp from `tabTask` where project=%s """,(doc.project),as_dict=True)[0]
        tot_lp=frappe.db.sql("""SELECT sum(custom_lp) as lp from `tabTask` where project=%s""",(doc.project),as_dict=True)[0]
        tot_rp=frappe.db.sql("""SELECT sum(custom_rp) as rp from `tabTask` where project=%s""",(doc.project),as_dict=True)[0]
        tot_vac=frappe.db.sql("""SELECT sum(vac) as vac from `tabTask` where project=%s""",(doc.project),as_dict=True)[0]
        if tot_fp['fp'] is not None:
            frappe.db.set_value("Project",doc.project,'tfp',tot_fp['fp'])
        if tot_psl['psl'] is not None:
            frappe.db.set_value("Project",doc.project,'tpsl',tot_psl['psl'])
        if tot_sl['sl'] is not None:
            frappe.db.set_value("Project",doc.project,'tsl',tot_sl['sl'])
        if tot_sp['sp'] is not None:
            frappe.db.set_value("Project",doc.project,'tsp',tot_sp['sp'])
        if tot_lp['lp'] is not None:
            frappe.db.set_value("Project",doc.project,'custom_t_lp',tot_lp['lp'])  
        if tot_rp['rp'] is not None:
            frappe.db.set_value("Project",doc.project,'custom_t_rp',tot_rp['rp'])              
        if tot_vac['vac'] is not None:
            frappe.db.set_value("Project",doc.project,'tvac',tot_vac['vac'])              
        # frappe.db.set_value("Project", doc.project, 'tfp', tot_fp[0].get('fp', 0))
        # frappe.db.set_value("Project", doc.project, 'tpsl', tot_psl[0].get('psl', 0))
        # frappe.db.set_value("Project", doc.project, 'tsl', tot_sl[0].get('sl', 0))
        # frappe.db.set_value("Project", doc.project, 'tsp', tot_sp[0].get('sp', 0))

@frappe.whitelist()
def update_sa_details_in_task(doc,method):
    if doc.name and doc.service=="REC-I":
        
        tasks = frappe.db.get_all("Task", filters={"project":doc.name}, fields=["name"])
        for task in tasks:
            task_doc = frappe.get_doc("Task", task["name"])
            existing_sa_ids = {i.sa_id for i in task_doc.sa_detail}
            for row in doc.custom_sa_details:
                if row.sa_id not in existing_sa_ids:
                    task_doc.append(
                        "sa_detail",
                        {
                            "sa_id": row.sa_id,
                            "sa_name": row.sa_name,
                            "sa_contact_number": row.sa_contact_number,
                        },
                    )
          
            task_doc.save()
            frappe.db.commit()
            task_doc.reload()
      
import frappe

@frappe.whitelist()
def update_proj_position(doc, method=None):
    frappe.enqueue(
        update_fp_count_proj,
        queue="long",
        timeout=36000,
        is_async=True,
        now=False,
        job_name=f"Project Update {doc.name}",
        enqueue_after_commit=True,
        project_name=doc.name
    )

@frappe.whitelist()
def update_fp_count_proj(project_name):
    project_doc = frappe.get_doc("Project", project_name)
    if project_doc.service not in ['REC-D','REC-I']:
        return
    if not project_doc.custom_profile_submission:
        return "No profile submissions found"

    task_rows = {}
    for row in project_doc.custom_profile_submission:
        task_rows.setdefault(row.task, []).append(row)

    for task, rows in task_rows.items():
        rows.sort(key=lambda x: x.date)
        previous_date = None

        for row in rows:
            current_date = row.date
            candidate_count = frappe.db.sql("""
                SELECT COUNT(DISTINCT c.name)
                FROM `tabCandidate` c
                WHERE c.task = %s
                AND c.project = %s
                AND c.pending_for IN ('Submit(SPOC)','Submitted(Client)','Interviewed')
            """, (task, project_doc.name))[0][0]
            if previous_date:
                candidate_achieved_count = frappe.db.sql("""
                    SELECT COUNT(DISTINCT c.name)
                    FROM `tabCandidate` c
                    INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                    WHERE DATE(cs.sourced_date) > %s
                    AND DATE(cs.sourced_date) <= %s
                    AND cs.task = %s
                    AND cs.project = %s
                    AND cs.status = 'Submit(SPOC)'
                """, (previous_date, current_date, task, project_doc.name))[0][0]
            else:
                candidate_achieved_count = frappe.db.sql("""
                    SELECT COUNT(DISTINCT c.name)
                    FROM `tabCandidate` c
                    INNER JOIN `tabCandidate status` cs ON c.name = cs.parent
                    WHERE DATE(cs.sourced_date) <= %s
                    AND cs.task = %s
                    AND cs.project = %s
                    AND cs.status = 'Submit(SPOC)'
                """, (current_date, task, project_doc.name))[0][0]

            row.fp = candidate_count or 0
            row.achieved = candidate_achieved_count or 0
            previous_date = current_date
    return f"Project {project_name} FP counts updated"