"""Brief → poster bytes → aibridge-owned upload → public HTTPS URL (AC-09-03)."""

from __future__ import annotations

from aibridge.poster.errors import PosterFailure, PosterFailureClass
from aibridge.poster.image import generate_poster_bytes
from aibridge.poster.port import PosterUploadPort
from aibridge.poster.storage import CredentialGatedUploader, MockHttpsUploader
from aibridge.sense_brief.model import SenseBrief


def upload_poster_https(
    brief: SenseBrief,
    *,
    image_poster_model: str,
    storage_credential: str,
    object_key: str,
    uploader: PosterUploadPort | None = None,
    poster_bytes: bytes | None = None,
) -> str:
    """Upload poster bytes; return public HTTPS URL.

    When ``poster_bytes`` is omitted, generate via Present ``generate_poster_bytes``
    (legacy/direct callers). Accept path (STORY-52) supplies bytes from the image port.
    ``uploader`` is injectable for STORY-50 harness / unit tests.
    Aibridge-owned ``storage_credential`` is always required (DP2 fail-closed).
    """
    if not (storage_credential or "").strip():
        raise PosterFailure(
            PosterFailureClass.STORAGE_UPLOAD_FAILED,
            "aibridge storage credential missing",
        )
    data = (
        poster_bytes
        if poster_bytes is not None
        else generate_poster_bytes(brief, image_poster_model=image_poster_model)
    )
    inner: PosterUploadPort = uploader or MockHttpsUploader()
    gated = CredentialGatedUploader(storage_credential, inner)
    return gated.upload(data, content_type="image/png", object_key=object_key)
