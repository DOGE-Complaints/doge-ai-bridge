"""STORY-65/66 — bind semantic state + roles into channel turns (lift G-02).

No new HTTP surface. Keep InterviewEngine / dual-confirm.
STORY-66: when roles-schema paths Present (ROLES_* or INSTRUCTIONS_* cutover),
assemble per turn; ADR-1 mega-string is legacy/dev-only under cutover.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aibridge.roles.assembly import assemble_role_prompt
from aibridge.roles.policy import select_next_role
from aibridge.semantic_state.service import SemanticStateService


@dataclass
class ChannelWireContext:
    """Per-app wire: semantic service + optional roles dir/manifest for assembly."""

    semantic: SemanticStateService
    roles_instructions_dir: Path | None = None
    roles_manifest_path: Path | None = None
    # Last evidence for harness (single-threaded TestClient).
    last_evidence: dict[str, Any] = field(default_factory=dict)


def apply_before_engine_turn(
    ctx: ChannelWireContext | None,
    *,
    session_id: str,
    engine: Any,
) -> dict[str, Any]:
    """Invoke select_next_role (+ assemble when roles paths Present) and semantic get.

    When roles dir/manifest absent: selection still runs; keep existing
    ``engine.instructions`` (ADR-1 mega-string — legacy/dev-only after cutover).
    """
    evidence: dict[str, Any] = {
        "wired": False,
        "role_id": None,
        "assembled": False,
        "cutover": False,
        "semantic_get": False,
        "phase": None,
        "session_pin": None,
    }
    if ctx is None:
        return evidence

    evidence["wired"] = True
    snap = ctx.semantic.get(session_id)
    evidence["semantic_get"] = True
    phase = snap.phase or "interviewing"
    if snap.phase is None:
        ctx.semantic.set_phase(session_id, phase, changes_role_rights=False)
    evidence["phase"] = phase

    role = select_next_role(phase=phase)
    evidence["role_id"] = role.role_id

    roles_dir = ctx.roles_instructions_dir
    roles_man = ctx.roles_manifest_path
    if (
        roles_dir is not None
        and roles_man is not None
        and roles_dir.is_dir()
        and roles_man.is_file()
    ):
        prompt = assemble_role_prompt(
            instructions_dir=roles_dir,
            manifest_path=roles_man,
            role_id=role.role_id,
        )
        engine.instructions = prompt.assembled
        evidence["assembled"] = True
        evidence["cutover"] = True
        evidence["session_pin"] = prompt.session_pin

    ctx.last_evidence = dict(evidence)
    return evidence
