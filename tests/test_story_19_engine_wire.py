"""STORY-AIBRIDGE-19 — assembled instructions → InterviewEngine (ADR-1)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import _apply_deployment_to_engine, create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.content import LoadedContentBundle
from aibridge.dedupe import EventDedupeStore
from aibridge.deployment import DeploymentBundleState
from aibridge.interview import default_recording_engine
from aibridge.registry import ContentBundleRow, MemoryBundleRegistry

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "openapi"
    / "story-intake-actions.openapi.yaml"
)


def _content_settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INSTRUCTIONS_DIR=str(FIXTURES / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(FIXTURES / "instructions.manifest.json"),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="ready-commit",
        DOGESTONIA_OPENAPI_PATH=str(WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(FIXTURES / "pack" / "payload.schema.json"),
        DATABASE_URL="memory",
        DOGESTONIA_API_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(**base)


def _loaded(*, assembled: str = "# first\n\n# second") -> LoadedContentBundle:
    return LoadedContentBundle(
        bundle_version="test-v1",
        source_commit="ready-commit",
        instructions_hash="i" * 64,
        wire_oas_hash="w" * 64,
        pack_hash="p" * 64,
        tool_schema_hash="t" * 64,
        bundle_hash="b" * 64,
        assembled_instructions=assembled,
        file_hashes=(("alpha.md", "a" * 64),),
        components={},
    )


def _registered(loaded: LoadedContentBundle) -> ContentBundleRow:
    return ContentBundleRow(
        bundle_hash=loaded.bundle_hash,
        source_commit=loaded.source_commit,
        bundle_version=loaded.bundle_version,
        instructions_hash=loaded.instructions_hash,
        wire_oas_hash=loaded.wire_oas_hash,
        pack_hash=loaded.pack_hash,
        tool_schema_hash=loaded.tool_schema_hash,
        verified_at=datetime.now(timezone.utc),
        components_json="{}",
    )


def test_helper_sets_prefix_instructions_from_ready_deploy() -> None:
    engine = default_recording_engine()
    loaded = _loaded(assembled="MODULE-1 canon")
    deployment = DeploymentBundleState(
        loaded=loaded,
        registered=_registered(loaded),
        error=None,
        strict_tool=None,
    )
    settings = _content_settings()
    out = _apply_deployment_to_engine(engine, deployment, settings)
    assert out is deployment
    assert engine.prompt_channel == "prefix"
    assert engine.instructions == "MODULE-1 canon"
    assert engine.tools == []


def test_helper_maps_strict_tool_and_pack_id() -> None:
    engine = default_recording_engine()
    tool = {"type": "function", "name": "postStoryDraftStash", "strict": True}
    loaded = _loaded()
    deployment = DeploymentBundleState(
        loaded=loaded,
        registered=_registered(loaded),
        error=None,
        strict_tool=tool,
    )
    settings = _content_settings(
        DOGESTONIA_SCHEMA_ID="tallinn_civic",
        DOGESTONIA_SCHEMA_VERSION="v1",
    )
    _apply_deployment_to_engine(engine, deployment, settings)
    assert engine.tools == [tool]
    assert engine.pack_id == "tallinn_civic/v1"


def test_helper_does_not_invent_tool_when_strict_tool_none() -> None:
    engine = default_recording_engine(tools=[{"type": "function", "name": "keep"}])
    loaded = _loaded()
    deployment = DeploymentBundleState(
        loaded=loaded,
        registered=_registered(loaded),
        error=None,
        strict_tool=None,
    )
    _apply_deployment_to_engine(engine, deployment, _content_settings())
    assert engine.tools == [{"type": "function", "name": "keep"}]


def test_helper_fail_closed_empty_assembled() -> None:
    engine = default_recording_engine(instructions="stale")
    loaded = _loaded(assembled="   ")
    deployment = DeploymentBundleState(
        loaded=loaded,
        registered=_registered(loaded),
        error=None,
        strict_tool={"type": "function", "name": "x"},
    )
    out = _apply_deployment_to_engine(engine, deployment, _content_settings())
    assert out is not None
    assert out.error == "assembled_instructions_empty"
    assert out.ready is False
    assert engine.instructions == "stale"  # not silently overwritten to empty


def test_create_app_wires_assembled_into_engine_and_prefix_xor() -> None:
    settings = _content_settings()
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
    assert "# first" in engine.instructions
    assert "# second" in engine.instructions

    engine.run_turn(session_id="s19", user_text="hi")
    sent = engine.client.calls[0]
    assert "instructions" not in sent
    system = next(
        i for i in sent["input"] if isinstance(i, dict) and i.get("role") == "system"
    )
    assert "# first" in str(system.get("content", ""))


def test_create_app_wires_strict_tool_when_schema_configured() -> None:
    settings = _content_settings(
        DOGESTONIA_SCHEMA_ID="tallinn_civic",
        DOGESTONIA_SCHEMA_VERSION="v1",
    )
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        interview_engine=default_recording_engine(),
    )
    engine = app.state.interview_engine
    dep = app.state.deployment_bundle
    assert dep is not None and dep.strict_tool is not None
    assert engine.tools == [dep.strict_tool]
    assert engine.pack_id == "tallinn_civic/v1"


def test_readyz_fails_when_assembled_empty_after_helper() -> None:
    """Fail-closed surface: empty assembled → deployment.error → /readyz 503."""
    settings = _content_settings()
    engine = default_recording_engine()
    loaded = _loaded(assembled="")
    deployment = DeploymentBundleState(
        loaded=loaded,
        registered=_registered(loaded),
        error=None,
    )
    closed = _apply_deployment_to_engine(engine, deployment, settings)
    assert closed is not None and closed.error == "assembled_instructions_empty"

    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        interview_engine=default_recording_engine(),
    )
    # Inject fail-closed deploy after create (simulates empty assembled path).
    app.state.deployment_bundle = closed
    client = TestClient(app)
    assert client.get("/healthz").status_code == 200
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "assembled_instructions_empty"
