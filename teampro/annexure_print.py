import frappe
import os
from io import BytesIO


def append_annexure_to_pdf(pdf_bytes, doc):
    """
    Append annexure file (PDF or image) as additional pages after the invoice.
    """
    annexure_url = getattr(doc, "annexure", None)
    if not annexure_url:
        return pdf_bytes

    # Resolve file path - try File doc first, then direct path
    file_path = _resolve_file_path(annexure_url)
    if not file_path or not os.path.exists(file_path):
        return pdf_bytes

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _merge_pdf(pdf_bytes, file_path)
    elif ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
        return _merge_image_pdf(pdf_bytes, file_path, annexure_url)
    else:
        return pdf_bytes


def _resolve_file_path(file_url):
    """Resolve file URL to absolute path."""
    # Try via File doc
    try:
        file_doc = frappe.get_doc("File", {"file_url": file_url})
        path = file_doc.get_full_path()
        if os.path.exists(path):
            return path
    except Exception:
        pass

    # Try direct path resolution
    try:
        if file_url.startswith("/private/files/"):
            return frappe.get_site_path("private", "files", os.path.basename(file_url))
        elif file_url.startswith("/files/"):
            return frappe.get_site_path("public", "files", os.path.basename(file_url))
        elif file_url.startswith("/protected/"):
            return frappe.get_site_path("protected", "files", os.path.basename(file_url))
    except Exception:
        pass

    return None


def _merge_pdf(invoice_pdf_bytes, annexure_path):
    """Merge invoice PDF with annexure PDF using pypdf."""
    try:
        from pypdf import PdfReader, PdfWriter

        writer = PdfWriter()

        # Add invoice pages
        invoice_reader = PdfReader(BytesIO(invoice_pdf_bytes))
        for page in invoice_reader.pages:
            writer.add_page(page)

        # Add annexure pages
        annexure_reader = PdfReader(annexure_path)
        for page in annexure_reader.pages:
            writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        return output.getvalue()
    except Exception as e:
        frappe.log_error(f"Annexure PDF merge failed: {e}")
        return invoice_pdf_bytes


def _merge_image_pdf(invoice_pdf_bytes, image_path, file_url):
    """Convert image to PDF page and merge with invoice PDF."""
    try:
        from pypdf import PdfReader, PdfWriter
        from weasyprint import HTML
        import pathlib

        # Resolve to absolute path before converting to URI
        abs_path = os.path.abspath(image_path)
        file_uri = pathlib.Path(abs_path).as_uri()

        html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin: 0; padding: 0;">
<img src="{file_uri}" style="width: 210mm; height: 297mm; object-fit: contain;" />
</body>
</html>"""

        image_pdf = HTML(string=html_content).write_pdf()

        # Merge
        writer = PdfWriter()
        invoice_reader = PdfReader(BytesIO(invoice_pdf_bytes))
        for page in invoice_reader.pages:
            writer.add_page(page)

        image_reader = PdfReader(BytesIO(image_pdf))
        for page in image_reader.pages:
            writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        return output.getvalue()
    except Exception as e:
        frappe.log_error(f"Annexure image merge failed: {e}")
        return invoice_pdf_bytes
