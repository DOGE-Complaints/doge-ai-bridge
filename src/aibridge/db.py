"""PostgreSQL connection helpers — dict_row factory; production memory policy."""

from __future__ import annotations

from typing import Any


def is_postgres_url(database_url: str) -> bool:
    url = (database_url or "").strip().lower()
    return url.startswith("postgresql://") or url.startswith("postgres://")


def require_psycopg() -> Any:
    try:
        import psycopg
        from psycopg import errors as pg_errors
        from psycopg.rows import dict_row
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "psycopg is required for postgresql:// DATABASE_URL; "
            "pip install 'doge-ai-bridge[postgres]' or install psycopg"
        ) from exc
    return psycopg, pg_errors, dict_row


def connect_postgres(database_url: str, *, conn: Any | None = None) -> Any:
    """Open psycopg connection with dict_row (REQ-03 R3-P0-08)."""
    if conn is not None:
        return conn
    psycopg, _errors, dict_row = require_psycopg()
    return psycopg.connect(database_url, row_factory=dict_row)


def assert_no_silent_memory_fallback(
    *,
    database_url: str,
    allow_memory: bool,
) -> None:
    """Fail closed when production forbids memory stores (AC #5)."""
    if allow_memory:
        return
    if not is_postgres_url(database_url):
        raise RuntimeError(
            "production forbids silent memory fallback for "
            "dedupe/session/confirm/tokens/history; "
            "set DATABASE_URL=postgresql://… or AIBRIDGE_ALLOW_MEMORY_STORES=true for local tests only"
        )
