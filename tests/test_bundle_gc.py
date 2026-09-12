"""t05 — GC skips active session refs; honors grace."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from aibridge.bundle_gc import gc_unreferenced_bundles
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


def test_gc_skips_referenced_and_honors_grace() -> None:
    reg = MemoryBundleRegistry()
    sessions = MemorySessionStore()
    bundle = load_content_bundle(
        instructions_dir=FIXTURES / "instructions",
        manifest_path=FIXTURES / "instructions.manifest.json",
        source_commit="gc-commit",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=FIXTURES / "pack" / "payload.schema.json",
    )
    row = reg.register_once(bundle)
    sessions.create(
        session_id="alive",
        content_bundle_hash=row.bundle_hash,
        deployment_id="n1",
    )
    now = datetime.now(timezone.utc) + timedelta(days=30)
    deleted = gc_unreferenced_bundles(
        reg, sessions, grace_seconds=3600, now=now
    )
    assert deleted == []
    assert reg.get(row.bundle_hash) is not None

    sessions.deactivate("alive")
    # Still within grace relative to verified_at if grace huge from now-back
    early = row.verified_at + timedelta(seconds=10)
    deleted_early = gc_unreferenced_bundles(
        reg, sessions, grace_seconds=3600, now=early
    )
    assert deleted_early == []

    late = row.verified_at + timedelta(seconds=3601)
    deleted_late = gc_unreferenced_bundles(
        reg, sessions, grace_seconds=3600, now=late
    )
    assert deleted_late == [row.bundle_hash]
    assert reg.get(row.bundle_hash) is None
