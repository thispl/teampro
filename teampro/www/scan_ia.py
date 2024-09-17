import frappe

@frappe.whitelist()
def get_candidate_info(qr_code):
    # Example: Search for candidate by ID or another identifier
    candidate = frappe.get_all("Candidate", filters={"identifier_field": qr_code}, fields=["name", "given_name", "status"])
    
    if candidate:
        return candidate[0]  # Assuming qr_code maps to one candidate
    return None
