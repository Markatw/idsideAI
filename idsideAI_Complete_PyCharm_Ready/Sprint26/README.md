# idsideAI


## PyCharm Setup
- Open the project in PyCharm.
- Ensure Python 3.11 interpreter is selected.
- Install dependencies via `pip install -r requirements-dev.txt`.
- Run FastAPI with `uvicorn main:app --reload`.


## Packaging
- Install in editable mode for development:
  ```bash
  pip install -e .
  ```
- Build a distribution:
  ```bash
  python -m pip install build
  python -m build
  ```


## Deployment

### Docker Compose
1. Copy `.env.example` to `.env` and adjust values as needed.
2. Run `docker compose up --build`.
3. App will be available at `http://localhost:8000`.

### Gunicorn
- Container launches with `gunicorn` using `docker/gunicorn.conf.py`.
- Logs are sent to stdout/stderr.

### Healthchecks
- `GET /healthz` → liveness probe.
- `GET /readyz` → readiness probe (checks env wiring).

### PyCharm + CI
- For dev: open in PyCharm, use Python 3.11 interpreter, install `requirements-dev.txt`.
- CI: `pytest` and `flake8` run via GitHub Actions (see .github/workflows/ci.yml).


## Investor Materials
- [Investor Pack (PDF)](docs/investor/Investor_Pack_Final.pdf)
- [Pitch Deck (PPTX)](docs/investor/Investor_Pitch_Deck.pptx)
