"""t02 — content_bundle register-once + uniqueness."""

from __future__ import annotations

from pathlib import Path

from aibridge.content import load_content_bundle
from aibridge.registry import MemoryBundleRegistry, SqliteBundleRegistry

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "openapi"
    / "story-intake-actions.openapi.yaml"
)


def _loaded():
    return load_content_bundle(
        instructions_dir=FIXTURES / "instructions",
        manifest_path=FIXTURES / "instructions.manifest.json",
        source_commit="commit-a",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=FIXTURES / "pack" / "payload.schema.json",
    )


def test_memory_register_once_idempotent() -> None:
    reg = MemoryBundleRegistry()
    loaded = _loaded()
    first = reg.register_once(loaded)
    second = reg.register_once(loaded)
    assert first.bundle_hash == second.bundle_hash == loaded.bundle_hash
    assert first.verified_at == second.verified_at
    assert len(reg.list_hashes()) == 1


def test_sqlite_unique_bundle_hash(tmp_path: Path) -> None:
    db = tmp_path / "bundles.db"
    reg = SqliteBundleRegistry(db)
    loaded = _loaded()
    first = reg.register_once(loaded)
    second = reg.register_once(loaded)
    assert first.bundle_hash == second.bundle_hash
    assert reg.get(loaded.bundle_hash) is not None
    reg.close()
