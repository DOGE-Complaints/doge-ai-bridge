"""GPT E1 consume parity — mounted inventory vs locked export artifact.

STORY-67 / AC-AIB-13-05 code side. Wire format = GPT E1 only
(roles-schema root children + SHA-256 after normalize_text). Do not invent
alternate hash schemes. session_pin / assembled core+role ≠ this inventory.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from aibridge.content import (
    ContentLoadError,
    classify_manifest,
    load_manifest,
    normalize_text,
    roles_file_list,
    sha256_hex,
)

WIRE_E1 = "e1"
HASH_METHOD_E1 = "normalize_text+sha256_hex"


class ExportParityError(ValueError):
    """Invalid export inventory artifact or compare inputs."""


ParityDisposition = Literal[
    "pass",
    "missing",
    "changed",
    "unexpected",
    "bad_inventory",
    "manifest_drift",
]


@dataclass(frozen=True)
class ExportInventory:
    """Locked export artifact (GPT E1 semantics)."""

    wire: str
    bundle_version: str
    hash_method: str
    files: dict[str, str]


@dataclass(frozen=True)
class ParityFinding:
    name: str
    disposition: ParityDisposition
    expected_hash: str | None = None
    actual_hash: str | None = None
    detail: str = ""


@dataclass(frozen=True)
class ParityResult:
    ok: bool
    reason: str | None = None
    findings: tuple[ParityFinding, ...] = field(default_factory=tuple)

    @property
    def ready_reason(self) -> str:
        """Stable /readyz reason token."""
        if self.ok:
            return "export_parity_ok"
        return self.reason or "export_parity_mismatch"


def _hash_file_text(path: Path) -> str:
    if not path.is_file():
        raise ContentLoadError(f"Parity file missing: {path}")
    raw = path.read_bytes()
    if not raw:
        raise ContentLoadError(f"Parity file empty: {path}")
    text = normalize_text(raw)
    return sha256_hex(text.encode("utf-8"))


def load_export_inventory(path: Path) -> ExportInventory:
    """Load locked E1 export inventory JSON artifact."""
    if not path.is_file():
        raise ExportParityError(f"export inventory missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExportParityError(f"export inventory JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise ExportParityError("export inventory must be a JSON object")

    wire = data.get("wire")
    if wire != WIRE_E1:
        raise ExportParityError(
            f"export inventory wire must be {WIRE_E1!r} (GPT E1); got {wire!r}"
        )
    hash_method = data.get("hash_method")
    if hash_method != HASH_METHOD_E1:
        raise ExportParityError(
            f"export inventory hash_method must be {HASH_METHOD_E1!r}; got {hash_method!r}"
        )
    bundle_version = data.get("bundle_version")
    if not isinstance(bundle_version, str) or not bundle_version:
        raise ExportParityError("export inventory bundle_version required")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise ExportParityError("export inventory files must be a non-empty object")
    out: dict[str, str] = {}
    for name, digest in files.items():
        if not isinstance(name, str) or not name or "/" in name or "\\" in name:
            raise ExportParityError(f"invalid inventory file key: {name!r}")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ExportParityError(f"invalid sha256 for {name!r}")
        out[name] = digest.lower()
    return ExportInventory(
        wire=WIRE_E1,
        bundle_version=bundle_version,
        hash_method=HASH_METHOD_E1,
        files=out,
    )


def build_mounted_inventory(
    *,
    instructions_dir: Path,
    manifest_path: Path,
) -> tuple[str, dict[str, str]]:
    """Build E1-shaped inventory from mounted dir + manifest (roles-schema).

    Returns (bundle_version, files→sha256). Includes manifest basename hash.
    Phase-A mounts are rejected — consume parity is roles-schema / E1 only.
    """
    manifest = load_manifest(manifest_path)
    schema = classify_manifest(manifest)
    if schema != "roles":
        raise ExportParityError(
            "export parity requires roles-schema mount (Phase-A files[] not E1 inventory)"
        )
    bundle_version = str(manifest["bundle_version"])
    files: dict[str, str] = {}
    man_key = manifest_path.name
    files[man_key] = _hash_file_text(manifest_path)
    for name in roles_file_list(manifest):
        files[name] = _hash_file_text(instructions_dir / name)
    return bundle_version, files


def compare_inventories(
    *,
    expected: ExportInventory,
    mounted_bundle_version: str,
    mounted_files: dict[str, str],
) -> ParityResult:
    """Diagnose missing / changed / unexpected vs export artifact + manifest drift."""
    findings: list[ParityFinding] = []

    if mounted_bundle_version != expected.bundle_version:
        findings.append(
            ParityFinding(
                name="bundle_version",
                disposition="manifest_drift",
                expected_hash=None,
                actual_hash=None,
                detail=(
                    f"expected {expected.bundle_version!r} "
                    f"got {mounted_bundle_version!r}"
                ),
            )
        )

    for name, exp_hash in sorted(expected.files.items()):
        actual = mounted_files.get(name)
        if actual is None:
            findings.append(
                ParityFinding(
                    name=name,
                    disposition="missing",
                    expected_hash=exp_hash,
                    actual_hash=None,
                )
            )
        elif actual != exp_hash:
            findings.append(
                ParityFinding(
                    name=name,
                    disposition="changed",
                    expected_hash=exp_hash,
                    actual_hash=actual,
                )
            )

    for name, actual in sorted(mounted_files.items()):
        if name not in expected.files:
            findings.append(
                ParityFinding(
                    name=name,
                    disposition="unexpected",
                    expected_hash=None,
                    actual_hash=actual,
                )
            )

    if not findings:
        return ParityResult(ok=True, findings=())

    primary = findings[0].disposition
    reason_map = {
        "missing": "export_parity_missing",
        "changed": "export_parity_changed",
        "unexpected": "export_parity_unexpected",
        "manifest_drift": "export_parity_manifest_drift",
        "bad_inventory": "export_parity_bad_inventory",
        "pass": "export_parity_ok",
    }
    return ParityResult(
        ok=False,
        reason=reason_map.get(primary, "export_parity_mismatch"),
        findings=tuple(findings),
    )


def compare_mount_to_export(
    *,
    instructions_dir: Path,
    manifest_path: Path,
    export_inventory_path: Path,
) -> ParityResult:
    """Full consume compare: mount vs locked E1 artifact."""
    try:
        expected = load_export_inventory(export_inventory_path)
    except ExportParityError as exc:
        return ParityResult(
            ok=False,
            reason="export_parity_bad_inventory",
            findings=(
                ParityFinding(
                    name=str(export_inventory_path),
                    disposition="bad_inventory",
                    detail=str(exc),
                ),
            ),
        )
    try:
        bv, mounted = build_mounted_inventory(
            instructions_dir=instructions_dir,
            manifest_path=manifest_path,
        )
    except (ContentLoadError, ExportParityError) as exc:
        return ParityResult(
            ok=False,
            reason="export_parity_missing",
            findings=(
                ParityFinding(
                    name="mount",
                    disposition="missing",
                    detail=str(exc),
                ),
            ),
        )
    return compare_inventories(
        expected=expected,
        mounted_bundle_version=bv,
        mounted_files=mounted,
    )


def dump_e1_inventory_dict(
    *,
    bundle_version: str,
    files: dict[str, str],
) -> dict[str, Any]:
    """Serialize E1 inventory (helper for fixtures / ops notes)."""
    return {
        "wire": WIRE_E1,
        "bundle_version": bundle_version,
        "hash_method": HASH_METHOD_E1,
        "files": dict(sorted(files.items())),
    }
