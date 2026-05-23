import frappe
@frappe.whitelist()
def update_service_in_payment_entries(ref_doc,ref_name):
    if ref_doc=="Sales Order":
        if ref_doc and ref_name:
            reference_doc = frappe.get_doc(ref_doc, ref_name)
            if hasattr(reference_doc, 'service'):
                service_value = reference_doc.service
    elif ref_doc=="Sales Invoice":
        if ref_doc and ref_name:
            reference_doc = frappe.get_doc(ref_doc, ref_name)
            if hasattr(reference_doc, 'services'):
                service_value = reference_doc.services
    elif ref_doc=="Purchase Invoice":
        if ref_doc and ref_name:
            reference_doc = frappe.get_doc(ref_doc, ref_name)
            if hasattr(reference_doc, 'services'):
                service_value = reference_doc.services
    elif ref_doc=="Purchase Order":
        if ref_doc and ref_name:
            reference_doc = frappe.get_doc(ref_doc, ref_name)
            if hasattr(reference_doc, 'custom_service'):
                service_value = reference_doc.custom_service

    return service_value
