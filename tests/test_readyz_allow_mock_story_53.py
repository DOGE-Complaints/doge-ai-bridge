"""STORY-AIBRIDGE-53 — readyz + allow-mock refuse (AC-10-08 / AC-10-09)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.readiness import evaluate_readiness
from aibridge.worker_accept import WORKER_ACCEPT_PATH

WORKER_TOKEN = "worker-s2s-cccccccccccccccccccccccccccccccc"
CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = {
        "_env_file": None,
        "AIBRIDGE_CHANNEL_BEARER_TOKEN": CHANNEL_TOKEN,
        "AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN": "",
        "GATEWAY_SERVICE_API_TOKEN": GATEWAY_TOKEN,
        "AIBRIDGE_MAX_REQUEST_BYTES": 65536,
        "PORT": 8080,
        "GATEWAY_BASE_URL": "https://gateway.example.invalid",
        "SPA_BASE_URL": "https://spa.example.invalid",
        "OPENAI_API_KEY": "sk-test-not-real",
        "OPENAI_MODEL": "gpt-test",
        "AIBRIDGE_DRY_RUN": True,
        "AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED": True,
        "AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN": WORKER_TOKEN,
        "AIBRIDGE_WORKER_TEXT_BRIEF_MODEL": "gpt-test-brief",
        "AIBRIDGE_WORKER_IMAGE_POSTER_MODEL": "img-test-poster",
        "AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL": "aibridge-storage-cred-test",
        "AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER": "mock",
        "AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER": "mock",
        "AIBRIDGE_ALLOW_MOCK_PROVIDERS": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))


def test_allow_mock_env_surface_truthy() -> None:
    assert _settings(AIBRIDGE_ALLOW_MOCK_PROVIDERS=True).allow_mock_providers() is True
    assert _settings(AIBRIDGE_ALLOW_MOCK_PROVIDERS=False).allow_mock_providers() is False
    assert _settings(AIBRIDGE_ALLOW_MOCK_PROVIDERS="1").allow_mock_providers() is True
    assert _settings(AIBRIDGE_ALLOW_MOCK_PROVIDERS="0").allow_mock_providers() is False


def test_ac_10_08_readyz_mock_mock_without_openai_key() -> None:
    s = _settings(
        OPENAI_API_KEY="",
        OPENAI_MODEL="",
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock",
        AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
        AIBRIDGE_ALLOW_MOCK_PROVIDERS=True,
    )
    assert s.worker_openai_presence_required() is False
    result = evaluate_readiness(s)
    assert result.ready is True
    r = _client(s).get("/readyz")
    assert r.status_code == 200
    assert r.json() == {"status": "ready"}


def test_openai_still_required_when_worker_slot_openai() -> None:
    s = _settings(
        OPENAI_API_KEY="",
        OPENAI_MODEL="",
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
        AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
        AIBRIDGE_ALLOW_MOCK_PROVIDERS=True,
    )
    assert s.worker_openai_presence_required() is True
    result = evaluate_readiness(s)
    assert result.ready is False
    assert result.reason == "openai_config_missing"


def test_ac_10_09_readyz_refuse_mock_without_allow() -> None:
    s = _settings(AIBRIDGE_ALLOW_MOCK_PROVIDERS=False)
    assert s.worker_mock_not_allowed_fail_closed() is True
    result = evaluate_readiness(s)
    assert result.ready is False
    assert result.reason == "worker_mock_not_allowed"
    r = _client(s).get("/readyz")
    assert r.status_code == 503
    assert r.json()["reason"] == "worker_mock_not_allowed"


def test_ac_10_09_accept_refuse_mock_without_allow() -> None:
    s = _settings(AIBRIDGE_ALLOW_MOCK_PROVIDERS=False)
    r = _client(s).post(
        WORKER_ACCEPT_PATH,
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
        json={"issue_id": "iss-53", "job_id": "job-53", "corpus": {"stories": []}},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "worker_mock_not_allowed"


def test_both_openai_slots_skip_allow_mock_gate() -> None:
    s = _settings(
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
        AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="openai",
        AIBRIDGE_ALLOW_MOCK_PROVIDERS=False,
    )
    assert s.worker_uses_mock_provider() is False
    assert s.worker_mock_not_allowed_fail_closed() is False
    result = evaluate_readiness(s)
    assert result.ready is True


def test_channel_readyz_still_requires_openai_when_worker_off() -> None:
    s = _settings(
        AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=False,
        OPENAI_API_KEY="",
        OPENAI_MODEL="",
        AIBRIDGE_ALLOW_MOCK_PROVIDERS=False,
    )
    assert s.worker_openai_presence_required() is True
    result = evaluate_readiness(s)
    assert result.ready is False
    assert result.reason == "openai_config_missing"
