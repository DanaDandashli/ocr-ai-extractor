import sys,os
from app.router import extract_file
from app.exporter import export

document_json = extract_file("data/scanned_sample_invoice.pdf")

if isinstance(document_json, dict) and document_json.get("success") is False:
    print("\nExtraction failed. Nothing will be exported.")
    print(document_json.get("message"))
    sys.exit(0)

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
export(document_json, format="pdf", output_dir=output_dir)

# print("\n=== FINAL JSON ===\n")
# print(document_json)
