# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements_docker.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download model from Hugging Face
RUN curl -L https://huggingface.co/abhiramAnanathu/Repay-ai/resolve/main/waste_classifier_v3.pkl -o waste_classifier_v3.pkl

# Copy the application code
COPY main.py .

# Expose the API port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
