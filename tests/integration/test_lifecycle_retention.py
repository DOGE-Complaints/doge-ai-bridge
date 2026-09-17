"""STORY-AIBRIDGE-31 — LIFE-001…012 restart / lifecycle / retention (integration).

Fixture-driven. Memory session store simulates PG restart when disposable PG absent.
LIFE-009/010 characterization capture-first. No live Telegram.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from aibridge.action_tokens import ActionTokenStore
from aibridge.app import create_app
from aibridge.bundle_gc import gc_unreferenced_bundles
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import SessionState
from aibridge.content import load_content_bundle
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import (
    GatewayExecutor,
    GatewayOutcome,
    RawHttpResponse,
    RecordingGatewayTransport,
)
from aibridge.history import HistoryStore
from aibridge.interview import default_recording_engine
from aibridge.pg_runtime import (
    GatewayAttemptStore,
    PostgresActionTokenStore,
    PostgresConfirmSessionStore,
    PostgresHistoryStore,
)
from aibridge.privacy_retention import SessionActivityClock, TOMBSTONE_ITEM
from aibridge.registry import MemoryBundleRegistry
from aibridge.responses_client import RecordingResponsesClient
from aibridge.sessions import MemorySessionStore

import pytest

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402
from story13_e2e_helpers import (  # noqa: E402
    DISPOSABLE_URL,
    pg_available,
    rebuild_app_same_pg,
    truncate_pg,
)

STORY = "STORY-AIBRIDGE-31-qa-restart-lifecycle-retention"
LIFE_IDS = {f"LIFE-{i:03d}" for i in range(1, 13)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)
CONTENT = _TESTS_ROOT / "fixtures" / "content"
WIRE_OAS = _TESTS_ROOT.parents[0] / "docs" / "openapi" / "story-intake-actions.openapi.yaml"

CHANNEL = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

FIXTURE_NAMES = [
    ("settings", "life-shutting-down"),
    ("channel", "life-turns-private"),
    ("spies", "life-restart-interview"),
    ("spies", "life-restart-pending-token"),
    ("spies", "life-restart-consumed-token"),
    ("spies", "life-restart-executing-unknown"),
    ("spies", "life-session-ttl-expire"),
    ("spies", "life-bundle-retained"),
    ("spies", "life-bundle-gc-eligible"),
    ("spies", "life-after-cancelled"),
    ("spies", "life-after-stashed"),
    ("spies", "life-edit-from-unknown"),
    ("spies", "life-deployment-mismatch"),
]


def _hash(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


class _MemConfirmSessions:
    """In-memory confirm_sessions seam — simulates PG persist across guard rebuild."""

    def __init__(self) -> None:
        self._by_id: dict[str, dict[str, Any]] = {}
        self._by_principal: dict[tuple[str, str], str] = {}

    def upsert(
        self, *, session_id: str, user_id: str, chat_id: str, state: dict[str, Any]
    ) -> None:
        row = {
            "session_id": session_id,
            "user_id": user_id,
            "chat_id": chat_id,
            "state": dict(state),
            "updated_at": datetime.now(timezone.utc),
        }
        self._by_id[session_id] = row
        self._by_principal[(user_id, chat_id)] = session_id

    def get(self, session_id: str) -> dict[str, Any] | None:
        row = self._by_id.get(session_id)
        return dict(row) if row else None

    def get_by_principal(self, *, user_id: str, chat_id: str) -> dict[str, Any] | None:
        sid = self._by_principal.get((user_id, chat_id))
        return self.get(sid) if sid else None


class _FakeGwAttemptConn:
    """Minimal conn for GatewayAttemptStore create/list/set/get without live PG."""

    def __init__(self) -> None:
        self._rows: dict[tuple[str, int], dict[str, Any]] = {}
        self._last: dict[str, Any] | None = None
        self._last_many: list[dict[str, Any]] = []

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> _FakeGwAttemptConn:
        sql_l = " ".join(sql.lower().split())
        if "insert into gateway_attempt" in sql_l and params is not None:
            key = (str(params[0]), int(params[1]))
            self._rows[key] = {
                "session_id": params[0],
                "revision": int(params[1]),
                "status": "executing",
                "outcome": None,
                "created_at": params[2],
                "updated_at": params[3],
            }
            self._last = None
        elif "update gateway_attempt" in sql_l and params is not None:
            key = (str(params[3]), int(params[4]))
            row = self._rows.get(key)
            if row is not None:
                row["status"] = params[0]
                row["outcome"] = params[1]
                row["updated_at"] = params[2]
            self._last = None
        elif (
            "select * from gateway_attempt" in sql_l
            and "where session_id" in sql_l
            and params is not None
        ):
            self._last = self._rows.get((str(params[0]), int(params[1])))
        elif "status = 'executing'" in sql_l or 'status = "executing"' in sql_l:
            self._last_many = [
                dict(r) for r in self._rows.values() if r.get("status") == "executing"
            ]
            self._last = None
        return self

    def fetchone(self) -> dict[str, Any] | None:
        return self._last

    def fetchall(self) -> list[dict[str, Any]]:
        return list(self._last_many)

    def commit(self) -> None:
        return None

    def rollback(self) -> None:
        return None

    def close(self) -> None:
        return None


class _FakeLifePgConn:
    """Minimal conn for PostgresConfirmSessionStore + PostgresActionTokenStore + history."""

    def __init__(self) -> None:
        self._confirm: dict[str, dict[str, Any]] = {}
        self._by_principal: dict[tuple[str, str], str] = {}
        self._tokens: dict[str, dict[str, Any]] = {}
        self._history: dict[str, list[dict[str, Any]]] = {}
        self._last: dict[str, Any] | None = None
        self._last_many: list[dict[str, Any]] = []
        self.rowcount = 0

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> _FakeLifePgConn:
        sql_l = " ".join(sql.lower().split())
        self.rowcount = 0
        self._last = None
        self._last_many = []
        if "insert into confirm_session" in sql_l and params is not None:
            sid, uid, cid, state_json, updated = params
            state = json.loads(state_json) if isinstance(state_json, str) else state_json
            row = {
                "session_id": sid,
                "user_id": uid,
                "chat_id": cid,
                "state_json": state,
                "updated_at": updated,
            }
            self._confirm[str(sid)] = row
            self._by_principal[(str(uid), str(cid))] = str(sid)
        elif "from confirm_session" in sql_l and "where session_id" in sql_l and params is not None:
            row = self._confirm.get(str(params[0]))
            self._last = row
        elif (
            "from confirm_session" in sql_l
            and "user_id" in sql_l
            and params is not None
            and len(params) >= 2
        ):
            sid = self._by_principal.get((str(params[0]), str(params[1])))
            self._last = self._confirm.get(sid) if sid else None
        elif "delete from confirm_session" in sql_l and params is not None:
            sid = str(params[0])
            row = self._confirm.pop(sid, None)
            if row is not None:
                self._by_principal.pop((row["user_id"], row["chat_id"]), None)
                self.rowcount = 1
        elif "insert into action_token" in sql_l and params is not None:
            th = str(params[0])
            self._tokens[th] = {
                "token_hash": params[0],
                "action": params[1],
                "session_id": params[2],
                "user_id": params[3],
                "chat_id": params[4],
                "deployment_id": params[5],
                "revision": params[6],
                "issued_at": params[7],
                "expires_at": params[8],
                "expected_state": params[9],
                "state": params[10],
                "operation_id": params[11],
                "draft_hash": params[12],
                "nonce": params[13],
            }
        elif "select * from action_token" in sql_l and params is not None:
            self._last = self._tokens.get(str(params[0]))
        elif "update action_token set state" in sql_l and params is not None:
            if "token_hash" in sql_l and len(params) >= 3:
                new_state, th, old_state = params[0], str(params[1]), params[2]
                row = self._tokens.get(th)
                if row is not None and row["state"] == old_state:
                    row["state"] = new_state
                    self.rowcount = 1
                    self._last = row
            elif "revision" in sql_l and len(params) >= 4:
                new_state, sid, rev, old_state = (
                    params[0],
                    str(params[1]),
                    int(params[2]),
                    params[3],
                )
                n = 0
                for row in self._tokens.values():
                    if (
                        row["session_id"] == sid
                        and int(row["revision"]) == rev
                        and row["state"] == old_state
                    ):
                        row["state"] = new_state
                        n += 1
                self.rowcount = n
            elif len(params) >= 3:
                new_state, sid, old_state = params[0], str(params[1]), params[2]
                n = 0
                for row in self._tokens.values():
                    if row["session_id"] == sid and row["state"] == old_state:
                        row["state"] = new_state
                        n += 1
                self.rowcount = n
        elif "coalesce(max(seq)" in sql_l and params is not None:
            items = self._history.get(str(params[0]), [])
            self._last = {"m": len(items) - 1}
        elif "insert into conversation_history" in sql_l and params is not None:
            sid, seq, item = str(params[0]), int(params[1]), params[2]
            parsed = json.loads(item) if isinstance(item, str) else item
            self._history.setdefault(sid, [])
            while len(self._history[sid]) <= seq:
                self._history[sid].append({})
            self._history[sid][seq] = {"item": parsed}
        elif "from conversation_history" in sql_l and "order by seq" in sql_l and params:
            sid = str(params[0])
            self._last_many = [
                {"item": r["item"]} for r in self._history.get(sid, []) if r
            ]
        elif "delete from conversation_history" in sql_l and params is not None:
            self._history.pop(str(params[0]), None)
            self.rowcount = 1
        return self

    def fetchone(self) -> dict[str, Any] | None:
        return self._last

    def fetchall(self) -> list[dict[str, Any]]:
        return list(self._last_many)

    def commit(self) -> None:
        return None

    def rollback(self) -> None:
        return None

    def close(self) -> None:
        return None


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL,
        DOGESTONIA_API_BEARER_TOKEN=GATEWAY,
        DATABASE_URL="memory",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def _stash_raw() -> RawHttpResponse:
    return RawHttpResponse(
        status_code=201,
        body=json.dumps(
            {"data": {"draft_id": "draft-life-31"}, "trace_id": "trace-life-31"}
        ).encode(),
    )


def _guard(
    *,
    confirm_sessions: Any | None = None,
    tokens: Any | None = None,
    activity_clock: SessionActivityClock | None = None,
    gateway_attempts: Any | None = None,
    history: Any | None = None,
    dry_run: bool = True,
    raise_on_call: Exception | None = None,
    deployment_id: str = "local",
) -> tuple[ConfirmationGuard, RecordingGatewayTransport, Any]:
    transport = RecordingGatewayTransport(scripted=[_stash_raw()])
    if raise_on_call is not None:
        transport.raise_on_call = raise_on_call
    tok = tokens or ActionTokenStore(ttl_seconds=3600)
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY,
        channel_bearer=CHANNEL,
        dry_run=dry_run,
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    g = ConfirmationGuard(
        executor=ex,
        tokens=tok,
        confirm_sessions=confirm_sessions,
        activity_clock=activity_clock,
        gateway_attempts=gateway_attempts,
        history=history,
    )
    return g, transport, tok


def _rebuild_guard(
    *,
    confirm_sessions: Any,
    tokens: Any,
    activity_clock: SessionActivityClock | None = None,
    gateway_attempts: Any | None = None,
    history: Any | None = None,
) -> ConfirmationGuard:
    """Simulate process restart: empty in-memory maps, shared persist seams."""
    g, _t, _tok = _guard(
        confirm_sessions=confirm_sessions,
        tokens=tokens,
        activity_clock=activity_clock,
        gateway_attempts=gateway_attempts,
        history=history,
    )
    return g


def test_fixtures_promoted_hash_eq_and_matrix_coverage() -> None:
    seen: set[str] = set()
    for cluster, name in FIXTURE_NAMES:
        env = load_fixture(cluster, name)
        assert env["schema_version"] == "1.0"
        assert STORY in env["story_keys"]
        seen.update(env["matrix_ids"])
        pkg = PKG_FIXTURES / f"{name}.json"
        copy = _TESTS_ROOT / "fixtures" / cluster / f"{name}.json"
        assert pkg.is_file() and copy.is_file()
        assert _hash(pkg) == _hash(copy)
    assert LIFE_IDS.issubset(seen)
    for name in ("life-after-cancelled", "life-after-stashed"):
        assert "characterization" in load_fixture("spies", name)["notes"]


def test_life_001_shutting_down_503_retryable() -> None:
    env = load_fixture("settings", "life-shutting-down")
    ch = load_fixture("channel", "life-turns-private")
    expect = env["payload"]["expect_channel"]
    app = create_app(
        settings=_settings(),
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    client = TestClient(app)
    app.state.accepting_traffic = False
    r = client.post(
        ch["payload"]["path"],
        json=ch["payload"]["body"],
        headers={"Authorization": f"Bearer {CHANNEL}"},
    )
    assert r.status_code == expect["http_status"]
    body = r.json()
    assert body["error"]["code"] == expect["error_code"]
    assert body["error"]["retryable"] is expect["retryable"]
    if env["payload"].get("healthz_ok"):
        assert client.get("/healthz").status_code == 200


def test_life_002_restart_interview_restored_no_duplicate() -> None:
    """LIFE-002 + G-02: restore + spy openai + history across rebuild."""
    spy = load_fixture("spies", "life-restart-interview")["payload"]
    store = _MemConfirmSessions()
    tokens = ActionTokenStore(ttl_seconds=3600)
    hist = HistoryStore()
    openai = RecordingResponsesClient()
    g1, transport, _ = _guard(confirm_sessions=store, tokens=tokens, history=hist)
    sess = g1.get_or_create_session(user_id="31", chat_id="31-002")
    g1.offer_interpretation_confirm(sess.session_id)
    g1._persist_session(sess)  # noqa: SLF001 — channel persist seam after offer
    hist.append(sess.session_id, {"role": "user", "content": "life-002-narrative"})
    # Simulate one pre-restart OpenAI turn already recorded (interview in flight).
    openai.calls.append({"model": "gpt-test", "input": "pre-restart"})
    calls_at_restart = len(openai.calls)
    assert sess.state is SessionState.AWAITING_INTERPRETATION_CONFIRM
    sid = sess.session_id
    rev = sess.revision

    g2 = _rebuild_guard(confirm_sessions=store, tokens=tokens, history=hist)
    sess2 = g2.get_or_create_session(user_id="31", chat_id="31-002")
    assert sess2.session_id == sid
    assert sess2.state is SessionState.AWAITING_INTERPRETATION_CONFIRM
    assert sess2.revision == rev
    assert len(transport.calls) == spy["gateway_call_count"]
    # G-02: no OpenAI replay on restore; history persists across rebuild.
    assert (
        len(openai.calls) - calls_at_restart
        == spy["openai_call_count_after_restart_replay"]
    )
    items = hist.list_items(sid)
    assert items and items[0]["content"] == "life-002-narrative"


def test_g01_life_002_pg_confirm_store_rebuild() -> None:
    """G-01 Preference A: PostgresConfirmSessionStore fake-conn + rebuild."""
    spy = load_fixture("spies", "life-restart-interview")["payload"]
    fake = _FakeLifePgConn()
    confirm = PostgresConfirmSessionStore("postgresql://fake/aibridge_test", conn=fake)
    tokens = ActionTokenStore(ttl_seconds=3600)
    g1, transport, _ = _guard(confirm_sessions=confirm, tokens=tokens)
    sess = g1.get_or_create_session(user_id="31", chat_id="31-002-pg")
    g1.offer_interpretation_confirm(sess.session_id)
    g1._persist_session(sess)  # noqa: SLF001
    sid, rev = sess.session_id, sess.revision

    g2 = _rebuild_guard(confirm_sessions=confirm, tokens=tokens)
    sess2 = g2.get_or_create_session(user_id="31", chat_id="31-002-pg")
    assert sess2.session_id == sid
    assert sess2.state is SessionState.AWAITING_INTERPRETATION_CONFIRM
    assert sess2.revision == rev
    assert len(transport.calls) == spy["gateway_call_count"]
    confirm.close()


def test_g01_life_003_pg_token_pending_usable() -> None:
    """G-01 Preference A: PostgresActionTokenStore pending survives rebuild."""
    spy = load_fixture("spies", "life-restart-pending-token")["payload"]
    fake = _FakeLifePgConn()
    confirm = PostgresConfirmSessionStore("postgresql://fake/aibridge_test", conn=fake)
    tokens = PostgresActionTokenStore(
        "postgresql://fake/aibridge_test", ttl_seconds=3600, conn=fake
    )
    g1, _t, _ = _guard(confirm_sessions=confirm, tokens=tokens)
    sess = g1.get_or_create_session(user_id="31", chat_id="31-003-pg")
    acts = g1.offer_interpretation_confirm(sess.session_id)
    g1._persist_session(sess)  # noqa: SLF001
    tok = next(a["token"] for a in acts if a["style"] == "success")

    g2 = _rebuild_guard(confirm_sessions=confirm, tokens=tokens)
    r = g2.consume_action_token(tok, user_id="31", chat_id="31-003-pg")
    assert r["ok"] is spy["token_usable_after_restart"]
    assert r["http_status"] == spy["http_status"]
    tokens.close()
    confirm.close()


def test_g01_life_004_pg_token_consumed_stays() -> None:
    """G-01 Preference A: PostgresActionTokenStore consumed stays consumed."""
    spy = load_fixture("spies", "life-restart-consumed-token")["payload"]
    fake = _FakeLifePgConn()
    confirm = PostgresConfirmSessionStore("postgresql://fake/aibridge_test", conn=fake)
    tokens = PostgresActionTokenStore(
        "postgresql://fake/aibridge_test", ttl_seconds=3600, conn=fake
    )
    g1, _t, _ = _guard(confirm_sessions=confirm, tokens=tokens)
    sess = g1.get_or_create_session(user_id="31", chat_id="31-004-pg")
    acts = g1.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    assert g1.consume_action_token(tok, user_id="31", chat_id="31-004-pg")["ok"] is True

    g2 = _rebuild_guard(confirm_sessions=confirm, tokens=tokens)
    r = g2.consume_action_token(tok, user_id="31", chat_id="31-004-pg")
    assert r["ok"] is spy["token_usable_after_restart"]
    assert r["http_status"] == spy["http_status"]
    tokens.close()
    confirm.close()


def test_g02_life_002_pg_history_restore() -> None:
    """G-02: PostgresHistoryStore fake-conn history survives rebuild."""
    fake = _FakeLifePgConn()
    confirm = PostgresConfirmSessionStore("postgresql://fake/aibridge_test", conn=fake)
    hist = PostgresHistoryStore("postgresql://fake/aibridge_test", conn=fake)
    tokens = ActionTokenStore(ttl_seconds=3600)
    g1, _t, _ = _guard(confirm_sessions=confirm, tokens=tokens, history=hist)
    sess = g1.get_or_create_session(user_id="31", chat_id="31-002-hist")
    g1.offer_interpretation_confirm(sess.session_id)
    g1._persist_session(sess)  # noqa: SLF001
    hist.append(sess.session_id, {"role": "user", "content": "pg-hist-life-002"})
    sid = sess.session_id

    g2 = _rebuild_guard(confirm_sessions=confirm, tokens=tokens, history=hist)
    sess2 = g2.get_or_create_session(user_id="31", chat_id="31-002-hist")
    assert sess2.session_id == sid
    items = hist.list_items(sid)
    assert items and items[0]["content"] == "pg-hist-life-002"
    hist.close()
    confirm.close()


@pytest.mark.skipif(not pg_available(), reason="disposable Postgres not running")
def test_g01_life_rebuild_app_same_pg_live() -> None:
    """G-01 live path: rebuild_app_same_pg when disposable PG present."""
    from story13_e2e_helpers import build_e2e_harness, text_openai_payload

    truncate_pg()
    h = build_e2e_harness(openai_scripted=[text_openai_payload()])
    assert h.guard.confirm_sessions is not None
    assert isinstance(h.guard.tokens, PostgresActionTokenStore)
    sess = h.guard.get_or_create_session(user_id="31", chat_id="31-live-pg")
    h.guard.offer_interpretation_confirm(sess.session_id)
    h.guard._persist_session(sess)  # noqa: SLF001
    sid, rev = sess.session_id, sess.revision

    h2 = rebuild_app_same_pg(h)
    sess2 = h2.guard.get_or_create_session(user_id="31", chat_id="31-live-pg")
    assert sess2.session_id == sid
    assert sess2.state is SessionState.AWAITING_INTERPRETATION_CONFIRM
    assert sess2.revision == rev
    assert h2.settings.database_url == DISPOSABLE_URL


def test_life_003_restart_pending_token_usable() -> None:
    spy = load_fixture("spies", "life-restart-pending-token")["payload"]
    store = _MemConfirmSessions()
    tokens = ActionTokenStore(ttl_seconds=3600)
    g1, _t, _ = _guard(confirm_sessions=store, tokens=tokens)
    sess = g1.get_or_create_session(user_id="31", chat_id="31-003")
    acts = g1.offer_interpretation_confirm(sess.session_id)
    g1._persist_session(sess)  # noqa: SLF001
    tok = next(a["token"] for a in acts if a["style"] == "success")

    g2 = _rebuild_guard(confirm_sessions=store, tokens=tokens)
    r = g2.consume_action_token(tok, user_id="31", chat_id="31-003")
    assert r["ok"] is spy["token_usable_after_restart"]
    assert r["http_status"] == spy["http_status"]


def test_life_004_restart_consumed_token_stays_consumed() -> None:
    spy = load_fixture("spies", "life-restart-consumed-token")["payload"]
    store = _MemConfirmSessions()
    tokens = ActionTokenStore(ttl_seconds=3600)
    g1, _t, _ = _guard(confirm_sessions=store, tokens=tokens)
    sess = g1.get_or_create_session(user_id="31", chat_id="31-004")
    acts = g1.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    assert g1.consume_action_token(tok, user_id="31", chat_id="31-004")["ok"] is True

    g2 = _rebuild_guard(confirm_sessions=store, tokens=tokens)
    r = g2.consume_action_token(tok, user_id="31", chat_id="31-004")
    assert r["ok"] is spy["token_usable_after_restart"]
    assert r["http_status"] == spy["http_status"]


def test_life_005_restart_executing_unknown_no_resend() -> None:
    spy = load_fixture("spies", "life-restart-executing-unknown")["payload"]
    fake = _FakeGwAttemptConn()
    attempts = GatewayAttemptStore("postgresql://fake/aibridge_test", conn=fake)
    store = _MemConfirmSessions()
    tokens = ActionTokenStore(ttl_seconds=3600)
    g1, transport, _ = _guard(
        confirm_sessions=store, tokens=tokens, gateway_attempts=attempts, dry_run=False
    )
    sess = g1.get_or_create_session(user_id="31", chat_id="31-005")
    sess.state = SessionState.EXECUTING
    sess.revision = 1
    sess.gateway_authorized = True
    g1._persist_session(sess)  # noqa: SLF001
    attempts.create_executing(session_id=sess.session_id, revision=1)

    g2 = _rebuild_guard(
        confirm_sessions=store, tokens=tokens, gateway_attempts=attempts
    )
    n = g2.recover_all_executing_attempts()
    assert n == 1
    sess2 = g2.get_session(sess.session_id)
    assert sess2 is not None
    assert sess2.state.value == spy["state"]
    assert sess2.last_outcome == spy["outcome"]
    assert g2.send_blocked_for_revision(sess2) is spy["send_blocked_same_revision"]
    assert len(transport.calls) == spy["gateway_call_count"]
    attempts.close()


def test_life_006_session_ttl_expire_new_session() -> None:
    spy = load_fixture("spies", "life-session-ttl-expire")["payload"]
    clock = SessionActivityClock(ttl_seconds=10)
    hist = HistoryStore()
    tokens = ActionTokenStore(ttl_seconds=3600)
    g, _t, _ = _guard(tokens=tokens, activity_clock=clock, history=hist)
    sess = g.get_or_create_session(user_id="31", chat_id="31-006")
    old_sid = sess.session_id
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    hist.append(old_sid, {"role": "user", "content": "SECRET_LIFE_006"})
    clock.seed(old_sid, time.time() - 1000)

    sess2 = g.get_or_create_session(user_id="31", chat_id="31-006")
    assert spy["expect_new_session"] is True
    assert sess2.session_id != old_sid
    assert sess2.state is SessionState.INTERVIEWING
    items = hist.list_items(old_sid)
    assert any(i.get("type") == TOMBSTONE_ITEM["type"] for i in items)
    assert "SECRET_LIFE_006" not in str(items)
    r = g.consume_action_token(tok, user_id="31", chat_id="31-006")
    assert (r.get("ok") is True) is spy["old_token_usable"]


def test_life_007_bundle_retained_while_active() -> None:
    spy = load_fixture("spies", "life-bundle-retained")["payload"]
    reg = MemoryBundleRegistry()
    sessions = MemorySessionStore()
    bundle = load_content_bundle(
        instructions_dir=CONTENT / "instructions",
        manifest_path=CONTENT / "instructions.manifest.json",
        source_commit="life-31",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=CONTENT / "pack" / "payload.schema.json",
    )
    row = reg.register_once(bundle)
    sessions.create(
        session_id="life-alive",
        content_bundle_hash=row.bundle_hash,
        deployment_id="n1",
    )
    now = datetime.now(timezone.utc) + timedelta(days=30)
    deleted = gc_unreferenced_bundles(reg, sessions, grace_seconds=3600, now=now)
    assert deleted == spy["deleted_hashes"]
    assert (reg.get(row.bundle_hash) is not None) is spy["bundle_present"]


def test_life_008_bundle_gc_after_grace() -> None:
    spy = load_fixture("spies", "life-bundle-gc-eligible")["payload"]
    reg = MemoryBundleRegistry()
    sessions = MemorySessionStore()
    bundle = load_content_bundle(
        instructions_dir=CONTENT / "instructions",
        manifest_path=CONTENT / "instructions.manifest.json",
        source_commit="life-31-gc",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=CONTENT / "pack" / "payload.schema.json",
    )
    row = reg.register_once(bundle)
    sessions.create(
        session_id="life-gone",
        content_bundle_hash=row.bundle_hash,
        deployment_id="n1",
    )
    sessions.deactivate("life-gone")
    late = row.verified_at + timedelta(seconds=3601)
    deleted = gc_unreferenced_bundles(reg, sessions, grace_seconds=3600, now=late)
    assert (row.bundle_hash in deleted) is spy["expect_deleted"]
    assert reg.get(row.bundle_hash) is None


def test_life_009_after_cancelled_characterization() -> None:
    """Characterization: capture resume behavior after cancelled (no product invent)."""
    env = load_fixture("spies", "life-after-cancelled")
    assert "characterization" in env["notes"]
    spy = env["payload"]
    g, _t, _ = _guard()
    sess = g.get_or_create_session(user_id="31", chat_id="31-009")
    acts = g.offer_interpretation_confirm(sess.session_id)
    cancel = next(a["token"] for a in acts if a["style"] == "danger")
    g.consume_action_token(cancel, user_id="31", chat_id="31-009")
    assert sess.state.value == spy["prior_state"]
    # Capture-first: same principal returns existing terminal session (current product).
    again = g.get_or_create_session(user_id="31", chat_id="31-009")
    captured = {
        "same_session_id": again.session_id == sess.session_id,
        "state": again.state.value,
    }
    assert spy["capture"] is True
    assert captured["same_session_id"] is True
    assert captured["state"] == SessionState.CANCELLED.value


def test_life_010_after_stashed_characterization() -> None:
    """Characterization: capture resume behavior after stashed (no product invent)."""
    env = load_fixture("spies", "life-after-stashed")
    assert "characterization" in env["notes"]
    spy = env["payload"]
    g, transport, _ = _guard(dry_run=False)
    sess = g.get_or_create_session(user_id="31", chat_id="31-010")
    g.consume_action_token(
        next(
            a["token"]
            for a in g.offer_interpretation_confirm(sess.session_id)
            if a["style"] == "success"
        ),
        user_id="31",
        chat_id="31-010",
    )
    g.set_frozen_tool_intent(sess.session_id, {"title": "pothole"})
    send_tok = next(
        a["token"] for a in g.offer_send_confirm(sess.session_id) if a["style"] == "primary"
    )
    r = g.consume_action_token(send_tok, user_id="31", chat_id="31-010")
    assert r["outcome"] == GatewayOutcome.STASHED.value
    assert sess.state.value == spy["prior_state"]
    again = g.get_or_create_session(user_id="31", chat_id="31-010")
    captured = {
        "same_session_id": again.session_id == sess.session_id,
        "state": again.state.value,
        "gateway_calls": len(transport.calls),
    }
    assert spy["capture"] is True
    assert captured["same_session_id"] is True
    assert captured["state"] == SessionState.STASHED.value


def test_life_011_edit_from_unknown_new_revision() -> None:
    spy = load_fixture("spies", "life-edit-from-unknown")["payload"]
    g, transport, _ = _guard(dry_run=False, raise_on_call=TimeoutError("timeout"))
    sess = g.get_or_create_session(user_id="31", chat_id="31-011")
    g.consume_action_token(
        next(
            a["token"]
            for a in g.offer_interpretation_confirm(sess.session_id)
            if a["style"] == "success"
        ),
        user_id="31",
        chat_id="31-011",
    )
    g.set_frozen_tool_intent(sess.session_id, {"title": "x"})
    send_tok = next(
        a["token"] for a in g.offer_send_confirm(sess.session_id) if a["style"] == "primary"
    )
    r = g.consume_action_token(send_tok, user_id="31", chat_id="31-011")
    assert r["outcome"] == GatewayOutcome.UNKNOWN_OUTCOME.value
    old_rev = sess.revision
    assert g.send_blocked_for_revision(sess) is True
    g.apply_edit(sess.session_id)
    assert sess.revision == old_rev + spy["revision_delta"]
    assert sess.unknown_outcome_revision is None
    assert g.send_blocked_for_revision(sess) is spy["send_blocked_old_revision"]
    # New interview path allowed
    acts = g.offer_interpretation_confirm(sess.session_id)
    assert acts
    assert len(transport.calls) == 1


def test_life_012_deployment_mismatch_rejects_token() -> None:
    spy = load_fixture("spies", "life-deployment-mismatch")["payload"]
    g, _t, _ = _guard()
    sess = g.get_or_create_session(
        user_id="31", chat_id="31-012", deployment_id="deploy-a"
    )
    g.consume_action_token(
        next(
            a["token"]
            for a in g.offer_interpretation_confirm(sess.session_id)
            if a["style"] == "success"
        ),
        user_id="31",
        chat_id="31-012",
    )
    g.set_frozen_tool_intent(sess.session_id, {"title": "x"}, draft_hash="h1")
    send_tok = next(
        a["token"] for a in g.offer_send_confirm(sess.session_id) if a["style"] == "primary"
    )
    sess.deployment_id = "deploy-b"
    r = g.consume_action_token(send_tok, user_id="31", chat_id="31-012")
    assert r["ok"] is False
    assert r["http_status"] == spy["http_status"]
    assert r["code"] == spy["error_code"]
    assert "deployment" in r["message"].lower()
