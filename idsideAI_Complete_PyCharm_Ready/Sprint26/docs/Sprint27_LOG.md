# Sprint 27 — Final QA & Packaging

## 27.1 — Scaffold 27
- Time: 03-09-2025 10:56 (Europe/London)
- VERSION bumped to 27.0.0
- Log + checklist seeded

## 27.2 — PyCharm project skeleton finalizer
- Time: 03-09-2025 10:59 (Europe/London)
- Added pyproject.toml, requirements-dev.txt, .idea/.gitignore, README PyCharm section

## 27.3 — Docker Compose (Postgres, Redis, app)
- Time: 03-09-2025 11:01 (Europe/London)
- Added docker-compose.yml, docker/Dockerfile, .env.example

## 27.4 — Production gunicorn config
- Time: 03-09-2025 11:04 (Europe/London)
- Added docker/gunicorn.conf.py and docker/start.sh; Dockerfile now installs gunicorn and starts via start.sh

## 27.5 — Healthcheck endpoints for Docker
- Time: 03-09-2025 11:05 (Europe/London)
- Added /healthz (liveness) and /readyz (readiness) with env checks; imported in routes/__init__.py

## 27.6 — Lint/test CI pipeline (pytest, flake8)
- Time: 03-09-2025 11:08 (Europe/London)
- Added .github/workflows/ci.yml, pytest.ini, .flake8

## 27.7 — Packaging (pip installable)
- Time: 03-09-2025 11:11 (Europe/London)
- Added setup.py, setup.cfg, MANIFEST.in; ensured app/__init__.py; README packaging section

## 27.8 — Deployment README.md polish
- Time: 03-09-2025 11:13 (Europe/London)
- README updated with Docker Compose, gunicorn, healthchecks, PyCharm+CI notes

## 27.9 — Pre-wrap stabilization
- Time: 03-09-2025 11:15 (Europe/London)
- Ensured __init__.py in core dirs, top-level files present, .gitkeep added for empty dirs

## 27.10 — Deep Audit Pack + Wrap
- Time: 03-09-2025 11:17 (Europe/London)
- Deep audit generated; wrap packaged; protocol v2 satisfied
