# 🧾 AI Invoice Extraction & Multi-Exporter System

A modular AI-powered pipeline that extracts structured invoice data from multiple file types, processes it using LLMs, and exports it into various formats and storage systems.

---

## 🚀 Key Idea

This project is designed as a **configurable pipeline controlled from `main.py`**.

You choose:

- Input file type (PDF, image, Excel, DOCX, HTML, TXT, XML, email)
- Output format (Excel, PDF, DOCX, HTML, Google Sheets, Database)

---

## 🧠 How the Pipeline Works

```
INPUT FILE → TEXT EXTRACTION → LLM PROCESSING → EXPORT LAYER
```

---

## 🧠 System Architecture Overview

flowchart TD

A[📄 Input Layer<br/>PDF / Image / DOCX / HTML / XLSX / TXT / EMAIL / XML]

B[🔍 Extraction Layer<br/>PyMuPDF · Tesseract OCR · BeautifulSoup · openpyxl · docx]

C[🧹 Text Cleaning Layer<br/>Normalization & Formatting]

D[🤖 LLM Processing Layer<br/>OpenAI / OpenRouter<br/>Structured JSON Output]

E[📊 Export Layer<br/>Excel · PDF · DOCX · HTML · Google Sheets · PostgreSQL]

F1[📁 Excel Export]
F2[📄 PDF / DOCX / HTML]
F3[☁️ Google Sheets]
F4[🗄️ PostgreSQL DB]

A --> B --> C --> D --> E

E --> F1
E --> F2
E --> F3
E --> F4

---

## ⚙️ main.py (Main Control Center)

All execution is controlled from `main.py`.

You decide:

- which file to process
- which extractor to use
- which exporter to run

### Example:

```python
# Step 1: Extract raw text from file
text = extract_file("data/sample_invoice.xlsx")

# Step 2: Send text to LLM
invoice_json = extract_invoice_json(text)

# Step 3: Export result (choose format here)
export_to_html(invoice_json, output_dir)
```

---

## 🔧 How to Use

### 📌 Change INPUT file type (in main.py)

Supported formats:

- PDF
- Image
- Excel
- DOCX
- HTML
- TXT
- XML
- Email

Example:

```python
text = extract_file("data/sample_invoice.pdf")
```

---

### 📌 Change EXPORT format (in main.py)

Supported exporters:

- Excel
- PDF
- DOCX
- HTML
- Google Sheets
- PostgreSQL Database

Example:

```python
export_to_excel(invoice_json, output_dir)
```

---

## 📂 Project Structure

```
app/
│
├── data/              # Sample invoices (test files)
├── llm/               # LLM processing layer
├── extractors/        # File → Text converters
├── exporters/         # Output systems
├── db/                # Database layer
└── main.py            # 🚀 Main controller
```

---

## 📁 Data Folder

The `data/` folder contains sample files:

- PDF invoices
- Excel invoices
- Images
- HTML files
- DOCX files

You can add your own test files here.

---

## 📥 Supported Input Formats

| Type   | Method        |
| ------ | ------------- |
| PDF    | PyMuPDF       |
| Images | Tesseract OCR |
| HTML   | BeautifulSoup |
| TXT    | Direct read   |
| DOCX   | python-docx   |
| XLSX   | openpyxl      |
| Email  | email parser  |
| XML    | xml parser    |

---

## 📤 Supported Export Formats

| Destination   | Purpose            |
| ------------- | ------------------ |
| Excel         | Reporting          |
| PDF           | Printable invoices |
| DOCX          | Editable documents |
| HTML          | Web display        |
| Google Sheets | Cloud sharing      |
| PostgreSQL DB | Structured storage |

---

## 🤖 LLM Model

- Don't forget to modify the openai model in `llm/invoice_extractor.py`

---

## 🌍 OCR Language Support

Install Tesseract languages:

- `eng` → English
- `ara` → Arabic
- `fra` → French

---

## ⚙️ Installation

```bash
python -m pip install openai pymupdf pillow pytesseract python-dotenv openpyxl beautifulsoup4 python-docx psycopg2-binary gspread google-auth google-auth-oauthlib google-auth-httplib2
```

---

## ▶️ Run Project

```bash
.\.venv\Scripts\python.exe app/main.py
```

---

## 🔐 Environment Variables

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

## 🏗️ System Architecture

```
Input Files
(PDF / Image / DOCX / XLSX / HTML / TXT / XML / Email)
        ↓
Extraction Layer
(PyMuPDF · Tesseract · BeautifulSoup · openpyxl · docx)
        ↓
LLM Processing Layer
(OpenAI / OpenRouter → structured JSON)
        ↓
Export Layer
Excel · PDF · DOCX · HTML · Google Sheets · Database
```

---

## 👨‍💻 Author

AI-powered invoice extraction system for structured document intelligence and automation.
