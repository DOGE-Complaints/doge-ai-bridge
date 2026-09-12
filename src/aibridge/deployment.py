"""Deployment content verify + register-once orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aibridge.content import ContentLoadError, LoadedContentBundle, load_content_bundle
from aibridge.registry import BundleRegistry, ContentBundleRow
from aibridge.tool_gen import ToolGenError, generate_strict_tool


@dataclass(frozen=True)
class DeploymentBundleState:
    loaded: LoadedContentBundle | None
    registered: ContentBundleRow | None
    error: str | None
    strict_tool: dict[str, Any] | None = None

    @property
    def ready(self) -> bool:
        return self.error is None and self.loaded is not None and self.registered is not None


def verify_and_register_deployment(
    *,
    instructions_dir: str,
    manifest_path: str,
    source_commit: str,
    wire_oas_path: str,
    pack_schema_path: str,
    tool_schema_path: str,
    registry: BundleRegistry,
    schema_id: str = "",
    schema_version: str = "",
) -> DeploymentBundleState:
    """Load local artifacts; on success register-once into registry.

    When schema_id + schema_version are set, also generate the strict Responses tool
    (unsupported OAS constructs → readiness failure, no silent non-strict).
    """
    if not instructions_dir or not manifest_path or not source_commit:
        return DeploymentBundleState(
            loaded=None,
            registered=None,
            error="content_env_incomplete",
        )
    if not wire_oas_path or not pack_schema_path:
        return DeploymentBundleState(
            loaded=None,
            registered=None,
            error="content_env_incomplete",
        )
    try:
        tool_path = Path(tool_schema_path) if tool_schema_path else None
        loaded = load_content_bundle(
            instructions_dir=Path(instructions_dir),
            manifest_path=Path(manifest_path),
            source_commit=source_commit,
            wire_oas_path=Path(wire_oas_path),
            pack_schema_path=Path(pack_schema_path),
            tool_schema_path=tool_path,
        )
    except ContentLoadError as exc:
        return DeploymentBundleState(
            loaded=None,
            registered=None,
            error=f"content_verify_failed:{exc}",
        )

    strict_tool: dict[str, Any] | None = None
    if schema_id and schema_version:
        try:
            strict_tool = generate_strict_tool(
                wire_oas_path=Path(wire_oas_path),
                pack_schema_path=Path(pack_schema_path),
                schema_id=schema_id,
                schema_version=schema_version,
            )
        except ToolGenError as exc:
            return DeploymentBundleState(
                loaded=loaded,
                registered=None,
                error=f"tool_gen_failed:{exc}",
            )

    try:
        registered = registry.register_once(loaded)
    except Exception as exc:  # noqa: BLE001 — surface as readiness reason
        return DeploymentBundleState(
            loaded=loaded,
            registered=None,
            error=f"content_register_failed:{exc}",
            strict_tool=strict_tool,
        )
    return DeploymentBundleState(
        loaded=loaded,
        registered=registered,
        error=None,
        strict_tool=strict_tool,
    )
