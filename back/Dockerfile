FROM python:3.12-slim

WORKDIR /app

# Create a non-root user for security
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# Create home directory for appuser
RUN mkdir -p /home/appuser && chown -R appuser:appgroup /home/appuser

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.4

# Configure Poetry to not create a virtual environment inside the container
RUN poetry config virtualenvs.create false --local

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the code
COPY . /app/

# Create all required directories for uploads based on config.py
RUN mkdir -p /app/uploads/videos /app/uploads/subtitles /app/uploads/thumbnails \
    && chown -R appuser:appgroup /app

# Set environment variables for the non-root user
ENV HOME=/home/appuser
ENV PATH="$PATH:/home/appuser/.local/bin"
ENV POETRY_HOME="$HOME/.poetry"
ENV POETRY_CACHE_DIR="$HOME/.cache/pypoetry"

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Command to start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
