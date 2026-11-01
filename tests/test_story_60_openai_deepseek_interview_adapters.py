"""STORY-AIBRIDGE-60 — OpenAI + DeepSeek interview adapters (AC-AIB-12-03)."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from aibridge.config import Settings, reset_settings_cache
from aibridge.interview import InterviewEngine
from aibridge.interview_providers import (
    InterviewProviderConfigError,
    InterviewProviderFailureClass,
    InterviewProviderId,
    InterviewProviderTransportError,
    bind_interview_engine_at_wire,
    port_from_settings,
)
from aibridge.interview_providers.deepseek_slot import (
    DeepSeekChatCompletionsClient,
    DeepSeekInterviewProvider,
    completions_payload_to_engine_dict,
    responses_input_to_chat_messages,
    responses_tools_to_completions,
)
from aibridge.interview_providers.openai_slot import OpenAIInterviewProvider
from aibridge.responses_client import (
    ProductionResponsesClient,
    RecordingResponsesTransport,
    ResponsesRequest,
    ResponsesTransportError,
)


CHANNEL_TOKEN = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY_TOKEN = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = {
        "_env_file": None,
        "AIBRIDGE_CHANNEL_BEARER_TOKEN": CHANNEL_TOKEN,
        "GATEWAY_SERVICE_API_TOKEN": GATEWAY_TOKEN,
        "GATEWAY_BASE_URL": "https://gateway.example.invalid",
        "SPA_BASE_URL": "https://spa.example.invalid",
        "OPENAI_API_KEY": "sk-test-not-real",
        "OPENAI_MODEL": "gpt-test",
        "AIBRIDGE_INTERVIEW_PROVIDER": "openai",
        "AIBRIDGE_DRY_RUN": True,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def _deepseek_settings(**overrides: object) -> Settings:
    base = {
        "AIBRIDGE_INTERVIEW_PROVIDER": "deepseek",
        "AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY": "ds-key",
        "AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL": "https://api.deepseek.com",
        "AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL": "deepseek-v4-pro",
    }
    base.update(overrides)
    return _settings(**base)


def _scripted_completions_ok(text: str = "hello-ds") -> RecordingResponsesTransport:
    return RecordingResponsesTransport(
        scripted=[
            (
                200,
                {
                    "id": "chatcmpl_fixture",
                    "choices": [
                        {"message": {"role": "assistant", "content": text}}
                    ],
                    "usage": {
                        "prompt_tokens": 3,
                        "completion_tokens": 2,
                        "total_tokens": 5,
                    },
                },
                "",
            )
        ]
    )


# --- t01 OpenAI Keep ---


def test_t01_openai_adapter_keep_production_responses_client() -> None:
    port = port_from_settings(_settings())
    assert isinstance(port, OpenAIInterviewProvider)
    client = port.build_client(timeout_ms=5000, connect_timeout_ms=1000)
    assert isinstance(client, ProductionResponsesClient)
    engine = bind_interview_engine_at_wire(
        _settings(), timeout_ms=5000, connect_timeout_ms=1000
    )
    assert isinstance(engine.client, ProductionResponsesClient)
    assert engine.model == "gpt-test"


# --- t02 DeepSeek Chat Completions + L12-3 ---


def test_t02_deepseek_adapter_chat_completions_l12_3() -> None:
    port = port_from_settings(_deepseek_settings())
    assert isinstance(port, DeepSeekInterviewProvider)
    assert port.model_id() == "deepseek-v4-pro"
    client = port.build_client(timeout_ms=2000, connect_timeout_ms=500)
    assert isinstance(client, DeepSeekChatCompletionsClient)
    client.transport = _scripted_completions_ok()
    out = client.create(
        ResponsesRequest(
            payload={
                "model": "deepseek-v4-pro",
                "input": [{"type": "message", "role": "user", "content": "hi"}],
                "store": False,
                "max_output_tokens": 64,
            }
        )
    )
    call = client.transport.calls[0]
    assert call["url"] == "https://api.deepseek.com/chat/completions"
    assert call["json_body"]["model"] == "deepseek-v4-pro"
    assert call["json_body"]["messages"][0]["role"] == "user"
    assert call["json_body"]["max_tokens"] == 64
    assert "Authorization" in call["headers"]
    assert out["aibridge_parsed"]["reply_text"] == "hello-ds"
    assert out["usage"]["input_tokens"] == 3


def test_t02_deepseek_reads_only_l12_3_nest() -> None:
    s = _deepseek_settings(OPENAI_API_KEY="", OPENAI_MODEL="")
    port = port_from_settings(s)
    assert port.provider_id is InterviewProviderId.DEEPSEEK
    src = inspect.getsource(DeepSeekInterviewProvider.build_client)
    assert "OPENAI" not in src
    assert "openai" not in src.lower()


# --- t03 narrow surface Keep Engine ---


def test_t03_narrow_surface_keep_interview_engine() -> None:
    client = DeepSeekChatCompletionsClient(
        api_key="ds-key",
        base_url="https://api.deepseek.com",
        model="deepseek-v4-pro",
        transport=_scripted_completions_ok("engine-ok"),
    )
    engine = InterviewEngine(client=client, model="deepseek-v4-pro")
    result = engine.run_turn(session_id="s60", user_text="ping")
    assert result["ok"] is True
    assert result["reply_text"] == "engine-ok"
    assert result["gateway_called"] is False
    # OpenAI path still Keep Engine
    oa = bind_interview_engine_at_wire(
        _settings(), timeout_ms=3000, connect_timeout_ms=500
    )
    assert type(oa).__name__ == "InterviewEngine"


def test_t03_messages_and_tools_mapping() -> None:
    msgs = responses_input_to_chat_messages(
        [
            {"type": "message", "role": "system", "content": "sys"},
            {"type": "message", "role": "user", "content": "u"},
            {
                "type": "function_call",
                "call_id": "c1",
                "name": "stash",
                "arguments": "{}",
            },
            {"type": "function_call_output", "call_id": "c1", "output": "ok"},
        ],
        instructions="instr",
    )
    assert msgs[0] == {"role": "system", "content": "instr"}
    assert msgs[1]["role"] == "system"
    assert msgs[-1]["role"] == "tool"
    tools = responses_tools_to_completions(
        [{"type": "function", "name": "stash", "parameters": {"type": "object"}}]
    )
    assert tools is not None
    assert tools[0]["function"]["name"] == "stash"
    mapped = completions_payload_to_engine_dict(
        {
            "id": "x",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "tc1",
                                "type": "function",
                                "function": {
                                    "name": "stash",
                                    "arguments": '{"a":1}',
                                },
                            }
                        ],
                    }
                }
            ],
            "usage": {},
        }
    )
    assert mapped["output"][0]["type"] == "function_call"
    assert mapped["aibridge_parsed"]["function_calls"][0]["name"] == "stash"


# --- t04 no silent OpenAI ---


def test_t04_no_silent_openai_when_deepseek() -> None:
    s = _deepseek_settings(
        OPENAI_API_KEY="sk-would-be-wrong",
        OPENAI_MODEL="gpt-would-be-wrong",
    )
    port = port_from_settings(s)
    client = port.build_client(timeout_ms=1000, connect_timeout_ms=500)
    assert isinstance(client, DeepSeekChatCompletionsClient)
    assert not isinstance(client, ProductionResponsesClient)
    client.transport = _scripted_completions_ok("ds-only")
    client.create(
        ResponsesRequest(
            payload={
                "model": "deepseek-v4-pro",
                "input": [{"type": "message", "role": "user", "content": "x"}],
                "store": False,
            }
        )
    )
    url = client.transport.calls[0]["url"]
    assert "api.openai.com" not in url
    assert url.endswith("/chat/completions")
    assert "deepseek" in url
    # Incomplete deepseek nest must not fall back to OpenAI
    bad = _settings(
        AIBRIDGE_INTERVIEW_PROVIDER="deepseek",
        AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY="",
        AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL="https://api.deepseek.com",
        AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL="deepseek-v4-pro",
        OPENAI_API_KEY="sk-present",
        OPENAI_MODEL="gpt-present",
    )
    with pytest.raises(InterviewProviderConfigError) as ei:
        port_from_settings(bad)
    assert ei.value.failure_class is InterviewProviderFailureClass.INCOMPLETE


# --- t05 error classes ---


def test_t05_error_classes_config_vs_vendor_transport() -> None:
    assert InterviewProviderFailureClass.MISSING.value.startswith("interview_")
    assert InterviewProviderFailureClass.VENDOR_TRANSPORT.value == (
        "interview_provider_vendor_transport"
    )
    with pytest.raises(InterviewProviderConfigError):
        port_from_settings(_settings(AIBRIDGE_INTERVIEW_PROVIDER=""))
    client = DeepSeekChatCompletionsClient(
        api_key="ds-key",
        base_url="https://api.deepseek.com",
        model="deepseek-v4-pro",
        transport=RecordingResponsesTransport(
            scripted=[(500, None, "upstream boom")]
        ),
    )
    with pytest.raises(InterviewProviderTransportError) as ei:
        client.create(
            ResponsesRequest(
                payload={
                    "model": "deepseek-v4-pro",
                    "input": [{"type": "message", "role": "user", "content": "x"}],
                    "store": False,
                }
            )
        )
    assert ei.value.failure_class is InterviewProviderFailureClass.VENDOR_TRANSPORT
    assert isinstance(ei.value, ResponsesTransportError)
    assert ei.value.outcome == "transient_failure"
    assert ei.value.provider_id == "deepseek"


# --- t06 module home ≠ providers ---


def test_t06_module_home_ne_worker_providers() -> None:
    import aibridge.interview_providers as ip
    import aibridge.interview_providers.deepseek_slot as ds
    import aibridge.interview_providers.openai_slot as oa

    home = Path(ip.__file__ or "").resolve().parent
    assert home.name == "interview_providers"
    assert (home.parent / "providers").is_dir()
    assert home != (home.parent / "providers")
    assert "providers" not in Path(ds.__file__).parts[-2:]
    assert Path(oa.__file__).parent == home
    # worker registry must not be imported by deepseek adapter
    src = Path(ds.__file__).read_text(encoding="utf-8")
    assert "from aibridge.providers" not in src
    assert "import aibridge.providers" not in src



# --- t07 no gateway send permission ---


def test_t07_adapter_no_gateway_send_permission() -> None:
    client = DeepSeekChatCompletionsClient(
        api_key="ds-key",
        base_url="https://api.deepseek.com",
        model="deepseek-v4-pro",
        transport=_scripted_completions_ok("no-gw"),
    )
    engine = InterviewEngine(client=client, model="deepseek-v4-pro")
    before = engine.gateway_invocations
    result = engine.run_turn(session_id="s60-gw", user_text="hi")
    assert result["ok"] is True
    assert result["gateway_called"] is False
    assert engine.gateway_invocations == before
    # Adapter modules must not call gateway send paths
    for mod_path in (
        Path(__file__).resolve().parents[1]
        / "src/aibridge/interview_providers/deepseek_slot.py",
        Path(__file__).resolve().parents[1]
        / "src/aibridge/interview_providers/openai_slot.py",
    ):
        text = mod_path.read_text(encoding="utf-8")
        assert "call_gateway" not in text
        assert "gateway_invocations" not in text
        assert "/v1/stories" not in text


# --- t08 story gate harness AC-03 ---


def test_t08_story_gate_both_adapters_harness() -> None:
    # OpenAI harness (RecordingResponsesClient via Engine — port still Production)
    oa_port = port_from_settings(_settings())
    assert oa_port.provider_id is InterviewProviderId.OPENAI
    assert isinstance(
        oa_port.build_client(timeout_ms=1000, connect_timeout_ms=500),
        ProductionResponsesClient,
    )
    # DeepSeek harness fixture Completions → Engine
    ds_client = DeepSeekChatCompletionsClient(
        api_key="ds-key",
        base_url="https://api.deepseek.com",
        model="deepseek-v4-pro",
        transport=_scripted_completions_ok("gate-pass"),
    )
    engine = InterviewEngine(client=ds_client, model="deepseek-v4-pro")
    out = engine.run_turn(session_id="gate", user_text="ready")
    assert out["ok"] is True
    assert out["reply_text"] == "gate-pass"
    # OOS: live Pass (61) — no live HTTP claim here
    assert "api.openai.com" not in ds_client.transport.calls[0]["url"]
