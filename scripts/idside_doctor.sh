#!/usr/bin/env bash
set -euo pipefail
APP_LOG=/tmp/app_stderr.log
PORT_DEFAULT=${PORT:-8013}
DB_URL_DEFAULT=${DATABASE_URL:-"postgresql://idside:idside@127.0.0.1:5432/idside"}
echo "🔧 IDECIDE Doctor starting…"
if [[ ! -f ".env" ]]; then
  if [[ -f ".env.sample" ]]; then cp .env.sample .env; fi
fi
set -a; source .env; set +a
PORT=${PORT:-$PORT_DEFAULT}
DATABASE_URL=${DATABASE_URL:-$DB_URL_DEFAULT}
if lsof -i :$PORT >/dev/null 2>&1; then
  echo "Port $PORT busy"; exit 1
fi
if command -v psql >/dev/null 2>&1; then
  PGPASSWORD=$(echo "$DATABASE_URL" | sed -n 's|.*://[^:]*:\([^@]*\)@.*|\1|p') psql "$DATABASE_URL" -c "select 1;" || exit 1
fi
alembic upgrade head || exit 1
uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --reload 2> "$APP_LOG" &
sleep 2
echo "🎉 Done."
