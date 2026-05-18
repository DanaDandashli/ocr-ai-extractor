# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-ara \
    tesseract-ocr-fra \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ───────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project files ────────────────────────────────────────────────────────
COPY . .

# Expose app port
EXPOSE 8000

# ── Create required directories ───────────────────────────────────────────────
RUN mkdir -p cache output temp_pages data

# ── Environment variables ─────────────────────────────────────────────────────
ENV TESSERACT_PATH=/usr/bin/tesseract
ENV PYTHONUNBUFFERED=1

# ── Entry point ───────────────────────────────────────────────────────────────
CMD ["python", "main.py"]
