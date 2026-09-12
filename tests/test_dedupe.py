"""t04 — event dedupe."""

from __future__ import annotations

from fastapi.testclient import TestClient

from aibridge.dedupe import EventDedupeStore


def test_duplicate_event_id_same_response(
    client: TestClient,
    auth_header: dict[str, str],
    turn_payload: dict,
    store: EventDedupeStore,
) -> None:
    first = client.post(
        "/v1/channel/turns", json=turn_payload, headers=auth_header
    )
    second = client.post(
        "/v1/channel/turns", json=turn_payload, headers=auth_header
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert store.side_effect_count("telegram", turn_payload["event_id"]) == 1


def test_different_event_ids_independent(
    client: TestClient, auth_header: dict[str, str], turn_payload: dict
) -> None:
    a = client.post("/v1/channel/turns", json=turn_payload, headers=auth_header)
    other = {**turn_payload, "event_id": "1002", "message": {**turn_payload["message"], "text": "other"}}
    b = client.post("/v1/channel/turns", json=other, headers=auth_header)
    assert a.json()["request_id"] != b.json()["request_id"]
