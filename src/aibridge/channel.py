"""Channel turn/action processing — coordinator + dual-confirm (story 11)."""

from __future__ import annotations

import uuid
from typing import Any

from aibridge.audit import audit_event
from aibridge.confirm import ConfirmationGuard, get_confirmation_guard
from aibridge.coordinator import build_turn_from_engine
from aibridge.dedupe import EventDedupeStore
from aibridge.metrics import get_metrics
from aibridge.schemas import (
    ChannelAction,
    ChannelActionRequest,
    ChannelSuccessResponse,
    ChannelTurnRequest,
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


def process_turn(
    body: ChannelTurnRequest,
    store: EventDedupeStore,
    *,
    guard: ConfirmationGuard | None = None,
    turn_lock: Any | None = None,
    interview_engine: Any | None = None,
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
            if engine is None:
                # Fail closed — product path requires an engine (tests inject one).
                return build_success(
                    session_id=sess.session_id,
                    state=sess.state.value,
                    reply_text="Interview engine not configured.",
                ).model_dump()
            result = _run_engine_turn(
                engine,
                session_id=sess.session_id,
                user_text=body.message.text,
            )
            mapped = build_turn_from_engine(g, sess, result)
            return build_success(
                session_id=str(mapped["session_id"]),
                state=str(mapped["state"]),
                reply_text=str(mapped["reply_text"]),
                actions=list(mapped.get("actions") or []),
                outcome=mapped.get("outcome"),
                draft_id=mapped.get("draft_id"),
                continuation_url=mapped.get("continuation_url"),
            ).model_dump()

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
            if hasattr(existing, "body"):
                return dict(existing.body), False
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
        if engine is None:
            return build_success(
                session_id=sess.session_id,
                state=sess.state.value,
                reply_text="Interview engine not configured.",
            ).model_dump()
        result = await _arun_engine_turn(
            engine,
            session_id=sess.session_id,
            user_text=body.message.text,
        )
        mapped = build_turn_from_engine(g, sess, result)
        return build_success(
            session_id=str(mapped["session_id"]),
            state=str(mapped["state"]),
            reply_text=str(mapped["reply_text"]),
            actions=list(mapped.get("actions") or []),
            outcome=mapped.get("outcome"),
            draft_id=mapped.get("draft_id"),
            continuation_url=mapped.get("continuation_url"),
        ).model_dump()

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
) -> tuple[dict[str, Any] | None, bool, dict[str, Any] | None]:
    """Process action with dedupe + confirmation guard.

    Returns (success_body | None, is_new, error_info | None).
    error_info: {http_status, code, message} when fail-closed.

    G-02: turn_lock is held only for token consume / state prep — never across
    gateway HTTPS (deferred via execute_gateway=False).
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
