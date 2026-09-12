"""STORY-AIBRIDGE-06 G-01 — wire openai/gateway/http-error metric increments."""

from __future__ import annotations

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayExecutor, RecordingGatewayTransport, RawHttpResponse
from aibridge.interview import InterviewEngine
from aibridge.metrics import get_metrics, reset_metrics
from aibridge.responses_client import RecordingResponsesClient


def test_openai_calls_increment_on_interview_create() -> None:
    reset_metrics()
    engine = InterviewEngine(client=RecordingResponsesClient())
    before = get_metrics().openai_calls_total
    result = engine.run_turn(session_id="s-m1", user_text="hello metrics")
    assert result["ok"] is True
    assert get_metrics().openai_calls_total == before + 1
    body = get_metrics().render_prometheus()
    assert "aibridge_openai_calls_total 1" in body
    assert "hello metrics" not in body


def test_gateway_posts_increment_on_transport_request() -> None:
    reset_metrics()
    body = b'{"data":{"draft_id":"d1"},"trace_id":"t1"}'
    transport = RecordingGatewayTransport(
        scripted=[RawHttpResponse(status_code=201, body=body)]
    )
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        channel_bearer="ch-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        transport=transport,
    )
    before = get_metrics().gateway_posts_total
    result = ex.execute_stash({"payload": True}, gateway_authorized=True)
    assert result.http_posted is True
    assert get_metrics().gateway_posts_total == before + 1


def test_gateway_dry_run_does_not_increment_posts() -> None:
    reset_metrics()
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        dry_run=True,
        transport=RecordingGatewayTransport(),
    )
    ex.execute_stash({"payload": True}, gateway_authorized=True)
    assert get_metrics().gateway_posts_total == 0


def test_channel_http_errors_increment_on_401() -> None:
    reset_settings_cache()
    reset_confirmation_guard()
    reset_metrics()
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_GATEWAY_ORIGIN="https://gateway.example.invalid",
        AIBRIDGE_DRY_RUN=True,
    )
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    client = TestClient(app)
    before = get_metrics().channel_http_errors_total
    r = client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "m-401",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "1", "text": "x"},
        },
    )
    assert r.status_code == 401
    assert get_metrics().channel_http_errors_total == before + 1
    # /metrics itself must not count as channel error
    assert client.get("/metrics").status_code == 200
    assert get_metrics().channel_http_errors_total == before + 1
