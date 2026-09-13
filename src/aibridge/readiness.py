"""Strict `/readyz` evaluation — REQ-03 §5.5 (no OpenAI gen / no gateway write)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aibridge.config import Settings
from aibridge.db import connect_postgres, is_postgres_url
from aibridge.deployment import DeploymentBundleState
from aibridge.migrate import list_migration_files


@dataclass(frozen=True)
class ReadinessResult:
    ready: bool
    reason: str | None = None


def _postgres_migration_ok(database_url: str) -> ReadinessResult:
    """Read-only connectivity + migration version (SELECT only; no DDL/DML)."""
    try:
        conn = connect_postgres(database_url)
    except Exception:
        return ReadinessResult(False, "database_unreachable")
    try:
        expected = [p.stem for p in list_migration_files()]
        if not expected:
            return ReadinessResult(False, "migrations_missing")
        try:
            rows = conn.execute("SELECT version FROM schema_migrations").fetchall()
        except Exception:
            return ReadinessResult(False, "migration_version_missing")
        versions: set[str] = set()
        for row in rows:
            if isinstance(row, dict):
                versions.add(str(row["version"]))
            else:
                versions.add(str(row[0]))
        if not versions:
            return ReadinessResult(False, "migration_version_missing")
        current = sorted(versions)[-1]
        if current != expected[-1]:
            return ReadinessResult(False, "migration_version_mismatch")
        return ReadinessResult(True)
    except Exception:
        return ReadinessResult(False, "database_migration_check_failed")
    finally:
        try:
            conn.close()
        except Exception:
            pass


def _tool_schema_ok(settings: Settings) -> ReadinessResult:
    path = (settings.dogestonia_tool_schema_path or "").strip()
    if not path:
        # Tool path optional until content+tool wiring; content bundle covers pack.
        return ReadinessResult(True)
    p = Path(path)
    if not p.is_file():
        return ReadinessResult(False, "tool_schema_missing")
    try:
        raw = p.read_text(encoding="utf-8")
        if not raw.strip():
            return ReadinessResult(False, "tool_schema_empty")
    except OSError:
        return ReadinessResult(False, "tool_schema_unreadable")
    return ReadinessResult(True)


def _strict_tool_ok(
    settings: Settings,
    deployment: DeploymentBundleState | None,
) -> ReadinessResult:
    """§5.5 — when schema ids configured, require generate_strict_tool success (local files only)."""
    schema_id = (settings.dogestonia_schema_id or "").strip()
    schema_version = (settings.dogestonia_schema_version or "").strip()
    if not schema_id or not schema_version:
        return ReadinessResult(True)
    if not settings.content_configured():
        return ReadinessResult(True)
    if deployment is not None and deployment.strict_tool is not None:
        return ReadinessResult(True)
    if deployment is not None and deployment.error and str(deployment.error).startswith(
        "tool_gen_failed:"
    ):
        return ReadinessResult(False, deployment.error)
    try:
        from aibridge.tool_gen import ToolGenError, generate_strict_tool

        generate_strict_tool(
            wire_oas_path=Path(settings.dogestonia_openapi_path),
            pack_schema_path=Path(settings.dogestonia_payload_schema_path),
            schema_id=schema_id,
            schema_version=schema_version,
        )
    except ToolGenError as exc:
        return ReadinessResult(False, f"tool_gen_failed:{exc}")
    except Exception as exc:  # noqa: BLE001
        return ReadinessResult(False, f"tool_gen_failed:{exc}")
    return ReadinessResult(True)


def evaluate_readiness(
    settings: Settings,
    deployment: DeploymentBundleState | None = None,
) -> ReadinessResult:
    """Return readiness without OpenAI generation or gateway HTTPS writes."""
    if not settings.channel_auth_configured():
        return ReadinessResult(False, "channel_auth_missing")
    if not settings.dogestonia_api_bearer_token:
        return ReadinessResult(False, "gateway_bearer_missing")
    if settings.channel_gateway_bearers_equal():
        return ReadinessResult(False, "channel_gateway_bearer_equal")

    if settings.gateway_base_url_conflict():
        return ReadinessResult(False, "gateway_base_url_conflict")
    if not settings.resolved_gateway_base_url():
        return ReadinessResult(False, "gateway_base_url_missing")
    if not settings.gateway_base_url_https_ok():
        return ReadinessResult(False, "gateway_base_url_not_https")

    if not settings.draft_redirect_base_ok():
        return ReadinessResult(False, "draft_redirect_base_invalid")

    if not settings.openai_presence_ok():
        return ReadinessResult(False, "openai_config_missing")
    if not settings.responses_store_false_enforced():
        return ReadinessResult(False, "openai_store_not_false")

    # Until story 14 (R3-P1-03): dry-run must be true for readiness.
    if not settings.aibridge_schema_validation_complete and not settings.aibridge_dry_run:
        return ReadinessResult(False, "dry_run_required")

    if settings.content_configured():
        if deployment is None or not deployment.ready:
            reason = "content_bundle_not_ready"
            if deployment is not None and deployment.error:
                reason = deployment.error
            return ReadinessResult(False, reason)
    elif deployment is not None and deployment.error:
        return ReadinessResult(False, deployment.error)

    tool = _tool_schema_ok(settings)
    if not tool.ready:
        return tool

    strict = _strict_tool_ok(settings, deployment)
    if not strict.ready:
        return strict

    if is_postgres_url(settings.database_url):
        db = _postgres_migration_ok(settings.database_url)
        if not db.ready:
            return db
    elif not settings.aibridge_allow_memory_stores:
        return ReadinessResult(False, "database_not_postgres")

    return ReadinessResult(True)


def readiness_payload(result: ReadinessResult) -> dict[str, Any]:
    if result.ready:
        return {"status": "ready"}
    return {"status": "not_ready", "reason": result.reason or "unknown"}
