"""Request assembly, three validation gates, draft hash, cache hooks."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from aibridge.tool_gen import (
    CANONICAL_OPERATION_ID,
    strip_server_owned_fields,
)


class ValidationGateError(ValueError):
    """One of the three AIB-REQ-02 gates failed."""

    def __init__(self, gate: int, message: str) -> None:
        super().__init__(f"gate{gate}: {message}")
        self.gate = gate


@dataclass
class ServerConstants:
    schema_version: str = "m2.story_intake_envelope.v2"
    schema_id: str = ""
    schema_version_pack: str = ""
    origin_source: str = "openai_responses_telegram"


@dataclass
class CacheTelemetry:
    events: list[dict[str, Any]] = field(default_factory=list)

    def emit(
        self,
        *,
        bundle_hash: str | None = None,
        tool_hash: str | None = None,
        pack_hash: str | None = None,
        cached_tokens: int = 0,
    ) -> None:
        self.events.append(
            {
                "event": "cache_hint",
                "bundle_hash": bundle_hash,
                "tool_hash": tool_hash,
                "pack_hash": pack_hash,
                "cached_tokens": cached_tokens,
            }
        )


def stable_prefix_parts(
    *,
    instructions: str,
    tool_schema_json: str,
    pack_id: str,
) -> list[str]:
    """Deterministic prompt prefix order (AIB-CACHE / Scope #5)."""
    return [
        "<<<INSTRUCTIONS>>>",
        instructions,
        "<<<TOOL_SCHEMA>>>",
        tool_schema_json,
        "<<<PACK_ID>>>",
        pack_id,
    ]


def build_stable_prefix(
    *,
    instructions: str,
    tool_schema_json: str,
    pack_id: str,
) -> str:
    return "\n".join(
        stable_prefix_parts(
            instructions=instructions,
            tool_schema_json=tool_schema_json,
            pack_id=pack_id,
        )
    )


def _validate_type(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    """Minimal JSON Schema subset validator (type/required/properties/additionalProperties)."""
    types = schema.get("type")
    if types is not None:
        allowed = types if isinstance(types, list) else [types]
        ok = False
        for t in allowed:
            if t == "object" and isinstance(instance, dict):
                ok = True
            elif t == "array" and isinstance(instance, list):
                ok = True
            elif t == "string" and isinstance(instance, str):
                ok = True
            elif t == "number" and isinstance(instance, (int, float)) and not isinstance(instance, bool):
                ok = True
            elif t == "integer" and isinstance(instance, int) and not isinstance(instance, bool):
                ok = True
            elif t == "boolean" and isinstance(instance, bool):
                ok = True
            elif t == "null" and instance is None:
                ok = True
        if not ok:
            raise ValidationGateError(0, f"type mismatch at {path}")
    if isinstance(instance, dict):
        props = schema.get("properties") or {}
        required = schema.get("required") or []
        for req in required:
            if req not in instance:
                raise ValidationGateError(0, f"missing required {path}.{req}")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    raise ValidationGateError(0, f"additional property {path}.{key}")
        for key, child in instance.items():
            if key in props and isinstance(props[key], dict):
                _validate_type(child, props[key], f"{path}.{key}")
    if isinstance(instance, list) and isinstance(schema.get("items"), dict):
        for i, child in enumerate(instance):
            _validate_type(child, schema["items"], f"{path}[{i}]")


def validate_gate1_tool_args(args: dict[str, Any], tool_parameters: dict[str, Any]) -> None:
    try:
        _validate_type(args, tool_parameters)
    except ValidationGateError as exc:
        raise ValidationGateError(1, str(exc).removeprefix("gate0: ")) from exc


def validate_gate2_pack_payload(payload: Any, pack_schema: dict[str, Any]) -> None:
    try:
        _validate_type(payload, pack_schema)
    except ValidationGateError as exc:
        raise ValidationGateError(2, str(exc).removeprefix("gate0: ")) from exc


def validate_gate3_wire_body(body: dict[str, Any], wire_schema: dict[str, Any]) -> None:
    try:
        _validate_type(body, wire_schema)
    except ValidationGateError as exc:
        raise ValidationGateError(3, str(exc).removeprefix("gate0: ")) from exc


def assemble_server_body(
    model_args: dict[str, Any],
    *,
    constants: ServerConstants,
) -> dict[str, Any]:
    cleaned = strip_server_owned_fields(model_args)
    binding = dict(cleaned.get("schema_binding") or {})
    structured = binding.get("structured_payload")
    binding["schema_id"] = constants.schema_id
    binding["schema_version"] = constants.schema_version_pack
    if structured is not None:
        binding["structured_payload"] = structured
    body = {
        **cleaned,
        "schema_version": constants.schema_version,
        "schema_binding": binding,
        "origin": {"source": constants.origin_source},
    }
    return body


def draft_hash(
    body: dict[str, Any],
    *,
    operation_id: str = CANONICAL_OPERATION_ID,
    revision: int,
) -> str:
    domain = {
        "operation_id": operation_id,
        "revision": revision,
        "schema_binding": body.get("schema_binding"),
        "body": body,
    }
    canonical = json.dumps(domain, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_three_gates(
    model_args: dict[str, Any],
    *,
    tool_parameters: dict[str, Any],
    pack_schema: dict[str, Any],
    wire_schema: dict[str, Any],
    constants: ServerConstants,
) -> tuple[dict[str, Any], str]:
    """Gates 1→2→3 then return assembled body + draft hash (revision 1)."""
    cleaned = strip_server_owned_fields(model_args)
    validate_gate1_tool_args(cleaned, tool_parameters)
    binding = cleaned.get("schema_binding") or {}
    payload = binding.get("structured_payload") if isinstance(binding, dict) else None
    if payload is None:
        raise ValidationGateError(2, "structured_payload required")
    validate_gate2_pack_payload(payload, pack_schema)
    body = assemble_server_body(cleaned, constants=constants)
    validate_gate3_wire_body(body, wire_schema)
    return body, draft_hash(body, revision=1)
