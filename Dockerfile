# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for image processing (OpenCV, etc.)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements_docker.txt requirements.txt

# Install dependencies
# Note: Using the provided requirements.txt might try to install CUDA versions of torch.
# If you want CPU-only, remove the --index-url and specify torch versions.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model
COPY main.py .
COPY waste_classifier_v3.pkl .

# Expose the API port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
