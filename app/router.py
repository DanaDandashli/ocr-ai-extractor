import os
from llm.invoice_extractor import extract_invoice_json, extract_invoice_from_pdf, extract_invoice_from_image
# from extractors.pdf_extractor import extract_text_from_pdf
# from extractors.image_extractor import extract_text_from_image
from extractors.docx_extractor import extract_text_from_docx
from extractors.excel_extractor import extract_text_from_excel
from extractors.html_extractor import extract_text_from_html
from extractors.text_extractor import extract_text_from_txt
from extractors.xml_extractor import extract_text_from_xml
from extractors.email_extractor import extract_text_from_email


"""
    Smart router that detects file type and calls correct extractor.
"""


def extract_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    # Vision Pipeline
    if ext == ".pdf":
        return extract_invoice_from_pdf(file_path)

    elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
        return extract_invoice_from_image(file_path)

    # Text Pipeline
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)

    elif ext in [".xlsx", ".xls"]:
        text = extract_text_from_excel(file_path)

    elif ext == ".html" or ext == ".htm":
        text = extract_text_from_html(file_path)

    elif ext == ".txt":
        text = extract_text_from_txt(file_path)

    elif ext == ".xml":
        text = extract_text_from_xml(file_path)

    elif ext == ".eml":
        text = extract_text_from_email(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    # Convert extracted text -> JSON
    return extract_invoice_json(text)
