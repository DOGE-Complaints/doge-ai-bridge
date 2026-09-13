#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PGDATA="${AIBRIDGE_PGDATA:-$ROOT/.pgdata-test}"
PG_BIN="${AIBRIDGE_PG_BIN:-/opt/homebrew/opt/postgresql@15/bin}"
if [[ ! -x "$PG_BIN/pg_ctl" ]]; then
  PG_BIN="/usr/local/opt/postgresql@15/bin"
fi
if [[ -d "$PGDATA" ]] && "$PG_BIN/pg_ctl" -D "$PGDATA" status >/dev/null 2>&1; then
  "$PG_BIN/pg_ctl" -D "$PGDATA" stop -m fast
  echo "stopped $PGDATA"
else
  echo "not running"
fi
