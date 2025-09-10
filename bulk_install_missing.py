import ast, subprocess, sys
from pathlib import Path

ROOT = Path("idsideAI_Complete_PyCharm_Ready")
if not ROOT.exists():
    print("Run from repo root."); sys.exit(1)

ALIASES = {
    # known renames / extras
    "jose": "python-jose[cryptography]",
    "prometheus_client": "prometheus-client",
    "python_dotenv": "python-dotenv",
    "python_multipart": "python-multipart",
    "docx": "python-docx",
    "pptx": "python-pptx",
    "xlsxwriter": "XlsxWriter",
    "pydantic_settings": "pydantic-settings",
    "yaml": "PyYAML",
    "neo4j": "neo4j",
    "stripe": "stripe",
}

EXCLUDE_DIRS = {".venv","__pycache__","node_modules",".idea",".ruff_cache",".git",".mypy_cache"}
IGNORE = {
    # stdlib / builtins / project packages to ignore
    "typing","os","sys","re","json","time","pathlib","dataclasses","datetime","subprocess","hashlib",
    "logging","functools","itertools","uuid","base64","typing_extensions","http","urllib","zipfile",
    "collections","contextlib","asyncio","signal","shutil","tempfile","argparse","csv","math","random",
    "pprint","enum","importlib","inspect","glob","traceback","pathlib","io","gzip","tarfile",
    # project-local roots
    "backend","app","idsideai","idsideAI_Complete_PyCharm_Ready","idsideAIfinal_PyCharm_Ready","api",
}

def imported_top_levels(py_path: Path):
    try:
        tree = ast.parse(py_path.re        tree = ast.parse(py_path.re     "))
    except Exception:
                          ods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                mods.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.add(node.module.split(".")[0])
    return mods

mods = set()
for py in ROOT.rglob("*.py"):
    if any(part in EXCLUDE_DIRS for part in py.parts):
        continue
    mods |= imported_top_levels(py)

mods = {m for m in mods if m and m not in IGNORE}

# what's installed?
try:
    out = subprocess.check_output([sys.executable,"-m","pip","freeze"], text=True)
    installed = {ln.split("==")[0].split("@")[0].lower() for ln in out.splitlines() if ln.strip()}
except Exception:
    installed = set()

to_install = []
for m in sorted(mods):
    pip_name = ALIASES.get(m, m)
    base = pip_name.split("[")[0].lower()
    if base not in installed:
        to_install.append(pip_name)

if not to_install:_
python3 bulk_install_missing.py
python - <<'PY'
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "idsideAI_Complete_PyCharm_Ready"))
from backend.app import app
print("✅ import ok:", bool(app))
