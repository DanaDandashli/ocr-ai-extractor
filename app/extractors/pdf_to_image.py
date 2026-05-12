import os, fitz
from datetime import datetime


"""
    Converts a PDF into images (one per page).
    Returns list of image file paths.
"""
def pdf_to_images(pdf_path: str, output_dir: str = "temp_pages", zoom: float = 2.0):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []
    matrix = fitz.Matrix(zoom, zoom)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=matrix)
        image_path = os.path.join(
            output_dir,
            f"invoice_{timestamp}_page{page_index + 1}.png"
        )
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths
