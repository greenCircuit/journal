# # --- STAGE 1: Build Stage ---
# FROM python:3.12-slim-bookworm AS builder
# # Prevent Python from writing .pyc files and enable unbuffered logging
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # Install system dependencies needed to build psycopg2 and other C-extensions
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     python3-dev \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Install dependencies into a wheels directory
# COPY requirements.txt .
# RUN pip install --upgrade pip && \
#     pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# # --- STAGE 2: Final Runtime Stage ---
# FROM python:3.12-slim-bookworm

# WORKDIR /app

# # Install ONLY the runtime library for PostgreSQL (smaller than the dev headers)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libpq5 \
#     && rm -rf /var/lib/apt/lists/*
# # Copy wheels from builder and install them
# COPY --from=builder /app/wheels /wheels
# RUN pip install --no-cache /wheels/*

# # Copy the rest of your Django project
# COPY . .
# RUN python3 manage.py collectstatic

# # Expose the port Gunicorn/Django will run on
# EXPOSE 8000

# # Use a non-root user for security
# RUN useradd -m django-user
# USER django-user

# # Run the application (using Gunicorn)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]

# Using alpine 
# --- STAGE 1: Build Stage ---
FROM python:3.12.12-alpine3.23 AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed to build psycopg2 and other C-extensions
# 'musl-dev' is critical for compiling C extensions on Alpine
# 'postgresql-dev' replaces 'libpq-dev'
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    postgresql-dev

# Install dependencies into a wheels directory
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- STAGE 2: Final Runtime Stage ---
FROM python:3.12.12-alpine3.23

WORKDIR /app

# Install ONLY the runtime library for PostgreSQL
# 'libpq' replaces 'libpq5'
RUN apk add --no-cache libpq

# Copy wheels from builder and install them
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy the rest of your Django project
COPY . .

RUN python3 manage.py collectstatic --noinput

# Expose the port Gunicorn/Django will run on
EXPOSE 8000

# Use a non-root user for security
# Alpine uses 'adduser' with '-D' (disabled password) instead of 'useradd'
RUN adduser -D django-user
USER django-user

# Run the application (using Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]