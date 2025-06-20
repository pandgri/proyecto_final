# Builder stage
FROM python:3.12-slim as builder
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m myuser && \
    chown -R myuser:myuser /app && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R myuser:myuser /app/staticfiles /app/media

USER myuser

ENV DEBUG=True \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
