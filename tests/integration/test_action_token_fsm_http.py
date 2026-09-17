"""STORY-AIBRIDGE-29 — ACT-* HTTP façade (integration; no live Telegram)."""

from __future__ import annotations

import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayExecutor, RecordingGatewayTransport

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402


def _client(settings: Settings, guard: ConfirmationGuard) -> TestClient:
    reset_settings_cache()
    reset_confirmation_guard(guard)
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        confirmation_guard=guard,
    )
    return TestClient(app)


def _post(client: TestClient, body: dict, auth_header: dict[str, str]):
    return client.post("/v1/channel/actions", json=body, headers=auth_header)


def test_act_001_http_looks_right_200(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    env = load_fixture("channel", "act-looks-right")
    expect = env["payload"]["expect"]
    g = ConfirmationGuard()
    transport = RecordingGatewayTransport(scripted=[])
    g.executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        channel_bearer="ch",
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    body = dict(env["payload"]["body"])
    assert body["action_token"] == "PLACEHOLDER_TOKEN"
    uid, cid = body["principal"]["user_id"], body["principal"]["chat_id"]
    sess = g.get_or_create_session(user_id=uid, chat_id=cid)
    acts = g.offer_interpretation_confirm(sess.session_id)
    body["action_token"] = next(a["token"] for a in acts if a["style"] == "success")
    client = _client(settings, g)
    r = _post(client, body, auth_header)
    assert r.status_code == expect["http_status"]
    assert r.json()["state"] == expect["state"]
    assert transport.calls == []


def test_act_005_http_random_404(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    env = load_fixture("channel", "act-random-token")
    expect = env["payload"]["expect"]
    client = _client(settings, ConfirmationGuard())
    r = _post(client, env["payload"]["body"], auth_header)
    assert r.status_code == expect["http_status"]
    assert r.json()["error"]["code"] == expect["error_code"]


def test_act_006_http_foreign_user_403(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    env = load_fixture("channel", "act-foreign-user")
    spy = load_fixture("spies", "act-reject-403")["payload"]
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="501122334", chat_id="501122334")
    acts = g.offer_interpretation_confirm(sess.session_id)
    body = dict(env["payload"]["body"])
    body["action_token"] = next(a["token"] for a in acts if a["style"] == "success")
    client = _client(settings, g)
    r = _post(client, body, auth_header)
    assert r.status_code == spy["http_status"]
    assert r.json()["error"]["code"] == spy["error_code"]


def test_act_007_http_foreign_chat_403(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    env = load_fixture("channel", "act-foreign-chat")
    spy = load_fixture("spies", "act-reject-403")["payload"]
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="501122334", chat_id="501122334")
    acts = g.offer_interpretation_confirm(sess.session_id)
    body = dict(env["payload"]["body"])
    body["action_token"] = next(a["token"] for a in acts if a["style"] == "success")
    client = _client(settings, g)
    r = _post(client, body, auth_header)
    assert r.status_code == spy["http_status"]
    assert r.json()["error"]["code"] == spy["error_code"]


def test_act_008_http_expired_409(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    env = load_fixture("channel", "act-expired")
    spy = load_fixture("spies", "act-reject-409")["payload"]
    g = ConfirmationGuard()
    body = dict(env["payload"]["body"])
    uid, cid = "501122334", "501122334"
    sess = g.get_or_create_session(user_id=uid, chat_id=cid)
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    g.tokens.lookup(tok).expires_at = time.time() - 1
    body["action_token"] = tok
    body["principal"] = {"user_id": uid, "chat_id": cid}
    client = _client(settings, g)
    r = _post(client, body, auth_header)
    assert r.status_code == spy["http_status"]
    assert r.json()["error"]["code"] == spy["error_code"]


def test_act_009_http_consumed_retry_409(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    spy = load_fixture("spies", "act-reject-409")["payload"]
    g = ConfirmationGuard()
    uid, cid = "501122334", "501122334"
    sess = g.get_or_create_session(user_id=uid, chat_id=cid)
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    body1 = {
        "channel": "telegram",
        "event_id": "act-009-a",
        "callback_query_id": "cq-a",
        "principal": {"user_id": uid, "chat_id": cid},
        "action_token": tok,
    }
    client = _client(settings, g)
    assert _post(client, body1, auth_header).status_code == 200
    body2 = {**body1, "event_id": "act-009-b", "callback_query_id": "cq-b"}
    r2 = _post(client, body2, auth_header)
    assert r2.status_code == spy["http_status"]


def test_act_018_http_token_len_65_422(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    env = load_fixture("channel", "act-token-len-65")
    spy = load_fixture("spies", "act-facade-422")["payload"]
    client = _client(settings, ConfirmationGuard())
    r = _post(client, env["payload"]["body"], auth_header)
    assert r.status_code == spy["http_status"]
    assert r.json()["error"]["code"] == spy["error_code"]
