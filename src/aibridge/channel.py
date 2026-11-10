"""Channel turn/action processing — coordinator + dual-confirm (story 11).

STORY-69: first-turn language-pick gate before interview engine when locale
unbound and text is unclear; clear-text may soft-bind and skip picker.

STORY-72: after CONFIRM_INTERPRETATION consume, server-owned InterviewEngine
turn → build_turn_from_engine on the same /actions response (no citizen free-text).
"""

from __future__ import annotations

import logging
import re
import uuid
from typing import Any

from aibridge.audit import audit_event
from aibridge.channel_wire import ChannelWireContext, apply_before_engine_turn
from aibridge.confirm import ConfirmationGuard, ConfirmSession, get_confirmation_guard
from aibridge.coordinator import build_turn_from_engine
from aibridge.dedupe import EventDedupeStore
from aibridge.locale_policy import (
    infer_locale_from_clear_text,
    is_unclear_language,
    locale_prompt_prefix,
)
from aibridge.metrics import get_metrics
from aibridge.schemas import (
    ChannelAction,
    ChannelActionRequest,
    ChannelSuccessResponse,
    ChannelTurnRequest,
)
from aibridge.seam_policy import needs_control_surface, reply_claims_send_control

logger = logging.getLogger(__name__)

_OPS_PREFIX_MAX = 80
_WS_RE = re.compile(r"\s+")


def _ops_reply_prefix(text: object) -> str:
    """Length-capped single-line prefix for ops logs (no full reply bodies)."""
    if not isinstance(text, str) or not text:
        return ""
    collapsed = _WS_RE.sub(" ", text).strip()
    if len(collapsed) <= _OPS_PREFIX_MAX:
        return collapsed
    return collapsed[:_OPS_PREFIX_MAX]


def log_ops_channel_turn(
    *,
    session_id: str,
    state: str,
    reply_text: str,
    actions: list[Any] | None,
    fc_count: int,
    continuation_url: str | None = None,
    event_id: str | None = None,
) -> None:
    """INFO ops line for button/mint diagnosis (retest-friendly; no secrets)."""
    acts = list(actions or [])
    send_claim = reply_claims_send_control(reply_text)
    needs = needs_control_surface(
        reply_text=reply_text,
        actions=acts if acts else None,
        continuation_url=continuation_url,
    )
    logger.info(
        "ops_channel_turn event_id=%s session_id=%s state=%s fc_count=%s "
        "actions_count=%s send_claim=%s needs_control=%s reply_prefix=%s",
        event_id or "-",
        session_id,
        state,
        fc_count,
        len(acts),
        send_claim,
        needs,
        _ops_reply_prefix(reply_text),
    )


def _new_request_id() -> str:
    return str(uuid.uuid4())


def build_success(
    *,
    request_id: str | None = None,
    session_id: str | None = None,
    state: str = "interviewing",
    reply_text: str = "Acknowledged.",
    actions: list[dict[str, str]] | None = None,
    outcome: str | None = None,
    draft_id: str | None = None,
    continuation_url: str | None = None,
) -> ChannelSuccessResponse:
    """Bounded OAS envelope."""
    action_models = [
        ChannelAction.model_validate(a) for a in (actions or [])
    ]
    return ChannelSuccessResponse(
        request_id=request_id or _new_request_id(),
        session_id=session_id or f"sess_{uuid.uuid4().hex[:16]}",
        state=state,
        reply_text=reply_text,
        actions=action_models,
        outcome=outcome,
        draft_id=draft_id,
        continuation_url=continuation_url,
    )


# Back-compat alias for story 01 tests.
build_stub_success = build_success


def _run_engine_turn(
    engine: Any,
    *,
    session_id: str,
    user_text: str,
) -> dict[str, Any]:
    """Prefer sync create for process_turn; ASGI uses process_turn_async."""
    return engine.run_turn(session_id=session_id, user_text=user_text)


async def _arun_engine_turn(
    engine: Any,
    *,
    session_id: str,
    user_text: str,
) -> dict[str, Any]:
    arun = getattr(engine, "arun_turn", None)
    if arun is not None:
        return await arun(session_id=session_id, user_text=user_text)
    return engine.run_turn(session_id=session_id, user_text=user_text)


def _maybe_language_pick_gate(
    guard: ConfirmationGuard,
    sess: ConfirmSession,
    *,
    user_text: str,
) -> dict[str, Any] | None:
    """STORY-69 — until locale bound: unclear → pick CTAs; clear → soft-bind skip.

    ``language_code`` is intentionally unused here (soft hint only — no silent lock).
    Returns a success envelope dict when engine must not advance; else None.
    """
    if sess.locale is not None:
        return None
    if is_unclear_language(user_text):
        actions = guard.offer_language_pick(sess.session_id)
        guard._persist_session(sess)  # noqa: SLF001
        return build_success(
            session_id=sess.session_id,
            state=sess.state.value,
            reply_text="Please choose your language.",
            actions=actions,
        ).model_dump()
    # Clear-text skip (AC-69-04) — soft-bind when detectable; never invent catalog.
    inferred = infer_locale_from_clear_text(user_text)
    if inferred is not None:
        guard.bind_locale(sess.session_id, inferred)
    return None


def _engine_user_text(sess: ConfirmSession, raw_text: str) -> str:
    """Apply bound locale as thin prompt prefix (not full i18n)."""
    return f"{locale_prompt_prefix(sess.locale)}{raw_text}"


# STORY-72 — fixed server-owned prompt (never citizen free-text on this path).
POST_INTERPRETATION_CONFIRM_PROMPT = (
    "[server] Citizen confirmed draft interpretation. "
    "If the draft is submit-ready, emit the allowlisted function_call; "
    "otherwise continue the interview without inventing Send."
)


def run_post_interpretation_confirm_chain(
    guard: ConfirmationGuard,
    sess: ConfirmSession,
    *,
    interview_engine: Any | None = None,
) -> dict[str, Any]:
    """STORY-72 — post-CONFIRM_INTERPRETATION: engine → build_turn_from_engine.

    Must run **outside** turn_lock. Never authorizes gateway / invents stash.
    Missing engine / engine fail / no-FC → CONTINUE/Edit (no CONFIRM_SEND).
    FC OK → Present validate → persist → offer_send_confirm.
    """
    assert sess.gateway_authorized is False
    engine = interview_engine
    if engine is None:
        engine = getattr(guard, "interview_engine", None)

    if engine is None:
        actions = guard.offer_continue_seam(sess.session_id)
        guard._persist_session(sess)  # noqa: SLF001
        assert sess.gateway_authorized is False
        return {
            "session_id": sess.session_id,
            "state": sess.state.value,
            "reply_text": "Interpretation confirmed — continue when ready.",
            "actions": actions,
            "outcome": None,
            "draft_id": None,
            "continuation_url": None,
        }

    result = _run_engine_turn(
        engine,
        session_id=sess.session_id,
        user_text=_engine_user_text(sess, POST_INTERPRETATION_CONFIRM_PROMPT),
    )
    mapped = build_turn_from_engine(guard, sess, result)
    assert sess.gateway_authorized is False
    return mapped


def process_turn(
    body: ChannelTurnRequest,
    store: EventDedupeStore,
    *,
    guard: ConfirmationGuard | None = None,
    turn_lock: Any | None = None,
    interview_engine: Any | None = None,
    channel_wire: ChannelWireContext | None = None,
) -> tuple[dict[str, Any], bool]:
    """Process turn with dedupe + InterviewEngine coordinator (no Received stub)."""
    g = guard or get_confirmation_guard()
    engine = interview_engine
    if engine is None:
        engine = getattr(g, "interview_engine", None)

    def _side_effect() -> dict[str, Any]:
        sess = g.get_or_create_session(
            user_id=body.principal.user_id,
            chat_id=body.principal.chat_id,
        )

        def _work() -> dict[str, Any]:
            audit_event(
                "channel_turn",
                detail=f"channel={body.channel} text_len={len(body.message.text)}",
            )
            get_metrics().inc_turns()
            gated = _maybe_language_pick_gate(g, sess, user_text=body.message.text)
            if gated is not None:
                log_ops_channel_turn(
                    session_id=str(gated.get("session_id") or sess.session_id),
                    state=str(gated.get("state") or sess.state.value),
                    reply_text=str(gated.get("reply_text") or ""),
                    actions=list(gated.get("actions") or []),
                    fc_count=0,
                    continuation_url=gated.get("continuation_url"),
                    event_id=body.event_id,
                )
                return gated
            if engine is None:
                # Fail closed — product path requires an engine (tests inject one).
                out = build_success(
                    session_id=sess.session_id,
                    state=sess.state.value,
                    reply_text="Interview engine not configured.",
                ).model_dump()
                log_ops_channel_turn(
                    session_id=sess.session_id,
                    state=sess.state.value,
                    reply_text=str(out.get("reply_text") or ""),
                    actions=[],
                    fc_count=0,
                    event_id=body.event_id,
                )
                return out
            apply_before_engine_turn(
                channel_wire,
                session_id=sess.session_id,
                engine=engine,
            )
            result = _run_engine_turn(
                engine,
                session_id=sess.session_id,
                user_text=_engine_user_text(sess, body.message.text),
            )
            mapped = build_turn_from_engine(g, sess, result)
            actions = list(mapped.get("actions") or [])
            out = build_success(
                session_id=str(mapped["session_id"]),
                state=str(mapped["state"]),
                reply_text=str(mapped["reply_text"]),
                actions=actions,
                outcome=mapped.get("outcome"),
                draft_id=mapped.get("draft_id"),
                continuation_url=mapped.get("continuation_url"),
            ).model_dump()
            fc_raw = (
                result.get("function_calls") if isinstance(result, dict) else None
            )
            fc_count = len(list(fc_raw or []))
            log_ops_channel_turn(
                session_id=str(mapped["session_id"]),
                state=str(mapped["state"]),
                reply_text=str(mapped["reply_text"]),
                actions=actions,
                fc_count=fc_count,
                continuation_url=mapped.get("continuation_url"),
                event_id=body.event_id,
            )
            return out

        if turn_lock is not None:
            with turn_lock.hold(sess.session_id):
                return _work()
        return _work()

    return store.get_or_create(body.channel, body.event_id, _side_effect)


async def process_turn_async(
    body: ChannelTurnRequest,
    store: EventDedupeStore,
    *,
    guard: ConfirmationGuard | None = None,
    turn_lock: Any | None = None,
    interview_engine: Any | None = None,
    channel_wire: ChannelWireContext | None = None,
) -> tuple[dict[str, Any], bool]:
    """ASGI path — claim dedupe **before** engine (G-03); await arun_turn."""
    g = guard or get_confirmation_guard()
    engine = interview_engine
    if engine is None:
        engine = getattr(g, "interview_engine", None)

    # Claim-or-hit before Responses (G-03).
    begin_fn = getattr(store, "try_begin", None)
    if begin_fn is not None:
        existing, status = begin_fn(body.channel, body.event_id)
        if status == "hit" and existing is not None:
            return existing, False
        if status == "inflight":
            wait_fn = getattr(store, "wait_for_result", None)
            if wait_fn is not None:
                waited = wait_fn(body.channel, body.event_id)
                if waited is not None:
                    return waited, False
            # Fail closed — do not double-call engine.
            return (
                build_success(
                    reply_text="Duplicate event in flight.",
                    state="interviewing",
                ).model_dump(),
                False,
            )
        claimed = status == "begin"
    else:
        # Legacy stores: peek then proceed (best-effort).
        existing = None
        if hasattr(store, "get"):
            existing = store.get(body.channel, body.event_id)
        if existing is not None:
            if isinstance(existing, dict):
                return dict(existing), False
            body_attr = getattr(existing, "body", None)
            if body_attr is not None:
                return dict(body_attr), False
            return dict(existing), False
        claimed = True

    sess = g.get_or_create_session(
        user_id=body.principal.user_id,
        chat_id=body.principal.chat_id,
    )

    async def _work() -> dict[str, Any]:
        audit_event(
            "channel_turn",
            detail=f"channel={body.channel} text_len={len(body.message.text)}",
        )
        get_metrics().inc_turns()
        gated = _maybe_language_pick_gate(g, sess, user_text=body.message.text)
        if gated is not None:
            log_ops_channel_turn(
                session_id=str(gated.get("session_id") or sess.session_id),
                state=str(gated.get("state") or sess.state.value),
                reply_text=str(gated.get("reply_text") or ""),
                actions=list(gated.get("actions") or []),
                fc_count=0,
                continuation_url=gated.get("continuation_url"),
                event_id=body.event_id,
            )
            return gated
        if engine is None:
            out = build_success(
                session_id=sess.session_id,
                state=sess.state.value,
                reply_text="Interview engine not configured.",
            ).model_dump()
            log_ops_channel_turn(
                session_id=sess.session_id,
                state=sess.state.value,
                reply_text=str(out.get("reply_text") or ""),
                actions=[],
                fc_count=0,
                event_id=body.event_id,
            )
            return out
        apply_before_engine_turn(
            channel_wire,
            session_id=sess.session_id,
            engine=engine,
        )
        result = await _arun_engine_turn(
            engine,
            session_id=sess.session_id,
            user_text=_engine_user_text(sess, body.message.text),
        )
        mapped = build_turn_from_engine(g, sess, result)
        actions = list(mapped.get("actions") or [])
        out = build_success(
            session_id=str(mapped["session_id"]),
            state=str(mapped["state"]),
            reply_text=str(mapped["reply_text"]),
            actions=actions,
            outcome=mapped.get("outcome"),
            draft_id=mapped.get("draft_id"),
            continuation_url=mapped.get("continuation_url"),
        ).model_dump()
        fc_raw = result.get("function_calls") if isinstance(result, dict) else None
        fc_count = len(list(fc_raw or []))
        log_ops_channel_turn(
            session_id=str(mapped["session_id"]),
            state=str(mapped["state"]),
            reply_text=str(mapped["reply_text"]),
            actions=actions,
            fc_count=fc_count,
            continuation_url=mapped.get("continuation_url"),
            event_id=body.event_id,
        )
        return out

    try:
        if turn_lock is not None:
            with turn_lock.hold(sess.session_id):
                body_out = await _work()
        else:
            body_out = await _work()
    except Exception:
        abort_fn = getattr(store, "abort", None)
        if claimed and abort_fn is not None:
            abort_fn(body.channel, body.event_id)
        raise

    complete_fn = getattr(store, "complete", None)
    if claimed and complete_fn is not None:
        complete_fn(body.channel, body.event_id, body_out)
        return body_out, True

    def _side_effect() -> dict[str, Any]:
        return body_out

    stored, created = store.get_or_create(body.channel, body.event_id, _side_effect)
    return stored, created


def process_action(
    body: ChannelActionRequest,
    store: EventDedupeStore,
    *,
    guard: ConfirmationGuard | None = None,
    turn_lock: Any | None = None,
    interview_engine: Any | None = None,
) -> tuple[dict[str, Any] | None, bool, dict[str, Any] | None]:
    """Process action with dedupe + confirmation guard.

    Returns (success_body | None, is_new, error_info | None).
    error_info: {http_status, code, message} when fail-closed.

    G-02: turn_lock is held only for token consume / state prep — never across
    gateway HTTPS (deferred via execute_gateway=False).

    STORY-72: after CONFIRM_INTERPRETATION, post-confirm engine chain runs
    **outside** the turn_lock (same response; no invent stash / TokenActionKind).
    """
    g = guard or get_confirmation_guard()

    def _side_effect() -> dict[str, Any]:
        sess = g.get_or_create_session(
            user_id=body.principal.user_id,
            chat_id=body.principal.chat_id,
        )

        def _consume(*, execute_gateway: bool) -> dict[str, Any]:
            return g.consume_action_token(
                body.action_token,
                user_id=body.principal.user_id,
                chat_id=body.principal.chat_id,
                execute_gateway=execute_gateway,
            )

        # Always defer gateway when a turn_lock is present so HTTPS is outside hold.
        defer = turn_lock is not None
        if turn_lock is not None:
            with turn_lock.hold(sess.session_id):
                result = _consume(execute_gateway=not defer)
        else:
            result = _consume(execute_gateway=True)

        if result.get("ok") and result.get("deferred_gateway"):
            # Lock released — HTTPS + outcome.
            result = g.finish_deferred_gateway(
                str(result["session_id"]),
                frozen_body=dict(result.get("frozen_body") or {}),
            )

        # STORY-72 — post-confirm chain outside turn_lock (arch 05 §2).
        if result.get("ok") and result.get("post_confirm_engine"):
            post_sess = g.get_session(str(result["session_id"]))
            if post_sess is None:
                post_sess = sess
            mapped = run_post_interpretation_confirm_chain(
                g,
                post_sess,
                interview_engine=interview_engine,
            )
            result = {
                **result,
                "session_id": mapped["session_id"],
                "state": mapped["state"],
                "reply_text": mapped["reply_text"],
                "actions": list(mapped.get("actions") or []),
                "outcome": mapped.get("outcome"),
                "draft_id": mapped.get("draft_id"),
                "continuation_url": mapped.get("continuation_url"),
                # Keep: interpret path never authorizes gateway.
                "gateway_authorized": False,
            }

        get_metrics().inc_actions()
        audit_event(
            "channel_action",
            detail=f"channel={body.channel} ok={bool(result.get('ok'))}",
        )
        if not result.get("ok"):
            return {"__error__": result}
        return build_success(
            session_id=str(result["session_id"]),
            state=str(result["state"]),
            reply_text=str(result["reply_text"]),
            actions=list(result.get("actions") or []),
            outcome=result.get("outcome"),
            draft_id=result.get("draft_id"),
            continuation_url=result.get("continuation_url"),
        ).model_dump()

    body_out, created = store.get_or_create(body.channel, body.event_id, _side_effect)
    if isinstance(body_out, dict) and "__error__" in body_out:
        err = body_out["__error__"]
        return None, created, {
            "http_status": int(err["http_status"]),
            "code": str(err["code"]),
            "message": str(err["message"]),
        }
    return body_out, created, None
