"""STORY-AIBRIDGE-24 — VAL-* JSON/schema boundary contract tests."""

from __future__ import annotations

import base64
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.interview import default_recording_engine

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

CHANNEL = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
STORY = "STORY-AIBRIDGE-24-qa-json-schema-boundary"
VAL_IDS = {f"VAL-{i:03d}" for i in range(1, 19)}


def _base_settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL,
        DOGESTONIA_API_BEARER_TOKEN=GATEWAY,
        DATABASE_URL="memory",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def _client(settings: Settings | None = None) -> TestClient:
    cfg = settings or _base_settings()
    app = create_app(
        settings=cfg,
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    return TestClient(app)


def _auth_header(auth_ref: str | None) -> dict[str, str]:
    if auth_ref in (None, "none"):
        return {}
    if auth_ref == "channel":
        return {"Authorization": f"Bearer {CHANNEL}"}
    raise AssertionError(f"unknown auth_ref: {auth_ref!r}")


def _request(client: TestClient, payload: dict[str, Any]):
    method = payload["method"].upper()
    path = payload["path"]
    headers = {**_auth_header(payload.get("auth_ref")), **(payload.get("headers") or {})}
    send_mode = payload.get("send_mode", "json")

    if method != "POST":
        raise AssertionError(f"unsupported method {method}")

    if send_mode == "json":
        return client.post(path, json=payload.get("body"), headers=headers or None)

    if send_mode == "raw":
        content = payload["raw_body"]
        if isinstance(content, str):
            content = content.encode("utf-8")
        # Starlette TestClient sets Content-Type for json=; for raw we pass content=
        return client.post(path, content=content, headers=headers or None)

    if send_mode == "raw_b64":
        content = base64.b64decode(payload["raw_body_b64"])
        return client.post(path, content=content, headers=headers or None)

    raise AssertionError(f"unsupported send_mode {send_mode!r}")


def test_traceability_story_covers_all_val_ids() -> None:
    names = [
        ("channel", "turns-valid-private"),
        ("channel", "val-valid-actions"),
        ("channel", "val-malformed-json"),
        ("channel", "val-invalid-utf8"),
        ("channel", "val-unknown-top-level"),
        ("channel", "val-unknown-nested"),
        ("channel", "val-missing-required"),
        ("channel", "val-channel-not-telegram"),
        ("channel", "val-empty-event-id"),
        ("channel", "val-numeric-telegram-id"),
        ("channel", "val-non-decimal-id"),
        ("channel", "val-negative-chat-id"),
        ("channel", "val-empty-message-text"),
        ("channel", "val-whitespace-message"),
        ("channel", "val-action-token-len-65"),
        ("channel", "val-payload-too-large"),
        ("channel", "val-invalid-content-length"),
        ("channel", "val-negative-content-length"),
        ("channel", "val-missing-content-type"),
    ]
    seen: set[str] = set()
    for cluster, name in names:
        env = load_fixture(cluster, name)
        assert STORY in env["story_keys"] or "VAL-001" in env["matrix_ids"]
        seen.update(i for i in env["matrix_ids"] if i.startswith("VAL-"))
    assert VAL_IDS == seen


@pytest.mark.parametrize(
    "name,matrix_id",
    [
        ("turns-valid-private", "VAL-001"),
        ("val-valid-actions", "VAL-002"),
        ("val-malformed-json", "VAL-003"),
        ("val-invalid-utf8", "VAL-004"),
        ("val-unknown-top-level", "VAL-005"),
        ("val-unknown-nested", "VAL-006"),
        ("val-missing-required", "VAL-007"),
        ("val-channel-not-telegram", "VAL-008"),
        ("val-empty-event-id", "VAL-009"),
        ("val-numeric-telegram-id", "VAL-010"),
        ("val-non-decimal-id", "VAL-011"),
        ("val-negative-chat-id", "VAL-012"),
        ("val-empty-message-text", "VAL-013"),
        ("val-action-token-len-65", "VAL-015"),
        ("val-payload-too-large", "VAL-016"),
        ("val-invalid-content-length", "VAL-017"),
        ("val-negative-content-length", "VAL-017"),
    ],
)
def test_val_matrix_must_rows(name: str, matrix_id: str) -> None:
    env = load_fixture("channel", name)
    assert matrix_id in env["matrix_ids"]
    payload = dict(env["payload"])
    # Seed VAL-001 envelope has no auth_ref/expect — harness pins channel Bearer + 200.
    if name == "turns-valid-private":
        payload.setdefault("auth_ref", "channel")
        payload.setdefault("method", "POST")
        payload.setdefault("path", "/v1/channel/turns")
        payload.setdefault("expect", {"http_status": 200})

    overrides = payload.get("settings_overrides") or {}
    client = _client(_base_settings(**overrides))
    response = _request(client, payload)
    expect = payload["expect"]

    if "http_status" in expect:
        assert response.status_code == expect["http_status"]
    if "http_status_in" in expect:
        assert response.status_code in expect["http_status_in"]
    if "error_code" in expect:
        body = response.json()
        assert body["error"]["code"] == expect["error_code"]
    if expect.get("no_openai_calls"):
        engine = client.app.state.interview_engine
        assert getattr(engine.client, "calls", []) == []
    if name == "val-payload-too-large":
        dedupe = client.app.state.dedupe_store
        assert dedupe.side_effect_count("telegram", "848301552") == 0


@pytest.mark.parametrize(
    "name,matrix_id",
    [
        ("val-whitespace-message", "VAL-014"),
        ("val-missing-content-type", "VAL-018"),
    ],
)
def test_val_characterization_capture_first(name: str, matrix_id: str) -> None:
    """Characterization — record status; do not invent product trim/Content-Type policy."""
    env = load_fixture("channel", name)
    assert matrix_id in env["matrix_ids"]
    assert "characterization" in env["notes"].lower() or env["payload"].get("characterization")
    payload = env["payload"]
    client = _client()
    response = _request(client, payload)
    # Capture-first: explicit expected status only (no vacuous 100–599 band — QUAL-001 / STORY-40).
    assert isinstance(response.status_code, int)
    # Documented current product (2026-09-17): whitespace passes min_length; missing CT accepted.
    if matrix_id == "VAL-014":
        assert response.status_code == 200
    if matrix_id == "VAL-018":
        assert response.status_code == 200


def test_seed_turns_valid_private_hash_eq_package() -> None:
    import hashlib

    original = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "tasks"
        / "backlog-stories"
        / "qa-inbound-outbound-data-flow"
        / "fixtures"
        / "turns-valid-private.json"
    )
    copy = _TESTS_ROOT / "fixtures" / "channel" / "turns-valid-private.json"
    assert original.is_file() and copy.is_file()
    assert hashlib.sha256(original.read_bytes()).digest() == hashlib.sha256(copy.read_bytes()).digest()
