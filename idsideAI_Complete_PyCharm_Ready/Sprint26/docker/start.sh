#!/usr/bin/env sh
# Sprint 27.4 — start script for gunicorn (protocol v2)
set -e
exec python -m gunicorn -c docker/gunicorn.conf.py main:app
