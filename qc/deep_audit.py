import os, json, hashlib, ast
from pathlib import Path

STAMP = "100925"
ROOT = Path("idsideAI_Complete_PyCharm_Ready")
EXCL = {".venv",".git","__pycache__", ".ruff_cache",".mypy_cache",".idea","node_modules"}

def excluded(p: Path) -> bool:
    return any(part in EXCL for part in p.parts)

# Manifest (path, size, sha256)
files = []
for p in ROOT.rglob("*"):
    if p.is_file() and not excluded(p):
        try:
            files.append({
                "path": str(p),
                "size": int(p.stat().st_size),
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()
            })
        except Exception:
            pass

# Import scan (top-level imports per .py)
imports = {}
for py in ROOT.rglob("*.py"):
    if excluded(py):
        continue
    try:
        tree = ast.parse(py.read_text(encoding="utf-8", errors="ignore"))
        mods = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names 
                    mods.add(a.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom) and n.module:
                mods.add(n.module.split(".")[0])
        imports[str(py)] = sorted(mods)
    except Exception:
        imports[str(py)] = []

summary = {"files": len(filesummary = {"files": len(filesummary =in files))}
out = {"summary": summary, "manifest": filesout = {"summ imports}
# ensure envs for the uvicorn process:
export STRIPE_DRY_RUN=1
export STRIPE_DRY_RUN_MAX_REQUESTS=20

# run in a second terminal:
for i in $(seq 1 22); do
  printf "#%02d " "$i"
  curl -s -o /dev/null -w "%{http_code}\n" -X POST "http://127.0.0.1:${PORT:-8013}/billing/checkout"
done
python - <<'PY'
import os,json,hashlib,ast
from pathlib import Path
STAMP="100925"; ROOT=Path("idsideAI_Complete_PyCharm_Ready")
EXCL={".venv",".git","__pycache__", ".ruff_cache",".mypy_cache",".idea","node_modules"}
def excluded(p): return any(part in EXCL for part in p.parts)
# manifest
files=[]
for p in ROOT.rglob("*"):
    if p.is_file() and not excluded(p):
        try: files.append({"path":str(p),"size":int(p.stat().st_size),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
        except Exception: pass
# imports
imports={}
for py in ROOT.rglob("*.py"):
    if excluded(py): continue
    try:
        tree=ast.parse(py.read_text(encoding="utf-8",errors="ignore"))
        mods=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):
                for a in n.names: mods.add(a.name.split(".")[0])
            elif isinstance(n,ast.ImportFrom) and n.module:
                mods.add(n.module.split(".")[0])
        imports[str(py)]=sorted(mods)
    except Exception:
        imports[str(py)]=[]
summary={"files":len(files),"bytes":int(sum(f["size"] for f in files))}
out={"summary":summary,"manifest":files,"imports":imports}
Path("qc").mkdir(exist_ok=True); dst=Path(f"qc/Deep_Audit_{STAMP}.json")
dst.write_text(json.dumps(out,indent=2))
print(f"✅ Wrote {dst} (files={summary['fprint(f"✅ Wrote {mary['bytes']})")
