FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_FILE=/data/expenses.json

# the pipeline passes the release version in here
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

# dependencies first, so this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py tracker.py ./

# run as a normal user instead of root
RUN useradd --create-home appuser \
    && mkdir /data \
    && chown appuser /data
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# one worker, because expenses are kept in a single json file
CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:8000", "app:app"]
