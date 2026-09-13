"""STORY-AIBRIDGE-13 P6 audit gaps G-01/G-02/G-03."""

from __future__ import annotations

import concurrent.futures

import pytest
from fastapi.testclient import TestClient

from aibridge.gateway import GatewayOutcome
from aibridge.pg_runtime import PostgresEventDedupeStore
from story13_e2e_helpers import (
    DISPOSABLE_URL,
    action_body,
    assert_channel_error_conforms,
    assert_channel_success_conforms,
    build_e2e_harness,
    fc_openai_payload,
    followup_openai_payload,
    ok_201,
    pg_available,
    text_openai_payload,
    truncate_pg,
    turn_body,
)

pytestmark = pytest.mark.skipif(
    not pg_available(),
    reason="disposable Postgres (.pgdata-test) not running — ./scripts/start-disposable-pg.sh",
)


def test_story_13_audit_g01_pg_try_begin_single_winner() -> None:
    truncate_pg(DISPOSABLE_URL)
    store = PostgresEventDedupeStore(DISPOSABLE_URL)
    outcomes: list[str] = []

    def _race() -> None:
        _body, status = store.try_begin("telegram", "race-try-begin")
        outcomes.append(status)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda _: _race(), range(4)))

    assert outcomes.count("begin") == 1
    assert outcomes.count("begin") + outcomes.count("inflight") == 4
    store.complete(
        "telegram",
        "race-try-begin",
        {
            "request_id": "r",
            "session_id": "s",
            "state": "interviewing",
            "reply_text": "ok",
            "actions": [],
            "outcome": None,
            "draft_id": None,
            "continuation_url": None,
        },
    )
    body, status = store.try_begin("telegram", "race-try-begin")
    assert status == "hit"
    assert body is not None
    assert body["reply_text"] == "ok"


def test_story_13_audit_g01_asgi_claim_skips_second_openai() -> None:
    h = build_e2e_harness(openai_scripted=[text_openai_payload("First")])
    payload = turn_body(event_id="e2e-claim-1", text="hi")
    r1 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r1.status_code == 200
    assert len(h.openai.calls) == 1
    r2 = h.client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
    assert r2.status_code == 200
    assert r2.json() == r1.json()
    assert len(h.openai.calls) == 1
    assert hasattr(h.app.state.dedupe_store, "try_begin")


def test_story_13_audit_g01_concurrent_asgi_same_event() -> None:
    h = build_e2e_harness(
        openai_scripted=[text_openai_payload("Only once under claim")]
    )
    payload = turn_body(event_id="e2e-conc-1", text="race me")

    def _post() -> tuple[int, dict]:
        client = TestClient(h.app)
        r = client.post("/v1/channel/turns", json=payload, headers=h.auth_header)
        return r.status_code, r.json()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(_post)
        f2 = pool.submit(_post)
        s1, b1 = f1.result()
        s2, b2 = f2.result()

    assert s1 == 200 and s2 == 200
    assert_channel_success_conforms(b1)
    assert_channel_success_conforms(b2)
    assert b1["request_id"] == b2["request_id"]
    assert len(h.openai.calls) == 1


def test_story_13_audit_g02_openapi_409_and_500() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_g02"),
            followup_openai_payload(),
        ],
        gateway_scripted=[ok_201("draft-g02")],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-g02-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-g02-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-g02-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(
        a["token"] for a in r1.json()["actions"] if a["style"] == "primary"
    )
    r_ok = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-g02-s1", token=send_tok, callback_query_id="c1"),
        headers=h.auth_header,
    )
    assert r_ok.status_code == 200
    assert_channel_success_conforms(r_ok.json())
    r409 = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-g02-s2", token=send_tok, callback_query_id="c2"),
        headers=h.auth_header,
    )
    assert r409.status_code == 409
    assert_channel_error_conforms(r409.json())

    async def _boom(*_a: object, **_k: object) -> object:
        raise RuntimeError("forced e2e 500")

    import aibridge.app as app_mod

    original = app_mod.process_turn_async
    app_mod.process_turn_async = _boom  # type: ignore[assignment]
    try:
        client = TestClient(h.app, raise_server_exceptions=False)
        r500 = client.post(
            "/v1/channel/turns",
            json=turn_body(event_id="e2e-g02-500", text="crash"),
            headers=h.auth_header,
        )
        assert r500.status_code == 500
        assert_channel_error_conforms(r500.json())
        assert r500.json()["error"]["code"] == "internal_error"
    finally:
        app_mod.process_turn_async = original  # type: ignore[assignment]


def test_story_13_audit_g02_openapi_401_still() -> None:
    h = build_e2e_harness(openai_scripted=[text_openai_payload("x")])
    r401 = h.client.post(
        "/v1/channel/turns", json=turn_body(event_id="e2e-g02-401", text="hi")
    )
    assert r401.status_code == 401
    assert_channel_error_conforms(r401.json())


def test_story_13_audit_g03_wrong_owner_no_gateway() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_g03"),
        ],
        gateway_scripted=[ok_201()],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-g03-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-g03-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-g03-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(
        a["token"] for a in r1.json()["actions"] if a["style"] == "primary"
    )
    r_bad = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="e2e-g03-bad",
            token=send_tok,
            user_id="999",
            chat_id="-100",
            callback_query_id="cbad",
        ),
        headers=h.auth_header,
    )
    assert r_bad.status_code == 403
    assert_channel_error_conforms(r_bad.json())
    assert h.transport.calls == []


def test_story_13_audit_g03_double_consume_no_second_gateway() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_g03b"),
            followup_openai_payload(),
        ],
        gateway_scripted=[ok_201("draft-g03")],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-g03b-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-g03b-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="e2e-g03b-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(
        a["token"] for a in r1.json()["actions"] if a["style"] == "primary"
    )
    r1s = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-g03b-s1", token=send_tok, callback_query_id="s1"),
        headers=h.auth_header,
    )
    assert r1s.status_code == 200
    assert r1s.json()["outcome"] == GatewayOutcome.STASHED.value
    assert len(h.transport.calls) == 1
    r2s = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="e2e-g03b-s2", token=send_tok, callback_query_id="s2"),
        headers=h.auth_header,
    )
    assert r2s.status_code == 409
    assert_channel_error_conforms(r2s.json())
    assert len(h.transport.calls) == 1
