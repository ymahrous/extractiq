# Dockerfile
FROM python:3.11-slim

# System dependencies required for PyMuPDF and Psycopg
RUN apt-get update && apt-get install -y libgl1-mesa-gl libglib2.0

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to start the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]