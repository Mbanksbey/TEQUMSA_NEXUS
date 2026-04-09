# TEQUMSA Quantum-MCP v3.0 - Recognition Orchestrator
# Constitutional Invariants: σ=1.0, L∞=φ^48, RDoD≥0.9777

FROM python:3.11-slim

LABEL maintainer="TEQUMSA Project <recognition@tequmsa.org>"
LABEL version="3.0.0"
LABEL description="Recognition Orchestrator - Core Consciousness Coordination"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/lib/python \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy core library
COPY lib/ /app/lib/

# Copy service code
COPY services/recognition-orchestrator/ /app/services/recognition-orchestrator/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "services.recognition-orchestrator.main:app", "--host", "0.0.0.0", "--port", "8000"]
