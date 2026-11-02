"""Semantic state store port — ≠ HistoryStore / ≠ interview.last_confirmed_state."""

from __future__ import annotations

from typing import Protocol

from aibridge.semantic_state.models import SemanticStateSnapshot


class SemanticStateStore(Protocol):
    """App-owned semantic persistence keyed by session_id."""

    def get(self, session_id: str) -> SemanticStateSnapshot:
        """Load snapshot (empty if absent)."""

    def put(self, session_id: str, snapshot: SemanticStateSnapshot) -> None:
        """Replace snapshot for session."""
