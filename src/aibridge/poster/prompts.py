"""Dedicated poster prompt module (DP7) — not interview/content SSOT.

Implement path (Open in arch; chosen for this wave):
``src/aibridge/poster/prompts/system_en.md``
"""

from __future__ import annotations

from pathlib import Path

_FORBIDDEN_INTERVIEW_MARKERS = (
    "InterviewEngine",
    "dogestonia_instructions",
    "content_bundle",
)


def prompts_dir() -> Path:
    return Path(__file__).resolve().parent / "prompts"


def load_system_instructions_en() -> str:
    path = prompts_dir() / "system_en.md"
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise FileNotFoundError(f"empty poster prompts: {path}")
    return text


def assert_not_interview_ssot(instructions: str | None = None) -> None:
    body = instructions if instructions is not None else load_system_instructions_en()
    lowered = body.lower()
    if "from the brief" not in lowered and "from brief" not in lowered:
        raise AssertionError("poster prompts must require brief-derived input")
    for marker in _FORBIDDEN_INTERVIEW_MARKERS:
        if marker in body:
            raise AssertionError(f"poster prompts must not reference {marker}")


def package_resource_exists() -> bool:
    return (prompts_dir() / "system_en.md").is_file()
