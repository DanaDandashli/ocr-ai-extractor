import sys, os
from router import extract_file
from exporters.html_exporter import export_to_html

sys.stdout.reconfigure(encoding="utf-8")

invoice_json = extract_file("data/scanned_sample_invoice.pdf")

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
export_to_html(invoice_json, output_dir)
#print("\n=== FINAL JSON ===\n")
#print(invoice_json)
