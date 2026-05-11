import sys
from router import extract_file
from llm.invoice_extractor import extract_invoice_json

sys.stdout.reconfigure(encoding="utf-8")

# Step 1: Extract raw text from file
# print(extract_file("data/ara_sample_invoice.png", "ara+eng"))
text = extract_file("data/sample_invoice.pdf")

# Step 2: Send text to LLM
print(extract_invoice_json(text))