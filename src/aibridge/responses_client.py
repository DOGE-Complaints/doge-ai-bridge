"""Responses request assembly + production/recording clients (REQ-03 §5.1)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol

# Finite client knobs (not inventing budget policy — required on production path).
DEFAULT_MAX_OUTPUT_TOKENS = 4096
DEFAULT_TIMEOUT_MS = 30_000
DEFAULT_CONNECT_TIMEOUT_MS = 5_000


class DualInstructionsError(ValueError):
    """R3-P0-13 — stable prefix and instructions= must not both be used."""


class ResponsesTransportError(RuntimeError):
    """Bounded transport failure (timeout / HTTP / network)."""

    def __init__(self, outcome: str, message: str) -> None:
        super().__init__(message)
        self.outcome = outcome


class ResponsesOutcome(StrEnum):
    OK = "ok"
    RATE_LIMITED = "rate_limited"
    TRANSIENT_FAILURE = "transient_failure"
    TIMEOUT = "timeout"
    CLIENT_ERROR = "client_error"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True)
class ResponsesRequest:
    """Assembled Responses API payload (not sent until client.call)."""

    payload: dict[str, Any]

    @property
    def store(self) -> bool:
        return bool(self.payload.get("store"))


@dataclass(frozen=True)
class FunctionCallItem:
    call_id: str
    name: str
    arguments: str


@dataclass
class ParsedResponsesResult:
    """Normalized Responses payload — preserves all output items for replay."""

    outcome: ResponsesOutcome
    response_id: str | None
    output_items: list[dict[str, Any]]
    function_calls: list[FunctionCallItem]
    usage: dict[str, Any]
    cached_input_tokens: int
    reply_text: str
    http_status: int | None = None
    raw: dict[str, Any] = field(default_factory=dict)


def redact_secrets(text: str, *secrets: str) -> str:
    """Never leak API keys (or other secrets) into logs/exceptions."""
    out = text
    for secret in secrets:
        if secret and secret in out:
            out = out.replace(secret, "***")
    # Common Authorization header shapes.
    out = re.sub(r"(Bearer\s+)\S+", r"\1***", out, flags=re.IGNORECASE)
    out = re.sub(
        r"(api[_-]?key[\"']?\s*[:=]\s*[\"']?)[^\"'\s]+",
        r"\1***",
        out,
        flags=re.IGNORECASE,
    )
    return out


def assemble_responses_request(
    *,
    model: str,
    input_items: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    instructions: str | None = None,
    max_output_tokens: int | None = None,
) -> ResponsesRequest:
    """Build a Responses request. Every request must set store:false (AIB-RSP-01)."""
    payload: dict[str, Any] = {
        "model": model,
        "input": list(input_items),
        "store": False,
        "parallel_tool_calls": False,
    }
    if tools is not None:
        payload["tools"] = list(tools)
    if instructions is not None:
        payload["instructions"] = instructions
    # Finite max_output_tokens on every production-shaped assemble when provided.
    if max_output_tokens is not None:
        if max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be a positive finite int")
        payload["max_output_tokens"] = int(max_output_tokens)
    return ResponsesRequest(payload=payload)


def assert_prompt_xor(
    *,
    has_stable_prefix: bool,
    instructions: str | None,
) -> None:
    """Fail closed when both stable prefix and instructions= would be sent."""
    instr = (instructions or "").strip()
    if has_stable_prefix and instr:
        raise DualInstructionsError(
            "canonical prompt: use stable prefix OR instructions=, not both (R3-P0-13)"
        )


def cached_input_tokens_from_usage(usage: dict[str, Any] | None) -> int:
    """Read cached input tokens from Responses usage shapes."""
    if not usage:
        return 0
    if "cached_tokens" in usage:
        return int(usage.get("cached_tokens") or 0)
    details = usage.get("input_tokens_details")
    if isinstance(details, dict) and "cached_tokens" in details:
        return int(details.get("cached_tokens") or 0)
    # Some fixtures nest under input_tokens_details.cached_tokens already handled.
    return 0


def parse_responses_payload(
    payload: dict[str, Any],
    *,
    outcome: ResponsesOutcome = ResponsesOutcome.OK,
    http_status: int | None = None,
) -> ParsedResponsesResult:
    """Parse function_call/call_id/args/usage; preserve every output item."""
    output = payload.get("output")
    items: list[dict[str, Any]] = []
    if isinstance(output, list):
        items = [dict(x) for x in output if isinstance(x, dict)]

    function_calls: list[FunctionCallItem] = []
    reply_text = ""
    for item in items:
        itype = str(item.get("type") or "")
        if itype == "function_call":
            function_calls.append(
                FunctionCallItem(
                    call_id=str(item.get("call_id") or item.get("id") or ""),
                    name=str(item.get("name") or ""),
                    arguments=str(item.get("arguments") or ""),
                )
            )
        elif itype == "message":
            for part in item.get("content") or []:
                if isinstance(part, dict) and part.get("type") == "output_text":
                    text = str(part.get("text") or "")
                    if text:
                        reply_text = text

    usage = dict(payload.get("usage") or {}) if isinstance(payload.get("usage"), dict) else {}
    return ParsedResponsesResult(
        outcome=outcome,
        response_id=str(payload["id"]) if payload.get("id") is not None else None,
        output_items=items,
        function_calls=function_calls,
        usage=usage,
        cached_input_tokens=cached_input_tokens_from_usage(usage),
        reply_text=reply_text or "Acknowledged.",
        http_status=http_status,
        raw=dict(payload),
    )


def map_http_to_outcome(status_code: int) -> ResponsesOutcome:
    if status_code == 429:
        return ResponsesOutcome.RATE_LIMITED
    if 500 <= status_code <= 599:
        return ResponsesOutcome.TRANSIENT_FAILURE
    if 400 <= status_code <= 499:
        return ResponsesOutcome.CLIENT_ERROR
    if 200 <= status_code <= 299:
        return ResponsesOutcome.OK
    return ResponsesOutcome.INTERNAL_ERROR


class ResponsesClient(Protocol):
    def create(self, request: ResponsesRequest) -> dict[str, Any]: ...


class ResponsesHttpTransport(Protocol):
    def post_json(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout_seconds: float,
        connect_timeout_seconds: float,
    ) -> tuple[int, dict[str, Any] | None, str]:
        """Return (status, json_or_none, raw_text)."""
        ...


class AsyncResponsesHttpTransport(Protocol):
    async def post_json(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout_seconds: float,
        connect_timeout_seconds: float,
    ) -> tuple[int, dict[str, Any] | None, str]:
        """Async return (status, json_or_none, raw_text)."""
        ...


@dataclass
class RecordingResponsesTransport:
    """Scripted HTTP responses — never contacts OpenAI."""

    scripted: list[tuple[int, dict[str, Any] | None, str]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    raise_timeout: bool = False

    def post_json(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout_seconds: float,
        connect_timeout_seconds: float,
    ) -> tuple[int, dict[str, Any] | None, str]:
        self.calls.append(
            {
                "url": url,
                "headers": dict(headers),
                "json_body": dict(json_body),
                "timeout_seconds": timeout_seconds,
                "connect_timeout_seconds": connect_timeout_seconds,
            }
        )
        if self.raise_timeout:
            raise TimeoutError("connect/read timeout")
        if not self.scripted:
            raise RuntimeError("RecordingResponsesTransport: no scripted response")
        return self.scripted.pop(0)


@dataclass
class RecordingAsyncResponsesTransport:
    """Async scripted HTTP — never contacts OpenAI; for acreate unit tests."""

    scripted: list[tuple[int, dict[str, Any] | None, str]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)

    async def post_json(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout_seconds: float,
        connect_timeout_seconds: float,
    ) -> tuple[int, dict[str, Any] | None, str]:
        self.calls.append(
            {
                "url": url,
                "headers": dict(headers),
                "json_body": dict(json_body),
                "timeout_seconds": timeout_seconds,
                "connect_timeout_seconds": connect_timeout_seconds,
            }
        )
        if not self.scripted:
            raise RuntimeError("RecordingAsyncResponsesTransport: no scripted response")
        return self.scripted.pop(0)


@dataclass
class HttpxResponsesTransport:
    """Sync httpx transport — used only from thread or sync callers."""

    verify_tls: bool = True

    def post_json(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout_seconds: float,
        connect_timeout_seconds: float,
    ) -> tuple[int, dict[str, Any] | None, str]:
        import httpx

        timeout = httpx.Timeout(
            timeout_seconds,
            connect=connect_timeout_seconds,
        )
        with httpx.Client(timeout=timeout, verify=self.verify_tls) as client:
            resp = client.post(url, headers=headers, json=json_body)
        text = resp.text
        try:
            body = resp.json() if resp.content else None
        except json.JSONDecodeError:
            body = None
        if not isinstance(body, dict):
            body = None
        return resp.status_code, body, text


@dataclass
class ProductionResponsesClient:
    """Production Responses path — knobs + bounded errors; fake transport OK in tests."""

    api_key: str
    model: str = "gpt-4.1-mini"
    base_url: str = "https://api.openai.com/v1"
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    timeout_ms: int = DEFAULT_TIMEOUT_MS
    connect_timeout_ms: int = DEFAULT_CONNECT_TIMEOUT_MS
    transport: ResponsesHttpTransport = field(default_factory=HttpxResponsesTransport)
    async_transport: AsyncResponsesHttpTransport | None = None

    def __post_init__(self) -> None:
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be finite and positive")
        if self.timeout_ms <= 0 or self.connect_timeout_ms <= 0:
            raise ValueError("timeouts must be finite and positive")

    def _url(self) -> str:
        return f"{self.base_url.rstrip('/')}/responses"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _ensure_knobs(self, request: ResponsesRequest) -> dict[str, Any]:
        body = dict(request.payload)
        body["store"] = False
        body["parallel_tool_calls"] = False
        if "max_output_tokens" not in body:
            body["max_output_tokens"] = self.max_output_tokens
        return body

    def _safe_message(self, exc: BaseException) -> str:
        return redact_secrets(str(exc), self.api_key)

    def create(self, request: ResponsesRequest) -> dict[str, Any]:
        """Sync create — InterviewEngine / tests. Prefer acreate from ASGI."""
        parsed = self._execute(request)
        return self._to_engine_dict(parsed)

    async def acreate(self, request: ResponsesRequest) -> dict[str, Any]:
        """ASGI-safe create — async_transport (tests) or httpx.AsyncClient."""
        body = self._ensure_knobs(request)
        headers = self._headers()
        timeout_s = self.timeout_ms / 1000.0
        connect_s = self.connect_timeout_ms / 1000.0
        try:
            if self.async_transport is not None:
                status, payload, text = await self.async_transport.post_json(
                    self._url(),
                    headers=headers,
                    json_body=body,
                    timeout_seconds=timeout_s,
                    connect_timeout_seconds=connect_s,
                )
            else:
                import httpx

                timeout = httpx.Timeout(timeout_s, connect=connect_s)
                async with httpx.AsyncClient(timeout=timeout, verify=True) as client:
                    resp = await client.post(self._url(), headers=headers, json=body)
                text = resp.text
                try:
                    payload = resp.json() if resp.content else None
                except json.JSONDecodeError:
                    payload = None
                if not isinstance(payload, dict):
                    payload = None
                status = resp.status_code
            parsed = self._map_response(status, payload, text)
        except TimeoutError as exc:
            raise ResponsesTransportError(
                ResponsesOutcome.TIMEOUT.value, self._safe_message(exc)
            ) from None
        except ResponsesTransportError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ResponsesTransportError(
                ResponsesOutcome.INTERNAL_ERROR.value, self._safe_message(exc)
            ) from None
        if parsed.outcome is not ResponsesOutcome.OK:
            raise ResponsesTransportError(
                parsed.outcome.value,
                redact_secrets(
                    f"Responses HTTP {parsed.http_status}: {parsed.reply_text}",
                    self.api_key,
                ),
            )
        return self._to_engine_dict(parsed)

    def _execute(self, request: ResponsesRequest) -> ParsedResponsesResult:
        body = self._ensure_knobs(request)
        try:
            status, payload, text = self.transport.post_json(
                self._url(),
                headers=self._headers(),
                json_body=body,
                timeout_seconds=self.timeout_ms / 1000.0,
                connect_timeout_seconds=self.connect_timeout_ms / 1000.0,
            )
        except TimeoutError as exc:
            raise ResponsesTransportError(
                ResponsesOutcome.TIMEOUT.value, self._safe_message(exc)
            ) from None
        except Exception as exc:  # noqa: BLE001
            msg = self._safe_message(exc)
            if "timeout" in msg.lower():
                raise ResponsesTransportError(ResponsesOutcome.TIMEOUT.value, msg) from None
            raise ResponsesTransportError(ResponsesOutcome.INTERNAL_ERROR.value, msg) from None
        return self._map_response(status, payload, text)

    def _map_response(
        self,
        status: int,
        payload: dict[str, Any] | None,
        text: str,
    ) -> ParsedResponsesResult:
        outcome = map_http_to_outcome(status)
        if outcome is ResponsesOutcome.OK and payload is not None:
            return parse_responses_payload(payload, outcome=outcome, http_status=status)
        safe = redact_secrets(text[:500] if text else f"HTTP {status}", self.api_key)
        return ParsedResponsesResult(
            outcome=outcome,
            response_id=None,
            output_items=[],
            function_calls=[],
            usage={},
            cached_input_tokens=0,
            reply_text=safe or outcome.value,
            http_status=status,
            raw=dict(payload or {}),
        )

    def _to_engine_dict(self, parsed: ParsedResponsesResult) -> dict[str, Any]:
        if parsed.outcome is not ResponsesOutcome.OK:
            raise ResponsesTransportError(
                parsed.outcome.value,
                redact_secrets(
                    f"Responses outcome={parsed.outcome.value} status={parsed.http_status}",
                    self.api_key,
                ),
            )
        # Preserve full output list for InterviewEngine history replay.
        return {
            "id": parsed.response_id or "resp_unknown",
            "output": list(parsed.output_items),
            "usage": {
                **parsed.usage,
                "cached_tokens": parsed.cached_input_tokens,
            },
            "aibridge_parsed": {
                "function_calls": [
                    {
                        "call_id": fc.call_id,
                        "name": fc.name,
                        "arguments": fc.arguments,
                    }
                    for fc in parsed.function_calls
                ],
                "cached_input_tokens": parsed.cached_input_tokens,
                "reply_text": parsed.reply_text,
            },
        }


class RecordingResponsesClient:
    """Test double — records payloads; never contacts OpenAI or gateway."""

    def __init__(
        self,
        *,
        scripted: list[dict[str, Any]] | None = None,
    ) -> None:
        self.calls: list[dict[str, Any]] = []
        self.gateway_calls: int = 0
        self._scripted = list(scripted or [])

    def create(self, request: ResponsesRequest) -> dict[str, Any]:
        assert request.payload.get("store") is False
        assert request.payload.get("parallel_tool_calls") is False
        self.calls.append(dict(request.payload))
        if self._scripted:
            return dict(self._scripted.pop(0))
        return {
            "id": f"resp_test_{len(self.calls)}",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "ok"}],
                }
            ],
            "usage": {"input_tokens": 10, "output_tokens": 5, "cached_tokens": 0},
        }

    async def acreate(self, request: ResponsesRequest) -> dict[str, Any]:
        """Async mirror of create — ASGI/engine tests without blocking I/O."""
        return self.create(request)

    def call_gateway(self) -> None:
        """Must never be invoked on budget breach paths."""
        self.gateway_calls += 1
