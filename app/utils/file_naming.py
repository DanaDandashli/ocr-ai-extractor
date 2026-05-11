from datetime import datetime


def generate_filename(invoice_data, extension: str):

    invoice_number = invoice_data.get("invoice_number", "unknown")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"invoice_{invoice_number}_{timestamp}.{extension}"

    return filename
