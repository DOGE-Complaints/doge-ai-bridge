"""Interview turn orchestration (story 03) — Responses + budgets; no Send/gateway."""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from aibridge.budgets import BudgetBreachError, BudgetGuard
from aibridge.history import HistoryStore
from aibridge.metrics import get_metrics
from aibridge.request_assembly import CacheTelemetry, build_stable_prefix
from aibridge.responses_client import (
    RecordingResponsesClient,
    ResponsesClient,
    assemble_responses_request,
)
from aibridge.turn_lock import SessionTurnLock


@dataclass
class InterviewEngine:
    """Runs a serialized Responses turn with store:false and budget checks."""

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

    def run_turn(self, *, session_id: str, user_text: str) -> dict[str, Any]:
        with self.locks.hold(session_id):
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
            input_items = [
                {"type": "message", "role": "system", "content": prefix},
                *prior,
                user_item,
            ]

            request = assemble_responses_request(
                model=self.model,
                input_items=input_items,
                tools=self.tools or None,
                instructions=self.instructions or None,
            )
            assert request.store is False
            assert request.payload.get("parallel_tool_calls") is False

            if self.budgets is not None:
                try:
                    est_in = max(1, len(user_text) // 4)
                    self.budgets.check_usage(input_tokens=est_in, responses_calls=1)
                except BudgetBreachError as exc:
                    return self._budget_fail(exc, session_id)

            started = time.monotonic()
            response = self.client.create(request)
            get_metrics().inc_openai_calls()
            elapsed_ms = int((time.monotonic() - started) * 1000)
            if self.budgets is not None:
                try:
                    self.budgets.check_elapsed(elapsed_ms)
                except BudgetBreachError as exc:
                    return self._budget_fail(exc, session_id)

            usage = response.get("usage") or {}
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
            for out in response.get("output") or []:
                self.history.append(session_id, out)
            if self.budgets is not None:
                self.budgets.record_turn(session_id)
            self.last_confirmed_state[session_id] = "interviewing"
            cached = int(usage.get("cached_tokens") or 0)
            self.cache.emit(cached_tokens=cached, pack_hash=self.pack_id)

            text = "Acknowledged."
            for out in response.get("output") or []:
                if out.get("type") == "message":
                    for part in out.get("content") or []:
                        if part.get("type") == "output_text":
                            text = str(part.get("text") or text)

            return {
                "ok": True,
                "session_id": session_id,
                "state": "interviewing",
                "reply_text": text,
                "request_id": str(uuid.uuid4()),
                "store": False,
                "gateway_called": False,
            }


def default_recording_engine(**kwargs: Any) -> InterviewEngine:
    return InterviewEngine(client=RecordingResponsesClient(), **kwargs)
