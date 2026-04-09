FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ai_service.py ./

# Expose the service port
EXPOSE 5000

# Default command to run the Flask app. In production this can be replaced
# with a WSGI server like gunicorn for improved performance.
CMD ["python", "ai_service.py"]