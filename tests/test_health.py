"""Health/ready probes — z-paths and REQ9 short aliases (G2)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore


def test_healthz_ok(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_alias_parity_with_healthz(client: TestClient) -> None:
    """REQ9 G2 — GET /health same status/body as /healthz."""
    z = client.get("/healthz")
    short = client.get("/health")
    assert short.status_code == z.status_code == 200
    assert short.json() == z.json() == {"status": "ok"}


def test_readyz_ready_when_channel_auth_present(client: TestClient) -> None:
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_ready_alias_parity_with_readyz_when_ready(client: TestClient) -> None:
    """REQ9 G2 — GET /ready same status/body as /readyz when ready."""
    z = client.get("/readyz")
    short = client.get("/ready")
    assert short.status_code == z.status_code == 200
    assert short.json() == z.json()
    assert short.json()["status"] == "ready"


def test_readyz_fails_without_channel_token() -> None:
    reset_settings_cache()
    settings = Settings(
        _env_file=None,
        AIBRIDGE_CHANNEL_BEARER_TOKEN="",
        GATEWAY_SERVICE_API_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "channel_auth_missing"


def test_ready_alias_parity_with_readyz_when_not_ready() -> None:
    """REQ9 G2 — GET /ready same 503/reason as /readyz when not ready."""
    reset_settings_cache()
    settings = Settings(
        _env_file=None,
        AIBRIDGE_CHANNEL_BEARER_TOKEN="",
        GATEWAY_SERVICE_API_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    z = client.get("/readyz")
    short = client.get("/ready")
    assert short.status_code == z.status_code == 503
    assert short.json() == z.json()
    assert short.json()["reason"] == "channel_auth_missing"


def test_settings_port_alias() -> None:
    reset_settings_cache()
    settings = Settings(_env_file=None, PORT="9090")
    assert settings.port == 9090
