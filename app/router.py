import os
from app.client import extract_from_text, extract_from_pdf, extract_from_image_group
from app.file_extractor import from_docx, from_excel, from_html, from_txt, from_xml, from_email
from app.handle_errors import make_error, validate_input, validate_output
from app.lookup import get_file_type, SUPPORTED_EXTENSIONS

TEXT_PIPELINE = {
    ".docx": from_docx,
    ".xlsx": from_excel,
    ".xls":  from_excel,
    ".html": from_html,
    ".htm":  from_html,
    ".txt":  from_txt,
    ".xml":  from_xml,
    ".eml":  from_email,
}


def extract_file(file_path: str) -> dict:
    ext = os.path.splitext(file_path)[1].lower()
    error = validate_input(file_path, ext)
    if error:
        return error

    file_type = get_file_type(ext)

    if file_type == "pdf":
        result = extract_from_pdf(file_path)
        if isinstance(result, dict) and result.get("success") is False:
            return result
        if isinstance(result, dict) and "pages" in result:
            error = validate_output(result)
            return error if error else result

    elif file_type == "image":
        result = extract_from_image_group([file_path])

    elif file_type == "text":
        extractor = TEXT_PIPELINE.get(ext)
        result = extract_from_text(extractor(file_path))

    else:
        supported = ", ".join(SUPPORTED_EXTENSIONS.keys())
        return make_error(
            "UNSUPPORTED_FILE_TYPE",
            f"Unsupported file type '{ext}'. Supported formats: {supported}."
        )

    if isinstance(result, dict) and result.get("success") is False:
        return result

    return validate_output(result) or result
