"""Deterministic strict Responses tool from wire OAS + pack projection."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import yaml

CANONICAL_OPERATION_ID = "postStoryDraftStash"

# Constructs that make canonical-to-tool conversion impossible (fail generation).
UNSUPPORTED_KEYWORDS = frozenset(
    {
        "oneOf",
        "anyOf",
        "not",
        "if",
        "then",
        "else",
        "patternProperties",
        "unevaluatedProperties",
        "dependentSchemas",
        "dependentRequired",
    }
)

# Valid canonical constraints OpenAI rejects; strip only from OpenAI-facing copy
# (AIB-COMPAT-10/11). Sole allow-list for projection strip targets.
OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS = frozenset({"uniqueItems"})

# Map keys whose *keys* are names (not schema keywords) — never strip property names.
_PROPERTY_MAP_KEYS = frozenset({"properties", "patternProperties", "$defs", "definitions"})
_SCHEMA_LIST_KEYS = frozenset({"allOf", "anyOf", "oneOf", "prefixItems"})

_logger = logging.getLogger(__name__)

# Model / n8n must never set these (AIB-GEN-03).
SERVER_OWNED_FIELD_PATHS = frozenset(
    {
        "schema_version",
        "schema_binding",
        "schema_binding.schema_id",
        "schema_binding.schema_version",
        "origin",
        "origin.source",
        "Authorization",
        "authorization",
        "gateway_url",
        "gateway_method",
        "gateway_path",
    }
)


class ToolGenError(ValueError):
    """Startup / conversion failure — no silent non-strict fallback."""


def _load_oas(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ToolGenError(f"Wire OAS missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ToolGenError("Wire OAS must be a mapping")
    return data


def _resolve_ref(doc: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ToolGenError(f"Unsupported external $ref: {ref}")
    node: Any = doc
    for part in ref[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            raise ToolGenError(f"Unresolved $ref: {ref}")
        node = node[part]
    if not isinstance(node, dict):
        raise ToolGenError(f"$ref target not object: {ref}")
    return node


def _merge_all_of(parts: list[Any], doc: dict[str, Any], stack: set[str]) -> dict[str, Any]:
    """Deterministic allOf merge for strict projection (not silent non-strict)."""
    merged: dict[str, Any] = {"type": "object", "properties": {}, "required": []}
    props: dict[str, Any] = merged["properties"]
    required: list[str] = []
    for part in parts:
        resolved = _deref(part, doc, stack)
        if not isinstance(resolved, dict):
            raise ToolGenError("allOf members must be objects")
        for pk, pv in (resolved.get("properties") or {}).items():
            props[pk] = pv
        for req in resolved.get("required") or []:
            if req not in required:
                required.append(req)
        if resolved.get("additionalProperties") is False:
            merged["additionalProperties"] = False
    merged["required"] = sorted(set(required) | set(props.keys())) if props else sorted(required)
    # After strict force, required = all props; keep merge for intermediate.
    return merged


def _deref(schema: Any, doc: dict[str, Any], stack: set[str]) -> Any:
    if not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        ref = str(schema["$ref"])
        if ref in stack:
            raise ToolGenError(f"Cyclic $ref: {ref}")
        stack.add(ref)
        resolved = _deref(_resolve_ref(doc, ref), doc, stack)
        stack.discard(ref)
        merged = {**resolved, **{k: v for k, v in schema.items() if k != "$ref"}}
        return _deref(merged, doc, stack)
    if "allOf" in schema:
        return _merge_all_of(list(schema["allOf"]), doc, stack)
    out: dict[str, Any] = {}
    for k, v in schema.items():
        if k in UNSUPPORTED_KEYWORDS:
            raise ToolGenError(f"Unsupported OpenAPI construct for strict tools: {k}")
        if k == "properties" and isinstance(v, dict):
            out[k] = {pk: _deref(pv, doc, stack) for pk, pv in v.items()}
        elif k == "items":
            out[k] = _deref(v, doc, stack)
        elif k == "additionalProperties" and isinstance(v, dict):
            out[k] = _deref(v, doc, stack)
        else:
            out[k] = v
    return out


def _strip_openapi_only(schema: dict[str, Any]) -> dict[str, Any]:
    drop = {
        "example",
        "examples",
        "xml",
        "externalDocs",
        "discriminator",
        "nullable",
        "readOnly",
        "writeOnly",
        "deprecated",
        "title",
        "description",
    }
    out: dict[str, Any] = {}
    for k, v in schema.items():
        if k in drop:
            continue
        if k == "properties" and isinstance(v, dict):
            out[k] = {pk: _strip_openapi_only(pv) if isinstance(pv, dict) else pv for pk, pv in v.items()}
        elif k == "items" and isinstance(v, dict):
            out[k] = _strip_openapi_only(v)
        else:
            out[k] = v
    # nullable → type union with null
    if schema.get("nullable") is True:
        t = out.get("type")
        if isinstance(t, str):
            out["type"] = [t, "null"]
        elif isinstance(t, list) and "null" not in t:
            out["type"] = [*t, "null"]
    return out


def _force_strict_object(schema: dict[str, Any]) -> dict[str, Any]:
    schema = copy.deepcopy(schema)
    if schema.get("type") == "object" or "properties" in schema:
        props = schema.setdefault("properties", {})
        if not isinstance(props, dict):
            raise ToolGenError("object properties must be a mapping")
        schema["additionalProperties"] = False
        schema["required"] = sorted(props.keys())
        for name, child in list(props.items()):
            if isinstance(child, dict):
                props[name] = _force_strict_object(child)
    if schema.get("type") == "array" and isinstance(schema.get("items"), dict):
        schema["items"] = _force_strict_object(schema["items"])
    return schema


def project_schema_for_openai(schema: dict[str, Any]) -> dict[str, Any]:
    """Return a deep-copied OpenAI-compatible schema; never mutate input.

    Removes only JSON Schema *keywords* listed in ``OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS``.
    Does not delete domain property names that happen to match those strings
    (AIB-COMPAT-02 / T-COMPAT-05).
    """
    if not isinstance(schema, dict):
        raise ToolGenError("openai_schema_projection_failed")
    try:
        return _project_schema_node(copy.deepcopy(schema))
    except ToolGenError:
        raise
    except Exception as exc:  # noqa: BLE001 — fail closed
        raise ToolGenError("openai_schema_projection_failed") from exc


def _project_schema_node(node: Any) -> Any:
    if isinstance(node, list):
        return [_project_schema_node(item) for item in node]
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key in OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS:
            continue
        if key in _PROPERTY_MAP_KEYS and isinstance(value, dict):
            out[key] = {pk: _project_schema_node(pv) for pk, pv in value.items()}
        elif key in _SCHEMA_LIST_KEYS and isinstance(value, list):
            out[key] = [_project_schema_node(item) for item in value]
        elif key == "items":
            out[key] = _project_schema_node(value)
        elif key == "additionalProperties" and isinstance(value, dict):
            out[key] = _project_schema_node(value)
        elif key in ("not", "if", "then", "else") and isinstance(value, dict):
            out[key] = _project_schema_node(value)
        elif isinstance(value, (dict, list)):
            out[key] = _project_schema_node(value)
        else:
            out[key] = value
    return out


def count_openai_unsupported_keywords(schema: Any) -> dict[str, int]:
    """Count schema-keyword occurrences of policy keywords (not property names)."""
    counts = {name: 0 for name in sorted(OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS)}

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return
        for key, value in node.items():
            if key in OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS:
                counts[key] = counts.get(key, 0) + 1
                continue
            if key in _PROPERTY_MAP_KEYS and isinstance(value, dict):
                for pv in value.values():
                    walk(pv)
            elif key in _SCHEMA_LIST_KEYS and isinstance(value, list):
                walk(value)
            elif key in ("items", "additionalProperties", "not", "if", "then", "else"):
                walk(value)
            elif isinstance(value, (dict, list)):
                walk(value)

    walk(schema)
    return {k: v for k, v in counts.items() if v > 0}


def assert_openai_projection_clean(schema: dict[str, Any]) -> None:
    """Fail closed if any policy keyword remains as a schema keyword."""
    found = _first_unsupported_schema_keyword(schema)
    if found is not None:
        raise ToolGenError(f"unsupported_keyword_remaining:{found}")


def _first_unsupported_schema_keyword(node: Any) -> str | None:
    if isinstance(node, list):
        for item in node:
            found = _first_unsupported_schema_keyword(item)
            if found is not None:
                return found
        return None
    if not isinstance(node, dict):
        return None
    for key, value in node.items():
        if key in OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS:
            return key
        if key in _PROPERTY_MAP_KEYS and isinstance(value, dict):
            for pv in value.values():
                found = _first_unsupported_schema_keyword(pv)
                if found is not None:
                    return found
        elif key in _SCHEMA_LIST_KEYS and isinstance(value, list):
            found = _first_unsupported_schema_keyword(value)
            if found is not None:
                return found
        elif key in ("items", "additionalProperties", "not", "if", "then", "else"):
            found = _first_unsupported_schema_keyword(value)
            if found is not None:
                return found
        elif isinstance(value, (dict, list)):
            found = _first_unsupported_schema_keyword(value)
            if found is not None:
                return found
    return None


def _emit_projection_ready_event(
    *,
    tool: dict[str, Any],
    pack: dict[str, Any],
    removed_keywords: dict[str, int],
) -> None:
    """Redacted init event (REQ-07 §10). Must never raise into caller."""
    try:
        pack_hash = hashlib.sha256(
            json.dumps(pack, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        tool_hash = hashlib.sha256(tool_schema_canonical_bytes(tool)).hexdigest()
        _logger.info(
            "openai_schema_projection_ready tool=%s removed_keywords=%s "
            "canonical_pack_hash=%s projected_tool_hash=%s",
            tool.get("name"),
            removed_keywords,
            pack_hash,
            tool_hash,
        )
    except Exception:  # noqa: BLE001 — never block readiness on logging
        pass


def resolve_canonical_operation(oas: dict[str, Any]) -> dict[str, Any]:
    matches: list[tuple[str, str, dict[str, Any]]] = []
    for path, item in (oas.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if not isinstance(op, dict):
                continue
            if op.get("operationId") == CANONICAL_OPERATION_ID:
                matches.append((str(path), str(method).lower(), op))
    if len(matches) != 1:
        raise ToolGenError(
            f"operationId {CANONICAL_OPERATION_ID} must be unique (found {len(matches)})"
        )
    path, method, op = matches[0]
    if method != "post":
        raise ToolGenError(f"{CANONICAL_OPERATION_ID} must be POST")
    if path != "/story-drafts":
        raise ToolGenError(f"{CANONICAL_OPERATION_ID} path must be /story-drafts")
    security = op.get("security") or oas.get("security")
    if not security:
        raise ToolGenError(f"{CANONICAL_OPERATION_ID} must declare Bearer security")
    responses = op.get("responses") or {}
    if "201" not in responses:
        raise ToolGenError(f"{CANONICAL_OPERATION_ID} must declare success 201")
    return {"path": path, "method": method, "operation": op}


def load_wire_request_schema(wire_oas_path: Path) -> dict[str, Any]:
    """Canonical Story Intake request-body schema (Gate 3) — not OpenAI-projected."""
    oas = _load_oas(wire_oas_path)
    resolved = resolve_canonical_operation(oas)
    op = resolved["operation"]
    body = (op.get("requestBody") or {}).get("content", {}).get("application/json", {})
    schema_node = body.get("schema")
    if not isinstance(schema_node, dict):
        raise ToolGenError("requestBody application/json schema required")
    wire_schema = _deref(schema_node, oas, set())
    if not isinstance(wire_schema, dict):
        raise ToolGenError("dereferenced request schema must be object")
    return wire_schema


def generate_strict_tool(
    *,
    wire_oas_path: Path,
    pack_schema_path: Path,
    schema_id: str,
    schema_version: str,
) -> dict[str, Any]:
    """Return deterministic Responses function tool JSON (strict:true)."""
    wire_schema = load_wire_request_schema(wire_oas_path)
    resolved = resolve_canonical_operation(_load_oas(wire_oas_path))

    if not pack_schema_path.is_file():
        raise ToolGenError(f"Pack schema missing: {pack_schema_path}")
    pack = json.loads(pack_schema_path.read_text(encoding="utf-8"))
    if not isinstance(pack, dict):
        raise ToolGenError("Pack schema must be a JSON object")

    # Model-facing: project structured_payload from pack (AIB-GEN-02).
    model_schema = _strip_openapi_only(wire_schema)
    props = model_schema.setdefault("properties", {})
    if not isinstance(props, dict):
        raise ToolGenError("schema.properties must be a mapping")
    binding = props.get("schema_binding")
    if isinstance(binding, dict):
        bprops = binding.setdefault("properties", {})
        if isinstance(bprops, dict):
            bprops["structured_payload"] = copy.deepcopy(pack)
            # Keep schema_id/version as strings for model visibility but server overrides on assemble.
    model_schema = _force_strict_object(model_schema)

    # OpenAI compatibility projection (REQ-07 / AIB-COMPAT-01…03): strip policy keywords
    # from the in-memory tool only — never mutate pack/OAS on disk or the input pack object.
    removed_keywords = count_openai_unsupported_keywords(model_schema)
    model_schema = project_schema_for_openai(model_schema)
    assert_openai_projection_clean(model_schema)

    tool = {
        "type": "function",
        "name": CANONICAL_OPERATION_ID,
        "description": "Stash a story draft for browser submit",
        "strict": True,
        "parameters": model_schema,
        "x_aibridge": {
            "schema_id": schema_id,
            "schema_version": schema_version,
            "operation_path": resolved["path"],
            "operation_method": resolved["method"],
        },
    }
    _emit_projection_ready_event(tool=tool, pack=pack, removed_keywords=removed_keywords)
    # Deterministic serialization order via sorted keys when hashed.
    return tool


def to_responses_flat_tool(tool: dict[str, Any]) -> dict[str, Any]:
    """Normalize nested Chat Completions function wrap → Responses-flat."""
    if "function" in tool and isinstance(tool.get("function"), dict):
        nested = tool["function"]
        flat: dict[str, Any] = {
            "type": "function",
            "name": nested.get("name"),
            "strict": nested.get("strict", True),
            "parameters": nested.get("parameters"),
        }
        if nested.get("description") is not None:
            flat["description"] = nested["description"]
        for key, value in tool.items():
            if key in {"type", "function"}:
                continue
            flat[key] = value
        return flat
    # Already flat — require name/parameters/strict at top level.
    if tool.get("type") == "function" and "name" in tool and "parameters" in tool:
        return tool
    raise ToolGenError("tool must be Responses-flat or nested function wrap")


def strip_server_owned_fields(args: dict[str, Any]) -> dict[str, Any]:
    """Remove model attempts to set server-owned fields (AIB-GEN-03 / AC #4)."""
    out = copy.deepcopy(args)
    for key in ("schema_version", "Authorization", "authorization", "gateway_url", "gateway_method", "gateway_path"):
        out.pop(key, None)
    origin = out.get("origin")
    if isinstance(origin, dict):
        origin.pop("source", None)
        if not origin:
            out.pop("origin", None)
    binding = out.get("schema_binding")
    if isinstance(binding, dict):
        binding.pop("schema_id", None)
        binding.pop("schema_version", None)
    return out


def tool_schema_canonical_bytes(tool: dict[str, Any]) -> bytes:
    return json.dumps(tool, sort_keys=True, separators=(",", ":")).encode("utf-8")
