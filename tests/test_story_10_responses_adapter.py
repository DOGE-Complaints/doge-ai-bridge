"""STORY-AIBRIDGE-10 — production Responses adapter, flat tools, prompt xor."""

from __future__ import annotations

import asyncio

import pytest

from aibridge.history import HistoryStore
from aibridge.interview import InterviewEngine, default_recording_engine
from aibridge.responses_client import (
    DualInstructionsError,
    ProductionResponsesClient,
    RecordingResponsesClient,
    RecordingResponsesTransport,
    ResponsesOutcome,
    ResponsesTransportError,
    assert_prompt_xor,
    assemble_responses_request,
    parse_responses_payload,
    redact_secrets,
)
from aibridge.tool_gen import generate_strict_tool, to_responses_flat_tool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIRE_OAS = ROOT / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
PACK = ROOT / "tests" / "fixtures" / "content" / "pack" / "payload.schema.json"


def _ok_payload_with_tool() -> dict:
    return {
        "id": "resp_fc_1",
        "output": [
            {
                "type": "reasoning",
                "summary": [{"type": "summary_text", "text": "think"}],
            },
            {
                "type": "function_call",
                "call_id": "call_abc",
                "name": "postStoryDraftStash",
                "arguments": '{"schema_binding":{}}',
            },
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "ready"}],
            },
        ],
        "usage": {
            "input_tokens": 100,
            "output_tokens": 20,
            "input_tokens_details": {"cached_tokens": 40},
        },
    }


# --- t01 client knobs ---


def test_client_knobs_store_parallel_max_tokens() -> None:
    transport = RecordingResponsesTransport(
        scripted=[(200, {"id": "r1", "output": [], "usage": {}}, "{}")]
    )
    client = ProductionResponsesClient(
        api_key="sk-secret-key-should-not-leak",
        max_output_tokens=512,
        timeout_ms=12_000,
        connect_timeout_ms=2_000,
        transport=transport,
    )
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
    )
    client.create(req)
    sent = transport.calls[0]["json_body"]
    assert sent["store"] is False
    assert sent["parallel_tool_calls"] is False
    assert sent["max_output_tokens"] == 512
    assert transport.calls[0]["timeout_seconds"] == 12.0
    assert transport.calls[0]["connect_timeout_seconds"] == 2.0


def test_client_maps_429_and_redacts_key() -> None:
    transport = RecordingResponsesTransport(
        scripted=[(429, None, "Bearer sk-secret-key-should-not-leak rate limit")]
    )
    client = ProductionResponsesClient(
        api_key="sk-secret-key-should-not-leak",
        transport=transport,
    )
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=64,
    )
    with pytest.raises(ResponsesTransportError) as exc_info:
        client.create(req)
    assert exc_info.value.outcome == ResponsesOutcome.RATE_LIMITED.value
    assert "sk-secret-key-should-not-leak" not in str(exc_info.value)


def test_client_timeout_outcome() -> None:
    transport = RecordingResponsesTransport(raise_timeout=True)
    client = ProductionResponsesClient(api_key="sk-x", transport=transport)
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=64,
    )
    with pytest.raises(ResponsesTransportError) as exc_info:
        client.create(req)
    assert exc_info.value.outcome == ResponsesOutcome.TIMEOUT.value


def test_client_5xx_maps_transient_failure() -> None:
    transport = RecordingResponsesTransport(scripted=[(503, None, "upstream unavailable")])
    client = ProductionResponsesClient(api_key="sk-x", transport=transport)
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=64,
    )
    with pytest.raises(ResponsesTransportError) as exc_info:
        client.create(req)
    assert exc_info.value.outcome == ResponsesOutcome.TRANSIENT_FAILURE.value


def test_acreate_awaits_async_transport() -> None:
    """Real async path — RecordingAsyncResponsesTransport, not callable-only."""
    from aibridge.responses_client import RecordingAsyncResponsesTransport

    async_transport = RecordingAsyncResponsesTransport(
        scripted=[(200, {"id": "async-1", "output": [], "usage": {}}, "{}")]
    )
    client = ProductionResponsesClient(
        api_key="sk-secret",
        async_transport=async_transport,
    )
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=128,
    )

    async def _run() -> dict:
        return await client.acreate(req)

    out = asyncio.run(_run())
    assert out["id"] == "async-1"
    assert len(async_transport.calls) == 1
    assert async_transport.calls[0]["json_body"]["store"] is False


def test_arun_turn_uses_acreate() -> None:
    client = RecordingResponsesClient(
        scripted=[
            {
                "id": "resp_async",
                "output": [
                    {
                        "type": "message",
                        "role": "assistant",
                        "content": [{"type": "output_text", "text": "async-ok"}],
                    }
                ],
                "usage": {"input_tokens": 1, "output_tokens": 1, "cached_tokens": 0},
            }
        ]
    )
    engine = InterviewEngine(client=client, instructions="sys")

    async def _run() -> dict:
        return await engine.arun_turn(session_id="s-async", user_text="hello")

    result = asyncio.run(_run())
    assert result["ok"] is True
    assert result["reply_text"] == "async-ok"
    assert len(client.calls) == 1


def test_redact_secrets_helper() -> None:
    assert "sk-abc" not in redact_secrets("key=sk-abc leaked", "sk-abc")


# --- t02 parse + replay ---


def test_parse_function_call_and_cached_tokens() -> None:
    parsed = parse_responses_payload(_ok_payload_with_tool())
    assert len(parsed.function_calls) == 1
    assert parsed.function_calls[0].call_id == "call_abc"
    assert parsed.function_calls[0].name == "postStoryDraftStash"
    assert parsed.cached_input_tokens == 40
    assert len(parsed.output_items) == 3  # reasoning + function_call + message
    assert parsed.reply_text == "ready"


def test_interview_preserves_all_output_items() -> None:
    client = RecordingResponsesClient(scripted=[_ok_payload_with_tool()])
    history = HistoryStore()
    engine = InterviewEngine(client=client, history=history, instructions="sys")
    result = engine.run_turn(session_id="s1", user_text="hi")
    assert result["ok"] is True
    assert result["function_calls"][0]["call_id"] == "call_abc"
    assert result["cached_input_tokens"] == 40
    items = history.list_items("s1")
    types = [i.get("type") for i in items if isinstance(i, dict)]
    assert "function_call" in types
    assert "reasoning" in types
    assert "message" in types


# --- t03 flat tools ---


def test_flat_tool_schema_from_generator() -> None:
    tool = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK,
        schema_id="tallinn_civic",
        schema_version="v1",
    )
    assert tool["type"] == "function"
    assert "function" not in tool
    assert set(tool) >= {"type", "name", "parameters", "strict"}


def test_to_responses_flat_tool_normalizes_nested() -> None:
    nested = {
        "type": "function",
        "function": {
            "name": "postStoryDraftStash",
            "strict": True,
            "parameters": {"type": "object"},
        },
    }
    flat = to_responses_flat_tool(nested)
    assert flat["name"] == "postStoryDraftStash"
    assert "function" not in flat


# --- t04 prompt xor ---


def test_prompt_xor_fails_when_both() -> None:
    with pytest.raises(DualInstructionsError):
        assert_prompt_xor(has_stable_prefix=True, instructions="also")


def test_prompt_xor_prefix_channel_omits_instructions() -> None:
    engine = default_recording_engine(instructions="canon", prompt_channel="prefix")
    engine.run_turn(session_id="s1", user_text="x")
    sent = engine.client.calls[0]
    assert "instructions" not in sent
    assert any(
        i.get("role") == "system" for i in sent["input"] if isinstance(i, dict)
    )


def test_prompt_xor_instructions_channel_skips_system_prefix() -> None:
    engine = default_recording_engine(
        instructions="canon-only", prompt_channel="instructions"
    )
    engine.run_turn(session_id="s2", user_text="x")
    sent = engine.client.calls[0]
    assert sent.get("instructions") == "canon-only"
    assert not any(
        isinstance(i, dict)
        and i.get("role") == "system"
        and str(i.get("content", "")).startswith("<<<INSTRUCTIONS>>>")
        for i in sent["input"]
    )
