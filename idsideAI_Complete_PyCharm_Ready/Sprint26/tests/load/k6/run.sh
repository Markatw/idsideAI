#!/usr/bin/env bash
# Sprint 26.4 — k6 load test runner
set -euo pipefail
BASE=${BASE:-http://localhost:8000}
VUS=${VUS:-10}
DURATION=${DURATION:-1m}
echo "Running k6: BASE=$BASE VUS=$VUS DURATION=$DURATION"
k6 run -e BASE="$BASE" -e VUS="$VUS" -e DURATION="$DURATION" tests/load/k6/script.js
