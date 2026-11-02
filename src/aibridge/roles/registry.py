"""Five v1 roles + version pins (AC-AIB-13-02). Bodies = fixtures/export, not aibridge SSOT."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

# Product §6 / REQ-13 — slug ids for code; labels for display.
ROLE_COMMUNICATION_SETUP = "communication_setup"
ROLE_INTERVIEWER = "interviewer"
ROLE_EXTRACTOR = "extractor"
ROLE_NORMALIZER = "normalizer"
ROLE_CHECKER = "checker"

V1_ROLE_IDS: tuple[str, ...] = (
    ROLE_COMMUNICATION_SETUP,
    ROLE_INTERVIEWER,
    ROLE_EXTRACTOR,
    ROLE_NORMALIZER,
    ROLE_CHECKER,
)

_V1_LABELS: dict[str, str] = {
    ROLE_COMMUNICATION_SETUP: "Communication setup",
    ROLE_INTERVIEWER: "Interviewer",
    ROLE_EXTRACTOR: "Extractor",
    ROLE_NORMALIZER: "Normalizer",
    ROLE_CHECKER: "Checker",
}

DEFAULT_ROLE_VERSION = "v1"


@dataclass(frozen=True)
class RoleSpec:
    """Callable role with version pin (pin ≠ GPT-48 body SSOT)."""

    role_id: str
    version: str
    label: str


def _v1_specs() -> tuple[RoleSpec, ...]:
    return tuple(
        RoleSpec(role_id=rid, version=DEFAULT_ROLE_VERSION, label=_V1_LABELS[rid])
        for rid in V1_ROLE_IDS
    )


class RoleRegistry:
    """In-process registry of five v1 roles with version pins."""

    def __init__(self, specs: Iterable[RoleSpec] | None = None) -> None:
        items = tuple(specs) if specs is not None else _v1_specs()
        if len(items) != len({s.role_id for s in items}):
            raise ValueError("duplicate role_id in registry")
        self._by_id: dict[str, RoleSpec] = {s.role_id: s for s in items}

    def list_roles(self) -> tuple[RoleSpec, ...]:
        return tuple(self._by_id[rid] for rid in V1_ROLE_IDS if rid in self._by_id)

    def get(self, role_id: str) -> RoleSpec:
        try:
            return self._by_id[role_id]
        except KeyError as exc:
            raise KeyError(f"unknown role_id: {role_id!r}") from exc

    def require_v1_five(self) -> tuple[RoleSpec, ...]:
        missing = [rid for rid in V1_ROLE_IDS if rid not in self._by_id]
        if missing:
            raise ValueError(f"missing v1 roles: {missing}")
        return self.list_roles()


DEFAULT_ROLE_REGISTRY = RoleRegistry()
