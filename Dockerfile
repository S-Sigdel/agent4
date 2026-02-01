# Use slim python image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the standard port
EXPOSE 8080

# Start app on port 8080 (Code Engine requirement)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]