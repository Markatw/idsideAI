"""
Sprint 25.8 — Structured JSON logging (protocol v2)
"""

import datetime
import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        ts = datetime.datetime.utcfromtimestamp(record.created).isoformat() + "Z"
        log_obj = {
            "timestamp": ts,
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_obj)


def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(JsonFormatter())
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger
