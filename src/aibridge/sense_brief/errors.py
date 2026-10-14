"""Brief failure classes (arch DP9). Wire strings = implement choice (Open in arch)."""

from __future__ import annotations

from enum import Enum


class BriefFailureClass(str, Enum):
    """Logical classes — values are implement wire strings for this wave."""

    CORPUS_INSUFFICIENT = "corpus_insufficient"
    BRIEF_GENERATION_FAILED = "brief_generation_failed"


class BriefFailure(Exception):
    def __init__(self, failure_class: BriefFailureClass, message: str = "") -> None:
        self.failure_class = failure_class
        self.message = message or failure_class.value
        super().__init__(self.message)
