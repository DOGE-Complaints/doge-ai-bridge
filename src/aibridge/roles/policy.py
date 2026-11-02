"""Coordinator policy table → exactly one next role (D3). No LLM-router."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from aibridge.roles.registry import (
    DEFAULT_ROLE_REGISTRY,
    ROLE_CHECKER,
    ROLE_COMMUNICATION_SETUP,
    ROLE_EXTRACTOR,
    ROLE_INTERVIEWER,
    ROLE_NORMALIZER,
    RoleRegistry,
    RoleSpec,
)


@dataclass(frozen=True)
class PolicyRow:
    """Thin phase → role mapping (concrete rows Open→Present at implement)."""

    phase: str
    role_id: str
    # Optional flag key that must be truthy to match (None = phase-only).
    require_flag: str | None = None


# Thin v1 rows — phase-driven; flags optional overlays.
DEFAULT_POLICY_ROWS: tuple[PolicyRow, ...] = (
    PolicyRow(phase="setup", role_id=ROLE_COMMUNICATION_SETUP),
    PolicyRow(phase="interviewing", role_id=ROLE_INTERVIEWER),
    PolicyRow(phase="extract", role_id=ROLE_EXTRACTOR),
    PolicyRow(phase="normalize", role_id=ROLE_NORMALIZER),
    PolicyRow(phase="check", role_id=ROLE_CHECKER),
    # Soft overlay: when `needs_check` flag set during interviewing → Checker.
    PolicyRow(
        phase="interviewing",
        role_id=ROLE_CHECKER,
        require_flag="needs_check",
    ),
)


class PolicySelectionError(ValueError):
    """No unique role matched the policy table."""


def select_next_role(
    *,
    phase: str,
    flags: Mapping[str, bool] | None = None,
    rows: tuple[PolicyRow, ...] = DEFAULT_POLICY_ROWS,
    registry: RoleRegistry = DEFAULT_ROLE_REGISTRY,
) -> RoleSpec:
    """Pick exactly one role from the policy table. Forbidden: LLM-as-router."""
    flag_map = dict(flags or {})
    # Prefer flagged rows over phase-only when both match.
    flagged: list[PolicyRow] = []
    plain: list[PolicyRow] = []
    for row in rows:
        if row.phase != phase:
            continue
        if row.require_flag is not None:
            if flag_map.get(row.require_flag):
                flagged.append(row)
        else:
            plain.append(row)

    matched = flagged if flagged else plain
    if len(matched) != 1:
        raise PolicySelectionError(
            f"policy must yield exactly one role for phase={phase!r} "
            f"flags={flag_map!r}; got {len(matched)}"
        )
    return registry.get(matched[0].role_id)
