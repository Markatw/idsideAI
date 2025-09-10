# Sprint 27.4 — gunicorn production config (protocol v2)
import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv("WEB_THREADS", 2))
timeout = int(os.getenv("WEB_TIMEOUT", 60))
graceful_timeout = int(os.getenv("WEB_GRACEFUL", 30))
keepalive = int(os.getenv("WEB_KEEPALIVE", 5))
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")
