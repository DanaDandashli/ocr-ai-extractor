from docx import Document


"""
    This function extract text from .docx file (Word documents).
"""
def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    seen = set()
    output = []

    # paragraphs
    for para in doc.paragraphs:
        t = para.text.strip()
        if t and t not in seen:
            seen.add(t)
            output.append(t)

    # tables
    for table in doc.tables:
        for row in table.rows:
            row_data = []

            for cell in row.cells:
                text = cell.text.strip()

                # avoid duplicates inside same row
                if text and text not in row_data:
                    row_data.append(text)

            if row_data:
                row_str = " | ".join(row_data)

                # avoid duplicate rows
                if row_str not in seen:
                    seen.add(row_str)
                    output.append(row_str)

    return "\n".join(output).strip()
