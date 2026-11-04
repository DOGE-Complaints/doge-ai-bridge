"""STORY-AIBRIDGE-65 — ASGI channel semantic + roles wire (lift G-02).

Locks: no new HTTP · Keep dual-confirm/stash · OOS 66/67/GPT-48.
"""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.channel import process_turn
from aibridge.channel_wire import ChannelWireContext, apply_before_engine_turn
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.confirm_fsm import SessionState
from aibridge.dedupe import EventDedupeStore
from aibridge.interview import default_recording_engine
from aibridge.schemas import ChannelTurnRequest
from aibridge.semantic_state import MemorySemanticStateStore, SemanticStateService

_REPO = Path(__file__).resolve().parents[1]
_DOC = _REPO / "docs" / "runtime-docs" / "12-asgi-channel-semantic-roles-wire.md"
_FIXTURES = _REPO / "tests" / "fixtures" / "content"
_ROLES_DIR = _FIXTURES / "roles-instructions"
_ROLES_MANIFEST = _FIXTURES / "roles.manifest.json"
_REQ13 = (
    _REPO
    / "docs"
    / "requirements"
    / "REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md"
)


def _settings(**extra: str) -> Settings:
    reset_settings_cache()
    kwargs = {
        "_env_file": None,
        "AIBRIDGE_CHANNEL_BEARER_TOKEN": "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "GATEWAY_SERVICE_API_TOKEN": "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "GATEWAY_BASE_URL": "https://gateway.example.invalid",
        "SPA_BASE_URL": "https://spa.example.invalid",
        "OPENAI_API_KEY": "sk-test-not-real",
        "OPENAI_MODEL": "gpt-test",
        "AIBRIDGE_INTERVIEW_PROVIDER": "openai",
        "AIBRIDGE_DRY_RUN": "true",
        "DOGESTONIA_ROLES_INSTRUCTIONS_DIR": str(_ROLES_DIR),
        "DOGESTONIA_ROLES_MANIFEST": str(_ROLES_MANIFEST),
    }
    kwargs.update(extra)
    return Settings(**kwargs)  # type: ignore[arg-type]


def _auth() -> dict[str, str]:
    return {
        "Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }


def _turn(event_id: str = "6501") -> dict:
    return {
        "channel": "telegram",
        "event_id": event_id,
        "principal": {"user_id": "65", "chat_id": "-165"},
        "message": {"message_id": "1", "text": "hello wire"},
    }


def test_t01_semantic_state_bound_on_channel_session() -> None:
    reset_confirmation_guard()
    app = create_app(
        settings=_settings(),
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    assert getattr(app.state, "semantic_state_service", None) is not None
    assert getattr(app.state, "channel_wire", None) is not None
    client = TestClient(app)
    r = client.post("/v1/channel/turns", json=_turn("6501a"), headers=_auth())
    assert r.status_code == 200
    sid = r.json()["session_id"]
    snap = app.state.semantic_state_service.get(sid)
    assert snap.phase == "interviewing"
    # Persist across second turn
    r2 = client.post("/v1/channel/turns", json=_turn("6501b"), headers=_auth())
    assert r2.status_code == 200
    assert r2.json()["session_id"] == sid
    snap2 = app.state.semantic_state_service.get(sid)
    assert snap2.phase == "interviewing"


def test_t02_select_and_assemble_on_channel_turns() -> None:
    reset_confirmation_guard()
    engine = default_recording_engine()
    engine.instructions = "ADR1-mega-before"
    app = create_app(
        settings=_settings(),
        dedupe_store=EventDedupeStore(),
        interview_engine=engine,
    )
    client = TestClient(app)
    r = client.post("/v1/channel/turns", json=_turn("6502"), headers=_auth())
    assert r.status_code == 200
    ev = app.state.channel_wire.last_evidence
    assert ev.get("wired") is True
    assert ev.get("role_id") == "interviewer"
    assert ev.get("assembled") is True
    assert ev.get("session_pin")
    assert "interviewer" in engine.instructions.lower() or len(engine.instructions) > 20
    assert engine.instructions != "ADR1-mega-before"


def test_t03_meaning_change_invalidates_send_on_channel() -> None:
    reset_confirmation_guard()
    guard = ConfirmationGuard()
    sess = guard.get_or_create_session(user_id="u65", chat_id="c65")
    sess.state = SessionState.AWAITING_SEND_CONFIRM
    sess.gateway_authorized = True
    sess.frozen_tool_intent = {"op": "x"}
    old_rev = sess.revision
    svc = SemanticStateService(MemorySemanticStateStore(), confirm_guard=guard)
    svc.upsert_confirmed_fact(sess.session_id, "fact-on-channel")
    assert sess.revision == old_rev + 1
    assert sess.gateway_authorized is False
    assert sess.frozen_tool_intent is None
    assert sess.state is SessionState.AWAITING_SEND_CONFIRM  # no FSM EDIT


def test_t03_app_wire_confirm_guard_callback() -> None:
    """App-created SemanticStateService uses confirm_guard invalidate path."""
    reset_confirmation_guard()
    app = create_app(
        settings=_settings(),
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    client = TestClient(app)
    r = client.post("/v1/channel/turns", json=_turn("6503"), headers=_auth())
    sid = r.json()["session_id"]
    guard = app.state.confirmation_guard
    sess = guard._sessions[sid]
    sess.gateway_authorized = True
    sess.frozen_tool_intent = {"op": "y"}
    old_rev = sess.revision
    app.state.semantic_state_service.upsert_confirmed_fact(sid, "meaning")
    assert sess.revision == old_rev + 1
    assert sess.gateway_authorized is False
    assert sess.frozen_tool_intent is None


def test_t04_no_new_channel_http_and_dual_confirm_smoke() -> None:
    reset_confirmation_guard()
    app = create_app(
        settings=_settings(),
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    paths = {getattr(r, "path", None) for r in app.routes}
    channel_paths = {p for p in paths if isinstance(p, str) and p.startswith("/v1/channel")}
    assert channel_paths == {"/v1/channel/turns", "/v1/channel/actions"}
    # Dual-confirm smoke: process_turn still maps via build_turn_from_engine
    body = ChannelTurnRequest.model_validate(_turn("6504"))
    store = EventDedupeStore()
    out, created = process_turn(
        body,
        store,
        guard=app.state.confirmation_guard,
        interview_engine=app.state.interview_engine,
        channel_wire=app.state.channel_wire,
    )
    assert created is True
    assert out["session_id"]
    assert "reply_text" in out


def test_t05_g02_waiver_lifted_in_docs() -> None:
    assert _DOC.is_file()
    text = _DOC.read_text(encoding="utf-8")
    assert "G-02" in text
    assert "lift" in text.lower() or "Lifted" in text or "Present" in text
    assert "/v1/channel/turns" in text
    assert "no new" in text.lower() or "No new HTTP" in text
    assert "STORY-66" in text or "66" in text
    req = _REQ13.read_text(encoding="utf-8")
    assert "STORY-65" in req or "channel wire" in req.lower()
    # Must not still claim ASGI bind Absent/WAIVED as current residual without 65 note
    assert "STORY-65" in req


def test_apply_before_engine_without_roles_paths_still_selects() -> None:
    svc = SemanticStateService(MemorySemanticStateStore())
    ctx = ChannelWireContext(semantic=svc)
    engine = default_recording_engine()
    engine.instructions = "keep-me"
    ev = apply_before_engine_turn(ctx, session_id="s1", engine=engine)
    assert ev["wired"] and ev["role_id"] == "interviewer"
    assert ev["assembled"] is False
    assert engine.instructions == "keep-me"
