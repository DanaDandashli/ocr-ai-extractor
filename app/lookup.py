# ── Currency mapping ──────────────────────────────────────────────────────────
CURRENCY_MAP = {
    "$": "USD", "usd": "USD", "us$": "USD",
    "€": "EUR", "eur": "EUR", "euro": "EUR",
    "£": "GBP", "gbp": "GBP",
    "¥": "JPY", "jpy": "JPY", "yen": "JPY",
    "₺": "TRY", "try": "TRY", "turkish lira": "TRY",
    "₹": "INR", "inr": "INR", "rs": "INR",
    "aed": "AED", "dh": "AED", "dhs": "AED",
    "sar": "SAR", "sr": "SAR",
    "ll": "LBP", "lbp": "LBP",
}

# ── Supported file extensions ─────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {
    ".pdf":  "pdf",
    ".png":  "image",
    ".jpg":  "image",
    ".jpeg": "image",
    ".webp": "image",
    ".docx": "text",
    ".xlsx": "text",
    ".xls":  "text",
    ".html": "text",
    ".htm":  "text",
    ".txt":  "text",
    ".xml":  "text",
    ".eml":  "text",
}

# ── Document type labels ──────────────────────────────────────────────────────
DOCUMENT_TYPES = [
    "invoice",
    "tender",
    "legal",
    "receipt",
    "contract",
    "report",
    "form",
    "letter",
    "purchase_order",
    "delivery_note",
    "other",
]

# ── Prompts ──────────────────────────────────────────────────────────
EXTRACTION_RULES = """
- Extract every field exactly as printed. Do not compute, infer, or invent.
- If a value is absent → null.
- If tables exist → extract them as lists of row objects.
- For multi-sheet spreadsheets, wrap sheets under a "sheets" array where each sheet contains a "document_type" field.
- All string values must be on a single line. Replace any line breaks (\\n) with a single space.
Return ONLY valid JSON. No markdown, no prose, no extra text.
"""

PROMPTS: dict[str, str] = {
    "tender": """
You are extracting a tender/RFP document. Focus on:
- Issuing authority, reference number, submission deadline
- Scope of work and deliverables
- Evaluation criteria and weightings
- Required documents and certifications
""",
    "legal": """
You are extracting a legal document. Focus on:
- Parties, their roles and signatories
- Effective date, jurisdiction, governing law
- Obligations, rights, and restrictions
- Termination clauses and penalties
""",
    "invoice": """
You are extracting an invoice. Focus on:
{
    "invoice_number":       null,
    "date":                 null,   # invoice date (YYYY-MM-DD)
    "due_date":             null,   # payment due date (YYYY-MM-DD)
    "order_number":         null,   # sales/order number on the invoice
    "purchase_order_number": null,  # buyer's PO number
    "payment_terms":        null,   # e.g. "Net 30", "20 days".
    "payment_method":       null,   # e.g. "Bank Transfer", "UPI", "Credit Card", "PayPal".
    "notes":                null,   # footer notes, terms, or instructions

    # ── Vendor ────────────────────────────────────────
    "vendor_name":          null,
    "vendor_address":       null,   # full address including Attn:, department, street, city, zip exclude phone, email, and contact details
    "vendor_phone_nb":      null,   
    "vendor_email":         null,   # extract from header/footer only if clearly labeled — do NOT include in notes
    "vendor_website":       null,   # Check header and footer for website, extract separately — do NOT include in notes
    "vendor_tax_id":        null,   # EIN, SSN, PAN, or generic tax ID
    "vendor_vat_number":    null,   # VAT / GSTIN / GST registration number
    "vendor_iban":          null,
    "vendor_bank_name":     null,
    "vendor_account_number": null,
    "vendor_swift_bic":     null,
    "vendor_ifsc":          null,   # Indian IFSC code

    # ── Customer ──────────────────────────────────────
    "customer_name":        null,
    "customer_address":     null,   # full address including Attn:, department, street, city, zip exclude phone, email, and contact details
    "customer_phone_nb":    null,
    "customer_email":       null,
    "customer_website":     null,
    "customer_tax_id":      null,
    "customer_vat_number":  null,
    "customer_iban":        null,
    "customer_reference":   null,   # customer's internal account/reference number

    # ── Line Items ────────────────────────────────────
    "items": [
        {
            "name":         null,
            "description":  null,   # second line or sub-text printed below the name, if any — never a product code or identifier
            "sku":          null,   # product code, SKU, barcode, ASIN — any alphanumeric identifier printed near the item name
            "unit":         null,   # unit of measure ONLY e.g. "each", "BTL", "kg", "hr", "STRP" - never include quantity here
            "quantity":     0,
            "unit_price":   0.0,
            "discount":     0.0,   # line-level discount
            "tax_rate":     null,  # per-line tax rate e.g. "12%", "18%"
            "tax_amount":   0.0,   # per-line tax amount
            "total":        0.0    # extract printed value exactly, never calculate
        }
    ],

    # ── Summary ───────────────────────────────────────
    "subtotal":             0.0,   # sum of line totals before tax/discount
    "discount":             0.0,   # total discount
    "shipping":             0.0,   # shipping & handling
    "tax_rate":             null,
    "tax_amount":           0.0,   # total tax amount
    "total":                0.0,   # extract printed value exactly, never calculate
    "extra_fields":         {},    # ONLY unexpected financial charges or fees not listed above e.g. fuel_surcharge, late_fee, customs_duty, handling_fee
    "amount_paid":          0.0,   # already paid
    "currency":             null   # extract exactly as printed e.g. "$", "USD", "LL"
}
""",
    "contract": """
You are extracting a contract. Focus on:
- Contracting parties and representatives
- Term, renewal conditions, exit clauses
- Financial terms and payment schedules
- Warranties, liabilities, and indemnities
""",
    "receipt": """
You are extracting a receipt. Focus on:
- Store name, address, date and time
- Itemised purchases with prices
- Payment method, subtotal, tax, total
""",
    "report": """
You are extracting a report document. Focus on:
- Title, author(s), date, organization
- Executive summary or abstract
- Key findings and recommendations
- Data tables, metrics, and statistics
- Sections and sub-sections with their content
""",
}

FALLBACK_PROMPT = """
You are a precise data extraction engine.
Extract every meaningful field from this document into a structured JSON object.
"""

CLASSIFICATION_PROMPT = f"""
Classify this document into exactly ONE of these types:
{", ".join(DOCUMENT_TYPES)}

Reply with ONLY the single lowercase type word. No explanation.
"""

GROUPING_PROMPT = """
Given {n} PDF page images, group pages that belong to the same document.
Return ONLY a JSON array of 0-based page index groups.
Example (4 pages: 0-1 together, 2 and 3 separate):
[[0,1],[2],[3]]
"""

# ── Lookup functions ──────────────────────────────────────────────────────────

def get_file_type(extension: str) -> str | None:
    """Return pipeline type for a given file extension, or None if unsupported."""
    return SUPPORTED_EXTENSIONS.get(extension.strip().lower())


def is_supported(extension: str) -> bool:
    """Check if a file extension is supported."""
    return extension.strip().lower() in SUPPORTED_EXTENSIONS


def get_prompt(doc_type: str) -> str:
    base = PROMPTS.get(doc_type, FALLBACK_PROMPT)
    return f"{base}{EXTRACTION_RULES}"
