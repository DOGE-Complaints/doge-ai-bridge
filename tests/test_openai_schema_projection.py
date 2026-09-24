"""STORY-AIBRIDGE-41 — OpenAI schema compatibility projection (T-COMPAT / AC)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from aibridge.tool_gen import (
    OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS,
    ToolGenError,
    _PROPERTY_MAP_KEYS,
    assert_openai_projection_clean,
    generate_strict_tool,
    project_schema_for_openai,
    tool_schema_canonical_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
WIRE_OAS = ROOT / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
PACK_FIXTURE = ROOT / "tests" / "fixtures" / "content" / "pack" / "payload.schema.json"
PACK_CANONICAL = (
    ROOT / "src" / "instructions" / "schema-packs.uus_veerenni_civic.v3.payload.schema.json"
)


def _keyword_in_schema_tree(node: object, keyword: str) -> bool:
    """True if *keyword* appears as a schema keyword (not a property-map key name).

    Walk aligns with production ``_PROPERTY_MAP_KEYS`` (G-01 / P6).
    """
    if isinstance(node, list):
        return any(_keyword_in_schema_tree(x, keyword) for x in node)
    if not isinstance(node, dict):
        return False
    for key, value in node.items():
        if key == keyword:
            return True
        if key in _PROPERTY_MAP_KEYS and isinstance(value, dict):
            # Keys under properties/$defs/… are names, not schema keywords.
            if any(_keyword_in_schema_tree(pv, keyword) for pv in value.values()):
                return True
            continue
        if isinstance(value, (dict, list)) and _keyword_in_schema_tree(value, keyword):
            return True
    return False


def test_helper_ignores_defs_entry_named_unique_items() -> None:
    """G-01 — `$defs` key named uniqueItems is not a schema keyword false-positive."""
    schema = {
        "type": "object",
        "$defs": {
            "uniqueItems": {"type": "string"},
        },
        "properties": {
            "ref": {"$ref": "#/$defs/uniqueItems"},
        },
    }
    assert not _keyword_in_schema_tree(schema, "uniqueItems")
    # Still detect real keyword under nested schema value.
    schema_kw = {
        "type": "object",
        "$defs": {
            "arr": {
                "type": "array",
                "uniqueItems": True,
                "items": {"type": "string"},
            }
        },
    }
    assert _keyword_in_schema_tree(schema_kw, "uniqueItems")
    projected = project_schema_for_openai(schema_kw)
    assert not _keyword_in_schema_tree(projected, "uniqueItems")



def test_policy_constant_sole_strip_allowlist() -> None:
    assert OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS == frozenset({"uniqueItems"})


def test_project_strips_unique_items_preserves_input(tmp_path: Path) -> None:
    """T-COMPAT-01/02/04 — nested uniqueItems removed; input unchanged."""
    schema = {
        "type": "object",
        "properties": {
            "houses": {
                "type": "array",
                "uniqueItems": True,
                "items": {"type": "string"},
            },
            "nested": {
                "type": "object",
                "properties": {
                    "tags": {
                        "type": "array",
                        "uniqueItems": True,
                        "items": {"type": "string"},
                    }
                },
            },
        },
    }
    before = copy.deepcopy(schema)
    projected = project_schema_for_openai(schema)
    assert schema == before
    assert not _keyword_in_schema_tree(projected, "uniqueItems")
    assert projected["properties"]["houses"]["type"] == "array"
    assert projected["properties"]["nested"]["properties"]["tags"]["type"] == "array"
    assert_openai_projection_clean(projected)


def test_project_preserves_property_named_unique_items() -> None:
    """T-COMPAT-05 — domain field named uniqueItems is not stripped."""
    schema = {
        "type": "object",
        "properties": {
            "uniqueItems": {"type": "boolean"},
            "houses": {
                "type": "array",
                "uniqueItems": True,
                "items": {"type": "string"},
            },
        },
        "required": ["uniqueItems", "houses"],
    }
    projected = project_schema_for_openai(schema)
    assert "uniqueItems" in projected["properties"]
    assert projected["properties"]["uniqueItems"]["type"] == "boolean"
    assert "uniqueItems" not in projected["properties"]["houses"]
    assert_openai_projection_clean(projected)


def test_generate_tool_no_unique_items_on_canonical_pack() -> None:
    """AC-03 · T-COMPAT-01 — OpenAI tool has no uniqueItems; strict + name."""
    assert _keyword_in_schema_tree(
        json.loads(PACK_CANONICAL.read_text(encoding="utf-8")), "uniqueItems"
    )
    tool = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    assert tool["name"] == "postStoryDraftStash"
    assert tool["strict"] is True
    assert not _keyword_in_schema_tree(tool["parameters"], "uniqueItems")
    assert_openai_projection_clean(tool["parameters"])


def test_disk_pack_and_oas_unchanged() -> None:
    """AC-01/02 · T-COMPAT-08 — no disk rewrite of pack or Story Intake OAS."""
    pack_before = PACK_CANONICAL.read_bytes()
    oas_before = WIRE_OAS.read_bytes()
    generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    assert PACK_CANONICAL.read_bytes() == pack_before
    assert WIRE_OAS.read_bytes() == oas_before
    assert b'"uniqueItems"' in pack_before


def test_input_python_pack_unchanged_via_project() -> None:
    """AC-05 · T-COMPAT-02 — projection never mutates the input Python object."""
    pack = json.loads(PACK_CANONICAL.read_text(encoding="utf-8"))
    snapshot = copy.deepcopy(pack)
    _ = project_schema_for_openai(pack)
    assert pack == snapshot


def test_deterministic_serialization() -> None:
    """AC-07 · T-COMPAT-03 — identical inputs → identical canonical bytes."""
    a = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    b = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    assert tool_schema_canonical_bytes(a) == tool_schema_canonical_bytes(b)


def test_fail_closed_when_projection_leaves_keyword(monkeypatch: pytest.MonkeyPatch) -> None:
    """T-COMPAT-07 — remaining forbidden keyword → tool_gen_failed path."""

    def _noop_project(schema: dict) -> dict:
        return schema

    monkeypatch.setattr("aibridge.tool_gen.project_schema_for_openai", _noop_project)
    with pytest.raises(ToolGenError, match="unsupported_keyword_remaining:uniqueItems"):
        generate_strict_tool(
            wire_oas_path=WIRE_OAS,
            pack_schema_path=PACK_CANONICAL,
            schema_id="uus_veerenni_civic",
            schema_version="v3",
        )


def test_fixture_pack_still_generates() -> None:
    """Regression: small fixture pack without uniqueItems still works."""
    tool = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_FIXTURE,
        schema_id="tallinn_civic",
        schema_version="v1",
    )
    assert tool["strict"] is True
    assert tool["name"] == "postStoryDraftStash"


def test_t_compat_06_supported_constraints_survive() -> None:
    """T-COMPAT-06 — supported constraints (minItems) remain after projection."""
    pack = json.loads(PACK_CANONICAL.read_text(encoding="utf-8"))
    houses_before = pack["properties"]["geo"]["properties"]["streets"]["items"]["properties"][
        "houses"
    ]
    assert houses_before.get("minItems") == 1
    assert houses_before.get("uniqueItems") is True

    tool = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_CANONICAL,
        schema_id="uus_veerenni_civic",
        schema_version="v3",
    )
    payload = tool["parameters"]["properties"]["schema_binding"]["properties"]["structured_payload"]
    houses = payload["properties"]["geo"]["properties"]["streets"]["items"]["properties"]["houses"]
    assert houses.get("minItems") == 1
    assert "uniqueItems" not in houses
    assert not _keyword_in_schema_tree(tool["parameters"], "uniqueItems")
