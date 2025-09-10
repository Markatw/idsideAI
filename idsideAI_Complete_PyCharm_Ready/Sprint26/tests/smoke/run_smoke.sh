#!/usr/bin/env bash
# Sprint 26.3 — smoke test runner
set -euo pipefail
SMOKE_BASE=${SMOKE_BASE:-http://localhost:8000}
echo "Running smoke tests against ${SMOKE_BASE}"
python3 tests/smoke/test_endpoints.py
