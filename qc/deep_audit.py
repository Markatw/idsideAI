#!/usr/bin/env python3
import json, hashlib, ast
from pathlib import Path

STAMP = "100925"
ROOT = Path("idsideAI_Complete_PyCharm_Ready")
EXCL = {".venv",".git","__pycache__", ".ruff_cache",".mypy_cache",".idea","node_modules","qc"}

def excluded(p: Path) -> bool:
    return any(part in EXCL for part in p.parts)

# Manifest
manifest = []
for p in ROOT.rglob("*"):
    if p.is_file() and not excluded(p):
        try:
            manifest.append({
                "path": str(p),
                "size": int(p.stat().st_size),
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            })
        except Exception:
            pass

# Import scan
imports = {}
for py in ROOT.rglob("*.py"):
    if excluded(py):
        continue
    try:
        tree = ast.parse(py.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        imports[str(py)] = []
        continue
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom) and n.m        elif isinstance(n, ast.ImportFrom) ".")[0])
    imports[str(py)] = sorted(mods)

summary = {"files": len(manifest), "bytes": int(sum(f["size"] for f in manifest))}
out = {"summary": summary, "manifest": manifest, "imports": imports}

Path("qc").mkdir(exist_ok=True)
dst = Path(f"qc/Deep_Audit_{STAMP}.json")
dst.write_text(json.dumps(out, indent=2))
dst.write_text(json.dumps(outs={summary['files']}, bytes={summary['bytes']})")
