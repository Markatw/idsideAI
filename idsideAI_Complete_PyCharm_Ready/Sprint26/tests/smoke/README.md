# Smoke Tests (Sprint 26.3)

Run against a local FastAPI server:

```bash
export SMOKE_BASE=http://localhost:8000
bash tests/smoke/run_smoke.sh
# or
python3 tests/smoke/test_endpoints.py
```
Artifacts print a JSON summary to stdout.
