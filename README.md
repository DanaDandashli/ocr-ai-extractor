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

### 📌 Change INPUT file type

Modify this line inside main.py:

```python
text = extract_file("data/sample_invoice.pdf")
```
You can replace:

.pdf, 
.png,
.jpg,
.jpeg,
.webp,
.xlsx,
.docx,
.html,
.txt,
.xml,
.eml

---

### 📌 Change EXPORT format

Modify the exporter function inside main.py.

Example:

```python
export_to_excel(invoice_json, output_dir)
```
Available exporters:

- export_to_excel
- export_to_pdf
- export_to_docx
- export_to_html
- export_to_google_sheets
- export_to_db

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

## Invoice Exporter — Setup Guide

## ☁️ Google Sheets Setup

If you want to export invoices to Google Sheets, follow **all steps below** carefully.

---

### Step 1 — Create Google Cloud Project

Go to [https://console.cloud.google.com/](https://console.cloud.google.com/) and create a new project.

---

### Step 2 — Enable APIs

Enable the following APIs in your project:

- **Google Sheets API**
- **Google Drive API**

---

### Step 3 — Create Service Account

Inside Google Cloud Console:

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → Service Account**
3. Complete the service account creation flow

---

### Step 4 — Generate Credentials

After creating the service account:

1. Open the service account
2. Go to the **Keys** tab
3. Click **Add Key → Create New Key → JSON**
4. Download the JSON credentials file

---

### Step 5 — Extract Required Values

From the downloaded JSON file, copy the following fields:

```
client_email
private_key
```

Paste them into your `.env` file:

```env
GOOGLE_CLIENT_EMAIL=your-service-account@project-id.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----
```

> ⚠️ **Important:**
> - Keep the private key on a **single line** (use `\n` for line breaks)
> - Do **not** expose it publicly

---

### Step 6 — Create Google Sheet Manually

Before running the code:

1. Open [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet manually

Example sheet name:

```
Invoices
```

---

### Step 7 — Get Google Sheet Key

From the Google Sheet URL:

```
https://docs.google.com/spreadsheets/d/THIS_PART_IS_THE_KEY/edit
```

Copy the key portion and add it to `.env`:

```env
GOOGLE_SHEET_KEY=THIS_PART_IS_THE_KEY
```

---

### Step 8 — Share Sheet with Service Account

1. Open your Google Sheet
2. Click **Share**
3. Add the service account email, for example:

```
your-service-account@project-id.iam.gserviceaccount.com
```

4. Grant it **Editor** access

> ⚠️ Without this step, the exporter will fail.

---

## 🗄️ PostgreSQL Database Setup

If you want to export invoices into PostgreSQL:

---

### Step 1 — Fill Database Environment Variables

Inside `.env`:

```env
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_PORT=5432
```

---

### Step 2 — Initialize Database Tables

Run this command **once** to set up the database schema:

```bash
python -m app.db.init_db
```

This will automatically create the following tables if they do not already exist:

- `invoices`
- `invoice_items`

> ✅ You only need to run this command once.

---

## 🖼️ Tesseract OCR Setup

This project uses **Tesseract OCR** for image and scanned invoice text extraction.

---

### Step 1 — Install Tesseract OCR

#### Windows

Download and install from:

- [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

> ⚠️ **During installation, select these additional languages:**
> - English (`eng`)
> - Arabic (`ara`)
> - French (`fra`)

---

### Step 2 — Locate Tesseract Executable Path

After installation, find the location of `tesseract.exe`.

Common Windows path:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

### Step 3 — Add Path to `.env`

Inside `.env`:

```env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

### Step 4 — Verify Installation

Run this command in your terminal:

```bash
tesseract --version
```

If installed correctly, Tesseract version information will appear.

---

### Notes

- Without Tesseract installed, image OCR will not work.
- Arabic OCR requires the `ara.traineddata` language file.
- French OCR requires the `fra.traineddata` language file.
- Language files are usually installed automatically if selected during setup.

---

## 📄 Full `.env` Example

```env
# Google Sheets
GOOGLE_CLIENT_EMAIL=your-service-account@project-id.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----
GOOGLE_SHEET_KEY=your_google_sheet_key_here

# PostgreSQL
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_PORT=5432

# Tesseract OCR
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
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

Dana Dandashli
