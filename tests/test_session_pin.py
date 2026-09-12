"""t04 — session pins content_bundle_hash; resume ignores newer disk bundle."""

from __future__ import annotations

from pathlib import Path

from aibridge.content import load_content_bundle
from aibridge.registry import MemoryBundleRegistry
from aibridge.sessions import MemorySessionStore

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "openapi"
    / "story-intake-actions.openapi.yaml"
)


def test_resume_uses_pinned_hash_not_current() -> None:
    reg = MemoryBundleRegistry()
    sessions = MemorySessionStore()
    bundle_a = load_content_bundle(
        instructions_dir=FIXTURES / "instructions",
        manifest_path=FIXTURES / "instructions.manifest.json",
        source_commit="commit-a",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=FIXTURES / "pack" / "payload.schema.json",
    )
    bundle_b = load_content_bundle(
        instructions_dir=FIXTURES / "instructions",
        manifest_path=FIXTURES / "instructions.manifest.json",
        source_commit="commit-b",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=FIXTURES / "pack" / "payload.schema.json",
    )
    assert bundle_a.bundle_hash != bundle_b.bundle_hash
    reg.register_once(bundle_a)
    reg.register_once(bundle_b)
    sessions.create(
        session_id="s1",
        content_bundle_hash=bundle_a.bundle_hash,
        deployment_id="node-1",
    )
    resumed = sessions.resume_bundle("s1", reg)
    assert resumed.bundle_hash == bundle_a.bundle_hash
    assert resumed.source_commit == "commit-a"
