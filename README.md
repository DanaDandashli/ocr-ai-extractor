# 🧾 AI Document Extraction & Multi-Exporter System

A modular AI-powered pipeline that extracts structured document data from multiple file types, processes it using LLMs and Vision Models, and exports it into various formats and storage systems.

---

<p align="center">
  <img src="assets/architecture_2.png" width="900"/>
</p>


## 🚀 Key Idea

This project is designed as a configurable pipeline controlled from `main.py`.

You choose:

- Input file type (PDF, Image, Excel, DOCX, HTML, TXT, XML, Email)
- Extraction method (Vision Model or Text Extraction)
- Output format (Excel, PDF, DOCX, HTML, Google Sheets, Database)

---

# 🧠 Updated Pipeline Architecture

## 📄 Text-Based Documents

```text
INPUT FILE → TEXT EXTRACTION → LLM PROCESSING → EXPORT LAYER
```

Used for:

- DOCX
- XLSX
- HTML
- TXT
- XML
- EML

---

## 🖼️ Vision-Based Documents

```text
PDF / IMAGE
        ↓
Vision Processing Layer
(PDF → Images)
        ↓
Vision LLM Extraction
(qwen/qwen3.5-flash-02-23)
        ↓
Structured JSON
        ↓
Export Layer
```

Used for:

- PDF documents
- Scanned documents
- Images (`png`, `jpg`, `jpeg`, `webp`)

---

## ⚙️ main.py (Main Control Center)

All execution is controlled from `main.py`.

You decide:

- which file to process
- which extraction pipeline to use
- which exporter to run

---

## Example

```python
# Step 1: Extract document data
document_json = extract_file("data/scanned_invoice.pdf")

# Step 2: Export result
export(document_json, format="html", output_dir=output_dir)
```

---

# 🔧 How to Use

## 📌 Change INPUT File

Modify this line inside `main.py`:

```python
document_json = extract_file("data/sample_invoice.pdf")
```

Supported formats:

```text
.pdf, .png, .jpg, .jpeg, .webp, .xlsx, .docx, .html, .txt, .xml, .eml
```

---

## 📌 Change EXPORT Format

Modify exporter function inside `main.py`.

Example:

```python
export(document_json, format="html", output_dir=output_dir)
```

Available formats:

- `html`
- `excel`
- `docx`
- `pdf`
- `sheets`
- `db`

---

# 📂 Project Structure

```text
ocr-ai-extractor/
│
├── app/
│   ├── fonts/                    # Arabic & custom fonts
│   ├── exporters/                # Export systems
│   │   ├── db/
│   │   |    ├── connection.py
│   │   |    ├── init_db.py
│   │   |    └── schema.sql
│   │   ├── excel_exporter.py
│   │   ├── pdf_exporter.py
│   │   ├── docx_exporter.py
│   │   ├── html_exporter.py
│   │   ├── google_sheets_exporter.py
│   │   └── db_exporter.py
│   ├── cache.py                  # Caching layer
│   ├── cleaning.py               # Data cleaning utilities
│   ├── client.py                 # AI client setup
│   ├── exporter.py               # Export router
│   ├── file_extractor.py         # File → Text extraction
│   ├── file_naming.py            # Unique filename generator
│   ├── handle_errors.py          # Error handling
│   ├── lookup.py                 # Lookup utilities
│   └── router.py                 # Extraction pipeline router
│
├── cache/                        # Cached extraction results
├── assets/                       # README images
├── data/                         # Sample documents
├── output/                       # Exported files
├── temp_pages/                   # PDF pages converted to images
├── .env                          # Environment variables
├── requirements.txt              # Project dependencies
└── main.py                       # Main controller
```

---

# 🖼️ temp_pages Folder

When processing PDF documents using the Vision pipeline:

```text
PDF → Converted into images → Stored in temp_pages/
```

Each PDF page is converted into an image before being sent to the Vision Model.

Example:

```text
temp_pages/
├── page_20260512_1.png
├── page_20260512_2.png
```

These temporary images are used during Vision extraction.

---

# ⚡ Caching System

The system includes a caching layer to avoid redundant AI extraction calls.

## How It Works

```text
File Submitted
      ↓
Cache Check
      ↓
Cache Hit? → Return Cached Result (instant)
      ↓
Cache Miss? → Run AI Extraction → Store in Cache → Return Result
```

- When a file is submitted, the system checks the `cache/` folder first
- If the same file was processed before, the cached result is returned immediately — no API call is made
- This reduces cost, improves response time, and avoids duplicate processing

---


# 📥 Supported Input Formats

| Type | Method |
|---|---|
| PDF | Vision Model + PyMuPDF |
| Images | Vision Model |
| HTML | BeautifulSoup |
| TXT | Direct Read |
| DOCX | python-docx |
| XLSX | openpyxl |
| Email | email parser |
| XML | xml parser |

---

# 🤖 Vision Model Support

The system now supports Vision Models for scanned documents and images.

## Vision Pipeline

Used for:

- scanned PDFs
- screenshots
- document images
- low-quality OCR cases

---

## Current Vision Model

```python
qwen/qwen3.5-flash-02-23
```

Configured inside:

```text
app/client.py
```

---

# 🧠 Why Vision Models Were Added

Traditional OCR sometimes fails to extract:

- tables
- item structures
- blurry scans
- complex document layouts

Vision Models improve:

- table understanding
- layout comprehension
- scanned document extraction
- structured document detection

---

# 📤 Supported Export Formats

| Destination | Purpose |
|---|---|
| Excel | Reporting |
| PDF | Printable documents |
| DOCX | Editable documents |
| HTML | Web display |
| Google Sheets | Cloud sharing |
| PostgreSQL DB | Structured storage |

---

# 🌍 OCR Language Support

Install Tesseract languages:

- `eng` → English
- `ara` → Arabic
- `fra` → French

---

# ⚙️ Installation

```bash
python -m pip install openai pymupdf pillow pytesseract python-dotenv openpyxl beautifulsoup4 python-docx psycopg2-binary gspread google-auth google-auth-oauthlib google-auth-httplib2 arabic-reshaper python-bidi
```

---

# ▶️ Run Project

```bash
.\.venv\Scripts\python.exe main.py
```

---

# 🔐 Environment Variables

```env
OPENAI_API_KEY=

DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=5432

GOOGLE_CLIENT_EMAIL=
GOOGLE_PRIVATE_KEY=
GOOGLE_SHEET_KEY=

TESSERACT_PATH=
```

---

# ☁️ Google Sheets Setup

If you want to export documents to Google Sheets, follow all steps below carefully.

---

## Step 1 — Create Google Cloud Project

Go to:

https://console.cloud.google.com/

Create a new project.

---

## Step 2 — Enable APIs

Enable:

- Google Sheets API
- Google Drive API

---

## Step 3 — Create Service Account

Inside Google Cloud Console:

1. Go to:
   `APIs & Services → Credentials`
2. Click:
   `Create Credentials → Service Account`
3. Complete setup

---

## Step 4 — Generate Credentials

After creating service account:

1. Open service account
2. Go to `Keys`
3. Click:
   `Add Key → Create New Key → JSON`
4. Download credentials JSON

---

## Step 5 — Extract Required Values

Copy these values from JSON:

```text
client_email
private_key
```

Add them into `.env`:

```env
GOOGLE_CLIENT_EMAIL=your-service-account@project-id.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----
```

---

## Step 6 — Create Google Sheet

Open:

https://sheets.google.com/

Create a spreadsheet manually.

Example:

```text
Documents
```

---

## Step 7 — Get Google Sheet Key

From:

```text
https://docs.google.com/spreadsheets/d/THIS_PART_IS_THE_KEY/edit
```

Add:

```env
GOOGLE_SHEET_KEY=THIS_PART_IS_THE_KEY
```

---

## Step 8 — Share Sheet with Service Account

Share sheet with:

```text
your-service-account@project-id.iam.gserviceaccount.com
```

Grant:

- Editor access

Without this step, export will fail.

---

# 🗄️ PostgreSQL Database Setup

---

## Step 1 — Fill Database Variables

```env
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_PORT=5432
```

---

## Step 2 — Initialize Database

Run once:

```bash
python -m app.exporters.db.init_db
```

This creates:

- documents table — stores all extracted document data as JSONB,
  supporting any document type (invoices, receipts, contracts, reports, etc.)

---

# 🖼️ Tesseract OCR Setup

This project uses Tesseract OCR for traditional OCR extraction.

---

## Step 1 — Install Tesseract

### Windows

Download from:

https://github.com/UB-Mannheim/tesseract/wiki

During installation select:

- English (`eng`)
- Arabic (`ara`)
- French (`fra`)

---

## Step 2 — Locate Executable

Common path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## Step 3 — Add to `.env`

```env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## Step 4 — Verify Installation

```bash
tesseract --version
```

---

# 📄 Full `.env` Example

```env
# OpenAI / OpenRouter
OPENAI_API_KEY=

# Google Sheets
GOOGLE_CLIENT_EMAIL=
GOOGLE_PRIVATE_KEY=
GOOGLE_SHEET_KEY=

# PostgreSQL
DB_HOST=localhost
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=5432

# Tesseract OCR
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

# 🏗️ Full System Architecture

```text
Input Files
(PDF / Images / DOCX / XLSX / HTML / TXT / XML / Email)
        ↓
Cache Layer
(Return instantly if file was processed before)
        ↓
Extraction Layer
(PyMuPDF · Tesseract · BeautifulSoup · openpyxl · docx)
        ↓
Vision Layer
(PDF → Images → Vision Model)
        ↓
LLM Processing Layer
(OpenAI / OpenRouter)
        ↓
Structured JSON
(Multi-invoice detection → pages[] / sheets[])
        ↓
Export Layer
Excel · PDF · DOCX · HTML · Google Sheets · PostgreSQL
```

## 👨‍💻 Author

Dana Dandashli
