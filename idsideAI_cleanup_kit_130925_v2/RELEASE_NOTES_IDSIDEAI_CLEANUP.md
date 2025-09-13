# idsideAI Cleanup Kit — 13 Sep 2025

## What changed
- Added AST auto-fixer for B008 (mutable/call defaults).
- Added timezone fix script (utcnow -> timezone-aware).
- Added Ruff JSON triage and F821 import suggestion tools.
- Solidified CI workflow with Ruff/Mypy/Bandit/pip-audit (audit-only for Bandit & pip-audit).
- Included reference `backend/auth/jwt_auth.py` with HS256 verify + aware datetimes.

## Temporary flags (to revisit before release)
- Ruff ignores: E402, B905 (documented).
- Stripe remains in dry-run with note-only behavior.
- 20-command cap still in effect (document in release notes & Owner’s Manual).

## Next steps
1) Run auto-fixers, then regenerate Ruff JSON and attack E9 syntax errors first.
2) Apply import suggestions for F821 or define missing symbols.
3) Re-enable ignored rules after repo is green: E402, then B905.