"""Shared fixtures for channel façade tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore


@pytest.fixture
def channel_token() -> str:
    return "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@pytest.fixture
def gateway_token() -> str:
    return "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


@pytest.fixture
def settings(channel_token: str, gateway_token: str) -> Settings:
    reset_settings_cache()
    return Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=channel_token,
        AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN="",
        DOGESTONIA_API_BEARER_TOKEN=gateway_token,
        AIBRIDGE_MAX_REQUEST_BYTES=65536,
        PORT=8080,
    )


@pytest.fixture
def store() -> EventDedupeStore:
    return EventDedupeStore()


@pytest.fixture
def client(settings: Settings, store: EventDedupeStore) -> TestClient:
    from aibridge.confirm import reset_confirmation_guard

    reset_confirmation_guard()
    app = create_app(settings=settings, dedupe_store=store)
    return TestClient(app)


@pytest.fixture
def auth_header(channel_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {channel_token}"}


@pytest.fixture
def turn_payload() -> dict:
    return {
        "channel": "telegram",
        "event_id": "1001",
        "principal": {"user_id": "42", "chat_id": "-100"},
        "message": {"message_id": "7", "text": "hello"},
    }
