FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application
COPY . .

# Fix permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports for backend and frontend
EXPOSE 8000
EXPOSE 8080

# Create startup script
RUN echo '#!/bin/sh\npython -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & python frontend/serve.py' > /app/start.sh && \
    chmod +x /app/start.sh

# Start both services
CMD ["/app/start.sh"]
