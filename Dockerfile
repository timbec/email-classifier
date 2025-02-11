# Use the official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY ALL application files (Fixes missing `main.py`)
COPY . .  # ← This ensures `main.py` and other files are copied

# Expose the FastAPI port
EXPOSE 8080

# Set Python path explicitly
ENV PYTHONPATH=/app

# Run FastAPI app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

