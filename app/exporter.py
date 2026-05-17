from app.exporters.html_exporter import export_to_html
from app.exporters.excel_exporter import export_to_excel
from app.exporters.docx_exporter import export_to_docx
from app.exporters.pdf_exporter import export_to_pdf
from app.exporters.google_sheets_exporter import export_to_google_sheets
from app.exporters.db_exporter import export_to_db


# exporter.py — routes to the correct exporter
def export(data: dict, format: str, output_dir: str = "output") -> None:
    if format == "html":
        export_to_html(data, output_dir)
    elif format == "excel":
        export_to_excel(data, output_dir)
    elif format == "docx":
        export_to_docx(data, output_dir)
    elif format == "pdf":
        export_to_pdf(data, output_dir)
    elif format == "sheets":
        export_to_google_sheets(data)
    elif format == "db":
        export_to_db(data)
    else:
        print(f"Unsupported export format: {format}")
