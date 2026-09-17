"""G-01 — create_app wires GatewayExecutor (no manual inject)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import get_confirmation_guard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayOutcome, HttpxGatewayTransport


def test_create_app_wires_executor_from_settings() -> None:
    reset_settings_cache()
    reset_confirmation_guard()
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        AIBRIDGE_DRY_RUN=True,
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example",
    )
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    guard = app.state.confirmation_guard
    assert guard.executor is not None
    assert guard.executor.dry_run is True
    assert isinstance(guard.executor.transport, HttpxGatewayTransport)
    assert guard.executor.transport.verify_tls is True


def test_testclient_send_dry_run_without_manual_inject() -> None:
    reset_settings_cache()
    reset_confirmation_guard()
    channel = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=channel,
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        AIBRIDGE_DRY_RUN=True,
    )
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    client = TestClient(app)
    headers = {"Authorization": f"Bearer {channel}"}

    # Mint Send token via process-local guard (same as app.state after create_app).
    guard = app.state.confirmation_guard
    sess = guard.get_or_create_session(user_id="42", chat_id="99")
    interpret = guard.offer_interpretation_confirm(sess.session_id)
    guard.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="42",
        chat_id="99",
    )
    guard.set_frozen_tool_intent(sess.session_id, {"schema_binding": {"x": 1}})
    send_actions = guard.offer_send_confirm(sess.session_id)
    tok = next(a["token"] for a in send_actions if a["style"] == "primary")

    response = client.post(
        "/v1/channel/actions",
        json={
            "channel": "telegram",
            "event_id": "gw-wire-1",
            "callback_query_id": "cb-wire",
            "principal": {"user_id": "42", "chat_id": "99"},
            "action_token": tok,
        },
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == GatewayOutcome.DRY_RUN_OK.value
    assert body["continuation_url"] is None
    assert "not sent" in body["reply_text"].lower()
    # Same guard object as get_confirmation_guard after create_app wiring.
    assert get_confirmation_guard() is guard
