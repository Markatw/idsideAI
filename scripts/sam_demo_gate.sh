#!/usr/bin/env bash
set -euo pipefail
# Lightweight gate that calls the full gold vault by default
if [[ -x "scripts/idsideai_gold_vault.sh" ]]; then
  bash scripts/idsideai_gold_vault.sh
else
  echo "Gold vault script missing at scripts/idsideai_gold_vault.sh"; exit 1
fi
