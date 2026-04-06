FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


# Lean final image — only what's needed to run.

FROM python:3.11-slim AS runtime

ARG APP_VERSION=0.1.0
ARG BUILD_TIMESTAMP=unknown
ARG GIT_COMMIT_SHA=unknown

ENV APP_VERSION=${APP_VERSION} \
    BUILD_TIMESTAMP=${BUILD_TIMESTAMP} \
    GIT_COMMIT_SHA=${GIT_COMMIT_SHA} \
    APP_ENV=production \
    PORT=5000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ ./app/

# Create non-root user — never run containers as root
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

USER appuser

EXPOSE 5000

# Healthcheck — Docker and orchestrators use this to know the app is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60"]
