FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dri \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libpq-dev \
    gcc \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (NO .env, NO models, NO data)
COPY app.py .
COPY classes.py .
COPY models.py .
COPY HSE.py .
COPY safetytrack_bridge.py .
COPY usermodels.py .
COPY language_middleware.py .
COPY extensions.py .



# Create required directories
RUN mkdir -p uploads detection_results generated_certificates generated_documents sessions static model_cache

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

EXPOSE 8000

CMD ["python", "app.py"]