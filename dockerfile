FROM python:3.13.4-alpine

WORKDIR /app

# Install dev dependencies
RUN apk update && apk add --no-cache \
    curl \
    build-base \
    && rm -rf /var/cache/apk/*

# Copy requirements file (if you have one)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
