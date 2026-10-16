"""Sense-brief worker isolation harness — mocks for LLM/image/storage/gateway bind.

CI runs without live OpenAI / image vendor / bucket / gateway. Module name is an
implement choice for STORY-AIBRIDGE-50 (Open until created).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import RawHttpResponse, RecordingGatewayTransport
from aibridge.poster.storage import MockHttpsUploader
from aibridge.worker_accept import WORKER_ACCEPT_PATH

WORKER_TOKEN = "worker-s2s-cccccccccccccccccccccccccccccccc"
CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TEXT_BRIEF_MODEL = "gpt-test-brief"
IMAGE_POSTER_MODEL = "img-test-poster"
STORAGE_CREDENTIAL = "aibridge-storage-cred-test"

_FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
GOLDEN_CORPUS: dict[str, Any] = json.loads(
    (_FIXTURES / "sense_brief_golden_l2.json").read_text(encoding="utf-8")
)
INSUFFICIENT_CORPUS: dict[str, Any] = json.loads(
    (_FIXTURES / "sense_brief_insufficient.json").read_text(encoding="utf-8")
)


def isolation_settings(**overrides: object) -> Settings:
    """Settings for isolation suite — dry_run + fake slot models; no live secrets."""
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
        "AIBRIDGE_ALLOW_MOCK_PROVIDERS": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def isolation_client(
    settings: Settings | None = None,
    *,
    transport: RecordingGatewayTransport | None = None,
) -> TestClient:
    app = create_app(
        settings=settings or isolation_settings(),
        dedupe_store=EventDedupeStore(),
    )
    if transport is not None:
        app.state.sense_bind_transport = transport
    return TestClient(app)


def accept_body(
    *,
    issue_id: str = "issue-50",
    generation_version: str = "v1",
    corpus: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "issue_id": issue_id,
        "generation_version": generation_version,
        "corpus": dict(corpus if corpus is not None else GOLDEN_CORPUS),
    }


def worker_auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {WORKER_TOKEN}"}


def channel_auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {CHANNEL_TOKEN}"}


def mock_storage_uploader(prefix: str = "https://isolation-harness.test/objects/") -> MockHttpsUploader:
    return MockHttpsUploader(url_prefix=prefix)


def recording_gateway(
    *,
    status_code: int = 200,
    body: bytes = b'{"ok":true}',
) -> RecordingGatewayTransport:
    return RecordingGatewayTransport(
        scripted=[RawHttpResponse(status_code=status_code, body=body)]
    )


__all__ = [
    "CHANNEL_TOKEN",
    "GATEWAY_TOKEN",
    "GOLDEN_CORPUS",
    "IMAGE_POSTER_MODEL",
    "INSUFFICIENT_CORPUS",
    "STORAGE_CREDENTIAL",
    "TEXT_BRIEF_MODEL",
    "WORKER_ACCEPT_PATH",
    "WORKER_TOKEN",
    "accept_body",
    "channel_auth_headers",
    "isolation_client",
    "isolation_settings",
    "mock_storage_uploader",
    "recording_gateway",
    "worker_auth_headers",
]
