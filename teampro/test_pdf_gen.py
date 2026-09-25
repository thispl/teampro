
import frappe
from frappe.utils.pdf import get_pdf

def test():
    result = frappe.call(
        frappe.get_attr("teampro.utility.get_party_statement"),
        party_type="Customer",
        party="Badhrinath Surgicals",
        from_date="2020-09-01",
        to_date="2020-09-30",
        company="TEAMPRO General Trading"
    )
    html = result["html"]
    options = {
        "page-size": "A4",
        "margin-top": "15mm",
        "margin-bottom": "15mm",
        "margin-left": "12mm",
        "margin-right": "12mm",
        "encoding": "UTF-8",
        "enable-local-file-access": "",
        "print-media-type": "",
    }
    pdf = get_pdf(html, options=options)
    print("PDF generated, size:", len(pdf), "bytes")
    with open("/tmp/test_statement2.pdf", "wb") as f:
        f.write(pdf)
    print("Saved to /tmp/test_statement2.pdf")
