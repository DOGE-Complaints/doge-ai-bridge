"""STORY-AIBRIDGE-54 — OpenAI text live port (AC-10-04 / AC-10-10).

Live vendor SUCCESS against real OpenAI credentials/network is residual Unknown —
all SUCCESS paths here use mocked invoke/transport only.
"""

from __future__ import annotations

import json

import httpx
import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.providers import (
    ProviderId,
    resolve_image_poster_provider,
    resolve_text_brief_provider,
)
from aibridge.providers.adapters import (
    MockImagePosterProvider,
    MockTextBriefProvider,
    OpenAIImagePosterProvider,
    OpenAITextBriefProvider,
)
from aibridge.providers.openai_text_live import extract_brief_from_stories
from aibridge.responses_client import RecordingResponsesTransport
from aibridge.sense_brief.errors import BriefFailure, BriefFailureClass
from aibridge.worker_accept import WORKER_ACCEPT_PATH

WORKER_TOKEN = "worker-s2s-cccccccccccccccccccccccccccccccc"
CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TEXT_BRIEF_MODEL = "gpt-test-brief"
IMAGE_POSTER_MODEL = "img-test-poster"
STORAGE_CREDENTIAL = "aibridge-storage-cred-test"

_L2 = {
    "title": "Broken streetlight on Oak Ave",
    "summary": {
        "et": "Katkenud tänavavalgusti Oak Ave-l.",
        "ru": "Неработающий фонарь на Oak Ave.",
        "en": "Broken streetlight on Oak Ave.",
    },
    "problem": "Streetlight out for two weeks",
    "context": "Residential block reported via resident stories",
    "severity": "medium",
    "audience": "city maintenance",
    "desired_outcome": "Restore lighting within 72h",
    "evidence_refs": ["story-101", "story-102"],
}

_STORIES_CORPUS = {
    "stories": [
        {"id": "story-101", "text": "Streetlight dark on Oak Ave for two weeks."},
        {"id": "story-102", "text": "Residents want lighting restored soon."},
    ]
}


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
        "AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER": "openai",
        "AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER": "mock",
        "AIBRIDGE_ALLOW_MOCK_PROVIDERS": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings=settings, dedupe_store=EventDedupeStore()))


def _scripted_openai_payload(brief: dict | None = None) -> dict:
    body = brief if brief is not None else _L2
    return {
        "id": "resp_test_54",
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [
                    {"type": "output_text", "text": json.dumps(body, ensure_ascii=False)}
                ],
            }
        ],
        "usage": {"input_tokens": 10, "output_tokens": 20, "cached_tokens": 0},
        "aibridge_parsed": {
            "reply_text": json.dumps(body, ensure_ascii=False),
            "function_calls": [],
            "cached_input_tokens": 0,
        },
    }


def test_ac_10_04_env_flip_resolves_openai_text_mock_image() -> None:
    openai_text = resolve_text_brief_provider(_settings())
    assert isinstance(openai_text, OpenAITextBriefProvider)
    assert openai_text.provider_id is ProviderId.OPENAI
    mock_text = resolve_text_brief_provider(
        _settings(AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock")
    )
    assert isinstance(mock_text, MockTextBriefProvider)
    image = resolve_image_poster_provider(_settings())
    assert isinstance(image, MockImagePosterProvider)
    assert image.provider_id is ProviderId.MOCK


def test_ac_10_10_stories_to_l2_via_mocked_invoke() -> None:
    brief = extract_brief_from_stories(
        _STORIES_CORPUS,
        text_brief_model=TEXT_BRIEF_MODEL,
        api_key="sk-test",
        invoke=lambda _payload: _scripted_openai_payload(),
    )
    assert brief.title == _L2["title"]
    assert brief.satisfies_l2()
    assert brief.summary.en


def test_honest_corpus_insufficient_empty_stories() -> None:
    with pytest.raises(BriefFailure) as exc:
        extract_brief_from_stories(
            {"stories": []},
            text_brief_model=TEXT_BRIEF_MODEL,
            api_key="sk-test",
            invoke=lambda _p: _scripted_openai_payload(),
        )
    assert exc.value.failure_class is BriefFailureClass.CORPUS_INSUFFICIENT


def test_honest_corpus_insufficient_missing_stories() -> None:
    with pytest.raises(BriefFailure) as exc:
        extract_brief_from_stories(
            {"title": "no stories key"},
            text_brief_model=TEXT_BRIEF_MODEL,
            api_key="sk-test",
            invoke=lambda _p: _scripted_openai_payload(),
        )
    assert exc.value.failure_class is BriefFailureClass.CORPUS_INSUFFICIENT


def test_transport_failure_maps_to_brief_generation_failed() -> None:
    transport = RecordingResponsesTransport(scripted=[(500, None, "boom")])
    with pytest.raises(BriefFailure) as exc:
        extract_brief_from_stories(
            _STORIES_CORPUS,
            text_brief_model=TEXT_BRIEF_MODEL,
            api_key="sk-test",
            transport=transport,
        )
    assert exc.value.failure_class is BriefFailureClass.BRIEF_GENERATION_FAILED


def test_no_silent_openai_when_text_is_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    def _forbid(*_a: object, **_k: object) -> None:
        raise AssertionError("OpenAI text must not run when provider=mock")

    monkeypatch.setattr(OpenAITextBriefProvider, "generate_brief", _forbid)
    text = resolve_text_brief_provider(
        _settings(AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="mock")
    )
    assert isinstance(text, MockTextBriefProvider)


def test_image_stays_mock_openai_image_still_deferred() -> None:
    img = resolve_image_poster_provider(
        _settings(
            AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER="openai",
            AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER="openai",
        )
    )
    assert isinstance(img, OpenAIImagePosterProvider)
    with pytest.raises(NotImplementedError, match="deferred"):
        img.generate_poster_bytes(object(), image_poster_model=IMAGE_POSTER_MODEL)


def test_accept_openai_text_mock_image_with_mocked_invoke(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _forbid_httpx(*_a: object, **_k: object) -> None:
        raise AssertionError("live vendor HTTP must not be used — inject invoke")

    monkeypatch.setattr(httpx, "Client", _forbid_httpx)
    monkeypatch.setattr(httpx, "AsyncClient", _forbid_httpx)

    def _fake_generate(
        self: OpenAITextBriefProvider,
        corpus: dict,
        *,
        text_brief_model: str,
    ) -> object:
        return extract_brief_from_stories(
            corpus,
            text_brief_model=text_brief_model,
            api_key="sk-test",
            invoke=lambda _p: _scripted_openai_payload(),
        )

    monkeypatch.setattr(OpenAITextBriefProvider, "generate_brief", _fake_generate)

    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-54",
            "generation_version": "v1",
            "corpus": _STORIES_CORPUS,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "accepted"
    assert data["brief"]["title"] == _L2["title"]
    assert str(data["poster_url"]).startswith("https://")


def test_accept_corpus_insufficient_maps_reason_class(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _fake_generate(
        self: OpenAITextBriefProvider,
        corpus: dict,
        *,
        text_brief_model: str,
    ) -> object:
        return extract_brief_from_stories(
            corpus,
            text_brief_model=text_brief_model,
            api_key="sk-test",
            invoke=lambda _p: _scripted_openai_payload(),
        )

    monkeypatch.setattr(OpenAITextBriefProvider, "generate_brief", _fake_generate)
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-54-empty",
            "generation_version": "v1",
            "corpus": {"stories": []},
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "corpus_insufficient"


# Residual fact (P3): live OpenAI SUCCESS with real credentials/network was not
# exercised — Unknown in this environment. Mocked SUCCESS paths above are green.
RESIDUAL_LIVE_OPENAI_SUCCESS = True
