"""STORY-AIBRIDGE-64 — volume/parity stub + Explicit Partial honesty.

Product Done = gate/docs + stub. AC-05 live = Explicit Partial.
No invent live SUCCESS / Railway Pass / inventory hash SSOT.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.content import ContentLoadError, load_content_bundle
from aibridge.dedupe import EventDedupeStore
from aibridge.registry import MemoryBundleRegistry

_REPO = Path(__file__).resolve().parents[1]
_DOC = _REPO / "docs" / "runtime-docs" / "11-content-volume-parity-stub-live-evidence.md"
_INDEX = (
    _REPO
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "req-13-req15-semantic-state-roles-instruction-assembly"
    / "INDEX.md"
)
_FIXTURES = _REPO / "tests" / "fixtures" / "content"
_INCOMPLETE = _FIXTURES / "incomplete"
_WIRE_OAS = _REPO / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
_T62 = _REPO / "tests" / "test_story_62_semantic_state_store_invalidation.py"
_T63 = _REPO / "tests" / "test_story_63_roles_coordinator_assembly_fixtures.py"


def _content_settings(**overrides: str) -> Settings:
    reset_settings_cache()
    base = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        GATEWAY_SERVICE_API_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INSTRUCTIONS_DIR=str(_FIXTURES / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(_FIXTURES / "instructions.manifest.json"),
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


# --- t01 stub matrix cites ---


def test_t01_stub_matrix_cites_62_63_and_ac06() -> None:
    assert _DOC.is_file()
    text = _DOC.read_text(encoding="utf-8")
    assert "test_story_62_semantic_state_store_invalidation" in text
    assert "test_story_63_roles_coordinator_assembly_fixtures" in text
    assert "AC-AIB-13-01" in text
    assert "AC-AIB-13-02" in text
    assert "AC-AIB-13-03" in text
    assert "AC-AIB-13-07" in text
    assert "AC-AIB-13-08" in text
    assert "AC-AIB-13-06" in text
    assert _T62.is_file() and _T63.is_file()
    assert "live SUCCESS" in text.lower() or "Railway" in text
    assert "Explicit Partial" in text
    # No invented live Pass claim.
    assert "Live Pass this wave" not in text or "Explicit Partial" in text


# --- t02 volume path ---


def test_t02_prod_volume_path_documented_l13_2() -> None:
    text = _DOC.read_text(encoding="utf-8")
    assert "Railway volume" in text
    assert "DOGESTONIA_INSTRUCTIONS_DIR" in text
    assert "src/instructions/" in text
    assert "fixture/dev" in text.lower() or "fixture/dev" in text
    assert "AC-AIB-13-04" in text or "L13-2" in text


# --- t03 AC-06 fail-closed ---


def test_t03_incomplete_manifest_fail_closed() -> None:
    with pytest.raises(ContentLoadError, match="missing"):
        load_content_bundle(
            instructions_dir=_INCOMPLETE / "instructions",
            manifest_path=_INCOMPLETE / "instructions.manifest.json",
            source_commit="incomplete-commit",
            wire_oas_path=_WIRE_OAS,
            pack_schema_path=_FIXTURES / "pack" / "payload.schema.json",
        )


def test_t03_readyz_fail_closed_incomplete_fixture() -> None:
    settings = _content_settings(
        DOGESTONIA_INSTRUCTIONS_DIR=str(_INCOMPLETE / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(
            _INCOMPLETE / "instructions.manifest.json"
        ),
    )
    client = TestClient(
        create_app(
            settings=settings,
            dedupe_store=EventDedupeStore(),
            bundle_registry=MemoryBundleRegistry(),
        )
    )
    response = client.get("/readyz")
    assert response.status_code == 503
    reason = response.json()["reason"]
    assert "content_verify_failed" in reason or reason == "content_bundle_not_ready"


# --- t04 AC-05 Explicit Partial ---


def test_t04_ac05_explicit_partial_no_invent_live() -> None:
    text = _DOC.read_text(encoding="utf-8")
    assert "AC-AIB-13-05" in text
    assert "Explicit Partial" in text
    assert "GPT-48" in text or "export" in text.lower()
    assert "Not open" in text or "not open" in text.lower()
    assert "Forbidden" in text or "do **not** invent" in text.lower()
    # Must not claim live Done.
    assert "live/parity Done" in text or "live/parity **Done**" in text or "≠" in text
    assert "hash" in text.lower() and ("Open" in text or "not invented" in text.lower() or "do **not** invent" in text.lower())


# --- t05 INDEX honesty ---


def test_t05_package_index_honesty_stub_ne_ac05() -> None:
    assert _INDEX.is_file()
    text = _INDEX.read_text(encoding="utf-8")
    assert "stub ≠" in text or "stub !=" in text or "Honesty" in text
    assert "AC-AIB-13-05" in text or "AC-05" in text
    assert "Explicit Partial" in text
    assert "live SUCCESS" in text.lower() or "Railway" in text


# --- t08 gate ---


def test_t08_story_gate_docs_and_locks() -> None:
    assert _DOC.is_file()
    text = _DOC.read_text(encoding="utf-8")
    assert "AC-AIB-13-04" in text or "Railway volume" in text
    assert "AC-AIB-13-05" in text
    assert "AC-AIB-13-06" in text or "fail-closed" in text.lower()
    assert "Explicit Partial" in text
    assert "62" in text and "63" in text
    assert (_INCOMPLETE / "instructions.manifest.json").is_file()
