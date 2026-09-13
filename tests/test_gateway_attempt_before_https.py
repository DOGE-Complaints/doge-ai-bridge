"""G-02 — GatewayAttempt create+commit before HTTPS; fail-closed on duplicate."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aibridge.confirm import ConfirmationGuard, ConfirmSession
from aibridge.confirm_fsm import SessionState
from aibridge.db import is_postgres_url
from aibridge.gateway import (
    GatewayExecutor,
    GatewayOutcome,
    RawHttpResponse,
    RecordingGatewayTransport,
)
from aibridge.migrate import apply_migrations
from aibridge.pg_runtime import GatewayAttemptStore

PGDATA = Path(__file__).resolve().parents[1] / ".pgdata-test"
PGPORT = "55432"
DISPOSABLE_URL = (
    f"postgresql://aibridge@/aibridge_test?host={PGDATA}&port={PGPORT}"
)


def _pg_available() -> bool:
    if not PGDATA.is_dir():
        return False
    try:
        from aibridge.db import connect_postgres

        conn = connect_postgres(DISPOSABLE_URL)
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _pg_available(),
    reason="disposable Postgres (.pgdata-test) not running",
)


@pytest.fixture()
def pg_url() -> str:
    assert is_postgres_url(DISPOSABLE_URL)
    apply_migrations(DISPOSABLE_URL)
    from aibridge.db import connect_postgres

    conn = connect_postgres(DISPOSABLE_URL)
    conn.execute("TRUNCATE gateway_attempt CASCADE")
    conn.commit()
    conn.close()
    return DISPOSABLE_URL


def _ok_201() -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": "d1"}, "trace_id": "t1"}).encode()
    return RawHttpResponse(status_code=201, body=body)


def test_attempt_committed_before_https_and_outcome_after(pg_url: str) -> None:
    attempts = GatewayAttemptStore(pg_url)
    calls: list[str] = []

    class OrderTransport(RecordingGatewayTransport):
        def request(self, *a: object, **k: object) -> RawHttpResponse:  # type: ignore[no-untyped-def]
            row = attempts.get(session_id="sess-g02", revision=1)
            assert row is not None, "attempt row must exist before HTTPS"
            assert row["status"] == "executing"
            calls.append("https")
            return super().request(*a, **k)

    transport = OrderTransport(scripted=[_ok_201()])
    guard = ConfirmationGuard(
        executor=GatewayExecutor(
            transport=transport,
            origin="https://gateway.example",
            gateway_bearer="tok",
            dry_run=False,
        ),
        gateway_attempts=attempts,
    )
    sess = ConfirmSession(
        session_id="sess-g02",
        user_id="u",
        chat_id="c",
        deployment_id="local",
        state=SessionState.EXECUTING,
        revision=1,
        gateway_authorized=True,
        frozen_tool_intent={"x": 1},
    )
    result = guard.call_gateway(sess, body={"x": 1})
    assert calls == ["https"]
    assert result.outcome is GatewayOutcome.STASHED
    row = attempts.get(session_id="sess-g02", revision=1)
    assert row is not None
    assert row["outcome"] == GatewayOutcome.STASHED.value
    attempts.close()


def test_duplicate_attempt_blocks_second_https(pg_url: str) -> None:
    attempts = GatewayAttemptStore(pg_url)
    transport = RecordingGatewayTransport(scripted=[_ok_201(), _ok_201()])
    guard = ConfirmationGuard(
        executor=GatewayExecutor(
            transport=transport,
            origin="https://gateway.example",
            gateway_bearer="tok",
            dry_run=False,
        ),
        gateway_attempts=attempts,
    )
    sess = ConfirmSession(
        session_id="sess-dup",
        user_id="u",
        chat_id="c",
        deployment_id="local",
        state=SessionState.EXECUTING,
        revision=2,
        gateway_authorized=True,
        frozen_tool_intent={"x": 1},
    )
    guard.call_gateway(sess, body={"x": 1})
    assert len(transport.calls) == 1
    with pytest.raises(RuntimeError, match="already exists"):
        guard.call_gateway(sess, body={"x": 1})
    assert len(transport.calls) == 1  # no second HTTPS
    attempts.close()
