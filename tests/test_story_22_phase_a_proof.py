"""STORY-AIBRIDGE-22 — Content Phase A proof (ADR-4 / REQ-05 §4.5)."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.content import load_manifest
from aibridge.dedupe import EventDedupeStore
from aibridge.interview import default_recording_engine
from aibridge.registry import MemoryBundleRegistry

ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = ROOT / "src" / "instructions"
MANIFEST = INSTRUCTIONS / "instructions.manifest.json"
MANIFEST_NAME = "instructions.manifest.json"
WIRE_OAS = ROOT / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
PAYLOAD = INSTRUCTIONS / "schema-packs.uus_veerenni_civic.v3.payload.schema.json"


def _full_dump_settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INSTRUCTIONS_DIR=str(INSTRUCTIONS),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(MANIFEST),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="phase-a-proof",
        DOGESTONIA_OPENAPI_PATH=str(WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(PAYLOAD),
        DATABASE_URL="memory",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    # Isolate ambient doge-ai-bridge/.env so intake/content pins come only from kwargs.
    return Settings(_env_file=None, **base)


def _dir_children() -> set[str]:
    return {p.name for p in INSTRUCTIONS.iterdir() if p.is_file()} - {MANIFEST_NAME}


# --- t01: engine wired + prefix -------------------------------------------------


def test_full_dump_create_app_wires_nonempty_prefix_instructions() -> None:
    settings = _full_dump_settings()
    assert settings.content_configured()
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        interview_engine=default_recording_engine(),
    )
    engine = app.state.interview_engine
    dep = app.state.deployment_bundle
    assert dep is not None and dep.ready
    assert engine.prompt_channel == "prefix"
    assert engine.instructions.strip()
    assert "root.md" in dict(dep.loaded.file_hashes)  # type: ignore[union-attr]

    engine.run_turn(session_id="s22", user_text="hi")
    sent = engine.client.calls[0]
    assert "instructions" not in sent
    system = next(
        i for i in sent["input"] if isinstance(i, dict) and i.get("role") == "system"
    )
    assert str(system.get("content", "")).strip()


def test_full_dump_readyz_not_content_bundle_not_ready() -> None:
    """Proof surface for smoke: complete Phase A paths → content reason absent."""
    settings = _full_dump_settings()
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        interview_engine=default_recording_engine(),
    )
    client = TestClient(app)
    assert client.get("/healthz").status_code == 200
    response = client.get("/readyz")
    body = response.json()
    assert body.get("reason") != "content_bundle_not_ready"
    if response.status_code == 503:
        reason = str(body.get("reason") or "")
        assert not reason.startswith("content_verify_failed:")
        assert reason != "assembled_instructions_empty"


# --- t02: readyz fail-closed ----------------------------------------------------


def test_readyz_fail_closed_missing_instructions_dir() -> None:
    settings = _full_dump_settings(
        DOGESTONIA_INSTRUCTIONS_DIR=str(ROOT / "src" / "instructions-DOES-NOT-EXIST"),
    )
    assert settings.content_configured()
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        interview_engine=default_recording_engine(),
    )
    dep = app.state.deployment_bundle
    assert dep is not None
    assert dep.ready is False
    assert dep.error is not None
    assert "content_verify_failed" in dep.error or dep.error == "content_bundle_not_ready"
    # Engine must not silently hold empty assembled prompt as a ready path.
    assert app.state.interview_engine.instructions == ""

    client = TestClient(app)
    assert client.get("/healthz").status_code == 200
    response = client.get("/readyz")
    assert response.status_code == 503
    reason = response.json()["reason"]
    assert reason.startswith("content_verify_failed:") or reason == "content_bundle_not_ready"


def test_readyz_fail_closed_broken_openapi_path() -> None:
    settings = _full_dump_settings(
        DOGESTONIA_OPENAPI_PATH=str(ROOT / "docs" / "openapi" / "missing-wire.yaml"),
    )
    assert settings.content_configured()
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        interview_engine=default_recording_engine(),
    )
    dep = app.state.deployment_bundle
    assert dep is not None and dep.ready is False
    client = TestClient(app)
    response = client.get("/readyz")
    assert response.status_code == 503
    reason = response.json()["reason"]
    assert reason.startswith("content_verify_failed:") or reason == "content_bundle_not_ready"


# --- t03: manifest completeness -------------------------------------------------


def test_proof_completeness_dir_set_equals_files_set() -> None:
    files = load_manifest(MANIFEST)["files"]
    assert set(files) == _dir_children()
    assert MANIFEST_NAME not in files


def test_proof_omit_would_fail_completeness() -> None:
    files = list(load_manifest(MANIFEST)["files"])
    omitted = files[0]
    remaining = set(files) - {omitted}
    assert remaining != _dir_children()
