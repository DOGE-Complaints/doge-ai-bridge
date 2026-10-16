"""STORY-AIBRIDGE-46 — worker accept entry, S2S, idempotency (brief corpus for 47 hook)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
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
    base = {
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
        "AIBRIDGE_ALLOW_MOCK_PROVIDERS": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings) -> TestClient:
    return TestClient(
        create_app(settings=settings, dedupe_store=EventDedupeStore())
    )


def _accept_body(**extra: object) -> dict:
    body: dict = {
        "issue_id": "issue-1",
        "generation_version": "v1",
        "corpus": dict(_GOLDEN),
    }
    body.update(extra)
    return body


def test_accept_path_is_not_channel_prefix() -> None:
    assert not WORKER_ACCEPT_PATH.startswith("/v1/channel/")
    assert WORKER_ACCEPT_PATH.startswith("/v1/worker/")


def test_channel_bearer_rejected_on_worker_accept() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {CHANNEL_TOKEN}"},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "unauthorized"


def test_missing_auth_rejected() -> None:
    client = _client(_settings())
    r = client.post(WORKER_ACCEPT_PATH, json=_accept_body())
    assert r.status_code == 401


def test_valid_worker_s2s_admits_accept() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "accepted"
    assert data["issue_id"] == "issue-1"
    assert data["generation_version"] == "v1"
    assert data["idempotent"] is False
    assert data["pipeline"] in {"brief_ready", "poster_ready", "bind_ready"}
    assert data["brief"]["title"]


def test_same_version_idempotent_no_second_create() -> None:
    client = _client(_settings())
    headers = {"Authorization": f"Bearer {WORKER_TOKEN}"}
    r1 = client.post(WORKER_ACCEPT_PATH, json=_accept_body(), headers=headers)
    r2 = client.post(WORKER_ACCEPT_PATH, json=_accept_body(), headers=headers)
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["idempotent"] is False
    assert r2.json()["idempotent"] is True
    assert r2.json()["status"] == r1.json()["status"]


def test_new_generation_version_allows_new_work() -> None:
    client = _client(_settings())
    headers = {"Authorization": f"Bearer {WORKER_TOKEN}"}
    r1 = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(generation_version="v1"),
        headers=headers,
    )
    r2 = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(generation_version="v2"),
        headers=headers,
    )
    assert r1.json()["idempotent"] is False
    assert r2.json()["idempotent"] is False
    assert r2.json()["generation_version"] == "v2"


def test_enabled_missing_s2s_fail_closed_accept() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
            AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN="",
        )
    )
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "worker_s2s_missing"


def test_enabled_missing_s2s_fail_closed_readyz() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
            AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN="",
        )
    )
    r = client.get("/readyz")
    assert r.status_code == 503
    assert r.json()["reason"] == "worker_s2s_missing"


def test_worker_disabled_returns_503() -> None:
    client = _client(
        _settings(AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=False)
    )
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "worker_disabled"


def test_gateway_token_not_worker_s2s() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {GATEWAY_TOKEN}"},
    )
    assert r.status_code == 401


def test_channel_eq_worker_s2s_still_rejected() -> None:
    """Misconfig: channel Bearer == worker S2S → still 401 (channel set wins)."""
    shared = "shared-misconfig-token-dddddddddddddddddddddddd"
    client = _client(
        _settings(
            AIBRIDGE_CHANNEL_BEARER_TOKEN=shared,
            AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN=shared,
        )
    )
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=_accept_body(),
        headers={"Authorization": f"Bearer {shared}"},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "unauthorized"
