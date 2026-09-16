"""STORY-AIBRIDGE-21 — OAS path contract (ADR-3 / REQ-05 §4.4)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "Dockerfile"
MANIFEST = ROOT / "src" / "instructions" / "instructions.manifest.json"
OPENAPI_DIR = ROOT / "docs" / "openapi"
WIRE_NAME = "story-intake-actions.openapi.yaml"
CHANNEL_NAME = "aibridge-channel-v1.openapi.yaml"
ENV_EXAMPLE = ROOT / ".env.example"


def test_dockerfile_copies_docs_openapi() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "COPY docs/openapi ./docs/openapi" in text
    assert (OPENAPI_DIR / WIRE_NAME).is_file()
    assert (OPENAPI_DIR / CHANNEL_NAME).is_file()


def test_env_example_openapi_path_is_story_intake() -> None:
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    assert f"DOGESTONIA_OPENAPI_PATH=docs/openapi/{WIRE_NAME}" in text
    assert "DOGESTONIA_SCHEMA_ID=uus_veerenni_civic" in text
    assert "DOGESTONIA_SCHEMA_VERSION=v3" in text
    assert CHANNEL_NAME not in [
        line.split("=", 1)[1].strip()
        for line in text.splitlines()
        if line.startswith("DOGESTONIA_OPENAPI_PATH=")
    ]


def test_channel_oas_not_in_instruction_manifest_files() -> None:
    import json

    files = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
    assert CHANNEL_NAME not in files
    assert WIRE_NAME not in files
    assert "aibridge-channel-v1.openapi.yaml" not in files
