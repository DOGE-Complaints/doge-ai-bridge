"""Dedicated worker prompt module (DP7) — not interview/content SSOT.

Implement path (Open in arch; chosen for this wave):
``src/aibridge/sense_brief/prompts/system_en.md``
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

# Marker strings that must NOT appear as civic SSOT sources.
_FORBIDDEN_INTERVIEW_MARKERS = (
    "InterviewEngine",
    "dogestonia_instructions",
    "content_bundle",
)


def prompts_dir() -> Path:
    return Path(__file__).resolve().parent / "prompts"


def load_system_instructions_en() -> str:
    """Load EN system instructions shipped with the worker image."""
    path = prompts_dir() / "system_en.md"
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise FileNotFoundError(f"empty sense-brief prompts: {path}")
    return text


def assert_not_interview_ssot(instructions: str | None = None) -> None:
    """Ensure loaded prompts do not pull interview/content templates as SSOT."""
    body = instructions if instructions is not None else load_system_instructions_en()
    lowered = body.lower()
    # Explicit policy line must be present (EN).
    if "do not invent" not in lowered and "not invent" not in lowered:
        raise AssertionError("sense-brief prompts missing no-invent policy")
    for marker in _FORBIDDEN_INTERVIEW_MARKERS:
        # Allow mentioning "Telegram interview" only as a prohibition.
        if marker == "Telegram interview":
            continue
        if marker in body:
            raise AssertionError(f"sense-brief prompts must not reference {marker}")


def package_resource_exists() -> bool:
    """True when prompts package data is importable beside this module."""
    return (prompts_dir() / "system_en.md").is_file()
