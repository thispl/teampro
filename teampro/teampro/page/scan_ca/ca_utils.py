import frappe
from frappe.utils import get_url
from frappe import _

@frappe.whitelist()
def get_qr_details():
    candidate = frappe.get_all(
        "Candidate",
        fields=["given_name", "name", "pending_for"]
    )

    if candidate:
        return candidate[0]
    else:
        return {}

@frappe.whitelist()
def validation_scan_qr(result):
    
    candidate_exists = frappe.db.exists('Candidate', {'name': result})
    if not candidate_exists:
        return {
            'error': _('Invalid Candidate ID')
        }

   
    candidate = frappe.db.get_value(
        'Candidate',
        {'name': result},
        ['given_name', 'name'],
        as_dict=True
    )

    if candidate:
        given_name = candidate.get('given_name')
        candidate_id = candidate.get('name')

        
        # print_format = 'IAF Form'

        
        # print_format_url = get_url(
        #     f"/api/method/frappe.utils.print_format.download_pdf"
        #     f"?doctype=Candidate&name={candidate_id}&trigger_print=1&format={print_format}&no_letterhead=0"
        # )

        
        link_format_url = get_url(
            f"/app/candidate/{candidate_id}"
        )

        return {
            'candidate_name': given_name,
            'candidate_id': candidate_id,
            # 'print_format_url': print_format_url,
            'link_format_url': link_format_url
        }
    else:
        return {
            'error': _('Candidate details not found or access denied.')
        }
