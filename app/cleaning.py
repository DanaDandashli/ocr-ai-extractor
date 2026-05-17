import os


# It strips noise from the raw extracted text - empty lines, extra whitespace - before sending it to the LLM
def clean_text(text: str) -> str:
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def cleanup_images(image_paths: list):
    """Remove temporary page images after extraction."""
    for path in image_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError as e:
            print(f"[WARN] Could not delete temp file {path}: {e}")
