"""Postgres-backed runtime stores — dedupe replay, turn lock, tokens, history, gateway attempts."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterator

from aibridge.action_tokens import (
    ActionTokenStore,
    TokenActionKind,
    TokenConflictError,
    TokenNotFoundError,
    TokenOwnershipError,
    TokenRecord,
    TokenRecordState,
    hash_token,
    mint_opaque_token,
)
from aibridge.db import connect_postgres, require_psycopg
from aibridge.history import HistoryStore


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class StoredChannelResponse:
    http_status: int
    body: dict[str, Any]


class PostgresEventDedupeStore:
    """Event dedupe with stored HTTP status + body (transport replay)."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        self._url = database_url
        self._owned = conn  # optional injected (fakes / single-thread tests)
        self._pg_errors = require_psycopg()[1]

    def _connect(self) -> Any:
        if self._owned is not None:
            return self._owned
        return connect_postgres(self._url)

    def _close_if_ephemeral(self, conn: Any) -> None:
        if self._owned is None:
            conn.close()

    def get(self, channel: str, event_id: str) -> StoredChannelResponse | None:
        conn = self._connect()
        try:
            row = conn.execute(
                """
                SELECT http_status, response_body FROM event_dedupe
                WHERE channel = %s AND event_id = %s
                """,
                (channel, event_id),
            ).fetchone()
            if row is None:
                return None
            body = row["response_body"]
            if isinstance(body, str):
                body = json.loads(body)
            return StoredChannelResponse(
                http_status=int(row["http_status"]), body=dict(body)
            )
        finally:
            self._close_if_ephemeral(conn)

    def get_or_create(
        self,
        channel: str,
        event_id: str,
        factory: Callable[[], dict[str, Any]],
        *,
        http_status: int = 200,
    ) -> tuple[dict[str, Any], bool]:
        """Insert-once under PK; concurrent losers replay stored body."""
        existing = self.get(channel, event_id)
        if existing is not None:
            return dict(existing.body), False
        body = dict(factory())
        conn = self._connect()
        try:
            try:
                conn.execute(
                    """
                    INSERT INTO event_dedupe (channel, event_id, http_status, response_body)
                    VALUES (%s, %s, %s, %s::jsonb)
                    """,
                    (channel, event_id, http_status, json.dumps(body)),
                )
                conn.commit()
                return dict(body), True
            except self._pg_errors.UniqueViolation:
                conn.rollback()
                again = self.get(channel, event_id)
                assert again is not None
                return dict(again.body), False
        finally:
            self._close_if_ephemeral(conn)

    def store_response(
        self,
        channel: str,
        event_id: str,
        *,
        http_status: int,
        body: dict[str, Any],
    ) -> None:
        conn = self._connect()
        try:
            conn.execute(
                """
                INSERT INTO event_dedupe (channel, event_id, http_status, response_body)
                VALUES (%s, %s, %s, %s::jsonb)
                ON CONFLICT (channel, event_id) DO UPDATE
                  SET http_status = EXCLUDED.http_status,
                      response_body = EXCLUDED.response_body
                """,
                (channel, event_id, http_status, json.dumps(body)),
            )
            conn.commit()
        finally:
            self._close_if_ephemeral(conn)

    def side_effect_count(self, channel: str, event_id: str) -> int:
        return 1 if self.get(channel, event_id) is not None else 0

    def clear(self) -> None:
        conn = self._connect()
        try:
            conn.execute("DELETE FROM event_dedupe")
            conn.commit()
        finally:
            self._close_if_ephemeral(conn)

    def close(self) -> None:
        if self._owned is not None:
            self._owned.close()


class PostgresTurnLock:
    """Database-backed one active turn per session."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        self._url = database_url
        self._owned = conn
        self._pg_errors = require_psycopg()[1]

    def _connect(self) -> Any:
        if self._owned is not None:
            return self._owned
        return connect_postgres(self._url)

    def _close_if_ephemeral(self, conn: Any) -> None:
        if self._owned is None:
            conn.close()

    @contextmanager
    def hold(self, session_id: str) -> Iterator[None]:
        holder = uuid.uuid4().hex
        hold_conn = self._connect()
        try:
            hold_conn.execute(
                """
                INSERT INTO session_turn_lock (session_id, holder, acquired_at)
                VALUES (%s, %s, %s)
                """,
                (session_id, holder, _utc_now()),
            )
            hold_conn.commit()
        except self._pg_errors.UniqueViolation:
            hold_conn.rollback()
            self._close_if_ephemeral(hold_conn)
            raise RuntimeError(f"turn already active: {session_id}") from None
        try:
            yield
        finally:
            try:
                hold_conn.execute(
                    "DELETE FROM session_turn_lock WHERE session_id = %s AND holder = %s",
                    (session_id, holder),
                )
                hold_conn.commit()
            finally:
                self._close_if_ephemeral(hold_conn)

    def is_active(self, session_id: str) -> bool:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT 1 FROM session_turn_lock WHERE session_id = %s",
                (session_id,),
            ).fetchone()
            return row is not None
        finally:
            self._close_if_ephemeral(conn)

    def close(self) -> None:
        if self._owned is not None:
            self._owned.close()


class PostgresActionTokenStore:
    """Postgres action token hash store — unique token_hash."""

    def __init__(
        self,
        database_url: str,
        *,
        ttl_seconds: int = 15 * 60,
        conn: Any | None = None,
    ) -> None:
        self.ttl_seconds = ttl_seconds
        self._conn = connect_postgres(database_url, conn=conn)

    def issue(
        self,
        *,
        action: TokenActionKind,
        session_id: str,
        user_id: str,
        chat_id: str,
        deployment_id: str,
        revision: int,
        expected_state: str,
        draft_hash: str | None = None,
        nonce: str | None = None,
        now: float | None = None,
    ) -> tuple[str, TokenRecord]:
        import time

        ts = time.time() if now is None else now
        raw = mint_opaque_token()
        th = hash_token(raw)
        rec = TokenRecord(
            token_hash=th,
            action=action,
            session_id=session_id,
            user_id=user_id,
            chat_id=chat_id,
            deployment_id=deployment_id,
            revision=revision,
            issued_at=ts,
            expires_at=ts + self.ttl_seconds,
            expected_state=expected_state,
            draft_hash=draft_hash,
            nonce=nonce or uuid.uuid4().hex,
        )
        self._conn.execute(
            """
            INSERT INTO action_token (
              token_hash, action, session_id, user_id, chat_id, deployment_id,
              revision, issued_at, expires_at, expected_state, state,
              operation_id, draft_hash, nonce
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                rec.token_hash,
                rec.action.value,
                rec.session_id,
                rec.user_id,
                rec.chat_id,
                rec.deployment_id,
                rec.revision,
                rec.issued_at,
                rec.expires_at,
                rec.expected_state,
                rec.state.value,
                rec.operation_id,
                rec.draft_hash,
                rec.nonce,
            ),
        )
        self._conn.commit()
        return raw, rec

    def _row_to_record(self, row: dict[str, Any]) -> TokenRecord:
        return TokenRecord(
            token_hash=str(row["token_hash"]),
            action=TokenActionKind(str(row["action"])),
            session_id=str(row["session_id"]),
            user_id=str(row["user_id"]),
            chat_id=str(row["chat_id"]),
            deployment_id=str(row["deployment_id"]),
            revision=int(row["revision"]),
            issued_at=float(row["issued_at"]),
            expires_at=float(row["expires_at"]),
            expected_state=str(row["expected_state"]),
            state=TokenRecordState(str(row["state"])),
            operation_id=str(row["operation_id"]),
            draft_hash=row["draft_hash"],
            nonce=str(row["nonce"] or ""),
        )

    def peek(self, raw_token: str) -> TokenRecord:
        th = hash_token(raw_token)
        row = self._conn.execute(
            "SELECT * FROM action_token WHERE token_hash = %s", (th,)
        ).fetchone()
        if row is None:
            raise TokenNotFoundError()
        return self._row_to_record(row)

    def lookup(self, raw: str) -> TokenRecord:
        """ActionTokenStore-compatible alias."""
        return self.peek(raw)

    def verify_for_consume(
        self,
        raw: str,
        *,
        user_id: str,
        chat_id: str,
        now: float | None = None,
    ) -> TokenRecord:
        import time

        rec = self.lookup(raw)
        if rec.user_id != user_id or rec.chat_id != chat_id:
            raise TokenOwnershipError()
        ts = time.time() if now is None else now
        if rec.state is TokenRecordState.CONSUMED:
            raise TokenConflictError("Token already consumed")
        if rec.state is TokenRecordState.INVALIDATED:
            raise TokenConflictError("Token invalidated")
        if ts > rec.expires_at:
            raise TokenConflictError("Token expired")
        return rec

    def consume(
        self,
        raw_token: str,
        *,
        user_id: str | None = None,
        chat_id: str | None = None,
        now: float | None = None,
    ) -> TokenRecord:
        """Mark pending token consumed.

        With user_id/chat_id: verify ownership (story-09 store tests).
        Without: ActionTokenStore-compatible path after verify_for_consume.
        """
        import time

        ts = time.time() if now is None else now
        if user_id is not None and chat_id is not None:
            rec = self.verify_for_consume(
                raw_token, user_id=user_id, chat_id=chat_id, now=ts
            )
        else:
            rec = self.lookup(raw_token)
            if rec.state is not TokenRecordState.PENDING:
                raise TokenConflictError("Token not pending")
            if ts > rec.expires_at:
                raise TokenConflictError("Token expired")
        cur = self._conn.execute(
            """
            UPDATE action_token SET state = %s
            WHERE token_hash = %s AND state = %s
            """,
            (TokenRecordState.CONSUMED.value, rec.token_hash, TokenRecordState.PENDING.value),
        )
        self._conn.commit()
        if cur.rowcount != 1:
            raise TokenConflictError()
        rec.state = TokenRecordState.CONSUMED
        return rec

    def invalidate_session_revision(
        self, session_id: str, revision: int | None = None
    ) -> int:
        if revision is None:
            cur = self._conn.execute(
                """
                UPDATE action_token SET state = %s
                WHERE session_id = %s AND state = %s
                """,
                (
                    TokenRecordState.INVALIDATED.value,
                    session_id,
                    TokenRecordState.PENDING.value,
                ),
            )
        else:
            cur = self._conn.execute(
                """
                UPDATE action_token SET state = %s
                WHERE session_id = %s AND revision = %s AND state = %s
                """,
                (
                    TokenRecordState.INVALIDATED.value,
                    session_id,
                    revision,
                    TokenRecordState.PENDING.value,
                ),
            )
        self._conn.commit()
        return int(cur.rowcount or 0)

    def close(self) -> None:
        self._conn.close()


class PostgresHistoryStore:
    """Postgres conversation history keyed by session_id + seq."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        self._conn = connect_postgres(database_url, conn=conn)

    def append(self, session_id: str, item: dict[str, Any]) -> None:
        row = self._conn.execute(
            "SELECT COALESCE(MAX(seq), -1) AS m FROM conversation_history WHERE session_id = %s",
            (session_id,),
        ).fetchone()
        nxt = int(row["m"]) + 1
        self._conn.execute(
            """
            INSERT INTO conversation_history (session_id, seq, item)
            VALUES (%s, %s, %s::jsonb)
            """,
            (session_id, nxt, json.dumps(item)),
        )
        self._conn.commit()

    def list_items(self, session_id: str) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            """
            SELECT item FROM conversation_history
            WHERE session_id = %s ORDER BY seq
            """,
            (session_id,),
        ).fetchall()
        out: list[dict[str, Any]] = []
        for r in rows:
            item = r["item"]
            if isinstance(item, str):
                item = json.loads(item)
            out.append(dict(item))
        return out

    def replace(self, session_id: str, items: list[dict[str, Any]]) -> None:
        self._conn.execute(
            "DELETE FROM conversation_history WHERE session_id = %s", (session_id,)
        )
        for i, item in enumerate(items):
            self._conn.execute(
                """
                INSERT INTO conversation_history (session_id, seq, item)
                VALUES (%s, %s, %s::jsonb)
                """,
                (session_id, i, json.dumps(item)),
            )
        self._conn.commit()

    def clear(self, session_id: str) -> None:
        self._conn.execute(
            "DELETE FROM conversation_history WHERE session_id = %s", (session_id,)
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


class GatewayAttemptStore:
    """At most one gateway attempt per (session_id, revision)."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        self._conn = connect_postgres(database_url, conn=conn)
        self._pg_errors = require_psycopg()[1]

    def create_executing(self, *, session_id: str, revision: int) -> None:
        now = _utc_now()
        try:
            self._conn.execute(
                """
                INSERT INTO gateway_attempt (session_id, revision, status, created_at, updated_at)
                VALUES (%s, %s, 'executing', %s, %s)
                """,
                (session_id, revision, now, now),
            )
            self._conn.commit()
        except self._pg_errors.UniqueViolation:
            self._conn.rollback()
            raise RuntimeError(
                f"gateway attempt already exists for {session_id}@{revision}"
            ) from None

    def set_outcome(self, *, session_id: str, revision: int, outcome: str) -> None:
        self._conn.execute(
            """
            UPDATE gateway_attempt
            SET status = %s, outcome = %s, updated_at = %s
            WHERE session_id = %s AND revision = %s
            """,
            (outcome, outcome, _utc_now(), session_id, revision),
        )
        self._conn.commit()

    def get(self, *, session_id: str, revision: int) -> dict[str, Any] | None:
        return self._conn.execute(
            """
            SELECT * FROM gateway_attempt
            WHERE session_id = %s AND revision = %s
            """,
            (session_id, revision),
        ).fetchone()

    def list_executing(self) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            """
            SELECT * FROM gateway_attempt
            WHERE status = 'executing'
            ORDER BY created_at ASC
            """
        ).fetchall()
        return list(rows or [])

    def close(self) -> None:
        self._conn.close()


class PostgresConfirmSessionStore:
    """Persist confirm session state JSON (no silent memory in production)."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        self._conn = connect_postgres(database_url, conn=conn)

    def upsert(self, *, session_id: str, user_id: str, chat_id: str, state: dict[str, Any]) -> None:
        self._conn.execute(
            """
            INSERT INTO confirm_session (session_id, user_id, chat_id, state_json, updated_at)
            VALUES (%s, %s, %s, %s::jsonb, %s)
            ON CONFLICT (session_id) DO UPDATE SET
              user_id = EXCLUDED.user_id,
              chat_id = EXCLUDED.chat_id,
              state_json = EXCLUDED.state_json,
              updated_at = EXCLUDED.updated_at
            """,
            (session_id, user_id, chat_id, json.dumps(state), _utc_now()),
        )
        self._conn.commit()

    def get(self, session_id: str) -> dict[str, Any] | None:
        row = self._conn.execute(
            "SELECT * FROM confirm_session WHERE session_id = %s", (session_id,)
        ).fetchone()
        if row is None:
            return None
        state = row["state_json"]
        if isinstance(state, str):
            state = json.loads(state)
        return {
            "session_id": row["session_id"],
            "user_id": row["user_id"],
            "chat_id": row["chat_id"],
            "state": dict(state),
        }

    def get_by_principal(self, *, user_id: str, chat_id: str) -> dict[str, Any] | None:
        row = self._conn.execute(
            """
            SELECT * FROM confirm_session
            WHERE user_id = %s AND chat_id = %s
            ORDER BY updated_at DESC
            LIMIT 1
            """,
            (user_id, chat_id),
        ).fetchone()
        if row is None:
            return None
        state = row["state_json"]
        if isinstance(state, str):
            state = json.loads(state)
        return {
            "session_id": row["session_id"],
            "user_id": row["user_id"],
            "chat_id": row["chat_id"],
            "state": dict(state),
        }

    def close(self) -> None:
        self._conn.close()


def register_session_call(*, conn: Any, session_id: str, call_id: str) -> None:
    """Unique (session_id, call_id) — fail closed on duplicate."""
    _psycopg, pg_errors, _ = require_psycopg()
    try:
        conn.execute(
            """
            INSERT INTO session_call (session_id, call_id) VALUES (%s, %s)
            """,
            (session_id, call_id),
        )
        conn.commit()
    except pg_errors.UniqueViolation:
        conn.rollback()
        raise RuntimeError(f"duplicate call_id for session: {session_id}/{call_id}") from None


# Keep in-process ActionTokenStore import used by confirm — PG store is optional wire.
_ = (ActionTokenStore, HistoryStore, field)
