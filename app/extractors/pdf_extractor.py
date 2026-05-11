import os, fitz
from dotenv import load_dotenv
from PIL import Image
import pytesseract


load_dotenv()
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


"""
    This function extract text from PDF using PyMuPDF.
    Handles both normal PDFs and scanned images.
"""
def extract_text_from_pdf(file_path: str, lang: str = "eng") -> str:
    text = ""
    ocr_text = ""

    with fitz.open(file_path) as doc: 
        # Step 1: Try normal PDF text extraction
        for page in doc:  
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
    
        # If text exists -> return normally
        if text.strip():
            return text.strip()
    
        # Step 2: OCR fallback (scanned PDF)
        for page in doc:
            pix = page.get_pixmap(colorspace=fitz.csRGB)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text += pytesseract.image_to_string(img, lang=lang) + "\n"

    return ocr_text.strip()
