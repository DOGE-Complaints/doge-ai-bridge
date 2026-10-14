"""Aibridge-owned storage upload (DP2) — gateway does not hold write keys.

Credential gate is local to aibridge. Live vendor/bucket is not required for CI;
inject ``PosterUploadPort`` (mock) or use the default HTTPS mint for fixtures.
Provider / bucket id / CDN — Open (not invented as SSOT).
"""

from __future__ import annotations

from urllib.parse import quote

from aibridge.poster.errors import PosterFailure, PosterFailureClass
from aibridge.poster.port import PosterUploadPort

# Implement-local mint host for fixture/default path — not CDN/provider SSOT.
_DEFAULT_HTTPS_MINT_PREFIX = "https://aibridge-poster.test/objects/"


class MockHttpsUploader:
    """Test/harness port — returns HTTPS URL without a live bucket."""

    def __init__(self, url_prefix: str = _DEFAULT_HTTPS_MINT_PREFIX) -> None:
        if not url_prefix.startswith("https://"):
            raise ValueError("mock uploader prefix must be https://")
        self._prefix = url_prefix.rstrip("/") + "/"

    def upload(
        self,
        data: bytes,
        *,
        content_type: str,
        object_key: str,
    ) -> str:
        if not data:
            raise PosterFailure(
                PosterFailureClass.STORAGE_UPLOAD_FAILED,
                "empty poster bytes",
            )
        _ = content_type
        key = quote(object_key.strip("/"), safe="/")
        return f"{self._prefix}{key}"


class CredentialGatedUploader:
    """Require aibridge-owned credential before delegating to an inner port."""

    def __init__(self, credential: str, inner: PosterUploadPort) -> None:
        self._credential = (credential or "").strip()
        self._inner = inner

    def upload(
        self,
        data: bytes,
        *,
        content_type: str,
        object_key: str,
    ) -> str:
        if not self._credential:
            raise PosterFailure(
                PosterFailureClass.STORAGE_UPLOAD_FAILED,
                "aibridge storage credential missing",
            )
        url = self._inner.upload(
            data, content_type=content_type, object_key=object_key
        )
        if not isinstance(url, str) or not url.startswith("https://"):
            raise PosterFailure(
                PosterFailureClass.STORAGE_UPLOAD_FAILED,
                "upload did not yield public HTTPS URL",
            )
        return url


def build_default_uploader(credential: str) -> CredentialGatedUploader:
    """Production-path default: credential gate + mockable HTTPS mint (no live bucket)."""
    return CredentialGatedUploader(credential, MockHttpsUploader())
