"""t05 — three validation gates, draft hash, cache hooks, server-owned overrides."""

from __future__ import annotations

import pytest

from aibridge.request_assembly import (
    CacheTelemetry,
    ServerConstants,
    ValidationGateError,
    assemble_server_body,
    build_stable_prefix,
    draft_hash,
    run_three_gates,
)


PACK_SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string"}},
    "required": ["title"],
    "additionalProperties": False,
}

TOOL_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "required": ["narrative", "schema_binding"],
    "properties": {
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["structured_payload"],
            "properties": {
                # Gate1: shape only; pack types enforced in gate2.
                "structured_payload": {"type": "object", "additionalProperties": True},
            },
        },
    },
}

WIRE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "narrative", "schema_binding", "origin"],
    "properties": {
        "schema_version": {"type": "string"},
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_id", "schema_version", "structured_payload"],
            "properties": {
                "schema_id": {"type": "string"},
                "schema_version": {"type": "string"},
                "structured_payload": PACK_SCHEMA,
            },
        },
        "origin": {
            "type": "object",
            "additionalProperties": False,
            "required": ["source"],
            "properties": {"source": {"type": "string"}},
        },
    },
}


def test_three_gates_and_server_owned_pack_origin() -> None:
    model_args = {
        "schema_version": "model_override_ignored",
        "narrative": {"note": "n"},
        "schema_binding": {
            "schema_id": "hijack",
            "schema_version": "v9",
            "structured_payload": {"title": "ok"},
        },
        "origin": {"source": "attacker"},
        "gateway_url": "https://evil",
    }
    constants = ServerConstants(
        schema_id="tallinn_civic",
        schema_version_pack="v1",
        origin_source="openai_responses_telegram",
    )
    body, h = run_three_gates(
        model_args,
        tool_parameters=TOOL_PARAMS,
        pack_schema=PACK_SCHEMA,
        wire_schema=WIRE_SCHEMA,
        constants=constants,
    )
    assert body["schema_version"] == "m2.story_intake_envelope.v2"
    assert body["schema_binding"]["schema_id"] == "tallinn_civic"
    assert body["schema_binding"]["schema_version"] == "v1"
    assert body["origin"]["source"] == "openai_responses_telegram"
    assert "gateway_url" not in body
    assert len(h) == 64
    assert draft_hash(body, revision=1) == h


def test_gate2_fails_on_bad_pack() -> None:
    model_args = {
        "narrative": {},
        "schema_binding": {"structured_payload": {"title": 1}},
    }
    with pytest.raises(ValidationGateError) as ei:
        run_three_gates(
            model_args,
            tool_parameters=TOOL_PARAMS,
            pack_schema=PACK_SCHEMA,
            wire_schema=WIRE_SCHEMA,
            constants=ServerConstants(schema_id="a", schema_version_pack="v1"),
        )
    assert ei.value.gate == 2


def test_stable_prefix_order_and_cache_hooks() -> None:
    prefix = build_stable_prefix(
        instructions="SYS",
        tool_schema_json='{"a":1}',
        pack_id="pack-1",
    )
    assert prefix.startswith("<<<INSTRUCTIONS>>>\nSYS\n<<<TOOL_SCHEMA>>>")
    assert "<<<PACK_ID>>>\npack-1" in prefix
    cache = CacheTelemetry()
    cache.emit(tool_hash="t", pack_hash="p", cached_tokens=3)
    assert cache.events[0]["cached_tokens"] == 3


def test_assemble_server_body_strips_model_overrides() -> None:
    body = assemble_server_body(
        {
            "schema_version": "x",
            "schema_binding": {
                "schema_id": "bad",
                "schema_version": "bad",
                "structured_payload": {"title": "t"},
            },
            "origin": {"source": "bad"},
        },
        constants=ServerConstants(schema_id="good", schema_version_pack="v1"),
    )
    assert body["schema_binding"]["schema_id"] == "good"
    assert body["origin"]["source"] == "openai_responses_telegram"
