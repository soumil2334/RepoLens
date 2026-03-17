# ── Base image ────────────────────────────────────────────────────────────────
# Python 3.11 — matches local environment, tree-sitter-languages supports 3.11
FROM python:3.11-slim-bookworm

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    gcc \
    g++ \
    build-essential \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ───────────────────────────────────────────────
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --no-deps -r requirements.txt

# ── Copy application code ─────────────────────────────────────────────────────
COPY . .

# ── Environment ───────────────────────────────────────────────────────────────
ENV PORT=8000
ENV WKHTMLTOPDF_PATH=/usr/bin/wkhtmltopdf

# ── Expose port ───────────────────────────────────────────────────────────────
EXPOSE 8000

# ── Start command ─────────────────────────────────────────────────────────────
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
