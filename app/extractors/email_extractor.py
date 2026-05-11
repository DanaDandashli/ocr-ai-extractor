from email import policy
from email.parser import BytesParser


"""
    This function extract text from .eml email files.
    Captures subject + body (plain/text + html fallback).
"""
def extract_text_from_email(file_path: str) -> str:
    with open(file_path, "rb") as file:
        msg = BytesParser(policy=policy.default).parse(file)

    parts = []

    # Subject
    if msg["subject"]:
        parts.append(f"Subject: {msg['subject']}")

    # From / To 
    if msg["from"]:
        parts.append(f"From: {msg['from']}")
    if msg["to"]:
        parts.append(f"To: {msg['to']}")

    # Body extraction
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()

            if content_type == "text/plain":
                body += part.get_content()

            elif content_type == "text/html":
                body += part.get_content()
    else:
        body = msg.get_content()

    parts.append("\nEmail Body:\n" + body)

    return "\n".join(parts).strip()
