# --- STAGE 1: Build Stage ---
FROM python:3.12-slim-bookworm AS builder
# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed to build psycopg2 and other C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a wheels directory
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- STAGE 2: Final Runtime Stage ---
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install ONLY the runtime library for PostgreSQL (smaller than the dev headers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*
RUN pyton3 manage.py collectstatic
# Copy wheels from builder and install them
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy the rest of your Django project
COPY . .

# Expose the port Gunicorn/Django will run on
EXPOSE 8000

# Use a non-root user for security
RUN useradd -m django-user
USER django-user

# Run the application (using Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]