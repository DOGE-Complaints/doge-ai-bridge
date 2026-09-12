"""t05 — /actions fail-closed 4xx for bad tokens."""

from __future__ import annotations

import time

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore


def _client_with_guard(
    settings: Settings, guard: ConfirmationGuard
) -> TestClient:
    reset_settings_cache()
    reset_confirmation_guard(guard)
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        confirmation_guard=guard,
    )
    return TestClient(app)


def test_unknown_token_404(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    client = _client_with_guard(settings, ConfirmationGuard())
    payload = {
        "channel": "telegram",
        "event_id": "e-unknown",
        "callback_query_id": "cb",
        "principal": {"user_id": "1", "chat_id": "2"},
        "action_token": "not-a-real-token",
    }
    r = client.post("/v1/channel/actions", json=payload, headers=auth_header)
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


def test_foreign_token_403(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = acts[0]["token"]
    client = _client_with_guard(settings, g)
    payload = {
        "channel": "telegram",
        "event_id": "e-foreign",
        "callback_query_id": "cb",
        "principal": {"user_id": "999", "chat_id": "2"},
        "action_token": tok,
    }
    r = client.post("/v1/channel/actions", json=payload, headers=auth_header)
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "forbidden"


def test_expired_token_409(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    g = ConfirmationGuard()
    g.tokens.ttl_seconds = 1
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = acts[0]["token"]
    # Force expiry on record.
    rec = g.tokens.lookup(tok)
    rec.expires_at = time.time() - 1
    client = _client_with_guard(settings, g)
    payload = {
        "channel": "telegram",
        "event_id": "e-expired",
        "callback_query_id": "cb",
        "principal": {"user_id": "1", "chat_id": "2"},
        "action_token": tok,
    }
    r = client.post("/v1/channel/actions", json=payload, headers=auth_header)
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "conflict"


def test_consumed_token_409(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    client = _client_with_guard(settings, g)
    payload = {
        "channel": "telegram",
        "event_id": "e-consume-1",
        "callback_query_id": "cb1",
        "principal": {"user_id": "1", "chat_id": "2"},
        "action_token": tok,
    }
    r1 = client.post("/v1/channel/actions", json=payload, headers=auth_header)
    assert r1.status_code == 200
    payload2 = {**payload, "event_id": "e-consume-2", "callback_query_id": "cb2"}
    r2 = client.post("/v1/channel/actions", json=payload2, headers=auth_header)
    assert r2.status_code == 409


def test_valid_minted_token_200(
    settings: Settings, auth_header: dict[str, str]
) -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="42", chat_id="99")
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    client = _client_with_guard(settings, g)
    payload = {
        "channel": "telegram",
        "event_id": "2002",
        "callback_query_id": "cb-1",
        "principal": {"user_id": "42", "chat_id": "99"},
        "action_token": tok,
    }
    r = client.post("/v1/channel/actions", json=payload, headers=auth_header)
    assert r.status_code == 200
    body = r.json()
    assert "callback_ack_text" not in body
    assert body["state"] == "interpretation_confirmed"
