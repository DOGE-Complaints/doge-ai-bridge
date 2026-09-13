"""STORY-AIBRIDGE-13 — Wave-1 ASGI E2E (fake OpenAI + fake/dry-run gateway + disposable Postgres).

Covers REQ-03 §4 AC #1–#9 for wave 1. Never contacts live OpenAI / n8n / Railway.
"""

from __future__ import annotations

import pytest

from aibridge.confirm_fsm import SessionState
from aibridge.gateway import GatewayOutcome, STASH_REPLY
from aibridge.pg_runtime import GatewayAttemptStore
from story13_e2e_helpers import (
    action_body,
    assert_channel_error_conforms,
    assert_channel_success_conforms,
    build_e2e_harness,
    fc_openai_payload,
    followup_openai_payload,
    ok_201,
    pg_available,
    rebuild_app_same_pg,
    text_openai_payload,
    turn_body,
)

pytestmark = pytest.mark.skipif(
    not pg_available(),
    reason="disposable Postgres (.pgdata-test) not running — ./scripts/start-disposable-pg.sh",
)


# --- t01 harness smoke ---


def test_story_13_e2e_harness_pg_fakes_ready() -> None:
    h = build_e2e_harness(openai_scripted=[text_openai_payload()])
    assert h.app.state.dedupe_store is not None
    assert h.guard.gateway_attempts is not None
    assert h.guard.confirm_sessions is not None
    assert h.guard.validation_context is not None
    assert h.transport.calls == []
    assert h.openai.gateway_calls == 0


# --- t02 AC #1–#2 ---


def test_story_13_e2e_turns_interview_not_received() -> None:
    h = build_e2e_harness(
        openai_scripted=[text_openai_payload("Wave1 interview answer")]
    )
    r = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-turn-1", text="hello e2e"),
        headers=h.auth_header,
    )
    assert r.status_code == 200
    body = r.json()
    assert_channel_success_conforms(body)
    assert not str(body["reply_text"]).startswith("Received:")
    assert "Received:" not in str(body["reply_text"])
    assert body["reply_text"] == "Wave1 interview answer"
    assert len(h.openai.calls) == 1


def test_story_13_e2e_transport_replay_stored_status_body() -> None:
    h = build_e2e_harness(
        openai_scripted=[text_openai_payload("First compute only")]
    )
    payload = turn_body(event_id="e2e-replay-1", text="same event")
    r1 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r1.status_code == 200
    body1 = r1.json()
    assert_channel_success_conforms(body1)
    calls_after_first = len(h.openai.calls)

    r2 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r2.status_code == 200
    body2 = r2.json()
    assert_channel_success_conforms(body2)
    assert body2 == body1
    assert len(h.openai.calls) == calls_after_first
    assert h.transport.calls == []


def test_story_13_e2e_replay_survives_restart() -> None:
    h = build_e2e_harness(
        openai_scripted=[text_openai_payload("Persist for restart")]
    )
    payload = turn_body(event_id="e2e-replay-restart", text="restart me")
    r1 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r1.status_code == 200
    body1 = r1.json()

    h2 = rebuild_app_same_pg(h)
    r2 = h2.client.post("/v1/channel/turns", json=payload, headers=h2.auth_header)
    assert r2.status_code == 200
    body2 = r2.json()
    assert body2["request_id"] == body1["request_id"]
    assert body2["reply_text"] == body1["reply_text"]
    assert len(h2.openai.calls) == 0
    assert h2.transport.calls == []


# --- t03 AC #3–#4 ---


def test_story_13_e2e_fc_interpretation_no_gateway() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_e2e_fc"),
        ],
        gateway_scripted=[ok_201()],
    )
    # Ordinary turn → interpretation buttons
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-fc-0", text="start"),
        headers=h.auth_header,
    )
    assert r0.status_code == 200
    acts0 = r0.json()["actions"]
    assert acts0
    interpret_tok = next(a["token"] for a in acts0 if a["style"] == "success")

    r_i = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-fc-i", token=interpret_tok),
        headers=h.auth_header,
    )
    assert r_i.status_code == 200
    bi = r_i.json()
    assert_channel_success_conforms(bi)
    assert bi["state"] == SessionState.INTERPRETATION_CONFIRMED.value
    assert h.transport.calls == []

    # FC turn after interpretation
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-fc-1", text="stash please"),
        headers=h.auth_header,
    )
    assert r1.status_code == 200
    b1 = r1.json()
    assert_channel_success_conforms(b1)
    assert b1["state"] == SessionState.AWAITING_SEND_CONFIRM.value
    assert len(b1["actions"]) == 3
    sess = h.guard.get_or_create_session(user_id="42", chat_id="-100")
    assert sess.pending_call_id == "call_e2e_fc"
    assert sess.frozen_tool_intent is not None
    assert "schema_version" in sess.frozen_tool_intent["arguments"]
    # No gateway until Send
    assert h.transport.calls == []


# --- t04 AC #5–#6 ---


def test_story_13_e2e_send_fake_stash_and_fco() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_orig_13"),
            followup_openai_payload("Draft noted — not published."),
        ],
        gateway_scripted=[ok_201("draft-e2e-13")],
        dry_run_gateway=False,
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-send-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-send-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-send-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(
        a["token"] for a in r1.json()["actions"] if a["style"] == "primary"
    )
    r_s = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-send-s", token=send_tok, callback_query_id="cbs"),
        headers=h.auth_header,
    )
    assert r_s.status_code == 200
    bs = r_s.json()
    assert_channel_success_conforms(bs)
    assert bs["outcome"] == GatewayOutcome.STASHED.value
    assert bs["draft_id"] == "draft-e2e-13"
    assert bs["continuation_url"]
    # STASH_REPLY explicitly denies publication (must not claim published Story).
    assert bs["reply_text"] == STASH_REPLY
    assert "not a published Story" in bs["reply_text"]
    # Exactly one fake HTTPS attempt
    assert len(h.transport.calls) == 1
    assert "/story-drafts" in h.transport.calls[0]["url"]
    assert "gateway.example.invalid" in h.transport.calls[0]["url"]
    # function_call_output with original call_id
    assert len(h.openai.calls) == 3
    follow_input = h.openai.calls[2]["input"]
    fco = [x for x in follow_input if x.get("type") == "function_call_output"]
    assert fco and fco[0]["call_id"] == "call_orig_13"


def test_story_13_e2e_send_dryrun_zero_real_https() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_dry"),
            followup_openai_payload("Dry-run follow-up."),
        ],
        gateway_scripted=[],
        dry_run_gateway=True,
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-dry-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-dry-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-dry-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(
        a["token"] for a in r1.json()["actions"] if a["style"] == "primary"
    )
    r_s = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-dry-s", token=send_tok, callback_query_id="cbd"),
        headers=h.auth_header,
    )
    assert r_s.status_code == 200
    bs = r_s.json()
    assert_channel_success_conforms(bs)
    assert bs["outcome"] == GatewayOutcome.DRY_RUN_OK.value
    assert h.transport.calls == []


# --- t05 AC #7–#9 ---


def test_story_13_e2e_restart_pending_confirm_preserves_state() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_pending"),
        ],
        gateway_scripted=[ok_201()],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-pend-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-pend-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-pend-1", text="go"),
        headers=h.auth_header,
    )
    assert r1.json()["state"] == SessionState.AWAITING_SEND_CONFIRM.value
    actions_before = r1.json()["actions"]
    assert len(actions_before) == 3
    send_tok = next(a["token"] for a in actions_before if a["style"] == "primary")
    sess = h.guard.get_or_create_session(user_id="42", chat_id="-100")
    pending_call = sess.pending_call_id
    frozen = dict(sess.frozen_tool_intent or {})

    h2 = rebuild_app_same_pg(
        h,
        openai_scripted=[followup_openai_payload()],
        gateway_scripted=[ok_201()],
    )
    sess2 = h2.guard.get_or_create_session(user_id="42", chat_id="-100")
    assert sess2.state is SessionState.AWAITING_SEND_CONFIRM
    assert sess2.pending_call_id == pending_call
    assert sess2.frozen_tool_intent == frozen
    # Pre-restart Send token still valid (PG action_token) — buttons/state survive.
    r_s = h2.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="e2e-pend-s", token=send_tok, callback_query_id="cbp"
        ),
        headers=h2.auth_header,
    )
    assert r_s.status_code == 200
    assert r_s.json()["outcome"] == GatewayOutcome.STASHED.value
    assert len(h2.transport.calls) == 1


def test_story_13_e2e_restart_unknown_outcome_no_auto_resend() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_unk"),
        ],
        gateway_scripted=[ok_201()],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-unk-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-unk-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-unk-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(
        a["token"] for a in r1.json()["actions"] if a["style"] == "primary"
    )
    sess = h.guard.get_or_create_session(user_id="42", chat_id="-100")
    # Simulate crash mid-Send: executing attempt committed, no outcome
    assert isinstance(h.guard.gateway_attempts, GatewayAttemptStore)
    h.guard.gateway_attempts.create_executing(
        session_id=sess.session_id, revision=sess.revision
    )
    sess.state = SessionState.EXECUTING
    h.guard._persist_session(sess)  # noqa: SLF001

    h2 = rebuild_app_same_pg(h)
    # Boot must not auto-call gateway
    assert h2.transport.calls == []
    sess2 = h2.guard.get_or_create_session(user_id="42", chat_id="-100")
    h2.guard.recover_stale_executing(
        session_id=sess2.session_id, revision=sess2.revision
    )
    sess2 = h2.guard.get_or_create_session(user_id="42", chat_id="-100")
    assert sess2.state is SessionState.UNKNOWN_OUTCOME
    assert h2.guard.send_blocked_for_revision(sess2) is True
    # Stale Send token must not trigger gateway HTTPS after unknown_outcome.
    r_s = h2.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="e2e-unk-s", token=send_tok, callback_query_id="cbu"
        ),
        headers=h2.auth_header,
    )
    assert r_s.status_code in {200, 409}
    assert h2.transport.calls == []


def test_story_13_e2e_openapi_success_replay_and_non2xx() -> None:
    h = build_e2e_harness(openai_scripted=[text_openai_payload("oas ok")])
    payload = turn_body(event_id="e2e-oas-1", text="hi")
    r1 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r1.status_code == 200
    assert_channel_success_conforms(r1.json())

    r2 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r2.status_code == 200
    assert_channel_success_conforms(r2.json())

    r401 = h.client.post("/v1/channel/turns", json=payload)
    assert r401.status_code == 401
    assert_channel_error_conforms(r401.json())
