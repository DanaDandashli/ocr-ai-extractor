import sys, os
from router import extract_file
from llm.invoice_extractor import extract_invoice_json
from exporters.html_exporter import export_to_html

sys.stdout.reconfigure(encoding="utf-8")

# Step 1: Extract raw text from file
# print(extract_file("data/ara_sample_invoice.png", "ara+eng"))
text = extract_file("data/sample_invoice.xlsx")

# Step 2: Send text to LLM
invoice_json = extract_invoice_json(text)

# Step 3: Print final JSON
# Create folder if it does not exist
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
export_to_html(invoice_json, output_dir)
