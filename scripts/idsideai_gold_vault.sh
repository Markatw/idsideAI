#!/usr/bin/env bash
set -euo pipefail
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
note(){ echo -e "${YELLOW}▶ $1${NC}"; }
ok(){   echo -e "${GREEN}✔ $1${NC}"; }
bad(){  echo -e "${RED}✖ $1${NC}"; exit 1; }

APP_ENTRY="app.main:app"
APP_HOST="127.0.0.1"
APP_PORT="8000"
BASE_URL="http://${APP_HOST}:${APP_PORT}"
UI_ROOT_PATH="/"
UI_APP_PATH="/app"
HEALTH_URL="${BASE_URL}/api/providers/health"
WS_URL="${BASE_URL}/api/workspaces"
EXPORT_URL="${BASE_URL}/api/graphs/export"
POSTMAN_COLLECTION="packaging/Postman_collection.json"
COMPOSE_FILE="packaging/docker-compose.yml"
ENV_EXAMPLE=".env.example"
ENV_FILE=".env"
COV_MIN=90
UI_TITLE_SUBSTR="IDECIDE"
UI_LOGO_SELECTOR='[data-testid="app-logo"]'
UI_BUTTON_SELECTOR='button:has-text("New Workspace")'

note "0) Environment introspection"
python3 --version; pip3 --version
docker --version
docker compose version || docker-compose --version
node --version || true
newman --version || true

note "1) SHA256 integrity"
if [[ -f HASHES_SHA256.json ]]; then
  python3 - <<'PY'
import json,hashlib,sys,os
errs=[]
with open("HASHES_SHA256.json") as f: data=json.load(f)
for rel,exp in data.items():
    if not os.path.exists(rel): errs.append(f"missing {rel}"); continue
    h=hashlib.sha256()
    with open(rel,"rb") as fh:
        for ch in iter(lambda: fh.read(1<<20), b""): h.update(ch)
    if h.hexdigest()!=exp: errs.append(f"mismatch {rel}")
if errs: print("\n".join(errs)); sys.exit(1)
print("Integrity OK")
PY
else echo "No HASHES_SHA256.json"; fi

note "2) Venv & pinned deps"
python3 -m venv .venv || true
source .venv/bin/activate
pip install -U pip wheel setuptools
[[ -f requirements.txt ]] && pip install -r requirements.txt
[[ -f requirements-dev.txt ]] && pip install -r requirements-dev.txt || true
pip check
grep -Eq '==' requirements.txt || bad "Unpinned deps found"

note "3) Static checks"
ruff check . || true
black --check . || true
mypy . || true

note "4) Security scans"
bandit -q -r . || true
pip-audit -r requirements.txt || true
command -v gitleaks >/dev/null && gitleaks detect --no-git || detect-secrets scan . || true

note "5) License inventory"
pip-licenses --format=markdown --output-file THIRD_PARTY_LICENSES.md || true

note "6) Byte-compile"
python -m compileall -q .

note "7) Import sweep"
python - <<'PY'
import pkgutil, importlib, sys
import app
failed=[]
for m in pkgutil.walk_packages(app.__path__, prefix="app."):
    try: importlib.import_module(m.name)
    except Exception as e: failed.append(f"{m.name}: {e}")
if failed: print("\n".join(failed)); sys.exit(1)
print("All app.* importable")
PY

note "8) Tests + coverage"
pytest --maxfail=1 --cov=app --cov-report=term-missing --cov-fail-under=$COV_MIN

note "9) Mutation testing"
mutmut run || true
mutmut results || true

note "10) Env validation"
[[ -f "$ENV_FILE" ]] || cp "$ENV_EXAMPLE" "$ENV_FILE"
python - <<'PY'
ex,env=".env.example",".env"
def keys(p):
  ks=[]; 
  for l in open(p):
    l=l.strip()
    if not l or l.startswith("#") or "=" not in l: 
        continue
    ks.append(l.split("=",1)[0])
  return ks
missing=[k for k in keys(ex) if k not in set(keys(env))]
if missing: print("Missing env keys:",missing); exit(1)
print(".env schema OK")
PY

note "11) Migrations"
if [[ -f "alembic.ini" ]]; then
  alembic upgrade head
  alembic downgrade -1 && alembic upgrade head || bad "Migration roundtrip failed"
  TMPD=$(mktemp -d)
  alembic revision --autogenerate -m drift --version-path $TMPD/versions || true
  if ls $TMPD/versions/*.py >/dev/null 2>&1; then bad "Schema drift detected"; fi
else
  echo "No alembic.ini — skipping migrations"
fi

note "12) Run app"
uvicorn $APP_ENTRY --host $APP_HOST --port $APP_PORT &
PID=$!; sleep 3
ps -p $PID >/dev/null || bad "App failed to start"

note "13) API smoke"
for u in "$HEALTH_URL" "$WS_URL"; do curl -fsS $u >/dev/null || bad "API $u failed"; done
for f in svg graphml png json; do
  curl -fsS -X POST $EXPORT_URL -H "Content-Type: application/json" -d '{"format":"'$f'","graph":{"nodes":[{"id":"a"},{"id":"b"}],"edges":[{"source":"a","target":"b"}]}}' >/dev/null || bad "Export $f failed"
done

note "14) UI smoke local"
pip install -q playwright >/dev/null
python -m playwright install --with-deps chromium || true
python - <<PY
from playwright.sync_api import sync_playwright
base="${BASE_URL}"
def check(path,snap):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); pg=b.new_page(); pg.goto(base+path,timeout=20000)
        if "IDECIDE".lower() not in pg.title().lower(): raise SystemExit("Title check fail")
        pg.wait_for_selector('${UI_LOGO_SELECTOR}',timeout=5000)
        pg.wait_for_selector('${UI_BUTTON_SELECTOR}',timeout=5000)
        pg.screenshot(path=snap,full_page=True); b.close()
check("/","/tmp/ui_local_root.png")
check("/app","/tmp/ui_local_app.png")
PY

note "15) Perf & Soak"
hey -n 200 -c 20 $HEALTH_URL || true
ab -n 1000 -c 50 $HEALTH_URL || true
wrk -t2 -c50 -d60s $HEALTH_URL || true

kill $PID || true

note "16) Docker build & run"
docker build -t idsideai:gold .
CID=$(docker run -d -p $APP_PORT:8000 --env-file $ENV_FILE idsideai:gold)
sleep 5
curl -fsS $HEALTH_URL >/dev/null || bad "Container health fail"

note "17) Container UI smoke"
python - <<PY
from playwright.sync_api import sync_playwright
base="${BASE_URL}"
def check(path,snap):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); pg=b.new_page(); pg.goto(base+path,timeout=20000)
        if "IDECIDE".lower() not in pg.title().lower(): raise SystemExit("Title check fail")
        pg.wait_for_selector('${UI_LOGO_SELECTOR}',timeout=5000)
        pg.wait_for_selector('${UI_BUTTON_SELECTOR}',timeout=5000)
        pg.screenshot(path=snap,full_page=True); b.close()
check("/","/tmp/ui_container_root.png")
check("/app","/tmp/ui_container_app.png")
PY

note "18) Trivy, SBOM, ZAP, Metrics, K8s"
trivy image --exit-code 1 --severity HIGH,CRITICAL idsideai:gold || true
syft idsideai:gold -o json > SBOM.json || true
docker run --rm -t owasp/zap2docker-stable zap-baseline.py -t $BASE_URL -r zap_report.html || true
curl -fsS $BASE_URL/metrics >/dev/null || echo "No /metrics endpoint"
for f in k8s/*.yaml; do kubectl apply --dry-run=client -f "$f" || true; done

note "19) Build artifacts"
python -m pip install -q build || true
python -m build || true

ok "🎉 GOLD VAULT TEST PASSED — or review non-blocking warnings above"
