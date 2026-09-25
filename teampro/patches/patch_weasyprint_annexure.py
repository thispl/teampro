"""
Patch PrintFormatGenerator.render_pdf to:
1. Round header/footer heights to avoid WeasyPrint float-precision clipping bug
2. Handle pages without a body in overlay application
3. Rewrite relative image src URLs to local file paths for WeasyPrint
4. Append annexure pages
5. Reserve @page margins for the fixed header/footer in browser print preview,
   so the letterhead does not overlap document content
Applied at module import time via teampro __init__.py
"""
import os
import re
import frappe
from frappe.utils.weasyprint import PrintFormatGenerator

_original_render_pdf = PrintFormatGenerator.render_pdf
_original_get_main_html = PrintFormatGenerator.get_main_html
_original_make_header_footer = PrintFormatGenerator._make_header_footer
_original_apply_overlay_on_main = PrintFormatGenerator._apply_overlay_on_main
_original_get_html_preview = PrintFormatGenerator.get_html_preview
_original_get_header_footer_html = PrintFormatGenerator.get_header_footer_html
_patch_applied = False


def _rewrite_image_src(html):
	"""Rewrite Frappe /private/files and /files image URLs to local file paths.

	WeasyPrint cannot authenticate for /private/files URLs. Map them to the
	bench site file system so images in Quill editor content render in PDFs.
	"""
	site_path = os.path.abspath(frappe.get_site_path())

	def _replace(match):
		attr = match.group(1)
		src = match.group(2)
		# Strip query strings (?fid=...)
		clean = src.split("?")[0]
		if clean.startswith("/private/files/"):
			rel = clean[len("/private/files/"):]
			file_path = os.path.join(site_path, "private", "files", rel)
		elif clean.startswith("/files/"):
			rel = clean[len("/files/"):]
			file_path = os.path.join(site_path, "public", "files", rel)
		else:
			return match.group(0)
		if os.path.exists(file_path):
			return f'{attr}="file://{file_path}"'
		return match.group(0)

	return re.sub(r'(src)="([^"]+)"', _replace, html)


def _get_main_html_local_images(self):
	html = _original_get_main_html(self)
	return _rewrite_image_src(html)


def _make_header_footer_rounded(self):
	"""Wrap _make_header_footer to round header/footer heights.

	WeasyPrint has a bug where high-precision float values in @page padding
	(e.g. 153.02913475610305px) cause content to be clipped instead of
	flowing to new pages. Rounding to integers fixes this.
	"""
	_original_make_header_footer(self)
	self.header_height = round(self.header_height) if self.header_height else 0
	self.footer_height = round(self.footer_height) if self.footer_height else 0


_OVERLAY_IMG_STYLE = (
	"<style>"
	# full-bleed letterhead: fixed header/footer span the whole page width and
	# the letterhead <img> (which has no width attr) scales to fill it.
	# Without this, WeasyPrint renders the image at its natural pixel size,
	# blowing the header up to hundreds of mm and clipping it at the page edge.
	"header, footer { width: 100% !important; box-sizing: border-box !important;"
	" padding: 0 !important; margin: 0 !important; }"
	"header img, footer img { width: 100% !important; height: auto !important;"
	" display: block !important; }"
	"</style>"
)


def _get_header_footer_html_scaled(self):
	"""Inject image-scaling CSS into the standalone header/footer documents.

	WeasyPrint renders header_html/footer_html on their own to build the
	repeating overlay, so print-format CSS (which only lives in the main doc)
	never applies there.
	"""
	header_html, footer_html = _original_get_header_footer_html(self)
	if header_html:
		header_html = _OVERLAY_IMG_STYLE + header_html
	if footer_html:
		footer_html = _OVERLAY_IMG_STYLE + footer_html
	return header_html, footer_html


def _apply_overlay_on_main_safe(self, main_doc, header_body=None, footer_body=None):
	"""Wrap _apply_overlay_on_main to skip pages without a body element.

	When content flows across pages, some overflow pages may not contain the
	body element. The original method crashes with AttributeError on those.
	"""
	for page in main_doc.pages:
		page_body = PrintFormatGenerator.get_element(page._page_box.all_children(), "body")
		if page_body is None:
			continue
		if header_body:
			page_body.children += header_body.all_children()
		if footer_body:
			page_body.children += footer_body.all_children()


def _get_html_preview_static_header_footer(self):
	"""Render header/footer in normal flow for paged print media.

	get_html_preview feeds the printview page. The <header>/<footer> elements
	are marked position:fixed under @media print so they repeat on every page.
	That only works in WeasyPrint, where @page padding reserves space for them.
	Browsers and wkhtmltopdf reserve no space, so the fixed letterhead overlaps
	the document body. Rendering them in normal flow (like standard print
	formats) puts the letterhead at the top of the document and the footer at
	the end, with no overlap in any print engine.
	"""
	html = _original_get_html_preview(self)
	ml, mr = _body_side_padding_mm(self.print_format)
	fix = (
		"<style>"
		"@page { size: A4; margin: 0; }"
		"@media print {"
		"html, body { height: auto !important; min-height: 0 !important; }"
		"body { padding-left: 0 !important; padding-right: 0 !important; }"
		"header, footer { position: static !important; top: auto !important;"
		" bottom: auto !important; left: auto !important;"
		" width: 100% !important; margin: 0 !important; padding: 0 !important; }"
		".section { padding-left: " + str(ml) + "mm !important;"
		" padding-right: " + str(mr) + "mm !important; }"
		"}</style>"
	)
	return html.replace("</head>", fix + "</head>", 1)


def _body_side_padding_mm(print_format):
	"""Return (left, right) body padding in mm for a print format.

	Our modern formats put the side padding in their custom CSS
	(`body { padding-left: 15mm; }`) rather than the margin fields.
	"""
	css = print_format.css or ""
	left = right = 0.0
	for m in re.finditer(r"body[^{]*\{([^}]*)\}", css):
		block = m.group(1)
		pl = re.search(r"padding-left\s*:\s*([\d.]+)\s*mm", block)
		pr = re.search(r"padding-right\s*:\s*([\d.]+)\s*mm", block)
		if pl or pr:
			if pl:
				left = float(pl.group(1))
			if pr:
				right = float(pr.group(1))
			break
	if not left:
		left = float(print_format.margin_left or 0)
	if not right:
		right = float(print_format.margin_right or 0)
	return left, right


def _render_pdf_with_annexure(self):
	pdf_bytes = _original_render_pdf(self)

	# Only process docs with annexure field
	if hasattr(self.doc, "annexure") and self.doc.annexure:
		try:
			from teampro.annexure_print import append_annexure_to_pdf
			pdf_bytes = append_annexure_to_pdf(pdf_bytes, self.doc)
		except Exception as e:
			frappe.log_error(f"Annexure append failed: {e}")

	return pdf_bytes


def apply_patch():
	global _patch_applied
	if not _patch_applied:
		PrintFormatGenerator._make_header_footer = _make_header_footer_rounded
		PrintFormatGenerator._apply_overlay_on_main = _apply_overlay_on_main_safe
		PrintFormatGenerator.get_main_html = _get_main_html_local_images
		PrintFormatGenerator.render_pdf = _render_pdf_with_annexure
		PrintFormatGenerator.get_html_preview = _get_html_preview_static_header_footer
		PrintFormatGenerator.get_header_footer_html = _get_header_footer_html_scaled
		_patch_applied = True


# Apply patch immediately when module is imported
apply_patch()
