import os
from dotenv import load_dotenv
from PIL import Image
import pytesseract


load_dotenv()
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

"""
    This function extract text from image using OCR (Tesseract).
    Supports: PNG, JPG, JPEG

    Supported languages depend on installed Tesseract language packs.
    Example:
    - eng = English
    - ara = Arabic
    - fra = French
"""


def extract_text_from_image(file_path: str, lang: str = "eng") -> str:
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()
