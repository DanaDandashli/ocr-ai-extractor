import os

from extractors.pdf_extractor import extract_text_from_pdf
from extractors.image_extractor import extract_text_from_image
from extractors.docx_extractor import extract_text_from_docx
from extractors.excel_extractor import extract_text_from_excel
from extractors.html_extractor import extract_text_from_html
from extractors.text_extractor import extract_text_from_txt
from extractors.xml_extractor import extract_text_from_xml
from extractors.email_extractor import extract_text_from_email


"""
    Smart router that detects file type and calls correct extractor.
    Returns clean extracted text.
"""


def extract_file(file_path: str, lang: str = "eng") -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path, lang=lang)

    elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
        return extract_text_from_image(file_path, lang=lang)

    elif ext == ".docx":
        return extract_text_from_docx(file_path)

    elif ext in [".xlsx", ".xls"]:
        return extract_text_from_excel(file_path)

    elif ext == ".html" or ext == ".htm":
        return extract_text_from_html(file_path)

    elif ext == ".txt":
        return extract_text_from_txt(file_path)

    elif ext == ".xml":
        return extract_text_from_xml(file_path)

    elif ext == ".eml":
        return extract_text_from_email(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
