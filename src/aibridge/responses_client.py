"""Responses request assembly — always store:false; parallel_tool_calls:false."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ResponsesRequest:
    """Assembled Responses API payload (not sent until client.call)."""

    payload: dict[str, Any]

    @property
    def store(self) -> bool:
        return bool(self.payload.get("store"))


def assemble_responses_request(
    *,
    model: str,
    input_items: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    instructions: str | None = None,
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
    return ResponsesRequest(payload=payload)


class ResponsesClient(Protocol):
    def create(self, request: ResponsesRequest) -> dict[str, Any]: ...


class RecordingResponsesClient:
    """Test double — records payloads; never contacts OpenAI or gateway."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.gateway_calls: int = 0

    def create(self, request: ResponsesRequest) -> dict[str, Any]:
        assert request.payload.get("store") is False
        assert request.payload.get("parallel_tool_calls") is False
        self.calls.append(dict(request.payload))
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

    def call_gateway(self) -> None:
        """Must never be invoked on budget breach paths."""
        self.gateway_calls += 1
