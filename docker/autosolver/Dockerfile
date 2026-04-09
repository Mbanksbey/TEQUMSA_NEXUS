# Multi-stage Alpine-based Dockerfile for TEQUMSA Autosolver
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

# Copy requirements files
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
RUN addgroup -g 1000 autosolver && \
    adduser -D -u 1000 -G autosolver autosolver

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/autosolver/.local

# Copy application code
COPY main.py .

# Set ownership
RUN chown -R autosolver:autosolver /app

# Switch to non-root user
USER autosolver

# Update PATH to include local packages
ENV PATH=/home/autosolver/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "main.py", "--daemon"]
