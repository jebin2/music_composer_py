FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy system dependencies file first
COPY requirements-system.txt /app/

# Install system dependencies
RUN apt-get update && \
    xargs apt-get install -y --no-install-recommends < /app/requirements-system.txt && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY setup.py README.md test_music_composer.py .env /app/
COPY music_composer /app/music_composer/

# Install Python dependencies
RUN pip install -e .

# Default command
CMD ["python", "test_music_composer.py"]