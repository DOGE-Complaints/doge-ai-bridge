"""STORY-AIBRIDGE-52 — mock providers through accept pipe (AC-10-03 / AC-10-06)."""

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
    MockImagePosterProvider,
    MockTextBriefProvider,
    OpenAIImagePosterProvider,
    OpenAITextBriefProvider,
)
from aibridge.providers.ids import ProviderId
from aibridge.sense_brief.pipeline import generate_sense_brief
from aibridge.worker_accept import WORKER_ACCEPT_PATH

WORKER_TOKEN = "worker-s2s-cccccccccccccccccccccccccccccccc"
CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TEXT_BRIEF_MODEL = "gpt-test-brief"
IMAGE_POSTER_MODEL = "img-test-poster"
STORAGE_CREDENTIAL = "aibridge-storage-cred-test"

_GOLDEN = json.loads(
    (Path(__file__).parent / "fixtures" / "sense_brief_golden_l2.json").read_text(
        encoding="utf-8"
    )
)


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
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))


def _accept_body(**extra: object) -> dict:
    body: dict = {
        "issue_id": "issue-52",
        "generation_version": "v1",
        "corpus": dict(_GOLDEN),
    }
    body.update(extra)
    return body


def test_t03_mock_adapters_delegate_to_present_pipelines() -> None:
    text = MockTextBriefProvider()
    assert text.provider_id is ProviderId.MOCK
    brief = text.generate_brief(_GOLDEN, text_brief_model=TEXT_BRIEF_MODEL)
    direct = generate_sense_brief(_GOLDEN, text_brief_model=TEXT_BRIEF_MODEL)
    assert brief.model_dump() == direct.model_dump()
    image = MockImagePosterProvider()
    assert image.provider_id is ProviderId.MOCK
    png = image.generate_poster_bytes(brief, image_poster_model=IMAGE_POSTER_MODEL)
    assert isinstance(png, (bytes, bytearray))
    assert png[:8] == b"\x89PNG\r\n\x1a\n"


def test_ac_10_03_mock_mock_accept_bind_without_live_vendor_http(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbid_httpx(*_a: object, **_k: object) -> None:
        raise AssertionError("live vendor HTTP must not be used on mock+mock accept")

    monkeypatch.setattr(httpx, "Client", _forbid_httpx)
    monkeypatch.setattr(httpx, "AsyncClient", _forbid_httpx)

    def _openai_text_must_not_run(*_a: object, **_k: object) -> None:
        raise AssertionError("OpenAI text provider must not run on mock+mock")

    def _openai_image_must_not_run(*_a: object, **_k: object) -> None:
        raise AssertionError("OpenAI image provider must not run on mock+mock")

    monkeypatch.setattr(OpenAITextBriefProvider, "generate_brief", _openai_text_must_not_run)
    monkeypatch.setattr(
        OpenAIImagePosterProvider, "generate_poster_bytes", _openai_image_must_not_run
    )

    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "accepted"
    assert data["pipeline"] == "bind_ready"
    assert data["bind_outcome"] == "success"
    assert data["brief"]["title"]
    assert str(data["poster_url"]).startswith("https://")


def test_ac_10_06_l2_valid_and_https_bindable_poster() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    brief = data["brief"]
    for key in (
        "title",
        "summary",
        "problem",
        "context",
        "severity",
        "audience",
        "desired_outcome",
        "evidence_refs",
    ):
        assert key in brief
    assert isinstance(brief["summary"], dict)
    assert brief["summary"].get("en")
    url = data["poster_url"]
    assert url.startswith("https://")
    assert "issue-52" in url
    assert "v1" in url


def test_accept_uses_resolved_mock_ports(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, object] = {}

    real_text = MockTextBriefProvider.generate_brief
    real_image = MockImagePosterProvider.generate_poster_bytes

    def _text(self: MockTextBriefProvider, corpus: dict, *, text_brief_model: str):
        seen["text"] = self.provider_id
        return real_text(self, corpus, text_brief_model=text_brief_model)

    def _image(self: MockImagePosterProvider, brief: object, *, image_poster_model: str):
        seen["image"] = self.provider_id
        return real_image(self, brief, image_poster_model=image_poster_model)

    monkeypatch.setattr(MockTextBriefProvider, "generate_brief", _text)
    monkeypatch.setattr(MockImagePosterProvider, "generate_poster_bytes", _image)

    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(generation_version="v-ports"),
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    assert seen.get("text") is ProviderId.MOCK
    assert seen.get("image") is ProviderId.MOCK


def test_t07_accept_path_and_channel_prefix_unchanged() -> None:
    assert WORKER_ACCEPT_PATH == "/v1/worker/sense-brief/accept"
    assert not WORKER_ACCEPT_PATH.startswith("/v1/channel/")
    client = _client(_settings())
    # Channel bearer still rejected on worker accept (auth surface unchanged).
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {CHANNEL_TOKEN}"},
    )
    assert r.status_code == 401
    # Channel turns route still exists and is separate.
    r2 = client.post(
        "/v1/channel/turns",
        json={"type": "message", "text": "hi"},
        headers={"Authorization": f"Bearer {CHANNEL_TOKEN}"},
    )
    assert r2.status_code != 404


def test_openai_text_provider_not_implemented_is_honest_501() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
            AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="mock",
        )
    )
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(generation_version="v-oai"),
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 501
    assert r.json()["error"]["code"] == "brief_generation_failed"
