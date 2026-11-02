"""Role instruction assembly from configured dir + manifest (AC-AIB-13-03 / D5).

Shared core + per-role slice + session pin. Reads only via paths given by caller
(typically DOGESTONIA_INSTRUCTIONS_DIR + MANIFEST). OOS live volume (STORY-64).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aibridge.content import ContentLoadError, normalize_text, sha256_hex
from aibridge.roles.registry import (
    DEFAULT_ROLE_REGISTRY,
    V1_ROLE_IDS,
    RoleRegistry,
    RoleSpec,
)

STABLE_SEPARATOR = "\n\n"


@dataclass(frozen=True)
class AssembledRolePrompt:
    """Assembled core+role text with session pin (no mid-flight silent swap)."""

    role: RoleSpec
    core_text: str
    role_text: str
    assembled: str
    session_pin: str
    node_id: str | None
    manifest_version: str


def _reject_root_child(name: str) -> None:
    if not name or name.strip() != name:
        raise ContentLoadError(f"Invalid manifest path: {name!r}")
    if name in {".", ".."} or "/" in name or "\\" in name:
        raise ContentLoadError(f"Manifest path must be a root child: {name!r}")
    if Path(name).is_absolute():
        raise ContentLoadError(f"Absolute manifest paths forbidden: {name!r}")


def load_roles_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.is_file():
        raise ContentLoadError(f"Roles manifest missing: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContentLoadError(f"Roles manifest JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise ContentLoadError("Roles manifest must be a JSON object")
    version = data.get("bundle_version")
    core = data.get("core")
    roles = data.get("roles")
    if not isinstance(version, str) or not version:
        raise ContentLoadError("roles.manifest.bundle_version required")
    if not isinstance(core, str) or not core:
        raise ContentLoadError("roles.manifest.core required")
    _reject_root_child(core)
    if not isinstance(roles, dict) or not roles:
        raise ContentLoadError("roles.manifest.roles must be a non-empty object")
    for rid, entry in roles.items():
        if not isinstance(rid, str) or not rid:
            raise ContentLoadError("roles.manifest.roles keys must be strings")
        if not isinstance(entry, dict):
            raise ContentLoadError(f"roles.manifest.roles[{rid!r}] must be object")
        fname = entry.get("file")
        ver = entry.get("version")
        if not isinstance(fname, str) or not fname:
            raise ContentLoadError(f"roles.manifest.roles[{rid!r}].file required")
        _reject_root_child(fname)
        if not isinstance(ver, str) or not ver:
            raise ContentLoadError(f"roles.manifest.roles[{rid!r}].version required")
    return data


def _read_instruction_file(instructions_dir: Path, name: str) -> str:
    path = instructions_dir / name
    if not path.is_file():
        raise ContentLoadError(f"Instruction file missing: {path}")
    raw = path.read_bytes()
    if not raw:
        raise ContentLoadError(f"Instruction file empty: {path}")
    return normalize_text(raw)


def session_pin_hex(
    *,
    core_text: str,
    role_text: str,
    role_id: str,
    role_version: str,
    node_id: str | None,
) -> str:
    """Hash/pin of core+role(+node) at conversation start."""
    payload = {
        "core": core_text,
        "role": role_text,
        "role_id": role_id,
        "role_version": role_version,
        "node_id": node_id or "",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256_hex(canonical.encode("utf-8"))


def assemble_role_prompt(
    *,
    instructions_dir: Path,
    manifest_path: Path,
    role_id: str,
    node_id: str | None = None,
    registry: RoleRegistry = DEFAULT_ROLE_REGISTRY,
) -> AssembledRolePrompt:
    """Assemble shared core + per-role slice; pin session. Dir+manifest only."""
    if not instructions_dir.is_dir():
        raise ContentLoadError(f"Instructions dir missing: {instructions_dir}")
    manifest = load_roles_manifest(manifest_path)
    roles_map: dict[str, Any] = dict(manifest["roles"])
    if role_id not in roles_map:
        raise ContentLoadError(f"Role {role_id!r} absent from roles manifest")
    entry = roles_map[role_id]
    file_name = str(entry["file"])
    pin_version = str(entry["version"])
    base = registry.get(role_id)
    role = RoleSpec(role_id=base.role_id, version=pin_version, label=base.label)

    core_text = _read_instruction_file(instructions_dir, str(manifest["core"]))
    role_text = _read_instruction_file(instructions_dir, file_name)
    assembled = STABLE_SEPARATOR.join((core_text, role_text))
    pin = session_pin_hex(
        core_text=core_text,
        role_text=role_text,
        role_id=role.role_id,
        role_version=role.version,
        node_id=node_id,
    )
    return AssembledRolePrompt(
        role=role,
        core_text=core_text,
        role_text=role_text,
        assembled=assembled,
        session_pin=pin,
        node_id=node_id,
        manifest_version=str(manifest["bundle_version"]),
    )


def assert_manifest_covers_v1(manifest_path: Path) -> None:
    """Harness helper — all five v1 role ids present in manifest."""
    data = load_roles_manifest(manifest_path)
    roles = set(data["roles"])
    missing = [rid for rid in V1_ROLE_IDS if rid not in roles]
    if missing:
        raise ContentLoadError(f"roles manifest missing v1 roles: {missing}")
