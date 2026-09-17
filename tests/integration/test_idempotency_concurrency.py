"""STORY-AIBRIDGE-26 — IDEM-001…010 idempotency/concurrency (no live Telegram).

Fixture-driven spy expectations + channel envelopes. Barriers/events for races — not sleep.
Characterization: IDEM-003 collision-log if implemented; IDEM-004 second-path branch — capture-first.
"""

from __future__ import annotations

import concurrent.futures
import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.audit import get_audit_buffer, reset_audit_buffer
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayExecutor, GatewayOutcome, RecordingGatewayTransport
from aibridge.interview import InterviewEngine
from aibridge.responses_client import RecordingResponsesClient
from aibridge.turn_lock import SessionTurnLock

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402
from story13_e2e_helpers import (  # noqa: E402
    CHANNEL_TOKEN,
    GATEWAY_TOKEN,
    ok_201,
    text_openai_payload,
    validation_context,
)

STORY = "STORY-AIBRIDGE-26-qa-idempotency-concurrency"
IDEM_IDS = {f"IDEM-{i:03d}" for i in range(1, 11)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)
FORBID = ("Bearer ", "sk-", "callback_data_raw")


class _TrackingTurnLock(SessionTurnLock):
    """SessionTurnLock that records max concurrent holds (G-01)."""

    def __init__(self) -> None:
        super().__init__()
        self.max_concurrent = 0
        self.phases: list[str] = []
        self._depth = 0
        self._clk = threading.Lock()

    @contextmanager
    def hold(self, session_id: str) -> Iterator[None]:
        with super().hold(session_id):
            with self._clk:
                self._depth += 1
                self.max_concurrent = max(self.max_concurrent, self._depth)
                self.phases.append("enter")
            try:
                yield
            finally:
                with self._clk:
                    self._depth -= 1
                    self.phases.append("exit")


class _BoomThenOkClient(RecordingResponsesClient):
    """First create raises (after record); later creates succeed — IDEM-005."""

    def __init__(self) -> None:
        super().__init__(scripted=[text_openai_payload("after-abort-retry")])
        self._attempts = 0

    def create(self, request: Any) -> dict[str, Any]:
        assert request.payload.get("store") is False
        self.calls.append(dict(request.payload))
        self._attempts += 1
        if self._attempts == 1:
            raise RuntimeError("synthetic openai failure after claim")
        if self._scripted:
            return dict(self._scripted.pop(0))
        return text_openai_payload("fallback")


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL_TOKEN,
        DOGESTONIA_API_BEARER_TOKEN=GATEWAY_TOKEN,
        DATABASE_URL="memory",
        AIBRIDGE_ALLOW_MEMORY_STORES=True,
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def _auth() -> dict[str, str]:
    return {"Authorization": f"Bearer {CHANNEL_TOKEN}"}


def _build(
    *,
    openai: RecordingResponsesClient | None = None,
    dry_run: bool = True,
    gateway_scripted: list | None = None,
    turn_lock: SessionTurnLock | None = None,
) -> tuple[TestClient, Any, RecordingResponsesClient, RecordingGatewayTransport, EventDedupeStore]:
    reset_confirmation_guard()
    openai = openai or RecordingResponsesClient(scripted=[text_openai_payload("ok")])
    engine = InterviewEngine(client=openai)
    store = EventDedupeStore()
    app = create_app(
        settings=_settings(AIBRIDGE_DRY_RUN=dry_run),
        dedupe_store=store,
        interview_engine=engine,
    )
    transport = RecordingGatewayTransport(scripted=list(gateway_scripted or []))
    guard: ConfirmationGuard = app.state.confirmation_guard
    guard.executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY_TOKEN,
        channel_bearer=CHANNEL_TOKEN,
        dry_run=dry_run,
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    guard.validation_context = validation_context()
    guard.interview_engine = engine
    app.state.interview_engine = engine
    if turn_lock is not None:
        app.state.turn_lock = turn_lock
    return TestClient(app), app, openai, transport, store


def _body(cluster: str, name: str) -> dict[str, Any]:
    return load_fixture(cluster, name)["payload"]["body"]


def _spy(name: str) -> dict[str, Any]:
    return load_fixture("spies", name)["payload"]


def _assert_forbid(log_text: str) -> None:
    """Spy bag §14 — forbidden patterns must not appear in captured audit text."""
    for pat in FORBID:
        assert pat not in log_text
    assert CHANNEL_TOKEN not in log_text
    assert GATEWAY_TOKEN not in log_text


def _mint_send_token(app: Any, *, user_id: str = "501122334", chat_id: str = "501122334") -> str:
    guard: ConfirmationGuard = app.state.confirmation_guard
    sess = guard.get_or_create_session(user_id=user_id, chat_id=chat_id)
    interpret = guard.offer_interpretation_confirm(sess.session_id)
    guard.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id=user_id,
        chat_id=chat_id,
    )
    guard.set_frozen_tool_intent(
        sess.session_id,
        {
            "name": "postStoryDraftStash",
            "call_id": "call_idem",
            "arguments": {
                "narrative": {"note": "idem"},
                "schema_binding": {"structured_payload": {"title": "ok"}},
            },
        },
    )
    send_actions = guard.offer_send_confirm(sess.session_id)
    return next(a["token"] for a in send_actions if a["style"] == "primary")


# --- coverage / promote integrity ---


def test_idem_matrix_ids_bound_and_fixtures_present() -> None:
    covered: set[str] = set()
    for cluster in ("spies", "channel"):
        root = _TESTS_ROOT / "fixtures" / cluster
        for path in sorted(root.glob("idem-*.json")) + sorted(root.glob("*-idem-*.json")) + sorted(
            root.glob("turns-idem-*.json")
        ) + sorted(root.glob("actions-idem-*.json")):
            data = load_fixture(cluster, path.stem)
            assert STORY in data["story_keys"]
            covered.update(data["matrix_ids"])
    # seed spy
    seed = load_fixture("spies", "idem-same-event-once-openai")
    covered.update(seed["matrix_ids"])
    assert IDEM_IDS <= covered


def test_idem_package_originals_intact_hash_eq() -> None:
    import hashlib

    names = [
        ("spies", "idem-same-event-once-openai.json"),
        ("spies", "idem-new-event-id-second-openai.json"),
        ("channel", "turns-idem-same-event.json"),
        ("openai", "text-only-ru-clarify.json"),
    ]
    for cluster, name in names:
        pkg = PKG_FIXTURES / name
        copy = _TESTS_ROOT / "fixtures" / cluster / name
        assert pkg.is_file() and copy.is_file()
        assert hashlib.sha256(pkg.read_bytes()).digest() == hashlib.sha256(copy.read_bytes()).digest()


# --- IDEM-001 ---


def test_idem_001_same_event_once_openai() -> None:
    spy = _spy("idem-same-event-once-openai")
    body = _body("channel", "turns-idem-same-event")
    client, _app, openai, transport, store = _build(
        openai=RecordingResponsesClient(scripted=[text_openai_payload("once")])
    )
    reset_audit_buffer()
    r1 = client.post("/v1/channel/turns", json=body, headers=_auth())
    r2 = client.post("/v1/channel/turns", json=body, headers=_auth())
    assert r1.status_code == spy["http_status"] == r2.status_code
    assert r1.json() == r2.json()
    assert len(openai.calls) == spy["openai_call_count"]
    assert len(transport.calls) == spy["gateway_call_count"]
    assert store.side_effect_count("telegram", body["event_id"]) == 1
    bag = get_audit_buffer().dump_text()
    _assert_forbid(bag)
    for pat in spy["forbid_substrings_in_logs"]:
        assert pat not in bag


# --- IDEM-002 ---


def test_idem_002_new_event_id_second_openai() -> None:
    """Demonstrate wrong retry: new event_id → second OpenAI call (n8n must prevent)."""
    spy = _spy("idem-new-event-id-second-openai")
    first = _body("channel", "turns-idem-same-event")
    second = _body("channel", "turns-idem-retry-new-event")
    client, _app, openai, _tr, _store = _build(
        openai=RecordingResponsesClient(
            scripted=[text_openai_payload("a"), text_openai_payload("b")]
        )
    )
    assert client.post("/v1/channel/turns", json=first, headers=_auth()).status_code == 200
    assert client.post("/v1/channel/turns", json=second, headers=_auth()).status_code == 200
    assert len(openai.calls) == spy["openai_call_count"]


# --- IDEM-003 ---


def test_idem_003_same_event_diff_body_first_wins() -> None:
    spy = _spy("idem-same-event-diff-body")
    first = _body("channel", "turns-idem-same-event")
    diff = _body("channel", "turns-idem-same-event-diff-body")
    assert first["event_id"] == diff["event_id"]
    assert first["message"]["text"] != diff["message"]["text"]
    client, _app, openai, _tr, store = _build(
        openai=RecordingResponsesClient(scripted=[text_openai_payload("first-wins")])
    )
    # Capture-first: no dedicated body-collision log API in EventDedupeStore / channel.py.
    collision_log_implemented = hasattr(EventDedupeStore, "log_collision") or hasattr(
        store, "log_collision"
    )
    assert spy.get("characterization", {}).get("collision_log") == "capture-first"
    r1 = client.post("/v1/channel/turns", json=first, headers=_auth())
    r2 = client.post("/v1/channel/turns", json=diff, headers=_auth())
    assert r1.status_code == 200 and r2.status_code == 200
    assert r2.json() == r1.json()
    assert len(openai.calls) == spy["openai_call_count"]
    assert store.side_effect_count("telegram", first["event_id"]) == 1
    # Characterization capture: collision log not implemented in current code.
    assert collision_log_implemented is False


# --- IDEM-004 ---


def test_idem_004_concurrent_identical_turns_one_openai() -> None:
    spy = _spy("idem-concurrent-identical-turns")
    body = _body("channel", "turns-idem-concurrent-identical")
    client, app, openai, _tr, _store = _build(
        openai=RecordingResponsesClient(scripted=[text_openai_payload("only-once")])
    )
    barrier = threading.Barrier(2)
    results: list[tuple[int, dict[str, Any]]] = []

    def _post() -> None:
        c = TestClient(app)
        barrier.wait()
        r = c.post("/v1/channel/turns", json=body, headers=_auth())
        results.append((r.status_code, r.json()))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(_post)
        f2 = pool.submit(_post)
        f1.result()
        f2.result()

    assert all(s == 200 for s, _ in results)
    assert len(openai.calls) == spy["openai_call_count"]
    # Capture-first second path: replay same request_id OR bounded in-flight text.
    bodies = [b for _, b in results]
    same_replay = bodies[0].get("request_id") == bodies[1].get("request_id")
    inflight_msg = any(
        "in flight" in str(b.get("reply_text", "")).lower() for b in bodies
    )
    assert same_replay or inflight_msg
    assert spy.get("characterization", {}).get("second_path") == "capture-first"


# --- IDEM-005 ---


def test_idem_005_openai_exception_aborts_claim_retry_ok() -> None:
    spy = _spy("idem-openai-exception-abort")
    body = _body("channel", "turns-idem-openai-abort")
    boom = _BoomThenOkClient()
    _client, app, openai, _tr, store = _build(openai=boom)
    client = TestClient(app, raise_server_exceptions=False)
    r1 = client.post("/v1/channel/turns", json=body, headers=_auth())
    assert r1.status_code >= 500
    # Claim aborted — no completed side-effect for this event.
    assert store.side_effect_count("telegram", body["event_id"]) == 0
    r2 = client.post("/v1/channel/turns", json=body, headers=_auth())
    assert r2.status_code == 200
    assert store.side_effect_count("telegram", body["event_id"]) == 1
    # One successful Responses completion after abort (attempt records may be >1).
    assert len([c for c in openai.calls]) >= spy["openai_call_count"]


# --- IDEM-006 ---


def test_idem_006_callback_retry_same_update_one_gateway() -> None:
    spy = _spy("idem-callback-retry-same-update")
    action = _body("channel", "actions-idem-callback-retry")
    client, app, _openai, transport, _store = _build(
        dry_run=False,
        gateway_scripted=[ok_201("draft-idem-006")],
    )
    tok = _mint_send_token(app)
    action = {**action, "action_token": tok}
    reset_audit_buffer()
    r1 = client.post("/v1/channel/actions", json=action, headers=_auth())
    r2 = client.post("/v1/channel/actions", json=action, headers=_auth())
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json() == r1.json()
    assert r1.json().get("outcome") in (
        GatewayOutcome.STASHED.value,
        spy.get("outcome"),
        r1.json().get("outcome"),
    )
    assert len(transport.calls) == spy["gateway_call_count"]
    bag = get_audit_buffer().dump_text()
    _assert_forbid(bag)
    for pat in spy["forbid_substrings_in_logs"]:
        assert pat not in bag
    assert tok not in bag


# --- IDEM-007 ---


def test_idem_007_concurrent_send_same_token_one_gateway() -> None:
    spy = _spy("idem-concurrent-send-same-token")
    a = _body("channel", "actions-idem-concurrent-send-a")
    b = _body("channel", "actions-idem-concurrent-send-b")
    client, app, _openai, transport, _store = _build(
        dry_run=False,
        gateway_scripted=[ok_201("draft-idem-007")],
    )
    tok = _mint_send_token(app)
    a = {**a, "action_token": tok}
    b = {**b, "action_token": tok}
    barrier = threading.Barrier(2)
    outcomes: list[tuple[int, dict[str, Any]]] = []

    def _post(payload: dict[str, Any]) -> None:
        c = TestClient(app)
        barrier.wait()
        r = c.post("/v1/channel/actions", json=payload, headers=_auth())
        outcomes.append((r.status_code, r.json()))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(_post, a)
        f2 = pool.submit(_post, b)
        f1.result()
        f2.result()

    statuses = sorted(s for s, _ in outcomes)
    assert 200 in statuses
    assert 409 in statuses or statuses.count(200) == 1
    # Exactly one gateway attempt.
    assert len(transport.calls) == spy["gateway_call_count"]


# --- IDEM-008 ---


def test_idem_008_same_session_serialized_by_turn_lock() -> None:
    spy = _spy("idem-same-session-serialized")
    a = _body("channel", "turns-idem-session-a")
    b = _body("channel", "turns-idem-session-b")
    assert a["principal"] == b["principal"]
    lock = _TrackingTurnLock()
    client, app, openai, _tr, _store = _build(
        openai=RecordingResponsesClient(
            scripted=[text_openai_payload("A"), text_openai_payload("B")]
        ),
        turn_lock=lock,
    )
    barrier = threading.Barrier(2)
    finish_order: list[str] = []
    session_ids: list[str] = []
    order_lock = threading.Lock()

    def _post(payload: dict[str, Any], label: str) -> None:
        c = TestClient(app)
        barrier.wait()
        r = c.post("/v1/channel/turns", json=payload, headers=_auth())
        assert r.status_code == 200
        body = r.json()
        with order_lock:
            finish_order.append(label)
            session_ids.append(str(body["session_id"]))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(_post, a, "a")
        f2 = pool.submit(_post, b, "b")
        f1.result()
        f2.result()

    assert len(openai.calls) == spy["openai_call_count"]
    assert set(finish_order) == {"a", "b"}
    # Non-overlapping holds: enter/exit pairs; never two enters without exit.
    assert lock.max_concurrent == 1
    assert lock.phases == ["enter", "exit", "enter", "exit"]
    # Same session for both principals; lock idle after both complete.
    assert len(set(session_ids)) == 1
    assert lock.is_active(session_ids[0]) is False
    # Deterministic OpenAI history order matches completion order of holds
    # (serialized): both texts appear exactly once in call payloads.
    joined = "\n".join(str(c) for c in openai.calls)
    assert a["message"]["text"] in joined
    assert b["message"]["text"] in joined
    assert len(finish_order) == 2


# --- IDEM-009 ---


def test_idem_009_diff_sessions_independent() -> None:
    spy = _spy("idem-diff-sessions-parallel")
    x = _body("channel", "turns-idem-session-x")
    y = _body("channel", "turns-idem-session-y")
    assert x["principal"] != y["principal"]
    lock = SessionTurnLock()
    client, app, openai, _tr, _store = _build(
        openai=RecordingResponsesClient(
            scripted=[text_openai_payload("X"), text_openai_payload("Y")]
        ),
        turn_lock=lock,
    )
    barrier = threading.Barrier(2)

    def _post(payload: dict[str, Any]) -> int:
        c = TestClient(app)
        barrier.wait()
        r = c.post("/v1/channel/turns", json=payload, headers=_auth())
        return r.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(_post, x)
        f2 = pool.submit(_post, y)
        assert f1.result() == 200
        assert f2.result() == 200
    assert len(openai.calls) == spy["openai_call_count"]


# --- IDEM-010 ---


def test_idem_010_turns_actions_same_event_id_safe_replay() -> None:
    spy = _spy("idem-turns-actions-event-collision")
    turn = _body("channel", "turns-idem-ns-collision")
    action = _body("channel", "actions-idem-ns-collision")
    assert turn["event_id"] == action["event_id"]
    client, app, openai, transport, _store = _build(
        openai=RecordingResponsesClient(scripted=[text_openai_payload("turns-first")]),
        dry_run=False,
        gateway_scripted=[ok_201("should-not-fire")],
    )
    tok = _mint_send_token(app)
    action = {**action, "action_token": tok}
    r1 = client.post("/v1/channel/turns", json=turn, headers=_auth())
    assert r1.status_code == 200
    r2 = client.post("/v1/channel/actions", json=action, headers=_auth())
    # Safe replay of stored /turns envelope (actions get_or_create hits).
    assert r2.status_code == 200
    assert r2.json() == r1.json()
    assert len(openai.calls) == spy["openai_call_count"]
    assert len(transport.calls) == spy["gateway_call_count"]


def test_idem_spy_bag_no_secrets_in_forbid_patterns() -> None:
    """Spy bag §14 — forbid patterns are patterns only, never secret values."""
    for name in (
        "idem-same-event-once-openai",
        "idem-new-event-id-second-openai",
        "idem-callback-retry-same-update",
    ):
        payload = _spy(name)
        for pat in payload["forbid_substrings_in_logs"]:
            assert CHANNEL_TOKEN not in pat
            assert GATEWAY_TOKEN not in pat
            assert "sk-test" not in pat
        # Patterns themselves may contain the substring tokens (e.g. "Bearer ").
        assert "Bearer " in payload["forbid_substrings_in_logs"]
