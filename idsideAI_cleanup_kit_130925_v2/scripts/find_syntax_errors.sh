#!/usr/bin/env bash
    set -euo pipefail
    python - <<'PY'
import sys, compileall
ok = compileall.compile_dir(".", force=False, quiet=1, maxlevels=10)
print("compileall ok:", ok)
PY