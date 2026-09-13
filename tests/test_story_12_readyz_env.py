"""STORY-AIBRIDGE-12 — env canon, strict /readyz, dry-run gate, bounded 500."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import default_executor_from_settings
from aibridge.readiness import evaluate_readiness


def _ready_settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_API_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(**base)


def test_canonical_api_base_url_used_by_gateway_executor() -> None:
    settings = _ready_settings(
        DOGESTONIA_API_BASE_URL="https://canonical.example.invalid",
        DOGESTONIA_GATEWAY_ORIGIN="",
    )
    ex = default_executor_from_settings(settings)
    assert ex.origin == "https://canonical.example.invalid"


def test_gateway_origin_alias_fallback() -> None:
    settings = _ready_settings(
        DOGESTONIA_API_BASE_URL="",
        DOGESTONIA_GATEWAY_ORIGIN="https://alias.example.invalid",
    )
    assert settings.resolved_gateway_base_url() == "https://alias.example.invalid"
    ex = default_executor_from_settings(settings)
    assert ex.origin == "https://alias.example.invalid"


def test_readyz_fails_on_base_url_conflict() -> None:
    settings = _ready_settings(
        DOGESTONIA_API_BASE_URL="https://a.example.invalid",
        DOGESTONIA_GATEWAY_ORIGIN="https://b.example.invalid",
    )
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "gateway_base_url_conflict"


def test_settings_accept_ttl_rate_log_budget_knobs() -> None:
    settings = _ready_settings(
        AIBRIDGE_SESSION_TTL_SECONDS=3600,
        AIBRIDGE_ACTION_TOKEN_TTL_SECONDS=900,
        AIBRIDGE_MAX_RESPONSE_BYTES=8192,
        AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS=1000,
        AIBRIDGE_HTTP_TOTAL_TIMEOUT_MS=5000,
        AIBRIDGE_LOG_LEVEL="DEBUG",
        AIBRIDGE_PRINCIPAL_RATE_LIMIT=10,
        AIBRIDGE_GLOBAL_RATE_LIMIT=100,
        AIBRIDGE_MAX_INPUT_TOKENS=1000,
    )
    assert settings.aibridge_session_ttl_seconds == 3600
    assert settings.aibridge_action_token_ttl_seconds == 900
    assert settings.aibridge_max_response_bytes == 8192
    assert settings.aibridge_http_connect_timeout_ms == 1000
    assert settings.aibridge_http_total_timeout_ms == 5000
    assert settings.aibridge_log_level == "DEBUG"
    assert settings.aibridge_principal_rate_limit == 10
    assert settings.aibridge_global_rate_limit == 100
    assert settings.aibridge_max_input_tokens == 1000


def test_readyz_ok_when_strict_checks_pass() -> None:
    settings = _ready_settings()
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readyz_fails_openai_missing() -> None:
    settings = _ready_settings(OPENAI_API_KEY="", OPENAI_MODEL="")
    result = evaluate_readiness(settings)
    assert result.ready is False
    assert result.reason == "openai_config_missing"


def test_readyz_fails_http_gateway_origin() -> None:
    settings = _ready_settings(DOGESTONIA_API_BASE_URL="http://insecure.example.invalid")
    result = evaluate_readiness(settings)
    assert result.ready is False
    assert result.reason == "gateway_base_url_not_https"


def test_dry_run_false_fails_readyz_until_schema_complete() -> None:
    settings = _ready_settings(AIBRIDGE_DRY_RUN=False)
    client = TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "dry_run_required"


def test_dry_run_true_passes_dry_run_gate() -> None:
    settings = _ready_settings(AIBRIDGE_DRY_RUN=True)
    result = evaluate_readiness(settings)
    assert result.ready is True


def test_schema_validation_complete_lifts_dry_run_gate() -> None:
    settings = _ready_settings(
        AIBRIDGE_DRY_RUN=False,
        AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=True,
    )
    result = evaluate_readiness(settings)
    assert result.ready is True


def test_unhandled_channel_exception_returns_bounded_500(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = _ready_settings()
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())

    async def _boom(*_a: object, **_k: object) -> object:
        raise RuntimeError("secret=sk-leak should not appear")

    monkeypatch.setattr("aibridge.app.process_turn_async", _boom)
    client = TestClient(app, raise_server_exceptions=False)
    response = client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "500-test",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "1", "text": "x"},
        },
        headers={
            "Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        },
    )
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "internal_error"
    assert "request_id" in body
    assert "sk-leak" not in response.text
    assert "RuntimeError" not in response.text
    assert "traceback" not in response.text.lower()
