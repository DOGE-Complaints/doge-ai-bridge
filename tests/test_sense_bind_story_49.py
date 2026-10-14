"""STORY-AIBRIDGE-49 — gateway bind-in, fail classes, version distinguishability."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.audit import get_audit_buffer, reset_audit_buffer
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import RawHttpResponse, RecordingGatewayTransport
from aibridge.sense_bind.client import BIND_PATH, SenseBriefBindClient, client_from_settings
from aibridge.sense_bind.errors import BindFailure, BindFailureClass
from aibridge.sense_bind.payload import (
    assert_no_fake_brief_on_fail,
    build_fail_bind_payload,
    build_success_bind_payload,
)
from aibridge.sense_bind.version import regenerate_assets_distinguishable
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
_INSUFFICIENT = json.loads(
    (Path(__file__).parent / "fixtures" / "sense_brief_insufficient.json").read_text(
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
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _client(settings: Settings, transport: RecordingGatewayTransport | None = None) -> TestClient:
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    if transport is not None:
        app.state.sense_bind_transport = transport
    return TestClient(app)


def _brief_dict() -> dict:
    return {
        "title": "Broken streetlight on Main",
        "summary": {"et": "e", "ru": "r", "en": "Broken streetlight"},
        "problem": "p",
        "context": "c",
        "severity": "s",
        "audience": "a",
        "desired_outcome": "d",
        "evidence_refs": [],
    }


def test_t01_bind_uses_gateway_service_auth_not_channel_or_worker() -> None:
    transport = RecordingGatewayTransport(
        scripted=[RawHttpResponse(status_code=200, body=b'{"ok":true}')]
    )
    client = SenseBriefBindClient(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY_TOKEN,
        channel_bearer=CHANNEL_TOKEN,
        worker_s2s_token=WORKER_TOKEN,
        dry_run=False,
        transport=transport,
    )
    result = client.bind_success(
        issue_id="i1",
        generation_version="v1",
        brief=_brief_dict(),
        poster_url="https://aibridge-poster.test/objects/i1/v1.png",
    )
    assert result.ok
    assert len(transport.calls) == 1
    call = transport.calls[0]
    assert call["url"].endswith(BIND_PATH)
    assert call["headers"]["Authorization"] == f"Bearer {GATEWAY_TOKEN}"
    assert CHANNEL_TOKEN not in call["headers"]["Authorization"]
    assert WORKER_TOKEN not in call["headers"]["Authorization"]


def test_t01_refuse_when_gateway_equals_channel() -> None:
    client = SenseBriefBindClient(
        origin="https://gateway.example.invalid",
        gateway_bearer=CHANNEL_TOKEN,
        channel_bearer=CHANNEL_TOKEN,
        dry_run=False,
        transport=RecordingGatewayTransport(
            scripted=[RawHttpResponse(200, b"{}")]
        ),
    )
    try:
        client.bind_success(
            issue_id="i1",
            generation_version="v1",
            brief=_brief_dict(),
            poster_url="https://aibridge-poster.test/x.png",
        )
        raise AssertionError("expected BindFailure")
    except BindFailure as exc:
        assert exc.failure_class == BindFailureClass.INTERNAL_ERROR


def test_t02_success_payload_has_apply_url_version() -> None:
    payload = build_success_bind_payload(
        issue_id="issue-1",
        generation_version="v2",
        brief=_brief_dict(),
        poster_url="https://aibridge-poster.test/objects/issue-1/v2.png",
    )
    assert payload["outcome"] == "success"
    assert payload["generation_version"] == "v2"
    assert payload["poster_url"].startswith("https://")
    assert payload["apply"]["title"]
    assert payload["apply"]["summary"]["en"]


def test_t03_fail_payload_no_fake_brief() -> None:
    payload = build_fail_bind_payload(
        issue_id="issue-1",
        generation_version="v1",
        reason_class=BindFailureClass.IMAGE_GENERATION_FAILED,
    )
    assert payload["outcome"] == "failure"
    assert payload["reason_class"] == "image_generation_failed"
    assert "brief" not in payload
    assert "apply" not in payload
    assert_no_fake_brief_on_fail(payload)


def test_t04_regenerate_versions_distinguishable() -> None:
    assert regenerate_assets_distinguishable(
        version_a="v1",
        version_b="v2",
        url_a="https://aibridge-poster.test/objects/i/v1.png",
        url_b="https://aibridge-poster.test/objects/i/v2.png",
    )
    assert not regenerate_assets_distinguishable(
        version_a="v1",
        version_b="v1",
        url_a="https://aibridge-poster.test/a.png",
        url_b="https://aibridge-poster.test/b.png",
    )


def test_t05_pii_safe_bind_logging() -> None:
    reset_audit_buffer()
    transport = RecordingGatewayTransport(
        scripted=[RawHttpResponse(200, b'{"ok":true}')]
    )
    client = SenseBriefBindClient(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY_TOKEN,
        dry_run=False,
        transport=transport,
    )
    secret = "CITIZEN_SECRET_SHOULD_NOT_APPEAR"
    brief = _brief_dict()
    brief["problem"] = secret
    client.bind_success(
        issue_id="issue-pii",
        generation_version="v9",
        brief=brief,
        poster_url="https://aibridge-poster.test/objects/issue-pii/v9.png",
    )
    dumped = get_audit_buffer().dump_text()
    assert secret not in dumped
    assert "issue-pii" in dumped
    assert GATEWAY_TOKEN not in dumped


def test_t06_mock_gateway_reject_maps_bind_rejected() -> None:
    transport = RecordingGatewayTransport(
        scripted=[RawHttpResponse(status_code=403, body=b'{"err":"no"}')]
    )
    client = SenseBriefBindClient(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY_TOKEN,
        dry_run=False,
        transport=transport,
    )
    try:
        client.bind_success(
            issue_id="i1",
            generation_version="v1",
            brief=_brief_dict(),
            poster_url="https://aibridge-poster.test/x.png",
        )
        raise AssertionError("expected BindFailure")
    except BindFailure as exc:
        assert exc.failure_class == BindFailureClass.BIND_REJECTED


def test_t06_accept_bind_ready_dry_run() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-49",
            "generation_version": "v1",
            "corpus": _GOLDEN,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["pipeline"] == "bind_ready"
    assert data["bind_outcome"] == "success"
    assert str(data["poster_url"]).startswith("https://")


def test_t06_accept_fail_bind_on_corpus_insufficient() -> None:
    transport = RecordingGatewayTransport(
        scripted=[RawHttpResponse(200, b'{"ok":true}')]
    )
    # dry_run True → fail bind does not need scripted; use False to assert call.
    settings = _settings(AIBRIDGE_DRY_RUN=False)
    client = _client(settings, transport=transport)
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-insuf-49",
            "generation_version": "v1",
            "corpus": _INSUFFICIENT,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "corpus_insufficient"
    assert len(transport.calls) == 1
    body = transport.calls[0]["json_body"]
    assert body["outcome"] == "failure"
    assert body["reason_class"] == "corpus_insufficient"
    assert "brief" not in body
    assert "apply" not in body


def test_t06_two_versions_distinguishable_on_accept() -> None:
    client = _client(_settings())
    r1 = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-regen",
            "generation_version": "v1",
            "corpus": _GOLDEN,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    r2 = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-regen",
            "generation_version": "v2",
            "corpus": _GOLDEN,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r1.status_code == 200 and r2.status_code == 200
    d1, d2 = r1.json(), r2.json()
    assert regenerate_assets_distinguishable(
        version_a=d1["generation_version"],
        version_b=d2["generation_version"],
        url_a=d1["poster_url"],
        url_b=d2["poster_url"],
    )


def test_client_from_settings_wires_tokens() -> None:
    c = client_from_settings(_settings(), transport=RecordingGatewayTransport())
    assert c.gateway_bearer == GATEWAY_TOKEN
    assert c.channel_bearer == CHANNEL_TOKEN
    assert c.worker_s2s_token == WORKER_TOKEN
