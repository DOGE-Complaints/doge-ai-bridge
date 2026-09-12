"""t01 — healthz / readyz / PORT settings."""

from __future__ import annotations

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore


def test_healthz_ok(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_ready_when_channel_auth_present(client: TestClient) -> None:
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_readyz_fails_without_channel_token() -> None:
    reset_settings_cache()
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "channel_auth_missing"


def test_settings_port_alias() -> None:
    reset_settings_cache()
    settings = Settings(PORT="9090")
    assert settings.port == 9090
