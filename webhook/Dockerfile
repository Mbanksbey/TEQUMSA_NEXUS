# Alpine-based Dockerfile for TEQUMSA Autosolver Webhook
# Part of ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞ Consciousness Framework

# Build stage
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-alpine

# Install runtime dependencies
RUN apk add --no-cache \
    libffi \
    openssl \
    ca-certificates && \
    rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1000 webhook && \
    adduser -D -u 1000 -G webhook webhook

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/webhook/.local

# Copy application code
COPY app.py .

# Set ownership
RUN chown -R webhook:webhook /app

# Switch to non-root user
USER webhook

# Update PATH to include local packages
ENV PATH=/home/webhook/.local/bin:$PATH

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5000/health || exit 1

# Default command
CMD ["python", "app.py"]
