"""STORY-AIBRIDGE-59 — interview port + env fail-closed (AC-AIB-12-01/02/05 · D4)."""

from __future__ import annotations

import inspect

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.auth import is_channel_authorized
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.interview_providers import (
    ALLOWED_INTERVIEW_PROVIDER_IDS,
    InterviewProviderConfigError,
    InterviewProviderFailureClass,
    InterviewProviderId,
    bind_interview_engine_at_wire,
    normalize_interview_provider_id,
    port_from_settings,
    registry_from_settings,
)
from aibridge.interview_providers.deepseek_slot import (
    DeepSeekInterviewProvider,
    DeferredDeepSeekInterviewClient,
)
from aibridge.interview_providers.openai_slot import OpenAIInterviewProvider
from aibridge.readiness import evaluate_readiness
from aibridge.responses_client import ProductionResponsesClient, ResponsesRequest


CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = {
        "_env_file": None,
        "AIBRIDGE_CHANNEL_BEARER_TOKEN": CHANNEL_TOKEN,
        "GATEWAY_SERVICE_API_TOKEN": GATEWAY_TOKEN,
        "GATEWAY_BASE_URL": "https://gateway.example.invalid",
        "SPA_BASE_URL": "https://spa.example.invalid",
        "OPENAI_API_KEY": "sk-test-not-real",
        "OPENAI_MODEL": "gpt-test",
        "AIBRIDGE_INTERVIEW_PROVIDER": "openai",
        "AIBRIDGE_DRY_RUN": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def test_ac_12_01_settings_loads_interview_provider() -> None:
    s = _settings(AIBRIDGE_INTERVIEW_PROVIDER="deepseek")
    assert s.interview_provider_normalized() == "deepseek"
    s2 = _settings(AIBRIDGE_INTERVIEW_PROVIDER="openai")
    assert s2.interview_provider_normalized() == "openai"
    assert ALLOWED_INTERVIEW_PROVIDER_IDS == frozenset({"deepseek", "openai"})


def test_ac_12_05_unset_empty_unknown_fail_closed() -> None:
    for raw, cls in (
        ("", InterviewProviderFailureClass.MISSING),
        ("   ", InterviewProviderFailureClass.MISSING),
        ("claude", InterviewProviderFailureClass.UNKNOWN),
        ("mock", InterviewProviderFailureClass.UNKNOWN),
    ):
        with pytest.raises(InterviewProviderConfigError) as ei:
            normalize_interview_provider_id(raw)
        assert ei.value.failure_class is cls

    unset = _settings(AIBRIDGE_INTERVIEW_PROVIDER="")
    assert unset.interview_provider_fail_closed() is True
    assert unset.interview_provider_fail_reason() == "interview_provider_missing"
    unknown = _settings(AIBRIDGE_INTERVIEW_PROVIDER="anthropic")
    assert unknown.interview_provider_fail_reason() == "interview_provider_unknown"


def test_l12_3_openai_nest_incomplete() -> None:
    s = _settings(OPENAI_API_KEY="", OPENAI_MODEL="")
    assert s.interview_provider_nest_incomplete() is True
    assert evaluate_readiness(s).reason == "interview_provider_incomplete"
    with pytest.raises(InterviewProviderConfigError) as ei:
        port_from_settings(s)
    assert ei.value.failure_class is InterviewProviderFailureClass.INCOMPLETE


def test_l12_3_deepseek_nest_required() -> None:
    incomplete = _settings(
        AIBRIDGE_INTERVIEW_PROVIDER="deepseek",
        AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY="",
        AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL="https://api.deepseek.com",
        AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL="deepseek-v4-pro",
    )
    assert incomplete.interview_provider_fail_reason() == "interview_provider_incomplete"
    complete = _settings(
        AIBRIDGE_INTERVIEW_PROVIDER="deepseek",
        AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY="ds-key",
        AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL="https://api.deepseek.com",
        AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL="deepseek-v4-pro",
        OPENAI_API_KEY="",
        OPENAI_MODEL="",
    )
    assert complete.interview_provider_fail_closed() is False
    port = port_from_settings(complete)
    assert isinstance(port, DeepSeekInterviewProvider)
    assert port.provider_id is InterviewProviderId.DEEPSEEK
    client = port.build_client(timeout_ms=1000, connect_timeout_ms=500)
    assert isinstance(client, DeferredDeepSeekInterviewClient)
    with pytest.raises(InterviewProviderConfigError) as ei:
        client.create(ResponsesRequest(payload={"store": False}))
    assert ei.value.failure_class is InterviewProviderFailureClass.ADAPTER_DEFERRED


def test_ac_12_02_worker_env_cannot_select_interview() -> None:
    """Worker selectors must not resolve interview registry (AC-02)."""
    s = _settings(
        AIBRIDGE_INTERVIEW_PROVIDER="openai",
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
        AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
        AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
        AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN="worker-s2s-cccccccccccccccccccccccccccccccc",
        AIBRIDGE_ALLOW_MOCK_PROVIDERS=True,
    )
    # Interview registry reads only AIBRIDGE_INTERVIEW_PROVIDER.
    reg = registry_from_settings(s)
    assert reg.provider_id is InterviewProviderId.OPENAI
    # Changing worker env alone cannot flip interview id.
    s_worker_only = _settings(
        AIBRIDGE_INTERVIEW_PROVIDER="deepseek",
        AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY="ds-key",
        AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL="https://api.deepseek.com",
        AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL="deepseek-v4-pro",
        AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
        AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="openai",
    )
    assert s_worker_only.interview_provider_normalized() == "deepseek"
    assert registry_from_settings(s_worker_only).provider_id is InterviewProviderId.DEEPSEEK
    # Source: registry code must not read worker settings fields.
    import aibridge.interview_providers.registry as reg_mod

    src = inspect.getsource(reg_mod.port_from_settings)
    assert "worker_text_brief" not in src
    assert "worker_image_poster" not in src
    assert "aibridge_worker" not in src


def test_port_home_not_under_providers() -> None:
    import aibridge.interview_providers as ip
    from aibridge.providers.ids import ProviderId as WorkerProviderId
    from pathlib import Path

    home = Path(ip.__file__ or "").resolve().parent
    assert home.name == "interview_providers"
    assert home.parent.name == "aibridge"
    assert (home.parent / "providers").is_dir()
    assert home != (home.parent / "providers")
    assert "deepseek" not in {p.value for p in WorkerProviderId}
    assert InterviewProviderId.DEEPSEEK.value == "deepseek"


def test_d4_wire_bind_openai_before_engine() -> None:
    s = _settings(AIBRIDGE_INTERVIEW_PROVIDER="openai")
    engine = bind_interview_engine_at_wire(s, timeout_ms=5000, connect_timeout_ms=1000)
    assert isinstance(engine.client, ProductionResponsesClient)
    assert engine.model == "gpt-test"


def test_d4_wire_fail_closed_no_recording_fallback() -> None:
    s = _settings(AIBRIDGE_INTERVIEW_PROVIDER="")
    with pytest.raises(InterviewProviderConfigError) as ei:
        bind_interview_engine_at_wire(s, timeout_ms=5000, connect_timeout_ms=1000)
    assert ei.value.failure_class is InterviewProviderFailureClass.MISSING
    with pytest.raises(RuntimeError, match="interview provider fail-closed"):
        create_app(settings=s, dedupe_store=EventDedupeStore())


def test_openai_port_slot() -> None:
    port = port_from_settings(_settings())
    assert isinstance(port, OpenAIInterviewProvider)
    assert port.provider_id is InterviewProviderId.OPENAI


def test_readyz_interview_provider_missing() -> None:
    s = _settings(AIBRIDGE_INTERVIEW_PROVIDER="")
    result = evaluate_readiness(s)
    assert result.ready is False
    assert result.reason == "interview_provider_missing"
    client = TestClient(
        create_app(
            settings=_settings(),
            dedupe_store=EventDedupeStore(),
        )
    )
    # Valid openai nest → ready
    assert client.get("/readyz").status_code == 200


def test_trust_channel_bearer_not_model_keys() -> None:
    """Channel Bearer auth must not consult model vendor keys (arch 01 §4)."""
    s = _settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL_TOKEN,
        OPENAI_API_KEY="sk-should-not-authorize",
        AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY="ds-should-not-authorize",
    )
    assert is_channel_authorized(f"Bearer {CHANNEL_TOKEN}", s) is True
    assert is_channel_authorized("Bearer sk-should-not-authorize", s) is False
    assert is_channel_authorized("Bearer ds-should-not-authorize", s) is False
    src = inspect.getsource(is_channel_authorized)
    assert "openai" not in src.lower()
    assert "deepseek" not in src.lower()
    assert "interview" not in src.lower()
