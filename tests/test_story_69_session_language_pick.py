"""STORY-AIBRIDGE-69 — session language pick + ConfirmSession.locale SSOT.

Honesty: locale ∈ ConfirmSession (not semantic_state); EN=🇺🇸; unclear→pick;
clear-text skip; no invent full i18n / live TG SUCCESS; STORY-68 OOS.
"""

from __future__ import annotations

from typing import Any

from aibridge.action_tokens import TokenActionKind
from aibridge.channel import process_turn
from aibridge.confirm import ConfirmationGuard
from aibridge.dedupe import EventDedupeStore
from aibridge.locale_policy import (
    LANG_PICK_LABELS,
    infer_locale_from_clear_text,
    is_unclear_language,
    lang_pick_label,
)
from aibridge.schemas import ChannelTurnRequest


class _FakeConfirmSessionStore:
    """Minimal PG-shaped store for locale state_json round-trip (t03)."""

    def __init__(self) -> None:
        self._by_id: dict[str, dict[str, Any]] = {}
        self._by_principal: dict[tuple[str, str], str] = {}

    def upsert(
        self,
        *,
        session_id: str,
        user_id: str,
        chat_id: str,
        state: dict[str, Any],
    ) -> None:
        row = {
            "session_id": session_id,
            "user_id": user_id,
            "chat_id": chat_id,
            "state": dict(state),
        }
        self._by_id[session_id] = row
        self._by_principal[(user_id, chat_id)] = session_id

    def get(self, session_id: str) -> dict[str, Any] | None:
        return self._by_id.get(session_id)

    def get_by_principal(self, *, user_id: str, chat_id: str) -> dict[str, Any] | None:
        sid = self._by_principal.get((user_id, chat_id))
        return self._by_id.get(sid) if sid else None


class _RecordingEngine:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def run_turn(self, *, session_id: str, user_text: str) -> dict[str, Any]:
        self.calls.append(user_text)
        return {"ok": True, "reply_text": "Interview ack.", "function_calls": []}


def _turn(
    *,
    user_id: str,
    chat_id: str,
    text: str,
    event_id: str,
    language_code: str | None = None,
) -> ChannelTurnRequest:
    msg: dict[str, Any] = {"message_id": "1", "text": text}
    if language_code is not None:
        msg["language_code"] = language_code
    return ChannelTurnRequest.model_validate(
        {
            "channel": "telegram",
            "event_id": event_id,
            "principal": {"user_id": user_id, "chat_id": chat_id},
            "message": msg,
        }
    )


# --- t01 detector ---


def test_t01_unclear_vs_clear_detector() -> None:
    assert is_unclear_language("888")
    assert is_unclear_language("   ")
    assert is_unclear_language("!!!")
    assert is_unclear_language("ab12")
    assert not is_unclear_language("историю хочу подать")
    assert not is_unclear_language("I want to submit a story")
    assert infer_locale_from_clear_text("историю хочу подать") == "ru"
    assert infer_locale_from_clear_text("I want to submit a story") == "en"


# --- t02 / t04 mint ---


def test_t02_t04_locale_field_and_pick_labels() -> None:
    assert lang_pick_label("en") == "English 🇺🇸"
    assert "🇺🇸" in LANG_PICK_LABELS["en"]
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="69", chat_id="1")
    assert sess.locale is None
    acts = g.offer_language_pick(sess.session_id)
    assert len(acts) == 3
    labels = {a["label"] for a in acts}
    assert "Eesti 🇪🇪" in labels
    assert "Русский 🇷🇺" in labels
    assert "English 🇺🇸" in labels
    kinds = {g.tokens.lookup(a["token"]).action for a in acts}
    assert TokenActionKind.PICK_LOCALE_EN in kinds
    assert TokenActionKind.PICK_LOCALE_ET in kinds
    assert TokenActionKind.PICK_LOCALE_RU in kinds


# --- t03 PG/memory round-trip ---


def test_t03_locale_persists_via_state_json_store() -> None:
    store = _FakeConfirmSessionStore()
    g = ConfirmationGuard(confirm_sessions=store)
    sess = g.get_or_create_session(user_id="69", chat_id="2")
    g.bind_locale(sess.session_id, "et")
    assert store.get(sess.session_id)["state"]["locale"] == "et"
    # Simulate cold hydrate
    g2 = ConfirmationGuard(confirm_sessions=store)
    sess2 = g2.get_or_create_session(user_id="69", chat_id="2")
    assert sess2.locale == "et"
    assert sess2.session_id == sess.session_id


# --- t05 / t06 / channel gate ---


def test_t05_unclear_gates_before_engine() -> None:
    engine = _RecordingEngine()
    g = ConfirmationGuard(interview_engine=engine)
    out, _ = process_turn(
        _turn(user_id="69", chat_id="3", text="888", event_id="e69-unclear"),
        EventDedupeStore(),
        guard=g,
        interview_engine=engine,
    )
    assert engine.calls == []
    assert out["reply_text"].startswith("Please choose")
    assert len(out["actions"]) == 3
    assert any("🇺🇸" in a["label"] for a in out["actions"])
    # language_code must not silent-lock when unclear
    out2, _ = process_turn(
        _turn(
            user_id="69",
            chat_id="4",
            text="888",
            event_id="e69-lc",
            language_code="et",
        ),
        EventDedupeStore(),
        guard=ConfirmationGuard(interview_engine=engine),
        interview_engine=engine,
    )
    assert len(out2["actions"]) == 3
    assert engine.calls == []


def test_t05_clear_text_skips_picker_and_soft_binds() -> None:
    engine = _RecordingEngine()
    g = ConfirmationGuard(interview_engine=engine)
    out, _ = process_turn(
        _turn(
            user_id="69",
            chat_id="5",
            text="историю хочу подать",
            event_id="e69-clear",
        ),
        EventDedupeStore(),
        guard=g,
        interview_engine=engine,
    )
    sess = g.get_or_create_session(user_id="69", chat_id="5")
    assert sess.locale == "ru"
    assert engine.calls  # engine advanced
    assert "[session_locale=ru]" in engine.calls[0]
    # No lang-pick forced on clear start
    assert not any("🇺🇸" in a.get("label", "") for a in out.get("actions") or [])


def test_t06_consume_bind_locale_no_gateway() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="69", chat_id="6")
    acts = g.offer_language_pick(sess.session_id)
    en_tok = next(
        a["token"]
        for a in acts
        if g.tokens.lookup(a["token"]).action is TokenActionKind.PICK_LOCALE_EN
    )
    before = sess.gateway_invocations
    result = g.consume_action_token(en_tok, user_id="69", chat_id="6")
    assert result["ok"] is True
    assert sess.locale == "en"
    assert sess.gateway_authorized is False
    assert sess.gateway_invocations == before
    assert "en" in result["reply_text"]
