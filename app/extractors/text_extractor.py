"""
    This function extract raw text from .txt files.
    Used for logs, OCR outputs, and simple documents.
"""


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text.strip()
