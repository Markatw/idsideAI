#!/usr/bin/env bash
set -euo pipefail
mkdir -p qc
ruff check . --format json > qc/ruff.json
echo "Wrote qc/ruff.json"