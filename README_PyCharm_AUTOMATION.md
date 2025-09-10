# IDECIDE — PyCharm Ready Automations (040925)

This package adds **PyCharm automation** and scripts to run the **Gold Vault Test** and common developer tasks.

## What's inside
- `.run/` — shared PyCharm Run/Debug configurations (no local IDE hacks needed)
- `scripts/idsideai_gold_vault.sh` — full enterprise gate (Gold Vault)
- `scripts/sam_demo_gate.sh` — lightweight entry point that invokes Gold Vault
- `scripts/setup_pycharm.sh` — venv + deps bootstrap
- `.env.example` — copy to `.env` before running
- `requirements-dev.txt` — optional dev/test tools

## Quick start
```bash
bash scripts/setup_pycharm.sh
cp .env.example .env   # if not already present
# From PyCharm: select Run config "Gold Vault Test" or run:
bash scripts/idsideai_gold_vault.sh
```

**Date:** 2025-09-08
