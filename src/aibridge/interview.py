"""Interview turn orchestration (story 03) — Responses + budgets; no Send/gateway."""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Literal

from aibridge.budgets import BudgetBreachError, BudgetGuard
from aibridge.history import HistoryStore
from aibridge.metrics import get_metrics
from aibridge.request_assembly import CacheTelemetry, build_stable_prefix
from aibridge.responses_client import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    RecordingResponsesClient,
    ResponsesClient,
    ResponsesRequest,
    assert_prompt_xor,
    assemble_responses_request,
    cached_input_tokens_from_usage,
    parse_responses_payload,
)
from aibridge.turn_lock import SessionTurnLock


@dataclass
class InterviewEngine:
    """Runs a serialized Responses turn with store:false and budget checks.

    ASGI contract (REQ-03 §5.1): prefer ``await arun_turn(...)`` so production
    clients use ``acreate`` (non-blocking). Sync ``run_turn`` remains for tests /
    non-ASGI callers.
    """

    client: ResponsesClient
    history: HistoryStore = field(default_factory=HistoryStore)
    locks: SessionTurnLock = field(default_factory=SessionTurnLock)
    budgets: BudgetGuard | None = None
    tools: list[dict[str, Any]] = field(default_factory=list)
    model: str = "gpt-test"
    instructions: str = ""
    pack_id: str = ""
    cache: CacheTelemetry = field(default_factory=CacheTelemetry)
    last_confirmed_state: dict[str, str] = field(default_factory=dict)
    gateway_invocations: int = 0
    # R3-P0-13: exactly one prompt channel.
    prompt_channel: Literal["prefix", "instructions"] = "prefix"
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS

    def call_gateway(self) -> None:
        """Send path — must not run on budget breach (story 05)."""
        self.gateway_invocations += 1

    def _budget_fail(self, exc: BudgetBreachError, session_id: str) -> dict[str, Any]:
        return {
            "ok": False,
            "error": "budget_breach",
            "message": exc.reason,
            "metric_reason": exc.metric_reason,
            "state": self.last_confirmed_state.get(session_id, "interviewing"),
            "gateway_called": False,
        }

    def _build_request(
        self, *, session_id: str, user_text: str
    ) -> tuple[ResponsesRequest, dict[str, Any]] | dict[str, Any]:
        """Return (request, user_item) or a budget-fail dict."""
        if self.budgets is not None:
            try:
                self.budgets.check_turn_start(session_id)
            except BudgetBreachError as exc:
                return self._budget_fail(exc, session_id)

        tool_json = json.dumps(self.tools, sort_keys=True, separators=(",", ":"))
        prefix = build_stable_prefix(
            instructions=self.instructions,
            tool_schema_json=tool_json,
            pack_id=self.pack_id,
        )
        self.cache.emit(tool_hash=str(len(tool_json)), pack_hash=self.pack_id)

        prior = self.history.list_items(session_id)
        user_item = {"type": "message", "role": "user", "content": user_text}

        if self.prompt_channel == "prefix":
            assert_prompt_xor(has_stable_prefix=True, instructions=None)
            input_items: list[dict[str, Any]] = [
                {"type": "message", "role": "system", "content": prefix},
                *prior,
                user_item,
            ]
            instructions_kw: str | None = None
        else:
            assert_prompt_xor(has_stable_prefix=False, instructions=self.instructions)
            input_items = [*prior, user_item]
            instructions_kw = self.instructions or None

        request = assemble_responses_request(
            model=self.model,
            input_items=input_items,
            tools=self.tools or None,
            instructions=instructions_kw,
            max_output_tokens=self.max_output_tokens,
        )
        assert request.store is False
        assert request.payload.get("parallel_tool_calls") is False
        assert "max_output_tokens" in request.payload
        if self.prompt_channel == "prefix":
            assert "instructions" not in request.payload

        if self.budgets is not None:
            try:
                est_in = max(1, len(user_text) // 4)
                self.budgets.check_usage(input_tokens=est_in, responses_calls=1)
            except BudgetBreachError as exc:
                return self._budget_fail(exc, session_id)

        return request, user_item

    def _finalize(
        self,
        *,
        session_id: str,
        user_item: dict[str, Any],
        response: dict[str, Any],
        started: float,
    ) -> dict[str, Any]:
        get_metrics().inc_openai_calls()
        elapsed_ms = int((time.monotonic() - started) * 1000)
        if self.budgets is not None:
            try:
                self.budgets.check_elapsed(elapsed_ms)
            except BudgetBreachError as exc:
                return self._budget_fail(exc, session_id)

        parsed = parse_responses_payload(response)
        usage = parsed.usage
        if self.budgets is not None:
            try:
                self.budgets.check_usage(
                    input_tokens=int(usage.get("input_tokens") or 0),
                    output_tokens=int(usage.get("output_tokens") or 0),
                    responses_calls=1,
                )
            except BudgetBreachError as exc:
                return self._budget_fail(exc, session_id)

        self.history.append(session_id, user_item)
        for out in parsed.output_items:
            self.history.append(session_id, out)
        if self.budgets is not None:
            self.budgets.record_turn(session_id)
        self.last_confirmed_state[session_id] = "interviewing"
        cached = parsed.cached_input_tokens or cached_input_tokens_from_usage(usage)
        self.cache.emit(cached_tokens=cached, pack_hash=self.pack_id)

        return {
            "ok": True,
            "session_id": session_id,
            "state": "interviewing",
            "reply_text": parsed.reply_text,
            "request_id": str(uuid.uuid4()),
            "store": False,
            "gateway_called": False,
            "function_calls": [
                {
                    "call_id": fc.call_id,
                    "name": fc.name,
                    "arguments": fc.arguments,
                }
                for fc in parsed.function_calls
            ],
            "replay_items": list(parsed.output_items),
            "cached_input_tokens": cached,
        }

    def submit_function_call_output(
        self,
        *,
        session_id: str,
        call_id: str,
        output: str,
    ) -> dict[str, Any]:
        """Post-gateway follow-up: function_call_output with original call_id."""
        with self.locks.hold(session_id):
            item = {
                "type": "function_call_output",
                "call_id": call_id,
                "output": output,
            }
            prior = self.history.list_items(session_id)
            if self.prompt_channel == "prefix":
                tool_json = json.dumps(self.tools, sort_keys=True, separators=(",", ":"))
                prefix = build_stable_prefix(
                    instructions=self.instructions,
                    tool_schema_json=tool_json,
                    pack_id=self.pack_id,
                )
                assert_prompt_xor(has_stable_prefix=True, instructions=None)
                input_items: list[dict[str, Any]] = [
                    {"type": "message", "role": "system", "content": prefix},
                    *prior,
                    item,
                ]
                instructions_kw: str | None = None
            else:
                assert_prompt_xor(has_stable_prefix=False, instructions=self.instructions)
                input_items = [*prior, item]
                instructions_kw = self.instructions or None
            request = assemble_responses_request(
                model=self.model,
                input_items=input_items,
                tools=self.tools or None,
                instructions=instructions_kw,
                max_output_tokens=self.max_output_tokens,
            )
            response = self.client.create(request)
            return self._finalize(
                session_id=session_id,
                user_item=item,
                response=response,
                started=time.monotonic(),
            )

    def run_turn(self, *, session_id: str, user_text: str) -> dict[str, Any]:
        """Sync path — blocking client.create (tests / non-ASGI)."""
        with self.locks.hold(session_id):
            built = self._build_request(session_id=session_id, user_text=user_text)
            if isinstance(built, dict):
                return built
            request, user_item = built
            started = time.monotonic()
            response = self.client.create(request)
            return self._finalize(
                session_id=session_id,
                user_item=user_item,
                response=response,
                started=started,
            )

    async def arun_turn(self, *, session_id: str, user_text: str) -> dict[str, Any]:
        """ASGI-safe path — prefers client.acreate; else asyncio.to_thread(create)."""
        with self.locks.hold(session_id):
            built = self._build_request(session_id=session_id, user_text=user_text)
            if isinstance(built, dict):
                return built
            request, user_item = built
            started = time.monotonic()
            acreate = getattr(self.client, "acreate", None)
            if acreate is not None:
                response = await acreate(request)
            else:
                response = await asyncio.to_thread(self.client.create, request)
            return self._finalize(
                session_id=session_id,
                user_item=user_item,
                response=response,
                started=started,
            )


def default_recording_engine(**kwargs: Any) -> InterviewEngine:
    return InterviewEngine(client=RecordingResponsesClient(), **kwargs)
