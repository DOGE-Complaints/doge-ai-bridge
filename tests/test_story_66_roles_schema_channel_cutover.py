"""STORY-AIBRIDGE-66 — roles-schema channel cutover (+ local GPT-48 consume light).

Locks: no invent instruction bodies · OOS Railway-67 · Keep dual-confirm · fixtures ≠ invent export.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.content import (
    ContentLoadError,
    classify_manifest,
    load_content_bundle,
    load_manifest,
    peek_manifest_schema,
)
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.interview import default_recording_engine
from aibridge.roles.assembly import assert_manifest_covers_v1, load_roles_manifest

_REPO = Path(__file__).resolve().parents[1]
_WORKSPACE = _REPO.parent
_DOC = _REPO / "docs" / "runtime-docs" / "13-roles-schema-channel-cutover.md"
_REQ13 = (
    _REPO
    / "docs"
    / "requirements"
    / "REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md"
)
_FIXTURES = _REPO / "tests" / "fixtures" / "content"
_ROLES_DIR = _FIXTURES / "roles-instructions"
_ROLES_MANIFEST = _FIXTURES / "roles.manifest.json"
_PHASE_A_MANIFEST = _FIXTURES / "instructions.manifest.json"
_PHASE_A_DIR = _FIXTURES / "instructions"
_OAS = _FIXTURES / "bad-tool-gen.openapi.yaml"
_PACK = _FIXTURES / "pack" / "payload.schema.json"
_EXPORT = _WORKSPACE / "GPT UI" / "instructions-roles-req15"
_EXPORT_MANIFEST = _EXPORT / "roles.manifest.json"


def _settings(**extra: str) -> Settings:
    reset_settings_cache()
    kwargs = {
        "_env_file": None,
        "AIBRIDGE_CHANNEL_BEARER_TOKEN": "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "GATEWAY_SERVICE_API_TOKEN": "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "GATEWAY_BASE_URL": "https://gateway.example.invalid",
        "SPA_BASE_URL": "https://spa.example.invalid",
        "OPENAI_API_KEY": "sk-test-not-real",
        "OPENAI_MODEL": "gpt-test",
        "AIBRIDGE_INTERVIEW_PROVIDER": "openai",
        "AIBRIDGE_DRY_RUN": "true",
    }
    kwargs.update(extra)
    return Settings(**kwargs)  # type: ignore[arg-type]


def _auth() -> dict[str, str]:
    return {
        "Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }


def _turn(event_id: str = "6601") -> dict:
    return {
        "channel": "telegram",
        "event_id": event_id,
        "principal": {"user_id": "66", "chat_id": "-166"},
        "message": {"message_id": "1", "text": "hello cutover"},
    }


def test_t01_instructions_env_roles_schema_cutover_unify() -> None:
    """INSTRUCTIONS_* roles-schema unifies into channel_wire without ROLES_*."""
    assert peek_manifest_schema(_ROLES_MANIFEST) == "roles"
    reset_confirmation_guard()
    engine = default_recording_engine()
    engine.instructions = "ADR1-legacy-mega"
    app = create_app(
        settings=_settings(
            DOGESTONIA_INSTRUCTIONS_DIR=str(_ROLES_DIR),
            DOGESTONIA_INSTRUCTIONS_MANIFEST=str(_ROLES_MANIFEST),
            # ROLES_* intentionally empty — cutover unify
            DOGESTONIA_ROLES_INSTRUCTIONS_DIR="",
            DOGESTONIA_ROLES_MANIFEST="",
        ),
        dedupe_store=EventDedupeStore(),
        interview_engine=engine,
    )
    wire = app.state.channel_wire
    assert wire.roles_instructions_dir == _ROLES_DIR
    assert wire.roles_manifest_path == _ROLES_MANIFEST
    client = TestClient(app)
    r = client.post("/v1/channel/turns", json=_turn("6601"), headers=_auth())
    assert r.status_code == 200
    ev = wire.last_evidence
    assert ev.get("assembled") is True
    assert ev.get("cutover") is True
    assert engine.instructions != "ADR1-legacy-mega"


def test_t02_content_ready_roles_schema_loader() -> None:
    data = load_manifest(_ROLES_MANIFEST)
    assert classify_manifest(data) == "roles"
    assert "files" not in data
    bundle = load_content_bundle(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        source_commit="test-commit-66",
        wire_oas_path=_OAS,
        pack_schema_path=_PACK,
    )
    assert bundle.bundle_version
    assert bundle.components.get("schema") == "roles"
    assert bundle.components.get("core") == "core.md"
    assert "interviewer" in bundle.components.get("roles", {})
    # ADR-1 prefix = core only (not Phase-A join)
    core_text = (_ROLES_DIR / "core.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    assert bundle.assembled_instructions == core_text
    names = {n for n, _ in bundle.file_hashes}
    assert "core.md" in names
    assert "interviewer.md" in names

    # Phase-A still loads (legacy/dev)
    phase = load_manifest(_PHASE_A_MANIFEST)
    assert classify_manifest(phase) == "phase_a"
    phase_bundle = load_content_bundle(
        instructions_dir=_PHASE_A_DIR,
        manifest_path=_PHASE_A_MANIFEST,
        source_commit="test-commit-66-phase-a",
        wire_oas_path=_OAS,
        pack_schema_path=_PACK,
    )
    assert phase_bundle.components.get("schema") == "phase_a"


def test_t02_dual_schema_fail_closed(tmp_path: Path) -> None:
    dual = tmp_path / "dual.json"
    dual.write_text(
        '{"bundle_version":"x","core":"core.md","roles":{"a":{"file":"a.md","version":"v1"}},'
        '"files":["a.md"]}',
        encoding="utf-8",
    )
    with pytest.raises(ContentLoadError, match="dual schema"):
        load_manifest(dual)


def test_t03_channel_wire_assemble_default_cutover() -> None:
    reset_confirmation_guard()
    engine = default_recording_engine()
    engine.instructions = "ADR1-mega-before"
    app = create_app(
        settings=_settings(
            DOGESTONIA_ROLES_INSTRUCTIONS_DIR=str(_ROLES_DIR),
            DOGESTONIA_ROLES_MANIFEST=str(_ROLES_MANIFEST),
        ),
        dedupe_store=EventDedupeStore(),
        interview_engine=engine,
    )
    client = TestClient(app)
    r = client.post("/v1/channel/turns", json=_turn("6603"), headers=_auth())
    assert r.status_code == 200
    ev = app.state.channel_wire.last_evidence
    assert ev.get("wired") is True
    assert ev.get("assembled") is True
    assert ev.get("cutover") is True
    assert ev.get("role_id") == "interviewer"
    assert engine.instructions != "ADR1-mega-before"


def test_t04_local_gpt48_export_consume_light() -> None:
    """MVP light: Present GPT-48 export inventory loads; no invent bodies."""
    assert _EXPORT_MANIFEST.is_file(), "GPT UI export roles.manifest.json must be Present"
    assert_manifest_covers_v1(_EXPORT_MANIFEST)
    data = load_roles_manifest(_EXPORT_MANIFEST)
    assert data["bundle_version"]
    assert data["core"]
    core_path = _EXPORT / str(data["core"])
    assert core_path.is_file() and core_path.stat().st_size > 0
    for rid, entry in data["roles"].items():
        fpath = _EXPORT / str(entry["file"])
        assert fpath.is_file(), f"missing export role file for {rid}"
        assert fpath.stat().st_size > 0
    # content loader consume (OAS/pack from aibridge fixtures — not invent texts)
    bundle = load_content_bundle(
        instructions_dir=_EXPORT,
        manifest_path=_EXPORT_MANIFEST,
        source_commit="gpt48-export-local-66",
        wire_oas_path=_OAS,
        pack_schema_path=_PACK,
    )
    assert bundle.components.get("schema") == "roles"
    assert len(bundle.file_hashes) >= 6  # core + 5 roles


def test_t05_phase_a_files_legacy_dev_docs() -> None:
    text = _DOC.read_text(encoding="utf-8")
    assert "legacy/dev-only" in text or "legacy/dev" in text
    assert "files[]" in text
    assert "STORY-67" in text or "Railway" in text
    req = _REQ13.read_text(encoding="utf-8")
    assert "legacy/dev-only" in req
    assert "13-roles-schema-channel-cutover" in req or "runtime-docs/13" in req


def test_t08_story_gate_checklist() -> None:
    assert _DOC.is_file()
    assert peek_manifest_schema(_ROLES_MANIFEST) == "roles"
    assert _EXPORT_MANIFEST.is_file()
    # dual-confirm Keep — ConfirmationGuard.invalidate_send_permission Present
    from aibridge.confirm import ConfirmationGuard

    assert hasattr(ConfirmationGuard, "invalidate_send_permission")
