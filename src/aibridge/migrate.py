"""Versioned SQL migrations — sole production schema mechanism (story 09)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aibridge.db import connect_postgres, is_postgres_url, require_psycopg

DEFAULT_MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"


def migrations_dir() -> Path:
    return DEFAULT_MIGRATIONS_DIR


def list_migration_files(directory: Path | None = None) -> list[Path]:
    root = directory or migrations_dir()
    if not root.is_dir():
        return []
    return sorted(p for p in root.glob("*.sql") if p.is_file())


def applied_versions(conn: Any) -> set[str]:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
          version TEXT PRIMARY KEY,
          applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    conn.commit()
    rows = conn.execute("SELECT version FROM schema_migrations").fetchall()
    out: set[str] = set()
    for row in rows:
        if isinstance(row, dict):
            out.add(str(row["version"]))
        else:
            out.add(str(row[0]))
    return out


def current_migration_version(conn: Any) -> str | None:
    versions = applied_versions(conn)
    if not versions:
        return None
    return sorted(versions)[-1]


def apply_migrations(
    database_url: str,
    *,
    directory: Path | None = None,
    conn: Any | None = None,
) -> list[str]:
    """Apply pending ``*.sql`` files in order. Returns applied version ids."""
    if not is_postgres_url(database_url) and conn is None:
        raise ValueError("apply_migrations requires postgresql:// DATABASE_URL")
    own_conn = conn is None
    c = connect_postgres(database_url, conn=conn)
    _psycopg, pg_errors, _dict_row = require_psycopg()
    applied: list[str] = []
    try:
        have = applied_versions(c)
        for path in list_migration_files(directory):
            version = path.stem  # e.g. 0001_ssot_core
            if version in have:
                continue
            sql = path.read_text(encoding="utf-8")
            try:
                c.execute(sql)
                c.execute(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    (version,),
                )
                c.commit()
            except Exception:
                c.rollback()
                raise
            applied.append(version)
    finally:
        if own_conn:
            c.close()
    return applied


def boot_create_table_forbidden_in_production(*, ensure_schema: bool) -> None:
    """Documented guard — production callers must pass ensure_schema=False."""
    if ensure_schema:
        # Allowed only for disposable unit fakes / offline mirrors — not production.
        return
