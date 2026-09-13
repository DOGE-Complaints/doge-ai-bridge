"""STORY-AIBRIDGE-15 — n8n/Telegram gate contract (no live Bot secrets).

Documents REQ-03 §6.1 mapping formulas and façade binding. Live Telegram proof is
ops checklist evidence — see docs/ops/n8n-channel-workflow/live-evidence-BLOCKED-*.md.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from story13_e2e_helpers import (
    action_body,
    build_e2e_harness,
    fc_openai_payload,
    ok_201,
    pg_available,
    text_openai_payload,
    turn_body,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
OAS_PATH = REPO_ROOT / "docs" / "openapi" / "aibridge-channel-v1.openapi.yaml"
CHECKLIST = (
    REPO_ROOT
    / "docs"
    / "ops"
    / "n8n-channel-workflow"
    / "r3-p1-09-live-gate-checklist.md"
)
N8N_README = REPO_ROOT / "docs" / "ops" / "n8n-channel-workflow" / "README.md"

pytestmark_pg = pytest.mark.skipif(
    not pg_available(),
    reason="disposable Postgres (.pgdata-test) not running — ./scripts/start-disposable-pg.sh",
)


def telegram_event_id(update_id: int | str) -> str:
    """n8n MUST use String(update.update_id) — never mint UUID on HTTP retry."""
    return str(update_id)


def map_telegram_message_to_turns(update: dict) -> dict:
    """Mirror docs/ops/n8n-channel-workflow/README.md §3 turns mapping."""
    msg = update["message"]
    return {
        "channel": "telegram",
        "event_id": telegram_event_id(update["update_id"]),
        "principal": {
            "user_id": str(msg["from"]["id"]),
            "chat_id": str(msg["chat"]["id"]),
        },
        "message": {
            "message_id": str(msg["message_id"]),
            "text": msg.get("text") or "",
        },
    }


def map_telegram_callback_to_actions(update: dict, *, action_token: str) -> dict:
    """Mirror README §3 actions mapping — event_id stays update_id."""
    cq = update["callback_query"]
    return {
        "channel": "telegram",
        "event_id": telegram_event_id(update["update_id"]),
        "callback_query_id": str(cq["id"]),
        "principal": {
            "user_id": str(cq["from"]["id"]),
            "chat_id": str(cq["message"]["chat"]["id"]),
        },
        "action_token": action_token,
    }


def test_story_15_checklist_ssot_on_disk() -> None:
    assert CHECKLIST.is_file()
    text = CHECKLIST.read_text(encoding="utf-8")
    for needle in (
        "answerCallbackQuery",
        "event_id",
        "story-drafts",
        "channel Bearer",
        "callback_data",
        "session_id",
    ):
        assert needle in text
    readme = N8N_README.read_text(encoding="utf-8")
    assert "r3-p1-09-live-gate-checklist.md" in readme
    assert "String(update.update_id)" in readme or "update.update_id" in readme


def test_story_15_oas_channel_enum_telegram_only() -> None:
    spec = yaml.safe_load(OAS_PATH.read_text(encoding="utf-8"))
    turn_ch = spec["components"]["schemas"]["ChannelTurnRequest"]["properties"]["channel"]
    act_ch = spec["components"]["schemas"]["ChannelActionRequest"]["properties"]["channel"]
    assert turn_ch.get("enum") == ["telegram"]
    assert act_ch.get("enum") == ["telegram"]
    # Do not invent callback_ack_text
    success = spec["components"]["schemas"]["ChannelSuccessResponse"]["properties"]
    assert "callback_ack_text" not in success


def test_story_15_event_id_derivation_stable_across_retry() -> None:
    update_id = 987654321
    first = telegram_event_id(update_id)
    retry = telegram_event_id(update_id)
    assert first == retry == "987654321"
    # Callback path must not swap in callback_query.id
    update = {
        "update_id": update_id,
        "callback_query": {
            "id": "cq-different",
            "from": {"id": 42},
            "message": {"chat": {"id": -100}},
            "data": "opaque-token",
        },
    }
    body = map_telegram_callback_to_actions(update, action_token="opaque-token")
    assert body["event_id"] == "987654321"
    assert body["callback_query_id"] == "cq-different"
    assert body["event_id"] != body["callback_query_id"]


def test_story_15_principal_mapping_from_telegram_shapes() -> None:
    update = {
        "update_id": 111,
        "message": {
            "message_id": 7,
            "text": "hello",
            "from": {"id": 42},
            "chat": {"id": -100},
        },
    }
    body = map_telegram_message_to_turns(update)
    assert body["channel"] == "telegram"
    assert body["event_id"] == "111"
    assert body["principal"] == {"user_id": "42", "chat_id": "-100"}
    assert body["message"]["message_id"] == "7"


@pytest.mark.postgres
@pytestmark_pg
def test_story_15_same_event_id_retry_does_not_remint() -> None:
    """HTTP retry with identical event_id → stored replay (no second OpenAI call)."""
    h = build_e2e_harness(openai_scripted=[text_openai_payload("once")])
    # Use deterministic id as n8n would from update.update_id
    eid = telegram_event_id(555001)
    payload = turn_body(event_id=eid, text="retry me")
    r1 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r1.status_code == 200
    calls_after_first = len(h.openai.calls)
    r2 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r2.status_code == 200
    assert len(h.openai.calls) == calls_after_first
    assert r2.json()["session_id"] == r1.json()["session_id"]


@pytest.mark.postgres
@pytestmark_pg
def test_story_15_session_id_stable_for_principal() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("turn a"),
            text_openai_payload("turn b"),
        ]
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id=telegram_event_id(7001), text="a"),
        headers=h.auth_header,
    )
    r2 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id=telegram_event_id(7002), text="b"),
        headers=h.auth_header,
    )
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["session_id"] == r2.json()["session_id"]


@pytest.mark.postgres
@pytestmark_pg
def test_story_15_actions_token_binding_wrong_owner() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_s15"),
        ],
        gateway_scripted=[ok_201()],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id=telegram_event_id(8001), text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id=telegram_event_id(8002), token=interpret_tok
        ),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id=telegram_event_id(8003), text="go"),
        headers=h.auth_header,
    )
    send_tok = next(a["token"] for a in r1.json()["actions"] if a["style"] == "primary")
    r_bad = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id=telegram_event_id(8004),
            token=send_tok,
            user_id="999",
            chat_id="-100",
            callback_query_id="cb15",
        ),
        headers=h.auth_header,
    )
    assert r_bad.status_code == 403
    assert h.transport.calls == []
