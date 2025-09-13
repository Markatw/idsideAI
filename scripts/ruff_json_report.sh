#!/usr/bin/env bash
set -euo pipefail
mkdir -p qc
ruff check . --config qc/ruff.toml --output-format json > qc/ruff.json
echo "Wrote qc/ruff.json"
