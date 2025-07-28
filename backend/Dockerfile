# CreatorMate Backend Dockerfile
# Multi-stage build for Python FastAPI application

# =============================================================================
# Build Stage
# =============================================================================
FROM python:3.9-slim as builder

# Set build arguments
ARG BUILD_ENV=production
ARG BUILD_DATE
ARG VCS_REF

# Set metadata labels
LABEL maintainer="CreatorMate Team" \
      org.opencontainers.image.title="CreatorMate Backend" \
      org.opencontainers.image.description="Multi-agent YouTube analytics API" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.revision=$VCS_REF \
      org.opencontainers.image.source="https://github.com/your-org/creatormate"

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt requirements-prod.txt* ./

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install production-specific dependencies if available
RUN if [ -f "requirements-prod.txt" ]; then \
        pip install --no-cache-dir -r requirements-prod.txt; \
    fi

# =============================================================================
# Production Stage
# =============================================================================
FROM python:3.9-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r creatormate && useradd -r -g creatormate creatormate

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=creatormate:creatormate . .

# Create necessary directories
RUN mkdir -p logs backups /app/data && \
    chown -R creatormate:creatormate /app

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    LOG_LEVEL=INFO \
    HOST=0.0.0.0 \
    PORT=8888

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8888/health || exit 1

# Switch to non-root user
USER creatormate

# Expose port
EXPOSE 8888

# Start command
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888", "--workers", "1"]

# =============================================================================
# Development Stage
# =============================================================================
FROM production as development

# Switch back to root to install dev dependencies
USER root

# Install development tools
RUN apt-get update && apt-get install -y \
    git \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Copy and install development requirements
COPY requirements-dev.txt* ./
RUN if [ -f "requirements-dev.txt" ]; then \
        pip install --no-cache-dir -r requirements-dev.txt; \
    fi

# Set development environment variables
ENV ENVIRONMENT=development \
    LOG_LEVEL=DEBUG \
    RELOAD=true

# Switch back to non-root user
USER creatormate

# Development start command with auto-reload
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888", "--reload", "--log-level", "debug"]