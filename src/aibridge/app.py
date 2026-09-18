"""ASGI application — single process bound to Railway $PORT."""

from __future__ import annotations

import json
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any, overload

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from aibridge.auth import is_channel_authorized
from aibridge.budgets import (
    BudgetGuard,
    budget_limits_from_settings,
)
from aibridge.channel import process_action, process_turn_async
from aibridge.config import Settings, get_settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.deployment import DeploymentBundleState, verify_and_register_deployment
from aibridge.gateway import default_executor_from_settings
from aibridge.interview import InterviewEngine, default_recording_engine
from aibridge.metrics import get_metrics
from aibridge.rate_limit import RateLimiter, hash_principal_key
from aibridge.readiness import evaluate_readiness, readiness_payload
from aibridge.registry import BundleRegistry, MemoryBundleRegistry, open_bundle_registry
from aibridge.responses_client import (
    ProductionResponsesClient,
    ResponsesOutcome,
    ResponsesTransportError,
)
from aibridge.schemas import (
    ChannelActionRequest,
    ChannelErrorBody,
    ChannelErrorDetail,
    ChannelTurnRequest,
)
from aibridge.sessions import MemorySessionStore, SessionStore, open_session_store
from aibridge.action_tokens import ActionTokenStore

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
        error=ChannelErrorDetail(code=code, message=message, retryable=retryable),
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


@overload
def parse_channel_body(
    raw: bytes, model: type[ChannelTurnRequest]
) -> ChannelTurnRequest | JSONResponse: ...


@overload
def parse_channel_body(
    raw: bytes, model: type[ChannelActionRequest]
) -> ChannelActionRequest | JSONResponse: ...


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
            if length < 0:
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


def _apply_deployment_to_engine(
    engine: InterviewEngine,
    deployment: DeploymentBundleState | None,
    settings: Settings,
) -> DeploymentBundleState | None:
    """ADR-1 — mutate InterviewEngine from a ready deployment (stable prefix).

    Does not reorder create_app. When content is configured and assembled text is
    empty, returns a fail-closed DeploymentBundleState so /readyz stays 503.
    """
    if deployment is None:
        return None
    if not deployment.ready or deployment.loaded is None:
        return deployment

    assembled = (deployment.loaded.assembled_instructions or "").strip()
    if not assembled:
        return DeploymentBundleState(
            loaded=deployment.loaded,
            registered=deployment.registered,
            error="assembled_instructions_empty",
            strict_tool=deployment.strict_tool,
        )

    engine.prompt_channel = "prefix"
    engine.instructions = deployment.loaded.assembled_instructions
    if deployment.strict_tool is not None:
        engine.tools = [deployment.strict_tool]

    schema_id = (settings.dogestonia_schema_id or "").strip()
    schema_version = (settings.dogestonia_schema_version or "").strip()
    if schema_id and schema_version:
        engine.pack_id = f"{schema_id}/{schema_version}"

    return deployment


def create_app(
    *,
    settings: Settings | None = None,
    dedupe_store: EventDedupeStore | None = None,
    bundle_registry: BundleRegistry | None = None,
    session_store: SessionStore | None = None,
    confirmation_guard: ConfirmationGuard | None = None,
    interview_engine: InterviewEngine | None = None,
) -> FastAPI:
    """Application factory for production and tests."""
    if settings is not None:
        reset_settings_cache()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """AIB-OPS-03 — accept traffic on start; drain + mark executing unknown on stop."""
        app.state.accepting_traffic = True
        app.state.shutting_down = False
        yield
        app.state.shutting_down = True
        app.state.accepting_traffic = False
        guard_sd = getattr(app.state, "confirmation_guard", None)
        if guard_sd is not None and hasattr(guard_sd, "recover_all_executing_attempts"):
            guard_sd.recover_all_executing_attempts()

    app = FastAPI(
        title="doge-ai-bridge Channel Façade",
        version="0.2.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )
    cfg0 = settings if settings is not None else get_settings()
    app.state.accepting_traffic = True
    app.state.shutting_down = False

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

    # Log level when set (REQ-03 §5.6).
    import logging

    logging.getLogger("aibridge").setLevel(
        getattr(logging, str(cfg0.aibridge_log_level or "INFO").upper(), logging.INFO)
    )

    token_ttl = (
        int(cfg0.aibridge_action_token_ttl_seconds)
        if cfg0.aibridge_action_token_ttl_seconds is not None
        else 15 * 60
    )
    # R3-P1-02 — always attach BudgetGuard (finite defaults in Settings).
    budget_limits = budget_limits_from_settings(cfg0)
    budget_guard = BudgetGuard(budget_limits)

    connect_ms = (
        int(cfg0.aibridge_http_connect_timeout_ms)
        if cfg0.aibridge_http_connect_timeout_ms is not None
        else 5_000
    )
    openai_timeout_ms = (
        int(cfg0.aibridge_openai_timeout_ms)
        if cfg0.aibridge_openai_timeout_ms is not None
        else (
            int(cfg0.aibridge_http_total_timeout_ms)
            if cfg0.aibridge_http_total_timeout_ms is not None
            else 30_000
        )
    )

    # Interview engine — production client when key present; else recording default.
    if interview_engine is not None:
        engine = interview_engine
    elif cfg0.openai_api_key:
        engine = InterviewEngine(
            client=ProductionResponsesClient(
                api_key=cfg0.openai_api_key,
                model=cfg0.openai_model or "gpt-4.1-mini",
                timeout_ms=openai_timeout_ms,
                connect_timeout_ms=connect_ms,
            ),
            model=cfg0.openai_model or "gpt-4.1-mini",
        )
    else:
        engine = default_recording_engine()

    if engine.budgets is None:
        engine.budgets = budget_guard

    turn_lock: Any | None = None
    history_store: Any | None = None
    if confirmation_guard is not None:
        guard = confirmation_guard
        if guard.interview_engine is None:
            guard.interview_engine = engine
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
        engine.history = history_store
        guard = reset_confirmation_guard(
            ConfirmationGuard(
                executor=default_executor_from_settings(cfg0),
                tokens=PostgresActionTokenStore(
                    cfg0.database_url, ttl_seconds=token_ttl
                ),
                gateway_attempts=GatewayAttemptStore(cfg0.database_url),
                confirm_sessions=PostgresConfirmSessionStore(cfg0.database_url),
                interview_engine=engine,
            )
        )
        # REQ-03 §4 #8 / §5.3 — restart: executing → unknown_outcome, no auto-resend.
        guard.recover_all_executing_attempts()
    else:
        # G-01 (story 05): default ASGI path wires GatewayExecutor.
        guard = reset_confirmation_guard(
            ConfirmationGuard(
                executor=default_executor_from_settings(cfg0),
                tokens=ActionTokenStore(ttl_seconds=token_ttl),
                interview_engine=engine,
            )
        )
    app.state.confirmation_guard = guard
    app.state.interview_engine = engine
    app.state.turn_lock = turn_lock
    app.state.history_store = history_store
    app.state.budget_guard = budget_guard

    # Attach history for idle expiry minimize (G-01).
    if history_store is not None:
        guard.history = history_store
    elif getattr(engine, "history", None) is not None:
        guard.history = engine.history

    # R3-P1-10 — sliding session TTL clock (touch only on legitimate get_or_create).
    from aibridge.privacy_retention import (
        PILOT_SESSION_TTL_SECONDS,
        SessionActivityClock,
    )

    session_ttl = (
        int(cfg0.aibridge_session_ttl_seconds)
        if cfg0.aibridge_session_ttl_seconds is not None
        else PILOT_SESSION_TTL_SECONDS
    )
    activity_clock = SessionActivityClock(ttl_seconds=session_ttl)
    if getattr(guard, "activity_clock", None) is None:
        guard.activity_clock = activity_clock
    app.state.activity_clock = guard.activity_clock

    rate_limiter = RateLimiter(
        principal_limit=cfg0.aibridge_principal_rate_limit,
        global_limit=cfg0.aibridge_global_rate_limit,
    )
    app.state.rate_limiter = rate_limiter

    registry, sessions, deployment = _init_stores(
        cfg0, registry=bundle_registry, sessions=session_store
    )
    if cfg0.aibridge_session_ttl_seconds is not None and hasattr(
        sessions, "ttl_seconds"
    ):
        sessions.ttl_seconds = int(cfg0.aibridge_session_ttl_seconds)
    app.state.bundle_registry = registry
    app.state.session_store = sessions
    app.state.deployment_bundle = deployment
    # ADR-1 / REQ-05 §4.1 — wire assembled instructions + tools onto the same engine.
    app.state.deployment_bundle = _apply_deployment_to_engine(
        engine, app.state.deployment_bundle, cfg0
    )

    max_bytes = cfg0.aibridge_max_request_bytes
    app.add_middleware(BodySizeLimitMiddleware, max_bytes=max_bytes)

    @app.middleware("http")
    async def channel_drain_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """AIB-OPS-03 — stop accepting new channel turns/actions while shutting down."""
        if request.url.path.startswith(CHANNEL_PATH_PREFIX) and not getattr(
            app.state, "accepting_traffic", True
        ):
            return JSONResponse(
                status_code=503,
                content=error_body(
                    code="shutting_down",
                    message="Bridge is shutting down",
                    retryable=True,
                ),
            )
        return await call_next(request)

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
    async def channel_rate_limit_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path.startswith(CHANNEL_PATH_PREFIX) and rate_limiter.enabled():
            # Opaque hash — never store raw Authorization / Bearer prefix (AUTH-009 hygiene).
            principal_key = hash_principal_key(request.headers.get("authorization"))
            denied = rate_limiter.allow(principal_key)
            if denied is not None:
                return JSONResponse(
                    status_code=429,
                    content=error_body(
                        code="rate_limited",
                        message="Rate limit exceeded",
                        retryable=True,
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
        dep: DeploymentBundleState | None = app.state.deployment_bundle
        result = evaluate_readiness(cfg, dep)
        status = 200 if result.ready else 503
        return JSONResponse(status_code=status, content=readiness_payload(result))

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
        response, created = await process_turn_async(
            parsed,
            store,
            guard=app.state.confirmation_guard,
            turn_lock=getattr(app.state, "turn_lock", None),
            interview_engine=getattr(app.state, "interview_engine", None),
        )
        status_code = 200
        if not created:
            peek = getattr(store, "get", None)
            if peek is not None:
                stored = peek(parsed.channel, parsed.event_id)
                if stored is not None and hasattr(stored, "http_status"):
                    code = int(stored.http_status)
                    if code > 0:
                        status_code = code
        return JSONResponse(status_code=status_code, content=response)

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

    @app.exception_handler(ResponsesTransportError)
    async def responses_transport_channel_error(
        request: Request, exc: ResponsesTransportError
    ) -> JSONResponse:
        """CHAR-006 Option A — map OpenAI transport outcomes to bounded channel errors.

        Distinct from client rate-limit middleware (also 429 ``rate_limited``).
        Unmapped outcomes fall through to generic ``internal_error`` handler.
        """
        if not request.url.path.startswith(CHANNEL_PATH_PREFIX):
            return JSONResponse(
                status_code=500,
                content={"status": "error", "reason": "internal_error"},
            )
        outcome = str(exc.outcome)
        if outcome == ResponsesOutcome.RATE_LIMITED.value:
            return JSONResponse(
                status_code=429,
                content=error_body(
                    code="rate_limited",
                    message="OpenAI rate limited",
                    retryable=True,
                ),
            )
        if outcome == ResponsesOutcome.TRANSIENT_FAILURE.value:
            return JSONResponse(
                status_code=503,
                content=error_body(
                    code="transient_failure",
                    message="OpenAI upstream transient failure",
                    retryable=True,
                ),
            )
        # TIMEOUT / CLIENT_ERROR / INTERNAL_ERROR — keep bounded 500 shape (OAI-010 etc.)
        return JSONResponse(
            status_code=500,
            content=error_body(
                code="internal_error",
                message="Internal bridge error",
                retryable=True,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_channel_exception(
        request: Request, _exc: Exception
    ) -> JSONResponse:
        """Bounded OpenAPI channel 500 — no stack traces / secrets in body (P0-11)."""
        if request.url.path.startswith(CHANNEL_PATH_PREFIX):
            return JSONResponse(
                status_code=500,
                content=error_body(
                    code="internal_error",
                    message="Internal bridge error",
                    retryable=True,
                ),
            )
        return JSONResponse(
            status_code=500,
            content={"status": "error", "reason": "internal_error"},
        )

    return app


app = create_app()
