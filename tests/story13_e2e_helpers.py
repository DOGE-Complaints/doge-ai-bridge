"""STORY-AIBRIDGE-13 — shared ASGI E2E harness (fake OpenAI + fake/dry-run gateway + disposable PG)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.coordinator import ValidationContext
from aibridge.db import is_postgres_url
from aibridge.gateway import GatewayExecutor, RawHttpResponse, RecordingGatewayTransport
from aibridge.interview import InterviewEngine
from aibridge.migrate import apply_migrations
from aibridge.request_assembly import ServerConstants
from aibridge.responses_client import RecordingResponsesClient

ROOT = Path(__file__).resolve().parents[1]
PGDATA = ROOT / ".pgdata-test"
PGPORT = "55432"
DISPOSABLE_URL = (
    f"postgresql://aibridge@/aibridge_test?host={PGDATA}&port={PGPORT}"
)
OAS_PATH = ROOT / "docs" / "openapi" / "aibridge-channel-v1.openapi.yaml"

CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

PACK_SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string"}},
    "required": ["title"],
    "additionalProperties": False,
}
TOOL_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "required": ["narrative", "schema_binding"],
    "properties": {
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["structured_payload"],
            "properties": {
                "structured_payload": {"type": "object", "additionalProperties": True},
            },
        },
    },
}
WIRE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "narrative", "schema_binding", "origin"],
    "properties": {
        "schema_version": {"type": "string"},
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_id", "schema_version", "structured_payload"],
            "properties": {
                "schema_id": {"type": "string"},
                "schema_version": {"type": "string"},
                "structured_payload": PACK_SCHEMA,
            },
        },
        "origin": {
            "type": "object",
            "additionalProperties": False,
            "required": ["source"],
            "properties": {"source": {"type": "string"}},
        },
    },
}

_OAS_CACHE: dict[str, Any] | None = None


def pg_available() -> bool:
    if not PGDATA.is_dir():
        return False
    try:
        from aibridge.db import connect_postgres

        conn = connect_postgres(DISPOSABLE_URL)
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False


def truncate_pg(url: str = DISPOSABLE_URL) -> str:
    assert is_postgres_url(url)
    apply_migrations(url)
    from aibridge.db import connect_postgres

    conn = connect_postgres(url)
    # Drop leftover app connections so TRUNCATE is not blocked by idle-in-txn.
    conn.execute(
        """
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = current_database()
          AND pid <> pg_backend_pid()
        """
    )
    conn.commit()
    for table in (
        "event_dedupe",
        "action_token",
        "session_call",
        "gateway_attempt",
        "session_turn_lock",
        "conversation_history",
        "confirm_session",
        "session",
        "content_bundle",
    ):
        conn.execute(f"TRUNCATE {table} CASCADE")
    conn.commit()
    conn.close()
    return url


def validation_context() -> ValidationContext:
    return ValidationContext(
        tool_parameters=TOOL_PARAMS,
        pack_schema=PACK_SCHEMA,
        wire_schema=WIRE_SCHEMA,
        constants=ServerConstants(schema_id="pack-test", schema_version_pack="v1"),
    )


def good_tool_args() -> dict[str, Any]:
    return {
        "narrative": {"note": "e2e"},
        "schema_binding": {"structured_payload": {"title": "ok"}},
    }


def text_openai_payload(text: str = "Interview reply for wave-1 E2E.") -> dict[str, Any]:
    return {
        "id": "resp_text",
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": text}],
            }
        ],
        "usage": {"input_tokens": 3, "output_tokens": 5},
    }


def fc_openai_payload(*, call_id: str = "call_e2e", args: dict | None = None) -> dict[str, Any]:
    return {
        "id": "resp_fc",
        "output": [
            {
                "type": "function_call",
                "call_id": call_id,
                "name": "postStoryDraftStash",
                "arguments": json.dumps(args or good_tool_args()),
            },
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "Ready to stash."}],
            },
        ],
        "usage": {"input_tokens": 5, "output_tokens": 3},
    }


def followup_openai_payload(text: str = "Draft noted — not published.") -> dict[str, Any]:
    return {
        "id": "resp_fco",
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": text}],
            }
        ],
        "usage": {"input_tokens": 1, "output_tokens": 1},
    }


def ok_201(draft_id: str = "draft-e2e-13") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": "t-e2e"}).encode()
    return RawHttpResponse(status_code=201, body=body)


def load_oas() -> dict[str, Any]:
    global _OAS_CACHE
    if _OAS_CACHE is None:
        _OAS_CACHE = yaml.safe_load(OAS_PATH.read_text(encoding="utf-8"))
    return _OAS_CACHE


SUCCESS_REQUIRED = {
    "request_id",
    "session_id",
    "state",
    "reply_text",
    "actions",
    "outcome",
    "draft_id",
    "continuation_url",
}


def assert_channel_success_conforms(body: dict[str, Any]) -> None:
    """Conformance to OAS ChannelSuccessResponse (required keys + action shape)."""
    spec = load_oas()
    required = set(spec["components"]["schemas"]["ChannelSuccessResponse"]["required"])
    assert required == SUCCESS_REQUIRED
    assert set(body.keys()) == SUCCESS_REQUIRED
    assert isinstance(body["reply_text"], str)
    assert isinstance(body["actions"], list)
    for action in body["actions"]:
        assert set(action.keys()) >= {"label", "token", "style"}
        assert action["style"] in {"primary", "success", "danger", "default"}


def assert_channel_error_conforms(body: dict[str, Any]) -> None:
    """Conformance to OAS ChannelErrorBody."""
    spec = load_oas()
    required = set(spec["components"]["schemas"]["ChannelErrorBody"]["required"])
    assert required == {"request_id", "error"}
    assert set(body.keys()) == {"request_id", "error"}
    err = body["error"]
    assert set(err.keys()) == {"code", "message", "retryable"}
    assert isinstance(err["retryable"], bool)


@dataclass
class E2EHarness:
    client: TestClient
    app: Any
    openai: RecordingResponsesClient
    transport: RecordingGatewayTransport
    settings: Settings
    auth_header: dict[str, str]

    @property
    def guard(self) -> ConfirmationGuard:
        return self.app.state.confirmation_guard


def build_e2e_harness(
    *,
    openai_scripted: list[dict[str, Any]] | None = None,
    gateway_scripted: list[RawHttpResponse] | None = None,
    dry_run_gateway: bool = False,
    pg_url: str = DISPOSABLE_URL,
) -> E2EHarness:
    """ASGI app on disposable Postgres with fake OpenAI + fake/dry-run gateway.

    Never contacts live OpenAI / n8n / Railway. Fake transport never hits real
    ``POST /story-drafts``; dry-run path never posts HTTPS.
    """
    truncate_pg(pg_url)
    reset_settings_cache()
    reset_confirmation_guard()

    openai = RecordingResponsesClient(scripted=list(openai_scripted or []))
    engine = InterviewEngine(client=openai)
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL_TOKEN,
        AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN="",
        DOGESTONIA_API_BEARER_TOKEN=GATEWAY_TOKEN,
        AIBRIDGE_MAX_REQUEST_BYTES=65536,
        PORT=8080,
        DOGESTONIA_API_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="",  # never ProductionResponsesClient
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
        DATABASE_URL=pg_url,
        AIBRIDGE_ALLOW_MEMORY_STORES=False,
    )
    app = create_app(settings=settings, interview_engine=engine)
    transport = RecordingGatewayTransport(scripted=list(gateway_scripted or []))
    guard = app.state.confirmation_guard
    guard.executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY_TOKEN,
        channel_bearer=CHANNEL_TOKEN,
        dry_run=dry_run_gateway,
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    guard.validation_context = validation_context()
    guard.interview_engine = engine
    app.state.interview_engine = engine
    return E2EHarness(
        client=TestClient(app),
        app=app,
        openai=openai,
        transport=transport,
        settings=settings,
        auth_header={"Authorization": f"Bearer {CHANNEL_TOKEN}"},
    )


def rebuild_app_same_pg(
    h: E2EHarness,
    *,
    openai_scripted: list[dict[str, Any]] | None = None,
    gateway_scripted: list[RawHttpResponse] | None = None,
    dry_run_gateway: bool = False,
) -> E2EHarness:
    """Simulate process restart against the same disposable Postgres (no truncate)."""
    reset_settings_cache()
    reset_confirmation_guard()
    openai = RecordingResponsesClient(scripted=list(openai_scripted or []))
    engine = InterviewEngine(client=openai)
    app = create_app(settings=h.settings, interview_engine=engine)
    transport = RecordingGatewayTransport(scripted=list(gateway_scripted or []))
    guard = app.state.confirmation_guard
    guard.executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY_TOKEN,
        channel_bearer=CHANNEL_TOKEN,
        dry_run=dry_run_gateway,
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    guard.validation_context = validation_context()
    guard.interview_engine = engine
    app.state.interview_engine = engine
    return E2EHarness(
        client=TestClient(app),
        app=app,
        openai=openai,
        transport=transport,
        settings=h.settings,
        auth_header=h.auth_header,
    )


def turn_body(
    *,
    event_id: str,
    text: str = "hello",
    user_id: str = "42",
    chat_id: str = "-100",
) -> dict[str, Any]:
    return {
        "channel": "telegram",
        "event_id": event_id,
        "principal": {"user_id": user_id, "chat_id": chat_id},
        "message": {"message_id": "1", "text": text},
    }


def action_body(
    *,
    event_id: str,
    token: str,
    user_id: str = "42",
    chat_id: str = "-100",
    callback_query_id: str = "cb1",
) -> dict[str, Any]:
    return {
        "channel": "telegram",
        "event_id": event_id,
        "callback_query_id": callback_query_id,
        "principal": {"user_id": user_id, "chat_id": chat_id},
        "action_token": token,
    }
