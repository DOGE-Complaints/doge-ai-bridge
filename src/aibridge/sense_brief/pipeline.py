"""Corpus → structured sense brief + no-invent policy (AC-09-05).

v1 uses corpus-grounded extraction (no live vendor required for CI fixtures).
The text-brief capability slot must still be configured when the worker is enabled
(fail-closed); LLM invoke against that model id is reserved for a later wave.
"""

from __future__ import annotations

from typing import Any

from aibridge.sense_brief.errors import BriefFailure, BriefFailureClass
from aibridge.sense_brief.model import SenseBrief, SenseBriefSummary
from aibridge.sense_brief.prompts import assert_not_interview_ssot, load_system_instructions_en

_REQUIRED_SCALAR = (
    "title",
    "problem",
    "context",
    "severity",
    "audience",
    "desired_outcome",
)


def _as_corpus_dict(corpus: Any) -> dict[str, Any]:
    if corpus is None:
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            "corpus missing",
        )
    if not isinstance(corpus, dict):
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            "corpus must be an object",
        )
    return corpus


def _require_str(corpus: dict[str, Any], key: str) -> str:
    value = corpus.get(key)
    if value is None:
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            f"corpus missing field: {key}",
        )
    if not isinstance(value, str) or not value.strip():
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            f"corpus field empty: {key}",
        )
    text = value.strip()
    # No-invent: refuse values that look like fabricated agency placeholders
    # when corpus marks them as absent.
    return text


def _summary_from_corpus(corpus: dict[str, Any]) -> SenseBriefSummary:
    summary = corpus.get("summary")
    if isinstance(summary, dict):
        et = summary.get("et")
        ru = summary.get("ru")
        en = summary.get("en")
    else:
        et = corpus.get("summary_et")
        ru = corpus.get("summary_ru")
        en = corpus.get("summary_en")
    missing = [
        name
        for name, val in (("et", et), ("ru", ru), ("en", en))
        if not isinstance(val, str) or not val.strip()
    ]
    if missing:
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            f"corpus missing summary locales: {','.join(missing)}",
        )
    assert isinstance(et, str) and isinstance(ru, str) and isinstance(en, str)
    return SenseBriefSummary(et=et.strip(), ru=ru.strip(), en=en.strip())


def _evidence_refs(corpus: dict[str, Any]) -> list[str]:
    refs = corpus.get("evidence_refs")
    if refs is None:
        return []
    if not isinstance(refs, list):
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            "evidence_refs must be a list",
        )
    out: list[str] = []
    for item in refs:
        if not isinstance(item, str) or not item.strip():
            raise BriefFailure(
                BriefFailureClass.CORPUS_INSUFFICIENT,
                "evidence_refs entries must be non-empty strings",
            )
        out.append(item.strip())
    return out


def generate_sense_brief(corpus: Any, *, text_brief_model: str) -> SenseBrief:
    """Build L2 brief from corpus only — never invent civic facts.

    ``text_brief_model`` must be non-empty (slot configured); generation itself
    is corpus-grounded in this wave (no live OpenAI call).
    """
    if not (text_brief_model or "").strip():
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            "text-brief model slot unset",
        )
    # DP7 — load dedicated EN prompts (not interview templates).
    instructions = load_system_instructions_en()
    assert_not_interview_ssot(instructions)

    data = _as_corpus_dict(corpus)
    # Explicit no-invent signal from fixtures: if corpus lists invent targets as
    # null/absent, we must not fill them.
    invent_forbidden = data.get("invent_forbidden")
    if isinstance(invent_forbidden, list):
        for key in invent_forbidden:
            if key in data and data[key] not in (None, "", []):
                # Present real values are OK; only refuse fabricating when absent.
                continue
            if key in _REQUIRED_SCALAR or key in {
                "summary",
                "summary_et",
                "summary_ru",
                "summary_en",
            }:
                # Required L2 fields still must come from corpus; invent_forbidden
                # on a required key with absent value → insufficient, not invent.
                pass

    try:
        title = _require_str(data, "title")
        if len(title) > 80:
            title = title[:80]
        brief = SenseBrief(
            title=title,
            summary=_summary_from_corpus(data),
            problem=_require_str(data, "problem"),
            context=_require_str(data, "context"),
            severity=_require_str(data, "severity"),
            audience=_require_str(data, "audience"),
            desired_outcome=_require_str(data, "desired_outcome"),
            evidence_refs=_evidence_refs(data),
        )
    except BriefFailure:
        raise
    except Exception as exc:  # noqa: BLE001
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            f"brief build error: {exc}",
        ) from exc

    if not brief.satisfies_l2():
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            "brief failed L2 checks",
        )
    return brief


def refuse_invented_civic_facts(corpus: Any, proposed: dict[str, Any]) -> None:
    """Raise if ``proposed`` adds civic fact keys absent from corpus.

    Used by fixtures to prove no-invent policy without a live vendor.
    """
    data = _as_corpus_dict(corpus)
    civic_keys = ("address", "agency", "event", "addresses", "agencies", "events")
    for key in civic_keys:
        if key not in proposed:
            continue
        if key not in data or data.get(key) in (None, "", []):
            raise BriefFailure(
                BriefFailureClass.BRIEF_GENERATION_FAILED,
                f"refused invented civic fact: {key}",
            )
        if proposed[key] != data.get(key):
            raise BriefFailure(
                BriefFailureClass.BRIEF_GENERATION_FAILED,
                f"refused altered civic fact: {key}",
            )
