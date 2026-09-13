"""ASGI application — single process bound to Railway $PORT."""

from __future__ import annotations

import json
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from aibridge.auth import is_channel_authorized
from aibridge.channel import process_action, process_turn
from aibridge.config import Settings, get_settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.deployment import DeploymentBundleState, verify_and_register_deployment
from aibridge.gateway import default_executor_from_settings
from aibridge.metrics import get_metrics
from aibridge.registry import BundleRegistry, MemoryBundleRegistry, open_bundle_registry
from aibridge.schemas import ChannelActionRequest, ChannelErrorBody, ChannelTurnRequest
from aibridge.sessions import MemorySessionStore, SessionStore, open_session_store

CHANNEL_PATH_PREFIX = "/v1/channel/"

# Pydantic error types treated as "unknown field" → HTTP 400 (AIB-CH-05 / audit G-01).
_UNKNOWN_FIELD_TYPES = frozenset({"extra_forbidden"})


def error_body(
    *,
    code: str,
    message: str,
    retryable: bool = False,
    request_id: str | None = None,
) -> dict[str, Any]:
    return ChannelErrorBody(
        request_id=request_id or str(uuid.uuid4()),
        error={"code": code, "message": message, "retryable": retryable},
    ).model_dump()


def validation_http_status(exc: ValidationError) -> tuple[int, str, str]:
    """Map ValidationError → (status, error_code, message).

    400 — unknown/extra fields (malformed shape at boundary).
    422 — semantically invalid channel input (AIB-CH-05).
    """
    errors = exc.errors()
    if errors and all(err.get("type") in _UNKNOWN_FIELD_TYPES for err in errors):
        return (
            400,
            "bad_request",
            "Malformed request or unknown field",
        )
    return (
        422,
        "semantic_invalid",
        "Semantically invalid channel input",
    )


def parse_channel_body(
    raw: bytes, model: type[ChannelTurnRequest] | type[ChannelActionRequest]
) -> ChannelTurnRequest | ChannelActionRequest | JSONResponse:
    """Parse JSON + validate; return model or JSONResponse error."""
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JSONResponse(
            status_code=400,
            content=error_body(code="bad_request", message="Malformed JSON"),
        )
    try:
        return model.model_validate(payload)
    except ValidationError as exc:
        status, code, message = validation_http_status(exc)
        return JSONResponse(
            status_code=status,
            content=error_body(code=code, message=message),
        )


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    """Reject oversized bodies with 413 (CORS not enabled — server-to-server)."""

    def __init__(self, app: ASGIApp, max_bytes: int) -> None:
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content=error_body(
                        code="bad_request",
                        message="Invalid Content-Length",
                    ),
                )
            if length > self.max_bytes:
                return JSONResponse(
                    status_code=413,
                    content=error_body(
                        code="payload_too_large",
                        message="Request body too large",
                    ),
                )
        return await call_next(request)


def _init_stores(
    settings: Settings,
    *,
    registry: BundleRegistry | None,
    sessions: SessionStore | None,
) -> tuple[BundleRegistry, SessionStore, DeploymentBundleState | None]:
    allow_memory = bool(settings.aibridge_allow_memory_stores)
    if registry is None:
        try:
            from aibridge.db import is_postgres_url
            from aibridge.migrate import apply_migrations

            if is_postgres_url(settings.database_url):
                apply_migrations(settings.database_url)
            registry = open_bundle_registry(
                settings.database_url,
                allow_memory=allow_memory,
                ensure_schema=False,
            )
        except RuntimeError:
            raise
        except (NotImplementedError, ImportError, OSError, ValueError) as exc:
            if not allow_memory:
                raise
            registry = MemoryBundleRegistry()
            return (
                registry,
                sessions or MemorySessionStore(),
                DeploymentBundleState(
                    loaded=None,
                    registered=None,
                    error=f"database_adapter_unavailable:{exc}",
                ),
            )
    if sessions is None:
        try:
            sessions = open_session_store(
                settings.database_url,
                allow_memory=allow_memory,
                ensure_schema=False,
            )
        except RuntimeError:
            raise
        except (NotImplementedError, ImportError, OSError, ValueError):
            if not allow_memory:
                raise
            sessions = MemorySessionStore()

    deployment: DeploymentBundleState | None = None
    if settings.content_configured():
        deployment = verify_and_register_deployment(
            instructions_dir=settings.dogestonia_instructions_dir,
            manifest_path=settings.dogestonia_instructions_manifest,
            source_commit=settings.dogestonia_content_source_commit,
            wire_oas_path=settings.dogestonia_openapi_path,
            pack_schema_path=settings.dogestonia_payload_schema_path,
            tool_schema_path=settings.dogestonia_tool_schema_path,
            registry=registry,
            schema_id=settings.dogestonia_schema_id,
            schema_version=settings.dogestonia_schema_version,
        )
    return registry, sessions, deployment


def create_app(
    *,
    settings: Settings | None = None,
    dedupe_store: EventDedupeStore | None = None,
    bundle_registry: BundleRegistry | None = None,
    session_store: SessionStore | None = None,
    confirmation_guard: ConfirmationGuard | None = None,
) -> FastAPI:
    """Application factory for production and tests."""
    if settings is not None:
        reset_settings_cache()

    app = FastAPI(
        title="doge-ai-bridge Channel Façade",
        version="0.2.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    cfg0 = settings if settings is not None else get_settings()

    from aibridge.db import is_postgres_url

    use_pg_runtime = is_postgres_url(cfg0.database_url) and not bool(
        cfg0.aibridge_allow_memory_stores
    )

    if dedupe_store is not None:
        store: Any = dedupe_store
    elif use_pg_runtime:
        from aibridge.migrate import apply_migrations
        from aibridge.pg_runtime import PostgresEventDedupeStore

        apply_migrations(cfg0.database_url)
        store = PostgresEventDedupeStore(cfg0.database_url)
    else:
        store = EventDedupeStore()
    app.state.dedupe_store = store
    app.state.settings_override = settings

    def resolve_settings() -> Settings:
        return settings if settings is not None else get_settings()

    turn_lock: Any | None = None
    history_store: Any | None = None
    if confirmation_guard is not None:
        guard = confirmation_guard
    elif use_pg_runtime:
        from aibridge.pg_runtime import (
            GatewayAttemptStore,
            PostgresActionTokenStore,
            PostgresConfirmSessionStore,
            PostgresHistoryStore,
            PostgresTurnLock,
        )

        # Migrations already applied above when dedupe defaulted; re-apply is no-op.
        from aibridge.migrate import apply_migrations

        apply_migrations(cfg0.database_url)
        turn_lock = PostgresTurnLock(cfg0.database_url)
        history_store = PostgresHistoryStore(cfg0.database_url)
        guard = reset_confirmation_guard(
            ConfirmationGuard(
                executor=default_executor_from_settings(cfg0),
                tokens=PostgresActionTokenStore(cfg0.database_url),
                gateway_attempts=GatewayAttemptStore(cfg0.database_url),
                confirm_sessions=PostgresConfirmSessionStore(cfg0.database_url),
            )
        )
    else:
        # G-01 (story 05): default ASGI path wires GatewayExecutor.
        guard = reset_confirmation_guard(
            ConfirmationGuard(executor=default_executor_from_settings(cfg0))
        )
    app.state.confirmation_guard = guard
    app.state.turn_lock = turn_lock
    app.state.history_store = history_store

    registry, sessions, deployment = _init_stores(
        cfg0, registry=bundle_registry, sessions=session_store
    )
    app.state.bundle_registry = registry
    app.state.session_store = sessions
    app.state.deployment_bundle = deployment

    max_bytes = cfg0.aibridge_max_request_bytes
    app.add_middleware(BodySizeLimitMiddleware, max_bytes=max_bytes)

    @app.middleware("http")
    async def channel_bearer_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path.startswith(CHANNEL_PATH_PREFIX):
            cfg = resolve_settings()
            if not is_channel_authorized(request.headers.get("authorization"), cfg):
                return JSONResponse(
                    status_code=401,
                    content=error_body(
                        code="unauthorized",
                        message="Unauthorized",
                    ),
                )
        return await call_next(request)

    @app.middleware("http")
    async def channel_http_error_metrics(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Count channel-facing HTTP errors (≥400) for Prometheus (G-01)."""
        response = await call_next(request)
        if (
            request.url.path.startswith(CHANNEL_PATH_PREFIX)
            and response.status_code >= 400
        ):
            get_metrics().inc_http_errors()
        return response

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz")
    async def readyz() -> JSONResponse:
        cfg = resolve_settings()
        if not cfg.channel_auth_configured():
            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "reason": "channel_auth_missing"},
            )
        if cfg.channel_gateway_bearers_equal():
            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "reason": "channel_gateway_bearer_equal"},
            )
        dep: DeploymentBundleState | None = app.state.deployment_bundle
        if cfg.content_configured():
            if dep is None or not dep.ready:
                reason = "content_bundle_not_ready"
                if dep is not None and dep.error:
                    reason = dep.error
                return JSONResponse(
                    status_code=503,
                    content={"status": "not_ready", "reason": reason},
                )
        elif dep is not None and dep.error:
            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "reason": dep.error},
            )
        return JSONResponse(status_code=200, content={"status": "ready"})

    @app.get("/metrics")
    async def metrics() -> PlainTextResponse:
        """Prometheus text — private network only (no channel Bearer required)."""
        body = get_metrics().render_prometheus()
        return PlainTextResponse(
            content=body,
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    @app.post("/v1/channel/turns")
    async def channel_turns(request: Request) -> JSONResponse:
        raw = await request.body()
        cfg = resolve_settings()
        if len(raw) > cfg.aibridge_max_request_bytes:
            return JSONResponse(
                status_code=413,
                content=error_body(code="payload_too_large", message="Request body too large"),
            )
        parsed = parse_channel_body(raw, ChannelTurnRequest)
        if isinstance(parsed, JSONResponse):
            return parsed
        response, _created = process_turn(
            parsed,
            store,
            guard=app.state.confirmation_guard,
            turn_lock=getattr(app.state, "turn_lock", None),
        )
        return JSONResponse(status_code=200, content=response)

    @app.post("/v1/channel/actions")
    async def channel_actions(request: Request) -> JSONResponse:
        raw = await request.body()
        cfg = resolve_settings()
        if len(raw) > cfg.aibridge_max_request_bytes:
            return JSONResponse(
                status_code=413,
                content=error_body(code="payload_too_large", message="Request body too large"),
            )
        parsed = parse_channel_body(raw, ChannelActionRequest)
        if isinstance(parsed, JSONResponse):
            return parsed
        success, _created, err = process_action(
            parsed,
            store,
            guard=app.state.confirmation_guard,
            turn_lock=getattr(app.state, "turn_lock", None),
        )
        if err is not None:
            status = int(err["http_status"])
            code = str(err["code"])
            # Map internal codes to channel error codes.
            code_map = {
                "forbidden": "forbidden",
                "not_found": "not_found",
                "conflict": "conflict",
            }
            return JSONResponse(
                status_code=status,
                content=error_body(
                    code=code_map.get(code, code),
                    message=str(err["message"]),
                ),
            )
        return JSONResponse(status_code=200, content=success)

    @app.exception_handler(RequestValidationError)
    async def validation_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # FastAPI may wrap body validation; prefer 422 unless all errors are extra_forbidden.
        errors = exc.errors()
        if errors and all(err.get("type") in _UNKNOWN_FIELD_TYPES for err in errors):
            status, code, message = (
                400,
                "bad_request",
                "Malformed request or unknown field",
            )
        else:
            status, code, message = (
                422,
                "semantic_invalid",
                "Semantically invalid channel input",
            )
        return JSONResponse(
            status_code=status,
            content=error_body(code=code, message=message),
        )

    return app


app = create_app()
