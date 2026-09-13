# Reproducible deploy / node clone (R3-P1-07). No Railway SUCCESS invent — build locally.
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

COPY requirements.txt pyproject.toml README.md ./
COPY src ./src
COPY migrations ./migrations

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --no-deps .

EXPOSE 8080

# Match railpack.json start shape; PORT from env at runtime.
CMD ["sh", "-c", "python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port ${PORT:-8080}"]
