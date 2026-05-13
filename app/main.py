import sys, os
from router import extract_file
from exporters.html_exporter import export_to_html

sys.stdout.reconfigure(encoding="utf-8")

invoice_json = extract_file("data/sample_invoice.html")
# invoice_json = extract_file("test_pipeline/02_corrupt/blur_image.png")

if isinstance(invoice_json, dict) and invoice_json.get("success") is False:
    print("\nExtraction failed. Nothing will be exported.")
    print(invoice_json.get("message"))
    sys.exit(0)

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
export_to_html(invoice_json, output_dir)
# print("\n=== FINAL JSON ===\n")
# print(invoice_json)
