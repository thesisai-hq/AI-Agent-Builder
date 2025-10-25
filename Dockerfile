FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install package in development mode
RUN pip install -e .

# Expose API port (can be overridden with --env API_PORT=<port>)
ARG API_PORT=8000
EXPOSE ${API_PORT}

# Run API server with configurable host and port
CMD uvicorn agent_framework.api:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${API_PORT:-8000}
