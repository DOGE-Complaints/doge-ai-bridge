"""Local instruction/content bundle load, hash, and source-commit pin.

No GitHub / network fetch at request time (AIB-INS-04 / AC #4).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.is_file():
        raise ContentLoadError(f"Manifest missing: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContentLoadError(f"Manifest JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise ContentLoadError("Manifest must be a JSON object")
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
    return data


def load_content_bundle(
    *,
    instructions_dir: Path,
    manifest_path: Path,
    source_commit: str,
    wire_oas_path: Path,
    pack_schema_path: Path,
    tool_schema_path: Path | None = None,
) -> LoadedContentBundle:
    """Load manifest-listed local roots; hash; pin source commit. Local FS only."""
    if not source_commit or not source_commit.strip():
        raise ContentLoadError("DOGESTONIA_CONTENT_SOURCE_COMMIT required")
    source_commit = source_commit.strip()

    if not instructions_dir.is_dir():
        raise ContentLoadError(f"Instructions dir missing: {instructions_dir}")

    manifest = load_manifest(manifest_path)
    bundle_version = str(manifest["bundle_version"])
    files: list[str] = list(manifest["files"])

    parts: list[str] = []
    file_hashes: list[tuple[str, str]] = []
    for name in files:
        path = instructions_dir / name
        if not path.is_file():
            raise ContentLoadError(f"Instruction file missing: {path}")
        raw = path.read_bytes()
        if not raw:
            raise ContentLoadError(f"Instruction file empty: {path}")
        text = normalize_text(raw)
        file_hashes.append((name, sha256_hex(text.encode("utf-8"))))
        parts.append(text)

    assembled = STABLE_SEPARATOR.join(parts)
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
        # Story 03 generates tools; pin empty canonical until then.
        tool_schema_hash = sha256_hex(b"")

    components: dict[str, Any] = {
        "bundle_version": bundle_version,
        "source_commit": source_commit,
        "files": [{"name": n, "sha256": h} for n, h in file_hashes],
        "instructions_hash": instructions_hash,
        "wire_oas_hash": wire_oas_hash,
        "pack_hash": pack_hash,
        "tool_schema_hash": tool_schema_hash,
    }
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
