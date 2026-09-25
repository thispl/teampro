"""pdf_generator hook for builder-beta (WeasyPrint) print formats.

frappe.utils.print_utils.get_print routes any pdf_generator other than
"wkhtmltopdf" through the `pdf_generator` hook. This handler produces the
PDF via PrintFormatGenerator.render_pdf so that "Get PDF" / PDF download
links on the printview page return the same WeasyPrint output as the
Modern Print button, including letterhead overlays and annexures.
"""
import frappe


def weasyprint_pdf_generator(print_format, html, options, output, pdf_generator=None, **kwargs):
	if pdf_generator != "weasyprint":
		return

	from frappe.utils.weasyprint import PrintFormatGenerator

	doc = frappe.get_doc(frappe.form_dict.doctype, frappe.form_dict.name)
	letterhead = frappe.form_dict.get("letterhead") or None
	if letterhead in ("No Letterhead", "0"):
		letterhead = None

	generator = PrintFormatGenerator(print_format, doc, letterhead)
	pdf = generator.render_pdf()

	if output is not None:
		from io import BytesIO

		from pypdf import PdfReader

		reader = PdfReader(BytesIO(pdf))
		for page in reader.pages:
			output.add_page(page)
		return output

	return pdf
