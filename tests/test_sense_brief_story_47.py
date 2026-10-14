"""STORY-AIBRIDGE-47 — L2 brief, dedicated prompts, text-brief slot, no-invent."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.audit import get_audit_buffer, reset_audit_buffer
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.sense_brief.errors import BriefFailure, BriefFailureClass
from aibridge.sense_brief.model import SenseBrief
from aibridge.sense_brief.pipeline import generate_sense_brief, refuse_invented_civic_facts
from aibridge.sense_brief.prompts import (
    assert_not_interview_ssot,
    load_system_instructions_en,
    package_resource_exists,
)
from aibridge.worker_accept import WORKER_ACCEPT_PATH

WORKER_TOKEN = "worker-s2s-cccccccccccccccccccccccccccccccc"
CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
TEXT_BRIEF_MODEL = "gpt-test-brief"
IMAGE_POSTER_MODEL = "img-test-poster"
STORAGE_CREDENTIAL = "aibridge-storage-cred-test"

_FIXTURES = Path(__file__).parent / "fixtures"
_GOLDEN = json.loads((_FIXTURES / "sense_brief_golden_l2.json").read_text(encoding="utf-8"))
_INSUFFICIENT = json.loads(
    (_FIXTURES / "sense_brief_insufficient.json").read_text(encoding="utf-8")
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


def _client(settings: Settings) -> TestClient:
    return TestClient(
        create_app(settings=settings, dedupe_store=EventDedupeStore())
    )


def test_t01_golden_l2_model_satisfies_ac() -> None:
    brief = generate_sense_brief(_GOLDEN, text_brief_model=TEXT_BRIEF_MODEL)
    assert isinstance(brief, SenseBrief)
    assert brief.satisfies_l2()
    assert len(brief.title) <= 80
    assert brief.summary.et and brief.summary.ru and brief.summary.en


def test_t02_dedicated_prompts_not_interview_ssot() -> None:
    assert package_resource_exists()
    text = load_system_instructions_en()
    assert "English" in text or "EN" in text or "Do not invent" in text
    assert_not_interview_ssot(text)
    assert "InterviewEngine" not in text
    assert "dogestonia_instructions" not in text


def test_t03_text_brief_slot_fail_closed_accept() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
            AIBRIDGE_WORKER_TEXT_BRIEF_MODEL="",
        )
    )
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-1",
            "generation_version": "v1",
            "corpus": _GOLDEN,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "worker_text_brief_missing"


def test_t03_text_brief_slot_fail_closed_readyz() -> None:
    client = _client(
        _settings(
            AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=True,
            AIBRIDGE_WORKER_TEXT_BRIEF_MODEL="",
        )
    )
    r = client.get("/readyz")
    assert r.status_code == 503
    assert r.json()["reason"] == "worker_text_brief_missing"


def test_t04_corpus_insufficient_no_fake_brief() -> None:
    try:
        generate_sense_brief(_INSUFFICIENT, text_brief_model=TEXT_BRIEF_MODEL)
        raise AssertionError("expected BriefFailure")
    except BriefFailure as exc:
        assert exc.failure_class == BriefFailureClass.CORPUS_INSUFFICIENT


def test_t04_refuse_invented_civic_facts() -> None:
    proposed = {"agency": "Invented Agency LLC", "address": "Nowhere 1"}
    try:
        refuse_invented_civic_facts(_INSUFFICIENT, proposed)
        raise AssertionError("expected invent refusal")
    except BriefFailure as exc:
        assert exc.failure_class == BriefFailureClass.BRIEF_GENERATION_FAILED


def test_t04_accept_returns_brief_without_interview_engine() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-47",
            "generation_version": "v1",
            "corpus": _GOLDEN,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["pipeline"] in {"brief_ready", "poster_ready"}
    assert data["brief"]["summary"]["en"]
    assert len(data["brief"]["title"]) <= 80
    if data["pipeline"] == "poster_ready":
        assert str(data.get("poster_url", "")).startswith("https://")


def test_t05_accept_surfaces_corpus_insufficient_class() -> None:
    client = _client(_settings())
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-insuf",
            "generation_version": "v1",
            "corpus": _INSUFFICIENT,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "corpus_insufficient"


def test_t06_pii_safe_logging_no_corpus_body() -> None:
    reset_audit_buffer()
    client = _client(_settings())
    secret_phrase = "CITIZEN_SECRET_BODY_SHOULD_NOT_LOG"
    corpus = dict(_GOLDEN)
    corpus["problem"] = secret_phrase
    r = client.post(
        WORKER_ACCEPT_PATH,
        json={
            "issue_id": "issue-pii",
            "generation_version": "v9",
            "corpus": corpus,
        },
        headers={"Authorization": f"Bearer {WORKER_TOKEN}"},
    )
    assert r.status_code == 200
    dumped = get_audit_buffer().dump_text()
    assert secret_phrase not in dumped
    assert "issue-pii" in dumped or "sense_brief" in dumped
