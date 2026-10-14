"""Civic poster bytes from sense brief (AC-09-03) — not interview templates.

v1 builds a deterministic minimal PNG embedding brief title/summary markers.
Live image-vendor invoke against the image-poster slot is reserved for later;
the slot must still be configured when the worker is enabled (fail-closed).
"""

from __future__ import annotations

import hashlib
import struct
import zlib

from aibridge.poster.errors import PosterFailure, PosterFailureClass
from aibridge.poster.prompts import assert_not_interview_ssot, load_system_instructions_en
from aibridge.sense_brief.model import SenseBrief

# Minimal 1×1 PNG IHDR+IDAT+IEND scaffolding.
_PNG_SIG = b"\x89PNG\r\n\x1a\n"


def _chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def _minimal_png_with_text(label: str) -> bytes:
    """Valid tiny PNG with a tEXt chunk carrying brief-derived label."""
    ihdr = _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    # Single RGB pixel (civic slate).
    raw = zlib.compress(b"\x00\x2f\x4f\x6a")
    idat = _chunk(b"IDAT", raw)
    text_payload = b"Brief\x00" + label.encode("utf-8", errors="replace")[:200]
    text = _chunk(b"tEXt", text_payload)
    iend = _chunk(b"IEND", b"")
    return _PNG_SIG + ihdr + text + idat + iend


def generate_poster_bytes(brief: SenseBrief, *, image_poster_model: str) -> bytes:
    """Derive civic poster image bytes from brief only.

    ``image_poster_model`` must be non-empty (slot configured).
    """
    if not (image_poster_model or "").strip():
        raise PosterFailure(
            PosterFailureClass.IMAGE_GENERATION_FAILED,
            "image-poster model slot unset",
        )
    instructions = load_system_instructions_en()
    assert_not_interview_ssot(instructions)

    if not brief.satisfies_l2():
        raise PosterFailure(
            PosterFailureClass.IMAGE_GENERATION_FAILED,
            "brief failed L2 checks for poster",
        )
    try:
        digest = hashlib.sha256(
            f"{brief.title}|{brief.summary.en}|{image_poster_model}".encode("utf-8")
        ).hexdigest()[:16]
        label = f"{brief.title}|{digest}"
        data = _minimal_png_with_text(label)
    except PosterFailure:
        raise
    except Exception as exc:  # noqa: BLE001
        raise PosterFailure(
            PosterFailureClass.IMAGE_GENERATION_FAILED,
            f"poster build error: {exc}",
        ) from exc
    if not data.startswith(_PNG_SIG):
        raise PosterFailure(
            PosterFailureClass.IMAGE_GENERATION_FAILED,
            "poster bytes invalid",
        )
    # Prove brief-derived (title bytes appear in PNG text chunk).
    if brief.title.encode("utf-8") not in data:
        raise PosterFailure(
            PosterFailureClass.IMAGE_GENERATION_FAILED,
            "poster missing brief title marker",
        )
    return data
