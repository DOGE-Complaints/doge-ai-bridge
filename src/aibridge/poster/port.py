"""Mockable poster upload port (DP8 seam for STORY-50 harness).

Provider / bucket / CDN hostnames remain Open — not SSOT in this module.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class PosterUploadPort(Protocol):
    """Upload poster bytes → public HTTPS URL string."""

    def upload(
        self,
        data: bytes,
        *,
        content_type: str,
        object_key: str,
    ) -> str:
        """Return a public ``https://`` URL or raise ``PosterFailure``."""
        ...
