
import frappe
from frappe.utils.pdf import get_pdf

def test():
    result = frappe.call(
        frappe.get_attr("teampro.utility.get_party_statement"),
        party_type="Supplier",
        party="JPM Snacks",
        from_date="2026-04-01",
        to_date="2027-03-31",
        company="TEAMPRO Food Products"
    )
    html = result["html"]
    options = {
        "page-size": "A4",
        "margin-top": "15mm",
        "margin-bottom": "20mm",
        "margin-left": "12mm",
        "margin-right": "12mm",
        "encoding": "UTF-8",
        "enable-local-file-access": "",
        "print-media-type": "",
        "footer-center": "Page [page] of [topage]",
        "footer-font-size": "8",
        "footer-spacing": "5",
    }
    pdf = get_pdf(html, options=options)
    with open("/tmp/statement_test.pdf", "wb") as f:
        f.write(pdf)
    print("PDF saved, size:", len(pdf))
