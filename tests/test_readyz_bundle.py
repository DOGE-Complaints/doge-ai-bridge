"""t03 — /readyz fails on missing/mismatched content bundle."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.registry import MemoryBundleRegistry

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "openapi"
    / "story-intake-actions.openapi.yaml"
)


def _content_settings(**overrides: str) -> Settings:
    reset_settings_cache()
    base = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INSTRUCTIONS_DIR=str(FIXTURES / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(FIXTURES / "instructions.manifest.json"),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="ready-commit",
        DOGESTONIA_OPENAPI_PATH=str(WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(FIXTURES / "pack" / "payload.schema.json"),
        DATABASE_URL="memory",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(**base)


def test_readyz_ok_with_verified_bundle() -> None:
    settings = _content_settings()
    client = TestClient(
        create_app(
            settings=settings,
            dedupe_store=EventDedupeStore(),
            bundle_registry=MemoryBundleRegistry(),
        )
    )
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_readyz_fails_missing_pack() -> None:
    settings = _content_settings(
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(FIXTURES / "pack" / "missing.json")
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
    assert "content_verify_failed" in response.json()["reason"]
