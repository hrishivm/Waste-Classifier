# -------- Base image --------
FROM python:3.11-slim-bookworm

# -------- Environment variables --------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# -------- Set working directory --------
WORKDIR /app

# -------- Install system dependencies (minimal) --------
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------- Install Python dependencies (cache optimized) --------
COPY requirements_docker.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements_docker.txt

# -------- Copy application code --------
COPY main.py .

# -------- Create non-root user & writable directories --------
RUN useradd -m appuser \
    && mkdir -p /app/models \
    && chown -R appuser:appuser /app

# -------- Switch to non-root user --------
USER appuser

# -------- Expose port --------
EXPOSE 8000

# -------- Run FastAPI app --------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
