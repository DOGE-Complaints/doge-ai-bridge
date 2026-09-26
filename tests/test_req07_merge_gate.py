"""STORY-AIBRIDGE-44 — REQ-07 merge-gate proof (TECH-ARCH §5.1 / AC-08).

Automated CI/local suite. No live Telegram / live OpenAI.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.interview import InterviewEngine
from aibridge.readiness import evaluate_readiness
from aibridge.registry import MemoryBundleRegistry
from aibridge.request_assembly import (
    ValidationGateError,
    schema_validation_complete,
    validate_gate2_pack_payload,
)
from aibridge.responses_client import RecordingResponsesClient, assemble_responses_request
from aibridge.sessions import MemorySessionStore
from aibridge.tool_gen import (
    CANONICAL_OPERATION_ID,
    assert_openai_projection_clean,
    generate_strict_tool,
    project_schema_for_openai,
)

ROOT = Path(__file__).resolve().parents[1]
WIRE_OAS = ROOT / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
PACK_CANONICAL = (
    ROOT / "src" / "instructions" / "schema-packs.uus_veerenni_civic.v3.payload.schema.json"
)
CONTENT_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
INVALID_PARAMS_FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "openai"
    / "invalid_function_parameters_uniqueitems.json"
)


def _keyword_in_schema_tree(node: object, keyword: str) -> bool:
    """Schema-keyword walk (property-map keys are names, not keywords)."""
    from aibridge.tool_gen import _PROPERTY_MAP_KEYS

    if isinstance(node, list):
        return any(_keyword_in_schema_tree(x, keyword) for x in node)
    if not isinstance(node, dict):
        return False
    for key, value in node.items():
        if key == keyword:
            return True
        if key in _PROPERTY_MAP_KEYS and isinstance(value, dict):
            if any(_keyword_in_schema_tree(pv, keyword) for pv in value.values()):
                return True
            continue
        if isinstance(value, (dict, list)) and _keyword_in_schema_tree(value, keyword):
            return True
    return False


def _content_settings(**overrides: object) -> Settings:
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
        DOGESTONIA_INSTRUCTIONS_DIR=str(CONTENT_FIXTURES / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(CONTENT_FIXTURES / "instructions.manifest.json"),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="ready-commit",
        DOGESTONIA_OPENAPI_PATH=str(WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(CONTENT_FIXTURES / "pack" / "payload.schema.json"),
        DOGESTONIA_SCHEMA_ID="tallinn_civic",
        DOGESTONIA_SCHEMA_VERSION="v1",
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


# --- §5.1 #1 + REQ §11.4 — Responses tools payload ---


def test_merge_gate_responses_tools_payload_no_uniqueitems() -> None:
    """§5.1#1 · §11.4 — recording transport: no uniqueItems under tools[*].parameters."""
    tool = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    assert tool["type"] == "function"
    assert tool["name"] == CANONICAL_OPERATION_ID == "postStoryDraftStash"
    assert tool["strict"] is True
    assert not _keyword_in_schema_tree(tool["parameters"], "uniqueItems")
    assert_openai_projection_clean(tool["parameters"])

    client = RecordingResponsesClient()
    engine = InterviewEngine(client=client, tools=[tool], model="gpt-test")
    result = engine.run_turn(session_id="merge-gate-s1", user_text="hello")
    assert result["ok"] is True
    assert result.get("gateway_called") is False
    assert len(client.calls) == 1
    payload = client.calls[0]
    assert payload["store"] is False
    assert payload["parallel_tool_calls"] is False
    tools = payload["tools"]
    assert isinstance(tools, list) and len(tools) == 1
    outbound = tools[0]
    assert outbound["name"] == "postStoryDraftStash"
    assert outbound["strict"] is True
    assert not _keyword_in_schema_tree(outbound["parameters"], "uniqueItems")
    # G-02 — full-object mutation proof (no soft OR on parameters alone).
    assert tool == outbound


def test_merge_gate_assemble_contract_knobs() -> None:
    """§11.4 — assemble_responses_request always store/parallel knobs."""
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "x"}],
        tools=[{"type": "function", "name": "postStoryDraftStash", "strict": True, "parameters": {}}],
    )
    assert req.payload["store"] is False
    assert req.payload["parallel_tool_calls"] is False


# --- §5.1 #2 — canonical pack unchanged ---


def test_merge_gate_canonical_pack_unchanged_by_projection() -> None:
    """§5.1#2 · AC-01 — disk + in-memory pack retain houses uniqueItems:true."""
    pack_before = PACK_CANONICAL.read_bytes()
    pack = json.loads(pack_before.decode("utf-8"))
    houses = pack["properties"]["geo"]["properties"]["streets"]["items"]["properties"]["houses"]
    assert houses.get("uniqueItems") is True
    snapshot = copy.deepcopy(pack)

    projected = project_schema_for_openai(pack)
    assert pack == snapshot
    assert PACK_CANONICAL.read_bytes() == pack_before
    assert not _keyword_in_schema_tree(projected, "uniqueItems")
    assert houses.get("uniqueItems") is True

    generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    assert PACK_CANONICAL.read_bytes() == pack_before
    assert b'"uniqueItems"' in pack_before


# --- §5.1 #3 + #5 — Gate 2 + regression fixture ---


def test_merge_gate_gate2_rejects_duplicate_houses() -> None:
    """§5.1#3 — Gate 2 rejects duplicate houses under one street."""
    pack = json.loads(PACK_CANONICAL.read_text(encoding="utf-8"))
    payload = {
        "signals": {"civic_domain": "roads", "failure_pattern": "pothole"},
        "geo": {"streets": [{"street": "Veerenni", "houses": ["24", "24"]}]},
    }
    with pytest.raises(ValidationGateError, match=r"gate2:.*uniqueItems"):
        validate_gate2_pack_payload(payload, pack)


def test_merge_gate_invalid_function_parameters_fixture() -> None:
    """§5.1#5 — regression fixture for prior invalid_function_parameters / uniqueItems."""
    assert INVALID_PARAMS_FIXTURE.is_file()
    data = json.loads(INVALID_PARAMS_FIXTURE.read_text(encoding="utf-8"))
    err = data["error"]
    assert err["code"] == "invalid_function_parameters"
    assert "uniqueItems" in err["message"]
    assert "tools[0].parameters" in err["param"]
    # Prove remediation path: projected tool has no uniqueItems (would avoid this error).
    tool = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    assert not _keyword_in_schema_tree(tool["parameters"], "uniqueItems")


# --- §5.1 #4 + T-READY — VC / readyz without OpenAI ---


def test_merge_gate_readyz_vc_not_bound() -> None:
    """§5.1#4 — missing VC → /readyz not_ready; no OpenAI call."""
    settings = _content_settings()
    engine = InterviewEngine(client=RecordingResponsesClient())
    guard = reset_confirmation_guard(ConfirmationGuard(interview_engine=engine))
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        session_store=MemorySessionStore(),
        interview_engine=engine,
        confirmation_guard=guard,
    )
    assert isinstance(engine.client, RecordingResponsesClient)
    openai_calls_before = len(engine.client.calls)

    app.state.confirmation_guard.validation_context = None
    client = TestClient(app)
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["reason"] == "validation_context_not_bound"
    assert len(engine.client.calls) == openai_calls_before  # no OpenAI from /readyz

    result = evaluate_readiness(
        settings,
        app.state.deployment_bundle,
        validation_context=None,
    )
    assert result.ready is False
    assert result.reason == "validation_context_not_bound"


def test_merge_gate_t_ready_schema_validation_complete_no_openai() -> None:
    """T-READY — schema_validation_complete proves uniqueItems locally (no OpenAI)."""
    assert schema_validation_complete() is True
