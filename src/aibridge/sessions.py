"""Minimal session store with content_bundle_hash pin (story 02)."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from aibridge.registry import BundleRegistry, ContentBundleRow, _require_psycopg


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class SessionRow:
    session_id: str
    content_bundle_hash: str
    deployment_id: str
    active: bool
    created_at: datetime
    updated_at: datetime


class SessionStore(Protocol):
    def create(
        self,
        *,
        session_id: str,
        content_bundle_hash: str,
        deployment_id: str,
    ) -> SessionRow: ...

    def get(self, session_id: str) -> SessionRow | None: ...

    def resume_bundle(
        self, session_id: str, registry: BundleRegistry
    ) -> ContentBundleRow: ...

    def active_bundle_hashes(self) -> set[str]: ...

    def deactivate(self, session_id: str) -> None: ...

    def close(self) -> None: ...


class MemorySessionStore:
    def __init__(self) -> None:
        self._rows: dict[str, SessionRow] = {}

    def create(
        self,
        *,
        session_id: str,
        content_bundle_hash: str,
        deployment_id: str,
    ) -> SessionRow:
        now = _utc_now()
        row = SessionRow(
            session_id=session_id,
            content_bundle_hash=content_bundle_hash,
            deployment_id=deployment_id,
            active=True,
            created_at=now,
            updated_at=now,
        )
        self._rows[session_id] = row
        return row

    def get(self, session_id: str) -> SessionRow | None:
        return self._rows.get(session_id)

    def resume_bundle(
        self, session_id: str, registry: BundleRegistry
    ) -> ContentBundleRow:
        session = self.get(session_id)
        if session is None or not session.active:
            raise KeyError(f"session not found or inactive: {session_id}")
        row = registry.get(session.content_bundle_hash)
        if row is None:
            raise LookupError(
                f"pinned bundle missing: {session.content_bundle_hash}"
            )
        return row

    def active_bundle_hashes(self) -> set[str]:
        return {
            r.content_bundle_hash for r in self._rows.values() if r.active
        }

    def deactivate(self, session_id: str) -> None:
        existing = self._rows.get(session_id)
        if existing is None:
            return
        self._rows[session_id] = SessionRow(
            session_id=existing.session_id,
            content_bundle_hash=existing.content_bundle_hash,
            deployment_id=existing.deployment_id,
            active=False,
            created_at=existing.created_at,
            updated_at=_utc_now(),
        )

    def close(self) -> None:
        return None


_SESSION_SCHEMA = """
CREATE TABLE IF NOT EXISTS session (
  session_id TEXT PRIMARY KEY,
  content_bundle_hash TEXT NOT NULL,
  deployment_id TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""

_PG_SESSION_SCHEMA = """
CREATE TABLE IF NOT EXISTS session (
  session_id TEXT PRIMARY KEY,
  content_bundle_hash TEXT NOT NULL,
  deployment_id TEXT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
"""


class SqliteSessionStore:
    def __init__(self, path: str | Path) -> None:
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(_SESSION_SCHEMA)
        self._conn.commit()

    def create(
        self,
        *,
        session_id: str,
        content_bundle_hash: str,
        deployment_id: str,
    ) -> SessionRow:
        now = _utc_now().isoformat()
        self._conn.execute(
            """
            INSERT INTO session (
              session_id, content_bundle_hash, deployment_id, active, created_at, updated_at
            ) VALUES (?, ?, ?, 1, ?, ?)
            """,
            (session_id, content_bundle_hash, deployment_id, now, now),
        )
        self._conn.commit()
        row = self.get(session_id)
        assert row is not None
        return row

    def get(self, session_id: str) -> SessionRow | None:
        cur = self._conn.execute(
            "SELECT * FROM session WHERE session_id = ?", (session_id,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        return SessionRow(
            session_id=str(row["session_id"]),
            content_bundle_hash=str(row["content_bundle_hash"]),
            deployment_id=str(row["deployment_id"]),
            active=bool(row["active"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
        )

    def resume_bundle(
        self, session_id: str, registry: BundleRegistry
    ) -> ContentBundleRow:
        session = self.get(session_id)
        if session is None or not session.active:
            raise KeyError(f"session not found or inactive: {session_id}")
        row = registry.get(session.content_bundle_hash)
        if row is None:
            raise LookupError(
                f"pinned bundle missing: {session.content_bundle_hash}"
            )
        return row

    def active_bundle_hashes(self) -> set[str]:
        cur = self._conn.execute(
            "SELECT content_bundle_hash FROM session WHERE active = 1"
        )
        return {str(r[0]) for r in cur.fetchall()}

    def deactivate(self, session_id: str) -> None:
        self._conn.execute(
            "UPDATE session SET active = 0, updated_at = ? WHERE session_id = ?",
            (_utc_now().isoformat(), session_id),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


class PostgresSessionStore:
    """PostgreSQL session store with content_bundle_hash pin."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        psycopg, _pg_errors = _require_psycopg()
        self._url = database_url
        self._conn = conn if conn is not None else psycopg.connect(database_url)
        self._conn.execute(_PG_SESSION_SCHEMA)
        self._conn.commit()

    def create(
        self,
        *,
        session_id: str,
        content_bundle_hash: str,
        deployment_id: str,
    ) -> SessionRow:
        now = _utc_now()
        self._conn.execute(
            """
            INSERT INTO session (
              session_id, content_bundle_hash, deployment_id, active, created_at, updated_at
            ) VALUES (%s, %s, %s, TRUE, %s, %s)
            """,
            (session_id, content_bundle_hash, deployment_id, now, now),
        )
        self._conn.commit()
        row = self.get(session_id)
        assert row is not None
        return row

    def get(self, session_id: str) -> SessionRow | None:
        row = self._conn.execute(
            "SELECT * FROM session WHERE session_id = %s", (session_id,)
        ).fetchone()
        if row is None:
            return None
        created = row["created_at"]
        updated = row["updated_at"]
        return SessionRow(
            session_id=str(row["session_id"]),
            content_bundle_hash=str(row["content_bundle_hash"]),
            deployment_id=str(row["deployment_id"]),
            active=bool(row["active"]),
            created_at=created
            if isinstance(created, datetime)
            else datetime.fromisoformat(str(created)),
            updated_at=updated
            if isinstance(updated, datetime)
            else datetime.fromisoformat(str(updated)),
        )

    def resume_bundle(
        self, session_id: str, registry: BundleRegistry
    ) -> ContentBundleRow:
        session = self.get(session_id)
        if session is None or not session.active:
            raise KeyError(f"session not found or inactive: {session_id}")
        row = registry.get(session.content_bundle_hash)
        if row is None:
            raise LookupError(
                f"pinned bundle missing: {session.content_bundle_hash}"
            )
        return row

    def active_bundle_hashes(self) -> set[str]:
        rows = self._conn.execute(
            "SELECT content_bundle_hash FROM session WHERE active = TRUE"
        ).fetchall()
        return {str(r[0]) for r in rows}

    def deactivate(self, session_id: str) -> None:
        self._conn.execute(
            "UPDATE session SET active = FALSE, updated_at = %s WHERE session_id = %s",
            (_utc_now(), session_id),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


def open_session_store(database_url: str) -> SessionStore:
    url = (database_url or "").strip()
    if not url or url in {":memory:", "memory"}:
        return MemorySessionStore()
    if url.startswith("sqlite:///"):
        return SqliteSessionStore(url.removeprefix("sqlite:///"))
    if url.startswith("sqlite://"):
        path = url.removeprefix("sqlite://")
        return SqliteSessionStore(path or ":memory:")
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        return PostgresSessionStore(url)
    return SqliteSessionStore(url)
