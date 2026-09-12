"""t03 — turns/actions validation + success envelope."""

from __future__ import annotations

from fastapi.testclient import TestClient


SUCCESS_KEYS = {
    "request_id",
    "session_id",
    "state",
    "reply_text",
    "actions",
    "outcome",
    "draft_id",
    "continuation_url",
}


def test_valid_turn_200_envelope(
    client: TestClient, auth_header: dict[str, str], turn_payload: dict
) -> None:
    response = client.post(
        "/v1/channel/turns", json=turn_payload, headers=auth_header
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == SUCCESS_KEYS
    assert "callback_ack_text" not in body
    assert body["outcome"] is None
    assert isinstance(body["actions"], list)


def test_valid_action_200(
    client: TestClient, auth_header: dict[str, str]
) -> None:
    payload = {
        "channel": "telegram",
        "event_id": "2002",
        "callback_query_id": "cb-1",
        "principal": {"user_id": "42", "chat_id": "99"},
        "action_token": "opaque-token-1",
    }
    response = client.post(
        "/v1/channel/actions", json=payload, headers=auth_header
    )
    assert response.status_code == 200
    assert "callback_ack_text" not in response.json()


def test_unknown_field_rejected_400(
    client: TestClient, auth_header: dict[str, str], turn_payload: dict
) -> None:
    bad = {**turn_payload, "extra_field": "nope"}
    response = client.post("/v1/channel/turns", json=bad, headers=auth_header)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "bad_request"


def test_malformed_json_400(
    client: TestClient, auth_header: dict[str, str]
) -> None:
    response = client.post(
        "/v1/channel/turns",
        content=b"{not-json",
        headers={**auth_header, "Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "bad_request"


def test_non_decimal_user_id_rejected_422(
    client: TestClient, auth_header: dict[str, str], turn_payload: dict
) -> None:
    turn_payload["principal"]["user_id"] = "not-a-number"
    response = client.post(
        "/v1/channel/turns", json=turn_payload, headers=auth_header
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "semantic_invalid"


def test_action_token_max_length_422(
    client: TestClient, auth_header: dict[str, str]
) -> None:
    payload = {
        "channel": "telegram",
        "event_id": "2003",
        "callback_query_id": "cb-2",
        "principal": {"user_id": "1", "chat_id": "2"},
        "action_token": "x" * 65,
    }
    response = client.post(
        "/v1/channel/actions", json=payload, headers=auth_header
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "semantic_invalid"

def test_content_length_over_limit_413(
    client: TestClient, auth_header: dict[str, str]
) -> None:
    response = client.post(
        "/v1/channel/turns",
        content=b"{}",
        headers={**auth_header, "Content-Length": "999999", "Content-Type": "application/json"},
    )
    assert response.status_code == 413
