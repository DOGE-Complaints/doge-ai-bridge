"""t02 — strict tool from wire OAS + pack; unsupported constructs fail."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from aibridge.tool_gen import (
    ToolGenError,
    generate_strict_tool,
    strip_server_owned_fields,
    tool_schema_canonical_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
WIRE_OAS = ROOT / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
PACK = ROOT / "tests" / "fixtures" / "content" / "pack" / "payload.schema.json"


def test_generate_strict_tool_from_wire_oas() -> None:
    tool = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK,
        schema_id="tallinn_civic",
        schema_version="v1",
    )
    assert tool["type"] == "function"
    assert tool["function"]["name"] == "postStoryDraftStash"
    assert tool["function"]["strict"] is True
    params = tool["function"]["parameters"]
    assert params["additionalProperties"] is False
    binding = params["properties"]["schema_binding"]["properties"]
    assert "title" in binding["structured_payload"]["properties"]
    # Deterministic bytes across runs.
    assert tool_schema_canonical_bytes(tool) == tool_schema_canonical_bytes(tool)


def test_unsupported_oneof_fails_startup(tmp_path: Path) -> None:
    oas = yaml.safe_load(WIRE_OAS.read_text(encoding="utf-8"))
    oas["components"]["schemas"]["I18nText"] = {
        "oneOf": [{"type": "string"}, {"type": "object"}]
    }
    bad = tmp_path / "bad-oas.yaml"
    bad.write_text(yaml.dump(oas), encoding="utf-8")
    with pytest.raises(ToolGenError, match="Unsupported OpenAPI construct"):
        generate_strict_tool(
            wire_oas_path=bad,
            pack_schema_path=PACK,
            schema_id="x",
            schema_version="v1",
        )


def test_strip_server_owned_fields() -> None:
    cleaned = strip_server_owned_fields(
        {
            "schema_version": "evil",
            "origin": {"source": "attacker", "conversation_id": "c1"},
            "schema_binding": {
                "schema_id": "hijack",
                "schema_version": "v9",
                "structured_payload": {"title": "t"},
            },
            "gateway_url": "https://evil.example",
            "narrative": {"title": {"et": "a", "ru": "b", "en": "c"}},
        }
    )
    assert "schema_version" not in cleaned
    assert "gateway_url" not in cleaned
    assert "origin" not in cleaned or "source" not in cleaned.get("origin", {})
    assert "schema_id" not in cleaned["schema_binding"]
    assert cleaned["schema_binding"]["structured_payload"]["title"] == "t"
