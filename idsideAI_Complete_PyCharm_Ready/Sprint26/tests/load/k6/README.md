# k6 Load Test (Sprint 26.4)

Basic load harness using k6 to hit `/api/metrics/health`.

## Requirements
- k6 installed locally (`brew install k6` or see https://k6.io).

## Run
```bash
export BASE=http://localhost:8000  # optional
export VUS=20                      # optional
export DURATION=2m                 # optional
bash tests/load/k6/run.sh
# or directly:
k6 run -e BASE=${BASE:-http://localhost:8000} -e VUS=${VUS:-10} -e DURATION=${DURATION:-1m} tests/load/k6/script.js
```
