# exporter.py — routes to the correct exporter
def export(data: dict, format: str, output_dir: str = "output") -> None:
    if format == "html":
        from app.exporters.html_exporter import export_to_html
        export_to_html(data, output_dir)
    elif format == "excel":
        from app.exporters.excel_exporter import export_to_excel
        export_to_excel(data, output_dir)
    elif format == "docx":
        from app.exporters.docx_exporter import export_to_docx
        export_to_docx(data, output_dir)
    elif format == "pdf":
        from app.exporters.pdf_exporter import export_to_pdf
        export_to_pdf(data, output_dir)
    elif format == "sheets":
        from app.exporters.google_sheets_exporter import export_to_google_sheets
        export_to_google_sheets(data)
    elif format == "db":
        from app.exporters.db_exporter import export_to_db
        export_to_db(data)
    else:
        print(f"Unsupported export format: {format}")
