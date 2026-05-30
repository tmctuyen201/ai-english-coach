# =============================================================================
# AI English Coach — Backend Dockerfile (Multi-stage)
# =============================================================================

# ---- Base ----
FROM python:3.12-slim as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ffmpeg libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

# ---- Dependencies ----
FROM base as dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Development ----
FROM dependencies as development
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"]

# ---- Production ----
FROM dependencies as production
COPY . .
RUN python -m compileall -q app/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "warning"]
