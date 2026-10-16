"""STORY-AIBRIDGE-55 — provider docs + verify matrix (AC-10-07 + arch 03 surfaces).

Does not invent live OpenAI SUCCESS — residual Unknown; sibling story tests remain SSOT.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.providers.adapters import (
    OpenAIImagePosterProvider,
    OpenAITextBriefProvider,
)
from aibridge.providers.errors import ProviderConfigError, ProviderFailureClass
from aibridge.providers.ids import ProviderId
from aibridge.providers.registry import registry_from_settings
from aibridge.readiness import evaluate_readiness
from aibridge.worker_accept import WORKER_ACCEPT_PATH

WORKER_TOKEN = "worker-s2s-cccccccccccccccccccccccccccccccc"
CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TEXT_BRIEF_MODEL = "gpt-test-brief"
IMAGE_POSTER_MODEL = "img-test-poster"
STORAGE_CREDENTIAL = "aibridge-storage-cred-test"

_REPO = Path(__file__).resolve().parents[1]
_GOLDEN = json.loads(
    (Path(__file__).parent / "fixtures" / "sense_brief_golden_l2.json").read_text(
        encoding="utf-8"
    )
)

# Residual fact — do not invent live vendor SUCCESS in this wave.
RESIDUAL_LIVE_OPENAI_SUCCESS_UNKNOWN = True


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
        "AIBRIDGE_WORKER_TEXT_BRIEF_MODEL": TEXT_BRIEF_MODEL,
        "AIBRIDGE_WORKER_IMAGE_POSTER_MODEL": IMAGE_POSTER_MODEL,
        "AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL": STORAGE_CREDENTIAL,
        "AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER": "mock",
        "AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER": "mock",
        "AIBRIDGE_ALLOW_MOCK_PROVIDERS": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))


def test_ac_10_07_runtime_docs_present() -> None:
    for rel in (
        "docs/runtime-docs/02-ai-provider-selection.md",
        "docs/runtime-docs/03-provider-verify-matrix.md",
    ):
        path = _REPO / rel
        assert path.is_file(), rel
        text = path.read_text(encoding="utf-8")
        assert "mock" in text.lower()
        assert "REQ-58" in text or "AC-10" in text


def test_unit_ports_defaults_and_unknown_refuse() -> None:
    reg = registry_from_settings(_settings())
    assert reg.resolve_text().provider_id is ProviderId.MOCK
    assert reg.resolve_image().provider_id is ProviderId.MOCK
    with pytest.raises(ProviderConfigError) as ei:
        registry_from_settings(
            _settings(AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="anthropic")
        ).resolve_text()
    assert ei.value.failure_class is ProviderFailureClass.UNKNOWN_PROVIDER


def test_readyz_matrix_ac_10_08_and_09() -> None:
    ready = evaluate_readiness(
        _settings(
            OPENAI_API_KEY="",
            AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock",
            AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
            AIBRIDGE_ALLOW_MOCK_PROVIDERS=True,
        )
    )
    assert ready.ready is True

    refuse = evaluate_readiness(
        _settings(
            AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock",
            AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
            AIBRIDGE_ALLOW_MOCK_PROVIDERS=False,
        )
    )
    assert refuse.ready is False
    assert refuse.reason == "worker_mock_not_allowed"


def test_worker_accept_smoke_mock_no_live_http(monkeypatch: pytest.MonkeyPatch) -> None:
    def _forbid_httpx(*_a: object, **_k: object) -> None:
        raise AssertionError("live vendor HTTP must not be used on mock+mock accept")

    monkeypatch.setattr(httpx, "Client", _forbid_httpx)
    monkeypatch.setattr(httpx, "AsyncClient", _forbid_httpx)
    monkeypatch.setattr(
        OpenAITextBriefProvider,
        "generate_brief",
        lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("openai text")),
    )
    monkeypatch.setattr(
        OpenAIImagePosterProvider,
        "generate_poster_bytes",
        lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("openai image")),
    )

    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-55",
            "generation_version": "v1",
            "corpus": dict(_GOLDEN),
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "accepted"
    assert data["pipeline"] == "bind_ready"
    assert str(data["poster_url"]).startswith("https://")


def test_residual_live_openai_success_unknown() -> None:
    assert RESIDUAL_LIVE_OPENAI_SUCCESS_UNKNOWN is True
