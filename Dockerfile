# =============================================================================
# Daily Expense Sharing Application - Production Dockerfile
# =============================================================================
# This Dockerfile follows security best practices:
# - Uses multi-stage build for smaller image size
# - Runs as non-root user
# - Uses specific base image versions (not 'latest')
# - Minimizes layers and installed packages
# =============================================================================

# Stage 1: Builder stage
FROM python:3.11-slim-bookworm AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn


# Stage 2: Production stage
FROM python:3.11-slim-bookworm AS production

# Labels for container metadata
LABEL maintainer="Abhinav Nagar" \
      version="1.0.0" \
      description="Daily Expense Sharing Application" \
      org.opencontainers.image.source="https://github.com/abhinavnagar2696/Expense-Sharer"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    APP_HOME=/app \
    PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Set working directory
WORKDIR $APP_HOME

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appgroup . .

# Create directories for SQLite database and Flask instance with proper permissions
RUN mkdir -p /app/data /app/instance && chown -R appuser:appgroup /app/data /app/instance

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Run the application with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "60", "run:app"]
