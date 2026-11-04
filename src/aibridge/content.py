"""Local instruction/content bundle load, hash, and source-commit pin.

No GitHub / network fetch at request time (AIB-INS-04 / AC #4).

STORY-66: live SSOT = roles-schema (`bundle_version`/`core`/`roles.*`).
Phase-A `files[]` remains legacy/dev-only after cutover.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

ManifestSchema = Literal["roles", "phase_a"]


class ContentLoadError(ValueError):
    """Invalid or missing content artifacts."""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_text(raw: bytes) -> str:
    """UTF-8 decode and normalize newlines to LF."""
    text = raw.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n")


STABLE_SEPARATOR = "\n\n"


@dataclass(frozen=True)
class LoadedContentBundle:
    """Verified local content for one deployment."""

    bundle_version: str
    source_commit: str
    instructions_hash: str
    wire_oas_hash: str
    pack_hash: str
    tool_schema_hash: str
    bundle_hash: str
    assembled_instructions: str
    file_hashes: tuple[tuple[str, str], ...]
    components: dict[str, Any]


def _reject_path(name: str) -> None:
    if not name or name.strip() != name:
        raise ContentLoadError(f"Invalid manifest path: {name!r}")
    if name in {".", ".."} or "/" in name or "\\" in name:
        raise ContentLoadError(f"Manifest path must be a root child: {name!r}")
    if Path(name).is_absolute():
        raise ContentLoadError(f"Absolute manifest paths forbidden: {name!r}")


def classify_manifest(data: dict[str, Any]) -> ManifestSchema:
    """Return roles-schema or Phase-A; refuse dual schema on one manifest."""
    has_roles = isinstance(data.get("core"), str) and isinstance(data.get("roles"), dict)
    has_files = isinstance(data.get("files"), list)
    if has_roles and has_files:
        raise ContentLoadError(
            "manifest dual schema forbidden: both files[] and roles.* present"
        )
    if has_roles:
        return "roles"
    if has_files:
        return "phase_a"
    raise ContentLoadError(
        "manifest must be roles-schema (core/roles.*) or Phase-A files[]"
    )


def peek_manifest_schema(manifest_path: Path) -> ManifestSchema:
    """Classify manifest on disk (STORY-66 env unify)."""
    if not manifest_path.is_file():
        raise ContentLoadError(f"Manifest missing: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContentLoadError(f"Manifest JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise ContentLoadError("Manifest must be a JSON object")
    return classify_manifest(data)


def _validate_roles_schema(data: dict[str, Any]) -> None:
    version = data.get("bundle_version")
    core = data.get("core")
    roles = data.get("roles")
    if not isinstance(version, str) or not version:
        raise ContentLoadError("roles.manifest.bundle_version required")
    if not isinstance(core, str) or not core:
        raise ContentLoadError("roles.manifest.core required")
    _reject_path(core)
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
        _reject_path(fname)
        if not isinstance(ver, str) or not ver:
            raise ContentLoadError(f"roles.manifest.roles[{rid!r}].version required")


def _validate_phase_a(data: dict[str, Any]) -> None:
    version = data.get("bundle_version")
    files = data.get("files")
    if not isinstance(version, str) or not version:
        raise ContentLoadError("manifest.bundle_version required")
    if not isinstance(files, list) or not files:
        raise ContentLoadError("manifest.files must be a non-empty list")
    if len(files) != len(set(files)):
        raise ContentLoadError("manifest.files contains duplicates")
    for name in files:
        if not isinstance(name, str):
            raise ContentLoadError("manifest.files entries must be strings")
        _reject_path(name)


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.is_file():
        raise ContentLoadError(f"Manifest missing: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContentLoadError(f"Manifest JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise ContentLoadError("Manifest must be a JSON object")
    schema = classify_manifest(data)
    if schema == "roles":
        _validate_roles_schema(data)
    else:
        _validate_phase_a(data)
    return data


def _read_instruction_file(instructions_dir: Path, name: str) -> tuple[str, str]:
    path = instructions_dir / name
    if not path.is_file():
        raise ContentLoadError(f"Instruction file missing: {path}")
    raw = path.read_bytes()
    if not raw:
        raise ContentLoadError(f"Instruction file empty: {path}")
    text = normalize_text(raw)
    return text, sha256_hex(text.encode("utf-8"))


def _roles_file_list(manifest: dict[str, Any]) -> list[str]:
    """Ordered unique root children: core then role files (stable sort by role id)."""
    core = str(manifest["core"])
    roles: dict[str, Any] = dict(manifest["roles"])
    names = [core]
    for rid in sorted(roles.keys()):
        fname = str(roles[rid]["file"])
        if fname not in names:
            names.append(fname)
    return names


def load_content_bundle(
    *,
    instructions_dir: Path,
    manifest_path: Path,
    source_commit: str,
    wire_oas_path: Path,
    pack_schema_path: Path,
    tool_schema_path: Path | None = None,
) -> LoadedContentBundle:
    """Load local roots; hash; pin source commit. Local FS only.

    Roles-schema (live): hashes core + all role files; assembled = core text
    (per-role assembly on channel turns — STORY-65/66). Phase-A `files[]`
    remains legacy/dev Join of listed files.
    """
    if not source_commit or not source_commit.strip():
        raise ContentLoadError("DOGESTONIA_CONTENT_SOURCE_COMMIT required")
    source_commit = source_commit.strip()

    if not instructions_dir.is_dir():
        raise ContentLoadError(f"Instructions dir missing: {instructions_dir}")

    manifest = load_manifest(manifest_path)
    schema = classify_manifest(manifest)
    bundle_version = str(manifest["bundle_version"])

    file_hashes: list[tuple[str, str]] = []
    if schema == "roles":
        names = _roles_file_list(manifest)
        texts: dict[str, str] = {}
        for name in names:
            text, digest = _read_instruction_file(instructions_dir, name)
            texts[name] = text
            file_hashes.append((name, digest))
        # ADR-1 readiness prefix = core only; channel assemble overrides per turn.
        assembled = texts[str(manifest["core"])]
        schema_label = "roles"
        files_component: list[dict[str, Any]] = [
            {"name": n, "sha256": h} for n, h in file_hashes
        ]
        roles_meta = {
            rid: {"file": entry["file"], "version": entry["version"]}
            for rid, entry in dict(manifest["roles"]).items()
        }
    else:
        files: list[str] = list(manifest["files"])
        parts: list[str] = []
        for name in files:
            text, digest = _read_instruction_file(instructions_dir, name)
            file_hashes.append((name, digest))
            parts.append(text)
        assembled = STABLE_SEPARATOR.join(parts)
        schema_label = "phase_a"
        files_component = [{"name": n, "sha256": h} for n, h in file_hashes]
        roles_meta = None

    instructions_hash = sha256_hex(assembled.encode("utf-8"))

    if not wire_oas_path.is_file():
        raise ContentLoadError(f"Wire OAS missing: {wire_oas_path}")
    wire_oas_hash = sha256_hex(wire_oas_path.read_bytes())

    if not pack_schema_path.is_file():
        raise ContentLoadError(f"Pack schema missing: {pack_schema_path}")
    pack_hash = sha256_hex(pack_schema_path.read_bytes())

    if tool_schema_path is not None:
        if not tool_schema_path.is_file():
            raise ContentLoadError(f"Tool schema missing: {tool_schema_path}")
        tool_schema_hash = sha256_hex(tool_schema_path.read_bytes())
    else:
        tool_schema_hash = sha256_hex(b"")

    components: dict[str, Any] = {
        "bundle_version": bundle_version,
        "source_commit": source_commit,
        "schema": schema_label,
        "files": files_component,
        "instructions_hash": instructions_hash,
        "wire_oas_hash": wire_oas_hash,
        "pack_hash": pack_hash,
        "tool_schema_hash": tool_schema_hash,
    }
    if roles_meta is not None:
        components["core"] = str(manifest["core"])
        components["roles"] = roles_meta
    canonical = json.dumps(components, sort_keys=True, separators=(",", ":"))
    bundle_hash = sha256_hex(canonical.encode("utf-8"))

    return LoadedContentBundle(
        bundle_version=bundle_version,
        source_commit=source_commit,
        instructions_hash=instructions_hash,
        wire_oas_hash=wire_oas_hash,
        pack_hash=pack_hash,
        tool_schema_hash=tool_schema_hash,
        bundle_hash=bundle_hash,
        assembled_instructions=assembled,
        file_hashes=tuple(file_hashes),
        components=components,
    )
