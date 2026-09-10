FROM python:3.11-slim

WORKDIR /app

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

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY classes.py .
COPY models.py .
COPY HSE.py .
COPY safetytrack_bridge.py .
COPY usermodels.py .
COPY language_middleware.py .
COPY extensions.py .

RUN mkdir -p uploads detection_results generated_certificates generated_documents sessions static model_cache

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# ✅ Shell form for $PORT expansion + module-level app
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 4 --timeout 300