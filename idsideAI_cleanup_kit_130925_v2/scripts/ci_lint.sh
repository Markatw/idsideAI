#!/usr/bin/env bash
set -euo pipefail
ruff check . --config qc/ruff.toml --output-format=concise
mypy . --config-file qc/mypy.ini
bandit -r . -c qc/bandit.yaml || true
if [ -f requirements.txt ]; then
  pip-audit -r requirements.txt --ignore-vuln GHSA-wj6h-64fc-37mp || true
else
  echo "No requirements.txt found; skipping pip-audit"
fi