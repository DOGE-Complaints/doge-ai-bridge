"""STORY-AIBRIDGE-09 — migrations, constraints, replay, no memory fallback, races."""

from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from aibridge.action_tokens import TokenActionKind
from aibridge.db import assert_no_silent_memory_fallback, is_postgres_url
from aibridge.migrate import apply_migrations, current_migration_version, list_migration_files
from aibridge.pg_runtime import (
    GatewayAttemptStore,
    PostgresActionTokenStore,
    PostgresConfirmSessionStore,
    PostgresEventDedupeStore,
    PostgresHistoryStore,
    PostgresTurnLock,
    register_session_call,
)
from aibridge.registry import open_bundle_registry
from aibridge.sessions import open_session_store

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
    reason="disposable Postgres (.pgdata-test) not running — start via tests/helpers or local pg_ctl",
)


@pytest.fixture()
def pg_url() -> str:
    assert is_postgres_url(DISPOSABLE_URL)
    # Isolate schemas per test via truncate of app tables after migrate
    apply_migrations(DISPOSABLE_URL)
    from aibridge.db import connect_postgres

    conn = connect_postgres(DISPOSABLE_URL)
    for table in (
        "event_dedupe",
        "action_token",
        "session_call",
        "gateway_attempt",
        "session_turn_lock",
        "conversation_history",
        "confirm_session",
        "session",
        "content_bundle",
    ):
        conn.execute(f"TRUNCATE {table} CASCADE")
    conn.commit()
    conn.close()
    return DISPOSABLE_URL


def test_migrations_files_exist_and_apply(pg_url: str) -> None:
    files = list_migration_files()
    assert any(p.name.startswith("0001_") for p in files)
    # second apply is no-op
    again = apply_migrations(pg_url)
    assert again == []
    from aibridge.db import connect_postgres

    conn = connect_postgres(pg_url)
    ver = current_migration_version(conn)
    conn.close()
    assert ver is not None
    assert ver.startswith("0001_")


def test_boot_schema_flag_defaults_off_for_open_helpers(pg_url: str) -> None:
    # ensure_schema=False is production path; tables already from migrations
    reg = open_bundle_registry(pg_url, allow_memory=False, ensure_schema=False)
    sessions = open_session_store(pg_url, allow_memory=False, ensure_schema=False)
    assert reg.list_hashes() == []
    sessions.close()
    reg.close()


def test_no_silent_memory_fallback_policy() -> None:
    with pytest.raises(RuntimeError, match="silent memory fallback"):
        assert_no_silent_memory_fallback(database_url="", allow_memory=False)
    with pytest.raises(RuntimeError, match="silent memory fallback"):
        open_session_store("", allow_memory=False)
    with pytest.raises(RuntimeError, match="silent memory fallback"):
        open_bundle_registry("sqlite:///:memory:", allow_memory=False)


def test_event_dedupe_unique_and_replay_after_reconnect(pg_url: str) -> None:
    store = PostgresEventDedupeStore(pg_url)
    body, created = store.get_or_create(
        "telegram", "e-1", lambda: {"request_id": "r1", "ok": True}, http_status=200
    )
    assert created is True
    body2, created2 = store.get_or_create(
        "telegram", "e-1", lambda: {"request_id": "SHOULD_NOT"}, http_status=200
    )
    assert created2 is False
    assert body2 == body
    store.close()

    # Restart / new connection — replay stored body (AC #3)
    store2 = PostgresEventDedupeStore(pg_url)
    replay = store2.get("telegram", "e-1")
    assert replay is not None
    assert replay.http_status == 200
    assert replay.body["request_id"] == "r1"
    store2.close()


def test_gateway_attempt_unique_per_revision(pg_url: str) -> None:
    g = GatewayAttemptStore(pg_url)
    g.create_executing(session_id="s1", revision=3)
    with pytest.raises(RuntimeError, match="already exists"):
        g.create_executing(session_id="s1", revision=3)
    g.set_outcome(session_id="s1", revision=3, outcome="stashed")
    row = g.get(session_id="s1", revision=3)
    assert row is not None
    assert row["status"] == "stashed"
    g.close()


def test_session_call_unique(pg_url: str) -> None:
    from aibridge.db import connect_postgres

    conn = connect_postgres(pg_url)
    register_session_call(conn=conn, session_id="s1", call_id="c1")
    with pytest.raises(RuntimeError, match="duplicate call_id"):
        register_session_call(conn=conn, session_id="s1", call_id="c1")
    conn.close()


def test_action_token_and_history_and_confirm(pg_url: str) -> None:
    tokens = PostgresActionTokenStore(pg_url)
    raw, rec = tokens.issue(
        action=TokenActionKind.CONFIRM_SEND,
        session_id="s1",
        user_id="u1",
        chat_id="c1",
        deployment_id="d1",
        revision=1,
        expected_state="awaiting_send_confirm",
    )
    assert tokens.peek(raw).token_hash == rec.token_hash
    consumed = tokens.consume(raw, user_id="u1", chat_id="c1")
    assert consumed.state.value == "consumed"
    tokens.close()

    hist = PostgresHistoryStore(pg_url)
    hist.append("s1", {"type": "message", "role": "user", "content": "hi"})
    assert hist.list_items("s1")[0]["content"] == "hi"
    hist.close()

    confirm = PostgresConfirmSessionStore(pg_url)
    confirm.upsert(
        session_id="s1", user_id="u1", chat_id="c1", state={"fsm": "interviewing"}
    )
    got = confirm.get("s1")
    assert got is not None
    assert got["state"]["fsm"] == "interviewing"
    confirm.close()


def test_turn_lock_concurrency_one_wins(pg_url: str) -> None:
    lock = PostgresTurnLock(pg_url)
    results: list[str] = []
    barrier = threading.Barrier(2)

    def worker(name: str) -> None:
        barrier.wait()
        try:
            with lock.hold("sess-race"):
                results.append(f"{name}:ok")
                # hold briefly so loser hits UniqueViolation
                import time

                time.sleep(0.05)
        except RuntimeError as exc:
            results.append(f"{name}:fail:{exc}")

    with ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(worker, "a")
        f2 = pool.submit(worker, "b")
        f1.result()
        f2.result()
    lock.close()
    oks = [r for r in results if r.endswith(":ok")]
    fails = [r for r in results if ":fail:" in r]
    assert len(oks) == 1
    assert len(fails) == 1


def test_event_dedupe_concurrency_constraints_win(pg_url: str) -> None:
    store = PostgresEventDedupeStore(pg_url)
    counter = {"n": 0}
    lock = threading.Lock()

    def factory() -> dict:
        with lock:
            counter["n"] += 1
            n = counter["n"]
        return {"n": n}

    barrier = threading.Barrier(2)

    def worker() -> tuple[dict, bool]:
        barrier.wait()
        return store.get_or_create("telegram", "race-e", factory, http_status=200)

    with ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(worker)
        f2 = pool.submit(worker)
        r1 = f1.result()
        r2 = f2.result()
    store.close()
    bodies = {json_dumpsish(r1[0]), json_dumpsish(r2[0])}
    assert len(bodies) == 1
    assert (r1[1] ^ r2[1]) is True  # exactly one created


def json_dumpsish(d: dict) -> str:
    import json

    return json.dumps(d, sort_keys=True)
