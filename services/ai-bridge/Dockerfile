FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ai_bridge_service.py ./
COPY config/ ./config/

# Expose the service port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8002", "--workers", "2", "ai_bridge_service:app"]