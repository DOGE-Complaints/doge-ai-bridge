#!/usr/bin/env bash
# Start disposable local Postgres for aibridge story-09 tests (no Railway).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export LANG="${LANG:-en_US.UTF-8}" LC_ALL="${LC_ALL:-en_US.UTF-8}"
PGDATA="${AIBRIDGE_PGDATA:-$ROOT/.pgdata-test}"
PGPORT="${AIBRIDGE_PGPORT:-55432}"
PG_BIN="${AIBRIDGE_PG_BIN:-/opt/homebrew/opt/postgresql@15/bin}"
if [[ ! -x "$PG_BIN/initdb" ]]; then
  PG_BIN="/usr/local/opt/postgresql@15/bin"
fi
if [[ ! -d "$PGDATA" ]]; then
  "$PG_BIN/initdb" -D "$PGDATA" -U aibridge --auth-local=trust --auth-host=trust -A trust --locale=C --encoding=UTF8
fi
if ! "$PG_BIN/pg_ctl" -D "$PGDATA" status >/dev/null 2>&1; then
  "$PG_BIN/pg_ctl" -D "$PGDATA" -o "-p $PGPORT -k $PGDATA" -l "$PGDATA/logfile" start
  sleep 1
fi
"$PG_BIN/createdb" -h "$PGDATA" -p "$PGPORT" -U aibridge aibridge_test 2>/dev/null || true
echo "DATABASE_URL=postgresql://aibridge@/aibridge_test?host=$PGDATA&port=$PGPORT"
