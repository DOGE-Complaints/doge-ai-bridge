"""STORY-AIBRIDGE-62 — semantic store + L13-3 Target A / Transition C.

Store ≠ HistoryStore / ≠ last_confirmed_state SSOT. No invent hash format.
OOS roles (63) / parity (64).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import IllegalTransitionError, SessionState
from aibridge.gateway import (
    GatewayExecutor,
    RecordingGatewayTransport,
    RawHttpResponse,
)
from aibridge.history import HistoryStore
from aibridge.interview import InterviewEngine
from aibridge.migrate import list_migration_files
from aibridge.semantic_state import (
    MemorySemanticStateStore,
    PostgresSemanticStateStore,
    SemanticStateService,
)
from aibridge.semantic_state.memory import MemorySemanticStateStore as MemCls
from aibridge.semantic_state.postgres import PostgresSemanticStateStore as PgCls

_REPO = Path(__file__).resolve().parents[1]
_DOC = _REPO / "docs" / "runtime-docs" / "09-semantic-state-store-invalidation.md"
_SEM_PKG = _REPO / "src" / "aibridge" / "semantic_state"
_HIST = _REPO / "src" / "aibridge" / "history.py"


def _ok_201() -> RawHttpResponse:
    body = json.dumps(
        {"data": {"draft_id": "draft-62"}, "trace_id": "trace-62"}
    ).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard_with_send_offered() -> tuple[ConfirmationGuard, object, str]:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-62",
        channel_bearer="ch-62",
        redirect_base="https://spa.example",
        transport=transport,
    )
    g = ConfirmationGuard(executor=executor)
    sess = g.get_or_create_session(user_id="u62", chat_id="c62")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="u62",
        chat_id="c62",
    )
    g.set_frozen_tool_intent(sess.session_id, {"arguments": {"t": 1}}, draft_hash="h62")
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    return g, sess, send_tok


# --- t01 boundary ---


def test_t01_semantic_store_home_not_history_or_last_confirmed() -> None:
    assert _SEM_PKG.is_dir()
    assert (_SEM_PKG / "memory.py").is_file()
    assert (_SEM_PKG / "postgres.py").is_file()
    assert (_SEM_PKG / "service.py").is_file()
    assert MemCls is not HistoryStore
    assert PgCls.__name__ != "PostgresHistoryStore"
    # last_confirmed_state lives on InterviewEngine — not semantic SSOT.
    assert "last_confirmed_state" in getattr(InterviewEngine, "__dataclass_fields__", {}) or hasattr(
        InterviewEngine, "last_confirmed_state"
    )
    # Field exists on engine type; store API must not be that map.
    src = (_REPO / "src" / "aibridge" / "interview.py").read_text(encoding="utf-8")
    assert "last_confirmed_state" in src
    store = MemorySemanticStateStore()
    assert not isinstance(store, HistoryStore)
    assert "last_confirmed_state" not in store.__dict__
    assert "semantic_state" in str(_SEM_PKG)
    assert "history.py" not in str(_SEM_PKG)


# --- t02 postgres logical classes / migration ---


def test_t02_migration_semantic_state_table_present() -> None:
    files = {p.name for p in list_migration_files()}
    assert "0002_semantic_state.sql" in files
    sql = (_REPO / "migrations" / "0002_semantic_state.sql").read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS semantic_state" in sql
    assert "CREATE TABLE IF NOT EXISTS conversation_history" not in sql
    assert "payload" in sql


def test_t02_memory_persists_logical_classes() -> None:
    svc = SemanticStateService(MemorySemanticStateStore())
    sid = "s62-t02"
    svc.set_phase(sid, "intake")
    svc.upsert_confirmed_fact(sid, "fact-a", fact_id="f1", ground_utterance_refs=("u1",))
    svc.add_hypothesis(sid, "maybe", hypothesis_id="h1")
    svc.add_gap(sid, "missing", gap_id="g1")
    svc.add_correction(sid, "fix-a", correction_id="c1")
    snap = svc.get(sid)
    assert snap.phase == "intake"
    assert snap.facts[0].text == "fact-a"
    assert snap.facts[0].ground_utterance_refs == ("u1",)
    assert snap.hypotheses[0].id == "h1"
    assert snap.gaps[0].id == "g1"
    assert snap.corrections[0].id == "c1"


# --- t03 AC-01 multi-turn harness ---


def test_t03_ac01_persist_across_turns_no_gpt_ui() -> None:
    store = MemorySemanticStateStore()
    svc = SemanticStateService(store)
    sid = "s62-t03"
    # Turn 1
    svc.upsert_confirmed_fact(sid, "citizen report", fact_id="f-turn1")
    # Simulate new service instance (next turn / process boundary within harness)
    svc2 = SemanticStateService(store)
    snap = svc2.get(sid)
    assert len(snap.facts) == 1
    assert snap.facts[0].id == "f-turn1"
    # Turn 2 append
    svc2.add_hypothesis(sid, "hypothesis-2")
    snap2 = SemanticStateService(store).get(sid)
    assert len(snap2.facts) == 1
    assert len(snap2.hypotheses) == 1


# --- t04 Target A meaning invalidate without EDIT ---


def test_t04_confirmed_fact_invalidates_without_telegram_edit() -> None:
    g, sess, send_tok = _guard_with_send_offered()
    pre_state = sess.state
    old_rev = sess.revision
    svc = SemanticStateService(
        MemorySemanticStateStore(),
        confirm_guard=g,
    )
    svc.upsert_confirmed_fact(sess.session_id, "meaning changed")
    assert sess.revision == old_rev + 1
    assert sess.gateway_authorized is False
    assert sess.frozen_tool_intent is None
    assert sess.state is pre_state  # no FSM EDIT
    bad = g.consume_action_token(send_tok, user_id="u62", chat_id="c62")
    assert bad["ok"] is False
    assert bad["http_status"] == 409


def test_t04_correction_invalidates_hypothesis_does_not() -> None:
    calls: list[tuple[str, str]] = []

    def _capture(sid: str, reason: str) -> None:
        calls.append((sid, reason))

    svc = SemanticStateService(
        MemorySemanticStateStore(),
        on_meaning_change=_capture,
    )
    sid = "s62-draft"
    svc.add_hypothesis(sid, "draft only")
    svc.add_gap(sid, "gap only")
    assert calls == []
    svc.add_correction(sid, "fix it")
    assert calls == [(sid, "correction")]
    svc.set_phase(sid, "deep", changes_role_rights=True)
    assert calls == [(sid, "correction"), (sid, "phase_rights_change")]
    svc.set_phase(sid, "deep2", changes_role_rights=False)
    assert calls == [(sid, "correction"), (sid, "phase_rights_change")]


# --- t05 Transition C ---


def test_t05_transition_c_apply_edit_still_enforces() -> None:
    g, sess, send_tok = _guard_with_send_offered()
    assert sess.state is SessionState.AWAITING_SEND_CONFIRM
    g.apply_edit(sess.session_id)
    assert sess.state is SessionState.INTERVIEWING
    bad = g.consume_action_token(send_tok, user_id="u62", chat_id="c62")
    assert bad["ok"] is False
    with pytest.raises(IllegalTransitionError):
        g.offer_send_confirm(sess.session_id)


# --- t06 history orthogonality ---


def test_t06_history_remains_utterance_log_separate() -> None:
    hist = HistoryStore()
    hist.append("s62-h", {"role": "user", "content": "hello", "id": "utt-1"})
    svc = SemanticStateService(MemorySemanticStateStore())
    svc.upsert_confirmed_fact(
        "s62-h",
        "from utterance",
        ground_utterance_refs=("utt-1",),
    )
    items = hist.list_items("s62-h")
    assert len(items) == 1
    assert items[0]["content"] == "hello"
    snap = svc.get("s62-h")
    assert snap.facts[0].ground_utterance_refs == ("utt-1",)
    # Semantic payload is not written into history store.
    assert all("facts" not in it for it in items)


# --- t08 gate ---


def test_t08_story_gate_docs_and_module() -> None:
    assert _DOC.is_file()
    text = _DOC.read_text(encoding="utf-8")
    assert "AC-AIB-13-01" in text or "persist" in text.lower()
    assert "invalidate_send_permission" in text
    assert "Transition C" in text or "apply_edit" in text
    assert "HistoryStore" in text or "conversation_history" in text
    assert "hash" in text.lower()  # honesty: no invent hash SSOT
    assert "63" in text and "64" in text
    assert _HIST.is_file()
    assert PostgresSemanticStateStore.__module__.endswith("semantic_state.postgres")
