FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 libpq-dev gcc wget curl \
    libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 \
    libffi-dev shared-mime-info fonts-dejavu-core && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py classes.py models.py HSE.py safetytrack_bridge.py usermodels.py language_middleware.py extensions.py debug_models.py app_init_debug.py .

RUN mkdir -p uploads detection_results generated_certificates generated_documents sessions static model_cache

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 TF_CPP_MIN_LOG_LEVEL=2 PYTHONFAULTHANDLER=1

EXPOSE 8000

CMD exec gunicorn app:app --bind 0.0.0.0:${PORT:-8000} --workers 2 --worker-class sync --timeout 900 --graceful-timeout 60 2>&1 | tee -a /tmp/startup.log
