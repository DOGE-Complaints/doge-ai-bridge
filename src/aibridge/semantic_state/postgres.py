"""Postgres semantic store — table ``semantic_state`` (≠ conversation_history)."""

from __future__ import annotations

import json
from typing import Any

from aibridge.db import connect_postgres
from aibridge.semantic_state.models import SemanticStateSnapshot


class PostgresSemanticStateStore:
    """Same DB family as sessions; separate table from HistoryStore."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        self._conn = connect_postgres(database_url, conn=conn)

    def get(self, session_id: str) -> SemanticStateSnapshot:
        row = self._conn.execute(
            "SELECT payload FROM semantic_state WHERE session_id = %s",
            (session_id,),
        ).fetchone()
        if row is None:
            return SemanticStateSnapshot()
        payload = row["payload"]
        if isinstance(payload, str):
            payload = json.loads(payload)
        return SemanticStateSnapshot.from_dict(dict(payload))

    def put(self, session_id: str, snapshot: SemanticStateSnapshot) -> None:
        body = json.dumps(snapshot.to_dict())
        self._conn.execute(
            """
            INSERT INTO semantic_state (session_id, payload, updated_at)
            VALUES (%s, %s::jsonb, now())
            ON CONFLICT (session_id) DO UPDATE
              SET payload = EXCLUDED.payload,
                  updated_at = now()
            """,
            (session_id, body),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
