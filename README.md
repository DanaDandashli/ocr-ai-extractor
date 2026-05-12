# 🧾 AI Invoice Extraction & Multi-Exporter System

A modular AI-powered pipeline that extracts structured invoice data from multiple file types, processes it using LLMs and Vision Models, and exports it into various formats and storage systems.

---

<p align="center">
  <img src="assets/architecture.png" width="900"/>
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
(GPT-4o-mini)
        ↓
Structured JSON
        ↓
Export Layer
```

Used for:

- PDF invoices
- Scanned invoices
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
# Step 1: Extract invoice data
invoice_json = extract_file("data/scanned_invoice.pdf")

# Step 2: Export result
export_to_html(invoice_json, output_dir)
```

---

# 🔧 How to Use

## 📌 Change INPUT File

Modify this line inside `main.py`:

```python
invoice_json = extract_file("data/sample_invoice.pdf")
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
export_to_excel(invoice_json, output_dir)
```

Available exporters:

- `export_to_excel`
- `export_to_pdf`
- `export_to_docx`
- `export_to_html`
- `export_to_google_sheets`
- `export_to_db`

---

# 📂 Project Structure

```text
app/
│
├── data/                 # Sample invoices
├── temp_pages/           # PDF pages converted to images
├── extractors/           # File → Text extractors
├── llm/                  # LLM & Vision extraction layer
├── exporters/            # Export systems
├── db/                   # Database layer
├── utils/                # Helpers & utilities
└── main.py               # Main controller
```

---

# 🖼️ temp_pages Folder

When processing PDF invoices using the Vision pipeline:

```text
PDF → Converted into images → Stored in temp_pages/
```

Each PDF page is converted into an image before being sent to the Vision Model.

Example:

```text
temp_pages/
├── invoice_20260512_page1.png
├── invoice_20260512_page2.png
```

These temporary images are used during Vision extraction.

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

The system now supports Vision Models for scanned invoices and images.

## Vision Pipeline

Used for:

- scanned PDFs
- screenshots
- invoice images
- low-quality OCR cases

---

## Current Vision Model

```python
gpt-4o-mini
```

Configured inside:

```text
llm/invoice_extractor.py
```

---

# 🧠 Why Vision Models Were Added

Traditional OCR sometimes fails to extract:

- tables
- item structures
- blurry scans
- complex invoice layouts

Vision Models improve:

- table understanding
- layout comprehension
- scanned invoice extraction
- structured invoice detection

---

# 📤 Supported Export Formats

| Destination | Purpose |
|---|---|
| Excel | Reporting |
| PDF | Printable invoices |
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
python -m pip install openai pymupdf pillow pytesseract python-dotenv openpyxl beautifulsoup4 python-docx psycopg2-binary gspread google-auth google-auth-oauthlib google-auth-httplib2
```

---

# ▶️ Run Project

```bash
.\.venv\Scripts\python.exe app/main.py
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

If you want to export invoices to Google Sheets, follow all steps below carefully.

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
Invoices
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
python -m app.db.init_db
```

This creates:

- invoices
- invoice_items

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
        ↓
Export Layer
Excel · PDF · DOCX · HTML · Google Sheets · PostgreSQL
```

## 👨‍💻 Author

Dana Dandashli
