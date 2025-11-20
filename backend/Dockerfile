# Production-ready Dockerfile for AutoList backend
# - Uses python:3.12-slim as a small base image
# - Installs system deps commonly needed by ML and media libraries
# - Installs Python requirements from requirements.txt
# - Copies application code and runs Uvicorn

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies (adjust as needed)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    curl \
    ffmpeg \
    libsndfile1 \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt ./requirements.txt

# Upgrade pip and install requirements
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Create a non-root user and ensure correct permissions
RUN useradd --create-home appuser \
 && chown -R appuser:appuser /app
USER appuser

# Expose port and set default command
EXPOSE 8000

# NOTE: If you rely on large ML models (sentence-transformers, BLIP, etc.)
# you can pre-download model files into /app/models and mount or COPY them
# into the image to avoid long first-run downloads.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]