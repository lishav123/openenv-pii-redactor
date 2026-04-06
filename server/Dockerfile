# Use the specified Python 3.11-slim base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install openenv-core

# Copy the entire project to the working directory
COPY . /app/

# Set the PYTHONPATH to include the /app directory
ENV PYTHONPATH="/app"

# Expose the server port
EXPOSE 8000

# Command to run the application
CMD ["python", "server/app.py"]
