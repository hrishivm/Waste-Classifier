# -------- Base image (small & stable) --------
FROM python:3.11-slim-bookworm

# -------- Environment settings --------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# -------- Set workdir --------
WORKDIR /app

# -------- Install system dependencies (minimal) --------
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# -------- Install Python dependencies (layer caching optimized) --------
COPY requirements_docker.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements_docker.txt

# -------- Copy only required app files --------
COPY main.py .

# -------- Use non-root user (best practice) --------
RUN useradd -m appuser
USER appuser

# -------- Expose port --------
EXPOSE 8000

# -------- Run app --------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
