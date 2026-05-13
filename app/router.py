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
Smart router:
- Detects file type
- Extracts raw content
- Applies STRICT OCR validation
- Sends valid data to LLM
"""


# OCR Validation Gate (STRICT)
def invoice_quality_score(inv: dict) -> float:
    score = 0

    # critical fields
    if inv.get("invoice_number"):
        score += 2
    if inv.get("date"):
        score += 1
    if inv.get("vendor_name"):
        score += 1
    if inv.get("customer_name"):
        score += 1

    # items quality
    items = inv.get("items", [])
    if isinstance(items, list) and len(items) > 0:
        score += 1

    # financial validity
    if float(inv.get("total") or 0) > 0:
        score += 1

    return score


def validate_final_invoice(result: dict):
    """
    Ensures extracted invoice is meaningful, not empty hallucination.
    """
    
    if not isinstance(result, dict):
        return {
            "success": False,
            "stage": "final_validation",
            "error_code": "INVALID_RESULT_TYPE",
            "message": "Internal error: invalid extraction result."
        }

    score = invoice_quality_score(result)
    if score < 5:
        return {
            "success": False,
            "stage": "validation",
            "error_code": "LOW_CONFIDENCE_EXTRACTION",
            "message": "The document quality is too low to reliably extract invoice data.\nUpload a clear invoice..."
        }
    
    return None


def extract_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    # Vision Pipeline
    if ext == ".pdf":
        result = extract_invoice_from_pdf(file_path)

        # Pass through extractor errors directly
        if isinstance(result, list) and result.get("success") is False:
            return result

        if isinstance(result, dict) and "pages" in result:
            return result
        
        error = validate_final_invoice(result)
        if error:
            return error

        return result

    elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
        result = extract_invoice_from_image(file_path)
        error = validate_final_invoice(result)
        if error:
            return error

        return result

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
