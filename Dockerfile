# ── Base image ────────────────────────────────────────────────────────────────
# Python 3.11 slim — tree-sitter-languages supports up to 3.11
# Using Debian Bookworm (12) which is the current Railway default
FROM python:3.11-slim-bookworm

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    # wkhtmltopdf for PDF generation
    wkhtmltopdf \
    # build tools needed for some Python packages
    gcc \
    g++ \
    build-essential \
    # git (some langchain packages fetch at install time)
    git \
    # curl for healthchecks
    curl \
    # cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ───────────────────────────────────────────────
# Copy requirements first so Docker caches this layer
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy application code ─────────────────────────────────────────────────────
COPY . .

# ── Environment ───────────────────────────────────────────────────────────────
# Railway injects PORT automatically — default to 8000 for local Docker runs
ENV PORT=8000

# Tell pdfkit where wkhtmltopdf is on this Linux image
ENV WKHTMLTOPDF_PATH=/usr/bin/wkhtmltopdf

# ── Expose port ───────────────────────────────────────────────────────────────
EXPOSE 8000

# ── Start command ─────────────────────────────────────────────────────────────
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
