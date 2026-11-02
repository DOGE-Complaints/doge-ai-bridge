"""Logical semantic-state classes (REQ-13 / arch 01) — not HistoryStore items."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GroundedText:
    """Text with optional utterance refs into history (cite, do not replace history)."""

    id: str
    text: str
    ground_utterance_refs: tuple[str, ...] = ()


@dataclass
class SemanticStateSnapshot:
    """Per-session semantic payload. Confirmed facts/corrections ≠ draft hypotheses/gaps."""

    phase: str | None = None
    facts: list[GroundedText] = field(default_factory=list)
    hypotheses: list[GroundedText] = field(default_factory=list)
    gaps: list[GroundedText] = field(default_factory=list)
    corrections: list[GroundedText] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        def _rows(items: list[GroundedText]) -> list[dict[str, Any]]:
            return [
                {
                    "id": i.id,
                    "text": i.text,
                    "ground_utterance_refs": list(i.ground_utterance_refs),
                }
                for i in items
            ]

        return {
            "phase": self.phase,
            "facts": _rows(self.facts),
            "hypotheses": _rows(self.hypotheses),
            "gaps": _rows(self.gaps),
            "corrections": _rows(self.corrections),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SemanticStateSnapshot:
        if not data:
            return cls()

        def _parse(key: str) -> list[GroundedText]:
            out: list[GroundedText] = []
            for raw in data.get(key) or []:
                if not isinstance(raw, dict):
                    continue
                refs = raw.get("ground_utterance_refs") or []
                out.append(
                    GroundedText(
                        id=str(raw["id"]),
                        text=str(raw["text"]),
                        ground_utterance_refs=tuple(str(r) for r in refs),
                    )
                )
            return out

        phase = data.get("phase")
        return cls(
            phase=str(phase) if phase is not None else None,
            facts=_parse("facts"),
            hypotheses=_parse("hypotheses"),
            gaps=_parse("gaps"),
            corrections=_parse("corrections"),
        )
