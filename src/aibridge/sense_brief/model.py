"""Logical L2 sense-brief model (AC-09-02).

Implement JSON keys (Open in arch; chosen for this wave — not gateway SSOT freeze):
``title``, ``summary``{``et``,``ru``,``en``}, ``problem``, ``context``,
``severity``, ``audience``, ``desired_outcome``, ``evidence_refs``.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SenseBriefSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    et: str = Field(min_length=1)
    ru: str = Field(min_length=1)
    en: str = Field(min_length=1)


class SenseBrief(BaseModel):
    """Structured sense brief — logical L2 outcomes."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=80)
    summary: SenseBriefSummary
    problem: str = Field(min_length=1)
    context: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    audience: str = Field(min_length=1)
    desired_outcome: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)

    @field_validator("title", mode="before")
    @classmethod
    def _strip_title(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    def satisfies_l2(self) -> bool:
        """AC-09-02: title ≤80 + summary et/ru/en present."""
        return (
            bool(self.title)
            and len(self.title) <= 80
            and bool(self.summary.et)
            and bool(self.summary.ru)
            and bool(self.summary.en)
        )
