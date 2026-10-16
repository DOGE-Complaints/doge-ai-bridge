"""STORY-AIBRIDGE-51 — provider ports + env registry (AC-10-01/02/05 + nest)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.providers import (
    ProviderConfigError,
    ProviderFailureClass,
    ProviderId,
    registry_from_settings,
    resolve_image_poster_provider,
    resolve_text_brief_provider,
)
from aibridge.providers.adapters import (
    MockImagePosterProvider,
    MockTextBriefProvider,
    OpenAIImagePosterProvider,
    OpenAITextBriefProvider,
)
from aibridge.providers.registry import normalize_provider_id
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
        "AIBRIDGE_ALLOW_MOCK_PROVIDERS": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))


def test_unset_provider_defaults_to_mock() -> None:
    s = _settings(
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="",
        AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="",
    )
    assert s.worker_text_brief_provider_normalized() == "mock"
    assert s.worker_image_poster_provider_normalized() == "mock"
    assert normalize_provider_id("", slot="text_brief") is ProviderId.MOCK
    assert normalize_provider_id(None, slot="image_poster") is ProviderId.MOCK


def test_ac_10_01_text_slot_resolves_via_port() -> None:
    mock = resolve_text_brief_provider(_settings(AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock"))
    assert isinstance(mock, MockTextBriefProvider)
    assert mock.provider_id is ProviderId.MOCK
    oai = resolve_text_brief_provider(
        _settings(AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai")
    )
    assert isinstance(oai, OpenAITextBriefProvider)
    assert oai.provider_id is ProviderId.OPENAI


def test_ac_10_02_image_slot_independent_of_text() -> None:
    reg = registry_from_settings(
        _settings(
            AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
            AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
        )
    )
    assert reg.text_provider_id is ProviderId.OPENAI
    assert reg.image_provider_id is ProviderId.MOCK
    assert isinstance(reg.resolve_text(), OpenAITextBriefProvider)
    assert isinstance(reg.resolve_image(), MockImagePosterProvider)
    flipped = registry_from_settings(
        _settings(
            AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock",
            AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="openai",
        )
    )
    assert flipped.text_provider_id is ProviderId.MOCK
    assert flipped.image_provider_id is ProviderId.OPENAI
    assert isinstance(flipped.resolve_image(), OpenAIImagePosterProvider)


def test_model_nest_openai_only_readyz_and_accept() -> None:
    # mock + empty model → not fail-closed
    mock_empty = _settings(
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock",
        AIBRIDGE_WORKER_TEXT_BRIEF_MODEL="",
        AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
        AIBRIDGE_WORKER_IMAGE_POSTER_MODEL="",
    )
    assert not mock_empty.worker_text_brief_fail_closed()
    assert not mock_empty.worker_image_poster_fail_closed()
    client = _client(mock_empty)
    assert client.get("/readyz").status_code == 200

    # openai + empty model → fail-closed
    oai_empty = _settings(
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
        AIBRIDGE_WORKER_TEXT_BRIEF_MODEL="",
    )
    assert oai_empty.worker_text_brief_fail_closed()
    r = _client(oai_empty).get("/readyz")
    assert r.status_code == 503
    assert r.json()["reason"] == "worker_text_brief_missing"


def test_ac_10_05_unknown_provider_fail_closed_no_silent_openai() -> None:
    with pytest.raises(ProviderConfigError) as exc:
        normalize_provider_id("anthropic", slot="text_brief")
    assert exc.value.failure_class is ProviderFailureClass.UNKNOWN_PROVIDER
    # Must not resolve as OpenAI
    assert "openai" not in str(exc.value).lower() or "unknown" in str(exc.value).lower()

    bad = _settings(AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="anthropic")
    assert bad.worker_provider_unknown_fail_closed()
    client = _client(bad)
    r_ready = client.get("/readyz")
    assert r_ready.status_code == 503
    assert r_ready.json()["reason"] == "worker_provider_unknown"
    r_accept = client.post(
        WORKER_ACCEPT_PATH,
        json={"issue_id": "i1", "generation_version": "v1", "corpus": {"title": "t"}},
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r_accept.status_code == 503
    assert r_accept.json()["error"]["code"] == "worker_provider_unknown"


def test_resolve_image_poster_provider_helper() -> None:
    port = resolve_image_poster_provider(
        _settings(AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock")
    )
    assert port.provider_id is ProviderId.MOCK


def test_channel_auth_unchanged_by_worker_providers() -> None:
    """L10-1: channel bearer path still distinct from worker provider registry."""
    s = _settings(AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai")
    assert s.channel_auth_configured()
    assert s.aibridge_channel_bearer_token == CHANNEL_TOKEN
    # Worker provider does not replace channel openai presence helper.
    assert s.openai_presence_ok()
