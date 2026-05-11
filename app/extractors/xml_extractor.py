import xml.etree.ElementTree as ET


"""
    This function extract text from XML invoice files.
    Flattens all tags into readable text.
"""
def extract_text_from_xml(file_path: str) -> str:
    tree = ET.parse(file_path)
    root = tree.getroot()

    text_parts = []

    def recurse(element):
        if element.text and element.text.strip():
            text_parts.append(f"{element.tag}: {element.text.strip()}")

        for child in element:
            recurse(child)

        if element.tail and element.tail.strip():
            text_parts.append(element.tail.strip())

    recurse(root)

    return "\n".join(text_parts).strip()
