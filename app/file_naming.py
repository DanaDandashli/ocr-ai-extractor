from datetime import datetime


def generate_filename(data: dict, extension: str) -> str:
    doc_type = data.get("document_type", "document")
    invoice_number = data.get("invoice_number", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if invoice_number:
        return f"{doc_type}_{invoice_number}_{timestamp}.{extension}"
    return f"{doc_type}_{timestamp}.{extension}"
