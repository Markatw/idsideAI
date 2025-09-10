# Sprint 26 — Running Log (protocol v2)

## 26.1 — QA & Soak Testing Scaffold
- Time: 03-09-2025 10:29 (Europe/London)
- Actions: Created Sprint26 root; VERSION set to 26.0.0; initialized log and checklist.

## 26.2 — Test data factories
- Time: 03-09-2025 10:32 (Europe/London)
- utils/factories: make_user, make_workspace, make_subscription
- routes/factories_test: endpoints for each factory

## 26.3 — API smoke tests (FastAPI)
- Time: 03-09-2025 10:34 (Europe/London)
- tests/smoke: test_endpoints.py, run_smoke.sh, README.md

## 26.4 — Load test harness (k6 skeleton)
- Time: 03-09-2025 10:36 (Europe/London)
- tests/load/k6: script.js, run.sh, README.md

## 26.5 — Long-run soak job
- Time: 03-09-2025 10:38 (Europe/London)
- utils/soak: start/stop/status, background loop
- routes/soak: /api/soak/start, /stop, /status

## 26.6 — Error budget tracker (SLO draft)
- Time: 03-09-2025 10:39 (Europe/London)
- utils/slo: record/status with 1% budget
- routes/slo: /record, /status

## 26.7 — Synthetic uptime probe
- Time: 03-09-2025 10:41 (Europe/London)
- utils/probe: check_url, uptime
- routes/probe: /check, /batch

## 26.8 — Flaky test catcher
- Time: 03-09-2025 10:42 (Europe/London)
- utils/flaky: rerun(func, times)
- tests/flaky/test_flaky: demo test

## 26.9 — Pre-wrap stabilization
- Time: 03-09-2025 10:44 (Europe/London)
- Ensured __init__.py files, bumped VERSION to 26.0.1, updated routes imports

## 26.10 — Deep Audit Pack + Wrap
- Time: 03-09-2025 10:45 (Europe/London)
- Full manifest, critical hashes, stub sweep, delta summary
