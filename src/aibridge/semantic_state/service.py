"""Semantic writes + L13-3 Target A meaning → invalidate_send_permission."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import TYPE_CHECKING

from aibridge.semantic_state.models import GroundedText, SemanticStateSnapshot
from aibridge.semantic_state.ports import SemanticStateStore

if TYPE_CHECKING:
    from aibridge.confirm import ConfirmationGuard

MeaningInvalidator = Callable[[str, str], None]


def _new_id() -> str:
    """Opaque record id (uuid4). Not a hash-format SSOT."""
    return str(uuid.uuid4())


class SemanticStateService:
    """App-validated semantic mutations.

    Confirmed facts / corrections / phase-with-rights → invalidate send (Target A).
    Draft hypotheses / gaps alone do **not** auto-invalidate.
    """

    def __init__(
        self,
        store: SemanticStateStore,
        *,
        on_meaning_change: MeaningInvalidator | None = None,
        confirm_guard: ConfirmationGuard | None = None,
    ) -> None:
        self._store = store
        if on_meaning_change is not None:
            self._on_meaning = on_meaning_change
        elif confirm_guard is not None:
            guard = confirm_guard

            def _via_guard(session_id: str, reason: str) -> None:
                guard.invalidate_send_permission(session_id, reason=reason)

            self._on_meaning = _via_guard
        else:
            self._on_meaning = None

    def get(self, session_id: str) -> SemanticStateSnapshot:
        return self._store.get(session_id)

    def set_phase(
        self,
        session_id: str,
        phase: str | None,
        *,
        changes_role_rights: bool = False,
    ) -> SemanticStateSnapshot:
        snap = self._store.get(session_id)
        snap.phase = phase
        self._store.put(session_id, snap)
        if changes_role_rights:
            self._invalidate(session_id, "phase_rights_change")
        return self._store.get(session_id)

    def upsert_confirmed_fact(
        self,
        session_id: str,
        text: str,
        *,
        fact_id: str | None = None,
        ground_utterance_refs: tuple[str, ...] = (),
    ) -> SemanticStateSnapshot:
        snap = self._store.get(session_id)
        fid = fact_id or _new_id()
        replaced = False
        for i, fact in enumerate(snap.facts):
            if fact.id == fid:
                snap.facts[i] = GroundedText(
                    id=fid,
                    text=text,
                    ground_utterance_refs=ground_utterance_refs,
                )
                replaced = True
                break
        if not replaced:
            snap.facts.append(
                GroundedText(
                    id=fid,
                    text=text,
                    ground_utterance_refs=ground_utterance_refs,
                )
            )
        self._store.put(session_id, snap)
        self._invalidate(session_id, "confirmed_fact")
        return self._store.get(session_id)

    def add_correction(
        self,
        session_id: str,
        text: str,
        *,
        correction_id: str | None = None,
        ground_utterance_refs: tuple[str, ...] = (),
    ) -> SemanticStateSnapshot:
        snap = self._store.get(session_id)
        cid = correction_id or _new_id()
        snap.corrections.append(
            GroundedText(
                id=cid,
                text=text,
                ground_utterance_refs=ground_utterance_refs,
            )
        )
        self._store.put(session_id, snap)
        self._invalidate(session_id, "correction")
        return self._store.get(session_id)

    def add_hypothesis(
        self,
        session_id: str,
        text: str,
        *,
        hypothesis_id: str | None = None,
        ground_utterance_refs: tuple[str, ...] = (),
    ) -> SemanticStateSnapshot:
        snap = self._store.get(session_id)
        hid = hypothesis_id or _new_id()
        snap.hypotheses.append(
            GroundedText(
                id=hid,
                text=text,
                ground_utterance_refs=ground_utterance_refs,
            )
        )
        self._store.put(session_id, snap)
        # Draft only — no invalidate.
        return self._store.get(session_id)

    def add_gap(
        self,
        session_id: str,
        text: str,
        *,
        gap_id: str | None = None,
        ground_utterance_refs: tuple[str, ...] = (),
    ) -> SemanticStateSnapshot:
        snap = self._store.get(session_id)
        gid = gap_id or _new_id()
        snap.gaps.append(
            GroundedText(
                id=gid,
                text=text,
                ground_utterance_refs=ground_utterance_refs,
            )
        )
        self._store.put(session_id, snap)
        # Draft only — no invalidate.
        return self._store.get(session_id)

    def _invalidate(self, session_id: str, reason: str) -> None:
        if self._on_meaning is not None:
            self._on_meaning(session_id, reason)
