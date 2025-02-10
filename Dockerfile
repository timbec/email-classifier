# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Print Python and pip version
RUN python --version && pip --version

# Show what's inside the requirements file
COPY requirements.txt .
RUN cat requirements.txt

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip setuptools wheel

# Install system dependencies (some packages need these)
RUN apt-get update && apt-get install -y \
    gcc libpq-dev python3-dev libssl-dev libffi-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
