"""STORY-AIBRIDGE-43 — ValidationContext create_app bind + readyz fail-closed."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.coordinator import (
    ToolValidationError,
    validate_function_calls,
    validation_context_is_bound,
)
from aibridge.confirm_fsm import SessionState
from aibridge.dedupe import EventDedupeStore
from aibridge.interview import default_recording_engine
from aibridge.readiness import evaluate_readiness
from aibridge.registry import MemoryBundleRegistry
from aibridge.sessions import MemorySessionStore
from aibridge.tool_gen import CANONICAL_OPERATION_ID

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = ROOT / "docs" / "openapi" / "story-intake-actions.openapi.yaml"


def _base_overrides(**extra: object) -> dict[str, object]:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        GATEWAY_SERVICE_API_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        GATEWAY_BASE_URL="https://gateway.example.invalid",
        SPA_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
        DATABASE_URL="memory",
        AIBRIDGE_ALLOW_MEMORY_STORES=True,
    )
    base.update(extra)
    return base


def _content_settings(**overrides: object) -> Settings:
    base = _base_overrides(
        DOGESTONIA_INSTRUCTIONS_DIR=str(FIXTURES / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(FIXTURES / "instructions.manifest.json"),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="ready-commit",
        DOGESTONIA_OPENAPI_PATH=str(WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(FIXTURES / "pack" / "payload.schema.json"),
        DOGESTONIA_SCHEMA_ID="tallinn_civic",
        DOGESTONIA_SCHEMA_VERSION="v1",
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def _memory_app(settings: Settings, *, confirmation_guard: ConfirmationGuard | None = None):
    engine = default_recording_engine()
    guard = confirmation_guard
    if guard is None:
        guard = reset_confirmation_guard(ConfirmationGuard(interview_engine=engine))
    return create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        session_store=MemorySessionStore(),
        interview_engine=engine,
        confirmation_guard=guard,
    )


def test_create_app_binds_validation_context_when_content_configured() -> None:
    """t01 — dual schemas + constants on ConfirmationGuard when content+schema set."""
    settings = _content_settings()
    assert settings.content_configured()
    app = _memory_app(settings)
    guard = app.state.confirmation_guard
    vc = guard.validation_context
    assert validation_context_is_bound(vc)
    assert isinstance(vc.tool_parameters, dict) and vc.tool_parameters
    assert isinstance(vc.pack_schema, dict) and vc.pack_schema
    assert isinstance(vc.wire_schema, dict) and vc.wire_schema
    assert vc.constants.schema_id == "tallinn_civic"
    # G-01/G-03 — envelope enum for Gate 3; pack version only in schema_version_pack.
    assert vc.constants.schema_version == "m2.story_intake_envelope.v2"
    assert vc.constants.schema_version_pack == "v1"
    # Gate 1 uses projected tool parameters from strict_tool.
    assert app.state.deployment_bundle is not None
    assert app.state.deployment_bundle.strict_tool is not None
    assert vc.tool_parameters == app.state.deployment_bundle.strict_tool["parameters"]


def test_readyz_validation_context_not_bound_when_missing() -> None:
    """t02 — content ready but VC unbound → reason validation_context_not_bound."""
    settings = _content_settings()
    app = _memory_app(settings)
    assert app.state.deployment_bundle is not None and app.state.deployment_bundle.ready
    # Simulate missing bind (e.g. operator cleared / injection without VC).
    app.state.confirmation_guard.validation_context = None
    client = TestClient(app)
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "validation_context_not_bound"

    result = evaluate_readiness(
        settings,
        app.state.deployment_bundle,
        validation_context=None,
    )
    assert result.ready is False
    assert result.reason == "validation_context_not_bound"


def test_readyz_ok_when_validation_context_bound() -> None:
    """Bound VC + content ready → /readyz ready (no invent OpenAI/gateway)."""
    settings = _content_settings()
    app = _memory_app(settings)
    assert validation_context_is_bound(app.state.confirmation_guard.validation_context)
    client = TestClient(app)
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_ac06_no_silent_fc_accept_without_schemas() -> None:
    """AC-06 partial — consequential FC without VC raises schemas-not-configured."""
    with pytest.raises(ToolValidationError, match="schemas not configured"):
        validate_function_calls(
            [
                {
                    "name": CANONICAL_OPERATION_ID,
                    "call_id": "call_ac06",
                    "arguments": {"narrative": {"note": "x"}},
                }
            ],
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=None,
        )


def test_no_content_skips_vc_bind_requirement() -> None:
    """Without content_configured, unbound VC does not force validation_context_not_bound."""
    settings = Settings(_env_file=None, **_base_overrides())
    assert not settings.content_configured()
    result = evaluate_readiness(settings, deployment=None, validation_context=None)
    assert result.ready is True
