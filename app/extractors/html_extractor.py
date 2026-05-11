from bs4 import BeautifulSoup


"""
    This function extract clean readable text from HTML files.

    Removes:
    - HTML tags
    - JavaScript
    - CSS styles
    - unnecessary spacing
"""
def extract_text_from_html(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "meta", "link"]):
        tag.decompose()

    # Extract visible text
    text = soup.get_text(separator=" ")

    # Clean excessive spaces/newlines
    text = " ".join(text.split())

    return text.strip()
