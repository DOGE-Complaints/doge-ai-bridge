"""Regenerate / version distinguishability (AC-09-06)."""

from __future__ import annotations


def versions_distinguishable(version_a: str, version_b: str) -> bool:
    """True when generation-version strings differ (non-empty)."""
    a = (version_a or "").strip()
    b = (version_b or "").strip()
    if not a or not b:
        return False
    return a != b


def urls_distinguishable(url_a: str, url_b: str) -> bool:
    """True when poster HTTPS URLs differ."""
    a = (url_a or "").strip()
    b = (url_b or "").strip()
    if not a.startswith("https://") or not b.startswith("https://"):
        return False
    return a != b


def regenerate_assets_distinguishable(
    *,
    version_a: str,
    version_b: str,
    url_a: str,
    url_b: str,
) -> bool:
    """AC-09-06: new version work yields distinguishable version and/or URL."""
    return versions_distinguishable(version_a, version_b) and urls_distinguishable(
        url_a, url_b
    )
