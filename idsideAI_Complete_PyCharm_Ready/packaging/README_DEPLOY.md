# idsideAI — Deploy & Run (ABSOLUTE GREEN)

## Run locally (PyCharm)
- Open project root in PyCharm
- Ensure Python 3.11
- Use the run configuration: **Run idsideAI (uvicorn)**
  - It sets PYTHONPATH to `Sprint26` so `app.*` imports resolve
  - Launches `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Run locally (CLI)
```bash
export PYTHONPATH=$(pwd)/Sprint26
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker
```bash
cd packaging
docker build -t idsideai:green .
docker run --rm -p 8000:8000 idsideai:green
# or with compose:
docker compose up --build
```

## Quick API smoke (manual)
- POST /api/graphs/export with {"fmt":"svg","graph":{"nodes":[{"id":"A"}],"edges":[]}} → 200 + SVG
- GET /api/workspaces → 200 + [{"id":"default","name":"Default"}]
- POST /api/graphs/export with {"fmt":"graphml", ...} → 200 + XML header

## Notes
- This pack matches the **ABSOLUTE GREEN** tree: compile=0, import(app.*)=0, stubs=0, placeholders=0.
- All imports are side-effect free; webserver start is only via uvicorn CLI.
