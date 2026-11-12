#!/usr/bin/env bash
# Start disposable local Postgres for aibridge QA / story13 E2E (no Railway).
# Cluster lives under doge-ai-bridge/.pgdata-test (not Homebrew system Postgres).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export LANG="${LANG:-en_US.UTF-8}" LC_ALL="${LC_ALL:-en_US.UTF-8}"
PGDATA="${AIBRIDGE_PGDATA:-$ROOT/.pgdata-test}"
PGPORT="${AIBRIDGE_PGPORT:-55432}"
PG_BIN="${AIBRIDGE_PG_BIN:-/opt/homebrew/opt/postgresql@15/bin}"
if [[ ! -x "$PG_BIN/initdb" ]]; then
  PG_BIN="/usr/local/opt/postgresql@15/bin"
fi
if [[ ! -x "$PG_BIN/pg_ctl" ]]; then
  echo "ERROR: pg_ctl not found (tried homebrew postgresql@15). Set AIBRIDGE_PG_BIN." >&2
  exit 1
fi

_port_listening() {
  if command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:"$PGPORT" -sTCP:LISTEN 2>/dev/null | grep -q postgres
    return $?
  fi
  (echo >/dev/tcp/127.0.0.1/"$PGPORT") >/dev/null 2>&1
}

_psql_ok() {
  "$PG_BIN/psql" -h "$PGDATA" -p "$PGPORT" -U aibridge -d postgres -v ON_ERROR_STOP=1 -c 'SELECT 1' >/dev/null 2>&1
}

_stop_cluster() {
  # Best-effort: pg_ctl stop, pidfile PID, then any postgres still listening on PGPORT
  "$PG_BIN/pg_ctl" -D "$PGDATA" -m fast stop >/dev/null 2>&1 || true
  if [[ -f "$PGDATA/postmaster.pid" ]]; then
    local pid
    pid="$(head -1 "$PGDATA/postmaster.pid" 2>/dev/null || true)"
    if [[ -n "${pid:-}" ]]; then
      kill "$pid" 2>/dev/null || true
      sleep 0.5
      kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$PGDATA/postmaster.pid"
  fi
  if command -v lsof >/dev/null 2>&1; then
    local p
    for p in $(lsof -t -nP -iTCP:"$PGPORT" -sTCP:LISTEN 2>/dev/null || true); do
      kill "$p" 2>/dev/null || true
      sleep 0.3
      kill -9 "$p" 2>/dev/null || true
    done
  fi
  rm -f "$PGDATA/.s.PGSQL.${PGPORT}" "$PGDATA/.s.PGSQL.${PGPORT}.lock" 2>/dev/null || true
}

if [[ ! -d "$PGDATA" ]]; then
  "$PG_BIN/initdb" -D "$PGDATA" -U aibridge --auth-local=trust --auth-host=trust -A trust --locale=C --encoding=UTF8
fi

already=0
if _psql_ok; then
  already=1
fi

# Port up but psql dead / pidfile missing = orphaned listener → recycle
if [[ "$already" -eq 0 ]] && _port_listening; then
  _stop_cluster
  sleep 0.5
fi

if [[ "$already" -ne 1 ]]; then
  if _port_listening || [[ -f "$PGDATA/postmaster.pid" ]]; then
    _stop_cluster
    sleep 0.5
  fi
  if ! "$PG_BIN/pg_ctl" -D "$PGDATA" -o "-p $PGPORT -k $PGDATA" -l "$PGDATA/logfile" start; then
    echo "WARN: pg_ctl start failed; forcing stop and retry once..." >&2
    if tail -5 "$PGDATA/logfile" 2>/dev/null | grep -q "Operation not permitted"; then
      echo "HINT: shmget Operation not permitted — run this script in a normal macOS Terminal" >&2
      echo "      (Cursor agent sandbox blocks Postgres shared memory)." >&2
    fi
    _stop_cluster
    sleep 1
    "$PG_BIN/pg_ctl" -D "$PGDATA" -o "-p $PGPORT -k $PGDATA" -l "$PGDATA/logfile" start
  fi
  for _i in 1 2 3 4 5 6 7 8 9 10; do
    if _psql_ok; then
      break
    fi
    sleep 0.3
  done
fi

if ! _psql_ok; then
  echo "ERROR: disposable Postgres not accepting connections on $PGDATA port $PGPORT" >&2
  echo "--- last logfile lines ---" >&2
  tail -20 "$PGDATA/logfile" 2>/dev/null >&2 || true
  exit 1
fi

"$PG_BIN/createdb" -h "$PGDATA" -p "$PGPORT" -U aibridge aibridge_test 2>/dev/null || true

echo "DATABASE_URL=postgresql://aibridge@/aibridge_test?host=$PGDATA&port=$PGPORT"
echo "OK: disposable Postgres accepting connections (pg_available should be True)."
