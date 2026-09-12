"""t01 — content load / hash / source-commit pin."""

from __future__ import annotations

from pathlib import Path

import pytest

from aibridge.content import ContentLoadError, load_content_bundle, sha256_hex

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "openapi"
    / "story-intake-actions.openapi.yaml"
)


def test_load_hashes_and_pins_source_commit() -> None:
    loaded = load_content_bundle(
        instructions_dir=FIXTURES / "instructions",
        manifest_path=FIXTURES / "instructions.manifest.json",
        source_commit="abc123deadbeef",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=FIXTURES / "pack" / "payload.schema.json",
    )
    assert loaded.source_commit == "abc123deadbeef"
    assert loaded.bundle_version == "test-v1"
    assert len(loaded.bundle_hash) == 64
    assert loaded.instructions_hash == sha256_hex(
        loaded.assembled_instructions.encode("utf-8")
    )
    assert "alpha.md" in dict(loaded.file_hashes)


def test_missing_file_fails() -> None:
    with pytest.raises(ContentLoadError, match="missing"):
        load_content_bundle(
            instructions_dir=FIXTURES / "instructions",
            manifest_path=FIXTURES / "instructions.manifest.json",
            source_commit="abc",
            wire_oas_path=WIRE_OAS,
            pack_schema_path=FIXTURES / "pack" / "does-not-exist.json",
        )


def test_loader_has_no_github_fetch_api() -> None:
    import aibridge.content as mod
    import inspect

    src = inspect.getsource(mod)
    assert "requests." not in src
    assert "httpx" not in src
    assert "urllib.request" not in src
    assert "github.com" not in src.lower()
