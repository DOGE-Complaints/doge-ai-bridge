"""t01 — Responses store:false + local history."""

from __future__ import annotations

from aibridge.history import HistoryStore
from aibridge.interview import default_recording_engine
from aibridge.responses_client import (
    RecordingResponsesClient,
    assemble_responses_request,
)


def test_assemble_responses_request_always_store_false() -> None:
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        tools=[{"type": "function", "name": "x", "strict": True, "parameters": {}}],
        max_output_tokens=256,
    )
    assert req.store is False
    assert req.payload["store"] is False
    assert req.payload["parallel_tool_calls"] is False
    assert req.payload["max_output_tokens"] == 256


def test_recording_client_rejects_store_true_path() -> None:
    client = RecordingResponsesClient()
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "a"}],
    )
    out = client.create(req)
    assert out["id"].startswith("resp_test_")
    assert client.calls[0]["store"] is False


def test_history_replay_and_interview_turn() -> None:
    history = HistoryStore()
    history.append("s1", {"type": "message", "role": "user", "content": "one"})
    assert len(history.list_items("s1")) == 1

    engine = default_recording_engine(history=history)
    result = engine.run_turn(session_id="s1", user_text="two")
    assert result["ok"] is True
    assert result["store"] is False
    assert result["gateway_called"] is False
    items = history.list_items("s1")
    assert any(i.get("content") == "two" for i in items)
    assert isinstance(engine.client, RecordingResponsesClient)
    assert engine.client.calls[0]["store"] is False
