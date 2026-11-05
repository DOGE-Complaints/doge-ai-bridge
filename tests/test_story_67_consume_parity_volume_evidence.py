"""STORY-AIBRIDGE-67 — consume parity (E1) + volume honesty.

Locks: adopt GPT E1 only · stale evidence ≠ Export Pass ·
t07 without ops window → Explicit Partial · no invent Railway/live SUCCESS.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.export_parity import (
    HASH_METHOD_E1,
    WIRE_E1,
    compare_mount_to_export,
    load_export_inventory,
)
from aibridge.registry import MemoryBundleRegistry

_REPO = Path(__file__).resolve().parents[1]
_WORKSPACE = _REPO.parent
_DOC11 = _REPO / "docs" / "runtime-docs" / "11-content-volume-parity-stub-live-evidence.md"
_DOC14 = _REPO / "docs" / "runtime-docs" / "14-hybrid-c-volume-consume-parity-runbook.md"
_REQ13 = (
    _REPO
    / "docs"
    / "requirements"
    / "REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md"
)
_PREFLIGHT = (
    _REPO
    / "docs"
    / "analysis"
    / "story-67-export-preflight-e1-reconfirm-20261105.md"
)
_LIVE_PARTIAL = (
    _REPO
    / "docs"
    / "analysis"
    / "story-67-live-volume-evidence-explicit-partial-20261105.md"
)
_INDEX = (
    _REPO
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "req-13-req15-semantic-state-roles-instruction-assembly"
    / "INDEX.md"
)
_STORY = (
    _REPO
    / "docs"
    / "tasks"
    / "epics"
    / "EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly"
    / "stories"
    / "STORY-AIBRIDGE-67-consume-parity-volume-evidence"
    / "STORY-AIBRIDGE-67-consume-parity-volume-evidence.md"
)
_FIXTURES = _REPO / "tests" / "fixtures" / "content"
_PARITY = _REPO / "tests" / "fixtures" / "parity"
_ROLES_DIR = _FIXTURES / "roles-instructions"
_ROLES_MANIFEST = _FIXTURES / "roles.manifest.json"
_WIRE_OAS = _REPO / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
_GPT_EVIDENCE = (
    _WORKSPACE / "GPT UI" / "docs" / "analysis" / "req-48-export-parity-evidence.md"
)
_GPT_EXPORT = _WORKSPACE / "GPT UI" / "instructions-roles"
_GPT_EXPORT_STALE_PATH = _WORKSPACE / "GPT UI" / "instructions-roles-req15"


def _content_settings(**overrides: str) -> Settings:
    reset_settings_cache()
    base = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        GATEWAY_SERVICE_API_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INSTRUCTIONS_DIR=str(_ROLES_DIR),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(_ROLES_MANIFEST),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="ready-commit",
        DOGESTONIA_OPENAPI_PATH=str(_WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(_FIXTURES / "pack" / "payload.schema.json"),
        DOGESTONIA_SCHEMA_ID="tallinn_civic",
        DOGESTONIA_SCHEMA_VERSION="v1",
        DATABASE_URL="memory",
        AIBRIDGE_ALLOW_MEMORY_STORES=True,
        GATEWAY_BASE_URL="https://gateway.example.invalid",
        SPA_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_INTERVIEW_PROVIDER="openai",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def _client(settings: Settings) -> TestClient:
    return TestClient(
        create_app(
            settings=settings,
            dedupe_store=EventDedupeStore(),
            bundle_registry=MemoryBundleRegistry(),
        )
    )


# --- t01 preflight ---


def test_t01_export_preflight_stale_block_pass_claim() -> None:
    assert _PREFLIGHT.is_file()
    text = _PREFLIGHT.read_text(encoding="utf-8")
    assert "Explicit Block" in text or "stale" in text.lower()
    assert "instructions-roles-req15" in text
    assert "instructions-roles" in text
    assert "core.md" in text and ("DRIFT" in text or "drift" in text.lower())
    assert "Export Pass" in text
    assert "≠" in text or "not" in text.lower()
    assert not _GPT_EXPORT_STALE_PATH.is_dir()
    assert _GPT_EXPORT.is_dir()
    assert _GPT_EVIDENCE.is_file()
    # Stale evidence must not be treated as live Export Pass in our docs.
    assert "stale evidence ≠ Export Pass" in text.lower() or "≠ Export Pass" in text


# --- t02 E1 lock ---


def test_t02_joint_inventory_locked_e1() -> None:
    req = _REQ13.read_text(encoding="utf-8")
    assert "WIRE_E1" in req or "wire: e1" in req.lower() or "**E1**" in req or "GPT E1" in req
    assert "normalize_text" in req and "sha256" in req.lower()
    assert "session_pin" in req.lower()
    assert "Locked" in req or "locked" in req
    doc = _DOC11.read_text(encoding="utf-8")
    assert "E1" in doc and ("locked" in doc.lower() or "Locked" in doc)
    assert WIRE_E1 == "e1"
    assert HASH_METHOD_E1 == "normalize_text+sha256_hex"


# --- t03 / t05 comparator matrix ---


def test_t03_t05_parity_pass() -> None:
    result = compare_mount_to_export(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        export_inventory_path=_PARITY / "export-inventory-e1-pass.json",
    )
    assert result.ok
    assert result.ready_reason == "export_parity_ok"


def test_t05_parity_missing() -> None:
    result = compare_mount_to_export(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        export_inventory_path=_PARITY / "export-inventory-e1-missing.json",
    )
    assert not result.ok
    assert result.reason == "export_parity_missing"
    assert any(f.disposition == "missing" for f in result.findings)


def test_t05_parity_changed_hash() -> None:
    result = compare_mount_to_export(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        export_inventory_path=_PARITY / "export-inventory-e1-changed.json",
    )
    assert not result.ok
    assert result.reason == "export_parity_changed"
    assert any(f.name == "core.md" and f.disposition == "changed" for f in result.findings)


def test_t05_parity_unexpected() -> None:
    result = compare_mount_to_export(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        export_inventory_path=_PARITY / "export-inventory-e1-unexpected.json",
    )
    assert not result.ok
    assert result.reason == "export_parity_unexpected"
    assert any(f.disposition == "unexpected" for f in result.findings)


def test_t05_parity_bad_inventory() -> None:
    with pytest.raises(Exception):
        load_export_inventory(_PARITY / "export-inventory-bad.json")
    result = compare_mount_to_export(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        export_inventory_path=_PARITY / "export-inventory-bad.json",
    )
    assert not result.ok
    assert result.reason == "export_parity_bad_inventory"


def test_t05_parity_manifest_drift() -> None:
    result = compare_mount_to_export(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        export_inventory_path=_PARITY / "export-inventory-e1-manifest-drift.json",
    )
    assert not result.ok
    assert result.reason == "export_parity_manifest_drift"


# --- t04 readyz + seam ---


def test_t04_readyz_parity_pass_when_inventory_configured() -> None:
    settings = _content_settings(
        DOGESTONIA_EXPORT_INVENTORY_PATH=str(
            _PARITY / "export-inventory-e1-pass.json"
        ),
    )
    response = _client(settings).get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_t04_readyz_fail_closed_changed_hash() -> None:
    settings = _content_settings(
        DOGESTONIA_EXPORT_INVENTORY_PATH=str(
            _PARITY / "export-inventory-e1-changed.json"
        ),
    )
    response = _client(settings).get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "export_parity_changed"


def test_t04_roles_instructions_seam_mismatch_fail_closed() -> None:
    settings = _content_settings(
        DOGESTONIA_ROLES_INSTRUCTIONS_DIR=str(_FIXTURES / "instructions"),
        DOGESTONIA_ROLES_MANIFEST=str(_FIXTURES / "instructions.manifest.json"),
        DOGESTONIA_EXPORT_INVENTORY_PATH=str(
            _PARITY / "export-inventory-e1-pass.json"
        ),
    )
    assert settings.roles_instructions_seam_mismatch()
    response = _client(settings).get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "roles_instructions_seam_mismatch"


# --- t06 runbook ---


def test_t06_hybrid_c_runbook_present() -> None:
    assert _DOC14.is_file()
    text = _DOC14.read_text(encoding="utf-8")
    assert "Hybrid C" in text or "hybrid C" in text.lower() or "Hybrid-C" in text
    assert "DOGESTONIA_INSTRUCTIONS_DIR" in text
    assert "DOGESTONIA_EXPORT_INVENTORY_PATH" in text
    assert "Railway" in text
    assert "fixture/dev" in text.lower() or "image-baked" in text.lower()
    assert "session_pin" in text.lower()
    assert "no invent" in text.lower() or "Forbidden" in text or "do **not** invent" in text.lower()


# --- t07 Explicit Partial ---


def test_t07_live_volume_explicit_partial_no_invent_success() -> None:
    assert _LIVE_PARTIAL.is_file()
    text = _LIVE_PARTIAL.read_text(encoding="utf-8")
    assert "Explicit Partial" in text
    assert "ops window" in text.lower() or "Ops window" in text
    assert "SUCCESS" not in text.split("invent")[0] or "no invent" in text.lower()
    assert "not open" in text.lower() or "Not open" in text or "Absent" in text
    # Must not invent live Pass.
    assert "live Pass: Done" not in text
    assert "Railway SUCCESS" not in text


# --- t08 gate ---


def test_t08_story_gate_checklist() -> None:
    assert _STORY.is_file()
    story = _STORY.read_text(encoding="utf-8")
    assert "Explicit Partial" in story
    assert "E1" in story
    assert "pkg-000070" in story
    idx = _INDEX.read_text(encoding="utf-8")
    assert "67" in idx and ("Explicit Partial" in idx or "partial" in idx.lower())
    req = _REQ13.read_text(encoding="utf-8")
    assert "AC-AIB-13-05" in req
    assert "AC-AIB-13-06" in req
