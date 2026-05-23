// Copyright (c) 2025, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Case", {
    setup(frm) {

        frm.set_query("package", function() {
            return {
                filters: {
                    customer: frm.doc.customer,
                }
            };
        });

    },
    refresh(frm) {

        if (frappe.user.has_role("Employee")) {

            frm.add_custom_button("Case", async () => {

                // 1️⃣ Check if case already linked
                let assigned = await frappe.db.get_list("Case", {
                    fields: ["name"],
                    filters: {
                        batch: frm.doc.batch,
                        check_package: frm.doc.package,
                        employee_case: frm.doc.name
                    },
                    limit: 1
                });

                if (assigned.length > 0) {
                    frappe.set_route("Form", "Case", assigned[0].name);
                    return;
                }

                // 2️⃣ Get next unassigned case
                let next_case = await frappe.db.get_list("Case", {
                    fields: ["name"],
                    filters: {
                        batch: frm.doc.batch,
                        check_package: frm.doc.package,
                        employee_case: ["=", ""]
                    },
                    order_by: "name asc",
                    limit: 1
                });

                if (next_case.length === 0) {
                    frappe.msgprint("No Case available.");
                    return;
                }

                let case_name = next_case[0].name;

                // 3️⃣ Fetch the case to modify in memory
                frappe.call({
                    method: "frappe.client.get",
                    args: { doctype: "Case", name: case_name },
                    callback: function (res) {
                        let case_doc = res.message;

                        // update in memory
                        let local_doc = frappe.model.sync(case_doc)[0];

                        // prefill fields (no save)
                        local_doc.employee_case = frm.doc.name;

                        // clear and fill child table
                        // local_doc.employee_case_details = [];
                        // frm.doc.employee_case_details.forEach(row => {
                        //     let child = frappe.model.add_child(local_doc, "employee_case_details");
                        //     child.title_of_attachment = row.title_of_attachment;
                        //     child.attach = row.attach;
                        // });

                        // 4️⃣ finally open the modified doc
                        frappe.set_route("Form", "Case", case_name);
                    }
                });

            });
        }
    }


});

