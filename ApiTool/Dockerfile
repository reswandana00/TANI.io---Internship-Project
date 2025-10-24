# Use official Python image as base
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8011

# Command to run the application
CMD ["uvicorn", "api_endpoints:app", "--host", "0.0.0.0", "--port", "8011"]