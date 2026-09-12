"""STORY-AIBRIDGE-05 — gateway executor, dry-run, outcomes (recorded fixtures)."""

from __future__ import annotations

import json

import pytest

from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import IllegalTransitionError, SessionState
from aibridge.gateway import (
    STASH_PATH,
    STASH_REPLY,
    GatewayExecutor,
    GatewayOutcome,
    RecordingGatewayTransport,
    RawHttpResponse,
    build_continuation_url,
    map_http_outcome,
    parse_success_body,
)


def _ok_201(draft_id: str = "draft-abc", trace_id: str = "trace-xyz") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": trace_id}).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard_with_executor(**kwargs: object) -> tuple[ConfirmationGuard, RecordingGatewayTransport]:
    transport = RecordingGatewayTransport(
        scripted=list(kwargs.pop("scripted", [_ok_201()]))  # type: ignore[arg-type]
    )
    if "raise_on_call" in kwargs:
        transport.raise_on_call = kwargs.pop("raise_on_call")  # type: ignore[assignment]
    executor = GatewayExecutor(
        origin=str(kwargs.pop("origin", "https://gateway.example.invalid")),
        gateway_bearer=str(kwargs.pop("gateway_bearer", "gw-secret")),
        channel_bearer=str(kwargs.pop("channel_bearer", "ch-secret")),
        dry_run=bool(kwargs.pop("dry_run", False)),
        redirect_base=str(kwargs.pop("redirect_base", "https://spa.example")),
        transport=transport,
    )
    assert not kwargs
    return ConfirmationGuard(executor=executor), transport


def _send_flow(g: ConfirmationGuard) -> dict:
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="1",
        chat_id="2",
    )
    g.set_frozen_tool_intent(sess.session_id, {"schema_binding": {"x": 1}})
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    return g.consume_action_token(send_tok, user_id="1", chat_id="2")


# --- t01 constrained HTTPS + bearer ---


def test_executor_uses_gateway_bearer_never_channel() -> None:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-only",
        channel_bearer="channel-only",
        transport=transport,
        redirect_base="https://spa.example",
    )
    result = ex.execute_stash({"a": 1}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.STASHED
    assert len(transport.calls) == 1
    auth = transport.calls[0]["headers"]["Authorization"]
    assert auth == "Bearer gw-only"
    assert "channel-only" not in auth
    assert transport.calls[0]["url"].endswith(STASH_PATH)
    assert transport.calls[0]["allow_redirects"] is False


def test_executor_rejects_equal_channel_and_gateway_bearer() -> None:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="same-token",
        channel_bearer="same-token",
        transport=transport,
    )
    result = ex.execute_stash({"a": 1}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.INTERNAL_BRIDGE_ERROR
    assert transport.calls == []


def test_executor_requires_https_origin() -> None:
    ex = GatewayExecutor(
        origin="http://insecure.example",
        gateway_bearer="gw",
        transport=RecordingGatewayTransport(scripted=[_ok_201()]),
    )
    result = ex.execute_stash({"a": 1}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.INTERNAL_BRIDGE_ERROR
    assert result.http_posted is False


def test_blocked_without_send_authorization() -> None:
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        transport=RecordingGatewayTransport(scripted=[_ok_201()]),
    )
    result = ex.execute_stash({"a": 1}, gateway_authorized=False)
    assert result.outcome is GatewayOutcome.BLOCKED_BY_CONFIRMATION
    assert result.http_posted is False


# --- t02 verify 201 ---


def test_malformed_201_not_stashed() -> None:
    bad = RawHttpResponse(
        status_code=201,
        body=b'{"data": {}, "trace_id": "t"}',
    )
    transport = RecordingGatewayTransport(scripted=[bad])
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        transport=transport,
        redirect_base="https://spa.example",
    )
    result = ex.execute_stash({"a": 1}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.CONTRACT_MISMATCH
    assert result.draft_id is None
    assert result.continuation_url is None


def test_valid_201_stashed_with_ids() -> None:
    draft_id, trace_id, err = parse_success_body(_ok_201().body)
    assert err is None
    assert draft_id == "draft-abc"
    assert trace_id == "trace-xyz"
    assert map_http_outcome(201, _ok_201().body) is GatewayOutcome.STASHED


# --- t03 outcome map + unknown no retry ---


def test_timeout_maps_unknown_and_blocks_resend() -> None:
    g, transport = _guard_with_executor(raise_on_call=TimeoutError("timeout"))
    result = _send_flow(g)
    assert result["ok"] is True
    assert result["outcome"] == GatewayOutcome.UNKNOWN_OUTCOME.value
    assert result["state"] == SessionState.UNKNOWN_OUTCOME.value
    assert "unknown-outcome-reconciliation" in result["reply_text"]
    assert len(transport.calls) == 1

    sess = g.get_session(result["session_id"])
    assert sess is not None
    assert g.send_blocked_for_revision(sess) is True
    with pytest.raises(IllegalTransitionError):
        # Need interpretation_confirmed path — after unknown, offer_send blocked.
        g.set_frozen_tool_intent(sess.session_id, {"a": 1})
        sess.state = SessionState.INTERPRETATION_CONFIRMED
        g.offer_send_confirm(sess.session_id)


def test_unknown_blocks_confirm_send_same_revision() -> None:
    g, _transport = _guard_with_executor(raise_on_call=TimeoutError("read timeout"))
    result = _send_flow(g)
    assert result["outcome"] == GatewayOutcome.UNKNOWN_OUTCOME.value
    sess = g.get_session(result["session_id"])
    assert sess is not None
    assert sess.unknown_outcome_revision == sess.revision

    # Edit clears block for new revision.
    g.apply_edit(sess.session_id)
    assert sess.unknown_outcome_revision is None


# --- t04 dry-run ---


def test_dry_run_validates_without_post() -> None:
    g, transport = _guard_with_executor(dry_run=True, scripted=[_ok_201()])
    result = _send_flow(g)
    assert result["ok"] is True
    assert result["outcome"] == GatewayOutcome.DRY_RUN_OK.value
    assert result["gateway_invocations"] == 0
    assert transport.calls == []
    assert "not sent" in result["reply_text"].lower()
    assert "published" not in result["reply_text"].lower()
    assert result["continuation_url"] is None
    assert result["state"] == SessionState.EXECUTING.value


# --- t05 continuation + copy ---


def test_continuation_url_only_when_stashed() -> None:
    g, _t = _guard_with_executor(redirect_base="https://spa.example")
    result = _send_flow(g)
    assert result["outcome"] == GatewayOutcome.STASHED.value
    assert result["state"] == SessionState.STASHED.value
    assert result["draft_id"] == "draft-abc"
    assert result["continuation_url"] == build_continuation_url(
        redirect_base="https://spa.example", draft_id="draft-abc"
    )
    assert result["reply_text"] == STASH_REPLY
    assert "not a published Story" in result["reply_text"]
    assert "Story published" not in result["reply_text"]


def test_non_stashed_has_no_continuation() -> None:
    bad = RawHttpResponse(status_code=201, body=b'{"oops": true}')
    g, _t = _guard_with_executor(scripted=[bad], redirect_base="https://spa.example")
    result = _send_flow(g)
    assert result["outcome"] == GatewayOutcome.CONTRACT_MISMATCH.value
    assert result["continuation_url"] is None
    assert result["draft_id"] is None
