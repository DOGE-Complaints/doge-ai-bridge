"""t02 — channel Bearer auth + equal-token readiness fail."""

from __future__ import annotations

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.auth import constant_time_token_match, is_channel_authorized
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore


def test_unauthenticated_channel_returns_401(
    client: TestClient, turn_payload: dict
) -> None:
    response = client.post("/v1/channel/turns", json=turn_payload)
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "unauthorized"
    assert "Authorization" not in body["error"]["message"]


def test_invalid_bearer_returns_401(
    client: TestClient, turn_payload: dict
) -> None:
    response = client.post(
        "/v1/channel/turns",
        json=turn_payload,
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401


def test_previous_token_overlap_accepted(
    channel_token: str, gateway_token: str, turn_payload: dict
) -> None:
    previous = "previous-token-cccccccccccccccccccccccccccccccc"
    reset_settings_cache()
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=channel_token,
        AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN=previous,
        DOGESTONIA_API_BEARER_TOKEN=gateway_token,
    )
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    response = client.post(
        "/v1/channel/turns",
        json=turn_payload,
        headers={"Authorization": f"Bearer {previous}"},
    )
    assert response.status_code == 200


def test_equal_channel_gateway_bearer_readyz_fail(
    channel_token: str,
) -> None:
    reset_settings_cache()
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=channel_token,
        DOGESTONIA_API_BEARER_TOKEN=channel_token,
    )
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "channel_gateway_bearer_equal"


def test_constant_time_match() -> None:
    assert constant_time_token_match("abc", ("abc",))
    assert not constant_time_token_match("abc", ("abd",))
    assert not constant_time_token_match("", ("abc",))


def test_is_channel_authorized(settings: Settings, channel_token: str) -> None:
    assert is_channel_authorized(f"Bearer {channel_token}", settings)
    assert not is_channel_authorized(None, settings)
    assert not is_channel_authorized("Basic x", settings)
