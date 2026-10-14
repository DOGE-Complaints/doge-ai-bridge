"""STORY-AIBRIDGE-48 — image-poster slot, brief→bytes, storage HTTPS, mock port."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.poster.errors import PosterFailure, PosterFailureClass
from aibridge.poster.image import generate_poster_bytes
from aibridge.poster.pipeline import upload_poster_https
from aibridge.poster.port import PosterUploadPort
from aibridge.poster.prompts import (
    assert_not_interview_ssot,
    load_system_instructions_en,
    package_resource_exists,
)
from aibridge.poster.storage import MockHttpsUploader, build_default_uploader
from aibridge.sense_brief.model import SenseBrief, SenseBriefSummary
from aibridge.sense_brief.pipeline import generate_sense_brief
from aibridge.worker_accept import WORKER_ACCEPT_PATH

WORKER_TOKEN = "worker-s2s-cccccccccccccccccccccccccccccccc"
CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TEXT_BRIEF_MODEL = "gpt-test-brief"
IMAGE_POSTER_MODEL = "img-test-poster"
STORAGE_CREDENTIAL = "aibridge-storage-cred-test"

_FIXTURES = Path(__file__).parent / "fixtures"
_GOLDEN = json.loads((_FIXTURES / "sense_brief_golden_l2.json").read_text(encoding="utf-8"))


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
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings) -> TestClient:
    return TestClient(
        create_app(settings=settings, dedupe_store=EventDedupeStore())
    )


def _brief() -> SenseBrief:
    return generate_sense_brief(_GOLDEN, text_brief_model=TEXT_BRIEF_MODEL)


def test_t01_image_poster_slot_fail_closed_accept() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
            AIBRIDGE_WORKER_IMAGE_POSTER_MODEL="",
        )
    )
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-48-img",
            "generation_version": "v1",
            "corpus": _GOLDEN,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "worker_image_poster_missing"


def test_t01_image_poster_slot_fail_closed_readyz() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
            AIBRIDGE_WORKER_IMAGE_POSTER_MODEL="",
        )
    )
    r = client.get("/readyz")
    assert r.status_code == 503
    assert r.json()["reason"] == "worker_image_poster_missing"


def test_t02_poster_bytes_from_brief_not_interview() -> None:
    assert package_resource_exists()
    text = load_system_instructions_en()
    assert_not_interview_ssot(text)
    assert "InterviewEngine" not in text
    brief = _brief()
    data = generate_poster_bytes(brief, image_poster_model=IMAGE_POSTER_MODEL)
    assert data.startswith(b"\x89PNG")
    assert brief.title.encode("utf-8") in data


def test_t02_image_slot_unset_raises_class() -> None:
    brief = SenseBrief(
        title="T",
        summary=SenseBriefSummary(et="e", ru="r", en="n"),
        problem="p",
        context="c",
        severity="s",
        audience="a",
        desired_outcome="d",
    )
    try:
        generate_poster_bytes(brief, image_poster_model="")
        raise AssertionError("expected PosterFailure")
    except PosterFailure as exc:
        assert exc.failure_class == PosterFailureClass.IMAGE_GENERATION_FAILED


def test_t03_storage_creds_fail_closed_readyz() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
            AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL="",
        )
    )
    r = client.get("/readyz")
    assert r.status_code == 503
    assert r.json()["reason"] == "worker_storage_creds_missing"


def test_t03_missing_creds_upload_fail_class() -> None:
    brief = _brief()
    try:
        upload_poster_https(
            brief,
            image_poster_model=IMAGE_POSTER_MODEL,
            storage_credential="",
            object_key="x/y.png",
        )
        raise AssertionError("expected PosterFailure")
    except PosterFailure as exc:
        assert exc.failure_class == PosterFailureClass.STORAGE_UPLOAD_FAILED


def test_t04_mock_upload_yields_https_url() -> None:
    brief = _brief()
    url = upload_poster_https(
        brief,
        image_poster_model=IMAGE_POSTER_MODEL,
        storage_credential=STORAGE_CREDENTIAL,
        object_key="issue-1/v1.png",
    )
    assert url.startswith("https://")
    assert "issue-1" in url


def test_t05_mockable_upload_port_injectable() -> None:
    class CapturingUploader:
        def __init__(self) -> None:
            self.seen: bytes | None = None

        def upload(
            self, data: bytes, *, content_type: str, object_key: str
        ) -> str:
            self.seen = data
            _ = content_type
            return f"https://harness.example.test/{object_key}"

    brief = _brief()
    cap = CapturingUploader()
    assert isinstance(cap, PosterUploadPort)
    url = upload_poster_https(
        brief,
        image_poster_model=IMAGE_POSTER_MODEL,
        storage_credential=STORAGE_CREDENTIAL,
        object_key="inj/v1.png",
        uploader=cap,
    )
    assert url == "https://harness.example.test/inj/v1.png"
    assert cap.seen is not None and cap.seen.startswith(b"\x89PNG")


def test_t06_accept_returns_poster_https_url() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-48",
            "generation_version": "v1",
            "corpus": _GOLDEN,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["pipeline"] in {"poster_ready", "bind_ready"}
    assert str(data["poster_url"]).startswith("https://")
    assert data["brief"]["title"]


def test_t06_default_uploader_uses_aibridge_creds_only() -> None:
    gated = build_default_uploader(STORAGE_CREDENTIAL)
    url = gated.upload(b"\x89PNG\r\n\x1a\nfake", content_type="image/png", object_key="k")
    assert url.startswith("https://")
    mock = MockHttpsUploader()
    assert mock.upload(b"abc", content_type="image/png", object_key="z").startswith(
        "https://"
    )
