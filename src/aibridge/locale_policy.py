"""STORY-69 — unclear-language detector + session locale helpers.

Arch: docs/architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md
Locale SSOT = ConfirmSession.locale ∈ {et,ru,en} — not semantic_state facts.
English pick label uses 🇺🇸 (US). No invent full i18n catalog.
"""

from __future__ import annotations

import re
from typing import Final

SUPPORTED_LOCALES: Final[frozenset[str]] = frozenset({"et", "ru", "en"})

# Product label contract (ChannelAction.label) — EN MUST use US flag.
LANG_PICK_LABELS: Final[dict[str, str]] = {
    "et": "Eesti 🇪🇪",
    "ru": "Русский 🇷🇺",
    "en": "English 🇺🇸",
}

_CYRILLIC = re.compile(r"[\u0400-\u04FF]")
_ET_MARKERS = re.compile(r"[äöüõšžÄÖÜÕŠŽ]")
_LETTER = re.compile(r"[A-Za-z\u0400-\u04FF\u00C0-\u024F]")


def is_supported_locale(value: str | None) -> bool:
    return value is not None and value in SUPPORTED_LOCALES


def is_unclear_language(text: str) -> bool:
    """True when start text cannot reliably identify language (AC-69-01).

    Unclear: empty/whitespace, digits-only (e.g. ``888``), no letters,
    or a short opaque alphanumeric token without spaces.
    ``language_code`` alone must not decide — caller ignores soft TG hint.
    """
    t = (text or "").strip()
    if not t:
        return True
    if t.isdigit():
        return True
    if not _LETTER.search(t):
        return True
    # Opaque short token (e.g. "abc", "x9") — not natural-language start.
    if " " not in t and len(t) <= 4 and t.isascii() and t.isalnum():
        return True
    return False


def infer_locale_from_clear_text(text: str) -> str | None:
    """Soft bind when clear-text skips picker (AC-69-04). Not full i18n."""
    if is_unclear_language(text):
        return None
    if _CYRILLIC.search(text):
        return "ru"
    if _ET_MARKERS.search(text):
        return "et"
    if any(c.isalpha() and c.isascii() for c in text):
        return "en"
    return None


def locale_prompt_prefix(locale: str | None) -> str:
    """Thin Adapt hint for interview turns — not a string catalog."""
    if not is_supported_locale(locale):
        return ""
    return f"[session_locale={locale}] "


def lang_pick_label(locale: str) -> str:
    if locale not in LANG_PICK_LABELS:
        raise ValueError(f"unsupported locale: {locale}")
    return LANG_PICK_LABELS[locale]
