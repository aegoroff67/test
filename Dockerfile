# Use Python base image
FROM python:3.11-slim

# Install system dependencies including LibreOffice
RUN apt-get update && \
    apt-get install -y \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Start backend server
CMD ["python", "backend/server.py"]