"""DeepSeek interview slot — Chat Completions + L12-3 nest behind ResponsesClient surface.

Hides Completions quirks inside the adapter (Interview D3). Never falls back to OpenAI.
Home: ``aibridge.interview_providers`` (≠ ``aibridge.providers``).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from aibridge.interview_providers.errors import InterviewProviderTransportError
from aibridge.interview_providers.ids import InterviewProviderId
from aibridge.responses_client import (
    DEFAULT_CONNECT_TIMEOUT_MS,
    DEFAULT_MAX_OUTPUT_TOKENS,
    DEFAULT_TIMEOUT_MS,
    AsyncResponsesHttpTransport,
    HttpxResponsesTransport,
    ResponsesClient,
    ResponsesHttpTransport,
    ResponsesOutcome,
    ResponsesRequest,
    map_http_to_outcome,
    redact_secrets,
)


def _text_from_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                text = part.get("text")
                if text is None:
                    text = part.get("content")
                if text is not None:
                    parts.append(str(text))
        return "\n".join(p for p in parts if p)
    return str(content)


def responses_input_to_chat_messages(
    input_items: list[dict[str, Any]],
    *,
    instructions: str | None = None,
) -> list[dict[str, Any]]:
    """Map Responses ``input`` (+ optional instructions) → Chat Completions messages."""
    messages: list[dict[str, Any]] = []
    instr = (instructions or "").strip()
    if instr:
        messages.append({"role": "system", "content": instr})

    for item in input_items:
        if not isinstance(item, dict):
            continue
        itype = str(item.get("type") or "message")
        if itype == "message" or ("role" in item and itype not in {"function_call", "function_call_output"}):
            role = str(item.get("role") or "user")
            messages.append({"role": role, "content": _text_from_content(item.get("content"))})
            continue
        if itype == "function_call":
            call_id = str(item.get("call_id") or item.get("id") or "")
            messages.append(
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {
                                "name": str(item.get("name") or ""),
                                "arguments": str(item.get("arguments") or "{}"),
                            },
                        }
                    ],
                }
            )
            continue
        if itype == "function_call_output":
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": str(item.get("call_id") or ""),
                    "content": str(item.get("output") or ""),
                }
            )
    return messages


def responses_tools_to_completions(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]] | None:
    """Responses-flat tools → Chat Completions nested ``function`` wrap."""
    if not tools:
        return None
    out: list[dict[str, Any]] = []
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        if isinstance(tool.get("function"), dict):
            out.append({"type": "function", "function": dict(tool["function"])})
            continue
        fn: dict[str, Any] = {
            "name": tool.get("name"),
            "parameters": tool.get("parameters") or {},
        }
        if tool.get("description") is not None:
            fn["description"] = tool["description"]
        out.append({"type": "function", "function": fn})
    return out or None


def completions_payload_to_engine_dict(payload: dict[str, Any]) -> dict[str, Any]:
    """Map Chat Completions JSON → Responses-shaped dict for InterviewEngine."""
    choices = payload.get("choices")
    message: dict[str, Any] = {}
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict) and isinstance(first.get("message"), dict):
            message = dict(first["message"])

    output: list[dict[str, Any]] = []
    function_calls: list[dict[str, str]] = []
    tool_calls = message.get("tool_calls")
    if isinstance(tool_calls, list):
        for tc in tool_calls:
            if not isinstance(tc, dict):
                continue
            fn = tc.get("function") if isinstance(tc.get("function"), dict) else {}
            call_id = str(tc.get("id") or "")
            name = str(fn.get("name") or "")
            arguments = str(fn.get("arguments") or "{}")
            output.append(
                {
                    "type": "function_call",
                    "call_id": call_id,
                    "name": name,
                    "arguments": arguments,
                }
            )
            function_calls.append(
                {"call_id": call_id, "name": name, "arguments": arguments}
            )

    content = message.get("content")
    reply_text = ""
    if isinstance(content, str) and content.strip():
        reply_text = content
        output.append(
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": content}],
            }
        )

    usage_raw = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
    usage = {
        "input_tokens": int(usage_raw.get("prompt_tokens") or 0),
        "output_tokens": int(usage_raw.get("completion_tokens") or 0),
        "total_tokens": int(usage_raw.get("total_tokens") or 0),
        "cached_tokens": 0,
    }
    return {
        "id": str(payload.get("id") or "chatcmpl_unknown"),
        "output": output,
        "usage": usage,
        "aibridge_parsed": {
            "function_calls": function_calls,
            "cached_input_tokens": 0,
            "reply_text": reply_text or "Acknowledged.",
        },
    }


@dataclass
class DeepSeekChatCompletionsClient:
    """Chat Completions client presenting ``ResponsesClient`` create/acreate surface."""

    api_key: str
    base_url: str
    model: str
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
        if not (self.api_key and self.base_url and self.model):
            raise ValueError("deepseek client requires api_key, base_url, and model")

    def _url(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _safe_message(self, exc: BaseException) -> str:
        return redact_secrets(str(exc), self.api_key)

    def _completions_body(self, request: ResponsesRequest) -> dict[str, Any]:
        payload = dict(request.payload)
        input_items = payload.get("input")
        if not isinstance(input_items, list):
            input_items = []
        instructions = payload.get("instructions")
        instructions_s = str(instructions) if isinstance(instructions, str) else None
        body: dict[str, Any] = {
            "model": str(payload.get("model") or self.model),
            "messages": responses_input_to_chat_messages(
                [x for x in input_items if isinstance(x, dict)],
                instructions=instructions_s,
            ),
        }
        tools = responses_tools_to_completions(
            payload.get("tools") if isinstance(payload.get("tools"), list) else None
        )
        if tools:
            body["tools"] = tools
        max_tokens = payload.get("max_output_tokens")
        if max_tokens is None:
            max_tokens = self.max_output_tokens
        body["max_tokens"] = int(max_tokens)
        return body

    def _raise_mapped(
        self,
        status: int,
        payload: dict[str, Any] | None,
        text: str,
    ) -> dict[str, Any]:
        outcome = map_http_to_outcome(status)
        if outcome is ResponsesOutcome.OK and payload is not None:
            return completions_payload_to_engine_dict(payload)
        safe = redact_secrets(text[:500] if text else f"HTTP {status}", self.api_key)
        raise InterviewProviderTransportError(
            outcome.value,
            f"DeepSeek Completions HTTP {status}: {safe or outcome.value}",
            provider_id=InterviewProviderId.DEEPSEEK.value,
        )

    def create(self, request: ResponsesRequest) -> dict[str, Any]:
        body = self._completions_body(request)
        try:
            status, payload, text = self.transport.post_json(
                self._url(),
                headers=self._headers(),
                json_body=body,
                timeout_seconds=self.timeout_ms / 1000.0,
                connect_timeout_seconds=self.connect_timeout_ms / 1000.0,
            )
        except TimeoutError as exc:
            raise InterviewProviderTransportError(
                ResponsesOutcome.TIMEOUT.value,
                self._safe_message(exc),
                provider_id=InterviewProviderId.DEEPSEEK.value,
            ) from None
        except InterviewProviderTransportError:
            raise
        except Exception as exc:  # noqa: BLE001
            msg = self._safe_message(exc)
            outcome = (
                ResponsesOutcome.TIMEOUT.value
                if "timeout" in msg.lower()
                else ResponsesOutcome.INTERNAL_ERROR.value
            )
            raise InterviewProviderTransportError(
                outcome,
                msg,
                provider_id=InterviewProviderId.DEEPSEEK.value,
            ) from None
        return self._raise_mapped(status, payload, text)

    async def acreate(self, request: ResponsesRequest) -> dict[str, Any]:
        body = self._completions_body(request)
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
        except TimeoutError as exc:
            raise InterviewProviderTransportError(
                ResponsesOutcome.TIMEOUT.value,
                self._safe_message(exc),
                provider_id=InterviewProviderId.DEEPSEEK.value,
            ) from None
        except InterviewProviderTransportError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise InterviewProviderTransportError(
                ResponsesOutcome.INTERNAL_ERROR.value,
                self._safe_message(exc),
                provider_id=InterviewProviderId.DEEPSEEK.value,
            ) from None
        return self._raise_mapped(status, payload, text)


# Historical alias (STORY-59 deferred name) — same concrete adapter after STORY-60.
DeferredDeepSeekInterviewClient = DeepSeekChatCompletionsClient


@dataclass(frozen=True)
class DeepSeekInterviewProvider:
    """Interview port binding for provider=deepseek (L12-3 nest required)."""

    api_key: str
    base_url: str
    model: str

    @property
    def provider_id(self) -> InterviewProviderId:
        return InterviewProviderId.DEEPSEEK

    def model_id(self) -> str:
        return self.model

    def build_client(
        self,
        *,
        timeout_ms: int,
        connect_timeout_ms: int,
    ) -> ResponsesClient:
        return DeepSeekChatCompletionsClient(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model,
            timeout_ms=timeout_ms,
            connect_timeout_ms=connect_timeout_ms,
        )
