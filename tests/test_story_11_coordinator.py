"""STORY-AIBRIDGE-11 — coordinator + P6 audit gaps G-01/G-02/G-03."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.channel import process_action, process_turn, process_turn_async
from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import SessionState
from aibridge.coordinator import (
    ToolValidationError,
    ValidationContext,
    persist_pending_tool,
    validate_function_calls,
)
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import (
    STASH_REPLY,
    GatewayExecutor,
    GatewayOutcome,
    RawHttpResponse,
    RecordingGatewayTransport,
)
from aibridge.interview import InterviewEngine
from aibridge.request_assembly import ServerConstants
from aibridge.responses_client import RecordingResponsesClient
from aibridge.schemas import ChannelActionRequest, ChannelTurnRequest
from aibridge.turn_lock import SessionTurnLock

PACK_SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string"}},
    "required": ["title"],
    "additionalProperties": False,
}
TOOL_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "required": ["narrative", "schema_binding"],
    "properties": {
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["structured_payload"],
            "properties": {
                "structured_payload": {"type": "object", "additionalProperties": True},
            },
        },
    },
}
WIRE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "narrative", "schema_binding", "origin"],
    "properties": {
        "schema_version": {"type": "string"},
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_id", "schema_version", "structured_payload"],
            "properties": {
                "schema_id": {"type": "string"},
                "schema_version": {"type": "string"},
                "structured_payload": PACK_SCHEMA,
            },
        },
        "origin": {
            "type": "object",
            "additionalProperties": False,
            "required": ["source"],
            "properties": {"source": {"type": "string"}},
        },
    },
}


def _validation() -> ValidationContext:
    return ValidationContext(
        tool_parameters=TOOL_PARAMS,
        pack_schema=PACK_SCHEMA,
        wire_schema=WIRE_SCHEMA,
        constants=ServerConstants(schema_id="pack-test", schema_version_pack="v1"),
    )


def _good_args() -> dict:
    return {
        "narrative": {"note": "n"},
        "schema_binding": {"structured_payload": {"title": "ok"}},
    }


def _ok_201(draft_id: str = "draft-11") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": "t11"}).encode()
    return RawHttpResponse(status_code=201, body=body)


def _fc_payload(*, call_id: str = "call_11", args: dict | None = None) -> dict:
    return {
        "id": "resp_fc",
        "output": [
            {
                "type": "function_call",
                "call_id": call_id,
                "name": "postStoryDraftStash",
                "arguments": json.dumps(args or _good_args()),
            },
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "Ready to stash."}],
            },
        ],
        "usage": {"input_tokens": 5, "output_tokens": 3},
    }


# --- t01 wire turns ---


def test_turn_returns_interview_not_received(
    client: TestClient, auth_header: dict[str, str], turn_payload: dict
) -> None:
    response = client.post(
        "/v1/channel/turns", json=turn_payload, headers=auth_header
    )
    assert response.status_code == 200
    body = response.json()
    assert not str(body["reply_text"]).startswith("Received:")
    assert body["reply_text"]


# --- t02 / G-01 three gates ---


def test_function_call_persisted_before_send_actions() -> None:
    client = RecordingResponsesClient(scripted=[_fc_payload()])
    engine = InterviewEngine(client=client)
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        channel_bearer="ch",
        transport=transport,
        redirect_base="https://spa.example",
    )
    guard = ConfirmationGuard(
        executor=executor,
        interview_engine=engine,
        validation_context=_validation(),
    )
    sess = guard.get_or_create_session(user_id="1", chat_id="2")
    acts = guard.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    guard.consume_action_token(tok, user_id="1", chat_id="2")

    body = ChannelTurnRequest.model_validate(
        {
            "channel": "telegram",
            "event_id": "e-fc-1",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "1", "text": "stash please"},
        }
    )
    out, _ = process_turn(
        body, EventDedupeStore(), guard=guard, interview_engine=engine
    )
    assert out["state"] == SessionState.AWAITING_SEND_CONFIRM.value
    assert len(out["actions"]) == 3
    assert sess.pending_call_id == "call_11"
    assert sess.frozen_tool_intent is not None
    assert "schema_version" in sess.frozen_tool_intent["arguments"]
    assert transport.calls == []


def test_three_gates_reject_bad_payload() -> None:
    with pytest.raises(ToolValidationError, match="gate"):
        validate_function_calls(
            [
                {
                    "call_id": "c1",
                    "name": "postStoryDraftStash",
                    "arguments": json.dumps(
                        {
                            "narrative": {},
                            "schema_binding": {"structured_payload": {"no_title": 1}},
                        }
                    ),
                }
            ],
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=_validation(),
        )


def test_validate_function_call_gates() -> None:
    with pytest.raises(ToolValidationError):
        validate_function_calls(
            [{"call_id": "c1", "name": "evil", "arguments": "{}"}],
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=_validation(),
        )


# --- t03 interpretation ---


def test_interpretation_confirm_no_gateway_http() -> None:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        channel_bearer="ch",
        transport=transport,
    )
    g = ConfirmationGuard(executor=executor)
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    acts = g.offer_interpretation_confirm(sess.session_id)
    before = sess.gateway_invocations
    result = g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="1",
        chat_id="2",
    )
    assert result["ok"] is True
    assert result["gateway_authorized"] is False
    assert sess.gateway_invocations == before
    assert transport.calls == []


# --- t04 frozen body ---


def test_send_uses_frozen_body_only() -> None:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        channel_bearer="ch",
        transport=transport,
        redirect_base="https://spa.example",
    )
    g = ConfirmationGuard(executor=executor)
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="1",
        chat_id="2",
    )
    g.set_frozen_tool_intent(
        sess.session_id,
        {
            "name": "postStoryDraftStash",
            "call_id": "c",
            "arguments": {"only": "frozen"},
        },
        draft_hash="abc",
    )
    send = g.offer_send_confirm(sess.session_id)
    result = g.consume_action_token(
        next(a["token"] for a in send if a["style"] == "primary"),
        user_id="1",
        chat_id="2",
    )
    assert result["ok"] is True
    assert transport.calls[0]["json_body"] == {"only": "frozen"}


# --- t05 stash + FCO ---


def test_stashed_then_function_call_output_with_call_id() -> None:
    scripted = [
        _fc_payload(call_id="call_orig"),
        {
            "id": "resp_out",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "Draft noted."}],
                }
            ],
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    ]
    resp_client = RecordingResponsesClient(scripted=scripted)
    engine = InterviewEngine(client=resp_client)
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        channel_bearer="ch",
        transport=transport,
        redirect_base="https://spa.example",
    )
    guard = ConfirmationGuard(
        executor=executor,
        interview_engine=engine,
        validation_context=_validation(),
    )
    sess = guard.get_or_create_session(user_id="9", chat_id="9")
    interpret = guard.offer_interpretation_confirm(sess.session_id)
    guard.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="9",
        chat_id="9",
    )
    turn = ChannelTurnRequest.model_validate(
        {
            "channel": "telegram",
            "event_id": "e-stash",
            "principal": {"user_id": "9", "chat_id": "9"},
            "message": {"message_id": "2", "text": "go"},
        }
    )
    out, _ = process_turn(
        turn, EventDedupeStore(), guard=guard, interview_engine=engine
    )
    send_tok = next(a["token"] for a in out["actions"] if a["style"] == "primary")
    result = guard.consume_action_token(send_tok, user_id="9", chat_id="9")
    assert result["outcome"] == GatewayOutcome.STASHED.value
    assert result["reply_text"] == STASH_REPLY
    assert len(resp_client.calls) == 2
    follow_input = resp_client.calls[1]["input"]
    fco = [x for x in follow_input if x.get("type") == "function_call_output"]
    assert fco[0]["call_id"] == "call_orig"


# --- t06 unknown_outcome ---


def test_recover_stale_executing_blocks_auto_resend() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    sess.state = SessionState.EXECUTING
    sess.revision = 3
    g.recover_stale_executing(session_id=sess.session_id, revision=3)
    assert sess.state is SessionState.UNKNOWN_OUTCOME
    assert g.send_blocked_for_revision(sess) is True


def test_pending_survives_fresh_guard_memory_rehydrate() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="u", chat_id="c")
    sess.state = SessionState.INTERPRETATION_CONFIRMED
    persist_pending_tool(
        g,
        sess,
        frozen={
            "name": "postStoryDraftStash",
            "call_id": "call_p",
            "arguments": {"k": 1},
            "draft_hash": "h",
        },
        replay_items=[{"type": "function_call", "call_id": "call_p"}],
    )
    state = {
        "state": sess.state.value,
        "revision": sess.revision,
        "deployment_id": sess.deployment_id,
        "frozen_tool_intent": sess.frozen_tool_intent,
        "draft_hash": sess.draft_hash,
        "gateway_authorized": False,
        "gateway_invocations": 0,
        "last_outcome": None,
        "draft_id": None,
        "continuation_url": None,
        "unknown_outcome_revision": None,
        "pending_call_id": sess.pending_call_id,
        "pending_replay_items": sess.pending_replay_items,
    }
    g2 = ConfirmationGuard()
    hydrated = g2._hydrate_from_row(  # noqa: SLF001
        {
            "session_id": sess.session_id,
            "user_id": "u",
            "chat_id": "c",
            "state": state,
        }
    )
    assert hydrated.pending_call_id == "call_p"


# --- G-02 lock released before HTTPS ---


def test_g02_turn_lock_not_held_during_gateway_https() -> None:
    lock = SessionTurnLock()
    held_during_https: list[bool] = []

    class SpyTransport(RecordingGatewayTransport):
        def request(self, *a: object, **k: object) -> RawHttpResponse:  # type: ignore[no-untyped-def]
            held_during_https.append(lock.is_active("sess-lock"))
            return super().request(*a, **k)

    transport = SpyTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        channel_bearer="ch",
        transport=transport,
        redirect_base="https://spa.example",
    )
    g = ConfirmationGuard(executor=executor)
    sess = g.get_or_create_session(user_id="1", chat_id="2", session_id="sess-lock")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="1",
        chat_id="2",
    )
    g.set_frozen_tool_intent(sess.session_id, {"arguments": {"a": 1}}, draft_hash="h")
    send = g.offer_send_confirm(sess.session_id)
    tok = next(a["token"] for a in send if a["style"] == "primary")

    action = ChannelActionRequest.model_validate(
        {
            "channel": "telegram",
            "event_id": "act-g02",
            "callback_query_id": "cb",
            "principal": {"user_id": "1", "chat_id": "2"},
            "action_token": tok,
        }
    )
    success, _, err = process_action(action, EventDedupeStore(), guard=g, turn_lock=lock)
    assert err is None
    assert success is not None
    assert held_during_https == [False]
    assert lock.is_active("sess-lock") is False


# --- G-03 claim before engine ---


def test_g03_claim_prevents_double_engine_call() -> None:
    import asyncio

    calls = {"n": 0}

    class CountingClient(RecordingResponsesClient):
        async def acreate(self, request):  # type: ignore[no-untyped-def]
            calls["n"] += 1
            return self.create(request)

    engine = InterviewEngine(client=CountingClient())
    store = EventDedupeStore()
    g = ConfirmationGuard(interview_engine=engine, validation_context=_validation())

    turn = ChannelTurnRequest.model_validate(
        {
            "channel": "telegram",
            "event_id": "same-evt",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "1", "text": "hi"},
        }
    )

    async def _run() -> None:
        out1, created1 = await process_turn_async(
            turn, store, guard=g, interview_engine=engine
        )
        out2, created2 = await process_turn_async(
            turn, store, guard=g, interview_engine=engine
        )
        assert created1 is True
        assert created2 is False
        assert out1["reply_text"] == out2["reply_text"]

    asyncio.run(_run())
    assert calls["n"] == 1


# --- G-03 PG pending ---

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


@pytest.mark.skipif(not _pg_available(), reason="disposable Postgres not running")
def test_g03_pending_survives_pg_confirm_session_store() -> None:
    from aibridge.migrate import apply_migrations
    from aibridge.pg_runtime import PostgresConfirmSessionStore

    apply_migrations(DISPOSABLE_URL)
    store = PostgresConfirmSessionStore(DISPOSABLE_URL)
    g = ConfirmationGuard(confirm_sessions=store)
    sess = g.get_or_create_session(user_id="pg-u", chat_id="pg-c")
    sess.state = SessionState.INTERPRETATION_CONFIRMED
    persist_pending_tool(
        g,
        sess,
        frozen={
            "name": "postStoryDraftStash",
            "call_id": "call_pg",
            "arguments": {"title": "x"},
            "draft_hash": "hh",
        },
        replay_items=[{"type": "function_call", "call_id": "call_pg"}],
    )
    # Fresh guard — hydrate from PG only.
    g2 = ConfirmationGuard(confirm_sessions=PostgresConfirmSessionStore(DISPOSABLE_URL))
    loaded = g2.get_or_create_session(user_id="pg-u", chat_id="pg-c")
    assert loaded.pending_call_id == "call_pg"
    assert loaded.frozen_tool_intent is not None
    assert loaded.frozen_tool_intent["call_id"] == "call_pg"
