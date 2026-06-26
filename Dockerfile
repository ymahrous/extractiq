# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (Required for PyMuPDF/psycopg)
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command will be overridden by fly.toml for the worker
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]