#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv || true
source .venv/bin/activate
python -m pip install -U pip wheel setuptools
if [[ -f requirements.txt ]]; then pip install -r requirements.txt; fi
if [[ -f requirements-dev.txt ]]; then pip install -r requirements-dev.txt; fi
if [[ -f .env.example && ! -f .env ]]; then cp .env.example .env; fi
echo "PyCharm setup complete."
