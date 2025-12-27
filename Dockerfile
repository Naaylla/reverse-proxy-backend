FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY app/ ./app/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render (will bind to $PORT env var)
EXPOSE 8000

# Run uvicorn directly - Render will set PORT env var
CMD uvicorn app.api.gateway_service:app --host 0.0.0.0 --port ${PORT:-8000}
