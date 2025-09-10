# Sprint 27.3 — minimal app image (protocol v2)
FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Install runtime deps; dev deps optional
RUN pip install --no-cache-dir fastapi uvicorn sqlmodel requests gunicorn

EXPOSE 8000
# Expect main:app as ASGI entrypoint in repo
CMD ["docker/start.sh"]
