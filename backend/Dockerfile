FROM python:3.10.0-slim AS base

# Set environment variables to prevent pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add /app to PYTHONPATH so imports like 'from backend.src...' work
ENV PYTHONPATH=/app

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/backend/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/backend/requirements.txt

# Copy the rest of the application code
COPY . /app/backend/

# Ensure log and db directories exist and declare them as volumes
RUN mkdir -p /app/backend/logs /app/backend/db
VOLUME ["/app/backend/logs", "/app/backend/db"]

# Expose the defined port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]