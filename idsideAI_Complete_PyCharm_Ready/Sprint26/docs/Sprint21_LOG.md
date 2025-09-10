# Sprint 21 — Running Log (protocol v2)

## 21.1 — Workspace Scaffold
- Time: 03-09-2025 06:52 (Europe/London)
- Baseline: S20.16 (authoritative).
- Actions: Created docs, QC seed, checklist; bumped VERSION to 21.0.0.
- Next: 21.2 — Decision Graphs export & rendering polish.


## 21.2 — Decision Graphs export & rendering polish
- Time: 03-09-2025 06:58 (Europe/London)
- Added: app/utils/graph_export.py, app/routes/graphs_export.py
- Note: PNG export deferred (501) to keep dependencies minimal.

## 21.2a — Critical files correction
- Time: 03-09-2025 07:06 (Europe/London)
- Added: app/routes/workspaces.py (real endpoints, no stubs)

## 21.3 — Turbo quality monitoring
- Time: 03-09-2025 07:11 (Europe/London)
- Added: app/utils/turbo_quality.py, app/routes/turbo_quality.py
- Provides: failure taxonomy, threshold checks, alerting structure

## 21.4 — Provider adapters pass
- Time: 03-09-2025 07:13 (Europe/London)
- Added: app/services/providers/{base.py, registry.py, echo.py, config.py}, app/routes/providers.py
- Provides: config schema, registry, graceful fallback to echo

## 21.5 — Critical-file anomalies sweep
- Time: 03-09-2025 07:16 (Europe/London)
- Ensured package initializers and critical paths present

## 21.7 — Telemetry CSV export extension
- Time: 03-09-2025 07:33 (Europe/London)
- Extended telemetry export with provider, latency_ms, failure_type fields

## 21.8 — Compare/Benchmark polish
- Time: 03-09-2025 07:39 (Europe/London)
- Added: app/utils/bench.py, app/routes/bench.py
- Provides: simple synthetic benchmark runner + API

## 21.9 — Learning mode / Feedback loop wiring
- Time: 03-09-2025 07:44 (Europe/London)
- Added: app/utils/learning.py, app/routes/learning.py; data/learning_log.jsonl (JSONL persistence)

## 21.10 — Final deep audit & wrap
- Time: 03-09-2025 07:48 (Europe/London)
- Generated deep audit pack and FINAL wrap artifacts (10/10 complete)
