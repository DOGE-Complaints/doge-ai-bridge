"""In-memory semantic store for harness (no GPT UI)."""

from __future__ import annotations

from aibridge.semantic_state.models import SemanticStateSnapshot


class MemorySemanticStateStore:
    """Process-local store — not HistoryStore / not last_confirmed_state."""

    def __init__(self) -> None:
        self._by_session: dict[str, SemanticStateSnapshot] = {}

    def get(self, session_id: str) -> SemanticStateSnapshot:
        snap = self._by_session.get(session_id)
        if snap is None:
            return SemanticStateSnapshot()
        # Return a shallow copy of lists so callers cannot mutate store silently.
        return SemanticStateSnapshot.from_dict(snap.to_dict())

    def put(self, session_id: str, snapshot: SemanticStateSnapshot) -> None:
        self._by_session[session_id] = SemanticStateSnapshot.from_dict(
            snapshot.to_dict()
        )
