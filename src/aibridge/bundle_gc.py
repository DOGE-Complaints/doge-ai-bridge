"""Bundle GC — delete only if no active sessions and grace elapsed."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from aibridge.registry import BundleRegistry
from aibridge.sessions import SessionStore


def gc_unreferenced_bundles(
    registry: BundleRegistry,
    sessions: SessionStore,
    *,
    grace_seconds: int,
    now: datetime | None = None,
) -> list[str]:
    """Delete bundles with no active session refs after grace.

    Returns deleted bundle_hash list.
    """
    if grace_seconds < 0:
        raise ValueError("grace_seconds must be >= 0")
    clock = now or datetime.now(timezone.utc)
    referenced = sessions.active_bundle_hashes()
    deleted: list[str] = []
    for bundle_hash in list(registry.list_hashes()):
        if bundle_hash in referenced:
            continue
        row = registry.get(bundle_hash)
        if row is None:
            continue
        verified = row.verified_at
        if verified.tzinfo is None:
            verified = verified.replace(tzinfo=timezone.utc)
        if clock < verified + timedelta(seconds=grace_seconds):
            continue
        if registry.delete(bundle_hash):
            deleted.append(bundle_hash)
    return deleted
